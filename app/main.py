from fastapi import FastAPI
from app.routes.tasks import router as tasks_router

app = FastAPI(
    title="TaskFlow API",
    version="1.0.0"
)

app.include_router(tasks_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
