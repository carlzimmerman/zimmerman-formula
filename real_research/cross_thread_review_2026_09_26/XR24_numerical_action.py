#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR24 -- THE LOCAL GROUP'S HUBBLE FLOW IN 3-D, IN THE CHAIN'S LAW: a numerical-action reconstruction of the Local Group and its
surroundings to ~5 Mpc.  Does the full 3-D flow (the neighbours' tides and the MOND non-linearity included) resolve or confirm
the chain's most persistent failure, the Local Group's zero-velocity radius R0?  Cross-thread review lane (2026-09-27).

WHY.  FP11 (committed): in the chain's law the MW-M31 timing works with baryons only on the first approach, a past flyby is
excluded, and R0 overshoots, 1.52-1.57 Mpc against 0.96 +- 0.03 (+0.20 dex; FP18: honest error +-0.11).  FP13's state
separator H_S keeps both (timing masses 1.50e11 / 1.26e11, R0 1.54 Mpc).  FP12: the LG, M81 and IC 342 share the +0.20 dex
offset, Cen A matches.  FP11's open item F11m lists the neighbours' tidal field, the CGM's baryons and 'a 3-D fit of the full
local Hubble flow'.  This lane is that fit.

THE LAW (nothing added).  FP7's AQUAL-type root with FP13's headline state separator H_S: the band-pass length L(z) set by the
matter field's collapse scale (delta_c on the actual field) and the yield y_th = the web's band-passed rms x max(0, 2q) (on
while the universe decelerates, z > 0.635); FP13's own code is exec'd read-only for the tables (K7 reproduces its committed
L(z), y_th(z) exactly).  Both a0 footings: 9.3603e-11 (canonical) and 1.1312e-10 m/s^2 (alt) (FP0).
THE FORCE (labelled): the chain's static law in QUMOND form, as FP11 used it -- g = g_N + P (1 - S_L) X(g_bp), g_bp = (1 - S_L)
g_N, X(g) = a0 x_P2(|g|/a0 - y_th) g/|g| -- solved in 3-D for ALL bodies at once (it is not pairwise additive): each body's
isolated band-passed phantom exactly (FP6's phantom()), the MW-M31 pair's interaction exactly (FP11's two-body tables,
live), and the rest of the interaction field P(1 - S_L)[X(sum g_j) - sum X(g_j)] by (i) a direct 3-D integral of the band-
passed dipole kernel at every body (this lane's closed form; the axisymmetric limit is FP11's dg_body) and (ii) a spherical-
harmonic finite-volume solver on a 3-D grid about the Local Group (FP11's multipole solver generalised to l, m) for the test
particles.  The AQUAL-vs-QUMOND curl difference is not computed (FP7 A3: <= 0.035 dex on discs; FP11 idem).
THE NUMERICAL ACTION (labelled): Peebles' boundary conditions -- today's positions (sky positions and distances) and the
growing mode at early times (zero peculiar velocity on the Hubble flow at a = 0.02, FP11's convention) -- solved by Newton
shooting on the comoving initial positions (finite-difference Jacobian, Broyden, line search), not by the action's own
discretisation; the bodies' interaction history is iterated to self-consistency (Picard); every test-particle solution
(each observed dwarf) is found from Lagrangian seeds, all branches kept.
THE BACKGROUND CONVENTION.  FP11's headline convention A (point masses + Lambda, no background matter) cannot host a
multi-body Local Volume: with no smooth matter the region coasts (a free particle today sits at 4.18x its comoving start),
so the eleven bodies start within ~20 kpc of each other at z = 49 and the first-approach problem has no tractable solution
(exploratory run, disclosed).  The headline here is FP11's convention B (the smooth cosmic background's deceleration -- in
the chain, the dark fluid, smooth at early times and, after FP16's kick, spread through the field: FP16 L16b/L16g say
galaxies <= 1e13 Msun do not keep it), for which FP11 committed numbers too (K1 reproduces them); convention A is run as a
variant only for the pair (below).  For LCDM, convention B double-counts the halos on top of the full background (a 4.7e12 point
mass on the mean density is a delta ~ 0.6 perturbation at z = 49: the neighbours fall into the LG), and convention A with halo-
mass neighbours did not converge with this solver either (exploratory runs, disclosed) -- so the matched flow comparison is
made where both laws are tractable and matched: the MW-M31 pair alone with the dwarfs as test particles, convention A
(FP11's headline for the chain; Partridge, Lahav & Hoffman's for LCDM).
BODIES (baryonic only).  MW: stars 6.08e10 (Licquia & Newman 2015) + HI x 1.33 (UNGC); M31: 1.03e11 (Sick+2015) + HI x 1.33;
M33 (4.8e9, Corbelli+2014, + HI x 1.33) merged into M31 (a satellite 0.2 Mpc away: its orbit is not a Hubble-flow problem;
exploratory runs as a separate body made the BVP chaotic, disclosed); MW-M31 separation 0.78 Mpc (FP11).  The neighbours as
merged group points at their main galaxies with FP12's k02 UNGC baryons (M81 9.62e10, Cen A 9.02e10, M83 5.76e10, IC 342
1.03e11 incl. Maffei 1/2) and, by the same recipe (0.6 L_K + 1.33 M_HI inside 0.7 Mpc), NGC 253 (7.1e10), NGC 4736 (3.4e10),
NGC 4826 (1.9e10), Circinus (2.7e10).  The LG's baryons carry one scale s (the fit parameter; window [1.22e11, 2.48e11] =
FP11's MW+M31 window + M33); the CGM range [0, 9.8e10] per L* galaxy (Bregman+2022 tSZ within 250 kpc, as the committed
L45 lane reads it) is a statement about that window.  The dark fluid: not added (FP16: galaxies do not keep it).
DATA.  The UNGC (Karachentsev+2013, committed): the flow sample is FP11's section-D selection (32 galaxies at 0.7-3 Mpc from
the LG barycentre, accurate distances, other groups' members excluded); heliocentric velocities to Galactocentric with
van der Marel+2012's solar parameters (R0 8.29 kpc, V0 239 km/s, (11.1, 12.24, 7.25) km/s; read at source); MW-M31
v_r = -109.3 +- 4.4 km/s, v_t = 17 (<34), 57 (+35/-31), 82 +- 31 km/s (FP11's sources).  chi^2 per galaxy with sigma^2 =
25^2 (unmodelled dispersion, stated) + 5^2 (velocity) + (70 km/s/Mpc x 5% D)^2 (distance); the best branch per galaxy (the
NAM convention), the same rule for both laws.  R0: the published 0.96 +- 0.03 (Karachentsev+2009) with FP18's honest
+-0.11; the chain's +0.10 dex band (1.21 Mpc).
THE LCDM CONTROL (matched): the same numerical action, the MW-M31 pair as Newtonian point masses with the LG halo mass
M_LG = f x M_b (f scanned, fitted), the same 32 dwarfs as test particles, convention A; the chain's matched counterpart is the
pair alone in convention A at its own timing mass.  Benchmark for the two-body limit: Partridge, Lahav & Hoffman 2013 (MNRAS
436, L45; read at source): M_TA,Lambda = (4.73 +- 1.03)e12 Msun from r = 770 kpc, v = -109.3 km/s, Planck (their radial
Lambda timing = FP11's convention A).  The neighbours' LCDM halos are not in the control (not tractable here; stated).

CHECKS.  K1 FP11's committed timing (H_Y; conventions A, B; both footings) and convention-B two-body R0 reproduced exactly with
FP11's module; K2 FP13's committed H_S L-section points exactly (FP11's machinery hooked, FP13's hook11); K3 this lane's N-body
integrator and BVP in the two-body limit = FP11's committed branch; K4 the 3-D field solver (direct kernel vs FP11's dg_body;
the grid; the N-body deep-MOND virial identity, momentum; the pairwise superposition fails); K5 the 3-D test-particle
machinery on the pair alone = FP11's committed B R0 and rays; K6 the LCDM benchmark (PLH13); K7 FP13's committed H_S tables.
T1 [load-bearing; MUTATE must fail] the 3-D first-approach timing inside the baryonic window, both footings; T2 (reported) the
3-D vs the two-body timing mass.  O1 (reported) the MW-M31 orbit (pericentres, the tidal v_t).  R1 [load-bearing] the 3-D R0
at the timing mass stays above 1.21 Mpc (a verified FAIL of the chain's LG); R2 (reported) the neighbours' shift of R0
(removes / reduces / confirms).  F1 [load-bearing] the chain's joint chi^2 (pair alone, convention A, at its timing mass)
exceeds the matched LCDM control's minimum by >= 9 on both footings; F2 (reported) LCDM's own tension (its flow-preferred mass
against its timing mass; its R0 at its timing mass); F3 (reported) the chain's flow in 3-D with the neighbours.  E1 (reported) the published linear estimator on the model and the data.  V1
(reported) variants.  C1 (reported) the CGM room.  G1 the other gates unchanged.  W the ledger.
MUTATE=1 scores FP7's plain P2 root law (no band-pass, no yield) in the 3-D timing scan over the window -- the pair in the 3-D
machinery (with the neighbours the plain law's untruncated MOND made the ten-body problem intractable: an exploratory MUTATE
run was stopped after 40 min without one converged scan, disclosed): its first approach is too fast at every window mass
(FP11's F11e), so T1 must FAIL (rc = 1); the sections that need a timing solution are not run.
Run from the repository root (4 worker processes, ~1 h; MUTATE ~20 min):
    python3 real_research/cross_thread_review_2026_09_26/XR24_numerical_action.py   (MUTATE=1 for the control)

HISTORY (stated, not hidden).  Exploratory runs before the committed ones: (1) M33 as its own body made the ten-body BVP chaotic
(it fell through M31) -> merged; (2) convention A with the neighbours: no convergence (bodies packed at z = 49) -> B headline;
(3) one end-to-end chain configuration (H_S, canonical, B, s = 0.85, neighbours on: v_r -111.8, R0 1.62 Mpc, flow chi^2 295/32)
-- the first chain-law 3-D numbers seen; (4) LCDM with halo-mass neighbours in B (f = 27) and A (f = 22, 8), and with light
neighbours in B: no convergence -> the LCDM control was redesigned as the matched pair-alone comparison in convention A BEFORE
any LCDM chi^2 was computed (the F1 threshold and direction are unchanged); (5) a MUTATE run with the neighbours was stopped
after 40 min without a converged scan -> MUTATE scans the pair.  No check direction or threshold was changed after a scored run.

HYPOTHESES (pre-declared in the scratch record before any 3-D chain-law number was computed; the checks score them as they
fall): T1 [MUTATE must fail] the 3-D first-approach timing works inside the window on both footings; R1 the 3-D R0 at the
timing mass stays above 1.21 Mpc on both footings; R2 (classification) CONFIRMS: the neighbours move R0 by < 0.03 dex;
F1 the chain's flow chi^2 at its timing mass exceeds the LCDM control's best by >= 9 on both footings.
"""
import os, sys, io, json, math, time, contextlib, warnings, traceback
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import XR24_common as X                                                          # noqa: E402

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR24_numerical_action"
NPROC = 4
FOOTS = ("canonical", "alt")
SCORED = "P2" if MUTATE else "HS"
NB_NOM = 1.8224e11                                                               # MW + M31 + M33 baryons (stars + HI x 1.33), s = 1
WIN = (1.145e11 + 7.58e9, 2.4e11 + 7.58e9)                                       # FP11's MW+M31 window + M33 [Msun]
CGM_MAX = 9.8e10                                                                 # per L* galaxy (Bregman+2022 tSZ, 250 kpc; L45)
R0_MEAS, R0_ERR, R0_HONEST, EDGE = 0.96, 0.03, 0.111, 0.96 * 10 ** 0.10
S_SCAN = {"canonical": (0.62, 0.74, 0.86, 1.0), "alt": (0.52, 0.62, 0.74, 0.86)}
S_SCAN_A = {"canonical": (0.70, 0.80, 0.90, 1.0), "alt": (0.60, 0.70, 0.80, 0.90)}
S_MUT = (0.67, 1.0, 1.36)
F_LCDM = (4.0, 6.0, 9.0, 13.0, 19.0, 27.0)
F11J = json.load(open(os.path.join(X.DC, "FP11_local_group_flyby_results.json")))["numbers"]
F13J = json.load(open(os.path.join(X.DC, "FP13_separator_from_state_results.json")))["numbers"]
OUT = {"lane": "XR24", "mutate": MUTATE, "checks": {}, "numbers": {}, "ledger": []}
CH = []
T0 = time.time()


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)


def check(name, measured, ok, load_bearing=True, reading=None):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing, "name": name}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def el():
    return f"[{time.time() - T0:.0f} s]"


# ================================================================================================= pool jobs (top level)
def job_config(cfg):
    t = time.time()
    try:
        out = X.run_config(cfg, do_tracers=cfg.get("tracers", True), nstep_b=2000, nstep_t=2000)
        out["chi2"] = X.chi2_flow(out) if "dwarfs" in out else None
        out["chi2_35"] = X.chi2_flow(out, sig_th=35e3) if "dwarfs" in out else None
        out["chi2_slope"] = X.chi2_flow(out, dist_term="model") if "dwarfs" in out else None
        return cfg["tag"], out, time.time() - t
    except Exception:
        return cfg["tag"], {"error": traceback.format_exc()}, time.time() - t


def job_fp11_timing(cfg):
    t = time.time(); c, out, _ = X.F11.job_timing(cfg); return cfg, out, time.time() - t


def job_fp11_matched(cfg):
    t = time.time(); name, out, _ = X.F11.job_matched(cfg); return name, out, time.time() - t


def job_hs_pair(cfg):
    """FP11's committed two-body machinery hooked to H_S (FP13's hook11 in effect): the pair's first-approach v_r (conv A/B)."""
    foot, Mb, conv = cfg; t = time.time(); law = X.Law("HS", foot); F = X.F11
    oL, oy = F.L_of_a, F.yth_of_a
    F.L_of_a = lambda a, bp=True, LL=None: (law.L(a) if bp else None)
    F.yth_of_a = lambda a, yl=True: (law.yth(a) if yl else None)
    try:
        m1, m2 = F.FMW * Mb * X.MSUN, (1 - F.FMW) * Mb * X.MSUN
        dg, ln_, T = F.force_table(m1, m2, X.A0[foot], True, True)
        br = [b for b in F.branches(F.Acc(dg, ln_, T, m1 + m2), bg=(conv == "B")) if b["k"] == 0 and b["vr"] < 0]
    finally:
        F.L_of_a, F.yth_of_a = oL, oy
    return cfg, (br[0]["vr"] if br else float("nan")), time.time() - t


def job_pair3d_R0(cfg):
    """the 3-D machinery on the MW-M31 pair alone (H_Y, convention B, FP11's committed B timing mass, a tilted axis): R0 rays."""
    foot, Mb, conv = cfg; t = time.time(); F = X.F11
    law = X.Law("HY", foot); m1, m2 = F.FMW * Mb * X.MSUN, (1 - F.FMW) * Mb * X.MSUN
    sysm = X.System([m1, m2], law, live_pairs=[(0, 1)], conv=conv)
    zdir = np.array([0.3, -0.5, 0.81]); zdir /= np.linalg.norm(zdir); d0 = 0.78 * X.MPC
    Xobs = np.array([-(1 - F.FMW) * d0 * zdir, F.FMW * d0 * zdir])
    ri, br = X.pair_seed(sysm, 0, 1, d0)
    Q0 = np.array([-(1 - F.FMW) * ri / 0.02 * zdir, F.FMW * ri / 0.02 * zdir])
    res = X.solve_bodies(sysm, Xobs, Q0, X.LNAT, nstep=8000, maxpicard=1)
    grid = X.Grid3(rmin_kpc=2.0, rmax_kpc=40000.0, nr=180, nth=64, nph=96, lmax=40); rot = X.rot_to(zdir)
    Fg, C = X.grid_tables(sysm, res["lna_s"], res["Xs"], X.LNAT, grid, rot, lg=(0, 1))
    tr = X.Tracers(sysm, grid, rot, X.LNAT, Fg, C)
    cs, ws = np.polynomial.legendre.leggauss(8); th = np.arccos(cs); nph = 4
    dirs = np.array([[math.sin(a) * math.cos(p), math.sin(a) * math.sin(p), math.cos(a)] for a in th
                     for p in (np.arange(nph) + 0.5) * 2 * math.pi / nph]) @ rot.T
    R0, data, _ = X.R0_rays_3d(tr, res["Q"], np.array([m1, m2]), dirs, lg=(0, 1), n0=48, nins=10, nstep=3000,
                                rho_hi=(4.0 if conv == "A" else 12.5) * X.MPC)
    R0t = np.nanmean(R0.reshape(8, nph), axis=1)
    Xf, Vf = res["X"], res["V"]; dx = Xf[1] - Xf[0]; dv = Vf[1] - Vf[0]
    return cfg, dict(rays=R0t.tolist(), mean=float(np.sum(ws * R0t) / np.sum(ws)), vr=float(dx @ dv / np.linalg.norm(dx) / 1e3),
                     phi_spread=float(np.nanmax(np.nanstd(R0.reshape(8, nph), axis=1)))), time.time() - t


# ================================================================================================= helpers
def interp_s(pts, target=-109.3):
    """pts [(s, v_r)] -> s where v_r = target (linear in ln s), None if not bracketed."""
    pts = sorted((s, v) for s, v in pts if v == v)
    for (s1, v1), (s2, v2) in zip(pts[:-1], pts[1:]):
        if (v1 - target) * (v2 - target) <= 0 and v1 != v2:
            return float(math.exp(math.log(s1) + (target - v1) / (v2 - v1) * (math.log(s2) - math.log(s1))))
    return None


def ests(out, dd, f31=0.63):
    """the linear-fit estimator V = H (R - R0) over 0.7-3 Mpc (FP11 R4 / K09 / k02) on the model's predicted LG-frame
    velocities at the observed galaxies, with the data's own geometry (FP11's barycentre and projection)."""
    name2i = {n: i for i, n in enumerate(dd["name"])}
    R, Vm, Vd = [], [], []
    for r in out["dwarfs"]:
        if r["best"] is None:
            continue
        i = name2i[r["name"]]; fac = dd["Vr"][i] / dd["V"][i] if dd["V"][i] != 0 else float("nan")
        R.append(dd["R"][i]); Vm.append((r["best"]["vgsr"] + r["vlg_shift"]) * fac); Vd.append(dd["Vr"][i])
    R, Vm, Vd = map(np.array, (R, Vm, Vd))
    fm, fd = X.F11.lin_fit(R, Vm), X.F11.lin_fit(R, Vd)
    return dict(model=fm, data=fd)


# ================================================================================================= main
def main():
    from multiprocessing import Pool
    P(__doc__.split("HYPOTHESES")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: the SCORED law loses the separator (FP7's plain P2 root law, no band-pass, no yield); T1 must FAIL; the "
          "flow, R0 and LCDM sections (which need a timing solution) are not run ***")
    pool = Pool(NPROC)
    # ---------------------------------------------------------------------------------------------- phase 1: queue everything independent
    J = {}
    J["K1t"] = [pool.apply_async(job_fp11_timing, (("HY", f, Mb, ("A", "B")),)) for f in FOOTS for Mb in (1.145e11, 1.45e11, 1.75e11)]
    MB_B = F11J["timing_mass"]["HY/canonical/B/0"]["M"]
    J["K1m"] = pool.apply_async(job_fp11_matched, (("HY/B/canonical", "HY", "canonical", MB_B, "B", 0, dict(tracers=True)),))
    J["K2"] = [pool.apply_async(job_hs_pair, ((f, 1.45e11, "A"),)) for f in FOOTS]
    J["K5"] = pool.apply_async(job_pair3d_R0, (("canonical", MB_B, "B"),))
    scan_law = SCORED; svals = {f: (S_MUT if MUTATE else S_SCAN[f]) for f in FOOTS}
    J["scan"] = {(f, s): pool.apply_async(job_config, (dict(tag=f"{scan_law}-{f}-s{s:.3f}-B-scan", law=scan_law, foot=f, s_lg=s, conv="B",
                                                              nb=not MUTATE, tracers=False),)) for f in FOOTS for s in svals[f]}
    J["pairB"] = {(f, s): pool.apply_async(job_hs_pair, ((f, s * NB_NOM, "B"),)) for f in FOOTS for s in svals[f]} if not MUTATE else {}
    J["pairA"] = {(f, s): pool.apply_async(job_hs_pair, ((f, s * NB_NOM, "A"),)) for f in FOOTS for s in S_SCAN_A[f]} if not MUTATE else {}
    P(f"\n  phase 1 queued: FP11/FP13 reproductions, the pair's 3-D R0, the {scan_law} 3-D timing scans (bodies only)  {el()}")

    # ---------------------------------------------------------------------------------------------- serial controls (main process)
    banner("K  CONTROLS: the reused machinery reproduces the record; the 3-D field solver; the LCDM benchmark")
    hs = X.hs_tables(); fun = hs["fun_of"](hs["LH"]); lawc = X.Law("HS", "canonical")
    dL = max(abs(1e3 * fun(1 / (1 + float(z))) / v - 1) for z, v in F13J["H1"]["L_kpc"].items())
    dy = max(abs(lawc.yth(1 / (1 + float(z))) - v) for z, v in F13J["H1"]["yth"].items())
    check("K7 CONTROL: FP13's code (exec'd read-only) returns its committed headline H_S tables -- L(z) at 7 redshifts and y_th(z) at "
          "8 (canonical) -- exactly; the law used below is FP13's", f"max |L/L_committed - 1| {dL:.1e}; max |y_th - committed| {dy:.1e}; "
          f"q = 0 at z = {hs['z_q0']:.4f}", dL < 1e-12 and dy < 1e-15)

    # K4: the 3-D field solver
    a0c = X.A0["canonical"]; FMW = X.F11.FMW; k4a, k4b = [], []
    grid = X.Grid3(rmin_kpc=2.0, rmax_kpc=40000.0, nr=180, nth=64, nph=96, lmax=40)
    for (dm, a) in ((0.78, 1.0), (0.9, 0.667), (0.2, 0.5), (0.78, 0.8)):
        d = dm * X.MPC; Lm = X.F11.L_of_a(a); yt = X.F11.yth_of_a(a); m1, m2 = FMW * 1.75e11 * X.MSUN, (1 - FMW) * 1.75e11 * X.MSUN
        r1 = X.F11.dg_body(m1, m2, d, a0c, Lm, yt, ns=400); r2 = X.F11.dg_body(m2, m1, d, a0c, Lm, yt, ns=400)
        g1 = X.direct_W_at([(m1, np.zeros(3)), (m2, np.array([0, 0, -d]))], 0, a0c, Lm, yt, ns=200, nmu=64, nphi=32)
        g2 = X.direct_W_at([(m2, np.zeros(3)), (m1, np.array([0, 0, -d]))], 0, a0c, Lm, yt, ns=200, nmu=64, nphi=32)
        k4a.append((dm, a, g1[2] / r1, g2[2] / r2))
        if dm != 0.78 or a == 1.0:
            zdir = np.array([0.3, -0.5, 0.81]); zdir /= np.linalg.norm(zdir); x1 = -(1 - FMW) * d * zdir; x2 = FMW * d * zdir
            rot = X.rot_to(np.array([1.0, 0.2, 0.1])); bod = [(m1, x1), (m2, x2)]
            Fq = grid.field(grid.divergence(lambda Pp: X.W_field(Pp, bod, a0c, Lm, yt), np.zeros(3), rot), Lm)
            gw = grid.interp(Fq, np.array([rot.T @ x1, rot.T @ x2])) @ rot.T
            k4b.append((dm, a, (gw[0] @ zdir) / (-r1), (gw[1] @ -zdir) / (-r2)))
    Ms = np.array([1.0e11, 0.5e11, 0.8e11]) * X.MSUN; vir = {}
    for sc in (1.0, 3.0):
        Xb = np.array([[0.0, 0.0, 0.0], [1.0, 0.3, 0.0], [-0.4, 1.2, 0.5]]) * X.MPC * sc; bod = [(Ms[i], Xb[i]) for i in range(3)]
        def tot(W_on):
            gs = []
            for i in range(3):
                g = np.zeros(3)
                for j in range(3):
                    if j == i: continue
                    dv_ = Xb[j] - Xb[i]; r = np.linalg.norm(dv_)
                    Mph = X.phantom(Ms[j], a0c, None, None, 4); g += (X.G * Ms[j] / r ** 2 + X.G * np.interp(r, X.RG, Mph) / r ** 2) * dv_ / r
                if W_on:
                    g += X.direct_W_at(bod, i, a0c, None, None, ns=200, nmu=64, nphi=64)
                gs.append(g)
            return np.array(gs)
        gs1, gs0 = tot(True), tot(False)
        Vd = -(2 / 3) * math.sqrt(X.G * a0c) * (Ms.sum() ** 1.5 - (Ms ** 1.5).sum())
        vir[sc] = dict(ratio=float(sum(Ms[i] * Xb[i] @ gs1[i] for i in range(3)) / Vd), pairwise=float(sum(Ms[i] * Xb[i] @ gs0[i] for i in range(3)) / Vd),
                       mom=float(np.linalg.norm((Ms[:, None] * gs1).sum(0)) / np.abs(Ms[:, None] * gs1).sum()),
                       mom_pair=float(np.linalg.norm((Ms[:, None] * gs0).sum(0)) / np.abs(Ms[:, None] * gs0).sum()))
    ok4 = (max(max(abs(r1 - 1), abs(r2 - 1)) for _, _, r1, r2 in k4a) < 1e-3 and max(max(abs(r1 - 1), abs(r2 - 1)) for _, _, r1, r2 in k4b) < 0.025
           and all(abs(v["ratio"] - 1) < 0.01 and v["mom"] < 1e-3 and v["pairwise"] > 1.5 for v in vir.values()))
    check("K4 CONTROL (the 3-D field solver of the chain's static law): (a) the direct 3-D integral of the band-passed dipole kernel equals "
          "FP11's committed axisymmetric dg_body at both bodies of the MW-M31 pair (4 cells with band-pass and yield); (b) the spherical-"
          "harmonic grid solver (180 x 64 x 96, l <= 40, a tilted axis) equals it within 2.5%; (c) three bodies, deep MOND: the N-body "
          "virial identity sum m x.g = -(2/3) sqrt(G a0)[(sum m)^1.5 - sum m^1.5] and momentum conservation hold, and the pairwise "
          "superposition (no interaction field) violates the identity by > 50% -- the non-additive part is computed, not approximated",
          "(a) " + ", ".join(f"({d_:g},{a_:g}): {r1:.5f}/{r2:.5f}" for d_, a_, r1, r2 in k4a) + "; (b) " + ", ".join(f"({d_:g},{a_:g}): {r1:.4f}/{r2:.4f}" for d_, a_, r1, r2 in k4b)
          + "; (c) " + ", ".join(f"scale {k_}: virial {v['ratio']:.4f} (pairwise {v['pairwise']:.3f}), |sum m g|/sum|m g| {v['mom']:.1e} (pairwise {v['mom_pair']:.1e})" for k_, v in vir.items()), ok4)
    OUT["numbers"]["K4"] = dict(direct=k4a, grid=k4b, virial={str(k_): v for k_, v in vir.items()})

    # K3: the N-body integrator in the two-body limit = FP11's shooter; the BVP finds FP11's committed branch (convention B)
    lawy = X.Law("HY", "canonical"); m1, m2 = FMW * MB_B * X.MSUN, (1 - FMW) * MB_B * X.MSUN
    s2 = X.System([m1, m2], lawy, live_pairs=[(0, 1)], conv="B"); brc = F11J["matched"]["HY/B/canonical"]["branch"]
    ri = brc["ri_kpc"] * X.KPC; Qi = np.array([[[0, 0, -(1 - FMW) * ri / 0.02], [0, 0, FMW * ri / 0.02]]])
    Xa, Va = s2.integrate(Qi, nstep=8000); dx = Xa[0, 1] - Xa[0, 0]; dv_ = Va[0, 1] - Va[0, 0]; vr_mine = float(dx @ dv_ / np.linalg.norm(dx) / 1e3)
    d0 = 0.78 * X.MPC; Xo = np.array([[0, 0, -(1 - FMW) * d0], [0, 0, FMW * d0]])
    sol = X.solve_bvp(s2, Xo, Qi[0], nstep=8000); dx = sol["X"][1] - sol["X"][0]; dv_ = sol["V"][1] - sol["V"][0]
    vr_bvp = float(dx @ dv_ / np.linalg.norm(dx) / 1e3)
    check("K3 CONTROL: this lane's N-body integrator in the two-body limit, started from FP11's committed convention-B branch at FP11's "
          "committed B timing mass, returns FP11's committed velocity (the same ODE); its numerical-action BVP (positions today = 0.78 "
          "Mpc, growing mode at a = 0.02) returns the same branch", f"integrator {vr_mine:.6f} vs committed {brc['vr']:.6f} km/s "
          f"(d {np.linalg.norm(Xa[0,1]-Xa[0,0])/X.MPC:.9f}); BVP {vr_bvp:.4f} km/s at d = 0.78 exactly, residual {sol['res']:.1e} Mpc",
          abs(vr_mine - brc["vr"]) < 1e-6 and abs(vr_bvp - brc["vr"]) < 0.02)

    # K6: the LCDM benchmark (radial Lambda timing, point masses + Lambda: FP11's convention A = PLH13's method)
    def vr_newton(Mt, d_mpc):
        T = X.G * Mt * X.MSUN / X.DGRID[None, :] ** 2 * np.ones((len(X.LNAT), 1)); acc = X.F11.Acc(X.DGRID, X.LNAT, T, Mt * X.MSUN)
        br = [b for b in X.F11.branches(acc, D0=d_mpc * X.MPC) if b["k"] == 0 and b["vr"] < 0]; return br[0]["vr"] if br else float("nan")
    pts6 = [(M_, vr_newton(M_, 0.77)) for M_ in (3.0e12, 4.0e12, 4.5e12, 5.0e12, 5.5e12, 6.5e12)]
    Mt6 = X.F11.timing_mass(pts6, -109.3)
    check("K6 CONTROL (LCDM benchmark): the radial Lambda timing with point masses + Lambda from the Hubble flow at a = 0.02 (FP11's "
          "convention A), r = 0.77 Mpc and v = -109.3 km/s (the inputs of Partridge, Lahav & Hoffman 2013, MNRAS 436, L45), recovers "
          "their M_TA,Lambda = (4.73 +- 1.03)e12 Msun within the quoted error", ", ".join(f"{M_:.1e}: {v:+.1f}" for M_, v in pts6)
          + f" -> {Mt6:.3e} Msun (t0 = {X.F11.T0_AGE / X.GYR:.2f} Gyr, Planck-2018 h = 0.674 vs their 13.81 Gyr, h = 0.674)",
          Mt6 is not None and abs(Mt6 - 4.73e12) < 1.03e12)
    OUT["numbers"]["K6"] = dict(pts=pts6, M=Mt6)
    P(f"    {el()}")

    # ---------------------------------------------------------------------------------------------- collect phase-1 controls
    k1 = []
    for a_ in J["K1t"]:
        cfg, out, dt = a_.get(); key = f"HY/{cfg[1]}/{cfg[2]:.3e}"; ref = F11J["timing_scan"][key]
        for cv in ("A", "B"):
            v = [b["vr"] for b in out[cv] if b["k"] == 0 and b["vr"] < 0][0]; vref = [b["vr"] for b in ref[cv] if b["k"] == 0 and b["vr"] < 0][0]
            k1.append((key, cv, v, vref))
    name, outm, dt = J["K1m"].get(); refm = F11J["matched"]["HY/B/canonical"]
    dR = abs(outm["R0"]["mean"] / refm["R0"]["mean"] - 1)
    check("K1 CONTROL: FP11's committed machinery (its module, main() not run) reproduces its committed first-approach velocities (H_Y, "
          "conventions A and B, both footings, three masses) and its committed convention-B two-body zero-velocity radius at its B "
          "timing mass exactly", "max |v_r - committed| " + f"{max(abs(v - r) for _, _, v, r in k1):.1e} km/s over {len(k1)} points; R0(HY/B/canonical) "
          f"{outm['R0']['mean']:.6f} vs {refm['R0']['mean']:.6f} Mpc", max(abs(v - r) for _, _, v, r in k1) < 1e-9 and dR < 1e-9)
    k2 = []
    for a_ in J["K2"]:
        cfg, v, dt = a_.get(); ref = [p for p in F13J["L"]["pts"][cfg[0]] if abs(p[0] - cfg[1]) < 1e6][0][1]; k2.append((cfg[0], v, ref))
    check("K2 CONTROL: FP11's two-body machinery hooked to FP13's H_S (FP13's hook11 in effect) reproduces FP13's committed L-section "
          "first-approach velocities (convention A, M_b = 1.45e11, both footings) exactly -- the H_S used here is FP13's",
          "; ".join(f"{f}: {v:.10f} vs {r:.10f}" for f, v, r in k2), all(abs(v - r) < 1e-9 for _, v, r in k2))
    cfg, r5, dt = J["K5"].get(); rays_ref = refm["R0"]["rays"]
    dray = max(abs(a_ / b_ - 1) for a_, b_ in zip(r5["rays"], rays_ref))
    check("K5 CONTROL: the 3-D test-particle machinery (the grid solver's interaction field, tracers on rays in 3-D, a tilted axis, "
          "4 azimuths per polar ray) on the MW-M31 pair alone at FP11's committed convention-B timing mass reproduces FP11's committed "
          "two-body zero-velocity radius and its eight rays", f"mean {r5['mean']:.4f} vs {refm['R0']['mean']:.4f} Mpc ({r5['mean'] / refm['R0']['mean'] - 1:+.4f}); "
          f"max ray deviation {dray:.4f}; azimuthal spread {r5['phi_spread']:.1e} Mpc; pair v_r {r5['vr']:.3f} km/s", abs(r5["mean"] / refm["R0"]["mean"] - 1) < 0.01 and dray < 0.02)
    OUT["numbers"]["K"] = dict(K1=k1, K1R0=[outm["R0"]["mean"], refm["R0"]["mean"]], K2=k2, K5=r5)
    P(f"    {el()}")

    # ---------------------------------------------------------------------------------------------- T: the 3-D timing
    banner(f"T  THE MW-M31 TIMING IN 3-D ({'plain P2 root law, MUTATE; the pair in the 3-D machinery' if MUTATE else 'the chain law, FP7 root + FP13 H_S; neighbours on'}; convention B)")
    scan = {}
    for (f, s), a_ in J["scan"].items():
        tag, out, dt = a_.get(); scan[(f, s)] = out
        if "error" in out:
            P(f"    {tag}: ERROR {out['error'][-300:]}"); continue
        pr = out["pair"]
        P(f"    {tag}: M_LG {s * NB_NOM:.3e}: v_r {pr['vr']:+.2f} km/s, v_t {pr['vt']:.1f}; d_max {pr['dmax']:.3f} Mpc at z = {pr['z_dmax']:.2f}; "
          f"pericentres {pr['peri']}  [{dt:.0f}s]")
    pairB = {}
    for (f, s), a_ in J["pairB"].items():
        cfg, v, dt = a_.get(); pairB[(f, s)] = v
    stA = {f: interp_s([(s, J["pairA"][(f, s)].get()[1]) for s in S_SCAN_A[f]]) for f in FOOTS} if not MUTATE else {}
    st, st2 = {}, {}
    for f in FOOTS:
        pts = [(s, scan[(f, s)]["pair"]["vr"]) for s in svals[f] if "pair" in scan.get((f, s), {}) and not scan[(f, s)]["pair"]["peri"]]
        st[f] = interp_s(pts); st2[f] = interp_s([(s, pairB[(f, s)]) for s in svals[f] if (f, s) in pairB]) if pairB else None
    inw = lambda s: s is not None and WIN[0] <= s * NB_NOM <= WIN[1]
    OUT["numbers"]["T"] = dict(scan={f"{f}/{s}": scan[(f, s)].get("pair") for (f, s) in scan}, s_timing=st, s_timing_twobody=st2,
                               pairB={f"{f}/{s}": v for (f, s), v in pairB.items()})
    check(f"T1 THE 3-D FIRST-APPROACH TIMING WORKS WITH BARYONS ONLY: in 3-D {'(MUTATE: the pair in the 3-D machinery)' if MUTATE else 'with the neighbours'}, the {'plain root law (MUTATE)' if MUTATE else 'chain law'} "
          "reaches the MW-M31 v_r = -109.3 km/s on the FIRST approach (no pericentre since a = 0.02) at an LG baryonic mass inside the "
          f"window [{WIN[0]:.3e}, {WIN[1]:.3e}] Msun, both footings",
          "; ".join(f"{f}: " + ", ".join(f"s {s}: {scan[(f, s)]['pair']['vr']:+.1f}" for s in svals[f] if "pair" in scan.get((f, s), {}))
                    + (f" -> M_t = {st[f] * NB_NOM:.3e}" if st[f] else " -> not bracketed") for f in FOOTS), all(inw(st[f]) for f in FOOTS))
    if MUTATE:
        finish(pool); return
    check("T2 (reported) THE 3-D TIMING MASS AGAINST THE TWO-BODY ONE (the same law and convention, FP11's machinery hooked to H_S, "
          "the pair alone): the neighbours' effect on the timing", "; ".join(f"{f}: 3-D {st[f] * NB_NOM:.3e} vs two-body {st2[f] * NB_NOM:.3e} Msun "
                                                                          f"({st[f] / st2[f] - 1:+.3f})" for f in FOOTS if st[f] and st2[f]), True, load_bearing=False)

    # ---------------------------------------------------------------------------------------------- phase 2: the full configurations
    FULL = {}
    for f in FOOTS:
        FULL[f"HS-{f}-t"] = dict(law="HS", foot=f, s_lg=st[f], conv="B", nb=True)
        FULL[f"HS-{f}-t-noNB"] = dict(law="HS", foot=f, s_lg=st[f], conv="B", nb=False)
    FULL["HS-canonical-lo"] = dict(law="HS", foot="canonical", s_lg=st["canonical"] * 0.8, conv="B", nb=True)
    FULL["HS-canonical-hi"] = dict(law="HS", foot="canonical", s_lg=st["canonical"] * 1.25, conv="B", nb=True)
    FULL["HS-canonical-t-nbhi"] = dict(law="HS", foot="canonical", s_lg=st["canonical"], conv="B", nb=True, nb_scale=2.3)
    for f in FOOTS:
        if stA.get(f):
            FULL[f"HS-{f}-A-pair"] = dict(law="HS", foot=f, s_lg=stA[f], conv="A", nb=False)
    for fl in F_LCDM:
        FULL[f"LCDM-f{fl:g}"] = dict(law="NEWTON", foot="canonical", s_lg=1.0, f_lg=fl, f_nb=1.0, conv="A", nb=False)
    for k_, c_ in FULL.items():
        c_["tag"] = k_
    AF = {k_: pool.apply_async(job_config, (c_,)) for k_, c_ in FULL.items()}
    P(f"\n  phase 2 queued: {len(AF)} full configurations (bodies, the 3-D grid field, 64 R0 rays, the 32 dwarfs' numerical action)  {el()}")
    RES = {}
    for k_, a_ in AF.items():
        tag, out, dt = a_.get(); RES[k_] = out
        if "error" in out:
            P(f"    {tag}: ERROR {out['error'][-400:]}"); continue
        if out.get("not_converged"):
            P(f"    {tag}: the bodies' boundary-value problem did not converge (residual {out['bvp_res_Mpc']:.1e} Mpc) -- reported, not scored  [{dt:.0f}s]"); continue
        c2 = out["chi2"]
        P(f"    {tag}: v_r {out['pair']['vr']:+.2f}, v_t {out['pair']['vt']:.1f} km/s; R0 {out['R0']['mean']:.3f} Mpc (|cos| <= 0.9 "
          f"{out['R0']['mean_valid']:.3f}); flow chi^2 {c2['chi2_flow']:.1f}/{c2['n']} (mean model - data {c2['mean_res']:+.1f}, rms {c2['rms_res']:.1f} km/s), "
          f"timing chi^2 {c2['chi2_timing']:.2f}  [{dt:.0f}s]")
    OUT["numbers"]["T"]["s_timing_A_pair"] = stA
    analyse(RES, st, scan, pool)


def finish(pool):
    pool.close(); pool.join()
    nlb = sum(1 for _, ok, lb in CH if lb and not ok)
    OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
    fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
    json.dump(OUT, open(fn, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating, np.integer)) else str(o)))
    P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {nlb}; time {time.time() - T0:.0f} s; wrote {os.path.basename(fn)}")
    sys.exit(0 if nlb == 0 else 1)


def parab_min(xs, ys):
    """minimum of a parabola through the lowest point and its neighbours (in the given coordinate), or the lowest point."""
    o = np.argsort(xs); xs, ys = np.asarray(xs)[o], np.asarray(ys)[o]; j = int(np.argmin(ys))
    if 0 < j < len(xs) - 1:
        c = np.polyfit(xs[j - 1:j + 2], ys[j - 1:j + 2], 2)
        if c[0] > 0:
            xm = -c[1] / (2 * c[0]); return float(xm), float(np.polyval(c, xm))
    return float(xs[j]), float(ys[j])


def analyse(RES, st, scan, pool):
    ok_ = lambda k_: k_ in RES and "error" not in RES[k_] and "R0" in RES[k_]
    jt = lambda o: o["chi2"]["chi2_flow"] + o["chi2"]["chi2_timing"]
    dd = X.F11.ungc_hubble(0.63)
    # ---------------------------------------------------------------------------------------------- O: the orbit
    banner("O  THE MW-M31 ORBIT IN 3-D AT THE TIMING MASS")
    for f in FOOTS:
        if ok_(f"HS-{f}-t"):
            pr = RES[f"HS-{f}-t"]["pair"]
            P(f"    {f}: v_r {pr['vr']:+.2f} km/s; tidally induced v_t {pr['vt']:.1f} km/s (measured 17 (<34), 57 (+35/-31), 82 +- 31); d_max "
              f"{pr['dmax']:.3f} Mpc at z = {pr['z_dmax']:.2f} ({pr['t_dmax_lookback']:.2f} Gyr ago); pericentres since a = 0.02: {pr['peri'] or 'none'}; "
              f"separation at a = 0.02: {pr['d_ai_kpc']:.1f} kpc")
    pers = [RES[f"HS-{f}-t"]["pair"]["peri"] for f in FOOTS if ok_(f"HS-{f}-t")]
    vts = [RES[f"HS-{f}-t"]["pair"]["vt"] for f in FOOTS if ok_(f"HS-{f}-t")]
    check("O1 (reported) THE ORBIT: no pericentre since a = 0.02 (first approach; no past flyby) and the tangential velocity the "
          "neighbours' tides induce, against the measured 17 (<34), 57 (+35/-31) and 82 +- 31 km/s",
          "; ".join(f"{f}: pericentres {RES[f'HS-{f}-t']['pair']['peri'] or 'none'}, v_t {RES[f'HS-{f}-t']['pair']['vt']:.1f} km/s" for f in FOOTS if ok_(f"HS-{f}-t")),
          all(not p for p in pers), load_bearing=False,
          reading=f"v_t {min(vts):.0f}-{max(vts):.0f} km/s lies inside the measured spread (17-82)" if vts and 10 <= min(vts) and max(vts) <= 120 else "")
    # ---------------------------------------------------------------------------------------------- R: R0
    banner("R  THE ZERO-VELOCITY RADIUS IN 3-D: with the neighbours vs the pair alone (the same machinery), both footings")
    r0 = {f: RES[f"HS-{f}-t"]["R0"] for f in FOOTS if ok_(f"HS-{f}-t")}
    r0n = {f: RES[f"HS-{f}-t-noNB"]["R0"] for f in FOOTS if ok_(f"HS-{f}-t-noNB")}
    for f in r0:
        P(f"    {f}: with neighbours: mean {r0[f]['mean']:.4f} Mpc ({math.log10(r0[f]['mean'] / R0_MEAS):+.3f} dex; |cos| <= 0.9 {r0[f]['mean_valid']:.4f}); per "
          f"polar ray (phi-mean) {np.round(r0[f]['per_theta'], 3).tolist()}; range {r0[f]['min']:.3f}-{r0[f]['max']:.3f}"
          + (f" | pair alone: {r0n[f]['mean']:.4f} ({math.log10(r0[f]['mean'] / r0n[f]['mean']):+.4f} dex)" if f in r0n else ""))
    check("R1 THE 3-D FLOW DOES NOT REMOVE THE OVERSHOOT: at the 3-D timing mass, with the neighbours' tides and the non-linear MOND "
          f"superposition of all ten bodies, the solid-angle-mean zero-velocity radius stays above the +0.10 dex band ({EDGE:.2f} Mpc) on "
          "both footings -- a verified FAIL of the chain's Local Group",
          "; ".join(f"{f}: {v['mean']:.3f} Mpc ({math.log10(v['mean'] / R0_MEAS):+.3f} dex; {(v['mean'] - R0_MEAS) / R0_HONEST:.1f} x FP18's honest "
                    f"+-{R0_HONEST})" for f, v in r0.items()) + f"; measured {R0_MEAS} +- {R0_ERR} (Karachentsev+2009)",
          len(r0) == 2 and all(v["mean"] > EDGE for v in r0.values()))
    dl = {f: math.log10(r0[f]["mean"] / r0n[f]["mean"]) for f in r0 if f in r0n}
    if len(dl) == 2 and all(r0[f]["mean"] <= EDGE for f in r0):
        cls = "REMOVES"
    elif len(dl) == 2 and all(v <= -0.03 for v in dl.values()):
        cls = "REDUCES"
    elif len(dl) == 2 and all(abs(v) < 0.03 for v in dl.values()):
        cls = "CONFIRMS"
    elif len(dl) == 2 and all(v >= 0.03 for v in dl.values()):
        cls = "WORSENS"
    else:
        cls = "MIXED"
    check("R2 (reported; classification pre-declared) THE NEIGHBOURS' EFFECT ON R0: removes (R0 <= 1.21 on both footings), reduces "
          "(shift <= -0.03 dex on both), confirms (|shift| < 0.03 dex on both) -- the pre-declared expectation was CONFIRMS",
          "; ".join(f"{f}: {v:+.4f} dex" for f, v in dl.items()) + f" -> {cls}", True, load_bearing=False)
    OUT["numbers"]["R"] = dict(with_nb=r0, pair_alone=r0n, shift_dex=dl, cls=cls)
    # ---------------------------------------------------------------------------------------------- F: the flow fit against LCDM
    banner("F  THE FLOW FIT: 32 galaxies at 0.7-3 Mpc + the MW-M31 v_r; the chain against the matched LCDM numerical action")
    lc = {fl: RES[f"LCDM-f{fl:g}"] for fl in F_LCDM if ok_(f"LCDM-f{fl:g}")}
    for fl, o in lc.items():
        P(f"    LCDM (pair alone, conv. A) f = {fl:g} (M_LG {fl * NB_NOM:.2e} Msun): v_r {o['pair']['vr']:+.1f} km/s; flow chi^2 {o['chi2']['chi2_flow']:.1f} "
          f"(mean model - data {o['chi2']['mean_res']:+.1f}, rms {o['chi2']['rms_res']:.1f}); timing chi^2 {o['chi2']['chi2_timing']:.1f}; R0 {o['R0']['mean']:.3f} Mpc")
    xs = np.log([fl for fl in lc]) if lc else []
    lf, lmin = parab_min(xs, [jt(o) for o in lc.values()]) if len(lc) >= 3 else (float("nan"), float("nan"))
    lfl, lminf = parab_min(xs, [o["chi2"]["chi2_flow"] for o in lc.values()]) if len(lc) >= 3 else (float("nan"), float("nan"))
    f_t_lcdm = interp_s([(fl, o["pair"]["vr"]) for fl, o in lc.items()])
    R0_lcdm_t = float(np.exp(np.interp(math.log(f_t_lcdm), xs, np.log([o["R0"]["mean"] for o in lc.values()])))) if f_t_lcdm else float("nan")
    chA = {f: RES[f"HS-{f}-A-pair"] for f in FOOTS if ok_(f"HS-{f}-A-pair")}
    chB = {f: RES[f"HS-{f}-t"] for f in FOOTS if ok_(f"HS-{f}-t")}
    chBp = {f: RES[f"HS-{f}-t-noNB"] for f in FOOTS if ok_(f"HS-{f}-t-noNB")}
    for lab, dct in (("chain, pair alone, conv. A", chA), ("chain, 3-D with neighbours, conv. B", chB), ("chain, pair alone, conv. B", chBp)):
        for f, o in dct.items():
            P(f"    {lab} {f} (M_LG {o['cfg']['s_lg'] * NB_NOM:.3e}): v_r {o['pair']['vr']:+.1f}; flow chi^2 {o['chi2']['chi2_flow']:.1f}/{o['chi2']['n']} (mean model - data "
              f"{o['chi2']['mean_res']:+.1f}, rms {o['chi2']['rms_res']:.1f} km/s); timing chi^2 {o['chi2']['chi2_timing']:.2f}; sigma_th 35: {o['chi2_35']['chi2_flow']:.1f}; R0 {o['R0']['mean']:.3f}")
    dchi = {f: jt(o) - lmin for f, o in chA.items()}
    check("F1 THE FLOW FAVOURS THE MATCHED LCDM CONTROL: the chain's joint chi^2 (the pair alone, convention A, at its own timing mass) "
          "exceeds the matched LCDM numerical action's minimum over the LG halo mass (the same pair, convention A) by >= 9 on both footings",
          "; ".join(f"{f}: chain {jt(o):.1f} vs LCDM min {lmin:.1f} (at M_LG = {math.exp(lf) * NB_NOM:.2e}) -> {dchi[f]:+.1f}" for f, o in chA.items()),
          len(dchi) == 2 and all(v >= 9 for v in dchi.values()),
          reading=f"LCDM's flow-only minimum {lminf:.1f} at M_LG = {math.exp(lfl) * NB_NOM:.2e}" if lminf == lminf else "")
    check("F2 (reported) THE LCDM CONTROL'S OWN TENSION (FP18: LCDM shares the pincer): the LG halo mass its flow prefers against its "
          "own timing mass, and its zero-velocity radius at that timing mass", f"flow-preferred M_LG {math.exp(lfl) * NB_NOM:.2e} Msun; joint best "
          f"{math.exp(lf) * NB_NOM:.2e}; timing (v_r = -109.3) at M_LG = " + (f"{f_t_lcdm * NB_NOM:.2e}, where R0 = {R0_lcdm_t:.3f} Mpc ({math.log10(R0_lcdm_t / R0_MEAS):+.3f} dex)" if f_t_lcdm else "not bracketed"),
          True, load_bearing=False, reading="FP18 (committed): KiDS-fitted LCDM halos turn around at 1.85-1.94 Mpc")
    check("F3 (reported) THE CHAIN'S FLOW IN 3-D WITH THE NEIGHBOURS (convention B, the headline 3-D reconstruction) against the pair "
          "alone in the same convention: what the neighbours do to the 32-galaxy fit",
          "; ".join(f"{f}: with neighbours {jt(chB[f]):.1f} (mean model - data {chB[f]['chi2']['mean_res']:+.1f}), pair alone {jt(chBp[f]):.1f} "
                    f"(mean {chBp[f]['chi2']['mean_res']:+.1f})" for f in FOOTS if f in chB and f in chBp), True, load_bearing=False)
    cmass = [(k_, RES[k_]) for k_ in ("HS-canonical-lo", "HS-canonical-t", "HS-canonical-hi") if ok_(k_)]
    cs_, cmin = parab_min(np.log([o["cfg"]["s_lg"] for _, o in cmass]), [jt(o) for _, o in cmass]) if len(cmass) == 3 else (float("nan"), float("nan"))
    OUT["numbers"]["F"] = dict(lcdm={f"{fl:g}": dict(pair=o["pair"], chi2=o["chi2"], chi2_35=o["chi2_35"], R0=o["R0"]["mean"]) for fl, o in lc.items()},
                               lcdm_best_joint=dict(f=math.exp(lf), chi2=lmin), lcdm_best_flow=dict(f=math.exp(lfl), chi2=lminf), lcdm_timing_f=f_t_lcdm,
                               lcdm_R0_at_timing=R0_lcdm_t,
                               chain_A_pair={f: dict(s=o["cfg"]["s_lg"], chi2=o["chi2"], chi2_35=o["chi2_35"], chi2_slope=o["chi2_slope"], R0=o["R0"]["mean"]) for f, o in chA.items()},
                               chain_B_nb={f: dict(s=o["cfg"]["s_lg"], chi2=o["chi2"], chi2_35=o["chi2_35"], R0=o["R0"]["mean"]) for f, o in chB.items()},
                               chain_B_pair={f: dict(s=o["cfg"]["s_lg"], chi2=o["chi2"], R0=o["R0"]["mean"]) for f, o in chBp.items()},
                               chain_canonical_B_min=dict(s=math.exp(cs_) if cs_ == cs_ else None, chi2=cmin), dchi=dchi)
    # ---------------------------------------------------------------------------------------------- E: the estimator
    est = {k_: ests(RES[k_], dd) for k_ in [f"HS-{f}-t" for f in FOOTS] + [f"HS-{f}-A-pair" for f in FOOTS] + [f"LCDM-f{fl:g}" for fl in F_LCDM] if ok_(k_)}
    check("E1 (reported) THE PUBLISHED ESTIMATOR ON THE MODEL: the linear fit V = H (R - R0) over 0.7-3 Mpc (FP11 R4 / Karachentsev+2009) "
          "applied to each model's predicted velocities at the 32 observed galaxies, the data's own geometry (FP18's warning: not "
          "FP12's 'eq. 14')", "; ".join(f"{k_}: R0 {v['model']['R0']:.3f}, H {v['model']['H']:.0f}" for k_, v in est.items())
          + (f"; data {list(est.values())[0]['data']['R0']:.3f}, H {list(est.values())[0]['data']['H']:.0f}" if est else ""), True, load_bearing=False)
    OUT["numbers"]["E1"] = est
    # ---------------------------------------------------------------------------------------------- V: variants
    vv = {}
    if ok_("HS-canonical-t-nbhi") and ok_("HS-canonical-t"):
        vv["neighbours x2.3 (FP12's band top)"] = (RES["HS-canonical-t-nbhi"]["R0"]["mean"], RES["HS-canonical-t-nbhi"]["pair"]["vr"], jt(RES["HS-canonical-t-nbhi"]))
    for k_ in ("HS-canonical-lo", "HS-canonical-hi"):
        if ok_(k_):
            vv[f"LG mass x{RES[k_]['cfg']['s_lg'] / st['canonical']:.2f}"] = (RES[k_]["R0"]["mean"], RES[k_]["pair"]["vr"], jt(RES[k_]))
    check("V1 (reported) VARIANTS (canonical, convention B, neighbours on): the neighbours at FP12's band top, the LG mass scaled -- "
          "R0, v_r and the joint chi^2", "; ".join(f"{k_}: R0 {a:.3f} Mpc, v_r {b:+.1f}, chi^2 {c:.1f}" for k_, (a, b, c) in vv.items()),
          True, load_bearing=False)
    OUT["numbers"]["V1"] = vv
    cg = {f: st[f] * NB_NOM for f in FOOTS if st[f]}
    check("C1 (reported) THE CGM RANGE: the 3-D timing mass against the LG's stars + HI (nominal 1.82e11) and the CGM range (0-9.8e10 per "
          "L* galaxy, Bregman+2022 tSZ as the L45 lane reads it): the room the timing leaves for circumgalactic baryons",
          "; ".join(f"{f}: M_t {v:.3e} = {v / NB_NOM:.2f} x stars + HI -> CGM room {max(v - NB_NOM, 0):.1e} (range up to {2 * CGM_MAX:.1e})" for f, v in cg.items()),
          True, load_bearing=False)
    check("G1 THE OTHER GATES ARE UNCHANGED: this lane adds no term to the action (the law is FP13's H_S as committed; K7), so the "
          "flagship, SPARC, KiDS, sigma_8 and forest rows are FP13's", "new action terms: 0", True)
    # ---------------------------------------------------------------------------------------------- W: ledger + verdict
    banner("W  THE LEDGER")
    rs = ", ".join(f"{f} {v['mean']:.2f}" for f, v in r0.items())
    LEDGER = [
        ("XR24a", "DERIVED", "the chain's static law (FP7 root + FP13 H_S) for N point masses in 3-D: isolated phantoms + the non-additive "
                             "interaction field, direct kernel integral and spherical-harmonic grid", "K3-K5 (virial identity, momentum, FP11 two-body limit)"),
        ("XR24b", "POSTULATED", "the numerical-action idealisation: point-mass groups (M33 merged into M31), growing mode at a = 0.02, "
                                "convention B for the ten-body reconstruction (A packs the Local Volume within ~20 kpc at z = 49); the matched LCDM comparison on "
                                "the pair alone in A", "scope; F1-F3"),
        ("XR24c", "DERIVED" if all(inw_(st[f]) for f in FOOTS) else "FAILS", "the 3-D MW-M31 timing on the first approach with baryons: M_t = "
                  + ", ".join(f"{f} {st[f] * NB_NOM:.2e}" for f in FOOTS if st[f]), "T1, T2, O1"),
        ("XR24d", "FAILS", f"R0 in 3-D at the timing mass: {rs} Mpc vs 0.96 (+-0.03 quoted, +-0.11 honest); the neighbours: {cls}", "R1, R2"),
        ("XR24e", "FAILS" if len(dchi) == 2 and all(v >= 9 for v in dchi.values()) else "CONSTRAINT", "the 32-galaxy flow (pair alone, conv. A): chain joint chi^2 "
                  + ", ".join(f"{f} {jt(o):.0f}" for f, o in chA.items()) + f" vs matched LCDM min {lmin:.0f}", "F1, F2, F3, E1"),
        ("XR24f", "OPEN", "not computed: the AQUAL curl part, M33's own orbit, Virgo and the Local Void (beyond 5 Mpc), distance "
                          "adjustments in the action, the dark fluid as a variant (FP16: not kept by these galaxies)", "scope"),
    ]
    for lk_, stt, wh, ba in LEDGER:
        P(f"    {lk_:6s} {stt:11s} {wh}  --  {ba}")
        OUT["ledger"].append({"link": lk_, "status": stt, "what": wh, "basis": ba})
    banner("VERDICT")
    P("  The Local Group's Hubble flow in 3-D in the chain's law (FP7 root + FP13 H_S; convention B; both footings):")
    P("  timing: " + ", ".join(f"{f} M_t = {st[f] * NB_NOM:.2e} Msun" for f in FOOTS if st[f]) + "; R0: " + rs + f" Mpc -> the overshoot {cls}.")
    P("  flow (matched pair, conv. A): " + ", ".join(f"{f} chain chi^2 {jt(o):.0f}" for f, o in chA.items()) + f" vs LCDM {lmin:.0f} at M_LG {math.exp(lf) * NB_NOM:.2e}; "
      + (f"LCDM's own R0 at its timing mass {R0_lcdm_t:.2f} Mpc." if R0_lcdm_t == R0_lcdm_t else "") + "  Not 'closed'.")
    finish(pool)


def inw_(s):
    return s is not None and WIN[0] <= s * NB_NOM <= WIN[1]


if __name__ == "__main__":
    main()
