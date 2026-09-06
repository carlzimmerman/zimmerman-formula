#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""g03q -- the candidate's dust against X-COP's measured residual profile.  Data: h67b's medians over the twelve X-COP clusters (canonical footing),
eta_data(r) = M_HSE(<r)/[nu(y_b) M_b(<r)] and y_b(r) = G M_b(<r)/(r^2 a0) at r = 30-420 kpc, which fix the median baryon profile M_b(<r) = y_b a0 r^2/G.
Prediction (the dust sources the MOND scalar, the AeST reading): M_dyn(<r) = nu(y_tot) [M_b + M_d](<r), y_tot = y_b (1 + M_d/M_b), with M_d/M_b(<r) from
the g03o collapse of the cluster at |K_2| = 3e5 (the dust-to-baryon ratio profile of the model cluster, transplanted onto X-COP's median baryon profile;
a modelling shortcut, stated).  eta_pred = M_dyn/[nu(y_b) M_b]; the fraction of the residual supplied is (eta_pred - 1)/(eta_data - 1).
The cluster's assembly redshift z_c sets how much of the share is captured: 0.3, 0.7, 1.0.  Checks can fail."""
import math, sys, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); src = open(os.path.join(HERE, "g03o_dust_spherical_collapse.py")).read()
head = src[:src.index('print("=" * 100)')]
head = head.replace("    return float((np.sum(m[order][bound]) + M_lump)/Mshare), float((np.sum(m[order][inner]) + M_lump)/Mshare)", "    return dict(rs=rs, rv=rv, E=E, m=m[order], bound_all=(E < 0) & (rs < R_edge), M_lump=M_lump)")
g = {"__file__": os.path.join(HERE, "g03o_dust_spherical_collapse.py")}; exec(compile(head, "g03ohead", "exec"), g)
run, kpc, MSUN, a0, G, nu_tot = g["run"], g["kpc"], g["MSUN"], g["a0"], g["G"], g["nu_tot"]
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
print("=" * 100); print("g03q -- X-COP residual profile vs the candidate's captured dust"); print("=" * 100)
R_kpc = np.array([30, 40, 50, 75, 100, 150, 200, 300, 420.0]); eta_data = np.array([3.13, 3.00, 2.86, 2.73, 2.78, 2.68, 2.76, 2.61, 2.31]); yb = np.array([0.49, 0.40, 0.36, 0.32, 0.30, 0.29, 0.27, 0.25, 0.22])
Mb = yb*a0*(R_kpc*kpc)**2/G
print("  X-COP medians (h67b, canonical): r [kpc] " + " ".join(f"{r:5.0f}" for r in R_kpc)); print("    eta_data:                  " + " ".join(f"{e:5.2f}" for e in eta_data)); print("    M_b(<r) [1e12 Msun]:       " + " ".join(f"{m/MSUN/1e12:5.1f}" for m in Mb))
Mb0, R500 = 1e14*MSUN, 1000*kpc
def dust_ratio_profile(zc, K2=3e5):
    d = run(Mb0, R500, K2, zc=zc); b = d["bound_all"]
    rr = R_kpc*kpc; Md = np.array([np.sum(d["m"][b & (d["rv"] < r)]) + d["M_lump"] for r in rr]); Mb_model = Mb0*(rr/R500)**1.2   # the model cluster's baryon profile
    return Md/Mb_model
RES = {}
for zc in (0.3, 0.7, 1.0):
    q = dust_ratio_profile(zc); ytot = yb*(1 + q); Mdyn = nu_tot(ytot)*Mb*(1 + q); eta_pred = Mdyn/(nu_tot(yb)*Mb); frac = (eta_pred - 1)/(eta_data - 1)
    RES[zc] = (q, eta_pred, frac)
    print(f"  z_c = {zc}: M_d/M_b(<r):  " + " ".join(f"{v:5.2f}" for v in q)); print(f"           eta_pred:      " + " ".join(f"{v:5.2f}" for v in eta_pred)); print(f"           residual supplied: " + " ".join(f"{v:5.2f}" for v in frac) + f"   (median {np.median(frac):.2f})", flush=True)
best = max(RES, key=lambda z: np.median(RES[z][2]))
fr = RES[best][2]
check("X1 the dust supplies a NONZERO but INCOMPLETE part of X-COP's residual at every radius 30-420 kpc for the best assembly redshift (between 5% and 90% at each radius)", np.all((fr > 0.05) & (fr < 0.9)), f"z_c = {best}: {np.round(fr, 2)}")
shape = np.corrcoef(np.log(R_kpc), fr)[0, 1]
check("X2 [reported] the radial trend of the supplied fraction: correlation with log r (negative = the dust covers the core better than the outskirts, positive = the reverse)", True, f"corr = {shape:+.2f}")
check("X3 no assembly redshift in 0.3-1.0 brings the median supplied fraction above 0.9: the dust in its window does not close the X-COP residual", all(np.median(RES[z][2]) < 0.9 for z in RES), f"medians {[round(float(np.median(RES[z][2])), 2) for z in RES]}")
print("\n  reading: with the dust sourcing the MOND scalar, the captured dust at |K_2| = 3e5 covers a fraction of the measured residual that is printed above; the rest is the framework's cluster liability, unchanged. Quantisation from the shell count is ~20%. The collapse method is UNCONVERGED (g03o D4: the cluster capture at this |K_2| ranges from 0 to 2x the cold reference under a change of shell spacing or start redshift), so the profile above is ONE configuration (equal-mass shells, z_i = 50), not a converged prediction. The modelling shortcut (model-cluster dust ratio onto X-COP's median baryon profile) and the assumed assembly history are stated.")
print(f"\nRESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "\nRESULT: 0 FAIL"); sys.exit(1 if FAILS else 0)
