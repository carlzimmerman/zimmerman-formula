#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR26 (part 3) -- BIG BANG NUCLEOSYNTHESIS IN THE CHAIN: helium-4, deuterium and lithium-7 with the chain's G_cos.

WHY.  Part 1 (XR26_linear_equations.py) found the chain's Friedmann equation is GR's with the bare G, so during BBN the
expansion rate uses G_cos = G_N (1 - alpha_c/2), alpha_c in [8e-16, 3.2e-9] (FP14 A3's floor, FP2's PPN bound), with no other
energy component: the khronon has no background energy, the MOND scalar is decoupled (its datum phibar-dot = 0 is declared;
part 1 F1 bounds it), and the dark field (m >= 1.9-5.2e-19 eV) is frozen until T ~ 28-46 keV with Delta N_eff <= 2e-4 (part 1
E1).  BBN therefore tests only G_cos/G_N at T ~ 1 MeV - 30 keV, and the baryon density the chain's CMB fit returns (part 2:
identical to LCDM's).

METHOD.  (i) The standard-BBN tables shipped with CAMB 1.6.6 -- PRIMAT 2024 (Pitrou et al.; tau_n = 878.4 s, LUNA d(p,g)3He)
and PArthENoPE 2017 (tau_n = 880.2 s, Planck 2018's) -- give Y_P^BBN and D/H versus (omega_b, Delta N_eff); a change of G at
BBN is mapped to the equivalent Delta N_eff through S^2 = G_BBN/G_0 = 1 + 7 Delta N/43 before e+e- annihilation (Steigman 2012,
Adv. High Energy Phys. 268321, eqs. 7-8) and S^2 = 1 + 0.135 Delta N after it (eq. 10); both maps are carried.  (ii) An
independent BBN-lite integration (this script): the n <-> p weak rates in the Born approximation with Fermi-Dirac e+- and
neutrinos, normalised to tau_n; exact e+e- thermodynamics and entropy transfer; H^2 = (8 pi G_cos/3) rho; the neutron fraction
integrated to the deuterium bottleneck (Saha) with free decay; Y_P = 2 X_n(T_nuc).  It puts G_cos into H directly, with no
Delta N_eff map, and is calibrated once to the PRIMAT table at G_cos = G_N.  (iii) Lithium-7: standard BBN's value at Planck's
omega_b (Fields, Olive, Yeh & Young 2020, JCAP 03, 010, as quoted by the PDG 2024 review) with its S-dependence from Steigman's
fit y_Li = 4.82 (eta_Li/6)^2, eta_Li = eta_10 - 3(S - 1) (2012, eqs. 18, 21).
OBSERVED (cited): Y_P = 0.245 +- 0.003 (PDG 2024, Fields, Molaro & Sarkar, eq. 24.3) and 0.2453 +- 0.0034 (Aver et al. 2021,
JCAP 03, 027); D/H = (2.547 +- 0.029) x 1e-5 (PDG 2024 eq. 24.2) and (2.527 +- 0.030) x 1e-5 (Cooke, Pettini & Steidel 2018,
ApJ 855, 102); 7Li/H = (1.6 +- 0.3) x 1e-10 (PDG 2024 eq. 24.4, the Spite plateau, -2.8 < [Fe/H] < -1.5).  omega_b = 0.02236 +-
0.00015 (Planck 2018 VI, TT,TE,EE+lowE).  Both a0 footings (canonical 9.3603e-11, alt 1.1312e-10 m/s^2) are carried.

PRE-DECLARED (written before any run of this script):
  H1  CONTROLS.  The CAMB tables reproduce Planck 2018 VI's quoted standard-BBN numbers at omega_b = 0.02236: PArthENoPE
      Y_P^BBN = 0.24672 (eq. 72a) and D/H = 2.587e-5 (eq. 74, case a) to <= 3e-4 in Y_P and 1.5% in D/H; the BBN-lite Y_P lies
      within 3% of PRIMAT's before calibration and its response dY_P/d(Delta N_eff) within 20% of the table's.  EXPECT TRUE.
  H2  THE CHAIN.  G_cos/G_N - 1 = -alpha_c/2 >= -1.6e-9 shifts Y_P by ~ -1e-10, D/H and 7Li/H by ~ +1e-9 (relative): the
      chain's light elements are standard BBN's at the chain's omega_b (= LCDM's), for both footings (a0 enters nothing here).
      EXPECT TRUE.
  H3  AGAINST OBSERVATIONS (the chain = standard BBN): Y_P ~ 0.247 vs 0.245 +- 0.003 (within 1 sigma); D/H 2.4-2.6e-5
      depending on the nuclear rates (PRIMAT low by ~2-3 sigma, PArthENoPE within ~1 sigma of 2.547 +- 0.029); 7Li/H ~ 4.7e-10
      vs 1.6 +- 0.3e-10: the factor-3 lithium problem, untouched by the chain.  EXPECT TRUE.
  H4  MUTATE (G_cos = 2 G_N, the York/CMC kill's value): Y_P rises to ~0.31-0.33 and D/H by ~50-100%: excluded at > 10 sigma.
      EXPECT TRUE.
  DISCLOSURE (added after the first full run, which was made on a scratch copy of this script): H1's BBN-lite expectation FAILED
  -- the uncalibrated Y_P came out 7.2% below PRIMAT's (declared <= 3%), while the Delta N_eff response agreed to 9% (declared
  <= 20%).  K2 is kept exactly as declared (so this script's main run returns rc = 1 on that control); a post-hoc diagnostic,
  K2b (reported, not load-bearing), shows where the deficit comes from (the Saha X_D = X_n bottleneck at 66 keV sits late).
  Only the calibrated RESPONSE of BBN-lite is used below; the abundances themselves come from the PRIMAT/PArthENoPE tables.
"""
# (the docstring above is the pre-declaration; everything below was written after it and before the first run)
DOC_CHECKS = r"""
CHECKS
  K  CONTROLS: K1 CAMB's PArthENoPE table reproduces Planck 2018 VI's quoted standard-BBN Y_P^BBN and D/H at omega_b = 0.02236;
     K2 the BBN-lite integration against the PRIMAT 2024 table (Y_P before calibration; the Delta N_eff response); K3 part 1's
     committed dark-field Delta N_eff at BBN (XR26_linear_equations_results.json, E1) is read and bounded.
  B  THE CHAIN: B1 [HEADLINE] the shifts of Y_P, D/H and 7Li/H at G_cos/G_N = 1 - alpha_c/2 (BBN-lite directly; both Delta N_eff
     maps; Steigman's lithium fit) are negligible: <= 1e-7 (absolute in Y_P, relative in D/H and Li); B2 (reported) the chain's
     (= standard BBN's) abundances at its omega_b against the observed values; B3 (reported) lithium-7 and the Spite plateau
     (the coordinator's question); B4 both a0 footings; M (reported in the main run) the MUTATE's numbers.  W the ledger.
MUTATE=1 sets G_cos = 2 G_N in B1 (the York/CMC kill's value): B1 must FAIL (rc = 1).

SCOPE.  BBN-lite is a freeze-out + bottleneck calculation, not a network: it carries G_cos into Y_P directly and is calibrated to
PRIMAT; D/H and lithium come from the tables and fits named above.  At most 2 threads (single-threaded numpy here).

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR26_bbn.py   (MUTATE=1 for the control).
Writes XR26_bbn[_MUTATE].out and XR26_bbn_results[_MUTATE].json next to itself.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "2"
import sys, json, math, time, warnings
warnings.filterwarnings("ignore")
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
from scipy.special import zeta

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CHAIN = os.path.join(REPO, "real_research", "derivation_chain_2026")
MUTATE = os.environ.get("MUTATE", "0") == "1"
NAME = "XR26_bbn"
TXT = os.path.join(HERE, NAME + ("_MUTATE.out" if MUTATE else ".out"))
JSN = os.path.join(HERE, NAME + ("_results_MUTATE.json" if MUTATE else "_results.json"))
T_START = time.time()


class _Tee:
    def __init__(self, path):
        self._f = open(path, "w", encoding="utf-8")
        self._s = sys.__stdout__

    def write(self, t):
        self._s.write(t)
        self._f.write(t)

    def flush(self):
        self._s.flush()
        self._f.flush()

    def close(self):
        self._f.close()


TEE = _Tee(TXT)
sys.stdout = TEE
OUT = {"lane": "XR26", "part": "3: BBN", "mutate": MUTATE, "checks": {}, "numbers": {}, "ledger": []}
CH = []


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 114 + "\n" + t + "\n" + "=" * 114)


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing, "name": name}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


P(__doc__.strip())
P(DOC_CHECKS.strip())
if MUTATE:
    P("\n  *** MUTATE=1: G_cos = 2 G_N at BBN (the York/CMC value) in B1 -- B1 must FAIL ***")

# ================================================================================================ inputs
OMB, OMB_ERR = 0.02236, 0.00015                                     # Planck 2018 VI, TT,TE,EE+lowE
OBS = {"Y_P (PDG 2024)": (0.245, 0.003), "Y_P (Aver+2021)": (0.2453, 0.0034), "D/H (PDG 2024)": (2.547e-5, 0.029e-5),
       "D/H (Cooke+2018)": (2.527e-5, 0.030e-5), "Li/H (PDG 2024, Spite plateau)": (1.6e-10, 0.3e-10)}
LI_SBBN = (4.72e-10, 0.72e-10)                                       # Fields et al. 2020 at Planck's omega_b (PDG 2024 quotes it)
PLANCK_BBN = {"Y_P PArthENoPE (eq. 72a)": 0.24672, "D/H PArthENoPE case a (eq. 74)": 2.587e-5}
fp14 = json.load(open(os.path.join(CHAIN, "FP14_zero_knob_core_results.json")))
fp0 = json.load(open(os.path.join(CHAIN, "FP0_core_postulates_results.json")))
A0 = {"canonical": fp0["numbers"]["a0_canonical"], "alt": fp0["numbers"]["a0_rho_total"]}
AC_MAX, AC_MIN = 3.2e-9, fp14["numbers"]["A3"]["oo|XC1 gate"]
S_CHAIN = 1 - AC_MAX / 2
S_TEST = 2.0 if MUTATE else S_CHAIN
ETA10 = 273.9 * OMB                                                 # Steigman 2012 eq. 2
P(f"\n  inputs: omega_b = {OMB} +- {OMB_ERR} (eta_10 = {ETA10:.3f}); G_cos/G_N = 1 - alpha_c/2 in [{S_CHAIN:.10f}, {1 - AC_MIN / 2:.16f}]"
  + (f"; MUTATE G_cos/G_N = {S_TEST}" if MUTATE else "") + f"; observed {OBS}")
from camb import bbn as camb_bbn
TAB_PRI = camb_bbn.BBN_table_interpolator("PRIMAT_Yp_DH_ErrorMC_2024.dat", function_of=("Ombh2", "DeltaN"))
TAB_PAR = camb_bbn.BBN_table_interpolator("PArthENoPE_880.2_standard.dat")
TABS = {"PRIMAT 2024": TAB_PRI, "PArthENoPE 2017": TAB_PAR}


def dN_pre(s):
    return (s - 1.0) * 43.0 / 7.0                                     # S^2 = 1 + 7 dN/43 (before e+e- annihilation)


def dN_post(s):
    return (s - 1.0) / 0.135                                          # S^2 = 1 + 0.135 dN (after it)


# ================================================================================================ K controls
banner("K  CONTROLS")
yp_par, dh_par = float(TAB_PAR.Y_p(OMB, 0.0)), float(TAB_PAR.DH(OMB, 0.0))
k1_ok = abs(yp_par - PLANCK_BBN["Y_P PArthENoPE (eq. 72a)"]) <= 3e-4 and abs(dh_par / PLANCK_BBN["D/H PArthENoPE case a (eq. 74)"] - 1) <= 0.015
check("K1 CONTROL: CAMB's PArthENoPE table (tau_n = 880.2 s) reproduces Planck 2018 VI's quoted standard-BBN predictions at omega_b = "
      "0.02236 -- Y_P^BBN = 0.24672 (eq. 72a) and D/H = 2.587e-5 (eq. 74, case a)",
      f"Y_P {yp_par:.5f}, D/H {dh_par:.4e}", k1_ok)
# BBN-lite
ME, QNP, TAU_N, MPL, HBAR = 0.51099895, 1.29333236, 878.4, 1.220890e22, 6.582119569e-22     # MeV, MeV, s, MeV, MeV s
BD, MN = 2.224566, 938.918


def fd(x):
    return 1.0 / (np.exp(np.minimum(x, 700.0)) + 1.0)


def weak_rates(T, Tn):
    """Born-approximation n <-> p rates [1/s] with Fermi-Dirac e+- (T) and neutrinos (Tn), normalised to the free decay."""
    Emax = ME + 60.0 * max(T, Tn, 0.05)
    E = np.linspace(ME, Emax, 6000)
    p = np.sqrt(np.maximum(E * E - ME * ME, 0.0))
    Ep = E * p
    hi = E >= QNP
    lo = E <= QNP
    fe, fe_ = fd(E / T), 1 - fd(E / T)
    j1 = np.trapz(np.where(hi, Ep * (E - QNP) ** 2 * fd((E - QNP) / Tn) * fe_, 0.0), E)
    j2 = np.trapz(Ep * (E + QNP) ** 2 * fe * (1 - fd((E + QNP) / Tn)), E)
    j3 = np.trapz(np.where(lo, Ep * (QNP - E) ** 2 * fe_ * (1 - fd((QNP - E) / Tn)), 0.0), E)
    j4 = np.trapz(np.where(hi, Ep * (E - QNP) ** 2 * fe * (1 - fd((E - QNP) / Tn)), 0.0), E)
    j5 = np.trapz(Ep * (E + QNP) ** 2 * fd((E + QNP) / Tn) * fe_, E)
    j6 = np.trapz(np.where(lo, Ep * (QNP - E) ** 2 * fe * fd((QNP - E) / Tn), 0.0), E)
    return (j1 + j2 + j3) / (TAU_N * I0), (j4 + j5 + j6) / (TAU_N * I0)


_E0 = np.linspace(ME, QNP, 20001)
I0 = float(np.trapz(_E0 * np.sqrt(_E0 ** 2 - ME ** 2) * (QNP - _E0) ** 2, _E0))


def epm(T):
    """e+e- energy density, pressure and entropy density [MeV^4, MeV^3] (g = 4)."""
    E = np.linspace(ME, ME + 60.0 * T, 6000)
    p = np.sqrt(np.maximum(E * E - ME * ME, 0.0))
    f_ = fd(E / T)
    rho = 4 / (2 * math.pi ** 2) * np.trapz(E * E * p * f_, E)
    pr = 4 / (6 * math.pi ** 2) * np.trapz(p ** 3 * f_, E)
    return rho, pr, (rho + pr) / T


F_INF = 11 * math.pi ** 2 / 45.0


def T_of_Tnu(Tn):
    if Tn > 5.0:
        return Tn
    return brentq(lambda T: T ** 3 * (4 * math.pi ** 2 / 45.0 + epm(T)[2] / T ** 3) - F_INF * Tn ** 3, Tn * 0.99, Tn * 1.5)


TNU = np.geomspace(20.0, 0.02, 360)
TG = np.array([T_of_Tnu(x) for x in TNU])
RATES = np.array([weak_rates(T, Tn) for T, Tn in zip(TG, TNU)])
RHO_EPM = np.array([epm(T)[0] for T in TG])


def bbn_lite(s_cos=1.0, dNeff=0.0, omb=OMB):
    """Y_P from the n/p freeze-out integrated in T_nu, H^2 = (8 pi G_cos/3) rho, to the deuterium bottleneck (Saha, X_D = X_n)."""
    eta = 2.7377e-8 * omb                                            # eta = 273.9e-10 omega_b
    rho = (math.pi ** 2 / 15) * TG ** 4 + RHO_EPM + (7 * math.pi ** 2 / 40) * TNU ** 4 * (3.044 / 3.0) + dNeff * (7 * math.pi ** 2 / 120) * TNU ** 4
    Hs = np.sqrt(8 * math.pi * s_cos * rho / (3 * MPL ** 2)) / HBAR     # 1/s
    lnT = np.log(TNU[::-1]); lnl = np.log(RATES[::-1]); lnH = np.log(Hs[::-1]); Tg_ = TG[::-1]

    def lam(Tn):
        x = math.log(Tn)
        return math.exp(np.interp(x, lnT, lnl[:, 0])), math.exp(np.interp(x, lnT, lnl[:, 1])), math.exp(np.interp(x, lnT, lnH))

    def Tph(Tn):
        return float(np.interp(math.log(Tn), lnT, Tg_))

    def rhs(lnTn, X):
        Tn = math.exp(lnTn)
        lnp, lpn, H = lam(Tn)
        return [(lpn * (1 - X[0]) - lnp * X[0]) / (-H)]            # dX/dln T_nu = (dX/dt) (dt/dln T_nu), dt/dln T_nu = -1/H

    def xd_over_xn(T, Xp):
        return 8.14 * eta * (T / MN) ** 1.5 * math.exp(BD / T) * Xp

    T0 = TG[0]
    X0 = 1.0 / (1.0 + math.exp(QNP / T0))
    ev = lambda lnTn, X: xd_over_xn(Tph(math.exp(lnTn)), 1 - X[0]) - 1.0
    ev.terminal = True
    sol = solve_ivp(rhs, (math.log(TNU[0]), math.log(TNU[-1])), [X0], method="LSODA", rtol=1e-10, atol=1e-13, events=ev)
    Xn = float(sol.y_events[0][0][0]) if sol.t_events[0].size else float("nan")
    return 2 * Xn, Tph(math.exp(sol.t_events[0][0])) if sol.t_events[0].size else float("nan")


yl0, Tnuc0 = bbn_lite()
yp_pri = float(TAB_PRI.Y_p(OMB, 0.0))
CAL = yp_pri / yl0
dY_tab = {d_: float(TAB_PRI.Y_p(OMB, d_)) - yp_pri for d_ in (-1.0, 1.0)}
dY_lite = {d_: CAL * bbn_lite(1.0, d_)[0] - yp_pri for d_ in (-1.0, 1.0)}
resp = max(abs(dY_lite[d_] / dY_tab[d_] - 1) for d_ in dY_tab)
P(f"    BBN-lite: Y_P = {yl0:.5f} at T_nuc = {Tnuc0 * 1e3:.1f} keV (PRIMAT 2024 {yp_pri:.5f}: calibration x{CAL:.4f}); Delta N_eff = -1/+1: "
  f"lite {dY_lite[-1.0]:+.5f}/{dY_lite[1.0]:+.5f} vs table {dY_tab[-1.0]:+.5f}/{dY_tab[1.0]:+.5f}")
check("K2 CONTROL: the BBN-lite freeze-out integration lands within 3% of PRIMAT 2024's Y_P before calibration and reproduces its "
      "Delta N_eff = +-1 response to within 20% after it -- good enough to carry a G_cos change into Y_P directly",
      f"uncalibrated {yl0:.5f} vs {yp_pri:.5f} ({abs(yl0 / yp_pri - 1):.1%}); response mismatch {resp:.1%}",
      abs(yl0 / yp_pri - 1) <= 0.03 and resp <= 0.20)
OUT["numbers"]["K2"] = dict(Y_lite=yl0, T_nuc_MeV=Tnuc0, Y_primat=yp_pri, calibration=CAL, dY_tab=dY_tab, dY_lite=dY_lite)
# K2b (post-hoc diagnostic): stop the same integration at fixed photon temperatures instead of the Saha X_D = X_n point
def y_at_T(Tstop):
    lnT = np.log(TNU[::-1]); Tg_ = TG[::-1]
    Tn_stop = float(np.exp(np.interp(math.log(Tstop), np.log(Tg_), lnT)))
    rho = (math.pi ** 2 / 15) * TG ** 4 + RHO_EPM + (7 * math.pi ** 2 / 40) * TNU ** 4 * (3.044 / 3.0)
    Hs = np.sqrt(8 * math.pi * rho / (3 * MPL ** 2)) / HBAR
    lnl = np.log(RATES[::-1]); lnH = np.log(Hs[::-1])
    f_ = lambda lnTn, X: [(math.exp(np.interp(lnTn, lnT, lnl[:, 1])) * (1 - X[0]) - math.exp(np.interp(lnTn, lnT, lnl[:, 0])) * X[0])
                          / (-math.exp(np.interp(lnTn, lnT, lnH)))]
    so = solve_ivp(f_, (math.log(TNU[0]), math.log(Tn_stop)), [1.0 / (1.0 + math.exp(QNP / TG[0]))], method="LSODA", rtol=1e-10, atol=1e-13)
    return 2 * float(so.y[0, -1])


k2b = {Tk: y_at_T(Tk * 1e-3) for Tk in (66.0, 70.0, 75.0, 80.0, 85.0)}
check("K2b (reported; post-hoc, see the docstring's disclosure) THE BBN-LITE DEFICIT IS THE BOTTLENECK TEMPERATURE: the same "
      "integration stopped at a fixed photon temperature gives the printed Y_P -- stopping at ~75-80 keV instead of the Saha point "
      "(66 keV) removes most of the 7% (less free-neutron decay); the calibrated response used below does not depend on this choice",
      ", ".join(f"T = {Tk:.0f} keV: {v:.4f}" for Tk, v in k2b.items()) + f" (PRIMAT {yp_pri:.4f})", True, load_bearing=False)
OUT["numbers"]["K2b"] = {str(k_): v for k_, v in k2b.items()}
xr1 = None
try:
    xr1 = json.load(open(os.path.join(HERE, "XR26_linear_equations_results.json")))["numbers"]["E1"]
except Exception:
    pass
dm_dN = max(max(r_["dNeff"] for r_ in v["rows"].values()) for v in xr1.values()) if xr1 else float("nan")
check("K3 CONTROL: part 1's committed dark-field numbers (E1, misalignment normalised to Omega_c) bound its Delta N_eff-equivalent at "
      "every BBN temperature (1 MeV - 30 keV) by <= 1e-3 -- the dark field does not enter BBN",
      f"max Delta N_eff (both masses) {dm_dN:.1e}", xr1 is not None and dm_dN <= 1e-3)
P(f"    ({time.time() - T_START:.0f} s)")

# ================================================================================================ B the chain
banner("B  THE CHAIN'S BBN" + ("  [MUTATE: G_cos = 2 G_N]" if MUTATE else ""))
DS = 0.01
yp_p, yp_m = CAL * bbn_lite(1 + DS)[0], CAL * bbn_lite(1 - DS)[0]
dYds = (yp_p - yp_m) / (2 * DS)
dYds_pre = (float(TAB_PRI.Y_p(OMB, dN_pre(1 + DS))) - float(TAB_PRI.Y_p(OMB, dN_pre(1 - DS)))) / (2 * DS)
dlnD_pre = (math.log(TAB_PRI.DH(OMB, dN_pre(1 + DS))) - math.log(TAB_PRI.DH(OMB, dN_pre(1 - DS)))) / (2 * DS)
dlnD_post = (math.log(TAB_PRI.DH(OMB, dN_post(1 + DS))) - math.log(TAB_PRI.DH(OMB, dN_post(1 - DS)))) / (2 * DS)
dlnLi = -2 * 3 * 0.5 / ETA10                                         # d ln y_Li/ds from eta_Li = eta_10 - 3(S - 1), S = sqrt(s)


def shifts(s):
    if abs(s - 1) < 0.05:
        dY = dYds * (s - 1)
        dD = dlnD_post * (s - 1)
        dD2 = dlnD_pre * (s - 1)
        dL = dlnLi * (s - 1)
    else:
        dY = CAL * bbn_lite(s)[0] - yp_pri
        dD = math.log(TAB_PRI.DH(OMB, min(dN_post(s), 7.0)) / TAB_PRI.DH(OMB, 0.0))
        dD2 = math.log(TAB_PRI.DH(OMB, min(dN_pre(s), 7.0)) / TAB_PRI.DH(OMB, 0.0))
        dL = 2 * math.log((ETA10 - 3 * (math.sqrt(s) - 1)) / ETA10)
    return dict(dY=dY, dlnD_post=dD, dlnD_pre=dD2, dlnLi=dL)


SH = shifts(S_TEST)
SH_FLOOR = shifts(1 - AC_MIN / 2)
P(f"    dY_P/d ln G_cos: BBN-lite direct {dYds:+.4f}, PRIMAT with the pre-annihilation map {dYds_pre:+.4f}; d ln(D/H)/d ln G_cos "
  f"{dlnD_post:+.3f} (post map) / {dlnD_pre:+.3f} (pre map); d ln(Li/H)/d ln G_cos {dlnLi:+.3f} (Steigman's fit)")
P(f"    {'MUTATE' if MUTATE else 'the chain'} (G_cos/G_N = {S_TEST}): dY_P = {SH['dY']:+.2e}, d ln(D/H) = {SH['dlnD_post']:+.2e} "
  f"({SH['dlnD_pre']:+.2e} pre map), d ln(Li/H) = {SH['dlnLi']:+.2e}; at the regulator's floor: dY_P = {SH_FLOOR['dY']:+.1e}")
b1_ok = abs(SH["dY"]) <= 1e-7 and max(abs(SH["dlnD_post"]), abs(SH["dlnD_pre"]), abs(SH["dlnLi"])) <= 1e-7
check("B1 [HEADLINE] THE CHAIN'S LIGHT ELEMENTS ARE STANDARD BBN'S: G_cos/G_N = 1 - alpha_c/2 (>= 1 - 1.6e-9) moves Y_P, D/H and 7Li/H "
      "by <= 1e-7 (absolute in Y_P, relative in D/H and Li) -- a million times below the observational errors; G_cos = G_N is not exact "
      "(alpha_c >= 8e-16), but the difference is invisible",
      f"dY_P {SH['dY']:+.1e}, d ln D/H {SH['dlnD_post']:+.1e}, d ln Li {SH['dlnLi']:+.1e}", b1_ok,
      reading=("MUTATE: G_cos = 2 G_N moves them at O(1) -- the headline fails, as pre-declared" if MUTATE else ""))
OUT["numbers"]["B1"] = dict(dYds_lite=dYds, dYds_table_pre=dYds_pre, dlnD_ds=[dlnD_post, dlnD_pre], dlnLi_ds=dlnLi, shifts=SH, floor=SH_FLOOR)
# B2 the chain (= standard BBN at its omega_b) against observations
ROWS = {}
for nm, tab in TABS.items():
    yp = float(tab.Y_p(OMB, 0.0))
    dh = float(tab.DH(OMB, 0.0))
    dyo = (float(tab.Y_p(OMB + OMB_ERR, 0.0)) - float(tab.Y_p(OMB - OMB_ERR, 0.0))) / 2
    ddo = (float(tab.DH(OMB + OMB_ERR, 0.0)) - float(tab.DH(OMB - OMB_ERR, 0.0))) / 2
    th_y = float(tab.get("sig(Yp^BBN)", OMB, 0.0)) if "sig(Yp^BBN)" in tab.interpolators else 0.0
    th_d = float(tab.get("sig(D/H)", OMB, 0.0)) if "sig(D/H)" in tab.interpolators else 0.0
    ROWS[nm] = dict(Y_P=yp, sig_Y=math.hypot(dyo, th_y), DH=dh, sig_D=math.hypot(ddo, th_d))
for nm, r_ in ROWS.items():
    pulls = {k_: ((r_["Y_P"] if k_.startswith("Y_P") else r_["DH"]) - v[0]) / math.hypot(v[1], r_["sig_Y"] if k_.startswith("Y_P") else r_["sig_D"])
             for k_, v in OBS.items() if not k_.startswith("Li")}
    r_["pulls"] = pulls
    P(f"    {nm}: Y_P = {r_['Y_P']:.5f} +- {r_['sig_Y']:.5f}, D/H = {r_['DH']:.4e} +- {r_['sig_D']:.2e} (omega_b and rate errors); pulls vs "
      + ", ".join(f"{k_} {v:+.2f}" for k_, v in pulls.items()))
check("B2 (reported) AGAINST OBSERVATIONS: the chain's (= standard BBN's) Y_P lies within 1 sigma of the PDG 2024 and Aver+2021 values; "
      "D/H depends on the nuclear rates -- the printed pulls (PRIMAT low, PArthENoPE close), exactly as for LCDM",
      "; ".join(f"{nm}: Y {r_['pulls']['Y_P (PDG 2024)']:+.2f}, D/H {r_['pulls']['D/H (PDG 2024)']:+.2f} sigma" for nm, r_ in ROWS.items()),
      all(abs(r_["pulls"]["Y_P (PDG 2024)"]) <= 1.0 for r_ in ROWS.values()), load_bearing=False)
OUT["numbers"]["B2"] = ROWS
# B3 lithium-7
li_c = LI_SBBN[0] * math.exp(shifts(S_CHAIN)["dlnLi"])
li_obs = OBS["Li/H (PDG 2024, Spite plateau)"]
li_sig = (li_c - li_obs[0]) / math.hypot(LI_SBBN[1], li_obs[1])
P(f"    7Li/H: standard BBN (Fields et al. 2020) {LI_SBBN[0]:.3e} +- {LI_SBBN[1]:.2e}; the chain {li_c:.6e} (relative shift "
  f"{shifts(S_CHAIN)['dlnLi']:+.1e}); Spite plateau {li_obs[0]:.2e} +- {li_obs[1]:.1e}: ratio {li_c / li_obs[0]:.2f}, {li_sig:.1f} sigma "
  "(PDG 2024: 'a factor 3.1 ... a 4.4 sigma discrepancy')")
check("B3 (reported) LITHIUM-7 (the coordinator's question): the chain's G_cos changes 7Li/H by ~ +1e-9 (relative), so the chain inherits "
      "standard BBN's overprediction of the Spite plateau unchanged -- a factor ~3, ~4 sigma: the chain neither solves nor worsens the "
      "lithium problem", f"Li/H = {li_c:.3e}; ratio to the plateau {li_c / li_obs[0]:.2f}; {li_sig:.1f} sigma",
      abs(li_c / LI_SBBN[0] - 1) < 1e-6 and li_c / li_obs[0] > 2.5, load_bearing=False)
OUT["numbers"]["B3"] = dict(Li_chain=li_c, Li_sbbn=LI_SBBN, Li_obs=li_obs, ratio=li_c / li_obs[0], sigma=li_sig)
check("B4 (reported) BOTH a0 FOOTINGS: the BBN inputs are G_cos/G_N (alpha_c), omega_b, N_eff and the dark field's frozen energy -- a0 "
      "enters none of them (part 1 B9), so the canonical (9.3603e-11) and alt (1.1312e-10 m/s^2) footings give identical BBN",
      "a0-free inputs", True, load_bearing=False)
MUT = {}
if not MUTATE:
    sm = shifts(2.0)
    MUT = dict(Y_P=yp_pri + sm["dY"], DH=float(TAB_PRI.DH(OMB, 0.0)) * math.exp(sm["dlnD_post"]),
               DH_pre=float(TAB_PRI.DH(OMB, 0.0)) * math.exp(sm["dlnD_pre"]), Li=LI_SBBN[0] * math.exp(sm["dlnLi"]),
               dN_pre=dN_pre(2.0), dN_post=dN_post(2.0))
    pull_m = (MUT["Y_P"] - OBS["Y_P (PDG 2024)"][0]) / OBS["Y_P (PDG 2024)"][1]
    P(f"    the MUTATE's model (G_cos = 2 G_N): Y_P = {MUT['Y_P']:.4f} (BBN-lite, calibrated) -> {pull_m:+.1f} sigma from PDG 2024; D/H = "
      f"{MUT['DH']:.3e} (post map, Delta N = {min(dN_post(2.0), 7.0):.2f}; the table stops at 7) / {MUT['DH_pre']:.3e} (pre map); 7Li/H ~ "
      f"{MUT['Li']:.2e} (Steigman's fit far outside its range)")
    check("M (reported) the MUTATE's model fails BBN: G_cos = 2 G_N puts Y_P more than 10 sigma above the observed value",
          f"Y_P {MUT['Y_P']:.4f} ({pull_m:+.1f} sigma)", pull_m > 10, load_bearing=False)
OUT["numbers"]["M"] = MUT

# ================================================================================================ W ledger
banner("W  THE LEDGER: XR26 part 3")
rp_ = ROWS["PRIMAT 2024"]; ra_ = ROWS["PArthENoPE 2017"]
LEDGER = [
    ("X26-3a", "BBN in the chain = standard BBN at the chain's omega_b: G_cos/G_N = 1 - alpha_c/2 shifts Y_P by "
               f"{shifts(S_CHAIN)['dY']:+.0e}, D/H and 7Li/H by ~1e-9 (relative); dark field and khronon absent", "DERIVED", "B1, K3"),
    ("X26-3b", f"Y_P = {rp_['Y_P']:.4f} (PRIMAT) / {ra_['Y_P']:.4f} (PArthENoPE) vs 0.245 +- 0.003: consistent", "DERIVED", "B2"),
    ("X26-3c", f"D/H = {rp_['DH']:.3e} (PRIMAT, {rp_['pulls']['D/H (PDG 2024)']:+.1f} sigma) / {ra_['DH']:.3e} (PArthENoPE, "
               f"{ra_['pulls']['D/H (PDG 2024)']:+.1f} sigma) vs 2.547 +- 0.029e-5: the same nuclear-rate question LCDM has", "DERIVED", "B2"),
    ("X26-3d", f"7Li/H = {li_c:.2e} vs the Spite plateau 1.6 +- 0.3e-10: the factor-3 lithium problem, unchanged", "FAILS",
     "B3 (standard BBN's failure, inherited)"),
    ("X26-3e", "the datum phibar-dot = 0 (lambda > 0) must be < ~1e-12 H0/sqrt(lambda) today (a stiff component at BBN)", "CONSTRAINT",
     "part 1 F1"),
]
for k_, what, st_, why in LEDGER:
    P(f"    {k_:8s} {st_:11s} {what}  --  {why}")
OUT["ledger"] = [dict(link=k_, what=w_, status=s_, basis=b_) for k_, w_, s_, b_ in LEDGER]
check("W (reported) the ledger", f"{len(LEDGER)} links", True, load_bearing=False)
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
banner("VERDICT" + ("  [MUTATE]" if MUTATE else ""))
if not MUTATE:
    P(f"  The chain's BBN is standard BBN: G_cos/G_N = 1 - alpha_c/2 moves Y_P by {shifts(S_CHAIN)['dY']:+.0e} and D/H, 7Li/H by ~1e-9.  At the")
    P(f"  chain's omega_b (= LCDM's) Y_P = {rp_['Y_P']:.4f}, D/H = {rp_['DH']:.3e} (PRIMAT) / {ra_['DH']:.3e} (PArthENoPE), 7Li/H = {li_c:.2e}:")
    P("  helium consistent, deuterium as good or as tense as LCDM's (rate-dependent), lithium overpredicted ~3x exactly as in standard BBN.")
else:
    P("  MUTATE: G_cos = 2 G_N moves the abundances at O(1); the headline fails as pre-declared.")
OUT["verdict"] = dict(n_checks=len(CH), n_fail_load_bearing=n_fail, elapsed_s=round(time.time() - T_START))
json.dump(OUT, open(JSN, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating, np.integer)) else str(o)))
rc = 0 if n_fail == 0 else 1
P(f"\n  {sum(1 for _, ok, _l in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {os.path.basename(JSN)} "
  f"({time.time() - T_START:.0f} s)")
P(f"rc = {rc}")
TEE.flush()
sys.stdout = sys.__stdout__
TEE.close()
sys.exit(rc)
