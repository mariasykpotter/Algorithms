import math


class Heap:
    @staticmethod
    def parent(i):
        return math.floor((i + 1) // 2) - 1

    @staticmethod
    def left(i):
        return 2 * (i + 1) - 1

    @staticmethod
    def right(i):
        return 2 * (i + 1)


class MaxHeap:
    @staticmethod
    def maxheapify(A, i):
        p = Heap.left(i)
        q = Heap.right(i)
        if p < len(A) and A[p] > A[i]:
            largest = p
        else:
            largest = i
        if q < len(A) and A[q] > A[largest]:
            largest = q
        if largest != i:
            val = A[largest]
            A[largest] = A[i]
            A[i] = val
            MaxHeap.maxheapify(A, largest)
        return A

    @staticmethod
    def buildmaxheap(A):
        for i in range(math.floor(len(A) // 2), -1, -1):
            MaxHeap.maxheapify(A, i)
        return A

    @staticmethod
    def heapmaximum(A):
        try:
            return A[0]
        except IndexError as er:
            print(er)

    @staticmethod
    def heapextractmax(A):
        size = len(A)
        if size < 1:
            print("Queue is empty")
        max = A[0]
        A[0] = A[size - 1]
        del (A[size - 1])
        MaxHeap.maxheapify(A, 0)
        return max

    @staticmethod
    def heapincreasekey(A, i, key):
        if key < A[i]:
            print("New key is smaller than previous one")
        A[i] = key
        while i > 0 and A[Heap.parent(i)] < A[i]:
            val = A[Heap.parent(i)]
            A[Heap.parent(i)] = A[i]
            A[i] = val
            i = Heap.parent(i)
        return A

    @staticmethod
    def maxheapinsert(A, key):
        size = len(A)
        size += 1
        A.append(float('-inf'))
        MaxHeap.heapincreasekey(A, size - 1, key)
        return A


class MinHeap(Heap):
    @staticmethod
    def minheapify(A, i):
        p = Heap.left(i)
        q = Heap.right(i)
        if p < len(A) and A[p] < A[i]:
            smallest = p
        else:
            smallest = i
        if q < len(A) and A[q] < A[smallest]:
            smallest = q
        if smallest != i:
            val = A[smallest]
            A[smallest] = A[i]
            A[i] = val
            MinHeap.minheapify(A, smallest)
        return A

    @staticmethod
    def buildminheap(A):
        size = len(A)
        for i in range(size // 2, -1, -1):
            MinHeap.minheapify(A, i)
        return A

    @staticmethod
    def heapminimum(A):
        return A[0]

    @staticmethod
    def heapdecreasekey(A, i, key):
        if key < A[i]:
            print("New key is smaller than previous one")
        A[i] = key
        while i > 0 and A[Heap.parent(i)] > A[i]:
            val = A[Heap.parent(i)]
            A[Heap.parent(i)] = A[i]
            A[i] = val
            i = Heap.parent(i)
        return A

    @staticmethod
    def heapextractmin(A):
        size = len(A)
        if size < 1:
            print("Queue is empty")
        min = A[0]
        A[0] = A[size - 1]
        del (A[size - 1])
        MinHeap.minheapify(A, 0)
        return min

    @staticmethod
    def minheapinsert(A, key):
        size = len(A)
        size = size + 1
        A.append(float('-inf'))
        MinHeap.heapdecreasekey(A, size - 1, key)
        return A


class Median:
    def __init__(self):
        self.A_min = []
        self.A_max = []

    def add_element(self, value):
        if len(self.A_max) == 0:
            self.A_max = MaxHeap.maxheapinsert(self.A_max, value)
            self.optimize()
            return 0
        elif value < MaxHeap.heapmaximum(self.A_max):
            self.A_max = MaxHeap.maxheapinsert(self.A_max, value)
            self.optimize()
            return 0
        else:
            self.A_min = MinHeap.minheapinsert(self.A_min, value)
        self.optimize()

    def optimize(self):
        if len(self.A_min) - len(self.A_max) > 1:
            MaxHeap.maxheapinsert(self.A_max, MinHeap.heapextractmin(self.A_min))
        elif len(self.A_max) - len(self.A_min) > 1:
            MinHeap.minheapinsert(self.A_min, MaxHeap.heapextractmax(self.A_max))

    def get_median(self):
        if len(self.A_max) == len(self.A_min):
            return (MaxHeap.heapmaximum(self.A_max), MinHeap.heapminimum(self.A_min))
        elif len(self.A_min) > len(self.A_max):
            return MinHeap.heapminimum(self.A_min)
        else:
            return MaxHeap.heapmaximum(self.A_max)

    def get_maxheap_elements(self):
        return self.A_max

    def get_minheap_elements(self):
        return self.A_min


class Node():
    def __init__(self, value):
        self.value = value
        self.kids = []


class PairingHeap():
    def __init__(self, max):
        self.root = None
        self.max = max

    def meld(self, root1, root2):
        if root1 is None:
            return root2
        elif root2 is None:
            return root1
        elif ((self.max and root1.value > root2.value) or (not self.max and root1.value < root2.value)):
            root1.kids.append(root2)
            return root1
        else:
            root2.kids.append(root1)
            return root2

    def get_root(self):
        if self.root is None:
            raise ValueError("Heap is empty!")
        else:
            return self.root.value

    def insert(self, val):
        self.root = self.meld(self.root, Node(val))

    def delete_min(self):
        if self.root is None:
            raise ValueError("Heap is empty!")
        else:
            min = self.root.value
            self.root = self.merge_pairs(self.root.kids)

    def merge_pairs(self, arr):
        if len(arr) == 0:
            return None
        elif len(arr) == 1:
            return arr[0]
        else:
            return self.meld(self.meld(arr[0], arr[1]), self.merge_pairs(arr[2:]))

    def get_all_nodes(self, el, lst):
        if el is not None:
            if lst == []:
                lst.append(el.value)
            if el.kids:
                for e in el.kids:
                    lst.append(e.value)
                    self.get_all_nodes(e, lst)
            return lst
        else:
            return []


class PairingMedian:
    def __init__(self):
        self.maxheap = PairingHeap(True)
        self.minheap = PairingHeap(False)

    def add_element(self, value):
        if self.maxheap.root is None:
            self.maxheap.insert(value)
            self.optimize()
            return 0
        elif value < self.maxheap.get_root():
            self.maxheap.insert(value)
            self.optimize()
            return 0
        else:
            self.minheap.insert(value)
            self.optimize()

    def optimize(self):
        if len(self.minheap.get_all_nodes(self.minheap.root, [])) - len(
                self.maxheap.get_all_nodes(self.maxheap.root, [])) > 1:
            self.maxheap.insert(self.minheap.get_root())
            self.minheap.delete_min()
        elif len(self.maxheap.get_all_nodes(self.maxheap.root, [])) - len(
                self.minheap.get_all_nodes(self.minheap.root, [])) > 1:
            self.minheap.insert(self.maxheap.get_root())
            self.maxheap.delete_min()

    def get_median(self):
        if len(self.maxheap.get_all_nodes(self.maxheap.root, [])) == len(
                self.minheap.get_all_nodes(self.minheap.root, [])):
            return (self.maxheap.get_root(), self.minheap.get_root())
        elif len(self.minheap.get_all_nodes(self.minheap.root, [])) > len(
                self.maxheap.get_all_nodes(self.maxheap.root, [])):
            return self.minheap.get_root()
        else:
            return self.maxheap.get_root()