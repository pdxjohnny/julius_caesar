#!/usr/bin/env python3
import sys

fileName = sys.argv[1]
findName = sys.argv[2].upper()

inAct = False
inScene = False
inCharacter = False
firstBlock = False

PLAY = {}

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

def onLine(l):
    global PLAY
    global inAct
    global inScene
    global inCharacter
    global firstBlock
    l = l.rstrip()
    if isSection(l, START_ACT):
        inAct = l.split()[1]
        # print('Act', inAct)
        createIfEmpty(PLAY, inAct)
        inScene = False
        inCharacter = False
        return
    if isSection(l, START_SCENE):
        inScene = l.split()[1][:-1]
        # print('Scene', inScene)
        createIfEmpty(PLAY[inAct], inScene)
        createIfEmpty(PLAY[inAct], inScene + '_line')
        PLAY[inAct][inScene + '_line'] = []
        inCharacter = False
        return
    if isSection(l, START_CHARACTER) and \
            l[len(START_CHARACTER) + 1] != ' ' and \
            len([word for word in l.split() if word[0].isupper()]) == len(l.split()):
        inCharacter = l.strip().upper()
        firstBlock = False
        # print('Character', inCharacter)
        createIfEmpty(PLAY[inAct][inScene], inCharacter)
        PLAY[inAct][inScene][inCharacter] = ''
        return
    if inAct and inScene and inCharacter:
        if len(l.strip()) == 0:
            if not firstBlock:
                firstBlock = True
            else:
                print()
                print(inCharacter)
                print(PLAY[inAct][inScene][inCharacter][:-1], len(PLAY[inAct][inScene + '_line']))
                inCharacter = False
                firstBlock = False
            return
        # print(inAct, inScene, inCharacter)
        PLAY[inAct][inScene][inCharacter] += l + '\n'
        PLAY[inAct][inScene + '_line'].append(l.strip().upper())
        if findName in l.strip().upper():
            return
            print()
            print('Act', inAct, 'Scene', inScene, inCharacter, 'Line:', len(PLAY[inAct][inScene + '_line']))
            print('\t', l.strip())

with open(fileName, 'rb') as f:
    for l in f:
        l = l.decode('utf-8')
        onLine(l)
if inCharacter:
    print()
    print(inCharacter)
    print(PLAY[inAct][inScene][inCharacter][:-1], len(PLAY[inAct][inScene + '_line']))
