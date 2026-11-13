from pathlib import Path
import csv,subprocess,hashlib,json,datetime,concurrent.futures
P=Path(__file__).resolve().parent;OLD=P.parents[1]/'euclid_for_j0332_fit_2026_11_13/desi_crossmatch';rows=list(csv.DictReader(open(OLD/'matches_1arcsec.csv')));rows=[r for r in rows if r['Unique_Identifier']!='EUCL-DR1-L015780'];rows.sort(key=lambda r:['EUCL-DR1-L000216','EUCL-DR1-L018096','EUCL-DR1-L001368','EUCL-DR1-L002239'].index(r['Unique_Identifier']))
def fetch(r):
 p=P/r['Unique_Identifier'];p.mkdir(exist_ok=True);url='https://www.legacysurvey.org/viewer/desi-spectrum/dr1/targetid'+r['TARGETID'];f=p/'viewer.html';subprocess.run(['curl','-sSfL','--max-time','45','-D',str(p/'headers.txt'),'-o',str(f),url],check=True);pr=dict(url=url,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),bytes=f.stat().st_size,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),catalogue_row=r);(p/'fetch_provenance.json').write_text(json.dumps(pr,indent=2));return r['Unique_Identifier'],f.stat().st_size
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 for x in pool.map(fetch,rows):print(x,flush=True)
