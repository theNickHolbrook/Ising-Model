import random
# import matplotlib.pyplot as plt
# import numpy as np
# print(plt.style.available)
# plt.style.use('_mpl-gallery-nogrid')

# spins = [1,0,1,0,1,0,1,0]
spins = [1,1,1,1,1,1,1,1]
# spins = [0,0,0,0,0,0,0,0]
temp = 1
E = 0
rep = spins.copy()
fig, ax = plt.subplots()
print(spins)
for j in range(10):
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
        elif random.random() <= 3 ** (-1 * (E + val) / temp) and False:
            spins[index] = 1 ^ val
            # rep[index] = 1
        # else:
            # rep[index] = 0                
    # ax.imshow(spins, origin='lower')
    # plt.show()
    # print(rep, j)
    print(spins)