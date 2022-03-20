#!/usr/bin/python

import string

def getPossibleWords(woerterbuch, possibleWordmatch, vorhandeneBuchstaben, woerterBlacklist):
    words = []

    for wort in woerterbuch:
        wort = wort.replace('\n', '')
        
        if(wort in woerterBlacklist):
            continue

        if(
            wort[0] in possibleWordmatch[0] and
            wort[1] in possibleWordmatch[1] and
            wort[2] in possibleWordmatch[2] and
            wort[3] in possibleWordmatch[3] and
            wort[4] in possibleWordmatch[4] 
        ):
            buchstabenVorhanden = True

            for buchstabe in vorhandeneBuchstaben:
                if(buchstabe not in wort):
                    buchstabenVorhanden = False

            if(buchstabenVorhanden):
                words.append(wort)

    return words

def getWordThatHisMostIfAllFalse(possibleWords, richtigeBuchstaben):
    killerWord = possibleWords[0]
    killerWordKillCount = 0

    for possibleKiller in possibleWords:
        killCount = getKillCountOfWord(possibleWords, possibleKiller, richtigeBuchstaben)

        if(killCount > killerWordKillCount):
            killerWord = possibleKiller
            killerWordKillCount = killCount

    return killerWord



def getKillCountOfWord(possibleWords, killerWord, richtigeBuchstaben):
    killcount = 0

    for word in possibleWords:
        kills = False

        for i in range(0, 5):
            if(killerWord[i] in word and not richtigeBuchstaben[i]):
                killcount += 1
                kills = True
                break

        if kills: continue

    return killcount

def hatGewonnen(richtigeBuchstaben):
    gewonnen = True

    for richtig in richtigeBuchstaben:
        if(not richtig):
            gewonnen = False

    return gewonnen


alphabet = list(string.ascii_lowercase)

# Darfenthaltensein und muss in einem enthalten sein.
possibleWordmatch = [
    list(string.ascii_lowercase), 
    list(string.ascii_lowercase),
    list(string.ascii_lowercase),
    list(string.ascii_lowercase),
    list(string.ascii_lowercase)
]

richtigeBuchstaben = [False, False, False, False, False]
vorhandeneBuchstaben = []
woerterBlacklist = []

firstRound = True

while(True):    
    woerterbuch = open("wordleWords_de", 'r')
    possibleWords = getPossibleWords(woerterbuch, possibleWordmatch, vorhandeneBuchstaben, woerterBlacklist)
    woerterbuch.close()

    print(possibleWords)
    print(len(possibleWords))

    if(firstRound):
        zuRatendesWort = "saite"
        firstRound = False
    else:
        zuRatendesWort = getWordThatHisMostIfAllFalse(possibleWords, richtigeBuchstaben)

    print("Höchste wahrscheinlichkeit: " + zuRatendesWort)
    muster = input("Ergebnis [R=Richtig, F=Falsch, V=Vorhanden, G=Wort Nicht vorhanden]: ")

    if(muster[0].lower() == 'g'):
        woerterBlacklist.append(zuRatendesWort)
        continue

    gerateneswort = zuRatendesWort

    for i in range(0, 5):

        if(muster[i].lower() == 'r'):
            possibleWordmatch[i] = [gerateneswort[i]]

            if(not richtigeBuchstaben[i] and gerateneswort[i] in vorhandeneBuchstaben):
                vorhandeneBuchstaben.remove(gerateneswort[i])

            richtigeBuchstaben[i] = True

        elif(muster[i].lower() == 'f'):
            if(gerateneswort[i] in vorhandeneBuchstaben and gerateneswort[i] in possibleWordmatch[i]):
                possibleWordmatch[i].remove(gerateneswort[i])
            else:
                for match in possibleWordmatch:
                    if(gerateneswort[i] in match):
                        match.remove(gerateneswort[i])

        elif(muster[i].lower() == 'v'):
            possibleWordmatch[i].remove(gerateneswort[i])

            if(gerateneswort[i] not in vorhandeneBuchstaben):
                vorhandeneBuchstaben.append(gerateneswort[i])


    if(hatGewonnen(richtigeBuchstaben)):
        print("Gewonnen")
        break


    
exit()
        
