# bilans-oze
Analiza raportów godzinowych z eLicznika pod kątem bilansowania godzinowego

## Licencja
Niniejszy program jest wolnym oprogramowaniem; możesz go
rozprowadzać dalej i/lub modyfikować na warunkach Powszechnej
Licencji Publicznej GNU, wydanej przez Fundację Wolnego
Oprogramowania - według wersji 3-ciej tej Licencji lub którejś
z późniejszych wersji.
Niniejszy program rozpowszechniany jest z nadzieją, iż będzie on
użyteczny - jednak **BEZ JAKIEJKOLWIEK GWARANCJI**, nawet domyślnej
gwarancji PRZYDATNOŚCI HANDLOWEJ albo PRZYDATNOŚCI DO OKREŚLONYCH
ZASTOSOWAŃ. W celu uzyskania bliższych informacji - Powszechna
Licencja Publiczna GNU.

## Geneza skryptu
Motywacją powstania skryptu była wprowadzona od 1.04.2022 zmiana
sposobu bilansowania poboru i oddania do sieci energii przez prosumentów.
Zgodnie z ustawą od tego dnia bilansowanie poboru i oddania następuje
w przedziałach godzinowych po zsumowaniu wszystkich faz. Podejście takie jest
korzystne dla prosumentów w porównaniu z bilansowaniem algebraicznym gdyż
w znaczący sposób poszerza autokonsumpcję.

Celem poniższego skryptu jest analiza plików raportów godzinowych z aplikacji
eLicznik (Tauron Dystrybucja) zapisanych w formacie CSV i wyliczanie na ich 
podstawie importu, eksportu oraz wartości energii zmagazynowanej 
(lub jej deficytu) w oparciu o godzinową metodę bilansowania.

## Wymagania
Skrypt wymaga interpretera Pythona w wersji 3.
Nie są wymagane żadne niestandardowe pakiety.

## Pozyskanie danych
Dane źródłowe dla skryptu należy pozyskać ze strony eLicznika:
https://elicznik.tauron-dystrybucja.pl/raporty

1. Wybieramy interesujący nas punkt PPE,
2. Określamy interesujący nas zakres danych. Strona umożliwia jedynie 
wybranie zakresu miesięcznego. Jeśli interesuje nas szerszy zakres możemy
wygenerować więcej raportów z róznych zakresów. Skrypt potraktuje je sumarycznie,
3. W sekcji "Rodzaj danych" wybieramy: "godzinowe",
4. W sekcji "Rodzaj energii" zaznaczamy zarówno energię pobraną jak i oddaną.

Po wygenerowaniu wybranych raportów pobieramy je na dysk lokalny. Najwygodniej
jest zapisać je w jednym, wybranym katalogu.

UWAGA: Raporty z serwisu bywają niekompletne ze względu na opóźnienie
przesyłania danych z licznika.

## Korzystanie ze skryptu
Skrypt uruchamiamy z linii poleceń. Jedynym wymaganym parametrem jest plik
(lub pliki) do analizy. Możliwe jest stosowanie wieloznaczników (np.: *.csv).
Przy wywołaniu bez parametrów opcjonalnych skrypt dokona porównania wartości
importu, eksportu i stanu magazynu dla bilansowania algebraicznego (starego)
i godzinowego (obowiązującego od 1.04.2022):

```
python bilans.py *.csv
Bilans OZE wersja 1.0, Copyright 2022, Łukasz Cielecki

Bilans OZE wydawany jest ABSOLUTNIE BEZ ŻADNEJ GWARANCJI
W celu uzyskania bliższych informacji - Powszechna Licencja Publiczna GNU
――――――――――――――――――――――――――――――――――――――――
Przetwarzam plik Rap_godzinowy_2022-01-01_2022-01-31.csv
Przetwarzam plik Rap_godzinowy_2022-02-01_2022-02-28.csv
Przetwarzam plik Rap_godzinowy_2022-03-01_2022-03-31.csv
Przetwarzam plik Rap_godzinowy_2022-04-01_2022-04-30.csv
Przetwarzam plik Rap_godzinowy_2022-05-01_2022-05-29.csv
――――――――――――――――――――――――――――――――――――――――
Zakres pomiaru: 01.01.2022 01:00:00 -> 29.05.2022 01:00:00
Mnożnik dla energii zmagazynowanej: 0,8
――――――――――――――――――――――――――――――――――――――――
Import algebraicznie: 1 855,56 kWh
Eksport algebraicznie: 1 473,45 kWh
Magazyn / deficyt algebraicznie: -676,797 kWh
――――――――――――――――――――――――――――――――――――――――
Import zbilansowany: 1 297,32 kWh
Eksport zbilansowany: 915,214 kWh
Magazyn / deficyt zbilansowany: -565,15 kWh
```

### Parametry opcjonalne
**-m**, **--mnoznik**: Mnożnik dla energii magazynowanej. Wartośc domyślna
0,8. W przypadku instalacji 10 kWp lub większych należy stosować mnożnik 0,7.
Parametr ma znaczenie tylko przy obliczaniu energii zmagazynowanej.

**-p**, **--podzial**: Uwzględnij rozpoczęcie bilansowania godzinowego.
Domyślnie za start bilansowania przyjmowana jest data 1.04.2022. Po użyciu
tego przełącznika skrypt będzie dokonywał symylacji bilansowania z uwzględnieniem
algorytmu algebraicznego przed datą 1.04.2022 i godzinowego po tej niej.

**-d**, **--data**: Data wprowadzenie bilansowania godzinowego (RRRR-MM-DD), 
domyślnie 2022-04-01.

Przykład działania skryptu z parametrem **-p** i domyślną datą 1.04.2022:

```
Bilans OZE wersja 1.0, Copyright 2022, Łukasz Cielecki

Bilans OZE wydawany jest ABSOLUTNIE BEZ ŻADNEJ GWARANCJI
W celu uzyskania bliższych informacji - Powszechna Licencja Publiczna GNU
――――――――――――――――――――――――――――――――――――――――
Przetwarzam plik Rap_godzinowy_2022-01-01_2022-01-31.csv
Przetwarzam plik Rap_godzinowy_2022-02-01_2022-02-28.csv
Przetwarzam plik Rap_godzinowy_2022-03-01_2022-03-31.csv
Przetwarzam plik Rap_godzinowy_2022-04-01_2022-04-30.csv
Przetwarzam plik Rap_godzinowy_2022-05-01_2022-05-29.csv
――――――――――――――――――――――――――――――――――――――――
Zakres pomiaru: 01.01.2022 01:00:00 -> 29.05.2022 01:00:00
Mnożnik dla energii zmagazynowanej: 0,8
Uwzględnione wprowadzenie bilansowania godzinowego od 01.04.2022 (włącznie)
――――――――――――――――――――――――――――――――――――――――
Import: 1 607,11 kWh
Eksport: 1 225 kWh
Magazyn / deficyt: -627,107 kWh
```