"""Trace Gaspari -> van den Bosch -> Beifiori Table 1 upper-limit rows."""
import json,re,hashlib
from pathlib import Path
from bs4 import BeautifulSoup
import numpy as np
B=Path(__file__).resolve().parent
v=BeautifulSoup((B/'data/vandenbosch_source.html').read_text(),'html.parser')
s=BeautifulSoup((B/'data/beifiori_source.html').read_text(),'html.parser')
p=json.loads((B/'data/gaspari.json').read_text());gp={r['name']:r for r in p['optical_table']}
def key(t):return re.sub(r'^NGC0*','N',re.sub(r'\s+','',t))
tab=s.find('table',id='Sx1.T1.3');assert 'Upper limits' in tab.get_text()
bt={key(tr.find(['td','th']).get_text(' ',strip=True)):tr for tr in tab.find_all('tr') if tr.find(['td','th'])}
rows=[]
for tr in v.find_all('tr'):
 if not tr.find('a',href='#bib.bib14'):continue
 cells=tr.find_all('td');name=cells[0].get_text(' ',strip=True) if cells else '';gname='N'+name[3:] if name.startswith('NGC') else name
 if gname not in gp:continue
 orig=bt[key(name)];bc=orig.find_all('td');low=float(bc[-2].get_text(strip=True));high=float(bc[-3].get_text(strip=True));assert bc[-1].get_text(strip=True)=='…'
 logmean=float(np.log10(high*low)/2);halfwidth=float(np.log10(high/low)/2)
 assert abs(logmean-gp[gname]['logMBH'])<.011
 assert abs(halfwidth-gp[gname]['err_logMBH'])<.011
 rows.append({'name':gname,'upper_limit_33deg_Msun':high,'upper_limit_81deg_Msun':low,'log_geometric_mean':logmean,'half_log_range':halfwidth,'catalog_logMBH':gp[gname]['logMBH'],'catalog_error':gp[gname]['err_logMBH'],'source_reference':'van den Bosch Table 1 reference 14 -> Beifiori 2012 Table 1 upper-limit section','primary_row':orig.get_text(' ',strip=True)})
assert len(rows)==16
out={'source_urls':['https://arxiv.org/html/1606.01246v2','https://arxiv.org/html/1109.6265v2'],'source_hashes':{n:hashlib.sha256((B/'data'/n).read_bytes()).hexdigest() for n in ['vandenbosch_source.html','beifiori_source.html']},'finding':'16 catalog central values match geometric means of two inclination-dependent upper limits; quoted errors match their half log ranges. These are not 16 secure measured BH masses. This audit is not a full classification of every remaining object.','rows':rows}
(B/'data/bh_upper_limit_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'n':len(rows),'names':[r['name'] for r in rows]}))
