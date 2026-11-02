#!/usr/bin/env python3
"""DA1 D3: is LC1/PZ1's f_Q the same quantity RM2 needs? LC1's f_Q is measured against Blumenthal on the zoom's own cuspy no-disc profile. RM2's f multiplies (M_c - M_0) on the smooth-core start. Here the live cold mass at r/R_d 2, 3, 4 is put on the smooth-core start's own terms. kappa = 1/2 FITTED, unused; not theory closed."""
import glob, json, math, os, sys
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); RB=os.path.dirname(HERE); OUT=[]
sys.dont_write_bytecode=True; sys.path.insert(0,os.path.join(RB,'UR3_direct_weighing')); import ur3_common as U
def P(s): print(s); OUT.append(s)
RD=[2,3,4]; res={}
def lane(root,lab,tag):
    rows=[]
    for d in sorted(glob.glob(os.path.join(RB,root,'runs','M1e12_s?_ng64'))):
        s=os.path.basename(d); f=os.path.join(d,'snap_z0.00.npz'); g=os.path.join(RB,'ZN1_zooms_to_z0','runs',s,'snap_z0.00.npz')
        if not(os.path.exists(f) and os.path.exists(g)): continue
        A,B=np.load(f,allow_pickle=False),np.load(g,allow_pickle=False); me=json.loads(str(A['meta'])); m0=float(B['m']); N=len(B['x'])
        ctr=lambda x:_c(x)
        Md=float(me.get('Md_now',me.get('Md'))); Rd=3.565; Msim=m0*N; m1=m0*(1-Md/Msim)
        ra=np.sort(np.sqrt(((A['x']-_c(A['x']))**2).sum(1)))*1e3; rb=np.sort(np.sqrt(((B['x']-_c(B['x']))**2).sum(1)))*1e3
        rr=np.array(RD)*Rd; Ml=np.searchsorted(ra,rr)*m1; Mn=np.searchsorted(rb,rr)*m1; Ql=Ml/Mn
        M,R,S,r0=U.halo(math.log10(Md),tag); rg=np.geomspace(1e-2,R,6000); M0=math.pi*S*r0**2*U.Bs(rg/r0); Mb=Md*(1-Rd/np.sqrt(rg**2+Rd**2))
        Mc=U.contract(rg,Mb,M0,float(Mb[-1]/M0[-1]))[0]; M0r=np.interp(rr,rg,M0); Mcr=np.interp(rr,rg,Mc); feq=(Ml-M0r)/(Mcr-M0r); fQ_core=(Ql-1)/(Mcr/M0r-1)
        rows.append(dict(seed=s,Ml=Ml.tolist(),Mn=Mn.tolist(),M0=M0r.tolist(),Mc=Mcr.tolist(),feq=feq.tolist(),f_ratio=fQ_core.tolist(),Ql=Ql.tolist(),Qc=(Mcr/M0r).tolist(),cold_M=M,r0=r0))
    med=lambda k:np.median([q[k] for q in rows],axis=0)
    P(f"{lab}, {tag}: {len(rows)} seeds; chain's cold M {rows[0]['cold_M']:.3e}, r0 {rows[0]['r0']:.2f} kpc; r/R_d {RD}")
    P(f"  live cold mass (disc)        {np.round(med('Ml')/1e10,3).tolist()} e10"); P(f"  live cold mass (no disc)     {np.round(med('Mn')/1e10,3).tolist()} e10")
    P(f"  smooth-core start M_0        {np.round(med('M0')/1e10,3).tolist()} e10"); P(f"  smooth core + Blumenthal M_c {np.round(med('Mc')/1e10,3).tolist()} e10")
    P(f"  Q live {np.round(med('Ql'),3).tolist()}; Q on smooth core {np.round(med('Qc'),3).tolist()}")
    fe=[float(np.median(q['feq'])) for q in rows]; fr=[float(np.median(q['f_ratio'])) for q in rows]
    P(f"  f in RM2's own form, live mass on the core start, (M_live - M_0)/(M_c - M_0): median {np.median(fe):.3f} [{min(fe):.3f}, {max(fe):.3f}]")
    P(f"  f as a ratio of responses, (Q_live - 1)/(Q_core - 1): median {np.median(fr):.3f} [{min(fr):.3f}, {max(fr):.3f}]")
    res[lab+'|'+tag]=dict(rows=rows,feq_med=float(np.median(fe)),feq_range=[min(fe),max(fe)],fratio_med=float(np.median(fr)),fratio_range=[min(fr),max(fr)])
def _c(x):
    c=np.median(x,0); r=np.sqrt(((x-c)**2).sum(1)).max()
    for _ in range(40):
        s=((x-c)**2).sum(1)<r*r
        if s.sum()<200: break
        c=x[s].mean(0); r*=0.85
    return c
for tag in ('A_c2b_refit','B_cfg886_bg'):
    lane('LC1_live_contraction','LC1',tag); lane('PZ1_disc_during_collapse','PZ1',tag)
json.dump(res,open(os.path.join(HERE,'da1_d3.json'),'w'),indent=1); open(os.path.join(HERE,'da1_d3.out'),'w').write('\n'.join(OUT)+'\n')
