# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/4/27

import requests

response = requests.get('https://kctbh9vrtdwd.statuspage.io/api/v2/summary.json')

def get_status():
    last_update_time = response.json()['page']['updated_at']
    indicator = response.json()['status']['indicator']
    description = response.json()['status']['description']
    try:
        incident = response.json()['incidents'][0]['incident_updates'][0]['body']
        text = 'Github目前的警报为：{}，\n目前的状态为:{}'\
            '{}出现了故障：\n{}'.format(indicator,description,last_update_time,incident)
        return text
    except IndexError:
        text = 'Github目前的警报为：{}，\n目前的状态为:{}'.format(indicator,description)
        return text


if __name__ == '__main__':
    print(get_status())
