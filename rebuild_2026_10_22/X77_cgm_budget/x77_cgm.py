#!/usr/bin/env python3
"""X77_cgm_budget: can a hot CGM (Zhang+24 eRASS:4 beta profile, normalised to f_b(<R_vir)) extrapolated to the
self-consistent r_ta supply the budget multiplier X76 needs? Frozen criteria: FROZEN_CRITERIA.md (d40d851943).
kappa = 1/2 FITTED; c_f EXTERNAL; not theory closed; nothing here says the data favour the framework.
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x77_cgm.py
"""
import os, sys, json, math
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REB, "X76_galaxy_fair_share_halos")); import x76_patch as XP
OUT = []; CHK = {}
def P(s=""): print(s, flush=True); OUT.append(str(s))
def check(k, ok, v): CHK[k] = bool(ok); P(f"  {k}: {'PASS' if ok else 'FAIL'} ({v})")

H_NAT = 0.679; Z_TA = 0.1797                      # F2 native h for the cold-gas relation (as X53/X76); X75 median host z
NEED = dict(sat=1.25, lens=0.85)                 # X76 per-bin needs, smaller of bins 3-4 (frozen)
BINS = {"MW": dict(Ms=5.5e10, fb=0.12, sfb=0.06, Mvir=1.3e12, Rvir=196e3, beta=0.43, bp=0.10, bm=0.06, rc=6e3),
        "M31": dict(Ms=1.3e11, fb=0.07, sfb=0.02, Mvir=4.2e12, Rvir=281e3, beta=0.37, bp=0.04, bm=0.02, rc=4e3)}
# Rvir: Zhang Table 1 (log Mh, R_h) = (12.0,178),(12.2,210),(12.7,295) interpolated in log Mh
TAB = np.array([[12.0, 178], [12.2, 210], [12.7, 295]])
for k in BINS: BINS[k]["Rvir"] = float(np.interp(math.log10(BINS[k]["Mvir"]), TAB[:, 0], TAB[:, 1])) * 1e3


def shape_mass(r, beta, rc):
    """M(<r) / rho0 for the beta profile, by quadrature (pc units)."""
    return quad(lambda x: 4 * math.pi * x * x * (1 + (x / rc) ** 2) ** (-1.5 * beta), 0, r, epsabs=0, epsrel=1e-11, limit=500)[0]


def cold(Ms):
    l = math.log10(Ms); l70 = l - 2 * math.log10(0.70 / H_NAT); return Ms * 10 ** (-0.69 * l70 + 6.63)


def budget(b, fb, beta, hot_override=False):
    Ms, Mc = b["Ms"], cold(b["Ms"]); M0 = Ms + Mc + 0.5 * Ms
    Mhv = fb * b["Mvir"] - Ms
    norm = Mhv / shape_mass(b["Rvir"], beta, b["rc"])
    Mhot = (lambda r: 0.5 * Ms) if hot_override else (lambda r: norm * shape_mass(r, beta, b["rc"]))
    f = lambda lr: math.log(XP.rta_pc(Ms + Mc + Mhot(math.exp(lr)), Z_TA)) - lr
    rta = math.exp(brentq(f, math.log(1e4), math.log(1e8), xtol=1e-14))
    Mbt = Ms + Mc + Mhot(rta)
    return dict(m=math.log10(Mbt / M0), rta_kpc=rta / 1e3, rta_over_Rvir=rta / b["Rvir"], Mhot_vir=Mhv, Mhot_rta=Mhot(rta),
                frac_beyond_Rvir=1 - (Mhv / Mhot(rta) if not hot_override else 1.0), Mbt=Mbt, M0=M0,
                fixed_point_resid=abs(XP.rta_pc(Mbt, Z_TA) / rta - 1),
                M_3Rvir=(norm * shape_mass(3 * b["Rvir"], beta, b["rc"]) if not hot_override else None))


P("X77_cgm_budget  criteria d40d851943  [kappa = 1/2 FITTED; c_f EXTERNAL; not theory closed]")
b = BINS["MW"]
# K1: beta=2/3 closed form M(<r) = 4 pi rc^3 (x - atan x)
r_, rc_ = 2e5, 6e3; cf = 4 * math.pi * rc_ ** 3 * (r_ / rc_ - math.atan(r_ / rc_))
check("K1_beta_mass_closed_form", abs(shape_mass(r_, 2 / 3, rc_) / cf - 1) < 1e-8, f"{shape_mass(r_, 2 / 3, rc_) / cf - 1:+.1e}")
c = budget(b, b["fb"], b["beta"])
check("K2_rta_fixed_point", c["fixed_point_resid"] < 1e-10, f"{c['fixed_point_resid']:.1e}")
k3 = budget(b, b["fb"], b["beta"], hot_override=True)["m"]
check("K3_inventory_identity", abs(k3) < 1e-12, f"m {k3:+.1e}")
mu = budget(b, b["fb"], 0.25)["m"]
check("MUTATE_beta_0.25_raises_m", mu > c["m"], f"{mu:+.3f} vs {c['m']:+.3f}")
RES = {"criteria": "d40d851943", "need": NEED, "z_ta": Z_TA, "bins": {}, "checks": CHK}
for name, b in BINS.items():
    cases = {"central": (b["fb"], b["beta"]), "generous": (b["fb"] + b["sfb"], b["beta"] - b["bm"]), "tight": (max(b["fb"] - b["sfb"], 1e-3), b["beta"] + b["bp"])}
    rows = {}
    for lab, (fb, be) in cases.items():
        if fb * b["Mvir"] <= b["Ms"]:
            rows[lab] = dict(m=None, note="f_b M_vir <= M*: no hot CGM"); P(f"  [{name} {lab}] f_b {fb:.2f}: no hot CGM inside R_vir"); continue
        r = budget(b, fb, be); rows[lab] = r
        P(f"  [{name} {lab:8s}] f_b {fb:.2f} beta {be:.2f}: M_hot(<Rvir {b['Rvir'] / 1e3:.0f} kpc) {r['Mhot_vir']:.2e}; r_ta {r['rta_kpc']:.0f} kpc "
          f"({r['rta_over_Rvir']:.1f} Rvir); M_hot(<r_ta) {r['Mhot_rta']:.2e} ({100 * r['frac_beyond_Rvir']:.0f}% beyond Rvir); m_CGM {r['m']:+.3f}")
    RES["bins"][name] = rows
mc, mg = RES["bins"]["MW"]["central"]["m"], RES["bins"]["MW"]["generous"]["m"]
if mc >= NEED["sat"]: V = "CGM BUDGET SUPPLIES THE MASS"
elif mc >= NEED["lens"]: V = "CGM BUDGET SUPPLIES LENSING ONLY"
elif mg >= NEED["lens"]: V = "CGM BUDGET ONLY AT THE GENEROUS EDGE"
else: V = "CGM BUDGET EXCLUDED"
RES["verdict"] = V
P(f"\n=== VERDICT (MW-mass bin vs needs sat +{NEED['sat']} / lens +{NEED['lens']}): {V}  (central m_CGM {mc:+.3f}, generous {mg:+.3f})")
n = sum(CHK.values()); P(f"checks {n}/{len(CHK)}")
json.dump(RES, open(os.path.join(HERE, "x77_cgm_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "x77_cgm.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if n == len(CHK) else 1)
