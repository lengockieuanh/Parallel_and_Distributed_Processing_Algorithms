import random
import time
import threading
from multiprocessing import Process, cpu_count

# Hàm tạo ma trận ngẫu nhiên
def generate_random_matrix(n):
    return [[random.randint(0, 5) for _ in range(n)] for _ in range(n)]

# Hàm nhân ma trận song song
def parallel_multiply_matrices(matrix_a, matrix_b):
    # Các hàm bổ trợ để đệm và bỏ đệm ma trận
    def pad_matrix(matrix, new_size):    
        padded_matrix = [[0] * new_size for _ in range(new_size)]
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                padded_matrix[i][j] = matrix[i][j]
        return padded_matrix

    def unpad_matrix(matrix, original_size):    
        return [row[:original_size] for row in matrix[:original_size]]

    n = len(matrix_a)    
    m = 1
    while m < n:
        m *= 2

    padded_a = pad_matrix(matrix_a, m)
    padded_b = pad_matrix(matrix_b, m)

    # Hàm nhân ma trận đơn giản
    def multiply(matrix_a, matrix_b):
        n = len(matrix_a)
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += matrix_a[i][k] * matrix_b[k][j]
        return result

    # Hàm cộng hai ma trận
    def add(matrix_a, matrix_b):
        n = len(matrix_a)
        return [[matrix_a[i][j] + matrix_b[i][j] for j in range(n)] for i in range(n)]

    if m == 1:
        return [[padded_a[0][0] * padded_b[0][0]]]

    mid = m // 2    
    A11 = [row[:mid] for row in padded_a[:mid]]
    A12 = [row[mid:] for row in padded_a[:mid]]
    A21 = [row[:mid] for row in padded_a[mid:]]
    A22 = [row[mid:] for row in padded_a[mid:]]
    
    B11 = [row[:mid] for row in padded_b[:mid]]
    B12 = [row[mid:] for row in padded_b[:mid]]
    B21 = [row[:mid] for row in padded_b[mid:]]
    B22 = [row[mid:] for row in padded_b[mid:]]

    # Tính các khối ma trận kết quả
    C11 = add(multiply(A11, B11), multiply(A12, B21))
    C12 = add(multiply(A11, B12), multiply(A12, B22))
    C21 = add(multiply(A21, B11), multiply(A22, B21))
    C22 = add(multiply(A21, B12), multiply(A22, B22))
    
    result = []
    for i in range(mid):
        result.append(C11[i] + C12[i])
    for i in range(mid):
        result.append(C21[i] + C22[i])

    return unpad_matrix(result, n)

# Hàm in ma trận
def print_matrix(matrix, name):
    print(f"{name}:")
    for row in matrix:
        print(row)
    print()  # Dòng trống để ngăn cách giữa các ma trận

# Hàm đo thời gian chạy đơn luồng và in kết quả
def single_threaded(matrix_a, matrix_b):
    start = time.time()
    result = parallel_multiply_matrices(matrix_a, matrix_b)
    end = time.time()
    print("Thời gian chạy đơn luồng:", end - start)
    print_matrix(matrix_a, "Matrix A")
    print_matrix(matrix_b, "Matrix B")
    print_matrix(result, "Matrix C (Result)")
    return result

# Hàm đo thời gian chạy đa luồng (4 luồng)
def multi_threaded(matrix_a, matrix_b):
    start = time.time()
    threads = []
    for _ in range(4):  # Tối đa 4 luồng
        thread = threading.Thread(target=parallel_multiply_matrices, args=(matrix_a, matrix_b))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    end = time.time()
    print("Thời gian chạy đa luồng:", end - start)

# Hàm đo thời gian chạy đa tiến trình (4 tiến trình)
def multi_process(matrix_a, matrix_b):
    start = time.time()
    processes = []
    for _ in range(4):  # Tối đa 4 tiến trình
        process = Process(target=parallel_multiply_matrices, args=(matrix_a, matrix_b))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    end = time.time()
    print("Thời gian chạy đa tiến trình:", end - start)

# Đảm bảo rằng mã được chạy trong khối if __name__ == '__main__':
if __name__ == '__main__':
    n = int(input("Nhập kích thước n của ma trận vuông: "))
    A = generate_random_matrix(n)
    B = generate_random_matrix(n)
    
    print("Kết quả đơn luồng:")
    single_threaded(A, B)
    
    print("\nKết quả đa luồng:")
    multi_threaded(A, B)
    
    print("\nKết quả đa tiến trình:")
    multi_process(A, B)
