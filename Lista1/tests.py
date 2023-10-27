import sqlite3
import statistics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def linear_regression(new_price, prices, name):
    data = {
    'Data': [x for x in range(len(prices))],
    'Cena': prices
    }
    df = pd.DataFrame(data)
    X = np.arange(len(df)).reshape(-1, 1)
    y = df['Cena']
    regression = LinearRegression()
    regression.fit(X, y)

    trend = regression.predict(X)

    plt.plot(df['Data'], y, label='Cena')
    plt.plot(df['Data'], trend, label='Trend Ceny', color='red')
    plt.xlabel('Data')
    plt.ylabel('Ceny')
    plt.legend()
    plt.title('Trend Ceny')
    plt.savefig("wykresy/{}_regresja_liniowa".format(name))
    plt.clf()

    indeks_nowej_ceny = len(df)
    predicted_new_price = regression.predict(np.array([[indeks_nowej_ceny]]))[0]

    print("Nowa cena: ", new_price)
    print("Przewidywana cena: ", predicted_new_price)
    if predicted_new_price * 0.75 <= new_price <= predicted_new_price * 1.25: 
        return False
    return True

def zscore(new_price, prices, z, name):
    mean = statistics.mean(prices)
    variance = statistics.variance(prices)
    std = statistics.stdev(prices)
    ox = [x for x in range(len(prices)+1)]
    z_scores = []
    for price in prices:
        z_scores.append((price-mean)/std)
    z_score = (new_price - mean) / std
    z_scores.append(z_score)
    lower_bound_draw = [z] * (len(prices)+1)
    upper_bound_draw = [-1 * z] * (len(prices)+1)
    plt.title("Z-score dla towaru: {}, k: {}".format(name,z))
    plt.plot(ox, z_scores, label='Ceny', color='b', marker='o')
    plt.plot(ox, lower_bound_draw, label='Dolne', color='r', linestyle='--')
    plt.plot(ox, upper_bound_draw, label='Gorne', color='r', linestyle='--')
    plt.savefig("wykresy/{}_{}_z-score.png".format(name,z))
    plt.clf()
    if abs(z_score) > z:
        return True
    return False

def plot_start(prices,name):
    ox = [x for x in range(len(prices))]
    plt.title("{} - Wykres cen bez zmian".format(name))
    plt.plot(ox, prices, label='Ceny', color='b', marker='o')
    plt.savefig("wykresy/{}_bez_zmian.png".format(name))
    plt.clf()


def chebyshev(new_price,prices,k,name):
    mean = statistics.mean(prices)
    variance = statistics.variance(prices)
    std = statistics.stdev(prices)
    upper_bound = mean + k * std
    lower_bound = mean - k * std
    ox = [x for x in range(len(prices)+1)]
    lower_bound_draw = [lower_bound] * (len(prices)+1)
    upper_bound_draw = [upper_bound] * (len(prices)+1)
    diff = abs(new_price - mean)

    '''print("Ograniczenie górne:: ", upper_bound)
    print("Ograniczenie dolne: ", lower_bound)
    print("Srednia: ", mean)
    print("Wariancja: ", variance)
    print("Odchylenie standardowe: ",std)'''
    prices.append(new_price)
    plt.title("Czebyszew dla towaru: {}, k: {}".format(name,k))
    plt.plot(ox, prices, label='Ceny', color='b', marker='o')
    plt.plot(ox, lower_bound_draw, label='Dolne', color='r', linestyle='--')
    plt.plot(ox, upper_bound_draw, label='Gorne', color='r', linestyle='--')
    plt.savefig("wykresy/{}_{}_czebyszew.png".format(name,k))
    plt.clf()
    if lower_bound <= new_price <= upper_bound:
        pass
    else:
        return True
    return False

def reduce_variance(prices,percentile):
    mean = statistics.mean(prices)
    variance = statistics.variance(prices)
    print("Srednia: ", mean)
    print("Wariancja: ", variance)
    percentage = variance*100/mean
    counter = 0
    while percentage>10 and len(prices)>40:
        counter = counter + 1
        tmp = [(x,abs(mean-x)) for x in prices]
        sorted_tmp = sorted(tmp, key=lambda x: x[1], reverse = True)
        sorted_tmp = sorted_tmp[:5]
        tmp_values = [x[0] for x in sorted_tmp]
        prices = [x for x in prices if x not in tmp_values]
        mean = statistics.mean(prices)
        variance = statistics.variance(prices)
        percentage = variance*100/mean
    print("Usunieto {} cen".format(counter*5))
    return counter, prices

def iqr(prices):
    q1 = np.percentile(prices, 25)
    q3 = np.percentile(prices, 75)

    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    print(lower_bound)
    print(upper_bound)
    outliers = [x for x in prices if x < lower_bound or x > upper_bound]
    print("Granice wartości odstających: ".format(lower_bound, upper_bound))
    print("Znalezione wartości odstające: ".format(outliers))
    return [x for x in prices if lower_bound <= x <= upper_bound]

def add_to_database(conn,name,quantity,new_price):
    cursor = conn.cursor()
    cursor.execute("SELECT cena FROM towary WHERE nazwa = '{}'".format(name))
    prices = [row[0] for row in cursor.fetchall()]
    plot_start(prices,name)
    counter, prices = reduce_variance(prices,5)
    if(counter == 0):
        iqr(prices)
    input_ok = True
    if(zscore(new_price,prices, 3, name)):
        print("Cena zablokowana przez ograniczenie z-score")
        input_ok = False
    if(chebyshev(new_price,prices, 3, name)):
        print("Cena zablokowana przez ograniczenie Czebyszewa")
        input_ok = False 
    if(linear_regression(new_price,prices,name)):
        print("Nowa cena  odbiega od trendu.")
    if(input_ok):
        cursor.execute("INSERT INTO towary (nazwa, ilosc, cena) VALUES (?, ?, ?)", ('{}'.format(name), quantity, new_price))
        conn.commit()
        print('Dodano nowy wpis')
        return True
    return False

def main():
    conn = sqlite3.connect('baza_danych.db')
    cursor = conn.cursor()

    #Test 1
    if(add_to_database(conn,'chleb',30,5.5) == True):
        print('Test 1 OK') 
    #Test 2
    if(add_to_database(conn,'chleb',60,7.0) == False):
        print('Test 2 OK')
    #Test 3
    if(add_to_database(conn,'krzeslo',90,140.0) == False):
        print('Test 3 OK')
    #Test 4
    if(add_to_database(conn,'krzeslo',45,125.0) == True):
        print('Test 4 OK')
    #Test 5
    if(add_to_database(conn,'parowki',30,5.0) == True):
        print('Test 5 OK')
    #Test 6
    if(add_to_database(conn,'parowki',60,7.0) == False):
        print('Test 6 OK')
    #Test 7
    if(add_to_database(conn,'mleko',40,5.0) == False):
        print('Test 7 OK')
    #Test 8
    if(add_to_database(conn,'mleko',20, 4.0) == True):
        print('Test 8 OK')
    #Test 9
    if(add_to_database(conn,'plyn',60, 10.25) == False):
        print('Test 9 OK')
    #Test 10
    if(add_to_database(conn,'plyn',30,6.5) == True):
        print('Test 10 OK')




if __name__ == '__main__':
    main()