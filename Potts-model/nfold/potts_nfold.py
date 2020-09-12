# -*- coding: utf-8 -*-
"""
Potts model, the n fold method
@author: Nina
"""
import random
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

#dimenzije resetke
L = 50
N = L*L

q = 3
states = [1, 2, 3]

def decision(probability):
    """Do smth with given probability"""
    return random.random() < probability

def class_decision(wk_1, wk_2):
    """Probability of choosing a spin class is proportional to its probability of flipping"""
    if random.random() <= min(wk_1, wk_2):
        return min(wk_1, wk_2)
    else:
        return max(wk_1, wk_2)
   
def remove2(what_to_remove, place):
    """Remove element from list if it exists"""
    if what_to_remove in place:
        place.remove(what_to_remove)
    
def update_class_lists(klasa, spin):
    """Update class lists"""
    if klasa == 1:
        k_1.append(spin)
    elif klasa == 2:
        k_2.append(spin)
    elif klasa == 3:
        nonflippable.append(spin)
    else:
        print('???')
    
def kronecker(i, j):
    """Kronecker delta function"""
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
for j in range(N):
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

#pravljenje resetke
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
print('Resetka napravljena')
print('jedinica ima:', np.count_nonzero(lattice == 1))
print('dvojki ima: ', np.count_nonzero(lattice == 2))
print('trojki ima: ', np.count_nonzero(lattice == 3))

#print('RESETKA: \n', lattice)

#u SPIN_STATES se cuva broj suseda spina u stanju 1,2,3, za svaki spin
SPIN_STATES = []
for spin in range(N):
    N_1 = 0
    N_2 = 0
    N_3 = 0
    for neighbour in links[spin]:
        if lattice[neighbour] == 1:
            N_1 += 1
        elif lattice[neighbour] == 2:
            N_2 += 1
        else:
            N_3 += 1
    SPIN_STATES.append([N_1, N_2, N_3])

#print(SPIN_STATES)

def state_in_majority(state_neighbours):
    majority = max(state_neighbours)
    majorstate = [i+1 for i, j in enumerate(state_neighbours) if j == majority]
    return majorstate

def determine_spin_class(spin):
    """Determine spin class"""
    state_spin = lattice[spin]
    state_neighbours = SPIN_STATES[spin]
    majorstate = state_in_majority(state_neighbours)
    if len(majorstate) == 1 and lattice[spin] == majorstate[0]:
        klasa = 3
        return klasa
        #nije flippable
    else:
        #flippable je i odredjujemo koja je klasa
        klasa = 0 
        hi_pre = -1* state_neighbours[state_spin - 1]
        hi_flip_1 = -1* state_neighbours[state_spin - 2]
        hi_flip_2 = -1* state_neighbours[state_spin - 3]
        #poredimo energ
        if hi_flip_1 <= hi_pre:
            klasa += 1
        if hi_flip_2 <= hi_pre:
            klasa += 1      
        return klasa

#raspodela spinova u klase na pocetku
nonflippable = [] #ne moze se flipovati
k_1 = [] #klasa koja se moze flipovati u jedno stanje
k_2 = [] #klasa koja se moze flipovati u dva stanja

for spin in range(N):
    klasa = determine_spin_class(spin)
    update_class_lists(klasa, spin)
#print('U klasi k1 su: ', k_1, '\nU klasi k2 su: ', k_2, '\nNe mogu se flipovati: ', nonflippable)    

Wk_1 = 1* len(k_1)
Wk_2 = 2* len(k_2)
print('pocinje n fold')

counter = 0
while Wk_1 + Wk_2 != 0:
    #relativna/normirana tezina klasa
    wk_1 = Wk_1/(Wk_1 + Wk_2)
    wk_2 = Wk_2/(Wk_1 + Wk_2)
    
    if class_decision(wk_1, wk_2) == wk_1:
        #odabrana je prva klasa
        spin = random.choice(k_1)
        #odabran je random spin iz klase
        old_orient = lattice[spin]
        h_pre = hi(spin)
        
        #moguc je flip u jedno stanje
        state_neighbours = SPIN_STATES[spin]
        possible_flip_state = state_in_majority(state_neighbours)
        remove2(old_orient, possible_flip_state)
        new_orient = possible_flip_state[0]
        
        #flip, lokalno polje posle flipa
        lattice[spin] = new_orient
        h_posle = hi(spin)
        
        #check, dozvoljeni flipovi koji snizavaju ili ne menjanju energiju
#       if h_posle > h_pre:
#           lattice[spin] = old_orient
        
        #ako je energija ista, vracam na staro stanje sa ver 0.5
        if h_posle == h_pre and decision(0.5):
            lattice[spin] = old_orient
        #ukoliko ne vracam staro stanje, flip se dogodio, update
        else:
            for neighbour in links[spin]:
                SPIN_STATES[neighbour][old_orient - 1] -= 1
                SPIN_STATES[neighbour][new_orient - 1] += 1
                 
                #proveriti klasu komsija
                remove2(neighbour, k_1)
                remove2(neighbour, k_2)
                remove2(neighbour, nonflippable)
                klasa = determine_spin_class(neighbour)
                update_class_lists(klasa, neighbour)
                
                #proveriti klasu spina
                klasa = determine_spin_class(spin)
                remove2(spin, k_1)
                remove2(spin, k_2)
                remove2(spin, nonflippable)
                update_class_lists(klasa, spin)
                
    else:
        #odabrana je druga klasa
        spin = random.choice(k_2)
        #odabran je random spin iz klase
        old_orient = lattice[spin]
        h_pre = hi(spin)
        #bira se random stanje posle flipa, moguca su dva
        for q in states:
            possible_flip_states = [j for j in states if j != old_orient]
        new_orient = random.choice(possible_flip_states)
        #flip, lokalno polje posle flipa
        lattice[spin] = new_orient
        h_posle = hi(spin)
        
        #ako je energija ista, vracam na staro stanje sa ver 0.5
        if h_posle == h_pre and decision(0.5):
            lattice[spin] = old_orient
        else:
            #ukoliko ne vracam staro stanje, flip se sigurno dogodio, update
            for neighbour in links[spin]:
                SPIN_STATES[neighbour][old_orient - 1] -= 1
                SPIN_STATES[neighbour][new_orient - 1] += 1
                
                #proveriti klasu komsija
                remove2(neighbour, k_1)
                remove2(neighbour, k_2)
                remove2(neighbour, nonflippable)
                klasa = determine_spin_class(neighbour)
                update_class_lists(klasa, neighbour)
                #proveriti klasu spina
                klasa = determine_spin_class(spin)
                remove2(spin, k_1)
                remove2(spin, k_2)
                remove2(spin, nonflippable)
                update_class_lists(klasa, spin)
                
    #update broja mogucih flipova po klasama
    Wk_1 = 1* len(k_1)
    Wk_2 = 2* len(k_2)
    counter += 1
    
print(counter)
#==================================================================================       
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

