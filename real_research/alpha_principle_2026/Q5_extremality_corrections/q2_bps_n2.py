#!/usr/bin/env python3
"""Q5 / item 2: 4D N=2 supergravity BPS bound as an exact equality, and whether it forces a gauge coupling.
One-modulus cubic ('t^3') model F = -(X^1)^3/X^0 and pure N=2 supergravity F = -(i/4)(X^0)^2 (formulas RECALLED,
validated numerically by the black-hole-potential identity, check Q2-H1).

Real run:     python3 q2_bps_n2.py           -> exit 0
MUTATE ctrl:  python3 q2_bps_n2.py MUTATE    -> the ONLY trigger is the literal argv 'MUTATE'
              (Kahler-covariant derivative without the K_t term: Q2-H1 and Q2-H2 must FAIL, exit 1)
"""
import sys
import numpy as np
import sympy as sp

MUTATE = (len(sys.argv) > 1 and sys.argv[1] == 'MUTATE')
res = []
def check(name, ok, info=""):
    res.append(bool(ok))
    print(("[PASS] " if ok else "[FAIL] ") + name + (("  " + info) if info else ""))

# ------------------------------------------------------------------ t^3 model, symbolic pieces
t, tb = sp.symbols('t tb')            # t and its conjugate treated as independent symbols
X = [1, t]; Xb = [1, tb]
F = lambda X0, X1: -X1**3 / X0
X0s, X1s = sp.symbols('X0 X1')
Fs = F(X0s, X1s)
FI = [sp.diff(Fs, X0s), sp.diff(Fs, X1s)]
FIJ = sp.Matrix(2, 2, lambda i, j: sp.diff(Fs, [X0s, X1s][i], [X0s, X1s][j]))
sub = {X0s: 1, X1s: t}
subb = {X0s: 1, X1s: tb}
FI_t = [e.subs(sub) for e in FI]; FIb = [e.subs(subb) for e in FI]     # F_I(t), conj(F_I) = F_I(tb)
FIJ_t = FIJ.subs(sub); FIJb = FIJ.subs(subb)
eK_inv = sp.simplify(sp.I * (sum(Xb[i] * FI_t[i] for i in range(2)) - sum(X[i] * FIb[i] for i in range(2))))
Kpot = -sp.log(eK_inv)
Kt = sp.simplify(sp.diff(Kpot, t))
Ktb = sp.simplify(sp.diff(Kpot, tb))
gtt = sp.simplify(sp.diff(Kpot, t, tb))
# N_IJ = conj(F_IJ) + 2i (Im F X)_I (Im F X)_J / (X Im F X);  Im F_IJ = (F_IJ - conj F_IJ)/(2i)
ImF = (FIJ_t - FIJb) / (2 * sp.I)
ImFX = ImF * sp.Matrix(X)
den = (sp.Matrix(X).T * ImF * sp.Matrix(X))[0, 0]
N = FIJb + 2 * sp.I * (ImFX * ImFX.T) / den
N = sp.simplify(N)
x_, y_ = sp.symbols('x y', real=True)
Ntxy = N.subs({t: x_ + sp.I * y_, tb: x_ - sp.I * y_})
ImN_sym = sp.simplify(sp.im(sp.expand(Ntxy)))
print("e^{-K}     =", sp.simplify(eK_inv.subs({t: x_ + sp.I * y_, tb: x_ - sp.I * y_})))
print("g_{t tbar} =", sp.simplify(gtt.subs({t: x_ + sp.I * y_, tb: x_ - sp.I * y_})))
print("Im N (symbolic in t=x+iy):"); sp.pprint(ImN_sym)

eK_f = sp.lambdify((t, tb), 1 / eK_inv, 'numpy')
Kt_f = sp.lambdify((t, tb), Kt, 'numpy')
g_f = sp.lambdify((t, tb), gtt, 'numpy')
N_f = sp.lambdify((t, tb), N, 'numpy')
FI_f = sp.lambdify(t, FI_t, 'numpy')
W_of = lambda tt, p, q: q[0] * 1 + q[1] * tt - (p[0] * FI_f(tt)[0] + p[1] * FI_f(tt)[1])   # q_I X^I - p^I F_I
dW_of = lambda tt, p, q, h=1e-6: (W_of(tt + h, p, q) - W_of(tt - h, p, q)) / (2 * h)       # holomorphic derivative (analytic fn)

def quantities(tt, p, q):
    ttb = np.conj(tt)
    eK = np.real(eK_f(tt, ttb)); K_t = Kt_f(tt, ttb); g = np.real(g_f(tt, ttb))
    W = W_of(tt, p, q); dW = dW_of(tt, p, q)
    Zabs2 = eK * abs(W)**2
    DW = dW if MUTATE else dW + K_t * W      # D_t Z = e^{K/2}(d_t W + K_t W)   (MUTATE drops K_t)
    DZabs2 = eK * abs(DW)**2 / g
    Nm = np.array(N_f(tt, ttb), dtype=complex)
    ReN, ImN = Nm.real, Nm.imag
    ImNi = np.linalg.inv(ImN)
    M = np.block([[ImN + ReN @ ImNi @ ReN, -ReN @ ImNi], [-ImNi @ ReN, ImNi]])
    Qv = np.array(list(p) + list(q), dtype=float)
    VBH = -0.5 * Qv @ M @ Qv
    return Zabs2, DZabs2, VBH, ImN

# ------------------------------------------------------------------ Q2-H1 convention check
rng = np.random.default_rng(20260928)
maxrel = 0.0
for _ in range(200):
    tt = rng.normal() + 1j * np.exp(rng.uniform(-1.5, 1.5))
    p = rng.integers(-5, 6, 2); q = rng.integers(-5, 6, 2)
    if not (p.any() or q.any()):
        continue
    Z2, DZ2, V, ImN = quantities(tt, p, q)
    maxrel = max(maxrel, abs(Z2 + DZ2 - V) / max(V, 1e-30))
    # Im N negative definite
    if np.max(np.linalg.eigvalsh(ImN)) >= 0:
        maxrel = 1e9
print("max |(|Z|^2+|DZ|^2) - V_BH| / V_BH over 200 random points =", maxrel)
check("Q2-H1 V_BH = -1/2 Q^T M Q = |Z|^2 + |D_t Z|^2 at 200 random (t, charges); Im N negative definite", maxrel < 1e-6)

# ------------------------------------------------------------------ Q2-H2 BPS equality only on the attractor locus
# D0-D4 charges: p^1 = p > 0, q_0 = q < 0  (regular attractor t* = i sqrt(|q|/p)); W = q0 - p F_1 = q0 + 3 p t^2
p_ = np.array([0, 1]); q_ = np.array([-3, 0])
tstar = 1j * np.sqrt(3.0)
Z2s, DZ2s, Vs, _ = quantities(tstar, p_, q_)
print(f"attractor t* = i sqrt(3): |Z|^2 = {Z2s:.6f}  |DZ|^2 = {DZ2s:.3e}  V_BH = {Vs:.6f}")
check("Q2-H2a at the attractor DZ = 0 and |Z|^2 = V_BH (BPS mass = RN-type extremal value)", DZ2s < 1e-9 and abs(Z2s - Vs) < 1e-6 * Vs)
ratios = []
for yy in np.exp(np.linspace(-2, 2, 41)):
    if abs(yy - np.sqrt(3.0)) < 1e-9:
        continue
    for xx in (0.0, 0.7):
        Z2, DZ2, V, _ = quantities(xx + 1j * yy, p_, q_)
        ratios.append(np.sqrt(V / Z2))
ratios = np.array(ratios)
print(f"off-attractor z_g = sqrt(V_BH)/|Z| : min {ratios.min():.4f} max {ratios.max():.4f} (equals 1 only at t*)")
check("Q2-H2b off the attractor V_BH > |Z|^2 strictly: the gauge(+scalar)-charge-to-BPS-mass ratio z_g > 1 and varies with the modulus", ratios.min() > 1 + 1e-6)

# ------------------------------------------------------------------ Q2-H3 coupling is a free function of the modulus
y = sp.symbols('y', positive=True)
Nfun = sp.lambdify(y, ImN_sym.subs({x_: 0, y_: y}), 'sympy')
ImN00 = sp.simplify(ImN_sym[0, 0].subs({x_: 0, y_: y}))
ImN11 = sp.simplify(ImN_sym[1, 1].subs({x_: 0, y_: y}))
print("axion-free slice: Im N_00 =", ImN00, "  Im N_11 =", ImN11)
e0sq = sp.simplify(-1 / ImN00)
e1sq = sp.simplify(-1 / ImN11)
print("e_0^2(y) := 1/(-Im N_00) =", e0sq, "   e_1^2(y) := 1/(-Im N_11) =", e1sq)
mono0 = sp.simplify(sp.diff(e0sq, y))
lim0 = (sp.limit(e0sq, y, 0, '+'), sp.limit(e0sq, y, sp.oo))
lim1 = (sp.limit(e1sq, y, 0, '+'), sp.limit(e1sq, y, sp.oo))
print("limits of e_0^2 (y->0+, y->inf):", lim0, "   of e_1^2:", lim1, "   d e_0^2/dy =", mono0)
check("Q2-H3 e_0^2(Im t) is strictly monotone and onto (0,inf) (power law): a modulus-dependent coupling with the BPS relation holding identically",
      bool(mono0.is_negative) and lim0[0] == sp.oo and lim0[1] == 0)
# x-dependence (axion) as a second free direction
print("full (x,y) dependence of -Im N_00:", sp.simplify(-ImN_sym[0, 0]))

# ------------------------------------------------------------------ Q2-H4 pure N=2 supergravity + arithmetic of the BPS tower
Y0 = sp.symbols('Y0'); q0s = sp.symbols('q0', real=True)
Fp = -sp.I / 4 * Y0**2
F0p = sp.diff(Fp, Y0); F00p = sp.diff(Fp, Y0, 2)
eKp_inv = sp.simplify(sp.I * (1 * F0p.subs(Y0, 1) - 1 * sp.conjugate(F0p.subs(Y0, 1))))
Np = sp.simplify(sp.conjugate(F00p) + 2 * sp.I * (sp.im(F00p) ** 2) / sp.im(F00p))
Vp = sp.simplify(-sp.Rational(1, 2) * q0s * (1 / sp.im(Np)) * q0s)
Zp2 = sp.simplify(q0s**2 / eKp_inv)
print("pure sugra: e^{-K} =", eKp_inv, " N_00 =", Np, " V_BH =", Vp, " |Z|^2 =", Zp2)
check("Q2-H4a pure N=2 supergravity: V_BH = |Z|^2 identically (no scalar charge): the BPS mass IS the RN extremal mass; charge unit not fixed by the theory",
      sp.simplify(Vp - Zp2) == 0 and sp.im(Np) < 0)

alpha = 1 / 137.035999177
mP = 1.220890e19        # GeV
me = 0.51099895e-3
Mpl_red = mP / np.sqrt(8 * np.pi)
e_HL = np.sqrt(4 * np.pi * alpha)
M_el = np.sqrt(2) * e_HL * Mpl_red
print(f"\nBPS tower arithmetic (lane A normalisation, Thomson alpha; identity M = sqrt2 q M_Pl(red) = sqrt(alpha) m_P):")
print(f"  minimal electric BPS quantum : M = {M_el:.4e} GeV = {M_el/mP:.5f} m_P  (sqrt(alpha) = {np.sqrt(alpha):.5f})")
print(f"  minimal magnetic BPS quantum : M = {1/(2*np.sqrt(alpha)):.4f} m_P")
print(f"  (m_e/m_P)^2 = {(me/mP)**2:.4e}  vs alpha = {alpha:.4e}  ->  electron is {np.sqrt(alpha)/(me/mP):.3e} times lighter than the BPS quantum; not BPS")
check("Q2-H4b M_BPS(electric unit) = sqrt(alpha) m_P (an identity restating alpha as (M/m_P)^2, needs M independently)", abs(M_el / mP - np.sqrt(alpha)) < 1e-12)
check("Q2-H4c the electron does not saturate: (m_e/m_P)^2 / alpha < 1e-40", (me / mP)**2 / alpha < 1e-40)

print("\nQ2-H5 (RECALLED, NOT VERIFIED): minimal gauged N=2 supergravity ties the gravitino charge to Lambda < 0 (alpha ~ G|Lambda|); no unitary dS version. Not scored, no computation.")
print("\nSUMMARY: %d/%d checks pass (MUTATE=%s)" % (sum(res), len(res), MUTATE))
sys.exit(0 if all(res) else 1)
