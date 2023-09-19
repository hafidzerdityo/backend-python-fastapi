import repositories.postgres.crud.auth as crud
import services.utils as utils
from datetime import datetime, timedelta
import api.schemas.auth as schemas

class AuthService:
    def __init__(self, database, logger):
        self.database = database
        self.logger = logger

    async def get_token(self, username, password):
        async with self.database.transaction():
            user = await crud.get_hashed_pass_by_username(username)
            if not user or not utils.verify_password(password, user['hashed_password']):
                raise Exception("Incorrect username or password")
            access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = utils.create_access_token(
                data={"username": user['username'], "role":user['role']}, expires_delta=access_token_expires
            )
            service_response = {"access_token": access_token, "token_type": "bearer"}
            return schemas.ResponseLoginItem(**service_response)