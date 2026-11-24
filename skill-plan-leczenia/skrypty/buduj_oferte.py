"""Fly4Smile – generator oferty (plan leczenia Esnan) z pliku JSON pacjenta.
Użycie:
  python3 buduj_oferte.py <pacjent.json> <katalog_wyjściowy>
Wynik: <katalog>/oferta-esnan-pl-Imie-Nazwisko.html (wszystkie obrazki osadzone base64).
Potem: popraw_v7.py (styl v7) i topdf.js (PDF 520 px, wersja na telefon).
Schemat JSON: patrz przyklad/pacjent_przyklad.json i SKILL.md (rozdz. 7)."""
import re, base64, sys, urllib.parse, os, json

PJSON, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(PJSON, encoding='utf-8'))
PJDIR = os.path.dirname(os.path.abspath(PJSON))
TPL = os.path.join(HERE, '..', 'szablon', 'oferta-esnan-pl-v5.html')
SRC = {'pl': TPL, 'en': TPL}
PHONE_TXT = '+44 7520 636 317'
PHONE = '447520636317'
CASE = P['pacjent']

def wa(text):
    return f'https://wa.me/{PHONE}?text=' + urllib.parse.quote(text)

T = {
 'pl': dict(
  lang='pl',
  title='Plan leczenia — Esnan Dental Clinics Skyland | Fly4Smile',
  tag='Plan leczenia', h1='Twój nowy uśmiech zaczyna się w Stambule',
  sub='Osobisty plan leczenia implantologiczno-protetycznego, przygotowany wspólnie z Esnan Dental Clinics — Skyland.',
  accept_btn='Akceptuję plan — napisz na WhatsApp →', costs_btn='Zobacz koszty',
  wa_accept=f'Dzień dobry, akceptuję plan leczenia ({CASE}) i chcę zarezerwować termin.',
  wa_q=f'Dzień dobry, mam pytanie do mojego planu leczenia ({CASE}).',
  meta=[],  # uzupełniane z JSON
  plan_tag='Plan leczenia', plan_h2='Implantologiczno-protetyczny <span class="accent">plan leczenia</span>',
  plan_intro='',  # z JSON: opis
  stage_cost='Koszt wizyty',
  includes='Cena każdej wizyty zawiera: leczenie stomatologiczne, zakwaterowanie, transfery lotnisko–hotel–klinika oraz opiekę polskojęzycznego koordynatora. Osoba towarzysząca może nocować w tym samym pokoju bez dodatkowych kosztów.',
  price_tag='Cennik', price_h2='Koszt i <span class="accent">harmonogram płatności</span>',
  th=['Wizyta', 'Koszt', 'Zaliczka', 'Na miejscu'],
  rows=[],  # z JSON: platnosci.wiersze
  total_l='Całkowity koszt leczenia i pobytu', total='',
  dep_note='Zaliczka obejmuje zakwaterowanie oraz koszty organizacyjne i stanowi część kosztu danej wizyty.',
  info_h='Ważne informacje',
  info=['Oferta jest ważna 30 dni od daty przygotowania. Po tym czasie cena i dostępność terminów mogą się zmienić.',
        'Plan leczenia ma charakter wstępny i może ulec zmianie po wykonaniu RTG oraz badania klinicznego na miejscu.',
        'Do kalkulacji przyjęto zakwaterowanie w cenie 60 EUR za dobę — cena zależy od terminu pobytu.',
        'Transfery lotnisko – hotel – klinika – hotel – lotnisko oraz opieka polskojęzycznego koordynatora są w cenie każdej wizyty. Osoba towarzysząca może nocować w tym samym pokoju bez dodatkowych kosztów.',
        'Cena nie obejmuje kosztów przelotów — pacjent organizuje je we własnym zakresie.',
        'Płatność na miejscu gotówką lub kartą. Karta: tylko fizyczna (bez płatności zbliżeniowych), transakcja w TRY, opłata operatora 2%.'],
  next_h='Co dalej? <span class="accent">3 proste kroki</span>',
  steps=[('Akceptujesz plan', 'Napisz do nas na WhatsApp — jednym kliknięciem w przycisk poniżej.'),
         ('Wybierasz termin i kupujesz bilety', 'Potwierdzamy z Tobą termin w klinice, a Ty przesyłasz nam godziny lotów.'),
         ('Wpłacasz zaliczkę i przyjeżdżasz', 'Rezerwujemy hotel i wizyty, odbieramy Cię z lotniska — resztą zajmujemy się my.')],
  cta_b='Gotowy na pierwszy krok?', cta_s='Zaakceptuj plan i wybierz termin — termin zawsze potwierdzamy z Tobą.',
  cta_q='Mam pytania — napisz do koordynatora',
  war_tag='Gwarancja', war_h2='Dowody, nie <span class="accent">obietnice</span>',
  war_lead='Każdy implant posiada Paszport implantu — oficjalny zapis marki, modelu i numeru seryjnego implantu umieszczonego w Twojej jamie ustnej. To dowód autentyczności i dokument, którego każdy przyszły dentysta będzie potrzebował do dalszej opieki.',
  pkg_h='Pakiet Standard', pkg_s='Warunki gwarancji',
  pkg=['Dożywotnia gwarancja producenta implantów na wady materiałowe i produkcyjne',
       '5 lat gwarancji kliniki na wszystkie prace stomatologiczne',
       '2 lata opieki pozabiegowej Fly4Smile'],
  pkg_note='Szczegółowe warunki gwarancji określa klinika.',
  about_tag='O klinice', about_h2='Esnan Dental Clinics — Skyland',
  maps='Zobacz klinikę i opinie pacjentów w Google Maps ↗',
  stats=[('2007', 'rok założenia sieci Esnan'), ('1,2 mln', 'pacjentów od 2007 r.'), ('JCI', 'międzynarodowa akredytacja jakości')],
  about_p='Esnan to sieć klinik stomatologicznych w Stambule, działająca od 2007 roku. Skyland to jej główna klinika: implantologia, protetyka, chirurgia i periodontologia w jednym miejscu, z własnym cyfrowym laboratorium (skanery 3D, CAD/CAM, cyfrowe RTG).',
  cert_tag='Wyróżnienia i certyfikaty', cert_h2='Certyfikaty i <span class="accent">wyróżnienia</span>',
  cert_lead='Niezależnie weryfikowalne akredytacje — nie tylko marketingowe deklaracje.',
  certs=[('cert_img_p4_0', 'Certyfikat JCI — Esnan Dental Clinics', 'Akredytacja JCI', 'Ambulatory Care · ważna do 1 lipca 2029',
          ['JCI (Joint Commission International) to <span class="hl">jedna z najbardziej prestiżowych międzynarodowych akredytacji medycznych na świecie</span>. To nie kolejny certyfikat na ścianę — placówka przechodzi rygorystyczny audyt bezpieczeństwa pacjentów, procedur medycznych, sterylizacji i zarządzania ryzykiem, a akredytację trzeba regularnie odnawiać.',
           '<span class="hl">Esnan jest jedyną prywatną kliniką stomatologiczną w Turcji posiadającą JCI. W Polsce żadna prywatna klinika stomatologiczna jej nie posiada.</span> Dla skali: akredytację JCI posiadają w Polsce m.in. <b>duże placówki szpitalne Medicover i LUX MED</b> — czyli instytucje kojarzone z najwyższym standardem prywatnej opieki medycznej.',
           'To najlepiej pokazuje rangę Esnan: nie mówimy o zwykłym gabinecie dentystycznym, ale o klinice stomatologicznej funkcjonującej według międzynarodowych standardów jakości i bezpieczeństwa stosowanych przez wiodące placówki medyczne na świecie.']),
         ('cert_img_p5_1', 'Highest Volume Clinic Türkiye 2025 — Straumann Group i Medentika', 'Highest Volume Clinic — Turcja 2025', 'Straumann Group · 15 000+ implantów w jednym roku',
          ['To wyróżnienie pochodzi <b>bezpośrednio od producentów implantów — Straumann Group i Medentika</b>, a nie od samej kliniki.',
           'Esnan został wyróżniony jako klinika o największym wolumenie implantologicznym w Turcji w 2025 roku — z wynikiem <span class="hl">ponad 15 000 implantów Straumann oraz 13 000 implantów Medentika</span>.',
           'To <b>konkretna, policzalna skala doświadczenia</b>. Dla pacjenta oznacza jedno: trafia do zespołu, dla którego implantologia jest codzienną praktyką wykonywaną na ogromną skalę, a nie zabiegiem przeprowadzanym okazjonalnie.']),
         ('cert_img_p5_0', 'Esnan — pierwszy na świecie Diamond Partner Amann Girrbach', 'Diamond Partner', 'Amann Girrbach · pierwszy na świecie',
          ['Esnan jako <span class="hl">pierwsza klinika na świecie</span> uzyskała status Diamond Partner marki Amann Girrbach — jednego z wiodących producentów technologii i materiałów do cyfrowej protetyki stomatologicznej.',
           '<b>Co to oznacza dla pacjenta?</b> Przede wszystkim dostęp do <b>najnowocześniejszych technologii wykonywania koron i protez</b>, bardzo wysoką precyzję ich projektowania i dopasowania oraz sprawniejszy proces wykonania finalnych zębów.',
           '<span class="hl">W praktyce: większa precyzja, lepsze dopasowanie i krótszy czas oczekiwania na finalny uśmiech.</span>'])],
  chips=['JCI (2026–2029)', 'Straumann® Highest Volume Clinic 2025', 'Medentika 13 000+ implantów', 'Pierwszy na świecie Diamond Partner — Amann Girrbach'],
  badges=['Pierwszy na świecie Diamond Partner Amann Girrbach', 'Straumann Group: klinika z największą liczbą implantów w Turcji w 2025 r. (15 000+)'],
  src_l='Źródła', src=[('JCI — Dental Tribune', 'https://www.dental-tribune.com/news/esnan-becomes-first-private-dental-clinic-in-turkey-to-achieve-jci-accreditation/'),
                       ('Diamond Partner — Amann Girrbach', 'https://www.amanngirrbach.com/en-gb/esnan-becomes-amann-girrbachs-first-diamond-partner/'),
                       ('Highest Volume Clinic 2025 — Straumann', 'https://www.straumann.com/tr/tr/patients/str-certificate-verification/esnandentalclinics-2025-str111.html')],
  src_tail='Liczba pacjentów według danych kliniki.',
  col_alt=['Wnętrza kliniki Esnan Skyland', 'Recepcja kliniki', 'Strefa wypoczynku'],
  loc_tag='Lokalizacja', loc_h2='Hotel i klinika — <span class="accent">wszystko blisko siebie</span>',
  loc_lead='Standardowo zakwaterowanie organizujemy w Icon Hotel Bomonti w dzielnicy Şişli. Transfery hotel–klinika–hotel są w cenie, więc nie musisz sam szukać drogi.',
  map_note='Schemat poglądowy. Odległość drogowa wg Map Google: ok. 7 km.', km='ok. 7 km autem',
  hotel='Hotel', clinic='Klinika', city='Stambuł',
  hotel_btn='Hotel w Mapach Google ↗', clinic_btn='Klinika w Mapach Google ↗', route_btn='Pokaż trasę hotel → klinika ↗',
  rev_tag='Opinie pacjentów', rev_more='Zobacz wszystkie opinie o Fly4Smile w Google ↗', rev_h2='Co mówią nasi <span class="accent">pacjenci</span>',
  reviews=[(10, 'Wilhelm', '22%', 'Pełna rekonstrukcja uśmiechu', 'Na Paulinę trafiłem szukając rozwiązania swoich problemów zdrowotnych na YouTube i od razu wiedziałem, że to osoba, której mogę powierzyć swoje zdrowie. Paulina zorganizowała wszystko: przeloty, transport w Turcji, hotel, dodatkowe ubezpieczenie. Klinika, profesjonalny personel i przebieg leczenia przerosły moje oczekiwania.'),
           (11, 'Tomek', '30%', 'Pełna metamorfoza uśmiechu', 'Od początku do końca mogłem liczyć na Twoje wsparcie, cierpliwość i pełne zaangażowanie, dzięki czemu mój pobyt w Turcji oraz cały proces leczenia przebiegły spokojnie i bez stresu.'),
           (12, 'Weronika', '30%', 'Pełna metamorfoza uśmiechu', 'Paulina była zawsze dostępna pod telefonem i zadbała o to, żeby wszystko było dobrze zorganizowane. Klinika zrobiła na mnie bardzo dobre wrażenie — profesjonalna, czysta i wszystko przebiegło bezproblemowo. Szczerze polecam!'),
           (14, 'Beata', '25%', 'Pełna rekonstrukcja uśmiechu', 'Bardzo ładna i czysta klinika, lekarze profesjonaliści na 100%. Podziękowania dla Pauliny, była bardzo pomocna, polecam skorzystać z jej usług.')],
  vid_tag='Zobacz na własne oczy', vid_h2='Warto obejrzeć <span class="accent">przed przyjazdem</span>',
  vid_p='Na moim kanale YouTube pokazuję prawdziwe historie pacjentów i tłumaczę krok po kroku, jak wygląda leczenie w Turcji — bez medycznego żargonu i bez ukrywania trudnych tematów.',
  vid_more='Więcej historii pacjentów na kanale Fly4Smile →', watch='Oglądaj na YouTube',
  videos=[('sFxOVJNxHsE', 'Korony i implant — relacja pacjentki mieszkającej w Wielkiej Brytanii', 'Zobacz cały proces leczenia z perspektywy pacjentki — od planu po efekt końcowy.'),
          ('o89SVaGqhac', 'Dlaczego marka implantu ma znaczenie i które systemy warto wybrać', 'Nie każdy system implantologiczny oferuje tę samą jakość, dostępność części i przewidywalność na lata. Wyjaśniam, czym różnią się popularne marki i dlaczego w Twoim planie są implanty Medentika by Straumann.'),
          ('TG6kRoWFYkg', 'Korony zębowe — które naprawdę wytrzymają 10+ lat?', 'Monolityczna cyrkonia, porcelana, ceramika szklana: co się dzieje z koronami po latach i dlaczego w Twoim planie są korony cyrkonowe z systemów Amann Girrbach i Ivoclar.')],
  f_contact='KONTAKT', f_clinic='KLINIKA', f_seat='Siedziba',
  f_cta_h='Gotowi na kolejny krok?', f_cta_p='Twój plan jest gotowy, a koordynator czeka na Twoją wiadomość.',
  f_btn='Akceptuję plan — napisz na WhatsApp →', f_btn2='Zadzwoń', f_wa='WhatsApp', f_mail='E-mail',
  passport_alt='Paszport implantu',
 ),
 'en': dict(
  lang='en',
  title='Treatment plan — Esnan Dental Clinics Skyland | Fly4Smile',
  tag='Treatment plan', h1='Your new smile starts in Istanbul',
  sub='A personal implant and prosthetic treatment plan, prepared together with Esnan Dental Clinics — Skyland.',
  accept_btn='I accept the plan — message us on WhatsApp →', costs_btn='See the costs',
  wa_accept=f'Hello, I accept my treatment plan (case {CASE}) and would like to book my dates.',
  wa_q=f'Hello, I have a question about my treatment plan (case {CASE}).',
  meta=[('Case', CASE), ('Prepared for', CASE), ('Coordinator', 'Paulina Ayla'),
        ('Date', '11 Oct 2026'), ('Offer valid until', '10 Nov 2026')],
  plan_tag='Treatment plan', plan_h2='Implant and prosthetic <span class="accent">treatment plan</span>',
  plan_intro='Treatment takes place over two visits, planned around healing time.',
  s1='Stage I — Visit 1', s1d='4 days / 4 nights',
  sinus_h='Sinus lift with bone augmentation',
  sinus_p='The sinus membrane is gently lifted and bone material is placed in the space created — this forms the foundation for a stable implant.',
  s1_alt='Stage I plan — implants', s2_alt='Stage II plan — crowns',
  up='Upper jaw', low='Lower jaw',
  i1='Medentika implant (Straumann Group) · teeth 16, 14, 12, 22, 24, 26',
  i2='Fixed temporary prosthesis on implants — one jaw',
  i3='Sinus lift and bone grafting — one side',
  i4='Medentika implant (Straumann Group) · tooth 36', i5='Simple extraction · tooth 37',
  s2='Stage II — Visit 2', s2d='7 days / 6 nights',
  c1='Zirconia crown on implant (Amann Girrbach / Ivoclar) · teeth 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26',
  c2='Zirconia crown (Amann Girrbach / Ivoclar) · teeth 46, 45, 44, 43, 42, 41, 31, 32, 33, 34, 35',
  c3='Zirconia crown on implant (Amann Girrbach / Ivoclar) · tooth 36',
  stage_cost='Stage cost', p1='€4,766.00', p2='€6,206.00',
  includes='The price of each stage includes: treatment, accommodation, airport–hotel–clinic transfers and a dedicated coordinator. A companion can stay in the same room at no extra cost.',
  tl=[('Stage I', '4 days / 4 nights'), ('Healing period', 'approx. 5 months'), ('Stage II', '7 days / 6 nights')],
  price_tag='Pricing', price_h2='Cost and <span class="accent">payment schedule</span>',
  th=['Stage', 'Stage cost', 'Deposit', 'Payable on site'],
  rows=[('Stage I', '€4,766.00', '€410.00', '€4,356.00'), ('Stage II', '€6,206.00', '€620.00', '€5,586.00')],
  total_l='Total cost of treatment and stay', total='€10,972.00',
  dep_note='The deposit covers accommodation and organisational costs and is part of the cost of the given stage.',
  info_h='Important information',
  info=['This offer is valid for 30 days from the date it was prepared. After that, the price and availability of dates may change.',
        'The treatment plan is preliminary and may change after X-rays and a clinical examination on site.',
        'The calculation assumes accommodation at EUR 60 per night — the price depends on your dates.',
        'The offer does not include flights.',
        'Payment on site by cash or card. Card: physical card only (no contactless), processed in TRY, 2% operator fee.'],
  next_h='What happens next? <span class="accent">3 simple steps</span>',
  steps=[('You accept the plan', 'Message us on WhatsApp — one tap on the button below.'),
         ('You choose your dates and book flights', 'We confirm your dates with the clinic and you send us your flight times.'),
         ('You pay the deposit and come over', 'We book your hotel and appointments and pick you up at the airport — we take care of the rest.')],
  cta_b='Ready for the first step?', cta_s='Accept the plan and choose your dates — we always confirm them with you.',
  cta_q='I have questions — message the coordinator',
  war_tag='Warranty', war_h2='Proof, not <span class="accent">promises</span>',
  war_lead='Every implant comes with an Implant Passport — an official record of the brand, model and serial number of the implant placed in your mouth. It is your proof of authenticity and a document every future dentist will need for follow-up care.',
  pkg_h='Standard Package', pkg_s='Warranty terms',
  pkg=['Lifetime implant manufacturer warranty against material and manufacturing defects',
       '5-year clinic warranty on all dental work',
       '2 years of Fly4Smile aftercare'],
  pkg_note='Detailed warranty terms are set by the clinic.',
  about_tag='About the clinic', about_h2='Esnan Dental Clinics — Skyland',
  maps='See the clinic and patient reviews on Google Maps ↗',
  stats=[('2007', 'year Esnan was founded'), ('1.2M', 'patients since 2007'), ('JCI', 'international quality accreditation')],
  about_p='Esnan is a network of dental clinics in Istanbul, operating since 2007. Skyland is its main clinic: implantology, prosthetics, surgery and periodontology under one roof, with its own digital laboratory (3D scanners, CAD/CAM, digital X-rays).',
  cert_tag='Recognition', cert_h2='Certificates &amp; <span class="accent">achievements</span>',
  cert_lead='Independently verified accreditation, not just marketing claims.',
  certs=[('cert_img_p4_0', 'JCI certificate — Esnan Dental Clinics', 'JCI Accreditation', 'Ambulatory Care · valid through 1 July 2029',
          ['JCI (Joint Commission International) is <span class="hl">one of the most prestigious international medical accreditations in the world</span>. It is not just another certificate on the wall — the clinic undergoes a rigorous audit of patient safety, medical procedures, sterilisation and risk management, and the accreditation must be renewed regularly.',
           '<span class="hl">Esnan is the only private dental clinic in Turkey with JCI accreditation.</span>',
           'That is the best measure of Esnan: not an ordinary dental practice, but a dental clinic operating to the international quality and safety standards used by leading medical institutions worldwide.']),
         ('cert_img_p5_1', 'Highest Volume Clinic Türkiye 2025 — Straumann Group and Medentika', 'Highest Volume Clinic — Türkiye 2025', 'Straumann Group · 15,000+ implants in one year',
          ['This award comes <b>directly from the implant manufacturers — Straumann Group and Medentika</b>, not from the clinic itself.',
           'Esnan was named the clinic with the highest implant volume in Türkiye in 2025 — with <span class="hl">more than 15,000 Straumann implants and 13,000 Medentika implants</span>.',
           'That is <b>concrete, measurable experience</b>. For you it means one thing: you are treated by a team for whom implantology is everyday practice at a huge scale, not an occasional procedure.']),
         ('cert_img_p5_0', "Esnan — Amann Girrbach's world's first Diamond Partner", 'Diamond Partner', "Amann Girrbach · world's first",
          ['Esnan became <span class="hl">the first clinic in the world</span> to achieve Diamond Partner status with Amann Girrbach — one of the leading manufacturers of technology and materials for digital dental prosthetics.',
           '<b>What does it mean for you?</b> Above all, access to <b>the latest technology for making crowns and dentures</b>, very high precision of design and fit, and a faster process for making your final teeth.',
           '<span class="hl">In practice: greater precision, a better fit and a shorter wait for your final smile.</span>'])],
  chips=['JCI Accredited (2026–2029)', 'Straumann® Highest Volume Clinic 2025', 'Medentika 13,000+ Implant Achievement', "World's First Diamond Partner — Amann Girrbach"],
  badges=["Amann Girrbach's world's first Diamond Partner", 'Straumann Group: Highest Volume Clinic in Türkiye 2025 (15,000+ implants)'],
  src_l='Sources', src=[('JCI — Dental Tribune', 'https://www.dental-tribune.com/news/esnan-becomes-first-private-dental-clinic-in-turkey-to-achieve-jci-accreditation/'),
                        ('Diamond Partner — Amann Girrbach', 'https://www.amanngirrbach.com/en-gb/esnan-becomes-amann-girrbachs-first-diamond-partner/'),
                        ('Highest Volume Clinic 2025 — Straumann', 'https://www.straumann.com/tr/tr/patients/str-certificate-verification/esnandentalclinics-2025-str111.html')],
  src_tail='Patient numbers as reported by the clinic.',
  col_alt=['Esnan Skyland clinic interior', 'Clinic reception', 'Relaxation area'],
  loc_tag='Location', loc_h2='Hotel and clinic — <span class="accent">close to each other</span>',
  loc_lead='We normally arrange accommodation at Icon Hotel Bomonti in the Şişli district. Hotel–clinic–hotel transfers are included, so you never have to find your own way.',
  map_note='Illustrative diagram. Road distance according to Google Maps: approx. 7 km.', km='approx. 7 km by car',
  hotel='Hotel', clinic='Clinic', city='Istanbul',
  hotel_btn='Hotel on Google Maps ↗', clinic_btn='Clinic on Google Maps ↗', route_btn='Show route hotel → clinic ↗',
  rev_tag='Patient reviews', rev_more='See all Fly4Smile reviews on Google ↗', rev_h2='What our <span class="accent">patients say</span>',
  reviews=[(10, 'Wilhelm', '22%', 'Full smile reconstruction', 'I found Paulina on YouTube while looking for a solution to my health problems, and I knew right away she was someone I could trust with my health. Paulina organised everything: flights, transport in Turkey, the hotel, additional insurance. The clinic, the professional staff and the course of treatment exceeded my expectations.'),
           (11, 'Tomek', '30%', 'Full smile makeover', 'From start to finish I could count on your support, patience and full commitment, which made my stay in Turkey and the whole treatment calm and stress-free.'),
           (12, 'Weronika', '30%', 'Full smile makeover', 'Paulina was always available by phone and made sure everything was well organised. The clinic made a very good impression on me — professional, clean, and everything went smoothly. I sincerely recommend it!'),
           (14, 'Beata', '25%', 'Full smile reconstruction', 'A very nice and clean clinic, 100% professional doctors. Thanks to Paulina, she was very helpful — I recommend using her services.')],
  vid_tag='See for yourself', vid_h2='Worth watching <span class="accent">before you travel</span>',
  vid_p='On my YouTube channel I share real patient stories and explain step by step what treatment in Turkey looks like — no medical jargon, and no hiding the difficult topics. The videos are in Polish with auto-translated subtitles available.',
  vid_more='More patient stories on the Fly4Smile channel →', watch='Watch on YouTube',
  videos=[('sFxOVJNxHsE', 'Crowns and an implant — the story of a patient living in the UK', 'Ewelina had treatment similar to yours: upper and lower crowns plus an implant. See the whole process from the patient’s perspective — from the plan to the final result.'),
          ('o89SVaGqhac', 'Why the implant brand matters and which systems are worth choosing', 'Not every implant system offers the same quality, parts availability and long-term predictability. I explain how popular brands differ — including Medentika from the Straumann Group, which you will receive.'),
          ('TG6kRoWFYkg', 'Dental crowns — which ones really last 10+ years?', 'Monolithic zirconia, porcelain, glass ceramic: what happens to crowns over the years, and why your plan uses zirconia crowns from Amann Girrbach and Ivoclar systems.')],
  f_contact='CONTACT', f_clinic='CLINIC', f_seat='Registered office',
  f_cta_h='Ready for the next step?', f_cta_p='Your plan is ready and your coordinator is waiting for your message.',
  f_btn='I accept the plan — message us on WhatsApp →', f_btn2='Call', f_wa='WhatsApp', f_mail='E-mail',
  passport_alt='Implant Passport',
 ),
}

EXTRA_CSS = """
.opt-h{font-family:var(--font-display);font-size:21px;color:#0B1220;background:#E9FBFA;border-left:4px solid var(--cyan);padding:12px 16px;margin:28px 0 18px;}
.opt-p{color:#0B1220;margin:-8px 0 16px;}
.dt-h{font-family:var(--font-display);color:var(--navy);font-size:17px;margin:30px 0 10px;}
.dt{width:100%;border-collapse:collapse;font-size:14px;}
.dt th{text-align:left;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#3A4256;border-bottom:2px solid var(--cyan);padding:8px 6px;}
.dt td{padding:11px 6px;border-bottom:1px solid var(--line);color:#0B1220;vertical-align:top;}
.dt th:nth-child(n+2),.dt td:nth-child(n+2){text-align:right;white-space:nowrap;}
.dt .dt-sum td{font-weight:700;color:var(--navy);border-bottom:none;}
.dt .dt-sum td:first-child{text-align:left;}
.disc{margin:24px 0 6px;padding:16px 18px;border-radius:12px;background:#E9FBFA;border:1px solid var(--cyan-muted);display:flex;flex-direction:column;gap:6px;color:#0B1220;font-size:14px;line-height:1.55;}
.disc>b{font-family:var(--font-display);color:var(--navy);font-size:16px;}
.disc s{color:#3A4256;}
@media(max-width:700px){.dt{font-size:13px;}.dt td,.dt th{padding:9px 4px;}}

.rc-card{border:1px solid var(--line);border-radius:18px;overflow:hidden;background:#fff;display:flex;flex-direction:column;}
.rc-card.wide{margin-top:4px;}
.rc-img{background:#0B1626;display:flex;justify-content:center;}
.rc-card.wide .rc-img{background:#fff;border-bottom:1px solid var(--line);}
.rc-img img{height:340px;width:auto;max-width:100%;object-fit:contain;}
.rc-card.wide .rc-img img{height:420px;}
.rc-body{padding:18px 20px 20px;}
.rc-body h3{font-size:16px;color:var(--graphite);}
.rc-body small{display:block;font-size:12.5px;color:var(--muted);margin:2px 0 10px;}
.rc-body p{font-size:13.5px;line-height:1.6;margin-bottom:9px;}
.rc-body p:last-child{margin-bottom:0;}
.rc-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px;}
@media(max-width:700px){.rc-grid{grid-template-columns:1fr;}}

.cert-feature .img-col img{background:none;}
.cert-feature{margin-top:16px;}
*{-webkit-print-color-adjust:exact;print-color-adjust:exact;}
.meta{grid-template-columns:repeat(5,1fr);}
.meta div.valid{color:var(--cyan);font-weight:700;}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:22px;}
.step{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);border-radius:14px;padding:16px 18px;}
.step i{display:inline-flex;width:28px;height:28px;border-radius:50%;background:var(--cyan);color:var(--graphite);font-style:normal;font-family:var(--font-display);font-weight:800;font-size:14px;align-items:center;justify-content:center;margin-bottom:10px;}
.step b{display:block;font-family:var(--font-display);font-weight:800;font-size:14.5px;color:#fff;margin-bottom:4px;}
.step span{font-size:13px;color:#B9C5E6;}
.next-h{font-family:var(--font-display);font-weight:800;font-size:20px;color:#fff;margin-top:30px;}
.next-h .accent{color:var(--cyan);}
.badges{display:flex;flex-direction:column;gap:8px;margin:18px 0;}
.badges .badge-bar{margin:0;}
.sources{font-size:11.5px;color:var(--muted);margin-top:12px;line-height:1.7;}
.sources a{color:var(--muted);}
.pkg-note{font-size:12px;color:var(--muted);padding:10px 20px 14px;border-top:1px solid var(--line);}
.f-top a{color:#fff;text-decoration:none;font-weight:600;}
.f-links{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px;}
.f-links a{display:inline-flex;font-family:var(--font-display);font-weight:700;font-size:12px;color:#fff;border:1px solid rgba(255,255,255,.3);border-radius:999px;padding:7px 14px;text-decoration:none;}
@media(max-width:700px){.steps{grid-template-columns:1fr;}}
"""

def build(lang, imgs):
    t = T[lang]
    src = open(SRC[lang], encoding='utf-8').read()
    css = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
    css = css.replace('@media print{.btn{display:none;} body{font-size:13px;} .section{break-inside:avoid;}}', '')
    css += EXTRA_CSS
    svg = re.search(r'(<svg viewBox="0 0 760 250".*?</svg>)', src, re.S).group(1)
    svg = svg.replace('ok. 7 km autem', t['km']).replace('approx. 7 km by car', t['km'])
    maps_icon = re.search(r'(<svg viewBox="0 0 24 24".*?</svg>)', src, re.S).group(1)
    A = wa(t['wa_accept']); Q = wa(t['wa_q'])
    def tbl(title, head, rows, foot):
        r=''.join('<tr>'+''.join(f'<td>{c}</td>' for c in row)+'</tr>' for row in rows)
        return (f'<h4 class="dt-h">{title}</h4><table class="dt"><tr>'+''.join(f'<th>{h}</th>' for h in head)+'</tr>'+r+
                f'<tr class="dt-sum"><td colspan="{len(head)-1}">{foot[0]}</td><td>{foot[1]}</td></tr></table>')
    I = lambda n: imgs[n]

    meta = ''.join(f'<div{" class=\"valid\"" if i == 4 else ""}><span>{k}</span>{v}</div>' for i, (k, v) in enumerate(t['meta']))
    item = lambda jaw, txt, q: f'<div class="item"><div><small>{jaw}</small>{txt}</div><div class="q">{q}</div></div>'
    rows = ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in t['rows'])
    info = ''.join(f'<li>{x}</li>' for x in t['info'])
    steps = ''.join(f'<div class="step"><i>{n}</i><b>{h}</b><span>{p}</span></div>' for n, (h, p) in enumerate(t['steps'], 1))
    pkg = ''.join(f'<div class="row">{x}</div>' for x in t['pkg'])
    stats = ''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in t['stats'])
    def card(c, wide=False):
        key, alt, h, sub, ps = c
        return (f'<div class="rc-card{" wide" if wide else ""}"><div class="rc-img"><img src="{imgs[key]}" alt="{alt}"></div>'
                f'<div class="rc-body"><h3>{h}</h3><small>{sub}</small>' + ''.join(f'<p>{x}</p>' for x in ps) + '</div></div>')
    cs = t['certs']
    certs = card(cs[0], True) + '<div class="rc-grid">' + card(cs[1]) + card(cs[2]) + '</div>' + '<div class="cert-row">' + ''.join(f'<span class="cert-chip">{x}</span>' for x in t['chips']) + '</div>'
    badges = ''.join(f'<div class="badge-bar">{b}</div>' for b in t['badges'])
    srcs = ' · '.join(f'<a href="{u}">{n}</a>' for n, u in t['src'])
    revs = ''.join(f'<div class="rv-card"><div class="rv-ph"><img src="{I(n)}" alt="{nm}" style="object-position:center {pos}"></div><div class="rv-tx"><div class="rv-stars">★★★★★</div><p>{txt}</p><div class="rv-line"></div><b>{nm}</b><span>{lab}</span></div></div>'
                   for n, nm, pos, lab, txt in t['reviews'])
    vids = ''
    for k, (vid, h, p) in enumerate(t['videos']):
        url = f'https://www.youtube.com/watch?v={vid}'
        vids += (f'<div class="vid{" rev" if k % 2 else ""}"><div class="th"><a href="{url}"><img src="{imgs["yt_" + vid]}" alt="{h}"></a></div>'
                 f'<div class="tx"><h3><a href="{url}">{h}</a></h3><p>{p}</p><a class="yt" href="{url}"><i></i>{t["watch"]}</a></div></div>')


    def visit_html(i, v):
        h = f'<div class="stage-head"{" style=\"margin-top:34px;\"" if i else ""}><h3>{v["tytul"]}</h3><span>{v["pobyt"]}</span></div>'
        h += f'<img class="chart-img" src="{imgs["chart_%d" % i]}" alt="{v["tytul"]}">'
        h += '<div class="items">' + ''.join(item(it['luk'], it['opis'], it['ilosc']) for it in v['pozycje']) + '</div>'
        if P.get('szczegolowa'):
            d = v['koszt_leczenia']
            h += tbl(f'Koszt leczenia — {v["krotko"]}', ['Zabieg','Ilość','Cena jedn.','Łącznie'], d['wiersze'], d['suma'])
            o = v['koszty_organizacyjne']
            h += tbl(f'Koszty organizacyjne — {v["krotko"]}', ['Pozycja','Ilość','Cena jedn.','Łącznie'], o['wiersze'], o['suma'])
        h += f'<div class="stage-cost"><span>{t["stage_cost"]}</span><b>{v["koszt"]}</b></div>'
        return h
    if P.get('opcje'):
        PLAN = ''
        for o in P['opcje']:
            PLAN += f'<h3 class="opt-h">{o["nazwa"]}</h3>'
            if o.get('opis'): PLAN += f'<p class="opt-p">{o["opis"]}</p>'
            PLAN += ''.join(visit_html(i, v) for i, v in o['_wiz'])
    else:
        PLAN = ''.join(visit_html(i, v) for i, v in enumerate(P['wizyty']))
    _tot = P['platnosci']['razem'] if isinstance(P['platnosci']['razem'], list) else [(t['total_l'], P['platnosci']['razem'])]
    _st = ' style="margin-top:12px;"'
    TOTALS = ''.join('<div class="total"' + (_st if k else '') + f'><span>{a}</span><b>{b}</b></div>' for k, (a, b) in enumerate(_tot))
    PLAN += '<div class="timeline">' + ''.join(f'<div class="tl"><i></i><b>{a}</b><span>{b}</span></div>' for a, b in P['os_czasu']) + '</div>'
    if P.get('rabat_html'):
        PLAN += f'<div class="disc">{P["rabat_html"]}</div>'
    body = f"""<div class="page">
<div class="topbar" id="sec-top"><img src="{I(0)}" alt="Fly4Smile"><div class="clinic">Esnan Dental Clinics — Skyland</div></div>
<div class="cover" id="sec-cover">
  <div class="photo" style="background-image:url('{I(1)}')"></div>
  <div class="overlay">
    <span class="tag">{t['tag']}</span>
    <h1>{t['h1']}</h1>
    <p class="sub">{t['sub']}</p>
    <div class="btn-row"><a class="btn btn-accent" href="{A}">{t['accept_btn']}</a></div>
  </div>
</div>
<div class="meta">{meta}</div>

<div class="section" id="sec-plan"><div class="wrap">
  <span class="tag">{t['plan_tag']}</span>
  <h2>{t['plan_h2']}</h2>
  <p class="plan-intro">{t['plan_intro']}</p>
  {PLAN}
  <p class="includes">{t['includes']}</p>
</div></div>

<div class="section dark" id="sec-pricing"><div class="wrap">
  <span class="tag">{t['price_tag']}</span>
  <h2>{t['price_h2']}</h2>
  <table class="pay"><tr>{''.join(f'<th>{h}</th>' for h in t['th'])}</tr>{rows}</table>
  {TOTALS}
  <p class="note">{t['dep_note']}</p>
  <div class="info-box"><h3>{t['info_h']}</h3><ul>{info}</ul></div>
  <h3 class="next-h">{t['next_h']}</h3>
  <div class="steps">{steps}</div>
  <div class="cta-panel">
    <div><b>{t['cta_b']}</b><span>{t['cta_s']}</span></div>
    <div class="btn-row"><a class="btn btn-accent" href="{A}">{t['accept_btn']}</a><a class="btn btn-outline" href="{Q}">{t['cta_q']}</a></div>
  </div>
</div></div>

<div class="section" id="sec-warranty"><div class="wrap">
  <span class="tag">{t['war_tag']}</span>
  <h2>{t['war_h2']}</h2>
  <p class="lead">{t['war_lead']}</p>
  <div class="warranty">
    <div class="passport"><img src="{I(9)}" alt="{t['passport_alt']}"></div>
    <div class="pkg"><div class="hd"><b>{t['pkg_h']}</b><span>{t['pkg_s']}</span></div>{pkg}<div class="pkg-note">{t['pkg_note']}</div></div>
  </div>
</div></div>

<div class="section about" id="sec-about"><div class="wrap">
  <span class="tag">{t['about_tag']}</span>
  <h2>{t['about_h2']}</h2>
  <a class="maps-btn" href="https://maps.app.goo.gl/CdzfoAYNo1TH7wpEA">{maps_icon}{t['maps']}</a>
  <div class="about-stats">{stats}</div>
  <p>{t['about_p']}</p>
  <div class="collage"><img class="wide" src="{I(2)}" alt="{t['col_alt'][0]}"><img class="half" src="{I(3)}" alt="{t['col_alt'][1]}"><img class="half" src="{I(4)}" alt="{t['col_alt'][2]}"></div>
</div></div>

<div class="section" id="sec-certs"><div class="wrap">
  <span class="tag">{t['cert_tag']}</span>
  <h2>{t['cert_h2']}</h2>
  <p class="lead">{t['cert_lead']}</p>
  {certs}
  <p class="sources">{t['src_l']}: {srcs}. {t['src_tail']}</p>
</div></div>

<div class="section" id="sec-where"><div class="wrap">
  <span class="tag">{t['loc_tag']}</span>
  <h2>{t['loc_h2']}</h2>
  <p class="lead">{t['loc_lead']}</p>
  <div class="where-map">{svg}<p class="note" style="margin-top:6px;">{t['map_note']}</p></div>
  <div class="where-grid">
    <div class="where-card"><small>{t['hotel']}</small><b>Icon Hotel Bomonti</b><span>Birahane Sk. No:32, Merkez, 34360 Şişli / {t['city']}</span>
      <a class="btn btn-line" href="https://www.google.com/maps/search/?api=1&amp;query=41.0609136,28.9810779&amp;query_place_id=ChIJ1z8ZFp-3yhQRXbLfFVNm1g4">{t['hotel_btn']}</a></div>
    <div class="where-card"><small>{t['clinic']}</small><b>Esnan Dental Clinics — Skyland</b><span>Ayazağa Mah. Azerbaycan Cad., Skyland İstanbul, D Blok, Sky Atrium, 34415 Sarıyer / {t['city']}</span>
      <a class="btn btn-line" href="https://maps.app.goo.gl/CdzfoAYNo1TH7wpEA">{t['clinic_btn']}</a></div>
  </div>
  <div class="inline-cta"><a class="btn btn-navy" href="https://www.google.com/maps/dir/?api=1&amp;origin=41.0609136,28.9810779&amp;destination=41.1032756,28.9866096&amp;origin_place_id=ChIJ1z8ZFp-3yhQRXbLfFVNm1g4&amp;destination_place_id=ChIJGdribNq3yhQR_iOmv7hQ8io">{t['route_btn']}</a></div>
</div></div>

<!-- Opinie: przed wysyłką potrzebna zgoda pacjentów na użycie imienia, zdjęcia i opinii. -->
<div class="reviews" id="sec-reviews"><div class="wrap">
  <span class="tag">{t['rev_tag']}</span>
  <h2>{t['rev_h2']}</h2>
  <div class="rv-grid">{revs}</div>
  <div class="inline-cta"><a class="btn btn-navy" href="https://maps.app.goo.gl/8K3caWcMiL2NKZZ58">{t['rev_more']}</a></div>
</div></div>

<div class="section" id="sec-video" style="padding-bottom:var(--gap);"><div class="wrap">
  <span class="tag">{t['vid_tag']}</span>
  <h2>{t['vid_h2']}</h2>
  <div class="vid-intro"><p>{t['vid_p']}</p><a class="vid-more" href="https://www.youtube.com/@fly4smile">{t['vid_more']}</a></div>
  {vids}
</div></div>

<div class="footer" id="sec-footer">
  <div class="f-top">
    <div><div class="lab">{t['f_contact']}</div>
      <a href="tel:+{PHONE}">{PHONE_TXT}</a> · <a href="https://wa.me/{PHONE}">WhatsApp</a><br>
      <a href="mailto:kontakt@fly4smile.pl">kontakt@fly4smile.pl</a><br>
      <a href="https://www.fly4smile.pl">www.fly4smile.pl</a> · <a href="https://www.fly4smile.co.uk">www.fly4smile.co.uk</a>
      <div class="f-links"><a href="https://www.instagram.com/fly4_smile/">Instagram</a><a href="https://www.youtube.com/@fly4smile">YouTube</a></div></div>
    <div class="r"><div class="lab">{t['f_clinic']}</div>Esnan Dental Clinics — Skyland<br>Sarıyer, {t['city']}</div>
  </div>
  <div class="f-co"><b>FLY4SMILE MEDICAL TOURISM LTD</b> · Company No. 16059266 (England &amp; Wales)<br>{t['f_seat']}: First Floor Office, 3 Hornton Place, London, W8 4LZ, United Kingdom</div>
  <div class="cta">
    <h2>{t['f_cta_h']}</h2>
    <p>{t['f_cta_p']}</p>
    <div class="btn-row"><a class="btn btn-accent" href="{A}">{t['f_btn']}</a><a class="btn btn-outline" href="tel:+{PHONE}">{t['f_btn2']} {PHONE_TXT}</a></div>
  </div>
</div>
</div>"""
    head = (f'<!DOCTYPE html>\n<html lang="{lang}">\n<head>\n<meta charset="UTF-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>{t["title"]}</title>\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Karla:wght@400;500;600;700&display=swap" rel="stylesheet">\n'
            f'<style>{css}</style>\n</head>\n<body>\n')
    return head + body + '\n</body>\n</html>\n'

IMG = os.path.join(HERE, '..', 'szablon', 'img') + '/'
def uri(fn, base=IMG):
    path = fn if os.path.isabs(fn) else os.path.join(base, fn)
    mime = 'image/png' if path.endswith('.png') else 'image/jpeg'
    return f'data:{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode()
# dane pacjenta -> pola szablonu PL
t = T['pl']
t['wa_accept'] = f'Dzień dobry, akceptuję plan leczenia ({CASE}) i chcę zarezerwować termin.'
t['wa_q'] = f'Dzień dobry, mam pytanie do mojego planu leczenia ({CASE}).'
t['meta'] = [('Klinika', 'Esnan Skyland'), ('Przygotowano dla', CASE), ('Koordynator', P.get('koordynator', 'Paulina Ayla')),
             ('Data', P['data']), ('Oferta ważna do', P['wazna_do'])]
t['plan_intro'] = P['opis']
if P.get('naglowek_planu'): t['plan_h2'] = P['naglowek_planu']
if P.get('podtytul'): t['sub'] = P['podtytul']
t['rows'] = [tuple(r) for r in P['platnosci']['wiersze']]
if P['platnosci'].get('naglowki'): t['th'] = P['platnosci']['naglowki']
t['total'] = P['platnosci']['razem'] if isinstance(P['platnosci']['razem'], str) else ''
if P.get('dodatkowe_informacje'):
    t['info'] = t['info'] + P['dodatkowe_informacje']
imgs = {0: uri('00.png')}
for k in [1,2,3,4,9,10,11,12,14]: imgs[k] = uri(f'{k:02d}.jpg')
for c in ['cert_img_p4_0','cert_img_p5_0','cert_img_p5_1','yt_sFxOVJNxHsE','yt_o89SVaGqhac','yt_TG6kRoWFYkg']: imgs[c] = uri(c + '.jpg')
if P.get('opcje'):
    k = 0
    for o in P['opcje']:
        o['_wiz'] = []
        for v in o['wizyty']:
            o['_wiz'].append((k, v)); imgs['chart_%d' % k] = uri(v['schemat'], PJDIR); k += 1
else:
    for i, v in enumerate(P['wizyty']): imgs['chart_%d' % i] = uri(v['schemat'], PJDIR)
os.makedirs(OUT, exist_ok=True)
p = os.path.join(OUT, 'oferta-esnan-pl-' + CASE.replace(' ', '-') + '.html')
open(p, 'w', encoding='utf-8').write(build('pl', imgs))
print(p, os.path.getsize(p) // 1024, 'KB')
