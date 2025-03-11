import time
import threading
from multiprocessing import Process

matrix = [i for i in range(1, 1000)] 

def parallel_prefix_sum(matrix_a):     
    #Quy hoach dong 
    def parallel_left_sum(l):
        n = len(l)
        mid = n // 2
        leftPrefix = []
        rightPrefix = []
        leftPrefix.append(l[0])
        for i in range(1, mid):
            leftPrefix.append(leftPrefix[i - 1] + l[i])
        rightPrefix.append(l[mid])
        for i in range(1, n - mid):
            rightPrefix.append(rightPrefix[i - 1] + l[mid + i])
        totalLeft = leftPrefix[-1]
        rightPrefix = [x + totalLeft for x in rightPrefix]
        return leftPrefix + rightPrefix
    #De quy song song
    def parallel_right_sum(r):
        if len(r) == 1:
            return [r[0]]
        mid = len(r) // 2
        leftPrefix = parallel_right_sum(r[:mid])
        rightPrefix = parallel_right_sum(r[mid:])
        totalLeft = leftPrefix[-1]
        rightPrefix = [totalLeft + x for x in rightPrefix]        
        return leftPrefix + rightPrefix
    
    mid = len(matrix_a) // 2
    leftPrefix_sum = parallel_left_sum(matrix_a[:mid])
    rightPrefix_sum = parallel_right_sum(matrix_a[mid:])
    totalLeft = leftPrefix_sum[-1]  
    rightPrefix_sum = [totalLeft + x for x in rightPrefix_sum]
    return leftPrefix_sum + rightPrefix_sum

# Chạy chế độ đơn luồng
def single_threaded():
    start = time.time()
    result = parallel_prefix_sum(matrix)    
    end = time.time()
    print("Matrix = ",matrix)
    print("PrefixSum = ",result)
    print("Thời gian chạy đơn luồng:", end - start)

# Chạy chế độ đa luồng với tối đa 4 luồng
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
    #print(parallel_prefix_sum108(matrix))
    single_threaded()
    multi_threaded()
    multi_process()
