from datetime import timedelta

SECRET_KEY = "fastapi-insecure-@wce-&&ynyy+twy496^3x%n7i@@7j79a8zxz+xe_kpayf6lqkj"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def get_token_expiry() -> timedelta:
    return timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
