#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L315 -- THE PHANTOM LAW (L311/L312) CONFRONTED WITH SPARC: does the rotation data carry the active phantom mass?

THE LAW UNDER TEST (real_research/clock_2026/L311_phantom_law.py, L312_law_implications.py, committed 09-20):
    g_obs^2 = a0 g_N,tot,   g_N,tot = g_N,b + G M_act(<r)/r^2,   M_act(<r) = 1.05 M_b sqrt(r / 30 kpc),
    a0 = c H_Lambda / Z (kappa = 1/2, "not a fit"), "zero parameters inside the halo".
  L312 I3 states it as a universal residual: y^2 - 1 = 1.05 sqrt(r/30 kpc) at every galaxy, "SPARC-testable".
  Neither lane confronted it with rotation curves (their checks on it are literal True).  This lane does.

THREE READINGS, so the kill (or the survival) is not a reading artefact:
  literal      M_act = 1.05 M_b,tot sqrt(r/30 kpc)            (L311/L312 as written)
  selfsimilar  M_act = 1.05 M_b,tot sqrt(r/(30 kpc r_M/r_M,MW)) (the 30-kpc anchor rescaled by each galaxy's MOND radius)
  enclosed     M_act = 1.05 M_b(<r) sqrt(r/30 kpc)            (the active mass tied to the ENCLOSED baryons: the gentlest)
  literal_deep the literal M_act in L311's literal deep form g_obs = sqrt(a0 g_tot) (no interior kernel boost)
  literal_deep IS the law as written (L311: g_obs^2 = a0 g_N,tot in the domain g_N,b <= a0).  The other three
  embed the active mass in the framework's kernel g_model = nu_RAR(g_tot/a0) g_tot -- which turns out HARSHER on
  the law (the interior boost is then added on top), so literal_deep at the law's own a0 is its best case and
  is reported first in the verdict.  The amplitude A multiplies M_act (the law: A = 1).

DATA: SPARC (Lelli+2016), Q <= 2, i >= 30 deg; the law's domain g_N,b <= a0 (x <= 1, selected at Upsilon_d = 0.5).
  M_b,tot = Upsilon_d L[3.6] + 1.33 M_HI.  Point errors 2 eV/V/ln10 in quadrature with 0.05 dex intrinsic;
  every uncertainty from a GALAXY bootstrap (points inside a galaxy are correlated: the V01 lesson).

TESTS
  T1 WITHIN-GALAXY RADIAL SHAPE (Upsilon-robust: a per-galaxy offset is removed by demeaning): the slope of
     the residual vs log r inside galaxies, data vs each reading's prediction.
  T2 THE AMPLITUDE A: global fit with (i) a0 fixed canonical, (ii) a0 free jointly, (iii) a0 free AND
     Upsilon_d profiled per galaxy on a grid -- the law needs A = 1.
  T3 L312 I3's own mass correlation: at fixed x in [0.05, 0.3] the galaxy-mean residual vs log M_b, data vs law.
  V  INJECTION-RECOVERY: law-true mocks must return A ~ 1 and null mocks A ~ 0 through the same pipeline.
  MUTATE=1 replaces the data by a law-true mock: the finding "the data exclude A = 1" must then FAIL (rc = 1).

Run from the repository root:  python3 real_research/cq_gravity_2026/L315_phantom_law_vs_sparc.py
"""
import os, sys, json, glob, math
import numpy as np
from scipy.optimize import minimize, minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L315_phantom_law_vs_sparc"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L315", "mutate": MUTATE, "checks": {}, "numbers": {}}
NBOOT = 200


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 104); P(t); P("=" * 104)


P(__doc__)
KPC, G, MSUN = 3.0856775814913673e19, 6.6743e-11, 1.98892e30
CONV = 1e6 / KPC                                   # (km/s)^2/kpc -> m/s^2
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
a0c = A0["canonical"]
UPS_GRID = np.round(np.arange(0.25, 0.951, 0.05), 3)
READINGS = ("literal", "selfsimilar", "enclosed", "literal_deep")
MW_rM = math.sqrt(G * 6e10 * MSUN / a0c) / KPC     # the L311 anchor galaxy's MOND radius


def nu(x):
    return 1.0 / (1.0 - np.exp(-np.sqrt(np.clip(x, 1e-12, None))))


# ------------------------------------------------------------------------------------------------ data
tab = {}
for ln in open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    tk = ln.split()
    if len(tk) < 18:
        continue
    try:
        tab[tk[0]] = dict(T=int(tk[1]), D=float(tk[2]), Inc=float(tk[5]), L=float(tk[7]), MHI=float(tk[13]),
                          Q=int(tk[17]))
    except ValueError:
        continue
gals = []
for f in sorted(glob.glob(os.path.join(REPO, "real_research", "data", "sparc_data", "*_rotmod.dat"))):
    nm = os.path.basename(f).replace("_rotmod.dat", "")
    t = tab.get(nm)
    if t is None or t["Q"] > 2 or t["Inc"] < 30:
        continue
    d = np.genfromtxt(f, comments="#")
    R, V, eV, Vg, Vd, Vb = (d[:, i] for i in range(6))
    vb2_05 = np.sign(Vg) * Vg**2 + 0.5 * Vd**2 + 0.7 * Vb**2
    sel = (R > 0) & (V > 0) & (eV > 0) & (vb2_05 > 0) & (vb2_05 / R * CONV / a0c <= 1.0)
    if sel.sum() < 1:
        continue
    gals.append(dict(nm=nm, R=R[sel], V=V[sel], eV=eV[sel], Vg=Vg[sel], Vd=Vd[sel], Vb=Vb[sel], **t))
NG = len(gals)
P(f"  SPARC: {len(tab)} in the table; {NG} galaxies with Q<=2, i>=30 and >=1 point in the law's domain "
  f"(x<=1); {sum(len(g['R']) for g in gals)} points")


def arrays(g, Ud, A, reading, a0=a0c):
    """model log10 g for one galaxy at disk M/L Ud, active amplitude A."""
    R = g["R"]; Rm = R * KPC
    vb2 = np.sign(g["Vg"]) * g["Vg"]**2 + Ud * g["Vd"]**2 + 1.4 * Ud * g["Vb"]**2
    gb = np.clip(vb2, 1e-6, None) / R * CONV
    Mb = (Ud * g["L"] + 1.33 * g["MHI"]) * 1e9 * MSUN
    if reading in ("literal", "literal_deep"):
        M = 1.05 * Mb * np.sqrt(R / 30.0)
    elif reading == "selfsimilar":
        rM = math.sqrt(G * Mb / a0c) / KPC
        M = 1.05 * Mb * np.sqrt(R / (30.0 * rM / MW_rM))
    else:
        Menc = np.clip(vb2, 1e-6, None) * 1e6 * Rm / G
        M = 1.05 * Menc * np.sqrt(R / 30.0)
    gt = gb + A * G * M / Rm**2
    gt = np.clip(gt, 1e-18, None)
    if reading == "literal_deep":
        return np.log10(np.sqrt(a0 * gt)), gb, Mb
    return np.log10(nu(gt / a0) * gt), gb, Mb


def obs(g):
    lg = np.log10(g["V"]**2 / g["R"] * CONV)
    s = 2 * g["eV"] / g["V"] / np.log(10)
    return lg, 1.0 / (s**2 + 0.05**2)


LOBS = [obs(g) for g in gals]


def make_mock(truth_A, reading="literal", seed=11):
    rng = np.random.default_rng(seed)
    out = []
    for g, (lg, w) in zip(gals, LOBS):
        lm, _, _ = arrays(g, 0.5, truth_A, reading)
        off = rng.normal(0, 0.05)                        # galaxy-level systematic (distance/inclination/M-L)
        out.append((lm + off + rng.normal(0, 1) * np.sqrt(1 / w), w))
    return out


if MUTATE:
    LOBS = make_mock(1.0, "literal", seed=99)
    P("  MUTATE: the data are REPLACED by a law-true (A = 1, literal) mock")


# ------------------------------------------------------------------------------------------------ chi tables
def chi_table(reading, lobs, Agrid, a0grid, Ugrid):
    """chi[g, iU, iA, ia0] for every galaxy."""
    T = np.zeros((NG, len(Ugrid), len(Agrid), len(a0grid)))
    for i, g in enumerate(gals):
        lg, w = lobs[i]
        for iu, U in enumerate(Ugrid):
            for ia, A in enumerate(Agrid):
                for ib, a0 in enumerate(a0grid):
                    lm, _, _ = arrays(g, U, A, reading, a0)
                    T[i, iu, ia, ib] = np.sum(w * (lg - lm)**2)
    return T


AGRID = np.round(np.arange(-0.2, 1.501, 0.02), 3)
A0GRID = np.geomspace(7.5e-11, 1.6e-10, 15)
iU05 = int(np.argmin(np.abs(UPS_GRID - 0.5)))
ia0c = int(np.argmin(np.abs(A0GRID - a0c)))


def best_A(T, idx, mode):
    """mode: 'fixed' (U=0.5, a0 canonical), 'free' (U=0.5, a0 profiled), 'prof' (U per galaxy + a0 profiled)."""
    if mode == "fixed":
        s = T[idx, iU05, :, :][:, :, ia0c].sum(axis=0)
        return AGRID[int(np.argmin(s))]
    if mode == "profU":
        s = T[idx][:, :, :, ia0c].min(axis=1).sum(axis=0)   # per-galaxy min over U at a0 canonical -> (A,)
        return AGRID[int(np.argmin(s))]
    if mode == "free":
        s = T[idx, iU05, :, :].sum(axis=0)             # (A, a0)
        return AGRID[np.unravel_index(int(np.argmin(s)), s.shape)[0]]
    s = T[idx].min(axis=1).sum(axis=0)                  # per-galaxy min over U -> (A, a0)
    return AGRID[np.unravel_index(int(np.argmin(s)), s.shape)[0]]


def a_with_boot(T, mode, seed=5):
    rng = np.random.default_rng(seed)
    full = np.arange(NG)
    ah = best_A(T, full, mode)
    bs = [best_A(T, rng.integers(0, NG, NG), mode) for _ in range(NBOOT)]
    return float(ah), float(np.std(bs))


# ================================================================================================ V
banner("V  INJECTION-RECOVERY -- the pipeline must see the law when it is there, and not when it is not")
rec = {}
for truth in (1.0, 0.0):
    mock = make_mock(truth, "literal", seed=21 + int(truth))
    Tm = chi_table("literal", mock, AGRID, A0GRID, UPS_GRID)
    rec[truth] = a_with_boot(Tm, "prof")
    P(f"    literal, truth A = {truth}: recovered A = {rec[truth][0]:.3f} +/- {rec[truth][1]:.3f} (U and a0 profiled)")
OUT["numbers"]["injection"] = {str(k): v for k, v in rec.items()}
okV = abs(rec[1.0][0] - 1) < max(3 * rec[1.0][1], 0.1) and abs(rec[0.0][0]) < max(3 * rec[0.0][1], 0.1)
check("V1 injection-recovery through the full pipeline (Upsilon per galaxy + a0 profiled): law-true -> A ~ 1, "
      "null -> A ~ 0", f"A(1) = {rec[1.0][0]:.3f}+/-{rec[1.0][1]:.3f}; A(0) = {rec[0.0][0]:.3f}+/-{rec[0.0][1]:.3f}",
      okV, "the amplitude is identifiable with a0 AND the M/L free -- so a null on the data is a real null")

# ================================================================================================ T2
banner("T2  THE ACTIVE-MASS AMPLITUDE ON THE DATA (the law: A = 1)")
res, TABLES = {}, {}
for rd in READINGS:
    T = chi_table(rd, LOBS, AGRID, A0GRID, UPS_GRID)
    TABLES[rd] = T
    row = {}
    for mode in ("fixed", "profU", "free", "prof"):
        a, s = a_with_boot(T, mode)
        s_eff = max(s, 0.02)                             # never quote an error below the 0.02 grid step
        row[mode] = dict(A=a, sig=s, z_law=(1 - a) / s_eff)
    sf = T[:, :, :, :].min(axis=1).sum(axis=0)
    iA, ib = np.unravel_index(int(np.argmin(sf)), sf.shape)
    row["a0_at_best_prof"] = float(A0GRID[ib])
    res[rd] = row
    zs = lambda q: f">{q:.0f}" if q >= 20 else f"{q:.1f}"
    P(f"    {rd:12s} " + "  ".join(f"{m}: A = {row[m]['A']:+.3f} +/- {max(row[m]['sig'], 0.02):.3f} (A=1 at {zs(row[m]['z_law'])} sigma)"
                                     for m in ("fixed", "profU", "free", "prof")) + f"  [a0 at best: {row['a0_at_best_prof']:.3e}]")
OUT["numbers"]["amplitude"] = res
zmin = min(res[rd]["prof"]["z_law"] for rd in READINGS)
check("T2 the law's active mass (A = 1) is excluded in EVERY reading with a0 free and Upsilon_d profiled per "
      "galaxy (galaxy bootstrap)", "; ".join(f"{rd}: A = {res[rd]['prof']['A']:+.3f}+/-{res[rd]['prof']['sig']:.3f} "
                                             f"({res[rd]['prof']['z_law']:.1f} sigma)" for rd in READINGS),
      zmin > 3, "the rotation data carry no active phantom mass; the gentlest reading is the binding one; errors "
      "floored at the 0.02 grid step, so large z are lower bounds")

# ================================================================================================ T1
banner("T1  THE WITHIN-GALAXY RADIAL SHAPE (a per-galaxy offset -- any M/L or distance error -- is removed)")


def wslope(lr, e, w, gid):
    num = den = 0.0
    for g in np.unique(gid):
        m = gid == g
        if m.sum() < 3 or np.ptp(lr[m]) < 0.2:
            continue
        lm = np.average(lr[m], weights=w[m]); em = np.average(e[m], weights=w[m])
        num += np.sum(w[m] * (lr[m] - lm) * (e[m] - em)); den += np.sum(w[m] * (lr[m] - lm)**2)
    return num / den


lr_all, e_all, w_all, gid_all, pred = [], [], [], [], {rd: [] for rd in READINGS}
for i, g in enumerate(gals):
    lg, w = LOBS[i]
    l0, _, _ = arrays(g, 0.5, 0.0, "literal")
    lr_all.append(np.log10(g["R"])); e_all.append(lg - l0); w_all.append(w); gid_all.append(np.full(len(lg), i))
    for rd in READINGS:
        l1, _, _ = arrays(g, 0.5, 1.0, rd)
        pred[rd].append(l1 - l0)
lr_all, e_all, w_all, gid_all = map(np.concatenate, (lr_all, e_all, w_all, gid_all))
pred = {k: np.concatenate(v) for k, v in pred.items()}
b_data = wslope(lr_all, e_all, w_all, gid_all)
rng = np.random.default_rng(7)
bs = []
for _ in range(NBOOT):
    pick = rng.integers(0, NG, NG)
    idx = np.concatenate([np.where(gid_all == p)[0] for p in pick])
    gnew = np.concatenate([np.full((gid_all == p).sum(), j) for j, p in enumerate(pick)])
    bs.append(wslope(lr_all[idx], e_all[idx], w_all[idx], gnew))
sb = float(np.std(bs))
t1 = {rd: dict(b_law=float(wslope(lr_all, pred[rd], w_all, gid_all))) for rd in READINGS}
for rd in READINGS:
    t1[rd]["z"] = abs(b_data - t1[rd]["b_law"]) / sb
OUT["numbers"]["T1"] = dict(b_data=b_data, sig=sb, readings=t1)
P(f"    data: d(resid)/d log r = {b_data:+.4f} +/- {sb:.4f} (galaxy bootstrap)")
for rd in READINGS:
    P(f"    {rd:12s} predicts {t1[rd]['b_law']:+.4f}  -> {t1[rd]['z']:.1f} sigma")
check("T1 the within-galaxy radial trend of the residual is consistent with ZERO; it rejects the kernel-embedded "
      "literal and self-similar laws at > 5 sigma and the law AS WRITTEN (literal_deep) at > 3 sigma",
      f"data {b_data:+.4f}+/-{sb:.4f}; z(literal) {t1['literal']['z']:.1f}, z(selfsimilar) {t1['selfsimilar']['z']:.1f}, "
      f"z(enclosed) {t1['enclosed']['z']:.1f}, z(literal_deep) {t1['literal_deep']['z']:.1f}",
      abs(b_data) < 3 * sb and min(t1['literal']['z'], t1['selfsimilar']['z']) > 5 and t1['literal_deep']['z'] > 3,
      "the shape test needs no M/L, no distance and no a0: the law's r-dependence is absent from the data")

# ================================================================================================ T3
banner("T3  L312 I3's OWN FALSIFIER: the RAR residual's mass correlation at fixed x in [0.05, 0.3]")
gm_e, gm_p, gm_M = [], [], []
for i, g in enumerate(gals):
    lg, w = LOBS[i]
    l0, gb, Mb = arrays(g, 0.5, 0.0, "literal")
    l1, _, _ = arrays(g, 0.5, 1.0, "literal")
    x = gb / a0c
    m = (x >= 0.05) & (x <= 0.3)
    if m.sum() < 2:
        continue
    gm_e.append(np.average(lg[m] - l0[m], weights=w[m])); gm_p.append(np.average(l1[m] - l0[m], weights=w[m]))
    gm_M.append(math.log10(Mb / MSUN))
gm_e, gm_p, gm_M = map(np.array, (gm_e, gm_p, gm_M))
s_data = float(np.polyfit(gm_M, gm_e, 1)[0]); s_law = float(np.polyfit(gm_M, gm_p, 1)[0])
rng = np.random.default_rng(8)
sb3 = float(np.std([np.polyfit(gm_M[k], gm_e[k], 1)[0] for k in (rng.integers(0, len(gm_M), len(gm_M)) for _ in range(NBOOT))]))
off_data, off_law = float(np.median(gm_e)), float(np.median(gm_p))
OUT["numbers"]["T3"] = dict(n=len(gm_M), slope_data=s_data, sig=sb3, slope_law=s_law, median_data=off_data, median_law=off_law)
check("T3 (informational) L312 I3's mass SLOPE is NOT discriminating: data %+.3f +/- %.3f vs the literal law %+.3f; "
      "its LEVEL at fixed x is %+.3f dex vs the data %+.3f (Upsilon/a0-degenerate: T2 is the clean version)"
      % (s_data, sb3, s_law, off_law, off_data),
      f"N = {len(gm_M)} galaxies; slope z = {abs(s_data - s_law)/sb3:.1f}; level gap {off_law - off_data:+.3f} dex",
      abs(s_data - s_law) / sb3 < 2 and abs(off_law - off_data) > 0.1,
      "I3's advertised observable (the slope) cannot decide; the law dies on the level and the shape instead",
      load_bearing=False)

# ================================================================================================ T4
banner("T4  HEAD-TO-HEAD ON THE LAW'S OWN TERMS (a0 = c H_Lambda/Z fixed, Upsilon_d profiled per galaxy)")
ia1 = int(np.argmin(np.abs(AGRID - 1.0))); ia0_ = int(np.argmin(np.abs(AGRID - 0.0)))
law = TABLES["literal_deep"][:, :, ia1, ia0c].min(axis=1)            # the law as written, A = 1
deep0 = TABLES["literal_deep"][:, :, ia0_, ia0c].min(axis=1)         # the same deep form without the active mass
kern0 = TABLES["literal"][:, :, ia0_, ia0c].min(axis=1)              # the framework kernel, no active mass
rng = np.random.default_rng(9)
def boot_sum(d):
    return float(np.sum(d)), float(np.std([np.sum(d[rng.integers(0, NG, NG)]) for _ in range(NBOOT)]))
d_law_vs_deep0 = boot_sum(law - deep0)
d_law_vs_kern = boot_sum(law - kern0)
frac_kern = float(np.mean(kern0 < law))
OUT["numbers"]["T4"] = dict(a0_grid=float(A0GRID[ia0c]), dchi_law_minus_deep0=d_law_vs_deep0,
                            dchi_law_minus_kernel=d_law_vs_kern, frac_galaxies_prefer_kernel=frac_kern)
P(f"    at a0 = {A0GRID[ia0c]:.3e} (grid point nearest canonical): sum chi2(law) - chi2(deep, A=0) = "
  f"{d_law_vs_deep0[0]:+.1f} +/- {d_law_vs_deep0[1]:.1f}")
P(f"    sum chi2(law) - chi2(framework kernel, A=0) = {d_law_vs_kern[0]:+.1f} +/- {d_law_vs_kern[1]:.1f}; "
  f"{100*frac_kern:.0f}% of galaxies prefer the kernel")
check("T4 on the law's own terms the kernel WITHOUT any active mass fits better than the law as written "
      "(galaxy-bootstrap sign of the summed chi^2 difference)",
      f"chi2(law) - chi2(kernel) = {d_law_vs_kern[0]:+.1f} +/- {d_law_vs_kern[1]:.1f} "
      f"({d_law_vs_kern[0]/d_law_vs_kern[1]:.1f} bootstrap sigma); active mass vs none in the deep form: "
      f"{d_law_vs_deep0[0]:+.1f} +/- {d_law_vs_deep0[1]:.1f}",
      d_law_vs_kern[0] > 2 * d_law_vs_kern[1],
      "with the M/L profiled, the active mass does not significantly improve even the law's own deep form, and "
      "the ordinary kernel with no active mass beats the law outright")

# ================================================================================================ verdict
banner("VERDICT")
P(f"""  ON ITS OWN TERMS (the law as written, g_obs^2 = a0 g_N,tot, a0 = c H_Lambda/Z fixed): the amplitude is
  A = {res['literal_deep']['fixed']['A']:.2f} +/- {res['literal_deep']['fixed']['sig']:.2f} at Upsilon_d = 0.5 ({res['literal_deep']['fixed']['z_law']:.1f} sigma below 1) and A = {res['literal_deep']['profU']['A']:.2f} +/- {max(res['literal_deep']['profU']['sig'], 0.02):.2f} with the M/L
  profiled per galaxy ({res['literal_deep']['profU']['z_law']:.1f} sigma); the within-galaxy shape is off at
  {t1['literal_deep']['z']:.1f} sigma, and the plain framework kernel with NO active mass fits better
  (chi2 difference {d_law_vs_kern[0]:+.0f} +/- {d_law_vs_kern[1]:.0f}). DISFAVOURED at ~4 sigma, not killed.
  THE ACTIVE MASS IS NOT NEEDED: free a0 or profiled M/L drive A -> {res['literal_deep']['prof']['A']:+.2f}; in every kernel
  embedding A = 1 is excluded (>= {zmin:.1f} sigma, the enclosed reading being the gentlest). The pipeline recovers
  A = 1 when the law is injected, so the null is measured, not an insensitivity.
  Standing consequence: L311's "law of nature" and L312's implications (the halo-baryon correspondence, the
  self-truncation at 790 kpc, the M_b^(+1/4) residual) rest on an active mass SPARC does not want; what SPARC
  wants is the ordinary kernel with a0 ~ {res['literal']['a0_at_best_prof']:.2e} (M/L profiled; 5.6% grid).""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
