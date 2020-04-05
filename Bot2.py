# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/3/29 13:58
import telebot
from config import TOKEN2
bot = telebot.TeleBot(TOKEN2)

@bot.message_handler(commands=['start'])
def sendMessage(message):
    bot.send_message(message.chat.id,\
                     'TG目前会Spam部分+86账号，请使用我跟老板聊天。\n'\
                     +'同时希望您询问的问题能用一个聊天框全部说完，提高效率。\n'\
                     +'其次谷歌可以搜出来的问题老板是不会回复的，请自重。\n'\
                     +'最后希望我们都能愉快交流\n'\
                     +'使用 /aff 获取金属云注册链接，目前金属云年费8折活动正在进行')

@bot.message_handler(commands=['help'])
def sendMessage(message):
    bot.send_message(message.chat.id,'没有帮助菜单，我就是没有感情的转发机器')

@bot.message_handler(commands=['aff'])
def sendMessage(message):
    bot.send_message(message.chat.id,'http://ironcloud.pw/auth/register?code=dyEL')

@bot.message_handler(func=lambda message: True)
def forward_all(message):
	bot.forward_message('649191333',message.from_user.id,message.message_id)

bot.polling()
