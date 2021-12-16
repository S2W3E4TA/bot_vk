import vk_api as vk
import asyncio
import random
import time, datetime
import requests
from vk_api.longpoll import VkLongPoll, VkEventType
token='7455b59111ad6186ff1e6dff27a25b49bef7da1638e0b486a95c1580f3600a2b3b3ff65e2f8b6eaef8cc9'

vk_session = vk.VkApi(token=token)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
time_reminder = datetime.datetime.now()
time_now = time_reminder.replace(hour = 20, minute = 16)

longpoll = VkLongPoll(vk_session)
days_week = ['понедельник','вторник', 'среда', 'четверг', 'пятница']



async def weather():
    url='https://wttr.in/'# get post, delete, put, patch
    weather_parametrs={
        'format':2,
        '0':'',
        'M':''
        }
    response = requests.get(url, params=weather_parametrs)
    print(response.text)
    return response.text
days_week = ['понедельник','вторник', 'среда', 'четверг', 'пятница']
async def time_table(day_week):
    answer = open(f'{day_week}.txt','r')
    answer = answer.read()
    return answer

async def to_count_dis(a, b, c):
    d = (b**2)-4*a*c
    if d > 0:
        x1 = ((-b + math.sqrt(d))/(2*a))
        x2 = ((-b - math.sqrt(d))/(2*a))
        return x1, x2
    elif d == 0:
        x = (-b)/(2*a)
        return x
    else:
        return'нет корней'
        
async def start_bot():
    for event in longpoll.listen():
        time_now = datetime.datetime.now()
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:           
            if event.from_user:
                message = event.text
                if message.lower() == 'погода':
                    task = asyncio.create_task(weather())
                    answer_weather = await task
                    vk.messages.send(user_id=event.user_id, message=answer_weather, random_id = random.randint(1,100000))
                if message.split()[0].lower() == 'дискриминант':
                    task = asyncio.create_task(to_count_dis(message.split()[1], message.split()[2], message.split()[3])())
                    result = await task
                    vk.messages.send(user_id=event.user_id, message=result, random_id = random.randint(1,100000))
                for i in days_week:
                    if i == message.lower():
                        task = asyncio.create_task(time_table(i))
                        result = await task
                        print(result)
                        vk.messages.send(user_id=event.user_id, message=result, random_id = random.randint(1,100000))
if __name__ == '__main__':
    asyncio.run(start_bot())


