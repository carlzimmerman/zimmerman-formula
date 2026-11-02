#!/usr/bin/env python3
"""PA1 post-result, no label: where the alt SEPARATES fires; form gaps in log alpha; height degeneracy. kappa = 1/2 FITTED; not theory closed."""
import json, numpy as np, math
G=4.30091e-6; KZU=2*math.pi*G*1e6; GY=1.02271; O=[]
for f in ("canonical","alt"):
    d=json.load(open(f"pa1_all_{f}.json")); Z=np.array(d["Z"]); Q=np.array(d["KQ"]); R=np.array(d["KR"]); al=KZU/Z*GY**2
    for nm,sg in (("D24 alpha",590.),("D24 anharmonic",655.)):
        O.append(f"[{f}] {nm} min-gap/sigma by z: "+", ".join(f"{z:.2f}:{(Q[:,j]-R[:,j]).min()*al[j]/sg:.2f}" for j,z in enumerate(Z)))
    O.append(f"[{f}] median log-alpha gap Q-R by z: "+", ".join(f"{z:.2f}:{np.median(np.log10(Q[:,j]/R[:,j])):.3f}" for j,z in enumerate(Z)))
    mq=np.median(Q,axis=0)*al; mr=np.median(R,axis=0)*al
    for t in (3981.,3236.):
        O.append(f"[{f}] log alpha {np.log10(t):.2f}: height where median Q chord matches {np.interp(-np.log10(t),-np.log10(mq),Z):.2f} kpc, median R {np.interp(-np.log10(t),-np.log10(mr),Z):.2f} kpc")
open("pa1_post.out","w").write("\n".join(O)+"\n"); print("\n".join(O))
