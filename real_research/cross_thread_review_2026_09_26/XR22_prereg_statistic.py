#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR22_prereg_statistic -- THE CHAIN'S WIDE-BINARY PREDICTION IN THE FROZEN GAIA DR4 STATISTIC: the pre-registered gamma_v estimator
applied to the derivation chain's force law (XR22_force_law.py), across the heat filter's window, both a0 footings; where it lands
against the frozen decision rows; whether DR4 can measure xi; and FP17's Galileon variant as a labelled estimate.

WHY.  The frozen pre-registration (prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md; read-only, never edited here) scores one
number, gamma_hat: the median of vtilde = v_perp/sqrt(G M/s_proj) in 8 bins of log10 y_proj, fitted by a 1-parameter asymptote
with the EFE-saturated shape and an anchored nuisance kappa (section 1.3), against rows built for Arm A (Route A one-field AQUAL,
no filter; canonical 1.1614-1.1814) and Arm B (the carrier reading, xi >= 4 pc: 1.0000 +- 0.0025; killed from above at 1.084).
The chain's law (FP7 + FP14 + FP13 at z = 0: two-field AQUAL with J_P2 and a double heat filter of length xi) is neither arm.

THE TWO PATHS FROM FORCE LAW TO gamma_hat (both through the frozen estimator's own functions, exec'd read-only):
  REG   the theory-to-gamma_v path Amendments 11 and 12 register for coherence-length arms (g03y / L47 run_estimator, mirrored
        line by line): tables B(M_tot in {1, 2}, s in 3-30 kAU, 0/45/90 deg), orientation-averaged by the 3-point rule,
        log-interpolated in s and linear in M with clipping, velocity boost sqrt(B) at fixed orbit, population =
        make_population(1.5e6, seed 20261216) used as data and model.
  PHYS  the same population and model medians (a mirror of make_population, bit-identical by control), each system boosted at
        its TRUE mass (0.6-2.5 Msun), TRUE 3-D separation (1.5-120 kAU) and its own angle psi to an isotropic Galactic-field
        direction (Amendment 10 PART D's treatment), with the full angular dependence (lane 1's validated interpolation).
Both are reported; PHYS is the more faithful force law, REG the like-for-like comparison with the registered arms.

PRE-DECLARED HYPOTHESES (before the first run of this script; the lane-1 dry run and a linear-kernel preview of the boost vs
separation had been seen, the estimator's response to the chain's law had not).  They are REPORTED checks, kept as they fall:
  H1  PLACEMENT: the chain's gamma_hat at the canonical floor lies in [1.007, 1.056] on both paths -- the frozen row where Arm A
      is falsified and Newton is not excluded.  EXPECT TRUE.
  H2  xi DEPENDENCE: gamma_hat falls monotonically with xi and is <= 1.0025 (Arm B's registered precision) for xi >= 0.3 pc.
      EXPECT TRUE.
  H3  NOT DECISIVE vs NEWTON: at no allowed xi does gamma_hat exceed 1 + 3 sigma_tot (1.084, sigma_tot = 0.028).  EXPECT TRUE.
  H4  xi NOT FIXED BY THE FROZEN STATISTIC: for a true xi at the floor, the 2 sigma_tot interval of gamma_hat reaches 1.000, so
      DR4's frozen number gives at most an upper bound on the boost, i.e. a LOWER bound on xi.  EXPECT TRUE.
  H5  WHERE THE xi INFORMATION IS: in a separation-resolved statistic (median vtilde per s_proj bin, N = 30,000) >= 70% of the
      Fisher information on ln xi at the floor comes from s_proj = 5-30 kAU.  EXPECT TRUE.
  H6  THE FROZEN LADDER: the strictness-ladder rung 3-20 kAU moves the chain's floor gamma_hat by less than sigma_fit = 0.019
      (so the frozen stability rule would not by itself void a true chain signal).  EXPECT TRUE (weakly held).
  H7  KAPPA WINDOW: the anchored nuisance kappa stays in the frozen [0.95, 1.05] for the chain at every xi.  EXPECT TRUE.
  H8  GALILEON vs HEAT FILTER, FROZEN STATISTIC: over FP17's window (k^(1/4) in [104, ~400] kpc) the Galileon's gamma_hat range
      overlaps the heat filter's, so the frozen number cannot tell them apart.  EXPECT TRUE.
  H9  GALILEON vs HEAT FILTER, RESOLVED: at matched gamma_hat, a separation x mass resolved statistic at N = 30,000 separates
      them by < 3 sigma.  EXPECT TRUE (weakly held).
  H10 ANISOTROPY: the chain's sample-level projected split (Amendment 2(e)) at the floor is parallel-dominant, i.e. opposite to
      the sense Amendment 2(f) registers for Arm A, at < 1 sigma for N = 30,000.  EXPECT TRUE.
"""
DOC_CHECKS = r"""
CHECKS (load-bearing: S1-S3, L1, L2)
  S1  CONTROL: the registered path on g03y's committed tables returns Amendment 11(b)'s 1.0450 / 1.0300 and on g03g's the
      published 1.0325 / 1.0400; the cached estimator is bit-identical to the direct call.
  S2  CONTROL: the frozen pipeline's own gate (seed 20261216, 3,000,000-pair master) reproduces its committed inject-1.00 recovery
      0.9850 +- 0.0137 (kappa 1.0070) / 0.9900 +- 0.0125 (kappa 1.0043).
  S3  CONTROL: the population mirror is bit-identical to the frozen make_population.
  L1  THE PREDICTION PATH CARRIES THE FILTER: at the canonical floor the separation-binned boost of the median vtilde at s_proj
      2-5 kAU is below 25% of that at 20-30 kAU (lane 1's derived transition, H1/H2 there, seen through the frozen population).
  L2  THE PREDICTION PATH CARRIES xi: gamma_hat(100 pc) = 1.0000 +- 0.0025 on both paths, and gamma_hat(floor) exceeds it by > 0.005.
  H1-H10 as above (reported).   V2-K  FP17's wide-binary screening radius reproduced (control of the V2 estimate, reported).
  P  the placement table (Amendment 7(e) reporting).   W  the ledger.
VARIANTS SCORED
  V1  the heat filter (the chain as committed), xi from the floor to 100 pc: FP17's tie xi = ((hbar/m)^2/a0)^(1/3) = 1.57-3.28 pc
      is this variant at that xi.
  V2  BDEF's Riemann-coupled Galileon (Babichev, Deffayet & Esposito-Farese 2011, PRD 84, 061502(R)) in FP17's OWN spherical
      reduction (flux x^2/(1 - 2x) + (r_V/r)^4 x^2 = y, r_V = (8 k G M a0)^(1/4)/c), carried onto the linear EFE response of the
      UNFILTERED law as a per-pair screening factor -- an ESTIMATE, NOT ADOPTED (its static-gradient c_T and its stability are
      open, FP17).  Two readings of the reduction around the Galactic field (the Galileon acting on the pair's own perturbation,
      FP17's r_E logic; or linearised about x_e, a stiffening 2 x_e (r_V/r)^4) x two stiffnesses (mu_T, mu_L) bracket it.
  V0  the xi -> 0 LINEAR kernel (reported): y-independent, so it shows what the frozen estimator does with a boost that is the same
      at every acceleration (the anchored kappa absorbs it); it is NOT the unfiltered law's gamma_hat (that law returns to Newton at
      high y, and is excluded by the Solar System, FP7 A4).
MUTATE=1 moves the filter to xi = 0 in the prediction path (every heat-filter prediction uses the unfiltered tables): L1 and L2
must FAIL (rc = 1).  The controls S1-S3 are unaffected.

SCOPE.  Noise-free estimator response (the 1.5e6-pair population is both data and model, as the registered path does); DR4
precision taken from the frozen document (sigma_fit = 0.019 at N = 30,000, sigma_tot = 0.028); velocity scaling at fixed orbit
(the pipeline's declared shortcut); the Galaxy's field direction isotropic per pair; equal-mass force tables (lane 1 K7 measures
the mass-ratio effect).  Nothing in prep_2026/gaia_dr4_prep is written.  Needs XR22_force_law_results.json (the main run).
Run from the repository root:
    MUTATE=1 python3 real_research/cross_thread_review_2026_09_26/XR22_prereg_statistic.py     (first)
    python3 real_research/cross_thread_review_2026_09_26/XR22_prereg_statistic.py               (last)
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "4")
sys.dont_write_bytecode = True
import json, math, time, warnings
warnings.filterwarnings("ignore")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import XR22_common as C

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR22_prereg_statistic"
_DRY = os.environ.get("XR22_DRYRUN", "0") == "1"                 # development only: reads the dry-run force law, writes to XR22_SCRATCH
if _DRY and not os.environ.get("XR22_SCRATCH"):
    sys.exit("XR22_DRYRUN needs XR22_SCRATCH (a directory outside the repository)")
_ODIR = os.environ["XR22_SCRATCH"] if _DRY else HERE
OUTF = os.path.join(_ODIR, SLUG + ("_MUTATE" if MUTATE else "") + ("_QUICK" if _DRY else "") + ".out")
JSN = os.path.join(_ODIR, SLUG + "_results" + ("_MUTATE" if MUTATE else "") + ("_QUICK" if _DRY else "") + ".json")
LAW_JSON = os.path.join(_ODIR, "XR22_force_law_results_QUICK.json") if _DRY else os.path.join(HERE, "XR22_force_law_results.json")
SIG_FIT, SIG_TOT = 0.019, 0.028                 # frozen section 1.5 (N = 30,000)
N_FROZEN = 30000
ARM_A = {"canonical": (1.1614, 1.1814), "alt": (1.1917, 1.2267)}
ARM_B, ARM_B_SIG, ARM_B_KILL, ARM_A_FALSE_BELOW, EDGE = 1.0000, 0.0025, 1.084, 1.056, 1.23
TH3 = [0.0, 45.0, 90.0]
SEPBINS = [2.0, 3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0]
POPSEED = 20261216


class Tee:
    def __init__(self, path):
        self.f = open(path, "w")

    def write(self, s):
        sys.__stdout__.write(s)
        self.f.write(s)

    def flush(self):
        sys.__stdout__.flush()
        self.f.flush()


OUT = {"lane": "XR22_prereg_statistic", "mutate": MUTATE, "checks": {}, "numbers": {}, "ledger": []}
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


def key(M, s, th):
    return f"{float(M)}|{float(s)}|{float(th)}"


def row_reading(g, kappa=1.0):
    """the frozen decision rows (section 1.5 as amended by 9-12), canonical logic; the frozen kappa rule first"""
    if not (0.95 <= kappa <= 1.05):
        return f"kappa = {kappa:.4f} outside the frozen [0.95, 1.05]: 'systematic-limited, no verdict' (frozen section 1.3/1.5)"
    if g <= 1.007:
        return "<= 1.007: Arm A falsified; Newton-side; Arm B consistent only as its Newtonian limit"
    if g < ARM_A_FALSE_BELOW:
        return "1.007-1.056: Arm A falsified (>= 3.8 sigma_tot); Newton not excluded; Amdt 11(d)'s 'decided for B' voided by Amdt 12(d)"
    if g < ARM_B_KILL:
        return "1.056-1.084: Arm A disfavored (2.8-3.8 sigma_tot); Newton disfavored at 2-3 sigma_tot"
    if g < 1.101:
        return "1.084-1.101: Arm B killed from above (Amdt 12(d)); arm not decided"
    if g < 1.129:
        return "1.101-1.129: leaning Arm A"
    if g <= EDGE:
        return "framework band rows (Amdt 10)"
    return "> 1.23: no-verdict guard zone"


class GenericEstimator:
    """the frozen estimator on an arbitrary population (data = model, the registered path's noise-free convention): the model
    medians are built once, the rng state after them is restored for every fit"""

    def __init__(self, PL, pop, a0, rng):
        self.P, self.pop, self.a0 = PL, pop, a0
        self.logy = np.log10(pop["g_proj"] / a0)
        self.mod = PL["model_medians"](pop, a0, PL["GRID"], rng)
        self.state = rng.bit_generator.state

    fit = C.RegisteredEstimator.fit


def main():
    sys.stdout = Tee(OUTF)
    T0 = time.time()
    P_(__doc__.split("PRE-DECLARED")[0].strip())
    if MUTATE:
        P_("\n  *** MUTATE=1: the filter is moved to xi = 0 in the prediction path: L1 and L2 must FAIL ***")
    CI = C.chain_inputs()
    A0 = CI["a0"]
    FLOOR = CI["xi_floor_pc"]
    LAW = C.load_json(LAW_JSON)
    TAB, LIN, ST = LAW["tables"], LAW["lin_tables"], LAW["numbers"]["stiffness"]
    S_EXT = sorted({float(k_.split("|")[1]) for k_ in TAB[f"canonical|prereg_primary|{FLOOR['canonical']:.6g}"]})
    M_EXT = sorted({float(k_.split("|")[0]) for k_ in TAB[f"canonical|prereg_primary|{FLOOR['canonical']:.6g}"]})
    TH_FINE = sorted({float(k_.split("|")[1]) for k_ in LIN["canonical|prereg_primary|0"]})
    XI_3D = {f: sorted({float(k_.split("|")[2]) for k_ in TAB if k_.startswith(f"{f}|prereg_primary|")}) for f in A0}
    XI_LIN = sorted({float(k_.split("|")[2]) for k_ in LIN if k_.startswith("canonical|prereg_primary|")} - set(XI_3D["canonical"]) - {0.0})
    P_(f"\n    force law: {os.path.basename(LAW_JSON)} (lane 1 main run: {LAW['verdict']['n_fail_load_bearing']} load-bearing failures); "
       f"3-D xi = {XI_3D['canonical']} (canonical) / {XI_3D['alt']} (alt); linear-kernel xi = {XI_LIN}; M = {M_EXT}; s = {S_EXT[0]}-{S_EXT[-1]} kAU")
    PL = C.load_pipeline()
    A0P = {"canonical": PL["A0_CAN"], "alt": PL["A0_ALT"]}           # the pipeline's own binning a0 (frozen)

    # ======================================================================================== S1-S3 controls
    banner("S1-S3  CONTROLS: the pre-registration's own machinery reproduces its committed numbers")
    t_ = time.time()
    EST = {f: C.RegisteredEstimator(PL, A0P[f]) for f in A0}
    P_(f"    registered estimator populations built ({len(EST['canonical'].pop['pmx'])} pairs after the frozen selection; {time.time() - t_:.0f} s)")
    ctrl = {}
    for lab, fn_, want in (("g03y rar_carried (Amendment 11(b))", "g03y_table_rar_carried_{}.json", {"canonical": 1.0450, "alt": 1.0300}),
                           ("g03g original (g03h published)", "g03g_table_{}.json", {"canonical": 1.0325, "alt": 1.0400})):
        for f in A0:
            Ms, S, tab = C.registered_table(C.load_json(os.path.join(C.CLOSURE, fn_.format(f)))["table"])
            r = EST[f].run_table(Ms, S, tab)
            ctrl[(lab, f)] = (r["gamma"], r["sigma"], want[f])
            P_(f"    {lab:36s} [{f:9s}]: gamma = {r['gamma']:.4f} +- {r['sigma']:.4f}  (committed {want[f]:.4f})")
    Ms, S, tab = C.registered_table(C.load_json(os.path.join(C.CLOSURE, "g03y_table_rar_carried_canonical.json"))["table"])
    direct = C.run_estimator_direct(PL, Ms, S, tab, A0P["canonical"])
    cached = EST["canonical"].run_table(Ms, S, tab)
    same = (direct[0] == cached["gamma"] and direct[1] == cached["sigma"] and direct[4] == cached["kappa"])
    P_(f"    direct run_estimator (verbatim) = {direct[0]:.4f} +- {direct[1]:.4f}, kappa {direct[4]:.6f}; cached {cached['gamma']:.4f} +- "
       f"{cached['sigma']:.4f}, kappa {cached['kappa']:.6f}: identical {same}")
    OUT["numbers"]["S1"] = {f"{k_[0]}|{k_[1]}": v_ for k_, v_ in ctrl.items()}
    check("S1 CONTROL: the registered theory-to-gamma_v path reproduces Amendment 11(b)'s 1.0450 / 1.0300 (g03y) and the published "
          "1.0325 / 1.0400 (g03g) exactly, and the cached estimator equals the direct call bit for bit",
          "; ".join(f"{k_[0][:4]} {k_[1][:3]} {v_[0]:.4f}" for k_, v_ in ctrl.items()) + f"; identical {same}",
          all(abs(v_[0] - v_[2]) < 1e-9 for v_ in ctrl.values()) and same)
    t_ = time.time()
    import multiprocessing as mp
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=1, mp_context=mp.get_context("spawn")) as ex:     # the master's memory is released on exit
        gate = ex.submit(C.frozen_gate_inject1).result()
    P_(f"    frozen gate, inject 1.00: canonical {gate['canonical'][0]:.4f} +- {gate['canonical'][1]:.4f} (kappa {gate['canonical'][2]:.4f}); alt "
       f"{gate['alt'][0]:.4f} +- {gate['alt'][1]:.4f} (kappa {gate['alt'][2]:.4f})  [committed: 0.9850 +- 0.0137 (1.0070) / 0.9900 +- 0.0125 (1.0043)]  ({time.time() - t_:.0f} s)")
    OUT["numbers"]["S2"] = gate
    check("S2 CONTROL: the frozen pipeline's own gate (seed 20261216, 3,000,000-pair master) reproduces its committed inject-1.00 recovery",
          f"{gate['canonical'][0]:.4f} +- {gate['canonical'][1]:.4f} (kappa {gate['canonical'][2]:.4f}) / {gate['alt'][0]:.4f} +- {gate['alt'][1]:.4f} (kappa {gate['alt'][2]:.4f})",
          abs(gate["canonical"][0] - 0.9850) < 1e-9 and abs(gate["canonical"][1] - 0.0137) < 5e-5 and abs(gate["alt"][0] - 0.9900) < 1e-9
          and abs(gate["alt"][1] - 0.0125) < 5e-5 and abs(gate["canonical"][2] - 1.0070) < 5e-5 and abs(gate["alt"][2] - 1.0043) < 5e-5)
    popF = C.make_population_full(PL, 1_500_000, np.random.default_rng(POPSEED), rng_orient=np.random.default_rng(POPSEED + 22))
    ident = all(np.array_equal(popF[k_], EST["canonical"].pop[k_]) for k_ in EST["canonical"].pop)
    P_(f"    population mirror vs the frozen make_population (same seed): all {len(EST['canonical'].pop)} returned fields identical: {ident}")
    check("S3 CONTROL: the mirrored population (with the 3-D separation, true masses and a field direction drawn from a SEPARATE "
          "generator) is bit-identical to the frozen make_population", f"identical {ident}", ident)
    SYS = dict(Mt=popF["Mt"], s=popF["r3d"] / PL["KAU"], th=np.minimum(popF["psi"], np.pi - popF["psi"]))

    # ======================================================================================== the prediction machinery
    def reg_table(foot, gk, xi_pc):
        """REG-format table {M|s|th: gamma} from the 3-D tables (xi in the 3-D list) or the linear kernel (mass-independent)"""
        tk = f"{foot}|{gk}|{xi_pc:.6g}"
        T = {}
        if tk in TAB and not MUTATE:
            for kk, v_ in TAB[tk].items():
                M_, s_, th_ = (float(z_) for z_ in kk.split("|"))
                if M_ in (1.0, 2.0) and 3.0 <= s_ <= 30.0:
                    T[key(M_, s_, th_)] = {"gamma": v_["B"]}
        else:
            lk = f"{foot}|{gk}|{(0.0 if MUTATE else xi_pc):.6g}"
            for M_ in (1.0, 2.0):
                for s_ in [3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0]:
                    for th_ in TH3:
                        T[key(M_, s_, th_)] = {"gamma": LIN[lk][f"{s_}|{th_}"]}
        return C.registered_table(T)

    def fine_grid(foot, xi_pc, gk="prereg_primary"):
        """B on (M_EXT, S_EXT, TH_FINE): 3-D tables with lane 1's angular interpolation, or the exact linear kernel"""
        use_lin = MUTATE or f"{foot}|{gk}|{xi_pc:.6g}" not in TAB
        lk = f"{foot}|{gk}|{(0.0 if MUTATE else xi_pc):.6g}"
        thf = np.radians(np.array(TH_FINE))
        if use_lin:
            return np.array([[LIN[lk][f"{s_}|{t_}"] for t_ in TH_FINE] for s_ in S_EXT])[None, :, :].repeat(len(M_EXT), 0)
        tg = TAB[f"{foot}|{gk}|{xi_pc:.6g}"]
        Bf = np.zeros((len(M_EXT), len(S_EXT), len(TH_FINE)))
        for i, M_ in enumerate(M_EXT):
            for j, s_ in enumerate(S_EXT):
                B3 = np.array([tg[key(M_, s_, t_)]["B"] for t_ in TH3])
                L3 = np.array([tg[key(M_, s_, t_)]["B_lin_free"] for t_ in TH3])
                linf = np.array([LIN[lk][f"{s_}|{t_}"] for t_ in TH_FINE])
                Bf[i, j] = C.angular_interp(thf, B3[None, :].repeat(len(thf), 0), L3[None, :].repeat(len(thf), 0), linf)
        return Bf

    def phys_boost(foot, xi_pc, sysd=None, gk="prereg_primary"):
        """per-system radial boost at (TRUE M, TRUE r3d, own angle): trilinear in (M, ln s, theta) on the fine grid"""
        sysd = SYS if sysd is None else sysd
        Bf = fine_grid(foot, xi_pc, gk)
        ls = np.log(np.array(S_EXT))
        thf = np.radians(np.array(TH_FINE))
        Mg = np.array(M_EXT)
        x_m = np.clip(sysd["Mt"], Mg[0], Mg[-1])
        x_s = np.clip(np.log(np.maximum(sysd["s"], 1e-9)), ls[0], ls[-1])
        x_t = sysd["th"]
        im = np.clip(np.searchsorted(Mg, x_m) - 1, 0, len(Mg) - 2)
        is_ = np.clip(np.searchsorted(ls, x_s) - 1, 0, len(ls) - 2)
        it = np.clip(np.searchsorted(thf, x_t) - 1, 0, len(thf) - 2)
        fm = (x_m - Mg[im]) / (Mg[im + 1] - Mg[im])
        fs = (x_s - ls[is_]) / (ls[is_ + 1] - ls[is_])
        ft = (x_t - thf[it]) / (thf[it + 1] - thf[it])
        out = np.zeros_like(x_m)
        for dm, wm in ((0, 1 - fm), (1, fm)):
            for ds, ws in ((0, 1 - fs), (1, fs)):
                for dt, wt in ((0, 1 - ft), (1, ft)):
                    out += wm * ws * wt * Bf[im + dm, is_ + ds, it + dt]
        return out

    def galileon_boost(foot, k14, reading, which, sysd=None, gk="prereg_primary"):
        """V2 (ESTIMATE): 1 + (B_lin,unfiltered(theta) - 1) x S_G(s; M) with FP17's reduced flux balance"""
        sysd = SYS if sysd is None else sysd
        a0 = A0[foot]
        st = ST[f"{foot}|{gk}"]
        mu = st["muT"] if which == "muT" else st["muL"]
        Bu = np.array([C.analytic_tensor(t_, st["muT"], st["muL"]) for t_ in np.radians(TH_FINE)])
        Bth = np.interp(sysd["th"], np.radians(TH_FINE), Bu)
        s_m = sysd["s"] * PL["KAU"]
        M_kg = sysd["Mt"] * C.GM_SUN
        rho = 8 * k14 ** 4 * M_kg * a0 / C.C_SI ** 4 / s_m ** 4
        yint = M_kg / s_m ** 2 / a0
        if reading == "FP17":
            u = 4 * rho * yint / mu ** 2
            Sg = np.where(u > 1e-12, 2 * (np.sqrt(1 + u) - 1) / np.maximum(u, 1e-300), 1 - u / 4)
        else:
            Sg = mu / (mu + 2 * st["xe"] * rho)
        return 1 + (Bth - 1) * Sg

    def fit_phys(B, foot, sel=None, est=None):
        return (EST[foot] if est is None else est).fit(np.sqrt(np.maximum(B, 1e-6)), sel=sel)

    def sepbins(B, foot, boot=100, seed=5):
        """the separation-resolved observable: median vtilde per s_proj bin, relative to the Newtonian median of the same pairs"""
        pop = EST[foot].pop
        rr = np.random.default_rng(seed)
        sk = pop["s_obs"] / PL["KAU"]
        vt1 = np.hypot(pop["pmx"] + pop["npmx"], pop["pmy"] + pop["npmy"]) * 4.74e3 * (pop["d_obs"] / 1000.) / pop["vc_obs"]
        g_ = np.sqrt(np.maximum(B, 1e-6))
        vtg = np.hypot(g_ * pop["pmx"] + pop["npmx"], g_ * pop["pmy"] + pop["npmy"]) * 4.74e3 * (pop["d_obs"] / 1000.) / pop["vc_obs"]
        rows = []
        for lo_, hi_ in zip(SEPBINS[:-1], SEPBINS[1:]):
            m_ = (sk >= lo_) & (sk < hi_) & (vtg < PL["VTCAP"]) & (vt1 < PL["VTCAP"])
            v0, v1 = vt1[m_], vtg[m_]
            idx = rr.integers(0, m_.sum(), (boot, m_.sum()))
            sb = np.median(v1[idx], axis=1)
            rows.append(dict(lo=lo_, hi=hi_, n=int(m_.sum()), ratio=float(np.median(v1) / np.median(v0) - 1),
                             sig_med=float(sb.std(ddof=1) / np.median(v0)), frac=float(m_.sum() / len(sk))))
        return rows

    # ======================================================================================== V1: the heat filter across xi
    banner("V1  THE CHAIN AS COMMITTED (heat filter), gamma_hat vs xi, both paths, the pre-registration's primary field" + ("  [MUTATE: xi -> 0]" if MUTATE else ""))
    XIS = {f: sorted(set(XI_3D[f]) | set(XI_LIN)) for f in A0}
    RES = {}
    for f in A0:
        P_(f"  [{f}]  (a0 = {A0[f]:.4e} in the force law; the estimator bins with the frozen {A0P[f]:.3e})")
        P_(f"    {'xi [pc]':>9s} {'REG gamma':>10s} {'kappa':>7s} {'PHYS gamma':>11s} {'kappa':>7s} {'(g-1)/sig_tot':>14s}  frozen row (PHYS)")
        for xi_pc in XIS[f]:
            Ms_, S_, tab_ = reg_table(f, "prereg_primary", xi_pc)
            rR = EST[f].run_table(Ms_, S_, tab_)
            rP = fit_phys(phys_boost(f, xi_pc), f)
            RES[(f, xi_pc)] = dict(reg=rR, phys=rP)
            P_(f"    {xi_pc:9.4f} {rR['gamma']:10.4f} {rR['kappa']:7.4f} {rP['gamma']:11.4f} {rP['kappa']:7.4f} {(rP['gamma'] - 1) / SIG_TOT:14.2f}  "
               f"{row_reading(rP['gamma'], rP['kappa'])}")
    V0 = {}
    for f in A0:
        Ms_, S_, tab_ = reg_table(f, "prereg_primary", 0.0) if not MUTATE else reg_table(f, "prereg_primary", 0.0)
        T0_ = {}
        for M_ in (1.0, 2.0):
            for s_ in [3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0]:
                for th_ in TH3:
                    T0_[key(M_, s_, th_)] = {"gamma": LIN[f"{f}|prereg_primary|0"][f"{s_}|{th_}"]}
        rR = EST[f].run_table(*C.registered_table(T0_))
        lkB = np.interp(SYS["th"], np.radians(TH_FINE), np.array([LIN[f"{f}|prereg_primary|0"][f"{S_EXT[0]}|{t_}"] for t_ in TH_FINE]))
        rP = fit_phys(lkB, f)
        V0[f] = dict(reg=rR, phys=rP)
        P_(f"  V0 [{f}] the xi -> 0 LINEAR kernel (y-independent: its boost is the same in the anchor bins as in the deep bins): REG "
           f"{rR['gamma']:.4f} (kappa {rR['kappa']:.4f}), PHYS {rP['gamma']:.4f} (kappa {rP['kappa']:.4f}) -- the anchored kappa absorbs a "
           f"y-flat boost, so this is the estimator's blind spot, NOT the unfiltered law's gamma_hat (that law returns to Newton at high y "
           f"where the scalar saturates; it is excluded by the Solar System anyway, FP7 A4); frozen row: {row_reading(rP['gamma'], rP['kappa'])}")
    OTHER = {}
    for f in A0:
        for gk, xl in (("prereg_alt", [FLOOR[f], 0.03, 0.05, 0.1]), ("chain_FP7", [FLOOR[f]])):
            for xi_pc in xl:
                rR = EST[f].run_table(*reg_table(f, gk, xi_pc))
                OTHER[(f, gk, xi_pc)] = rR
                P_(f"  [{f}] Galactic field {gk} ({dict(prereg_alt=2.078e-10, chain_FP7=2.32e-10)[gk]:.3e}), xi = {xi_pc:.4f} pc: REG gamma = "
                   f"{rR['gamma']:.4f} (kappa {rR['kappa']:.4f})")
    OUT["numbers"]["V1"] = {f"{k_[0]}|{k_[1]:.6g}": dict(reg=v_["reg"]["gamma"], reg_kappa=v_["reg"]["kappa"], phys=v_["phys"]["gamma"],
                                                         phys_kappa=v_["phys"]["kappa"], reg_sigma=v_["reg"]["sigma"], phys_sigma=v_["phys"]["sigma"],
                                                         phys_med=v_["phys"]["med"], phys_cnt=v_["phys"]["cnt"])
                            for k_, v_ in RES.items()}
    OUT["numbers"]["V0"] = {f: dict(reg=v_["reg"]["gamma"], reg_kappa=v_["reg"]["kappa"], phys=v_["phys"]["gamma"], phys_kappa=v_["phys"]["kappa"],
                                    grade="linear xi -> 0 kernel, y-independent: absorbed by the anchored kappa; not the unfiltered law's gamma_hat")
                            for f, v_ in V0.items()}
    OUT["numbers"]["other_fields"] = {f"{k_[0]}|{k_[1]}|{k_[2]:.6g}": v_["gamma"] for k_, v_ in OTHER.items()}

    # ======================================================================================== separation signature, Fisher on xi
    banner("THE SEPARATION SIGNATURE AND WHERE DR4'S xi INFORMATION IS (N = 30,000)")
    SB = {}
    for f in A0:
        for xi_pc in XIS[f]:
            SB[(f, xi_pc)] = sepbins(phys_boost(f, xi_pc), f)
        fl = SB[(f, XIS[f][0])]
        P_(f"  [{f}] separation-binned boost of the median vtilde (PHYS, chain / Newton - 1), s_proj bins {SEPBINS} kAU:")
        for xi_pc in XIS[f][:9]:
            P_(f"    xi = {xi_pc:7.4f} pc: " + " ".join(f"{r_['ratio']:+.4f}" for r_ in SB[(f, xi_pc)]))
        P_(f"    per-bin error at N = 30,000: " + " ".join(f"{r_['sig_med'] * math.sqrt(r_['n'] / (N_FROZEN * r_['frac'])):.4f}" for r_ in fl)
           + f"  (bin shares of the sample: " + " ".join(f"{r_['frac']:.2f}" for r_ in fl) + ")")
    fl = SB[("canonical", XIS["canonical"][0])]
    h0 = (fl[0]["ratio"] + fl[1]["ratio"]) / 2 / max(fl[-1]["ratio"], 1e-12)
    check("L1 THE PREDICTION PATH CARRIES THE FILTER: at the canonical floor the separation-binned boost at s_proj 2-5 kAU is < 25% of that "
          "at 20-30 kAU", f"2-3: {fl[0]['ratio']:+.4f}, 3-5: {fl[1]['ratio']:+.4f}, 20-30: {fl[-1]['ratio']:+.4f} (ratio {h0:.2f})",
          0 < fl[-1]["ratio"] and h0 < 0.25)
    FISH = {}
    for f in A0:
        xs_ = XIS[f]
        for i in range(len(xs_) - 1):
            a_, b_ = SB[(f, xs_[i])], SB[(f, xs_[i + 1])]
            dl = math.log(xs_[i + 1] / xs_[i])
            Fb = []
            for ra, rb in zip(a_, b_):
                sig30 = ra["sig_med"] * math.sqrt(ra["n"] / (N_FROZEN * ra["frac"]))
                Fb.append(((rb["ratio"] - ra["ratio"]) / dl / sig30) ** 2)
            FISH[(f, xs_[i])] = Fb
        for xi_pc in xs_[:6]:
            Fb = FISH[(f, xi_pc)]
            tot = sum(Fb)
            P_(f"  [{f}] Fisher information on ln xi at xi = {xi_pc:.4f} pc (separation bins, N = 30,000): {tot:.3f} -> sigma(ln xi) = "
               f"{1 / math.sqrt(tot) if tot > 0 else float('inf'):.2f}; per-bin shares "
               + (" ".join(f"{b_ / tot:.2f}" for b_ in Fb) if tot > 0 else "(no information: the boost does not depend on xi)"))
    Fb = FISH[("canonical", XIS["canonical"][0])]
    share = sum(Fb[2:]) / sum(Fb) if sum(Fb) > 0 else 0.0          # bins from 5 kAU up: [5,7],[7,10],[10,15],[15,20],[20,30]
    OUT["numbers"]["sepbins"] = {f"{k_[0]}|{k_[1]:.6g}": v_ for k_, v_ in SB.items()}
    OUT["numbers"]["fisher_sep"] = {f"{k_[0]}|{k_[1]:.6g}": v_ for k_, v_ in FISH.items()}
    check("H5 WHERE THE xi INFORMATION IS: >= 70% of the separation-resolved Fisher information on ln xi at the floor comes from s_proj = 5-30 kAU",
          f"share {share:.2f}", share >= 0.7, load_bearing=False)

    # ======================================================================================== the frozen number as a xi-meter
    banner("THE FROZEN NUMBER AS A xi-METER: gamma_hat(xi) against the frozen error model")
    PREC = {}
    for f in A0:
        xs_ = XIS[f]
        gP = np.array([RES[(f, x_)]["phys"]["gamma"] for x_ in xs_])
        gR = np.array([RES[(f, x_)]["reg"]["gamma"] for x_ in xs_])
        mono = all(gP[i + 1] <= gP[i] + 1e-12 for i in range(len(gP) - 1)) and all(gR[i + 1] <= gR[i] + 1e-12 for i in range(len(gR) - 1))
        top = float(gP[0])
        slope = float((gP[1] - gP[0]) / math.log(xs_[1] / xs_[0]))
        PREC[f] = dict(top=top, top_reg=float(gR[0]), lo2=top - 2 * SIG_TOT, newton_in=bool(top - 2 * SIG_TOT <= 1.0), mono=mono,
                       zN=(top - 1) / SIG_TOT, zN_fit=(top - 1) / SIG_FIT, dgdlnxi=slope,
                       sig_lnxi_tot=SIG_TOT / max(abs(slope), 1e-12), sig_lnxi_fit=SIG_FIT / max(abs(slope), 1e-12))
        # the xi a Newtonian (gamma_hat = 1.000) outcome excludes at 2 sigma_tot, and the same at the infinite-N ceiling (sigma_sys = 0.02)
        for lab, sg in (("tot", SIG_TOT), ("sys_only", 0.02)):
            cut = 1.0 + 2 * sg
            xi_ex = None
            for i in range(len(xs_) - 1):
                if gP[i] >= cut > gP[i + 1]:
                    xi_ex = math.exp(np.interp(cut, [gP[i + 1], gP[i]], [math.log(xs_[i + 1]), math.log(xs_[i])]))
            PREC[f][f"xi_excluded_by_newton_{lab}"] = xi_ex
        P_(f"  [{f}] ceiling (floor xi): PHYS {top:.4f} / REG {gR[0]:.4f}; distance to Newton {PREC[f]['zN']:.2f} sigma_tot ({PREC[f]['zN_fit']:.2f} "
           f"sigma_fit); d gamma/d ln xi at the floor {slope:+.4f} -> sigma(ln xi) from the frozen number {PREC[f]['sig_lnxi_tot']:.1f} (sigma_tot) / "
           f"{PREC[f]['sig_lnxi_fit']:.1f} (sigma_fit); a true-floor outcome's 2 sigma_tot interval [{top - 2 * SIG_TOT:.4f}, {top + 2 * SIG_TOT:.4f}] "
           f"{'reaches' if top - 2 * SIG_TOT <= 1 else 'does not reach'} Newton; a Newtonian outcome (1.000) excludes xi below "
           f"{PREC[f]['xi_excluded_by_newton_tot']} pc at 2 sigma_tot (below {PREC[f]['xi_excluded_by_newton_sys_only']} pc at the infinite-N floor sigma_sys = 0.02)")
    OUT["numbers"]["precision"] = PREC
    g100 = {f: (RES[(f, max(XIS[f]))]["phys"]["gamma"], RES[(f, max(XIS[f]))]["reg"]["gamma"]) for f in A0}
    check("L2 THE PREDICTION PATH CARRIES xi: gamma_hat(100 pc) = 1.0000 +- 0.0025 on both paths and gamma_hat(floor) exceeds it by > 0.005",
          "; ".join(f"{f}: floor {PREC[f]['top']:.4f} / {PREC[f]['top_reg']:.4f}, 100 pc {g100[f][0]:.4f} / {g100[f][1]:.4f}" for f in A0),
          all(abs(g100[f][0] - 1) <= ARM_B_SIG and abs(g100[f][1] - 1) <= ARM_B_SIG and PREC[f]["top"] > g100[f][0] + 0.005
              and PREC[f]["top_reg"] > g100[f][1] + 0.005 for f in A0))
    check("H1 PLACEMENT: the chain's gamma_hat at the canonical floor lies in [1.007, 1.056] on both paths (Arm A falsified, Newton not excluded)",
          f"PHYS {PREC['canonical']['top']:.4f}, REG {PREC['canonical']['top_reg']:.4f} (alt: {PREC['alt']['top']:.4f} / {PREC['alt']['top_reg']:.4f})",
          all(1.007 <= v_ <= 1.056 for v_ in (PREC["canonical"]["top"], PREC["canonical"]["top_reg"])), load_bearing=False)
    xi_n = {f: min([x_ for x_ in XIS[f] if RES[(f, x_)]["phys"]["gamma"] <= 1.0025 and RES[(f, x_)]["reg"]["gamma"] <= 1.0025], default=None) for f in A0}
    check("H2 xi DEPENDENCE: gamma_hat falls monotonically with xi on both paths and is <= 1.0025 for every xi >= 0.3 pc",
          "; ".join(f"{f}: monotone {PREC[f]['mono']}, first xi with gamma <= 1.0025: {xi_n[f]}" for f in A0),
          all(PREC[f]["mono"] for f in A0) and all(max(v_["phys"]["gamma"], v_["reg"]["gamma"]) <= 1.0025
                                                   for (f, x_), v_ in RES.items() if x_ >= 0.3), load_bearing=False)
    check("H3 NOT DECISIVE vs NEWTON: at no allowed xi does gamma_hat exceed 1 + 3 sigma_tot = 1.084",
          f"max gamma_hat {max(max(v_['phys']['gamma'], v_['reg']['gamma']) for v_ in RES.values()):.4f}",
          all(max(v_["phys"]["gamma"], v_["reg"]["gamma"]) < 1 + 3 * SIG_TOT for v_ in RES.values()), load_bearing=False)
    check("H4 xi NOT FIXED BY THE FROZEN NUMBER: a true floor-xi outcome's 2 sigma_tot interval reaches gamma = 1 (so the frozen number bounds "
          "the boost from above and xi only from below)", "; ".join(f"{f}: [{PREC[f]['lo2']:.4f}, ...]" for f in A0),
          all(PREC[f]["newton_in"] for f in A0), load_bearing=False)
    kap_all = [v_[p_]["kappa"] for v_ in RES.values() for p_ in ("reg", "phys")]
    check("H7 KAPPA WINDOW: the anchored nuisance kappa stays in the frozen [0.95, 1.05] at every xi (both paths, both footings)",
          f"kappa in [{min(kap_all):.4f}, {max(kap_all):.4f}]", min(kap_all) >= 0.95 and max(kap_all) <= 1.05, load_bearing=False)

    # ======================================================================================== the frozen strictness ladder (3-20 kAU)
    banner("THE FROZEN STRICTNESS LADDER: separation 2-30 -> 3-20 kAU (the frozen generator rerun with the rung's cut; data = model)")
    LAD = {}
    for f in A0:
        rngR = np.random.default_rng(POPSEED + 3)
        popR = C.make_population_full(PL, 1_500_000, rngR, smin_kAU=3.0, smax_kAU=20.0, rng_orient=np.random.default_rng(POPSEED + 23))
        estR = GenericEstimator(PL, {k_: popR[k_] for k_ in EST[f].pop}, A0P[f], rngR)
        sysR = dict(Mt=popR["Mt"], s=popR["r3d"] / PL["KAU"], th=np.minimum(popR["psi"], np.pi - popR["psi"]))
        for xi_pc in (XIS[f][0], XIS[f][1], XIS[f][2]):
            rF = RES[(f, xi_pc)]["phys"]
            rS = estR.fit(np.sqrt(np.maximum(phys_boost(f, xi_pc, sysR), 1e-6)))
            rN = estR.fit(np.ones(len(popR["Mt"])))
            LAD[(f, xi_pc)] = dict(full=rF["gamma"], sub=rS["gamma"], newton_sub=rN["gamma"], shift=rS["gamma"] - rF["gamma"], kappa_sub=rS["kappa"])
            P_(f"  [{f}] xi = {xi_pc:.4f} pc: gamma_hat 2-30 kAU {rF['gamma']:.4f} -> 3-20 kAU {rS['gamma']:.4f} (kappa {rS['kappa']:.4f}; Newton on the "
               f"rung {rN['gamma']:.4f}); shift {rS['gamma'] - rF['gamma']:+.4f} = {(rS['gamma'] - rF['gamma']) / SIG_FIT:+.2f} sigma_fit")
    OUT["numbers"]["ladder"] = {f"{k_[0]}|{k_[1]:.6g}": v_ for k_, v_ in LAD.items()}
    check("H6 THE FROZEN LADDER: the 3-20 kAU rung moves the chain's floor gamma_hat by < sigma_fit = 0.019",
          "; ".join(f"{k_[0]} {k_[1]:.4f}: {v_['shift']:+.4f}" for k_, v_ in LAD.items() if k_[1] == XIS[k_[0]][0]),
          all(abs(v_["shift"]) < SIG_FIT for k_, v_ in LAD.items() if k_[1] == XIS[k_[0]][0]),
          "the frozen stability rule requires every ladder variant to move gamma_hat by < 1 sigma_fit, else 'systematic-limited'",
          load_bearing=False)

    # ======================================================================================== anisotropy split (non-scoring)
    banner("THE ORIENTATION-RESOLVED SPLIT (Amendment 2(e), non-scoring): projected separation vs the projected field direction")
    ANI = {}
    par = popF["cosphi_proj"] > math.cos(math.pi / 4)
    for f in A0:
        Bp = phys_boost(f, XIS[f][0])
        rpar = fit_phys(Bp, f, sel=par)
        rper = fit_phys(Bp, f, sel=~par)
        d_ = rper["gamma"] - rpar["gamma"]
        s30 = SIG_FIT * math.sqrt(2.0) * math.sqrt(2.0)             # each half of N = 30,000: sigma_fit sqrt(2); the difference: x sqrt(2)
        ANI[f] = dict(par=rpar["gamma"], perp=rper["gamma"], diff=d_, z=d_ / s30, n_par=int(par.sum()), n_perp=int((~par).sum()))
        P_(f"  [{f}] floor: gamma_hat projected-parallel half {rpar['gamma']:.4f}, perpendicular half {rper['gamma']:.4f}: perp - par = {d_:+.4f} "
           f"({d_ / s30:+.2f} sigma at N = 30,000)")
    OUT["numbers"]["anisotropy"] = ANI
    check("H10 ANISOTROPY: the chain's floor sample-level split is parallel-dominant (opposite to Amendment 2(f)'s registered Arm-A "
          "sense) at < 1 sigma for N = 30,000", "; ".join(f"{f}: {v_['diff']:+.4f} ({v_['z']:+.2f} sigma)" for f, v_ in ANI.items()),
          all(v_["diff"] < 0 and abs(v_["z"]) < 1 for v_ in ANI.values()), load_bearing=False)

    # ======================================================================================== V2 the Galileon (estimate)
    banner("V2  BDEF'S RIEMANN-COUPLED GALILEON, FP17'S REDUCTION (ESTIMATE; NOT ADOPTED: its c_T and stability are open)")
    V4 = CI["V4"]
    k_floor = {f: V4["floor_saturn_kpc"][f] * C.KPC_M for f in A0}
    k_ceil = {f: V4["ceil_gw_kpc"][f] * C.KPC_M for f in A0}
    rE, rE7 = {}, {}
    for f in A0:
        a0 = A0[f]
        rV = (8 * k_floor[f] ** 4 * 2 * C.GM_SUN * a0) ** 0.25 / C.C_SI
        rM = math.sqrt(2 * C.GM_SUN / a0)
        # FP17's own convention: x_p2(2.32e-10/a0), i.e. the Galactic field fed to P2 as a NEWTONIAN field
        xeN, muTN, muLN = C.LAW_P2.stiffness(2.32e-10 / a0)
        rE[f] = [(rV ** 4 * rM ** 2 / mu ** 2) ** (1 / 6) / C.PC_M for mu in (muTN, muLN)]
        # FP7 A4's convention (and this lane's): 2.32e-10 is the OBSERVED field, inverted through P2
        xe7, muT7, muL7 = C.LAW_P2.stiffness(C.eta_of_gobs(2.32e-10 / a0))
        rE7[f] = [(rV ** 4 * rM ** 2 / mu ** 2) ** (1 / 6) / C.PC_M for mu in (muT7, muL7)]
    P_(f"    FP17 V4: k^(1/4) floor (Saturn monopole) {V4['floor_saturn_kpc']['canonical']:.2f} kpc, GW170817 ceiling (FP17's estimate) "
       f"{V4['ceil_gw_kpc']['canonical']:.0f} / {V4['ceil_gw_kpc']['alt']:.0f} kpc")
    P_("    r_E(2 Msun, k floor, 2.32e-10) in FP17's convention (the field as Newtonian): "
       + "; ".join(f"{f}: {rE[f][0]:.4f} (mu_T) / {rE[f][1]:.4f} (mu_L) pc" for f in A0) + "  (FP17 quotes 0.035-0.087 pc)")
    P_("    the same with the field as OBSERVED (FP7 A4's convention, used for every number below): "
       + "; ".join(f"{f}: {rE7[f][0]:.4f} / {rE7[f][1]:.4f} pc" for f in A0)
       + "  -- FP17's r_E runs 6-12% small from that convention (flagged, not load-bearing here)")
    rng_all = [v_ for f in A0 for v_ in rE[f]]
    OUT["numbers"]["V2_rE"] = dict(fp17_convention=rE, fp7_convention=rE7)
    check("V2-K CONTROL (reported): this lane's reduction, in FP17's convention, reproduces FP17's wide-binary screening radius for a "
          "2-Msun pair at the floor (0.035-0.087 pc)", f"{min(rng_all):.4f}-{max(rng_all):.4f} pc",
          abs(min(rng_all) - 0.035) < 0.0015 and abs(max(rng_all) - 0.087) < 0.0015, load_bearing=False)
    GAL = {}
    for f in A0:
        for kl, kv in (("floor", k_floor[f]), ("ceiling", k_ceil[f])):
            for reading in ("FP17", "linearised"):
                for which in ("muT", "muL"):
                    Bg = galileon_boost(f, kv, reading, which)
                    rP = fit_phys(Bg, f)
                    GAL[(f, kl, reading, which)] = dict(gamma=rP["gamma"], kappa=rP["kappa"], B=Bg)
        P_(f"  [{f}] gamma_hat (PHYS): " + "; ".join(f"k {kl}, {rd}, {w}: {GAL[(f, kl, rd, w)]['gamma']:.4f}"
                                                    for kl in ("floor", "ceiling") for rd in ("FP17", "linearised") for w in ("muT", "muL")))
    OUT["numbers"]["V2"] = {"|".join(k_): dict(gamma=v_["gamma"], kappa=v_["kappa"]) for k_, v_ in GAL.items()}
    P_("  gamma_v(s) = sqrt(<B>) (sphere average over the field direction), primary field, canonical:")
    sgrid = [2.0, 3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0, 45.0, 60.0]
    stc = ST["canonical|prereg_primary"]
    Bu = np.array([C.analytic_tensor(t_, stc["muT"], stc["muL"]) for t_ in np.radians(TH_FINE)])
    uu = np.cos(np.radians(TH_FINE))
    GCURVE = {}
    for M_ in (1.0, 2.0):
        for kl, kv in (("floor", k_floor["canonical"]), ("ceiling", k_ceil["canonical"])):
            for reading in ("FP17", "linearised"):
                row = []
                for sk in sgrid:
                    s_m = sk * C.KAU_M
                    Mk = M_ * C.GM_SUN
                    rho = 8 * kv ** 4 * Mk * A0["canonical"] / C.C_SI ** 4 / s_m ** 4
                    yint = Mk / s_m ** 2 / A0["canonical"]
                    Bs = []
                    for which in ("muT", "muL"):
                        mu = stc[which]
                        if reading == "FP17":
                            u = 4 * rho * yint / mu ** 2
                            Sg = 2 * (math.sqrt(1 + u) - 1) / u if u > 1e-12 else 1.0
                        else:
                            Sg = mu / (mu + 2 * stc["xe"] * rho)
                        Bs.append(float(-np.trapz(1 + (Bu - 1) * Sg, uu)))
                    row.append((sk, math.sqrt(min(Bs)), math.sqrt(max(Bs))))
                GCURVE[f"{M_}|{kl}|{reading}"] = row
                P_(f"    Galileon M = {M_}, k {kl:7s}, {reading:10s}: " + " ".join(f"{a_:.3f}-{b_:.3f}" for _, a_, b_ in row) + f"   (s = {sgrid} kAU)")
        hf = LAW["numbers"]["curves"].get(f"canonical|{FLOOR['canonical']:.6g}|{M_}")
        if hf:
            P_(f"    heat filter M = {M_}, xi at the floor:          " + " ".join(f"{math.sqrt(x_[4]):.3f}" for x_ in hf if x_[0] in sgrid))
    OUT["numbers"]["V2_curves"] = GCURVE
    ghf = [RES[("canonical", x_)]["phys"]["gamma"] for x_ in XIS["canonical"]]
    ggal = [v_["gamma"] for k_, v_ in GAL.items() if k_[0] == "canonical"]
    overlap = (min(ggal) <= max(ghf)) and (max(ggal) >= min(ghf))
    check("H8 GALILEON vs HEAT FILTER, FROZEN NUMBER: the Galileon's gamma_hat range over its window overlaps the heat filter's, so the "
          "frozen statistic cannot tell them apart", f"heat filter [{min(ghf):.4f}, {max(ghf):.4f}]; Galileon (all readings) [{min(ggal):.4f}, {max(ggal):.4f}]",
          overlap, load_bearing=False)
    pop = EST["canonical"].pop
    sk_ = pop["s_obs"] / PL["KAU"]
    mq = np.quantile(pop["M_obs"], [0, 1 / 3, 2 / 3, 1])
    mq[-1] = np.inf

    def resolved(B):
        g_ = np.sqrt(np.maximum(B, 1e-6))
        vt = np.hypot(g_ * pop["pmx"] + pop["npmx"], g_ * pop["pmy"] + pop["npmy"]) * 4.74e3 * (pop["d_obs"] / 1000.) / pop["vc_obs"]
        cells = []
        for lo_, hi_ in zip(SEPBINS[:-1], SEPBINS[1:]):
            for j in range(3):
                m_ = (sk_ >= lo_) & (sk_ < hi_) & (pop["M_obs"] >= mq[j]) & (pop["M_obs"] < mq[j + 1]) & (vt < PL["VTCAP"])
                v = vt[m_]
                cells.append((float(np.median(v)), float(1.2533 * v.std() / math.sqrt(m_.sum())), int(m_.sum())))
        return cells
    SEPR = {}
    xs_c = XIS["canonical"]
    gcurve = np.array([RES[("canonical", x_)]["phys"]["gamma"] for x_ in xs_c])
    for k_, v_ in GAL.items():
        if k_[0] != "canonical" or v_["gamma"] > gcurve[0] or v_["gamma"] < gcurve[-1] + 1e-4:
            continue
        i = int(np.searchsorted(-gcurve, -v_["gamma"])) - 1
        i = min(max(i, 0), len(xs_c) - 2)
        w = (gcurve[i] - v_["gamma"]) / max(gcurve[i] - gcurve[i + 1], 1e-12)
        Bh = (1 - w) * phys_boost("canonical", xs_c[i]) + w * phys_boost("canonical", xs_c[i + 1])
        ch, cg = resolved(Bh), resolved(v_["B"])
        chi2 = 0.0
        for (mh, sh, nh), (mg, sg, ng) in zip(ch, cg):
            chi2 += ((mh - mg) / (sh * math.sqrt(len(sk_) / N_FROZEN))) ** 2
        xi_m = math.exp((1 - w) * math.log(xs_c[i]) + w * math.log(xs_c[i + 1]))
        SEPR[k_] = dict(gamma=v_["gamma"], xi_matched=xi_m, chi2=chi2, z=math.sqrt(chi2))
        P_(f"    matched gamma_hat {v_['gamma']:.4f}: Galileon ({', '.join(k_[1:])}) vs heat filter at xi = {xi_m:.4f} pc: resolved "
           f"(7 s_proj x 3 mass bins) Asimov chi^2 = {chi2:.2f} -> {math.sqrt(chi2):.2f} sigma at N = 30,000")
    OUT["numbers"]["V2_resolved"] = {"|".join(k_): v_ for k_, v_ in SEPR.items()}
    zmax = max((v_["z"] for v_ in SEPR.values()), default=float("nan"))
    check("H9 GALILEON vs HEAT FILTER, RESOLVED: at matched gamma_hat a separation x mass resolved statistic at N = 30,000 separates them by < 3 sigma",
          f"max {zmax:.2f} sigma over {len(SEPR)} matched readings", len(SEPR) > 0 and zmax < 3.0, load_bearing=False)

    # ======================================================================================== placement table
    banner("P  PLACEMENT AGAINST THE FROZEN PRE-REGISTRATION (Amendment 7(e)/10(b)/11(g) reporting: raw gamma_hat, sigma_fit, distances)")
    PLACE = []
    for f in A0:
        for xi_pc in XIS[f]:
            g = RES[(f, xi_pc)]["phys"]["gamma"]
            gr = RES[(f, xi_pc)]["reg"]["gamma"]
            PLACE.append(dict(foot=f, xi=xi_pc, phys=g, reg=gr, d_newton=(g - 1) / SIG_FIT, d_armA_floor=(g - ARM_A[f][0]) / SIG_FIT,
                              d_armA_top=(g - ARM_A[f][1]) / SIG_FIT, d_armB=(g - ARM_B) / SIG_FIT,
                              row=row_reading(g, RES[(f, xi_pc)]["phys"]["kappa"])))
    for p_ in PLACE:
        P_(f"    {p_['foot']:9s} xi {p_['xi']:8.4f} pc: gamma_hat {p_['phys']:.4f} (REG {p_['reg']:.4f}); to Newton {p_['d_newton']:+.2f}, to Arm A "
           f"{ARM_A[p_['foot']][0]} {p_['d_armA_floor']:+.2f} / {ARM_A[p_['foot']][1]} {p_['d_armA_top']:+.2f}, to Arm B {p_['d_armB']:+.2f} sigma_fit  |  {p_['row']}")
    OUT["numbers"]["placement"] = PLACE

    # ======================================================================================== ledger
    banner("W  THE LEDGER")
    LEDGER = [
        ("X22f", f"the chain's gamma_hat under the frozen statistic: {PREC['canonical']['top']:.4f} (canonical) / {PREC['alt']['top']:.4f} (alt) at the "
                 "Solar-System floor of xi, falling to 1.000 as xi grows: a CEILING, not a point", "DERIVED", "V1 (PHYS; REG reported alongside)"),
        ("X22g", "the frozen pre-registration registers no reading for this law (Arm A: no filter, Route A; Arm B: carrier + biharmonic cone); "
                 "its rows only place the number", "CONSTRAINT", "P"),
        ("X22h", "the frozen number cannot fix xi (at best a bound); the transition (s ~ 2 xi, inside 2-30 kAU at the floor) needs a "
                 "separation-resolved statistic", "DERIVED", "H4, H5"),
        ("X22i", "BDEF's Galileon (FP17's reduction, ESTIMATE, not adopted) is not separable from the heat filter by the frozen number", "DERIVED", "H8, H9"),
        ("X22j", "an amendment registering the chain's ceiling and a separation-resolved xi statistic would be needed for DR4 to test the chain "
                 "on its own terms; the author decides", "OPEN", "the verdict"),
    ]
    for k_, what, st_, why in LEDGER:
        P_(f"    {k_:6s} {st_:11s} {what}  --  {why}")
    OUT["ledger"] = [dict(link=k_, what=w_, status=s_, basis=b_) for k_, w_, s_, b_ in LEDGER]
    n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
    OUT["verdict"] = dict(n_checks=len(CH), n_fail_load_bearing=n_fail, wall_s=time.time() - T0)
    with open(JSN, "w") as fh:
        json.dump(OUT, fh, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    rc = 0 if n_fail == 0 else 1
    P_(f"\n  {len(CH) - sum(1 for _, ok, _l in CH if not ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote "
       f"{os.path.basename(JSN)}  ({time.time() - T0:.0f} s)")
    P_(f"rc = {rc}")
    sys.stdout.flush()
    sys.stdout = sys.__stdout__
    return rc


if __name__ == "__main__":
    sys.exit(main())
