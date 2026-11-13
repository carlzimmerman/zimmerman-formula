"""Extract only one target from public uncompressed DESI coadd using HTTP Range.

Never follows authenticated endpoints; hard stop if ranges are ignored. Raw bytes,
headers, SHA256 and exact offsets are retained to make derived subset reproducible.
"""
from pathlib import Path
import hashlib,json,urllib.request,math,time
from datetime import datetime,timezone
import numpy as np
from astropy.io import fits

P=Path(__file__).resolve().parent
URL='https://data.desi.lbl.gov/public/dr1/spectro/redux/iron/healpix/main/dark/99/9907/coadd-main-dark-9907.fits'
SIZE=124251840
TARGET=39633153882587315
R=P/'ranges';R.mkdir(exist_ok=True)
requests=[]
def get(start,n,label):
    assert n<=2000000 and start>=0 and start+n<=SIZE
    f=R/(label+'.bin'); m=R/(label+'.json')
    if f.exists() and m.exists():
        b=f.read_bytes();rec=json.loads(m.read_text())
        assert len(b)==n and rec['start']==start and rec['sha256']==hashlib.sha256(b).hexdigest()
        requests.append(rec);return b
    t=time.monotonic()
    req=urllib.request.Request(URL,headers={'Range':f'bytes={start}-{start+n-1}','User-Agent':'Astronomy-public-data-audit/1.0'})
    with urllib.request.urlopen(req,timeout=30) as resp:
        assert resp.status==206,('Server ignored range',resp.status)
        assert resp.headers['Content-Range']==f'bytes {start}-{start+n-1}/{SIZE}'
        b=resp.read(n+1);assert len(b)==n
        rec=dict(url=URL,start=start,nbytes=n,status=resp.status,headers=dict(resp.headers),
                 utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-t,
                 sha256=hashlib.sha256(b).hexdigest())
    f.write_bytes(b);m.write_text(json.dumps(rec,indent=2)+'\n');requests.append(rec)
    return b

def header(off,k):
    b=b''
    while True:
        block=get(off+len(b),2880,f'header_{k}_{len(b)//2880}')
        b+=block
        if any(block[i:i+8]==b'END     ' for i in range(0,2880,80)):break
    return fits.Header.fromstring(b.decode('ascii')),b

def ndata(h):
    if h.get('XTENSION') in ('BINTABLE','TABLE'):
        return int(h['NAXIS1']*h['NAXIS2']+h.get('PCOUNT',0))
    n=int(np.prod([h[f'NAXIS{i}'] for i in range(1,h['NAXIS']+1)])) if h['NAXIS'] else 0
    return n*abs(h['BITPIX'])//8

offset=0;spec={};hlist=[];summary=[]
while offset<SIZE:
    k=len(hlist);h,raw=header(offset,k);dataoff=offset+len(raw);n=ndata(h)
    name=h.get('EXTNAME','PRIMARY');summary.append(dict(name=name,header_offset=offset,data_offset=dataoff,data_bytes=n,header=dict(h)))
    hlist.append((name,h,dataoff,n))
    offset=dataoff+math.ceil(n/2880)*2880
assert offset==SIZE

# Download small complete FIBERMAP only; obtain row by actual target ID, not
# by assuming redrock/coadd row ordering. Reconstruct table for Astropy decoding.
name,h,off,n=next(x for x in hlist if x[0]=='FIBERMAP')
data=get(off,n,'fibermap')
from io import BytesIO
primary=fits.PrimaryHDU().header.tostring().encode('ascii')
table=fits.open(BytesIO(primary+h.tostring().encode('ascii')+data+b'\0'*((-n)%2880)))[1].data
rows=np.flatnonzero(table['TARGETID']==TARGET);assert len(rows)==1
row=int(rows[0]);assert abs(float(table['TARGET_RA'][row])-231.19026708953797)<1e-9
meta={k:(v.item() if isinstance(v,np.generic) else v) for k,v in zip(table.names,table[row])}
hdus=[fits.PrimaryHDU(),fits.BinTableHDU(table[rows],name='FIBERMAP')]
for name,h,off,n in hlist:
    if not any(name.startswith(b+'_') for b in 'BRZ'):continue
    dt={8:'>u1',16:'>i2',32:'>i4',64:'>i8',-32:'>f4',-64:'>f8'}[h['BITPIX']]
    shape=tuple(h[f'NAXIS{i}'] for i in range(h['NAXIS'],0,-1))
    if name.endswith('WAVELENGTH'):
        raw=get(off,n,name);arr=np.frombuffer(raw,dtype=dt).reshape(shape).copy()
    else:
        assert shape[0]==len(table)
        stride=n//shape[0];raw=get(off+row*stride,stride,name)
        arr=np.frombuffer(raw,dtype=dt).reshape((1,)+shape[1:]).copy()
    spec[name]=arr
    hh=h.copy()
    if not name.endswith('WAVELENGTH'):hh[f'NAXIS{h["NAXIS"]}']=1
    hdus.append(fits.ImageHDU(arr,header=hh,name=name))
np.savez_compressed(P/'target_coadd.npz',**spec)
fits.HDUList(hdus).writeto(P/'target_coadd_derived.fits',overwrite=True,checksum=True)
(P/'target_fibermap.json').write_text(json.dumps(meta,indent=2)+'\n')
(P/'coadd_range_manifest.json').write_text(json.dumps(dict(url=URL,parent_bytes=SIZE,targetid=TARGET,row=row,
    request_count=len(requests),downloaded_bytes=sum(r['nbytes'] for r in requests),
    hdu_layout=summary,derived_note='One-target subset rebuilt from raw byte ranges; not original whole-file checksum certified.'),indent=2)+'\n')
print(json.dumps(dict(targetid=TARGET,row=row,downloaded_bytes=sum(r['nbytes'] for r in requests),arrays={k:list(v.shape) for k,v in spec.items()})))
