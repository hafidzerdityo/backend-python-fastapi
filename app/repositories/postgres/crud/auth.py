import repositories.postgres.config.db_model as db_model
from repositories.postgres.config.database_config import database
from api.schemas.user_management import RequestDaftar, ResponseDaftarItem
import repositories.postgres.crud.utils as utils
from log.log import logger

async def get_hashed_pass_by_username(username: str) -> dict:
    try:
        query = db_model.User.select().where(db_model.User.c.username == username)
        row = await database.fetch_one(query)
        if row:
            return dict(row)
        else:
            return {}
    except Exception as e:
        remark = 'Database Crud Error'
        logger.error(str(e))
        raise Exception(remark)
    
    