import random
import matplotlib.pyplot as plt
# import numpy as np
# print(plt.style.available)
# plt.style.use('_mpl-gallery-nogrid')

# plt.ion()

spins = [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0]
# spins = [1,1,1,1,1,1,1,1]
# spins = [0,0,0,0,0,0,0,0]
lattice = [spins]

graph = [
    [0,0,0,0,0,0,0,0,0,0],#kT/J
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]#C/Nk 
]

temp = 0.0001
E = 0
rep = spins.copy()
fig, ax = plt.subplots()
for temp in range(10):
    temp += 1
# if True:
    for j in range(100000):
        for index, val in enumerate(spins):
            
            if index - 1 < 0:
                E = spins[len(spins) - 1] + spins[index + 1]
            elif index + 1 >= len(spins):
                E = spins[index - 1] + spins[0]
            else:
                E = spins[index - 1] + spins[index + 1]
                
            #del E < 0
            # print(E + (val ^ 1), E + val)
            if (E + (val ^ 1)) < E + val:
                spins[index] = 1 ^ val
                # rep[index] = 2
            #r <= p
            elif random.random() <= 3 ** (-1 * (E + val) / temp):
                spins[index] = 1 ^ val
                # rep[index] = 1
            # else:
                # rep[index] = 0                
        # ax.imshow(lattice, origin='lower', cmap='magma')
        # plt.show()
        # plt.pause(0.001)
    # print(rep, j)
    graph[0][temp - 1] = temp
    graph[1][temp - 1] = sum(spins) / len(spins)
plt.plot(graph[0], graph[1])
plt.show()