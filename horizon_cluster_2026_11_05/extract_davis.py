"""Numerical extraction of table 1, arXiv:1901.06509v2 (2019-05-25)."""
from pathlib import Path
from bs4 import BeautifulSoup
import re,json,hashlib
B=Path(__file__).resolve().parent
raw=B/'data/davis_source.html';s=BeautifulSoup(raw.read_text(),'html.parser')
def first(v):
 m=re.match(r'^\s*([+-]?\d+(?:\.\d+)?)',v.replace('−','-'))
 return float(m[1]) if m else None
rows=[]
for tr in s.find(id='S2.T1').select('tr')[3:]:
 cells=[]
 for c in tr.find_all(['td','th'],recursive=False):
  cells.append(c.get_text(' ',strip=True));cells.extend(['']*(int(c.get('colspan',1))-1))
 assert len(cells)==13,cells
 name=cells[0].split(' (catalog')[0]
 tex=re.search(r'\^\{\+([\d.]+)\}_\{-([\d.]+)\}',cells[2])
 rows.append({'name':name,'logMBH':first(cells[2]),'err_logMBH_plus':float(tex[1]) if tex else None,'err_logMBH_minus':float(tex[2]) if tex else None,
  'sigma_km_s':first(cells[5]),'err_sigma':first(cells[6]),'vmax_km_s':first(cells[7]),'err_vmax':first(cells[8]),'inclination_deg':first(cells[10]),'vmax_source':cells[9],
  'limit_vmax':any(ch in cells[7] for ch in ['<','>','≤','≥'])})
assert len(rows)==48 and len({r['name'] for r in rows})==48
assert all(r['logMBH'] is not None for r in rows)
out={'source':'https://arxiv.org/html/1901.06509v2','version':'v2, 2019-05-25','source_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'rows':rows}
(B/'data/davis.json').write_text(json.dumps(out,indent=2)+'\n')
print('rows',len(rows),'finite vmax',sum(r['vmax_km_s'] is not None for r in rows))
print(rows[:2])
