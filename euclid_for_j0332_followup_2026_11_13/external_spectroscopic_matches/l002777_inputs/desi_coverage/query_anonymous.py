"""Bounded public Data Lab queries; explicit documented guest token only."""
from pathlib import Path
import urllib.request,urllib.parse,urllib.error,json,hashlib,time
P=Path(__file__).resolve().parent
for label,ra,dec in [('l002777',141.2955,63.42385),('l017819',231.19015110938125,44.16376016502161)]:
    sql=f'select * from desi_dr1.zpix where q3c_radial_query(mean_fiber_ra,mean_fiber_dec,{ra},{dec},0.01) limit 20'
    url='https://datalab.noirlab.edu/query/query?'+urllib.parse.urlencode(dict(sql=sql,ofmt='csv',out='',async_='False')).replace('async_','async')
    req=urllib.request.Request(url,headers={'X-DL-AuthToken':'anonymous.0.0.anon_access','User-Agent':'Astronomy-public-data-audit/1.0'})
    t=time.monotonic()
    try:r=urllib.request.urlopen(req,timeout=45)
    except urllib.error.HTTPError as e:r=e
    with r:
        b=r.read(1000001);assert len(b)<=1000000
        rec=dict(url=url,sql=sql,guest_identity_source='https://raw.githubusercontent.com/astro-datalab/datalab/master/dl/Util.py',status=r.status,headers=dict(r.headers),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),elapsed_seconds=time.monotonic()-t)
    (P/(label+'_anonymous.csv')).write_bytes(b)
    (P/(label+'_anonymous.json')).write_text(json.dumps(rec,indent=2)+'\n')
    print(label,r.status,len(b),b[:300])
