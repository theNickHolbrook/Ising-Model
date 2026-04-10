import random
import matplotlib.pyplot as plt
import numpy as np

graph = [
    [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],#kT/J
    [0.0] * 10#C/Nk 
]
energies = [
    [[],#count
    []] #energy
]

plt.ion()

lattice = np.zeros((30, 30), dtype=int)

def set_lattice(lattice):
    for i in range(len(lattice)):
        for j in range(len(lattice[0])):
            if random.random() < 0.5:
                lattice[i][j] = -1
            else:
                lattice[i][j] = 1

set_lattice(lattice)


def reset_lattice(lattice):
    lattice = np.zeros((10, 10), dtype=int)
    set_lattice(lattice)



def get_E_j(j, lattice, i, spin):
    if j - 1 < 0:
        E_j = lattice[len(lattice) - 1][i] * spin +  lattice[j + 1][i] * spin
    elif j + 1 >= len(lattice):
        E_j = lattice[j - 1][i] * spin + lattice[0][i] * spin
    else:
        E_j = lattice[j - 1][i] * spin + lattice[j - 1][i] * spin
    return E_j
        

def get_E_i(i, I_spins, spin):
    if i - 1 < 0:
        E_i = I_spins[len(I_spins) - 1] * spin + I_spins[i + 1] * spin
    elif i + 1 >= len(I_spins):
        E_i = I_spins[i - 1] * spin + I_spins[0] * spin
    else:
        E_i = I_spins[i - 1] * spin +  I_spins[i + 1] * spin
    return E_i
    
def getE(lattice):
    sum = 0
    N = len(lattice) * len(lattice[0])
    for j, j_spins in enumerate(lattice):
        for i_spin in j_spins:
            sum += i_spin / N
    return sum

def model(lattice, temp):
    E = 0
    # for j, I_spins in enumerate(lattice):
            
    #         for i, i_spin in enumerate(I_spins):
    

    j = random.randint(0, len(lattice) - 1)
    i = random.randint(0, len(lattice[0]) - 1)
    I_spins = lattice[j]
    i_spin = lattice[j][i]
    
    E_norm = get_E_i(i, I_spins, i_spin)
    E_norm += get_E_j(j, lattice, i, i_spin)
    
    E_flip = get_E_i(i, I_spins, i_spin * -1)
    E_flip += get_E_j(j, lattice, i, i_spin * -1)
        
    #del E < 0
    # if (E * (i_spin * -1)) > E * i_spin:
    if E_norm < E_flip:
        I_spins[i] = -1 * i_spin
        # rep[index] = 2
    #r <= p
    elif random.random() <= np.exp(-1 * (E_norm) / temp):
        I_spins[i] = -1 * i_spin

fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()

def plot_energy(lattice, count, index):
    E = getE(lattice)
    if index >= len(energies):
        energies.append([[],[]])
    energies[index][0].append(count)
    energies[index][1].append(E)
    ax3.plot(energies[index][0], energies[index][1], label=str(graph[0][index]))
    fig3.show()
    
    

def plot_model(lattice):
    ax1.imshow(lattice, origin='lower', cmap='magma')
    fig1.show()
    plt.pause(0.01)

for graph_index, temp in enumerate(graph[0]):
    for counts in range(100000):
        model(lattice, temp)
        # plot_energy(lattice, counts, graph_index)
    # for i in range(100):
    model(lattice, temp)
    plot_model(lattice)
    graph[1][graph_index] = getE(lattice)
    # for counts in range(10000):
    #     model(lattice)
    #     plot_model(lattice)
    reset_lattice(lattice)
ax2.plot(graph[0], graph[1])
plt.ioff()
fig3.show()