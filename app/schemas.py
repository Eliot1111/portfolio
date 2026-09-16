from pydantic import BaseModel, ConfigDict


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    role: str


class ItemCreate(BaseModel):
    name: str
    description: str | None = None


class ItemResponse(ItemCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
