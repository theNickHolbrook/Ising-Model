import random
import matplotlib.pyplot as plt
import threading

# import numpy as np
# print(plt.style.available)
# plt.style.use('_mpl-gallery-nogrid')

# spins = [1,0,1,0,1,0,1,0]
spins = [1,1,1,1,1,1,1,1]
# spins = [0,0,0,0,0,0,0,0]

lattice = [spins.copy(),
           spins.copy(),
           spins.copy(),
           spins.copy(),
           spins.copy(),
           spins.copy(),
           spins.copy(),
           spins.copy(),
           ]

def get_E_j(j, lattice, i):
    if j - 1 < 0:
        E_j = lattice[len(lattice) - 1][i] + lattice[j + 1][i]
    elif j + 1 >= len(lattice):
        E_j = lattice[j - 1][i] + lattice[0][i]
    else:
        E_j = lattice[j - 1][i] + lattice[j - 1][i]
    return E_j
        

def get_E_i(i, I_spins):
    if i - 1 < 0:
        E_i = I_spins[len(I_spins) - 1] + I_spins[i + 1]
    elif i + 1 >= len(I_spins):
        E_i = I_spins[i - 1] + I_spins[0]
    else:
        E_i = I_spins[i - 1] + I_spins[i + 1]
    return E_i
    


temp = 1
E = 0
rep = spins.copy()
fig, ax = plt.subplots()

plt_thread_end = False

# def plot(ax, plt, lattice, plt_thread_end):
#     plt.clf()
#     ax.imshow(lattice, origin='lower')
#     plt.show()

# plt_thread = threading.Thread(target=plot, args=(ax, plt, lattice, plt_thread_end))


for j, I_spins in enumerate(lattice):
    
    for i, i_spin in enumerate(I_spins):
        
        E = get_E_i(i, I_spins)
        E += get_E_j(j, lattice, i)
        
            
        #del E < 0
        # print(E + (val ^ 1), E + val)
        if (E + (i_spin ^ 1)) < E + i_spin:
            I_spins[i] = 1 ^ i_spin
            # rep[index] = 2
        #r <= p
        elif random.random() <= 3 ** (-1 * (E + i_spin) / temp):
            I_spins[i] = 1 ^ i_spin
            # rep[index] = 1
        # else:
            # rep[index] = 0                
    # print(rep, j)
    # if plt_thread.is_alive():
    #     plt_thread_end = True
    #     plt_thread.join()
    #     plt_thread_end = False
    # plt_thread.start()
    ax.imshow(lattice, origin='lower')
    plt.show()
    print(spins)