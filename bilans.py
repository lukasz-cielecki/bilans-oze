#!/usr/bin/env python

__author__ = "Łukasz Cielecki"
__copyright__ = "Copyright 2022, Łukasz Cielecki"
__credits__ = ["Łukasz Cielecki"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Łukasz Cielecki"
__email__ = "lukasz@cielecki.pl"
__status__ = "Production"

# Niniejszy program jest wolnym oprogramowaniem; możesz go
# rozprowadzać dalej i/lub modyfikować na warunkach Powszechnej
# Licencji Publicznej GNU, wydanej przez Fundację Wolnego
# Oprogramowania - według wersji 3-ciej tej Licencji lub którejś
# z późniejszych wersji.
# Niniejszy program rozpowszechniany jest z nadzieją, iż będzie on
# użyteczny - jednak BEZ JAKIEJKOLWIEK GWARANCJI, nawet domyślnej
# gwarancji PRZYDATNOŚCI HANDLOWEJ albo PRZYDATNOŚCI DO OKREŚLONYCH
# ZASTOSOWAŃ. W celu uzyskania bliższych informacji - Powszechna
# Licencja Publiczna GNU.

from enum import Enum, auto
import csv
from datetime import datetime
import locale

import argparse
from glob import glob

print('Bilans OZE wersja {}, {}\r\n\r\nBilans OZE wydawany jest ABSOLUTNIE BEZ ŻADNEJ GWARANCJI\r\nW celu uzyskania bliższych informacji - Powszechna Licencja Publiczna GNU'.format(__version__, __copyright__))
print('―' * 40)

# Definiujemy rodzaj rekordu z raportu
class Kierunek(Enum):
    EXPORT = auto()
    IMPORT = auto()

locale.setlocale(locale.LC_ALL, 'pl_pl')

def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "nieprawidłowy format daty: {0!r}".format(s)
        raise argparse.ArgumentTypeError(msg)

parser = argparse.ArgumentParser()
parser.add_argument('plik', nargs='+', help='Plik(i) CSV do analizy')
parser.add_argument("-m", "--mnoznik", help="Mnożnik energii magazynowanej", default="0,8")
parser.add_argument("-p", "--podzial", help="Uwzględnij rozpoczęcie bilansowania godzinowego", action='store_true')
parser.add_argument("-d", "--data", help="Data wprowadzenie bilansowania godzinowego (RRRR-MM-DD), domyślnie 2022-04-01", type=valid_date, default='2022-04-01')
args = parser.parse_args()
file_names = []
for arg in args.plik:
    file_names += glob(arg)

mnoznik = locale.atof(args.mnoznik)

Kierunek_strings = {'energia czynna oddana': Kierunek.EXPORT, 'energia czynna pobrana': Kierunek.IMPORT}

Tablica_energii = {}
Timestamps = []

# Odczytujemy raporty z eLicznika
for plik in file_names:
    raport_godzinowy = csv.DictReader(open(plik, newline=''), delimiter=';')
    print('Przetwarzam plik {}'.format(plik))

    for rekord in raport_godzinowy:
        date_time_obj = datetime.strptime(rekord['Data i godzina'], '%Y-%m-%d %H:%M')
        kierunek_obj = Kierunek_strings[rekord['Rodzaj energii']]
        wartosc = locale.atof(rekord['Wartosc[kWh/kvar]'])

        Tablica_energii[date_time_obj, kierunek_obj] = wartosc
        if date_time_obj not in Timestamps:
            Timestamps.append(date_time_obj)

        #print('{} / {}: {}'.format(date_time_obj, kierunek_obj, wartosc))

# Liczniki energii
unb_exported = 0
unb_imported = 0
bal_exported = 0
bal_imported = 0

for element in Timestamps:
    if (element < args.data) or (not args.podzial):
        unb_imported += Tablica_energii[element, Kierunek.IMPORT]
        unb_exported += Tablica_energii[element, Kierunek.EXPORT]

    if (element >= args.data) or (not args.podzial):
        bilans = Tablica_energii[element, Kierunek.IMPORT] - Tablica_energii[element, Kierunek.EXPORT]
        #print('Bilans za {}: {}'.format(element, bilans))
        if bilans > 0:
            bal_imported += bilans
        else:
            bal_exported -= bilans

print('―' * 40)
print('Zakres pomiaru: {} -> {}'.format(min(Timestamps).strftime('%c'), max(Timestamps).strftime('%c')))
print('Mnożnik dla energii zmagazynowanej: {:n}'.format(mnoznik))
if args.podzial:
    print('Uwzględnione wprowadzenie bilansowania godzinowego od {} (włącznie)'.format(args.data.strftime('%x')))
    sum_imported = unb_imported + bal_imported
    sum_exported = unb_exported + bal_exported
    print('―' * 40)
    print('Import: {:n} kWh\r\nEksport: {:n} kWh'.format(sum_imported, sum_exported))
    print('Magazyn / deficyt: {:n} kWh'.format(sum_exported * mnoznik - sum_imported))
else:
    print('―' * 40)
    print('Import algebraicznie: {:n} kWh\r\nEksport algebraicznie: {:n} kWh'.format(unb_imported, unb_exported))
    print('Magazyn / deficyt algebraicznie: {:n} kWh'.format(unb_exported * mnoznik - unb_imported))

    print('―' * 40)
    print('Import zbilansowany: {:n} kWh\r\nEksport zbilansowany: {:n} kWh'.format(bal_imported, bal_exported))
    print('Magazyn / deficyt zbilansowany: {:n} kWh'.format(bal_exported * mnoznik - bal_imported))
