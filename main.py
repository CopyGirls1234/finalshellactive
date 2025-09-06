from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

import re
from Crypto.Hash import keccak
from Crypto.Hash import MD5
def md5(msg):
    hash_obj = MD5.new(msg)
    return hash_obj.hexdigest()
def keccak384(msg):
    hash_obj = keccak.new(data=msg, digest_bits=384)
    return hash_obj.hexdigest()

@register("active", "finalshell", "FinalShell离线授权。", "v3.6.3")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
    
    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("active")
    async def active(self, event: AstrMessageEvent):
        """参数是机器码""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        result = re.search(r'\s([^\s]+)$', message_str).group(1)  # 匹配最后一个空格后的非空格内容
        yield event.plain_result(f"{user_name}您的专业版激活码：{keccak384(f'{result}Scfg*ZkvJZc,s,Y'.encode())[12:28]}") # 发送一条纯文本消息

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
