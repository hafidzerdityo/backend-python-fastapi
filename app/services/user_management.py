from api.schemas.user_management import RequestDaftar, ResponseDaftarItem, RequestUser, ResponseUserItem
import services.utils as utils
from jose import jwt
from repositories.postgres.crud.user_management import RepositoryUser

class UserService:
    def __init__(self, repo, database, logger):
        self.repo = repo
        self.database = database
        self.logger = logger

    async def post_user(self, req_payload: dict) -> dict:
        async with self.database.transaction():
            user_exist = await self.repo.get_user(req_payload.get('username'))
            if user_exist:
                raise Exception("Username is already exist")
            if not utils.validate_password(req_payload.get('password')):
                raise Exception("Password should have a minimum of 6 digits and must include at least 1 symbol, 1 number, and 1 uppercase letter")

            get_rekening = await self.repo.create_user(req_payload=req_payload)
            
        return get_rekening

    async def get_user(self, token: str) -> dict:
        async with self.database.transaction():
            payload = jwt.decode(token, utils.SECRET_KEY, algorithms=["HS256"])
            user_exist = await self.repo.get_user(payload.get('username'))
            if not user_exist:
                raise Exception("Username Does Not Exist")
        return user_exist   
    
    async def select_users(self, token: str) -> list[dict]:
        async with self.database.transaction():
            payload = jwt.decode(token, utils.SECRET_KEY, algorithms=["HS256"])
            if payload['role'] != 'admin':
                raise Exception("Unauthorized role")
            list_user = await self.repo.select_users()
            if not list_user:
                raise Exception("List of Users is not exist")
        return list_user   

def init_service_user(database, db_model, logger):
    repo = RepositoryUser(database, db_model, logger)
    return UserService(repo,database,logger)