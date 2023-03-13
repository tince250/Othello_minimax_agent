
class EmptyQueueException(Exception):
    pass

class Queue():

    def __init__(self):
        self._data = []

    def is_empty(self):
        return len(self._data) == 0

    def __len__(self):
        return len(self._data) #ovaj py len() je slozenosti O(n)

    def first(self):
        if self.is_empty():
            raise EmptyQueueException("Red je prazan")
        return self._data[0]

    def dequeue(self):
        if self.is_empty():
            raise EmptyQueueException("Red je prazan")

        elem = self._data[0]
        del self._data[0] #operator del brise objekte, aka bilo sta u pythonu

        return elem

    def enqueue(self, elem):
        self._data.append(elem)

    def __str__(self):
        return str(self._data)

class LimitedQueue(Queue):

    def __init__(self, capacity = 10):
        self._data = [None]*capacity
        self._capacity = capacity
        self._first = 0
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def first(self):
        if self.is_empty():
            raise EmptyQueueException("Red je prazan")
        return self._data[self._first]

    def dequeue(self):
        if self.is_empty():
            raise EmptyQueueException("Red je prazan")

        elem = self._data[self._first]
        self._data[self._first] = None
        self._size -= 1
        self._first = (self._first + 1) % self._capacity #opet mod zbog cirkularnosti

        if self._size < self._capacity/4:
            self.resize(self._capacity//2)

        return elem

    def enqueue(self, elem):
        if self._size + 1 > self._capacity:
            self.resize(self._capacity * 2)

        new_index = (self._first + self._size) % self._capacity
        print(new_index)
        self._data[new_index] = elem

        self._size += 1

    def resize(self, new_capacity):
        new_data = [None] * new_capacity #zauzmemo nove pozicije i stavimo ih None

        for new_index in range(self._size):
            old_index = (new_index + self._first) % self._capacity # mod zbog cirkularnosti
            new_data[new_index] = self._data[old_index]

        self._data = new_data
        self._capacity = new_capacity
        self._first = 0

if __name__ == '__main__':
    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    #print(q.dequeue())
    #print(q)

    lq = LimitedQueue(2)
    lq.enqueue(1)
    lq.enqueue(2)
    lq.enqueue(3)
    print(len(lq))
    print(lq)
    lq.enqueue(4)
    print(lq)
    lq.enqueue(5)
    print(lq)
