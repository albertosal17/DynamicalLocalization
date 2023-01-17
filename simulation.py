from qiskit.providers.aer import AerSimulator #particolare simulatore di circuiti quantistici
from qiskit.tools.visualization import circuit_drawer
from qiskit import QuantumCircuit, IBMQ, transpile

from copy import deepcopy
from fnmatch import filter
import os
import matplotlib.pyplot as plt
import numpy as np


import quantumCircuit
import plot


#SIMULAZIONE BACKEND
#
#funzione che permette di simulare il circuito su una specifica backend impostata
def simulation(backendKeyword, initial_qc, n, N, k, T, label, vettori, vettori_united, iter_list, shots, directory_path):

    for i in iter_list:

        qc = deepcopy(initial_qc)

        iter = i

        for j in range(iter):
            quantumCircuit.iteration(qc, n, N, k, T, label, vettori, vettori_united)

        # misura sigma_z dopo le varie iterazioni
        qc.measure(range(n), range(n))

        
        if (backendKeyword =='noiseless'):

            
            filename = directory_path+'\\'+str(n)+'_'+backendKeyword+str(iter)+'iter'

            # Plot the circuit
            qc.draw(output="mpl")
            # Save the figure to a file
            plt.savefig(filename+"_qc"'.png')
            plt.clf()
            #plt.gca()

            #simulation
            backend=AerSimulator()
            qc_compiled = transpile(qc, backend) #compilo il circuito
            job_sim = backend.run(qc_compiled, shots=shots) #testa il circuito 8192 volte e salva i risultati delle misure sui bit c
            result_sim = job_sim.result()
            counts = result_sim.get_counts(qc_compiled)

            print("eseguita simulazione su ", str(backend), "per ", iter , "iterazioni della mappa con", shots, "tentativi")
            
            #salvo risultati in un nuovo file
            with open(filename+'.json', 'w') as file:
                # Write some data to the file
                file.write(str(counts))
            print("dati sono stati salvati in ", filename)

            plot.plot(counts, shots, filename,n,N,iter,backendKeyword)
        

        if (backendKeyword == 'fakeLima'):

            filename = directory_path+'\\'+str(n)+'_'+backendKeyword+str(iter)+'iter'

            #RICONTROLLARE: DA PROBLEMI
            # Plot the circuit
            #qc.draw(output="mpl")
            # Save the figure to a file
            #plt.savefig(filename+"_qc"'.png')
            #plt.clf()
            #plt.gca()

            from qiskit.providers.fake_provider import FakeLimaV2
            backend=FakeLimaV2()
            qc_compiled = transpile(qc, backend) #compilo il circuito
            job_sim = backend.run(qc_compiled, shots=shots) #testa il circuito 8192 volte e salva i risultati delle misure sui bit classici
            result_sim = job_sim.result()
            counts = result_sim.get_counts(qc_compiled)

            print("eseguita simulazione su ", str(backend), "per ", iter , "iterazioni della mappa con", shots, "tentativi")

            #salvo risultati in un nuovo file
            with open(filename+'.json', 'w') as file:
                # Write some data to the file
                file.write(str(counts))
            print("dati sono stati salvati in ", filename)

            plot.plot(counts, shots, filename,n,N,iter,backendKeyword)

    
        if (backendKeyword == 'lima'):

                from qiskit import IBMQ
                #tokenUSC
                IBMQ.enable_account('df77ce8fbc3c2ca8fabd89e18f52496647559be8ef2d1d88fdbe6f8eb55ae143e92912be4a8cfb35ead3c1ca38edf982fbd5dd98e4afea404d4edd4b10908772') #If you do not have your account saved and do not want to save it
                IBMQ.providers()    # List all available providers
                # Replace YOUR_HUB, YOUR_GROUP, and YOUR_PROJECT with the actual values for your provider
                provider = IBMQ.get_provider(hub='ibm-q-research', group='uni-south-cali-1', project='main')
                #inizializzo particolare computer
                backend = provider.get_backend('ibmq_lima')
                #testo il circuito
                qc_compiled = transpile(qc, backend) #compilo il circuito
                job_sim = backend.run(qc_compiled, shots=shots) #testa il circuito 8192 volte e salva i risultati delle misure sui bit classici�
                result_sim = job_sim.result()
                counts = result_sim.get_counts()
                print("eseguita simulazione su ", str(backend), "per ", iter , "iterazioni della mappa con", shots, "tentativi")
                print("i dati sono reperibili al sito di IBMQ")

    return


