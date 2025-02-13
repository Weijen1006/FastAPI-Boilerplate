import jwt
import time
from typing import Optional, Dict
from configs import settings
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from utils.logger import LoggerUtils
from models.user import UserData

JWT_SECRET = settings.JWT_SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM
JWT_EXPIRED_IN_SECOND = settings.JWT_EXPIRED_IN_SECOND

bearer_auth = HTTPBearer()
logger = LoggerUtils.get_logger(__name__)


def encode_jwt(payload: Dict[str, str]) -> str:
    """
    Encodes a JWT with the provided payload.
    
    :param payload: The payload data that will be encoded in the JWT.
    :return: The encoded JWT token as a string.
    """
    expiration_time = time.time() + JWT_EXPIRED_IN_SECOND
    payload.update({"exp": expiration_time})

    # Encode the payload using the secret key and specified algorithm
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def decode_jwt(token: str) -> Optional[Dict[str, str]]:
    """
    Decodes a JWT and returns the payload if the token is valid.
    
    :param token: The JWT token to be decoded.
    :return: The decoded payload if valid, or None if the token is invalid/expired.
    """
    try:
        # Decode the token using the secret key and specified algorithm
        decoded_payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        logger.info(f"Decoded payload: {decoded_payload}")
        logger.info(f"Decoded timestamp: {decoded_payload["exp"]}")
        logger.info(f"Timestamp Now: {time.time()} ")
        return decoded_payload if decoded_payload["exp"] >= time.time() else None
    except:
        return None

def verify_jwt(token: str) -> bool:
    """
    Verifies the validity of the JWT token.
    
    :param token: The JWT token to verify.
    :return: True if the token is valid, False otherwise.
    """
    decoded_payload = decode_jwt(token)
    return decoded_payload is not None

def get_user_role(payload: Dict[str, str]) -> str:
    """
    Extracts the user's role from the JWT payload.
    
    :param payload: The decoded JWT payload.
    :return: The role of the user (e.g., "user", "admin", "super admin").
    """
    return payload.get("role", "user")  # Default to "user" if no role is found


def has_permission(user_role: str, required_role: str) -> bool:
    """
    Checks if the user's role is equal to or higher than the required role.
    
    :param user_role: The role of the user (e.g., "user", "admin", "super admin").
    :param required_role: The required role to check against.
    :return: True if the user has the required role, False otherwise.
    """
    user_role_index = settings.ROLE_HIERARCHY.index(user_role)
    required_role_index = settings.ROLE_HIERARCHY.index(required_role)
    
    # User has permission if their role is equal or higher than the required role
    return user_role_index >= required_role_index

def get_current_user(token: str = Depends(bearer_auth)) -> UserData:
    """
    Decodes the JWT token to retrieve the current user information.

    :param token: The JWT token from the request's Authorization header (Bearer token).
    :return: The current user's information (e.g., user_id, username).
    """
    try:
        logger.info(f"JWT Bearer Token: {token}")
        # Decode the JWT token
        payload = decode_jwt(token.credentials)
        # Extract user information from the payload (you can customize this)
        # Try not to rely solely on jwt token to verify user role, recommend to include secondary checking (read from db or redis cache)
        user = UserData(user_id=payload.get("user_id"), user_name=payload.get("user_name"), role=payload.get("role"))

        return user
    except Exception as e:
        logger.error(f"{e}")
        raise HTTPException(status_code=404, detail=f"User not found")