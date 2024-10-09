# LIBRERIE
import pandas as pd
import csv

# COSTANTI
LETTURA = 'r'
SCRITTURA = 'w'
FILE = 'csv/dati.csv'  # File letto
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

    # chiamo la media ponderata dei dati
    dati = list(pulizia(dati))
    dati = list(t_media_giornaliera(dati))

    # Stampo i dati
    stampa(dati)


# Funzione di media giornaliera
def t_media_giornaliera(dati):
    giorno = 1
    temperature = list()

    for i in range(0, len(dati), 1):
        if int(((dati[i][0]).split("-")[0]).split("/")[0]) == giorno:
            temperature.append(dati[i][-1])
        else:
            giorno = int(((dati[i][0]).split("-")[0]).split("/")[0])
            dati[i - 1].append((max(temperature) + min(temperature) + temperature[8] + temperature[19]) / 4)
            temperature = list()

    dati[-1].append((max(temperature) + min(temperature) + temperature[8] + temperature[19]) / 4)
    return dati


# Sommatoria gradi giorno
def gradi_giorno(dati):
    somma = 0
    accesi = 0
    tre_valori = list()

    for i in range(23, len(dati), 24):
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
    stampa_su_excel(dati)


def stampa_su_excel(dati):
    giorni = [dato[0] for dato in dati]
    dati_excel = [dato[1:] for dato in dati]

    df = pd.DataFrame(dati_excel, columns=["Gb(i)", "Gd(i)", "Gr(i)", "Altezza sole", "Temperatura aria ext",
                                           "Text media giornaliera "],
                      index=giorni)
    df.to_excel('Dati variazioni orari.xlsx', sheet_name='Dati variazioni orari')


# Funzione di pulizia e formattazione dei dati
def pulizia(dati):
    # Inizializzo il pulito

    # Sistemo la data 01/01/2019 - 00:09
    for i in range(0, len(dati), 1):
        data = dati[i][0].split(":")
        data[0] = data[0][6:len(data[0]):1] + "/" + data[0][4:len(data[0]) - 2:1] + "/" + data[0][0:4:1]
        data[1] = data[1][0:2:1] + ':' + data[1][2:len(data[1]):1]
        dati[i][0] = data[0] + " - " + data[1]

    for i in range(0, len(dati) - 2, 1):
        dati[i][0] = dati[i + 2][0]

    dati = dati[0:len(dati) - 2:1]

    return dati


# Funzione di lettura dei dati
def leggi_dati(reader):
    # Inizializzo la struttura dati
    dati = list()

    # Scorro le righe del file
    for riga in reader:
        try:
            float(riga[len(riga) - 1])
        except Exception:
            continue

        riga[1] = float(riga[1])
        riga[2] = float(riga[2])
        riga[3] = float(riga[3])
        riga[4] = float(riga[4])
        riga[5] = float(riga[5])

        dati.append(riga[0:len(riga) - 2:1])

    return dati


# Chiamo il main
main()
