import random
import matplotlib.pyplot as plt
import numpy as np

#used to graph values, will cycle through first index's list (rn thats the temperatures)
graph = [
    [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],#kT/J
    [0.0] * 10#C/Nk 
]

energies = [
    [[],#count
     []]#energies
]

#allows for interactivity, so we can update the plot
plt.ion()

#lattice of atoms, -1 is down spin, 1 is up
lattice = np.zeros((30, 30), dtype=int)

#sets the lattice to random spins, use reset_lattice instead
def set_lattice(lattice):
    for i in range(len(lattice)):
        for j in range(len(lattice[0])):
            if random.random() < 0.5:
                lattice[i][j] = -1
            else:
                lattice[i][j] = 1
    return lattice

lattice = set_lattice(lattice)

#resets the lattice to random spins
def reset_lattice(lattice):
    lattice = np.zeros((len(lattice), len(lattice[0])), dtype=int)
    lattice = set_lattice(lattice)
    return lattice


#gets the column neighbors energy
def get_E_j(j, lattice, i, spin):
    if j - 1 < 0:
        E_j = lattice[len(lattice) - 1][i] * spin +  lattice[j + 1][i] * spin
    elif j + 1 >= len(lattice):
        E_j = lattice[j - 1][i] * spin + lattice[0][i] * spin
    else:
        E_j = lattice[j - 1][i] * spin + lattice[j - 1][i] * spin
    return E_j
        
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
    N = len(lattice) * len(lattice[0])
    for j, I_spins in enumerate(lattice):
        for i, i_spin in enumerate(I_spins):
            sum += abs(get_E_i(i, I_spins, i_spin))
            sum += abs(get_E_j(j, lattice, i, i_spin))
    return sum

#picks a random atom to see if it should flip the spin of it
def model(lattice, temp):
    
    #i is the row and j is the column
    j = random.randint(0, len(lattice) - 1)
    i = random.randint(0, len(lattice[0]) - 1)
    I_spins = lattice[j] #the row the chosen atom falls in
    i_spin = lattice[j][i] #the spin value of that atom
    
    E_norm = get_E_i(i, I_spins, i_spin) #current state
    E_norm += get_E_j(j, lattice, i, i_spin)
    
    E_flip = get_E_i(i, I_spins, i_spin * -1) #flipped state
    E_flip += get_E_j(j, lattice, i, i_spin * -1)
        
    #del E < 0
    if E_norm < E_flip:
        I_spins[i] = -1 * i_spin
        # rep[index] = 2
    #r <= p
    elif random.random() <= np.exp(-1 * (E_norm) / temp):
        I_spins[i] = -1 * i_spin

#first one is the only important one its to show the model the others I don't remember
fig1, ax1 = plt.subplots()
im = ax1.imshow(lattice, origin='lower', cmap='magma')
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
    
    
#plots the model
def plot_model(lattice, count):
    # ax1.imshow(lattice, origin='lower', cmap='magma')
    # fig1.canvas.restore_region(axbackground)
    # ax1.draw_artist(lattice)
    # fig1.canvas.blit(ax1.bbox)
    # fig1.canvas.draw()
    # fig1.canvas.flush_events()
    im.set_data(lattice)
    fig1.canvas.draw()
    # plt.pause(0.000001)
    fig1.canvas.flush_events()
    print(count)

#main loop
for graph_index, temp in enumerate(graph[0]):
    # for counts in range(100000):
    #     model(lattice, temp)
    for i in range(100000):
        model(lattice, temp)
        # if i % 1000 == 0:
        #     plot_model(lattice, i)
    graph[1][graph_index] = getE(lattice)
    lattice = reset_lattice(lattice)
    print("New temp")
ax2.plot(graph[0], graph[1])
plt.ioff()
fig3.show()
plt.show()