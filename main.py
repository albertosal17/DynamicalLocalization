# importing Qiskit
from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit

import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
import os
#importing CODICE
import simulation
from quantumCircuit import riempi_lista
from plotLima import plotLima

#creo la cartella dove verranno salvati i risultati della simulazione
from datetime import datetime
# Get current date and hour
now = datetime.now()
date_string = now.strftime('%Y%m%d')
hour_string = now.strftime('%H')
minute_string = now.strftime('%M')
# Create the directory path
global directory_path
directory_path = 'C:\\Users\\ASUS\\Desktop\\TESI\\data\\test\\' + date_string + hour_string + minute_string
# Create the directory
os.mkdir(directory_path)

backends = ['noiseless']
"""
print("Quali backend si vogliono usare? [backendKeyword: noiseless, fakeLima, lima - stop: per terminare]:")
while True:
    user_input = input("Inserisci una backendKeyword: ")
    if user_input == "stop":
        break
    else:
        backends.append(user_input)
print(backends)
"""

for backendKeyword in backends:

    if (backendKeyword=="lima"):
        #s = input("vuoi runnare su lima[run] oppure plottare da file di risultati di lima[plot]?: ") 
        s = "plot"

        if(s=="plot"):
            import sys

            #n= int(input("numero qubit: "))
            n_list=[3,4,5]
            for n in n_list:
                N = 2**n
                print("numero qubit=",n)

                iter_list=plotLima(n,N,backendKeyword, directory_path)


            plt.legend()
            plt.title(str(n_list)+' qubit per '+str(iter_list)+' iterazioni')
            plt.savefig(directory_path+'\\''ALL_'+str(n_list)+'_'+str(iter_list)+'.png',dpi=300)
            print("end")
            sys.exit()

    #
    #oss. scelti in modo che ci si trovi in regime caotico (difusione del momento) e tale da
    #esibire il piccco di localizzazione dopo una singola iterazione della mappa
    #n = int(input("numero qubit: "))
    n_list=[5]

    for n in n_list:

        N = 2**n
        K = 1.5
        L = 7
        T = 2*pi*L/N
        k = K/T


        #CIRCUITO
        #
        #definisco il circuito (qubit, bit classici)
        qc = QuantumCircuit(n,n)

        qc.x(n-1) #momento iniziale piccato su |001>

        # definisco e riempio gli array che conterranno label qubit
        label = np.arange(n) #label = [0,1,2,....,n-1]
        label_reversed = np.arange(n-1,-1,-1)  #label_reversed = [n-1,...,1,0]
        #definisco gli array che conterranno le permutazioni delle coppie di qubit
        vettori = riempi_lista(label) #vettori = [[0,1], [0,2], [1,2]
        vettori_reversed = riempi_lista(label_reversed) #vettori_reversed = [[2,1], [2,0], [1,0]]
        vettori_united = np.append(vettori_reversed,vettori,axis=0) #vettori_united = [ [2,1], [2,0], [1,0], [0,1], [0,2], [1,2] ])

        #definisco quante iterazioni della mappa voglio provare
        iter_list = [1,2,3,5,10]
        print("verranno eseguite il seguente numero di iterazioni: ", iter_list)


        #SIMULAZIONE
        shots = 8192
        simulation.simulation(backendKeyword, qc, n, N, k, T, label, vettori, vettori_united, iter_list, shots,directory_path)

plt.legend()
plt.title(str(n)+' qubit per '+str(iter_list)+' iterazioni')
plt.yscale("log")###############
plt.savefig(directory_path+'\\''ALL_'+str(n)+'_'+str(iter_list)+'.png',dpi=300)
print("end")






#COMANDI UTILI

#plt.show()
# backends = provider.backends()   
#disegno il circuito
#qc.draw(output="mpl")
#plt.show()