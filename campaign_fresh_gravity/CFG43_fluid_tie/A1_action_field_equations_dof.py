#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
A1 -- ONE ACTION: GR + Henneaux-Teitelboim (HT) sector with integration constant Lambda + a conserved (Schutz-Sorkin / Brown)
fluid whose stress cap P_cap = a0^2/(8 pi G) is a function of the SAME HT field.  Field equations, number conservation, the
Dirac constraint count.  (Gap 3 of scratchpad/closure/actions.md.)

THE ACTION (c = 1, Mp2 = 1/(8 pi G), eps = kappa^2/(8 pi), kappa = 1/2 FITTED):
  S = Int d^4x { sqrt(-g) [ (Mp2/2) R - Mp2 Lambda ]  +  Mp2 Lambda d_m T^m                      GR + HT (T^m: vector density)
                 - sqrt(-g) rho(n; Lambda)  +  J^m d_m theta } ,   n = sqrt(-g_mn J^m J^n)/sqrt(-g)   Schutz-Sorkin fluid
  rho(n; Lambda) = m n  +  P_cap(Lambda) * x atan(x) ,   x = m n / (nu_s Mp2 Lambda) ,   P_cap(Lambda) = eps Mp2 Lambda
  =>  P = n rho_n - rho = P_cap x^2/(1 + x^2)   (saturating, P -> P_cap),  rho_Lambda|_n = - P/Lambda   (homogeneity).
  POSTULATED: the saturating form F(x) = x^2/(1+x^2) and the argument x = rho_c/(nu_s rho_Lambda).  nu_s is a pure number.
  DERIVED from the action (this script): Lambda constant (T^m eq.), number conservation (theta eq.), the clock d_m T^m
  = sqrt(-g)(1 - P/(Mp2 Lambda)) absorbing the fluid's dependence on Lambda, reparametrisation (Bianchi) identity, Friedmann
  eq., the continuity equation (rho' + 3H(rho + P) = rho_Lambda Lambda'), the Dirac count 2N + 2 (fluid + ONE global pair).

MUTATE=1  the multiplier is replaced by a dynamical scalar psi, Lambda -> U(psi) with kinetic term (Mp2/2)(d psi)^2 (the fluid still
          reads Lambda = U(psi)): Lambda' = 0 no longer follows, the fluid is no longer separately conserved, the count has an
          extra local dof, delta Lambda obeys a wave equation.  Every check below is COMPUTED on the mutated action.
MUTATE=2  the tie is dropped: the fluid's cap reads an independent constant Lc, not the HT field (HT multiplier kept):
          rho_Lambda|_n = 0, the clock is Na^3 with no fluid term, and sqrt(8 pi G P_cap) != kappa sqrt(Lambda/8pi).

Checks:  H-EOS, H-TIE, H-CONST, H-NUM, H-CLOCK, H-FRIED, H-BIANCHI, H-SEPCONS, H-LOCAL, H-DIRAC-0, H-DIRAC.
Run:  python3 A1_action_field_equations_dof.py       (MUTATE=1 or 2 for the controls)
"""
import os
import sys
import math
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import A_common as C

R = C.Run("A1_action_field_equations_dof")
P, check = R.P, R.check
M = C.MUTATE
P(__doc__)
P("MUTATE mode = %d  (0 = HT multiplier + tied cap; 1 = dynamical scalar replaces the multiplier; 2 = cap not tied to Lambda)" % M)

t = sp.Symbol('t')
Mp2, m, eps, nus = sp.symbols('Mp2 m epsilon nu_s', positive=True)
Lc = sp.Symbol('Lc', positive=True)          # an independent constant (what the cap reads in the MUTATE=2 action)


def rho_eos(n_, L_):
    """rho(n; Lambda) with the cap read from L_."""
    x_ = m * n_ / (nus * Mp2 * L_)
    return m * n_ + eps * Mp2 * L_ * x_ * sp.atan(x_)


def cap_arg(L_ht):
    """what the fluid Lagrangian reads as 'Lambda': the HT field (mode 0), an independent constant (mode 2)."""
    return Lc if M == 2 else L_ht


# ---------------------------------------------------------------------------------------------- the EOS (POSTULATED entry)
R.banner("E  THE FLUID'S EOS: P = n rho_n - rho, the cap, and how the cap reads Lambda")
nn, LL = sp.symbols('n LL', positive=True)                  # LL: the HT field's value
arg = cap_arg(LL)
x_s = m * nn / (nus * Mp2 * arg)
rho_s = rho_eos(nn, arg)
P_s = sp.simplify(nn * sp.diff(rho_s, nn) - rho_s)
Pcap_s = eps * Mp2 * arg
e1 = sp.simplify(P_s - Pcap_s * x_s ** 2 / (1 + x_s ** 2)) == 0
lim = sp.limit(P_s.subs({m: 1, Mp2: 1, nus: 1, eps: sp.Rational(1, 100), Lc: 1}).subs(LL, 1), nn, sp.oo)
e2 = sp.simplify(lim - sp.Rational(1, 100)) == 0            # sup P = P_cap = eps Mp2 (Lambda or Lc)
e3 = sp.simplify(sp.diff(rho_s, LL) + P_s / LL) == 0         # rho_Lambda|_n = -P/Lambda for the HT field Lambda (LL)
check("H-EOS", "P = n rho_n - rho = P_cap x^2/(1+x^2); sup_n P = P_cap; and the fluid depends on the HT field Lambda as rho_Lambda|_n = -P/Lambda "
      "(degree-1 homogeneity in (n, Lambda))", "P closed form %s; sup P = P_cap %s; d rho/d Lambda_HT = -P/Lambda_HT: %s" % (e1, e2, e3),
      e1 and e2 and e3, "MUTATE=2: the fluid reads Lc, so it does not depend on the HT field at all" if M == 2 else
      "the tie is a statement about rho(n; Lambda): the cap scale and the saturation density both scale with Lambda")
# a0 from the cap == XR20's alpha(Lambda), as FUNCTIONS of the HT field (symbolic) and as numbers (canonical footing)
Lsym = sp.Symbol('Lsym', positive=True)
Psup = Pcap_s.subs(LL, Lsym)
a0_cap_fn = sp.sqrt(Psup / Mp2)                             # sqrt(8 pi G P_cap), c = 1
alpha_xr20 = sp.sqrt(eps * Lsym)                            # = kappa sqrt(Lambda/8 pi)  (eps = kappa^2/8pi)
fn_eq = sp.simplify(a0_cap_fn - alpha_xr20) == 0
Lam_SI = 8 * math.pi * C.G_SI * C.RHO_L / C.C_SI ** 2
Pcap_SI = C.EPS * C.RHO_L * C.C_SI ** 2
a0_a = math.sqrt(8 * math.pi * C.G_SI * Pcap_SI)
a0_b = C.KAPPA * math.sqrt(Lam_SI / (8 * math.pi)) * C.C_SI ** 2
a0_c = C.KAPPA * C.C_SI * math.sqrt(C.G_SI * C.RHO_L)
num_eq = abs(a0_a / a0_c - 1) < 1e-12 and abs(a0_b / a0_c - 1) < 1e-12 and abs(a0_c / C.A0["canonical"] - 1) < 2e-4
check("H-TIE", "as functions of the HT field: sqrt(8 pi G P_cap(Lambda)) == kappa sqrt(Lambda/8pi) (the SAME alpha(Lambda) XR20 wrote into the AQUAL kernel), "
      "so a0 = kappa c sqrt(G rho_Lambda) with kappa the only coupling",
      "function identity %s; numbers: sqrt(8 pi G P_cap) = %.5e, kappa sqrt(Lambda/8pi) c^2 = %.5e, kappa c sqrt(G rho_L) = %.5e m/s^2 "
      "(canonical footing %.4e); P_cap = %.4e Pa (= %.3f%% of rho_L c^2 = %.4e Pa)" % (fn_eq, a0_a, a0_b, a0_c, C.A0["canonical"], Pcap_SI,
                                                                                  100 * C.EPS, C.RHO_L * C.C_SI ** 2),
      fn_eq and num_eq, "kappa = 1/2 stays FITTED; the sqrt(Lambda) power is dimensional (FP0 C1)")

# ---------------------------------------------------------------------------------------------- minisuperspace variation
R.banner("F  FLAT-FRW MINISUPERSPACE: the action varied (sympy Euler-Lagrange), generic rho(n, Lambda) for the structure")
a = sp.Function('a')(t); N = sp.Function('N')(t); Lam = sp.Function('Lam')(t); T0 = sp.Function('T0')(t)
J0 = sp.Function('J0')(t); th = sp.Function('th')(t); psi = sp.Function('psi')(t)
rhoG = sp.Function('rho')
Uf = sp.Function('U')
n_of = J0 / a ** 3

if M == 1:
    # ---- scalar replaces the multiplier: Lambda = U(psi); L_psi = N a^3 Mp2 [psi'^2/(2N^2) - U]; NO T
    L_gen = (-3 * Mp2 * a * a.diff(t) ** 2 / N + N * a ** 3 * Mp2 * (psi.diff(t) ** 2 / (2 * N ** 2) - Uf(psi))
             - N * a ** 3 * rhoG(n_of, Uf(psi)) + J0 * th.diff(t))
    fields = [a, N, psi, J0, th]
    names = ['a', 'N', 'psi', 'J', 'th']
    L_con = (-3 * Mp2 * a * a.diff(t) ** 2 / N + N * a ** 3 * Mp2 * (psi.diff(t) ** 2 / (2 * N ** 2) - Uf(psi))
             - N * a ** 3 * rho_eos(n_of, Uf(psi)) + J0 * th.diff(t))
else:
    L_gen = (-3 * Mp2 * a * a.diff(t) ** 2 / N - N * a ** 3 * Mp2 * Lam + Mp2 * Lam * T0.diff(t)
             - N * a ** 3 * rhoG(n_of, cap_arg(Lam)) + J0 * th.diff(t))
    fields = [a, N, Lam, T0, J0, th]
    names = ['a', 'N', 'Lam', 'T', 'J', 'th']
    L_con = (-3 * Mp2 * a * a.diff(t) ** 2 / N - N * a ** 3 * Mp2 * Lam + Mp2 * Lam * T0.diff(t)
             - N * a ** 3 * rho_eos(n_of, cap_arg(Lam)) + J0 * th.diff(t))
Egen = dict(zip(names, [e.lhs for e in euler_equations(L_gen, fields, t)]))
Ec = dict(zip(names, [e.lhs for e in euler_equations(L_con, fields, t)]))

# --- H-CONST: is Lambda' = 0 implied by the field equations?
if M != 1:
    eq_T = sp.simplify(Egen['T'])
    imp = sp.solve(sp.Eq(eq_T, 0), Lam.diff(t))
    Ldot_zero = imp == [0]
    txt = "E_T = %s  =>  Lambda' = %s   (the matter Lagrangian, incl. the fluid's Lambda-dependence, does not enter E_T)" % (eq_T, imp)
else:
    Epsi = Ec['psi']
    psidd = sp.solve(sp.Eq(Epsi.subs(N, 1), 0), psi.diff(t, 2))[0]
    psidd0 = sp.simplify(psidd.subs(psi.diff(t), 0))
    Ldot_zero = sp.simplify(psidd0) == 0
    txt = "no T-equation.  Lambda = U(psi); at psi' = 0 the field equation gives psi'' = %s != 0, so Lambda' = U' psi' is generated" % sp.simplify(psidd0)
check("H-CONST", "Lambda is a global integration constant: the equations imply Lambda' = 0 (so P_cap(Lambda) and a0 are constant in z)", txt, Ldot_zero,
      "MUTATE=1: with a dynamical scalar the cap runs with redshift" if M == 1 else "a0 = alpha(Lambda) c^2 and P_cap are constant on every solution")

# --- H-NUM
eq_th = sp.simplify(Egen['th'])
num_ok = sp.simplify(eq_th + J0.diff(t)) == 0
check("H-NUM", "number conservation: the theta equation is J0' = 0, i.e. n a^3 = const, for ANY rho(n, Lambda) and any Lambda(t)",
      "E_theta = %s; n = J0/a^3" % eq_th, num_ok, "Omega_c is initial data: the constant J0 (comoving particle number) is free, not fixed by the action")

# --- H-CLOCK (HT-type actions only)
if M != 1:
    eq_L = sp.simplify(Egen['Lam'])
    Tdot = sp.simplify(sp.solve(sp.Eq(eq_L, 0), T0.diff(t))[0])
    Tdot_c = sp.solve(sp.Eq(Ec['Lam'], 0), T0.diff(t))[0]
    n_ = sp.Symbol('n_', positive=True)
    rr = rho_eos(n_, Lam)                                                    # the pressure that the fluid ACTUALLY has, with Lambda = the HT field
    Pfl = (n_ * sp.diff(rho_eos(n_, cap_arg(Lam)), n_) - rho_eos(n_, cap_arg(Lam))).subs(n_, n_of)
    Pty = (n_ * sp.diff(rr, n_) - rr).subs(n_, n_of)
    clock_ok = sp.simplify(Tdot_c - N * a ** 3 * (1 - Pty / (Mp2 * Lam))) == 0
    elsewhere = any(sp.simplify(Egen[k]).has(T0) for k in ('a', 'N', 'J', 'th'))
    check("H-CLOCK", "the fluid's Lambda-dependence lands ONLY in the unimodular clock: T0' = N a^3 [1 + rho_Lambda/Mp2] = N a^3 [1 - P/(Mp2 Lambda)], and T^m appears "
          "in no other equation", "generic: T0' = %s; concrete: T0' = N a^3 (1 - P/(Mp2 Lambda)) is %s; T in other equations: %s" % (Tdot, clock_ok, elsewhere),
          clock_ok and (not elsewhere),
          "XR20 T1b had the same structure for the MOND term (clock shift (kappa^2/8pi) F); here the shift is P/rho_Lambda = eps F(x)")
else:
    P("  [n/a ] H-CLOCK: no multiplier and no T^m in the mutated action (nothing absorbs d L_fluid/d Lambda; it back-reacts on psi)")

# --- H-FRIED: lapse equation: is it GR + Lambda + fluid, with no other component?
eq_N = sp.simplify(Egen['N'])
H_ = sp.Symbol('H')
EN = sp.expand(sp.simplify(eq_N.subs(N, 1).subs(a.diff(t), H_ * a)) / a ** 3)
if M != 1:
    fr_ok = sp.simplify(EN - (3 * Mp2 * H_ ** 2 - Mp2 * Lam - rhoG(n_of, cap_arg(Lam)))) == 0
    frtxt = "E_N/a^3 = %s" % sp.simplify(EN)
else:
    extra = EN.has(psi.diff(t))
    fr_ok = not extra
    frtxt = "E_N/a^3 = %s  (contains psi'^2: an extra dark-energy kinetic term)" % sp.simplify(EN)
check("H-FRIED", "lapse equation = Friedmann with no extra component: 3 Mp2 H^2 = Mp2 Lambda + rho(n; Lambda) (GR + Lambda + the fluid)", frtxt, fr_ok,
      "with Lambda' = 0 the HT sector adds nothing to the background")

# --- H-BIANCHI: reparametrisation identity (must hold in every mode: the mutated action is also invariant)
if M != 1:
    ident = (Ec['a'] * a.diff(t) + Ec['Lam'] * Lam.diff(t) + Ec['T'] * T0.diff(t) + Ec['th'] * th.diff(t) + Ec['J'] * J0.diff(t) - N * Ec['N'].diff(t))
else:
    ident = (Ec['a'] * a.diff(t) + Ec['psi'] * psi.diff(t) + Ec['th'] * th.diff(t) + Ec['J'] * J0.diff(t) - N * Ec['N'].diff(t))
bian_ok = sp.simplify(ident) == 0
check("H-BIANCHI", "time-reparametrisation identity  sum_i E_i q_i' - N E_N' == 0  holds identically (the constraint propagates iff the field equations hold)",
      "identity: %s" % bian_ok, bian_ok, "holds in every mode (an invariant action); the physics is in the NEXT check")

# --- H-SEPCONS: the fluid's energy is separately conserved on shell  <=>  Lambda' = 0 is implied
nsym = sp.Symbol('nsym', positive=True); Ls_ = sp.Symbol('Ls_', positive=True)
rho2 = rho_eos(nsym, Ls_)
P2 = sp.simplify(nsym * sp.diff(rho2, nsym) - rho2)
Hh, Ld = sp.symbols('Hh Ldot')
chain = sp.simplify(sp.diff(rho2, nsym) * (-3 * Hh * nsym) + sp.diff(rho2, Ls_) * Ld + 3 * Hh * (rho2 + P2) - sp.diff(rho2, Ls_) * Ld) == 0   # rho' + 3H(rho+P) = rho_L L'
if M != 1:
    src_zero = Ldot_zero                                    # source rho_Lambda Lambda' with Lambda' = 0 from E_T
    srctxt = "source rho_Lambda*Lambda' = 0 because Lambda' = 0 on shell"
else:
    # evaluate the source along a solution of the mutated system: pick psi' != 0 (Lambda' = U' psi') -> nonzero
    srcval = float(sp.diff(rho2, Ls_).subs({nsym: 1.0, Ls_: 0.7, m: 1, Mp2: 1, nus: 3, eps: float(C.EPS)}) * (-0.7) * 0.3)
    src_zero = abs(srcval) < 1e-30
    srctxt = "source rho_Lambda*Lambda' = %.3e for a solution with psi' = 0.3 (nonzero): the fluid exchanges energy with psi" % srcval
check("H-SEPCONS", "chain rule: rho' + 3H(rho + P) = rho_Lambda Lambda' (verified) -- the fluid is separately conserved on shell, so Omega_c a^3 = const",
      "chain rule %s; %s" % (chain, srctxt), chain and src_zero,
      "MUTATE=1: coupled dark energy; Omega_c is no longer free initial data")

# ---------------------------------------------------------------------------------------------- 1+1 toy: local structure
R.banner("L  LOCAL STRUCTURE (1+1 toy with x-dependence): does delta Lambda propagate?")
x = sp.Symbol('x')
J0t = sp.Function('J0')(t, x); J1t = sp.Function('J1')(t, x); tht = sp.Function('th')(t, x)
nt = sp.sqrt(J0t ** 2 - J1t ** 2)
if M != 1:
    Lt = sp.Function('Lam')(t, x); T0t = sp.Function('T0')(t, x); T1t = sp.Function('T1')(t, x)
    L2 = (-Mp2 * Lt + Mp2 * Lt * (T0t.diff(t) + T1t.diff(x)) - rho_eos(nt, cap_arg(Lt)) + J0t * tht.diff(t) + J1t * tht.diff(x))
    E2 = euler_equations(L2, [Lt, T0t, T1t, J0t, J1t, tht], [t, x])
    e_T0, e_T1, e_th = sp.simplify(E2[1].lhs), sp.simplify(E2[2].lhs), sp.simplify(E2[5].lhs)
    loc_ok = (sp.simplify(e_T0 + Mp2 * Lt.diff(t)) == 0 and sp.simplify(e_T1 + Mp2 * Lt.diff(x)) == 0
              and sp.simplify(e_th + J0t.diff(t) + J1t.diff(x)) == 0)
    d = sp.Function('d')(t, x); e_ = sp.Symbol('e_'); L0 = sp.Symbol('L0', positive=True)
    lin = [sp.simplify(sp.diff(E2[i].lhs.subs(Lt, L0 + e_ * d).doit(), e_).subs(e_, 0)) for i in (1, 2)]
    lin_ok = sp.simplify(lin[0] + Mp2 * d.diff(t)) == 0 and sp.simplify(lin[1] + Mp2 * d.diff(x)) == 0
    # any second derivative of Lambda anywhere in the Lambda-sector equations?
    sec = any(E2[i].lhs.has(sp.Derivative(Lt, (t, 2))) or E2[i].lhs.has(sp.Derivative(Lt, (x, 2))) or E2[i].lhs.has(sp.Derivative(Lt, t, x)) for i in range(6))
    check("H-LOCAL", "with x-dependence: E_T0 = -Mp2 d_t Lambda, E_T1 = -Mp2 d_x Lambda, E_theta = -(d_t J^0 + d_x J^1); a perturbation obeys d_t(dL) = d_x(dL) = 0; "
          "no second derivative of Lambda appears anywhere (no wave operator)",
          "T equations + number current %s; linearised first-order homogeneous %s; second derivatives of Lambda present: %s" % (loc_ok, lin_ok, sec),
          loc_ok and lin_ok and (not sec), "no propagating delta Lambda: the only freedom is the global constant")
else:
    psit = sp.Function('psi')(t, x)
    L2s = ((Mp2 / 2) * (psit.diff(t) ** 2 - psit.diff(x) ** 2) - Mp2 * Uf(psit) - rho_eos(nt, Uf(psit)) + J0t * tht.diff(t) + J1t * tht.diff(x))
    E2s = euler_equations(L2s, [psit], [t, x])[0].lhs
    sec = E2s.has(sp.Derivative(psit, (t, 2))) or E2s.has(sp.Derivative(psit, (x, 2)))
    check("H-LOCAL", "no second derivative of Lambda appears anywhere (delta Lambda has no wave operator)",
          "psi equation: %s ; second derivatives present: %s" % (E2s, sec), not sec, "MUTATE=1: delta psi propagates (wave equation with speed 1)")

# ---------------------------------------------------------------------------------------------- Dirac count on a periodic lattice
R.banner("D  DIRAC CONSTRAINT COUNT on a periodic 1-D lattice (flat background; gravity's 2 counted as textbook): fluid + HT (or + scalar)")
NL = 3
h = 1


def build_system(mode):
    """returns (coords, momenta, H_c, primaries, secondaries, symbols).  mode: 'HT', 'HT_UNTIED', 'SCALAR', 'FIXED'."""
    mk = lambda nm: [sp.Symbol('%s_%d' % (nm, j), real=True) for j in range(NL)]
    Ls, Ts, T1s, J0s, J1s, ths, psis = (mk(nm) for nm in ('Lam', 'Q', 'T1', 'J0', 'J1', 'th', 'psi'))
    Pq, pL, pT1, p0, p1, pith, ppsi = (mk(nm) for nm in ('P', 'pLam', 'pT1', 'p0', 'p1', 'pi', 'ppsi'))
    Lam0 = sp.Symbol('Lam_fixed', positive=True)
    Ufun = lambda p_: sp.exp(-p_)
    Hc = 0
    prim, sec = [], []
    for j in range(NL):
        jp = (j + 1) % NL
        if mode == 'HT':
            Lj, Lfl = Ls[j], Ls[j]
        elif mode == 'HT_UNTIED':
            Lj, Lfl = Ls[j], Lam0
        elif mode == 'SCALAR':
            Lj = Lfl = Ufun(psis[j])
        else:
            Lj = Lfl = Lam0
        nj = sp.sqrt(J0s[j] ** 2 - J1s[j] ** 2)
        Hc += rho_eos(nj, Lfl) + Mp2 * Lj - J1s[j] * (ths[jp] - ths[j]) / h
        if mode in ('HT', 'HT_UNTIED'):
            Hc += -Mp2 * Ls[j] * (T1s[jp] - T1s[j]) / h
        if mode == 'SCALAR':
            Hc += ppsi[j] ** 2 / (2 * Mp2) + Mp2 * (psis[jp] - psis[j]) ** 2 / (2 * h ** 2)
    fl_q, fl_p = J0s + J1s + ths, p0 + p1 + pith
    if mode in ('HT', 'HT_UNTIED'):
        coords, moms = Ts + Ls + T1s + fl_q, Pq + pL + pT1 + fl_p
    elif mode == 'SCALAR':
        coords, moms = psis + fl_q, ppsi + fl_p
    else:
        coords, moms = fl_q, fl_p
    for j in range(NL):
        jp = (j + 1) % NL
        prim += [p0[j], p1[j], pith[j] - J0s[j]]
        sec += [sp.diff(Hc, J1s[j])]                                # from p1 preservation
        if mode in ('HT', 'HT_UNTIED'):
            prim += [pL[j], pT1[j], Pq[j] - Mp2 * Ls[j]]
            sec += [Ls[jp] - Ls[j]]                                  # from pT1 preservation
    return coords, moms, Hc, prim, sec, dict(J0=J0s, J1=J1s, th=ths, Lam=Ls, T1=T1s, Q=Ts, P=Pq, psi=psis, Lam0=Lam0, pL=pL, pT1=pT1, p0=p0, p1=p1, pi=pith, ppsi=ppsi)


def dirac_count(mode, seed=3):
    coords, moms, Hc, prim, sec, S = build_system(mode)
    cons = prim + sec
    nq = len(coords)
    allsyms = coords + moms
    pars = [Mp2, m, eps, nus, S['Lam0']]
    Jc = sp.Matrix([[sp.diff(c, v) for v in allsyms] for c in cons])
    Om = np.zeros((2 * nq, 2 * nq))
    for i in range(nq):
        Om[i, nq + i], Om[nq + i, i] = 1.0, -1.0
    rng = np.random.default_rng(seed)
    vals = {Mp2: 1.3, m: 0.9, eps: float(C.EPS), nus: 7.0, S['Lam0']: 0.8}
    Lam0v = 0.8
    for j in range(NL):
        vals[S['th'][j]] = rng.normal()
        for k in ('pL', 'pT1', 'p0', 'p1'):
            vals[S[k][j]] = 0.0
        if mode in ('HT', 'HT_UNTIED'):
            vals[S['Lam'][j]] = Lam0v
            vals[S['T1'][j]] = rng.normal()
            vals[S['Q'][j]] = rng.normal()
            vals[S['P'][j]] = float(vals[Mp2]) * Lam0v
        if mode == 'SCALAR':
            vals[S['psi'][j]] = 0.4 + 0.1 * rng.normal()
            vals[S['ppsi'][j]] = rng.normal()
    nvals = rng.uniform(0.5, 2.0, NL)
    for j in range(NL):
        jp = (j + 1) % NL
        Lj = Lam0v if mode != 'SCALAR' else float(sp.exp(-vals[S['psi'][j]]))
        nj = float(nvals[j])
        rn = float(sp.diff(rho_eos(nn, LL), nn).subs({nn: nj, LL: Lj, Mp2: vals[Mp2], m: vals[m], eps: vals[eps], nus: vals[nus]}))
        dth = float(vals[S['th'][jp]] - vals[S['th'][j]])
        J1v = -nj * dth / rn
        vals[S['J1'][j]] = J1v
        vals[S['J0'][j]] = math.sqrt(nj ** 2 + J1v ** 2)
        vals[S['pi'][j]] = vals[S['J0'][j]]
    args = [float(vals[s]) for s in allsyms] + [float(vals[p_]) for p_ in pars]
    fJ = sp.lambdify(allsyms + pars, Jc, 'numpy')
    Jn = np.array(fJ(*args), dtype=float)
    fC = sp.lambdify(allsyms + pars, cons, 'numpy')
    cons_val = np.array(fC(*args), dtype=float)
    dH = [sp.diff(Hc, v) for v in allsyms]
    fH = sp.lambdify(allsyms + pars, dH, 'numpy')
    dHn = np.array(fH(*args), dtype=float)
    with np.errstate(all='ignore'):
        Mn = Jn @ Om @ Jn.T
        vec = Jn @ Om @ dHn
    assert np.isfinite(Mn).all() and np.isfinite(vec).all() and np.isfinite(Jn).all()
    svJ = np.linalg.svd(Jn, compute_uv=False)
    K = int((svJ > 1e-9 * svJ[0]).sum())
    svM = np.linalg.svd(Mn, compute_uv=False)
    Sc = int((svM > 1e-9 * max(svM[0], 1e-300)).sum())
    Mcp = Mn[:, :len(prim)]
    u = np.linalg.lstsq(Mcp, -vec, rcond=None)[0]
    resid = float(np.linalg.norm(Mcp @ u + vec))
    return dict(nq=nq, K=K, S=Sc, F=K - Sc, D=2 * nq - 2 * K + Sc, closure=resid, maxcons=float(np.abs(cons_val).max()))


mode_now = {0: 'HT', 1: 'SCALAR', 2: 'HT_UNTIED'}[M]
res_fixed = dirac_count('FIXED')
res_now = dirac_count(mode_now)
P("  lattice N = %d (periodic).  dim = phase-space dimension of the extended space; K = independent constraints; S = rank of their Poisson matrix (second class);"
  % NL)
P("  F = K - S (first class); D = dim - 2F - S = physical phase-space dimension; closure = residual of the consistency system for the multipliers (0 => no tertiary constraint)")
for nm_, r_ in (("FIXED Lambda (before: fluid only)", res_fixed), ("%s (now)" % mode_now, res_now)):
    P("    %-34s dim=%3d  K=%3d  S=%3d  F=%3d  D=%3d  closure=%.1e  max|C|=%.1e" % (nm_, 2 * r_['nq'], r_['K'], r_['S'], r_['F'], r_['D'], r_['closure'], r_['maxcons']))
D_fluid = 2 * NL
check("H-DIRAC-0", "before: the fluid alone (J^m second class with p_J and chi = dH/dJ^1; Hessian of rho(n) non-degenerate) leaves (theta, pi): D = 2N = %d, "
      "i.e. ONE local dof per site (the sound mode)" % D_fluid, "D_fixed = %d; closure residual %.1e" % (res_fixed['D'], res_fixed['closure']),
      res_fixed['D'] == D_fluid and res_fixed['closure'] < 1e-8,
      "with GR's 2 tensor dof (textbook: 12 canonical variables - 8 from 4 first-class constraints = 4 = 2 dof, NOT re-derived here) the local count is 3")
target = D_fluid + 2
check("H-DIRAC", "after adding the HT multiplier: D = 2N + 2 = %d (fluid + ONE global pair (Lambda_0, clock volume)), first class F = 2N - 1 (the pT^1 momenta and the "
      "N-1 independent d_x Lambda constraints), and NO secondary constraint arises from the fluid's Lambda-dependence (closure)" % target,
      "mode %s: D = %d, F = %d (target %d), closure %.1e" % (mode_now, res_now['D'], res_now['F'], 2 * NL - 1, res_now['closure']),
      res_now['D'] == target and res_now['F'] == 2 * NL - 1 and res_now['closure'] < 1e-8,
      ("MUTATE=1: (psi, p_psi) at every site adds a propagating dark-energy mode: D = 4N" if M == 1 else
       "local dof unchanged (2 + 1); the one new integration constant is global" + ("  [MUTATE=2 is not a dof question: the count is unchanged, the tie checks H-EOS/H-TIE/H-CLOCK catch it]" if M == 2 else "")))

R.finish()
