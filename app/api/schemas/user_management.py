from typing import Optional, List,Dict, Union
from pydantic import BaseModel, StrictFloat, StrictStr, StrictInt, StrictBool, validator,constr
from datetime import date


class RequestDaftar(BaseModel):
    username: constr(min_length = 5, max_length = 20)
    password: constr(max_length=255)
    nama: constr(max_length=255)
    role: constr(max_length=255)
    email: constr(max_length=255)
    @validator("username")
    def username_not_empty(cls, value):
        if not value.strip():
            raise ValueError("Username cannot be an empty string")
        return value
    
    @validator("nama")
    def nama_not_empty(cls, value):
        if not value.strip():
            raise ValueError("Nama cannot be an empty string")
        return value
    
class ResponseDaftarItem(BaseModel):
    success: StrictBool


class ResponseDaftar(BaseModel):
    resp_msg: StrictStr
    resp_data: None

# class RequestUser(BaseModel):
#     username: str

class ResponseUserItem(BaseModel):
    username: str
    nama: str
    role: str
    email: str
    created_at: str
    updated_at: Optional[str]
    is_deleted: bool

class ResponseUser(BaseModel):
    resp_msg: StrictStr
    resp_data: ResponseUserItem

class ResponseUsers(BaseModel):
    resp_msg: StrictStr
    resp_data: List[ResponseUserItem]


