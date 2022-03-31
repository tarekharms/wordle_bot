#!/usr/bin/python

import string
import math
import time

def dd(var):
    print(str(var))
    exit()


def getEntropy(word, possibleWords):
    rfv = ['f', 'v', 'r']

    entropy = 0

    for a in rfv:
        woerterA = getMatchesWordMuster(word, [a], possibleWords)
        for b in rfv:
            woerterB = getMatchesWordMuster(word, [a, b], woerterA)
            for c in rfv:
                woerterC = getMatchesWordMuster(word, [a, b, c], woerterB)
                for d in rfv:
                    woerterD = getMatchesWordMuster(word, [a, b, c, d], woerterC)
                    for e in rfv:
                        muster = a + b + c + d + e
                        matches = getMatchesWordMuster(word, muster, woerterD)
                        # entropy += len(matches) / len(possibleWords) * len(matches)
                        p = len(matches) / len(possibleWords)
                        if p != 0:
                            entropy += p * math.log(1/p, 2)                    

    return entropy
    




def getMatchesWordMuster(word, muster, possibleWords):    
    gerateneswort = word

    possibleWordmatch = [
        list(string.ascii_lowercase), 
        list(string.ascii_lowercase),
        list(string.ascii_lowercase),
        list(string.ascii_lowercase),
        list(string.ascii_lowercase)
    ]

    # umlaute = ['ö', 'ä', 'ü']

    # for umlaut in umlaute:
    #     for wordMatch in possibleWordmatch:
    #         wordMatch.append(umlaut)

    richtigeBuchstaben = [False, False, False, False, False]
    vorhandeneBuchstaben = []

    for i in range(0, len(muster)):

        if(muster[i].lower() == 'r'):
            possibleWordmatch[i] = [gerateneswort[i]]
            vorhandeneBuchstaben.append(gerateneswort[i])

            # if(not richtigeBuchstaben[i] and gerateneswort[i] in vorhandeneBuchstaben):
            #     vorhandeneBuchstaben.remove(gerateneswort[i])

            richtigeBuchstaben[i] = True

        elif(muster[i].lower() == 'f'):
            if(gerateneswort[i] in vorhandeneBuchstaben and gerateneswort[i] in possibleWordmatch[i]):
                possibleWordmatch[i].remove(gerateneswort[i])
            else:
                for match in possibleWordmatch:
                    if(gerateneswort[i] in match):
                        match.remove(gerateneswort[i])

        elif(muster[i].lower() == 'v'):
            if(gerateneswort[i] in possibleWordmatch[i]):
                possibleWordmatch[i].remove(gerateneswort[i])

            vorhandeneBuchstaben.append(gerateneswort[i])

    return getPossibleWords(possibleWords, possibleWordmatch, vorhandeneBuchstaben, [])


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

            copyVorhandeneBuchstaben = vorhandeneBuchstaben.copy()

            for buchstabe in wort:
                if(buchstabe in copyVorhandeneBuchstaben):
                    copyVorhandeneBuchstaben.remove(buchstabe)
                     

            if(len(copyVorhandeneBuchstaben) == 0):
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

def getWortBesteEntropy(possibleWords):
    bestesWord = possibleWords[0]
    besteEntropy = getEntropy(bestesWord, possibleWords)

    for word in possibleWords:
        entropy = getEntropy(word, possibleWords)

        if(entropy > besteEntropy):
            besteEntropy = entropy
            bestesWord = word

        print(word + ": " + str(entropy) + ", Bestes Wort: " + bestesWord + "(" + str(besteEntropy) + ")")

    
    return bestesWord
    


# Darfenthaltensein und muss in einem enthalten sein.
possibleWordmatch = [
    list(string.ascii_lowercase), 
    list(string.ascii_lowercase),
    list(string.ascii_lowercase),
    list(string.ascii_lowercase),
    list(string.ascii_lowercase)
]

# umlaute = ['ö', 'ä', 'ü']

# for umlaut in umlaute:
#     for wordMatch in possibleWordmatch:
#         wordMatch.append(umlaut)

richtigeBuchstaben = [False, False, False, False, False]
vorhandeneBuchstaben = []
woerterBlacklist = ['altre', 'lasre', 'knaur'] # Deutsch
# woerterBlacklist = ['aires', 'aries'] # Englisch


firstRound = True

woerterbuch = open("wordleWords_de", 'r')
possibleWords = getPossibleWords(woerterbuch, possibleWordmatch, vorhandeneBuchstaben, woerterBlacklist)
woerterbuch.close()

# getWortBesteEntropy(possibleWords)
# exit()

while(True):    

    if(firstRound):
        # zuRatendesWort = "rates" # ohne umlaute 6.12 Bit
        zuRatendesWort = "rates" # mit umlaute 6.03 Bit
        # zuRatendesWort = "tares" # Englisch
        firstRound = False
    else:
        zuRatendesWort = getWortBesteEntropy(possibleWords)

    print("Höchste wahrscheinlichkeit: " + zuRatendesWort)
    muster = input("Ergebnis [R=Richtig, F=Falsch, V=Vorhanden, G=Wort Nicht vorhanden, A=Anderes Wort]: ")

    if(muster[0].lower() == 'a'):
        zuRatendesWort = input("Wort: ")
        muster = input("Ergebnis [R=Richtig, F=Falsch, V=Vorhanden, G=Wort Nicht vorhanden, A=Anderes Wort]: ")



    if(muster[0].lower() == 'g'):
        woerterBlacklist.append(zuRatendesWort)
        continue

    possibleWords = getMatchesWordMuster(zuRatendesWort, muster, possibleWords)


    
exit()
        
