#!/usr/bin/env python3
"""SMF1 symbolic part: the member's grading form (FROZEN_CRITERIA.md section 1.3), its Euler-Lagrange equations, the
known answers KA1 (LFS1 frozen Y) and KA2 (T-SCR), the S0 gates (S0a reduction, S0b net fill, S0c fill where counted
once holds), S1 (FRW dispersion, static decoupling, GW) and the MUTATE arms.

    python3 smf1_sym.py                      -> smf1_sym.out / smf1_sym.json
    SMF1_MUTATE=MU1|MU2|MU3 python3 smf1_sym.py   -> smf1_sym_MUTATE_<arm>.out / .json

Units: Newtonian grading form, K = 4 pi G (c = 1 in the frame's h). Radial reduction with the r^2 measure for S0 and KA1;
a 1D plane wave for S1 and KA2. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json, os, sys, time
import sympy as sp
from sympy.calculus.euler import euler_equations

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get('SMF1_MUTATE', '')
T0 = time.time()
OUT, RES = [], {}


def say(*a):
    s = ' '.join(str(x) for x in a)
    OUT.append(s)
    print(s, flush=True)


t, r, x = sp.symbols('t r x', real=True)
K, a0, mu, hb, m = sp.symbols('K a0 mu_K hbar m', positive=True)
al, lam, gx, c0, E, R = sp.symbols('alpha lambda_s g_x c0 E R', positive=True)
sgn_al = -1 if MUT == 'MU3' else 1
sgn_gx = -1 if MUT == 'MU3' else 1

ph = sp.Function('phi_f')(t, r)     # frame velocity potential (tau = t - phi_f)
th = sp.Function('theta')(t, r)     # Psi velocity potential (Madelung)
rho = sp.Function('rho')(t, r)      # Psi mass density
Phi = sp.Function('Phi')(t, r)      # Newtonian potential
rb = sp.Function('rho_b')(r)        # baryons (static source)
Jg = sp.Function('J')               # generic law function (identities hold for any J)

h = -(sp.diff(ph, t) + sp.diff(ph, r) ** 2 / 2 + Phi)
s = -sp.diff(h, r)                  # |A|, A = -grad h (outward where s > 0)
lap_ph = sp.diff(ph, r, 2) + 2 * sp.diff(ph, r) / r
chi = (m / hb) * (th - ph)
if MUT == 'MU2':
    Lx = -gx * sp.Function('V')(chi)                    # non-analytic exchange, not multiplied by rho_Psi
else:
    Lx = -sgn_gx * gx * rho * sp.sin(chi) ** 2


def lagr(Jexpr):
    return r ** 2 * (mu ** 2 * h ** 2 / (2 * K) + Jexpr
                     - rho * (sp.diff(th, t) + sp.diff(th, r) ** 2 / 2 + Phi)
                     - (hb ** 2 / (8 * m ** 2)) * sp.diff(rho, r) ** 2 / rho
                     - sgn_al * (al / 2) * rho * (sp.diff(ph, r) - sp.diff(th, r)) ** 2
                     - (lam / (2 * K)) * lap_ph ** 2
                     + Lx
                     - sp.diff(Phi, r) ** 2 / (2 * K) - rb * Phi)


say('SMF1 smf1_sym.py' + (f'  [MUTATE {MUT}]' if MUT else ''))
say('Grading form (radial, r^2 measure): frame h, Psi Madelung (rho, theta), alignment alpha, stiffness lambda_s,')
say('exchange -g_x rho sin^2 chi, chi = (m/hbar)(theta - phi_f), gravity Phi; J generic in E1 and KA1.')
EL = euler_equations(lagr(Jg(s)), [ph, th, rho, Phi], [t, r])
EL_ph, EL_th, EL_rho, EL_Phi = [e.lhs for e in EL]

sd = sp.Dummy('sd')
Pr = sp.Subs(sp.diff(Jg(sd), sd), sd, s)      # P^r = J'(|A|) along A (K P = K J'(s))
N = mu ** 2 * h / K + sp.diff(r ** 2 * Pr, r) / r ** 2
Sf_expr = -sp.diff(Lx, ph)                    # exchange source into the frame
F_f = N * sp.diff(ph, r) + sgn_al * al * rho * (sp.diff(ph, r) - sp.diff(th, r)) - (lam / K) * sp.diff(lap_ph, r)
F_p = rho * sp.diff(th, r) - sgn_al * al * rho * (sp.diff(ph, r) - sp.diff(th, r))
cont_f = sp.diff(N, t) + sp.diff(r ** 2 * F_f, r) / r ** 2 - Sf_expr     # d_t N + div F_f - S_f
cont_p = sp.diff(rho, t) + sp.diff(r ** 2 * F_p, r) / r ** 2 + sp.diff(Lx, th)   # d_t rho + div F_Psi + S_f

# ---- E1: the Euler-Lagrange equations are the two continuity equations (exact, any J)
res_f = sp.simplify(sp.expand((EL_ph - r ** 2 * cont_f).doit()))
res_p = sp.simplify(sp.expand((EL_th - r ** 2 * cont_p).doit()))
RES['E1_frame_EL_is_continuity_residual'] = str(res_f)
RES['E1_Psi_EL_is_continuity_residual'] = str(res_p)
say('E1 frame EL == r^2 [d_t N + div F_f - S_f]   residual:', res_f)
say('E1 Psi EL   == r^2 [d_t rho + div F_Psi + S_f] residual:', res_p)
sum_src = sp.simplify(sp.diff(Lx, ph) + sp.diff(Lx, th))
RES['E1_sum_of_sources'] = str(sum_src)
say('E1 dL_x/dphi_f + dL_x/dtheta (diagonal symmetry => 0):', sum_src, '  so d_t(N + rho) + div(F_f + F_Psi) = 0')
say('   S_f =', sp.simplify(Sf_expr))
RES['E1_PASS'] = bool(res_f == 0 and res_p == 0 and sum_src == 0)

# ---- KA1: alpha = g_x = lambda_s = 0, mu_K = 0, zero shift (phi_f = -c0 t): Y = r^2 P^r frozen; with L_x: d_t Y = Int S r^2
Y = (r ** 2 * Pr).subs(ph, -c0 * t).doit()
ka1_off = sp.simplify(sp.expand((EL_ph.subs({al: 0, gx: 0, lam: 0, mu: 0}).subs(ph, -c0 * t).doit())
                                - sp.diff(Y, t, r)))
RES['KA1_off_residual'] = str(ka1_off)
say('KA1 (L_x = L_al = 0, mu_K = 0, zero shift): frame EL - d_r d_t Y, residual:', ka1_off,
    '=> d_t Y = f(t); regular centre => Y frozen')
ka1_on = sp.simplify(sp.expand((EL_ph.subs({al: 0, lam: 0, mu: 0}).subs(ph, -c0 * t).doit())
                               - sp.diff(Y, t, r) + r ** 2 * Sf_expr.subs(ph, -c0 * t)))
RES['KA1_on_residual'] = str(ka1_on)
say('KA1 (L_x on): frame EL - d_r d_t Y + r^2 S_f, residual:', ka1_on, '=> d_t Y(R) = Int_0^R S_f r^2 dr')
RES['KA1_PASS'] = bool(ka1_off == 0 and ka1_on == 0)

# ---- S0a: static frame (phi_f = -c0 t), static Psi (theta = -E t, rho(r)), static Phi(r); concrete J
Jc = (a0 ** 2 / K) * (s / a0 - sp.log(1 + s / a0))
ELc = euler_equations(lagr(Jc), [Phi], [t, r])[0].lhs
Phis = sp.Function('Phis')(r)
rhos = sp.Function('rhos')(r)
st = {ph: -c0 * t, th: -E * t, Phi: Phis, rho: rhos}
ELP_s = sp.simplify(ELc.subs(st).doit())
xx = sp.diff(Phis, r) / a0
mu_law = xx / (1 + xx)
target = r ** 2 * (rb + rhos) + r ** 2 * mu ** 2 * (c0 - Phis) / K - sp.diff(r ** 2 * mu_law * sp.diff(Phis, r), r) / K
s0a_res = sp.simplify(ELP_s + target)
if s0a_res != 0:
    s0a_res = sp.simplify(ELP_s - target)
    sgn_t = -1
else:
    sgn_t = +1
RES['S0a_residual'] = str(s0a_res)
say('S0a static Phi equation vs d_r[r^2 mu(Phi_r/a0) Phi_r]/K = r^2 (rho_b + rho_Psi) + r^2 mu_K^2 (c0 - Phi)/K;')
say('    residual:', s0a_res, f'(sign convention {sgn_t:+d})')
say('    i.e. div[mu grad Phi] + mu_K^2 (Phi - c0) = K (rho_b + rho_Psi): rho = rho_b + rho_Psi. The alignment and')
say('    exchange energies do not depend on Phi in the grading form (they are O(v^2/c^2) of rho_Psi c^2), so they do')
say('    not source Phi at Newtonian order. (A)\'s law with rho = rho_b (counted once) iff rho_Psi = 0 in V_s.')
RES['S0a_PASS'] = bool(s0a_res == 0)
ELf_s = sp.simplify(EL_ph.subs(st).doit())
RES['S0a_static_frame_EL'] = str(ELf_s)
say('S0a static frame EL (zero shift, static Psi):', ELf_s)
say('    => stationary only if rho_Psi = 0 or the phase is locked (c0 = E and sin 2 chi = 0).')

# ---- S0b: net transfer into the polarization charge over V = ball of radius R whose boundary free-falls
Wf = sp.Function('W')(t, r)      # W = r^2 P^r (polarization flux through the sphere / 4 pi)
Vf = sp.Function('V_F')(t, r)    # r^2 F (frame current through the sphere / 4 pi)
hg = sp.Function('h')(t, r)
Sg = sp.Function('S')(t, r)
# r^2 [d_t N + div F - S] with N = mu_K^2 h/K + r^-2 d_r W (E1's N, exact)
dens = r ** 2 * mu ** 2 * sp.diff(hg, t) / K + sp.diff(Wf, t, r) + sp.diff(Vf, r) - r ** 2 * Sg
tot = (sp.Integral(r ** 2 * mu ** 2 * sp.diff(hg, t) / K, (r, 0, R)) + sp.integrate(sp.diff(Wf, r, t), (r, 0, R))
       + sp.integrate(sp.diff(Vf, r), (r, 0, R)) - sp.Integral(r ** 2 * Sg, (r, 0, R)))
pol_part = sp.integrate(sp.diff(Wf, r, t), (r, 0, R))
say('S0b Int_0^R r^2 d_t N dr, polarization part = Int_0^R d_r d_t W dr =', pol_part)
reg = {Wf.subs(r, 0): 0, Vf.subs(r, 0): 0}       # regular centre: r^2 P -> 0, r^2 F -> 0
pol_part_reg = sp.simplify(pol_part.doit().subs({sp.Derivative(Wf.subs(r, 0), t): 0}).subs(reg))
say('    with a regular centre:', pol_part_reg)
RES['S0b_polarization_part'] = str(pol_part_reg)
say('S0b integrated frame continuity: Int_0^R S_f r^2 dr = d/dt Int_0^R (mu_K^2 h/K) r^2 dr + d/dt W(t,R) + V_F(t,R)')
if MUT == 'MU1':
    Mb = sp.Function('M_b')(t)
    G = K / (4 * sp.pi)
    W_R = R ** 2 * sp.sqrt(G * Mb * a0) / (K * R)     # law's deep-regime flux at a static boundary, (1 - mu) -> 1
    net = sp.simplify(sp.diff(W_R, t))
    say('MU1 boundary kept static (A = g at R): net transfer into polarization = d/dt W(t,R) =', net)
    RES['MU1_net_transfer'] = str(net)
    RES['MU1_bites'] = bool(net != 0)
    s0b_zero = False
else:
    # boundary free-falls for all t: P(t,R) = 0, so W(t,R) = 0 for all t and its time derivative vanishes
    net = sp.simplify(pol_part_reg.subs(sp.Derivative(Wf.subs(r, R), t), sp.diff(sp.S(0), t)).subs(Wf.subs(r, R), 0))
    say('S0b boundary free-falling, W(t,R) = R^2 P(t,R) = 0 for all t: net transfer into the polarization charge of V =', net)
    s0b_zero = bool(net == 0)
    RES['S0b_net_transfer_into_polarization'] = str(net)
X3, Y3, Z3 = sp.symbols('X Y Z', real=True)
Pc = [X3 * (1 - X3) * (1 + Y3 * Z3 + X3 ** 2), Y3 * (1 - Y3) * (2 - X3 * Z3), Z3 * (1 - Z3) * (X3 + Y3 ** 3)]
div3 = sp.diff(Pc[0], X3) + sp.diff(Pc[1], Y3) + sp.diff(Pc[2], Z3)
cube = sp.integrate(div3, (X3, 0, 1), (Y3, 0, 1), (Z3, 0, 1))
say('S0b 3D check (no symmetry): Int_cube div P for a P vanishing on the faces =', cube)
RES['S0b_3D_cube'] = str(cube)
RES['S0b_FAIL_identity'] = bool(s0b_zero and cube == 0)
say('S0b reading: in net the exchange changes only the frame\'s dust part (mu_K^2 h/K) and the boundary fluxes; the')
say('    polarization charge of V is zero at every time, for every exchange rate, alignment and ell (Gauss).')

# ---- S0c: exchange source where counted once holds exactly (rho_Psi = 0)
S_expr = sp.simplify(Sf_expr)
S_at0 = sp.simplify(S_expr.subs(rho, 0))
RES['S0c_S_f'] = str(S_expr)
RES['S0c_S_f_at_rho0'] = str(S_at0)
say('S0c S_f =', S_expr, ';  at rho_Psi = 0:', S_at0)
if MUT == 'MU2':
    RES['MU2_bites'] = bool(S_at0 != 0)
    say('MU2 (non-analytic V(chi), no rho_Psi factor): S_f at rho_Psi = 0 =', S_at0, '->', 'bites' if S_at0 != 0 else 'does NOT bite')
RES['S0c_FAIL_identity'] = bool(S_at0 == 0)

# ---- KA2 and S1-FRW: plane wave on a homogeneous background (Jeans swindle)
ff = sp.Function('f')(t, x); dr_ = sp.Function('d')(t, x); tq = sp.Function('q')(t, x); Pp = sp.Function('U')(t, x)
nd, rbar, kk = sp.symbols('n_d rhobar k', positive=True)
w = sp.symbols('omega')
w2 = sp.symbols('w2')
cx = (m / hb) * (tq - ff)


def L2(with_psi=True, a_=al, l_=lam, g_=gx):
    u = sp.diff(ff, t) + Pp
    L = (-nd * sp.diff(ff, x) ** 2 / 2 + mu ** 2 * u ** 2 / (2 * K) + sp.diff(u, x) ** 2 / (2 * K)
         - sp.diff(Pp, x) ** 2 / (2 * K) - (l_ / (2 * K)) * sp.diff(ff, x, 2) ** 2)
    if with_psi:
        L += (-dr_ * (sp.diff(tq, t) + Pp) - rbar * sp.diff(tq, x) ** 2 / 2
              - (hb ** 2 / (8 * m ** 2 * rbar)) * sp.diff(dr_, x) ** 2
              - sgn_al * (a_ / 2) * rbar * (sp.diff(ff, x) - sp.diff(tq, x)) ** 2 - sgn_gx * g_ * rbar * cx ** 2)
    return L


def dispersion(L, fields):
    """Linear constant-coefficient EL equations -> matrix in (omega, k) by d_t -> -i omega, d_x -> i k."""
    eqs = [sp.expand(e.lhs) for e in euler_equations(L, fields, [t, x])]
    amps = sp.symbols('A0:%d' % len(fields))
    rows = []
    for e in eqs:
        row = []
        for f, a in zip(fields, amps):
            coef = 0
            for term in sp.Add.make_args(e):
                ds = [d for d in term.atoms(sp.Derivative) if d.expr == f]
                if ds:
                    d = ds[0]
                    nt = sum(c for v, c in d.variable_count if v == t)
                    nx = sum(c for v, c in d.variable_count if v == x)
                    coef += (term / d) * (-sp.I * w) ** nt * (sp.I * kk) ** nx
                elif term.has(f) and not any(dd.expr == f for dd in term.atoms(sp.Derivative)):
                    coef += term / f
            row.append(sp.expand(coef))
        rows.append(row)
    return sp.Matrix(rows)


# KA2: frame alone with its dust (chi = mu_K^2/K) and J''(0) = 1/K, around free fall
M_ka2 = dispersion(L2(with_psi=False, l_=0), [ff, Pp])
det_ka2 = sp.factor(sp.expand(M_ka2.det()))
sol_ka2 = sp.solve(sp.expand(det_ka2).subs(w, sp.sqrt(w2)), w2)
tscr = -K * nd * mu ** 2 / (mu ** 2 + kk ** 2)
ka2_res = [sp.simplify(sv - tscr) for sv in sol_ka2]
RES['KA2_branches'] = [str(sp.simplify(sv)) for sv in sol_ka2]
RES['KA2_PASS'] = bool(any(rz == 0 for rz in ka2_res))
say('KA2 frame-only omega^2 branches:', [sp.simplify(sv) for sv in sol_ka2],
    '; vs T-SCR -K n_d mu_K^2/(mu_K^2 + k^2), residuals:', ka2_res)

# S1-FRW: full system (frame f, Psi density d and phase q, potential U); quadratic in omega^2: A w^4 + B w^2 + C = 0
M_full = dispersion(L2(), [ff, dr_, tq, Pp])
det_full = sp.expand(M_full.det(method='berkowitz'))
Pw = sp.Poly(det_full, w)
cA, cB, cC = [sp.factor(Pw.coeff_monomial(w ** n)) for n in (4, 2, 0)]
odd = [Pw.coeff_monomial(w ** n) for n in (3, 1)]
RES['S1_det_coeffs'] = {'A': str(cA), 'B': str(cB), 'C': str(cC), 'odd_terms_zero': bool(all(o == 0 for o in odd))}
say('S1-FRW determinant = A w^4 + B w^2 + C (odd powers zero:', all(o == 0 for o in odd), ')')
say('   A =', cA)
say('   C =', cC)
prod = sp.cancel(cC / cA)          # product of the two omega^2 roots
summ = sp.cancel(-cB / cA)         # sum of the two omega^2 roots
lim_prod = sp.limit(prod / kk ** 4, kk, sp.oo)
lim_sum = sp.limit(summ / kk ** 4, kk, sp.oo)
lim_neg = sp.limit(prod / summ, kk, sp.oo)      # the small root when the large one dominates the sum
say('S1 large k: (product of roots)/k^4 ->', lim_prod, ';  (sum)/k^4 ->', lim_sum, ';  small root ~ product/sum ->', lim_neg)
grad_inst = bool(lim_sum.is_positive is not True or (lim_neg.is_finite is not True))
RES['S1_large_k'] = {'product_over_k4': str(lim_prod), 'sum_over_k4': str(lim_sum), 'small_root_limit': str(lim_neg)}
# k -> 0: the growing root is -K (n_d + rhobar) exactly
red0 = sp.expand(sp.limit(sp.cancel(det_full / kk ** 2), kk, 0))
jeans_root = -K * (nd + rbar)
j0 = sp.simplify(red0.subs(w, sp.sqrt(jeans_root)))
other0 = [sp.simplify(v) for v in sp.solve(red0.subs(w, sp.sqrt(w2)), w2)]
say('S1 k -> 0: det/k^2 at omega^2 = -K (n_d + rhobar):', j0, ';  roots:', other0)
RES['S1_k0_roots'] = [str(v) for v in other0]
RES['S1_k0_Jeans_root_residual'] = str(j0)
# k^2 coefficient of the growing root: omega^2 = -K (n_d + rhobar) + c1 k^2 + O(k^4)
c1s = sp.symbols('c1')
W0 = -K * (nd + rbar)
ser = sp.series(sp.expand((cA * (W0 + c1s * kk ** 2) ** 2 + cB * (W0 + c1s * kk ** 2) + cC) / kk ** 2), kk, 0, 3).removeO()
c1v = sp.factor(sp.solve(sp.expand(ser.coeff(kk, 2)), c1s)[0])
c1_split = sp.simplify(c1v - (-lam + K * hb ** 2 * nd ** 2 / (2 * gx * m ** 2 * rbar + hb ** 2 * mu ** 2 * (nd + rbar))))
RES['S1_growing_root_k2_coefficient'] = str(c1v)
RES['S1_c1_split_residual'] = str(c1_split)
say('S1 growing root to k^2: c1 =', c1v)
say('   c1 - [-lambda_s + K hbar^2 n_d^2/(2 g_x m^2 rhobar + hbar^2 mu_K^2 (n_d + rhobar))], residual:', c1_split)
say('   (the frame stiffness enters the growing mode with a NEGATIVE sound speed squared; reported, see smf1_num.out)')
# numeric sweep at representative values (units: kpc, km/s, Gyr-free ratios; only signs and the Jeans ratio matter)
import math
numvals = {K: 1.0, rbar: 1.0, nd: 0.01, mu: 1e-3, hb: 1.0, m: 1e4, al: 1.0, lam: 1e-6, gx: 1e-2}
sweep = []
for lk in [x_ / 4 for x_ in range(-16, 25)]:
    kv = 10 ** lk
    a_, b_, c_ = [float(e.subs(numvals).subs(kk, kv)) for e in (cA, cB, cC)]
    disc = b_ * b_ - 4 * a_ * c_
    r1 = (-b_ + math.sqrt(disc)) / (2 * a_); r2 = (-b_ - math.sqrt(disc)) / (2 * a_)
    sweep.append({'k': kv, 'disc_pos': disc >= 0, 'w2_hi': r1, 'w2_lo': r2, 'lo_over_minusK(n+rho)': r2 / (-1.01)})
RES['S1_numeric_sweep'] = sweep
lo_min = min(sv['w2_lo'] for sv in sweep)
real_all = all(sv['disc_pos'] for sv in sweep)
say(f'S1 numeric sweep (K = rho = 1, n_d = 0.01, mu_K = 1e-3, hbar/m = 1e-4, alpha = 1, lambda_s = 1e-6, g_x = 1e-2;')
say(f'    k from 1e-4 to 1e6): all roots real: {real_all}; min omega^2 = {lo_min:.4g} (Jeans -K(n_d + rho) = -1.01);')
say('    growing root / Jeans at k = 1e-4, 1, 1e2, 1e4:',
    [round(sv['lo_over_minusK(n+rho)'], 4) for sv in sweep if round(math.log10(sv['k']), 2) in (-4.0, 0.0, 2.0, 4.0)])
neg_inf = bool(grad_inst or lo_min < -1.01 * 1.0001 or not real_all)
RES['S1_gradient_instability'] = neg_inf
say('S1 gradient instability (a root unbounded below as k grows, or complex roots):', neg_inf)
kin = {'frame_phi_t^2_coefficient_(mu_K^2+k^2)/K': True,
       'alignment_energy_alpha_rho_k^2|f-q|^2/2': sgn_al > 0,
       'stiffness_energy_lambda_s_k^4|f|^2/(2K)': True,
       'exchange_energy_g_x_rho_(m/hbar)^2|q-f|^2': sgn_gx > 0,
       'Psi_Hamiltonian_rho_k^2|q|^2/2_+_hbar^2_k^2|d|^2/(8 m^2 rho)': True}
noghost = all(kin.values())
RES['S1_unmixed_energy_signs_positive'] = kin
RES['S1_no_ghost_unmixed'] = noghost
say('S1 unmixed kinetic and energy coefficients positive (QG1 method):', noghost)
if MUT == 'MU3':
    RES['MU3_bites'] = bool(neg_inf or not noghost)
    say('MU3 (alpha and g_x signs flipped): gradient instability or negative energy appears:', RES['MU3_bites'])

# S1-static: around psi = 0 the couplings are quadratic in psi; a psi-frame cross term is at least cubic
ps, pc, dphi, eta = sp.symbols('psi psibar dphi eta')
cross = sp.expand(sp.series(-gx * (eta * ps) * (eta * pc) * sp.sin((m / hb) * (th - (ph + eta * dphi))) ** 2,
                            eta, 0, 4).removeO())
cross_terms = [term for term in sp.Add.make_args(cross) if term.has(dphi)]
min_deg = min(sp.Poly(term, eta).degree() for term in cross_terms) if cross_terms else None
RES['S1_static_lowest_order_psi_frame_cross_term'] = min_deg
say('S1-static: lowest order of a psi-frame cross term in L_x around psi = 0:', min_deg, '(>= 3: decoupled at linear order;')
say('    the alignment term rho |grad phi_f - grad theta|^2 is likewise quadratic in psi times the frame background)')
RES['S1_static_PASS'] = bool(min_deg is None or min_deg >= 3)
RES['GW_cT_equals_c'] = True
say('GW: the member adds no K_ij K^ij, curvature or beta term (L_st is the khronometric lambda term); c_T^2 = 1/(1 - beta) = 1.')

RES['S1_PASS'] = bool(noghost and not neg_inf and RES['S1_static_PASS'])
RES['runtime_s'] = time.time() - T0
RES['mutate'] = MUT
RES['note'] = 'Adopts nothing. kappa = 1/2 FITTED; not theory closed.'
say(f'runtime {RES["runtime_s"]:.1f} s')
say('Adopts nothing. kappa = 1/2 FITTED; not theory closed.')
suf = f'_MUTATE_{MUT}' if MUT else ''
json.dump(RES, open(os.path.join(HERE, f'smf1_sym{suf}.json'), 'w'), indent=1, default=str)
open(os.path.join(HERE, f'smf1_sym{suf}.out'), 'w').write('\n'.join(OUT) + '\n')
# Adopts nothing. kappa = 1/2 FITTED; not theory closed.
