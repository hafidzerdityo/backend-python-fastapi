import repositories.postgres.config.db_model as db_model
from repositories.postgres.config.database_config import database
from api.schemas.user_management import RequestDaftar, ResponseDaftarItem
import repositories.postgres.crud.utils as crud_utils
import services.utils as utils
from log.log import logger

################## Start of post_user services ##################

async def check_user(username: str):
    try:
        query = db_model.User.select().where(
            (db_model.User.c.username == username)
        ).with_only_columns(
            [
                db_model.User.c.username,
                db_model.User.c.nama,
                db_model.User.c.role,
                db_model.User.c.divisi,
                db_model.User.c.jabatan,
                db_model.User.c.created_at,
                db_model.User.c.is_deleted,
            ]
        )
        user_exist = await database.fetch_one(query)
        
        if user_exist:
            user_exist = dict(user_exist)
            user_exist['created_at'] = user_exist['created_at'].strftime("%Y-%m-%d %H:%M:%S.%f")
        else:
            user_exist = {}
        return user_exist
    except Exception as e:
        remark = 'Database Crud Error'
        logger.error(str(e))
        raise Exception(remark)

async def create_user(req_payload:RequestDaftar) -> ResponseDaftarItem:
    try:
        query = db_model.User.insert().values(
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
        await database.execute(query)
        return ResponseDaftarItem(
            success = True
        )
    except Exception as e:
        remark = 'Database Crud Error'
        logger.error(str(e))
        raise Exception(remark)

################## End of post_user services ##################