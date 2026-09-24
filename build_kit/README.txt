LA course build kit v3 (re-upload this zip in a later session so nothing has to be rebuilt)
  content/            one JSON per part = single source for slide text, timings, notes
  build_html.js, deck.css, deck.client.js   -> node build_html.js content/<part>.json out/<part>.html
  build_pptx.js       optional PowerPoint copy of any part
  audit/decisions.py  keep/rebuild/update/merge/move/cut decision + reason for all 93 Week-1 source slides
  audit/inventory.json per-slide words, images (pixel sizes), notes for the five Week-1 decks
  audit/inv.py, build_board.py  regenerate the inventory and the review board from the uploaded decks
Agreed rules: HTML delivery; 30-35 slides per 45' part, one idea per slide; formal Greek in the lecturer's own wording
("Να θυμάστε", "Προβληματισμοί"); no slide presupposes student answers; max one 60-90s timed question per theory part,
label = timer; no repeated part label, small slide number only; sources mostly 2020+; outline approved before any build.

Style additions (approved): running text fully justified where lines are long enough; plan slide has no footline;
break slide reads "Επιστρέφουμε σε 15′" with a 15:00 countdown that starts when the slide opens (T restarts it).
Use build_html2.js + deck2.css (v2 engine). Part 1 content: content/w1p1_v2.json.

Part 2: content/w1p2.json; its images (the lecturer's ViLLE visuals, cropped from his slides 3.40-3.49) are in img_w1p2/ .
To rebuild Part 2, set meta.imgDir in w1p2.json to the folder that holds those images.

LAB DECISION (approved): OULAD is NOT used for the labs.
  Lab 1 (Week 2, Part 2): a DESIGNED CASE with known ground truth - a simulated first-year programming course at a Greek
    university (~300 students: eclass logins, lab submissions as error/success sequences as in the lecturer's Markov-chain study,
    midterm, January exam), calibrated on published effect sizes, with four planted features: one valid indicator, one confounded
    proxy, one reverse-causality trap (like Course Signals), one subgroup that is measured worse. The debrief reveals the
    data-generating process. The student pack says on its first page that the data are simulated.
  Lab 2 (Week 3, Part 2): REAL data - Realinho, Machado, Baptista & Martins (2022), "Predicting Student Dropout and Academic
    Success", Data 7(11), 146; UCI dataset 697; Polytechnic Institute of Portalegre; 4,424 students, 36 features, one CSV,
    CC BY 4.0; part of a deployed tool that gives the tutoring team a dropout-risk estimate.
  Week 1 slides were already patched accordingly (OULAD stays only as an example of scale and of a relational schema).
Week 1 is complete: content/w1p1_v2.json, content/w1p2.json (+ img_w1p2/), content/w1p3.json, workbook/make_wb.py.

WEEK 2 (in progress)
  audit/inv_any.py            inventory for any deck numbers: python3 inv_any.py 6,7,8,9 inventory_w2.json (run where d6.pptx ... are)
  audit/inventory_w2.json     per-slide words, images, notes for decks 6-9 (42 slides)
  audit/decisions_w2.py       keep/rebuild/update/merge/move/cut + reason for all 42 slides (review board v1)
  audit/outline_w2p1.py       Week 2 Part 1 outline v1 (35 slides, 45') + source list with what was actually opened
  audit/build_board_w2.py     python3 build_board_w2.py <folder with r/d6-01.jpg renders> <out.html>; also writes content/w2p1_outline.md
  img_w2p1/                   the lecturer's original figures for Part 1 (7.9 t-SNE, 7.10, 7.11 k-means). NOTE: the dividing lines on 7.11 are
                              PowerPoint shapes, so slide figures must be cropped from high-resolution RENDERS of the slides, not from these files.
  Status: review board and Part 1 outline sent, waiting for approval. Proposal: transition matrix = worked example on slides (23-24) + one 60 s poll;
          the exercise lives in Lab 1 (pre-computed matrices in the student pack).
  Routing: deck 6 and 7.12-7.14 -> W3.P3; 7.2-7.11 (+ ideas of 9.6, 9.8) -> W2.P1; 7.15, 9.10 -> W2.P3; decks 8 and 9 otherwise cut.
  Still to verify when their part comes: framework paper behind deck 6, publication behind the VR robotics study (7.12-7.15), credit for the chart chooser (9.10).

==================== KIT v4 (adds Week 2, Part 1) ====================
New in this version
  content/w2p1.json      Week 2 Part 1, 35 slides, 45 min (42 + 3 slack on the break), skippable 21 and 31, one 60-s poll (25).
  img_w2p1/              kmeans_7_11.png = crop of the 200-dpi render of the lecturer's slide 7.11 (his lines and labels kept);
                         tsne_7_9.png   = his original figure on white. Originals s7_*.png kept beside them.
  audit/                 inventory_w2.json, decisions_w2.py, outline_w2p1.py, build_board_w2.py, inv_any.py (decks 6-9 audit, approved outline).
Build, check, PDF
  node build_html2.js content/w2p1.json out/W2P1.html
  python3 shot2.py /abs/path/out/W2P1.html out/s_ ""          (layout check, all slides; must end "problems: 0")
  Student PDF: open the HTML, press P, save as PDF (one slide per page); or Playwright page.pdf(prefer_css_page_size, print_background) with print media.
Engine changes (all backward compatible; Week 1 slide HTML verified byte-identical)
  meta.imgDir may be relative: it is resolved against the engine folder.
  Any slide type accepts kicker / kickerTone (amber | red | green).
  definition: a callout may carry items[] instead of t.     poll: seqs[{label,seq}] shows E/S chips.
  table: wideTag:true widens the tag column.                 shotside: caption under the image.      compare: left:true = no justification.
New slide types
  gradetab   tableTitle, head[], rows[][], hiCol, arrow{top,bottom}, side{h,prefix,items[]} or quote + notesOn[]
  seqflow    pipe{from,a1,mid[[k,t]],a2,to,loop}, cols[2], students[{label,seq,tag}], foot   (pairs are generated from seq)
  chain2     a{k,name,tone}, b{...}, p{aa,ab,ba,bb}, seq, seqMap, seqLabel, statement, points[] | legend[[k,t]]
  tmatrix    seq, step 1|2, seqLabel, pairLabel, tabLabel, foot   (counts and probabilities are COMPUTED from seq)
  adjmatrix  corner, states[{n,k,name}], matrixNote, steps[{h,t}], foot   (allowed transitions per Lokkila et al. 2023, Table 1)
  anatomy    upto 1|2, weeks, cut, pointLabel, lanes[2]{h,sub,end}, train[], apply[] (chips {t,cls} and ">"), foot
Class names: do not reuse .model or .act for new components (taken by reveal and poll). New chip classes are mdl / actn.
Hash navigation only applies on load (file.html#12); inside a session use keys, the run sheet or the buttons.


==================== v5 (Week 2, Part 2: Group Lab 1) ====================
Deck:  content/w2p2.json is GENERATED. Do not edit it by hand: edit lab1/make_deck_json.py and re-run it.
       node build_html2.js content/w2p2.json out/W2P2.html ; python3 shot2.py /abs/out/W2P2.html out/p2_ ""   (must report 0 problems)
New slide types (appended to build_html2.js / deck2.css; Week 1 and W2P1 slide HTML verified byte-identical):
  work      prompts + timer (timerSec); the timer is the only time label on the slide
  datagrid  what is recorded in which week, with the prediction line (weeks, cut, rows[{h,sub,weeks[],exam}])
  bars      native bar panels: panels[{h,unit:'%'|'',bars[{l,v,n,tone}] | groups[{h,bars}],dense,flex,note}], points[], lesson
  dgp       process diagram traces <- causes -> outcomes, upto 1|2 for the build-up
  compare   now also accepts tone 'blue' / 'amber'
Class-name warning: deck2.css already uses .model .act .trace (and many short names). New components use mdl/actn/trc/dn/dg*.
Lab pipeline (lab1/), run in this order; every number shown anywhere comes from exhibits.json:
  simulate.py        -> cohort_*_full.csv, subs_*.csv, logins_*.csv   (seeds 36 and 71; parameters documented in the key, p.2)
  exhibits.py        -> exhibits.json                                  (single source of all numbers)
  make_deck_json.py  -> ../content/w2p2.json, midterm_bands.json
  build_pack.py      -> ../out/Lab1_pack.html   ; topdf.py html pdf   (prints an overflow check; must say "none")
  build_key.py       -> ../out/Lab1_key.html    ; topdf.py html pdf
  export_data.py     -> data/*.csv, data/teacher/*.csv                 (re-computes P(E->S) from raw submissions as a check)
  build_notebooks.py -> Lab1_notebook_student.ipynb, Lab1_notebook_teacher.ipynb (data embedded; test-run with nbclient)
Terminology fixed for the lab: flag = «επισήμανση / επισημαίνονται» (never «σημαίνει», which reads as "means").

==================== v6 (Week 2, Part 3: dashboards + assignment workshop 1) ====================
Deck:  content/w2p3.json is GENERATED by workshop1/make_deck_json.py (ERIC counts from workshop1/eric_counts.json, mock-up numbers from lab1/).
       node build_html2.js content/w2p3.json out/W2P3.html ; python3 shot2.py /abs/out/W2P3.html out/p3_ ""   (must report 0 problems)
       26 slides, 45 min; timers on 5 (01:00), 22 (14:00), 23 (02:30 per team); skippable 8 and 13; last slide is an endslide carrying the 3 min of slack.
New slide types (appended; Week 1, W2P1 and W2P2 slide HTML verified byte-identical):
  shotmark    screenshot with native numbered markers: marks[{x,y,w,h,label}] in % of the image; with timerSec + question it becomes the timed question
  chooser     four purposes (comparison, relationship, distribution, composition), each with q, ex and charts[{g,l}]; glyph ids in GLY
  methodpics  four cards: method, glyph g, h, t
  mock        native teacher-screen mock-up: bar[2], tiles[{v,l}], lists[{tone,h,n,rule,action}], strip, foot
  funnel      search narrowed block by block: rows[{code,n,verdict,tone}]
  Extensions: em() now turns `text` into <code>; bars panels accept bw (bar width, px); grid accepts tall:true.
Workshop pipeline (workshop1/), in this order:
  eric_counts.py      -> eric_counts.json   real counts from eric.ed.gov with the retrieval date. RE-RUN BEFORE EACH NEW YEAR: slides 19-20, the handout and the
                         teacher sheet pick the numbers up automatically. Check afterwards that the verdicts on slide 20 (above 500 / below 40) still hold.
  ../workbook/make_wb_v2.py -> ../out/LA_review_templates_v2.xlsx ; then python3 /mnt/skills/public/xlsx/scripts/recalc.py on it (must report 0 errors)
  render_sheet.py     -> ../img_w2p3/sheet0.png   (image of the builder sheet for slide 18; needs LibreOffice + pdftoppm)
  make_deck_json.py   -> ../content/w2p3.json
  build_handout.py    -> ../out/Workshop1_handout.html and ../out/Workshop1_teacher.html ; ../lab1/topdf.py html pdf (overflow check must say "none")
The ViLLE collage (img_w2p3/ville_collage.png) is the lecturer's own image from source deck 7, slide 15.
Set-up fixed with the lecturer: the review ASSIGNMENT is single or pair work; in-class LAB work is one team of about four per Zoom room, one search string per room.
Audit and outline of this part: audit/outline_w2p3.py, audit/build_board_w2p3.py.

==================== v7a (Week 3, Part 1: audit and outline ONLY; nothing is built yet) ====================
Status: review board and 32-slide outline sent; WAITING FOR THE LECTURER'S APPROVAL. Do not build before it.
  audit/outline_w3p1.py        outline v1 (32 slides, 45 min = 42 + 3 slack on the break; timed question on 8; skippable 14 and 19),
                               verdicts on the old Week 3 files (OLD), promises of Weeks 1-2 with the slide that pays each (PROMISES),
                               and the source list with what was actually opened (SOURCES).
  audit/build_board_w3p1.py    python3 build_board_w3p1.py  -> out/W3P1_review_board.html and content/w3p1_outline.md (asserts 45 minutes)
  w3p1/lab1_numbers.py         every number Part 1 borrows from the Lab 1 case, from the two LOCKED cohorts -> w3p1/lab1_numbers.json.
                               Never name a script numbers.py: it shadows a Python standard module and breaks pandas.
Decisions taken in the audit
  The old Week 3 material (E3 practicals DS1/DS2, findings PDF, instructions, LA revision deck) is cut: the practical data are noise and the
  risk label leaks into the classifier; the PDF contradicts its own HTML files. The systematic-review revision deck moves to W3.P3 (workshop 2).
  One slide of the LA revision deck survives in Part 1: the three types of intervention (slide 24), in the lecturer's wording.
  Part 1 has no source deck. It stands on the Lab 1 numbers of THIS YEAR'S cohort (298 students; they match the teacher screen of W2.P3:
  298, 192, 98, 67) and on sources opened online (list in outline_w3p1.py). Already taught in Week 1 and therefore NOT repeated: OU Analyse,
  MAAPS, Georgia State, Course Signals, Baker & Hawn (2022). Precision/recall were never named in Weeks 1-2: slide 5 names them once.
  At build: open Ofqual's own 2020 report and look for a published version of Perdomo et al. (2023); open the full texts where a slide
  needs a table from inside a paper. New slide type needed: a four-cell "people" matrix (check the class name is free in deck2.css).
Open question put to the lecturer: a revision element in Week 3? Default = no class time, a two-page revision sheet from the nine
  "Να θυμάστε" slides in the final package.
Still missing: source decks 4, 6 and 7 as .pptx (images are needed for W3.P2 and W3.P3; their text and decisions are in audit/).

==================== v7 (Week 3, Part 1: BUILT, checked and delivered) ====================
Deck:  content/w3p1.json is GENERATED by w3p1/make_deck_json.py (Lab 1 numbers from w3p1/lab1_numbers.json and lab1/exhibits.json; the script
       stops if the cohort no longer gives 298 / 192 / 98 / 67, the figures of the teacher screen of W2.P3).
       python3 w3p1/lab1_numbers.py ; python3 w3p1/make_deck_json.py ; node build_html2.js content/w3p1.json out/W3P1.html
       python3 shot2.py /abs/out/W3P1.html out/w3p1_ ""      (must end "problems: 0")
       32 slides, 45 min (42 + 3 slack on the break slide); timed question on 8 (01:00); skippable 14 and 19; ends on the break slide.
New slide type (appended; Week 1, W2P1, W2P2 and W2P3 slide HTML verified byte-identical, deck2.css is a pure append, class prefix ppl):
  people   the confusion matrix as four groups of people: cols[2], rows[2], cells[4]{n,h,t,tone: green|amber|red|grey} in reading order,
           side[{v,l}] (three dark metric tiles), lesson
Things learnt about existing types while building
  cards3 and compare REQUIRE foot / lesson (the engine prints "undefined" otherwise).   fact: a big value with any character other than
  digits . , + is set in the smaller "word" style (39,1% and x4 are).   bars with unit '' scales every panel to its own maximum, so counts that
  must be comparable go in ONE panel with groups[]; with unit '%' use max to zoom (0.25 on slide 18).   barH sets the bar height (240 default).
Checks done for this part: layout check 0 problems; three contact sheets and six revised slides looked at; timer on 8 counts down and T pauses it;
  break countdown starts by itself; plan slide shows 18:15 / 19:15 / 20:15; speaker window opens with N and follows the deck; placeholder scan
  clean (the only date-like hit is the fraction 1/6 on slide 7); student PDF 32 pages, two pages looked at.
Sources: audit/outline_w3p1.py lists what was opened. Added at build: Ofqual's own documents (small-cohort rule, Annex Q on socio-economic
  groups: Ofqual found similar adjustments across groups; the press found larger drops for poorer pupils; both are in the notes of slide 20) and
  the published version of Perdomo et al. (ACM FAccT 2025, doi 10.1145/3715275.3732175; the numbers on slide 28 were read in arXiv:2304.06205v2).
NEXT: Week 3, Part 2 = Group Lab 2 on Realinho et al. (2022), UCI 697, then the ethics debrief (GDPR, AI Act, the seven questions of deck 4).
  Part 1 has already promised Lab 2 three things: choose the action BEFORE the threshold (slide 11), check the errors per subgroup (15-18, 22),
  write the message to the student (26). Three questions were explicitly sent to Part 2: must an intervention always pass through a person (23),
  should the message reveal that a model exists (26), fairness auditing against data minimisation (19).
  Still missing: source decks 4, 6 and 7 as .pptx (images). Every detail of the Realinho dataset is still to be verified online.

==================== v8a (Week 3, Part 2: audit and outline ONLY; nothing is built yet) ====================
Status: review board and 23-slide outline sent; WAITING FOR THE LECTURER'S APPROVAL. Do not build before it. Week 3, Part 1 is FINAL.
  audit/outline_w3p2.py, audit/build_board_w3p2.py -> out/W3P2_review_board.html and content/w3p2_outline.md (asserts 45 minutes)
  lab2/raw/data.csv            the real dataset (UCI 697, downloaded from archive.ics.uci.edu; ';' separated, 4,424 rows, 37 columns, CC BY 4.0)
  lab2/explore.py              feasibility analysis behind the outline: three prediction moments, threshold sweep, top-k, subgroups, weights.
                               seed 697, 80/20 stratified split, logistic regression (C = 0.3) on standardised dummies; outcome = Dropout against the rest.
Design: 4' briefing, 15' teams (timer), 5' two teams report (02:30 each), 5' what the exhibits showed, 4' GDPR and AI Act, 8' the lecturer's seven
  questions (one slide each, verbatim, existing "definition" layout) + his closing question (skippable), remember, break. Skippable 11 and 21.
  No file is needed from the lecturer for Part 2. Deck 4 images are all cut (third-party); the teacher quote 4.16 is cut unless he names its source.
At build: open every GDPR / AI Act article on EUR-Lex before its slide is written (Week 1 verified Annex III and Article 5 only); open Prinsloo & Slade
  (2017), Kaliisa et al. (2025), the NYT piece on Illuminate; read in the data descriptor: number of degrees, years covered, definition of "Enrolled",
  coding of Gender. Build the lab like Lab 1: one locked numbers file -> deck JSON, pack, key, data export, notebooks. No dates on slides.
Two data cautions for the teacher key: 180 rows have zero ENROLLED units in semester 1 and 75 of those students graduated; the Zenodo copy of the
  dataset is restricted while the UCI copy is open.
For Part 3 only: the lecturer's PowerPoints "6. Τεχνολογίες Εμβύθισης" and "7. Ενδεικτικά Παραδείγματα" (his architecture figure 6.10 and the VR robotics
  slides 7.12-7.14 cannot be recreated from text).

==================== v8b (still outline stage for W3.P2; sources for W3.P3 secured) ====================
  sources_w3p3/                the lecturer's two PowerPoints for Part 3 (deck 6, 10 slides; deck 7, 16 slides), so no re-upload is ever needed.
  img_w3p3/ + manifest.json    every picture of deck 6 and of deck 7 slides 12-15 at full resolution, named d<deck>_s<slide>_<k>; the two that
                               cannot be redrawn are d6_s10_1.png (system architecture, 2937x1150) and d7_s12_1.jpeg (VR robotics, 1920x947).
  LEGAL UPDATE found while verifying Part 2: Regulation (EU) 2026/1744 (the "Digital Omnibus on AI", in force since summer 2026) postponed the
  high-risk obligations of Annex III (education included), amended Article 4 (AI literacy) and moved/widened the bias-detection legal basis of
  Article 10(5). Week 1 (slide 31) gave no dates and stays correct. In Part 2: years only, no dates; read the Official Journal text at build.
  Opened so far for Part 2: AI Act Arts 4, 10(5), 14(4)(b), 86; GDPR Art. 22(1), Recital 43; UCI record, data file, data descriptor front matter.

==================== v8 (Week 3, Part 2 = GROUP LAB 2 + ethics debrief: BUILT, checked and delivered) ====================
Deck:  content/w3p2.json is GENERATED by w3p2/make_deck_json.py from lab2/numbers.json (the script stops if 4424 / 885 / 284 / 270 / 99 / 71 change).
       23 slides, 45 min: 4 briefing, 15 teams (timer 15:00), 5 two teams report (02:30 each), 5 what the exhibits showed, 4 GDPR + AI Act,
       7 + 1 the lecturer's seven questions and his closing question, 1 remember, 3 break (slack). Skippable 11 and 21. NO engine change in this part.
       The seven questions are verbatim from source deck 4 with two grammar fixes (συγκατάθεσή -> συγκατάθεση; επρόκειτο -> πρόκειται); 4.7 keeps only its question.
Lab:   lab2/ (see lab2/README_lab2.txt). Deliverables: out/Lab2_pack.pdf (8 pp.), out/Lab2_key.pdf (5 pp.), lab2/Lab2_notebook_student.ipynb, lab2/Lab2_notebook_teacher.ipynb, lab2/data/.
Checks done: layout 0 problems; both contact sheets looked at; timers on 5 and 6 count down, pause with T and reset; break countdown starts by itself;
       speaker window opens with N and follows; placeholder scan clean over deck, pack and key; no calendar dates on slides (dates only in notes and in the key);
       pack and key: "pages overflowing: none", all pages looked at; notebooks test-run and equal to numbers.json; student PDF 23 pages.
Sources opened for this part: UCI record + file; data descriptor (front matter, abstract); GDPR Art. 5(1)(b)(c), 15(1)(h), 22(1), Recital 43; AI Act Art. 4, 10(5), 14, 86
       (and the titles of 13 and 15); Regulation (EU) 2026/1744 through five concordant legal notes (the OJ text itself was NOT opened); CJEU C-634/21 through four
       legal notes; Prinsloo & Slade (2017): citation only, no finding is attributed to it; NYT (2022) on Illuminate: first paragraphs.
       NOT used because not verified: AI Act Art. 4 on a slide (the 2026 amendment touched it), Art. 26, Kaliisa et al. (2025), the teacher quote of deck 4.
NEXT: Week 3, Part 3 = frontiers (15 min: deck 6 framework + VR robotics study 7.12-7.14 + GenAI and LA) and assignment workshop 2 (30 min: extraction and synthesis,
       PRISMA numbers, common mistakes). Sources are in sources_w3p3/ and img_w3p3/; the systematic-review revision deck was audited in the W3.P1 board (OLD list).
       Still to verify online: the paper behind the deck 6 framework; the publication behind the VR robotics study; GenAI + LA literature (2023 or later).
       When Part 3 is done: ONE download LA_Week3_package.zip organised like LA_Week2_package, plus the two-page revision sheet from the nine "Να θυμάστε" slides.

==================== v8c (Week 3, Part 3: audit and outline ONLY; nothing is built yet) ====================
Status: review board and 25-slide outline sent; WAITING FOR THE LECTURER'S APPROVAL and for his answer on the VR robotics publication.
  audit/outline_w3p3.py, audit/build_board_w3p3.py -> out/W3P3_review_board.html and content/w3p3_outline.md
  An interim download was given at his request: LA_Week3_package_PARTS_1_and_2.zip, laid out exactly like LA_Week2_package
  (00_READ_ME_FIRST.txt, 1_Teach_from_these, 2_Give_to_students/A_before_the_evening, B_after_the_evening, C_optional_Lab2_notebook,
  3_Teacher_only, 4_Build_kit, 5_Planning_documents; student PDFs are named W3P1_student.pdf, W3P2_student.pdf). The FINAL package keeps this layout.
Design: frontiers 15' (slides 1-12: his framework 6.4-6.10, the VR robotics study 7.12-7.14, GenAI through the LA cycle) + workshop 2 30' (briefing 5',
  rooms 12' timer, two teams 02:30 each, debrief, checklist, until submission, remember, end slide with 3' slack). Skippable 6 and 21.
  Workbook: students have v2 (sheets Οδηγίες, 0_Συμβολοσειρά, 1_Αναζήτηση, 2_Επιλογή, PRISMA_αριθμοί, 3_Εξαγωγή, 4_Ποιότητα); Part 3 adds 5_Σύνθεση -> v3
  (workbook/make_wb_v2.py is the generator to extend). Handout and teacher sheet: reuse workshop1/build_handout.py.
  The three study cards of the handout = Borrella et al. (2022), Baneres et al. (2023), Hellings & Haelermans (2022), in own words, with DOIs.
Verified: framework paper = Christopoulos, Pellas & Laakso (2020), Education Sciences 10(11), 317 (abstract; "four-dimensional", deck says 3 data dimensions:
  three feed the fourth). Candidate for the VR robotics slides = Antonelli, Christopoulos, Laakso et al. (2023), Education Sciences 13(5), 528 (JANUS, ViLLE):
  NOT confirmed that the findings of 7.14 are in it; default: cite it for the laboratory, and for the findings only if found in its full text, otherwise
  "unpublished results of the lecturer". GenAI: Yan, Martinez-Maldonado & Gasevic (2024), LAK '24, 101-111 (abstract opening read); others at build.
  Not in the Week 1 brief, so left out of the checklist unless he says otherwise: "Cohen's kappa >= 0.80", "Abstract 150-250 words".
At the end of Part 3: the two-page revision sheet from the nine "Να θυμάστε" slides, then LA_Week3_package.zip (complete) and tell him plainly the week is done.

==================== v9 (Week 3, Part 3: BUILT, checked and delivered. WEEK 3 IS COMPLETE. THE REMASTER IS COMPLETE.) ====================
Deck:  content/w3p3.json is GENERATED by w3p3/make_deck_json.py; images in img_w3p3/ (d6_s10_white.png = the lecturer's architecture figure flattened on white,
       because the original PNG is transparent; d7_s12_1.jpg = his simulator screenshot; the engine does not know the extension .jpeg).
       25 slides, 45 min: frontiers 15 (slides 1-12) + workshop 2 30 (13-25); timers on 18 (12:00) and 19 (02:30 per team); skippable 6 and 21; end slide carries 3' slack.
       NO engine change. Pitfall met: two underscores inside one text field turn the text between them italic (em()); keep at most one per field.
Documents: w3p3/build_workshop2.py -> out/Workshop2_handout.pdf (4 pp.), out/Workshop2_teacher.pdf (3 pp.), out/LA_revision_sheet.pdf (2 pp., the 27 points of the nine
       "Να θυμάστε" slides, read from the content JSONs). workbook/make_wb_v3.py -> out/LA_review_templates_v3.xlsx (new sheet 5_Σύνθεση; the rest as v2).
DEPARTURE FROM THE APPROVED OUTLINE, reported to the lecturer: slide 10 shows the PUBLISHED results of Antonelli et al. (2023), read in the full text
       (119 invited, 107, 102, VR assessments 25/16/13, 84, 82; no significant pre-post change, t(69) = 0.04, p = 0.96; alpha 0.63-0.89; VR assessment data not analysed).
       His old slides 7.13-7.14 (57/43/35 participants, "significant improvement", Wilcoxon/Friedman) describe other numbers that are NOT in that paper and were not used.
Sources opened for this part: Christopoulos, Pellas & Laakso (2020) full text; Antonelli et al. (2023) full text; Yan, Martinez-Maldonado & Gasevic (2024) abstract (arXiv);
       DOIs of the three handout studies at Crossref. NOT opened, therefore NOT on any slide: Yan, Greiff et al. (2024), Yan et al. (2025), SWiM (Campbell et al., 2020).
       Slide 12 is the lecturer's own synthesis and says so in its source line and notes.
Final package: LA_Week3_package.zip, same layout as LA_Week2_package.

==================== v10 (rework of 20 Sept 2026: no preparation, no homework, one page per lab, one breakout per evening) ====================
Plan and rules: the instructor's handover (_handover/00_HANDOVER_READ_FIRST.md of the course folder) — all decisions there are agreed; do not reopen them.
Decks (rebuilt, layout check 0 problems each; student PDFs via /home/claude/topdf_deck.py recipe = Playwright print media, prefer_css_page_size):
  W2P2  8 slides, 45': case 6' · rooms 2+18+2 (timer 18:00) · two rooms in full 3' each (03:00) · 5' spare. content/w2p2.json from lab1/make_deck_json.py, which
        now also writes content/lab1_reveal.json (old slides 8-18) for W2P3.
  W2P3 33 slides: Lab 1 reveal (11', from content/lab1_reveal.json) · dashboards 18' (unchanged slides) · search DEMONSTRATION by the lecturer 7' (slides 26-30,
        3' on the ERIC funnel) · guidance for their own review · Να θυμάστε · 7' questions. workshop1/make_deck_json.py. No breakout, no version numbers.
  W3P2 12 slides: case 6' · rooms 2+15+2 (15:00) · two rooms in full (02:30) · reveal 7' (subgroups, weights and the message as «πέρα από το φύλλο») · 3' spare.
        w3p2/make_deck_json.py also writes content/lab2_ethics.json (old slides 12-22) for W3P3.
  W3P3 27 slides: ethics block 13' (from lab2_ethics.json; question 4 no longer says «Το μήνυμα που γράψατε») · new directions 8 slides 8' (cut: data-collection table,
        levels of analysis, architecture figure, «Τι συλλέχθηκε») · worked example 5 slides 5' · «Ερωτήσεις για την εργασία σας» 15:00 timer · Να θυμάστε · 3' spare.
  W1P3, W2P1, W3P1: only the lines that promised room work or homework were changed (W1P3 slides 4, 5, 30, 32; W2P1 slide 2; W3P1 slides 2, 22, 26, 32 + notes).
Student sheets (one A4 page each, pack CSS): handouts/build_sheets.py -> out/Lab1_sheet, Lab2_sheet (ported from handouts/Lab*_one_page.html, numbers untouched),
  Search_sheet (ERIC counts from workshop1/eric_counts.json), Submission_checklist. Revision sheet: handouts/build_revision.py (lab «Να θυμάστε» credited to Part 2).
Teacher sheets (two pages each): handouts/build_teacher.py -> out/Lab1_key, Lab2_key, Search_demo_teacher, Example_QA_teacher (numbers from exhibits.json,
  numbers.json, eric_counts.json). Superseded: lab1/build_pack.py, lab1/build_key.py, lab2/build_pack.py, lab2/build_key.py, workshop1/build_handout.py, w3p3/build_workshop2.py.
Spreadsheet: workbook/make_wb_v3.py -> out/LA_review_templates.xlsx (v3 content, no version wording, marked optional); lives only in Assignment/Review_Log_Template.
PDF of sheets: python3 lab1/topdf.py <html> <pdf> (must print "pages overflowing: none").
Course-folder layout after v10: Week2/2_Give_to_students = Lab1_sheet.pdf, Search_sheet.pdf; Week3/2_Give_to_students = Lab2_sheet.pdf, Submission_checklist.pdf,
  LA_revision_sheet.pdf; 3_Teacher_only = Lab1_key.pdf + Search_demo_teacher.pdf, Lab2_key.pdf + Example_QA_teacher.pdf (+ the untouched lab files and notebooks).
  Backup of the pre-rework Week2 and Week3: builds/week 3 - build/backup_before_rework_2026-09-20.zip.
v10.1 (same day): «κοόρτη» replaced everywhere by natural Greek (περσινοί / φετινοί φοιτητές, σειρά φοιτητών) in W2P1, W2P2, W2P3, W3P1, the Lab 1 sheet, the keys and the
  revision sheet; Lab 1 sheet sentence on the six rules reworded; «Πότε είναι διαθέσιμος»; the rule names in the Lab 1 key are now HTML-escaped («< 0,35» had vanished).
  Course-folder zips must be written with UTF-8 file names (Python zipfile), or the Greek folder names in Assignment/ appear garbled on Windows.
v10.2 (proofreading pass, same day): full read of all nine decks and all nine sheets. Fixes: «κοόρτη» removed everywhere (v10.1); Lab 1 sheet sentence on the six rules;
  «Πότε είναι διαθέσιμος»; W2P2 «τα δεδομένα των περσινών φοιτητών»; W2P3 «τα φετινά δεδομένα παράγονται…», «Συνδέσεις ανά κατάσταση εγγραφής», «Η κατάσταση εγγραφής
  είναι ο συγχυτικός παράγοντας»; src lines now read «312 περσινοί φοιτητές» / «298 φετινοί φοιτητές»; Lab 1 key rule names HTML-escaped. Content corrections against the
  official assignment brief (Assignment/…): W1P3 slide 1 now says «Ατομικά ή σε ομάδες των δύο ατόμων» (the brief allows individual work) and «4.000 έως 6.000 λέξεις»
  (the «μέγιστο 7.000, χωρίς εξώφυλλο…» of the old slide is not in the brief); W1P3 slides 3, 12 and 30 no longer presuppose a pair. Example_QA_teacher answers aligned
  with the brief (language, pairs, topic declaration) and reworded («Είτε είτε», «από το βήμα»). Still deliberately unchanged: the two-reviewer wording of W1P3 slides
  16, 17 and of the workbook's 2_Επιλογή sheet (PRISMA good practice, not a course requirement) — mentioned to the instructor.

==================== v11 (21 Sept 2026: no clock times, one teacher file per lab, assignment material handed out in Week 1) ====================
1. Clock times removed from the deck: build_html2.js `plan()` no longer renders the ptime column and deck2.css `.plan li` is a two-column grid. The «Το πλάνο της βραδιάς»
   slides now read «Μέρος 1 / 2 / 3» only. meta.start is still used by nothing visible; ?start= has no effect on the plan slide any more.
   Also fixed: deck2.css `.sq` (week-2 code squares) was overriding `.step .sq` and clipping the Week 1 «Τύποι αναλυτικής» stairs slides; `.step .sq` now resets
   display/size/background. W1P1 rebuilds identically to the delivered file apart from its plan slide. W1P2 cannot be rebuilt here (its ViLLE screenshots live outside
   the kit, /home/claude/src/ville) and was not touched: it has no plan slide.
2. Teacher material: ONE file per lab. handouts/build_teacher.py -> out/Lab1_answers.html and out/Lab2_answers.html (two A4 pages each). Page 1 = the answers that hold
   and the numbers table; page 2 = the run of the evening (relative minutes, no clock), the reveal, and — folded in from the deleted files — the ERIC demonstration script
   (Week 2) and the fifteen minutes of questions on the assignment (Week 3). Deleted: Lab1_key, Lab2_key, Search_demo_teacher, Example_QA_teacher.
   The optional Colab notebooks, the CSV data and simulate.py are no longer in the course folder: they live in this kit (lab1/, lab2/) and in the pre-rework backup zip.
3. Student lab sheets carry their own timing now («18 λεπτά στην αίθουσα… 3 λεπτά ανά ομάδα»), so the sheet alone tells a room what to do.
4. Assignment material is handed out in Week 1: Search_sheet.pdf and Submission_checklist.pdf sit in Assignment/ next to the brief, the PRISMA files, the sample reviews
   and the optional workbook. W1P3 slide 28 («Εργαλεία») lists all of it and says it is posted that evening; W2P3 and W3P3 now refer back to it instead of handing it out.
   Week2/2_Give_to_students = Lab1_sheet.pdf · Week3/2_Give_to_students = Lab2_sheet.pdf + LA_revision_sheet.pdf.
v11.1: HEAL-Link is now explained wherever it appears («μέσω HEAL-Link, του συνδέσμου των ελληνικών ακαδημαϊκών βιβλιοθηκών: ιδρυματικός λογαριασμός, από το δίκτυο του
  ιδρύματος ή με VPN»), with the ERIC fallback stated next to it (search sheet, W1P3 slide 13, W2P3 note, Lab2_answers). The two assignment sheets no longer carry a week
  and part label, since they are handed out in Week 1: their kicker is «Εργασία 3 · Υλικό υποστήριξης · …» and the calibration heading of the search sheet reads
  «το παράδειγμα του μαθήματος» instead of «το ερώτημα της Εβδομάδας 1».
v11.2: (a) Mouse-wheel navigation added to deck.client.js — one notch, one slide, 400 ms lock, and it stays out of the way of anything that scrolls (the help overlay,
  the presenter window). The Week 1 Part 2 deck cannot be rebuilt here (its ViLLE screenshots live outside the kit), so the same behaviour was injected into the delivered
  file as a small script before </body>; rebuild it from the original sources when those are at hand and the engine version takes over. (b) Bar labels may now contain \n
  and are rendered with <br>. (c) US racial categories are named by origin: «Αφροαμερικανοί φοιτητές», «Λατινοαμερικανοί φοιτητές», «λευκοί φοιτητές», «φοιτητές ασιατικής
  καταγωγής», and «φυλή» became «φυλετική καταγωγή» (W1P1 slides 26 and 29, W3P1 slides 18, 21 and their notes). «Έγχρωμοι» was not used: it is a dated euphemism.
  (d) Self-describing labels («…, μία σελίδα», «PDF, μία σελίδα») removed from sheets, footers, slides and notes.
v11.3: flow audit of every forward/backward reference on all nine decks after the rework. Fixed: W1P1 slide 32 now answers its own question in one line and says why the
  same question returns in Week 3 (it used to defer with no answer); W1P1 slide 33 (roadmap) carried the pre-rework structure and now matches the three evenings exactly,
  with the assignment given in full on night 1; W2P2 break line said «αναζήτηση βιβλιογραφίας για την εργασία σας» and now says «επίδειξη αναζήτησης». Everything else
  checked out: every «Εβδομάδα/Μέρος», «απόψε», «ακολουθεί», «θα δείτε» on a slide or in a note points at what actually happens there now.

v11.4 (21 Sept 2026, second flow audit: all nine decks read end to end as one sequence, plus the four student sheets and the two answers sheets)
  CORRECTION of v11 point 1 and v11.2 (a): W1P2 CAN be rebuilt here. Its ten ViLLE pictures are in img_w1p2/ and content/w1p2.json now says meta.imgDir = "img_w1p2".
  The rebuilt file has all 34 slides byte-identical to the delivered one (checked slide by slide, pictures included, and pixel by pixel); it simply carries the current
  engine, so the wheel-navigation script that had been injected by hand is no longer needed. Build: node build_html2.js content/w1p2.json out/W1P2.html
  ENGINE: poll() printed the literal word "undefined" when a poll had no context line. W1P2 slide 16 showed it, on screen and in the student PDF. The context
  paragraph is now rendered only when the field exists; every other deck rebuilds byte-identical slides.
  GENERATOR BUG: lab1/make_deck_json.py ran .replace('.', ',') over whole sentences to get decimal commas, which turned the full stops of two reveal notes into commas
  (W2P3 slides 4 and 6). Use g2() for ONE number; never replace over a sentence.
  NEW: topdf_deck.py = the student-PDF recipe as a script (python3 topdf_deck.py /abs/out/W3P1.html /abs/out/W3P1_student.pdf). It reproduces the delivered PDFs byte for byte
  in size. Regenerate a student PDF only when a SLIDE changed: notes are not printed, so a notes-only change leaves the PDF as it is.
  Slides that changed (4): W1P2 16 («undefined» gone) · W1P3 3 (title «Τρεις ανασκοπήσεις· δύο τις συναντήσατε απόψε»: Viberg et al. 2018 is not shown in Parts 1-2 since
  Part 1 v2) · W3P1 26 (last sentence «Οι ίδιοι κανόνες επανέρχονται στο Εργαστήριο 2»: Lab 2 shows the rules of the message in its model answer, not a message) ·
  W3P3 23 (title «Τρεις μελέτες του Μέρους 1 σε μία πρόταση»: the study cards of the old workshop are gone, the three studies are those of W3P1 slides 25 and 29).
  Speaker notes that still described the pre-rework course, now fixed: W1P1 23 (where the self-selection error returns: slide 28), 35 (no «οδηγός μελέτης» exists; the
  break slide shows a countdown, not a clock time) · W1P2 21 (the advice to shorten the ViLLE section moved here from the break slide, where it came too late), 30, 31
  (the rooms work on ready analyses, not on files), 34 · W1P3 3, 14 (no room writes a search string in Week 2: the lecturer demonstrates), 24 (no document template exists
  among the assignment files) · W2P1 24 (the Lab 1 sheet has no transition matrices, only P(E→S)) · W2P2 1 (the sheet is handed out at that moment, as in W3P2) ·
  W3P1 4, 18 (the subgroup check is shown by the lecturer, beyond the sheet) · W3P2 3 (the rule comes from slide 11 of Part 1, not from its first «Να θυμάστε»),
  4 (the Colab notebook lives in this kit, not in a teacher folder) · W3P3 1 (the block now OPENS Part 3: one opening sentence; the rooms never had the data file),
  5, 11 (no break follows this «Να θυμάστε» any more), 23. The generator of w3p3.json asserts 2 to 3 notes per slide: keep to that.
  Sheets: Search_sheet said «οι τρεις παγίδες παρακάτω» in a line that sits at the bottom of the page («παραπάνω»). Lab1_answers: the four search-string errors moved from
  page 1 (under the Lab 1 rules table) to the search demonstration on page 2. Lab2_answers: page 1 = the answers, the threshold table with the two data caveats, and what the
  lecturer adds in the reveal; page 2 = Part 2 minute by minute, then Part 3 (the questions table and «Αν δεν ρωτά κανείς…») in one place; «ο πίνακας της σελίδας 1» is true
  again; page 2 title shortened to fit one line. Lab1_sheet, Lab2_sheet, Submission_checklist and LA_revision_sheet were read and rebuild byte-identical: untouched.
  Checked and left alone: every numeric slide reference in the notes points at the right slide; every part totals 45 minutes; every timer equals its label.
  NOT in this kit and therefore not touched: the assignment brief (Assignment/Εργασία 3 LA 2026-27.pdf has no source here). It still calls the two assignment sheets
  «τα φυλλάδια των εργαστηρίων»; they are now «φύλλο αναζήτησης» and «λίστα ελέγχου έως την υποβολή».

==================== v12 (23 Sept 2026: NoSQL / MongoDB, Evening 1 BUILT and delivered; Evening 2 next) ====================
The lecturer now also teaches the NoSQL part of the course: 2 evenings, same 3 x 45' rhythm, after his colleague's 3 SQL evenings and before the 3 LA weeks.
Source material from the colleague (Dr I. Kazanidis) is in sources_nosql/: NoSQL_Part_A_2024.pdf (51 slides), NoSQL_Part_B_2025.pdf (40 slides), books.json (431 books),
  persons.txt (persons collection for the aggregation example), Ergasia2_brief_original.docx (Εργασία 2 = MongoDB assignment, 12 numbered sections) and
  Ergasia2_brief_corrected.txt (language fixes only, requirements unchanged; to be handed over in the Evening 2 package).
Evening 1 = N1P1 "Γιατί NoSQL" (32 slides) · N1P2 "Τέσσερα μοντέλα δεδομένων" (30) · N1P3 "Πρώτα βήματα στη MongoDB" (33). Each 45' = 42 + 3 slack; one poll per part
  (N1P1 s23 60 s, N1P2 s27 90 s, N1P3 s27 60 s); skippable N1P1 20+29, N1P2 5+24, N1P3 9+31. N1P3 ends on an endslide carrying the 3' slack (no break).
  Generators: nosql/make_n1p1.py, make_n1p2.py, make_n1p3.py -> content/n1p1..3.json ; node build_html2.js content/n1pN.json out/N1PN.html
  Image: img_n1p2/forum_graph.png from nosql/make_graph_img.py (invented forum reply network, labelled as such on the slide).
  Demo file for the lecturer: nosql/NoSQL_Evening1_demo.js (copy-paste order of N1P3). Student PDFs: topdf_deck.py.
ENGINE (pure append; all nine LA decks rebuilt and their slide HTML compared: identical): new slide type
  shell   cmd, out, cmdLabel ('Εντολή'), outLabel ('Αποτέλεσμα'), points[], foot  -> command pane (dark) above output pane (light), points on the right. Class prefix shl.
  Code panes use white-space:pre with overflow hidden, so shot2.py does NOT see clipped code: also run a pre-overflow check (scrollWidth > clientWidth on every <pre>).
REAL OUTPUTS: every mongosh output on the N1P3 slides comes from a real run: MongoDB Community 8.0.32 (fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu2404-8.0.32.tgz,
  run mongod --dbpath <dir> --fork --logpath <dir>/mongod.log) and mongosh 2.12.0 (npm install -g mongosh); script nosql/E1_demo.js, transcript nosql/E1_demo_output.txt.
  Pipe a script into mongosh (mongosh --quiet < script.js) to get the interactive display with prompts. mongod may stop between tool calls: restart with --fork.
  Verified in that run: 42 is stored as Int32, 8.5 and 3000000000 as Double; count() and insert() print DeprecationWarning; a field name "capital.name" on insert creates a
  literal top-level field and find({"capital.name": ...}) does not match it; duplicate _id gives E11000; createCollection returns { ok: 1 }; getTimestamp() works.
DATA used in N1P3 (collection world.country): Greece {euSince 1981, population 10400000}, Cyprus {_id 2, population 980000}, France/Germany {euSince 1958, populations
  68600000 / 83600000, capital {name, timezone IANA}}. Populations = Eurostat 1 Jan 2025, rounded. The colleague's yearOfIndipendence (misspelt; France 1688) is gone.
CORRECTIONS of the colleague's slides (reported to the lecturer): NoSQL "cannot guarantee reliable transactions" (MongoDB: multi-document ACID since 4.0 in 2018, sharded 4.2);
  failover belongs to replication, not sharding; key-value = unique key + value; wide-column is row-oriented (columnar is another thing); outdated system lists;
  mongo shell -> mongosh (legacy shell gone since 6.0); count()/insert() deprecated; "use" does not create the database (first insert does); "capital.name" as key;
  map-reduce slide cut; install screenshots of 5.0 replaced by five text steps; third-party figures (educba, A5, A24) redrawn natively.
Sources opened for Evening 1: MongoDB Manual (Transactions, Write Concern, Schema Validation, Install on Windows), DB-Engines ranking Sep 2026 and Redgate H1-2026 climbers,
  Khan et al. (2023) BDCC 7(2) 97, Brewer (2000/2012), Gilbert & Lynch (2002), Abadi (2012), Pritchett (2008), Bailis & Ghodsi (2013), Chang et al. (2006),
  DeCandia et al. (2007), NoSQL history (Strozzi 1998, meetup 11 June 2009), Moodle MDL-62907 (other field JSON since 3.7), Learning Locker architecture (Mongo + Redis),
  ISO/IEC 39075:2024 GQL, Eurostat population 1 Jan 2025. NOT used because not verifiable at source: Stack Overflow 2025 database percentages.
NEXT = NoSQL Evening 2 (approved in the Evening 1 outline, details to be outlined part by part):
  Part 1: queries on books.json (mongoimport; projection; comparison and logical operators; arrays incl. $elemMatch; regex; dot notation; sort/limit/skip; countDocuments;
          printjson and variables, both required by Εργασία 2).
  Part 2: group exercise in Zoom breakout rooms, one team of about 4 per room, every room the same page and questions, in the browser (Mongo Playground: verify at build
          that a books subset can be loaded there), no install, no preparation. ONE student sheet + ONE answers file.
  Part 3: update ($set, $unset, $inc, $push, upsert), deleteMany, aggregation pipeline ($match, $group, $sort, $limit, $project, $unset, $unwind) on persons and books,
          SQL<->MongoDB comparison, Εργασία 2 sections 4-11 mapped to slides, questions.
  Colleague's exercise solutions to correct: "Piter" in the task vs "^Peter" in the solution; db.books.count() in his optional exercises.
  Final: NoSQL_Evening2_package (decks, student PDFs, books.json, persons.txt, exercise sheet, answers file, Ergasia2_brief_corrected.txt) and tell him the NoSQL part is done.
v12.1 (same day): one-page teacher guide for the demo file: nosql/make_demo_guide.py -> out/NoSQL_Evening1_demo_instructions.html, PDF with lab1/topdf.py
  ("pages overflowing: none"). It sits next to NoSQL_Evening1_demo.js in 3_Teacher_only of NoSQL_Evening1_package (what the file is, installing MongoDB and mongosh
  once, opening the .js with Notepad and never by double-click, the order of use during Part 3, four common errors and their fixes).
v12.2 (same day): NO LIVE DEMO. The lecturer teaches N1P3 from the slides (15-28 show every command with its real output). Decided with him: keep the colleague's line on
  activities. The colleague's NoSQL 1 (Part A) had no demo file and no group work: its only activity was three "Hands On" slides (A44 db/use/db.country, A46 insertOne Greece,
  A47 insertOne Cyprus _id 2), after his install slides A38-42. N1P3 slides 15, 17, 18 now carry the green kicker «Δοκιμάστε» (same commands, same activity: whoever has MongoDB
  installed tries them). Wording that promised a live demo was removed (N1P2 break slide, N1P3 slide 1 and notes of N1P1 1, N1P3 1, 8, 21, 27). NoSQL_Evening1_package no
  longer has 3_Teacher_only; the demo file and its guide stay in nosql/ only. His NoSQL 2 (Part B) activities, to be kept in Evening 2: Άσκηση 1 and 2 with solutions
  (B31-34), the group task on the SQL-comparison page with plenary presentation (B35), optional exercises (B36-39).
v12.3 (same day): STUDENTS INSTALL MONGODB IN CLASS (the colleague's line: his install slides A38-42 came before his Hands On slides, and Εργασία 2 needs a real MongoDB).
  N1P2 break slide: students start both downloads (server msi + mongosh msi) before the break. N1P3 rebuilt, 27 slides, 45' (42 + 3 on the end slide):
  2 «Εγκατάσταση: τι χρειάζεστε» (1') · 3 «Εγκατάσταση τώρα» work slide with timer 08:00 (8') · concepts 4-11 · «Δοκιμάστε» 12 (2'), 13 (3'), 14 (2') · commands 15-23 ·
  poll 23 (60 s) · answer 24 · Εργασία 2 map 25 · remember 26 · end slide 27 (4' incl. slack). Skippable: 7 (JSON) and 16 (embedded document).
  Cut from N1P3: BSON slide (merged into the types table), dynamic-schema, 16 MB (now a line on «Ενσωμάτωση ή αναφορά»), tools, mongosh-vs-mongo (now the foot of slide 2),
  «use creates the database» (now a point and a note on the navigation slide), home-work slide, home install slide.
  EVENING 2 CONSEQUENCE: the exercises run in the students' own mongosh (installed in Evening 1), not in a browser playground; Database Tools (mongoimport) are installed
  in class at the start of Evening 2, as in the colleague's Part B slides 27-28.

==================== v13 (23 Sept 2026: NoSQL Evening 2, Part 1 BUILT and checked; Parts 2 and 3 next) ====================
Principle set by the lecturer: follow the colleague's approach; only make the content current, accurate and deliverable in the style of the course.
  Part 1 follows the order of his Part B: find + projection, printjson, variables, comparison, logical, limit + sort; his Database Tools install, mongoimport of
  books.json, Άσκηση 1 and Άσκηση 2 each followed by its solution. His group task on the SQL-comparison page (B35) and his optional exercises (B36-39) are kept
  for Part 2, so Part 1 avoids their queries (Java category, more than 500 pages, the five longest books, Java in the title, 2nd and 4th letter).
  Changes from outline v1: printjson and variables moved after projection; $all/$size replaced by $elemMatch; poll on Internet (41 / 21). content/n2p1_outline.md = v2.
Pipeline (nothing typed by hand): nosql/e2p1_cmds.py (every statement, as displayed) -> nosql/run_e2p1.py (mongod 8.0.32 + mongosh 2.12.0 + Database Tools 100.19.0
  on PATH; writes nosql/e2p1_outputs.json and nosql/E2P1_output.txt) -> nosql/make_n2p1.py -> content/n2p1.json -> node build_html2.js content/n2p1.json out/N2P1.html
  Checks: python3 shot2.py /abs/out/N2P1.html out/s_ "" (problems: 0) · python3 nosql/check_pre.py /abs/out/N2P1.html (clipped code: none) ·
  python3 topdf_deck.py /abs/out/N2P1.html /abs/out/N2P1_student.pdf (33 pages). Timers 4 (06:00), 15 and 27 (03:00), poll 21 (60 s) tested: count down, T pauses;
  break countdown starts by itself; speaker window opens with N and follows. Skippable 6 and 30. Deck: 33 slides, 45'.
ENGINE (opt-in flags; all twelve earlier decks rebuilt, slide HTML identical): shell dense (20px code, 430px points) · shell stack (wide panes, points in three
  columns underneath) · htable compact · work items may be {t, code} (code line under the item, class n2code) · poll code (code block under the context, class n2pq).
  Trap met: class .wkc already exists (Week 2 anatomy slide); check every new class name with grep before use.
Verified at source (MongoDB docs fetched as markdown: curl https://www.mongodb.com/docs/<page>.md): Database Tools installation (Windows msi, PATH steps; Homebrew
  install includes the tools) and release notes (100.0.0 = first separate release, 2020; 100.19.0 released 22 Sept 2026); mongoimport (system command line, --drop,
  --jsonArray, continues on duplicate keys); Query an Array (exact match incl. order, $all, $elemMatch with $regex + $ne, index dot notation); $elemMatch single
  condition; projection (no mixing except _id); comparison and logical operator pages ($ne, $nin, $not also match missing fields); $regex; cursor.sort/limit/skip;
  Comparison/Sort Order (missing = null); count() deprecated; mongosh print/printjson = console.log; EJSON.stringify; SQL mapping chart (LIKE <-> regex; the chart
  still shows count(): Part 2 must tell students to use countDocuments). books.json = ozlerhakan/mongodb-json-files datasets/books.json, CC0, same 431 documents
  (the course copy has CRLF line endings). MEAP = Manning Early Access Program (manning.com). Greek Windows labels from iGuRu.gr.
Corrections of the colleague's Part B: Άσκηση 2 task said «Piter» (0 books), solution searched ^Peter (13); Άσκηση 1 answer (12) is right but misses
  «WebWork in Action» (category «internet»); count(), insert() deprecated; his printjson screenshot showed _id: {}.
v13.1 (same day): Part 2 BUILT and checked (outline approved: "OK").
  Deck: 12 slides, 45': aim (his B35) 1 · the manual's SQL-to-MongoDB page (its own people examples; count() -> countDocuments()) 2 · how we work 1 ·
  worked example with SQL pane 2 · rooms 22 (timer 20:00) · two teams 6 (03:00 each: items 4-8 and 9-13) · solutions where mistakes happen 4 x 2
  (Java 96/76/97, AND 95 / OR 364, binary sort and collation, /Java/ 38 vs \bJava\b 29) · remember 1 · break 2. Skippable 9 and 10. No poll (lab part).
  Sheet (one A4 page): his 13 optional exercises B36-39 with updated wording, each with its SQL (a books table with one category per book), blank
  columns for the MongoDB query and the count, timing and roles on the sheet itself. Answers (two A4 pages): every solution with its real result and
  the trap it hides; Part 2 minute by minute; what to do if a room is stuck; what changed from the old material.
  Pipeline: nosql/e2p2_cmds.py -> run_e2p2.py -> e2p2_outputs.json, E2P2_output.txt -> make_n2p2.py -> content/n2p2.json -> out/N2P2.html;
  build_n2p2_docs.py -> out/N2P2_sheet.html, out/N2P2_answers.html; PDFs with lab1/topdf.py ("pages overflowing: none") and topdf_deck.py.
  ENGINE (opt-in): shell sql pane (class n2sql). Earlier decks re-checked: slide HTML identical.
  Corrections of B36-39: count() -> countDocuments(); items 4 and 5 used typographic quotes (SyntaxError: Unexpected character '“'. (1:27)) and
  item 4 lacked its closing quote; «φθίνουσα σειρά βιβλίων» -> «σελίδων»; wording «έχουν έχουν», «έχουν ξεκινούν»; docs.mongodb.com -> mongodb.com/docs.
v13.2 (same day): Part 3 BUILT and checked (outline approved: "ok"). THE NoSQL PART IS COMPLETE.
  Deck: 32 slides, 45': update and delete 16 (updateOne/$set, matched vs modified, $inc/$push, $unset, operator table, updateOne vs updateMany, updateMany
  on the 166 zero-page books, upsert of Cyprus, poll 10 (60 s: updateOne without an operator -> MongoInvalidArgumentError), answer, count before deleting
  (skippable 12), deleteMany) · aggregation 19 ($group total population 162.600.000, per status, $match + $avg/$max, $unwind top 5, HAVING, $project +
  $round, persons.txt, his pipeline, $unset = $project with 0, the same with find (skippable 24), §10 needs grouping, persons per vocation) · SQL side by
  side (commands, aggregation) · Εργασία 2 map (slide numbers read from n1p3.json and n2p1.json) · what to submit · remember · end slide «Ερωτήσεις» 5'.
  Pipeline: nosql/e2p3_cmds.py -> run_e2p3.py (sets the starting state: fresh books import, Evening 1's world.country, persons pasted) ->
  e2p3_outputs.json, E2P3_output.txt -> make_n2p3.py -> content/n2p3.json -> out/N2P3.html. The three persons variants ($unset, $project, find) are
  asserted identical. ENGINE (opt-in): shell side=true (command and output side by side, class n2side). N2P1 and N2P2 rebuild identical.
  persons.txt: pasting (the colleague's method) worked; load() of his file left mongosh in a database named «book-filtered-top-subset;» without the
  persons, and load() of «use …» without semicolon fails. sources_nosql/persons_corrected.txt starts with db = db.getSiblingDB("book-filtered-top-subset");
  and works both ways; it is persons.txt in the package.
  Εργασία 2 brief: nosql/make_brief.js (+ blocks.json) -> out/Ergasia2_MongoDB.docx, a clean Word copy of sources_nosql/Ergasia2_brief_corrected.txt
  (the original .docx is a Moodle page copy with UI links and a 2025 due date; both left out; no date: the platform holds the deadline). Validated, 1 page.
  Package: NoSQL_Evening2_package.zip = 00_READ_ME_FIRST.txt · 1_Teach_from_these (N2P1-3.html) · 2_Give_to_students (three student PDFs, N2P2_exercise_sheet.pdf,
  books.json, persons.txt, Ergasia2_MongoDB.docx) · 3_Teacher_only (N2P2_answers.pdf).
v13.3 (same day, lecturer's feedback on N2P1 slide 3: "odd / GenAI style"; "we want them to download stuff: give direct links"; "who cares" about
  facts such as "separate from the server since 2020, own numbering 100.x"). RULE FOR ALL FUTURE WORK: anything students must open or download gets a
  direct clickable link on the slide (and in the PDF); no background facts that do not help students do or understand the task; plain, natural wording.
  ENGINE: em() understands [label](https://…) -> <a class="n2a" target=_blank>; links open in a new tab, do not move the deck, and stay clickable in the
  student PDFs (pdfinfo -url lists them). No earlier deck contains the pattern; their slide HTML is unchanged (checked).
  N2P1: slide 3 rewritten (links: Database Tools download page, books.json raw file on GitHub, installation page; no history or version facts);
  slide 8 MEAP in plain words; slide 11 EJSON moved to the notes; slide 31 null-sorting fact moved to the notes. N2P2: the SQL-to-MongoDB page is a link
  on slides 2 and 5 and on the sheet. N2P3: slide 1 «Τι περιέχει το Μέρος 3»; slide 11 plain warning on the old update(); slide 24 trivia to the notes.
  Package and kit rebuilt.
v13.4 (same day, second example from the lecturer: «Οι λύσεις του φύλλου, με την πραγματική έξοδο» — the qualifier is unnecessary). Wording pass over all three
  decks, the sheet, the answers file and the notes: no process claims ("real output", "real run", "checked", versions of the run) in any text the lecturer
  or the students read; labels «Αποτελέσματα, με τη σειρά» -> «Αποτελέσματα»; restated brief requirements and repeated lines cut (N2P1 slides 3, 4, 5, 6, 9,
  11, 28, 29; N2P2 slide 2; N2P3 slides 21, 23, 30); answers file: title «Οι λύσεις του φύλλου», intro paragraph and run details removed. Process facts
  stay only here and in the nosql/ scripts. RULE: write only what the reader needs, in plain words; no qualifiers that vouch for the material.
v13.5 (lecturer's comments on the exercise sheet ONLY, "this concerns only this file, explicitly"): the instructions of N2P2_sheet rewritten in plain
  full sentences; presentation rule changed from "two teams, items 4-8 and 9-13" to "every team in turn presents one item, 1, 2, 3 ... until all 13 are
  presented" (works for any number of teams, covers 1-3); the help note reworded. NOT changed, by instruction: N2P2 slide 6 and the answers file still
  carry the old two-team rule; align them only if the lecturer asks.
v13.6 (same day): the kit moves to a git repository for Claude Code. Repository layout: CLAUDE.md (rules, build, checks, notes rules, how to work with the
  lecturer), FIRST_TASK.md (steps and the first message), setup.sh (Playwright Chromium, poppler-utils, Pillow, docx), .gitignore, and this kit as build_kit/.
  Next task: speaker notes, deck by deck (N2P1, N2P2, N2P3, then W1P1 to W3P3), pilot first on N2P1 slides 5, 7 and 8.

==================== v14 (23 Sept 2026: speaker notes, PILOT on N2P1 slides 5, 7 and 8; waiting for the lecturer's OK) ====================
Pipeline proved in the repository: N2P1-3 JSON (make_n2p*.py) and HTML rebuild byte-identical to the delivered files; shot2.py problems 0, check_pre.py clipped code
  none, topdf_deck.py 33 / 12 / 32 pages with the same links; N2P2 sheet and answers "pages overflowing: none".
ENGINE (opt-in, meta.notesMarkup = true): in the speaker notes **item** -> bold and `code` -> code. build_html2.js writes notesHtml next to notes, deck.client.js
  shows it when present; decks without the flag get byte-identical DECK data and the old plain-text path. All fifteen decks rebuilt: slide HTML identical.
  The optional spotlight (click a note, light up its item on the slide) is not built.
N2P1: meta.notesMarkup = true; notes of slides 5, 7, 8 rewritten by the notes rules of CLAUDE.md (item in bold, top to bottom, 4 notes each, one «Αν ρωτήσουν»
  on slide 7). Every number in them comes from e2p1_outputs.json; new slide reference [[s_install]]. make_n2p1.py now asserts 2 to 4 notes per slide.
  Student PDF not regenerated: notes are not printed. Left out of the notes (not on the slide): slide 5, Extended JSON and --jsonArray; slide 7, why _id 23 was
  chosen (the first book's long description does not fit); slide 8, that the solution of Άσκηση 1 misses the «internet» book (slide 16 shows it, and at slide 8
  it would give away the trap before the exercise). The _id types line of slide 7 is now its «Αν ρωτήσουν».
  CLAUDE.md updated to match: notes markup flag, review.py in the checks, README pointer to v14, setup.sh installs the font.
REVIEW IMAGES: review.py -> review/<deck>/…png, each slide next to its notes as the presenter window shows them, 4 slides per image; it also checks that the
  presenter shows every note of the deck ("notes shown: all"). Pilot: python3 review.py "$PWD/out/N2P1.html" ../review/N2P1/pilot.png 5,7,8
CLOUD ENVIRONMENT: the decks load Commissioner from Google Fonts, which headless Chromium cannot reach there; without it every check runs on a fallback font
  (Liberation Sans). setup.sh now installs Commissioner locally (static TTFs from the Google Fonts API in /usr/local/share/fonts, fc-cache) and pins the Python
  playwright to the version of the global npm playwright, whose Chromium the cloud image already has (1.56 -> chromium-1194): the old unpinned upgrade moved
  playwright past that Chromium and needed a browser download, which the cloud network refuses.

==================== v15 (24 Sept 2026: speaker notes for every deck by the CLAUDE.md notes rules, after the lecturer's OK of the pilot) ====================
Branches: one per deck, notes/<deck>; W2P2+W2P3 and W3P2+W3P3 share one, because lab1/make_deck_json.py and w3p2/make_deck_json.py also write the
  reveal (lab1_reveal.json) and ethics (lab2_ethics.json) slides of the next part. Evening 1 (N1P1-N1P3) is final and was not touched.
ENGINE (opt-in, same flag): decks with meta.notesMarkup also send titleHtml, so the presenter shows `code` in titles as code, not as backticks.
  Same flag: the T key also starts/pauses the timer when the notes window has the focus (before, only the slide window reacted to T).
ENGINE (opt-in per slide): 'ragged': True on a slide left-aligns its running text (class .ragged, deck2.css end). The house style stays justified
  (v3: "where lines are long enough"); the flag is for slides whose short lines open wide gaps. All 15 decks rebuild with identical slide HTML.
ENGINE (opt-in per slide): 'hLinks': True on a table slide renders its row names with em(), so a row name can be a [link](https://…).
COURSE FOLDERS: the lecture HTML files under «1. NoSQL/» and «2. Database Systems & Learning Analytics (2026)/» are byte-identical copies of
  build_kit/out/<DECK>.html (N2Pn -> 1. NoSQL/Week 2/1. Lecture/NoSQL_W2Pn.html; W1Pn -> Week1/1. Lecture/LA_W1_Partn.html; W2Pn, W3Pn ->
  Week2|Week3/1. Lecture/HTML/WnPn.html); student PDFs likewise. Every deck branch copies its rebuilt deck there, so the lecture files carry the notes.
setup.sh also installs pandas (lab1/ and workshop1/ generators).
check_notes.py: the notes rules checked on the built deck (2-4 notes, **item** found on the slide, one «Αν ρωτήσουν» at most, meta words, order).

N2P1:
  pending

N2P2:
  pending

N2P3:
  pending

W1P1:
  pending

W1P2:
  pending

W1P3:
  pending

W2P1:
  pending

W2P2:
  pending

W2P3:
  pending

W3P1:
  32 slides, 110 notes (2 to 4 per slide, six «Αν ρωτήσουν»), all other notes led by their on-slide item in bold; meta.notesMarkup on; Lab 1 numbers
  from the generator's variables. make_deck_json.py asserts 2 to 4 notes per slide (was 2 to 3) and computes the slide 29 reference [[s_uoc]] (= 25).
  Slides changed (approved): 16 foot «Στην προηγούμενη διαφάνεια παραβιάζονται…» -> «Στο Εργαστήριο 1 παραβιάζονται…»; 29 «(UOC, προηγούμενη διαφάνεια)» -> «(UOC, διαφάνεια 25)».
  Student PDF regenerated for the two slide changes (32 pages).
  Left out: the skip remarks (slides 14, 19, 32); why an older source (17); the journalistic-source remark (21); «rarely the teacher» (6); the Java effect per specialisation (29).

W3P2:
  pending

W3P3:
  pending

==================== Αλλαγές από το παλαιότερο υλικό (kept out of the speaker notes; notes rule 4) ====================
N2P1:
N2P1 slide 5: the older material also showed the reverse command, mongoexport (mongoexport --db=world --collection=country --out=country_export.json);
  not needed for Εργασία 2.
N2P1 slide 8: the older material used count(); it still works, with a DeprecationWarning. The deck uses countDocuments().

N2P2:
  none

N2P3:
  none

W1P1:
  none

W1P2:
  none

W1P3:
  none

W2P1:
  none

W2P2:
  none

W2P3:
  none

W3P1:
W3P1 slide 8: the statement is worded as it appears in exercise solutions and handbooks (it comes from the key of the older Week 3 practical, DS1).
W3P1 slide 24: the typology of interventions comes from the older material of the course (the LA revision deck) and remains useful.

W3P2:
  none

W3P3:
  none
