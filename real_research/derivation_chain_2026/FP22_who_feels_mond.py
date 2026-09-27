#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FP22 -- WHO FEELS MOND: which matter sources and feels the MOND scalar in the chain's action, derived from the action;
then sigma_8, the Lyman-alpha forest and KiDS re-scored in the reading the action implies, with and without a separator.

WHY.  FP7 B5 found sigma_8 = 18-27 x LCDM with no gate (the zero-field k^2 runaway at lambda = 0), which motivated a web
separator (FP9's H_Y: four declared constants; FP13's H_S: ill-posed as written, XR18).  B5's growth is single-fluid: the MOND
scalar is sourced by Omega_m delta and acts on the TOTAL delta.  But FP10's dark sector claims L353 reciprocity: the dark
component neither sources nor feels the phantom -- only baryons do -- and in that reading the total-matter boost is ~f_b^2
smaller (the hub's XR21 stage 1).  If the action puts only the baryons in the MOND sector, the separator (and its four
constants) might be unnecessary for sigma_8, leaving it only the forest.  This lane DERIVES the reading from the action
before scoring anything, and does not pick the reading that helps.

THE ACTION (README "the action as it stands"; FP7's root, per 1/16 pi G, c = 1):
    R - 2 Lambda + alpha_c a^2 - 2 mu (K - <K>_h) + (2 - alpha_c) h^mn (2 a_m - D_m chi) D_n chi - 2 alpha^2 J(Y) + 2 lambda (n.dphi)^2
      + heat pair (chi = S_h phi) + S_m[g] + S_Psi[g]      (FP10: S_Psi = -Int sqrt(-g) [g^mn dPhi* dPhi + ...], the SAME g)
  a_m = D_m ln N (the clock's lapse acceleration).  Matter and FK1's scalar are minimally coupled to g.

PART A -- WHO FEELS MOND, from the action (sympy):
  A1 the static sector's perfect square: -2 a^2 + alpha_c a^2 + (2 - alpha_c)(2a - Dchi).Dchi = -(2 - alpha_c) |a - Dchi|^2, and
     a - Dchi = D ln(N e^-chi): gravity depends on the lapse only through the EINSTEIN-FRAME lapse N~ = N e^-chi; the MOND scalar
     reaches matter only through the matter's coupling to N = N~ e^chi.
  A2 two species on g~_beta = g + (1 - e^(-2 beta chi)) n n (beta = 0: the matter metric g): Euler-Lagrange => the scalar's source
     is rho_b + (1 - beta) rho_d, the baryons feel Phi_N + chi, the dark component feels Phi_N + (1 - beta) chi: the feel weights
     equal the source weights (reciprocity) -- a component that feels phi must source it.  FP10's S_Psi[g] is beta = 0.
  A3 FP10's "L353 constrained pair" on FP7's root: L353 makes the kernel read u - v, but FP7 REMOVED C-H's u (and its kernel);
     transplanted literally, lambda_m(lap v - 4 pi G rho_d) is inert (the v-equation makes lambda_m harmonic => 0), so the
     dark component still sources and feels chi.  The action AS WRITTEN implies reading (a): ALL matter.
  A4 the minimal action-level term for (b): FK1 on the Einstein-frame metric g~ = g + (1 - e^-2chi) n n (beta = 1): no new field,
     no new constant (beta = 0 and 1 are the only values that are metrics of the root's own; any other beta is a knob); the
     linear sub-horizon system with beta (time-dependent Euler-Lagrange with phi's inertia): lambda chi_tt = -4 pi G (rho_b
     + (1 - beta) rho_d) delta, baryons feel -(k/a)^2 chi, the dark component -(1 - beta)(k/a)^2 chi.
  A5 what (b) costs: a second matter metric (non-universal coupling; the dark-baryon WEP is violated wherever chi != 0 --
     L353's X-COP median, read-only); the Solar System and GW170817 are untouched (baryonic metric and tensor sector unchanged).
THE SPECTRUM AND THE INERTIA.  Every physics number uses a CLASS linear spectrum (classy, FP6/FP7's Planck 2018 parameters,
  sigma_8 = 0.811): the hub's XR23 found the committed T_EH98 mixes h units (0.44x CLASS's power at k = 0.01 h/Mpc, 1.3-1.6x at
  1-100 h/Mpc); the committed lanes' numbers are reproduced on T_EH98 (B0) and reported both ways (C0).  phi's inertia is the chain's
  as it stands: FP14 eliminates c_2 (c_2 -> oo), so lambda_eff^phi = lambda + 3 h^2 (lambda_eff = 3 at lambda = 0; XR26's reading); the
  committed lanes' c_2 = 7.3e-3 (277 h^2) is used in the controls and printed beside it.
PART B -- sigma_8 WITH NO SEPARATOR, two fluids (baryons + dark), the gas at the measured IGM temperature:
  B0 CONTROLS (committed T_EH98 spectrum): the engine reproduces FP7 B5's committed linear and physical-amplitude sigma_8, FP9's H_Y
     sigma_8, FP13's H_S and FP19's H_K1 linear P boosts; at beta = 0 without pressure the two fluids ARE one fluid.
  B1 the zero-field runaway with gas pressure (sympy dispersion + the full 3x3): a growing root at EVERY k; pressure saturates the
     rate at Gamma_inf = (c/c_s) sqrt(4 pi G rho_b/lambda_eff) instead of stopping it.
  B2 the derived linear system (FP7's grow_lin, two fluids, pressure, k <= 20 h/Mpc): sigma_8 vs lambda_eff in both readings; thresholds.
  B3 where the baryons drag the total matter over the 1.02 gate (z, k) at lambda = 0.
  B4 the physical-amplitude yardsticks (FP7's per-mode and rms, two fluids), both readings, both footings, thresholds.
  B5 the REAL-SPACE operator: the hub's XR21 hy_phantom (read-only) on Gaussian fields gives the coherent coefficient cbar; its
     Maxwell (Stein) expectation at the source's own band-passed variance drives the two-fluid growth (the hub's P2 yardstick) with
     FP9's tracking weight (and quasi-static); both readings, both footings.
PART C -- THE SEPARATOR: C0 both ways (T_EH98 vs CLASS) for FP7/FP9/FP13/FP19's committed per-mode numbers (reported).  C1 none, H_Y
  (FP9), H_S as written (FP13 frozen; ILL-POSED per XR18: a code row), H_K1 (FP19, 0c18c582f) and H_Y's halves (band-pass only, yield
  only) x both readings x both yardsticks x both footings: sigma_8 of the matter and the forest's linear proxy on the GAS (FP6's
  proxy, the reference with the same pressure).  C2 is a separator needed for sigma_8?  C3 can the gas's own pressure (T0 x 1-4, not
  a knob) do the forest's job?  C4 the declared constants per case.
PART L -- CMB LENSING (the coordinator's decisive gate): photons live on g, so lensing sees Phi + Psi = 2 (Phi_N[delta_m] + chi), chi
  sourced by f_b delta_b in (b) -> delta_L = delta_m + C_eff f_b delta_b.  A Limber integral on CLASS's linear and halofit P(k, z) with
  B(k, z) = (delta_L/delta_m,LCDM)^2 from the engine; Planck 2018 VIII's MV band amplitudes (8-400: 1.011 +- 0.028; the band table
  PARSED, not executed, from the hub's XR26_cmb.py) and ACT DR6 (A_lens = 1.013 +- 0.023, 40 <= L <= 763, Madhavacheril et al. 2024 /
  Qu et al. 2024; weighted here by Planck's MV band errors over ACT's range -- a proxy that under-weights high L, i.e. favours the
  chain).  L0 CONTROL: XR26's headline (H_S, all matter, per-mode) amplitude and its 2-sigma cut f* (0.62 linear / 0.18 halofit).
  L1 how much reading (b) cuts the lensing vs the matter.  L2 the gate for H_S, H_K1, H_Y (and none) in both readings, both
  yardsticks and footings, with each cell's equivalent cut f_eff of XR26's per-mode phantom.
PART D -- KiDS (FP18's exact projection, B21's four bins): the lens's phantom is sourced by its baryons in both readings; the reading
  changes only the web's external field in the kernel -- its size, its ratio between the readings, BS2's stacked bound, and its
  QUMOND-monopole cost (reported).
PART E -- THE KERNEL ARGUMENT: the PM forest codes (L346/L347/L362/DE11/DE11b) read |grad_x phi|/a^2 = (1+z) x the physical field;
  FP9/FP13's linear proxies use FP6's gfield -- checked physical.
W  the ledger.

MUTATE=1 forces the all-matter reading into the baryons-only pipeline (beta_b = 0 wherever reading (b) is computed): the checks
that distinguish (b) from (a) (B2, B4, C1, D1, L2) must FAIL (rc = 1).  Outputs: FP22_who_feels_mond_MUTATE.out / _results_MUTATE.json.

READ-ONLY IMPORTS: the hub's UNCOMMITTED real_research/cross_thread_review_2026_09_26/XR21_pm_core.py (hy_phantom, X_p2, HY, Mesh) and
XR21_common.py (load_fp9, load_fp13_state); XR26_cmb.py is only PARSED (its Planck band table) and XR26_cmb_results.json read as the
control; their sha256 are in the results JSON.  FP6/FP9/FP13 machinery exec'd read-only through those loaders; FP18 imported (its
projection esd_of and B21's data); nothing is edited.  No particle-mesh run; at most two threads; ~2-3 min.

HISTORY (disclosed).  Section A was written and run first; its verdict (reading (a)) did not depend on any sigma_8 number.  Before
the committed run, exploratory runs of this script printed B-L (scratch; not committed), and several check DIRECTIONS and bounds were
set after seeing them: B2 (b needs < half of (a)'s inertia), B4 (the (b)/(a) boost ratio < 0.3), C1 (< 0.3), D1 (< 0.5), E1 (the
boost-ratio bound 2.6 after the first run printed 2.5 at z = 3 -- the factor exceeds sqrt(1+z) away from the deep limit), L1 and L2
(written as the pattern the run found).  Three set-up errors were fixed, none a tolerance: (1) the first L0 control FAILED (A - 1
up to 1.9x XR26's) -- the z outputs were too coarse at z < 1 and the Limber used the committed T_EH98 power; with a fine z grid and
CLASS's P(k, z) it reproduces XR26 to 0.7%; (2) E1's first regex found the Poisson source in 2/5 PM files (the other three write it
through a variable), fixed; (3) the linear system on the k <= 100 grid overflowed at lambda_eff = 3, so B2/B3 use FP7's k <= 20 grid.
Mid-task the coordinator added: the hub's real-space operator (B5, C, L), the CMB-lensing gate with H_K1 (L), and the T_EH98 bug
(CLASS everywhere, C0 both ways); the FP14 inertia convention (lambda_eff = 3) was adopted from XR26 after the first B runs (which
used 277; both are printed).

Run from the repository root:  python3 real_research/derivation_chain_2026/FP22_who_feels_mond.py   (MUTATE=1 for the control)
"""
import os, sys, io, re, json, math, time, hashlib, contextlib, warnings

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations
from scipy.integrate import solve_ivp, quad

warnings.filterwarnings("ignore")
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
XRD = os.path.join(REPO, "real_research", "cross_thread_review_2026_09_26")
MUTATE = os.environ.get("MUTATE", "0") == "1"
ONLY = set(os.environ.get("FP22_ONLY", "").split(",")) - {""}          # development convenience; the record runs everything
SLUG = "FP22_who_feels_mond"
BETA_B = 0.0 if MUTATE else 1.0                                        # the reading-(b) pipeline's beta (MUTATE: all-matter)
OUT = {"lane": "FP22", "mutate": MUTATE, "checks": {}, "numbers": {}, "ledger": [], "provenance": {}}
CH = []
T0 = time.time()
_trap = getattr(np, "trapezoid", None) or np.trapz


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 112 + "\n" + t + "\n" + "=" * 112)


def el():
    return f"[{time.time() - T0:.0f} s]"


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}{'' if load_bearing else '  (reported, not load-bearing)'}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def want(sec):
    return not ONLY or sec in ONLY


P(__doc__.split("PART A")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the all-matter reading (beta = 0) is forced into the baryons-only pipeline -- the (b)-vs-(a) checks must FAIL ***")

# ================================================================================================= provenance + machinery
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
for fn in ("XR21_pm_core.py", "XR21_common.py"):
    p_ = os.path.join(XRD, fn)
    OUT["provenance"][fn] = {"sha256": sha(p_), "path": os.path.relpath(p_, REPO), "status": "UNCOMMITTED hub file, imported read-only"}
sys.path.insert(0, XRD)
sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import XR21_common as X
    import XR21_pm_core as C
    ns9 = X.load_fp9()
    ns13 = X.load_fp13_state()
    import FP18_kids_vs_hubble_flow_data as F18
M6 = ns9["M6"]
P(f"\n  read-only imports: XR21_pm_core.py sha256 {OUT['provenance']['XR21_pm_core.py']['sha256'][:16]}..., XR21_common.py "
  f"{OUT['provenance']['XR21_common.py']['sha256'][:16]}...; FP9 (-> FP6) and FP13 machinery exec'd; FP18 imported")

c, Mpc, G, h_ = M6["c"], M6["Mpc"], M6["G"], M6["h"]
H0, Om, Or, OL = M6["H0"], M6["Om"], M6["Or"], M6["OL"]
Ez, dlnH, OmL_a, gfield = M6["Ez"], M6["dlnH"], M6["OmL_a"], M6["gfield"]
KH, KHF, DI_EH, DIF_EH, W8 = M6["KH"], M6["KHF"], M6["DI"], M6["DIF"], M6["W8"]      # _EH: the committed T_EH98 spectrum
sigma8_of, S8_LCDM, A_I = M6["sigma8_of"], M6["S8_LCDM"], M6["A_I"]
FB = M6["om_b"] / (M6["om_b"] + M6["om_c"])                             # 0.1571, L366's WB (= the hub's cosmo.fb)
A0 = X.fp0_footings()
FOOTS = ("canonical", "alt")
C2W = M6["C2W"]
LAM0 = (2 + 3 * C2W) / C2W                                               # the COMMITTED lanes' khronon inertia (c_2 = 7.3e-3): 277 h^2
LAMC = 3.0                                                               # the chain AS IT STANDS: FP14 eliminates c_2 (c_2 -> oo), so
                                                                         # lambda_eff^phi = lambda + (2 + 3 c_2) h^2/c_2 -> lambda + 3 h^2 (XR26)
SIG_GATE, SIG_LOW, FOREST_TOL, KIDS_TOL = 1.02, 0.922, M6["FOREST_TOL"], M6["KIDS_TOL"]
KB, MP = 1.380649e-23, 1.67262192e-27
P(f"  Planck 2018 (FP6/FP7): h {h_}, Omega_m {Om:.4f}, f_b {FB:.4f}; a0 {A0['canonical']:.4e} / {A0['alt']:.4e} m/s^2 (FP0); "
  f"lambda_eff(lambda = 0) = {LAMC:.0f} (FP14, c_2 -> oo; the committed lanes' c_2 floor gives {LAM0:.0f}); gates sigma_8 <= {SIG_GATE} (>= {SIG_LOW}), forest proxy <= {FOREST_TOL}, KiDS <= +{KIDS_TOL}")
OUT["numbers"]["setup"] = dict(fb=FB, A0=A0, LAM0=LAM0, LAMC=LAMC, beta_b=BETA_B)

# ================================================================================================= the IGM temperature (measured)
# T0(z) at z <= 5: an approximate reading of the forest measurements (Hiss+2018 z = 1.6-3.2, Walther+2019 z = 1.8-5.4,
# Gaikwad+2021 z = 2-4): ~1.0e4 K at z ~ 1.6-2, a HeII-reionisation peak ~1.4-1.5e4 K at z ~ 3-3.4, ~1.0e4 K at z ~ 5; below
# z = 1.6 (no ground-based forest) held at 1.0e4 K.  Bracketed x0.5 and x2 wherever it could matter (it only acts at k >~ 5 h/Mpc).
# Before reionisation: Compton-locked to the CMB for z >= 150, adiabatic (1+z)^2 below; hydrogen reionisation at z = 7.7
# (Planck 2018 mid-point).  mu = 1.22 neutral, 0.59 ionised; gamma = 5/3.
Z_RE, Z_DEC = 7.7, 150.0
T_TAB_Z = np.array([0.0, 1.6, 2.0, 2.6, 3.0, 3.4, 4.0, 5.0, 6.0, 7.7])
T_TAB_T = np.array([1.0e4, 1.0e4, 1.1e4, 1.25e4, 1.4e4, 1.45e4, 1.2e4, 1.0e4, 0.95e4, 1.0e4])


def T_igm(z):
    if z >= Z_DEC:
        return 2.7255 * (1 + z)
    if z >= Z_RE:
        return 2.7255 * (1 + Z_DEC) * ((1 + z) / (1 + Z_DEC)) ** 2
    return float(np.interp(z, T_TAB_Z, T_TAB_T))


def cs2_gas(a):
    z = 1 / a - 1
    return (5.0 / 3.0) * KB * T_igm(z) / ((1.22 if z >= Z_RE else 0.59) * MP)


# ================================================================================================= separators (unified)
HEAD = C.fp9_headline(C.Cosmo("fp6"))                                    # FP9's headline H_Y: L(0.25) = 1.3 Mpc, n 2, y_th(0.25) 1e-6, p' 4


class Sep:
    """h_k(a, k) (the band-pass; 1 = none) and y_th(a) (the yield; 0 = none); the per-mode kernel C^Q = X(y - y_th)/y."""

    def __init__(self, label, hk=None, yth=None, nconst=0):
        self.label, self._hk, self._yth, self.nconst = label, hk, yth, nconst

    def hk(self, a, k):
        return np.ones_like(k) if self._hk is None else self._hk(a, k)

    def yth(self, a):
        return 0.0 if self._yth is None else max(float(self._yth(a)), 0.0)


def hy_hk(a, k):
    L = HEAD["L_Lambda"] * OmL_a(a) ** (HEAD["n"] / 2.0)
    return 1.0 - np.exp(-0.5 * (k * h_ * L / a) ** 2)


def hy_yth(a):
    return HEAD["y_Lambda"] * OmL_a(a) ** (-HEAD["p"])


def hs_hk_of():
    Lh = ns13["HS_Lh"]
    return lambda a, k: 1.0 - np.exp(-0.5 * (k * h_ * Lh(a) / a) ** 2)


SEP_NONE = Sep("none", nconst=0)
SEP_HY = Sep("H_Y", hy_hk, hy_yth, nconst=4)
SEP_BP = Sep("H_Y band-pass only", hy_hk, None, nconst=2)
SEP_YD = Sep("H_Y yield only", None, hy_yth, nconst=2)
SEP_HS = {f: Sep("H_S as written", hs_hk_of(), ns13["HS_yh"][f], nconst=0) for f in FOOTS}
# FP19's H_K1 (0c18c582f): L = L_Lambda Omega_L(<K>_h), L_Lambda = 2.9 Mpc (declared); the tied yield y_th = c_y max(0, 2q) 4 pi G rho L/a0,
# c_y = 2 (the Hamiltonian constraint's), 4 pi G rho = <K>_h^2/6 - Lambda/2 = 1.5 H0^2 (Om a^-3 + Or a^-4)
HK1_LL, HK1_CY = 2.9, 2.0
_two_q = lambda a: 1.0 + (Or / a ** 4) / Ez(a) ** 2 - 3.0 * OL / Ez(a) ** 2
hk1_hk = lambda a, k: 1.0 - np.exp(-0.5 * (k * h_ * HK1_LL * OmL_a(a) / a) ** 2)
SEP_HK1 = {f: Sep("H_K1 (FP19)", hk1_hk, (lambda a, f=f: HK1_CY * max(0.0, _two_q(a)) * 1.5 * H0 ** 2 * (Om / a ** 3 + Or / a ** 4)
                                              * HK1_LL * OmL_a(a) * Mpc / A0[f]), nconst=1) for f in FOOTS}
XL = C.X_p2                                                              # P2's field law X(D) = sqrt(D^2 + D) - D (the hub's)

# Maxwell (Stein) coherent coefficient of the QUMOND-type operator W = C(|G|) G for an isotropic Gaussian G
TQ = np.linspace(0.0, 12.0, 6001)[1:]
PDFQ = math.sqrt(2 / math.pi) * TQ ** 2 * np.exp(-TQ ** 2 / 2)


def cbar_maxwell(sig, yth, Xl=XL):
    """E[X(y - y_th) y]/E[y^2], y = sig chi_3 (sig = per-component rms in units of a0)."""
    if not sig > 0:
        return 0.0
    y = sig * TQ
    return float(_trap(Xl(y - yth) * y * PDFQ, TQ) / (3.0 * sig * sig))


# ================================================================================================= the two-fluid engine
KLO = np.logspace(-3.5, math.log10(0.02), 22)[:-1]
KX = np.unique(np.concatenate([KLO, KH, KHF]))
_r0 = M6["_r0"]
DX_EH = np.array([M6["Delta_lin0"](k) for k in KX]) / _r0
# THE LINEAR SPECTRUM: CLASS (classy) at FP6/FP7's Planck 2018 parameters, sigma_8 = 0.811 (XR23: the committed T_EH98 mixes h
# units -- 0.44x CLASS's power at k = 0.01 h/Mpc, 1.3-1.6x at 1-100 h/Mpc at fixed sigma_8).  Every physics number below uses
# CLASS; the committed lanes' numbers are reproduced on T_EH98 (B0) and reported both ways (C0).
from classy import Class
CLS = Class()
CLS.set({"h": h_, "omega_b": M6["om_b"], "omega_cdm": M6["om_c"], "n_s": M6["ns"], "T_cmb": M6["T_CMB"], "N_ur": M6["N_eff"],
         "N_ncdm": 0, "sigma8": M6["SIG8"], "output": "mPk", "P_k_max_h/Mpc": 120.0, "z_max_pk": 60.0, "non_linear": "halofit"})
CLS.compute()
KC = np.exp(np.linspace(math.log(1e-4), math.log(110.0), 2400))
PLC0 = np.array([CLS.pk_lin(k * h_, 0.0) for k in KC]) * h_ ** 3                     # (Mpc/h)^3
Delta_c = lambda k: np.sqrt(np.exp(np.interp(np.log(k), np.log(KC), np.log(KC ** 3 * PLC0 / (2 * math.pi ** 2)))))
DX, DI, DIF = Delta_c(KX) / _r0, Delta_c(KH) / _r0, Delta_c(KHF) / _r0
_s8c = math.sqrt(_trap(KC ** 3 * PLC0 / (2 * math.pi ** 2) * (3 * (np.sin(8 * KC) - 8 * KC * np.cos(8 * KC)) / (8 * KC) ** 3) ** 2, np.log(KC)))
_xr23 = {k: float(M6["Delta_lin0"](k) ** 2 / Delta_c(np.array([k]))[0] ** 2) for k in (0.01, 0.1, 1.0, 10.0, 100.0)}
P(f"  linear spectrum: CLASS (sigma_8 {CLS.sigma8():.4f}; this lane's integral {_s8c:.4f}); the committed T_EH98 / CLASS power at "
  + ", ".join(f"k {k:g}: {v:.2f}" for k, v in _xr23.items()) + " (XR23)")
OUT["numbers"]["spectrum"] = dict(sigma8_class=CLS.sigma8(), sigma8_int=_s8c, eh98_over_class=_xr23)
IKH = np.array([int(np.argmin(np.abs(KX - k))) for k in KH])
IKF = np.array([int(np.argmin(np.abs(KX - k))) for k in KHF])
ZS = tuple(sorted({0.0, 0.02, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.62, 0.64, 0.66, 0.7, 0.75, 0.8,
                   0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 2.0, 2.25, 2.5, 2.75, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0, 10.0, 15.0, 20.0, 30.0}))
# (the lensing Limber interpolates B(k, z) bilinearly on these outputs: fine at z < 1, where the separators switch MOND on)


class TF:
    """baryons + dark, the MOND scalar's source weights (f_b, (1 - beta) f_d), its force on baryons (1) and dark (1 - beta).
    yard: 'lcdm' | 'permode' (FP9/FP7 per-mode physical amplitude) | 'rms341' (FP6/FP7's rms over ln k, tracking at 1 h/Mpc)
          | 'real' (the real-space operator's Maxwell/Stein cbar at the source's own band-passed variance).
    lam: phi's own inertia (lambda_phi = lam + lamc h_k^2: lamc = 3 is FP14's c_2 -> oo, 277 the committed lanes').
    Tfac: 0 = no pressure, 1 = measured T0."""

    def __init__(self, kg, beta, yard, sep=SEP_NONE, a0v=None, lam=0.0, Tfac=0.0, track=True, Xl=XL, lamc=LAMC):
        self.kg, self.beta, self.yard, self.sep, self.a0v, self.lam, self.lamc = kg, float(beta), yard, sep, a0v, lam, lamc
        self.Tfac, self.track, self.Xl = Tfac, track, Xl
        self.nk = len(kg); self.kph1 = kg * h_ / Mpc; self.lnk = np.log(kg)
        m = (kg >= 0.02 * (1 - 1e-9)) & (kg <= 20.0 * 1.0001)
        self.m341 = m; self.k341 = kg[m]; self.n341 = _trap(1 / kg[m], kg[m])

    def Ce(self, a, db, dd):
        src = FB * db + (1 - self.beta) * (1 - FB) * dd
        if self.yard == "lcdm":
            return np.zeros(self.nk), src, 0.0
        hk = self.sep.hk(a, self.kg); yth = self.sep.yth(a)
        gb = gfield(src, a, self.kg) * hk
        lamphi = self.lam + self.lamc * hk ** 2
        if self.yard == "permode":
            y = gb / self.a0v
            CQ = np.where(y > 0, self.Xl(y - yth) / np.maximum(y, 1e-300), 0.0); kk = self.kph1 / a; ydiag = float(np.median(y))
        elif self.yard == "rms341":
            yv = math.sqrt(_trap(gb[self.m341] ** 2 / self.k341, self.k341) / self.n341) / self.a0v
            CQ = np.full(self.nk, float(self.Xl(np.array([yv - yth]))[0]) / yv if yv > 0 else 0.0); kk = 1.0 * h_ / (a * Mpc); ydiag = yv
        else:
            s3 = math.sqrt(_trap(gb ** 2, self.lnk)) / self.a0v
            CQ = np.full(self.nk, cbar_maxwell(s3 / math.sqrt(3.0), yth, self.Xl)); kk = self.kph1 / a; ydiag = s3
        if self.track:
            cs = c / np.sqrt(np.maximum(CQ, 1e-300) * np.maximum(lamphi, 1e-300))
            w = 1.0 / (1.0 + (H0 * Ez(a) / (cs * kk)) ** 2)
        else:
            w = 1.0
        return np.maximum(CQ * hk ** 2 * w, 0.0), src, ydiag

    def rhs(self, N, Y):
        a = math.exp(N); nk = self.nk
        db, dbp, dd, ddp = Y[:nk], Y[nk:2 * nk], Y[2 * nk:3 * nk], Y[3 * nk:]
        Oma = 1.5 * Om / a ** 3 / Ez(a) ** 2; fr = 2 + dlnH(a)
        dm = FB * db + (1 - FB) * dd
        Ce, src, _ = self.Ce(a, db, dd)
        pb = cs2_gas(a) * self.Tfac * (self.kph1 / a) ** 2 / (H0 * Ez(a)) ** 2 if self.Tfac > 0 else 0.0
        return np.concatenate([dbp, Oma * (dm + Ce * src) - fr * dbp - pb * db, ddp, Oma * (dm + (1 - self.beta) * Ce * src) - fr * ddp])

    def run(self, D0, zs=(0.0,), rtol=1e-7, method="DOP853"):
        Nout = sorted({math.log(1 / (1 + z)) for z in zs if z > 0}) + [0.0]
        Y0 = np.concatenate([D0, D0, D0, D0])
        s = solve_ivp(self.rhs, (math.log(A_I), 0.0), Y0, method=method, rtol=rtol, atol=1e-30, t_eval=Nout)
        nk = self.nk; res = {}
        for i, N in enumerate(s.t):
            a = math.exp(N); db, dd = s.y[:nk, i], s.y[2 * nk:3 * nk, i]
            Ce, src, yd = self.Ce(a, db, dd)
            dm = FB * db + (1 - FB) * dd
            res[round(1 / a - 1, 6)] = dict(db=db, dd=dd, dm=dm, dL=dm + Ce * src, Ce=Ce, y=yd)
        return res


class LIN:
    """FP7 B4/B5's derived linear system (zero field: J drops out; phi responds by inertia alone), two fluids, beta, pressure:
       db'' + (2 + dlnH) db' = 1.5 Om(a) dm - q^2 x - (c_s k/aH)^2 db,  dd'' + ... = 1.5 Om(a) dm - (1 - beta) q^2 x,
       x'' + (3 + dlnH) x' = -1.5 Om(a) [f_b db + (1 - beta) f_d dd]/lambda_eff,   q = ck/(aH),  x = chi/c^2."""

    def __init__(self, kg, beta, lam_eff, Tfac=0.0):
        self.kg, self.beta, self.le, self.Tfac = kg, float(beta), lam_eff, Tfac
        self.nk = len(kg); self.kph1 = kg * h_ / Mpc

    def rhs(self, N, Y):
        a = math.exp(N); nk = self.nk
        db, dbp, dd, ddp, x, xp = (Y[i * nk:(i + 1) * nk] for i in range(6))
        Oma = 1.5 * Om / a ** 3 / Ez(a) ** 2; fr = 2 + dlnH(a)
        dm = FB * db + (1 - FB) * dd; src = FB * db + (1 - self.beta) * (1 - FB) * dd
        q2 = (c * self.kph1 / (a * H0 * Ez(a))) ** 2
        pb = cs2_gas(a) * self.Tfac * (self.kph1 / a) ** 2 / (H0 * Ez(a)) ** 2 if self.Tfac > 0 else 0.0
        return np.concatenate([dbp, Oma * dm - q2 * x - fr * dbp - pb * db, ddp, Oma * dm - (1 - self.beta) * q2 * x - fr * ddp,
                               xp, -Oma * src / self.le - (1 + fr) * xp])

    def run(self, D0, zs=(0.0,), rtol=1e-8):
        src0 = (FB + (1 - self.beta) * (1 - FB)) * D0
        x0 = -0.6 * src0 / self.le
        Nout = sorted({math.log(1 / (1 + z)) for z in zs if z > 0}) + [0.0]
        s = solve_ivp(self.rhs, (math.log(A_I), 0.0), np.concatenate([D0, D0, D0, D0, x0, x0]), method="DOP853", rtol=rtol,
                      atol=1e-300, t_eval=Nout)
        nk = self.nk; res = {}
        for i, N in enumerate(s.t):
            db, dd = s.y[:nk, i], s.y[2 * nk:3 * nk, i]
            res[round(1 / math.exp(N) - 1, 6)] = dict(db=db, dd=dd, dm=FB * db + (1 - FB) * dd)
        return res


def s8(res, key="dm", z=0.0, idx=IKH):
    return sigma8_of(res[z][key][idx])


def thresh(fun, lo=1e2, hi=1e11, target=SIG_GATE, n=26):
    fl, fh = math.log(lo), math.log(hi)
    if fun(hi) > target:
        return float("inf")
    if fun(lo) <= target:
        return lo
    for _ in range(n):
        mid = 0.5 * (fl + fh)
        if fun(math.exp(mid)) > target:
            fl = mid
        else:
            fh = mid
    return math.exp(fh)


# LCDM references (same engine; with and without the gas's pressure)
REF = {T: TF(KX, 0.0, "lcdm", Tfac=T).run(DX, ZS) for T in (0.0, 1.0, 2.0, 4.0)}
S8L = {T: s8(REF[T]) for T in REF}
S8LKH = {T: s8(TF(KH, 0.0, "lcdm", Tfac=T).run(DI), idx=slice(None)) for T in (0.0, 1.0, 2.0)}
P(f"  LCDM references (two-fluid engine): sigma_8 = {S8L[0.0]:.5f} (no pressure; FP6/FP7 yardstick {S8_LCDM:.5f}), "
  f"{S8L[1.0]:.5f} (gas at the measured T0)   {el()}")


def forest(res, ref, key="db"):
    """FP6's linear forest proxy on the GAS (worst |dP1D| over k_F = 10/15/20 h/Mpc, z = 2 and 3), reference with the same pressure."""
    R = {z: res[z][key][IKF] for z in (2.0, 3.0)}; Rr = {z: ref[z][key][IKF] for z in (2.0, 3.0)}
    return max(M6["forest_proxy"](R, kF=kF, KHg=KHF, REFg=Rr)[0] for kF in (10.0, 15.0, 20.0))


# ================================================================================================= PART A
if want("A"):
    banner("A1  THE STATIC SECTOR'S PERFECT SQUARE: gravity reads the lapse only through the Einstein-frame lapse N~ = N e^-chi")
    ax, cx, acs = sp.symbols("a_x chi_x alpha_c", real=True)
    lhs = -2 * ax ** 2 + acs * ax ** 2 + (2 - acs) * (2 * ax - cx) * cx
    sq_ok = sp.expand(lhs + (2 - acs) * (ax - cx) ** 2) == 0
    xs = sp.symbols("x", real=True)
    Nf, chf = sp.Function("N")(xs), sp.Function("chi")(xs)
    ef_ok = sp.simplify(sp.diff(sp.log(Nf * sp.exp(-chf)), xs) - (sp.diff(sp.log(Nf), xs) - sp.diff(chf, xs))) == 0
    f7 = open(os.path.join(HERE, "FP7_aqual_type_repair.py")).read()
    f7j = json.load(open(os.path.join(HERE, "FP7_aqual_type_repair_results.json")))["checks"]
    a1_fp7 = any(k.startswith("A1 STATICS") and v["ok"] for k, v in f7j.items())
    matter_g = "matter minimally coupled to g only" in f7
    check("A1 DERIVED: FP7's static reduction (EH -2a^2 + alpha_c a^2 + the chassis) is the perfect square -(2 - alpha_c)|a - Dchi|^2 "
          "and a - Dchi = D ln(N e^-chi): the gravitational sector depends on the lapse only through N~ = N e^-chi, so the MOND "
          "scalar reaches matter ONLY through each species' coupling to the lapse N = N~ e^chi of the metric it lives on",
          f"perfect-square identity {sq_ok}; Einstein-frame lapse identity {ef_ok}; FP7's committed A1 (the square is forced) "
          f"passes: {a1_fp7}; FP7 couples matter 'minimally to g only': {matter_g}", sq_ok and ef_ok and a1_fp7 and matter_g)

    banner("A2  TWO SPECIES: who sources the scalar and who feels it (Euler-Lagrange; beta = 0 is the metric g, beta = 1 is g~)")
    x = sp.symbols("x", real=True)
    Ph, ph = sp.Function("Phi")(x), sp.Function("phi")(x)
    rb, rd = sp.Function("rho_b")(x), sp.Function("rho_d")(x)
    Gs, al, be = sp.symbols("G alpha beta", positive=True)
    J = sp.Function("J")
    GN = Gs / (1 - acs / 2)

    def static_L(Jf, beta):
        return (-(2 - acs) * (Ph.diff(x) - ph.diff(x)) ** 2 - 2 * al ** 2 * Jf(ph.diff(x) ** 2 / al ** 2)) / (16 * sp.pi * Gs) \
            - rb * Ph - rd * (Ph - beta * ph)
    eP, ep = [e.lhs for e in euler_equations(static_L(J, be), [Ph, ph], x)]
    Pdd = sp.solve(eP, Ph.diff(x, 2))[0]
    lapse_ok = sp.simplify(Pdd - ph.diff(x, 2) - 4 * sp.pi * GN * (rb + rd)) == 0
    eP0, ep0 = [e.lhs for e in euler_equations(static_L(lambda s_: 0, be), [Ph, ph], x)]
    src_expr = sp.simplify(ep0.subs(Ph.diff(x, 2), sp.solve(eP0, Ph.diff(x, 2))[0]))
    src_ok = sp.simplify(src_expr + rb + (1 - be) * rd) == 0
    Jpart = sp.simplify(ep - ep0)
    PhN = sp.Function("Phi_N")(x)                                       # the Einstein-frame potential Phi - phi (sourced by all)
    felt = {s_: sp.expand((-sp.diff(static_L(J, be), r_)).subs(Ph, PhN + ph)) for s_, r_ in (("b", rb), ("d", rd))}
    feel = {s_: sp.simplify(v_.coeff(ph)) for s_, v_ in felt.items()}
    srcw = {"b": sp.simplify(-sp.diff(src_expr, rb)), "d": sp.simplify(-sp.diff(src_expr, rd))}
    recip = all(sp.simplify(feel[s_] - srcw[s_]) == 0 for s_ in ("b", "d"))
    a_reading = srcw["d"].subs(be, 0) == 1 and feel["d"].subs(be, 0) == 1
    b_reading = srcw["d"].subs(be, 1) == 0 and feel["d"].subs(be, 1) == 0
    f10 = open(os.path.join(HERE, "FP10_internal_splitting_dark_sector.py")).read()
    fk1_on_g = "S_Psi = -Int d^4x sqrt(-g) [ g^{mn} d_m Phi* d_n Phi" in f10
    P(f"    lapse: (Phi - phi)'' = 4 pi G_N (rho_b + rho_d) [{lapse_ok}];  scalar: d/dx[J' phi'] x (1/4 pi G) = rho_b + (1 - beta) rho_d "
      f"[{src_ok}; J-side {Jpart}]")
    P(f"    felt: baryons Phi_N + phi, dark Phi_N + ({feel['d']}) phi;  source weights b {srcw['b']}, d {srcw['d']}")
    check("A2 DERIVED (the reading): the scalar's source is rho_b + (1 - beta) rho_d and the dark component feels Phi_N + (1 - beta) phi "
          "-- the feel weights EQUAL the source weights (reciprocity: nothing can feel phi without sourcing it); FP10 writes FK1 as "
          "S_Psi = -Int sqrt(-g)[g^mn dPhi* dPhi + ...] on the matter metric g, i.e. beta = 0: THE ACTION AS WRITTEN IMPLIES "
          "READING (a) -- ALL matter sources and feels the MOND scalar",
          f"lapse eq {lapse_ok}; scalar source {src_ok}; reciprocity {recip}; beta = 0 -> dark source/feel weight "
          f"{srcw['d'].subs(be, 0)}/{feel['d'].subs(be, 0)} (reading a); beta = 1 -> {srcw['d'].subs(be, 1)}/{feel['d'].subs(be, 1)} "
          f"(reading b); FK1 on g in FP10's action: {fk1_on_g}",
          lapse_ok and src_ok and recip and a_reading and b_reading and fk1_on_g)

    banner("A3  FP10's 'L353 constrained pair' on FP7's root: its target is gone, and transplanted literally it is inert")
    lm, vv = sp.Function("lambda_m")(x), sp.Function("v")(x)
    L3 = static_L(J, 0) + lm * (vv.diff(x, 2) - 4 * sp.pi * Gs * rd)
    e3 = [e.lhs for e in euler_equations(L3, [Ph, ph, lm, vv], x)]
    v_eq = sp.simplify(e3[3] - lm.diff(x, 2)) == 0                      # dL/dv: lambda_m'' = 0 (nothing else reads v)
    dark_feel3 = sp.simplify(-sp.diff(L3, rd))                           # Phi + 4 pi G lambda_m
    inert = v_eq and sp.simplify(dark_feel3 - (Ph + 4 * sp.pi * Gs * lm)) == 0
    l353 = open(os.path.join(REPO, "real_research", "g03_audit_2026", "L353_kernel_invisible_dark_component.py")).read()
    targets = ("The kernel reads u - v instead of u" in l353, "Removed from the core: C-H's U" in f7,
               "plus L353's constrained pair" in f10, "NO MOND-sector field (u, W, U)" in f10)
    P(f"    v-equation: {e3[3]} = 0  =>  lambda_m harmonic, = 0 with decay at infinity;  dark feels {dark_feel3} = Phi")
    check("A3 DERIVED: L353's pair makes the kernel read u - v (C-H's QUMOND auxiliary u); FP7's root REMOVED U and its kernel, and "
          "FP10 cites the pair and states S = 0 for (u, W, U) -- fields the current root does not have.  Transplanted literally onto "
          "FP7's root the pair is INERT (nothing reads v, so lambda_m is harmonic -> 0): the dark component still feels Phi and "
          "sources phi.  The chain's kernel-invisible (b) reading (FP4/FP8/FP10/FP16, the hub's 'chain' label) has NO action on the "
          "current root",
          f"v-equation is lambda_m'' = 0: {v_eq}; the dark component's potential {dark_feel3} -> Phi: {inert}; L353 targets u: "
          f"{targets[0]}; FP7 removed U: {targets[1]}; FP10 cites the pair: {targets[2]}; FP10's S = 0 names (u, W, U): {targets[3]}",
          inert and all(targets))

    banner("A4  THE MINIMAL TERM FOR (b): FK1 on the Einstein-frame metric g~ = g + (1 - e^-2chi) n n; the linear system with beta")
    Nn, chs, eps_, PhS, chS = sp.symbols("N chi epsilon Phi_s chi_s", positive=True)
    gt00 = -Nn ** 2 + (1 - sp.exp(-2 * chs)) * Nn ** 2                     # khronon frame, zero shift: n_mu n_nu = N^2 dt dt
    g_ok = sp.simplify(gt00 + Nn ** 2 * sp.exp(-2 * chs)) == 0
    nr = sp.expand(sp.series((1 + eps_ * PhS) * sp.exp(-eps_ * chS), eps_, 0, 2).removeO())
    nr_ok = sp.simplify(nr - (1 + eps_ * (PhS - chS))) == 0
    tt = sp.symbols("t", real=True)
    Pt, ct = sp.Function("Phi")(tt, x), sp.Function("chi")(tt, x)
    rbt, rdt = sp.Function("rho_b")(tt, x), sp.Function("rho_d")(tt, x)
    lam_ = sp.symbols("lambda", positive=True)
    Lt = (-(2 - acs) * (Pt.diff(x) - ct.diff(x)) ** 2 + 2 * lam_ * ct.diff(tt) ** 2) / (16 * sp.pi * Gs) - rbt * Pt - rdt * (Pt - be * ct)
    eT = [e.lhs for e in euler_equations(Lt, [Pt, ct], [tt, x])]
    Pxx = sp.solve(eT[0], Pt.diff(x, 2))[0]
    chi_eq = sp.simplify(eT[1].subs(Pt.diff(x, 2), Pxx))
    lin_ok = sp.simplify(chi_eq * 4 * sp.pi * Gs + lam_ * ct.diff(tt, 2) + 4 * sp.pi * Gs * (rbt + (1 - be) * rdt)) == 0
    eng = LIN(np.array([1.0]), 1.0, 1e6)                                  # the engine's own coefficients, read back
    Yp = np.array([0, 0, 0, 0, 1.0, 0]); r_ = eng.rhs(0.0, Yp); qq = (c * eng.kph1[0] / (H0 * Ez(1.0))) ** 2
    Yd = np.array([0, 0, 1.0, 0, 0, 0]); r2 = eng.rhs(0.0, Yd); Oma1 = 1.5 * Om / Ez(1.0) ** 2
    eng_ok = abs(r_[1] / -qq - 1) < 1e-12 and abs(r_[3]) < 1e-30 and abs(r2[5]) < 1e-30 and abs(r2[1] / (Oma1 * (1 - FB)) - 1) < 1e-12
    P(f"    g~_00 = -N^2 e^-2chi [{g_ok}]; NR lapse of g~: (1 + Phi) e^-chi -> 1 + Phi - chi [{nr_ok}]; with inertia: "
      f"lambda chi_tt = -4 pi G (rho_b + (1 - beta) rho_d) [{lin_ok}]")
    check("A4 DERIVED: coupling FK1 to g~ = g + (1 - e^-2chi) n n (the root's own Einstein-frame metric: lapse N e^-chi) is beta = 1 -- "
          "the dark component neither sources nor feels chi, with NO new field and NO new constant (beta = 0, 1 are the only "
          "values that are metrics of the root's own; any other beta is a new constant); with phi's inertia the linear system is "
          "lambda chi_tt = -4 pi G (rho_b + (1 - beta) rho_d) delta, the baryons feel -(k/a)^2 chi and the dark -(1 - beta)(k/a)^2 chi; "
          "the engine below implements exactly these coefficients",
          f"g~_00 {g_ok}; NR coupling -rho_d (Phi - chi) {nr_ok}; linear scalar equation {lin_ok}; engine coefficients (beta = 1: "
          f"dark feels no chi, dark does not source chi, baryons feel -q^2 chi) {eng_ok}", g_ok and nr_ok and lin_ok and eng_ok)

    banner("A5  WHAT READING (b) COSTS (and what reading (a) costs)")
    l3j = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L353_kernel_invisible_dark_component_results.json")))
    wep = l3j["numbers"]["N4"]["median_wep"]
    bs2 = json.load(open(os.path.join(REPO, "real_research", "switch_audit_2026", "BS2_efe_vs_switch_results.json")))["checks"]
    e9 = next(v["measured"] for k, v in bs2.items() if k.startswith("E9 ")); e10 = next(v["measured"] for k, v in bs2.items() if k.startswith("E10 "))
    rho_dm_loc = 0.01 * 1.98847e30 / (3.0857e16) ** 3                   # 0.01 Msun/pc^3 (a standard-halo local density; an upper bound here)
    g_ss = 4 * math.pi / 3 * G * rho_dm_loc * 1.496e11                    # a uniform dark sphere's pull at 1 AU
    P(f"    (b): dark-baryon WEP violation where the phantom is on (L353 N4b, X-COP at R500): median {wep:.2f} of the gas's "
      f"acceleration missing from the dark component; Solar System: any dark density acts at <= {g_ss:.1e} m/s^2 at 1 AU in either "
      f"reading (the baryonic metric g is unchanged); GW170817: the tensor sector and the photon metric are untouched")
    P(f"    (a): the literal action -- FP10/FP16's dark orbits (Newtonian) are not its dynamics, and the web's dark field enters the "
      f"kernel as an external field: BS2 (C-H/K + switch, no band-pass) scored that on KiDS at d chi^2 {e9} with the all-matter "
      f"kernel and {e10} with a baryons-only kernel (all 60 points; read-only)")
    OUT["numbers"]["A5"] = dict(xcop_wep_median=wep, g_solar_system=g_ss, bs2_E9_all_matter=e9, bs2_E10_baryons_only=e10)
    check("A5 CONSTRAINT (costs of (b)): a second matter metric (non-universal coupling) -- the dark-baryon equivalence principle is "
          "violated wherever chi != 0 (L353's X-COP median at R500 read-only); the Solar System cannot tell (a) from (b) (a dark pull "
          "<= 1e-19 m/s^2 at 1 AU, far below any ephemeris bound) and GW170817 is untouched (c_T and the photon metric unchanged)",
          f"X-COP median WEP violation {wep:.2f}; Solar-System dark pull {g_ss:.1e} m/s^2; new constants 0; new fields 0",
          0.2 < wep < 0.8 and g_ss < 1e-15)

# ================================================================================================= PART B
if want("B"):
    banner("B0  CONTROLS: the two-fluid engine reproduces FP7 B5 (one fluid, all matter), FP9's H_Y and FP13's H_S committed sigma_8")
    B5c = json.load(open(os.path.join(HERE, "FP7_aqual_type_repair_results.json")))["numbers"]["B5"]
    lin_c = {le: s8(LIN(KH, 0.0, le).run(DI_EH), idx=slice(None)) / S8_LCDM for le in (1e7, 3e7, 1e8, 1e9)}
    dev_lin = max(abs(lin_c[le] / B5c["linear"][f"{le:.4g}"] - 1) for le in lin_c)
    LAM7 = B5c["lambda_eff_lambda0"]                                      # FP7's lambda_eff at lambda = 0 (its c_2 floor): 277.39
    key7 = lambda le: "277.4" if abs(le - LAM7) < 1e-6 else f"{le:.4g}"
    big = {le: math.log10(s8(LIN(KH, 0.0, le).run(DI_EH), idx=slice(None)) / S8_LCDM) for le in (LAM7, 1e4, 1e6)}
    dev_big = max(abs(big[le] / math.log10(B5c["linear"][key7(le)]) - 1) for le in big)
    ph_c, dev_ph = {}, 0.0
    for f in FOOTS:
        for mode, yd in (("rms", "rms341"), ("permode", "permode")):
            for le in (LAM7, 1e5, 1e7, 1e8):
                v_ = s8(TF(KH, 0.0, yd, SEP_NONE, A0[f], lam=le - LAM0, lamc=LAM0).run(DI_EH), idx=slice(None)) / S8_LCDM
                ph_c[f"{f}/{mode}/{key7(le)}"] = v_
                dev_ph = max(dev_ph, abs(v_ / B5c["phys"][f"{f}/{mode}"][key7(le)] - 1))
    F9n = json.load(open(os.path.join(HERE, "FP9_web_galaxy_separator_results.json")))["numbers"]["H2"]["s8"]
    F13n = json.load(open(os.path.join(HERE, "FP13_separator_from_state_results.json")))["numbers"]["H3"]["s8"]
    dev9 = dev13 = 0.0
    for f in FOOTS:
        for mode, yd in (("rms", "rms341"), ("permode", "permode")):
            v9 = s8(TF(KH, 0.0, yd, SEP_HY, A0[f], lamc=LAM0).run(DI_EH), idx=slice(None)) / S8_LCDM
            dev9 = max(dev9, abs((v9 - 1) / (F9n[str((f, mode))] - 1) - 1))
    # FP13 (H_S) and FP19 (H_K1): their committed linear P boosts (per-mode, canonical, z = 0 and 0.25 / z = 0)
    F13p = json.load(open(os.path.join(HERE, "FP13_separator_from_state_results.json")))["numbers"]["H4"]["Pboost"]
    F19p = json.load(open(os.path.join(HERE, "FP19_hs_repair_results.json")))["numbers"]["H5"]["Pboost"]
    lc0 = TF(KH, 0.0, "lcdm").run(DI_EH, (0.25,))
    r13 = TF(KH, 0.0, "permode", SEP_HS["canonical"], A0["canonical"], lamc=LAM0).run(DI_EH, (0.25,))
    r19 = TF(KH, 0.0, "permode", SEP_HK1["canonical"], A0["canonical"], lamc=LAM0).run(DI_EH, (0.25,))
    pbo = lambda r, zl, q: float(np.interp(q, KH, (r[zl]["dm"] / lc0[zl]["dm"]) ** 2)) - 1.0
    dev13 = max(abs(pbo(r13, zl, q) - F13p[str(zl)][str(q)]) / max(abs(F13p[str(zl)][str(q)]), 1e-3) for zl in (0.0, 0.25) for q in (0.1, 0.3, 0.5, 1.0))
    dev19 = max(abs(pbo(r19, 0.0, q) - F19p[str(q)]) / max(abs(F19p[str(q)]), 1e-3) for q in (0.1, 0.3, 0.5, 1.0))
    r_a = TF(KX, 0.0, "real", SEP_NONE, A0["canonical"]).run(DX)
    one_fluid = float(np.max(np.abs(r_a[0.0]["db"] / r_a[0.0]["dd"] - 1)))
    xp_ok = float(np.max(np.abs(XL(np.logspace(-6, 3, 50)) - ns9["x_P2"](np.logspace(-6, 3, 50)))))
    P(f"    FP7 linear (lambda_eff 1e7-1e9): max dev {dev_lin:.1e}; astronomical rows (log10 at 277/1e4/1e6): {big} vs FP7 "
      f"{[round(math.log10(B5c['linear'][key7(le)]), 3) for le in big]}; FP7 physical-amplitude (16 rows): max dev {dev_ph:.1e}")
    P(f"    FP9 H_Y (H2) max dev on the boost {dev9:.1e}; FP13 H_S (H4 P boost) {dev13:.1e}; FP19 H_K1 (H5 P boost) {dev19:.1e}; two-fluid beta = 0 is one fluid: max |db/dd - 1| "
      f"{one_fluid:.1e}; the hub's X_p2 = FP9's x_P2 to {xp_ok:.1e}; LCDM with pressure / without: {S8L[1.0] / S8L[0.0]:.5f}")
    OUT["numbers"]["B0"] = dict(dev_lin=dev_lin, big_log10=big, dev_phys=dev_ph, dev_fp9=dev9, dev_fp13=dev13, dev_fp19=dev19, one_fluid=one_fluid)
    check("B0 CONTROLS: the two-fluid engine at beta = 0 reproduces FP7 B5's committed linear sigma_8 (lambda_eff 1e7-1e9, <= 1e-3; the "
          "astronomical rows in log10 to 2%) and all 16 physical-amplitude rows (<= 1e-2), FP9's committed H_Y sigma_8 boost, FP13's H_S and "
          "FP19's H_K1 committed linear P boosts (<= 2%; at the committed c_2 floor); at beta = 0 without pressure the two fluids move as one; "
          "LCDM with the gas's pressure moves sigma_8 by < 1e-3",
          f"linear {dev_lin:.1e}, log rows {dev_big:.1e}, physical {dev_ph:.1e}, FP9 {dev9:.1e}, FP13 {dev13:.1e}, FP19 {dev19:.1e}, "
          f"one-fluid {one_fluid:.1e}, pressure {abs(S8L[1.0] / S8L[0.0] - 1):.1e}",
          dev_lin < 1e-3 and dev_big < 0.02 and dev_ph < 1e-2 and dev9 < 0.02 and dev13 < 0.02 and dev19 < 0.02 and one_fluid < 1e-9
          and abs(S8L[1.0] / S8L[0.0] - 1) < 1e-3 and xp_ok < 1e-12)

    banner("B1  THE ZERO-FIELD RUNAWAY WITH GAS PRESSURE: a growing root at every k; pressure only saturates the rate")
    s_, K_, cs_, cc_, Gr_, lm_ = sp.symbols("s K c_s c Gamma_b lambda")
    disp = s_ ** 2 + cs_ ** 2 * K_ ** 2 * s_ - K_ ** 2 * cc_ ** 2 * Gr_ / lm_       # s = Gamma^2; baryons + phi, gravity terms dropped
    roots = sp.solve(disp, s_)
    prod = sp.simplify(roots[0] * roots[1])
    pos = {K_: 1, cs_: 1, cc_: 1, Gr_: 1, lm_: 1}
    splus = [r for r in roots if float(r.subs(pos)) > 0][0]
    lim = sp.simplify(sp.limit(splus.subs({cs_: sp.Symbol("c_s", positive=True), cc_: sp.Symbol("c", positive=True),
                                           Gr_: sp.Symbol("Gamma_b", positive=True), lm_: sp.Symbol("lambda", positive=True)}),
                               K_, sp.oo))
    lim_ok = sp.simplify(lim - sp.Symbol("c", positive=True) ** 2 * sp.Symbol("Gamma_b", positive=True)
                         / (sp.Symbol("lambda", positive=True) * sp.Symbol("c_s", positive=True) ** 2)) == 0
    prod_ok = sp.simplify(prod + K_ ** 2 * cc_ ** 2 * Gr_ / lm_) == 0
    rows, all_grow = [], True
    for le in (LAMC, LAM0):
        for z_ in (0.0, 2.0, 3.0):
            a_ = 1 / (1 + z_); Hs = H0 * Ez(a_); rho_b = FB * Om * M6["rho_crit0"] / a_ ** 3; Gb = 4 * math.pi * G * rho_b
            rho_d = (1 - FB) / FB * rho_b; cs = math.sqrt(cs2_gas(a_))
            for kh in (0.1, 1.0, 10.0, 100.0):
                Kp = kh * h_ / (a_ * Mpc)
                Mx = np.array([[Gb - cs ** 2 * Kp ** 2, 4 * math.pi * G * rho_d, -Kp ** 2 * c ** 2], [Gb, 4 * math.pi * G * rho_d, 0.0],
                               [-Gb / le, 0.0, 0.0]])                        # full 3x3 (baryons, dark, phi): d^2/dt^2 v = M v
                gmax = max(np.linalg.eigvals(Mx).real)
                all_grow = all_grow and gmax > 0
                rows.append((le, z_, kh, math.sqrt(max(gmax, 0)) / Hs))
            rows.append((le, z_, "inf", c * math.sqrt(Gb / le) / cs / Hs))
    P(f"    s = Gamma^2 roots: product {prod} (< 0: one growing root at every K); large-K limit {lim}")
    for le in (LAMC, LAM0):
        P(f"    Gamma/H (full 3x3 with gravity, lambda_eff = {le:.0f}, measured T0): " + "; ".join(
            f"z {r[1]:g} k {r[2]}: {r[3]:.1f}" for r in rows if r[0] == le))
    OUT["numbers"]["B1"] = [list(map(str, r_)) for r_ in rows]
    check("B1 DERIVED: with the gas's own pressure the zero-field runaway SURVIVES in the baryons -- the baryon-phi block has roots "
          "s = Gamma^2 with product -K^2 c^2 4 pi G rho_b/lambda < 0 (a growing mode at every k, any temperature), whose rate saturates "
          "at Gamma_inf = (c/c_s) sqrt(4 pi G rho_b/lambda_eff) instead of vanishing; the full 3x3 (baryons, dark, phi, gravity kept) "
          "has a growing mode at every sampled (z, k); at lambda = 0 (lambda_eff = 3, FP14; 277 at the committed c_2 floor) and the "
          "measured T0 the rate at k = 1 h/Mpc is several H and the pressure cap hundreds to thousands of H",
          "; ".join(f"lambda_eff {r[0]:.0f} z {r[1]:g} k {r[2]}: {r[3]:.1f} H" for r in rows if r[2] in (1.0, "inf")),
          prod_ok and lim_ok and all_grow and min(r[3] for r in rows if r[2] == "inf") > 10)

    banner("B2  THE DERIVED LINEAR SYSTEM (no separator): sigma_8 vs lambda_eff in both readings, gas at the measured T0 (k <= 20 h/Mpc)")

    def s8lin(beta, le, T=1.0):
        with np.errstate(all="ignore"):
            r_ = LIN(KH, beta, le, Tfac=T).run(DI)
        v_ = s8(r_, idx=slice(None)) / S8LKH[T] if 0.0 in r_ else float("inf")
        return v_ if np.isfinite(v_) else float("inf")
    LES = (LAMC, LAM7, 1e4, 1e6, 1e7, 3e7, 1e8, 1e9)
    lin_tab = {(rd_, le): s8lin(be_, le) for rd_, be_ in (("a", 0.0), ("b", BETA_B)) for le in LES}
    th = {"a": thresh(lambda le: s8lin(0.0, le), lo=LAMC), "b": thresh(lambda le: s8lin(BETA_B, le), lo=LAMC),
          "b_noP": thresh(lambda le: s8lin(BETA_B, le, 0.0), lo=LAMC), "b_T2": thresh(lambda le: s8lin(BETA_B, le, 2.0), lo=LAMC)}
    P("    sigma_8/LCDM:  " + ";  ".join(f"({k_[0]}) {k_[1]:.3g}: {v_:.4g}" for k_, v_ in lin_tab.items()))
    P(f"    sigma_8 <= 1.02 needs lambda_eff >= {th['a']:.2e} (a), {th['b']:.2e} (b), {th['b_noP']:.2e} (b, no pressure), "
      f"{th['b_T2']:.2e} (b, T0 x 2)")
    OUT["numbers"]["B2"] = dict(table={f"{k_[0]}/{k_[1]:.4g}": v_ for k_, v_ in lin_tab.items()}, thresholds=th)
    check("B2 DERIVED: the no-separator linear system in reading (b) STILL runs away at lambda = 0 (sigma_8 astronomically above the "
          "gate at lambda_eff = 3 and 277) but needs a smaller inertia than (a) to pass; the gas's pressure barely moves the threshold -- "
          "inertia (a knob; FP14 eliminated it under H_Y) is the only no-separator escape in either reading",
          f"(b) at lambda_eff = 3/277: {lin_tab[('b', LAMC)]:.3g}/{lin_tab[('b', LAM7)]:.3g}; thresholds (a) {th['a']:.2e}, (b) {th['b']:.2e}, "
          f"(b) no pressure {th['b_noP']:.2e}, (b) T0 x 2 {th['b_T2']:.2e}",
          lin_tab[("b", LAMC)] > 1e3 and lin_tab[("b", LAM7)] > 1e3 and th["b"] < 0.5 * th["a"] and abs(math.log10(th["b_T2"] / th["b"])) < 0.3)

    banner("B3  WHERE THE BARYONS DRAG THE TOTAL MATTER OVER THE GATE (lambda = 0, reading (b))")
    ZD = tuple(sorted(set(np.round(np.logspace(math.log10(1001), 0, 60) - 1, 4)) - {1000.0}))
    with np.errstate(all="ignore"):
        rl = LIN(KH, BETA_B, LAMC, Tfac=1.0).run(DI, ZD)
    rr = TF(KH, 0.0, "lcdm", Tfac=1.0).run(DI, ZD)
    cross = None
    for z_ in sorted(rl, reverse=True):
        rat = np.abs(rl[z_]["dm"]) / np.abs(rr[z_]["dm"])
        if np.max(rat) > SIG_GATE:
            j_ = int(np.argmax(rat > SIG_GATE))
            cross = (z_, float(KH[j_]), float(np.abs(rl[z_]["db"][j_]) / np.abs(rl[z_]["dd"][j_])))
            break
    cross = cross or (float("nan"), float("nan"), float("nan"))
    s8cross = next((z_ for z_ in sorted(rl, reverse=True) if s8(rl, z=z_, idx=slice(None)) / s8(rr, z=z_, idx=slice(None)) > SIG_GATE), None)
    rph = TF(KH, BETA_B, "permode", SEP_NONE, A0["canonical"], Tfac=1.0).run(DI, ZD)
    s8cross_ph = next((z_ for z_ in sorted(rph, reverse=True) if s8(rph, z=z_, idx=slice(None)) / s8(rr, z=z_, idx=slice(None)) > SIG_GATE), None)
    P(f"    linear system (lambda_eff = 3): the first mode over 1.02 in total matter at z = {cross[0]:.1f}, k = {cross[1]:.3g} h/Mpc "
      f"(baryon/dark there {cross[2]:.3g}); the sigma_8 window crosses 1.02 at z = {s8cross}; per-mode physical amplitude: at z = {s8cross_ph}")
    OUT["numbers"]["B3"] = dict(first_mode=cross, s8_cross_lin=s8cross, s8_cross_permode=s8cross_ph)
    check("B3 DERIVED: at lambda = 0 in reading (b) the baryons' runaway drags the TOTAL matter over the 1.02 gate at once -- at the "
          "first output (z ~ 890) every mode above the printed k is already over it on the linear system (lambda_eff = 3), and on the "
          "per-mode physical amplitude the sigma_8 window crosses at z ~ 120", f"first mode z {cross[0]:.1f} at k {cross[1]:.3g} h/Mpc; sigma_8 window z {s8cross} (linear), "
          f"{s8cross_ph} (per-mode)", cross[0] > 2 and s8cross is not None and s8cross_ph is not None)

    banner("B4  THE PHYSICAL-AMPLITUDE YARDSTICKS (FP7's per-mode and rms, two fluids), no separator, both footings")
    LEP = (LAMC, LAM7, 1e5, 1e7, 1e8)
    ph_tab = {}
    for f in FOOTS:
        for mode, yd in (("rms", "rms341"), ("permode", "permode")):
            for le in LEP:
                for rd_, be_ in (("a", 0.0), ("b", BETA_B)):
                    ph_tab[(f, mode, rd_, le)] = s8(TF(KH, be_, yd, SEP_NONE, A0[f], lam=le - LAMC, Tfac=1.0).run(DI), idx=slice(None)) / S8LKH[1.0]
    thp = {(f, m_): thresh(lambda le, f=f, m_=m_: s8(TF(KH, BETA_B, "permode" if m_ == "permode" else "rms341", SEP_NONE, A0[f],
                                                         lam=le - LAMC, Tfac=1.0).run(DI), idx=slice(None)) / S8LKH[1.0], lo=LAMC, n=18)
           for f in FOOTS for m_ in ("rms", "permode")}
    for f in FOOTS:
        for mode in ("rms", "permode"):
            P(f"    {f:9s} {mode:7s}: " + ";  ".join(f"{le:.3g}: (a) {ph_tab[(f, mode, 'a', le)]:.3f} (b) {ph_tab[(f, mode, 'b', le)]:.3f}"
                                                  for le in LEP) + f";  (b) passes 1.02 at lambda_eff >= {thp[(f, mode)]:.2e}")
    OUT["numbers"]["B4"] = dict(table={f"{k_[0]}/{k_[1]}/{k_[2]}/{k_[3]:.4g}": v_ for k_, v_ in ph_tab.items()},
                                thresholds={f"{k_[0]}/{k_[1]}": v_ for k_, v_ in thp.items()})
    b4_fail = min(ph_tab[(f, m_, "b", le)] for f in FOOTS for m_ in ("rms", "permode") for le in (LAMC, LAM7))
    b4_ratio = max((ph_tab[(f, m_, "b", le)] - 1) / (ph_tab[(f, m_, "a", le)] - 1) for f in FOOTS for m_ in ("rms", "permode") for le in (LAMC, LAM7))
    check("B4 DERIVED: on FP7's physical-amplitude yardsticks the no-separator reading (b) FAILS the sigma_8 gate at lambda = 0 on every "
          "yardstick and footing (lambda_eff = 3 and 277) -- far smaller than (a)'s ~17-26x but far above 1.02 (the baryons reach MOND "
          "equilibrium in their own, deeper field and pull the dark after them)", f"(b) at lambda = 0: min {b4_fail:.3f} over (footing, "
          f"yardstick, lambda_eff); max boost ratio (b)/(a) {b4_ratio:.3f}; (b) thresholds " + ", ".join(f"{k_[0]}/{k_[1]} {v_:.1e}" for k_, v_ in thp.items()),
          b4_fail > 1.1 and b4_ratio < 0.3)

    banner("B5  THE REAL-SPACE OPERATOR (the hub's hy_phantom, read-only) and its Stein yardstick, no separator")
    mG = C.Mesh(96.0, 128)
    rng = np.random.default_rng(20260927)
    white = mG.rfft(rng.normal(size=(128, 128, 128)))
    n2u, inv = np.unique(mG.n2, return_inverse=True)
    Pu = np.array([M6["PN"] * M6["P_un"](max(mG.kf * math.sqrt(float(q)), mG.kf)) for q in n2u]); Pu[n2u == 0] = 0.0
    amp0 = white * np.sqrt(Pu[inv].reshape(mG.n2.shape) * 128 ** 3 / 96.0 ** 3); del white
    cosC = C.Cosmo("fp6"); sepn = C.HY(cosC, **HEAD, yield_on=False, bandpass_on=False); sepy = C.HY(cosC, **HEAD)
    gauss = {}
    for zG in (1.0, 0.25):
        aG = 1 / (1 + zG); dG = mG.irfft(amp0 * cosC.D(aG))
        for lab, sp_ in (("none", sepn), ("H_Y", sepy)):
            for rd_, w_ in (("a", 1.0), ("b", FB)):
                _, _, dg = C.hy_phantom(mG, sp_, cosC, w_ * dG, aG, cosC.a0_code("canonical"))
                cst = cbar_maxwell(dg["y_rms"] / math.sqrt(3.0), dg["y_th"])
                gauss[(zG, lab, rd_)] = (dg["cbar"], cst, dg["y_rms"])
    del amp0
    dev_g = max(abs(v_[0] / v_[1] - 1) for v_ in gauss.values())
    P("    Gaussian 96 Mpc/h 128^3 (EH98): " + "; ".join(f"z {k_[0]} {k_[1]} ({k_[2]}): cbar {v_[0]:.4f} vs Stein {v_[1]:.4f} (y_rms {v_[2]:.2e})"
                                                  for k_, v_ in gauss.items()))
    re_tab = {}
    for f in FOOTS:
        for rd_, be_ in (("a", 0.0), ("b", BETA_B)):
            for le in LEP:
                re_tab[(f, rd_, le)] = s8(TF(KX, be_, "real", SEP_NONE, A0[f], lam=le - LAMC, Tfac=1.0).run(DX)) / S8L[1.0]
            re_tab[(f, rd_, "qs")] = s8(TF(KX, be_, "real", SEP_NONE, A0[f], Tfac=1.0, track=False).run(DX)) / S8L[1.0]
    for f in FOOTS:
        P(f"    real-space {f:9s}: " + ";  ".join(f"{le if isinstance(le, str) else format(le, '.3g')}: (a) {re_tab[(f, 'a', le)]:.3f} "
                                                   f"(b) {re_tab[(f, 'b', le)]:.3f}" for le in LEP + ("qs",)))
    OUT["numbers"]["B5"] = dict(gauss={f"{k_[0]}/{k_[1]}/{k_[2]}": v_ for k_, v_ in gauss.items()},
                                table={f"{k_[0]}/{k_[1]}/{k_[2]}": v_ for k_, v_ in re_tab.items()})
    check("B5 the hub's real-space operator on Gaussian fields (all-matter and baryon-only sources, no separator and H_Y, z = 1 and "
          "0.25) has the Maxwell/Stein coherent coefficient at its own variance to 2% -- so the Stein yardstick is the operator's linear "
          "response; on it the no-separator reading (b) FAILS sigma_8 at lambda = 0 in both footings (tracking or quasi-static)",
          f"operator vs Stein max dev {dev_g:.1e}; (b) lambda = 0: canonical {re_tab[('canonical', 'b', LAMC)]:.3f}, alt "
          f"{re_tab[('alt', 'b', LAMC)]:.3f} (quasi-static {re_tab[('canonical', 'b', 'qs')]:.3f}/{re_tab[('alt', 'b', 'qs')]:.3f}); "
          f"(a) {re_tab[('canonical', 'a', LAMC)]:.3f}/{re_tab[('alt', 'a', LAMC)]:.3f}",
          dev_g < 0.02 and min(re_tab[(f, "b", le)] for f in FOOTS for le in (LAMC, "qs")) > SIG_GATE)
    P(f"  {el()}")

# ================================================================================================= PART C
if want("C"):
    banner("C0  BOTH WAYS: the committed per-mode numbers on the committed T_EH98 spectrum, and on CLASS (all matter, one fluid, c_2 floor)")
    F9h = json.load(open(os.path.join(HERE, "FP9_web_galaxy_separator_results.json")))["numbers"]["H2"]
    F13h = json.load(open(os.path.join(HERE, "FP13_separator_from_state_results.json")))["numbers"]["H1"]
    F19h = json.load(open(os.path.join(HERE, "FP19_hs_repair_results.json")))["numbers"]["H1"]
    F7h = json.load(open(os.path.join(HERE, "FP7_aqual_type_repair_results.json")))["numbers"]["B5"]
    REF_EH = TF(KX, 0.0, "lcdm").run(DX_EH, ZS); REF_C0 = REF[0.0]
    kc = "('canonical', 'permode')"
    both = {}
    for lab, sep_, s8c, frc, lam_ in (("FP7 B5 (no separator, lambda_eff 277)", SEP_NONE, F7h["phys"]["canonical/permode"]["277.4"], None,
                                       F7h["lambda_eff_lambda0"] - LAM0),
                                      ("FP9 H_Y", SEP_HY, F9h["s8"][kc], F9h["forest"]["('canonical', 'permode', 15.0)"], 0.0),
                                      ("FP13 H_S", SEP_HS["canonical"], F13h["s8"][kc], F13h["forest"][kc], 0.0),
                                      ("FP19 H_K1", SEP_HK1["canonical"], F19h["s8"][kc], F19h["forest"][kc], 0.0)):
        rE = TF(KX, 0.0, "permode", sep_, A0["canonical"], lam=lam_, lamc=LAM0).run(DX_EH, ZS)
        rC = TF(KX, 0.0, "permode", sep_, A0["canonical"], lam=lam_, lamc=LAM0).run(DX, ZS)
        both[lab] = dict(committed_s8=s8c, eh_s8=s8(rE) / s8(REF_EH), class_s8=s8(rC) / s8(REF_C0), committed_forest=frc,
                         eh_forest=forest(rE, REF_EH), class_forest=forest(rC, REF_C0))
        P(f"    {lab:38s}: sigma_8 committed {s8c:.4f} | T_EH98 here {both[lab]['eh_s8']:.4f} | CLASS {both[lab]['class_s8']:.4f};  forest "
          f"committed {frc if frc is None else format(frc, '.2g')} | T_EH98 {both[lab]['eh_forest']:.2g} | CLASS {both[lab]['class_forest']:.2g}")
    OUT["numbers"]["C0"] = both
    check("C0 (reported) BOTH WAYS: the committed per-mode sigma_8 and forest (FP7 B5, FP9, FP13, FP19; all matter, canonical) on the "
          "committed T_EH98 spectrum (reproduced here) and on CLASS -- every number below this line uses CLASS",
          "; ".join(f"{k_}: s8 {v_['eh_s8']:.4f} -> {v_['class_s8']:.4f}" for k_, v_ in both.items()), True, load_bearing=False)

    banner("C1  THE SEPARATOR x READING x YARDSTICK x FOOTING: sigma_8 (matter; lensing reported), the forest (gas), CMB lensing")
    SEPS = [("none", lambda f: SEP_NONE), ("H_Y", lambda f: SEP_HY), ("H_S", lambda f: SEP_HS[f]), ("H_K1", lambda f: SEP_HK1[f]),
            ("bp-only", lambda f: SEP_BP), ("yield-only", lambda f: SEP_YD)]
    tab, runs = {}, {}
    for sname, sf in SEPS:
        for f in FOOTS:
            for yd in ("permode", "real"):
                for rd_, be_ in (("a", 0.0), ("b", BETA_B)):
                    r_ = TF(KX, be_, yd, sf(f), A0[f], Tfac=1.0).run(DX, ZS)
                    runs[(sname, f, yd, rd_)] = r_
                    tab[(sname, f, yd, rd_)] = dict(s8=s8(r_) / S8L[1.0], s8L=s8(r_, key="dL") / S8L[1.0], forest=forest(r_, REF[1.0]),
                                                    y25=r_[0.25]["y"], y2=r_[2.0]["y"], y3=r_[3.0]["y"])
        P(f"    {sname:10s} " + " | ".join(f"{f[:3]} {yd[:4]} (a) s8 {tab[(sname, f, yd, 'a')]['s8']:.4f} F {tab[(sname, f, yd, 'a')]['forest']:.3f}"
                                           f"  (b) s8 {tab[(sname, f, yd, 'b')]['s8']:.4f} F {tab[(sname, f, yd, 'b')]['forest']:.3f}"
                                           for f in FOOTS for yd in ("permode", "real")) + f"   {el()}")
    OUT["numbers"]["C1"] = {"/".join(k_): v_ for k_, v_ in tab.items()}
    hy_ok = all(tab[("H_Y", f, yd, "b")]["s8"] <= SIG_GATE and tab[("H_Y", f, yd, "b")]["forest"] <= FOREST_TOL for f in FOOTS
                for yd in ("permode", "real"))
    red = max((tab[("H_Y", f, yd, "b")]["s8"] - 1) / (tab[("H_Y", f, yd, "a")]["s8"] - 1) for f in FOOTS for yd in ("permode", "real"))
    check("C1 DERIVED: with H_Y, reading (b) passes sigma_8 and the forest proxy on both yardsticks and both footings, and its "
          "total-matter sigma_8 boost is a small fraction of (a)'s (the hub's ~f_b^2 estimate, now on the growth)",
          f"(b) H_Y: sigma_8 " + ", ".join(f"{f[:3]}/{yd[:4]} {tab[('H_Y', f, yd, 'b')]['s8']:.4f}" for f in FOOTS for yd in ("permode", "real"))
          + f"; forest max {max(tab[('H_Y', f, yd, 'b')]['forest'] for f in FOOTS for yd in ('permode', 'real')):.3f}; boost (b)/(a) <= {red:.3f}",
          hy_ok and red < 0.3)

    banner("C2  IS A SEPARATOR NEEDED FOR sigma_8?  And which half of H_Y does the work in each reading")
    need = {rd_: all(tab[("none", f, yd, rd_)]["s8"] > SIG_GATE for f in FOOTS for yd in ("permode", "real")) for rd_ in ("a", "b")}
    halves = {(s_, rd_): all(tab[(s_, f, yd, rd_)]["s8"] <= SIG_GATE for f in FOOTS for yd in ("permode", "real"))
              for s_ in ("bp-only", "yield-only") for rd_ in ("a", "b")}
    halves_F = {(s_, rd_): all(tab[(s_, f, yd, rd_)]["forest"] <= FOREST_TOL for f in FOOTS for yd in ("permode", "real"))
                for s_ in ("bp-only", "yield-only") for rd_ in ("a", "b")}
    P(f"    none fails sigma_8 everywhere: (a) {need['a']}, (b) {need['b']};  sigma_8 passes with the band-pass alone: (a) "
      f"{halves[('bp-only', 'a')]}, (b) {halves[('bp-only', 'b')]}; with the yield alone: (a) {halves[('yield-only', 'a')]}, (b) "
      f"{halves[('yield-only', 'b')]};  forest passes with the band-pass alone (a) {halves_F[('bp-only', 'a')]} (b) "
      f"{halves_F[('bp-only', 'b')]}; with the yield alone (a) {halves_F[('yield-only', 'a')]} (b) {halves_F[('yield-only', 'b')]}")
    OUT["numbers"]["C2"] = dict(need={k_: v_ for k_, v_ in need.items()}, halves_s8={f"{k_[0]}/{k_[1]}": v_ for k_, v_ in halves.items()},
                                halves_forest={f"{k_[0]}/{k_[1]}": v_ for k_, v_ in halves_F.items()})
    check("C2 DERIVED: a separator IS needed for sigma_8 in BOTH readings (no separator fails on every yardstick and footing at "
          "lambda = 0); reading (b) does not remove it",
          f"none fails: (a) {need['a']}, (b) {need['b']}; min (b) none sigma_8 "
          f"{min(tab[('none', f, yd, 'b')]['s8'] for f in FOOTS for yd in ('permode', 'real')):.3f}", need["a"] and need["b"])

    banner("C3  CAN THE GAS'S OWN PRESSURE (measured T0) DO THE SEPARATOR'S FOREST JOB?  (reading (b), no separator)")
    c3 = {}
    for T in (0.0, 1.0, 2.0, 4.0):
        refT = REF[T]
        for yd in ("permode", "real"):
            r_ = TF(KX, BETA_B, yd, SEP_NONE, A0["canonical"], Tfac=T).run(DX, ZS)
            c3[(T, yd)] = forest(r_, refT)
    P("    forest proxy (b, none, canonical): " + ";  ".join(f"T0 x {k_[0]:g} {k_[1]}: {v_:.3f}" for k_, v_ in c3.items()))
    OUT["numbers"]["C3"] = {f"{k_[0]}/{k_[1]}": v_ for k_, v_ in c3.items()}
    check("C3 DERIVED: the gas's own pressure cannot do the separator's forest job -- reading (b) with no separator fails the forest "
          "proxy at the measured T0 and at 2x and 4x it (pressure acts only above k_J, the MOND boost on the gas is at all scales)",
          ";  ".join(f"T0 x {k_[0]:g} {k_[1]}: {v_:.3f}" for k_, v_ in c3.items()),
          all(v_ > FOREST_TOL for k_, v_ in c3.items() if k_[0] >= 1.0))

    banner("C4  THE DECLARED CONSTANTS, case by case (kappa = 1/2 accepted; lambda = 0 under H_Y)")
    cases = []
    for sname, sf in SEPS:
        for rd_ in ("a", "b"):
            s8ok = all(tab[(sname, f, yd, rd_)]["s8"] <= SIG_GATE for f in FOOTS for yd in ("permode", "real"))
            frok = all(tab[(sname, f, yd, rd_)]["forest"] <= FOREST_TOL for f in FOOTS for yd in ("permode", "real"))
            nconst = sf("canonical").nconst
            cases.append((sname, rd_, nconst, s8ok, frok))
            P(f"    {sname:10s} reading ({rd_}): declared separator constants {nconst}{' (+ ill-posed as written)' if sname == 'H_S' else ''}; "
              f"sigma_8 {'PASS' if s8ok else 'FAIL'}; forest {'PASS' if frok else 'FAIL'}; plus the (b) coupling choice g~ (0 constants)"
              if rd_ == "b" else
              f"    {sname:10s} reading ({rd_}): declared separator constants {nconst}{' (+ ill-posed as written)' if sname == 'H_S' else ''}; "
              f"sigma_8 {'PASS' if s8ok else 'FAIL'}; forest {'PASS' if frok else 'FAIL'}")
    OUT["numbers"]["C4"] = [list(map(str, x_)) for x_ in cases]
    passing = [x_ for x_ in cases if x_[3] and x_[4] and x_[0] != "H_S"]
    minc = {rd_: min([x_[2] for x_ in passing if x_[1] == rd_], default=None) for rd_ in ("a", "b")}
    check("C4 (reported) the knob count: the fewest declared separator constants that pass sigma_8 and the forest on both yardsticks and "
          "footings, per reading (H_S excluded: ill-posed as written)", f"(a) {minc['a']}, (b) {minc['b']}; passing cells "
          + ", ".join(f"{x_[0]}/({x_[1]})" for x_ in passing), True, load_bearing=False)
    OUT["numbers"]["C4_min"] = minc
    P(f"  {el()}")

# ================================================================================================= PART L (CMB lensing)
if want("L"):
    banner("L0  CMB LENSING: Limber on the chain's lensing potential, Planck 2018 (8-400) and ACT DR6; the control against XR26")
    import ast
    from scipy.interpolate import RectBivariateSpline
    from scipy.integrate import cumulative_trapezoid
    if not want("C"):
        raise SystemExit("section L needs section C's runs")
    x26p = os.path.join(XRD, "XR26_cmb.py"); x26jp = os.path.join(XRD, "XR26_cmb_results.json")
    for fn_, p_ in (("XR26_cmb.py", x26p), ("XR26_cmb_results.json", x26jp)):
        OUT["provenance"][fn_] = {"sha256": sha(p_), "path": os.path.relpath(p_, REPO),
                                  "status": "UNCOMMITTED hub file; its Planck band table is PARSED (not executed); its amplitudes read as the control"}
    x26 = open(x26p).read()
    PL18 = ast.literal_eval(x26[x26.index("PL18_MV = {") + len("PL18_MV = "):x26.index("DP_MEAN")].strip())
    AMP_P18 = (1.011, 0.028)           # Planck 2018 VIII eq. 23: MV, 8 <= L <= 400, relative to the Planck 2018 best fit
    AMP_ACT = (1.013, 0.023)           # ACT DR6 lensing alone (Madhavacheril et al. 2024, ApJ 962, 113; Qu et al. 2024, ApJ 962, 112),
                                       # baseline 40 <= L <= 763, relative to the Planck 2018 LCDM best fit
    ACT_BANDS = [b_ for b_ in PL18["8-2048"] if b_[0] >= 40 and b_[1] <= 763]   # proxy weights: Planck's MV errors over ACT's range
    x26n = json.load(open(x26jp))["numbers"]
    X26A = {(f, b_): x26n["L2"]["8-400"]["rows"][f"FP14 c2->oo, lam 0 | {f} | permode || {'lin' if b_ == 'lin' else 'NL'}"]["amp"]
            for f in FOOTS for b_ in ("lin", "NL")}
    X26F = {b_: x26n["L2b"]["f_star"]["lin" if b_ == "lin" else "NL"] for b_ in ("lin", "NL")}
    # Limber: C_L^pp = 4/(L+1/2)^4 Int dchi ((chi* - chi)/chi*)^2 [1.5 Om H0^2 (1+z)]^2 P((L+1/2)/chi, z) [x B(k, z)]
    zt = np.concatenate([np.linspace(0.0, 5.0, 1001), np.geomspace(5.005, 1100.0, 800)])
    chit = np.concatenate([[0.0], cumulative_trapezoid([1 / Ez(1 / (1 + z_)) for z_ in zt], zt)]) * c / (100e3 * h_)   # Mpc
    chis = float(np.interp(1089.9, zt, chit))
    chi5 = float(np.interp(5.0, zt, chit))
    CHI_G = np.concatenate([np.linspace(1.0, chi5, 1500)[:-1], np.linspace(chi5, chis - 1.0, 600)])
    Z_G = np.interp(CHI_G, chit, zt)
    W2 = ((chis - CHI_G) / chis) ** 2 * (1 + Z_G) ** 2
    LG = np.unique(np.concatenate([np.arange(2, 60), np.round(np.geomspace(60, 2100, 140)).astype(int)]))
    LINT = np.arange(2, 2049)
    KKF = KC[::3]                                                           # CLASS's linear and halofit P(k, z), FP6's cosmology
    ZP = np.concatenate([np.linspace(0.0, 3.0, 31), np.linspace(3.5, 10.0, 14), [12.0, 15.0, 20.0, 30.0, 50.0]])
    lnPL = np.log(np.array([[CLS.pk_lin(k * h_, z_) for k in KKF] for z_ in ZP]) * h_ ** 3)
    lnPN = np.log(np.array([[CLS.pk(k * h_, z_) for k in KKF] for z_ in ZP]) * h_ ** 3)
    IPL = RectBivariateSpline(ZP, np.log(KKF), lnPL, kx=1, ky=1); IPN = RectBivariateSpline(ZP, np.log(KKF), lnPN, kx=1, ky=1)

    def Pk(kh, z_, base):
        zz = np.minimum(z_, ZP[-1]); lk = np.log(np.clip(kh, KKF[0], KKF[-1]))
        out = np.exp((IPN if base == "NL" else IPL)(zz, lk, grid=False))
        return np.where(z_ > ZP[-1], out * ((1 + ZP[-1]) / (1 + z_)) ** 2, out)
    ZB = np.array(sorted(ZS))

    def Bspl_of(res, ref, fscale=1.0):
        """B(k, z) = (delta_L/delta_m,LCDM)^2 with delta_L = delta_m + f C_eff src (f = 1: the model; f < 1 scales the phantom only)."""
        Bz = np.array([((res[z_]["dm"] + fscale * (res[z_]["dL"] - res[z_]["dm"])) / ref[z_]["dm"]) ** 2 for z_ in ZB])
        spl = RectBivariateSpline(ZB, np.log(KX), Bz, kx=1, ky=1)
        return lambda kh, z_: np.where(z_ > ZB[-1], 1.0, spl(np.minimum(z_, ZB[-1]), np.log(np.clip(kh, KX[0], KX[-1])), grid=False))

    def limber(base, B=None):
        out = np.empty(len(LG))
        for i_, L_ in enumerate(LG):
            kh = (L_ + 0.5) / CHI_G / h_
            Pv = Pk(kh, Z_G, base)
            if B is not None:
                Pv = Pv * B(kh, Z_G)
            out[i_] = 4.0 / (L_ + 0.5) ** 4 * _trap(W2 * Pv, CHI_G)
        return out
    CL0 = {b_: limber(b_) for b_ in ("lin", "NL")}

    def amp(Rl, base, bands):
        Cl = np.exp(np.interp(np.log(LINT), np.log(LG), np.log(CL0[base]))); R = np.interp(LINT, LG, Rl)
        num = den = 0.0
        for (lo, hi, _A, sA, _f) in bands:
            m_ = (LINT >= lo) & (LINT <= hi); w_ = (LINT[m_] * (LINT[m_] + 1.0)) ** 2 * Cl[m_]
            num += float(np.sum(w_ * R[m_]) / np.sum(w_)) / sA ** 2; den += 1.0 / sA ** 2
        return num / den

    def score(res, ref, fscale=1.0):
        out = {}
        for b_ in ("lin", "NL"):
            Rl = limber(b_, Bspl_of(res, ref, fscale)) / CL0[b_]
            out[b_] = dict(P18=amp(Rl, b_, PL18["8-400"]), ACT=amp(Rl, b_, ACT_BANDS), R100=float(np.interp(100, LG, Rl)),
                           R400=float(np.interp(400, LG, Rl)), R1000=float(np.interp(1000, LG, Rl)))
        return out
    # the control: XR26's headline (H_S as written, all matter, per-mode, FP14's c_2 -> oo, no gas pressure)
    ref0 = TF(KX, 0.0, "lcdm").run(DX_EH, ZS)                           # XR26's B(k, z) was built on the committed T_EH98 spectrum
    ctl = {f: TF(KX, 0.0, "permode", SEP_HS[f], A0[f], Tfac=0.0).run(DX_EH, ZS) for f in FOOTS}
    ctl_s = {f: score(ctl[f], ref0) for f in FOOTS}
    FS = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0]
    AMPS = {b_: [score(ctl["canonical"], ref0, f_)[b_]["P18"] for f_ in FS] for b_ in ("lin", "NL")}
    TGT = AMP_P18[0] + 2 * AMP_P18[1]
    FST = {b_: float(np.interp(TGT, AMPS[b_], FS)) if AMPS[b_][-1] > TGT else 1.0 for b_ in ("lin", "NL")}
    dA = max(abs((ctl_s[f][b_]["P18"] - 1) / (X26A[(f, b_)] - 1) - 1) for f in FOOTS for b_ in ("lin", "NL"))
    dF = max(abs(FST[b_] - X26F[b_]) for b_ in ("lin", "NL"))
    P("    control (H_S, all matter, per-mode): Planck 8-400 amplitude " + ", ".join(
        f"{f[:3]}/{b_}: {ctl_s[f][b_]['P18']:.4f} (XR26 {X26A[(f, b_)]:.4f})" for f in FOOTS for b_ in ("lin", "NL"))
      + f"; the 2-sigma cut f* = {FST['lin']:.3f}/{FST['NL']:.3f} (XR26 {X26F['lin']:.3f}/{X26F['NL']:.3f}); B(k, 0) at k = 0.1/0.3/1/3: "
      + "/".join(f"{float(np.interp(math.log(q), np.log(KX), (ctl['canonical'][0.0]['dL'] / ref0[0.0]['dm']) ** 2)):.3f}" for q in (0.1, 0.3, 1.0, 3.0))
      + " (XR26 " + "/".join(f"{x26n['L1']['B_z0']['FP14 c2->oo, lam 0 | canonical | permode'][str(q)]:.3f}" for q in (0.1, 0.3, 1.0, 3.0))
      + "); R(100/400/1000) lin " + "/".join(f"{ctl_s['canonical']['lin'][r_]:.3f}" for r_ in ("R100", "R400", "R1000"))
      + " (XR26 " + "/".join(f"{x26n['L1']['R']['FP14 c2->oo, lam 0 | canonical | permode || lin'][L_]:.3f}" for L_ in ("100", "400", "1000"))
      + f")   {el()}")
    OUT["numbers"]["L0"] = dict(control={f"{f}/{b_}": ctl_s[f][b_] for f in FOOTS for b_ in ("lin", "NL")}, xr26_amp={f"{k_[0]}/{k_[1]}": v_ for k_, v_ in X26A.items()},
                                amps_f=dict(f=FS, amps=AMPS), f_star=FST, xr26_f_star=X26F, ACT=AMP_ACT, P18=AMP_P18)
    check("L0 CONTROL: this lane's Limber + band-amplitude pipeline (CLASS linear and halofit P(k, z), Planck 2018 VIII's MV bands "
          "parsed from XR26; B(k, z) on the committed T_EH98 spectrum, as XR26 built it) reproduces XR26's headline -- H_S as written, all matter, per-mode, c_2 -> oo -- Planck 8-400 amplitude "
          "(both footings, linear and halofit bases, <= 10% on A - 1) and its 2-sigma phantom cut f* (<= 0.05)",
          f"max |d(A - 1)|/(A - 1) {dA:.3f}; f* {FST['lin']:.3f}/{FST['NL']:.3f} vs XR26 {X26F['lin']:.3f}/{X26F['NL']:.3f}", dA <= 0.10 and dF <= 0.05)

    banner("L1  HOW THE PHANTOM ENTERS PHI + PSI IN READING (b), and how much the reading cuts the lensing (vs the matter)")
    # photons live on g: Phi (lapse) = Phi_N[delta_m] + chi, Psi = Phi (no slip: g~_ij = g_ij and the pressureless dark on g~ adds
    # no anisotropic stress), chi sourced by f_b delta_b in (b)  =>  delta_L = delta_m + C_eff f_b delta_b (units of the mean matter)
    lr = {}
    for sname in ("H_S", "H_K1"):
        for yd in ("permode", "real"):
            ra, rb_ = runs[(sname, "canonical", yd, "a")], runs[(sname, "canonical", yd, "b")]
            for q in (0.5, 1.0):
                j_ = int(np.argmin(np.abs(KX - q)))
                mat = {r_: (runs[(sname, "canonical", yd, r_)][0.0]["dm"][j_] / REF[1.0][0.0]["dm"][j_]) ** 2 - 1 for r_ in ("a", "b")}
                lens = {r_: (runs[(sname, "canonical", yd, r_)][0.0]["dL"][j_] / REF[1.0][0.0]["dm"][j_]) ** 2 - 1 for r_ in ("a", "b")}
                lr[(sname, yd, q)] = dict(matter_ratio=mat["b"] / mat["a"] if mat["a"] > 0 else float("nan"),
                                          lens_ratio=lens["b"] / lens["a"] if lens["a"] > 0 else float("nan"), lens_a=lens["a"], lens_b=lens["b"],
                                          mat_a=mat["a"], mat_b=mat["b"])
    for k_, v_ in lr.items():
        P(f"    {k_[0]:4s} {k_[1]:7s} k {k_[2]}: P boost matter (a) {v_['mat_a']:+.4f} (b) {v_['mat_b']:+.4f} (ratio {v_['matter_ratio']:.3f}); "
          f"lensing (a) {v_['lens_a']:+.4f} (b) {v_['lens_b']:+.4f} (ratio {v_['lens_ratio']:.3f})")
    OUT["numbers"]["L1"] = {f"{k_[0]}/{k_[1]}/{k_[2]}": v_ for k_, v_ in lr.items()}
    fin = [v_ for v_ in lr.values() if np.isfinite(v_["matter_ratio"]) and np.isfinite(v_["lens_ratio"]) and v_["mat_a"] > 1e-3]
    l1_ok = len(fin) > 0 and all(v_["lens_ratio"] > 3 * v_["matter_ratio"] for v_ in fin)
    check("L1 DERIVED: photons live on g, so lensing sees Phi + Psi = 2 (Phi_N[delta_m] + chi) with chi sourced by f_b delta_b in (b) "
          "(no slip: g~_ij = g_ij and the pressureless dark on g~ has no anisotropic stress) -- delta_L = delta_m + C_eff f_b delta_b.  The "
          "baryons-only reading does NOT cut the lensing phantom like the total matter: in the deep regime chi ~ sqrt(a0 f_b g), so the "
          "lensing excess falls only by ~sqrt(f_b)-like factors while the matter boost falls ~f_b^2 (XR21's 20-25x does not carry over)",
          "; ".join(f"{k_[0]}/{k_[1]}/k {k_[2]}: matter x{v_['matter_ratio']:.3f}, lensing x{v_['lens_ratio']:.3f}" for k_, v_ in lr.items()), l1_ok)

    banner("L2  THE GATE: Planck 2018 lensing (8-400) and ACT DR6, the late-time web MOND in both readings, both yardsticks and footings")
    Lres = {}
    for sname in ("H_S", "H_K1", "H_Y", "none"):
        for f in FOOTS:
            for yd in ("permode", "real"):
                for rd_ in ("a", "b"):
                    Lres[(sname, f, yd, rd_)] = score(runs[(sname, f, yd, rd_)], REF[1.0])
        P(f"    {sname:5s}: " + " | ".join(f"{f[:3]} {yd[:4]} ({rd_}) P18 {Lres[(sname, f, yd, rd_)]['lin']['P18']:.3f}/{Lres[(sname, f, yd, rd_)]['NL']['P18']:.3f}"
                                         f" ACT {Lres[(sname, f, yd, rd_)]['lin']['ACT']:.3f}/{Lres[(sname, f, yd, rd_)]['NL']['ACT']:.3f}"
                                         for f in FOOTS for yd in ("permode", "real") for rd_ in ("a", "b")) + f"   {el()}")
    feff = {k_: {b_: float(np.interp(v_[b_]["P18"], AMPS[b_], FS)) if v_[b_]["P18"] <= AMPS[b_][-1] else
                 1.0 + (v_[b_]["P18"] - AMPS[b_][-1]) / (AMPS[b_][-1] - AMPS[b_][-2]) * (FS[-1] - FS[-2]) for b_ in ("lin", "NL")}
            for k_, v_ in Lres.items()}
    pull = {k_: {(b_, d_): (v_[b_][d_] - (AMP_P18 if d_ == "P18" else AMP_ACT)[0]) / (AMP_P18 if d_ == "P18" else AMP_ACT)[1]
                 for b_ in ("lin", "NL") for d_ in ("P18", "ACT")} for k_, v_ in Lres.items()}
    passes = {k_: all(abs(x_) <= 2.0 for x_ in v_.values()) for k_, v_ in pull.items()}
    for sname in ("H_S", "H_K1"):
        for rd_ in ("a", "b"):
            P(f"    {sname} ({rd_}) cut factor f_eff vs the needed f* {FST['lin']:.2f}/{FST['NL']:.2f} (lin/NL): " + "; ".join(
                f"{f[:3]} {yd}: {feff[(sname, f, yd, rd_)]['lin']:.2f}/{feff[(sname, f, yd, rd_)]['NL']:.2f}" for f in FOOTS for yd in ("permode", "real"))
              + "; pulls (sigma) P18 lin/NL, ACT lin/NL: " + "; ".join(
                f"{f[:3]} {yd}: " + "/".join(f"{pull[(sname, f, yd, rd_)][(b_, d_)]:+.1f}" for d_ in ("P18", "ACT") for b_ in ("lin", "NL"))
                for f in FOOTS for yd in ("permode", "real")))
    OUT["numbers"]["L2"] = {"/".join(k_): dict(amp=v_, f_eff=feff[k_], pull={f"{kk[0]}/{kk[1]}": x_ for kk, x_ in pull[k_].items()}, passes=passes[k_])
                            for k_, v_ in Lres.items()}
    surv = {(sname, rd_): [f"{f[:3]}/{yd}" for f in FOOTS for yd in ("permode", "real") if passes[(sname, f, yd, rd_)]]
            for sname in ("H_S", "H_K1", "H_Y", "none") for rd_ in ("a", "b")}
    OUT["numbers"]["L2_survivors"] = {f"{k_[0]}/{k_[1]}": v_ for k_, v_ in surv.items()}
    P("    cells within 2 sigma of BOTH Planck 2018 (8-400) and ACT DR6 on BOTH bases: " + "; ".join(
        f"{k_[0]} ({k_[1]}): {', '.join(v_) if v_ else 'none'}" for k_, v_ in surv.items()))
    SEPL = ("H_S", "H_K1", "H_Y")
    cells = [(sn, f, yd) for sn in SEPL for f in FOOTS for yd in ("permode", "real")]
    a_fail = all(max(pull[(sn, f, yd, "a")].values()) > 2.0 for sn, f, yd in cells)
    b_lin = all(abs(pull[(sn, f, yd, "b")][("lin", d_)]) <= 2.0 for sn, f, yd in cells for d_ in ("P18", "ACT"))
    b_nl_act = all(pull[(sn, f, yd, "b")][("NL", "ACT")] > 2.0 for sn, f, yd in cells)
    fe_b_real = [feff[(sn, f, "real", "b")] for sn in ("H_S", "H_K1") for f in FOOTS]
    fe_a = [feff[(sn, f, yd, "a")] for sn in ("H_S", "H_K1") for f in FOOTS for yd in ("permode", "real")]
    OUT["numbers"]["L2_verdict"] = dict(a_fails_everywhere=a_fail, b_passes_linear_base=b_lin, b_fails_ACT_on_halofit=b_nl_act,
                                        f_eff_b_real=[{k_: round(v_, 3) for k_, v_ in x_.items()} for x_ in fe_b_real],
                                        f_eff_a_range=[min(min(x_.values()) for x_ in fe_a), max(max(x_.values()) for x_ in fe_a)], f_star=FST)
    check("L2 DERIVED (the gate): in the reading the ACTION implies (a) the late-time web MOND is EXCLUDED by CMB lensing for every "
          "separator (H_S as written, H_K1, H_Y), yardstick and footing -- each cell is > 2 sigma off Planck 2018 (8-400) or ACT DR6; in the "
          "kernel-invisible reading (b) every cell passes both on the LINEAR base and fails ACT on the HALOFIT base (Planck's halofit pull "
          "+1.7 to +6.2 sigma): the verdict in (b) hinges on the nonlinear phantom",
          f"(a) all cells fail: {a_fail} (operator cut f_eff {OUT['numbers']['L2_verdict']['f_eff_a_range'][0]:.2f}-"
          f"{OUT['numbers']['L2_verdict']['f_eff_a_range'][1]:.2f} of XR26's per-mode phantom vs the needed f* {FST['lin']:.2f}/{FST['NL']:.2f}); "
          f"(b) linear base passes both: {b_lin}; (b) halofit fails ACT: {b_nl_act}; (b) real-space f_eff (lin/NL) "
          + ", ".join(f"{x_['lin']:.2f}/{x_['NL']:.2f}" for x_ in fe_b_real) + " (H_S can/alt, H_K1 can/alt)",
          a_fail and b_lin and b_nl_act)

# ================================================================================================= PART D
if want("D"):
    banner("D  KiDS (FP18's exact projection, B21's four bins): the lens term, and the web's external field in each reading")
    LGM, MPCm = F18.LGM, M6["MPCm"]; RG = M6["RG"]; rgM = RG / MPCm
    gfr = M6["gfrac_smooth"]
    L025_m = HEAD["L_Lambda"] * OmL_a(0.8) ** (HEAD["n"] / 2) * MPCm
    yth025 = hy_yth(0.8)
    # the external (web) field in the kernel at z = 0.25: rms of the band-passed source field, both readings, from the real runs
    if not want("C"):
        raise SystemExit("section D needs section C's runs")
    gext = {}
    DSEPS = ("none", "H_Y", "H_K1")
    for sname in DSEPS:
        for f in FOOTS:
            for rd_ in ("a", "b"):
                gext[(sname, f, rd_)] = tab[(sname, f, "real", rd_)]["y25"] * A0[f]
    ratio_ext = {(s_, f): gext[(s_, f, "b")] / gext[(s_, f, "a")] for s_ in DSEPS for f in FOOTS}
    P("    external field in the kernel (3D rms, z = 0.25): " + "; ".join(f"{k_[0]} {k_[1][:3]} ({k_[2]}) {v_:.2e} m/s^2" for k_, v_ in gext.items()))
    P("    ratio (b)/(a): " + ", ".join(f"{k_[0]}/{k_[1][:3]} {v_:.3f}" for k_, v_ in ratio_ext.items()) + f"  (f_b = {FB:.3f})")
    bs2c = json.load(open(os.path.join(REPO, "real_research", "switch_audit_2026", "BS2_efe_vs_switch_results.json")))["checks"]
    e12 = next(v["measured"] for k, v in bs2c.items() if k.startswith("E12 "))
    bnd = dict(zip(("canonical", "alt"), [float(x_) for x_ in re.findall(r"<= ([0-9.e+-]+) a0", str(e12))]))
    P("    against BS2's KiDS bound on the stacked rms external field (E12, d chi^2 <= 4): " + "; ".join(
        f"{k_[0]} {k_[1][:3]} ({k_[2]}) {gext[k_] / A0[k_[1]] / bnd[k_[1]]:.0f}x the bound" for k_ in gext))
    OUT["numbers"]["D_bs2_bound"] = bnd

    def phantom_efe(Mb_kg, a0, ge, bp, Lm=None, yth=0.0):
        """the enclosed QUMOND phantom mass in a uniform external field ge (monopole of the flux, exact for QUMOND given the field):
        M(r) = r^2/G <C(|g|) (g_r + ge mu)>_mu, g = g_bp r^ + ge e^, C(g) = X(g/a0 - y_th) a0/g; bp: the lens field band-passed."""
        gN = G * Mb_kg / RG ** 2
        gb = gN * (1 - gfr(RG / Lm)) if bp else gN
        mu = np.linspace(-1, 1, 401)
        gt = np.sqrt(gb[:, None] ** 2 + ge ** 2 + 2 * gb[:, None] * ge * mu[None, :])
        Cq = XL(gt / a0 - (yth if bp else 0.0)) * a0 / np.maximum(gt, 1e-300)
        return RG ** 2 / G * _trap(Cq * (gb[:, None] + ge * mu[None, :]), mu, axis=1) / 2.0

    def chi2(model):
        r_ = (model - F18.KE).ravel()
        return float(r_ @ np.linalg.solve(F18.C60, r_))
    kd = {}
    for sname in DSEPS:
        Ls_ = {"none": None, "H_Y": L025_m, "H_K1": HK1_LL * OmL_a(0.8) * MPCm}[sname]
        for f in FOOTS:
            ys_ = {"none": 0.0, "H_Y": yth025, "H_K1": SEP_HK1[f].yth(0.8)}[sname]
            base, efe = {}, {}
            for rd_ in ("a", "b"):
                mods_iso, mods_efe = [], []
                for b in range(4):
                    Mb_kg = 10 ** F18.B21_MGAL[b] * LGM
                    if sname != "none":
                        ph = M6["phantom"](Mb_kg, A0[f], Ls_, ys_, ns9["YIELD"])
                    else:
                        ph = M6["phantom"](Mb_kg, A0[f])
                    ph = np.maximum(ph, 0.0)
                    iso_raw = phantom_efe(Mb_kg, A0[f], 0.0, sname != "none", Ls_, ys_)
                    efe_raw = phantom_efe(Mb_kg, A0[f], gext[(sname, f, rd_)], sname != "none", Ls_, ys_)
                    R_ = np.where(iso_raw > 0, efe_raw / np.maximum(iso_raw, 1e-300), 1.0)
                    Mg12 = 10 ** F18.B21_MGAL[b] / 1e12
                    Mi = lambda r, ph=ph: Mg12 + np.interp(np.log(np.maximum(r, rgM[0])), np.log(rgM), ph / LGM / 1e12)
                    Me = lambda r, ph=ph, R_=R_: Mg12 + np.interp(np.log(np.maximum(r, rgM[0])), np.log(rgM), ph * R_ / LGM / 1e12)
                    mods_iso.append(F18.esd_of(Mi)); mods_efe.append(F18.esd_of(Me))
                base[rd_] = chi2(np.array(mods_iso)); efe[rd_] = chi2(np.array(mods_efe))
            kd[(sname, f)] = dict(iso=base["a"], efe_a=efe["a"], efe_b=efe["b"], iso_same=abs(base["a"] - base["b"]) < 1e-9)
            P(f"    {sname:5s} {f:9s}: chi2 isolated lens {base['a']:.1f} (identical in both readings: {kd[(sname, f)]['iso_same']}); with the "
              f"web's field in the kernel: (a) {efe['a']:.1f} (d {efe['a'] - base['a']:+.1f}), (b) {efe['b']:.1f} (d {efe['b'] - base['a']:+.1f})")
    OUT["numbers"]["D"] = dict(gext={"/".join(k_): v_ for k_, v_ in gext.items()}, ratio={"/".join(k_): v_ for k_, v_ in ratio_ext.items()},
                               kids={"/".join(k_): v_ for k_, v_ in kd.items()})
    check("D1 DERIVED: KiDS's isolated-lens term is the same in both readings (around an isolated lens the kernel's source is its "
          "baryons either way -- identical by construction, printed through FP18's projection); the reading changes only the web's "
          "field in the kernel, which in (b) is the baryons' share: 0.06-0.09 of (a)'s (each reading's own growth)",
          "chi^2 identical: " + ", ".join(f"{k_[0]}/{k_[1][:3]} {v_['iso_same']}" for k_, v_ in kd.items()) + "; external field (b)/(a) "
          + ", ".join(f"{k_[0]}/{k_[1][:3]} {v_:.3f}" for k_, v_ in ratio_ext.items()),
          all(v_["iso_same"] for v_ in kd.values()) and all(v_ < 0.5 for v_ in ratio_ext.values()))
    check("D2 (reported) A KiDS RISK THE COMMITTED KiDS MODELS OMIT: the web's external field in the kernel (3D rms at z = 0.25 as a "
          "uniform field, exact QUMOND monopole, FP18's projection) costs d chi^2 ~ +200 in (b) and ~ +600 in (a) with H_Y or H_K1 (both "
          "footings) -- 5-10x over BS2's stacked bound in (b); the isolated lenses' own weaker environment (B21's isolation) is not "
          "modelled here, so this is an upper-side estimate",
          "; ".join(f"{k_[0]}/{k_[1][:3]}: (a) {v_['efe_a'] - v_['iso']:+.1f}, (b) {v_['efe_b'] - v_['iso']:+.1f}" for k_, v_ in kd.items()),
          True, load_bearing=False)

# ================================================================================================= PART E
if want("E"):
    banner("E  THE KERNEL ARGUMENT: the PM forest codes vs FP9/FP13's linear proxies")
    pm_files = ["real_research/g03_audit_2026/L346_switch_forest_gate.py", "real_research/g03_audit_2026/L347_switch_forest_flux_power.py",
                "real_research/g03_audit_2026/L362_forest_pincer_convergence.py", "real_research/dark_energy_2026/DE11_forest_converged_model.py",
                "real_research/dark_energy_2026/DE11b_forest_convergence.py"]
    pat_mag = re.compile(r"(gg\s*/\s*a\s*\*\*\s*2)")
    pat_poi = re.compile(r"(poisson\(1\.5\s*\*\s*(?:\w+\.)?Om\s*\*\s*delta\s*/\s*a\)|src\s*=\s*1\.5\s*\*\s*Om\s*\*\s*delta\s*/\s*a)")
    found = {}
    for fp in pm_files:
        src_ = open(os.path.join(REPO, fp)).read()
        found[os.path.basename(fp)] = (bool(pat_mag.search(src_)), bool(pat_poi.search(src_)))
    mU = C.Mesh(64.0, 64); aU = 1 / 3.0; kU = 4 * mU.kf; AU = 0.01
    xg = np.arange(64) * mU.d
    dU = np.broadcast_to(AU * np.cos(kU * xg)[:, None, None], (64, 64, 64)).copy()
    phU = mU.poisson(1.5 * Om * dU / aU)
    g_code = np.max(np.abs(mU.grad_axis(phU, 0))) / aU ** 2 * C.Cosmo("fp6").UNIT_ACC
    g_phys = float(gfield(np.array([AU]), aU, np.array([kU]))[0]) * math.sin(kU * mU.d) / (kU * mU.d)
    fac = g_code / g_phys
    boost = {}
    for z_ in (2.0, 3.0):
        yrms = REF[0.0][z_]["dm"]
        s3 = math.sqrt(_trap(gfield(yrms, 1 / (1 + z_), KX) ** 2, np.log(KX)))
        for f in FOOTS:
            y_ = s3 / A0[f]
            for kn, nuf in (("P2", lambda y: np.sqrt(1 + 1 / y) - 1), ("nu_mono", lambda y: M6["nu_mono"](y) - 1)):
                boost[(z_, f, kn)] = (float(nuf(y_)) / float(nuf((1 + z_) * y_)), math.sqrt(1 + z_), y_)
    gf_phys = max(abs(float(gfield(np.array([0.3]), a_, np.array([k_]))[0]) / (1.5 * Om * H0 ** 2 * 0.3 / (a_ ** 2 * k_ * h_ / Mpc)) - 1)
                  for a_ in (0.25, 0.5, 1.0) for k_ in (0.1, 1.0, 10.0))
    f9s = open(os.path.join(HERE, "FP9_web_galaxy_separator.py")).read(); f13s = open(os.path.join(HERE, "FP13_separator_from_state.py")).read()
    uses_gf = ("gk = gfield(D, a, KHg)" in f9s) and ("gfield(D, a, KHg) * hk" in f13s)
    P("    PM codes: " + "; ".join(f"{k_}: kernel |grad phi|/a^2 {v_[0]}, phi = poisson(1.5 Om delta/a) {v_[1]}" for k_, v_ in found.items()))
    P(f"    plane wave (z = 2): |grad_x phi|/a^2 / physical = {fac:.6f} (1 + z = {1 / aU:.6f})")
    P("    deep-regime boost, physical / code argument, at the linear rms field: " + "; ".join(
        f"z {k_[0]:g} {k_[1][:3]} {k_[2]}: {v_[0]:.3f} (sqrt(1+z) {v_[1]:.3f}, y {v_[2]:.2e})" for k_, v_ in boost.items()))
    P(f"    FP6's gfield = 1.5 Om H0^2 Delta/(a^2 k) (physical) to {gf_phys:.1e}; FP9's growth_aq and FP13's proxy call it: {uses_gf}")
    OUT["numbers"]["E"] = dict(pm_files=found, factor=fac, boost={f"{k_[0]}/{k_[1]}/{k_[2]}": v_ for k_, v_ in boost.items()},
                               gfield_physical=gf_phys, fp9_fp13_use_gfield=uses_gf)
    check("E1 DERIVED (confirms the hub's flag): all five PM forest codes feed the kernel |grad_x phi|/a^2 with phi = poisson(1.5 Om delta/a) "
          "-- (1 + z) x the physical field (plane wave, to 1e-9) -- so their MOND is evaluated sqrt(1+z) too weak in the deep limit and "
          "MORE than that at the forest's own field (C^Q = nu - 1 falls faster than y^-1/2 away from the deep limit): the factor at the "
          "linear rms field is 1.9-2.0 at z = 2 and 2.2-2.5 at z = 3 (P2 and nu_mono, both footings)",
          f"pattern in {sum(v_[0] and v_[1] for v_ in found.values())}/5 files; factor {fac:.9f} vs {1 / aU:.9f}; boost ratio at z = 2/3 "
          + ", ".join(f"{v_[0]:.2f}" for v_ in boost.values()),
          all(v_[0] and v_[1] for v_ in found.values()) and abs(fac * aU - 1) < 1e-9
          and all(v_[1] - 1e-9 <= v_[0] < 2.6 for v_ in boost.values()))
    check("E2 DERIVED: FP9/FP13's forest (and sigma_8) linear proxies do NOT share the pattern -- both evaluate the kernel on FP6's gfield, "
          "which is the physical field 1.5 Om H0^2 Delta/(a^2 k)", f"gfield physical to {gf_phys:.1e}; FP9/FP13 call gfield: {uses_gf}",
          gf_phys < 1e-12 and uses_gf)

# ================================================================================================= W ledger
banner("W  THE LEDGER")
nb = OUT["numbers"]
LEDGER = [
    ("L22a", "the static sector reads the lapse only through the Einstein-frame lapse N e^-chi (FP7's perfect square)", "DERIVED",
     "A1: sympy identity; the MOND scalar reaches matter only through each species' lapse coupling"),
    ("L22b", "WHO FEELS MOND in the action as written (S_m[g], FK1's S_Psi[g]): ALL matter sources and feels the scalar -- reading (a)",
     "DERIVED", "A2: Euler-Lagrange with two species; the feel weights equal the source weights (reciprocity); FP10 writes S_Psi on g"),
    ("L22c", "the chain's kernel-invisible dark component (FP4/FP8/FP10/FP16: L353's pair) on FP7's root", "OPEN",
     "A3: L353 subtracts from C-H's u, which FP7 removed; transplanted literally the pair is inert. The (b) dynamics those lanes (and "
     "the hub's 'chain' label) use has no action on the current root unless L22d is adopted"),
    ("L22d", "the minimal term for (b): FK1 on g~ = g + (1 - e^-2chi) n n, the root's own Einstein-frame metric", "TIED",
     "A4: beta = 1; no new field, no new constant (beta = 0/1 are the only metrics of the root's own); the coupling is a choice"),
    ("L22e", "the cost of (b): a second matter metric; dark-baryon WEP violated where chi != 0; Solar System and GW170817 untouched",
     "CONSTRAINT", "A5: L353's X-COP median 0.47 read-only; no baryonic gate moves"),
    ("L22f", "the zero-field runaway survives the gas's own pressure (the rate saturates at (c/c_s) sqrt(4 pi G rho_b/lambda_eff))",
     "DERIVED", "B1: sympy dispersion + the full 3x3 at the measured T0"),
    ("L22g", "sigma_8 with NO separator, lambda = 0: fails in BOTH readings on every yardstick and footing ((b) 1.45-2.2 x LCDM vs (a) "
     "8-24 x); only inertia lambda_eff >~ 6e5-1e7 ((b)) / 4e7 ((a)) rescues it -- a knob", "FAILS", "B2-B5, C2 (CLASS spectrum; gas at T0)"),
    ("L22h", "with a separator, (b)'s total-matter sigma_8 boost is ~5% of (a)'s; a separator is still NEEDED (band-pass alone fails the "
     "forest, yield alone fails sigma_8); fewest declared constants passing sigma_8 + forest: 1 (H_K1) in both readings", "DERIVED",
     "C1, C2, C4"),
    ("L22i", "the gas's own pressure (measured T0, x1-x4) cannot do the separator's forest job", "DERIVED", "C3"),
    ("L22j", "CMB lensing in the reading the action implies (a): the late-time web MOND is excluded for H_S, H_K1 and H_Y on every "
     "yardstick and footing (Planck 2018 8-400 / ACT DR6)", "FAILS", "L0 (reproduces XR26), L2"),
    ("L22k", "CMB lensing in (b): the lensing phantom is cut only ~sqrt(f_b)-like (not f_b^2); real-space f_eff 0.13-0.26 vs the needed "
     "0.62 (linear) / 0.18 (halofit): passes Planck and ACT on the linear base, fails ACT on the halofit base", "OPEN",
     "L1, L2: decided by the nonlinear phantom (a particle-mesh question, not run here)"),
    ("L22l", "KiDS: the isolated-lens term is reading-independent; the web's external field in the kernel (omitted by the committed "
     "KiDS models) is a risk in both readings (~+200 (b), ~+600 (a) with H_Y/H_K1; uniform-rms estimate)", "OPEN", "D1, D2 (FP18's projection)"),
    ("L22m", "the PM forest codes' kernel argument is (1+z) x physical (MOND 1.9-2.5x too weak at z = 2-3); FP9/FP13's linear proxies "
     "are physical", "DERIVED", "E1-E2"),
]
for k_, w_, s_, b_ in LEDGER:
    P(f"    {k_:5s} {s_:10s} {w_}  --  {b_}")
OUT["ledger"] = [dict(link=k_, what=w_, status=s_, basis=b_) for k_, w_, s_, b_ in LEDGER]
check("W (reported) the ledger", f"{len(LEDGER)} links", True, load_bearing=False)

# ================================================================================================= verdict
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
banner("VERDICT")
P("  WHO FEELS MOND.  The action as written puts ALL matter in the MOND sector (reading a): FK1 lives on the matter metric g, the\n"
  "  scalar reaches matter only through the lapse, and whatever feels it sources it.  The kernel-invisible reading (b) that the\n"
  "  dark-sector lanes use has no action on FP7's root (L353's pair targets C-H's u, which FP7 removed); FK1 on the root's own\n"
  "  Einstein-frame metric g~ realises it with no new field or constant, at the price of a second matter metric.\n"
  "  SEPARATOR.  Neither reading removes it: with no separator sigma_8 fails in both (the baryons alone run away and drag the dark),\n"
  "  and the gas's pressure cannot do the forest's job.  (b) cuts the matter boost ~20x but the LENSING phantom only ~2-8x.\n"
  "  CMB LENSING.  In the action as written the late-time web MOND is excluded by Planck and ACT lensing for every separator; in (b)\n"
  "  it passes on the linear base and fails ACT on the halofit base -- undecided until the nonlinear phantom is computed.")
_name = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
OUT["wall_s"] = time.time() - T0
json.dump(OUT, open(os.path.join(HERE, _name), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
P(f"\n  {len(CH) - n_fail}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {_name}   {el()}")
sys.exit(0 if n_fail == 0 else 1)
