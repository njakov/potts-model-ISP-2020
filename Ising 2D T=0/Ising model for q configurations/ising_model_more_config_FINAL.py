# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 11:00:00 2020

@author: Nina
"""

from timeit import default_timer as timer
import random
import numpy as np

start = timer()

L = 50
N = L*L

def decision(probability):
    """ Do smth with given probability"""
    return random.random() < probability
    
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
#------------------------------------------------------------------------------
def sum_spins(i):
    """Sum over nearest neighbours"""
    s = 0
    for neighbour in links[i]:
        s += lattice[neighbour]
    return s

#def sum_spins2(i):
#    """Sum over nearest neighbours"""
#    s = sum(lattice[links[i]])
#    return s

def hi(i):
    """Local field"""
    return -1*lattice[i]*sum_spins(i)

def energy():
    """Energy"""
    E = 0
    for i in range(N):
        E += hi(i)
    return E/2

def magn():
    """Magnetization"""
    m = np.sum(lattice)/N
    return m
#------------------------------------------------------------------------------
no_config = 5
no_ground_states = 0
magn_all_config = []
energy_all_config = []
magn_active_config = []
energy_active_config = []

time = 3000

graph = open(f'{no_config}_configurations_lattices.txt', 'w+')

for configuration in range(no_config):

    lattice = np.ones((N,), dtype=int)
    minus_spin = 0
    while minus_spin != N/2:
        #random_lattice_field = np.random.randint(0, N)
        random_lattice_field = int(N * random.random())
        
        
        if lattice[random_lattice_field] != -1:
            lattice[random_lattice_field] = -1
            minus_spin += 1

    for step in range(1, time+1):
        for every_spin in range(N):
            #random spin
#            spin = np.random.randint(0, N)
            spin = int(N * random.random())
            ss=sum_spins(spin)
            if ss > 0:
                #flip
                lattice[spin] = 1

            elif ss == 0:
                if decision(0.5):
                    lattice[spin] = -1*lattice[spin]
            else:
                lattice[spin] = -1

        if step >= 500 and step % 50 == 0:
            if np.count_nonzero(lattice == 1) in [N, 0]:
                no_ground_states += 1
                break
    print(configuration)

    #magnetization and energy, all configurations
    magn_all_config.append(abs(magn()))
    energy_all_config.append(energy())

    #magnetization and energy, active configurations
    if step == time:
        magn_active_config.append(magn())
        energy_active_config.append(energy())

    #write lattice in .txt
    graph.write('Configuration number: %i \n' %configuration)
    graph.write("|")
    for spin in range(N):
        #x, y = spin//L, spin%L
        if (spin % L == 0 and spin != 0):
            graph.write("|\n")
            graph.write("|")
        if lattice[spin] == 1:
            graph.write("X")
        if lattice[spin] == -1:
            graph.write(" ")
    graph.write("|\n")
    graph.write("_______________________________________________________________________________\n")

graph.close()
end = timer()
run_time = end - start

#data
no_active_states = no_config - no_ground_states

m_magn_all_config = np.mean(magn_all_config)
m_energy_all_config = np.mean(energy_all_config)

m_magn_active_config = np.mean(magn_active_config)
m_energy_active_config = np.mean(energy_active_config)


ensemble = open(f'{no_config}_config_ensemble_data.txt', 'w+')

ensemble.write(
        f"""
Lattice dimensions: {L} \n
Number of configurations: {no_config} \n

Time (Total number of MC steps): {time} \n

Number of active states: {no_active_states} \n
Fraction of active states: {no_active_states/no_config} \n

Number of ground states: {no_ground_states} \n
Fraction of ground states: {no_ground_states/no_config} \n
Magnetization: {magn_all_config} \n
Mean magnetization: {m_magn_all_config} \n
Energy: {energy_all_config} \n
Mean energy: {m_energy_all_config}

Magnetization of active states: {magn_active_config} \n
Mean magnetization of active states: {m_magn_active_config} \n

Energy of active states: {energy_active_config} \n
Mean energy of active states: {m_energy_active_config} \n

Time of execution: {run_time} seconds \n
""")

ensemble.close()
print('done')
