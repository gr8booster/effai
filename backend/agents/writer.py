"""WriterAgent - Deterministic template filler and PDF generator"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import logging
import hashlib
import json
from jinja2 import Template
from typing import Dict, Any
import os
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime, timedelta, timezone
import re

from schemas import (
    WriterGenerateInput,
    WriterGenerateOutput,
    ToneType
)
from database import get_mongo_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/writer", tags=["writer"])

# Template templates (for immediate use)
DEBT_VALIDATION_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>Debt Validation Request</title>
</head>
<body style="font-family: Arial, sans-serif; margin: 40px; line-height: 1.6;">
    <div style="text-align: right; margin-bottom: 40px;">
        <p>{{ consumer_name }}<br>{{ consumer_address }}<br>{{ date }}</p>
    </div>
    <p>{{ recipient_name }}<br>Attn: Validation Department</p>
    <p>Re: Account Number {{ account_number }}</p>
    <div style="margin: 20px 0;">
        {% if tone == 'formal' %}
        <p>Dear Sir or Madam,</p>
        <p>I am writing to formally request validation of the alleged debt pursuant to 15 U.S.C. § 1692g.</p>
        {% else %}
        <p>Hello,</p>
        <p>I'm writing to ask for validation of this debt under the Fair Debt Collection Practices Act.</p>
        {% endif %}
    </div>
    <div style="margin-top: 60px;">
        <p>Sincerely,<br><br>{{ consumer_name }}</p>
    </div>
    <div style="margin-top: 40px; font-size: 8px; color: #ccc;">
        <!-- Provenance: {{ provenance_json }} -->
    </div>
</body>
</html>
"""

CEASE_DESIST_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>Cease and Desist</title>
</head>
<body style="font-family: Arial, sans-serif; margin: 40px; line-height: 1.6;">
    <div style="text-align: right; margin-bottom: 40px;">
        <p>{{ consumer_name }}<br>{{ consumer_address }}<br>{{ date }}</p>
    </div>
    <p>{{ recipient_name }}<br>{{ recipient_address }}</p>
    <p><strong>RE: Cease and Desist - Account {{ account_number }}</strong></p>
    <div style="margin: 20px 0;">
        <p>Dear Sir or Madam:</p>
        <p>This letter is to formally notify you that I am invoking my rights under 15 U.S.C. § 1692c(c) 
        of the Fair Debt Collection Practices Act.</p>
        <p>You are hereby directed to <strong>CEASE AND DESIST</strong> all communication with me regarding 
        the alleged debt referenced above.</p>
        <p>This includes, but is not limited to:</p>
        <ul>
            <li>Telephone calls to my home, cell, or workplace</li>
            <li>Letters or written correspondence</li>
            <li>Contact through third parties</li>
            <li>Any other form of communication</li>
        </ul>
        <p>You may only contact me to:</p>
        <ul>
            <li>Confirm receipt of this letter</li>
            <li>Notify me that collection efforts are being terminated</li>
            <li>Notify me of specific legal action you intend to take</li>
        </ul>
        <p>Please consider this my formal written notice under the FDCPA.</p>
    </div>
    <div style="margin-top: 60px;">
        <p>Sincerely,<br><br>{{ consumer_name }}</p>
    </div>
    <div style="margin-top: 40px; font-size: 8px; color: #ccc;">
        <!-- Provenance: {{ provenance_json }} -->
    </div>
</body>
</html>
"""

CREDIT_DISPUTE_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>Credit Report Dispute</title>
</head>
<body style="font-family: Arial, sans-serif; margin: 40px; line-height: 1.6;">
    <div style="text-align: right; margin-bottom: 40px;">
        <p>{{ consumer_name }}<br>{{ consumer_address }}<br>{{ date }}</p>
    </div>
    <p>{{ bureau_name }}<br>Dispute Department</p>
    <p><strong>RE: Formal Dispute of Inaccurate Information</strong></p>
    <div style="margin: 20px 0;">
        <p>To Whom It May Concern:</p>
        <p>I am writing to dispute the following inaccurate information on my credit report, 
        pursuant to my rights under 15 U.S.C. § 1681i (FCRA Section 611).</p>
        <p><strong>Item Being Disputed:</strong> {{ disputed_item }}</p>
        <p><strong>Account Number:</strong> {{ account_number }}</p>
        <p><strong>Reason for Dispute:</strong> {{ dispute_reason }}</p>
        <p>Under the Fair Credit Reporting Act, you are required to investigate this dispute within 30 days 
        and must correct or delete any information found to be inaccurate, incomplete, or unverifiable.</p>
        <p>I request that you:</p>
        <ol>
            <li>Investigate this disputed item thoroughly</li>
            <li>Contact the furnisher of this information</li>
            <li>Remove this item if it cannot be verified as 100% accurate</li>
            <li>Send me written confirmation of the results</li>
        </ol>
        <p>Enclosed are supporting documents that verify my position.</p>
    </div>
    <div style="margin-top: 60px;">
        <p>Sincerely,<br><br>{{ consumer_name }}</p>
    </div>
    <div style="margin-top: 40px; font-size: 8px; color: #ccc;">
        <!-- Provenance: {{ provenance_json }} -->
    </div>
</body>
</html>
"""

SETTLEMENT_OFFER_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>Debt Settlement Offer</title>
</head>
<body style="font-family: Arial, sans-serif; margin: 40px; line-height: 1.6;">
    <div style="text-align: right; margin-bottom: 40px;">
        <p>{{ consumer_name }}<br>{{ consumer_address }}<br>{{ date }}</p>
    </div>
    <p>{{ recipient_name }}<br>Settlement Department</p>
    <p><strong>RE: Settlement Offer - Account {{ account_number }}</strong></p>
    <div style="margin: 20px 0;">
        <p>Dear Sir or Madam:</p>
        <p>I am writing regarding the above-referenced account. Due to financial hardship, I am unable to pay 
        the full amount currently claimed.</p>
        <p>However, I am willing to resolve this matter and hereby offer to settle this account for 
        <strong>${{ settlement_amount }}</strong>, which represents {{ settlement_percentage }}% of the alleged balance.</p>
        <p><strong>Settlement Terms:</strong></p>
        <ul>
            <li>Payment amount: ${{ settlement_amount }}</li>
            <li>Payment method: {{ payment_method }}</li>
            <li>In exchange, you agree to mark this account as "Paid in Full" or "Settled"</li>
            <li>You agree to request deletion of all negative tradelines related to this account from all credit bureaus</li>
            <li>You agree this settles the account completely with no further amounts owed</li>
        </ul>
        <p>This offer is contingent upon receiving written confirmation of these terms <strong>before</strong> I submit payment.</p>
        <p>If you accept this offer, please send written confirmation on company letterhead within 15 days.</p>
        <p>This is an offer of settlement and should not be construed as acknowledgment of the debt or waiver of any rights.</p>
    </div>
    <div style="margin-top: 60px;">
        <p>Sincerely,<br><br>{{ consumer_name }}</p>
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
        
        # Generate PDF using ReportLab
        pdf_path = None
        try:
            # Create temp file for PDF
            temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf', dir='/tmp')
            pdf_path = temp_pdf.name
            temp_pdf.close()
            
            # Generate PDF from template data
            doc = SimpleDocTemplate(pdf_path, pagesize=letter)
            story = []
            styles = getSampleStyleSheet()
            
            # Add content
            story.append(Paragraph(f"{sanitized_fields['consumer_name']}", styles['Normal']))
            story.append(Paragraph(f"{sanitized_fields['consumer_address']}", styles['Normal']))
            story.append(Paragraph(f"{sanitized_fields['date']}", styles['Normal']))
            story.append(Spacer(1, 0.5*inch))
            
            story.append(Paragraph(f"{sanitized_fields['recipient_name']}", styles['Normal']))
            story.append(Paragraph(f"Re: Account Number {sanitized_fields['account_number']}", styles['Normal']))
            story.append(Spacer(1, 0.3*inch))
            
            # Body
            if sanitized_fields['tone'] == 'formal':
                body_text = f"""Dear Sir or Madam,<br/><br/>
                I am writing to formally request validation of the alleged debt you claim I owe, 
                pursuant to my rights under the Fair Debt Collection Practices Act (FDCPA), 15 U.S.C. § 1692g.<br/><br/>
                Please provide: the original creditor's name, the original amount, proof of licensing, 
                verification that statute of limitations has not expired, and a complete account statement.<br/><br/>
                Until you provide proper validation, I expect all collection activities to cease as required by law.<br/><br/>
                Sincerely,<br/>{sanitized_fields['consumer_name']}"""
            else:
                body_text = f"""Hello,<br/><br/>
                I'm writing to ask you to validate the debt you say I owe. Under the Fair Debt Collection Practices Act, 
                I have the right to ask for proof.<br/><br/>
                Please send me: who the original creditor was, the original amount, proof you can collect this debt, 
                confirmation this debt isn't too old, and a full statement.<br/><br/>
                Please don't contact me until you send this information.<br/><br/>
                Sincerely,<br/>{sanitized_fields['consumer_name']}"""
            
            story.append(Paragraph(body_text, styles['Normal']))
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"PDF generated at {pdf_path}")
            
        except Exception as pdf_error:
            logger.warning(f"PDF generation failed: {pdf_error}. Returning HTML only.")
            pdf_path = None
        
        result = WriterGenerateOutput(
            html_preview=rendered_html,
            pdf_url=f"/api/writer/download/{content_hash}" if pdf_path else None,
            hash=content_hash,
            provenance_ref=f"writer_{input_data.trace_id}"
        )
        
        # Store PDF path in MongoDB for download
        if pdf_path:
            db = get_mongo_db()
            await db.generated_documents.insert_one({
                "document_id": content_hash,
                "pdf_path": pdf_path,
                "template_id": input_data.template_id,
                "user_id": input_data.user_id,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "expires_at": (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
            })
        
        logger.info(f"Document generated: template={input_data.template_id}, hash={content_hash[:8]}..., pdf={pdf_path is not None}")
        
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



@router.get("/download/{document_id}")
async def download_pdf(document_id: str):
    """Download generated PDF document"""
    try:
        db = get_mongo_db()
        
        # Get document record
        doc = await db.generated_documents.find_one({"document_id": document_id})
        
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found or expired")
        
        # Check if file exists
        pdf_path = doc['pdf_path']
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=404, detail="PDF file not found")
        
        # Return PDF file
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"debt_validation_{document_id[:8]}.pdf"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"PDF download failed: {e}")
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
