import matplotlib.pyplot as plt
import numpy as np
import json
from fnmatch import filter
import os


# CODICE SE DEVI PLOTTARE FILE DA LIMA CONTENUTI IN UNA CARTELLA
def plotLima(n,N,backendKeyword, directory_path):
    #ik = input("n_qubit oppure n_iter?: ")  
    ik = 'n_qubit'
    
    #accedo alla cartella che contiene i risultati del run sul quantum computer e seleziono solo i file desiderati
    directory = "C:\\Users\\ASUS\\Desktop\\TESI\\data\\"+ik+"\\"+backendKeyword+"\\"
    # Get the list of all files in directory tree at given path
    files = list(os.walk(directory))[0][2]
    # Filter the list of files to only include .json files
    json_files = filter(files, '*.json')
    filter_word = str(n)+"_lima"
    filtered_files = [file for file in json_files if filter_word in file]
    print("filtered files: ", filtered_files)

    if(ik == 'n_iter'):

        iter_list = [] 

        #accedo ai file selezionati, mi salvo i conteggi e plotto
        for i in filtered_files:
            
                filename = directory+i
            
                title= i

                if(i[i.find("iter")-1]==str(0)):
                    print("ECCOLO LA")
                    iter = int(i[i.find("iter")-2:i.find("iter")]) #iter=10
                    print("iter",iter)
                    iter_list.append(iter)


                else: #iter != 10
                    iter = int(i[i.find("iter")-1])
                    print("iter",iter)
                    iter_list.append(iter)

                #importo i dati contenuti dentro al file
                with open(filename) as fh: #with ti consente di non dovere chiudere manualmente il file alla fine 
                    data = json.load(fh) #data sarà un dictonary (lista di coppie label-elemento)

                #mi salvo a parte i conteggi delle misure 
                counts = data["results"][0]["data"]["counts"] #counts = {"0x0": 1441, "0x1": 606, "0x2": 559, "0x3": 616, "0x4": 3543, "0x5": 575, "0x6": 603, "0x7": 249}
                shots = data["results"][0]["shots"] #shots = 8192

                #ridefinisco opportunamente il dictionary che contiene le misure al fine di plottare
                binKey_counts = {}
                for idx, cnt in counts.items(): 
                    binKey_counts[ np.binary_repr( int(idx, base=0), n) ] = cnt #la key viene convertita in binario dopo un passaggio intermedio in cui è convertita in decimale
                print("binKey_counts", binKey_counts)

                #copio il file di dati nella nuova cartella
                new_filename = directory_path+'\\'+str(n)+'_'+backendKeyword+str(iter)+'iter'
                with open(new_filename+'.json', 'w') as file:
                # Write some data to the file
                    file.write(str(binKey_counts))
                print("il file di dati"+ filename +" è stato copiato in ", new_filename)
            
                #passo alla rappresentazione decimale degli stati e alle probabilità al posto dei conteggi
                new_counts_intermediate = {}
                for key in binKey_counts:
                    new_counts_intermediate[int(key,2)-N/2]=(binKey_counts[key])/shots

                #riscrivo il diionario in ordine crescente rispetto le keys
                new_counts = sorted(new_counts_intermediate.keys())
                # Create a new dictionary with the sorted keys and their corresponding values
                new_counts = {key: new_counts_intermediate[key] for key in new_counts}
                print("dati con label in decimale e probabilità:", new_counts)
            
                plt.plot(new_counts.keys(), new_counts.values(), 'o--', label=str(n)+'_'+backendKeyword+str(iter)) #matplotlib.pyplot.plot(lista valori ascissa, lista valori ordinata, stile linea)  
                plt.xticks(range(int(min(new_counts.keys())), int(max(new_counts.keys()))+1))
                plt.grid()
                plt.title(title)
                plt.savefig(new_filename+'.png',dpi=300)
                print("generato plot da file ", new_filename)
    
        return iter_list
    
    if(ik == 'n_qubit'):

        iter=1
        iter_list=[iter]

        for i in filtered_files:
            
                filename = directory+i

                title= i
                    

                #importo i dati contenuti dentro al file
                with open(filename) as fh: #with ti consente di non dovere chiudere manualmente il file alla fine 
                    data = json.load(fh) #data sarà un dictonary (lista di coppie label-elemento)

                #mi salvo a parte i conteggi delle misure 
                counts = data["results"][0]["data"]["counts"] #counts = {"0x0": 1441, "0x1": 606, "0x2": 559, "0x3": 616, "0x4": 3543, "0x5": 575, "0x6": 603, "0x7": 249}
                shots = data["results"][0]["shots"] #shots = 8192

                #ridefinisco opportunamente il dictionary che contiene le misure al fine di plottare
                binKey_counts = {}
                for idx, cnt in counts.items(): 
                    binKey_counts[ np.binary_repr( int(idx, base=0), n) ] = cnt #la key viene convertita in binario dopo un passaggio intermedio in cui è convertita in decimale
                print("binKey_counts", binKey_counts)

                #copio il file di dati nella nuova cartella
                new_filename = directory_path+'\\'+str(n)+'_'+backendKeyword+str(iter)+'iter'
                with open(new_filename+'.json', 'w') as file:
                # Write some data to the file
                    file.write(str(binKey_counts))
                print("il file di dati"+ filename +" è stato copiato in ", new_filename)
            
                #passo alla rappresentazione decimale degli stati e alle probabilità al posto dei conteggi
                new_counts_intermediate = {}
                for key in binKey_counts:
                    new_counts_intermediate[int(key,2)-N/2]=(binKey_counts[key])/shots

                #riscrivo il diionario in ordine crescente rispetto le keys
                new_counts = sorted(new_counts_intermediate.keys())
                # Create a new dictionary with the sorted keys and their corresponding values
                new_counts = {key: new_counts_intermediate[key] for key in new_counts}
                print("dati con label in decimale e probabilità:", new_counts)
            
                plt.plot(new_counts.keys(), new_counts.values(), 'o--', label=str(n)+'_'+backendKeyword+str(iter)) #matplotlib.pyplot.plot(lista valori ascissa, lista valori ordinata, stile linea)  
                plt.xticks(range(int(min(new_counts.keys())), int(max(new_counts.keys()))+1))
                plt.grid()
                plt.yscale("log")################
                plt.title(title)
                plt.savefig(new_filename+'.png',dpi=300)
                print("generato plot da file ", new_filename)
    
        return iter_list
    

