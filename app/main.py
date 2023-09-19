from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from repositories.postgres.config.database_config import metadata, engine, database
import api.routers.user_management
import api.routers.auth

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, constr
from log.log import logger

from dotenv import load_dotenv
import os
load_dotenv('service.env')

HOST = os.environ.get('SERVICE_HOST')
PORT = os.environ.get('SERVICE_PORT')
WORKERS = os.environ.get('SERVICE_WORKERS')



app = FastAPI(title="Template API",
    description="author: Muhammad Hafidz Erdityo",
    version="0.0.1",
    terms_of_service=None,
    contact=None,
    license_info=None)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

metadata.create_all(engine)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = exc.errors()
    error_list = []
    for error in details:
        error_list.append(
            {
                "loc": error["loc"],
                "message": error["msg"],
                "type": error["type"],
            }
        )
    modified_response = {
        "resp_data": None,
        "resp_msg": error_list
    }
    logger.error(error_list) 
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(modified_response),
    )

app.include_router(api.routers.user_management.router,prefix="/api/v1/user_management")
app.include_router(api.routers.auth.router,prefix="/api/v1/auth")

if __name__ == '__main__':
    uvicorn.run('main:app', host=HOST, port=int(PORT), workers=int(WORKERS), reload=True)
