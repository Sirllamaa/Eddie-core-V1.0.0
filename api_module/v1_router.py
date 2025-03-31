from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from api_module.models import UserInput, CoreResponse
from auth_module.auth_handler import create_access_token, get_current_user
from auth_module.auth_models import Token, User
from auth_module.user_store import authenticate_user
from config import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt
from core_logic.model_router import (
    process_with_cloud,
    process_with_local_llama,
    process_with_quantized_llama,
    needs_cloud_processing,
    gpu_available
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

v1_router = APIRouter(prefix="/api/v1")

@v1_router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    # OPTIONAL: verify user still exists in DB
    token = create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

@v1_router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "username": current_user.username,
            "role": current_user.role,
            "token_payload": {
                "sub": payload.get("sub"),
                "role": payload.get("role"),
                "exp": payload.get("exp"),
            }
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@v1_router.post("/process", response_model=CoreResponse)
def process_input(user_input: UserInput, current_user: User = Depends(get_current_user)):
    is_admin = current_user.role == "admin"

    # Admins can force cloud model
    if is_admin and user_input.use_cloud:
        response_text, confidence = process_with_cloud(user_input.input_text)
        model_used = "cloud_gpt"
    # Try GPU-based LLaMA if available
    elif gpu_available():
        response_text, confidence = process_with_local_llama(user_input.input_text)
        model_used = "local_llama_gpu"
    # Fallback to quantized CPU model
    else:
        response_text, confidence = process_with_quantized_llama(user_input.input_text)
        model_used = "local_llama_quantized"

    return CoreResponse(
        response_text=response_text,
        model_used=model_used,
        confidence=confidence if is_admin else None
    )

