from fastapi import Depends, FastAPI, Header, HTTPException, Request
from apis.v1.User import userRouter
from apis.v1.ddns.ServiceConfig import serviceConfig
from apis.v1.ddns.DDNS import DDNSRouter
import jwt
from untils.jwtool import verify_jwt_token
from sql import crud, models, schemas
from sql.base import SessionLocal, engine
from sqlalchemy.orm import Session
import logging
# 预先创建数据表
models.Base.metadata.create_all(bind=engine)
#日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# 定时任务
from apscheduler.schedulers.background import BackgroundScheduler
from untils.ddns import update

scheduler = BackgroundScheduler()
# 添加定时任务，每5分钟执行一次
scheduler.add_job(update, 'interval', seconds=300)
# 启动调度器
scheduler.start()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


demo = {
    "message": 'Token失效或你想干坏事？',
    "code": 0
}


async def verify_token(request: Request, Authorization: str = Header(...)):
    # print(request.get('path'))
    path: str = request.get('path')
    print(Authorization)
    if path.startswith('/api/v1/user/login'):
        return
    elif verify_jwt_token(Authorization):
        return
    else:
        print('========================')
        raise HTTPException(status_code=200, detail=demo)


app = FastAPI(dependencies=[Depends(verify_token)])
# app = FastAPI()


@app.get("/")
async def root(db: Session = Depends(get_db)):
    a = crud.get_user(db, 'demo')
    return a.upasswd


def shutdown_event():
    """
    应用关闭时停止调度器
    """
    scheduler.shutdown()


app.include_router(userRouter)
app.include_router(serviceConfig)
app.include_router(DDNSRouter)
