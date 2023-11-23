from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
import json

import api.schemas.user_management as schemas
import services.user_management as services_user
import services.utils as utils
from repositories.postgres.config.database_config import database
import repositories.postgres.config.db_model as db_model
from utils.custom_exception import handle_exception, DataExist, InvalidPassword

from log import logger

router = APIRouter()

user_service = services_user.init_service_user(database,db_model,logger)

@router.post('/user', tags=["User Management"], status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseDaftar)
async def create_user(request_payload: schemas.RequestDaftar) -> schemas.ResponseDaftar:
    try:
        request_payload = json.loads(request_payload.json())
        _ = await user_service.post_user(request_payload)
        return schemas.ResponseDaftar(
            resp_msg = "Pendaftaran Berhasil",
            resp_data = None
        ) 
    except DataExist as e:
        return handle_exception(logger, status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))
    except InvalidPassword as e:
        return handle_exception(logger, status.HTTP_400_BAD_REQUEST, str(e))
    except Exception as e:
        return handle_exception(logger, status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))
    
@router.get('/user', tags=["User Management"], status_code=status.HTTP_200_OK, response_model=schemas.ResponseUser)
async def get_user(token: str = Depends(utils.oauth2_scheme)) -> schemas.ResponseUser:
    try:
        data_fetch_success = await user_service.get_user(token)
        data_fetch_success = schemas.ResponseUserItem(**data_fetch_success)
        return schemas.ResponseUser(
            resp_msg = "Get Data Berhasil",
            resp_data = data_fetch_success
        ) 
    except Exception as e:
        logger.error(str(e)) 
        return JSONResponse(
            status_code= status.HTTP_401_UNAUTHORIZED,
            content={"resp_msg": str(e),
                     "resp_data":  None
                     },
        )
    
@router.get('/users', tags=["User Management"], status_code=status.HTTP_200_OK, response_model=schemas.ResponseUsers)
async def get_user(token: str = Depends(utils.oauth2_scheme)) -> schemas.ResponseUsers:
    try:
        data_fetch_success = await user_service.select_users(token)
        data_fetch_success = [schemas.ResponseUserItem(**i) for i in data_fetch_success]
        return schemas.ResponseUsers(
            resp_msg = "Get Data Berhasil",
            resp_data = data_fetch_success
        )

    except Exception as e:
        logger.error(str(e)) 
        return JSONResponse(
            status_code= status.HTTP_401_UNAUTHORIZED,
            content={"resp_msg": str(e),
                     "resp_data":  None
                     },
        )
    

