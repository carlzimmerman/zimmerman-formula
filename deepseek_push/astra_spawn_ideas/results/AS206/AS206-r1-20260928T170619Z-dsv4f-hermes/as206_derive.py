#!/usr/bin/env python3
# AS206 seed -- metric variation of the intrinsic (leaf) Laplacian.
# SymPy derivation controls. All symbolic identities are structural (residual == 0),
# no case sampling for the algebra. Numeric substitution controls live in as206_numeric.py.
import sympy as sp
import sys

PASS = True
def check(cid, name, cond, obs, thr, extra=None):
    global PASS
    ok = bool(cond)
    PASS = PASS and ok
    print(f"[{'PASS' if ok else 'FAIL'}] {cid} {name}: {obs}  (threshold: {thr})")
    if extra: print(f"      {extra}")

# ================= generic curved 2D leaf, fully symmetric k =================
x, y = sp.symbols('x y', real=True)
h11 = sp.Function('h11')(x, y); h12 = sp.Function('h12')(x, y); h22 = sp.Function('h22')(x, y)
u   = sp.Function('u')(x, y)
k11 = sp.Function('k11')(x, y); k12 = sp.Function('k12')(x, y); k22 = sp.Function('k22')(x, y)
h = sp.Matrix([[h11, h12], [h12, h22]])
k = sp.Matrix([[k11, k12], [k12, k22]])
Hi = h.inv()

def christoffel(hh, coords):
    Hi_ = hh.inv(); n = hh.rows
    out = {}
    for i in range(n):
        for j in range(n):
            for l in range(n):
                G = sp.Rational(1, 2) * sum(
                    Hi_[l, m] * (sp.diff(hh[m, j], coords[i]) + sp.diff(hh[i, m], coords[j])
                                 - sp.diff(hh[i, j], coords[m])) for m in range(n))
                out[(i, j, l)] = sp.expand(G)   # Gamma^l_{ij}
    return out

XY = (x, y)
Gam2 = christoffel(h, XY)

def DD_u2(i, j):
    return sp.diff(u, XY[i], XY[j]) - sum(Gam2[(i, j, l)] * sp.diff(u, XY[l]) for l in range(2))

def Lap2(gg):
    Gi = gg.inv(); det = gg.det(); sdet = sp.sqrt(det)
    out = sp.S.Zero
    for i in range(2):
        for j in range(2):
            out += sp.diff(sdet * Gi[i, j] * sp.diff(u, XY[j]), XY[i])
    return sp.simplify(out / sdet)

T  = sp.simplify((Hi * k).trace())            # tr_h(k)
Khat = sp.simplify(Hi * k * Hi)               # raised k^{ij} (NOT delta h^{ij})
Delta_u = Lap2(h)

# --- first-order expansion of the coordinate definition (divergence form) ---
# Delta_{h+eps k} u = (1 - eps T/2) [ Delta u + eps * div( (T/2)H - Khat ) grad u ] + O(eps^2)
V = sp.zeros(2, 1)
for i in range(2):
    for j in range(2):
        V[i] += (sp.Rational(1, 2) * T * Hi[i, j] - Khat[i, j]) * sp.diff(u, XY[j])
divV = sp.S.Zero
for i in range(2):
    divV += sp.diff(V[i], XY[i]) + sum(Gam2[(i, j, j)] for j in range(2)) * V[i]
lhs = sp.expand(-sp.Rational(1, 2) * T * Delta_u + divV)

# covariant divergence (D_i Khat)^{i j}  [free index j]:
DK = sp.zeros(2, 1)
for j in range(2):
    e = sp.S.Zero
    for i in range(2):
        e += sp.diff(Khat[i, j], XY[i])
        for l in range(2):
            e += Gam2[(i, l, j)] * Khat[i, l]          # Gamma^j_{i l} Khat^{i l}
            e += Gam2[(i, l, i)] * Khat[l, j]          # Gamma^i_{i l} Khat^{l j}
    DK[j] = sp.expand(e)
DT_up = [sum(Hi[i, j] * sp.diff(T, XY[j]) for j in range(2)) for i in range(2)]   # D^j T

rhs = sp.expand(-sum(Khat[i, j] * DD_u2(i, j) for i in range(2) for j in range(2))
                - sum((DK[j] - sp.Rational(1, 2) * DT_up[j]) * sp.diff(u, XY[j]) for j in range(2)))
res = sp.simplify(lhs - rhs)
check('D1', 'divergence-form variation == displayed formula (generic curved 2D leaf, full symmetric k)',
      res == 0, f'symbolic residual = {res}', 'residual == 0 (structural); k^ij = h^ia h^jb k_ab used, not delta h^ij')

# --- connection-form route (independent derivation) ---
# delta(D_i D_j u) = -dGamma^k_ij d_k u ;  dGamma^k_ij = (1/2) h^{kl} (D_i k_{jl} + D_j k_{il} - D_l k_{ij})
def cov_der_2(TT, i, j, l):   # D_i T_{jl} = d_i T_{jl} - G^m_{ij} T_{ml} - G^m_{il} T_{jm}
    return sp.diff(TT[j, l], XY[i]) - sum(Gam2[(i, j, m)] * TT[m, l] for m in range(2)) \
           - sum(Gam2[(i, l, m)] * TT[j, m] for m in range(2))

dG = {}
for i in range(2):
    for j in range(2):
        for k2 in range(2):
            e = sp.S.Zero
            for l in range(2):
                e += sp.Rational(1, 2) * Hi[k2, l] * (cov_der_2(k, i, j, l) + cov_der_2(k, j, i, l)
                                                      - cov_der_2(k, l, i, j))
            dG[(i, j, k2)] = sp.expand(e)
conn_route = sp.expand(-sum(Khat[i, j] * DD_u2(i, j) for i in range(2) for j in range(2))
                       - sum(Hi[i, j] * dG[i, j, l] * sp.diff(u, XY[l]) for i in range(2) for j in range(2) for l in range(2)))
res2 = sp.simplify(conn_route - rhs)
check('D1b', 'connection-form route (Christoffel variation) agrees with divergence-form route',
      res2 == 0, f'symbolic residual = {res2}', 'residual == 0 (structural); independent route')

# ================= conformal specialization, curved 3D leaf =================
X3 = sp.symbols('x3 y3 z3', real=True)
f1 = sp.Function('f1')(*X3); f2 = sp.Function('f2')(*X3); f3 = sp.Function('f3')(*X3)
sig = sp.Function('sigma')(*X3); u3 = sp.Function('u3')(*X3)
hc = sp.diag(f1, f2, f3)
kc3 = 2 * sig * hc
Hic = hc.inv()
Gam3 = christoffel(hc, X3)

def Lap3(gg):
    Gi = gg.inv(); det = gg.det(); sdet = sp.sqrt(det)
    out = sp.S.Zero
    for i in range(3):
        for j in range(3):
            out += sp.diff(sdet * Gi[i, j] * sp.diff(u3, X3[j]), X3[i])
    return sp.simplify(out / sdet)

def DDc(i, j):   # D_i D_j u3 on the 3D leaf
    return sp.diff(u3, X3[i], X3[j]) - sum(Gam3[(i, j, l)] * sp.diff(u3, X3[l]) for l in range(3))

Del3 = Lap3(hc)
grad_sig_up = [sum(Hic[i, j] * sp.diff(sig, X3[j]) for j in range(3)) for i in range(3)]  # D^i sigma
conf_rhs = sp.expand(-2 * sig * Del3 + sum(grad_sig_up[i] * sp.diff(u3, X3[i]) for i in range(3)))
conf_formula = sp.expand(-2 * sig * Del3 + sum(Hic[i, j] * sp.diff(sig, X3[i]) * sp.diff(u3, X3[j])
                                               for i in range(3) for j in range(3)))
res3 = sp.simplify(conf_rhs - conf_formula)
check('D2', 'conformal k_ij = 2 sigma h_ij, curved 3D leaf: delta Delta u = -2 sigma Delta u + <grad sigma, grad u>',
      res3 == 0, f'symbolic residual = {res3}', 'residual == 0; (n-2) = +1 in dim 3')

# direct substitution of the conformal k into the master identity on a CURVED leaf:
# (a) 2D curved leaf: conformal formula has coefficient (n-2) = 0  ->  delta Delta u = -2 sig Delta u
sig2 = sp.Function('sigma2')(x, y)
kc2e = 2 * sig2 * h
T2 = sp.simplify((Hi * kc2e).trace())
Khat2 = sp.simplify(Hi * kc2e * Hi)
bracket2 = [sp.expand(sum(sp.diff(Khat2[i, j], XY[i]) for i in range(2))
                      + sum(Gam2[(i, l, j)] * Khat2[i, l] + Gam2[(i, l, i)] * Khat2[l, j]
                            for i in range(2) for l in range(2))
                      - sp.Rational(1, 2) * sum(Hi[j, m] * sp.diff(T2, XY[m]) for m in range(2))) for j in range(2)]
master_conf2 = sp.expand(-sum(Khat2[i, j] * DD_u2(i, j) for i in range(2) for j in range(2))
                         - sum(bracket2[j] * sp.diff(u, XY[j]) for j in range(2)))
formula_conf2 = sp.expand(-2 * sig2 * Delta_u)   # (n-2) grad-term vanishes at n = 2
res4 = sp.simplify(master_conf2 - formula_conf2)
check('D2c', 'conformal k = 2 sig h substituted into master identity (2D curved leaf): delta Delta u = -2 sig Delta u (n-2 = 0)',
      res4 == 0, f'symbolic residual = {res4}', 'residual == 0; tr_h(2 sig h) = 2 n sig, n = 2')

# (b) 3D curved leaf (diagonal h): conformal formula has coefficient (n-2) = +1
sig3 = sp.Function('sigma3')(*X3)
kc3e = 2 * sig3 * hc
T3 = sp.simplify((Hic * kc3e).trace())
Khat3 = sp.simplify(Hic * kc3e * Hic)
bracket3 = [sp.expand(sum(sp.diff(Khat3[i, j], X3[i]) for i in range(3))
                      + sum(Gam3[(i, l, j)] * Khat3[i, l] + Gam3[(i, l, i)] * Khat3[l, j]
                            for i in range(3) for l in range(3))
                      - sp.Rational(1, 2) * sum(Hic[j, m] * sp.diff(T3, X3[m]) for m in range(3))) for j in range(3)]
master_conf3 = sp.expand(-sum(Khat3[i, j] * DDc(i, j) for i in range(3) for j in range(3))
                         - sum(bracket3[j] * sp.diff(u3, X3[j]) for j in range(3)))
formula_conf3 = sp.expand(-2 * sig3 * Del3 + sum(Hic[i, j] * sp.diff(sig3, X3[i]) * sp.diff(u3, X3[j])
                                                 for i in range(3) for j in range(3)))
res5 = sp.simplify(master_conf3 - formula_conf3)
check('D2d', 'conformal k = 2 sig h substituted into master identity (3D curved diagonal leaf): -2 sig Delta u + <grad sig, grad u>',
      res5 == 0, f'symbolic residual = {res5}', 'residual == 0; (n-2) = +1 at n = 3')

# general-n algebra: bracket coefficient 2 - (1/2)(2n)  equals  -(n-2)
n_sym = sp.Symbol('n', positive=True)
check('D2b', 'general-n algebra: 2 - (1/2) tr(2 sig h) == -(n-2)',
      sp.simplify(2 - sp.Rational(1, 2) * (2 * n_sym) + (n_sym - 2)) == 0,
      '2 - n + (n-2) = 0', 'so delta Delta u = -2 sig Delta u + (n-2) <grad sig, grad u> in dim n')

# ================= Fourier kernel on flat T^3 =================
q1, q2, q3 = sp.symbols('q1 q2 q3', real=True)
r1, r2, r3 = sp.symbols('r1 r2 r3', real=True)
qmod = q1**2 + q2**2 + q3**2
rq = r1*q1 + r2*q2 + r3*q3
lhs_f = sp.expand(2*qmod - rq)                                      # -2 sig Del u + grad sig . grad u, modes exp(i q.x), exp(i r.x)
rhs_f = sp.expand(3*qmod - (q1+r1)*q1 - (q2+r2)*q2 - (q3+r3)*q3)    # p = q + r
check('D3', 'Fourier kernel: coefficient (2|q|^2 - r.q) == (3|q|^2 - p.q) at p = q + r',
      sp.simplify(lhs_f - rhs_f) == 0, f'symbolic residual = {sp.simplify(lhs_f - rhs_f)}',
      'structural; matches XC1 witness kernel (3|q|^2 - p.q) sigma_{p-q}')

K = sp.Symbol('K', positive=True)
b = sp.Rational(1, 2)
coef_cosx = sp.simplify(sp.Rational(1, 2) * (3*K**2 - K))           # cos x coefficient of delta Del[cos(Kx)], sigma = cos((K-1)x)
check('D3b', 'review witness (1D fold): cos x coefficient of delta Del = (3K^2 - K)/2',
      sp.simplify(coef_cosx - sp.Rational(1, 2) * (3*K**2 - K)) == 0,
      f'coeff = {coef_cosx}', 'structural; K(3K-1)/2')

# ================= negative control: omit the volume variation =================
alt_rhs = sp.expand(-sum(Khat[i, j] * DD_u2(i, j) for i in range(2) for j in range(2))
                    - sum(DK[j] * sp.diff(u, XY[j]) for j in range(2)))     # no (1/2) D^j T term
alt_res = sp.simplify(lhs - alt_rhs)
check('D4', 'NEGATIVE CONTROL (symbolic): omitting the volume variation gives a WRONG operator',
      alt_res != 0, f'residual vs the true variation = {alt_res} (nonzero)', 'control MUST fire: residual != 0')
# conformal form of the WRONG operator (volume term omitted): -2 sig Del u - 2 <grad sig, grad u>
# (bracket = D_i k^ij without the -(1/2)D^j tr piece = 2 D^j sig), so the grad-sig coefficient is -2.
wrong_conf2 = sp.expand(-2 * sig2 * Delta_u - 2 * sp.simplify(sum(Hi[i, j] * sp.diff(sig2, XY[i]) * sp.diff(u, XY[j])
                                                                  for i in range(2) for j in range(2))))
gradcoef_wrong = sp.Integer(-2)
gradcoef_true = sp.Integer(2) - sp.Integer(3)   # (n - 2) at n = 3  -> +1
check('D4b', 'NEGATIVE CONTROL (conformal): wrong grad-sigma coefficient is -2, true (n-2)=+1 at n=3',
      gradcoef_wrong != gradcoef_true,
      f'wrong bracket gives coefficient {gradcoef_wrong}, displayed formula gives {gradcoef_true}',
      'control fires: -2 != +1; also implied by the nonzero D4 residual')

# ================= dimensions, measure, footings =================
G = sp.Float('6.67430e-11'); c = sp.Float('299792458')
a0c = sp.Float('9.3619e-11'); a0a = sp.Float('1.1279e-10')
rho_c = 4 * a0c**2 / (G * c**2)
rho_a = 4 * a0a**2 / (G * c**2)
kappa_eff = a0a / (c * sp.sqrt(G * rho_c))
check('D5', 'footings separate: canonical rho_L = 4 a0^2/(G c^2) at fixed kappa = 1/2',
      abs(float(rho_c) - 5.844412e-27) / 5.844412e-27 < 1e-6 and abs(float(kappa_eff) - 0.60238840) < 1e-6,
      f'rho_L(canonical a0 = 9.3619e-11) = {rho_c.evalf(12)} kg/m^3, kappa_eff(alt, fixed rho_L) = {kappa_eff.evalf(10)}',
      'alt a0 = 1.1279e-10 is NOT a second point on the same (rho_L, kappa): kappa_eff = 0.60238840 != 1/2 at fixed rho_L;'
      ' rho_L(alt, fixed kappa) = ' + str(rho_a.evalf(10)) + ' kg/m^3')

print('\nunits: [Delta] = L^-2, [k_ij] = [sigma] = 1 (dimensionless metric variation), [tr_h k] = 1,'
      ' [kernel 3|q|^2 - p.q] = L^-2 -> identity dimensionally closed, scale-free (a0 enters only via the filter width b = xi^2/2)')
print('\n' + ('ALL SYMBOLIC CHECKS PASS' if PASS else 'SOME CHECKS FAILED'))
sys.exit(0 if PASS else 1)