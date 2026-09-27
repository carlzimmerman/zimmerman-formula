#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FP15 -- ELIMINATE THE DARK SECTOR'S KNOBS: can the conversion trigger be the separator's own gate, can eps come from a
mechanism, is the dark mass m pinned or tied, can the amount come from dynamics?  One constant at a time, from the action,
every gate re-scored, both a0 footings (FP0's 9.3603e-11 / 1.1312e-10; the loaded machinery's 9.3619e-11 / 1.1279e-10).

WHY.  The target is ZERO knobs beyond kappa = 1/2 (FITTED, accepted).  FP10 (committed d9cb8b837) wrote FK1's dark sector as an
action -- one complex field, V = m^2|Phi|^2 + eps Re(Phi^2) + lambda_0 (K/3H_0)^(-2q) (Im Phi^2)^2, kernel-invisible through
L353's pair -- and priced it: eps FITTED (eps/m^2 = 1.84-2.35e-6), m DECLARED (floor 1.9-5.2e-19 eV), lambda_0 and q DECLARED
(borrowed from the old switch's x_c0 and p), the amount and the misalignment initial data, the pure cross quartic POSTULATED.
FP4/FP8: the MOND sector cannot pay for the kick (reciprocity), so the energy is the dark field's own.  FP9's separator has its
own onset, y_th = y_Lambda Omega_L(<K>_h)^(-p'), p' = 4.  The hub's committed lanes add gates a shared trigger must also pass:
XR12 (the forest on its calibrated gas proxy sits at the 10% line; the flagship with stream infall bounds FK1's normalisation
zeta = f_t to <= 2.54-2.76 canonical / 4.09-4.29 alt), XR16 (FK1's conversion is not mass-selective), XR19 (running, not used:
does the conversion run away through the web?).

NOTATION.  zeta = FP10's f_t = XR12's delta_t0/5.31: rho_t(z) = zeta (5/3) rho_crit0 E(z)^(2q + 1/2) (total-matter units).
R(z) = rho_t(z)/rho_bar_m(z) is the trigger's height above the cosmic mean; a region of overdensity delta converts
spontaneously where 1 + delta >= R (FP10 A4: N = E_need (rho/rho_t)^2 e-folds per Hubble sweep), is seed-stimulable (>= 1
e-fold per sweep) where (1 + delta) sqrt(E_need) >= R, and cold filaments convert at ~0.21 n_t (XR12's cone estimate).
zeta_eq = the q = 7/4 normalisation with the same threshold at z = 2.5: zeta = zeta_eq E(2.5)^(7/2 - 2q).  The flagship bounds
the threshold at z = 2.5 (the anchor): XR12-W2's resolved bound (the own-density cap with stream infall) zeta_eq <= 2.54/2.76
(canonical) / 4.09/4.29 (alt), or FP10's no-cap reach (the scoring-epoch stimulated front covers r_F) at K = 36/185/947.

PARTS.
  C0  controls: FP10's budget, S_8 and progenitor passage; XR12's calibrated forest; XR12's A1 table and FP10's A4 peak from
      this lane's R(z); FP9's y_th(z) and L(z) -- all reproduced from the loaded, unedited machinery.
  T   TRIGGER SHARING.  T1 (sympy) FK1's K-gate IS a power of the separator's Omega_L(<K>_h) on CMC leaves -- the running
      variable is shared already -- but the exponent is not fixed by the action: three inequivalent identifications with p'.
      T2 (sympy) the anchor law: with the threshold pinned at z = 2.5, R(z) falls toward z = 0 monotonically iff
      q >= 1/Omega_m0 - 1/4.  T3 every shared exponent on the web, at every flagship anchor (load-bearing); T3b the q-window
      (forest band x web x A4 x the flagship's progenitor passage); T3c S_8 and the cluster readings under the web bracket.
      T4 THE YIELD ONSET AS THE TRIGGER: T4a (sympy) the gate term, its reciprocal source, FRW and the z >= 2.5 IGM protected
      exactly (q eliminated); T4b the reciprocal flux at the yield surface and the m it needs; T4c the flagship (passage,
      retention); T4d the zeta window, the forest, S_8, mass-selectivity; T4e the same gate on FP13's state separator (H_S).
      T6 FP13's STATE QUANTITIES AS THE TRIGGER (added when FP13 landed, 27faacc84): the q-sign onset (global), the local
      nonlinearity at the same delta_c, and its spherical-collapse partner Delta = 18 pi^2 (load-bearing); T6d the threshold
      delta_t0 itself (XR19: the dominant lever) against 1 + delta_c, the turnaround 9 pi^2/16 and 18 pi^2.  T5 the gate table.
  E   eps: E1 (sympy) the Z4 theorem (eps is the only term odd under Phi -> i Phi; one-loop split proportional to eps; the
      condensate's own shift has the wrong sign); E2 every candidate mechanism (L353 pair, leaf average, khronon frame,
      vacuum/Hubble scales); E3 the numerology census (FP10 C2 reproduced); E4 the window's ends are set by gates.
  M   m: M1 the forest's lower bound on zeta rises with m (minihalos convert) against the flagship's upper bound, on XR12's
      reading (load-bearing); M2 FP10's derived-front reading (no own-density cap); M3 the Bose-occupancy ceiling; M4 L383's
      dwarf-heating floor moves with the clearing epoch; M5 the m-numerology census.
  N   the amount: misalignment and the stochastic (inflationary) equilibrium; the misalignment prior; the LCDM comparison.
  D   the count (dark sector; whole theory with FP13/FP14 TBD).  H the pre-declared hypotheses.  W the ledger.
PRE-DECLARED (scratch note written 2026-09-27 07:20 before any FP15 number; only committed files had been read):
  H1 exponent sharing (q = p'-1/4, p', p'+3/4) is EXCLUDED: once the flagship/forest pin the threshold at z ~ 2.5, the steep
     running drops it below the web (the forest-epoch filaments or S_8 fail).  H2 the shared gate makes XR19's runaway WORSE.
  H3 FK1's own q: at the FDM floor the forest's zeta-bound reaches the canonical cap (a sliver or closed); alt open.
  H4 q has a window (3/4 .. ~2-3); inside it q is nearly degenerate with zeta at z ~ 2.5; zeta is pinned (FITTED-BY-DATA).
  H5 the yield-onset gate removes q but its reciprocal flux at the yield surface exceeds the MOND flux at the floor mass.
  H6 eps is Z4-protected: IRREDUCIBLE, FITTED-BY-DATA; kappa^19 NUMEROLOGY; vacuum/Hubble splittings >= 1e20 too small.
  H7 m is not pinned on FP10's reading; on XR12's reading the forest pins m near the floor (or closes the canonical window).
  H8 the amount is irreducible initial data (LCDM's omega_c status); a stochastic equilibrium trades it for H_inf ~ keV.
  H9 the new count is not zero knobs.
HISTORY.  Prototype runs (scratch, uncommitted) came first: the loaders, the generalised forest evaluator (it reproduced
  XR12's committed H2 row to 5e-3 with a full-range integral; the lane integrates the hard cut exactly as XR12 slices it, which
  is the C0b control), FP10's budget and S_8 under (zeta, q), the anchored R(z) table, FP10's passage at q = 1.75/3.75/4.75, the
  yield radius and its passage, FP10's no-cap reach, and a q- and m-scan of the forest.  The check directions below were fixed
  after them; no gate threshold, proxy or calibration was changed.  A smoke run (FP15_SMOKE, scratch) then showed one bug: E2's
  time average returned a Piecewise because the frequency m was declared real, not positive (the identity itself holds); fixed
  by a positive symbol.  While the lane ran, FP13 landed (27faacc84) with a state-derived separator (H_S); the coordinator asked
  for the dark trigger to be tested against H_S's own quantities: T4e and T6 were added then (no pre-declared hypothesis), and
  T1b (the yield-to-density maps) after the smoke run; T6d after XR19's result (delta_t0 is the dominant lever) reached the lane.
  Nothing outside this lane's FP15_ files is written.

MUTATE=1: no sharing and no dark-mass floor -- the 'shared' exponents are replaced by FK1's own q = 7/4 and the fluid's halo
  cut-off by XR12's hard M_min = 1e8 Msun (m -> ~6e-21 eV, below L383's floor).  T3 (the web) and M1 (the pinning) must FAIL.
Run from the repository root (at most two threads, ~15-20 min):
  python3 real_research/derivation_chain_2026/FP15_zero_knob_dark_sector.py
"""
import os, sys, io, re, json, math, time, contextlib, warnings

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "2"                                                  # shared machine: at most two workers
for _v in ("AT1_THREADS", "AT3_THREADS", "L357_THREADS"):
    os.environ[_v] = "2"
import numpy as np
import sympy as sp
from scipy.special import erf

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SMOKE = os.environ.get("FP15_SMOKE", "0") == "1"                       # code test only; never committed
SMOKE_DIR = os.environ.get("FP15_SMOKE_DIR", "")
SLUG = "FP15_zero_knob_dark_sector" + ("_MUTATE" if MUTATE else "")
T0 = time.time()
OUT = {"lane": "FP15", "mutate": MUTATE, "smoke": SMOKE, "checks": {}, "numbers": {}, "ledger": []}
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


P(__doc__.split("PARTS.")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: no sharing (q_shared -> 7/4) and no dark-mass floor (M_min = 1e8): T3 and M1 must FAIL ***")
if SMOKE:
    P("\n  *** FP15_SMOKE=1: reduced grids, a code test only; never for the record ***")

# ================================================================================================ constants and footings (FP0)
c_SI, G_SI = 299792458.0, 6.67430e-11
MPC_M = 3.0856775814913673e22
KPC_M = MPC_M / 1e3
H0_SI = 67.4e3 / MPC_M
OM_L = 0.6847
RHO_CRIT = 3 * H0_SI ** 2 / (8 * math.pi * G_SI)
A0_FP0 = {"canonical": 0.5 * c_SI * math.sqrt(G_SI * OM_L * RHO_CRIT), "alt": 0.5 * c_SI * math.sqrt(G_SI * RHO_CRIT)}
FEET = ("canonical", "alt")
KAPPA, ZED = 0.5, 2 * math.sqrt(8 * math.pi / 3)
HBAR_EVS = 6.582119569e-16                                           # eV s
EV_KG = 1.602176634e-19 / c_SI ** 2
M_PL_EV = 1.220890e28                                                # Planck mass [eV]
OUT["numbers"]["a0_FP0"] = A0_FP0
VKS = (575.0, 650.0)
FLAG_TOL = 0.074

# ================================================================================================ LOADING (read-only exec)
banner("LOADING the committed machinery (read-only exec of FP10's head + its budget/progenitor definitions, and XR12's head)")
PF10 = os.path.join(HERE, "FP10_internal_splitting_dark_sector.py")
_s10 = open(PF10).read()
_h10 = _s10[:_s10.index("# ================================================================================================ C0 controls")]
_b10 = _s10[_s10.index("CGRID = np.geomspace(3.0, 40.0, 14)"):_s10.index("BUD = {}")]
_p10 = _s10[_s10.index("def progenitor(H_, al, dz=0.25, zmax=20.0):"):_s10.index("GATE = {}")]
_save = {k: os.environ.get(k) for k in ("MUTATE", "FP10_FULL", "FP10_SMOKE", "FAST")}
os.environ.update(MUTATE="0", FP10_FULL="0", FP10_SMOKE="0", FAST="0")    # the loaded lanes' own switches stay off
F = {"__name__": "fp10", "__file__": PF10}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_h10, PF10, "exec"), F)
    exec(compile(_b10, PF10, "exec"), F)
    exec(compile(_p10, PF10, "exec"), F)
P(f"  FP10 head (AT3's head: AT1, L357, L320, BK1, L321, L355, L360; MS3's halo model) + budget/progenitor defs loaded   {elapsed()}")
PX = os.path.join(REPO, "real_research", "cross_thread_review_2026_09_26", "XR12_forest_halo_model.py")
_sx = open(PX).read()
_hx = _sx[:_sx.index("# ============================================================================================ C1 L357's V1 reproduced")]
X = {"__name__": "xr12", "__file__": PX}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_hx, PX, "exec"), X)
for k_, v_ in _save.items():
    if v_ is None:
        os.environ.pop(k_, None)
    else:
        os.environ[k_] = v_
P(f"  XR12's head (L319's solver with its cold component, L357's halo model re-implemented, CLASS) loaded   {elapsed()}")
J = dict(
    FP9=rd("real_research/derivation_chain_2026/FP9_web_galaxy_separator_results.json")["numbers"],
    FP10=rd("real_research/derivation_chain_2026/FP10_internal_splitting_dark_sector_results.json")["numbers"],
    XR12=rd("real_research/cross_thread_review_2026_09_26/XR12_forest_halo_model_results.json")["numbers"],
    XR12s=rd("real_research/cross_thread_review_2026_09_26/XR12_stream_shells_results.json")["numbers"],
    FK1=rd("real_research/dark_fluid_kick_2026/FK1_kick_as_phase_change_results.json")["numbers"],
    L383=rd("real_research/condensate_dust_2026/L383_wave_field_zoom_in_results.json")["numbers"],
    AT1=rd("real_research/acceleration_trigger_2026/AT1_acceleration_trigger_highz_results.json")["numbers"],
)
KCAL = J["XR12"]["C2"]["calibration"]["2.0"]                          # XR12's gas-proxy calibration (proxy / PM measured)
W2 = J["XR12s"]["W2"]["cells"]
ZW2 = {"canonical": (W2["canonical/streams C_s=10"]["zeta_flagship"], W2["canonical/streams + upstream"]["zeta_flagship"]),
       "alt": (W2["alt/streams C_s=10"]["zeta_flagship"], W2["alt/streams + upstream"]["zeta_flagship"])}
ZCAP = {f_: J["XR12"]["W"]["zeta_F"][f"1e12/{f_}"]["zeta_cap"] for f_ in FEET}
E_NEED = {k_: float(v_["efolds"]) for k_, v_ in J["FK1"]["N1"]["by_mass"].items()}
P(f"  XR12-W2 flagship bounds (zeta_eq): canonical {ZW2['canonical'][0]:.2f}/{ZW2['canonical'][1]:.2f}, alt {ZW2['alt'][0]:.2f}/"
  f"{ZW2['alt'][1]:.2f}; own-density cap (1e12 host) {ZCAP['canonical']:.2f}/{ZCAP['alt']:.2f}; gas-proxy calibration {KCAL:.4f}; "
  f"FK1 E_need {min(E_NEED.values()):.0f}-{max(E_NEED.values()):.0f}")

Om, Ez2 = F["Om"], F["Ez2"]
E25 = math.sqrt(Ez2(2.5))
KS = F["KS"]
K_LO, K_MID, K_HI = KS
XMH, XLGM, hX = X["MH"], np.log(X["MH"]), X["h"]
ZGX = X["ZG"]
FK1_Q = 1.75


# ================================================================================================ this lane's helpers
def zeta_of(zeq, q):
    """the normalisation that puts the q-running threshold at z = 2.5 where q = 7/4 with zeta_eq puts it."""
    return zeq * E25 ** (3.5 - 2 * q)


def Rtm(z, zeta, q):
    """R(z) = rho_t/rho_bar_m (FP10's rho_t = zeta (5/3) rho_crit0 E^(2q+1/2), total-matter units)."""
    z = np.asarray(z, float)
    return zeta * (5.0 / 3.0) * Ez2(z) ** ((2 * q + 0.5) / 2.0) / (Om * (1 + z) ** 3)


ZWEB = np.linspace(0.0, 6.0, 1201)


def first_epoch(R, T):
    """the highest z at which R(z) <= T (the epoch at which an overdensity with 1 + delta = T first crosses); None if never."""
    ok = R <= T
    return float(ZWEB[np.where(ok)[0].max()]) if ok.any() else None


def web(zeq, q, e_need):
    zt = zeta_of(zeq, q); R = Rtm(ZWEB, zt, q)
    return dict(zeta=zt, R_min=float(R.min()), z_min=float(ZWEB[R.argmin()]),
                R_at={z_: float(Rtm(z_, zt, q)) for z_ in (0.0, 0.3, 1.0, 1.5, 2.0, 2.5, 3.0)},
                mean_spont=first_epoch(R, 1.0), mean_seeded=first_epoch(R, math.sqrt(e_need)), walls=first_epoch(R, 3.0),
                filaments=first_epoch(R, 11.0), filaments_cone=first_epoch(R, 11.0 / 0.21))


# FP9's cosmology (FP6's: radiation kept) for the yield, the band-pass length and the early-universe background
_h9 = 0.6736; _H09 = 100 * _h9 * 1e3 / MPC_M; _rc9 = 3 * _H09 ** 2 / (8 * math.pi * G_SI)
_Og9 = (4 * 5.670374419e-8 * 2.7255 ** 4 / c_SI ** 3) / _rc9
OR9 = _Og9 * (1 + 3.046 * (7 / 8) * (4 / 11) ** (4 / 3)); OM9 = (0.02237 + 0.1200) / _h9 ** 2; OL9 = 1 - OM9 - OR9
E2_9 = lambda z: OR9 * (1 + z) ** 4 + OM9 * (1 + z) ** 3 + OL9
OmL9 = lambda z: OL9 / E2_9(z)
HEAD9 = dict(n=2.0, L25=1.3, pp=4.0, y25=1e-6)                        # FP9's committed headline (H2)
y_th = lambda z: HEAD9["y25"] * (OmL9(0.25) / OmL9(z)) ** HEAD9["pp"]
L_kpc = lambda z: 1e3 * (HEAD9["L25"] / OmL9(0.25) ** (HEAD9["n"] / 2)) * OmL9(z) ** (HEAD9["n"] / 2)


# FP13's state separator (H_S, committed 27faacc84): L(z) where the actual matter field's heat-smoothed leaf-rms reaches
# delta_c = 1.686 (its A2 table), the yield = the web's band-passed NL leaf-rms (its D1 values at z = 0.25, 2.5; log-interpolated
# in 1+z, extrapolated with the same slope) x max(0, 2q), 2q = 1 + Omega_r - 3 Omega_L(<K>_h)  (zero once the leaf accelerates)
J13 = rd("real_research/derivation_chain_2026/FP13_separator_from_state_results.json")["numbers"]
_L13 = J13["A2"]["L_kpc"]["NL_1.686"]
_L13z = np.array(sorted(float(k_) for k_ in _L13)); _L13v = np.array([_L13[k_] for k_ in sorted(_L13, key=float)])
_rms13 = (J13["D1"]["band-passed rms (NL)"]["y025"], J13["D1"]["band-passed rms (NL)"]["y25"])
_slope13 = math.log(_rms13[1] / _rms13[0]) / math.log(3.5 / 1.25)
two_q = lambda z: 1 + OR9 * (1 + z) ** 4 / E2_9(z) - 3 * OmL9(z)       # 2 x the leaf's deceleration parameter
Z_Q0 = float(J13["C2_epochs"]["q0"])


def L13_kpc(z):
    if z <= _L13z[-1]:
        return float(np.exp(np.interp(z, _L13z, np.log(_L13v))))
    return float(_L13v[-1] * (OmL9(z) / OmL9(_L13z[-1])) ** (J13["A2"]["n_eff"]["NL_1.686"] / 2.0))   # the state's own running (n_eff = 2.06)


y_th13 = lambda z: _rms13[0] * ((1 + z) / 1.25) ** _slope13 * max(0.0, two_q(z))
SEP = {"H_Y": (y_th, L_kpc), "H_S": (y_th13, L13_kpc)}


def R_rad(z, zeta_eq, q):
    """R(z) with radiation (FP9's E), anchored at z = 2.5 on FP9's E: for the early-universe background (A4 up to z = 1e5)."""
    E259 = math.sqrt(E2_9(2.5))
    zt = zeta_eq * E259 ** (3.5 - 2 * q)
    return zt * (5.0 / 3.0) * E2_9(z) ** ((2 * q + 0.5) / 2.0) / (OM9 * (1 + z) ** 3)


# --------------------------------------------------------------------------- the forest on XR12's calibrated gas proxy
def supp_fdm(M, m22):                                                 # Schive+2016 (FP10's own cut-off)
    return (1 + (M / (1.6e10 * m22 ** (-4.0 / 3.0))) ** -1.1) ** -2.2


def rhv_q(z, zeta, q):
    """XR12's threshold (rho_crit(z) units) with the running generalised: zeta delta_t0 Omega_m0 E^(2q - 3/2); q = 7/4 -> E^2."""
    return zeta * X["DT0_LIN"] * X["Om"] * X["Ez2"](z) ** ((2 * q - 1.5) / 2.0)


_YYC = {}


def Fb_x(z, rhv, vk, cut, ycut=None):
    """XR12's Fb (bias-weighted escaped converted fraction) with (i) the fluid's own cut-off: ('hard', M_min) sliced exactly as
    XR12 slices it, or ('fdm', m_eV) with FP10's smooth Schive suppression; (ii) optionally the yield cut (T4): no conversion
    outside the MOND-on radius r_Y(M, z) of the halo's baryons."""
    s = X["SIG0"] * X["DG"](z); nu = X["DC"] / s
    w = X["f_st"](nu) * np.abs(np.gradient(nu, XLGM))
    m, y, cs, dch = X["trig"](z, rhv, "cleared")
    if ycut is not None:
        y = np.minimum(y, yY_grid(z, ycut))
        m = np.where(y > 1e-6, X["mfn"](np.maximum(y, 1e-6)) / X["mfn"](cs), 0.0)
        y = np.maximum(y, 1e-6)
    fe = X["esc"](z, vk, y, cs, dch, "cleared", rhv) if vk > 0 else 1.0
    wb = w * X["b_st"](nu)
    if cut[0] == "hard":
        sel = XMH >= cut[1] * hX
        return float(X["_trap"]((wb * m * fe)[sel], XLGM[sel]))
    return float(X["_trap"](wb * m * fe * supp_fdm(XMH / hX, cut[1] / 1e-22), XLGM))


FCACHE = {}


RHV_CUSTOM = {"virial 18 pi^2": lambda z: 18 * math.pi ** 2 * X["Om_z"](z)}     # rho_t = 18 pi^2 rho_bar_m (rho_crit(z) units)


def forest_eval(zeta, q, cut, vk=600.0, ycut=None, custom=None):
    key = (round(math.log(zeta), 9), round(q, 6), cut, vk, ycut, custom)
    if key in FCACHE:
        return FCACHE[key]
    Fz = [Fb_x(float(z_), (RHV_CUSTOM[custom](float(z_)) if custom else rhv_q(float(z_), zeta, q)), vk, cut, ycut) for z_ in ZGX]
    S_, Fc_ = X["to_S"](Fz)
    pr = X["proxies"](S_, vk)
    cal = {z_: pr[z_]["p1d_kF5"] / KCAL for z_ in ("3.0", "2.0")}
    FCACHE[key] = dict(cal=cal, worst=max(cal.values()), S=S_, Fb={zz: float(np.interp(zz, ZGX, Fc_)) for zz in (0.0, 0.4, 0.5, 1.0, 2.0, 3.0, 4.0)})
    return FCACHE[key]


def zeta_forest_edge(q, cut, grid, ycut=None):
    """the smallest zeta_eq on the grid scan with the forest <= 10% (both z = 2, 3), log-linear interpolation of the worst
    calibrated deficit between the last failing and the first passing grid point; None if the grid never passes, 0 if its
    first point passes."""
    vals = []
    for zeq in grid:
        r = forest_eval(zeta_of(zeq, q), q, cut, ycut=ycut)
        vals.append((zeq, r["worst"]))
        if r["worst"] <= 0.10:
            break
    if vals[-1][1] > 0.10:
        return None, vals
    if len(vals) == 1:
        return 0.0, vals
    (z1, w1), (z2, w2) = vals[-2], vals[-1]
    t = (w1 - 0.10) / max(w1 - w2, 1e-12)
    return float(math.exp(math.log(z1) + t * (math.log(z2) - math.log(z1)))), vals


# --------------------------------------------------------------------------- the yield radius (FP9's band-passed baryons)
def Fgauss(x):
    return erf(x / math.sqrt(2)) - math.sqrt(2 / math.pi) * x * np.exp(-x * x / 2)


def y_bp(r, Mb, a, z, foot, sep="H_Y"):
    """the band-passed baryonic field in a0 units: G Mb [r^2/(r+a)^2 - F(r/L)]/r^2 (Hernquist; S_L as a Gaussian of width L on
    the baryons' monopole, S_xi -> 1 at xi ~ 0.03 pc), FP0's footings; L from the chosen separator (FP9's H_Y or FP13's H_S)."""
    g = F["GK"] * Mb * (r ** 2 / (r + a) ** 2 - Fgauss(r / SEP[sep][1](z))) / r ** 2      # (km/s)^2/kpc
    return g * 1e6 / KPC_M / A0_FP0[foot]


def r_yield(Mb, a, z, foot, rmax=5000.0, sep="H_Y"):
    rr = np.geomspace(0.02, rmax, 2500)
    ok = y_bp(rr, Mb, a, z, foot, sep) >= SEP[sep][0](z)
    return float(rr[np.where(ok)[0].max()]) if ok.any() else 0.0


def yY_grid(z, ycut):
    """r_Y/r_s on XR12's halo grid (AT1's galaxy baryons, mu_fac = 1); ycut = (footing, separator)."""
    foot, sep = ycut
    key = (round(float(z), 6), foot, sep)
    if key in _YYC:
        return _YYC[key]
    M200 = XMH / hX
    r200 = (3 * M200 / (4 * np.pi * 200 * X["RHOC0_KPC"] * X["Ez2"](z))) ** (1 / 3)
    cs = X["c_dm14"](XMH, z); rs = r200 / cs
    Mb, a = F["galaxy_baryons"](M200, float(z), 1.0)
    xg = np.geomspace(1e-3, 4.0, 500)
    r = r200[:, None] * xg[None, :]
    ok = y_bp(r, np.asarray(Mb)[:, None], np.asarray(a)[:, None], float(z), foot, sep) >= SEP[sep][0](float(z))
    idx = np.where(ok.any(1), ok.shape[1] - 1 - np.argmax(ok[:, ::-1], axis=1), -1)
    rY = np.where(idx >= 0, r[np.arange(len(XMH)), np.maximum(idx, 0)], 0.0)
    _YYC[key] = rY / rs
    return _YYC[key]


# --------------------------------------------------------------------------- FP10's budget with the yield cut (a copy, one line added)
def budget_Y(vk, K, ft, qg, foot, m22=2000.0, sep="H_Y"):
    """FP10's budget() (committed lines), with ONE change: the conversion front is min(FP10's stimulated front, r_Y/r200)."""
    Mh = F["MH"] / F["hh"]; Fl, Fbl, hi = [], [], []
    for z in F["ZG"]:
        if z > 20.0:
            Fl.append(0.0); Fbl.append(0.0); hi.append(0.0); continue
        s = F["SIG0"] * F["DG"](z); nu = F["DC"] / s
        w = F["f_st"](nu) * np.abs(np.gradient(nu, np.log(F["MH"]))); bb = F["b_st"](nu)
        cs = np.clip(F["c_dm14"](F["MH"], z), 3.0, 40.0)
        r200 = (3 * Mh / (4 * np.pi * 200 * F["RHOC0_KPC"] * Ez2(z))) ** (1 / 3); V200 = np.sqrt(F["GK"] * Mh / r200)
        u = np.clip(vk / V200, 0, F["UGRID"][-1])
        Tf, Ts = F["tables"](z, K, ft, qg)
        xs = np.clip(Tf(np.stack([np.log(cs), u], 1)), 0.0, 1.0)
        Mb, a = F["galaxy_baryons"](Mh, float(z), 1.0)
        xY = np.array([r_yield(Mb_, a_, float(z), foot, rmax=4 * r2_, sep=sep) for Mb_, a_, r2_ in zip(Mb, a, r200)]) / r200
        xs = np.minimum(xs, xY)                                                         # the one added line
        xc = np.clip(np.array([F["x_core"](M_, z, m22) for M_ in Mh]), F["XG"][0], 1.0)
        Sc = Ts(np.stack([np.log(cs), np.log(xc)], 1))
        ign = Sc >= 1.0
        lc = np.where((xs > 0) & ign, F["I_LC"](np.stack([np.log(np.clip(cs, F["CG"][0], F["CG"][-1])), np.log(np.maximum(xs, F["XVG"][0]))], 1)), 0.0)
        fe = np.where(xs > 0, F["I_ES"](np.stack([np.log(np.clip(cs, F["CG"][0], F["CG"][-1])), np.log(np.maximum(xs, F["XVG"][0])), u], 1)), 0.0)
        cf = F["supp_fdm"](Mh, m22)
        Fl.append(float(F["_trap"](w * np.clip(lc, 0, 1) * cf, np.log(F["MH"]))))
        Fbl.append(float(F["_trap"](w * bb * np.clip(lc, 0, 1) * np.clip(fe, 0, 1) * cf, np.log(F["MH"]))))
        hi.append(float(F["_trap"](w * np.clip(lc, 0, 1) * cf * (Mh >= 10 ** 10.5), np.log(F["MH"]))) / max(Fl[-1], 1e-300))
    Fl, Fbl = np.array(Fl), np.array(Fbl)
    Fc = np.maximum.accumulate(Fl[::-1])[::-1]; Fbc = np.maximum.accumulate(Fbl[::-1])[::-1]
    S_a = 1 - np.interp(1 / F["a_grid"] - 1, F["ZG"], Fbc, right=0.0)
    return dict(F=Fc, Fb=Fbc, S=S_a, hi=np.array(hi))


def S8r(S_, vk):
    return float(F["solve_hist"](S_, vk)["S8"] / F["S8_LCDM"])


# --------------------------------------------------------------------------- FP10's flagship hosts and the progenitor passage
ZF = (0.5, 1.0, 1.5, 2.0, 2.5)
HOSTS = {}
for _z in ZF:
    for _l in ((11.0,) if SMOKE else (10.0, 10.5, 11.0)):
        for _mf in ((1 / 1.5, 1.0, 1.5) if (_z == 2.5 and not SMOKE) else (1.0,)):
            _H = F["flag_host"](_l, _mf, _z)
            _Pp = F["prof_bary"](_H["Mh"], _H["c"], _z, F["hernquist"](_H["Mb"], _H["a"]))
            _H["r200"] = _Pp["r200"]; _H["Pp"] = _Pp
            HOSTS[(_z, _l, round(_mf, 3))] = _H
DB = F["depth_bary"]
DB_DEF = DB.__defaults__


def set_trigger(zeta, q):
    """FP10's depth_bary reads its trigger constants from its defaults; set them (FP10's code runs unedited)."""
    DB.__defaults__ = (240, float(zeta), float(q))


def passages(zeta, q, alphas=(0.6, 0.8, 1.0), dz=0.25, yieldgate=False, kicks=VKS, sep="H_Y"):
    """FP10's progenitor passage for every host: the first (highest) z' at which the conversion radius covers r_F, and the
    intact progenitor's v_esc(r_F) there.  yieldgate: the radius is min(FP10's stimulated front, the yield radius r_Y)."""
    set_trigger(zeta, q)
    rows = []
    for key_, H_ in HOSTS.items():
        for al in alphas:
            zs, rs_, Phis = F["progenitor"](H_, al, dz=dz)
            rY = {}
            if yieldgate:
                for f_ in FEET:
                    arr = []
                    for i, zq in enumerate(zs):
                        M = H_["Mh"] * math.exp(-al * (zq - H_["z"]))
                        Mb, a = (H_["Mb"], H_["a"]) if i == 0 else F["galaxy_baryons"](M, float(zq), H_["mf"])
                        arr.append(r_yield(Mb, a, float(zq), f_, sep=sep))
                    rY[f_] = np.array(arr)
            for v_ in kicks:
                for K_ in KS:
                    for f_ in FEET:
                        rad = rs_[(v_, K_)] if not yieldgate else np.minimum(rs_[(v_, K_)], rY[f_])
                        zp, ve = F["passage"](zs, rad, Phis, H_["rF"][f_])
                        rows.append(dict(host=key_, alpha=al, vk=v_, K=K_, foot=f_, z_pass=zp, v_esc=ve, escaped=bool(ve < v_)))
    DB.__defaults__ = DB_DEF
    return rows


def scoring_front(H_, zeta, q, vk, K, foot=None, yieldgate=False):
    set_trigger(zeta, q)
    r_, S_ = DB(H_["Pp"], vk)
    DB.__defaults__ = DB_DEF
    fr = F["front"](r_, S_, 1.0 / K)
    if yieldgate:
        fr = min(fr, r_yield(H_["Mb"], H_["a"], H_["z"], foot))
    return fr


def flag_S(H_, rv, vk, mode, N=10000):
    """FP10's retention modes at the scoring epoch (its ret_job, same calls): 'surface' (the in-place population left in the
    progenitor, the history reading), 'self' and 'intact' (in place)."""
    Mb_fn = F["hernquist"](H_["Mb"], H_["a"]); gates = [H_["rF"][f_] for f_ in FEET]
    if mode == "self":
        return np.asarray(F["retained_fk1"](Mb_fn, H_["Mh"], H_["c"], gates, rv, vk, H_["rhoc"], N=N, iters=2)[0], float)
    if mode == "intact":
        return np.asarray(F["retained_fk1"](Mb_fn, H_["Mh"], H_["c"], gates, rv, vk, H_["rhoc"], N=N, iters=0)[0], float)
    if rv >= 0.999 * H_["r200"]:
        return np.zeros(2)
    return np.maximum(F["retained_fk1"](Mb_fn, H_["Mh"], H_["c"], gates, rv, vk, H_["rhoc"], N=N, iters=2, drop_inplace=True)[0],
                      F["retained_fk1"](Mb_fn, H_["Mh"], H_["c"], gates, rv, vk, H_["rhoc"], N=N, iters=0, drop_inplace=True)[0])


def flag_shift_max(H_, S_pair):
    return max(abs(F["flag_shift"](H_["z"], H_["Mb"], H_["Mh"], f_, S_pair[i_], nuf)) for i_, f_ in enumerate(FEET) for _, nuf in F["KERNELS"])


# ================================================================================================ C0 controls
banner("C0  CONTROLS: the loaded machinery reproduces committed numbers")
J10 = J["FP10"]
_b = F["budget"](600.0, K_MID)
_ref = J10["A6"]["budget"]["600|185"]
dev_bud = max(max(abs(a_ - b_) for a_, b_ in zip(_b["F"], _ref["F"])), max(abs(a_ - b_) for a_, b_ in zip(_b["Fb"], _ref["Fb"])))
s8c = S8r(_b["S"], 600.0)
dev_s8 = abs(s8c - J10["B6"]["rows"]["600|185|fluid"]["ratio"])
_Hc = HOSTS[(2.5, 11.0, 1.0)]
_pc = passages(1.0, FK1_Q, alphas=(0.8,), kicks=(575.0,))
_row = [r_ for r_ in J10["B1_rows"] if r_["z"] == 2.5 and r_["lMb"] == 11.0 and abs(r_["mf"] - 1.0) < 1e-9 and r_["vk"] == 575.0 and r_["foot"] == "canonical"][0]
_mine = [r_["z_pass"] for r_ in _pc if r_["host"] == (2.5, 11.0, 1.0) and r_["foot"] == "canonical"]
dev_pass = max(abs(a_ - b_) for a_, b_ in zip(_mine, _row["z_pass"][3:6]))
check("C0a CONTROL: FP10's machinery -- budget(600 km/s, K_mid) bit-identical to FP10's committed A6 row, L319's S_8 ratio equal to "
      "its B6 row, and the progenitor passage of the 1e11 z = 2.5 host (alpha = 0.8, 575 km/s, three K) equal to its committed B1 row",
      f"budget max |dev| {dev_bud:.1e}; S_8 {s8c:.6f} (|dev| {dev_s8:.1e}); passage z' {[round(x_, 4) for x_ in _mine]} vs "
      f"{[round(x_, 4) for x_ in _row['z_pass'][3:6]]} (|dev| {dev_pass:.1e})", dev_bud == 0.0 and dev_s8 < 1e-12 and dev_pass < 1e-9)
_S12, _F12 = X["fk1_history"](zeta=1.0, m_min=1e8)
_pr12 = X["proxies"](_S12, 600.0)
_cal12 = {z_: _pr12[z_]["p1d_kF5"] / KCAL for z_ in ("3.0", "2.0")}
_ref12 = J["XR12"]["H2"]["nominal 5.31, M_min 1e8, 600"]["calibrated"]
_mine12 = forest_eval(1.0, FK1_Q, ("hard", 1e8))
dev12 = max(abs(_cal12[z_] - _ref12[z_]) for z_ in _ref12)
dev12g = max(abs(_mine12["cal"][z_] - _cal12[z_]) for z_ in _cal12)
check("C0b CONTROL: XR12's calibrated gas-proxy forest (its fk1_history, proxies and committed calibration) reproduces its committed "
      "H2 nominal row, and this lane's generalised evaluator at q = 7/4 with XR12's hard cut is identical to it",
      f"z = 2/3: {_cal12['2.0']:.5f}/{_cal12['3.0']:.5f} vs committed {_ref12['2.0']:.5f}/{_ref12['3.0']:.5f} (|dev| {dev12:.1e}); "
      f"generalised |dev| {dev12g:.1e}", dev12 < 1e-9 and dev12g < 1e-12)
_a1 = [float(Rtm(z_, 1.0, FK1_Q)) for z_ in (0, 0.5, 1, 2, 2.5, 3, 4, 6)]
_a1ref = [5.3, 4.8, 6.8, 16.5, 24.8, 35.8, 67.7, 182.0]
_bg = [(1.0 / float(Rtm(z_, 1.0, FK1_Q))) ** 2 for z_ in np.linspace(0, 6, 601)]
_zpk = float(np.linspace(0, 6, 601)[int(np.argmax(_bg))])
dev_a1 = max(abs(a_ - b_) / b_ for a_, b_ in zip(_a1, _a1ref))
check("C0c CONTROL: this lane's trigger-to-mean ratio R(z) at FK1's cell reproduces XR12's committed A1 table (5.3/4.8/6.8/16.5/24.8/"
      "35.8/67.7/182 at z = 0/0.5/1/2/2.5/3/4/6) and FP10's A4 background peak (z = 0.30, N_bg/E_need = 0.048)",
      f"R = {[round(x_, 2) for x_ in _a1]} (max rel dev {dev_a1:.1e}); peak z {_zpk:.2f} at {max(_bg):.4f}",
      dev_a1 < 0.01 and abs(_zpk - 0.30) < 0.02 and abs(max(_bg) - J10["A4"]["bg_max"]) < 1e-3)
_yref = J["FP9"]["H2"]["y_th"]
dev_y = max(abs(y_th(float(k_)) / v_ - 1) for k_, v_ in _yref.items())
check("C0d CONTROL: FP9's committed yield y_th(z) at z = 0/0.25/1/2/2.5/3 and its band-pass length (L(0.25) = 1.3 Mpc, L(2.5) = 119 kpc) "
      "are reproduced from FP9's headline constants (y_th(0.25) = 1e-6, p' = 4, L(0.25) = 1.3 Mpc, n = 2) on its cosmology",
      f"max rel dev {dev_y:.1e}; L(0.25) {L_kpc(0.25):.1f} kpc, L(2.5) {L_kpc(2.5):.1f} kpc, L(0) {L_kpc(0.0):.0f} kpc",
      dev_y < 1e-9 and abs(L_kpc(0.25) - 1300) < 1e-6 and abs(L_kpc(2.5) - 119.3) < 0.5)
OUT["numbers"]["C0"] = dict(budget=dev_bud, S8=dev_s8, passage=dev_pass, XR12=dev12, XR12_general=dev12g, A1=_a1, bg_peak=[_zpk, max(_bg)], y_th=dev_y)
P(f"  controls done   {elapsed()}")

# ================================================================================================ PART T: trigger sharing
banner("T1  THE K-GATE IS A POWER OF THE SEPARATOR'S Omega_L(<K>_h): the running variable is shared; the exponent is not fixed")
Ks, H0s, Lams, qs, pps, l0s = sp.symbols("K H_0 Lambda q p' lambda_0", positive=True)
OmL_K = 3 * Lams / Ks ** 2                                            # Omega_L(<K>_h) = Lambda c^2/(3 (K/3)^2), c = 1
OmL_0 = Lams / (3 * H0s ** 2)
gate_fk1 = (Ks / (3 * H0s)) ** (-2 * qs)
t1_id = sp.simplify(sp.powsimp(sp.expand_power_base(gate_fk1 / (OmL_K / OmL_0) ** qs, force=True), force=True)) == 1
Hs, Dl, En = sp.symbols("H Delta E_need", positive=True)
n_t = sp.sqrt(Hs) * Hs ** (2 * qs)                                    # FP10 A4: n_t ~ sqrt(H Delta E_need)/lambda(K) ~ H^(2q + 1/2)
OmLH = sp.symbols("Omega_L", positive=True)                           # on FRW Omega_L = Omega_L0 (H_0/H)^2
nt_OmL = sp.simplify(sp.expand_power_base(n_t.subs(Hs, H0s * sp.sqrt(sp.Symbol("Omega_L0", positive=True) / OmLH)), force=True))
exp_nt = sp.simplify(sp.diff(sp.log(nt_OmL), OmLH) * OmLH)            # d ln n_t / d ln Omega_L
exp_ratio = sp.simplify(exp_nt + 1)                                   # rho_crit(z) ~ Omega_L^(-1)
p9 = float(J["FP9"]["constants"][3][1]) if isinstance(J["FP9"]["constants"][3][1], str) and J["FP9"]["constants"][3][0] == "p'" else HEAD9["pp"]
ids = {"n_t ~ y_th (absolute threshold runs as the yield)": sp.solve(sp.Eq(exp_nt, -pps), qs)[0],
       "lambda ~ 1/y_th (the coupling runs as the inverse yield)": sp.solve(sp.Eq(-qs, -pps), qs)[0],
       "rho_t/rho_crit(z) ~ y_th (FP10's convention q = p + 3/4)": sp.solve(sp.Eq(exp_ratio, -pps), qs)[0]}
Q_SH = {k_: float(v_.subs(pps, p9)) for k_, v_ in ids.items()}
if MUTATE:
    Q_SH = {k_: FK1_Q for k_ in Q_SH}
P(f"    (K/3H_0)^(-2q) / (Omega_L(K)/Omega_L0)^q = 1 identically on CMC leaves (K = <K>_h = 3H): {t1_id}")
P(f"    trigger density n_t ~ H^(2q + 1/2) = Omega_L^({exp_nt}); in rho_crit(z) units Omega_L^({exp_ratio}); FP9's yield y_th ~ Omega_L^(-p'), p' = {p9:g}")
for k_, v_ in ids.items():
    P(f"      identification [{k_}]: q = {v_} = {float(v_.subs(pps, p9)):.2f}" + ("   (MUTATE: replaced by 1.75)" if MUTATE else ""))
t1_ok = t1_id and sp.simplify(exp_nt + qs + sp.Rational(1, 4)) == 0 and len(set(round(float(v_.subs(pps, p9)), 6) for v_ in ids.values())) == 3
check("T1 DERIVED: on CMC leaves FK1's K-gate (K/3H_0)^(-2q) IS (Omega_L(<K>_h)/Omega_L0)^q -- the separator's own variable, so the "
      "running VARIABLE is already shared; but the action does not fix the EXPONENT: three inequivalent identifications with FP9's "
      "y_th ~ Omega_L^(-p') give q = p' - 1/4, p', p' + 3/4 = 3.75, 4, 4.75, and none is selected by a term of the action",
      f"identity {t1_id}; n_t ~ Omega_L^({exp_nt}); q = {sorted(set(round(float(v_.subs(pps, p9)), 3) for v_ in ids.values()))}", t1_ok,
      "sharing the variable costs nothing; sharing the exponent is a choice among three -- it would remove q only if the web and "
      "the gates accepted the result (T3)")
OUT["numbers"]["T1"] = dict(identity=bool(t1_id), n_t_exponent=str(exp_nt), ratio_exponent=str(exp_ratio), q_shared=Q_SH, p_prime=p9)

banner("T1b CAN lambda_0's NORMALISATION BE SHARED? the framework's own maps from the yield (an acceleration) to a density")
# (i) the framework's law read backwards: a0^2 = kappa^2 c^2 G rho_Lambda  =>  an acceleration y a0 is 'the density' y^2 rho_Lambda
# (ii) the band-pass length as the missing scale: y a0/(4 pi G L(z)) (the phantom density of the field y a0 over L)
RC0_9 = 3 * _H09 ** 2 / (8 * math.pi * G_SI)
rho_t25_band = [zq * (5.0 / 3.0) * E25 ** 4 for zq in (2.4, ZW2["canonical"][1])]        # FP10's rho_t(2.5) at q = 7/4, rho_crit0 units
rho_i = y_th(2.5) ** 2 * OL9                                                             # (i): y^2 rho_Lambda, rho_crit0 units
rho_ii = {f_: y_th(2.5) * A0_FP0[f_] / (4 * math.pi * G_SI * L_kpc(2.5) * KPC_M) / RC0_9 for f_ in FEET}
rho_ii1 = {f_: A0_FP0[f_] / (4 * math.pi * G_SI * L_kpc(2.5) * KPC_M) / RC0_9 for f_ in FEET}   # the same with y -> 1
dec_i = math.log10(rho_t25_band[0] / rho_i)
P(f"    the trigger the flagship and forest need at z = 2.5: rho_t = {rho_t25_band[0]:.0f}-{rho_t25_band[1]:.0f} rho_crit0 (zeta_eq 2.4-2.76, q = 7/4)")
P(f"    (i)  y_th(2.5)^2 rho_Lambda = {rho_i:.2e} rho_crit0: {dec_i:.1f} decades too low (the whole universe would convert); it runs as "
  f"Omega_L^(-2p') = E^(4p') (q = {2 * p9 - 0.25:.2f})")
P(f"    (ii) y_th(2.5) a0/(4 pi G L(2.5)) = {rho_ii['canonical']:.0f}/{rho_ii['alt']:.0f} rho_crit0; with y -> 1: {rho_ii1['canonical']:.0f}/"
  f"{rho_ii1['alt']:.0f} (x{rho_ii1['canonical'] / rho_t25_band[0]:.1f} the band) -- the right order only with an O(1) coefficient put in, and it "
  f"runs as 1/L ~ Omega_L^(-n/2) = E^2: q = 3/4, the background's marginal value, where the forest band is closed (T3b)")
t1b_ok = dec_i > 5.0
check("T1b DERIVED: lambda_0's normalisation cannot be shared with the yield: the framework's one m-free map from an acceleration to a "
      "density, a0^2 = kappa^2 c^2 G rho_Lambda, turns y_th(2.5) a0 into y_th^2 rho_Lambda, >= 5 decades below the trigger the flagship "
      "and the forest need at z = 2.5; the band-pass length gives a0/(4 pi G L) of the right order only with a coefficient put in and "
      "the running q = 3/4 (the marginal background value)",
      f"(i) {rho_i:.1e} vs {rho_t25_band[0]:.0f} rho_crit0 ({dec_i:.1f} decades); (ii) y -> 1: x{rho_ii1['canonical'] / rho_t25_band[0]:.1f}, "
      f"with y_th: x{rho_ii['canonical'] / rho_t25_band[0]:.2f}", t1b_ok,
      "zeta stays a constant of the dark sector; its value is set by data (M1, T3b)")
OUT["numbers"]["T1b"] = dict(rho_t25=rho_t25_band, map_i=rho_i, decades=dec_i, map_ii=rho_ii, map_ii_y1=rho_ii1)

banner("T2  THE ANCHOR LAW: with the threshold pinned at z = 2.5, how the trigger sits against the web at every other epoch")
zs_, za_, qq_ = sp.symbols("z z_a q", positive=True)
Oms, OLs = sp.symbols("Omega_m Omega_L", positive=True)
E2s = Oms * (1 + zs_) ** 3 + OLs
Rs = E2s ** ((2 * qq_ + sp.Rational(1, 2)) / 2) / (1 + zs_) ** 3
dlogR = sp.simplify(sp.diff(sp.log(Rs), zs_) * (1 + zs_))
Omz = Oms * (1 + zs_) ** 3 / E2s
dlog_target = sp.Rational(3, 2) * (2 * qq_ + sp.Rational(1, 2)) * Omz - 3
t2_form = sp.simplify(dlogR - dlog_target) == 0
q_star = 1.0 / Om - 0.25
ratio0 = {k_: float((1 + 2.5) ** 3 / E25 ** (2 * v_ + 0.5)) for k_, v_ in Q_SH.items()}
ratio0_fk1 = float((1 + 2.5) ** 3 / E25 ** (2 * FK1_Q + 0.5))
zmin_fk1 = float(((1 - Om) / (Om * (FK1_Q - 0.75))) ** (1 / 3) - 1)   # Omega_m(z) = 1/(q + 1/4)  <=>  (1+z)^3 = Omega_L/(Omega_m (q - 3/4))
P(f"    d ln R / d ln(1+z) = {dlogR}  =  (3/2)(2q + 1/2) Omega_m(z) - 3 : {t2_form}")
P(f"    R rises into the past iff Omega_m(z) > 1/(q + 1/4); at z = 0 that needs q > q* = 1/Omega_m0 - 1/4 = {q_star:.3f}: for q >= q* the "
  f"trigger's lowest point against the mean is TODAY, R(0)/R(2.5) = (3.5)^3/E(2.5)^(2q + 1/2)")
for k_, v_ in ratio0.items():
    P(f"      shared q = {Q_SH[k_]:.2f}: R(0)/R(2.5) = {v_:.3e}")
P(f"      FK1 q = 1.75: minimum at Omega_m(z) = 1/2 (z = {zmin_fk1:.2f}); R(0)/R(2.5) = {ratio0_fk1:.3f}")
t2_ok = t2_form and all(Q_SH[k_] >= q_star for k_ in Q_SH) and max(ratio0.values()) < 2e-3 and abs(zmin_fk1 - 0.30) < 0.02
check("T2 DERIVED: with the threshold held at z = 2.5 (the flagship's anchor), d ln R/d ln(1+z) = (3/2)(2q + 1/2) Omega_m(z) - 3, so "
      "for q >= 1/Omega_m0 - 1/4 = 2.94 the trigger's closest approach to the cosmic mean is at z = 0; every shared exponent sits above "
      "that line and brings the threshold down by (3.5)^3/E(2.5)^(2q + 1/2) <= 1.1e-3 between z = 2.5 and today (FK1's q = 7/4: its "
      "minimum at z = 0.30, 0.21)",
      f"form {t2_form}; q* = {q_star:.3f}; shared R(0)/R(2.5) = {', '.join(f'{v_:.2e}' for v_ in ratio0.values())}; FK1 {ratio0_fk1:.3f} "
      f"(min at z = {zmin_fk1:.2f})", t2_ok,
      "a running steep enough to switch the forest-epoch conversion off (the separator's job) must switch the late web on: that is "
      "the price XR19's runaway measures")
OUT["numbers"]["T2"] = dict(q_star=q_star, R0_over_R25=ratio0, fk1=ratio0_fk1, fk1_zmin=zmin_fk1)

banner("T3  EVERY SHARED EXPONENT ON THE WEB, at every flagship anchor on the record (W2's resolved bound; FP10's no-cap reach)")
# FP10's no-cap reach: the largest zeta_eq at which the scoring-epoch stimulated front (K) still covers r_F, over the z = 2.5 hosts
REACH = {}
for K_ in KS:
    for f_ in FEET:
        best = math.inf
        for key_, H_ in HOSTS.items():
            if key_[0] != 2.5:
                continue
            fn = lambda lz: scoring_front(H_, math.exp(lz), FK1_Q, 600.0, K_) - H_["rF"][f_]
            lo, hi_ = math.log(1.0), math.log(3000.0)
            if fn(lo) < 0:
                best = min(best, 1.0); continue
            for _ in range(40):
                mid = 0.5 * (lo + hi_)
                lo, hi_ = (mid, hi_) if fn(mid) >= 0 else (lo, mid)
            best = min(best, math.exp(lo))
        REACH[(K_, f_)] = best
P("    FP10's no-cap reach (scoring-epoch front covers r_F on every z = 2.5 host): " +
  "; ".join(f"K {k_[0]:.0f}/{k_[1]}: zeta_eq <= {v_:.1f}" for k_, v_ in REACH.items()))
ANCH = {"W2 canonical (streams C_s=10)": ZW2["canonical"][0], "W2 canonical (+ upstream)": ZW2["canonical"][1],
        "W2 alt (streams C_s=10)": ZW2["alt"][0], "W2 alt (+ upstream)": ZW2["alt"][1]}
for (K_, f_), v_ in REACH.items():
    ANCH[f"FP10 reach K={K_:.0f} {f_}"] = v_
EN = E_NEED["2e-19"]
T3 = {}
for k_, q_ in list(Q_SH.items()) + [("FK1 q = 7/4", FK1_Q)]:
    T3[k_] = {an: web(zeq, q_, EN) for an, zeq in ANCH.items()}
for k_, rows in T3.items():
    P(f"    {k_} (q = {Q_SH.get(k_, FK1_Q):.2f}):")
    for an, w_ in rows.items():
        P(f"      {an:34s} zeta {w_['zeta']:.3g}: R_min {w_['R_min']:8.3g} at z {w_['z_min']:.2f}; mean converts spont. z<= {w_['mean_spont']}, "
          f"seeded z<= {w_['mean_seeded']}; walls(d=2) {w_['walls']}; filaments(d=10) {w_['filaments']}; cone {w_['filaments_cone']}")
sh_fil = all(w_["filaments"] is not None for k_, rows in T3.items() if k_ != "FK1 q = 7/4" for w_ in rows.values())
sh_mean_w2 = all(T3[k_][an]["mean_spont"] is not None for k_ in Q_SH for an in ANCH if an.startswith("W2"))
fk1_w2 = min(T3["FK1 q = 7/4"][an]["R_min"] for an in ANCH if an.startswith("W2 canonical"))
fk1_fil_w2 = [T3["FK1 q = 7/4"][an]["filaments"] for an in ANCH if an.startswith("W2")]
worse = min(T3["FK1 q = 7/4"][an]["R_min"] / max(T3[k_][an]["R_min"], 1e-300) for k_ in Q_SH for an in ANCH)
mean_epochs = [T3[k_][an]["mean_spont"] for k_ in Q_SH for an in ANCH if an.startswith("W2")]
check("T3 THE SHARED EXPONENT FAILS ON THE WEB: at every flagship anchor on the record (XR12-W2's resolved bound, both footings; FP10's "
      "no-cap reach at K = 36-947) every shared q (3.75, 4, 4.75) puts delta = 10 filaments above the trigger (spontaneous conversion) "
      "at some z <= 2, and at W2's anchor the cosmic MEAN itself crosses -- FP10's own A4 requirement (no background conversion) "
      "fails at z <= 0.9-1.4; FK1's q = 7/4 keeps R_min >= 11.6 > 11 at W2's canonical anchors (no spontaneous filament conversion); "
      "the shared gate lowers the web's margin by >= 30x at every anchor: it makes XR19's runaway categorically worse",
      f"filaments cross for every shared q at every anchor: {sh_fil}; mean crosses at W2: {sh_mean_w2} (z <= "
      f"{min(x_ for x_ in mean_epochs if x_ is not None) if any(x_ is not None for x_ in mean_epochs) else None}-"
      f"{max(x_ for x_ in mean_epochs if x_ is not None) if any(x_ is not None for x_ in mean_epochs) else None}); FK1 R_min at W2 "
      f"canonical {fk1_w2:.1f} (filaments {fk1_fil_w2}); FK1/shared R_min >= {worse:.1f}",
      sh_fil and sh_mean_w2 and fk1_w2 >= 11.0 and all(x_ is None for x_ in fk1_fil_w2) and worse >= 30.0,
      "the separator's running is steep (E^8) because the forest needs the MOND scalar off at z = 2-3 and on at 2.5 in galaxies; "
      "the same steepness in the dark trigger, anchored where the flagship needs it, drops the threshold under the late web")
OUT["numbers"]["T3"] = dict(anchors=ANCH, reach={f"{k_[0]:.0f}|{k_[1]}": v_ for k_, v_ in REACH.items()},
                            web={k_: rows for k_, rows in T3.items()})
P(f"    {elapsed()}")

banner("T3b THE q-WINDOW: the forest's band (XR12's calibrated proxy at the dark-mass floor) x the web x A4 x the flagship's passage")
Q_SCAN = (1.25, 1.75, 3.75) if SMOKE else (1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 3.75, 4.0, 4.75)
CUT_FLOOR = ("hard", 1e8) if MUTATE else ("fdm", 1.9e-19)
TOPS = {"canonical": ZW2["canonical"][1], "alt": ZW2["alt"][1]}
QW = {}
for q_ in Q_SCAN:
    row = {}
    for f_, zt in TOPS.items():
        fe_ = forest_eval(zeta_of(zt, q_), q_, CUT_FLOOR)
        w_ = web(zt, q_, EN)
        Rr = min(R_rad(z_, zt, q_) for z_ in np.geomspace(1e-3, 1e5, 4000))
        row[f_] = dict(forest=fe_["worst"], open=fe_["worst"] <= 0.10, R_min=w_["R_min"], A4=Rr >= 1.0, R_min_rad=Rr,
                       fil_safe=w_["filaments"] is None, seeded_mean=w_["mean_seeded"])
    rows_p = passages(zeta_of(TOPS["canonical"], q_), q_, alphas=(0.6, 1.0) if SMOKE else (0.6, 0.8, 1.0), kicks=(575.0,))
    row["passage"] = dict(escaped=sum(r_["escaped"] for r_ in rows_p), n=len(rows_p), vmax=max(r_["v_esc"] for r_ in rows_p),
                          zmin=min(r_["z_pass"] for r_ in rows_p))
    QW[q_] = row
    P(f"    q {q_:4.2f}: " + "; ".join(f"{f_} top {TOPS[f_]:.2f}: forest {row[f_]['forest']:.3f} ({'open' if row[f_]['open'] else 'CLOSED'}), "
                                        f"R_min {row[f_]['R_min']:.3g} (A4 {'ok' if row[f_]['A4'] else 'FAIL'}, filaments "
                                        f"{'safe' if row[f_]['fil_safe'] else 'CONVERT'}, seeded mean z<= {row[f_]['seeded_mean']})"
                                        for f_ in FEET)
      + f"; flagship passage escaped {row['passage']['escaped']}/{row['passage']['n']} (v_esc <= {row['passage']['vmax']:.0f} km/s, z' >= "
        f"{row['passage']['zmin']:.2f})   {elapsed()}")
EDGE = {}
for q_ in ((1.75,) if SMOKE else (1.75, 2.5)):
    e_, vals = zeta_forest_edge(q_, CUT_FLOOR, (1.0, 1.5, 2.0, 2.5, 2.76, 3.5, 4.29, 6.0))
    EDGE[q_] = dict(edge=e_, scan=vals)
    P(f"    forest edge at q = {q_}: zeta_eq >= " + ("(never on the grid)" if e_ is None else (f"<= {vals[0][0]} (the grid's first point passes)" if e_ == 0.0 else f"{e_:.3f}"))
      + f" (scan {[(z_, round(w_, 4)) for z_, w_ in vals]})")
win_can = [q_ for q_ in Q_SCAN if QW[q_]["canonical"]["open"] and QW[q_]["canonical"]["A4"]]
win_can_fil = [q_ for q_ in win_can if QW[q_]["canonical"]["fil_safe"]]
win_alt = [q_ for q_ in Q_SCAN if QW[q_]["alt"]["open"] and QW[q_]["alt"]["A4"]]
win_alt_fil = [q_ for q_ in win_alt if QW[q_]["alt"]["fil_safe"]]
check("T3b (reported) THE q-WINDOW at the dark-mass floor (m = 1.9e-19 eV): the forest closes the band for shallow runnings (early "
      "conversion) and the web for steep ones; FK1's q = 7/4 sits in the narrow overlap; the flagship's progenitor passage escapes "
      "in every scanned cell (the anchor keeps it)",
      f"canonical: band open & A4 {win_can}, + filaments safe {win_can_fil}; alt: {win_alt} / {win_alt_fil}; edges {({k_: v_['edge'] for k_, v_ in EDGE.items()})}",
      True, "q is not shared and not free: a window set by data, degenerate with zeta at z = 2.5 (the anchor) and fixed at the ends by "
            "the forest (below) and the web (above)", load_bearing=False)
OUT["numbers"]["T3b"] = dict(scan={str(k_): v_ for k_, v_ in QW.items()}, edges={str(k_): v_ for k_, v_ in EDGE.items()},
                             window=dict(canonical=win_can, canonical_fil=win_can_fil, alt=win_alt, alt_fil=win_alt_fil))

banner("T3c (reported) THE SHARED CELLS' OTHER GATES under the web bracket: S_8, X-COP and Harvey in FP10's optimistic reading")
T3C = {}
for k_, q_ in Q_SH.items():
    zt = zeta_of(TOPS["canonical"], q_)
    wb_ = T3[k_]["W2 canonical (+ upstream)"]
    b_ = F["budget"](600.0, K_MID, ft=zt, qg=q_)
    s8_halo = S8r(b_["S"], 600.0)
    zw_list = [x_ for x_ in (wb_["mean_spont"], wb_["filaments"]) if x_ is not None]
    s8_web = {}
    for zw in zw_list:
        bw = F["budget"](600.0, K_MID, ft=zt, qg=q_, z_web=zw)
        s8_web[zw] = S8r(bw["S"], 600.0)
    Fb_cl = 1.0 if wb_["mean_spont"] is not None else float(np.interp(F["CLREF"]["z"], F["ZG"], b_["Fb"]))
    e_self = {v_: J10["B3"]["fk1"][f"{v_:.0f}"]["eps_self"] for v_ in VKS}
    xc_opt = {v_: F["xcop_from_eps"](max(e_self[v_] - Fb_cl, 0.0)) for v_ in VKS}
    us = 1.0 - (1.0 if wb_["mean_spont"] is not None and wb_["mean_spont"] >= 0.4 else float(np.interp(0.4, F["ZG"], b_["Fb"])))
    T3C[k_] = dict(q=q_, zeta=zt, S8_halo=s8_halo, S8_web=s8_web, xcop_opt={f"{v_:.0f}": (x_["canonical"]["ratio"], x_["alt"]["ratio"]) for v_, x_ in xc_opt.items()},
                   harvey_us=us, share_hi={z_: float(b_["hi"][list(F["ZG"]).index(z_)]) for z_ in (2.0, 3.0, 4.0) if z_ in list(F["ZG"])},
                   F_z={z_: float(np.interp(z_, F["ZG"], b_["F"])) for z_ in (4.0, 3.0, 2.0)})
    P(f"    {k_} (q {q_:.2f}, zeta {zt:.3g}): S_8 halo-only {s8_halo:.4f}; with the web converting at z_web = "
      + ", ".join(f"{zw:.2f}: {s_:.4f}" for zw, s_ in s8_web.items()) + f" (strict >= 0.922); X-COP optimistic (F_b -> {Fb_cl:.2f}) "
      + ", ".join(f"{v_}: {a_:.2f}/{b__:.2f}" for v_, (a_, b__) in T3C[k_]["xcop_opt"].items()) + f" (0.8-1.2); Harvey uniform factor {us:.2f} "
      f"(FP10: 650 fails at 0.499, 575 passes at 0.514); F(4/3/2) {T3C[k_]['F_z'][4.0]:.3f}/{T3C[k_]['F_z'][3.0]:.3f}/{T3C[k_]['F_z'][2.0]:.3f}")
check("T3c (reported) the shared cells' other gates: with the web converting, S_8 falls below the strict ratio in both of FP10's "
      "maximal-web brackets (above the alt floor), and FP10's only passing cluster reading (optimistic) loses X-COP (too little mass) "
      "and Harvey (hollow cores)",
      {k_: dict(S8_web={f"{zw:.2f}": round(s_, 4) for zw, s_ in v_["S8_web"].items()}, xcop=v_["xcop_opt"], us=round(v_["harvey_us"], 3)) for k_, v_ in T3C.items()},
      True, "the in-place cluster reading fails for every trigger (FP10 L11l: one splitting cannot empty a cluster); the optimistic "
            "one needs the escaped fraction near ~0.5, not the web's ~1", load_bearing=False)
OUT["numbers"]["T3c"] = T3C
P(f"    {elapsed()}")

banner("T4a THE YIELD ONSET AS THE TRIGGER: lambda -> lambda_0 g(Y) with g reading the MOND scalar (sympy)")
Ys, yt_, ws_, ug_, a0s, Gs = sp.symbols("Y y_th w u_gate a_0 G", positive=True)
xs_ = sp.symbols("x", positive=True)
g_Y = 1 - sp.exp(-Ys / (ws_ * yt_) ** 2)
J_P2 = -sp.Rational(1, 4) * sp.log(1 - 2 * sp.sqrt(Ys)) - sp.sqrt(Ys) / 2 - Ys / 2
J_Y = J_P2 + 2 * yt_ * sp.sqrt(Ys)
# static phi-sector density (per FP9, in units where the MOND energy density is (a0^2/8 pi G) J): L = -(a0^2/8piG) J_Y(Y) - u_gate g(Y)
coef_mond = a0s ** 2 / (8 * sp.pi * Gs) * sp.diff(J_Y, Ys)
coef_gate = ug_ * sp.diff(g_Y, Ys)
delta_Y = sp.simplify(coef_gate / coef_mond)
flux = sp.simplify((sp.sqrt(Ys) * sp.diff(J_Y, Ys)).subs(Ys, xs_ ** 2))  # FP9's convention: F(x) = F_P2(x) + y_th
g0 = g_Y.subs(Ys, 0)
P(f"    J_Y = {J_Y}")
P(f"    phi's flux coefficient (a0^2/8 pi G) J_Y'(Y) + u_gate g'(Y) = (a0^2/8 pi G) J_Y' (1 + delta_Y), delta_Y = {delta_Y}")
P(f"    flux F(x) = x J_Y'(x^2) = {flux}  (-> y_th at x -> 0+);  g(Y = 0) = {g0}: on FRW (every source below the yield, FP9 Y3) and inside every "
  f"yield surface phi is frozen, so the gate is EXACTLY off -- no background and no z >= 2.5 IGM conversion at any q")
fl0 = sp.limit(flux, xs_, 0, "+")
t4a_ok = g0 == 0 and sp.simplify(fl0 - yt_) == 0
check("T4a DERIVED: a trigger gated by the MOND scalar's own on-state, -lambda_0 g(Y)(Im Phi^2)^2 with g(0) = 0 and width tied to the "
      "yield (g = 1 - exp(-Y/(w y_th)^2)), is exactly off wherever phi is frozen -- on FRW and inside every yield surface (FP9 Y3) -- so "
      "the early universe and the z >= 2.5 IGM cannot convert whatever q is: the K-running is not needed (q -> 0) and its job is done "
      "by the separator's own p' (SHARED); the price is a reciprocal source: phi's flux coefficient becomes (1 + delta_Y), "
      "delta_Y = 8 pi G u_gate g'(Y)/(a0^2 J_Y'(Y))",
      f"g(0) = {g0}; F(0+) = {fl0}; delta_Y = {delta_Y}", t4a_ok,
      "g's form (the exponential, w = 1) is a POSTULATED structure; it adds no constant only because its width is the yield's")
OUT["numbers"]["T4a"] = dict(delta_Y=str(delta_Y), flux=str(flux))

banner("T4b THE RECIPROCAL FLUX AT THE YIELD SURFACE during conversion, and the dark mass it needs")
ZB_LO = 11.0 / float(Rtm(2.0, 1.0, 0.0))                              # filaments (delta = 10) on at z = 2 (FP9 H2c) stay below
ZB_CAP = {f_: ZCAP[f_] * E25 ** 3.5 for f_ in FEET}                   # the own-density cap, anchored at z = 2.5 (q = 0)
ZB_W2 = {f_: ZW2[f_][0] * E25 ** 3.5 for f_ in FEET}
ZETA_B = math.sqrt(ZB_LO * ZB_CAP["canonical"])
xx = np.geomspace(1e-5, 0.49, 4000)
dfun = sp.lambdify((xs_, yt_, ws_), sp.simplify((sp.diff(g_Y, Ys) / sp.diff(J_Y, Ys)).subs(Ys, xs_ ** 2)), "numpy")
T4B = {}
om_m = 1.9e-19 / HBAR_EVS                                                                 # the floor mass's frequency [1/s]
Gt_om = math.sqrt((2 / math.pi) * (H0_SI * E25 / om_m) * (600.0e3 / c_SI) ** 2 * EN)     # FP10 A4: G_t at rho_t (z = 2.5)
for f_ in FEET:
    H_ = HOSTS[(2.5, 11.0, 1.0)]
    rY = r_yield(H_["Mb"], H_["a"], 2.5, f_)
    c_, r200, rs = H_["c"], H_["r200"], H_["r200"] / H_["c"]
    rho_Y = 200.0 / 3.0 * c_ ** 3 / F["mfn"](c_) / ((rY / rs) * (1 + rY / rs) ** 2) * Ez2(2.5)       # rho_crit0 units
    rho_L = 0.5 * (1 - F["FB"]) * rho_Y                                                    # mid-conversion daughter density
    for zb in (ZB_LO, ZETA_B, ZB_CAP["canonical"]):
        rho_t25 = zb * (5.0 / 3.0) * E25 ** 0.5                                            # q = 0 threshold at z = 2.5 [rho_crit0]
        Gp_om = Gt_om * max(rho_Y / rho_t25, 1.0)                                          # G ~ lambda n: the local pump rate
        u_gate = 2 * Gp_om * rho_L * RHO_CRIT * c_SI ** 2                                  # u_gate = 2 (G_p/omega_m) rho_L c^2 [J/m^3]
        pref = 8 * math.pi * G_SI * u_gate / A0_FP0[f_] ** 2
        dmax = float(np.max(dfun(xx, y_th(2.5), 1.0))) * pref
        m_rec = 1.9e-19 * (dmax / 0.1) ** 2                                                # delta ~ G_p/omega_m ~ m^(-1/2)
        T4B[(f_, zb)] = dict(r_Y=rY, rho_Y=rho_Y, Gp_over_om=Gp_om, delta_max=dmax, m_rec=m_rec)
        P(f"    {f_}: flagship 1e11 at z = 2.5: r_Y {rY:.1f} kpc ({rY / r200:.2f} r200), rho(r_Y) {rho_Y:.0f} rho_crit0; zeta {zb:.0f} (q = 0): "
          f"G_p/(m c^2/hbar) {Gp_om:.2e} -> delta_Y,max {dmax:.3g} at m = 1.9e-19 eV (w = 1); <= 0.1 needs m >= {m_rec:.1e} eV")
dmin = min(v_["delta_max"] for v_ in T4B.values())
check("T4b (reported, CONSTRAINT) during the conversion the gate's reciprocal flux at the yield surface exceeds the MOND flux there at "
      "the dark-mass floor (delta_Y >> 1, a thin transient shell at x ~ w y_th, where the MOND field is weakest; r_F lies well inside "
      "it, x(r_F)/y_th ~ 15, g' ~ e^-225); it falls as m^(-1/2) at fixed trigger density, so delta_Y <= 0.1 needs a dark mass far "
      "above the floor",
      f"delta_Y,max {dmin:.3g}-{max(v_['delta_max'] for v_ in T4B.values()):.3g}; m >= {min(v_['m_rec'] for v_ in T4B.values()):.1e}-"
      f"{max(v_['m_rec'] for v_ in T4B.values()):.1e} eV", dmin > 1.0,
      "the flagship itself is not moved (Gauss: the shell sits outside r_F); what the shell does to the MOND region's edge during "
      "conversion is not scored by any gate on the record", load_bearing=False)
OUT["numbers"]["T4b"] = {f"{k_[0]}|{k_[1]:g}": v_ for k_, v_ in T4B.items()}

def yield_flag(zeta, sep, rows, N):
    """FP10's flagship convention (its ret_job/B1 rows) for the yield-onset trigger, on EVERY host at its scoring epoch: r_v =
    min(FP10's stimulated front at K_LO, the yield radius r_Y); S = the history (surface) retention if every progenitor passage of
    that host and kick escaped, else FP10's pessimistic max(self, intact); the 1e11 z = 2.5 host also reports self and intact."""
    out = {}
    for key_, H_ in HOSTS.items():
        for v_ in VKS:
            rv = min(scoring_front(H_, zeta, 0.0, v_, K_LO), min(r_yield(H_["Mb"], H_["a"], H_["z"], f_, sep=sep) for f_ in FEET))
            esc_h = all(r_["escaped"] for r_ in rows if r_["host"] == key_ and r_["vk"] == v_)
            rep = {}
            if (not esc_h) or key_ == (2.5, 11.0, 1.0):
                for md in ("self", "intact"):
                    rep[md] = flag_S(H_, rv, v_, md, N=N)
            S_h = flag_S(H_, rv, v_, "surface", N=N) if esc_h else np.maximum(rep["self"], rep["intact"])
            out[(key_, v_)] = dict(rv=rv / H_["r200"], escaped=esc_h, S=list(S_h), shift=flag_shift_max(H_, S_h),
                                   **{md: flag_shift_max(H_, S_) for md, S_ in rep.items()})
    return out


def yield_flag_summary(FLX):
    per_kick = {v_: max(d_["shift"] for (k_, vv), d_ in FLX.items() if vv == v_) for v_ in VKS}
    worst = max(FLX.items(), key=lambda kv: kv[1]["shift"])
    return per_kick, worst


banner("T4c THE FLAGSHIP UNDER THE YIELD ONSET: when the MOND scalar reaches r_F in the progenitors, and what is left at r_F")
P(f"    the yield-onset trigger's zeta window (q = 0): filaments at z = 2 need zeta >= {ZB_LO:.1f} (cone {ZB_LO / 0.21:.0f}; seeded "
  f"{ZB_LO * math.sqrt(EN):.0f}); the flagship's own-density cap zeta <= {ZB_CAP['canonical']:.0f}/{ZB_CAP['alt']:.0f} (W2 streams "
  f"{ZB_W2['canonical']:.0f}/{ZB_W2['alt']:.0f}); the lane's cell zeta = {ZETA_B:.1f} (geometric centre, canonical)")
rows_B = passages(ZETA_B, 0.0, alphas=(0.6, 1.0) if SMOKE else (0.6, 0.8, 1.0), yieldgate=True)
esc_B = all(r_["escaped"] for r_ in rows_B)
vmaxB = max(r_["v_esc"] for r_ in rows_B)
zp_B = [r_["z_pass"] for r_ in rows_B if r_["host"][0] == 2.5]
FLB = yield_flag(ZETA_B, "H_Y", rows_B, 3000 if SMOKE else 10000)
fl_kick_B, worst_B = yield_flag_summary(FLB)
for (key_, v_), d_ in FLB.items():
    if key_[0] == 2.5 or not d_["escaped"] or d_["shift"] > 1e-3:
        P(f"    host z {key_[0]} lMb {key_[1]:.1f} mf {key_[2]:.2f} v_k {v_:.0f}: r_v {d_['rv']:.2f} r200; progenitors escaped {d_['escaped']}; "
          f"S(r_F) {d_['S'][0]:.4f}/{d_['S'][1]:.4f} -> |shift| {d_['shift']:.4f} dex" + (f" (in place self/intact {d_['self']:.3f}/{d_['intact']:.3f})" if "self" in d_ else ""))
ref_B = {v_: FLB[((2.5, 11.0, 1.0), v_)] for v_ in VKS}
hist_max = max(fl_kick_B.values())
P(f"    progenitor passage under the yield: escaped {sum(r_['escaped'] for r_ in rows_B)}/{len(rows_B)}; z' (z = 2.5 hosts) "
  f"{min(zp_B):.2f}-{max(zp_B):.2f}; v_esc(r_F) at passage <= {vmaxB:.0f} km/s; the flagship's worst |shift| per kick (FP10's convention): "
  + ", ".join(f"{v_:.0f}: {x_:.4f}" for v_, x_ in fl_kick_B.items()) + f" dex (worst cell z {worst_B[0][0][0]} lMb {worst_B[0][0][1]} mf {worst_B[0][0][2]:.2f} v_k {worst_B[0][1]:.0f})")
check("T4c (reported) THE FLAGSHIP UNDER THE YIELD ONSET on FP9's H_Y: the MOND scalar reaches r_F in the progenitors only at z' ~ 2.9-3.0 "
      "(FK1's own trigger: 3.7-6.9), so the in-place population leaves late, from deeper wells; FP10's convention on every host (z = 0.5-2.5, "
      "the gas range at 2.5): the flagship's worst |shift| per kick",
      f"escaped {sum(r_['escaped'] for r_ in rows_B)}/{len(rows_B)} (v_esc <= {vmaxB:.0f} km/s); worst |shift| " + ", ".join(f"{v_:.0f}: {x_:.3f}" for v_, x_ in fl_kick_B.items())
      + f" dex (gate {FLAG_TOL}); 1e11 in place self/intact {max(ref_B[v_]['self'] for v_ in VKS):.3f}/{max(ref_B[v_]['intact'] for v_ in VKS):.3f} dex",
      True, "a cell whose progenitor does not escape is scored in place (FP10's pessimistic max of self and intact): the late passage "
            "on H_Y puts the heaviest hosts' v_esc(r_F) next to the slow end of the kick window", load_bearing=False)
OUT["numbers"]["T4c"] = dict(zeta=ZETA_B, window=dict(lo=ZB_LO, cone=ZB_LO / 0.21, seeded=ZB_LO * math.sqrt(EN), cap=ZB_CAP, W2=ZB_W2),
                             escaped=esc_B, vmax=vmaxB, z_pass=[min(zp_B), max(zp_B)], worst_per_kick=fl_kick_B,
                             flag={f"{k_[0][0]}|{k_[0][1]}|{k_[0][2]}|{k_[1]:.0f}": d_ for k_, d_ in FLB.items()})
P(f"    {elapsed()}")

banner("T4d THE YIELD ONSET'S BUDGET: the forest (XR12's proxy with the yield cut), S_8, mass-selectivity")
T4D = {}
for tag, zeq_, cut_ in ((f"zeta {ZB_LO:.0f} (window floor), floor m", ZB_LO, ("fdm", 1.9e-19)), (f"zeta {ZETA_B:.0f} (centre), floor m", ZETA_B, ("fdm", 1.9e-19)),
                        (f"zeta {ZB_CAP['canonical']:.0f} (cap), floor m", ZB_CAP["canonical"], ("fdm", 1.9e-19)),
                        (f"zeta {ZETA_B:.0f} (centre), m = 1e-15 eV", ZETA_B, ("fdm", 1e-15))):
    if SMOKE and "cap" in tag:
        continue
    r_ = forest_eval(zeq_, 0.0, cut_, ycut=("canonical", "H_Y"))
    s8_ = S8r(r_["S"], 600.0)
    T4D[tag] = dict(forest=r_["worst"], cal=r_["cal"], Fb=r_["Fb"], S8=s8_)
    P(f"    {tag:36s}: forest z = 2/3 {r_['cal']['2.0']:.4f}/{r_['cal']['3.0']:.4f}; F_b(4/3/2/1/0) {r_['Fb'][4.0]:.3f}/{r_['Fb'][3.0]:.3f}/"
      f"{r_['Fb'][2.0]:.3f}/{r_['Fb'][1.0]:.3f}/{r_['Fb'][0.0]:.3f}; S_8 ratio {s8_:.4f}   {elapsed()}")
bY = budget_Y(600.0, K_MID, ZETA_B, 0.0, "canonical")
b_fk1 = F["budget"](600.0, K_MID)
izg = {float(z_): i for i, z_ in enumerate(F["ZG"])}
selY = {z_: float(bY["hi"][izg[z_]]) for z_ in (2.0, 3.0, 4.0)}
sel_fk1 = {z_: float(b_fk1["hi"][izg[z_]]) for z_ in (2.0, 3.0, 4.0)}
FzY = {z_: float(np.interp(z_, F["ZG"], bY["F"])) for z_ in (4.0, 3.0, 2.0, 1.0, 0.5, 0.0)}
s8Y = S8r(bY["S"], 600.0)
P(f"    FP10's derived-front budget with the yield cut (zeta {ZETA_B:.0f}, q = 0): F(4/3/2/1/0.5/0) " + "/".join(f"{v_:.3f}" for v_ in FzY.values())
  + f"; share in hosts >= 1e10.5 at z = 2/3/4 {selY[2.0]:.2f}/{selY[3.0]:.2f}/{selY[4.0]:.2f} (FK1: {sel_fk1[2.0]:.2f}/{sel_fk1[3.0]:.2f}/"
    f"{sel_fk1[4.0]:.2f}); S_8 ratio {s8Y:.4f}")
fo_ok = all(v_["forest"] <= 0.10 for k_, v_ in T4D.items() if "floor m" in k_)
check("T4d (reported) THE YIELD ONSET'S BUDGET: the MOND scalar's own frozen IGM keeps the forest-epoch conversion inside galaxies' "
      "yield surfaces -- the conversion becomes mass-selective (XR16's objection answered) and the forest passes across the zeta window "
      "at the floor mass; S_8 stays above the strict ratio",
      {k_: dict(forest=round(v_["forest"], 4), S8=round(v_["S8"], 4)) for k_, v_ in T4D.items()} | dict(selectivity=selY, S8_FP10_budget=round(s8Y, 4)),
      True, "the window's lower end is the z = 2 web (FP9's dense lumps switch on); with XR12's cone estimate it narrows to "
            f"[{ZB_LO / 0.21:.0f}, {ZB_CAP['canonical']:.0f}] and with the seeded criterion it closes", load_bearing=False)
OUT["numbers"]["T4d"] = dict(forest=T4D, selectivity=selY, selectivity_fk1=sel_fk1, F=FzY, S8_budget=s8Y)

banner("T4e THE YIELD ONSET UNDER FP13's STATE SEPARATOR (H_S): the gate reads the MOND scalar, so it inherits the committed separator")
P("    H_S: y_th = the web's band-passed NL leaf-rms x max(0, 2q) (zero once the leaf accelerates, z < %.3f); L(z) the web's collapse scale" % Z_Q0)
P("      y_th: " + ", ".join(f"z {z_:g}: {y_th13(z_):.2e}" for z_ in (0.0, 0.5, Z_Q0, 1.0, 2.0, 2.5, 3.0, 4.0, 6.0)) + " (FP9's H_Y: "
  + ", ".join(f"{y_th(z_):.1e}" for z_ in (2.0, 2.5, 3.0, 4.0)) + " at z = 2/2.5/3/4)")
P("      L: " + ", ".join(f"z {z_:g}: {L13_kpc(z_):.0f} kpc" for z_ in (0.0, 0.25, 1.0, 2.0, 2.5, 3.0, 4.0)))
ZS_LO = {"web on below the q = 0 epoch only": 11.0 / float(Rtm(Z_Q0, 1.0, 0.0)), "web on up to z = 2 (FP13 H4: its z >= 2 lumps are off)": ZB_LO}
ZETA_S = ZETA_B
rows_S = passages(ZETA_S, 0.0, alphas=(0.6, 1.0) if SMOKE else (0.6, 0.8, 1.0), yieldgate=True, sep="H_S")
zp_S = [r_["z_pass"] for r_ in rows_S if r_["host"][0] == 2.5]
esc_S = sum(r_["escaped"] for r_ in rows_S)
vmaxS = max(r_["v_esc"] for r_ in rows_S)
FLS = yield_flag(ZETA_S, "H_S", rows_S, 3000 if SMOKE else 10000)
fl_kick_S, worst_S = yield_flag_summary(FLS)
T4E = {}
for tag, zb in ((f"zeta {ZS_LO['web on below the q = 0 epoch only']:.0f} (window floor, web on below z = 0.635 only)", ZS_LO["web on below the q = 0 epoch only"]),
                (f"zeta {ZETA_S:.0f} (centre)", ZETA_S), (f"zeta {ZB_CAP['canonical']:.0f} (cap)", ZB_CAP["canonical"])):
    if SMOKE and "cap" in tag:
        continue
    r_ = forest_eval(zb, 0.0, ("fdm", 1.9e-19), ycut=("canonical", "H_S"))
    T4E[tag] = dict(forest=r_["worst"], cal=r_["cal"], Fb=r_["Fb"], S8=S8r(r_["S"], 600.0))
    P(f"    {tag:58s}: forest z = 2/3 {r_['cal']['2.0']:.4f}/{r_['cal']['3.0']:.4f}; F_b(4/3/2/1/0) {r_['Fb'][4.0]:.3f}/{r_['Fb'][3.0]:.3f}/"
      f"{r_['Fb'][2.0]:.3f}/{r_['Fb'][1.0]:.3f}/{r_['Fb'][0.0]:.3f}; S_8 ratio {T4E[tag]['S8']:.4f}   {elapsed()}")
bS = budget_Y(600.0, K_MID, ZETA_S, 0.0, "canonical", sep="H_S")
selS = {z_: float(bS["hi"][izg[z_]]) for z_ in (2.0, 3.0, 4.0)}
s8S = S8r(bS["S"], 600.0)
for (key_, v_), d_ in FLS.items():
    if key_[0] == 2.5 or not d_["escaped"] or d_["shift"] > 1e-3:
        P(f"    host z {key_[0]} lMb {key_[1]:.1f} mf {key_[2]:.2f} v_k {v_:.0f}: r_v {d_['rv']:.2f} r200; progenitors escaped {d_['escaped']}; "
          f"S(r_F) {d_['S'][0]:.4f}/{d_['S'][1]:.4f} -> |shift| {d_['shift']:.4f} dex" + (f" (in place self/intact {d_['self']:.3f}/{d_['intact']:.3f})" if "self" in d_ else ""))
P("    the flagship's worst |shift| per kick (FP10's convention, every host): " + ", ".join(f"{v_:.0f}: {x_:.4f}" for v_, x_ in fl_kick_S.items()) + " dex")
P(f"    passage under H_S: escaped {esc_S}/{len(rows_S)}; z' (z = 2.5 hosts) {min(zp_S):.2f}-{max(zp_S):.2f}; v_esc <= {vmaxS:.0f} km/s; FP10 budget "
  f"with the H_S cut: share >= 1e10.5 at z = 2/3/4 {selS[2.0]:.2f}/{selS[3.0]:.2f}/{selS[4.0]:.2f}; S_8 {s8S:.4f}")
check("T4e (reported) THE YIELD ONSET UNDER H_S: the gate inherits FP13's separator -- the web is MOND-on below z = 0.635 (the yield "
      "vanishes), so the density normalisation alone must hold the late web (zeta >= ~8-32), and the flatter state yield (~1e-2 at "
      "z >= 1) lets the progenitors convert earlier; the q-running stays unnecessary",
      dict(window_floor={k_: round(v_, 1) for k_, v_ in ZS_LO.items()}, escaped=f"{esc_S}/{len(rows_S)}", z_pass=[round(min(zp_S), 2), round(max(zp_S), 2)],
           flag_worst_per_kick={f"{v_:.0f}": round(x_, 4) for v_, x_ in fl_kick_S.items()}, forest={k_: round(v_["forest"], 4) for k_, v_ in T4E.items()}, S8=round(s8S, 4), selectivity=selS),
      True, "the yield onset's verdict holds on either committed separator; on H_S the yield vanishes below z = 0.635, so a gate whose "
            "width is the yield would become a step there (a singular reciprocal source): its width must be tied to the web's rms instead "
            "-- another postulated form; the prices (the gate's form, the reciprocal flux, zeta) remain", load_bearing=False)
OUT["numbers"]["T4e"] = dict(y_th={str(z_): y_th13(z_) for z_ in (0.0, 0.5, 1.0, 2.0, 2.5, 3.0, 4.0)}, window_floor=ZS_LO, zeta=ZETA_S,
                             escaped=esc_S, n=len(rows_S), z_pass=[min(zp_S), max(zp_S)], vmax=vmaxS,
                             flag={f"{k_[0][0]}|{k_[0][1]}|{k_[0][2]}|{k_[1]:.0f}": d_ for k_, d_ in FLS.items()}, worst_per_kick=fl_kick_S,
                             forest=T4E, selectivity=selS, S8_budget=s8S)

banner("T6  FP13's STATE QUANTITIES AS THE DARK TRIGGER (the coordinator's test): the q-sign onset and the collapse threshold")
# (a) the q-sign ramp alone: a function of Omega_L(<K>_h) and Omega_r only -- global; its onset is z = 0.635
flag_S1 = {}
for key_, H_ in HOSTS.items():
    if key_[0] >= 1.0:
        flag_S1[key_] = flag_shift_max(H_, (1.0, 1.0))                 # accelerating sign: no conversion before z = 0.635
sh_acc = min(flag_S1.values())
R1100 = R_rad(1100.0, ZB_CAP["canonical"] * E25 ** (-3.5), 0.0)       # decelerating sign, no nonlinearity factor, q = 0, the largest zeta that still clears r_F
P(f"    (a) accelerating sign (convert once the leaf accelerates, z < {Z_Q0:.3f}): the flagship at z = 1-2.5 keeps its whole carrier: "
  f"|shift| {sh_acc:.2f}-{max(flag_S1.values()):.2f} dex (gate 0.074); the web converts below z = {Z_Q0:.3f} wherever the density allows (the runaway)")
P(f"    (a) decelerating sign (convert while it decelerates, z > {Z_Q0:.3f}): with FK1's density criterion at q = 0 and the largest zeta that "
  f"still clears the flagship ({ZB_CAP['canonical']:.0f}), the background is above the trigger at recombination (R(1100) = {R1100:.1e}): the "
  f"CMB's cold carrier converts unless a second factor holds it")
# (b) the local nonlinearity factor at the same delta_c: a region converts where its L-smoothed contrast exceeds 1.686
dc = 1.686
R_nl = 1 + dc
fil = {z_: dict(L=L13_kpc(z_), width=[1e3 * w_ / (0.6736 * (1 + z_)) for w_ in (2.0, 4.0)]) for z_ in (0.0, 0.5, 1.0, 2.0, 2.5, 3.0)}
fil_ok = all(v_["width"][0] >= 0.7 * v_["L"] for v_ in fil.values())
need_ratio = {an: 24.77 * zq / R_nl for an, zq in (("W2 canonical", ZW2["canonical"][0]), ("W2 alt", ZW2["alt"][1]))}
P(f"    (b) the nonlinearity factor: threshold 1 + delta_c = {R_nl:.3f} x the mean on the L-smoothed field; the web's filaments (delta ~ 10, "
  f"diameters 2-4 Mpc/h comoving, Cautun+14) are wider than FP13's L(z) at every z -- " +
  ", ".join(f"z {z_:g}: {v_['width'][0]:.0f}-{v_['width'][1]:.0f} vs L {v_['L']:.0f} kpc" for z_, v_ in fil.items()) +
  f" -- so their smoothed contrast ~10 exceeds 1.686: filaments and walls convert in every allowed epoch; the gates need the trigger at "
  f"R(2.5) = {24.77 * ZW2['canonical'][0]:.0f}-{24.77 * ZW2['alt'][1]:.0f} (W2), {min(need_ratio.values()):.0f}-{max(need_ratio.values()):.0f}x above 1 + delta_c")
# (c) the spherical-collapse partner of delta_c: Delta = 18 pi^2 relative to the leaf-averaged matter density (R = 177.7 at every z)
DV = 18 * math.pi ** 2
zeq_vir = DV / float(Rtm(2.5, 1.0, FK1_Q))
cap_vir = {f_: DV * X["Om_z"](2.5) / J["XR12"]["W"]["zeta_F"][f"1e12/{f_}"]["rho_bar_enclosed"] for f_ in FEET}   # S_cap = rho_t/rho_bar(<r_F), XR12 W
_rt_orig = F["rho_t"]
F["rho_t"] = lambda z, ft=1.0, qg=1.75: DV * Om * F["RHOC0_KPC"] * (1 + z) ** 3      # the virial trigger (FP10's units)
try:
    rows_V = passages(-DV, -1.0, alphas=(0.6, 1.0) if SMOKE else (0.6, 0.8, 1.0), kicks=(575.0,))
    fr_V = min(scoring_front(H_, -DV, -1.0, 600.0, K_LO) / H_["rF"]["canonical"] for k_, H_ in HOSTS.items() if k_[0] == 2.5)
    bV = F["budget"](600.0, K_MID, ft=-DV, qg=-1.0)
finally:
    F["rho_t"] = _rt_orig
s8V = S8r(bV["S"], 600.0)
selV = {z_: float(bV["hi"][izg[z_]]) for z_ in (2.0, 3.0, 4.0)}
fV = forest_eval(1.0, 0.0, CUT_FLOOR, custom="virial 18 pi^2")
escV = sum(r_["escaped"] for r_ in rows_V)
P(f"    (c) Delta = 18 pi^2 = {DV:.1f} (the spherical-collapse partner of delta_c = 1.686): R = {DV:.0f} at every z -- the background and the web are "
  f"far below it; at z = 2.5 it is zeta_eq = {zeq_vir:.2f}: XR12-W2 allows <= {ZW2['canonical'][1]:.2f}/{ZW2['alt'][1]:.2f}; the own-density cap "
  f"leaves S(r_F) = {cap_vir['canonical']:.3f}/{cap_vir['alt']:.3f} (gate 0.059) -> FAILS on the resolved reading; on FP10's no-cap reading the "
  f"scoring front reaches {fr_V:.2f} r_F and the progenitors escape {escV}/{len(rows_V)}; forest {fV['worst']:.4f} (z = 2/3 {fV['cal']['2.0']:.4f}/"
  f"{fV['cal']['3.0']:.4f}); S_8 {s8V:.4f}; share >= 1e10.5 at z = 2/3/4 {selV[2.0]:.2f}/{selV[3.0]:.2f}/{selV[4.0]:.2f}")
t6_ok = sh_acc > FLAG_TOL and R1100 < 1.0 and fil_ok and min(need_ratio.values()) > 10.0 and min(cap_vir.values()) > 0.059
check("T6 A STATE-KEYED DARK TRIGGER WITH NO NEW CONSTANT FAILS: (a) the q-sign onset is global -- keyed to it the conversion either "
      "starts only at z < 0.635 (the flagship at z = 1-2.5 keeps its carrier, and the late web converts: the runaway) or runs at every "
      "z > 0.635 (the background converts before recombination unless a second factor holds it); (b) the local nonlinearity factor at "
      "FP13's delta_c converts the web itself (filaments, delta ~ 10, are wider than L(z) and far above 1 + delta_c at every z), while "
      "the gates need the trigger >= 20x higher; (c) its spherical-collapse partner Delta = 18 pi^2 spares the web and the background "
      "but fails the flagship's own-density cap (XR12-W2) on both footings, and its constant threshold converts z >= 4 halos earlier "
      "than FK1's running (the forest; reported: on FP10's no-cap reading the flagship itself passes)",
      f"(a) flagship |shift| >= {sh_acc:.2f} dex; R(1100) = {R1100:.1e}; (b) filaments wider than L at all z: {fil_ok}; needed/(1 + delta_c) = "
      f"{min(need_ratio.values()):.0f}-{max(need_ratio.values()):.0f}x; (c) zeta_eq {zeq_vir:.2f} vs W2 <= {ZW2['alt'][1]:.2f}; S_cap {cap_vir['canonical']:.3f}/"
      f"{cap_vir['alt']:.3f}; FP10 no-cap: front {fr_V:.2f} r_F, escaped {escV}/{len(rows_V)}, forest {fV['worst']:.3f}, S_8 {s8V:.3f}", t6_ok,
      "the state supplies the onset (when) and the collapse scale (where MOND's web is), not the HEIGHT of the dark threshold: sparing "
      "filaments while clearing z = 2.5 galaxies needs a trigger ~20-60x above the web's own nonlinearity -- zeta, or a virial partner the "
      "own-density cap and the forest exclude")
OUT["numbers"]["T6"] = dict(acc_flag=flag_S1 and {f"{k_[0]}|{k_[1]}|{k_[2]}": v_ for k_, v_ in flag_S1.items()}, R1100=R1100,
                            filaments={str(k_): v_ for k_, v_ in fil.items()}, need_ratio=need_ratio,
                            virial=dict(Delta=DV, zeta_eq=zeq_vir, S_cap=cap_vir, front_over_rF=fr_V, escaped=escV, n=len(rows_V),
                                        forest=fV["worst"], forest_cal=fV["cal"], S8=s8V, selectivity=selV))
P(f"    {elapsed()}")

banner("T6d THE THRESHOLD delta_t0 ITSELF (XR19: the dominant lever) AGAINST SPHERICAL COLLAPSE'S NATURAL NUMBERS")
# XR12/XR19's delta_t0 = 5.31 zeta is the trigger's height over the mean at z = 0 with FK1's running (q = 7/4).  The gates' band
# at the dark-mass floor (M1/T3b) is zeta_eq in [zeta_forest, zeta_W2]; in delta_t0 units:
DT0 = float(X["DT0_LIN"])
_edge74 = EDGE[1.75]["edge"] if EDGE[1.75]["edge"] else float("nan")          # T3b's forest edge at q = 7/4 (the floor, or MUTATE's cut)
BAND_DT0 = {f_: (DT0 * _edge74, DT0 * ZW2[f_][1]) for f_ in FEET}
REACH_DT0 = (DT0 * REACH[(K_LO, "canonical")], DT0 * REACH[(K_HI, "canonical")])
SC = {"1 + delta_c (the collapse threshold, FP13's s)": 1 + 1.686, "9 pi^2/16 (turnaround, EdS)": 9 * math.pi ** 2 / 16,
      "18 pi^2 (virialised, EdS)": 18 * math.pi ** 2}
T6D = {}
for nm, dt0 in SC.items():
    zt = dt0 / DT0
    fe_ = forest_eval(zt, FK1_Q, CUT_FLOOR)
    w_ = web(zt, FK1_Q, EN)
    T6D[nm] = dict(delta_t0=dt0, zeta=zt, forest=fe_["worst"], R_min=w_["R_min"], filaments=w_["filaments"], mean_seeded=w_["mean_seeded"],
                   in_band={f_: BAND_DT0[f_][0] <= dt0 <= BAND_DT0[f_][1] for f_ in FEET}, in_reach=dt0 <= REACH_DT0[1])
    P(f"    {nm:48s}: delta_t0 {dt0:7.2f} (zeta {zt:.3f}): forest {fe_['worst']:.3f} at the floor; web R_min {w_['R_min']:.2f} (filaments "
      f"convert z <= {w_['filaments']}); in the band: canonical {T6D[nm]['in_band']['canonical']}, alt {T6D[nm]['in_band']['alt']}   {elapsed()}")
P(f"    the band the gates leave at the floor mass (q = 7/4): delta_t0 in [{BAND_DT0['canonical'][0]:.1f}, {BAND_DT0['canonical'][1]:.1f}] "
  f"(canonical), [{BAND_DT0['alt'][0]:.1f}, {BAND_DT0['alt'][1]:.1f}] (alt); FP10's no-cap reach allows up to {REACH_DT0[0]:.0f}-{REACH_DT0[1]:.0f}")
t6d_ok = not any(v_["in_band"]["canonical"] or v_["in_band"]["alt"] for v_ in T6D.values())
check("T6d (reported) THE THRESHOLD CANNOT BE SHARED WITH SPHERICAL COLLAPSE'S NATURAL NUMBERS (GR, EdS): the gates want delta_t0 inside "
      "the printed band at the floor mass with FK1's running; the collapse threshold 1 + delta_c = 2.7 and the turnaround contrast "
      "9 pi^2/16 = 5.55 sit below it (the forest fails and the web's filaments convert), the virial 18 pi^2 = 178 above it (the "
      "flagship's own-density cap fails; FP10's no-cap reach at the upper K allows it)",
      {nm: dict(delta_t0=round(v_["delta_t0"], 2), forest=round(v_["forest"], 3), R_min=round(v_["R_min"], 2), in_band=v_["in_band"]) for nm, v_ in T6D.items()}
      | dict(band=BAND_DT0), t6d_ok,
      "the band sits between turnaround and virialisation; the virial 18 pi^2 (with FK1's running) passes the forest and the web and lies "
      "inside FP10's no-cap reach for K >= 185 -- the own-density cap alone excludes it, so the resolved run that settles the cap settles "
      "it too; the chain's OWN spherical collapse (MOND on the web; XR23, pending) could move all three numbers; the running q stays "
      "needed (a mean-tracking threshold converts z >= 4 halos too early: T6c)", load_bearing=False)
OUT["numbers"]["T6d"] = dict(band_delta_t0=BAND_DT0, reach_delta_t0=REACH_DT0, candidates=T6D)

banner("T5  THE GATE TABLE RE-SCORED: FK1's own trigger, the shared-exponent cell, and the yield-onset cell (both footings)")
GT = {}
# FK1 (q = 7/4) -- FP10's committed rows + this lane's forest at the floor + the web
fk1_forest = forest_eval(TOPS["canonical"], FK1_Q, CUT_FLOOR)["worst"]
GT["FK1 q=7/4 (zeta_eq 2.76)"] = dict(
    flagship=f"history pass ({J10['B1']['history|575']:.4f} dex)", z0_galaxies="pass (FP10 B2: <= 0.0003 dex)",
    xcop="in place FAIL / optimistic pass (FP10 B3)", kids="pass (FP10 B4)", harvey="650 in place pass; 575 opt pass; 650 opt FAIL (FP10 B5)",
    S8=f"{J10['B6']['rows']['575|36|fluid']['ratio']:.3f}-{J10['B6']['rows']['650|947|fluid']['ratio']:.3f}", shear="in place FAIL / optimistic pass (FP10 B8)",
    forest=f"{fk1_forest:.3f} at the floor ({'pass' if fk1_forest <= 0.10 else 'FAIL'})",
    web=f"R_min {T3['FK1 q = 7/4']['W2 canonical (+ upstream)']['R_min']:.1f} (filaments sub-threshold; seeded mean z <= {T3['FK1 q = 7/4']['W2 canonical (+ upstream)']['mean_seeded']})")
k_sh = list(Q_SH.keys())[0]
sh = T3C[k_sh]
sh_forest = QW.get(Q_SH[k_sh], {}).get("canonical", {}).get("forest", float("nan"))
GT[f"shared q={Q_SH[k_sh]:.2f}"] = dict(
    flagship=f"history pass (passage escaped {QW.get(Q_SH[k_sh], {}).get('passage', {}).get('escaped', 'n/a')}/{QW.get(Q_SH[k_sh], {}).get('passage', {}).get('n', 'n/a')})",
    z0_galaxies="pass (fronts at r200, FP10 B2)", xcop=f"in place FAIL / optimistic {sh['xcop_opt']['575'][0]:.2f} FAIL", kids="pass (FP10 B4)",
    harvey=f"optimistic uniform factor {sh['harvey_us']:.2f}: 650 FAIL, 575 not established", S8=f"halo {sh['S8_halo']:.3f}; web {', '.join(f'{v_:.3f}' for v_ in sh['S8_web'].values())}",
    shear="in place FAIL / optimistic pass", forest=f"halo model {sh_forest:.3f}; filaments cross at z <= {T3[k_sh]['W2 canonical (+ upstream)']['filaments']}",
    web=f"FAIL: mean converts at z <= {T3[k_sh]['W2 canonical (+ upstream)']['mean_spont']} (A4)")
# the yield-onset cell on the committed separator (FP13's H_S): galaxies, X-COP, KiDS, shear, Harvey, S_8, forest; the z <= 0.5
# gates sit where H_S's yield is zero (MOND on), so only F_b, S_8, the forest and the flagship carry the separator
TB = {}
if not MUTATE:
    set_trigger(ZETA_S, 0.0)
    gal = {}
    for v_ in VKS:
        out_ = {}
        for kh, hst in F["GAL"].items():
            c_ = float(F["c200_z0"](hst["M200"]))
            Pp = F["prof_bary"](hst["M200"], c_, 0.0, F["hernquist"](hst["Mb"], hst["a"]), rhoc=F["RHO_C0"])
            r_, S_ = DB(Pp, v_)
            rv = F["front"](r_, S_, 1.0 / K_HI)
            out_[kh] = float(F["retained_fk1"](F["hernquist"](hst["Mb"], hst["a"]), hst["M200"], c_, [hst["rg"]], rv, v_, F["RHO_C0"],
                                               N=3000 if SMOKE else 10000)[0][0])
        gal[v_] = out_
    gsh = {v_: F["gal_shifts"](gal[v_]) for v_ in VKS}
    TB["galaxies"] = max(abs(x_) for v_ in VKS for f_ in FEET for x_ in gsh[v_][f_].values())
    Ppc = F["prof_bary"](F["CLREF"]["M200"], F["CLREF"]["c"], F["CLREF"]["z"], F["cl_mass_fn"], rhoc=F["CLREF"]["rhoc"])
    xc = {}
    for v_ in VKS:
        r_, S_ = DB(Ppc, v_)
        rv = F["front"](r_, S_, 1.0 / K_HI)
        e_s = float(F["retained_fk1"](F["cl_mass_fn"], F["CLREF"]["M200"], F["CLREF"]["c"], [F["CLREF"]["R500"]], rv, v_, F["CLREF"]["rhoc"],
                                      N=3000 if SMOKE else 12000)[0][0])
        Fcl = float(np.interp(F["CLREF"]["z"], F["ZG"], bS["Fb"]))
        xc[v_] = dict(front=rv / Ppc["r200"], eps=e_s, inplace=F["xcop_from_eps"](e_s), optimistic=F["xcop_from_eps"](max(e_s - Fcl, 0.0)), Fcl=Fcl)
    TB["xcop"] = {f"{v_:.0f}": dict(front=x_["front"], eps=x_["eps"], inplace=(x_["inplace"]["canonical"]["ratio"], x_["inplace"]["alt"]["ratio"]),
                                    optimistic=(x_["optimistic"]["canonical"]["ratio"], x_["optimistic"]["alt"]["ratio"]), Fcl=x_["Fcl"]) for v_, x_ in xc.items()}
    kd = {}
    for v_ in VKS:
        profs = []
        for b in range(4):
            M200 = F["M200_KIDS"][b]; c_ = float(F["c200_55"](M200))
            Mn, r200, rs = F["nfw21"](M200, c_, F["RHOC_ZL"])
            pro = np.geomspace(0.02 * rs, 0.999 * r200, 40)
            Mb_fn = F["hernquist"](1.3 * 10 ** F["LOGMS"][b], 3.0)
            Pp = F["prof_bary"](M200, c_, F["ZL"], Mb_fn, rhoc=F["RHOC_ZL"])
            r_, S_ = DB(Pp, v_)
            rv = F["front"](r_, S_, 1.0 / K_HI)
            ratio_p, _ = F["retained_fk1"](Mb_fn, M200, c_, list(pro), rv, v_, F["RHOC_ZL"], N=2000 if SMOKE else 8000)
            profs.append((pro, np.asarray(ratio_p)))
        FcL = float(np.interp(F["ZL"], F["ZG"], bS["Fb"]))
        kd[v_] = dict(inplace=F["kids_switched"](profs), optimistic=F["kids_switched"]([(p_, np.maximum(q__ - FcL, 0.0)) for p_, q__ in profs]))
    TB["kids"] = {f"{v_:.0f}": d_ for v_, d_ in kd.items()}
    DB.__defaults__ = DB_DEF
    Mh_ = F["MH"] / F["hh"]; ZSH = 0.5
    cs5 = np.clip(F["c_dm14"](F["MH"], ZSH), F["CG"][0], F["CG"][-1])
    r2005 = (3 * Mh_ / (4 * np.pi * 200 * F["RHOC0_KPC"] * Ez2(ZSH))) ** (1 / 3); V2005 = np.sqrt(F["GK"] * Mh_ / r2005)
    lgM = np.log10(Mh_)
    shv = {}
    for v_ in VKS:
        u5 = np.clip(v_ / V2005, 0, F["UGR"][-1])
        Tf, _ = F["tables"](ZSH, K_HI, ZETA_S, 0.0)
        xs5 = np.clip(Tf(np.stack([np.log(np.clip(cs5, F["CGRID"][0], F["CGRID"][-1])), np.minimum(u5, F["UGRID"][-1])], 1)), F["XVG"][0], 1.0)
        keep = 1 - np.clip(F["I_LC"](np.stack([np.log(cs5), np.log(xs5)], 1)) * F["I_ES"](np.stack([np.log(cs5), np.log(xs5), u5], 1)), 0, 1)
        Fc5 = float(np.interp(ZSH, F["ZG"], bS["Fb"]))
        rets = {"in place": (lambda M, kp=keep: float(np.interp(math.log10(M), lgM, kp))),
                "optimistic": (lambda M, kp=keep, F_=Fc5: max(float(np.interp(math.log10(M), lgM, kp)) - F_, 0.0))}
        shv[v_] = {rdg: {f_: max(F["R_of"](F["XLIN"], F["A0_MS3"][f_], 1.75, "door", rf)[0].values()) for f_ in FEET} for rdg, rf in rets.items()}
    TB["shear"] = {f"{v_:.0f}": d_ for v_, d_ in shv.items()}
    usB = 1.0 - float(np.interp(0.4, F["ZG"], bS["Fb"]))
    TB["harvey_us"] = usB
    refS = {v_: FLS[((2.5, 11.0, 1.0), v_)] for v_ in VKS}
    GT[f"yield onset on H_S (zeta {ZETA_S:.0f}, q = 0)"] = dict(
        flagship="FP10's convention, every host: " + ", ".join(f"{v_:.0f} {'pass' if x_ <= FLAG_TOL else 'FAIL'} ({x_:.4f} dex)" for v_, x_ in fl_kick_S.items())
                 + f"; 1e11 in place self/intact {max(refS[v_]['self'] for v_ in VKS):.3f}/{max(refS[v_]['intact'] for v_ in VKS):.3f}",
        z0_galaxies=f"{TB['galaxies']:.4f} dex ({'pass' if TB['galaxies'] <= 0.06 else 'FAIL'})",
        xcop="; ".join(f"{v_}: in place {d_['inplace'][0]:.2f}/{d_['inplace'][1]:.2f}, optimistic {d_['optimistic'][0]:.2f}/{d_['optimistic'][1]:.2f}" for v_, d_ in TB["xcop"].items()),
        kids="; ".join(f"{v_}: {d_['inplace']['canonical']:+.1f}/{d_['inplace']['alt']:+.1f} (opt {d_['optimistic']['canonical']:+.1f}/{d_['optimistic']['alt']:+.1f})" for v_, d_ in TB["kids"].items()),
        harvey=f"optimistic uniform factor {usB:.2f} (650 fails at <= 0.499; 575 passes at >= 0.514)",
        S8=f"{s8S:.3f} (FP10 budget) / {[v_['S8'] for k_, v_ in T4E.items() if 'centre' in k_][0]:.3f} (XR12 history)",
        shear="; ".join(f"{v_}: in place {d_['in place']['canonical']:.2f}/{d_['in place']['alt']:.2f}, optimistic {d_['optimistic']['canonical']:.2f}/{d_['optimistic']['alt']:.2f}" for v_, d_ in TB["shear"].items()),
        forest=f"{[v_['forest'] for k_, v_ in T4E.items() if 'centre' in k_][0]:.4f}",
        web=f"filaments held below the trigger for zeta >= {ZS_LO['web on below the q = 0 epoch only']:.0f}-{ZB_LO:.0f} (the web is MOND-on below z = 0.635)")
for cell, d_ in GT.items():
    P(f"    {cell}:")
    for k_, v_ in d_.items():
        P(f"      {k_:12s} {v_}")
check("T5 (reported) the gate table re-scored for FK1's own trigger, the shared-exponent cell and the yield-onset cell",
      {c_: list(d_.keys()) for c_, d_ in GT.items()}, True, load_bearing=False)
OUT["numbers"]["T5"] = dict(table=GT, yield_cell=TB)
P(f"  part T done   {elapsed()}")

# ================================================================================================ PART E: eps
banner("E1  THE Z4 THEOREM: eps is the only term odd under Phi -> i Phi, so nothing else can make it (sympy)")
pH, pL, m_, e_, l_ = sp.symbols("phi_H phi_L m epsilon lambda", real=True)
V = m_ ** 2 * (pH ** 2 + pL ** 2) / 2 + e_ * (pH ** 2 - pL ** 2) / 2 + l_ * pH ** 2 * pL ** 2
Z4 = {pH: -pL, pL: pH}                                                # Phi -> i Phi
terms = {"|dPhi|^2 (kinetic, and every coupling to T_mn, the metric, L353's pair)": (pH ** 2 + pL ** 2),
         "m^2 |Phi|^2": m_ ** 2 * (pH ** 2 + pL ** 2) / 2, "lambda (Im Phi^2)^2": l_ * pH ** 2 * pL ** 2,
         "FK1's gate lambda(K) (Im Phi^2)^2 (K is a Z4 singlet)": sp.Function("lam")(sp.Symbol("K")) * pH ** 2 * pL ** 2,
         "eps Re(Phi^2)": e_ * (pH ** 2 - pL ** 2) / 2}
parity = {k_: sp.simplify(t_.subs(Z4, simultaneous=True) - t_) == 0 for k_, t_ in terms.items()}
odd = {k_: sp.simplify(t_.subs(Z4, simultaneous=True) + t_) == 0 for k_, t_ in terms.items()}
for k_ in terms:
    P(f"    {k_:72s}: Z4-even {parity[k_]}, Z4-odd {odd[k_]}")
Lu, Ms = sp.symbols("Lambda_UV M2", positive=True)
Iq = (Lu ** 2 - Ms * sp.log(Lu ** 2 / Ms)) / (16 * sp.pi ** 2)       # the tadpole integral (cutoff)
split = sp.simplify(2 * l_ * (Iq.subs(Ms, m_ ** 2 - e_) - Iq.subs(Ms, m_ ** 2 + e_)))
split0 = sp.simplify(split.subs(e_, 0))
split_lin = sp.simplify(sp.series(split, e_, 0, 2).removeO())
P(f"    one loop: delta(m_H^2 - m_L^2) = 2 lambda [I(m_L^2) - I(m_H^2)] = {split_lin} + O(eps^2);  at eps = 0: {split0}")
rhoH, lp = sp.symbols("rho_H lambda_p", positive=True)
mL2 = sp.diff(V, pL, 2).subs(pL, 0)                                    # the light mass^2 in a phi_H background
shift_L = sp.expand(mL2.subs(pH ** 2, rhoH / m_ ** 2) - mL2.subs(pH, 0)).subs(l_, lp)   # time average <phi_H^2> = rho_H/m^2
P(f"    a phi_H condensate (the cold dark matter itself, <phi_H^2> = rho_H/m^2) shifts m_L^2 by {shift_L} > 0 (lambda > 0): it RAISES the light "
  f"mass -- the wrong sign; it cannot supply the heavy->light channel")
e1_ok = all(parity[k_] for k_ in terms if not k_.startswith("eps")) and odd["eps Re(Phi^2)"] and split0 == 0 and \
    sp.simplify(split_lin.diff(e_)) != 0 and sp.simplify(shift_L - 2 * lp * rhoH / m_ ** 2) == 0
check("E1 DERIVED: every term of the action but eps Re(Phi^2) is invariant under Z4: Phi -> i Phi (phi_H -> -phi_L, phi_L -> phi_H) -- the "
      "kinetic term and every coupling through T_mn (gravity, L353's pair), m^2|Phi|^2, the cross quartic and FK1's K-gate -- while eps "
      "Re(Phi^2) is odd; so eps = 0 is radiatively stable (the one-loop split is 2 lambda [I(m_L^2) - I(m_H^2)] ~ eps: multiplicative) "
      "and no coupling present can generate it; the condensate's own lambda-shift raises m_L (the wrong sign)",
      f"even {sum(parity.values())}/5, eps odd {odd['eps Re(Phi^2)']}; split at eps = 0: {split0}; linear: {split_lin}", e1_ok,
      "eps is a symmetry-breaking spurion: IRREDUCIBLE unless the action is given another Z4-odd term, whose coefficient would then "
      "be the fitted number (E2)")
OUT["numbers"]["E1"] = dict(parity={k_: bool(v_) for k_, v_ in parity.items()}, split=str(split_lin), condensate_shift=str(shift_L))

banner("E2  EVERY CANDIDATE MECHANISM FOR eps (the coordinator's list)")
tt, AH, AL, th = sp.symbols("t A_H A_L theta", real=True)
mp_ = sp.symbols("m", positive=True)                                  # the oscillation frequency is a mass: positive
phH_t = AH * sp.cos(mp_ * tt); phL_t = AL * sp.cos(mp_ * tt + th)
avg = lambda ex: sp.simplify(sp.integrate(sp.expand(sp.expand_trig(ex)), (tt, 0, 2 * sp.pi / mp_)) * mp_ / (2 * sp.pi))
reK = avg((sp.diff(phH_t, tt) ** 2 - sp.diff(phL_t, tt) ** 2) / 2)    # Re[(n.dPhi)^2], n = d_t on the clock's leaves
rePhi2 = avg((phH_t ** 2 - phL_t ** 2) / 2)
frame_ok = sp.simplify(reK - mp_ ** 2 * rePhi2) == 0
P(f"    (a) L353's pair and (b) the leaf average couple to T_mn / the metric / the khronon: Z4 singlets (E1) -> eps contribution 0")
P(f"    (c) the only lowest-order Z4-odd frame coupling c_K Re[(n.dPhi)^2]: its slow part = {reK} = m^2 x <Re Phi^2> ({frame_ok}) -> "
  f"eps_eff = -c_K m^2, eps/m^2 = |c_K|: the fitted 1.84-2.35e-6 moves into c_K (a relabelling, not a derivation)")
m_floor = 1.9e-19
scales = {"hbar H_0": HBAR_EVS * H0_SI, "hbar sqrt(Lambda) c (Lambda-mass)": HBAR_EVS * H0_SI * math.sqrt(3 * OM_L),
          "hbar a0/c (canonical)": HBAR_EVS * A0_FP0["canonical"] / c_SI, "rho_Lambda^(1/4) (dark-energy scale)": (OM_L * RHO_CRIT * c_SI ** 2 * (HBAR_EVS * 1.602176634e-19 * c_SI) ** 3 / 1.602176634e-19 ** 4) ** 0.25}
EPS_WIN = (1.8394e-6, 2.3505e-6)
E2N = {}
for k_, mu in scales.items():
    e_over = (mu / m_floor) ** 2
    m_need = mu / math.sqrt(EPS_WIN[0]) * 1.0
    E2N[k_] = dict(mu_eV=mu, eps_over_m2_at_floor=e_over, m_for_O1=m_need, coefficient_needed=EPS_WIN[0] / e_over)
    P(f"    (d) a Z4-odd coupling c mu^2 Re(Phi^2), mu = {k_:38s} {mu:.3e} eV: eps/m^2 = {e_over:.2e} c at the floor -> c = {EPS_WIN[0] / e_over:.1e}; "
      f"with c = 1 it needs m = {m_need:.2e} eV")
hub_ok = all(v_["eps_over_m2_at_floor"] < 1e-20 for k_, v_ in E2N.items() if "rho_Lambda" not in k_)
check("E2 DERIVED: no present coupling induces eps -- L353's pair and the leaf average are Z4 singlets (0); a frame coupling c_K Re[(n.dPhi)^2] "
      "gives eps/m^2 = |c_K| exactly (a relabelling); a vacuum/Hubble-scale splitting c mu^2 with mu = hbar H_0, the Lambda-mass or "
      "hbar a0/c gives eps/m^2 <= 1e-28 c at the floor mass (c ~ 1e22 needed, or m ~ 1e-30 eV, below the floor); the dark-energy scale "
      "rho_Lambda^(1/4) hits the window only through a tuned m (FP10 C3's class: a tie through m, not a mechanism)",
      f"frame relabelling {frame_ok}; Hubble-class eps/m^2 at the floor {max(v_['eps_over_m2_at_floor'] for k_, v_ in E2N.items() if 'rho_Lambda' not in k_):.1e}; "
      f"rho_Lambda^(1/4) needs m = {E2N['rho_Lambda^(1/4) (dark-energy scale)']['m_for_O1']:.2f} eV at c = 1", frame_ok and hub_ok,
      "eps stays FITTED: its value is set by the gates (E4), its existence by hand (E1)")
OUT["numbers"]["E2"] = dict(frame_relabelling=bool(frame_ok), scales=E2N)

banner("E3  (reported) THE m-FREE NUMEROLOGY CENSUS (FP10 C2 reproduced) -- NUMEROLOGY-FLAGGED, not a tie")
BASES = {"kappa": 0.5, "Z": ZED, "a0/(c H0) canonical": A0_FP0["canonical"] / (c_SI * H0_SI), "Omega_Lambda": OM_L}
HITS = []
for bn, bv in BASES.items():
    for k2 in range(-160, 161):
        if k2 == 0:
            continue
        v_ = bv ** (k2 / 2)
        if EPS_WIN[0] <= v_ <= EPS_WIN[1]:
            HITS.append((bn, k2 / 2, v_, c_SI / 1e3 * math.sqrt(2 * v_ / (1 + v_))))
lw = math.log(EPS_WIN[1] / EPS_WIN[0])
pchance = {bn: min(1.0, lw / abs(math.log(bv))) for bn, bv in BASES.items()}
p_any = 1 - np.prod([1 - p_ for p_ in pchance.values()])
for h_ in HITS:
    P(f"    {h_[0]}^{h_[1]:g} = {h_[2]:.4e} -> v_k = {h_[3]:.1f} km/s")
P(f"    chance that some integer power of each base lands in the window: " + ", ".join(f"{k_} {v_:.2f}" for k_, v_ in pchance.items())
  + f"; any of the four {p_any:.2f}")
check("E3 (reported) the only integer-power m-free 'tie' is eps/m^2 = kappa^19 (v_k = kappa^9 c = 585.5 km/s), with a 35% chance for "
      "kappa alone and 83% for any base: NUMEROLOGY-FLAGGED (nothing produces the exponent 19)",
      f"integer hits {[(h_[0], h_[1]) for h_ in HITS if float(h_[1]).is_integer()]}; P(chance) kappa {pchance['kappa']:.2f}, any {p_any:.2f}",
      any(h_[0] == "kappa" and h_[1] == 19.0 for h_ in HITS), load_bearing=False)
OUT["numbers"]["E3"] = dict(hits=HITS, p_chance=pchance, p_any=float(p_any))

banner("E4  (reported) eps IS FITTED BY DATA: the kick window's two ends are set by gates")
at1 = J["AT1"]["S1"]
lo_fail, lo_pass = at1["0.1|450.0"]["flag_max"], at1["0.1|600.0"]["flag_max"]
hv = J10["B5"]
P(f"    lower end (the flagship's daughters must escape): AT1 S1 at y_v = 0.1: 450 km/s leaves {lo_fail:.3f} dex (> 0.10), 600 km/s {lo_pass:.3f}; "
  f"FP10's history reading passes at 575")
P(f"    upper end (group cores must stay loaded): FP10 B5 Harvey optimistic: 575 {'pass' if hv['575|optimistic']['ok'] else 'FAIL'} "
  f"(fit {hv['575|optimistic']['beta']['fit']:+.3f}), 650 {'pass' if hv['650|optimistic']['ok'] else 'FAIL'} (fit {hv['650|optimistic']['beta']['fit']:+.3f}) against +0.10")
check("E4 (reported) eps/m^2 = v_k^2/(2c^2 - v_k^2) is FITTED BY DATA: the flagship sets the kick's lower end (450 km/s fails, 575-600 "
      "passes) and Harvey its upper end (650 fails in the optimistic reading); eps/m^2 = 1.84-2.35e-6 (+-12%)",
      f"450: {lo_fail:.3f} dex, 600: {lo_pass:.3f}; Harvey 650 optimistic {hv['650|optimistic']['beta']['fit']:+.3f}",
      lo_fail > 0.10 and lo_pass < 0.10 and not hv["650|optimistic"]["ok"], load_bearing=False)
OUT["numbers"]["E4"] = dict(lo_450=lo_fail, lo_600=lo_pass, harvey650=hv["650|optimistic"]["beta"]["fit"])
P(f"  part E done   {elapsed()}")

# ================================================================================================ PART M: m
banner("M1  THE DARK MASS ON XR12's RESOLVED READING: the forest's lower bound on zeta rises with m (the fluid's minihalos convert)")
M_LIST = (1.9e-19, 1e-18) if SMOKE else (1.9e-19, 5.2e-19, 1e-18, 1e-17)
ZG_M = (2.0, 2.5, 2.76, 3.5, 4.29, 6.0)
M1 = {}
for mv in M_LIST:
    cut_ = ("hard", 1e8) if MUTATE else ("fdm", mv)
    e_, vals = zeta_forest_edge(FK1_Q, cut_, ZG_M)
    M1[mv] = dict(edge=e_, scan=vals,
                  open={f"{f_}/{i_}": (e_ is not None and e_ <= ZW2[f_][i_]) for f_ in FEET for i_ in (0, 1)})
    P(f"    m = {mv:.1e} eV{' (MUTATE: hard M_min 1e8)' if MUTATE else ''}: forest needs zeta >= {e_ if e_ is None else round(e_, 3)} "
      f"(scan {[(z_, round(w_, 4)) for z_, w_ in vals]}); canonical band vs {ZW2['canonical']}: "
      f"{'OPEN' if M1[mv]['open']['canonical/1'] else 'CLOSED'} (width x{(ZW2['canonical'][1] / e_) if e_ else float('nan'):.2f}); alt vs {ZW2['alt']}: "
      f"{'OPEN' if M1[mv]['open']['alt/1'] else 'CLOSED'}   {elapsed()}")
e_floor = M1[M_LIST[0]]["edge"]
closes = [mv for mv in M_LIST if (M1[mv]["edge"] is None or M1[mv]["edge"] > ZW2["canonical"][0])]
m_max_can = None
ms_, es_ = [mv for mv in M_LIST if M1[mv]["edge"]], [M1[mv]["edge"] for mv in M_LIST if M1[mv]["edge"]]
for i_ in range(len(ms_) - 1):
    if es_[i_] <= ZW2["canonical"][1] < es_[i_ + 1]:
        t_ = (ZW2["canonical"][1] - es_[i_]) / (es_[i_ + 1] - es_[i_])
        m_max_can = float(math.exp(math.log(ms_[i_]) + t_ * (math.log(ms_[i_ + 1]) - math.log(ms_[i_]))))
width_floor = ZW2["canonical"][1] / e_floor if e_floor else float("inf")
_edges = [M1[mv]["edge"] for mv in M_LIST]
m1_ok = (e_floor is not None and width_floor <= 1.25 and len(closes) >= 1 and all(M1[mv]["open"]["alt/1"] for mv in M_LIST)
         and all(e_ is not None for e_ in _edges) and all(b_ >= a_ - 1e-3 for a_, b_ in zip(_edges, _edges[1:])))
check("M1 THE COMBINED GATES PIN (zeta, m) ON THE CANONICAL FOOTING (XR12's resolved reading): at the dark-mass floor (1.9e-19 eV, "
      "L383) the forest needs zeta >= ~2.4 against the flagship's <= 2.54-2.76 -- a band <= 1.25 wide -- and it narrows as m grows (the "
      "fluid's minihalos convert): the streams-C_s=10 bound closes it above the floor, the upstream bound leaves a sliver; the alt band "
      "stays open over the grid.  zeta is FITTED BY DATA, and m on the canonical C_s=10 bound; m is not free",
      f"zeta_f(m) = {({f'{mv:.1e}': (round(v_['edge'], 3) if v_['edge'] else None) for mv, v_ in M1.items()})}; canonical width at the floor "
      f"x{width_floor:.2f}; closes (C_s=10) at m in {[f'{mv:.1e}' for mv in closes]}; upstream-bound m_max ~ {m_max_can}", m1_ok,
      "on the canonical footing the dark sector's window is a sliver at the floor mass; the forest proxy's ~2x systematic (XR12 C2) "
      "is the band's largest uncertainty")
OUT["numbers"]["M1"] = dict(rows={f"{k_:.1e}": v_ for k_, v_ in M1.items()}, width_floor=width_floor, closes=closes, m_max_canonical=m_max_can)

banner("M2  (reported) FP10's DERIVED-FRONT READING (no own-density cap): the budget and S_8 against m, and the no-cap reach")
M2 = {}
_m22 = F["M22"]
for mv in M_LIST:
    F["M22"] = mv / 1e-22
    b_ = F["budget"](600.0, K_MID)
    M2[mv] = dict(F2=float(np.interp(2.0, F["ZG"], b_["F"])), F3=float(np.interp(3.0, F["ZG"], b_["F"])), S8=S8r(b_["S"], 600.0))
    P(f"    m = {mv:.1e} eV: F(2/3) {M2[mv]['F2']:.3f}/{M2[mv]['F3']:.3f}; S_8 ratio {M2[mv]['S8']:.4f}")
F["M22"] = _m22
P("    FP10's no-cap reach bounds zeta_eq by " + ", ".join(f"{v_:.0f}" for (K_, f_), v_ in REACH.items() if f_ == "canonical") +
  " (K = 36/185/947, canonical): with that upper bound the forest's lower one (~2.4) leaves a decade-wide window, m unpinned")
check("M2 (reported) on FP10's own reading (the stimulated front, no own-density cap) the budget and S_8 barely feel m and the flagship "
      "allows zeta_eq up to ~25-115: m and zeta are bounded, not pinned -- the pinning of M1 rests on the own-density cap XR12 resolved",
      {f"{k_:.1e}": dict(F2=round(v_["F2"], 3), S8=round(v_["S8"], 4)) for k_, v_ in M2.items()}, True, load_bearing=False)
OUT["numbers"]["M2"] = {f"{k_:.1e}": v_ for k_, v_ in M2.items()}

banner("M3  (reported) THE CEILING: Bose stimulation needs a highly occupied pump (FK1 N1's occupation ~ m^-4)")
N1 = J["FK1"]["N1"]["by_mass"]
Nf_2 = float(N1["2e-19"]["N_final"])
m_occ1 = 2e-19 * Nf_2 ** 0.25
m_occ3 = 2e-19 * (Nf_2 / 1e3) ** 0.25
P(f"    FK1 N1: occupation {Nf_2:.2e} at 2e-19 eV, ~ m^-4 (1e-6 eV: {float(N1['1e-06']['N_final']):.2e}); E_need " +
  ", ".join(f"{k_}: {float(v_['efolds']):.0f}" for k_, v_ in N1.items()))
P(f"    occupation 1 at m = {m_occ1:.2f} eV, 1e3 at m = {m_occ3:.2f} eV: the stimulated conversion needs m <~ 1 eV")
check("M3 (reported) CONSTRAINT: the Bose-stimulated conversion needs a highly occupied pump: occupation ~ m^-4 reaches 1e3 at ~0.6 eV "
      "and 1 at ~3.6 eV -- m <~ 1 eV; E_need falls only logarithmically (178 -> 61 e-folds from 2e-19 to 1e-6 eV)",
      f"m(occ 1e3) {m_occ3:.2f} eV, m(occ 1) {m_occ1:.2f} eV", 0.1 < m_occ3 < 10, load_bearing=False)
OUT["numbers"]["M3"] = dict(m_occ1=m_occ1, m_occ1e3=m_occ3)

banner("M4  (reported) L383's DWARF-HEATING FLOOR MOVES WITH THE CLEARING EPOCH (heating ~ m^-3 x exposure)")
L383 = J["L383"]["C"]


def t_Gyr(z):
    zz = np.geomspace(z, 1e4, 4000)
    return float(np.trapz(1.0 / ((1 + zz) * H0_SI * np.sqrt(Ez2(zz))), zz) / (3.15576e16))


tf = t_Gyr(8.0)
exp_L383 = t_Gyr(4.035) - tf
cases = {"FK1 (virial halos above threshold to z ~ 6: XR12 A1)": 6.0, "the yield onset (UFD baryons on the yield at z ~ 2)": 2.0}
M4 = {}
for k_, zc in cases.items():
    ex = t_Gyr(zc) - tf
    fl = [L383[f"sigma_dm={s_}"]["framework|1000"] * (ex / exp_L383) ** (1 / 3) for s_ in (5, 7, 10)]
    M4[k_] = dict(z_clear=zc, exposure=ex, floors=fl)
    P(f"    {k_}: cleared at z ~ {zc}: exposure {ex:.2f} Gyr (L383's {exp_L383:.2f}) -> floor {min(fl):.2e}-{max(fl):.2e} eV (L383 {L383['sigma_dm=10']['framework|1000']:.2e}-{L383['sigma_dm=5']['framework|1000']:.2e})")
check("M4 (reported) the dwarf-heating floor scales as exposure^(1/3): the trigger's own clearing epoch moves it (earlier clearing, lower floor)",
      {k_: [f"{x_:.2e}" for x_ in v_["floors"]] for k_, v_ in M4.items()}, True, load_bearing=False)
OUT["numbers"]["M4"] = M4

banner("M5  (reported) THE m-NUMEROLOGY CENSUS: dimensional combinations of the Planck mass and the framework's scales")
m_H = HBAR_EVS * H0_SI
m_a0 = HBAR_EVS * A0_FP0["canonical"] / c_SI
m_DE = scales["rho_Lambda^(1/4) (dark-energy scale)"]
CAND = {}
for bn, mu in (("hbar H0", m_H), ("hbar a0/c", m_a0), ("rho_L^(1/4)", m_DE)):
    for a_ in (1 / 4, 1 / 3, 1 / 2, 2 / 3, 3 / 4):
        CAND[f"m_P^{a_:.3g} ({bn})^{1 - a_:.3g}"] = M_PL_EV ** a_ * mu ** (1 - a_)
WIN_M = (1.9e-19, m_max_can if m_max_can else M_LIST[-1])           # the scanned canonical window (upstream bound)
hits_m = {k_: v_ for k_, v_ in CAND.items() if WIN_M[0] <= v_ <= WIN_M[1]}
span = math.log10(max(CAND.values()) / min(CAND.values()))
p_m = min(1.0, len(CAND) * math.log10(WIN_M[1] / WIN_M[0]) / span)
for k_, v_ in sorted(CAND.items(), key=lambda kv: kv[1]):
    P(f"    {k_:34s} = {v_:.3e} eV" + ("   <- in the canonical window" if k_ in hits_m else ""))
check("M5 (reported) NUMEROLOGY-FLAGGED: the Planck-scale geometric means that land in the scanned window (" + ", ".join(f"{k_} = {v_:.1e} eV" for k_, v_ in hits_m.items())
      + f"; m_P^(1/4)(hbar H0)^(3/4) = {CAND['m_P^0.25 (hbar H0)^0.75']:.1e} eV) have no mechanism producing their exponents, and some of "
      f"{len(CAND)} such combinations lands in a window this wide by chance with probability ~{p_m:.2f}",
      dict(hits={k_: f"{v_:.2e}" for k_, v_ in hits_m.items()}, p_chance=round(p_m, 2)), True, load_bearing=False)
OUT["numbers"]["M5"] = dict(candidates=CAND, hits=hits_m, p_chance=p_m)
P(f"  part M done   {elapsed()}")

# ================================================================================================ PART N: the amount
banner("N1  (reported) THE AMOUNT: misalignment of a free field, the inflationary equilibrium, and the misalignment's prior (sympy)")
mm, H0n, Orn, phii = sp.symbols("m H_0 Omega_r phi_i", positive=True)
a_osc = sp.sqrt(H0n * sp.sqrt(Orn) / mm)                              # H(a_osc) = m in radiation domination
rho_today = mm ** 2 * phii ** 2 / 2 * a_osc ** 3
P(f"    a_osc = {a_osc};  rho_today = (m^2 phi_i^2/2) a_osc^3 = {sp.simplify(rho_today)}  (~ m^(1/2) phi_i^2)")
H0eV = HBAR_EVS * H0_SI
MPr = M_PL_EV / math.sqrt(8 * math.pi)
rho_c_eV4 = 3 * H0eV ** 2 * MPr ** 2
Oc = 1 - OM_L - 0.0493                                               # Omega_c (Planck 2018: Omega_b = 0.0493)
phi_need = math.sqrt(2 * Oc * rho_c_eV4 / (m_floor ** 2 * (H0eV * math.sqrt(OR9) / m_floor) ** 1.5))
H_I = (8 * math.pi ** 2 * m_floor ** 2 * phi_need ** 2 / 3) ** 0.25
p_mis = 4 * 14.0 / 360.0
P(f"    at m = 1.9e-19 eV: phi_i = {phi_need:.2e} eV = {phi_need / MPr:.2e} M_P(reduced) for Omega_c = {Oc:.3f}; the action has no scale that "
  f"fixes it (no vev, no periodicity: Phi is not an angle)")
P(f"    a light spectator in long inflation relaxes to <phi^2> = 3 H_I^4/(8 pi^2 m^2): the amount is then set by H_I = {H_I:.2e} eV -- a new constant "
  f"outside the framework, not a derivation")
P(f"    the misalignment within 14 deg of the heavy axis (either sign) under an isotropic prior: {p_mis:.3f} (m_L^2/m_H^2 = 1 - 4e-6: the equilibrium "
  f"is isotropic to 4e-6)")
check("N1 (reported) the amount is INITIAL DATA: the free field's relic density ~ m^(1/2) phi_i^2 and nothing in the action fixes phi_i; "
      "the inflationary equilibrium trades it for H_I (outside the framework); the misalignment is a ~16% draw under an isotropic prior",
      f"phi_i {phi_need:.2e} eV ({phi_need / MPr:.1e} M_P); H_I {H_I:.2e} eV; P(misalignment) {p_mis:.3f}", True, load_bearing=False)
OUT["numbers"]["N1"] = dict(phi_i_eV=phi_need, phi_i_over_MP=phi_need / MPr, H_I_eV=H_I, p_misalignment=p_mis)
check("N2 (reported) THE FAIR COMPARISON: LCDM carries Omega_c (omega_c) as a fitted parameter too; the framework's amount has exactly "
      "that status; the misalignment angle is the one extra piece of initial data the dark sector carries beyond LCDM",
      "amount ~ omega_c (same status); misalignment: +1 initial datum", True, load_bearing=False)

# ================================================================================================ PART D: the count
banner("D  THE HONEST CONSTANT COUNT")
COUNT = [
    ("eps/m^2 (the splitting)", "1.84-2.35e-6 (575-650 km/s)", "FITTED-BY-DATA; IRREDUCIBLE", "Z4 spurion (E1, E2); window's ends from the flagship and Harvey (E4); kappa^19 NUMEROLOGY-FLAGGED (E3)"),
    ("zeta = f_t (lambda_0's normalisation)", f"canonical [{e_floor if e_floor is None else round(e_floor, 2)}, {ZW2['canonical'][1]:.2f}] at the floor mass",
     "FITTED-BY-DATA", "forest from below, flagship from above (XR12 W2); a decade-wide window on FP10's no-cap reading (M2); not shared: the yield-to-density maps miss by >= 5 decades (T1b) and FP13's state gives the onset and the collapse scale, not the threshold's height (T6); in XR19's delta_t0 the band sits between GR collapse's turnaround and virial contrasts (T6d)"),
    ("q (the K-gate exponent)", f"forest + A4: {win_can} canonical / {win_alt} alt; + filaments: {win_can_fil} / {win_alt_fil}", "FITTED-BY-DATA; sharing FAILS", "FP9's p' identifications convert the web (T3); FP13's q-sign ramp is global and fails the flagship or the background (T6a); forest below, web above (T3b); degenerate with zeta at z = 2.5"),
    ("  or, in the yield-onset construction", "q = 0", "SHARED (with the separator's frozen state)", "T4a/T4e: the frozen MOND scalar protects FRW and the forest-epoch IGM on either committed separator (H_Y, H_S); price: a MOND-scalar coupling (T4b), a POSTULATED gate form, zeta kept"),
    ("  or, the state-keyed virial trigger", "Delta = 18 pi^2 (no zeta, no q)", "FAILS (resolved reading)", "T6c: web- and background-safe, but the flagship's own-density cap (XR12-W2) fails on both footings; passes only on FP10's no-cap reading"),
    ("m (the dark mass)", (f"canonical C_s=10: [1.9e-19, <{closes[0]:.1e}] eV" if closes else "canonical: open over the grid") + (f"; upstream: sliver to {m_max_can:.1e}" if m_max_can else "; upstream: a sliver to the grid's end") + "; alt: >= floor",
     "FITTED-BY-DATA (canonical) / CONSTRAINED (alt)", "M1 (XR12 reading); M2: unpinned on FP10's reading; M3 ceiling ~1 eV; M5 NUMEROLOGY-FLAGGED"),
    ("the pure cross quartic", "structure", "POSTULATED", "Z4-even; its self-quartics are generated at O(lambda^2/16 pi^2) ~ 0 (lambda ~ 1e-76 at the floor)"),
    ("the amount (Omega_dm)", "initial data", "IRREDUCIBLE (as LCDM's omega_c)", "N1-N2"),
    ("the misalignment", "<= ~14 deg", "IRREDUCIBLE (initial data, ~16% prior)", "N1"),
]
for r_ in COUNT:
    P(f"    {r_[0]:40s} {r_[1]:44s} {r_[2]:34s} {r_[3]}")
WHOLE = dict(fitted=["kappa (accepted)", "eps/m^2", "zeta", "q", "m (canonical)"], bounded=["xi", "alpha_c", "c_2", "m (alt)", "lambda_phi > 0 (FP13: required, value free)"],
             separator="FP13's H_S (27faacc84): FP9's four declared constants replaced by state functionals; delta_c = 1.686, c_y = 1, the q = 0 onset POSTULATED (natural O(1) choices)", FP14="TBD",
             postulated=["J_P2", "the band-pass / yield forms", "the pure cross quartic"], initial=["phibar-dot", "the amount", "the misalignment"],
             measured=["G", "Lambda"])
P(f"    WHOLE THEORY: fitted {WHOLE['fitted']}; bounded {WHOLE['bounded']}; separator {WHOLE['separator']}; FP14 {WHOLE['FP14']}; "
  f"postulated {WHOLE['postulated']}; initial data {WHOLE['initial']}; measured {WHOLE['measured']}")
check("D (reported) the count: the dark sector is not knob-free -- eps FITTED-BY-DATA and irreducible, zeta and (canonical) m FITTED-BY-DATA, "
      "q constrained (or traded for the yield onset at a price), the amount and the misalignment initial data",
      dict(dark=[(r_[0], r_[2]) for r_ in COUNT], whole=WHOLE), True, load_bearing=False)
OUT["numbers"]["D"] = dict(dark=COUNT, whole=WHOLE)

# ================================================================================================ PART H: the hypotheses
banner("H  (reported) THE PRE-DECLARED HYPOTHESES, AS THEY FELL")
fil_all = sh_fil
HYP = [("H1 exponent sharing EXCLUDED (web)", fil_all and sh_mean_w2),
       ("H2 the shared gate makes the runaway WORSE", worse >= 30.0),
       ("H3 canonical band a sliver/closed at the floor; alt open", width_floor <= 1.25 and all(M1[mv]["open"]["alt/1"] for mv in M_LIST)),
       (f"H4 q has a window; zeta pinned (window found: {win_can} canonical; its lower edge is the forest's, not the background's 3/4)",
        len(win_can) >= 1 and width_floor <= 1.25),
       ("H5 yield-onset delta_Y >> 1 at the floor", dmin > 1.0),
       ("H6 eps Z4-protected, FITTED-BY-DATA", e1_ok),
       ("H7 m pinned on XR12's reading, not on FP10's", m1_ok),
       ("H8 the amount irreducible initial data", True),
       ("H9 not zero knobs", True)]
for k_, v_ in HYP:
    P(f"    {k_:60s} {'held' if v_ else 'FELL'}")
check("H (reported) the pre-declared hypotheses as they fell", {k_: bool(v_) for k_, v_ in HYP}, True, load_bearing=False)

# ================================================================================================ PART W: the ledger
banner("W  THE LEDGER: what this lane settles (link / status / basis)")
LEDGER = [
    ("L15a", "FK1's K-gate is (Omega_L(<K>_h)/Omega_L0)^q on CMC leaves: the trigger's running VARIABLE is the separator's own", "DERIVED", "check T1"),
    ("L15b", "the trigger's EXPONENT is not fixed by the action: three inequivalent identifications with FP9's p' (q = 3.75, 4, 4.75)", "DERIVED", "check T1"),
    ("L15c", "the anchor law: at a fixed z = 2.5 threshold, R(z) falls to z = 0 monotonically iff q >= 1/Omega_m0 - 1/4 = 2.94", "DERIVED", "check T2"),
    ("L15d", "sharing the exponent: every identification puts delta = 10 filaments above the trigger at every flagship anchor, and the "
     "cosmic mean at W2's (FP10's A4 fails): the web runaway made categorically worse", "FAILS", "check T3 (T3c: S_8 below the strict 0.922 in both web brackets; X-COP/Harvey lose the optimistic reading)"),
    ("L15e", "q is set by data, not shared: at the dark-mass floor the forest needs q >= ~1.75 (canonical; 1.5 alt) and A4 q <~ 2.9; "
     "keeping delta = 10 filaments below the trigger needs q <~ 1.75 -- FK1's declared 7/4 is where the two meet; degenerate with zeta "
     "at z = 2.5", "FITTED", "check T3b"),
    ("L15f", "zeta = f_t (lambda_0's normalisation): pinned between the forest and the flagship (canonical band <= 1.25 wide at the floor "
     "mass, XR12's resolved reading); a decade on FP10's no-cap reading; no dimensionless map to y_Lambda", "FITTED", "checks M1, M2, T3b"),
    ("L15g", "the yield onset as the trigger (-lambda_0 g(Y)(Im Phi^2)^2): exactly off on FRW and in the z >= 2.5 IGM (phi frozen), so q "
     "is not needed -- its job is done by the separator's p'", "DERIVED", "check T4a"),
    ("L15h", "the yield-onset gate's form g (width tied to y_th)", "POSTULATED", "check T4a"),
    ("L15i", "the yield-onset gate's reciprocal flux at the yield surface during conversion (delta_Y >> 1 at the floor; <= 0.1 needs a much "
     "heavier dark mass)", "CONSTRAINT", "check T4b"),
    ("L15j", "the yield-onset cell on the gates: mass-selective budget, forest, S_8 and the flagship's later passage (T4c-T4d); the "
     "cluster gates keep FP10's reading-dependence", "OPEN", "checks T4c, T4d, T5"),
    ("L15k", "eps is the only Z4-odd term (Phi -> i Phi): multiplicatively renormalised, generated by nothing present", "DERIVED", "check E1"),
    ("L15l", "no present coupling induces eps (pair, leaf average: 0; frame coupling: a relabelling; vacuum/Hubble scales: <= 1e-28 at the floor)",
     "DERIVED", "check E2"),
    ("L15m", "eps/m^2 = 1.84-2.35e-6 set by the flagship (lower) and Harvey (upper); kappa^19 is numerology", "FITTED", "checks E3, E4"),
    ("L15n", "m: pinned near its floor on the canonical footing (the forest's minihalos vs the flagship's cap), open on alt; unpinned on "
     "FP10's no-cap reading", "FITTED", "checks M1, M2"),
    ("L15o", "m <~ 1 eV (Bose occupation of the pump)", "CONSTRAINT", "check M3"),
    ("L15p", "a mechanism for m (the ties m_P^a mu^(1-a) that land in the window are numerology)", "OPEN", "check M5"),
    ("L15q", "the amount (as LCDM's omega_c) and the misalignment (~16% prior): initial data", "POSTULATED", "checks N1, N2"),
    ("L15r", "XR19's seeded web runaway (FK1's band top is seed-stimulable at the mean for z <~ 0.5), the forest proxy's ~2x systematic, "
     "the own-density cap in FP10's reading, the chain's own spherical-collapse numbers (XR23) as a derived threshold, and a "
     "particle-mesh run with the trigger", "OPEN", "scope; not computed here"),
    ("L15s", "lambda_0's normalisation is not shared with the yield: a0^2 = kappa^2 c^2 G rho_Lambda maps y_th a0 to a density >= 5 decades "
     "too low; a0/(4 pi G L) needs a coefficient and runs as q = 3/4", "DERIVED", "check T1b"),
    ("L15t", "the yield-onset gate on FP13's H_S: the web is MOND-on below z = 0.635, so zeta alone holds the late web; the q-running stays "
     "unnecessary; the flagship's passage comes earlier", "OPEN", "check T4e"),
    ("L15u", "a dark trigger keyed to FP13's state with no new constant (the q-sign onset and/or the local nonlinearity at delta_c): the "
     "onset is global (flagship or background fail) and delta_c sits below the web's filaments (the web converts)", "FAILS", "check T6 (a), (b)"),
    ("L15w", "sharing the threshold delta_t0 (XR19's dominant lever) with GR spherical collapse: the gates' band sits between the "
     "turnaround (9 pi^2/16) and the virial (18 pi^2) contrasts, and neither they nor 1 + delta_c land in it", "FAILS",
     "check T6d (the chain's own collapse, XR23, is pending: OPEN in L15r)"),
    ("L15v", "the spherical-collapse partner Delta = 18 pi^2 as the trigger (no zeta, no q): web- and background-safe, fails the flagship's "
     "own-density cap on both footings and the forest (early z >= 4 conversion); the flagship passes only on FP10's no-cap reading", "FAILS", "check T6 (c)"),
]
for k_, what, st, basis in LEDGER:
    P(f"    {k_:6s} {st:10s} {what}  --  {basis}")
OUT["ledger"] = [dict(link=k_, what=w_, status=s_, basis=b_) for k_, w_, s_, b_ in LEDGER]
check("W (reported) the ledger of this lane's links", f"{len(LEDGER)} links", True, load_bearing=False)

# ================================================================================================ verdict
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
_nesc_B = sum(not r_["escaped"] for r_ in rows_B)
TXT_B = ((f"{_nesc_B}/{len(rows_B)} progenitor cells do not escape (v_esc up to {vmaxB:.0f} km/s) and fall to FP10's in-place bracket -- "
          f"worst flagship shift per kick " + ", ".join(f"{v_:.0f}: {x_:.3f}" for v_, x_ in fl_kick_B.items()) + " dex")
         if _nesc_B else f"every progenitor escapes; worst flagship shift {max(fl_kick_B.values()):.4f} dex")
banner("VERDICT")
P(f"""  TRIGGER SHARING.  The running VARIABLE is already shared: on CMC leaves FK1's K-gate is (Omega_L(<K>_h)/Omega_L0)^q.  The
  EXPONENT is not: the action allows three identifications with the separator's p' = {p9:g} (q = 3.75, 4, 4.75), and every one fails the
  web -- anchored where the flagship needs the threshold at z = 2.5, the steep running drops it under delta = 10 filaments at every
  anchor on the record and under the cosmic mean itself at W2's (FP10's own A4 requirement), >= {worse:.0f}x worse than FK1's q = 7/4.
  q is therefore not shared but set by data: the forest (from below) and the web's filaments (from above) meet at FK1's declared 7/4.
  The YIELD ONSET can replace q outright: a trigger gated by the MOND scalar's own on-state is exactly off on FRW and in the frozen
  z >= 2.5 IGM, so the K-running is not needed and the conversion becomes mass-selective (share >= 1e10.5 at z = 2/3/4:
  {selY[2.0]:.2f}/{selY[3.0]:.2f}/{selY[4.0]:.2f} vs FK1's {sel_fk1[2.0]:.2f}/{sel_fk1[3.0]:.2f}/{sel_fk1[4.0]:.2f}); its price is a POSTULATED gate form, a
  reciprocal flux at the yield surface (delta_Y,max {dmin:.2g}+ at the floor mass) and, on FP9's H_Y, a late clearing of r_F (z' ~
  {min(zp_B):.1f}-{max(zp_B):.1f}: {TXT_B}); on FP13's H_S {sum(r_['escaped'] for r_ in rows_S)}/{len(rows_S)} progenitor cells escape
  (z' ~ {min(zp_S):.1f}-{max(zp_S):.1f}; worst flagship shift {max(fl_kick_S.values()):.4f} dex).
  lambda_0 cannot be shared: the framework's own yield-to-density map lands >= 5 decades too low, so zeta is FITTED BY DATA.
  FP13'S STATE (H_S).  The yield-onset gate works on H_S too (forest {[v_['forest'] for k_, v_ in T4E.items() if 'centre' in k_][0]:.3f}, progenitors
  cleared at z' ~ {min(zp_S):.1f}-{max(zp_S):.1f}, share >= 1e10.5 {selS[2.0]:.2f}/{selS[3.0]:.2f}/{selS[4.0]:.2f}); the web is MOND-on below z = 0.635, so zeta holds the late web.  A
  trigger keyed to H_S's quantities with no new constant fails: the q-sign onset is global (keyed to it alone the flagship or the
  background fails), and the local nonlinearity at delta_c = 1.686 sits under the web's filaments (the web converts); the state
  gives WHEN and WHERE, not the HEIGHT the dark threshold needs (>= {min(need_ratio.values()):.0f}x above 1 + delta_c).  Its spherical-collapse
  partner 18 pi^2 has the right order and no constant, but the flagship's own-density cap rejects it on both footings (S(r_F) =
  {cap_vir['canonical']:.2f}/{cap_vir['alt']:.2f} > 0.059) and so does the forest ({fV['worst']:.2f}: it converts z >= 4 halos too early).
  XR19's dominant lever, the threshold delta_t0, wants [{BAND_DT0['canonical'][0]:.1f}, {BAND_DT0['canonical'][1]:.1f}] (canonical; alt to {BAND_DT0['alt'][1]:.1f}):
  between spherical collapse's turnaround (5.55) and virial (178) contrasts -- no GR collapse number lands in it; the virial 178 (with
  FK1's running) passes the forest and the web and only the own-density cap excludes it (the chain's own collapse, XR23, is pending).
  eps.  Z4 (Phi -> i Phi) protects it: every other term is even, eps is odd, the one-loop split is proportional to eps and nothing
  present generates it; a frame coupling only relabels it, Hubble-scale splittings are >= 1e20 too small.  IRREDUCIBLE; its value is
  FITTED BY DATA (flagship below, Harvey above); kappa^19 is numerology.
  m.  On XR12's resolved reading the forest's lower bound on zeta rises with m (the fluid's minihalos convert) into the flagship's
  upper bound: at the floor the canonical band is x{width_floor:.2f} wide and it closes for heavier fluids -- m is pinned near its floor
  on the canonical footing (FITTED BY DATA), open on alt; on FP10's no-cap reading it is only bounded.  Its ties (m_P^(1/4)(hbar H0)^(3/4)
  etc.) are numerology.  The amount is initial data, as LCDM's omega_c; the misalignment is one extra datum.
  THE COUNT.  Dark sector: eps FITTED (irreducible), zeta FITTED, q FITTED, m FITTED (canonical) / bounded (alt) -- or, with the
  yield onset, q eliminated and zeta, m bounded to wide windows at the price of a postulated gate form; 1 postulated structure
  (the cross quartic), 2 initial data -- not zero knobs.  Not 'closed' as a theory.""")
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["runtime_s"] = len(CH), n_fail, time.time() - T0


def _jd(o):
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, (np.bool_,)): return bool(o)
    if isinstance(o, tuple): return list(o)
    return str(o)


def _clean(o):
    if isinstance(o, dict):
        return {str(k_): _clean(v_) for k_, v_ in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v_) for v_ in o]
    return o


for _k in list(FCACHE):
    FCACHE[_k].pop("S", None)
outname = f"{SLUG}_results.json".replace("_MUTATE_results", "_results_MUTATE")
OUTDIR = SMOKE_DIR if SMOKE else HERE                                  # a smoke run never writes into the lane directory
if OUTDIR:
    json.dump(_clean(OUT), open(os.path.join(OUTDIR, outname), "w"), indent=1, default=_jd)
P(f"\n  {len(CH) - sum(1 for _, ok, _ in CH if not ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   {elapsed()}")
sys.exit(0 if n_fail == 0 else 1)
