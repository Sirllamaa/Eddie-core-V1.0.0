from pydantic import BaseModel

class UserInput(BaseModel):
    input_text: str

class CoreResponse(BaseModel):
    response_text: str
    model_used: str
    confidence: float | None = None
