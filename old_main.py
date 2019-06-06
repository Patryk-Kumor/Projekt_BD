import argparse
import psycopg2
import json


#
#   LOGOWANIE W POSTGRESIE:
#   psql init -h 127.0.0.1 -d student
#
#   psql app -h 127.0.0.1 -d student
#


# Pierwsze uruchomienie programu
def f_open_init(arg):
    # Dane dostepowe do bazy danych (zakladam poprawnosc danych dostepu)
    global conn
    conn = psycopg2.connect(host="localhost", port="5432",
                            dbname=arg['open']['database'],
                            user=arg['open']['login'],
                            password=arg['open']['password'])
    # Inicjalizacja kursora odpowiadajacego za polecenia bazodwanowe
    global cur
    cur = conn.cursor()
    # Polecenia tworzace niezbedne tabele bazy (w pliku base.sql z katalogu)
    try:
        # Pobieranie zawartosci z pliku .sql
        database_create = open('base.sql','r') 
        # Execute z pliku
        cur.execute(database_create.read())
        # Commit zmian pobranych z .sql
        conn.commit()
        print ('{"status" : "OK"}')
    except Exception as err:
        # Rollback w przypadku bledow
        conn.rollback()
        print ('{"status" : "ERROR",\n "debug" : "%s" }' % ( str(err)[0:-1] ) )       


# Kolejne uruchomienia programu
def f_open_normal(arg):
    # Dane dostepowe do bazy danych (zakladam poprawnosc danych dostepu)
    global conn
    conn = psycopg2.connect(host="localhost", port="5432",
                            dbname=arg['open']['database'],
                            user=arg['open']['login'],
                            password=arg['open']['password'])
    # Inicjalizacja kursora
    global cur
    cur = conn.cursor()
    print ('{"status" : "OK"}')


def f_leader(arg):
    # Sprawdzamy czy istnieje taki member/ czy istnieje gdzies takie ID
    cur.execute("SELECT * FROM global_ids WHERE ID = %s;" % (arg['leader']['member']))
    wynik = len(cur.fetchall())
    if wynik == 0: 
        # Jezeli nie ma znalezionych krotek - nie istnieje nic o takim id - droga wolna do dodania membera
        try:
            # Dodawanie uzytkownika wraz z haszowaniem hasla w bazie danych oraz dodawanie ID do tabeli z globalnymi id
            # crypt(password, gen_salt('md5'))
            args = "%s, True, True, crypt('%s', gen_salt('md5')), to_timestamp(%s)" % (arg['leader']['member'], arg['leader']['password'], arg['leader']['timestamp'])
            cur.execute("INSERT INTO member (ID, leader, activity, password, activity_date) VALUES (%s);" %(args) \
                      + "INSERT INTO global_ids (ID) VALUES (%s);" %(arg['leader']['member']) )
            conn.commit()
            print ('{"status" : "OK"}')
        except Exception as err:
            # Rollback jesli cos poszlo nie tak
            conn.rollback()
            print ('{"status" : "ERROR",\n "debug" : "%s" }' % ( str(err)[0:-1] ) )  
    else: 
        # Jezeli znaleziono krotki - id jest juz zajete
        print ('{"status" : "ERROR",\n "debug" : "ID jest juz uzywany" }')     


def f_protest(arg):
    com = """

                # SPRAWDZANIE AKTYWNOSCI 
                #########

    # Sprawdzamy czy istnieje taki member/ czy istnieje gdzies takie ID
    cur.execute("SELECT * FROM member WHERE ID = %s;" % (arg['protest']['member']))
    wynik = cur.fetchall()
    if  len(wynik) == 1:





        # Sprawdzamy dane membera
        hasz = wynik[0][3]
        string = "SELECT password = crypt('%s', password) FROM  (SELECT password FROM member WHERE id=%s) as foo;" %(arg['protest']['password'], arg['protest']['member'])
        cur.execute(string)
        potwierdzenie = cur.fetchall()
        if potwierdzenie[0][0]:
            # AKTUALIZACJA TIMESTAMP MEMBERA

            ###
            print ""
        else:
            # Niepoprawne haslo
            print ('{"status" : "ERROR",\n "debug" : "Haslo jest niepoprawne" }')     
            return       
    else:
        # Dodawanie membera
        try:
            # Dodawanie uzytkownika wraz z haszowaniem hasla w bazie danych oraz dodawanie ID do tabeli z globalnymi id
            # crypt(password, gen_salt('md5'))
            args = "%s, False, True, crypt('%s', gen_salt('md5')), to_timestamp(%s)" % (arg['protest']['member'], arg['protest']['password'], arg['protest']['timestamp'])
            cur.execute("INSERT INTO member (ID, leader, activity, password, activity_date) VALUES (%s);" %(args) \
                      + "INSERT INTO global_ids (ID) VALUES (%s);" %(arg['leader']['member']) )
            conn.commit()
        except Exception as err:
            # Rollback jesli cos poszlo nie tak
            conn.rollback()
            print ('{"status" : "ERROR",\n "debug" : "%s" }' % ( str(err)[0:-1] ) )  
            return


    # DALSZE DZIALANIA DODAWANIA PROTESTU
    """
    print ('{"status" : "OK"')


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


# Wywolanie wraz a flaga --init
def initialize():
    # Przetwarzanie linijek pliku wejsciowego
    for line in args.file:
        # Wczytanie jsona
        dic = json.loads(line)
        # Case funkcji       
        case = dic.keys()[0]
        if case == 'open':
            f_open_init(dic)
        elif case == 'leader':
            f_leader(dic)
        # Koniec - zakladamy ze dane sa poprawne -> nie zwrocimy bledow
        else:
            print ('{"status": "ERROR"}')


# Kolejne wywolania programu
def normal():
    # Przetwarzanie linijek pliku wejsciowego
    for line in args.file:
        # Wczytanie jsona
        dic = json.loads(line)
        # Case funkcji       
        case = dic.keys()[0]
        if case == 'open':
            f_open_normal(dic)
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
        # Koniec - zakladamy ze dane sa poprawne -> nie zwrocimy bledow
        else:
            print ('{"status": "ERROR"}')


# Wywolanie main
# Parser argumentow
parser = argparse.ArgumentParser(description='System Zarzadzania Partia Polityczna')
parser.add_argument("file", 
                   type=file,
                   help="wymagane: pobieranie wierszy json zawartych w pliku")
parser.add_argument("--init", 
                   action="store_true", 
                   help="pierwsze wywolanie")
args = parser.parse_args()
# Rozpoznanie flagi
if args.init:
    initialize()
else:
    normal()
# Koniec open <- zakonczenie cursora i connect
cur.close()
conn.close()




