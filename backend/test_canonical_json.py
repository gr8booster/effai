"""Unit tests for canonical JSON utility"""
import pytest
from canonical_json import (
    canonical_json,
    payload_hash,
    hmac_sign,
    verify_payload_hash,
    create_audit_record
)


def test_canonical_json_deterministic():
    """Same data should always produce same JSON string"""
    data1 = {"name": "John", "age": 30, "city": "NYC"}
    data2 = {"city": "NYC", "name": "John", "age": 30}  # Different order
    
    json1 = canonical_json(data1)
    json2 = canonical_json(data2)
    
    assert json1 == json2
    assert json1 == '{"age":30,"city":"NYC","name":"John"}'


def test_payload_hash_deterministic():
    """Same data should always produce same hash"""
    data1 = {"balance": 1000.50, "apr": 0.24}
    data2 = {"apr": 0.24, "balance": 1000.50}
    
    hash1 = payload_hash(data1)
    hash2 = payload_hash(data2)
    
    assert hash1 == hash2
    assert len(hash1) == 64  # SHA256 produces 64 hex characters


def test_payload_hash_different_data():
    """Different data should produce different hashes"""
    data1 = {"amount": 100}
    data2 = {"amount": 101}
    
    hash1 = payload_hash(data1)
    hash2 = payload_hash(data2)
    
    assert hash1 != hash2


def test_verify_payload_hash():
    """Hash verification should work correctly"""
    data = {"test": "value", "number": 42}
    hash_val = payload_hash(data)
    
    assert verify_payload_hash(data, hash_val) is True
    assert verify_payload_hash(data, "wrong_hash") is False


def test_hmac_sign():
    """HMAC signing should be deterministic"""
    key = b"secret_key_123"
    message = "test message"
    
    sig1 = hmac_sign(key, message)
    sig2 = hmac_sign(key, message)
    
    assert sig1 == sig2
    assert len(sig1) == 64  # HMAC-SHA256 produces 64 hex characters


def test_create_audit_record():
    """Audit record creation should be complete"""
    record = create_audit_record(
        event_id="evt_123",
        trace_id="tr_abc",
        actor="TestAgent",
        event_type="test",
        payload={"data": "value"},
        prev_hash="prev_hash_456",
        hmac_key=b"test_key"
    )
    
    assert record["event_id"] == "evt_123"
    assert record["trace_id"] == "tr_abc"
    assert record["actor"] == "TestAgent"
    assert record["event_type"] == "test"
    assert "payload_hash" in record
    assert record["prev_hash"] == "prev_hash_456"
    assert "timestamp_utc" in record
    assert "hmac" in record
    assert len(record["hmac"]) == 64


def test_nested_object_canonical():
    """Nested objects should be canonicalized correctly"""
    data1 = {
        "user": {"name": "John", "age": 30},
        "balance": 1000
    }
    data2 = {
        "balance": 1000,
        "user": {"age": 30, "name": "John"}
    }
    
    assert canonical_json(data1) == canonical_json(data2)
    assert payload_hash(data1) == payload_hash(data2)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
