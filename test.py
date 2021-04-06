from itertools import permutations

l = [1,2,3]

for i in range(1,4):
    print([list(p) for p in permutations(l,i)])