# 此为后端更新DDNS的工具

import json
from untils.dnspod_demo import update_domain
from untils.ali_demo import update_domain as ali_update_domain
import logging
from untils.get_ip import get_public_ip
from untils.edit_config import edit_config
logger = logging.getLogger(__name__)
profilefile = 'config.json'


def update():
    try:
        logger.info("开始更新IP，祝你好运！")
        with open(profilefile, "r", encoding="utf-8") as file:
            json_data = file.read()
            Config = json.loads(json_data)
            file.close()
        if Config == {}:
            logger.error("请添加配置！")
            return
        for config_name, config_values in Config.items():
            dns_provider = config_values["DNS"]
            if dns_provider == "腾讯云":
                id_value = config_values["ID"]
                domain = config_values["DOMAIN"]
                record_type = config_values["RECORD_TYPE"]
                secret_id = config_values["SECRET_ID"]
                secret_key = config_values["SECRET_KEY"]
                sub_domain = config_values["SUB_DOMAIN"]
                created_time = config_values["CREATED_TIME"]
                # 配置名
                ip = get_public_ip()
                res = update_domain(domain, sub_domain, record_type, ip, secret_id, secret_key, id_value)
                if res['code'] == 1:
                    STATUS = res['message']
                    logger.error(f"配置{id_value}:" + res.get_message())
                elif res['code'] == 0:
                    STATUS = res['message']
                    logger.info(res)
                edit_config(id_value,'STATUS',STATUS)

            elif dns_provider == "阿里云":
                id_value = config_values["ID"]
                domain = config_values["DOMAIN"]
                record_type = config_values["RECORD_TYPE"]
                ACCESS_KEY_ID = config_values["ACCESS_KEY_ID"]
                ACCESS_KEY_SECRET = config_values["ACCESS_KEY_SECRET"]
                sub_domain = config_values["SUB_DOMAIN"]
                created_time = config_values["CREATED_TIME"]
                # 配置名
                ip = get_public_ip()
                res = ali_update_domain(domain, sub_domain, record_type, ip, ACCESS_KEY_ID, ACCESS_KEY_SECRET, id_value)

                if res['code'] == 1:
                    print(res['message'])
                    STATUS = res['message']
                    logger.info(res['message'])
                elif res['code'] == 0:
                    STATUS = res['message']
                    logger.info(res)
                edit_config(id_value,'STATUS',STATUS)
    except:
        logger.error("更新失败！请检查配置", )
        return
