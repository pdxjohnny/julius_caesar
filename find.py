#!/usr/bin/env python3
import os
import sys

import roman

fileName = sys.argv[1]
findName = sys.argv[2].upper()

inAct = False
inScene = False
inCharacter = False
firstBlock = False

currCharacter = ''

line = 0

PLAY = {}
PLAY_LINES = {}
DEBUG = os.getenv('DEBUG', False)

START_ACT = '  ACT'
START_SCENE = '  SCENE'
START_CHARACTER = '   '

def isSection(l, section):
    # print(l, section, l[:len(section)])
    if len(l) > len(section) and l[:len(section)] == section:
        return True
    return False

def createIfEmpty(obj, key):
    if not key in obj:
        obj[key] = {}

def flushCharacter():
    global PLAY
    global inAct
    global inScene
    global inCharacter
    global currCharacter
    if DEBUG:
        print(inCharacter)
        print(currCharacter)
    if inCharacter:
        PLAY[inAct][inScene].append((inCharacter, currCharacter))

def onLine(l):
    global PLAY
    global PLAY_LINES
    global line
    global inAct
    global inScene
    global inCharacter
    global currCharacter
    global firstBlock
    l = l.rstrip()
    if isSection(l, START_ACT):
        inAct = roman.fromRoman(l.split()[1])
        if DEBUG:
            print('Act', inAct)
        createIfEmpty(PLAY, inAct)
        inScene = False
        inCharacter = False
        return
    if isSection(l, START_SCENE):
        inScene = roman.fromRoman(l.split()[1][:-1])
        if DEBUG:
            print('Scene', inScene)
        createIfEmpty(PLAY[inAct], inScene)
        PLAY[inAct][inScene] = []
        inCharacter = False
        line = 0
        return
    if isSection(l, START_CHARACTER) and \
            l[len(START_CHARACTER) + 1] != ' ' and \
            len([word for word in l.split() if word[0].isupper()]) == len(l.split()):
        flushCharacter()
        inCharacter = l.strip().upper()
        currCharacter = ''
        firstBlock = True
        if DEBUG:
            print('Character', inCharacter)
        return
    if inAct and inScene and inCharacter and firstBlock:
        if len(l.strip()) == 0 and firstBlock:
            if len(currCharacter) > 0:
                firstBlock = False
            return
        line += 1
        PLAY_LINES[''.join([str(inAct), str(inScene), inCharacter, l.strip().upper()])] = line
        currCharacter += l + '\n'

with open(fileName, 'rb') as f:
    for l in f:
        l = l.decode('utf-8')
        onLine(l)
flushCharacter()

for act in PLAY:
    for scene in PLAY[act]:
        for character, lines in PLAY[act][scene]:
            if findName == character or findName in lines.strip().upper():
                print()
                print('Act', act, 'Scene', scene, character)
                for l in lines.split('\n')[:-1]:
                    ln = PLAY_LINES[''.join([str(act), str(scene), character,
                        l.strip().upper()])]
                    # print('%-70s%d' % (l.rstrip(), ln))
                    print('%-4d%s' % (ln, l.rstrip()))
