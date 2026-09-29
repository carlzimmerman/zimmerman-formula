#!/usr/bin/env python3
"""Synthetic tests for cut13.py: literal 5-sigma vs orbit-aware criteria.

    python3 test_cut13.py            # tests, disagreement table, MUTATE control

Exit code 0 only if (i) every real test passes and (ii) the MUTATE control
(PM inequality inverted) is caught by the tests.  About 20 s.

What is tested (all SYNTHETIC; no DR3/DR4 data, no network):
  T0  the DR4 error-model copy below equals wide_binary_pipeline.py lines
      200-205 (drift check by reading that file, read-only).
  T1  grid: third-star G = 15..20 (step 0.5; the top column is 19.999 because G < 20 is strict) x d = 100/150/250 pc x third at
      the 30 kAU edge and at 10 kAU.  For each cell a third star is planted at
      many proper-motion offsets delta from the pair; the largest delta each
      criterion flags is found by calling the REAL functions and must bracket
      the analytic threshold  5*sdmu  (literal)  and  orb + 2*sdmu
      (orbit-aware),  sdmu = hypot(sigma_pm(G_pair), sigma_pm(G3)).
  T2  the Amendment 16 draft arithmetic: orb(250 pc, 120") = 0.324 mas/yr,
      crossover sdmu = orb/3 = 0.108 mas/yr, per-star errors 0.026/0.052/
      0.111/0.259 at G = 17/18/19/20, and the regime statements (250 pc: code
      flags more at G <~ 18, literal more at G = 20; 100 pc: code flags more
      throughout).
  T3  boundary behaviour: G < 20 strict, NaN G dropped and counted, 3-sigma
      parallax edge, 30 kAU edge, third near component b, orbit-aware theta
      taken from the primary (reproduced quirk), reference='mean', errors.
  T4  cross-check of the orbit-aware function and the copied maths against the
      builder's own third_star_flags / ang_sep_arcsec / delta_mu_and_sigma on
      random data (import is read-only; bytecode writing is disabled).
  MUTATE  cut13._MUTATE inverts the PM inequality; T1 and T3 must then FAIL.
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np

HERE = Path(__file__).resolve().parent
PREP = HERE.parent
sys.path.insert(0, str(HERE))
import cut13  # noqa: E402

# ------------------------------------------------------------------
# Repo's approximate DR4 error model: wide_binary_pipeline.py lines 200-206
#   _GGRID / _SPM_DR3 / _SPLX_DR3 (DR3 table, Lindegren+21-based, APPROX)
#   PM_FAC_DR4 = (66/34)^-1.5 = 0.372, PLX_FAC_DR4 = (66/34)^-0.5 = 0.718
#   sigma_pm(G, dr4) = interp(G) * factor          (lines 205-206)
# Copied, and T0 checks the copy against the file.
# ------------------------------------------------------------------
_GGRID = np.array([6., 12., 14., 15., 16., 17., 18., 19., 20.])
_SPM_DR3 = np.array([.016, .014, .016, .020, .035, .070, .140, .300, .700])
_SPLX_DR3 = np.array([.021, .016, .019, .025, .040, .070, .130, .250, .600])
PM_FAC_DR4, PLX_FAC_DR4 = (66 / 34.) ** -1.5, (66 / 34.) ** -0.5


def sigma_pm(G):
    return np.interp(G, _GGRID, _SPM_DR3) * PM_FAC_DR4


def sigma_plx(G):
    return np.interp(G, _GGRID, _SPLX_DR3) * PLX_FAC_DR4


G_PAIR = 17.0      # cut 2 allows G < 17: 17 is the faintest allowed, the largest sdmu contribution
S_PAIR_KAU = 10.0  # pair separation in the synthetic set-up

FAILS: list[str] = []


def check(name, ok, detail=""):
    if not ok:
        FAILS.append(name)
    print(f"  [{'ok' if ok else 'FAIL'}] {name}" + (f"   {detail}" if detail else ""))


# ------------------------------------------------------------------
# synthetic catalogue builder
# ------------------------------------------------------------------
class Cat:
    """Accumulates (pair a, pair b, third) triplets at well-separated sky spots."""

    def __init__(self):
        self.rows = []      # each: dict of the 9 columns
        self.a, self.b, self.meta = [], [], []
        self.n_spots = 0

    def _spot(self):
        k = self.n_spots
        self.n_spots += 1
        ra = (k % 360) * 1.0 + 0.5
        dec = -70.0 + (k // 360) * 3.2
        return ra, dec

    def add(self, d_pc, G3, delta, s3_kau, *, near="a", plx_off_sig=0.0, g_pair=G_PAIR,
            third_from_b_kau=None, meta=None):
        """Pair (a,b) at d_pc, b displaced S_PAIR_KAU along RA from a.  Third
        star: at projected s3_kau from a along Dec (near='a'), or
        third_from_b_kau beyond b along RA (near='b').  PM offset delta (mas/yr,
        along RA) and parallax offset plx_off_sig * hypot(e_plx_ref, e_plx_3)."""
        plx = 1000.0 / d_pc
        ra0, dec0 = self._spot()
        as_per_kau = 1000.0 / d_pc                       # arcsec per kAU at d_pc
        cosd = np.cos(np.radians(dec0))
        e_pm_p, e_plx_p = float(sigma_pm(g_pair)), float(sigma_plx(g_pair))
        e_pm_3 = float(sigma_pm(G3)) if np.isfinite(G3) else float(sigma_pm(20.0))
        e_plx_3 = float(sigma_plx(G3)) if np.isfinite(G3) else float(sigma_plx(20.0))
        dra_b = S_PAIR_KAU * as_per_kau / 3600 / cosd
        if near == "a":
            r3, d3 = ra0, dec0 + s3_kau * as_per_kau / 3600
        else:
            r3, d3 = ra0 + (S_PAIR_KAU + third_from_b_kau) * as_per_kau / 3600 / cosd, dec0
        plx3 = plx + plx_off_sig * np.hypot(e_plx_p, e_plx_3)

        def row(ra, dec, p, ep, pmra, e_pm, g):
            return dict(ra=ra, dec=dec, parallax=p, parallax_error=ep, pmra=pmra, pmdec=-10.0,
                        pmra_error=e_pm, pmdec_error=e_pm, phot_g_mean_mag=g)
        base = len(self.rows)
        self.rows.append(row(ra0, dec0, plx, e_plx_p, 25.0, e_pm_p, g_pair))
        self.rows.append(row(ra0 + dra_b, dec0, plx, e_plx_p, 25.0, e_pm_p, g_pair))
        self.rows.append(row(r3, d3, plx3, e_plx_3, 25.0 + delta, e_pm_3, G3))
        self.a.append(base)
        self.b.append(base + 1)
        self.meta.append(meta)

    def arrays(self):
        cat = {k: np.array([r[k] for r in self.rows], float) for k in cut13.REQUIRED}
        return cat, np.array(self.a), np.array(self.b)


def one_case(d, G3, delta, s3, **kw):
    c = Cat()
    c.add(d, G3, delta, s3, **kw)
    cat, a, b = c.arrays()
    return cut13.third_star_literal(cat, a, b), cut13.third_star_orbit_aware(cat, a, b)


# ------------------------------------------------------------------
# T0
# ------------------------------------------------------------------
def t0_error_model_drift():
    print("T0 error-model copy vs wide_binary_pipeline.py lines 200-206")
    txt = (PREP / "wide_binary_pipeline.py").read_text()

    def grab(name):
        m = re.search(name + r"\s*=\s*np\.array\(\[([^\]]*)\]\)", txt)
        return np.array([float(x) for x in m.group(1).split(",")])
    check("G grid identical", np.allclose(grab("_GGRID"), _GGRID))
    check("sigma_pm DR3 table identical", np.allclose(grab("_SPM_DR3"), _SPM_DR3))
    check("sigma_plx DR3 table identical", np.allclose(grab("_SPLX_DR3"), _SPLX_DR3))
    check("DR4 factor line present", "PM_FAC_DR4, PLX_FAC_DR4 = (66/34.)**-1.5, (66/34.)**-0.5" in txt)


# ------------------------------------------------------------------
# T1 grid
# ------------------------------------------------------------------
DISTS = (100.0, 150.0, 250.0)
G3S = np.arange(15.0, 20.01, 0.5)
G3S[-1] = 19.999   # the '20' column is planted at 19.999: G < 20 is strict (a G = 20.0 third is never flagged; tested in T3)
S3_EDGE, S3_INNER = 29.9, 10.0
DELTAS = np.geomspace(0.005, 20.0, 240)


def analytic(d, G3, s3, g_pair=G_PAIR):
    plx = 1000.0 / d
    theta = s3 * 1000.0 / d
    orb = float(cut13.orbit_allowance(plx, theta))
    sd = float(np.hypot(sigma_pm(g_pair), sigma_pm(G3)))
    return orb, sd, 5 * sd, orb + 2 * sd


def grid_thresholds(dists, G3s, s3, deltas=DELTAS):
    """For each (d, G3): largest delta flagged by each real function, plus the
    grid index bracket.  One catalogue per s3 holds every cell x delta."""
    c = Cat()
    cells = []
    for d in dists:
        for G3 in G3s:
            cells.append((d, G3))
            for dl in deltas:
                c.add(d, G3, dl, s3)
    cat, a, b = c.arrays()
    rl = cut13.third_star_literal(cat, a, b)
    ro = cut13.third_star_orbit_aware(cat, a, b)
    out = {}
    n = len(deltas)
    for ci, cell in enumerate(cells):
        fl = rl.flags[ci * n:(ci + 1) * n]
        fo = ro.flags[ci * n:(ci + 1) * n]
        out[cell] = (fl, fo)
    return out


def bracket_ok(flags, deltas, thr):
    """flags must be True exactly for deltas < thr (monotone, threshold inside grid step)."""
    return bool(np.array_equal(flags, deltas < thr))


def t1_grid(dists=DISTS, G3s=G3S, verbose=True):
    print("T1 grid of real-function thresholds vs analytic (5*sdmu ; orb+2*sdmu)")
    rows = []
    all_ok = True
    bad = []
    for s3 in (S3_EDGE, S3_INNER):
        res = grid_thresholds(dists, G3s, s3)
        for (d, G3), (fl, fo) in res.items():
            orb, sd, thr_l, thr_o = analytic(d, G3, s3)
            ok_l = bracket_ok(fl, DELTAS, thr_l)
            ok_o = bracket_ok(fo, DELTAS, thr_o)
            if not (ok_l and ok_o):
                all_ok = False
                bad.append((s3, d, G3, ok_l, ok_o))
            rows.append((s3, d, G3, sd, orb, thr_l, thr_o))
    check(f"literal and orbit-aware thresholds bracket the analytic values in all {len(rows)} cells",
          all_ok, f"failing cells: {bad[:3]}{'...' if len(bad) > 3 else ''}" if bad else "")
    # the sign of the difference is exactly the sign of (3 sdmu - orb)
    sign_ok = all(np.sign(tl - to) == np.sign(3 * sd - orb) for (_, _, _, sd, orb, tl, to) in rows)
    check("sign(literal - orbit-aware threshold) == sign(3*sdmu - orb) in every cell", sign_ok)
    return rows


def print_disagreement_table(rows):
    print("\nDISAGREEMENT TABLE (pair at G=17 both; third's PM offset delta from the pair; mas/yr)")
    print("  'orb+2s' = orbit-aware flags delta < orb+2*sdmu ;  '5s' = literal flags delta < 5*sdmu")
    print("  MORE = which criterion flags more thirds; band = delta range where they DISAGREE")
    for s3 in (S3_EDGE, S3_INNER):
        print(f"\n  third at {s3:.1f} kAU from primary (" + ("the 30 kAU edge" if s3 == S3_EDGE else "interior") + ")")
        print("   d[pc] theta[\"]  G3   sdmu   orb   5s     orb+2s  MORE         band(width)")
        for (s, d, G3, sd, orb, tl, to) in rows:
            if s != s3 or abs(G3 - round(G3)) > 0.01:      # table prints integer G3 only; regimes below use all
                continue
            more = "orbit-aware" if to > tl else "literal    "
            print(f"   {d:5.0f} {s3 * 1000 / d:7.1f} {G3:5.1f} {sd:6.3f} {orb:6.3f} {tl:6.3f} {to:7.3f}  {more}  "
                  f"[{min(tl, to):.3f}, {max(tl, to):.3f}] ({abs(tl - to):.3f})")
    print("\nREGIMES (edge column, 30 kAU): for each distance, the G3 range where each criterion is the larger")
    for d in DISTS:
        cells = [(G3, tl, to) for (s, dd, G3, sd, orb, tl, to) in rows if s == S3_EDGE and dd == d]
        lit = [g for g, tl, to in cells if tl > to]
        orbm = [g for g, tl, to in cells if to > tl]
        print(f"   {d:.0f} pc: orbit-aware flags more at G3 = {fmt_range(orbm)}; literal flags more at G3 = {fmt_range(lit)}")
    print("   Crossover G3* (3*sdmu = orb) at the 30 kAU edge, by the pair's G:")
    for gp in (15.0, 16.0, 17.0):
        parts = []
        for d in DISTS:
            parts.append(f"{d:.0f} pc: {crossover_G3(d, S3_EDGE, gp):.2f}")
        print(f"     pair G = {gp:.0f}: " + "; ".join(parts))


def fmt_range(gs):
    return "none" if not gs else f"{min(gs):.1f}-{max(gs):.1f}"


def crossover_G3(d, s3, g_pair):
    lo, hi = 12.0, 20.0
    plx, theta = 1000.0 / d, s3 * 1000.0 / d
    orb = float(cut13.orbit_allowance(plx, theta))
    f = lambda G: 3 * np.hypot(sigma_pm(g_pair), sigma_pm(G)) - orb
    if f(lo) > 0:
        return float("nan")      # literal larger at every G3 in range
    if f(hi) < 0:
        return float("inf")      # orbit-aware larger at every G3 in range
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if f(mid) < 0 else (lo, mid)
    return 0.5 * (lo + hi)


# ------------------------------------------------------------------
# T2 Amendment 16 arithmetic
# ------------------------------------------------------------------
def t2_amendment_arithmetic(rows):
    print("T2 Amendment 16 draft arithmetic")
    orb250 = float(cut13.orbit_allowance(4.0, 120.0))
    check("orb(250 pc, theta=120\") = 0.324 mas/yr", abs(orb250 - 0.324) < 5e-4, f"{orb250:.5f}")
    check("crossover sdmu = orb/3 = 0.108 mas/yr", abs(orb250 / 3 - 0.108) < 5e-4, f"{orb250 / 3:.5f}")
    per_star = [float(sigma_pm(g)) for g in (17, 18, 19, 20)]
    check("per-star DR4 sigma_pm at G=17/18/19/20 = 0.026/0.052/0.111/0.259",
          [round(x, 3) for x in per_star] == [0.026, 0.052, 0.111, 0.259], str([round(x, 4) for x in per_star]))
    edge250 = {round(G3, 3): (tl, to) for (s, d, G3, sd, orb, tl, to) in rows if s == S3_EDGE and d == 250.0}
    check("250 pc, edge: orbit-aware flags more for every G3 <= 18",
          all(edge250[round(g, 3)][1] > edge250[round(g, 3)][0] for g in G3S if g <= 18.0))
    check("250 pc, edge: literal flags more at G3 = 20", edge250[19.999][0] > edge250[19.999][1])
    g19 = edge250[19.0]
    print(f"     (G3 = 19 at 250 pc is the borderline: literal {g19[0]:.3f}, orbit-aware {g19[1]:.3f} mas/yr; "
          f"the Amendment's per-star value 0.111 vs crossover 0.108 is the same near-tie)")
    check("100 pc, edge: orbit-aware flags more at every G3 = 15..20",
          all(to > tl for (s, d, G3, sd, orb, tl, to) in rows if s == S3_EDGE and d == 100.0))
    gstar = crossover_G3(250.0, S3_EDGE, G_PAIR)
    check("250 pc crossover G3* sits between 18 and 19.5 (pair G=17)", 18.0 < gstar < 19.5, f"G3* = {gstar:.2f}")
    # the Amendment's sentence "code flags more at G <~ 18": true at G3=18, and consistent with G3* > 18


# ------------------------------------------------------------------
# T3 boundaries
# ------------------------------------------------------------------
def t3_boundaries():
    print("T3 boundary behaviour (d = 250 pc unless stated; delta = 0.01 mas/yr so PM always passes)")
    d = 250.0
    # G < 20 strict
    for G3, exp in ((19.99, True), (20.0, False), (20.5, False)):
        rl, ro = one_case(d, G3, 0.01, 20.0)
        check(f"G3 = {G3}: flagged == {exp} (both criteria)", rl.flags[0] == exp and ro.flags[0] == exp)
    # NaN G: not flagged, counted separately
    rl, ro = one_case(d, np.nan, 0.01, 20.0)
    check("NaN G: not flagged by either", not rl.flags[0] and not ro.flags[0])
    check("NaN G: counted (n_no_g = n_no_g_kin = 1, both criteria)",
          (rl.n_no_g, rl.n_no_g_kin, ro.n_no_g, ro.n_no_g_kin) == (1, 1, 1, 1),
          f"{(rl.n_no_g, rl.n_no_g_kin, ro.n_no_g, ro.n_no_g_kin)}")
    rl, ro = one_case(d, np.nan, 50.0, 20.0)
    check("NaN G with PM far off: counted in n_no_g but NOT in n_no_g_kin",
          rl.n_no_g == 1 and rl.n_no_g_kin == 0 and ro.n_no_g_kin == 0)
    # a co-moving third with NO parallax/PM (2-parameter solution): never flagged, never in n_no_g, counted in n_no_kin
    c = Cat(); c.add(d, 19.0, 0.01, 20.0)
    cat, a_, b_ = c.arrays()
    cat["parallax"][2] = np.nan; cat["pmra"][2] = np.nan
    rl = cut13.third_star_literal(cat, a_, b_); ro = cut13.third_star_orbit_aware(cat, a_, b_)
    check("third with NaN parallax/PM (G = 19): not flagged, n_no_g = 0, n_no_kin = 1 (both criteria)",
          (not rl.flags[0]) and (not ro.flags[0]) and rl.n_no_g == 0 and ro.n_no_g == 0 and rl.n_no_kin == 1 and ro.n_no_kin == 1,
          f"{(rl.flags[0], rl.n_no_g, rl.n_no_kin, ro.flags[0], ro.n_no_g, ro.n_no_kin)}")
    rl, ro = one_case(d, 17.0, 0.01, 20.0)
    check("normal third: n_no_kin = 0", rl.n_no_kin == 0 and ro.n_no_kin == 0)
    rl, ro = one_case(d, 17.0, 0.01, 20.0)
    check("normal third: n_no_g = 0 and n_neigh = 1", rl.n_no_g == 0 and rl.n_neigh == 1 and ro.n_neigh == 1)
    # parallax 3 sigma edge
    for k, exp in ((2.9, True), (3.1, False)):
        rl, ro = one_case(d, 17.0, 0.01, 20.0, plx_off_sig=k)
        check(f"parallax offset {k} sigma: flagged == {exp} (both)", rl.flags[0] == exp and ro.flags[0] == exp)
    # 30 kAU edge (radius is measured from either component; b is 10 kAU east of a)
    for s3, exp in ((29.9, True), (30.3, False)):
        rl, ro = one_case(d, 17.0, 0.01, s3)
        check(f"third at {s3} kAU from primary: flagged == {exp} (both)", rl.flags[0] == exp and ro.flags[0] == exp)
    # near b, beyond 30 kAU from a but inside 30 kAU of b
    rl, ro = one_case(d, 17.0, 0.01, None, near="b", third_from_b_kau=25.0)
    check("third 25 kAU beyond b (35 kAU from a): flagged (either component counts), both",
          rl.flags[0] and ro.flags[0])
    rl, ro = one_case(d, 17.0, 0.01, None, near="b", third_from_b_kau=31.0)
    check("third 31 kAU beyond b: not flagged, both", (not rl.flags[0]) and (not ro.flags[0]))
    # orbit-aware theta is taken from the PRIMARY (reproduced quirk of build_catalog.py l.377-385)
    d100 = 100.0
    plx = 10.0
    sd = float(np.hypot(sigma_pm(G_PAIR), sigma_pm(15.0)))
    orb_a = float(cut13.orbit_allowance(plx, 35.0 * 1000 / d100))   # theta from primary (35 kAU)
    orb_b = float(cut13.orbit_allowance(plx, 25.0 * 1000 / d100))   # theta from b (25 kAU)
    delta = 0.5 * (orb_a + orb_b) + 2 * sd
    rl, ro = one_case(d100, 15.0, delta, None, near="b", third_from_b_kau=25.0)
    check("quirk: third near b, delta between the two thetas' bounds -> orbit-aware uses the primary's theta (not flagged)",
          (not ro.flags[0]) and (not rl.flags[0]), f"delta={delta:.3f} orb_a+2s={orb_a + 2 * sd:.3f} orb_b+2s={orb_b + 2 * sd:.3f}")
    # reference='mean' and errors
    c = Cat()
    c.add(d, 17.0, 0.01, 20.0)
    cat, a, b = c.arrays()
    m = cut13.third_star_literal(cat, a, b, reference="mean")
    p = cut13.third_star_literal(cat, a, b, reference="primary")
    check("reference='mean' == 'primary' when both components are identical", m.flags[0] == p.flags[0] and m.n_neigh == p.n_neigh)
    for label, fn in (("bad reference string", lambda: cut13.third_star_literal(cat, a, b, reference="x")),
                      ("orbit-aware with reference='mean'", lambda: cut13.third_star_orbit_aware(cat, a, b, reference="mean")),
                      ("missing column", lambda: cut13.third_star_literal({k: v for k, v in cat.items() if k != "pmra"}, a, b))):
        try:
            fn()
            ok = False
        except (ValueError, KeyError):
            ok = True
        check(f"raises on {label}", ok)
    # no third at all
    c = Cat()
    c.add(d, 17.0, 0.01, 20.0)
    cat, a, b = c.arrays()
    cat = {k: v[:2] for k, v in cat.items()}
    rl = cut13.third_star_literal(cat, a, b)
    check("no candidate neighbours: no flag, n_neigh = 0", (not rl.flags[0]) and rl.n_neigh == 0)


# ------------------------------------------------------------------
# T4 cross-check against the builder (read-only import)
# ------------------------------------------------------------------
def t4_builder_crosscheck():
    print("T4 cross-check against catalog_builder/build_catalog.py (read-only import)")
    try:
        sys.path.insert(0, str(PREP / "catalog_builder"))
        import build_catalog as bc
    except Exception as e:  # noqa: BLE001
        print(f"  [SKIPPED] could not import build_catalog ({type(e).__name__}: {e}); NOT verified against the builder")
        return
    rng = np.random.default_rng(13)
    x = rng.normal(size=(8, 200))
    dm1, s1 = bc.delta_mu_and_sigma(*[np.abs(v) if i >= 4 else v for i, v in enumerate(x)])
    dm2, s2 = cut13._delta_mu_and_sigma(*[np.abs(v) if i >= 4 else v for i, v in enumerate(x)])
    check("copied delta_mu_and_sigma == builder", np.array_equal(dm1, dm2) and np.array_equal(s1, s2, equal_nan=True))
    r = rng.uniform(0, 360, (4, 200)); r[1] = rng.uniform(-80, 80, 200); r[3] = rng.uniform(-80, 80, 200)
    check("copied ang_sep_arcsec == builder", np.allclose(bc.ang_sep_arcsec(*r), cut13._ang_sep_arcsec(*r), rtol=0, atol=1e-9))
    # random field: pairs with 0-3 thirds around either component, PM/parallax/G random
    rows, a_idx, b_idx = [], [], []
    for k in range(300):
        d = rng.choice([80.0, 120.0, 180.0, 245.0]); plx = 1000 / d
        ra0, dec0 = (k % 100) * 3.5 + 1, -60 + (k // 100) * 40 + rng.uniform(0, 5)
        asec_per_kau = 1000 / d
        gp = rng.uniform(12, 17)

        def mk(ra, dec, p, ep, pm1, pm2, epm, g):
            return dict(ra=ra, dec=dec, parallax=p, parallax_error=ep, pmra=pm1, pmdec=pm2,
                        pmra_error=epm, pmdec_error=epm * rng.uniform(0.8, 1.2), phot_g_mean_mag=g)
        pm = rng.normal(0, 30, 2)
        base = len(rows)
        rows.append(mk(ra0, dec0, plx, float(sigma_plx(gp)), pm[0], pm[1], float(sigma_pm(gp)), gp))
        rows.append(mk(ra0 + 8 * asec_per_kau / 3600 / np.cos(np.radians(dec0)), dec0, plx, float(sigma_plx(gp)),
                       pm[0] + rng.normal(0, .02), pm[1] + rng.normal(0, .02), float(sigma_pm(gp)), gp))
        a_idx.append(base); b_idx.append(base + 1)
        for _ in range(rng.integers(0, 4)):
            g3 = rng.uniform(15, 21.5)
            ang = rng.uniform(0, 2 * np.pi); rad = rng.uniform(3, 44) * asec_per_kau / 3600
            cx = rows[base + rng.integers(0, 2)]
            e3 = float(sigma_pm(min(g3, 20)))
            rows.append(mk(cx["ra"] + rad * np.cos(ang) / np.cos(np.radians(dec0)), cx["dec"] + rad * np.sin(ang),
                           plx + rng.normal(0, 2.0) * float(sigma_plx(g3)), float(sigma_plx(min(g3, 20))),
                           pm[0] + rng.normal(0, 3.0) * (e3 + 0.15 * rng.uniform()), pm[1] + rng.normal(0, 3.0) * (e3 + 0.15 * rng.uniform()),
                           e3, g3))
    S = {k: np.array([r[k] for r in rows], float) for k in cut13.REQUIRED}
    a_idx, b_idx = np.array(a_idx), np.array(b_idx)
    ref = bc.third_star_flags(S, a_idx, b_idx)
    mine = cut13.third_star_orbit_aware(S, a_idx, b_idx).flags
    lit = cut13.third_star_literal(S, a_idx, b_idx).flags
    check("orbit-aware flags identical to builder third_star_flags on 300 random pairs",
          np.array_equal(ref, mine), f"builder hits {ref.sum()}, mine {mine.sum()}, literal {lit.sum()}, mismatches {(ref != mine).sum()}")
    check("cross-check is not degenerate (0 < hits < 300, and literal differs from orbit-aware somewhere)",
          0 < ref.sum() < 300 and (lit != mine).any())


# ------------------------------------------------------------------
def run_real():
    t0 = time.time()
    t0_error_model_drift()
    rows = t1_grid()
    t2_amendment_arithmetic(rows)
    t3_boundaries()
    t4_builder_crosscheck()
    print_disagreement_table(rows)
    print(f"\nreal tests: {len(FAILS)} failure(s) in {time.time() - t0:.1f} s")
    return len(FAILS)


def run_mutate():
    """Invert the PM inequality; the T1 and T3 checks must now fail."""
    print("\n=== MUTATE control: PM inequality inverted (cut13._MUTATE = True); tests are REQUIRED to fail ===")
    FAILS.clear()
    cut13._MUTATE = True
    try:
        # reduced T1 grid (cheap) and the full T3
        t1_grid(dists=(250.0,), G3s=np.array([16.0, 20.0]))
        t1_failed = bool(FAILS)
        n1 = len(FAILS)
        t3_boundaries()
        t3_failed = len(FAILS) > n1
    finally:
        cut13._MUTATE = False
    caught = t1_failed and t3_failed
    print(f"MUTATE control: T1 caught = {t1_failed}, T3 caught = {t3_failed} -> "
          + ("DETECTED (control passes)" if caught else "NOT DETECTED (the tests are blind: control FAILS)"))
    return caught


if __name__ == "__main__":
    nfail = run_real()
    real_fails = list(FAILS)
    caught = run_mutate()
    ok = nfail == 0 and caught
    print(f"\nRESULT: real failures = {len(real_fails)}; mutate detected = {caught}; overall {'PASS' if ok else 'FAIL'}")
    sys.exit(0 if ok else 1)
