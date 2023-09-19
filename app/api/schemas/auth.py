from typing import Optional, List,Dict, Union
from pydantic import BaseModel, StrictFloat, StrictStr, StrictInt, StrictBool, validator,constr
from datetime import date


class RequestLogin(BaseModel):
    username: constr(max_length=255)
    password: constr(max_length=255)

class ResponseLoginItem(BaseModel):
    access_token : StrictStr 
    token_type : StrictStr 

class ResponseLogin(BaseModel):
    resp_msg: StrictStr
    resp_data: ResponseLoginItem

class ResponseProtected(BaseModel):
    resp_msg: StrictStr 
    resp_data: Optional[None]
