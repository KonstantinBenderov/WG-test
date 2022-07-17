# 2. На языке Python (2.7) реализовать минимум по 2 класса реализовывающих циклический буфер FIFO.
#    Объяснить плюсы и минусы каждой реализации.

"""
    * Для Python 3

    RingBufferPure_:
        + без импортов
        - нагромождение кода. Можно написать более элегантно с использованием библиотек (+10 к оптимизации)

    RingBufferDeque:
        + лаконичный код (если бы не буферная переменная)
        - буферная переменная занимает место в памяти

"""

from abc import ABC, abstractmethod
from collections import deque


class RingBuffer(ABC):

    @abstractmethod
    def count_it(self, value):
        pass

    @abstractmethod
    def append_right(self, value):
        pass

    @abstractmethod
    def append_left(self, value):
        pass

    @abstractmethod
    def pop_right(self):
        pass

    @abstractmethod
    def pop_left(self):
        pass

    @abstractmethod
    def reverse_it(self):
        pass

    @abstractmethod
    def rotate_it(self, n):
        pass

    @abstractmethod
    def remove_it(self, value):
        pass

    @abstractmethod
    def extend_right(self, iter_obj):
        pass

    @abstractmethod
    def extend_left(self, iter_obj):
        pass

    @abstractmethod
    def clear_it(self):
        pass


class RingBufferPure(RingBuffer):

    def __init__(self, lst, capacity: int = None):
        if capacity and len(lst) > capacity:
            while len(lst) > capacity:
                lst.pop(0)

        self.lst = lst
        self.capacity = capacity

    def count_it(self, value):
        return len([i for i in self.lst if i == value])

    def append_right(self, value):
        if self.capacity and len(self.lst) + 1 > self.capacity:
            self.pop_left()
        self.lst.append(value)

    def append_left(self, value):
        if self.capacity and len(self.lst) + 1 > self.capacity:
            self.pop_right()
        self.lst.insert(0, value)

    def pop_right(self):
        if self.lst:
            return self.lst.pop()
        else:
            raise IndexError('pop from an empty list')

    def pop_left(self):
        if self.lst:
            return self.lst.pop(0)
        else:
            raise IndexError('pop from an empty list')

    def reverse_it(self):
        self.lst.reverse()

    def rotate_it(self, n):
        for _ in range(abs(n)):
            if n > 0:
                self.append_left(self.pop_right())
            if n < 0:
                self.append_right(self.pop_left())

    def remove_it(self, value):
        if value in self.lst:
            self.lst.remove(value)
        else:
            raise ValueError(f'list.remove_it({value}): {value} not in list')

    def extend_right(self, iter_obj):
        for i in iter_obj:
            if self.capacity and len(self.lst) > self.capacity:
                self.pop_left()
                self.append_right(i)
            else:
                self.append_right(i)

    def extend_left(self, iter_obj):
        for i in iter_obj:
            if self.capacity and len(self.lst) > self.capacity:
                self.pop_right()
                self.append_left(i)
            else:
                self.append_left(i)

    def clear_it(self):
        self.lst.clear()


class RingBufferDeque(RingBuffer):

    def __init__(self, lst, capacity: int = None):
        self.deque = deque(lst, maxlen=capacity)
        self.lst = list(self.deque)
        self.capacity = capacity

    def count_it(self, value):
        return self.deque.count(value)

    def append_right(self, value):
        self.deque.append(value)
        self.lst = list(self.deque)

    def append_left(self, value):
        self.deque.appendleft(value)
        self.lst = list(self.deque)

    def pop_right(self):
        if self.deque:
            res = self.deque.pop()
            self.lst = list(self.deque)
            return res
        else:
            raise IndexError('pop from an empty deque')

    def pop_left(self):
        if self.deque:
            res = self.deque.popleft()
            self.lst = list(self.deque)
            return res
        else:
            raise IndexError('pop from an empty deque')

    def reverse_it(self):
        self.deque = deque(reversed(self.deque), maxlen=self.capacity)
        self.lst = list(self.deque)

    def rotate_it(self, n):
        self.deque.rotate(n)
        self.lst = list(self.deque)

    def remove_it(self, value):
        if value in self.deque:
            self.deque.remove(value)
            self.lst = list(self.deque)
        else:
            raise ValueError(f'deque.remove({value}): {value} not in deque')

    def extend_right(self, iter_obj):
        self.deque.extend(iter_obj)
        self.lst = list(self.deque)

    def extend_left(self, iter_obj):
        self.deque.extendleft(iter_obj)
        self.lst = list(self.deque)

    def clear_it(self):
        self.deque.clear()
        self.lst = list(self.deque)


if __name__ == '__main__':
    lst_range = 10
    maxlen = 7

    buffers = [
        RingBufferPure([_ for _ in range(lst_range)], maxlen),
        RingBufferDeque([_ for _ in range(lst_range)], maxlen)
    ]

    for buffer in buffers:
        print(f'{"":15}{type(buffer).__name__:15}:    {buffer.lst}')
        cnt = 6
        cnt_res = buffer.count_it(cnt)
        print(f'              count_it({cnt}) == {cnt_res}:    {buffer.lst}')
        buffer.append_right(42)
        print(f'                  append_right:    {buffer.lst}')
        buffer.append_left(24)
        print(f'                   append_left:    {buffer.lst}')
        pop_test = buffer.pop_right()
        print(f'              pop_right() == {pop_test}:    {buffer.lst}')
        pop_test = buffer.pop_left()
        print(f'              pop_left() == {pop_test}:    {buffer.lst}')
        buffer.reverse_it()
        print(f'                    reverse_it:    {buffer.lst}')
        rt = 2
        buffer.rotate_it(rt)
        print(f'                  rotate_it({rt}):    {buffer.lst}')
        rt = -1
        buffer.rotate_it(rt)
        print(f'                 rotate_it({rt}):    {buffer.lst}')
        rm = 8
        buffer.remove_it(rm)
        print(f'                  remove_it({rm}):    {buffer.lst}')
        lst_test = [111, 222, 333]
        buffer.extend_right(lst_test)
        print(f' extend_right({lst_test}):    {buffer.lst}')
        lst_test = [777, 888, 999]
        buffer.extend_left(lst_test)
        print(f'  extend_left({lst_test}):    {buffer.lst}')
        buffer.clear_it()
        print(f'                      clear_it:    {buffer.lst}\n')
