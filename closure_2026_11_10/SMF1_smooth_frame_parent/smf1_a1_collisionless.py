#!/usr/bin/env python3
"""SMF1 AMENDMENT A1 checks: does a collisionless (kinetic, non-wave) carrier in the same B-Tm-smooth structure escape
the failing gates? C1: S0b's balance with a kinetic loss term. C2: kinetic starvation (+ MUTATE MA1, f allowed
negative). C3: the collisionless fluid limit of S1's FRW dispersion (g_x = 0, isothermal sigma^2 in place of quantum
pressure), its growing-root k^2 coefficient and the condition that removes the -lambda_s band.

    nice -n 19 python3 smf1_a1_collisionless.py   -> smf1_a1_collisionless.out / .json

Criteria: AMENDMENT_A1.md (post hoc, committed alone before this script). Adopts nothing. kappa = 1/2 FITTED; not theory
closed.
"""
import json, math, os, time
import sympy as sp
from sympy.calculus.euler import euler_equations

HERE = os.path.dirname(os.path.abspath(__file__))
T0 = time.time()
OUT, RES = [], {}


def say(*a):
    s = ' '.join(str(v) for v in a)
    OUT.append(s)
    print(s, flush=True)


t, r, v, R, x = sp.symbols('t r v R x', real=True)
K, mu, al, lam, sig, nd, rb, kk = sp.symbols('K mu_K alpha lambda_s sigma n_d rhobar k', positive=True)
w, w2, c1s = sp.symbols('omega w2 c1')

# ---- C1: S0b with a kinetic carrier. Frame: d_t N + r^-2 d_r(r^2 F) = S, S = Int gamma(v) f(t,r,v) dv (loss from the carrier)
f = sp.Function('f')(t, r, v)
gam = sp.Function('gamma')(v)
S_kin = sp.Integral(gam * f, (v, -sp.oo, sp.oo))
Wf = sp.Function('W')(t, r)        # r^2 P
Vf = sp.Function('V_F')(t, r)      # r^2 F_f
hg = sp.Function('h')(t, r)
lhs = sp.Integral(r ** 2 * S_kin, (r, 0, R))
rhs = (sp.Integral(r ** 2 * mu ** 2 * sp.diff(hg, t) / K, (r, 0, R)) + sp.integrate(sp.diff(Wf, r, t), (r, 0, R))
       + sp.integrate(sp.diff(Vf, r), (r, 0, R)))
# continuity density integrated term by term equals rhs - lhs; with W(t,0) = V_F(t,0) = 0 and W(t,R) = 0 for all t:
rhs_bc = rhs.subs({sp.Derivative(Wf.subs(r, 0), t): 0}).subs({Wf.subs(r, 0): 0, Vf.subs(r, 0): 0})
pol = sp.integrate(sp.diff(Wf, r, t), (r, 0, R)).subs({sp.Derivative(Wf.subs(r, 0), t): 0})
pol_ff = sp.simplify(pol.subs(sp.Derivative(Wf.subs(r, R), t), 0))
free = sorted(str(s_) for s_ in (rhs_bc - sp.Integral(r ** 2 * mu ** 2 * sp.diff(hg, t) / K, (r, 0, R))).free_symbols)
RES['C1_net_polarization_transfer_free_fall'] = str(pol_ff)
RES['C1_carrier_enters_only_through_S'] = not (rhs_bc.has(f) or rhs_bc.has(gam))
say('C1 kinetic carrier: Int_0^R r^2 [Int gamma f dv] dr = d/dt Int (mu_K^2 h/K) r^2 dr + d/dt W(t,R) + V_F(t,R);')
say('   the right side contains no carrier variable:', RES['C1_carrier_enters_only_through_S'],
    '; net transfer into the polarization charge with a free-falling boundary =', pol_ff)
RES['C1_PASS'] = bool(pol_ff == 0 and RES['C1_carrier_enters_only_through_S'])

# ---- C2: kinetic starvation, and MA1 (f allowed negative)
n = sp.symbols('n', nonnegative=True)
g = sp.exp(-v ** 2) / sp.sqrt(sp.pi)                       # normalized velocity shape, Int g dv = 1
gm = v ** 2                                                # a loss rate depending on speed
S_n = sp.integrate(gm * n * g, (v, -sp.oo, sp.oo))
RES['C2_S_of_n'] = str(sp.simplify(S_n))
RES['C2_S_at_n0'] = str(S_n.subs(n, 0))
hneg = (v ** 2 - sp.Rational(1, 2)) * sp.exp(-v ** 2)     # sign-indefinite, Int h dv = 0
dens_ma1 = sp.integrate(hneg, (v, -sp.oo, sp.oo))
S_ma1 = sp.integrate(gm * hneg, (v, -sp.oo, sp.oo))
RES['MA1_density'] = str(dens_ma1)
RES['MA1_S'] = str(S_ma1)
RES['C2_PASS'] = bool(S_n.subs(n, 0) == 0)
RES['MA1_bites'] = bool(dens_ma1 == 0 and S_ma1 != 0)
say('C2 kinetic loss S = Int gamma f dv with f = n g, Int g = 1:', sp.simplify(S_n), '-> at n = 0:', S_n.subs(n, 0))
say('MA1 (f = (v^2 - 1/2) e^{-v^2}, sign-indefinite): density', dens_ma1, ', loss', S_ma1, '->',
    'bites' if RES['MA1_bites'] else 'DOES NOT BITE')

# ---- C3: collisionless fluid limit of the S1 FRW system (g_x = 0; sigma^2 in place of quantum pressure)
ff = sp.Function('fr')(t, x); dr_ = sp.Function('d')(t, x); tq = sp.Function('q')(t, x); Pp = sp.Function('U')(t, x)
u = sp.diff(ff, t) + Pp
L = (-nd * sp.diff(ff, x) ** 2 / 2 + mu ** 2 * u ** 2 / (2 * K) + sp.diff(u, x) ** 2 / (2 * K)
     - sp.diff(Pp, x) ** 2 / (2 * K) - (lam / (2 * K)) * sp.diff(ff, x, 2) ** 2
     - dr_ * (sp.diff(tq, t) + Pp) - rb * sp.diff(tq, x) ** 2 / 2 - (sig ** 2 / (2 * rb)) * dr_ ** 2
     - (al / 2) * rb * (sp.diff(ff, x) - sp.diff(tq, x)) ** 2)


def dispersion(Lag, fields):
    eqs = [sp.expand(e.lhs) for e in euler_equations(Lag, fields, [t, x])]
    rows = []
    for e in eqs:
        row = []
        for fld in fields:
            coef = 0
            for term in sp.Add.make_args(e):
                ds = [d for d in term.atoms(sp.Derivative) if d.expr == fld]
                if ds:
                    d = ds[0]
                    nt = sum(c for vv, c in d.variable_count if vv == t)
                    nx = sum(c for vv, c in d.variable_count if vv == x)
                    coef += (term / d) * (-sp.I * w) ** nt * (sp.I * kk) ** nx
                elif term.has(fld) and not any(dd.expr == fld for dd in term.atoms(sp.Derivative)):
                    coef += term / fld
            row.append(sp.expand(coef))
        rows.append(row)
    return sp.Matrix(rows)


M = dispersion(L, [ff, dr_, tq, Pp])
det = sp.expand(M.det(method='berkowitz'))
Pw = sp.Poly(det, w)
cA, cB, cC = [sp.factor(Pw.coeff_monomial(w ** p)) for p in (4, 2, 0)]
W0 = -K * (nd + rb)
k0 = sp.simplify(sp.limit(sp.cancel(det / kk ** 2), kk, 0).subs(w, sp.sqrt(W0)))
ser = sp.series(sp.expand((cA * (W0 + c1s * kk ** 2) ** 2 + cB * (W0 + c1s * kk ** 2) + cC) / kk ** 2), kk, 0, 3).removeO()
c1v = sp.factor(sp.solve(sp.expand(ser.coeff(kk, 2)), c1s)[0])
target = sig ** 2 * rb / (nd + rb) - lam + K * nd ** 2 / (mu ** 2 * (nd + rb))
c1_res = sp.simplify(c1v - target)
summ = sp.cancel(-cB / cA); prod = sp.cancel(cC / cA)
lim_sum = sp.limit(summ / kk ** 2, kk, sp.oo)
lim_prod = sp.factor(sp.limit(prod / kk ** 2, kk, sp.oo))
lim_small = sp.factor(sp.limit(prod / summ, kk, sp.oo))
small_res = sp.simplify(lim_small + lam * (K * rb + mu ** 2 * sig ** 2) / sig ** 2)
say('C3 collisionless fluid limit: Jeans root -K(n_d + rho) at k -> 0, residual:', k0)
say('C3 growing root k^2 coefficient c1 =', c1v)
say('   c1 - [sigma^2 rho/(n_d + rho) - lambda_s + K n_d^2/(mu_K^2 (n_d + rho))], residual:', c1_res)
say('C3 large k: (sum of roots)/k^2 ->', lim_sum, ';  (product)/k^2 ->', lim_prod, ';  small root -> product/sum ->', lim_small)
say('   small root + lambda_s (K rho + mu_K^2 sigma^2)/sigma^2, residual:', small_res)
say('   so the growing branch saturates at omega^2 = -lambda_s (K rho + mu_K^2 sigma^2)/sigma^2: bounded for sigma > 0, rate ~ sqrt(lambda_s)/sigma x Jeans;')
say('   it is no faster than Jeans iff lambda_s (K rho + mu_K^2 sigma^2)/sigma^2 <= K (n_d + rho), i.e. sigma^2 >= lambda_s up to O(n_d/rho, mu_K^2 sigma^2/(K rho)).')
RES['C3_k0_Jeans_residual'] = str(k0)
RES['C3_c1'] = str(c1v)
RES['C3_c1_residual'] = str(c1_res)
RES['C3_large_k'] = {'sum_over_k2': str(lim_sum), 'product_over_k2': str(lim_prod), 'small_root_limit': str(lim_small),
                     'small_root_residual': str(small_res)}
# numbers: lambda_s from SMF1's band reference (ell at the 10 kpc halo density of log M_b 10.45, alpha = 1)
G = 4.30091e-6
rho_gal = 137.0 ** 2 / (4 * math.pi * G * 10.0 ** 2)
lam_1kpc = 4 * math.pi * G * rho_gal * 1.0 ** 2
cbar = 9.199
ell_max = cbar / math.sqrt(4 * math.pi * G * rho_gal)
RES['C3_numbers'] = {'lambda_s_at_ell_1kpc_kms2': lam_1kpc, 'sigma_forest_kms': cbar,
                     'peak_growth_over_Jeans_ell_1kpc_sigma_forest': math.sqrt(lam_1kpc) / cbar,
                     'ell_max_kpc_for_sigma2_ge_lambda_s_alpha1': ell_max,
                     'note': 'fluid stand-in for a kinetic carrier; valid below the free-streaming scale'}
say(f'C3 numbers: lambda_s = {lam_1kpc:.3g} (km/s)^2 at ell = 1 kpc (alpha = 1); with sigma at the forest line ({cbar} km/s)'
    f' the band is removed only if ell <= {ell_max:.2f} kpc (alpha = 1; ell_max ~ 1/sqrt(alpha)). A CDM-cold carrier'
    f' (sigma -> 0) has the band with no cutoff in this limit. At ell = 1 kpc and sigma = {cbar} km/s the saturated rate is'
    f' {math.sqrt(lam_1kpc) / cbar:.2f} x Jeans.')
RES['C3_PASS'] = bool(k0 == 0 and c1_res == 0 and small_res == 0)
RES['runtime_s'] = time.time() - T0
RES['note'] = 'Adopts nothing. kappa = 1/2 FITTED; not theory closed.'
say(f'runtime {RES["runtime_s"]:.1f} s')
say('Adopts nothing. kappa = 1/2 FITTED; not theory closed.')
json.dump(RES, open(os.path.join(HERE, 'smf1_a1_collisionless.json'), 'w'), indent=1, default=str)
open(os.path.join(HERE, 'smf1_a1_collisionless.out'), 'w').write('\n'.join(OUT) + '\n')
# Adopts nothing. kappa = 1/2 FITTED; not theory closed.
