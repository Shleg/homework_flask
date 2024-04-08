import random
import time
import threading
import multiprocessing
import asyncio


def generate_array(size):
    return [random.randint(1, 100) for _ in range(size)]


def sum_array(arr):
    return sum(arr)


def sum_with_threads(arr):
    start_time = time.time()
    threads = []
    chunk_size = len(arr) // 4
    results = []

    for i in range(4):
        thread = threading.Thread(target=partial_sum, args=(arr[i * chunk_size:(i + 1) * chunk_size], results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    result = sum(results)
    print(f'Sum with threads: {result}, Time: {time.time() - start_time:.4f} seconds')


def sum_with_processes(arr):
    global chunks
    start_time = time.time()
    pool = multiprocessing.Pool(processes=4)

    results = pool.map(sum_array, chunks)
    pool.close()
    pool.join()
    result = sum(results)
    print(f'Sum with processes: {result}, Time: {time.time() - start_time:.4f} seconds')


async def sum_with_asyncio(arr):
    global chunks
    start_time = time.time()
    results = await asyncio.gather(*(async_sum_array(chunk) for chunk in chunks))
    result = sum(results)
    print(f'Sum with asyncio: {result}, Time: {time.time() - start_time:.4f} seconds')


async def async_sum_array(arr):
    return sum(arr)


def partial_sum(arr, results):
    results.append(sum(arr))


if __name__ == '__main__':
    arr = generate_array(1000000)
    chunks = [arr[i * len(arr) // 4:(i + 1) * len(arr) // 4] for i in range(4)]
    sum_with_threads(arr)
    sum_with_processes(arr)
    asyncio.run(sum_with_asyncio(arr))
