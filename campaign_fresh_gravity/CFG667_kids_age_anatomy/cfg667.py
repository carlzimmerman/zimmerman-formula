#!/usr/bin/env python3
"""CFG667 (FROZEN_CRITERIA.md, fd97db64b): what is the KiDS age signal?  Raw lensing only.
Part A: radial shape of the raw OLD/YOUNG ESD log-ratio across K9 (GLS slope, patch jackknife).
Part B: independent Taylor+11 colour-M/L masses (LePhare rest-frame g, i) -> re-matched tertiles, K9 amplitude.
Masks and estimator: CFG585's head and CFG531's esd_loo executed unedited, CFG589's stratified tertiles (as CFG700).
No law, kappa, footing or model.  Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg667.py
CFG667_MUTATE=1 CFG667_M=M1|M2 -> _MUTATE outputs, exit 1 iff the tooth bites."""
import os, io, json, math, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); ROOT = os.path.dirname(LANES)
MUT = os.environ.get("CFG667_MUTATE", "0") == "1"; MODE = os.environ.get("CFG667_M", "") if MUT else ""
TAG = f"_MUTATE{MODE}" if MUT else ""
OUT, RES = [], {"lane": "CFG667", "criteria": "fd97db64b", "mutate": MUT, "mode": MODE}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


for v in ("CFG585_MUTATE", "CFG531_MUTATE"):
    os.environ.pop(v, None)
path = os.path.join(LANES, "CFG585_age_settling", "cfg585_age.py")
ns = {"__file__": path, "__name__": "head"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(open(path).read().split('P("=" * 100)')[0], path, "exec"), ns)
U, F30, TYP, LMSL, esd_loo, NPATCH = (ns[k] for k in ("U", "F30", "TYP", "LMSL", "esd_loo", "NPATCH"))
Lp, o, ix = ns["Lp"], ns["o"], ns["ix"]
G = esd_loo.__globals__
WG0 = G["WG"].copy()
C = F30 & (TYP == 1)
K9 = list(range(6, 15))


def tertiles(mass):
    qb = np.quantile(mass[C], np.linspace(0, 1, 11)); qb[-1] += 1e-9
    ter = np.full(len(U), -1)
    for i in range(10):
        idx = np.where(C & (mass >= qb[i]) & (mass < qb[i + 1]))[0]
        dc = U[idx] - np.median(U[idx]); od = np.argsort(dc, kind="stable"); n = len(idx)
        for k in range(3):
            ter[idx[od[k * n // 3:(k + 1) * n // 3]]] = k
    return (ter == 0) & C, (ter == 2) & C          # YOUNG, OLD


dall, Call, _ = esd_loo(C)
W = 1.0 / np.diag(Call)


def k9_amp(mo, my):
    do, _, Lo = esd_loo(mo); dy, _, Ly = esd_loo(my)
    a = math.log10((W[K9] @ do[K9]) / (W[K9] @ dy[K9]))
    al = np.log10((Lo[:, K9] @ W[K9]) / (Ly[:, K9] @ W[K9]))
    sj = math.sqrt((NPATCH - 1) / NPATCH * ((al - al.mean()) ** 2).sum())
    return a, sj, do, dy, Lo, Ly


YOUNG, OLD = tertiles(LMSL)
if MODE == "M1":
    G["WG"] = WG0.copy(); G["WG"][OLD] *= 0.8
elif MODE == "M2":
    G["WG"] = WG0.copy(); G["WG"][np.ix_(np.where(OLD)[0], [12, 13, 14])] *= 1.5
A, sA, do, dy, Lo, Ly = k9_amp(OLD, YOUNG)
P(f"CFG667  KiDS age-signal anatomy (raw lensing)  {('MUTATE ' + MODE) if MUT else 'PRIMARY'}")
P(f"C1 K9 amplitude (CFG700 reproduction): A = {A:+.6f} +- {sA:.4f} (jackknife)  [CFG700: +0.166]")
RES["C1"] = dict(A=A, sA=sA)

# ---------------------------------------------------------------- Part A: radial shape
good = [k for k in K9 if do[k] > 0 and dy[k] > 0 and np.all(Lo[:, k] > 0) and np.all(Ly[:, k] > 0)]
ell = np.log10(do[good] / dy[good])
lr = np.log10(Lo[:, good] / Ly[:, good])
dev = lr - lr.mean(0)
Cv = (NPATCH - 1) / NPATCH * dev.T @ dev
cond = float(np.linalg.cond(Cv))
use_diag = cond > 1e8
Ci = np.diag(1 / np.diag(Cv)) if use_diag else np.linalg.inv(Cv)
X = np.column_stack([np.ones(len(good)), (np.array(good) - 10) / 8.0])
Fm = X.T @ Ci @ X; beta = np.linalg.solve(Fm, X.T @ Ci @ ell); cov = np.linalg.inv(Fm)
S, sS = float(beta[1]), float(math.sqrt(cov[1, 1])); ZS = S / sS
chi2 = float((ell - X @ beta) @ Ci @ (ell - X @ beta))
clsA = "INNER-CONCENTRATED" if (S > 0 and ZS >= 2) else ("OUTER-RISING" if (S < 0 and ZS <= -2) else "NOT DECIDED")
P(f"\nPart A: bins used {good} (of K9); jackknife covariance condition {cond:.2e} -> {'diagonal' if use_diag else 'full'}")
P("   per-bin log10 ratio (k: value +- jackknife sigma): " +
  ", ".join(f"{k}: {v:+.3f}+-{math.sqrt(Cv[i, i]):.3f}" for i, (k, v) in enumerate(zip(good, ell))))
P(f"   slope S (inner minus outer across K9) = {S:+.4f} +- {sS:.4f}  Z = {ZS:+.2f};  chi2 {chi2:.2f} / {len(good) - 2} dof  -> {clsA}")
RES["A"] = dict(bins=good, ell=ell.tolist(), sig=np.sqrt(np.diag(Cv)).tolist(), cond=cond, diag=bool(use_diag), S=S, sS=sS, Z=ZS,
                chi2=chi2, cls=clsA)

# ---------------------------------------------------------------- Part B: Taylor+11 masses
gabs = np.array(Lp["MAG_ABS_g"], "f8")[o[ix]]; iabs = np.array(Lp["MAG_ABS_i"], "f8")[o[ix]]
LMT = -0.68 + 0.70 * (gabs - iabs) + 0.4 * (4.58 - iabs)
fin = np.isfinite(LMT)
d_old = float(np.median((LMT - LMSL)[OLD & fin])); d_young = float(np.median((LMT - LMSL)[YOUNG & fin]))
B1 = d_old - d_young
P(f"\nPart B1: median(log M*_Taylor - log M*_LePhare): OLD {d_old:+.4f}, YOUNG {d_young:+.4f} -> OLD - YOUNG = {B1:+.4f} dex")
G["WG"] = WG0.copy()
Cfin = C & fin
YT, OT = tertiles(np.where(fin, LMT, -99.0))
YT &= Cfin; OT &= Cfin
AT, sAT, *_ = k9_amp(OT, YT)
ZT = AT / sAT
clsB = "M* BIAS EXPLAINS" if (AT <= 0.05 and abs(ZT) < 1) else ("SIGNAL PERSISTS" if (AT >= 0.12 and ZT >= 2) else "PARTIAL")
mT_o, mT_y = float(np.median(LMT[OT])), float(np.median(LMT[YT]))
mL_o, mL_y = float(np.median(LMSL[OT])), float(np.median(LMSL[YT]))
P(f"Part B2: tertiles at fixed Taylor mass: N {int(OT.sum())}/{int(YT.sum())}; median log M*_T {mT_o:.3f}/{mT_y:.3f}; "
  f"LePhare {mL_o:.3f}/{mL_y:.3f}")
P(f"   K9 amplitude A_T = {AT:+.4f} +- {sAT:.4f}  Z = {ZT:+.2f}  -> {clsB}")
RES["B"] = dict(B1=B1, d_old=d_old, d_young=d_young, A_T=AT, sA_T=sAT, Z_T=ZT, cls=clsB,
                med=dict(LMT_old=mT_o, LMT_young=mT_y, LMSL_old=mL_o, LMSL_young=mL_y))

if clsA == "OUTER-RISING" and clsB == "SIGNAL PERSISTS":
    lab = "EXTRA MASS LIKELY"
elif (clsA == "INNER-CONCENTRATED" or clsB == "M* BIAS EXPLAINS") and not (clsA == "OUTER-RISING" or clsB == "SIGNAL PERSISTS"):
    lab = "STELLAR-MASS ARTEFACT LIKELY"
else:
    lab = "UNDECIDED"
rc = 0
if MUT:
    J = json.load(open(os.path.join(HERE, "cfg667_results.json")))
    if MODE == "M1":
        bite = abs((A - J["C1"]["A"]) - math.log10(0.8)) <= 0.002 and abs(S - J["A"]["S"]) <= 0.002
    else:
        bite = S > 0 and ZS >= 2
    RES["tooth_bites"] = bool(bite); P(f"\nMUTATE {MODE}: tooth bites: {bite}"); rc = 1 if bite else 0
else:
    RES["label"] = lab; P(f"\nCOMBINED LABEL: {lab}  (A: {clsA}; B: {clsB})")
json.dump(RES, open(os.path.join(HERE, f"cfg667_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg667{TAG}.out"), "w").write("\n".join(OUT) + "\n")
raise SystemExit(rc)
