# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 15:51:10 2020

@author: Nina
"""

from timeit import default_timer as timer
import random
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

L = 50
N = L*L
q = 3
states  = [1,2,3]
time = 2000

lattice = np.ones((N,), dtype=int)
twos = 0
threes = 0

while twos != N//3:
    random_lattice_field = int(N * random.random())
    if lattice[random_lattice_field] == 1:
        lattice[random_lattice_field] = 2
        twos += 1
while threes != N//3:
    random_lattice_field = int(N * random.random())
    if lattice[random_lattice_field] == 1:
        lattice[random_lattice_field] = 3
        threes += 1
#check
print('jedinica ima: ', np.count_nonzero(lattice == 1))
print('dvojki ima: ', np.count_nonzero(lattice == 2))
print('trojki ima: ', np.count_nonzero(lattice == 3))

def decision(probability):
    """ Do smth with given probability"""
    return random.random() < probability
    
def kronecker(i,j):
    if lattice[i] == lattice[j]:
        return 1
    else:
        return 0
 
def up(i):
    if i//L == 0:
        return ((i-L) + N)   
    else:
        return (i-L)
    
def down(i):
    if i//L == L-1:
        return(i%L)
    else:
        return (i+L)
    
def left(i):
    if i%L == 0:
        return(i+L-1)
    else:
        return (i-1)
    
def right(i):
    if i%L == L-1:
        return(i-(L-1))
    else:
        return (i+1)
    
links = []   
for j in range (N):
    links.append([left(j), right(j), up(j), down(j)])

def sum_spins(i):
    """Sum over nearest neighbours"""
    s = 0
    for neighbour in links[i]:
        s += kronecker(i, neighbour)
    return s

def hi(i):
    """Local field"""
    return -1*sum_spins(i)

def energy():
    """Energy"""
    E = 0
    for i in range(N):
        E += hi(i)
    return E


print('Energija na pocetku: ', energy())

for step in range(1, time+1):
    for every_spin in range(N):
        
        #random spin
        spin = int(N * random.random())
        old_orient = lattice[spin]
        h_pre = hi(spin)
        
        #random configuration
        new_orient = random.choice(states)
        #flipujem odmah da bih izracunala h_posle
        lattice[spin] = new_orient
        h_posle = hi(spin)
        
        #check
        #vracam na staro ako zadovoljeno
        if h_posle > h_pre:
            lattice[spin] = old_orient
            
        #vracam na staro stanje sa ver 0.5
        if h_posle == h_pre:
            if decision(0.5):
                lattice[spin] = old_orient
                
        #u suprotnom ostaje flipovan
        
print('Energija na kraju: ', energy()) 
#------------------------------------------------------------------------------
lattice1 = np.reshape(lattice, (L,L))
lattice1 = np.ma.array(lattice1, mask=np.isnan(lattice1))
cmap = mpl.colors.LinearSegmentedColormap.from_list('my_colormap',
                                                    ['orange', 'white', 'turquoise'],
                                                    3)
cmap.set_bad(color='black')

#plt.imshow(a, interpolation='none', cmap=cmap)
#
img2 = plt.imshow(lattice1, interpolation='none',
                  cmap=cmap,
                  origin='lower')

plt.colorbar(img2, cmap=cmap)
plt.ylabel('L')
plt.xlabel('L')
plt.show()
