#!/usr/bin/env python3
import sys
import time
import buildhat

MORSE = {
  'A':'.-',
  'B':'-...',
  'C':'-.-.',
  'D':'-..',
  'E':'.',
  'F':'..-.',
  'G':'--.',
  'H':'....',
  'I':'..',
  'J':'.---',
  'K':'-.-',
  'L':'.-..',
  'M':'--',
  'N':'-.',
  'O':'---',
  'P':'.--.',
  'Q':'--.-',
  'R':'.-.',
  'S':'...',
  'T':'-',
  'U':'..-',
  'V':'...-',
  'W':'.--',
  'X':'-..-',
  'Y':'-.--',
  'Z':'--..',
  '1':'.----',
  '2':'..---',
  '3':'...--',
  '4':'....-',
  '5':'.....',
  '6':'-....',
  '7':'--...',
  '8':'---..',
  '9':'----.',
  '0':'-----',
  ',':'--..--',
  '.':'.-.-.-',
  '?':'..--..',
  '/':'-..-.',
  '-':'-....-',
  '(':'-.--.',
  ')':'-.--.-',
  ' ':' ',
}

SLEEP = {
  ' ': 0.5,
  '.': 0.2,
  '-': 0.4,
  'token': 0.1,
  'letter': 0.4,
}

light = buildhat.Light('A')

motor = buildhat.PassiveMotor('B')
motor.start(20)

for line in sys.stdin:
    letters = [MORSE[c] for c in line.strip().upper() if c in MORSE]
    for letter in letters:
        for token in letter:
            light.off()
            time.sleep(SLEEP['token'])
            light.on()
            time.sleep(SLEEP[token])
        time.sleep(SLEEP['letter'])
