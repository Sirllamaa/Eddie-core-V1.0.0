from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from api_module.models import UserInput, CoreResponse
from auth_module.auth_handler import create_access_token, get_current_user
from auth_module.auth_models import Token, User
from auth_module.user_store import authenticate_user
from core_logic.query_handler import query
from config import USER_AUTH_KEY, USER_AUTH_ALGORITHM
from jose import JWTError, jwt
from pydantic import BaseModel

# from core_logic.model_router import (
#     process_with_cloud,
#     process_with_local_llama,
#     process_with_quantized_llama,
#     needs_cloud_processing,
#     gpu_available
# )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

v1_router = APIRouter(prefix="/core/api/v1")

@v1_router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(f"Login attempt for user: {form_data.username}")  # Debugging line
    print(f"Password: {form_data.password}")  # Debugging line
    user = authenticate_user(form_data.username, form_data.password)
    print(f"User: {user}") # Debugging line
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    # verify user still exists in DB
    token = create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

@v1_router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, USER_AUTH_KEY, algorithms=[USER_AUTH_ALGORITHM])
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

class ProcessRequest(BaseModel):
    input_text: str
    system_prompt: str | None = None  # Optional override

class ProcessResponse(BaseModel):
    output_text: str

@v1_router.post("/process", response_model=ProcessResponse)
async def process_input(
    request: ProcessRequest,
    current_user=Depends(get_current_user),
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(token, USER_AUTH_KEY, algorithms=[USER_AUTH_ALGORITHM])
        result = query(request.input_text)
        return {"output_text": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLaMA API error: {e}")