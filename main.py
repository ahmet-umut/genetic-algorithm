from bitstring import BitArray as bitarray
import random

class DNA(bitarray):
    def __init__(self, bitsize):
        super().__init__(bitsize)
        for i in range(bitsize):
            self[i] = random.randrange(2)
    def mutate(self):
        self[random.randrange(len(self))] = not self[random.randrange(len(self))]
    def __getitem__(self, key):
        key = key % len(self)
        return super().__getitem__(key)

random.seed(31)

bitsize = 9
best = DNA(bitsize)
#initialize with random bit string
for i in range(bitsize):
    best[i] = random.randrange(2)
print(best)

step=0
one_count_best = best.count(1)
while one_count_best != bitsize:
    print(best, step:=step+1)
    candidate = best.copy()
    candidate[random.randrange(bitsize)] = not candidate[random.randrange(bitsize)]
    ni_count = candidate.count(1)
    """
    if ni_count > one_count_best:
        best = candidate
        one_count_best = ni_count
    """
    best = candidate
    one_count_best = ni_count

print(best)