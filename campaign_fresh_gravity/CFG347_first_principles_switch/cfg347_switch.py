#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG347 -- a first-principles bound-only switch from the framework's own structure?  (criteria: FROZEN_CRITERIA.md)

Routes: R1 slaved theta_b gate B W(theta_b/theta_*); R2 the leaf comparison theta_* = <K>_h = 3H; R3 a dynamical switch
sigma with its own kinetic term, sourced by theta_b through C sigma nabla.u_b (a gyroscopic, velocity-linear coupling).
Tests (a) FRW-off, (b) bound ON + fidelity/reach/timing, (c) transition health; controls C1 (XR36), C2 (GR), MUTATE.
DE12's transition() and L341's growth harness are exec'd read-only (no file of theirs is written).
"""
import os, sys, json, math, io, contextlib, time
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("CFG347_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
T0 = time.time()
P = lambda *a: print(*a, flush=True)
OUT = {"lane": "CFG347", "mutate": MUTATE, "checks": {}, "numbers": {}}
CH = []


def check(name, measured, ok, reading=""):
    ok = bool(ok)
    CH.append((name, ok))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}" + (f"\n         reading:  {reading}" if reading else ""))
    return ok


def banner(t):
    P("\n" + "=" * 110 + "\n" + t + "\n" + "=" * 110)


P(__doc__.strip())
if MUTATE:
    P("\n  *** CFG347_MUTATE=1: threshold sign flipped -- the switch is ON where theta_b >= theta_on (expanding regions) ***")

# ------------------------------------------------------------------ record machinery, read-only
P_DE12 = os.path.join(REPO, "real_research", "dark_energy_2026", "DE12_mond_sector_gate_stiffness.py")
NS = {"__name__": "de12_readonly", "__file__": P_DE12}
_src = open(P_DE12).read().split('banner("G1 G2')[0].replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False")
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src, NS)
G, KPC, MS, FB, CS, Wd, transition, host = [NS[k] for k in ("G", "KPC", "MS", "FB", "CS", "Wd", "transition", "host")]
H0, Om, rho_crit0, A0, Hz = NS["H0"], NS["Om"], NS["rho_crit0"], NS["A0"], NS["Hz"]
CL = 299792458.0
ZS, MBS, FOOTS = (0.25, 1.0, 2.5, 4.0), (1e10, 1e11, 1e12), ("canonical", "alt")
HOSTS = [(z, Mb, f) for z in ZS for Mb in MBS for f in FOOTS]
KEY = lambda z, Mb, f: f"{z}/{Mb:.0e}/{f}"
WPP_MAX = float(np.max(Wd(np.linspace(1e-5, 1 - 1e-5, 200001))[2]))
S_step = lambda x: Wd(np.atleast_1d(np.asarray(x, float)))[0]          # DE12's C-inf step, 0 at x <= 0, 1 at x >= 1
with contextlib.redirect_stdout(io.StringIO()):
    TRS = {KEY(*hk): transition(hk[0], hk[1], hk[2], 0.25) for hk in HOSTS}
P(f"\n  DE12 transition() loaded read-only (24 hosts); W''max of the C-inf step = {WPP_MAX:.3f}; c_s(1e6 K) = {CS['1e6K']/1e3:.0f} km/s")
TH_ON = {f: A0[f] / CL for f in FOOTS}                                 # primary threshold a0/c (framework rate)


def r_ta(z, Mb):
    """turnaround radius: mean enclosed density (DE12's NFW host + mean) = 5.55 rho_m-bar(z) (EdS value; approximation)."""
    hs = host(Mb, z); rb = Om * rho_crit0 * (1 + z) ** 3
    menc = lambda r: 4 * math.pi * hs["rho_s"] * hs["rs"] ** 3 * (math.log(1 + r / hs["rs"]) - (r / hs["rs"]) / (1 + r / hs["rs"]))
    fn = lambda lr: (menc(math.exp(lr)) / (4 / 3 * math.pi * math.exp(lr) ** 3) + rb) - 5.55 * rb
    return math.exp(brentq(fn, math.log(hs["r200"]), math.log(1e3 * hs["r200"])))


RTA = {KEY(*hk): r_ta(hk[0], hk[1]) for hk in HOSTS}
P(f"  r_ta range {min(RTA.values())/KPC:.0f}-{max(RTA.values())/KPC:.0f} kpc")

# ============================================================================== S: symbolic derivations
banner("S  SYMBOLIC: the slaved gate's kinetic symbol and K-dot force (R1/R2), theta_b of steady flows, R3's dispersion")
t, x = sp.symbols("t x", real=True)
rho, Bs, W1, W2, k, w, cs2, cg2, Gam2, Z_, M_, C_ = sp.symbols("rho B W1 W2 k w c_s2 c_sig2 Gamma2 Z M C", real=True)
xi = sp.Function("xi")(x, t); th = sp.Function("thetastar")(t); Bx = sp.Function("Bf")(x)
# second-order Lagrangian of the slaved gate about a static background (theta = d_x xi_t): rho/2 xi_t^2 + B[W1 theta/th + W2/2 (theta/th)^2]
L1 = rho / 2 * sp.diff(xi, t) ** 2 + Bx * (W1 * sp.diff(xi, x, t) / th + W2 / 2 * (sp.diff(xi, x, t) / th) ** 2)
EL = sp.euler_equations(L1, [xi], [x, t])[0].lhs
EL_force = sp.simplify(EL.subs({W2: 0}) + rho * sp.diff(xi, t, 2))   # the W1 part: the static force density on baryons
P(f"  slaved gate, W1 (first-variation) part of the EL equation: {sp.simplify(EL_force)}")
force_static = sp.simplify(EL_force.subs(xi, 0).doit())
P(f"  static background (xi = 0): force density = {force_static}  (zero iff d(1/theta_*)/dt = 0 or W'(0) = 0)")
# kinetic symbol: plane wave, constant B, constant theta_*
xi0, om = sp.symbols("xi0 omega", positive=True)
Lk = rho / 2 * om ** 2 + Bs * W2 / 2 * (k * om) ** 2 / sp.Symbol("ths") ** 2
mk = sp.simplify(2 * sp.diff(Lk, om, 2) / 2)
P(f"  compressive kinetic coefficient m(k) = {mk}  (XR36's H2; a pole/ghost wherever W2 < 0)")
OUT["numbers"]["S_slaved"] = dict(m_k=str(mk), static_force=str(force_static))
# theta_b of steady flows (b1)
R_, ph, zz = sp.symbols("R phi z", positive=True)
vphi = sp.Function("v")(R_, zz)
div_rot = sp.simplify(sp.diff(R_ * 0, R_) / R_ + sp.diff(vphi, ph) / R_ + 0)
P(f"  steady axisymmetric rotation u = v(R,z) e_phi: theta_b = {div_rot}; pressure-supported (u = 0): theta_b = 0")
# R3 dispersion: L = rho/2 (xi_t^2 - A xi^2) + Z/2 (s_t^2 - b s^2) + C k s xi_t
A_, b_ = sp.symbols("A b", real=True)
X_, S_ = sp.symbols("X S")
Mx = sp.Matrix([[rho * (A_ - w), -sp.I * om * C_ * k], [sp.I * om * C_ * k, Z_ * (b_ - w)]])
disp = sp.expand(Mx.det().subs(om ** 2, w))
P(f"  R3 dispersion (w = omega^2): {sp.factor(disp)} = 0, i.e. (A - w)(b - w) = G w with G = C^2 k^2/(rho Z)")
Gs = sp.Symbol("G", positive=True)
poly = sp.expand((A_ - w) * (b_ - w) - Gs * w)
disc = sp.expand(sp.discriminant(poly, w))
P(f"  discriminant = {sp.factor(disc)}  = (A + b + G)^2 - 4 A b > 0 for A, b, G > 0 (real roots); product A b, sum A + b + G")
# principal symbol: w = v k^2, A = c_s^2 k^2 - Gamma^2, b = c_sig^2 k^2 + M^2, G = C^2 k^2/(rho Z)
v_ = sp.Symbol("v")
pr = sp.expand(poly.subs({A_: cs2 * k ** 2 - Gam2, b_: cg2 * k ** 2 + M_ ** 2, Gs: C_ ** 2 * k ** 2 / (rho * Z_), w: v_ * k ** 2}) / k ** 4)
prin = sp.limit(pr, k, sp.oo)
P(f"  principal symbol (k -> oo): {sp.factor(prin)} = 0 -> (c_s^2 - v)(c_sig^2 - v) = (C^2/(rho Z)) v: the gyroscopic term is "
  f"PRINCIPAL (same order); speeds^2 real and positive (product c_s^2 c_sig^2 > 0, discriminant > 0), the larger one >= c_sig^2 + C^2/(rho Z) - c_s^2")
OUT["numbers"]["S_R3"] = dict(dispersion=str(sp.factor(disp)), principal=str(sp.factor(prin)))
s_ok = (sp.simplify(force_static.subs(th, sp.Symbol("c0"))) == 0) and div_rot == 0 and \
       sp.simplify(disc - ((A_ + b_ + Gs) ** 2 - 4 * A_ * b_)) == 0 and sp.simplify(prin - ((cs2 - v_) * (cg2 - v_) - C_ ** 2 * v_ / (rho * Z_))) == 0
check("S1 symbolic: slaved m(k) = rho + B W'' k^2/theta_*^2; static force vanishes for constant theta_* (needs d theta_*/dt "
      "or W'(0) != 0); steady flows have theta_b = 0; R3 dispersion (A-w)(b-w) = G w, principal (c_s^2-v)(c_sig^2-v) = (C^2/rho Z) v",
      f"force(static, const theta_*) = 0; theta_b(rotation) = {div_rot}; disc identity; principal = (c_s2 - v)(c_sig2 - v) - C^2 v/(rho Z)", s_ok)

# ============================================================================== C1, C2 controls
banner("C1  CONTROL: XR36's theta gate (DE12 step, Delta_x = 1, <K>_h = 3H) returns its recorded ghost")
c1 = {}
for hk in HOSTS:
    tr = TRS[KEY(*hk)]; m = (tr["t"] > 0) & (tr["t"] < 1)
    Lth = tr["B"] * WPP_MAX / (3 * tr["H"]) ** 2
    kg = np.sqrt(tr["rho_b"] / Lth)
    mk1 = tr["rho_b"] - Lth / KPC ** 2
    c1[KEY(*hk)] = dict(lo=float(np.min(1 / kg[m]) / KPC), hi=float(np.max(1 / kg[m]) / KPC), ghost1=bool(np.all(mk1[m] < 0)),
                        vB=float(np.median(np.sqrt(tr["B"][m] / tr["rho_b"][m])) / 1e3))
lo = min(v["lo"] for v in c1.values()); hi = max(v["hi"] for v in c1.values())
check("C1 CONTROL: XR36's 1/k_g range 132-1756 kpc within 1%, ghost at 1/kpc on 24/24", f"1/k_g {lo:.1f}-{hi:.1f} kpc; "
      f"ghost {sum(v['ghost1'] for v in c1.values())}/24", abs(lo / 132.0 - 1) < 0.01 and abs(hi / 1756.0 - 1) < 0.01 and
      all(v["ghost1"] for v in c1.values()))
OUT["numbers"]["C1"] = c1
banner("C2  CONTROL: GR limit (B = 0)")
gr = sp.factor(poly.subs(Gs, 0))
check("C2 CONTROL: with B = 0 (so C = 0 and W-terms vanish) the symbols reduce to gas + Jeans: m(k) = rho > 0, "
      "w = A = c_s^2 k^2 - Gamma^2 (growth <= Gamma) and the decoupled sigma (w = b > 0)", f"m = {mk.subs(Bs, 0)}; {gr} = 0",
      mk.subs(Bs, 0) == rho and sp.simplify(gr - (A_ - w) * (b_ - w)) == 0)

# ============================================================================== (a) FRW
banner("(a) FRW + LINEAR PERTURBATIONS")
SRC = os.path.join(REPO, "real_research", "g03_audit_2026", "L341_chk_frw_gate.py")
code = open(SRC).read(); cut = code.index('banner("F1')
L41 = {"__file__": SRC, "__name__": "l341_defs"}
_old = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code[:cut], SRC, "exec"), L41)
if _old is None:
    os.environ.pop("MUTATE")
else:
    os.environ["MUTATE"] = _old
Or, h, Mpc, KH, DREF, A0H, nu_mono, sigma8_of = (L41[k] for k in ("Or", "h", "Mpc", "KH", "DREF", "A0", "nu_mono", "sigma8_of"))
OL = 1 - Om - Or
Ez = lambda a: math.sqrt(Or / a ** 4 + Om / a ** 3 + OL)
dlnH = lambda a: 0.5 * (-4 * Or / a ** 4 - 3 * Om / a ** 3) / Ez(a) ** 2
trapz = getattr(np, "trapezoid", None) or np.trapz


def f_of_theta(theta, th_on):
    """the switch value for a (quasi-static) flow expansion theta: ON (1) at theta <= 0, OFF (0) at theta >= th_on."""
    s = theta / th_on
    return float(S_step(s)[0]) if MUTATE else float(1.0 - S_step(s)[0])


def growth(foot, fFRW, z_i=1000.0):
    a_i = 1 / (1 + z_i)
    sL = solve_ivp(lambda N, Y: [Y[1], 1.5 * (Om / math.exp(3 * N) / Ez(math.exp(N)) ** 2) * Y[0] - (2 + dlnH(math.exp(N))) * Y[1]],
                   (math.log(a_i), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-9, atol=1e-14, dense_output=True)
    Di = DREF / sL.sol(0.0)[0]

    def grms(a, D):
        rhom = Om * rho_crit0 / a ** 3
        gk = 4 * math.pi * G * rhom * np.abs(Di * D) / (KH * h / (a * Mpc))
        return math.sqrt(trapz(gk ** 2 / KH, KH) / trapz(1 / KH, KH))

    def rhs(N, Y):
        a = math.exp(N); D, Dp = Y
        boost = 1.0 + fFRW(a) * (nu_mono(grms(a, D) / A0H[foot]) - 1.0)
        return [Dp, 1.5 * (Om / a ** 3 / Ez(a) ** 2) * boost * D - (2 + dlnH(a)) * Dp]
    s = solve_ivp(rhs, (math.log(a_i), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-9, atol=1e-14, dense_output=True)
    return s.sol(0.0)[0] / sL.sol(0.0)[0], sigma8_of(Di * s.sol(0.0)[0])


aout = {}
for f in FOOTS:
    sFRW_min = 3 * H0 * CL / A0[f]                                   # sigma_FRW = theta_FRW/theta_on = 3H c/a0 >= 3 H0 c/a0
    fbar = lambda a, f=f: f_of_theta(3 * H0 * Ez(a), TH_ON[f])
    nbhd = all(f_of_theta(3 * H0 * Ez(a) * (1 + d), TH_ON[f]) == fbar(a) for a in (1e-3, 0.1, 0.5, 1.0) for d in (-0.9, -0.5, 0.5))
    ratio, s8 = growth(f, fbar)
    aout[f] = dict(sigma_FRW_min=sFRW_min, f_bar_z0=fbar(1.0), nbhd_const=nbhd, growth_ratio_z0=ratio, sigma8=s8)
    P(f"  {f}: sigma_FRW = 3H c/a0 >= {sFRW_min:.2f} (f = 0 for sigma >= 1); f_bar(z=0) = {fbar(1.0)}; f constant for "
      f"|delta theta/theta| <= 0.9: {nbhd}; growth D/D_LCDM(z=0) = {ratio:.8f}; sigma_8 = {s8:.4f}")
OUT["numbers"]["a"] = aout
a_ok = all(v["f_bar_z0"] == 0.0 and v["nbhd_const"] and abs(v["growth_ratio_z0"] - 1) < 1e-6 for v in aout.values())
check("A1 (a) FRW: f = 0 on the background and in a finite neighbourhood (MOND term absent from the quadratic action); "
      "growth = LCDM within 1e-6 (all theta_b routes with threshold theta_on = a0/c, and R2 at x = theta/3H >= 1)",
      "; ".join(f"{f}: f {v['f_bar_z0']}, D ratio {v['growth_ratio_z0']:.3g}, sigma_8 {v['sigma8']:.3f}" for f, v in aout.items()), a_ok)
if MUTATE:
    mut = min(v["growth_ratio_z0"] for v in aout.values())
    check("MUTATE growth: the sign-flipped switch is ON on FRW and gives chassis-like fast growth (ratio >= 3)",
          f"min growth ratio {mut:.2f}; sigma_8 " + ", ".join(f"{v['sigma8']:.2f}" for v in aout.values()), mut >= 3.0)

# ============================================================================== (b) static bound + fidelity
banner("(b) STATIC VIRIALISED SYSTEM: ON, fidelity at r = 30 kpc, R3 reach and timing")
r30 = 30 * KPC
b_on = f_of_theta(0.0, 1.0)
check("B1 (b1) static bound: theta_b = 0 => f = 1 (nu_mono) for every theta_b route", f"f(theta_b = 0) = {b_on}", b_on == 1.0)
# R1/R2 slaved flicker test: theta_b = 0.1 Omega(30 kpc)
r1 = {}
for hk in HOSTS:
    tr = TRS[KEY(*hk)]
    gi = float(np.interp(r30, tr["r"], tr["g"])); Om30 = math.sqrt(gi / r30)
    th = 0.1 * Om30
    for lab, ths in (("R2 3H", 3 * tr["H"]), ("R1 a0/c", TH_ON[hk[2]])):
        xx = th / ths
        r1.setdefault(lab, []).append(dict(host=KEY(*hk), x=xx, W_sat=float(1 - S_step(xx)[0]), W_ramp_dev=xx))
for lab, rows in r1.items():
    P(f"  {lab}: x = 0.1 Omega/theta_* = {min(r['x'] for r in rows):.3g}-{max(r['x'] for r in rows):.3g}; saturated W "
      f"{min(r['W_sat'] for r in rows):.3g}-{max(r['W_sat'] for r in rows):.3g} (need >= 0.9); ramp |W - 1| up to {max(r['W_ramp_dev'] for r in rows):.3g}")
r1_ok = all(r["W_sat"] >= 0.9 and r["W_ramp_dev"] <= 0.1 for rows in r1.values() for r in rows)
check("B2 (b2) R1/R2 slaved fidelity: a 10% compression at Omega(30 kpc) keeps W >= 0.9 (saturated) and |W - 1| <= 0.1 (ramp)",
      "; ".join(f"{lab}: x min {min(r['x'] for r in rows):.3g}" for lab, rows in r1.items()), r1_ok,
      "theta_* <= 3H while Omega_dyn >> H: any compression flips (saturated) or overshoots (ramp) a slaved theta gate")
OUT["numbers"]["b2_R1"] = r1
# R2 ramp K-dot force (W'(0+) = -1): |dB/dr| (1+q)/3 / (rho_b g) at 30 kpc (saturated step: W'(0) = 0, force 0)
kd = []
for hk in HOSTS:
    tr = TRS[KEY(*hk)]
    dB = np.gradient(tr["B"], tr["r"]); i = int(np.searchsorted(tr["r"], r30))
    z = hk[0]; Oz = Om * (1 + z) ** 3 / (Om * (1 + z) ** 3 + 1 - Om); q = 0.5 * Oz - (1 - Oz)
    kd.append(abs(dB[i]) * (1 + q) / 3 / (tr["rho_b"][i] * tr["g"][i]))
P(f"  R2 ramp: K-dot force / (rho_b g) at 30 kpc = {min(kd):.3g}-{max(kd):.3g} (saturated step: 0, since W'(0) = 0)")
OUT["numbers"]["b1_R2_ramp_Kdot_force_ratio"] = [min(kd), max(kd)]

# R3 zero-constant: luminal range and timing
z0 = {}
for hk in HOSTS:
    z, Mb, f = hk; Hh = Hz(z); rt = RTA[KEY(*hk)]
    for lab, M in (("a0/c", A0[f] / CL), ("H(z)", Hh), ("3H(z)", 3 * Hh)):
        ell = CL / M
        z0.setdefault(lab, []).append(dict(host=KEY(*hk), ell_Mpc=ell / (1e3 * KPC), ell_over_rta=ell / rt,
                                           reach=ell <= rt / 3.89, timing=M >= math.sqrt(3) * Hh))
for lab, rows in z0.items():
    P(f"  R3 zero-constant M = {lab}: ell = c/M = {min(r['ell_Mpc'] for r in rows):.3g}-{max(r['ell_Mpc'] for r in rows):.3g} Mpc; "
      f"ell/r_ta {min(r['ell_over_rta'] for r in rows):.3g}-{max(r['ell_over_rta'] for r in rows):.3g} (need <= 0.257); "
      f"timing M >= sqrt3 H on {sum(r['timing'] for r in rows)}/24")
z0_ok = any(all(r["reach"] and r["timing"] for r in rows) for rows in z0.values())
check("B3 (b3) R3 zero-constant (c_sigma = c, framework mass): reach ell <= r_ta/3.89 and timing M >= sqrt3 H on all hosts",
      "; ".join(f"{lab}: min ell/r_ta {min(r['ell_over_rta'] for r in rows):.3g}" for lab, rows in z0.items()), z0_ok,
      "a luminal switch with a Hubble-scale mass averages theta_b over Gpc: it cannot be ON inside a ~Mpc bound region")
OUT["numbers"]["b3_R3_zero"] = {lab: dict(ell_over_rta_min=min(r["ell_over_rta"] for r in rows)) for lab, rows in z0.items()}

# R3 costed feasibility at its most lenient admissible point
Mmin = max(math.sqrt(3) * Hz(z) for z in ZS)
ellmax = min(RTA.values()) / 3.89
csig = Mmin * ellmax
Bedge = max(float(np.max(TRS[KEY(*hk)]["B"][(TRS[KEY(*hk)]["t"] > 0) & (TRS[KEY(*hk)]["t"] < 1)])) for hk in HOSTS)
P(f"  R3 costed lenient point: M = sqrt3 H(4) = {Mmin:.3e} 1/s ({Mmin/H0:.2f} H0); ell = min r_ta/3.89 = {ellmax/KPC:.1f} kpc; "
      f"c_sigma = {csig/1e3:.2f} km/s; B_edge,max = {Bedge:.3e} J/m^3 (R = 1)")


def fidelity(rho_b, Gam2, cs, k_, M, cs_sig, Zc, Cc):
    A = cs ** 2 * k_ ** 2 - Gam2; b = cs_sig ** 2 * k_ ** 2 + M ** 2; Gc = Cc ** 2 * k_ ** 2 / (rho_b * Zc)
    roots = np.roots([1.0, -(A + b + Gc), A * b])
    wg = roots[np.argmin(np.abs(roots - A))].real
    return abs(wg / A - 1), Gc / A


def rho_ph(tr, Mb):
    y = tr["y"]
    return np.maximum(Mb * MS * (NS["h_of"](y) - y * NS["dh_of"](y)) / (2 * math.pi * tr["r"] ** 3 * y), 0.0)


cost = {}
for thlab in ("a0/c", "3H0"):
    for mode in ("universal", "lenient"):
        rows = []
        for hk in HOSTS:
            z, Mb, f = hk; tr = TRS[KEY(*hk)]
            th_on = TH_ON[f] if thlab == "a0/c" else 3 * H0
            m = (tr["t"] > 0) & (tr["t"] < 1)
            if mode == "universal":
                M, ell, Be = Mmin, ellmax, Bedge
            else:
                M, ell, Be = math.sqrt(3) * Hz(z), RTA[KEY(*hk)] / 3.89, float(np.max(tr["B"][m]))
            Zc = Be / M ** 2; Cc = Zc * M ** 2 / th_on
            i = int(np.searchsorted(tr["r"], r30)); rb = tr["rho_b"][i]
            Gm2 = 4 * math.pi * G * (rb / FB + rho_ph(tr, Mb)[i])
            for cslab in ("1e6K", "1e5K"):
                for kk in (1 / KPC, 1 / (10 * KPC)):
                    dev, GA = fidelity(rb, Gm2, CS[cslab], kk, M, M * ell, Zc, Cc)
                    rows.append(dict(host=KEY(*hk), cs=cslab, k_inv_kpc=1 / kk / KPC, dev=float(dev), G_over_A=float(GA)))
        cost[f"{thlab}/{mode}"] = rows
        r6 = [r for r in rows if r["cs"] == "1e6K"]
        P(f"  R3 costed, theta_on = {thlab:4s}, {mode:9s}: F_b dev (1e6 K) {min(r['dev'] for r in r6):.3g}-{max(r['dev'] for r in r6):.3g}; "
          f"passing (<= 0.1) {sum(r['dev'] <= 0.1 for r in r6)}/{len(r6)}")
cu = [r for r in cost["a0/c/universal"] if r["cs"] == "1e6K"]
check("B4 (b2) R3 costed (scored: theta_on = a0/c, universal constants at their most lenient point, R = 1): gas compressive "
      "mode changed <= 10% at r = 30 kpc, k = 1/kpc and 1/10 kpc, on all 24 hosts (1e6 K)",
      f"dev {min(r['dev'] for r in cu):.3g}-{max(r['dev'] for r in cu):.3g}; passing {sum(r['dev'] <= 0.1 for r in cu)}/48",
      all(r["dev"] <= 0.1 for r in cu), "the trigger coupling C = Z M^2/theta_on must be large because theta_on <= 3H; "
      "its gyroscopic mixing with the bound gas is G/b ~ R B_edge k^2/(rho theta_on^2 (1 + k^2 ell^2))")
OUT["numbers"]["b_R3_costed"] = {k_: dict(dev_min=min(r["dev"] for r in v if r["cs"] == "1e6K"), dev_max=max(r["dev"] for r in v if r["cs"] == "1e6K"),
                                          n_pass=sum(r["dev"] <= 0.1 for r in v if r["cs"] == "1e6K")) for k_, v in cost.items()}
OUT["numbers"]["R3_lenient_point"] = dict(M_over_H0=Mmin / H0, ell_kpc=ellmax / KPC, c_sigma_kms=csig / 1e3, B_edge=Bedge)

# ============================================================================== (c) transition
banner("(c) TRANSITION: ghost / gradient / Hadamard; the switch width the theory picks")
# R1: ghost on every layer (C1); R3: gyroscopic -> healthy; negative-w root bounded by Jeans (checked on a grid of signs)
rng = np.random.default_rng(347)
bad = 0
for _ in range(20000):
    A = rng.uniform(-1, 1) * 10 ** rng.uniform(-3, 3); b = 10 ** rng.uniform(-3, 3); Gc = 10 ** rng.uniform(-3, 6)
    rts = np.roots([1.0, -(A + b + Gc), A * b])
    if np.any(np.abs(rts.imag) > 1e-9 * np.abs(rts).max()) or np.min(rts.real) < min(A, 0) * (1 + 1e-9) - 1e-12:
        bad += 1
check("C3 (c) R3 H1-H3: kinetic matrix diag(rho, Z) > 0 (no ghost); principal speeds^2 real > 0; every root w is "
      "real and w >= min(A, 0) >= -Gamma^2, so growth never exceeds Jeans (uniform in k: Hadamard well posed) -- 20000 random cases",
      f"violations {bad}/20000", bad == 0 and not MUTATE or (MUTATE and bad == 0))
check("C4 (c) R1 saturated slaved gate H1: m(k) > 0 on the layers", "ghost on 24/24 (C1)", False,
      "XR36's mirror lemma: a gate saturated at theta <= 0 has W'' < 0 just above 0 -> pole at k_g, ghost beyond")
xr = sp.Symbol("x_r")
ramp_W2 = sp.diff(1 - xr, xr, 2)
check("C5 (c) R1 ramp H1: W = 1 - x on x < 1 (unsaturated) has W'' = 0, and its only kink, at x = 1, is convex (W' jumps "
      "from -1 to 0), so m(k) = rho + B W'' k^2/theta_*^2 >= rho > 0 (no pole)", f"W'' = {ramp_W2}; kink +1", ramp_W2 == 0)
# characteristic speeds (reported; criterion B allows them w.r.t. the khronon foliation but they are recorded as liabilities)
sup = {}
for hk in HOSTS:
    tr = TRS[KEY(*hk)]; m = (tr["t"] > 0) & (tr["t"] < 1)
    g_ = (Bedge / TH_ON[hk[2]]) ** 2 / (tr["rho_b"][m] * Bedge / Mmin ** 2)   # C^2/(rho Z), costed universal point
    sup[KEY(*hk)] = float(np.max(g_) / CL ** 2)
P(f"  R3 costed universal point: principal C^2/(rho Z) on the layers = {min(sup.values()):.3g}-{max(sup.values()):.3g} c^2 -> the fast "
  f"characteristic speed is {math.sqrt(min(sup.values())):.3g}-{math.sqrt(max(sup.values())):.3g} c")
P("  R3 zero-constant (c_sig = c): p(c^2) = (c_s^2 - c^2)(c^2 - c^2) - g c^2 = -g c^2 < 0 for ANY coupling g > 0, so one "
  "characteristic is strictly superluminal (Lean T6); allowed by criterion B only relative to the khronon foliation")
OUT["numbers"]["superluminal_costed_c2"] = [min(sup.values()), max(sup.values())]
# the Lean fidelity bound T5: F_b requires G <= b/9 + A/10 (A > 0); report the minimum ratio on the scored configuration
t5 = []
for hk in HOSTS:
    tr = TRS[KEY(*hk)]; i = int(np.searchsorted(tr["r"], r30)); rb = tr["rho_b"][i]
    Gm2 = 4 * math.pi * G * (rb / FB + rho_ph(tr, hk[1])[i])
    Zc = Bedge / Mmin ** 2; Cc = Bedge / TH_ON[hk[2]]
    for kk in (1 / KPC, 1 / (10 * KPC)):
        A = CS["1e6K"] ** 2 * kk ** 2 - Gm2; b = (Mmin * ellmax) ** 2 * kk ** 2 + Mmin ** 2; Gc = Cc ** 2 * kk ** 2 / (rb * Zc)
        if A > 0:
            t5.append(Gc / (b / 9 + A / 10))
P(f"  T5 ratio G/(b/9 + A/10) on the scored configuration (F_b needs <= 1): min {min(t5):.3g}, max {max(t5):.3g} over {len(t5)} rows")
OUT["numbers"]["T5_ratio"] = [min(t5), max(t5), len(t5)]
wid = {}
for hk in HOSTS:
    tr = TRS[KEY(*hk)]; m = (tr["t"] > 0) & (tr["t"] < 1)
    l3 = np.sqrt(Bedge / tr["rho_b"][m]) / TH_ON[hk[2]]
    wid[KEY(*hk)] = dict(R1=[c1[KEY(*hk)]["lo"], c1[KEY(*hk)]["hi"]], R3=[float(l3.min() / KPC), float(l3.max() / KPC)])
r1w = [min(v["R1"][0] for v in wid.values()), max(v["R1"][1] for v in wid.values())]
r3w = [min(v["R3"][0] for v in wid.values()), max(v["R3"][1] for v in wid.values())]
P(f"  ell_theta (R1 slaved pole 1/k_g): {r1w[0]:.0f}-{r1w[1]:.0f} kpc; (R3 costed universal, sqrt(B_edge/rho)/theta_on): "
  f"{r3w[0]:.3g}-{r3w[1]:.3g} kpc; CFG337 ell_min 183-378 kpc (C2 lenient) / 2.9 Mpc (C1); tolerance 100 (500) kpc")
OUT["numbers"]["width"] = dict(R1_kpc=r1w, R3_kpc=r3w, per_host=wid)

# ============================================================================== verdict
banner("VERDICT (frozen rule)")
routes = {
    "R1 saturated (theta_* = a0/c)": dict(a=a_ok, b=False, c=False, n=0),
    "R1 ramp (theta_* = a0/c)": dict(a=a_ok, b=False, c=ramp_W2 == 0, n=0),
    "R2 leaf (theta_* = 3H), saturated": dict(a=a_ok, b=False, c=False, n=0),
    "R3 zero-constant (c_sigma = c, M framework rate)": dict(a=a_ok, b=z0_ok, c=bad == 0, n=0),
    "R3 costed (c_sigma, M, Z)": dict(a=a_ok, b=all(r["dev"] <= 0.1 for r in cu), c=bad == 0, n=3),
}
tier = lambda r: ("FIRST-PRINCIPLES CANDIDATE" if (r["a"] and r["b"] and r["c"] and r["n"] == 0) else
                  "CANDIDATE WITH COST" if (r["a"] and r["b"] and r["c"]) else
                  "PARTIAL" if (r["a"] + r["b"] + r["c"]) == 2 else "NO-GO")
order = ["FIRST-PRINCIPLES CANDIDATE", "CANDIDATE WITH COST", "PARTIAL", "NO-GO"]
for nm, r in routes.items():
    r["tier"] = tier(r)
    P(f"  {nm:52s}: (a) {'P' if r['a'] else 'F'} (b) {'P' if r['b'] else 'F'} (c) {'P' if r['c'] else 'F'}; new constants {r['n']} -> {r['tier']}")
bt = min(order.index(r["tier"]) for r in routes.values())
bests = [nm for nm, r in routes.items() if order.index(r["tier"]) == bt and r["n"] == min(rr["n"] for rr in routes.values() if order.index(rr["tier"]) == bt)]
P(f"\n  OVERALL: {order[bt]} (best routes: {'; '.join(bests)})")
OUT["verdict"] = dict(overall=order[bt], best_routes=bests, routes=routes)
P(f"\n  elapsed {time.time() - T0:.1f} s")
json.dump(OUT, open(os.path.join(HERE, f"cfg347_switch_results{SUF}.json"), "w"), indent=1, default=str)
P("  checks: " + ", ".join(f"{n.split()[0]} {'PASS' if ok else 'FAIL'}" for n, ok in CH))
sys.exit(1 if MUTATE and not a_ok else 0)
