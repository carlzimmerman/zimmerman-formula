#!/usr/bin/env python3
"""VSJ1 G2 (and KA3): what gravitates in a standing clock of action (A) kept whole. sympy, residuals must be 0.
QX17 (A) at gamma_L = 0, weak field, spherical, c = 1, K = 4 pi G. Writes vsj1_g2.json / vsj1_g2.out.
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import json, os
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
out = []; res = {}
r, a0, G, R = sp.symbols('r a_0 G R', positive=True)
K = 4 * sp.pi * G


def rec(key, text, residual):
    z = sp.simplify(residual)
    res[key] = {'statement': text, 'residual': str(z), 'pass': bool(z == 0)}
    out.append(f"{key}: {text} -> residual {z} -> {'PASS' if z == 0 else 'FAIL'}")


# (a) the acceleration of a static clock is grad ln N, whatever else is in the action (kinematic identity).
t, th, ph = sp.symbols('t theta phi')
N = sp.Function('N', positive=True)(r); B = sp.Function('B', positive=True)(r)
x = [t, r, th, ph]
g = sp.diag(-N ** 2, B ** 2, r ** 2, r ** 2 * sp.sin(th) ** 2); gi = g.inv()
Gam = [[[sum(gi[l, s] * (sp.diff(g[s, m], x[n]) + sp.diff(g[s, n], x[m]) - sp.diff(g[m, n], x[s])) for s in range(4)) / 2
         for n in range(4)] for m in range(4)] for l in range(4)]
n_dn = [-N, 0, 0, 0]                                   # n_m = -d_m tau / Q with tau = t, Q = 1/N
n_up = [sum(gi[m, k] * n_dn[k] for k in range(4)) for m in range(4)]
A = [sum(n_up[k] * (sp.diff(n_dn[m], x[k]) - sum(Gam[l][k][m] * n_dn[l] for l in range(4))) for k in range(4)) for m in range(4)]
rec('G2a', 'static clock (tau = t): A_r = d_r ln N, A_t = A_theta = A_phi = 0; no other field enters',
    sp.Abs(sp.simplify(A[1] - sp.diff(sp.log(N), r))) + sum(sp.Abs(sp.simplify(A[i])) for i in (0, 2, 3)))

# (b) E2 on the leaves: |A| = K W'(K|P|) gives K|P| = (1 - mu)|A|, mu(x) = x/(1 + x).
p, Aa = sp.symbols('p A', positive=True)
W = (a0 ** 2 / K) * (-p / a0 - sp.log(1 - p / a0))
KWp = sp.simplify(K * sp.diff(W, p))                    # = a0 p/(a0 - p)
mu = lambda u: u / (1 + u)
psol = (1 - mu(Aa / a0)) * Aa
rec('G2b', 'E2 leaves: K W\'(p) = A at p = K|P| = (1 - mu(A/a0)) A', sp.simplify(KWp.subs(p, psol) - Aa))

# (c) E3 charge rho_Q = div P + n_hot; E4_00 weak: lap Phi = K (rho_b + rho_Q)  =>  div[mu grad Phi] = K (rho_b + n_hot).
Phi = sp.Function('Phi')(r); rb = sp.Function('rho_b')(r); nh = sp.Function('n_hot')(r)
gf = sp.diff(Phi, r)                                    # g = Phi' = A_r (from a), taken positive
div = lambda F: sp.diff(r ** 2 * F, r) / r ** 2
Pr = (1 - mu(gf / a0)) * gf / K                          # from (b)
poisson = div(gf) - K * (rb + nh + div(Pr))
law = div(mu(gf / a0) * gf) - K * (rb + nh)
rec('G2c', 'E4_00 with rho_Q = div P + n_hot is div[mu grad Phi] = 4 pi G (rho_b + n_hot)', sp.simplify(poisson - law))
# isentropic hot dust (AKS1 T5h): h = c0 - Phi, n = (2h/(5 K_s))^(3/2), p = K_s n^(5/3): dp/dr = -n Phi'
Ks = sp.symbols('K_s', positive=True)
hd = sp.Function('h', positive=True)(r)                  # the depth h = c0 - Phi > 0, so Phi' = -h'
nd = (2 * hd / (5 * Ks)) ** sp.Rational(3, 2)
rec('G2c2', 'the hot static dust n_d(depth, s) is in hydrostatic balance in the total field: dp/dr = -n Phi\'',
    sp.simplify(sp.powsimp(sp.diff(Ks * nd ** sp.Rational(5, 3), r) - nd * sp.diff(hd, r), force=True)))

# (d) Gauss: polarization charge inside R is R^2 (g - g_N)/G; if P = 0 outside (free fall, A = 0) the layer is minus that.
gR, gN = sp.symbols('g g_N', positive=True)
QP = 4 * sp.pi * R ** 2 * ((1 - mu(gR / a0)) * gR / K)
rec('G2d', 'polarization charge inside R = R^2 (g - mu g)/G; layer at the edge = -4 pi R^2 P(R-); net 0',
    sp.simplify(QP - R ** 2 * (gR - mu(gR / a0) * gR) / G) + sp.simplify(QP + (-4 * sp.pi * R ** 2 * (1 - mu(gR / a0)) * gR / K)))

# (e) VSH1's force law at rest: 0 = -g_Nb - y + U(y) + f, U(y) = a0 y/(a0 - y), y = G Q/r^2, f = pressure acceleration.
y, f, gNb = sp.symbols('y f g_Nb', positive=True)
U = lambda u: a0 * u / (a0 - u)
yA = (1 - mu(gR / a0)) * gR                              # (A)'s polarization field for total field g
e1 = sp.simplify(U(yA) - gR)                             # with all charge polarization and f = 0: U(y) = g, the law
e2 = sp.simplify((U(yA) - yA) - mu(gR / a0) * gR)        # U(y) - y = g_N of the real sources
dUy = sp.simplify(sp.diff(U(y) - y, y) - (a0 ** 2 / (a0 - y) ** 2 - 1))
rec('G2e', 'VSH1\'s rest condition U(y) - y = g_Nb - f equals (A)\'s U(y_A) - y_A = g_N(real sources) only at f = 0',
    sp.Abs(e1) + sp.Abs(e2) + sp.Abs(dUy))
out.append('    so with pressure support (f > 0) VSH1\'s polarization y is below (A)\'s y_A: d(U - y)/dy = a0^2/(a0 - y)^2 - 1 > 0.')
out.append('    In (A) kept whole E2 ties P to the clock\'s total acceleration (G2a), so a clock at rest carries the full')
out.append('    polarization of the total field whatever holds it up; the pressure belongs to the dust part n_hot.')

# KA3 SIS identities and the law's closed form.
sig, Mb, rr = sp.symbols('sigma M_b r', positive=True)
rho_sis = sig ** 2 / (2 * sp.pi * G * rr ** 2)
M_sis = sp.integrate(4 * sp.pi * rr ** 2 * rho_sis, (rr, 0, R))
k1 = sp.simplify(M_sis - 2 * sig ** 2 * R / G)
k2 = sp.simplify(G * M_sis / R - 2 * sig ** 2)           # v_c^2 = 2 sigma^2
vf4 = G * Mb * a0                                        # deep law: v_f^4 = G M_b a0, phantom SIS with 2 sigma^2 = v_f^2
k3 = sp.simplify((sp.sqrt(vf4) / 2) ** 2 - G * Mb * a0 / 4)
xx = sp.symbols('x', positive=True)
XL = (sp.sqrt(1 + 4 * xx ** 2) - 1) / 2
gNx = 1 / xx ** 2                                        # g_N/a0 at x = r/r_M
gx = gNx * (1 + XL)                                      # g/a0
k4 = sp.simplify(gx ** 2 - gNx * (gx + 1))               # law S: g^2 = g_N (g + a0)
k5 = sp.simplify(mu(gx) * gx - gNx)                      # equivalently mu(g/a0) g = g_N
rec('KA3', 'SIS: M = 2 sigma^2 r/G, v_c^2 = 2 sigma^2; deep law sigma^4 = G M_b a0/4; X_L solves g^2 = g_N (g + a0)',
    sp.Abs(k1) + sp.Abs(k2) + sp.Abs(k3) + sp.Abs(k4) + sp.Abs(k5))

res['G2_pass'] = all(res[k]['pass'] for k in ('G2a', 'G2b', 'G2c', 'G2c2', 'G2d', 'G2e'))
res['KA3_pass'] = res['KA3']['pass']
out.append(f"G2: {'PASS' if res['G2_pass'] else 'FAIL'}; KA3: {'PASS' if res['KA3_pass'] else 'FAIL'}")
out.append('Statement fixed by G2: inside the standing region mu(g/a0) g = G [M_b + M_hot(<r)]/r^2; the gravitating density is')
out.append('rho_b + n_hot + div P, the law\'s phantom of (baryons + real hot charge); outside, g = G [M_b + Q(<r)]/r^2; a layer of')
out.append('minus the phantom mass sits at the edge.')
out.append('Adopts nothing. kappa = 1/2 FITTED; not theory closed.')
json.dump(res, open(os.path.join(HERE, 'vsj1_g2.json'), 'w'), indent=1)
open(os.path.join(HERE, 'vsj1_g2.out'), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
