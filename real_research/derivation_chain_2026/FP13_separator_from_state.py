#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FP13 -- THE SEPARATOR'S SCALES FROM THE ACTION'S OWN STATE: can the four DECLARED constants of FP9's separator (H_Y) --
L_Lambda, n, y_Lambda, p' -- be supplied by what the action's state already carries, so that each becomes derived or
eliminated instead of declared?  Every candidate is written as a term in the chain's action, scored with the chain's own
machinery on every gate, both a0 footings.

WHY.  FP9 (committed b510eebfe) put a separator on FP7's AQUAL-type root: a band-pass chi = (S_xi - S_L) phi with
L = L_Lambda Omega_L(<K>_h)^(n/2) and a yield floor J_Y = J_P2 + 2 y_th sqrt(Y) with y_th = y_Lambda Omega_L(<K>_h)^(-p').
It passes sigma_8, the forest proxy, the flagship, SPARC and KiDS with FOUR declared constants (L_Lambda = 2.46 Mpc, n = 2,
y_Lambda = 7.8e-8, p' = 4) inside the windows L(0.25) >~ 1.2 Mpc, y_th(0.25) <~ 3e-6, 4e-3 <~ y_th(2.5) <~ 0.03.  FP9 V1
proved that (a0, Lambda, G, c) build only Gpc lengths and that an Mpc scale needs a host mass, which a LOCAL term cannot
read.  FP10's dark field carries a declared mass m >= 1.9-5.2e-19 eV.  FP11: the MW-M31 timing works with baryons only,
R0 overshoots by +0.20 dex.  The user rejects added knobs; this lane attacks the knob count.

THE CANDIDATES (the coordinator's list), each a leaf-averaged functional of the state -- nonlocal like <K>_h already is:
  (a) L from the matter field's own nonlinearity: the heat branch's readout at diffusion time B = L^2/2 applied to the
      matter density, <(S_B delta_m)^2>_h = s^2 (the Gaussian-smoothed leaf-rms contrast equals a threshold s), with
      delta_m = D_i(a^i - D^i chi)/(4 pi G_N rho_bar) (the chassis's Newtonian combination, FP7 A1) or the dynamical
      delta_dyn = D_i a^i/(4 pi G_N rho_bar) (phantom included), 4 pi G rho_bar = <K>_h^2/6 - Lambda/2; natural s = 1
      (the nonlinear scale) and s = delta_c = (3/20)(12 pi)^(2/3) = 1.686 (spherical collapse, GR); the linear reading and
      the nonlinear one (halofit, Takahashi+2012); the leaf-averaged MOND-sector energy; the unsmoothed variance.
  (b) the dark field's own lengths at FP10's m: Compton, de Broglie, Jeans (cosmic and halo densities).
  (c) the exponents n and p' from Omega_L's time dependence plus a derived onset: the running of the state's scale (n);
      the running of every state measure against the yield's required 3.1 decades (p'); onsets -- the leaf's deceleration
      changing sign (q = 0), Omega_L = Omega_m, E_MOND = E_kin, the first y ~ 1 on the leaf.
  (d) y_th from the leaf-averaged field: the web's leaf-rms (raw or band-passed, linear or nonlinear), alone and switched.
THE RESULT'S SEPARATOR (H_S), the four constants replaced by state functionals (per 1/16 pi G, c = 1):
  chi = (S_xi - S_B) phi,   B[state] = L^2/2:  <(S_B delta_m)^2>_h = delta_c^2   (L = xi, band-pass closed, if no root)
  J_Y = J_P2(Y) + 2 y_th sqrt(Y),   y_th[state] = <|(S_xi - S_B)(a - D chi)|^2>_h^(1/2) (c^2/a0) x max(0, 2 q),
  2 q = 1 + Omega_r - 3 Omega_L(<K>_h)   (the leaf's deceleration; the yield vanishes once the leaf accelerates).
The footings: a0 = 9.3603e-11 (canonical) and 1.1312e-10 m/s^2 (alt), FP0.

CHECKS
  K  CONTROLS: K1 FP9's machinery (exec'd read-only up to its K banner) driven by THIS lane's general L(a)/y_th(a) model
     reproduces FP9's committed headline (sigma_8 x4, forest x12, flagship x4, SPARC, KiDS) and its LG R0; K2 this lane's
     halofit equals CLASS's halofit on CLASS's own linear spectrum; K3 the state machinery (sigma_8 normalisation, the
     linear growth against FP6's, the Gaussian variance by quadrature); K4 FP11's two-body machinery, hooked to an
     arbitrary L(a)/y_th(a), reproduces FP11's committed X1 point.
  S  THE CONSTANTS: S1 no length built from (a0, c, G, Lambda, hbar, m, xi) has an Mpc size at natural exponents AND the
     web's running (n_eff >= 2); S2 (reported) numerology controls with their look-elsewhere rates.
  A  CANDIDATE (a): A1 the state-length term is nonlocal (no local variation) and closes on exact FRW (h = 0), where FP7's
     lambda > 0 becomes necessary; A2 the scale and its running (n derived); A3 the threshold windows (FP9's yield and the
     state yield), delta_c and 1; A4 the self-consistent readouts: the dynamical one runs away (FAIL), the matter one is
     stable; A5 the other named measures set no web length; A6 (reported) the linear-spectrum systematic (CLASS vs EH98);
     A7 (reported) the nonlinear reading's dependence on the halos' dark mass (FP10's clearing).
  B  CANDIDATE (b): B1 the dark field's lengths at m >= floor: sub-kpc, wrong running, no coupling (FAIL).
  C  CANDIDATE (c): C1 no power law of a state measure gives the yield's running without a declared exponent AND
     normalisation (FAIL); C2 a sign-change onset (q = 0) needs neither, the alternatives fail or are reading-dependent.
  D  CANDIDATE (d): D1 the yield at the web's rms alone FAILS KiDS and SPARC; D2 switched at q = 0 it passes, with the
     window of its coefficient.
  H  THE HEADLINE (H_S): H1 every linchpin gate, both footings and modes, tolerance and grid; H2 E in the BPS window at
     every epoch; H3 the self-consistent matter feedback on the headline; H4 (reported) the prices; H5 (reported) variants.
  L  THE LOCAL GROUP (FP11's machinery): L1 the MW-M31 timing; L2 R0 at the timing mass (FAIL, verified); L3 (reported).
  F  the count against FP9 and LCDM.   W  the ledger.   G (reported) G-1 whole including the Local Group.
MUTATE=1 removes the onset switch from the headline yield (y_th = the web's band-passed rms at every epoch -- candidate (d)
alone in the headline's clothes): H1's KiDS and SPARC gates must FAIL (rc = 1).

SCOPE.  The chain's frozen-coefficient linear yardstick (L341/FP6/FP9: EH98, growing-mode ICs, rms and per-mode fields, the
tracking weight); the forest is FP6's LINEAR PROXY; KiDS is lead grade (isolated lenses, one lens redshift, 0.25; 0.4 and
0.7 reported); the LG is FP11's two-body law + XR4's shell model.  The nonlinear state is read through halofit (LCDM), not a
particle-mesh run of this theory.  No PM or N-body run; at most 2 worker processes.

Run from the repository root:  python3 real_research/derivation_chain_2026/FP13_separator_from_state.py
"""
import os, re, sys, io, json, math, time, contextlib, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
warnings.filterwarnings("ignore")
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import solve_ivp, quad

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "FP13_separator_from_state"
NPROC = 2
DELTA_C = 3.0 / 20.0 * (12.0 * math.pi) ** (2.0 / 3.0)        # 1.68647: spherical collapse (EdS, GR)
XI_FLOOR_MPC = 0.0243e-6                                      # FP7's filter floor xi (canonical) [Mpc]: the band-pass closes at L = xi
HBARC_EVM = 1.973269804e-7                                    # hbar c [eV m]
M_DARK = (1.9e-19, 5.2e-19)                                   # FP4 L10f / FP10: the dark field's mass floor [eV]
KAPPA, ZZ = 0.5, 2.0 * math.sqrt(8.0 * math.pi / 3.0)         # FP0: kappa = 1/2 (FITTED), Z = 5.7888
HEAD_S = DELTA_C                                              # the headline threshold
HEAD_READ = "NL"                                              # the headline reading of the state (the actual, nonlinear field)
HEAD_SWITCH = "none" if MUTATE else "ramp"                    # MUTATE: the yield at the web's rms at every epoch
HEAD_CY = 1.0                                                 # the yield's level = the web's band-passed leaf-rms, coefficient 1


# ================================================================================================= the chain's machinery (read-only)
_M = {}


def _exec_ro(path, cut_marker=None, name="machinery"):
    src = open(path).read()
    if cut_marker:
        src = src[:src.index(cut_marker)]
    ns = {"__file__": path, "__name__": name}
    old = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src, path, "exec"), ns)
    finally:
        if old is None:
            os.environ.pop("MUTATE", None)
        else:
            os.environ["MUTATE"] = old
    return ns


def mach9():
    """FP9's committed script exec'd read-only up to its K CONTROLS banner: FP6's machinery (EH98 growth yardstick, the forest
    proxy, the band-passed phantom, KiDS lead grade, the LG shell model) with FP9's yield law hooked into FP6's kernel slot."""
    if "ns9" not in _M:
        _M["ns9"] = _exec_ro(os.path.join(HERE, "FP9_web_galaxy_separator.py"),
                             "# ================================================================================================= K  CONTROLS",
                             "fp9_machinery")
    return _M["ns9"]


def fp11():
    """FP11's committed module exec'd read-only (its main() is not run): the MW-M31 two-body force table, the Hubble-flow shooter,
    the timing interpolation and the merged-pair zero-velocity radius."""
    if "ns11" not in _M:
        ns = _exec_ro(os.path.join(HERE, "FP11_local_group_flyby.py"), None, "fp11_machinery")
        ns["_L_orig"], ns["_y_orig"] = ns["L_of_a"], ns["yth_of_a"]
        _M["ns11"] = ns
    return _M["ns11"]


def hook11(ns, law):
    """point FP11's L_of_a / yth_of_a at a tabulated law (ln a, L_phys [Mpc], y_th [a0]); None restores FP9's."""
    if law is None:
        ns["L_of_a"], ns["yth_of_a"] = ns["_L_orig"], ns["_y_orig"]
        return
    lna, Lp, yt = (np.asarray(v, float) for v in law)
    lLp = np.log(np.maximum(Lp, 1e-300)); MPCm = ns["MPC"]
    ns["L_of_a"] = lambda a, bp=True, LL=None: (float(np.exp(np.interp(math.log(a), lna, lLp))) * MPCm if bp else None)
    ns["yth_of_a"] = lambda a, yl=True: (max(float(np.interp(math.log(a), lna, yt)), 0.0) if yl else None)


def job_lg(cfg):
    """worker: the first-approach relative velocity today at M_b under a law (FP11's force table + shooter, convention A)."""
    tag, foot, Mb, law = cfg; t = time.time(); ns = fp11(); hook11(ns, law)
    m1, m2 = ns["FMW"] * Mb * ns["MSUN"], (1 - ns["FMW"]) * Mb * ns["MSUN"]
    dg, ln_, T = ns["force_table"](m1, m2, ns["A0"][foot], True, True)
    br = [b for b in ns["branches"](ns["Acc"](dg, ln_, T, m1 + m2)) if b["k"] == 0 and b["vr"] < 0]
    return tag, foot, Mb, (br[0]["vr"] if br else float("nan")), time.time() - t


# ================================================================================================= the lane
def main():
    from multiprocessing import Pool
    T0 = time.time()
    CH = []
    OUT = {"lane": "FP13", "mutate": MUTATE, "root": "FP7's AQUAL-type root + FP9's separator forms", "checks": {}, "numbers": {}, "ledger": []}

    def P(*a):
        print(*a, flush=True)

    def banner(t):
        P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)

    def el():
        return f"[{time.time() - T0:.0f} s]"

    def check(name, measured, ok, load_bearing=True, reading=None):
        ok = bool(ok); CH.append((name, ok, load_bearing))
        OUT["checks"][name.split()[0]] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing, "name": name}
        P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
        if reading:
            P(f"         reading:  {reading}")
        return ok

    def js(d):
        return {str(k_): (js(v) if isinstance(v, dict) else v) for k_, v in d.items()}

    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: the onset switch is removed from the headline yield (y_th = the web's band-passed rms at every epoch) -- "
          "H1's KiDS and SPARC gates must FAIL ***")

    # --------------------------------------------------------------------------------------------- names from the machinery
    ns9 = mach9(); M6 = ns9["M6"]
    A0 = dict(ns9["A0"]); A06 = dict(M6["A0"]); FOOTS, MODES = ns9["FOOTS"], ns9["MODES"]
    h, Om, OL, Or = M6["h"], M6["Om"], M6["OL"], M6["Or"]
    OmL_a, OmL_z, Ez, dlnH, A_I = M6["OmL_a"], M6["OmL_z"], M6["Ez"], M6["dlnH"], M6["A_I"]
    c, Mpc, G, rho_crit0, H0, MSUN = M6["c"], M6["Mpc"], M6["G"], M6["rho_crit0"], M6["H0"], M6["MSUN"]
    G6, MPCm = M6["G6"], M6["MPCm"]
    Delta_lin0 = M6["Delta_lin0"]
    s8_aq, forest_aq, growth_aq = ns9["s8_aq"], ns9["forest_aq"], ns9["growth_aq"]
    law_dev_dex, kids_class, phantom, x_P2 = ns9["law_dev_dex"], ns9["kids_class"], ns9["phantom"], ns9["x_P2"]
    YIELD, cutfac, nu_p2, gfield = ns9["YIELD"], M6["cutfac"], M6["nu_p2"], M6["gfield"]
    KH, KHF, DI, DIF = M6["KH"], M6["KHF"], M6["DI"], M6["DIF"]
    sigma8_of, S8_LCDM, forest_proxy, C2W = M6["sigma8_of"], M6["S8_LCDM"], M6["forest_proxy"], M6["C2W"]
    SIG8_BAND, SIG8_TIGHT, FOREST_TOL = M6["SIG8_BAND"], M6["SIG8_TIGHT"], M6["FOREST_TOL"]
    FLAG_TOL, SPARC_TOL, KIDS_TOL, LG_EDGE = M6["FLAG_TOL"], M6["SPARC_TOL"], M6["KIDS_TOL"], M6["LG_EDGE"]
    Z_KIDS, Z_FLAG = M6["Z_KIDS"], M6["Z_FLAG"]
    F9 = json.load(open(os.path.join(HERE, "FP9_web_galaxy_separator_results.json")))["numbers"]
    F11 = json.load(open(os.path.join(HERE, "FP11_local_group_flyby_results.json")))["numbers"]
    P(f"\n  machinery: FP9 exec'd read-only up to its K banner (FP6 inside, FP9's yield hook); footings a0 = {A0['canonical']:.4e} / "
      f"{A0['alt']:.4e} m/s^2; gates sigma_8 in {SIG8_BAND} (1.02 reported), forest proxy <= {FOREST_TOL}, flagship <= {FLAG_TOL} dex, "
      f"SPARC <= {SPARC_TOL} dex, KiDS d chi^2 <= +{KIDS_TOL}; LG 0.96 +- 0.03 Mpc (edge {LG_EDGE:.2f})")

    # --------------------------------------------------------------------------------------------- the state: linear (EH98) and nonlinear (halofit)
    _sD = solve_ivp(lambda N_, Y: [Y[1], 1.5 * (Om / math.exp(3 * N_) / Ez(math.exp(N_)) ** 2) * Y[0] - (2 + dlnH(math.exp(N_))) * Y[1]],
                    (math.log(A_I), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-10, atol=1e-14, dense_output=True)
    _D1 = _sD.sol(0.0)[0]

    def Dl(a):
        return float(_sD.sol(math.log(a))[0] / _D1)

    LKF = np.linspace(math.log(1e-4), math.log(1000.0), 5000); KKF = np.exp(LKF)
    D2L0 = np.array([Delta_lin0(k) for k in KKF]) ** 2
    RMIN = 1e-5                                                                   # Mpc/h: the whole grid (exp(-(1e3 x 1e-5)^2) = 1)

    def sig2(R, D2):
        return float(np.trapz(D2 * np.exp(-(KKF * R) ** 2), LKF))

    def Om_a(a):
        return Om / a ** 3 / (Om / a ** 3 + OL + Or / a ** 4)

    def halofit(D2lin, a, Omx=None, split=False):
        """Takahashi et al. 2012 (flat, w = -1): Delta^2_NL from Delta^2_lin on the fine grid (checked against CLASS in K2)."""
        Oma = Om_a(a) if Omx is None else Omx / a ** 3 / (Omx / a ** 3 + 1.0 - Omx)
        Rs = brentq(lambda R: sig2(R, D2lin) - 1.0, RMIN, 100.0); ks = 1.0 / Rs; e = 1e-3
        l0, lp, lm = (math.log(sig2(Rs * math.exp(x), D2lin)) for x in (0.0, e, -e))
        n = -3.0 - (lp - lm) / (2 * e); C = -(lp - 2 * l0 + lm) / e ** 2
        an = 10 ** (1.5222 + 2.8553 * n + 2.3706 * n ** 2 + 0.9903 * n ** 3 + 0.2250 * n ** 4 - 0.6038 * C)
        bn = 10 ** (-0.5642 + 0.5864 * n + 0.5716 * n ** 2 - 1.5474 * C)
        cn = 10 ** (0.3698 + 2.0404 * n + 0.8161 * n ** 2 + 0.5869 * C)
        gn = 0.1971 - 0.0843 * n + 0.8460 * C
        al = abs(6.0835 + 1.3373 * n - 0.1959 * n ** 2 - 5.5274 * C)
        be = 2.0379 - 0.7354 * n + 0.3157 * n ** 2 + 1.2490 * n ** 3 + 0.3980 * n ** 4 - 0.1682 * C
        nun = 10 ** (5.2105 + 3.6902 * n)
        f1, f2, f3 = Oma ** -0.0307, Oma ** -0.0585, Oma ** 0.0743
        y = KKF / ks
        DQ = D2lin * ((1 + D2lin) ** be / (1 + al * D2lin)) * np.exp(-(y / 4 + y ** 2 / 8))
        DH = an * y ** (3 * f1) / (1 + bn * y ** f2 + (cn * f3 * y) ** (3 - gn)) / (1 + nun * y ** -2)
        if split:
            return DQ, DH
        return DQ + DH, dict(ks=ks, n=n, C=C)

    LNA = np.linspace(math.log(1e-3), 0.0, 300); AGR = np.exp(LNA)
    DLA = np.array([Dl(a) for a in AGR])
    D2LIN = [D2L0 * d ** 2 for d in DLA]
    D2NL = [(halofit(D2LIN[i], AGR[i])[0] if sig2(RMIN, D2LIN[i]) > 1.0 else D2LIN[i]) for i in range(len(LNA))]
    STATE = {"lin": D2LIN, "NL": D2NL}

    def L_table(s, reading):
        out = np.empty(len(LNA))
        for i, a in enumerate(AGR):
            D2 = STATE[reading][i]
            out[i] = XI_FLOOR_MPC if sig2(RMIN, D2) < s * s else brentq(lambda R: sig2(R, D2) - s * s, RMIN, 300.0) / h * a
        return out

    def fun_of(tab, log=True):
        tab = np.asarray(tab, float)
        if log:
            lt = np.log(np.maximum(tab, 1e-300))
            return lambda a: float(np.exp(np.interp(math.log(a), LNA, lt)))
        return lambda a: float(np.interp(math.log(a), LNA, tab))

    def gbp_rms_phys(i, Lphys, reading, bp=True):
        """the leaf-rms of the (band-passed) Newtonian field at epoch i [m/s^2], sqrt(Int g_k^2 dln k) (the TRUE rms)."""
        a = AGR[i]; D2 = STATE[reading][i]
        g = 4 * math.pi * G * Om * rho_crit0 / a ** 3 * np.sqrt(D2) / (KKF * h / (a * Mpc))
        if bp:
            g = g * (1.0 - np.exp(-0.5 * (KKF * h * Lphys / a) ** 2))
        return math.sqrt(float(np.trapz(g ** 2, LKF)))

    def two_q(a):
        E2 = Om / a ** 3 + OL + Or / a ** 4
        return 1.0 + (Or / a ** 4) / E2 - 3.0 * OL / E2

    Z_Q0 = brentq(lambda z: two_q(1 / (1 + z)), 0.1, 2.0)
    Z_EQ = brentq(lambda z: OmL_z(z) - (1 - OmL_z(z)), 0.05, 1.0)

    SWITCH = {"none": lambda a: 1.0, "ramp": lambda a: max(0.0, two_q(a)), "step": lambda a: 1.0 if two_q(a) > 0 else 0.0,
              "eq": lambda a: 1.0 if OmL_a(a) < 1 - OmL_a(a) else 0.0}

    def yth_state(Ltab, reading, switch="ramp", cy=1.0, onset=None):
        """the state yield per footing: y_th(a) = c_y <|g_bp|^2>_h^(1/2)/a0 x switch(a) (onset: a custom switch function)."""
        sw = onset if onset is not None else SWITCH[switch]
        rms = np.array([gbp_rms_phys(i, Ltab[i], reading) for i in range(len(LNA))])
        tabs = {f: np.array([cy * rms[i] / A0[f] * sw(AGR[i]) for i in range(len(LNA))]) for f in FOOTS}
        return {f: fun_of(tabs[f], log=False) for f in FOOTS}, tabs, rms

    # --------------------------------------------------------------------------------------------- the general separator model + gates
    KB = {f: kids_class(A0[f]) for f in FOOTS}

    def model_of(Lf, yf):
        return {"hfac": lambda a, k: 1.0 - np.exp(-0.5 * (k * h * Lf(a) / a) ** 2),
                "cut": lambda y, a: cutfac(y, yf(a), YIELD), "yr": 0.0}

    def gates(Lf, yfd, extra=False, a0d=None):
        a0d = A0 if a0d is None else a0d
        r = {"s8": {}, "forest": {}, "flag": {}, "sparc": {}, "kids": {}}
        for f in FOOTS:
            mod = model_of(Lf, yfd[f])
            for m in MODES:
                r["s8"][(f, m)] = s8_aq(mod, f, m)
                r["forest"][(f, m)] = forest_aq(mod, f, m)
            for Mv in (1e10, 1e11):
                r["flag"][(f, Mv)] = law_dev_dex(Mv, a0d[f], 0.1, Lf(1 / (1 + Z_FLAG)), yfd[f](1 / (1 + Z_FLAG)), YIELD)
            r["sparc"][f] = max(abs(law_dev_dex(Mv, a0d[f], yv, Lf(1.0), yfd[f](1.0), YIELD)) for Mv in (1e9, 1e10, 1e11, 1e12)
                                for yv in (0.01, 0.03, 0.1, 1.0, 10.0, 100.0))
            r["kids"][f] = kids_class(a0d[f], Lf(1 / (1 + Z_KIDS)), yfd[f](1 / (1 + Z_KIDS)), YIELD) - KB[f]
            if extra:
                for zz in (0.4, 0.7):
                    r.setdefault(f"kids@{zz}", {})[f] = kids_class(a0d[f], Lf(1 / (1 + zz)), yfd[f](1 / (1 + zz)), YIELD) - KB[f]
                for yv in (0.1, 0.03, 0.01):
                    r.setdefault("z1gal", {})[(f, yv)] = law_dev_dex(1e11, a0d[f], yv, Lf(0.5), yfd[f](0.5), YIELD)
        ok = {"sigma_8": all(SIG8_BAND[0] <= v <= SIG8_BAND[1] for v in r["s8"].values()),
              "forest": max(r["forest"].values()) <= FOREST_TOL, "flagship": max(abs(v) for v in r["flag"].values()) <= FLAG_TOL,
              "SPARC": max(r["sparc"].values()) <= SPARC_TOL, "KiDS": max(r["kids"].values()) <= KIDS_TOL}
        r["ok"] = ok; r["all"] = all(ok.values()); r["s8_tight"] = max(r["s8"].values()) <= SIG8_TIGHT
        return r

    def gline(r):
        s = (f"s8 {min(r['s8'].values()):.4f}-{max(r['s8'].values()):.4f}, forest {max(r['forest'].values()):.2g}, flagship "
             f"{min(r['flag'].values()):+.4f}..{max(r['flag'].values()):+.4f} dex, SPARC {max(r['sparc'].values()):.1e}, KiDS "
             f"{min(r['kids'].values()):+.1f}..{max(r['kids'].values()):+.1f}")
        if "kids@0.4" in r:
            s += f" | KiDS@0.4 {max(r['kids@0.4'].values()):+.1f}, @0.7 {max(r['kids@0.7'].values()):+.1f}"
        return s + ("  ALL PASS" if r["all"] else "  fails: " + ",".join(k_ for k_, v in r["ok"].items() if not v))

    def lg_custom(Lf, yf, Mb_msun=None, a0d=None):
        """FP6's lg_both with an arbitrary L(a) [Mpc] and y_th(a) (both footings; merged point mass)."""
        a0d = A0 if a0d is None else a0d
        lg_R0, LNA_T, RG = M6["lg_R0"], M6["LNA_T"], M6["RG"]
        Mb = (M6["LG_MB"] if Mb_msun is None else Mb_msun) * M6["LG_Msun"]
        tabs = {f: [] for f in FOOTS}
        for la in LNA_T:
            a = math.exp(la); Lm = Lf(a) * MPCm
            for f in FOOTS:
                yt = yf[f](a) if isinstance(yf, dict) else yf(a)
                tabs[f].append(Mb + phantom(Mb, a0d[f], Lm, yt if yt > 0 else None, YIELD if yt > 0 else 4))
        lnR = np.log(RG); out = {}
        for f in FOOTS:
            tab = np.array(tabs[f])

            def Menc(r, a, tab=tab):
                x = math.log(a); j = min(max(np.searchsorted(LNA_T, x) - 1, 0), len(LNA_T) - 2)
                fr_ = (x - LNA_T[j]) / (LNA_T[j + 1] - LNA_T[j])
                return np.interp(np.log(np.maximum(r, RG[0])), lnR, (1 - fr_) * tab[j] + fr_ * tab[j + 1])
            out[f] = lg_R0(Menc)
        return out

    # ============================================================================================= K  CONTROLS
    banner("K  CONTROLS: the reused machinery reproduces the record; the halofit, the state, FP11's hook")
    LL9 = ns9["LL_of"](1.3, 2.0)
    L9 = lambda a: LL9 * OmL_a(a)
    y9 = lambda a: 1e-6 * (OmL_z(Z_KIDS) / OmL_a(a)) ** 4.0
    y9d = {f: y9 for f in FOOTS}
    k1 = {"s8": {}, "forest": {}, "flag": {}, "sparc": {}, "kids": {}}
    for f in FOOTS:
        mod = model_of(L9, y9)
        for m in MODES:
            k1["s8"][(f, m)] = s8_aq(mod, f, m)
            res_ = growth_aq(mod, A0[f], mode=m, KHg=KHF, Dig=DIF, zs_out=(2.0, 3.0))
            for kF in (10.0, 15.0, 20.0):
                k1["forest"][(f, m, kF)] = forest_proxy(res_, kF=kF)[0]
        for Mv in (1e10, 1e11):
            k1["flag"][(f, Mv)] = law_dev_dex(Mv, A0[f], 0.1, L9(1 / 3.5), y9(1 / 3.5), YIELD)
        k1["sparc"][f] = max(abs(law_dev_dex(Mv, A0[f], yv, L9(1.0), y9(1.0), YIELD)) for Mv in (1e9, 1e10, 1e11, 1e12) for yv in (0.01, 0.03, 0.1, 1.0, 10.0, 100.0))
        k1["kids"][f] = kids_class(A0[f], L9(0.8), y9(0.8), YIELD) - KB[f]
    LGO = M6["LG_OmL"]
    L9LG = lambda a: LL9 * LGO(a)                                                 # FP6's lg_both: the LG cosmology's Omega_L(a)
    y9LG = lambda a: 1e-6 * (LGO(1 / 1.25) / LGO(a)) ** 4.0
    k1["lg"] = lg_custom(L9LG, y9LG, a0d=A06)
    ref = F9["H2"]
    devs = ([abs(k1["s8"][k_] / ref["s8"][str(k_)] - 1) for k_ in k1["s8"]]
            + [abs(k1["forest"][k_] - ref["forest"][str(k_)]) for k_ in k1["forest"]]
            + [abs(k1["flag"][k_] / ref["flag"][str(k_)] - 1) for k_ in k1["flag"]]
            + [abs(k1["sparc"][f] / ref["sparc"][f] - 1) for f in FOOTS] + [abs(k1["kids"][f] - ref["kids"][f]) for f in FOOTS]
            + [abs(k1["lg"][f] / F9["H3"]["2.0_1.3"][f] - 1) for f in FOOTS])
    P(f"    FP9's L(a) = {LL9:.4f} Omega_L(a) Mpc and y_th = 1e-6 (Omega_L(0.25)/Omega_L)^4 through this lane's model: sigma_8 "
      + ", ".join(f"{k_[0][:3]}/{k_[1]} {v:.5f}" for k_, v in k1["s8"].items()) + f"; KiDS {k1['kids']['canonical']:+.3f}/{k1['kids']['alt']:+.3f}; "
      f"LG {k1['lg']['canonical']:.4f}/{k1['lg']['alt']:.4f} Mpc (FP6's footing digits)")
    check("K1 CONTROL: FP9's committed machinery, exec'd read-only and driven by THIS lane's general separator model (any L(a), any "
          "y_th(a)), reproduces FP9's committed (H_Y) headline -- sigma_8 (both footings, both modes), the forest proxy (k_F = 10, 15, "
          "20), the 1e10/1e11 flagships, SPARC, KiDS -- and its Local-Group R0",
          f"max deviation {max(devs):.1e} (relative; forest and KiDS absolute)", max(devs) < 1e-6)
    OUT["numbers"]["K1"] = {"max_dev": max(devs)}

    # K2 halofit vs CLASS
    k2 = {}; k2_ok = False; CLS = None
    try:
        from classy import Class
        CLS = Class()
        CLS.set({"h": h, "omega_b": M6["om_b"], "omega_cdm": M6["om_c"], "n_s": M6["ns"], "sigma8": M6["SIG8"], "T_cmb": M6["T_CMB"],
                 "N_ur": M6["N_eff"], "output": "mPk", "P_k_max_h/Mpc": 200, "z_max_pk": 3.0, "non linear": "halofit"})
        CLS.compute()
        OmC = CLS.Omega_m(); kin = KKF <= 150.0; sel = (KKF >= 0.05) & (KKF <= 20.0)
        for z in (0.0, 0.25, 1.0, 2.5):
            PL = np.array([CLS.pk_lin(k * h, z) for k in KKF[kin]]) * h ** 3
            D2c = np.zeros_like(KKF); D2c[kin] = KKF[kin] ** 3 * PL / (2 * math.pi ** 2)
            PN = np.array([CLS.pk(k * h, z) for k in KKF[sel]]) * h ** 3
            D2n = halofit(D2c, 1 / (1 + z), OmC)[0]
            ratio = D2n[sel] / (KKF[sel] ** 3 * PN / (2 * math.pi ** 2))
            k2[z] = (float(ratio.min()), float(ratio.max()))
        k2_ok = all(abs(v[0] - 1) < 3e-3 and abs(v[1] - 1) < 3e-3 for v in k2.values())
    except Exception as ex:                                                     # CLASS unavailable: the control cannot pass
        k2["error"] = repr(ex)
    P("    this lane's halofit / CLASS halofit on CLASS's own linear spectrum, 0.05-20 h/Mpc: "
      + ", ".join(f"z = {z}: {v[0]:.4f}-{v[1]:.4f}" for z, v in k2.items() if z != "error") + (f" ({k2['error']})" if "error" in k2 else ""))
    check("K2 CONTROL: this lane's halofit (Takahashi et al. 2012) applied to CLASS's own linear spectrum equals CLASS's halofit P_NL at "
          "z = 0, 0.25, 1, 2.5 over 0.05-20 h/Mpc -- the nonlinear reading of the state is the literature's",
          ", ".join(f"z={z}: [{v[0]:.4f}, {v[1]:.4f}]" for z, v in k2.items() if z != "error") or k2.get("error"), k2_ok)
    OUT["numbers"]["K2"] = js(k2)

    # K3 the state machinery
    W8f = np.array([3 * (math.sin(8 * k) - 8 * k * math.cos(8 * k)) / (8 * k) ** 3 for k in KKF]) ** 2
    s8_fine = math.sqrt(float(np.trapz(D2L0 * W8f, LKF)))
    D_ctrl = abs(Dl(A_I) * M6["_r0"] - 1.0)
    sg_q = math.sqrt(quad(lambda lk_: Delta_lin0(math.exp(lk_)) ** 2 * math.exp(-(math.exp(lk_) * 1.0) ** 2), math.log(1e-4), math.log(50.0), limit=400)[0])
    sg_t = math.sqrt(sig2(1.0, D2L0))
    check("K3 CONTROL: the state machinery -- the fine-grid EH98 spectrum's top-hat sigma_8 equals FP6's normalisation 0.811, the "
          "linear growth D(a) equals FP6's (_r0), and the Gaussian (heat-kernel) variance by trapezoid equals quadrature",
          f"sigma_8 {s8_fine:.5f}; |D(a_i) r0 - 1| {D_ctrl:.1e}; sigma_G(1 Mpc/h) trapz {sg_t:.5f} vs quad {sg_q:.5f}",
          abs(s8_fine / M6["SIG8"] - 1) < 2e-3 and D_ctrl < 1e-6 and abs(sg_t / sg_q - 1) < 1e-4)
    P(f"    {el()}")

    # ============================================================================================= S  THE CONSTANTS
    banner("S  THE CONSTANTS: which lengths the action's constants can build, and whether any has the web's size AND running")
    import sympy as sp
    ea, ec, eG, eH, eh, em = sp.symbols("e_a e_c e_G e_H e_hbar e_m")
    # dims (M, L, T): a0 (0,1,-2), c (0,1,-1), G (-1,3,-2), H_Lambda (0,0,-1), hbar (1,2,-1), m (1,0,0); target a length (0,1,0)
    sol = sp.solve([-eG + eh + em, ea + ec + 3 * eG + 2 * eh - 1, -2 * ea - ec - 2 * eG - eH - eh], [ec, eG, eH], dict=True)[0]
    H_L = H0 * math.sqrt(OL); LH = c / H_L / Mpc                                    # c/H_Lambda [Mpc]
    lamC = {m: HBARC_EVM / m / Mpc for m in M_DARK}                                 # Compton hbar/(m c) [Mpc]
    rhoL = OL * rho_crit0

    def jeans_phys(m_eV, rho):                                                      # 2 pi / k_J, k_J^4 = 16 pi G rho (m/hbar)^2
        hbar_over_m = HBARC_EVM * c / m_eV                                          # [m^2/s]
        return 2 * math.pi / ((16 * math.pi * G * rho) ** 0.25 / math.sqrt(hbar_over_m)) / Mpc
    p_hit = {m: math.log(1.0 / LH) / math.log(lamC[m] / LH) for m in M_DARK}         # (c/H)^(1-p) lambda_C^p = 1 Mpc
    p_xi = math.log(1.0 / LH) / math.log(XI_FLOOR_MPC / LH)
    a_Z = math.log((1.3 / OmL_z(0.25)) * (H_L ** 2) * Mpc / A0["canonical"]) / math.log(ZZ)   # FP9's n = 2 form a_L/H^2: a_L = a0 Z^a
    Lwin = (1.2 / OmL_z(0.25), 1.6 / OmL_z(0.25))                                # L_Lambda's window at n = 2 (FP9 H4)
    fam = {}
    for X, nm in ((ZZ, "Z"), (KAPPA, "kappa")):
        fam[f"(c/H) {nm}^k  [n_eff = 0 or 1]"] = [(k, LH * X ** k) for k in range(-40, 41) if 1e-3 < LH * X ** k < 1e3]
        fam[f"a0 {nm}^k/H^2 [n_eff = 2]"] = [(k, A0["canonical"] * X ** k / H_L ** 2 / Mpc) for k in range(-40, 41) if 1e-3 < A0["canonical"] * X ** k / H_L ** 2 / Mpc < 1e3]
    hits = {k_: [(k, round(v, 3)) for k, v in vs if Lwin[0] <= v <= Lwin[1]] for k_, vs in fam.items()}
    n2_hits = [v for k_, v in hits.items() if "n_eff = 2" in k_ and v]
    # the one natural hit with the wrong running: score kappa^11 c/H_Lambda as n = 0 (constant) and n = 1 (c/H(z))
    Lk11 = LH * KAPPA ** 11
    s1g = {nn: gates(lambda a, nn=nn: Lk11 * OmL_a(a) ** (nn / 2.0), y9d) for nn in (0.0, 1.0)}
    P(f"    length monomials of (a0, c, G, H_Lambda, hbar, m): exponents {sol} (free: e_a, e_hbar, e_m) -- c/H_Lambda times powers of "
      f"a0/(c H_Lambda) and of the dark-mass groups")
    P(f"    c/H_Lambda = {LH:.0f} Mpc; Compton hbar/(mc) = {lamC[M_DARK[0]] * 1e6:.2e} / {lamC[M_DARK[1]] * 1e6:.2e} pc (m = 1.9e-19 / 5.2e-19 eV); "
      f"Jeans at rho_Lambda {1e3 * jeans_phys(M_DARK[0], rhoL):.2f} kpc; xi = {XI_FLOOR_MPC * 1e6:.4f} pc")
    P(f"    Mpc from the dark mass or xi only at NON-natural exponents: (c/H_Lambda)^(1-p) (hbar/mc)^p = 1 Mpc at p = {p_hit[M_DARK[0]]:.3f} / "
      f"{p_hit[M_DARK[1]]:.3f}, (c/H_Lambda)^(1-p) xi^p at p = {p_xi:.3f} (running n_eff = 1 - p with c/H(z): {1 - p_hit[M_DARK[0]]:.2f} / {1 - p_xi:.2f})")
    P(f"    L_Lambda window [{Lwin[0]:.2f}, {Lwin[1]:.2f}] Mpc; integer-power hits: {hits}; FP9's a_L = H_Lambda^2 L_Lambda = a0 Z^{a_Z:.2f}")
    P("    the natural hit kappa^11 c/H_Lambda = " + f"{Lk11:.2f} Mpc scored with its own running: n = 0 (constant): {gline(s1g[0.0])}; n = 1 (c/H(z)): {gline(s1g[1.0])}")
    s1_ok = (not n2_hits) and (1 - p_hit[M_DARK[0]]) < 2 and (1 - p_xi) < 2 and abs(a_Z - round(a_Z)) > 0.2 and not s1g[0.0]["ok"]["sigma_8"] and not s1g[1.0]["ok"]["sigma_8"]
    check("S1 THE CONSTANTS BUILD NO WEB LENGTH: every length from (a0, c, G, Lambda, hbar, m) [+ the filter floor xi] is c/H_Lambda "
          "times powers of dimensionless groups; the one family that runs like the web (a_L/H^2, n_eff = 2) misses L_Lambda's window at "
          "every integer power of Z and kappa (FP9 needs a_L = a0 Z^-3.38); the families that hit it (kappa^11 c/H_Lambda) or reach an "
          "Mpc through the dark mass or xi (non-natural powers) run with n_eff <= 1 and FAIL sigma_8 when scored -- the separator's Mpc "
          "scale cannot come from the constants",
          f"n = 2 hits {n2_hits or 'none'}; kappa^11 c/H_Lambda = {Lk11:.2f} Mpc: sigma_8 max n=0 {max(s1g[0.0]['s8'].values()):.2f}, n=1 "
          f"{max(s1g[1.0]['s8'].values()):.2f}; p(m floor) = {p_hit[M_DARK[0]]:.3f}; p(xi) = {p_xi:.3f}; a_L = a0 Z^{a_Z:.2f}", s1_ok)
    OUT["numbers"]["S1"] = {"LH_Mpc": LH, "p_hit": {str(k_): v for k_, v in p_hit.items()}, "p_xi": p_xi, "a_Z": a_Z, "hits": hits,
                            "kappa11_s8": {str(nn): js(g_["s8"]) for nn, g_ in s1g.items()}}

    # S2 numerology controls (look-elsewhere)
    ywin = (3e-7 * OmL_z(0.25) ** 4, 3e-6 * OmL_z(0.25) ** 4)                    # y_Lambda window at p' = 4 (FP9 H1)
    Lhits = {"kappa": [k for k in range(0, 30) if Lwin[0] <= LH * KAPPA ** k <= Lwin[1]],
             "Z": [k for k in range(0, 12) if Lwin[0] <= LH * ZZ ** -k <= Lwin[1]]}
    yhits = {"kappa": [k for k in range(0, 40) if ywin[0] <= KAPPA ** k <= ywin[1]], "Z": [k for k in range(0, 20) if ywin[0] <= ZZ ** -k <= ywin[1]]}
    chance = {"L_Lambda/kappa": math.log10(Lwin[1] / Lwin[0]) / math.log10(2), "L_Lambda/Z": math.log10(Lwin[1] / Lwin[0]) / math.log10(ZZ),
              "y_Lambda/kappa": min(1.0, math.log10(ywin[1] / ywin[0]) / math.log10(2)), "y_Lambda/Z": min(1.0, math.log10(ywin[1] / ywin[0]) / math.log10(ZZ))}
    check("S2 (reported) NUMEROLOGY CONTROLS: integer powers of kappa and Z that land in FP9's windows -- L_Lambda = kappa^k c/H_Lambda, "
          "y_Lambda = kappa^k or Z^-k -- with the chance that SOME integer power lands in a window that wide: a hit is not a derivation",
          f"L_Lambda window {Lwin[0]:.2f}-{Lwin[1]:.2f} Mpc: kappa^{Lhits['kappa']} (c/H_Lambda kappa^11 = {LH * KAPPA ** 11:.2f} Mpc), Z^-{Lhits['Z']}; "
          f"y_Lambda window {ywin[0]:.1e}-{ywin[1]:.1e}: kappa^{yhits['kappa']}, Z^-{yhits['Z']}; chance "
          + ", ".join(f"{k_} {v:.0%}" for k_, v in chance.items()), True, load_bearing=False)
    OUT["numbers"]["S2"] = {"Lwin": Lwin, "ywin": ywin, "Lhits": Lhits, "yhits": yhits, "chance": chance}
    P(f"    {el()}")

    # ============================================================================================= A  CANDIDATE (a)
    banner("A  CANDIDATE (a): the band-pass length from the matter field's own nonlinear scale, <(S_B delta_m)^2>_h = s^2")
    # A1 nonlocality and FRW
    rng = np.random.default_rng(13); nl_scal = {}
    for Ng in (8, 16, 32):
        kx = 2 * math.pi * np.fft.fftfreq(Ng); K2g = kx[:, None, None] ** 2 + kx[None, :, None] ** 2 + kx[None, None, :] ** 2
        dg = rng.standard_normal((Ng, Ng, Ng)); Bd = 2.0
        Sd = np.real(np.fft.ifftn(np.exp(-Bd * K2g) * np.fft.fftn(dg)))
        grad = 2.0 / Ng ** 3 * np.real(np.fft.ifftn(np.exp(-2 * Bd * K2g) * np.fft.fftn(dg)))   # d<(S delta)^2>/d delta_j (S symmetric)
        eps_ = 1e-6; j0 = (1, 2, 3); dg2 = dg.copy(); dg2[j0] += eps_
        Sd2 = np.real(np.fft.ifftn(np.exp(-Bd * K2g) * np.fft.fftn(dg2)))
        fd = (np.mean(Sd2 ** 2) - np.mean(Sd ** 2)) / eps_
        nl_scal[Ng] = (float(np.sqrt(np.mean(grad ** 2))) * Ng ** 3, abs(fd / grad[j0] - 1))
    frw_closed = sig2(RMIN, np.zeros_like(D2L0)) < HEAD_S ** 2                     # sigma = 0 at every R on exact FRW -> L = xi
    lam_, al_, c2_, hh_, Cp_, kk_, ww_ = sp.symbols("lambda alpha_c c_2 h C_phi k omega", real=True)
    det9 = sp.sympify(re.sub(r"\blambda\b", "lam_", F9["K2"]["det"]), locals={"lam_": lam_, "alpha_c": al_, "c_2": c2_, "h": hh_, "C_phi": Cp_, "k": kk_, "omega": ww_})
    det_h0 = sp.factor(det9.subs({Cp_: 0, hh_: 0}))
    det_h0_l0 = sp.simplify(det_h0.subs(lam_, 0))
    root2_h0 = sp.simplify(sp.sympify(re.sub(r"\blambda\b", "lam_", F9["A2"]["roots"][1]), locals={"lam_": lam_, "alpha_c": al_, "c_2": c2_, "h": hh_}).subs(hh_, 0))
    r2num = [float(root2_h0.subs({al_: av, c2_: 7.29e-3, lam_: 1.0})) for av in (9.62e-14, 3.2e-9)]
    P(f"    leaf-average gradient: rms_j |d sigma^2/d delta_j| x N^3 = " + ", ".join(f"N = {k_}: {v[0]:.2f} (FD check {v[1]:.1e})" for k_, v in nl_scal.items())
      + " -> the functional derivative is O(1/V)")
    P(f"    exact FRW: sigma(R) = 0 at every R -> B = b (L = xi): h = 0; FP9's committed zero-field block at h = 0: det = {det_h0}; at lambda = 0: {det_h0_l0}; "
      f"the non-zero root at h = 0: omega^2/k^2 = {root2_h0} (= {r2num[0]:.2e} / {r2num[1]:.2e} at the alpha_c ends, c_2 = 7.29e-3)")
    a1_ok = (all(abs(nl_scal[k_][0] / nl_scal[8][0] - 1) < 0.2 for k_ in nl_scal) and all(v[1] < 1e-3 for v in nl_scal.values())
             and frw_closed and det_h0_l0 == 0 and all(v > 0 for v in r2num))
    check("A1 THE STATE-LENGTH TERM IS NONLOCAL AND CLOSES ON FRW: B[state] is fixed by a leaf average, whose derivative with respect "
          "to any local field is O(1/V) (checked on periodic leaves N = 8-32, finite differences) -- it adds no local term to the "
          "field equations and FP3's local-gate lemma does not apply; on exact FRW sigma = 0 at every R, so L = xi and the band-pass "
          "closes (h = 0): FP9's committed zero-field block then has roots omega^2 = 0 and (2 - alpha_c) c_2/(alpha_c (2 + 3 c_2)) k^2 "
          "> 0 (lambda-free), but its determinant is proportional to lambda -- with the band-pass closed AND the state yield zero (the "
          "rms vanishes on FRW) phi has no equation at lambda = 0: FP7's inertia lambda > 0 becomes REQUIRED (its value irrelevant)",
          "N^3 rms|grad| " + ", ".join(f"{v[0]:.2f}" for v in nl_scal.values()) + f"; L(FRW) = xi: {frw_closed}; det(h=0, lambda=0) = {det_h0_l0}; "
          f"root {r2num[0]:.2e}/{r2num[1]:.2e}", a1_ok)

    # A2 the scale and its running
    LT = {}
    for rd in ("lin", "NL"):
        for s in (1.0, DELTA_C):
            LT[(rd, s)] = L_table(s, rd)
    Lfun = {k_: fun_of(v) for k_, v in LT.items()}

    def n_eff(Lf, z1=0.25, z2=2.5):
        return 2 * math.log(Lf(1 / (1 + z2)) / Lf(1 / (1 + z1))) / math.log(OmL_z(z2) / OmL_z(z1))
    for k_, Lf in Lfun.items():
        P(f"    {k_[0]:>3} s = {k_[1]:.3f}: L(z) = " + ", ".join(f"{zz}: {1e3 * Lf(1 / (1 + zz)):.0f}" for zz in (0.0, 0.25, 0.5, 1.0, 2.0, 2.5, 3.0))
          + f" kpc; n_eff(0.25 -> 2.5) = {n_eff(Lf):.2f}; M_*(0.25) = (2 pi)^1.5 rho_m L_com^3 = "
          f"{(2 * math.pi) ** 1.5 * Om * rho_crit0 * (Lf(0.8) / 0.8 * Mpc) ** 3 / MSUN:.1e} Msun")
    LNLs = {s: L_table(s, "NL") for s in (1.3, 1.5, 2.0, 2.4, 3.0)}
    ne_scan = {s: n_eff(fun_of(t)) for s, t in LNLs.items()}
    L9n = n_eff(L9)
    a2_ok = 2.0 - 0.05 <= n_eff(Lfun[("NL", DELTA_C)]) <= 2.7 and 2.0 <= n_eff(Lfun[("lin", DELTA_C)]) <= 2.7 and all(1.9 <= v <= 2.2 for v in ne_scan.values())
    check("A2 n IS THE STATE'S OWN RUNNING (derived): the matter field's heat-smoothed nonlinear scale shrinks into the past as "
          "Omega_L^(n_eff/2) with n_eff = 2.06 (nonlinear reading; 2.02-2.13 for every threshold 1.3-3, 1.99 at s = 1) and 2.66 (linear reading, "
          "delta_c) between z = 0.25 and 2.5 -- inside FP9's window n in [2, 2.7] with no exponent declared; the Mpc size is the web's "
          "characteristic (Press-Schechter) mass M_* ~ 1e13 Msun, which a leaf average CAN read (FP9 V1's host-mass loophole)",
          f"n_eff: NL/delta_c {n_eff(Lfun[('NL', DELTA_C)]):.3f}, lin/delta_c {n_eff(Lfun[('lin', DELTA_C)]):.3f}, NL/1 {n_eff(Lfun[('NL', 1.0)]):.3f}, "
          f"lin/1 {n_eff(Lfun[('lin', 1.0)]):.3f}; NL scan {', '.join(f'{s}: {v:.2f}' for s, v in ne_scan.items())}; FP9 declared n = {L9n:.2f}", a2_ok)
    OUT["numbers"]["A2"] = {"L_kpc": {f"{k_[0]}_{k_[1]:.3f}": {str(zz): 1e3 * Lfun[k_](1 / (1 + zz)) for zz in (0.0, 0.25, 0.5, 1.0, 2.0, 2.5, 3.0)} for k_ in Lfun},
                            "n_eff": {f"{k_[0]}_{k_[1]:.3f}": n_eff(Lfun[k_]) for k_ in Lfun}, "n_eff_NL_scan": ne_scan}
    P(f"    {el()}")

    # the headline tables (needed from here on)
    LH_tab = L_table(HEAD_S, HEAD_READ); Lh = fun_of(LH_tab)
    yh, yh_tab, rms_h = yth_state(LH_tab, HEAD_READ, HEAD_SWITCH, HEAD_CY)

    # A3 threshold windows
    a3 = {}
    for rd, ss in (("NL", (1.0, 1.2, 1.3, 1.5, DELTA_C, 2.0, 2.4, 2.6, 2.7)), ("lin", (1.0, 1.1, 1.2, 1.4, 1.6, 1.65, DELTA_C, 1.75))):
        for s in ss:
            Lt = L_table(s, rd); Lf = fun_of(Lt)
            ysd, _, _ = yth_state(Lt, rd, "ramp", 1.0)
            a3[(rd, s, "FP9 yield")] = gates(Lf, y9d)
            a3[(rd, s, "state yield")] = gates(Lf, ysd, extra=(s in (DELTA_C, 1.3, 2.0)))
            for yl in ("FP9 yield", "state yield"):
                P(f"    {rd:>3} s = {s:.3f} ({yl:11s}): L(0.25) = {Lf(0.8):.3f} Mpc, L(2.5) = {1e3 * Lf(1 / 3.5):5.1f} kpc | {gline(a3[(rd, s, yl)])}")
    win = {(rd, yl): [k_[1] for k_, v in a3.items() if k_[0] == rd and k_[2] == yl and v["all"]] for rd in ("NL", "lin") for yl in ("FP9 yield", "state yield")}
    P("    windows (s passing all five): " + "; ".join(f"{k_[0]}/{k_[1]}: {[round(s, 3) for s in v]}" for k_, v in win.items()))
    a3a = a3[("NL", DELTA_C, "FP9 yield")]["all"] and a3[("NL", DELTA_C, "state yield")]["all"]
    check("A3a THE NATURAL COLLAPSE THRESHOLD WORKS IN THE NONLINEAR READING: with L the scale where the actual (nonlinear) matter "
          "field's heat-smoothed leaf-rms contrast equals delta_c = 1.686, the separator passes sigma_8, the forest, the flagship, SPARC "
          "and KiDS on both footings and both modes -- with FP9's yield held AND with the state yield (D2) -- no length declared",
          f"FP9 yield: {gline(a3[('NL', DELTA_C, 'FP9 yield')])}; state yield: {gline(a3[('NL', DELTA_C, 'state yield')])}", a3a)
    a3b = (not a3[("NL", 1.0, "FP9 yield")]["ok"]["sigma_8"]) and (not a3[("lin", 1.0, "FP9 yield")]["ok"]["sigma_8"]) and (not a3[("NL", 1.0, "state yield")]["ok"]["sigma_8"])
    check("A3b THE OTHER NATURAL THRESHOLD FAILS (verified): s = 1 (the textbook nonlinear scale, halofit's k_sigma) makes L too long -- "
          "sigma_8 leaves the band in both readings, with either yield: s is a CHOICE between natural O(1) numbers, not a derivation",
          f"s = 1: NL/FP9 yield s8 max {max(a3[('NL', 1.0, 'FP9 yield')]['s8'].values()):.3f}, NL/state {max(a3[('NL', 1.0, 'state yield')]['s8'].values()):.3f}, "
          f"lin/FP9 {max(a3[('lin', 1.0, 'FP9 yield')]['s8'].values()):.3f}, lin/state {max(a3[('lin', 1.0, 'state yield')]['s8'].values()):.3f}", a3b)
    lin_dc = a3[("lin", DELTA_C, "FP9 yield")]
    check("A3c (reported) THE LINEAR READING IS NARROWER AND EXCLUDES delta_c: on the linear field the window is the printed s range and "
          "delta_c misses it by a hair (flagship and KiDS, one footing each) -- the result is CONDITIONAL on the action reading the actual "
          "(nonlinear) field, which is what a leaf average of D_i(a^i - D^i chi) is; the linear field is not a state variable",
          f"lin window {[round(s, 3) for s in win[('lin', 'FP9 yield')]]} (FP9 yield), {[round(s, 3) for s in win[('lin', 'state yield')]]} (state yield); "
          f"lin/delta_c: {gline(lin_dc)}; NL window {[round(s, 3) for s in win[('NL', 'FP9 yield')]]} / {[round(s, 3) for s in win[('NL', 'state yield')]]}",
          True, load_bearing=False)
    OUT["numbers"]["A3"] = {f"{k_[0]}_{k_[1]:.3f}_{k_[2]}": {"s8": js(v["s8"]), "forest": js(v["forest"]), "flag": js(v["flag"]), "sparc": v["sparc"],
                                                             "kids": v["kids"], "ok": v["ok"], "all": v["all"]} for k_, v in a3.items()}
    OUT["numbers"]["A3_windows"] = {f"{k_[0]}/{k_[1]}": v for k_, v in win.items()}
    P(f"    {el()}")

    # A4 self-consistent readouts (the chain's linear state, fed back)
    D0cache = {}

    def growth_sc(s, a0v, mode="rms", yfix=None, ysw=None, readout="matter", base="lin", KHg=None, Dig=None, zs_out=(), rtol=1e-6,
                  track=None, lam=0.0):
        """FP9's AQUAL growth with L (and optionally y_th) read from the RUNNING state: sigma_G(L) = s on the state's spectrum
        (base spectrum x the running boost D_k/D_k^LCDM, interpolated in log k); readout 'dyn' multiplies delta by (1 + C_eff w)."""
        KHg = KH if KHg is None else KHg; Dig = DI if Dig is None else Dig
        nk = len(KHg); m341 = KHg <= 20.0 * 1.0001; kk341 = KHg[m341]; norm341 = np.trapz(1 / kk341, kk341)
        key = id(KHg)
        if key not in D0cache:
            D0cache[key] = np.array([Delta_lin0(k) for k in KHg])
        D0g = D0cache[key]; lkg = np.log(KHg)

        def base_D2(a):
            if base == "lin":
                return D2L0 * Dl(a) ** 2
            x = math.log(a); j = min(max(np.searchsorted(LNA, x) - 1, 0), len(LNA) - 2); f_ = (x - LNA[j]) / (LNA[j + 1] - LNA[j])
            return (1 - f_) * D2NL[j] + f_ * D2NL[j + 1]

        def Lof(a, D, fac, D2b):
            bf = np.interp(LKF, lkg, np.abs(D) * fac / (D0g * Dl(a)))
            D2 = D2b * bf ** 2
            if sig2(RMIN, D2) < s * s:
                return XI_FLOOR_MPC, D2
            return brentq(lambda R: sig2(R, D2) - s * s, RMIN, 300.0) / h * a, D2

        def fields(a, D, L, yth):
            hk = 1.0 - np.exp(-0.5 * (KHg * h * L / a) ** 2); gb = gfield(D, a, KHg) * hk
            y = np.full(nk, math.sqrt(np.trapz(gb[m341] ** 2 / kk341, kk341) / norm341) / a0v) if mode == "rms" else gb / a0v
            CQ = np.maximum((nu_p2(y) - 1.0) * cutfac(y, yth, YIELD), 0.0)
            lam_phi = lam + (2 + 3 * C2W) * hk ** 2 / C2W
            cs = c / np.sqrt(np.maximum(CQ, 1e-300) * np.maximum(lam_phi, 1e-300))
            kk = (1.0 * h / (a * Mpc)) if mode == "rms" else KHg * h / (a * Mpc)
            return CQ * hk ** 2 / (1.0 + (H0 * Ez(a) / (cs * kk)) ** 2)

        def ystate(a, L, D2):
            g = 4 * math.pi * G * Om * rho_crit0 / a ** 3 * np.sqrt(D2) / (KKF * h / (a * Mpc)) * (1.0 - np.exp(-0.5 * (KKF * h * L / a) ** 2))
            return math.sqrt(float(np.trapz(g ** 2, LKF))) / a0v * SWITCH[ysw](a)

        def rhs(N_, Y):
            a = math.exp(N_); D = Y[:nk]; Dp = Y[nk:]; D2b = base_D2(a)
            L, D2s = Lof(a, D, 1.0, D2b)
            yth = yfix(a) if yfix is not None else ystate(a, L, D2s)
            Ce = fields(a, D, L, yth)
            if readout == "dyn":
                for _ in range(2):
                    L, D2s = Lof(a, D, 1.0 + Ce, D2b)
                    Ce = fields(a, D, L, yth)
            if track is not None:
                track.append((a, L))
            return np.concatenate([Dp, 1.5 * (Om / a ** 3 / Ez(a) ** 2) * (1.0 + Ce) * D - (2 + dlnH(a)) * Dp])
        Nout = sorted({math.log(1 / (1 + z)) for z in zs_out if z > 0}) + [0.0]
        sol_ = solve_ivp(rhs, (math.log(A_I), 0.0), np.concatenate([Dig, Dig]), method="LSODA", rtol=rtol, atol=1e-24, t_eval=Nout)
        return {round(1 / math.exp(N_) - 1, 6): sol_.y[:nk, i] for i, N_ in enumerate(sol_.t)}

    def sc_run(s, readout, base, yfd=None, ysw=None, modes=MODES, foots=FOOTS):
        s8, trk = {}, []
        for f in foots:
            for m in modes:
                tr = [] if (f, m) == ("canonical", "permode") else None
                g = growth_sc(s, A0[f], mode=m, yfix=(yfd[f] if yfd else None), ysw=ysw, readout=readout, base=base, track=tr)
                s8[(f, m)] = sigma8_of(g[0.0]) / S8_LCDM
                if tr is not None:
                    trk = tr
        trk = sorted(trk); ta = np.array([t_[0] for t_ in trk]); tL = np.array([t_[1] for t_ in trk])
        return s8, (lambda a: float(np.interp(a, ta, tL))) if len(ta) else None
    a4 = {}
    for s in (DELTA_C, 2.0, 2.5, 3.0):
        a4[("dyn", s)] = sc_run(s, "dyn", "lin", yfd=y9d, modes=MODES, foots=("canonical",))
    a4[("matter", DELTA_C)] = sc_run(DELTA_C, "matter", "lin", yfd=y9d)
    L_lin_dc = Lfun[("lin", DELTA_C)]
    for k_, (s8v, Lsc) in a4.items():
        P(f"    self-consistent {k_[0]:>6} readout, s = {k_[1]:.3f} (linear state, FP9 yield): sigma_8 " + ", ".join(f"{kk[0][:3]}/{kk[1]} {v:.4f}" for kk, v in s8v.items())
          + f" | L_sc(0) = {Lsc(1.0):.2f}, L_sc(0.25) = {Lsc(0.8):.2f} Mpc, L_sc(2.5) = {1e3 * Lsc(1 / 3.5):.1f} kpc")
    dyn_fail = all(max(a4[("dyn", s)][0].values()) > SIG8_BAND[1] for s in (DELTA_C, 2.0))
    s_flag_max = max([s for s in (1.0, 1.1, 1.2, 1.4, 1.6, 1.65, DELTA_C, 1.75) if a3[("lin", s, "FP9 yield")]["ok"]["flagship"]] or [0])
    dyn_s8_min = min([s for s in (DELTA_C, 2.0, 2.5, 3.0) if max(a4[("dyn", s)][0].values()) <= SIG8_BAND[1]] or [99])
    Lsc_m = a4[("matter", DELTA_C)][1]
    mat_ok = max(a4[("matter", DELTA_C)][0].values()) <= SIG8_TIGHT and abs(Lsc_m(0.8) / L_lin_dc(0.8) - 1) < 0.20
    check("A4 THE READOUT IS FORCED (derived both ways): read from the DYNAMICAL density (D_i a^i, the MOND phantom included) the "
          "separator feeds on its own phantom -- the sub-L MOND boost raises the state's smoothed variance, which lengthens L, which "
          "lets more MOND through: sigma_8 leaves the band at every s <= 2 while the flagship (MOND off at z = 2.5, where L is the "
          "state's own) needs s <= the printed edge -- NO window (FAIL, verified); read from the MATTER density (D_i(a^i - D^i chi), "
          "the chassis's Newtonian combination, FP7 A1) the feedback is mild and stable",
          "dyn: sigma_8 max " + ", ".join(f"s={s_:.2f}: {max(a4[('dyn', s_)][0].values()):.3f}" for s_ in (DELTA_C, 2.0, 2.5, 3.0)) + "; "
          f"dyn needs s >= {dyn_s8_min:.2f} for sigma_8, the flagship s <= {s_flag_max:.3f}; matter: sigma_8 <= {max(a4[('matter', DELTA_C)][0].values()):.4f}, "
          f"L_sc(0.25)/L_state(0.25) = {Lsc_m(0.8) / L_lin_dc(0.8):.3f}", dyn_fail and dyn_s8_min > s_flag_max and mat_ok)
    OUT["numbers"]["A4"] = {f"{k_[0]}_{k_[1]:.3f}": {"s8": js(v[0]), "L0": v[1](1.0), "L025": v[1](0.8), "L25": v[1](1 / 3.5)} for k_, v in a4.items()}

    # A5 the other named measures
    def xP2s(D):
        return 0.0 if D <= 0 else 1.0 / (1.0 + math.sqrt(1.0 + 1.0 / D))

    def JP2x(x):
        return -0.25 * math.log(1 - 2 * x) - x / 2 - x * x / 2

    def maxwell(fun, rms):
        s_ = rms / math.sqrt(3.0)
        return quad(lambda u: fun(u * s_) * math.sqrt(2 / math.pi) * u * u * math.exp(-u * u / 2), 0, 12, limit=200)[0]
    i025 = int(np.argmin(np.abs(AGR - 0.8)))
    epsM = {}
    for rd in ("lin", "NL"):
        for Lm in (0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0):
            yr = gbp_rms_phys(i025, Lm, rd) / A0["canonical"]
            epsM[(rd, Lm)] = (yr, maxwell(lambda y: JP2x(xP2s(y)), yr) / maxwell(lambda y: y * y, yr))
    sgR = [math.sqrt(sig2(R, D2LIN[i025])) for R in np.geomspace(1e-3, 30, 40)]
    mono = all(np.diff(sgR) < 0)
    P("    MOND energy / Newtonian field energy of the band-passed web at z = 0.25 vs L [Mpc]: "
      + "; ".join(f"{rd} " + ", ".join(f"{Lm}: {v[1]:.1f}" for (rd2, Lm), v in epsM.items() if rd2 == rd) for rd in ("lin", "NL")))
    P(f"    linear sigma_G(R) at z = 0.25, R = 1e-3 .. 30 Mpc/h: {sgR[0]:.2f} -> {sgR[-1]:.3f}, strictly decreasing: {mono} (no feature: only a threshold picks R)")
    a5_ok = min(v[1] for v in epsM.values()) > 3.0 and mono
    check("A5 THE OTHER NAMED MEASURES SET NO WEB LENGTH (verified): the leaf-averaged MOND-sector energy is 4-90x the Newtonian field "
          "energy at every band-pass length 10 kpc-30 Mpc (the web is deep-MOND), so 'MOND energy = field energy' has no root and any "
          "other ratio is a declared number (reading-dependent: the same ratio picks lengths a decade apart); the unsmoothed variance "
          "reads the smallest scale of the state (galaxies, stars, the filter xi), and sigma(R) has no feature -- the heat branch's "
          "relaxation depth against the web's variance IS candidate (a)'s condition",
          f"eps_M range lin {min(v[1] for k_, v in epsM.items() if k_[0] == 'lin'):.1f}-{max(v[1] for k_, v in epsM.items() if k_[0] == 'lin'):.1f}, "
          f"NL {min(v[1] for k_, v in epsM.items() if k_[0] == 'NL'):.1f}-{max(v[1] for k_, v in epsM.items() if k_[0] == 'NL'):.1f}; sigma(R) monotone {mono}", a5_ok)
    OUT["numbers"]["A5"] = {f"{k_[0]}_{k_[1]}": v for k_, v in epsM.items()}

    # A6 the linear-spectrum systematic (CLASS vs EH98)
    a6 = {}
    if CLS is not None:
        for z in (0.0, 0.25, 1.0, 2.5):
            a_ = 1 / (1 + z)
            PLc = np.array([CLS.pk_lin(k * h, z) for k in KKF[(KKF >= 1e-3) & (KKF <= 150)]]) * h ** 3
            kc = KKF[(KKF >= 1e-3) & (KKF <= 150)]
            D2c = np.interp(LKF, np.log(kc), kc ** 3 * PLc / (2 * math.pi ** 2), left=0.0, right=0.0)
            for rd in ("lin", "NL"):
                DD = halofit(D2c, a_, CLS.Omega_m())[0] if rd == "NL" else D2c
                Rc = brentq(lambda R: sig2(R, DD) - DELTA_C ** 2, RMIN, 100.0)
                a6[(z, rd)] = (Rc / h * a_, Lfun[(rd, DELTA_C)](a_))
    P("    L(z) at delta_c, CLASS's linear spectrum vs EH98 (the chain's): " + "; ".join(f"z={k_[0]} {k_[1]}: {1e3 * v[0]:.0f} vs {1e3 * v[1]:.0f} kpc" for k_, v in a6.items()))
    check("A6 (reported) THE LINEAR-SPECTRUM SYSTEMATIC: the nonlinear reading of the state is insensitive to the small-scale shape of "
          "the linear spectrum (CLASS vs EH98), the linear reading is not -- another reason the actual (nonlinear) field is the "
          "robust reading",
          "; ".join(f"z={k_[0]} {k_[1]}: {v[0] / v[1] - 1:+.0%}" for k_, v in a6.items()) or "CLASS unavailable", True, load_bearing=False)
    OUT["numbers"]["A6"] = {f"{k_[0]}_{k_[1]}": v for k_, v in a6.items()}

    # A7 the nonlinear reading's dependence on the dark sector's small-scale state (FP10's clearing thins the halo term)
    a7 = {}
    for fH in (1.0, 0.6, 0.44, 0.34, 0.2):
        STATE["fH"] = [((lambda q: q[0] + fH * q[1])(halofit(D2LIN[i], AGR[i], split=True)) if sig2(RMIN, D2LIN[i]) > 1.0 else D2LIN[i])
                       for i in range(len(LNA))]
        Lt = L_table(DELTA_C, "fH"); Lf = fun_of(Lt)
        ysd, _, _ = yth_state(Lt, "fH", "ramp", 1.0)
        a7[fH] = (Lf(0.8), Lf(1 / 3.5), gates(Lf, ysd, extra=True))
        P(f"    one-halo term x {fH:.2f}: L(0.25) = {a7[fH][0]:.2f} Mpc, L(2.5) = {1e3 * a7[fH][1]:.0f} kpc | {gline(a7[fH][2])}")
    STATE.pop("fH", None)
    a7_five = [fH for fH, v in a7.items() if v[2]["all"]]
    a7_spread = [fH for fH, v in a7.items() if v[2]["all"] and max(v[2]["kids@0.4"].values()) <= KIDS_TOL]
    check("A7 (reported) THE NONLINEAR READING DEPENDS ON THE DARK SECTOR'S SMALL-SCALE STATE: halofit's one-halo term stands for "
          "LCDM-like halos; FP10's clearing kicks 40-50% of the halo dark mass out by z <~ 2.5, which thins the one-halo power to "
          "roughly (0.16 + 0.84 x 0.5-0.6)^2 ~ 0.34-0.44 of LCDM's (a crude stand-in, not a computation of FP10's field); scaling the "
          "term shortens L toward the linear reading -- the five lead-grade gates hold down to the printed factor, the z = 0.4 lens "
          "check only to the larger printed factor: delta_c's success needs the web's halos to stay LCDM-like to ~50%",
          f"five gates pass for one-halo factors {a7_five}; + KiDS at z = 0.4 for {a7_spread}", True, load_bearing=False)
    OUT["numbers"]["A7"] = {str(fH): {"L025": v[0], "L25": v[1], "all": v[2]["all"], "kids04": v[2]["kids@0.4"], "s8": js(v[2]["s8"])} for fH, v in a7.items()}
    P(f"    {el()}")

    # ============================================================================================= B  CANDIDATE (b)
    banner("B  CANDIDATE (b): the dark field's own lengths at FP10's mass")
    sv0 = None

    def sigv(a):
        D = Dl(a); f_ = Om_a(a) ** 0.55
        return f_ * H0 * Ez(a) * math.sqrt(float(np.trapz(D2L0 * D ** 2 / (KKF * h / (a * Mpc)) ** 2, LKF)))
    sv0 = sigv(0.8)
    b1 = {}
    for m in M_DARK:
        hbm = HBARC_EVM * c / m                                                     # hbar/m [m^2/s]
        b1[m] = {"Compton [pc]": HBARC_EVM / m / (Mpc / 1e6),
                 "de Broglie h/(m v), v = sigma_v(0.25) [pc]": 2 * math.pi * hbm / sv0 / (Mpc / 1e6),
                 "de Broglie, v = 200 km/s [pc]": 2 * math.pi * hbm / 2e5 / (Mpc / 1e6),
                 "Jeans, cosmic mean (z = 0.25) [kpc]": 1e3 * jeans_phys(m, Om * rho_crit0 / 0.8 ** 3),
                 "Jeans, 200 x mean (halo) [kpc]": 1e3 * jeans_phys(m, 200 * Om * rho_crit0 / 0.8 ** 3)}
    lJ = b1[M_DARK[0]]["Jeans, cosmic mean (z = 0.25) [kpc]"]
    m_need = M_DARK[0] * (lJ / 1.2e3) ** 2                                          # lambda_J ~ m^(-1/2): the m giving 1.2 Mpc at z = 0.25
    nJ = 2 * 0.75 * math.log(1.25 / 3.5) / math.log(OmL_z(2.5) / OmL_z(0.25))
    for m, d in b1.items():
        P(f"    m = {m:.1e} eV: " + "; ".join(f"{k_} {v:.3g}" for k_, v in d.items()))
    P(f"    sigma_v(0.25) = {sv0 / 1e3:.0f} km/s (3-D, linear); the mass a 1.2-Mpc Jeans length needs: {m_need:.1e} eV (floor {M_DARK[0]:.1e}); "
      f"Jeans running lambda_J ~ rho^(-1/4) ~ a^(3/4): n_eff = {nJ:.2f}; Compton: n_eff = 0")
    b_kpc = max(max(v * (1e-3 if "[pc]" in k_ else 1.0) for k_, v in d.items()) for d in b1.values())
    b_ok = (b_kpc < 2.0 and m_need < M_DARK[0] * 1e-4 and nJ < 2.0)
    check("B1 THE DARK FIELD CANNOT SUPPLY THE SCALE (FAIL, verified): at FP10's floor m >= 1.9-5.2e-19 eV every length it carries is "
          "sub-2-kpc (Compton ~1-3e-5 pc, de Broglie 0.05-0.3 pc, Jeans 0.3-1.8 kpc at halo and cosmic densities); a 1.2-Mpc Jeans "
          "length needs m ~ 4e-25 eV, 5.7 decades below the floor; the Jeans length runs as a^(3/4) (n_eff ~ 0.65 < 2, FP9's growth bound), the "
          "Compton length not at all; and the dark field is kernel-invisible (FP10: S = 0, L353's pair) -- the separator cannot read "
          "Psi's state without a coupling the chain has excluded.  The same holds for FP9's y_th bounds: m enters no dimensionless "
          "yield at a natural power (FP10 C3's census: any window is hit at SOME m)",
          f"longest length {b_kpc:.2f} kpc; m needed {m_need:.1e} eV ({math.log10(M_DARK[0] / m_need):.1f} decades below the floor); n_eff(Jeans) {nJ:.2f}", b_ok)
    OUT["numbers"]["B1"] = {str(m): d for m, d in b1.items()}
    OUT["numbers"]["B1"]["m_need_eV"] = m_need; OUT["numbers"]["B1"]["nJ"] = nJ

    # ============================================================================================= C  CANDIDATE (c)
    banner("C  CANDIDATE (c): the epoch exponents -- n from the state's running (A2); p' against every state measure; onset switches")
    need = math.log10(4e-3 / 3e-6)                                                   # the yield's required rise z = 0.25 -> 2.5 (FP9 H1)
    iz = {z: int(np.argmin(np.abs(AGR - 1 / (1 + z)))) for z in (0.25, 2.5)}
    rawr = {rd: gbp_rms_phys(iz[2.5], 0, rd, bp=False) / gbp_rms_phys(iz[0.25], 0, rd, bp=False) for rd in ("lin", "NL")}
    bpr = {rd: gbp_rms_phys(iz[2.5], LH_tab[iz[2.5]], rd) / gbp_rms_phys(iz[0.25], LH_tab[iz[0.25]], rd) for rd in ("lin", "NL")}

    def ek_ratio(i, rd):
        a = AGR[i]; yr = gbp_rms_phys(i, LH_tab[i], rd) / A0["canonical"]
        EM = A0["canonical"] ** 2 / (8 * math.pi * G) * maxwell(lambda y: JP2x(xP2s(y)), yr)
        return EM / (0.5 * Om * rho_crit0 / a ** 3 * sigv(a) ** 2)
    ekr = {rd: ek_ratio(iz[0.25], rd) / ek_ratio(iz[2.5], rd) for rd in ("lin", "NL")}
    cen = {"1/Omega_L (the clock)": OmL_z(0.25) / OmL_z(2.5), "Omega_m": (1 - OmL_z(2.5)) / (1 - OmL_z(0.25)),
           "1/D (the web's amplitude)": Dl(0.8) / Dl(1 / 3.5), "raw web rms (lin)": rawr["lin"], "raw web rms (NL)": rawr["NL"],
           "band-passed rms (lin)": bpr["lin"], "band-passed rms (NL)": bpr["NL"],
           "c/(H L_nl) (the scale vs the horizon)": (Lh(0.8) * Ez(0.8)) / (Lh(1 / 3.5) * Ez(1 / 3.5)),
           "E_kin/E_MOND (lin)": ekr["lin"], "E_kin/E_MOND (NL)": ekr["NL"],
           "M_* (needs a reference mass)": (Lh(0.8) / 0.8 / (Lh(1 / 3.5) * 3.5)) ** 3}
    rows = {k_: (math.log10(v), need / math.log10(v) if v > 1 else float("inf")) for k_, v in cen.items()}
    for k_, (dl_, ex_) in rows.items():
        P(f"    {k_:40s} log10 change z 0.25 -> 2.5: {dl_:+.2f}  -> exponent needed for the yield's {need:.2f} decades: {ex_:.1f}")
    steepest_nat = max(v[0] for k_, v in rows.items() if "M_*" not in k_)
    yL3 = 3e-6 * OmL_z(0.25) ** 3
    check("C1 p' IS NOT A STATE QUANTITY (FAIL, verified): the yield must rise by >= 3.1 decades from z = 0.25 (KiDS: <= 3e-6) to "
          "z = 2.5 (forest: >= 4e-3); every dimensionless state measure changes by at most ~1 decade over that interval (the clock "
          "1/Omega_L 1.04, the web's field 0.1-0.5, its amplitude 0.39), so a power law needs a DECLARED exponent (>= 3.0 on the "
          "steepest, the clock: FP9's p') AND a declared normalisation (y_Lambda <= 4.4e-7 at p' = 3); only a mass (M_*) runs faster, "
          "and it needs a reference mass",
          f"steepest natural measure {steepest_nat:.2f} dex vs {need:.2f} needed; normalisation at p' = 3: y_Lambda <= {yL3:.1e}", steepest_nat < need)
    OUT["numbers"]["C1"] = {k_: {"dex": v[0], "exponent": v[1]} for k_, v in rows.items()}

    # C2 onset switches (sign changes need no exponent)
    ek_tab = {rd: np.array([ek_ratio(i, rd) for i in range(len(LNA))]) for rd in ("lin", "NL")}

    def z_cross(tab):
        s_ = np.sign(tab - 1.0); idx = np.where(s_[:-1] != s_[1:])[0]
        return [float(1 / AGR[j] - 1) for j in idx]
    z_ek = {rd: z_cross(ek_tab[rd]) for rd in ("lin", "NL")}
    c2 = {}
    for nm, sw in (("q = 0 (ramp)", "ramp"), ("q = 0 (step)", "step"), ("Omega_L = Omega_m", "eq")):
        ysd, _, _ = yth_state(LH_tab, HEAD_READ, sw, 1.0)
        c2[nm] = gates(Lh, ysd, extra=True)
    for rd in ("lin", "NL"):
        onset = (lambda tab: (lambda a: 1.0 if float(np.interp(math.log(a), LNA, tab)) < 1.0 else 0.0))(ek_tab[rd])
        ysd, _, _ = yth_state(LH_tab, HEAD_READ, onset=onset)
        c2[f"E_MOND = E_kin ({rd} reading)"] = gates(Lh, ysd, extra=True)
    y_off = {f: (lambda a: 0.0) for f in FOOTS}                                      # 'first y ~ 1 on the leaf': z_on >~ 20, off after
    c2["first y ~ 1 on the leaf (z_on >~ 20)"] = gates(Lh, y_off, extra=True)
    for nm, r in c2.items():
        P(f"    onset {nm:38s}: {gline(r)}")
    P(f"    epochs: q = 0 at z = {Z_Q0:.3f} (Omega_L = 1/3); Omega_L = Omega_m at z = {Z_EQ:.3f}; E_MOND = E_kin at z = {z_ek['lin']} (lin) / {z_ek['NL']} (NL); "
      f"the leaf's maximum field passes a0 at the first stars (z >~ 20)")
    good = lambda r: r["all"] and max(r["kids@0.4"].values()) <= KIDS_TOL
    c2_ok = (good(c2["q = 0 (ramp)"]) and good(c2["q = 0 (step)"]) and not good(c2["Omega_L = Omega_m"])
             and not c2["first y ~ 1 on the leaf (z_on >~ 20)"]["ok"]["forest"])
    check(f"C2 A SIGN CHANGE NEEDS NO EXPONENT: the leaf's deceleration q = (1 + Omega_r - 3 Omega_L)/2 changes sign at z = {Z_Q0:.3f} "
          "(Omega_L(<K>_h) ~ 1/3), inside the window z_on in (~0.5, ~2) that the KiDS lens spread (z <= 0.5, yield off) and the forest "
          "(z >= 2, yield on) leave; switched there (ramp or step) the state yield passes the five gates AND KiDS at z = 0.4; the "
          "alternatives: Omega_L = Omega_m (z = 0.30) fails the lens spread, E_MOND = E_kin is reading-dependent (the printed "
          "epochs: at z = 0.18 on the linear field it fails KiDS, at z = 1.83 on the actual field it passes -- a second natural onset, not a "
          "reading-independent one), and 'the first y ~ 1 on the leaf' switches at the first stars, leaving the forest and sigma_8 "
          "unprotected (FP9's route (i))",
          "; ".join(f"{nm}: {'pass' if good(r) else 'FAIL'}" for nm, r in c2.items()), c2_ok)
    OUT["numbers"]["C2"] = {nm: {"s8": js(r["s8"]), "forest": js(r["forest"]), "flag": js(r["flag"]), "sparc": r["sparc"], "kids": r["kids"],
                                 "kids04": r["kids@0.4"], "kids07": r["kids@0.7"], "all": r["all"]} for nm, r in c2.items()}
    OUT["numbers"]["C2_epochs"] = {"q0": Z_Q0, "eq": Z_EQ, "ek_lin": z_ek["lin"], "ek_NL": z_ek["NL"]}
    P(f"    {el()}")

    # ============================================================================================= D  CANDIDATE (d)
    banner("D  CANDIDATE (d): the yield threshold from the leaf-averaged field itself")
    d1 = {}
    for nm, (rd, bp) in (("raw rms (lin)", ("lin", False)), ("raw rms (NL)", ("NL", False)), ("band-passed rms (lin)", ("lin", True)),
                         ("band-passed rms (NL)", ("NL", True))):
        rms = np.array([gbp_rms_phys(i, LH_tab[i], rd, bp=bp) for i in range(len(LNA))])
        ysd = {f: fun_of(rms / A0[f], log=False) for f in FOOTS}
        d1[nm] = (ysd["canonical"](0.8), ysd["canonical"](1 / 3.5), gates(Lh, ysd))
        P(f"    y_th = {nm:22s}: y_th(0.25) = {d1[nm][0]:.2e} ({math.log10(d1[nm][0] / 3e-6):+.1f} dex over KiDS's 3e-6), y_th(2.5) = {d1[nm][1]:.2e} | {gline(d1[nm][2])}")
    d1_ok = all((not v[2]["ok"]["KiDS"]) and v[0] > 3e-6 * 100 for v in d1.values())
    check("D1 THE YIELD AT THE WEB'S RMS ALONE FAILS (verified): y_th = the leaf-rms field (raw or band-passed, linear or nonlinear; "
          "FP6's 4.8e-3-1.3e-2 at z = 0.25) sits 3.0-3.8 decades above KiDS's ceiling y_th(0.25) <~ 3e-6: KiDS's lenses at 0.3-3 Mpc "
          "live BELOW the web's rms field, so any threshold that tracks the web switches their phantom off (KiDS d chi^2 +870 to "
          "+1200; SPARC's y = 0.01 points too) -- incompatible, as the coordinator suspected",
          "; ".join(f"{nm}: {v[0]:.1e} ({math.log10(v[0] / 3e-6):+.1f} dex), KiDS {max(v[2]['kids'].values()):+.0f}, SPARC {max(v[2]['sparc'].values()):.2f} dex"
                    for nm, v in d1.items()), d1_ok)
    OUT["numbers"]["D1"] = {nm: {"y025": v[0], "y25": v[1], "kids": v[2]["kids"], "sparc": v[2]["sparc"]} for nm, v in d1.items()}

    d2 = {}
    for rd in ("NL", "lin"):
        for cy in (0.1, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0):
            ysd, _, _ = yth_state(LH_tab, rd, "ramp", cy)
            d2[(rd, cy)] = gates(Lh, ysd)
    cwin = {rd: [cy for (r2, cy), v in d2.items() if r2 == rd and v["all"]] for rd in ("NL", "lin")}
    for (rd, cy), r in d2.items():
        P(f"    y_th = {cy:.1f} x band-passed rms ({rd:>3}) x max(0, 2q): {gline(r)}")
    d2_ok = d2[("NL", 1.0)]["all"] and d2[("lin", 1.0)]["all"]
    check("D2 THE YIELD AT THE WEB'S RMS WHILE THE LEAF DECELERATES: y_th = c_y <|g_bp|^2>_h^(1/2)/a0 x max(0, 2q) with c_y = 1 (no "
          "coefficient) passes the five gates in both readings of the state; the coefficient's window is the printed range -- the level "
          "must sit above the web's per-mode fields (forest) and below the flagship's ~0.03 (z = 2.5): y_Lambda is replaced by the "
          "state's own rms, p' by the sign of q",
          f"c_y window NL {cwin['NL']}, lin {cwin['lin']}", d2_ok)
    OUT["numbers"]["D2"] = {f"{k_[0]}_{k_[1]}": {"all": v["all"], "ok": v["ok"]} for k_, v in d2.items()}
    OUT["numbers"]["D2_window"] = cwin
    P(f"    {el()}")

    # ============================================================================================= H  THE HEADLINE (H_S)
    banner(f"H  THE HEADLINE (H_S): L at delta_c on the actual field, y_th = the web's band-passed rms x {HEAD_SWITCH} switch" + ("  [MUTATE]" if MUTATE else ""))
    H = gates(Lh, yh, extra=True)
    h_conv = {}
    for f in FOOTS:
        mod = model_of(Lh, yh[f])
        h_conv[f] = (s8_aq(mod, f, "rms"), s8_aq(mod, f, "rms", rtol=1e-8))
    KHF2 = np.logspace(math.log10(0.02), math.log10(100.0), 144); DIF2 = np.array([Delta_lin0(k) for k in KHF2]) / M6["_r0"]
    REF_F2 = M6["growth"](M6["lcdm_model"](), A0["canonical"], KHg=KHF2, Dig=DIF2, zs_out=(2.0, 3.0))
    modc = model_of(Lh, yh["canonical"])
    fconv = {m: (forest_aq(modc, "canonical", m, kFs=(15.0,)),
                 forest_proxy(growth_aq(modc, A0["canonical"], mode=m, KHg=KHF2, Dig=DIF2, zs_out=(2.0, 3.0)), kF=15.0, KHg=KHF2, REFg=REF_F2)[0])
             for m in MODES}
    P(f"    (H_S): L(z) = " + ", ".join(f"{zz}: {1e3 * Lh(1 / (1 + zz)):.0f}" for zz in (0.0, 0.25, 0.5, 1.0, 2.0, 2.5, 3.0)) + " kpc; y_th(z) = "
      + ", ".join(f"{zz}: {yh['canonical'](1 / (1 + zz)):.2e}" for zz in (0.0, 0.25, 0.5, 0.632, 1.0, 2.0, 2.5, 3.0)) + " (canonical)")
    P("      sigma_8/LCDM: " + ", ".join(f"{k_[0][:3]}/{k_[1]}: {v:.4f}" for k_, v in H["s8"].items())
      + "; forest " + ", ".join(f"{k_[0][:3]}/{k_[1]}: {v:.2g}" for k_, v in H["forest"].items())
      + "; flagship " + ", ".join(f"{k_[0][:3]} {k_[1]:.0e}: {v:+.4f}" for k_, v in H["flag"].items())
      + f"; SPARC {H['sparc']['canonical']:.1e}/{H['sparc']['alt']:.1e} dex; KiDS {H['kids']['canonical']:+.1f}/{H['kids']['alt']:+.1f}")
    P(f"      sigma_8 at rtol 1e-6 / 1e-8: " + ", ".join(f"{f[:3]} {v[0]:.5f}/{v[1]:.5f}" for f, v in h_conv.items())
      + "; forest 96 vs 144 k-points: " + ", ".join(f"{m}: {v[0]:.2e}/{v[1]:.2e}" for m, v in fconv.items()))
    h1_ok = H["all"] and all(abs(v[0] - v[1]) < 1e-3 for v in h_conv.values()) and all(max(v) <= FOREST_TOL for v in fconv.values())
    check("H1 THE STATE SEPARATOR (H_S) passes every linchpin gate on both footings: sigma_8 in [0.922, 1.05] (rms and per-mode), the "
          "forest proxy within 10% at k_F = 10, 15, 20 h/Mpc, the 1e10 and 1e11 flagships within 0.05 dex at z = 2.5, SPARC within "
          "0.01 dex, KiDS within +9 -- robust to the ODE tolerance and the k-grid -- with NO continuous constant declared (L_Lambda, n, "
          "y_Lambda, p' all replaced by state functionals)",
          gline(H) + f"; sigma_8 <= 1.02: {H['s8_tight']}", h1_ok,
          reading=f"the forest passes because at z >= {Z_Q0:.2f} the yield sits at the web's own band-passed rms (every linear web mode is "
                  f"below it); KiDS and SPARC pass because the yield is zero once the leaf accelerates (z < {Z_Q0:.3f}) and the band-pass "
                  f"length at z = 0.25 is the web's collapse scale ({Lh(0.8):.2f} Mpc)")
    OUT["numbers"]["H1"] = {"s8": js(H["s8"]), "forest": js(H["forest"]), "flag": js(H["flag"]), "sparc": H["sparc"], "kids": H["kids"],
                            "kids04": H["kids@0.4"], "kids07": H["kids@0.7"], "z1gal": js(H["z1gal"]), "s8_rtol": h_conv, "forest_conv": fconv,
                            "L_kpc": {str(zz): 1e3 * Lh(1 / (1 + zz)) for zz in (0.0, 0.25, 0.5, 1.0, 2.0, 2.5, 3.0)},
                            "yth": {str(zz): yh["canonical"](1 / (1 + zz)) for zz in (0.0, 0.25, 0.5, 0.632, 1.0, 2.0, 2.5, 3.0)}}

    # H2 E in the BPS window at every epoch
    ALC = (9.62e-14, 3.2e-9)
    xg = np.logspace(-9, math.log10(0.4999), 3000); Emin, Emax = 9.0, -1.0
    ymax = max(float(np.max(v)) for v in yh_tab.values())
    for yt in (0.0, 1e-6, 1e-3, ymax, 0.03):
        CT = (xg ** 2 / (1 - 2 * xg) + yt) / xg; CL = 2 * xg * (1 - xg) / (1 - 2 * xg) ** 2
        for Cv in (CT, CL):
            for hv in (1e-4, 0.3, 1.0):
                for av in ALC:
                    Ev = (2 * (2 - av) * hv ** 2 + 2 * av * Cv) / ((2 - av) * hv ** 2 + 2 * Cv)
                    Emin, Emax = min(Emin, float(Ev.min())), max(Emax, float(Ev.max()))
    jumps = max(abs(yh_tab["canonical"][i + 1] - yh_tab["canonical"][i]) for i in range(len(LNA) - 1))
    check("H2 E IN THE BPS WINDOW AT EVERY EPOCH: with the state yield y_th in [0, max] (both channels, band-pass gains 1e-4-1, both "
          "alpha_c ends) the khronon's E(C_phi, h) stays in [alpha_c, 2] -- no Hadamard band at any epoch; the ramp switch keeps the "
          f"yield continuous in time (the step variant jumps at z = {Z_Q0:.3f}, allowed: E is in the window on both sides)",
          f"E in [{Emin:.2e}, {Emax:.10f}]; y_th max {ymax:.2e}; largest step between table epochs {jumps:.1e}", Emax <= 2 + 1e-12 and Emin >= 0)

    # H3 the self-consistent matter feedback on the headline (nonlinear base x the running linear boost)
    h3_s8, h3_L = sc_run(HEAD_S, "matter", "NL", yfd=None, ysw=HEAD_SWITCH)
    Lsc3 = h3_L
    y_sc = {f: yh[f] for f in FOOTS}
    k3 = {f: kids_class(A0[f], Lsc3(0.8), y_sc[f](0.8), YIELD) - KB[f] for f in FOOTS}
    sp3 = {f: max(abs(law_dev_dex(Mv, A0[f], yv, Lsc3(1.0), y_sc[f](1.0), YIELD)) for Mv in (1e9, 1e10, 1e11, 1e12) for yv in (0.01, 0.03, 0.1, 1.0, 10.0, 100.0)) for f in FOOTS}
    P(f"    self-consistent (H_S): sigma_8 " + ", ".join(f"{k_[0][:3]}/{k_[1]} {v:.4f}" for k_, v in h3_s8.items())
      + f" | L_sc(0) = {Lsc3(1.0):.2f} (vs {Lh(1.0):.2f}), L_sc(0.25) = {Lsc3(0.8):.2f} (vs {Lh(0.8):.2f}) Mpc, L_sc(2.5) = {1e3 * Lsc3(1 / 3.5):.0f} kpc; "
      f"KiDS at L_sc {k3['canonical']:+.1f}/{k3['alt']:+.1f}; SPARC {sp3['canonical']:.1e}/{sp3['alt']:.1e}")
    h3_ok = all(SIG8_BAND[0] <= v <= SIG8_BAND[1] for v in h3_s8.values()) and max(k3.values()) <= KIDS_TOL and max(sp3.values()) <= SPARC_TOL
    check("H3 THE FEEDBACK IS MILD ON THE HEADLINE: re-reading L and y_th from the RUNNING state (the nonlinear spectrum times the "
          "sub-L MOND boost the separator itself produces, matter readout) moves L by the printed amount and keeps sigma_8, KiDS and "
          "SPARC inside their gates -- the headline is a fixed point, not a fine balance",
          f"sigma_8 max {max(h3_s8.values()):.4f}; L_sc(0.25)/L(0.25) = {Lsc3(0.8) / Lh(0.8):.3f}; KiDS {max(k3.values()):+.1f}; SPARC {max(sp3.values()):.1e}", h3_ok)
    OUT["numbers"]["H3"] = {"s8": js(h3_s8), "L0": Lsc3(1.0), "L025": Lsc3(0.8), "L25": Lsc3(1 / 3.5), "kids": k3, "sparc": sp3}

    # H4 (reported) the prices
    def flag_z(z, f="canonical"):
        return law_dev_dex(1e11, A0[f], 0.1, Lh(1 / (1 + z)), yh[f](1 / (1 + z)), YIELD)
    fz = {z: flag_z(z) for z in (2.5, 3.0, 3.5, 4.0, 5.0, 6.0)}
    try:
        zmax = brentq(lambda z: flag_z(z) + FLAG_TOL, 2.5, 6.0, xtol=1e-3)
    except ValueError:
        zmax = float("nan")
    gfr = M6["gfrac_smooth"]; lumps = {}
    for z in (2.0, 2.5, 3.0):
        Lz = Lh(1 / (1 + z)) * MPCm; yt = yh["canonical"](1 / (1 + z)); rhob = Om * rho_crit0 * (1 + z) ** 3
        for Rc in (0.1, 0.3, 1.0):
            sg_ = Rc / h / (1 + z) * MPCm
            for dl in (1.0, 3.0, 10.0):
                Ml = dl * rhob * (2 * math.pi) ** 1.5 * sg_ ** 3; r_ = np.geomspace(0.05, 5, 300) * sg_
                gN_ = G6 * Ml * gfr(r_ / sg_) / r_ ** 2
                gbp_ = G6 * Ml * (gfr(r_ / sg_) - gfr(r_ / math.sqrt(sg_ ** 2 + Lz ** 2))) / r_ ** 2
                lumps[(z, Rc, dl)] = float(np.max(x_P2(gbp_ / A0["canonical"] - yt) * A0["canonical"] / gN_))
    lumps_on = [k_ for k_, v in lumps.items() if v > 0]
    resh = growth_aq(modc, A0["canonical"], mode="permode", zs_out=(0.25,)); D_lc = growth_aq(M6["lcdm_model"](), A0["canonical"], mode="permode", zs_out=(0.25,))
    Pb = {zl: {kv: float(np.interp(kv, KH, (resh[zl] / D_lc[zl]) ** 2)) - 1.0 for kv in (0.1, 0.3, 0.5, 1.0)} for zl in (0.0, 0.25)}
    check("H4 (reported) THE PRICES OF (H_S): the flagship's MOND at 0.1 a0 survives to the printed z_max (the band-pass shortens "
          "into the past; the yield no longer runs away); the z = 2-3 IGM lumps against the web-rms yield; the linear P boost at "
          "sub-L scales -- the cosmic-shear risk FP9 flagged, LARGER here (the longer late-time L passes more sub-L modes); and TWO "
          "NEW PREDICTIONS the lead-grade gates do not see -- between "
          f"z = {Z_Q0:.2f} and ~3 galaxies lose their MOND below g ~ 1e-2 a0 (the yield is the web's rms), and galaxy-galaxy lensing of "
          f"lenses at z_l > {Z_Q0:.2f} loses its phantom beyond ~0.1-0.3 Mpc (KiDS-type chi^2 at z = 0.7); KiDS's own lenses (z <= 0.5) pass",
          f"z_max {zmax:.2f} (FP9's (H_Y): {F9['H2c']['zmax']['canonical']:.2f}); flagship(z) {', '.join(f'{z}: {v:+.3f}' for z, v in fz.items())}; lumps on {len(lumps_on)}/{len(lumps)}; "
          f"P boost z=0 k=0.3/0.5/1: {Pb[0.0][0.3]:+.3f}/{Pb[0.0][0.5]:+.3f}/{Pb[0.0][1.0]:+.3f} (FP9's (H_Y): {F9['H2c']['Pboost']['0.0']['0.3']:+.3f}/"
          f"{F9['H2c']['Pboost']['0.0']['0.5']:+.3f}/{F9['H2c']['Pboost']['0.0']['1.0']:+.3f}); z=1 galaxies y=0.1/0.03/0.01 (can): "
          f"{H['z1gal'][('canonical', 0.1)]:+.3f}/{H['z1gal'][('canonical', 0.03)]:+.3f}/{H['z1gal'][('canonical', 0.01)]:+.3f} dex; "
          f"KiDS@0.4 {max(H['kids@0.4'].values()):+.1f}, KiDS@0.7 {max(H['kids@0.7'].values()):+.0f}", True, load_bearing=False)
    OUT["numbers"]["H4"] = {"zmax": zmax, "flag_z": fz, "lumps": {f"{k_[0]}_{k_[1]}_{k_[2]}": v for k_, v in lumps.items()}, "Pboost": js(Pb)}

    # H5 (reported) the variants: the step switch; the linear-reading bracket at its natural-window threshold
    ystep, _, _ = yth_state(LH_tab, HEAD_READ, "step", 1.0)
    H5 = {"step": gates(Lh, ystep, extra=True)}
    Llin13 = L_table(1.3, "lin"); ylin13, _, _ = yth_state(Llin13, "lin", "ramp", 1.0)
    H5["linear reading, s = 1.3"] = gates(fun_of(Llin13), ylin13, extra=True)
    H5["FP9 (H_Y) itself"] = gates(L9, y9d, extra=True)
    for nm, r in H5.items():
        P(f"    {nm:26s}: {gline(r)}")
    check("H5 (reported) VARIANTS: the step switch passes as the ramp does; the linear reading needs s ~ 1.3 (its window) and then "
          "passes; FP9's own (H_Y) FAILS KiDS scored at z = 0.4 (its L(0.4) = 1.07 Mpc < 1.2): the lead grade's single lens redshift "
          "hid it",
          "; ".join(f"{nm}: five gates {'pass' if r['all'] else 'FAIL'}, KiDS@0.4 {max(r['kids@0.4'].values()):+.1f}" for nm, r in H5.items()), True, load_bearing=False)
    OUT["numbers"]["H5"] = {nm: {"all": r["all"], "kids04": r["kids@0.4"], "kids07": r["kids@0.7"]} for nm, r in H5.items()}
    P(f"    {el()}")

    # ============================================================================================= L  THE LOCAL GROUP
    banner("L  THE LOCAL GROUP: FP11's two-body timing and the merged-pair R0 under (H_S), both footings (2 workers)")
    lawd = {f: (LNA, LH_tab, yh_tab[f]) for f in FOOTS}
    MASSES = (1.145e11, 1.45e11, 1.75e11, 2.1e11, 2.4e11)
    jobs = [("control", "canonical", 1.45e11, None)] + [("HS", f, Mb, lawd[f]) for f in FOOTS for Mb in MASSES]
    P(f"    {len(jobs)} force tables (FP11's machinery, hooked to (H_S)'s L(a), y_th(a)); the main process waits  {el()}")
    with Pool(NPROC) as pool:
        res = pool.map(job_lg, jobs)
    ctrl = [r for r in res if r[0] == "control"][0]
    ref_ctrl = [p_ for p_ in F11["X1"]["1.3/canonical"]["pts"] if abs(p_[0] - 1.45e11) < 1e6][0][1]
    check("K4 CONTROL: FP11's committed two-body machinery (force table, Hubble-flow shooter), exec'd read-only and hooked to an "
          "arbitrary tabulated L(a)/y_th(a), reproduces FP11's committed X1 first-approach velocity with FP9's law restored",
          f"v_r(1.45e11, canonical) = {ctrl[3]:.4f} vs committed {ref_ctrl:.4f} km/s", abs(ctrl[3] - ref_ctrl) < 1e-6)
    ns11 = fp11()
    tm, r0t = {}, {}
    for f in FOOTS:
        pts = sorted((r[2], r[3]) for r in res if r[0] == "HS" and r[1] == f)
        P(f"    (H_S) {f:9s} first approach: " + ", ".join(f"{m_:.3g}: {v:+.1f}" for m_, v in pts) + " km/s")
        tm[f] = ns11["timing_mass"](pts)
        if tm[f]:
            hook11(ns11, lawd[f]); r0t[f] = ns11["lgR0_efe"](tm[f], A0[f], 0.0)
    hook11(ns11, None)
    r0m = lg_custom(Lh, yh); r0m9 = lg_custom(L9LG, y9LG)
    P(f"    timing masses (-109.3 km/s): " + ", ".join(f"{f}: {tm[f]:.3e}" if tm[f] else f"{f}: not bracketed" for f in FOOTS)
      + f"; R0 at them (merged pair): " + ", ".join(f"{f}: {r0t.get(f, float('nan')):.3f}" for f in FOOTS)
      + f" Mpc; FP11: 1.652e11 / 1.367e11 -> 1.505 / 1.500")
    P(f"    merged R0 at FP9's 1.145e11: (H_S) {r0m['canonical']:.3f}/{r0m['alt']:.3f} vs FP9 {r0m9['canonical']:.3f}/{r0m9['alt']:.3f} Mpc")
    inw = lambda m_: m_ is not None and 1.145e11 <= m_ <= 2.4e11
    check("L1 THE MW-M31 TIMING SURVIVES (H_S): on the chain's two-body law with the state separator the first approach reaches "
          "-109.3 km/s at a baryonic mass inside the window on both footings (no flyby, no dark halo) -- the pair's MOND is off until "
          "the ramp has nearly closed (z ~ 0.65: the pair's field at ~1 Mpc, ~4e-4 a0, lies far below the web-rms yield before) and "
          "the longer late-time band-pass makes up the difference",
          ", ".join(f"{f}: M_t = {tm[f]:.3e}" if tm[f] else f"{f}: none" for f in FOOTS), all(inw(tm[f]) for f in FOOTS))
    check("L2 THE LOCAL GROUP's R0 STILL FAILS (verified): at the timing mass the merged-pair zero-velocity radius is ~1.54 Mpc against "
          "0.96 +- 0.03 (edge 1.21) -- slightly WORSE than FP11's 1.50, because the state's band-pass is longer today (L(0) = 2.9 vs "
          "1.7 Mpc); R0 needs L(0.25) ~ 0.6 Mpc, which KiDS forbids and the web's nonlinear scale is not: reading the separator from "
          "the state does not touch the KiDS-LG pincer",
          ", ".join(f"{f}: {r0t.get(f, float('nan')):.3f} Mpc" for f in FOOTS) + f" (edge {LG_EDGE:.2f})",
          all(r0t.get(f, 0) > LG_EDGE for f in FOOTS))
    check("L3 (reported) the merged R0 at FP9's committed LG mass (1.145e11) under (H_S) vs FP9's (H_Y)",
          f"(H_S) {r0m['canonical']:.3f}/{r0m['alt']:.3f} vs (H_Y) {r0m9['canonical']:.3f}/{r0m9['alt']:.3f} Mpc", True, load_bearing=False)
    OUT["numbers"]["L"] = {"pts": {f: sorted((r[2], r[3]) for r in res if r[0] == "HS" and r[1] == f) for f in FOOTS}, "timing_mass": tm, "R0_timing": r0t,
                           "R0_merged_1145": r0m, "R0_merged_1145_FP9": r0m9, "control": ctrl[3]}
    P(f"    {el()}")

    # ============================================================================================= F  THE COUNT
    banner("F  THE CONSTANT COUNT: FP9's four declared constants against what the state now supplies")
    rows_f = [("L_Lambda (2.46 Mpc)", "the web's nonlinear scale: <(S_B delta_m)^2>_h = s^2", "ELIMINATED as a dimensional constant (A2, A3a)"),
              ("n (2)", f"the state's running: n_eff = {n_eff(Lfun[('NL', DELTA_C)]):.2f} (NL) / {n_eff(Lfun[('lin', DELTA_C)]):.2f} (lin)", "DERIVED (A2)"),
              ("y_Lambda (7.8e-8)", "the web's band-passed leaf-rms, coefficient 1", "ELIMINATED (D2; window of c_y printed)"),
              ("p' (4)", f"the sign of the leaf's deceleration q (Omega_L ~ 1/3, z = {Z_Q0:.3f})", "ELIMINATED (C1: no exponent works; C2)"),
              ("s = delta_c = 1.686", "spherical collapse (GR), applied to the actual field", "POSTULATED (natural; NL window, not lin)"),
              ("the matter readout D_i(a^i - D^i chi)", "the dynamical readout runs away", "CONSTRAINT (A4: forced)"),
              ("c_y = 1, the ramp max(0, 2q)", "no coefficient; continuous in time", "POSTULATED (natural; windows D2, C2)"),
              ("FP7's lambda", "phi needs an equation where the band-pass closes and the yield vanishes", "CONSTRAINT (lambda > 0, value free)")]
    for a_, b_, c_ in rows_f:
        P(f"    {a_:40s} {b_:66s} {c_}")
    P("    FP9 (H_Y): 4 declared continuous constants.  FP13 (H_S): 0 declared continuous constants; 3 postulated natural choices "
      "(s = delta_c, c_y = 1, the q = 0 ramp) and 1 forced readout; FP7's lambda from optional to required (> 0, any value).")
    P("    Unchanged elsewhere: kappa = 1/2 (FITTED), xi, alpha_c, c_2 (bounded), FP10's m (declared), eps (fitted), lambda_0, q (declared), the "
      "background inputs shared with LCDM (Omega_b h^2, the dark amount, h, n_s, A_s/sigma_8, tau).")
    check("F (reported) THE COUNT: the separator's four declared constants are replaced by three leaf-averaged state functionals "
          "(the web's collapse scale, its band-passed rms, the sign of the leaf's deceleration); what remains are O(1) postulated "
          "choices, each inside a measured window, chosen among natural candidates after scoring (look-elsewhere: threshold -- 1 of 2 "
          "natural values passes, and only in the nonlinear reading; onset -- of 4 natural conditions q = 0 passes in both readings, "
          f"E_MOND = E_kin in the nonlinear one only, the other two fail; level -- c_y = 1 inside [{min(cwin['NL'])}, {max(cwin['NL'])}] (NL) / "
          f"[{min(cwin['lin'])}, {max(cwin['lin'])}] (lin) of the scanned values)",
          "continuous declared: 4 -> 0; postulated natural choices: 3; forced constraints: 2 (matter readout, lambda > 0)", True, load_bearing=False)
    OUT["numbers"]["F"] = {"rows": rows_f}

    # ============================================================================================= W  THE LEDGER
    banner("W  THE LEDGER: FP13, the separator's scales from the action's state")
    LEDGER = [
        ("R13a", "DERIVED", "no length from (a0, c, G, Lambda, hbar, m, xi) has an Mpc size at natural exponents AND the web's running (n_eff >= 2); FP9's n = 2 form needs a declared acceleration a0 Z^-3.38", "S1 (dimension census); S2 numerology rates"),
        ("R13b", "POSTULATED", "the state-length form: B[state] with <(S_B delta_m)^2>_h = s^2 -- the heat branch read out on the matter density; a leaf average (no local variation), closed on exact FRW", "A1"),
        ("R13c", "DERIVED", "n eliminated: the web's nonlinear scale runs as Omega_L^(n_eff/2), n_eff = 2.06 (actual field) / 2.66 (linear), inside FP9's [2, 2.7]", "A2"),
        ("R13d", "CONSTRAINT", "the threshold window: nonlinear reading s in ~[1.3, 2.6], linear ~[1.1, 1.65]; delta_c inside the nonlinear only; s = 1 excluded (sigma_8)", "A3a-A3c, A6"),
        ("R13e", "FAILS", "the dynamical readout (D_i a^i, phantom included): the separator feeds on its own phantom; no threshold window", "A4"),
        ("R13f", "CONSTRAINT", "the matter readout D_i(a^i - D^i chi) is required, and its feedback is mild (the headline is a fixed point)", "A4, H3"),
        ("R13g", "FAILS", "the MOND-sector energy, the unsmoothed variance and the heat relaxation depth set no web length of their own", "A5"),
        ("R13h", "FAILS", "the dark field's scales at m >= 1.9e-19 eV: sub-kpc, n_eff <= 0.65, kernel-invisible (no coupling)", "B1"),
        ("R13i", "FAILS", "p' as a power of any state measure: the yield's 3.1-decade rise exceeds every measure's (<= 1 decade) without a declared exponent and normalisation", "C1"),
        ("R13j", "FAILS", "y_th at the web's rms alone: 3-3.8 decades above KiDS's ceiling (KiDS +870..+1200, SPARC)", "D1"),
        ("R13k", "POSTULATED", "the state yield y_th = <|g_bp|^2>_h^(1/2)/a0 x max(0, 2q): the web's own rms while the leaf decelerates (c_y = 1, ramp)", "C2, D2"),
        ("R13l", "DERIVED", "(H_S) passes sigma_8, the forest proxy, the flagship, SPARC and KiDS on both footings and modes; E in the BPS window at every epoch", "H1, H2, H3"),
        ("R13m", "CONSTRAINT", "FP7's lambda > 0 is required at exact zero field (band-pass closed and yield zero on FRW); its value is free", "A1"),
        ("R13n", "DERIVED", "the MW-M31 timing with baryons only survives (H_S) on both footings", "L1, K4"),
        ("R13o", "FAILS", "the Local Group's R0 ~1.54 Mpc (edge 1.21): the state band-pass is longer today; the KiDS-LG pincer is untouched", "L2"),
        ("R13p", "POSTULATED", "the remaining choices: s = delta_c (a GR number applied to the actual field), c_y = 1, the q = 0 ramp -- natural, windowed, chosen after scoring", "F"),
        ("R13q", "OPEN", "the nonlinear reading rests on halofit LCDM, not a PM run of this theory, and on halos staying LCDM-like (FP10's clearing thins them: the five gates hold to 20% of LCDM's one-halo power, the z = 0.4 lens check to ~45%: A7); lensing of lenses at z_l > 0.64 and galaxies below ~1e-2 a0 at 0.64 < z < 3 (new predictions); KiDS beyond lead grade (lens-z spread, 2-halo); the Local Group", "A7, H4, H5, L2"),
    ]
    for lk_, st, wh, ba in LEDGER:
        P(f"    {lk_:6s} {st:11s} {wh}  --  {ba}")
        OUT["ledger"].append({"link": lk_, "what": wh, "status": st, "basis": ba})
    check("W (reported) the ledger", f"{len(LEDGER)} links", True, load_bearing=False)
    check("G (reported) G-1 passed WHOLE (the linchpin's gates AND the Local Group)",
          "no: (H_S) meets sigma_8, forest, flagship, SPARC and KiDS with no declared continuous constant, but the LG gives R0 = "
          + ", ".join(f"{r0t.get(f, float('nan')):.2f}" for f in FOOTS) + " Mpc", False, load_bearing=False)

    # ============================================================================================= VERDICT
    nlb = sum(1 for _, ok, lb in CH if lb and not ok)
    banner("VERDICT")
    P("  (a) The band-pass length IS supplied by the state: the heat branch read out on the matter density, <(S_B delta_m)^2>_h = s^2,")
    P(f"      gives the web's collapse scale, L(0.25) = {Lh(0.8):.2f} Mpc and L(2.5) = {1e3 * Lh(1 / 3.5):.0f} kpc at s = delta_c on the actual field, running as")
    P(f"      Omega_L^(n_eff/2) with n_eff = {n_eff(Lh):.2f} -- FP9's n = 2 is what the web does anyway (n DERIVED, L_Lambda ELIMINATED).  The")
    P("      threshold is a postulated natural number: delta_c passes in the nonlinear reading, not in the linear one; s = 1 fails;")
    P("      and the nonlinear reading needs halos that stay roughly LCDM-like: the five gates hold down to 20% of LCDM's one-halo")
    P("      power, the z = 0.4 lens check to ~45% (FP10's clearing thins them to ~35-45%, crude: A7).")
    P("      The readout must be the MATTER density: read with its own phantom the separator runs away (no window).")
    P("  (b) The dark field's lengths are sub-kpc at m >= 1.9e-19 eV, run wrongly and are invisible to the MOND sector: FAIL.")
    P("  (c) n: derived (a).  p': no power of any state measure rises the 3.1 decades the yield needs; a SIGN CHANGE does -- the")
    P(f"      leaf's deceleration q = 0 at z = {Z_Q0:.3f} -- with no exponent.  The other onsets fail or depend on the reading.")
    P("  (d) The web's rms field is 3-3.8 decades above KiDS's yield ceiling: alone it FAILS; switched off once the leaf accelerates it")
    P("      passes, with coefficient 1.")
    P(f"  (H_S) passes sigma_8 {min(H['s8'].values()):.3f}-{max(H['s8'].values()):.3f} (inside the 1.05 band; 1.02 tight: {H['s8_tight']}), the forest proxy, the flagship,")
    P("      SPARC and KiDS on both footings with NO")
    P("      declared continuous constant (4 -> 0); three natural choices remain postulated (delta_c, c_y = 1, the q = 0 ramp) and FP7's")
    P(f"      lambda becomes required (> 0, any value).  Prices: galaxies at {Z_Q0:.2f} < z < 3 lose MOND below ~1e-2 a0; lenses at z_l > {Z_Q0:.2f}")
    P("      lose their phantom beyond ~0.1-0.3 Mpc; the sub-L linear P boost is larger than FP9's (the cosmic-shear risk grows).")
    P("      The MW-M31 timing survives; the Local Group's R0 still FAILS (~1.54 Mpc).")
    P(f"  Not 'closed'.  Time {time.time() - T0:.0f} s.")
    OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
    fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
    json.dump(OUT, open(fn, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating, np.integer)) else str(o)))
    P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}")
    sys.exit(0 if nlb == 0 else 1)


if __name__ == "__main__":
    main()
