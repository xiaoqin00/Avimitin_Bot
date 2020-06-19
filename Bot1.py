# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/3/27 18:04
import telebot
from telebot import types
import random
import yaml
import re
import json
import logging
import time
from modules import regexp_search

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

# 从config文件读取token
with open("config/config.yaml", 'r+', encoding='UTF-8') as token_file:
    bot_token = yaml.load(token_file, Loader=yaml.FullLoader)
TOKEN = bot_token['TOKEN']

# 实例化机器人
bot = telebot.TeleBot(TOKEN)


# 命令返回语句
@bot.message_handler(commands=['start'])
def send_welcome(message):
    new_message = bot.send_message(message.chat.id, "咱是个可爱的回话机器人")
    time.sleep(120)
    bot.delete_message(chat_id=new_message.chat.id, message_id=new_message.message_id)


@bot.message_handler(commands=['help'])
def send_help(message):
    new_message = bot.send_message(message.chat.id, "你需要什么帮助？随便提，反正我帮不上忙")
    time.sleep(120)
    bot.delete_message(chat_id=new_message.chat.id, message_id=new_message.message_id)


# 关键词添加程序
@bot.message_handler(commands=['add'])
def add_keyword(message):
    if message.from_user.username != 'example':
        new_message = bot.send_message(message.chat.id, '别乱碰我！')
        time.sleep(120)
        bot.delete_message(chat_id=new_message.chat.id, message_id=new_message.message_id)
    else:
        if len(message.text) == 4:
            bot.send_message(message.chat.id, '/add 命令用法： `/add keyword=value` 。请不要包含空格。', parse_mode='Markdown')
        elif re.search(r' ', message.text[5:]):
            bot.send_message(message.chat.id, '请不要包含空格！')
        else:
            text = message.text[5:]
            split_sen = re.split(r'=', text)
            split_sen_dic = {split_sen[0]: split_sen[1]}
            bot.send_message(message.chat.id, '我已经学会了,当你说{}的时候，我会回复{}'.format(split_sen[0], split_sen[1]))
            with open('config/Reply.yml', 'a+', encoding='UTF-8') as reply_file:
                reply_file.write('\n')
                yaml.dump(split_sen_dic, reply_file, allow_unicode=True)


# 关键词删除程序
@bot.message_handler(commands=['delete'])
def del_keyword(message):
    if message.from_user.username != 'SaiToAsuKa_kksk':
        new_message = bot.send_message(message.chat.id, '你不是我老公，爬')
        time.sleep(10)
        bot.delete_message(chat_id=new_message.chat.id, message_id=new_message.message_id)
    else:
        if len(message.text) == 7:
            bot.send_message(message.chat.id, "/delete usage: `/delete keyword`.", parse_mode='Markdown')
        else:
            text = message.text[8:]
            with open('config/Reply.yml', 'r+', encoding='UTF-8') as reply_file:
                reply_msg_dic = yaml.load(reply_file, Loader=yaml.FullLoader)
            if reply_msg_dic.get(text):
                del reply_msg_dic[text]
                bot.send_message(message.chat.id, '已经删除{}'.format(text))
                with open('config/Reply.yml', 'w+', encoding='UTF-8') as new_file:
                    yaml.dump(reply_msg_dic, new_file, allow_unicode=True)
            else:
                msg = bot.send_message(message.chat.id, '没有找到该关键词')
                time.sleep(5)
                bot.delete_message(msg.chat.id, msg.message_id)


# 信息json处理
@bot.message_handler(commands=['dump'])
def dump_msg(message):
    text = json.dumps(message.json, sort_keys=True, indent=4, ensure_ascii=False)
    new_msg = bot.send_message(message.chat.id, text)
    time.sleep(60)
    bot.delete_message(new_msg.chat.id, new_msg.message_id)


@bot.message_handler(commands=['post'])
def post_message(message):
    if message.chat.type == 'supergroup':
        if message.from_user.id == 'YOUR_TG_ID':
            if message.reply_to_message:
                msg = bot.send_message(message.chat.id, '正在发送投稿')
                bot.forward_message('YOUR_CHANNEL_ID', message.chat.id, message.reply_to_message.message_id)
                bot.edit_message_text('投稿成功', msg.chat.id, msg.message_id)
                time.sleep(30)
                bot.delete_message(msg.chat.id, msg.message_id)
            else:
                bot.send_message(message.chat.id, '请回复一个消息来投稿')
        else:
            bot.send_message(message.chat.id, '只有管理员可以用！再乱动我扁你')
    else:
        bot.send_message(message.chat.id, '请在群组里使用')


# +--------------------------------------------------------------------------------------------+
# 查询关键词是否在字典，查询字典key对应值是否为列表，是则返回随机语句，否则直接返回key对应语句
# 语法糖中的lambda从导入的regexp模块中查询关键词存在与否，存在返回True，不存在返回False
# +--------------------------------------------------------------------------------------------+
re_mg = regexp_search.Msg()


@bot.message_handler(func=lambda message: re_mg.msg_match(message.text))
def reply_msg(message):
    msg_dic = re_mg.reply_msg_dic
    keyword = re_mg.keyword
    # 通过上面的keyword键从字典中读取值 
    reply_words = msg_dic[keyword]  
    if type(reply_words) == list:
        num = random.randrange(len(reply_words))
        bot.send_chat_action(message.chat.id, 'typing')
        new_msg = bot.send_message(message.chat.id, reply_words[num])
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        new_msg = bot.send_message(message.chat.id, reply_words)


if __name__ == '__main__':
    # 轮询
    bot.polling()
