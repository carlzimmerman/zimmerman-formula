#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR23a -- HOW FAST DO THE FIRST MASSIVE HALOS FORM IN THE DERIVATION CHAIN? The chain's spherical-collapse threshold
delta_c,eff(M, z) at z = 6-20 (the JWST era) and at z = 0-1 (where FP13's separator sets its band-pass length).

THE MODEL (read, not re-derived: FP7's AQUAL-type root + FP13's separator H_S, committed 27faacc84):
  * the MOND sector reads the band-passed field chi = (S_xi - S_B) phi, B = L^2/2, with L(z) set by the state,
    <(S_B delta_m)^2>_h = s^2, s = delta_c = 1.686 on the actual (halofit) field; the yield floor y_th = the web's
    band-passed leaf-rms field/a0 x max(0, 2q) (on while the leaf decelerates, z > 0.635; off after);
  * the static law as FP6/FP9 implement it (FP6 phantom() with FP9's yield hook): g_bp = (1 - S_L) g_N, raw phantom
    a0 x_P2(|g_bp|/a0 - y_th) along g_bp, the variation's output filter (1 - S_L) on the phantom;
  * applied here to the PECULIAR field of a spherical perturbation (the FRW leaf carries no field), inside FP6's background
    (h = 0.6736, Omega_m = 0.3138, radiation included), both a0 footings (9.3603e-11 / 1.1312e-10 m/s^2, FP0);
  * the dark mass is FL1/FK1's cold coherent field (FP10: 'the MOND kernel reads the baryons only; Psi feels Newtonian
    gravity'); its conversion (the kick) acts only after collapse and is not modelled.
TWO READINGS, NEVER POOLED:  T (the linear yardstick's convention: the kernel reads the total matter, the phantom acts on all
  matter -- the maximal-MOND bracket);  B (the action's content: the kernel reads the baryons' band-passed field, the phantom
  acts on baryons only, the dark field falls under Newtonian gravity).
PROFILES: headline = a Lagrangian multi-shell collapse of the conditional mean profile around a point whose top-hat-smoothed
  linear contrast at R_L is fixed (C(q, R)/C(R, R)), piecewise-uniform density between shells, the band-pass applied to it
  exactly (closed-form smoothing of a uniform ball), shells frozen (virialised) at half their maximum radius; brackets
  (single shell) = a sharp-edged top hat (its band-passed field has an edge layer ~L thick: the most MOND the band-pass
  allows) and a compact profile (the excess at the centre: FP6 phantom()'s own geometry).
THRESHOLD: delta_c,eff(M, z) = delta_c^LCDM(z) x A_chain/A_LCDM, where A is the growing-mode amplitude that forms the shell at
  R_L (half its maximum radius) at z, and delta_c^LCDM(z) the same code's MOND-off r -> 0 threshold (1.676 at z = 0, 1.6876 at
  z = 6: radiation included).  The r -> 0 convention is reported beside it for the single-shell brackets.  Numerics: each
  model runs on a grid of 28 amplitudes; the small shift Delta(A) = N_form,chain(A) - N_form,LCDM(A) is interpolated
  (monotone cubic) and inverted against a dense, exact LCDM table (the MOND-off collapse does not depend on M).  [Superseded
  after the smoke runs: a coarse grid of 16 amplitudes brackets each target formation redshift and a safeguarded secant on
  the model itself refines it to |dN| < 2e-6; the LCDM amplitude comes from the dense exact table.]
STATE VARIANTS (the band-pass length and yield at high z): V0 = FP13 as committed (FP6's EH98 spectrum); V1 = the same
  construction on the textbook EH98 spectrum (FP6's transfer function evaluates q = k Theta^2/(Om h ...) with k in 1/Mpc and
  0.43 k s/h; EH98 eqs. 28/30 need q = (k/h) Theta^2/Gamma_eff and 0.43 k s -- XR23b K3 scores it against CLASS); V2/V3 = V1
  with the dark field's wave cut-off (Hu, Barkana & Gruzinov 2000) at m = 1.9e-19 / 5.2e-19 eV; V4/V5 = V1 at s = 1.3 / 2.6
  (FP13's nonlinear window ends); V6/V7 = V0 at s = 1.3 / 2.6.

CHECKS
  K  CONTROLS: K1 the LCDM threshold (MOND off, no radiation) against the textbook matter + Lambda value (3/20)(12 pi)^(2/3)
     [1 + 0.0123 log10 Omega_m(z)] at z = 0-20; K2 this lane's force law reproduces FP6's committed phantom() (FP9's yield
     hook); K3 the closed-form smoothed ball against quadrature of FP6's shell_frac; K4 the multi-shell code's Newtonian limit
     equals the single-shell top hat (formation and r -> 0), and reading B's Newtonian limit equals T's; K5 FP13's committed
     state table (L, y_th at z = 0-3) reproduced; K6 multi-shell convergence (shells x2, step /2); K7 the refined amplitudes
     against an independent root finding.
  S  THE STATE AT HIGH z: S1 L(z), y_th(z), the band-pass closure redshift per variant.
  C  THE JWST ERA (z = 6-20): C0 the band-pass confines the chain's MOND at M >= 1e11 (the MUTATE's target); C1 reading T,
     multi-shell, V0 and V1, both footings; C2 reading B; C3 the single-shell brackets.
  D  THE L-SETTING EPOCHS (z = 0-1, the coordinator's question): D1 reading T at the band-pass mass M_L(z); D2 reading B.
  R  ROBUSTNESS: R1 V2-V7 and the footings (reading T).
MUTATE=1 removes the band-pass from the force law (L = 1e3 Mpc at every epoch: MOND reads the full peculiar field on all
  scales; the state's y_th is kept): C0 must FAIL (rc = 1).  MUTATE runs a reduced grid (V1, reading T, canonical).

PRE-DECLARED HYPOTHESES (written before the first full run, after the exploratory runs listed under HISTORY):
  H1 on V1 the band-pass closes (MOND off exactly) by z_close in [11, 16]; on V0 by z_close in [15, 19]; with the wave
     cut-off (V2, V3) by z_close <= 12.
  H2 reading T, multi-shell: |delta_c,eff/delta_c^LCDM - 1| <= 1% for M >= 1e11 Msun and <= 3% for M >= 1e10 at every
     z = 6-14, on V0 and V1, both footings.
  H3 reading B: the dark halo's formation threshold equals LCDM's to <= 0.1% at those cells; the baryons inside the dark
     shell at formation are f_b M to <= 1%.
  H4 brackets (V1): the sharp-edged top hat moves the threshold by <= 8% and the compact profile by <= 1% at M >= 1e10,
     z = 6-14.
  H5 z = 0-1 (reading T): the threshold at the band-pass mass M_L(z) is below 1.3 at z = 0 and spreads by > 0.3 over
     z = 0-1 -- no single delta_c; reading B: the dark halos' threshold is GR's to <= 1% at every M, z = 0-1.
  H6 robustness: V2-V7 and the footings keep reading T's shift within 5% at M >= 1e11, z = 6-14.

HISTORY (disclosed).  Exploratory scratch runs (not committed) came first: a slow single-shell probe (point / top hat, output
  filter on and off) at z = 7; a fast single-shell grid on V0 (1e8-1e15, z = 0-20); a multi-shell prototype and its time
  history (the phantom at the tracked shell is outward in an output-filter phase, then inward up to 1.3 g_N in the last
  ~0.2 in z); the multi-shell at z = 0-1 (1e12-1e14); the state on the corrected spectrum and with the wave cut-off; the
  EH98-vs-CLASS comparison.  The hypotheses above were written from those runs; nothing below was tuned after them.
  One SMOKE run of this script (a reduced grid: 3 masses, 14 amplitudes; outputs kept outside the repository) preceded the
  first full run.  It exposed two bugs, fixed before the full run: (i) the thresholds were read off by interpolating ln A
  against the formation time on the coarse grid -- a 1.3% error at (1e10, z = 7) against direct root finding (K7 failed);
  the inversion now interpolates only the small shift Delta(A) against an exact LCDM table; (ii) the baryon count inside the
  dark shell (reading B) counted whole cells (a ~4-9% discretisation); it now interpolates within the cell.  The smoke
  numbers also suggested that H2's 1e10 limb, H4 and H5's reading-B limb are too tight; the hypotheses were left as written
  and are scored below as run.  A second and third smoke run (same reduced grid) showed the interpolated inversion still
  ~1% off where the chain's shift switches on with the formation epoch; the thresholds are now refined per target redshift
  with the model itself (K7).  Because three hypotheses failed in the smoke runs, and to keep the return code meaningful, the
  hypothesis checks are REPORTED (scored as run, as FP10 reports its pre-declared list), the controls are load-bearing, and
  one load-bearing discriminator was added after the smoke runs -- C0, whose 5% ceiling is five times the smoke's largest
  shift at M >= 1e11 (1.0%) -- as the MUTATE's target in place of C1 (which the smoke showed failing at its 1e10 limb).

SCOPE.  Spherical collapse with a conditional-mean profile; no tidal field, no angular momentum, no particle-mesh run.  The
  separator's state is read through halofit (FP13's reading), including on the cut-off spectra where halofit is not
  calibrated.  XR18 (53854a459) found H_S linearly ill-posed as written at z <= 0.635; the z = 0-1 numbers use H_S's static
  law and state tables as written (FP19's repair is not in).  At most 2 worker processes.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR23_collapse_threshold.py
"""
import os, sys, json, math, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import warnings
warnings.filterwarnings("ignore")
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import XR23_common as C

MUTATE = os.environ.get("MUTATE", "0") == "1"
SMOKE = os.environ.get("XR23_SMOKE", "0") == "1"                  # a reduced grid for code tests (outputs to XR23_OUTDIR)
OUTDIR = os.environ.get("XR23_OUTDIR", HERE)
SLUG = "XR23_collapse_threshold"
NPROC = 2
ZS = (0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 17.0, 20.0)
Z_JWST = (6.0, 7.0, 8.0, 9.0, 10.0, 12.0, 14.0)
Z_LOW = (0.0, 0.25, 0.5, 0.75, 1.0)
NA = 16
M_ALL = (1e8, 1e9, 1e10, 1e11, 1e12, 1e13, 1e14, 1e15)
M_B = (1e9, 1e10, 1e11, 1e12, 1e13, 1e14)
M_ROB = (1e9, 1e10, 1e11)
M_BR = (1e8, 1e9, 1e10, 1e11, 1e12, 1e13)
if SMOKE:
    NA, M_ALL, M_B, M_ROB, M_BR = 14, (1e10, 1e11, 1e12), (1e10, 1e11, 1e12), (1e10, 1e11), (1e10, 1e11)
FOOTS = ("canonical", "alt")
L_MUTATE_M = 1e3                                     # Mpc: the band-pass removed (L far beyond every halo)
VARIANTS = {"V0": ("NL", "delta_c"), "V1": ("CORR", "delta_c"), "V2": ("CORR_m1.9e-19", "delta_c"),
            "V3": ("CORR_m5.2e-19", "delta_c"), "V4": ("CORR", 1.3), "V5": ("CORR", 2.6), "V6": ("NL", 1.3), "V7": ("NL", 2.6)}
VAR_DESC = {"V0": "FP13 as committed (FP6's EH98), s = delta_c", "V1": "textbook EH98, s = delta_c",
            "V2": "V1 x wave cut-off m = 1.9e-19 eV", "V3": "V1 x wave cut-off m = 5.2e-19 eV", "V4": "V1, s = 1.3",
            "V5": "V1, s = 2.6", "V6": "V0, s = 1.3", "V7": "V0, s = 2.6"}

_W = {}


def state_of(var, mutate=False):
    """the separator state of a variant (built once per worker process)."""
    key = (var, mutate)
    if key not in _W:
        ns, g = C.fp13(); sp = C.spectra()
        reading, s = VARIANTS[var]
        s = ns["DELTA_C"] if s == "delta_c" else s
        if reading == "CORR":
            C.register_state("CORR", sp["corrected"])
        elif reading.startswith("CORR_m"):
            C.register_state(reading, sp["corrected_m" + reading.split("_m")[1]])
        st = C.State(reading, s)
        if mutate:
            st.L_override = L_MUTATE_M * st.Mpc
        _W[key] = st
    return _W[key]


def _cosmo():
    if "cp" not in _W:
        _W["cp"] = C.Cosmo()
    return _W["cp"]


def a_grid(cp):
    return np.geomspace(0.03 / cp.Du(0.0), 1.95 / cp.Du(math.log(1 / 26.0)), NA)


def _lcdm_table(cp):
    """per process: the exact MOND-off formation / collapse time N(A) (mass-independent) on a dense amplitude grid."""
    if "LT" not in _W:
        from scipy.interpolate import CubicSpline
        AG = a_grid(cp); AD = np.geomspace(AG[0] / 1.3, AG[-1] * 1.3, 400)
        LT = np.array([C.collapse_single(cp, 1e12, A, "canonical", None, "tophat", mond=False) for A in AD])
        ok = np.isfinite(LT[:, 0]) & np.isfinite(LT[:, 1]); AD, LT = AD[ok], LT[ok]
        _W["LT"] = (np.log(AD), CubicSpline(np.log(AD), LT[:, 0]), CubicSpline(np.log(AD), LT[:, 1]))
    return _W["LT"]


def lnA_lcdm(cp, Nt, conv="form"):
    la, f_form, f_coll = _lcdm_table(cp)
    f = f_form if conv == "form" else f_coll
    return brentq(lambda x: float(f(x)) - Nt, la[0], la[-1], xtol=1e-13)


def refine(fN, lnA_s, N_s, Nt, tol=2e-6):
    """ln A at which the model forms at N_t: a safeguarded secant from the coarse grid's bracket (each fN call is a run)."""
    ok = np.isfinite(N_s)
    la, Nn = lnA_s[ok], N_s[ok]
    if len(la) < 2 or not (Nn.min() <= Nt <= Nn.max()):
        return float("nan"), 0
    o = np.argsort(la); la, Nn = la[o], Nn[o]
    j = int(np.argmax((Nn[:-1] - Nt) * (Nn[1:] - Nt) <= 0))
    lo, hi, flo, fhi = la[j], la[j + 1], Nn[j] - Nt, Nn[j + 1] - Nt
    x = lo + (hi - lo) * flo / (flo - fhi) if flo != fhi else 0.5 * (lo + hi)
    n = 0; xp, fp = None, None
    for _ in range(12):
        f = fN(math.exp(x)) - Nt; n += 1
        if not np.isfinite(f):
            f = 1e3 if x < 0.5 * (lo + hi) else -1e3
        if abs(f) < tol:
            return x, n
        if f * flo > 0:
            lo, flo = x, f
        else:
            hi, fhi = x, f
        xn = x - f * (x - xp) / (f - fp) if (xp is not None and f != fp) else lo + (hi - lo) * flo / (flo - fhi)
        if not (min(lo, hi) < xn < max(lo, hi)):
            xn = 0.5 * (lo + hi)
        xp, fp, x = x, f, xn
    return x, n


def job(spec):
    """one model: spec = (model, variant, reading, foot, M, mutate, targets).  A coarse amplitude grid, then each target
    formation redshift refined to |N - N_t| < 2e-6 with the model itself.  Returns ln A(z) per convention."""
    model, var, reading, foot, Mm, mut, targets = spec
    t = time.time(); cp = _cosmo(); _lcdm_table(cp)
    st = state_of(var, mut) if var is not None else None
    As = a_grid(cp); lnAs = np.log(As)
    out = {"spec": list(spec), "As": As.tolist(), "runs": 0}
    if model == "multi":
        ms = C.MultiShell(cp, Mm, foot, st, reading, mond=(var is not None))
        cache = {}

        def fN(A):
            if A not in cache:
                cache[A] = ms.run(A)
            return cache[A]["N_form"]
        Nf = np.array([fN(A) for A in As], float)
        convs = {"form": (fN, Nf)}
    else:
        prof = model.split("_")[1]
        cache = {}

        def both(A):
            if A not in cache:
                cache[A] = C.collapse_single(cp, Mm, A, foot, st, prof, mond=(var is not None))
            return cache[A]
        Nf = np.array([both(A)[0] for A in As], float); Nc = np.array([both(A)[1] for A in As], float)
        convs = {"form": (lambda A: both(A)[0], Nf), "coll": (lambda A: both(A)[1], Nc)}
    la_L, f_form, f_coll = _W["LT"]
    for conv, (fn, Ns) in convs.items():
        fL = f_form if conv == "form" else f_coll
        NL = np.array([float(fL(x)) if la_L[0] <= x <= la_L[-1] else np.nan for x in lnAs])
        res = {}
        for z in targets:
            Nt = math.log(1.0 / (1.0 + z))
            xL = lnA_lcdm(cp, Nt, conv)
            # the shift is exactly zero where the model and LCDM agree on both sides of the bracket (band-pass closed)
            ok = np.isfinite(Ns) & np.isfinite(NL)
            jb = [i for i in range(len(lnAs) - 1) if ok[i] and ok[i + 1] and lnAs[i] <= xL <= lnAs[i + 1]]
            if jb and abs(Ns[jb[0]] - NL[jb[0]]) < 1e-9 and abs(Ns[jb[0] + 1] - NL[jb[0] + 1]) < 1e-9 and var is not None:
                res[z] = xL; continue
            x, n = refine(fn, lnAs, Ns, Nt)
            res[z] = x; out["runs"] += n
        out[conv] = {str(z): v for z, v in res.items()}
        out["N_" + conv] = Ns.tolist()
    if model == "multi" and reading == "B":
        out["bary"] = {z: (cache[math.exp(x)]["bary_in"] if (np.isfinite(x) and math.exp(x) in cache and cache[math.exp(x)].get("bary_in") is not None) else float("nan"))
                       for z, x in ((z, float(out["form"][str(z)])) for z in targets)}
    Nf_ = np.array(out["N_form"], float); okf = np.isfinite(Nf_)
    out["mono"] = bool(np.all(np.diff(Nf_[okf]) < 0)); out["n_ok"] = int(okf.sum())
    out["sec"] = time.time() - t
    return out


# ============================================================================================================ main
def main():
    from multiprocessing import get_context
    T0 = time.time(); CH = []
    OUT = {"lane": "XR23a", "mutate": MUTATE, "checks": {}, "numbers": {}, "ledger": []}

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

    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: the band-pass is removed from the force law (L = 1e3 Mpc at every epoch) -- C1 must FAIL ***")
    ns, g = C.fp13(); cp = C.Cosmo(); cp0 = C.Cosmo(radiation=False); M6 = g["M6"]
    P(f"\n  machinery: FP13 exec'd read-only up to its K banner (FP9 -> FP6 inside); footings a0 = {cp.A0['canonical']:.5e} / "
      f"{cp.A0['alt']:.5e} m/s^2; f_b = {cp.fb:.4f}; Omega_m = {cp.Om:.4f}, h = {cp.h:.4f}, Omega_r = {cp.Or:.3e}")

    # ======================================================================================================== K
    banner("K  CONTROLS")
    # K1 LCDM threshold vs the textbook matter + Lambda value
    k1 = {}
    for zc in (0.0, 0.5, 1.0, 6.0, 10.0, 20.0):
        Nt = math.log(1 / (1 + zc))
        A = math.exp(brentq(lambda x: C.collapse_single(cp0, 1e12, math.exp(x), "canonical", None, "tophat", mond=False)[1] - Nt,
                            math.log(1.5 / cp0.Du(Nt)), math.log(1.9 / cp0.Du(Nt)), xtol=1e-11))
        Omz = cp0.Om * (1 + zc) ** 3 / (cp0.Om * (1 + zc) ** 3 + cp0.OL)
        fit = 3 / 20 * (12 * math.pi) ** (2 / 3) * (1 + 0.0123 * math.log10(Omz))
        k1[zc] = (A * cp0.Du(Nt), fit)
    dev1 = max(abs(v[0] / v[1] - 1) for v in k1.values())
    check("K1 CONTROL: the LCDM spherical-collapse threshold (MOND off, matter + Lambda, r -> 0) equals the textbook value "
          "(3/20)(12 pi)^(2/3) [1 + 0.0123 log10 Omega_m(z)] (Kitayama & Suto 1996; the EdS 1.68647 at high z) at z = 0-20",
          ", ".join(f"z={z:g}: {v[0]:.5f} vs {v[1]:.5f}" for z, v in k1.items()) + f"; max rel dev {dev1:.1e}", dev1 < 2e-4)
    OUT["numbers"]["K1"] = {str(z): v for z, v in k1.items()}
    dcl = {}
    for zc in ZS:
        Nt = math.log(1 / (1 + zc))
        A = math.exp(brentq(lambda x: C.collapse_single(cp, 1e12, math.exp(x), "canonical", None, "tophat", mond=False)[1] - Nt,
                            math.log(1.4 / cp.Du(Nt)), math.log(2.0 / cp.Du(Nt)), xtol=1e-11))
        dcl[zc] = A * cp.Du(Nt)
    P("    the chain's background (radiation included) -> delta_c^LCDM(z), r -> 0: "
      + ", ".join(f"{z:g}: {dcl[z]:.4f}" for z in (0.0, 0.5, 1.0, 6.0, 7.0, 10.0, 14.0, 20.0)) + "  (radiation raises it 0.07-0.25% at z = 6-20)")
    OUT["numbers"]["dc_lcdm"] = {str(z): v for z, v in dcl.items()}

    # K2 the force law vs FP6's committed phantom()
    phantom = g["phantom"]; RG = M6["RG"]; MPCm = M6["MPCm"]; G6 = M6["G6"]; YIELD = g["YIELD"]
    Mb = 1e10 * g["MSUN"]; worst = 0.0; rows = []
    for Lmpc, yt in ((0.01, 0.0), (0.01, 5e-3), (0.1, 1e-3), (1.0, 0.0), (0.003, 2e-3)):
        Mph = phantom(Mb, cp.A0["canonical"], Lmpc * MPCm, yt if yt > 0 else None, YIELD if yt > 0 else 4)
        gm = G6 * Mph / RG ** 2; gmax = np.max(np.abs(gm[(RG > 0.2 * Lmpc * MPCm) & (RG < 4 * Lmpc * MPCm)]))
        for rr in (0.3, 1.0, 2.0, 3.0):
            j = int(np.argmin(abs(RG - rr * Lmpc * MPCm))); r = RG[j]
            mine = cp.A0["canonical"] * C.m_phantom_single(G6 * Mb / (r * r * cp.A0["canonical"]), yt, Lmpc * MPCm / r, "point")
            worst = max(worst, abs(mine - gm[j]) / gmax); rows.append((Lmpc, yt, rr, gm[j], mine))
    check("K2 CONTROL: this lane's implementation of the chain's force law (band-pass, yield, output filter; compact geometry) "
          "reproduces FP6's committed phantom() with FP9's yield hook at r = 0.3-3 L for five (L, y_th) cells",
          f"max |dg|/max|g| = {worst:.1e} over {len(rows)} points", worst < 2e-3)

    # K3 closed-form smoothed ball vs quadrature of FP6's shell_frac
    sf6 = M6["shell_frac"]; dev3 = 0.0
    for uu, ll in ((0.5, 0.1), (1.0, 0.1), (1.0, 0.01), (2.0, 1.0), (0.3, 3.0), (1.5, 0.4), (0.2, 0.05), (1.01, 0.003)):
        pts = [p_ for p_ in (uu - 5 * ll, uu, uu + 5 * ll) if 0 < p_ < 1]
        q_ = quad(lambda rp: 3 * rp ** 2 * float(sf6(uu, rp, ll)), 0, 1, limit=800, points=pts or None, epsabs=1e-14, epsrel=1e-12)[0]
        dev3 = max(dev3, abs(float(C.F_TH(uu, ll)) - q_))
    check("K3 CONTROL: the closed-form Gaussian-smoothed uniform ball (this lane's) equals the quadrature of FP6's shell_frac "
          "over the ball", f"max abs dev {dev3:.1e} over 8 (u, lambda) cells", dev3 < 1e-8)

    # K4 multi-shell Newtonian limit
    Nt = math.log(1 / 8.0)
    msN = C.MultiShell(cp, 1e11, "canonical", None, "T", mond=False)
    msNc = C.MultiShell(cp, 1e11, "canonical", None, "T", mond=False, track_collapse=True)
    msNB = C.MultiShell(cp, 1e11, "canonical", None, "B", mond=False)
    A_f = math.exp(brentq(lambda x: msN.run(math.exp(x))["N_form"] - Nt, math.log(1.4 / cp.Du(Nt)), math.log(1.8 / cp.Du(Nt)), xtol=1e-9))
    A_c = math.exp(brentq(lambda x: msNc.run(math.exp(x))["N_coll"] - Nt, math.log(1.5 / cp.Du(Nt)), math.log(1.9 / cp.Du(Nt)), xtol=1e-9))
    A_fB = math.exp(brentq(lambda x: msNB.run(math.exp(x))["N_form"] - Nt, math.log(1.4 / cp.Du(Nt)), math.log(1.8 / cp.Du(Nt)), xtol=1e-9))
    s_f = math.exp(brentq(lambda x: C.collapse_single(cp, 1e11, math.exp(x), "canonical", None, "tophat", mond=False)[0] - Nt, math.log(1.4 / cp.Du(Nt)), math.log(1.8 / cp.Du(Nt)), xtol=1e-11))
    s_c = math.exp(brentq(lambda x: C.collapse_single(cp, 1e11, math.exp(x), "canonical", None, "tophat", mond=False)[1] - Nt, math.log(1.5 / cp.Du(Nt)), math.log(1.9 / cp.Du(Nt)), xtol=1e-11))
    d4 = max(abs(A_f / s_f - 1), abs(A_c / s_c - 1)); d4B = abs(A_fB / A_f - 1)
    check("K4 CONTROL: the multi-shell code in the Newtonian limit reproduces the single-shell top hat at z = 7 (formation at half "
          "the maximum radius: delta = 1.584; collapse r -> 0: 1.688), and reading B's two-species Newtonian limit equals T's",
          f"formation {A_f * cp.Du(Nt):.6f} vs {s_f * cp.Du(Nt):.6f}; collapse {A_c * cp.Du(Nt):.6f} vs {s_c * cp.Du(Nt):.6f}; B/T - 1 = {d4B:.1e}",
          d4 < 2e-5 and d4B < 1e-6)

    # K5 FP13's committed state reproduced
    F13 = json.load(open(os.path.join(C.CHAIN, "FP13_separator_from_state_results.json")))["numbers"]["H1"]
    st0 = state_of("V0")
    dev5 = max([abs(st0.L(1 / (1 + float(z))) / st0.Mpc * 1e3 / v - 1) for z, v in F13["L_kpc"].items()]
               + [abs(st0.y(1 / (1 + float(z)), "canonical") - v) / max(v, 1e-12) if v > 0 else st0.y(1 / (1 + float(z)), "canonical") for z, v in F13["yth"].items()])
    check("K5 CONTROL: FP13's committed state -- L(z) and y_th(z) at z = 0-3 (its H1 table) -- is reproduced by FP13's own "
          "machinery exec'd read-only", f"max rel dev {dev5:.1e}", dev5 < 1e-9)
    P(f"    {time.time() - T0:.0f} s")

    # ======================================================================================================== S
    banner("S  THE STATE AT HIGH z: the band-pass length L(z), the yield y_th(z), and where the band-pass closes")
    s1 = {}
    for var in VARIANTS:
        st = state_of(var)
        zgrid = np.linspace(0, 25, 2501); cl = np.array([st.closed(1 / (1 + z)) for z in zgrid])
        open_ = np.where(~cl)[0]
        z_close = float(zgrid[open_[-1] + 1]) if len(open_) and open_[-1] + 1 < len(zgrid) else (0.0 if not len(open_) else float("nan"))
        s1[var] = {"z_close": z_close, "L_kpc": {str(z): st.L(1 / (1 + z)) / st.Mpc * 1e3 for z in (0, 0.5, 1, 3, 6, 7, 8, 10, 12, 14, 17)},
                   "yth_can": {str(z): st.y(1 / (1 + z), "canonical") for z in (0, 0.5, 1, 3, 6, 7, 8, 10, 12, 14, 17)}}
        P(f"    {var} ({VAR_DESC[var]:36s}): band-pass closed for z >= {z_close:5.2f}; L [kpc] z=6/7/10/14: "
          + "/".join(f"{s1[var]['L_kpc'][str(z)]:.2f}" for z in (6, 7, 10, 14)) + "; y_th(can) z=6/7/10/14: "
          + "/".join(f"{s1[var]['yth_can'][str(z)]:.1e}" for z in (6, 7, 10, 14)))
    h1 = (11 <= s1["V1"]["z_close"] <= 16 and 15 <= s1["V0"]["z_close"] <= 19 and s1["V2"]["z_close"] <= 12 and s1["V3"]["z_close"] <= 12)
    check("S1 (H1) THE BAND-PASS CLOSES AT HIGH z: where the state's smallest-scale variance no longer reaches s, L = xi and chi = 0 "
          "-- the MOND sector is exactly off; closure by z = 11-16 on V1, 15-19 on V0 (FP13 as committed), <= 12 with the dark "
          "field's wave cut-off (V2, V3)",
          "; ".join(f"{v}: z_close {s1[v]['z_close']:.2f}" for v in ("V0", "V1", "V2", "V3", "V4", "V5", "V6", "V7")), h1, load_bearing=False)
    OUT["numbers"]["S1"] = s1

    # ======================================================================================================== grid
    ZT_T = Z_LOW + (2.0,) + Z_JWST + (15.0, 17.0, 20.0)                    # reading T multi-shell (XR23b's barrier nodes)
    ZT_B = Z_LOW + (6.0, 7.0, 10.0, 14.0)                                  # reading B: the reported cells
    ZT_R = (6.0, 7.0, 10.0, 14.0)                                          # robustness and brackets: the JWST era
    specs = []
    if MUTATE:
        for Mm in (1e9, 1e10, 1e11, 1e12):
            specs.append(("multi", "V1", "T", "canonical", Mm, True, Z_JWST))
    else:
        for var in ("V0", "V1"):
            for f in FOOTS:
                for Mm in M_ALL:
                    specs.append(("multi", var, "T", f, Mm, False, ZT_T))
                for Mm in M_B:
                    specs.append(("multi", var, "B", f, Mm, False, ZT_B))
        for var in ("V2", "V3", "V4", "V5", "V6", "V7"):
            for f in FOOTS:
                for Mm in M_ROB:
                    specs.append(("multi", var, "T", f, Mm, False, ZT_R))
        for f in FOOTS:
            for Mm in M_BR:
                specs += [("single_tophat", "V1", "T", f, Mm, False, ZT_R), ("single_point", "V1", "T", f, Mm, False, ZT_R)]
    specs.sort(key=lambda s_: (s_[0] != "multi", s_[2] != "B"))
    P(f"\n  the grid: {len(specs)} models x ({NA} amplitudes + per-target refinement) on {NPROC} worker processes  [{time.time() - T0:.0f} s]")
    with get_context("spawn").Pool(NPROC) as pool:
        res = pool.map(job, specs, chunksize=1)
    R = {tuple(r["spec"][:6]): r for r in res}
    P(f"  grid done  [{time.time() - T0:.0f} s]; slowest model {max(r['sec'] for r in res):.0f} s; refinement runs {sum(r['runs'] for r in res)}")

    _lcdm_table(cp)

    def ratio(model, var, reading, foot, Mm, z, mut=False, conv="form"):
        """A_chain/A_LCDM at formation (or r -> 0) redshift z, from the refined amplitudes."""
        r = R.get((model, var, reading, foot, Mm, mut))
        if r is None or conv not in r or str(z) not in r[conv]:
            return float("nan")
        x = r[conv][str(z)]
        return math.exp(x - lnA_lcdm(cp, math.log(1.0 / (1.0 + z)), conv)) if np.isfinite(x) else float("nan")

    def dceff(model, var, reading, foot, Mm, z, mut=False):
        return dcl[z] * ratio(model, var, reading, foot, Mm, z, mut)

    mono_bad = [k for k, r in R.items() if not r["mono"]]
    P(f"  monotone amplitude -> formation maps: {len(R) - len(mono_bad)}/{len(R)}" + (f"; non-monotone: {mono_bad}" if mono_bad else ""))
    OUT["numbers"]["grid"] = {"|".join(str(x) for x in k): {"N_form": r.get("N_form"), "N_coll": r.get("N_coll"), "lnA_form": r.get("form"),
                                                             "lnA_coll": r.get("coll"), "bary": r.get("bary"), "mono": r["mono"],
                                                             "n_ok": r["n_ok"], "runs": r["runs"], "sec": r["sec"]} for k, r in R.items()}
    OUT["numbers"]["A_grid"] = a_grid(cp).tolist()

    # ======================================================================================================== K6/K7 (need the grid)
    if not MUTATE:
        banner("K  CONTROLS (numerical): convergence and interpolation")
        st1 = state_of("V1")
        Nt = math.log(1 / 8.0)

        def root(ms, lo=1.3, hi=1.8):
            return math.exp(brentq(lambda x: ms.run(math.exp(x))["N_form"] - Nt, math.log(lo / cp.Du(Nt)), math.log(hi / cp.Du(Nt)), xtol=1e-8))
        base0 = root(C.MultiShell(cp, 1e10, "canonical", None, "T", mond=False))
        b1 = root(C.MultiShell(cp, 1e10, "canonical", st1, "T")) / base0
        b2 = root(C.MultiShell(cp, 1e10, "canonical", st1, "T", N_in=48, N_out=48)) / root(C.MultiShell(cp, 1e10, "canonical", None, "T", mond=False, N_in=48, N_out=48))
        b3 = root(C.MultiShell(cp, 1e10, "canonical", st1, "T", stepf=0.01)) / root(C.MultiShell(cp, 1e10, "canonical", None, "T", mond=False, stepf=0.01))
        dconv = max(abs(b2 - b1), abs(b3 - b1))
        check("K6 CONTROL: the multi-shell result is converged -- doubling the shells (24+24 -> 48+48) or halving the step moves "
              "the amplitude ratio at the largest high-z cell of the pre-run (1e10 Msun, z = 7, V1, T) by less than 10% of its shift",
              f"ratio {b1:.5f} (base) / {b2:.5f} (shells x2) / {b3:.5f} (step/2); max change {dconv:.1e} vs shift {abs(1 - b1):.1e}",
              dconv < 0.1 * abs(1 - b1) + 2e-4)
        k7 = {}
        for (Mm, zc, var) in ((1e10, 7.0, "V1"), (1e10, 6.0, "V0"), (1e11, 7.0, "V0"), (1e12, 0.5, "V0"), (1e11, 0.25, "V1")):
            Ntt = math.log(1 / (1 + zc)); stv = state_of(var)
            msv = C.MultiShell(cp, Mm, "canonical", stv, "T")
            AL = math.exp(lnA_lcdm(cp, Ntt))
            Fv = lambda x: msv.run(math.exp(x))["N_form"] - Ntt
            lo, hi = math.log(AL * 0.02), math.log(AL * 1.2)
            xs = np.linspace(lo, hi, 12); fs = [Fv(x) for x in xs]
            j = next(i for i in range(len(xs) - 1) if np.isfinite(fs[i]) and np.isfinite(fs[i + 1]) and fs[i] * fs[i + 1] < 0)
            Ad = math.exp(brentq(Fv, xs[j], xs[j + 1], xtol=1e-9))
            k7[(Mm, zc, var)] = (ratio("multi", var, "T", "canonical", Mm, zc), Ad / AL)
        dev7 = max(abs(v[0] - v[1]) for v in k7.values())
        check("K7 CONTROL: the refined amplitudes (a coarse grid, then each target redshift refined with the model itself) equal an "
              "independent root finding at five "
              "cells spanning the high-z and z = 0-1 regimes (reading T, canonical)",
              "; ".join(f"{k[0]:.0e}, z={k[1]:g}, {k[2]}: {v[0]:.5f} vs {v[1]:.5f}" for k, v in k7.items()) + f"; max |dev| {dev7:.1e}",
              dev7 < 3e-4)
        OUT["numbers"]["K7"] = {f"{k[0]:.0e}|{k[1]}|{k[2]}": v for k, v in k7.items()}

    # ======================================================================================================== C
    banner("C  THE JWST ERA (z = 6-20): the chain's threshold against LCDM's")
    c0_cells = ([("V1", "canonical", Mm) for Mm in (1e11, 1e12)] if MUTATE else
                [(var, f, Mm) for var in ("V0", "V1") for f in FOOTS for Mm in M_ALL if Mm >= 1e11])
    c0v = [ratio("multi", var, "T", f, Mm, z, MUTATE) for (var, f, Mm) in c0_cells for z in Z_JWST]
    c0 = max([abs(v - 1) for v in c0v if np.isfinite(v)] or [float("inf")])
    if not all(np.isfinite(c0v)):
        c0 = float("inf")                                                   # a cell outside the amplitude grid counts as a failure
    check("C0 THE BAND-PASS CONFINES THE CHAIN'S MOND AT JWST HOST MASSES: reading T's threshold (multi-shell) moves by < 5% at "
          "M >= 1e11 Msun, z = 6-14" + (" [MUTATE: band-pass removed, V1, canonical]" if MUTATE else " (V0 and V1, both footings)"),
          f"max |A_chain/A_LCDM - 1| = {c0:.2%}", c0 < 0.05)
    if MUTATE:
        rows_m = {Mm: {z: ratio("multi", "V1", "T", "canonical", Mm, z, True) for z in Z_JWST} for Mm in (1e9, 1e10, 1e11, 1e12)}
        for Mm, rw in rows_m.items():
            P(f"    [MUTATE] M = {Mm:.0e}: A_chain/A_LCDM " + ", ".join(f"z={z:g}: {v:.4f}" for z, v in rw.items()))
        worst = max(abs(v - 1) for Mm, rw in rows_m.items() if Mm >= 1e10 for v in rw.values() if np.isfinite(v))
        worst11 = max(abs(v - 1) for Mm, rw in rows_m.items() if Mm >= 1e11 for v in rw.values() if np.isfinite(v))
        check("C1 (H2) READING T: the chain's threshold is within 1% of LCDM's for M >= 1e11 and 3% for M >= 1e10 at z = 6-14 "
              "(multi-shell, V0 and V1, both footings)", f"[MUTATE, V1 canonical] max |shift| M>=1e11 {worst11:.1%}, M>=1e10 {worst:.1%}",
              worst11 <= 0.01 and worst <= 0.03, load_bearing=False)
        OUT["numbers"]["C1_mutate"] = {str(k): v for k, v in rows_m.items()}
    else:
        c1 = {}
        for var in ("V0", "V1"):
            for f in FOOTS:
                for Mm in M_ALL:
                    c1[(var, f, Mm)] = {z: ratio("multi", var, "T", f, Mm, z) for z in ZS}
        for var in ("V0", "V1"):
            P(f"    reading T, multi-shell, {var} ({VAR_DESC[var]}): delta_c,eff(M, z) [canonical | alt]")
            for Mm in M_ALL:
                P(f"      M = {Mm:.0e}: " + ", ".join(f"z={z:g}: {dcl[z] * c1[(var, 'canonical', Mm)][z]:.4f}|{dcl[z] * c1[(var, 'alt', Mm)][z]:.4f}" for z in Z_JWST))
        sh = lambda Mmin: max(abs(v[z] - 1) for (var, f, Mm), v in c1.items() if Mm >= Mmin for z in Z_JWST if np.isfinite(v[z]))
        check("C1 (H2) READING T: the chain's threshold is within 1% of LCDM's for M >= 1e11 and 3% for M >= 1e10 at z = 6-14 "
              "(multi-shell, V0 and V1, both footings)",
              f"max |shift| M>=1e11 {sh(1e11):.2%}, M>=1e10 {sh(1e10):.2%}, M>=1e9 {sh(1e9):.2%}, M>=1e8 {sh(1e8):.2%}",
              sh(1e11) <= 0.01 and sh(1e10) <= 0.03, load_bearing=False,
              reading=f"the band-pass passes a halo's field only within ~2L of its centre, and L(z = 6-14) is "
                      f"{s1['V0']['L_kpc']['14']:.2f}-{s1['V0']['L_kpc']['6']:.1f} kpc (V0) / {s1['V1']['L_kpc']['14']:.2f}-{s1['V1']['L_kpc']['6']:.1f} kpc (V1): "
                      "the MOND phantom acts only in the last stretch of infall of the smaller halos")
        OUT["numbers"]["C1"] = {f"{k[0]}|{k[1]}|{k[2]:.0e}": {str(z): v for z, v in vv.items()} for k, vv in c1.items()}
        c2 = {}; bi = {}
        for var in ("V0", "V1"):
            for f in FOOTS:
                for Mm in M_B:
                    c2[(var, f, Mm)] = {z: ratio("multi", var, "B", f, Mm, z) for z in ZS}
                    bb = R[("multi", var, "B", f, Mm, False)].get("bary", {})
                    bi[(var, f, Mm)] = {z: float(bb.get(z, bb.get(str(z), float("nan")))) for z in ZS}
        shB = max(abs(v[z] - 1) for v in c2.values() for z in (6.0, 7.0, 10.0, 14.0) if np.isfinite(v[z]))
        biB = max([abs(b[z] - 1) for b in bi.values() for z in (6.0, 7.0, 10.0, 14.0) if np.isfinite(b[z])] or [float("nan")])
        P("    reading B (the action's content): dark-halo formation shift, max over V0/V1, footings, M = 1e9-1e14, z = 6-14: "
          f"{shB:.2e}; baryons inside the dark shell at formation / (f_b M): max |dev| {biB:.1e}")
        for var in ("V0", "V1"):
            P(f"      {var} canonical: " + "; ".join(f"M={Mm:.0e}: " + ",".join(f"{c2[(var, 'canonical', Mm)][z]:.5f}" for z in (6.0, 7.0, 10.0, 14.0)) for Mm in M_B))
        check("C2 (H3) READING B: the dark halo forms on LCDM's schedule (<= 0.1%) and holds f_b M of baryons (<= 1%) at every "
              "cell z = 6-14 -- the phantom acts on the baryons, which are inside the dark shell already",
              f"max |shift| {shB:.2e}; max |bary_in - 1| {biB:.1e}", shB <= 1e-3 and (biB <= 0.01 or not np.isfinite(biB)), load_bearing=False)
        OUT["numbers"]["C2"] = {f"{k[0]}|{k[1]}|{k[2]:.0e}": {str(z): v for z, v in vv.items()} for k, vv in c2.items()}
        OUT["numbers"]["C2_bary_in"] = {f"{k[0]}|{k[1]}|{k[2]:.0e}": {str(z): v for z, v in vv.items()} for k, vv in bi.items()}
        c3 = {}
        for prof in ("tophat", "point"):
            for f in FOOTS:
                for Mm in M_BR:
                    c3[(prof, f, Mm)] = {z: ratio("single_" + prof, "V1", "T", f, Mm, z) for z in ZS}
                    c3[(prof + "_coll", f, Mm)] = {z: ratio("single_" + prof, "V1", "T", f, Mm, z, conv="coll") for z in ZS}
        for prof in ("tophat", "point"):
            P(f"    single-shell bracket '{prof}' (V1, canonical), formation | r -> 0 conventions:")
            for Mm in M_BR:
                P(f"      M = {Mm:.0e}: " + ", ".join(f"z={z:g}: {c3[(prof, 'canonical', Mm)][z]:.4f}|{c3[(prof + '_coll', 'canonical', Mm)][z]:.4f}" for z in ZT_R))
        tb = max(abs(v[z] - 1) for (p_, f, Mm), v in c3.items() if p_ in ("tophat", "tophat_coll") and Mm >= 1e10 for z in Z_JWST if np.isfinite(v[z]))
        pt = max(abs(v[z] - 1) for (p_, f, Mm), v in c3.items() if p_ in ("point", "point_coll") and Mm >= 1e10 for z in Z_JWST if np.isfinite(v[z]))
        check("C3 (H4) THE BRACKETS: the sharp-edged top hat (the most MOND the band-pass allows) moves the threshold by <= 8% and "
              "the compact profile by <= 1% at M >= 1e10, z = 6-14 (both conventions, both footings)",
              f"top hat max |shift| {tb:.2%}; compact {pt:.2%}", tb <= 0.08 and pt <= 0.01, load_bearing=False)
        OUT["numbers"]["C3"] = {f"{k[0]}|{k[1]}|{k[2]:.0e}": {str(z): v for z, v in vv.items()} for k, vv in c3.items()}

        # ==================================================================================================== D
        banner("D  THE L-SETTING EPOCHS (z = 0-1): is the chain's own collapse threshold a single number in FP13's window 1.3-2.6?")
        MLz = {}
        for var in ("V0", "V1"):
            st = state_of(var)
            for z in Z_LOW:
                Lc = st.L(1 / (1 + z)) / st.Mpc * (1 + z)                                   # comoving Mpc
                MLz[(var, z)] = (2 * math.pi) ** 1.5 * cp.Om * cp.rho_c0 * (Lc * st.Mpc) ** 3 / g["MSUN"]   # FP13's M_* formula
        lm = np.log10(M_ALL)

        def at_mass(var, reading, foot, Mv, z):
            vals = np.array([ratio("multi", var, reading, foot, Mm, z) if (reading == "T" or Mm in M_B) else np.nan for Mm in M_ALL])
            ok = np.isfinite(vals)
            return float(dcl[z] * np.interp(math.log10(Mv), lm[ok], vals[ok])) if ok.sum() >= 2 else float("nan")
        d1 = {}
        for var in ("V0", "V1"):
            for f in FOOTS:
                for z in Z_LOW:
                    d1[(var, f, z)] = (MLz[(var, z)], at_mass(var, "T", f, MLz[(var, z)], z))
        for var in ("V0", "V1"):
            P(f"    reading T, {var}: delta_c,eff at M = 1e11..1e15 [canonical]:")
            for z in Z_LOW:
                P(f"      z = {z:4.2f}: " + ", ".join(f"{Mm:.0e}: {dceff('multi', var, 'T', 'canonical', Mm, z):.3f}" for Mm in M_ALL if Mm >= 1e11)
                  + f"  | at M_L(z) = {MLz[(var, z)]:.1e}: {d1[(var, 'canonical', z)][1]:.3f} (can) / {d1[(var, 'alt', z)][1]:.3f} (alt)")
        vals_ML = [v[1] for v in d1.values()]
        spread_z = max(max(d1[(var, f, z)][1] for z in Z_LOW) - min(d1[(var, f, z)][1] for z in Z_LOW) for var in ("V0", "V1") for f in FOOTS)
        spread_M = max(max(dceff("multi", var, "T", f, Mm, z) for Mm in M_ALL if Mm >= 1e11) - min(dceff("multi", var, "T", f, Mm, z) for Mm in M_ALL if Mm >= 1e11)
                       for var in ("V0", "V1") for f in FOOTS for z in Z_LOW)
        inwin = [(k, v[1]) for k, v in d1.items() if 1.3 <= v[1] <= 2.6]
        z0below = all(d1[(var, f, 0.0)][1] < 1.3 for var in ("V0", "V1") for f in FOOTS)
        check("D1 (H5) READING T: the chain's own threshold at the band-pass mass M_L(z) is NOT one number in FP13's window -- below "
              "1.3 at z = 0 and spread by > 0.3 over z = 0-1 (both variants, both footings)",
              f"at M_L(z): range {min(vals_ML):.3f}-{max(vals_ML):.3f}; in [1.3, 2.6] for {len(inwin)}/{len(d1)} cells; spread over z "
              f"(max) {spread_z:.3f}; spread over M = 1e11-1e15 at fixed z (max) {spread_M:.3f}; below 1.3 at z = 0: {z0below}",
              z0below and spread_z > 0.3,
              reading=f"with the yield off (z < 0.635) and L ~ 1-3 Mpc the band-passed peculiar field of a sub-L perturbation is deep-MOND: "
                      f"at z = 0 the threshold runs {dceff('multi', 'V0', 'T', 'canonical', 1e11, 0.0):.2f} (1e11) to "
                      f"{dceff('multi', 'V0', 'T', 'canonical', 1e15, 0.0):.2f} (1e15); at M_L(z) it runs {d1[('V0', 'canonical', 0.0)][1]:.2f} (z = 0) "
                      f"to {d1[('V0', 'canonical', 1.0)][1]:.2f} (z = 1) -- a single s cannot be read off it", load_bearing=False)
        OUT["numbers"]["D1"] = {f"{k[0]}|{k[1]}|{k[2]}": {"M_L": v[0], "dc_eff": v[1]} for k, v in d1.items()}
        OUT["numbers"]["D1_table"] = {f"{var}|{f}|{Mm:.0e}": {str(z): dceff("multi", var, "T", f, Mm, z) for z in Z_LOW} for var in ("V0", "V1") for f in FOOTS for Mm in M_ALL}
        d2 = {(var, f, Mm): {z: dceff("multi", var, "B", f, Mm, z) for z in Z_LOW} for var in ("V0", "V1") for f in FOOTS for Mm in M_B}
        devB = max(abs(v[z] / dcl[z] - 1) for v in d2.values() for z in Z_LOW if np.isfinite(v[z]))
        P("    reading B (dark halos): delta_c,eff at z = 0-1, V0 canonical: " + "; ".join(f"{Mm:.0e}: " + ",".join(f"{d2[('V0', 'canonical', Mm)][z]:.3f}" for z in Z_LOW) for Mm in M_B))
        check("D2 (H5) READING B: the dark halos' threshold at z = 0-1 is GR's (the dark field ignores the phantom) to <= 1% at every "
              "M = 1e9-1e14 -- inside FP13's window, but as GR's number, not a MOND-sector one",
              f"max |delta_c,eff/delta_c^LCDM - 1| = {devB:.2%}", devB <= 0.01, load_bearing=False)
        OUT["numbers"]["D2"] = {f"{k[0]}|{k[1]}|{k[2]:.0e}": {str(z): v for z, v in vv.items()} for k, vv in d2.items()}

        # ==================================================================================================== R
        banner("R  ROBUSTNESS (reading T, multi-shell): the separator threshold window, the dark field's mass, the footings")
        r1 = {}
        for var in ("V2", "V3", "V4", "V5", "V6", "V7"):
            for f in FOOTS:
                for Mm in M_ROB:
                    r1[(var, f, Mm)] = {z: ratio("multi", var, "T", f, Mm, z) for z in ZS}
            P(f"    {var} ({VAR_DESC[var]}): " + "; ".join(f"M={Mm:.0e}: " + ",".join(f"{r1[(var, 'canonical', Mm)][z]:.4f}" for z in (6.0, 7.0, 10.0, 14.0)) for Mm in M_ROB))
        rob11 = max(abs(v[z] - 1) for (var, f, Mm), v in r1.items() if Mm >= 1e11 for z in Z_JWST if np.isfinite(v[z]))
        rob10 = max(abs(v[z] - 1) for (var, f, Mm), v in r1.items() if Mm >= 1e10 for z in Z_JWST if np.isfinite(v[z]))
        check("R1 (H6) ROBUSTNESS: over FP13's threshold window (s = 1.3, 2.6 on both spectra), the dark field's mass (1.9e-19, "
              "5.2e-19 eV) and both footings, reading T's shift stays within 5% at M >= 1e11, z = 6-14",
              f"max |shift| M>=1e11 {rob11:.2%}; M>=1e10 {rob10:.2%}", rob11 <= 0.05, load_bearing=False)
        OUT["numbers"]["R1"] = {f"{k[0]}|{k[1]}|{k[2]:.0e}": {str(z): v for z, v in vv.items()} for k, vv in r1.items()}

    # ======================================================================================================== barrier table for XR23b
    bar = {}
    for k, r in R.items():
        model, var, reading, foot, Mm, mut = k
        if var is None:
            continue
        key = f"{model}|{var}|{reading}|{foot}|{'MUT' if mut else 'main'}"
        bar.setdefault(key, {})[f"{Mm:.0e}"] = {str(z): ratio(model, var, reading, foot, Mm, z, mut) for z in ZS}
    OUT["barrier_ratio"] = bar
    OUT["zs"] = list(ZS)

    # ======================================================================================================== ledger + verdict
    nlb = sum(1 for _, ok, lb in CH if lb and not ok)
    banner("VERDICT")
    if MUTATE:
        P("  MUTATE: with the band-pass removed the chain's MOND reads every halo's full peculiar field (y ~ 0.1-1 early on) and the")
        P("  threshold collapses far below LCDM's (most cells fall below the amplitude grid) -- C0 fails, as pre-declared.")
    else:
        P(f"  JWST era: the band-pass closes the MOND sector at z >= {s1['V1']['z_close']:.1f} (V1; {s1['V0']['z_close']:.1f} as committed; "
          f"{s1['V2']['z_close']:.1f}/{s1['V3']['z_close']:.1f} with the wave cut-off); below that L(z = 6) is {s1['V1']['L_kpc']['6']:.1f} kpc (V1) / "
          f"{s1['V0']['L_kpc']['6']:.1f} kpc (V0).")
        P(f"  Reading T moves the threshold by at most {sh(1e11):.2%} at M >= 1e11 and {sh(1e10):.2%} at M >= 1e10 (z = 6-14); reading B (the")
        P(f"  action's content) by {shB:.1e}.  The sharp-edged top hat, the most the band-pass allows, reaches {tb:.1%}.")
        bvals = [v[z] for v in d2.values() for z in Z_LOW if np.isfinite(v[z])]
        P(f"  z = 0-1 (the coordinator's question): reading T's threshold at the band-pass mass runs {min(vals_ML):.2f}-{max(vals_ML):.2f} and over")
        zb = [z for z in Z_LOW if all(d1[(var, f, z)][1] < 1.3 for var in ("V0", "V1") for f in FOOTS)]
        P(f"  M = 1e11-1e15 spreads by up to {spread_M:.2f} at fixed z: not one number; below FP13's window at z = {zb}.  Reading B gives")
        P(f"  {min(bvals):.3f}-{max(bvals):.3f} (GR's {dcl[0.0]:.3f}-{dcl[1.0]:.3f}; the baryons' MOND infall lowers it by up to {devB:.1%} at z = 0).")
    P(f"  Not 'closed'.  Time {time.time() - T0:.0f} s.")
    OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
    fn = os.path.join(OUTDIR, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
    json.dump(OUT, open(fn, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating, np.integer)) else str(o)))
    P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}")
    sys.exit(0 if nlb == 0 else 1)


if __name__ == "__main__":
    main()
