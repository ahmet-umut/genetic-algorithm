from bitstring import BitArray as bitarray
import random2

random2.seed()

class DNA(bitarray):
    def __init__(self, *args):
        super().__init__(*args)
    def mutate(self):
        index = random2.rrange(len(self))
        self[index] = not self[index]
    def __getitem__(self, key):
        key = key % len(self)
        return super().__getitem__(key)
    def __copy__(self):
        return DNA(super().__copy__())
    def randomize(self):
        for i in range(len(self)):
            self[i] = random2.rrange(2)


bitsize = 9
best = DNA(bitsize)
best.randomize()
print(best)

step=0
one_count_best = best.count(1)
while one_count_best != bitsize:
    print(best, step:=step+1)
    candidate = best.copy()
    candidate.mutate()
    ni_count = candidate.count(1)
    if ni_count > one_count_best:
        best = candidate
        one_count_best = ni_count
    """
    best = candidate
    one_count_best = ni_count
    """

print(best)

"""
for i in range(9):
    print(random2.rrange(9))
exit()

"""