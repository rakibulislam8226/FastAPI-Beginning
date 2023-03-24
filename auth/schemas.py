from pydantic import BaseModel, Field, EmailStr
from fastapi_jwt_auth import AuthJWT


class UserBaseSchema(BaseModel):
    email: EmailStr
    full_name: str


class CreateUserSchema(UserBaseSchema):
    hashed_password: str = Field(alias="password")


class UserSchema(UserBaseSchema):
    id: int
    is_active: bool = Field(default=False)

    class Config:
        orm_mode = True


class Settings(BaseModel):
    authjwt_secret_key:str='e8ae5c5d5cd7f0f1bec2303ad04a7c80f09f759d480a7a5faff5a6bbaa4078d0'


@AuthJWT.load_config
def get_config():
    return Settings()

class User(BaseModel):
    id: int
    username:str
    email:str
    hashed_password:str

    class Config:
        schema_extra={
            "example":{
                "username":"name",
                "email":"mail@gmail.com",
                "hashed_password":""
            }
        }
        orm_mode = True


class UserLogin(BaseModel):
    username:str
    hashed_password:str

    class Config:
        schema_extra={
            "example":{
                "username":"name",
                "hashed_password":""
            }
        }