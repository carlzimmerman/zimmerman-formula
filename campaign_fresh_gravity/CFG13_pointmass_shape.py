#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG13 -- CFG9's PRINCIPLE ON ITS OWN TERMS: is the transition shape P2's (beta = 1) where the baryons look like a point mass?

WHY.  CFG9 proved that a cold component locally virialized around a POINT mass makes the law exactly P2 (beta = 1 in the family
nu_beta = (1 + y^-beta)^(1/2beta)).  CFG4's committed shape bootstrap, applied to every SPARC point, excludes beta = 1 (best 0.48
[0.40, 0.59] canonical, 0.55 [0.45, 0.77] alt; P2 loses in 1000/1000 resamples).  But the theorem fixes the shape only where the
baryons are interior.  This lane splits SPARC's points by how much baryonic mass lies outside them and repeats CFG4's bootstrap
on each part.

THE SPLIT (declared; the selection uses Upsilon_disk = 0.5, bulge 0.7, fixed before any fit).  Spherical-equivalent baryonic mass
M_b(R) = V_bar(R)^2 R / G.  A point at R_i is in the POINT-MASS regime if the galaxy's measured baryonic mass beyond it is at most
10%: M_b(R_last) / M_b(R_i) <= 1.10.  It is EMBEDDED if M_b(R_last) / M_b(R_i) >= 1.5.

THE STATISTIC.  CFG4 H2/H3's exactly (the record's weighted rms of log g_obs/g_pred; one global Upsilon profiled on 0.30-1.20;
beta on CFG4's 49-point grid; the galaxy bootstrap with CFG4's seed, 1000 resamples) restricted to the subset's points.

PRE-DECLARED (before this script's first run)
  C1  CONTROL  with every point kept, CFG4 H3's committed best beta, U, rms(beta = 1), 95% interval and P2-worse fraction are
      reproduced exactly (both footings).
  C2  POWER  synthetic nu_mono data (CFG4's nu_mono best Upsilon; a per-galaxy offset N(0, 0.08 dex) and per-point N(0, 0.05 dex),
      seed 13) restricted to the POINT-MASS subset give a 95% interval that EXCLUDES beta = 1 (both footings).  If this fails the
      subset cannot tell P2 from the record's kernel and H1 is reported as NO POWER.
  C3  BIAS  synthetic P2 data (P2's best Upsilon, the same noise) in the point-mass subset give an interval CONTAINING beta = 1.
  H1  [HEADLINE; MUTATE must fail] CFG9's principle is NOT falsified: the real point-mass subset's 95% interval contains beta = 1,
      both footings.  Outcome labels: SUPPORTED if it contains 1 and excludes the full-sample best beta (0.48 / 0.55); NO POWER if it
      contains both (or C2 failed); FALSIFIED if it excludes 1.
  H2  the shape preference lives inside the baryons: the EMBEDDED subset's 95% interval excludes beta = 1, both footings.
  R1  (reported) subset sizes, their median g_bar/a0, and the best beta and rms per subset.
MUTATE=1: the real g_obs of the point-mass subset are replaced by the synthetic nu_mono data for H1 -- H1 must FAIL (rc = 1) if the
subset has power.
Run: python3 campaign_fresh_gravity/CFG13_pointmass_shape.py   (MUTATE=1 for the control; ~1 min)
"""
import os, sys, math, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C7
C = C7.C4
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C7.Report("CFG13_pointmass_shape", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the point-mass subset's data replaced by synthetic nu_mono data in H1 -- H1 must FAIL ***")
np.seterr(all="ignore")
GL = json.load(open(os.path.join(HERE, "CFG4_galaxy_law_results.json")))["numbers"]
A0 = C.A0

# ================================================================================================ CFG4 H2/H3's statistic, exactly
GAL = C.load_sparc()
NG = len(GAL)
UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2)
KPC_S = 3.0857e19
Rm = np.concatenate([g["R"] for g in GAL]) * KPC_S
Vo = np.concatenate([g["Vobs"] for g in GAL])
eV = np.concatenate([g["eV"] for g in GAL])
Vg = np.concatenate([g["Vgas"] for g in GAL])
Vd = np.concatenate([g["Vdisk"] for g in GAL])
Vb = np.concatenate([g["Vbul"] for g in GAL])
GI = np.concatenate([np.full(len(g["R"]), i) for i, g in enumerate(GAL)])
VB2 = np.sign(Vg)[:, None] * Vg[:, None] ** 2 + UPS[None, :] * Vd[:, None] ** 2 + 1.4 * UPS[None, :] * Vb[:, None] ** 2
GB = VB2 * 1e6 / Rm[:, None]
GO_REAL = ((Vo * 1e3) ** 2 / Rm)[:, None] * np.ones_like(GB)
OK = (GB > 0) & (GO_REAL > 0) & np.isfinite(GB) & np.isfinite(GO_REAL) & (Vo > 0)[:, None]
WPT = (1.0 / (np.clip(eV, 1, None) / np.clip(Vo, 1, None)) ** 2)
WW = np.where(OK, WPT[:, None], 0.0)
ONEHOT = np.zeros((NG, len(Rm)))
ONEHOT[GI, np.arange(len(Rm))] = 1.0
BETAS = np.round(np.geomspace(0.25, 6.0, 49), 4)
J1 = int(np.argmin(np.abs(BETAS - 1.0)))
rng = np.random.default_rng(20260927)
NB = 1000
WB = rng.multinomial(NG, np.full(NG, 1.0 / NG), size=NB).astype(float)


def shape_fit(GO, mask, f):
    """CFG4 H3 on the points in `mask` (per point, bool): best beta, U, rms(beta=1), bootstrap intervals."""
    w = WW * mask[:, None]
    SS, WS = [], []
    for b in BETAS:
        with np.errstate(all="ignore"):
            r_ = np.log10(np.where(OK, GO, 1.0)) - np.log10(np.where(OK, C.nu_beta(np.where(OK, GB, 1.0) / A0[f], b) * np.where(OK, GB, 1.0), 1.0))
        SS.append(ONEHOT @ (w * r_ ** 2)); WS.append(ONEHOT @ w)
    SS = np.stack(SS); WS = np.stack(WS)
    mse = SS.sum(1) / WS.sum(1)                                                               # (nbeta, NU)
    full = np.sqrt(mse.min(axis=1))
    jb = int(np.argmin(full)); ub = float(UPS[int(np.argmin(mse[jb]))])
    num = np.einsum("bg,kgu->bku", WB, SS); den = np.einsum("bg,kgu->bku", WB, WS)
    msb = (num / den).min(axis=2)
    bb = BETAS[np.argmin(msb, axis=1)]
    lo95, hi95 = np.percentile(bb, [2.5, 97.5])
    d1 = np.sqrt(msb[:, J1]) - np.sqrt(msb.min(axis=1))
    return dict(best_beta=float(BETAS[jb]), best_rms=float(full[jb]), U_best=ub, rms_beta1=float(full[J1]),
                ci95=[float(lo95), float(hi95)], P2_worse_frac=float(np.mean(d1 > 0)), n_pts=int((mask & OK[:, 0]).sum()),
                n_gal=int(len(np.unique(GI[mask]))))


# ================================================================================================ C1
R.banner("C1  CONTROL: CFG4 H3's committed shape bootstrap, every point kept")
ALL = np.ones(len(Rm), bool)
c1 = {}
for f in C.FOOTS:
    mine = shape_fit(GO_REAL, ALL, f); ref = GL["H3"][f]
    c1[f] = (mine, ref)
    P(f"    {f:9s}: best beta {mine['best_beta']} (CFG4 {ref['best_beta']}), U {mine['U_best']} ({ref['U_best']}), rms(1) "
      f"{mine['rms_beta1']:.10f} ({ref['rms_beta1']:.10f}), 95% {mine['ci95']} ({ref['ci95']}), P2 worse {mine['P2_worse_frac']} ({ref['P2_worse_frac']})")
ok1 = all(m["best_beta"] == r["best_beta"] and m["U_best"] == r["U_best"] and abs(m["rms_beta1"] - r["rms_beta1"]) < 1e-12 and
          np.allclose(m["ci95"], r["ci95"]) and m["P2_worse_frac"] == r["P2_worse_frac"] for m, r in c1.values())
check("C1 CONTROL: CFG4 H3's committed best beta, Upsilon, rms(beta = 1), 95% interval and P2-worse fraction reproduced exactly",
      "; ".join(f"{f}: best {m['best_beta']}, 95% [{m['ci95'][0]:.4f}, {m['ci95'][1]:.4f}]" for f, (m, r) in c1.items()), ok1)

# ================================================================================================ the split
Vb2s = np.sign(Vg) * Vg ** 2 + 0.5 * Vd ** 2 + 0.7 * Vb ** 2
Mb = Vb2s * Rm                                                                           # proportional to M_b(<R)
ratio = np.full(len(Rm), np.nan)
off = 0
for g in GAL:
    n = len(g["R"]); sl = slice(off, off + n)
    mb = Mb[sl]
    with np.errstate(all="ignore"):
        ratio[sl] = np.where(mb > 0, mb[-1] / mb, np.nan)
    off += n
PM = np.isfinite(ratio) & (ratio <= 1.10)
EMB = np.isfinite(ratio) & (ratio >= 1.5)
P(f"\n  the split (Upsilon 0.5 for selection): point-mass {int((PM & OK[:, 0]).sum())} points in {len(np.unique(GI[PM]))} galaxies; "
  f"embedded {int((EMB & OK[:, 0]).sum())} points in {len(np.unique(GI[EMB]))} galaxies; rest {int((~PM & ~EMB).sum())}")

# ================================================================================================ synthetic data (power, bias, MUTATE)
srng = np.random.default_rng(13)
goff = srng.normal(0.0, 0.08, NG)
pnoise = srng.normal(0.0, 0.05, len(Rm))


def synthetic(kname, f):
    U = GL["H2"][f"{f}|{kname}"]["U"]; iu = int(np.argmin(np.abs(UPS - U)))
    gb = GB[:, iu]
    with np.errstate(all="ignore"):
        g = C.KERNELS[kname](gb / A0[f]) * gb * 10 ** (goff[GI] + pnoise)
    return np.where(OK[:, iu], g, GO_REAL[:, 0])[:, None] * np.ones_like(GB)


RES = {}
for f in C.FOOTS:
    syn_m = synthetic("nu_mono", f); syn_p = synthetic("P2", f)
    RES[(f, "C2")] = shape_fit(syn_m, PM, f)
    RES[(f, "C3")] = shape_fit(syn_p, PM, f)
    RES[(f, "PM")] = shape_fit(syn_m if MUTATE else GO_REAL, PM, f)
    RES[(f, "EMB")] = shape_fit(GO_REAL, EMB, f)
    for k in ("C2", "C3", "PM", "EMB"):
        v = RES[(f, k)]
        P(f"    {f:9s} {k:4s}: {v['n_pts']:4d} pts / {v['n_gal']:3d} gal: best beta {v['best_beta']:.2f} (U {v['U_best']:.2f}, rms "
          f"{v['best_rms']:.4f}); 95% [{v['ci95'][0]:.2f}, {v['ci95'][1]:.2f}]; rms(beta=1) {v['rms_beta1']:.4f}; P2 worse in "
          f"{v['P2_worse_frac']:.3f}")
c2 = all(not (RES[(f, "C2")]["ci95"][0] <= 1.0 <= RES[(f, "C2")]["ci95"][1]) for f in C.FOOTS)
check("C2 POWER: synthetic nu_mono data in the point-mass subset exclude beta = 1 at 95% (both footings)",
      "; ".join(f"{f}: [{RES[(f, 'C2')]['ci95'][0]:.2f}, {RES[(f, 'C2')]['ci95'][1]:.2f}]" for f in C.FOOTS), c2)
c3 = all(RES[(f, "C3")]["ci95"][0] <= 1.0 <= RES[(f, "C3")]["ci95"][1] for f in C.FOOTS)
check("C3 BIAS: synthetic P2 data in the point-mass subset contain beta = 1 at 95% (both footings)",
      "; ".join(f"{f}: [{RES[(f, 'C3')]['ci95'][0]:.2f}, {RES[(f, 'C3')]['ci95'][1]:.2f}]" for f in C.FOOTS), c3)
lab = {}
for f in C.FOOTS:
    lo, hi = RES[(f, "PM")]["ci95"]; fb = GL["H3"][f]["best_beta"]
    if not (lo <= 1.0 <= hi):
        lab[f] = "FALSIFIED"
    elif (lo <= fb <= hi) or not c2:
        lab[f] = "NO POWER"
    else:
        lab[f] = "SUPPORTED"
h1 = all(RES[(f, "PM")]["ci95"][0] <= 1.0 <= RES[(f, "PM")]["ci95"][1] for f in C.FOOTS)
check("H1 [HEADLINE] CFG9's principle is not falsified: the point-mass subset's 95% interval contains beta = 1 (both footings)"
      + ("  [MUTATE: synthetic nu_mono data]" if MUTATE else ""),
      "; ".join(f"{f}: [{RES[(f, 'PM')]['ci95'][0]:.2f}, {RES[(f, 'PM')]['ci95'][1]:.2f}] -> {lab[f]}" for f in C.FOOTS), h1)
h2 = all(not (RES[(f, "EMB")]["ci95"][0] <= 1.0 <= RES[(f, "EMB")]["ci95"][1]) for f in C.FOOTS)
check("H2 the shape preference lives inside the baryons: the embedded subset's 95% interval excludes beta = 1 (both footings)",
      "; ".join(f"{f}: [{RES[(f, 'EMB')]['ci95'][0]:.2f}, {RES[(f, 'EMB')]['ci95'][1]:.2f}]" for f in C.FOOTS), h2)
med = {}
for nm, m in (("point-mass", PM), ("embedded", EMB)):
    for f in C.FOOTS:
        iu = int(np.argmin(np.abs(UPS - GL["H2"][f"{f}|P2"]["U"])))
        sel = m & OK[:, iu]
        med[(nm, f)] = float(np.median(GB[sel, iu] / A0[f]))
check("R1 (reported) the subsets' median g_bar/a0 (at P2's best Upsilon)", "; ".join(f"{k[0]} {k[1][:3]}: {v:.3f}" for k, v in med.items()),
      True, load_bearing=False)
R.num("fits", {f"{k[0]}|{k[1]}": v for k, v in RES.items()})
R.num("labels", lab)
R.num("median_y", {f"{k[0]}|{k[1]}": v for k, v in med.items()})
nf = R.write()
sys.exit(1 if nf else 0)
