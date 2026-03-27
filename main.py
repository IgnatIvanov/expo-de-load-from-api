import os
import time
import math
import json
import queue
# import asyncio
import requests
from typing import List
from dotenv import load_dotenv

from data_combine import combine_pages
from load_data import DownloadThread

load_dotenv()
THREADS_COUNT = int(os.getenv('THREADS_COUNT', 1))
BASE_URL = str(os.getenv('BASE_URL', ''))
SAVE_DIR = os.path.join(
    '.',
    'pages'
)



def main():
    q = queue.Queue()
    threads: List[DownloadThread] = []
    for i in range(THREADS_COUNT):
        threads.append(
            DownloadThread(
                queue=q,
                name=f'Thread {i + 1}',
                save_dir=SAVE_DIR,
                base_url=BASE_URL,
            )
        )

    for t in threads:
        t.daemon = True
        t.start()

    
    page_id = 1
    resp = requests.get(
        url=BASE_URL,
        params={
            'page': 1
        }
    )
    data = resp.json()
    last_id = math.ceil(data['totalEntries']/data['per_page'])

    while page_id <= last_id:
        q.put(page_id)
        page_id += 1

    q.join()
    combine_pages(
        pages_dir=SAVE_DIR
    )


if __name__ == '__main__':
    main()
