#!/usr/bin/env python3
"""CFG216 -- RC100 (Nestor Shachar+2023, 100 massive discs at z 0.61-2.52): a WITHIN-SAMPLE delta(z) test with velocities.
D = 1/(1 - f_DM(R_e)), g_obs = V_c^2 / R_e, g_bar = (1 - f_DM) g_obs from the table (no geometry assumption).  delta_L = log10(D_obs / nu(g_bar / a0_L)).
Frozen criteria: FROZEN_CRITERIA.md here (96d384dba), committed before any number.  kappa = 1/2 FITTED, NOT DERIVED.
Author decompositions, not a direct a0 measurement.  No sentence says the data favour the framework.
Run:  python3 campaign_fresh_gravity/CFG216_rc100_within_sample/cfg216_rc100.py        (MUTATE=1: D_obs x 10^(0.2 (z - z_med)))
"""
import os, sys, io, csv, math, json, contextlib
sys.dont_write_bytecode = True
import numpy as np
from scipy.special import i0e, i1e, k0e, k1e
from scipy.optimize import brentq

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, CFG)
_mut = os.environ.pop("MUTATE", None)
try:
    import CFG4_common as K
    import CFG7_common as C
finally:
    if _mut is not None:
        os.environ["MUTATE"] = _mut
MODE = (_mut or "").strip()
assert MODE in ("", "0", "1")
MUT = MODE == "1"
# INPUT-CORRECTION switch (2026-09-29, after the data chat's provenance check 03922e8c7): RC100_INPUT=corrected reads the corrected six-field copy instead of the
# repo CSV and writes cfg216_rc100_corrected* outputs; the default is unchanged and the original outputs are kept.
CORR = os.environ.get("RC100_INPUT", "").strip() == "corrected"
RC100_PATH = (os.path.join(REPO, "data_assembly", "rc100_provenance", "rc100_table3_six_fields_paper_values.csv") if CORR
              else os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3.csv"))
R = C.Report("cfg216_rc100" + ("_corrected" if CORR else ""), MUT)
P, check = R.P, R.check
P(__doc__.split("Run:")[0].strip())

G_KPC = 4.30091e-6
G2SI = 1e6 / 3.0856775814913673e19
XN = 1.678
OM = 0.315
A0F = {"canonical": K.A0["canonical"], "alt": K.A0["alt"]}
KER = {"nu_mono": K.nu_mono, "P2": K.nu_p2}
NBOOT, SEED = 10000, 216
LAWS = ("flat", "rival")


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + 1 - OM)


def nu1(nu, y):
    return float(nu(np.array([y]))[0])


def gbar_of_gobs(gobs_si, a0, nu):
    q = gobs_si / a0
    return a0 * 10 ** brentq(lambda ly: nu1(nu, 10 ** ly) * 10 ** ly - q, -80, 14, xtol=1e-14, rtol=1e-14)


def disc_v2(M, Re, Rr):
    Rd = Re / XN
    y = Rr / (2 * Rd)
    return 2 * G_KPC * M / Rd * y ** 2 * (i0e(y) * k0e(y) - i1e(y) * k1e(y))


def fnum(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else float("nan")
    except (TypeError, ValueError):
        return float("nan")


def verdict(lo, hi):
    return "CONSISTENT" if lo <= 0 <= hi else ("DISFAVOURED-over" if lo > 0 else "DISFAVOURED-under")


# ------------------------------------------------------------------------------------------------ data
raw = list(csv.DictReader(open(RC100_PATH, newline="")))
rows = []
excl = {"non-finite": 0, "fDM outside (0, 1)": 0}
for r in raw:
    z, Re, Vc, fd, lm = (fnum(r[k]) for k in ("z", "Re_kpc", "Vc_Re_kms", "fDM_within_Re", "logMbar_Msun"))
    if not all(math.isfinite(v) for v in (z, Re, Vc, fd)):
        excl["non-finite"] += 1; continue
    if not 0 < fd < 1:
        excl["fDM outside (0, 1)"] += 1; continue
    gobs = Vc ** 2 / Re * G2SI
    rows.append(dict(name=r["name"], z=z, Re=Re, Vc=Vc, fd=fd, lm=lm, gobs=gobs, D=1 / (1 - fd), gbar=(1 - fd) * gobs))
z = np.array([r["z"] for r in rows]); zmed = float(np.median(z))
P(f"  RC100: {len(raw)} rows; analysed {len(rows)}; excluded {excl}; z {z.min():.2f}-{z.max():.2f} (median {zmed:.2f})")
if MUT:
    for r in rows:
        r["D"] *= 10 ** (0.2 * (r["z"] - zmed))
    P("  MUTATE=1: D_obs x 10^(0.2 (z - z_med))")


def delta(rs, law, foot, nu, key="gbar"):
    out = []
    for r in rs:
        a0 = A0F[foot] * (E(r["z"]) if law == "rival" else 1.0)
        out.append(math.log10(r["D"] / nu1(nu, r[key] / a0)))
    return np.array(out)


def ts(x, y):
    i, j = np.triu_indices(len(x), 1)
    dx = x[j] - x[i]
    m = dx != 0
    return float(np.median((y[j] - y[i])[m] / dx[m]))


rng = np.random.default_rng(SEED)
IDX = {}


def boots(n):
    if n not in IDX:
        IDX[n] = rng.integers(0, n, size=(NBOOT, n))
    return IDX[n]


def ts_boot(x, y):
    n = len(x)
    i, j = np.triu_indices(n, 1)
    out = np.empty(NBOOT)
    B = boots(n)
    for k in range(NBOOT):
        xb, yb = x[B[k]], y[B[k]]
        dx = xb[j] - xb[i]
        m = dx != 0
        out[k] = np.median((yb[j] - yb[i])[m] / dx[m])
    return out


def slope_ci(x, y):
    bs = ts_boot(x, y)
    return ts(x, y), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)), float(np.std(bs))


def med_ci(d):
    B = boots(len(d))
    bs = np.median(d[B], axis=1)
    return float(np.median(d)), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


# ------------------------------------------------------------------------------------------------ controls C1, C3
R.banner("CONTROLS")
c1 = max(abs(math.log10(nu1(nu, 3.0 * A0F[f] / (A0F[f] * fac)) / nu1(nu, 3.0 * A0F[f] / (A0F[f] * fac)))) for nu in KER.values() for f in A0F
         for fac in (1.0, E(1.5), E(2.5)))
check("C1 a synthetic galaxy placed exactly on each law returns delta = 0", f"max {c1:.1e}", c1 < 1e-12)
d0 = delta(rows, "flat", "canonical", K.nu_mono)
sh = ts(z, d0 + 0.2 * (z - zmed)) - ts(z, d0)
check("C3 an injected slope 0.2 (z - z_med) shifts the Theil-Sen slope by 0.2 to 1e-9", f"shift {sh:.12f}", abs(sh - 0.2) < 1e-9)

# C2: RC41 galaxies by name -> CFG215's geometry-based delta_flat
src215 = open(os.path.join(CFG, "CFG215_decomposition_timeline", "cfg215_timeline.py")).read()
ns = {"__file__": os.path.join(CFG, "CFG215_decomposition_timeline", "cfg215_timeline.py"), "__name__": "cfg215"}
_e = os.environ.pop("MUTATE", None)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src215[:src215.index("# ------------------------------------------------------------------------------------------------ the two series")], "cfg215", "exec"), ns)
if _e is not None:
    os.environ["MUTATE"] = _e
rc41 = {r["id"].replace("_", " "): r for r in ns["rc41"]}
sub = [r for r in rows if r["name"] in rc41]
dd = []
for r in sub:
    q = rc41[r["name"]]
    d100 = math.log10(1 / (1 - r["fd"]) / nu1(K.nu_mono, r["gbar"] / A0F["canonical"]))         # unmutated D for the cross-check
    d215 = math.log10((1 / (1 - q["fd"])) / nu1(K.nu_mono, q["gbar"] / A0F["canonical"]))
    dd.append(d100 - d215)
med_shift = float(np.median(dd)) if dd else float("nan")
check("C2 CFG215's RC41 geometry cross-check: for the RC41 galaxies found in RC100 by name, median [delta_flat(RC100 V_c, f_DM) - delta_flat(CFG215 geometry)] within 0.05 dex",
      f"{len(sub)} galaxies matched; median {med_shift:+.3f} dex, range [{min(dd):+.3f}, {max(dd):+.3f}]" if dd else "no match", bool(dd) and abs(med_shift) < 0.05,
      load_bearing=False)
R.num("C2", dict(n=len(sub), median=med_shift, values=dd))

# ------------------------------------------------------------------------------------------------ primary: slopes
R.banner("PRIMARY: within-sample slope of delta on z (Theil-Sen, 95% bootstrap CI)")
RES = {}
for kname, nu in KER.items():
    for foot in A0F:
        for law in LAWS:
            d = delta(rows, law, foot, nu)
            s, lo, hi, sd = slope_ci(z, d)
            m, mlo, mhi = med_ci(d)
            RES[(kname, foot, law)] = dict(slope=s, lo=lo, hi=hi, sd=sd, med=m, mlo=mlo, mhi=mhi, v=verdict(mlo, mhi))
            if (kname, foot) == ("nu_mono", "canonical"):
                P(f"  {law:5s} (nu_mono, canonical): median delta {m:+.3f} [{mlo:+.3f}, {mhi:+.3f}] {verdict(mlo, mhi)}; slope {s:+.3f} [{lo:+.3f}, {hi:+.3f}] per unit z (sigma {sd:.3f})")
for kname in KER:
    for foot in A0F:
        if (kname, foot) == ("nu_mono", "canonical"):
            continue
        P(f"  ({kname}, {foot}): flat slope {RES[(kname, foot, 'flat')]['slope']:+.3f} [{RES[(kname, foot, 'flat')]['lo']:+.3f}, {RES[(kname, foot, 'flat')]['hi']:+.3f}]; "
          f"rival slope {RES[(kname, foot, 'rival')]['slope']:+.3f} [{RES[(kname, foot, 'rival')]['lo']:+.3f}, {RES[(kname, foot, 'rival')]['hi']:+.3f}]")


def outcome(sf, sr):
    fz = sf["lo"] <= 0 <= sf["hi"]; rz = sr["lo"] <= 0 <= sr["hi"]
    if fz and sr["hi"] < 0:
        return "W-flat (delta_flat flat in z; the rival's negative drift is in the data)"
    if sf["lo"] > 0 and rz:
        return "W-rival (delta_flat drifts up in z; delta_rival flat)"
    if fz and rz:
        return "W-none (no z-dependence detectable)"
    return "W-mixed"


P("\n  outcome per cell: " + "; ".join(f"{k}/{f}: {outcome(RES[(k, f, 'flat')], RES[(k, f, 'rival')]).split(' ')[0]}" for k in KER for f in A0F))
primary_outcome = outcome(RES[("nu_mono", "canonical", "flat")], RES[("nu_mono", "canonical", "rival")])
P(f"  -> PRIMARY (nu_mono, canonical): {primary_outcome}")
R.num("outcome_primary", primary_outcome)

# expected slopes if each hypothesis were exactly true
R.banner("EXPECTED SLOPES if each hypothesis were exactly true (g_obs and z held at the sample's own values; baryons from that law's inversion)")
EXP = {}
for truth in LAWS:
    dfl, dri = [], []
    for r in rows:
        a0t = A0F["canonical"] * (E(r["z"]) if truth == "rival" else 1.0)
        gt = gbar_of_gobs(r["gobs"], a0t, K.nu_mono)
        Dt = r["gobs"] / gt
        dfl.append(math.log10(Dt / nu1(K.nu_mono, gt / A0F["canonical"])))
        dri.append(math.log10(Dt / nu1(K.nu_mono, gt / (A0F["canonical"] * E(r["z"])))))
    EXP[truth] = dict(flat=ts(z, np.array(dfl)), rival=ts(z, np.array(dri)))
    P(f"  if {truth} were exactly true: slope of delta_flat {EXP[truth]['flat']:+.3f}, slope of delta_rival {EXP[truth]['rival']:+.3f}")
for law in LAWS:
    r_ = RES[("nu_mono", "canonical", law)]
    zs = {t: (r_["slope"] - EXP[t][law]) / r_["sd"] for t in LAWS}
    P(f"  observed slope of delta_{law} {r_['slope']:+.3f}: z-score vs 'flat true' {zs['flat']:+.2f}, vs 'rival true' {zs['rival']:+.2f} (bootstrap sigma {r_['sd']:.3f})")
R.num("expected", EXP)

# level in z-halves
R.banner("LEVEL in the two z-halves (nu_mono, canonical)")
lo_half = [r for r in rows if r["z"] <= zmed]; hi_half = [r for r in rows if r["z"] > zmed]
for nm, half in (("z <= median", lo_half), ("z > median", hi_half)):
    for law in LAWS:
        d = delta(half, law, "canonical", K.nu_mono)
        m, l_, h_ = med_ci(d)
        P(f"  {nm:12s} n = {len(half):3d} median z {np.median([r['z'] for r in half]):.2f}  {law:5s}: {m:+.3f} [{l_:+.3f}, {h_:+.3f}] {verdict(l_, h_)}")

# sensitivities
R.banner("SENSITIVITIES (reported beside the primary)")
SENS = {}
names41 = set(rc41)
sets = {"(a) the RC41 subset": [r for r in rows if r["name"] in names41], "(b) the other galaxies": [r for r in rows if r["name"] not in names41],
        "(c) g_bar < 3 a0": [r for r in rows if r["gbar"] / A0F["canonical"] < 3.0]}
for lab, rs in sets.items():
    if len(rs) < 6:
        P(f"  {lab}: n = {len(rs)} (too few)"); continue
    zz = np.array([r["z"] for r in rs])
    line = f"  {lab} (n = {len(rs)}): "
    parts = []
    for law in LAWS:
        d = delta(rs, law, "canonical", K.nu_mono)
        s, lo, hi, sd = slope_ci(zz, d)
        m, mlo, mhi = med_ci(d)
        SENS[(lab, law)] = dict(slope=s, lo=lo, hi=hi, med=m, mlo=mlo, mhi=mhi)
        parts.append(f"{law}: median {m:+.3f} [{mlo:+.3f}, {mhi:+.3f}], slope {s:+.3f} [{lo:+.3f}, {hi:+.3f}]")
    P(line + "; ".join(parts))
geo = []
for r in rows:
    if math.isfinite(r["lm"]):
        gg = 10 ** r["lm"] * disc_v2(1.0, r["Re"], r["Re"]) / r["Re"] * G2SI
        geo.append(dict(r, gbar_geo=gg, D=r["gobs"] / gg))
zg = np.array([r["z"] for r in geo])
parts = []
for law in LAWS:
    d = delta(geo, law, "canonical", K.nu_mono, key="gbar_geo")
    s, lo, hi, sd = slope_ci(zg, d)
    m, mlo, mhi = med_ci(d)
    SENS[("(d) table M_bar geometry", law)] = dict(slope=s, lo=lo, hi=hi, med=m, mlo=mlo, mhi=mhi)
    parts.append(f"{law}: median {m:+.3f} [{mlo:+.3f}, {mhi:+.3f}], slope {s:+.3f} [{lo:+.3f}, {hi:+.3f}]")
P(f"  (d) g_bar from the table's M_bar and R_e (thin exponential disc), D_ind = g_obs/g_bar,geom (n = {len(geo)}): " + "; ".join(parts))
sign_flip = any(np.sign(SENS[(l_, "flat")]["slope"]) != np.sign(RES[("nu_mono", "canonical", "flat")]["slope"]) for l_ in ("(d) table M_bar geometry",))
P(f"\n  route- or selection-dependent label for the primary slope of delta_flat (variant (d) or a half disagreeing in sign): "
  f"{'YES' if sign_flip else 'no (variant (d) has the same sign)'}")
R.num("results", {"|".join(k): v for k, v in RES.items()})
R.num("sens", {"|".join(k): v for k, v in SENS.items()})
if MUT:
    R.banner("MUTATE RESPONSE")
    d_un = np.array([math.log10((1 / (1 - r["fd"])) / nu1(K.nu_mono, r["gbar"] / A0F["canonical"])) for r in rows])
    d_mu = delta(rows, "flat", "canonical", K.nu_mono)
    shift = ts(z, d_mu) - ts(z, d_un)
    check("MUTATE: the injected 0.2 (z - z_med) slope moves delta_flat's Theil-Sen slope by exactly +0.2 (>= +0.19 required)", f"shift {shift:+.6f}", shift >= 0.19)
R.write(here=LANE)
