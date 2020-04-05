# Telegram机器人

## @Avimitin_bot

- 机器人地址：https://t.me/Avimitin_bot

- 机器人目前所拥有的功能：回话和回复命令。
- 机器人使用的依赖：`PyYaml`,`PyTelegramBotAPI`
- 机器人的特性：不使用api的`regexp`功能回话，通过yaml文件的独特文件格式，实现自定义关键词回复的功能，从而减少代码行数。并且支持单关键词多语句回复，实现随机回话的效果。

- 使用方法：

> 安装好python3.8，和上述依赖。
>
> 本地新建目录，使用`git clone https://github.com/Avimitin/Avimitin_Bot.git`命令下载源码。
>
> 新建一个`Reply.yaml`和`config.yaml`文件
>
> 在`config.yaml`里添加`TOKEN: 你的token`，保存退出
>
> 在`Reply.yaml`文件里按照以下格式添加关键词和回复:
>
> ```yaml
>keywords: replywords
> keywords2:
>    - replywords1
>    - replywords2
> ```
> 
> 最后添加代理执行`python Bot1.py`即可

- 目前还支持ssr教程回复，如果没有需要请把相关代码删除。

## @avimitin_forward_bot

- 机器人地址: https://t.me/avimitin_forward_bot
- 机器人目前功能：转发信息到我UID里
- 机器人依赖：`PyTelegramBotAPI`
- 机器人特性：普通的转发机器人。

