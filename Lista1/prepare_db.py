import sqlite3
import random

def things(conn):
    inserts = []
    cursor = conn.cursor()
    for i in range(20):
        no_pens = random.randint(20,60)
        inserts.append(('Krzeslo',no_pens,random.random() + 100 + i))
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