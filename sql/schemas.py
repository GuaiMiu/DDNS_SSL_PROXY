from typing import List, Union

from pydantic import BaseModel


class UserBase(BaseModel):
    phone: str


# 为了安全起见，password 不会出现在其他同类 Pydantic模型中，例如用户请求时不应该从 API 返回响应中包含它。
class UserCreate(UserBase):  # 字段名对不上会报错，所以单独搞个
    password: str


class User(UserBase):
    id: int
    uname: str
    upasswd: str

    class Config:
        orm_mode = True
