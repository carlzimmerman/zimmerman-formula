import math, numpy as np
src=open('wl1.py').read(); cut=src.index('# ------------------------------------------------------------- run')
import os; __file__=os.path.abspath('wl1.py'); exec(compile(src[:cut],'wl1.py','exec'))
for f,a0 in A0.items():
  for lab,Rf in (("C",RmsC),("L",RmsL),("NC",RmsNC),("NL",RmsNL)):
    out=[]
    for lm in (9.4,10.45,10.7,10.9):
      pts=[p for p in LE if abs(p["Mb"]/MS-10**lm)/10**lm<1e-6]; Rc=Rf(10**lm*MS,a0)
      R=[math.sqrt(G*p["Mb"]/p["gbar"]) for p in pts]
      s=np.mean([math.log10(g_proj(r,p["Mb"],a0,Rc)/g_proj(r,p["Mb"],a0,math.inf)) for r,p in zip(R,pts)])
      out.append(f"{lm}: Rms {Rc/MPC:.2f} Rmax {max(R)/MPC:.2f} n {len(pts)} shift {s:+.3f}")
    print(f, lab, " | ".join(out))
