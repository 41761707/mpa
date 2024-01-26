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
    values = []
    current_rep = 0.01
    with open('no_passengers.txt', 'r') as file:
        for line in file:
            line_content = line.split(":")
            rep = float(line_content[0].strip())
            t = int(line_content[1].strip())
            values.append(t)
            if rep != current_rep:
                current_rep = rep
                reps.append(rep)
                avg_p.append(np.mean(values))
                var = np.var(values)
                k = math.sqrt(var) / (1 - 0.7)
                #mins_p.append(np.mean(values)-k)
                #maxs_p.append(np.mean(values)+k)
                mins_p.append(min(values))
                maxs_p.append(max(values))
                values = [t]

    #n_log_n = []
    #for n in range(100, 3450, 25):
    #    #sqrt_n.append(1.2 * 10**(-6) * n *math.log(n))
    #    n_log_n.append(1.2 * 10**(-6)* n * math.log(n))

    #new_list = []
    #for i in range(len(reps)):
    #    new_list.append(avg_p[i]/sqrt_n[i])
    # Utworzenie wykresu
    #plt.hist(values, bins=[x for x in range(5,50)], align='left', rwidth=0.8)
    #plt.plot(reps, n_log_n ,linestyle = '--', color='y', label = '1.2 * 10^(-6) * n*log(n)')
    plt.plot(reps,avg_p, marker='o',markevery=5, linestyle='-', color='b', label = 'ALG')
    #plt.plot(reps,avg_k,linestyle='--', color='b', label = 'N^2')
    plt.plot(reps,maxs_p, linestyle='--', color='b', label = 'MAX')
    plt.plot(reps,mins_p, linestyle='--', color='b', label = 'MIN')
    plt.title('Liczba kółek pasażerów')
    plt.xlabel('x')
    plt.ylabel('Liczba kółek')
    plt.grid(True)
    plt.legend()
    plt.savefig('graphs/no_passengers/wheels.png')
    plt.clf()

if __name__ == '__main__':
    main()