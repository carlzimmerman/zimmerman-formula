#!/usr/bin/env python3
"""CMB2 / D3: does the preferred foliation (tau, n_m, Q, P) enter the photon-baryon physics before recombination
other than through the metric potentials and the background H(z)?  (criteria: FROZEN_CRITERIA.md, D3 + MUTATE-gravity)

Sections (all sympy, exact unless stated):
  S1  matter EL equations from S_m alone contain no khronon field (scalar matter, dust worldline, photon worldline)
  S1b Noether identity for S_m alone: nabla_m T^m_n = +(EL_chi/sqrtg) d_n chi, so matter conservation is separate on matter
      shell; with the Bianchi identity the khronon/P sector stress is separately conserved (QX17 E6, QX17A)
  S2  linear Newtonian-gauge photon / baryon equations from nabla_m T^mn = 0 + Thomson drag; free symbols checked;
      tight-coupling c_s^2 = 1/(3(1+R)) derived
  S3  linear anisotropic stress of the khronon / P sector (v3s blend and AC2q) in a local frame, both P regimes
      (P first order: |E| << a0; P saturated: K|P| -> a0); slip bound at z 1100, both footings
  S4  clock: S_m has no tau dependence (functional derivative zero)
  S5  MUTATE-gravity: L_int = beta n_m u^m added to the baryon worldline action; the check must find tau
Run:  nice -n 15 python3 d3_frame.py > d3_frame.out   (writes d3_frame.json)
"""
import json, os, sys
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = {"lane": "CMB2", "dof": "D3", "criteria": "FROZEN_CRITERIA.md", "adopts": "nothing",
       "kappa": "1/2 FITTED; not theory closed"}
checks = {}

def log(*a):
    print(*a); sys.stdout.flush()

t, x, y, z = sp.symbols('t x y z', real=True)
X4 = [t, x, y, z]
tau = sp.Function('tau')(t, x)          # khronon, present in the namespace for every check
KHRONON_FUNCS = {'tau'}

def has_khronon(expr):
    expr = sp.sympify(expr)
    names = {f.func.__name__ for f in expr.atoms(sp.Function) if hasattr(f, 'func')}
    names |= {str(s) for s in expr.free_symbols}
    return bool(names & (KHRONON_FUNCS | {'Q', 'n0', 'n1', 'lam', 'Pfield'}))

# ---------------------------------------------------------------- S1: matter EL from S_m alone
log("== S1: Euler-Lagrange of S_m (minimal coupling) ==")
N = sp.Function('N', positive=True)(t, x)
b = sp.Function('b', positive=True)(t, x)
g = sp.diag(-N**2, b**2, b**2, b**2)
ginv = g.inv()
sqrtg = N * b**3
chi = sp.Function('chi')(t, x)
V = sp.Function('V')
dchi = [sp.diff(chi, v) for v in X4]
Xk = -sp.Rational(1, 2) * sum(ginv[m, n] * dchi[m] * dchi[n] for m in range(4) for n in range(4))
Lm = sqrtg * (Xk - V(chi))                      # scalar matter proxy (irrotational perfect fluid family)
EL_chi = sp.euler_equations(Lm, [chi], [t, x])[0].lhs
checks['S1_scalar_EL_no_khronon'] = not has_khronon(EL_chi)
log("  scalar EL khronon-free:", checks['S1_scalar_EL_no_khronon'])

# S1b Noether identity: nabla_m T^m_n + EL_chi/sqrtg * d_n chi = 0  (identically, any metric N,b)
Gam = [[[sp.Rational(1, 2) * sum(ginv[a, d] * (sp.diff(g[d, bb], X4[c]) + sp.diff(g[d, c], X4[bb]) - sp.diff(g[bb, c], X4[d]))
                                  for d in range(4)) for c in range(4)] for bb in range(4)] for a in range(4)]
Lsc = Xk - V(chi)
T_lo = sp.Matrix(4, 4, lambda m, n: dchi[m] * dchi[n] + g[m, n] * Lsc)
T_mix = ginv * T_lo                                     # T^m_n
def div_mixed(T):
    res = []
    for n in range(4):
        s = sum(sp.diff(T[m, n], X4[m]) for m in range(4))
        s += sum(Gam[m][m][l] * T[l, n] for m in range(4) for l in range(4))
        s -= sum(Gam[l][m][n] * T[m, l] for m in range(4) for l in range(4))
        res.append(s)
    return res
divT = div_mixed(T_mix)
# EL_chi from euler_equations has sign: dL/dchi - d_m dL/d(d_m chi) = -sqrtg (box chi - V') ... identity:
noether_p = [sp.simplify(divT[n] + (EL_chi / sqrtg) * dchi[n]) for n in range(2)]
noether = [sp.simplify(divT[n] - (EL_chi / sqrtg) * dchi[n]) for n in range(2)]
log('  (sign check: with + sign residual zero?', all(e == 0 for e in noether_p), ')')
checks['S1b_noether_identity'] = all(e == 0 for e in noether)
log("  nabla_m T^m_n = +(EL/sqrtg) d_n chi identically (EL as sympy euler_equations lhs):", checks['S1b_noether_identity'], noether)

# dust (baryon) and photon worldlines: EL only g
lam_ = sp.symbols('lambda_', real=True)
tw = sp.Function('tw')(lam_); xw = sp.Function('xw')(lam_)
Nw = sp.Function('N', positive=True)(tw, xw); bw = sp.Function('b', positive=True)(tw, xw)
tauw = sp.Function('tau')(tw, xw)
m_, beta, e_ = sp.symbols('m beta e', positive=True)
tdot, xdot = sp.diff(tw, lam_), sp.diff(xw, lam_)
L_dust = -m_ * sp.sqrt(Nw**2 * tdot**2 - bw**2 * xdot**2)
L_phot = (-Nw**2 * tdot**2 + bw**2 * xdot**2) / (2 * e_)
EL_dust = [eq.lhs for eq in sp.euler_equations(L_dust, [tw, xw], lam_)]
EL_phot = [eq.lhs for eq in sp.euler_equations(L_phot, [tw, xw], lam_)]
checks['S1_dust_worldline_no_khronon'] = not any(has_khronon(e) for e in EL_dust)
checks['S1_photon_worldline_no_khronon'] = not any(has_khronon(e) for e in EL_phot)
log("  dust (baryon Euler) EL khronon-free:", checks['S1_dust_worldline_no_khronon'])
log("  photon geodesic (Liouville operator of the Boltzmann hierarchy) EL khronon-free:", checks['S1_photon_worldline_no_khronon'])

# ---------------------------------------------------------------- S2: linear Newtonian-gauge equations
log("== S2: linear Newtonian gauge, nabla_m T^mn = 0 per fluid + Thomson drag ==")
eta, X = sp.symbols('eta X', real=True)
eps = sp.symbols('epsilon', positive=True)
a = sp.Function('a', positive=True)(eta)
Psi = sp.Function('Psi')(eta, X); Phi = sp.Function('Phi')(eta, X)
XX = [eta, X, y, z]
gN = sp.diag(-a**2 * (1 + 2 * eps * Psi), a**2 * (1 - 2 * eps * Phi), a**2 * (1 - 2 * eps * Phi), a**2 * (1 - 2 * eps * Phi))
gNi = gN.inv()
GamN = [[[sp.Rational(1, 2) * sum(gNi[aa, d] * (sp.diff(gN[d, bb], XX[c]) + sp.diff(gN[d, c], XX[bb]) - sp.diff(gN[bb, c], XX[d]))
                                   for d in range(4)) for c in range(4)] for bb in range(4)] for aa in range(4)]

def fluid_eqs(w, name):
    rho0 = sp.Function('rho0_' + name, positive=True)(eta)
    dl = sp.Function('delta_' + name)(eta, X)
    v = sp.Function('v_' + name)(eta, X)
    rho = rho0 * (1 + eps * dl); p = w * rho
    u = [ (1 - eps * Psi) / a, eps * v / a, 0, 0 ]
    T = sp.Matrix(4, 4, lambda m, n: (rho + p) * u[m] * u[n] + p * gNi[m, n])
    div = []
    for n in range(2):
        s = sum(sp.diff(T[m, n], XX[m]) for m in range(4))
        s += sum(GamN[m][m][l] * T[l, n] for m in range(4) for l in range(4))
        s += sum(GamN[n][m][l] * T[m, l] for m in range(4) for l in range(4))
        div.append(sp.expand(sp.series(s, eps, 0, 2).removeO()))
    return rho0, dl, v, div

H = sp.Function('Hc')(eta)   # conformal Hubble a'/a
res_S2 = {}
eqs = {}
for w, name in [(sp.Rational(1, 3), 'g'), (0, 'b')]:
    rho0, dl, v, div = fluid_eqs(w, name)
    # background: rho0' = -3 H (1+w) rho0
    bg = sp.solve(div[0].coeff(eps, 0), sp.diff(rho0, eta))[0]
    e0 = sp.simplify(div[0].coeff(eps, 1).subs(sp.diff(rho0, eta), bg).subs(sp.diff(a, eta), H * a))
    e1 = sp.simplify(div[1].coeff(eps, 1).subs(sp.diff(rho0, eta), bg).subs(sp.diff(a, eta), H * a))
    ddl = sp.solve(e0, sp.diff(dl, eta))[0]
    dv = sp.solve(e1, sp.diff(v, eta))[0]
    eqs[name] = (dl, v, sp.simplify(ddl), sp.simplify(dv))
    log(f"  {name}: delta' =", eqs[name][2]); log(f"  {name}: v'     =", eqs[name][3])
    res_S2[name] = {"delta_prime": str(eqs[name][2]), "v_prime": str(eqs[name][3])}
# Thomson drag: collision term evaluated in the baryon rest frame of g; d t_proper = a d eta
taup, R = sp.symbols('taudot_T R', positive=True)   # taudot_T = a n_e sigma_T (conformal opacity), NOT the khronon
vg_p = eqs['g'][3] + taup * (eqs['b'][1] - eqs['g'][1])
vb_p = eqs['b'][3] + (taup / R) * (eqs['g'][1] - eqs['b'][1])
system = [eqs['g'][2], vg_p, eqs['b'][2], vb_p]
checks['S2_linear_system_no_khronon'] = not any(has_khronon(e) for e in system)
fs = set().union(*[sp.sympify(e).free_symbols for e in system])
fn = set().union(*[{f.func.__name__ for f in sp.sympify(e).atoms(sp.Function)} for e in system])
log("  free symbols:", sorted(map(str, fs)), " functions:", sorted(fn))
log("  linear photon-baryon system khronon-free:", checks['S2_linear_system_no_khronon'])
OUT['S2_symbols'] = {"symbols": sorted(map(str, fs)), "functions": sorted(fn)}
# tight coupling, plane wave: v = -i theta/k ... use theta = d_X v (real space), delta = delta_k e^{ikX}
k = sp.symbols('k', positive=True)
dg, th, ps, ph = [sp.Function(n_)(eta) for n_ in ('dg', 'th', 'ps', 'ph')]
# Fourier reading of the S2 output (verified textually): delta_g' = -4/3 theta + 4 Phi', theta_g' = k^2 dg/4 + k^2 Psi + drag,
#   theta_b' = -H theta_b + k^2 Psi + drag/R.  Re-derive these from S2 by plane-wave substitution:
E = sp.exp(sp.I * k * X)
def pw(expr, name):
    dl, v = eqs[name][0], eqs[name][1]
    sub = {dl: dg * E if name == 'g' else sp.Function('db')(eta) * E,
           v: (-sp.I * th / k) * E, Psi: ps * E, Phi: ph * E}
    return sp.simplify(expr.subs(sub).doit() / E)
dgp = pw(eqs['g'][2], 'g')
thg_p = sp.simplify(sp.I * k * pw(eqs['g'][3], 'g'))   # theta = i k v
thb_p = sp.simplify(sp.I * k * pw(eqs['b'][3], 'b'))
log("  plane wave: dg' =", dgp, "| theta_g' (no drag) =", thg_p, "| theta_b' (no drag) =", thb_p)
# tight coupling: theta_b = theta_g = th; photon + R*baryon kills drag
th_p = sp.simplify((thg_p + R * thb_p) / (1 + R))
d2 = sp.diff(dgp, eta).subs(sp.diff(th, eta), th_p)
th_from = sp.solve(sp.Eq(sp.diff(dg, eta), dgp), th)[0]
d2 = sp.expand(sp.simplify(d2.subs(th, th_from)))
cs2 = sp.simplify(-d2.coeff(dg) / k**2)
checks['S2_cs2_eq_1_over_3_1pR'] = sp.simplify(cs2 - 1 / (3 * (1 + R))) == 0
log("  tight-coupling dg'' coefficient of dg / (-k^2) = c_s^2 =", cs2, "->", checks['S2_cs2_eq_1_over_3_1pR'])
OUT['S2'] = {**res_S2, "cs2": str(cs2), "dg_second_order": str(d2)}

# ---------------------------------------------------------------- S3: anisotropic stress of khronon / P sector
log("== S3: anisotropic stress of the khronon/P sector, local orthonormal (Newtonian-gauge) frame ==")
# Plane wave along khat = e_x: A, P, E, D(Sigma) all along khat (leaf vectors); the khronon frame n is tilted by
# eps * nu (generic direction) relative to the matter/Newtonian frame. Exact in A, P, E; first order in the tilt.
Kc, a0, mu, Qs, gam, Ldot, lam_s, Vv, Ws = sp.symbols('K a0 mu_K Q gamma Ldot lambda V W', real=True)
Am, Em, cpar, cDn, Pis, F_s, f1 = sp.symbols('Amag Emag cpar cDn Pi F f1', real=True)
Pm = sp.symbols('Pmag', positive=True)   # |P| > 0 (P = 0 exactly gives no stress at all)
nu = sp.symbols('nu1:4', real=True)
eta4 = sp.diag(-1, 1, 1, 1)
n_lo = sp.Matrix([-sp.sqrt(1 + eps**2 * sum(v_**2 for v_ in nu))] + [eps * v_ for v_ in nu])
n_up = eta4 * n_lo
def leaf(mag):          # leaf vector of magnitude ~mag along khat, orthogonal to n
    v0 = sp.symbols('v0tmp')
    V_ = sp.Matrix([v0, mag, 0, 0])
    return V_.subs(v0, sp.solve((n_up.T * V_)[0], v0)[0])
A_lo = leaf(Am); P_lo = leaf(Pm); Dc_lo = leaf(cpar)
dl_lo = -A_lo - n_lo * Ldot                 # d l = -A - n (n.d l)
cD_lo = Dc_lo - n_lo * cDn                  # curlyD = leaf part - n (n.curlyD)
h = eta4 + n_lo * n_lo.T
sym = lambda u, v: (u * v.T + v * u.T) / 2
Pabs = sp.sqrt((P_lo.T * eta4 * P_lo)[0])
PdotA = (P_lo.T * eta4 * A_lo)[0]; PcD = (P_lo.T * eta4 * cD_lo)[0]
TW = -eta4 * Ws + Em * P_lo * P_lo.T / Pabs          # on shell K W'(K|P|) = |E|
TP = eta4 * PdotA + 2 * sym(P_lo, dl_lo) + Pis * n_lo * n_lo.T - 2 * lam_s * sym(n_lo, P_lo)
Tsec = {
  'v3s': {'Q': eta4 * mu**2 * (Qs - 1)**2 / (2 * Kc) + (mu**2 / Kc) * Qs * (Qs - 1) * n_lo * n_lo.T,
          'W': TW, 'P': TP,
          'gamma': gam * (-eta4 * F_s + Pis * f1 * h + h * PcD - 2 * sym(P_lo, cD_lo))},
  'AC2q': {'Q': Qs**2 * n_lo * n_lo.T + eta4 * (Qs**2 / 2 - Vv), 'W': TW, 'P': TP,
           'gamma': gam * (-eta4 * F_s + Pis * f1 * h + h * PcD - 2 * sym(P_lo, cD_lo)
                           - 2 * Qs**2 * f1 * n_lo * n_lo.T + eta4 * Qs**4 / 2 + 2 * Qs**4 * n_lo * n_lo.T)}}
def traceless_spatial(T):
    S = T[1:, 1:]; tr = sum(S[i, i] for i in range(3))
    return S - sp.eye(3) * tr / 3
basis = sp.diag(sp.Rational(2, 3), -sp.Rational(1, 3), -sp.Rational(1, 3))   # khat khat - delta/3
# on shell (QX17 E2 / QX17A F2), with Sigma_+ -> f1 = F'(.) and l = ln Q:
#   leaves:  E = (1 + gamma f1) A + gamma D f1      ->  cpar = D_par f1 + f1 * A  (curlyD leaf part = D f1 - f1 D l = D f1 + f1 A)
#   normal:  lambda = -Ldot (1 + gamma f1) + gamma n.d f1 ;  n.curlyD = n.d f1 - f1 Ldot
Df1, ndf1 = sp.symbols('Df1 ndf1', real=True)
onshell = {cpar: Df1 + f1 * Am, Em: (1 + gam * f1) * Am + gam * Df1,
           lam_s: -Ldot * (1 + gam * f1) + gam * ndf1, cDn: ndf1 - f1 * Ldot}
res_S3 = {}
for th_name, secs in Tsec.items():
    tot = sp.zeros(3, 3); per = {}
    for nm, T in secs.items():
        TL = traceless_spatial(T)
        o0 = TL.applyfunc(lambda e: sp.simplify(e.subs(eps, 0)))
        o1 = TL.applyfunc(lambda e: sp.simplify(sp.series(e, eps, 0, 2).removeO().coeff(eps, 1)))
        per[nm] = {"tilt0": str(sp.simplify(o0[0, 0] * sp.Rational(3, 2))) if o0 != sp.zeros(3, 3) else "0",
                   "tilt1_zero_offshell": o1 == sp.zeros(3, 3)}
        tot += o0 + eps * o1
    tot0 = tot.applyfunc(lambda e: e.coeff(eps, 0)); tot1 = tot.applyfunc(lambda e: e.coeff(eps, 1))
    tot0_on = tot0.applyfunc(lambda e: sp.simplify(e.subs(onshell)))
    tot1_on = tot1.applyfunc(lambda e: sp.simplify(e.subs(onshell)))
    # is tot0 exactly s * basis with s = -|P||E| ?
    s_tilt0 = sp.simplify(tot0_on[0, 0] * sp.Rational(3, 2))
    is_basis = sp.simplify(tot0_on - s_tilt0 * basis) == sp.zeros(3, 3)
    res_S3[th_name] = {"per_sector": per, "s_offshell_tilt0": str(sp.simplify(tot0[0, 0] * sp.Rational(3, 2))),
                       "s_onshell_tilt0": str(sp.factor(s_tilt0)), "pure_longitudinal": bool(is_basis),
                       "s_equals_minus_P_E": sp.simplify(s_tilt0 + Pm * ((1 + gam * f1) * Am + gam * Df1)) == 0,
                       "tilt_linear_term_onshell_zero": tot1_on == sp.zeros(3, 3),
                       "tilt_linear_term_offshell": str(sp.simplify(tot1[0, 1]))}
    log(f"  {th_name}: per sector:", per)
    log(f"     traceless spatial stress = s (khat khat - delta/3), s(off-shell, no tilt) =", res_S3[th_name]['s_offshell_tilt0'])
    log(f"     on shell: s =", res_S3[th_name]['s_onshell_tilt0'], "| s == -|P||E|:", res_S3[th_name]['s_equals_minus_P_E'],
        "| tilt-linear piece zero on shell:", res_S3[th_name]['tilt_linear_term_onshell_zero'],
        "(off shell xy comp:", res_S3[th_name]['tilt_linear_term_offshell'], ")")
OUT['S3'] = res_S3
for th_name in res_S3:
    checks[f'S3_{th_name}_aniso_is_minus_P_E'] = bool(res_S3[th_name]['s_equals_minus_P_E'] and res_S3[th_name]['pure_longitudinal'])
    checks[f'S3_{th_name}_tilt_term_zero_onshell'] = bool(res_S3[th_name]['tilt_linear_term_onshell_zero'])
# Reading: s = -|P||E| with K|P| = a0 x/(1+x), x = |E|/a0 (the Legendre map, QX17 E2).
#   x << 1: K|P| ~ |E| = O(eps)  -> s = O(eps^2): NO linear anisotropic stress (the expected zero).
#   x >~ 1: K|P| -> a0             -> s = -(a0/K)|E| x/(1+x) = O(eps * a0): a LINEAR slip proportional to a0 exists.
x_s = sp.symbols('x', positive=True)
s_law = sp.simplify(-(a0 * x_s / (1 + x_s) / Kc) * (x_s * a0))
OUT['S3_s_on_law'] = str(s_law)
log("  on the law: s = -(a0/K) |E| x/(1+x) =", s_law, " -> linear in |E| once x >~ 1 (not zero)")

# numerical slip bound at z 1100 (both footings, never pooled). k^2 (Phi - Psi) = -8 pi G a^2 s (MB95), physical units:
#   |Phi - Psi| = 2K |s| / (c^4 k_phys^2), |s| = |P||E|, K|P| <= a0 x_f; |A| = c^2 k_phys Psi (gamma pieces: E/A - 1 = gamma f1 + ... ~ 1e-11, QX17 sec 3)
c = 2.99792458e8; Mpc = 3.0857e22; zrec = 1100.0
footings = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
kl = [0.01, 0.03, 0.1, 0.3]; xs = [1, 3, 10, 30, 100]
bound = {}
for fn_, a0v in footings.items():
    bound[fn_] = {}
    for xf in xs:
        row = {}
        for kk in kl:
            kph = kk * (1 + zrec) / Mpc
            row[str(kk)] = 2 * xf * a0v / (c**2 * kph)     # |Phi-Psi|/Psi = 2 K|P|/(c^2 k) * |E|/|A| <= 2 x_f a0/(c^2 k_phys) (x/(1+x) <= 1, |E| ~ |A|)
        bound[fn_][str(xf)] = row
OUT['S3_slip_over_Psi_upper_bound'] = bound
log("  slip/Psi upper bound (z 1100), canonical x=1:", bound['canonical']['1'], " x=100:", bound['canonical']['100'])
log("  alt x=1:", bound['alt']['1'], " x=100:", bound['alt']['100'])

# ---------------------------------------------------------------- S4: clock
log("== S4: S_m has no tau dependence ==")
dSdtau = [sp.diff(Lm, tau)] + [sp.diff(Lm, sp.diff(tau, v)) for v in (t, x)]
checks['S4_Sm_tau_independent'] = all(e == 0 for e in dSdtau) and not has_khronon(Lm)
log("  dL_m/dtau, dL_m/d(d tau) all zero:", checks['S4_Sm_tau_independent'])

# ---------------------------------------------------------------- S5: MUTATE-gravity
log("== S5: MUTATE-gravity: L_int = beta n_m u^m on the baryon worldline ==")
gw = sp.diag(-Nw**2, bw**2)
dtau = sp.Matrix([sp.Derivative(tauw, tw), sp.Derivative(tauw, xw)])
# use partials of tau(t,x) evaluated on the worldline
tt, xx_ = sp.symbols('tt xx_')
tau_tx = sp.Function('tau')(tt, xx_)
Nt = sp.Function('N', positive=True)(tt, xx_); bt = sp.Function('b', positive=True)(tt, xx_)
Qexpr = sp.sqrt(sp.diff(tau_tx, tt)**2 / Nt**2 - sp.diff(tau_tx, xx_)**2 / bt**2)
n_t = -sp.diff(tau_tx, tt) / Qexpr; n_x = -sp.diff(tau_tx, xx_) / Qexpr
on_w = {tt: tw, xx_: xw}
L_int = beta * (n_t.subs(on_w) * tdot + n_x.subs(on_w) * xdot)
EL_mut = [eq.lhs for eq in sp.euler_equations(L_dust + L_int, [tw, xw], lam_)]
mut_found = any(has_khronon(e) for e in EL_mut)
# beta -> 0 returns the tau-free equations
mut_off = [sp.simplify(e.subs(beta, 0) - e0_) for e, e0_ in zip(EL_mut, EL_dust)]
checks['S5_MUTATE_finds_khronon'] = mut_found
checks['S5_MUTATE_beta0_reduces'] = all(e == 0 for e in mut_off)
log("  khronon in mutated baryon Euler equation:", mut_found, "| beta=0 reduces to geodesic:", checks['S5_MUTATE_beta0_reduces'])
# also: tau-only total derivative would NOT bite (beta * dtau/dlambda); the 1/Q makes it bite. Control:
L_td = beta * (sp.diff(tau_tx, tt).subs(on_w) * tdot + sp.diff(tau_tx, xx_).subs(on_w) * xdot)
EL_td = [sp.simplify(eq.lhs - e0_) for eq, e0_ in zip(sp.euler_equations(L_dust + L_td, [tw, xw], lam_), EL_dust)]
checks['S5_control_total_derivative_drops'] = all(e == 0 for e in EL_td)
log("  control: beta d tau/d lambda (total derivative) drops out:", checks['S5_control_total_derivative_drops'])

OUT['checks'] = checks
OUT['all_pass'] = all(checks.values())
log("== checks ==")
for k_, v_ in checks.items():
    log(f"  {k_}: {v_}")
with open(os.path.join(HERE, 'd3_frame.json'), 'w') as fh:
    json.dump(OUT, fh, indent=1)
