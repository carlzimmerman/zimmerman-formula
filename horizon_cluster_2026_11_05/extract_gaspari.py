"""Extract numerical facts from authenticated arXiv:1904.10972v2 HTML.
Command: python horizon_cluster_2026_11_05/extract_gaspari.py
Raw source is locally retained and ignored; no paper prose is redistributed.
"""
import hashlib, json, re
from pathlib import Path
from bs4 import BeautifulSoup

BASE = Path(__file__).resolve().parent
raw = BASE / 'data/gaspari_source.html'
soup = BeautifulSoup(raw.read_text(), 'html.parser')
def number(text):
    text = text.replace('−', '-')
    match = re.match(r'^\s*([+-]?\d+(?:\.\d+)?)', text)
    return float(match[1]) if match else None
def error(text):
    match = re.search(r'±\s*([\d.]+)', text)
    return float(match[1]) if match else None

opt = ['name', 'PGC', 'type', 'N_members', 'distance_Mpc', 'logMBH',
       'logSigma', 'logLK', 'logMbulge', 'logRe_opt_kpc', 'B_T', 'refs']
xray = ['name', 'environment', 'logLx_g', 'logTx_g', 'logRx_g',
        'logLx_c', 'logTx_c', 'logRx_c', 'logLx500', 'logR500', 'refs']
tables = []
for id_, fields in [('A2.T2', opt), ('A2.T3', xray)]:
    out = []
    for tr in soup.find(id=id_).select('tr')[3:]:
        cells = [c.get_text(' ', strip=True) for c in tr.find_all(['td','th'], recursive=False)]
        assert len(cells) == len(fields), (id_, cells)
        row = {}
        for key, value in zip(fields, cells):
            if key in ['name','type','environment','refs']:
                row[key] = value
            else:
                row[key] = number(value)
                row['err_' + key] = error(value)
                row['limit_' + key] = ('<' in value or '>' in value or '≤' in value or '≥' in value)
        out.append(row)
    assert len(out) == 85 and len({r['name'] for r in out}) == 85
    tables.append(out)
assert [r['name'] for r in tables[0]] == [r['name'] for r in tables[1]]
payload = {'source_url':'https://arxiv.org/html/1904.10972v2',
 'source_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),
 'date_checked':'2026-11-05', 'version':'v2, 2019-10-23',
 'optical_table':tables[0], 'xray_table':tables[1],
 'size_warning':'Optical total half-light radius is not the spheroid radius of galaxies.json.'}
(BASE/'data/gaspari.json').write_text(json.dumps(payload,indent=2)+'\n')
print('Extracted 85 optical and 85 X-ray rows; names/order validated.')
