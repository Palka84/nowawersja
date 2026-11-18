---
name: plan-leczenia-esnan
description: Przygotowanie kalkulacji wewnętrznej i oferty (planu leczenia) Fly4Smile dla pacjenta kliniki Esnan w Stambule na podstawie PDF kliniki – z weryfikacją cen, kosztami organizacyjnymi, schematem zębów zbudowanym z biblioteki rysunków i eksportem PDF w wersji na telefon. Używaj, gdy Paulina przesyła PDF kliniki Esnan, prosi o kalkulację, ofertę podstawową lub szczegółową, wersję angielską albo wizualizację planu leczenia.
---

# Plan leczenia Esnan – Fly4Smile

Ten dokument opisuje cały proces, który do tej pory wykonywał asystent: od PDF kliniki do gotowego pliku `Plan-leczenia-Esnan-pl-Imie-Nazwisko.pdf`. Jest napisany tak, żeby dział IT mógł go wdrożyć 1:1, a koordynatorka mogła przejść go krok po kroku i sprawdzić każdą decyzję.

Pliki w tym folderze:

| Ścieżka | Co to jest |
|---|---|
| `SKILL.md` | ten dokument – wszystkie zasady i proces |
| `KATALOG_RYSUNKOW.md` | co rysujemy w jakiej sytuacji, z przykładami i linkami do Google Drive |
| `katalog/` | przykładowe schematy (JPG) i ich konfiguracje (JSON) do każdej sytuacji |
| `biblioteka/drive_index.csv` | lista wszystkich rysunków na Google Drive z linkami (plik po pliku) |
| `biblioteka/arkusz_procedur.csv` | eksport arkusza „New Common Dental Procedures 2026-11-08” (procedury, ceny, które obrazki) |
| `biblioteka/natural/` | rysunki zębów naturalnych `natural_11.png` … `natural_48.png` (nie ma ich na Drive) |
| `skrypty/` | generatory: schemat zębów, pełne łuki, zatoki, oferta HTML, styl v7, eksport PDF |
| `szablon/` | szablon oferty (HTML v5 z CSS) i stałe zdjęcia (logo, klinika, certyfikaty, opinie, filmy) |
| `przyklad/` | kompletny przykład: JSON pacjenta → schematy → PDF podstawowy i szczegółowy |
| `../cennik/Esnan_cennik_2026-06-19.csv` / `.pdf` | obowiązujący cennik kliniki |
| `../CLAUDE.md` | skrót najważniejszych zasad (stałe ustalenia z Pauliną) |

---

## 1. Rola i granice

- Przenosimy wiernie zakres leczenia z dokumentu kliniki, sprawdzamy arytmetykę, dodajemy koszty organizacyjne i przygotowujemy ofertę.
- **Nie jesteśmy lekarzem.** Nie zmieniamy liczby implantów, koron, zabiegów ani ich lokalizacji. Nie uznajemy automatycznie za błąd, że koron na implantach jest więcej niż implantów (mosty). Gdy dokument jest niejednoznaczny – pytamy, bez własnej diagnozy.
- Nie wymyślamy brakujących cen ani danych. Jeśli czegoś brakuje – pytamy.
- Nie twierdzimy, że plik istnieje, dopóki nie został utworzony i sprawdzony.
- **Starszych planów nie ruszamy** bez wyraźnej prośby Pauliny, nawet gdy zmieniają się zasady.
- Polecenie Pauliny w konkretnej sprawie ma pierwszeństwo przed regułą ogólną (np. „koordynator 400”, „zrób 3 dni / 2 noce”).

## 2. Proces krok po kroku

```
PDF kliniki ──► 1. odczyt ──► 2. weryfikacja ──► 3. KALKULACJA WEWNĘTRZNA ──► akceptacja Pauliny
                                                                                  │
      PDF oferty ◄── 8. kontrola ◄── 7. PDF 520 px ◄── 6. HTML oferty ◄── 5. schematy zębów ◄── 4. odczyt RTG
```

1. **Odczyt całego PDF kliniki**: strona kosztorysowa, opis leczenia, schemat graficzny z RTG (zwykle str. 3–4, ale trzeba sprawdzić), imię i nazwisko, liczba wizyt, czas pobytu („4 days / 3 nights” itp.), odstęp między wizytami.
2. **Weryfikacja**: imię i nazwisko, liczba każdego zabiegu, ceny jednostkowe vs cennik (rozdz. 3), sumy wizyt, transfery (240 EUR/wizytę – czy są już w kwocie kliniki), suma regularna i zniżka. Każdą rozbieżność **zgłaszamy**, nie poprawiamy po cichu.
3. **Kalkulacja wewnętrzna** (rozdz. 6) – to jest pierwszy wynik. Ofertę robimy dopiero po akceptacji Pauliny, chyba że wprost poprosi o gotową ofertę.
4. **Odczyt RTG / schematu kliniki** (rozdz. 5): które zęby pacjent ma, których brakuje, gdzie są istniejące mosty i korony, gdzie klinika zaznaczyła zabiegi. Na tej podstawie numery zębów (FDI) dla każdej pozycji.
5. **Schematy zębów** – po jednym na wizytę (rozdz. 8 i `KATALOG_RYSUNKOW.md`).
6. **HTML oferty** z szablonu (rozdz. 7) – podstawowa albo szczegółowa.
7. **PDF w wersji na telefon** (rozdz. 9).
8. **Kontrola jakości** (rozdz. 11) i dopiero wtedy wysyłka do Pauliny z krótkim podsumowaniem i listą pytań otwartych.

## 3. Ceny

### 3.1 Cennik kliniki
- Obowiązuje cennik Esnan z **19.06.2026** (`cennik/Esnan_cennik_2026-06-19.pdf` i `.csv`), dopóki Paulina go nie zmieni.
- **Cena wyjściowa = cena promocyjna w EUR** (kolumna `cena_promocyjna_eur`). Od niej liczymy kalkulacje, ją podajemy w planach i od niej liczymy obniżki (np. −10%: 200 → 180 EUR).
- Ceny regularne – **tylko** w podsumowaniu rabatu.
- Zabiegu nie ma w cenniku → nie zgadujemy, pytamy.
- PDF kliniki podaje inną cenę niż cennik → najpierw sprawdzamy sumy w PDF, potem **wskazujemy rozbieżność** i pytamy, którą cenę przyjąć (przykład z praktyki: ekstrakcja 85 EUR w PDF vs 30 EUR w cenniku – zostawiono cenę kliniki po decyzji Pauliny).

Najczęstsze ceny promocyjne (EUR):

| Zabieg | Cena |
|---|---|
| Implant Medentika by Straumann (Niemcy) | 421 |
| Implant Straumann (Szwajcaria) | 849 |
| Korona cyrkonowa Amann Girrbach lub Ivoclar na własnym zębie | 200 |
| Korona cyrkonowa Amann Girrbach lub Ivoclar na implancie | 242 |
| Specjalistyczne leczenie kanałowe – jednokanałowe / trzonowce | 149 / 166 |
| Licówka porcelanowa Laminate Veneer / korona porcelanowa Empress | 421 / 421 |
| Licówka kompozytowa | 149 |
| Podniesienie zatoki z augmentacją / szerokie | 718 / 973 |
| Stała tymczasowa praca protetyczna (1 łuk) | 421 |
| Tymczasowa korona na implancie (1 szt.) | 55 |
| Ekstrakcja / ekstrakcja chirurgiczna (Extraction-2) | 30 / 149 |
| Surgical Extraction (osobna pozycja w cenniku) | 336 |

### 3.2 Koszty organizacyjne (Fly4Smile)

| Pozycja | Reguła |
|---|---|
| Hotel | **60 EUR za noc** (kwota kalkulacyjna, zależy od terminu). „4 dni / 3 noce” w PDF kliniki → liczymy **4 noce**. „7 dni / 6 nocy” → **6 nocy**. Inne długości – wg ustaleń z Pauliną (np. „3 dni / 2 noce” → 2 noce). |
| Koordynator | Płatność dla kliniki za wizytę **> 2500 EUR → 300 EUR**, **≤ 2500 EUR → 200 EUR**. Polecenie Pauliny ma pierwszeństwo (bywało 400 EUR albo 0). |
| Transfery | 240 EUR na wizytę, **zwykle już wliczone w płatność dla kliniki** – sprawdzić i nie liczyć podwójnie. |
| Przeloty | poza wyceną; pacjent organizuje je sam. |
| Osoba towarzysząca | nocuje w tym samym pokoju bez dopłaty (o ile nie ma innych ustaleń). |
| Wspólny pokój dwóch pacjentów | koszt jednego pokoju dzielony na pół. Pokój 3-osobowy i dostawka – tylko wg rzeczywistej wyceny / potwierdzonych ustaleń. |
| Dziecko / dostawka (gdy dotyczy) | dziecko do 8 lat bez dodatkowego łóżka – bezpłatnie; dodatkowe łóżko – 30 EUR za dobę. |
| Leki | nie doliczamy. |

### 3.3 Wzory
```
płatność_klinika(wizyta) = suma zabiegów wizyty + transfery (jeśli klinika je wykazuje w swojej kwocie)
zaliczka(wizyta)         = hotel(noce × 60) + koordynator
na_miejscu(wizyta)       = płatność_klinika(wizyta)
koszt_wizyty             = zaliczka + na_miejscu
razem                    = Σ koszt_wizyty
```
Przykład (2 implanty, potem 2 korony na implantach): wizyta I: klinika 842 + 240 = 1082; hotel 2 × 60 = 120; koordynator 200 → zaliczka 320, razem 1402. Wizyta II: klinika 484 + 240 = 724; hotel 4 × 60 = 240; koordynator 200 → zaliczka 440, razem 1164. Łącznie 2566 EUR.

### 3.4 Rabat
- Pokazujemy **raz**, na końcu, a nie w każdym wierszu: cena regularna (z cennika/kliniki), zniżka zaokrąglona do ~30%, jeśli tak wynika z dokumentu, dokładna kwota zniżki, cena po zniżce.
- Obniżka zlecona przez Paulinę (np. −10% na korony) – osobna informacja: „Cena korony … została obniżona z 200 EUR na 180 EUR” + ile to daje łącznie.

### 3.5 Płatności (tekst stały)
Na miejscu gotówką lub fizyczną kartą; transakcje kartą w TRY, opłata operatora 2%; płatności zbliżeniowe nie są akceptowane. **Nie doliczamy 2% do ceny bazowej.**

## 4. Nazewnictwo (obowiązkowe brzmienie)

| Zawsze piszemy | Nigdy |
|---|---|
| korony cyrkonowe **Amann Girrbach lub Ivoclar** (także w podsumowaniach i tabelach) | „korona cyrkonowa” bez marek, „Amann/Ivoclar” |
| implanty **Medentika by Straumann (Niemcy)** albo **implanty Straumann (Szwajcaria)** | „Medentika (grupa Straumann)” w ofercie |
| **podniesienie zatoki** (z augmentacją kości) | „sinus lifting” |
| **stała tymczasowa praca protetyczna mocowana na implantach** | „proteza tymczasowa” (przy stałej pracy) |
| **specjalistyczne leczenia kanałowe – liczba szacunkowa** | – |
| **korona porcelanowa Empress** (= Empress Veneer w nomenklaturze kliniki) | „Emax” |
| **licówka porcelanowa Laminate Veneer** (tylko przednia część zęba) | – |

- Zapis kliniki „laminate/empress veneers” = licówki, a tam, gdzie potrzebna jest korona (np. filar mostu), korony Empress. Obie pozycje kosztują 421 EUR.
- Używamy poprawnego nazwiska pacjenta, nawet jeśli w PDF kliniki jest literówka – i zgłaszamy rozbieżność.
- **Numery zębów (FDI)** wypisujemy zawsze: w opisie planu (wstęp) i przy każdej pozycji zakresu (implanty, korony, mosty, prace tymczasowe), np. „Implant Medentika by Straumann (Niemcy) · zęby 14, 15”, „most 24–26”.

## 5. Zasady medyczne i odczyt RTG

- Na podstawie panoramy RTG i schematu kliniki ustalamy **faktyczne uzębienie**: które zęby są, których brakuje (w tym ósemki!), gdzie są istniejące mosty, korony, wypełnienia, gdzie klinika rysuje implanty / korony / ekstrakcje.
- Jeśli klinika nie podała numerów zębów, ustalamy je ze schematu i RTG; gdy się nie da – pytamy (czasem numery podaje pacjent).
- Ósemki: rysujemy, jeśli są na RTG i nie są usuwane; jeśli ich nie ma – oznaczamy jako brak.
- Podniesienie zatoki zaplanowane → druga wizyta zwykle po ok. 5 miesiącach (jeśli klinika tak wskazuje). Zabieg tylko „możliwy” → rozróżniamy wariant bez i z zabiegiem; niewycenionych procedur nie dodajemy do kosztu.
- Liczba leczeń kanałowych jest szacunkowa – ostateczna po przygotowaniu zębów; mniej zabiegów = proporcjonalnie niższa cena.
- Ekstrakcje przy pełnej implantacji bywają bezpłatne – wtedy **nie piszemy o tym w ofercie**, robimy zwykły plan.
- Oznaczenia kliniki bez ceny (np. znak zapytania, cyfra na RTG) – nie dodajemy do oferty, zgłaszamy jako pytanie.
- Specjalne warunki od Pauliny wpisujemy do „Ważnych informacji” (np. „Do przeprowadzenia leczenia niezbędna jest zgoda onkologa z uprawnieniami na terenie Turcji”).

## 6. Kalkulacja wewnętrzna (pierwszy wynik)

- Tytuł: **„Kalkulacja wewnętrzna – Imię Nazwisko”**. Nie przedstawiamy jej jako oferty dla pacjenta.
- Wstęp: krótki opis leczenia i liczby etapów.
- Dla każdej wizyty: czas pobytu, odstęp do następnej wizyty, zakres osobno dla szczęki i żuchwy (z numerami zębów), tabela pozycji (ilość × cena = suma), transfery, płatność dla kliniki, hotel, koordynator, koszt wizyty, zaliczka, płatność na miejscu.
- Na końcu: zbiorcza tabela płatności, kontrola sum (zgodność z sumami kliniki), cena regularna i zniżka, **lista rozbieżności i pytań**.

## 7. Oferta dla pacjenta

### 7.1 Zasady treści
- Tylko **wersja na telefon** (szerokość 520 px). Wersji „na komputer” nie robimy. Nazwa pliku bez słowa „telefon”: `Plan-leczenia-Esnan-pl-Imie-Nazwisko.pdf` (angielska: `Plan-leczenia-Esnan-en-…`).
- **Oferta podstawowa** (domyślna): bez cen jednostkowych. Na wizytę: tytuł, czas pobytu, schemat zębów, lista pozycji (łuk + opis z numerami zębów + ilość), koszt wizyty.
- **Oferta szczegółowa** (na prośbę): w każdej wizycie dodatkowo tabela **„Koszt leczenia”** (Zabieg / Ilość / Cena jednostkowa / Łącznie) i **„Koszty organizacyjne”** (transfery, hotel, koordynacja i tłumaczenie). Każda widoczna pozycja sumuje się dokładnie do kosztu wizyty. Rabat – raz, na końcu.
- Sekcje stałe szablonu (w tej kolejności): okładka → metryczka (klinika, pacjent, koordynator, data, ważna do = data + 30 dni) → plan leczenia (wizyty) → oś czasu (Wizyta I / Gojenie / Wizyta II) → „Cena każdej wizyty zawiera…” → **Cennik**: tabela Wizyta / Koszt / Zaliczka / Na miejscu + suma → nota o zaliczce → **Ważne informacje** → 3 kroki → gwarancja (paszport implantu, pakiet) → certyfikaty (JCI, Straumann Highest Volume, Diamond Partner Amann Girrbach – z wyróżnieniami tekstu) → o klinice → lokalizacja (hotel–klinika) → opinie → filmy → stopka z WhatsApp.
- Teksty „Ważnych informacji” (domyślne): ważność 30 dni; plan wstępny do potwierdzenia po RTG i badaniu; hotel 60 EUR/dobę – zależnie od terminu; transfery i koordynator w cenie, osoba towarzysząca bez dopłaty; cena nie obejmuje przelotów – pacjent organizuje je we własnym zakresie; płatności (rozdz. 3.5). Plus punkty specyficzne dla pacjenta (zatoka, leczenia kanałowe, onkolog, dostawka, możliwość koron porcelanowych/licówek z różnicą ceny…).
- Opcje leczenia (np. 2–3 warianty) – osobne sekcje/plany w jednym dokumencie, w kolejności wskazanej przez Paulinę.

### 7.2 Styl (wersja v7 – zatwierdzona)
- Ciemniejszy tekst, czcionki ×1.15, białe tło grafik certyfikatów i paszportu implantu, bez plakietek pod certyfikatami.
- Wyróżnienia w tekstach certyfikatów (`.hl`) – **turkusowe podkreślenie-marker zrobione przez `text-decoration`**, nie przez gradient (gradient nie wyświetla się na iPhonie):
  `text-decoration-line:underline; text-decoration-color:#9BF6F1; text-decoration-thickness:.5em; text-underline-offset:-.28em; text-decoration-skip-ink:none; print-color-adjust:exact`.
- Nagłówki: akcent turkusowy jak we wzorze (nie zmieniać kolorów bez prośby).
- W PDF wyłączone cienie (`box-shadow`, `text-shadow`, `filter`) – inaczej powstają szare prostokąty.
- Obrazki kompresowane (schematy 1500 px, JPG q≈74), żeby plik nie był za duży (~2–3 MB).

### 7.3 Dane wejściowe generatora (JSON pacjenta)
`skrypty/buduj_oferte.py` czyta jeden plik JSON – patrz `przyklad/pacjent_przyklad.json`:

| Pole | Opis |
|---|---|
| `pacjent` | imię i nazwisko (też nazwa pliku i tekst WhatsApp) |
| `data`, `wazna_do` | np. „17 lis 2026”, „17 gru 2026” (+30 dni) |
| `koordynator` | domyślnie „Paulina Ayla” |
| `szczegolowa` | `false` = oferta podstawowa, `true` = z tabelami kosztów |
| `opis` | wstęp planu – z numerami zębów |
| `wizyty[]` | `tytul`, `krotko` (np. „wizyta I”), `pobyt` („3 dni / 2 noce”), `schemat` (ścieżka JPG schematu, względna do JSON), `pozycje[]` (`luk`: Szczęka górna / Żuchwa / Dodatkowo, `opis`, `ilosc`: „2×”), `koszt`; dla szczegółowej: `koszt_leczenia` i `koszty_organizacyjne` (`wiersze` [zabieg, ilość, cena jedn., łącznie], `suma` [etykieta, kwota]) |
| `os_czasu` | np. [["Wizyta I","3 dni / 2 noce"],["Gojenie","ok. 3 mies."],["Wizyta II","4 dni / 4 noce"]] |
| `platnosci` | `wiersze` [wizyta, koszt, zaliczka, na miejscu], `razem` |
| `rabat_html` | opcjonalnie blok rabatu (pokazywany raz) |
| `dodatkowe_informacje` | dodatkowe punkty „Ważnych informacji” |

Format kwot w PL: `€1 402,00` (spacja tysięcy, przecinek dziesiętny); w EN: `€1,402.00`.

## 8. Schemat zębów (wizualizacja)

Pełne zasady z przykładami i linkami: **`KATALOG_RYSUNKOW.md`**. Skrót:

- Jeden schemat na wizytę. Wizyta I pokazuje stan po wizycie I (implanty, prace tymczasowe, ekstrakcje), wizyta II – stan końcowy (korony, mosty, protezy).
- Układ: 32 zęby, FDI, górny łuk 18→28 (korzenie do góry), dolny 48→38 (korzenie w dół), linia środkowa i zgryzowa, numer nad/pod każdym zębem. **Strona prawa pacjenta = lewa strona obrazka.**
- Zęby w naturalnych proporcjach (skala anatomiczna Wheelera, 32,7 px = 1 mm w bibliotece), ułożone obok siebie; nie zmniejszać.
- Numer zęba leczonego na danej wizycie – w turkusowej „pigułce”; ząb nieistniejący – szary, przekreślony numer, bez rysunku; ząb własny bez zabiegu – rysunek naturalnego zęba, szary numer.
- Mosty – łącznik w kolorze korony za koronami (turkus dla stałych, bursztyn dla tymczasowych).
- Podniesienie zatoki – rysunek zatoki nad zębem 16 i/lub 26 z podpisem „Podniesienie zatoki — prawa/lewa strona”.
- Pełne łuki (All-on-4/6, proteza tymczasowa, hybrydowa, 12 koron) – gotowe rysunki łuków zamiast pojedynczych zębów.
- Rysunki pochodzą z biblioteki „New Common Dental Procedures 2026-11-08” na Google Drive (`biblioteka/drive_index.csv`), zęby naturalne – z `biblioteka/natural/`.
- **Nie zastępujemy oryginalnego schematu kliniki** w kalkulacji: oryginalną stronę RTG/schematu z PDF kliniki wyodrębniamy jako JPG (`Imie_Nazwisko_plan_leczenia_PELNY.jpg`) i dołączamy do dokumentacji.

## 9. Eksport PDF

```bash
cd skill-plan-leczenia/skrypty
# 0) jednorazowo: wszystkie PNG z Drive (biblioteka/drive_index.csv) do jednego płaskiego folderu <folder_biblioteki_PNG>
#    + przęsła tymczasowe, których nie ma na Drive:
python3 zrob_przesla_tymczasowe.py <folder_biblioteki_PNG> <folder_biblioteki_PNG>
#    (zęby naturalne są gotowe w ../biblioteka/natural; odtworzenie: zrob_zeby_naturalne.py)
# 1) schematy (po jednym na wizytę), zmniejszone do 1500 px
python3 schemat_zebow.py <folder_biblioteki_PNG> ../biblioteka/natural wizyta1.png wizyta1.json
python3 dodaj_zatoki.py wizyta1.png <sinus_lift_one_side.png> wizyta1.jpg prawa|lewa|obie   # tylko gdy jest podniesienie zatoki
# 2) HTML oferty
python3 buduj_oferte.py pacjent.json out/
# 3) styl v7
python3 popraw_v7.py out/oferta-esnan-pl-Imie-Nazwisko.html out/v7.html <folder_ze_zdjeciami_lub_pusty>
# 4) PDF na telefon (520 px, jedna długa strona, reguły @media(max-width:700px) wymuszone)
node topdf.js out/v7.html out/Plan-leczenia-Esnan-pl-Imie-Nazwisko.pdf 520
```
Wymagania: Python 3 + Pillow, Node + Playwright (Chromium), font Inter (`/usr/share/fonts/opentype/inter/`), dostęp do Google Fonts (Manrope, Karla) przy renderowaniu.

`topdf.js`: ustawia szerokość okna 520 px, zamienia `@media(max-width:700px)` na `@media all`, wyłącza cienie, czeka na fonty, drukuje jedną stronę o wysokości całego dokumentu z tłem `#162447`.

## 10. Wersja angielska
Ten sam układ i te same zasady; teksty z `T['en']`, nazwa pliku `Plan-leczenia-Esnan-en-Imie-Nazwisko.pdf`, podpisy zatok `Sinus lift — right/left side` (`dodaj_zatoki.py … en`). Nazwy: „Medentika by Straumann implant (Germany)”, „Amann Girrbach or Ivoclar zirconia crown”.

## 11. Kontrola jakości (przed wysłaniem)

1. Imię i nazwisko pacjenta (też w nazwie pliku i w WhatsApp).
2. Liczba implantów i ich system.
3. Liczba koron na implantach i na własnych zębach; mosty.
4. Liczba leczeń kanałowych (szacunkowa).
5. Liczba nocy i stawka hotelowa.
6. Koordynator na każdej wizycie (reguła 200/300 albo polecenie Pauliny).
7. Transfery bez podwójnego liczenia.
8. Sumy w tabelach, zaliczki, płatności na miejscu, suma całkowita; w szczegółowej – suma wierszy = koszt wizyty.
9. „Amann Girrbach lub Ivoclar” wszędzie.
10. Numery zębów w opisie i przy każdej pozycji.
11. Schemat zgodny z RTG: ósemki, braki, istniejące prace; numery leczonych zębów podświetlone.
12. Brak nieuzasadnionych zmian medycznych.
13. Zgodność kalkulacji wewnętrznej z ofertą.
14. Plik istnieje, ma jedną stronę 520 px, wyróżnienia w certyfikatach są widoczne, brak cieni.

## 12. Błędy, które już się zdarzyły (nie powtarzać)

| Błąd | Prawidłowo |
|---|---|
| Schemat nieostry / zęby za małe | proporcjonalny układ z biblioteki, eksport 2400 px → 1500 px |
| Ósemki narysowane, choć ich nie ma (albo pominięte, choć są) | każdorazowo z RTG; brak = szary przekreślony numer |
| Szare prostokąty (cienie) w PDF | wyłączyć `box-shadow`/`filter` przy druku |
| Wyróżnienia niewidoczne na iPhonie | `text-decoration` zamiast `linear-gradient` |
| Zmiana kolorów nagłówków bez prośby | trzymać się wzoru |
| Poprawiony starszy plan bez prośby | nie ruszać starszych planów |
| Pozostałości tekstów z poprzedniego pacjenta (dostawka, opisy filmów, podwójna oś czasu) | dane pacjenta tylko z JSON; szablon bez treści pacjenta |
| „Emax” zamiast Empress | Empress Veneer = korona porcelanowa Empress; Laminate Veneer = licówka |
| Podniesienie zatoki narysowane nieczytelnie | rysunek zatoki nad 16/26 z podpisem strony |
| Wersja „telefon” w nazwie / wersja desktop | tylko 520 px, nazwa bez „telefon” |

## 13. Pytania otwarte do IT
- Biblioteka PNG ma być pobierana z Drive przy każdym generowaniu, czy trzymana lokalnie (ZIP ~120 MB „New Common Dental Procedures 2026-11-08.zip”)? Zęby naturalne są tylko w tym repozytorium (`biblioteka/natural/`).
- Zdjęcia szablonu w `szablon/img` to wersja odtworzona; oryginały w wysokiej jakości są na Macu Pauliny (`~/Desktop/filmy-claude/oferta-esnan/_narzedzia/obrazki-v7/`) – można je podmienić przez `popraw_v7.py <…> <folder_ze_zdjeciami>`.
