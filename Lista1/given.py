import sqlite3
import random

def things(conn):
    inserts = []
    cursor = conn.cursor()
    for i in range(50):
        no_pens = random.randint(20,60)
        inserts.append(('krzeslo',no_pens,random.random() + 100 + (i/2)))
        if i%10 == 0:
            inserts.append(('krzeslo',no_pens,random.random()+1000))
    for insert in inserts:
        print(insert)
    for insert in inserts:
        cursor.execute("INSERT INTO towary (nazwa, ilosc, cena) VALUES (?, ?, ?)", insert)
    conn.commit()
    

def main():
    conn = sqlite3.connect('baza_danych.db')

    things(conn)

    conn.close()
if __name__ == '__main__':
    main()