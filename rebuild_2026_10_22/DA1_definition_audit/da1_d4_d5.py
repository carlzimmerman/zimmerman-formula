#!/usr/bin/env python3
"""DA1 D4 and D5, from raw tables and the record's JSON. D5: exponential refit of Bovy & Rix's K_z table; line windows; R_d prior readings on the UR3 and BS1 cells. D4: every source reading of the Upsilon window on FG1's S cells. kappa = 1/2 FITTED; not theory closed. Nothing here says the data favour the framework."""
import json, os, re
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); RB=os.path.dirname(HERE); REPO=os.path.dirname(RB); OUT=[]; RES={}
def P(s): print(s); OUT.append(str(s))
a=np.loadtxt(os.path.join(REPO,'real_research','data','mw_kz11_bovyrix2013_table3.tsv'),comments='#',skiprows=0,dtype=str); a=a[a[:,0]!='FeH'].astype(float)
d,K,e=a[:,5],a[:,6],a[:,7]
def fit(w):
    X=np.vstack([np.ones_like(d),d]).T; y=np.log(K); W=np.diag(w); C=np.linalg.inv(X.T@W@X); b=C@X.T@W@y; return b,C
for lab,sig in (('table errors',e),('errors + 5 %',np.hypot(e,0.05*K))):
    b,C=fit((K/sig)**2); h=1/b[1]; chi=float((((np.log(K)-(b[0]+b[1]*d))*K/sig)**2).sum()); P(f"K_z refit, {lab}, N {len(K)}: K(R0) {np.exp(b[0]):.2f} +- {np.exp(b[0])*np.sqrt(C[0,0]):.2f}, h {h:.2f} +- {h**2*np.sqrt(C[1,1]):.2f}, chi2 {chi:.1f}"); RES['Kfit_'+lab]=dict(K=float(np.exp(b[0])),eK=float(np.exp(b[0])*np.sqrt(C[0,0])),h=float(h),eh=float(h**2*np.sqrt(C[1,1])),chi2=chi)
P("Source: Bovy & Rix eq. 28, 67 exp(-(R-R0)/2.7), about 2.5 % and 4 %. Chain: 66.4 +- 2.2, h 2.72 +- 0.15, total force at |Z| 1.1 kpc, BR_R = R + (R0 - 8), fixed R0 - R as the table says")
U=json.load(open(os.path.join(RB,'UR3_direct_weighing','ur3_mw.json')))['rows']
RD={'LN16 photometric 2.64 +- 0.13, chain':(2.38,2.90),'BHG16 review thin disc 2.6 +- 0.5':(1.6,3.6),'BHG16 without GLIMPSE 2.5 +- 0.4':(1.7,3.3),'Bovy & Rix mass scale 2.15 +- 0.14':(1.87,2.43)}; MST=(3.8e10,8.36e10)
RES['MW']={}
for k,lab in (('A_c2b_refit|d0|off','C1 A'),('B_cfg886_bg|d0|off','C1 B'),('A_c2b_refit|d0|blum','C2 A'),('B_cfg886_bg|d0|blum','C2 B')):
    q=U[k]; b=q['best']; P(f"{lab}: class {q['cls']}, n_all {q['n_all']}, passing R_d {[round(x,2) for x in q['passing_Rd']]}; best cell R_d {b['R_d']:.2f}, M* {b['Mstar']:.3e}, M_bb {b['M_bb']:.3e}, disc {b['Mstar']-b['M_bb']:.3e}, V_c {b['vc_R0']:.1f}, K_z {b['K_R0']:.1f}")
    r={}
    for n,(lo,hi) in RD.items(): ok=any(lo<=x<=hi for x in q['passing_Rd']) and MST[0]<=b['Mstar']<=MST[1]; r[n]=bool(ok); P(f"   R_d prior {n}: {'IN PRIORS' if ok else 'not in priors'}")
    RES['MW'][lab]=r
P("C3: BS1's README: 3 cells on all four, Sigma_b 47.1, R_d 1.93, M_bb 1.88-2.12e10: same R_d, so the same reading applies; at its own L 4.0")
P("C4: X5 passing cells R_d 1.93, 2.27 have K_z 76.7-80.9, outside the 66.4 +- 4.4 line RF1 and UR3 use, so a wider R_d prior does not make them feasible on all four")
# D4
W={'chain 0.50-0.80':(0.50,0.80),'0.5 +- 25 % (Lelli+17), 0.375-0.625':(0.375,0.625),'0.5 +- 2 x 25 %, 0.25-0.75':(0.25,0.75),'McGaugh & Schombert 0.47 +- 25 %, 0.353-0.588':(0.3525,0.5875),'up to max-disc 0.7 (Lelli+16), 0.375-0.70':(0.375,0.70)}
txt=open(os.path.join(RB,'FG1_final_grade','README.md')).read()
c1=re.search(r'\| S SPARC \| \*\*PASS\*\* U ([\d.]+)/([\d.]+), rms ([\d.]+)/([\d.]+).*?\*\*FAIL\*\* U ([\d.]+)/([\d.]+), rms ([\d.]+)',txt); c3=re.search(r'\| Line \| C3 basin.*?\| S SPARC \| \*\*PASS\*\* U ([\d.]+)/([\d.]+).*?\*\*PASS\*\* U ([\d.]+)/([\d.]+)',txt,re.S); al=re.search(r'Alt, reported.*?\| S SPARC \| \*\*FAIL\*\* U ([\d.]+)/([\d.]+).*?\*\*FAIL\*\* U ([\d.]+)/([\d.]+)',txt,re.S)
S={'C1':(c1[1],c1[2]),'C2':(c1[5],c1[6]),'C3':(c3[1],c3[2]),'C4':(c3[3],c3[4]),'C3 alt':(al[1],al[2]),'C4 alt':(al[3],al[4])}; S={k:tuple(map(float,v)) for k,v in S.items()}; RES['S']=S; RES['D4']={}
for n,(lo,hi) in W.items():
    v={k:all(lo<=x<=hi for x in u) for k,u in S.items()}; RES['D4'][n]=v; P(f"Upsilon window {n}: "+', '.join(f"{k} {u[0]}/{u[1]} {'PASS' if v[k] else 'FAIL'}" for k,u in S.items()))
json.dump(RES,open(os.path.join(HERE,'da1_d4_d5.json'),'w'),indent=1); open(os.path.join(HERE,'da1_d4_d5.out'),'w').write('\n'.join(OUT)+'\n')
