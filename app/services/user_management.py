from api.schemas.user_management import RequestDaftar, ResponseDaftarItem, RequestUser, ResponseUserItem
import repositories.postgres.crud.user_management as crud
import services.utils as utils
from jose import JWTError, jwt

class UserService:
    def __init__(self, database, logger):
        self.database = database
        self.logger = logger

    async def post_user(self, req_payload: RequestDaftar) -> ResponseDaftarItem:
        async with self.database.transaction():
            user_exist = await crud.check_user(req_payload.username)
            if user_exist:
                raise Exception("Username Sudah Terdaftar")
            if not utils.validate_password(req_payload.password):
                raise Exception("Password minimal 6 angka dengan minimal 1 simbol, 1 angka, dan 1 huruf besar")

            get_rekening = await crud.create_user(req_payload=req_payload)
            
        return get_rekening

    async def get_user(self, token):
        async with self.database.transaction():
            payload = jwt.decode(token, utils.SECRET_KEY, algorithms=["HS256"])
            user_exist = await crud.check_user(payload.get('username'))
            if not user_exist:
                raise Exception("Username Belum Terdaftar")
        return user_exist   
