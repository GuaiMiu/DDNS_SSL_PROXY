from fastapi import APIRouter, Request
import json

from pydantic import BaseModel


DDNSRouter = APIRouter(tags=['DDNS'])
CONFIG = 'config.json'


# 获取配置
@DDNSRouter.get("/api/v1/ddns/config")
async def get_config():
    with open(CONFIG, "r", encoding='utf-8') as loadConfig:
        fileData = json.load(loadConfig)
    print("123123")
    return {
        "code": 1,
        "message": "yes",
        "data": fileData
    }


# 添加配置
@DDNSRouter.post("/api/v1/ddns/config")
async def save_config(data: dict):
    if data['ID']:
        with open(CONFIG, "r", encoding='utf-8') as loadConfig:
            fileData = json.load(loadConfig)
            fileData[data['ID']] = data
            loadConfig.close()
        with open(CONFIG, "w", encoding='utf-8') as saveConfig:
            saveConfig.write(json.dumps(fileData, indent=4, ensure_ascii=False))
    else:
        return {
            "code": 0,
            "message": "未填写配置名称"
        }

    return {
        "code": 1,
        "message": "yes"
    }


# 删除配置
@DDNSRouter.delete("/api/v1/ddns/config")
async def delete_config(del_id: dict):
    print(del_id)
    try:
        with open(CONFIG, "r", encoding='utf-8') as loadConfig:
            fileData = json.load(loadConfig)
            if del_id['delid'] in fileData:
                print(del_id['delid'])
                del fileData[del_id['delid']]
            else:
                return {
                    "code": 0,
                    "message": "删除失败"
                }
            loadConfig.close()
        with open(CONFIG, "w", encoding='utf-8') as saveConfig:
            saveConfig.write(json.dumps(fileData, indent=4, ensure_ascii=False))
        return {
            "code": 1,
            "message": "删除成功"
        }
    except:
        return {
            "code": 0,
            "message": "删除失败"
        }
