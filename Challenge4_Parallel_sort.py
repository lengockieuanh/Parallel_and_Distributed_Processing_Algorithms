# Challenge 3: Viết hàm "parallel_sorting_descending (array_a)" trả về một array là sắp xếp theo thứ tự giảm dần. Thực hiện sắp xếp mảng này sử dụng lập trình song song.
# o Input: một mảng có kích thước 10^5
# o Output: một mảng đã được sắp xếp theo thứ tự giảm dần
# o Giới Hạn tối đa 4 Core
# Yêu cầu khác với lab 3: Đo và in ra thời gian cần thiết để thực hiện thuật toán sắp xếp
import random
import concurrent.futures

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
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:        
        left_future = executor.submit(compute_prefix, left_half)
        right_future = executor.submit(compute_prefix, right_half)
        
        left_prefix = left_future.result()
        right_prefix = right_future.result()
    
    total_left = left_prefix[-1]
    right_prefix = [x + total_left for x in right_prefix]
    
    return left_prefix + right_prefix

# Sắp xếp Counting dựa trên chữ số tại exp
def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10  # Mảng đếm cho các chữ số từ 0 đến 9

    # Đếm số lần xuất hiện của mỗi chữ số
    for i in arr:
        index = (i // exp) % 10
        count[index] += 1

    count = parallel_prefix_sum(count)

    # Sắp xếp theo chữ số hiện tại từ cuối mảng đầu vào
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]  # Chèn vào vị trí chính xác
        count[index] -= 1  # Giảm số lượng để xử lý các phần tử giống nhau

    # Sao chép kết quả đã sắp xếp vào mảng ban đầu
    for i in range(n):
        arr[i] = output[i]

def radix_sort(arr):
    if len(arr) == 0:
        return arr

    # Tìm giá trị lớn nhất để biết cần duyệt qua bao nhiêu chữ số
    max_num = max(arr)

    # Sắp xếp theo từng chữ số từ hàng đơn vị đến hàng cao nhất
    exp = 1
    while max_num // exp > 0:
        counting_sort(arr, exp)
        exp *= 10
    
    return arr[::-1]  # Đảo ngược để sắp xếp giảm dần

# Hợp nhất hai danh sách đã sắp xếp theo thứ tự giảm dần
def merge(left, right):
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] >= right[j]:  # Sắp xếp theo thứ tự giảm dần
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    
    merged.extend(left[i:])
    merged.extend(right[j:])
    
    return merged

# Radix Sort song song
def parallel_radix_sort(arr):
    if len(arr) == 0:
        return arr

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        left_sorted_future = executor.submit(radix_sort, left_half)
        right_sorted_future = executor.submit(radix_sort, right_half)

        left_sorted = left_sorted_future.result()
        right_sorted = right_sorted_future.result()

    # Hợp nhất hai nửa đã sắp xếp 
    return merge(left_sorted, right_sorted)

def quicksort(arr):    
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    
    # Phân vùng cho sắp xếp giảm dần
    left = []
    middle = []
    right = []
    
    for x in arr:
        if x < pivot:  # Giá trị nhỏ hơn pivot
            left.append(x)
        elif x == pivot:
            middle.append(x)
        else:
            right.append(x)  # Giá trị lớn hơn pivot

    return quicksort(right) + middle + quicksort(left)

# Sắp xếp song song cho dữ liệu lớn hơn một triệu phần tử
def parallel_sorting_descending(array_a):
    n = len(array_a)
    
    if n > 10**4:
        return parallel_radix_sort(array_a)
    
    elif n > 1000:
        chunk_size = n // 4
        chunks = [array_a[i:i + chunk_size] for i in range(0, n, chunk_size)]

        with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
            sorted_chunks = list(executor.map(radix_sort, chunks))

        # Hợp nhất các phần đã sắp xếp
        while len(sorted_chunks) > 1:
            sorted_chunks = [merge(sorted_chunks[i], sorted_chunks[i + 1]) for i in range(0, len(sorted_chunks) - 1, 2)]
        
        return sorted_chunks[0] if sorted_chunks else []

    else:  
        return quicksort(array_a)

# Các trường hợp kiểm tra để xác thực
def test_parallel_sorting():
    test_cases = [
        [],  
        [5],  
        [5, 5, 5],  
        [1, 2, 3, 4, 5],  
        [5, 4, 3, 2, 1],  
        [random.randint(1, 1000) for _ in range(1000)],
        [2] * 80 + [1] * 20 + [100] * 100 + [99] * 50 + [98] * 30 + [97] * 10,
        [random.randint(1, 1000) for _ in range(10**6)],  
        
    ]

    for i, case in enumerate(test_cases):
        print(f"Running Test case {i + 1}...")
        sorted_case = parallel_sorting_descending(case)
        
        # Kiểm tra xem kết quả có được sắp xếp theo thứ tự giảm dần không
        assert sorted_case == sorted(case, reverse=True), f"Test case {i + 1} failed!"
        
        print(f"Test case {i + 1}: PASSED")

if __name__ == "__main__":
    test_parallel_sorting()
