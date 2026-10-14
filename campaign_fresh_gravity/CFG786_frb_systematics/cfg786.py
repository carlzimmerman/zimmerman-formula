"""CFG786 -- CFG779's FRB exclusion under its own assumptions.  Criteria: FROZEN_CRITERIA.md (7ca119528).
Self-contained copy of CFG779's B-fit (same likelihood: CFG632's, imported read-only).  Run after T1x:
  OMP_NUM_THREADS=1 nice -n 10 python3 cfg786.py   (CFG786_MUTATE=1: mocks B = 0.71 under the worst-case settings).
kappa = 1/2 FITTED; not theory closed.
"""
import json
import math
import os
import sys

import numpy as np
from scipy import integrate

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CFG632_frb_dm_variance"))
import cfg632_fit as F  # noqa: E402

MUT = os.environ.get("CFG786_MUTATE") == "1"
OUT = []


def P(s=""):
    print(s, flush=True)
    OUT.append(str(s))


LNB = np.arange(-1.5, 0.7 + 1e-9, 0.02)
LNA = F.LNA                                        # same lnA grid as CFG779 (K1 exactness)


def loglike_B(dm, z, mean, sig, hm, mwh=50.0):
    nH = len(F.MUf)
    tot = np.zeros((len(LNB), len(LNA), nH)); sA = np.exp(LNA)
    for i, (d, zz) in enumerate(zip(dm, z)):
        x, w, H = hm[i]
        dc = np.maximum(d - x - mwh, 1e-300); pos = (d - x - mwh) > 0
        for b, lb in enumerate(LNB):
            m = mean[i] * math.exp(lb); v = (sA * sig[i]) ** 2
            sl = np.sqrt(np.log1p(v / m ** 2))[:, None]; ml = np.log(m ** 2 / np.sqrt(m ** 2 + v))[:, None]
            C = np.where(pos[None, :], np.exp(-0.5 * ((np.log(dc)[None, :] - ml) / sl) ** 2) / (dc[None, :] * sl * math.sqrt(2 * math.pi)), 0.0)
            C = np.clip(np.nan_to_num(C), 1e-300, None)
            with np.errstate(all="ignore"):
                L = (C * w) @ H
            tot[b] += np.log(np.maximum(L, 1e-300))
    return tot


def post(LL):
    Pb = np.exp(LL - LL.max()).sum(axis=(1, 2)); Pb /= Pb.sum(); c = np.cumsum(Pb)
    q = lambda p: float(np.interp(p, c, LNB))
    return q(0.5), q(0.16), q(0.84)


def set_host(mu_lo, mu_hi, s_lo, s_hi):
    F.MU = np.linspace(mu_lo, mu_hi, 41); F.SH = np.linspace(s_lo, s_hi, 33)
    g1, g2 = np.meshgrid(F.MU, F.SH, indexing="ij"); F.MUf, F.SHf = g1.ravel(), g2.ravel()


# P2 sightline multiplier (CFG779's construction, MD14 shape, s_b0 0.70)
OM = 0.308
psi = lambda zz: 0.015 * (1 + zz) ** 2.7 / (1 + ((1 + zz) / 2.9) ** 5.6)
dtdz = lambda zz: 1 / ((1 + zz) * math.sqrt(OM * (1 + zz) ** 3 + 1 - OM))
D0 = integrate.quad(lambda x: psi(x) * dtdz(x), 0, 8.0)[0]
ZZ = np.linspace(0, 2.5, 251); FC = np.array([integrate.quad(lambda x: psi(x) * dtdz(x), zz, 8.0)[0] / D0 for zz in ZZ])


def Bpred(zs, s0):
    out = []
    for zi in zs:
        zg = np.linspace(0, max(zi, 1e-4), 200); w = (1 + zg) / np.sqrt(OM * (1 + zg) ** 3 + 1 - OM)
        sb = 1 - (1 - s0) * np.interp(zg, ZZ, FC)
        out.append(float(np.trapz(sb * w, zg) / np.trapz(w, zg)))
    return float(np.median(out))


def run(label, which="extended", hfac=1.0, imf="chabrier", host=(4.0, 6.0, 0.2, 1.0), obh=1.0, mock_B=None, seed=0):
    set_host(*host)
    dm, z, _ = F.load_sample(which)
    mean = F.mean_dm(z, imf) * (0.70 / (0.70 * hfac)) * obh
    sig = F.sig_interp("canonical|census|lo|H|DIFF", z)
    if mock_B is not None:
        dm = F.draw_mock(np.random.default_rng(seed), z, mean * mock_B, sig)
    m, lo, hi = post(loglike_B(dm, z, mean, sig, F.host_matrices(dm, z)))
    bp = math.log(Bpred(z, 0.70))
    Z = (m - bp) / max(m - lo, 1e-9)
    if mock_B is None:
        P(f"  {label:34s}: lnB {m:+.3f} ({lo:+.3f}, {hi:+.3f}); P2 B_pred {math.exp(bp):.3f} -> Z {Z:+.2f}")
    return dict(m=m, lo=lo, hi=hi, Z=Z, Bp=math.exp(bp))


P("CFG786  FRB exclusion vs its assumptions" + ("  [MUTATE]" if MUT else ""))
if MUT:
    rec = [run("mock", hfac=0.73 / 0.70, imf="salpeter", host=(3.5, 6.5, 0.1, 1.3), obh=1.0, mock_B=0.71, seed=s)["m"] for s in range(30)]
    P(f"  MUTATE mocks B = 0.71 under V6-type settings: median lnB {np.median(rec):+.3f} vs {math.log(0.71):+.3f} -> {'bites' if abs(np.median(rec) - math.log(0.71)) <= 0.1 else 'DID NOT BITE'}")
    open(os.path.join(HERE, "cfg786_MUTATE.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1)

R = {}
R["V0 baseline"] = run("V0 baseline (CFG779)")
k1 = abs(R["V0 baseline"]["m"] - 0.062) <= 0.005
P(f"  K1 reproduces CFG779 lnB +0.062: {k1}")
R["V1 h 0.67"] = run("V1 h = 0.67", hfac=0.67 / 0.70)
R["V1 h 0.73"] = run("V1 h = 0.73", hfac=0.73 / 0.70)
R["V2 Salpeter f_d"] = run("V2 Salpeter f_d", imf="salpeter")
R["V3 wide host box"] = run("V3 wide host box", host=(3.5, 6.5, 0.1, 1.3))
R["V4 Obh2 +2sig"] = run("V4 Omega_b h^2 +2 sigma", obh=1 + 2 * 0.0011 / 0.02218)
R["V4 Obh2 -2sig"] = run("V4 Omega_b h^2 -2 sigma", obh=1 - 2 * 0.0011 / 0.02218)
R["V5 strict sample"] = run("V5 Sharma 'yes' only", which="strict")
# V6: each assumption at the end that LOWERS Z (worst for the exclusion), chosen from V1-V4 (criteria intent; parenthetical
# in the frozen file may name the opposite ends - disclosed in the README)
hw = 0.67 if R["V1 h 0.67"]["Z"] < R["V1 h 0.73"]["Z"] else 0.73
imfw = "salpeter" if R["V2 Salpeter f_d"]["Z"] < R["V0 baseline"]["Z"] else "chabrier"
hostw = (3.5, 6.5, 0.1, 1.3) if R["V3 wide host box"]["Z"] < R["V0 baseline"]["Z"] else (4.0, 6.0, 0.2, 1.0)
obw = 1 + 2 * 0.0011 / 0.02218 if R["V4 Obh2 +2sig"]["Z"] < R["V4 Obh2 -2sig"]["Z"] else 1 - 2 * 0.0011 / 0.02218
R["V6 worst combined"] = run(f"V6 worst (h {hw}, {imfw}, host {hostw[:2]}, obh x{obw:.3f})", hfac=hw / 0.70, imf=imfw, host=hostw, obh=obw)
# escape route (declared analytic): converted baryons drawn first from the condensed budget fc
P("\n  escape route (as declared): condensed budget fc absorbs part of P2's 30% depletion; diffuse deficit = (0.30 - fc)/f_d0")
esc = {}
for fc in (0.12, 0.24):
    Bes = 1 - max(0.30 - fc, 0) / 0.93
    m, lo = R["V0 baseline"]["m"], R["V0 baseline"]["lo"]
    Zs = (m - math.log(Bes)) / max(m - lo, 1e-9)
    esc[str(fc)] = dict(B=Bes, Z=Zs)
    P(f"   fc {fc}: B_pred,escape {Bes:.3f} -> Z {Zs:+.2f}")
Zs_all = [v["Z"] for v in R.values()]
minZ = min(Zs_all); minZe = min(v["Z"] for v in esc.values())
cls = "ROBUST" if (minZ >= 3 and minZe >= 3) else ("WEAKENED" if min(minZ, minZe) >= 2 else "NOT ROBUST")
P(f"\n  min Z over variants {minZ:+.2f}; over escape {minZe:+.2f} -> CLASS {cls}")
json.dump(dict(variants=R, escape=esc, K1=k1, cls=cls), open(os.path.join(HERE, "cfg786_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg786.out"), "w").write("\n".join(OUT) + "\n")
