import argparse
import psycopg2
import json

# Pierwsze uruchomienie programu
def f_open_init(arg):
    # Dane dostepowe do bazy danych
    conn = psycopg2.connect(host="localhost",
                            dbname=arg['open']['database'],
                            user=arg['open']['login'],
                            password=arg['open']['password'],
                            port="5432")
    cur = conn.cursor()
    # Polecenia tworzace niezbedne elementy bazy (w pliku base.sql z katalogu)
    database_create = open('base.sql','r') 
    cur.execute(database_create.read())
    # debug
    #print cur.fetchone()

    #cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
    #cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))
    #cur.execute("SELECT * FROM test;")
    #print cur.fetchone() # (1, 100, "abc'def")

    # Potwierdzenie connect
    conn.commit()
    cur.close()
    conn.close()
    # Koniec open
    print ('{"status" : "OK"}')

def f_open_normal(arg):
    print ("open_normal")

def f_leader(arg):
    print ("leader") 

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
            print ('{"status": "Error"}')


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
            print ('{"status": "Error"}')


# Wywolanie main
# Parser argumentow
parser = argparse.ArgumentParser(description='System Zarzadzania Partia Polityczna')
parser.add_argument("file", 
                   type=file,
                   help="pobieranie wierszy json zawartych w pliku")
parser.add_argument("--init", 
                   action="store_true", 
                   help="pierwsze wywolanie")
args = parser.parse_args()
# Rozpoznanie flagi
if args.init:
    initialize()
else:
    normal()




