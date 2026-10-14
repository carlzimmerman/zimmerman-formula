"""CFG779 -- FRB baryon census vs black-hole dark energy eating baryons (criteria FROZEN_CRITERIA.md, 25f2c4548).
Likelihood: CFG632's (authors' eq. 1, host marginalised over their flat box), imported read-only. Mean DM_cosmic = B x the record's
<DM>_F (BBN Omega_b h^2, MD14 f_d); scatter = census PRIMARY sigma(z) x A with lnA free and marginalised; B fitted.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg779.py   (CFG779_MUTATE=1: mock controls B = 1 and B = 0.43).  < 1.5 GB.
kappa = 1/2 FITTED; not theory closed.
"""
import json
import math
import os
import sys
import time

import numpy as np
from scipy import integrate

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CFG632_frb_dm_variance"))
import cfg632_fit as F  # noqa: E402  (read-only import; its main() is guarded)

MUT = os.environ.get("CFG779_MUTATE") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = []
T0 = time.time()


def P(s=""):
    print(s, flush=True)
    OUT.append(str(s))


LNB = np.arange(-1.5, 0.7 + 1e-9, 0.02)
LNB_C = np.arange(-1.5, 0.7 + 1e-9, 0.05)          # mocks: coarser grids (numerical choice, disclosed)
LNA_C = np.arange(-1.0, 1.0 + 1e-9, 0.1)


def loglike_B(dm, z, mean, sig, hm, lnB, lnA, mwh=50.0):
    """log L[lnB, lnA, host] summed over FRBs (CFG632's per-FRB integral, mean scaled by B)."""
    nB, nA, nH = len(lnB), len(lnA), len(F.MUf)
    tot = np.zeros((nB, nA, nH))
    sA = np.exp(lnA)
    for i, (d, zz) in enumerate(zip(dm, z)):
        x, w, H = hm[i]
        dc = np.maximum(d - x - mwh, 1e-300)
        pos = (d - x - mwh) > 0
        for b, lb in enumerate(lnB):
            m = mean[i] * math.exp(lb)
            v = (sA * sig[i]) ** 2
            sl = np.sqrt(np.log1p(v / m ** 2))[:, None]
            ml = np.log(m ** 2 / np.sqrt(m ** 2 + v))[:, None]
            C = np.where(pos[None, :], np.exp(-0.5 * ((np.log(dc)[None, :] - ml) / sl) ** 2) / (dc[None, :] * sl * math.sqrt(2 * math.pi)), 0.0)
            C = np.clip(np.nan_to_num(C), 1e-300, None)
            with np.errstate(all="ignore"):
                L = (C * w) @ H
            tot[b] += np.log(np.maximum(L, 1e-300))
    return tot


def post_B(LL, lnB):
    mx = LL.max()
    Pb = np.exp(LL - mx).sum(axis=(1, 2))
    Pb /= Pb.sum()
    c = np.cumsum(Pb)
    q = lambda p: float(np.interp(p, c, lnB))
    return q(0.5), q(0.16), q(0.84)


# ---------------------------------------------------------------- s_b(z) histories (MD14, z_start 8, flat Omega_m 0.308)
OM, h = 0.308, 0.70
psi = lambda zz: 0.015 * (1 + zz) ** 2.7 / (1 + ((1 + zz) / 2.9) ** 5.6)
dtdz = lambda zz: 1 / ((1 + zz) * math.sqrt(OM * (1 + zz) ** 3 + 1 - OM))
Dz = lambda zz: integrate.quad(lambda x: psi(x) * dtdz(x), zz, 8.0, limit=200)[0]
D0 = Dz(0.0)
ZZ = np.linspace(0, 2.5, 251)
FC = np.array([Dz(zz) / D0 for zz in ZZ])           # fraction of all conversion that happened before z


def s_b(zz, s0):
    return 1 - (1 - s0) * np.interp(zz, ZZ, FC)


def B_pred(zi, s0):
    zg = np.linspace(0, zi, 200)
    wgt = (1 + zg) / np.sqrt(OM * (1 + zg) ** 3 + 1 - OM)
    return float(np.trapz(s_b(zg, s0) * wgt, zg) / np.trapz(wgt, zg)) if zi > 0 else s0


dm, z, names = F.load_sample("extended")
hm = F.host_matrices(dm, z)
meanF = F.mean_dm(z)
RES = {"lane": "CFG779", "mutate": MUT, "N": len(z)}

if MUT:
    rng = np.random.default_rng(779)
    sig = F.sig_interp("canonical|census|lo|H|DIFF", z)
    med = {}
    for Btrue in (1.0, 0.43):
        lb = []
        for k in range(50):
            dmk = F.draw_mock(rng, z, meanF * Btrue, sig)
            hk = F.host_matrices(dmk, z)
            m, lo, hi = post_B(loglike_B(dmk, z, meanF, sig, hk, LNB_C, LNA_C), LNB_C)
            lb.append((m, lo, hi))
        lb = np.array(lb)
        med[Btrue] = dict(median=float(np.median(lb[:, 0])), sigma=float(np.median(lb[:, 2] - lb[:, 1]) / 2))
        P(f"MUTATE mocks B = {Btrue}: median lnB {med[Btrue]['median']:+.3f} (true {math.log(Btrue):+.3f}), typical sigma {med[Btrue]['sigma']:.3f}  ({time.time() - T0:.0f} s)")
    sep = abs(med[1.0]["median"] - med[0.43]["median"]) / max(med[1.0]["sigma"], 1e-9)
    ok1 = abs(med[1.0]["median"]) <= 0.1
    P(f"MUTATE: B=1 recovered within 0.1: {ok1}; B=0.43 vs 1 separated by {sep:.1f} sigma -> {'DIAGNOSTIC' if sep >= 3 else 'NOT DIAGNOSTIC'}")
    RES["mocks"] = med
    json.dump(RES, open(os.path.join(HERE, f"cfg779_results{TAG}.json"), "w"), indent=1)
    open(os.path.join(HERE, f"cfg779{TAG}.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(1)

# ---------------------------------------------------------------- K2 injection (B = 0.5), coarse grid
rng = np.random.default_rng(2)
sigc = F.sig_interp("canonical|census|lo|H|DIFF", z)
inj = []
for k in range(50):
    dmk = F.draw_mock(rng, z, meanF * 0.5, sigc)
    inj.append(post_B(loglike_B(dmk, z, meanF, sigc, F.host_matrices(dmk, z), LNB_C, LNA_C), LNB_C)[0])
k2 = abs(np.median(inj) - math.log(0.5)) <= 0.1
P(f"K2 injection B = 0.5 (50 mocks): median lnB {np.median(inj):+.3f} vs {math.log(0.5):+.3f} -> {'PASS' if k2 else 'FAIL'}  ({time.time() - T0:.0f} s)")
RES["K2"] = dict(median=float(np.median(inj)), ok=bool(k2))

# ---------------------------------------------------------------- predictions
Bp = {"P0 (no conversion)": np.ones(len(z)), "P1 (MD14 conserved, s_b0 0.43)": np.array([B_pred(zi, 0.4307) for zi in z]),
      "P2 (Croker-like, s_b0 0.70)": np.array([B_pred(zi, 0.70) for zi in z])}
P("\npredicted sightline multipliers (median over the sample): " + "; ".join(f"{k} {np.median(v):.3f}" for k, v in Bp.items()))
for zq in (0.0, 0.5, 1.0, 2.0):
    P(f"  s_b(z={zq}): P1 {s_b(zq, 0.4307):.3f}  P2 {s_b(zq, 0.70):.3f}")

# ---------------------------------------------------------------- fits
for foot in F.FOOTS:
    key = f"{foot}|census|lo|H|DIFF"
    sig = F.sig_interp(key, z)
    LL = loglike_B(dm, z, meanF, sig, hm, LNB, F.LNA)
    m, lo, hi = post_B(LL, LNB)
    i0 = int(np.argmin(np.abs(LNB)))
    mA, loA, hiA, _ = F.posterior_lnA(LL[i0])
    ref = json.load(open(os.path.join(HERE, "..", "CFG632_frb_dm_variance", "cfg632_fit.json")))
    P(f"\n{foot}: lnB {m:+.3f} ({lo:+.3f}, {hi:+.3f})  B = {math.exp(m):.3f}  [{math.exp(lo):.3f}, {math.exp(hi):.3f}]   ({time.time() - T0:.0f} s)")
    P(f"  K1 slice B = 1: lnA {mA:+.3f} (CFG632 PRIMARY reported -0.057 canonical / -0.132 alt)")
    RES[foot] = dict(lnB=m, p16=lo, p84=hi, K1_lnA=mA)
    for k, v in Bp.items():
        lp = math.log(float(np.median(v)))
        Zs = (m - lp) / max((m - lo) if m > lp else (hi - m), 1e-9)
        cls = "EXCLUDED" if abs(Zs) >= 3 else ("TENSION" if abs(Zs) >= 2 else "CONSISTENT")
        RES[foot][k] = dict(lnB_pred=lp, Z=Zs, cls=cls)
        P(f"  {k:32s}: B_pred {math.exp(lp):.3f} -> Z {Zs:+.2f}  {cls}")
json.dump(RES, open(os.path.join(HERE, "cfg779_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg779.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0)
