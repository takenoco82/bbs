from sqlalchemy import Column, String
# python - SqlAlchemy mysql millisecond or microsecond precision - Stack Overflow
#   https://stackoverflow.com/questions/29711102/sqlalchemy-mysql-millisecond-or-microsecond-precision
from sqlalchemy.dialects.mysql import DATETIME

from app.database import db


class Thread(db.Model):
    __tablename__ = "thread"

    id = Column(String(36), primary_key=True)
    title = Column(String(128), nullable=False)
    created_at = Column(DATETIME(fsp=6), nullable=False)
    updated_at = Column(DATETIME(fsp=6), nullable=False)
