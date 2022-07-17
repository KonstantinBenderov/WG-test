# 3. На языке Python реализовать функцию, которая быстрее всего (по процессорным тикам)
#    отсортирует данный ей массив чисел. Массив может быть любого размера со случайным порядком чисел
#    (в том числе и отсортированным). Объяснить почему вы считаете, что функция соответствует заданным критериям.

"""

    Во время обучения не сравнивал скорость "Сортировки кучей" и "Быстрой сортировки".
    А тем более - с уже отсортированными массивами.
    Пользуясь случаем, решил наверстать :)

    Скорость "Быстрой сортировки" сильно зависит от:
        - наличия одинаковых элементов (больше повторов - ниже скорость)
        - и положения ключевого индекса (ближе к началу / концу - медленнее).
    На отсортированных данных - время такое же.
    Из-за её рекурсивности не всякой длины массив осилит (если не менять настройки глубины, конечно)

    "Сортировка кучей" - разница в скорости меняется не сильно.
    С множеством одинаковых элементов работает быстрее, чем с разными.

    Встроенная функция 'sort' самая шустрая.
    Лучше, конечно, использовать встроенные инструменты: они ведь не зря встроены ;)

    А какой вариант выбрать из "рукописных" - уже зависит от параметров сортируемого массива. ¯\_(ツ)_/¯
        Уникальные элементы - "Быстрая сортировка"
        Много повторяющихся - "Кучей"

"""

from random import randint
from time import time


# Сортировка кучей (Пирамида)
class HeapSort:

    def __init__(self, lst: list):
        self.lst = lst

    @staticmethod
    def heap_sift(lst, start, end):
        root = start

        while True:
            child = root * 2 + 1
            if child > end:
                break

            if child + 1 <= end and lst[child] < lst[child + 1]:
                child += 1

            if lst[root] < lst[child]:
                lst[root], lst[child] = lst[child], lst[root]
                root = child
            else:
                break

    def heap_sort(self):
        max_idx = len(self.lst) - 1

        for start in range(max_idx // 2, -1, -1):
            self.heap_sift(self.lst, start, max_idx)

        for end in range(max_idx, 0, -1):
            self.lst[end], self.lst[0] = self.lst[0], self.lst[end]
            self.heap_sift(self.lst, 0, end - 1)

        return self.lst


# Быстрая сортировка
def quick_sort(lst, start=0, end=None):
    def subpart(lst, start, end, pivot_idx):
        lst[start], lst[pivot_idx] = lst[pivot_idx], lst[start]
        pivot = lst[start]
        x = start + 1
        y = start + 1

        while y <= end:
            if lst[y] <= pivot:
                lst[y], lst[x] = lst[x], lst[y]
                x += 1
            y += 1

        lst[start], lst[x - 1] = lst[x - 1], lst[start]
        return x - 1

    if end is None:
        end = len(lst) - 1

    if end - start < 1:
        return

    pivot_idx = randint(start, end)
    x = subpart(lst, start, end, pivot_idx)
    quick_sort(lst, start, x - 1)
    quick_sort(lst, x + 1, end)


if __name__ == '__main__':
    rand_range = 100
    for x in range(2):
        nums = [randint(-rand_range, rand_range) for _ in range(100000)]
        nums2 = nums.copy()
        nums3 = nums.copy()

        for y in range(2):
            if y == 0:
                print(f'\n{"":39}Вводные данные: [randint(-{rand_range}, {rand_range}) for _ in range(100000)]\n')
            heap = HeapSort(nums)
            time_start = time()
            heap.heap_sort()
            time_diff = time() - time_start
            print(f'                                    Время "heap_sort": {time_diff}')

            time_start = time()
            quick_sort(nums2)
            time_diff = time() - time_start
            print(f'            Время "quick_sort" (ключевой индекс == 0): {time_diff}')

            time_start = time()
            quick_sort(nums2, len(nums2) // 2)
            time_diff = time() - time_start
            print(f'   Время "quick_sort" (ключевой индекс ~ по середине): {time_diff}')

            time_start = time()
            nums3.sort()
            time_diff = time() - time_start
            print(f'                                       Время "sort()": {time_diff}')

            if y == 0:
                print('\n                                      Отсортированные:')

        rand_range *= 1000

        if x == 0:
            print('\n' + '#' * 106 + '\n')
