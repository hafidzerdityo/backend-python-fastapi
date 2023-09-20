from fastapi import status, APIRouter, Depends
from fastapi.responses import JSONResponse
import api.schemas.auth as schemas
import services.auth as services_auth
import services.utils as utils
from log.log import logger
from datetime import datetime, timedelta
from repositories.postgres.config.database_config import database
import repositories.postgres.config.db_model as db_model


router = APIRouter()

active_tokens = {}
revoked_tokens = set()

user_service = services_auth.init_service_auth(database, db_model, logger)



@router.post("/token", tags=["Authentication"], response_model=schemas.ResponseLogin)
async def login_for_access_token(form_data: utils.OAuth2PasswordRequestForm = Depends()) -> schemas.ResponseLogin:
    try:
        print(active_tokens)
        if form_data.username in active_tokens:
            _, expiration_time = active_tokens[form_data.username]
            current_time = datetime.utcnow()
            if current_time < expiration_time:
                print(current_time)
                print(expiration_time)
                raise Exception("Token is still Valid")    
        get_token_data = await user_service.get_token(form_data.username, form_data.password)
        # Store the new token and its expiration time
        expiration_time = datetime.utcnow() + timedelta(seconds=utils.ACCESS_TOKEN_EXPIRE_MINUTES * 60)  # Adjust the expiration time as needed
        active_tokens[form_data.username] = [get_token_data, expiration_time]

        return schemas.ResponseLogin(
            resp_msg="Login Berhasil",
            resp_data=get_token_data
        )
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
            content={
                "resp_msg": str(e),
                "resp_data": None
            },
        )
    

@router.post("/logout", tags=["Authentication"])
async def logout(token: str = Depends(utils.oauth2_scheme)):
    try:
        _ = utils.jwt.decode(token, utils.SECRET_KEY, algorithms=["HS256"])
        # Add the token to the revoked tokens set
        revoked_tokens.add(token)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"resp_msg": "Logout successful", "resp_data": None},
        )
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"resp_msg": str(e), "resp_data": None},
        )
    
@router.get('/protected/admin', tags=["Authorization"], status_code=status.HTTP_200_OK, response_model=schemas.ResponseProtected)
async def admin_authorization(token: str = Depends(utils.oauth2_scheme)):
    try:
        payload = utils.jwt.decode(token, utils.SECRET_KEY, algorithms=["HS256"])
        if payload.get('role') != 'admin':
            raise Exception('Unauthorized')
        return schemas.ResponseProtected(
            resp_msg = "welcome admin",
            resp_data = None 
        )
    except Exception as e:
        logger.error(str(e)) 
        return JSONResponse(
            status_code= status.HTTP_401_UNAUTHORIZED,
            content={"resp_msg": str(e),
                     "resp_data":  None
                     },
        )
    
@router.get('/protected/view', tags=["Authorization"], status_code=status.HTTP_200_OK, response_model=schemas.ResponseProtected)
async def view_authorization(token: str = Depends(utils.oauth2_scheme)):
    try:
        payload = utils.jwt.decode(token, utils.SECRET_KEY, algorithms=["HS256"])
        if payload.get('role') != 'view':
            raise Exception('Unauthorized')
        return schemas.ResponseProtected(
            resp_msg = "welcome view only",
            resp_data = None 
        )
    except Exception as e:
        logger.error(str(e)) 
        return JSONResponse(
            status_code= status.HTTP_401_UNAUTHORIZED,
            content={"resp_msg": str(e),
                     "resp_data":  None
                     },
        )
    
@router.get('/current', tags=["Authorization"], status_code=status.HTTP_200_OK)
async def check_current_token(token: str = Depends(utils.oauth2_scheme)):
    try:
        _ = utils.jwt.decode(token, utils.SECRET_KEY, algorithms=["HS256"])
        return schemas.ResponseProtected(
            resp_msg = "Current Token is Valid",
            resp_data = None 
        )
    except Exception as e:
        logger.error(str(e)) 
        return JSONResponse(
            status_code= status.HTTP_401_UNAUTHORIZED,
            content={"resp_msg": str(e),
                     "resp_data":  None
                     },
        )
    
