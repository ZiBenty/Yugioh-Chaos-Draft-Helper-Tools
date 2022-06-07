import PySimpleGUI as sg
import os.path
import json
import io
import base64
import PIL.Image
import sys
import DBC
import pathlib
import time

#per l'eseguibile, SOSTITUIRE application_path con pathlib.Path(__file__).parent.resolve() per testare
application_path = os.path.dirname(sys.executable)
# poi digitare pyinstaller --onefile Draft_Pool_Filter.py nella directory per convertire in .exe

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
        
# --------------------------------------------------- STRUTTURE DATI PER IL PROGRAMMA ---------------------------------------------------------

#DATABASE CARTE
f = open(os.path.join(parentDict, "structs\card pool.txt"), "r")
dum = f.read()
cards = json.loads(dum)
f.close()

#lista di id carta.jpg
clist = []
for c in cards.keys():
    clist.append(c.rstrip("\n")+".jpg")

#lista per visualizzazione veloce immagini
temp_images = []
y = 1

#DB decoder
dec = DBC.DBdecoder()

#Lista per combo Archetipo
f = open(os.path.join(parentDict, "structs\poolArch.txt"), "r")
dum = f.read()
archetype = json.loads(dum)
f.close()

f = open(os.path.join(parentDict, "structs\poolArchLst.txt"), "r")
dum = f.read()
archetypelst = json.loads(dum)
f.close()
       
#------------------------------------------------------------------------------- FINESTRE ---------------------------------------------------------------------------

#Prepara le strutture con i valori per le Combo di filtraggio
types = {"": [], "Monster": ["", "Normal", "Normal Tuner", "Effect", "Flip",
                    "Spirit", "Union", "Gemini", "Toon", "Tuner", "Ritual",
                    "Fusion", "Synchro", "Synchro Tuner", "XYZ",
                    "Pendulum Normal", "Pendulum", "Link"],
        "Spell": ["", "Normal", "Ritual", "Quick-Play", "Continuos",
                  "Equip", "Field"],
        "Trap": ["", "Normal", "Continuos", "Counter"]}

races = {"": [], "Monster": ["", "Warrior", "Spellcaster", "Fairy", "Fiend",
                             "Zombie", "Machine", "Aqua", "Pyro", "Rock",
                             "Winged Beast", "Plant", "Insect", "Thunder", "Dragon",
                             "Beast", "Beast-Warrior", "Dinosaur", "Fish", "Sea Serpent",
                             "Reptile", "Psychic", "Divine-Beast", "Creator God", "Wyrm",
                             "Cyberse"]}
attributes = {"": [], "Monster": ["", "EARTH", "WATER", "FIRE", "WIND", "LIGHT", "DARK", "DIVINE"]}

#Costanti Grandezze
SIZE_CARD_POOL = (70, 100)
CARD_IMAGE_SIZE = (300, 431)

#Aggiorna la lista per visualizzare velocemente le immagini
def updateImages(listc):
    global temp_images
    if temp_images != []:
        temp_images = []
    n = 0
    temp_listc = []
    for c in listc:
        temp_listc.append(c)
        n += 1
        if n % 16 == 0:
            temp_images.append(temp_listc)
            temp_listc = []
            n = 0
    if n != 0:
        temp_images.append(temp_listc)
        temp_listc = []
        n = 0

#Piazza un bottone in una colonna (evita cambiamento di layout)
def place(elem):
    return sg.Column([[elem]], pad=(0,0))

#Crea disposizione delle carte filtrate per la visualizzazione(DA CAMBIARE)
def pool_cards(listc):
    i = 0
    controw = 0
    col = []
    row = []
    n = 0
    updateImages(listc)
    for c in temp_images[0]:
        kca = "CARD" + str(n)
        n += 1
        row.append(place(sg.Image(data = convert_to_bytes("pics/" + c, SIZE_CARD_POOL), enable_events = True, metadata = c, key = kca)))
        if i == 3:
            col.append(row)
            controw = controw+1
            i = 0
            row = []
        else:
            i = i+1
    if len(row)!=0:
        col.append(row)
    return col

def vscroll(event):
    delta = int(event.delta/120)
    global y
    y -= delta
    if y < 1:
        y = 1
    if y > len(temp_images):
        y = len(temp_images)
    window1.write_event_value("Refresh", ())
    window1['V_Scrollbar'].update(value = y)

# --------------------------- window layout in 2 columns -------------------
option = {'resolution':1, 'pad':(0, 0), 'disable_number_display':False,
    'enable_events':True}

card_list_column = [
    [
        sg.Text("Filters"),
    ],
    [
        sg.Text("Category:"),
        sg.Combo(list(types.keys()), enable_events=True, default_value="", key="-TYPE FILTER-"),
        sg.Combo([], enable_events=True, default_value="", size=(15, 0), key="-TYPESON FILTER-"),        
    ],
    [
        sg.Text("Attribute:"),
        sg.Combo([], enable_events=True, default_value="", size=(10, 0), key="-ATTR FILTER-"),
        sg.Text("Type:"),
        sg.Combo([], enable_events=True, default_value="", size=(10, 0), key="-RACE FILTER-")
    ],
    [
        sg.Text("Level/Rank:"),
        sg.Input(size=(5, 0), enable_events=True, key="-LVL FILTER-"),
        sg.Text("ATK:"),
        sg.Input(size=(5, 0), enable_events=True, key="-ATK FILTER-"),
        sg.Text("DEF"),
        sg.Input(size=(5, 0), enable_events=True, key="-DEF FILTER-"),
    ],
    [
        sg.Text("Search:"),
        sg.Input(size=(25, 1), enable_events=True, key="-SEARCHES-"),
        sg.Button("Reset"),
    ],
    [
        sg.Text("Archetype:"),
        sg.Combo(archetypelst, enable_events=True, size=(15, 5), key="-ARCH FILTER-"),
        sg.Text("", key="-ARCH-")
    ],
    [
        sg.Frame("Card Pool", [[sg.Column(pool_cards(clist), size=(310, 430), key="-CARD LIST-", expand_x=True), 
        sg.Slider(range=(len(temp_images), 1), default_value=1, size=(21, 24), orientation='v', **option, key='V_Scrollbar')]])
    ]
]

#---------------------------- card viewer coloumn --------------------------
card_viewer_column = [
    [sg.Text("Choose a card from list on left:")],
    [sg.Image(key="-IMAGE-")],
    [sg.Text(size=(40, 2), key="-NAME-")],
    [sg.Text(size=(40, 2), key="-INFO-")],
    [sg.Column([[sg.Text(size=(38, 20), key="-DESC-")]], size = (350, 450), scrollable = True, vertical_scroll_only = True, visible = False, key = "-COL_TEXT-")]
]

# ---------------------------- Full layout window1 ---------------------------------
layout = [
    [
        sg.Column(card_list_column, vertical_alignment="top"),
        sg.VSeperator(),
        sg.Column(card_viewer_column, vertical_alignment="top"),
    ]
]

#crea una finestra di tipo window1
def make_win1():
    win = sg.Window("Chaos Draft Card Pool", layout, resizable=True, finalize=True)
    return win

#finestra principale
global window1
window1 = make_win1()
window1["-LVL FILTER-"].bind("<Return>", "_Enter")
window1["-ATK FILTER-"].bind("<Return>", "_Enter")
window1["-DEF FILTER-"].bind("<Return>", "_Enter")
window1["-SEARCHES-"].bind("<Return>", "_Enter")
window1.TKroot.bind('<MouseWheel>', vscroll)
window1.bind('<Configure>', "Resizing")

#se la stringa è un numero, lo ritorna, altrimenti ritorna None
def checkint(num):
    if num.isdigit():
        return int(num)
    elif num == "?":
        return "?"
    else:
        return None
    
# -------------------------------------------------------- FILTRAGGIO CARTE --------------------------------------------------------------

#lista temporanea per la ricerca per scritte
temp_clist = []

#lista valori nei filtri
def wordsfiltri():
    words = []
    words.append(values["-TYPE FILTER-"]) #0
    words.append(values["-TYPESON FILTER-"]) #1
    words.append(values["-ATTR FILTER-"]) #2
    words.append(values["-RACE FILTER-"]) #3
    words.append(values["-LVL FILTER-"]) #4
    words.append(values["-ATK FILTER-"]) #5
    words.append(values["-DEF FILTER-"]) #6
    words.append(values["-SEARCHES-"]) #7
    words.append(values["-ARCH FILTER-"]) #8
    #print(words)
    return words
        

#cerca le carte con i filtri selezionati tra i valori degli elementi nella window1
def filter():
    filtered_card_list = []
    words = wordsfiltri()
    #inizia filtraggio per tipo di carta
    if values["-TYPE FILTER-"] != "":
        #lista carte temporanee
        temp_list = []
        for c in clist:
            c1 = c.strip(".jpg")
            #v = typedictionary.get(c1, "")
            #new SQL
            v = dec.DBdecode("id", c1, "type")
            if words[0] in v:
                temp_list.append(c)
        filtered_card_list = temp_list
    #filtraggio sottotipo di carta
    if values["-TYPESON FILTER-"] != "":
        if values["-TYPE FILTER-"] == "Monster":
            #lista carte temporanee
            temp_list = []
            for c in (filtered_card_list if filtered_card_list != [] else clist):
                c1 = c.strip(".jpg")
                #v = typedictionary.get(c1, "")
                #new SQL
                v = dec.DBdecode("id", c1, "type")
                if words[1] in v:
                    temp_list.append(c)
            filtered_card_list = temp_list
        else:
            #lista carte temporanee
            temp_list = []
            for c in (filtered_card_list if filtered_card_list != [] else clist):
                c1 = c.strip(".jpg")
                #v = racedictionary.get(c1, "")
                #new SQL
                v = dec.DBdecode("id", c1, "type")
                if words[1] in v:
                    temp_list.append(c)
            filtered_card_list = temp_list
    #filtraggio attributo mostro
    if values["-ATTR FILTER-"] != "":
        #lista carte temporanee
        temp_list = []
        for c in (filtered_card_list if filtered_card_list != [] else clist):
            c1 = c.strip(".jpg")
            #v = attrdictionary.get(c1, "")
            #new SQL
            v = dec.DBdecode("id", c1, "attribute")
            if words[2] in v:
                temp_list.append(c)
        filtered_card_list = temp_list
    #filtraggio tipo mostro (PROBLEMA GUERRIERO/GUERRIERO BESTIA)
    if values["-RACE FILTER-"] != "":
        #lista carte temporanee
        temp_list = []
        for c in (filtered_card_list if filtered_card_list != [] else clist):
            c1 = c.strip(".jpg")
            #v = racedictionary.get(c1, "")
            #new SQL
            v = dec.DBdecode("id", c1, "race")
            if words[3] in v and not (words[3] == "Warrior" and v == "Beast-Warrior") and not (words[3] == "Beast" and v == "Beast-Warrior") and not (words[3] == "Beast" and v == "Winged Beast"):
                temp_list.append(c)
        filtered_card_list = temp_list
    #filtraggio livello mostro
    if values["-LVL FILTER-"] != "":
        #lista carte temporanee
        temp_list = []
        for c in (filtered_card_list if filtered_card_list != [] else clist):
            c1 = c.strip(".jpg")
            #v = lvldictionary.get(c1, "")
            #new SQL
            type1 = dec.DBdecode("id", c1, "type")
            v = dec.DBdecode("id", c1, "level")
            w = checkint(words[4])
            if w == v and w != None and "Monster" in type1:
                temp_list.append(c)
        filtered_card_list = temp_list
    #filtraggio attacco mostro
    if values["-ATK FILTER-"] != "":
        #lista carte temporanee
        temp_list = []
        for c in (filtered_card_list if filtered_card_list != [] else clist):
            c1 = c.strip(".jpg")
            #v = atkdictionary.get(c1, "")
            #new SQL
            type1 = dec.DBdecode("id", c1, "type")
            v = dec.DBdecode("id", c1, "atk")
            w = checkint(words[5])
            if w == v and w != None and "Monster" in type1:
                temp_list.append(c)
        filtered_card_list = temp_list
    #filtraggio difesa mostro
    if values["-DEF FILTER-"] != "":
        #lista carte temporanee
        temp_list = []
        for c in (filtered_card_list if filtered_card_list != [] else clist):
            c1 = c.strip(".jpg")
            #v = defdictionary.get(c1, "")
            #new SQL
            type1 = dec.DBdecode("id", c1, "type")
            v = dec.DBdecode("id", c1, "def")
            w = checkint(words[6])
            if w == v and w != None and "Monster" in type1:
                temp_list.append(c)
        filtered_card_list = temp_list
    return filtered_card_list

#filtra le carte della pool secondo i parametri riempiti
def filtercards(event):
    global y
    if event == "-TYPE FILTER-" and values[event] == "":
        updateImages(clist)
        y = 1
        window1["V_Scrollbar"].update(value = 1, range = (1, len(temp_images)))
        window1.write_event_value("Refresh", (clist))
        window1["-TYPESON FILTER-"].update(value="", values=[])
        window1["-RACE FILTER-"].update(value="", values=[])
        window1["-ATTR FILTER-"].update(value="", values=[])
        return clist     
    elif event == "-TYPE FILTER-":
        #aggiorna altri tipi di ricerche
        item = values[event]
        title_list = types[item]
        window1["-TYPESON FILTER-"].update(value="", values=title_list)
        values["-TYPESON FILTER-"] = ''
        if item == "Monster":
            title_list = [i for i in races[item]]
            window1["-RACE FILTER-"].update(value="", values=title_list)
            title_list = [i for i in attributes[item]]
            window1["-ATTR FILTER-"].update(value="", values=title_list)
        else:
            window1["-RACE FILTER-"].update(value="", values=[])
            window1["-ATTR FILTER-"].update(value="", values=[])
    listc = filter()
    updateImages(listc)
    y = 1
    window1["V_Scrollbar"].update(value = 1, range = (1, len(temp_images)))
    window1.write_event_value("Refresh", (listc))
    return listc

'''#PROVA: resizing automatico
win_size = window1.size
current_image = None

def resizingFunc(x, y):
    (size_x, size_y) = window1["-IMAGE-"].get_size()
    if (x != 0 or y != 0) and (size_x > 0 or size_y > 0):
        new_size_x = size_x + ((size_x*x)/100)
        new_size_y = size_y + ((size_y*y)/100)
        print(str(new_size_x) + " " + str(new_size_y))
        #window1["-IMAGE-"].set_size((new_size_x, new_size_y))
        window1["-IMAGE-"].update(data=convert_to_bytes(current_image, (new_size_x, new_size_y)))'''
        
        
#controlla che il programma sia partito per la prima volta
start = True
#--------------------------------- Event Loop ---------------------------------
while True:
    window, event, values = sg.read_all_windows()
    
    # End program if user closes window
    if event == "Exit" or event == sg.WIN_CLOSED:
        if window != window1:
            window.hide()
        elif window == window1:
            break
    if start is True:
        temp_clist = clist
        start = not start
    #filtra per nome
    if event == "-SEARCHES-" + "_Enter" and values["-SEARCHES-"] != "":
        word = values["-SEARCHES-"]
        #lista carte temporanee
        filtered_card_list = []
        for c in temp_clist:
            c1 = c.strip(".jpg")
            v = dec.DBdecode("id", c1, "name")
            v1 = dec.DBdecode("id", c1, "desc")
            trovato = False
            if word.casefold() in v.casefold():
                filtered_card_list.append(c)
                trovato = True
            if word.casefold() in v1.casefold() and not trovato:
                filtered_card_list.append(c)
        updateImages(filtered_card_list)
        y = 1
        window1["V_Scrollbar"].update(value = 1, range = (1, len( temp_images)))
        window1.write_event_value("Refresh", (filtered_card_list))
    #resetta ricerca carte
    if event == "Reset":
        window1["-TYPE FILTER-"].update("")
        window1["-TYPESON FILTER-"].update("")
        window1["-ATTR FILTER-"].update("")
        window1["-RACE FILTER-"].update("")
        window1["-LVL FILTER-"].update("")
        window1["-ATK FILTER-"].update("")
        window1["-DEF FILTER-"].update("")
        window1["-SEARCHES-"].update("")
        window1["-ARCH-"].update("")
        window1["-ARCH FILTER-"].update(set_to_index = 0)
        temp_clist = clist
        updateImages(clist)
        y = 1
        window1["V_Scrollbar"].update(value = 1, range = (1, len(temp_images)))
        window1.write_event_value("Refresh", (clist))
    #filtraggio carte
    if event == "-TYPE FILTER-" or event == "-TYPESON FILTER-" or event == "-ATTR FILTER-" or event == "-RACE FILTER-":
        temp_clist = filtercards(event)
    if event == "-LVL FILTER-" + "_Enter" or event == "-ATK FILTER-" + "_Enter" or event == "-DEF FILTER-" + "_Enter":
        temp_clist = filtercards(event)
    if event == "-ARCH FILTER-":
        if values["-ARCH FILTER-"] != "":
            window1["-ARCH-"].update(archetype[values["-ARCH FILTER-"]])
            word = values["-ARCH FILTER-"]
            #lista carte temporanee
            filtered_card_list = []
            for c in temp_clist:
                c1 = c.strip(".jpg")
                v = dec.DBdecode("id", c1, "setcode")
                trovato = False
                if v != [] and word in v:
                    filtered_card_list.append(c)
                    trovato = True
                if not trovato:
                    v1 = dec.DBdecode("id", c1, "name")
                    v2 = dec.DBdecode("id", c1, "desc")
                    tdtk = word[0] == "True Draco|True King"
                    pyfu = word[0] == "Polymerization|Fusion"
                    if word in v1 or word in v2 or (tdtk and ("True Draco" in v1 or "True King" in v1) or (pyfu and("Polymerization" in v1 or "Fusion" in v1))):
                        filtered_card_list.append(c)
            updateImages(filtered_card_list)
            y = 1
            window1["V_Scrollbar"].update(value = 1, range = (1, len(temp_images)))
            window1.write_event_value("Refresh", (filtered_card_list))
    #aggiornamento pool
    if event == "Refresh" or event == "V_Scrollbar":
        manual = int(values[event]) if not isinstance(values[event], list) and not isinstance(values[event], tuple) else None
        if manual != None:
            y = manual
        if values[event] == []:
            for i in range(0, 16):
                image = window1["CARD" + str(i)]
                image.update(data=convert_to_bytes("pics/null.png", SIZE_CARD_POOL))
                image.metadata = ""
        else:
            for i in range(0, 16):
                image = window1["CARD" + str(i)]
                #print(temp_images[y-1][i])
                if temp_images != [] and i < len(temp_images[y-1]):
                    image.update(data=convert_to_bytes("pics/" + temp_images[y-1][i], SIZE_CARD_POOL))
                    image.metadata = temp_images[y-1][i]
                else:
                    image.update(data=convert_to_bytes("pics/null.png", SIZE_CARD_POOL))
                    image.metadata = ""
    #visualizza informazioni carta
    if event != vscroll and "CARD" in event:
        element = window[event]
        if window[event].metadata != "":
            try:
                #check banned cards
                b = open(os.path.join(parentDict, "structs/bans.json"), 'r')
                bans = b.readline()
                b.close()
                #show card informations
                filename = os.path.join("pics", element.metadata)
                window1["-IMAGE-"].update(data=convert_to_bytes(filename, CARD_IMAGE_SIZE))
                current_image = filename
                idc = element.metadata.rstrip(".jpg")
                qnt = cards[str(idc)]
                name = dec.DBdecode("id", idc, "name") + "\nQnt: " + str(qnt)
                window1["-NAME-"].update(name)
                typestxt = dec.DBdecode("id", idc, "type")
                attr = dec.DBdecode("id", idc, "attribute")
                race = dec.DBdecode("id", idc, "race")
                level = dec.DBdecode("id", idc, "level")
                atk = dec.DBdecode("id", idc, "atk")
                defe = dec.DBdecode("id", idc, "def")
                first = typestxt + ((" [" + attr + " " + race + "] ") if (attr != "" and race != "") else "")
                second = ("Level/Rank: " if (level != 0 and "Link" not in str(typestxt)) else ("Link Rating: " if (level != 0 and "Link" in str(typestxt)) else "")) + ((str(level) + " ") if level != 0 else "")
                third = (("\nATK: " + str(atk) + "  DEF: " + str(defe)) if ("Trap" not in typestxt and "Spell" not in typestxt) else "")
                info = first + second + third
                window1["-INFO-"].update(info)
                if (idc) in bans:
                    window1["-DESC-"].update("***BANNED***\n" + dec.DBdecode("id", idc, "desc"))
                else:
                    window1["-DESC-"].update(dec.DBdecode("id", idc, "desc"))
                window1["-COL_TEXT-"].update(visible=True)
            except Exception as E:
                print(E)
                pass        # something weird happened making the full filename
    '''#resizing automation
    if "CARD" not in event and event == "Resizing":
        print("Resizing")
        new_win_size = window1.size
        x = ((new_win_size[0]-win_size[0])*100)/win_size[0]
        y = ((new_win_size[1]-win_size[1])*100)/win_size[1]
        print(str(win_size) + " " + str(new_win_size) + " " + str(x) + " " + str(y))
        resizingFunc(x, y)
        win_size = new_win_size'''

        
#---------------------------------- Close & Exit ---------------------------------
f.close()
window1.close()



