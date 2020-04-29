# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/4/26 17:24
import re


def search_signal(lines):
    if re.match('\$', lines):
        return True
    else:
        return False


def change_word(lines):
    text = lines[1:]
    return text.replace("你", "我").replace("吗", "吧").replace("？", "！").replace("?", "!")


if __name__ == '__main__':
    sentence = input('输入一句话')
    print(search_signal(sentence))
    print(change_word(sentence))

