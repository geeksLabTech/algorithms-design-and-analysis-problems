from utils import is_adyacent_valid

all_subarr = []

def check(arr: list[int], indexes: list[int]):
    # print(arr,'arr')
    # print(indexes,'iii')
    for i in range(len(indexes)-1):
        # print(arr[i+1],'sss')
        if not is_adyacent_valid(arr[indexes[i]],arr[indexes[i+1]],7):
            # print(arr[i],arr[i+1], 'false')
            return False
    return True


def allSubsequences(arr: list[int], index: int, subarr: list[int]):
    if index == len(arr):
        if len(subarr) != 0:
            return subarr

    else:
        subarr1 = allSubsequences(arr, index + 1, subarr)
        # print(subarr1,'subsequence 1')
        if subarr1 and check(arr, subarr1):
            all_subarr.append(subarr1)
        subarr2 = allSubsequences(arr, index + 1,subarr+[index])
        # print(subarr2,'subsequence 2')
        if subarr2 and check(arr, subarr2):
            all_subarr.append(subarr2)
    # all_subarr.clear()
    

  
# arr = [1,3,4,8,5,10,5,78,4,2]
# allSubsequences(arr, 0, [])
# print(all_subarr,'aaa')

def choose_longest(arr_l: list[int]):
    max_len = 0
    bests = []
    for i, num_1 in enumerate(arr_l):
        for j, num_2 in enumerate(arr_l):
            for k, num_3 in enumerate(arr_l):
                for l, num_4 in enumerate(arr_l):
                    if len(set([i, j, k, l])) == 4:
                        if len(set(num_1+num_2+num_3+num_4)) == len(num_1+num_2+num_3+num_4):
                            if len(num_1+num_2+num_3+num_4) > max_len:
                                max_len = len(num_1+num_2+num_3+num_4)
                                bests = [num_1, num_2, num_3, num_4]
    # arr.clear()
    return max_len, bests


# print(choose_longest(all_subarr))

def execute_brute_force(array):
    
    all_subarr.clear()
    allSubsequences(array, 0, [])
    solve = choose_longest(all_subarr)
    # print(all_subarr,'all')
    all_subarr.clear()
    # print(all_subarr,'before')
    return solve

# print(execute_brute_force([7,34,16,19,47]))
# print(execute_brute_force([1,3,4,8,5,10,5,78,4,13]))






