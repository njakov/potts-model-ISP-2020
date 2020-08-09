# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 18:38:31 2020

@author: Acer
"""
import random
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def decision(probability):
    """ Do smth with given probability"""
    return random.random() < probability

def up(i, j):
    if i == 0:
        return (L-1, j)
    return (i-1, j)
  
def down(i, j):
    if i == (L-1):
        return(0, j)
    return (i+1, j)

def left(i, j):
    if j == 0:
        return(i, L-1)
    return (i, j-1)

def right(i, j):
    if j == L-1:
        return(i, 0)
    return (i, j+1)

neighbours = [up, down, left, right]
#------------------------------------------------------------------------------
def sum_spins(i, j):
    """Sum over nearest neighbours"""
    s = 0
    for neighbour in neighbours:
        s += lattice[neighbour(i, j)]
    return s
   
def hi(i, j):
    """Hamiltonian for specific spin site i"""
    return -1*lattice[i, j]*sum_spins(i, j)
       
def energy():
    """Energy"""
    E = 0
    for i in range(L):
        for j in range(L):
            E += hi(i, j)
    return E/2

def magn():
    """Magnetization"""
    spins_up = np.count_nonzero(lattice == 1)
    spins_down = N - spins_up
    m = abs(spins_up-spins_down)/N
    return m  
#------------------------------------------------------------------------------
time = 1000
L = 50
N = L*L
lattice = np.array([[1] * L for i in range(L)])

down = 0
while down != (L*L)/2:
    random_lattice_field = random.randrange(0, L*L)
    a, b = random_lattice_field//L, random_lattice_field%L
    if lattice[a, b] != -1:
        lattice[a, b] = -1
        down += 1
#------------------------------------------------------------------------------
energy_time = [energy()]
magn_time = [magn()]

for step in range(1, time+1):
    for every_spin in range(N):
        spin = random.randrange(0, L*L)
        x, y = spin//L, spin%L
        if sum_spins(x, y) > 0:
            #flip
            lattice[x, y] = 1
  
        elif sum_spins(x, y) == 0:
            if decision(0.5):
                lattice[x, y] = -1*lattice[x, y]
        else: 
            lattice[x, y] = -1
        
    if step%10 == 0:        
        energy_time.append(energy())
        magn_time.append(magn())
        
        
mc_step = list(range(time+1))[::10]

plt.plot(mc_step, energy_time)
plt.title('The Energy vs. time, for L= %i' %L)
plt.ylabel('Energy')
plt.xlabel('MC timestep')
plt.show()

plt.plot(mc_step, magn_time)
plt.title('Magnetisation vs. time, for L= %i' %L)
plt.ylabel('Magnetisation')
plt.xlabel('MC timestep')
plt.show()
#------------------------------------------------------------------------------  
lattice = np.ma.array(lattice, mask=np.isnan(lattice))
cmap = mpl.colors.LinearSegmentedColormap.from_list('my_colormap',
                                                    ['white', 'black'],
                                                    2)
cmap.set_bad(color='black')

#plt.imshow(a, interpolation='none', cmap=cmap)
#
img2 = plt.imshow(lattice, interpolation='none',
                  cmap=cmap,
                  origin='lower')

plt.colorbar(img2, cmap=cmap)
plt.ylabel('L')
plt.xlabel('L')
plt.show()
