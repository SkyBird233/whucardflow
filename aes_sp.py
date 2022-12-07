from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode
import random


# 加密方式：AES-128-CBC，密钥长度：16，偏移量长度：16，填充方式：PKCS7Padding，密文前 64 位随机字符串
def encrypt(data, key):
    data = (random_string(64) + data).encode("utf-8")
    key = key.encode("utf-8")
    iv = random_string(16).encode("utf-8")
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    ct = b64encode(ct_bytes).decode("utf-8")
    return ct


# 原 js 的随机字符串生成函数
def random_string(len):
    chars = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678"
    return_str = ""
    for i in range(len):
        return_str += random.choice(chars)
    return return_str
