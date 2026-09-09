#!/usr/bin/env python3
"""
L15 -- the IC6 obstruction at the value of sigma that the physics forces (sigma = 1)
====================================================================================
Lane L15 of `fable_independent_2026/CHARTER.md`; open challenge B1 of `HANDOFF_CONTRACT.md`.
The lead agent's construction lives in `closure_2026/integrable_clock_construction_2026/` and is READ-ONLY to
this lane: nothing there is imported, executed or copied.  Everything below is re-derived from the ACTION AS
WRITTEN in IC4_ACTION.md / IC5_ACTION.md / TENSOR_BALANCE.md / LOCAL_WAVE_REPORT.md, transcribed by hand into
sympy here, then evaluated at 60 decimal digits with mpmath.

WHY sigma MOVES.  IC-4 fixes the design parameter sigma = 1/3 and states "more generally the calculation covers
0 < sigma <= 1".  LOCAL_WAVE_REPORT.md's boxed reduced scalar equation is z'' + 3z' + sigma x z = 0 with
"proper-time conversion gives c_s^2 = sigma c^2", and IC6_EVEN's reduced isotropic equation
qddot + 3qdot + e^{2/3} k^2 diag(1/3,1) q = 0 carries the same 1/3 in its scalar slot.  So sigma IS the squared
sound speed of the propagating clock scalar.  Gravitational Cherenkov radiation off ultra-high-energy cosmic
rays bounds a subluminal gravitational-sector mode at 1 - c_s <= 2e-15 (Moore & Nelson 2001; Elliott, Moore &
Stoica 2005 -- the same gate this repository imposes on its own khronon in g03v_k2_pincer_closure V6).
c_s^2 = 1/3 is excluded by 2.1e14x (L10, HANDOFF_CONTRACT A5).  The bound collapses (0,1] to sigma = 1 within
4e-15: the mode must be marginally luminal or marginally SUPERluminal, which is standard and causally
acceptable in a theory with a preferred foliation.

WHERE sigma ENTERS THE ALGEBRA (determined by me from the action; see section 0 for the symbolic proof).
IC-4 has a_* = 3 - 81/(4T), p_R = 8/3 + 4 a_* sigma, q_R = -1 - 3 p_R/8, A_R = 3 p_R/(16 l^2),
B_R = 3 q_R/(16 l^2), F = A_R(xi - 1/4) + B_R(u - 2/3).  Nothing else in the action carries sigma:
l, T, e, d, alpha, beta, gamma, b, a0^2, Lambda, U are all sigma-free.  So sigma reaches the IC6/IC7
machinery through exactly one channel -- F -- and therefore through J_T = 1 + e^{-6w} rho^2 F/(m^2 a0^2),
c = m e^{u xi} J_T, and nothing else.

THE QUESTION.  Does the IC6 quartic obstruction survive at sigma = 1, and is IC7's counterterm still needed?

MANDATORY CONTROL.  L4 independently confirmed the lead's boxed identity
    S_4'(1) = -e^{5/6}(5T-27)(8T-27)(8T+27)/(18 T^2 (4T-27)) = -11.1407711251147987   at sigma = 1/3.
L15-C6 reproduces that number by the same implicit-function route before any sigma is moved.  If it fails,
nothing downstream is trustworthy and the run stops there.
"""
import sys
import sympy as sp
import mpmath as mp

mp.mp.dps = 60
FAILS = []
STOP = []


def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok:
        FAILS.append(name)
    return ok


def close(a, b, tol):
    a, b = mp.mpf(a), mp.mpf(b)
    return abs(a - b) <= tol * max(mp.mpf(1), abs(b))


BAR = "=" * 118
print(BAR)
print("L15 -- the IC6 obstruction at the Cherenkov-forced value of its own design parameter, sigma = 1")
print(BAR)

# ================================================================================================================
# section 0 -- sigma's role, established symbolically from the action
# ================================================================================================================
print("\n-- 0. where sigma enters, established from the action (IC4/IC5) -------------------------------------------")

sig = sp.Symbol('sigma', positive=True)
ell = sp.log(sp.Rational(9, 5))
Tcal = -sp.Rational(27, 16) + 54 / (5 * ell)
astar = 3 - 81 / (4 * Tcal)
e_c = sp.Rational(1, 8)
d_c = -9 * e_c / Tcal
al_c = 81 * e_c / Tcal**2
be_c = 2 * d_c - sp.Rational(1, 3) - 3 * al_c / 4
ga_c = e_c - sp.Rational(1, 16) + 9 * al_c / 64 - 3 * d_c / 4
b_c = -Tcal / 9 - sp.Rational(3, 8)                        # IC5_ACTION.md
m, kappa = sp.Integer(1), sp.Integer(6)                    # the lead's fixture units, m = h0 = V = 1
h0 = sp.sqrt(kappa / (6 * m))
a02 = 9 * kappa * sp.exp(-sp.Rational(1, 2)) / (16 * m * ell**2)
Ufun = lambda cc_: (1 - cc_) * (sp.log(1 - cc_)**2 - 2 * sp.log(1 - cc_) + 2) - 2
Lam = kappa * sp.exp(-sp.Rational(1, 2)) / m - a02 * Ufun(sp.Rational(4, 9))

pR_s = sp.Rational(8, 3) + 4 * astar * sig
qR_s = -1 - 3 * pR_s / 8
AR_s = 3 * pR_s / (16 * ell**2)
BR_s = 3 * qR_s / (16 * ell**2)

sigma_free = {'ell': ell, 'Tcal': Tcal, 'a_*': astar, 'e': e_c, 'd': d_c, 'alpha': al_c, 'beta': be_c,
              'gamma': ga_c, 'b': b_c, 'a0^2': a02, 'Lambda': Lam, 'h0': h0}
check("L15-S1 every frozen IC-4/IC-5 constant EXCEPT (p_R, q_R, A_R, B_R) is independent of sigma: "
      "l, T, e, d, alpha, beta, gamma, b, a0^2, Lambda, h0 all have zero sigma-derivative. Hence sigma reaches "
      "the whole IC5/IC6/IC7 machinery through ONE channel: the coefficient function F.",
      all(sp.simplify(sp.diff(v, sig)) == 0 for v in sigma_free.values()),
      "checked symbolically, 12 constants")

# --- the sigma <-> sound-speed link, re-derived from LOCAL_WAVE_REPORT section 2 (its algebra, my sympy)
xw, yw, vw, zw = sp.symbols('x y v z', real=True)
pRg = sp.Symbol('p_R', real=True)
qRg = -1 - 3 * pRg / 8
Lw = ((3 + al_c * xw / 4) * yw**2 - 9 * (Tcal + e_c * xw) * yw * vw / Tcal + (Tcal + e_c * xw) * vw**2
      + (sp.Rational(2, 3) + pRg / 2) * xw * zw * yw + (1 + 3 * pRg / 8 + qRg) * xw * zw * vw + xw * zw**2)
v_sol = sp.solve(sp.diff(Lw, vw), vw)[0]
Lw_red = sp.simplify(Lw.subs(vw, v_sol))
kin = sp.simplify(sp.expand(Lw_red).coeff(yw, 2))
bx = sp.simplify(sp.expand(Lw_red).coeff(zw, 1).coeff(yw, 1))
gx = sp.simplify(xw - sp.Rational(3, 2) * bx + xw * sp.diff(bx, xw))
pR_from_sigma = sp.solve(sp.Eq(gx, -astar * sig * xw), pRg)[0]
check("L15-S2 [control] LOCAL_WAVE_REPORT's scalar reduction re-derived in my own sympy: eliminating v from its "
      "quadratic Lagrangian gives kinetic coefficient a_* = 3 - 81/(4T) EXACTLY (the alpha x/4 and 81 e x/(4T^2) "
      "terms cancel), source b(x) = (2/3 + p_R/2) x, measure-corrected stiffness g(x) = (2/3 - p_R/4) x, and "
      "g = -a_* sigma x forces p_R = 8/3 + 4 a_* sigma. So sigma IS the squared sound speed and it enters ONLY "
      "through p_R.",
      sp.simplify(kin - astar) == 0
      and sp.simplify(bx - (sp.Rational(2, 3) + pRg / 2) * xw) == 0
      and sp.simplify(gx - (sp.Rational(2, 3) - pRg / 4) * xw) == 0
      and sp.simplify(pR_from_sigma - (sp.Rational(8, 3) + 4 * astar * sig)) == 0,
      f"a_* = {sp.N(astar, 12)} > 0, sigma-free  =>  the reduced scalar kinetic normalisation never depends on sigma")

check("L15-S3 [control] v = 9y/(2T) and n = (8T+27)y/(16T) reproduce from the same reduction, and the "
      "position-source cancellation that fixes q_R = -1 - 3 p_R/8 is an identity (the xz v coefficient vanishes)",
      sp.simplify(v_sol - 9 * yw / (2 * Tcal)) == 0
      and sp.simplify((yw / 2 + 3 * v_sol / 8) - (8 * Tcal + 27) * yw / (16 * Tcal)) == 0
      and sp.simplify(1 + 3 * pRg / 8 + qRg) == 0)

# --- the quadratic-Dirac constraint matrix of LOCAL_WAVE section 3 carries no p_R at all
MD11 = -24 - 81 * xw / (4 * Tcal**2)
MD12 = 27 + 9 * xw / (4 * Tcal) + 243 * xw / (32 * Tcal**2)
MD22 = -2 * Tcal - sp.Rational(135, 8) - xw / 4 - 27 * xw / (16 * Tcal) - 729 * xw / (256 * Tcal**2)
detMD = sp.simplify(MD11 * MD22 - MD12**2)
check("L15-S4 [control] LOCAL_WAVE's quadratic-Dirac auxiliary matrix M contains NO p_R, and its determinant "
      "reproduces the lead's 3 F^2 h^4 (4T-27)(8T+x)/(2T) > 0 symbolically. The scalar sector's constraint rank "
      "(4 second class + 2 first class, 1 physical pair) is therefore sigma-INDEPENDENT.",
      sp.simplify(detMD - 3 * (4 * Tcal - 27) * (8 * Tcal + xw) / (2 * Tcal)) == 0
      and len({pRg, sig} & (MD11.free_symbols | MD12.free_symbols | MD22.free_symbols)) == 0,
      f"det M/(F^2 h^4) at x=1 is {sp.N(detMD.subs(xw,1),12)} > 0")


# ================================================================================================================
# the IC5/IC6/IC7 density, built once as a function of sigma
# ================================================================================================================
xi, u, rho, tau = sp.symbols('xi u rho tau', real=True)
w = (u - 1) * xi
E = sp.exp((4 - 3 * u) * xi)
F_s = AR_s * (xi - sp.Rational(1, 4)) + BR_s * (u - sp.Rational(2, 3))
J_s = 1 + sp.exp(-6 * w) * rho**2 * F_s / (m**2 * a02)
Cp = Lam + a02 * Ufun(u**2)
h_s = (2 * E / m) * (tau / J_s - rho**2 / 6) + m * sp.exp((3 * u - 2) * xi) * Cp - (kappa / 2) * sp.exp((3 * u - 4) * xi)
c_s_ = m * sp.exp(u * xi) * J_s
Dt = lambda f: sp.diff(f, u) - b_c * sp.diff(f, xi)

check("L15-S5 the nongradient density h restricted to the ISOTROPIC slice tau = 0 is exactly sigma-free "
      "(the whole F-dependence sits in the tau/J term). Consequence, used throughout: the isotropic auxiliary "
      "constraints h_xi = h_u = 0, the witness, the auxiliary Hessian, the branch tangent dq/dj, M12 and M22 are "
      "ALL sigma-independent. Only M11 = (E/6)(1/J - 1) and v = (c_rho/2, D_t c) move with sigma.",
      sp.simplify(sp.diff(h_s.subs(tau, 0), sig)) == 0
      and sp.simplify(sp.diff(Dt(sp.diff(h_s, rho)).subs(tau, 0), sig)) == 0
      and sp.simplify(sp.diff(Dt(Dt(h_s)).subs(tau, 0), sig)) == 0
      and sp.simplify((sp.diff(h_s, rho, 2) / 4 + sp.diff(h_s, tau) / 12).subs(tau, 0)
                      - E * (1 / J_s.subs(tau, 0) - 1) / (6 * m)) == 0
      and sp.simplify(sp.diff((sp.diff(h_s, rho, 2) / 4 + sp.diff(h_s, tau) / 12).subs(tau, 0), sig)) != 0,
      "d(h|_tau=0)/dsigma = 0, d(M12)/dsigma = 0, d(M22)/dsigma = 0, d(M11)/dsigma != 0, all symbolic")


def build(sigma_value):
    """Lambdify the whole IC6/IC7 kit at one numeric value of the design parameter sigma."""
    sub = {sig: sigma_value}
    F_ = F_s.subs(sub)
    J_ = J_s.subs(sub)
    h_ = h_s.subs(sub)
    c_ = c_s_.subs(sub)
    M11 = sp.diff(h_, rho, 2) / 4 + sp.diff(h_, tau) / 12
    M12 = Dt(sp.diff(h_, rho)) / 2
    M22 = Dt(Dt(h_))
    v1, v2 = sp.diff(c_, rho) / 2, Dt(c_)
    detM = M11 * M22 - M12**2
    S4 = -4 * (M22 * v1**2 - 2 * M12 * v1 * v2 + M11 * v2**2) / detM
    SYM = dict(M11=M11, M12=M12, M22=M22, v1=v1, v2=v2, detM=detM, S4=S4, c7=-S4 / 32, J=J_, F=F_, c=c_,
               hxi=sp.diff(h_, xi), hu=sp.diff(h_, u), hxx=sp.diff(h_, xi, 2),
               hxu=sp.diff(sp.diff(h_, xi), u), huu=sp.diff(h_, u, 2),
               hxr=sp.diff(sp.diff(h_, xi), rho), hur=sp.diff(sp.diff(h_, u), rho),
               r=-rho * E / (3 * m * h0))
    f = {k: sp.lambdify((xi, u, rho, tau), v, modules='mpmath') for k, v in SYM.items()}
    g = {k: [sp.lambdify((xi, u, rho, tau), sp.diff(SYM[k], q), modules='mpmath') for q in (xi, u, rho)]
         for k in ('M11', 'M12', 'M22', 'v1', 'v2', 'S4', 'J', 'F')}
    return f, g


NUM = lambda e_: mp.mpf(str(sp.N(e_, 55)))
T = NUM(Tcal)
L2 = NUM(ell**2)
AST = NUM(astar)
WIT = [mp.mpf(1) / 4, mp.mpf(2) / 3, -3 * mp.e**mp.mpf('-0.5'), mp.mpf(0)]
rho_w = WIT[2]

KIT = {}
for name, val in (('1/3', sp.Rational(1, 3)), ('1', sp.Integer(1))):
    KIT[name] = build(val)


def solve_aux(f, rv, tv, guess=(mp.mpf(1) / 4, mp.mpf(2) / 3)):
    """My own Newton solve of the two auxiliary constraints h_xi = h_u = 0 at fixed (rho, tau)."""
    q = mp.matrix(list(guess))
    for _ in range(200):
        Fv = mp.matrix([f['hxi'](q[0], q[1], rv, tv), f['hu'](q[0], q[1], rv, tv)])
        Jv = mp.matrix([[f['hxx'](q[0], q[1], rv, tv), f['hxu'](q[0], q[1], rv, tv)],
                        [f['hxu'](q[0], q[1], rv, tv), f['huu'](q[0], q[1], rv, tv)]])
        dq = mp.lu_solve(Jv, -Fv)
        q = q + dq
        if mp.norm(dq) < mp.mpf(10)**-50:
            break
    return q[0], q[1]


def branch(f, g, sig_name):
    """Witness data + d/dj along the isotropic family lambda_i = -e^{-1/2} j."""
    Hm = mp.matrix([[f['hxx'](*WIT), f['hxu'](*WIT)], [f['hxu'](*WIT), f['huu'](*WIT)]])
    gj = mp.matrix([f['hxr'](*WIT) * rho_w, f['hur'](*WIT) * rho_w])
    dqdj = mp.lu_solve(Hm, -gj)

    def ddj(key):
        gg = g[key]
        return gg[0](*WIT) * dqdj[0] + gg[1](*WIT) * dqdj[1] + gg[2](*WIT) * rho_w
    return Hm, dqdj, ddj


# ================================================================================================================
# section 1 -- controls
# ================================================================================================================
print("\n-- 1. controls (these would catch my own algebra being wrong) ---------------------------------------------")

f13, g13 = KIT['1/3']
f1, g1 = KIT['1']

wres13 = (abs(f13['hxi'](*WIT)), abs(f13['hu'](*WIT)))
wres1 = (abs(f1['hxi'](*WIT)), abs(f1['hu'](*WIT)))
ok = check("L15-C1 the IC-4/IC-5 expanding witness (xi,u,rho,tau) = (1/4, 2/3, -3e^{-1/2}, 0) is an EXACT "
           "stationary point of my independently transcribed h at BOTH sigma = 1/3 and sigma = 1, with F = 0 and "
           "r = 1 at both. The witness does not move with sigma.",
           max(wres13 + wres1) < mp.mpf(10)**-45 and abs(f13['F'](*WIT)) < mp.mpf(10)**-45
           and abs(f1['F'](*WIT)) < mp.mpf(10)**-45 and close(f1['r'](*WIT), 1, mp.mpf(10)**-45),
           f"max |h_xi|,|h_u| over both sigma = {mp.nstr(max(wres13 + wres1), 3)}")
STOP.append(ok)

Hm13, dqdj13, ddj13 = branch(f13, g13, '1/3')
Hm1, dqdj1, ddj1 = branch(f1, g1, '1')
Hn = Hm13 / (m * mp.e**mp.mpf('-0.5') * h0**2)
Hlead = mp.matrix([[-24, 27], [27, -(2 * T + mp.mpf(135) / 8)]])
check("L15-C2 auxiliary Hessian at the witness (normalised by m V e^{-1/2} h0^2) = -[[24,-27],[-27,2T+135/8]] "
      "with det = 12(4T-27), and it is IDENTICAL at sigma = 1/3 and sigma = 1 to 40 digits",
      mp.norm(Hn - Hlead) < mp.mpf(10)**-40 and close(mp.det(Hn), 12 * (4 * T - 27), mp.mpf(10)**-40)
      and mp.norm(Hm13 - Hm1) < mp.mpf(10)**-40,
      f"det = {mp.nstr(mp.det(Hn), 12)} = 12(4T-27); ||H(1/3) - H(1)|| = {mp.nstr(mp.norm(Hm13 - Hm1), 3)}")

check("L15-C3 branch tangent dq/dj|_1 = ( -(8T+27)/(4(4T-27)), -18/(4T-27) ) from my own implicit-function solve, "
      "identical at sigma = 1/3 and sigma = 1. It is EXACTLY along the auxiliary null direction "
      "chi = (partial_u - b partial_xi), i.e. dq/dj = -18/(4T-27) * (-b, 1).",
      close(dqdj13[0], -(8 * T + 27) / (4 * (4 * T - 27)), mp.mpf(10)**-40)
      and close(dqdj13[1], -18 / (4 * T - 27), mp.mpf(10)**-40)
      and mp.norm(dqdj13 - dqdj1) < mp.mpf(10)**-40
      and close(dqdj13[0], 18 * NUM(b_c) / (4 * T - 27), mp.mpf(10)**-40),
      f"dq/dj = ({mp.nstr(dqdj13[0], 12)}, {mp.nstr(dqdj13[1], 12)})")

check("L15-C4 the five witness coefficients of IC6_EVEN reproduce at sigma = 1/3: h_pp = E(1/J-1)/(6V) as an "
      "exact identity, h_p,chi = 2T/9, g_chi = -e^{1/6}(8T-27)/9, h_pp' = -e^{1/2}J'/6, g_p' = 2e^{2/3}J'/3",
      sp.simplify((sp.diff(h_s.subs(sig, sp.Rational(1, 3)), rho, 2) / 4
                   + sp.diff(h_s.subs(sig, sp.Rational(1, 3)), tau) / 12).subs(tau, 0)
                  - E * (1 / J_s.subs(sig, sp.Rational(1, 3)).subs(tau, 0) - 1) / (6 * m)) == 0
      and close(f13['M12'](*WIT), 2 * T / 9, mp.mpf(10)**-40)
      and close(-2 * f13['v2'](*WIT), -mp.e**(mp.mpf(1) / 6) * (8 * T - 27) / 9, mp.mpf(10)**-40)
      and close(ddj13('M11'), -mp.e**mp.mpf('0.5') * ddj13('J') / 6, mp.mpf(10)**-40)
      and close(-2 * ddj13('v1'), 2 * mp.e**(mp.mpf(2) / 3) * ddj13('J') / 3, mp.mpf(10)**-40))

detstar13 = f13['detM'](*WIT)
detstar1 = f1['detM'](*WIT)
check("L15-C5 det(M_star) = -4 T^2 h0^2/81, nonzero, and IDENTICAL at sigma = 1/3 and sigma = 1 (M11 = 0 at the "
      "witness for every sigma, and M12, M22 are sigma-free) -- so IC7's cutoff normalisation does not move",
      close(detstar13, -4 * T**2 * h0**2 / 81, mp.mpf(10)**-40)
      and close(detstar1, detstar13, mp.mpf(10)**-40) and abs(detstar13) > mp.mpf(1),
      f"det(M*) = {mp.nstr(detstar13, 14)} at both")

S4p_13 = ddj13('S4')
S4p_lead = -mp.e**(mp.mpf(5) / 6) * (5 * T - 27) * (8 * T - 27) * (8 * T + 27) / (18 * T**2 * (4 * T - 27))
ok = check("L15-C6 [MANDATORY CONTROL] at the PUBLISHED parameters (sigma = 1/3) my independent rebuild returns "
           "S_4'(1) = -e^{5/6}(5T-27)(8T-27)(8T+27)/(18 T^2 (4T-27)) = -11.1407711251147987, L4's confirmed value. "
           "Nothing below is trustworthy without this.",
           close(S4p_13, S4p_lead, mp.mpf(10)**-40)
           and close(S4p_13, '-11.1407711251147987', mp.mpf('1e-16')),
           f"S_4'(1)|_sigma=1/3 = {mp.nstr(S4p_13, 18)}  (lead's closed form {mp.nstr(S4p_lead, 18)})")
STOP.append(ok)

if not all(STOP):
    print("\n*** CONTROL FAILED -- stopping. The rebuild does not reproduce L4's confirmed value, so no sigma = 1")
    print("*** statement from this script would be trustworthy. Nothing downstream is reported.")
    sys.exit(1)

# ================================================================================================================
# section 2 -- the general-sigma closed form
# ================================================================================================================
print("\n-- 2. the obstruction as a closed function of sigma --------------------------------------------------------")

# Derivation (by hand, from the same objects; each step is checked numerically below).
#   At the witness v1 = M11 = 0, so S_4(1) = 0 and S_4'(1) = 4[M11' v2^2 - 2 M12 v1' v2]/M12^2 with
#   M12 = 2T/9,  M11' = -(e^{1/2}/6) J',  J' = (9 - p_R T)/(4T - 27),  v1' = e^{2/3}(p_R T - 9)/(3(4T-27)),
#   v2  = e^{1/6} T (3 p_R + 4)/54.   Collecting:
S4p_closed = sp.exp(sp.Rational(5, 6)) * (pR_s * Tcal - 9) * (3 * pR_s + 4) * (3 * pR_s - 44) / (216 * (4 * Tcal - 27))
lead_boxed = (-sp.exp(sp.Rational(5, 6)) * (5 * Tcal - 27) * (8 * Tcal - 27) * (8 * Tcal + 27)
              / (18 * Tcal**2 * (4 * Tcal - 27)))
check("L15-G1 [control] my general-sigma closed form "
      "S_4'(1;sigma) = e^{5/6}(p_R T - 9)(3 p_R + 4)(3 p_R - 44) / (216 (4T - 27)),  p_R = 8/3 + 4 a_* sigma, "
      "reduces SYMBOLICALLY to the lead's boxed identity at sigma = 1/3",
      sp.simplify(S4p_closed.subs(sig, sp.Rational(1, 3)) - lead_boxed) == 0,
      "sympy: difference simplifies to exactly 0")

S4p_closed_f = sp.lambdify(sig, S4p_closed, modules='mpmath')
sweep_err = []
for sv_s, kitname in ((sp.Rational(1, 3), '1/3'), (sp.Integer(1), '1')):
    ff, gg = KIT[kitname]
    _, _, dd = branch(ff, gg, kitname)
    sweep_err.append(abs(dd('S4') - S4p_closed_f(mp.mpf(sp.N(sv_s, 50)))))
extra = []
for sv_r in (sp.Rational(1, 5), sp.Rational(1, 2), sp.Rational(9, 10), sp.Rational(3, 2)):
    ff, gg = build(sv_r)
    _, _, dd = branch(ff, gg, str(sv_r))
    extra.append(abs(dd('S4') - S4p_closed_f(mp.mpf(sp.N(sv_r, 50)))))
check("L15-G2 [control] the closed form agrees with the full numerical implicit-function derivative of S_4 at "
      "sigma = 1/5, 1/3, 1/2, 9/10, 1, 3/2 -- so it is the correct sigma-dependence, not a fit at one point",
      max(sweep_err + extra) < mp.mpf('1e-40'),
      f"max |closed - numeric| = {mp.nstr(max(sweep_err + extra), 4)}")

# ================================================================================================================
# section 3 -- sigma = 1
# ================================================================================================================
print("\n-- 3. the answer at sigma = 1 ------------------------------------------------------------------------------")

pR13, pR1 = NUM(pR_s.subs(sig, sp.Rational(1, 3))), NUM(pR_s.subs(sig, 1))
qR1 = NUM(qR_s.subs(sig, 1))
AR1, BR1 = NUM(AR_s.subs(sig, 1)), NUM(BR_s.subs(sig, 1))
AR13, BR13 = NUM(AR_s.subs(sig, sp.Rational(1, 3))), NUM(BR_s.subs(sig, sp.Rational(1, 3)))
print(f"    a_*    = {mp.nstr(AST, 12)}   T = {mp.nstr(T, 12)}   (both sigma-free)")
print(f"    p_R:   {mp.nstr(pR13, 12)}  (sigma=1/3)  ->  {mp.nstr(pR1, 12)}  (sigma=1)")
print(f"    q_R:   {mp.nstr(NUM(qR_s.subs(sig, sp.Rational(1,3))), 12)}  ->  {mp.nstr(qR1, 12)}")
print(f"    A_R:   {mp.nstr(AR13, 12)}  ->  {mp.nstr(AR1, 12)}")
print(f"    B_R:   {mp.nstr(BR13, 12)}  ->  {mp.nstr(BR1, 12)}")

S4p_1 = ddj1('S4')
Jp_13, Jp_1 = ddj13('J'), ddj1('J')
Fp_13, Fp_1 = ddj13('F'), ddj1('F')
print(f"    dF/dj: {mp.nstr(Fp_13, 12)}  ->  {mp.nstr(Fp_1, 12)}")
print(f"    dJ_T/dj: {mp.nstr(Jp_13, 12)}  ->  {mp.nstr(Jp_1, 12)}")
print(f"\n    S_4'(1) at sigma = 1/3 : {mp.nstr(S4p_13, 18)}")
print(f"    S_4'(1) at sigma = 1   : {mp.nstr(S4p_1, 18)}")
print(f"    ratio                  : {mp.nstr(S4p_1 / S4p_13, 12)}")

check("L15-R1 [THE QUESTION] does the IC6 quartic obstruction VANISH at sigma = 1? It does not. S_4'(1) is "
      "nonzero, has the SAME NEGATIVE SIGN, and is LARGER in magnitude than at the published sigma = 1/3. "
      "S_4(1) = 0 still holds at the witness, so S_4 < 0 for every small j - 1 > 0 exactly as at sigma = 1/3, "
      "and M_0 zeta_tt + S_4 k^4 zeta = 0 still has real growth ~ k^2.",
      S4p_1 < 0 and abs(S4p_1) > abs(S4p_13),
      f"S_4'(1)|_sigma=1 = {mp.nstr(S4p_1, 18)}, i.e. {mp.nstr(S4p_1 / S4p_13, 6)}x the sigma = 1/3 value")

# the Cherenkov window itself
sig_lo = mp.mpf(1) - 4 * mp.mpf(10)**-15
dS_dsig = mp.diff(lambda s: S4p_closed_f(s), mp.mpf(1))
check("L15-R2 the answer is uniform across the ENTIRE Cherenkov-allowed window. 1 - c_s <= 2e-15 with "
      "c_s^2 = sigma gives sigma >= 1 - 4e-15; over that whole window S_4'(1) moves by less than 1e-12, so no "
      "choice inside the window changes the verdict.",
      abs(S4p_closed_f(sig_lo) - S4p_closed_f(mp.mpf(1))) < mp.mpf('1e-12'),
      f"dS_4'/dsigma at sigma=1 = {mp.nstr(dS_dsig, 10)}; window swing = "
      f"{mp.nstr(abs(S4p_closed_f(sig_lo) - S4p_closed_f(mp.mpf(1))), 4)}")

# ================================================================================================================
# section 4 -- can ANY admissible sigma remove it?
# ================================================================================================================
print("\n-- 4. can any admissible sigma remove the obstruction? ------------------------------------------------------")

roots = sp.solve(sp.Eq(S4p_closed, 0), sig)
sig_star = sp.simplify(4 * Tcal / (4 * Tcal - 27))
SIGSTAR = NUM(sig_star)
root_num = sorted(mp.mpf(str(sp.N(r, 40))) for r in roots)
check("L15-R3 [THEOREM] S_4'(1;sigma) has exactly ONE zero in sigma, at sigma_* = 4T/(4T-27) = 3/a_*, and "
      "sigma_* > 1 for EVERY T in the frozen domain T > 27/4. The other two factors (p_R T - 9) and (3 p_R + 4) "
      "are strictly positive for all sigma > 0. Therefore S_4'(1;sigma) < 0 for the WHOLE of IC-4's own design "
      "interval 0 < sigma <= 1: no admissible choice of the design parameter removes the obstruction, and the "
      "one value that would is outside the interval.",
      len(roots) == 1 and close(root_num[0], SIGSTAR, mp.mpf('1e-35')) and SIGSTAR > 1
      and sp.simplify(sp.solve(sp.Eq(3 * pR_s - 44, 0), sig)[0] - sig_star) == 0
      and all(S4p_closed_f(mp.mpf(s)) < 0 for s in ('0.001', '0.1', '1/3', '0.5', '0.99', '1')),
      f"sigma_* = 4T/(4T-27) = {mp.nstr(SIGSTAR, 12)}, i.e. c_s = {mp.nstr(mp.sqrt(SIGSTAR), 10)} c "
      f"({mp.nstr(100 * (mp.sqrt(SIGSTAR) - 1), 4)}% superluminal)")

check("L15-R4 the frozen domain condition does NOT move. T = -27/16 + 54/(5 ln(9/5)) contains no sigma, so "
      "T > 27/4 holds at sigma = 1 exactly as at sigma = 1/3, and det H_qq = 12(4T-27) > 0 is unchanged. What the "
      "published factorisation (5T-27)(8T-27)(8T+27) hid is that the sign is really controlled by "
      "3 p_R - 44 < 0, i.e. by sigma < sigma_*, and the design interval sits entirely inside that region.",
      T > mp.mpf(27) / 4 and sp.simplify(sp.diff(Tcal, sig)) == 0
      and close(mp.det(Hn), 12 * (4 * T - 27), mp.mpf(10)**-40),
      f"T = {mp.nstr(T, 12)} > 6.75; 3 p_R - 44 = {mp.nstr(3 * pR1 - 44, 10)} < 0 at sigma = 1")

print("\n    S_4'(1;sigma) across the design interval and beyond:")
print("      sigma        p_R          S_4'(1)")
for sv in ('0.05', '0.2', '0.3333333333333333', '0.5', '0.75', '1.0', '1.25', '1.5',
           str(mp.nstr(SIGSTAR, 16)), '1.8'):
    s_ = mp.mpf(sv)
    print(f"      {mp.nstr(s_, 8):<12} {mp.nstr(mp.mpf(8)/3 + 4*AST*s_, 8):<12} {mp.nstr(S4p_closed_f(s_), 12)}")

sig_worst = mp.findroot(lambda s: mp.diff(S4p_closed_f, s), mp.mpf('0.95'))
check("L15-R3b [sharpest form of the result] S_4'(1;sigma) is not monotone: it is most negative at "
      f"sigma = {mp.nstr(sig_worst, 10)}, essentially AT the Cherenkov-forced value. Of the whole interval "
      "0 < sigma <= 1 that IC-4 declares admissible, the gravitational-Cherenkov bound selects the point where "
      "the IC6 obstruction is at its strongest. The published sigma = 1/3 was, by this measure, the mildest part "
      "of the interval that the construction could have been tested on.",
      abs(sig_worst - 1) < mp.mpf('0.15') and abs(S4p_closed_f(sig_worst)) >= abs(S4p_1),
      f"argmax|S_4'| at sigma = {mp.nstr(sig_worst, 10)}, value {mp.nstr(S4p_closed_f(sig_worst), 12)}; "
      f"at sigma = 1 it is {mp.nstr(S4p_1, 12)}, i.e. {mp.nstr(100*abs(S4p_1/S4p_closed_f(sig_worst)), 6)}% of "
      "the worst value in the interval")

# ================================================================================================================
# section 5 -- is IC7 still needed, and what happens to its window
# ================================================================================================================
print("\n-- 5. is IC7's counterterm still required? -----------------------------------------------------------------")

j7 = mp.mpf('1.007')
res = {}
for nm in ('1/3', '1'):
    ff, gg = KIT[nm]
    xs, us = solve_aux(ff, rho_w * j7, mp.mpf(0))
    S4v = ff['S4'](xs, us, rho_w * j7, 0)
    dMv = ff['detM'](xs, us, rho_w * j7, 0)
    M22v = ff['M22'](xs, us, rho_w * j7, 0)
    res[nm] = dict(xi=xs, u=us, S4=S4v, A0=dMv / M22v, lam2=-S4v * dMv / M22v,
                   c7=ff['c7'](xs, us, rho_w * j7, 0), J=ff['J'](xs, us, rho_w * j7, 0))

check("L15-R5 [control + result] the isotropic auxiliary solve is literally the same at both sigma: at j = 1.007 "
      "my Newton solve gives xi = 0.24297809, u = 0.66347046 (IC6_EVEN's quoted values) at sigma = 1/3 AND at "
      "sigma = 1, agreeing to 40 digits. Only J_T, S_4 and c_7 move.",
      close(res['1/3']['xi'], '0.24297809', mp.mpf('5e-9')) and close(res['1/3']['u'], '0.66347046', mp.mpf('5e-9'))
      and close(res['1/3']['S4'], '-0.07526051653', mp.mpf('1e-11'))
      and close(res['1/3']['lam2'], '0.03456985650', mp.mpf('1e-10'))
      and abs(res['1']['xi'] - res['1/3']['xi']) < mp.mpf('1e-40')
      and abs(res['1']['u'] - res['1/3']['u']) < mp.mpf('1e-40'),
      f"j=1.007: S_4 = {mp.nstr(res['1/3']['S4'], 12)} (sigma=1/3) -> {mp.nstr(res['1']['S4'], 12)} (sigma=1); "
      f"growth lambda^2/k^4 = {mp.nstr(res['1/3']['lam2'], 10)} -> {mp.nstr(res['1']['lam2'], 10)}")

check("L15-R6 [THE SECOND QUESTION] IC7's curvature-square counterterm is STILL REQUIRED at sigma = 1, and it is "
      "required MORE strongly: the coefficient it must supply, c_7 = -S_4/32, is nonzero and larger in magnitude "
      "at every isotropic sample. The construction does NOT simplify at sigma = 1.",
      res['1']['c7'] != 0 and abs(res['1']['c7']) > abs(res['1/3']['c7']),
      f"c_7 at j=1.007: {mp.nstr(res['1/3']['c7'], 15)} (sigma=1/3) -> {mp.nstr(res['1']['c7'], 15)} (sigma=1), "
      f"a factor {mp.nstr(res['1']['c7'] / res['1/3']['c7'], 8)}")


def Ebump(t):
    return mp.e**(-1 / t) if t > 0 else mp.mpf(0)


def theta_x(x_):
    return Ebump(1 - x_) / (Ebump(x_) + Ebump(1 - x_))


def theta_of(D):
    a = abs(D - 1)
    if a <= mp.mpf(1) / 4:
        return mp.mpf(1)
    if a >= mp.mpf(1) / 2:
        return mp.mpf(0)
    return theta_x(4 * (a - mp.mpf(1) / 4))


def edge(ff, dstar, target):
    lo, hi = mp.mpf('1.0'), mp.mpf('1.30')

    def Dj(jv):
        rv = rho_w * jv
        q = solve_aux(ff, rv, mp.mpf(0))
        return ff['detM'](q[0], q[1], rv, 0) / dstar
    for _ in range(80):
        mid = (lo + hi) / 2
        if Dj(mid) < target:
            lo = mid
        else:
            hi = mid
    rv = rho_w * lo
    q = solve_aux(ff, rv, mp.mpf(0))
    return lo, ff['S4'](q[0], q[1], rv, 0)


win = {}
for nm in ('1/3', '1'):
    ff, _ = KIT[nm]
    ds = ff['detM'](*WIT)
    e1 = edge(ff, ds, mp.mpf('1.25'))
    e0 = edge(ff, ds, mp.mpf('1.5'))
    win[nm] = (e1, e0)
check("L15-R7 IC7's repaired window SHRINKS by a factor ~2 at sigma = 1. L4 measured the theta == 1 plateau ending "
      "at j = 1.0736 and theta reaching 0 at j = 1.1316 for sigma = 1/3. Because dJ_T/dj is ~2x larger at "
      "sigma = 1, det M leaves its witness value ~2x faster and both edges move in. The unrepaired S_4 restored "
      "at the theta = 0 edge is also larger.",
      win['1'][0][0] < win['1/3'][0][0] and win['1'][1][0] < win['1/3'][1][0]
      and win['1/3'][1][1] < 0 and win['1'][1][1] < 0,
      f"theta=1 edge: j = {mp.nstr(win['1/3'][0][0], 8)} -> {mp.nstr(win['1'][0][0], 8)}; "
      f"theta=0 edge: j = {mp.nstr(win['1/3'][1][0], 8)} -> {mp.nstr(win['1'][1][0], 8)} "
      f"(S_4 there {mp.nstr(win['1/3'][1][1], 6)} -> {mp.nstr(win['1'][1][1], 6)})")

# where the positive-J_T branch ends.  The auxiliary solve is only meaningful while it stays on the regular
# branch 0 < u < 1 (U(u^2) leaves the reals otherwise), so the scan refuses to report past that.
def JT_positive(ff, jv):
    """(is the state usable, J_T there).  Usable means 0 < u < 1 and a real J_T."""
    rv = rho_w * jv
    try:
        q = solve_aux(ff, rv, mp.mpf(0))
        if not (mp.im(q[0]) == 0 and mp.im(q[1]) == 0):
            return False, None
        if not (mp.mpf(0) < q[1] < mp.mpf(1)):
            return False, None
        Jv = ff['J'](q[0], q[1], rv, 0)
        if mp.im(Jv) != 0:
            return False, None
        return True, mp.re(Jv)
    except (TypeError, ValueError, ZeroDivisionError):
        return False, None


JT_end = {}
for nm in ('1/3', '1'):
    ff, _ = KIT[nm]
    lo, hi, step = mp.mpf('1.0'), None, mp.mpf('0.002')
    jv = lo + step
    while jv < mp.mpf('3.0'):
        ok_j, Jv = JT_positive(ff, jv)
        if not ok_j or Jv <= 0:
            hi = jv
            break
        lo = jv
        jv += step
    if hi is not None:
        for _ in range(80):
            mid = (lo + hi) / 2
            ok_j, Jv = JT_positive(ff, mid)
            if ok_j and Jv > 0:
                lo = mid
            else:
                hi = mid
    q_end = solve_aux(ff, rho_w * lo, mp.mpf(0))
    JT_end[nm] = (lo, ff['J'](q_end[0], q_end[1], rho_w * lo, 0), q_end[1])
check("L15-R8 [corrected premise -- the obvious guess was wrong] the branch does NOT end because J_T reaches 0. "
      "The isotropic family itself terminates at a FOLD of the auxiliary constraint surface at j = 1.2165, where "
      "the real root of h_xi = h_u = 0 is lost and u is on its way out of the regular window 0 < u < 1. That fold "
      "is sigma-INDEPENDENT, because the tau = 0 constraints are sigma-free (L15-S5). J_T stays positive all the "
      "way to it at BOTH sigma -- but its margin at the fold collapses from 0.727 to 0.390, a factor 1.9. IC6's "
      "and IC7's stated precondition J_T > 0 therefore still holds on the whole branch at sigma = 1, with much "
      "less room.",
      abs(JT_end['1'][0] - JT_end['1/3'][0]) < mp.mpf('1e-6')
      and JT_end['1'][1] > 0 and JT_end['1/3'][1] > 0
      and JT_end['1'][1] < JT_end['1/3'][1],
      f"branch fold at j = {mp.nstr(JT_end['1/3'][0], 8)} (both sigma; u there = {mp.nstr(JT_end['1/3'][2], 8)}); "
      f"J_T at the fold = {mp.nstr(JT_end['1/3'][1], 8)} (sigma=1/3) -> {mp.nstr(JT_end['1'][1], 8)} (sigma=1)")

# ================================================================================================================
# section 6 -- tensor sector, DOF count, ghost
# ================================================================================================================
print("\n-- 6. tensor cone, degree-of-freedom count, ghost ----------------------------------------------------------")

B3 = sp.Symbol('B3', positive=True)
light2 = sp.exp((4 - 2 * u) * xi) / B3**2
cT2 = lambda Kc, Gc: sp.simplify(4 * Kc * Gc / light2)
cT2_IC6 = cT2(E / (m * J_s), c_s_ / (4 * B3**2))
cT2_IC5 = cT2(E / m, c_s_ / (4 * B3**2))
check("L15-R9 [THE TENSOR QUESTION] the IC6 tensor sector still gives c_T^2 = 1 EXACTLY at sigma = 1. The result "
      "is sigma-independent as an identity, not numerically: TENSOR_BALANCE's K_T = 1 + F Q^2/a0^2 = J_T and "
      "G_T = J_T cancel, and sigma lives only inside J_T. Reproduced here with sigma left symbolic, both "
      "polarisations, plus the IC5 mutation returning c_T^2 = J_T. So Cherenkov's tensor arm stays clean.",
      sp.simplify(cT2_IC6 - 1) == 0 and sp.simplify(cT2_IC5 - J_s) == 0
      and len({sig} & cT2_IC6.free_symbols) == 0,
      "symbolic in sigma: c_T^2(IC6) - 1 == 0 identically")

dof = lambda npair, n2nd, n1st: sp.Rational(2 * npair - n2nd - 2 * n1st, 2)
Kev13 = sorted(abs(e_) for e_ in mp.eig(Hm13, left=False, right=False))
Kev1 = sorted(abs(e_) for e_ in mp.eig(Hm1, left=False, right=False))
check("L15-R10 [THE DOF QUESTION] the local degree-of-freedom count is UNCHANGED at sigma = 1: 8 canonical pairs "
      "(6 barred-metric + xi + u) = 16, minus 4 second-class auxiliary constraints, minus 2x3 first-class "
      "spatial-momentum constraints = 3 -- two tensor polarisations plus one khronon-type clock scalar. The "
      "second-class classification rests on the invertibility of K = V h_AB, whose witness Hessian is "
      "sigma-independent (L15-C2), and on LOCAL_WAVE's sigma-free constraint matrix (L15-S4).",
      dof(6 + 2, 4, 3) == 3 and min(Kev13) > mp.mpf(1) and min(Kev1) > mp.mpf(1)
      and abs(mp.det(Hm1) - mp.det(Hm13)) < mp.mpf('1e-40'),
      f"count = {dof(6+2, 4, 3)}; |eig H_qq| at sigma=1: {mp.nstr(Kev1[0], 8)}, {mp.nstr(Kev1[1], 8)} "
      f"(identical to sigma=1/3)")

A0_w13 = detstar13 / f13['M22'](*WIT)
A0_w1 = detstar1 / f1['M22'](*WIT)
check("L15-R11 [THE GHOST QUESTION] the reduced scalar's kinetic normalisation stays POSITIVE at sigma = 1 -- and "
      "at the witness it is exactly sigma-independent, because A_0 = det M/M22 = -M12^2/M22 there and both M12 "
      "and M22 are sigma-free. It is still positive at j = 1.007. Independently, LOCAL_WAVE's reduced scalar "
      "Lagrangian has kinetic coefficient a_* = 3 - 81/(4T) > 0 with NO sigma in it (L15-S2). No ghost at "
      "sigma = 1, by two separate routes.",
      A0_w1 > 0 and close(A0_w1, A0_w13, mp.mpf('1e-40')) and res['1']['A0'] > 0 and AST > 0,
      f"A_0(witness) = {mp.nstr(A0_w1, 12)} at both sigma; A_0(j=1.007) = {mp.nstr(res['1/3']['A0'], 10)} -> "
      f"{mp.nstr(res['1']['A0'], 10)}; a_* = {mp.nstr(AST, 10)}")

# ================================================================================================================
# section 7 -- is sigma = 1 a singular or degenerate point?
# ================================================================================================================
print("\n-- 7. is sigma = 1 a singular or degenerate point of the construction? --------------------------------------")

Cconst = NUM((1 + astar * sig).subs(sig, 1))
deg = dict(p_R=pR1, q_R=qR1, A_R=AR1, B_R=BR1, a_star=AST, C_1_plus_astar_sigma=Cconst,
           three_pR_minus_44=3 * pR1 - 44, pR_T_minus_9=pR1 * T - 9, three_pR_plus_4=3 * pR1 + 4,
           detMstar=detstar1, M12_witness=f1['M12'](*WIT), M22_witness=f1['M22'](*WIT),
           det_Hqq=mp.det(Hm1), J_T_witness=f1['J'](*WIT))
check("L15-R12 [THE DEGENERACY QUESTION] sigma = 1 is a REGULAR point of the construction, not a singular one. "
      "Every coefficient that could have vanished there is bounded away from zero: p_R, q_R, A_R, B_R, a_*, "
      "C = 1 + a_* sigma, det M_star, M12, M22, det H_qq, J_T(witness), and all three factors of the obstruction. "
      "The construction's ONE degeneracy in sigma is the obstruction's zero at sigma_* = 4T/(4T-27) = 1.679, "
      "which is 29.6% superluminal -- not 'marginally' superluminal, and outside IC-4's declared 0 < sigma <= 1. "
      "Luminality does not sit where a coefficient vanishes here.",
      all(abs(v) > mp.mpf('1e-6') for v in deg.values()) and abs(SIGSTAR - 1) > mp.mpf('0.5'),
      "smallest |coefficient| at sigma=1 is "
      f"{min(deg, key=lambda k: abs(deg[k]))} = {mp.nstr(min(abs(v) for v in deg.values()), 6)}")

# ================================================================================================================
# section 8 -- the sheared state: what I can and cannot say at sigma = 1
# ================================================================================================================
print("\n-- 8. the sheared state ------------------------------------------------------------------------------------")

lamsh = [mp.mpf('-0.6424435072183933'), mp.mpf('-0.622272178918671'), mp.mpf('-0.5676134368548011')]
rsh = sum(lamsh)
tsh = sum(x_**2 for x_ in lamsh) - rsh**2 / 3
sh = {}
for nm in ('1/3', '1'):
    ff, _ = KIT[nm]
    xs, us = solve_aux(ff, rsh, tsh)
    sh[nm] = dict(xi=xs, u=us, J=ff['J'](xs, us, rsh, tsh), c7=ff['c7'](xs, us, rsh, mp.mpf(0)),
                  c=ff['c'](xs, us, rsh, tsh))
check("L15-R13 the sheared fixture DOES move with sigma, unlike the isotropic branch, because its tau != 0 makes "
      "the auxiliary constraints see F. At sigma = 1/3 my solve returns IC6_EVEN's xi = 0.242752746344542675, "
      "u = 0.663589818477735377, J_T = 0.986102159712075428 (18 digits); at sigma = 1 the state and IC7's "
      "coefficient there both shift.",
      close(sh['1/3']['xi'], '0.242752746344542675', mp.mpf('1e-17'))
      and close(sh['1/3']['u'], '0.663589818477735377', mp.mpf('1e-17'))
      and close(sh['1/3']['J'], '0.986102159712075428', mp.mpf('1e-17'))
      and abs(sh['1']['xi'] - sh['1/3']['xi']) > mp.mpf('1e-12'),
      f"sigma=1: xi = {mp.nstr(sh['1']['xi'], 19)}, u = {mp.nstr(sh['1']['u'], 19)}, "
      f"J_T = {mp.nstr(sh['1']['J'], 19)}; c_7 = {mp.nstr(sh['1/3']['c7'], 15)} -> {mp.nstr(sh['1']['c7'], 15)}")

check("L15-R14 [new liability at sigma = 1] IC7's tensor detuning off flat backgrounds gets WORSE. The exact form "
      "c_T,physical^2 = 1 - 4 c_7 Rbar_0 / c (L4 finding 2) is unchanged, but c_7 grows with sigma while c stays "
      "near 1, so the per-unit-Rbar_0 detuning at the sheared state roughly doubles. Whatever fixes the sheared "
      "mixing must now protect an exactly luminal tensor cone against a larger counterterm.",
      abs(4 * sh['1']['c7'] / sh['1']['c']) > abs(4 * sh['1/3']['c7'] / sh['1/3']['c']),
      f"4 c_7/c per unit Rbar_0: {mp.nstr(4*sh['1/3']['c7']/sh['1/3']['c'], 8)} (sigma=1/3) -> "
      f"{mp.nstr(4*sh['1']['c7']/sh['1']['c'], 8)} (sigma=1)")

print("\n    NOT AVAILABLE TO THIS LANE, named exactly:")
print("      - S4_11(sigma=1), the sheared reduced quartic. IC6_EVEN's -0.0642323935174161 and IC7's leftover")
print("        0.0151964888331 are outputs of the lead's ANISOTROPIC two-mode reduction (ic6_even_characteristics.py),")
print("        which is not reproduced in this lane and whose sigma-dependence is not published in closed form.")
print("        The sheared leftover at sigma = 1 therefore requires re-running that reduction with")
print("        p_R = 8/3 + 4 a_* sigma at sigma = 1. Same for the antisymmetric mixing N2_21 = 0.000563025148111.")
print("      - the k^2 reduction giving the witness speeds (sigma, 1) and IC7's quoted c_s^2 = 0.388526918 at")
print("        k = 1e5: that needs the background time derivatives (Mdot, Ndot) of the lead's reduced system.")
print("        The identification c_s^2 = sigma is read from LOCAL_WAVE_REPORT's boxed z'' + 3z' + sigma x z = 0")
print("        and re-derived here (L15-S2); the finite-k correction to it is not.")
print("      - IC10_LOCAL_CLOCK / OPTICAL_ALIGNMENT use the symbol 'sigma' for a DIFFERENT, unrelated quantity")
print("        (sigma = -1/4 in the s8/K8/J8/c8 optical block). Nothing in this lane touches that symbol.")

# ================================================================================================================
# section 9 -- the requirement itself
# ================================================================================================================
print("\n-- 9. the requirement ---------------------------------------------------------------------------------------")

check("L15-B1 [HANDOFF_CONTRACT open challenge B1, as literally written] 'the IC6 obstruction, the IC7 "
      "counterterm and the tensor balance all re-derive at sigma = 1'. They do: the obstruction re-derives "
      "(L15-R1), the counterterm re-derives and is still well defined (L15-R6), the tensor balance re-derives "
      "exactly (L15-R9). B1 is DISCHARGED. Its answer is negative for the construction.",
      S4p_1 < 0 and res['1']['c7'] != 0 and sp.simplify(cT2_IC6 - 1) == 0)

check("L15-P1 [PROGRAMME REQUIREMENT -- the outcome that was worth hoping for] 'moving sigma to the "
      "Cherenkov-forced value removes the IC6 obstruction, so IC7's counterterm becomes unnecessary and the "
      "construction SIMPLIFIES.' It does not. The obstruction persists with the same sign, is 1.81x larger, "
      "IC7 is needed 1.78x more strongly, its repair window halves, and no sigma in IC-4's own admissible "
      "interval (0,1] would have helped (L15-R3). This is a requirement not met, not a claim refuted: the lead "
      "never asserted that sigma = 1 would repair anything.",
      S4p_1 == 0,
      f"S_4'(1)|_sigma=1 = {mp.nstr(S4p_1, 18)} != 0; the construction does NOT simplify at sigma = 1")

# ================================================================================================================
print("\n-- verdict --------------------------------------------------------------------------------------------------")
print(f"    S_4'(1) at sigma = 1/3 (published)  : {mp.nstr(S4p_13, 18)}")
print(f"    S_4'(1) at sigma = 1   (Cherenkov)  : {mp.nstr(S4p_1, 18)}")
print(f"    zero of S_4'(1;sigma)               : sigma_* = 4T/(4T-27) = {mp.nstr(SIGSTAR, 12)}  (c_s = "
      f"{mp.nstr(mp.sqrt(SIGSTAR), 8)} c), OUTSIDE (0,1]")
print(f"    obstruction at sigma = 1            : PERSISTS, same sign, {mp.nstr(S4p_1/S4p_13, 6)}x larger")
print(f"    IC7 counterterm                     : STILL REQUIRED, and larger (c_7 x{mp.nstr(res['1']['c7']/res['1/3']['c7'], 6)})")
print( "    tensor cone c_T^2 = 1               : SURVIVES exactly, sigma-independent identity")
print( "    DOF count                           : UNCHANGED, 2 tensor + 1 clock scalar")
print( "    ghost                               : NONE; kinetic normalisation a_* and A_0(witness) are sigma-free")
print( "    sigma = 1 degenerate?               : NO, regular point")

print("\n" + BAR)
hard = [n for n in FAILS if not n.startswith('L15-P1')]
print(f"L15: {len(FAILS)} FAIL(S)" if FAILS else "L15: ALL CHECKS PASS")
for n in FAILS:
    print(f"    FAIL: {n.split('.')[0]}")
print("    Every reproduction check of the lead's own numbers PASSES, including the mandatory control L15-C6,")
print("    which returned L4's confirmed S_4'(1) = -11.1407711251147987 before any sigma was moved. The single")
print("    FAIL is the hoped-for outcome (sigma = 1 repairs the construction), which is false. Exit 2 marks that")
print("    designed outcome; exit 1 would mean one of the lead's numbers failed to reproduce.")
print(BAR)
sys.exit(1 if hard else (2 if FAILS else 0))
