# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/4/9 15:59
import yaml
import re


class Msg:

    def __init__(self):
        self.count = 0
        
        with open("config/Reply.yml", 'r', encoding="UTF-8") as reply_msg_file:
            self.reply_msg_dic = yaml.load(reply_msg_file, Loader=yaml.FullLoader)

        self.reply_msg_list = list(self.reply_msg_dic.keys())

    # 正则搜索
    def msg_match(self, lines):
        self.__init__()
        # 计算回复的关键词字数
        count = len(self.reply_msg_list)-1
        # 关键词从列表最后一个开始匹配
        while count >= 0:
            keywords = self.reply_msg_list[count]
            msg_keywords_match = re.match(r'(.*)%s(.*)' % keywords, str(lines))
            if msg_keywords_match:
                self.count = count
                return True
            else:
                count -= 1
