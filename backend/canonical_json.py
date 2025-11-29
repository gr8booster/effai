"""Canonical JSON utility for deterministic hashing across all agents

This ensures that the same data structure always produces the same hash,
regardless of which agent creates it or in what order keys are serialized.

Usage:
    from canonical_json import canonical_json, payload_hash, hmac_sign
    
    data = {"name": "John", "age": 30}
    json_str = canonical_json(data)  # '{"age":30,"name":"John"}'
    hash_val = payload_hash(data)    # 'abc123...'
"""
import json
import hashlib
import hmac as hmac_lib
from typing import Any, Dict


def canonical_json(obj: Any) -> str:
    """
    Convert object to canonical JSON string
    
    Rules:
    - Keys sorted alphabetically
    - No whitespace (compact separators)
    - UTF-8 encoding
    - Consistent number formatting
    - No trailing newlines
    
    Args:
        obj: Any JSON-serializable object
    
    Returns:
        Canonical JSON string
    """
    return json.dumps(
        obj,
        separators=(',', ':'),
        sort_keys=True,
        ensure_ascii=False
    )


def payload_hash(obj: Any) -> str:
    """
    Compute deterministic SHA256 hash of object
    
    Args:
        obj: Any JSON-serializable object
    
    Returns:
        Hex string of SHA256 hash
    """
    canonical_json_str = canonical_json(obj)
    canonical_bytes = canonical_json_str.encode('utf-8')
    return hashlib.sha256(canonical_bytes).hexdigest()


def hmac_sign(key: bytes, message: str) -> str:
    """
    Generate HMAC signature for message
    
    Args:
        key: Secret key (bytes)
        message: Message to sign (string)
    
    Returns:
        Hex string of HMAC-SHA256 signature
    """
    message_bytes = message.encode('utf-8') if isinstance(message, str) else message
    return hmac_lib.new(key, message_bytes, hashlib.sha256).hexdigest()


def verify_payload_hash(obj: Any, expected_hash: str) -> bool:
    """
    Verify that object matches expected hash
    
    Args:
        obj: Object to verify
        expected_hash: Expected hash value
    
    Returns:
        True if hash matches, False otherwise
    """
    actual_hash = payload_hash(obj)
    return actual_hash == expected_hash


def create_audit_record(
    event_id: str,
    trace_id: str,
    actor: str,
    event_type: str,
    payload: Dict[str, Any],
    prev_hash: str,
    hmac_key: bytes
) -> Dict[str, Any]:
    """
    Create standardized audit record with chained hashing
    
    Args:
        event_id: Unique event identifier
        trace_id: Request trace ID
        actor: Agent or user performing action
        event_type: Type of event
        payload: Event payload data
        prev_hash: Hash of previous event in chain
        hmac_key: HMAC signing key
    
    Returns:
        Complete audit record dict
    """
    from datetime import datetime, timezone
    
    payload_hash_val = payload_hash(payload)
    timestamp_utc = datetime.now(timezone.utc).isoformat()
    
    # Create record without HMAC first
    record = {
        "event_id": event_id,
        "trace_id": trace_id,
        "actor": actor,
        "event_type": event_type,
        "payload_hash": payload_hash_val,
        "prev_hash": prev_hash,
        "timestamp_utc": timestamp_utc
    }
    
    # Sign the record
    record_json = canonical_json(record)
    record["hmac"] = hmac_sign(hmac_key, record_json)
    
    return record
