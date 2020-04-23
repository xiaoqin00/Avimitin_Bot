# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/3/27 18:04
import telebot
from telebot import types
import random
import yaml
import regexp_search
import re
import time
import weather
import json

# 从config文件读取token
with open("config.yaml", 'r+', encoding='UTF-8') as token_file:
    bot_token = yaml.load(token_file, Loader=yaml.FullLoader)
TOKEN = bot_token['TOKEN']

# 实例化机器人
bot = telebot.TeleBot(TOKEN)

# 将列表赋值到简易列表,提高易读性
msg_list = regexp_search.Msg.reply_msg_list
msg_dic = regexp_search.reply_msg_dic


# 查询关键词是否在字典，查询字典key对应值是否为列表，是则返回随机语句，否则直接返回key对应语句
# 语法糖中的lambda从导入的regexp模块中查询关键词存在与否，存在返回True，不存在返回False
@bot.message_handler(func=lambda message: regexp_search.Msg.msg_match(message.text))
def reply_msg(message):
    keywords = msg_list[regexp_search.Msg.print_count()]  # 将回复列表中的键指向变量keyword
    reply_words = msg_dic[keywords]  # 通过上面的keyword键从字典中读取值
    if type(reply_words) == list:
        num = random.randrange(len(reply_words))
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, reply_words[num])
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, reply_words)


# 命令返回语句
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "咱是个可爱的回话机器人，目前功能只有：\n/help /closemenu /add /weather /lesson")


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, "你需要什么帮助？随便提，反正我帮不上忙")


@bot.message_handler(commands=['closemenu'])
def close_menu(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, "菜单关闭", reply_markup=markup)


# 关键词添加程序
@bot.message_handler(commands=['add'])
def add_keyword(message):
    if message.chat.username != 'SaiToAsuKa_kksk':
        bot.send_message(message.chat.id, '你不是我老公，爬')
    else:
        if len(message.text) == 4:
            bot.send_message(message.chat.id, '/add 命令用法： `/add keyword=value` 。请不要包含空格。', parse_mode='Markdown')
        elif re.search(r' ', message.text[5:]):
            bot.send_message(message.chat.id, '请不要包含空格！')
        else:
            text = message.text[5:]
            split_sen = re.split(r'=', text)
            split_sen_dic = {split_sen[0]: split_sen[1]}
            bot.send_message(message.chat.id, '我已经学会了,当你说{}的时候，我会回复{}'.format(split_sen[0],split_sen[1]))
            with open('Reply.yml', 'a+', encoding='UTF-8') as reply_file:
                reply_file.write('\n')
                yaml.dump(split_sen_dic, reply_file, encoding='UTF-8')


# 发送天气
@bot.message_handler(commands=['weather'])
def confirm(message):
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, '请告诉我你在哪里~我来帮你查天气~\n目前只支持中国城市哟', reply_markup=markup)
    bot.register_next_step_handler(message, transfer)


def transfer(message):
    weather.Weather.get_weather(message.text)

    bot.send_message(message.chat.id, message.text + '今天的天气：\n' + weather.Weather.today)

    markup = types.ReplyKeyboardMarkup()
    item_city = types.KeyboardButton('城市数据')
    item_tips = types.KeyboardButton('天气小贴士')
    item_tomorrow = types.KeyboardButton('明天天气')
    item_close = types.KeyboardButton('关闭菜单')
    markup.row(item_tips, item_tomorrow)
    markup.row(item_city, item_close)
    bot.send_message(message.chat.id, '还有什么需要查询的呢？', reply_markup=markup)
    bot.register_next_step_handler(message, next_wea_search)


def next_wea_search(message):
    if message.text == '城市数据':
        bot.send_message(message.chat.id, weather.Weather.data)
        bot.send_message(message.chat.id, '这部分数据还在维修哦~')
        close_menu(message)
    elif message.text == '天气小贴士':
        bot.send_message(message.chat.id, weather.Weather.tips)
        bot.send_message(message.chat.id, '要注意身体哦~')
        close_menu(message)
    elif message.text == '明天天气':
        bot.send_message(message.chat.id, '有备无患嘛~')
        bot.send_message(message.chat.id, weather.Weather.tomorrow)
        close_menu(message)
    else:
        bot.send_message(message.chat.id, '下次见~')
        close_menu(message)


# 输出键盘按键
@bot.message_handler(commands=['lesson'])
def send_a_reply(message):
    markup = types.InlineKeyboardMarkup()
    item_ssr = types.InlineKeyboardButton('ssr', url='https://docs.nameless13.com/winssr')
    item_clash = types.InlineKeyboardButton('clashr订阅', url='https://docs.nameless13.com/ios')
    item_shadowrocket = types.InlineKeyboardButton('小火箭', url='https://acl4ssr.netlify.com/')
    item_clash2 = types.InlineKeyboardButton('clash教程', url='https://avimitin.com/index.php/system/clash.html')
    markup.add(item_ssr, item_clash, item_shadowrocket, item_clash2)
    bot.send_message(message.chat.id, "请选择一个教程", reply_markup=markup)


# 轮询
bot.polling()
