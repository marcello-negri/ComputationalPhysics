# EXERCISE 8
import random
from datetime import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

def create_lattice (L):
    lattice = np.zeros((L,L))
    for i in range(L):
        for j in range(L):
            lattice[i][j] = 1

    return lattice

def period_bound(i,j,lattice,pos):
    max = len(lattice)-1
    if pos==0: # pos: 0 = up
        if j==0:
            return (i,max)
        else:
            return (i,j-1)
    elif pos==1: # pos: 1 = right
        if i==max:
            return (0,j)
        else:
            return (i+1,j)
    elif pos==2: # pos: 2 = down
        if j==max:
            return (i,0)
        else:
            return (i,j+1)
    elif pos==3: # pos: 3 = left
        if i==0:
            return (max,j)
        else:
            return (i-1,j)
    else:
        print "Index out of range!"

def delta_e (i,j,lattice):
    count = 0
    for k in range(0,4):
        pos = period_bound(i,j,lattice,k)
        count += lattice[pos[0]][pos[1]]
    return 2 * count * lattice[i][j]

def magnetization (lattice):
    count = 0
    for i in range (0,len(lattice)):
        for j in range (0,len(lattice)):
            count+=lattice[i][j]
    return count/len(lattice)**2

def metropolis (lattice,T, sweep):
    random.seed(datetime.now())
    energy = 0
    for k in range(0,sweep):
        i = random.randint(0,len(lattice)-1)
        j = random.randint(0,len(lattice)-1)
        eta = random.random()
        boltzmann = np.exp(-delta_e(i,j,lattice)/T)

        if delta_e(i,j,lattice)<0:
            lattice[i][j] = -lattice[i][j]
        elif eta < boltzmann:
            lattice[i][j] = -lattice[i][j]
            energy += boltzmann

    return lattice, energy

L = 50 # square lattice side
M = 1000 # iteration for each temperature

temp_range = np.arange(0.1,4,0.1)

magn_mean = []
energy_mean = []
magn_error = []
energy_error = []

plt.title('Magnetization(T)')
plt.xlabel('T(K)')
plt.ylabel('m')

for T in temp_range:
    lat = create_lattice(L)
    magn = []
    energy = []
    lat, en = metropolis(lat,T,L**2*100) # enough to reach equilibrium
    for i in range(0,M):
        lat, en = metropolis(lat,T,L**2) # enough to obtain a new equil config
        energy.append(en)
        magn.append(magnetization(lat))
    energy = np.array(energy)
    energy_mean.append(np.mean(energy))
    energy_error.append(np.std(energy))
    magn = np.array(magn)
    magn_mean.append(np.mean(magn))
    magn_error.append(np.std(magn))
    print "temperature = %0.1f"%T

plt.plot(temp_range, magn_mean, "o")
plt.errorbar(temp_range, magn_mean, yerr=magn_error)
plt.savefig('magnetization.pdf')
plt.close()

plt.title('Energy(T)')
plt.xlabel('T(K)')
plt.ylabel('E')
plt.plot(temp_range, energy_mean, "o")
plt.errorbar(temp_range,energy_mean,yerr=energy_error)
plt.savefig('energy.pdf')
plt.close()
