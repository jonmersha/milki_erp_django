import uuid
from datetime import datetime

def generate_custom_id(prefix: str = "SYS", partition: str = None, length: int = 16) -> str:
    """
    Generate a common, readable unique ID for all models.
    Example: PRD-20251004-A1B2C3
    - prefix: short code for the entity (PRD, STK, MOV, etc.)
    - partition: optional code (e.g., date, company, factory)
    - length: total desired ID length
    """
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
