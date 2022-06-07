import json
import os.path
import sys
import pandas as pd
import sqlite3 as sql
import pathlib

#per l'eseguibile, SOSTITUIRE application_path con pathlib.Path(__file__).parent.resolve() per testare
application_path = os.path.dirname(sys.executable)

parentDict = pathlib.Path(__file__).parent.resolve()

class DBdecoder:

    def __init__(self):
        #variabili per accesso al database locale
        self.conn = sql.connect("structs/cards.cdb")
        self.cur = self.conn.cursor()

    #traduce gli hexcode e ritorna gli archetipi della carta
    def decodeHexArch(self, value):
        hexed = hex(value)
        #print(hexed)
        no0x = hexed.lstrip("0x")
        f = open(os.path.join(parentDict, "structs/hexToArch.txt"), "r")
        contents = f.read()
        hexToArch = json.loads(contents)
        f.close()
        #nessun archetipo
        if value == 0:
            return []
        #normale archetipo o estesi
        elif hexed in hexToArch.keys():
            return [hexToArch[hexed]]
        #archetipi estesi che appaiono solo in carte con 2 archetipi
        elif len(no0x) < 5:
            match value:
                case 4166:
                    return ["Fusion Dragon"]
                case 4168:
                    return ["Chaos C"]
                case 4176:
                    return ["Starving Venom"]
                case 4211:
                    return ["CXyz"]
                case 4223:
                    return ["Utopia"]
                case 4427:
                    return ["Numeron Gate"]
                case 4472:
                    return ["Barian's"]
                case 8319:
                    return ["Utopic Future"]
                case 12411:
                    return ["Galaxy-Eyes Tachyon Dragon"]
                case 20552:
                    return ["Number C39"]
        #archetipi doppi
        elif len(no0x) < 9:
            first, second = no0x[:-4], no0x[-4:]
            iter = second
            for c in iter:
                if c == "0":
                    second = second.lstrip("0")
                else:
                    break
            #potrebbero apparire archetipi estesi in carte con + archetipi 
            if len(first) == 4 or len(second) == 4:
                intfirst = 0
                intsecond = 0
                if len(first) == 4:
                    intfirst = int(first, base=16)
                if len(second) == 4:
                    intsecond = int(second, base=16)
                return (self.decodeHexArch(intfirst) if (intfirst != 0) else [hexToArch["0x" + first]]) + (self.decodeHexArch(intsecond) if (intsecond != 0) else [hexToArch["0x" + second]])
            else:
                return [hexToArch["0x" + first], hexToArch["0x" + second]]
        #archetipi tripli
        else:
            first, third = no0x[:len(no0x)-8], no0x[-4:]
            second = no0x[len(first):len(first)+4]
            iter = second
            for c in iter:
                if c == "0":
                    second = second.lstrip("0")
                else:
                    break
            iter = third
            for c in iter:
                if c == "0":
                    third = third.lstrip("0")
                else:
                    break
            #potrebbero apparire archetipi estesi in carte con + archetipi
            if len(first) == 4 or len(second) == 4 or len(third) == 4:
                intfirst = 0
                intsecond = 0
                intthird = 0
                if len(first) == 4:
                    intfirst = int(first, base=16)
                if len(second) == 4:
                    intsecond = int(second, base=16)
                if len(third) == 4:
                    intthird = int(third, base=16)
                return (self.decodeHexArch(intfirst) if (intfirst != 0) else [hexToArch["0x" + first]]) + (self.decodeHexArch(intsecond) if (intsecond != 0) else [hexToArch["0x" + second]]) + (self.decodeHexArch(intthird) if (intthird != 0) else [hexToArch["0x" + third]])
            else:
                return [hexToArch["0x" + first], hexToArch["0x" + second], hexToArch["0x" + third]]


    #traduce decimali del database in valori concreti
    def DBdecode(self, key, c, filtering):
        table = None
        #print(c)
        if filtering == "name" or filtering == "desc":
            table = "texts"
        else:
            table = "datas"
        if key == "name" or key == "desc":
            #print(c)
            sql = ("SELECT " + filtering + " FROM texts WHERE " + key + " IS (?)")
            results = self.cur.execute(sql, (c,))
        else:
            results = self.cur.execute("SELECT " + filtering + " FROM " + table + " WHERE " + key + " IS " + c)
        df = pd.DataFrame(results)
        value = df.values[0][0]
        if filtering == "id":
            return value
        if filtering == "name" or filtering == "desc":
            return value
        if filtering == "type":
            match value:
                case 17:
                    return "Normal Monster"
                case 33:
                    return "Effect Monster"
                case 33554465:
                    return "Effect Monster"
                case 545:
                    return "Spirit Monster"
                case 33554977:
                    return "Spirit Monster"
                case 1057:
                    return "Union Effect Monster"
                case 2097185:
                    return "Flip Effect Monster"
                case 2081:
                    return "Gemini Monster"
                case 4194337:
                    return "Toon Monster"
                case 37748769:
                    return "Toon Monster"
                case 4113:
                    return "Normal Tuner Monster"
                case 4129:
                    return "Tuner Monster"
                case 33558561:
                    return "Tuner Monster"
                case 2101281:
                    return "Tuner Flip Monster"
                case 5153:
                    return "Union Tuner Monster"
                case 16777249:
                    return "Pendulum Effect Monster"
                case 50331681:
                    return "Pendulum Effect Monster"
                case 16777233:
                    return "Pendulum Normal Monster"
                case 18874401:
                    return "Pendulum Flip Effect Monster"
                case 16777761:
                    return "Pendulum Effect Spirit Monster"
                case 16781329:
                    return "Pendulum Normal Tuner Monster"
                case 16781345:
                    return "Pendulum Tuner Effect Monster"
                case 16777313:
                    return "Pendulum Effect Fusion Monster"
                case 16785441:
                    return "Pendulum Effect Synchro Monster"
                case 25165857:
                    return "Pendulum Effect XYZ Monster"
                case 161:
                    return "Ritual Effect Monster"
                case 673:
                    return "Ritual Spirit Monster"
                case 65:
                    return "Fusion Monster"
                case 97:
                    return "Fusion Monster"
                case 4161:
                    return "Fusion Tuner Monster"
                case 8225:
                    return "Synchro Monster"
                case 8193:
                    return "Synchro Monster"
                case 12321:
                    return "Synchro Tuner Monster"
                case 8388609:
                    return "XYZ Monster"
                case 8388641:
                    return "XYZ Monster"
                case 67108865:
                    return "Link Monster"
                case 67108897:
                    return "Link Monster"
                case 2:
                    return "Normal Spell Card"
                case 130:
                    return "Ritual Spell Card"
                case 65538:
                    return "Quick-Play Spell Card"
                case 131074:
                    return "Continuos Spell Card"
                case 262146:
                    return "Equip Spell Card"
                case 524290:
                    return "Field Spell Card"
                case 4:
                    return "Normal Trap Card"
                case 131076:
                    return "Continuos Trap Card"
                case 1048580:
                    return "Counter Trap Card"
        if filtering == "attribute":
            match value:
                case 0:
                    return ""
                case 1:
                    return "EARTH"
                case 2:
                    return "WATER"
                case 4:
                    return "FIRE"
                case 8:
                    return "WIND"
                case 16:
                    return "LIGHT"
                case 32:
                    return "DARK"
                case 64:
                    return "DIVINE"
        if filtering == "race":
            match value:
                case 0:
                    return ""
                case 1:
                    return "Warrior"
                case 2:
                    return "Spellcaster"
                case 4:
                    return "Fairy"
                case 8:
                    return "Fiend"
                case 16:
                    return "Zombie"
                case 32:
                    return "Machine"
                case 64:
                    return "Aqua"
                case 128:
                    return "Pyro"
                case 256:
                    return "Rock"
                case 512:
                    return "Winged Beast"
                case 1024:
                    return "Plant"
                case 2048:
                    return "Insect"
                case 4096:
                    return "Thunder"
                case 8192:
                    return "Dragon"
                case 16384:
                    return "Beast"
                case 32768:
                    return "Beast-Warrior"
                case 65536:
                    return "Dinosaur"
                case 131072:
                    return "Fish"
                case 262144:
                    return "Sea Serpent"
                case 524288:
                    return "Reptile"
                case 1048576:
                    return "Psychic"
                case 2097152:
                    return "Divine-Beast"
                case 4194304:
                    return "Creator God"
                case 8388608:
                    return "Wyrm"
                case 16777216:
                    return "Cyberse"
        if filtering == "level":
            if value == 0:
                return 0
            if value < 16842752:
                return value
            if value < 33685504:
                return value-16842752
            if value < 50528256:
                return value-33685504
            if value < 67371008:
                return value-50528256
            if value < 84213760:
                return value-67371008
            if value < 101056512:
                return value-84213760
            if value < 117899264:
                return value-101056512
            if value < 134742016:
                return value-117899264
            if value < 151584768:
                return value-134742016
            if value < 168427520:
                return value-151584768
            if value < 185270272:
                return value-168427520
            if value < 202113024:
                return value-185270272
            if value < 218955776:
                return value-202113024
            if value > 218955776:
                return value-218955776
        if filtering == "atk" or filtering == "def":
            if value == -2:
                return "?"
            else:
                return value
        if filtering == "setcode":
            return self.decodeHexArch(value)
