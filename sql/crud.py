from sqlalchemy.orm import Session

from . import models, schemas


# 通过 ID 查询单个用户。
def get_user(db: Session, user: str):
    return db.query(models.User).filter(models.User.uname == user).first()
