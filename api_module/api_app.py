from fastapi import FastAPI
from api_module.v1_router import v1_router as v1_api_router
from auth_module.user_store import get_db_session

app = FastAPI()

@app.on_event("startup")
def startup_event():
    # Ensure DB connection works on startup
    session = get_db_session()
    session.close()

app.include_router(v1_api_router)