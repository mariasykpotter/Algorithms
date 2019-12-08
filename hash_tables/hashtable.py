import math


def nextPowerOf2(n):
    count = 0
    if (n and not (n & (n - 1))):
        return n
    while (n != 0):
        n >>= 1
        count += 1
    return 1 << count


def next_Prime_num(num):
    i = num + 1
    while i:
        isPrime = True
        d = 2
        while d ** 2 <= i:
            if i % d == 0:
                isPrime = False
                break
            d += 1
        if (isPrime):
            return i
        else:
            i += 1


def primeNoGreaterThan(N):
    primes = [None] * N
    primes[0] = primes[1] = 0;
    for i in range(2, N):
        primes[i] = 1
    for i in range(2, N):
        if (primes[i]):
            winner = i
            j = i + i
            while j < N:
                primes[j] = 0
                j += i
    return winner


class HashTable:
    def __init__(self, hash_type, values):
        self.values = values
        self.hash_type = hash_type
        if hash_type <= 2:
            self.hashTable = hashChainedTable(len(values), hash_type)
        elif hash_type < 5:
            self.hashTable = hashOpenAdressation(len(values), hash_type)
        for el in values:
            self.hashTable.insert(el)

    def get_collisions_amount(self):
        if self.hash_type > 2:
            return self.hashTable.collisions
        else:
            sum = 0
            for lst in self.hashTable.hashTable:
                if lst.length() > 1:
                    sum += lst.length()
            return sum

    def find_sum(self, s):
        if self.hash_type <= 2:
            for lst in self.hashTable.hashTable:
                head = lst.head
                while head is not None:
                    if self.hashTable.search(head.data) != None and self.hashTable.search(s - head.data) != None:
                        return (head.data, s - head.data)
                    head = head.next
        else:
            for el in self.hashTable.hashTable:
                if el != None and self.hashTable.search(el) != None and self.hashTable.search(s - el) != None and (
                        el != s - el):
                    return (el, s - el)


class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def length(self):
        len = 0
        val = self.head
        while val is not None:
            len += 1
            val = val.next
        return len

    def insert_at_beginning(self, newdata):
        NewNode = Node(newdata)
        NewNode.next = self.head
        self.head = NewNode


class hashChainedTable:
    def __init__(self, m, hash_type):
        self.hash_type = hash_type
        if hash_type == 1 and nextPowerOf2(m) < 3 * m:
            self.size = nextPowerOf2(m)
            self.hashTable = [LinkedList() for _ in range(self.size)]
        elif hash_type == 2 and next_Prime_num(m) < 3 * m:
            self.size = next_Prime_num(m)
            self.hashTable = [LinkedList() for _ in range(self.size)]

    def generalized_hash(self, value):
        if self.hash_type == 1:
            return self.multiplication_hashing_func(value)
        else:
            return self.division_hashing_func(value)

    def multiplication_hashing_func(self, key):
        return math.floor(self.size * ((key * 0.6180339887) % 1))

    def division_hashing_func(self, key):
        return key % len(self.hashTable)

    def insert(self, value):
        self.hashTable[self.generalized_hash(value)].insert_at_beginning(value)

    def search(self, key):
        head = self.hashTable[self.generalized_hash(key)].head
        while head is not None:
            if head.data == key:
                return key
            head = head.next
        return None


class hashOpenAdressation:
    def __init__(self, m, hash_type):
        self.biggest_prime = primeNoGreaterThan(3 * m)
        self.hashTable = [None] * self.biggest_prime
        self.hash_type = hash_type
        self.collisions = 0

    def generalized_hash(self, key, i):
        if key != None:
            if self.hash_type == 3:
                return self.linear_hash(key, i)
            elif self.hash_type == 4:
                return self.quadratic_hash(key, i)
            else:
                return self.double_hash(key, i)

    def hash_func(self, key):
        return key % self.biggest_prime

    def hash2(self, key):
        smaller_prime = primeNoGreaterThan(key)
        return smaller_prime - (key % smaller_prime)

    def linear_hash(self, key, i):
        return (self.hash_func(key) + i) % self.biggest_prime

    def quadratic_hash(self, key, i):
        return (self.hash_func(key) + i + i ** 2) % self.biggest_prime

    def double_hash(self, key, i):
        return (self.hash_func(key) + i * self.hash2(key)) % self.biggest_prime

    def insert(self, k):
        i = 0
        while True:
            j = self.generalized_hash(k, i)
            if self.hashTable[j] == None:
                self.hashTable[j] = k
                return j
            else:
                i = i + 1
                self.collisions += 1
            if i == self.biggest_prime:
                break

    def search(self, k):
        i = 0
        while True:
            j = self.generalized_hash(k, i)
            if self.hashTable[j] == k:
                return j
            elif self.hashTable[j] == None or i == self.biggest_prime:
                break
            else:
                i = i + 1
        return None
