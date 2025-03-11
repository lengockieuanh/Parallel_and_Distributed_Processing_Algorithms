from concurrent.futures import ThreadPoolExecutor
import time
import threading
from multiprocessing import Process

matrix = [i for i in range(1, 10)]


def compute_prefix(arr):    
    prefix_sum = [arr[0]]
    for i in range(1, len(arr)):
        prefix_sum.append(prefix_sum[i - 1] + arr[i])
    return prefix_sum

def parallel_prefix_sum(matrix_a):
    n = len(matrix_a)
    mid = n // 2
    
    left_half = matrix_a[:mid]
    right_half = matrix_a[mid:]
    
    with ThreadPoolExecutor(max_workers=2) as executor:        
        left_future = executor.submit(compute_prefix, left_half)
        right_future = executor.submit(compute_prefix, right_half)
        
        left_prefix = left_future.result()
        right_prefix = right_future.result()
    
    total_left = left_prefix[-1]
    right_prefix = [x + total_left for x in right_prefix]
    
    return left_prefix + right_prefix

def single_threaded():
    start = time.time()
    result = parallel_prefix_sum(matrix)    
    end = time.time()
    print("Matrix = ",matrix)
    print("PrefixSum = ",result)
    print("Thời gian chạy đơn luồng:", end - start)

def multi_threaded():
    start = time.time()
    threads = []
    for _ in range(4):  # Tối đa 4 luồng
        thread = threading.Thread(target=parallel_prefix_sum, args=(matrix,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    end = time.time()
    print("Thời gian chạy đa luồng:", end - start)

# Chạy chế độ đa tiến trình với tối đa 4 tiến trình
def multi_process():
    start = time.time()
    processes = []
    for _ in range(4):  # Tối đa 4 tiến trình
        process = Process(target=parallel_prefix_sum, args=(matrix,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
    end = time.time()
    print("Thời gian chạy đa tiến trình:", end - start)

# Đảm bảo rằng mã được chạy trong khối if __name__ == '__main__':
if __name__ == '__main__':        
    single_threaded()
    multi_threaded()
    multi_process()

