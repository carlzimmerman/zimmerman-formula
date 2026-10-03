#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
AUDIT_SLUGGS (2026-10-03) -- hostile, two-sided re-computation of the SLUGGS law-alone row (CFG313 P5J = CFG55 H1:
+0.097 dex, +3.99 sigma canonical) from the raw files on disk, with code written for this audit.

Nothing is imported from h50 / CFG38 / CFG55 / CFG111 / CFG113 except the frozen kernel nu_mono (CFG4_common, read-only).
Raw inputs (all on disk, no downloads):
  real_research/data/sluggs_forbes2017_gcvel.tsv     (SLUGGS GC radial velocities, Forbes+2017)
  real_research/data/sluggs_forbes2017_galaxies.tsv  (SLUGGS galaxy table: D, log M*, R_eff, V_sys)
  real_research/data/atlas3d_fj_table.tsv            (ATLAS3D XV: logML_JAM, logL, logr12, qual; XX: logML_Salp)

The framework: g = nu(g_N/a0) g_N, a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 (FITTED), footings 9.36e-11 | 1.13e-10.
Kernel: nu_mono (primary). nu_RAR = 1/(1-exp(-sqrt y)) is also run, because CFG55 used it.
Jeans: spherical, constant beta, power-law GC tracer rho ~ r^-gamma, exact line-of-sight projection (u to 14, no u = 6 cut).
Calibration (CFG55's convention): nu(G (M/2)/r12^2 / a0) M/2 = M_JAM/2.  M_JAM, r12 scaled to the SLUGGS distance as D.
Statistic: mean over galaxies of the per-galaxy mean log10(sigma_obs/sigma_pred) over bins with R > max(R_e, 2 kpc);
error = galaxy-to-galaxy std (ddof 1)/sqrt(N).  Fixed physics inputs: gamma = 3, beta = 0 (as CFG55), then sensitivity rows that
reproduce the committed variants (literature gamma of CFG111; beta = +-0.5 of CFG113).  No fitting; kappa = 1/2 fixed.

MUTATE=1: a0 -> a0/100 (the law must collapse to Newton and the offset must rise by > 0.15 dex). Separate outputs.
"""
import os, sys, math, json
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
DATA = os.path.join(REPO, "real_research", "data")
sys.path.insert(0, LANES)
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4                                   # frozen nu_mono, read-only
MUTATE = os.environ.get("MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT = []


def P(s=""):
    print(s); OUT.append(s)


G = 6.674e-11; KPC = 3.0857e19; MSUN = 1.989e30
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
if MUTATE:
    A0 = {k: v / 100.0 for k, v in A0.items()}
ARCSEC = math.pi / 180 / 3600
KERN = {"nu_mono": lambda y: np.asarray(C4.nu_mono(np.maximum(np.asarray(y, float), 1e-14)), float),
        "nu_RAR": lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(np.asarray(y, float), 1e-14))))}


# ------------------------------------------------------------------ raw readers (written for this audit)
def vizier(fn):
    rows = [l.rstrip("\n") for l in open(os.path.join(DATA, fn), encoding="latin-1") if l.strip() and not l.startswith("#")]
    k = next(i for i, l in enumerate(rows) if set(l.replace("\t", "").strip()) <= set("-"))
    hdr = [h.strip() for h in rows[k - 2].split("\t")]
    return [dict(zip(hdr, [x.strip() for x in l.split("\t")])) for l in rows[k + 1:]]


def f(x):
    try:
        return float(x)
    except Exception:
        return float("nan")


GAL = {}
for r in vizier("sluggs_forbes2017_galaxies.tsv"):
    if r["NGC"].isdigit():
        GAL[int(r["NGC"])] = dict(D=f(r["Dist"]), lMs=f(r["logM*"]), Re_as=f(r["Reff"]), vsys=f(r["Vsys"]), env=r["Env"])
GCS = {n: [] for n in GAL}
for r in vizier("sluggs_forbes2017_gcvel.tsv"):
    key = r["Star"].split("_")[0]
    if not key.startswith("NGC") or not key[3:].isdigit():
        continue
    n = int(key[3:])                                           # integer key: immune to the NGC0720 / NGC720 mismatch
    v, e, rg = f(r["HRV"]), f(r["e_HRV"]), f(r["Rgal"])
    if n in GCS and np.isfinite(v) and np.isfinite(rg):
        GCS[n].append((rg, v, e if np.isfinite(e) else 15.0))

A3 = {}
for l in open(os.path.join(DATA, "atlas3d_fj_table.tsv")):
    if l.startswith("#") or not l.strip():
        continue
    p = l.rstrip("\n").split("\t")
    if p[0] == "name":
        H = p; continue
    A3[p[0]] = dict(zip(H, p))


# ------------------------------------------------------------------ dispersion estimator (own: deconvolved Gaussian ML, 3-sigma clip)
def ml_sigma(v, e):
    s2 = max(np.var(v) - np.mean(e ** 2), 1.0)
    for _ in range(500):
        w = 1 / (s2 + e ** 2); mu = np.sum(w * v) / np.sum(w)
        # exact ML stationarity for s2: sum w (1 - w (v-mu)^2) = 0  -> fixed-point
        s2n = max(np.sum(w ** 2 * ((v - mu) ** 2 - e ** 2)) / np.sum(w ** 2), 1.0)
        if abs(s2n - s2) < 1e-9 * s2:
            s2 = s2n; break
        s2 = s2n
    return mu, math.sqrt(s2)


def clipped(a, vsys):
    a = a[np.abs(a[:, 1] - vsys) < 1200.0]
    for _ in range(20):
        mu, s = ml_sigma(a[:, 1], a[:, 2])
        k = np.abs(a[:, 1] - mu) < 3.0 * math.hypot(s, a[:, 2].mean())
        if k.all():
            break
        a = a[k]
    return a


def bins_for(n):
    g = GAL[n]
    a = np.array(GCS[n], float)
    if len(a) < 8:
        return None
    a = clipped(a, g["vsys"])
    if len(a) < 30:
        return None
    kpc_am = math.pi / 180 / 60 * g["D"] * 1e3
    R = a[:, 0] * kpc_am
    o = np.argsort(R); a, R = a[o], R[o]
    nb = max(2, min(6, len(a) // 25))
    idx = np.array_split(np.arange(len(a)), nb)                # equal-number bins
    out = []
    for ii in idx:
        if len(ii) < 12:
            continue
        mu, s = ml_sigma(a[ii, 1], a[ii, 2])
        out.append((float(np.median(R[ii])), s, len(ii)))
    if len(out) < 2:
        return None
    Re = g["Re_as"] * ARCSEC * g["D"] * 1e3
    Rb = np.array([b[0] for b in out]); Sb = np.array([b[1] for b in out])
    outer = Rb > max(Re, 2.0)
    if not outer.any():
        outer = np.ones(len(Rb), bool)
    return dict(n=n, N=len(a), Re=Re, Rb=Rb, Sb=Sb, outer=outer)


# ------------------------------------------------------------------ Jeans (own)
RG = np.geomspace(1e-3, 1e8, 6000); LR = np.log(RG)


def g_law(M, a_h, a0, kern):
    gN = G * M * MSUN * RG ** 2 / (RG + a_h) ** 2 / (RG * KPC) ** 2
    return gN * KERN[kern](gN / a0), gN


def sig_los(Rb, g, gamma, beta=0.0):
    # sigma_r^2(r) = r^(gamma - 2 beta) int_r^inf r'^(2 beta - gamma) g(r') dr'   (SI, dr in m)
    w = RG ** (2 * beta - gamma) * g * RG * KPC                # integrand per d ln r
    cum = np.concatenate([np.cumsum((0.5 * (w[1:] + w[:-1]) * np.diff(LR))[::-1])[::-1], [0.0]])
    s2 = cum / RG ** (2 * beta - gamma)
    u = np.linspace(0, 14, 4000); ch = np.cosh(u)
    out = []
    for R in Rb:
        r = R * ch
        s2r = np.exp(np.interp(np.log(r), LR, np.log(np.maximum(s2, 1e-30))))
        rho = r ** -gamma
        num = np.trapz((1 - beta / ch ** 2) * rho * s2r * r, u)
        den = np.trapz(rho * r, u)
        out.append(math.sqrt(num / den) / 1e3)
    return np.array(out)


def offset(b, M, a0, kern, gamma=3.0, beta=0.0, a_h=None, use="outer"):
    a_h = b["Re"] / 1.8153 if a_h is None else a_h
    g, _ = g_law(M, a_h, a0, kern)
    s = sig_los(b["Rb"], g, gamma, beta)
    m = b["outer"] if use == "outer" else np.ones(len(b["Rb"]), bool)
    return float(np.mean(np.log10(b["Sb"][m] / s[m])))


def jam_mass(Mjam, r12, a0, kern, frac=0.5):
    fn = lambda lm: math.log10(frac * 10 ** lm * float(KERN[kern](G * frac * 10 ** lm * MSUN / (r12 * KPC) ** 2 / a0))) - math.log10(frac * Mjam)
    return 10 ** brentq(fn, math.log10(Mjam) - 4, math.log10(Mjam) + 1, xtol=1e-12)


def inner_excess(M, Mjam, r12, a0, kern):
    """dex by which the law with stellar mass M over-predicts the JAM mass inside r12 (> 0 = inner kinematics violated)."""
    return math.log10(0.5 * M * float(KERN[kern](G * 0.5 * M * MSUN / (r12 * KPC) ** 2 / a0)) / (0.5 * Mjam))


def stat(x):
    x = np.asarray(x, float); e = x.std(ddof=1) / math.sqrt(len(x))
    return float(x.mean()), float(e), float(x.mean() / e)


# ------------------------------------------------------------------ sample
B = {n: bins_for(n) for n in sorted(GAL) if np.isfinite(GAL[n]["D"]) and np.isfinite(GAL[n]["lMs"])}
B = {n: b for n, b in B.items() if b is not None}
CFG55_16 = [1023, 2768, 3377, 3607, 4278, 4365, 4374, 4459, 4473, 4486, 4494, 4526, 4649, 4697, 5846, 7457]
JAM = [n for n in B if f"NGC{n:04d}" in A3 and f(A3[f"NGC{n:04d}"]["qual"]) >= 1]
P("=" * 118)
P("AUDIT_SLUGGS -- independent recompute of the law-alone SLUGGS row from the raw files" + ("   *** MUTATE: a0/100 ***" if MUTATE else ""))
P("=" * 118)
P(f"galaxies with >= 30 clean GCs and >= 2 bins: {len(B)}  -> {['NGC%d' % n for n in B]}")
P(f"with ATLAS3D JAM (qual >= 1): {len(JAM)} -> {['NGC%d' % n for n in JAM]}")
P(f"CFG55's 16 all present: {all(n in JAM for n in CFG55_16)}; extra here: {[n for n in JAM if n not in CFG55_16]} (h50's key bug dropped NGC 720/821)")

for n in JAM:
    a = A3[f"NGC{n:04d}"]; DS, DA = GAL[n]["D"], f(a["Dist_Mpc"])
    B[n]["Mjam"] = 10 ** (f(a["logML_JAM"]) + f(a["logL"])) * DS / DA
    B[n]["r12"] = 10 ** f(a["logr12"]) * ARCSEC * DS * 1e3
    B[n]["Msalp"] = 10 ** (f(a["logML_Salp"]) + f(a["logL"])) * (DS / DA) ** 2
    B[n]["fDM_XX"] = f(a["fDM_Re"])
    B[n]["Msl"] = 10 ** GAL[n]["lMs"]

RES = {}
for kern in ("nu_mono", "nu_RAR"):
    for foot, a0 in A0.items():
        rows = {}
        for n in JAM:
            b = B[n]
            Mj = jam_mass(b["Mjam"], b["r12"], a0, kern)
            rows[n] = dict(lMjamlaw=math.log10(Mj), off=offset(b, Mj, a0, kern),
                           off_sl=offset(b, b["Msl"], a0, kern), off_salp=offset(b, b["Msalp"], a0, kern),
                           inner_sl=inner_excess(b["Msl"], b["Mjam"], b["r12"], a0, kern),
                           inner_salp=inner_excess(b["Msalp"], b["Mjam"], b["r12"], a0, kern))
        RES[(kern, foot)] = rows

# ------------------------------------------------------------------ 1. headline
P("\n" + "-" * 118); P("1. HEADLINE: JAM-calibrated law, gamma = 3, isotropic, outer bins"); P("-" * 118)
c55 = json.load(open(os.path.join(LANES, "CFG55_sluggs_dynamical_masses_results.json")))["numbers"]["RES"]
HEAD = {}
for kern in ("nu_mono", "nu_RAR"):
    for foot in A0:
        r = RES[(kern, foot)]
        s16 = stat([r[n]["off"] for n in CFG55_16]); s17 = stat([r[n]["off"] for n in JAM])
        HEAD[(kern, foot)] = dict(s16=s16, s17=s17)
        P(f"  {kern:7} {foot:9}: 16 (CFG55 sample) {s16[0]:+.4f} +- {s16[1]:.4f} ({s16[2]:+.2f} sigma) | "
          f"{len(JAM)} (key fixed) {s17[0]:+.4f} +- {s17[1]:.4f} ({s17[2]:+.2f} sigma)")
P(f"  committed CFG55 (nu_RAR): canonical {c55['canonical']['law']['mean']:+.4f} +- {c55['canonical']['law']['err']:.4f}; "
  f"alt {c55['alt']['law']['mean']:+.4f} +- {c55['alt']['law']['err']:.4f}")
per55 = dict(zip(CFG55_16, c55["canonical"]["law"]["per"]))
P("\n  per galaxy (canonical, nu_mono): log M* SLUGGS | JAM-law | Salpeter-pop ; outer offset ; CFG55 offset ; diff ; inner excess of Salpeter / SLUGGS mass")
dmax = 0.0
for n in JAM:
    r = RES[("nu_mono", "canonical")][n]; b = B[n]
    d = r["off"] - per55[n] if n in per55 else float("nan")
    if np.isfinite(d):
        dmax = max(dmax, abs(d))
    P(f"   NGC{n:<5} {math.log10(b['Msl']):6.2f} | {r['lMjamlaw']:6.2f} | {math.log10(b['Msalp']):6.2f} ; {r['off']:+.3f} ; "
      f"{per55.get(n, float('nan')):+.3f} ; {d:+.4f} ; Salp {r['inner_salp']:+.3f} dex, SLUGGS {r['inner_sl']:+.3f} dex ; nbins {len(b['Rb'])}, N_GC {b['N']}")
P(f"  max |independent - CFG55| per galaxy (nu_mono vs CFG55's nu_RAR): {dmax:.4f} dex")
dmaxR = max(abs(RES[("nu_RAR", "canonical")][n]["off"] - per55[n]) for n in CFG55_16)
P(f"  max |independent - CFG55| per galaxy, same kernel nu_RAR: {dmaxR:.4f} dex (differences = own clip/ML/projection code)")

# ------------------------------------------------------------------ 2. IMF lever
P("\n" + "-" * 118); P("2. STELLAR MASS / IMF: is any IMF heavier than the JAM ceiling allowed by the galaxy's own inner kinematics?"); P("-" * 118)
r = RES[("nu_mono", "canonical")]
ins = np.array([r[n]["inner_salp"] for n in CFG55_16]); isl = np.array([r[n]["inner_sl"] for n in CFG55_16])
P(f"  Salpeter population mass (ATLAS3D XX, r band): law over-predicts the JAM mass inside r12 by median {np.median(ins):+.3f} dex "
  f"(mean {ins.mean():+.3f}); {int((ins > 0).sum())}/16 galaxies over-predicted")
P(f"  SLUGGS mass (K-band, ~Kroupa/Chabrier-like): inner excess median {np.median(isl):+.3f} dex; {int((isl > 0).sum())}/16 over-predicted")
for foot in A0:
    rr = RES[("nu_mono", foot)]
    ss = stat([rr[n]["off_salp"] for n in CFG55_16]); sl = stat([rr[n]["off_sl"] for n in CFG55_16])
    P(f"  {foot:9}: outer offset with Salpeter masses {ss[0]:+.4f} ({ss[2]:+.2f} sigma); with SLUGGS masses {sl[0]:+.4f} ({sl[2]:+.2f} sigma)")
# mass needed to null each outer offset, vs JAM ceiling
need = []
for n in CFG55_16:
    b = B[n]; a0 = A0["canonical"]
    fn = lambda lm: offset(b, 10 ** lm, a0, "nu_mono")
    lo, hi = math.log10(b["Msl"]) - 2, math.log10(b["Msl"]) + 3
    lmn = brentq(fn, lo, hi, xtol=1e-4) if fn(lo) * fn(hi) < 0 else float("nan")
    need.append((n, lmn - r[n]["lMjamlaw"], inner_excess(10 ** lmn, b["Mjam"], b["r12"], a0, "nu_mono") if np.isfinite(lmn) else float("nan")))
nd = np.array([x[1] for x in need]); ne = np.array([x[2] for x in need])
P(f"  stellar mass that nulls each outer offset, relative to the JAM-law ceiling: median {np.nanmedian(nd):+.3f} dex (range {np.nanmin(nd):+.2f}..{np.nanmax(nd):+.2f});"
  f" it would over-predict the inner JAM mass by median {np.nanmedian(ne):+.3f} dex")
P("  -> an IMF heavier than the JAM ceiling is excluded by each galaxy's own inner kinematics under the law; an IMF gradient that is"
  " bottom-heavy only in the core (the measured sense) lowers the outer stellar mass and enlarges the deficit.")

# ------------------------------------------------------------------ 3. physics-input sensitivity (reproduces committed variants)
P("\n" + "-" * 118); P("3. SENSITIVITY TO THE FIXED PHYSICS INPUTS (gamma, beta, Hernquist scale, bin choice), JAM-calibrated, nu_mono"); P("-" * 118)
SENS = {}
for foot, a0 in A0.items():
    rr = RES[("nu_mono", foot)]
    Mj = {n: 10 ** rr[n]["lMjamlaw"] for n in CFG55_16}
    gl = {n: min(max(-0.63 * GAL[n]["lMs"] + 9.81, 2.0), 4.0) for n in CFG55_16}
    rows = {
        "gamma 3, beta 0 (CFG55)": [rr[n]["off"] for n in CFG55_16],
        "gamma = Alabi+17 relation (CFG111)": [offset(B[n], Mj[n], a0, "nu_mono", gamma=gl[n]) for n in CFG55_16],
        "gamma 3, beta +0.5": [offset(B[n], Mj[n], a0, "nu_mono", beta=0.5) for n in CFG55_16],
        "gamma 3, beta -0.5": [offset(B[n], Mj[n], a0, "nu_mono", beta=-0.5) for n in CFG55_16],
        "Alabi gamma, beta +0.5": [offset(B[n], Mj[n], a0, "nu_mono", gamma=gl[n], beta=0.5) for n in CFG55_16],
        "Hernquist a from ATLAS3D r12 (a = r12/2.414)": [offset(B[n], Mj[n], a0, "nu_mono", a_h=B[n]["r12"] / (1 + math.sqrt(2))) for n in CFG55_16],
        "all bins (inner + outer)": [offset(B[n], Mj[n], a0, "nu_mono", use="all") for n in CFG55_16],
        "without the 4 group/cluster centrals (N=12)": [rr[n]["off"] for n in CFG55_16 if n not in (4486, 4365, 4374, 5846)],
    }
    SENS[foot] = {k: stat(v) for k, v in rows.items()}
    for k, v in SENS[foot].items():
        P(f"  {foot:9} {k:46}: {v[0]:+.4f} +- {v[1]:.4f} ({v[2]:+.2f} sigma)")
# shared gamma shift that brings the canonical z to 2
rr = RES[("nu_mono", "canonical")]; a0 = A0["canonical"]
def zshift(dg):
    return stat([offset(B[n], 10 ** rr[n]["lMjamlaw"], a0, "nu_mono", gamma=3.0 + dg) for n in CFG55_16])[2]
_lo, _hi = zshift(-1.5) - 2.0, zshift(0.0) - 2.0
dg2 = brentq(lambda d: zshift(d) - 2.0, -1.5, 0.0, xtol=1e-3) if _lo * _hi < 0 else float("nan")
P(f"  shared shift of gamma (from 3) that brings the canonical z to 2.0: {dg2:+.2f} (gamma = {3 + dg2:.2f})")

# ------------------------------------------------------------------ 4. internal field at the outer bins (EFE relevance)
P("\n" + "-" * 118); P("4. INTERNAL FIELD AT THE OUTERMOST BIN (canonical; EFE matters only where g_ext is comparable)"); P("-" * 118)
for n in CFG55_16:
    b = B[n]; M = 10 ** rr[n]["lMjamlaw"]; g, gN = g_law(M, b["Re"] / 1.8153, A0["canonical"], "nu_mono")
    R = b["Rb"][-1]; gi = float(np.interp(R, RG, g)) / A0["canonical"]
    P(f"   NGC{n:<5} env {GAL[n]['env']}  R_out {R:6.1f} kpc  g_int/a0 {gi:.3f}")
P("  EFE (any g_ext > 0) can only LOWER the law's prediction -> it can only ENLARGE the deficit; with g_ext <~ 0.05 a0 for these")
P("  environments and g_int/a0 >~ 0.1 at the outer bins its size is small; no external-field table is on disk to quantify it.")

# ------------------------------------------------------------------ checks + outputs
P("\n" + "-" * 118); P("CHECKS"); P("-" * 118)
ok = []
def check(lbl, cond, det):
    ok.append(bool(cond)); P(f"  [{'PASS' if cond else 'FAIL'}] {lbl}\n         {det}")
hc = HEAD[("nu_RAR", "canonical")]["s16"][0]
check("A1 independent code (same kernel nu_RAR) reproduces CFG55's canonical law mean within 0.01 dex",
      abs(hc - c55["canonical"]["law"]["mean"]) < 0.01, f"{hc:+.4f} vs {c55['canonical']['law']['mean']:+.4f}")
check("A2 nu_mono vs nu_RAR differ by < 0.005 dex in the mean (CFG76: ~0.001)",
      abs(HEAD[("nu_mono", "canonical")]["s16"][0] - hc) < 0.005, f"{HEAD[('nu_mono','canonical')]['s16'][0]:+.4f} vs {hc:+.4f}")
if MUTATE:
    check("M1 MUTATE a0/100: offset rises by > 0.15 dex (estimator sensitive to a0)",
          HEAD[("nu_mono", "canonical")]["s16"][0] > c55["canonical"]["law"]["mean"] + 0.15, f"{HEAD[('nu_mono','canonical')]['s16'][0]:+.4f}")

json.dump(dict(mutate=MUTATE, a0=A0,
               headline={f"{k}|{f_}": v for (k, f_), v in HEAD.items()},
               per_galaxy={f"{k}|{f_}": {str(n): v for n, v in rows.items()} for (k, f_), rows in RES.items()},
               sensitivity=SENS, gamma_shift_to_2sigma=dg2,
               null_mass_vs_jam={str(n): dict(dlogM=d, inner_excess=e) for n, d, e in need}),
          open(os.path.join(HERE, f"audit_sluggs_recompute{TAG}_results.json"), "w"), indent=1)
P(f"\n  {sum(ok)}/{len(ok)} checks pass")
open(os.path.join(HERE, f"audit_sluggs_recompute{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(ok) else 1)
