#!/usr/bin/env python3
"""DA1 K2: the pre-fix outer-key template (before b62559a575). Definition from the estimator: a key's measured A and its prediction must share one denominator, sum(n)/sum(v_C), on the run's own template. Chain text: x71_fstar.py reads G-OUT-Mall, M1-M3 as (A_CAL, s_CAL, run's pred). Test, per cell, A_CAL against the run's own A. kappa = 1/2 FITTED; not theory closed."""
import json, os, re, subprocess, sys
CRG=os.environ['DA1_CRG']; sys.path.insert(0,CRG); sys.dont_write_bytecode=True; HERE=os.path.dirname(os.path.abspath(__file__)); RB=os.path.dirname(HERE); os.chdir(CRG)
import numpy as np, crg1_clusters as C
OUT=[]
def P(s): print(s); OUT.append(s)
pre=subprocess.run(['git','-C',RB,'show','b62559a575~1:rebuild_2026_10_22/X71_smooth_core_measured_fstar/x71_fstar.py'],capture_output=True,text=True).stdout
hit=bool(re.search(r'g\["G-OUT-Mall"\] = \(a7\["OUTER"\]\["A_CAL"\], a7\["OUTER"\]\["s_CAL"\], Aall\[2\]\)',pre)); P(f"Pre-fix chain text at b62559a575~1, x71_fstar.py: key reads (A_CAL, s_CAL, pred): {hit}")
D=C.Data(); ST=C.stacks(); CSS=C.all_css(); r={}
for lab,d,k in (('C* at f* 0.20, no tail (X7 template)',lambda h:C.load_or_build(f'C4_h{h}',None),'vC_tab_canonical'),('run at f* 0.034 with gas tail',lambda h:C.load_or_build(f'DA1_C1_f0.034_g0.005_h{h}',None),'vC_tab_canonical')):
    h=0.672; c=d(h); M=C.Meas(D,h); t=C.keys_table(M,c.get('V',c.get('V_canonical')),c[k],'canonical','given'); x={q:(t['G-OUT-'+q]['own_A'],t['G-OUT-'+q]['A']) for q in ('Mall','M1','M2','M3')}; P(lab+': '+', '.join(f"{q} own {a:.4f} A_CAL {b:.4f}" for q,(a,b) in x.items())); r[lab]={q:list(v) for q,v in x.items()}
a=max(abs(u/v-1) for u,v in r['C* at f* 0.20, no tail (X7 template)'].values()); b=max(abs(u/v-1) for u,v in r['run at f* 0.034 with gas tail'].values()); P(f"max |own/A_CAL - 1|: on X7's own template {a:.1e}; on the run's template {b:.3f}")
lab='DEFINITION WRONG' if hit and a<1e-3 and b>0.05 else 'NOT FOUND'; P(f"K2 result: {lab} (must read DEFINITION WRONG)")
json.dump(dict(rows=r,a=a,b=b,label=lab),open(os.path.join(HERE,'da1_k2.json'),'w'),indent=1); open(os.path.join(HERE,'da1_k2.out'),'w').write('\n'.join(OUT)+'\n')
