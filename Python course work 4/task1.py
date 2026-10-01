import numpy as np

## Numpy array creation and manipulation
def create1DArr(start,end,size):
    return np.random.randint(start,end,size)

def create2DArr():
    return np.random.randint(-10,10,(3,4))
def flattenArr(b):
    return b.flatten()
def create_arr_c(a):
    return a[::2]

## array slicing and indexing 
def get_third_element(a):
    return a[2]


def get_last_element_b(b):
    return b[-1, -1]


def get_first_two_rows_last_two_columns(b):
    return b[:2, -2:]


def get_second_row(b):
    return b[1]


def get_first_column(b):
    
    return b[:, 0]

## 3: Numpy array operations 
def create_array_d():
    return np.arange(1, 11)


def add_arrays(a, d):
    return a + d


def double_array_b(b):
    return b * 2


def matrix_multiplication(b, b_double):
    return b @ b_double.T


def calculate_means(a, b, b_double):
    return np.array([
        np.mean(a),
        np.mean(b),
        np.mean(b_double)
    ])
## numpy array aggregation
def sum_of_a(a):
    return np.sum(a)
def min_in_b(b):
    return np.min(b)
def max_in_b_double(b_double):
    return np.max(b_double)
if __name__=='__main__':
    a = create1DArr(1,100,10)
    b= create2DArr()
    b_flat = flattenArr(b) 
    a_copy = a.copy()
    a_copy[0] =-1
    c = create_arr_c(a)
    
    print("1.1 a:",a)
    print("1.2 b:",b)
    print("1.3 b flat : ",b_flat)
    print("1.4 acopy : " ,a_copy)
    print("1.5 c: ",c)
    
    #2: Numpy array indexing and slicing 
    
    third_element = get_third_element(a)
    last_element = get_last_element_b(b)
    selected_part = get_first_two_rows_last_two_columns(b)
    b_row = get_second_row(b)
    b_col = get_first_column(b)
    print("\n2.1 Third element of a:", third_element)
    print("2.2 Last element of b:", last_element)
    print("2.3 First two rows and last two columns of b:")
    print(selected_part)
    print("2.4 Second row of b:", b_row)
    print("2.5 First column of b:", b_col)
    
    ##3: Numpy array operations 
    d = create_array_d()
    e = add_arrays(a, d)
    b_double = double_array_b(b)
    f = matrix_multiplication(b, b_double)
    g = calculate_means(a, b, b_double)

    print("\n3.1 Array d:", d)
    print("3.2 Array e:", e)
    print("3.3 b_double:\n", b_double)
    print("3.4 Matrix multiplication f:")
    print(f)
    print("3.5 Means [a, b, b_double]:", g)
    
    ## numpy array aggregation
    a_sum = sum_of_a(a)
    b_min = min_in_b(b)
    b_double_max = max_in_b_double(b_double)
    print("4.1 sum of every element of a =",a_sum)
    print("4.2 minimum element in b=",b_min)
    print("4.3 Maximum in b_double=",b_double_max)
    