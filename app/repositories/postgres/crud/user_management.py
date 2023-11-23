from api.schemas.user_management import RequestDaftar, ResponseDaftarItem
import repositories.postgres.crud.utils as crud_utils
import services.utils as utils



class RepositoryUser:
    def __init__(self, database, db_model, logger):
        self.db_model = db_model
        self.database = database
        self.logger = logger

    async def create_user(self, req_payload:dict) -> dict:
        try:
            query = self.db_model.User.insert().values(
                username = req_payload.get('username'),
                hashed_password = utils.get_password_hash(req_payload.get('password')),
                nama = req_payload.get('nama'),
                role = req_payload.get('role'),
                email = req_payload.get('email'),
                created_at = crud_utils.current_datetime(),
                updated_at = None,
                is_deleted = False
            )
            await self.database.execute(query)
            return {
                'success' : True
            }
               
            
        except Exception as e:
            remark = 'Database Crud Error'
            self.logger.error(str(e))
            raise Exception(remark)


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
        
    async def get_user(self, username: str) -> dict:
        try:
            query = self.db_model.User.select().where(
                (self.db_model.User.c.username == username)
            ).with_only_columns(
                [
                    self.db_model.User.c.username,
                    self.db_model.User.c.nama,
                    self.db_model.User.c.role,
                    self.db_model.User.c.email,
                    self.db_model.User.c.created_at,
                    self.db_model.User.c.updated_at,
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
        
    async def select_users(self) -> list[dict]:
        try:
            query = self.db_model.User.select().with_only_columns(
                [
                    self.db_model.User.c.username,
                    self.db_model.User.c.nama,
                    self.db_model.User.c.role,
                    self.db_model.User.c.email,
                    self.db_model.User.c.created_at,
                    self.db_model.User.c.is_deleted,
                ]
            )
            user_list = await self.database.fetch_all(query)
            user_dicts = []
            for row in user_list:
                user_dict = dict(row)
                user_dict['created_at'] = user_dict['created_at'].strftime("%Y-%m-%d %H:%M:%S.%f")
                user_dicts.append(user_dict)
            return user_dicts
        except Exception as e:
            remark = 'Database Crud Error'
            self.logger.error(str(e))
            raise Exception(remark)


