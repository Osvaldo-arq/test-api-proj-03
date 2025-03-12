from fastapi import FastAPI
from app.api import routes

app = FastAPI(title="Invoice Processing API")

app.include_router(routes.router)

@app.get("/")
def health_check():
    return {"status": "API is running"}
