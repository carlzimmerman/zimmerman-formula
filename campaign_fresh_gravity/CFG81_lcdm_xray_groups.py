#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG81 -- A LCDM COMPARATOR FOR CFG34'S X-RAY GROUPS: is B's R2500 shortfall SPECIFIC-TO-B, SHARED, LCDM-WORSE or NON-DISCRIMINATING?

Criteria frozen and committed before this script: campaign_fresh_gravity/CFG81_FROZEN_CRITERIA.md (commit 27b4bf414).  CFG34 (and h7 through it) is exec'd
READ-ONLY with CFG69's exec_prefix pattern (its own MUTATE forced off, `open` replaced by CFG4's read-only _ro_open); FB, RHO_C and halo_mass come from CFG45's
prefix exactly as CFG69 obtains them; c_duffy_full, c_duffy_relaxed, c_dm and make_nfw are copied verbatim from CFG69.

CIRCULARITY (the design decision): CFG34's stars are h7's mstar500(M500) = 1.7e12 (M500/1e14)^0.6 evaluated at the HYDROSTATIC M500 (Kravtsov+2018: the group's
TOTAL stars, BCG + ICL + satellites; 0.65 of it inside R2500).  CFG69's base (M_h = Moster halo_mass(M_*)) would therefore return a function of M500_HSE --
circular -- and would feed a group total into a central-galaxy relation.  The lane's data permit NO non-circular LCDM mass at R500; they permit the SHAPE.
THE SHAPE DESIGN (declared once, no tuning): M_L(<r) = M_b(<r) + (1 - f_b) M_NFW(<r; M_h, c_duffy_full(M_h)), the lane's own baryons (identical to B's), M_h = M_200c
solved per group so that M_L(<R500) = M500_HSE at the measured R500; every overdensity in the data's own critical density rho_c,g = 3 M500 / (4 pi 500 R500^3);
the prediction M_L(<R2500) at the measured R2500.  Newtonian; no adiabatic contraction; no concentration scatter; c at z = 0.  LCDM has no a0: one number, both footings.
STATISTIC (CFG34's, same floor): median over the 20 groups of log10(M_HSE / M_L); err = std/sqrt(20); star = half the bracket spread (x/1.5, whole chain re-run);
HSE = log10 1.2; z = median / sqrt(err^2 + star^2 + HSE^2).  At R500 the comparator is normalised: NOT A TEST (offset 0 by construction).
PRE-DECLARED (from the frozen file)
  C1  CONTROL  CFG34's committed B numbers reproduced through the exec (RES to 1e-12; the four printed lines character for character; its checks fall as committed).
  C2  CONTROL  the NFW engine: M(<R_200c) = M_h to 1e-12; nfw_M = CFG69's verbatim make_nfw at RHO_C to 1e-12; the 200c -> 500c / 2500c conversion (fixed point)
               = a direct brentq root solve to 1e-9; M(<r) = the integral of the NFW density to 1e-7.
  C3  CONTROL  the data's rho_c from (M500, R500) and from (M2500, R2500) agree to 2% in every group.
  C4  CONTROL  every LCDM run is normalised: |M_L(<R500) / target - 1| < 1e-9 for all groups (base, bracket ends, variants, RM).
  C5  CONTROL  the base's c equals c_duffy_full at the solved M_h to 1e-12 (FAILS under the MUTATE by construction: the mutation detector).
  C6  CONTROL  (MUTATE run only) the MUTATE's base R2500 median and z equal the main run's RM row to 1e-9 (read from the main run's JSON).
  H1  [HEADLINE] LCDM reproduces the groups inside R2500: |z| < 2 (the MUTATE is expected, NOT guaranteed, to fail it).
  H2  (reported; NOT A TEST) LCDM at R500: |z| < 2 -- passes by construction.
  R0-R5, RM (reported): the circularity diagnostic; the class table; the variants V1 V2 V3 V4 V3u V4u V5 V6; B's shape-only offset; the MUTATE's model inside
  the main run; the per-group table; the concentration each group's own profile implies.
CLASSES (CFG69's, at R2500, per footing): |z_L| <= 2 SPECIFIC-TO-B; B's sign and |z_L| > 2 SHARED; opposite sign and |z_L| > 2 LCDM-WORSE; footings differ MIXED;
NON-DISCRIMINATING if the MUTATE (every concentration x 0.1) leaves LCDM's R2500 gate outcome unchanged.
MUTATE=1: every LCDM concentration x 0.1 -- C5 fails by construction (rc = 1); H1 is expected, not guaranteed, to fail.
ADDED AFTER THE FIRST MAIN AND MUTATE RUNS, BEFORE THE README (disclosed; NO check, threshold, model, variant or class rule changed; every check fell as in the
first runs: main 14/14, MUTATE 13/15 failing C5 and H1): R6 (reported only) -- the R2500 class with the 0.079-dex hydrostatic allowance removed from BOTH sides
(err and star only), because that allowance is almost all of LCDM's error and the frozen file itself calls it generous to LCDM in the shape design.
Run: python3 campaign_fresh_gravity/CFG81_lcdm_xray_groups.py   (MUTATE=1 for the control; ~10 s)
"""
import os, sys, io, math, json, contextlib, time
sys.dont_write_bytecode = True
import numpy as np
from scipy import integrate
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = HERE
sys.path.insert(0, HERE)
import CFG7_common as C
sys.path.insert(0, os.path.join(C.REPO, "hunt_2026"))
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG81_lcdm_xray_groups", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every LCDM concentration x 0.1 -- C5 must FAIL (exit 1); H1 is expected, not guaranteed, to fail ***")
CMUT = 0.1 if MUTATE else 1.0
FOOTS = ("canonical", "alt")
HH = 0.674
T0 = time.time()


# ================================================================================================ read-only exec of the lanes (CFG69's pattern; their own MUTATE forced off)
def exec_prefix(fname, marker, replace=None, capture=False):
    _e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    src = open(os.path.join(LANES, fname)).read()
    pre = src[:src.index(marker)]
    for a, b in (replace or []):
        assert pre.count(a) == 1
        pre = pre.replace(a, b)
    g = {"__file__": os.path.join(LANES, fname), "__name__": "lane_" + fname, "open": C.C4._ro_open}
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(pre, fname, "exec"), g)
    finally:
        os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
    return (g, buf.getvalue()) if capture else g


BAR = "# ================================================================================================ "
g45 = exec_prefix("CFG45_rule_readings.py", BAR + "P3 SPARC", [('READ = ("L", "S", "M", "E")', 'READ = ("L", "S")')])
FB, halo_mass, RHO_C = g45["FB"], g45["halo_mass"], g45["RHO_C"]
g34, OUT34 = exec_prefix("CFG34_groups_and_the_ladder_under_b.py", BAR + "H3", capture=True)
GR, mstar500, FIN, SBR = g34["GR"], g34["mstar500"], g34["FIN"], g34["SBR"]
RES34, run34, A0B, HSE_BIAS = g34["RES"], g34["run"], g34["A0B"], g34["HSE_BIAS"]
FIN_M = float(np.mean(FIN))
NG = len(GR)
P(f"\n  exec'd read-only: CFG45 prefix (FB = {FB:.5f}, RHO_C = {RHO_C:.4e} Msun/Mpc^3); CFG34 prefix up to its H3 banner ({NG} groups via h7); "
  f"stars inside R2500 = {FIN_M:.2f} M_*,500; bracket x/{SBR}; HSE allowance {HSE_BIAS:.4f} dex")

# ================================================================================================ C1
R.banner("C1  CONTROL: CFG34's committed B numbers reproduced through the read-only exec of its pipeline")
J34 = json.load(open(os.path.join(HERE, "CFG34_groups_and_the_ladder_under_b_results.json")))
KEYS = ("med", "err", "star", "tot", "z", "n_phantom_wins", "law_med", "fb_med")
d1 = max(abs(RES34[tuple(k.split("|"))][q] - v[q]) for k, v in J34["numbers"]["RES"].items() for q in KEYS)
nkeys = len(J34["numbers"]["RES"])
o34 = open(os.path.join(HERE, "CFG34_groups_and_the_ladder_under_b.out")).read().splitlines()
mine_lines = [l for l in OUT34.splitlines() if "median M_HSE/M_B =" in l]
com_lines = [l for l in o34 if "median M_HSE/M_B =" in l]
lines_ok = len(mine_lines) == 4 and mine_lines == com_lines
ck_mine = [(c["name"], c["ok"]) for c in g34["R"].checks]
ck_com = [(c["name"], c["ok"]) for c in J34["checks"][:len(ck_mine)]]
cks_ok = ck_mine == ck_com and [o for _, o in ck_mine] == [True, True, True, False]
for l in mine_lines:
    P(l)
check("C1 CONTROL: CFG34's committed B numbers reproduced through the read-only exec (RES to 1e-12; the four printed lines character for character; "
      "its C1/C2/H1 pass and H2 fails as committed)",
      f"RES: {nkeys} entries x {len(KEYS)} fields, max |d| = {d1:.1e}; printed lines identical: {lines_ok} ({len(mine_lines)} of {len(com_lines)}); "
      f"CFG34's own checks {[('PASS' if o else 'FAIL') for _, o in ck_mine]} vs committed {[('PASS' if o else 'FAIL') for _, o in ck_com]}",
      d1 <= 1e-12 and nkeys == 4 and lines_ok and cks_ok)


# ================================================================================================ the LCDM halo (CFG69's functions, copied verbatim)
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


# ------------------------------------------------------------------------------------------------ the lane's form: make_nfw's code with rho_c as an argument
def r200_kpc(Mh, rho_c):
    return (3 * Mh / (4 * math.pi * 200 * rho_c)) ** (1 / 3.) * 1000.0


def nfw_M(Mh, r_kpc, cfn, rho_c):
    Mh = np.asarray(Mh, float); r_kpc = np.asarray(r_kpc, float)
    c = cfn(Mh); R200 = (3 * Mh / (4 * math.pi * 200 * rho_c)) ** (1 / 3.) * 1000.0
    x = np.clip(r_kpc / R200, 1e-4, 5.0)
    return Mh * _m_nfw(c * x) / _m_nfw(c)


def so_fixed_point(Mh, c, rho_c, Delta):
    """R_Delta [kpc], M_Delta of an NFW with M_200c = Mh, c_200c = c, all overdensities in the same rho_c: x solves m(c x)/m(c) = (Delta/200) x^3."""
    x = 1.0
    for _ in range(20000):
        xn = ((200.0 / Delta) * _m_nfw(c * x) / _m_nfw(c)) ** (1 / 3.)
        if abs(xn - x) <= 4e-16 * x:
            x = xn
            break
        x = xn
    return x * r200_kpc(Mh, rho_c), Mh * _m_nfw(c * x) / _m_nfw(c)


def so_brentq(Mh, c, rho_c, Delta):
    """the same by a direct root solve of the mean enclosed density = Delta rho_c."""
    R200 = r200_kpc(Mh, rho_c)
    f = lambda r: Mh * _m_nfw(c * r / R200) / _m_nfw(c) / (4 / 3. * math.pi * (r / 1000.0) ** 3) - Delta * rho_c
    r = brentq(f, 1e-4 * R200, R200, xtol=1e-14 * R200, rtol=1e-15, maxiter=500)
    return r, Mh * _m_nfw(c * r / R200) / _m_nfw(c)


def nfw_integral(Mh, r_kpc, c, rho_c):
    R200 = r200_kpc(Mh, rho_c); rs = R200 / c
    rho_s = Mh / (4 * math.pi * rs ** 3 * _m_nfw(c))
    val, _ = integrate.quad(lambda r: 4 * math.pi * r ** 2 * rho_s / ((r / rs) * (1 + r / rs) ** 2), 0.0, r_kpc, epsabs=0.0, epsrel=1e-12, limit=400)
    return val


def mut(cfn, k):
    return lambda Mh: k * cfn(Mh)


# ================================================================================================ C2
R.banner("C2  CONTROL: the NFW engine (M(<R_200c) = M_h; nfw_M = CFG69's verbatim make_nfw; 200c -> 500c / 2500c vs a direct root solve; the density integral)")
CFNS = (("Duffy full", c_duffy_full), ("Duffy relaxed", c_duffy_relaxed), ("Dutton-Maccio", c_dm))
RHO_T = 1.36e11
d2a = 0.0
for _, cf in CFNS:
    for Mh in (1e12, 1e13, 1e14, 1e15):
        d2a = max(d2a, abs(float(nfw_M(Mh, r200_kpc(Mh, RHO_T), cf, RHO_T)) / Mh - 1), abs(float(make_nfw(cf)(Mh, r200_kpc(Mh, RHO_C))) / Mh - 1))
d2b = 0.0
rr = np.logspace(0.0, math.log10(3000.0), 30)
for _, cf in CFNS:
    for Mh in (1e12, 1e13, 1e14, 1e15):
        a_ = nfw_M(Mh, rr, cf, RHO_C); b_ = make_nfw(cf)(Mh, rr)
        d2b = max(d2b, float(np.max(np.abs(a_ / b_ - 1))))
d2c = 0.0; n2c = 0
for _, cf in CFNS:
    for k in (1.0, 0.1):
        for Mh in np.logspace(12, 15, 7):
            c = k * float(cf(Mh))
            for Dl in (500.0, 2500.0):
                rf, mf = so_fixed_point(Mh, c, RHO_T, Dl); rb, mb = so_brentq(Mh, c, RHO_T, Dl)
                d2c = max(d2c, abs(mf / mb - 1), abs(rf / rb - 1)); n2c += 1
d2d = 0.0
for Mh in (1e12, 1e13, 1e14):
    c = float(c_duffy_full(Mh)); R2 = r200_kpc(Mh, RHO_T)
    for fr in (0.01, 0.1, 0.3, 1.0, 3.0):
        d2d = max(d2d, abs(nfw_integral(Mh, fr * R2, c, RHO_T) / float(nfw_M(Mh, fr * R2, lambda M: c, RHO_T)) - 1))
check("C2 CONTROL: the NFW engine -- (i) M(<R_200c) = M_h; (ii) nfw_M = CFG69's verbatim make_nfw at RHO_C; (iii) the 200c -> 500c / 2500c fixed-point "
      "conversion = a direct brentq root solve; (iv) M(<r) = the integral of the NFW density",
      f"(i) max |d| {d2a:.1e} (tol 1e-12); (ii) {d2b:.1e} over 4 masses x 30 radii x 3 relations (tol 1e-12); (iii) {d2c:.1e} over {n2c} conversions "
      f"(7 masses x 3 relations x (1, 0.1) x Delta 500, 2500; tol 1e-9); (iv) {d2d:.1e} over 3 masses x 5 radii (tol 1e-7)",
      d2a <= 1e-12 and d2b <= 1e-12 and d2c <= 1e-9 and d2d <= 1e-7)

# ================================================================================================ C3
R.banner("C3  CONTROL: the data's own critical density (the convention in which R500 and R2500 are the 500c and 2500c radii)")


def rho_c_of(M, R_kpc, Delta):
    return 3 * M / (4 * math.pi * Delta * (R_kpc / 1000.0) ** 3)


RHOG = [rho_c_of(g["M500"], g["R500"], 500.0) for g in GR]
RHOG25 = [rho_c_of(g["M2500"], g["R2500"], 2500.0) for g in GR]
d3 = [b / a - 1 for a, b in zip(RHOG, RHOG25)]
check("C3 CONTROL: in every group the critical density implied by (M500, R500) and by (M2500, R2500) agree to 2%",
      f"max |d| {max(abs(x) for x in d3):.4f} over {NG} groups; rho_c,g / RHO_C (H0 = 67.4, z = 0) spans {min(RHOG) / RHO_C:.3f}-{max(RHOG) / RHO_C:.3f} "
      f"(median {np.median(RHOG) / RHO_C:.3f})", max(abs(x) for x in d3) <= 0.02)

# ================================================================================================ R0 the circularity diagnostic
R.banner("R0  THE CIRCULARITY DIAGNOSTIC (why CFG69's base cannot be used here)")
Ms_c = np.array([mstar500(g["M500"]) for g in GR])
r0a = float(np.max(np.abs(Ms_c / (1.7e12 * (np.array([g["M500"] for g in GR]) / 1e14) ** 0.6) - 1)))
Mh_mo = np.array([float(halo_mass(m)) for m in Ms_c])
n_clamp = int(np.sum(Mh_mo >= 10 ** 15.5 * (1 - 1e-9)))
check("R0 (reported) the lane's stars ARE the Kravtsov relation at the hydrostatic M500; CFG69's Moster halo_mass at those (group-total) stellar masses",
      f"max |M_* / 1.7e12 (M500_HSE/1e14)^0.6 - 1| = {r0a:.1e} over {NG} groups (M_* = {Ms_c.min():.2e}-{Ms_c.max():.2e} Msun); halo_mass(M_*) = "
      f"{Mh_mo.min():.2e}-{Mh_mo.max():.2e} Msun, {n_clamp} of {NG} clamped at the grid ceiling 10^15.5, for groups of M500 = "
      f"{min(g['M500'] for g in GR):.1e}-{max(g['M500'] for g in GR):.1e}: circular and a central/total mismatch (no ratio to the data is formed)",
      True, load_bearing=False)


# ================================================================================================ the LCDM engine (the shape design)
def lcdm_group(g, rho_c, cfn, sfac=1.0, nfac=1.0, m25=1.0, form="base", verbatim=False):
    """one group: M_h solved so that M_L(<R500) = nfac M500 at the measured R500; M_L(<R2500) predicted at the measured R2500."""
    Ms5 = mstar500(g["M500"]) * sfac
    Mb = {"R500": g["Mg500"] + Ms5, "R2500": g["Mg2500"] + Ms5 * FIN_M}
    rad = {"R500": g["R500"], "R2500": g["R2500"]}
    Mobs = {"R500": nfac * g["M500"], "R2500": m25 * g["M2500"]}
    nfw = (lambda Mh, r: float(make_nfw(cfn)(Mh, r))) if verbatim else (lambda Mh, r: float(nfw_M(Mh, r, cfn, rho_c)))
    if form == "base":
        ML = lambda Mh, tag: Mb[tag] + (1 - FB) * nfw(Mh, rad[tag])
    else:
        ML = lambda Mh, tag: nfw(Mh, rad[tag])
    f = lambda lm: ML(10 ** lm, "R500") / Mobs["R500"] - 1
    assert f(10.0) < 0 < f(18.0), g["name"]
    lm = brentq(f, 10.0, 18.0, xtol=1e-14, rtol=1e-15, maxiter=500)
    Mh = 10 ** lm
    out = dict(name=g["name"], Mh=Mh, c=float(cfn(Mh)), norm_dev=abs(ML(Mh, "R500") / Mobs["R500"] - 1))
    out["ML"] = {t: ML(Mh, t) for t in ("R500", "R2500")}
    out["lr"] = {t: math.log10(Mobs[t] / out["ML"][t]) for t in ("R500", "R2500")}
    return out


def lcdm_stats(v):
    rho = (lambda g, i: RHOG[i]) if v["rho"] == "data" else (lambda g, i: RHO_C)
    kw = dict(nfac=v["nfac"], m25=v["m25"], form=v["form"], verbatim=v["rho"] == "RHO_C")
    runs = {s: [lcdm_group(g, rho(g, i), v["cfn"], sfac=s, **kw) for i, g in enumerate(GR)] for s in (1.0, SBR, 1 / SBR)}
    base, lo, hi = runs[1.0], runs[SBR], runs[1 / SBR]
    out = dict(groups=base, norm_dev=max(d["norm_dev"] for s in runs.values() for d in s))
    for tag in ("R500", "R2500"):
        lr = np.array([d["lr"][tag] for d in base])
        med = float(np.median(lr)); err = float(np.std(lr, ddof=1) / math.sqrt(len(lr)))
        star = 0.5 * abs(float(np.median([d["lr"][tag] for d in lo])) - float(np.median([d["lr"][tag] for d in hi])))
        tot = math.sqrt(err ** 2 + star ** 2 + HSE_BIAS ** 2)
        out[tag] = dict(med=med, err=err, star=float(star), tot=tot, z=med / tot, n=len(lr))
    return out


VAR = {
    "base": dict(label="THE declared LCDM: Duffy full 200c, data rho_c,g, M_L(<R500) = M500", cfn=mut(c_duffy_full, CMUT), rho="data", nfac=1.0, m25=1.0, form="base"),
    "V1": dict(label="V1 Dutton-Maccio c", cfn=mut(c_dm, CMUT), rho="data", nfac=1.0, m25=1.0, form="base"),
    "V2": dict(label="V2 Duffy relaxed 200c", cfn=mut(c_duffy_relaxed, CMUT), rho="data", nfac=1.0, m25=1.0, form="base"),
    "V3": dict(label="V3 R500 normalisation x 1.2 (differential HSE bias)", cfn=mut(c_duffy_full, CMUT), rho="data", nfac=1.2, m25=1.0, form="base"),
    "V4": dict(label="V4 R500 normalisation x 0.8 (differential HSE bias)", cfn=mut(c_duffy_full, CMUT), rho="data", nfac=0.8, m25=1.0, form="base"),
    "V3u": dict(label="V3u M500 and M2500 x 1.2 (uniform HSE bias)", cfn=mut(c_duffy_full, CMUT), rho="data", nfac=1.2, m25=1.2, form="base"),
    "V4u": dict(label="V4u M500 and M2500 x 0.8 (uniform HSE bias)", cfn=mut(c_duffy_full, CMUT), rho="data", nfac=0.8, m25=0.8, form="base"),
    "V5": dict(label="V5 total mass as ONE NFW (no separate baryons)", cfn=mut(c_duffy_full, CMUT), rho="data", nfac=1.0, m25=1.0, form="total"),
    "V6": dict(label="V6 CFG45's RHO_C in CFG69's verbatim make_nfw", cfn=mut(c_duffy_full, CMUT), rho="RHO_C", nfac=1.0, m25=1.0, form="base"),
    "RM": dict(label="RM the MUTATE's model: base with every concentration x 0.1", cfn=mut(c_duffy_full, 0.1), rho="data", nfac=1.0, m25=1.0, form="base"),
}
L = {k: lcdm_stats(v) for k, v in VAR.items()}
LB = L["base"]

# ================================================================================================ C4 / C5
R.banner("C4 / C5  CONTROLS: the normalisation at R500 and the declared concentration")
nd4 = max(L[k]["norm_dev"] for k in L)
check("C4 CONTROL: every LCDM run is normalised at the measured R500 (|M_L(<R500)/target - 1| < 1e-9; base, bracket ends, every variant, RM)",
      f"max |d| {nd4:.1e} over {len(L)} runs x 3 stellar settings x {NG} groups; worst run {max(L, key=lambda k: L[k]['norm_dev'])}", nd4 < 1e-9)
d5 = max(abs(d["c"] / float(c_duffy_full(d["Mh"])) - 1) for d in LB["groups"])
check("C5 CONTROL: the base's concentration equals c_duffy_full at the solved M_h (the declared relation) in every group"
      + ("  [MUTATE: every c x 0.1 -- must FAIL]" if MUTATE else ""),
      f"max |c / c_duffy_full(M_h) - 1| = {d5:.1e} over {NG} groups; c = {min(d['c'] for d in LB['groups']):.2f}-{max(d['c'] for d in LB['groups']):.2f}", d5 <= 1e-12)

# ================================================================================================ H1 / H2
R.banner("H1 / H2  THE SHAPE DESIGN ON THE TWENTY X-RAY GROUPS (LCDM has no a0: one number for both footings)")
for tag in ("R2500", "R500"):
    v = LB[tag]
    P(f"    LCDM {tag:5s}: median M_HSE/M_L = {10 ** v['med']:.2f} ({v['med']:+.3f} dex) +- {v['tot']:.3f} (groups {v['err']:.3f}, stars {v['star']:.3f}, "
      f"HSE {HSE_BIAS:.3f}) -> {v['z']:+.2f} sigma" + ("   [normalised here: NOT A TEST]" if tag == "R500" else ""))
H1 = abs(LB["R2500"]["z"]) < 2
check("H1 [HEADLINE] LCDM (NFW + Duffy full c normalised at R500, the lane's baryons) REPRODUCES THE GROUPS INSIDE R2500: |z| < 2"
      + ("  [MUTATE: every c x 0.1]" if MUTATE else ""),
      f"median M_HSE/M_L = {10 ** LB['R2500']['med']:.2f} ({LB['R2500']['med']:+.3f} dex, {LB['R2500']['z']:+.2f} sigma); B (CFG34): canonical "
      f"{10 ** RES34[('canonical', 'R2500')]['med']:.2f} ({RES34[('canonical', 'R2500')]['z']:+.2f} sigma), alt {10 ** RES34[('alt', 'R2500')]['med']:.2f} "
      f"({RES34[('alt', 'R2500')]['z']:+.2f} sigma)", H1)
check("H2 (reported; NOT A TEST: passes by construction) LCDM at R500: |z| < 2",
      f"median {LB['R500']['med']:+.1e} dex ({LB['R500']['z']:+.2f} sigma) -- the comparator is normalised at R500; B (CFG34): canonical "
      f"{10 ** RES34[('canonical', 'R500')]['med']:.2f} ({RES34[('canonical', 'R500')]['z']:+.2f} sigma), alt {10 ** RES34[('alt', 'R500')]['med']:.2f} "
      f"({RES34[('alt', 'R500')]['z']:+.2f} sigma)", abs(LB["R500"]["z"]) < 2, load_bearing=False)


# ================================================================================================ R1 the class table
def b_status(z):
    return "FAIL" if abs(z) > 2 else ("MARGINAL" if abs(z) > 1 else "OK")


def classify(zB, zL):
    if b_status(zB) == "OK":
        return "B-ok"
    if abs(zL) <= 2:
        return "SPECIFIC-TO-B"
    return "SHARED" if np.sign(zL) == np.sign(zB) else "LCDM-WORSE"


def class_row(stats):
    per = {f: classify(RES34[(f, "R2500")]["z"], stats["R2500"]["z"]) for f in FOOTS}
    return per, (per["canonical"] if per["canonical"] == per["alt"] else "MIXED")


R.banner("R1  THE CLASS TABLE (B from CFG34, both footings; LCDM the shape design)")
per_cls, cls = class_row(LB)
gate_main, gate_mut = abs(LB["R2500"]["z"]) < 2, abs(L["RM"]["R2500"]["z"]) < 2
nondisc = gate_main == gate_mut
same_dir = (not gate_main) and (not gate_mut) and np.sign(L["RM"]["R2500"]["med"]) == np.sign(LB["R2500"]["med"]) and abs(L["RM"]["R2500"]["med"]) > abs(LB["R2500"]["med"])
headline_cls = ("NON-DISCRIMINATING (CFG69 class: " + cls + ")") if nondisc else cls
if MUTATE:
    headline_cls = f"MUTATE run -- the base IS the c x 0.1 halo (its CFG69 class {cls}); NON-DISCRIMINATING is decided in C6"
for tag in ("R2500", "R500"):
    for f in FOOTS:
        b, l_ = RES34[(f, tag)], LB[tag]
        P(f"    {tag:5s} {f:9s}: B {10 ** b['med']:.2f} ({b['med']:+.3f} dex, tot {b['tot']:.3f}, {b['z']:+.2f} sigma, {b_status(b['z'])}) | LCDM {10 ** l_['med']:.2f} "
          f"({l_['med']:+.3f} dex, tot {l_['tot']:.3f}, {l_['z']:+.2f} sigma) | B - LCDM {b['med'] - l_['med']:+.3f} dex | class "
          + (per_cls[f] if tag == "R2500" else "NOT TESTED (normalised at R500)"))
P(f"    R2500 combined class: {cls}; the MUTATE's model (RM, every c x 0.1): {L['RM']['R2500']['med']:+.3f} dex ({L['RM']['R2500']['z']:+.2f} sigma) -> gate "
  f"{'PASS' if gate_mut else 'FAIL'} vs the base's {'PASS' if gate_main else 'FAIL'}: NON-DISCRIMINATING = {nondisc}"
  + ("  (both FAIL with the mutated offset further out in the same direction: the gate responded; only its pass/fail did not change)" if nondisc and same_dir else ""))
P(f"    HEADLINE CLASS at R2500: {headline_cls}")
P("    R500: NOT TESTED -- the lane's data contain no non-circular LCDM prediction at R500 (the comparator is normalised there)")
check("R1 (reported) the class at R2500 (CFG69's rule per footing, NON-DISCRIMINATING from the MUTATE's model) and at R500",
      f"R2500: {headline_cls} (canonical {per_cls['canonical']}, alt {per_cls['alt']}); R500: NOT TESTED; B - LCDM at R2500 = "
      f"{RES34[('canonical', 'R2500')]['med'] - LB['R2500']['med']:+.3f} / {RES34[('alt', 'R2500')]['med'] - LB['R2500']['med']:+.3f} dex (canonical / alt)",
      True, load_bearing=False)

# ================================================================================================ R2 the variants
R.banner("R2  THE VARIANTS (reported only; never change H1 or the class)")
VCLS = {}
for k in ("V1", "V2", "V3", "V4", "V3u", "V4u", "V5", "V6"):
    s = L[k]; pc, cc = class_row(s); VCLS[k] = cc
    P(f"    {VAR[k]['label']:58s} R2500: {10 ** s['R2500']['med']:.2f} ({s['R2500']['med']:+.3f} dex) +- {s['R2500']['tot']:.3f} (groups {s['R2500']['err']:.3f}, "
      f"stars {s['R2500']['star']:.3f}) -> {s['R2500']['z']:+.2f} sigma; class {cc}; R500 offset {s['R500']['med']:+.3f} (by construction); "
      f"median c {np.median([d['c'] for d in s['groups']]):.2f}")
diff = [k for k, c_ in VCLS.items() if c_ != cls]
check("R2 (reported) the variants V1 V2 V3 V4 V3u V4u V5 V6 at R2500, each with its class",
      "; ".join(f"{k} {L[k]['R2500']['med']:+.3f} ({L[k]['R2500']['z']:+.2f}) {VCLS[k]}" for k in VCLS)
      + (f"  -- DIFFERENT class from the base: {', '.join(diff)}" if diff else "  -- every variant gives the base's class"), True, load_bearing=False)

# ================================================================================================ R3 B's shape-only offset
R.banner("R3  B's SHAPE-ONLY OFFSET: log(M_HSE/M_B) at R2500 minus at R500 (B normalised at R500 the way LCDM is), both footings")
R3 = {}
for f in FOOTS:
    rs = {s: run34(A0B[f], s) for s in (1.0, SBR, 1 / SBR)}
    dd = {s: np.log10([b["ratio"] for b in rs[s]["R2500"]]) - np.log10([a["ratio"] for a in rs[s]["R500"]]) for s in rs}
    med = float(np.median(dd[1.0])); err = float(np.std(dd[1.0], ddof=1) / math.sqrt(NG))
    star = 0.5 * abs(float(np.median(dd[SBR])) - float(np.median(dd[1 / SBR])))
    tot = math.sqrt(err ** 2 + star ** 2 + HSE_BIAS ** 2)
    R3[f] = dict(med=med, err=err, star=star, tot=tot, z=med / tot, per_group=dd[1.0].tolist())
    P(f"    {f:9s}: B's shape-only offset {med:+.3f} dex +- {tot:.3f} (groups {err:.3f}, stars {star:.3f}, HSE {HSE_BIAS:.3f}) -> {med / tot:+.2f} sigma   "
      f"| LCDM's (its R500 offset is 0): {LB['R2500']['med']:+.3f} dex ({LB['R2500']['z']:+.2f} sigma)")
check("R3 (reported) B's shape-only offset beside LCDM's R2500 offset (the like-for-like shape comparison)",
      "; ".join(f"{f}: B {R3[f]['med']:+.3f} ({R3[f]['z']:+.2f} sigma)" for f in FOOTS) + f"; LCDM {LB['R2500']['med']:+.3f} ({LB['R2500']['z']:+.2f} sigma)",
      True, load_bearing=False)

# ================================================================================================ RM
R.banner("RM  THE MUTATE's MODEL INSIDE THE MAIN RUN (every concentration x 0.1)")
check("RM (reported) the base with every concentration x 0.1: its R2500 gate",
      f"median {10 ** L['RM']['R2500']['med']:.2f} ({L['RM']['R2500']['med']:+.3f} dex) +- {L['RM']['R2500']['tot']:.3f} -> {L['RM']['R2500']['z']:+.2f} sigma: gate "
      f"{'PASS' if gate_mut else 'FAIL'} (the base: {'PASS' if gate_main else 'FAIL'}); shift {L['RM']['R2500']['med'] - LB['R2500']['med']:+.3f} dex; "
      f"median c {np.median([d['c'] for d in L['RM']['groups']]):.2f}", True, load_bearing=False)

# ================================================================================================ R4 the per-group table
R.banner("R4  PER GROUP (base; B from CFG34's own run)")
b_can, b_alt = run34(A0B["canonical"]), run34(A0B["alt"])
P(f"    {'group':18s} {'M500':>9s} {'R25/R5':>7s} {'rho_g/RHO_C':>11s} {'M_h':>9s} {'c':>5s} {'M_L(<R2500)':>11s} {'M2500':>9s} {'lg M/M_L':>9s} {'lg M/M_B can':>12s} {'alt':>7s}")
PG = []
for i, (g, d) in enumerate(zip(GR, LB["groups"])):
    bc, ba = math.log10(b_can["R2500"][i]["ratio"]), math.log10(b_alt["R2500"][i]["ratio"])
    PG.append(dict(name=g["name"], M500=g["M500"], r_ratio=g["R2500"] / g["R500"], rho_g=RHOG[i] / RHO_C, Mh=d["Mh"], c=d["c"], ML2500=d["ML"]["R2500"],
                   M2500=g["M2500"], lr_L=d["lr"]["R2500"], lr_B_can=bc, lr_B_alt=ba))
    P(f"    {g['name']:18s} {g['M500']:9.2e} {g['R2500'] / g['R500']:7.3f} {RHOG[i] / RHO_C:11.3f} {d['Mh']:9.2e} {d['c']:5.2f} {d['ML']['R2500']:11.2e} "
      f"{g['M2500']:9.2e} {d['lr']['R2500']:+9.3f} {bc:+12.3f} {ba:+7.3f}")
check("R4 (reported) the per-group table (above)", f"{NG} groups; LCDM log ratio at R2500 spans {min(p['lr_L'] for p in PG):+.3f} to {max(p['lr_L'] for p in PG):+.3f}; "
      f"B canonical {min(p['lr_B_can'] for p in PG):+.3f} to {max(p['lr_B_can'] for p in PG):+.3f}", True, load_bearing=False)

# ================================================================================================ R5 the concentration each group's profile implies
R.banner("R5  THE CONCENTRATION EACH GROUP's OWN PROFILE IMPLIES (a single total-mass NFW with M_500c = M500, rho_c,g)")


def implied_c(i, g):
    def ratio(c):
        cf = lambda M: c
        f = lambda lm: float(nfw_M(10 ** lm, g["R500"], cf, RHOG[i])) / g["M500"] - 1
        Mh = 10 ** brentq(f, 10.0, 18.0, xtol=1e-13)
        return float(nfw_M(Mh, g["R2500"], cf, RHOG[i])) / g["M500"], Mh
    tgt = g["M2500"] / g["M500"]
    lo_, hi_ = ratio(0.3)[0] - tgt, ratio(60.0)[0] - tgt
    if lo_ * hi_ > 0:
        return None
    cc = brentq(lambda c: ratio(c)[0] - tgt, 0.3, 60.0, xtol=1e-10)
    return cc, float(c_duffy_full(ratio(cc)[1]))


IC = [implied_c(i, g) for i, g in enumerate(GR)]
ok5 = [x for x in IC if x is not None]
for g, x in zip(GR, IC):
    P(f"    {g['name']:18s} M2500/M500 = {g['M2500'] / g['M500']:.3f}: " + (f"c_200c(data) = {x[0]:6.2f} vs Duffy full {x[1]:.2f}" if x else "no NFW solution in c = 0.3-60"))
check("R5 (reported) the concentration each group's own M2500/M500 implies (single total-mass NFW) vs Duffy full at the same M_200c",
      (f"{len(ok5)} of {NG} solved; median c(data) {np.median([x[0] for x in ok5]):.2f} (range {min(x[0] for x in ok5):.2f}-{max(x[0] for x in ok5):.2f}) vs Duffy "
       f"{np.median([x[1] for x in ok5]):.2f}; {sum(x[0] > x[1] for x in ok5)} of {len(ok5)} above Duffy; {NG - len(ok5)} without a solution") if ok5 else
      f"none of {NG} groups has an NFW solution in c = 0.3-60", True, load_bearing=False)

# ================================================================================================ R6 (ADDED AFTER THE FIRST RUNS; reported only)
R.banner("R6  (ADDED AFTER THE FIRST RUNS; reported only) THE R2500 CLASS WITHOUT THE 0.079-dex HYDROSTATIC ALLOWANCE (err and star only, both sides)")


def z_no_hse(s_):
    return s_["med"] / math.sqrt(s_["err"] ** 2 + s_["star"] ** 2)


zL6 = z_no_hse(LB["R2500"])
zB6 = {f: z_no_hse(RES34[(f, "R2500")]) for f in FOOTS}
per6 = {f: classify(zB6[f], zL6) for f in FOOTS}
cls6 = per6["canonical"] if per6["canonical"] == per6["alt"] else "MIXED"
check("R6 (reported; ADDED AFTER THE FIRST RUNS) the R2500 class with the hydrostatic allowance removed from both sides (err and star only)",
      f"LCDM {LB['R2500']['med']:+.3f} dex -> {zL6:+.2f} sigma; B canonical {zB6['canonical']:+.2f}, alt {zB6['alt']:+.2f} sigma; class {cls6} "
      f"(with the allowance: {cls})", True, load_bearing=False)

# ================================================================================================ C6 (MUTATE only)
MAINJ = os.path.join(HERE, "CFG81_lcdm_xray_groups_results.json")
c6 = None
if MUTATE:
    R.banner("C6  CONTROL (MUTATE run only): the MUTATE's base equals the main run's RM row; did the gate flip?")
    try:
        mj = json.load(open(MAINJ))["numbers"]
        rm = mj["LCDM"]["RM"]["R2500"]; h1m = mj["H1"]["pass"]
        dm, dz = abs(rm["med"] - LB["R2500"]["med"]), abs(rm["z"] - LB["R2500"]["z"])
        flip = bool(h1m) != bool(H1)
        c6 = dict(d_med=dm, d_z=dz, main_H1=h1m, mutate_H1=H1, flipped=flip)
        check("C6 CONTROL: the MUTATE's base R2500 median and z equal the main run's RM row to 1e-9 (main run's JSON)",
              f"|d med| {dm:.1e}, |d z| {dz:.1e}; the main run's H1 {'PASS' if h1m else 'FAIL'}, the MUTATE's H1 {'PASS' if H1 else 'FAIL'}: "
              + ("the gate FLIPPED -- the MUTATE is informative" if flip else "the gate did NOT flip -- NON-DISCRIMINATING confirmed"),
              dm <= 1e-9 and dz <= 1e-9)
    except (OSError, KeyError, ValueError) as e:
        check("C6 CONTROL: the MUTATE's base R2500 median and z equal the main run's RM row to 1e-9 (main run's JSON)",
              f"the main run's JSON could not be read ({type(e).__name__}); run the main run first", False)

# ================================================================================================ reading
if MUTATE:
    reading = f"MUTATE run (every c x 0.1): LCDM's R2500 gate {'PASS' if H1 else 'FAIL'}; C5 fails by construction"
elif H1:
    reading = ("SPECIFIC-TO-B: a standard NFW normalised at R500 reproduces the mass inside R2500 where B is 1.88x short; B's R2500 shortfall is B's own "
               "(a cosmic share tied to today's baryons)") + ("; NON-DISCRIMINATING: the c x 0.1 halo passes as well" if nondisc else "")
elif LB["R2500"]["med"] > 0:
    reading = ("SHARED: a standard LCDM halo is also short inside R2500 -- the groups' hydrostatic mass is more centrally concentrated than an NFW with Duffy's c "
               "plus the observed baryons; B's R2500 failure does not single out B") + (
        "; NON-DISCRIMINATING as the rule is written (the c x 0.1 halo also fails" + (", further out in the same direction: the gate responded, only its pass/fail "
                                                                                     "did not change)" if same_dir else ")") if nondisc else "")
else:
    reading = "LCDM-WORSE: LCDM over-predicts the mass inside R2500 where B under-predicts; the data lie between the two models" + (
        "; NON-DISCRIMINATING (the c x 0.1 halo gives the same gate outcome)" if nondisc else "")
if diff and not MUTATE:
    reading += f"; the class depends on the choice in {', '.join(diff)} (the declared class does not change)"
P(f"\n    READING (declared): {reading}")
P("    R500: NOT TESTED (no non-circular LCDM prediction at R500 in the lane's data).  kappa = 1/2 and Omega_c h^2 stay fitted.  Nothing here says the theory is closed.")

R.num("B_CFG34", {f"{f}|{t}": v for (f, t), v in RES34.items()})
R.num("LCDM", {k: {t: s[t] for t in ("R500", "R2500")} | dict(norm_dev=s["norm_dev"], median_c=float(np.median([d["c"] for d in s["groups"]])),
                                                                 label=VAR[k]["label"]) for k, s in L.items()})
R.num("H1", {"pass": bool(H1), "z": LB["R2500"]["z"], "med": LB["R2500"]["med"]})
R.num("class", dict(per_footing=per_cls, combined=cls, headline=headline_cls, non_discriminating=bool(nondisc), same_direction_fail=bool(same_dir),
                    R500="NOT TESTED", variants=VCLS, differ=diff))
R.num("C1", dict(max_dev=d1, lines_identical=lines_ok, checks=ck_mine))
R.num("C2", dict(i=d2a, ii=d2b, iii=d2c, iv=d2d)); R.num("C3", dict(dev=d3, rho_g_over_RHO_C=[x / RHO_C for x in RHOG]))
R.num("C5", d5); R.num("C6", c6); R.num("R0", dict(max_dev=r0a, Mh_moster=Mh_mo.tolist(), n_clamped=n_clamp))
R.num("R6", dict(z_L=zL6, z_B=zB6, per_footing=per6, combined=cls6)); R.num("R3", R3); R.num("R4", PG); R.num("R5", [None if x is None else dict(c_data=x[0], c_duffy=x[1]) for x in IC])
R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
