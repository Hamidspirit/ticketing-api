from ..utils.errors import InvalidInputError

ALLOWED_PRIORITIES = {"low", "medium", "high"}
ALLOWD_STATUSES = {"open", "in_progress", "closed"}

def require_json_keys(data: dict, keys: list[str]):
    missing = [k for k in keys if k not in data]
    if missing:
        raise InvalidInputError(f"Missing required fields: {', '.join(missing)}")

def validate_priority(priority: str):
    if priority not in ALLOWED_PRIORITIES:
        raise InvalidInputError(f"Invalid Priority, Allowed: {', '.join(ALLOWED_PRIORITIES)}")

def validate_status(status: str):
    if status not in ALLOWD_STATUSES:
        raise InvalidInputError(f"Invalid Status. Allowed: {', '.join(ALLOWD_STATUSES)}")

def validate_username(username: str):
    if not username or len(username) < 3:
        raise InvalidInputError("Username Must be at least 3 charachters long")

def validate_password(password: str):
    if not password or len(password) < 6:
        raise InvalidInputError("Password Must be at least 6 chatachters long")