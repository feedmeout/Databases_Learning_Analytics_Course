LAB 2 (Week 3, Part 2): real data, UCI 697 (Realinho, Machado, Baptista & Martins, 2022, Data 7(11), 146), CC BY 4.0.
Pipeline (run inside lab2/; every number shown anywhere comes from numbers.json):
  python3 make_numbers.py        raw/data.csv -> numbers.json + data/students_dropout_uci697.csv + data/test_set_with_risk.csv
  python3 ../w3p2/make_deck_json.py ; (cd .. && node build_html2.js content/w3p2.json out/W3P2.html && python3 shot2.py /abs/out/W3P2.html out/w3p2_ "")
  python3 build_pack.py  ; python3 ../lab1/topdf.py /abs/out/Lab2_pack.html /abs/out/Lab2_pack.pdf      (must print "pages overflowing: none")
  python3 build_key.py   ; python3 ../lab1/topdf.py /abs/out/Lab2_key.html  /abs/out/Lab2_key.pdf
  python3 build_notebooks.py     builds both notebooks and TEST-RUNS every code cell against data/ (asserts 270 flagged at 0.4 and 99 of the top 100)
model.py      seed 697, stratified 80/20 split (the split the authors recommend), logistic regression C = 0.3 on standardised dummies; outcome = Dropout against the rest.
codebook.json variable descriptions and category codes, saved from the UCI record (Gender: 1 = male; yes/no variables: 1 = yes).
explore.py    the feasibility analysis of the outline stage (kept for the record; superseded by make_numbers.py).
The pack and key read their CSS from lab1/build_pack.py and lab1/build_key.py by regex, without executing them.
Scenario assumption (stated on the slide and in the pack with "Έστω"): the support team can see 100 students.
Two data cautions (teacher key, page 2): 180 rows with zero ENROLLED units in semester 1, 75 of whom graduated; the class "Enrolled" (794) is counted as "did not drop out".
