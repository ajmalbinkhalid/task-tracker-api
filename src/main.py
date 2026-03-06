from fastapi import FastAPI
from src.database import Base , engine
from src.routes import auth_routes
from src.routes import user_routes

app = FastAPI()

app.include_router(user_routes.router)

Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router)

@app.get("/")
def root():
    return {"message": "Task Tracker API running"}