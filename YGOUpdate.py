import json
import progressbar
import os.path
import yugioh
import sys
import requests
import pathlib
import pandas as pd
import sqlite3 as sql
import time
import DBC

if os.name == 'nt': # Only if we are running on Windows
    from ctypes import windll
    k = windll.kernel32
    k.SetConsoleMode(k.GetStdHandle(-11), 7)

#per l'eseguibile, SOSTITUIRE application_path con pathlib.Path(__file__).parent.resolve() per testare
application_path = os.path.dirname(sys.executable)
# poi digitare pyinstaller --onefile YGOUpdate.py nella directory per convertire in .exe

parentDict = pathlib.Path(__file__).parent.resolve()

#DB decoder
dec = DBC.DBdecoder()

def trim_list(lines):
    for l in lines:
        if "#created by" in l:
            lines.remove(l)
            break
    #lines.remove("#created by ZiBenty\n")
    lines.remove("#main\n")
    lines.remove("#extra\n")
    lines.remove("!side\n")
    return lines

#AGGIORNA dictsetcodes e immagini mancanti
def dictupdate(Clist):
    dictsetcodes = {}
    cnt = 0
    lenghts = len(Clist)
    id = []
    print("Creazione dizionari in corso...")
    bar = progressbar.ProgressBar(maxval=lenghts, \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    print("")
    for c in Clist:
        card = None
        while card is None:
            try:
                card = yugioh.get_card(card_id = c)
            except:
                results = cur.execute("SELECT type FROM datas WHERE id IS " + str(c))
                df = pd.DataFrame(results)
                if df.values[0][0] == 20497 or df.values[0][0] == 16401:
                    card = 1 #la carta è un token
                if card is None:
                    results = cur.execute("SELECT alias FROM datas WHERE id IS " + str(c))
                    df = pd.DataFrame(results)
                    if df.values[0][0] != 0:
                        card = 1 #versione alternativa di una carta
                if card is None:
                    if c == 14478717 or c == 15590355 or c == 17885118 or c == 26435595:
                        card = 1 #carte non esistenti nel database carte online
                if card is None:
                    match c: #(codice ocg diverso da tcg)
                        case 5833312: 
                            card = yugioh.get_card(card_id = 100287011) #duel academy
                        case 33331231:
                            card = yugioh.get_card(card_id = 10028501) #Strategic Striker - H.A.M.P.
                        case 34293667:
                            card = yugioh.get_card(card_id = 100278013) #Ice Barrier
                        case 36114945:
                            card = yugioh.get_card(card_id = 10028503) #Yuki-Onna, the Icicle Mayakashi
                        case 62219643:
                            card = yugioh.get_card(card_id = 10028504) #Ghost Meets Girl - A Mayakashi and Shiranui's Tale
                        case 67378935:
                            card = yugioh.get_card(card_id = 100287027) #Overlay Network
        if card != None and card != 1:
            id.append(c)
            sys.stdout.write('\r') #va all'inizio della riga dei nomi
            sys.stdout.write("                                                                                               ")
            sys.stdout.write('\r') #dopo aver cancellato il contenuto, torna indietro
            sys.stdout.write(card.name) #scrive il nome della carta
            sys.stdout.flush()
        if card !=1 and hasattr(card, "card_images") and not os.path.exists('pics/' + str(c) + '.jpg'):
            url = getattr(card, "card_images")
            r = requests.get(url, allow_redirects=True)
            open('pics/' + str(c) + '.jpg', 'wb').write(r.content)
        if card != 1 and hasattr(card, "card_sets"):
            sets = getattr(card, "card_sets")
            setcodes = []
            if sets != None:
                for s in sets:
                    setcodes.append(s.get("set_code"))
                while card.id not in dictsetcodes:
                    dictsetcodes[card.id] = setcodes
        cnt += 1
        sys.stdout.write("\033[F") #il cursore torna sulla barra
        bar.update(cnt) #la aggiorna
        print("") #ritorna sul campo dei nomi
    #check carte finale
    missing = []
    for c in id:
        if c not in dictsetcodes:
            missing.append(c)
    print(missing)
    json.dump(dictsetcodes, open(os.path.join(parentDict, "structs/dict" + "setcodes" + ".txt"),'w'), sort_keys=True, indent='\t', separators=(',', ': '))
    sys.stdout.flush()
    print("\nCarte aggiornate")
    bar.finish()

print("Aggiornamento dei files in corso...\n")

cnt = 0
while os.path.isfile("c:/ProjectIgnis/deck/chaos draft " + str(cnt+1) + ".ydk"):
    cnt +=1
config = {"lastpool": cnt}

#aggiorna banlist
with open(os.path.join(parentDict, "structs/bans.json"), 'w') as f:
    with open('c:/ProjectIgnis/deck/chaos draft bans.ydk', 'r') as b:
        ban = b.readlines()
        ban = trim_list(ban)
        json.dump(ban, f)
        print("Banlist aggiornata\n")

#raccoglie tutte le carte
conn = sql.connect("structs/cards.cdb")
cur = conn.cursor()
results = cur.execute("SELECT id FROM texts")
df = pd.DataFrame(results)
cards = []

for c in df.values:
    cards.append(c[0])

#aggiorna pool draftata
cnt = 0
lenght = 0
newcardslist = []

for cnt in range(1, config["lastpool"]+1):
    f = open('c:/ProjectIgnis/deck/chaos draft ' + str(cnt) + '.ydk', 'r')
    newcards = f.readlines()
    newcards = trim_list(newcards)
    newcardslist.append(newcards)

for line in newcardslist:
    lenght += len(line)

#download cards.cdb
print("Download Database carte in corso...")
url = 'https://github.com/ProjectIgnis/BabelCDB/blob/master/cards.cdb?raw=true'
r = requests.get(url, allow_redirects=True)
open('structs/cards.cdb', 'wb').write(r.content)
print("Database aggiornato\n")

#salva pool draftata
pool = {}
bar = progressbar.ProgressBar(maxval=lenght, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
cnt = 0

print("Aggiornamento pool di carte in corso...")
bar.start()
with open(os.path.join(parentDict, "structs/card pool.txt"), "w") as card_pool:
    for line in newcardslist:
        for card in line:
            if card.rstrip("\n") in pool.keys():
                pool[card.rstrip("\n")] += 1
            else:
                pool[card.rstrip("\n")] = 1
            cnt += 1
            bar.update(cnt)
    json.dump(pool, card_pool, indent='\t', separators=(',', ': '))
bar.finish()
print("Pool aggiornata: " + str(len(pool)) + " carte differenti\n")

print("Aggiornamento lista Archetipi della pool in corso...")
#lista di id carta
clist = []
for c in pool.keys():
    clist.append(c.rstrip("\n"))
    
#Dizionario (Archetipo, n. carte trovate dell'Archetipo)
archetype = {}
inserted = {}
for c in clist:
    archs = dec.DBdecode("id", c, "setcode")
    for v in archs:
        if v in archetype.keys():
            archetype[v] = archetype[v] + pool[c]
            inserted[v].append(c)
        else:
            archetype[v] = pool[c]
            inserted[v] = [c]
for c in clist:
    v1 = dec.DBdecode("id", c, "desc")
    for v in archetype:
        if v in v1 and c not in inserted[v]:
            archetype[v] = archetype[v] + pool[c]
            inserted[v].append(c)
for c in clist:
    v1 = dec.DBdecode("id", c, "name")
    for v in archetype:
        if v in v1 and c not in inserted[v]:
            archetype[v] = archetype[v] + pool[c]

json.dump(archetype, open(os.path.join(parentDict, "structs/poolArch.txt"),'w'), sort_keys=True, indent='\t', separators=(',', ': '))

#Lista per combo Archetipo
sorted_values = sorted(archetype.values())
sorted_values.reverse()
sorted_dict = {}
for i in sorted_values:
    for k in archetype.keys():
        if archetype[k] == i and k not in sorted_dict.keys():
            sorted_dict[k] = archetype[k]
            break

archetypelst = []
archetypelst.append("")
tmp = list(sorted_dict.keys())
for arch in tmp:
    archetypelst.append(arch)

json.dump(archetypelst, open(os.path.join(parentDict, "structs/poolArchLst.txt"),'w'), sort_keys=True, indent='\t', separators=(',', ': '))
print("Lista Archetipi della pool aggiornata: " + str(len(archetypelst)) + " archetipi\n")

print("Vuoi aggiornare tutti i files? Questo può richiedere tra i 30 e i 50 minuti.")
choice = input("(Y/N):")

if choice.upper() == "Y":
    dictupdate(cards)
    
print("Aggiornamento Completato!")
time.sleep(3)
    



