# Fly4Smile – Esnan treatment-plan package (for the IT team)

This folder contains everything needed to reproduce Fly4Smile's treatment-plan offers for patients of the Esnan clinic (Istanbul): the business rules, the tooth-chart drawing rules, the drawing library index, the offer template and working scripts.

The **offers themselves are in Polish** (patients are Polish). All documentation, file names, JSON keys and code comments are in English; Polish appears only in patient-facing texts that must stay exactly as written.

## Start here

| File | What it is |
|---|---|
| `TREATMENT_PLAN_RULES.md` | All business rules: reading the clinic PDF, price list, hotel/coordinator/deposit calculation, naming, medical rules, offer structure, detailed offer, QA checklist. |
| `DRAWING_CATALOG.md` | Which drawing is used in which clinical situation (per-tooth states, full arches, sinus lift), with Google Drive links and examples. |
| `IMAGE_PROPORTIONS_SPEC.md` | **Short spec for the chart rendering in the system** – how the images must be prepared and laid out so that proportions are correct. |
| `SKILL.md`, `KATALOG_RYSUNKOW_PL.md` | Polish originals (used by Paulina / Claude). If anything differs, ask Paulina. |

## Folders

| Folder | Content |
|---|---|
| `scripts/` | `tooth_chart.py` (tooth chart), `full_arch_chart.py`, `add_sinus_lift.py`, `sinus_without_implants_chart.py`, `build_offer.py` (offer HTML from patient JSON), `apply_v7_style.py` (final style), `to_pdf.js` (520 px phone PDF), `normalize_images.py` (image library → system format), `make_natural_teeth.py`, `make_temp_pontics.py`, `generate_catalog.py` (Polish catalog) |
| `library/` | `drive_index.csv` – every drawing on Google Drive with its link; `procedures_sheet.csv` – procedure sheet export; `natural_teeth/` – natural-tooth drawings (not on Drive) |
| `catalog/` | Example chart for every situation (`*.jpg`) and its chart config (`*.json`) |
| `example/` | Complete example: `example_patient.json` (basic offer), `example_patient_detailed.json` (detailed offer), chart configs, resulting PDFs (`example_offer_basic_PL.pdf`, `example_offer_detailed_PL.pdf`) |
| `system_example/` | `tooth_chart_example.html` – the chart built only from normalized images + CSS (reference for the system) |
| `template/` | `offer_template_v5.html` (CSS/SVG source) and fixed photos in `img/` |
| `../cennik/` | Esnan price list 19.06.2026 (`Esnan_cennik_2026-06-19.csv` / `.pdf`) – promo prices are the base prices |

## Pipeline (one patient)

```bash
cd scripts
# 1) one chart per visit (config = tooth states for that visit)
python3 tooth_chart.py <drive_png_folder> ../library/natural_teeth visit1.png visit1.json
python3 add_sinus_lift.py visit1.png <sinus_lift_one_side.png> visit1.jpg left     # only if there is a sinus lift
# 2) offer HTML from the patient JSON (English keys, Polish values)
python3 build_offer.py ../example/example_patient.json out/
# 3) final style + phone PDF (520 px, single long page)
python3 apply_v7_style.py out/oferta-esnan-pl-Jan-Kowalski.html out/v7.html <photos_folder_or_empty>
node to_pdf.js out/v7.html out/Plan-leczenia-Esnan-pl-Jan-Kowalski.pdf 520
```
Requirements: Python 3 + Pillow, Node + Playwright (Chromium), Inter font, access to Google Fonts (Manrope, Karla).

## Patient JSON (input) – keys

`patient`, `date`, `valid_until`, `coordinator`, `detailed` (true = detailed offer with unit prices), `intro`, `visits[]` (`title`, `short`, `stay`, `chart`, `items[]` {`jaw`, `text`, `qty`}, `cost`, and for detailed offers `treatment_costs` / `organisational_costs` {`rows`, `total`}), or `options[]` {`name`, `description`, `visits[]`} for multi-option offers, `timeline`, `payments` {`headers`, `rows`, `total`}, `discount_html`, `extra_info[]`, optional `plan_heading`, `subtitle`, `warranty` {`lead`, `heading`, `subheading`, `points`, `note`}.
Values are the Polish texts shown to the patient – see `example/example_patient.json`.
