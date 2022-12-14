#QUESTO E' IL CODICE IN CUI HO AUTOMATIZZATO IL PROCESSO 
#QUI PUOI APLICARE IL CIRCUITO A N QUBIT





# importing Qiskit
from tkinter.tix import X_REGION
from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit, assemble, Aer, IBMQ, execute, transpile
from qiskit.providers.aer import AerSimulator #particolare simulatore di circuiti quantistici
from qiskit.tools.monitor import job_monitor
from qiskit.circuit.library import QFT
from qiskit.providers.ibmq import least_busy
from qiskit.visualization import plot_histogram, plot_bloch_multivector
import matplotlib.pyplot as plt 

#importing math
import numpy as np
from numpy import pi

from itertools import permutations


#Quantum fourier trasform e inversa
def qft_rotations(circuit, n):
    """Performs qft on the first n qubits in circuit (without swaps)"""
    if n == 0: # Exit function if circuit is empty
        return circuit
    n -= 1 # Indexes start from 0
    circuit.h(n) # Apply the H-gate to the most significant qubit
    for qubit in range(n):
        # For each less significant qubit, we need to do a
        # smaller-angled controlled rotation: 
        circuit.cp(pi/2**(n-qubit), qubit, n)
    # At the end of our function, we call the same function again on
    # the next qubits (we reduced n by one earlier in the function)
    qft_rotations(circuit, n)
    
def swap_registers(circuit, n):
    for qubit in range(n//2): #DIVIDE E ARROTONDA AL PIU' PICCOLO INTERO
        circuit.swap(qubit, n-qubit-1)
    return circuit

def qft(circuit, n):
    """QFT on the first n qubits in circuit"""
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit

def qft_dagger (circuit, n):
    """n-qubit QFTdagger the first n qubits in circ"""
    #for qubit in range(n//2): # // divistion that rounds decimals down to the nearest whole number
    #    circuit.swap(qubit, n-qubit-1)
    #NON FACCIO GLI SWAP -> ALL'USCITA DA QFT_DAGGER TRATTO q0 COME q2 E VICEVERSA
    for j in range(n):
            for m in range(j):
                circuit.cp(-pi/float(2**(j-m)), m, j) # ** operatore potenza
            circuit.h(j)


#definisco i parametri del circuito 
#oss. scelti in modo che ci si trovi in regime caotico (difusione del momento) e tale da
#esibire il piccco di localizzazione dopo una singola iterazione della mappa
n = input("Please enter the number of qubit:\n")
n = int(n)
N = 2**n
K = 1.5
L = 7
T = 2*pi*L/N
k = K/T

#definisco le fasi usate dalle varie porte (phase-shift e control phase shift)
def tk(j):
    tk = -2*(pi**2)*k/(2**j) + (pi**2)*k/(2**(2*j-1))
    return tk

def tT(j):
    tT = 2*(N**2)*T/2**(j+2) - (N**2)*T/(2**(2*j+1))
    return tT

def pk(j1,j2):
    pk = 2*(pi**2)*k/2**(j1+j2-1)
    return pk

def pT(j1,j2):
    pT = - 2*(N**2)*T/2**(j1+j2+1)
    return pT


#funzione che a partire da un insieme di numeri crea tutte le possibili combinazioni di coppie (coppie simmetriche non sono contemplate)
def riempi_lista (lista_vettori, lista_numeri, n):

    for i in range(n): #ciclo sugli indici dellla lista_numeri crescente

        #ciclo sugli indici dellla lista_numeri decrescente e che si arresta quando j=i
        for j in range (n-1, i, -1): # (start, stop, incremento ad ogni ciclo)

            lista_vettori.append( [ lista_numeri[i], lista_numeri[j] ] )


#funzione che applica una singola volta l'algoritmo 
def iteration(qc, n, vettori, vettori_reversed, vettori_united):

    #qft e passo allo spazio delle posizioni angolari
    qft_rotations(qc, n)   #without swaps
    qc.barrier(range(n))

    #applico U_k come decomposta nel paper in un control phase e due phase shift su ogni coppia di qubit (q0q1, q0q2, q1q2)
    #control-phase:
    for i in vettori:
        qc.cp(pk(i[0]+1,i[1]+1), i[0], i[1]) #(theta, control qubit, target qubit)  Perform a phase rotation if both qubits are in the |1,1> state
    """qc.cp(pk(1,3), 0, 2) 
       qc.cp(pk(1,2), 0, 1)  #come dovrebbero essere
       qc.cp(pk(2,3), 1, 2)"""

    #phase:
    for qubit in X:
        qc.p(tk(qubit+1), qubit)
    qc.barrier(range(n))

    #qft inversa e torno allo spazio dei momenti
    qft_dagger(qc, n) #no swap
    qc.barrier(range(n))

    #applico U_T 
    #control-phase
    for i in range(n):
        qc.cp(pT(vettori_united[i][0]+1,vettori_united[i][1]+1), vettori_united[i+n][0], vettori_united[i+n][1])
    """
    qc.cp(pT(3,2), 0, 1) 
    qc.cp(pT(1,3), 0, 2) #come dovrebbe essere
    qc.cp(pT(1,2), 1, 2)"""

    #phase
    for qubit in range (n):
        qc.p(tT(n-qubit), qubit)
    qc.barrier(range(n))

    # rappresento le misure dei vari qubit rispetto sigma_z (parametrizzati nella base dei momenti):
    qc.measure(range(n), range(n))

    return



#definisco il circuito (qubit, bit classici)
qc = QuantumCircuit(n,n)

qc.x(2) #momento iniziale piccato su |001>

# definisco e riempio le liste che conterranno label qubit
X = [] 

for i in range(n):
    X.append(i) #X = [0,1,2,....,n-1]

X_reversed = X
X_reversed.reverse() #X_reversed = [n-1,...,1,0]


#definisco le liste che conterranno le permutazioni delle coppie di qubit
vettori = []
vettori_reversed = []

riempi_lista(vettori, X, n) #vettori = [[0,2], [0,1], [1,2]

riempi_lista(vettori_reversed, X_reversed, n) #vettori_reversed = [[0,2], [2,1], [1,0]


vettori_united = vettori_reversed
vettori_united.extend(vettori) #vettori_reversed = [ [2,0], [2,1], [1,0], [0,2], [0,1], [1,2] ]



#applico l'algoritmo
iteration(qc, n, vettori, vettori_reversed, vettori_united)


# rappresento le misure dei vari qubit rispetto sigma_z (parametrizzati nella base dei momenti):
qc.measure(range(n), range(n))


#disegno il circuito
qc.draw(output="mpl")
plt.show()


#Simulo il circuito
backend = AerSimulator() #inizializzo un particolare simulatore

qc_compiled = transpile(qc, backend) #compilo il circuito

job_sim = backend.run(qc_compiled, shots=8192) #testa il circuito 8192 volte e salva i risultati delle misure sui bit classici

result_sim = job_sim.result()

counts = result_sim.get_counts(qc_compiled)

#mostro i risultati
plot_histogram(counts)
plt.show()
