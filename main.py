import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import sqlite3

import config


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': 0})


vk = vk_api.VkApi(token=config.TOKEN)
d = dict()
base = sqlite3.connect("answers.db")
cur = base.cursor()
base.execute('CREATE TABLE IF NOT EXISTS {}(key text, reply text)'.format('data'))
cur.execute('select key, reply from data')
result = cur.fetchall()
for key, reply in result:
    d[key] = reply
print("ok")

longpoll = VkLongPoll(vk)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text
            if request.lower() == "привет":
                write_msg(event.user_id, "Хай")
            elif request.lower() == "пока":
                write_msg(event.user_id, "Пока((")
            elif request[0] == "?":
                answer = request[1:].split("-&gt;")
                d[f'{answer[0]}'] = answer[1]
                cur.execute('INSERT INTO data VALUES (?, ?)', (answer[0].lower(), answer[1]))
                base.commit()
                write_msg(event.user_id, "Значения добавлены в словарь")
            elif request.lower() in d:
                write_msg(event.user_id, d[request.lower()])
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")
