#!/usr/bin/env python3

import argparse
import asyncio
import contextlib
import json
import random
import unicodedata

with open('ord.json') as f:
    all_tests = json.load(f)

def langs():
    for lang in all_tests:
        yield lang
        # yield lang['from'], lang['to'], lang['tests']

# print(all_tests)


def test_menu(lang, test):
    f = lang['from']
    t = lang['to']

    word_list = parse_test(f, t, test)

    choices = [
        ('a', '{from} till {to}'.format(**lang), lambda: a_to_b(word_list)),
        ('b', '{to} till {from}'.format(**lang), lambda: b_to_a(word_list)),
        ('v', 'Visa', lambda: show_words(lang, word_list)),
    ]
    run_menu(choices)

def parse_test(f, t, test):
    # print(f, t, test)
    pass

    def parse_line(line):
        return [part.strip() for part in line.split(sep)]

    sep = test['separator']
    order = parse_line(test['order'])

    swap = order != [f, t]

    result = []

    for line in test['words']:
        item = parse_line(line)
        if swap:
            result.append([a for a in reversed(item)])
        else:
            result.append(item)

    return result

def demangle(word):
    # l = ['NFC', 'NFKC', 'NFD', 'NFKD']

    # for p in l:
    #     print(p, unicodedata.normalize(p, word).encode('ascii', 'ignore'))
    return unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').upper()

def do_test(word_list):
    random.shuffle(word_list)

    correct = 0
    wrong = 0

    for item in word_list:
        for _ in range(3):
            print('Översätt {}'.format(item[1]))
            if item[0][0] == '¿':
                extra = '¿'
                correct_word = item[0][1:]
            else:
                extra = ''
                correct_word = item[0]

            word = input('> {}'.format(extra))

            if demangle(word) == demangle(correct_word):
            # if word.upper() == correct_word.upper():
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

def a_to_b(word_list):
    do_test([(b, a) for a, b in word_list])

def b_to_a(word_list):
    do_test(word_list)

def show_words(lang, word_list):
    max_a_len = max(len(word) for word, _ in word_list)

    line = '{from:{cnt}}   {to}'.format(cnt=max_a_len, **lang)
    print(line)
    print('=' * len(line))

    for a, b in word_list:
        print('{0:{cnt}} - {1}'.format(a, b, cnt=max_a_len))

    _ = input('Retur för att fortsätta.')
    print('\033[H\033[J')

def lang_menu(lang):
    # print(tests)
    choices = [
        (
            str(no),
            '{name}'.format(**test),
            lambda test=test: test_menu(lang, test),
        ) for no, test in enumerate(lang['tests'], 1)
    ]
    run_menu(choices)

def top_menu():
    choices = [
        (
            str(no),
            '{from} till {to}'.format(**lang),
            lambda lang=lang: lang_menu(lang)
         ) for no, lang in enumerate(langs(), 1)
    ]

    # print(choices)

    run_menu(choices)

class MenuQuit(Exception):
    pass

def menu_quit():
    raise MenuQuit

def run_menu(choices):
    choices.append(('q', 'Avsluta', menu_quit))
    # print(choices)

    while True:
        for num, choice, _ in choices:
            print(num, choice.format(**globals()))

        fun = lambda: None # Do nothing

        with contextlib.suppress(Exception):
            selection = input('Välj: ')
            for choice, _, fun_ in choices:
                if selection == choice:
                    # print(selection)
                    fun = fun_

        # print(fun)

        try:
            fun()
        except MenuQuit:
            break

top_menu()
print('Hej då')
