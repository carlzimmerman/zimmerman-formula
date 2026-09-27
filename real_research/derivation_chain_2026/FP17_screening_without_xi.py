#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FP17 -- SCREENING WITHOUT xi: can the Solar System be screened with NO new constant?  The heat-filter length xi is the
gravity core's last knob (FP14).  This lane asks whether a screening with a SELF-GENERATED scale (Vainshtein / k-mouflage),
a scale the theory already has (the dark field's mass m), or a curvature-keyed readout can replace it -- and proves what
none of them can do without a new constant.  kappa = 1/2 is the one accepted fitted input.

WHY.  FP14 left the core as
  R - 2 Lambda + alpha_c a^2 - 2 mu (K - <K>_h) + (2 - alpha_c) h^mn (2 a_m - D_m chi) D_n chi - 2 alpha^2 J_Y(Y) + heat pair
  (chi = S_h phi, b = xi^2/2) + S_m[g],      a0 = kappa c sqrt(G rho_DE),
with xi bounded to [0.0243 / 0.0268 pc, ~100 pc]: not derivable (X1), no field-dependent form (X2-X3b), not removable by a
kernel change (X5).  The goal is ZERO KNOBS.  Three routes are tried and every gate is scored, both a0 footings.

THE RECORD (searched first; kills cited, not re-proposed): route2_vainshtein_kmouflage_2026.py (5ba86489b: the cubic Galileon on
the a0-line kernel -- universal R_*, the 1-AU monopole untouched, 'anti-synergistic'); REALIZATION_REDTEAM_galileon_singular_
surface (one-field DE+MOND+Vainshtein: singular-surface ghost); DC-015/DC-018 (Galileon as the MOND carrier: dead class);
FC-KH (fc_kh_terminal: gradient instability; the Cassini-vs-ghost pincer); CCNL (dead at gate 7, c_T, KiDS); DC-008 (curvature-
ratio CCG: Ostrogradsky); Case 3a (curvature-coupled clock: c_T excluded 1e7-1e9x); york/L_CLOSURE_VERDICT (Theorem 8: r_M
is not a local functional of rho -- a precise no-go); york/ESCREEN_Q2_VERDICT (external-field screen: threshold FITTED, the
wide-binary lock relabelled); kappa_closure/k04 (four-form self-switch screens the monopole, not Q2: 'xi is still required');
ONE_NEW_THING_2026-09-04 (hbar/(xi c) = 2e-22 eV 'recorded as a coincidence, nothing more').

WHAT IS NEW HERE
  M  THE THRESHOLD-MASS THEOREM.  The strict law's Cassini Q2 is generated at 1700-7300 AU from the Sun (total y_N 1.7-22):
     a 1-Msun system at its own EFE transition.  For an isolated point source the only local invariants are y = GM/(r^2 a0),
     C = GM/(r c^2) and Lambda c^4/a0^2 = 8 pi/kappa^2 (Buckingham), so at fixed y a field-strength or curvature key can tell
     the Sun from a galaxy only through C ~ M^(1/2): every such screening needs a threshold MASS M_* between ~1 Msun and the
     lightest SPARC enclosed mass at the same y.  (a0, Lambda, G, c) supply only (c^4/G a0)(8 pi/kappa^2)^D -- the window
     needs D ~ -9..-12: numerology.  Each route's M_* is computed: the self-generated ones sit >= 13 decades above the window.
     (Keys on the EXTERNAL field are outside the theorem: relational, fitted in the record -- C5.)
  V  (a) Vainshtein / k-mouflage: the cubic Galileon's Vainshtein radius with r_c = c/H_Lambda (the '~70 kpc' estimate is low);
     the cubic Galileon on the chain's P2 k-mouflage (Route 2's reduction, re-derived on the AQUAL root: empty window for ANY
     R_*); BDEF 2011's Riemann-coupled Galileon (Phys. Rev. D 84, 061502(R), arXiv:1106.2538 -- verified, its eq. 8-9 and its
     numbers reproduced) on P2: mass-dependent r_V = (8 k G M a0)^(1/4)/c, which beats P2's pole; with k^(1/4) from the
     framework (c/H) galaxies are screened; with k fitted it REPLACES xi (a window, a new constant).
  B  (b) the dark field's mass: hbar/(m v) verified; the unique c-free length ((hbar/m)^2/a0)^(1/3); a state coupling in FP10's
     cleared galaxies; a parameter tie.
  C  (c) curvature keys: density (Ricci) keys, tidal (Weyl) keys and their length, and the second variation of a curvature-
     keyed readout depth (FP14 X3b at one more derivative: a gradient instability for any unsaturated key).
  R  the best candidates re-scored on every gate (Solar System, SPARC, KiDS, flagship, c_T, PPN, FRW/sigma_8, readout force,
     stability).

CHECKS
  K  CONTROLS: K1 SPARC (P2 profiled 0.1083 / 0.1035, Newtonian 0.2755) and KiDS (P2 110.6 / 102.4, Newtonian 1230) as FP14;
     K2 FP7's committed AQUAL Solar-System table and its floor re-interpolated; K3 the direct QUMOND quadrupole (FP14's
     dblquad, exec'd) and this lane's cumulative version reproduce FP14 X5's committed P2 Q2; K4 BDEF 2011 eq. (8) -> (9), its
     three regimes, r_V, k ~ (100 kpc)^4 and the '(r/22 AU)^4' ratio; K5 Route 2's reduction (universal R_*) and its monopole floor
     1.373e6 / 1.654e6 Mpc; K6 the unitary-gauge block with a first-order readout reproduces FP14 X3b; K7 FP9's (H_Y) sigma_8.
  M  M1 where Q2 is generated; M2 the (y, C) gap from SPARC + the Buckingham reduction; M3 masses from (a0, Lambda, G, c);
     M4 the threshold mass of every route.
  V  V1 cubic Galileon r_V; V2 cubic Galileon on P2; V3 BDEF on P2, framework k; V4 (reported) BDEF with k fitted.
  B  B1 de Broglie; B2 lengths from (hbar/m, a0, c); B3 the state coupling; B4 (reported) the parameter tie.
  C  C1 density keys; C2 tidal keys; C3 the curvature-keyed readout's second variation; C4 (reported) c_T / PPN; C5 (reported)
     external-field keys (outside theorem M).
  R  R1 the best constant-free candidate on every gate; R2 (reported) the xi_q tie on every gate.   F count.   W ledger.
MUTATE=1 gives the 'constant-free' Galileon a FITTED coupling k^(1/4) = 100 kpc (BDEF's own value) in place of c/H: its galaxies
are then no longer screened, so the load-bearing kills M4, V3 and R1 must FAIL (rc = 1).

SCOPE.  Static weak-field reductions (spherical fluxes; the chain's spherical SPARC and point-lens KiDS statistics), the
record's Solar-System machinery reused read-only, frozen-coefficient linear stability.  No particle-mesh run.  The c_T of the
Riemann-coupled Galileon on a static gradient is an ESTIMATE (reported, not load-bearing).  Nothing here edits another file.

Run from the repository root:  python3 real_research/derivation_chain_2026/FP17_screening_without_xi.py
"""
import os, re, io, sys, json, math, time, warnings, contextlib
warnings.filterwarnings("ignore")
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations
from scipy import integrate
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "FP17_screening_without_xi" + ("_MUTATE" if MUTATE else "")
OUT = {"lane": "FP17", "mutate": MUTATE, "root": "FP14's gravity core (FP7's AQUAL root at lambda = 0, c_2 -> oo; FP9's separator above it)",
       "checks": {}, "numbers": {}, "ledger": []}
CH = []
T0 = time.time()


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)


def check(name, measured, ok, load_bearing=True, reading=None):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def el():
    return f"[{time.time() - T0:.0f} s]"


def load_json(name):
    try:
        return json.load(open(os.path.join(HERE, name)))
    except Exception:
        return None


def exec_quiet(src, path, ns):
    old = os.environ.get("MUTATE")
    os.environ["MUTATE"] = "0"
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src, path, "exec"), ns)
    finally:
        if old is None:
            os.environ.pop("MUTATE", None)
        else:
            os.environ["MUTATE"] = old
    return ns


P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the 'constant-free' Galileon is given a FITTED k^(1/4) = 100 kpc -- M4, V3 and R1 must FAIL ***")

# ============================================================================================================== inputs
cc, Gn, PC_M, AU_M, MSUN = 299792458.0, 6.67430e-11, 3.0856775814913673e16, 1.495978707e11, 1.98847e30
GM_SUN = 1.32712440018e20
KPC, MPC = 1e3 * PC_M, 1e6 * PC_M
HBARC = 1.973269804e-7                                          # eV m
MP_C2 = 938.27208816e6                                          # eV (proton)
fp0, fp7, fp9, fp10, fp14 = (load_json(n) for n in ("FP0_core_postulates_results.json", "FP7_aqual_type_repair_results.json",
                                                    "FP9_web_galaxy_separator_results.json", "FP10_internal_splitting_dark_sector_results.json",
                                                    "FP14_zero_knob_core_results.json"))
A0 = {"canonical": fp0["numbers"]["a0_canonical"], "alt": fp0["numbers"]["a0_rho_total"]}
OMEGA_L = 0.6847                                                # Planck 2018, the chain's input (FP0/FP1)
H_FOOT = {"canonical": fp0["numbers"]["H_Lambda"]}              # the footing's own H: rho_Lambda -> H_Lambda, rho_total -> H_0
H_FOOT["alt"] = H_FOOT["canonical"] / math.sqrt(OMEGA_L)
KAPPA = 0.5
XI_FLOOR = {f: fp7["numbers"]["A4"]["AQUAL_floors"][f]["floor"] for f in ("canonical", "alt")}
XI_CEIL_PC = 100.0
FP7_TAB = fp7["numbers"]["A4"]["table_2p32"]                    # FP7 A4's committed AQUAL double-filter table at g_ext = 2.32e-10
RETAINED = fp10["numbers"]["B2"]["retained"]                    # FP10's cleared-galaxy fractions (in place, pessimistic reading)
M_DARK = (1.9e-19, 5.2e-19)                                     # eV: FP4 L10f / FP10's floor on the dark field's mass
V_KICK = (575e3, 650e3)                                         # FK1's kick window (FP10)
V_DISP = (200e3, 600e3)                                         # the task's velocity range for hbar/(m v)
A_SUNWARD = 0.5 * 9.36e-11 / 1278.0                             # g02 / FP14: the ephemeris gate on a constant sunward acceleration
M_SAT_BOUND, R_SAT = 6.7e-11 * MSUN, 9.54 * AU_M                # g02: Pitjev-Pitjeva monopole inside Saturn's orbit
Q2_CEIL = 5.2e-27                                               # Park 2026 two-sigma ceiling (FP1/FP14)
G_EXT = (2.00e-10, 2.32e-10, 2.64e-10)
RHO_B_LOCAL = 0.10                                              # Msun/pc^3, the repo's Oort-limit input (FP14 X3)
MSUN_PC3 = MSUN / PC_M ** 3
PLANETS = {"Mercury": 0.387, "Earth": 1.0, "Mars": 1.524, "Jupiter": 5.203, "Saturn": 9.54}
FLAG_TOL_FP10 = 0.074                                           # FP10's flagship gate (AT1's A2 pass level)
ELL_FREE = {f: cc / H_FOOT[f] for f in A0}                      # the self-generated Galileon length c/H of the footing
if MUTATE:
    ELL_FREE = {f: 100.0 * KPC for f in A0}
P(f"\n  inputs: a0 = {A0['canonical']:.4e} / {A0['alt']:.4e} m/s^2 (FP0); H = {H_FOOT['canonical']:.4e} / {H_FOOT['alt']:.4e} 1/s "
  f"(c/H = {cc / H_FOOT['canonical'] / MPC / 1e3:.3f} / {cc / H_FOOT['alt'] / MPC / 1e3:.3f} Gpc); xi floors {XI_FLOOR['canonical']:.4f} / "
  f"{XI_FLOOR['alt']:.4f} pc (FP7 A4), ceiling ~{XI_CEIL_PC:.0f} pc; gates: sunward {A_SUNWARD:.3e} m/s^2, Saturn monopole 6.7e-11 Msun, "
  f"Q2 {Q2_CEIL:.1e} s^-2; dark mass >= {M_DARK[0]:.1e}-{M_DARK[1]:.1e} eV (FP10)")


def nu_p2(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return np.sqrt(1.0 + 1.0 / y)


def x_p2(y):
    """P2's AQUAL scalar (units a0) in spherical symmetry: x^2/(1 - 2x) = y."""
    y = np.maximum(np.asarray(y, float), 0.0)
    return np.where(y > 0, 1.0 / (1.0 + np.sqrt(1.0 + 1.0 / np.maximum(y, 1e-300))), 0.0)


def x_screened(y, rho, nit=64):
    """the scalar (units a0) of P2's k-mouflage plus a Galileon flux: x^2/(1 - 2x) + rho x^2 = y (rho = R_*/r for the cubic
    Galileon, (r_V/r)^4 for BDEF's Riemann coupling).  Route 2's bisection in log w, x = 1/(2(1 + w)): full precision at both ends."""
    Y = np.asarray(y, float)
    RHO = np.asarray(rho, float)
    Y, RHO = np.broadcast_arrays(Y, RHO)
    lo = np.full(Y.shape, -300.0)
    hi = np.full(Y.shape, 300.0)
    for _ in range(nit):
        L = 0.5 * (lo + hi)
        w = 10.0 ** L
        F = 0.25 / (w * (1.0 + w)) + 0.25 * RHO / (1.0 + w) ** 2 - Y
        lo = np.where(F > 0, L, lo)
        hi = np.where(F > 0, hi, L)
    return 0.5 / (1.0 + 10.0 ** (0.5 * (lo + hi)))


def rho_bdef(k, a0, gN, r):
    """(r_V/r)^4 of BDEF's Riemann-coupled Galileon for the enclosed mass: 8 k G M(<r) a0/(c^4 r^4) = 8 k a0 g_N/(c^4 r^2)."""
    return 8.0 * k * a0 * gN / (cc ** 4 * r ** 2)


# ============================================================================================================== K controls
banner("K  CONTROLS: the reused machinery reproduces the record")
# ---- K1: SPARC (FP1 C / FP14 K5's statistic, vectorised over the Upsilon grid) and KiDS (FP1 E's copy of L355, exec'd)
KPC_S = 3.0857e19
DATA = os.path.join(REPO, "real_research", "data", "sparc_data")
GAL = []
for fn in sorted(os.listdir(DATA)):
    if not fn.endswith("_rotmod.dat"):
        continue
    try:
        d_ = np.genfromtxt(os.path.join(DATA, fn), comments="#")
    except Exception:
        continue
    if d_.ndim != 2 or d_.shape[1] < 6:
        continue
    GAL.append(tuple(d_[:, i] for i in range(6)))
UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2)
_R = np.concatenate([g_[0] for g_ in GAL]) * KPC_S
_Vo = np.concatenate([g_[1] for g_ in GAL])
_eV = np.concatenate([g_[2] for g_ in GAL])
_Vg, _Vd, _Vb = (np.concatenate([g_[i] for g_ in GAL]) for i in (3, 4, 5))
VB2 = np.sign(_Vg)[:, None] * _Vg[:, None] ** 2 + UPS[None, :] * _Vd[:, None] ** 2 + 1.4 * UPS[None, :] * _Vb[:, None] ** 2
GB = VB2 * 1e6 / _R[:, None]
GO = ((_Vo * 1e3) ** 2 / _R)[:, None] * np.ones_like(GB)
OKS = (GB > 0) & (GO > 0) & np.isfinite(GB) & (_Vo > 0)[:, None]
WW = np.where(OKS, (1.0 / (np.clip(_eV, 1, None) / np.clip(_Vo, 1, None)) ** 2)[:, None], 0.0)
RR = _R[:, None] * np.ones_like(GB)


def sparc_best(model, a0):
    """FP1 C's statistic: weighted rms of log g_obs - log g_model over all points, Upsilon profiled on 0.30-1.20."""
    gbs = np.where(OKS, GB, 1.0)
    gm = model(gbs, RR, a0)
    r_ = np.where(OKS, np.log10(np.where(OKS, GO, 1.0)) - np.log10(gm), 0.0)
    mse = (WW * r_ * r_).sum(0) / WW.sum(0)
    i = int(np.argmin(mse))
    return math.sqrt(mse[i]), float(UPS[i])


SP_P2 = {f: sparc_best(lambda gb, R, a0: nu_p2(gb / a0) * gb, A0[f]) for f in A0}
SP_N = {f: sparc_best(lambda gb, R, a0: gb, A0[f]) for f in A0}
src1 = open(os.path.join(HERE, "FP1_static_sector.py")).read()
GK = {"np": np, "math": math, "os": os, "REPO": REPO, "G_SI": Gn, "_trap": getattr(np, "trapezoid", None) or np.trapz}
exec(compile(src1[src1.index("# ---- KiDS: L355's machinery"):src1.index("w0 = np.zeros(len(ES)); w0[0] = 1.0")],
             os.path.join(HERE, "FP1_static_sector.py"), "exec"), GK)
W0K = np.zeros(len(GK["ES"]))
W0K[0] = 1.0


def kids_isolated(nu_eff):
    """FP1 E / L355's isolated-lens chi^2 (M_b profiled per bin, no 2-halo); nu_eff(y, r, Mb, a0) may depend on r (screening)."""
    out = {}
    for foot, a0 in A0.items():
        T = np.zeros((len(GK["ES"]), len(GK["LM"]), 4, GK["npb"]))
        for im, lm in enumerate(GK["LM"]):
            Mb = 10 ** lm * GK["MS"]
            y = Gn * Mb / GK["rrK"] ** 2 / a0
            dS = GK["esd_of_M"](Mb * nu_eff(y, GK["rrK"], Mb, a0), Mb)
            T[0, im] = [np.interp(GK["Rd"][b], GK["Rp"] / GK["MPCm"], dS) for b in range(4)]
        out[foot] = GK["kfit"]({foot: T}, foot, W0K, 0.0)[0]
    return out


KI_P2 = kids_isolated(lambda y, r, Mb, a0: nu_p2(y))
KI_N = kids_isolated(lambda y, r, Mb, a0: np.ones_like(np.asarray(y, float)))
ref_sp = fp14["numbers"]["X5"]["sparc"]["P2"]
ref_n = fp14["numbers"]["X2"]
k1_ok = (all(abs(SP_P2[f][0] - ref_sp[f]) < 1e-4 for f in A0) and all(abs(SP_N[f][0] - ref_n["sparc_newton"][f][0]) < 1e-4 for f in A0)
         and abs(KI_P2["canonical"] - 110.6) < 0.1 and abs(KI_P2["alt"] - 102.4) < 0.1
         and all(abs(KI_N[f] - ref_n["kids_newton"][f]) < 0.1 for f in A0))
check("K1 CONTROL: this lane's vectorised copy of FP1's SPARC statistic and FP1 E's KiDS-1000 machinery (exec'd read-only) "
      "reproduce FP14's committed numbers -- P2 profiled 0.1083 / 0.1035 dex, Newtonian 0.2755; KiDS isolated P2 110.6 / 102.4, "
      "Newtonian 1230.3",
      f"SPARC P2 {SP_P2['canonical'][0]:.4f} (U {SP_P2['canonical'][1]:.2f}) / {SP_P2['alt'][0]:.4f} (U {SP_P2['alt'][1]:.2f}); Newtonian "
      f"{SP_N['canonical'][0]:.4f}; KiDS P2 {KI_P2['canonical']:.1f} / {KI_P2['alt']:.1f}, Newtonian {KI_N['canonical']:.1f} / {KI_N['alt']:.1f} "
      f"({len(GAL)} galaxies)", k1_ok)

# ---- K2: FP7 A4's committed AQUAL Solar-System table, log-interpolated in xi
XI_TAB = {f: np.array([r_["xi"] for r_ in FP7_TAB[f]]) for f in FP7_TAB}


def fp7_gate(xi_pc, gate, foot="canonical"):
    """FP7 A4's AQUAL (double filter, g_ext = 2.32e-10) gate value at xi, log-log interpolated; clipped to the table's range."""
    xs = XI_TAB[foot]
    vs = np.array([max(r_["A"][gate], 1e-12) for r_ in FP7_TAB[foot]])
    xq = float(np.clip(xi_pc, xs[0], xs[-1]))
    return float(np.exp(np.interp(math.log(xq), np.log(xs), np.log(vs))))


fl_M = {f: brentq(lambda lx: math.log(fp7_gate(math.exp(lx), "M", f)), math.log(0.012), math.log(0.09)) for f in ("canonical", "alt")}
ref_M = {f: fp7["numbers"]["A4"]["AQUAL_floors"][f]["per"]["2.32"]["M"] for f in ("canonical", "alt")}
check("K2 CONTROL: FP7 A4's committed AQUAL double-filter table (g_ext = 2.32e-10) is read and this lane's log-log interpolation "
      "reproduces FP7's committed Saturn-monopole floor at that field (the binding gate) to < 1%",
      f"monopole floor {math.exp(fl_M['canonical']):.5f} / {math.exp(fl_M['alt']):.5f} pc vs committed {ref_M['canonical']:.5f} / {ref_M['alt']:.5f}",
      all(abs(math.exp(fl_M[f]) / ref_M[f] - 1) < 0.01 for f in fl_M))

# ---- K3: the direct QUMOND quadrupole (FP14's f28 integral, exec'd from FP14's source) and this lane's cumulative version
src14 = open(os.path.join(HERE, "FP14_zero_knob_core.py")).read()
N14 = {"np": np, "math": math, "integrate": integrate, "brentq": brentq}
exec(compile(src14[src14.index("def solve_eN(nu, et):"):src14.index("def nu_p2(y):")], os.path.join(HERE, "FP14_zero_knob_core.py"), "exec"), N14)
q_direct2D, solve_eN, PREF = N14["q_direct2D"], N14["solve_eN"], N14["PREF"]
MU_G = np.linspace(-1.0, 1.0, 2001)
V_G = np.concatenate([np.linspace(0.0, 0.05, 60, endpoint=False), np.geomspace(0.05, 400.0, 6000)])


def q2_cumulative(nu, et):
    """the f28 integrand integrated over mu at each v = r_M/r (the Sun's Newtonian field is v^2 a0), then cumulatively in v."""
    eN = solve_eN(nu, et)
    F = np.empty(len(V_G))
    for i, v in enumerate(V_G):
        D = eN * eN + v ** 4 + 2 * eN * v * v * MU_G
        nv = nu(np.sqrt(np.maximum(D, 1e-300)))
        F[i] = np.trapz((nv - 1.0) * (eN * (3 * MU_G - 5 * MU_G ** 3) + v * v * (1 - 3 * MU_G ** 2)), MU_G)
    cum = integrate.cumulative_trapezoid(F, V_G, initial=0.0)
    return eN, cum


Q2C = {}
for f, a0 in A0.items():
    for ge in G_EXT:
        eN, cum = q2_cumulative(nu_p2, ge / a0)
        Q2C[(f, ge)] = dict(eN=eN, cum=cum, q2=abs(1.5 * cum[-1]) * PREF(a0) / Q2_CEIL)
ref_q2 = fp14["numbers"]["X5"]["q2"]["P2"]                            # FP14 X5 integrated to v = 100 (r >= r_M/100)
q2_at100 = {(f, ge): abs(1.5 * float(np.interp(100.0, V_G, d2["cum"]))) * PREF(A0[f]) / Q2_CEIL for (f, ge), d2 in Q2C.items()}
dev_q2 = max(abs(q2_at100[(f, ge)] / ref_q2[f][i] - 1) for f in A0 for i, ge in enumerate(G_EXT))
q_dbl = q_direct2D(nu_p2, 2.32e-10 / A0["canonical"], 100.0) * PREF(A0["canonical"]) / Q2_CEIL
tail400 = max(abs(Q2C[k2]["q2"] / q2_at100[k2] - 1) for k2 in Q2C)
check("K3 CONTROL: FP14's direct QUMOND quadrupole (f28's dblquad, exec'd from FP14's source) and this lane's cumulative "
      "(trapezoid-in-mu, cumulative-in-v) version reproduce FP14 X5's committed strict P2 Q2/ceiling on both footings and all three "
      "Galactic fields (canonical 3.99 / 4.48 / 4.93, alt 4.53 / 5.13 / 5.68; X5 integrates to v = r_M/r = 100)",
      f"cumulative at v = 100: " + ", ".join(f"{f[:3]} {q2_at100[(f, ge)]:.3f}" for f in A0 for ge in G_EXT) + f"; max dev {dev_q2:.1e}; dblquad "
      f"(canonical, 2.32e-10) {q_dbl:.4f} vs committed {ref_q2['canonical'][1]:.4f}; extending to v = 400 moves Q2 by <= {tail400:.1e}",
      dev_q2 < 2e-3 and abs(q_dbl / ref_q2["canonical"][1] - 1) < 1e-4 and tail400 < 5e-3)

# ---- K4: BDEF 2011 (Phys. Rev. D 84, 061502(R); arXiv:1106.2538), eq. (8) -> eq. (9), regimes, r_V, numbers
r_, k_, M_, a0s, cs, eps_, Gs = sp.symbols('r k M a_0 c epsilon G', positive=True)
dphi = sp.Symbol("phi_p", positive=True)
rs_ = 2 * Gs * M_ / cs ** 2
eq8 = 4 * k_ * rs_ / r_ ** 2 * dphi ** 2 + r_ ** 2 * cs ** 2 / a0s * dphi ** 2 + eps_ * r_ ** 2 * dphi - rs_ / 2
eq9 = 1 / (sp.sqrt(8 * k_ / r_ ** 2 + r_ ** 2 * cs ** 4 / (Gs * M_ * a0s) + (eps_ * r_ ** 2 / rs_) ** 2) + eps_ * r_ ** 2 / rs_)
k4_sol = sp.simplify(eq8.subs(dphi, eq9))
if k4_sol != 0:                                                       # sympy may not close the nested roots: check numerically
    rng = np.random.default_rng(17)
    k4_num = max(abs(float((eq8.subs(dphi, eq9) / (rs_ / 2)).subs({r_: 10 ** rng.uniform(-2, 2), k_: 10 ** rng.uniform(-3, 3), M_: 10 ** rng.uniform(-1, 1),
                                                                    a0s: 10 ** rng.uniform(-1, 1), cs: 10 ** rng.uniform(-0.5, 0.5),
                                                                    eps_: 10 ** rng.uniform(-3, 0), Gs: 10 ** rng.uniform(-1, 1)}).evalf(30)))
                 for _ in range(20))
    k4_sol = 0 if k4_num < 1e-20 else k4_num
eq9_0 = eq9.subs(eps_, 0)
lim_small = sp.limit(eq9_0 / r_, r_, 0)                               # -> 1/sqrt(8k)
lim_mond = sp.simplify(sp.limit(eq9_0.subs(k_, 0) * r_ * cs ** 2, r_, sp.oo))   # -> sqrt(G M a0)
lim_bd = sp.simplify(sp.limit(eq9 * r_ ** 2, r_, sp.oo))                # -> G M/(eps c^2)
rV_sym = sp.solve(sp.diff(8 * k_ / r_ ** 2 + r_ ** 2 * cs ** 4 / (Gs * M_ * a0s), r_), r_)
rV_ok = any(sp.simplify(s_ ** 4 - 8 * k_ * Gs * M_ * a0s / cs ** 4) == 0 for s_ in rV_sym)
a0_B = 1.2e-10
k_B14 = 4e-6 * cc ** 2 / a0_B                                         # BDEF eq. (6): k^(1/4) = 4e-6 c^2/a0
k_B14b = (Gn * 1e3 * MSUN * cc ** 4 / (8 * a0_B ** 3)) ** 0.25          # k = G (1e3 Msun) c^4/(8 a0^3)
r22 = (2 * k_B14 ** 4) ** 0.125 * math.sqrt(2 * GM_SUN / cc ** 2)       # (r^2/r_s)^2/sqrt(2k) = (r/r22)^4
k4_ok = (sp.simplify(k4_sol) == 0 and sp.simplify(lim_small - 1 / sp.sqrt(8 * k_)) == 0 and sp.simplify(lim_mond - sp.sqrt(Gs * M_ * a0s)) == 0
         and sp.simplify(lim_bd - Gs * M_ / (eps_ * cs ** 2)) == 0 and rV_ok
         and abs(k_B14 / KPC / 100 - 1) < 0.05 and abs(k_B14b / k_B14 - 1) < 0.02 and abs(r22 / AU_M / 22 - 1) < 0.03)
P(f"    BDEF eq. (9) solves eq. (8): residual {k4_sol};  phi'/r (r -> 0) = {lim_small};  phi' r c^2 (MOND) = {lim_mond};  phi' r^2 (r -> oo) = {lim_bd}")
check("K4 CONTROL (the reference, verified): BDEF 2011 = Babichev, Deffayet, Esposito-Farese, 'Improving relativistic MOND with "
      "Galileon k-mouflage', Phys. Rev. D 84, 061502(R) (arXiv:1106.2538).  Its spherical eq. (8) 4k (r_s/r^2) phi'^2 + (r^2 c^2/a0) "
      "phi'^2 + eps r^2 phi' = r_s/2 is solved by its eq. (9) (sympy); the three regimes come out as stated (phi' -> r/sqrt(8k) inside, "
      "sqrt(G M a0)/(r c^2) in the MOND range, G M/(eps r^2 c^2) outside); the transition is r_V = (8 k G M a0)^(1/4)/c; and its numbers "
      "reproduce: k^(1/4) = 4e-6 c^2/a0 = G(1e3 Msun) c^4/(8 a0^3) ~ 100 kpc and the Solar-System ratio (r/22 AU)^4 (a0 = 1.2e-10)",
      f"eq. (8)-(9) {k4_sol == 0}; limits ok; r_V {rV_ok}; k^(1/4) = {k_B14 / KPC:.1f} kpc (eq. 6) / {k_B14b / KPC:.1f} kpc (1e3 Msun); "
      f"r_22 = {r22 / AU_M:.1f} AU", k4_ok,
      reading="its Galileon term -(k/3) eps eps phi_a phi_m phi_;bn R_gdrs is the Fab-Four 'Paul' term (Horndeski G5 ~ X): it couples the scalar "
              "to the Riemann tensor, which is why its r_V depends on M (the cubic flat Galileon's does not, K5)")

# ---- K5: Route 2's one-parameter reduction (cubic Galileon on the P2 k-mouflage), re-derived from a spherical Lagrangian
# L = 4 pi r^2 [-2 alpha^2 J_P2(pi'^2/alpha^2) - k_3 pi'^2 Box pi + pi rho], Box pi = pi'' + 2 pi'/r; the Euler-Lagrange expression
# dL/dpi - d/dr dL/dpi' + d^2/dr^2 dL/dpi'' is assembled with pi' = p > 0 (so sqrt(Y) = p/alpha) and compared with d/dr of the flux
rr_ = sp.Symbol('r', positive=True)
k3, al_, p_, q_ = sp.symbols('k_3 alpha p q', positive=True)
pif = sp.Function('pi')(rr_)
pp_, ppp_ = sp.diff(pif, rr_), sp.diff(pif, rr_, 2)
JP2 = lambda Y: -sp.log(1 - 2 * sp.sqrt(Y)) / 4 - sp.sqrt(Y) / 2 - Y / 2
L5 = 4 * sp.pi * rr_ ** 2 * (-2 * al_ ** 2 * JP2(p_ ** 2 / al_ ** 2) - k3 * p_ ** 2 * (q_ + 2 * p_ / rr_))
dLdp, dLdq = sp.simplify(sp.diff(L5, p_)), sp.diff(L5, q_)
sub5 = {p_: pp_, q_: ppp_}
EL5 = -sp.diff(dLdp.subs(sub5), rr_) + sp.diff(dLdq.subs(sub5), rr_, 2)          # the source term 4 pi r^2 rho is separate
mus = lambda x: x / (1 - 2 * x)
Flux5 = 4 * sp.pi * (4 * rr_ ** 2 * mus(pp_ / al_) * pp_ + 4 * k3 * rr_ * pp_ ** 2)
k5_div = sp.simplify(EL5 - sp.diff(Flux5, rr_))
x_ = sp.Symbol('x', positive=True)
ratio5 = sp.simplify((4 * k3 * rr_ * (al_ * x_) ** 2) / (4 * rr_ ** 2 * mus(x_) * al_ * x_))   # Galileon / k-mouflage flux at pi' = alpha x
ratio5_deep = sp.limit(ratio5, x_, 0)
A0_R2 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
Rstar_R2 = {f: GM_SUN * a_ / (1.4e-15 ** 2 * AU_M) / MPC for f, a_ in A0_R2.items()}
k5_ok = (k5_div == 0 and sp.simplify(ratio5_deep - k3 * al_ / rr_) == 0 and abs(Rstar_R2["canonical"] / 1.373e6 - 1) < 2e-3
         and abs(Rstar_R2["alt"] / 1.654e6 - 1) < 2e-3)
P(f"    spherical EL expression of -2 alpha^2 J_P2 - k_3 pi'^2 Box pi minus d/dr[4 pi (4 r^2 mu_s(x) pi' + 4 k_3 r pi'^2)] = {k5_div} (a flux); "
  f"Galileon/k-mouflage flux = {ratio5} -> {ratio5_deep} in the deep regime: x mu_s(x) + (R_*/r) x^2 = y with R_* = k_3 alpha, independent of M")
check("K5 CONTROL (Route 2, route2_vainshtein_kmouflage_2026.py, 5ba86489b, re-derived): for the cubic Galileon on P2's k-mouflage J_P2 "
      "the spherical Euler-Lagrange expression is exactly the r-derivative of a flux (sympy), and the Galileon flux over the k-mouflage "
      "flux is k_3 alpha (1 - 2x)/r -> k_3 alpha/r in the deep regime -- the field strength cancels, so the Vainshtein trigger degenerates "
      "into a UNIVERSAL radius R_* = k_3 alpha (independent of the source mass): x^2/(1 - 2x) + (R_*/r) x^2 = y.  Route 2's monopole floor "
      "R_* >= G M_sun a0/(a_b^2 AU) is reproduced (1.373e6 / 1.654e6 Mpc at its a0 and Mars budget 1.4e-15 m/s^2)",
      f"flux residual {k5_div}; ratio {ratio5} (deep {ratio5_deep}); floor {Rstar_R2['canonical']:.4g} / {Rstar_R2['alt']:.4g} Mpc", k5_ok)

# ---- K6: the unitary-gauge block (FP14's construction) with a readout of order p in the lapse's derivatives
tt_, xx_, yy_, zz_ = sp.symbols('t x y z', real=True)
X3m = (xx_, yy_, zz_)
eb = sp.Symbol('e_b')
alm, c2m, Cph, lmm, sgm, Kb, K2b = sp.symbols('alpha_c c_2 C_phi lambda sigma K K_2', real=True)
nf, pf, Bf, Sf, Ff = [sp.Function(s_)(tt_, xx_, yy_, zz_) for s_ in ('n', 'psi', 'B', 'S', 'phi')]
kq_, wq_ = sp.symbols('k omega', real=True)
An, Ap, AB, AS, AF = sp.symbols('A_n A_psi A_B A_S A_phi')
AMP = {"n": An, "psi": Ap, "B": AB, "S": AS, "phi": AF}


def unitary_block(order=0):
    """FP14's second variation of the root about Minkowski (unitary gauge, finite c_2), with the chassis field chi's readout
    depth depending on the lapse: order 1 = FP14 X3b (delta chi = K d_z delta n: the depth keyed on |a|), order 2 = a curvature
    key (delta chi = K_2 d_z^2 delta n: the depth keyed on the tidal component d_z^2 Phi / c^2)."""
    Nl = sp.exp(eb * nf)
    gam = sp.diag(*[sp.exp(-2 * eb * pf)] * 3)
    gin = gam.inv()
    Ni = [eb * (sp.diff(Bf, X3m[0]) + Sf), eb * sp.diff(Bf, X3m[1]), eb * sp.diff(Bf, X3m[2])]
    Gm3 = [[[sum(gin[a_, d_] * (sp.diff(gam[d_, b_], X3m[c_]) + sp.diff(gam[d_, c_], X3m[b_]) - sp.diff(gam[b_, c_], X3m[d_]))
                 for d_ in range(3)) / 2 for c_ in range(3)] for b_ in range(3)] for a_ in range(3)]
    DN = [[sp.diff(Ni[j], X3m[i]) - sum(Gm3[q][i][j] * Ni[q] for q in range(3)) for j in range(3)] for i in range(3)]
    Kij = sp.Matrix(3, 3, lambda i, j: (sp.diff(gam[i, j], tt_) - DN[i][j] - DN[j][i]) / (2 * Nl))
    Kup = gin * Kij * gin
    KK = sum(Kij[i, j] * Kup[i, j] for i in range(3) for j in range(3))
    trK = sum(gin[i, j] * Kij[i, j] for i in range(3) for j in range(3))

    def Ric3(b_, c_):
        return sum(sp.diff(Gm3[a_][b_][c_], X3m[a_]) - sp.diff(Gm3[a_][b_][a_], X3m[c_]) +
                   sum(Gm3[a_][a_][d_] * Gm3[d_][b_][c_] - Gm3[a_][c_][d_] * Gm3[d_][b_][a_] for d_ in range(3)) for a_ in range(3))
    R3 = sum(gin[b_, c_] * Ric3(b_, c_) for b_ in range(3) for c_ in range(3))
    ai = [sp.diff(sp.log(Nl), xi_) for xi_ in X3m]
    aa = sum(gin[i, j] * ai[i] * ai[j] for i in range(3) for j in range(3))
    Fi = [sp.diff(eb * Ff, xi_) for xi_ in X3m]
    if order == 1:
        ro = [Kb * sp.diff(eb * nf, zz_, X3m[i]) for i in range(3)]
    elif order == 2:
        ro = [K2b * sp.diff(eb * nf, zz_, zz_, X3m[i]) for i in range(3)]
    else:
        ro = [0, 0, 0]
    Xi = [sgm * Fi[i] + ro[i] for i in range(3)]
    Bch, Cch = 2 * (2 - alm), -(2 - alm)
    chassis = Bch * sum(gin[i, j] * ai[i] * Xi[j] for i in range(3) for j in range(3)) + Cch * sum(gin[i, j] * Xi[i] * Xi[j]
                                                                                               for i in range(3) for j in range(3))
    Jquad = -2 * Cph * sum(gin[i, j] * Fi[i] * Fi[j] for i in range(3) for j in range(3))
    ndphi = (sp.diff(eb * Ff, tt_) - sum(sum(gin[i, j] * Ni[j] for j in range(3)) * Fi[i] for i in range(3))) / Nl
    flds = [nf, pf, Bf, Sf, Ff]
    Lfull = Nl * sp.exp(-3 * eb * pf) * (KK - trK ** 2 + R3 + alm * aa - c2m * trK ** 2 + chassis + Jquad + 2 * lmm * ndphi ** 2)
    L2f = sp.expand((sp.diff(Lfull, eb, 2) / 2).subs(eb, 0))
    ELf = euler_equations(L2f, flds, [tt_, xx_, yy_, zz_])
    phs = sp.exp(sp.I * (kq_ * zz_ - wq_ * tt_))
    fsub = {nf: An * phs, pf: Ap * phs, Bf: AB * phs, Sf: AS * phs, Ff: AF * phs}
    ELk = [sp.expand(sp.simplify((e_.lhs - e_.rhs).subs(fsub).doit() / phs)) for e_ in ELf]
    return dict(zip([f_.func.__name__ for f_ in flds], ELk))


def reduce_TV(E, keep, aux):
    order = keep + aux
    M = sp.Matrix([[sp.expand(sp.diff(E[r2], AMP[c_])) for c_ in order] for r2 in order])
    herm = sp.simplify(M - M.H.subs({sp.conjugate(wq_): wq_, sp.conjugate(kq_): kq_, sp.conjugate(Kb): Kb, sp.conjugate(K2b): K2b})) == sp.zeros(*M.shape)
    nk = len(keep)
    Rm = (M[:nk, :nk] - M[:nk, nk:] * M[nk:, nk:].inv() * M[nk:, :nk]).applyfunc(lambda x2: sp.simplify(sp.expand(x2)))
    Rs = Rm.applyfunc(sp.expand)
    T = Rs.applyfunc(lambda x2: sp.simplify(x2.coeff(wq_, 2)))
    V = Rs.applyfunc(lambda x2: sp.simplify(-x2.coeff(wq_, 0)))
    rest = Rs.applyfunc(lambda x2: sp.simplify(x2 - x2.coeff(wq_, 2) * wq_ ** 2 - x2.coeff(wq_, 0)))
    return T, V, herm, rest == sp.zeros(nk, nk)


tK6 = time.time()
T0b, V0b, h0b, q0b = reduce_TV(unitary_block(0), ["psi", "phi"], ["n", "B"])
T1b, V1b, h1b, q1b = reduce_TV(unitary_block(1), ["psi", "phi"], ["n", "B"])
V_fp7 = sp.Matrix([[4 * kq_ ** 2 * (2 - alm) / alm, 4 * kq_ ** 2 * sgm * (alm - 2) / alm],
                   [4 * kq_ ** 2 * sgm * (alm - 2) / alm, 4 * kq_ ** 2 * (alm * (Cph - sgm ** 2) + 2 * sgm ** 2) / alm]])
V11_x3b = 4 * kq_ ** 2 * (2 - alm) * (1 + Kb ** 2 * kq_ ** 2) / (alm - (2 - alm) * Kb ** 2 * kq_ ** 2)
k6_ok = (sp.simplify(V0b - V_fp7) == sp.zeros(2, 2) and sp.simplify(V1b[0, 0] - V11_x3b) == 0 and h1b and q1b
         and sp.simplify(T0b - sp.Matrix([[12 + 8 / c2m, 0], [0, 4 * lmm]])) == sp.zeros(2, 2))
check("K6 CONTROL: this lane's copy of FP14's unitary-gauge second variation reproduces FP7 C1's V (no readout) and FP14 X3b's "
      "first-order readout block V_11 = 4k^2 (2 - alpha_c)(1 + K^2 k^2)/(alpha_c - (2 - alpha_c) K^2 k^2) exactly (Hermitian, "
      "exactly quadratic in omega, T = diag(12 + 8/c_2, 4 lambda))",
      f"V(no readout) == FP7: {sp.simplify(V0b - V_fp7) == sp.zeros(2, 2)}; V_11(order 1) == FP14 X3b: {sp.simplify(V1b[0, 0] - V11_x3b) == 0}; "
      f"Hermitian {h1b}; quadratic {q1b}; ({time.time() - tK6:.1f} s)", k6_ok)

# ---- K7: FP9's machinery (exec'd read-only up to its CONTROLS banner, as FP14 K2) and its (H_Y) sigma_8 headline
FP9_PATH = os.path.join(HERE, "FP9_web_galaxy_separator.py")
src9 = open(FP9_PATH).read()
M9 = exec_quiet(src9[:src9.index('\nbanner("K  CONTROLS')], FP9_PATH, {"__file__": FP9_PATH, "__name__": "fp9_machinery"})
HY = M9["bandpass_model"](M9["LL_of"](1.3, 2.0), 2.0, yr=0.0, floor=(1e-6, 4.0, M9["YIELD"]))
S8_HY = {str((f, m)): M9["sigma8_of"](M9["growth_aq"](HY, M9["A0"][f], mode=m, c2=M9["C2W"])[0.0]) / M9["S8_LCDM"]
         for f in ("canonical", "alt") for m in ("rms", "permode")}
dev_s8 = max(abs(S8_HY[k2] - fp9["numbers"]["H2"]["s8"][k2]) for k2 in S8_HY)
FLAG_TOL_FP9 = M9["FLAG_TOL"]
L0_SEP = float(M9["L_phys"](M9["LL_of"](1.3, 2.0), 2.0, 1.0))      # FP9's band-pass length today (FP6's L_phys: physical Mpc)
check("K7 CONTROL: FP9's committed machinery (exec'd read-only, as FP14 K2) reproduces FP9's (H_Y) headline sigma_8 on both footings "
      "and both yardsticks (used for the FRW re-score in R)",
      "sigma_8/LCDM " + ", ".join(f"{k2}: {v2:.5f}" for k2, v2 in S8_HY.items()) + f"; max dev {dev_s8:.1e}; FP9's flagship gate "
      f"{FLAG_TOL_FP9} dex; the separator's band-pass length today L(0) = {L0_SEP:.3f} Mpc", dev_s8 < 1e-6)
P(f"    {el()}")

# ============================================================================================================== M theorem
banner("M  THE THRESHOLD-MASS THEOREM: Solar-System screening is a statement about the Sun's MASS, and the framework has no mass there")
# ---- M1: where the strict law's Q2 comes from
M1 = {}
for (f, ge), d2 in Q2C.items():
    frac = d2["cum"] / d2["cum"][-1]
    mono = bool(np.all(np.diff(frac) >= -1e-6))
    v05, v50, v95 = (float(V_G[np.argmax(frac >= p_)]) for p_ in (0.05, 0.50, 0.95))
    rM = math.sqrt(GM_SUN / A0[f])
    rows = {}
    for nm, v in (("v05", v05), ("v50", v50), ("v95", v95)):
        r = rM / v
        rows[nm] = dict(v=v, r_AU=r / AU_M, r_pc=r / PC_M, y_tot=math.sqrt(d2["eN"] ** 2 + v ** 4), C=GM_SUN / (2 * r * cc ** 2))
    M1[(f, ge)] = dict(mono=mono, **rows)
r_lo_AU = min(m_["v95"]["r_AU"] for m_ in M1.values())
r_hi_AU = max(m_["v05"]["r_AU"] for m_ in M1.values())
y_lo = min(min(m_["v05"]["y_tot"], m_["v95"]["y_tot"]) for m_ in M1.values())
y_hi = max(max(m_["v05"]["y_tot"], m_["v95"]["y_tot"]) for m_ in M1.values())
C_sun_max = max(m_["v95"]["C"] for m_ in M1.values())
for (f, ge), m_ in M1.items():
    P(f"    {f:9s} g_ext {ge:.2e}: 5% / 50% / 95% of Q2 accumulated at r = {m_['v05']['r_AU']:.0f} / {m_['v50']['r_AU']:.0f} / "
      f"{m_['v95']['r_AU']:.0f} AU (total y_N {m_['v05']['y_tot']:.2f} / {m_['v50']['y_tot']:.2f} / {m_['v95']['y_tot']:.2f}; C = "
      f"{m_['v05']['C']:.1e} / {m_['v50']['C']:.1e} / {m_['v95']['C']:.1e}); monotone {m_['mono']}")
OUT["numbers"]["M1"] = {f"{k2[0]}|{k2[1]}": v2 for k2, v2 in M1.items()}
check("M1 WHERE CASSINI'S Q2 IS MADE: in the strict law the cumulative quadrupole (the f28 integrand, K3) rises monotonically and 90% of it "
      f"is generated at r = {r_lo_AU:.0f}-{r_hi_AU:.0f} AU from the Sun, where the total Newtonian field is y_N = {y_lo:.1f}-{y_hi:.0f} and the "
      f"source compactness C = G M/(r c^2) is <= {C_sun_max:.1e} -- a 1-Msun system at its own EFE transition (the same y as the inner "
      "parts of galaxies).  Any screening must switch MOND off THERE (FP14 X5: tail cuts above y = 20 move Q2 by < 3%).  The integrand is "
      "P2's QUMOND realisation (FP1/FP14); FP7 A4's AQUAL Q2 floors lie within 10% of QUMOND's, so the region carries over to the AQUAL root",
      f"r {r_lo_AU:.0f}-{r_hi_AU:.0f} AU; y_N {y_lo:.2f}-{y_hi:.1f}; C <= {C_sun_max:.2e}; monotone in all 6 cells: {all(m_['mono'] for m_ in M1.values())}",
      all(m_["mono"] for m_ in M1.values()) and r_hi_AU < 1e4 and y_lo > 1.0 and y_hi < 30)

# ---- M2: the (y, C) gap from SPARC, and the Buckingham reduction
dimM = sp.Matrix([[3, 1, 1, 1, -2], [-2, 0, -2, -1, 0]])                # (GM, r, a0, c, Lambda) in (m, s)
ns_ = dimM.nullspace()
yv = sp.Matrix([1, -2, -1, 0, 0])                                     # y = GM r^-2 a0^-1
Cv = sp.Matrix([1, -1, 0, -2, 0])                                     # C = GM r^-1 c^-2
Lv = sp.Matrix([0, 0, -2, 4, 1])                                      # Lambda c^4/a0^2
span_ok = sp.Matrix.hstack(*ns_).rank() == 3 and sp.Matrix.hstack(*ns_, yv, Cv, Lv).rank() == 3 and dimM * yv == sp.zeros(2, 1) \
    and dimM * Cv == sp.zeros(2, 1) and dimM * Lv == sp.zeros(2, 1)
Cgal, Menc = {}, {}
for U in (0.5, 0.7, 0.9):
    iu = int(np.argmin(np.abs(UPS - U)))
    for f, a0 in A0.items():
        yb = GB[:, iu] / a0
        m_ = OKS[:, iu] & (yb >= y_lo) & (yb <= y_hi)
        CC = VB2[:, iu] * 1e6 / (2 * cc ** 2)
        Cgal[(U, f)] = (float(CC[m_].min()), int(m_.sum()))
        Menc[(U, f)] = float((GB[:, iu] * _R ** 2 / Gn)[m_].min() / MSUN)
C_gal_min = min(v2[0] for v2 in Cgal.values())
M_gal_min = min(Menc.values())
gap = C_gal_min / C_sun_max
# any power-law key y^p C^q with a threshold theta: in (log y, log C) the key's boundary is the line log C = s log y + t.  Scan s:
# the Sun's points that must be screened (the Q2 region of every cell, and the planets) must lie below it, every SPARC point with
# y <= 100 (MOND >= 0.5%) above it; record the feasible t-interval and the smallest |t| (|log10 theta| up to the exponent q).
sun_pts = []
for (f, ge), d2 in Q2C.items():
    rM = math.sqrt(GM_SUN / A0[f])
    for v in np.linspace(M1[(f, ge)]["v05"]["v"], M1[(f, ge)]["v95"]["v"], 40):
        r = rM / v
        sun_pts.append((math.log10(math.sqrt(d2["eN"] ** 2 + v ** 4)), math.log10(GM_SUN / (2 * r * cc ** 2)), f))
    for a_ in PLANETS.values():
        r = a_ * AU_M
        sun_pts.append((math.log10(GM_SUN / r ** 2 / A0[f]), math.log10(GM_SUN / (2 * r * cc ** 2)), f))
gal_pts = []
for U in (0.5, 0.7, 0.9):
    iu = int(np.argmin(np.abs(UPS - U)))
    for f, a0 in A0.items():
        m_ = OKS[:, iu] & (GB[:, iu] / a0 <= 100.0)
        gal_pts.append(np.c_[np.log10(GB[m_, iu] / a0), np.log10(VB2[m_, iu] * 1e6 / (2 * cc ** 2))])
BEST, NFEAS, LLEN, NPTS = {}, {}, {}, {}
for f in A0:
    SUNP = np.array([(a_, b_) for a_, b_, g_ in sun_pts if g_ == f])
    GALP = np.vstack([gal_pts[i] for i, (U, g_) in enumerate((U, g_) for U in (0.5, 0.7, 0.9) for g_ in A0) if g_ == f])
    best_line, nfe = None, 0
    for s_ in np.linspace(-60.0, 60.0, 12001):
        tlo = float(np.max(SUNP[:, 1] - s_ * SUNP[:, 0]))
        thi = float(np.min(GALP[:, 1] - s_ * GALP[:, 0]))
        if tlo < thi:
            nfe += 1
            tt = 0.0 if tlo < 0 < thi else (tlo if tlo > 0 else thi)
            if best_line is None or abs(tt) < abs(best_line[1]):
                best_line = (float(s_), tt, tlo, thi)
    BEST[f] = best_line or (float('nan'), 0.0, float('nan'), float('nan'))
    NFEAS[f], NPTS[f] = nfe, (len(SUNP), len(GALP))
    LLEN[f] = (2 * 10 ** BEST[f][2] * cc ** 2 / A0[f] / PC_M, 2 * 10 ** BEST[f][3] * cc ** 2 / A0[f] / PC_M)
tmin = min(abs(BEST[f][1]) for f in A0)
P(f"    Buckingham: the dimension matrix of (GM, r, a0, c, Lambda) has rank 2 -> 3 groups, spanned by y, C and Lambda c^4/a0^2 = 8 pi/kappa^2: "
  f"{span_ok}")
P("    SPARC points with y_bar in the Q2 range: " + "; ".join(f"U {k2[0]} {k2[1][:3]}: {v2[1]} points, min C {v2[0]:.2e}" for k2, v2 in Cgal.items())
  + f";  smallest enclosed baryonic mass there {M_gal_min:.2e} Msun")
for f in A0:
    P(f"    {f:9s} power-law keys y^p C^q (the line log C = s log y + t): {NFEAS[f]} of 12001 slopes in [-60, 60] separate the Sun (Q2 region + "
      f"planets, {NPTS[f][0]} points) from SPARC ({NPTS[f][1]} points with y <= 100); the smallest |t| is {abs(BEST[f][1]):.2f} at s = {BEST[f][0]:.2f}, "
      f"feasible t in [{BEST[f][2]:.2f}, {BEST[f][3]:.2f}]: the key C/y = r a0/(2 c^2), a LENGTH r in [{LLEN[f][0]:.3f}, {LLEN[f][1]:.0f}] pc -- the "
      f"heat filter's own window [{XI_FLOOR[f]:.4f}, ~{XI_CEIL_PC:.0f}] pc")
OUT["numbers"]["M2"] = dict(C_gal={f"{k2[0]}|{k2[1]}": v2 for k2, v2 in Cgal.items()}, C_sun_max=C_sun_max, gap=gap, M_gal_min=M_gal_min,
                            y_range=[y_lo, y_hi], best_line=BEST, n_feasible_slopes=NFEAS, length_window_pc=LLEN)
check("M2 THE ONLY LOCAL DISCRIMINANT IS A MASS (OR A LENGTH), AND NO O(1) THRESHOLD SEPARATES: for an isolated point source the local "
      "invariants built from (GM, r, a0, c, Lambda) are functions of y = GM/(r^2 a0), C = GM/(r c^2) and 8 pi/kappa^2 (Buckingham, sympy "
      "nullspace; an external field adds e/a0 and an angle -- those keys are C5's, outside this theorem); at fixed y, C ~ M^(1/2).  "
      f"SPARC's points at the same y ({y_lo:.1f}-{y_hi:.0f}) have C >= {C_gal_min:.1e}, the Sun's Q2 region C <= {C_sun_max:.1e} ({gap:.0f}x): a "
      f"threshold mass between ~1 Msun and {M_gal_min:.1e} Msun.  Over EVERY power-law key y^p C^q (any exponents, each footing) the boundary "
      f"that screens the Sun's Q2 region and the planets but no SPARC point with y <= 100 sits >= {tmin:.1f} decades from unity; the best is "
      f"the length key C/y = r a0/(2c^2) with r_* in [{LLEN['canonical'][0]:.3f}, {LLEN['canonical'][1]:.0f}] / [{LLEN['alt'][0]:.3f}, "
      f"{LLEN['alt'][1]:.0f}] pc -- xi's own window.  A curvature key is a C-key (tidal 2GM/r^3 = 2 y^2 a0^2/(C c^2))",
      f"rank/span {span_ok}; C gap {C_sun_max:.2e} .. {C_gal_min:.2e} ({gap:.0f}x); min |log threshold| " + " / ".join(f"{abs(BEST[f][1]):.2f} (slope "
      f"{BEST[f][0]:.2f})" for f in A0) + "; length windows " + " / ".join(f"{LLEN[f][0]:.3f}-{LLEN[f][1]:.0f} pc" for f in A0),
      span_ok and gap > 100 and M_gal_min > 1e3 and tmin > 5,
      reading="the data themselves pick the length key: the one quantity that separates the Sun from galaxies is a length of order xi, and "
              "(a0, Lambda, G, c) give lengths only as c^2/a0 x (8 pi/kappa^2)^e (FP14 X1)")

# ---- M3: masses from (a0, Lambda, G, c)
eA, eC, eG, eL = sp.symbols('e_a e_c e_G e_L')
dims4 = {"a0": (1, 0, -2), "c": (1, 0, -1), "G": (3, -1, -2), "Lambda": (-2, 0, 0)}
eqsM = [sum(e_x * dims4[k2][i] for e_x, k2 in zip((eA, eC, eG, eL), dims4)) - t_x for i, t_x in enumerate((0, 1, 0))]
solM = sp.solve(eqsM, [eA, eC, eG], dict=True)[0]
PURE = 8 * math.pi / KAPPA ** 2
M_H = {f: cc ** 4 / (Gn * a_) / MSUN for f, a_ in A0.items()}
WIN_M = {f: (A0[f] * (XI_FLOOR[f] * PC_M) ** 2 / Gn / MSUN, A0[f] * (XI_CEIL_PC * PC_M) ** 2 / Gn / MSUN) for f in A0}
D_win = {f: (math.log(WIN_M[f][0] / M_H[f]) / math.log(PURE), math.log(WIN_M[f][1] / M_H[f]) / math.log(PURE)) for f in A0}
hitsM = {f"M_H (8 pi/kappa^2)^{D}": M_H["canonical"] * PURE ** D for D in range(-13, -7)
         if WIN_M["canonical"][0] <= M_H["canonical"] * PURE ** D <= WIN_M["canonical"][1]}
M_CH = (1.054571817e-34 * cc / Gn) ** 1.5 / (MP_C2 * 1.602176634e-19 / cc ** 2) ** 2 / MSUN     # (hbar c/G)^(3/2)/m_p^2
P(f"    exponents of (a0, c, G, Lambda) for a mass: {solM}  ->  M = (c^4/(G a0)) (Lambda c^4/a0^2)^e_L = M_H (8 pi/kappa^2)^D;  M_H = "
  f"{M_H['canonical']:.2e} / {M_H['alt']:.2e} Msun")
P(f"    the xi window as a threshold mass a0 xi^2/G: canonical {WIN_M['canonical'][0]:.2f} .. {WIN_M['canonical'][1]:.2e} Msun (D in "
  f"[{D_win['canonical'][0]:.1f}, {D_win['canonical'][1]:.1f}]), alt {WIN_M['alt'][0]:.2f} .. {WIN_M['alt'][1]:.2e} Msun")
P("    integer-D hits (NUMEROLOGY, flagged): " + "; ".join(f"{k2} = {v2:.3g} Msun" for k2, v2 in hitsM.items())
  + f";  the Chandrasekhar-type stellar mass (hbar c/G)^(3/2)/m_p^2 = {M_CH:.2f} Msun (needs m_p: NOT in the gravity action -- NUMEROLOGY)")
OUT["numbers"]["M3"] = dict(exponents=str(solM), M_H=M_H, window_Msun=WIN_M, D_window=D_win, hits=hitsM, M_chandra=M_CH)
check("M3 NO O(1) MASS FROM (a0, Lambda, G, c) LANDS IN THE WINDOW: G enters once (a mass needs 1/G), so every mass is "
      f"M_H (8 pi/kappa^2)^D with M_H = c^4/(G a0) = {M_H['canonical']:.1e} Msun; the window (the heat filter's xi window read as a0 xi^2/G, "
      f"{WIN_M['canonical'][0]:.1f}-{WIN_M['canonical'][1]:.0e} Msun, consistent with M2) needs D in [{D_win['canonical'][0]:.1f}, "
      f"{D_win['canonical'][1]:.1f}]: a pure number 1e-17..1e-24.  Integer D = -9..-12 land ({len(hitsM)} hits) -- NUMEROLOGY; the stellar "
      f"mass scale (hbar c/G)^(3/2)/m_p^2 = {M_CH:.2f} Msun lands too, but the proton mass is not in the gravity core -- NUMEROLOGY",
      f"G exponent {solM[eG]}; D window [{D_win['canonical'][0]:.2f}, {D_win['canonical'][1]:.2f}] (canonical), [{D_win['alt'][0]:.2f}, "
      f"{D_win['alt'][1]:.2f}] (alt); {len(hitsM)} integer hits; M_Ch-type {M_CH:.2f} Msun",
      solM[eG] == -1 and D_win["canonical"][1] < -8 and len(hitsM) >= 1,
      reading="xi ~ 0.6 r_M(Sun) is the Sun's MOND radius: the Solar-System floor encodes the Sun's mass, a datum of stellar physics")

# ---- M4: the threshold mass of every route (the source mass whose screening radius equals its own r_M = sqrt(GM/a0))
f0, a00 = "canonical", A0["canonical"]
HF = H_FOOT[f0]


def Mstar_bdef(ell, a0):
    return 8 * ell ** 4 * a0 ** 3 / (Gn * cc ** 4) / MSUN


ROUTES = [("heat filter (xi, FP7 floors .. 100 pc)", "FITTED-class knob", WIN_M[f0][0], "window"),
          ("cubic Galileon, Newtonian-regime r_V = (4 beta r_g r_c^2)^(1/3), r_c = c/H, beta = 1", "constant-free",
           64 * a00 ** 3 / (Gn * HF ** 4) / MSUN, None),
          ("cubic Galileon on P2 (Route 2), R_* = 2 a0/H^2", "constant-free", a00 * (2 * a00 / HF ** 2) ** 2 / Gn / MSUN, None),
          ("BDEF Riemann Galileon, k^(1/4) = c/H" + (" [MUTATE: 100 kpc]" if MUTATE else ""), "constant-free", Mstar_bdef(ELL_FREE[f0], a00), None),
          ("tidal (Weyl) key at T_* = Lambda c^2", "constant-free", (KAPPA ** 4 / (16 * math.pi ** 2)) * M_H[f0], None),
          ("BDEF Riemann Galileon, k^(1/4) = 104 kpc (fitted, V4)", "new constant", Mstar_bdef(104 * KPC, a00), None),
          ("xi = ((hbar/m)^2/a0)^(1/3) at m = 1.9e-19 eV (B2)", "numerology", a00 * (((HBARC * cc / 1.9e-19) ** 2 / a00) ** (1 / 3)) ** 2 / Gn / MSUN, None),
          ("r_M of the Chandrasekhar-type mass (M3)", "numerology", M_CH, None)]
free_rows = [r2 for r2 in ROUTES if r2[1] == "constant-free"]
free_out = all(r2[2] > 1e10 * WIN_M[f0][1] for r2 in free_rows)
inwin = [r2 for r2 in ROUTES if WIN_M[f0][0] <= r2[2] <= WIN_M[f0][1] and r2[1] != "FITTED-class knob"]
for r2 in ROUTES:
    tag = "in window" if WIN_M[f0][0] <= r2[2] <= WIN_M[f0][1] else f"{math.log10(r2[2] / WIN_M[f0][1]):+.1f} dex above the window" \
        if r2[2] > WIN_M[f0][1] else "below"
    P(f"    {r2[0]:78s} [{r2[1]:14s}] M_* = {r2[2]:.2e} Msun  ({tag})" if r2[3] is None else
      f"    {r2[0]:78s} [{r2[1]:14s}] M_* = {WIN_M[f0][0]:.2f} .. {WIN_M[f0][1]:.2e} Msun  (the window)")
OUT["numbers"]["M4"] = [dict(route=r2[0], kind=r2[1], Mstar=r2[2]) for r2 in ROUTES]
check("M4 EVERY ROUTE IS A THRESHOLD MASS IN DISGUISE: the constant-free constructions (the cubic Galileon with r_c = c/H, Route 2's "
      "R_* = 2 a0/H^2, BDEF's k^(1/4) = c/H, a Weyl key at Lambda) put M_* at 1e20-1e22 Msun -- >= 13 decades above the window, so every "
      "galaxy is screened; the rows that land in the window carry a fitted length (xi, BDEF's k) or are numerology (xi_q(m), the "
      "Chandrasekhar-type mass)",
      f"constant-free rows >= 1e10 x the window top: {free_out} (" + ", ".join(f"{r2[2]:.1e}" for r2 in free_rows) + f" Msun vs <= {WIN_M[f0][1]:.1e}); "
      f"in-window rows: {[r2[1] for r2 in inwin]}", free_out and all(r2[1] in ("new constant", "numerology") for r2 in inwin))
P(f"    {el()}")

# ============================================================================================================== V route (a)
banner("V  (a) VAINSHTEIN / k-MOUFLAGE WITH A SELF-GENERATED SCALE -- and what it costs with a fitted one")
# ---- V1: the cubic Galileon's Vainshtein radius with r_c = c/H_Lambda (decoupling limit)
r1_, L3_, Mp_, be_ = sp.symbols('r Lambda3 M_P beta', positive=True)
pi1 = sp.Function('pi')(r1_)
rho1 = sp.Function('rho')(r1_)
p1 = sp.diff(pi1, r1_)
Lag1 = 4 * sp.pi * r1_ ** 2 * (-sp.Rational(1, 2) * p1 ** 2 - p1 ** 2 * (sp.diff(pi1, r1_, 2) + 2 * p1 / r1_) / L3_ - be_ * pi1 * rho1 / Mp_)
E1 = euler_equations(Lag1, [pi1], [r1_])[0].lhs
F1 = 4 * sp.pi * (r1_ ** 2 * p1 + 4 * r1_ * p1 ** 2 / L3_)
v1_flux = sp.simplify(E1 - sp.diff(F1, r1_) + 4 * sp.pi * be_ * r1_ ** 2 * rho1 / Mp_) == 0
# r^2 pi' + 4 r pi'^2/Lambda3 = beta M/(4 pi M_P): the cubic term equals the linear one at r_V^3 = beta M/(pi M_P Lambda3^3); with
# Lambda3^3 = M_P H^2 (c = hbar = 1) and M_P^2 = 1/(8 pi G): r_V^3 = 8 beta G M/H^2 = 4 beta r_g (c/H)^2
V1 = {}
for f in A0:
    rc = cc / H_FOOT[f]
    for M in (1.0, 1e7, 1e9, 1e11):
        rg = 2 * Gn * M * MSUN / cc ** 2
        rM = math.sqrt(Gn * M * MSUN / A0[f])
        V1[(f, M)] = {b_: (4 * b_ * rg * rc ** 2) ** (1 / 3) for b_ in (1 / 6, 1 / 4, 1 / 2, 1.0)}
        V1[(f, M)]["rM"] = rM
for (f, M), v2 in V1.items():
    P(f"    {f:9s} M = {M:.0e} Msun: r_V(beta = 1/6, 1/4 [DGP (r_g r_c^2)^(1/3)], 1/2, 1) = " + ", ".join(f"{v2[b_] / KPC:.3g}" for b_ in (1 / 6, 1 / 4, 1 / 2, 1.0))
      + f" kpc;  r_M = {v2['rM'] / KPC:.3g} kpc;  r_V/r_M >= {v2[1 / 6] / v2['rM']:.0f}")
rv11 = [V1[(f, 1e11)][1 / 6] / KPC for f in A0]
ratio_min = min(V1[(f, M)][1 / 6] / V1[(f, M)]["rM"] for f in A0 for M in (1e7, 1e9, 1e11))
OUT["numbers"]["V1"] = {f"{k2[0]}|{k2[1]:.0e}": {str(b_): v3 for b_, v3 in v2.items()} for k2, v2 in V1.items()}
check("V1 THE CUBIC GALILEON WITH r_c = c/H_Lambda SCREENS GALAXIES: the decoupling-limit equation is a flux (sympy: r^2 pi' + 4 r "
      "pi'^2/Lambda_3^3 = beta M/(4 pi M_P)), so r_V = (4 beta r_g r_c^2)^(1/3); for a 1e11-Msun galaxy r_V = "
      f"{min(rv11):.0f}-{max(V1[(f, 1e11)][1.0] / KPC for f in A0):.0f} kpc over beta = 1/6..1 (the rough '~70 kpc' is low by "
      f"{min(rv11) / 70:.0f}-{max(V1[(f, 1e11)][1.0] / KPC for f in A0) / 70:.0f}x), and r_V/r_M >= {ratio_min:.0f} for every mass 1e7-1e11 Msun: "
      f"MOND is screened throughout every galaxy (the Sun's own r_V is {min(V1[(f, 1.0)][1 / 6] for f in A0) / KPC:.2f}-"
      f"{max(V1[(f, 1.0)][1.0] for f in A0) / KPC:.2f} kpc)",
      f"flux identity {v1_flux}; r_V(1e11) {min(rv11):.0f}-{max(V1[(f, 1e11)][1.0] / KPC for f in A0):.0f} kpc; min r_V/r_M {ratio_min:.0f}",
      v1_flux and min(rv11) > 5 * 70 and ratio_min > 20)

# ---- V2: the cubic Galileon on the chain's P2 k-mouflage (Route 2's reduction on the AQUAL root)
RS_FREE = {f: 2 * A0[f] / H_FOOT[f] ** 2 for f in A0}                  # R_* = 2 k_3 a0/c^2 with k_3 = (c/H)^2
sp_cub_free = {f: sparc_best(lambda gb, R, a0, Rs=RS_FREE[f]: gb + a0 * x_screened(gb / a0, Rs / R), A0[f]) for f in A0}
RS_SCAN = (0.3, 1.0, 3.0, 10.0, 30.0)
sp_cub = {(f, s2): sparc_best(lambda gb, R, a0, Rs=s2 * KPC: gb + a0 * x_screened(gb / a0, Rs / R), A0[f]) for f in A0 for s2 in RS_SCAN}


def sparc_ceiling(fam, foot, lo, hi, tol=0.005):
    """largest length (m) with SPARC rms <= P2 + tol for a screened family fam(length) -> model, by bisection in log length."""
    base = SP_P2[foot][0]
    f_ = lambda lx: sparc_best(fam(math.exp(lx)), A0[foot])[0] - base - tol
    if f_(math.log(hi)) <= 0:
        return hi
    if f_(math.log(lo)) > 0:
        return lo
    return math.exp(brentq(f_, math.log(lo), math.log(hi), xtol=1e-3))


ceil_cub = {f: sparc_ceiling(lambda Rs: (lambda gb, R, a0: gb + a0 * x_screened(gb / a0, Rs / R)), f, 0.01 * KPC, 1e3 * KPC) for f in A0}


def floor_len(gate_fun, lo, hi):
    """smallest length (m) that passes a monotone Solar-System gate: gate_fun(L) <= 1."""
    g_ = lambda lx: math.log(max(gate_fun(math.exp(lx)), 1e-300))
    if g_(math.log(lo)) <= 0:
        return lo
    return math.exp(brentq(g_, math.log(lo), math.log(hi), xtol=1e-4))


def ss_cubic(Rs, a0, what):
    if what == "earth":
        return float(x_screened(GM_SUN / AU_M ** 2 / a0, Rs / AU_M)) * a0 / A_SUNWARD
    x = float(x_screened(GM_SUN / R_SAT ** 2 / a0, Rs / R_SAT))
    return x * a0 * R_SAT ** 2 / Gn / M_SAT_BOUND


fl_cub = {(f, w_): floor_len(lambda Rs: ss_cubic(Rs, A0[f], w_), 1e3 * AU_M, 1e6 * MPC) for f in A0 for w_ in ("earth", "saturn")}
empty_cub = {f: max(fl_cub[(f, "earth")], fl_cub[(f, "saturn")]) / ceil_cub[f] for f in A0}
P("    constant-free R_* = 2 a0/H^2: " + ", ".join(f"{f} {RS_FREE[f] / MPC / 1e3:.2f} Gpc -> SPARC {sp_cub_free[f][0]:.4f} (U {sp_cub_free[f][1]:.2f})" for f in A0))
P("    SPARC rms vs R_* [kpc]: " + "; ".join(f"{f[:3]} " + ", ".join(f"{s2}: {sp_cub[(f, s2)][0]:.4f}" for s2 in RS_SCAN) for f in A0))
P("    R_* windows: " + "; ".join(f"{f}: Earth gate needs R_* >= {fl_cub[(f, 'earth')] / MPC / 1e3:.2f} Gpc, Saturn monopole >= "
                                 f"{fl_cub[(f, 'saturn')] / MPC / 1e3:.2f} Gpc, SPARC (+0.005 dex) allows <= {ceil_cub[f] / KPC:.2f} kpc: "
                                 f"empty by {empty_cub[f]:.1e}" for f in A0))
OUT["numbers"]["V2"] = dict(R_free_Gpc={f: RS_FREE[f] / MPC / 1e3 for f in A0}, sparc_free=sp_cub_free, sparc_scan={f"{k2[0]}|{k2[1]}": v2 for k2, v2 in sp_cub.items()},
                            floors_m={f"{k2[0]}|{k2[1]}": v2 for k2, v2 in fl_cub.items()}, ceiling_m=ceil_cub, empty_factor=empty_cub)
check("V2 THE CUBIC GALILEON ON THE CHAIN'S P2 k-MOUFLAGE FAILS FOR EVERY R_* (Route 2's kill, re-derived on the AQUAL root): the "
      "trigger is the universal radius R_* (K5); the constant-free R_* = 2 a0/H^2 = "
      f"{RS_FREE['canonical'] / MPC / 1e3:.2f} / {RS_FREE['alt'] / MPC / 1e3:.2f} Gpc screens SPARC ({sp_cub_free['canonical'][0]:.3f} / "
      f"{sp_cub_free['alt'][0]:.3f} dex, Newtonian {SP_N['canonical'][0]:.3f}); and with R_* FREE the window is empty: the Earth gate needs "
      f">= {fl_cub[('canonical', 'earth')] / MPC / 1e3:.1f} Gpc and the Saturn monopole >= {fl_cub[('canonical', 'saturn')] / MPC / 1e3:.0f} Gpc "
      f"(P2's pole x -> 1/2 beats a Galileon flux that grows only as 1/r), SPARC allows <= {ceil_cub['canonical'] / KPC:.1f} kpc -- "
      f"empty by {min(empty_cub.values()):.0e}",
      f"SPARC(free) {sp_cub_free['canonical'][0]:.4f} / {sp_cub_free['alt'][0]:.4f}; empty by {empty_cub['canonical']:.1e} / {empty_cub['alt']:.1e}",
      all(sp_cub_free[f][0] > SP_P2[f][0] + 0.1 for f in A0) and all(v2 > 1e4 for v2 in empty_cub.values()))

# ---- V3: BDEF's Riemann-coupled Galileon on P2: r_V ~ M^(1/4) beats the pole; the framework's k screens galaxies
yq, rhoq = sp.symbols('y rho', positive=True)
xs_ = sp.Symbol('x', positive=True)
flux3 = xs_ ** 2 / (1 - 2 * xs_) + rhoq * xs_ ** 2 - yq
x_in = sp.sqrt(yq / rhoq)
lead_in = sp.limit(sp.simplify(flux3.subs(xs_, x_in * (1 + sp.Symbol('d'))) / yq).subs(sp.Symbol('d'), 0), rhoq, sp.oo)
interior = sp.simplify((sp.sqrt(yq / rhoq) * a0s).subs({yq: Gs * M_ / (r_ ** 2 * a0s), rhoq: 8 * k_ * Gs * M_ * a0s / (cs ** 4 * r_ ** 4)}))
v3_sym = sp.simplify(interior - cs ** 2 * r_ / sp.sqrt(8 * k_)) == 0 and lead_in == 0
K_FREE = {f: ELL_FREE[f] ** 4 for f in A0}
sp_b_free = {f: sparc_best(lambda gb, R, a0, k=K_FREE[f]: gb + a0 * x_screened(gb / a0, rho_bdef(k, a0, gb, R)), A0[f]) for f in A0}


def nu_bdef(k):
    return lambda y, r, Mb, a0: 1.0 + x_screened(y, rho_bdef(k, a0, y * a0, r)) / np.maximum(y, 1e-300)


ki_b_free = {f: kids_isolated(nu_bdef(K_FREE[f]))[f] for f in A0}


def flag_dev(k, a0, M=1e11, y=0.1):
    r = math.sqrt(Gn * M * MSUN / (y * a0))
    x = float(x_screened(y, rho_bdef(k, a0, y * a0, r)))
    return math.log10((y + x) / math.sqrt(y * y + y))


fl_b_free = {f: flag_dev(K_FREE[f], A0[f]) for f in A0}
rV11_free = {f: (8 * K_FREE[f] * Gn * 1e11 * MSUN * A0[f]) ** 0.25 / cc for f in A0}
rV_sun_free = {f: (8 * K_FREE[f] * GM_SUN * A0[f]) ** 0.25 / cc for f in A0}
P(f"    flux x^2/(1 - 2x) + (r_V/r)^4 x^2 = y: interior x = sqrt(y) (r/r_V)^2, i.e. the scalar force c^2 r/sqrt(8k) (BDEF's universal "
  f"behaviour) for ANY mass: {v3_sym}")
P("    k^(1/4) = " + ", ".join(f"{f} {ELL_FREE[f] / MPC:.4g} Mpc" for f in A0) + ": r_V(1e11 Msun) = " + ", ".join(f"{rV11_free[f] / KPC:.3g}" for f in A0)
  + " kpc, r_V(Sun) = " + ", ".join(f"{rV_sun_free[f] / PC_M:.3g}" for f in A0) + " pc")
P("    SPARC " + ", ".join(f"{f} {sp_b_free[f][0]:.4f} (U {sp_b_free[f][1]:.2f})" for f in A0) + ";  KiDS isolated chi^2 " + ", ".join(
    f"{f} {ki_b_free[f]:.1f} (P2 {KI_P2[f]:.1f})" for f in A0) + ";  flagship (1e11 Msun, y = 0.1) " + ", ".join(f"{f} {fl_b_free[f]:+.3f} dex" for f in A0))
OUT["numbers"]["V3"] = dict(k14_m=ELL_FREE, rV_1e11_kpc={f: rV11_free[f] / KPC for f in A0}, rV_sun_pc={f: rV_sun_free[f] / PC_M for f in A0},
                            sparc=sp_b_free, kids=ki_b_free, flagship_dex=fl_b_free)
v3_ok = (v3_sym and all(sp_b_free[f][0] > SP_P2[f][0] + 0.1 for f in A0) and all(ki_b_free[f] - KI_P2[f] > 500 for f in A0)
         and all(abs(fl_b_free[f]) > FLAG_TOL_FP10 for f in A0))
check("V3 BDEF'S RIEMANN-COUPLED GALILEON WITH THE FRAMEWORK'S k FAILS GALAXIES: on the chain's P2 k-mouflage its flux is x^2/(1 - 2x) "
      "+ (r_V/r)^4 x^2 = y with r_V = (8 k G M a0)^(1/4)/c -- mass-dependent, growing as r^-4 inward, so unlike the cubic Galileon it beats "
      "P2's pole (interior force c^2 r/sqrt(8k), sympy).  But with k^(1/4) from the framework (its O(1) lengths are c/H = 4.4-5.4 Gpc and "
      "c^2/a0 = 26-31 Gpc; c/H screens least) r_V(1e11 Msun) = "
      f"{min(rV11_free.values()) / MPC:.1f} Mpc: SPARC {sp_b_free['canonical'][0]:.3f} / {sp_b_free['alt'][0]:.3f} dex, KiDS d chi^2 "
      f"{ki_b_free['canonical'] - KI_P2['canonical']:+.0f} / {ki_b_free['alt'] - KI_P2['alt']:+.0f}, the flagship {fl_b_free['canonical']:+.2f} / "
      f"{fl_b_free['alt']:+.2f} dex (gate {FLAG_TOL_FP10}): FAILS",
      f"interior {v3_sym}; SPARC {sp_b_free['canonical'][0]:.4f}/{sp_b_free['alt'][0]:.4f}; KiDS {ki_b_free['canonical']:.0f}/{ki_b_free['alt']:.0f}; "
      f"flagship {fl_b_free['canonical']:+.3f}/{fl_b_free['alt']:+.3f}", v3_ok)

# ---- V4 (reported): BDEF with k FITTED -- the window, and a tie to FP9's separator length
fl_b_earth = {f: floor_len(lambda ell: float(x_screened(GM_SUN / AU_M ** 2 / A0[f], rho_bdef(ell ** 4, A0[f], GM_SUN / AU_M ** 2, AU_M))) * A0[f] / A_SUNWARD,
                           1 * KPC, 1e4 * MPC) for f in A0}
fl_b_sat = {f: floor_len(lambda ell: float(x_screened(GM_SUN / R_SAT ** 2 / A0[f], rho_bdef(ell ** 4, A0[f], GM_SUN / R_SAT ** 2, R_SAT)))
                         * A0[f] * R_SAT ** 2 / Gn / M_SAT_BOUND, 1 * KPC, 1e4 * MPC) for f in A0}
an_sat = (cc ** 2 * R_SAT ** 3 / (Gn * M_SAT_BOUND * math.sqrt(8))) ** 0.5
an_earth = (cc ** 2 * AU_M / (A_SUNWARD * math.sqrt(8))) ** 0.5
ceil_b = {f: sparc_ceiling(lambda ell: (lambda gb, R, a0: gb + a0 * x_screened(gb / a0, rho_bdef(ell ** 4, a0, gb, R))), f, 0.1 * MPC, 1e3 * MPC) for f in A0}
# Cassini Q2 in the Galaxy's field (estimate): the Galileon dominates the Sun's linear EFE response inside r_E, where
# (r_V/r)^4 dx ~ mu_eff with dx ~ y/mu_eff -> r_E = (r_V^4 r_M^2/mu_eff^2)^(1/6); the phantom beyond r_E is kept (M1's cumulative)
MUE = {}
for f, a0 in A0.items():
    ye = 2.32e-10 / a0
    xe = float(x_p2(ye))
    MUE[f] = (xe / (1 - 2 * xe), 2 * xe * (1 - xe) / (1 - 2 * xe) ** 2)


def q2_excised(ell, f, ge=2.32e-10):
    rV = (8 * ell ** 4 * GM_SUN * A0[f]) ** 0.25 / cc
    rM = math.sqrt(GM_SUN / A0[f])
    out = []
    for mu in MUE[f]:
        rE = (rV ** 4 * rM ** 2 / mu ** 2) ** (1 / 6)
        cum = Q2C[(f, ge)]["cum"]
        frac = np.interp(rM / rE, V_G, cum / cum[-1])
        out.append((rE / PC_M, Q2C[(f, ge)]["q2"] * max(frac, 0.0)))
    return out


q2x = {f: q2_excised(fl_b_sat[f], f) for f in A0}
rE_wb = {f: [((8 * fl_b_sat[f] ** 4 * 2 * GM_SUN * A0[f]) ** 0.25 / cc) ** (2 / 3) * (2 * GM_SUN / A0[f]) ** (1 / 6) / mu ** (1 / 3) / PC_M
             for mu in MUE[f]] for f in A0}                            # r_E for a 2-Msun binary at the floor
# GW170817 (estimate): the Paul term is a Horndeski G5 ~ X term (G5X ~ k, G4 = 1/4 in BDEF's normalisation); on FRW c_T^2 - 1 ~
# X G5X (phi'' - H phi')/G4, and on a static gradient the analogue is c_T^2 - 1 ~ 8 k phi'^2 phi'', i.e. delta c_T ~ 4 k phi'^2 phi'';
# outside r_V (phi' c^2 = v_f^2/r) this is (r_V/r)^4 v_f^2/(2 c^2); the GW leaves NGC 4993 from r_src ~ 2 kpc (M_b ~ 5e10 Msun): delay
# ~ (v_f^2/2c^2) r_V^4/(3 r_src^3 c).  An ESTIMATE: the coefficient and the path geometry are O(1) uncertain (reported, not load-bearing).
M_HOST, R_SRC = 5e10 * MSUN, 2.0 * KPC


def gw_delay(ell, a0):
    vf2 = math.sqrt(Gn * M_HOST * a0)
    rV = (8 * ell ** 4 * Gn * M_HOST * a0) ** 0.25 / cc
    return vf2 / (2 * cc ** 2) * rV ** 4 / (3 * R_SRC ** 3 * cc)


ceil_gw = {f: brentq(lambda lx: math.log(gw_delay(math.exp(lx), A0[f]) / 10.0), math.log(1 * KPC), math.log(1e3 * MPC)) for f in A0}
ceil_gw = {f: math.exp(v2) for f, v2 in ceil_gw.items()}
ki_b_top = {f: kids_isolated(nu_bdef(ceil_gw[f] ** 4))[f] for f in A0}
flag_top = {f: flag_dev(ceil_gw[f] ** 4, A0[f]) for f in A0}
ppn_floor = {f: float(x_screened(GM_SUN / AU_M ** 2 / A0[f], rho_bdef(fl_b_sat[f] ** 4, A0[f], GM_SUN / AU_M ** 2, AU_M))) * A0[f] / (GM_SUN / AU_M ** 2)
             for f in A0}                                            # the MOND scalar's fractional force at 1 AU (C^Q_eff)
alpha1_floor = {f: 8 * v2 / (1 + v2) for f, v2 in ppn_floor.items()}   # FP2 L6d's MOND part |alpha_1| = 8 C/(1 + C) at that C
L_sep = L0_SEP * MPC
sp_sep = {f: sparc_best(lambda gb, R, a0: gb + a0 * x_screened(gb / a0, rho_bdef(L_sep ** 4, a0, gb, R)), A0[f]) for f in A0}
sep_ss = {f: (float(x_screened(GM_SUN / R_SAT ** 2 / A0[f], rho_bdef(L_sep ** 4, A0[f], GM_SUN / R_SAT ** 2, R_SAT))) * A0[f] * R_SAT ** 2 / Gn / M_SAT_BOUND)
          for f in A0}
c2a0 = {f: cc ** 2 / A0[f] for f in A0}
Zv = math.sqrt(32 * math.pi / 3)
hitsK = {nm: v2 for nm, v2 in {**{f"(c^2/a0) Z^-{n}": c2a0["canonical"] * Zv ** -n for n in range(5, 10)},
                               **{f"(c^2/a0)(8 pi/kappa^2)^-{n}": c2a0["canonical"] * PURE ** -n for n in (2, 3)}}.items()
         if max(fl_b_sat.values()) <= v2 <= min(ceil_gw.values())}
P("    floors on k^(1/4) (the interior's harmonic phantom, a0-independent): Earth gate " + ", ".join(f"{fl_b_earth[f] / KPC:.1f}" for f in A0)
  + f" kpc (analytic {an_earth / KPC:.1f}), Saturn monopole " + ", ".join(f"{fl_b_sat[f] / KPC:.1f}" for f in A0) + f" kpc (analytic {an_sat / KPC:.1f})")
P("    Cassini Q2 in the Galaxy's field at the monopole floor (estimate: phantom excised inside r_E = (r_V^4 r_M^2/mu^2)^(1/6), mu_T / mu_L): "
  + "; ".join(f"{f}: " + ", ".join(f"r_E {rE:.3f} pc -> Q2/ceil {q2:.2f}" for rE, q2 in q2x[f]) for f in A0))
P("    ceilings: SPARC (+0.005 dex) " + ", ".join(f"{ceil_b[f] / MPC:.1f} Mpc" for f in A0) + ";  GW170817 (estimate, delay <= 10 s from NGC 4993) "
  + ", ".join(f"{ceil_gw[f] / KPC:.0f} kpc" for f in A0) + ";  at the GW ceiling: KiDS " + ", ".join(f"{ki_b_top[f] - KI_P2[f]:+.1f}" for f in A0)
  + ", flagship " + ", ".join(f"{flag_top[f]:+.1e} dex" for f in A0) + ";  at the floor: MOND fraction at 1 AU " + ", ".join(f"{ppn_floor[f]:.1e}" for f in A0)
  + " -> |alpha_1| (FP2 L6d's MOND part) " + ", ".join(f"{alpha1_floor[f]:.1e}" for f in A0) + " (bound 1e-5); sigma_8 and FRW as FP9 (the term is cubic in "
  "phi, phibar frozen); stability, the Galileon-lapse mixing and the leaf projection OPEN")
P(f"    window k^(1/4) in [{max(fl_b_sat.values()) / KPC:.0f}, ~{min(ceil_gw.values()) / KPC:.0f}] kpc (M_* = {Mstar_bdef(max(fl_b_sat.values()), a00):.0f}-"
  f"{Mstar_bdef(min(ceil_gw.values()), a00):.1e} Msun); numerology hits in it (flagged): " + ", ".join(f"{k2} = {v2 / KPC:.0f} kpc" for k2, v2 in hitsK.items()))
P(f"    the tie k = L(0)^4 to FP9's band-pass length (L(0) = {L0_SEP:.2f} Mpc): Saturn monopole {sep_ss['canonical']:.1e} of the bound, SPARC "
  f"{sp_sep['canonical'][0]:.4f} / {sp_sep['alt'][0]:.4f}; GW170817 delay (estimate) {gw_delay(L_sep, A0['canonical']):.0f} s (vs <= 10 s)")
OUT["numbers"]["V4"] = dict(floor_earth_kpc={f: fl_b_earth[f] / KPC for f in A0}, floor_saturn_kpc={f: fl_b_sat[f] / KPC for f in A0},
                            q2_excised=q2x, ceil_sparc_Mpc={f: ceil_b[f] / MPC for f in A0}, ceil_gw_kpc={f: ceil_gw[f] / KPC for f in A0},
                            kids_at_gw_ceiling={f: ki_b_top[f] - KI_P2[f] for f in A0}, flagship_at_gw_ceiling=flag_top,
                            mond_fraction_1AU_at_floor=ppn_floor, alpha1_at_floor=alpha1_floor, numerology=hitsK,
                            tie_L=dict(L0_Mpc=L0_SEP, saturn=sep_ss, sparc=sp_sep, gw_delay_s=gw_delay(L_sep, A0["canonical"])))
check("V4 (reported) BDEF WITH k FITTED REPLACES xi -- IT DOES NOT REMOVE IT: the interior's harmonic phantom 3 c^2/(4 pi G sqrt(8k)) "
      f"needs k^(1/4) >= {max(fl_b_sat.values()) / KPC:.0f} kpc (Saturn monopole; Earth {max(fl_b_earth.values()) / KPC:.0f} kpc); Cassini Q2 passes "
      f"by the excision estimate; SPARC allows up to ~{min(ceil_b.values()) / MPC:.0f} Mpc; GW170817 (an ESTIMATE of the Paul term's c_T on the "
      f"host's static gradient) caps it near {min(ceil_gw.values()) / KPC:.0f} kpc.  One fitted length for one fitted length; the tie k = L(0)^4 "
      "to FP9's separator length passes the Solar System and SPARC but misses GW170817 by the estimate",
      f"window [{max(fl_b_sat.values()) / KPC:.0f}, ~{min(ceil_gw.values()) / KPC:.0f}] kpc; tie to L: delay {gw_delay(L_sep, A0['canonical']):.0f} s",
      max(fl_b_sat.values()) < min(ceil_gw.values()), load_bearing=False,
      reading=f"wide binaries (2 Msun) would be Newtonian inside r_E = (r_V^4 r_M^2/mu^2)^(1/6) = {min(min(v2) for v2 in rE_wb.values()):.3f}-"
              f"{max(max(v2) for v2 in rE_wb.values()):.3f} pc at the floor: a different wide-binary signature from the heat filter's")
P(f"    {el()}")

# ============================================================================================================== B route (b)
banner("B  (b) SHARING xi WITH THE DARK FIELD'S MASS m: a coincidence unless an action couples them")
# ---- B1: de Broglie lengths
DB = {(m, v): HBARC / m * cc / v / PC_M for m in M_DARK for v in V_DISP + V_KICK}
db_lo, db_hi = min(DB[(m, v)] for m in M_DARK for v in V_DISP), max(DB[(m, v)] for m in M_DARK for v in V_DISP)
db_kick = max(DB[(m, v)] for m in M_DARK for v in V_KICK)
gate_kick = {f: fp7_gate(db_kick, "M", f) for f in ("canonical", "alt")}
P("    hbar/(m v) [pc]: " + "; ".join(f"m {m:.1e} eV, v {v / 1e3:.0f} km/s: {DB[(m, v)]:.4f}" for m in M_DARK for v in V_DISP + V_KICK)
  + f";  h/(m v) = 2 pi x: {2 * math.pi * db_lo:.3f}-{2 * math.pi * db_hi:.3f} pc")
OUT["numbers"]["B1"] = dict(db_pc={f"{k2[0]}|{k2[1]}": v2 for k2, v2 in DB.items()}, kick_max_pc=db_kick, monopole_at_kick=gate_kick)
check("B1 THE DE BROGLIE LENGTH, VERIFIED: hbar/(m v) = "
      f"{db_lo:.4f}-{db_hi:.4f} pc for m = 1.9-5.2e-19 eV and v = 200-600 km/s (near 0.02-0.05 pc only at the light end; h/(m v) is 2 pi "
      f"larger).  At FP10's own kick speeds (575-650 km/s) it is <= {db_kick:.4f} pc < the AQUAL floor {XI_FLOOR['canonical']:.4f} / "
      f"{XI_FLOOR['alt']:.4f} pc for every allowed m: as the filter length it FAILS the Saturn monopole ({gate_kick['canonical']:.1f}x / "
      f"{gate_kick['alt']:.1f}x the bound, FP7's table)",
      f"range {db_lo:.4f}-{db_hi:.4f} pc; kick {db_kick:.4f} pc; monopole {gate_kick['canonical']:.2f}x / {gate_kick['alt']:.2f}x",
      0.004 < db_lo < 0.01 and 0.04 < db_hi < 0.06 and db_kick < min(XI_FLOOR.values()) and min(gate_kick.values()) > 1)

# ---- B2: lengths from (hbar/m, a0, c) -- the unique c-free one
ph, pa, pc_ = sp.symbols('p_h p_a p_c')
eqsB = [2 * ph + pa + pc_ - 1, -ph - 2 * pa - pc_]                    # (L, T) of (hbar/m [L^2/T], a0 [L/T^2], c [L/T])
solB = sp.solve(eqsB, [ph, pc_], dict=True)[0]
XIQ = {(f, m): ((HBARC * cc / m) ** 2 / A0[f]) ** (1 / 3) / PC_M for f in A0 for m in M_DARK}
LC = {m: HBARC / m / PC_M for m in M_DARK}
XLH = {m: ((HBARC / m) ** 2 * cc / H_FOOT["canonical"]) ** (1 / 3) / PC_M for m in M_DARK}
M_WIN = {f: (HBARC * cc / math.sqrt((XI_CEIL_PC * PC_M) ** 3 * A0[f]), HBARC * cc / math.sqrt((XI_FLOOR[f] * PC_M) ** 3 * A0[f])) for f in A0}
P(f"    lengths from (hbar/m, a0, c): exponents {solB} -> lambda_C (lambda_C/(c^2/a0))^q; q = 0: lambda_C = hbar/(m c) = "
  + ", ".join(f"{LC[m]:.2e}" for m in M_DARK) + " pc; q = -1/3 (the only c-free member): xi_q = ((hbar/m)^2/a0)^(1/3) = "
  + ", ".join(f"{f[:3]} {XIQ[(f, m)]:.2f}" for f in A0 for m in M_DARK) + " pc; with Lambda: (lambda_C^2 c/H)^(1/3) = "
  + ", ".join(f"{XLH[m]:.2f}" for m in M_DARK) + " pc")
P(f"    the m window if xi = xi_q(m): canonical {M_WIN['canonical'][0]:.2e} .. {M_WIN['canonical'][1]:.2e} eV, alt {M_WIN['alt'][0]:.2e} .. "
  f"{M_WIN['alt'][1]:.2e} eV (FP10's floor 1.9-5.2e-19 inside)")
OUT["numbers"]["B2"] = dict(exponents=str(solB), lambda_C_pc=LC, xi_q_pc={f"{k2[0]}|{k2[1]}": v2 for k2, v2 in XIQ.items()}, xi_L_pc=XLH, m_window_eV=M_WIN)
check("B2 THE LENGTHS m SUPPLIES: from (hbar/m, a0, c) every length is lambda_C (lambda_C a0/c^2)^q (sympy); the Compton length "
      f"hbar/(m c) = {min(LC.values()):.1e}-{max(LC.values()):.1e} pc is {min(XI_FLOOR.values()) / max(LC.values()):.0f}x below the floor, and the one "
      f"c-free member, xi_q = ((hbar/m)^2/a0)^(1/3) (the dark field's Airy length at a0), is {min(XIQ.values()):.2f}-{max(XIQ.values()):.2f} pc -- "
      "inside the window.  So are other exponents (q = -1/4, the Lambda-mixed (lambda_C^2 c/H)^(1/3)): NUMEROLOGY until an action "
      "makes the MOND readout smooth over it (B3, B4)",
      f"exponents {solB}; lambda_C {max(LC.values()):.1e} pc; xi_q {min(XIQ.values()):.2f}-{max(XIQ.values()):.2f} pc; m window {M_WIN['canonical'][0]:.1e}-"
      f"{M_WIN['canonical'][1]:.1e} eV", max(LC.values()) < min(XI_FLOOR.values()) and all(min(XI_FLOOR.values()) < v2 < XI_CEIL_PC for v2 in XIQ.values()),
      reading="flagged NUMEROLOGY (as FP14 X1's integer-power hits): no term in the action relates the heat pair's depth to m")

# ---- B3: a state coupling (the readout kernel built from the dark field's local coherence) in FP10's cleared galaxies
ret575, ret650 = RETAINED["575.0"], RETAINED["650.0"]
b3_ok = (ret575["dwarf"] == 0 and ret575["SPARC disc"] == 0 and ret650["SPARC disc"] == 0 and ret575["Milky Way"] < 1e-2)
check("B3 A STATE COUPLING DIES WHERE FP10 CLEARED THE FIELD: a readout that smooths the MOND source over the dark field's coherence "
      "length needs the field present -- its kernel's amplitude is ~ |Psi|^2 (normalised, 0/0 where the field is gone).  FP10 clears "
      f"galaxies at collapse: retained fraction dwarf {ret575['dwarf']}, SPARC disc {ret575['SPARC disc']}, Milky Way {ret575['Milky Way']:.1e} (575 km/s; "
      f"{ret650['Milky Way']} at 650).  With no field the MOND source is switched off (SPARC -> Newtonian {SP_N['canonical'][0]:.3f} dex, KiDS "
      f"{KI_N['canonical']:.0f}) or undefined; and any such coupling gives the dark field a MOND-sector source S != 0 (FP8's energy-reciprocity "
      "identity), which FP10's clearing was built to avoid",
      f"retained 575: {ret575}; 650: {ret650}; SPARC with the source off {SP_N['canonical'][0]:.4f} dex", b3_ok)

# ---- B4 (reported): the parameter tie
check("B4 (reported) THE PARAMETER TIE xi = xi_q(m) HAS NO DYNAMICS: the heat pair's depth b = xi^2/2 would be written as a function "
      "of another sector's mass parameter with nothing in the action connecting them (the dark field's Schroedinger kernel e^{i hbar t "
      "Delta/2m} is oscillatory, not the real heat kernel; a Wick rotation is not something an action does).  As FP10 C3 found for eps, a "
      "tie through a declared, floor-only m moves the knob into m: SHARED at best, and only by postulate",
      f"xi_q(m) = {min(XIQ.values()):.2f}-{max(XIQ.values()):.2f} pc at FP10's floor; m would then carry xi's role (window {M_WIN['canonical'][0]:.1e}-"
      f"{M_WIN['canonical'][1]:.1e} eV)", True, load_bearing=False)
P(f"    {el()}")

# ============================================================================================================== C route (c)
banner("C  (c) CURVATURE-KEYED READOUTS: density (Ricci) keys, tidal (Weyl) keys, and the second variation of a keyed depth")
# ---- C1: density keys
N_SW, N_LISM = 5.0, 0.2                                                # cm^-3: quiet solar wind at 1 AU; local interstellar cloud (inputs)
rho_sw = {pl: N_SW * 1e6 * 1.67262192e-27 / a_ ** 2 for pl, a_ in PLANETS.items()}
rho_disc = RHO_B_LOCAL * MSUN_PC3
rho_lism = N_LISM * 1e6 * 1.67262192e-27
T_q2 = 2 * GM_SUN / (M1[("canonical", 2.32e-10)]["v50"]["r_pc"] * PC_M) ** 3
ratio_sun = 4 * math.pi * Gn * rho_lism / T_q2
DISC_CASES = {"solar-neighbourhood disc": (0.1, 1.0), "inner disc": (10.0, 1.0), "gas-poor (elliptical) centre": (1.0, 1e-3)}   # (n_* pc^-3, n_gas cm^-3)
m_star = 0.5                                                          # Msun, a typical star


def vac_ratio(n_star, n_gas):
    T_star = 2 * Gn * m_star * MSUN / (n_star ** (-1 / 3) * PC_M) ** 3  # the nearest star's tide at the mean spacing
    return 4 * math.pi * Gn * n_gas * 1e6 * 1.67262192e-27 / T_star


RATIOS = {k2: vac_ratio(*v2) for k2, v2 in DISC_CASES.items()}
ratio_disc = RATIOS["solar-neighbourhood disc"]
P("    rho at the planets (solar wind ~ r^-2) [kg/m^3]: " + ", ".join(f"{pl} {v2:.1e}" for pl, v2 in rho_sw.items())
  + f";  the Galactic disc (Oort limit 0.1 Msun/pc^3) {rho_disc:.1e};  the local interstellar cloud {rho_lism:.1e}")
P(f"    the dimensionless vacuum key 4 pi G rho/|T| (constant-free): the Sun's Q2 region {ratio_sun:.1e}; galaxy points (gas density vs the "
  "nearest star's tide at the mean spacing): " + ", ".join(f"{k2} {v2:.1e}" for k2, v2 in RATIOS.items()))
OUT["numbers"]["C1"] = dict(rho_planets=rho_sw, rho_disc=rho_disc, rho_lism=rho_lism, vacuum_ratio_sun=ratio_sun, vacuum_ratio_galaxies=RATIOS)
check("C1 DENSITY (RICCI) KEYS CANNOT SCREEN THE PLANETS: R = 8 pi G rho/c^2 reads the local matter, and the planets orbit in a "
      f"vacuum no denser than a galaxy disc (solar wind {rho_sw['Earth']:.0e} kg/m^3 at 1 AU, {rho_sw['Saturn']:.0e} at Saturn; the disc "
      f"{rho_disc:.0e}; the Sun's Q2 region sits in the interstellar cloud, {rho_lism:.0e}): a threshold rho_* that screens Saturn screens every "
      "galaxy disc.  The constant-free ratio 4 pi G rho/|T| does separate the Sun's Q2 region "
      f"({ratio_sun:.0e}) from galaxy points ({min(RATIOS.values()):.0e}-{max(RATIOS.values()):.0e}), but only through a new small threshold (between "
      f"{ratio_sun:.0e} and the gas-poor centres' {min(RATIOS.values()):.0e}) and by switching MOND on and off with the local gas at sub-parsec scales: "
      "not a derivation (the record's L-closure: density keys swing with the averaging scale)",
      f"rho(Saturn)/rho_disc = {rho_sw['Saturn'] / rho_disc:.1e}; rho(Earth)/rho_disc = {rho_sw['Earth'] / rho_disc:.2f}; vacuum ratios {ratio_sun:.1e} vs "
      + ", ".join(f"{v2:.1e}" for v2 in RATIOS.values()),
      rho_sw["Saturn"] < rho_disc and rho_sw["Earth"] < 3 * rho_disc and ratio_sun < 1e-4)

# ---- C2: tidal (Weyl) keys -- the threshold is a new length
r95 = max(m_["v05"]["r_pc"] for m_ in M1.values()) * PC_M
T_sun_min = 2 * GM_SUN / r95 ** 3
Tg = []
for U in (0.5, 0.7, 0.9):
    iu = int(np.argmin(np.abs(UPS - U)))
    for f, a0 in A0.items():
        m_ = OKS[:, iu] & (GB[:, iu] / a0 <= y_hi)
        Tg.append(float((2 * GB[:, iu] / _R)[m_].max()))
T_gal_max = max(Tg)
ell_win = (cc / math.sqrt(T_sun_min), cc / math.sqrt(T_gal_max))
ell_fw = {"c/H_Lambda": cc / H_FOOT["canonical"], "c^2/a0": cc ** 2 / A0["canonical"]}
P(f"    tidal field |T| ~ 2 G M/r^3: the Sun's Q2 region (r <= {r95 / PC_M:.3f} pc) >= {T_sun_min:.1e} s^-2; SPARC points with y <= {y_hi:.0f} "
  f"(2 g_bar/R, conservative) <= {T_gal_max:.1e} s^-2 -> a threshold T_* = (c/ell_*)^2 needs ell_* in [{ell_win[0] / KPC:.0f}, {ell_win[1] / KPC:.0f}] kpc; "
  "the framework's lengths: " + ", ".join(f"{k2} = {v2 / MPC / 1e3:.1f} Gpc" for k2, v2 in ell_fw.items()))
OUT["numbers"]["C2"] = dict(T_sun_min=T_sun_min, T_gal_max=T_gal_max, ell_window_kpc=[ell_win[0] / KPC, ell_win[1] / KPC])
check("C2 TIDAL (WEYL) KEYS NEED A NEW LENGTH: the Weyl tensor is the tidal field, nonzero in vacuum, so it can see the Sun's Q2 region "
      f"(|T| >= {T_sun_min:.0e} s^-2) against every SPARC point with y <= {y_hi:.0f} (<= {T_gal_max:.0e}) -- but only through a threshold "
      f"(c/ell_*)^2 with ell_* in [{ell_win[0] / KPC:.0f}, {ell_win[1] / KPC:.0f}] kpc; the framework's lengths (c/H_Lambda, c^2/a0) are Gpc "
      "(a Weyl key at Lambda is M4's constant-free row: galaxies screened).  This is M2's mass threshold again, now as a length",
      f"ell_* window {ell_win[0] / KPC:.0f}-{ell_win[1] / KPC:.0f} kpc vs {ell_fw['c/H_Lambda'] / MPC / 1e3:.1f} Gpc",
      ell_win[0] < ell_win[1] and ell_fw["c/H_Lambda"] > 100 * ell_win[1])

# ---- C3: the second variation of a curvature-keyed readout depth (FP14 X3b at one more derivative)
tC3 = time.time()
T2b, V2b, h2b, q2b = reduce_TV(unitary_block(2), ["psi", "phi"], ["n", "B"])
u_ = sp.Symbol('u', real=True)
V11_c3 = 4 * kq_ ** 2 * (2 - alm) * (1 + K2b * kq_ ** 2) ** 2 / (2 - (2 - alm) * (1 + K2b * kq_ ** 2) ** 2)
c3_form = sp.simplify(V2b[0, 0] - V11_c3) == 0
detV2 = sp.factor(sp.simplify(V2b.det()))
det_target = 16 * Cph * kq_ ** 4 * (2 - alm) * (1 + K2b * kq_ ** 2) ** 2 / (2 - (2 - alm) * (1 + K2b * kq_ ** 2) ** 2)
c3_det = sp.simplify(detV2 - det_target) == 0
c3_ctl = sp.simplify(V2b.subs(K2b, 0) - V_fp7) == sp.zeros(2, 2)
Dden = lambda u, a: 2 - (2 - a) * (1 + u) ** 2
# instability: D < 0 for u > u+ = sqrt(2/(2 - a)) - 1 ~ a/4, or u < u- = -1 - sqrt(2/(2 - a)) ~ -2
AC_MAX = 3.2e-9
u_plus = math.sqrt(2 / (2 - AC_MAX)) - 1
u_minus = -1 - math.sqrt(2 / (2 - AC_MAX))
unstable_ok = Dden(2 * u_plus, AC_MAX) < 0 and Dden(1.01 * u_minus, AC_MAX) < 0 and Dden(-1.0, AC_MAX) > 0 and Dden(0.5 * u_plus, AC_MAX) > 0
# an illustrative K_2 at a key's transition: K_2 ~ 4 pi G rho_ph xi^2/T_* (FP14's vacuum phantom at the Sun, xi at the floor, T_* mid-window)
rho_ph = fp14["numbers"]["X3"]["rho_ph_scored"] * MSUN_PC3
T_mid = math.sqrt(T_sun_min * T_gal_max)
K2_ill = 4 * math.pi * Gn * rho_ph * (XI_FLOOR["canonical"] * PC_M) ** 2 / T_mid
lam_c3 = {"K_2 > 0": 2 * math.pi * math.sqrt(K2_ill / u_plus), "K_2 < 0": 2 * math.pi * math.sqrt(K2_ill / abs(u_minus))}
P(f"    curvature-keyed readout delta chi = sigma delta phi + K_2 d_z^2 delta n:  V_11 = {sp.factor(V2b[0, 0])}  ({time.time() - tC3:.1f} s)")
P(f"    = 4k^2 (2 - alpha_c)(1 + u)^2/(2 - (2 - alpha_c)(1 + u)^2), u = K_2 k^2: {c3_form};  det V has the same denominator: {c3_det};  "
  f"unstable for u > {u_plus:.1e} or u < {u_minus:.3f} (alpha_c = {AC_MAX:.1e});  illustrative K_2 ~ {K2_ill:.1e} m^2 -> unstable below "
  + ", ".join(f"{k2}: {v2 / AU_M:.0f} AU" for k2, v2 in lam_c3.items()))
OUT["numbers"]["C3"] = dict(V11=str(sp.factor(V2b[0, 0])), u_plus=u_plus, u_minus=u_minus, K2_illustrative=K2_ill,
                            lambda_crit_AU={k2: v2 / AU_M for k2, v2 in lam_c3.items()})
check("C3 A CURVATURE-KEYED READOUT DEPTH IS UNSTABLE UNLESS SATURATED (derived: FP14 X3b at one more derivative): if the depth reads the "
      "tidal field d_z^2 Phi/c^2 = d_z^2 delta n, the reduced block becomes V_11 = 4k^2 (2 - alpha_c)(1 + u)^2/(2 - (2 - alpha_c)(1 + u)^2) "
      f"with u = K_2 k^2 (det V likewise, Hermitian {h2b}, quadratic {q2b}): a gradient instability for u > ~alpha_c/4 (K_2 > 0) or u < -2 "
      "(K_2 < 0) -- every nonzero K_2 at short enough wavelengths, since alpha_c <= 3.2e-9 is the lapse's only stiffness.  Control: K_2 = 0 "
      "returns FP7's healthy V.  So a Weyl key may only switch where nothing varies -- it cannot be the Solar System's screen",
      f"V_11 form {c3_form}; det {c3_det}; control {c3_ctl}; thresholds u+ {u_plus:.2e}, u- {u_minus:.4f}; illustrative critical wavelengths "
      + ", ".join(f"{v2 / AU_M:.0f} AU" for v2 in lam_c3.values()), c3_form and c3_det and c3_ctl and h2b and q2b and unstable_ok)

# ---- C4 (reported): c_T and PPN of curvature keys
check("C4 (reported) c_T AND PPN OF CURVATURE KEYS: a key read from the matter's Newtonian field (the heat branch) leaves transverse-"
      "traceless modes untouched (c_T = 1, FP7 D1) and is saturated inside the Solar System (PPN = FP7 D2's filtered values); a key read from "
      "the metric's Weyl tensor E_ij (linear in h_TT) puts b'(E^2) (delta E)^2 ~ (d_t^2 h_TT)^2 into the graviton's action around every "
      "source (higher time derivatives, a direction-dependent c_T) -- the record's curvature-coupled clock (Case 3a: c_T excluded 1e7-1e9x) "
      "and door04 (Weyl^2: an opposite-residue spin-2 ghost).  Neither removes C2's new length or C3's instability",
      "cited, not recomputed", True, load_bearing=False)

# ---- C5 (reported): the one family theorem M does not cover -- keys on the EXTERNAL field
e_over_a0 = {f: 2.32e-10 / A0[f] for f in A0}
check("C5 (reported) EXTERNAL-FIELD KEYS ARE OUTSIDE THEOREM M, AND NOT A DERIVATION: at the Sun's Q2 region the Galaxy's field is "
      f"e = {e_over_a0['canonical']:.1f} a0 (O(1)), so an external-field threshold of order a0 could screen the Sun with no small number -- but "
      "'external' is relational (york/L_CLOSURE_VERDICT, Theorem 8: it needs a segmentation of rho), the record's ESCREEN realises it with "
      "an auxiliary field whose boundary data encode the segmentation and FITS its threshold (york/ESCREEN_Q2_VERDICT), a local proxy (the "
      "angle between g and the tidal axes) is direction-dependent around the Sun (aligned along e-hat) and would leave an anisotropic phantom, "
      "i.e. a Q2 of its own, and every such key screens all EFE-dominated systems alike (wide binaries at s ~ 7 kAU, satellites, the outer "
      "profiles of KiDS lenses in the web's field) while leaving the planets' aligned high-y region to a separate switch (k04: the monopole "
      "only).  OPEN as a construction; not pursued here",
      f"e/a0 at the Sun {e_over_a0['canonical']:.2f} / {e_over_a0['alt']:.2f}", True, load_bearing=False)
P(f"    {el()}")

# ============================================================================================================== R re-scores
banner("R  THE BEST CANDIDATES ON EVERY GATE")
# ---- R1: the best constant-free action candidate -- BDEF's Riemann Galileon with k^(1/4) = c/H (V3)
R1 = {}
for f, a0 in A0.items():
    k = K_FREE[f]
    ss = {}
    for pl, a_ in PLANETS.items():
        r = a_ * AU_M
        gN = GM_SUN / r ** 2
        ss[pl] = float(x_screened(gN / a0, rho_bdef(k, a0, gN, r))) * a0
    mono = ss["Saturn"] * R_SAT ** 2 / Gn / M_SAT_BOUND
    r50 = M1[(f, 2.32e-10)]["v50"]["r_pc"] * PC_M
    y50 = GM_SUN / r50 ** 2 / a0
    supp = float(x_screened(y50, rho_bdef(k, a0, y50 * a0, r50))) / float(x_p2(y50))
    q2 = Q2C[(f, 2.32e-10)]["q2"] * supp
    # c_T estimate in the Galileon interior (r_V(MW) >> the Sun): delta c_T ~ 4 k phi'^2 phi'' (V4's estimate) with phi' = r/sqrt(8k)
    # -> r^2/(2 sqrt(8k)); delay over the GW path inside r_V of the MW and of the host (~ r_V^3/(6 sqrt(8k) c) each)
    rVmw = (8 * k * Gn * 6e10 * MSUN * a0) ** 0.25 / cc
    rVh = (8 * k * Gn * M_HOST * a0) ** 0.25 / cc
    dt_ct = sum(min(rv, 40 * MPC) ** 3 / (6 * math.sqrt(8 * k) * cc) for rv in (rVmw, rVh))
    ppn = ss["Earth"] / (GM_SUN / AU_M ** 2)
    R1[f] = dict(ss=ss, mono=mono, q2=q2, sparc=sp_b_free[f][0], kids=ki_b_free[f] - KI_P2[f], flag=fl_b_free[f], ct_delay_s=dt_ct, ppn=ppn,
                 s8=S8_HY[str((f, 'permode'))])
    P(f"    {f:9s}: Earth {ss['Earth']:.1e}, Mars {ss['Mars']:.1e}, Saturn {ss['Saturn']:.1e} m/s^2 (gate {A_SUNWARD:.1e}); monopole {mono:.1e} of the "
      f"bound; Q2/ceil {q2:.1e} (the Q2-median scalar suppressed x{supp:.1e}); SPARC {R1[f]['sparc']:.4f} dex; KiDS {R1[f]['kids']:+.0f}; "
      f"flagship {R1[f]['flag']:+.3f} dex; PPN (MOND fraction at 1 AU) {ppn:.1e}; sigma_8 (per-mode) {R1[f]['s8']:.4f}; c_T on FRW = 1 "
      f"(phibar frozen), static-gradient GW delay (estimate) {dt_ct:.1e} s")
OUT["numbers"]["R1"] = R1
gates_R1 = {f: dict(solar_system=max(v2 / A_SUNWARD for v2 in R1[f]["ss"].values()) < 1 and R1[f]["mono"] < 1 and R1[f]["q2"] < 1,
                    sparc=R1[f]["sparc"] <= SP_P2[f][0] + 0.005, kids=R1[f]["kids"] <= 9, flagship=abs(R1[f]["flag"]) <= FLAG_TOL_FP10,
                    ppn=R1[f]["ppn"] < 1e-9, sigma8=0.922 <= R1[f]["s8"] <= 1.05) for f in A0}
P("    gate table (constant-free BDEF): " + "; ".join(f"{f}: " + ", ".join(f"{g2} {'pass' if ok2 else 'FAIL'}" for g2, ok2 in gt.items())
                                                   for f, gt in gates_R1.items()))
P("    c_T: FRW exact (phibar frozen by the yield; the Paul term's G5X X H phidot vanishes); static gradients: the estimate above (reported, "
  "not load-bearing); readout force / FC-KH (FP14 X3/X3b): no readout depth; the Galileon-lapse mixing through R_0i0j = d_i d_j N/c^2 "
  "is OPEN; stability of the Paul term: OPEN (BDEF's ref. [34], 'in preparation', never scored; Route 2's cubic analogue has c_r^2 = 4/3)")
r1_ok = all(gates_R1[f]["solar_system"] and gates_R1[f]["ppn"] and gates_R1[f]["sigma8"] and not gates_R1[f]["sparc"] and not gates_R1[f]["kids"]
            and not gates_R1[f]["flagship"] for f in A0)
check("R1 THE BEST CONSTANT-FREE CANDIDATE, ON EVERY GATE, FAILS: BDEF's Riemann Galileon on the chain's root with k^(1/4) = c/H passes "
      "the Solar System (deeply screened), PPN, FRW (the term is cubic in phi and phibar is frozen: linear cosmology and sigma_8 = FP9's "
      "headline) and c_T on FRW -- and FAILS SPARC, KiDS and the flagship on both footings (V3), with a static-gradient GW170817 delay of "
      f"~{min(R1[f]['ct_delay_s'] for f in A0):.0e} s by estimate",
      "; ".join(f"{f}: " + ", ".join(f"{g2} {'pass' if ok2 else 'FAIL'}" for g2, ok2 in gt.items()) for f, gt in gates_R1.items()), r1_ok)

# ---- R2 (reported): the tie xi = xi_q(m) -- it IS the heat filter at 1.6-3.3 pc
xq_lo, xq_hi = min(XIQ.values()), max(XIQ.values())
ss_R2 = {f: {g2: fp7_gate(min(xq_lo, 1.0), g2, f) for g2 in ("Q2", "M", "gmax")} for f in ("canonical", "alt")}
sparc_R2 = 7.5 * (xq_hi * PC_M / (0.5 * KPC)) ** 2
k_yard = 20.0 * 0.6736 / MPC
s8_fac = math.exp(-(xq_hi * PC_M * k_yard) ** 2)
alpha1_leak = 1.3e-12
P(f"    xi = xi_q(m) = {xq_lo:.2f}-{xq_hi:.2f} pc: Solar System (FP7's table at >= 1 pc) " + ", ".join(
    f"{f}: " + "/".join(f"{v2:.1e}" for v2 in ss_R2[f].values()) for f in ss_R2) + f"; SPARC (FP1 C1's bound at a = 0.5 kpc) <= {sparc_R2:.1e}; "
  f"KiDS / flagship unchanged (xi << 30 kpc, << r_F); sigma_8: filter factor at k = 20 h/Mpc {s8_fac:.12f}; c_T = 1 (FP7 D1); PPN alpha_1 "
  f"leak <= {alpha1_leak:.1e} (FP7 D2 at the floor, smaller above); readout force / X3b: none (xi constant); wide binaries Newtonian to "
  f"s ~ {xq_lo * PC_M / AU_M:.0e} AU")
OUT["numbers"]["R2"] = dict(xi_q_pc=[xq_lo, xq_hi], solar_system=ss_R2, sparc_bound=sparc_R2, s8_factor=s8_fac)
check("R2 (reported) THE TIE CANDIDATE PASSES EVERY GATE -- BECAUSE IT IS THE HEAT FILTER: xi = ((hbar/m)^2/a0)^(1/3) = "
      f"{xq_lo:.2f}-{xq_hi:.2f} pc sits inside xi's window, so the Solar System, SPARC, KiDS, the flagship, c_T, PPN, sigma_8 and FP14's "
      "readout-force and X3b rows are the heat filter's own (all pass; a constant xi has no readout gradient).  It removes nothing: the "
      "relation to m is NUMEROLOGY (B2-B4), and it predicts Newtonian wide binaries to ~1e5-1e6 AU",
      f"SS {ss_R2['canonical']}; SPARC <= {sparc_R2:.1e}; sigma_8 factor {s8_fac:.3e}",
      all(max(v2.values()) < 1 for v2 in ss_R2.values()) and sparc_R2 < 1e-3 and s8_fac > 1 - 1e-6, load_bearing=False)
P(f"    {el()}")

# ============================================================================================================== F count
banner("F  xi AFTER FP17")
COUNT = [("xi (heat-filter length)", "KNOB [0.0243/0.0268 pc, ~100 pc] (FP14)",
          "KNOB: no constant-free screening exists in routes (a)-(c) (M: it is a threshold mass, 0.4-7e6 Msun); the Riemann Galileon "
          "REPLACES it with k^(1/4) in [~100, ~200-400] kpc; the xi_q(m) tie is numerology", "M1-M4, V1-V4, B1-B4, C1-C3, R1-R2"),
         ("k (BDEF Galileon coupling)", "-", "not adopted: one fitted length for another, plus a Riemann-coupled term whose static c_T and "
          "stability are OPEN", "V4"),
         ("m (dark mass)", "DECLARED floor (FP10)", "unchanged; not tied to xi (no mechanism)", "B")]
for row in COUNT:
    P(f"    {row[0]:28s} | before: {row[1]:42s} | after: {row[2]}  [{row[3]}]")
OUT["numbers"]["F"] = [dict(constant=r2[0], before=r2[1], after=r2[2], basis=r2[3]) for r2 in COUNT]
check("F (reported) THE COUNT IS UNCHANGED: beyond (kappa, G, Lambda) the gravity core keeps ONE knob (xi) and ONE regulator (alpha_c); "
      "no route here eliminates or shares xi by a derivation", "xi: KNOB", True, load_bearing=False)

# ============================================================================================================== W ledger
banner("W  THE LEDGER: FP17")
LEDGER = [
    ("F17a", f"the strict law's Cassini Q2 is made at {r_lo_AU:.0f}-{r_hi_AU:.0f} AU (y_N {y_lo:.1f}-{y_hi:.0f}, C <= {C_sun_max:.0e}): the Sun at its own "
             "EFE transition, at the same y as galaxy interiors", "DERIVED", "M1 (f28's integrand, cumulative; FP14 X5 reproduced)"),
    ("F17b", f"at fixed y a local key sees only C ~ M^(1/2) (Buckingham); SPARC at the same y has C >= {C_gal_min:.0e}: every Solar-System screening "
             f"is a threshold MASS in [~1, ~{M_gal_min:.0e}] Msun", "DERIVED", "M2 (sympy nullspace; SPARC)"),
    ("F17c", f"no O(1) mass from (a0, Lambda, G, c) in the window: M_H (8 pi/kappa^2)^D needs D in [{D_win['canonical'][0]:.1f}, {D_win['canonical'][1]:.1f}]; "
             f"{len(hitsM)} integer hits and the Chandrasekhar-type {M_CH:.2f} Msun (needs m_p) are NUMEROLOGY", "FAILS", "M3"),
    ("F17d", "every constant-free construction puts the threshold mass at 1e20-1e22 Msun (galaxies screened); in-window rows carry a fitted "
             "length or are numerology", "DERIVED", "M4"),
    ("F17e", f"cubic Galileon, r_c = c/H_Lambda: r_V(1e11 Msun) = {min(rv11):.0f}-{max(V1[(f, 1e11)][1.0] / KPC for f in A0):.0f} kpc (the '~70 kpc' is low), "
             f"r_V/r_M >= {ratio_min:.0f}: galaxies screened", "FAILS", "V1 (sympy flux)"),
    ("F17f", f"cubic Galileon on P2 (Route 2 on the AQUAL root): constant-free R_* screens SPARC; for ANY R_* the window is empty "
             f"(>= {min(empty_cub.values()):.0e}): P2's pole beats a 1/r Galileon flux", "FAILS", "V2 (K5: Route 2 reproduced)"),
    ("F17g", "BDEF's Riemann Galileon on P2 beats the pole (interior force c^2 r/sqrt(8k)); with k^(1/4) = c/H it fails SPARC, KiDS and the "
             "flagship", "FAILS", "V3, R1"),
    ("F17h", f"BDEF with k fitted: k^(1/4) >= {max(fl_b_sat.values()) / KPC:.0f} kpc (Saturn), SPARC to ~{min(ceil_b.values()) / MPC:.0f} Mpc, GW170817 "
             f"(estimate) <= ~{min(ceil_gw.values()) / KPC:.0f} kpc: a REPLACEMENT of xi, not an elimination", "CONSTRAINT", "V4 (reported)"),
    ("F17i", "the tie k = L(0)^4 to FP9's separator length: Solar System and SPARC pass, GW170817 missed by the static-gradient c_T "
             "estimate", "OPEN", "V4 (an estimate; the Paul term's c_T on a static gradient is not derived here)"),
    ("F17j", f"de Broglie hbar/(m v) = {db_lo:.3f}-{db_hi:.3f} pc (verified); at FP10's kick speed <= {db_kick:.4f} pc, below the floor (monopole "
             f"{gate_kick['canonical']:.1f}x)", "FAILS", "B1"),
    ("F17k", f"xi_q = ((hbar/m)^2/a0)^(1/3) = {xq_lo:.1f}-{xq_hi:.1f} pc, the unique c-free length from (hbar/m, a0), inside the window: NUMEROLOGY "
             "(no action couples the heat depth to m); SHARED only by postulate", "FAILS", "B2, B4, R2"),
    ("F17l", "a readout keyed to the dark field's local coherence is absent where FP10 cleared the field (SPARC discs, dwarfs): MOND off, "
             "and S != 0", "FAILS", "B3 (FP10's retained fractions)"),
    ("F17m", "density (Ricci) keys: the planets' vacuum is no denser than a galaxy disc; the vacuum ratio needs a new small threshold",
     "FAILS", "C1"),
    ("F17n", f"tidal (Weyl) keys need ell_* in [{ell_win[0] / KPC:.0f}, {ell_win[1] / KPC:.0f}] kpc -- a new length", "FAILS", "C2"),
    ("F17o", "a curvature-keyed readout depth: V_11 = 4k^2 (2 - alpha_c)(1 + u)^2/(2 - (2 - alpha_c)(1 + u)^2), u = K_2 k^2: unstable unless "
             "saturated (the FC-KH lesson at one more derivative)", "DERIVED", "C3 (sympy, FP14's block)"),
    ("F17p", "not derived here: the Paul term's c_T on static gradients, the Galileon-lapse mixing (FC-KH for R_0i0j couplings), BDEF's "
             "stability, a leaf-projected Galileon's second-order property", "OPEN", "R1, V4"),
    ("F17q", "xi remains the gravity core's one knob; physically it encodes the stellar mass scale (a0 xi^2/G in [0.4, 7e6] Msun)",
     "CONSTRAINT", "F (verdict)"),
    ("F17r", "keys on the EXTERNAL field (outside theorem M): relational (Theorem 8), threshold FITTED in the record (ESCREEN), a local "
             "angle proxy is direction-dependent around the Sun; they screen every EFE-dominated system alike", "OPEN", "C5 (reported, not pursued)"),
]
for k2, what, status, basis in LEDGER:
    P(f"    {k2:6s} {status:11s} {what}  --  {basis}")
OUT["ledger"] = [dict(link=k2, what=w_, status=s_, basis=b_) for k2, w_, s_, b_ in LEDGER]
check("W (reported) the ledger of this lane", f"{len(LEDGER)} links", True, load_bearing=False)

# ============================================================================================================== verdict
n_lb_fail = sum(1 for _, ok, lb in CH if lb and not ok)
n_pass = sum(1 for _, ok, _ in CH if ok)
banner("VERDICT")
P("  xi       still a KNOB.  No Solar-System screening in routes (a)-(c) needs NO new constant, and the reason is one theorem (M):")
P(f"           Cassini's Q2 is made at {r_lo_AU:.0f}-{r_hi_AU:.0f} AU, where the Sun sits at the same y as galaxy interiors; the only local")
P("           discriminant left is C ~ M^(1/2), so every screen is a threshold MASS between ~1 Msun and the lightest galaxy, and")
P(f"           (a0, Lambda, G, c) supply only (c^4/G a0)(8 pi/kappa^2)^D with D ~ -9..-12.  xi ~ 0.6 r_M(Sun) encodes the Sun's mass.")
P("  (a)      Vainshtein / k-mouflage: with the framework's scale (c/H) every galaxy is screened -- the cubic Galileon's r_V(1e11) is")
P(f"           {min(rv11):.0f}+ kpc (not ~70); on P2 the cubic Galileon has an empty window for ANY R_* (Route 2's pole); BDEF's Riemann")
P("           Galileon beats the pole but with k^(1/4) = c/H fails SPARC, KiDS and the flagship.  With k FITTED it works in")
P(f"           [{max(fl_b_sat.values()) / KPC:.0f}, ~{min(ceil_gw.values()) / KPC:.0f}] kpc (GW170817 by estimate): it REPLACES xi with k, one knob for one.")
P(f"  (b)      hbar/(m v) = {db_lo:.3f}-{db_hi:.3f} pc is a coincidence (below the floor at FP10's kick speed); the unique c-free length")
P(f"           ((hbar/m)^2/a0)^(1/3) = {xq_lo:.1f}-{xq_hi:.1f} pc lands in the window but nothing in the action ties the heat depth to m, and a")
P("           state coupling dies in FP10's cleared galaxies: NUMEROLOGY (SHARED only by postulate).")
P(f"  (c)      density keys cannot see the planets' vacuum; tidal keys need a new {ell_win[0] / KPC:.0f}-{ell_win[1] / KPC:.0f} kpc length; a curvature-keyed")
P("           depth is gradient-unstable unless saturated (derived).  External-field keys lie outside theorem M but are relational")
P("           (Theorem 8) and fitted in the record (ESCREEN): OPEN, not a derivation.")
P("  COUNT    unchanged: 1 knob (xi) + 1 regulator (alpha_c).  Not 'zero knobs'.  The honest options: accept xi as the theory's one")
P("           length (and MEASURE it: the wide-binary transition at s ~ xi is the observable), or trade it for k with more structure.")
P(f"  Time {time.time() - T0:.0f} s.")
json.dump(OUT, open(os.path.join(HERE, f"{SLUG}_results.json".replace("_MUTATE_results", "_results_MUTATE")), "w"), indent=1, default=str)
P(f"\n  {n_pass}/{len(CH)} checks pass; load-bearing failures: {n_lb_fail}; wrote "
  f"{SLUG.replace('_MUTATE', '')}_results{'_MUTATE' if MUTATE else ''}.json")
sys.exit(0 if n_lb_fail == 0 else 1)
