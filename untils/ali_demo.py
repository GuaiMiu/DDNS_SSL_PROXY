# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.


from alibabacloud_alidns20150109.client import Client as Alidns20150109Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alidns20150109 import models as alidns_20150109_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


def create_client(
        access_key_id: str,
        access_key_secret: str,
) -> Alidns20150109Client:
    """
    使用AK&SK初始化账号Client
    @param access_key_id:
    @param access_key_secret:
    @return: Client
    @throws Exception
    """
    config = open_api_models.Config(
        # 必填，您的 AccessKey ID,
        access_key_id=access_key_id,
        # 必填，您的 AccessKey Secret,
        access_key_secret=access_key_secret
    )
    # Endpoint 请参考 https://api.aliyun.com/product/Alidns
    config.endpoint = f'alidns.cn-hangzhou.aliyuncs.com'
    return Alidns20150109Client(config)


def update_domain(domain: str, subdomain: str, recordtype, ip, accesskeyid, access_key_secret, ID):
    client = create_client(
        accesskeyid,
        access_key_secret)
    describe_domain_records_request = alidns_20150109_models.DescribeDomainRecordsRequest(
        domain_name=domain
    )
    runtime = util_models.RuntimeOptions()
    try:
        response = client.describe_domain_records_with_options(describe_domain_records_request, runtime)
        if response.status_code != 200:
            return
        for records in response.body.domain_records.record:
            # 如果存在此记录则更新
            if records.rr == subdomain and records.type == recordtype:

                if records.value == ip:
                    print(records.value)
                    return {
                        "code": 1,
                        "message": f"配置{ID}:" + "IP未改变，不用更新！"
                    }
                update_domain_record_request = alidns_20150109_models.UpdateDomainRecordRequest(
                    record_id=records.record_id,
                    type=recordtype,
                    value=ip,
                    rr=subdomain
                )
                try:
                    # 复制代码运行请自行打印 API 的返回值
                    client.update_domain_record_with_options(update_domain_record_request, runtime)
                    return {
                        "code": 1,
                        "message": f"配置{ID}:  " + "IP更新成功！"
                    }
                except Exception as error:
                    # 如有需要，请打印 error
                    return {
                        "code": 0,
                        "message": error.message
                    }

        # 反之则添加记录
        add_domain_record_request = alidns_20150109_models.AddDomainRecordRequest(
            domain_name=domain,
            rr=subdomain,
            type=recordtype,
            value=ip
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            client.add_domain_record_with_options(add_domain_record_request, runtime)
            return {
                "code": 1,
                "message": f"配置{ID}:  " + "新纪录添加成功！"
            }
        except Exception as error:
            # 如有需要，请打印 error
            return {
                "code": 0,
                "message": error.message
            }



    except Exception as error:
        # 如有需要，请打印 error
        # print(error)
        return {
            "code": 0,
            "message": error.message
        }
