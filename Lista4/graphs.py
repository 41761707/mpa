import sys
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.stats import kurtosis

def main():
    # Wczytanie danych z pliku tekstowego
    avg_p = []
    maxs_p = []
    maxs_k = []
    mins_k = []
    avg_k = []
    mins_p = []
    reps = []
    values = []
    values_k = []
    current_rep = 100
    with open('wyniki_normal.txt', 'r') as file:
        for line in file:
            line_content = line.split(":")
            rep = int(line_content[0].strip())
            t = list(line_content[1].split(';'))[3]
            y = list(line_content[1].split(';'))[5]
            values.append(float(t))
            values_k.append(float(y))
            if rep != current_rep:
                current_rep = rep
                reps.append(int(rep))
                avg_p.append(np.mean(values))
                avg_k.append(np.mean(values_k))
                var = np.var(values)
                k = math.sqrt(var) / (1 - 0.7)
                #mins_p.append(np.mean(values)-k)
                #maxs_p.append(np.mean(values)+k)


                mins_p.append(min(values))
                maxs_p.append(max(values))
                mins_k.append(min(values_k))
                maxs_k.append(max(values_k))
                values = [float(t)]
                values_k = [float(y)]
                #if current_rep == 1000:
                #    break

    n_log_n = []
    for n in range(100, 3450, 25):
        #sqrt_n.append(1.2 * 10**(-6) * n *math.log(n))
        n_log_n.append(1.2 * 10**(-6)* n * math.log(n))

    #new_list = []
    #for i in range(len(reps)):
    #    new_list.append(avg_p[i]/sqrt_n[i])
    # Utworzenie wykresu
    #plt.plot(reps, n_log_n ,linestyle = '--', color='y', label = '1.2 * 10^(-6) * n*log(n)')
    plt.plot(reps,avg_p, marker='o',markevery=5, linestyle='-', color='b', label = 'ALG')
    #plt.plot(reps,avg_k,linestyle='--', color='b', label = 'N^2')
    plt.plot(reps,maxs_p, linestyle='--', color='b', label = 'MAX')
    plt.plot(reps,mins_p, linestyle='--', color='b', label = 'MIN')
    plt.title('Czas wykonania algorytmu')
    plt.xlabel('Rozmiar instancji')
    plt.ylabel('Czas')
    plt.grid(True)
    plt.legend()
    plt.savefig('graphs/exp/Comp.png')
    plt.clf()

if __name__ == '__main__':
    main()