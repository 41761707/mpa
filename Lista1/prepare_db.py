import sqlite3
import random
import sys

def generate_inserts(conn,filename):
    cursor = conn.cursor()
    with open(filename, 'r') as file:
        for line in file:
            name = filename[2:-4]
            price = float(line)
            number = random.randint(5,10) * int(price)
            insert = (name,number,price)
            cursor.execute("INSERT INTO towary (nazwa, ilosc, cena) VALUES (?, ?, ?)", insert)
            conn.commit()
        
    

def main():
    conn = sqlite3.connect('baza_danych.db')
    filename = sys.argv[1]
    generate_inserts(conn,filename)

    conn.close()
if __name__ == '__main__':
    main()