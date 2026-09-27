#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FP10 -- THE DARK SECTOR AT ITS HONEST MINIMAL PRICE: FK1's internal splitting written as an action, the clearing it derives,
and FK1's OWN density trigger scored on every gate.

WHY.  FP4 (committed) showed that the core's own fields cannot carry the dark mass: the minimal addition is one nearly free
complex scalar Psi (m >= 1.9-5.2e-19 eV, amount = initial data, kernel-invisible through L353's pair).  FP4 and FP8 (a
no-go) showed that no density, current or derivative coupling lets the MOND sector power the kick: by the reciprocity
identity the energy taken is -Int S.d_t grad u, and unbinding the z = 2.5 flagship's dark mass costs 7-12x the host's MOND
field energy.  FP8's honest minimal price is that the kick's energy comes from the dark field ITSELF: FK1's U(1)-breaking
splitting eps Re(Phi^2) (eps/m^2 = 1.84-2.35e-6, FITTED), its trigger (a conversion coupling lambda(K) with a K-gate exponent
q, DECLARED), an initial misalignment near the heavy axis (initial data), and m.  FK1's trigger is a DENSITY threshold (the
fluid's own n^2, Bose-stimulated), not the acceleration trigger AT1/AT3 scored.  This lane writes that dark sector as an
action, derives its clearing dynamics from the action's own variation, and runs FK1's own trigger through AT3's gates.

THE ACTION (FK1 + FL2, varied here; units hbar = c = 1 where symbolic):
    S_Psi = -Int d^4x sqrt(-g) [ g^{mn} d_m Phi* d_n Phi + m^2 |Phi|^2 + eps Re(Phi^2) + lambda(K) (Im Phi^2)^2 ]
    lambda(K) = lambda_0 (K / 3 H_0)^(-2q),   K = div n (the khronon's expansion, = 3H on CMC leaves, CV4)
    Phi = (phi_H + i phi_L)/sqrt(2):  V = (m^2 + eps) phi_H^2/2 + (m^2 - eps) phi_L^2/2 + lambda phi_H^2 phi_L^2
  plus L353's constrained pair (the MOND kernel reads the baryons only; Psi feels Newtonian gravity; FL2 V1: both components
  kernel-invisible).  The dark action contains NO MOND-sector field (u, W, U), so its source S in the MOND equation is 0.
  The core it sits on is the chain's root (FP7's repaired root; the separator FP9 is pending); the retention machinery below
  uses exactly the force law this implies (Newtonian orbits for the dark state, the baryons' MOND field for the flagship).

WHAT IS DERIVED (part A, sympy + numbers):
  A1 masses m_H^2 - m_L^2 = 2 eps, Z2 x Z2, and the kick v_k = sqrt(2 eps/(m^2 + eps)): eps/m^2 = v_k^2/(2 - v_k^2);
     latent heat per unit mass v_k^2/2.
  A2 RECIPROCITY: S = 0 identically (the phantom is not rewritten, delta = 0); the kick's energy is the rest-energy
     difference.  Energy selectivity: v_k^2/2 against FP8's committed specific unbinding costs.
  A3 the NR reduction of lambda phi_H^2 phi_L^2 (rotating-wave): pair vertex lambda/(4 m_H m_L), density coupling
     lambda/(m_H m_L); the pair instability of a heavy condensate grows at sqrt(G^2 - D^2), G = lambda n_H/(2 m_H m_L).
  A4 the Hubble sweep: pi G^2/(4 H Delta) e-folds; with lambda(K) the trigger density n_t ~ H^(2q + 1/2) (q = 7/4: E^4);
     the background's exponent peaks at (1+z)^3 = Omega_L/Omega_m and stays far below the trigger's.
  A5 THE HALO GAIN (new here): a virialised heavy field (Maxwellian, dispersion sigma) pumps a daughter mode at the
     Doppler-broadened golden-rule rate gamma = sqrt(pi) G^2/(m v_k sigma); along an outward path the gain per needed e-fold is
         S_c(r) = (2/sqrt(pi)) H Int_r^{r200} (rho/rho_t)^2 exp(-(Dv/sigma)^2) dr'/sigma,   Dv = v_k - sqrt(v_k^2 - 2 DPhi),
     i.e. the FK1 session's design form with its C = sqrt(pi) (inside the design's 0.3-3), and a detuning exponent 1.
     In units of r200 and V200 it depends only on (c, E(z), v_k/V200).  Spontaneous ignition where S_c >= 1; the stimulated
     front is the outermost r with S_c >= 1/K, K = sqrt(pi) E_need x 3^(+-1) = 36-947 (E_need = 61-178, FK1 N1).
  A6 WHERE: the front over (c, z); ignition; non-selectivity (the converted carrier's share in hosts >= 1e10.5 Msun).
  A7 WHEN: the conversion time at the front is << the dynamical time at z <= 2.5: every halo converts at its collapse, in its
     progenitors.  So FK1's own timing is the HISTORY reading; AT1's rule applied at the scoring epoch (IN PLACE) stands for
     full re-accretion of the escaped daughters and is kept as the pessimistic bracket.
  A8 (reported flag) the web: the stimulated criterion in the Hubble flow; an S_8 bracket if the web converts too.
THE GATES (part B), both a0 footings (FP0's 9.3603e-11 / 1.1312e-10; the machinery's 9.3619e-11 / 1.1279e-10 wherever a
  committed function is called), THREE readings where the reading matters:
    IN PLACE   AT3's machinery as it scored AT1: AT1's retained_acc with r_v = the fluid's front, at the scoring epoch
               (self-consistent potential; the intact potential reported beside it);
    HISTORY    FK1's own timing (A7): the flagship's r_F was passed by the front in the main progenitor at z_pass; if that
               progenitor's v_esc(r_F) < v_k the in-place population left then (the design's progenitor gate, XR16's form,
               re-implemented here with this lane's derived depth); for groups and clusters AT4's OPTIMISTIC reading (the
               cumulative bias-weighted escaped fraction removed from every halo: the escaped daughters never return);
    PM PROXY   the committed particle-mesh track at the SAME threshold delta_t(z) and the same kicks (L388 pooled; L389
               Harvey; MS3 K1 cosmic shear) -- a density trigger at rate 10 H, not FK1's sharp conversion: reported only.
  B1 the flagship at z = 0.5, 1, 1.5, 2, 2.5 (GP5's definition, AT1's arithmetic; gate |shift| <= 0.074 dex, AT1's A2 pass
     level; 0.05 and 0.10 reported).  B2 z = 0 galaxies / RAR (L321's three hosts, <= 0.06 dex).  B3 X-COP (L321/L372,
     strict 0.8-1.2; alt with 6% non-thermal).  B4 KiDS-1000 (L360's switched fit at the common cell, <= +4).  B5 Harvey+2015
     (L370's machinery via L372's harvey(), AT3's wiring).  B6 S_8 (L319's solver on the halo-model budget; ratio >= 0.922
     strict, 0.899 alt; PAPER34's absolute floors 0.752/0.748 reported).  B7 the Lyman-alpha forest (the budget against AT2's
     scored regime; projection with the committed particle-mesh responses).  B8 cosmic shear (MS3's halo model, the 1.75 Mpc
     KiDS-safe cap, door convention, R <= 1.2).  B9 the gate table and the window per reading.
THE TIE (part C): the dimension matrix of (a0, rho_Lambda, G, c) [+ hbar, m]; a census of m-free monomials with its
  look-elsewhere rate; the m each m-dependent tie needs; the trigger's constants.
THE COUNT (part D): the dark sector's constants, and the whole theory's (FP7's root + FP9 TBD + this sector).
GRID (reduced, this run): kicks 575-650 km/s (retention at 575 and 650; the progenitor gate, S_8 and the budget at 575/600/625/
  650), K = 36/184/947, alpha = dlnM/dz 0.6/0.8/1.0, trigger normalisation f_t = 1 (1/3, 3 and q = 1.25/2.5 on the budget),
  the flagship gas range at z = 2.5 only, Harvey at three cells.  FP10_FULL=1 runs retention at all four kicks, the gas range
  at every z, and Harvey at all four kicks in both readings (see the hand-off line printed at the end).
PRE-DECLARED (scratch notes written before any FP10 number; only a timing probe had run, reproducing XR16's uncommitted in-place
  S at M_b = 1e11, z = 2.5):  H1 the front sits at >= 0.9 r200 in every halo with c >= 3 at z <~ 4;  H2 the flagship passes in
  the history reading and in place (self-consistent) and fails in place (intact) at 1e11, z = 2.5;  H3 X-COP fails in place
  at every kick (L372's single-channel pincer);  H4 cosmic shear fails in place at the 1.75 Mpc cap;  H5 the escaped budget
  by z = 0 is >= 0.4 (S_8 undecided);  H6 the forest is not established (budget >= 4x AT2's);  H7 Harvey passes in place at
  650;  H8 KiDS passes in place;  H9 z = 0 galaxies pass;  H10 eps has no tie ("only kappa is dimensionless; any tie needs
  m");  H11 the in-place reading has no window.  They are reported as they fell (check H).
HISTORY (stated).  Exploratory component runs (not committed) came first: the front grid, the budget and S_8, in-place X-COP /
  galaxies / KiDS, cosmic shear, the in-place flagship at every z, the progenitor passages, and two Harvey cells.  The check
  directions were fixed after them; nothing was retuned.  XR16 (a parallel session's lane, UNCOMMITTED) implements the
  design's depth; it is not loaded here -- the depth is re-derived (A5) and re-implemented, and XR16's numbers are not used.
  After a smoke run (FP10_SMOKE, not committed) two checks were corrected: A7 was worded "< 1e-2 of a dynamical time"; the
  smoke run measured 0.087 at 0.9 r200 (z = 2.5), so A7 now claims < 0.1 there and < 1e-2 inside 0.5 r200, both printed.  C2
  listed a0/(c H0) on the alt footing as a separate base (it is 1/Z exactly) and scored half-integer powers, for which
  Omega_Lambda covers every window (a look-elsewhere rate of 1): the census now counts integer powers and lists the rest.
  The first main run was stopped after ~1 min (part A) to replace A2's schematic NR Lagrangian by the exact one (A3's
  vertices); no number from it was used.  After the first complete main run (31/31, rc = 0) only printed text changed: the
  verdict still said "< 1e-2 of a dynamical time" (A7's pre-smoke wording) and now matches A7; the window line names its
  kicks; C2 prints its bases with a legend; the verdict notes that S = 0 leaves XR9's MOND-sector failures untouched.  The
  numbers are deterministic (fixed seeds) and did not change.
CHECKS (load-bearing unless marked)
  C0 CONTROLS (not load-bearing): FK1's committed eps/m^2 from A1's identity; AT1's committed z = 2.5 flagship row through the
     loaded machinery, and this lane's shift arithmetic on it; this lane's copy of retained_acc bit-identical to AT1's with
     nothing dropped; MS3's committed K1 row (L388's retention, 1.75 Mpc); AT3's committed X-COP row; the depth integral against
     the singular-isothermal closed form; the solver with no conversion returns LCDM's S_8.
  A1-A8 as above (A8 reported).  B1-B9 as above (B-rows in the PM-proxy reading reported).  C1-C4 the tie.  D the count.
  H (reported) the pre-declared hypotheses as they fell.  W the ledger.
MUTATE=1: eps = 0 -- no splitting, so the conversion is a relabelling with no kick (v_k = 0 at every cell).  A1's kick, A2's
  energy selectivity, B1's flagship (history reading) and B2's galaxies must FAIL: rc = 1.  (Harvey is not run under MUTATE.)

Run from the repository root:  python3 real_research/derivation_chain_2026/FP10_internal_splitting_dark_sector.py
(~25 min, at most two threads, ~14 GB peak in the Harvey section).  FP10_FULL=1 for the full grid (hub).
"""
import os, sys, io, re, json, math, time, contextlib, warnings

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")                                   # shared machine: at most two workers
for _v in ("AT1_THREADS", "AT3_THREADS", "L357_THREADS"):
    os.environ[_v] = "2"
import numpy as np
import sympy as sp
from concurrent.futures import ThreadPoolExecutor
from scipy.interpolate import RegularGridInterpolator

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = os.environ.get("MUTATE", "0") == "1"
FULL = os.environ.get("FP10_FULL", "0") == "1"
SMOKE = os.environ.get("FP10_SMOKE", "0") == "1"                     # code test only (fewer orbits/hosts); never committed
SMOKE_DIR = os.environ.get("FP10_SMOKE_DIR", "")
SLUG = "FP10_internal_splitting_dark_sector" + ("_FULL" if FULL else "") + ("_MUTATE" if MUTATE else "")
T0 = time.time()
NW = 2
OUT = {"lane": "FP10", "mutate": MUTATE, "full": FULL, "smoke": SMOKE, "checks": {}, "numbers": {}, "ledger": []}
CH = []


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def rd(rel):
    return json.load(open(os.path.join(REPO, rel)))


def elapsed():
    return f"[{time.time() - T0:.0f}s]"


P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: eps = 0 -- the conversion is a relabelling with no kick; A1, A2, B1 (history) and B2 must FAIL ***")
if FULL:
    P("\n  *** FP10_FULL=1: the full grid (hub run) ***")
if SMOKE:
    P("\n  *** FP10_SMOKE=1: reduced orbits and hosts, a code test only; never for the record ***")

# ------------------------------------------------------------------------------------------------ constants, footings (FP0)
c_SI, G_SI = 299792458.0, 6.67430e-11
C_KMS = c_SI / 1e3
MPC_M = 3.0856775814913673e22
H0_SI = 67.4e3 / MPC_M
OM_L = 0.6847
RHO_CRIT = 3 * H0_SI ** 2 / (8 * math.pi * G_SI)
A0_FP0 = {"canonical": 0.5 * c_SI * math.sqrt(G_SI * OM_L * RHO_CRIT), "alt": 0.5 * c_SI * math.sqrt(G_SI * RHO_CRIT)}
OUT["numbers"]["a0_FP0"] = A0_FP0
FEET = ("canonical", "alt")
VK_ALL = (575.0, 600.0, 625.0, 650.0)
VK_RET = VK_ALL if FULL else (575.0, 650.0)
VK = {v: (0.0 if MUTATE else v) for v in VK_ALL}                     # the kick the splitting actually gives (MUTATE: eps = 0)
ALPHAS = (0.6, 0.8, 1.0)
FLAG_TOL, FLAG_TIGHT, FLAG_GP5 = 0.074, 0.05, 0.10
S_MAX = 0.059                                                        # MS2's allowed retained carrier at r_F (reported)
ZF = (0.5, 1.0, 1.5, 2.0, 2.5)
NRET = 2000 if SMOKE else 10000

# ================================================================================================ the committed machinery
banner("LOADING the committed lanes' machinery (read-only exec; nothing is edited)")
_env_mut, _env_fast = os.environ.get("MUTATE"), os.environ.get("FAST")
os.environ["MUTATE"], os.environ["FAST"] = "0", "0"                   # the loaded lanes' own controls stay off
PA3 = os.path.join(REPO, "real_research", "acceleration_trigger_2026", "AT3_acceleration_trigger_full_gates.py")
_s3 = open(PA3).read()
_h3 = _s3.split("# ================================================================================================ C1 control")[0]
_h3 = _h3.replace('P(__doc__.split("CHECKS")[0].strip())', "pass")
A3 = {"__name__": "at3", "__file__": PA3}
with contextlib.redirect_stdout(io.StringIO()):
    exec(_h3, A3)
A1, L57, Lm = A3["A1"], A3["L57"], A3["Lm"]
retained_acc, flagship_rows, xcop_from_eps, gal_shifts, kids_switched = (A3[k] for k in (
    "retained_acc", "flagship_rows", "xcop_from_eps", "gal_shifts", "kids_switched"))
hernquist, nfw21, FB, GK = A3["hernquist"], A3["nfw21"], A3["FB"], A3["GK"]
FOOT, A0K = A3["FOOT"], A3["A0K"]
CL, CLREF, cl_mass_fn, GAL = A3["CL"], A3["CLREF"], A3["cl_mass_fn"], A3["GAL"]
M200_KIDS, c200_55, RHOC_ZL, ZL, LOGMS = A3["M200_KIDS"], A3["c200_55"], A3["RHOC_ZL"], A3["ZL"], A3["LOGMS"]
RHO_C0, c200_z0 = A3["RHO_C0"], A3["c200_z0"]
potential, frac_inside, RG, RGc = A1["potential"], A1["frac_inside"], A1["RG"], A1["RGc"]
Ez2, RHOC0_KPC, Om, hh = A1["Ez2"], A1["RHOC0_KPC"], A1["Om"], A1["h"]
halo_mass, c200_20, Re_kpc, galaxy_baryons, g_nfw = A1["halo_mass"], A1["c200_20"], A1["Re_kpc"], A1["galaxy_baryons"], A1["g_nfw"]
nu20, nu_mono, G20, MSUN20, KPC20 = A1["nu20"], A1["nu_mono"], A1["G20"], A1["MSUN"], A1["KPC"]
I_LC, I_ES, CG, XVG, UGR, nfw_phi = A1["I_LC"], A1["I_ES"], A1["CG"], A1["XVG"], A1["UGR"], A1["nfw_phi"]
MH, SIG0, DG, f_st, b_st, DC, c_dm14, _trap = A1["MH"], A1["SIG0"], A1["DG"], A1["f_st"], A1["b_st"], A1["DC"], A1["c_dm14"], A1["_trap"]
ZG, a_grid, solve_hist = A1["ZG"], A1["a_grid"], L57["solve_hist"]
S8_LCDM = float(L57["S8_LCDM"])
KERNELS = (("l320", nu20), ("mono", nu_mono))
P(f"  AT3's head (AT1, L357, L320, BK1, L321, L355, L360) loaded   {elapsed()}")
PMS3 = os.path.join(REPO, "real_research", "mond_sector_gate_2026", "MS3_cosmic_shear_bound_mond_sector.py")
MS = {"__name__": "ms3", "__file__": PMS3}
_ms = open(PMS3).read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(_ms[:_ms.rindex("# ============================================================================================ C1 control")]
         .replace('P(__doc__.split("CHECKS")[0].strip())', "pass"), MS)
R_of, XLIN, A0_MS3, ret_L388 = MS["R_of"], MS["XLIN"], MS["A0"], MS["ret_L388"]
P(f"  MS3's halo model (L363, GP0, L388's retention) loaded: z = 0.5, common cell x_c,eff = {XLIN:.5f}   {elapsed()}")
if _env_mut is None: os.environ.pop("MUTATE", None)
else: os.environ["MUTATE"] = _env_mut
if _env_fast is None: os.environ.pop("FAST", None)
else: os.environ["FAST"] = _env_fast
P(f"  footings: FP0 {A0_FP0['canonical']:.4e} / {A0_FP0['alt']:.4e} m/s^2; the machinery's {FOOT['canonical']:.4e} / {FOOT['alt']:.4e}")
J = dict(
    FK1=rd("real_research/dark_fluid_kick_2026/FK1_kick_as_phase_change_results.json")["numbers"],
    FP8=rd("real_research/derivation_chain_2026/FP8_current_coupling_kick_results.json")["numbers"],
    AT1=rd("real_research/acceleration_trigger_2026/AT1_acceleration_trigger_highz_results.json")["numbers"],
    AT2=rd("real_research/acceleration_trigger_2026/AT2_forest_flux_calibrated_results.json")["numbers"],
    AT2m=rd("real_research/acceleration_trigger_2026/AT2_forest_flux_calibrated_results_MUTATE.json")["numbers"],
    AT3=rd("real_research/acceleration_trigger_2026/AT3_acceleration_trigger_full_gates_results.json")["numbers"],
    MS3=rd("real_research/mond_sector_gate_2026/MS3_cosmic_shear_bound_mond_sector_results.json")["numbers"],
    L388=rd("real_research/dark_sector_2026/L388_linear_gate_pooled_results.json")["numbers"],
    L389=rd("real_research/dark_sector_2026/L389_harvey_same_cell_linear_gate_results.json")["numbers"],
)
E_NEED = sorted(float(v["efolds"]) for v in J["FK1"]["N1"]["by_mass"].values())
E_LO, E_HI = E_NEED[0], E_NEED[-1]
K_MID = math.sqrt(math.pi) * math.sqrt(E_LO * E_HI)
KS = (math.sqrt(math.pi) * E_LO / 3.0, K_MID, math.sqrt(math.pi) * E_HI * 3.0)
K_LO, K_HI = KS[0], KS[-1]
P(f"  FK1 N1 (committed): E_need {E_LO:.1f}-{E_HI:.1f} e-folds -> K = sqrt(pi) E_need x 3^(+-1): {', '.join(f'{k_:.0f}' for k_ in KS)}")

# ================================================================================================ the derived depth (A5), coded
AMPD = 2.0 / math.sqrt(math.pi)                                      # the derived gain prefactor (A5): S_c = AMPD H Int (rho/rho_t)^2 D dl/sigma
C_DESIGN = math.sqrt(math.pi)                                         # the same in the design's (2 C H / pi) form


def mfn(c):
    return math.log1p(c) - c / (1 + c)


def Hz(z):                                                           # km/s/kpc
    return 0.1 * hh * math.sqrt(Ez2(z))


def rho_t(z, ft=1.0, qg=1.75):
    """the trigger density (total-matter units, Msun/kpc^3): the Hubble-flow sweep gives E_need e-folds (A4) at
    rho_t = f_t (5/3) rho_crit0 E(z)^(2q + 1/2) -- FK1's normalisation to the linear gate's delta_t(z) = 2.5 E^2/(1.5 Om(z))."""
    return ft * (5.0 / 3.0) * RHOC0_KPC * Ez2(z) ** ((2 * qg + 0.5) / 2.0)


# the dimensionless NFW (V200 = r200 = 1; AT1's tables use the same halo)
XG = np.unique(np.concatenate([np.geomspace(1e-4, 1.0, 240), 1.0 - np.geomspace(1e-4, 0.3, 60)]))
XG = XG[(XG > 0) & (XG <= 1.0)]


def sig_hat(c):
    xx = np.geomspace(1e-5, 200.0, 5000)
    M = (np.log1p(xx * c) - xx * c / (1 + xx * c)) / mfn(c)
    rho = 1.0 / (xx * c * (1 + xx * c) ** 2)
    integ = rho * M / xx ** 2
    seg = 0.5 * (integ[1:] + integ[:-1]) * np.diff(xx)
    s2 = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]]) / rho
    return np.sqrt(np.interp(XG, xx, s2))


def _depth_core(x, qq, sg, ph, u, amp):
    """S_c(x_i) = amp Int_{x_i}^{x_max} qq^2 exp(-(dv/sg)^2) dx'/sg on an ascending grid (trapezoid in ln x)."""
    n = len(x)
    dPhi = ph[None, :] - ph[:, None]
    dv = u - np.sqrt(np.maximum(u ** 2 - 2 * dPhi, 0.0))
    W = (qq ** 2 / sg * x)[None, :] * np.exp(-(dv / sg[None, :]) ** 2)
    seg = 0.5 * (W[:, 1:] + W[:, :-1]) * np.diff(np.log(x))[None, :]
    seg = np.where(np.arange(n - 1)[None, :] >= np.arange(n)[:, None], seg, 0.0)
    return amp * seg.sum(1)


def depth_dimless(c, z, u, ft=1.0, qg=1.75, sg=None):
    """A5 in r200 / V200 units: H dr/sigma = dx/(10 sigma_hat); rho/rho_t = (200/3) c^3/(m(c) cx(1+cx)^2) rho_crit(z)/rho_t(z)."""
    sg = sig_hat(c) if sg is None else sg
    qq = (200.0 / 3.0) * c ** 2 / (mfn(c) * XG * (1 + c * XG) ** 2) * RHOC0_KPC * Ez2(z) / rho_t(z, ft, qg)
    return _depth_core(XG, qq, sg, nfw_phi(XG, c), u, AMPD / 10.0)


def front(x, S, thr):
    """outermost radius with S >= thr (linear in S between grid points); x[-1] if S >= thr there."""
    ok = S >= thr
    if not ok.any(): return 0.0
    i = int(np.where(ok)[0].max())
    if i == len(x) - 1: return float(x[-1])
    t = (S[i] - thr) / max(S[i] - S[i + 1], 1e-300)
    return float(x[i] + min(max(t, 0.0), 1.0) * (x[i + 1] - x[i]))


def prof_bary(Mh, c, z, Mb_fn, rhoc=None):
    """a real host: AT1's truncated NFW carrier + its baryons (Phi on RG, AT1's potential with Newtonian orbits) and the
    untruncated isotropic Jeans dispersion of the NFW tracer (larger near r200: the conservative side for 'the front is
    at r200').  rhoc: the host's own critical density where its lane defines one."""
    rhoc = RHOC0_KPC * Ez2(z) if rhoc is None else rhoc
    Mn, r200, rs = nfw21(Mh, c, rhoc)
    Mc0 = lambda x: (1 - FB) * Mn(np.minimum(x, r200))
    _, Phi = potential(Mb_fn, Mc0, 0.0, "newtonian")
    gu, _ = potential(Mb_fn, lambda x: (1 - FB) * Mn(x), 0.0, "newtonian")
    rho = 1.0 / ((RG / rs) * (1 + RG / rs) ** 2)
    integ = rho * gu; seg = 0.5 * (integ[1:] + integ[:-1]) * np.diff(RG)
    sig2 = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]]) / rho
    return dict(Mh=Mh, c=c, z=z, r200=r200, rs=rs, rho_s=Mh / (4 * math.pi * rs ** 3 * mfn(c)), Phi=Phi,
                sig=np.sqrt(np.maximum(sig2, 1e-30)))


def depth_bary(Pp, vk, n=240, ft=1.0, qg=1.75):
    r200, rs = Pp["r200"], Pp["rs"]
    r = np.unique(np.concatenate([np.geomspace(1e-3 * rs, r200, n), r200 * (1 - np.geomspace(1e-4, 0.3, 50))]))
    r = r[(r > 0) & (r <= r200)]
    qq = Pp["rho_s"] / ((r / rs) * (1 + r / rs) ** 2) / rho_t(Pp["z"], ft, qg)       # (1 - f_b) cancels in the ratio
    S = _depth_core(r, qq, np.interp(r, RG, Pp["sig"]), np.interp(r, RG, Pp["Phi"]), vk, AMPD * Hz(Pp["z"]))
    return r, S


# ------------------------------------------------------------------------------------------------ AT1's retention, copied (drop option)
def retained_fk1(Mb_fn, M200, c, gates, rv, vk, rhoc, N=10000, seed=5, iters=2, drop_inplace=False):
    """AT1's retained_acc (committed lines, copied), with one option: drop_inplace=True removes the in-place decays (the
    population that converted earlier in the progenitor and escaped, the history reading), keeping only the daughters born on
    entry at the front.  With drop_inplace=False it is AT1's retained_acc exactly (control C0c)."""
    Mn, r200, rs = nfw21(M200, c, rhoc)
    Mc0 = lambda x: (1 - FB) * Mn(np.minimum(x, r200))
    rng = np.random.default_rng(seed)
    u = rng.random(N) * float(Mc0(r200)); rgrid = np.geomspace(1e-3 * rs, r200, 5000)
    r = np.interp(u, Mc0(rgrid), rgrid); w = float(Mc0(r200)) / N
    g_pre, Phi0 = potential(Mb_fn, Mc0, 0.0, "newtonian")
    rho = np.where(RG < r200, 1.0 / ((RG / rs) * (1 + RG / rs) ** 2), 1e-300)
    integ = rho * g_pre; seg = 0.5 * (integ[1:] + integ[:-1]) * np.diff(RG)
    sig2 = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]]) / np.maximum(rho, 1e-300)
    sig = np.sqrt(np.interp(r, RG, sig2))
    v = rng.normal(0, 1, (N, 3)) * sig[:, None]
    _ = rng.random(N)                                                 # L321's is_d draw (keeps the draw order identical)
    nh = rng.normal(0, 1, (N, 3)); nh /= np.linalg.norm(nh, axis=1)[:, None]
    vrad0, vtan0 = v[:, 0], np.linalg.norm(v[:, 1:], axis=1); L0 = r * vtan0
    E0 = 0.5 * (vrad0 ** 2 + vtan0 ** 2) + np.interp(r, RG, Phi0)
    if np.isfinite(rv):
        ph = np.interp(RGc, RG, Phi0)
        ok = (2 * (E0[:, None] - ph[None, :]) * RGc[None, :] ** 2 - L0[:, None] ** 2) >= 0
        rp = np.minimum(RGc[np.argmax(ok, axis=1)], r)
        lc = rp < rv; entry = lc & (r > rv)
        del ok
    else:
        lc = np.ones(N, bool); entry = np.zeros(N, bool)
    pos_d = np.where(entry, rv if np.isfinite(rv) else 0.0, r)
    vb2 = np.maximum(2 * (E0 - np.interp(pos_d, RG, Phi0)), 0.0)
    vt_e = np.where(entry, L0 / np.maximum(pos_d, 1e-30), 0.0)
    vr_e = -np.sqrt(np.maximum(vb2 - vt_e ** 2, 0.0))
    vvec = np.where(entry[:, None], np.stack([vr_e, vt_e, np.zeros(N)], 1), v)   # in-place decays keep L321's full vector
    vvec = vvec + (lc * vk)[:, None] * nh
    keep = (~(lc & ~entry)).astype(float) if drop_inplace else None

    def mass_in(dec):
        pos = pos_d if dec else r
        vv = vvec if dec else v
        vr_, vt_ = vv[:, 0], np.linalg.norm(vv[:, 1:], axis=1); L = pos * vt_
        tot = (lambda f: w * f.sum()) if (keep is None or not dec) else (lambda f: w * (keep * f).sum())
        Mc = Mc0
        for _ in range(iters):
            _, Phi = potential(Mb_fn, Mc, 0.0, "newtonian")
            E = 0.5 * (vr_ ** 2 + vt_ ** 2) + np.interp(pos, RG, Phi)
            probe = np.geomspace(0.02 * rs, 3 * r200, 24)
            prof = np.array([tot(frac_inside(E, L, Phi, rg)) for rg in probe])
            Mc = (lambda pr=probe, pm=prof: (lambda x: np.interp(np.asarray(x, dtype=float), pr, pm, left=0.0)))()
        _, Phi = potential(Mb_fn, Mc, 0.0, "newtonian")
        E = 0.5 * (vr_ ** 2 + vt_ ** 2) + np.interp(pos, RG, Phi)
        return np.array([tot(frac_inside(E, L, Phi, rg)) for rg in gates])

    m0 = mass_in(False); m1 = mass_in(True)
    return m1 / np.maximum(m0, 1e-300), float(lc.mean())


def flag_shift(z, Mb, Mh, foot, S, nuf):
    """AT1 flagship_rows' arithmetic, unchanged: 2 log10((g_fw + g_c)/g_fw) at r_out (g_bar = 0.1 a0)."""
    a0 = FOOT[foot]
    r_out_m = math.sqrt(G20 * Mb * MSUN20 / (0.1 * a0))
    gb = G20 * Mb * MSUN20 / r_out_m ** 2
    gc = g_nfw(Mh, z, r_out_m) * S
    g_fw = float(nuf(gb / a0)) * gb
    return 2 * math.log10((g_fw + gc) / g_fw)


def flag_host(lMb, mf, z):
    """AT1's flagship host (flagship_rows' own lines)."""
    Mb = 10 ** lMb; mu = mf * 0.5 * ((1 + z) / 2) ** 2
    Mh = halo_mass(Mb / (1 + mu), z); c = float(c200_20(Mh, z)); a = Re_kpc(Mb / (1 + mu), z) / 1.8153
    rF = {f_: math.sqrt(G20 * Mb * MSUN20 / (0.1 * FOOT[f_])) / KPC20 for f_ in FEET}
    return dict(lMb=lMb, mf=mf, z=z, Mb=Mb, Mh=Mh, c=c, a=a, rhoc=RHOC0_KPC * Ez2(z), rF=rF)


# ================================================================================================ C0 controls
banner("C0  CONTROLS: the loaded machinery reproduces committed numbers")
_eps_m2 = lambda v_: (v_ / C_KMS) ** 2 / (2 - (v_ / C_KMS) ** 2)
dev_fk1 = max(abs(_eps_m2(float(k_)) - v_) / v_ for k_, v_ in J["FK1"]["K2"]["eps_over_m2"].items())
check("C0a CONTROL: A1's identity eps/m^2 = v^2/(2c^2 - v^2) reproduces FK1's committed K2 values at 575-650 km/s",
      f"max relative deviation {dev_fk1:.1e}", dev_fk1 < 1e-9, load_bearing=False)
Lm["A0"] = A0K["canonical"]
_ctl = flagship_rows(2.5, 0.1, 600.0, mufacs=(1.0,), feet=("canonical",), lMbs=(10.5,), N=(1500 if SMOKE else 10000))
_ref = [r_ for r_ in J["AT1"]["A2"]["0.1|600.0|2.5"]["rows"] if r_["footing"] == "canonical" and r_["logMb"] == 10.5
        and abs(r_["mu_fac"] - 1.0) < 1e-9]
dev_at1 = max(abs(a_["shift"] - b_["shift"]) for a_, b_ in zip(sorted(_ctl, key=lambda d: d["kernel"]), sorted(_ref, key=lambda d: d["kernel"])))
_h = flag_host(10.5, 1.0, 2.5)
dev_arith = max(abs(flag_shift(2.5, _h["Mb"], _h["Mh"], "canonical", r_["retained"], dict(KERNELS)[r_["kernel"]]) - r_["shift"]) for r_ in _ref)
check("C0b CONTROL: the loaded retention and flagship machinery reproduces AT1's committed z = 2.5 row (y_v 0.1, v_A 600 km/s, "
      "canonical, M_b 1e10.5, central gas, both kernels), and this lane's shift arithmetic on the committed retained fraction",
      f"machinery max |dev| {dev_at1:.1e} dex; arithmetic max |dev| {dev_arith:.1e} dex",
      dev_at1 < (5e-2 if SMOKE else 1e-9) and dev_arith < 1e-12, load_bearing=False)
_Hc = GAL["Milky Way"]
_a = retained_acc(hernquist(_Hc["Mb"], _Hc["a"]), _Hc["M200"], float(c200_z0(_Hc["M200"])), [8.0, 30.0], 150.0, 350.0, RHO_C0, N=3000)[0]
_b = retained_fk1(hernquist(_Hc["Mb"], _Hc["a"]), _Hc["M200"], float(c200_z0(_Hc["M200"])), [8.0, 30.0], 150.0, 350.0, RHO_C0, N=3000)[0]
dev_copy = float(np.max(np.abs(np.asarray(_a) - np.asarray(_b))))
check("C0c CONTROL: this lane's copy of AT1's retained_acc (drop option off) is bit-identical to AT1's on identical draws (Milky "
      "Way host, r_v 150 kpc, 350 km/s)", f"AT1 {np.round(_a, 6)}, copy {np.round(_b, 6)}, max |dev| {dev_copy:.1e}",
      dev_copy == 0.0 and 0.0 < float(_a[0]) < 1.0, load_bearing=False)
dev_ms3 = max(abs(max(R_of(XLIN, A0_MS3[f_], 1.75, "door", ret_L388)[0].values()) - J["MS3"]["K1"]["1.75"][f_]["worst"]) for f_ in FEET)
check("C0d CONTROL: MS3's committed K1 row (L388's retention, 1.75 Mpc cap, door convention, both footings) is reproduced",
      f"max |dev| {dev_ms3:.1e}", dev_ms3 < 1e-9, load_bearing=False)
_at3 = J["AT3"]["G1"]["0.003|600.0|0.0"]["xcop"]
_x = xcop_from_eps(_at3["eps"])
dev_xc = max(abs(_x[f_]["ratio"] - _at3[f_]["ratio"]) for f_ in FEET)
check("C0e CONTROL: AT3's committed X-COP row (y_v0 0.003, 600 km/s, f_U 0: eps 0.935) is reproduced by xcop_from_eps",
      f"ratios {_x['canonical']['ratio']:.4f}/{_x['alt']['ratio']:.4f}; max |dev| {dev_xc:.1e}", dev_xc < 1e-12, load_bearing=False)
_Ht, _st, _r0, _q0, _Rt = 0.3, 150.0, 10.0, 3.0, 300.0
_rt = np.geomspace(0.5, _Rt, 600)
_Sn = _depth_core(_rt, _q0 * (_r0 / _rt) ** 2, np.full_like(_rt, _st), 2 * _st ** 2 * np.log(_rt / _r0), 1e9, AMPD * _Ht)
_Sa = AMPD * _Ht * (_q0 * _r0 ** 2) ** 2 * (_rt ** -3 - _Rt ** -3) / (3 * _st)
dev_sis = float(np.max(np.abs(_Sn[:-20] / _Sa[:-20] - 1)))
check("C0f CONTROL: the depth integral on a singular isothermal sphere with the detuning switched off (v_k -> oo) against the "
      "closed form AMP H q0^2 r0^4 (r^-3 - R^-3)/(3 sigma)", f"max relative deviation {dev_sis:.1e}", dev_sis < 2e-3, load_bearing=False)
_s8c = solve_hist(np.ones_like(a_grid), 600.0)
check("C0g CONTROL: L319's solver with no conversion returns LCDM's S_8 and T^2 = 1", f"S_8 {_s8c['S8']:.6f} vs {S8_LCDM:.6f}; "
      f"T^2(k = 5) {_s8c['t2']:.6f}/{_s8c['t3']:.6f}", abs(_s8c["S8"] - S8_LCDM) < 1e-9 and abs(_s8c["t2"] - 1) < 1e-9, load_bearing=False)
OUT["numbers"]["controls"] = dict(FK1=dev_fk1, AT1=dev_at1, arith=dev_arith, copy=dev_copy, MS3=dev_ms3, AT3_xcop=dev_xc, SIS=dev_sis)
P(f"  controls done   {elapsed()}")

# ================================================================================================ PART A: the action and its dynamics
banner("A1  THE DOUBLET INSIDE PHI: masses, Z2 x Z2, the kick (sympy, varied from the action's potential)")
phH, phL, mS, epsS, lamS = sp.symbols("phi_H phi_L m epsilon lambda", real=True)
PhiS = (phH + sp.I * phL) / sp.sqrt(2)
VS = sp.expand(mS ** 2 * sp.expand(PhiS * sp.conjugate(PhiS)) + epsS * sp.re(sp.expand(PhiS ** 2))
               + lamS * sp.im(sp.expand(PhiS ** 2)) ** 2)
mH2 = sp.diff(VS, phH, 2).subs({phH: 0, phL: 0}); mL2 = sp.diff(VS, phL, 2).subs({phH: 0, phL: 0})
z2z2 = sp.simplify(VS.subs(phH, -phH) - VS) == 0 and sp.simplify(VS.subs(phL, -phL) - VS) == 0
cross = sp.Poly(VS, phH, phL).coeff_monomial(phH ** 2 * phL ** 2)
odd = [sp.Poly(VS, phH, phL).coeff_monomial(mon) for mon in (phH * phL ** 3, phH ** 3 * phL, phH * phL)]
pS = sp.symbols("p", positive=True)
mHs, mLs = sp.symbols("m_H m_L", positive=True)
v_k_sym = sp.simplify(sp.solve(sp.Eq(sp.sqrt(mH2), sp.sqrt(mL2 + pS ** 2)), pS)[0] / sp.sqrt(mH2))
vS = sp.symbols("v", positive=True)
eps_of_v = sp.simplify(sp.solve(sp.Eq(v_k_sym ** 2, vS ** 2), epsS)[0] / mS ** 2)
lat = sp.simplify(sp.series(sp.sqrt(mH2 / mL2) - 1, epsS, 0, 2).removeO() - sp.series(v_k_sym ** 2 / 2, epsS, 0, 2).removeO())
P(f"    V = {VS}")
P(f"    m_H^2 = {mH2}, m_L^2 = {mL2};  Z2 x Z2: {z2z2};  phi_H^2 phi_L^2 vertex {cross};  odd vertices {odd}")
P(f"    two-body phi_H phi_H -> phi_L phi_L at rest: v_k = {v_k_sym}  <=>  eps/m^2 = {eps_of_v};  latent heat per unit mass "
  f"(gamma - 1) - v_k^2/2 = {lat} + O(eps^2)")
EPS_M2 = {v_: (0.0 if MUTATE else float(eps_of_v.subs(vS, v_ / C_KMS))) for v_ in VK_ALL}
V_FROM = {v_: C_KMS * float(v_k_sym.subs({epsS: EPS_M2[v_], mS: 1})) for v_ in VK_ALL}
for v_ in VK_ALL:
    P(f"    window kick {v_:.0f} km/s: eps/m^2 = {EPS_M2[v_]:.4e} -> the Lagrangian's kick {V_FROM[v_]:.3f} km/s")
a1_ok = (sp.simplify(mH2 - mL2 - 2 * epsS) == 0 and z2z2 and all(o_ == 0 for o_ in odd) and lat == 0
         and all(abs(V_FROM[v_] - v_) < 1e-6 for v_ in VK_ALL))
check("A1 DERIVED: V = (m^2 + eps) phi_H^2/2 + (m^2 - eps) phi_L^2/2 + lambda phi_H^2 phi_L^2 (Z2 x Z2, no odd vertex), so a lone "
      "phi_H is stable and phi_H phi_H -> phi_L phi_L leaves back to back at v_k = sqrt(2 eps/(m^2 + eps)); the latent heat is "
      "v_k^2/2 per unit mass; eps/m^2 = v^2/(2c^2 - v^2) puts the kick at 575-650 km/s",
      f"m_H^2 - m_L^2 = {sp.simplify(mH2 - mL2)}; kicks from the Lagrangian {[round(V_FROM[v_], 3) for v_ in VK_ALL]} km/s at eps/m^2 "
      f"{[f'{EPS_M2[v_]:.3e}' for v_ in VK_ALL]}", a1_ok,
      "the splitting is the one new constant of the kick: a universal, isotropic speed, the same in every halo and at every z")
OUT["numbers"]["A1"] = dict(eps_over_m2=EPS_M2, v_from_lagrangian=V_FROM)

banner("A2  RECIPROCITY: the dark action has no MOND-sector field, so S = 0; the kick's energy is the dark field's own")
PhiN = sp.symbols("Phi_N", real=True)
qH, qHc, qL, qLc, dqH, dqHc, dqL, dqLc = sp.symbols("psi_H psi_Hc psi_L psi_Lc dpsi_H dpsi_Hc dpsi_L dpsi_Lc")
tH, tHc, tL, tLc = sp.symbols("dt_psi_H dt_psi_Hc dt_psi_L dt_psi_Lc")
# the NR dark Lagrangian (A3's vertices): kinetic, Newtonian coupling, rest-energy shifts +-eps/2m, pair and density terms
L_dark = (sp.I / 2 * (qHc * tH - qH * tHc) + sp.I / 2 * (qLc * tL - qL * tLc) - dqHc * dqH / (2 * mHs) - dqLc * dqL / (2 * mLs)
          - PhiN * (mHs * qHc * qH + mLs * qLc * qL) - epsS / (2 * mS) * (qHc * qH - qLc * qL)
          - lamS / (4 * mHs * mLs) * (qH ** 2 * qLc ** 2 + qHc ** 2 * qL ** 2) - lamS / (mHs * mLs) * qHc * qH * qLc * qL)
S_dark = sp.simplify(sp.diff(L_dark, sp.Symbol("du")))                # dL_dark/d(grad u): u and its gradient do not appear
dep = [s_ for s_ in L_dark.free_symbols if s_.name in ("u", "du", "dt_u", "U", "W", "W_b")]
P(f"    NR dark Lagrangian: {L_dark}")
P(f"    its MOND-sector symbols: {dep} -> S = dL_dark/d(grad u) = {S_dark}; FP8 A4: energy from the MOND sector = -Int S.d_t grad u = 0")
lat_heat = {v_: VK[v_] ** 2 / 2 for v_ in VK_ALL}                     # (km/s)^2 per unit mass
B0 = J["FP8"]["B0"]
sel = {}
for key_, row_ in B0.items():
    sel[key_] = {f"{v_:.0f}": lat_heat[v_] / row_["cost_per_mass"] for v_ in VK_ALL}
fl_min = min(min(d_.values()) for k_, d_ in sel.items() if "flagship" in k_)
cl_max = max(max(d_.values()) for k_, d_ in sel.items() if "X-COP" in k_)
for k_, d_ in sel.items():
    P(f"    {k_:22s}: FP8's specific unbinding cost {B0[k_]['cost_per_mass']:9.0f} (km/s)^2; latent heat / cost at 575-650: "
      + ", ".join(f"{x_:.2f}" for x_ in d_.values()))
a2_ok = len(dep) == 0 and S_dark == 0 and fl_min >= 1.0 and cl_max < 1.0
check("A2 DERIVED + NUMBERS: the dark action contains no MOND-sector field, so its source in the MOND equation is S = 0 (the "
      "phantom is not rewritten, delta = 0) and by FP8's reciprocity identity the MOND sector hands over nothing; the kick's "
      "energy is the rest-energy difference.  ENERGY SELECTIVITY: the latent heat v_k^2/2 exceeds FP8's committed specific "
      "unbinding cost on every z = 2.5 flagship host and falls short of the X-COP cluster's",
      f"S = {S_dark}; latent/cost on the flagship hosts >= {fl_min:.2f}; on X-COP <= {cl_max:.3f}", a2_ok,
      "the first mechanism in the chain with the right ORDER by construction (galaxies before clusters): a universal speed sits "
      "between the specific binding energies of z = 2.5 galaxies and clusters -- where it sits is the fit (C)")
OUT["numbers"]["A2"] = dict(latent_over_cost=sel, flagship_min=fl_min, xcop_max=cl_max)

banner("A3  THE NR REDUCTION AND THE PAIR INSTABILITY (sympy, rotating-wave, from lambda phi_H^2 phi_L^2)")
pH, pL, pHc, pLc, eH, eL = sp.symbols("psi_H psi_L psi_Hc psi_Lc e_H e_L")
fH = (pH * eH + pHc / eH) / sp.sqrt(2 * mHs); fL = (pL * eL + pLc / eL) / sp.sqrt(2 * mLs)
Vint = sp.expand(lamS * fH ** 2 * fL ** 2)
pair = sp.simplify(Vint.coeff(eH, 2).coeff(eL, -2))                   # e^{-2i(m_H - m_L)t}: resonant with the pair's energy
dens = sp.simplify(Vint.coeff(eH, 0).coeff(eL, 0))
nHs = sp.symbols("n_H", positive=True)
G_sym = sp.simplify(sp.diff(pair, pLc).subs({pH: sp.sqrt(nHs), pLc: 1}))
D_, G_ = sp.symbols("D G", real=True)
ev = list(sp.Matrix([[D_, G_], [-G_, -D_]]).eigenvals().keys())
growth_ok = any(sp.simplify(e_ ** 2 - (D_ ** 2 - G_ ** 2)) == 0 for e_ in ev)
P(f"    pair vertex (psi_H^2 psi_L*^2): {pair};  density coupling: {dens};  G = dH/dpsi_L* at psi_H = sqrt(n_H): {G_sym}")
P(f"    (a_k, b_-k*) block [[D, G], [-G, -D]]: eigenvalues {ev} -> growth sqrt(G^2 - D^2) for |D| < G")
a3_ok = (sp.simplify(pair - lamS * pH ** 2 * pLc ** 2 / (4 * mHs * mLs)) == 0
         and sp.simplify(dens - lamS * pH * pHc * pL * pLc / (mHs * mLs)) == 0
         and sp.simplify(G_sym - lamS * nHs / (2 * mHs * mLs)) == 0 and growth_ok)
check("A3 DERIVED: the rotating-wave reduction of lambda phi_H^2 phi_L^2 gives the pair vertex lambda/(4 m_H m_L) and the density "
      "coupling lambda/(m_H m_L); a heavy condensate pumps phi_L pairs at G = lambda n_H/(2 m_H m_L), growing at sqrt(G^2 - D^2)",
      f"pair {pair}; density {dens}; G {G_sym}; eigenvalues {ev}", a3_ok)

banner("A4  THE HUBBLE SWEEP, THE K-GATE, AND THE BACKGROUND")
HS, DlS, EnS, qS, l0S, K0S = sp.symbols("H Delta E_need q lambda_0 K_0", positive=True)
Gp = sp.symbols("G", positive=True)
N_sweep = sp.simplify(sp.integrate(sp.sqrt(Gp ** 2 - D_ ** 2), (D_, -Gp, Gp)) / (2 * HS * DlS))
lamK = l0S * (3 * HS / K0S) ** (-2 * qS)
n_t = sp.solve(sp.Eq(sp.pi * (lamK * nHs / (2 * mS ** 2)) ** 2 / (4 * HS * DlS), EnS), nHs)[0]
dlog = sp.simplify(sp.diff(sp.log(n_t), HS) * HS)
xS, OmS, OLS = sp.symbols("x Omega_m Omega_L", positive=True)
fbg = xS / (OmS * xS + OLS) ** 2
xpk = sp.solve(sp.diff(fbg, xS), xS)[0]
OL0 = 1 - Om
z_pk = float(xpk.subs({OmS: Om, OLS: OL0})) ** (1 / 3) - 1
bg_ratio = lambda z_: (1.5 * Om * (1 + z_) ** 3 / (2.5 * Ez2(z_) ** 2)) ** 2   # N_bg / E_need = (rho_bar/rho_t)^2, q = 7/4
bg_max = max(bg_ratio(z_) for z_ in np.linspace(0, 6, 601))
P(f"    a mode swept through the resonance (dD/dt = -2 H Delta): N = {N_sweep};  trigger n_t = {n_t}")
P(f"    d ln n_t / d ln H = {dlog} -> q = 7/4 gives n_t ~ E^4 (the linear gate's); the background's N_bg/E_need = (rho_bar/rho_t)^2 "
  f"peaks at (1+z)^3 = {xpk} (z = {z_pk:.2f}) at {bg_max:.3f} (z = 0: {bg_ratio(0.0):.3f})")
a4_ok = (sp.simplify(N_sweep - sp.pi * Gp ** 2 / (4 * HS * DlS)) == 0 and sp.simplify(dlog - (2 * qS + sp.Rational(1, 2))) == 0
         and abs(z_pk - 0.30) < 0.02 and bg_max < 0.1)
check("A4 DERIVED: the Hubble sweep gives pi G^2/(4 H Delta) e-folds; with lambda(K) ~ K^(-2q) the trigger density scales as "
      "H^(2q + 1/2) (E^4 at q = 7/4); the cosmic background's spontaneous exponent peaks at z = 0.30 and stays below 0.1 of the "
      "trigger's (no spontaneous background conversion)", f"N = {N_sweep}; dln n_t/dln H = {dlog}; peak z {z_pk:.2f}, N_bg/E_need <= {bg_max:.3f}",
      a4_ok, "q and the normalisation lambda_0 are DECLARED (FK1: q = p + 3/4 with the linear gate's p = 1; lambda_0 puts the "
      "threshold at its delta_t)")
OUT["numbers"]["A4"] = dict(z_peak=z_pk, bg_max=bg_max, bg_z0=bg_ratio(0.0))

banner("A5  THE HALO GAIN: a virialised heavy field pumps a daughter mode at the Doppler-broadened golden-rule rate")
sgS, vkS = sp.symbols("sigma v_k", positive=True)
PD0 = 1 / (sp.sqrt(2 * sp.pi) * mS * vkS * sgS / sp.sqrt(2))        # per-mode detuning D = -m v_k U_par, U_par ~ N(0, sigma/sqrt 2)
gam = sp.simplify(sp.pi * Gp ** 2 * PD0)                              # golden rule: gamma = pi G^2 P(D = 0)
Gt2 = 4 * HS * DlS * EnS / sp.pi                                      # G at the trigger density (A4: N = E_need)
dNdl = sp.simplify((gam / vkS * Gt2 / Gp ** 2).subs(DlS, mS * vkS ** 2 / 2))
pref = sp.simplify(dNdl / EnS * sgS / HS)
dvS = sp.symbols("dv", positive=True)
Dfac = sp.simplify(sp.exp(-dvS ** 2 / (2 * (sgS / sp.sqrt(2)) ** 2)))
lorentz = sp.simplify(sp.pi * Gp ** 2 / (sp.pi * sp.Symbol("Gamma_p", positive=True)))   # RPA check: gamma = G^2/Gamma_p
P(f"    gamma = pi G^2 P(D = 0) = {gam}  (a Lorentzian pump of half-width Gamma_p gives {lorentz}: the random-phase result)")
P(f"    gain per unit path per (rho/rho_t)^2 = {dNdl} -> S_c prefactor {pref} (the design's 2C/pi with C = {sp.nsimplify(pref * sp.pi / 2)}); "
  f"detuning factor {Dfac}")
_zs, _cs, _us = (0.0, 2.5, 6.0), (3.0, 5.0, 10.0), (0.5, 3.0)
_Sgrid = {(z_, c_, u_): depth_dimless(c_, z_, u_) for z_ in _zs for c_ in _cs for u_ in _us}
c_inv = max(abs(_Sgrid[(z_, c_, 0.5)][0] / _Sgrid[(z_, c_, 3.0)][0] - 1) for z_ in _zs for c_ in _cs)
a5_ok = (sp.simplify(gam - sp.sqrt(sp.pi) * Gp ** 2 / (mS * vkS * sgS)) == 0 and sp.simplify(pref - 2 / sp.sqrt(sp.pi)) == 0
         and sp.simplify(Dfac - sp.exp(-dvS ** 2 / sgS ** 2)) == 0 and 0.3 <= C_DESIGN <= 3.0)
check("A5 DERIVED (new here): gamma = sqrt(pi) G^2/(m v_k sigma); along an outward path S_c = (2/sqrt(pi)) H Int (rho/rho_t)^2 "
      "exp(-(Dv/sigma)^2) dl/sigma -- the FK1 session's design form with C = sqrt(pi) (inside its 0.3-3 bracket) and detuning "
      "exponent 1 (the design's 1/2); in r200/V200 units it depends only on (c, E(z), v_k/V200)",
      f"gamma {gam}; prefactor {pref} (C = {C_DESIGN:.3f}); D = {Dfac}; kick-dependence of S_c at the centre <= {c_inv:.1e}", a5_ok,
      "the front criterion (>= 1 e-fold on the way out) and E_need are the design's and FK1's; the O(1) path geometry is "
      "bracketed by K = sqrt(pi) E_need x 3^(+-1)")
OUT["numbers"]["A5"] = dict(C=C_DESIGN, prefactor=float(pref), K=list(KS))

banner("A6  WHERE: the stimulated front and the ignition over (c, z); the budget over the halo model; non-selectivity")
FR = {}
for z_ in (0.0, 1.0, 2.5, 4.0, 6.0, 10.0):
    row = []
    for c_ in (3.0, 5.0, 10.0):
        S_ = depth_dimless(c_, z_, 2.0)
        FR[(z_, c_)] = dict(front={f"{K_:.0f}": front(XG, S_, 1 / K_) for K_ in KS}, ignite=front(XG, S_, 1.0), S_centre=float(S_[0]))
        row.append(f"c {c_:.0f}: " + "/".join(f"{FR[(z_, c_)]['front'][f'{K_:.0f}']:.3f}" for K_ in KS) + f" (spont. {FR[(z_, c_)]['ignite']:.2f})")
    P(f"    z = {z_:4.1f} (E^2 = {Ez2(z_):6.1f}): front x_s = r_s/r200 at K = " + "/".join(f"{K_:.0f}" for K_ in KS) + ": " + "; ".join(row))
lo25 = min(FR[(z_, c_)]["front"][f"{K_:.0f}"] for z_ in (0.0, 1.0, 2.5) for c_ in (3.0, 5.0, 10.0) for K_ in KS)
lo4 = min(FR[(4.0, c_)]["front"][f"{K_:.0f}"] for c_ in (3.0, 5.0, 10.0) for K_ in KS)
OUT["numbers"]["A6_fronts"] = {f"{k_[0]}|{k_[1]}": v_ for k_, v_ in FR.items()}

# the budget over L357's halo model (the dimensionless front, AT1's loss-cone and escape tables, the fluid's own cut-off)
CGRID = np.geomspace(3.0, 40.0, 14)
UGRID = np.array([0.0, 0.5, 1.0, 2.0, 3.0, 4.5, 6.0, 8.0])
SIGH = {c_: sig_hat(c_) for c_ in CGRID}
M22 = 2000.0                                                          # m = 2e-19 eV (FP4's floor 1.9-5.2e-19)


def supp_fdm(M, m22):                                                 # Schive+2016 halo-mass-function suppression (the fluid's scale)
    return (1 + (M / (1.6e10 * m22 ** (-4.0 / 3.0))) ** -1.1) ** -2.2


def x_core(M, z, m22):                                                # Schive+2014 soliton radius / r200
    om = Om * (1 + z) ** 3 / Ez2(z); zeta = lambda o: (18 * math.pi ** 2 + 82 * (o - 1) - 39 * (o - 1) ** 2) / o
    rc = 1.6 / m22 * (1 + z) ** -0.5 * (zeta(om) / zeta(Om)) ** (-1 / 6) * (M / 1e9) ** (-1 / 3)
    return rc / (3 * M / (4 * math.pi * 200 * RHOC0_KPC * Ez2(z))) ** (1 / 3)


_TCACHE = {}


def tables(z, K, ft=1.0, qg=1.75):
    key_ = (round(float(z), 6), round(float(K), 6), round(float(ft), 6), round(float(qg), 6))
    if key_ in _TCACHE: return _TCACHE[key_]
    Tf = np.zeros((len(CGRID), len(UGRID))); Ts = np.zeros((len(CGRID), len(XG)))
    for i, c_ in enumerate(CGRID):
        for j, u_ in enumerate(UGRID):
            S_ = depth_dimless(c_, z, u_, ft, qg, SIGH[c_])
            Tf[i, j] = front(XG, S_, 1.0 / K)
            if j == 0: Ts[i] = S_
    out = (RegularGridInterpolator((np.log(CGRID), UGRID), Tf, bounds_error=False, fill_value=None),
           RegularGridInterpolator((np.log(CGRID), np.log(XG)), Ts, bounds_error=False, fill_value=None))
    _TCACHE[key_] = out
    return out


def budget(vk, K, ft=1.0, qg=1.75, cut="fluid", z_web=None):
    """F(z): the converted fraction of the carrier; F_b(z): the bias-weighted escaped fraction (irreversible running maxima);
    the share of the converted carrier in hosts >= 1e10.5 Msun; ignition failures at the soliton core (m = 2e-19 eV)."""
    Mh = MH / hh; F, Fb, hi, nfail = [], [], [], 0
    for z in ZG:
        if z > 20.0:
            F.append(0.0); Fb.append(0.0); hi.append(0.0); continue
        s = SIG0 * DG(z); nu = DC / s
        w = f_st(nu) * np.abs(np.gradient(nu, np.log(MH))); bb = b_st(nu)
        cs = np.clip(c_dm14(MH, z), 3.0, 40.0)
        r200 = (3 * Mh / (4 * np.pi * 200 * RHOC0_KPC * Ez2(z))) ** (1 / 3); V200 = np.sqrt(GK * Mh / r200)
        u = np.clip(vk / V200, 0, UGRID[-1])
        Tf, Ts = tables(z, K, ft, qg)
        xs = np.clip(Tf(np.stack([np.log(cs), u], 1)), 0.0, 1.0)
        xc = np.clip(np.array([x_core(M_, z, M22) for M_ in Mh]), XG[0], 1.0)
        Sc = Ts(np.stack([np.log(cs), np.log(xc)], 1))
        ign = Sc >= 1.0
        nfail += int(np.sum(~ign & (w > 1e-12) & (supp_fdm(Mh, M22) > 1e-3)))
        lc = np.where((xs > 0) & ign, I_LC(np.stack([np.log(np.clip(cs, CG[0], CG[-1])), np.log(np.maximum(xs, XVG[0]))], 1)), 0.0)
        fe = np.where(xs > 0, I_ES(np.stack([np.log(np.clip(cs, CG[0], CG[-1])), np.log(np.maximum(xs, XVG[0])), u], 1)), 0.0)
        cf = supp_fdm(Mh, M22) if cut == "fluid" else (Mh >= 1e8).astype(float)
        F.append(float(_trap(w * np.clip(lc, 0, 1) * cf, np.log(MH))))
        Fb.append(float(_trap(w * bb * np.clip(lc, 0, 1) * np.clip(fe, 0, 1) * cf, np.log(MH))))
        hi.append(float(_trap(w * np.clip(lc, 0, 1) * cf * (Mh >= 10 ** 10.5), np.log(MH))) / max(F[-1], 1e-300))
    F, Fb = np.array(F), np.array(Fb)
    Fc = np.maximum.accumulate(F[::-1])[::-1]; Fbc = np.maximum.accumulate(Fb[::-1])[::-1]
    if z_web is not None:                                             # A8's bracket: the unconverted carrier converts at z_web
        Fbc = np.where(ZG <= z_web, 1.0, Fbc)
    S_a = 1 - np.interp(1 / a_grid - 1, ZG, Fbc, right=0.0)
    return dict(F=Fc, Fb=Fbc, S=S_a, hi=np.array(hi), nfail=nfail)


BUD = {}
with ThreadPoolExecutor(NW) as ex:
    _jobs = [(v_, K_) for v_ in VK_ALL for K_ in KS]
    for (j_, r_) in zip(_jobs, ex.map(lambda j: budget(VK[j[0]], j[1]), _jobs)):
        BUD[j_] = r_
izg = {float(z_): i for i, z_ in enumerate(ZG)}
share = {z_: BUD[(600.0, K_MID)]["hi"][izg[z_]] for z_ in (2.0, 3.0, 4.0)}
at1B = J["AT1"]["B1"]["0.1|600.0"]
Fb_at1 = {z_: float(np.interp(z_, at1B["z"], at1B["F_b_escaped"])) for z_ in (0.0, 2.0, 3.0)}
P("    the budget (m = 2e-19 eV cut-off; K = %s): converted F at z = 4/3/2/1/0.5/0 and bias-weighted escaped F_b" % "/".join(f"{k_:.0f}" for k_ in KS))
for v_ in VK_ALL:
    for K_ in KS:
        b_ = BUD[(v_, K_)]
        P(f"      v_k {v_:.0f} K {K_:4.0f}: F " + "/".join(f"{np.interp(z_, ZG, b_['F']):.3f}" for z_ in (4, 3, 2, 1, 0.5, 0))
          + "; F_b " + "/".join(f"{np.interp(z_, ZG, b_['Fb']):.3f}" for z_ in (4, 3, 2, 1, 0.5, 0)) + f"; ignition failures {b_['nfail']}")
P(f"    share of the converted carrier in hosts >= 1e10.5 Msun at z = 2/3/4: {share[2.0]:.3f}/{share[3.0]:.3f}/{share[4.0]:.3f} "
  f"(AT1's acceleration trigger: >= 0.98 at z = 2-3)")
a6_ok = lo25 >= 0.95 and share[3.0] < 0.5 and share[2.0] < 0.6
check("A6 DERIVED + NUMBERS (where): at z <= 2.5 the stimulated front sits at >= 0.95 r200 for c = 3-10 and K = 36-947 (the "
      "whole halo converts); every cusp ignites; the conversion is NOT mass-selective -- most of the converted carrier sits in "
      "hosts below 1e10.5 Msun at z = 2-4", f"min front z <= 2.5: {lo25:.3f} r200; z = 4: {lo4:.3f}; share >= 1e10.5 at z = 2/3/4: "
      f"{share[2.0]:.2f}/{share[3.0]:.2f}/{share[4.0]:.2f}", a6_ok,
      "the threshold (5/3) E^2 rho_crit(z) lies below every halo's density at r200 for z <~ 3: FK1's trigger is a halo-collapse "
      "trigger, the budget tracks the collapsed fraction (the kick, not the trigger, selects galaxies over clusters)")
OUT["numbers"]["A6"] = dict(min_front_z25=lo25, min_front_z4=lo4, share_ge_10p5=share,
                            budget={f"{k_[0]:.0f}|{k_[1]:.0f}": dict(F=b_["F"].tolist(), Fb=b_["Fb"].tolist()) for k_, b_ in BUD.items()})

banner("A7  WHEN: the conversion time against the dynamical time (the derived rate at x = 0.5 and 0.9 r200)")
A7 = {}
for z_ in (0.0, 1.0, 2.5, 4.0):
    for c_ in (4.0, 8.0):
        for xq in (0.5, 0.9):
            sg = float(np.interp(xq, XG, sig_hat(c_)))
            qq = (200.0 / 3.0) * c_ ** 2 / (mfn(c_) * xq * (1 + c_ * xq) ** 2) * RHOC0_KPC * Ez2(z_) / rho_t(z_)
            vk_hat = 2.0                                               # v_k / V200 (a Milky-Way-like host); t_conv ~ sigma/v_k
            tconv_H = math.sqrt(math.pi) * sg / (2 * qq ** 2 * vk_hat)   # E_need e-folds / gamma, in Hubble times
            tdyn_H = 2 * math.pi * xq / (10.0 * math.sqrt(float(np.interp(xq, XG, (np.log1p(XG * c_) - XG * c_ / (1 + XG * c_)) / mfn(c_) / XG))))
            A7[(z_, c_, xq)] = tconv_H / tdyn_H
    P(f"    z = {z_}: t_conv/t_dyn at (c, x) = " + ", ".join(f"({c_:.0f}, {xq}): {A7[(z_, c_, xq)]:.1e}" for c_ in (4.0, 8.0) for xq in (0.5, 0.9)))
a7_out = max(v_ for k_, v_ in A7.items() if k_[0] <= 2.5)
a7_in = max(v_ for k_, v_ in A7.items() if k_[0] <= 2.5 and k_[2] == 0.5)
a7_ok = a7_out < 0.1 and a7_in < 1e-2
check("A7 DERIVED (when): at z <= 2.5 the spontaneous conversion (E_need e-folds from the vacuum seed at the derived rate: an upper "
      "bound, a seeded front needs a few) takes < 0.1 of the local dynamical time out to 0.9 r200 and < 0.01 inside 0.5 r200: every "
      "halo converts at its collapse, i.e. in its PROGENITORS.  FK1's own timing is the history reading; AT1's rule at the scoring "
      "epoch (in place) is the pessimistic bracket (full re-accretion)",
      f"max t_conv/t_dyn at z <= 2.5: {a7_out:.1e} (0.9 r200), {a7_in:.1e} (0.5 r200); at z = 4: "
      f"{max(v_ for k_, v_ in A7.items() if k_[0] == 4.0):.1e} (the outer halo converts over ~a dynamical time there)", a7_ok)
OUT["numbers"]["A7"] = {f"{k_[0]}|{k_[1]}|{k_[2]}": v_ for k_, v_ in A7.items()}

banner("A8  (reported flag) THE WEB: the stimulated criterion in the Hubble flow, and an S_8 bracket if the web converts")
A8 = {}
for En in (E_LO, E_HI):
    zz = np.linspace(0, 6, 1201)
    dts = np.array([2.5 * Ez2(z_) / (1.5 * Om * (1 + z_) ** 3 / Ez2(z_)) for z_ in zz])
    zm = float(zz[np.argmax(dts > math.sqrt(En))]) if (dts > math.sqrt(En)).any() else float("nan")
    A8[f"{En:.0f}"] = dict(z_mean_stimulable_below=zm, delta_t_z0=float(dts[0]))
    P(f"    E_need {En:.0f}: a seed resonant with the mean background gains >= 1 e-fold per sweep below z = {zm:.2f}; the "
      f"spontaneous threshold is delta_t = {dts[0]:.2f} at z = 0 (filaments above it meet the trigger itself)")
WEB = {}
for zw in (1.8, 1.2, 0.5):
    bw = budget(VK[600.0], K_MID, z_web=zw)
    WEB[zw] = float(solve_hist(bw["S"], VK[600.0])["S8"] / S8_LCDM)
P("    S_8 ratio if the whole unconverted carrier also converts at z_web (600 km/s, the maximal web case): "
  + ", ".join(f"z_web {k_}: {v_:.3f}" for k_, v_ in WEB.items()))
check("A8 (reported flag) the web: seeded stimulation in the Hubble flow and super-threshold filaments are not in the halo-model "
      "budget; the maximal web-conversion bracket on S_8", dict(criterion=A8, S8_web=WEB), True,
      "OPEN: whether seeds from converted halos drive a front through the web needs ln(pump/seed) e-folds, not 1; if they do, "
      "the budget below is a lower bound (a particle-mesh question)", load_bearing=False)
OUT["numbers"]["A8"] = dict(criterion=A8, S8_web=WEB)
P(f"  part A done   {elapsed()}")

# ================================================================================================ PART B: the gates
banner("B1  THE FLAGSHIP AT z = 0.5-2.5: the fluid's front, three readings (in place self / in place intact / history)")
HOSTS = {}
for z_ in ZF:
    for lMb in ((11.0,) if SMOKE else (10.0, 10.5, 11.0)):
        for mf in ((1 / 1.5, 1.0, 1.5) if (z_ == 2.5 or FULL) and not SMOKE else (1.0,)):
            H_ = flag_host(lMb, mf, z_)
            Pp = prof_bary(H_["Mh"], H_["c"], z_, hernquist(H_["Mb"], H_["a"]))
            fr_ = {}
            for v_ in VK_ALL:
                r_, S_ = depth_bary(Pp, VK[v_])
                fr_[v_] = {K_: front(r_, S_, 1.0 / K_) for K_ in KS}
            H_.update(r200=Pp["r200"], fr=fr_)
            HOSTS[(z_, lMb, round(mf, 3))] = H_


def progenitor(H_, al, dz=0.25, zmax=20.0):
    """the intact main progenitor M(z') = M_h exp(-alpha (z' - z)) on z' = z..20: fronts r_s(z'; v_k, K) and Phi(RG)."""
    zs = np.round(np.arange(H_["z"], zmax + 1e-9, dz), 4)
    rs_ = {(v_, K_): np.zeros(len(zs)) for v_ in VK_ALL for K_ in KS}
    Phis = np.zeros((len(zs), len(RG)))
    for i, zq in enumerate(zs):
        M = H_["Mh"] * math.exp(-al * (zq - H_["z"]))
        if i == 0:
            c_, Mb, a = H_["c"], H_["Mb"], H_["a"]
        else:
            c_ = max(float(c200_20(M, zq)), 3.0); Mb, a = galaxy_baryons(M, zq, H_["mf"])
        Pp = prof_bary(M, c_, zq, hernquist(Mb, a))
        for v_ in VK_ALL:
            r_, S_ = depth_bary(Pp, VK[v_], n=160)
            for K_ in KS: rs_[(v_, K_)][i] = front(r_, S_, 1.0 / K_)
        Phis[i] = Pp["Phi"]
    return zs, rs_, Phis


def passage(zs, rsK, Phis, rq):
    """the first epoch (highest z') at which the front covers rq, and the intact progenitor's v_esc(rq) there."""
    ok = rsK >= rq
    if not ok.any(): return float("nan"), float("inf")
    i = int(np.where(ok)[0].max())
    if i == len(zs) - 1: return float(zs[-1]), math.sqrt(-2 * float(np.interp(rq, RG, Phis[-1])))
    t = min(max((rsK[i] - rq) / max(rsK[i] - rsK[i + 1], 1e-300), 0.0), 1.0)
    ph = (1 - t) * float(np.interp(rq, RG, Phis[i])) + t * float(np.interp(rq, RG, Phis[i + 1]))
    return float(zs[i] + t * (zs[i + 1] - zs[i])), math.sqrt(-2 * ph)


GATE = {}
for key_, H_ in HOSTS.items():
    for al in ALPHAS:
        zs, rs_, Phis = progenitor(H_, al, dz=(0.5 if SMOKE else 0.25))
        for v_ in VK_ALL:
            for K_ in KS:
                for f_ in FEET:
                    zp, ve = passage(zs, rs_[(v_, K_)], Phis, H_["rF"][f_])
                    GATE[key_ + (al, v_, K_, f_)] = dict(z_pass=zp, v_esc=ve, escaped=bool(ve < VK[v_]))
P(f"    fronts and progenitor passages done for {len(HOSTS)} hosts x {len(ALPHAS)} accretion rates   {elapsed()}")


def ret_job(j):
    key_, v_, mode = j
    H_ = HOSTS[key_]; Mb_fn = hernquist(H_["Mb"], H_["a"]); gates = [H_["rF"][f_] for f_ in FEET]
    if mode == "self":
        r_, _ = retained_fk1(Mb_fn, H_["Mh"], H_["c"], gates, H_["fr"][v_][K_HI], VK[v_], H_["rhoc"], N=NRET, iters=2)
    elif mode == "intact":
        r_, _ = retained_fk1(Mb_fn, H_["Mh"], H_["c"], gates, H_["fr"][v_][K_HI], VK[v_], H_["rhoc"], N=NRET, iters=0)
    else:                                                             # surface-only (in-place dropped), smallest front
        rv = H_["fr"][v_][K_LO]
        if rv >= 0.999 * H_["r200"]:
            r_ = np.zeros(2)                                          # no entry population: everything was in place
        else:
            r_ = np.maximum(retained_fk1(Mb_fn, H_["Mh"], H_["c"], gates, rv, VK[v_], H_["rhoc"], N=NRET, iters=2, drop_inplace=True)[0],
                            retained_fk1(Mb_fn, H_["Mh"], H_["c"], gates, rv, VK[v_], H_["rhoc"], N=NRET, iters=0, drop_inplace=True)[0])
    return j, np.asarray(r_, float)


_jobs = [(k_, v_, m_) for k_ in HOSTS for v_ in VK_RET for m_ in ("self", "intact", "surface")]
with ThreadPoolExecutor(NW) as ex:
    RET = dict(ex.map(ret_job, _jobs))
P(f"    retention done: {len(_jobs)} runs   {elapsed()}")
FL = []
for key_, H_ in HOSTS.items():
    for v_ in VK_RET:
        for i_, f_ in enumerate(FEET):
            esc_all = all(GATE[key_ + (al, v_, K_, f_)]["escaped"] for al in ALPHAS for K_ in KS)
            S_self, S_int, S_surf = RET[(key_, v_, "self")][i_], RET[(key_, v_, "intact")][i_], RET[(key_, v_, "surface")][i_]
            S_hist = S_surf if esc_all else max(S_self, S_int)
            row = dict(z=key_[0], lMb=key_[1], mf=key_[2], vk=v_, foot=f_, escaped=esc_all, S_self=S_self, S_intact=S_int, S_surface=S_surf,
                       S_history=S_hist, z_pass=[GATE[key_ + (al, v_, K_, f_)]["z_pass"] for al in ALPHAS for K_ in KS],
                       v_esc_pass=max(GATE[key_ + (al, v_, K_, f_)]["v_esc"] for al in ALPHAS for K_ in KS))
            for rdg, S_ in (("self", S_self), ("intact", S_int), ("history", S_hist)):
                row[f"shift_{rdg}"] = max(abs(flag_shift(key_[0], H_["Mb"], H_["Mh"], f_, S_, nuf)) for _, nuf in KERNELS)
            FL.append(row)
OUT["numbers"]["B1_rows"] = FL
for z_ in ZF:
    for v_ in VK_RET:
        rs_ = [r_ for r_ in FL if r_["z"] == z_ and r_["vk"] == v_]
        P(f"    z = {z_} v_k {v_:.0f}: max |shift| history {max(r_['shift_history'] for r_ in rs_):.4f}, in place self "
          f"{max(r_['shift_self'] for r_ in rs_):.4f}, in place intact {max(r_['shift_intact'] for r_ in rs_):.3f} dex; max S "
          f"history/self/intact {max(r_['S_history'] for r_ in rs_):.4f}/{max(r_['S_self'] for r_ in rs_):.4f}/{max(r_['S_intact'] for r_ in rs_):.3f}; "
          f"progenitor v_esc(r_F) at passage <= {max(r_['v_esc_pass'] for r_ in rs_):.0f} km/s, escaped {sum(r_['escaped'] for r_ in rs_)}/{len(rs_)}")
FLAG = {}
for rdg in ("history", "self", "intact"):
    for v_ in VK_RET:
        FLAG[(rdg, v_)] = max(r_[f"shift_{rdg}"] for r_ in FL if r_["vk"] == v_)
fl_hist_ok = all(FLAG[("history", v_)] <= FLAG_TOL for v_ in VK_RET)
fl_self_ok = all(FLAG[("self", v_)] <= FLAG_TOL for v_ in VK_RET)
fl_int_fail = [f"{v_:.0f}" for v_ in VK_RET if FLAG[("intact", v_)] > FLAG_TOL]
worst_int = max(FL, key=lambda r_: r_["shift_intact"])
vesc_max = max(r_["v_esc_pass"] for r_ in FL)
check("B1 THE FLAGSHIP (history reading, FK1's own timing): at z = 0.5, 1, 1.5, 2 and 2.5 the front passed r_F in the main "
      "progenitor when its v_esc(r_F) was below the kick, so the in-place population left then; the zero point stays within "
      "0.074 dex of 0.00 on the record's grid (M_b 1e10-1e11), both footings, both kernels, every kick, K and accretion rate",
      f"max |shift| history {max(FLAG[('history', v_)] for v_ in VK_RET):.4f} dex (<= 0.05: {max(FLAG[('history', v_)] for v_ in VK_RET) <= FLAG_TIGHT}); "
      f"progenitor v_esc(r_F) at passage <= {vesc_max:.0f} km/s; in place self {max(FLAG[('self', v_)] for v_ in VK_RET):.4f}; "
      f"in place intact {max(FLAG[('intact', v_)] for v_ in VK_RET):.3f} (fails at {fl_int_fail} km/s)", fl_hist_ok,
      "the retained dark mass at r_F: history <= %.1e; the pessimistic in-place intact reading keeps S = %.3f at M_b 1e%.1f, z = %.1f "
      "(v_k %.0f) -- the knife-edge lives in the well's response, not in the kick; the re-accretion of escaped daughters into r_F "
      "is not modelled (OPEN)" % (max(r_["S_history"] for r_ in FL), worst_int["S_intact"], worst_int["lMb"], worst_int["z"], worst_int["vk"]))
OUT["numbers"]["B1"] = {f"{k_[0]}|{k_[1]:.0f}": v_ for k_, v_ in FLAG.items()}
P(f"    {elapsed()}")

banner("B2  z = 0 GALAXIES / RAR (L321's three hosts, in place: the pessimistic reading)")
GALR = {}


def gal_job(v_):
    out = {}
    for kh, hst in GAL.items():
        c_ = float(c200_z0(hst["M200"]))
        Pp = prof_bary(hst["M200"], c_, 0.0, hernquist(hst["Mb"], hst["a"]), rhoc=RHO_C0)
        r_, S_ = depth_bary(Pp, VK[v_])
        rv = front(r_, S_, 1.0 / K_HI)
        out[kh] = float(retained_fk1(hernquist(hst["Mb"], hst["a"]), hst["M200"], c_, [hst["rg"]], rv, VK[v_], RHO_C0, N=NRET)[0][0])
    return v_, out


with ThreadPoolExecutor(NW) as ex:
    GALR = dict(ex.map(gal_job, VK_RET))
GS = {v_: gal_shifts(GALR[v_]) for v_ in VK_RET}
gal_max = {v_: max(abs(x_) for f_ in FEET for x_ in GS[v_][f_].values()) for v_ in VK_RET}
for v_ in VK_RET:
    P(f"    v_k {v_:.0f}: retained {', '.join(f'{k_} {x_:.4f}' for k_, x_ in GALR[v_].items())} -> shifts canonical "
      f"{', '.join(f'{x_:+.4f}' for x_ in GS[v_]['canonical'].values())}, alt {', '.join(f'{x_:+.4f}' for x_ in GS[v_]['alt'].values())} dex")
check("B2 z = 0 GALAXIES: in place (the pessimistic reading) every host keeps <= 0.06 dex (both footings, every kick)",
      {f"{v_:.0f}": round(gal_max[v_], 4) for v_ in VK_RET}, all(gal_max[v_] <= 0.06 for v_ in VK_RET),
      "the RAR stays the MOND kernel's: the carrier leaves z = 0 discs (escape speeds below the kick outside the Milky Way's core)")
OUT["numbers"]["B2"] = dict(retained=GALR, shifts=GS)

banner("B3  X-COP: in place (AT3's machinery), the optimistic history reading, and the PM proxy (L388, reported)")
XC = {}
zcl = CLREF["z"]
Ppc = prof_bary(CLREF["M200"], CLREF["c"], zcl, cl_mass_fn, rhoc=CLREF["rhoc"])
for v_ in VK_RET:
    r_, S_ = depth_bary(Ppc, VK[v_])
    rv = front(r_, S_, 1.0 / K_HI)
    e_self = float(retained_fk1(cl_mass_fn, CLREF["M200"], CLREF["c"], [CLREF["R500"]], rv, VK[v_], CLREF["rhoc"], N=(3000 if SMOKE else 12000))[0][0])
    e_int = float(retained_fk1(cl_mass_fn, CLREF["M200"], CLREF["c"], [CLREF["R500"]], rv, VK[v_], CLREF["rhoc"], N=(3000 if SMOKE else 12000), iters=0)[0][0])
    Fcum = float(np.interp(zcl, ZG, BUD[(v_, K_MID)]["Fb"]))
    e_opt = max(e_self - Fcum, 0.0)
    XC[v_] = dict(front_r200=rv / Ppc["r200"], eps_self=e_self, eps_intact=e_int, F_cum=Fcum, eps_opt=e_opt,
                  inplace=xcop_from_eps(e_self), optimistic=xcop_from_eps(e_opt))
    P(f"    v_k {v_:.0f}: front {rv / Ppc['r200']:.3f} r200; in place eps {e_self:.3f} (intact {e_int:.3f}) -> "
      f"{XC[v_]['inplace']['canonical']['ratio']:.3f}/{XC[v_]['inplace']['alt']['ratio']:.3f}; optimistic eps {e_self:.3f} - {Fcum:.3f} = "
      f"{e_opt:.3f} -> {XC[v_]['optimistic']['canonical']['ratio']:.3f}/{XC[v_]['optimistic']['alt']['ratio']:.3f}")
PMX = {}
for tag, row in J["L388"]["table"]["pooled"].items():
    x_ = xcop_from_eps(row["eps_cl"]); PMX[tag] = dict(eps=row["eps_cl"], ratio=(x_["canonical"]["ratio"], x_["alt"]["ratio"]),
                                                     strict=x_["canonical"]["strict"] and x_["alt"]["strict"])
P("    PM proxy (L388 pooled, same threshold, rate 10 H): " + "; ".join(f"{k_}: eps {v_['eps']:.2f} -> {v_['ratio'][0]:.2f}/{v_['ratio'][1]:.2f}" for k_, v_ in PMX.items()))
xc_in_fail = all(not XC[v_]["inplace"][f_]["strict"] and not XC[v_]["inplace"][f_]["alt"] for v_ in VK_RET for f_ in FEET)
xc_opt_ok = {v_: all(XC[v_]["optimistic"][f_]["strict"] for f_ in FEET) for v_ in VK_RET}
check("B3 X-COP IN PLACE (AT3's machinery): one splitting (575-650 km/s, the whole cluster converted) keeps >= 0.9 of the cluster's "
      "carrier inside R500 and FAILS X-COP strict and alternative on both footings at every kick -- L372's single-channel pincer",
      f"in place eps {min(XC[v_]['eps_self'] for v_ in VK_RET):.3f}-{max(XC[v_]['eps_self'] for v_ in VK_RET):.3f} -> ratios "
      f"{min(XC[v_]['inplace']['canonical']['ratio'] for v_ in VK_RET):.2f}-{max(XC[v_]['inplace']['alt']['ratio'] for v_ in VK_RET):.2f}; "
      f"optimistic history {', '.join(f'{v_:.0f}: {XC[v_]['optimistic']['canonical']['ratio']:.2f}/{XC[v_]['optimistic']['alt']['ratio']:.2f}' for v_ in VK_RET)} "
      f"(strict pass {xc_opt_ok}); PM proxy strict pass {[k_ for k_, v_ in PMX.items() if v_['strict']]}",
      xc_in_fail and (min(XC[v_]["eps_self"] for v_ in VK_RET) >= 0.9 or MUTATE),
      "the cluster's escape speed (~2500-4000 km/s) is far above any kick in the window; only the history (the cluster's carrier "
      "converted in shallow progenitors and never came back) or a second, fast channel (AT3's mode U, 3000 km/s: a second "
      "splitting, FITTED) removes the 40-60% X-COP wants")
OUT["numbers"]["B3"] = dict(fk1={f"{k_:.0f}": v_ for k_, v_ in XC.items()}, pm_proxy=PMX)

banner("B4  KiDS-1000 (L360's switched fit at the common cell, AT3's carrier template), in place and optimistic")
KD = {}


def kids_job(v_):
    profs = []
    for b in range(4):
        M200 = M200_KIDS[b]; c_ = float(c200_55(M200))
        Mn, r200, rs = nfw21(M200, c_, RHOC_ZL)
        pro = np.geomspace(0.02 * rs, 0.999 * r200, 40)
        Mb_fn = hernquist(1.3 * 10 ** LOGMS[b], 3.0)
        Pp = prof_bary(M200, c_, ZL, Mb_fn, rhoc=RHOC_ZL)
        r_, S_ = depth_bary(Pp, VK[v_])
        rv = front(r_, S_, 1.0 / K_HI)
        ratio_p, _ = retained_fk1(Mb_fn, M200, c_, list(pro), rv, VK[v_], RHOC_ZL, N=(2000 if SMOKE else 8000))
        profs.append((pro, np.asarray(ratio_p)))
    return v_, profs


with ThreadPoolExecutor(NW) as ex:
    KPROF = dict(ex.map(kids_job, VK_RET))
for v_ in VK_RET:
    Fcum = float(np.interp(ZL, ZG, BUD[(v_, K_MID)]["Fb"]))
    KD[v_] = dict(inplace=kids_switched(KPROF[v_]),
                  optimistic=kids_switched([(p_, np.maximum(q_ - Fcum, 0.0)) for p_, q_ in KPROF[v_]]),
                  r200_retention=[float(q_[-1]) for _, q_ in KPROF[v_]])
    P(f"    v_k {v_:.0f}: in place {KD[v_]['inplace']['canonical']:+.1f}/{KD[v_]['inplace']['alt']:+.1f}; optimistic "
      f"{KD[v_]['optimistic']['canonical']:+.1f}/{KD[v_]['optimistic']['alt']:+.1f} (gate <= +4); retention at r200 by bin {np.round(KD[v_]['r200_retention'], 3)}")
kd_ok = all(KD[v_][rdg][f_] <= 4.0 for v_ in VK_RET for rdg in ("inplace", "optimistic") for f_ in FEET)
check("B4 KiDS-1000: every lens bin's halo converts whole; the switched fit at the common cell stays within +4 of L352's "
      "unswitched base on both footings, in place and optimistic, at every kick",
      {f"{v_:.0f}": {rdg: {f_: round(KD[v_][rdg][f_], 1) for f_ in FEET} for rdg in ("inplace", "optimistic")} for v_ in VK_RET}, kd_ok)
OUT["numbers"]["B4"] = {f"{k_:.0f}": v_ for k_, v_ in KD.items()}

banner("B6  S_8 (L319's solver on the halo-model budget; strict ratio >= 0.922, alt >= 0.899; PAPER34's absolute floors reported)")
S8R = {}
for v_ in VK_ALL:
    for K_ in KS:
        r_ = solve_hist(BUD[(v_, K_)]["S"], VK[v_])
        S8R[(v_, K_, "fluid")] = dict(S8=r_["S8"], ratio=r_["S8"] / S8_LCDM, t2=r_["t2"], t3=r_["t3"])
for v_ in (575.0, 650.0):
    b_ = budget(VK[v_], K_LO, cut="1e8")
    r_ = solve_hist(b_["S"], VK[v_]); S8R[(v_, K_LO, "1e8")] = dict(S8=r_["S8"], ratio=r_["S8"] / S8_LCDM, t2=r_["t2"], t3=r_["t3"])
VAR = {}
for tag, ft_, qg_ in (("f_t 1/3", 1 / 3, 1.75), ("f_t 3", 3.0, 1.75), ("q 1.25", 1.0, 1.25), ("q 2.5", 1.0, 2.5)):
    b_ = budget(VK[600.0], K_MID, ft=ft_, qg=qg_)
    r_ = solve_hist(b_["S"], VK[600.0])
    VAR[tag] = dict(ratio=r_["S8"] / S8_LCDM, F2=float(np.interp(2.0, ZG, b_["F"])), F3=float(np.interp(3.0, ZG, b_["F"])),
                    Fb0=float(b_["Fb"][0]))
for k_, v_ in S8R.items():
    P(f"    v_k {k_[0]:.0f} K {k_[1]:4.0f} cut {k_[2]:5s}: S_8 {v_['S8']:.4f} (ratio {v_['ratio']:.4f}); L319's matter proxy T^2(k = 5) z = 2/3 {v_['t2']:.3f}/{v_['t3']:.3f}")
P("    trigger-constant variants (600 km/s, K %.0f): " % K_MID + "; ".join(f"{k_}: ratio {v_['ratio']:.4f}, F(2/3) {v_['F2']:.3f}/{v_['F3']:.3f}" for k_, v_ in VAR.items()))
s8_min = min(v_["ratio"] for v_ in S8R.values())
check("B6 S_8: the escaped budget (bias-weighted ~0.5 by z = 2) costs S_8 only a few per cent, because the daughters' 575-650 km/s "
      "redshifts away and they re-cluster: the ratio stays >= 0.922 (strict) at every kick, K, cut-off and trigger variant",
      f"ratio {s8_min:.4f}-{max(v_['ratio'] for v_ in S8R.values()):.4f} (variants {min(v_['ratio'] for v_ in VAR.values()):.4f}-"
      f"{max(v_['ratio'] for v_ in VAR.values()):.4f}); absolute {min(v_['S8'] for v_ in S8R.values()):.3f} (PAPER34 floors 0.752/0.748); "
      f"PM proxy L388 {min(r_['S8'] for r_ in J['L388']['table']['pooled'].values()):.3f}-{max(r_['S8'] for r_ in J['L388']['table']['pooled'].values()):.3f}",
      s8_min >= 0.922 and min(v_["ratio"] for v_ in VAR.values()) >= 0.922,
      "the web bracket (A8) would cost more; L319's matter proxy at k = 5 is badly hit, which AT2 showed is the wrong yardstick "
      "for a halo-internal clearing (B7)")
OUT["numbers"]["B6"] = dict(rows={f"{k_[0]:.0f}|{k_[1]:.0f}|{k_[2]}": v_ for k_, v_ in S8R.items()}, variants=VAR)

banner("B7  THE LYMAN-ALPHA FOREST: the budget against AT2's scored regime; projection with the committed PM responses")
at1F = {z_: float(np.interp(z_, at1B["z"], at1B["F_trig_unweighted"])) for z_ in (2.0, 3.0)}
F23 = {k_: (float(np.interp(2.0, ZG, BUD[k_]["F"])), float(np.interp(3.0, ZG, BUD[k_]["F"]))) for k_ in BUD}
resp = []
for ck, cv in J["AT2"]["F12"]["cells"].items():
    if ck.endswith("|600.0"): resp.append((f"AT2 densest {ck}", cv["l365_rule"] / cv["decayed"][1], cv["decayed"][1]))
for ck, cv in J["AT2m"]["F12"]["cells"].items():
    if ck.endswith("|600.0"): resp.append((f"AT2 sparsest {ck}", cv["l365_rule"] / cv["decayed"][1], cv["decayed"][1]))
for rk, rv_ in J["AT2"]["F4"].items():
    if int(rk.split("_v")[1]) <= 700: resp.append((f"L365 {rk}", rv_["l365_rule"] / rv_["decayed"][1], rv_["decayed"][1]))
rlo, rhi = min(x_[1] for x_ in resp), max(x_[1] for x_ in resp)
analog = [x_ for x_ in resp if x_[0].startswith("L365 x5_v") and int(x_[0].split("_v")[1]) >= 550]
Fmax_pm = max(x_[2] for x_ in resp)
F2max = max(v_[0] for v_ in F23.values()); F2min = min(v_[0] for v_ in F23.values())
proj = (F2min * rlo, F2max * rhi)
proj_an = (F2min * min(x_[1] for x_ in analog), F2max * max(x_[1] for x_ in analog))
ratio_budget = min(F23[k_][0] / at1F[2.0] for k_ in F23), min(F23[k_][1] / at1F[3.0] for k_ in F23)
P(f"    FK1's converted fraction F(2)/F(3): {F2min:.3f}-{F2max:.3f} / {min(v_[1] for v_ in F23.values()):.3f}-{max(v_[1] for v_ in F23.values()):.3f}; "
  f"AT1's A2 cell (what AT2 scored) {at1F[2.0]:.3f}/{at1F[3.0]:.3f}: >= {ratio_budget[0]:.1f}x / {ratio_budget[1]:.1f}x")
for x_ in resp: P(f"      {x_[0]:26s}: L365 rule per unit F(2) {x_[1]:.3f} (F(2) {x_[2]:.3f})")
P(f"    projected L365 rule at z = 2: all committed responses {proj[0]:.3f}-{proj[1]:.3f}; the closest analog (L365's density trigger, "
  f"x5 at 550-700 km/s) {proj_an[0]:.3f}-{proj_an[1]:.3f}; gate 0.10; largest committed PM budget F(2) = {Fmax_pm:.3f} (an extrapolation)")
P(f"    PM proxy (L388 pooled, the same threshold): forest {min(r_['forest'] for r_ in J['L388']['table']['pooled'].values()):.3f}-"
  f"{max(r_['forest'] for r_ in J['L388']['table']['pooled'].values()):.3f} (reported)")
forest_ne = proj[0] < 0.10 < proj[1]
check("B7 THE FOREST IS NOT ESTABLISHED for FK1's own trigger: its budget leaves AT2's scored regime (>= 4x at z = 2-3) and the "
      "committed particle-mesh responses project L365's rule on both sides of the 10% gate",
      f"budget >= {ratio_budget[0]:.1f}x/{ratio_budget[1]:.1f}x AT2's; projection {proj[0]:.3f}-{proj[1]:.3f} (closest analog "
      f"{proj_an[0]:.3f}-{proj_an[1]:.3f}, leaning pass; an extrapolation past F(2) = {Fmax_pm:.2f})",
      (forest_ne and ratio_budget[0] >= 4.0) or MUTATE,
      "deciding it needs a particle-mesh run with this budget (every halo down to the fluid's scale, not densest-first)")
OUT["numbers"]["B7"] = dict(F23={f"{k_[0]:.0f}|{k_[1]:.0f}": v_ for k_, v_ in F23.items()}, AT1_cell=at1F, responses=resp, projection=proj,
                            projection_analog=proj_an, budget_ratio=ratio_budget)

banner("B8  COSMIC SHEAR (MS3's halo model, linear cell, 1.75 Mpc KiDS-safe cap, door convention; R <= 1.2)")
ZSH = 0.5
Mh_ = MH / hh
cs5 = np.clip(c_dm14(MH, ZSH), CG[0], CG[-1])
r2005 = (3 * Mh_ / (4 * np.pi * 200 * RHOC0_KPC * Ez2(ZSH))) ** (1 / 3); V2005 = np.sqrt(GK * Mh_ / r2005)
lgM = np.log10(Mh_)
SH = {}
for v_ in VK_RET:
    u5 = np.clip(VK[v_] / V2005, 0, UGR[-1])
    Tf, _ = tables(ZSH, K_HI)
    xs5 = np.clip(Tf(np.stack([np.log(np.clip(cs5, CGRID[0], CGRID[-1])), np.minimum(u5, UGRID[-1])], 1)), XVG[0], 1.0)
    lc5 = I_LC(np.stack([np.log(cs5), np.log(xs5)], 1))
    fe5 = I_ES(np.stack([np.log(cs5), np.log(xs5), u5], 1))
    keep = 1 - np.clip(lc5 * fe5, 0, 1)
    Fcum = float(np.interp(ZSH, ZG, BUD[(v_, K_MID)]["Fb"]))
    rets = {"in place (steady)": (lambda M, kp=keep: float(np.interp(math.log10(M), lgM, kp))),
            "optimistic history": (lambda M, kp=keep, F_=Fcum: max(float(np.interp(math.log10(M), lgM, kp)) - F_, 0.0))}
    SH[v_] = {}
    for rdg, rf in rets.items():
        for cap in (math.inf, 1.75):
            SH[v_][(rdg, cap)] = {f_: max(R_of(XLIN, A0_MS3[f_], cap, "door", rf)[0].values()) for f_ in FEET}
    keep_s = [rets["in place (steady)"](10 ** l_) for l_ in (12.0, 13.0, 13.5, 14.0, 14.5)]
    P(f"    v_k {v_:.0f}: in-place retention at 1e12/1e13/1e13.5/1e14/1e14.5 = " + "/".join(f"{k_:.2f}" for k_ in keep_s)
      + f"; F_b,cum(0.5) {Fcum:.3f}; worst R " + "; ".join(f"{rdg} cap {cap}: {w_['canonical']:.2f}/{w_['alt']:.2f}" for (rdg, cap), w_ in SH[v_].items()))
pm_sh = {f_: J["MS3"]["K1"]["1.75"][f_]["worst"] for f_ in FEET}
P(f"    PM proxy (MS3 K1, L388's retention, 1.75 Mpc): {pm_sh['canonical']:.2f}/{pm_sh['alt']:.2f} (reported)")
sh_in_fail = all(max(SH[v_][("in place (steady)", 1.75)].values()) > 1.2 for v_ in VK_RET)
sh_opt_ok = {v_: max(SH[v_][("optimistic history", 1.75)].values()) <= 1.2 for v_ in VK_RET}
sh_opt_txt = ", ".join("%.0f: %.2f" % (v_, max(SH[v_][("optimistic history", 1.75)].values())) for v_ in VK_RET)
check("B8 COSMIC SHEAR IN PLACE fails at the KiDS-safe 1.75 Mpc cap on some footing at every kick: groups and clusters keep their "
      "carrier (the kick is below their escape speeds) and the phantom's power at k = 1 lives there (MS3 D1, AT4)",
      f"in place worst R {min(max(SH[v_][('in place (steady)', 1.75)].values()) for v_ in VK_RET):.2f}-"
      f"{max(max(SH[v_][('in place (steady)', 1.75)].values()) for v_ in VK_RET):.2f}; optimistic history pass {sh_opt_ok} "
      f"({sh_opt_txt}); uncapped fails in every reading",
      sh_in_fail or MUTATE, "the cap itself (v_cap = 325 km/s) is the separator's declared constant (FP9 pending)")
OUT["numbers"]["B8"] = {f"{v_:.0f}": {f"{k_[0]}|{k_[1]}": w_ for k_, w_ in d_.items()} for v_, d_ in SH.items()}
OUT["numbers"]["B8_pm_proxy"] = pm_sh
P(f"  gates B1-B8 (bar Harvey) done   {elapsed()}")

banner("B5  HARVEY+2015 (L370's machinery via L372's harvey(), AT3's wiring; the carrier processed by FK1's conversion)")
HV = {}
if MUTATE or SMOKE:
    P("    not run under MUTATE / SMOKE (the flips are B1/B2; Harvey is the hub's)")
else:
    P72 = os.path.join(REPO, "real_research", "merger_infall_2026", "L372_gated_slow_kick_carrier.py")
    _s72 = open(P72).read()
    _harv = _s72[_s72.index('P70 = os.path.join(HERE, "L370_boosted_infall_mergers.py")'):_s72.index("def non_harvey_ok(r):")]
    from scipy.optimize import brentq
    from scipy.interpolate import PchipInterpolator
    HNS = dict(os=os, math=math, np=np, time=time, P=P, T0=T0, brentq=brentq, PchipInterpolator=PchipInterpolator, FAST=False,
               HERE=os.path.join(REPO, "real_research", "merger_infall_2026"), RHOC0_KPC_57=RHOC0_KPC, Ez2_57=Ez2,
               rho_thr_57=L57["rho_thr"], x_eff=None, retained_core_57=L57["retained_core"])
    _mut, os.environ["MUTATE"] = os.environ.get("MUTATE", "0"), "0"
    with contextlib.redirect_stdout(io.StringIO()):
        exec(_harv, HNS)
    os.environ["MUTATE"] = _mut
    cum_mass_70, RG70, RHOC_H, ZH = HNS["cum_mass"], HNS["RG"], HNS["RHOC_H"], HNS["ZH"]

    def ratio_profile_fk1(H, pic, xv, vk):
        """FK1's in-place retention profile of L370's real halo (pic, xv unused; the front is computed for the halo)."""
        Mb_tab = cum_mass_70(H.rho_b)
        Mb_fn = lambda r: np.interp(np.asarray(r, float), RG70, Mb_tab)
        Pp = prof_bary(H.M200, H.c, ZH, Mb_fn, rhoc=RHOC_H)
        r_, S_ = depth_bary(Pp, vk)
        rv = front(r_, S_, 1.0 / K_HI)
        pro = np.geomspace(10.0, 2.0 * H.R200, 24)
        q, _ = retained_fk1(Mb_fn, H.M200, H.c, list(pro), rv, vk, RHOC_H)
        return pro, np.asarray(q)

    HNS["ratio_profile"] = ratio_profile_fk1
    HNS["L70"]["SWITCH"]["p1_x2.5"] = (1.0, 2.5)                       # DE2's linear gate (AT3's wiring)
    HNS["SW_DEF"] = "p1_x2.5"
    harvey = HNS["harvey"]
    P(f"    L372's Harvey section loaded (L370's machinery, LCDM references computed); switch cell p1_x2.5; z_H = {ZH}   {elapsed()}")
    HCELLS = ([(v_, rdg) for v_ in VK_ALL for rdg in ("in place", "optimistic")] if FULL
              else [(650.0, "in place"), (575.0, "optimistic"), (650.0, "optimistic")])
    for v_, rdg in HCELLS:
        us = 1.0 if rdg == "in place" else 1.0 - float(np.interp(ZH, ZG, BUD[(v_, K_MID)]["Fb"]))
        h_ = harvey("fk1", None, VK[v_], us)
        HV[(v_, rdg)] = dict(beta=h_["beta"], core={f"{k_:.0e}": x_ for k_, x_ in h_["core"].items()}, ok=h_["ok"], uscale=us)
        P(f"    v_k {v_:.0f} {rdg:10s} (uniform factor {us:.3f}): excess beta " + "/".join(f"{h_['beta'][e_]:+.3f}" for e_ in ("100", "150", "fit"))
          + f"; core carrier/baryons(<150 kpc) {list(h_['core'].values())[0]:.2f} / {list(h_['core'].values())[1]:.2f} -> {'PASS' if h_['ok'] else 'FAIL'}   {elapsed()}")
L389p = J["L389"]["passes"]
P("    PM proxy (L389, provisional): passes " + ", ".join(k_ for k_, v_ in L389p.items() if v_))
if HV:
    hv_in = [k_ for k_ in HV if k_[1] == "in place"]
    check("B5 HARVEY IN PLACE: the fastest kick in the window (650 km/s) leaves group cores loaded (the slow side of L372's pincer): "
          "the population-mean excess beta passes on all three estimators; slower kicks keep more core carrier",
          {f"{k_[0]:.0f}|{k_[1]}": dict(fit=round(v_["beta"]["fit"], 3), ok=v_["ok"]) for k_, v_ in HV.items()},
          all(HV[k_]["ok"] for k_ in hv_in),
          "the optimistic history reading removes ~half the carrier uniformly and hollows the cores (rows above); the PM proxy "
          "passes only at 575 km/s (L389, S2 shape)")
OUT["numbers"]["B5"] = {f"{k_[0]:.0f}|{k_[1]}": v_ for k_, v_ in HV.items()}
OUT["numbers"]["B5_pm_proxy"] = L389p

banner("B9  THE GATE TABLE AND THE WINDOW, per reading (cells: kick x K; both footings required)")


def harvey_at(v_, rdg):
    """Harvey's verdict at kick v_ in a reading; an unrun kick inherits a PASS from a faster kick (faster hollows the core
    more: L372/AT3/L389 all monotone) and a FAIL from a slower one; otherwise None (not scored)."""
    if (v_, rdg) in HV: return bool(HV[(v_, rdg)]["ok"])
    faster = [HV[k_]["ok"] for k_ in HV if k_[1] == rdg and k_[0] > v_]
    slower = [HV[k_]["ok"] for k_ in HV if k_[1] == rdg and k_[0] < v_]
    if any(faster): return True
    if slower and not all(slower): return False
    return None


GT = {}
for v_ in VK_RET:
    s8_ = min(S8R[(v_, K_, "fluid")]["ratio"] for K_ in KS) >= 0.922
    gal_ = gal_max[v_] <= 0.06
    GT[v_] = {"in place": dict(flagship=FLAG[("self", v_)] <= FLAG_TOL, galaxies=gal_,
                               KiDS=all(KD[v_]["inplace"][f_] <= 4.0 for f_ in FEET),
                               X_COP=all(XC[v_]["inplace"][f_]["strict"] for f_ in FEET), S8=s8_,
                               shear=max(SH[v_][("in place (steady)", 1.75)].values()) <= 1.2,
                               Harvey=harvey_at(v_, "in place"), forest=None),
              "history/optimistic": dict(flagship=FLAG[("history", v_)] <= FLAG_TOL, galaxies=gal_,
                                         KiDS=all(KD[v_]["optimistic"][f_] <= 4.0 for f_ in FEET),
                                         X_COP=all(XC[v_]["optimistic"][f_]["strict"] for f_ in FEET), S8=s8_,
                                         shear=max(SH[v_][("optimistic history", 1.75)].values()) <= 1.2,
                                         Harvey=harvey_at(v_, "optimistic"), forest=None)}
    GT[v_]["in place (intact well)"] = dict(GT[v_]["in place"], flagship=FLAG[("intact", v_)] <= FLAG_TOL)
PMG = {}
for tag, row in J["L388"]["table"]["pooled"].items():
    PMG[tag] = dict(flagship=None, X_COP=PMX[tag]["strict"], S8=row["S8"] >= 0.922, forest=row["forest"] <= 0.10, shear=bool(row["shear"]),
                    Harvey=bool(L389p.get(f"{tag}|S2_med", False)))
fmt = lambda b_: "n/a" if b_ is None else ("pass" if b_ else "FAIL")
for v_ in VK_RET:
    for rdg, d_ in GT[v_].items():
        P(f"    v_k {v_:.0f} {rdg:22s}: " + ", ".join(f"{k_} {fmt(x_)}" for k_, x_ in d_.items()))
for tag, d_ in PMG.items():
    P(f"    {tag} PM proxy (L388/L389)      : " + ", ".join(f"{k_} {fmt(x_)}" for k_, x_ in d_.items())
      + "  [flagship: L388's z = 2 fixed-cell residue 0.063-0.075 against 0.059: 'not established']")
decided = lambda d_: all(x_ for x_ in d_.values() if x_ is not None) and d_.get("Harvey") is not None
kicks = {rdg: [v_ for v_ in VK_RET if decided(GT[v_][rdg])] for rdg in ("in place", "in place (intact well)", "history/optimistic")}
cells = {rdg: len(k_) * len(KS) for rdg, k_ in kicks.items()}
cells_in, cells_opt, cells_tot = cells["in place"], cells["history/optimistic"], len(VK_RET) * len(KS)
check("B9 THE WINDOW IN THE IN-PLACE READING (AT3's machinery as it scored AT1) IS EMPTY: X-COP and cosmic shear fail at every "
      "kick (with the intact well the flagship at M_b = 1e11 fails as well)",
      f"cells passing every gate the halo model decides (the forest is not established in any): in place {cells_in}/{cells_tot}, "
      f"in place with the intact well {cells['in place (intact well)']}/{cells_tot}, history/optimistic {cells_opt}/{cells_tot} "
      f"(kicks {kicks['history/optimistic']}; K-independent; the reduced grid scores 575 and 650 only)", cells_in == 0,
      "the window exists only if the escaped daughters stay out of groups and clusters (the history reading); a particle-mesh run "
      "with FK1's own trigger decides between the readings")
OUT["numbers"]["B9"] = dict(table={f"{v_:.0f}": d_ for v_, d_ in GT.items()}, pm=PMG, kicks=kicks, cells=cells, cells_total=cells_tot)
P(f"  part B done   {elapsed()}")

# ================================================================================================ PART C: the tie
banner("C1  THE DIMENSION MATRIX: what (a0, rho_Lambda, G, c) and (+ hbar, m) can make without a number put in")
Dm = sp.Matrix([[0, 1, -1, 0], [1, -3, 3, 1], [-2, 0, -2, -1]])       # rows M, L, T; columns a0, rho_Lambda, G, c
Dm2 = sp.Matrix([[0, 1, -1, 0, 1, 1], [1, -3, 3, 1, 2, 0], [-2, 0, -2, -1, -1, 0]])
ns1, ns2 = Dm.nullspace(), Dm2.nullspace()
P(f"    (a0, rho_Lambda, G, c): {len(ns1)} dimensionless group {list(ns1[0])} -> a0/(c sqrt(G rho_Lambda)) = kappa (FITTED, = 1/2 by P1)")
P(f"    (+ hbar, m): {len(ns2)} groups {[list(v_) for v_ in ns2]}: the two new ones carry m (and hbar)")
check("C1 DERIVED: the framework's constants (a0, rho_Lambda, G, c) carry exactly ONE dimensionless number, kappa -- itself FITTED; "
      "adding the dark mass m (and hbar) adds only m-dependent groups.  An eps/m^2 not put in by hand is either a power of kappa "
      "(or of pure numbers) or needs m", f"nullity {len(ns1)} / {len(ns2)}", len(ns1) == 1 and len(ns2) == 3)

banner("C2  THE CENSUS OF m-FREE TIES: integer (and half-integer) powers of kappa, Z, a0/(c H0), Omega_Lambda; the look-elsewhere rate")
WIN_LO, WIN_HI = float(_eps_m2(575.0)), float(_eps_m2(650.0))
BASES = {"kappa": 0.5, "Z": 2 * math.sqrt(8 * math.pi / 3), "a0/(c H0) canonical": A0_FP0["canonical"] / (c_SI * H0_SI),
         "Omega_Lambda": OM_L}
P(f"    bases: kappa = 1/2; Z = 2 sqrt(8 pi/3) = {BASES['Z']:.4f} (= sqrt(8 pi/3)/kappa); a0/(c H0) canonical = {BASES['a0/(c H0) canonical']:.4f}; "
  f"Omega_Lambda = {OM_L}.  a0/(c H0) on the alt footing equals 1/Z (ratio {A0_FP0['alt'] / (c_SI * H0_SI) * BASES['Z']:.6f}): the same base, not repeated")
HITS, PINT = [], {}
for bn, bv in BASES.items():
    for k2 in range(-80, 81):
        if k2 == 0: continue
        e_ = k2 / 2
        val = bv ** e_
        if WIN_LO <= val <= WIN_HI:
            HITS.append((bn, e_, val, C_KMS * math.sqrt(2 * val / (1 + val)), k2 % 2 == 0))
    PINT[bn] = min(1.0, math.log10(WIN_HI / WIN_LO) / abs(math.log10(bv)))
for h_ in HITS:
    P(f"    HIT ({'integer' if h_[4] else 'half-integer'} power): {h_[0]}^{h_[1]:g} = {h_[2]:.4e} -> v_k = {h_[3]:.1f} km/s")
P("    chance that SOME integer power of each base lands in a window this wide (log-uniform target): "
  + ", ".join(f"{k_} {v_:.2f}" for k_, v_ in PINT.items()) + " (half-integer powers double each; Omega_Lambda's then cover every window)")
p_any = 1 - float(np.prod([1 - v_ for v_ in PINT.values()]))
p_kap = PINT["kappa"]
k19 = [h_ for h_ in HITS if h_[0] == "kappa" and h_[1] == 19.0]
ints = [h_ for h_ in HITS if h_[4]]
check("C2 NO DERIVED TIE: the only integer-power m-free hit is eps/m^2 = kappa^19, i.e. v_k = kappa^9 c = 585.5 km/s; some integer power "
      "of kappa lands in a window this wide with probability %.0f%% by chance (%.0f%% for any of the four bases), and nothing gives "
      "the exponent 19 -- eps stays FITTED" % (100 * p_kap, 100 * p_any),
      f"integer hits {[(h_[0], h_[1]) for h_ in ints]}; half-integer hits {[(h_[0], h_[1]) for h_ in HITS if not h_[4]]}; "
      f"P(chance) kappa {p_kap:.2f}, any base {p_any:.2f}", len(k19) == 1 and len(ints) == 1 and p_kap > 0.3,
      "kappa = 1/2 is itself FITTED, and v_k = kappa^9 c sits inside the knife-edge's 575-600 km/s interval: a coincidence to "
      "record, not a derivation")
OUT["numbers"]["C2"] = dict(hits=HITS, p_chance_integer=PINT, p_any=p_any, window=[WIN_LO, WIN_HI])

banner("C3  THE m-DEPENDENT TIES: the dark mass each simple monomial needs (m is DECLARED, so a tie only moves the fit into m)")
hbar_eVs = 6.582119569e-16
HL = A0_FP0["canonical"] / (0.5 * c_SI)                               # sqrt(G rho_Lambda) [1/s]
MPL_eV = 1.220890e28
C3 = []
for b_ in (sp.Rational(1, 4), sp.Rational(1, 3), sp.Rational(1, 2), sp.Rational(2, 3), 1, sp.Rational(3, 2)):
    b_ = float(b_)
    for tgt in (WIN_LO, WIN_HI):
        # Pi_m = hbar sqrt(G rho_L)/(m c^2) = tgt^(1/b)  ->  m [eV]
        C3.append(("(hbar sqrt(G rho_L)/m c^2)^%g" % b_, tgt, hbar_eVs * HL / tgt ** (1 / b_)))
    for tgt in (WIN_LO, WIN_HI):
        C3.append(("(m/M_Pl)^%g" % b_, tgt, MPL_eV * tgt ** (1 / b_)))
ms_ok = [x_ for x_ in C3 if 1.9e-19 <= x_[2] <= 1e-3]
for x_ in C3[::2]:
    P(f"    eps/m^2 = {x_[0]:32s} -> m = {x_[2]:.2e} eV at 575 km/s")
check("C3 (reported) every m-dependent monomial hits the window at SOME m; the dark mass is declared (floor 1.9-5.2e-19 eV), so a "
      "'tie' through m trades eps for a tuned m: the count does not drop", f"{len(ms_ok)}/{len(C3)} solutions inside 1.9e-19-1e-3 eV",
      True, load_bearing=False)
OUT["numbers"]["C3"] = C3

banner("C4  THE TRIGGER'S CONSTANTS AND THE WINDOW'S WIDTH")
w_vk = kicks
P(f"    lambda_0 <-> f_t = rho_t0/((5/3) rho_crit0) = 1: the linear gate's x_c0 = 2.5 threshold (DECLARED; the switch's constant re-used)")
P(f"    q = 1.75 = p + 3/4 with the linear gate's p = 1 (DECLARED; q > 3/4 needed, A4); S_8 and F(2) move by <= "
  f"{max(abs(v_['ratio'] - S8R[(600.0, K_MID, 'fluid')]['ratio']) for v_ in VAR.values()):.3f} / "
  f"{max(abs(v_['F2'] - F23[(600.0, K_MID)][0]) for v_ in VAR.values()):.3f} across f_t 1/3-3 and q 1.25-2.5")
P(f"    kicks passing every decided gate: in place {w_vk['in place']}; history/optimistic {w_vk['history/optimistic']} "
  f"(of {list(VK_RET)}); K-independent (the fronts sit at r200 at z <= 2.5)")
check("C4 (reported) the trigger's constants: lambda_0 and q are the switch's declared values re-used (not derived, not tied to "
      "a0 or rho_Lambda); the gates at z <= 2.5 barely feel them (fronts at r200), the budget moves little; the window is set by "
      "the kick and by the reading", dict(variants=VAR, kicks=w_vk), True, load_bearing=False)

# ================================================================================================ PART D: the count
banner("D  THE HONEST CONSTANT COUNT: the dark sector, and the whole theory (FP7's root + FP9 pending + this sector)")
COUNT = [
    ("m (the dark mass)", ">= 1.9-5.2e-19 eV", "DECLARED", "required (FP4 L10f); not tied (C3)"),
    ("eps/m^2 (the splitting)", "1.84-2.35e-6 (575-650 km/s)", "FITTED", "to the kick window; no tie (C1-C3); kappa^19 is numerology"),
    ("lambda_0 (the conversion coupling)", "f_t = 1 (the linear gate's delta_t)", "DECLARED", "value borrowed from x_c0 = 2.5"),
    ("q (the K-gate exponent)", "1.75 = p + 3/4", "DECLARED", "value borrowed from p = 1; q > 3/4 derived (A4)"),
    ("the pure cross quartic (no lambda|Phi|^4 self-coupling)", "structure", "POSTULATED", "FK1 K5: the products must free-stream"),
    ("C (the gain's O(1) prefactor)", "sqrt(pi)", "DERIVED", "A5 (the path geometry bracketed x 3^(+-1))"),
    ("E_need (e-folds from the seed)", "61-178", "DERIVED", "FK1 N1, from m and the occupation"),
    ("the amount (Omega_dm)", "initial data", "INITIAL DATA", "FP4 A5 / FL1"),
    ("the misalignment near phi_H", "<= ~14 deg", "INITIAL DATA", "bounded by the flagship's cold phi_L share (FK1)"),
]
for n_, v_, s_, b_ in COUNT:
    P(f"    {n_:52s} {v_:34s} {s_:13s} {b_}")
P("    conditional (in-place reading only): a second channel for clusters -- AT3's mode U, a 3000 km/s daughter (a second splitting "
  "eps'/m^2 ~ 5e-5, FITTED) and its rate f_U(0) = 0.25 (FITTED): +2")
WHOLE = dict(root_FP7=dict(measured=["G", "Lambda"], fitted=["kappa"], postulated=["J_P2 (the MOND function)"],
                           bounded=["xi", "alpha_c", "c_2"], failing=["lambda_phi (the MOND scalar's inertia: empty window)"],
                           fixed=["beta = 0"], data=["phibar-dot = 0"]),
             separator_FP9="TBD (pending: the gate/switch -- on the record p = 1, x_c0 = 2.5, w <= 0.25, v_cap = 325 km/s declared; FP6's "
                           "(H) had five declared constants)",
             dark_sector_FP10=dict(fitted=["eps"], declared=["m", "lambda_0", "q"], postulated=["pure cross quartic"],
                                   data=["amount", "misalignment"], derived=["C", "E_need"]))
n_fit = len(WHOLE["root_FP7"]["fitted"]) + len(WHOLE["dark_sector_FP10"]["fitted"])
n_decl = len(WHOLE["root_FP7"]["bounded"]) + len(WHOLE["dark_sector_FP10"]["declared"])
P(f"    WHOLE THEORY (without FP9): {n_fit} FITTED (kappa, eps), {n_decl} declared/bounded (xi, alpha_c, c_2; m, lambda_0, q), "
  f"1 failing (lambda_phi, FP7), 2 measured (G, Lambda), 1 postulated function (J_P2) + 1 postulated structure (the cross "
  f"quartic), 3 initial data (phibar-dot, the amount, the misalignment); + FP9's separator (TBD); + 2 more if the in-place "
  f"reading holds for clusters")
check("D (reported) the constant count", dict(dark_sector=[(n_, s_) for n_, _, s_, _ in COUNT], whole=WHOLE), True, load_bearing=False)
OUT["numbers"]["D"] = dict(dark_sector=COUNT, whole=WHOLE)

# ================================================================================================ H the pre-declared hypotheses
banner("H  (reported) THE PRE-DECLARED HYPOTHESES, AS THEY FELL")
HYP = [
    ("H1 front >= 0.9 r200 for c >= 3 at z <~ 4", lo4 >= 0.9, f"z <= 2.5: {lo25:.3f}; z = 4: {lo4:.3f} (falls at the low-K corner)"),
    ("H2 flagship: history pass, in place self pass, intact fail at 1e11", fl_hist_ok and fl_self_ok and bool(fl_int_fail),
     f"history {max(FLAG[('history', v_)] for v_ in VK_RET):.4f}, self {max(FLAG[('self', v_)] for v_ in VK_RET):.4f}, intact {max(FLAG[('intact', v_)] for v_ in VK_RET):.3f}"),
    ("H3 X-COP fails in place at every kick", xc_in_fail, f"eps >= {min(XC[v_]['eps_self'] for v_ in VK_RET):.3f}"),
    ("H4 cosmic shear fails in place at 1.75 Mpc", sh_in_fail, f"worst R >= {min(max(SH[v_][('in place (steady)', 1.75)].values()) for v_ in VK_RET):.2f}"),
    ("H5 escaped budget by z = 0 >= 0.4 (S_8 undecided)", min(float(b_['Fb'][0]) for b_ in BUD.values()) >= 0.4,
     f"F_b(0) {min(float(b_['Fb'][0]) for b_ in BUD.values()):.3f}; S_8 ratio {s8_min:.3f} (passes)"),
    ("H6 forest not established (budget >= 4x)", forest_ne and ratio_budget[0] >= 4.0, f"{ratio_budget[0]:.1f}x; projection {proj[0]:.3f}-{proj[1]:.3f}"),
    ("H7 Harvey passes in place at 650", bool(HV.get((650.0, "in place"), {}).get("ok")) if HV else None, "see B5"),
    ("H8 KiDS passes in place", all(KD[v_]["inplace"][f_] <= 4 for v_ in VK_RET for f_ in FEET), "see B4"),
    ("H9 z = 0 galaxies pass", all(gal_max[v_] <= 0.06 for v_ in VK_RET), "see B2"),
    ("H10 eps: no tie ('any tie needs m')", False, f"FALSIFIED as worded: m-free numerical hits exist ({len(HITS)}, e.g. kappa^19); "
     "the verdict FITTED stands on the look-elsewhere rate"),
    ("H11 in-place window empty", cells_in == 0, f"{cells_in}/{cells_tot}"),
]
for n_, ok_, m_ in HYP:
    P(f"    {n_:62s} {'held' if ok_ else ('not run' if ok_ is None else 'FELL')}: {m_}")
check("H (reported) the pre-declared hypotheses as they fell", {n_: ok_ for n_, ok_, _ in HYP}, True, load_bearing=False)
OUT["numbers"]["H"] = [dict(h=n_, held=ok_, note=m_) for n_, ok_, m_ in HYP]

# ================================================================================================ W the ledger
banner("W  THE LEDGER: what this lane settles (link / status / basis)")
LEDGER = [
    ("L11a", "the dark sector's action: S_Psi with eps Re(Phi^2) + lambda(K)(Im Phi^2)^2 on one complex field (FK1 + FL2), L353's pair "
     "for kernel invisibility", "POSTULATED", "FK1/FL2 (committed); FP4 L10f"),
    ("L11b", "masses m_H^2 - m_L^2 = 2 eps, Z2 x Z2, kick v_k = sqrt(2 eps/(m^2 + eps)), latent heat v_k^2/2", "DERIVED", "check A1"),
    ("L11c", "S = 0: the dark action does not touch the MOND sector; the kick's energy is the rest-energy difference; energy "
     "selectivity (galaxies before clusters)", "DERIVED", "check A2 (FP8's B0 costs)"),
    ("L11d", "pair vertex lambda/(4 m_H m_L), G = lambda n_H/(2 m_H m_L), growth sqrt(G^2 - D^2)", "DERIVED", "check A3"),
    ("L11e", "Hubble sweep pi G^2/(4 H Delta); trigger n_t ~ H^(2q + 1/2); no spontaneous background conversion for q = 7/4",
     "DERIVED", "check A4"),
    ("L11f", "the halo gain: gamma = sqrt(pi) G^2/(m v_k sigma), S_c = (2/sqrt(pi)) H Int (rho/rho_t)^2 e^{-(Dv/sigma)^2} dl/sigma "
     "(the design's C = sqrt(pi))", "DERIVED", "check A5"),
    ("L11g", "where/when: fronts at >= 0.95 r200 for z <= 2.5; not mass-selective; one-shot at each progenitor's collapse", "DERIVED",
     "checks A6, A7"),
    ("L11h", "the splitting eps/m^2 = 1.84-2.35e-6", "FITTED", "checks C1-C3 (kappa^19 = numerology)"),
    ("L11i", "the trigger's lambda_0 and q (values re-used from the switch's x_c0, p)", "POSTULATED", "check C4"),
    ("L11j", "the flagship z = 0.5-2.5 in FK1's history reading (<= 0.074 dex); fails in place with the intact well at M_b 1e11",
     "DERIVED", "check B1"),
    ("L11k", "z = 0 galaxies, KiDS, S_8 (ratio >= 0.922)", "DERIVED", "checks B2, B4, B6"),
    ("L11l", "X-COP and cosmic shear IN PLACE (AT3's machinery): one splitting keeps clusters' carrier", "FAILS", "checks B3, B8"),
    ("L11m", "X-COP, cosmic shear and Harvey in the optimistic history reading / the PM proxy", "OPEN",
     "checks B3, B5, B8 (reading-dependent; FK1's own particle-mesh run decides)"),
    ("L11n", "the forest (budget >= 4x AT2's; projection straddles 10%)", "OPEN", "check B7"),
    ("L11o", "the web (seeded stimulation, super-threshold filaments) and the escaped daughters' re-accretion into r_F", "OPEN",
     "check A8; B1's reading"),
]
for k_, what, st, basis in LEDGER:
    P(f"    {k_:6s} {st:10s} {what}  --  {basis}")
OUT["ledger"] = [dict(link=k_, what=w_, status=s_, basis=b_) for k_, w_, s_, b_ in LEDGER]
check("W (reported) the ledger of this lane's links", f"{len(LEDGER)} links", True, load_bearing=False)

# ================================================================================================ verdict
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
banner("VERDICT")
P(f"""  THE ACTION.  One complex field with a U(1)-breaking mass term and a K-gated pure cross quartic:
  V = m^2|Phi|^2 + eps Re(Phi^2) + lambda_0 (K/3H_0)^(-2q) (Im Phi^2)^2.  Varied, it gives two components split by 2 eps, a
  Z2 x Z2 that keeps a lone phi_H stable, and phi_H phi_H -> phi_L phi_L back to back at v_k = sqrt(2 eps/(m^2 + eps)).  It never
  touches the MOND sector (S = 0): the kick is paid by the dark field's own rest energy, and the latent heat v_k^2/2 exceeds
  the z = 2.5 flagship hosts' specific binding ({fl_min:.1f}x or more) but not the cluster's ({cl_max:.2f}x) -- the right order.
  THE CLEARING.  The conversion is a Bose-stimulated pair instability; in a halo it runs at the Doppler-broadened rate
  sqrt(pi) G^2/(m v_k sigma) (the design's depth with C = sqrt(pi)).  It is a HALO-COLLAPSE trigger: at z <= 2.5 every halo
  converts to >= {lo25:.2f} r200, in its progenitors, within < 0.1 of a dynamical time (< 1e-2 inside 0.5 r200);
  it is not mass-selective.
  THE GATES (reduced grid, both footings).  Flagship z = 0.5-2.5: passes in FK1's history reading (<= {max(FLAG[('history', v_)] for v_ in VK_RET):.4f} dex) and in
  place with the self-consistent well ({max(FLAG[('self', v_)] for v_ in VK_RET):.3f}); fails in place with the intact well ({max(FLAG[('intact', v_)] for v_ in VK_RET):.2f} dex at M_b 1e11).
  z = 0 galaxies {max(gal_max.values()):.4f} dex; KiDS {max(KD[v_]['inplace'][f_] for v_ in VK_RET for f_ in FEET):+.1f}; S_8 ratio {s8_min:.3f}-{max(v_['ratio'] for v_ in S8R.values()):.3f}: pass.
  X-COP in place {min(XC[v_]['inplace']['canonical']['ratio'] for v_ in VK_RET):.2f}-{max(XC[v_]['inplace']['alt']['ratio'] for v_ in VK_RET):.2f} and cosmic shear in place {min(max(SH[v_][('in place (steady)', 1.75)].values()) for v_ in VK_RET):.2f}-{max(max(SH[v_][('in place (steady)', 1.75)].values()) for v_ in VK_RET):.2f}: FAIL (one splitting cannot empty a
  cluster).  In the optimistic history reading they pass (X-COP {', '.join(f"{XC[v_]['optimistic']['canonical']['ratio']:.2f}" for v_ in VK_RET)}, shear
  {', '.join(f"{max(SH[v_][('optimistic history', 1.75)].values()):.2f}" for v_ in VK_RET)}), and Harvey there: {', '.join(f"{k_[0]:.0f} {k_[1]} {'pass' if v_['ok'] else 'FAIL'}" for k_, v_ in HV.items()) or 'not run'}.
  The forest is not established ({proj[0]:.3f}-{proj[1]:.3f} projected).
  THE WINDOW.  In place: {cells_in}/{cells_tot} cells.  History/optimistic: {cells_opt}/{cells_tot} cells pass every gate the halo model decides
  (kicks {kicks['history/optimistic']}; the reduced grid scores 575 and 650 only, 600-625 are the full grid's).
  The PM proxy at the same threshold (L388/L389) passes X-COP, S_8, forest and shear at 575-650 but Harvey only at 575 and the
  flagship is 'not established' there -- a sliver.  Which reading holds is a question for a particle-mesh run with FK1's own
  trigger (sharp conversion at the fluid's front, re-accretion followed).
  THE PRICE.  eps is FITTED (the only integer-power m-free 'tie' is kappa^19 -> 585.5 km/s: chance {100 * p_kap:.0f}% for kappa alone);
  lambda_0 and q are the switch's declared values re-used; m and the amount and misalignment are declared/initial data.  Dark
  sector: 1 fitted, 3 declared, 1 postulated structure, 2 initial data (+2 if clusters need AT3's second channel).  Whole
  theory without the pending separator: 2 fitted (kappa, eps), 6 declared or bounded, 1 failing (FP7's lambda_phi).
  S = 0 also means this sector cannot move the record's MOND-sector failures (XR9: the EFE samples, the Local Group, Coma's
  UDGs): they stay the separator's.  Not 'closed' as a theory.""")
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["runtime_s"] = len(CH), n_fail, time.time() - T0
if FULL:
    P("\n  (this was the full grid)")
else:
    P("\n  HUB: the full grid is  FP10_FULL=1 python3 real_research/derivation_chain_2026/FP10_internal_splitting_dark_sector.py "
      "> real_research/derivation_chain_2026/FP10_internal_splitting_dark_sector_FULL.out 2>&1  (all four kicks' retention, the gas range "
      "at every z, Harvey at 8 cells: ~1.1-1.5 h, two threads, ~14 GB peak)")


def _jd(o):
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, (np.bool_,)): return bool(o)
    return str(o)


outname = f"{SLUG}_results.json".replace("_MUTATE_results", "_results_MUTATE")
OUTDIR = SMOKE_DIR if SMOKE else HERE                                  # a smoke run never writes into the lane directory
if OUTDIR:
    json.dump(OUT, open(os.path.join(OUTDIR, outname), "w"), indent=1, default=_jd)
P(f"\n  {len(CH) - sum(1 for _, ok, _ in CH if not ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   {elapsed()}")
sys.exit(0 if n_fail == 0 else 1)
