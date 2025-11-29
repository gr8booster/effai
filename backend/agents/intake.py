"""IntakeAgent - OCR, parsing, and document redaction with Tesseract"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
import logging
import uuid
from typing import Optional
import re
import pytesseract
from PIL import Image
import cv2
import numpy as np
import io

from schemas import (
    IntakeUploadOutput,
    ExtractedField
)
from database import get_mongo_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/intake", tags=["intake"])


@router.post("/upload", response_model=IntakeUploadOutput)
async def upload_document(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    trace_id: str = Form(...)
):
    """
    Upload and process document with full OCR using Tesseract
    """
    try:
        doc_id = str(uuid.uuid4())
        
        # Read file content
        content = await file.read()
        
        # Perform OCR
        text = perform_ocr(content, file.filename)
        
        # Extract fields using regex patterns
        extracted_fields = extract_fields_from_text(text)
        
        # Redact sensitive information
        redacted_text = redact_sensitive_info(text)
        
        # Calculate confidence scores
        confidence_scores = {
            field: extracted_fields[field].confidence
            for field in extracted_fields
        }
        
        # Determine if manual review needed
        needs_manual_review = any(
            conf < 0.85 for conf in confidence_scores.values()
        ) if confidence_scores else True
        
        # Store in MongoDB
        db = get_mongo_db()
        doc_record = {
            "doc_id": doc_id,
            "user_id": user_id,
            "trace_id": trace_id,
            "filename": file.filename,
            "ocr_text": text,
            "extracted_fields": {k: v.model_dump() for k, v in extracted_fields.items()},
            "redacted_text": redacted_text,
            "needs_manual_review": needs_manual_review,
            "uploaded_at": datetime.now(timezone.utc).isoformat()
        }
        
        await db.intake_documents.insert_one(doc_record)
        
        result = IntakeUploadOutput(
            doc_id=doc_id,
            ocr_text=text,
            extracted_fields=extracted_fields,
            redacted_preview=redacted_text,
            confidence_scores=confidence_scores,
            needs_manual_review=needs_manual_review,
            provenance_ref=f"intake_{trace_id}"
        )
        
        logger.info(f"Document processed: doc_id={doc_id}, review_needed={needs_manual_review}, text_length={len(text)}")
        
        return result
        
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/doc/{doc_id}/result")
async def get_document_result(doc_id: str):
    """Get document processing result"""
    try:
        db = get_mongo_db()
        doc = await db.intake_documents.find_one({"doc_id": doc_id}, {"_id": 0})
        
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return doc
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def extract_fields_from_text(text: str) -> dict:
    """
    Extract structured fields from text using regex patterns
    
    For POC: Basic pattern matching
    Phase 2: ML-based extraction
    """
    fields = {}
    
    # Extract creditor name (simple pattern)
    creditor_pattern = r"(?:from|creditor|collector):\s*([A-Za-z0-9\s&,.-]+)"
    creditor_match = re.search(creditor_pattern, text, re.IGNORECASE)
    if creditor_match:
        fields["creditor"] = ExtractedField(
            value=creditor_match.group(1).strip(),
            confidence=0.90
        )
    
    # Extract account number
    account_pattern = r"(?:account|acct|#)\s*(?:number|no\.?)?:?\s*([0-9X*\-]{4,})"
    account_match = re.search(account_pattern, text, re.IGNORECASE)
    if account_match:
        account_num = account_match.group(1)
        # Mask all but last 4
        if len(account_num) > 4:
            masked = "X" * (len(account_num) - 4) + account_num[-4:]
        else:
            masked = account_num
        
        fields["account_number_last4"] = ExtractedField(
            value=masked,
            confidence=0.88
        )
    
    # Extract amount
    amount_pattern = r"\$?\s*([0-9,]+\.\d{2})"
    amount_match = re.search(amount_pattern, text)
    if amount_match:
        amount_str = amount_match.group(1).replace(",", "")
        try:
            amount = float(amount_str)
            fields["amount"] = ExtractedField(
                value={"value": amount, "currency": "USD"},
                confidence=0.92
            )
        except:
            pass
    
    # Extract date
    date_pattern = r"(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})"
    date_match = re.search(date_pattern, text)
    if date_match:
        fields["date"] = ExtractedField(
            value=date_match.group(1),
            confidence=0.85
        )
    
    return fields


def redact_sensitive_info(text: str) -> str:
    """
    Redact PII and sensitive information
    """
    # Redact SSN
    text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "XXX-XX-XXXX", text)
    text = re.sub(r"\b\d{9}\b", "XXXXXXXXX", text)
    
    # Redact account numbers (keep last 4)
    text = re.sub(r"\b\d{12,19}\b", lambda m: "X" * (len(m.group()) - 4) + m.group()[-4:], text)
    
    # Redact phone numbers
    text = re.sub(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "XXX-XXX-XXXX", text)
    
    return text
