
import json
import numpy as np
import matplotlib.pyplot as plt


def plot (counts, shots, filename,n, N, iter, backendKeyword):
            
    with open(filename+'.json') as fh: #with ti consente di non dovere chiudere manualmente il file alla fine 
        json_string = fh.read()
        fixed_string = json_string.replace("'", '"')
        data = json.loads(fixed_string) #data sarà un dictonary (lista di coppie label-elemento)
        print("dati da file:", filename, ": ", data)

    title= filename

    #passo alla rappresentazione decimale degli stati e alle probabilità al posto dei conteggi
    new_counts_intermediate = {}
    for key in counts:
        new_counts_intermediate[int(key,2)-N/2]=(counts[key])/shots
    
    #riscrivo il diionario in ordine crescente rispetto le keys
    new_counts = sorted(new_counts_intermediate.keys())
    # Create a new dictionary with the sorted keys and their corresponding values
    new_counts = {key: new_counts_intermediate[key] for key in new_counts}
    print("dati con label in decimale e probabilità:", new_counts)

    plt.plot(new_counts.keys(), new_counts.values(), 'o--', label=str(n)+'_'+backendKeyword+str(iter)) #matplotlib.pyplot.plot(lista valori ascissa, lista valori ordinata, stile linea)  
    plt.xticks(range(int(min(new_counts.keys())), int(max(new_counts.keys()))+1))
    plt.grid()
    plt.title(title)
    plt.yscale("log")####################
    plt.savefig(filename+'.png',dpi=300, )
    print("generato plot da file ", filename)

    return
          



