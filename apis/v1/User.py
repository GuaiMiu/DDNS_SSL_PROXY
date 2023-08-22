import time

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from sql import crud, models, schemas
from sql.base import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi import Header
from untils.jwtool import get_jwt_token

userRouter = APIRouter(tags=['用户相关'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserData(BaseModel):
    username: str
    password: str


@userRouter.post("/api/v1/user/login")
async def login(userdata: UserData, db: Session = Depends(get_db)):
    print(userdata)
    msg: dict = {
        'message': '',
        'code': 0,
        'data': {
            'token': ''
        }

    }

    try:
        user = crud.get_user(db, userdata.username)
        if userdata.password == user.upasswd:
            msg['message'] = "登录成功，即将跳转"
            msg['code'] = 1
            msg['data']['token'] = get_jwt_token(user.uname, 6)
            return msg
        else:
            msg['message'] = "密码错误"
            print(msg)
            return msg
    except:
        msg['message'] = "用户不存在"
        print(msg)
        return msg
