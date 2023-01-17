import itertools
import numpy as np
from numpy import pi

#QFT E INVERSE QFT
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


#CALCOLO PERMUTAZIONI
#           
#funzione che a partire da un insieme di numeri crea tutte le possibili combinazioni di coppie (no coppie simmetriche) 
def riempi_lista (array_numeri):
    
    lista_vettori = []
    for combination in itertools.combinations(array_numeri, 2):
        lista_vettori.append(combination)

    array_vettori = np.array(lista_vettori) #array from list
    #MODIFICARE IN MODO DA FISSARE IL DTYPE

    return array_vettori


#phase
def tk(j,k):
    tk = -2*(pi**2)*k/(2**j) + (pi**2)*k/(2**(2*j-1))
    return tk

def tT(j,N,T):
    tT = 2*(N**2)*T/2**(j+2) - (N**2)*T/(2**(2*j+1))
    return tT

def pk(j1,j2,k):
    pk = 2*(pi**2)*k/2**(j1+j2-1)
    return pk

def pT(j1,j2,N,T):
    pT = - 2*(N**2)*T/2**(j1+j2+1)
    return pT



#SINGOLA ITERAZIONE
#
#funzione che applica una singola volta l'algoritmo 
def iteration(qc, n, N, k, T, label, vettori, vettori_united):

    #qft e passo allo spazio delle posizioni angolari
    qft_rotations(qc, n)   #without swaps
    qc.barrier(range(n))

    #applico U_k [come decomposta nel paper in un control phase e due phase shift su ogni coppia di qubit (q0q1, q0q2, q1q2)]
    #
    #control-phase:
    for i in vettori:#vettori = [[0,1], [0,2], [1,2]
        qc.cp(pk(i[0]+1,i[1]+1,k), i[0], i[1]) #(theta, control qubit, target qubit)  Perform a phase rotation if both qubits are in the |1,1> state
    """qc.cp(pk(1,3), 0, 2) 
       qc.cp(pk(1,2), 0, 1)  #come dovrebbero essere
       qc.cp(pk(2,3), 1, 2)"""
    #
    #phase shift:
    for qubit in label:
        qc.p(tk(qubit+1,k), qubit)
    qc.barrier(range(n))

    #qft inversa e torno allo spazio dei momenti
    qft_dagger(qc, n) #no swap
    qc.barrier(range(n))

    #applico U_T 
    #
    #control-phase
    for i in range(n):
        qc.cp(pT(vettori_united[i][0]+1,vettori_united[i][1]+1,N,T), vettori_united[i+n][0], vettori_united[i+n][1])
    """
    qc.cp(pT(3,2), 0, 1) 
    qc.cp(pT(1,3), 0, 2) #come dovrebbe essere
    qc.cp(pT(1,2), 1, 2)"""
    #
    #phase
    for qubit in label:
        qc.p(tT(n-qubit,N,T), qubit)
    qc.barrier(range(n))

    return


