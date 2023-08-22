import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.dnspod.v20210323 import dnspod_client, models
import logging
logger = logging.getLogger(__name__)
API_URL = "dnspod.tencentcloudapi.com"


def update_domain(domain: str, subdomain: str, recordtype, ip, secretid: str, secretkey: str,ID:str):
    get_record_params = {
        "Domain": domain
    }
    create_params = {
        "Domain": domain,
        "SubDomain": subdomain,
        "RecordType": recordtype,
        "RecordLine": "默认",
        "Value": ip
    }
    update_params = {
        "Domain": domain,
        "SubDomain": subdomain,
        "RecordType": recordtype,
        "RecordLine": "默认",
        "Value": ip
    }

    try:
        cred = credential.Credential(secretid, secretkey)
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = API_URL

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = dnspod_client.DnspodClient(cred, "", clientProfile)

        # 首先获取域名解析列表，判断是否存在记录
        getrecord_req = models.DescribeRecordListRequest()
        getrecord_req.from_json_string(json.dumps(get_record_params))
        recordlist_res = json.loads(client.DescribeRecordList(getrecord_req).to_json_string())['RecordList']

        # 循环获取想要的信息
        for record_list in recordlist_res:
            record = record_list["Name"]
            record_type = record_list["Type"]
            record_id = record_list['RecordId']

            if subdomain == record and recordtype == record_type:
                if record_list['Value'] == ip:
                    return {
                        "code": 1,
                        "message": f"配置{ID}:" + "IP未改变，不用更新！"
                    }
                update_params.update({"RecordId": record_id})
                # 如果存在当然就是更新记录呀呀
                update_req = models.ModifyRecordRequest()
                update_req.from_json_string(json.dumps(update_params))

                # 返回的resp是一个ModifyRecordResponse的实例，与请求对象对应
                update_res = client.ModifyRecord(update_req)
                # 输出json格式的字符串回包
                #print(update_res.to_json_string())
                return {
                    "code": 1,
                    "message": f"配置{ID}:"+"IP更新成功！"
                }

        # 如果不存在当然是添加记录呀 为什么不写到上面if的后面 因为我SB了，上面是for循环如果写道里面 凡是不等于的都会执行添加 我真是个SB
        create_record = models.CreateRecordRequest()
        create_record.from_json_string(json.dumps(create_params))
        resp = client.CreateRecord(create_record)
        # 输出json格式的字符串回包
        #print(resp.to_json_string())
        return {
            "code": 1,
            "message": f"配置{ID}:"+"新纪录添加成功！"
        }

    except TencentCloudSDKException as err:
        return {
            "code": 0,
            "message":err
        }


