# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 11:00:00 2020

@author: Nina
"""

from timeit import default_timer as timer
import random
import numpy as np

start = timer()

#dimenzije resetke
L = 50
N = L*L
k = 4 #broj suseda

#verovatnoca povezivanja
p = 0.05
broj_linkova = (N*2) 
potrebno_prepovezanih = int(broj_linkova*p)

#Ising
no_config = 10
time = 3000

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
    
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 

#==============================================================================        
susedi = []
susedi_resetka = []

#susedi na početku
for j in range (N):
    susedi.append([left(j), right(j), up(j), down(j)])
    susedi_resetka.append([left(j), right(j), up(j), down(j)])

#------------------------------------------------------------------------------
def sum_spins(i):
    """Sum over nearest neighbours"""
    s = 0
    for neighbour in susedi[i]:
        s += lattice[neighbour]
    return s

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

no_ground_states = 0
magn_all_config = []
energy_all_config = []
magn_active_config = []
energy_active_config = []

graph = open(f'{no_config}_configurations_lattices.txt', 'w+')

for configuration in range(no_config):
    
    #prepovezivanje resetka, svaka konfiguracija
    #--------------------------------------------------------------------------
    #susedi na početku
    susedi = []
    susedi_resetka = []
    for j in range (N):
        susedi.append([left(j), right(j), up(j), down(j)])
        susedi_resetka.append([left(j), right(j), up(j), down(j)])

    #prvi krug prepovezivanja
    brojac = 0
    broj_prepovezanih = 0
    for nod in range(N):
        linkovi = intersection(susedi[nod],susedi_resetka[nod])
        for sused in linkovi:
            if sused > nod:
                if decision(p):
                    if len(susedi[sused])> 2:
                        check = 0
                        while check == 0:
                            novi_sused = random.randrange(0, N)
                            if not (novi_sused in susedi[nod] or novi_sused in susedi_resetka[nod] or novi_sused == nod):        
                                check = 1    
    
                        susedi[nod].remove(sused)
                        susedi[nod].append(novi_sused)
                        susedi[sused].remove(nod)
                        susedi[novi_sused].append(nod)
                        broj_prepovezanih = broj_prepovezanih + 1 
                        if broj_prepovezanih ==  potrebno_prepovezanih:
                            break
        else:
            continue
        break
        
                    
    print('broj prepovezanih u prvom krugu: ',broj_prepovezanih, '  /  ', potrebno_prepovezanih)
    
    #susedi koji su ostali od inicijalne resetke
    neprepovezani_susedi  = []
    for nod in range(L*L):
        neprepovezani_susedi.append(intersection(susedi[nod],susedi_resetka[nod]))
    #--------------------------------------------------------------------------
    #drugi krug prepovezivanja
    if broj_prepovezanih < potrebno_prepovezanih:   
        print('Nedostaje', potrebno_prepovezanih - broj_prepovezanih,' suseda')
        
        while broj_prepovezanih != potrebno_prepovezanih:
            
            nod = random.randrange(0, N)
            if len(neprepovezani_susedi[nod]) > 0 :
                sused = random.choice(neprepovezani_susedi[nod])
             
                if len(susedi[sused]) > 2 :        
                    check = 0
                    while check==0:
                        novi_sused = random.randrange(0, N)
                        if not (novi_sused in susedi[nod] or novi_sused in susedi_resetka[nod] or novi_sused == nod ):        
                            if len(susedi[sused])> 2:
                                check = 1 
                    
                    susedi[nod].remove(sused)
                    neprepovezani_susedi[nod].remove(sused)
                    susedi[nod].append(novi_sused)
                    susedi[novi_sused].append(nod)
                    susedi[sused].remove(nod)
                    neprepovezani_susedi[sused].remove(nod)
                    broj_prepovezanih = broj_prepovezanih + 1
                    #print(broj_prepovezanih)
        print('kraj prepovezivanja')
    else:
        print('Ima ih više od p*broj_linkova ili jednako:', broj_prepovezanih)
        

    #Ising Glauber dinamika
    #--------------------------------------------------------------------------
    #dodavanje spinova
    lattice = np.ones((N,), dtype=int)
    minus_spin = 0
    while minus_spin != N/2:
        #random_lattice_field = np.random.randint(0, N)
        random_lattice_field = int(N * random.random())
        
        
        if lattice[random_lattice_field] != -1:
            lattice[random_lattice_field] = -1
            minus_spin += 1
    #--------------------------------------------------------------------------
    #Monte Carlo
    for step in range(1, time+1):
        for every_spin in range(N):
            #random spin
#           spin = np.random.randint(0, N)
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
    
    #--------------------------------------------------------------------------
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
#------------------------------------------------------------------------------
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
