from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TaskCreate(BaseModel):
    title: str
    description: str | None = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: str

    class Config:
        from_attributes = True    

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None        