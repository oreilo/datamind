"""Explicit PII masking helpers for exported records."""
import re
EMAIL=re.compile(r'([A-Za-z0-9._%+-]+)@([A-Za-z0-9.-]+\.[A-Za-z]{2,})')
PHONE=re.compile(r'(?<!\d)(?:\+?\d[\d ()-]{8,}\d)(?!\d)')
def mask_text(value):
    if not isinstance(value,str):return value
    return PHONE.sub('[PHONE]',EMAIL.sub('[EMAIL]',value))
def mask_records(records:list[dict],columns:list[str]|None=None):
    return [{key:('[REDACTED]' if columns and key in columns else mask_text(value)) for key,value in row.items()} for row in records]
