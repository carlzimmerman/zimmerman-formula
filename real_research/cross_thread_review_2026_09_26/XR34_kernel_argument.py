#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR34_kernel_argument -- IS THE MOND KERNEL'S ARGUMENT IN THE RECORD'S PARTICLE-MESH FOREST LANES WRONG?  (before any re-score)

WHY.  XR21 (U2) reported that L346, L347, L362, DE11 and DE11b evaluate the MOND kernel at |grad phi|/a^2, which it read as
(1+z) times the physical field: MOND about sqrt(1+z) too weak at z = 2-3.  Before anything is re-scored this lane shows
from the codes' own lines whether that is so, and which record scripts carry the pattern.

THE CODE'S CONVENTION, FROM ITS OWN LINES (L362:180-200; L347:201-221, L346:187-225, L359:96-117, DE11:100-129 and
DE11b:88-116 are the same lines).  Units H0 = 1, lengths comoving Mpc/h, t in 1/H0.
    drift   x <- x + dt p / a^2                 =>  p = a^2 dx/dt
    kick    p <- p + dt (-grad_x phi)           =>  dp/dt = -grad_x phi
    Poisson lap_x phi = 1.5 Om delta / a        =  4 pi G a^2 rho_bar_m(a) delta   (4 pi G rho_m0 = 1.5 Om H0^2)
The Poisson line makes phi the PHYSICAL peculiar potential Phi (lap_r Phi = 4 pi G rho_bar delta, r = a x).  With the
peculiar velocity v = a dx/dt = p/a, the peculiar equation of motion dv/dt + H v = g gives g = (dp/dt)/a, so the kick is
the physical acceleration only if g = -grad_x Phi / a, which is also -grad_r Phi.  Both lines agree: the physical
Newtonian field is |grad_x phi| / a.  The kernel is evaluated at |grad_x phi| / a^2 = (1+z) g_N,phys (in L346 through
gN = -grad phi / a^2).  THE CORRECT ARGUMENT, in code units, is  y = |grad_x phi_N| / (a a0),  a0 = a0_SI / UNIT_ACC with
UNIT_ACC = (Mpc/h) H0^2 in m s^-2 (the lanes' own constant).  (A code written in GADGET's convention, phi_c = a Phi, would
use a^2 -- but then its Poisson source would carry no 1/a and its kick would be -grad phi_c / a.  These codes have neither.)
In the deep regime nu - 1 ~ y^(-1/2), so the committed line makes the MOND term sqrt(1+z) too weak: 2.0 at z = 3, 1.73 at
z = 2.  At z = 0 (a = 1) the two lines coincide.

CHECKS (pre-declared before any XR34 run; the single-halo tolerance, 2%, was fixed after one exploratory probe of the
mesh error, which is <= 0.9% for the corrected line on this halo -- see XR34_README 'Disclosures')
  B0 [load-bearing] each lane's OWN Newtonian kick (its LCDM branch of accel(): its Poisson solve and gradient), divided by
     a, equals G M(<r)/r_phys^2 computed from SI constants alone for a Plummer sphere, at z = 3, 2 and 0 (2%, r = 8-16
     cells, six directions); divided by a^2 it is (1+z) too large (reported).
  B1 [load-bearing] the dynamics is the physical one: L346's own LCDM run (its committed P(k) at z = 6, the earliest,
     most linear output) over its regenerated z = 49 ICs grows the two largest-scale bins at the linear-theory rate D^2
     (5%).  A force wrong by a factor a or 1/a would miss by the factors printed alongside.  (The z = 6 / two-bin choice
     was made after an exploratory look at z = 6, 3, 2; z = 3 and 2 are printed.)
  K1 [load-bearing] the single-halo QUMOND profile, run through each lane's OWN accel() (patched only in the kernel line,
     switch on everywhere): with the CORRECTED line the kick/a matches nu_mono(g_N/a0) g_N (analytic, SI) to 2% at every
     radius, z = 3, 2, 0, both footings -- in all six code variants (L346, L347, L359, L362, DE11, DE11b).
  K2 [load-bearing] the bug is exactly the derivation's: for the committed line, the corrected line and the doubled
     correction alike, the measured profile ratio equals the predicted nu_mono(s y)/nu_mono(y), s = (1+z), 1, 1/(1+z), to
     2%; the committed line FAILS K1's 2% at z = 3 and 2 and passes at z = 0.
  S1 (reported) the census: every record .py (real_research/, fable_independent_2026/) carrying the pattern, by reading;
     which import it; which read the affected JSONs downstream.
MUTATE=1: the correction applied twice ('double', argument g_N,phys/(1+z)) is taken as "the corrected line" in K1:
K1 must FAIL (rc = 1).

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR34_kernel_argument.py   (MUTATE=1 first)
"""
import os, sys, re, json, math, glob, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import XR34_common as X                                                 # noqa: E402  (sets one thread per process)
import numpy as np                                                      # noqa: E402
from scipy.integrate import solve_ivp                                   # noqa: E402

MUTATE = os.environ.get("MUTATE", "0") == "1"
FIX = "double" if MUTATE else "fix"
TOL = 0.02
ZS = (3.0, 2.0, 0.0)
LN = X.Lane("XR34_kernel_argument", MUTATE)
P = LN.P

if __name__ == "__main__":
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: 'double' (|grad phi|/a^0) stands in for the corrected line; K1 must FAIL ***")

    # ============================================================================================== the one line, per lane
    LN.banner("THE LINE, PER LANE (the committed text, and the corrected text XR34 substitutes; nothing else changes)")
    lines = {}
    for lane in X.LANES:
        _, d = X.patched_source(lane, "fix")
        (ln, old, new), = d
        lines[lane] = dict(file=X.rel(X.lane_path(lane)), line=ln, committed=old.strip(), corrected=new.strip())
        P(f"    {lane:5s} {X.rel(X.lane_path(lane))}:{ln}\n          committed: {old.strip()}\n          corrected: {new.strip()}")
    LN.out["numbers"]["lines"] = lines

    # ============================================================================================== B0 + K1 + K2 per lane
    LN.banner("B0 K1 K2  THE SINGLE-HALO PROBE THROUGH EACH LANE'S OWN accel() (Plummer b = 4 cells, r = 8-16 cells)")
    tabs, summ = {}, {}
    for lane in X.LANES:
        for patch in ("none", "fix", "double"):
            t = X.halo_table(lane, patch)
            tabs[f"{lane}/{patch}"] = t
            summ[f"{lane}/{patch}"] = X.halo_summary(t)
        s0 = summ[f"{lane}/none"]
        P(f"    {lane:5s} box {tabs[lane + '/none']['box'][0]:g} Mpc/h, {tabs[lane + '/none']['box'][1]}^3 mesh   {LN.el()}")
        for zk in ("z3/canonical", "z3/alt", "z2/canonical", "z2/alt", "z0/canonical", "z0/alt"):
            row = "  ".join(f"{p_}: {summ[f'{lane}/{p_}'][zk]['ratio_min']:.3f}-{summ[f'{lane}/{p_}'][zk]['ratio_max']:.3f} "
                            f"(pred {min(tabs[f'{lane}/{p_}']['rows'][zk]['pred']):.3f}-{max(tabs[f'{lane}/{p_}']['rows'][zk]['pred']):.3f})"
                            for p_ in ("none", "fix", "double"))
            nw = tabs[f"{lane}/none"]["rows"][zk]["newton"]
            P(f"       {zk:13s} y {s0[zk]['y_min']:.3f}-{s0[zk]['y_max']:.3f}  Newton kick/a over SI {min(nw):.3f}-{max(nw):.3f}"
              f"  | kick/a over nu g_N -> {row}")
    LN.out["numbers"]["halo"] = {"summary": summ, "tables": tabs}

    b0 = max(v["newton"] for k, s in summ.items() if k.endswith("/none") for v in s.values())
    a2 = {f"z{z:g}": float(np.mean(tabs["L362/none"]["rows"][f"z{z:g}/canonical"]["newton_a2"])) for z in ZS}
    LN.check("B0 each lane's own Newtonian kick / a equals G M(<r)/r_phys^2 from SI constants (Plummer, z = 3, 2, 0, all six lanes)",
             f"max |kick/a over SI - 1| = {b0:.4f} (tolerance {TOL}); kick/a^2 over SI (L362, mean over r): "
             + ", ".join(f"{k} {v:.3f}" for k, v in a2.items()) + "  (= 1+z)",
             b0 <= TOL, "the codes' own phi_N is the physical peculiar potential: g_N,phys = |grad_x phi_N|/a; the "
             "committed kernel reads (1+z) g_N,phys")

    # ============================================================================================== B1 growth
    LN.banner("B1  THE DYNAMICS: L346's own LCDM run grows its largest modes at the linear-theory rate")
    m46 = X.module("L346", "none")
    x_i, _ = m46.make_ics()
    rho_i = m46.cic_deposit(x_i, np.full(len(x_i), 1.0)) * m46.NG ** 3 / len(x_i)
    pk_i = m46.pk(rho_i - 1)
    R46 = json.load(open(os.path.join(X.G03, "L346_switch_forest_gate_results.json")))["numbers"]["runs"]["lcdm"]["pk"]

    def growth(fpow):
        """D(z)/D(49) for the PM background (Om, 1 - Om), with the force multiplied by a^fpow (fpow = 0 is the physical one)."""
        Om, OL = m46.Om, m46.OL

        def rhs(N, Y):
            a = math.exp(N); E2 = Om / a ** 3 + OL
            return [Y[1], 1.5 * Om / a ** 3 / E2 * a ** fpow * Y[0] - (2 - 1.5 * Om / a ** 3 / E2) * Y[1]]
        sol = solve_ivp(rhs, (math.log(1 / 50.0), 0.0), [1.0, 1.0], dense_output=True, rtol=1e-10, atol=1e-14)
        return lambda z: sol.sol(math.log(1 / (1 + z)))[0] / sol.sol(math.log(1 / 50.0))[0]
    Dt, Dlo, Dhi = growth(0), growth(1), growth(-1)
    B1 = {}
    for z in ("6.0", "3.0", "2.0"):
        pz = np.array(R46[z]); g2 = Dt(float(z)) ** 2
        rr = pz[:, 1] / pk_i[:, 1] / g2
        B1[z] = dict(k=pz[:2, 0].tolist(), ratio=rr[:2].tolist(), D2=g2, D2_force_times_a=Dlo(float(z)) ** 2,
                     D2_force_over_a=Dhi(float(z)) ** 2)
        P(f"    z = {z}: P(k)/P_ICs over D^2 = {g2:.1f}: k = {pz[0, 0]:.2f} -> {rr[0]:.3f}, k = {pz[1, 0]:.2f} -> {rr[1]:.3f}"
          f"   (force x a would give D^2 = {Dlo(float(z)) ** 2:.2f}; force / a would give {Dhi(float(z)) ** 2:.3g})")
    LN.out["numbers"]["B1"] = B1
    b1 = max(abs(v - 1) for v in B1["6.0"]["ratio"])
    LN.check("B1 L346's own LCDM run grows the two largest-scale bins at the linear rate at z = 6 (5%)",
             f"max |P/P_ICs/D^2 - 1| = {b1:.3f} at k = {B1['6.0']['k'][0]:.2f}, {B1['6.0']['k'][1]:.2f} h/Mpc; a force off by a "
             f"or 1/a misses D^2 by x{B1['6.0']['D2_force_times_a'] / B1['6.0']['D2']:.3f} or x{B1['6.0']['D2_force_over_a'] / B1['6.0']['D2']:.3g}",
             b1 <= 0.05, "the Poisson line and the kick together are the standard physical-potential PM")

    # ============================================================================================== K1 / K2
    LN.banner(f"K1 K2  THE KERNEL LINE ON THE ANALYTIC HALO ('{FIX}' stands for the corrected line)")
    k1 = max(v["ratio"] for lane in X.LANES for v in summ[f"{lane}/{FIX}"].values())
    LN.check(f"K1 with the corrected line every lane's QUMOND kick matches nu_mono(g_N/a0) g_N (z = 3, 2, 0; both footings; {TOL:.0%})",
             f"max |kick/a over nu g_N - 1| = {k1:.4f} over six lanes x 3 z x 2 footings x 9 radii ('{FIX}')", k1 <= TOL,
             "the corrected argument is the physical one; the residual is the mesh (grad o poisson o div on a 4-cell core)")
    k2p = max(v["vs_pred"] for k, s in summ.items() for v in s.values())
    bug = {zk: summ["L362/none"][zk]["ratio"] for zk in ("z3/canonical", "z3/alt", "z2/canonical", "z2/alt", "z0/canonical", "z0/alt")}
    fails_hi = all(summ[f"{lane}/none"][f"z{z:g}/{f}"]["ratio"] > TOL for lane in X.LANES for z in (3.0, 2.0) for f in ("canonical", "alt"))
    pass_lo = all(summ[f"{lane}/none"][f"z0/{f}"]["ratio"] <= TOL for lane in X.LANES for f in ("canonical", "alt"))
    LN.check("K2 the measured profile follows the derivation for all three lines (committed / corrected / doubled): ratio = "
             "nu(s y)/nu(y), s = 1+z | 1 | 1/(1+z), to 2%; the committed line fails K1 at z = 3 and 2 and passes at z = 0",
             f"max |ratio/pred - 1| = {k2p:.4f}; committed line, L362, max |ratio - 1|: " + ", ".join(f"{k} {v:.3f}" for k, v in bug.items()),
             k2p <= TOL and fails_hi and pass_lo,
             "the committed MOND term is too weak by the predicted factor: kick 33-43% low at r = 8-16 cells on this halo")

    # ============================================================================================== S1 census
    LN.banner("S1  THE CENSUS: which record scripts carry the pattern (regex over real_research/ and fable_independent_2026/)")
    pat = re.compile(r"gg\s*/\s*a\s*\*\*\s*2")
    hits = []
    for root in ("real_research", "fable_independent_2026"):
        for py in sorted(glob.glob(os.path.join(X.REPO, root, "**", "*.py"), recursive=True)):
            if os.path.basename(py).startswith("XR34_"):
                continue
            try:
                for i, line in enumerate(open(py, errors="ignore")):
                    if pat.search(line):
                        hits.append((X.rel(py), i + 1, line.strip()))
            except OSError:
                pass
    for h in hits:
        P(f"    {h[0]}:{h[1]}   {h[2]}")
    census = {
        "forest lanes, own kernel line (re-scored by XR34)": ["L346 (matter power in the forest band)", "L347", "L362",
                                                             "DE11", "DE11b", "L359 (its forest runs F1)"],
        "forest lane that runs L347's run() (inherits the line)": ["L358 (pool.map(L7.run, ...))"],
        "not forest: matter power / lensing, same line (flagged, not re-scored)": ["fable_independent_2026/L176 (docstring: "
                                                                                  "'g_N = -grad phi_N / a^2 (physical)')",
                                                                                  "L178", "L179"],
        "correct argument (1/a) -- not affected": ["L377 (and L379/L388 through it)", "L393", "L394", "L395", "L396",
                                                   "XR21_pm_core"],
        "PM with no MOND kernel -- not affected": ["L365", "L366", "AT2"],
        "downstream readers of the affected forest numbers": ["DE2 (L358/L347 constant-threshold table; L359's (0.5, 1.5) "
                                                              "dominance anchor)", "L360 (L359's window W1)",
                                                              "L352 Z7 (L346's F2)", "PAPER34 (P34_paper_numbers: L358, L362, "
                                                                                     "L359's forest numbers)"],
    }
    for k, v in census.items():
        P(f"    {k}: {', '.join(v)}")
    l358 = open(os.path.join(X.G03, "L358_forest_kids_pincer_observable.py")).read()
    LN.out["numbers"]["S1"] = dict(hits=hits, census=census, L358_runs_L347=("L7.run" in l358))
    files = sorted({h[0] for h in hits})
    LN.check("S1 (reported) the pattern's census", f"{len(hits)} lines in {len(files)} files: {', '.join(os.path.basename(f) for f in files)}; "
             f"L358 calls L347's run(): {'L7.run' in l358}", True, load_bearing=False)

    LN.banner("VERDICT")
    if MUTATE:
        P(f"""  MUTATE: with the correction applied twice (argument g_N,phys/(1+z)) the halo kick misses nu g_N by up to {k1:.0%}:
  K1 fails, as it must.  B0, B1 and K2 do not depend on which line is called 'corrected'.""")
        sys.exit(LN.finish())
    P(f"""  The bug is real.  In all six code variants the Poisson line makes phi_N the physical peculiar potential, and each
  lane's own Newtonian kick / a is Newton's G M/r^2 in SI to {b0:.1%} (B0); the LCDM run grows its largest modes at the linear
  rate (B1).  The kernel reads |grad phi_N|/a^2 = (1+z) g_N,phys.  On an analytic halo the committed line's QUMOND kick is
  33-43% low at z = 2-3 (exactly nu((1+z) y)/nu(y), K2) and right at z = 0; the corrected line, |grad_x phi_N|/(a a0),
  is right at every z to {k1:.1%} ('{FIX}', K1).
  Affected: L346, L347, L359, L362, DE11, DE11b (own line), L358 (through L347's run()); and, outside the forest,
  fable_independent_2026's L176/L178/L179 (matter power and lensing; flagged, not re-scored here).""")
    sys.exit(LN.finish())
