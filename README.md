![LOGO](https://pic.imgdb.cn/item/6023d5aa3ffa7d37b3cb1d23.png)

# 该分支目前正在开发，不能使用

# bilibili-api

[![API数量](https://img.shields.io/badge/API数量-100+-blue)][api.json]
[![STARS](https://img.shields.io/github/stars/Passkou/bilibili_api?color=yellow&label=Github%20Stars)][stargazers]
[![LICENSE](https://img.shields.io/badge/LICENSE-GPLv3-red)][license]
![Python](https://img.shields.io/badge/Python-3.9|3.8|3.7-blue)
[![Testing](https://github.com/Passkou/bilibili-api/actions/workflows/test.yml/badge.svg)](https://github.com/Passkou/bilibili-api/actions/workflows/test.yml)

**开发文档**: [bilibili_api 开发文档][docs]

# 简介

这是一个用 Python 写的调用 [Bilibili](https://www.bilibili.com) 各种 API 的库，
范围涵盖视频、音频、直播、动态、专栏、用户、番剧等[[1]](#脚注)。

## 特色

- 范围涵盖广，基本覆盖常用的爬虫，操作。
- 可使用代理，绕过b站风控策略。
- 全面支持 BV 号（bvid），同时也兼容 AV 号（aid）。
- 调用简便，函数命名易懂，代码注释详细。
- 不仅仅是官方提供的 API！还附加：AV 号与 BV 号互转[[2]](#脚注)、连接直播弹幕 Websocket 服务器、视频弹幕反查[[3]](#脚注)、专栏内容爬取等。
- **全部是异步操作**。

# 快速上手

首先使用以下指令安装本模块：

```
$ pip install bilibili-api
```

接下来我们来获取视频的播放量等信息：

```python
import asyncio
from bilibili_api import video

async def main():
    # 实例化 Video 类
    v = video.Video(bvid="BV1uv411q7Mv")
    # 获取信息
    info = await v.get_info()
    # 打印信息
    print(info)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
```

输出（已格式化，已省略部分）：

```json
{
    "bvid": "BV1uv411q7Mv",
    "aid": 243922477,
    "videos": 1,
    "tid": 17,
    "tname": "单机游戏",
    "copyright": 1,
    "pic": "http://i2.hdslb.com/bfs/archive/82e52df9d0221836c260c82f2890e3761a46716b.jpg",
    "title": "爆肝９８小时！在MC中还原糖调小镇",
    "pubdate": 1595203214,
    "ctime": 1595168654,
    ...and more
}
```

如何给这个视频点赞？我们需要登录自己的账号。

这里设计是传入一个 Credential 类，获取所需的信息参照：[获取 Credential 类所需信息][get-credential]

下面的代码将会给视频点赞

```python
import asyncio
from bilibili_api import video, Credential

async def main():
    # 实例化 Credential 类
    credential = Credential(sessdata="你的 SESSDATA", bili_jct="你的 bili_jct")
    # 实例化 Video 类
    v = video.Video(bvid="BV1uv411q7Mv", credential=credential)
    # 给视频点赞
    await v.set_like(True)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
```

如果没有报错，就代表调用 API 成功，你可以到视频页面确认是不是调用成功了。

**注意，请不要泄露这两个值给他人，否则你的账号将可能遭受盗号的风险！**

**注意，请不要泄露这两个值给他人，否则你的账号将可能遭受盗号的风险！**

**注意，请不要泄露这两个值给他人，否则你的账号将可能遭受盗号的风险！**

# FA♂Q

## Q: 关于 API 调用的正确姿势是什么？

A: 所有 API 调用，请尽量使用 **指名方式** 传参，
因为 API 较多，可能不同函数的传参顺序不一样，例子：

```python
# 推荐
video.get_info(bvid="BV1uv411q7Mv")

# 当然也可以这样
kwargs = {
    "bvid": "BV1uv411q7Mv"
}
video.get_info(**kwargs)

# 不推荐
video.get_info("BV1uv411q7Mv")
```

## Q: 为什么会提示 412 Precondition Failed ？

A: 你的请求速度太快了。造成请求速度过快的原因可能是你写了高并发的代码。

这种情况下，你的 IP 会暂时被封禁而无法使用，你可以设置代理绕过。

```python
from bilibili_api import settings

settings.proxy = "http://your-proxy.com" # 里头填写你的代理地址
```

## Q: 怎么没有我想要的功能？

A: 你可以发 Issue 来提交你的需求，但是，最好的办法是自己写（懒）

## Q: 我有一个大胆的想法，如何给代码库贡献？

A: 请先 clone 本仓库一份，然后从 main 分支新建一个分支，在该分支上工作。
如果你觉得已经可以了，请向项目仓库的 develop 分支发起 Pull request。
如果你不明白这些操作的话，可以百度。

# 脚注

+ \[1\] 这里只列出一部分，请以实际API为准。
+ \[2\] 代码来源：<https://www.zhihu.com/question/381784377/answer/1099438784>
+ \[3\] 代码翻译自：<https://github.com/esterTion/BiliBili_crc2mid>


[docs]: https://github.com/Passkou/bilibili-api/blob/main/docs
[api.json]: https://github.com/Passkou/bilibili-api/tree/main/bilibili-api/data/api/
[license]: https://github.com/Passkou/bilibili-api/tree/main/LICENSE.md
[stargazers]: https://github.com/Passkou/bilibili-api/stargazers
[get-credential]: https://github.com/Passkou/bilibili-api/blob/main/docs/获取%20Credential%20类所需信息