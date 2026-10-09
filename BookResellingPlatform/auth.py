from fastapi import Header, HTTPException

API_KEY = "mysecretapikey"

def verify_api_key(a_api_key: str = Header()):
    if a_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid Header")
    return a_api_key