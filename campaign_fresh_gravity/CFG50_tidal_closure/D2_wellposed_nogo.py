#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
D2 -- WELL-POSEDNESS AND CLOSURE NO-GO for a fluid whose stress/dynamics is a functional of the tidal tensor T_ij[Phi_b] of a baryon-only auxiliary potential.
(Companion of D1; action and notation as in D1.  kappa = 1/2 FITTED; nothing new fitted; labels DERIVED/POSTULATED/OPEN in the report.)

W1  STATE-INDEPENDENT STRESS/FORCE (the 'stress is a functional of Phi_b only' reading).  (i) 3-D linearised dust in a prescribed force density F(x) (independent of the fluid state): xi_tt = (F/rho0) (div xi) + ...
    -> omega^2 = -i (F.k)/rho0 (sympy eigenvalues): Hadamard ill-posed, growth ~ sqrt(k), for F.k != 0 (B4-Q1 in 3-D).  (ii) FROM AN ACTION: L = -rho0 e(rho,x) with e = -P_b(x)/rho (a state-independent pressure P_b) is Int P_b(x) J d^3a = Int P_b d^3x:
    its Euler-Lagrange force is IDENTICALLY ZERO (sympy).  So a state-independent stress derived from an action does nothing; imposed by hand it is ill-posed.
W2  LOCAL EOS NO-GO.  A fluid with a state-dependent barotropic-type energy W(rho, x) whose x-dependence enters through LOCAL fields of Phi_b (T_perp = g_N/r, g_N = rT_perp [i.e. r], rho_b), i.e. chemical potential mu(rho, T_perp, r, rho_b):
    static equilibrium mu' = -g_tot with the TARGET density rho_c = a0 T_perp/(4 pi G g_tot) requires (sympy, coefficients of rho_b and 1/r):  mu_rho = mu_T = 0 and mu_r = -g_tot(rho,T) -- inconsistent (mixed partials).  NO such EOS exists on generic baryon profiles.  (On the point-mass family rho_b = 0 the same equation is a first-order linear PDE and IS solvable: the obstruction is the extended-baryon term.)
W3  K-COUPLING (kinetic effective metric g_ij = delta_ij + chi T_ij).  Sympy dispersion of the linearised fluid: omega^2 = (k g^-1 k)(c_s^2 - 4 pi G rho0/k^2): hyperbolic iff g positive-definite; a negative eigenvalue of g = ghost (negative kinetic energy) AND gradient instability (omega^2 ~ -k^2, Hadamard ill-posed).
    Ghost boundary for the exponential sphere: chi_crit = -1/lambda_max (chi<0, the sign that SUPPORTS the fluid: a_f>0), +1/max(-lambda) (chi>0, anti-support).  DETECTOR CONTROLS: flagged just above chi_crit, not just below.
    Combined with D1: the largest ghost-free support fraction is ~0.5 (r ~ h), scale-free.
W4  FRW.  (i) uniform baryon density gives T_ij = (8 pi G rho_b/3) delta_ij = Omega_b H^2 delta_ij (sympy): S_int renormalises the fluid inertia m = 1 + chi Omega_b H^2 (growth: delta'' + (2H + m'/m) delta' = 4 pi G rho/m);
    with chi ~ the galaxy-scale value D1 requires (1e-4..1e-2 kpc^2/(km/s)^2), m(z=0) - 1 ~ 1e-7..1e-5 but m(z=1100) - 1 ~ 5e1..3e3: incompatible with GR+CDM at the CMB unless Phi_b is defined on the OVERDENSITY (Jeans swindle, POSTULATED), in which case the background is untouched.
    (ii) The auxiliary sector with a finite-c completion L = lambda(lap Phi_b - Phi_b_tt/c^2 - 4 pi G rho_b)/(4 pi G): kinetic matrix [[0,D],[D,0]], det = -D^2, D = k^2 - omega^2/c^2 -> a degenerate (dipole) ghost pair: OPEN (frozen in the static limit).
MUTATE=b : chi -> -chi (reverse the coupling).  The ghost boundary moves by x~90 and the force on the fluid turns inward (anti-support): W3's sign-specific assertions must FAIL.
Run: python3 D2_wellposed_nogo.py   (MUTATE=b for the control)
"""
import os, sys, math
import numpy as np
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from Dcommon import *

MUTATE = os.environ.get("MUTATE", "")
R = Report("D2_wellposed_nogo", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
SIGN = -1.0 if MUTATE == "b" else 1.0        # MUTATE b: reverse the sign of the coupling

# ------------------------------------------------------------------------------------------------ W1
R.banner("W1  state-independent force density / stress: 3-D Hadamard ill-posedness; zero force from an action")
F1, F2, F3, k1, k2, k3, rho0 = sp.symbols("F1 F2 F3 k1 k2 k3 rho0", positive=True)
Fv = sp.Matrix([F1, F2, F3]); kv = sp.Matrix([k1, k2, k3])
Mm = sp.I * Fv * kv.T / rho0                        # xi_tt = M xi  (WKB, leading order in k)
ev = Mm.eigenvals()
om2 = [sp.simplify(-e) for e in ev.keys()]          # omega^2 = -eigenvalue
P(f"    linearised dust, prescribed force density F(x): omega^2 in {om2}  (multiplicities {list(ev.values())})")
target = -sp.I * (F1 * k1 + F2 * k2 + F3 * k3) / rho0
has = any(sp.simplify(o - target) == 0 for o in om2)
P("    -> omega^2 = -i (F.k)/rho0: Im omega = sqrt(|F.k|/2rho0) grows as sqrt(k): Hadamard ill-posed whenever F.k != 0 (F = rho g_tot rhat for the target: omega^2 = -i g k_r)")
# action: 1-D Lagrangian coordinates
a, t = sp.symbols("a t", real=True)
xa = sp.Function("x")(a, t); rho_0 = sp.Function("rho_0")(a); Pb = sp.Function("P_b")
J = sp.diff(xa, a)
L_int = Pb(xa) * J                                          # = -rho0 e with e = -P_b(x)/rho, rho = rho0/J
from sympy.calculus.euler import euler_equations
xs_, Js_ = sp.symbols("xs_ Js_")
Lsym = Pb(xs_) * Js_
force = sp.diff(Lsym, xs_).subs({xs_: xa, Js_: J}) - sp.diff(sp.diff(Lsym, Js_).subs({xs_: xa, Js_: J}), a)   # dL/dx - d/da dL/dJ
res = sp.simplify(force.doit())
P(f"    EL force from L = -rho0 e(rho,x), e = -P_b(x)/rho  (i.e. L = Int P_b(x) J da): {res}")
check("W1 (sympy) a prescribed state-independent force density has omega^2 = -i F.k/rho0 (Hadamard ill-posed); the same 'pressure' derived from an action, L = Int P_b(x) d^3x, exerts identically zero force",
      f"omega^2 set {om2}; EL force residual {res}", has and res == 0)

# ------------------------------------------------------------------------------------------------ W2
R.banner("W2  no local EOS mu(rho, T_perp, r, rho_b) has the target as its static equilibrium")
rho, T, tau, u, Gs, a0 = sp.symbols("rho T tau u G a0", positive=True)       # tau = rho_b, u = 1/r
mu_rho, mu_T, mu_r, mu_tau = sp.symbols("mu_rho mu_T mu_r mu_tau")
g = a0 * T / (4 * sp.pi * Gs * rho)                                           # target: rho g_tot = a0 T_perp/(4 pi G)
Tp = u * (4 * sp.pi * Gs * tau - 3 * T)                                       # T_perp' = (4 pi G rho_b - 3 T)/r   (T_perp = g_N/r)
gp = 4 * sp.pi * Gs * (tau + rho) - 2 * g * u                                 # g_tot' = 4 pi G (rho_b + rho_c) - 2 g_tot/r   (self-gravity of the fluid included)
rhop = rho * (Tp / T - gp / g)                                                # rho_T = a0 T/(4 pi G g)
E = mu_rho * rhop + mu_T * Tp + mu_r + g                                     # mu' = -g_tot  (mu_tau tau' with tau' = rho_b' free => mu_tau = 0)
E = sp.expand(E)
P("    equilibrium mu' + g_tot = 0 with mu_tau = 0 (rho_b' is an independent profile function):")
cf = {}
for pw in (1, 0):
    cpoly = sp.Poly(E, tau)
cpoly = sp.Poly(E, tau)
c1 = sp.simplify(cpoly.coeff_monomial(tau))          # coefficient of rho_b   (contains u and non-u parts)
c1u = sp.simplify(sp.Poly(sp.expand(c1), u).coeff_monomial(u)); c1n = sp.simplify(sp.Poly(sp.expand(c1), u).coeff_monomial(1))
P(f"      coefficient of rho_b*u : {c1u}")
P(f"      coefficient of rho_b   : {c1n}")
sol = sp.solve([c1u, c1n], [mu_rho, mu_T], dict=True)[0]
P(f"      => {sol}")
c0 = sp.simplify(cpoly.coeff_monomial(1).subs(sol))
mur = sp.solve(c0, mu_r)[0]
P(f"      remaining equation gives mu_r = {sp.simplify(mur)}   (must equal d mu/dr at fixed rho, T, with mu_rho = mu_T = 0 ->  mu = mu(r) only)")
mixed = sp.simplify(sp.diff(mur, rho))               # d(mu_r)/d rho must equal d(mu_rho)/dr = 0
P(f"      integrability: d(mu_r)/d rho = {mixed}  vs  d(mu_rho)/dr = 0")
ok_w2 = (sol[mu_rho] == 0 and sol[mu_T] == 0 and mixed != 0)
check("W2 (sympy) no equation of state whose energy depends on x through LOCAL fields of Phi_b (T_perp, g_N ~ r T, rho_b) can have the target as its static equilibrium on generic baryon profiles: the coefficients of rho_b force mu_rho = mu_T = 0, then mu_r = -a0 T/(4 pi G rho) is inconsistent",
      f"mu_rho = {sol[mu_rho]}, mu_T = {sol[mu_T]}, mu_r = {sp.simplify(mur)}, d mu_r/d rho = {mixed} != 0", ok_w2)

# ------------------------------------------------------------------------------------------------ W3
R.banner("W3  K-coupling: linearised fluid in the effective metric g_ij = delta_ij + h_ij: hyperbolicity, ghost, gradient stability")
hr, hp, cs2, J4, kk, kr, kt = sp.symbols("h_r h_p c_s2 J kk k_r k_t", real=True)
gm = sp.diag(1 + hr, 1 + hp, 1 + hp)
kvv = sp.Matrix([kr, kt, 0])
Kmat = (cs2 - J4 / (kr**2 + kt**2)) * kvv * kvv.T           # restoring matrix (pressure + self-gravity, J = 4 pi G rho0)
Mmat = gm.inv() * Kmat
ev3 = {sp.simplify(k_): v for k_, v in Mmat.eigenvals().items()}
w2 = sp.simplify(kvv.T * gm.inv() * kvv)[0, 0] * (cs2 - J4 / (kr**2 + kt**2))
P(f"    omega^2 eigenvalues of g^-1 K: {list(ev3.keys())}")
P(f"    the propagating mode: omega^2 = (k g^-1 k)(c_s^2 - 4 pi G rho0/k^2) = {sp.simplify(w2)}")
ok_disp = any(sp.simplify(e - w2) == 0 for e in ev3.keys())
# ghost/gradient: with (1+h_r) < 0 : omega^2 -> -|.| k^2 for radial k at large k
kin_sign = sp.simplify(w2.subs({kt: 0}) / kr**2).subs(J4, 0)
P(f"    radial k: omega^2/k^2 (J -> 0) = {kin_sign} = c_s^2/(1 + h_r):  negative if 1 + h_r < 0 -> ghost (negative kinetic energy rho0 (1+h_r) xi_dot^2/2) AND gradient instability (omega^2 ~ -k^2: Hadamard ill-posed)")
check("W3a (sympy) omega^2 = (k g^-1 k)(c_s^2 - 4 pi G rho0/k^2): hyperbolic (real omega^2 at high k) iff the effective metric g_ij = delta + chi T_ij is positive-definite; a negative eigenvalue is simultaneously a ghost and a gradient instability", f"dispersion residual ok = {ok_disp}", ok_disp)

# exponential-sphere numbers
rows = {}
gate_flags = []
for Mb, hh in ((1e9, 2.0), (1e10, 3.0), (1e11, 4.0), (1e12, 5.0)):
    prof = exp_sphere(Mb, hh)
    bf = baryon_fields(prof, r0=1e-2 * hh, r1=30 * hh, n=6001)
    r_, g_ = bf["r"], bf["g"]
    d = lambda yv: np.gradient(yv, r_)
    a_f = (0.5 / bf["rho"]) * (d(bf["Trr"]) * bf["Prr"] + 2 * d(bf["Tp"]) * bf["Pp"])          # per chi, outward +
    lam_ = np.stack([bf["Trr"], bf["Tp"]])
    lam_max, lam_negmax = lam_.max(), (-lam_).max()
    def ghost(chi):
        return bool(np.any(1.0 + chi * lam_ <= 0.0))
    chi_supp = -1.0 / lam_max            # support sign (chi<0)
    chi_anti = +1.0 / lam_negmax
    sgn = SIGN                           # MUTATE b: everything below that is 'the support sign' uses the reversed coupling
    chi_s = sgn * chi_supp               # strength at which the support-sign ghost boundary sits (physical run); reversed in MUTATE
    det_below = ghost(0.95 * chi_s); det_above = ghost(1.05 * chi_s)
    # sign of the force on the fluid for the coupling sign used
    force_dir = np.sign(np.median((chi_s * a_f / g_)[(r_ > 0.3 * hh) & (r_ < 5 * hh)]))
    fmax = np.abs(chi_s * a_f / g_)
    fm_peak = float(fmax[(r_ > 0.3 * hh) & (r_ < 5 * hh)].max())
    rows[f"{Mb:.0e}"] = dict(chi_crit_support=chi_supp, chi_crit_anti=chi_anti, ghost_below=det_below, ghost_above=det_above, force_dir=float(force_dir), fmax_peak=fm_peak,
                             fmax_at_h=float(fmax[int(np.argmin(abs(r_ - hh)))]))
    P(f"  M_b = {Mb:.0e}, h = {hh}: chi_crit(support, chi<0) = {chi_supp:.3e}; chi_crit(anti, chi>0) = {chi_anti:.3e} (x{chi_anti/abs(chi_supp):.0f});  coupling used: {'REVERSED' if MUTATE=='b' else 'support sign'} chi = {chi_s:.3e}: ghost at 0.95 chi: {det_below}, at 1.05 chi: {det_above};"
      f" force on fluid {'outward (support)' if force_dir>0 else 'INWARD (anti-support)'};  peak |a_f|/g_tot at the boundary strength = {fm_peak:.3f} (r in 0.3..5 h)")
R.num("W3_rows", rows)
ok3b = all((not v["ghost_below"]) and v["ghost_above"] for v in rows.values())              # detector controls (support sign)
ok3c = all(v["force_dir"] > 0 and v["fmax_peak"] < 1.0 for v in rows.values())            # the ghost-free support is < 1 and outward
check("W3b (numeric) ghost detector: exponential spheres, support-sign coupling: no ghost at 0.95 chi_crit, ghost at 1.05 chi_crit" + ("  [MUTATE b: coupling reversed]" if MUTATE == "b" else ""),
      f"{ {k: (v['ghost_below'], v['ghost_above']) for k, v in rows.items()} }", ok3b)
check("W3c (numeric) at the ghost boundary the coupling supplies an OUTWARD force of at most ~0.5 g_tot per unit fluid mass (peak over 0.3-5 h) -- less than the f = 1 needed to carry the closure" + ("  [MUTATE b: reversed sign -> inward force, x90 larger bound]" if MUTATE == "b" else ""),
      f"force direction sign and peak fraction: { {k: (v['force_dir'], round(v['fmax_peak'],3)) for k, v in rows.items()} }", ok3c)

# ------------------------------------------------------------------------------------------------ W4
R.banner("W4  FRW: the background tidal tensor of a uniform baryon density; inertia renormalisation; the finite-c multiplier pair")
xs = sp.symbols("x1 x2 x3", real=True); rbar = sp.Symbol("rhobar", positive=True); Gq = sp.Symbol("G", positive=True)
Phi_u = sp.Rational(2, 3) * sp.pi * Gq * rbar * sum(v**2 for v in xs)              # lap Phi = 4 pi G rhobar
lap_u = sum(sp.diff(Phi_u, v, 2) for v in xs)
Tu = sp.Matrix(3, 3, lambda i, j: (lap_u if i == j else 0) - sp.diff(Phi_u, xs[i], xs[j]))
P(f"    uniform density: lap Phi_b = {sp.simplify(lap_u)};  T_ij = {sp.simplify(Tu[0,0])} delta_ij  (= (8 pi G rho_b/3) delta_ij = Omega_b H^2 delta_ij for a flat matter-dominated background)")
okT = sp.simplify(Tu[0, 0] - 8 * sp.pi * Gq * rbar / 3) == 0 and Tu[0, 1] == 0
# growth with time-dependent inertia m(t): d(m xdot)/dt = -grad Phi  -> delta'' + (2H + m'/m) delta' = 4 pi G rho delta / m   (sympy check of the perturbation algebra)
tt = sp.symbols("t"); at = sp.Function("a")(tt); mt = sp.Function("m")(tt); q = sp.Function("q")(tt); dF = sp.Function("dPhiGrad")(tt)
xq = at * q
eq_m = sp.diff(mt * sp.diff(xq, tt), tt)
eq_bg = sp.diff(mt * sp.diff(at, tt), tt)                                          # background (q const)
pert = sp.simplify(sp.expand(eq_m - sp.diff(mt * sp.diff(at, tt), tt) * q))
pert_ref = sp.simplify(at * mt * sp.diff(q, tt, 2) + (2 * mt * sp.diff(at, tt) + sp.diff(mt, tt) * at) * sp.diff(q, tt))
okG = sp.simplify(pert - pert_ref) == 0
P(f"    perturbation of d(m x_dot)/dt = -grad Phi about the background: a m q'' + (2 m a' + m' a) q' = -grad(delta Phi)  ->  delta'' + (2H + m'/m) delta' = 4 pi G rho delta/m   [sympy residual ok = {okG}]")
# numbers
H0 = 67.4e-3                                    # km/s/kpc
Omb = 0.02237 / 0.674**2
chis = {"M1e9 r=h": 1.0 / abs(rows["1e+09"]["fmax_at_h"] and 1) }   # placeholder overwritten below
# chi needed for f = 1 at r = h  from D1 numbers: chi_need = g/|a_f| at r = h
need = {}
for Mb, hh in ((1e9, 2.0), (1e10, 3.0), (1e11, 4.0), (1e12, 5.0)):
    prof = exp_sphere(Mb, hh); bf = baryon_fields(prof, r0=1e-2 * hh, r1=30 * hh, n=6001)
    r_ = bf["r"]; d = lambda yv: np.gradient(yv, r_)
    a_f = (0.5 / bf["rho"]) * (d(bf["Trr"]) * bf["Prr"] + 2 * d(bf["Tp"]) * bf["Pp"])
    i = int(np.argmin(abs(r_ - hh)))
    need[Mb] = bf["g"][i] / abs(a_f[i])
    P(f"    M_b = {Mb:.0e}: chi needed for f = 1 at r = h : {need[Mb]:.3e} kpc^2/(km/s)^2  (galaxy-dependent: spread over the four spheres x{max(need.values())/min(need.values()) if len(need)>1 else 1:.1f} so far)")
sp_need = max(need.values()) / min(need.values())
m0 = {Mb: need[Mb] * Omb * H0**2 for Mb in need}
m1100 = {Mb: v * 1101.0**3 for Mb, v in m0.items()}
P(f"    chi Omega_b H^2 today: {[f'{v:.1e}' for v in m0.values()]};   at z = 1100 (x (1+z)^3): {[f'{v:.1e}' for v in m1100.values()]}   -> m - 1 >> 1 at recombination unless Phi_b is built from the OVERDENSITY")
cpair = sp.Matrix([[0, sp.Symbol("D")], [sp.Symbol("D"), 0]])
detp = sp.simplify(cpair.det()); evp = cpair.eigenvals()
P(f"    (Phi_b, lambda) quadratic form [[0,D],[D,0]]: det = {detp}, eigenvalues {list(evp.keys())} (one negative): indefinite pair (dipole ghost with D = k^2 - omega^2/c^2); enslaved (no propagating dof) in the static Poisson limit; relativistic completion OPEN")
ok4 = okT and okG and min(m1100.values()) > 10.0 and sp_need > 10.0
check("W4 (sympy + numbers) the background tidal tensor of uniform density is Omega_b H^2 delta_ij (nonzero): the coupling renormalises the fluid inertia by m - 1 = chi Omega_b H^2 -- for the galaxy-scale chi it is >> 1 at z = 1100 (incompatible with GR+CDM at the CMB) unless Phi_b is built on the overdensity (postulated); the required chi also varies by > x10 across M_b = 1e9..1e12 (not universal)",
      f"T_ii uniform ok {okT}; growth algebra ok {okG}; chi_need spread x{sp_need:.0f}; m(1100) - 1 in {min(m1100.values()):.0e}..{max(m1100.values()):.0e}", ok4)

nf = R.write()
sys.exit(1 if nf else 0)
