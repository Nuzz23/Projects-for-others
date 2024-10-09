# LIBRERIE
import csv
import pandas as pd

# COSTANTI
LETTURA = 'r'
SCRITTURA = 'w'
FILE = 'csv/LavoraOrarioOk.csv'  # File letto
TEMP_LIMITE = 12


def main():
    # Apro il file
    try:
        file = open(FILE, LETTURA, encoding='UTF-8')
    except FileNotFoundError:
        print('File non trovato')
        exit(1)

    # Creo un puntatore a inizio file
    reader = csv.reader(file)

    # Creo la struttura dati che legge i dati e invoco la funzione di lettura
    dati = leggi_dati(reader)
    file.close()

    # chiamo la media ponderata dei dati
    for i in range(0, len(dati), 1):
        dati[i][1] = dati[i][1].split("-")[0].strip()
        dati[i][2] = float(dati[i][2])

    dati = list(t_media_giornaliera(dati))

    # Stampo i dati
    stampa(dati)


# Funzione di media giornaliera
def t_media_giornaliera(dati):
    temperature = list()
    primo = True

    for i in range(0, len(dati), 1):
        if primo:
            primo = False
            temperature.append(dati[i][-1])
            continue

        if dati[i][0] == "":
            temperature.append(dati[i][-1])
        else:
            dati[i - 1].append((max(temperature) + min(temperature) + temperature[8] + temperature[19]) / 4)
            temperature = list()

    dati[-1].append((max(temperature) + min(temperature) + temperature[8] + temperature[19]) / 4)
    return dati


# Sommatoria gradi giorno
def gradi_giorno(dati):
    somma = 0
    accesi = 0
    tre_valori = list()

    for i in range(0, len(dati), 1):
        if len(dati[i]) == 4:
            if len(tre_valori) == 3:
                if (not accesi and tre_valori[0] < TEMP_LIMITE and tre_valori[1] < TEMP_LIMITE
                        and tre_valori[2] < TEMP_LIMITE):
                    accesi = True

                if accesi:
                    somma = somma + 20 - dati[i][-1]

                if (accesi and tre_valori[0] > TEMP_LIMITE and tre_valori[1] > TEMP_LIMITE
                        and tre_valori[2] > TEMP_LIMITE):
                    accesi = False

                tre_valori[0] = tre_valori[1]
                tre_valori[1] = tre_valori[2]
                tre_valori[2] = dati[i][-1]

            else:
                tre_valori.append(dati[i][-1])

    print("Gradi giorno : " + str(round(somma, 4)))


# Funzione di stampa
def stampa(dati):
    # Stampa in riga
    for elemento in dati:
        print(elemento)

    gradi_giorno(dati)


# Funzione di lettura dei dati
def leggi_dati(reader):
    # Inizializzo la struttura dati
    dati = list()

    # Scorro le righe del file
    for riga in reader:
        riga = riga[0].split(";")
        try:
            dati.append([row for row in riga if not row[0] == "\ufeff"])
        except IndexError:
            dati.append(riga)

    return dati


# Chiamo il main
main()
