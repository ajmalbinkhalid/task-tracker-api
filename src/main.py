from fastapi import FastAPI
from src.database import Base , engine
from src.routes import auth_routes
from src.routes import user_routes
from src.routes import task_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(user_routes.router)

app.include_router(auth_routes.router)

app.include_router(task_routes.router)

@app.get("/")
def root():
    return {"message": "Task Tracker API running"}