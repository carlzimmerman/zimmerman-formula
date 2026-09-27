#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR18 (H_S) -- FP13's STATE SEPARATOR, AUDITED AS AN ACTION: what varying H_S's leaf-averaged state functionals puts into the
field equations, whether the matter readout is something an action can read, and whether FRW growth across the q = 0 ramp
is well posed.

WHY.  FP13 (derivation_chain_2026/FP13_separator_from_state.py, 27faacc84) replaced FP9's four declared constants by state
functionals (per 1/16 pi G, c = 1):
  chi = (S_xi - S_B) phi,  B = L^2/2 fixed by <(S_B delta_m)^2>_h = delta_c^2 (delta_c = 1.686),
  delta_m = D_i(a^i - D^i chi)/(<K>_h^2/6 - Lambda/2)   (the MATTER readout: the chassis's Newtonian combination),
  J_Y = J_P2 + 2 y_th sqrt(Y),  y_th = c_y <|(S_xi - S_B)(a - D chi)|^2>_h^(1/2)/a0 x max(0, 2q),  2q = 1 + Omega_r - 9 Lambda/<K>_h^2,
  c_y = 1, the ramp switching the yield off once the leaf accelerates (z = 0.635); FP7's lambda > 0 required.
FP13 A1 checked that the derivative of the leaf-averaged VARIANCE with respect to a local field is O(1/V) and concluded that
the state-length term "adds no local term to the field equations"; its scoring then treats L(a) and y_th(a) as given
background functions.  But the action depends on B (and y_th) through an integral over the whole leaf, dS/dB = O(V), so the
variation through the state functional is O(V) x O(1/V) = O(1): a LOCAL term with a leaf-averaged (intensive) coefficient.
This lane derives those terms, measures them on FP13's own headline state, and asks what they do.

THE MEAN-FIELD TERMS (derived here; weak field, psi = Phi - chi the Newtonian combination, delta_m = lap psi/(4 pi G rho_bar)):
  (B)  d^2 S = (dS/dB) d^2 B = E_B Int (S_B d delta_m)^2 d^3x,   E_B = <dL/dB>/(2 <|grad S_B delta_m|^2>) > 0,
       <dL/dB> = rho_bar <delta lap S_B phi> = 4 pi G rho_bar^2 Int Delta^2 h C^Q e^(-B k^2) dln k  (phi_k = -4 pi G h C^Q rho_bar delta_k/k^2);
       in the psi-equation: psi_k = -4 pi G rho_k/(k^2 (1 - R_B)),  R_B(k) = [Int Delta^2 h C^Q e^(-Bk'^2) / Int k'^2 Delta^2 e^(-2Bk'^2)] k^2 e^(-2Bk^2)
       -- an ENHANCEMENT of Newtonian gravity at k ~ 1/L, singular at R_B = 1; UV-suppressed as e^(-2Bk^2) (DE12's mechanism evaded).
  (Y)  d^2 S = (dS/dy_th) d^2 y_th = -(a0 <x> c_y 2q / (8 pi G g_rms)) Int |d g_bp|^2 d^3x  (x = |grad phi|/a0; <x> the leaf mean)
       -- an extra gradient energy on psi: psi_k = -4 pi G rho_k/(k^2 (1 + kappa h^2 - R_B)),  kappa = c_y 2q <x>/y_rms (y_rms = g_rms/a0):
       a SCREENING of sub-L Newtonian gravity at z > 0.635 (the MOND scalar's own source B^T rho is not screened).
  Both act on psi only; their coefficients are leaf averages of the whole state (the power spectrum, the MOND response, the
  one-point distribution of |g_bp|), so local physics depends on the whole leaf's state; one distant structure changes them
  by its share of the leaf (~V_struct/V_leaf).

PRE-DECLARED (written into this file before its first full run; this file is written after the coordinator's 2026-09-27
redirect; exploratory runs disclosed in XR18_README.md: none for this file beyond reading FP13's committed outputs)
 HS1 [load-bearing] THE LOCAL TERM EXISTS: on periodic leaves with a fixed cell size (N = 8, 16, 32), for an action whose only
     dependence on the density contrast is through B[delta] (a leaf-averaged variance condition), the derivative of B itself
     scales as 1/V (FP13 A1 reproduced: N^3 |dB/d delta| N-independent within 20%), while the ACTION's gradient per cell is
     N-independent (within 20%) and equals the derived 2 E_B (S_B^2 delta)(x) within 5%: FP13 A1's "adds no local term" does
     not hold for the action.
 HS2 [load-bearing] MOMENTUM IS CONSERVED WITH THE MEAN-FIELD TERMS: the net mean-field force Int delta grad(S_B^2 delta) (the
     translation Noether identity, the leaf average being translation-covariant) vanishes to 1e-10 relative on the leaves.
 HS3 [load-bearing] ON FP13's HEADLINE STATE THE B-TERM IS BOUNDED AND DOES NOT MOVE sigma_8 OUT OF THE BAND: R_B(k) < 1 at
     every scanned epoch z = 0 .. 3 (the psi-constraint stays regular), and sigma_8 with the B-term in the growth yardstick stays in
     [0.922, 1.05] on both footings and both modes.
 HS4 [load-bearing; the adversarial one] THE Y-TERM IS O(1) IN FP13's OWN (GAUSSIAN, PER-MODE) READING OF THE WEB: with the
     band-passed field's one-point distribution Gaussian (Maxwell |g|, the reading FP13's per-mode yardstick implies),
     kappa(z = 1 .. 3) > 1 and the flagship (1e10, 1e11 at 0.1 a0, z = 2.5) moves by more than 0.05 dex once the Newtonian part is
     screened; with a halo-dominated field (Press-Schechter halos, FP9's yield-law bubbles) kappa < 0.1.
 HS5 [load-bearing] FRW GROWTH ACROSS THE q = 0 RAMP IS WELL POSED: with the ramp smoothed (softplus width eps), sigma_8 converges
     monotonically to FP13's value (within 1e-4 at the smallest eps); every sigma_8 mode crosses the yield at most once (y_th
     falls, the field grows); the chord G_eff is continuous through z = 0.635 with the ramp (the step variant's jump is reported).
 HS6 [load-bearing] lambda AT THE SWITCH-OFF: on exact FRW with the band-pass closed (h = 0) FP7's block determinant is
     proportional to lambda (phi has no equation at lambda = 0: FP13 A1 reproduced from FP7's committed det); with structure, the
     rate at which phi un-freezes, omega_r = c k sqrt(C_L^phi/lambda_eff), exceeds 10 H(z = 0.635) for every sub-L sigma_8 mode
     (h >= 0.4) at lambda <= 100 for c_2 = 7.29e-3 and c_2 -> oo (FP14): the quasi-static yardstick holds through the switch-off.
 HS7 [load-bearing; the shared yield structure] at z >= 1 H_S's yield surfaces on DE12's hosts (z = 1, 2.5, 4; three masses; both
     footings) obey criterion B's causal part (all roots of the exact block real and >= 0) and the degenerate exponents
     (C_L ~ d^(0.50 +- 0.02)).
The writer's expectation before running: HS1, HS2, HS5, HS6, HS7 pass; HS3 is uncertain (a rough estimate put R_B ~ 0.5 at
z = 0.25); HS4 is uncertain in both parts.

CHECKS
  K1 CONTROL: FP13's machinery (its module and main()'s body up to its K banner, exec'd read-only; nothing is written) reproduces
     FP13's committed headline exactly: L(z), y_th(z), sigma_8 x4, forest x4, flagships x4, SPARC, KiDS (0.25, 0.4, 0.7).
  K2 CONTROL: FP7's committed det M at sigma -> 0 and C_phi = 0 equals FP13 A1's printed h = 0 determinant (proportional to lambda).
  N1 = HS1 (tiled leaves).  N2 = HS2 (+ MUTATE's target).  N3 = HS3.  N4 = HS4.  Q1 = HS5.  Q2 = HS6.  Y1 = HS7.
  N3b [ADDED AFTER the first (MUTATE) run found max R_B ~ 8; written before its own first run]: the B-term checked independently --
     the exact second derivative of the linearised H_S reduced action on a 32^3 leaf, B re-solved at every step: its B-part is
     positive and equals the derived R_B(q) x the Newtonian part within 10% (q = 2 pi j/32, j = 1..6).
  Development record (disclosed in XR18_README.md): the first (MUTATE) run compared independent random leaves per N in N1 (the
  N^3 scaling then scattered by realisation, 0.31-0.68) -- N1 now tiles one base leaf; Q1 compared the ramp's chord step with 5x
  the typical step on one grid (failed: the sqrt onset is steep) -- Q1 now tests continuity by refinement; Y1 located r_Y on a
  grid (1e-7 relative error, which flattened the d/r_Y = 1e-10 fits) -- now brentq.  The hypotheses' text is unchanged.
  After the first recorded main run: Q1's refinement test took its epochs from growth_aq's output keys, which always include
  an appended z = 0; the 'largest step' it reported (18.15, unshrinking) was the change between z = 0.615 and z = 0, not a
  step at the switch.  The epochs are now restricted to the window |z - z_q0| <= 0.02 (the test as declared); the per-mode
  crossing epochs and the tabulated y_th near z_q0 are printed (reported).  The VERDICT text now prints the measured numbers and
  reads correctly under MUTATE, and the pass count counts every check.  MUTATE and main were then re-run in that order.
  R1 (item 2, reported + load-bearing parts inside N3): the matter readout reads D_i a^i: no time derivative (the lapse stays
     non-dynamical, no Ostrogradsky mode); the psi-constraint's symbol k^2 (1 + kappa h^2 - R_B) is the only change (regular iff
     R_B < 1 + kappa h^2); the leaf-averaged read's k^0-type term is suppressed as e^(-2Bk^2): at k = 1/kpc relative to 1e6 K gas
     pressure it is printed (DE12's UV mechanism evaded); its large-scale anti-pressure growth is printed.
  R2 (reported) the ramp: the action is Lipschitz in <K>_h (max(0, 2q) is C^0), its <K>-derivative jumps at q = 0 by a finite
     amount (no delta-function force); the y-term's coefficient is continuous (proportional to 2q).
MUTATE=1 replaces the leaf average by a position-weighted average (a fixed window w(x) = 1 + 0.5 cos(2 pi x/N), not
translation-covariant): N2 (momentum conservation) must FAIL, rc = 1.

SCOPE.  Weak-field, frozen-coefficient mean-field terms at second order; FP13's per-mode chord C^Q for the MOND response;
FP13's halofit state; the growth yardstick modified only by the derived mean-field factors; the Gaussian and halo readings
of the one-point field distribution are brackets, not a computation of the theory's own nonlinear web (a PM run's job).
kappa = 1/2 is FITTED (Z = 5.7888).  No particle-mesh run.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR18_state_separator.py
"""
import os, sys, io, re, json, math, time, contextlib, warnings
os.environ.setdefault("OMP_NUM_THREADS", "2"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
import numpy as np
import sympy as sp
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
from scipy.linalg import eigh
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR18_state_separator"
T0 = time.time()
_OUTF = open(os.path.join(HERE, SLUG + ("_MUTATE.out" if MUTATE else ".out")), "w")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _OUTF.write(s + "\n"); _OUTF.flush()


CH, OUT = [], {"lane": "XR18_HS", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}" if (ok or not MUTATE) else
          f"         reading (written for the unmutated theory; this MUTATE run fails the check):  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 112); P(t); P("=" * 112)


def el():
    return f"[{time.time() - T0:.0f} s]"


P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the leaf average is replaced by a fixed position-weighted window -- N2 must FAIL ***")

# ============================================================================================ FP13's machinery (read-only)
FP13 = os.path.join(REPO, "real_research", "derivation_chain_2026", "FP13_separator_from_state.py")
_s13 = open(FP13).read()
_mod = _s13[:_s13.index("\ndef main():")]
_body = _s13[_s13.index("\ndef main():") + len("\ndef main():"):
             _s13.index('    banner("K  CONTROLS: the reused machinery reproduces the record; the halofit, the state, FP11\'s hook")')]
_body = "\n".join(l_[4:] if l_.startswith("    ") else l_ for l_ in _body.split("\n"))
NS = {"__file__": FP13, "__name__": "fp13_machinery"}
_old = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(_mod, FP13, "exec"), NS)
        exec(compile(_body, FP13, "exec"), NS)
finally:
    if _old is None:
        os.environ.pop("MUTATE", None)
    else:
        os.environ["MUTATE"] = _old
F13 = json.load(open(os.path.join(REPO, "real_research", "derivation_chain_2026", "FP13_separator_from_state_results.json")))["numbers"]
F7 = json.load(open(os.path.join(REPO, "real_research", "derivation_chain_2026", "FP7_aqual_type_repair_results.json")))["numbers"]
M6, ns9 = NS["M6"], NS["ns9"]
A0, FOOTS, MODES = NS["A0"], NS["FOOTS"], NS["MODES"]
L_table, fun_of, yth_state, gates, model_of = NS["L_table"], NS["fun_of"], NS["yth_state"], NS["gates"], NS["model_of"]
STATE, LNA, AGR, KKF, LKF, sig2, two_q, DELTA_C = NS["STATE"], NS["LNA"], NS["AGR"], NS["KKF"], NS["LKF"], NS["sig2"], NS["two_q"], NS["DELTA_C"]
h_, Om, OL, H0, c_, Mpc, G, rho_crit0, MSUN = NS["h"], NS["Om"], NS["OL"], NS["H0"], NS["c"], NS["Mpc"], NS["G"], NS["rho_crit0"], NS["MSUN"]
Ez, dlnH, A_I, gfield, nu_p2, x_P2 = NS["Ez"], NS["dlnH"], NS["A_I"], NS["gfield"], NS["nu_p2"], NS["x_P2"]
KH, KHF, DI, DIF, sigma8_of, S8_LCDM, forest_proxy = NS["KH"], NS["KHF"], NS["DI"], NS["DIF"], NS["sigma8_of"], NS["S8_LCDM"], NS["forest_proxy"]
SIG8_BAND, FLAG_TOL, C2W, G6, MPCm = NS["SIG8_BAND"], NS["FLAG_TOL"], NS["C2W"], NS["G6"], NS["MPCm"]
growth_aq, YIELD, cutfac = NS["growth_aq"], NS["YIELD"], NS["cutfac"]
Z_Q0 = NS["Z_Q0"]
P(f"\n  FP13's machinery exec'd read-only (module + main()'s body up to its K banner; FP9/FP6 inside); a0 = {A0['canonical']:.4e} / "
  f"{A0['alt']:.4e}; q = 0 at z = {Z_Q0:.4f}   {el()}")

# ============================================================================================ K1 FP13's headline
banner("K1  CONTROL: FP13's committed headline (H_S), recomputed with its own machinery")
LH_tab = L_table(DELTA_C, "NL"); Lh = fun_of(LH_tab)
yh, yh_tab, rms_h = yth_state(LH_tab, "NL", "ramp", 1.0)
H = gates(Lh, yh, extra=True)
ref = F13["H1"]; devs = []
for grp in ("s8", "forest", "flag"):
    for k_, v in H[grp].items():
        rv = ref[grp][str(k_)]; devs.append(abs(v - rv) if rv == 0 else abs(v / rv - 1))
for grp, key in (("sparc", "sparc"), ("kids", "kids"), ("kids@0.4", "kids04"), ("kids@0.7", "kids07")):
    for f in FOOTS:
        devs.append(abs(H[grp][f] / ref[key][f] - 1))
for zz, v in ref["L_kpc"].items():
    devs.append(abs(1e3 * Lh(1 / (1 + float(zz))) / v - 1))
for zz, v in ref["yth"].items():
    vv = yh["canonical"](1 / (1 + float(zz))); devs.append(abs(vv - v) if v == 0 else abs(vv / v - 1))
k1dev = max(devs)
P(f"    sigma_8: " + ", ".join(f"{k_[0][:3]}/{k_[1]}: {v:.6f}" for k_, v in H["s8"].items()) + f"; KiDS {H['kids']}; KiDS@0.4 {H['kids@0.4']}; "
  f"L(0.25) = {1e3 * Lh(0.8):.1f} kpc; y_th(2.5) = {yh['canonical'](1 / 3.5):.4e}")
check("K1 CONTROL: FP13's machinery, exec'd read-only, reproduces FP13's committed H_S headline -- L(z) and y_th(z) tables, sigma_8 (4), "
      "forest (4), flagships (4), SPARC (2), KiDS at z = 0.25/0.4/0.7 (6)", f"max relative deviation {k1dev:.1e} over {len(devs)} numbers",
      k1dev <= 1e-9)
OUT["numbers"]["K1"] = {"dev": k1dev}
P(f"    {el()}")

# ============================================================================================ K2 lambda at h = 0
banner("K2  CONTROL: FP7's committed det M at sigma -> 0 (band-pass closed), C_phi = 0: proportional to lambda (FP13 A1)")
alm, c2m, Cph, lmm, sgm, kq_, wq_ = sp.symbols("alpha_c c_2 C_phi lam_ sigma k omega", real=True)
det7 = sp.sympify(re.sub(r"\blambda\b", "lam_", F7["B3"]["det"]),
                  locals={"alpha_c": alm, "c_2": c2m, "C_phi": Cph, "lam_": lmm, "sigma": sgm, "k": kq_, "omega": wq_})
det_h0 = sp.factor(det7.subs({sgm: 0, Cph: 0}))
fp13_str = "-64*k**6*lambda*omega**2*(alpha_c*c_2*k**2 + 3*alpha_c*c_2*omega**2 + 2*alpha_c*omega**2 - 2*c_2*k**2)"
fp13_det = sp.sympify(fp13_str.replace("lambda", "lam_"), locals={"alpha_c": alm, "c_2": c2m, "lam_": lmm, "k": kq_, "omega": wq_})
k2_ok = sp.simplify(det_h0 - fp13_det) == 0 and sp.simplify(det_h0.subs(lmm, 0)) == 0
P(f"    det M(sigma = 0, C_phi = 0) = {det_h0};  at lambda = 0: {sp.simplify(det_h0.subs(lmm, 0))}")
check("K2 CONTROL: FP7's committed zero-field det M with the band-pass closed (sigma -> 0) and no yield (C_phi = 0) equals FP13 A1's "
      "printed determinant and vanishes identically at lambda = 0 (phi has no equation)", f"match {k2_ok}", k2_ok)

# ============================================================================================ N1 N2 the lattice
banner("N1 N2  THE LOCAL MEAN-FIELD TERM ON PERIODIC LEAVES (fixed cell size), and momentum conservation")


def leaf_fields(N, seed=13, base=8):
    """a Gaussian random contrast on a base leaf of base^3 cells (cell size 1), TILED to N^3 (N = base, 2 base, 4 base): the tiled
    leaves are statistically identical, so any N-dependence of a per-cell quantity is pure volume scaling.  Normalised so that
    the S_B-smoothed variance reaches delta_c^2 at B = 2 (L = 2 cells)."""
    rng = np.random.default_rng(seed)
    kb = np.fft.fftfreq(base) * 2 * np.pi
    KX, KY, KZ = np.meshgrid(kb, kb, kb, indexing="ij"); K2b = KX ** 2 + KY ** 2 + KZ ** 2
    Pk = np.where(K2b > 0, np.exp(-K2b / (2 * 1.2 ** 2)) / np.maximum(K2b, 1e-12) ** 0.5, 0.0)
    d = np.real(np.fft.ifftn(np.fft.fftn(rng.standard_normal((base, base, base))) * np.sqrt(Pk)))
    d *= DELTA_C / np.sqrt(np.mean(np.real(np.fft.ifftn(np.fft.fftn(d) * np.exp(-2.0 * K2b))) ** 2))
    m = N // base
    d = np.tile(d, (m, m, m))
    kx = np.fft.fftfreq(N) * 2 * np.pi
    KX, KY, KZ = np.meshgrid(kx, kx, kx, indexing="ij")
    return d, KX ** 2 + KY ** 2 + KZ ** 2


def smooth(f, K2, B):
    return np.real(np.fft.ifftn(np.fft.fftn(f) * np.exp(-B * K2)))


def weight(N):
    if not MUTATE:
        return np.ones((N, N, N))
    x = np.arange(N)
    return (1 + 0.5 * np.cos(2 * np.pi * x / N))[:, None, None] * np.ones((1, N, N))


def solve_B(d, K2, wt):
    F = lambda B: float(np.sum(wt * smooth(d, K2, B) ** 2) / np.sum(wt)) - DELTA_C ** 2
    return brentq(F, 1e-6, 50.0, xtol=1e-14)


n1 = {}
for N in (8, 16, 32):
    d, K2 = leaf_fields(N)
    hB = lambda B: 1 - np.exp(-B * K2)
    wt = weight(N)
    B0 = solve_B(d, K2, wt)
    v = np.real(np.fft.ifftn(-hB(B0) * np.fft.fftn(d) / np.maximum(K2, 1e-12) * (K2 > 0)))
    u = d.copy()

    def S_of(B):                                                     # S = Sum u (S_xi - S_B) v: the chassis's B-dependence (xi -> 0)
        return float(np.sum(u * (v - smooth(v, K2, B))))
    rng = np.random.default_rng(5)
    cells = [tuple(rng.integers(0, 8, 3)) for _ in range(6)]                     # the same base cells on every tiled leaf
    eps_ = 1e-4
    dS_fd, dB_fd = [], []
    for cidx in cells:
        dp = d.copy(); dp[cidx] += eps_; dm = d.copy(); dm[cidx] -= eps_
        Bp, Bm = solve_B(dp, K2, wt), solve_B(dm, K2, wt)
        dB_fd.append((Bp - Bm) / (2 * eps_))
        dS_fd.append((S_of(Bp) - S_of(Bm)) / (2 * eps_))
    # the derived formula: dS/d delta(x) = (dS/dB) (dB/d delta(x)),  dB/d delta(x) = -(2/Sw) S_B(w S_B d)(x) / dF/dB
    dSdB = (S_of(B0 * (1 + 1e-6)) - S_of(B0 * (1 - 1e-6))) / (2e-6 * B0)
    sBd = smooth(d, K2, B0)
    dFdB = float(np.sum(wt * 2 * sBd * np.real(np.fft.ifftn(-K2 * np.fft.fftn(sBd)))) / np.sum(wt))
    grad_an = -dSdB * (2 / np.sum(wt)) * smooth(wt * sBd, K2, B0) / dFdB
    an = np.array([grad_an[cidx] for cidx in cells])
    # momentum: the net mean-field force Sum delta grad(K delta) with K the mean-field kernel (S_B w S_B)
    force_field = np.real(np.fft.ifftn(1j * (np.fft.fftfreq(N) * 2 * np.pi)[:, None, None] * np.fft.fftn(smooth(wt * sBd, K2, B0))))
    net = float(np.sum(d * force_field)); scale = float(np.sum(np.abs(d * force_field)))
    n1[N] = dict(B=B0, dB_rms=float(np.sqrt(np.mean(np.square(dB_fd)))), dS_rms=float(np.sqrt(np.mean(np.square(dS_fd)))),
                 an_dev=float(np.max(np.abs(np.array(dS_fd) / an - 1))), net_rel=abs(net) / scale, dSdB=dSdB)
    P(f"    N = {N:2d}: B = {B0:.4f}; rms dB/d delta_j = {n1[N]['dB_rms']:.3e} (x N^3 = {n1[N]['dB_rms'] * N ** 3:.3f}); rms dS/d delta_j = "
      f"{n1[N]['dS_rms']:.4f} (dS/dB = {dSdB:.1f}); FD vs derived 2 E_B S_B^2 delta: max dev {n1[N]['an_dev']:.1e}; net mean-field force / "
      f"sum |.| = {n1[N]['net_rel']:.1e}")
dBN3 = [n1[N]["dB_rms"] * N ** 3 for N in (8, 16, 32)]; dS = [n1[N]["dS_rms"] for N in (8, 16, 32)]
n1_ok = (max(dBN3) / min(dBN3) < 1.2 ** 2 and max(dS) / min(dS) < 1.2 ** 2 and max(n1[N]["an_dev"] for N in n1) < 0.05)
check("N1 [HS1, pre-declared] THE LOCAL TERM EXISTS: on periodic leaves of fixed cell size the derivative of B[delta] scales as 1/V "
      "(N^3 |dB/d delta| is N-independent: FP13 A1's check reproduced), but the ACTION's gradient per cell through B is N-independent "
      "and equals the derived mean-field form (dS/dB)(dB/d delta) = 2 E_B (S_B^2 delta)(x): FP13 A1's 'adds no local term to the field "
      "equations' does not hold for the action",
      f"N^3 rms dB/d delta: {[round(v, 3) for v in dBN3]}; rms dS/d delta: {[round(v, 4) for v in dS]}; FD vs derived max dev "
      f"{max(n1[N]['an_dev'] for N in n1):.1e}", n1_ok,
      "dS/dB is an integral over the whole leaf (O(V)); the O(1/V) derivative of the leaf average multiplies it: an O(1) local force with "
      "a leaf-averaged coefficient -- a mean field")
n2_ok = max(n1[N]["net_rel"] for N in n1) < 1e-10
check("N2 [HS2, pre-declared] MOMENTUM IS CONSERVED WITH THE MEAN-FIELD TERM: the net force Sum delta grad(S_B^2 delta) vanishes on every "
      "leaf (the leaf average is translation-covariant; the Noether identity of the full diffeomorphism-invariant action then gives "
      "matter conservation on shell, the global terms included)", f"max |net|/Sum|.| = {max(n1[N]['net_rel'] for N in n1):.1e}", n2_ok,
      "MUTATE's position-weighted window breaks translation covariance and must fail this")
OUT["numbers"]["N1"] = {str(k_): v for k_, v in n1.items()}
P(f"    {el()}")

# ============================================================================================ the state's mean-field coefficients
banner("N3 N4  THE MEAN-FIELD COEFFICIENTS ON FP13's HEADLINE STATE: R_B(k, z) and kappa(z), and what they do")
D2NL = STATE["NL"]; D2LIN = STATE["lin"]


def D2_at(a, reading="NL"):
    x = math.log(a); j = min(max(np.searchsorted(LNA, x) - 1, 0), len(LNA) - 2); f_ = (x - LNA[j]) / (LNA[j + 1] - LNA[j])
    S = STATE[reading]
    return (1 - f_) * S[j] + f_ * S[j + 1]


def chord_modes(D, a, a0v, Lp, yth, KHg, mode):
    hk = 1.0 - np.exp(-0.5 * (KHg * h_ * Lp / a) ** 2)
    gb = gfield(D, a, KHg) * hk
    m341 = KHg <= 20.0 * 1.0001; kk341 = KHg[m341]; norm341 = np.trapz(1 / kk341, kk341)
    y = np.full(len(KHg), math.sqrt(np.trapz(gb[m341] ** 2 / kk341, kk341) / norm341) / a0v) if mode == "rms" else gb / a0v
    CQ = np.maximum((nu_p2(y) - 1.0) * cutfac(y, yth, YIELD), 0.0)
    return CQ, hk, y


def RB_of(a, CQ_k, KHg, Lp):
    """R_B(k) on the growth grid: [Int Delta^2 h C^Q e^(-Bk^2) / Int k^2 Delta^2 e^(-2Bk^2)] k^2 e^(-2Bk^2), comoving 1/Mpc."""
    D2 = D2_at(a)
    Lc = Lp / a; kc = KKF * h_; B = 0.5 * Lc ** 2
    hk = 1.0 - np.exp(-B * kc ** 2)
    CQf = np.exp(np.interp(np.log(KKF), np.log(KHg), np.log(np.maximum(CQ_k, 1e-300))))
    CQf = np.where(KKF > KHg[-1], CQ_k[-1], CQf)
    num = float(np.trapz(D2 * hk * CQf * np.exp(-B * kc ** 2), LKF))
    den = float(np.trapz(kc ** 2 * D2 * np.exp(-2 * B * kc ** 2), LKF))
    kg = KHg * h_
    return (num / den) * kg ** 2 * np.exp(-2 * B * kg ** 2), num / den


def maxwell_x_mean(y_rms, yth, nu=4000):
    """<x> for a Gaussian (Maxwell |g|) band-passed field of rms y_rms under the yield law x = x_P2(y - y_th)."""
    u = np.linspace(0, 6, nu)
    p = math.sqrt(2 / math.pi) * 3 ** 1.5 * u ** 2 * np.exp(-1.5 * u ** 2)
    return float(np.trapz(p * x_P2(np.maximum(y_rms * u - yth, 0.0)), u))


# the halo reading: Press-Schechter halos (Gaussian-filter sigma(M), M = (2 pi)^1.5 rho_m R^3), baryons 0.3 f_b M, FP9's yield bubbles
FB = 0.02237 / (0.02237 + 0.1200)
gfr = M6["gfrac_smooth"]


def halo_x_mean(a, a0v, Lp, yth):
    z = 1 / a - 1
    D2 = D2_at(a, "lin")
    rho_m = Om * rho_crit0 / a ** 3                                              # physical
    lnM = np.linspace(math.log(1e8), math.log(1e15), 120)
    Rh = ((np.exp(lnM) * MSUN) / ((2 * math.pi) ** 1.5 * Om * rho_crit0)) ** (1 / 3) / Mpc * h_   # comoving Mpc/h
    sg = np.array([math.sqrt(sig2(R, D2)) for R in Rh])
    nu_ = DELTA_C / sg
    dlnsig = np.gradient(np.log(sg), lnM)
    dn = (Om * rho_crit0 / (np.exp(lnM) * MSUN)) * math.sqrt(2 / math.pi) * nu_ * np.exp(-nu_ ** 2 / 2) * np.abs(dlnsig) * Mpc ** 3   # per comoving Mpc^3
    tot = 0.0
    Lm = Lp * MPCm
    for i, lm in enumerate(lnM):
        Mb = 0.3 * FB * math.exp(lm) * MSUN
        r = np.geomspace(1e-4, 10.0, 600) * MPCm
        ybp = G6 * Mb * (1 - gfr(r / Lm)) / (a0v * r ** 2)
        x = x_P2(np.maximum(ybp - yth, 0.0))
        vol_x = float(np.trapz(4 * math.pi * r ** 2 * x, r)) / MPCm ** 3 * (1 + z) ** 3             # comoving Mpc^3
        tot += dn[i] * vol_x * (lnM[1] - lnM[0])
    return tot


ZS_SCAN = (0.0, 0.25, 0.5, 0.635, 0.8, 1.0, 1.5, 2.0, 2.5, 3.0)
coef = {}
for f in FOOTS:
    a0v = A0[f]
    res = growth_aq(model_of(Lh, yh[f]), a0v, mode="permode", KHg=KHF, Dig=DIF, zs_out=tuple(z for z in ZS_SCAN if z > 0))
    for z in ZS_SCAN:
        a = 1 / (1 + z); Lp = Lh(a); yt = yh[f](a)
        CQ, hk, yk = chord_modes(res[round(z, 6)], a, a0v, Lp, yt, KHF, "permode")
        RB, ratio = RB_of(a, CQ, KHF, Lp)
        CQr, _, _ = chord_modes(res[round(z, 6)], a, a0v, Lp, yt, KHF, "rms")
        RBr, _ = RB_of(a, CQr, KHF, Lp)
        y_rms = rms_h[int(np.argmin(np.abs(AGR - a)))] / a0v
        ramp = max(0.0, two_q(a))
        kG = ramp * maxwell_x_mean(y_rms, yt) / y_rms if ramp > 0 else 0.0
        kH = ramp * halo_x_mean(a, a0v, Lp, yt) / y_rms if ramp > 0 else 0.0
        jmax = int(np.argmax(RB))
        kge1 = KHF[RB >= 1.0]
        coef[(f, z)] = dict(RB_max=float(RB[jmax]), RB_max_rms=float(np.max(RBr)), k_RBmax=float(KHF[jmax]), ratio=ratio, y_rms=y_rms, kappa_G=kG, kappa_H=kH,
                            k_RBge1=(float(kge1.min()), float(kge1.max())) if len(kge1) else None,
                            RB_1Mpc=float(np.interp(1 / (1.0 * h_) , KHF, RB)), RB_03Mpc=float(np.interp(1 / (0.3 * h_), KHF, RB)))
for (f, z), v in coef.items():
    P(f"    {f:9s} z = {z:5.3f}: max_k R_B = {v['RB_max']:.3f} at k = {v['k_RBmax']:.2f} h/Mpc (rms chord: {v['RB_max_rms']:.3f}; R_B at 1/1 Mpc {v['RB_1Mpc']:.3f}, at 1/0.3 Mpc "
      f"{v['RB_03Mpc']:.2e}); R_B >= 1 on k = {('%.2f-%.2f h/Mpc' % v['k_RBge1']) if v['k_RBge1'] else 'none'}; y_rms = {v['y_rms']:.2e}; "
      f"kappa: Gaussian reading {v['kappa_G']:.3f}, halo reading {v['kappa_H']:.2e}")
OUT["numbers"]["coef"] = {f"{k_[0]}/{k_[1]}": v for k_, v in coef.items()}
P(f"    {el()}")


# ---- the growth yardstick with the mean-field factors: delta'' + (2 + dlnH) delta' = 1.5 Om(a) [1/(1 + kappa h^2 - R_B) + C^Q h^2 w] delta
def growth_mf(Lf, yf, a0v, mode, use_B=True, kap=None, KHg=None, Dig=None, zs_out=(), rtol=1e-6, lam=0.0):
    KHg = KH if KHg is None else KHg; Dig = DI if Dig is None else Dig
    nk = len(KHg)

    def rhs(N_, Yv):
        a = math.exp(N_); D = Yv[:nk]; Dp = Yv[nk:]
        Lp = Lf(a); yt = yf(a)
        CQ, hk, yk = chord_modes(D, a, a0v, Lp, yt, KHg, mode)
        lam_phi = lam + (2 + 3 * C2W) * hk ** 2 / C2W
        cs = c_ / np.sqrt(np.maximum(CQ, 1e-300) * np.maximum(lam_phi, 1e-300))
        kk = (1.0 * h_ / (a * Mpc)) if mode == "rms" else KHg * h_ / (a * Mpc)
        wt = 1.0 / (1.0 + (H0 * Ez(a) / (cs * kk)) ** 2)
        RB = RB_of(a, CQ, KHg, Lp)[0] if use_B else 0.0
        kp = kap(a) if kap is not None else 0.0
        newt = 1.0 / np.maximum(1.0 + kp * hk ** 2 - RB, 1e-3)
        return np.concatenate([Dp, 1.5 * (Om / a ** 3 / Ez(a) ** 2) * (newt + CQ * hk ** 2 * wt) * D - (2 + dlnH(a)) * Dp])
    Nout = sorted({math.log(1 / (1 + z)) for z in zs_out if z > 0}) + [0.0]
    sol = solve_ivp(rhs, (math.log(A_I), 0.0), np.concatenate([Dig, Dig]), method="LSODA", rtol=rtol, atol=1e-24, t_eval=Nout)
    return {round(1 / math.exp(N_) - 1, 6): sol.y[:nk, i] for i, N_ in enumerate(sol.t)}


def kappa_fun(f, reading):
    zz = np.array([0.635, 0.7, 0.8, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0, 6.0])
    vals = []
    for z in zz:
        a = 1 / (1 + z); Lp = Lh(a); yt = yh[f](a); y_rms = rms_h[int(np.argmin(np.abs(AGR - a)))] / A0[f]; ramp = max(0.0, two_q(a))
        if ramp <= 0:
            vals.append(0.0); continue
        xm = maxwell_x_mean(y_rms, yt) if reading == "G" else halo_x_mean(a, A0[f], Lp, yt)
        vals.append(ramp * xm / y_rms)
    la = np.log(1 / (1 + zz))
    return lambda a: float(np.interp(math.log(a), la[::-1], np.array(vals)[::-1])) if 1 / a - 1 > Z_Q0 else 0.0


n3 = {}
for f in FOOTS:
    kG, kH = kappa_fun(f, "G"), kappa_fun(f, "H")
    for m in MODES:
        s0 = sigma8_of(growth_mf(Lh, yh[f], A0[f], m, use_B=False)[0.0]) / S8_LCDM
        sB = sigma8_of(growth_mf(Lh, yh[f], A0[f], m, use_B=True)[0.0]) / S8_LCDM
        sBG = sigma8_of(growth_mf(Lh, yh[f], A0[f], m, use_B=True, kap=kG)[0.0]) / S8_LCDM
        sBH = sigma8_of(growth_mf(Lh, yh[f], A0[f], m, use_B=True, kap=kH)[0.0]) / S8_LCDM
        n3[(f, m)] = dict(fp13=H["s8"][(f, m)], rebuilt=s0, B=sB, B_Ygauss=sBG, B_Yhalo=sBH)
    for lab, kp in (("B", None), ("B+Y gauss", kG), ("B+Y halo", kH)):
        res_f = growth_mf(Lh, yh[f], A0[f], "permode", use_B=True, kap=kp, KHg=KHF, Dig=DIF, zs_out=(2.0, 3.0))
        n3[(f, "forest", lab)] = max(forest_proxy(res_f, kF=kF)[0] for kF in (10.0, 15.0, 20.0))
for k_, v in n3.items():
    P(f"    {k_}: {v}")
# ---- N3b [ADDED AFTER the first (MUTATE) run found max R_B ~ 8; written before its own first run].  An independent check of the
#      B-term with no WKB or mean-field algebra: on a 32^3 periodic leaf (cell 1, 4 pi G = rho_bar = 1) the reduced action of the
#      linearised H_S sector is exactly S_red[delta] = Sum_k (1/2)(1 + C^Q h(k; B[delta])^2)|delta_k|^2/k^2 (Newton + the chord MOND
#      response through the band-pass, phi and psi on shell), with B[delta] from <(S_B delta)^2> = delta_c^2.  Its exact second
#      derivative along plane waves (q = 2 pi j/32, j = 1..6) is split into the fixed-B part and the B-part; pre-declared: the
#      B-part is positive and its ratio to the Newtonian part equals the derived R_B(q) within 10%.
NL3 = 32
rngL = np.random.default_rng(29)
kxl = np.fft.fftfreq(NL3) * 2 * np.pi
KXl, KYl, KZl = np.meshgrid(kxl, kxl, kxl, indexing="ij"); K2l = KXl ** 2 + KYl ** 2 + KZl ** 2
Pl = np.where(K2l > 0, np.exp(-K2l / (2 * 0.9 ** 2)) / np.maximum(K2l, 1e-12) ** 0.75, 0.0)
dbar = np.real(np.fft.ifftn(np.fft.fftn(rngL.standard_normal((NL3, NL3, NL3))) * np.sqrt(Pl)))
dbar *= DELTA_C / np.sqrt(np.mean(np.real(np.fft.ifftn(np.fft.fftn(dbar) * np.exp(-3.0 * K2l))) ** 2))   # B0 = 1.5 cells^2 (sigma at 2B = 3)
CQL = 10.0


def B_of_l(d):
    return brentq(lambda B: float(np.mean(np.real(np.fft.ifftn(np.fft.fftn(d) * np.exp(-B * K2l))) ** 2)) - DELTA_C ** 2, 1e-6, 60.0,
                  xtol=1e-15, rtol=1e-15)


def S_red(d, B=None):
    B = B_of_l(d) if B is None else B
    dk = np.fft.fftn(d); h = 1 - np.exp(-B * K2l)
    return float(np.sum(np.where(K2l > 0, 0.5 * (1 + CQL * h ** 2) * np.abs(dk) ** 2 / np.maximum(K2l, 1e-12), 0.0)) / NL3 ** 3), B


B0l = B_of_l(dbar)
dkb = np.fft.fftn(dbar); hb = 1 - np.exp(-B0l * K2l)
ratio_l = float(np.sum(hb * CQL * np.exp(-B0l * K2l) * np.abs(dkb) ** 2) / np.sum(K2l * np.exp(-2 * B0l * K2l) * np.abs(dkb) ** 2))
xg_ = np.arange(NL3)[:, None, None] * np.ones((1, NL3, NL3))
n3b = {}
for j in range(1, 7):
    qv = 2 * np.pi * j / NL3
    eta = np.cos(qv * xg_)
    e_ = 1e-3
    Sp, _ = S_red(dbar + e_ * eta); Sm, _ = S_red(dbar - e_ * eta); S0, _ = S_red(dbar)
    Sp_f, _ = S_red(dbar + e_ * eta, B0l); Sm_f, _ = S_red(dbar - e_ * eta, B0l)
    tot = (Sp - 2 * S0 + Sm) / e_ ** 2; fixed = (Sp_f - 2 * S0 + Sm_f) / e_ ** 2
    ek = np.fft.fftn(eta)
    newton = float(np.sum(np.where(K2l > 0, np.abs(ek) ** 2 / np.maximum(K2l, 1e-12), 0.0)) / NL3 ** 3)
    pred = ratio_l * qv ** 2 * math.exp(-2 * B0l * qv ** 2)
    n3b[j] = dict(q=qv, B_part_over_newton=(tot - fixed) / newton, R_B_formula=pred)
    P(f"    lattice q = 2 pi {j}/32 = {qv:.3f} (q L = {qv * math.sqrt(2 * B0l):.2f}): B-part/Newton = {(tot - fixed) / newton:+.4f}, derived R_B = {pred:.4f}")
n3b_dev = max(abs(v["B_part_over_newton"] / v["R_B_formula"] - 1) for v in n3b.values())
check("N3b [added after the first run; pre-declared before its own] THE B-TERM, INDEPENDENTLY: the exact second derivative of the "
      "linearised H_S reduced action on a 32^3 leaf (B re-solved from the variance condition at every step) carries a B-part that "
      "is positive (adds to gravity's drive) and equals the derived R_B(q) x the Newtonian part within 10%, q = 2 pi j/32, j = 1..6",
      f"B0 = {B0l:.3f} cells^2; max relative deviation {n3b_dev:.2e}; B-part/Newton at q ~ 1/L: {max(v['B_part_over_newton'] for v in n3b.values()):.3f}",
      n3b_dev < 0.10 and all(v["B_part_over_newton"] > 0 for v in n3b.values()),
      "the mean-field term is the action's own second variation: adding variance raises B, which lets more of the web's MOND "
      "potential into chi, which binds all matter deeper -- a destabilising term whose size scales with the web's MOND energy")
OUT["numbers"]["N3b"] = {str(k_): v for k_, v in n3b.items()}
RBmax_all = max(v["RB_max"] for v in coef.values())
s8B = [v["B"] for k_, v in n3.items() if isinstance(v, dict)]
reb = max(abs(v["rebuilt"] / v["fp13"] - 1) for k_, v in n3.items() if isinstance(v, dict))
n3_ok = RBmax_all < 1.0 and all(SIG8_BAND[0] <= s <= SIG8_BAND[1] for s in s8B)
check("N3 [HS3, pre-declared] THE B-TERM ON FP13's HEADLINE STATE: max_k R_B < 1 at every scanned epoch (the psi-constraint's symbol "
      "k^2 (1 - R_B) stays regular) and sigma_8 with the B-term in the growth yardstick stays in [0.922, 1.05], both footings, both modes",
      f"max R_B over z = 0..3 and both footings {RBmax_all:.3f}; sigma_8 with the B-term {min(s8B):.4f}-{max(s8B):.4f} (FP13: "
      f"{min(H['s8'].values()):.4f}-{max(H['s8'].values()):.4f}; this lane's rebuild of FP13's yardstick without the terms: max dev {reb:.1e}); "
      f"forest with the B-term {max(n3[(f, 'forest', 'B')] for f in FOOTS):.3g}", n3_ok,
      "R_B multiplies the Newtonian response by 1/(1 - R_B) at k ~ 1/L: a real, derived part of H_S's physics that FP13's yardstick "
      "(L(a) as a given function) leaves out; where R_B >= 1 the psi-constraint's symbol k^2 (1 - R_B) vanishes or flips (a singular "
      "constraint), and the sigma_8 numbers of the floored yardstick are then not meaningful")
OUT["numbers"]["N3"] = {str(k_): v for k_, v in n3.items()}


def flag_shift(kap, yth, y=0.1):
    x = float(x_P2(max(y - yth, 0.0)))
    return math.log10((y / (1 + kap) + x) / (y + x))


kG25 = {f: kappa_fun(f, "G")(1 / 3.5) for f in FOOTS}; kH25 = {f: kappa_fun(f, "H")(1 / 3.5) for f in FOOTS}
flG = {f: flag_shift(kG25[f], yh[f](1 / 3.5)) for f in FOOTS}; flH = {f: flag_shift(kH25[f], yh[f](1 / 3.5)) for f in FOOTS}
kGz = [v["kappa_G"] for (f, z), v in coef.items() if 1.0 <= z <= 3.0]; kHz = [v["kappa_H"] for (f, z), v in coef.items() if 1.0 <= z <= 3.0]
s8Y = {k_: (v["B_Ygauss"], v["B_Yhalo"]) for k_, v in n3.items() if isinstance(v, dict)}
P(f"    kappa at z = 2.5: Gaussian {kG25}, halo {kH25}; flagship shift from the screened Newtonian part (0.1 a0, r_F << L): Gaussian "
  f"{ {f: round(v, 4) for f, v in flG.items()} } dex, halo { {f: round(v, 5) for f, v in flH.items()} } dex; sigma_8 with B + Y "
  f"(Gaussian / halo): { {str(k_): (round(a_, 4), round(b_, 4)) for k_, (a_, b_) in s8Y.items()} }")
n4_ok = min(kGz) > 1.0 and min(abs(v) for v in flG.values()) > FLAG_TOL and max(kHz) < 0.1
check("N4 [HS4, pre-declared] THE Y-TERM IS O(1) IN FP13's OWN GAUSSIAN READING OF THE WEB: kappa(z = 1..3) > 1 and the 1e11 flagship "
      "moves by > 0.05 dex once its Newtonian part is screened; in a halo-dominated reading kappa < 0.1",
      f"kappa_Gauss(z = 1..3) in [{min(kGz):.3f}, {max(kGz):.3f}]; flagship shift (Gauss) {min(flG.values()):+.4f}..{max(flG.values()):+.4f} dex; "
      f"kappa_halo(z = 1..3) in [{min(kHz):.2e}, {max(kHz):.2e}]; forest with B+Y (Gauss/halo) "
      f"{max(n3[(f, 'forest', 'B+Y gauss')] for f in FOOTS):.3g}/{max(n3[(f, 'forest', 'B+Y halo')] for f in FOOTS):.3g}", n4_ok,
      "which reading holds is a property of H_S's own nonlinear web (the one-point distribution of |g_bp| at z > 0.635) -- a PM "
      "run's job, and only if the run carries the y-term")
OUT["numbers"]["N4"] = dict(kappa_G25=kG25, kappa_H25=kH25, flag_G=flG, flag_H=flH)
P(f"    {el()}")

# ---- R1 item 2: the readout, the constraint's symbol, DE12's UV mechanism
bf = []
for (f, z), v in coef.items():
    a = 1 / (1 + z); Lp = Lh(a); Lc = Lp / a
    k1 = 1.0 / (1e-3 / a)                                                    # 1/kpc physical -> comoving 1/Mpc
    supp = math.exp(-Lc ** 2 * k1 ** 2)                                      # e^(-2 B k^2)
    rho_b = FB * Om * rho_crit0 / a ** 3
    # k^0-type coefficient per |delta rho|^2 of the B-term: 2 E_B e^(-2Bk^2)/rho_bar^2, E_B = 4 pi G rho_bar^2 ratio/2
    EBrat = 4 * math.pi * G * (Om * rho_crit0 / a ** 3) ** 2 * v["ratio"] / 2 * (Mpc ** 2 * a ** 2)   # ratio in comoving Mpc^2 -> physical m^2
    rel = 2 * EBrat * supp / (Om * rho_crit0 / a ** 3) ** 2 / ((1.17e5) ** 2 / rho_b)
    bf.append(rel)
P(f"    the leaf-averaged read's k^0-type coefficient at k = 1/kpc relative to 1e6 K gas pressure: max {max(bf):.1e} (e^(-2Bk^2) with L >= 100 kpc)")
check("R1 (item 2) THE MATTER READOUT: D_i a^i contains no time derivative (a_i = D_i ln N; the lapse stays non-dynamical: no "
      "Ostrogradsky mode, no new velocity); the only structural change is the psi-constraint's symbol k^2 (1 + kappa h^2 - R_B) (N3); the "
      "read's k^0-type second variation is smoothed by S_B, so DE12's UV mechanism (Gamma = c_gate k) is absent: at k = 1/kpc it is "
      "negligible against gas pressure", f"max relative size at 1/kpc {max(bf):.1e}", max(bf) < 1e-6, load_bearing=False)

# ============================================================================================ Q1 the ramp
banner("Q1  FRW GROWTH ACROSS THE q = 0 RAMP: smoothed ramp (eps -> 0), single crossings, continuity of the chord G_eff")


def yth_smooth(eps):
    if eps == 0:
        return yth_state(LH_tab, "NL", "ramp", 1.0)[0]
    sw = lambda a: eps * math.log1p(math.exp(min(two_q(a) / eps, 700.0))) if two_q(a) / eps < 700 else two_q(a)
    return yth_state(LH_tab, "NL", "ramp", 1.0, onset=sw)[0]


q1 = {}
for eps in (0.05, 0.01, 0.002, 0.0):
    ys = yth_smooth(eps)
    q1[eps] = {m: float(NS["s8_aq"](model_of(Lh, ys["canonical"]), "canonical", m)) for m in MODES}
d_eps = {e_: max(abs(q1[e_][m] - q1[0.0][m]) for m in MODES) for e_ in (0.05, 0.01, 0.002)}
mono = d_eps[0.05] >= d_eps[0.01] - 1e-9 >= -1 and d_eps[0.01] >= d_eps[0.002] - 1e-9
P("    sigma_8 (canonical) with the ramp smoothed: " + "; ".join(f"eps {e_:g}: rms {v['rms']:.6f}, per-mode {v['permode']:.6f}" for e_, v in q1.items()))
# per-mode crossings (z = 3 -> 0.5) and continuity of the chord through z = 0.635 by REFINEMENT: the largest epoch-to-epoch step
# within |z - z_q0| < 0.02 on grids of spacing 1e-3 and 1e-4 -- a continuous (sqrt-onset) switch shrinks it ~ sqrt(10); a jump does not
ZQ = np.linspace(3.0, 0.5, 400)
res_q = growth_aq(model_of(Lh, yh["canonical"]), A0["canonical"], mode="permode", zs_out=tuple(ZQ))
zq = np.array(sorted(res_q.keys(), reverse=True))
crossings = []
for z in zq:
    a = 1 / (1 + z)
    _, hk, yk = chord_modes(res_q[z], a, A0["canonical"], Lh(a), yh["canonical"](a), KH, "permode")
    crossings.append(yk > yh["canonical"](a))
ncross = np.sum(np.abs(np.diff(np.array(crossings).astype(int), axis=0)), axis=0)
_cr = np.array(crossings)
z_cross = [float(zq[np.argmax(_cr[:, j_])]) for j_ in range(_cr.shape[1]) if _cr[:, j_].any() and not _cr[0, j_]]
ystep = yth_state(LH_tab, "NL", "step", 1.0)[0]
_yq = {dzz: float(yh["canonical"](1 / (1 + Z_Q0 + dzz))) for dzz in (0.02, 0.0, -0.005, -0.01, -0.011)}
z_cross = z_cross or [float("nan")]
P(f"    the sigma_8 modes' first above-yield epochs (canonical, grid z = 3 -> 0.5): z = {min(z_cross):.3f} - {max(z_cross):.3f} "
  f"({len(z_cross)} of {_cr.shape[1]} modes cross; none within 0.02 of z_q0 = {Z_Q0:.4f}: {all(abs(zc - Z_Q0) > 0.02 for zc in z_cross)})")
P("    FP13's tabulated (interpolated) y_th near z_q0: " + ", ".join(f"z - z_q0 = {k_:+.3f}: {v:.2e}" for k_, v in _yq.items()))
steps = {}
for dz in (1e-3, 1e-4):
    zfine = np.arange(Z_Q0 + 0.02, Z_Q0 - 0.02, -dz)
    rf = growth_aq(model_of(Lh, yh["canonical"]), A0["canonical"], mode="permode", zs_out=tuple(zfine))
    zf = np.array(sorted(rf.keys(), reverse=True))
    zf = zf[(zf <= Z_Q0 + 0.02 + 1e-9) & (zf >= Z_Q0 - 0.02 - 1e-9)]      # growth_aq's keys also carry an appended z = 0: drop it
    for lab, yfun in (("ramp", yh["canonical"]), ("step", ystep["canonical"])):
        Ge = []
        for z in zf:
            a = 1 / (1 + z)
            CQv, hk, _ = chord_modes(rf[z], a, A0["canonical"], Lh(a), yfun(a), KH, "permode")
            Ge.append(CQv * hk ** 2)
        steps[(lab, dz)] = float(np.max(np.abs(np.diff(np.array(Ge), axis=0))))
shrink_ramp = steps[("ramp", 1e-3)] / max(steps[("ramp", 1e-4)], 1e-300)
shrink_step = steps[("step", 1e-3)] / max(steps[("step", 1e-4)], 1e-300)
P(f"    per-mode crossings of the yield (canonical, 48 sigma_8 modes, z = 3 -> 0.5): max {int(ncross.max())}; the chord G_eff's largest "
  f"step near z = {Z_Q0:.3f}: ramp {steps[('ramp', 1e-3)]:.3e} (dz = 1e-3) -> {steps[('ramp', 1e-4)]:.3e} (dz = 1e-4), shrink x{shrink_ramp:.2f}; "
  f"step variant {steps[('step', 1e-3)]:.3e} -> {steps[('step', 1e-4)]:.3e}, shrink x{shrink_step:.2f}")
q1_ok = d_eps[0.002] < 1e-4 and mono and int(ncross.max()) <= 1 and shrink_ramp >= 2.0
check("Q1 [HS5, pre-declared] FRW GROWTH ACROSS THE q = 0 RAMP IS WELL POSED: the smoothed ramp's sigma_8 converges monotonically to "
      "FP13's (within 1e-4 at eps = 0.002), every sigma_8 mode crosses the yield at most once, and the chord G_eff is continuous through "
      "z = 0.635 with the ramp (its largest epoch step shrinks under 10x refinement; a jump would not); the step variant's jump is reported",
      f"|d sigma_8| at eps 0.05/0.01/0.002: {d_eps[0.05]:.1e}/{d_eps[0.01]:.1e}/{d_eps[0.002]:.1e}; max crossings {int(ncross.max())}; "
      f"ramp step shrinks x{shrink_ramp:.2f}; step-variant step shrinks x{shrink_step:.2f} ({steps[('step', 1e-3)]:.2f} -> "
      f"{steps[('step', 1e-4)]:.2f})", q1_ok,
      (f"all {len(z_cross)} crossing sigma_8 modes are above the yield before z_q0 + 0.02 (printed), so through z = 0.635 their chord "
       "changes smoothly (the ramp's step scales with dz); " if all(zc > Z_Q0 + 0.02 for zc in z_cross) else
       "some sigma_8 modes cross the ramp's yield within 0.02 of z_q0 (printed); ")
      + "FP13's y_th(a) is a linearly interpolated table (printed: its zero sits below z_q0), so the step variant is also a linear "
      "ramp across one table cell; its step shrinking by ~sqrt(10) marks sqrt onsets, not a jump.  Development record "
      "(XR18_README.md): a one-grid 5x test was replaced by this refinement test before the recorded runs, and the first recorded "
      "main run's step included growth_aq's appended z = 0 epoch (fixed; MUTATE and main re-run)")
step_ramp, step_step = steps[("ramp", 1e-4)], steps[("step", 1e-4)]
OUT["numbers"]["Q1"] = dict(s8=q1, d_eps=d_eps, ncross=int(ncross.max()), steps={f"{k_[0]}/{k_[1]}": v for k_, v in steps.items()},
                            z_cross_range=[min(z_cross), max(z_cross)], n_cross=len(z_cross), yth_table_near_zq0={str(k_): v for k_, v in _yq.items()})
P(f"    {el()}")

# ============================================================================================ Q2 lambda at the switch-off
banner("Q2  lambda AT THE SWITCH-OFF: how fast phi un-freezes when the yield vanishes (z = 0.635)")
aq = 1 / (1 + Z_Q0)
Dq = growth_aq(model_of(Lh, yh["canonical"]), A0["canonical"], mode="permode", zs_out=(Z_Q0,))[round(Z_Q0, 6)]
_, hq, yq = chord_modes(Dq, aq, A0["canonical"], Lh(aq), 0.0, KH, "permode")
xq = x_P2(yq); CLphi = 2 * xq * (1 - xq) / (1 - 2 * xq) ** 2
sub = hq >= 0.4
q2 = {}
for c2lab, c2v in (("c2=7.29e-3", 7.29e-3), ("c2->oo", None)):
    for lam in (0.0, 1.0, 100.0, 1e4):
        lam_eff = lam + (3.0 * hq ** 2 if c2v is None else (2 + 3 * c2v) * hq ** 2 / c2v)
        om = c_ * (KH * h_ / (aq * Mpc)) * np.sqrt(CLphi / lam_eff) / (H0 * Ez(aq))
        q2[(c2lab, lam)] = float(np.min(om[sub]))
for k_, v in q2.items():
    P(f"    {k_}: min over sub-L sigma_8 modes (h >= 0.4) of omega_r/H = {v:.3g}")
q2_ok = k2_ok and all(v > 10 for (c2l, lam), v in q2.items() if lam <= 100)
check("Q2 [HS6, pre-declared] lambda AT THE SWITCH-OFF: on exact FRW with the band-pass closed phi has no equation at lambda = 0 (K2); with "
      "structure phi un-freezes at omega_r = c k sqrt(C_L^phi/lambda_eff) > 10 H for every sub-L sigma_8 mode at lambda <= 100, for "
      "c_2 = 7.29e-3 and c_2 -> oo: the quasi-static yardstick holds through z = 0.635",
      "; ".join(f"{k_[0]}, lambda {k_[1]:g}: {v:.3g}" for k_, v in q2.items()), q2_ok,
      "lambda > 0 is what keeps phi determined where the band-pass closes and the yield vanishes; its value only sets the un-freezing "
      "rate, which stays fast unless lambda >~ 1e4")
OUT["numbers"]["Q2"] = {f"{k_[0]}/{k_[1]}": v for k_, v in q2.items()}

# ============================================================================================ Y1 the shared yield structure
banner("Y1  THE SHARED YIELD STRUCTURE AT H_S's z >= 1 YIELD SURFACES: criterion B's roots and the surface exponents")
Ud = sp.Symbol("U")
polyU = sp.Poly(sp.numer(sp.together(det7.subs(wq_, sp.sqrt(Ud) * kq_))), Ud)
cU = [sp.simplify(cc / kq_ ** 10) for cc in polyU.all_coeffs()]
coef_fun = sp.lambdify((alm, c2m, Cph, lmm, sgm), cU, "numpy")


def roots_ok(C, lam, hv, ac, c2):
    a2, a1, a0_ = [np.broadcast_to(np.asarray(v_, float), np.shape(C)).astype(float) for v_ in coef_fun(ac, c2, C, lam, hv)]
    if lam == 0:
        U = -a0_ / a1; return np.isfinite(U) & (U >= 0)
    disc = a1 * a1 - 4 * a2 * a0_; sq = np.sqrt(np.maximum(disc, 0))
    Up, Um = (-a1 + sq) / (2 * a2), (-a1 - sq) / (2 * a2)
    return (disc >= -1e-12 * a1 * a1) & (Up >= 0) & (Um >= 0)


viol = 0; ncell = 0; slopes = []
TH = np.radians([0, 30, 60, 90])
for z in (1.0, 2.5, 4.0):
    for Mb in (1e10, 1e11, 1e12):
        for f in FOOTS:
            a = 1 / (1 + z); a0v = A0[f]; Lm = Lh(a) * MPCm; yt = yh[f](a)
            ybp_f = lambda r: G6 * Mb * MSUN / (a0v * r ** 2) * (1 - gfr(r / Lm))
            rr = np.geomspace(1e-3, 50, 30000) * MPCm; yy = ybp_f(rr)
            if not ((yy > yt).any() and (yy <= yt).any()):
                continue
            j = np.where(yy > yt)[0][-1]
            rY = brentq(lambda q: float(ybp_f(np.array([q]))[0]) - yt, rr[j], rr[j + 1], xtol=1e-15 * rr[j], rtol=1e-15)
            d = np.geomspace(1e-11, 0.5, 80)
            x = x_P2(np.maximum(ybp_f(rY * (1 - d)) - yt, 0.0)); x = x[x > 0]
            CT = (x ** 2 / (1 - 2 * x) + yt) / x; CL = 2 * x * (1 - x) / (1 - 2 * x) ** 2
            for th in TH:
                Cth = CT * np.sin(th) ** 2 + CL * np.cos(th) ** 2
                for ac in (9.62e-14, 3.2e-9):
                    for c2 in (7.29e-3, 0.1):
                        for lam in (0.0, 1.0, 100.0):
                            for hv in (0.3, 1.0):
                                ok = roots_ok(Cth, lam, hv, ac, c2); viol += int(np.sum(~ok)); ncell += len(ok)
            dd = np.geomspace(1e-10, 1e-5, 30)
            xs = x_P2(np.maximum(ybp_f(rY * (1 - dd)) - yt, 0.0))
            slopes.append(float(np.polyfit(np.log(dd), np.log(2 * xs * (1 - xs) / (1 - 2 * xs) ** 2), 1)[0]))
y1_ok = viol == 0 and ncell > 0 and all(abs(s_ - 0.5) <= 0.02 for s_ in slopes)
check("Y1 [HS7, pre-declared] THE SHARED YIELD STRUCTURE: at H_S's z >= 1 yield surfaces on DE12's hosts every root of the exact block is "
      "real and >= 0 (criterion B's causal part) and C_L ~ d^(0.50 +- 0.02); for z < 0.635 there is no yield, and the zeros of the "
      "band-passed field carry the same (y)^(-1/2) susceptibility (the plain P2 zero-field limit)",
      f"violations {viol} of {ncell}; slopes [{min(slopes):.4f}, {max(slopes):.4f}] ({len(slopes)} surfaces)", y1_ok)
P(f"    {el()}")

# ---- R2 the ramp's well-definedness (reported)
Kb, Lam_ = sp.symbols("K Lambda", positive=True)
twoq = 1 - 9 * Lam_ / Kb ** 2
d_left = sp.diff(0 * twoq, Kb); d_right = sp.diff(twoq, Kb)
Kq0 = sp.sqrt(9 * Lam_)
jump = sp.simplify(d_right.subs(Kb, Kq0) - d_left)
check("R2 (reported) THE RAMP: max(0, 2q) is Lipschitz in <K>_h, so the action is well defined; its <K>-derivative jumps at q = 0 by the "
      "printed finite amount (a coefficient jump in the (v/c)^2-suppressed khronon channel, no delta-function force); the y-term's "
      "coefficient kappa is proportional to 2q and continuous", f"d(2q)/d<K> at q = 0: {jump} (left 0)", True, load_bearing=False)

# ============================================================================================ verdict
nlb = sum(1 for _, ok, lb in CH if lb and not ok)
banner("VERDICT")
_ok = {k_: OUT['checks'][k_]['pass'] for k_ in ('N1', 'N2', 'N3', 'N3b', 'N4', 'R1', 'Q1', 'Q2', 'Y1')}
_pf = {k_: ('PASS' if v else 'FAIL') for k_, v in _ok.items()}
_kr = [v['k_RBge1'] for (f_, z_), v in coef.items() if z_ <= Z_Q0 + 1e-3 and v['k_RBge1']]
_kq = max([v['kappa_G'] for (f_, z_), v in coef.items() if z_ <= Z_Q0 + 1e-3] or [0.0])
_krs = f"{min(a_ for a_, b_ in _kr):.2f}-{max(b_ for a_, b_ in _kr):.2f} h/Mpc" if _kr else "no k"
_t1 = ("varying the action through B[state] and y_th[state] gives O(1) LOCAL mean-field terms with leaf-averaged coefficients"
       if _ok['N1'] else "the O(1) local mean-field term is NOT reproduced on the test leaves")
_t2 = "momentum is conserved with them" if _ok['N2'] else "momentum is NOT conserved on the test leaves"
_t4 = ("the y-term screens sub-L Newtonian gravity at z > 0.635 by 1/(1 + kappa h^2)")
_t_pm = (f"""      Particle mesh: as formulated (B and y_th read from the state and varied), H_S's linearised psi-constraint is singular: R_B >= 1
      on k = {_krs} at z <= 0.635, where the y-term is off or negligible (kappa <= {_kq:.3f}; max R_B {RBmax_all:.1f}); if B is not varied, the field equations are
      not an action's.  A PM run of H_S as it stands would evolve an ill-posed (or non-conservative) system; it should wait for a
      reformulation of the state read.""" if RBmax_all >= 1.0 else
         """      Particle mesh: R_B < 1 on every scanned epoch; the mean-field terms must be carried by any PM run of H_S.""")
P(f"""  (H_S) 1. Nonlocality: {_t1} (N1: {_pf['N1']}); {_t2} (N2: {_pf['N2']}).  On FP13's headline state the B-term
        multiplies Newtonian gravity at k ~ 1/L by 1/(1 - R_B), max R_B = {RBmax_all:.3f} (N3: {_pf['N3']}; independent lattice check N3b:
        {_pf['N3b']}); {_t4}, kappa = {min(kGz):.2f}-{max(kGz):.2f} in FP13's Gaussian reading and {min(kHz):.1e}-{max(kHz):.1e} in a halo
        reading (N4: {_pf['N4']}).
      2. The matter readout adds no time derivative and no mode; it changes the psi-constraint's symbol to k^2 (1 + kappa h^2 - R_B),
         singular where R_B = 1 + kappa h^2 (on FP13's state at z <= 0.635, where kappa <= {_kq:.3f}: wherever R_B ~ 1); DE12's UV mechanism
         is absent (R1: {_pf['R1']}).
      3. The q = 0 ramp: |d sigma_8| {d_eps[0.05]:.1e}/{d_eps[0.01]:.1e}/{d_eps[0.002]:.1e} at eps = 0.05/0.01/0.002, at most {int(ncross.max())} crossing per sigma_8
         mode, the chord's largest step through z_q0 shrinks x{shrink_ramp:.1f} under 10x refinement (Q1: {_pf['Q1']}); lambda > 0 keeps phi
         determined where the yield vanishes, un-freezing at >= {min(v for k_, v in q2.items() if k_[1] <= 100.0):.0f} H for lambda <= 100 (Q2: {_pf['Q2']}).
      Shared yield structure (criterion B's roots, d^(1/2) exponents) at H_S's z >= 1 surfaces (Y1: {_pf['Y1']}).
{_t_pm}
  Not 'closed'.  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {nlb}.  Time {time.time() - T0:.0f} s.""")
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
json.dump(OUT, open(fn, "w"), indent=1, default=str)
P(f"  wrote {os.path.basename(fn)}")
_OUTF.close()
sys.exit(1 if nlb else 0)
