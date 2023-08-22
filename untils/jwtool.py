import jwt
import time

JWT_TOKEN_EXPIRE_TIME = 3600 * 2  # token有效时间 2小时
JWT_SECRET = 'SECRET_KEY'  # 加解密密钥
JWT_ALGORITHM = 'HS256'  # 加解密算法


def get_jwt_token(username: str, hour: int):
    timestamp = int(time.time()) + 3600 * hour
    return jwt.encode({"user": username, "exp": timestamp}, JWT_SECRET, JWT_ALGORITHM)


def verify_jwt_token(token: str):
    """验证用户token"""
    try:
        de_token = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
        # print(de_token)
        return True
    except jwt.ExpiredSignatureError:
        print('Token:过期')
    except jwt.InvalidTokenError:
        print('Token:无效')
