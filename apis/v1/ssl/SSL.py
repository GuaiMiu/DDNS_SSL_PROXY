from fastapi import APIRouter, Request
import json
import logging

logger = logging.getLogger(__name__)

SSLRouter = APIRouter(tags=['SSL'])
CONFIG = 'config.json'


@SSLRouter.get("/api/v1/ssl/config")
async def get_config():
    with open(CONFIG, "r", encoding='utf-8') as loadConfig:
        fileData = json.load(loadConfig)['ssl']
        print(fileData)
    return {
        "code": 1,
        "message": "yes",
        "data": fileData
    }


@SSLRouter.post("/api/v1/ssl/config")
async def save_config(data: dict):
    print(data)
    logger.info(f'正在添加SSL配置')
    if data['ID']:
        with open(CONFIG, "r", encoding='utf-8') as loadConfig:
            fileData = json.load(loadConfig)
            fileData["ssl"][data['ID']] = data
            loadConfig.close()
        with open(CONFIG, "w", encoding='utf-8') as saveConfig:
            json.dump(fileData, saveConfig, ensure_ascii=False, indent=4)
            logger.info(f'配置：{data["ID"]}，添加成功')
    else:
        return {
            "code": 0,
            "message": "未填写配置名称"
        }

    return {
        "code": 1,
        "message": "yes"
    }

@SSLRouter.delete("/api/v1/ssl/config")
async def delete_config(del_id: dict):
    try:
        with open(CONFIG, "r", encoding='utf-8') as loadConfig:

            fileData = json.load(loadConfig)
            if del_id['delid'] in fileData['ssl']:
                del fileData['ssl'][str(del_id['delid'])]
                print(fileData)
            else:
                return {
                    "code": 0,
                    "message": "删除失败"
                }
            loadConfig.close()
        with open(CONFIG, "w", encoding='utf-8') as saveConfig:
            json.dump(fileData, saveConfig, ensure_ascii=False, indent=4)
        return {
            "code": 1,
            "message": "删除成功"
        }
    except:
        return {
            "code": 0,
            "message": "删除失败"
        }
