# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/4/9 15:59
import yaml
import re

with open("Reply.yml", 'r', encoding="UTF-8") as reply_msg_file:
    reply_msg_dic = yaml.load(reply_msg_file, Loader=yaml.FullLoader)


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