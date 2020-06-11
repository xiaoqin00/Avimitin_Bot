# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/4/9 15:59
import yaml
import re


class Msg:

    def __init__(self):
        self.keyword = ''

        with open("./config/Reply.yml", 'r', encoding="UTF-8") as reply_msg_file:
            self.reply_msg_dic = yaml.load(reply_msg_file, Loader=yaml.FullLoader)

        self.reply_msg_keywords_list = list(self.reply_msg_dic.keys())

    # 正则搜索
    def msg_match(self, lines):
        self.__init__()
        # 计算回复的关键词字数
        for keyword in self.reply_msg_keywords_list:
            msg_keywords_match = re.match(r'(.*)%s(.*)' % keyword, str(lines))
            if msg_keywords_match:
                self.keyword = keyword
                return True
            else:
                pass
