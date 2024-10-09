# LIBRERIE
import pandas as pd
import csv
from math import pow

# COSTANTI
LETTURA = 'r'
SCRITTURA = 'w'
FILE_DIARIO = 'csv/DiarioGiorni.csv'  # File letto
FILE_TEMPERATURE = "csv/dati.csv"
P_W = 1000.0
MJ = pow(10, 6) * 1.0
C_w = 4186.0
J_TO_kWh = 2.77778 * pow(10, -7)
TEMPERATURA_IDEALE = 40.0
L_TO_M3 = pow(10, -3)


def main():
    # Apro il file

    # Apro il file
    try:
        file = open(FILE_TEMPERATURE, LETTURA, encoding='UTF-8')
    except FileNotFoundError:
        print('File non trovato')
        exit(1)

    # Creo un puntatore a inizio file
    reader = csv.reader(file)

    # Creo la struttura dati che legge i dati e invoco la funzione di lettura
    temperature = leggi_temperature(reader)
    file.close()
    try:
        file = open(FILE_DIARIO, LETTURA, encoding='UTF-8')
    except FileNotFoundError:
        print('File non trovato')
        exit(1)

    # Creo la struttura dati che legge i dati e invoco la funzione di lettura
    diario = leggi_diario(file)
    file.close()

    dati = combina(temperature, diario)

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
    dati_excel = [dato[1::] for dato in dati]

    df = pd.DataFrame(dati_excel, columns=["Rubinetto (min)", "Doccia (min)", "Litri (L)",
                                           "Temperatura ext ora (C)", "ACS Oraria [MJ]", "ACS Oraria [kWh]"],
                      index=giorni)
    df.to_excel('Dati variazioni orari.xlsx', sheet_name='Dati variazioni orari')


# Funzione di lettura dei dati
def leggi_diario(reader):
    # Inizializzo la struttura dati
    dati = list()
    mese = list()
    reader.readline()

    # Scorro le righe del file
    for riga in reader:
        riga = riga.split(";")
        try:
            int(riga[1])
            if (riga[1]).find(",") >= 0:
                riga[1] = riga[1][0:riga[1].find(","):] + "." + riga[1][riga[1].find(",")+1::1]
            if (riga[2]).find(",") >= 0:
                riga[2] = riga[2][0:riga[2].find(","):] + "." + riga[2][riga[2].find(",")+1::1]
            if (riga[3]).find(",") >= 0:
                riga[3] = riga[3][0:riga[3].find(","):] + "." + riga[3][riga[3].find(",")+1::1]
            if (riga[4]).find(",") >= 0:
                riga[4] = riga[4][0:riga[4].find(","):] + "." + riga[4][riga[4].find(",") + 1::1]
            mese.append([int(riga[1]), float(riga[2]), float(riga[3]), float(riga[4])])
        except Exception:
            dati.append(list(mese))
            mese = list()

    return dati


# Funzione di lettura dei dati
def leggi_temperature(reader):
    # Inizializzo la struttura dati
    dati = list()

    # Scorro le righe del file
    for riga in reader:
        try:
            float(riga[len(riga) - 1])
        except Exception:
            continue

        data = riga[0].split(":")
        data[0] = data[0][6:len(data[0]):1] + "/" + data[0][4:len(data[0]) - 2:1] + "/" + data[0][0:4:1]
        data[1] = data[1][0:2:1] + ':' + data[1][2:len(data[1]):1]
        riga[5] = float(riga[5])

        dati.append([data[0] + " - " + data[1], riga[5]])

    for i in range(0, len(dati)-2, 1):
        dati[i][0] = dati[i+2][0]

    dati = dati[0:len(dati)-2:1]

    return dati


# Funzione di lettura dei dati
def combina(temperature, diario):
    # Inizializzo la struttura dati
    dati = list()

    for dato in temperature:
        mese = int(dato[0].split("-")[0].strip().split("/")[1])-1
        ora = int(dato[0].split("-")[1].strip().split(":")[0])

        risultato = P_W * C_w * L_TO_M3 * (TEMPERATURA_IDEALE - dato[1]) * diario[mese][ora][3]
        dati.append([dato[0][0:len(dato[0])-2:1] + "00", diario[mese][ora][1], diario[mese][ora][2],
                     diario[mese][ora][3], dato[1], round(risultato/MJ, 4), round(risultato*J_TO_kWh, 4)])

    return dati


# Chiamo il main
main()
