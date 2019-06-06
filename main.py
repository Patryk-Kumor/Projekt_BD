# -*- coding: utf-8 -*-
import argparse
import psycopg2
import json
import sys

#
#   LOGOWANIE W POSTGRESIE:
#   psql init -h 127.0.0.1 -d student
#
#   psql app -h 127.0.0.1 -d student
#


# Pierwsze uruchomienie programu
def f_open_init(arg):
    # Dane dostępowe do bazy danych (zakładam poprawność danych dostępu)
    global conn
    conn = psycopg2.connect(host="localhost", port="5432",
                            dbname=arg['open']['database'],
                            user=arg['open']['login'],
                            password=arg['open']['password'])
    # Inicjalizacja kursora odpowiadającego za polecenia bazodwanowe
    global cur
    cur = conn.cursor()
    # Polecenia tworzące niezbędne tabele bazy (w pliku base.sql z katalogu)
    try:
        # Pobieranie zawartości z pliku .sql
        database_create = open('base.sql','r') 
        # Execute z pliku
        cur.execute(database_create.read())
        # Commit zmian pobranych z .sql
        conn.commit()
        print '{"status" : "OK"}'
    except Exception as err:
        # Rollback w przypadku błędów w pliku .sql
        conn.rollback()
        print '{"status" : "ERROR",\n "debug" : "%s" }' % str(err)[0:-1]
        sys.exit(0)  


# Kolejne uruchomienia programu
def f_open_app(arg):
    # Dane dostępowe do bazy danych (zakładam poprawność danych dostępu)
    global conn
    conn = psycopg2.connect(host="localhost", port="5432",
                            dbname=arg['open']['database'],
                            user=arg['open']['login'],
                            password=arg['open']['password'])
    # Inicjalizacja kursora
    global cur
    cur = conn.cursor()
    print ('{"status" : "OK"}')

def check_id(member):
    return 0

def add_member(member, password, timestamp):
    return 0

def f_leader(arg):
    # Sprawdzamy czy istnieje taki member/ czy istnieje gdzieś takie ID
    cur.execute("SELECT * FROM global_ids WHERE ID = %s;", (arg['leader']['member'],))
    wynik = len(cur.fetchall())
    if wynik == 0: 
        # Jeżeli nie ma znalezionych krotek/ nie istnieje nic o takim id - droga wolna do dodania membera(leadera)
        try:
            # Dodawanie membera wraz z haszowaniem hasła w bazie danych oraz dodawanie ID do tabeli z globalnymi id
            # crypt(password, gen_salt('md5'))
            cur.execute("""INSERT INTO member (ID, leader, activity, password, activity_date) 
                               VALUES (%s, True, True, crypt(%s, gen_salt('md5')), to_timestamp(%s));
                           INSERT INTO global_ids (ID) VALUES (%s);""",
                        (arg['leader']['member'], arg['leader']['password'], arg['leader']['timestamp'], arg['leader']['member']) )
            conn.commit()
            print '{"status" : "OK"}'
        except Exception as err:
            # Rollback jeśli coś poszło nie tak
            conn.rollback()
            print '{"status" : "ERROR",\n "debug" : "%s" }' % str(err)[0:-1]  
    else: 
        # Jezeli znaleziono krotki - id jest juz zajete
        print ('{"status" : "ERROR",\n "debug" : "ID jest juz uzywany" }')    


def f_protest(arg):
    print ("protest")


def f_support(arg):
    print ("support")


def f_upvote(arg):
    print ("upvote") 


def f_downvote(arg):
    print ("downvote") 


def f_actions(arg):
    print ("actions") 


def f_projects(arg):
    print ("projects") 


def f_votes(arg):
    print ("votes")


def f_trolls(arg):
    print ("trolls") 

# Funkcja przyporządkowująca odpowiednie funkcje do dalszej obróbki jsonów 
def if_case(dic, case):
    if args.init:
        if case == 'open':
            f_open_init(dic)
        elif case == 'leader':
            f_leader(dic)
        else:
            # Koniec - zakładamy ze dane jsony są poprawne -> nie zwrócimy błędów
            print '{"status": "ERROR", "debug": "Niepoprawne wywołania init"}'
    else:
        if case == 'open':
            f_open_app(dic)
        elif case == 'protest':
            f_protest(dic)
        elif case == 'support':
            f_support(dic)
        elif case == 'upvote':
            f_upvote(dic)
        elif case == 'downvote':
            f_downvote(dic)
        elif case == 'actions':
            f_actions(dic)
        elif case == 'projects':
            f_projects(dic)
        elif case == 'votes':
            f_votes(dic)
        elif case == 'trolls':
            f_trolls(dic)
        else:
            # Koniec - zakładamy ze dane jsony są poprawne -> nie zwrócimy błędów
            print '{"status": "ERROR", "debug": "Niedozwolona zawartość json"}'

# Funkcja czytająca w pętli na standardowym wejściu
def from_standard_input():
    while True:
        try:
            # Czytanie ze standardowego wejścia linii z jsonami w tekście
            line = sys.stdin.readline()
            if not line:
                break
            # Wczytanie tekstu i przetworzenie jsona
            dic = json.loads(line)
            # Case funkcji       
            case = dic.keys()[0] 
            if_case(dic, case)
        except KeyboardInterrupt as err:
            #Koniec pracy programu - przerwanie użytkownika
            break
        except Exception as err:
            print '{"status" : "ERROR",\n "debug" : "%s" }' % str(err)[0:-1]      
            print err
            break

# Czytanie z pliku wejściowego (flaga --f)
def from_file():
    # Przetwarzanie linijek pliku wejściowego
    for line in args.f[0]:
        try:
            # Wczytanie jsona
            dic = json.loads(line)
            # Case funkcji       
            case = dic.keys()[0]
            if_case(dic, case)
        except Exception as err:
            print '{"status" : "ERROR",\n "debug" : "%s" }' % str(err)[0:-1]   
            break


# Przygotowanie parsera argumentów
parser = argparse.ArgumentParser(description='System Zarządzania Partią Polityczną')
parser.add_argument("--f", 
                   type=file,
                   nargs=1, 
                   help="Flaga wywołania z pliku, wymaga argumentu w postaci ścieżki pliku z danymi json")
parser.add_argument("--init", 
                   action="store_true", 
                   help="Flaga pierwszego wywołania")
args = parser.parse_args()

# Jeżeli flaga --f => czytaj z pliku na starcie
if args.f:
    from_file()
    from_standard_input()
else:
    from_standard_input()




