import sqlite3

# Nawiązujemy połączenie z bazą danych (lub tworzymy ją, jeśli nie istnieje)
conn = sqlite3.connect('baza_danych.db')

# Tworzymy kursor do wykonywania poleceń SQL
cursor = conn.cursor()

# Tworzymy tabelę "towary"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS towary (
        id INTEGER PRIMARY KEY,
        nazwa TEXT,
        ilosc INTEGER,
        cena REAL
    )
''')

# Zatwierdzamy zmiany w bazie danych
conn.commit()

# Zamykamy połączenie z bazą danych
conn.close()
