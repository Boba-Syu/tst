class Heap:

    def __init__(self, a):
        self.a = a
        self.N = a.__len__()

    def swim(self, i):
        if i > 1 and self.a[i] > self.a[i / 2]:
            self.a[i], self.a[i / 2] = self.a[i / 2], self.a[i]
            i /= 2

    def sink(self, i):
        if i < self.N:
            j = i * 2
            if self.a[j] < self.a[j + 1]:
                j += 1
            self.a[i], self.a[j] = self.a[j], self.a[i]
            i = j
