#!/usr/bin/env python3
"""DA1 D1 part 2. Own rebuild of GS4's d from its parsed inputs and raw tables; spot checks of parsed rows against the source tables; conventions; h identity. MODE: PRIMARY or MUTATE_h (planted: fixed-angle conversion exponent flipped to -2.5). kappa = 1/2 FITTED; not theory closed."""
import csv, json, math, os, re, sys
import numpy as np
from astropy.io import fits
HERE=os.path.dirname(os.path.abspath(__file__)); RB=os.path.dirname(HERE); REPO=os.path.dirname(RB); X=os.path.join(REPO,'_external_data','gs4'); OUT=[]
MODE=sys.argv[1] if len(sys.argv)>1 else 'PRIMARY'; EXP=-2.5 if MODE=='MUTATE_h' else 2.5
def P(s): print(s); OUT.append(str(s))
E=fits.open(os.path.join(REPO,'real_research','data','erass1cl_primary_v3.2.fits'))[1].data
ER,ED,EZ=[np.asarray(E[k],float) for k in ('RA','DEC','BEST_Z')]; EM=np.asarray(E['M500'],float)*1e13; EG=np.asarray(E['MGAS500'],float)*1e11; ERK=np.asarray(E['R500'],float)
def DA(z,h,Om):
    x=np.linspace(0,z,500); return 299792.458/(100*h)*np.trapz(1/np.sqrt(Om*(1+x)**3+1-Om),x)/(1+z)
# identity: a fixed-angle X-ray gas mass scales as D_A^2.5 (n_e from emission measure ~ D^-1/2, volume ~ D^3), so h^-2.5
idn=[]
rows=list(csv.DictReader(open(os.path.join(RB,'GS4_pointed_gas_offset','gs4_inputs.csv'))))
hs=sorted({(float(r['h']),float(r['Om'])) for r in rows}); chk=[]
for h,Om in hs:
    if h==0.7: continue
    ratio=(DA(0.1,0.7,0.3)/DA(0.1,h,Om))**EXP; want=(h/0.7)**2.5*(DA(0.1,0.7,0.3)*0.7/(DA(0.1,h,Om)*h))**2.5; chk.append(abs(ratio/want-1))
idok=max(chk)<1e-9; P(f"h identity on the conversion, h,Om {hs}: max |ratio/expected - 1| {max(chk):.2e}: {'HOLDS' if idok else 'DEFINITION WRONG'}")
# spot checks against the source tables
tests=[]
T=open(os.path.join(X,'croston08','x','9154_ms.tex')).read(); m=re.search(r'^RXCJ0006\.0\$-\$3443 .*?& ([\d.]+) & ([\d.]+)\$\\pm',T,re.M); r=[q for q in rows if q['cat']=='C08' and q['name'].startswith('RXCJ0006.0')][0]; tests.append(('C08 RXCJ0006.0',abs(float(m[1])-float(r['R500']))<1e-6 and abs(10**float(m[2])/float(r['Mgas'])-1)<1e-6))
T=open(os.path.join(X,'eckert16','x','table3.tex')).read(); m=re.search(r'XLSSC 006.*?\$\(([\d.]+)_',T); r=[q for q in rows if q['cat']=='E16' and q['name']=='XLSSC006'][0]; tests.append(('E16 XLSSC006 gas 4.09e13, first (..)e column is Mgas by table header order',abs(float(r['Mgas'])/4.09e13-1)<1e-6 and float(m[1])==4.09))
H=open(os.path.join(X,'eckert16','x','xxl_fgas.tex')).read(); tests.append(('E16 header rho convention mu 0.61, 2.21 n_H','2.21n_H' in H))
T=open(os.path.join(X,'mahdavi13','x','table2.tex')).read(); tests.append(('M13 header r500_WL then M_WL then M_Gas','M_\\mr{WL}' in T and 'M_\\mr{Gas}' in T and T.index('M_\\mr{WL}')<T.index('M_\\mr{Gas}')))
for t,ok in tests: P(f"  source spot check {t}: {'ok' if ok else 'DIFFERS'}")
# rebuild
def match(s=1.19):
    best={}
    for c in rows:
        ra,de,z=float(c['ra']),float(c['dec']),float(c['z']); q=np.degrees(np.arccos(np.clip(np.sin(np.radians(de))*np.sin(np.radians(ED))+np.cos(np.radians(de))*np.cos(np.radians(ED))*np.cos(np.radians(ER-ra)),-1,1)))
        ok=(q<=3/60)&(np.abs(EZ-z)<0.01)&(EG>0)&(ERK>0)&(EM>0)
        if not ok.any(): continue
        j=int(np.where(ok)[0][np.argmin(q[ok])]); k=(c['cat'],j)
        if k in best and best[k]['sep']<=q[j]*60: continue
        qd=DA(z,.7,.3)/DA(z,float(c['h']),float(c['Om'])); Mc=float(c['Mgas'])*qd**EXP; Rc=float(c['R500'])*qd
        best[k]=dict(cat=c['cat'],j=j,sep=float(q[j]*60),lgM=float(np.log10(EM[j])),d=math.log10(Mc*(ERK[j]/Rc)**s/EG[j]),own=math.log10(Mc/EG[j]))
    return list(best.values())
xc=json.load(open(os.path.join(HERE,'da1_d1_xcop_PRIMARY.json')))
def stat(rs,key='d',incl=None):
    D={}
    for r in rs:
        if r['cat']=='V09' or not 4.4e13<=10**r['lgM']<=5.6e14: continue
        if incl and r['cat'] not in incl: continue
        D.setdefault(r['j'],[]).append(r[key])
    v=np.array([np.median(x) for x in D.values()]); i=np.random.default_rng(0).integers(0,len(v),(10000,len(v))); return float(np.median(v)),float(np.std(np.median(v[i],axis=1))),len(v)
RES={}
R0=match(); a=stat(R0); RES['rebuild']=a; P(f"Rebuild, slope-converted rows only (X-COP not in the inputs file; GS4 adds it): median d {a[0]:+.3f} +- {a[1]:.3f}, N {a[2]}. GS4 on all incl. X-COP: +0.005 +- 0.017, N 45")
for s in (1.0,1.19,1.4,1.58,2.0): x=stat(match(s)); P(f"  slope s {s}: {x[0]:+.3f} +- {x[1]:.3f}"); RES[f's{s}']=x
x=stat(R0,'own'); P(f"  own apertures: {x[0]:+.3f} +- {x[1]:.3f}"); RES['own']=x
dc=xc['conv_dex']; P(f"Convention: rho_gas/(m_p n_e): eRASS1 1.18; X-COP 1.131; E16 {0.61*2.21/1.21:.3f}. If every pointed catalogue sat at X-COP's convention, d rises by at most +{dc:.3f}: {a[0]+dc:+.3f}")
RES['conv']=dc
lab='DEFINITION WRONG' if not idok else 'HOLDS on h'; P(f"D1 h reading {MODE}: {lab}")
RES['label_h']=lab; json.dump(RES,open(os.path.join(HERE,f'da1_d1_gs4_{MODE}.json'),'w'),indent=1); open(os.path.join(HERE,f'da1_d1_gs4_{MODE}.out'),'w').write('\n'.join(OUT)+'\n')
if MODE!='PRIMARY' and idok: sys.exit(1)
