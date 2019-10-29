from sqlalchemy import Column, String

from app.database import db
from app.models.utils import AwareDateTime


class Thread(db.Model):
    __tablename__ = "thread"

    id = Column(String(36), primary_key=True)
    title = Column(String(128), nullable=False)
    created_at = Column(AwareDateTime, nullable=False)
    updated_at = Column(AwareDateTime, nullable=False)

    @classmethod
    def find_list(cls):
        return Thread.query.order_by(Thread.updated_at.asc()).all()
