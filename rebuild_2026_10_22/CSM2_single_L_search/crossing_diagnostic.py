import argparse
import hashlib
import json
import math
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];REB=HERE.parent
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
refpath=HERE/'native_diagnostic_001/results.json';ref=json.loads(refpath.read_text())
snaps={s:REB/f'NATIVE_PARTIAL_2026-10-28/completed/M1e12_s{s}_ng64/snap_zf.npz' for s in (3,7,8)}
files=[Path(__file__),HERE/'CROSSING_CRITERIA.md',refpath,*snaps.values()];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hashes={str(p.relative_to(ROOT)):sha(p) for p in files};rows={};errors=[]
for seed,p in snaps.items():
    with np.load(p,allow_pickle=False) as z:
        x=z['x'];m=float(z['m']);meta=json.loads(str(z['meta']))
    centre=x.mean(axis=0);aperture=np.linalg.norm(x-centre,axis=1).max()
    while True:
        mask=np.linalg.norm(x-centre,axis=1)<aperture
        if mask.sum()<100:break
        centre=x[mask].mean(axis=0);aperture*=.8
    radii=np.sort(np.linalg.norm(x-centre,axis=1));n=np.arange(1,len(radii)+1)
    rho=meta['Mf']/(4/3*math.pi*meta['qM']**3)*(1+meta['zf'])**3
    above=np.flatnonzero(n*m/(4/3*math.pi*radii**3)>=18*math.pi**2*rho)
    rvir=float(radii[above.max()]);rconv=max(3*meta['eps'],float(radii[min(199,len(radii)-1)]))
    for ne in (21,25,29):
        edges=np.geomspace(rconv,rvir,ne);counts=np.histogram(radii,edges)[0]
        den=counts*m/(4/3*math.pi*np.diff(edges**3));rc=np.sqrt(edges[:-1]*edges[1:]);ok=counts>0
        lr=np.log(rc[ok]);ld=np.log(den[ok]);sm=np.convolve(ld,np.ones(3)/3,mode='same');sm[0],sm[-1]=ld[0],ld[-1]
        slopes=np.gradient(sm,lr);idx=np.flatnonzero((slopes[:-1]>-2)&(slopes[1:]<=-2))
        crossings=[]
        for i in idx:
            rm=float(np.exp(np.interp(-2,[slopes[i+1],slopes[i]],[lr[i+1],lr[i]])))
            crossings.append(dict(radius_Mpc=rm,cf=rvir/rm,n_inside=int((radii<rm).sum())))
        original=ref['variants'][str(ne)]['runs'][f'64|{seed}'];err=abs(crossings[0]['radius_Mpc']/original['rm2']-1);errors.append(err)
        rows[f'{seed}|{ne}']=dict(rvir=rvir,rconv=rconv,crossings=crossings,relative_first_radius_error=err)
checks=dict(nine_profiles=len(rows)==9,first_radius_reproduced=max(errors)<1e-10,inputs_stable=all(sha(ROOT/p)==h for p,h in hashes.items()))
result=dict(checks=checks,scope='Finite profile diagnostic; no replacement crossing or fitted parameter',rows=rows,input_sha256=hashes)
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(checks=checks,crossings={k:v['crossings'] for k,v in rows.items()}),indent=2));raise SystemExit(0 if all(checks.values()) else 1)
