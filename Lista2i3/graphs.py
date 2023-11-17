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
    with open('PrimCzasyNormal.txt', 'r') as file:
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

            mins_p.append(np.mean(values)-np.std(values))
            maxs_p.append(np.mean(values)+np.std(values))
            #mins_p.append(min(values))
            #maxs_p.append(max(values))

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
            maxs_k.append(max(values))

    n_log_n = []
    for n in range(1,37):
        n_log_n.append(n*math.log(n,10))

    # Utworzenie wykresu
    #plt.plot(n_log_n,marker='o',linestyle = '-', color='y')
    plt.plot(reps,avg_p, marker='o', linestyle='-', color='b')
    plt.plot(reps,maxs_p, linestyle='--', color='b')
    plt.plot(reps,mins_p, linestyle='--', color='b')
    #plt.plot(reps,avg_k, marker='o', linestyle='-', color='r')
    #plt.plot(reps,maxs_k, linestyle='--', color='r')
    #plt.plot(reps,mins_k, linestyle='--', color='r')
    plt.title('Prim rozkład normalny')
    plt.xlabel('Rozmiar grafu')
    plt.ylabel('Czas')
    plt.grid(True)

    # Wyświetlenie wykresu
    plt.savefig('graphs_normal/PrimCzasOdchylenie1Normal.jpg')
    plt.clf()

if __name__ == '__main__':
    main()