#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
E1 -- CFG43's committed action read as a dark-energy CURRENT: the full field equations for Lambda and T^m on an explicit metric,
the 3-form dual, the gauge freedom of the current, the metric equations, and exactly which part of the vacuum 'flow' is physical.

THE ACTION (CFG43, c = 1, Mp2 = M_P^2 = 1/(8 pi G), rho_vac = Mp2 Lambda, eps = kappa^2/(8 pi), kappa = 1/2 FITTED):
  S = Int d^4x { sqrt(-g)[(Mp2/2) R - Mp2 Lambda - rho(n; Lambda)] + Mp2 Lambda d_m T^m + J^m d_m theta }
  rho(n; Lambda) = m n + P_cap x atan x,  x = m n/(nu_s Mp2 Lambda),  P_cap = eps Mp2 Lambda      (CFG43's cap fluid; POSTULATED there)
  T^m is a vector DENSITY (the Henneaux-Teitelboim multiplier); t^m = T^m/sqrt(-g) is the vector ('the vacuum current').

Blocks: A the 3-form dual and the gauge (4-D, generic functions); B the Lambda/T^m field equations on the explicit static metric
(-e^{2 alpha(r)}, e^{2 beta(r)}, r^2, r^2 sin^2 theta), all fields functions of all four coordinates; C the fluid (reduced t-r);
D the metric equations (Weyl reduction, Ricci scalar computed); E the physical/gauge split (clock, river, inflow, stream gauges).

MUTATE=1  the 3-form mass term U = -(sigma/2) g_mn t^m t^n (sigma const) is added to the action: Lambda is no longer forced constant,
          the action is no longer gauge invariant, and T^m enters the metric equations.  (E1-FIELD, E1-GAUGE-S, E1-NOMETRIC must fail.)
"""
import os
import sys
import itertools
import sympy as sp
from sympy.calculus.euler import euler_equations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import E_common as C

R = C.Run("E1_ht_current_equations_gauge")
P, check = R.P, R.check
M = C.MUTATE
P(__doc__)
P("MUTATE mode = %d  (0 = CFG43's HT action; 1 = plus the 3-form mass term U = -(sigma/2) g_mn t^m t^n)" % M)

t, r, th, ph = X = sp.symbols('t r theta phi', real=True)
Mp2, sig, m, eps, nus = sp.symbols('Mp2 sigma m epsilon nu_s', positive=True)


def perm_sign(idx):
    """sign of the permutation sorting idx (0 if repeated)."""
    idx = list(idx)
    if len(set(idx)) < len(idx):
        return 0, None
    s = 1
    for i in range(len(idx)):
        for j in range(i + 1, len(idx)):
            if idx[i] > idx[j]:
                s = -s
    return s, tuple(sorted(idx))


def antisym(comp, k):
    """totally antisymmetric rank-k array from a dict {sorted tuple: expr}."""
    out = {}
    for idx in itertools.product(range(4), repeat=k):
        s, key = perm_sign(idx)
        out[idx] = 0 if s == 0 else s * comp[key]
    return out


def lc(*idx):
    return sp.LeviCivita(*idx)


# ============================================================================================ A: 3-form dual + gauge
R.banner("A  THE 3-FORM DUAL AND THE GAUGE FREEDOM OF THE CURRENT (4-D, generic component functions)")
Af = {key: sp.Function('A%d%d%d' % key)(*X) for key in itertools.combinations(range(4), 3)}
A = antisym(Af, 3)
T_of_A = [sp.Rational(1, 6) * sum(lc(mm, n, p, q) * A[(n, p, q)] for n in range(4) for p in range(4) for q in range(4)) for mm in range(4)]
F = {}
for mm, n, p, q in itertools.product(range(4), repeat=4):
    F[(mm, n, p, q)] = (sp.diff(A[(n, p, q)], X[mm]) - sp.diff(A[(mm, p, q)], X[n]) + sp.diff(A[(mm, n, q)], X[p]) - sp.diff(A[(mm, n, p)], X[q]))
divT = sum(sp.diff(T_of_A[mm], X[mm]) for mm in range(4))
starF = sp.Rational(1, 24) * sum(lc(*i) * F[i] for i in itertools.product(range(4), repeat=4))
dual_ok = sp.simplify(divT - starF) == 0
check("E1-DUAL", "T^m = (1/3!) eps^{mnpq} A_npq  =>  d_m T^m = (1/4!) eps^{mnpq} F_mnpq with F = dA (the HT current IS the dual of a 3-form; Lambda multiplies *F)",
      "identity for 4 generic components: %s" % dual_ok, dual_ok)

lam_f = {key: sp.Function('l%d%d' % key)(*X) for key in itertools.combinations(range(4), 2)}
lam = antisym(lam_f, 2)
dA = {}
for n, p, q in itertools.product(range(4), repeat=3):
    dA[(n, p, q)] = sp.diff(lam[(p, q)], X[n]) + sp.diff(lam[(q, n)], X[p]) + sp.diff(lam[(n, p)], X[q])
dF_zero = all(sp.simplify(sp.diff(dA[(n, p, q)], X[mm]) - sp.diff(dA[(mm, p, q)], X[n]) + sp.diff(dA[(mm, n, q)], X[p]) - sp.diff(dA[(mm, n, p)], X[q])) == 0
              for mm, n, p, q in itertools.combinations(range(4), 4))
dT = [sp.Rational(1, 6) * sum(lc(mm, n, p, q) * dA[(n, p, q)] for n in range(4) for p in range(4) for q in range(4)) for mm in range(4)]
omega = {(mm, n): sp.Rational(1, 2) * sum(lc(mm, n, p, q) * lam[(p, q)] for p in range(4) for q in range(4)) for mm in range(4) for n in range(4)}
omega_antisym = all(sp.simplify(omega[(a, b)] + omega[(b, a)]) == 0 for a in range(4) for b in range(4))
dT_is_curl = all(sp.simplify(dT[mm] - sum(sp.diff(omega[(mm, n)], X[n]) for n in range(4))) == 0 for mm in range(4))
ddivT = sp.simplify(sum(sp.diff(dT[mm], X[mm]) for mm in range(4)))
# conversely: ANY antisymmetric omega^{mn} (6 generic functions) leaves d_m T^m unchanged
wf = {key: sp.Function('w%d%d' % key)(*X) for key in itertools.combinations(range(4), 2)}
W = antisym(wf, 2)
dT_gen = [sum(sp.diff(W[(mm, n)], X[n]) for n in range(4)) for mm in range(4)]
ddiv_gen = sp.simplify(sum(sp.diff(dT_gen[mm], X[mm]) for mm in range(4)))
# reducibility: omega^{mn} -> omega^{mn} + eps^{mnpq} d_p xi_q changes nothing
xi = [sp.Function('xi%d' % q)(*X) for q in range(4)]
red = [sp.simplify(sum(sp.diff(sum(lc(mm, n, p, q) * sp.diff(xi[q], X[p]) for p in range(4) for q in range(4)), X[n]) for n in range(4))) for mm in range(4)]
gauge_ok = dF_zero and omega_antisym and dT_is_curl and ddivT == 0 and ddiv_gen == 0 and all(e == 0 for e in red)
check("E1-GAUGE", "A -> A + d lambda leaves F invariant and shifts T^m by d_n omega^{mn} with omega^{mn} = (1/2) eps^{mnpq} lambda_pq (antisymmetric); ANY "
      "antisymmetric omega leaves d_m T^m unchanged; the transformation is reducible (omega -> omega + eps d xi does nothing)",
      "dF = 0: %s; omega antisymmetric: %s; delta T = d_n omega^{mn}: %s; delta(div T) = %s (from dlambda), %s (generic omega); reducibility zero: %s"
      % (dF_zero, omega_antisym, dT_is_curl, ddivT, ddiv_gen, [str(e) for e in red]), gauge_ok,
      "counting: T^m has 4 components; omega has 6, minus the 4 - 1 = 3 of its own reducibility = 3 effective; 4 - 3 = 1 = the divergence")

# ============================================================================================ B: field equations on the explicit metric
R.banner("B  FIELD EQUATIONS FOR Lambda AND T^m ON THE EXPLICIT STATIC SPHERICAL METRIC (all fields depend on t, r, theta, phi)")
al = sp.Function('alpha')(r)
be = sp.Function('beta')(r)
gmat = sp.diag(-sp.exp(2 * al), sp.exp(2 * be), r ** 2, r ** 2 * sp.sin(th) ** 2)
sqrtg = sp.exp(al + be) * r ** 2 * sp.sin(th)
chk_det = sp.simplify(sp.sqrt(-gmat.det()) - sqrtg) == 0 if False else sp.simplify(-gmat.det() - sqrtg ** 2) == 0
Lam = sp.Function('Lam')(*X)
Tm = [sp.Function('T%d' % mm)(*X) for mm in range(4)]
n0 = sp.Function('n')(*X)                       # the fluid's number density field (Lambda-independent variable, as in CFG43)


def rho_eos(n_, L_):
    x_ = m * n_ / (nus * Mp2 * L_)
    return m * n_ + eps * Mp2 * L_ * x_ * sp.atan(x_)


nn, LL = sp.symbols('nn LL', positive=True)
P_eos = sp.simplify(nn * sp.diff(rho_eos(nn, LL), nn) - rho_eos(nn, LL))
Pcap_form = sp.simplify(P_eos - eps * Mp2 * LL * (m * nn / (nus * Mp2 * LL)) ** 2 / (1 + (m * nn / (nus * Mp2 * LL)) ** 2)) == 0
rhoL_ident = sp.simplify(sp.diff(rho_eos(nn, LL), LL) + P_eos / LL) == 0
check("E1-EOS", "CFG43's cap fluid: P = n rho_n - rho = P_cap x^2/(1+x^2) and d rho/d Lambda |_n = -P/Lambda (re-derived here)",
      "P closed form: %s; rho_Lambda = -P/Lambda: %s" % (Pcap_form, rhoL_ident), Pcap_form and rhoL_ident,
      "this identity is what puts the cap fluid's PRESSURE into the vacuum current's divergence")

tvec = [Tm[mm] / sqrtg for mm in range(4)]
t2 = sum(gmat[a, b] * tvec[a] * tvec[b] for a in range(4) for b in range(4))
U = -(sig / 2) * t2
L_B = sqrtg * (-Mp2 * Lam - rho_eos(n0, Lam)) + Mp2 * Lam * sum(sp.diff(Tm[mm], X[mm]) for mm in range(4))
if M == 1:
    L_B = L_B - sqrtg * U
EL = euler_equations(L_B, [Lam] + Tm, X)
E_Lam = EL[0].lhs
E_T = [EL[1 + mm].lhs for mm in range(4)]
ET_ok = all(sp.simplify(E_T[mm] + Mp2 * sp.diff(Lam, X[mm])) == 0 for mm in range(4))
Pn = P_eos.subs({nn: n0, LL: Lam})
div_expected = sqrtg * (1 - Pn / (Mp2 * Lam))
ELam_ok = sp.simplify(E_Lam - (Mp2 * sum(sp.diff(Tm[mm], X[mm]) for mm in range(4)) - Mp2 * div_expected)) == 0
if M == 1:
    ET_txt = "E_T0 = %s  (NOT -Mp2 d_t Lambda: the current is tied to grad Lambda, t_m = Mp2 d_m Lambda/sigma)" % sp.simplify(E_T[0])
else:
    ET_txt = "E_T^m = -Mp2 d_m Lambda for m = t, r, theta, phi"
check("E1-FIELD", "Euler-Lagrange: E_{T^m} = -Mp2 d_m Lambda (so d_m Lambda = 0 in all four directions: Lambda is a global constant whatever the matter) and "
      "E_Lambda  =>  d_m T^m = sqrt(-g) [1 - P/rho_vac]  (the vacuum current's divergence, with the cap fluid's pressure as its only matter source)",
      "%s: %s;  E_Lambda  <=>  d_m T^m = sqrt(-g)(1 - P/(Mp2 Lambda)): %s;  det: sqrt(-g) = e^(alpha+beta) r^2 sin(theta): %s" % (ET_txt, ET_ok, ELam_ok, chk_det),
      ET_ok and ELam_ok and chk_det,
      "covariantly: nabla_m t^m = 1 - P/rho_vac; dust baryons (rho = m n, no Lambda) do not enter at all; P <= P_cap = eps rho_vac, eps = %.5f" % C.EPS)
R.num("eps", C.EPS)

# ============================================================================================ C: the fluid (reduced t-r)
R.banner("C  THE FLUID EQUATIONS (reduced t-r sector, densities per sin(theta)): number conservation and the same divergence law")
Lr = sp.Function('Lr')(t, r); Tt = sp.Function('Tt')(t, r); Tr = sp.Function('Tr')(t, r)
Jt = sp.Function('Jt')(t, r); Jr = sp.Function('Jr')(t, r); thf = sp.Function('thf')(t, r)
sg2 = sp.exp(al + be) * r ** 2
n_J = sp.sqrt(sp.exp(2 * al) * Jt ** 2 - sp.exp(2 * be) * Jr ** 2) / sg2
L_C = sg2 * (-Mp2 * Lr - rho_eos(n_J, Lr)) + Mp2 * Lr * (sp.diff(Tt, t) + sp.diff(Tr, r)) + Jt * sp.diff(thf, t) + Jr * sp.diff(thf, r)
ELC = euler_equations(L_C, [Lr, Tt, Tr, Jt, Jr, thf], [t, r])
E_th = sp.simplify(ELC[5].lhs)
num_ok = sp.simplify(E_th + sp.diff(Jt, t) + sp.diff(Jr, r)) == 0
Pj = P_eos.subs({nn: n_J, LL: Lr})
divC_ok = sp.simplify(ELC[0].lhs - Mp2 * (sp.diff(Tt, t) + sp.diff(Tr, r)) + Mp2 * sg2 * (1 - Pj / (Mp2 * Lr))) == 0
check("E1-FLUID", "with the Schutz-Sorkin current: E_theta = -(d_t J^t + d_r J^r) (number conservation) and the Lambda equation again gives "
      "d_t T^t + d_r T^r = sqrt(-g)(1 - P(n)/rho_vac) with n = sqrt(-g_mn J^m J^n)/sqrt(-g)",
      "number conservation: %s; divergence law with the fluid's own n: %s" % (num_ok, divC_ok), num_ok and divC_ok)

# ============================================================================================ D: metric equations
R.banner("D  THE METRIC EQUATIONS: is the vacuum current in them?  (Weyl reduction of the static spherical metric, Ricci scalar computed)")


def ricci_scalar(g, co):
    gi = g.inv()
    n = len(co)
    Gam = [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], co[c]) + sp.diff(g[d, c], co[b]) - sp.diff(g[b, c], co[d])) for d in range(n)) / 2)
             for c in range(n)] for b in range(n)] for a in range(n)]
    Rs = 0
    for b in range(n):
        for d in range(n):
            if gi[b, d] == 0:
                continue
            Ric = sum(sp.diff(Gam[a][b][d], co[a]) - sp.diff(Gam[a][b][a], co[d]) for a in range(n))
            Ric += sum(Gam[a][a][e] * Gam[e][b][d] - Gam[a][d][e] * Gam[e][b][a] for a in range(n) for e in range(n))
            Rs += gi[b, d] * Ric
    return sp.simplify(Rs)


Rsc = ricci_scalar(gmat, list(X))
L0 = sp.Symbol('Lambda0', positive=True)
Mm = sp.Symbol('m_s', positive=True)
Tt_ = sp.Function('Tt')(t, r); Tr_ = sp.Function('Tr')(t, r)
L_grav = sp.exp(al + be) * r ** 2 * ((Mp2 / 2) * Rsc - Mp2 * L0)
L_T = Mp2 * L0 * (sp.diff(Tt_, t) + sp.diff(Tr_, r))
if M == 1:
    tv = [Tt_ / (sp.exp(al + be) * r ** 2), Tr_ / (sp.exp(al + be) * r ** 2)]
    L_T = L_T - sp.exp(al + be) * r ** 2 * (-(sig / 2) * (-sp.exp(2 * al) * tv[0] ** 2 + sp.exp(2 * be) * tv[1] ** 2))
# does the current enter the metric (alpha, beta) equations?  d L_T / d(alpha, alpha', alpha'', beta, ...) must vanish
dvars = [al, sp.diff(al, r), sp.diff(al, r, 2), be, sp.diff(be, r), sp.diff(be, r, 2)]
dLT = [sp.simplify(sp.diff(L_T, v)) for v in dvars]
nometric = all(e == 0 for e in dLT)
check("E1-NOMETRIC", "the HT term Mp2 Lambda d_m T^m contains no metric function: it contributes NOTHING to the metric equations "
      "(the vacuum current carries no stress; only -Mp2 Lambda sqrt(-g) gravitates, T_mn = -rho_vac g_mn, w = -1)",
      "d L_T/d(alpha, alpha', alpha'', beta, beta', beta'') = %s" % ([str(e) for e in dLT] if not nometric else "all 0"), nometric,
      "MUTATE=1: with the mass term the current's t^2 = g_mn t^m t^n carries the metric, so T^m sources gravity" if M == 1 else
      "the 'flow' is invisible to the geometry")
ELg = euler_equations(L_grav, [al, be], r)
f = 1 - 2 * Mm / r - L0 * r ** 2 / 3
sds = {al: sp.log(f) / 2, be: -sp.log(f) / 2}
res_sds = [sp.simplify(e.lhs.subs(sds).doit()) for e in ELg]
sds_ok = all(e == 0 for e in res_sds)
check("E1-SdS", "the reduced metric equations (GR + Lambda) are solved by Schwarzschild-de Sitter, e^{2 alpha} = e^{-2 beta} = 1 - 2 m/r - Lambda r^2/3, for ANY T^m",
      "residuals of E_alpha, E_beta on SdS: %s" % [str(e) for e in res_sds], sds_ok,
      "the only thing the dark-energy sector does to a point mass's geometry is the constant Lambda")

# ============================================================================================ E: physical vs gauge
R.banner("E  WHICH PART OF THE 'FLOW' IS PHYSICAL: clock, river, inflow and 'from the top' stream are gauge copies of ONE solution")
S = sp.Function('S')(r)                                          # the divergence source 1 - P/rho_vac (a function of r for a static system)
Wf = sp.Function('W')(r)                                         # W' = e^(alpha+beta) r^2 S   (the enclosed source)
Wp = sp.exp(al + be) * r ** 2 * S
sub_W = {sp.Derivative(Wf, r): Wp}


def div_tr(Tt_e, Tr_e):
    return sp.simplify((sp.diff(Tt_e, t) + sp.diff(Tr_e, r)).subs(sub_W))


target = sp.exp(al + be) * r ** 2 * S * sp.sin(th)
Cc, v = sp.symbols('C v', real=True)
gauges = {
    "clock (nothing flows; T^t = t sqrt(-g) S)": (t * target, 0),
    "river (radial outflow; T^r = W sin theta)": (0, Wf * sp.sin(th)),
    "inflow onto the galaxy (river - C sin theta, r > 0)": (0, (Wf - Cc) * sp.sin(th)),
}
divs = {k: div_tr(*vv) for k, vv in gauges.items()}
same_div = all(sp.simplify(d - target) == 0 for d in divs.values())
# explicit omega connecting clock -> river:  omega^{tr} = t W sin(theta) = -omega^{rt}
om_tr = t * Wf * sp.sin(th)
d_Tt = sp.diff(om_tr, r).subs(sub_W)                             # delta T^t = d_r omega^{tr}
d_Tr = sp.diff(-om_tr, t)                                        # delta T^r = d_t omega^{rt}
conn_ok = sp.simplify(gauges["clock (nothing flows; T^t = t sqrt(-g) S)"][0] - 0 - d_Tt) == 0 and sp.simplify(0 - Wf * sp.sin(th) - d_Tr) == 0
# river -> inflow: omega^{tr} = C t sin(theta) (constant in r, so delta T^t = 0 for r > 0; distributionally a clock pile-up at r = 0)
om2 = Cc * t * sp.sin(th)
conn2 = sp.simplify(sp.diff(om2, r)) == 0 and sp.simplify(sp.diff(-om2, t) - (-Cc * sp.sin(th))) == 0
# uniform stream 'from the top' in Cartesian coordinates: delta T^z = v is d_n omega^{zn} with omega^{zt} = v t
tt, xx, yy, zz = sp.symbols('tt xx yy zz', real=True)
omz = {('z', 't'): v * tt}
dTz = sp.diff(omz[('z', 't')], tt)
dTt_stream = sp.diff(-v * tt, zz)
stream_ok = sp.simplify(dTz - v) == 0 and dTt_stream == 0
# the instantaneous flux through the sphere r = R0 can be set to ANY function of time
kf = sp.Function('k')(t, r)
Rs0 = sp.Symbol('R0', positive=True)
h = r ** 2 * kf                                                  # omega^{tr} = h sin(theta), h(t, 0) = 0 (regular at the centre)
dFlux = sp.integrate(sp.integrate(-sp.diff(h, t) * sp.sin(th), (th, 0, sp.pi)), (ph, 0, 2 * sp.pi)).subs(r, Rs0)
dQ = sp.integrate(sp.integrate(sp.diff(h, r) * sp.sin(th), (th, 0, sp.pi)), (ph, 0, 2 * sp.pi))
dQ_R = sp.integrate(dQ, (r, 0, Rs0))
inv = sp.simplify(sp.diff(dQ_R, t) + dFlux)
flux_free = sp.simplify(dFlux + 4 * sp.pi * Rs0 ** 2 * sp.diff(kf, t).subs(r, Rs0)) == 0
check("E1-SPLIT", "on the SAME solution (same Lambda, same metric) the vacuum current can be a clock with no flow, a radial outflow, an inflow converging on the "
      "galaxy, or a uniform stream 'from the top': all differ by d_n omega^{mn}; the instantaneous flux through a sphere is shifted by -4 pi d_t h(t,R) "
      "(any function); the invariant is d/dt Q_ball + Flux = Int_ball d_m T^m",
      "same divergence in all three radial gauges: %s; clock->river omega^{tr} = t W sin(theta): %s; river->inflow omega^{tr} = C t sin(theta): %s; "
      "uniform stream omega^{zt} = v t: %s; flux shift = %s (free); delta(dQ/dt + Flux) = %s"
      % (same_div, conn_ok, conn2, stream_ok, sp.simplify(dFlux), inv), same_div and conn_ok and conn2 and stream_ok and flux_free and inv == 0,
      "PHYSICAL: the local scalar nabla.t = 1 - P/rho_vac (fixed by the matter, no freedom) and fluxes through CLOSED 3-surfaces (4-volumes; global zero "
      "mode = CFG43's one global pair).  GAUGE: direction, speed, where it passes, converging or streaming.")

# action invariance under the gauge transformation (the MUTATE mass term breaks it)
wfun = {key: sp.Function('q%d%d' % key)(*X) for key in itertools.combinations(range(4), 2)}
Wq = antisym(wfun, 2)
epsg = sp.Symbol('e_g')
Tshift = [Tm[mm] + epsg * sum(sp.diff(Wq[(mm, n)], X[n]) for n in range(4)) for mm in range(4)]
L_HT = Mp2 * Lam * sum(sp.diff(Tm[mm], X[mm]) for mm in range(4))
L_HTs = Mp2 * Lam * sum(sp.diff(Tshift[mm], X[mm]) for mm in range(4))
dL = sp.simplify(sp.diff(L_HTs, epsg).subs(epsg, 0))
if M == 1:
    t2s = sum(gmat[a, b] * Tshift[a] * Tshift[b] for a in range(4) for b in range(4)) / sqrtg ** 2
    t20 = sum(gmat[a, b] * Tm[a] * Tm[b] for a in range(4) for b in range(4)) / sqrtg ** 2
    dU = sp.diff(-sqrtg * (-(sig / 2)) * t2s, epsg).subs(epsg, 0)
    probe = {Tm[0]: 1, Tm[1]: 0, Tm[2]: 0, Tm[3]: 0}
    dU_num = sp.simplify(dU.subs(probe).doit())
    dL = sp.simplify(dL + dU_num)
gaugeS_ok = dL == 0
check("E1-GAUGE-S", "the action is invariant under T^m -> T^m + d_n omega^{mn} identically (Lagrangian shift = Mp2 Lambda d_m d_n omega^{mn} = 0)",
      "first-order Lagrangian shift: %s" % (dL if M == 1 else dL), gaugeS_ok,
      "MUTATE=1: the mass term makes the current's magnitude physical, so the 'flow' is no longer a gauge choice" if M == 1 else
      "so the committed action cannot tell a flowing vacuum from a static one")

R.P("")
R.P("  EQUATIONS OF THE DARK ENERGY IN THE COMMITTED ACTION (HT form):  d_m Lambda = 0;  nabla_m t^m = 1 - P/rho_vac;  t^m ~ t^m + (1/sqrt(-g)) d_n omega^{mn};")
R.P("  T_mn(vacuum) = -rho_vac g_mn (w = -1, no rest mass, no particle); the current contributes no stress.  Local dof: none (CFG43 H-DIRAC, and E3 below).")
R.finish()
