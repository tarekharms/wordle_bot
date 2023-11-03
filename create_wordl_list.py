#!/usr/bin/python

import sys
import os

print(sys.argv)

if(sys.argv[1] == 'en'):
    os.system('aspell -l en dump master | aspell -l en expand > words')
elif(sys.argv[1] == 'de'):
    os.system('aspell -l de dump master | aspell -l de expand > words')
elif(sys.argv[1] == 'nl'):
    os.system('aspell -l nl dump master | aspell -l nl expand > words')
else:
    print("Keine Sprache angegeben")
    exit()
    

wordFile = open("words", 'r')

woerterbuch = []

for line in wordFile:
    line = line.replace("\n", '')
    words = line.split(' ')

    for word in words:
        word = word.lower()

        if(len(sys.argv) >= 3 and sys.argv[2] == '--ohne-umlaute'):
            word = word.replace('ä', 'ae')
            word = word.replace('ö', 'oe')
            word = word.replace('ü', 'ue')
            word = word.replace('ß', 'ss')

        if(len(word) == 5 and '\'' not in word):
            woerterbuch.append(word)

wordFile.close()
os.system('rm words')

woerterbuch = list(dict.fromkeys(woerterbuch))
woerterbuch.sort()

for wort in woerterbuch:
    print(wort)
    
wordleFile = open("wordleWords_" + sys.argv[1], 'w')

for wort in woerterbuch:
    wordleFile.write(wort + '\n')

wordleFile.close()
