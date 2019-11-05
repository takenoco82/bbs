from sqlalchemy import Column, String

from app.database import db
from app.models.utils import AwareDateTime


class Thread(db.Model):
    __tablename__ = "thread"

    id = Column(String(36), primary_key=True)
    title = Column(String(128), nullable=False)
    created_at = Column(AwareDateTime, nullable=False)
    updated_at = Column(AwareDateTime, nullable=False)

    def __repr__(self):
        return (
            f"<Thread("
            f"id={self.id!r} "
            f"title={self.title!r} "
            f"created_at={self.created_at!r} "
            f"updated_at={self.updated_at!r})"
            ">"
        )

    @classmethod
    def find_list(cls):
        return Thread.query.order_by(Thread.updated_at.asc()).all()

    def save(self):
        db.session.add(self)
        # TODO トランザクションは個々で管理するのではなく、原則、リクエスト単位で管理する
        db.session.commit()
