#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG79 -- A LCDM COMPARATOR FOR THE X-RAY ELLIPTICALS (CFG32): through CFG32's IDENTICAL pipeline, does a standard LCDM halo also fall short?

Criteria frozen and committed before this script existed: campaign_fresh_gravity/CFG79_FROZEN_CRITERIA.md (commit 6cdfb9d8f), written before any LCDM
prediction for these seven galaxies was computed.  CFG32 found candidate B's law short of Humphrey+2006's hydrostatic masses (NGC 720, 1407, 4125, 4261,
4472, 4649, 6482) by +0.280 / +0.254 dex (a factor 1.91 / 1.79) at 1.70 / 1.58 sigma (canonical / alt), the shortfall growing outward in 7 of 7.

IDENTICAL TO CFG32 (exec'd read-only, its MUTATE forced off): h10's data and fitted model for g_obs (Hernquist stars at Humphrey's fitted M/L + his best-fit
NFW); the baryons (stars only, Hernquist a = R_e/1.8153, Kroupa population M/L; no hot gas); radii 5, 10, 20, 40, 70 kpc; a point's offset log10(g_obs /
g_model); a galaxy's offset the median over its radii; the sample offset the mean of the seven; the galaxy-to-galaxy error std/sqrt(7); the floor (IMF:
Kroupa -> Salpeter; radial range: r <= 40 kpc) recomputed by the same method through each model's pipeline, in quadrature.  B = CFG32's own numbers.
THE LCDM MODEL (declared once, no tuning; CFG69's base): g = G [M_stars(<r) + (1 - f_b) M_NFW(<r)] / r^2, Newtonian (nu = 1); M_h = Moster+2013 `halo_mass`
of the Kroupa M_* (h48's; obtained with FB and RHO_C exactly as CFG69 does, from CFG45's exec'd prefix); Duffy+2008 full-sample 200c concentration;
CFG69's make_nfw copied verbatim (normalised to M_h at R200c, x clipped to [1e-4, 5]).  No adiabatic contraction, no SHMR scatter (declared untested).
LCDM has no a0: identical on both footings.  The Salpeter floor row changes only the stars (the halo stays at the Kroupa-M_* Moster mass, CFG69's convention).
CIRCULARITY (stated in the frozen file): CFG32's g_obs is itself a best-fit NFW + stars model -- not circular in value (no LCDM input comes from that fit),
but FORM-MATCHED (LCDM is scored against data in its own functional form).  Caveat: group/cluster-central ellipticals; the Moster halo of the central
galaxy's M_* may be smaller than the group halo; stated, not fixed.
CLASSES (CFG69's): B FAIL |z| > 2 / MARGINAL 1 < |z| <= 2 / OK; for a FAIL or MARGINAL B: LCDM |z| <= 2 SPECIFIC-TO-B; same sign and |z| > 2 SHARED;
opposite sign and |z| > 2 LCDM-WORSE; footings differ -> MIXED.  NON-DISCRIMINATING (overrides): every M_h x 100 leaves LCDM's three-way class unchanged.
PRE-DECLARED
  C1  CONTROL  CFG32's committed B numbers reproduced through the exec of its pipeline: (a) at its printed precision against its committed .out, (b) to
               1e-9 against its committed JSON, (c) the generic estimator used for LCDM, run with B's law, reproduces them to 1e-12.  Both footings.
  C2  CONTROL  NFW M(<R200c) = M_h to 1e-12 for every halo used; make_nfw equals the numerical integral of the NFW density to 1e-7 at the five radii
               (every base, V1, V2 halo), monotone in r.
  C3  CONTROL  M_h -> 0 gives CFG32's g_obs/g_bar (1e-12); LCDM identical with the canonical and the alt a0; g_LCDM >= g_bar everywhere.
  C4  CONTROL  every M_* fed to halo_mass lies inside h48's Moster grid (no clamp); moster_mstar(halo_mass(M_*)) = M_* to 1e-6.
  H1a [HEADLINE] NOT SHARED: LCDM (base) is not off in B's direction at > 2 sigma.
  H1b [HEADLINE] NOT LCDM-WORSE: LCDM (base) is not off in the opposite direction at > 2 sigma.      (H1a and H1b pass <=> SPECIFIC-TO-B)
  H1c [HEADLINE; the NON-DISCRIMINATING test] THE GATE SEES THE HALO: LCDM's class with every declared M_h x 100 differs from its class with the declared M_h
      (both computed in every run).
  M1  [MUTATE detector] THE SCORED CLASS IS THE DECLARED CLASS (passes by construction in the main run; under MUTATE fails exactly when H1c passes).
  H1  (reported) the final label; B minus LCDM.
  R1-R6 (reported): per-galaxy offsets; the halos beside Humphrey's fits; V1 Dutton-Maccio c, V2 Duffy relaxed, V3 / V4 every M_h x 1/3 and x 3; the floor
      readings (M_h from the Salpeter M_*; B's floor on LCDM; CFG32's R1 row); LCDM's residual shape; the halo ladder x 1/100, x 1, x 100.
MUTATE=1: every LCDM halo mass x 100 (base and V1-V4; B untouched; the R6 ladder and H1c stay relative to the declared halos).  The MUTATE run always exits 1
(H1c or M1 fails); its failing set differs from the main run's exactly when H1c passes.
ADDED AFTER THE FIRST MAIN RUN, BEFORE THE MUTATE RUN (disclosed; the first run's log is kept as CFG79_lcdm_xray_ellipticals_first_run.out; NO hypothesis, gate,
  threshold, model choice or classification rule changed): control C4 FAILED as declared -- the round trip moster_mstar(halo_mass(M_*)) reproduces M_* to 1.1e-6,
  not 1e-6 (the tolerance came from a pre-run estimate of h48's 0.005-dex interpolation error made at the high-mass end only; at NGC 720's lower mass the
  relation curves more).  It is kept as a FAIL, tolerance unchanged.  Supplemental, REPORTED-ONLY row R7 to size it: the base LCDM with M_h from an exact
  inversion of moster_mstar (brentq) in place of h48's interpolated halo_mass.  The declared model still uses h48's halo_mass.
kappa = 1/2 and Omega_c h^2 stay FITTED.  Nothing here says the data favour either model, and nothing says the theory is closed.
Run: python3 campaign_fresh_gravity/CFG79_lcdm_xray_ellipticals.py   (MUTATE=1 for the control; ~15 s)
"""
import os, sys, math, io, re, json, contextlib, time
sys.dont_write_bytecode = True
import numpy as np
from scipy import integrate
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = HERE
sys.path.insert(0, LANES)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG79_lcdm_xray_ellipticals", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every LCDM halo mass x 100 (base and V1-V4; B untouched) -- the run must exit 1 (H1c or M1 fails) ***")
HMUT = 100.0 if MUTATE else 1.0
FOOTS = ("canonical", "alt")
FROZEN_COMMIT = "6cdfb9d8f"
T0 = time.time()


# ================================================================================================ read-only exec of the lanes (their own MUTATE forced off)
def exec_prefix(fname, marker, replace=None):
    _e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    src = open(os.path.join(LANES, fname)).read()
    pre = src[:src.index(marker)]
    for a, b in (replace or []):
        assert pre.count(a) == 1
        pre = pre.replace(a, b)
    g = {"__file__": os.path.join(LANES, fname), "__name__": "lane_" + fname}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(pre, fname, "exec"), g)
    finally:
        os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
    return g


BAR = "# ================================================================================================ "
g45 = exec_prefix("CFG45_rule_readings.py", BAR + "P3 SPARC", [('READ = ("L", "S", "M", "E")', 'READ = ("L", "S")')])
FB, halo_mass, RHO_C = g45["FB"], g45["halo_mass"], g45["RHO_C"]
H48 = halo_mass.__globals__                       # h48's exec'd namespace (the Moster relation and its grid)
moster_mstar, LMS, LMH = H48["moster_mstar"], np.asarray(H48["_LMS"], float), np.asarray(H48["_LMH"], float)
g32 = exec_prefix("CFG32_xray_ellipticals_under_b.py", "nf = R.write()")      # everything CFG32 computes, nothing it writes
assert not g32["MUTATE"] and g32["GSC"] == 1.0
GAL, M_hern, M_nfw, points32, RES32 = g32["GAL"], g32["M_hern"], g32["M_nfw"], g32["points"], g32["RES"]
G_, KPC, MSUN, A0B, KERN, RADII = g32["G_"], g32["KPC"], g32["MSUN"], g32["A0B"], g32["KERN"], g32["RADII"]
R40 = (5.0, 10.0, 20.0, 40.0)
NAMES = [g["name"] for g in GAL]
P(f"\n  exec'd read-only: CFG45 prefix (halo_mass, FB = {FB:.5f}, RHO_C = {RHO_C:.4e} Msun/Mpc^3) and CFG32 (up to its write): {len(GAL)} galaxies: "
  + ", ".join(NAMES) + f"   ({time.time() - T0:.0f} s)")

# ================================================================================================ the LCDM halo (CFG69's functions, copied verbatim)
HH = 0.674


def c_duffy_full(Mh):
    return 5.71 * (np.asarray(Mh, float) / (2e12 / HH)) ** (-0.084)


def c_duffy_relaxed(Mh):
    return 6.71 * (np.asarray(Mh, float) / (2e12 / HH)) ** (-0.091)


def c_dm(Mh):
    return 10 ** (0.905 - 0.101 * (np.log10(np.asarray(Mh, float) * 0.674) - 12.0))


def _m_nfw(t):
    return np.log1p(t) - t / (1 + t)


def make_nfw(cfn):
    def f(Mh, r_kpc):
        Mh = np.asarray(Mh, float); r_kpc = np.asarray(r_kpc, float)
        c = cfn(Mh); R200 = (3 * Mh / (4 * math.pi * 200 * RHO_C)) ** (1 / 3.) * 1000.0
        x = np.clip(r_kpc / R200, 1e-4, 5.0)
        return Mh * _m_nfw(c * x) / _m_nfw(c)
    return f


def r200(Mh):
    return (3 * Mh / (4 * math.pi * 200 * RHO_C)) ** (1 / 3.) * 1000.0


CFGS = {
    "base": dict(label="Moster + Duffy full 200c (THE declared LCDM)", cfn=c_duffy_full, hmf=HMUT),
    "V1": dict(label="V1 Moster + Dutton-Maccio c", cfn=c_dm, hmf=HMUT),
    "V2": dict(label="V2 Moster + Duffy relaxed 200c", cfn=c_duffy_relaxed, hmf=HMUT),
    "V3": dict(label="V3 base, every M_h x 1/3", cfn=c_duffy_full, hmf=HMUT / 3.0),
    "V4": dict(label="V4 base, every M_h x 3", cfn=c_duffy_full, hmf=HMUT * 3.0),
}
LADDER = (0.01, 1.0, 100.0)          # relative to the DECLARED halos in every run (R6); x1 and x100 feed H1c and M1


def mstar(g, ups="uk"):
    return g[ups] * g["LK"]


def halo_of(g, hmf, halo_ups="uk"):
    """the Moster M_200c of the galaxy (from the Kroupa M_* unless the reported R4a mapping asks otherwise) times the declared multiple."""
    return float(halo_mass(mstar(g, halo_ups))) * hmf


# ================================================================================================ the generic estimator (CFG32's points / sample / H1 block, with a model switch)
def pts(g, boost, ups="uk", radii=RADII, a0=A0B["canonical"]):
    """CFG32's points(), line for line; the model enters only as boost(g, r, Mb, y) = g_model / g_bar."""
    Mfit = g["uf"] * g["LK"]; Mdm = max(g["Mvir"] - Mfit, 1e9); Ms = g[ups] * g["LK"]
    out = []
    for r in radii:
        Mtot = M_hern(r, Mfit, g["Re"]) + M_nfw(r, Mdm, g["Rvir"], g["c"])
        Mb = M_hern(r, Ms, g["Re"])
        rr = r * KPC; gobs = G_ * Mtot * MSUN / rr ** 2; gb = G_ * Mb * MSUN / rr ** 2
        y = gb / a0; nu_ = boost(g, r, Mb, y)
        out.append(dict(r=r, y=y, obs=gobs / gb, nu=nu_, ratio=gobs / gb / nu_, gobs=gobs, gb=gb))
    return out


def samp(boost, **kw):
    per = np.array([np.median([math.log10(p["ratio"]) for p in pts(g, boost, **kw)]) for g in GAL])
    return dict(per=per, mean=float(per.mean()), err=float(per.std(ddof=1) / math.sqrt(len(per))), median=float(np.median(per)))


def score(bmaker, a0=A0B["canonical"]):
    """CFG32's H1 block: base (Kroupa, five radii), Salpeter, r <= 40 kpc; floor = hypot(IMF, radial); sigma = hypot(err, floor); z = mean / sigma."""
    base = samp(bmaker("uk"), a0=a0)
    salp = samp(bmaker("us"), ups="us", a0=a0)
    r40 = samp(bmaker("uk"), radii=R40, a0=a0)
    imf, rad = abs(salp["mean"] - base["mean"]), abs(r40["mean"] - base["mean"])
    floor = math.hypot(imf, rad); tot = math.hypot(base["err"], floor)
    return dict(base=base, salp=salp, r40=r40, imf_term=imf, radial_term=rad, floor=floor, tot=tot, z=base["mean"] / tot)


def b_boost(g, r, Mb, y):
    return float(KERN["nu_mono"](np.array([y]))[0])


def lcdm_boost(cfn, hmf, halo_ups="uk", mh_fixed=None):
    prof = make_nfw(cfn); cache = {}

    def b(g, r, Mb, y):
        if g["name"] not in cache:
            cache[g["name"]] = halo_of(g, hmf, halo_ups) if mh_fixed is None else mh_fixed
        return 1.0 + (1 - FB) * float(prof(cache[g["name"]], r)) / Mb
    return b


def status(z):
    return "FAIL" if abs(z) > 2 else ("MARGINAL" if abs(z) > 1 else "OK")


def classify(zb, zl):
    st = status(zb)
    if st == "OK":
        return "B-ok"
    if abs(zl) <= 2:
        return "SPECIFIC-TO-B"
    return "SHARED" if (zb > 0) == (zl > 0) else "LCDM-WORSE"


ZB = {f: RES32[f]["z"] for f in FOOTS}


def class_of(zl):
    cl = {f: classify(ZB[f], zl) for f in FOOTS}
    return cl["canonical"] if cl["canonical"] == cl["alt"] else f"MIXED({cl['canonical']}|{cl['alt']})"


# ================================================================================================ C4 / C2  the Moster grid and the NFW profile (before any offset is read)
R.banner("C4 / C2  CONTROLS: the Moster grid and the NFW profile")
lo_, hi_ = float(LMS.min()), float(LMS.max()); mono_grid = bool(np.all(np.diff(LMS) > 0))
outside, rt = [], 0.0
for g in GAL:
    for u in ("uk", "us", "uf"):
        lm = math.log10(mstar(g, u))
        if not (lo_ < lm < hi_):
            outside.append(f"{g['name']}:{u}")
        rt = max(rt, abs(float(moster_mstar(math.log10(float(halo_mass(mstar(g, u)))))) / mstar(g, u) - 1.0))
check("C4 CONTROL: every M_* fed to halo_mass (Kroupa; Salpeter and fitted for R4) lies inside h48's Moster grid (no clamp), and "
      "moster_mstar(halo_mass(M_*)) = M_* to 1e-6",
      f"grid log M_* {lo_:.2f} - {hi_:.2f} (log M_h {LMH.min():.1f} - {LMH.max():.1f}), monotone {mono_grid}; M_* used log {min(math.log10(mstar(g, u)) for g in GAL for u in ('uk', 'us', 'uf')):.2f} - "
      f"{max(math.log10(mstar(g, u)) for g in GAL for u in ('uk', 'us', 'uf')):.2f}; outside: {', '.join(outside) or 'none'}; max round-trip |dM/M| {rt:.1e}",
      mono_grid and not outside and rt <= 1e-6)


def quad_nfw(c, X):
    I = lambda T: integrate.quad(lambda t: t * t / (t * (1 + t) ** 2), 0.0, T, epsabs=0.0, epsrel=1e-12, limit=400)[0]
    return I(X) / I(c)


halos_used = []      # (label, Mh, cfn)
for name, v in CFGS.items():
    halos_used += [(f"{name}:{g['name']}", halo_of(g, v["hmf"]), v["cfn"]) for g in GAL]
for m_ in LADDER:
    halos_used += [(f"x{m_:g}:{g['name']}", halo_of(g, m_), c_duffy_full) for g in GAL]
for u in ("us", "uf"):
    halos_used += [(f"R4-{u}:{g['name']}", halo_of(g, HMUT, u), c_duffy_full) for g in GAL]
dev_n = max(abs(float(make_nfw(cf)(Mh, r200(Mh))) / Mh - 1.0) for _, Mh, cf in halos_used)
dev_q, mono = 0.0, True
for name in ("base", "V1", "V2"):
    cf = CFGS[name]["cfn"]; prof = make_nfw(cf)
    for g in GAL:
        Mh = halo_of(g, CFGS[name]["hmf"]); c = float(cf(Mh)); R2 = r200(Mh)
        for r in RADII:
            dev_q = max(dev_q, abs(float(prof(Mh, r)) / (Mh * quad_nfw(c, c * min(max(r / R2, 1e-4), 5.0))) - 1.0))
        # monotone over the profile's declared domain x = r/R200c in [1e-4, 5] (CFG69's clip makes it flat outside by construction)
        rr = np.logspace(math.log10(2e-4 * R2), math.log10(5 * R2), 200); mono = mono and bool(np.all(np.diff(np.asarray(prof(Mh, rr))) > 0))
check("C2 CONTROL: NFW M(<R200c) = M_h to 1e-12 for every halo used (base, V1-V4, the R6 ladder, the R4 mappings); make_nfw equals the numerical integral "
      "of the NFW density to 1e-7 at the five radii (every base, V1, V2 halo), monotone in r",
      f"{len(halos_used)} halos: max |M(<R200c)/M_h - 1| {dev_n:.1e}; max |closed form / integral - 1| {dev_q:.1e}; monotone {mono}",
      dev_n <= 1e-12 and dev_q <= 1e-7 and mono)

# ================================================================================================ C1  CFG32 reproduced
R.banner("C1  CONTROL: CFG32's committed B numbers reproduced through the exec of its pipeline")
out32 = open(os.path.join(LANES, "CFG32_xray_ellipticals_under_b.out")).read()
js32 = json.load(open(os.path.join(LANES, "CFG32_xray_ellipticals_under_b_results.json")))["numbers"]["RES"]
mis = []
for f in FOOTS:
    v = RES32[f]
    m = re.search(rf"{f}\s*: per-galaxy offsets \(Kroupa\) ([^\n]*)\n\s*mean (\S+) \+- (\S+) \(galaxy-to-galaxy\); floor (\S+) \(IMF (\S+), radial range (\S+)\) "
                  rf"-> (\S+) sigma;\s+Salpeter (\S+), fitted M/L (\S+), r <= 40 kpc (\S+), P2 (\S+)", out32)
    h = re.search(rf"{f}: (\S+) \+- (\S+) dex \((\S+) sigma; a factor ([0-9.]+)\)", out32)
    if not (m and h):
        mis.append(f"{f}: committed lines not found"); continue
    mine = [", ".join(f"{n} {o:+.2f}" for n, o in zip(NAMES, v["base"]["per"])), f"{v['base']['mean']:+.3f}", f"{v['base']['err']:.3f}", f"{v['floor']:.3f}",
            f"{v['imf_term']:.3f}", f"{v['radial_term']:.3f}", f"{v['z']:+.2f}", f"{v['salp']['mean']:+.3f}", f"{v['fit']['mean']:+.3f}", f"{v['r40']['mean']:+.3f}",
            f"{v['p2']['mean']:+.3f}"]
    for a, b, lab in zip(mine, m.groups(), ("per-galaxy", "mean", "err", "floor", "IMF", "radial", "z", "Salpeter", "fitted", "r<=40", "P2")):
        if a != b:
            mis.append(f"{f} {lab}: {a} vs committed {b}")
    for a, b, lab in zip((f"{v['base']['mean']:+.3f}", f"{v['tot']:.3f}", f"{v['z']:+.2f}", f"{10 ** v['base']['mean']:.2f}"), h.groups(), ("mean", "tot", "z", "factor")):
        if a != b:
            mis.append(f"{f} H1 {lab}: {a} vs committed {b}")
dj = 0.0
for f in FOOTS:
    v, j = RES32[f], js32[f]
    dj = max(dj, float(np.max(np.abs(np.asarray(v["base"]["per"]) - np.asarray(j["base"]["per"])))))
    for k in ("floor", "tot", "z", "imf_term", "radial_term"):
        dj = max(dj, abs(v[k] - j[k]))
    for k in ("base", "salp", "fit", "r40", "p2"):
        dj = max(dj, abs(v[k]["mean"] - j[k]["mean"]), abs(v[k]["err"] - j[k]["err"]))
BGEN = {f: score(lambda ups: b_boost, a0=A0B[f]) for f in FOOTS}
dg, dp = 0.0, 0.0
for f in FOOTS:
    v, w = RES32[f], BGEN[f]
    dg = max(dg, float(np.max(np.abs(w["base"]["per"] - np.asarray(v["base"]["per"])))))
    for k in ("floor", "tot", "z", "imf_term", "radial_term"):
        dg = max(dg, abs(w[k] - v[k]))
    for k in ("base", "salp", "r40"):
        dg = max(dg, abs(w[k]["mean"] - v[k]["mean"]), abs(w[k]["err"] - v[k]["err"]))
    for g in GAL:
        for u in ("uk", "us"):
            for a, b in zip(pts(g, b_boost, ups=u, a0=A0B[f]), points32(g, A0B[f], ups=u)):
                dp = max(dp, abs(a["ratio"] / b["ratio"] - 1.0), abs(a["obs"] / b["obs"] - 1.0), abs(a["y"] / b["y"] - 1.0))
check("C1 CONTROL: CFG32's committed B numbers reproduced through the exec of its pipeline -- (a) printed precision against its .out (per-galaxy offsets, mean, "
      "error, floor, IMF, radial, z, factor, Salpeter / fitted / r<=40 / P2 means), (b) 1e-9 against its JSON, (c) the generic estimator used for LCDM, run "
      "with B's law, to 1e-12; both footings",
      f"(a) mismatches: {'; '.join(mis) or 'none'}; (b) max |exec - JSON| {dj:.1e}; (c) max |generic - exec| {dg:.1e} (sample), {dp:.1e} (per point, relative); "
      + "; ".join(f"{f}: {RES32[f]['base']['mean']:+.3f} +- {RES32[f]['tot']:.3f} ({RES32[f]['z']:+.2f} sigma, B {status(RES32[f]['z'])})" for f in FOOTS),
      not mis and dj <= 1e-9 and dg <= 1e-12 and dp <= 1e-12)

# ================================================================================================ the LCDM engine
R.banner("THE LCDM ENGINE: the declared model and its variants through CFG32's pipeline" + ("  [MUTATE: every M_h x 100]" if MUTATE else ""))
LC = {name: score(lambda ups, v=v: lcdm_boost(v["cfn"], v["hmf"])) for name, v in CFGS.items()}
LAD = {m_: score(lambda ups, m_=m_: lcdm_boost(c_duffy_full, m_)) for m_ in LADDER}
for name, v in CFGS.items():
    s = LC[name]
    P(f"    {name:4s} {v['label']:46s}: {s['base']['mean']:+.3f} +- {s['tot']:.3f} (galaxy-to-galaxy {s['base']['err']:.3f}, IMF {s['imf_term']:.3f}, "
      f"radial {s['radial_term']:.3f}) -> {s['z']:+.2f} sigma; class {class_of(s['z'])}")
P(f"    ({time.time() - T0:.0f} s)")

# ================================================================================================ C3  the engine's limits
R.banner("C3  CONTROL: the zero-halo limit, the footing independence, mass only added")
zero = lcdm_boost(c_duffy_full, 1.0, mh_fixed=1e-30)
dz = 0.0
for g in GAL:
    for u in ("uk", "us"):
        for a, b in zip(pts(g, zero, ups=u), points32(g, A0B["canonical"], ups=u)):
            dz = max(dz, abs(a["ratio"] / b["obs"] - 1.0))
alt_base = score(lambda ups: lcdm_boost(c_duffy_full, HMUT), a0=A0B["alt"])
same_ft = bool(np.array_equal(alt_base["base"]["per"], LC["base"]["base"]["per"])) and alt_base["z"] == LC["base"]["z"] and alt_base["tot"] == LC["base"]["tot"]
minb = min(p["nu"] for v in list(CFGS.values()) for g in GAL for u in ("uk", "us", "uf") for p in pts(g, lcdm_boost(v["cfn"], v["hmf"]), ups=u))
minb = min(minb, min(p["nu"] for m_ in LADDER for g in GAL for p in pts(g, lcdm_boost(c_duffy_full, m_))))
check("C3 CONTROL: with M_h -> 0 the LCDM ratio is CFG32's g_obs/g_bar (1e-12); LCDM identical with the canonical and the alt a0; g_LCDM >= g_bar everywhere",
      f"max |zero-halo ratio / (g_obs/g_bar) - 1| {dz:.1e}; canonical == alt (bitwise): {same_ft}; minimum g_LCDM/g_bar over every model and point {minb:.4f}",
      dz <= 1e-12 and same_ft and minb >= 1.0)

# ================================================================================================ H1  the classification
R.banner("H1  THE CLASSIFICATION (base model; B's status from CFG32's own numbers)")
zl = LC["base"]["z"]; ml = LC["base"]["base"]["mean"]
bsign = {f: RES32[f]["base"]["mean"] > 0 for f in FOOTS}
sharedish = {f: abs(zl) > 2 and (zl > 0) == bsign[f] for f in FOOTS}
worseish = {f: abs(zl) > 2 and (zl > 0) != bsign[f] for f in FOOTS}
cls_scored = class_of(zl)
cls_decl, cls_x100, cls_x001 = class_of(LAD[1.0]["z"]), class_of(LAD[100.0]["z"]), class_of(LAD[0.01]["z"])
h1c = cls_x100 != cls_decl
m1 = cls_scored == cls_decl
final = cls_decl if h1c else f"NON-DISCRIMINATING (base class: {cls_decl})"
assert (not any(sharedish.values()) and not any(worseish.values())) == (abs(zl) <= 2)
tag = "  [MUTATE: scored on every M_h x 100]" if MUTATE else ""
dline = (f"LCDM {ml:+.3f} +- {LC['base']['tot']:.3f} dex -> {zl:+.2f} sigma (identical on both footings); B canonical {RES32['canonical']['base']['mean']:+.3f} "
         f"({ZB['canonical']:+.2f} sigma, {status(ZB['canonical'])}), alt {RES32['alt']['base']['mean']:+.3f} ({ZB['alt']:+.2f} sigma, {status(ZB['alt'])})")
check("H1a [HEADLINE] NOT SHARED: LCDM (base) is not off in B's direction at > 2 sigma" + tag, dline, not any(sharedish.values()))
check("H1b [HEADLINE] NOT LCDM-WORSE: LCDM (base) is not off in the opposite direction at > 2 sigma" + tag, dline, not any(worseish.values()))
check("H1c [HEADLINE; the NON-DISCRIMINATING test] THE GATE SEES THE HALO: LCDM's class with every declared M_h x 100 differs from its class with the declared M_h",
      f"declared (x1): {LAD[1.0]['base']['mean']:+.3f} +- {LAD[1.0]['tot']:.3f} ({LAD[1.0]['z']:+.2f} sigma) {cls_decl}; x100: {LAD[100.0]['base']['mean']:+.3f} +- "
      f"{LAD[100.0]['tot']:.3f} ({LAD[100.0]['z']:+.2f} sigma) {cls_x100}", h1c)
check("M1 [MUTATE detector] THE SCORED CLASS IS THE DECLARED CLASS: the class on the halos scored in H1a/H1b equals the class on the declared halos",
      f"scored (M_h x {HMUT:g}): {cls_scored}; declared (x1): {cls_decl}", m1)
check("H1 (reported) THE LABEL for the declared model (per footing and combined) and B minus LCDM",
      f"FINAL: {final}; per footing: " + ", ".join(f"{f} {classify(ZB[f], LAD[1.0]['z'])}" for f in FOOTS)
      + "; B - LCDM (declared): " + ", ".join(f"{f} {RES32[f]['base']['mean'] - LAD[1.0]['base']['mean']:+.3f} dex" for f in FOOTS)
      + (f"; scored in this MUTATE run: {cls_scored}" if MUTATE else ""), True, load_bearing=False)

# ================================================================================================ reported rows
R.banner("R1-R6  REPORTED (never enter a class)")
P(f"    {'galaxy':9s} {'B can':>7s} {'B alt':>7s} {'LCDM':>7s}   LCDM per radius (5, 10, 20, 40, 70 kpc) log10(g_obs/g_LCDM)" + tag)
per_rad = {}
bb = lcdm_boost(c_duffy_full, HMUT)
for i, g in enumerate(GAL):
    lr = [math.log10(p["ratio"]) for p in pts(g, bb)]; per_rad[g["name"]] = lr
    P(f"    {g['name']:9s} {RES32['canonical']['base']['per'][i]:+7.3f} {RES32['alt']['base']['per'][i]:+7.3f} {LC['base']['base']['per'][i]:+7.3f}   "
      + " ".join(f"{x:+.3f}" for x in lr))
check("R1 (reported) per-galaxy offsets: B (CFG32, both footings), LCDM (base); B minus LCDM on the sample means" + tag,
      "LCDM: " + ", ".join(f"{n} {o:+.2f}" for n, o in zip(NAMES, LC["base"]["base"]["per"]))
      + "; B - LCDM: " + ", ".join(f"{f} {RES32[f]['base']['mean'] - ml:+.3f}" for f in FOOTS)
      + f"; LCDM galaxies above / below zero: {int(np.sum(LC['base']['base']['per'] > 0))} / {int(np.sum(LC['base']['base']['per'] < 0))}", True, load_bearing=False)
r2 = []
for g in GAL:
    Mh = halo_of(g, 1.0); Mhs = halo_of(g, HMUT)
    dH = 3 * g["Mvir"] / (4 * math.pi * (g["Rvir"] / 1000.0) ** 3 * RHO_C)
    r2.append(dict(name=g["name"], logMstar=math.log10(mstar(g)), logMh=math.log10(Mh), c=float(c_duffy_full(Mh)), R200c=r200(Mh), logMh_scored=math.log10(Mhs),
                   logMvir_H=math.log10(g["Mvir"]), Rvir_H=g["Rvir"], c_H=g["c"], Delta_H=dH,
                   dark_to_stars_5=(1 - FB) * float(make_nfw(c_duffy_full)(Mhs, 5.0)) / M_hern(5.0, mstar(g), g["Re"]),
                   dark_to_stars_70=(1 - FB) * float(make_nfw(c_duffy_full)(Mhs, 70.0)) / M_hern(70.0, mstar(g), g["Re"])))
P(f"    {'galaxy':9s} {'logM*':>6s} {'logMh':>6s} {'c':>5s} {'R200c':>6s} | {'logMvir_H':>9s} {'Rvir_H':>6s} {'c_H':>5s} {'Delta_H':>7s} | LCDM dark/stars at 5, 70 kpc")
for d in r2:
    P(f"    {d['name']:9s} {d['logMstar']:6.2f} {d['logMh']:6.2f} {d['c']:5.2f} {d['R200c']:6.0f} | {d['logMvir_H']:9.2f} {d['Rvir_H']:6.0f} {d['c_H']:5.1f} {d['Delta_H']:7.0f} | "
      f"{d['dark_to_stars_5']:.2f}, {d['dark_to_stars_70']:.2f}")
check("R2 (reported) the LCDM halos (declared Moster M_200c, Duffy c, R200c [kpc]) beside Humphrey's fitted M_vir, R_vir, c and the overdensity they imply "
      "(this repo's rho_c; context only)" + tag,
      "; ".join(f"{d['name']} logMh {d['logMh']:.2f} (H {d['logMvir_H']:.2f}), c {d['c']:.1f} (H {d['c_H']:.1f})" for d in r2), True, load_bearing=False)
check("R3 (reported) the variants through the identical pipeline (each with its own recomputed floor): offset +- sigma (z) class" + tag,
      "; ".join(f"{n}: {LC[n]['base']['mean']:+.3f} +- {LC[n]['tot']:.3f} ({LC[n]['z']:+.2f}) {class_of(LC[n]['z'])}" for n in ("base", "V1", "V2", "V3", "V4")),
      True, load_bearing=False)
R4a = score(lambda ups: lcdm_boost(c_duffy_full, HMUT, halo_ups=ups))
R4b = {f: dict(tot=math.hypot(LC["base"]["base"]["err"], RES32[f]["floor"])) for f in FOOTS}
for f in FOOTS:
    R4b[f]["z"] = ml / R4b[f]["tot"]
fitL = samp(lcdm_boost(c_duffy_full, HMUT), ups="uf")
check("R4 (reported) the floor readings: (a) IMF term with M_h re-derived from the Salpeter M_*; (b) B's committed floor on LCDM's galaxy-to-galaxy error; "
      "(c) CFG32's R1 row for LCDM (Kroupa / Salpeter / fitted M/L, halo from the Kroupa M_* / r <= 40 kpc)" + tag,
      f"(a) Salpeter mean {R4a['salp']['mean']:+.3f}, IMF term {R4a['imf_term']:.3f}, floor {R4a['floor']:.3f} -> {R4a['z']:+.2f} sigma, {class_of(R4a['z'])}; (b) "
      + ", ".join(f"{f}: +- {R4b[f]['tot']:.3f} -> {R4b[f]['z']:+.2f} sigma, {classify(ZB[f], R4b[f]['z'])}" for f in FOOTS)
      + f"; (c) Kroupa {ml:+.3f}, Salpeter {LC['base']['salp']['mean']:+.3f}, fitted {fitL['mean']:+.3f}, r <= 40 {LC['base']['r40']['mean']:+.3f}",
      True, load_bearing=False)
slopes = []
for g in GAL:
    pp = pts(g, bb)
    slopes.append(float(np.polyfit(np.log10([p["gb"] for p in pp]), np.log10([p["ratio"] for p in pp]), 1)[0]))
check("R5 (reported) LCDM's residual shape: per-galaxy slope of log(g_obs/g_LCDM) against log g_bar (CFG32's H2 statistic; negative = the shortfall grows "
      "outward)" + tag,
      ", ".join(f"{n} {s:+.2f}" for n, s in zip(NAMES, slopes)) + f"; {sum(s < 0 for s in slopes)} of 7 negative (B, CFG32 H2: 7 of 7)", True, load_bearing=False)
check("R6 (reported) the halo ladder relative to the DECLARED halos (every run): offset +- sigma (z) class",
      "; ".join(f"x{m_:g}: {LAD[m_]['base']['mean']:+.3f} +- {LAD[m_]['tot']:.3f} ({LAD[m_]['z']:+.2f}) {class_of(LAD[m_]['z'])}" for m_ in LADDER),
      True, load_bearing=False)


# ---- R7: ADDED AFTER THE FIRST MAIN RUN (disclosed; reported only): the size of C4's failure
def halo_exact(Ms):
    return 10 ** brentq(lambda u: math.log10(float(moster_mstar(u))) - math.log10(Ms), float(LMH.min()), float(LMH.max()), xtol=1e-14)


def lcdm_boost_exact(cfn, hmf):
    prof = make_nfw(cfn); cache = {}

    def b(g, r, Mb, y):
        if g["name"] not in cache:
            cache[g["name"]] = halo_exact(mstar(g)) * hmf
        return 1.0 + (1 - FB) * float(prof(cache[g["name"]], r)) / Mb
    return b


EX = score(lambda ups: lcdm_boost_exact(c_duffy_full, HMUT))
dlogMh = max(abs(math.log10(halo_exact(mstar(g)) / float(halo_mass(mstar(g))))) for g in GAL)
check("R7 (reported; ADDED AFTER THE FIRST MAIN RUN, disclosed) the size of C4's failure: the base LCDM with M_h from an exact inversion of moster_mstar "
      "(brentq) in place of h48's interpolated halo_mass" + tag,
      f"max |d log M_h| {dlogMh:.1e} dex; offset {EX['base']['mean']:+.7f} vs {ml:+.7f} (|d| {abs(EX['base']['mean'] - ml):.1e} dex); z {EX['z']:+.5f} vs "
      f"{zl:+.5f}; class {class_of(EX['z'])} vs {cls_scored}", True, load_bearing=False)

# ================================================================================================ the table
R.banner("THE TABLE: offset [dex] (z); B canonical | alt; LCDM identical on both footings" + tag)
P(f"    {'model':50s} {'offset':>8s} {'sigma':>7s} {'z':>7s}  class")
for f in FOOTS:
    P(f"    {'B (CFG32, law nu_mono) ' + f:50s} {RES32[f]['base']['mean']:+8.3f} {RES32[f]['tot']:7.3f} {RES32[f]['z']:+7.2f}  B {status(RES32[f]['z'])}")
for n in ("base", "V1", "V2", "V3", "V4"):
    P(f"    {'LCDM ' + CFGS[n]['label']:50.50s} {LC[n]['base']['mean']:+8.3f} {LC[n]['tot']:7.3f} {LC[n]['z']:+7.2f}  {class_of(LC[n]['z'])}")
for m_ in LADDER:
    P(f"    {'LCDM declared halos x ' + format(m_, 'g'):50s} {LAD[m_]['base']['mean']:+8.3f} {LAD[m_]['tot']:7.3f} {LAD[m_]['z']:+7.2f}  {class_of(LAD[m_]['z'])}")
P(f"\n    FINAL LABEL (declared model): {final}")
P("    kappa = 1/2 and Omega_c h^2 stay fitted.  Nothing here says the data favour either model; nothing says the theory is closed.")


def jsc(s):
    return dict(s, base=dict(s["base"], per=s["base"]["per"].tolist()), salp=dict(s["salp"], per=s["salp"]["per"].tolist()),
                r40=dict(s["r40"], per=s["r40"]["per"].tolist()))


R.num("frozen_commit", FROZEN_COMMIT); R.num("HMUT", HMUT); R.num("FB", FB); R.num("names", NAMES)
R.num("B_CFG32", {f: dict(mean=RES32[f]["base"]["mean"], tot=RES32[f]["tot"], z=RES32[f]["z"], per=list(RES32[f]["base"]["per"]), status=status(RES32[f]["z"]),
                          floor=RES32[f]["floor"], imf_term=RES32[f]["imf_term"], radial_term=RES32[f]["radial_term"]) for f in FOOTS})
R.num("C1", dict(mismatches=mis, max_exec_vs_json=dj, max_generic_vs_exec=dg, max_generic_point=dp))
R.num("C2_C3_C4", dict(dev_R200=dev_n, dev_quad=dev_q, monotone=mono, zero_halo=dz, footing_identical=same_ft, min_boost=minb, grid_outside=outside, grid_roundtrip=rt))
R.num("LCDM", {n: jsc(LC[n]) | dict(cls=class_of(LC[n]["z"]), label=CFGS[n]["label"], hmf=CFGS[n]["hmf"]) for n in CFGS})
R.num("LADDER", {str(m_): jsc(LAD[m_]) | dict(cls=class_of(LAD[m_]["z"])) for m_ in LADDER})
R.num("H1", dict(z_lcdm=zl, mean_lcdm=ml, class_scored=cls_scored, class_declared=cls_decl, class_x100=cls_x100, class_x001=cls_x001, h1c_sees_halo=h1c,
                 m1=m1, final=final, B_minus_LCDM={f: RES32[f]["base"]["mean"] - LAD[1.0]["base"]["mean"] for f in FOOTS}))
R.num("R1_per_radius", per_rad); R.num("R2_halos", r2); R.num("R4a", jsc(R4a)); R.num("R4b", R4b); R.num("R4c_fitted", dict(fitL, per=fitL["per"].tolist()))
R.num("R5_slopes", slopes)
R.num("R7_exact_inversion_posthoc", dict(max_dlogMh=dlogMh, mean=EX["base"]["mean"], z=EX["z"], cls=class_of(EX["z"]), d_mean=EX["base"]["mean"] - ml))
nf = R.write()
sys.exit(1 if nf else 0)
