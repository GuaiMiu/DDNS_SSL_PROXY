from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
# 1.用Base类来创建 SQLAlchemy 模型
from .base import Base


class User(Base):
    __tablename__ = "users"
    # 2.创建模型属性/列
    id = Column(Integer, primary_key=True, index=True)
    uname = Column(String,index=True)
    upasswd = Column(String)



