import random
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import multiprocessing as mp

# Tạo một ma trận vuông ngẫu nhiên kích thước n x n với các phần tử là số nguyên ngẫu nhiên trong khoảng từ 0 đến 10.
def generate_random_matrix(n):
    return [[random.randint(0, 10) for x in range(n)] for x in range(n)]

# Hàm cộng hai ma trận có cùng kích thước
def add(matrix_a, matrix_b):
    n = len(matrix_a)
    return [[matrix_a[i][j] + matrix_b[i][j] for j in range(n)] for i in range(n)]

# Hàm đệm thêm số 0 vào ma trận để tăng kích thước thành new_size x new_size sao cho phù hợp với lũy thừa của 2.
def pad_matrix(matrix, new_size):    
    padded_matrix = [[0] * new_size for x in range(new_size)]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            padded_matrix[i][j] = matrix[i][j]
    return padded_matrix

# Đưa ma trận về kích thước ban đầu sau khi tính toán xong.
def unpad_matrix(matrix, original_size):
    return [row[:original_size] for row in matrix[:original_size]]

# Hàm nhân ma trận đệ quy với song song
def matrixMultiply(A, B, threshold=64):
    n = len(A)
    
    # Trường hợp cơ sở: nhân ma trận trực tiếp nếu nhỏ hơn ngưỡng (n=1)
    if n <= threshold:
        return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

    # Phân chia các ma trận con 
    mid = n // 2
    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]
    
    B11 = [row[:mid] for row in B[:mid]]
    B12 = [row[mid:] for row in B[:mid]]
    B21 = [row[:mid] for row in B[mid:]]
    B22 = [row[mid:] for row in B[mid:]]
    
    # Chạy các phép nhân song song với multi-threading hoặc multi-processing, sử dụng ProcessPoolExecutor để song song hóa các phép tính nhân các ma trận con. 
    return multiply_recursive(A11, A12, A21, A22, B11, B12, B21, B22)

def multiply_recursive(A11, A12, A21, A22, B11, B12, B21, B22):
    # Multi-process với ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=4) as executor:
        # Khởi tạo các phép nhân ma trận con
        M1_future = executor.submit(matrixMultiply, A11, B11)
        M2_future = executor.submit(matrixMultiply, A12, B21)
        M3_future = executor.submit(matrixMultiply, A11, B12)
        M4_future = executor.submit(matrixMultiply, A12, B22)
        M5_future = executor.submit(matrixMultiply, A21, B11)
        M6_future = executor.submit(matrixMultiply, A22, B21)
        M7_future = executor.submit(matrixMultiply, A21, B12)
        M8_future = executor.submit(matrixMultiply, A22, B22)

        # Đợi kết quả và cộng các ma trận tương ứng
        M1 = M1_future.result()
        M2 = M2_future.result()
        M3 = M3_future.result()
        M4 = M4_future.result()
        M5 = M5_future.result()
        M6 = M6_future.result()
        M7 = M7_future.result()
        M8 = M8_future.result()

        # Tính toán ma trận C con
        C11 = add(M1, M2)
        C12 = add(M3, M4)
        C21 = add(M5, M6)
        C22 = add(M7, M8)

    # Kết quả của mỗi phép nhân con được ghép lại thành bốn ma trận con C11, C12, C21, C22 và kết hợp chúng thành ma trận lớn.
    C = []
    for i in range(len(C11)):
        C.append(C11[i] + C12[i])
    for i in range(len(C21)):
        C.append(C21[i] + C22[i])
    return C

def parallel_multiply_matrices(matrix_a, matrix_b):
    # Kích thước ban đầu của ma trận
    n = len(matrix_a)

    # Tìm kích thước lũy thừa của 2 gần nhất lớn hơn hoặc bằng kích thước ma trận gốc
    m = 1
    while m < n:
        m *= 2

    # Đệm ma trận theo m
    padded_a = pad_matrix(matrix_a, m)
    padded_b = pad_matrix(matrix_b, m)
        
    padded_result = matrixMultiply(padded_a, padded_b)
    return unpad_matrix(padded_result, n)

# Tính toán thời gian
def measure_time(mode, matrix_a, matrix_b):
    start_time = time.time()
    
    if mode == 'single':
        parallel_multiply_matrices(matrix_a, matrix_b)
    elif mode == 'multi_process':
        with ProcessPoolExecutor(max_workers=4) as executor:
            parallel_multiply_matrices(matrix_a, matrix_b)
    elif mode == 'multi_thread':
        with ThreadPoolExecutor(max_workers=4) as executor:
            parallel_multiply_matrices(matrix_a, matrix_b)
    
    end_time = time.time() 
    return end_time - start_time

def print_matrix(matrix):
    """Hàm in kết quả ma trận"""
    for row in matrix:
        print(row)

if __name__ == '__main__':    
    mp.set_start_method('spawn', force=True)

    # Kích thước ma trận
    n = 300
    A = generate_random_matrix(n)
    B = generate_random_matrix(n)
    C = parallel_multiply_matrices(A, B)        
    
    print("Matrix A:")
    print_matrix(A)
    
    print("\nMatrix B:")
    print_matrix(B)

    print("\nMatrix C:")
    print_matrix(C)

    modes = ['single', 'multi_process', 'multi_thread']
    
    for mode in modes:
        time_taken = measure_time(mode, A, B)
        print(f"\nTime taken in {mode} mode: {time_taken:.6f} seconds")
