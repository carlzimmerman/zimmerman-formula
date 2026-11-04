#!/usr/bin/env python3
"""CFG478: cm14b's cluster satellites with the EXACT QUMOND enclosed phantom of a point mass in a uniform host field (FROZEN_CRITERIA.md).
Run: python3 cfg478_qumond_efe.py [--mutate]

CW3 COPY (cw_lanes_2026_11_04/CW3_cz1_defect_sweep). The original campaign_fresh_gravity/CFG478_satellites_qumond_efe/cfg478_qumond_efe.py
is not edited.  Only the host field inside nu changes.  CW3_FIELD=orig: the committed g_e = G M_NFW(<R)/R^2, the cluster's measured
mass (K1).  CW3_FIELD=newton: that field inverted through each kernel's own nu (y nu(y) = x) per footing; Q2/Q3 keep multiplying it
(AMENDMENTS A4).  CW3_MUTATE=1: nu == 1 in the phantom (the inversion keeps the real kernel, so the two fields still differ).
The lane's own --mutate (g_e -> 0) is not used here.  kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, io, contextlib
import numpy as np
from scipy.stats import chi2
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); LANES = os.path.join(REPO, "campaign_fresh_gravity")
FIELD = os.environ.get("CW3_FIELD", "orig"); assert FIELD in ("orig", "newton")
MUT = os.environ.get("CW3_MUTATE") == "1"; TAG = f"_{FIELD}" + ("_MUTATE" if MUT else "")
sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
CM = os.path.join(REPO, "sonnet55_push", "cold_mass", "cm14b_sifon_table.py")
src = open(CM).read(); ns = {"__file__": CM, "__name__": "cm14b"}
os.environ.pop("MUTATE", None)
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[:src.index('rows = {"A"')], ns)                       # parsing + host model only (read-only)
mstar, mbg, rsat, Mh = ns["mstar"], ns["mbg"], ns["rsat"], ns["Mh"]
rho_h, G, Msun, Mpc = ns["rho_h"], ns["G"], ns["Msun"], ns["Mpc"]
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
KER = {"P2": lambda y: np.sqrt(1 + 1 / np.maximum(y, 1e-30)), "nu_mono": lambda y: C.nu_mono(np.maximum(y, 1e-30))}
KER_INV = dict(KER)                                                # CW3: the real kernels, used only to invert the observed field
if MUT: KER = {k: (lambda y: np.ones_like(np.asarray(y, dtype=float))) for k in KER}
def yN_of(nuf, x):
    """CW3: Newtonian y with y nu(y) = x (the observed field / a0), through the kernel nuf."""
    f = lambda ly: math.log(math.exp(ly) * float(np.asarray(nuf(np.array([math.exp(ly)])))[0])) - math.log(x)
    return math.exp(brentq(f, math.log(x) - 30, math.log(x) + 5, xtol=1e-14))
P(f"[CW3] external field = {FIELD}; MUTATE nu == 1: {MUT}")
TH = np.linspace(0, math.pi, 4001)
def mph_exact(Mb_kg, r_m, ge, a0, nu):
    gn = G * Mb_kg / r_m ** 2
    gr = -gn + ge * np.cos(TH)                                  # g . r_hat
    gmag = np.sqrt(gn ** 2 + ge ** 2 - 2 * gn * ge * np.cos(TH))
    integrand = (nu(gmag / a0) - 1) * gr * np.sin(TH)
    flux = 2 * math.pi * r_m ** 2 * np.trapz(integrand, TH)
    return -flux / (4 * math.pi * G)                               # kg
# controls
a0c = 9.3603e-11; Mt = 1e11 * Msun; rt = 0.1 * Mpc
k1 = abs(mph_exact(Mt, rt, 0.0, a0c, KER["P2"]) / ((KER["P2"](G * Mt / rt ** 2 / a0c) - 1) * Mt) - 1) < 1e-6
k2 = abs(mph_exact(1e-30, rt, 0.7 * a0c, a0c, KER["P2"])) / (0.7 * a0c * rt ** 2 / G) < 1e-10
ye = 0.7; nue = float(KER["P2"](np.array([ye]))[0]); Le = -0.5 / (ye + 1)
rbig = math.sqrt(G * Mt / (0.01 * ye * a0c))
bst = 1 + mph_exact(Mt, rbig, ye * a0c, a0c, KER["P2"]) / Mt
k3 = nue * (1 + Le) <= bst <= nue
P(f"K1 isolated limit: {'PASS' if k1 else 'FAIL'}; K2 uniform field alone: {'PASS' if k2 else 'FAIL'}; K3 EFE-limit boost {bst:.4f} in [{nue*(1+Le):.4f}, {nue:.4f}] (linear theory nu_e(1+L_e/3) = {nue*(1+Le/3):.4f}) -> {'PASS' if k3 else 'FAIL'}")
res = {}
for foot, a0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
    for kname, nu in KER.items():
        for lab, fac in (("Q1", 1.0), ("Q2", 0.5), ("Q3", 0.25)):
            pulls, boosts, need = [], [], []
            for lm, (lmb, elo, ehi), R in zip(mstar, mbg, rsat):
                Ms = 10 ** lm; Mb = 1.2 * Ms; ret = 0.13 * (0.1200 / 0.02237) * Mb; mb = 10 ** lmb
                rbg = (mb / (4 * math.pi * rho_h(R))) ** (1 / 3)
                gobs = G * Mh(R) * Msun / (R * Mpc) ** 2            # the cluster's measured-mass field (observed)
                ge = fac * (gobs if FIELD == "orig" else yN_of(KER_INV[kname], gobs / a0) * a0)   # CW3: the only change
                Mtot = Mb + mph_exact(Mb * Msun, rbg * Mpc, ge, a0, nu) / Msun + ret
                sig = 0.5 * (elo + ehi); pulls.append((lmb - math.log10(Mtot)) / sig)
                boosts.append((Mtot - ret) / Mb); need.append((mb - ret) / Mb)
            z = np.array(pulls); X2 = float((z ** 2).sum()); p = float(chi2.sf(X2, 5))
            res[f"{foot}|{kname}|{lab}"] = dict(chi2=X2, p=p, pulls=z.tolist(), boost=boosts, need=need)
            P(f"{foot:9s} {kname:7s} {lab} (g_e x{fac}): chi2 {X2:6.1f}/5 p {p:.2g} | boost M/M_b {np.round(boosts,2).tolist()} vs needed {np.round(need,1).tolist()}")
def excl(lab): return all(res[k]["p"] < 0.01 for k in res if k.endswith(lab))
anyQ1 = any(res[k]["p"] > 0.01 for k in res if k.endswith("Q1"))
if anyQ1: v = "SURVIVES"
elif excl("Q1") and excl("Q2"): v = "FORCE+EFE EXCLUDED (robust)"
else: v = "FRAGILE"
P(f"VERDICT: {v}")
json.dump(dict(field=FIELD, mutate=MUT, K=[bool(k1), bool(k2), bool(k3)], res=res, verdict=v), open(os.path.join(HERE, f"cfg478_cw3{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg478_cw3{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if (k1 and k2 and k3) else 1)
