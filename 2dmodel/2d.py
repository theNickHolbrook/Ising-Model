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

lattice = np.zeros((10, 10), dtype=int)

def reset_lattice(lattice):
    lattice = np.zeros((10, 10), dtype=int)



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
    
def getE(lattice):
    sum = 0
    N = len(lattice) * len(lattice[0])
    for j, j_spins in enumerate(lattice):
        for i_spin in j_spins:
            sum += i_spin / N
    return sum

def model(lattice):
    E = 0
    for j, I_spins in enumerate(lattice):
            
            for i, i_spin in enumerate(I_spins):
                
                E = get_E_i(i, I_spins)
                E += get_E_j(j, lattice, i)
                
                    
                #del E < 0
                if (E + (i_spin ^ 1)) < E + i_spin:
                    I_spins[i] = 1 ^ i_spin
                    # rep[index] = 2
                #r <= p
                elif random.random() <= 3 ** (-1 * (E + i_spin) / temp):
                    I_spins[i] = 1 ^ i_spin

fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()

def plot_energy(lattice, count, index):
    E = getE(lattice)
    if index >= len(energies):
        energies.append([[],[]])
    energies[index][0].append(count)
    energies[index][1].append(E)
    ax3.plot(energies[index][0], energies[index][1], label=str(graph[index]))
    fig3.show()
    
    

def plot_model(lattice):
    ax1.imshow(lattice, origin='lower', cmap='magma')
    fig3.show()
    plt.pause(0.25)

for graph_index, temp in enumerate(graph[0]):
    for counts in range(100):
        model(lattice)
        plot_energy(lattice, counts, graph_index)
    for i in range(10):
        model(lattice)
        plot_model(lattice)
    graph[1][graph_index] = getE(lattice)
    reset_lattice(lattice)
ax2.plot(graph[0], graph[1])
plt.ioff()
fig3.show()