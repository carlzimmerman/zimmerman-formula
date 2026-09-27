#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR22_force_law -- THE CHAIN'S LAW FOR A WIDE BINARY IN THE GALAXY'S FIELD, SOLVED IN 3-D: the relative-force boost of a pair of
stars under the derivation chain's z = 0 static law, across the heat filter's allowed window, both a0 footings.

WHY.  The chain's root (FP7, the AQUAL-type repair, committed 17a90e572) carries a heat filter of length xi on the MOND scalar,
applied to the source and to the output (FP7 A1b: forced).  The Solar System needs xi >= 0.0243 / 0.0268 pc (FP7 A4, AQUAL
floors; the Saturn monopole binds), and FP14/FP17 leave xi as the gravity core's one knob, bounded to about [floor, ~100 pc].
A wide binary at 1-30 kAU straddles that length (5 kAU = 0.024 pc), so the chain's wide-binary prediction is set by xi.  The
frozen Gaia DR4 pre-registration (prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md, read-only) registers Arm A (Route A,
one-field AQUAL, no filter: canonical 1.1614-1.1814) and Arm B (the carrier reading with the biharmonic cone, xi >= 4 pc:
1.0000 +- 0.0025).  The chain is neither.  This lane computes its force law; XR22_prereg_statistic.py turns it into the
pre-registered statistic.

THE LAW (FP7 R7d; FP14: lambda = 0, c_2 -> oo, alpha_c <= 3.2e-9 a regulator; FP13's separator reduced to z = 0):
    g = g_N + S grad(phi),   div[mu_s(|grad phi|/a0) grad phi] = 4 pi G S rho,   mu_s(x) = x/(1 - 2x)  (J_P2),  S = e^{xi^2 Lap/2}
  with the Galaxy as the scalar's uniform background gradient x_e (mu_s(x_e) x_e = eta, eta the Newtonian Galactic field, P2
  inversion of the observed field).  FP13's band-pass leg S_L (L(z = 0) = 2.88 Mpc) and yield floor (y_th = 0 today: the switch is
  max(0, 2q) and q < 0) drop out locally (K0).  Two point stars, the relative acceleration along the separation, compared with
  G M_tot/s^2: the radial force boost B(M_tot, s, theta; xi) (theta = the angle between the separation and the Galactic field).

METHOD.  (i) the exact LINEAR response of the double-filtered anisotropic operator (Schwinger integral, XR22_common.lin_kernel);
(ii) the full NONLINEAR problem on a periodic box: pseudo-spectral, Newton on the convex energy with preconditioned CG, a
barrier-aware line search, the periodic images removed by the linear image correction; (iii) an independent axisymmetric
free-space P1-FEM Newton solver for the parallel orientation and for the isolated deep-MOND control.

PRE-DECLARED HYPOTHESES (written before the first full run; one exploratory prototype of the solver at a single point -- M = 1,
s = 1 r_M, xi = 0.63 r_M, parallel: B = 1.0169 nonlinear vs 1.0184 linear -- and a linear-kernel preview of the orientation
average informed H1, H2, H3 and H5; that is disclosed):
  H1  SUPPRESSION: at the canonical floor the orientation-averaged boost (B - 1) at s = 3 kAU is below 5% of the unfiltered
      EFE-saturated value, for M_tot = 1 and 2 Msun.  EXPECT TRUE.
  H2  TRANSITION AT s ~ xi: the separation where the orientation-averaged (B - 1) reaches half its unfiltered value lies in
      [1.5, 3] xi at the floor, and moves by < 15% between M_tot = 1 and 2 Msun (the linear response is mass-independent).
      EXPECT TRUE.
  H3  NONLINEARITY: the two-body nonlinear solve LOWERS the boost relative to the linear total-mass kernel, by less than 15% of
      (B_lin - 1), at the floors for every M_tot <= 2.5 Msun and s >= 3 kAU.  EXPECT TRUE.
  H4  MONOTONE IN xi: at every registered-grid point (M = 1, 2; s = 3-30 kAU; 0/45/90 deg) B decreases with xi.  EXPECT TRUE.
  H5  ANISOTROPY FLIP: at the canonical floor B(90 deg) > B(0 deg) at s <= 10 kAU and B(0 deg) > B(90 deg) at s >= 30 kAU (the
      filter suppresses the parallel direction more, the unfiltered tensor is parallel-dominant).  EXPECT TRUE.
  H6  NEWTONIAN LIMIT: for xi >= 1 pc, |B - 1| < 1e-3 at every s <= 30 kAU.  EXPECT TRUE.
  H7  FIELD SENSITIVITY: the chain's own Galactic field (2.32e-10, FP7) lowers the canonical-floor orientation-averaged (B - 1) at
      30 kAU by more than 20% relative to the pre-registration's primary 1.778e-10.  EXPECT TRUE.
  (The hypotheses are REPORTED checks: they fall as they fall and are kept as run.  Disclosure: before the first full run a
  development dry run -- XR22_DRYRUN=1, the linear kernel standing in for every nonlinear solve, outputs outside the repository --
  exercised the bookkeeping and showed that H4 fails for the perpendicular orientation at 20-30 kAU (the filtered kernel's
  in-plane overshoot).  H4 is kept exactly as declared; H4b, on the orientation average, was added after that dry run and is
  labelled as such.)
"""
DOC_CHECKS = r"""
CHECKS
  K0  the chain's inputs (committed JSONs, read-only) and the local reduction: FP0 a0 footings, FP7 AQUAL floors, FP13's
      L(z = 0) and y_th(0) = 0, FP14's xi window and alpha_c, the quasi-static limit (reported numbers).
  K1  CONTROL: the frozen section 1.1 numbers from the frozen pipeline's own function -- y_extN = 1.4647 / 1.1513 (P2 inversion
      of 1.778e-10 at 9.36e-11 / 1.13e-10) -- and the banked MG asymptote 1.1389 = sqrt(B_par) of the chain's UNFILTERED law
      (xi -> 0): the frozen record's 'AQUAL-EFE point-field, framework nu' number IS this law's parallel eigenvalue; FP7's
      committed stiffnesses at 2.32e-10 (x_e = 0.4501, mu_T = 4.507, mu_L = 49.64).
  K2  CONTROL: the linear kernel at xi = 0 equals the analytic anisotropic-Coulomb tensor (all angles, three separations,
      1e-7) and, at xi > 0, direct scipy quadrature (1e-7); the orientation average's closed form.
  K3  CONTROL (deep-MOND two-body): the independent 2-D solver with mu = x reproduces Milgrom's exact two-body force
      s F = (2/3)[M^1.5 - m1^1.5 - m2^1.5] for isolated Gaussian bodies: |ratio - 1| < 0.5% at xi/s = 0.05 (q = 1 and 0.3),
      < 0.25% at 0.025, and < 0.1% after Richardson in (xi/s)^2.
  K4  CONTROL (external-field-dominated linear regime): the 3-D solver's periodic LINEAR response, extrapolated in the box size
      (L^-3), equals the double-filtered free-space kernel (|dB| < max(5e-5, 0.5% of B - 1)), at two configurations.
  K5  CONTROL (nonlinear, independent method): 3-D periodic (image-corrected, margin 13.5 r_M) vs 2-D free-space FEM (Richardson in
      h^2) for the parallel orientation at the floors: |dB| < max(1e-4, 5% of the nonlinear correction), four configurations.
  K6  CONVERGENCE of the production settings (h = xi/2.5, margin 9 r_M): h -> xi/3.5 and margin -> 13.5 r_M at the worst cases;
      max |dB| < 3e-4 (the registered estimator's gamma grid step is 2.5e-3); momentum conservation over the production.
  K7  symmetry theta -> 180 - theta (equal masses); the mass-ratio sensitivity (q = 0.3 vs 1) [reported]; the angular
      interpolation used downstream (nonlinear correction quadratic in cos^2 theta through 0/45/90) against direct solves at
      22.5 and 67.5 deg: |dB| < 5e-4.
  K8  the PLUG-IN interface: a constant screening term c x^3/3 through the plug-in equals the equivalent law built directly
      (1e-8); a matter-keyed term conserves momentum only with its key force (reported).
  P   PRODUCTION: nonlinear tables B(M_tot in {0.6, 1, 1.5, 2, 2.5}, s in 1.5-120 kAU, theta in {0, 45, 90}) at xi in {floor, 0.03,
      0.04, 0.05, 0.07, 0.1, 0.15, 0.2} pc, both footings, the pre-registration's primary Galactic field 1.778e-10; the
      registered grid (M = 1, 2; s = 3-30 kAU) at the pre-registration's alt field 2.078e-10 (xi = floor, 0.03, 0.05, 0.1) and at
      the chain's 2.32e-10 (floor); the exact linear kernel at xi = 0 and 0.3-100 pc, with the nonlinear correction bounded at
      0.2 pc.
  H1-H7  the hypotheses above.   W  the ledger.
XR22_DRYRUN=1 (development only; needs XR22_SCRATCH outside the repository) replaces the solves by the linear kernel to test the
bookkeeping.  MUTATE=1 drops the OUTPUT leg of the double filter in the 3-D solver (a single filter on the source only; FP7 A1b says the
double filter is forced): K4 (3-D linear response vs the chain's double-filter kernel) and K5 (3-D vs the independent 2-D
solver, which keeps the double filter) must FAIL (rc = 1).  Under MUTATE the production (P) and H1-H7 are not run (they need
the main-run tables); the MUTATE run writes only _MUTATE files.

SCOPE.  Static weak-field limit; point stars (the filter is the chain's, not a stellar size); equal-mass tables (the mass-ratio
effect is measured in K7); quasi-static (K0); the Galactic field uniform over the pair (its tide is 1e-5 of the pair's own
field at 30 kAU) and taken as the pre-registration's frozen values.  The mapping to gamma_v is XR22_prereg_statistic.py.
At most 4 worker processes, one thread each.  Run from the repository root:
    MUTATE=1 python3 real_research/cross_thread_review_2026_09_26/XR22_force_law.py     (first)
    python3 real_research/cross_thread_review_2026_09_26/XR22_force_law.py               (last)
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
sys.dont_write_bytecode = True
import io, json, math, time, warnings
warnings.filterwarnings("ignore")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import XR22_common as C

MUTATE = os.environ.get("MUTATE", "0") == "1"
QUICK = os.environ.get("XR22_DRYRUN", "0") == "1"         # development only: solves replaced by the linear kernel, outputs to XR22_SCRATCH
SLUG = "XR22_force_law"
NPROC = int(os.environ.get("XR22_NPROC", "4"))             # worker processes, one thread each (the lane budget is 4 threads in total)
if QUICK and not os.environ.get("XR22_SCRATCH"):
    sys.exit("XR22_DRYRUN needs XR22_SCRATCH (a directory outside the repository) for its outputs")
_ODIR = os.environ["XR22_SCRATCH"] if QUICK else HERE
OUTF = os.path.join(_ODIR, SLUG + ("_MUTATE" if MUTATE else "") + ("_QUICK" if QUICK else "") + ".out")
JSN = os.path.join(_ODIR, SLUG + "_results" + ("_MUTATE" if MUTATE else "") + ("_QUICK" if QUICK else "") + ".json")
GEXT = {"prereg_primary": 1.9 * 9.36e-11, "prereg_alt": 2.078e-10, "chain_FP7": 2.32e-10}
S_EXT = [1.5, 2.0, 3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0, 45.0, 60.0, 90.0, 120.0]
S_REG = [3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0]
M_EXT = [0.6, 1.0, 1.5, 2.0, 2.5]
M_REG = [1.0, 2.0]
TH3 = [0.0, 45.0, 90.0]
TH_FINE = [0.0, 7.5, 15.0, 22.5, 30.0, 37.5, 45.0, 52.5, 60.0, 67.5, 75.0, 82.5, 90.0]
XI_3D_ABOVE = [0.03, 0.04, 0.05, 0.07, 0.1, 0.15, 0.2]
XI_LIN = [0.3, 0.5, 1.0, 2.0, 3.0, 10.0, 30.0, 100.0]


def _dry_task(task):
    """DRY RUN stand-in (development only): the linear kernel in place of the nonlinear solve -- exercises the bookkeeping"""
    a0, M = task["a0"], task["M"]
    rM = math.sqrt(C.GM_SUN * M / a0)
    xi, s = task["xi_pc"] * C.PC_M / rM, task["s_kAU"] * C.KAU_M / rM
    eta = C.eta_of_gobs(task["gext"] / a0)
    xe, muT, muL = C.LAW_P2.stiffness(eta)
    b, tn, _ = C.lin_boost(s, math.radians(task["theta_deg"]), xi, muT, muL)
    out = dict(task)
    out.update(B=b - 1e-9 * (b - 1), B_tan=tn, B_lin_free=b, B_lin_per=b, B_nl_per=b, newton=1, res=1e-12, momentum=1e-12, N=31, L=10.0,
               h=0.3, ok=True, error="", time=0.0, xi_rM=xi, s_rM=s, eta=eta, cg_total=0, xrange=(0.4, 0.46))
    return out


class Tee:
    def __init__(self, path):
        self.f = open(path, "w")

    def write(self, s):
        sys.__stdout__.write(s)
        self.f.write(s)

    def flush(self):
        sys.__stdout__.flush()
        self.f.flush()


OUT = {"lane": "XR22_force_law", "mutate": MUTATE, "checks": {}, "numbers": {}, "tables": {}, "lin_tables": {}, "ledger": []}
CH = []


def P_(*a):
    print(*a, flush=True)


def banner(t):
    P_("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P_(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")
    if reading:
        P_(f"         reading:  {reading}")
    return ok


def run_pool(tasks, label):
    """run physical-unit tasks on NPROC single-threaded workers, largest boxes first; returns results in task order"""
    import multiprocessing as mp
    t0 = time.time()
    order = sorted(range(len(tasks)), key=lambda i: -_cost(tasks[i]))
    ctx = mp.get_context("spawn")
    res = [None] * len(tasks)
    if QUICK:
        for k in order:
            res[k] = _dry_task(tasks[k])
    else:
        with ctx.Pool(NPROC, maxtasksperchild=40) as pool:
            for k, r in zip(order, pool.imap(C.phys_task, [tasks[i] for i in order], chunksize=1)):
                res[k] = r
    bad = [r for r in res if not r.get("ok", False)]
    P_(f"    [{label}] {len(tasks)} solves in {time.time() - t0:.0f} s wall; not converged / errors: {len(bad)}"
       + (f" -> {[(b['M'], b['s_kAU'], b['theta_deg'], b['xi_pc'], b.get('error', ''), b.get('res')) for b in bad[:5]]}" if bad else ""))
    return res


def _cost(t):
    a0, M = t["a0"], t["M"]
    rM = math.sqrt(C.GM_SUN * M / a0)
    xi = t["xi_pc"] * C.PC_M / rM
    s = t["s_kAU"] * C.KAU_M / rM
    if t.get("kind", "3d") == "2d":
        return 1e5
    N, L = C.box_for(s, xi, hfac=t.get("hfac", 2.5), margin=t.get("margin", 9.0), nmax=t.get("nmax", 231))
    return N ** 3 * math.log(N)


def key(M, s, th):
    return f"{float(M)}|{float(s)}|{float(th)}"


def main():
    sys.stdout = Tee(OUTF)
    T_START = time.time()
    P_(__doc__.split("PRE-DECLARED")[0].strip())
    if MUTATE:
        P_("\n  *** MUTATE=1: the OUTPUT leg of the double filter is dropped in the 3-D solver (source filter only): K4 and K5 must FAIL ***")
    CI = C.chain_inputs()
    A0 = CI["a0"]
    FLOOR = CI["xi_floor_pc"]
    OF = not MUTATE                                      # output_filter flag of the 3-D solver

    # ======================================================================================== K0 inputs and the local reduction
    banner("K0  THE CHAIN'S INPUTS AND ITS LOCAL (z = 0, wide-binary) REDUCTION")
    L0 = CI["L0_kpc"] * C.KPC_M
    s30 = 30 * C.KAU_M
    bp_leak = (s30 / L0) ** 3                                    # S_L leg: the band-pass's Mpc leg smooths the pair's own field away
    kid = C.eta_of_gobs(GEXT["prereg_primary"] / A0["canonical"])
    xe_c, muT_c, muL_c = C.LAW_P2.stiffness(kid)
    cs_over_c = math.sqrt(muT_c / 3.0)                           # FP7 R7n: c_s^2 = C_phi/lambda_eff, lambda_eff -> 3 at lambda = 0, c_2 -> oo
    v_orb = math.sqrt(C.GM_SUN * 2.0 / (30 * C.KAU_M))
    P_(f"    a0 = {A0['canonical']:.5e} / {A0['alt']:.5e} m/s^2 (FP0); xi floors {FLOOR['canonical']:.5f} / {FLOOR['alt']:.5f} pc (FP7 A4 AQUAL, "
       f"binding {CI['xi_floor_binding']['canonical']}); QUMOND floors {CI['xi_qumond_pc']['canonical']:.4f} / {CI['xi_qumond_pc']['alt']:.4f} pc")
    P_(f"    FP14 F14p: {CI['F14p']}")
    P_(f"    FP13 H1: L(z = 0) = {CI['L0_kpc']:.0f} kpc, y_th(z = 0) = {CI['yth0']} (the yield's switch max(0, 2q) is off while the leaf "
       f"accelerates); the band-pass's Mpc leg moves the pair's relative force by ~(s/L)^3 = {bp_leak:.1e} at 30 kAU")
    P_(f"    FP14 F14d: {CI['F14d']}")
    P_(f"    quasi-static: the scalar's signal speed c_s = c sqrt(C_phi/lambda_eff) ~ {cs_over_c:.2f} c (lambda_eff = 3 at lambda = 0, c_2 -> oo, "
       f"C_phi ~ mu_T = {muT_c:.2f}); a 2-Msun pair at 30 kAU orbits at {v_orb / 1e3:.2f} km/s: retardation ~ v/c_s = {v_orb / (cs_over_c * C.C_SI):.1e}")
    OUT["numbers"]["K0"] = dict(a0=A0, floors=FLOOR, L0_kpc=CI["L0_kpc"], yth0=CI["yth0"], bandpass_leak_30kAU=bp_leak,
                                cs_over_c=cs_over_c, retardation=v_orb / (cs_over_c * C.C_SI))
    check("K0 THE LOCAL REDUCTION: at z = 0 the chain's separator adds nothing on wide-binary scales (FP13: y_th(0) = 0; the band-pass's "
          "Mpc leg changes the pair's relative force by < 1e-12), alpha_c renormalises G by <= 1.6e-9 (FP14), and the pair is "
          "quasi-static (retardation < 1e-5): the law is FP7's double-filtered two-field AQUAL with J_P2",
          f"y_th(0) = {CI['yth0']}; band-pass leak {bp_leak:.1e}; retardation {v_orb / (cs_over_c * C.C_SI):.1e}",
          CI["yth0"] == 0.0 and bp_leak < 1e-12 and v_orb / (cs_over_c * C.C_SI) < 1e-5 and FLOOR["canonical"] > 0.02)

    # ======================================================================================== K1 frozen section 1.1 numbers
    banner("K1  CONTROL: THE FROZEN SECTION 1.1 NUMBERS AND FP7'S STIFFNESSES FROM THIS LANE'S LAW")
    PL = C.load_pipeline()
    yE = {f: float(PL["y_extN"](PL[k])) for f, k in (("canonical", "A0_CAN"), ("alt", "A0_ALT"))}
    xe_p, muT_p, muL_p = C.LAW_P2.stiffness(yE["canonical"])
    Bpar_p = 1 + 1 / muT_p
    nu_p2 = math.sqrt(1 + 1 / yE["canonical"])
    xe7, muT7, muL7 = C.LAW_P2.stiffness(C.eta_of_gobs(2.32e-10 / A0["canonical"]))
    P_(f"    frozen pipeline y_extN(A0_CAN) = {yE['canonical']:.4f}, y_extN(A0_ALT) = {yE['alt']:.4f} (section 1.1: 1.4647 / 1.1513)")
    P_(f"    the chain's unfiltered law at that field: x_e = {xe_p:.5f}, mu_T = {muT_p:.4f}, mu_L = {muL_p:.4f}; B_par = 1 + 1/mu_T = {Bpar_p:.6f} "
       f"= nu_P2(y_extN) = {nu_p2:.6f}; sqrt = {math.sqrt(Bpar_p):.5f} (the banked 'framework-as-MG' asymptote 1.1389); "
       f"B_perp = 1 + 1/sqrt(mu_T mu_L) = {1 + 1 / math.sqrt(muT_p * muL_p):.5f}")
    P_(f"    FP7 A4 at 2.32e-10 (canonical): x_e = {xe7:.4f}, mu_T = {muT7:.3f}, mu_L = {muL7:.2f} (committed 0.4501, 4.507, 49.64)")
    OUT["numbers"]["K1"] = dict(y_extN=yE, Bpar=Bpar_p, sqrtBpar=math.sqrt(Bpar_p), Bperp=1 + 1 / math.sqrt(muT_p * muL_p),
                                fp7=dict(xe=xe7, muT=muT7, muL=muL7))
    check("K1 CONTROL: the frozen pipeline's own y_extN reproduces section 1.1 (1.4647 / 1.1513); the banked MG asymptote 1.1389 is "
          "sqrt(B_par) of the chain's unfiltered two-field law (B_par = 1 + 1/mu_T = nu_P2(y_extN) identically); FP7's committed "
          "stiffnesses at 2.32e-10 reproduced to the printed digits",
          f"y_extN {yE['canonical']:.4f}/{yE['alt']:.4f}; sqrt(B_par) {math.sqrt(Bpar_p):.5f}; B_par - nu {Bpar_p - nu_p2:.1e}; FP7 {xe7:.4f}/{muT7:.3f}/{muL7:.2f}",
          abs(yE["canonical"] - 1.4647) < 5e-5 and abs(yE["alt"] - 1.1513) < 5e-5 and abs(math.sqrt(Bpar_p) - 1.1389) < 5e-5
          and abs(Bpar_p - nu_p2) < 1e-12 and abs(xe7 - 0.4501) < 5e-5 and abs(muT7 - 4.507) < 5e-4 and abs(muL7 - 49.64) < 5e-3,
          "so the pre-registration's own P2 number is the xi -> 0 limit of this lane's law, parallel direction only (the "
          "perpendicular eigenvalue is far smaller, and Amendment 10 showed the isotropic reading overstates)")

    # ======================================================================================== K2 the linear kernel
    banner("K2  CONTROL: THE EXACT LINEAR KERNEL (Schwinger integral) against the analytic tensor and direct quadrature")
    from scipy.integrate import quad
    errs = []
    for s_ in (0.5, 3.0, 20.0):
        for thd in (0.0, 30.0, 45.0, 60.0, 90.0):
            B_k = C.lin_boost(s_, math.radians(thd), 0.0, muT_c, muL_c)[0]
            B_a = C.analytic_tensor(math.radians(thd), muT_c, muL_c)
            errs.append(abs(B_k - B_a) / (B_a - 1))
    qerr = []
    for (x_, z_, xi_) in ((0.3, 0.8, 0.6), (1.5, 0.2, 0.4), (0.1, 2.5, 1.3)):
        g_k = C.lin_kernel_grad(np.array([[x_, 0.0, z_]]), xi_, muT_c, muL_c)[0]
        f_ = lambda t, comp: (4 * np.pi) ** -0.5 / ((xi_ ** 2 + t * muT_c) * math.sqrt(xi_ ** 2 + t * muL_c)) * math.exp(
            -x_ ** 2 / (4 * (xi_ ** 2 + t * muT_c)) - z_ ** 2 / (4 * (xi_ ** 2 + t * muL_c))) * (
            x_ / (2 * (xi_ ** 2 + t * muT_c)) if comp == 0 else z_ / (2 * (xi_ ** 2 + t * muL_c)))
        gq = [quad(lambda t: f_(t, 0), 0, np.inf, epsabs=0, epsrel=1e-12, limit=400)[0], quad(lambda t: f_(t, 1), 0, np.inf, epsabs=0, epsrel=1e-12, limit=400)[0]]
        qerr.append(max(abs(g_k[0] - gq[0]) / abs(gq[0]), abs(g_k[2] - gq[1]) / abs(gq[1])))
    us = np.linspace(0, 1, 200001)
    avg_num = np.trapz([C.analytic_tensor(math.acos(u), muT_c, muL_c) for u in us[::100]], us[::100])
    avg_cf = C.orient_avg_exact(muT_c, muL_c)
    P_(f"    xi = 0: max |B_kernel - B_analytic|/(B - 1) over 3 separations x 5 angles = {max(errs):.1e};  xi > 0 vs scipy.quad: max rel "
       f"{max(qerr):.1e};  orientation average (closed form) {avg_cf:.6f} vs quadrature {avg_num:.6f}")
    OUT["numbers"]["K2"] = dict(tensor_err=max(errs), quad_err=max(qerr), orient_avg=avg_cf)
    check("K2 CONTROL: the linear kernel reproduces the analytic anisotropic-Coulomb tensor at xi = 0 and direct quadrature at xi > 0 "
          "to 1e-7; the closed-form orientation average matches quadrature", f"{max(errs):.1e}; {max(qerr):.1e}; {abs(avg_cf - avg_num):.1e}",
          max(errs) < 1e-7 and max(qerr) < 1e-7 and abs(avg_cf - avg_num) < 1e-6)

    # ======================================================================================== K3 deep-MOND two-body (2-D)
    banner("K3  CONTROL: THE ISOLATED DEEP-MOND TWO-BODY FORCE (independent 2-D FEM solver, mu = x) vs Milgrom's exact virial result")
    tk3 = time.time()
    d05 = C.solve2d_deep_pair(0.05, q=1.0)
    d025 = C.solve2d_deep_pair(0.025, q=1.0)
    d05q = C.solve2d_deep_pair(0.05, q=0.3)
    rich = (4 * d025["ratio"] - d05["ratio"]) / 3
    for lab, d_ in (("xi/s = 0.05, q = 1", d05), ("xi/s = 0.025, q = 1", d025), ("xi/s = 0.05, q = 0.3", d05q)):
        P_(f"    {lab}: s F = {d_['virial']:.6f} vs (2/3)[M^1.5 - m1^1.5 - m2^1.5] = {d_['pred']:.6f}: ratio {d_['ratio']:.5f} "
           f"({d_['nodes']} nodes, {d_['newton']} Newton steps, |F1 + F2|/|F2| = {d_['momentum']:.1e})")
    P_(f"    Richardson in (xi/s)^2: ratio -> {rich:.5f}   ({time.time() - tk3:.0f} s)")
    OUT["numbers"]["K3"] = dict(r05=d05["ratio"], r025=d025["ratio"], r05q=d05q["ratio"], richardson=rich)
    check("K3 CONTROL (deep-MOND two-body): the independent 2-D solver reproduces Milgrom's exact two-body force within 0.5% at xi/s = 0.05 "
          "(q = 1 and 0.3), 0.25% at 0.025, 0.1% after Richardson",
          f"{d05['ratio']:.5f}, {d05q['ratio']:.5f}, {d025['ratio']:.5f}; Richardson {rich:.5f}",
          abs(d05["ratio"] - 1) < 5e-3 and abs(d05q["ratio"] - 1) < 5e-3 and abs(d025["ratio"] - 1) < 2.5e-3 and abs(rich - 1) < 1e-3,
          "the residual shrinks as (xi/s)^2: the finite size of the smoothed bodies, not the solver")

    # ======================================================================================== K4 3-D linear response vs the kernel
    banner("K4  CONTROL: THE 3-D SOLVER'S LINEAR RESPONSE, EXTRAPOLATED IN THE BOX SIZE, vs THE DOUBLE-FILTERED KERNEL" + ("  [MUTATE]" if MUTATE else ""))
    K4 = []
    for foot, M, skau, thd in (("canonical", 1.0, 10.0, 45.0), ("alt", 2.0, 20.0, 90.0)):
        a0 = A0[foot]
        rM = math.sqrt(C.GM_SUN * M / a0)
        xi = FLOOR[foot] * C.PC_M / rM
        s_ = skau * C.KAU_M / rM
        eta = C.eta_of_gobs(GEXT["prereg_primary"] / a0)
        xe_, muT_, muL_ = C.LAW_P2.stiffness(eta)
        Bs, Ls = [], []
        for mg in (9.0, 13.5, 18.0):
            N, L = C.box_for(s_, xi, margin=mg, nmax=231)
            o = C.solve3d(C.LAW_P2, C.HeatFilter(xi), eta, C.pair_bodies(s_, math.radians(thd)), N, L, output_filter=OF, linear_only=True)
            Bs.append(o["B_lin_per"])
            Ls.append(L)
        A = np.vstack([np.ones(3), np.array(Ls) ** -3.0]).T
        Binf = float(np.linalg.lstsq(A, np.array(Bs), rcond=None)[0][0])
        Bk = C.lin_boost(s_, math.radians(thd), xi, muT_, muL_)[0]
        tol = max(5e-5, 5e-3 * (Bk - 1))
        K4.append(dict(foot=foot, M=M, s=skau, th=thd, B_L=Bs, L=Ls, Binf=Binf, kernel=Bk, ok=abs(Binf - Bk) < tol))
        P_(f"    {foot} M = {M} s = {skau} kAU theta = {thd}: periodic linear B at L = {', '.join(f'{l_:.1f}' for l_ in Ls)} r_M: "
           f"{', '.join(f'{b_:.6f}' for b_ in Bs)} -> L^-3 extrapolation {Binf:.6f}; double-filter kernel {Bk:.6f} (|d| = {abs(Binf - Bk):.1e}, tol {tol:.1e})")
    OUT["numbers"]["K4"] = K4
    check("K4 CONTROL (linear regime): the 3-D solver's periodic linear response extrapolates (L^-3) to the chain's double-filtered "
          "free-space kernel at both configurations", "; ".join(f"{k_['foot']} {k_['Binf']:.6f} vs {k_['kernel']:.6f}" for k_ in K4),
          all(k_["ok"] for k_ in K4))

    # ======================================================================================== K5 3-D vs 2-D (nonlinear)
    banner("K5  CONTROL: 3-D PERIODIC NONLINEAR vs 2-D FREE-SPACE FEM, separation parallel to the Galactic field" + ("  [MUTATE]" if MUTATE else ""))
    tk5 = time.time()
    K5 = []
    for foot, M, skau in (("canonical", 1.0, 5.0), ("canonical", 1.0, 10.0), ("canonical", 2.5, 15.0), ("alt", 2.0, 10.0)):
        a0 = A0[foot]
        base = dict(a0=a0, gext=GEXT["prereg_primary"], xi_pc=FLOOR[foot], M=M, s_kAU=skau, theta_deg=0.0, q=1.0, output_filter=OF)
        t3 = C.phys_task(dict(base, kind="3d", margin=13.5))
        t2a = C.phys_task(dict(base, kind="2d", hfac2d=6.0))
        t2b = C.phys_task(dict(base, kind="2d", hfac2d=9.0))
        B2 = t2b["B"] + (t2b["B"] - t2a["B"]) / ((9.0 / 6.0) ** 2 - 1)
        nlc = abs(t3["B_lin_free"] - B2)
        tol = max(1e-4, 0.05 * nlc)
        K5.append(dict(foot=foot, M=M, s=skau, B3=t3["B"], B2a=t2a["B"], B2b=t2b["B"], B2R=B2, Blin=t3["B_lin_free"], ok=abs(t3["B"] - B2) < tol))
        P_(f"    {foot} M = {M} s = {skau} kAU (xi/r_M = {t3['xi_rM']:.3f}, s/r_M = {t3['s_rM']:.3f}): 3-D {t3['B']:.6f} (N = {t3['N']}, {t3['newton']} Newton, "
           f"momentum {t3['momentum']:.0e}); 2-D {t2a['B']:.6f} (h = xi/6) / {t2b['B']:.6f} (xi/9) -> {B2:.6f}; linear kernel {t3['B_lin_free']:.6f}; "
           f"|3D - 2D| = {abs(t3['B'] - B2):.1e} (tol {tol:.1e})")
    OUT["numbers"]["K5"] = K5
    check("K5 CONTROL (nonlinear, independent method): the 3-D periodic solver and the 2-D free-space FEM agree at the floors for "
          "the parallel orientation", "; ".join(f"{k_['foot']} M{k_['M']} s{k_['s']}: {k_['B3']:.6f} vs {k_['B2R']:.6f}" for k_ in K5),
          all(k_["ok"] for k_ in K5), f"({time.time() - tk5:.0f} s)")

    if MUTATE:
        banner("MUTATE: production and hypotheses not run (they need the main-run tables)")
        return finish(T_START)

    # ======================================================================================== K8 plug-in interface
    banner("K8  THE PLUG-IN INTERFACE (a different screening term drops into the same solver)")
    eta = C.eta_of_gobs(1.9)
    c0 = 0.8
    lawA = C.with_extra(C.LAW_P2, lambda box, bodies: c0, c0, lambda x: x ** 3 / 3, lambda x: x ** 2, lambda x: 2 * x)
    lawB = C.Law("P2 + c x (direct)", lambda x: x / (1 - 2 * x) + c0 * x, lambda x: 1 / (1 - 2 * x) ** 2 + c0,
                 lambda x: -0.25 * x * x - 0.25 * x - 0.125 * np.log1p(-2 * x) + c0 * x ** 3 / 3, 0.5)
    bb = C.pair_bodies(1.0, math.radians(45))
    oA = C.solve3d(lawA, C.HeatFilter(0.5), eta, bb, 65, 16.0)
    oB = C.solve3d(lawB, C.HeatFilter(0.5), eta, bb, 65, 16.0)
    W_, C1 = 0.5, 5.0

    def bump(box, p):
        X = box.x[:, None, None] - p[0]
        Y = box.x[None, :, None] - p[1]
        Z = box.x[None, None, :] - p[2]
        return X, Y, Z, np.exp(-(X * X + Y * Y + Z * Z) / (2 * W_ * W_))

    def kf(box, bodies, Gx):
        out = []
        for m_, p_ in bodies:
            X, Y, Z, g_ = bump(box, p_)
            out.append(np.array([-(1 / (4 * np.pi)) * box.h ** 3 * np.sum(Gx * C1 * g_ * D / W_ ** 2) for D in (X, Y, Z)]))
        return out
    moms = {}
    for lab, kf_ in (("without key force", None), ("with key force", kf)):
        lawC = C.with_extra(C.LAW_P2, lambda box, bodies: C1 * sum(bump(box, p_)[3] for m_, p_ in bodies), 0.0,
                            lambda x: x ** 3 / 3, lambda x: x ** 2, lambda x: 2 * x, name="density-keyed", key_force=kf_)
        moms[lab] = C.solve3d(lawC, C.HeatFilter(0.5), eta, bb, 65, 16.0)["momentum"]
    P_(f"    constant term via the plug-in: B = {oA['B']:.10f}; the same law built directly: {oB['B']:.10f}")
    P_(f"    a matter-keyed term (c = 5 x the bodies' Gaussian profile): momentum |F1 + F2|/|F2| = {moms['without key force']:.2e} without "
       f"its key force, {moms['with key force']:.1e} with it")
    OUT["numbers"]["K8"] = dict(plugin=oA["B"], direct=oB["B"], momentum=moms)
    check("K8 THE PLUG-IN INTERFACE: a screening term passed through the plug-in reproduces the equivalent law built directly (1e-8)",
          f"|dB| = {abs(oA['B'] - oB['B']):.1e}", abs(oA["B"] - oB["B"]) < 1e-8)
    check("K8b (reported) a matter-keyed screening term needs its key force: the momentum diagnostic flags it without (O(1)) and "
          "passes with it", f"{moms['without key force']:.2e} vs {moms['with key force']:.1e}",
          moms["without key force"] > 1e-2 and moms["with key force"] < 1e-6, load_bearing=False)

    # ======================================================================================== P production
    banner("P  PRODUCTION: NONLINEAR FORCE TABLES (4 single-threaded workers)")
    tasks = []
    for foot in ("canonical", "alt"):
        for xi_pc in [FLOOR[foot]] + XI_3D_ABOVE:
            for M in M_EXT:
                for sk in S_EXT:
                    for th in TH3:
                        tasks.append(dict(tag=f"{foot}|prereg_primary|{xi_pc:.6g}", a0=A0[foot], gext=GEXT["prereg_primary"], xi_pc=xi_pc,
                                          M=M, s_kAU=sk, theta_deg=th, q=1.0, kind="3d", hfac=2.5, margin=9.0, output_filter=True))
        for xi_pc in [FLOOR[foot], 0.03, 0.05, 0.1]:
            for M in M_REG:
                for sk in S_REG:
                    for th in TH3:
                        tasks.append(dict(tag=f"{foot}|prereg_alt|{xi_pc:.6g}", a0=A0[foot], gext=GEXT["prereg_alt"], xi_pc=xi_pc,
                                          M=M, s_kAU=sk, theta_deg=th, q=1.0, kind="3d", hfac=2.5, margin=9.0, output_filter=True))
        for M in M_REG:
            for sk in S_REG:
                for th in TH3:
                    tasks.append(dict(tag=f"{foot}|chain_FP7|{FLOOR[foot]:.6g}", a0=A0[foot], gext=GEXT["chain_FP7"], xi_pc=FLOOR[foot],
                                      M=M, s_kAU=sk, theta_deg=th, q=1.0, kind="3d", hfac=2.5, margin=9.0, output_filter=True))
    # convergence (K6), symmetry, mass ratio and angular interpolation (K7) ride on the same pool
    extra = []
    for foot, M, sk, th in (("canonical", 2.5, 10.0, 45.0), ("canonical", 2.5, 30.0, 0.0), ("canonical", 1.0, 5.0, 90.0), ("alt", 2.5, 20.0, 45.0),
                            ("canonical", 0.6, 120.0, 45.0)):
        for lab, hf, mg in (("fine", 3.5, 9.0), ("big", 2.5, 13.5)):
            extra.append(dict(tag=f"K6|{lab}", a0=A0[foot], gext=GEXT["prereg_primary"], xi_pc=FLOOR[foot], M=M, s_kAU=sk, theta_deg=th, q=1.0,
                              kind="3d", hfac=hf, margin=mg, output_filter=True, foot=foot))
    extra.append(dict(tag="K7|sym", a0=A0["canonical"], gext=GEXT["prereg_primary"], xi_pc=FLOOR["canonical"], M=1.5, s_kAU=10.0, theta_deg=135.0,
                      q=1.0, kind="3d", hfac=2.5, margin=9.0, output_filter=True, foot="canonical"))
    for sk in (5.0, 10.0, 20.0):
        for th in (0.0, 90.0):
            for q in (0.3, 0.6):
                extra.append(dict(tag="K7|q", a0=A0["canonical"], gext=GEXT["prereg_primary"], xi_pc=FLOOR["canonical"], M=1.5, s_kAU=sk,
                                  theta_deg=th, q=q, kind="3d", hfac=2.5, margin=9.0, output_filter=True, foot="canonical"))
    for M in (1.0, 2.5):
        for sk in (7.0, 15.0, 30.0):
            for th in (22.5, 67.5):
                extra.append(dict(tag="K7|ang", a0=A0["canonical"], gext=GEXT["prereg_primary"], xi_pc=FLOOR["canonical"], M=M, s_kAU=sk,
                                  theta_deg=th, q=1.0, kind="3d", hfac=2.5, margin=9.0, output_filter=True, foot="canonical"))
    # the nonlinear-correction bound where the linear kernel takes over (0.3 pc)
    for foot in ("canonical", "alt"):
        for M in (1.0, 2.5):
            for sk in (30.0, 120.0):
                extra.append(dict(tag=f"bound|{foot}", a0=A0[foot], gext=GEXT["prereg_primary"], xi_pc=0.3, M=M, s_kAU=sk, theta_deg=45.0, q=1.0,
                                  kind="3d", hfac=2.5, margin=9.0, output_filter=True, foot=foot))
    P_(f"    {len(tasks)} production solves + {len(extra)} convergence / symmetry / mass-ratio / angle / bound solves on {NPROC} worker processes")
    tP = time.time()
    res = run_pool(tasks + extra, "production")
    RP, RX = res[:len(tasks)], res[len(tasks):]
    OUT["numbers"]["production_wall_s"] = time.time() - tP
    TAB = {}
    for r in RP:
        TAB.setdefault(r["tag"], {})[key(r["M"], r["s_kAU"], r["theta_deg"])] = {
            k_: r.get(k_) for k_ in ("B", "B_tan", "B_lin_free", "B_lin_per", "B_nl_per", "newton", "res", "momentum", "N", "L", "ok", "time", "xi_rM", "s_rM")}
    OUT["tables"] = TAB
    nbad = sum(1 for r in RP if not r.get("ok"))
    mom = max((r.get("momentum", 0) for r in RP if r.get("ok")), default=float("nan"))
    ncap = sum(1 for r in RP if r.get("N", 0) >= 231)
    P_(f"    production: {len(RP)} solves, {nbad} not converged; max momentum non-conservation {mom:.1e}; boxes at the size cap: {ncap}; "
       f"wall {time.time() - tP:.0f} s")

    # the exact linear kernel tables (all xi, fine angles), and xi = 0
    tl = time.time()
    LIN = {}
    for foot in ("canonical", "alt"):
        for gk, gv in GEXT.items():
            eta = C.eta_of_gobs(gv / A0[foot])
            xe_, muT_, muL_ = C.LAW_P2.stiffness(eta)
            for xi_pc in [0.0, FLOOR[foot]] + XI_3D_ABOVE + XI_LIN:
                tab = {}
                for sk in S_EXT:
                    for th in TH_FINE:
                        # the linear boost is mass-independent: evaluate in r_M(1 Msun) units
                        rM = math.sqrt(C.GM_SUN / A0[foot])
                        tab[f"{sk}|{th}"] = C.lin_boost(sk * C.KAU_M / rM, math.radians(th), xi_pc * C.PC_M / rM, muT_, muL_)[0]
                LIN[f"{foot}|{gk}|{xi_pc:.6g}"] = tab
            OUT["numbers"].setdefault("stiffness", {})[f"{foot}|{gk}"] = dict(eta=eta, xe=xe_, muT=muT_, muL=muL_,
                                                                             B_par=1 + 1 / muT_, B_perp=1 + 1 / math.sqrt(muT_ * muL_),
                                                                             orient_avg=C.orient_avg_exact(muT_, muL_))
    OUT["lin_tables"] = LIN
    P_(f"    linear-kernel tables: {len(LIN)} (footing x field x xi) x {len(S_EXT) * len(TH_FINE)} points  ({time.time() - tl:.0f} s)")

    # ======================================================================================== K6 convergence
    banner("K6  CONVERGENCE OF THE PRODUCTION SETTINGS (h = xi/2.5, margin 9 r_M)")
    dmax = 0.0
    rows = []
    for r in RX:
        if not r["tag"].startswith("K6"):
            continue
        base = TAB[f"{r['foot']}|prereg_primary|{FLOOR[r['foot']]:.6g}"][key(r["M"], r["s_kAU"], r["theta_deg"])]
        d_ = abs(r["B"] - base["B"])
        dmax = max(dmax, d_)
        rows.append((r["foot"], r["M"], r["s_kAU"], r["theta_deg"], r["tag"].split("|")[1], base["B"], r["B"], d_, base["N"], r["N"]))
        P_(f"    {r['foot']:9s} M {r['M']:.1f} s {r['s_kAU']:5.1f} th {r['theta_deg']:4.0f} [{r['tag'].split('|')[1]:4s}]: production {base['B']:.6f} (N {base['N']}) -> "
           f"{r['B']:.6f} (N {r['N']}): |dB| = {d_:.1e}")
    OUT["numbers"]["K6"] = dict(rows=rows, max_dB=dmax, momentum_max=mom, not_converged=nbad)
    check("K6 CONVERGENCE: refining h (xi/2.5 -> xi/3.5) or enlarging the box (margin 9 -> 13.5 r_M) moves the production boosts by < 3e-4 at the "
          "worst cases; every production solve converged (|R| < 1e-8) and conserves momentum to < 1e-6",
          f"max |dB| = {dmax:.1e}; not converged {nbad}; momentum {mom:.1e}", dmax < 3e-4 and nbad == 0 and mom < 1e-6,
          "3e-4 in B is 1.5e-4 in gamma_v, 17x below the registered estimator's grid step")

    # ======================================================================================== K7 symmetry, mass ratio, angles
    banner("K7  SYMMETRY, MASS RATIO AND THE ANGULAR INTERPOLATION")
    fl_tab = TAB[f"canonical|prereg_primary|{FLOOR['canonical']:.6g}"]
    rs = [r for r in RX if r["tag"] == "K7|sym"][0]
    b45 = fl_tab[key(1.5, 10.0, 45.0)]["B"]
    P_(f"    theta = 135 vs 45 deg (M 1.5, 10 kAU, equal masses): {rs['B']:.8f} vs {b45:.8f}")
    check("K7a SYMMETRY: equal masses give B(180 - theta) = B(theta)", f"|dB| = {abs(rs['B'] - b45):.1e}", abs(rs["B"] - b45) < 1e-6)
    qrows = []
    for r in RX:
        if r["tag"] != "K7|q":
            continue
        b1 = fl_tab[key(1.5, r["s_kAU"], r["theta_deg"])]["B"]
        qrows.append((r["s_kAU"], r["theta_deg"], r["q"], r["B"], b1, (r["B"] - b1) / max(b1 - 1, 1e-12)))
        P_(f"    q = {r['q']:.1f}, s {r['s_kAU']:4.0f} kAU, th {r['theta_deg']:3.0f}: B = {r['B']:.6f} vs equal masses {b1:.6f}  (relative to B - 1: {(r['B'] - b1) / max(b1 - 1, 1e-12):+.2%})")
    qmax = max(abs(x_[5]) for x_ in qrows)
    OUT["numbers"]["K7q"] = dict(rows=qrows, max_rel=qmax)
    check("K7b (reported) MASS RATIO: unequal pairs (q = 0.3, 0.6) at the floor differ from the equal-mass table by at most this fraction "
          "of (B - 1)", f"{qmax:.2%}", True, load_bearing=False)
    arows = []
    for r in RX:
        if r["tag"] != "K7|ang":
            continue
        M, sk, th = r["M"], r["s_kAU"], r["theta_deg"]
        B3 = np.array([fl_tab[key(M, sk, t_)]["B"] for t_ in TH3])
        L3 = np.array([fl_tab[key(M, sk, t_)]["B_lin_free"] for t_ in TH3])
        Bi = float(C.angular_interp(math.radians(th), B3, L3, r["B_lin_free"]))
        arows.append((M, sk, th, r["B"], Bi, abs(r["B"] - Bi)))
        P_(f"    M {M} s {sk:4.0f} th {th:4.1f}: direct {r['B']:.6f}, interpolated {Bi:.6f} (|d| {abs(r['B'] - Bi):.1e})")
    amax = max(x_[5] for x_ in arows)
    OUT["numbers"]["K7ang"] = dict(rows=arows, max_err=amax)
    check("K7c ANGULAR INTERPOLATION: the downstream scheme (exact linear angular shape x a nonlinear correction quadratic in cos^2) "
          "matches direct solves at 22.5 and 67.5 deg", f"max |dB| = {amax:.1e}", amax < 5e-4)
    brows = []
    for r in RX:
        if not r["tag"].startswith("bound"):
            continue
        brows.append((r["tag"].split("|")[1], r["M"], r["s_kAU"], r["B"], r["B_lin_free"], r["B"] - r["B_lin_free"]))
        P_(f"    xi = 0.3 pc bound [{r['tag'].split('|')[1]}] M {r['M']} s {r['s_kAU']}: nonlinear {r['B']:.7f} vs linear {r['B_lin_free']:.7f} (d = {r['B'] - r['B_lin_free']:+.1e})")
    bmax = max(abs(x_[5]) for x_ in brows)
    OUT["numbers"]["bound_0p3pc"] = dict(rows=brows, max_abs=bmax)
    check("K7d THE LINEAR KERNEL TAKES OVER: at xi = 0.3 pc the nonlinear correction is below 1e-4 in B (so the exact linear kernel is used "
          "for xi >= 0.3 pc)", f"max |B_NL - B_lin| = {bmax:.1e}", bmax < 1e-4)

    # ======================================================================================== the gamma_v(s) curves
    banner("THE CHAIN'S BOOST vs SEPARATION (primary Galactic field 1.778e-10; orientation average = 3-point rule / exact sphere average)")
    CURVES = {}
    for foot in ("canonical", "alt"):
        st = OUT["numbers"]["stiffness"][f"{foot}|prereg_primary"]
        P_(f"  [{foot}] unfiltered (xi -> 0): B_par {st['B_par']:.4f}, B_perp {st['B_perp']:.4f}, sphere average {st['orient_avg']:.4f} "
           f"(gamma_v = sqrt: {math.sqrt(st['orient_avg']):.4f})")
        for xi_pc in [FLOOR[foot]] + XI_3D_ABOVE:
            tg = TAB[f"{foot}|prereg_primary|{xi_pc:.6g}"]
            for M in (1.0, 2.0):
                gv = []
                for sk in S_EXT:
                    B3 = np.array([tg[key(M, sk, t_)]["B"] for t_ in TH3])
                    L3 = np.array([tg[key(M, sk, t_)]["B_lin_free"] for t_ in TH3])
                    lin_fine = np.array([LIN[f"{foot}|prereg_primary|{xi_pc:.6g}"][f"{sk}|{t_}"] for t_ in TH_FINE])
                    uu = np.cos(np.radians(TH_FINE))
                    Bf = C.angular_interp(np.radians(TH_FINE), B3[None, :].repeat(len(TH_FINE), 0), L3[None, :].repeat(len(TH_FINE), 0), lin_fine)
                    Bavg = float(-np.trapz(Bf, uu))
                    gv.append((sk, B3[0], B3[1], B3[2], Bavg))
                CURVES[f"{foot}|{xi_pc:.6g}|{M}"] = gv
            g1 = CURVES[f"{foot}|{xi_pc:.6g}|1.0"]
            P_(f"    xi = {xi_pc:.4f} pc, M = 1: gamma_v(s) = sqrt(<B>) at s = " + ", ".join(f"{x_[0]:g}" for x_ in g1) + " kAU:\n        "
               + " ".join(f"{math.sqrt(x_[4]):.4f}" for x_ in g1)
               + "\n        par/perp B: " + " ".join(f"{x_[1]:.3f}/{x_[3]:.3f}" for x_ in g1))
    OUT["numbers"]["curves"] = CURVES

    # ======================================================================================== hypotheses
    banner("H  THE PRE-DECLARED HYPOTHESES")
    h1 = {}
    for M in (1.0, 2.0):
        st = OUT["numbers"]["stiffness"]["canonical|prereg_primary"]
        g3 = [x_ for x_ in CURVES[f"canonical|{FLOOR['canonical']:.6g}|{M}"] if x_[0] == 3.0][0]
        h1[M] = (g3[4] - 1) / (st["orient_avg"] - 1)
    check("H1 SUPPRESSION: at the canonical floor the orientation-averaged (B - 1) at 3 kAU is < 5% of the unfiltered value (M = 1, 2)",
          ", ".join(f"M {M}: {v_:.2%}" for M, v_ in h1.items()), all(v_ < 0.05 for v_ in h1.values()), load_bearing=False)
    shalf = {}
    for foot in ("canonical", "alt"):
        st = OUT["numbers"]["stiffness"][f"{foot}|prereg_primary"]
        for M in (1.0, 2.0):
            cv = CURVES[f"{foot}|{FLOOR[foot]:.6g}|{M}"]
            fr = np.array([(x_[4] - 1) / (st["orient_avg"] - 1) for x_ in cv])
            ss = np.array([x_[0] for x_ in cv])
            i = int(np.argmax(fr >= 0.5))
            sh = math.exp(np.interp(0.5, [fr[i - 1], fr[i]], [math.log(ss[i - 1]), math.log(ss[i])]))
            shalf[(foot, M)] = sh / (FLOOR[foot] * C.PC_M / C.KAU_M)
    OUT["numbers"]["H2_shalf_over_xi"] = {f"{k_[0]}|{k_[1]}": v_ for k_, v_ in shalf.items()}
    mdep = max(abs(shalf[(f, 2.0)] / shalf[(f, 1.0)] - 1) for f in ("canonical", "alt"))
    check("H2 TRANSITION AT s ~ xi: the orientation-averaged boost reaches half its unfiltered value at s_1/2 in [1.5, 3] xi, moving < 15% "
          "between 1 and 2 Msun", ", ".join(f"{k_[0][:3]} M{k_[1]:.0f}: {v_:.2f} xi" for k_, v_ in shalf.items()) + f"; mass dependence {mdep:.1%}",
          all(1.5 <= v_ <= 3.0 for v_ in shalf.values()) and mdep < 0.15, load_bearing=False)
    nl = []
    for foot in ("canonical", "alt"):
        tg = TAB[f"{foot}|prereg_primary|{FLOOR[foot]:.6g}"]
        for kk, v_ in tg.items():
            M, sk, th = (float(z_) for z_ in kk.split("|"))
            if sk >= 3.0 and v_["B_lin_free"] - 1 > 1e-4:
                nl.append(((v_["B"] - v_["B_lin_free"]) / (v_["B_lin_free"] - 1), foot, M, sk, th))
    nl_max = max(nl, key=lambda z_: z_[0])
    nl_min = min(nl, key=lambda z_: z_[0])
    OUT["numbers"]["H3"] = dict(max=nl_max, min=nl_min)
    check("H3 NONLINEARITY: at the floors (M <= 2.5, s >= 3 kAU) the two-body solve lowers the boost below the linear total-mass kernel, by "
          "< 15% of (B_lin - 1)", f"relative correction from {nl_min[0]:+.2%} ({nl_min[1:]}) to {nl_max[0]:+.2%} ({nl_max[1:]})",
          nl_max[0] <= 1e-6 and nl_min[0] > -0.15, load_bearing=False)
    viol = []
    for foot in ("canonical", "alt"):
        xs_ = [FLOOR[foot]] + XI_3D_ABOVE
        for M in M_REG:
            for sk in S_REG:
                for th in TH3:
                    bb_ = [TAB[f"{foot}|prereg_primary|{x_:.6g}"][key(M, sk, th)]["B"] for x_ in xs_]
                    bb_ += [LIN[f"{foot}|prereg_primary|{x_:.6g}"][f"{sk}|{th}"] for x_ in XI_LIN]
                    if any(bb_[i + 1] > bb_[i] + 1e-7 for i in range(len(bb_) - 1)):
                        viol.append((foot, M, sk, th))
    check("H4 MONOTONE IN xi: every registered-grid boost decreases with xi across the window (3-D below 0.3 pc, the exact kernel above)",
          f"violations: {len(viol)} {viol[:4]}", len(viol) == 0, load_bearing=False)
    # H4b: NOT pre-declared -- added after the development dry run (linear kernel standing in for the solves) showed that the
    # perpendicular boost overshoots its unfiltered value near s ~ 2-4 xi, so H4 fails for 90 deg at 20-30 kAU (kept as declared)
    viol_b = []
    for foot in ("canonical", "alt"):
        xs_ = [FLOOR[foot]] + XI_3D_ABOVE
        for M in M_REG:
            for sk in S_REG:
                av = [-np.trapz(np.array([TAB[f"{foot}|prereg_primary|{x_:.6g}"][key(M, sk, t_)]["B"] for t_ in TH3]), np.array([1.0, math.cos(math.radians(45)), 0.0])) for x_ in xs_]
                av += [-np.trapz(np.array([LIN[f"{foot}|prereg_primary|{x_:.6g}"][f"{sk}|{t_}"] for t_ in TH3]), np.array([1.0, math.cos(math.radians(45)), 0.0])) for x_ in XI_LIN]
                if any(av[i + 1] > av[i] + 1e-7 for i in range(len(av) - 1)):
                    viol_b.append((foot, M, sk))
    over = max((TAB[f"{foot}|prereg_primary|{x_:.6g}"][key(M, sk, 90.0)]["B"] - OUT["numbers"]["stiffness"][f"{foot}|prereg_primary"]["B_perp"], foot, x_, M, sk)
               for foot in ("canonical", "alt") for x_ in [FLOOR[foot]] + XI_3D_ABOVE for M in M_EXT for sk in S_EXT)
    OUT["numbers"]["H4b"] = dict(violations=viol_b, perp_overshoot_max=over)
    check("H4b (added after the dry run, NOT pre-declared) the ORIENTATION-AVERAGED boost (3-point rule) decreases with xi at every "
          "registered-grid point; the perpendicular component alone overshoots its unfiltered value",
          f"violations: {len(viol_b)}; largest perpendicular overshoot above B_perp(xi -> 0): {over[0]:+.4f} at {over[1:]}",
          len(viol_b) == 0, "a flattened (filtered) source pulls harder in its own plane near its edge: the in-plane (perpendicular) "
          "radial force of the Gaussian-smoothed anisotropic kernel exceeds the point value at s ~ 2-4 xi", load_bearing=False)
    h5 = []
    for M in (1.0, 2.0):
        tg = TAB[f"canonical|prereg_primary|{FLOOR['canonical']:.6g}"]
        small = all(tg[key(M, sk, 90.0)]["B"] > tg[key(M, sk, 0.0)]["B"] for sk in (3.0, 5.0, 7.0, 10.0))
        large = all(tg[key(M, sk, 0.0)]["B"] > tg[key(M, sk, 90.0)]["B"] for sk in (30.0, 45.0, 60.0, 90.0, 120.0))
        h5.append((M, small, large))
    check("H5 ANISOTROPY FLIP: at the canonical floor perpendicular > parallel at s <= 10 kAU and parallel > perpendicular at s >= 30 kAU",
          f"{h5}", all(a_ and b_ for _, a_, b_ in h5), load_bearing=False)
    h6 = max(abs(LIN[f"{foot}|prereg_primary|{x_:.6g}"][f"{sk}|{th}"] - 1) for foot in ("canonical", "alt") for x_ in (1.0, 2.0, 3.0, 10.0, 30.0, 100.0)
             for sk in S_EXT if sk <= 30 for th in TH_FINE)
    check("H6 NEWTONIAN LIMIT: for xi >= 1 pc, |B - 1| < 1e-3 at every s <= 30 kAU", f"max |B - 1| = {h6:.1e}", h6 < 1e-3, load_bearing=False)
    tp = TAB[f"canonical|prereg_primary|{FLOOR['canonical']:.6g}"]
    tc = TAB[f"canonical|chain_FP7|{FLOOR['canonical']:.6g}"]
    avg3 = lambda tg, M, sk: float(-np.trapz(np.array([tg[key(M, sk, t_)]["B"] for t_ in TH3]), np.array([1.0, math.cos(math.radians(45)), 0.0])))
    rp, rc = avg3(tp, 1.0, 30.0) - 1, avg3(tc, 1.0, 30.0) - 1
    check("H7 FIELD SENSITIVITY: the chain's own Galactic field (2.32e-10) lowers the canonical-floor (B - 1) at 30 kAU by > 20% vs the "
          "pre-registration's 1.778e-10", f"(B - 1) = {rp:.4f} (1.778e-10) vs {rc:.4f} (2.32e-10): {1 - rc / rp:.1%} lower", rc < 0.8 * rp, load_bearing=False)

    return finish(T_START)


def finish(T_START):
    banner("W  THE LEDGER")
    LEDGER = [
        ("X22a", "the chain's z = 0 wide-binary law = FP7's double-filtered two-field AQUAL with J_P2 (FP13's separator and FP14's alpha_c drop out locally)", "DERIVED", "K0"),
        ("X22b", "xi -> 0 limit: B_par = nu_P2(y_extN) (the frozen record's 1.1389 = sqrt), B_perp = 1 + 1/sqrt(mu_T mu_L): the parallel-only reading overstates", "DERIVED", "K1, K2"),
        ("X22c", "the force tables B(M, s, theta; xi) at the floors and above (3-D nonlinear, validated: deep-MOND two-body, linear kernel, 2-D FEM, convergence)", "DERIVED" if not MUTATE else "n/a", "K3-K7, P"),
        ("X22d", "the Galactic field at the Sun: the pre-registration's frozen 1.778e-10 / 2.078e-10 vs the chain's 2.32e-10 (FP7)", "POSTULATED", "inputs; H7 prices the choice"),
        ("X22e", "the solver takes a plug-in screening term (a matter-keyed one must supply its key force)", "DERIVED", "K8"),
    ]
    for k_, what, st_, why in LEDGER:
        P_(f"    {k_:6s} {st_:11s} {what}  --  {why}")
    OUT["ledger"] = [dict(link=k_, what=w_, status=s_, basis=b_) for k_, w_, s_, b_ in LEDGER]
    n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
    OUT["verdict"] = dict(n_checks=len(CH), n_fail_load_bearing=n_fail, wall_s=time.time() - T_START)
    with open(JSN, "w") as fh:
        json.dump(OUT, fh, indent=1, default=str)
    rc = 0 if n_fail == 0 else 1
    P_(f"\n  {len(CH) - sum(1 for _, ok, _l in CH if not ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote "
       f"{os.path.basename(JSN)}  ({time.time() - T_START:.0f} s)")
    P_(f"rc = {rc}")
    sys.stdout.flush()
    sys.stdout = sys.__stdout__
    return rc


if __name__ == "__main__":
    sys.exit(main())
