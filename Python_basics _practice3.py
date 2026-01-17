''' Задание 3: ЦИКЛЫ '''
import math
import builtins

"""
    Классы эквивалентности для validate_positive:
    1. валидные: положительные числа (включая дробные, с точкой/запятой)
    2. невалидные:
        2.1 ноль, 
        2.2 отрицательные числа
        2.3 нечисловые строки
        2.4 пустой ввод или только пробелы   
"""
def validate_positive (prompt: str) -> float:
    '''
    Функция осуществляет валидацию введенных пользователем значений.
    Если значение не прошло валидацию, запрашивается повторный ввод параметра.
    По получении корректного значения от пользователя, функция возвращает параметр в формате float
    '''
    while True:
        user_input = input(prompt)
        if not user_input or user_input.strip() == '':
            print('Ошибка: ввод не должен быть пустым, введите число.')
        try:
            value = float(user_input.replace(',', '.'))
            if value > 0:
                return value
            else:
                print('Ошибка: число должно быть положительным')
        except ValueError:
            print('Ошибка: обнаружены нечисловые символы, введите корректное число')

            
def take_input():
    '''
    Функция возвращает значения параметров, запрашиваемых у пользователя
    '''         
    d1 = validate_positive('Введите кратчайшее расстояние от спасателя до кромки воды d1 (в ярдах): ')      
    d2 = validate_positive('Введите кратчайшее расстояние от утопающего до берега d2 (в футах): ')
    h = validate_positive('Введите боковое смещение между спасателем и утопающим h (в ярдах): ')
    vsand = validate_positive('Введите cкорость движения спасателя по песку vsand(в милях в час): ')
    n = validate_positive('Введите коэффициент замедления спасателя при движении в воде n: ')

    return d1, d2, h, vsand, n


def calc_time_save(d1:float, d2:float, h:float, vsand:float, n:float) -> tuple():
    '''
    Функция принимает на вход числовые значения параметров
    Функция подбирает значение угла (theta1), под которым над начать движение спасателю, для достижения минимального времени.
    Функция возвращает оптимальное значение угла и соотв минимальное время спасения в секундах (формат float)
    '''
    yard_to_foot = 3
    mile_to_foot = 5280
    
    best_theta = 0.0
    best_time = float('inf')

    #Перебор c ограничением: прекращаем поиск, если значение увеличивается на 3 последовательных итерациях
    theta1 = 0.0
    step = 0.1
    increasing_count = 0
    max_increasing = 3
    while theta1 < 90:
        try:
            x = yard_to_foot * d1 * math.tan(math.radians(theta1))
            L1 = math.sqrt(x**2 + math.pow(yard_to_foot*d1,2))
            L2 = math.sqrt((yard_to_foot*h - x)**2 + math.pow(d2,2))
            t = 1/(mile_to_foot * vsand / 3600) *(L1 + n*L2)
        except (ValueError, OverflowError):
            break           
        if t < best_time:
            best_time = t
            best_theta = theta1
            increasing_count = 0
        else:
            increasing_count += 1
        if increasing_count >= max_increasing: 
            break
        theta1 += step
    return best_theta, best_time
                


def print_output(angle, t):
    print(f'Для заданных начальных условий оптимальный угол, равный {angle:.1f} градусам, обеспечит минимальное время спасения - {t:.1f} секунд')

#---МОДУЛЬНЫЕ ТЕСТЫ---
#Чтобы не вводить руками значения каждый раз
def make_fake_input(inputs):
    '''
    Для переопределения input() при тестировании функций валидации ввода.
    Принимает на вход коллекцию строк для теста (сценарий пользовательского ввода).
    На выходе выдает строчку из коллекции, плюс за счет замыкания хранит текущее значение итератора для последующих вызовов
    '''
    it = iter(inputs)
    def fake_input(prompt): 
        try:
            return next(it)
        except StopIteration:
            raise ValueError ("Fake_input: закончились значения для ввода")
    return fake_input

#Обертка для функций тестирования
def run_test(test_func):
    '''
    Функция для запуска теста:
        - принимает на вход функцию для теста
        - выводит имя теста (функции) на экран
        - запускает тест
        - обрабатывает результат теста и выводит на экран статус "пройден/не пройден"
    '''
    test_name = test_func.__name__
    print(f'Запуск теста {test_name}...')
    try:
        test_func()
        print(f'{test_name} пройден успешно')
        return True
    except Exception as e:
        print(f'{test_name} НЕ пройден: {e}')
        return False

def test_validate_positive():
    '''
    Тест для validate_positive: 
        - сначала по 1 экземпляру для каждого из невалидных классов эквивалентности
        - последним значение из валидного класса
    '''
    builtins.input = make_fake_input(["0", "-3", 'python', ' ', '2,5'])
    expected = 2.5
    result = validate_positive('')
    if result != expected:
        raise AssertionError(f'ожидалось {expected}, получено {result}')   

def test_calc_time_save():
    '''
    Тест для calc_time_save
    Ручной расчет 
    d1, d2, h, vsand, n = (3, 12, 10, 5, 2) --> оптимальный угол 69.2, мин время 7.2 сек
    '''
    expected_theta, expected_time = (69.2, 7.2)
    epsilon = 0.1
    actual_theta, actual_time = calc_time_save(3, 12, 10, 5, 2)
    if abs(actual_theta - expected_theta) >= epsilon or abs(actual_time - expected_time) >= epsilon:
        raise AssertionError(f'ожидаемые "угол-время" =({expected_theta},{expected_time}), получены =({actual_theta},{actual_time})')

all_tests = [test_validate_positive, test_calc_time_save]
print('Запуск модульных тестов...')
passed = 0
total = len(all_tests)
for test in all_tests:
    if run_test(test):
        passed +=1 
print(f'Итог: {passed} из {total} тестов пройдены успешно.')
    

# d1, d2, h, vsand, n = take_input()
# best_theta, best_time = calc_time_save(d1, d2, h, vsand, n)
# print_output(best_theta, best_time)


