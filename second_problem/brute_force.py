

all_subarr = []

def check(arr : list[int]):
    for i in range(len(arr)-1):
        if abs(arr[i] - arr[i+1]) != 1 or 7%(arr[i] - arr[i+1]) != 0:
            return False
    return True

def allSubsequences(arr:list[int], index : int, subarr:list[int]):

    if index == len(arr):    
        if len(subarr) != 0:
            return subarr
       
    else:
        subarr1 = allSubsequences(arr, index + 1, subarr)
        if subarr1 and check(subarr1):
            all_subarr.append(subarr1)
        subarr2 = allSubsequences(arr, index + 1, 
                            subarr+[arr[index]])
        if subarr2 and check(subarr2):
            all_subarr.append(subarr2)
       
    return      
arr = [1, 2, 4]
allSubsequences(arr, 0, [])
print(all_subarr,'aaa')

