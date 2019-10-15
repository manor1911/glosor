#!/usr/bin/env python3

import argparse
import asyncio
import contextlib
import random

def do_test(test):
    random.shuffle(test)

    correct = 0
    wrong = 0

    for item in test:
        for _ in range(3):
            print('Översätt {}'.format(item[1]))
            if item[0][0] == '¿':
                extra = '¿'
                correct_word = item[0][1:]
            else:
                extra = ''
                correct_word = item[0]

            word = input('> {}'.format(extra))

            if word.upper() == correct_word.upper():
                print('Rätt svar. Bra jobbat.')
                correct += 1
                break
            else:
                print("Fel svar. Försök igen.")
                wrong += 1
        else:
            print('Rätt svar ska vara: {}'.format(item[0]))

    print('Antal rätt: {:2}'.format(correct))
    print('Antal fel:  {:2}'.format(wrong))

def a_to_b():
    do_test([(b, a) for a, b in words])

def b_to_a():
    do_test(words[:])

keep_running = True

def show_words():
    print()

    max_a_len = max(len(word) for word, _ in words)

    line = '{a_lang:{cnt}}   {b_lang}'.format(cnt=max_a_len, **globals())
    print(line)
    print('=' * len(line))

    for a, b in words:
        print('{0:{cnt}} - {1}'.format(a, b, cnt=max_a_len))

def menu_quit():
    global keep_running
    keep_running = False

menu_choices = [
    ('Visa', show_words),
    ('{a_lang} till {b_lang}', a_to_b),
    ('{b_lang} till {a_lang}', b_to_a),
    ('Avsluta', menu_quit)
]

def menu():
    for num, choice in enumerate(menu_choices, 1):
        print(str(num), choice[0].format(**globals()))

    fun = lambda: None # Do nothing

    with contextlib.suppress(Exception):
        index = int(input('Välj: ')) - 1
        fun = menu_choices[index][1]

    fun()

words = []

with open('ord.txt') as f:

    for a, b in (line.split('=') for line in f):
        words.append((a.strip(), b.strip()))

a_lang = words[0][0]
b_lang = words[0][1]

del words[0]

while keep_running:
    menu()
