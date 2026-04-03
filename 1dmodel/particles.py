import random

spins = [1,0,1,0,1,0,1,0]
E = 0

for i in spins:
    E += i
    

for j in range(100):
    for index, val in enumerate(spins):
        if (E - val) < E:
            spins[index] = 1 ^ val
        else:
            if random.random() <= 3 ** (-1 * E):
                spins[index] = 1 ^ val

    print(spins, j)