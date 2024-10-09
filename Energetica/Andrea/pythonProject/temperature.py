# LIBRERIE
import pandas as pd
import csv

# COSTANTI
LETTURA = 'r'
SCRITTURA = 'w'
FILE = 'csv/dati2.csv'  # File letto
TEMP_LIMITE = 12


def main():
    dati = list()

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

    # Stampo i dati
    stampa(dati)


# Funzione di stampa
def stampa(dati):
    # Stampa in riga
    for elemento in dati:
        print(elemento)

    stampa_su_excel(dati)


def stampa_su_excel(dati):
    giorni = [dato[0] for dato in dati]
    dati_excel = [dato[1] for dato in dati]

    df = pd.DataFrame(dati_excel, columns=["Text media giornaliera "],
                      index=giorni)
    df.to_excel('Dati variazioni orari.xlsx', sheet_name='Dati variazioni orari')


# Funzione di lettura dei dati
def leggi_dati(reader):
    # Inizializzo la struttura dati
    dati = list()\

    # Scorro le righe del file
    for riga in reader:
        try:
            if float(riga[1].split(";")[-1] + riga[2].split(";")[0])/100 < 2 or riga[0].split("-")[-1].split(";")[0].strip() != "23:09":
                raise Exception
        except Exception:
            continue

        dati.append([riga[0].split("-")[0][2:-1:], float(riga[1].split(";")[-1] + riga[2].split(";")[0])/100])

    return dati


# Chiamo il main
main()
