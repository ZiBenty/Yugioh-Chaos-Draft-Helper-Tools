import json
import io
import os.path
from this import d
from tkinter import CENTER
import sys
import PySimpleGUI as sg
import base64
import PIL.Image
import pathlib
import pandas as pd
import sqlite3 as sql
from datetime import datetime
import DBC
import BP
import CS1
import CS2
import CS3
import CS4
import CS5
import CS6
import CU
import DLG
import DP1
import DP2
import GS1
import GS2
import GS3
import HA
import LC1
import LDS
import MP1
import MP2
import OTS
import RP1
import SP
import TC

#per l'eseguibile, SOSTITUIRE application_path con pathlib.Path(__file__).parent.resolve() per testare
application_path = os.path.dirname(sys.executable)
# poi digitare pyinstaller --onefile Pack_Opener.py nella directory per convertire in .exe

parentDict = pathlib.Path(__file__).parent.resolve()

# ------------------ converte immagine in stringa da 64bytes ---------------------
def convert_to_bytes(file_or_bytes, resize=None):
    '''
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (Union[str, bytes])
    :param resize:  optional new size
    :type resize: (Tuple[int, int] or None)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    '''
    b = open(os.path.join(parentDict, "structs/bans.json"), 'r') #per le carte bandite
    bans = b.readline()
    b.close()
    imgb = PIL.Image.open("pics/banned.png")
    try:
        img = PIL.Image.open(file_or_bytes)
        if ((file_or_bytes.rstrip(".jpg")).lstrip("pics/")) in bans:
            imgc = PIL.Image.open(file_or_bytes)
            imgc.paste(imgb,[0,0])
            img = imgc
    except:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
            if ((file_or_bytes.rstrip(".jpg")).lstrip("pics/")) in bans:
                imgc = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
                imgc.paste(imgb,[0,0])
                img = imgc
        except:
            try:
                dataBytesIO = io.BytesIO(file_or_bytes)
                img = PIL.Image.open(dataBytesIO)
                if ((file_or_bytes.rstrip(".jpg")).lstrip("pics/")) in bans:
                    imgc = PIL.Image.open(dataBytesIO)
                    imgc.paste(imgb,[0,0])
                    img = imgc
            except:
                img = PIL.Image.open("pics/unknown.jpg") #se l'immagine non c'è, usa una immagine default
    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
    with io.BytesIO() as bio:
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()

#Dizionario Codice Set -> Nome Set
f = open(os.path.join(parentDict, "sets/1setCodes.txt"), "r")
contents = f.read()
codeToName = json.loads(contents)
f.close()

#DATABASE CARTE
f = open(os.path.join(parentDict, "structs/card pool.txt"), "r")
dum = f.read()
cards = json.loads(dum)
f.close()

#Carte Bandite
b = open(os.path.join(parentDict, "structs/bans.json"), 'r')
bans = b.readline()
b.close()

#DB decoder
dec = DBC.DBdecoder()

#aggiorna pack corrente
def set_currentPack(name):
    global currentOpenedPack
    global currentSetType
    global currentAltRarity
    currentAltRarity = False
    for code in codeToName.keys():
        if name == codeToName[code]:
            f = open(os.path.join(parentDict, "sets/" + code + ".txt"), "r")
            contents = f.read()
            packCards = json.loads(contents)
            UltiGhosts = None
            f.close()
            try:
                f = open(os.path.join(parentDict, "sets/@" + code + ".txt"), "r")
                contents = f.read()
                #per le carte più rare che potrebbero apparire
                UltiGhosts = json.loads(contents)
                f.close()
                currentAltRarity = True
            except Exception as E:
                #print(f'** Error {E} **')
                pass
            #tutti i pacchetti
            if code in CS1.Core_Set1.sets:
                currentOpenedPack = CS1.Core_Set1()
                currentSetType = "CS1"
            elif code in CS4.Core_Set4.sets:
                currentOpenedPack = CS4.Core_Set4()
                currentSetType = "CS4"
            elif code in HA.Hidden_Arsenal_Like.sets:
                currentOpenedPack = HA.Hidden_Arsenal_Like()
                currentSetType = "HA"
            elif code in CU.Five_Ultras_Like.sets:
                currentOpenedPack = CU.Five_Ultras_Like()
                currentSetType = "CU"
            elif code in MP1.Mega_Pack1.sets:
                currentOpenedPack = MP1.Mega_Pack1()
                currentSetType = "MP1"
            elif code in MP2.Mega_Pack2.sets:
                currentOpenedPack = MP2.Mega_Pack2()
                currentSetType = "MP2"
            elif code in GS1.Gold_Series1.sets:
                currentOpenedPack = GS1.Gold_Series1()
                currentSetType = "GS1"
            elif code in GS2.Gold_Series2.sets:
                currentOpenedPack = GS2.Gold_Series2()
                currentSetType = "GS2"
            elif code in GS3.Gold_Series3.sets:
                currentOpenedPack = GS3.Gold_Series3()
                currentSetType = "GS3"
            elif code in LC1.Legendary_Collection1.sets:
                currentOpenedPack = LC1.Legendary_Collection1()
                currentSetType = "LC1"
            elif code in DP1.Duelist_Pack1.sets:
                currentOpenedPack = DP1.Duelist_Pack1()
                currentSetType = "DP1"
            elif code in LDS.Legenday_Duelists_Season.sets:
                currentOpenedPack = LDS.Legenday_Duelists_Season()
                currentSetType = "LDS"
            elif code in RP1.Reprint_Pack1.sets:
                currentOpenedPack = RP1.Reprint_Pack1()
                currentSetType = "RP1"
            elif code in DLG.Dark_Legends.sets:
                currentOpenedPack = DLG.Dark_Legends()
                currentSetType = "DLG"
            elif code in CS2.Core_Set2.sets:
                currentOpenedPack = CS2.Core_Set2()
                currentSetType = "CS2"
            elif code in CS3.Core_Set3.sets:
                currentOpenedPack = CS3.Core_Set3()
                currentSetType = "CS3"
            elif code in CS5.Core_Set5.sets:
                currentOpenedPack = CS5.Core_Set5()
                currentSetType = "CS5"
            elif code in CS6.Core_Set6.sets:
                currentOpenedPack = CS6.Core_Set6()
                currentSetType = "CS6"
            elif code in TC.Toon_Chaos_Like.sets:
                currentOpenedPack = TC.Toon_Chaos_Like()
                currentSetType = "TC"
            elif code in OTS.OTS_Like.sets:
                currentOpenedPack = OTS.OTS_Like()
                currentSetType = "OTS"
            elif code in SP.Star_Pack.sets:
                currentOpenedPack = SP.Star_Pack()
                currentSetType = "SP"
            elif code in BP.Battle_Pack.sets:
                currentOpenedPack = BP.Battle_Pack()
                currentSetType = "BP"
            elif code in DP2.Duelist_Pack2.sets:
                currentOpenedPack = DP2.Duelist_Pack2()
                currentSetType = "DP2"
            if UltiGhosts is not None:
                for c in UltiGhosts:
                    currentOpenedPack.add_card(UltiGhosts[c], c)
            for c in packCards:
                currentOpenedPack.add_card(packCards[c], c)
            global currentCodePack
            currentCodePack = code
            break

#costanti
SIZE_CARD_FILTER = (300, 431)
SIZE_CARD_PACK = (130, 190)
SIZE_CARD_POOL = (70, 100)
SIZE_IMAGE_PACK = (180, 317)

#tiene in memoria il set da aprire in questo momento 
global currentOpenedPack
currentCodePack = ""
currentSetType = ""
currentAltRarity = False

#sblocca/blocca alcune funzionalità
global customDraftMode
customDraftMode = False
chosenCard = ""
draftedCards = []
global maxRerolls
global remainingRerolls
draftPacks = {}
global iterPacks
global lastPack
global lastPackLay
global nPack
samePack = 1
global allPacks

#variabili per la wishlist
#wishlist: key: set_code, value: list of cards to find
chosenWishCard = None
setsWishCard = []
wishlist = {}
wishlistPack = []

#crea bottoni per pool carte scelte
def place_pool(elem, keyc):
    if keyc != "":
        k = "COL_" + keyc
        return sg.Column([[elem]], pad=(0,0), key = k)
    else:
        return sg.Column([[elem]], pad=(0,0))
    
#crea bottoni per scelta carta
def place_pack(elem, c, rarity):
    rarityTxt = None
    kcol = "COL" + c
    ktxtname = "Name" + c
    ktxtrarity = "Rarity" + c
    #ricerca name
    name = dec.DBdecode("id", c, "name")
    #dà un colore in base alla sua rarità
    if (rarity == "Rare" or rarity == "Mosaic Rare" or rarity == "Starfoil Rare" or rarity == "Shatterfoil Rare"):
        rarityTxt = sg.Text(rarity, key = ktxtrarity, size=(15,0), justification="center", text_color="#c3e5ff", font=('Arial', 10, "bold"))
    elif rarity == "Super Rare":
        rarityTxt = sg.Text(rarity, key = ktxtrarity, size=(15,0), justification="center", text_color="#f6ffa5", font=('Arial', 10, "bold"))
    elif rarity == "Ultra Rare":
        rarityTxt = sg.Text(rarity, key = ktxtrarity, size=(15,0), justification="center", text_color="#7bffc4", font=('Arial', 10, "bold"))
    elif "Secret Rare" in rarity:
        rarityTxt = sg.Text(rarity, key = ktxtrarity, size=(15,0), justification="center", text_color="#ffdb75", font=('Arial', 10, "bold"))
    elif (rarity == "Ultimate Rare" or rarity == "Starlight Rare" or rarity == "Collector's Rare"):
        rarityTxt = sg.Text(rarity, key = ktxtrarity, size=(15,0), justification="center", text_color="#ff892a", font=('Arial', 10, "bold"))
    elif "Ghost" in rarity:
        rarityTxt = sg.Text(rarity, key = ktxtrarity, size=(15,0), justification="center", text_color="#7fb5db", font=('Arial', 10, "bold"))
    elif "Gold Rare" in rarity:
        rarityTxt = sg.Text(rarity, key = ktxtrarity, size=(15,0), justification="center", text_color="#ffd700", font=('Arial', 10, "bold"))
    else:
        rarityTxt = sg.Text(rarity, key = ktxtrarity, size=(15,0), justification="center")
    return sg.Column([[elem],[sg.Text(name, size=(15,0), justification="center", key = ktxtname)],[rarityTxt]], pad=(10,10), background_color=None, key = kcol)
            
#crea layout per i pacchetti e la pool di carte
#pack: pacchetto
#cnum: numero di carte per riga
#sz: grandezza carte da visualizzare
def pack_layout(pack, cnum, sz, isPackPool):
    i = 0
    col = []
    row = []
    #print(str(pack))
    #visualizzare pool pacchetto
    if isPackPool:
            rarities = list(pack[0].values()) + list(pack[1].values())
            raritiestxt = {}
            registeredcards = []
            for r in rarities:
                if r not in raritiestxt:
                    raritiestxt[r] = []
            for c in pack[0]:
                raritiestxt[pack[0][c]].append(c)
            if pack[1] != {}:
                for c in pack[1]:
                        raritiestxt[pack[1][c]].append(c)
            n = 0
            for r in raritiestxt:
                col.append([sg.Text(r, justification = CENTER, size = (50, 1), font = ("Any 18"))])
                for c in raritiestxt[r]:
                    if c not in registeredcards:
                        registeredcards.append(c)
                        kca = "PACK_" + c
                    else:
                        kca = "PACK_" + c + "alt" + str(n)
                        n += 1
                    row.append(place_pool(sg.Button("", image_data = convert_to_bytes("pics/" + c + ".jpg", sz), metadata = c, key = kca), kca))
                    if i == cnum-1:
                        col.append(row)
                        i = 0
                        row = []
                    else:
                        i = i+1
                if len(row)!=0:
                    col.append(row)
                    i = 0
                    row = []
    else:
        for c in pack:
            #visualizzare pacchetto
            if sz == SIZE_CARD_PACK:
                kca = "CARD" + c
                row.append(place_pack(sg.Button("", image_data = convert_to_bytes("pics/" + c + ".jpg", sz), metadata = c, key = kca), c, pack[c]))
            #visualizzare carte draftate
            else:
                kca = "POOL_CARD" + c
                row.append(place_pool(sg.Button("", image_data = convert_to_bytes("pics/" + c + ".jpg", sz), metadata = c, key = kca), ""))
            if i == cnum-1:
                col.append(row)
                i = 0
                row = []
            else:
                i = i+1
        if len(row)!=0:
            col.append(row)
    return col

def saveDraft():
    #print(draftedCards)
    with open(os.path.join(parentDict, "structs/card pool.txt"), "w") as card_pool:
        for card in draftedCards:
            if card.rstrip("\n") in cards:
                cards[card.rstrip("\n")] += 1
            else:
                cards[card.rstrip("\n")] = 1
        json.dump(cards, card_pool)

#per il layout menu        
SetNames = []
#stringhe generali di set da NON includere
substrings = ["Tins", "Demo", "Terminal", "Egyptian", "Exclusive", "GX",
              "Decks", "McDonald", "Round Table", "Samurai", "Speed Duel Tournament", 
              "Space-Time", "Promotion", "Championship", "X-Saber", "Calendar",
              "Elemental Hero", "Beginner", "Remote Duel", "Collector", "Zexal",
              "Anniversary", "Alternative White Dragon", "Duelist raft Collection Tin",
              "Master Collection Volume", "Theater", "participation", "Battle Pack Tournament", 
              "prize", "Speed Duel:", "Reinforcements", "Duelist Pack Collection Tin"]

#togliamo tutti quelli che non sono pacchetti draftabili
for code in codeToName.keys():
    #LUUUUNGA condizione che esclude i pacchetti non validi
    if "@" not in code and not (any([substring in codeToName[code] for substring in substrings])) and not ((codeToName[code] == "Movie Pack") or (codeToName[code] == "2019 Gold Sarcophagus Tin") or (codeToName[code] == "Duel Disk - Yusei Version") or (codeToName[code] == "Forbidden Legacy") or (codeToName[code] == "Premium Collection Tin") or (codeToName[code] == "Spell Ruler") or (codeToName[code] == "Legendary Collection") or (codeToName[code] == "Legendary Collection 2: The Duel Academy Years") or (codeToName[code] == "Legendary Collection 3: Yugi's World") or (codeToName[code] == "Legendary Collection 4: Joey's World") or (codeToName[code] == "Legendary Collection 5D's") or (codeToName[code] == "Legendary Collection Kaiba") or (codeToName[code] == "Duel Devastator") or (codeToName[code] == "Light and Darkness Power Pack") or (codeToName[code] == "Hidden Arsenal: Chapter 1")):
        SetNames.append(codeToName[code])

#Lista nomi carte (per wishlist)
conn = sql.connect("structs/cards.cdb")
cur = conn.cursor()
results = cur.execute("SELECT name FROM texts")
df = pd.DataFrame(results)
cardNames = []

for c in df.values:
    cardNames.append(c[0])

#fills wishlist from saved file
f = open(os.path.join(parentDict, "wishlist.txt"), "r")
sum = f.read()
wishlist = json.loads(sum)
f.close()

#method to visualize wishlist
def wishlistToString():
    listc = []
    listn = []
    for set in wishlist.keys():
        for card in wishlist[set]:
            if card not in listc:
                listc.append(card)
                listn.append(str(dec.DBdecode("id", card, "name")))
    return listn

# ---------------------------- Menu layout ---------------------------------
custom_draft_columns = [
    [
        sg.Column([
            [sg.Multiline(size=(20, 9), autoscroll=True, visible=False, key="-CUSTOM DRAFT LIST-")]
        ], key="-CUSTOM COL1-"),
        sg.VSeperator(color=sg.DEFAULT_BACKGROUND_COLOR, pad=(0,0)),
        sg.Column([
            [sg.Text("N. of rerolls:", key="-TXT REROLLS-")],
            [sg.Input(default_text="0", size=(2, 1), enable_events=True, key="-IN REROLLS-")],
            [sg.Text("N. of selected pack to add:", key="-TXT NPACKS-")],
            [sg.Input(default_text="1", size=(2, 1), enable_events=True, key="-IN NPACKS-")],
            [sg.Button("Add Pack to Draft")],
            [sg.Combo(["Name", "Name (Z-A)", "Release Date", "Release Date (Oldest)"], enable_events=True, key="-SORT MODE-")]
        ], vertical_alignment="top", visible=False, key="-CUSTOM COL2-")
    ],
    [
        sg.Button("Continue Last Draft", visible=False)
    ]
    
]
pack_filter_column = [
    [
        sg.Text("Cerca e seleziona un pacchetto"),
    ],
    [
        sg.Input(do_not_clear=True, size=(20,1), enable_events=True, key='-INPUT-'),
    ],
    [
        sg.Listbox(sorted(SetNames), enable_events=True, size=(50,20), key="-PACKS LIST-"),
    ],
    [
        sg.Button("Open Selected Pack"),
    ],
    [
        sg.Button("Custom Draft Mode"),
        sg.Button("Start Custom Draft", visible=False),
    ],
    [
        sg.Column(custom_draft_columns)
    ]
]

pack_info_column = [
        [
            sg.Button("", image_data = None, key="-PACKIMAGE-")
        ],
        [
            sg.Text(size=(30, 1), key="-PACKDESC-")
        ],
        [
            sg.Text(size=(30, 8), key="-RARITY-")
        ],
]

packdraft = [
    [
        sg.Column(pack_filter_column, vertical_alignment="top"),
        sg.VSeperator(color=sg.DEFAULT_BACKGROUND_COLOR, pad=(0,0)),
        sg.Column(pack_info_column),
    ]
]

name_select = [
    [
        sg.Text("Cerca una carta da aggiungere alla Wishlist"),
    ],
    [
        sg.Input(do_not_clear=True, size=(30,1), enable_events=True, key='-INPUTNAME-'),
    ],
    [
        sg.Listbox(sorted(cardNames), enable_events=True, size=(30,8), key="-NAMES LIST-"),
    ],
    [
        sg.Button("Add to Wishlist"), sg.Button("Delete from Wishlist"), sg.Button("Clear Wishlist"),
    ],
    [
        sg.Text("WISHLIST:")
    ],
    [
        sg.Listbox(wishlistToString(), enable_events=True, size=(30, 15), key="-WISHLISTSAVED-"),
    ]
]

card_pools_stats = [
            [sg.Image(key="-WISH IMAGE-")],
            [sg.Text(size=(40, 15), key="-WISHLIST-")],
        ]

wishlistLayout = [
    [
        sg.Column(name_select, vertical_alignment="top"),
        sg.VSeperator(color=sg.DEFAULT_BACKGROUND_COLOR, pad=(0,0)),
        sg.Column(card_pools_stats, vertical_alignment="top"),
    ]
]

menu = [
    [
        sg.Column(packdraft, vertical_alignment="top"),
        sg.VSeperator(),
        sg.Column(wishlistLayout, vertical_alignment="top"),
    ]
]
#---------------------------------Finestre-------------------------------------
def make_winmenu():
    return sg.Window("Pack Opener", menu, resizable=True, finalize=True)

#supporto per make_WinPack, liste con tutti i possibili layout per ogni tipo di pacchetto
Nine = ["CS1", "CS2", "CS3", "CS4", "CS5", "CS6", "TC", "MP1", "MP2", "GS1", "LC1", "LDS", "RP1", "DLG"]
Five = ["HA", "CU", "GS2", "GS3", "OTS", "DP1", "DP2", "SP", "BP"]

def make_winPack(pack, name, code):
    card_viewer_column = [
        [sg.Image(key="-IMAGE-")],
        [sg.Text(size=(40, 2), key="-NAME-")],
        [sg.Text(size=(40, 2), key="-INFO-")],
        [sg.Text(size=(40, 15), key="-DESC-")],
    ]
    #cambiare tipo generazione a seconda n carte
    laypack = None
    if(currentSetType in Nine):
        laypack = pack_layout(pack, 4, SIZE_CARD_PACK, False)
    elif(currentSetType in Five):
        laypack = pack_layout(pack, 3, SIZE_CARD_PACK, False)
    #controllo pacchetto in wishlist
    wished = False
    if code in wishlist.keys():
        wished = True
    #carte da trovare in pacchetto
    #wishedcards = "- "
    global wishlistPack
    wishlistPack = []
    if wished:
        for card in wishlist[code]:
            #wishedcards += dec.DBdecode("id", card, "name") + " - "
            wishlistPack.append(card)
    #controllo trovata carta wishlist
    found = False
    foundcards = "- "
    for c in pack.keys():
        if wished and c in wishlist[code]:
            foundcards += dec.DBdecode("id", c, "name") + " - " 
            found = True
    lay = [
        [
            sg.Text("You found a card in your wishlist!\n" + foundcards if found else ("A card in your wishlist can be found here (" + str(len(wishlistPack)) + " cards):" if wished else ""), text_color="#00FF00" if found else "#ffffff", justification="center", font=('Arial', 12, "bold") ),
        ],
        [
            sg.Button("Look here!", visible = False if found else True)
        ],
        [
            sg.Frame("Choose one card", [
                [sg.Column(laypack, size=(650, 600), key="-OPEN PACK-", scrollable=True,  vertical_scroll_only=True, expand_x=True, element_justification='c')],
                [sg.Button("Reroll"), sg.Text("", key = "-N REROLLS-"), sg.Text("/"), sg.Text("", key = "-TOT REROLLS-"),
                sg.Button("Next Pack"), sg.Text("", key = "-N PACKS-"), sg.Text("/"), sg.Text("", key = "-TOT PACKS-"), sg.Text("", key = "-NEXT PACK-"),
                sg.Button("Show Drafted Cards")]
            ], vertical_alignment="top"),
            sg.VSeperator(),
            sg.Column(card_viewer_column)
        ],
        
    ]
    return sg.Window(str(name), lay, resizable=True, finalize=True, grab_anywhere=True, element_justification='center')

#mostra pool di carte. Se packList = True, mostra carte del pacchetti, altrimenti mostra lista carte draftate/in wishlist
def make_winPool(listc, packList):
    if not packList:
        lay = [[sg.Frame("Card Pool", [
            [sg.Column(pack_layout(listc, 4, SIZE_CARD_POOL, False), size=(350, 430), key="-DRAFTED CARDS-", scrollable=True,  vertical_scroll_only=True, expand_x=True)]
        ])]]
    else:
        card_viewer_column = [
            [sg.Image(key="-IMAGE-")],
            [sg.Text(size=(40, 2), key="-NAME-")],
            [sg.Text(size=(40, 2), key="-INFO-")],
            [sg.Text(size=(40, 15), key="-DESC-")],
        ]
        lay = [
            [
                sg.Frame("Pack Pool", [
                [sg.Column(pack_layout(listc, 5, SIZE_CARD_PACK, True), key="-PACK POOL-", scrollable=True,  vertical_scroll_only=True, expand_x=True)]
                ]),
                sg.VSeperator(),
                sg.Column(card_viewer_column)
            ]
        ]
    return sg.Window("Card Pool", lay, resizable=True, finalize=True, grab_anywhere=True)

#updates all variables and their visual representations in window2 in common with all changes
def update_draft_win():
    window2.Element("-N REROLLS-").Update(remainingRerolls)
    window2.Element("-TOT REROLLS-").Update(maxRerolls)
    window2.Element("-N PACKS-").Update(nPack)
    window2.Element("-TOT PACKS-").Update(allPacks)

global window1
window1 = make_winmenu()
window1.maximize()

global window2
window2 = None

global window3
window3 = None

while True:
    window, event, values = sg.read_all_windows()
    # End program if user closes window
    if event == "Exit" or event == sg.WIN_CLOSED:
        if window == window1:
            break
        elif window == window2 and customDraftMode:
            window.close()
            window1["Continue Last Draft"].update(visible = True)
        else:
            window.close()
    #----------------------------Eventi Finestra Menu-----------------------
    #ricerca pacchetti nella lista di pacchetti
    if event == "-INPUT-" and values["-INPUT-"] != "":
        search = values["-INPUT-"].casefold()
        new_values = [x for x in SetNames if search in x.casefold()]
        window.Element('-PACKS LIST-').Update(new_values)
    elif event == "-INPUT-":
        window.Element('-PACKS LIST-').Update(sorted(SetNames))
    #tasto apre pacchetto selezionato
    if event == "Open Selected Pack" and window1 and window1["-PACKS LIST-"].get() != []:
        set_currentPack(values["-PACKS LIST-"][0])
        #ritorna un dizionario con chiave id, valore rarità
        pack = currentOpenedPack.generate_pack(currentCodePack)
        window2 = make_winPack(pack, values["-PACKS LIST-"][0], currentCodePack)
        window2.maximize()
        window2["Next Pack"].update(visible = False)
    #mostra informazioni del pacchetto selezionato
    if event == "-PACKS LIST-":
        for code in codeToName.keys():
            if codeToName[code] == values["-PACKS LIST-"][0]:
                filename = os.path.join("pics/set_pics", code + ".jpg")
                sz = SIZE_IMAGE_PACK
                #immagine pacchetto
                window["-PACKIMAGE-"].update(image_data=convert_to_bytes(filename, sz))
                #info pacchetto
                f = open(os.path.join(parentDict, "sets/1SetInfo.txt"), "r")
                contents = f.read()
                packsInfos = json.loads(contents)
                f.close()
                window["-PACKDESC-"].update(packsInfos[code]["totrelease"].replace("\u2022", ""))
                lst = packsInfos[code]["rarities"]
                toPrint = ""
                for l in lst:
                    toPrint += l.replace("\u2022", "") + "\n"
                window["-RARITY-"].update(toPrint)
                break
    #se si clicca sull'immagine del pacchetto, si apre la lista delle carte che si possono trovare
    if event == "-PACKIMAGE-" and window1["-PACKS LIST-"].get() != []:
        cardPack = {}
        cardPackAlt = {}
        cardlst = {}
        set_currentPack(values["-PACKS LIST-"][0])
        f = open(os.path.join(parentDict, "sets/" + code + ".txt"), "r")
        contents = f.read()
        cardPack = json.loads(contents)
        f.close()
        if currentAltRarity is True:
            try:
                f = open(os.path.join(parentDict, "sets/@" + code + ".txt"), "r")
                contents = f.read()
                cardPackAlt = json.loads(contents)
                f.close()
            except:
                print("@" + code + " file not found")
        window3 = make_winPool([cardPack, cardPackAlt], True)
    #ricerca pacchetti nella lista di nomi
    if event == "-INPUTNAME-" and values["-INPUTNAME-"] != "":
        search = values["-INPUTNAME-"].casefold()
        new_values = [x for x in cardNames if search in x.casefold()]
        window.Element('-NAMES LIST-').Update(new_values)
    elif event == "-INPUTNAME-":
        window.Element('-NAMES LIST-').Update(sorted(cardNames))
    #visualizza carta e le rarità nei vari pacchetti
    if event == '-NAMES LIST-' or event == '-WISHLISTSAVED-':
        idc = None
        if event == '-NAMES LIST-':
            idc = dec.DBdecode("name", values['-NAMES LIST-'][0], "id")
        elif event == '-WISHLISTSAVED-':
            idc = dec.DBdecode("name", values['-WISHLISTSAVED-'][0], "id")
        f = open(os.path.join(parentDict, "structs/dictsetcodes.txt"), "r")
        dum = f.read()
        cardToSets = json.loads(dum)
        f.close()
        filename = os.path.join("pics", str(idc) + ".jpg")
        window["-WISH IMAGE-"].update(data=convert_to_bytes(filename, SIZE_CARD_PACK))
        chosenWishCard = idc
        try:
            S = cardToSets[str(idc)]
        except:
            S = None
        if(S != None):
            setsToPrint = ""
            checkedSets = []
            for set in S:
                set_code = set.split('-', 1)[0]
                #apre i files dei set e inizia a creare la stringa da stampare
                if set_code not in checkedSets:
                    try:
                        f = open(os.path.join(parentDict, "sets/@" + set_code + ".txt"), "r")
                        sum = f.read()
                        setCardsSpec = json.loads(sum)
                        f.close()
                        setsToPrint += codeToName[set_code] + ": " + setCardsSpec[str(idc)] + "\n"
                    except Exception as e:
                        #print(e)
                        pass
                    finally:
                        try:
                            f = open(os.path.join(parentDict, "sets/" + set_code + ".txt"), "r")
                            sum = f.read()
                            setCards = json.loads(sum)
                            f.close()
                            setsToPrint += codeToName[set_code] + ": " + setCards[str(idc)] + "\n"
                        except Exception as e:
                            #print(e)
                            pass
                    checkedSets.append(set_code)
            setsWishCard = checkedSets
            window["-WISHLIST-"].update(setsToPrint)
        else:
            window["-WISHLIST-"].update("Cannot be found in packs")
    #aggiunge alla wishlist
    if event == "Add to Wishlist":
        for set in setsWishCard:
            if set not in wishlist.keys():
                wishlist[set] = []
                wishlist[set].append(str(chosenWishCard))
            elif str(chosenWishCard) not in wishlist[set]:
                wishlist[set].append(str(chosenWishCard))
        json.dump(wishlist, open(os.path.join(parentDict, "wishlist.txt"), "w"))
        window1["-WISHLISTSAVED-"].update("")
        window1["-WISHLISTSAVED-"].update(wishlistToString())
    #salva la wishlist in un file
    if event == "Delete from Wishlist":
        if window1["-WISHLISTSAVED-"].get() != []:
            for set in setsWishCard:
                if str(chosenWishCard) in wishlist[set]:
                    wishlist[set].remove(str(chosenWishCard))
        json.dump(wishlist, open(os.path.join(parentDict, "wishlist.txt"), "w"))
        window1["-WISHLISTSAVED-"].update("")
        window1["-WISHLISTSAVED-"].update(wishlistToString())
    #cancella tutti i valori dalla variabile wishlist
    if event == "Clear Wishlist":
        wishlist = {}
        json.dump(wishlist, open(os.path.join(parentDict, "wishlist.txt"), "w"))
        window1["-WISHLISTSAVED-"].update("")
        window1["-WISHLISTSAVED-"].update(wishlistToString())
    #------------------------Custom Draft Mode Handling----------------------------------
    #mostra/nasconde elementi gui per la custom draft mode
    if event == "Custom Draft Mode" and window1:
        if customDraftMode is False:
            customDraftMode = True
            window.Element("Start Custom Draft").Update(visible=True)
            window.Element("-CUSTOM DRAFT LIST-").Update(visible=True)
            window.Element("-CUSTOM COL2-").Update(visible=True)
            window.Element("-SORT MODE-").Update(visible=True)
        else:
            customDraftMode = False
            window.Element("Start Custom Draft").Update(visible=False)
            window.Element("-CUSTOM DRAFT LIST-").Update(visible=False)
            window.Element("-CUSTOM COL2-").Update(visible=False)
            window.Element("-SORT MODE-").Update(visible=False)
    #fa partire il draft in base ai valori passati
    if event == "Start Custom Draft":
        if values["-CUSTOM DRAFT LIST-"] != "":
            packToDate = {}
            #info pacchetto
            f = open(os.path.join(parentDict, "sets/1SetInfo.txt"), "r")
            contents = f.read()
            packsInfos = json.loads(contents)
            f.close()
            tstr = ""
            i = 0
            for c in values["-CUSTOM DRAFT LIST-"]:
                if c == "\n" or i == len(values["-CUSTOM DRAFT LIST-"])-1:
                    if c != "\n":
                        tstr += c
                    numStr = tstr.split("|",1)[1]
                    packName = tstr.split("|",1)[0]
                    #LOB crea problemi :)
                    if packName == "The Legend of Blue Eyes White Dragon":
                        packName = "Legend of Blue Eyes White Dragon"
                    draftPacks[packName] = int(numStr)
                    infos = ""
                    for code in codeToName.keys():
                        if codeToName[code] == packName:
                            infos = packsInfos[code]["totrelease"].replace("\u2022", "").split(" Cards  ", 1)
                            date_str = infos[1].rstrip(" ").lstrip("Released ")
                            packToDate[packName] = datetime.strptime(date_str, '%Y-%m-%d')
                            break
                    tstr = ""
                else:
                    tstr += c
                i += 1
            maxRerolls = int(values["-IN REROLLS-"])
            remainingRerolls = int(values["-IN REROLLS-"])
            #crea un iteratore dei pacchetti scelti, e inizia dal primo
            #itera i pachhetti nell'ordine scelto
            selectedSort = list(draftPacks.keys())
            selectedSort.sort()
            sortMode = values["-SORT MODE-"]
            if sortMode != "":
                if sortMode == "Name (Z-A)":
                    selectedSort.reverse()
                elif sortMode == "Release Date (Oldest)":
                    dates = list(packToDate.values())
                    dates.sort()
                    pack_sorted = []
                    for date in dates:
                        for pack in packToDate.keys():
                            if packToDate[pack] == date:
                                pack_sorted.append(pack)
                    selectedSort = pack_sorted
                elif sortMode == "Release Date":
                    dates = list(packToDate.values())
                    dates.sort()
                    dates.reverse()
                    pack_sorted = []
                    for date in dates:
                        for pack in packToDate.keys():
                            if packToDate[pack] == date:
                                pack_sorted.append(pack)
                    selectedSort = pack_sorted
            iterPacks = iter(selectedSort)
            lastPack = next(iterPacks)
            nPack = 1
            samePack = draftPacks[lastPack]
            allPacks = 0
            for p in draftPacks.keys():
                allPacks += draftPacks[p]
            set_currentPack(lastPack)
            pack = currentOpenedPack.generate_pack(currentCodePack)
            lastPackLay = pack
            window2 = make_winPack(pack, lastPack, currentCodePack)
            window2.maximize()
            update_draft_win()
    if event == "Continue Last Draft":
        window2 = make_winPack(lastPackLay, codeToName[currentCodePack], currentCodePack)
        window2.maximize()
        update_draft_win()
        window1["Continue Last Draft"].update(visible = False)
    #aggiunge il pacchetto alla lista di pacchetti da draftare
    if event == "Add Pack to Draft" and window1.Element("-PACKS LIST-").get() != []:
        tstr = ""
        finalstr = window1.Element("-CUSTOM DRAFT LIST-").get()
        if finalstr == "":
            tstr += values["-PACKS LIST-"][0] + "|" + values["-IN NPACKS-"]
        else:
            tstr += "\n" + values["-PACKS LIST-"][0] + "|" + values["-IN NPACKS-"]
        window1.Element("-CUSTOM DRAFT LIST-").Update(finalstr+tstr)
    #evita di scrivere caratteri diversi da numeri nello spazio dei reroll
    if event == "-IN REROLLS-":
        for c in values["-IN REROLLS-"]:
            if c < "0" or c > "9":
                window.Element("-IN REROLLS-").Update("0")
    if event == "-IN NPACKS-":
        for c in values["-IN NPACKS-"]:
            if c < "0" or c > "9":
                window.Element("-IN NPACKS-").Update("1")
    #--------------------------Eventi Finestra Draft-------------------------
    #Mostra e salva in memoria carta selezionata
    if event != None and "CARD" in event and "POOL_" not in event:
        element = window[event]
        for key in window2.key_dict.keys():
            if not isinstance(key, int) and "Name" in key:
                window2[key].Widget.config(background='#64778d')
        window2["Name"+element.metadata].Widget.config(background='green')
        chosenCard = element.metadata
    #mostra informazioni carta selezionata
    if event != None and ("CARD" in event or "PACK_" in event):
        element = window[event]
        if "CARD" in event:
            window = window2
        try:
            #show card informations
            sz = SIZE_CARD_FILTER
            filename = os.path.join("pics", element.metadata + ".jpg")
            window["-IMAGE-"].update(data=convert_to_bytes(filename, sz))
            idc = element.metadata.rstrip(".jpg")
            try:
                qnt = cards[str(idc)]
            except:
                qnt = 0
            name = dec.DBdecode("id", idc, "name") + "\nQnt: " + str(qnt)
            window["-NAME-"].update(name)
            types = dec.DBdecode("id", idc, "type")
            attr = dec.DBdecode("id", idc, "attribute")
            race = dec.DBdecode("id", idc, "race")
            level = dec.DBdecode("id", idc, "level")
            atk = dec.DBdecode("id", idc, "atk")
            defe = dec.DBdecode("id", idc, "def")
            first = types + ((" [" + attr + " " + race + "] ") if (attr != "" and race != "") else "")
            second = ("Level/Rank: " if (level != 0 and "Link" not in str(types)) else ("Link Rating: " if (level != 0 and "Link" in str(types)) else "")) + ((str(level) + " ") if level != 0 else "")
            third = (("\nATK: " + str(atk) + "  DEF: " + str(defe)) if ("Trap" not in types and "Spell" not in types) else "")
            info = first + second + third
            window["-INFO-"].update(info)
            if (idc) in bans:
                window["-DESC-"].update("***BANNED***\n" + dec.DBdecode("id", idc, "desc"))
            else:
                window["-DESC-"].update(dec.DBdecode("id", idc, "desc"))
        except Exception as E:
            print(E)
            pass        # something weird happened making the full filename
    #rerolla il pacchetto
    if event == "Reroll":
        if draftPacks == {} or customDraftMode is False:
            window2.close()
            pack = currentOpenedPack.generate_pack(currentCodePack)
            lastPackLay = pack
            window2 = make_winPack(pack, codeToName[currentCodePack], currentCodePack)
            window2.maximize()
        elif customDraftMode is True and remainingRerolls > 0:
            remainingRerolls -= 1
            window2.close()
            pack = currentOpenedPack.generate_pack(currentCodePack)
            lastPackLay = pack
            window2 = make_winPack(pack, codeToName[currentCodePack], currentCodePack)
            window2.maximize()
            update_draft_win()
    if event == "Show Drafted Cards":
        window3 = make_winPool(draftedCards, False)
    if event == "Look here!":
        window3 = make_winPool(wishlistPack, False)
    #passa al prossimo pacchetto
    if event == "Next Pack" and customDraftMode is True:
        if nPack < allPacks:
            if samePack != 1:
                draftedCards.append(chosenCard)
                nPack += 1
                window2.close()
                pack = currentOpenedPack.generate_pack(currentCodePack)
                lastPackLay = pack
                window2 = make_winPack(pack, lastPack, currentCodePack)
                window2.maximize()
                update_draft_win()
                samePack -= 1
            else:
                draftedCards.append(chosenCard)
                nPack += 1
                lastPack = next(iterPacks)
                window2.close()
                set_currentPack(lastPack)
                samePack = draftPacks[lastPack]
                pack = currentOpenedPack.generate_pack(currentCodePack)
                lastPackLay = pack
                window2 = make_winPack(pack, lastPack, currentCodePack)
                window2.maximize()
                update_draft_win()
        else:
            draftedCards.append(chosenCard)
            customDraftMode = False
            maxRerolls = 0
            remainingRerolls = 0
            draftPacks = {}
            iterPacks = None
            lastPack = ""
            nPack = 0
            window2.close()
            #dopo averle salvate, svuota la lista samePack = 1
            saveDraft()
            draftedCards = []

#---------------------------------- Close & Exit ---------------------------------
f.close()
window1.close()
if window2 != None:
    window2.close()
if window3 != None:
    window3.close()
