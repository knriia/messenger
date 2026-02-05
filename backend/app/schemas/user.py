from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr | None
    model_config = ConfigDict(from_attributes=True)
