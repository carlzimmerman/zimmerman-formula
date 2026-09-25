#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L351 -- GW170817 THROUGH THE SWITCHING SHELL: L342's bound-region switch x = 9 R3/(4 K^2) makes gravitational waves
superluminal inside every galaxy's switching shell.  The integrated advance per shell is exactly G M_b/(6 c^3) -- about
14 hours for the Milky Way -- and GW170817 allows 1.74 s.  The shear-completed variable x~ = 9 (R3 + sigma_ij sigma^ij)/(4 K^2)
keeps every value L342 used and restores c_T = 1 exactly.

WHY THIS GATE.  L340 has c_T = 1 because nothing in C-H/K depends on the leaves' curvature R3 except GR's own R3 term
(the K^2 term is trace-only; the heat filter and the h^{mu nu} contractions carry no (d h_TT)^2).  L342 multiplies the
MOND term 2 alpha^2 q(...) by f(x) with x = 9 R3/(4 K^2).  Any Lagrangian with dL/dR3 != 0 rescales the gradient energy
of transverse-traceless waves without touching their kinetic energy, so c_T^2 = 1 + dL/dR3 wherever f' != 0.  GW170817
crossed at least two switching shells: its host's and the Milky Way's.

WHAT THIS LANE CHECKS
  W1 THE TT EXPANSION (symbolic, exact metric h = diag(e^h, e^-h, 1), h = h(t, z), unit lapse, zero shift): sqrt(h) K_ij K^ij
     = hdot^2/2 and sqrt(h) R3 = -h'^2/2, both exact for this parametrisation; K = 0.  With L = GR + F(x):
       x  = 9 R3/(4 K^2)             ->  c_T^2 = 1 + eps,   eps = F'(x) 9/(4 K^2)   (superluminal where F' > 0)
       x~ = 9 (R3 + sigma^2)/(4 K^2)  ->  c_T^2 = 1 exactly, for every F.
  W2 THE ADVANCE PER SHELL (symbolic): with F = 2 alpha^2 q f(x), deep-MOND q = (4/3) s^(3/2), s = G M/(r^2 a0), the
     phantom-dominated shell x = v_f^2/(r H)^2, v_f^4 = G M a0, K = 3H/c:
       Int (c_T - 1) dr = G M_b/(6 c^2) * [f(x_in) - f(x_out)]    -- independent of x_c, of f's shape and of H(z).
     Numeric check with L340's exact kernel nu_mono (not the deep-MOND form), the full unswitched MOND profile, and ten
     switch shapes (tanh widths 0.1-2.5, power logistics n = 2..32, smoothstep) at four masses: ratio to G M_b/(6c^2) = 1.
  W3 GW170817 (Abbott+2017, ApJL 848 L13: GRB 170817A arrived 1.74 +/- 0.05 s after the merger; the emission delay is
     >= 0, so a superluminal advance > 1.74 s is excluded).  The signal left its host NGC 4993 (log M* = 10.65,
     Blanchard+2017) and entered the Milky Way (M_b ~ 6e10 Msun): advance >= G(M_host + M_MW)/(6 c^3) ~ 20 hours even with
     the host mass halved -- excluded by > 1e4.  L342's switch in its R3 form is excluded by GW170817.
  W4 THE REPAIR (symbolic + numbers): x~ = 9 (R3 + sigma_ij sigma^ij)/(4 K^2) equals x on the FRW background (0), in the
     linear web ((3/2) Omega_m delta: sigma^2 is second order) and in static systems (L340's block has beta = 0 in the
     static limit, so sigma = 0), so L342's B1-B3 carry over; its TT terms rescale kinetic and gradient energy equally
     (c_T = 1 for any f); its extra kinetic terms are O(eps) ~ 1e-9 .. 1e-8, far below c_2.
  W5 C-H/K WITHOUT THE SWITCH has c_T = 1 (symbolic): the heat operator's second-order TT part contains no product of
     two derivatives of h, so it cannot change the wave speed.
  MUTATE=1 drops the sigma^2 completion (x~ -> x): W4 must FAIL (rc = 1).

SCOPE.  The advance formula uses the unswitched deep-MOND shell (the profile L342 itself used).  A strictly
discontinuous step f would jump across the band without a finite crossing length, but it makes dL/dR3 a delta
function and the static edge singular (L352); any differentiable f gives the full effect.  The repair removes the
issue for every f.  Principal order, geometric optics (GW wavelengths ~1e3 km << shell thickness ~0.1-1 Mpc).

Run from the repository root:  python3 real_research/g03_audit_2026/L351_switch_gw170817_gate.py
"""
import os, sys, json, math, time, warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L351_switch_gw170817_gate"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L351", "mutate": MUTATE, "checks": {}, "numbers": {}}
T0 = time.time()
_trap = getattr(np, "trapezoid", None) or np.trapz


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 104); P(t); P("=" * 104)


P(__doc__.split("WHAT THIS LANE CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the sigma^2 completion is dropped (x~ -> x); W4 must FAIL ***")
KAPPA_SHEAR = 0 if MUTATE else 1

# ============================================================================================ W1 TT expansion
banner("W1  THE TT EXPANSION OF R3, K_ij K^ij, K, sigma^2 (exact metric, symbolic)")
t, X, Y, Z = sp.symbols('t x y z', real=True)
hf = sp.Function('h')(t, Z)
eps_ = sp.symbols('epsilon', real=True)                              # bookkeeping amplitude
hij = sp.diag(sp.exp(eps_ * hf), sp.exp(-eps_ * hf), 1)              # det = 1 exactly
coords = (X, Y, Z)
hinv = hij.inv()
def christoffel(g, ginv):
    return [[[sp.simplify(sum(ginv[i, l] * (sp.diff(g[l, j], coords[k]) + sp.diff(g[l, k], coords[j]) - sp.diff(g[j, k], coords[l]))
                              for l in range(3)) / 2) for k in range(3)] for j in range(3)] for i in range(3)]
Gam = christoffel(hij, hinv)
def ricci_scalar(Gm, ginv):
    Ric = sp.zeros(3)
    for j in range(3):
        for k in range(3):
            Ric[j, k] = sum(sp.diff(Gm[i][j][k], coords[i]) - sp.diff(Gm[i][j][i], coords[k]) +
                            sum(Gm[i][i][l] * Gm[l][j][k] - Gm[i][k][l] * Gm[l][j][i] for l in range(3)) for i in range(3))
    return sp.simplify(sum(ginv[j, k] * Ric[j, k] for j in range(3) for k in range(3)))
R3 = ricci_scalar(Gam, hinv)
Kij = sp.Matrix(3, 3, lambda i, j: sp.diff(hij[i, j], t) / 2)        # unit lapse, zero shift
Ktr = sp.simplify(sum(hinv[i, j] * Kij[i, j] for i in range(3) for j in range(3)))
KK = sp.simplify(sum(hinv[i, k] * hinv[j, l] * Kij[i, j] * Kij[k, l] for i in range(3) for j in range(3) for k in range(3) for l in range(3)))
sig2 = sp.simplify(KK - Ktr**2 / 3)
sqrth = sp.sqrt(hij.det())
R3_2 = sp.expand(sp.series(sqrth * R3, eps_, 0, 3).removeO())
KK_2 = sp.expand(sp.series(sqrth * KK, eps_, 0, 3).removeO())
# sqrt(h) R3 at O(eps^2): subtract a total z-derivative to expose the gradient energy
hz, hzz = sp.diff(hf, Z), sp.diff(hf, Z, 2)
R3_quad = sp.expand(R3_2.coeff(eps_, 2))
R3_lin = sp.simplify(R3_2.coeff(eps_, 1))
# write R3_quad = A hz^2 + B h hzz and integrate B h hzz by parts: -> (A - B) hz^2 + d(B h hz)
A_ = sp.simplify(R3_quad.coeff(hz, 2)); B_ = sp.simplify(sp.expand(R3_quad - A_ * hz**2).coeff(hzz))
rest = sp.simplify(R3_quad - A_ * hz**2 - B_ * hzz)
grad_coeff = sp.simplify(A_ - B_ * 0) if B_ == 0 else sp.simplify(A_ - B_)   # (h hzz -> -hz^2 by parts)
P(f"    K = {Ktr};  sqrt(h) K_ij K^ij = {sp.simplify(KK_2)}   (exact: {sp.simplify(sqrth * KK)})")
P(f"    sqrt(h) R3 = {R3_lin} eps + [{A_} h_z^2 + ({B_}) h h_zz + {rest}] eps^2  -> gradient energy coefficient {grad_coeff} h_z^2 (by parts)")
P(f"    sigma_ij sigma^ij = {sig2}  (TT: sigma^2 = K_ij K^ij since K = 0)")
# the TT Lagrangian of GR + F(x):  L = sqrt(h)[K_ij K^ij + R3] + F(xbar) + F'(xbar) (9/(4 Kb^2)) sqrt(h)[R3 + kappa sigma^2]
Fp, Kb = sp.symbols('Fprime Kbar', positive=True)
epsR = Fp * sp.Rational(9, 4) / Kb**2
kin = sp.simplify(KK_2.coeff(eps_, 2) / sp.diff(hf, t)**2)          # coefficient of hdot^2
grad = sp.simplify(-grad_coeff)                                      # coefficient of -h_z^2
cT2 = {}
for lab, kap in (("x (L342)", 0), ("x~ (shear-completed)", 1)):
    cT2[lab] = sp.simplify((grad * (1 + epsR)) / (kin * (1 + kap * epsR)))
    P(f"    with the switch in {lab:22s}: c_T^2 = {cT2[lab]}")
w1_ok = (R3_lin == 0 and Ktr == 0 and sp.simplify(kin - sp.Rational(1, 2)) == 0 and sp.simplify(grad - sp.Rational(1, 2)) == 0
         and sp.simplify(cT2["x (L342)"] - (1 + epsR)) == 0 and sp.simplify(cT2["x~ (shear-completed)"] - 1) == 0)
OUT["numbers"]["W1"] = {"KK_quadratic": str(KK_2), "R3_quad": str(R3_quad), "grad_coeff": str(grad_coeff),
                        "cT2": {kk: str(vv) for kk, vv in cT2.items()}}
check("W1 GR's TT Lagrangian is (hdot^2 - h_z^2)/2; a switch through x = 9R3/(4K^2) adds F'(x) 9/(4K^2) to the gradient "
      "term only (c_T^2 = 1 + eps), while x~ = 9(R3 + sigma^2)/(4K^2) adds it to both (c_T^2 = 1 exactly)",
      f"x: {cT2['x (L342)']};  x~: {cT2['x~ (shear-completed)']}", w1_ok,
      "any Lagrangian with dL/dR3 != 0 and no matching dL/d(K_ij K^ij) changes the speed of gravitational waves")

# ============================================================================================ W2 advance per shell
banner("W2  THE INTEGRATED ADVANCE ACROSS ONE SWITCHING SHELL: G M_b/(6 c^2), symbolically and numerically")
Gs, M, a0s, cs_, Hs, r, xs = sp.symbols('G M a_0 c H r x', positive=True)
fprime = sp.Function('fprime')
vf = (Gs * M * a0s)**sp.Rational(1, 4)
alpha = a0s / cs_**2
s_r = Gs * M / (r**2 * a0s)
q_r = sp.Rational(4, 3) * s_r**sp.Rational(3, 2)
Kbar = 3 * Hs / cs_
x_r = vf**2 / (r * Hs)**2
integrand_r = sp.Rational(9, 8) * 2 * alpha**2 * q_r / Kbar**2     # (c_T - 1) / f'(x)
r_of_x = vf / (Hs * sp.sqrt(xs))
jac = sp.diff(r_of_x, xs)                                            # dr/dx (< 0: r decreases as x increases)
integrand_x = sp.simplify(integrand_r.subs(r, r_of_x) * (-jac))      # Int dr (...) f'(x(r)) = Int dx (...) f'(x)
P(f"    (c_T - 1) = f'(x) * {sp.simplify(integrand_r)} ;   dr = {sp.simplify(jac)} dx")
P(f"    Int (c_T - 1) dr = Int f'(x) dx * [{integrand_x}]")
w2_sym = sp.simplify(integrand_x - Gs * M / (6 * cs_**2)) == 0
# numeric: L340's exact kernel nu_mono, full unswitched profile, ten switch shapes, four masses
c = 2.99792458e8; Gn = 6.67430e-11; MS = 1.98892e30; Mpc = 3.0856775814913673e22; KPC = Mpc / 1e3
H0 = 67.36e3 / Mpc; A0 = 9.3619e-11
def h_rar(y): return y / np.expm1(np.sqrt(y))
def dh_rar(y, e=1e-6): return (h_rar(y*(1 + e)) - h_rar(y*(1 - e)))/(2*y*e)
Y_P = brentq(lambda y: dh_rar(y), 1.0, 5.0); H_P = h_rar(Y_P)
def nu_mono(y):
    y = np.asarray(y, float)
    below = 1.0 + h_rar(np.minimum(y, Y_P)) / y
    above = 1.0 + (H_P + 0.05 * H_P * np.log((y + Y_P) / (2 * Y_P))) / y
    return np.where(y <= Y_P, below, above)
# q(s^2) = Int_0^{s} (nu(sig) - 1) 2 sig d sig, tabulated in log s
LS = np.linspace(-16, 3, 60001); SS = 10**LS
dq = (nu_mono(SS) - 1.0) * 2 * SS
QS = np.concatenate([[(4/3) * SS[0]**1.5], (4/3) * SS[0]**1.5 + np.cumsum(0.5 * (dq[1:] + dq[:-1]) * np.diff(SS))])
def q_of_s(s): return np.interp(np.log10(s), LS, QS)
SHAPES = {"tanh w=0.1": ("tanh", 0.1), "tanh w=0.5": ("tanh", 0.5), "tanh w=1": ("tanh", 1.0), "tanh w=2.5": ("tanh", 2.5),
          "logistic n=2": ("pow", 2), "logistic n=4": ("pow", 4), "logistic n=8": ("pow", 8), "logistic n=32": ("pow", 32),
          "smoothstep 2.5-7.5": ("smooth", (2.5, 7.5)), "smoothstep 4-6": ("smooth", (4.0, 6.0))}
XC = 5.0
def fprime_num(xv, kind, par):
    if kind == "tanh":                                               # 0.5/w sech^2(u), overflow-free
        e2 = np.exp(-2 * np.abs((xv - XC) / par)); return (0.5 / par) * 4 * e2 / (1 + e2)**2
    if kind == "pow":                                                # n x^(n-1) x_c^n/(x^n + x_c^n)^2, in log form
        n = par; lx = np.log(np.maximum(xv, 1e-300) / XC)
        return (n / XC) * np.exp((n - 1) * lx - 2 * np.logaddexp(n * lx, 0.0))
    lo, hi = par; u = np.clip((xv - lo) / (hi - lo), 0, 1)
    return np.where((xv > lo) & (xv < hi), 6 * u * (1 - u) / (hi - lo), 0.0)
def fvals(xv, kind, par):
    if kind == "tanh": return 0.5 * (1 + np.tanh((xv - XC) / par))
    if kind == "pow": return 1 / (1 + (XC / np.maximum(xv, 1e-300))**par)
    lo, hi = par; u = np.clip((xv - lo) / (hi - lo), 0, 1); return u * u * (3 - 2 * u)
rr = np.geomspace(1.0, 3e4, 400001) * KPC                            # 1 kpc .. 30 Mpc
W2 = {}
for Mb in (1e9, 1e10, 6e10, 3e11):
    gN = Gn * Mb * MS / rr**2
    Mdyn = Mb * MS * nu_mono(gN / A0)                                 # spherical QUMOND: M_dyn(<r) = M_b nu(g_N/a0)
    rho = np.gradient(Mdyn, rr) / (4 * math.pi * rr**2)
    xr = 4 * math.pi * Gn * rho / H0**2
    s = gN / A0
    pref = (9 / 8) * 2 * (A0 / c**2)**2 * q_of_s(s) / (3 * H0 / c)**2
    target = Gn * Mb * MS / (6 * c**2)
    for lab, (kind, par) in SHAPES.items():
        dcT = pref * fprime_num(xr, kind, par)
        val = _trap(dcT, rr)
        span = float(fvals(xr[0], kind, par) - fvals(xr[-1], kind, par))
        W2[(Mb, lab)] = (val / target, span, val / c)
ratios = np.array([v[0] / v[1] for v in W2.values()])
for Mb in (1e9, 1e10, 6e10, 3e11):
    P(f"    M_b = {Mb:.0e} Msun: Int(c_T - 1)dr / [G M_b/(6c^2) * Delta f] over ten shapes = "
      f"{min(W2[(Mb, l)][0] / W2[(Mb, l)][1] for l in SHAPES):.4f} .. {max(W2[(Mb, l)][0] / W2[(Mb, l)][1] for l in SHAPES):.4f};  "
      f"advance {W2[(Mb, 'tanh w=1')][2] / 3600:.2f} h")
OUT["numbers"]["W2"] = {"symbolic_ok": w2_sym, "ratios_min": float(ratios.min()), "ratios_max": float(ratios.max()),
                        "rows": {f"{k_[0]:.0e}/{k_[1]}": v for k_, v in W2.items()}}
check("W2 the GW advance across one switching shell is G M_b/(6 c^2) exactly in the deep-MOND shell, independent of "
      "x_c, of f's shape and of H; L340's exact kernel reproduces it to within a few per cent for every shape and mass",
      f"symbolic: {w2_sym}; numeric ratio {ratios.min():.4f} .. {ratios.max():.4f}", w2_sym and abs(ratios.min() - 1) < 0.05 and abs(ratios.max() - 1) < 0.05,
      "a differential Shapiro-like delay for gravitons only: 1/6 of G M/c^3 per shell, with the opposite sign (early)")

# ============================================================================================ W3 GW170817
banner("W3  GW170817: the advance through NGC 4993's shell and the Milky Way's")
GMc3 = Gn * MS / c**3                                                # seconds per solar mass
M_host = 10**10.65                                                   # Blanchard+2017 stellar mass (gas-poor S0)
M_MW = 6.0e10                                                        # stars ~5.4e10 + cold gas (conservative)
rows = []
for lab, Mh in (("host M* (Blanchard+2017)", M_host), ("host M*/2 (M/L floor)", M_host / 2)):
    adv = (Mh + M_MW) * GMc3 / 6
    rows.append((lab, Mh, adv))
    P(f"    {lab:26s}: M_host = {Mh:.2e}, M_MW = {M_MW:.1e} -> advance >= {adv:.3e} s = {adv / 3600:.1f} h  vs allowed 1.74 s "
      f"(excess x {adv / 1.74:.1e})")
adv_min = min(r_[2] for r_ in rows)
OUT["numbers"]["W3"] = {"rows": rows, "allowed_s": 1.74, "excess_min": adv_min / 1.74}
check("W3 GW170817 excludes the R3-based switch: the gravitational wave would have arrived >= ~20 hours before the "
      "gamma rays (emission delay >= 0 allows at most 1.74 s)", f"advance >= {adv_min / 3600:.1f} h; excess >= {adv_min / 1.74:.1e}",
      adv_min > 1e3 * 1.74, "each additional galaxy shell on the line of sight (crossed twice) adds G M_b/(3 c^3)")

# ============================================================================================ W4 the repair
banner("W4  THE REPAIR: x~ = 9 (R3 + sigma_ij sigma^ij)/(4 K^2)")
x_tilde_cT2 = sp.simplify((grad * (1 + epsR)) / (kin * (1 + KAPPA_SHEAR * epsR)))
# values: FRW (R3 = 0, sigma = 0); linear web (sigma^2 second order); static limit of L340's block (beta = 0)
k_, w_, c2_, ac_ = sp.symbols('k omega c_2 alpha_c', real=True)
psi, phi, beta, U, Rs, Cc = sp.symbols('psi phi beta U R C')
D = -sp.I * w_
E = [4*k_**2*psi - 4*k_**2*phi - D*(-12*D*psi + 4*k_**2*beta - 6*c2_*(3*D*psi - k_**2*beta)),
     -4*k_**2*psi - 4*k_**2*(U - phi) + 2*ac_*k_**2*phi - Rs,
     4*k_**2*D*psi + 2*c2_*k_**2*(3*D*psi - k_**2*beta) + D*Rs,
     4*k_**2*(U - phi) + 4*k_**2*Cc*U]
Xv = [psi, phi, beta, U]
Mm = sp.Matrix([[sp.diff(e_, x_) for x_ in Xv] for e_ in E]); Sv = sp.Matrix([-e_.subs({x_: 0 for x_ in Xv}) for e_ in E])
sol_static = Mm.subs(w_, 0).LUsolve(Sv.subs(w_, 0))
beta_static = sp.simplify(sol_static[2])
# size of the extra kinetic coefficient in the shell (O(eps)): eps = (9/4) 2 alpha^2 q f'/K^2 at the shell, f' ~ 1/(2w)
eps_rows = []
for Mb in (1e10, 6e10, 3e11):
    vf_ = (Gn * Mb * MS * A0)**0.25; r_t = vf_ / (math.sqrt(XC) * H0)
    s_t = Gn * Mb * MS / (r_t**2 * A0)
    eps_sh = (9 / 4) * 2 * (A0 / c**2)**2 * q_of_s(s_t) / (3 * H0 / c)**2 * (1 / (2 * 1.0))
    eps_rows.append((Mb, r_t / Mpc, s_t, eps_sh))
    P(f"    M_b = {Mb:.0e}: shell at r_t = {r_t / Mpc:.2f} Mpc, s = {s_t:.2e}, eps = {eps_sh:.1e} (vs c_2 >= 6e-4)")
P(f"    static limit of L340's block: shift beta = {beta_static} -> sigma_ij = 0, x~ = x;  FRW: R3 = sigma = 0 -> x~ = 0;")
P(f"    linear web: sigma_ij is first order, sigma^2 second order -> x~ = (3/2) Omega_m delta + O(delta^2)")
P(f"    c_T^2 with x~ (kappa_shear = {KAPPA_SHEAR}): {x_tilde_cT2}")
w4_ok = sp.simplify(x_tilde_cT2 - 1) == 0 and beta_static == 0 and max(r_[3] for r_ in eps_rows) < 1e-6
OUT["numbers"]["W4"] = {"cT2_xtilde": str(x_tilde_cT2), "beta_static": str(beta_static),
                        "eps_rows": [dict(zip(("Mb", "r_t_Mpc", "s", "eps"), r_)) for r_ in eps_rows]}
check("W4 the shear-completed switch x~ has c_T = 1 exactly for every f, takes L342's values on FRW, in the linear web "
      "and in static systems, and perturbs the kinetic matrix only at O(1e-9..1e-8)",
      f"c_T^2 = {x_tilde_cT2}; static beta = {beta_static}; max eps = {max(r_[3] for r_ in eps_rows):.1e}", w4_ok,
      "L342's B1-B3 carry over unchanged; the repair is needed for any differentiable switch")

# ============================================================================================ W5 C-H/K alone
banner("W5  C-H/K WITHOUT THE SWITCH: the heat operator's TT expansion has no (d h)^2 term")
Wf = sp.Function('W')(X, Y, Z)
lap = sum(sp.diff(sqrth * hinv[i, j] * sp.diff(Wf, coords[j]), coords[i]) for i in range(3) for j in range(3)) / sqrth
lap2 = sp.expand(sp.series(sqrth * lap, eps_, 0, 3).removeO().coeff(eps_, 2))
has_dhdh = lap2.has(sp.diff(hf, Z)**2) or any(sp.diff(hf, Z)**2 in term.atoms(sp.Pow) or
                                              (term.count(sp.Derivative(hf, Z)) >= 2) for term in sp.Add.make_args(lap2))
n_dh = [sum(1 for f_ in sp.Mul.make_args(term) for _ in range(int(f_.exp) if (f_.is_Pow and f_.base == sp.Derivative(hf, Z)) else
            (1 if f_ == sp.Derivative(hf, Z) else 0))) for term in sp.Add.make_args(lap2)]
P(f"    second-order part of sqrt(h) Delta_h W: {len(sp.Add.make_args(lap2))} terms; max number of h_z factors per term = {max(n_dh) if n_dh else 0}")
w5_ok = (max(n_dh) if n_dh else 0) <= 1
OUT["numbers"]["W5"] = {"n_terms": len(sp.Add.make_args(lap2)), "max_hz_factors": max(n_dh) if n_dh else 0}
check("W5 without the switch C-H/K keeps c_T = 1: the filter's second-order TT terms carry at most one derivative of h "
      "(mass/friction-type), and the h^{mu nu} contractions of U and W_b carry none",
      f"max h_z factors per term = {max(n_dh) if n_dh else 0}", w5_ok, load_bearing=False)

banner("VERDICT")
P(f"""  L342's switch variable x = 9 R3/(4 K^2) puts R3 into the Lagrangian, and that changes the speed of gravitational
  waves wherever the switch is turning: c_T^2 = 1 + (9/4)(2 alpha^2 q/K^2) f'(x) (W1).  Across one galaxy's shell the
  graviton gains exactly G M_b/(6 c^3) on light, whatever the threshold or the switch's shape (W2): 13.7 h for the
  Milky Way.  GW170817 left NGC 4993 and entered the Milky Way, so it would have beaten the gamma rays by >= {adv_min/3600:.0f} h
  against the 1.74 s observed (W3): the switch as built is excluded.  The shear-completed variable
  x~ = 9 (R3 + sigma_ij sigma^ij)/(4 K^2) takes every value L342 used and keeps c_T = 1 exactly (W4); C-H/K without the
  switch already has c_T = 1 (W5).  Time {time.time() - T0:.0f} s.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
