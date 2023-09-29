from api.schemas.user_management import RequestDaftar, ResponseDaftarItem
import repositories.postgres.crud.utils as crud_utils
import services.utils as utils



class RepositoryUser:
    def __init__(self, database, db_model, logger):
        self.db_model = db_model
        self.database = database
        self.logger = logger

    # # RAW Query Example
    # async def check_user(self, username: str):
    #     try:
    #         query = f"""
    #             SELECT username, nama, role, divisi, jabatan, created_at, is_deleted
    #             FROM "user"
    #             WHERE username = :username
    #         """
    #         user_exist = await self.database.fetch_one(query=query, values={"username": username})
            
    #         if user_exist:
    #             user_exist = dict(user_exist)
    #             user_exist['created_at'] = user_exist['created_at'].strftime("%Y-%m-%d %H:%M:%S.%f")
    #         else:
    #             user_exist = {}
    #         return user_exist
    #     except Exception as e:
    #         remark = 'Database Crud Error'
    #         self.logger.error(str(e))
    #         raise Exception(remark)
        
    async def check_user(self, username: str):
        try:
            query = self.db_model.User.select().where(
                (self.db_model.User.c.username == username)
            ).with_only_columns(
                [
                    self.db_model.User.c.username,
                    self.db_model.User.c.nama,
                    self.db_model.User.c.role,
                    self.db_model.User.c.divisi,
                    self.db_model.User.c.jabatan,
                    self.db_model.User.c.created_at,
                    self.db_model.User.c.is_deleted,
                ]
            )
            user_exist = await self.database.fetch_one(query)
            
            if user_exist:
                user_exist = dict(user_exist)
                user_exist['created_at'] = user_exist['created_at'].strftime("%Y-%m-%d %H:%M:%S.%f")
            else:
                user_exist = {}
            return user_exist
        except Exception as e:
            remark = 'Database Crud Error'
            self.logger.error(str(e))
            raise Exception(remark)

    async def create_user(self, req_payload:RequestDaftar) -> ResponseDaftarItem:
        try:
            query = self.db_model.User.insert().values(
                username = req_payload.username,
                hashed_password = utils.get_password_hash(req_payload.password),
                nama = req_payload.nama,
                role = req_payload.role,
                divisi = req_payload.divisi,
                jabatan = req_payload.jabatan,
                created_at = crud_utils.current_datetime(),
                updated_at = None,
                is_deleted = False
            )
            await self.database.execute(query)
            return ResponseDaftarItem(
                success = True
            )
        except Exception as e:
            remark = 'Database Crud Error'
            self.logger.error(str(e))
            raise Exception(remark)

