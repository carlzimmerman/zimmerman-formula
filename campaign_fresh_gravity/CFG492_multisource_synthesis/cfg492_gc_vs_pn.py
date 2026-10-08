#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG492 part B: same-galaxy GC vs PN test of the SLUGGS outer deficit.  Criteria: FROZEN_CRITERIA.md (committed alone first).

Law g = nu_mono(g_N/a0) g_N, kappa = 1/2 FITTED, footings 9.36e-11 | 1.13e-10 (never pooled).  Mass model, JAM calibration and the
GC estimator are the AUDIT_SLUGGS code path (re-written here, checked by C1).  PN side: same estimator; the tracer density is the
Hernquist starlight profile (general-density Jeans solver, checked by C2).  No downloads; inputs under real_research/data/.
MUTATE=1: shuffled PN <-> galaxy pairing (cyclic derangement, rescaled to R/R_e and v - v_sys); separate outputs.
"""
import os, sys, math, json, re
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
DATA = os.path.join(REPO, "real_research", "data")
sys.path.insert(0, LANES)
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4
MUTATE = os.environ.get("MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(s=""):
    print(s); OUT.append(str(s))

G = 6.674e-11; KPC = 3.0857e19; MSUN = 1.989e30
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
ARCSEC = math.pi / 180 / 3600
nu = lambda y: np.asarray(C4.nu_mono(np.maximum(np.asarray(y, float), 1e-14)), float)
RNG = np.random.default_rng(492)
NBOOT = 500

# ------------------------------------------------------------------ readers
def vizier(fn):
    rows = [l.rstrip("\n") for l in open(os.path.join(DATA, fn), encoding="latin-1") if l.strip() and not l.startswith("#")]
    k = next(i for i, l in enumerate(rows) if l.replace("\t", "").strip() and set(l.replace("\t", "").strip()) <= set("-"))
    hdr = [h.strip() for h in rows[k - 2].split("\t")]
    return [dict(zip(hdr, [x for x in l.split("\t")])) for l in rows[k + 1:]]
def f(x):
    try:
        return float(x)
    except Exception:
        return float("nan")
def hms(s):
    p = [float(x) for x in s.replace(":", " ").split()]
    return 15 * (p[0] + p[1] / 60 + p[2] / 3600)
def dms(s):
    s = s.strip(); sg = -1 if s.startswith("-") else 1
    p = [float(x) for x in s.replace("+", " ").replace("-", " ").replace(":", " ").split()]
    return sg * (p[0] + p[1] / 60 + p[2] / 3600)

GAL = {}
for r in vizier("sluggs_forbes2017_galaxies.tsv"):
    if r["NGC"].strip().isdigit():
        GAL[int(r["NGC"])] = dict(D=f(r["Dist"]), Re_as=f(r["Reff"]), vsys=f(r["Vsys"]), ra=f(r["RAJ2000"]), dec=f(r["DEJ2000"]), env=r["Env"].strip())
GCS = {n: [] for n in GAL}
for r in vizier("sluggs_forbes2017_gcvel.tsv"):
    key = r["Star"].strip().split("_")[0]
    if not key.startswith("NGC") or not key[3:].isdigit():
        continue
    n = int(key[3:]); v, e, rg = f(r["HRV"]), f(r["e_HRV"]), f(r["Rgal"])
    if n in GCS and np.isfinite(v) and np.isfinite(rg):
        GCS[n].append((rg, v, e if np.isfinite(e) else 15.0))    # Rgal in arcmin (audit convention)
A3 = {}
for l in open(os.path.join(DATA, "atlas3d_fj_table.tsv")):
    if l.startswith("#") or not l.strip():
        continue
    p = l.rstrip("\n").split("\t")
    if p[0] == "name":
        H = p; continue
    A3[p[0]] = dict(zip(H, p))

# PN catalogues -> per galaxy list of (R_arcmin, v, e); positions relative to the SLUGGS centre
PNraw = {}
for r in vizier("pn_coccato2009_sampleA.tsv"):
    m = re.match(r"NGC0*(\d+)-", r["PNS-EPN"].strip())
    if m:
        PNraw.setdefault(int(m.group(1)), []).append((hms(r["RAJ2000"]), dms(r["DEJ2000"]), f(r["HRV"]), f(r["e_HRV"]), ""))
for r in vizier("pn_ngc1023_noordermeer2008.tsv"):
    PNraw.setdefault(1023, []).append((hms(r["RAJ2000"]), dms(r["DEJ2000"]), f(r["HV"]), f(r["e_HV"]), r["n_HV"].strip()))
for r in vizier("pn_ngc4494_napolitano2009.tsv"):
    PNraw.setdefault(4494, []).append((hms(r["RAJ2000"]), dms(r["DEJ2000"]), f(r["HV"]), float("nan"), ""))

def pn_set(n, keep_flagged=False):
    g = GAL[n]; out = []
    for ra, de, v, e, flag in PNraw[n]:
        if flag and not keep_flagged:
            continue
        if not np.isfinite(v):
            continue
        dx = (ra - g["ra"]) * math.cos(math.radians(g["dec"])); dy = de - g["dec"]
        out.append((math.hypot(dx, dy) * 60.0, v, e if np.isfinite(e) else 20.0))
    return np.array(out, float)

# ------------------------------------------------------------------ estimator (audit's)
def ml_sigma(v, e):
    s2 = max(np.var(v) - np.mean(e ** 2), 1.0)
    for _ in range(500):
        w = 1 / (s2 + e ** 2); mu = np.sum(w * v) / np.sum(w)
        s2n = max(np.sum(w ** 2 * ((v - mu) ** 2 - e ** 2)) / np.sum(w ** 2), 1.0)
        if abs(s2n - s2) < 1e-9 * s2:
            s2 = s2n; break
        s2 = s2n
    return mu, math.sqrt(s2)
def clipped(a, vsys, k=3.0):
    a = a[np.abs(a[:, 1] - vsys) < 1200.0]
    for _ in range(20):
        mu, s = ml_sigma(a[:, 1], a[:, 2])
        kk = np.abs(a[:, 1] - mu) < k * math.hypot(s, a[:, 2].mean())
        if kk.all():
            break
        a = a[kk]
    return a
def bins_of(a, n):
    """a = clean (R_arcmin, v, e).  The audit's binning rule."""
    g = GAL[n]; kpc_am = math.pi / 180 / 60 * g["D"] * 1e3
    R = a[:, 0] * kpc_am; o = np.argsort(R); a, R = a[o], R[o]
    nb = max(2, min(6, len(a) // 25))
    out = []
    for ii in np.array_split(np.arange(len(a)), nb):
        if len(ii) < 12:
            continue
        mu, s = ml_sigma(a[ii, 1], a[ii, 2]); out.append((float(np.median(R[ii])), s, len(ii)))
    if len(out) < 2:
        return None
    Re = g["Re_as"] * ARCSEC * g["D"] * 1e3
    Rb = np.array([b[0] for b in out]); Sb = np.array([b[1] for b in out])
    outer = Rb > max(Re, 2.0)
    if not outer.any():
        outer = np.ones(len(Rb), bool)
    return dict(Rb=Rb, Sb=Sb, outer=outer, N=len(a), Re=Re)
def clean_or_none(a, n, k=3.0):
    if a is None or len(a) < 8:
        return None
    c = clipped(a, GAL[n]["vsys"], k)
    return c if len(c) >= 30 else None

# ------------------------------------------------------------------ Jeans
RG = np.geomspace(1e-3, 1e8, 6000); LR = np.log(RG)
def g_law(M, a_h, a0):
    gN = G * M * MSUN * RG ** 2 / (RG + a_h) ** 2 / (RG * KPC) ** 2
    return gN * nu(gN / a0)
def sig_los_pow(Rb, g, gamma, beta=0.0):            # the audit's solver, verbatim logic (for C2)
    w = RG ** (2 * beta - gamma) * g * RG * KPC
    cum = np.concatenate([np.cumsum((0.5 * (w[1:] + w[:-1]) * np.diff(LR))[::-1])[::-1], [0.0]])
    s2 = cum / RG ** (2 * beta - gamma)
    u = np.linspace(0, 14, 4000); ch = np.cosh(u); out = []
    for R in Rb:
        r = R * ch
        s2r = np.exp(np.interp(np.log(r), LR, np.log(np.maximum(s2, 1e-30))))
        rho = r ** -gamma
        out.append(math.sqrt(np.trapz((1 - beta / ch ** 2) * rho * s2r * r, u) / np.trapz(rho * r, u)) / 1e3)
    return np.array(out)
def s2_general(g, rho_fn, beta=0.0):
    rho = rho_fn(RG)
    w = rho * RG ** (2 * beta) * g * RG * KPC
    cum = np.concatenate([np.cumsum((0.5 * (w[1:] + w[:-1]) * np.diff(LR))[::-1])[::-1], [0.0]])
    return cum / (rho * RG ** (2 * beta))
U = np.linspace(0, 14, 4000); CH = np.cosh(U)
def proj(Rb, s2, rho_fn, beta=0.0):
    out = []
    for R in Rb:
        r = R * CH
        s2r = np.exp(np.interp(np.log(r), LR, np.log(np.maximum(s2, 1e-30))))
        rho = rho_fn(r)
        out.append(math.sqrt(np.trapz((1 - beta / CH ** 2) * rho * s2r * r, U) / np.trapz(rho * r, U)) / 1e3)
    return np.array(out)
def jam_mass(Mjam, r12, a0, frac=0.5):
    fn = lambda lm: math.log10(frac * 10 ** lm * float(nu(G * frac * 10 ** lm * MSUN / (r12 * KPC) ** 2 / a0))) - math.log10(frac * Mjam)
    return 10 ** brentq(fn, math.log10(Mjam) - 4, math.log10(Mjam) + 1, xtol=1e-12)

def model(n, a0, M=None):
    g0 = GAL[n]; a = A3[f"NGC{n:04d}"]; DS, DA = g0["D"], f(a["Dist_Mpc"])
    Mjam = 10 ** (f(a["logML_JAM"]) + f(a["logL"])) * DS / DA
    r12 = 10 ** f(a["logr12"]) * ARCSEC * DS * 1e3
    Re = g0["Re_as"] * ARCSEC * DS * 1e3; ah = Re / 1.8153
    M = jam_mass(Mjam, r12, a0) if M is None else M
    return dict(M=M, ah=ah, Re=Re, g=g_law(M, ah, a0))
def offset_of(b, sig_pred, use="outer"):
    m = b["outer"] if use == "outer" else np.ones(len(b["Rb"]), bool)
    return float(np.mean(np.log10(b["Sb"][m] / sig_pred[m])))

def tracer_offset(a_clean, n, mod, kind, beta=0.0, gamma_gc=3.0, use="outer"):
    b = bins_of(a_clean, n)
    if b is None:
        return None, None
    if kind == "GC":
        rho = lambda r: r ** -gamma_gc
    else:
        ah = mod["ah"]; rho = lambda r: 1.0 / (r * (r + ah) ** 3)
    s2 = s2_general(mod["g"], rho, beta)
    return offset_of(b, proj(b["Rb"], s2, rho, beta), use), b

def boot_err(a_clean, n, mod, kind):
    ah = mod["ah"]
    rho = (lambda r: r ** -3.0) if kind == "GC" else (lambda r: 1.0 / (r * (r + ah) ** 3))
    s2 = s2_general(mod["g"], rho, 0.0)
    vals = []
    for _ in range(NBOOT):
        a = a_clean[RNG.integers(0, len(a_clean), len(a_clean))]
        b = bins_of(a, n)
        if b is None:
            continue
        vals.append(offset_of(b, proj(b["Rb"], s2, rho, 0.0)))
    return float(np.std(vals, ddof=1))

def stat2(x, e):
    """mean; error = max(galaxy-to-galaxy std/sqrt N, inverse-variance error)."""
    x = np.asarray(x, float); e = np.asarray(e, float); N = len(x)
    e1 = x.std(ddof=1) / math.sqrt(N) if N > 1 else float("inf")
    w = 1 / e ** 2; e2 = math.sqrt(1 / w.sum())
    return float(x.mean()), float(max(e1, e2)), float(e1), float(e2)

# ------------------------------------------------------------------ run
P("=" * 116)
P("CFG492 B -- same-galaxy GC vs PN test of the SLUGGS outer deficit" + ("   *** MUTATE: shuffled PN <-> galaxy pairing ***" if MUTATE else ""))
P("=" * 116)
CAND = sorted(set(PNraw) & set(GAL))
P(f"PN galaxies with a SLUGGS centre: {['NGC%d' % n for n in CAND]}")
AUD = json.load(open(os.path.join(LANES, "AUDIT_SLUGGS_2026-10-03", "audit_sluggs_recompute_results.json")))["per_galaxy"]

checks = []
def check(lbl, cond, det):
    checks.append(bool(cond)); P(f"  [{'PASS' if cond else 'FAIL'}] {lbl}\n         {det}")

GCc = {n: clean_or_none(np.array(GCS[n], float), n) for n in CAND}
PNc = {n: clean_or_none(pn_set(n), n) for n in CAND}
PNc_flag = {n: clean_or_none(pn_set(n, True), n) for n in CAND}
PNc_25 = {n: (clean_or_none(pn_set(n), n, 2.5)) for n in CAND}

# C3 centring
P("\nC3 PN centring (median PN radius-vector offset / R_e; clipped mean v - v_sys):")
c3 = True
for n in CAND:
    g = GAL[n]; raw = [(ra, de) for ra, de, *_ in PNraw[n]]
    mra = np.median([(ra - g["ra"]) * math.cos(math.radians(g["dec"])) for ra, de in raw]) * 3600
    mde = np.median([de - g["dec"] for ra, de in raw]) * 3600
    off_re = math.hypot(mra, mde) / g["Re_as"]
    if PNc[n] is not None:
        mu, s = ml_sigma(PNc[n][:, 1], PNc[n][:, 2]); dv = mu - g["vsys"]
    else:
        dv = float("nan")
    ok = off_re < 1.0 and (abs(dv) < 150 if np.isfinite(dv) else True)
    c3 &= ok
    P(f"   NGC{n:<5} N_raw {len(PNraw[n]):4d}  N_clean {0 if PNc[n] is None else len(PNc[n]):4d}  centre offset {off_re:.2f} R_e  dv {dv:+7.1f} km/s  {'ok' if ok else 'BAD'}")

PAIR = [n for n in CAND if GCc[n] is not None and PNc[n] is not None and bins_of(GCc[n], n) is not None and bins_of(PNc[n], n) is not None]
PNONLY = [n for n in CAND if n not in PAIR and PNc[n] is not None and f"NGC{n:04d}" in A3]
P(f"\nPaired galaxies (>= 30 clean GCs and PNe, >= 2 bins each): {['NGC%d' % n for n in PAIR]}  (N = {len(PAIR)})")
P(f"PN-only galaxies (no usable GC offset): {['NGC%d' % n for n in PNONLY]}")

# MUTATE: derangement of the PN sets across the paired list
PNuse = dict(PNc)
if MUTATE:
    shuf = {}
    for i, n in enumerate(PAIR):
        src = PAIR[i - 1]                     # galaxy n receives the PN set of the previous galaxy
        gs, gd = GAL[src], GAL[n]
        a = PNc[src].copy()
        a[:, 0] = a[:, 0] / (gs["Re_as"] / 60) * (gd["Re_as"] / 60)    # R in arcmin, rescaled by R_e
        a[:, 1] = a[:, 1] - gs["vsys"] + gd["vsys"]
        shuf[n] = a
    PNuse.update(shuf)

RES = {}
for foot, a0 in A0.items():
    rows = {}
    for n in PAIR + PNONLY:
        mod = model(n, a0)
        oPN, bPN = tracer_offset(PNuse[n], n, mod, "PN")
        row = dict(lM=math.log10(mod["M"]), O_PN=oPN, nPN=int(len(PNuse[n])), RPN=list(map(float, bPN["Rb"])), SPN=list(map(float, bPN["Sb"])),
                   e_PN=boot_err(PNuse[n], n, mod, "PN"), Re=mod["Re"])
        if n in PAIR:
            oGC, bGC = tracer_offset(GCc[n], n, mod, "GC")
            row.update(O_GC=oGC, nGC=int(len(GCc[n])), RGC=list(map(float, bGC["Rb"])), SGC=list(map(float, bGC["Sb"])),
                       e_GC=boot_err(GCc[n], n, mod, "GC"))
            # C2: general solver with rho = r^-3 vs the audit's power-law solver
            sp = sig_los_pow(bGC["Rb"], mod["g"], 3.0)
            sg = proj(bGC["Rb"], s2_general(mod["g"], lambda r: r ** -3.0), lambda r: r ** -3.0)
            row["C2"] = float(np.max(np.abs(np.log10(sg / sp))))
        for lbl, kw in (("O_PN_bp05", dict(beta=0.5)), ("O_PN_bm05", dict(beta=-0.5)), ("O_PN_all", dict(use="all"))):
            row[lbl] = tracer_offset(PNuse[n], n, mod, "PN", **kw)[0]
        if not MUTATE:
            row["O_PN_clip25"] = tracer_offset(PNc_25[n], n, mod, "PN")[0] if PNc_25[n] is not None else None
            row["O_PN_flagkept"] = tracer_offset(PNc_flag[n], n, mod, "PN")[0] if PNc_flag[n] is not None else None
            row["O_PN_a0div100"] = tracer_offset(PNc[n], n, model(n, a0 / 100.0), "PN")[0]
        rows[n] = row
    RES[foot] = rows

# Alabi gamma reported row for GC (CFG111 relation, uses SLUGGS log M*)
LMS = {int(r["NGC"]): f(r["logM*"]) for r in vizier("sluggs_forbes2017_galaxies.tsv") if r["NGC"].strip().isdigit()}
for foot, a0 in A0.items():
    for n in PAIR:
        mod = model(n, a0)
        gl = min(max(-0.63 * LMS[n] + 9.81, 2.0), 4.0)
        RES[foot][n]["O_GC_alabi"] = tracer_offset(GCc[n], n, mod, "GC", gamma_gc=gl)[0]
        RES[foot][n]["gamma_alabi"] = gl

# ------------------------------------------------------------------ report
VERD = {}
for foot in A0:
    r = RES[foot]
    P("\n" + "-" * 116)
    P(f"FOOTING {foot} (a0 = {A0[foot]:.3g})")
    P("-" * 116)
    P("  galaxy   logM_law  N_GC  O_GC +- boot   N_PN  O_PN +- boot   Delta=PN-GC   R_PN range kpc   R_GC range kpc")
    for n in PAIR:
        x = r[n]
        P(f"  NGC{n:<5}  {x['lM']:6.2f}  {x['nGC']:4d}  {x['O_GC']:+.3f} +- {x['e_GC']:.3f}  {x['nPN']:4d}  {x['O_PN']:+.3f} +- {x['e_PN']:.3f}   {x['O_PN']-x['O_GC']:+.3f}"
          f"        {min(x['RPN']):5.1f}-{max(x['RPN']):5.1f}       {min(x['RGC']):5.1f}-{max(x['RGC']):5.1f}")
    for n in PNONLY:
        x = r[n]
        P(f"  NGC{n:<5}  {x['lM']:6.2f}   --      --          {x['nPN']:4d}  {x['O_PN']:+.3f} +- {x['e_PN']:.3f}   (PN only)     {min(x['RPN']):5.1f}-{max(x['RPN']):5.1f}")
    d = [r[n]["O_PN"] - r[n]["O_GC"] for n in PAIR]
    de = [math.hypot(r[n]["e_PN"], r[n]["e_GC"]) for n in PAIR]
    D, sD, sD1, sD2 = stat2(d, de)
    M, sM, sM1, sM2 = stat2([r[n]["O_PN"] for n in PAIR], [r[n]["e_PN"] for n in PAIR])
    Gm, sG, _, _ = stat2([r[n]["O_GC"] for n in PAIR], [r[n]["e_GC"] for n in PAIR])
    rms = float(np.sqrt(np.mean(np.square(d))))
    P(f"\n  M_GC (paired) = {Gm:+.4f} +- {sG:.4f}")
    P(f"  M_PN (paired) = {M:+.4f} +- {sM:.4f}  (galaxy-to-galaxy {sM1:.4f}, inverse-variance {sM2:.4f})  -> {M/sM:+.2f} sigma")
    P(f"  D = mean(PN - GC) = {D:+.4f} +- {sD:.4f}  (galaxy-to-galaxy {sD1:.4f}, inverse-variance {sD2:.4f})  -> {D/sD:+.2f} sigma ;  rms(Delta) = {rms:.4f}")
    if len(PAIR) < 5:
        v = "NOT POSSIBLE (N_paired < 5)"
    elif M < -2 * sM:
        v = "PN SURPLUS"
    elif M > 2 * sM and abs(D) < 2 * sD:
        v = "MASS PROPERTY"
    elif D < -2 * sD and abs(M) < 2 * sM:
        v = "TRACER SYSTEMATIC"
    else:
        v = "UNDECIDED"
    VERD[foot] = dict(verdict=v, M_PN=M, sM=sM, D=D, sD=sD, M_GC=Gm, sG=sG, rms_delta=rms, N=len(PAIR))
    P(f"  frozen rule -> {v}")
    # reported rows
    P("\n  reported rows (not decision rows), mean over the paired galaxies:")
    for lbl in ("O_PN_bp05", "O_PN_bm05", "O_PN_all", "O_PN_clip25", "O_PN_flagkept", "O_PN_a0div100"):
        vals = [r[n][lbl] for n in PAIR if r[n].get(lbl) is not None]
        if vals:
            P(f"    {lbl:15}: {np.mean(vals):+.4f} (N {len(vals)})")
    P(f"    O_GC_alabi     : {np.mean([r[n]['O_GC_alabi'] for n in PAIR]):+.4f}  (gamma {[round(r[n]['gamma_alabi'],2) for n in PAIR]})")
    cen = [n for n in PAIR if n in (4374, 5846)]
    if cen:
        P(f"    centrals {['NGC%d' % n for n in cen]}: O_GC {np.mean([r[n]['O_GC'] for n in cen]):+.3f}, O_PN {np.mean([r[n]['O_PN'] for n in cen]):+.3f}")
        non = [n for n in PAIR if n not in cen]
        P(f"    non-centrals {['NGC%d' % n for n in non]}: O_GC {np.mean([r[n]['O_GC'] for n in non]):+.3f}, O_PN {np.mean([r[n]['O_PN'] for n in non]):+.3f}")
    rho = np.corrcoef([r[n]["O_GC"] for n in PAIR], [r[n]["O_PN"] for n in PAIR])[0, 1]
    P(f"    Pearson r(O_GC, O_PN) across galaxies: {rho:+.2f} (N {len(PAIR)}; descriptive)")

P("\n" + "-" * 116); P("CHECKS"); P("-" * 116)
if not MUTATE:
    dmax = max(abs(RES[foot][n]["O_GC"] - AUD[f"nu_mono|{foot}"][str(n)]["off"]) for foot in A0 for n in PAIR if str(n) in AUD[f"nu_mono|{foot}"])
    check("C1 GC offsets reproduce AUDIT_SLUGGS (nu_mono, both footings) within 0.005 dex", dmax < 0.005, f"max |diff| = {dmax:.5f} dex")
c2 = max(RES[foot][n]["C2"] for foot in A0 for n in PAIR)
check("C2 general-density Jeans solver (rho = r^-3) reproduces the power-law solver within 0.002 dex", c2 < 0.002, f"max |diff| = {c2:.2e} dex")
check("C3 every PN catalogue centred on its galaxy (median offset < 1 R_e, |dv| < 150 km/s)", c3, "see table above")
check("C4 >= 5 paired galaxies with >= 30 clean PNe and >= 2 bins", len(PAIR) >= 5, f"N_paired = {len(PAIR)}")
if MUTATE:
    true = json.load(open(os.path.join(HERE, "cfg492_gc_vs_pn_results.json")))["verdict"]
    for foot in A0:
        rt, rs = true[foot]["rms_delta"], VERD[foot]["rms_delta"]
        check(f"M1 ({foot}) shuffled pairing raises rms(Delta) above the true pairing", rs > rt, f"true {rt:.4f} -> shuffled {rs:.4f}")

fin = {k: v["verdict"] for k, v in VERD.items()}
both = fin["canonical"] if fin["canonical"] == fin["alt"] else "FOOTING-DEPENDENT"
P(f"\nVERDICT (frozen rules, both footings): {both}   [canonical: {fin['canonical']}; alt: {fin['alt']}]")
P(f"{sum(checks)}/{len(checks)} checks pass")
json.dump(dict(mutate=MUTATE, a0=A0, paired=PAIR, pn_only=PNONLY, verdict=VERD, final=both,
               per_galaxy={foot: {str(n): v for n, v in rows.items()} for foot, rows in RES.items()}),
          open(os.path.join(HERE, f"cfg492_gc_vs_pn{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg492_gc_vs_pn{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(checks) else 1)
