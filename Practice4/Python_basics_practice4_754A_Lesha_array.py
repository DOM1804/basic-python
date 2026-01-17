#https://codeforces.com/contest/754/problem/A
'''
ЛЕША И РАЗБИЕНИЕ МАССИВА
1. если в массиве все нули, то разбить не получится (NO)
2. в остальных случаях разбиение возможно по ненулевым элементам
'''
n = int(input()) #число элементов в массиве
arr_ini= list(map(int, input().split()))

#если все элементы нули
if all(x == 0 for x in arr_ini): 
    print("NO")
    
else: #если не все элементы нули
    #список для записи индексов сегментов разбиения
    segment_indices_lst = []
    
    #ищем первый ненулевой элемент и создаем разбиение по нему (включительно)
    first_nonzero_idx = 0
    while arr_ini[first_nonzero_idx] == 0:
        first_nonzero_idx += 1   
    segment_indices_lst.append((0, first_nonzero_idx))

    #ищем следующий ненулевой элемент, если есть
    next_nonzero_idx = first_nonzero_idx + 1
    while next_nonzero_idx < n:
        if arr_ini[next_nonzero_idx] != 0:
            segment_indices_lst.append((next_nonzero_idx, next_nonzero_idx))
            next_nonzero_idx += 1
        else:
            #увеличиваем индекс конечного элемента в предшествующем сегменте, если есть нулевые элементы после него
            last_l, last_r = segment_indices_lst[-1]
            segment_indices_lst[-1] = (last_l, last_r + 1)
            next_nonzero_idx += 1
            
    print("YES")
    print(len(segment_indices_lst))
    for l, r in segment_indices_lst:
        print(l + 1, r + 1)
