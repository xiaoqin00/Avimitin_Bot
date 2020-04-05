# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/3/27 18:04
import telebot
from telebot import types
import random
import yaml
import re
import logging

# 读取yaml文件
with open("Reply.yml", "r+", encoding="UTF-8") as reply_file, \
        open("SSR_Lesson_Command.yml", "r+", encoding="UTF-8") as ssr_lesson_command_file, \
        open("config.yaml", 'r+', encoding='UTF-8') as token_file:
    reply_msg_dic = yaml.load(reply_file, Loader=yaml.FullLoader)
    ssr_lesson_command = yaml.load(ssr_lesson_command_file, Loader=yaml.FullLoader)
    bot_token = yaml.load(token_file, Loader=yaml.FullLoader)

TOKEN = bot_token['TOKEN']
print(TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.
# 初始化机器人
bot = telebot.TeleBot(TOKEN)


class Msg:
    count = 0
    reply_msg_list = list(reply_msg_dic.keys())

    # 正则搜索
    @staticmethod
    def msg_match(lines):
        # 计算回复的关键词字数
        count = len(Msg.reply_msg_list)-1
        # 关键词从列表最后一个开始匹配
        while count >= 0:
            keywords = Msg.reply_msg_list[count]
            msg_keywords_match = re.match(r'(.*)%s(.*)' % keywords, str(lines))
            if msg_keywords_match:
                Msg.get_count(count)
                return True
            else:
                count -= 1

    @staticmethod
    def get_count(num):
        Msg.count = num

    @staticmethod
    def print_count():
        return Msg.count


# 查询是否在字典，查询字典key对应值是否为列表，是则返回随机语句，否则直接返回key对应语句
@bot.message_handler(func=lambda message: Msg.msg_match(message.text))
def reply_msg(message):
    keywords = Msg.reply_msg_list[Msg.print_count()]  # 将回复列表中的键输出到变量中
    reply_words = reply_msg_dic[keywords]  # 将键输出到字典中
    if type(reply_words) == list:
        print('yes')
        num = random.randrange(len(reply_words))
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, reply_words[num])
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, reply_words)


# 命令返回语句
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "咱是个可爱的回话机器人，目前功能只有：\n" \
                          "/help，/lesson\n和简单的回复功能")


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, "你需要什么帮助？随便提，反正我帮不上忙")


# 输出按键回复，并关闭列表
@bot.message_handler(func=lambda message: message.text in ssr_lesson_command)
def send_ssr_lesson_back(message):
    bot.reply_to(message, ssr_lesson_command[message.text])
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, "教程关闭", reply_markup=markup)


# 输出键盘按键
@bot.message_handler(commands=['lesson'])
def send_a_reply(message):
    markup = types.ReplyKeyboardMarkup()
    item_ssr = types.KeyboardButton('ssr')
    item_clash = types.KeyboardButton('clashr订阅')
    item_shadowrocket = types.KeyboardButton('小火箭')
    item_clash2 = types.KeyboardButton('clash教程')
    markup.row(item_ssr, item_clash)
    markup.row(item_shadowrocket, item_clash2)
    bot.send_message(message.chat.id, "选择一个选项:", reply_markup=markup)


bot.polling()
