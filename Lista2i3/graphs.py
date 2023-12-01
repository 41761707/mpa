import sys
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.stats import kurtosis

def main():
    # Wczytanie danych z pliku tekstowego
    avg_p = []
    maxs_p = []
    mins_p = []
    reps = []
    with open('czas.txt', 'r') as file:
        for line in file:
            values = []
            line_content = line.split(" : ")
            rep = line_content[0]
            observations = list(line_content[1].split(';'))[:-1]
            for observation in observations:
                values.append(float(observation))
            reps.append(int(rep))
            #kurtoza = kurtosis(values, fisher=True) 
            #print(kurtoza)
            avg_p.append(np.mean(values))
            #var = np.var(values)
            #k = math.sqrt(var) / (1 - 0.75)
            #mins_k.append(np.mean(values)-k)
            #maxs_k.append(np.mean(values)+k)
            mins_p.append(min(values))
            maxs_p.append(max(values))
    '''
    avg_k = []
    maxs_k = []
    mins_k = []
    with open('KruskalCzasyNormal.txt', 'r') as file:
        for line in file:
            values = []
            line_content = line.split(" : ")
            rep = line_content[0]
            observations = list(line_content[1].split(';'))[:-1]
            for observation in observations:
                values.append(float(observation))
            avg_k.append(np.mean(values))

            #mins_k.append(np.mean(values)-np.std(values))
            #axs_k.append(np.mean(values)+np.std(values))
            mins_k.append(min(values))
            maxs_k.append(max(values)
    '''

    sqrt_n = []
    for n in range(10, 1000, 25):
        sqrt_n.append(7*math.log(n))

    new_list = []
    for i in range(len(reps)):
        new_list.append(avg_p[i]/sqrt_n[i])
    # Utworzenie wykresu
    #plt.plot(reps, new_list, linestyle = '--', color = 'y', label = 'AVG/7*log(n)')
    #plt.plot(reps, sqrt_n ,linestyle = '--', color='y', label = '7*log(n)')
    plt.plot(reps,avg_p, marker='o', linestyle='-', color='b', label = 'AVG')
    plt.plot(reps,maxs_p, linestyle='--', color='b', label = 'MAX')
    plt.plot(reps,mins_p, linestyle='--', color='b', label = 'MIN')
    #plt.plot(reps,avg_k, marker='o', linestyle='-', color='r')
    #plt.plot(reps,maxs_k, linestyle='--', color='r')
    #plt.plot(reps,mins_k, linestyle='--', color='r')
    plt.title('Czas wykonania algorytmu')
    plt.xlabel('Rozmiar grafu')
    plt.ylabel('Czas')
    plt.grid(True)
    plt.legend()
    plt.savefig('graphs_normal/Czas1.jpg')
    plt.clf()

if __name__ == '__main__':
    main()