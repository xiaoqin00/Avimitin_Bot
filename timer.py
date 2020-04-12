# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/4/10 15:04
import telebot
import yaml
from telebot import types
import time

with open('config.yaml', 'r+', encoding='UTF-*') as token_file:
    token_dic = yaml.load(token_file, Loader=yaml.FullLoader)
bot = telebot.TeleBot(token=token_dic['TOKEN'])


@bot.message_handler(commands=['timer'])
def get_time(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    itembtn30 = types.KeyboardButton('5秒')
    itembtn1 = types.KeyboardButton('1分钟')
    itembtn2 = types.KeyboardButton('2分钟')
    itembtn5 = types.KeyboardButton('5分钟')
    itembtncancel = types.KeyboardButton('取消定时')

    markup.row(itembtn30, itembtn1)
    markup.row(itembtn2, itembtn5)
    markup.row(itembtncancel)

    bot.send_message(message.chat.id, "选择要定的时间：", reply_markup=markup)
    bot.register_next_step_handler(message, timer_set)


def timer_set(message):

    if message.text == "5秒" or message.text == "1分钟" or message.text == "2分钟" or message.text == "5分钟":
        bot.send_message(message.chat.id, "成功定时" + message.text + "！")
    elif message.text == "取消定时":
        bot.send_message(message.chat.id, "定时取消！")
    else:
        bot.send_message(message.chat.id, "参数错误！")

    if message.text == "5秒":
        time.sleep(5)
        print('yes123')
        bot.register_next_step_handler(message, test)
    elif message.text == "1分钟":
        time.sleep(60)
        bot.send_message(message.chat.id, "1分钟到了！")
    elif message.text == "2分钟":
        time.sleep(120)
        bot.send_message(message.chat.id, "2分钟到了！")
    elif message.text == "5分钟":
        time.sleep(300)
        bot.send_message(message.chat.id, "5分钟到了！")


def test(message):
    print('yes')
    bot.send_message(message.chat.id, "30秒到了！")


bot.polling()
