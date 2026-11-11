#!/usr/bin/env python3
"""SET1 A1a: exact (sympy) checks of the spherical fixed point with an isotropic target pressure P = J(g).

    python3 set1_a1_sym.py                 -> set1_a1_sym.out / .json
    SET1_MUTATE=M2 python3 set1_a1_sym.py  -> set1_a1_sym_MUTATE_M2.out / .json  (identity checked against 2 a0 rho_b)

g is the magnitude of the inward total field, u = g/a0, K = 4 pi G, J(g) = (a0^2/K)[u - ln(1 + u)], mu(u) = u/(1 + u).
Jeans (isotropic, static): dP/dr = -rho_c g.  Poisson: (1/r^2) d(r^2 g)/dr = K (rho_b + rho_c).
TEST lane (FROZEN_CRITERIA.md section 3, A1a). Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json, os, sys
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get('SET1_MUTATE', '')
r, a0, G, M = sp.symbols('r a0 G M', positive=True)
K = 4 * sp.pi * G
gf = sp.Function('g')(r)
u = gf / a0
mu = u / (1 + u)
J = a0 ** 2 / K * (u - sp.log(1 + u))
lines, res = [], {}


def out(s):
    print(s); lines.append(s)


def z(expr):
    return sp.simplify(sp.together(sp.expand(expr)))


# (i) Jeans + Poisson with P = J(g)  <=>  F(g) = K rho_b
rho_c_jeans = -sp.diff(J, r) / gf
Krho_b = sp.diff(r ** 2 * gf, r) / r ** 2 - K * rho_c_jeans
F = sp.diff(gf, r) * (2 + u) / (1 + u) + 2 * gf / r
res['i_JP_equals_F'] = str(z(Krho_b - F))
law_lhs = sp.diff(r ** 2 * mu * gf, r) / r ** 2
res['i_law_equals_muF'] = str(z(law_lhs - mu * F))
res['i_Jprime'] = str(z(sp.diff(J, gf) - gf / (K * (1 + u))))
out(f"(i)  [Jeans+Poisson with P=J] - F(g) = {res['i_JP_equals_F']};  (1/r^2) d(r^2 mu g)/dr - mu F = {res['i_law_equals_muF']};"
    f"  J'(g) - g/(K(1+u)) = {res['i_Jprime']}")

# (ii) the law's state put into Jeans with P = J: residual dJ/dr + rho_ph g, against a0 rho_b
Mb = r ** 2 * mu * gf / G                      # the law: mu g = g_N = G M_b(<r)/r^2 defines M_b(<r)
rho_b = sp.diff(Mb, r) / (4 * sp.pi * r ** 2)
gN = G * Mb / r ** 2
rho_ph = sp.diff(r ** 2 * (gf - gN), r) / (K * r ** 2)
resid = sp.diff(J, r) + rho_ph * gf
coef = 2 if MUT == 'M2' else 1
res['ii_resid_minus_a0rhob'] = str(z(resid - coef * a0 * rho_b))
out(f"(ii) law state in Jeans with P=J: [dJ/dr + rho_ph g] - {coef} a0 rho_b = {res['ii_resid_minus_a0rhob']}")
# the anisotropy of M5's field stress in spherical symmetry: Pi_rr - Pi_tt = -g^2/(K(1+u)) = -a0 g_N/K
res['ii_anisotropy'] = str(z(gf ** 2 / (K * (1 + u)) - a0 * gN / K))
out(f"     g^2/(K(1+u)) - a0 g_N/K = {res['ii_anisotropy']}  (so div of the anisotropic part = -a0 rho_b radially)")

# (iii) point mass: residual 0 for r > 0 (rho_b = 0) -- parametrize the exact law by u
uu, x = sp.symbols('u x', positive=True)
# exact point-mass law: mu(u) g = G M / r^2  ->  r^2 = G M (1+u)/(a0 u^2)
r_of_u = sp.sqrt(G * M * (1 + uu) / (a0 * uu ** 2))
g_u = a0 * uu
J_u = a0 ** 2 / K * (uu - sp.log(1 + uu))
dJdr = sp.diff(J_u, uu) / sp.diff(r_of_u, uu)
Mtot_u = r_of_u ** 2 * g_u / G
rho_ph_u = (sp.diff(Mtot_u, uu) / sp.diff(r_of_u, uu)) / (4 * sp.pi * r_of_u ** 2)       # M_b const outside the point
res['iii_point_mass_residual'] = str(z(dJdr + rho_ph_u * g_u))
out(f"(iii) point mass, exact law: dJ/dr + rho_ph g = {res['iii_point_mass_residual']}")
# closed-form M_ph against the parametrization
xr = r_of_u / sp.sqrt(G * M / a0)
Mph_closed = M * (sp.sqrt(sp.factor(sp.simplify(1 + 4 * xr ** 2))) - 1) / 2     # 1 + 4x^2 = (u+2)^2/u^2 on u > 0
res['iii_Mph_closed_form'] = str(z(Mtot_u - M - Mph_closed))
out(f"      M_tot - M_b - M_b(sqrt(1+4x^2)-1)/2 = {res['iii_Mph_closed_form']}")
# deep-field known answer: sigma^2 = J/rho_ph -> (1/2) sqrt(G M a0); rho -> sigma^2/(2 pi G r^2)
sig2 = sp.simplify(J_u / rho_ph_u)
lim_sig2 = sp.limit(sig2, uu, 0, '+')
res['iii_sigma2_deep_over_sqrtGMa0'] = str(sp.simplify(lim_sig2 / sp.sqrt(G * M * a0)))
iso = sp.limit(rho_ph_u / (lim_sig2 / (2 * sp.pi * G * r_of_u ** 2)), uu, 0, '+')
res['iii_rho_over_isothermal_deep'] = str(sp.simplify(iso))
lim_newt = sp.limit(sig2 / (G * M / (2 * r_of_u)), uu, sp.oo)
res['iii_sigma2_newtonian_over_GM_2r'] = str(sp.simplify(lim_newt))
out(f"      deep: sigma^2/sqrt(G M a0) -> {res['iii_sigma2_deep_over_sqrtGMa0']};  rho_ph / [sigma^2/(2 pi G r^2)] -> "
    f"{res['iii_rho_over_isothermal_deep']};  Newtonian: sigma^2/(G M/2r) -> {res['iii_sigma2_newtonian_over_GM_2r']}")

# (iv) uniqueness: outside the baryons F = 0 <=> d(r^2 mu g)/dr = 0; family r^2 mu g = C
res['iv_dYdr_equals_r2muF'] = str(z(sp.diff(r ** 2 * mu * gf, r) - r ** 2 * mu * F))
C = sp.symbols('C', positive=True)
# as r -> 0 on the family: u -> oo, mu -> 1, r^2 g -> C, so the enclosed total mass at 0+ is C/G
r_C = sp.sqrt(C * (1 + uu) / (a0 * uu ** 2))
res['iv_r2g_at_centre_over_C'] = str(sp.limit(r_C ** 2 * a0 * uu / C, uu, sp.oo))
out(f"(iv) d(r^2 mu g)/dr - r^2 mu F = {res['iv_dYdr_equals_r2muF']};  on r^2 mu g = C: r^2 g / C -> "
    f"{res['iv_r2g_at_centre_over_C']} at the centre, so a central total mass C/G = M_b + m_c (cold point mass m_c)")

# (v) any cored profile: centre is deep (g -> 0) and the P=J state has g ~ c r with c = K rho_b0/4 -> rho_c(0) = -rho_b0/4
c, rb0 = sp.symbols('c rho_b0', positive=True)
lin = sp.limit((F.subs(gf, c * r).doit()) , r, 0)
csol = sp.solve(sp.Eq(lin, K * rb0), c)[0]
rho_c0 = sp.limit((-sp.diff(J, r) / gf).subs(gf, csol * r).doit(), r, 0)
res['v_centre_slope_over_Krhob0'] = str(sp.simplify(csol / (K * rb0)))
res['v_rho_c_centre_over_rho_b0'] = str(sp.simplify(rho_c0 / rb0))
out(f"(v)  cored centre: g = c r with c/(K rho_b0) = {res['v_centre_slope_over_Krhob0']};  rho_c(0)/rho_b(0) = "
    f"{res['v_rho_c_centre_over_rho_b0']}  (any mass, any cored profile)")

# (vi) deep-limit closed forms used as known answer KA3 (deep F: 2 g' + 2 g / r = K rho_b)
b, a = sp.symbols('b a', positive=True)
gP = G * M / (2 * r * b) * (1 - (1 + r ** 2 / b ** 2) ** sp.Rational(-3, 2))
rhoP = 3 * M / (4 * sp.pi * b ** 3) * (1 + r ** 2 / b ** 2) ** sp.Rational(-5, 2)
gH = G * M * (r + 2 * a) / (2 * a * (r + a) ** 2)
rhoH = M * a / (2 * sp.pi * r * (r + a) ** 3)
res['vi_plummer_deep_closed'] = str(z(2 * sp.diff(gP, r) + 2 * gP / r - K * rhoP))
res['vi_hernquist_deep_closed'] = str(z(2 * sp.diff(gH, r) + 2 * gH / r - K * rhoH))
res['vi_hernquist_deep_gprime'] = str(sp.factor(sp.simplify(sp.diff(gH, r))))
out(f"(vi) deep closed forms: Plummer {res['vi_plummer_deep_closed']}, Hernquist {res['vi_hernquist_deep_closed']};"
    f" Hernquist deep g' = {res['vi_hernquist_deep_gprime']} (< 0: rho_c > 0)")

ok_main = all(res[k] == '0' for k in ('i_JP_equals_F', 'i_law_equals_muF', 'i_Jprime', 'ii_resid_minus_a0rhob',
                                      'ii_anisotropy', 'iii_point_mass_residual', 'iii_Mph_closed_form',
                                      'iv_dYdr_equals_r2muF', 'vi_plummer_deep_closed', 'vi_hernquist_deep_closed'))
ok_vals = (res['iii_sigma2_deep_over_sqrtGMa0'] == '1/2' and res['iii_rho_over_isothermal_deep'] == '1'
           and res['iii_sigma2_newtonian_over_GM_2r'] == '1' and res['iv_r2g_at_centre_over_C'] == '1'
           and res['v_centre_slope_over_Krhob0'] == '1/4' and res['v_rho_c_centre_over_rho_b0'] == '-1/4')
res['all_exact_checks_pass'] = bool(ok_main and ok_vals)
out(f"ALL A1a CHECKS {'PASS' if res['all_exact_checks_pass'] else 'FAIL'}" + (f"  (MUTATE {MUT})" if MUT else ''))
out('Adopts nothing. kappa = 1/2 FITTED; not theory closed.')
stem = 'set1_a1_sym' + (f'_MUTATE_{MUT}' if MUT else '')
open(os.path.join(HERE, stem + '.out'), 'w').write('\n'.join(lines) + '\n')
json.dump(res, open(os.path.join(HERE, stem + '.json'), 'w'), indent=1)
sys.exit(0 if res['all_exact_checks_pass'] else 1)
