#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG57 -- THE HOT-GAS TEST ON SLUGGS: does each galaxy's measured hot X-ray gas, added to the baryons, close the globular-cluster deficit that
survived dynamical stellar masses (CFG55: law +0.097 +- 0.024 dex, 4.0 sigma; rule +0.046, 2.6 sigma)?

Criteria frozen and committed before any gas data were fetched and before any run: campaign_fresh_gravity/CFG57_FROZEN_CRITERIA.md (78a5a3a0a).
The owner approved the two sources in this session (Lakhchaura+2018 PDF; Fukazawa+2006 source); they were digitised / transcribed by
real_research/data/cfg57_gas_sources/ (its README states the digitisation error and validation).
  sample   CFG55's 16 intersected with the sources' coverage (fixed by coverage alone): Lakhchaura+2018 for NGC 4486 (M87), NGC 5846, NGC 4374,
           NGC 4649; Fukazawa+2006 for NGC 4365, NGC 4494, NGC 3607, NGC 4697 (and the first three as a cross-check).  Uncovered galaxies are
           reported without gas and are not in the headline mean.
  gas      spherical; rho_gas = mu_e m_p n_e, mu_e = 1.155.  Source 1: the digitised n_e(r), log-log interpolated; beyond the last point the
           power law of the outermost three points; inside the first point constant.  Source 2: beta = 0.5, r_c = 1 kpc normalised to
           n_e(10 kpc).  Moved to SLUGGS's distance: radii ~ D, n_e ~ D^-1/2.  No hydrostatic equilibrium assumed: gas enters as mass only.
  dynamics CFG55's machinery (exec'd read-only): the calibration nu(g_N/a0) [M_*/2 + M_gas(<r12)] (+ the rule's debris) = M_JAM/2 with g_N from
           the same enclosed baryons; the Jeans baryons M_* f_H(r) + M_gas(<r); the rule's collapse mass from M_*; its edge phantom from
           M_* + M_gas(<R_max of the source) (measured gas only).
PRE-DECLARED (from the frozen file)
  C1  CONTROL  CFG55's committed per-galaxy offsets reproduced with the gas set to zero on the covered subset (1e-9).
  C2  CONTROL  the transcription / digitisation: rows per source and one spot value; for a digitised curve, one printed number within 10%.
  C3  CONTROL  the numerical gas-mass integral of the beta model against its closed form (1e-8).
  H1  [HEADLINE; MUTATE must fail] with the measured hot gas the JAM-calibrated law fits the outer GCs of the covered galaxies: |mean| < 2 sigma
      (galaxy-to-galaxy), both footings.
  H2  the rule, with the same gas, fits: |mean| < 2 sigma, both footings.
  H3  (leverage) the gas moves the law's mean offset by more than that mean's error (else non-diagnostic).
  R   per-galaxy offsets with and without gas (M87, NGC 5846, NGC 4374 always shown); the gas each galaxy would need to null its law offset
      (the same shape, scaled); the outer extrapolation slope +-0.3; beta = 0.4 / 0.6 for source 2; the edge phantom from M_* only.
MUTATE=1: every gas density x 0 (the test reduces to CFG55 on the covered subset) -- H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG57_sluggs_hot_gas.py   (MUTATE=1 for the control)
"""
import os, sys, io, math, json, contextlib
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad
from scipy.special import hyp2f1

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG57_sluggs_hot_gas", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every gas density x 0 -- H1 must FAIL ***")
GF = 0.0 if MUTATE else 1.0
FOOTS = ("canonical", "alt")
MU_E, MP_G, KPC_CM, MSUN_G = 1.155, 1.67262192e-24, 3.0856775814913673e21, 1.98892e33
RHO_PER_NE = MU_E * MP_G * KPC_CM ** 3 / MSUN_G          # Msun / kpc^3 per (cm^-3)

# ------------------------------------------------------------------ CFG55's machinery, read-only
_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
src = open(os.path.join(HERE, "CFG55_sluggs_dynamical_masses.py")).read()
g55 = {"__file__": os.path.join(HERE, "CFG55_sluggs_dynamical_masses.py"), "__name__": "cfg55"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("\nRES = {}\n")], "CFG55", "exec"), g55)
os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
G16, sigma_los, sigma_r2, GAMMA, nu_h = g55["G16"], g55["sigma_los"], g55["sigma_r2"], g55["GAMMA"], g55["nu_h"]
collapse, edge_phantom, FB, nfw_enclosed, A0SI = g55["collapse"], g55["edge_phantom"], g55["FB"], g55["nfw_enclosed"], g55["A0SI"]
G_, KPC, MSUN = g55["G_"], g55["KPC"], g55["MSUN"]
c55 = json.load(open(os.path.join(HERE, "CFG55_sluggs_dynamical_masses_results.json")))["numbers"]
NAMES55 = c55["names"]

# ------------------------------------------------------------------ the gas data
DD = os.path.join(C.REPO, "real_research", "data", "cfg57_gas_sources")


def rd_tsv(fn):
    L = [l.rstrip("\n").split("\t") for l in open(os.path.join(DD, fn)) if l.strip() and not l.startswith("#")]
    H = [h.strip() for h in L[0]]
    return [dict(zip(H, [x.strip() for x in r])) for r in L[1:]]


LAK = {}
for r_ in rd_tsv("lakhchaura2018_ne_profiles.tsv"):
    LAK.setdefault(r_["name"], []).append(r_)
FUK = {r_["name"]: r_ for r_ in rd_tsv("fukazawa2006_table4.tsv")}
SRC1 = ["NGC4486", "NGC5846", "NGC4374", "NGC4649"]
SRC2 = ["NGC4365", "NGC4494", "NGC3607", "NGC4697"]
COVER = [n for n in NAMES55 if (n in SRC1 and n in LAK) or (n in SRC2 and n in FUK and math.isfinite(float(FUK[n]["ne10_1e-3cm3"])))]
UNCOVERED = [n for n in SRC2 if n not in COVER]


def fnum(s):
    try:
        return float(s)
    except Exception:
        return float("nan")


RGAS = np.geomspace(1e-3, 3e4, 4000)       # kpc (h50's Jeans grid runs to 3e4 kpc)


def gas_profile_src1(name, DS, dslope=0.0, drop_last=False):
    rows = sorted(LAK[name], key=lambda x: float(x["r_kpc"]))[:(-1 if drop_last else None)]
    Dp = fnum(rows[0]["D_Mpc_paper"])
    r = np.array([fnum(x["r_kpc"]) for x in rows]); ne = np.array([fnum(x["ne_cm3"]) for x in rows])
    o = np.argsort(r); r, ne = r[o], ne[o]
    f = DS / Dp
    r, ne = r * f, ne * f ** -0.5
    lr, ln = np.log(r), np.log(ne)
    s = np.polyfit(lr[-3:], ln[-3:], 1)[0] + dslope
    lg = np.log(RGAS)
    lne = np.where(lg <= lr[0], ln[0], np.where(lg >= lr[-1], ln[-1] + s * (lg - lr[-1]), np.interp(lg, lr, ln)))
    rho = RHO_PER_NE * np.exp(lne)
    return rho, float(r[-1]), s


def gas_profile_src2(name, DS, beta=0.5, rc=1.0):
    row = FUK[name]
    Dp = fnum(row["D_Mpc"]); f = DS / Dp
    ne10 = fnum(row["ne10_1e-3cm3"]) * 1e-3 * f ** -0.5
    r10 = 10.0 * f                                     # the paper's 10 kpc, moved to SLUGGS's distance
    shape = lambda x: (1 + (x / rc) ** 2) ** (-1.5 * beta)
    rho = RHO_PER_NE * ne10 * shape(RGAS) / shape(r10)
    return rho, fnum(row["Rmax_kpc"]) * f, None


def mass_fn(rho):
    dm = 4 * math.pi * RGAS ** 2 * rho
    M = np.concatenate([[dm[0] * RGAS[0] / 3], dm[0] * RGAS[0] / 3 + np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(RGAS))])
    lr = np.log(RGAS)
    return lambda rr: GF * np.interp(np.log(np.maximum(np.asarray(rr, float), RGAS[0])), lr, M)


def gas_for(g, which_src=None, dslope=0.0, beta=0.5, drop_last=False):
    n = g["name"]
    use1 = (n in SRC1 and n in LAK) if which_src is None else (which_src == 1)
    if use1:
        rho, Rmax, s = gas_profile_src1(n, g["DS"], dslope, drop_last)
        src_ = 1
    elif n in FUK and (n in SRC2 or which_src == 2):
        rho, Rmax, s = gas_profile_src2(n, g["DS"], beta=beta)
        src_ = 2
    else:
        return None
    return dict(M=mass_fn(rho), Rmax=Rmax, slope=s, src=src_)


# ------------------------------------------------------------------ the models with gas (identical for law and rule)
def debris(Ms, Mb_edge, foot):
    Mh = collapse(Ms, "red")
    return max(0.0, 1.0 - edge_phantom(Mb_edge, foot, 0.40) / ((1 - FB) * Mh)), Mh


def calib(g, foot, which, gas, edge_mstar_only=False):
    a0 = A0SI[foot]; r12 = g["r12"]
    Mg12 = float(gas["M"](r12)) if gas else 0.0
    Mge = (float(gas["M"](gas["Rmax"])) if gas else 0.0)

    def tot(lm):
        Ms = 10 ** lm; Mb12 = 0.5 * Ms + Mg12
        gN = G_ * Mb12 * MSUN / (r12 * KPC) ** 2
        t = Mb12 * float(nu_h(gN / a0))
        if which == "rule":
            fx, Mh = debris(Ms, Ms + (0.0 if edge_mstar_only else Mge), foot)
            t += fx * (1 - FB) * float(nfw_enclosed(Mh, r12))
        return t
    f = lambda lm: math.log10(tot(lm)) - math.log10(g["Mjam"] / 2)
    if f(6.0) * f(13.5) > 0:
        return float("nan")
    return 10 ** brentq(f, 6.0, 13.5, xtol=1e-12)


def offset(g, foot, Ms, which, gas, edge_mstar_only=False):
    r = g["r"]; a0 = A0SI[foot]; a_h = r["Re"] / 1.8153
    Mge = (float(gas["M"](gas["Rmax"])) if gas else 0.0)
    fx, Mh = debris(Ms, Ms + (0.0 if edge_mstar_only else Mge), foot) if which == "rule" else (0.0, 1.0)

    def gf(rr):
        Mb = Ms * MSUN * rr ** 2 / (rr + a_h) ** 2 + (gas["M"](rr) * MSUN if gas else 0.0)
        gN = G_ * Mb / (rr * KPC) ** 2
        out = gN * nu_h(gN / a0)
        if fx > 0:
            out = out + fx * (1 - FB) * G_ * np.asarray(nfw_enclosed(Mh, rr), float) * MSUN / (rr * KPC) ** 2
        return out
    s = sigma_los(r["Rb"], sigma_r2(gf, GAMMA), GAMMA)
    return float(np.mean(np.log10(r["Sb"][r["out"]] / s[r["out"]])))


def run(foot, which, gasmap, **kw):
    per = {}
    for g in G16:
        if g["name"] not in COVER:
            continue
        gas = gasmap.get(g["name"])
        Ms = calib(g, foot, which, gas, **kw)
        per[g["name"]] = (offset(g, foot, Ms, which, gas, **kw) if np.isfinite(Ms) else float("nan"), Ms)
    v = np.array([x[0] for x in per.values() if np.isfinite(x[0])])
    return per, float(v.mean()), float(v.std(ddof=1) / math.sqrt(len(v))), len(v)


# ------------------------------------------------------------------ C1 / C3
R.banner("C1 / C3  CONTROLS")
dev = 0.0
for foot in FOOTS:
    for which in ("law", "rule"):
        per0, *_ = run(foot, which, {})
        com = dict(zip(NAMES55, c55["RES"][foot][which]["per"]))
        dev = max(dev, max(abs(per0[n][0] - com[n]) for n in per0 if np.isfinite(per0[n][0])))
check("C1 CONTROL: CFG55's committed per-galaxy offsets reproduced with the gas set to zero on the covered subset (1e-9)",
      f"covered = {COVER}; max |deviation| {dev:.1e} dex", dev < 1e-9)
b_, rc_ = 0.5, 1.0
xx = 7.3
num = quad(lambda x: x * x * (1 + x * x) ** (-1.5 * b_), 0, xx, epsabs=1e-14, epsrel=1e-13)[0]
closed = xx ** 3 / 3 * hyp2f1(1.5 * b_, 1.5, 2.5, -xx * xx)
check("C3 CONTROL: the beta-model gas-mass integral against its closed form (x^3/3) 2F1(3b/2, 3/2; 5/2; -x^2) (1e-8)",
      f"numerical {num:.12f}, closed {closed:.12f}, rel. dev. {abs(num / closed - 1):.1e}", abs(num / closed - 1) < 1e-8)

nL = {n: len(LAK.get(n, [])) for n in SRC1}
spot = FUK.get("NGC5846", {})
ext = open(os.path.join(DD, "extract_lakhchaura.out")).read()
import re as _re
mv1 = _re.search(r"V1 RESULT \(four targets\): max \|digitised/printed - 1\| = ([0-9.e+-]+) \(kT\), ([0-9.e+-]+) \(LX\)", ext)
v1 = max(float(mv1.group(1)), float(mv1.group(2))) if mv1 else float("nan")
v3 = [float(x) for x in _re.findall(r"\(a\) shells cut at 10 kpc: [0-9.e+]+, ratio ([0-9.]+)", ext)]
check("C2 CONTROL: the transcription / digitisation -- rows per source; a Fukazawa spot value (NGC 5846 n_e(10 kpc) = 7.17e-3, D 22.9 Mpc); "
      "the digitisation method reproduces the paper's PRINTED numbers (Table 1 kT, L_X of the four targets) within 10%",
      f"Lakhchaura rows {nL} (80 total); Fukazawa NGC5846 ne10 {spot.get('ne10_1e-3cm3')} D {spot.get('D_Mpc')}; V1 max |dig/printed - 1| {v1:.1e}; "
      f"reported: the density profiles integrated to 10 kpc (whole shells cut at 10 kpc) against the paper's PLOTTED Fig. 1 gas masses: ratios {v3} "
      f"(no per-galaxy density or gas mass is printed; a whole-shell scheme found after two others fell short matches to 1.002 -- see the data README)",
      sum(nL.values()) == 80 and spot.get("ne10_1e-3cm3") == "7.17" and spot.get("D_Mpc") == "22.9" and v1 < 0.10)
P(f"    uncovered (the source lacks the needed quantity): {UNCOVERED}; covered: {COVER}")

# ------------------------------------------------------------------ the gas maps and the main runs
GAS = {g["name"]: gas_for(g) for g in G16 if g["name"] in COVER}
P("\n    gas per covered galaxy (SLUGGS distance): " + "; ".join(
    f"{n} src{v['src']} M_gas(<r12) {float(v['M'](g['r12'])):.2e}, (<20 kpc) {float(v['M'](20.0)):.2e}, (<50 kpc) {float(v['M'](50.0)):.2e}, "
    f"R_max {v['Rmax']:.0f} kpc" + (f", outer slope {v['slope']:.2f}" if v["slope"] is not None else "")
    for g in G16 for n, v in GAS.items() if g["name"] == n and v))
RES = {}
for foot in FOOTS:
    for which in ("law", "rule"):
        RES[(foot, which, "gas")] = run(foot, which, GAS)
        RES[(foot, which, "nogas")] = run(foot, which, {})

R.banner("PER GALAXY (canonical): offsets without and with the measured hot gas")
for n in COVER:
    a = RES[("canonical", "law", "nogas")][0][n][0]; b = RES[("canonical", "law", "gas")][0][n][0]
    c_ = RES[("canonical", "rule", "nogas")][0][n][0]; d = RES[("canonical", "rule", "gas")][0][n][0]
    P(f"    {n:8s} (source {GAS[n]['src'] if GAS.get(n) else '-'}): law {a:+.3f} -> {b:+.3f}; rule {c_:+.3f} -> {d:+.3f}")
for foot in FOOTS:
    for which in ("law", "rule"):
        _, m0, e0, n0 = RES[(foot, which, "nogas")]; _, m1, e1, n1 = RES[(foot, which, "gas")]
        P(f"    {foot:9s} {which:4s}: without gas {m0:+.4f} +- {e0:.4f} ({m0 / e0:+.2f} sigma, n={n0}); with gas {m1:+.4f} +- {e1:.4f} ({m1 / e1:+.2f} sigma, n={n1})")

R.banner("H1 / H2 / H3")
z1 = {f: RES[(f, "law", "gas")][1] / RES[(f, "law", "gas")][2] for f in FOOTS}
z2 = {f: RES[(f, "rule", "gas")][1] / RES[(f, "rule", "gas")][2] for f in FOOTS}
check("H1 [HEADLINE] WITH THE MEASURED HOT GAS THE JAM-CALIBRATED LAW FITS THE OUTER GCs: |mean| < 2 sigma, both footings"
      + ("  [MUTATE: gas x 0]" if MUTATE else ""),
      "; ".join(f"{f}: {RES[(f, 'law', 'gas')][1]:+.4f} +- {RES[(f, 'law', 'gas')][2]:.4f} ({z1[f]:+.2f} sigma)" for f in FOOTS),
      all(abs(z) < 2 for z in z1.values()))
check("H2 THE RULE, WITH THE SAME GAS, FITS: |mean| < 2 sigma, both footings",
      "; ".join(f"{f}: {RES[(f, 'rule', 'gas')][1]:+.4f} ({z2[f]:+.2f} sigma)" for f in FOOTS), all(abs(z) < 2 for z in z2.values()))
lev = {f: RES[(f, "law", "nogas")][1] - RES[(f, "law", "gas")][1] for f in FOOTS}
h3 = all(abs(lev[f]) > RES[(f, "law", "gas")][2] for f in FOOTS)
check("H3 (leverage) the gas moves the law's mean offset by more than its error, both footings",
      "; ".join(f"{f}: shift {lev[f]:+.4f} vs error {RES[(f, 'law', 'gas')][2]:.4f}" for f in FOOTS), h3, load_bearing=False)

R.banner("REPORTED ROWS (canonical)")
# the gas each galaxy would need to null its law offset: scale the same profile by k
need = {}
for g in G16:
    n = g["name"]
    if n not in COVER or not GAS.get(n):
        continue
    base = GAS[n]

    def off_k(k):
        gk = dict(base, M=(lambda rr, b=base, kk=k: kk * b["M"](rr)))
        Ms = calib(g, "canonical", "law", gk)
        return offset(g, "canonical", Ms, "law", gk) if np.isfinite(Ms) else float("nan")
    o1 = off_k(1.0)
    kk = None
    for k in (1.5, 2, 3, 5, 8, 13, 20, 35, 60, 100):
        ok = off_k(k)
        if np.isfinite(ok) and ok <= 0:
            lo, hi = (1.0 if o1 > 0 else 0.0), float(k)
            for _ in range(30):
                mid = 0.5 * (lo + hi)
                om = off_k(mid)
                if np.isfinite(om) and om > 0: lo = mid
                else: hi = mid
            kk = hi; break
    need[n] = dict(k=kk, M50=(kk * float(base["M"](50.0)) if kk else None), off_at_1=o1)
check("R1 (reported) the gas each covered galaxy would need to null its law offset (the measured profile scaled by k; M_gas(<50 kpc) at that k)",
      "; ".join(f"{n}: k {v['k']:.2f}, M_gas(<50 kpc) {v['M50']:.2e}" if v["k"] else f"{n}: offset {v['off_at_1']:+.3f} at k = 1, no k <= 100 nulls it"
                for n, v in need.items()), True, load_bearing=False)
sl = {}
for dsl in (+0.3, -0.3):
    gm = {n: (gas_for(g, dslope=dsl) if GAS.get(n) and GAS[n]["src"] == 1 else GAS.get(n)) for g in G16 for n in [g["name"]] if n in COVER}
    sl[dsl] = run("canonical", "law", gm)[1]
check("R2 (reported) the outer extrapolation slope +-0.3 (source 1): the law's mean",
      f"+0.3: {sl[0.3]:+.4f}; -0.3: {sl[-0.3]:+.4f} (headline {RES[('canonical', 'law', 'gas')][1]:+.4f})", True, load_bearing=False)
bt = {}
for b in (0.4, 0.6):
    gm = {n: (gas_for(g, beta=b) if GAS.get(n) and GAS[n]["src"] == 2 else GAS.get(n)) for g in G16 for n in [g["name"]] if n in COVER}
    bt[b] = run("canonical", "law", gm)[1]
check("R3 (reported) beta = 0.4 / 0.6 for source 2: the law's mean", f"0.4: {bt[0.4]:+.4f}; 0.6: {bt[0.6]:+.4f}", True, load_bearing=False)
xs = {}
for n in SRC1:
    g = [x for x in G16 if x["name"] == n][0]
    if n in FUK:
        g1, g2 = gas_for(g, which_src=1), gas_for(g, which_src=2)
        xs[n] = (float(g1["M"](20.0)), float(g2["M"](20.0)))
check("R4 (reported) source 2 as a cross-check where both sources cover a galaxy: M_gas(<20 kpc) Lakhchaura vs Fukazawa",
      "; ".join(f"{n}: {a:.2e} vs {b:.2e}" for n, (a, b) in xs.items()), True, load_bearing=False)
eo = run("canonical", "rule", GAS, edge_mstar_only=True)[1]
check("R5 (reported) the rule with its edge phantom from M_* only", f"rule mean {eo:+.4f} (headline {RES[('canonical', 'rule', 'gas')][1]:+.4f})",
      True, load_bearing=False)

# ---- DISCLOSED DEPARTURE (declared after seeing the digitised profiles; the frozen verdicts above are unchanged) ----
# The frozen extrapolation (power law of the outermost three points) inherits an upturned OUTERMOST shell in three Lakhchaura profiles (a
# deprojection edge effect: the last shell absorbs the emission of gas beyond the field), giving outer slopes of +2 to +4 -- a density
# rising outward to 3e4 kpc, i.e. unbounded gas.  D1 drops the outermost shell of each Lakhchaura profile and fits the three points before it.
fs = {n: GAS[n]["slope"] for n in COVER if GAS.get(n) and GAS[n]["src"] == 1}
check("D0 (reported) the frozen rule's outer slopes (source 1): positive slopes mean a density rising outward without bound",
      "; ".join(f"{n} {v:+.2f}" for n, v in fs.items()), True, load_bearing=False)
GASD = {g["name"]: gas_for(g, drop_last=True) for g in G16 if g["name"] in COVER}
DEP = {}
for foot in FOOTS:
    for which in ("law", "rule"):
        DEP[(foot, which)] = run(foot, which, GASD)
check("D1 (reported; DISCLOSED departure, post hoc) the outermost Lakhchaura shell dropped, the slope fitted to the three points before it",
      "slopes " + "; ".join(f"{n} {GASD[n]['slope']:+.2f}" for n in fs) + " | " +
      "; ".join(f"{f} {w}: {DEP[(f, w)][1]:+.4f} +- {DEP[(f, w)][2]:.4f} ({DEP[(f, w)][1] / DEP[(f, w)][2]:+.2f} sigma)" for f in FOOTS for w in ("law", "rule")),
      True, load_bearing=False)
P("    D1 per galaxy (canonical): " + "; ".join(f"{n} law {DEP[('canonical', 'law')][0][n][0]:+.3f} rule {DEP[('canonical', 'rule')][0][n][0]:+.3f}" for n in COVER))
d1s = {}
for dsl in (+0.3, -0.3):
    gm = {g["name"]: (gas_for(g, dslope=dsl, drop_last=True) if GAS.get(g["name"]) and GAS[g["name"]]["src"] == 1 else GAS.get(g["name"])) for g in G16 if g["name"] in COVER}
    d1s[dsl] = run("canonical", "law", gm)[1]
check("D2 (reported; with D1) the outer slope +-0.3 around the D1 slopes: the law's mean", f"+0.3: {d1s[0.3]:+.4f}; -0.3: {d1s[-0.3]:+.4f}",
      True, load_bearing=False)
R.num("D1", {f"{k[0]}|{k[1]}": dict(mean=v[1], err=v[2], per={n: x[0] for n, x in v[0].items()}) for k, v in DEP.items()}); R.num("D0_slopes", fs)
# D3 (added after the first run, reported only): the frozen H1 / H2 / H3 and the frozen reading map applied to D1, same code paths as above
z1d = {f: DEP[(f, "law")][1] / DEP[(f, "law")][2] for f in FOOTS}
z2d = {f: DEP[(f, "rule")][1] / DEP[(f, "rule")][2] for f in FOOTS}
levd = {f: RES[(f, "law", "nogas")][1] - DEP[(f, "law")][1] for f in FOOTS}
h1d = all(abs(z) < 2 for z in z1d.values())
h3d = all(abs(levd[f]) > DEP[(f, "law")][2] for f in FOOTS)
if not h3d:
    read_d1 = "non-diagnostic: the measured gas moves the law's mean by less than its error"
elif h1d:
    read_d1 = "the SLUGGS deficit is baryonic: the measured hot gas closes it"
else:
    read_d1 = ("the deficit survives the measured gas as well"
               + ("; the rule supplies it" if all(abs(z) < 2 for z in z2d.values()) else "; the rule does not close it"))
check("D3 (reported; with D1) the frozen H1, H2 and H3 applied to D1, and the frozen reading map",
      "; ".join(f"{f}: H1 {'PASS' if abs(z1d[f]) < 2 else 'FAIL'} ({z1d[f]:+.2f} sigma), H2 {'PASS' if abs(z2d[f]) < 2 else 'FAIL'} "
                f"({z2d[f]:+.2f} sigma), H3 {'PASS' if abs(levd[f]) > DEP[(f, 'law')][2] else 'FAIL'} (shift {levd[f]:+.4f} vs error "
                f"{DEP[(f, 'law')][2]:.4f})" for f in FOOTS) + f" -> reading: {read_d1}", True, load_bearing=False)
R.num("D3", dict(z1=z1d, z2=z2d, shift=levd, h1=h1d, h3=h3d, reading=read_d1))

h1 = all(abs(z) < 2 for z in z1.values())
if not h3:
    reading = "non-diagnostic: the measured gas moves the law's mean by less than its error"
elif h1:
    reading = ("the SLUGGS deficit is baryonic: the measured hot gas closes it, and B's derived rule loses its last supporting population"
               + ("; the rule, with the same gas, also fits" if all(abs(z) < 2 for z in z2.values()) else "; the rule, with the same gas, over- or under-shoots"))
else:
    reading = ("the deficit survives the measured gas as well: the massive early types want mass beyond the law's baryons"
               + ("; the rule supplies it" if all(abs(z) < 2 for z in z2.values()) else "; the rule does not close it"))
P(f"\n    READING (declared, mechanical): {reading}")
P("    DISCLOSED: the frozen extrapolation is non-physical on these profiles (row D0: positive outer slopes from the upturned last shell), so "
  "the mechanical reading is not interpretable; the disclosed departure D1 (outermost shell dropped) is the physically meaningful variant.")
P(f"    D1 under the frozen reading map (row D3): {read_d1}.")
R.num("covered", COVER); R.num("need", need); R.num("R2", {str(k): v for k, v in sl.items()}); R.num("R3", {str(k): v for k, v in bt.items()})
R.num("RES", {f"{k[0]}|{k[1]}|{k[2]}": dict(per={n: v[0] for n, v in val[0].items()}, mean=val[1], err=val[2], n=val[3]) for k, val in RES.items()})
R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
