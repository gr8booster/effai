"""WriterAgent - Deterministic template filler and document generator"""
from fastapi import APIRouter, HTTPException
import logging
import hashlib
import json
from jinja2 import Template
from typing import Dict, Any

from schemas import (
    WriterGenerateInput,
    WriterGenerateOutput,
    ToneType
)
from database import get_pg_pool

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/writer", tags=["writer"])

# Template templates (for POC)
DEBT_VALIDATION_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>Debt Validation Request</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
        .header { text-align: right; margin-bottom: 40px; }
        .content { margin: 20px 0; }
        .signature { margin-top: 60px; }
    </style>
</head>
<body>
    <div class="header">
        <p>{{ consumer_name }}<br>
        {{ consumer_address }}<br>
        {{ date }}</p>
    </div>
    
    <p>{{ recipient_name }}<br>
    Attn: Validation Department</p>
    
    <p>Re: Account Number {{ account_number }}</p>
    
    <div class="content">
        {% if tone == 'formal' %}
        <p>Dear Sir or Madam,</p>
        
        <p>I am writing to formally request validation of the alleged debt you claim I owe, 
        pursuant to my rights under the Fair Debt Collection Practices Act (FDCPA), 
        15 U.S.C. § 1692g.</p>
        
        <p>Please provide the following documentation:</p>
        <ul>
            <li>The original creditor's name and account number</li>
            <li>The original amount of the debt</li>
            <li>Proof that you are licensed to collect debts in my state</li>
            <li>Verification that the statute of limitations has not expired</li>
            <li>A complete account statement from the original creditor</li>
        </ul>
        
        <p>Until you provide proper validation, I expect all collection activities to cease 
        as required by law.</p>
        {% else %}
        <p>Hello,</p>
        
        <p>I'm writing to ask you to validate the debt you say I owe. Under the Fair Debt 
        Collection Practices Act, I have the right to ask for proof.</p>
        
        <p>Please send me:</p>
        <ul>
            <li>Who the original creditor was</li>
            <li>The original amount I owed</li>
            <li>Proof you can collect this debt</li>
            <li>Confirmation this debt isn't too old to collect</li>
            <li>A full statement from the original creditor</li>
        </ul>
        
        <p>Please don't contact me about this debt until you send this information.</p>
        {% endif %}
    </div>
    
    <div class="signature">
        <p>Sincerely,<br><br>
        {{ consumer_name }}</p>
    </div>
    
    <div style="margin-top: 40px; font-size: 8px; color: #ccc;">
        <!-- Provenance: {{ provenance_json }} -->
    </div>
</body>
</html>
"""


@router.post("/generate", response_model=WriterGenerateOutput)
async def generate_document(input_data: WriterGenerateInput):
    """
    Generate document from template with strict field validation
    
    For POC: Returns HTML preview + hash (PDF generation in Phase 2)
    """
    try:
        # Get template
        if input_data.template_id == "debt_validation_v1":
            template_html = DEBT_VALIDATION_TEMPLATE
        else:
            # Try to load from MongoDB
            db = get_mongo_db()
            row = await db.legal_templates.find_one(
                {
                    'template_id': input_data.template_id,
                    'template_version': input_data.template_version
                },
                {'_id': 0}
            )
            
            if not row:
                raise HTTPException(status_code=404, detail="Template not found")
            
            template_html = row['template_html']
        
        # Validate required fields based on template
        required_fields = get_required_fields(input_data.template_id)
        for field in required_fields:
            if field not in input_data.fields:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required field: {field}"
                )
        
        # Sanitize inputs
        sanitized_fields = {k: sanitize_input(v) for k, v in input_data.fields.items()}
        sanitized_fields['tone'] = input_data.tone.value
        
        # Generate provenance JSON
        provenance = {
            "template_id": input_data.template_id,
            "template_version": input_data.template_version,
            "user_id": input_data.user_id,
            "trace_id": input_data.trace_id,
            "tone": input_data.tone.value
        }
        sanitized_fields['provenance_json'] = json.dumps(provenance)
        
        # Render template
        template = Template(template_html)
        rendered_html = template.render(**sanitized_fields)
        
        # Generate hash
        content_hash = hashlib.sha256(rendered_html.encode()).hexdigest()
        
        result = WriterGenerateOutput(
            html_preview=rendered_html,
            hash=content_hash,
            provenance_ref=f"writer_{input_data.trace_id}"
        )
        
        logger.info(f"Document generated: template={input_data.template_id}, hash={content_hash[:8]}...")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Document generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/template/{template_id}")
async def get_template_metadata(template_id: str):
    """Get template metadata from MongoDB"""
    try:
        if template_id == "debt_validation_v1":
            return {
                "template_id": "debt_validation_v1",
                "template_version": "1.0.0",
                "template_type": "debt_validation",
                "required_fields": get_required_fields(template_id)
            }
        
        db = get_mongo_db()
        row = await db.legal_templates.find_one({'template_id': template_id}, {'_id': 0})
        
        if not row:
            raise HTTPException(status_code=404, detail="Template not found")
        
        return row
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get template: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def get_required_fields(template_id: str) -> list:
    """Get required fields for template"""
    template_fields = {
        "debt_validation_v1": [
            "date",
            "recipient_name",
            "account_number",
            "consumer_name",
            "consumer_address"
        ]
    }
    
    return template_fields.get(template_id, [])


def sanitize_input(value: Any) -> str:
    """Sanitize input to prevent injection"""
    if value is None:
        return ""
    
    # Convert to string and escape HTML
    value_str = str(value)
    value_str = value_str.replace("<", "&lt;").replace(">", "&gt;")
    value_str = value_str.replace("'", "&#39;").replace('"', "&quot;")
    
    return value_str
