from bitstring import BitArray as bitarray
import random2

class DNA(bitarray):
    def __init__(self, *args):
        super().__init__(*args)
        for i in range(len(self)):
            self[i] = random2.bit()
    def mutate(self):
        self[random2.rrange(len(self))] = not self[random2.rrange(len(self))]
    def __getitem__(self, key):
        key = key % len(self)
        return super().__getitem__(key)
    def __copy__(self):
        return DNA(super().__copy__())


bitsize = 9
best = DNA(bitsize)
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

for i in range(99):
    print(random2.rrange(9))
exit()

"""