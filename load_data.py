import os
import json
import time
import queue
import requests
# from collections.abc import Callable
from threading import Thread
# from typing import Any, Iterable, Mapping



class DownloadThread(Thread):
    def __init__(
        self, 
        queue: queue.Queue, 
        name: str, 
        save_dir: str, 
        base_url: str,
    ) -> None:
        super().__init__()
        self.queue = queue
        self.name = name
        self.save_dir = save_dir
        self.base_url = base_url

    def run(self):
        while True:
            page_id = self.queue.get()
            save_path = os.path.join(
                self.save_dir,
                f'{page_id}.json'
            )

            if os.path.exists(save_path):
                # Если страницу уже скачивали,
                # то загружаем следующую
                print(f'INFO: Page {page_id} loaded already')
                self.queue.task_done()
                continue

            # Загрузка данных
            resp = requests.get(
                url=self.base_url,
                params={
                    'page': page_id
                }
            )

            if resp.status_code != 200:
                print(f'ERROR: Loading page {page_id} finished with code {resp.status_code}')
                time.sleep(60*3)
                self.queue.task_done()
                continue
            else:
                with open(save_path, 'w', encoding='utf8') as f:
                    json.dump(
                        resp.json()['items'],
                        f,
                        ensure_ascii=False,
                        indent=4,
                    )
            print(f'SUCCESS: Loading page {page_id} finished with code {resp.status_code}')
            self.queue.task_done()
