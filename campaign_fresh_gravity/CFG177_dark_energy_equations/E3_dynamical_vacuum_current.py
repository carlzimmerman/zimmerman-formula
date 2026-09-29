#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
E3 -- the minimal addition that makes the vacuum current PHYSICAL: CFG43's HT action plus the 3-form mass term (dual form), its field
equations, the Koivisto-Nunes dual identities, the Dirac count, ghost/gradient stability, and its background cosmology (w(z), growth).

THE ACTION (c = 1, Mp2 = M_P^2; t^m = T^m/sqrt(-g); U = -(sigma/2) g_mn t^m t^n, the dual of a 3-form mass term V(A^2), A^2 = -6 t^2):
  S = Int d^4x { sqrt(-g)[(Mp2/2) R - Mp2 Lambda - rho(n; Lambda) - U] + Mp2 Lambda d_m T^m + J^m d_m theta },
  sigma(Lambda) = s Mp2 Lambda^2.   Dimensional analysis: sigma has mass dimension 6; built from M_P and the HT field alone it is
  s M_P^(6-2b) Lambda^b; b = 2 is the only power whose dimensionless slope today is O(1) (b = 0, 1 need s ~ 1e-240, 1e-120; b = 3 gives
  a slope ~ sqrt(s) 1e-60).  s is a NEW pure number (G4).  Declared illustration (FROZEN_QUESTION, not scanned): s = kappa^2, i.e. lambda = 1/2.

MUTATE=1  s < 0 (s = -kappa^2): the ghost sign; E3-HEALTH must fail (the background is integrated on the mutated, phantom-signed action).
MUTATE=2  s = 0 (the HT limit): the current is gauge again; the Dirac count must fall back to CFG43's 2N + 2 and w = -1 (E3-DIRAC, E3-BG fail).
"""
import os
import sys
import math
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import E_common as C

R = C.Run("E3_dynamical_vacuum_current")
P, check = R.P, R.check
M = C.MUTATE
P(__doc__)
S_VAL = {0: C.KAPPA ** 2, 1: -C.KAPPA ** 2, 2: 0.0}[M]
P("MUTATE mode = %d ; s = %g" % (M, S_VAL))
R.num("s", S_VAL)

t = sp.Symbol('t', real=True)
Mp2, s_, m, eps, nus = sp.symbols('Mp2 s m epsilon nu_s', positive=True)
MP = sp.sqrt(Mp2)

# ============================================================================================ A: FRW minisuperspace
R.banner("A  FLAT-FRW MINISUPERSPACE (sympy Euler-Lagrange): the vacuum current's equations, Friedmann, and the canonical scalar they hide")
a = sp.Function('a')(t); N = sp.Function('N')(t); Lam = sp.Function('Lam')(t); T0 = sp.Function('T0')(t)
J0 = sp.Function('J0')(t); thf = sp.Function('th')(t)
rhoG = sp.Function('rho')
sigF = sp.Function('sigma')                                        # generic sigma(Lambda) for the structure
n_of = J0 / a ** 3
L_gen = (-3 * Mp2 * a * a.diff(t) ** 2 / N - N * a ** 3 * Mp2 * Lam + Mp2 * Lam * T0.diff(t)
         - N * sigF(Lam) * T0 ** 2 / (2 * a ** 3) - N * a ** 3 * rhoG(n_of, Lam) + J0 * thf.diff(t))
E = dict(zip(['a', 'N', 'Lam', 'T', 'J', 'th'], [e.lhs for e in euler_equations(L_gen, [a, N, Lam, T0, J0, thf], t)]))
T0sol = sp.solve(sp.Eq(E['T'], 0), T0)[0]
T0_ok = sp.simplify(T0sol + Mp2 * a ** 3 * Lam.diff(t) / (N * sigF(Lam))) == 0
# Friedmann (lapse eq.) with T0 eliminated: 3 Mp2 H^2 = Mp2 Lambda + Mp2^2 Lambda'^2/(2 sigma) + rho
H_ = sp.Symbol('H')
EN = sp.simplify(E['N'].subs(T0, T0sol).subs(N, 1).subs(a.diff(t), H_ * a) / a ** 3)
fr_ok = sp.simplify(EN - (3 * Mp2 * H_ ** 2 - Mp2 * Lam - Mp2 ** 2 * Lam.diff(t) ** 2 / (2 * sigF(Lam)) - rhoG(n_of, Lam))) == 0
# flow energy: sigma T0^2/(2 a^6) = Mp2^2 Lam'^2/(2 sigma)  (= phi'^2/2 for sigma = s Mp2 Lam^2, phi = (M_P/sqrt s) ln Lam)
flow_E = sp.simplify((sigF(Lam) * T0sol ** 2 / (2 * a ** 6)).subs(N, 1))
phi_dot = MP * Lam.diff(t) / (sp.sqrt(s_) * Lam)
flowE_ok = sp.simplify(flow_E.subs(sigF(Lam), s_ * Mp2 * Lam ** 2) - phi_dot ** 2 / 2) == 0
# the reduced Lagrangian: integrate Mp2 Lam T0' by parts, eliminate the auxiliary T0, compare with a canonical scalar
L_ibp = L_gen - Mp2 * Lam * T0.diff(t) - Mp2 * Lam.diff(t) * T0
L_red = sp.simplify(L_ibp.subs(T0, T0sol).subs(sigF(Lam), s_ * Mp2 * Lam ** 2))
L_scal = (-3 * Mp2 * a * a.diff(t) ** 2 / N + N * a ** 3 * (phi_dot ** 2 / (2 * N ** 2) - Mp2 * Lam) - N * a ** 3 * rhoG(n_of, Lam) + J0 * thf.diff(t))
red_ok = sp.simplify(L_red - L_scal) == 0
# the Gauss law in FRW: (1/(N a^3)) T0' = 1 + rho_Lambda/Mp2 + sigma'(Lambda) T0^2/(2 Mp2 a^6)  <=>  nabla.t = 1 - P/rho_vac - (sigma'/(2 Mp2)) t^2
Tdot = sp.solve(sp.Eq(E['Lam'], 0), T0.diff(t))[0]
gauss_ok = sp.simplify(Tdot / (N * a ** 3) - (1 + sp.diff(rhoG(n_of, Lam), Lam) / Mp2
                                             + sp.diff(sigF(Lam), Lam) * T0 ** 2 / (2 * Mp2 * a ** 6))) == 0
check("E3-FRW", "Euler-Lagrange on the minisuperspace: T0 = -Mp2 a^3 Lambda'/(N sigma) (the current is locked to Lambda's rate); Friedmann 3 Mp2 H^2 = Mp2 Lambda + "
      "Mp2^2 Lambda'^2/(2 sigma) + rho; the flow's energy sigma (t^0)^2/2 = phi'^2/2; after eliminating T0 the action IS a canonical scalar phi = (M_P/sqrt s) ln Lambda "
      "with V(phi) = Mp2 Lambda = Mp2 Lambda_* e^{sqrt(s) phi/M_P}; the Lambda equation is the Gauss law (1/N a^3) T0' = 1 - P/rho_vac + (sigma'/2Mp2)(t^0)^2",
      "T0: %s; Friedmann: %s; flow energy = phi'^2/2: %s; reduced Lagrangian == canonical scalar: %s; Gauss law: %s" % (T0_ok, fr_ok, flowE_ok, red_ok, gauss_ok),
      T0_ok and fr_ok and flowE_ok and red_ok and gauss_ok,
      "the vacuum 'flowing in time' is the dark energy's kinetic energy; in the HT limit s -> 0 the flow carries no energy (E3-BG)")

# covariant check (flat space, generic phi(t,x,y,z)): nabla^m(d_m Lambda/(s Lambda^2)) + s Lambda (d Lambda)^2/(s Lambda^2)^2 == box(phi)/(sqrt(s) M_P Lambda)
Xc = sp.symbols('t x y z', real=True)
eta = sp.diag(-1, 1, 1, 1)
phi = sp.Function('phi')(*Xc)
Lamc = sp.exp(sp.sqrt(s_) * phi / MP)
tl = [sp.diff(Lamc, Xc[i]) / (s_ * Lamc ** 2) for i in range(4)]                  # t_m = Mp2 d_m Lambda/sigma
divt = sum(eta[i, i] * sp.diff(tl[i], Xc[i]) for i in range(4))
t2c = sum(eta[i, i] * tl[i] ** 2 for i in range(4))
box = sum(eta[i, i] * sp.diff(phi, Xc[i], 2) for i in range(4))
cov_ok = sp.simplify(divt + s_ * Lamc * t2c - box / (sp.sqrt(s_) * MP * Lamc)) == 0
check("E3-COV", "covariantly: t_m = d_m Lambda/(s Lambda^2) = -d_m(1/(s Lambda)) and nabla.t = 1 - P/rho_vac - s Lambda t^2 are together EXACTLY  box(phi) = V'(phi) - (sqrt(s)/M_P) P "
      "(identity nabla.t + s Lambda t^2 = box(phi)/(sqrt(s) M_P Lambda) for generic phi)", "identity: %s" % cov_ok, cov_ok,
      "the vacuum flows down its own density gradient (a Darcy law); the unimodular clock becomes 1/(s Lambda)")

# ============================================================================================ B: the 3-form dual identities (Koivisto-Nunes relation)
R.banner("B  THE 3-FORM DUAL: A_npq = eps_mnpq t^m gives A^2 = -6 t^2 (mass term <-> U); a quadratic W(Lambda) is the -F^2/48 kinetic term; HT's LINEAR W fixes *F")
import itertools
tv = sp.symbols('t0:4', real=True)
tup = [tv[i] for i in range(4)]
tdn = [eta[i, i] * tup[i] for i in range(4)]
Adn = {(n, p, q): sum(sp.LeviCivita(mm, n, p, q) * (-1) * tup[mm] for mm in range(4)) for n, p, q in itertools.product(range(4), repeat=3)}   # eps_{mnpq} = -eps^{mnpq} (Lorentzian)
Aup = {k: eta[k[0], k[0]] * eta[k[1], k[1]] * eta[k[2], k[2]] * v for k, v in Adn.items()}
A2 = sp.simplify(sum(Adn[k] * Aup[k] for k in Adn))
t2v = sum(tup[i] * tdn[i] for i in range(4))
A2_ok = sp.simplify(A2 + 6 * t2v) == 0
psi, L_ = sp.symbols('psi Lambda_', real=True)
Wq = Mp2 ** 2 * L_ ** 2 / 2
leg = sp.solve(sp.diff(Mp2 * L_ * psi - Wq, L_), L_)[0]
leg_val = sp.simplify((Mp2 * L_ * psi - Wq).subs(L_, leg))
epsF = sum(sp.LeviCivita(*i) * (-1) * sp.LeviCivita(*i) for i in itertools.product(range(4), repeat=4))   # eps_{mnpq} eps^{mnpq}
F2term = sp.simplify(-sp.Rational(1, 48) * psi ** 2 * epsF)
kn_ok = A2_ok and sp.simplify(leg_val - psi ** 2 / 2) == 0 and sp.simplify(F2term - psi ** 2 / 2) == 0
check("E3-KN", "Lorentzian identities: A_npq A^npq = -6 t_m t^m (so a 3-form mass term V(A^2) is exactly a U(t^2)); Legendre: max_Lambda[Mp2 Lambda psi - Mp2^2 Lambda^2/2] = psi^2/2 "
      "= -F^2/48 for F = psi eps; i.e. Koivisto-Nunes' massive 3-form (from memory, unverified) = this family with QUADRATIC W; CFG43's HT = LINEAR W (Lambda then "
      "enforces *F = 1 - P/rho_vac); the minimal promotion keeps CFG43's linear W and adds only U",
      "A^2 + 6 t^2 = %s; Legendre value %s; -F^2/48 = %s" % (sp.simplify(A2 + 6 * t2v), leg_val, F2term), kn_ok)

# ============================================================================================ C: Dirac count on a periodic lattice
R.banner("C  DIRAC CONSTRAINT COUNT on a periodic 1-D lattice (CFG43's method, re-implemented): fluid + HT, and fluid + HT + U")
NL, hl = 3, 1


def rho_eos(n_, L_):
    x_ = m * n_ / (nus * Mp2 * L_)
    return m * n_ + eps * Mp2 * L_ * x_ * sp.atan(x_)


def build(mode, sval):
    mk = lambda nm: [sp.Symbol('%s_%d' % (nm, j), real=True) for j in range(NL)]
    Qs, Ls, T1s, J0s, J1s, ths = (mk(nm) for nm in ('Q', 'Lam', 'T1', 'J0', 'J1', 'th'))
    Ps, pL, pT1, p0, p1, pith = (mk(nm) for nm in ('P', 'pLam', 'pT1', 'p0', 'p1', 'pi'))
    Hc = 0
    for j in range(NL):
        jp = (j + 1) % NL
        nj = sp.sqrt(J0s[j] ** 2 - J1s[j] ** 2)
        Hc += rho_eos(nj, Ls[j]) + Mp2 * Ls[j] - J1s[j] * (ths[jp] - ths[j]) / hl - Mp2 * Ls[j] * (T1s[jp] - T1s[j]) / hl
        if mode == 'HT+U':
            Hc += (sval * Mp2 * Ls[j] ** 2 / 2) * (Qs[j] ** 2 - T1s[j] ** 2)          # U = -(sigma/2) t^2, t^2 = -Q^2 + T1^2 (flat 1+1)
    coords = Qs + Ls + T1s + J0s + J1s + ths
    moms = Ps + pL + pT1 + p0 + p1 + pith
    prim, sec = [], []
    for j in range(NL):
        prim += [p0[j], p1[j], pith[j] - J0s[j], pL[j], pT1[j], Ps[j] - Mp2 * Ls[j]]
        sec += [sp.diff(Hc, J1s[j]), sp.diff(Hc, T1s[j])]
    return coords, moms, Hc, prim, sec, dict(Q=Qs, L=Ls, T1=T1s, J0=J0s, J1=J1s, th=ths, P=Ps, pL=pL, pT1=pT1, p0=p0, p1=p1, pi=pith)


def dirac(mode, sval, seed=5):
    coords, moms, Hc, prim, sec, S = build(mode, sval)
    cons = prim + sec
    nq = len(coords)
    allv = coords + moms
    pars = [Mp2, m, eps, nus]
    vals = {Mp2: 1.3, m: 0.9, eps: float(C.EPS), nus: 7.0}
    rng = np.random.default_rng(seed)
    Lv = 0.8 * np.ones(NL) if mode == 'HT' else 0.8 + 0.05 * rng.normal(size=NL)
    for j in range(NL):
        vals[S['th'][j]] = rng.normal()
        vals[S['Q'][j]] = rng.normal()
        vals[S['L'][j]] = float(Lv[j])
        vals[S['P'][j]] = 1.3 * float(Lv[j])
        for k in ('pL', 'pT1', 'p0', 'p1'):
            vals[S[k][j]] = 0.0
    for j in range(NL):                                        # T1 on the secondary surface d H/d T1 = 0
        jm = (j - 1) % NL
        if mode == 'HT':
            vals[S['T1'][j]] = rng.normal()
        else:
            vals[S['T1'][j]] = 1.3 * (Lv[j] - Lv[jm]) / hl / (sval * 1.3 * Lv[j] ** 2) if sval != 0 else rng.normal()
    nvals = rng.uniform(0.5, 2.0, NL)
    nn_, LL_ = sp.symbols('nn_ LL_', positive=True)
    drho = sp.lambdify((nn_, LL_), sp.diff(rho_eos(nn_, LL_), nn_).subs({Mp2: 1.3, m: 0.9, eps: float(C.EPS), nus: 7.0}), 'math')
    for j in range(NL):                                        # J1 on the fluid's secondary surface (CFG43's construction)
        jp = (j + 1) % NL
        rn = drho(float(nvals[j]), float(Lv[j]))
        J1v = -float(nvals[j]) * (vals[S['th'][jp]] - vals[S['th'][j]]) / rn
        vals[S['J1'][j]] = J1v
        vals[S['J0'][j]] = math.sqrt(nvals[j] ** 2 + J1v ** 2)
        vals[S['pi'][j]] = vals[S['J0'][j]]
    args = [float(vals[v]) for v in allv] + [float(vals[p]) for p in pars]
    Jc = sp.Matrix([[sp.diff(c, v) for v in allv] for c in cons])
    Jn = np.array(sp.lambdify(allv + pars, Jc, 'numpy')(*args), dtype=float)
    cval = np.array(sp.lambdify(allv + pars, cons, 'numpy')(*args), dtype=float)
    dHn = np.array(sp.lambdify(allv + pars, [sp.diff(Hc, v) for v in allv], 'numpy')(*args), dtype=float)
    Om = np.zeros((2 * nq, 2 * nq))
    for i in range(nq):
        Om[i, nq + i], Om[nq + i, i] = 1.0, -1.0
    with np.errstate(all='ignore'):                            # Accelerate BLAS raises spurious FP flags in matmul (as CFG43); finiteness asserted
        Mn = Jn @ Om @ Jn.T
        vec = Jn @ Om @ dHn
    assert np.isfinite(Mn).all() and np.isfinite(vec).all() and np.isfinite(Jn).all()
    svJ = np.linalg.svd(Jn, compute_uv=False)
    K = int((svJ > 1e-9 * svJ[0]).sum())
    svM = np.linalg.svd(Mn, compute_uv=False)
    Sc = int((svM > 1e-9 * max(svM[0], 1e-300)).sum())
    u = np.linalg.lstsq(Mn[:, :len(prim)], -vec, rcond=None)[0]
    return dict(nq=nq, K=K, S=Sc, F=K - Sc, D=2 * nq - 2 * (K - Sc) - Sc, closure=float(np.linalg.norm(Mn[:, :len(prim)] @ u + vec)),
                maxC=float(np.abs(cval).max()))


r_ht = dirac('HT', 0.0)
r_u = dirac('HT+U', S_VAL) if S_VAL != 0 else dirac('HT', 0.0)
for nm_, rr in (("HT (CFG43)", r_ht), ("HT + U (now)" if S_VAL != 0 else "HT + U with s = 0 (= HT)", r_u)):
    P("    %-26s dim=%3d K=%3d S=%3d F=%3d D=%3d closure=%.1e max|C|=%.1e" % (nm_, 2 * rr['nq'], rr['K'], rr['S'], rr['F'], rr['D'], rr['closure'], rr['maxC']))
ht_ok = r_ht['D'] == 2 * NL + 2 and r_ht['closure'] < 1e-8
u_ok = r_u['D'] == 4 * NL and r_u['F'] == 0 and r_u['closure'] < 1e-8 and r_u['maxC'] < 1e-9
check("E3-DIRAC", "HT reproduces CFG43 (D = 2N + 2: fluid + one GLOBAL pair); with the mass term every constraint is second class and D = 4N: the fluid's sound mode plus "
      "ONE LOCAL dark-energy mode per site (the longitudinal part of the current; its curl part is zero on shell), no tertiary constraint",
      "HT: D = %d (target %d); HT+U: D = %d (target %d), F = %d, closure %.1e" % (r_ht['D'], 2 * NL + 2, r_u['D'], 4 * NL, r_u['F'], r_u['closure']),
      ht_ok and u_ok, "MUTATE=2 (s = 0): back to the gauge current, no local mode" if M == 2 else "")
R.num("dirac", dict(HT=r_ht, HTU=r_u))

# ============================================================================================ D: health (ghost, gradient), c_s
R.banner("D  GHOST AND GRADIENT STABILITY: the reduced Hamiltonian after solving the second-class constraints, and the dispersion relation")
Qc, Pc, T1c, kx, w_ = sp.symbols('Q P T1 k omega', real=True)
Lb = sp.Symbol('Lbar', positive=True)
sig_b = sp.Symbol('sigma_b', real=True)                          # sigma evaluated on the background Lambda
# continuum 1+1, flat: H = P(1 - d_x T1) + (sigma/2)(Q^2 - T1^2); T1 from dH/dT1 = 0 -> T1 = d_x P/sigma ; Lambda = P/Mp2
dP = sp.Symbol('dP', real=True)
Hdens = Pc + T1c * dP + (sig_b / 2) * (Qc ** 2 - T1c ** 2)               # after integrating -P d_x T1 by parts
T1star = sp.solve(sp.diff(Hdens, T1c), T1c)[0]
Hred = sp.simplify(Hdens.subs(T1c, T1star))
Hred_ok = sp.simplify(Hred - (Pc + sig_b * Qc ** 2 / 2 + dP ** 2 / (2 * sig_b))) == 0
# dispersion: Qdot = dH/dP = -d_x^2 P / sigma ; Pdot = -sigma Q  => P'' = d_x^2 P  (plane wave: omega^2 = k^2)
# plane waves dQ = Q0 e^{i(kx - wt)}, dP = P0 e^{i(kx - wt)} in Hamilton's equations  Qdot = dH/dP = 1 - d_x^2 P/sigma,  Pdot = -dH/dQ = -sigma Q
Q0, P0 = sp.symbols('Q0 P0')
Hfun = Pc + sig_b * Qc ** 2 / 2                                            # the local part; the gradient part gives -d_x^2 P/sigma -> +k^2 P0/sigma
eqs = [sp.Eq(-sp.I * w_ * Q0, kx ** 2 * P0 / sig_b), sp.Eq(-sp.I * w_ * P0, -sp.diff(Hfun, Qc).subs(Qc, Q0))]
Msys = sp.Matrix([[sp.diff(e.lhs - e.rhs, v) for v in (Q0, P0)] for e in eqs])
disp = sp.solve(sp.Eq(Msys.det(), 0), w_)
cs_ok = len(disp) > 0 and all(sp.simplify(d ** 2 - kx ** 2) == 0 for d in disp)
sig_num = S_VAL * 1.3 * 0.8 ** 2
kin_coef, grad_coef = sig_num / 2, (1 / (2 * sig_num) if sig_num != 0 else float('inf'))
health = sig_num > 0
check("E3-HEALTH", "reduced Hamiltonian density H = rho_vac + (sigma/2) Q^2 + (d_x rho_vac)^2/(2 sigma) (Q = the unimodular clock density, conjugate to rho_vac = Mp2 Lambda): "
      "kinetic and gradient energies are both positive iff sigma = s Mp2 Lambda^2 > 0; omega^2 = k^2 (c_s = 1, causal)",
      "H_red identity: %s; c_s^2 = 1: %s; sigma on the background = %.4g: kinetic coefficient %.4g, gradient coefficient %.4g" % (Hred_ok, cs_ok, sig_num, kin_coef, grad_coef),
      Hred_ok and cs_ok and health,
      "MUTATE=1 (s < 0): both signs flip -- a ghost relative to gravity and matter" if M == 1 else
      ("MUTATE=2 (s = 0): no local mode at all (the HT limit)" if M == 2 else "canonical field phi = rho_vac/sqrt(sigma)-type, the time flow Q is its momentum"))

# ============================================================================================ E: background cosmology
R.banner("E  BACKGROUND COSMOLOGY: thawing from rest at a = 1e-6; flat; Omega_m = %.4f, Omega_r = 9.2e-5; units H0 = 1, M_P = 1 (rho_crit0 = 3)" % C.OMEGA_M)
OM, ORAD = C.OMEGA_M, 9.2e-5
lam = math.sqrt(abs(S_VAL))
zeta = 1.0 if S_VAL >= 0 else -1.0                              # sign of the kinetic term (MUTATE=1: ghost/phantom)


def run_bg(lam_, Vstar, zeta_=1.0, dense=False):
    """y = [psi, psi_N, delta, delta_N, logTc]; N = ln a.  psi = phi/M_P; V = Vstar exp(lam psi)."""
    def H2(N_, y):
        a_ = math.exp(N_)
        V = Vstar * math.exp(lam_ * y[0])
        return (3 * OM * a_ ** -3 + 3 * ORAD * a_ ** -4 + V) / (3 - zeta_ * y[1] ** 2 / 2)

    def rhs(N_, y):
        a_ = math.exp(N_)
        h2 = H2(N_, y)
        rm, rr = 3 * OM * a_ ** -3, 3 * ORAD * a_ ** -4
        V = Vstar * math.exp(lam_ * y[0])
        eps_h = (rm + 4 * rr / 3 + zeta_ * h2 * y[1] ** 2) / (2 * h2)          # -Hdot/H^2
        psiNN = -(3 - eps_h) * y[1] - lam_ * V / (zeta_ * h2)
        Om_a = rm / (3 * h2)
        dNN = -(2 - eps_h) * y[3] + 1.5 * Om_a * y[2]
        return [y[1], psiNN, y[3], dNN]

    N0 = math.log(1e-6)
    y0 = [0.0, 0.0, 1e-6, 1e-6]
    sol = solve_ivp(rhs, (N0, 0.0), y0, rtol=1e-10, atol=1e-13, dense_output=True, method='LSODA')
    return sol, H2


def omega_de0(lam_, Vstar, zeta_=1.0):
    sol, H2 = run_bg(lam_, Vstar, zeta_)
    y = sol.y[:, -1]
    h2 = H2(0.0, y)
    return h2 - 1.0                                             # flatness: H0 = 1


def fit_V(lam_, zeta_=1.0):
    return brentq(lambda V: omega_de0(lam_, V, zeta_), 0.5, 20.0, xtol=1e-12)


def w_of(sol, H2, lam_, Vstar, N_, zeta_=1.0):
    y = sol.sol(N_)
    h2 = H2(N_, y)
    K = zeta_ * h2 * y[1] ** 2 / 2
    V = Vstar * math.exp(lam_ * y[0])
    return (K - V) / (K + V)


def growth_lcdm():
    OL = 1 - OM - ORAD

    def rhs(N_, y):
        a_ = math.exp(N_)
        h2 = OM * a_ ** -3 + ORAD * a_ ** -4 + OL
        eps_h = (1.5 * OM * a_ ** -3 + 2 * ORAD * a_ ** -4) / h2
        return [y[1], -(2 - eps_h) * y[1] + 1.5 * (OM * a_ ** -3 / h2) * y[0]]
    sol = solve_ivp(rhs, (math.log(1e-6), 0.0), [1e-6, 1e-6], rtol=1e-10, atol=1e-13, method='LSODA')
    return sol.y[0, -1]


D_lcdm = growth_lcdm()
bg = {}
if lam > 0:
    Vs = fit_V(lam, zeta)
    sol, H2 = run_bg(lam, Vs, zeta)
    ws = {("z=%g" % z): w_of(sol, H2, lam, Vs, -math.log(1 + z), zeta) for z in (0, 0.5, 1, 2, 5)}
    da = 1e-4
    wa = -(w_of(sol, H2, lam, Vs, 0.0, zeta) - w_of(sol, H2, lam, Vs, math.log(1 - da), zeta)) / da
    Dq = sol.y[2, -1]
    grat = Dq / D_lcdm
    # Gauss-law residual along the solution: t^0 = -psi_dot/(lam V) (units M_P = 1); (1/a^3) d(a^3 t^0)/dt - 1 - s V (t^0)^2 = 0
    Ns = np.linspace(math.log(0.05), -0.01, 200)
    res = []
    for N_ in Ns:
        def t0f(NN):
            y = sol.sol(NN)
            Hh = math.sqrt(H2(NN, y))
            V = Vs * math.exp(lam * y[0])
            return -lam * (Hh * y[1]) / (S_VAL * V), Hh, V                  # t^0 = -Lambda_dot/(s Lambda^2), Lambda = V (M_P = 1)
        e = 1e-5
        tp, Hp, _ = t0f(N_ + e)
        tm, Hm, _ = t0f(N_ - e)
        t0v, Hh, V = t0f(N_)
        d_a3t = (math.exp(3 * (N_ + e)) * tp - math.exp(3 * (N_ - e)) * tm) / (2 * e) * Hh / math.exp(3 * N_)   # d/dt = H d/dN
        res.append(abs(d_a3t - 1 - S_VAL * V * t0v ** 2))
    gauss_res = max(res)
    bg = dict(w=ws, w0=ws["z=0"], wa=wa, growth_ratio=grat, Vstar=Vs, gauss_residual=gauss_res)
    P("  lambda = sqrt|s| = %.4f, kinetic sign %+d: w(z) = %s; w0 = %.4f, wa = %.4f; D(z=0)/D_LCDM = %.4f; Gauss-law residual along the solution = %.1e"
      % (lam, zeta, {k: round(v, 4) for k, v in ws.items()}, ws["z=0"], wa, grat, gauss_res))
    # the s -> 0 limit (a limit check, not a scan)
    lam_small = 1e-3
    Vs0 = fit_V(lam_small, 1.0)
    sol0, H20 = run_bg(lam_small, Vs0, 1.0)
    w0_small = w_of(sol0, H20, lam_small, Vs0, 0.0, 1.0)
    bg["w0_lambda_1e-3"] = w0_small
    P("  limit check lambda = 1e-3: 1 + w0 = %.2e (-> 0: LCDM)" % (1 + w0_small))
else:
    ws = {"z=0": -1.0}
    bg = dict(w=ws, w0=-1.0, wa=0.0, growth_ratio=1.0, gauss_residual=0.0)
    P("  s = 0: the current carries no energy; w = -1 identically (the HT/LCDM background)")
R.num("background", bg)
# quasi-static clustering of delta phi relative to matter (active densities): 2 (V'/M_P)^2 (a/k)^4 with V' = sqrt(s) V/M_P, V ~ 3 M_P^2 H_L^2
HL_Mpc = C.H_LAMBDA * 3.0856775814913673e22 / C.C_SI
clus = {("k=%g/Mpc" % k): 2 * 9 * abs(S_VAL) * (HL_Mpc / k) ** 4 for k in (0.01, 0.1, 1.0, 30.0)}
bg_ok = (lam > 0) and zeta > 0 and (-1 < bg["w0"] < -0.8) and abs(bg["growth_ratio"] - 1) <= 0.05 and bg["gauss_residual"] < 1e-5 and abs(1 + bg.get("w0_lambda_1e-3", -1)) < 1e-5
check("E3-BG", "background of the promoted dark energy: a thawing exponential quintessence, w0 in (-1, -0.8), linear growth within 5% of LCDM (sub-horizon quintessence does not "
      "cluster: quasi-static active-density ratio 18 s (a H_L/k)^4), the Gauss law satisfied along the numerical solution, and w0 -> -1 as s -> 0",
      "w0 = %.4f, wa = %.4f, D/D_LCDM = %.4f, Gauss residual %.1e; clustering ratio %s" % (bg["w0"], bg["wa"], bg["growth_ratio"], bg["gauss_residual"],
                                                                                        {k: "%.1e" % v for k, v in clus.items()}), bg_ok,
      "G2: background + growth PASS for the declared illustration; the CMB is NOT computed (OPEN); the background current t^mu is along the Hubble flow "
      "(t_m proportional to d_m phi, phi homogeneous); the cold mass Omega_c stays as in candidate B")
R.num("clustering_ratio", clus)
# which Lambda-power b in sigma = s M_P^(6-2b) Lambda^b gives an O(1) slope?  lambda_eff = M_P V'/V = sqrt(s) (Lambda l_P^2)^(b/2 - 1)  (sympy + numbers)
bb_, Ls_, sp_ = sp.symbols('b Lambda_s s_p', positive=True)
Lam_f = sp.Function('Lam')(t)
sigma_b = sp_ * Mp2 ** (3 - bb_) * Lam_f ** bb_
kin = sp.simplify(Mp2 ** 2 / (2 * sigma_b))                              # coefficient of Lambda'^2 in the reduced action
dphi_dL = sp.sqrt(2 * kin)                                                 # canonical: phi'^2/2 = kin Lambda'^2
lam_eff = sp.simplify((MP * Mp2 / (Mp2 * Lam_f * dphi_dL)).subs(Lam_f, Ls_))
lam_eff_ok = sp.simplify(lam_eff - sp.sqrt(sp_) * (Ls_ / Mp2) ** (bb_ / 2 - 1)) == 0
hbar = 1.054571817e-34
LlP2 = C.LAMBDA_SI * 8 * math.pi * C.G_SI * hbar / C.C_SI ** 3          # Lambda in reduced-Planck units
lam_tab = {("b=%d" % b): "sqrt(s) x %.2e" % (LlP2 ** (b / 2 - 1)) for b in (0, 1, 2, 3)}
check("E3-TIEPOWER", "sigma = s M_P^(6-2b) Lambda^b (no dimensionful constant beyond M_P and the HT field): the dark energy's slope today is lambda_eff = sqrt(s) (Lambda/M_P^2)^(b/2-1); "
      "only b = 2 gives an O(1) slope for an O(1) number s, so s is a genuinely new pure number (it cannot be removed by choosing b)",
      "symbolic form: %s; Lambda l_P^2 = %.3e; lambda_eff by b: %s" % (lam_eff_ok, LlP2, lam_tab), lam_eff_ok, load_bearing=False)
R.num("lambda_eff_by_power", lam_tab)
P("")
P("  THE PROMOTED DARK ENERGY, AS DERIVED:  t_m = d_m Lambda/(s Lambda^2)  [the vacuum flows down its own density gradient];  nabla.t = 1 - P/rho_vac - s Lambda t^2;")
P("  equivalently box(phi) = V'(phi) - (sqrt(s)/M_P) P,  phi = (M_P/sqrt s) ln(Lambda/Lambda_0),  V = rho_vac,0 e^{sqrt(s) phi/M_P};  T_mn = d_m phi d_n phi - g_mn[(d phi)^2/2 + V];")
P("  the flow's energy density = (1 + w) rho_DE/2; one local dof; healthy iff s > 0; c_s = 1.")
R.finish()
