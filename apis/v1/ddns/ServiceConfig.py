from fastapi import APIRouter, Depends
from pydantic import BaseModel

from sql import crud, models, schemas
from sql.base import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi import Header
from untils.jwtool import get_jwt_token

serviceConfig = APIRouter(tags=['获取服务商所需要的配置文件'])


@serviceConfig.get("/api/v1/ddns/serviceconfig")
async def service_config(data: str):
    print(data)
    return {
        "code": 1,
        "message": "yes",
        "data": [
            {
                'SERVICE_NAME': '腾讯云',
                'KEY_NUM': 2,
                'HELP_URL': 'https://console.cloud.tencent.com/cam/capi',
                'KEY': ['SECRET_ID', 'SECRET_KEY']
            },
            {
                'SERVICE_NAME': '阿里云',
                'KEY_NUM': 2,
                'HELP_URL': 'https://ram.console.aliyun.com/manage/ak',
                'KEY': ['ACCESS_KEY_ID', 'ACCESS_KEY_SECRET']
            }
        ]
    }
