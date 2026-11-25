English version for the IT team. The Polish original is SKILL.md; if they differ, ask Paulina.

> For the image-proportion rules for the system, see **IT_SPEC_image_proportions_EN.md** (short, self-contained spec).

---
name: plan-leczenia-esnan
description: Preparing the internal calculation and the Fly4Smile offer (treatment plan) for a patient of the Esnan clinic in Istanbul based on the clinic's PDF – with price verification, organisational costs, a tooth chart built from the drawing library and a PDF export in the phone version. Use when Paulina sends an Esnan clinic PDF, asks for a calculation, a basic or detailed offer, an English version or a visualisation of the treatment plan.
---

# Esnan treatment plan – Fly4Smile

This document describes the entire process that the assistant has performed so far: from the clinic's PDF to the finished file `Plan-leczenia-Esnan-pl-Imie-Nazwisko.pdf`. It is written so that the IT department can implement it 1:1, and the coordinator can walk through it step by step and check every decision.

Files in this folder:

| Path | What it is |
|---|---|
| `SKILL.md` | this document (Polish original) – all rules and the process |
| `KATALOG_RYSUNKOW.md` | what we draw in which situation, with examples and links to Google Drive |
| `katalog/` | sample charts (JPG) and their configurations (JSON) for each situation |
| `biblioteka/drive_index.csv` | list of all drawings on Google Drive with links (file by file) |
| `biblioteka/arkusz_procedur.csv` | export of the spreadsheet "New Common Dental Procedures 2026-11-08" (procedures, prices, which images) |
| `biblioteka/natural/` | drawings of natural teeth `natural_11.png` … `natural_48.png` (they are not on Drive) |
| `skrypty/` | generators: tooth chart, full arches, sinuses, HTML offer, v7 style, PDF export |
| `szablon/` | offer template (HTML v5 with CSS) and fixed photos (logo, clinic, certificates, reviews, videos) |
| `przyklad/` | complete example: patient JSON → charts → basic and detailed PDF |
| `../cennik/Esnan_cennik_2026-06-19.csv` / `.pdf` | the clinic's current price list (cennik) |
| `../CLAUDE.md` | summary of the most important rules (standing agreements with Paulina) |

---

## 1. Role and boundaries

- We faithfully transfer the scope of treatment from the clinic's document, check the arithmetic, add organisational costs and prepare the offer.
- **We are not a doctor.** We do not change the number of implants, crowns or procedures, nor their location. We do not automatically treat it as an error when there are more crowns on implants than implants (bridges). When the document is ambiguous – we ask, without making our own diagnosis.
- We do not invent missing prices or data. If something is missing – we ask.
- We do not claim a file exists until it has been created and checked.
- **We do not touch older plans** without an explicit request from Paulina, even when the rules change.
- Paulina's instruction in a specific case takes precedence over a general rule (e.g. "coordinator 400", "make it 3 days / 2 nights").

## 2. Step-by-step process

```
Clinic PDF ──► 1. reading ──► 2. verification ──► 3. INTERNAL CALCULATION ──► Paulina's approval
                                                                                  │
      Offer PDF ◄── 8. check ◄── 7. PDF 520 px ◄── 6. offer HTML ◄── 5. tooth charts ◄── 4. reading the X-ray
```

1. **Read the entire clinic PDF**: the cost estimate page, the treatment description, the graphic chart with the X-ray (usually pages 3–4, but this must be checked), first name and surname, number of visits, length of stay ("4 days / 3 nights" etc.), interval between visits.
2. **Verification**: first name and surname, the quantity of each procedure, unit prices vs the price list (chapter 3), visit totals, transfers (240 EUR/visit – whether they are already included in the clinic's amount), regular total and discount. We **report** every discrepancy; we do not silently correct it.
3. **Internal calculation** (chapter 6) – this is the first output. We prepare the offer only after Paulina's approval, unless she directly asks for a finished offer.
4. **Reading the X-ray / clinic chart** (chapter 5): which teeth the patient has, which are missing, where existing bridges and crowns are, where the clinic marked procedures. On this basis, the tooth numbers (FDI) for each item.
5. **Tooth charts** – one per visit (chapter 8 and `KATALOG_RYSUNKOW.md`).
6. **Offer HTML** from the template (chapter 7) – basic or detailed.
7. **PDF in the phone version** (chapter 9).
8. **Quality check** (chapter 11), and only then send to Paulina with a short summary and a list of open questions.

## 3. Prices

### 3.1 Clinic price list
- The Esnan price list dated **19.06.2026** applies (`cennik/Esnan_cennik_2026-06-19.pdf` and `.csv`) until Paulina changes it.
- **Base price = promotional price in EUR** (column `cena_promocyjna_eur`). We calculate from it, we quote it in plans and we calculate reductions from it (e.g. −10%: 200 → 180 EUR).
- Regular prices – **only** in the discount summary.
- Procedure not in the price list → we do not guess, we ask.
- The clinic PDF gives a different price than the price list → first we check the totals in the PDF, then we **point out the discrepancy** and ask which price to use (real-world example: extraction 85 EUR in the PDF vs 30 EUR in the price list – the clinic's price was kept after Paulina's decision).

Most common promotional prices (EUR):

| Procedure | Price |
|---|---|
| Medentika by Straumann implant (Germany) | 421 |
| Straumann implant (Switzerland) | 849 |
| Amann Girrbach or Ivoclar zirconia crown on own tooth | 200 |
| Amann Girrbach or Ivoclar zirconia crown on implant | 242 |
| Specialist root canal treatment – single-canal / molars | 149 / 166 |
| Laminate Veneer porcelain veneer / Empress porcelain crown | 421 / 421 |
| Composite veneer | 149 |
| Sinus lift with bone augmentation / wide | 718 / 973 |
| Fixed temporary prosthesis (1 arch) | 421 |
| Temporary crown on implant (1 pc.) | 55 |
| Extraction / surgical extraction (Extraction-2) | 30 / 149 |
| Surgical Extraction (separate item in the price list) | 336 |

### 3.2 Organisational costs (Fly4Smile)

| Item | Rule |
|---|---|
| Hotel | **60 EUR per night** (calculation amount, depends on the dates). "4 days / 3 nights" in the clinic PDF → we count **4 nights**. "7 days / 6 nights" → **6 nights**. Other lengths – as agreed with Paulina (e.g. "3 days / 2 nights" → 2 nights). |
| Coordinator | Payment to the clinic per visit **> 2500 EUR → 300 EUR**, **≤ 2500 EUR → 200 EUR**. By default the coordinator is Polish-speaking. **English-speaking coordinator → 0 EUR**, but only when Paulina specifies this for a particular patient (deposit = hotel only; in the texts „anglojęzycznego koordynatora” ("an English-speaking coordinator"), the deposit note without „kosztów organizacyjnych” ("organisational costs")). Paulina's instruction takes precedence (it has been 400 EUR or 0). |
| Transfers | 240 EUR per visit, **usually already included in the payment to the clinic** – check this and do not count it twice. |
| Flights | outside the quote; the patient arranges them on their own. |
| Accompanying person | stays in the same room at no extra charge (unless otherwise agreed). |
| Shared room for two patients | the cost of one room split in half. Triple room and extra bed – only according to the actual quote / confirmed arrangements. |
| Child / extra bed (where applicable) | child up to 8 years old without an extra bed – free of charge; extra bed – 30 EUR per night. |
| Medication | we do not add it. |

### 3.3 Formulas
```
clinic_payment(visit) = sum of the visit's procedures + transfers (if the clinic includes them in its amount)
deposit(visit)        = hotel(nights × 60) + coordinator
on_site(visit)        = clinic_payment(visit)
visit_cost            = deposit + on_site
total                 = Σ visit_cost
```
Example (2 implants, then 2 crowns on implants): visit I: clinic 842 + 240 = 1082; hotel 2 × 60 = 120; coordinator 200 → deposit 320, total 1402. Visit II: clinic 484 + 240 = 724; hotel 4 × 60 = 240; coordinator 200 → deposit 440, total 1164. Grand total 2566 EUR.

### 3.4 Discount
- The amounts in the discount box must match the payment table: regular price (including transfers) → discount → **price after discount = the "on-site" total** (e.g. 12 491 → −3 515 → 8 976 EUR). In the text of the box we do not mention transfers: „Cena regularna według cennika kliniki: X EUR · zniżka ok. 30% (Y EUR) · cena po zniżce: Z EUR” ("Regular price according to the clinic's price list: X EUR · discount approx. 30% (Y EUR) · price after discount: Z EUR").
- We show it **once**, at the end, not in every row: regular price (from the price list/clinic), discount rounded to ~30% if that follows from the document, exact discount amount, price after discount.
- A reduction ordered by Paulina (e.g. −10% on crowns) – a separate note: „Cena korony … została obniżona z 200 EUR na 180 EUR” ("The price of the crown … has been reduced from 200 EUR to 180 EUR") + how much this amounts to in total.

### 3.5 Payments (fixed text)
On site in cash or with a physical card; card transactions in TRY, 2% operator fee; contactless payments are not accepted. **We do not add the 2% to the base price.**

## 4. Naming (mandatory wording)

The offers are generated in Polish, so the mandatory wording is given in Polish, with an English translation in parentheses.

| We always write | Never |
|---|---|
| „korony cyrkonowe **Amann Girrbach lub Ivoclar**” ("Amann Girrbach or Ivoclar zirconia crowns") (also in summaries and tables) | „korona cyrkonowa” ("zirconia crown") without the brands, „Amann/Ivoclar” |
| „implanty **Medentika by Straumann (Niemcy)**” ("Medentika by Straumann implants (Germany)") or „**implanty Straumann (Szwajcaria)**” ("Straumann implants (Switzerland)") | „Medentika (grupa Straumann)” ("Medentika (Straumann group)") in the offer |
| „**podniesienie zatoki**” ("sinus lift") (z augmentacją kości – "with bone augmentation") | „sinus lifting” |
| „**stała tymczasowa praca protetyczna mocowana na implantach**” ("fixed temporary prosthesis on implants") | „proteza tymczasowa” ("temporary denture") (for a fixed prosthesis) |
| „**specjalistyczne leczenia kanałowe – liczba szacunkowa**” ("specialist root canal treatments – estimated number") | – |
| „**korona porcelanowa Empress**” ("Empress porcelain crown") (= Empress Veneer in the clinic's nomenclature) | „Emax” |
| „**licówka porcelanowa Laminate Veneer**” ("Laminate Veneer porcelain veneer") (front part of the tooth only) | – |

- The clinic's notation "laminate/empress veneers" = veneers, and where a crown is needed (e.g. a bridge abutment), Empress crowns. Both items cost 421 EUR.
- We use the patient's correct surname, even if there is a typo in the clinic PDF – and we report the discrepancy.
- **Tooth numbers (FDI)** are always listed: in the plan description (introduction) and with every item of the scope (implants, crowns, bridges, temporary prostheses), e.g. „Implant Medentika by Straumann (Niemcy) · zęby 14, 15” ("Medentika by Straumann implant (Germany) · teeth 14, 15"), „most 24–26” ("bridge 24–26").

## 5. Medical rules and reading the X-ray

- Based on the panoramic X-ray and the clinic's chart we establish the **actual dentition**: which teeth are present, which are missing (including wisdom teeth!), where existing bridges, crowns and fillings are, where the clinic draws implants / crowns / extractions.
- If the clinic did not give tooth numbers, we establish them from the chart and the X-ray; when that is not possible – we ask (sometimes the patient provides the numbers).
- Wisdom teeth: we draw them if they are on the X-ray and are not being extracted; if they are absent – we mark them as missing.
- Sinus lift planned → the second visit is usually after approx. 5 months (if the clinic indicates so). Procedure only "possible" → we distinguish a variant without and with the procedure; we do not add unpriced procedures to the cost.
- The number of root canal treatments is an estimate – final after the teeth are prepared; fewer procedures = proportionally lower price.
- Extractions with full implantation are sometimes free of charge – in that case **we do not mention this in the offer**, we make a normal plan.
- Clinic markings without a price (e.g. a question mark, a digit on the X-ray) – we do not add them to the offer, we report them as a question.
- Special conditions from Paulina are entered in „Ważne informacje” ("Important information") (e.g. „Do przeprowadzenia leczenia niezbędna jest zgoda onkologa z uprawnieniami na terenie Turcji” – "Consent from an oncologist licensed in Turkey is required to carry out the treatment").

## 6. Internal calculation (first output)

- Title: **„Kalkulacja wewnętrzna – Imię Nazwisko”** ("Internal calculation – First name Surname"). We do not present it as an offer for the patient.
- Introduction: short description of the treatment and the number of stages.
- For each visit: length of stay, interval to the next visit, scope separately for the upper jaw and the lower jaw (with tooth numbers), table of items (quantity × price = total), transfers, payment to the clinic, hotel, coordinator, visit cost, deposit, on-site payment.
- At the end: summary payment table, check of totals (consistency with the clinic's totals), regular price and discount, **list of discrepancies and questions**.

## 7. Offer for the patient

### 7.1 Content rules
- Only the **phone version** (width 520 px). We do not make a "desktop" version. File name without the word "telefon" ("phone"): `Plan-leczenia-Esnan-pl-Imie-Nazwisko.pdf` (English: `Plan-leczenia-Esnan-en-…`).
- **Basic offer** (default): without unit prices. Per visit: title, length of stay, tooth chart, list of items (arch + description with tooth numbers + quantity), visit cost.
- **Price list section (every offer):** below the payment table a „Razem” ("Total") row (cost / deposits / on site) and a box „Zaliczki łącznie” ("Total deposits") + „Na miejscu łącznie — cena leczenia po zniżce” ("Total on site — treatment price after discount"); the on-site amount = the price after discount from the „Twoja zniżka” ("Your discount") box. The generator calculates this itself.
- **Detailed offer** – heading „Szczegółowy plan leczenia” ("Detailed treatment plan"), and in the „Cennik” ("Price list") section, above the payment table, a summary table **„Szczegółowa wycena — wszystkie pozycje”** ("Detailed quote — all items") (each visit: procedures with unit price, transfers, hotel, coordinator, „Razem — wizyta” ("Total — visit"), and at the end the total cost). The generator does this itself when `"szczegolowa": true`. The file is sent with the suffix `-szczegolowa` ("-detailed") so that the phone does not show an old cached copy.
- **Detailed offer** (on request): in each visit additionally a table **„Koszt leczenia”** ("Treatment cost") (Zabieg / Ilość / Cena jednostkowa / Łącznie – "Procedure / Quantity / Unit price / Total") and **„Koszty organizacyjne”** ("Organisational costs") (transfers, hotel, coordination and interpreting). Every visible item adds up exactly to the visit cost. Discount – once, at the end.
- Fixed template sections (in this order): cover → summary card (clinic, patient, coordinator, date, valid until = date + 30 days) → treatment plan (visits) → timeline (Wizyta I / Gojenie / Wizyta II – "Visit I / Healing / Visit II") → „Cena każdej wizyty zawiera…” ("The price of each visit includes…") → **Cennik** ("Price list"): table Wizyta / Koszt / Zaliczka / Na miejscu ("Visit / Cost / Deposit / On site") + total → deposit note → **Ważne informacje** ("Important information") → 3 steps → warranty (10 years: Esnan clinic certificate, Amann Girrbach Zolid certificate, implants – lifetime from the manufacturer + implant passport, 2 years of Fly4Smile care; exclusions: esnandentalclinics.com/warranty) → certificates (JCI, Straumann Highest Volume, Diamond Partner Amann Girrbach – with text highlights) → about the clinic → location (hotel–clinic) → reviews → videos → footer with WhatsApp.
- "Important information" texts (default): validity 30 days; preliminary plan to be confirmed after X-ray and examination; hotel 60 EUR/night – depending on the dates; transfers and coordinator included in the price, accompanying person at no extra charge; the price does not include flights – the patient arranges them on their own; payments (chapter 3.5). Plus patient-specific points (sinus, root canal treatments, oncologist, extra bed, the option of porcelain crowns/veneers with a price difference…).
- Treatment options (e.g. 2–3 variants) – separate sections/plans in one document, in the order specified by Paulina.

### 7.2 Style (version v7 – approved)
- Darker text, fonts ×1.15, white background for the certificate and implant passport graphics, no badges under the certificates.
- Highlights in the certificate texts (`.hl`) – **turquoise marker-style underline made with `text-decoration`**, not with a gradient (the gradient does not display on iPhone):
  `text-decoration-line:underline; text-decoration-color:#9BF6F1; text-decoration-thickness:.5em; text-underline-offset:-.28em; text-decoration-skip-ink:none; print-color-adjust:exact`.
- Headings: turquoise accent as in the template (do not change colours without a request).
- In the PDF, shadows are disabled (`box-shadow`, `text-shadow`, `filter`) – otherwise grey rectangles appear.
- Images compressed (charts 1500 px, JPG q≈74) so the file is not too large (~2–3 MB).

### 7.3 Generator input data (patient JSON)
`skrypty/buduj_oferte.py` reads a single JSON file – see `przyklad/pacjent_przyklad.json`:

| Field | Description |
|---|---|
| `pacjent` | patient's first name and surname (also used in the file name and the WhatsApp text) |
| `data`, `wazna_do` | offer date and valid-until date, e.g. "17 lis 2026", "17 gru 2026" (+30 days) |
| `koordynator` | coordinator; default "Paulina Ayla" |
| `szczegolowa` | "detailed": `false` = basic offer, `true` = with cost tables |
| `opis` | description: plan introduction – with tooth numbers |
| `wizyty[]` | visits: `tytul` (title), `krotko` (short label, e.g. "wizyta I" – "visit I"), `pobyt` (length of stay, "3 dni / 2 noce" – "3 days / 2 nights"), `schemat` (path to the chart JPG, relative to the JSON), `pozycje[]` (items: `luk` (arch): "Szczęka górna" / "Żuchwa" / "Dodatkowo" – "Upper jaw" / "Lower jaw" / "Additionally", `opis` (description), `ilosc` (quantity): "2×"), `koszt` (cost); for the detailed offer: `koszt_leczenia` (treatment cost) and `koszty_organizacyjne` (organisational costs) (`wiersze` (rows) [procedure, quantity, unit price, total], `suma` (total) [label, amount]) |
| `opcje[]` | options: instead of `wizyty`, when the offer has several options: `nazwa` (name), optionally `opis` (description), `wizyty[]` (as above); in that case `platnosci.naglowki` (headers) = ["Opcja / wizyta" ("Option / visit"), …], and `platnosci.razem` (total) = list [label, amount] – one total per option |
| `naglowek_planu`, `podtytul` | plan heading and subtitle; optional – e.g. „Protetyczny plan leczenia” ("Prosthetic treatment plan") when there are no implants |
| `gwarancja` | warranty; optional: `lead`, `naglowek` (heading), `podtytul` (subtitle), `punkty[]` (points), `uwaga` (note), `obraz` (image, e.g. `certyfikaty_gwarancji.jpg` from `szablon/img`), `opis_obrazu` (image caption) – e.g. without the implant point when there are no implants in the plan |
| `os_czasu` | timeline, e.g. [["Wizyta I","3 dni / 2 noce"],["Gojenie","ok. 3 mies."],["Wizyta II","4 dni / 4 noce"]] (["Visit I","3 days / 2 nights"],["Healing","approx. 3 months"],["Visit II","4 days / 4 nights"]) |
| `platnosci` | payments: `wiersze` (rows) [visit, cost, deposit, on site], `razem` (total) |
| `rabat_html` | optional discount block (shown once) |
| `dodatkowe_informacje` | additional points for "Important information" |

Amount format in PL: `€1 402,00` (space as thousands separator, decimal comma); in EN: `€1,402.00`.

## 8. Tooth chart (visualisation)

Full rules with examples and links: **`KATALOG_RYSUNKOW.md`** (English version: `DRAWING_CATALOG_EN.md`). Summary:

- One chart per visit. Visit I shows the state after visit I (implants, temporary prostheses, extractions), visit II – the final state (crowns, bridges, dentures/prostheses).
- Layout: 32 teeth, FDI, upper arch 18→28 (roots pointing up), lower arch 48→38 (roots pointing down), midline and occlusal line, number above/below each tooth. **Patient's right side = left side of the image.**
- Teeth in natural proportions (Wheeler's anatomical scale, 32.7 px = 1 mm in the library), placed side by side; do not shrink them.
- Number of a tooth treated at the given visit – in a turquoise "pill"; non-existent tooth – grey, crossed-out number, no drawing; own tooth without a procedure – drawing of a natural tooth, grey number.
- Bridges – a connector in the crown's colour behind the crowns (turquoise for fixed, amber for temporary).
- Sinus lift – drawing of the sinus above tooth 16 and/or 26 with the caption „Podniesienie zatoki — prawa/lewa strona” ("Sinus lift — right/left side").
- Full arches (All-on-4/6, temporary prosthesis, hybrid, 12 crowns) – ready-made arch drawings instead of individual teeth. When an arch appears together with individual teeth, everything is at one scale: the arch is inserted exactly in place of the teeth it covers (`"arch"` in the `schemat_zebow.py` configuration, see KATALOG_RYSUNKOW.md chapter 4a). Never scale the arch and the teeth separately.
- The drawings come from the library "New Common Dental Procedures 2026-11-08" on Google Drive (`biblioteka/drive_index.csv`), natural teeth – from `biblioteka/natural/`.
- **We do not replace the clinic's original chart** in the calculation: we extract the original X-ray/chart page from the clinic PDF as a JPG (`Imie_Nazwisko_plan_leczenia_PELNY.jpg`) and attach it to the documentation.

## 9. PDF export

```bash
cd skill-plan-leczenia/skrypty
# 0) one-off: all PNGs from Drive (biblioteka/drive_index.csv) into a single flat folder <folder_biblioteki_PNG>
#    + temporary pontics, which are not on Drive:
python3 zrob_przesla_tymczasowe.py <folder_biblioteki_PNG> <folder_biblioteki_PNG>
#    (natural teeth are ready in ../biblioteka/natural; to regenerate: zrob_zeby_naturalne.py)
# 1) charts (one per visit), downscaled to 1500 px
python3 schemat_zebow.py <folder_biblioteki_PNG> ../biblioteka/natural wizyta1.png wizyta1.json
python3 dodaj_zatoki.py wizyta1.png <sinus_lift_one_side.png> wizyta1.jpg prawa|lewa|obie   # only when there is a sinus lift (prawa = right, lewa = left, obie = both)
# 2) offer HTML
python3 buduj_oferte.py pacjent.json out/
# 3) v7 style
python3 popraw_v7.py out/oferta-esnan-pl-Imie-Nazwisko.html out/v7.html <folder_ze_zdjeciami_lub_pusty>
# 4) PDF for phone (520 px, one long page, @media(max-width:700px) rules forced on)
node topdf.js out/v7.html out/Plan-leczenia-Esnan-pl-Imie-Nazwisko.pdf 520
```
Requirements: Python 3 + Pillow, Node + Playwright (Chromium), Inter font (`/usr/share/fonts/opentype/inter/`), access to Google Fonts (Manrope, Karla) during rendering.

`topdf.js`: sets the window width to 520 px, replaces `@media(max-width:700px)` with `@media all`, disables shadows, waits for fonts, prints a single page with the height of the whole document on a `#162447` background.

## 10. English version
Same layout and same rules; texts from `T['en']`, file name `Plan-leczenia-Esnan-en-Imie-Nazwisko.pdf`, sinus captions `Sinus lift — right/left side` (`dodaj_zatoki.py … en`). Names: "Medentika by Straumann implant (Germany)", "Amann Girrbach or Ivoclar zirconia crown".

## 11. Quality check (before sending)

1. Patient's first name and surname (also in the file name and in WhatsApp).
2. Number of implants and their system.
3. Number of crowns on implants and on own teeth; bridges.
4. Number of root canal treatments (estimated).
5. Number of nights and the hotel rate.
6. Coordinator at every visit (200/300 rule or Paulina's instruction).
7. Transfers not counted twice.
8. Totals in the tables, deposits, on-site payments, grand total; in the detailed offer – sum of rows = visit cost.
9. „Amann Girrbach lub Ivoclar” ("Amann Girrbach or Ivoclar") everywhere.
10. Tooth numbers in the description and with every item.
11. Chart consistent with the X-ray: wisdom teeth, missing teeth, existing work; numbers of treated teeth highlighted.
12. No unjustified medical changes.
13. Internal calculation consistent with the offer.
14. The file exists, has one page 520 px wide, the certificate highlights are visible, no shadows.

## 12. Mistakes that have already happened (do not repeat)

| Mistake | Correct |
|---|---|
| Chart blurry / teeth too small | proportional layout from the library, export 2400 px → 1500 px |
| Wisdom teeth drawn although absent (or omitted although present) | each time from the X-ray; missing = grey crossed-out number |
| Grey rectangles (shadows) in the PDF | disable `box-shadow`/`filter` when printing |
| Highlights invisible on iPhone | `text-decoration` instead of `linear-gradient` |
| Heading colours changed without a request | stick to the template |
| An older plan corrected without a request | do not touch older plans |
| Leftover texts from the previous patient (extra bed, video descriptions, double timeline) | patient data only from the JSON; template without patient content |
| "Emax" instead of Empress | Empress Veneer = Empress porcelain crown; Laminate Veneer = veneer |
| Sinus lift drawn illegibly | drawing of the sinus above 16/26 with a side caption |
| Version "telefon" ("phone") in the name / desktop version | only 520 px, name without "telefon" |

## 13. Open questions for IT
- Should the PNG library be downloaded from Drive on every generation, or kept locally (ZIP ~120 MB "New Common Dental Procedures 2026-11-08.zip")? The natural teeth exist only in this repository (`biblioteka/natural/`).
- The template photos in `szablon/img` are a reconstructed version; the high-quality originals are on Paulina's Mac (`~/Desktop/filmy-claude/oferta-esnan/_narzedzia/obrazki-v7/`) – they can be swapped in via `popraw_v7.py <…> <folder_ze_zdjeciami>`.
