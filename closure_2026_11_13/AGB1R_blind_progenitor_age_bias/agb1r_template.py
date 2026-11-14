"""AGB1R: build T_S and T_W from the frozen recipe; check KT. Writes agb1r_templates.json. Reads no supernova magnitude."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agb1r_common import build_template, dump, HERE

S = build_template("S"); W = build_template("W")
alt = build_template("S", bg=dict(H0=70.0, Om=0.3, w0=-1.0, wa=0.0))
pts = [0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.2]
idx = lambda z: int(round(z/0.01))
print(f"T_S: median age at z 0 = {S['age'][0]:.3f} Gyr")
for z in pts:
    print(f"  z {z:4.2f}  dage_S {S['dage'][idx(z)]:.3f} Gyr  T_S {S['T'][idx(z)]:.4f} mag   "
          f"dage_W {W['dage'][idx(z)]:.3f} Gyr  T_W {W['T'][idx(z)]:.4f} mag")
print(f"T_W: median age at z 0 = {W['age'][0]:.3f} Gyr")
print(f"T_S on a flat Om 0.3, H0 70 LCDM background: dage(1.0) = {alt['dage'][idx(1.0)]:.3f} Gyr")
kt = dict(dage_S_1=float(S['dage'][idx(1.0)]), T_S_1=float(S['T'][idx(1.0)]), dage_W_12=float(W['dage'][idx(1.2)]))
kt["pass"] = bool(5.0 <= kt["dage_S_1"] <= 5.6 and 0.15 <= kt["T_S_1"] <= 0.17 and 1.7 <= kt["dage_W_12"] <= 2.1)
print(f"KT: dage_S(1.0) {kt['dage_S_1']:.3f} in [5.0,5.6]; T_S(1.0) {kt['T_S_1']:.4f} in [0.15,0.17]; "
      f"dage_W(1.2) {kt['dage_W_12']:.3f} in [1.7,2.1] -> {'PASS' if kt['pass'] else 'FAIL'}")
dump(dict(z=S["z"], age_S=S["age"], T_S=S["T"], age_W=W["age"], T_W=W["T"], dage_S_lcdm_bg=alt["dage"], KT=kt),
     os.path.join(HERE, "agb1r_templates.json"))
