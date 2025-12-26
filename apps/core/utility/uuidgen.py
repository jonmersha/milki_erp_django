import uuid
from datetime import datetime
from django.utils import timezone

def generate_custom_id(prefix: str = "SYS", partition: str = None, length: int = 16) -> str:
   
    # Take 6 chars from UUID for uniqueness
    random_part = uuid.uuid4().hex[:6].upper()

    # Build base format
    if partition:
        base = f"{prefix}-{partition}-{random_part}"
    else:
        base = f"{prefix}-{random_part}"

    # Normalize to fixed length
    if len(base) > length:
        base = base[:length]
    elif len(base) < length:
        base = base.ljust(length, "X")

    return base

def cid(prefix: str = "SYS", length: int = 16) -> str:
    partition = timezone.now().strftime("%Y%m%d")
    random_part = uuid.uuid4().hex[:6].upper()
    
    if partition:
        base = f"{prefix}-{partition}-{random_part}"
    else:
        base = f"{prefix}-{random_part}"
    # Normalize to fixed length
    if len(base) > length:
        base = base[:length]
    elif len(base) < length:
        base = base.ljust(length, "X")

    return base
