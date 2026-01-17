#https://codeforces.com/contest/1811/problem/A
'''
ВСТАВЬ ЧИСЛО
Если цифра > 0, ставим её перед первой цифрой числа, которая МЕНЬШЕ вставляемой.
Если все цифры числа БОЛЬШЕ или равны вставляемой, то вставляем цифру в конец
'''
t = int(input()) #количество наборов данных

for _ in range(t):
    n, d = input().split() #количество цифр в числе и новая цифра
    n = int(n)
    number = input() #исходное число в виде строки
    for idx in range(n):
        if number[idx] < d:
            print(number[:idx] + d + number[idx:])
            break
    else:
        print(number + d)
        



