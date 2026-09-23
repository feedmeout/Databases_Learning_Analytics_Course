"""Real ERIC (eric.ed.gov) result counts for the workshop materials. Run on build day; writes eric_counts.json with the retrieval date."""
import urllib.request, urllib.parse, re, time, json, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
def count(q):
    url = 'https://eric.ed.gov/?' + urllib.parse.urlencode({'q': q})
    h = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=45).read().decode('utf8', 'replace')
    t = re.sub(r'<script.*?</script>', ' ', h, flags=re.S); t = re.sub(r'<[^>]+>', ' ', t); t = re.sub(r'\s+', ' ', t)
    m = re.search(r'Showing (?:all |\d[\d,]* to \d[\d,]* of )?([\d,]+) results?', t)
    if m: return int(m.group(1).replace(',', ''))
    if re.search(r'(No results|no results|0 results|did not match|Sorry)', t): return 0
    return None
B1 = '"learning analytics"'; B2 = '(dashboard* OR "visual analytics")'; B3 = '("self-regulated learning" OR self-regulation OR SRL)'; B4 = '("higher education" OR universit* OR undergraduate*)'
Q = {
 'n1': '(' + B1 + ')', 'n2': f'({B1}) AND {B2}', 'n3': f'({B1}) AND {B2} AND {B3}', 'n4': f'({B1}) AND {B2} AND {B3} AND {B4}', 'n4_2019': f'({B1}) AND {B2} AND {B3} AND {B4} pubyearmin:2019', 'n3_2019': f'({B1}) AND {B2} AND {B3} pubyearmin:2019', 'n2_2019': f'({B1}) AND {B2} pubyearmin:2019',
 'q_wild_in_quotes': f'{B1} AND "self-regulat*"', 'q_hyphen_wild': f'{B1} AND self-regulat*', 'q_phrase': f'{B1} AND "self-regulated learning"', 'q_word_wild': f'{B1} AND dashboard*', 'q_word': f'{B1} AND dashboard',
 'q_curly': '\u201clearning analytics\u201d AND dashboard*', 'q_straight': '"learning analytics" AND dashboard*',
 'p_none': 'dashboard* OR widget* AND "learning analytics"', 'p_or_first': '(dashboard* OR widget*) AND "learning analytics"', 'p_and_first': 'dashboard* OR (widget* AND "learning analytics")',
 'kaliisa': '(widget* OR dashboard*) AND ("learning analytics" OR "educational data mining" OR "educational datamining")',
}
if __name__ == '__main__':
    out = {'retrieved': datetime.date.today().isoformat(), 'site': 'https://eric.ed.gov', 'queries': {}}
    for k, q in Q.items():
        try: n = count(q)
        except Exception as ex: n = 'ERR ' + str(ex)[:80]
        out['queries'][k] = {'q': q, 'n': n}; print(f'{str(n):>8}  {k:18s} {q}'); time.sleep(1.3)
    json.dump(out, open(f'{HERE}/eric_counts.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
