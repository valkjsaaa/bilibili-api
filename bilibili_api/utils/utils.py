"""
bilibili_api.utils.utils

通用工具库
"""

import json
import os


def get_api(field: str):
    """
    获取 API

    :param field: API所属分类
    """
    path = os.path.abspath(os.path.join(os.path.dirname(
        __file__), "..", "data", "api", f"{field.lower()}.json"))
    if os.path.exists(path):
        with open(path, encoding="utf8") as f:
            return json.loads(f.read())


def crack_uid(crc32: str):
    """
    弹幕中的CRC32 ID转换成用户UID
    代码翻译自：https://github.com/esterTion/BiliBili_crc2mid
    """
    __CRCPOLYNOMIAL = 0xEDB88320
    __crctable = [None] * 256
    __index = [None] * 4

    def __create_table():
        for i in range(256):
            crcreg = i
            for j in range(8):
                if (crcreg & 1) != 0:
                    crcreg = __CRCPOLYNOMIAL ^ (crcreg >> 1)
                else:
                    crcreg >>= 1
            __crctable[i] = crcreg

    __create_table()

    def __crc32(input_):
        if type(input_) != str:
            input_ = str(input_)
        crcstart = 0xFFFFFFFF
        len_ = len(input_)
        for i in range(len_):
            index = (crcstart ^ ord(input_[i])) & 0xFF
            crcstart = (crcstart >> 8) ^ __crctable[index]
        return crcstart

    def __crc32lastindex(input_):
        if type(input_) != str:
            input_ = str(input_)
        crcstart = 0xFFFFFFFF
        len_ = len(input_)
        index = None
        for i in range(len_):
            index = (crcstart ^ ord(input_[i])) & 0xFF
            crcstart = (crcstart >> 8) ^ __crctable[index]
        return index

    def __getcrcindex(t):
        for i in range(256):
            if __crctable[i] >> 24 == t:
                return i
        return -1

    def __deepCheck(i, index):
        tc = 0x00
        str_ = ""
        hash_ = __crc32(i)
        tc = hash_ & 0xFF ^ index[2]
        if not (57 >= tc >= 48):
            return [0]
        str_ += str(tc - 48)
        hash_ = __crctable[index[2]] ^ (hash_ >> 8)

        tc = hash_ & 0xFF ^ index[1]
        if not (57 >= tc >= 48):
            return [0]
        str_ += str(tc - 48)
        hash_ = __crctable[index[1]] ^ (hash_ >> 8)

        tc = hash_ & 0xFF ^ index[0]
        if not (57 >= tc >= 48):
            return [0]
        str_ += str(tc - 48)
        hash_ = __crctable[index[0]] ^ (hash_ >> 8)

        return [1, str_]

    ht = int(crc32, 16) ^ 0xFFFFFFFF
    i = 3
    while i >= 0:
        __index[3-i] = __getcrcindex(ht >> (i*8))
        snum = __crctable[__index[3-i]]
        ht ^= snum >> ((3-i)*8)
        i -= 1
    for i in range(10000000):
        lastindex = __crc32lastindex(i)
        if lastindex == __index[3]:
            deepCheckData = __deepCheck(i, __index)
            if deepCheckData[0]:
                break
    if i == 10000000:
        return -1
    return str(i) + deepCheckData[1]
