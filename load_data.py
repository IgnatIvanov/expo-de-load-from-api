import os
import json
import queue
import requests
from collections.abc import Callable
from threading import Thread
from typing import Any, Iterable, Mapping



class DownloadThread(Thread):
    def __init__(self, queue, name, save_dir, base_url) -> None:
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

            # Загрузка данных
            resp = requests.get(
                url=self.base_url,
                params={
                    'page': page_id
                }
            )
            resp.raise_for_status()

            if resp.status_code != 200:
                print(f'Loading page {page_id} finished with code {resp.status_code}')
            else:
                # data = resp.json()
                with open(save_path, 'w', encoding='utf8') as f:
                    json.dump(
                        resp.json()['items'],
                        f,
                        ensure_ascii=False,
                        indent=4,
                    )
            self.queue.task_done()
