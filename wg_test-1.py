# 1. На языке Python реализовать алгоритм (функцию) определения четности целого числа, который будет аналогичен
#    нижеприведенному по функциональности, но отличен по своей сути. Объяснить плюсы и минусы обеих реализаций.
#
#        Python example:
#
#        def isEven(value):return value%2==0

"""

    is_even_example():
        Плюсы: используется самый лаконичный вариант.
        Минусы: не представляю, когда бы мне могла понадобилась такая функция. Только ради самой функции.

    is_even_1():
        Минусы: костыли

    is_even_2():
        Минусы: ещё больше костылей

"""


def is_even_example(value):
    return value % 2 == 0


def is_even_1(value):
    res = int(str(value / 2).split('.')[1])
    return True if res == 0 else False


def is_even_2(value):
    res = bool(int(str(value / 2).split('.')[1]))
    return not res


if __name__ == '__main__':
    num = 42
    print(f'Remainder: {is_even_example(num)}')
    print(f'  Decimal: {is_even_1(num)}')
    print(f'     Bool: {is_even_2(num)}')
