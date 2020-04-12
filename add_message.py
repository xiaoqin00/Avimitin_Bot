# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/4/9 16:33
import yaml


class BotsKeyword:
    keyword = ""
    value_word = ""

    @staticmethod
    def change_keyword(words):
        BotsKeyword.keyword = words

    @staticmethod
    def change_value(value_words):
        BotsKeyword.value_word = value_words

    @staticmethod
    def get_keyword():
        return BotsKeyword.keyword

    @staticmethod
    def get_value_word():
        return BotsKeyword.value_word

    @staticmethod
    def set_value():
        keyword = BotsKeyword.keyword
        value_word = BotsKeyword.value_word
        with open('Reply.yml', 'a+', encoding='UTF-8') as reply_msg_file:
            reply_msg_dic = {keyword: value_word}
            reply_msg_file.write('\n')
            yaml.dump(reply_msg_dic, reply_msg_file, encoding='UTF-8', allow_unicode=True)
