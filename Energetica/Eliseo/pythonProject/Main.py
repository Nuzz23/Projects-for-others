# LIBRERIE
import pandas as pd
import csv
import datetime


# COSTANTI
LETTURA = 'r'
SCRITTURA = 'w'
FILES = ['csv/1_5 a 3.csv', 'csv/3 a 4_5.csv', 'csv/4_5 a 6.csv']  # Elenco dei file letti
# Presuppongo che il file 1 sia case piccole, il 2 case medie e il 3 case grandi
# Fattori moltiplicativi per case piccole medie e grandi
FATTORE_CASA_PICCOLA = 1
FATTORE_CASA_MEDIA = 1
FATTORE_CASA_GRANDE = 1
# Prendo la data iniziale del periodo di osservazione
DATA_INIZIALE = datetime.datetime.strptime('2022-01-01', '%Y-%m-%d')
# Prendo la variazione di data di giorno in giorno
TIME_DELTA = datetime.timedelta(days=1)
# Giorni massimi in un anno
MAX_DAYS = 365
# Ore in un giorno
HOURS = 24


def main():
    dati = list()

    # Prendo ogni nome del file contenuto in valori
    for filename in FILES:

        # Apro il file
        try:
            file = open(filename, LETTURA, encoding='UTF-8')
        except FileNotFoundError:
            print('File non trovato')
            exit(1)

        # Creo un puntatore a inizio file
        reader = csv.reader(file)

        # Creo la struttura dati che legge i dati e invoco la funzione di lettura
        dati.append(leggi_dati(reader))
        file.close()

    # chiamo la media ponderata dei dati
    dati = list(media(dati))

    # Stampo i dati
    stampa(dati)


# Funzione di stampa
def stampa(dati):
    # Stampa come vettore
    print(dati)

    # Stampa in riga
    for dato in dati:
        print(dato, end=' ')

    print('\n')
    giorni = crea_vettore_giorni()
    for i in range(0, len(giorni), 1):
        print(giorni[i], end='\t\t')
        for j in range(i*24, (i+1)*24, 1):
            print(dati[j], end='  ')
        print()

    # stampa_su_excel(dati, giorni)


def stampa_su_excel(dati, giorni):
    orario = list()

    for i in range(0, HOURS, 1):
        orario.append('Ora ' + str(i+1))

    dati_divisi = list()
    for i in range(0, MAX_DAYS, 1):
        dati_divisi.append(dati[i*24:(i+1)*24:1])

    df = pd.DataFrame(dati_divisi, index=giorni, columns=orario)
    df.to_excel('Risultato.xlsx', sheet_name='Dati 2022-Torino')


# Funzione di media pesata
def media(dati):
    # Inizializzo il vettore media
    mediato = list()

    # Scorro sulla lunghezza dei 3 vettori contenuti interamente
    for i in range(0, len(dati[0]), 1):
        # aggiungo al vettore l'elemento mediato e arrotondato alla 4 cifra significativa
        mediato.append(round((dati[0][i]*FATTORE_CASA_PICCOLA + dati[1][i]*FATTORE_CASA_MEDIA +
                              dati[2][i]*FATTORE_CASA_GRANDE)
                        / (FATTORE_CASA_MEDIA+FATTORE_CASA_GRANDE+FATTORE_CASA_PICCOLA), 4))

    return mediato


# Funzione di lettura dei dati
def leggi_dati(reader):
    # Inizializzo la struttura dati
    dati = list()
    feriali = [[]]
    sabato = [[]]
    domenica = [[]]

    # Scorro le righe del file
    for riga in reader:

        # Mi assicuro che la data sia valida, prendo la data e se non può essere convertita in intero va bene
        try:
            # Provo a convertirla in intero
            float(riga[0].split(';')[0])
            flag = False
        except ValueError:
            # Gestisco l'eccezione di non conversione in intero
            flag = True

        # Mi accerto che la provincia è Torino e che il flag sia vero e che sia tutti e che sia tutti
        if (((riga[0].split(';')[1]).strip().upper() == 'TORINO' and flag
                and (riga[0].split(';')[2]).strip().upper() == 'TUTTI') and
                (riga[0].split(';')[4]).strip().upper() == 'TUTTI'):

            # Controllo il giorno, se è feriale
            if (riga[0].split(';')[5]).strip().upper() == 'GIORNO_FERIALE':
                # Se ho già riempito il feriale per il mese significa che sono al mese prossimo
                # altrimenti non ho raggiunto le 24h
                if len(feriali[len(feriali)-1]) != HOURS:
                    feriali[len(feriali)-1].append(float(riga[1]))
                else:
                    feriali.append([float(riga[1])])
            # Controllo il giorno, se è sabato
            elif (riga[0].split(';')[5]).strip().upper() == 'SAB':
                # Se ho già riempito il feriale per il mese significa che sono al mese prossimo
                # altrimenti non ho raggiunto le 24h
                if len(sabato[len(sabato)-1]) != HOURS:
                    sabato[len(sabato)-1].append(float(riga[1]))
                else:
                    sabato.append([float(riga[1])])
            # Controllo il giorno, se è domenica, non metto else per evitare ambiguità
            elif (riga[0].split(';')[5]).strip().upper() == 'DOM':
                # Se ho già riempito il feriale per il mese significa che sono al mese prossimo
                # altrimenti non ho raggiunto le 24h
                if len(domenica[len(domenica)-1]) != HOURS:
                    domenica[len(domenica)-1].append(float(riga[1]))
                else:
                    domenica.append([float(riga[1])])

    # Inizializzo la variabile data corrente
    data_corrente = DATA_INIZIALE

    for i in range(0, MAX_DAYS, 1):
        if 0 <= data_corrente.weekday() <= 4:
            for j in range(0, HOURS, 1):
                try:
                    dati.append(feriali[int(data_corrente.month)-1][j])
                except IndexError:
                    print('errore selezione cella vettore')
                    exit(1)

        elif data_corrente.weekday() == 5:
            for j in range(0, HOURS, 1):
                try:
                    dati.append(sabato[int(data_corrente.month)-1][j])
                except IndexError:
                    print('errore selezione cella vettore')
                    exit(1)
        else:
            for j in range(0, HOURS, 1):
                try:
                    dati.append(domenica[int(data_corrente.month)-1][j])
                except IndexError:
                    print('errore selezione cella vettore')
                    exit(1)
        data_corrente = data_corrente + TIME_DELTA

    return dati


# Traduco il giorno da numero a Human Readable
def value_to_day(valore):
    if not 0 <= valore <= 6:
        return ''

    if valore == 0:
        return 'MON'
    elif valore == 1:
        return 'TUE'
    elif valore == 2:
        return 'WED'
    elif valore == 3:
        return 'THU'
    elif valore == 4:
        return 'FRI'
    elif valore == 5:
        return 'SAT'
    elif valore == 6:
        return 'SUN'


# Creo il vettore dei giorni
def crea_vettore_giorni():
    giorni = list()
    data_corrente = DATA_INIZIALE

    # Controllo che la traduzione vada a buon fine e poi aggiungo la data
    for i in range(0, MAX_DAYS, 1):
        # Controllo data valida
        if value_to_day(data_corrente.weekday()):
            # Appendo il nome del giorno con la data + qualche magheggio per il formato
            giorni.append(value_to_day(data_corrente.weekday()) + ' ' +
                          '-'.join(str(data_corrente).split()[0].strip().split('-')[::-1]))
        else:
            print('Data non valida')
            exit(2)
        data_corrente = data_corrente + TIME_DELTA

    return giorni


# Chiamo il main
main()


