import os
import time
import math
import json
import asyncio
import requests

from data_combine import combine_pages

THREAD_COUNT = 1
BASE_URL = 'http://5.159.103.79:4000/api/v1/logs'
SAVE_DIR = os.path.join(
    '.',
    'pages'
)



def main():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    # Получение номера страницы, с которой начинаем скачивание
    # page_id = len(os.listdir(SAVE_DIR)) + 1
    page_id = 1
    last_id = page_id + 1


    # Сделать запросы
    while page_id <= last_id:
        save_path = os.path.join(
            SAVE_DIR,
            f'{page_id}.json'
        )
        if os.path.exists(save_path):
            # Если страницу уже скачивали,
            # то загружаем следующую
            page_id += 1
            continue
        # Загрузка данных
        resp = requests.get(
            url=BASE_URL,
            params={
                'page': page_id
            }
        )
        # Проверка на ошибку по превышению rate_limit
        if resp.status_code == 429: 
            time.sleep(60*3)
            continue
        
        data = resp.json()
        # Обновляем номер последней страницы
        last_id = math.ceil(data['totalEntries']/data['per_page'])
        # Сохранение данных
        with open(save_path, 'w', encoding='utf8') as f:
            json.dump(
                data['items'], 
                f, 
                ensure_ascii=False,
                indent=4,
            )

        print(f'Page loaded: {page_id}')
        page_id += 1
        # if page_id == 151: page_id = last_id + 1
    else:
        combine_pages(SAVE_DIR)

    # Если нет 429, то добавить один доп поток

    # Сохранить результаты

    # Если есть 429, то больше не добавляем потоков
    # Уменьшаем число потоков на 1
    # ждём 3 минуты


if __name__ == '__main__':
    main()
