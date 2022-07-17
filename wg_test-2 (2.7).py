# 2. Na yazyke Python (2.7) realizovat minimum po 2 klassa realizovyvayushchikh tsiklicheskiy bufer FIFO.
#    Obyasnit plyusy i minusy kazhdoy realizatsii.

"""

    Spoiler: sponsor etogo chudesnogo translita - translate.google.com


    RingBufferPure_:
        + bez importov
        - nagromozhdeniye koda. Mozhno napisat boleye elegantno s ispolzovaniyem bibliotek (+10 k optimizatsii)


    RingBufferDeque:
        + lakonichnyy kod (yesli by ne bufernaya peremennaya)
        - bufernaya peremennaya zanimayet mesto v pamyati

"""

from collections import deque


class RingBufferPure_:

    def __init__(self, lst, capacity=None):
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
            raise ValueError('list.remove_it({value}): {value} not in list'.format(value=value))

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
        del self.lst[:]


class RingBufferDeque:

    def __init__(self, lst, capacity=None):
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
            raise ValueError('deque.remove({value}): {value} not in deque'.format(value=value))

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
        RingBufferPure_([_ for _ in range(lst_range)], maxlen),
        RingBufferDeque([_ for _ in range(lst_range)], maxlen)
    ]

    for buffer in buffers:
        print('               {}:    {}'.format(buffer.__class__.__name__, buffer.lst))
        cnt = buffer.count_it(6)
        print('              count_it(6) == {}:    {}'.format(cnt, buffer.lst))
        buffer.append_right(42)
        print('                  append_right:    {}'.format(buffer.lst))
        buffer.append_left(24)
        print('                   append_left:    {}'.format(buffer.lst))
        pop_test = buffer.pop_right()
        print('              pop_right() == {}:    {}'.format(pop_test, buffer.lst))
        pop_test = buffer.pop_left()
        print('              pop_left() == {}:    {}'.format(pop_test, buffer.lst))
        buffer.reverse_it()
        print('                    reverse_it:    {}'.format(buffer.lst))
        rt = 2
        buffer.rotate_it(rt)
        print('                  rotate_it({}):    {}'.format(rt, buffer.lst))
        rt = -1
        buffer.rotate_it(rt)
        print('                 rotate_it({}):    {}'.format(rt, buffer.lst))
        rm = 8
        buffer.remove_it(rm)
        print('                  remove_it({}):    {}'.format(rm, buffer.lst))
        lst_test = [111, 222, 333]
        buffer.extend_right(lst_test)
        print(' extend_right({}):    {}'.format(lst_test, buffer.lst))
        lst_test = [777, 888, 999]
        buffer.extend_left(lst_test)
        print('  extend_left({}):    {}'.format(lst_test, buffer.lst))
        buffer.clear_it()
        print('                      clear_it:    {}\n'.format(buffer.lst))
