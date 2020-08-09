# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 13:03:02 2019

@author: Acer
"""
import random
import time
import matplotlib.pyplot as plt
import numpy as np

pocetak = time.time()
#verovatnoca povezivanja
p = 0.6

#dimenije resetke
L = 50
k = 4 #broj suseda
N = L*L

#==============================================================================
#susedni nodovi
def gore(i):
    if i//L == 0:
        return ((i-L)+L*L)
    else:
        return (i-L)
    
def dole(i):
    if i//L == L-1:
        return(i%L)
    else:
        return (i+L)
    
def levo(i):
    if i%L == 0:
        return(i+L-1)
    else:
        return (i-1)
    
def desno(i):
    if i%L == L-1:
        return(i-(L-1))
    else:
        return (i+1)
      
def ishod(verovatnoca):
    return random.random() < verovatnoca

def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 
#==============================================================================
susedi = []
susedi_resetka = []
broj_linkova = (N*2) #ili ipak L*L*4
#==============================================================================
#susedi na početku
for i in range (L*L):
    susedi.append([gore(i),dole(i),desno(i),levo(i)])
    susedi_resetka.append([gore(i),dole(i),desno(i),levo(i)])

#==============================================================================
#prvi krug prepovezivanja
brojac = 0
broj_prepovezanih = 0
for nod in range(L*L):
    linkovi = intersection(susedi[nod],susedi_resetka[nod])
    for sused in linkovi:
        if sused > nod:
            if ishod(p):
                check = 0
                while check == 0:
                    novi_sused = random.randrange(0,L*L)
                    if not (novi_sused in susedi[nod] or novi_sused in susedi_resetka[nod] or novi_sused == nod):        
                        check = 1    
                if len(susedi[sused])> 2:
                    susedi[nod].remove(sused)
                    susedi[nod].append(novi_sused)
                    susedi[sused].remove(nod)
                    susedi[novi_sused].append(nod)
                    broj_prepovezanih = broj_prepovezanih + 1 
                    if broj_prepovezanih ==  int(broj_linkova*p):
                        break
    else:
        continue
    break
    
                
print('broj prepovezanih u prvom krugu: ',broj_prepovezanih, '  /  ', broj_linkova*p)
#==============================================================================
#susedi koji su ostali od inicijalne resetke
neprepovezani_susedi  = []
for nod in range(L*L):
    neprepovezani_susedi.append(intersection(susedi[nod],susedi_resetka[nod]))

#===============================================================================
#drugi krug prepovezivanja
if broj_prepovezanih < broj_linkova*p:   
    print('Nedostaje', broj_linkova*p - broj_prepovezanih,' suseda')
    
    while broj_prepovezanih != broj_linkova*p:
        
        nod = random.randrange(0,L*L)
        if len(neprepovezani_susedi[nod]) > 0 :
            sused = random.choice(neprepovezani_susedi[nod])
         
            if len(susedi[sused]) > 2 :        
                check = 0
                while check==0:
                    novi_sused = random.randrange(0,L*L)
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
    print('Ima ih više od p*broj_linkova:', broj_prepovezanih)
    
#============================================================================== 
#broj linkova
broj_linkova = 0
for element in susedi:
    broj_linkova = broj_linkova + len(element)
print('broj linkova:', broj_linkova,'  /  ',L*L*4)
#==============================================================================
#histogram mreze
    
histogram = []  
for i in range(len(susedi)):
    histogram.append(len(susedi[i]))

number_bins =range(min(histogram),max(histogram),1)

#n, bins, patches = plt.hist(histogram, number_bins, facecolor='gray')

hist, bins = np.histogram(histogram, number_bins)

hist = [ float(n)/(L*L) for n in hist]

center = (bins[:-1]+bins[1:])/2
width = 1*(bins[1]-bins[0])
plt.bar(center, hist, align = 'center', width = width,  facecolor='gray')
plt.xlabel('Broj linkova')
plt.ylabel('Broj nodova/ukupan nodova')
plt.xlim(1,max(histogram))
plt.text(1.5, 0.15, f'p = {p}')
plt.title('')
plt.show()

#==============================================================================      

#vreme
kraj = time.time()
print('vreme prepovezivanja: ', kraj - pocetak)
#==============================================================================


broj_neprepovezanih = 0
for nod in range(L*L):
    broj_neprepovezanih = broj_neprepovezanih + len(intersection(susedi[nod],susedi_resetka[nod]))

print('broj onih linkova koji su ostali isti:',broj_neprepovezanih)
print('broj prepovezanih linkova:', broj_prepovezanih)


if (broj_linkova - broj_neprepovezanih)/2 == broj_prepovezanih :
    print('svaka cast')
else: print('ubise ili vidi da li ih ima vise u p')