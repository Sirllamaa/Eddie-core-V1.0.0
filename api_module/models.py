from pydantic import BaseModel

class UserInput(BaseModel):
    user_id: str
    input_text: str
    use_cloud: bool = False  # Admins can request cloud use explicitly

class CoreResponse(BaseModel):
    response_text: str
    model_used: str
    confidence: float | None = None  # Only visible to admins
