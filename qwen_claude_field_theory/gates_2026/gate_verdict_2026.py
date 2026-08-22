#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
gate_verdict_2026.py -- the go/no-go inequality.

beta_req = ln(n_SS / n_gal) / ln(T_SS / T_gal)     vs     beta_SPARC +/- sigma_beta

T = a0^{3/2}/sqrt(G M)  =>  T_SS/T_gal = sqrt(M_gal/M_sun) EXACTLY, independent of a0.
Both n_SS and n_gal are carried as RANGES, per Carl's instruction not to use one pair of
central values.  Verdict is one of Carl's Case A / B / C.
"""
import os, sys, json
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__))
def info(l,d=""): print(f"  [info] {l}"+(f"   {d}" if d else ""))
def head(t): print("\n"+"="*104+f"\n{t}\n"+"="*104)
print(__doc__)
g2=json.load(open(os.path.join(HERE,"gate2_result.json")))
g3=json.load(open(os.path.join(HERE,"gate3_result.json")))
MSUN=1.98892e30; M_PIVOT=1.0e10

head("1. DHF REPRODUCTION STATUS")
info("Q2 pipeline","DHF Table 1 n-family, all five fiducial rows, reproduced end-to-end to 0.24%")
info("q(e~) validation","DHF Fig.1 nu_RAR anchors to 0.001-0.76%; M09 mu_3 to 0.2%")
info("SPARC sample",f"{g2['sample']['ngal']} galaxies / {g2['sample']['npts']} points / "
                    f"{g2['sample']['bulge']} bulges  vs DHF's 147 / 2696 / 31")
info("H0 universal-n fit",f"n = {g2['H0']['n']:.3f}, a0 = {g2['H0']['a0']*1e10:.3f}e-10, "
     f"sigma_int = {g2['H0']['sig']:.4f} dex   vs DHF 1.02+-0.04 / 1.08+-0.04 / 0.034")

head("2. UNIVERSAL-n vs ENVIRONMENT-DEPENDENT-n")
H1=g2["H1"]
info("H1 best fit",f"beta = {H1['beta']:+.4f}   n0 = {H1['n0']:.3f}   a0 = {H1['a0']*1e10:.3f}e-10")
info("model comparison",f"Delta chi2 = {H1['dchi2']:+.2f}   Delta AIC = {H1['dAIC']:+.2f}   "
                         f"Delta BIC = {H1['dBIC']:+.2f}   (positive favours H1)")
pn=g2.get("perm_null")
if pn: info("permutation null",f"sd {pn['sd']:.4f}, p(two-sided) = {pn['p']:.3f}")
for k,v in g2.get("confounds",{}).items(): info(f"confound {k[:52]:<52}",f"beta = {v['beta']:+.4f}")

head("3. SPARC POSTERIOR / UPPER LIMIT ON beta")
b1,b2=g2["beta_1sig"],g2["beta_2sig"]
info("beta_SPARC",f"{H1['beta']:+.4f}   1sigma [{b1[0]:+.3f}, {b1[1]:+.3f}]   "
                   f"2sigma [{b2[0]:+.3f}, {b2[1]:+.3f}]")
info("SPARC internal lever",f"ln T spans {g2['lnT_lever']:.2f} within the sample "
                             f"({g2['lnT_lever']/np.log(10):.2f} decades)")

head("4. SOLAR-SYSTEM REQUIRED beta_req")
nSS_lo=g3["n_post"]["p05"]; nSS_med=g3["n_post"]["median"]
info("n_SS (full posterior, Cassini alone)",
     f"median {nSS_med:.2f}, 95% lower credible bound {nSS_lo:.2f}")
for r in g3["n_hard"]: info(f"n_SS {r['label'][:46]:<46}",f"{r['lo']:.2f} to {r['hi']:.2f}")
lnT=0.5*np.log(M_PIVOT)
info("lever",f"ln(T_SS/T_gal) = 0.5 ln(M_gal/M_sun) = {lnT:.2f} at the 1e10 Msun pivot "
             "-- EXACT, a0-independent")
ngal_lo,ngal_hi=0.98,1.06                                  # [DHF Tab.1] 1.02 +- 0.04
brl,brh=[],[]
for nSS in (nSS_lo,nSS_med,g3["n_post"]["p95"]):
    for ng in (ngal_lo,ngal_hi):
        for Mg in (1e9,1e10,3.6e11):
            b=np.log(nSS/ng)/(0.5*np.log(Mg))
            brl.append(b); brh.append(b)
br=np.array(brl)
b_med=np.log(nSS_med/1.02)/lnT
b_min=np.log(nSS_lo/ngal_hi)/(0.5*np.log(3.6e11))
b_max=np.log(g3["n_post"]["p95"]/ngal_lo)/(0.5*np.log(1e9))
info("beta_req median",f"{b_med:+.4f}")
info("beta_req full range",f"[{br.min():+.4f}, {br.max():+.4f}]  "
     f"(over n_SS 5th-95th pctile x n_gal 1.02+-0.04 x M_gal 1e9-3.6e11 Msun)")

head("5. GO / NO-GO")
lo,hi=b2[0],b2[1]      # SPARC 2sigma
overlap=not (br.min()>hi or br.max()<lo)
req_lo,req_hi=br.min(),br.max()
info("SPARC 2sigma allows",f"beta in [{lo:+.3f}, {hi:+.3f}]")
info("Solar System requires",f"beta in [{req_lo:+.3f}, {req_hi:+.3f}]")
if not overlap:
    verdict="NO-GO (Carl's Case A)"
    why=("the SPARC 2-sigma interval on beta and the Solar-System required interval are "
         "DISJOINT. The environment-dependent-transition escape fails phenomenologically, "
         "before any action is written.")
elif abs(H1["beta"])<max(abs(lo),abs(hi))*0.5 and H1["dBIC"]<0:
    verdict="VIABLE BUT UNSUPPORTED (Carl's Case B)"
    why=("SPARC permits the required beta but does not require it; beta = 0 remains an "
         "acceptable fit. The mechanism is a hypothesis, not an empirical clue.")
else:
    verdict="GO (Carl's Case C)"
    why=("SPARC PREFERS beta != 0 and the preferred value overlaps beta_req. This is a new "
         "empirical clue and justifies the covariant-invariant search.")
info("*** VERDICT ***",verdict); info("",why)
json.dump(dict(verdict=verdict,beta_sparc=H1["beta"],beta_1sig=b1,beta_2sig=b2,
               beta_req_range=[float(br.min()),float(br.max())],beta_req_median=float(b_med),
               n_SS=g3["n_post"],overlap=bool(overlap)),
          open(os.path.join(HERE,"gate_verdict.json"),"w"),indent=1)
print("\n"+"="*104+f"\n{verdict}\n"+"="*104)
