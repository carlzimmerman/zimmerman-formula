#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR36 (part 1) -- THE TURNAROUND GATE AS AN ACTION TERM: MOND switched on only where the matter flow has stopped expanding
(theta_m = div u <= 0).  Is a velocity-divergence gate well posed where DE12/DE13's density gates are not?

WHY.  The chain's separators (FP13's H_S, FP19's H_K1) switch MOND on across the linear web once the leaf accelerates
(z < 0.635); XR26 found that this over-lenses the CMB (+4.9 sigma on the linear base).  The candidate keys the MOND switch
on the LOCAL expansion rate of the matter flow, theta_m = div u: MOND on where the flow has turned around (theta_m <= 0,
bound systems and their turnaround regions), off where it still expands (theta_m ~ 3H, the linear web).  The khronon cannot
supply this: its leaves are CMC, so K = <K>_h carries no local information.  This part writes the gate as an action term,
varies it, and tests well-posedness the way the record does (FP3 C1's static symbol, DE12's baryon stiffness budget on its
24 host layers, XR18's constraint-symbol standard); part 2 (XR36_bound_regions.py) scores KiDS, the Local Group,
clusters, the flagship and SPARC; part 3 (XR36_web_lensing.py) the web: CMB lensing, sigma_8 and the forest.

THE ACTION.  The matter flow is a fluid with Lagrangian coordinates q (Brown/Schutz; dust in the Brown-Kuchar form): the map
x(q, t), J = det(dx/dq), n = n_0(q)/J.  Then theta = div u = d ln J/dt: the gate reads the FIRST time derivative of the
deformation, so a gate W(theta) adds no second time derivative in Lagrangian variables (no Ostrogradsky mode) -- it is a
velocity-dependent term.  Per unit volume, with sigma B the MOND sector's contribution to the Lagrangian at fixed fields:
    L = (1/2) rho |u|^2 - rho e(rho) + sigma B(fields) W(theta/<K>_h) + (fields),        <K>_h = 3H on FRW
where W = 1 for theta <= 0 (MOND on) and W = 0 for theta >= <K>_h Delta_x (off).  The four ways the chain's action can switch
MOND off at fixed fields -- the QUMOND phantom energy +q W (FP1/FP3's core), an AQUAL stiffness -s Y (FP7's root: 'off' is
an infinitely stiff scalar), the yield -2 y sqrt(Y) (FP9/FP19), and the band-pass length (FP19 A2: dS/dB > 0) -- all LOWER
the Lagrangian when MOND turns off (check K3): sigma = +1 in the sense that the gate term is largest when MOND is on.

THE MATTER THE GATE READS (the coordinator's MS1 question).  theta_m is read on the BARYON flow.  The carrier's converted
daughters stream out of every galaxy at v_k = 575-650 km/s (FK1 K2, FP10) and through the web at 200-400 km/s (XR19):
their divergence is ~2 v_k/r >> 3H near galaxies, so the total-matter reading would switch MOND OFF around every galaxy
whose carrier has converted -- a leak in exactly the wrong place (check A7).  MS1's rule (read baryons, never the carrier)
is therefore followed; its price is that the kinetic term in the symbols below carries rho_b, not rho_m.

PRE-DECLARED (written before this script's first run; the exploratory scratch runs listed under DISCLOSED came first).
 H1 [load-bearing; MUTATE must fail] THE STATIC SECTOR IS UNTOUCHED.  Expanded to second order about a static (and a Hubble-flow)
    background, the gate term sigma B J W(J-dot/J) contributes only (1/2) sigma B W'' (div xi-dot)^2 (the W' terms cancel
    identically; W_0 B J is a null Lagrangian at second order): no k^0 and no k^2 POTENTIAL term.  FP3 C1's static symbol has
    no gate term and DE12's c_gate^2 = rho_b S is identically ZERO for the theta gate.  A density-read gate (the MUTATE) puts
    (1/2) sigma B W'' (rho-derivatives)^2 (div xi)^2 into the potential and brings FP3's zero back.
 H2 THE KINETIC SECTOR: the compressive velocity symbol is m(k) = rho_b + sigma B W''_theta k^2 (static and moving backgrounds:
    delta theta = i k.D_t xi + O(k^0)); the dispersion relation omega^2 = K(k)/m(k) has a POLE at k_g^2 = rho_b/(-sigma B W'')
    wherever sigma W'' < 0.  The stability rule is the MIRROR of FP3 C1: density gates must be CONCAVE in rho, theta gates must
    make the Lagrangian CONVEX in theta.
 H3 [load-bearing] THE MIRROR LEMMA.  A gate that saturates on the turned-around side (MOND fully on, W flat, for all
    theta <= 0) and is lower on the expanding side cannot make L convex in theta, because sigma = +1 in every formulation (K3):
    L_g(theta) is flat and then decreasing, so L_g'' < 0 somewhere in (0, Delta_x <K>).  Verified on DE12's C-infinity step
    (every width, the sharp limit included), the linear ramp (a concave kink at theta = 0) and the four formulations.  The
    ghost sits at the switch-on, i.e. at the turnaround layer and inside virialised systems (theta ~ 0).
 H4 [load-bearing] THE NUMBERS on DE12's own 24 host layers (z = 0.25, 1, 2.5, 4; M_b = 1e10, 1e11, 1e12; both footings;
    DE12's gas rho_b = f_b(rho_NFW + rho_bar) and DE12's B = a0^2 q(y)/(8 pi G)), with the gate at its natural width
    Delta_x = 1 (from turnaround to the Hubble flow): the compressive velocity symbol is NEGATIVE at k = 1/kpc on every
    layer (a ghost at DE12's own scale), the pole k_g lies at 1/k_g <= 1 Mpc on every layer, and the static c_gate is 0.
    Expected ghost scales 1/k_g ~ 20-200 kpc; the growth at 1/kpc for 1e6 K gas Gamma ~ 10-100 H (NOT DE12's 1e3-5e4 H:
    the theta gate's pathology is a ghost with a pole, not a fast Jeans-type instability).
 H5 THE SMOOTHEST WELL-POSED VERSIONS AND THEIR PRICE.  (a) CONVEX (unsaturated) W = max(0, 1 - x/Delta_x): the Lagrangian is
    convex, the kinetic symbol positive, the gate well posed; but W = 1 + |x|/Delta_x in contracting regions, so SPARC's
    0.01 dex needs |theta_R| <= 0.023 Delta_x <K> in every SPARC host, which a host accreting a fraction f_acc of its mass per
    Hubble time violates for f_acc >~ 0.07 Delta_x.  (b) FILTERED argument theta_R = S_R[theta] (the chain's leafwise heat
    kernel at a length R): m(k) >= rho_b - B |W''_theta|/(e R^2), so it is well posed iff R >= R_min = sqrt(B|W''_theta|/(e rho_b))
    on every switch-on layer; expected R_min from ~0.1 Mpc (galaxy layers) to >~ 1 Mpc (clusters), so no single R keeps every
    layer healthy AND stays below the turnaround radius of isolated 1e10-1e11 galaxies (part 2: 0.2-0.5 Mpc).
 H6 [MS1] the total-matter reading leaks: at r = 0.3-3 Mpc the daughters' divergence 2 v_k/r exceeds <K>_h(z = 0.25) by a
    factor >= 1 (>= 10 inside 0.3 Mpc), so any outstreaming daughter fraction moves the switch-on inward (part 2 prices it).

CHECKS
  K  K1 CONTROL (FP3 C1): this lane's engine rebuilds FP3 C1's static symbol for the density gate and matches FP3's committed
     det, zero and local term exactly (sympy); K2 CONTROL (DE12): DE12's transition() (definitions only, XR18's recipe)
     reproduces DE12's committed c_gate_max and Gamma(1/kpc)/H on all 24 layers (<= 1e-12); K3 the sign: MOND-on raises the
     Lagrangian at fixed fields in all four formulations (q >= 0 on P2; -s Y, -2 y sqrt(Y) decreasing; FP19 A2's committed I > 0).
  A  A1 [H1, headline] the static sector (sympy, 1-D and 3-D, static and Hubble-flow backgrounds); A2 [H2] the kinetic symbol
     and the pole (sympy); A3 [H3] the mirror lemma; A4 [H4] DE12's 24 layers; A5 (reported) the pole's growth band;
     A6 [H5] the well-posed variants and their price; A7 [H6, reported] MS1: baryons vs total matter; A8 (reported) the
     gate's first-order effects: its own force and the Raychaudhuri feedback at the switch-on.
  W  the ledger.
MUTATE=1: the gate reads the baryon DENSITY (FP3's class, W(rho_b/rho_*)) instead of theta: A1 must FAIL (rc = 1).

SCOPE.  Frozen-coefficient (WKB) analysis on DE12's backgrounds, fluid baryons (isothermal gas at 1e6 K as DE12), the QUMOND
form of the MOND energy for B (DE12's convention; the AQUAL stiffness and yield forms are treated by K3/A3 and have a larger
concave coefficient).  No nonlinear evolution of the ghost is computed.  kappa = 1/2 is FITTED (Z = kappa = 5.7888) and does
not enter; both a0 footings (9.3603e-11, 1.1312e-10 m/s^2) are carried through DE12's layers.  Nothing here closes the theory.

DISCLOSED.  Exploratory scratch runs (not in the repository) were made before this file was written: the spherical flow
model of part 2 (turnaround and theta = 0 radii), the Zel'dovich web census of part 3, and the maximum curvature of DE12's
C-infinity step (9.84 at t = 0.218).  They informed H4's and H5's expected ranges.  Four debug runs of this file preceded the
recorded runs: two MUTATE runs stopped on sympy calls (the null-Lagrangian test and the Hubble-flow series, rewritten as a
direct Euler-Lagrange derivative and a log-derivative identity); a first official-attempt main run stopped in A1 because
sympy's series cannot collect mixed derivatives (the expansion now runs on plain symbols A = grad xi, B = its rate, with the
same content; MUTATE was re-run after the rewrite); a MUTATE run completed and showed a coding error (A4's pass
condition also required MUTATE = 0, coupling it to the control; removed so that MUTATE flips only A1).  The same run showed
that two of H4's EXPECTATIONS were false: 1/k_g is 132-1756 kpc (not 20-200: the ghost reaches LARGER scales) and
Gamma(1/kpc) is 0.7-4.7 H (not 10-100 H).  H4's pass condition (1/k_g <= 1 Mpc on every layer) is kept exactly as declared
and fails on the 1e12 layers at z = 0.25 and 1 (1/k_g = 1.1-1.8 Mpc) -- a failure in the direction of MORE ghost.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR36_gate_action.py   (MUTATE=1 for the
control).  Writes XR36_gate_action[_MUTATE].out and XR36_gate_action_results[_MUTATE].json next to itself.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "2"
import sys, io, json, math, time, contextlib, warnings
warnings.filterwarnings("ignore")
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CHAIN = os.path.join(REPO, "real_research", "derivation_chain_2026")
MUTATE = os.environ.get("MUTATE", "0") == "1"
NAME = "XR36_gate_action"
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


sys.stdout = _Tee(TXT)
OUT = {"lane": "XR36", "part": "1: the gate as an action term", "mutate": MUTATE, "checks": {}, "numbers": {}, "ledger": []}
CH = []


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)


def el():
    return f"[{time.time() - T_START:.0f} s]"


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing, "name": name}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the gate reads the baryon DENSITY (FP3's class) instead of theta -- A1 must FAIL ***")

# ================================================================================================ machinery (read-only)
FP0 = json.load(open(os.path.join(CHAIN, "FP0_core_postulates_results.json")))["numbers"]
A0 = {"canonical": FP0["a0_canonical"], "alt": FP0["a0_rho_total"]}
FOOTS = ("canonical", "alt")
P12 = os.path.join(REPO, "real_research", "dark_energy_2026", "DE12_mond_sector_gate_stiffness.py")
D12 = {"__name__": "de12", "__file__": P12}
_s12 = open(P12).read()
_head = _s12.split("# ============================================================================================ C1 the amplification")[0]
_trans = _s12.split("# ============================================================================================ the transitions")[1].split(
    "# ============================================================================================ G1 G2 the budget")[0]
_trans = _trans.split('banner("C2')[0]
_old = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec((_head + _trans).replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), D12)
finally:
    if _old is None:
        os.environ.pop("MUTATE", None)
    else:
        os.environ["MUTATE"] = _old
transition, Wd, CS, KPC, MS, G12, Hz12 = D12["transition"], D12["Wd"], D12["CS"], D12["KPC"], D12["MS"], D12["G"], D12["Hz"]
nu_of, ynup_of, q_of = D12["nu_of"], D12["ynup_of"], D12["q_of"]
MPCm = 1e3 * KPC
R12 = json.load(open(os.path.join(REPO, "real_research", "dark_energy_2026", "DE12_mond_sector_gate_stiffness_results.json")))["numbers"]
F3 = json.load(open(os.path.join(CHAIN, "FP3_cosmology_linear_results.json")))["numbers"]
F19 = json.load(open(os.path.join(CHAIN, "FP19_hs_repair_results.json")))["numbers"]
GAL = [(z, Mb, f) for z in (0.25, 1.0, 2.5, 4.0) for Mb in (1e10, 1e11, 1e12) for f in FOOTS]
KEY = lambda z, Mb, f: f"{z}/{Mb:.0e}/{f}"
P(f"\n  machinery: DE12's transition() definitions only (XR18's recipe; its constants, kernel tables and gas profiles); FP3, "
  f"FP19, DE12 committed JSONs; a0 = {A0['canonical']:.4e} / {A0['alt']:.4e} m/s^2   {el()}")

# ================================================================================================ K controls
banner("K  CONTROLS: FP3 C1's static symbol; DE12's 24 layers; the sign of the MOND energy in every formulation")
# K1: FP3 C1 rebuilt (the density gate reading the lapse Laplacian; same bracket as FP3's)
k2 = sp.symbols("k2", positive=True)
B_, Wpp, Wb, CT, Cn = sp.symbols("B W2 Wbar C_T C", real=True)
psi_, phi_, U_, drho, Gc = sp.symbols("psi phi U delta_rho G", real=True)
L2 = (2 * k2 * psi_ ** 2 - 4 * k2 * phi_ * psi_ + 2 * k2 * (U_ - phi_) ** 2
      + (B_ / 2) * Wpp * (Cn * k2 * phi_) ** 2 + 2 * Wb * CT * k2 * U_ ** 2 - 16 * sp.pi * Gc * drho * phi_)
Xv = [psi_, phi_, U_]
Mk = sp.Matrix(3, 3, lambda i, j: sp.diff(L2, Xv[i], Xv[j]))
detM = sp.factor(Mk.det())
roots = [r_ for r_ in sp.solve(sp.Eq(detM, 0), k2)]
Jv = sp.Matrix([-sp.diff(L2, x_).subs({psi_: 0, phi_: 0, U_: 0}) for x_ in Xv])
dphi_s = sp.simplify(Mk.LUsolve(Jv)[1])
eps_ = sp.symbols("e", positive=True)
dphi_ser = sp.series(sp.simplify(dphi_s.subs(Wpp, eps_ / (B_ * Cn ** 2))), eps_, 0, 2).removeO()
newton = sp.simplify(dphi_ser.subs(eps_, 0))
local = sp.simplify(dphi_ser - newton)
ref_c1 = F3["C1"]
loc_ns = {"k2": k2, "B": B_, "C": Cn, "C_T": CT, "W2": Wpp, "Wbar": Wb, "G": Gc, "delta_rho": drho, "e": eps_, "pi": sp.pi}
k1_ok = (sp.simplify(detM - sp.sympify(ref_c1["det"], locals=loc_ns)) == 0
         and sp.simplify(roots[0] - sp.sympify(ref_c1["zero_k2"], locals=loc_ns)[0]) == 0
         and sp.simplify(local - sp.sympify(ref_c1["local_term"], locals=loc_ns)) == 0
         and sp.simplify(newton - sp.sympify(ref_c1["newtonian"], locals=loc_ns)) == 0)
check("K1 CONTROL (FP3 C1): this lane's static-symbol engine, given FP3's density-read gate (B W'' (C lap phi)^2/2 on the C-H "
      "bracket), reproduces FP3's committed determinant, its zero, the Newtonian response and the gate's local (anti-pressure) term",
      f"det = {detM}; zero k^2 = {roots}; local term {local}; all equal to FP3's committed strings: {k1_ok}", k1_ok)
OUT["numbers"]["K1"] = {"det": str(detM), "zero": str(roots), "local": str(local)}

# K2: DE12 on its own 24 layers
S_fun = lambda Bv, W1, W2, tU, Umx, A: Bv * (W2 * tU ** 2 * (Umx * A) ** 2)
k2rows, k2dev = {}, 0.0
TRS = {}
for (z, Mb, f) in GAL:
    tr = transition(z, Mb, f, 0.25)
    TRS[KEY(z, Mb, f)] = tr
    m = (tr["t"] > 0) & (tr["t"] < 1)
    _, W1, W2 = Wd(tr["t"])
    Umx = 4 * math.pi * G12 / (tr["H"] ** 2 * tr["xce"])
    Sper = S_fun(tr["B"], W1, W2, 1 / (2 * 0.25), Umx, nu_of(tr["y"]))
    Spar = S_fun(tr["B"], W1, W2, 1 / (2 * 0.25), Umx, nu_of(tr["y"]) + ynup_of(tr["y"]))
    cg = np.sqrt(np.maximum(tr["rho_b"] * np.maximum(Sper, 0), tr["rho_b"] * np.maximum(Spar, 0)))
    cmax = float(np.max(cg[m]))
    gam = (1 / KPC) * math.sqrt(max(cmax ** 2 - CS["1e6K"] ** 2, 0.0)) / tr["H"]
    ref = R12["budget"][KEY(z, Mb, f)]
    k2dev = max(k2dev, abs(cmax / ref["c_gate_max"] - 1), abs(gam / ref["Gamma_over_H"] - 1))
    k2rows[KEY(z, Mb, f)] = dict(c_gate=cmax, Gamma_over_H=gam, r_edge_kpc=ref["r_edge_kpc"])
check("K2 CONTROL (DE12): DE12's transition() (definitions loaded unedited, XR18's recipe) reproduces DE12's committed "
      "c_gate_max and Gamma(1/kpc)/H of its density-read gate on all 24 layers",
      f"max relative deviation {k2dev:.1e}; c_gate_max {min(v['c_gate'] for v in k2rows.values()) / 1e3:.0f}-"
      f"{max(v['c_gate'] for v in k2rows.values()) / 1e3:.0f} km/s, Gamma/H {min(v['Gamma_over_H'] for v in k2rows.values()):.1e}-"
      f"{max(v['Gamma_over_H'] for v in k2rows.values()):.1e}", k2dev <= 1e-12)
OUT["numbers"]["K2"] = k2rows

# K3: the sign of the MOND sector's Lagrangian at fixed fields (MOND on vs off)
yy = np.logspace(-8, 4, 2001)
qP2 = q_of(yy)                                                                     # DE12's (L352's) q(y) = int (nu - 1) dZ
sign_q = bool(np.all(qP2 >= -1e-15)) and bool(np.all(np.diff(qP2) >= -1e-15))
s_vals = np.linspace(0, 50, 101); Yv = 0.3
sign_s = bool(np.all(np.diff(-s_vals * Yv) <= 0))                                   # AQUAL stiffness: L = -(J + s Y) falls with s
ys_vals = np.linspace(0, 1e-2, 101); sqY = 0.02
sign_y = bool(np.all(np.diff(-2 * ys_vals * sqY) <= 0))                             # the yield: L = -(J + 2 y sqrt Y) falls with y
a2 = F19.get("A2", {})
I_min = None
for kk_, vv_ in a2.items():
    if isinstance(vv_, dict):
        for k3_, v3_ in vv_.items():
            if "I" in str(k3_) and isinstance(v3_, (int, float)):
                I_min = v3_ if I_min is None else min(I_min, v3_)
sign_B = bool(I_min is not None and I_min > 0)
P(f"    QUMOND (FP1/FP3): q(y) >= 0 and non-decreasing on y = 1e-8..1e4: {sign_q} (q(1e-4) = {float(q_of(np.array([1e-4]))[0]):.3e}, "
  f"q(1) = {float(q_of(np.array([1.0]))[0]):.3f}); AQUAL stiffness (FP7): -s Y falls with s: {sign_s}; the yield (FP9/FP19): "
  f"-2 y sqrt(Y) falls with y: {sign_y}; the band-pass (FP19 A2, committed): min I(B) = {I_min} > 0: {sign_B}")
check("K3 THE SIGN (all four formulations): at fixed fields the MOND sector's contribution to the Lagrangian is LARGEST when "
      "MOND is on -- QUMOND's +q W with q >= 0 (MOND on = W = 1); the AQUAL stiffness -s Y and the yield -2 y sqrt(Y) fall as "
      "the switch closes; FP19 A2's committed dS/dB = V 4 pi G rho^2 I(B) with I > 0 (opening the band-pass adds binding)",
      f"q >= 0: {sign_q}; stiffness: {sign_s}; yield: {sign_y}; band-pass I_min = {I_min}", sign_q and sign_s and sign_y and sign_B,
      reading="sigma = +1: 'MOND off' always lowers L at fixed fields -- the fact the mirror lemma (A3) turns on")
OUT["numbers"]["K3"] = dict(q_min=float(qP2.min()), I_min=I_min)
P(f"    {el()}")

# ================================================================================================ A1 the static sector
banner("A1  THE STATIC SECTOR (sympy): the theta gate's second variation has no potential part" + ("  [MUTATE: density-read gate]" if MUTATE else ""))
t_, q1, q2, q3, ep, sig, Bs, rho0, cs2 = sp.symbols("t q1 q2 q3 epsilon sigma B rho_0 c_s2", real=True)
W0s, W1s, W2s = sp.symbols("W0 W1 W2", real=True)                                  # W, W', W'' at the background argument
th0 = sp.Symbol("theta0", real=True)


def Wtaylor(arg, a0_=0):
    return W0s + W1s * (arg - a0_) + W2s * (arg - a0_) ** 2 / 2


# The expansion is done on plain symbols (the displacement gradient A_ij = d xi_i/d q_j and its rate B_ij = dA_ij/dt), because
# sympy's series cannot collect mixed derivatives; J = det(I + eps A), J-dot = sum_ij (dJ/dA_ij) B_ij (the chain rule).
# 1-D: x = q + eps xi(q, t);  J = 1 + eps xi_q;  theta = J_t/J
a11, b11 = sp.symbols("a11 b11", real=True)                                          # xi_q and xi_qt
J1 = 1 + ep * a11
theta1 = ep * b11 / J1
if MUTATE:
    gate1 = sig * Bs * J1 * Wtaylor(rho0 / J1, rho0)                                  # the density reading (FP3's class)
else:
    gate1 = sig * Bs * J1 * Wtaylor(theta1, 0)
g2_1d = sp.simplify(sp.series(gate1, ep, 0, 3).removeO().coeff(ep, 2))
kin_expected = sig * Bs * W2s * b11 ** 2 / 2
res_1d = sp.simplify(g2_1d - kin_expected)
# 3-D: J = det(I + eps A); second-order gate term vs (1/2) sigma B W'' (tr B)^2 + W0 x J_2 + W1 x dJ_2/dt
Aij = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"a{i + 1}{j + 1}", real=True))
Bij = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"b{i + 1}{j + 1}", real=True))
J3sym = sp.expand((sp.eye(3) + ep * Aij).det())
J3dot = sp.expand(sum(sp.diff(J3sym, Aij[i, j]) * Bij[i, j] for i in range(3) for j in range(3)))
if MUTATE:
    gate3 = sig * Bs * J3sym * Wtaylor(rho0 / J3sym, rho0)
else:
    gate3 = sig * Bs * J3sym * Wtaylor(J3dot / J3sym, 0)
g2_3d = sp.expand(sp.series(gate3, ep, 0, 3).removeO().coeff(ep, 2))
J2sym = J3sym.coeff(ep, 2)
J2dot = sp.expand(sum(sp.diff(J2sym, Aij[i, j]) * Bij[i, j] for i in range(3) for j in range(3)))
trB = Bij[0, 0] + Bij[1, 1] + Bij[2, 2]
res_3d = sp.simplify(sp.expand(g2_3d - sig * Bs * W2s * trB ** 2 / 2 - sig * Bs * (W0s * J2sym + W1s * J2dot)))
# the same J_2 as a functional of the displacement field (for the null-Lagrangian test)
XIs = [sp.Function(f"xi{i}")(q1, q2, q3, t_) for i in (1, 2, 3)]
Qs = (q1, q2, q3)
J3_2 = J2sym.subs({Aij[i, j]: sp.diff(XIs[i], Qs[j]) for i in range(3) for j in range(3)})
J3_1 = sum(sp.diff(XIs[i], Qs[i]) for i in range(3))
divxi_t = sum(sp.diff(XIs[i], Qs[i], t_) for i in range(3))
# J3_2 is a null Lagrangian (a divergence): its Euler-Lagrange derivative vanishes identically
def _el(Lag, fi):
    """Euler-Lagrange expression of a first-order Lagrangian density for field fi (coordinates q1, q2, q3, t)."""
    out = sp.diff(Lag, fi)
    for co in Qs + (t_,):
        d1 = sp.diff(fi, co)
        out -= sp.diff(sp.diff(Lag, d1), co)
    return sp.simplify(sp.expand(out))


el_null = [_el(J3_2, XIs[i]) for i in range(3)]
null_ok = all(e_ == 0 for e_ in el_null)
static_1d = sp.simplify(g2_1d.subs(b11, 0))                                         # the part surviving a static perturbation (xi_qt = 0)
# Hubble-flow background: x = a(t) (q + eps xi): theta = 3 a'/a + eps div xi_t + O(eps^2)
a_t = sp.Function("a")(t_)
Jfun = 1 + ep * J3_1 + ep ** 2 * J3_2                                                # J(xi) to second order, as a functional
theta_h0 = sp.diff(3 * sp.log(a_t), t_)                                             # d ln(a^3)/dt: the background
dlnJ = sp.diff(Jfun, t_) / Jfun                                                     # d ln J/dt, the perturbation
theta_h1 = sp.simplify(sp.diff(dlnJ, ep).subs(ep, 0))                              # its first order in eps
h_ok = (sp.simplify(theta_h0 - 3 * sp.diff(a_t, t_) / a_t) == 0 and sp.simplify(theta_h1 - divxi_t) == 0)
P(f"    1-D: second-order gate term = {g2_1d}")
P(f"    1-D (a11 = xi_q, b11 = xi_qt): minus (1/2) sigma B W'' xi_qt^2 = {res_1d};  its static part (xi_qt = 0): {static_1d}")
P(f"    3-D (A = grad xi, B = its rate): second-order gate term minus (1/2) sigma B W'' (tr B)^2 minus sigma B [W0 J_2 + W1 dJ_2/dt] = {res_3d};  "
  f"J_2 is a null Lagrangian (EL derivatives {el_null}): {null_ok}")
P(f"    Hubble-flow background (x = a(t)(q + eps xi)): theta = 3 a'/a + eps div xi_t + O(eps^2): {h_ok}")
a1_ok = (res_1d == 0) and (res_3d == 0) and null_ok and h_ok
check("A1 [H1, HEADLINE; MUTATE must fail] THE STATIC SECTOR IS UNTOUCHED: expanded to second order in the displacement about a "
      "static background (1-D and 3-D, sympy) the gate term sigma B J W(J-dot/J) contributes exactly (1/2) sigma B W'' (div xi-dot)^2 "
      "plus W0 x a null Lagrangian plus W' x its time derivative -- no potential (static) term; on a Hubble-flow background "
      "delta theta = div xi-dot (Lagrangian frame).  FP3 C1's static symbol gains no gate term and DE12's c_gate^2 = rho_b S is 0",
      f"1-D residual {res_1d}; 3-D residual {sp.simplify(res_3d) if res_3d != 0 else 0}; null Lagrangian {null_ok}; Hubble-flow "
      f"delta theta {h_ok}", a1_ok,
      reading=("MUTATE: read on the density the gate's second variation is a POTENTIAL term (1/2) sigma B W'' rho_0^2 (div xi)^2 "
               "-- FP3's anti-pressure returns" if MUTATE else
               "the theta gate escapes FP3's density lemma where FP3 stated it -- in the static symbol -- because theta vanishes on "
               "static perturbations"))
OUT["numbers"]["A1"] = dict(g2_1d=str(g2_1d), res_1d=str(res_1d), res_3d=str(res_3d), null_ok=null_ok, hubble_ok=h_ok, static_1d=str(static_1d))

# ================================================================================================ A2 the kinetic sector
banner("A2  THE KINETIC SECTOR (sympy): the compressive velocity symbol and the pole")
kk, om, csq, fourpiGrho, Lthth = sp.symbols("k omega c_s2 fourpiGrho L_thth", real=True)
rhob = sp.Symbol("rho_b", positive=True)
Xamp = sp.Symbol("X", real=True)
# plane wave xi = X e^{i(kq - omega t)} longitudinal: kinetic (1/2)(rho_b + L_thth k^2)|omega X|^2, potential (1/2) rho_b (c_s^2 k^2 - 4 pi G rho) |X|^2
m_k = rhob + Lthth * kk ** 2
K_k = rhob * (csq * kk ** 2 - fourpiGrho)
omega2 = sp.simplify(K_k / m_k)
pole = sp.solve(sp.Eq(m_k, 0), kk)
pole_pos = [p_ for p_ in pole if p_.is_positive is not False]
P(f"    m(k) = {m_k};  K(k) = {K_k};  omega^2 = {omega2};  m(k) = 0 at k = {pole}")
a2_ok = (sp.simplify(omega2 - (rhob * (csq * kk ** 2 - fourpiGrho)) / (rhob + Lthth * kk ** 2)) == 0
         and any(sp.simplify(p_ ** 2 - (-rhob / Lthth)) == 0 for p_ in pole))
check("A2 [H2] THE KINETIC SECTOR: the longitudinal (compressive) mode has kinetic coefficient m(k) = rho_b + L_thth k^2 with "
      "L_thth = sigma B W''_theta, potential K(k) = rho_b (c_s^2 k^2 - 4 pi G rho) (the gate adds nothing to K: A1); omega^2 = K/m "
      "has a POLE at k_g^2 = -rho_b/L_thth wherever L_thth < 0 -- the stability rule is the MIRROR of FP3 C1 (density gates: W "
      "concave in rho; theta gates: L convex in theta)",
      f"omega^2 = {omega2}; pole at k^2 = -rho_b/L_thth: {a2_ok}", a2_ok)
OUT["numbers"]["A2"] = dict(omega2=str(omega2), pole=str(pole))

# ================================================================================================ A3 the mirror lemma
banner("A3  THE MIRROR LEMMA: a gate saturated on the turned-around side makes L concave at the switch-on (sigma = +1)")
xg = np.linspace(-0.5, 3.5, 400001)
lem = {}
for dx_ in (0.01, 0.1, 0.3, 1.0, 3.0):
    tt = xg / dx_
    Wv, W1v, W2v = Wd(tt)
    Wgate = 1.0 - Wv                                                               # on (1) for x <= 0, off (0) for x >= dx
    Wpp_x = -W2v / dx_ ** 2
    jmin = int(np.argmin(Wpp_x))
    lem[dx_] = dict(min_Wpp=float(Wpp_x.min()), x_at_min=float(xg[jmin]), W_at_min=float(Wgate[jmin]), max_Wpp=float(Wpp_x.max()))
    P(f"    DE12's C-infinity step as a theta gate, width Delta_x = {dx_:5.2f}: min W''_x = {Wpp_x.min():+.3e} at x = {xg[jmin]:.4f} "
      f"(W = {Wgate[jmin]:.3f}: the saturated, switch-on side); max W''_x = {Wpp_x.max():+.3e}")
# the linear ramp: W = clip(1 - x, 0, 1): a concave kink at x = 0 (W' jumps from 0 to -1)
ramp = np.clip(1 - xg, 0, 1); dW = np.gradient(ramp, xg)
kink0 = float(dW[np.searchsorted(xg, 0.01)] - dW[np.searchsorted(xg, -0.01)])
kink1 = float(dW[np.searchsorted(xg, 1.01)] - dW[np.searchsorted(xg, 0.99)])
# the four formulations, each with a smooth switch s(x) from 'on' to 'off' saturating at x <= 0: L(x) = sigma_form * E(x)
forms = {}
S_on = 1.0 - Wd(xg / 1.0)[0]                                                        # 1 on the turned-around side, 0 off
Lq = +1.0 * S_on                                                                    # QUMOND: +q W (q = 1 unit)
Ls = -(1.0 - S_on) * 5.0                                                            # AQUAL stiffness: -s Y, s = 5 (1 - W)
Ly = -2 * (1.0 - S_on) * 0.01                                                       # yield: -2 y sqrt(Y), y = 0.01 (1 - W)
LB = +np.interp(S_on, [0, 1], [0.0, 1.0]) ** 1.0                                    # band-pass: S rises with B (dS/dB > 0), B = B_on W
for nm, Lf in (("QUMOND +q W", Lq), ("AQUAL stiffness -s Y", Ls), ("yield -2 y sqrt Y", Ly), ("band-pass S(B), dS/dB > 0", LB)):
    d2 = np.gradient(np.gradient(Lf, xg), xg)
    forms[nm] = dict(min_Lxx=float(d2.min()), x_at_min=float(xg[int(np.argmin(d2))]), L_on=float(Lf[0]), L_off=float(Lf[-1]))
    P(f"    {nm:28s}: L(on) = {Lf[0]:+.3f} > L(off) = {Lf[-1]:+.3f}; min L'' = {d2.min():+.3e} at x = {xg[int(np.argmin(d2))]:.3f}")
lem_ok = (all(v["min_Wpp"] < 0 and 0 < v["x_at_min"] < k_ for k_, v in lem.items())
          and lem[0.01]["min_Wpp"] < -1e4 and kink0 < -0.9 and kink1 > 0.9
          and all(v["min_Lxx"] < 0 and v["L_on"] > v["L_off"] and 0 < v["x_at_min"] < 1.0 for v in forms.values()))
check("A3 [H3] THE MIRROR LEMMA: with sigma = +1 (K3) a gate flat on the turned-around side (theta <= 0) and lower on the "
      "expanding side makes L_g(theta) flat-then-decreasing, hence NOT convex: L_g'' < 0 just above theta = 0 -- on DE12's C-inf "
      "step at every width (-> -oo in the sharp limit), on the linear ramp (a concave kink at theta = 0: W' jumps by -1; its "
      "convex kink sits at the Hubble flow) and in all four formulations (QUMOND, AQUAL stiffness, yield, band-pass)",
      "; ".join(f"Delta_x {k_}: min W'' {v['min_Wpp']:+.2e} at x = {v['x_at_min']:.3f}" for k_, v in lem.items())
      + f"; ramp kinks {kink0:+.2f} (x = 0), {kink1:+.2f} (x = 1); forms min L'' " + ", ".join(f"{k_.split()[0]} {v['min_Lxx']:+.2e}" for k_, v in forms.items()),
      lem_ok, reading="FP3's lemma (a gate zero on FRW is convex somewhere) forbids density gates at the web end; its mirror forbids "
      "saturated theta gates at the switch-on end: the theta gate trades FP3's anti-pressure for a kinetic ghost at theta ~ 0")
OUT["numbers"]["A3"] = dict(steps={str(k_): v for k_, v in lem.items()}, ramp_kinks=[kink0, kink1], forms=forms)
P(f"    {el()}")

# ================================================================================================ A4 DE12's 24 layers
banner("A4  THE NUMBERS ON DE12's 24 HOST LAYERS: the theta gate at its natural width (Delta_x = 1), 1e6 K gas, both footings")
WPP_MAX = float(np.max(Wd(np.linspace(1e-5, 1 - 1e-5, 200001))[2]))                # 9.84 for DE12's C-inf step
a4 = {}
for (z, Mb, f) in GAL:
    tr = TRS[KEY(z, Mb, f)]
    Kh = 3.0 * tr["H"]                                                             # <K>_h = 3H on FRW
    m = (tr["t"] > 0) & (tr["t"] < 1)                                               # DE12's own layer (its gate's transition band)
    Lth = tr["B"] * WPP_MAX / Kh ** 2                                               # |L_thth| at the concave maximum, Delta_x = 1
    kg = np.sqrt(tr["rho_b"] / Lth)                                                 # the pole [1/m]
    k1 = 1.0 / KPC
    mk1 = tr["rho_b"] - Lth * k1 ** 2
    gam1 = np.where(mk1 < 0, CS["1e6K"] * k1 * np.sqrt(tr["rho_b"] / np.maximum(-mk1, 1e-300)), 0.0) / tr["H"]
    lay = dict(inv_kg_kpc_layer=float(np.max(1 / kg[m]) / KPC), inv_kg_kpc_layer_min=float(np.min(1 / kg[m]) / KPC),
               ghost_at_1kpc_layer=bool(np.all(mk1[m] < 0)), Gamma_1kpc_over_H_layer=float(np.max(gam1[m])),
               inv_kg_kpc_profile_max=float(np.max(1 / kg) / KPC), r_layer_kpc=[float(tr["r"][m].min() / KPC), float(tr["r"][m].max() / KPC)],
               vB_kms_layer=float(np.median(np.sqrt(tr["B"][m] / tr["rho_b"][m])) / 1e3), c_gate_static=0.0,
               DE12_Gamma_over_H=R12["budget"][KEY(z, Mb, f)]["Gamma_over_H"])
    a4[KEY(z, Mb, f)] = lay
for kk_, v in a4.items():
    P(f"    {kk_:22s}: layer r = {v['r_layer_kpc'][0]:7.0f}-{v['r_layer_kpc'][1]:7.0f} kpc, v_B = sqrt(B/rho_b) = {v['vB_kms_layer']:6.1f} km/s; "
      f"1/k_g = {v['inv_kg_kpc_layer_min']:6.1f}-{v['inv_kg_kpc_layer']:6.1f} kpc (whole profile up to {v['inv_kg_kpc_profile_max']:7.0f}); "
      f"ghost at 1/kpc: {v['ghost_at_1kpc_layer']}; "
      f"Gamma(1/kpc) = {v['Gamma_1kpc_over_H_layer']:6.1f} H (DE12's density gate {v['DE12_Gamma_over_H']:.1e} H); static c_gate = 0")
a4_ok = (all(v["ghost_at_1kpc_layer"] for v in a4.values()) and all(v["inv_kg_kpc_layer"] <= 1000.0 for v in a4.values()))
check("A4 [H4] DE12's OWN 24 LAYERS (same gas, same MOND energy B = a0^2 q(y)/(8 pi G), both footings): with the gate at its "
      "natural width Delta_x = 1 the compressive velocity symbol is NEGATIVE at k = 1/kpc on every layer (a ghost at DE12's own "
      "scale), the pole sits at 1/k_g <= 1 Mpc on every layer, and the static c_gate is 0 (A1)",
      f"ghost at 1/kpc on {sum(v['ghost_at_1kpc_layer'] for v in a4.values())}/24 layers; 1/k_g on the layers "
      f"{min(v['inv_kg_kpc_layer_min'] for v in a4.values()):.1f}-{max(v['inv_kg_kpc_layer'] for v in a4.values()):.1f} kpc; Gamma(1/kpc) "
      f"{min(v['Gamma_1kpc_over_H_layer'] for v in a4.values()):.1f}-{max(v['Gamma_1kpc_over_H_layer'] for v in a4.values()):.1f} H "
      f"(DE12's density gate 1.3e3-4.9e4 H)", a4_ok,
      reading="not DE12's fast Jeans-type instability but a ghost: negative kinetic energy of compressive gas motions below ~0.01-1 "
              "Mpc at the switch-on, with a pole in the growth rate (A5)")
OUT["numbers"]["A4"] = a4

# A5 the pole's band (reported)
kr = np.array([1.001, 1.01, 1.1, 2.0, 10.0])
band = {}
for kk_ in ("0.25/1e+11/canonical", "0.25/1e+11/alt", "2.5/1e+11/canonical"):
    tr = TRS[kk_]; mm = (tr["t"] > 0) & (tr["t"] < 1); j = int(np.argmax(mm)); Kh = 3 * tr["H"]
    Lth = tr["B"][j] * WPP_MAX / Kh ** 2; kg = math.sqrt(tr["rho_b"][j] / Lth)
    kv = kr * kg
    band[kk_] = [float(CS["1e6K"] * k_ * math.sqrt(tr["rho_b"][j] / (Lth * k_ ** 2 - tr["rho_b"][j])) / tr["H"]) for k_ in kv]
    P(f"    {kk_}: 1/k_g = {1 / kg / KPC:.1f} kpc; Gamma/H at k/k_g = " + ", ".join(f"{a_:g}: {b_:.2e}" for a_, b_ in zip(kr, band[kk_])))
check("A5 (reported) THE POLE: next to k_g the growth rate of the pressure-supported gas exceeds any bound (Gamma -> oo as "
      "k -> k_g+), so the linearised evolution is not bounded in any norm -- the XR18 standard (a symbol that changes sign) "
      "calls this ill posed; the sharp theta = 0 gate is the limit Delta_x -> 0, where k_g -> 0 (the whole layer is ghost-like)",
      "; ".join(f"{k_}: Gamma(1.001 k_g) = {v[0]:.1e} H" for k_, v in band.items()), True, load_bearing=False)
OUT["numbers"]["A5"] = band
P(f"    {el()}")

# ================================================================================================ A6 the well-posed variants
banner("A6  THE SMOOTHEST WELL-POSED VERSIONS AND WHAT THEY COST")
# (a) convex, unsaturated: W = max(0, 1 - x/Dx) -> healthy; SPARC: the galaxy law changes by log10(1 + (W - 1)(nu - 1)/nu)
tol = 0.01
xa = {}
for yv in (0.01, 0.1, 1.0):
    nuv = float(nu_of(np.array([yv]))[0])
    xa[yv] = (10 ** tol - 1) * nuv / (nuv - 1)                                     # |x|/Dx allowed
f_acc_need = {yv: 3.0 * xa[yv] for yv in xa}                                       # |theta_R| = f_acc H -> x = f_acc/3
P("    (a) convex, unsaturated W = max(0, 1 - x/Delta_x): L convex, kinetic symbol >= rho_b (healthy); SPARC's 0.01 dex allows "
  "|x|/Delta_x <= " + ", ".join(f"{v:.3f} (y = {k_:g})" for k_, v in xa.items())
  + "; a host accreting a fraction f_acc of its mass per Hubble time has |x| ~ f_acc/3: allowed only for f_acc <= "
  + ", ".join(f"{v:.3f} Delta_x" for v in f_acc_need.values()))
# (b) filtered argument: R_min = sqrt(B |W''_theta| / (e rho_b)) at the switch-on layer
rmin = {}
for kk_, tr in TRS.items():
    mm = (tr["t"] > 0) & (tr["t"] < 1); Kh = 3 * tr["H"]
    R = np.sqrt(tr["B"][mm] * WPP_MAX / (math.e * tr["rho_b"][mm])) / Kh
    rmin[kk_] = float(np.max(R) / MPCm)
trc = {f: transition(0.25, 1e14, f, 0.25) for f in FOOTS}                           # a 1e14 cluster (DE12's host rule), uncapped
for f, tr in trc.items():
    Kh = 3 * tr["H"]; r = tr["r"]
    sel = (r > 2 * MPCm) & (r < 12 * MPCm)                                         # its turnaround zone
    R = np.sqrt(tr["B"][sel] * WPP_MAX / (math.e * tr["rho_b"][sel])) / Kh
    rmin[f"0.25/1e+14/{f} (cluster, 2-12 Mpc)"] = float(np.max(R) / MPCm)
for kk_, v in rmin.items():
    if kk_.startswith("0.25/") or "cluster" in kk_:
        P(f"    (b) filtered theta_R: R_min at {kk_:36s} = {v:.3f} Mpc")
gal_rmin = [v for k_, v in rmin.items() if "cluster" not in k_ and k_.split("/")[1] in ("1e+10", "1e+11")]
clu_rmin = [v for k_, v in rmin.items() if "cluster" in k_]
a6_ok = (min(f_acc_need.values()) < 0.2 and max(clu_rmin) > 0.5 and min(gal_rmin) < 1.0)
check("A6 [H5] THE WELL-POSED VERSIONS COST THE GATE ITS PURPOSE: (a) the convex (unsaturated) gate is healthy but multiplies "
      "MOND by 1 + |x|/Delta_x in contracting hosts, so SPARC's 0.01 dex needs accretion below ~0.07 Delta_x per Hubble time "
      "in every SPARC host; (b) filtering the argument on a heat-kernel length R is healthy iff R >= R_min, which spans galaxy "
      "layers to clusters -- no single R keeps every layer healthy and stays below an isolated galaxy's turnaround radius",
      f"(a) f_acc allowed <= {min(f_acc_need.values()):.3f}-{max(f_acc_need.values()):.3f} x Delta_x; (b) R_min galaxies (1e10-1e11, all z) "
      f"{min(gal_rmin):.3f}-{max(gal_rmin):.3f} Mpc, 1e12 {min(v for k_, v in rmin.items() if '1e+12' in k_):.3f}-"
      f"{max(v for k_, v in rmin.items() if '1e+12' in k_):.3f} Mpc, 1e14 cluster {min(clu_rmin):.2f}-{max(clu_rmin):.2f} Mpc", a6_ok,
      reading="a well-posed theta gate needs a new length R (or a new width Delta_x); the one that heals clusters erases the "
              "turned-around regions of isolated galaxies (part 2: 0.2-0.5 Mpc at z = 0.25)")
OUT["numbers"]["A6"] = dict(convex_x_allowed={str(k_): v for k_, v in xa.items()}, f_acc_allowed={str(k_): v for k_, v in f_acc_need.items()},
                            R_min_Mpc=rmin)

# ================================================================================================ A7 MS1: baryons vs total matter
banner("A7  (reported) MS1: the baryon flow vs the total matter flow -- the carrier's daughters stream out")
H025 = Hz12(0.25); Kh025 = 3 * H025
ms1 = {}
for vk in (575.0, 600.0, 650.0):
    for rr in (0.1, 0.3, 1.0, 3.0):
        ms1[f"{vk:.0f}/{rr}"] = (2 * vk * 1e3 / (rr * MPCm)) / Kh025
P("    the daughters' divergence 2 v_k/r in units of <K>_h(z = 0.25): " + ", ".join(f"v_k {k_.split('/')[0]} km/s, r = {k_.split('/')[1]} Mpc: "
                                                                              f"{v:.1f}" for k_, v in ms1.items() if k_.startswith("600")))
check("A7 [H6] (reported) MS1: at the baryons' switch-on surface theta_b = 0, so a total-matter reading adds f_d x 2 v_k/r > 0 "
      "from any outstreaming daughter fraction f_d and pushes the switch-on inward; 2 v_k/r exceeds <K>_h by the printed factors -- "
      "the total-matter gate turns MOND off around galaxies after their carrier converts (a leak into the wrong region); the gate "
      "reads the BARYON flow (part 2 prices the shift of the switch-on radius)",
      f"2 v_k/r / <K>_h at 0.3 / 1 / 3 Mpc (600 km/s): {ms1['600/0.3']:.1f} / {ms1['600/1.0']:.1f} / {ms1['600/3.0']:.1f}",
      ms1["600/1.0"] > 1.0, load_bearing=False)
OUT["numbers"]["A7"] = ms1

# ================================================================================================ A8 first-order effects
banner("A8  (reported) THE GATE'S FIRST-ORDER EFFECTS: its own force on the baryons and the Raychaudhuri feedback")
a8 = {}
for kk_ in ("0.25/1e+10/canonical", "0.25/1e+11/canonical", "0.25/1e+12/canonical", "2.5/1e+11/canonical"):
    tr = TRS[kk_]; mm = (tr["t"] > 0) & (tr["t"] < 1); Kh = 3 * tr["H"]
    j = int(np.where(mm)[0][len(np.where(mm)[0]) // 2]); r = tr["r"][j]
    Wp = 2.0 / Kh                                                                   # |W'_theta| max for DE12's step at Delta_x = 1 (max W1 = 2)
    f_gate = tr["B"][j] * Wp * tr["H"] / r                                          # ~ d/dt grad(B W') ~ H B |W'| / r  [N/m^3]
    g_grav = float(tr["g"][j])
    rho_ph = float(np.gradient(tr["g"] * tr["r"] ** 2, tr["r"])[j] / (4 * math.pi * G12 * r ** 2) - tr["rho_b"][j] / 0.157 * 0.157)
    gam_fb = 4 * math.pi * G12 * abs(rho_ph) * Wp / tr["H"]
    a8[kk_] = dict(force_over_gravity=float(f_gate / (tr["rho_b"][j] * g_grav)), feedback_over_H=float(gam_fb), r_kpc=float(r / KPC))
    P(f"    {kk_}: at r = {r / KPC:.0f} kpc the gate's own force / gravity on the baryons ~ {a8[kk_]['force_over_gravity']:.2e}; "
      f"Raychaudhuri feedback rate 4 pi G rho_ph |W'| ~ {gam_fb:.2e} H")
check("A8 (reported) the gate's FIRST-order effects: its own force (d/dt of grad(B W')) and the feedback of the switch on the "
      "flow's expansion (more expansion -> less MOND -> more expansion) at the switch-on layer -- the printed ratios; a Hubble-time "
      "switch, not an ill-posedness",
      "; ".join(f"{k_}: force/gravity {v['force_over_gravity']:.1e}, feedback {v['feedback_over_H']:.1e} H" for k_, v in a8.items()), True,
      load_bearing=False)
OUT["numbers"]["A8"] = a8

# ================================================================================================ W the ledger
banner("W  THE LEDGER")
LEDGER = [
    ("XR36-a", "DERIVED", "the turnaround gate as an action term: sigma B W(theta_m/<K>_h) on a Lagrangian-coordinate (Brown/Schutz) "
     "fluid; theta_m = d ln J/dt, a velocity-dependent term with no Ostrogradsky mode", "A1"),
    ("XR36-b", "DERIVED", "the theta gate adds NO static term: FP3 C1's density lemma and DE12's baryon-stiffness instability are "
     "escaped exactly (c_gate = 0)", "A1, K1, K2"),
    ("XR36-c", "DERIVED", "the mirror lemma: well-posedness needs L convex in theta; MOND-on raises L at fixed fields in every "
     "formulation (K3), so a gate saturated on the turned-around side is concave at the switch-on", "A2, A3, K3"),
    ("XR36-d", "FAILS", "the sharp theta = 0 gate and every saturated smooth gate: the compressive velocity symbol changes sign "
     "(a ghost with a pole), on all 24 of DE12's layers at k = 1/kpc", "A4, A5"),
    ("XR36-e", "CONSTRAINT", "a well-posed theta gate is either unsaturated (MOND x (1 + |x|/Delta_x) in contracting hosts: SPARC) "
     "or filtered on R >= R_min (galaxies to clusters: no single R); either adds a constant", "A6"),
    ("XR36-f", "CONSTRAINT", "MS1: the gate must read the baryon flow; the total-matter reading is switched off by the carrier's "
     "outstreaming daughters", "A7"),
]
for row in LEDGER:
    OUT["ledger"].append(dict(zip(("link", "status", "what", "basis"), row)))
    P(f"    {row[0]:8s} {row[1]:10s} {row[2]}  [{row[3]}]")

n_pass = sum(1 for c in CH if c[1]); n_lb_fail = sum(1 for c in CH if (not c[1]) and c[2])
P(f"\n{n_pass}/{len(CH)} checks pass; load-bearing failures: {n_lb_fail}   {el()}")
OUT["verdict"] = dict(passed=n_pass, total=len(CH), load_bearing_failures=n_lb_fail)
with open(JSN, "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
sys.stdout.flush()
sys.exit(1 if n_lb_fail else 0)
