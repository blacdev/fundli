from fastapi import APIRouter, HTTPException, Request, Header
from fastapi.responses import JSONResponse
from pocketguardapp.services.account import get_account, decode_token

app = APIRouter()


def authenticate(authorization: str = Header()):
    token = get_authorization_token(authorization)
    if not token:
        return HTTPException(status_code=401, detail="token not found")

    # get email from token
    email = decode_token(token).get("email")
    # get account for email
    account, error = get_account(email)
    if error:
        raise HTTPException(status_code=401, detail=error.msg)

    return account


def get_authorization_token(authorization: str):
    """
    get_authorization_token returns the authorization token from the request
    expects format: Authorization: Bearer <token>
    """
    parts = authorization.split(" ")
    if len(parts) != 2:
        return None
    return parts[1]
