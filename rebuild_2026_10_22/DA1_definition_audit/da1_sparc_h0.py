#!/usr/bin/env python3
"""DA1 D6: SPARC's Hubble-flow distances (fD = 1, 97 galaxies) use the paper's H0. Rerun S, Tl, LT on the native h 0.6856427: those galaxies' D x k, k = H0_paper/68.56; R x k, V_gas, V_disk, V_bul squared x k, L, MHI x k^2, V_obs unchanged. CRG1's scratch copy, its own partials. kappa = 1/2 FITTED; not theory closed."""
import glob, json, math, os, shutil, sys
CRG=os.environ['DA1_CRG']; TAG=os.environ.get('DA1_H0TAG','h0n'); H0P=float(os.environ.get('DA1_H0P','73.0')); PART=f'parts_{TAG}'; os.environ['CRG1_PARTIALS']=PART; sys.path.insert(0,CRG); sys.dont_write_bytecode=True
HERE=os.path.dirname(os.path.abspath(__file__)); os.chdir(CRG); os.makedirs(PART,exist_ok=True)
for f in glob.glob('partials/zoom_*.json'): shutil.copy(f,PART)
for f in glob.glob(PART+'/sparc_*'): os.remove(f)
import crg1_sparc as C, numpy as np
k=H0P/68.56427; fD={l.split()[0]:l.split()[4] for l in open(os.path.join(C.INP,'sparc','SPARC_Lelli2016c.mrt')) if len(l.split())==19}; old=C.load_gal
def scaled():
    G=old(); n=0
    for g in G:
        if fD[g['name']]!='1': continue
        n+=1; s=math.sqrt(k); g['Rk']=g['Rk']*k; g['R']=g['R']*k; g['Vgas']=g['Vgas']*s; g['Vdisk']=g['Vdisk']*s; g['Vbul']=g['Vbul']*s; g['L36']=g['L36']*k**2; g['MHI']=g['MHI']*k**2; g['lgMb']=g['lgMb']+2*math.log10(k)
    print('scaled',n,'k',k); return G
C.load_gal=scaled; C.main()
out={}
for f in sorted(glob.glob(PART+'/sparc_*.json')):
    a=json.load(open(f)); n=os.path.basename(f)[:-5]; out[n]={}
    rows=a.get('rows',a)
    for b,r in rows.items():
        if isinstance(r,dict) and 'S' in r: out[n][b]=dict(Y=r['S'].get('Y_med'),rms=r['S'].get('rms'),tilt=(r.get('Tl') or {}).get('tilt'))
    out[n]['passes']=a.get('passes')
    print(n,json.dumps(out[n])[:300])
json.dump(dict(k=k,H0_paper=H0P,out=out),open(os.path.join(HERE,f'da1_sparc_{TAG}.json'),'w'),indent=1)
open(os.path.join(HERE,f'da1_sparc_{TAG}.out'),'w').write(json.dumps(dict(k=k,H0_paper=H0P,out=out),indent=0)+'\n')
