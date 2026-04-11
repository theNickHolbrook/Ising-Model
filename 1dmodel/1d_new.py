#this is just the 1d case of the 2d model because I'm to lazy to fix the 1d model
import random
import matplotlib.pyplot as plt
import numpy as np

#used to graph values, will cycle through first index's list (rn thats the temperatures)
graph = [
    [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],#kT/J
    [0.0] * 10#C/Nk 
]

# energies = [
#     [[],#count
#      []]#energies
# ]

#allows for interactivity, so we can update the plot
plt.ion()

lattice = np.zeros((10,), dtype=int)

#sets the lattice to random spins, use reset_lattice instead
def set_lattice(lattice):
    for i in range(len(lattice)):
        if random.random() < 0.5:
            lattice[i] = -1
        else:
            lattice[i] = 1

set_lattice(lattice)

#resets the lattice to random spins
def reset_lattice(lattice):
    lattice = np.zeros((1, 10), dtype=int)
    set_lattice(lattice)

        
#gets the row neighbors energy
def get_E_i(i, I_spins, spin):
    if i - 1 < 0:
        E_i = I_spins[len(I_spins) - 1] * spin + I_spins[i + 1] * spin
    elif i + 1 >= len(I_spins):
        E_i = I_spins[i - 1] * spin + I_spins[0] * spin
    else:
        E_i = I_spins[i - 1] * spin +  I_spins[i + 1] * spin
    return E_i

#sums the energy, might need to be fixed
def getE(lattice):
    sum = 0
    N = len(lattice) * len(lattice)
    for i_spin in lattice:
        sum += i_spin / N
    return sum

#picks a random atom to see if it should flip the spin of it
def model(lattice, temp):
    
    #gets random spin
    i = random.randint(0, len(lattice) - 1)
    i_spin = lattice[i] #the spin value of that atom
    
    E_norm = get_E_i(i, lattice, i_spin) #current state
    
    E_flip = get_E_i(i, lattice, i_spin * -1) #flipped state
        
    #del E < 0
    if E_norm < E_flip:
        lattice[i] = -1 * i_spin
        # rep[index] = 2
    #r <= p
    elif random.random() <= np.exp(-1 * (E_norm) / temp):
        lattice[i] = -1 * i_spin

#first one is the only important one its to show the model the others I don't remember
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()

# def plot_energy(lattice, count, index):
#     E = getE(lattice)
#     if index >= len(energies):
#         energies.append([[],[]])
#     energies[index][0].append(count)
#     energies[index][1].append(E)
#     ax3.plot(energies[index][0], energies[index][1], label=str(graph[0][index]))
#     fig3.show()
    
    
#plots the model
def plot_model(lattice):
    ax1.imshow([lattice, [0]*10], origin='lower', cmap='magma')
    fig1.show()
    plt.pause(0.01)

#main loop
for graph_index, temp in enumerate(graph[0]):
    for counts in range(100000):
        model(lattice, temp)
    for i in range(10):
        model(lattice, temp)
        plot_model(lattice)
    graph[1][graph_index] = getE(lattice)
    reset_lattice(lattice)
ax2.plot(graph[0], graph[1])
plt.ioff()
fig3.show()