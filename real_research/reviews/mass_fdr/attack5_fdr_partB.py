#!/usr/bin/env python3
"""
ATTACK 5 -- Part B: FDR on MASS-RATIO hits with TRANSCENDENTAL targets.

The dangerous case is NOT 2/3 (a rational, trivially re-describable) but
ratios like m_mu/m_e = 206.768 being matched by '64*pi + Z'. Here the target
is a generic real number, so FDR (how dense is the reachable set near the
target?) is the honest test.

Method: build a large library of O(1)-coefficient expressions from the allowed
symbol pool, then for each measured dimensionless ratio count how many library
expressions land within the measurement tolerance. Compare to the Poisson
expectation = (library density near target) x (2 x tol). A hit is FRIED only
if observed << expected is FALSE, i.e. only if the target is hit AND the
reachable set is sparse there.
"""
import numpy as np
from itertools import product

np.random.seed(1)
pi = np.pi
Z      = np.sqrt(32*pi/3)
kernel = np.sqrt(8*pi/3)

# --- measured dimensionless mass ratios (PDG-ish) -------------------------
m_e, m_mu, m_tau = 0.51099895, 105.6583755, 1776.86
m_u,m_d,m_s,m_c,m_b,m_t = 2.16,4.67,93.4,1270.0,4180.0,172570.0
m_p, m_W, m_Z, m_H = 938.272, 80377.0, 91187.6, 125250.0
alpha_inv = 137.035999

targets = {
    'm_mu/m_e'  : m_mu/m_e,        # 206.768
    'm_tau/m_mu': m_tau/m_mu,      # 16.817
    'm_tau/m_e' : m_tau/m_e,       # 3477.2
    'm_p/m_e'   : m_p/m_e,         # 1836.15
    'm_b/m_tau' : m_b/m_tau,       # 2.353
    'm_c/m_s'   : m_c/m_s,         # 13.597
    'm_t/m_b'   : m_t/m_b,         # 41.28
    'm_Z/m_W'   : m_Z/m_W,         # 1.1346
    'm_H/m_Z'   : m_H/m_Z,         # 1.3735
    'm_H/m_W'   : m_H/m_W,         # 1.5583
    '1/alpha'   : alpha_inv,       # 137.036
}

# --- symbol pool ----------------------------------------------------------
pool = {'Z':Z,'kernel':kernel,'pi':pi,'kappa':0.5,'sqrtpi':np.sqrt(pi),
        '2':2.,'3':3.,'4':4.,'5':5.,'6':6.,'7':7.,'8':8.,'9':9.,'10':10.,
        '11':11.,'12':12.,'16':16.,'32':32.,'64':64.,'e':np.e,
        'CUBE':8.,'GAUGE':12.,'Ngen':3.,'BEK':4.}
names = list(pool); vals = np.array([pool[n] for n in names])

# --- build expression library --------------------------------------------
# forms covering what the corpus uses: a, a*b, a/b, a+b, a*b+c, a+b/c, a/b/c...
lib_vals=[]; lib_lab=[]
def add(v,l):
    if np.isfinite(v) and 1e-3 < abs(v) < 1e7:
        lib_vals.append(v); lib_lab.append(l)

n=len(names)
for i in range(n):
    add(vals[i],names[i])
for i in range(n):
    for j in range(n):
        a,b=vals[i],vals[j]
        add(a*b,f"{names[i]}*{names[j]}")
        if b: add(a/b,f"{names[i]}/{names[j]}")
        add(a+b,f"{names[i]}+{names[j]}")
        add(a-b,f"{names[i]}-{names[j]}")
# triple: a*b+c, a*b-c, a*b/c, a/b+c  (this is where '64*pi+Z' lives)
for i,j,k in product(range(n),repeat=3):
    a,b,c=vals[i],vals[j],vals[k]
    add(a*b+c,f"{names[i]}*{names[j]}+{names[k]}")
    add(a*b-c,f"{names[i]}*{names[j]}-{names[k]}")
    if c: add(a*b/c,f"{names[i]}*{names[j]}/{names[k]}")
    if b: add(a/b+c,f"{names[i]}/{names[j]}+{names[k]}")

lib_vals=np.array(lib_vals)
N=len(lib_vals)
print(f"Expression library size = {N}")
print(f"(forms: a, a*b, a/b, a+-b, a*b+-c, a*b/c, a/b+c)\n")

# --- FDR per target -------------------------------------------------------
print(f"{'ratio':12s} {'measured':>12s} {'tol%':>6s} {'#hits':>6s} {'E[chance]':>10s} {'best label':<28s} {'verdict'}")
print("-"*100)
# assume ~0.5% measurement-ish tolerance for quark ratios, tighter for leptons
tols = {'m_mu/m_e':1e-4,'m_tau/m_mu':5e-3,'m_tau/m_e':5e-3,'m_p/m_e':1e-4,
        'm_b/m_tau':2e-2,'m_c/m_s':2e-2,'m_t/m_b':1e-2,'m_Z/m_W':1e-4,
        'm_H/m_Z':1e-3,'m_H/m_W':1e-3,'1/alpha':1e-5}

for name,t in targets.items():
    tol = tols[name]
    lo,hi = t*(1-tol), t*(1+tol)
    mask = (lib_vals>=lo)&(lib_vals<=hi)
    nhit = int(mask.sum())
    # local density: count library values within +-10% of target, get per-unit-frac density
    wide = (lib_vals>=t*0.9)&(lib_vals<=t*1.1)
    n_wide = int(wide.sum())
    # expected hits in the +-tol window if uniform over the +-10% band:
    E_chance = n_wide * (2*tol)/(0.2)
    # best matching label
    if nhit>0:
        idx=np.where(mask)[0]
        best=idx[np.argmin(np.abs(lib_vals[idx]-t))]
        best_lab=lib_lab[best]; best_val=lib_vals[best]
        best_err=abs(best_val-t)/t
    else:
        best_lab="--"; best_err=np.nan
    # verdict: FRIED only if a hit exists AND E_chance << 1 (sparse) AND it's not trivial
    verdict = "BAKED"
    if nhit>0 and E_chance<0.3:
        verdict="LOOK"   # worth a closer look
    if nhit>0 and E_chance>=1:
        verdict="BAKED(dense)"
    print(f"{name:12s} {t:12.4f} {tol*100:5.2f}% {nhit:6d} {E_chance:10.2f}  {best_lab:<28s} {verdict}")

print("\nInterpretation:")
print("  E[chance] = expected # of library expressions in the tolerance window")
print("  given the LOCAL density of reachable values. E>=1 => the hit is")
print("  unsurprising (the symbol set densely covers that region) => BAKED.")
print("  Only E<<1 with an actual hit would be a candidate ('LOOK').")
