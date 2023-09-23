def descending_sort(arr):
    n = len(arr)
    for i in range(n):
        print(i,"ラウンド")
        for j in range(0, n-i-1):
            if arr[j] < arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
        print(arr)

my_list = [3, 1, 4, 5 ,2 ,8 ]#結果 5,4,3,1 
descending_sort(my_list)
print("結果",my_list)