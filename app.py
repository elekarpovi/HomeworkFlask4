# Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск. Каждое изображение 
# должно сохраняться в отдельном файле, название которого соответствует названию изображения в URL-адресе. Например, URL-адрес: 
# https://example/images/image1.jpg -> файл на диске: image1.jpg
# — Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
# — Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
# — Программа должна выводить в консоль информацию о времени скачивания каждого изображения и общем времени выполнения программы.


import asyncio
import aiohttp
import threading
import requests
import os
import time
from multiprocessing import Process

URLS = ['https://st3.depositphotos.com/1031062/14744/i/1600/depositphotos_147442255-stock-photo-cottage-cheese-pancakes-with-oats.jpg',
        'https://static5.depositphotos.com/1022214/518/i/450/depositphotos_5186192-stock-photo-gelatin.jpg',
        'https://www.vsegdavkusno.ru/assets/images/recipes/1380/draniki-old-1.jpg',
        'https://kartinki.pics/uploads/posts/2022-05/1652236313_1-kartinkin-net-p-kartinki-o-yede-1.jpg',
        'https://images.wallpaperscraft.ru/image/single/pitstsa_eda_bokal_73012_1920x1080.jpg',
        ]


def downloads():
    folder = 'picture_sync'
    if not os.path.exists(folder):
        os.mkdir(folder)
    for url in URLS:
        filename = os.path.join(folder, os.path.basename(url))
        download_data(url, filename)


def download_data(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)


async def async_download_data(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            pict = await response.read()
            with open(filename, 'wb') as f:
                f.write(pict)


if __name__ == '__main__':

    start_time = time.time()
    downloads()
    print(f'sync {time.time() - start_time:.2f}')

    threads = []
    start_time = time.time()
    folder = 'picture_thread'
    if not os.path.exists(folder):
        os.mkdir(folder)
    for url in URLS:
        filename = os.path.join(folder, os.path.basename(url))
        thread = threading.Thread(target=download_data, args=[url, filename])
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    print(f'threads {time.time() - start_time:.2f}')

    proces = []
    start_time = time.time()
    folder = 'picture_proc'
    if not os.path.exists(folder):
        os.mkdir(folder)
    for url in URLS:
        filename = os.path.join(folder, os.path.basename(url))
        proc = Process(target=download_data, args=[url, filename])
        proces.append(proc)
        proc.start()
    for proc in proces:
        proc.join()
    print(f'proc {time.time() - start_time:.2f}')

    tasks = []
    start_time = time.time()
    folder = 'picture_task'
    if not os.path.exists(folder):
        os.mkdir(folder)
    for url in URLS:
        filename = os.path.join(folder, os.path.basename(url))
        task = asyncio.ensure_future(async_download_data(url, filename))
        tasks.append(task)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    print(f'async {(time.time() - start_time):.2f}')


# sync 17.14
# threads 2.18
# proc 2.89
# async 1.99