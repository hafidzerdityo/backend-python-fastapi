from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DATE, Table, DateTime, Numeric, BOOLEAN
from sqlalchemy.orm import relationship
from repositories.postgres.config.database_config import metadata, SQLALCHEMY_DATABASE_URL


User = Table(
    "user",
    metadata,
    Column('username',String(20),primary_key=True, unique=True, index=True, nullable=False),
    Column('hashed_password',String(255), unique=True, index=True, nullable=False),
    Column('nama',String(255), index=True, nullable=False),
    Column('role',String(30), index=True, nullable=False),
    Column('divisi',String(255), index=True, nullable=False),
    Column('jabatan',String(255), index=True, nullable=False),
    Column('created_at' ,DateTime, index=True, nullable=False),
    Column('updated_at' ,DateTime, index=True),
    Column('is_deleted', BOOLEAN)
)

Transaksi = Table(
    'transaksi',
    metadata, 
    Column('id',Integer, primary_key=True, index=True),
    Column('kategori' ,String(255), index=True),
    Column('metode_pengadaan' ,String(255), index=True),
    Column('created_at', DateTime, index=True, nullable=False),
    Column('updated_at', DateTime, index=True),
    Column('bsu', Numeric(precision=10, scale=2), index=True, nullable=False),
    Column('username',String(20), ForeignKey("user.username"), index=True, nullable=False)
)
