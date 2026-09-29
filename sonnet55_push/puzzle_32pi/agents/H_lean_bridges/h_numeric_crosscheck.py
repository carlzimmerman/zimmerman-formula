"""Independent numerical cross-check (mpmath/numpy/sympy) of the NUMBERS that the Lean bridge certificates prove exactly.
Purpose: guard against a mis-stated Lean statement (Lean checks the proof, not that the statement is the physical one).
Each check has a control (a wrong constant) that must FAIL.  Exit 0 iff every check passes and every control fails."""
import mpmath as mp, numpy as np, sympy as sp, sys
mp.mp.dps = 30
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)
def ctrl(name, cond_that_must_be_false):
    good = not bool(cond_that_must_be_false); ok.append(good); print(("PASS " if good else "FAIL ") + "control: " + name)
pi = mp.pi

# 1. BPST: int_0^inf 192 rho^4 r^3/(r^2+rho^2)^4 dr = 16 for several rho; 2 pi^2 * 16 = 32 pi^2
for rho in [mp.mpf('0.3'), mp.mpf(1), mp.mpf(7)]:
    val = mp.quad(lambda r: 192*rho**4*r**3/(r**2+rho**2)**4, [0, rho, 10*rho, mp.inf])
    chk("1 BPST radial integral = 16 at rho=%s (%.3e)" % (rho, abs(val-16)), abs(val-16) < 1e-20)
ctrl("BPST integral is not 8", abs(mp.quad(lambda r: 192*r**3/(r**2+1)**4, [0, 1, mp.inf]) - 8) < 1e-6)
chk("1 2 pi^2 * 16 = 32 pi^2", abs(2*pi**2*16 - 32*pi**2) < 1e-25)
# Vol(S^3) = 2 pi^2 from sine powers
v3 = mp.quad(lambda t: mp.sin(t)**2, [0, pi]) * mp.quad(lambda t: mp.sin(t), [0, pi]) * 2*pi
chk("1 Vol(S^3) = 2 pi^2 from sin^2, sin integrals", abs(v3 - 2*pi**2) < 1e-25)

# 2. Vol(S^4_L), Euler density of constant curvature (sympy, symbolic Riemann of the round S^4 metric), integral = 64 pi^2
v4 = mp.quad(lambda t: mp.sin(t)**3, [0, pi]) * mp.quad(lambda t: mp.sin(t)**2, [0, pi]) * mp.quad(lambda t: mp.sin(t), [0, pi]) * 2*pi
chk("2 Vol(S^4_1) = 8 pi^2/3", abs(v4 - 8*pi**2/3) < 1e-25)
ctrl("Vol(S^4_1) is not 4 pi^2/3", abs(v4 - 4*pi**2/3) < 1e-6)
th1, th2, th3, ph, L = sp.symbols('th1 th2 th3 ph L', positive=True)
X = [th1, th2, th3, ph]
g = sp.diag(L**2, L**2*sp.sin(th1)**2, L**2*sp.sin(th1)**2*sp.sin(th2)**2, L**2*sp.sin(th1)**2*sp.sin(th2)**2*sp.sin(th3)**2)
gi = g.inv()
n = 4
Gam = [[[sum(gi[a, d]*(sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d])) for d in range(n))/2 for c in range(n)] for b in range(n)] for a in range(n)]
def Riem(a, b, c, d):   # R^a_{bcd}
    r = sp.diff(Gam[a][b][d], X[c]) - sp.diff(Gam[a][b][c], X[d])
    r += sum(Gam[a][c][e]*Gam[e][b][d] - Gam[a][d][e]*Gam[e][b][c] for e in range(n))
    return sp.simplify(r)
R4 = [[[[Riem(a, b, c, d) for d in range(n)] for c in range(n)] for b in range(n)] for a in range(n)]
Ric = sp.Matrix(n, n, lambda b, d: sp.simplify(sum(R4[a][b][a][d] for a in range(n))))
Rs = sp.simplify(sum(gi[b, d]*Ric[b, d] for b in range(n) for d in range(n)))
# lower first index
Rl = [[[[sp.simplify(sum(g[a, e]*R4[e][b][c][d] for e in range(n))) for d in range(n)] for c in range(n)] for b in range(n)] for a in range(n)]
Ric2 = sp.simplify(sum(gi[a, c]*gi[b, d]*Ric[a, b]*Ric[c, d] for a in range(n) for b in range(n) for c in range(n) for d in range(n) if gi[a, c] != 0 and gi[b, d] != 0))
Riem2 = sp.simplify(sum(gi[a, e]*gi[b, f]*gi[c, h]*gi[d, k]*Rl[a][b][c][d]*Rl[e][f][h][k]
                        for a in range(n) for b in range(n) for c in range(n) for d in range(n)
                        for e in [a] for f in [b] for h in [c] for k in [d]))
E4 = sp.simplify(Rs**2 - 4*Ric2 + Riem2)
chk("2 symbolic Riemann of the round S^4_L: R = 12/L^2, Ric^2 = 36/L^4, Riem^2 = 24/L^4, E4 = 24/L^4 (the constants Lean uses)",
    sp.simplify(Rs - 12/L**2) == 0 and sp.simplify(Ric2 - 36/L**4) == 0 and sp.simplify(Riem2 - 24/L**4) == 0 and sp.simplify(E4 - 24/L**4) == 0)
chk("2 int E4 dV = 24/L^4 * 8 pi^2 L^4/3 = 64 pi^2 = 32 pi^2 * chi (chi = 2)", abs(24*8*pi**2/3 - 64*pi**2) < 1e-25)

# 3. area/Lambda chain numerically: pick a0 = 1, Z^2 = 32 pi/3, L = 1/(a0 Z)
a0 = mp.mpf(1); Z = mp.sqrt(32*pi/3); Lv = 1/(a0*Z); Lam = 3/Lv**2
Aa0 = pi/a0**2
chk("3 A_a0 Lambda = 32 pi^2", abs(Aa0*Lam - 32*pi**2) < 1e-25)
chk("3 Lambda = 32 pi a0^2", abs(Lam - 32*pi*a0**2) < 1e-25)
chk("3 G rho = 4 a0^2 (rho = Lambda/8 pi)", abs(Lam/(8*pi) - 4*a0**2) < 1e-25)
V4 = 8*pi**2*Lv**4/3
chk("3 A_a0 = 4 Vol(S^4_L)/L^2 = (4/3) Lambda Vol", abs(Aa0 - 4*V4/Lv**2) < 1e-25 and abs(Aa0 - mp.mpf(4)/3*Lam*V4) < 1e-25)
ctrl("A_a0 = 8 Vol/L^2 is false", abs(Aa0 - 8*V4/Lv**2) < 1e-6)
ctrl("with kappa^2 = rho_Lambda (a0^2 = Lambda/8pi) Z^2 = 32 pi/3 is false (it is 8 pi/3)", abs((1/(mp.sqrt(Lam/(8*pi))*Lv))**2 - 32*pi/3) < 1e-6)

# 4. graviton: h_ij h_ij = 2 h_+^2; canonical normalisation; Isaacson average
ePlus = np.diag([1., -1., 0.]); eCross = np.array([[0, 1., 0], [1., 0, 0], [0, 0, 0]])
chk("4 e+ : sum e_ij^2 = 2, traceless, transverse; e+.ex = 0", abs((ePlus**2).sum()-2) < 1e-15 and abs(np.trace(ePlus)) < 1e-15 and abs((ePlus*eCross).sum()) < 1e-15)
G = mp.mpf('0.7'); h0 = mp.mpf('1.3'); w = mp.mpf('2.1'); T = 2*pi/w
avg = mp.quad(lambda t: 2*(h0*w*mp.sin(w*t))**2, [0, T]) / T
chk("4 <hdot_ij hdot_ij> = w^2 h0^2", abs(avg - w**2*h0**2) < 1e-20)
rho_gw = avg/(32*pi*G)
A_c = h0/mp.sqrt(16*pi*G)
e_can = mp.quad(lambda t: (A_c*w*mp.sin(w*t))**2, [0, T]) / T         # (1/2)(phidot^2+phi'^2) = (A w)^2 sin^2
chk("4 canonical phi = h_+/sqrt(16 pi G): energy density average = Isaacson w^2 h0^2/(32 pi G)", abs(e_can - rho_gw) < 1e-20)
ctrl("Isaacson with 1/(16 pi G) is not the canonical value", abs(avg/(16*pi*G) - e_can) < 1e-6)
ctrl("kappa_g^2 = 16 pi G does not make (1/64 pi G) kappa^2 = 1/2", abs((16*pi*G)/(64*pi*G) - mp.mpf(1)/2) < 1e-6)
chk("4 kappa_g^2 = 32 pi G makes kappa^2/(64 pi G) = 1/2", abs((32*pi*G)/(64*pi*G) - mp.mpf(1)/2) < 1e-25)

# 5. free fall: int dr / sqrt(2GM(1/r - 1/r0)) = sqrt(3 pi/(32 G rho)); ODE integration cross-check
G = mp.mpf('0.9'); rho = mp.mpf('1.7'); r0 = mp.mpf('2.3'); M = 4*pi/3*rho*r0**3
tff = mp.quad(lambda r: 1/mp.sqrt(2*G*M*(1/r - 1/r0)), [0, r0/2, r0])
chk("5 t_ff quadrature = sqrt(3 pi/(32 G rho))  (%.3e)" % abs(tff - mp.sqrt(3*pi/(32*G*rho))), abs(tff - mp.sqrt(3*pi/(32*G*rho))) < 1e-12)
ctrl("t_ff is not sqrt(3 pi/(16 G rho))", abs(tff - mp.sqrt(3*pi/(16*G*rho))) < 1e-3)
chk("5 int_0^1 sqrt(x/(1-x)) dx = pi/2", abs(mp.quad(lambda x: mp.sqrt(x/(1-x)), [0, 1]) - pi/2) < 1e-12)
from scipy.integrate import solve_ivp
Gf, Mf, r0f = float(G), float(M), float(r0)
def rhs(t, y): return [y[1], -Gf*Mf/y[0]**2]
ev = lambda t, y: y[0] - 1e-4*r0f
ev.terminal = True
sol = solve_ivp(rhs, [0, 50], [r0f, 0.0], events=ev, rtol=1e-11, atol=1e-13)
chk("5 direct r'' = -GM/r^2 integration reaches r ~ 0 at t_ff (within the 1e-4 cutoff)", abs(sol.t_events[0][0] - float(tff)) < 2e-3)
# cycloid
eta = np.linspace(0.1, 3.0, 40)
Aq = float(mp.sqrt(r0**3/(8*G*M)))
r = r0f/2*(1+np.cos(eta)); dr = -(r0f/2)*np.sin(eta); dt = Aq*(1+np.cos(eta))
chk("5 cycloid: (dr/dt)^2 = 2GM(1/r - 1/r0) at 40 points", np.allclose((dr/dt)**2, 2*Gf*Mf*(1/r - 1/r0f), rtol=1e-12))
ctrl("cycloid with 4GM fails", np.allclose((dr/dt)**2, 4*Gf*Mf*(1/r - 1/r0f), rtol=1e-6))

# 6. non-embedding: Z, r_s, Nariai, Israel
Zp = mp.sqrt(32*pi/3)
chk("6 Z = 5.7888 > 2; r_s = Z L/2 > L", abs(Zp-mp.mpf('5.7888')) < 1e-3 and Zp > 2)
chk("6 M_s/M_N = 3 sqrt3 Z/4 = 3 sqrt(32 pi)/4 = 7.52", abs(3*mp.sqrt(3)*Zp/4 - 3*mp.sqrt(32*pi)/4) < 1e-25 and abs(3*mp.sqrt(3)*Zp/4 - mp.mpf('7.52')) < 0.01)
Lm = 1.0; Ms = float(Zp)*Lm/4
rr = np.linspace(1e-3, 50, 200001)
chk("6 SdS with M_s: r - 2M - r^3/L^2 < 0 for all sampled r>0 (max %.4f)" % (rr - 2*Ms - rr**3/Lm**2).max(), ((rr - 2*Ms - rr**3/Lm**2) < 0).all())
MN = Lm/(3*np.sqrt(3))
ctrl("SdS with 0.9 M_N has no horizon (it has)", ((rr - 2*0.9*MN - rr**3/Lm**2) < 0).all())
rng = np.random.default_rng(7); bad = 0
for _ in range(20000):
    hi, ho, s = rng.uniform(0, 3), rng.uniform(0, 3), rng.uniform(1e-3, 3)
    x = 4*np.pi*s; A = 0.5*((ho**2 - hi**2)/x + x); B = A - x
    u = hi**2 + A**2
    if abs(u - (ho**2 + B**2)) > 1e-9*max(1, u) or u < max(hi, ho)**2 - 1e-9: bad += 1
chk("6 Israel: 1/R^2 = Hi^2 + A^2 = Ho^2 + B^2 >= max(Hi^2, Ho^2) on 20000 random (Hi, Ho, sigma)", bad == 0)
kap = float(mp.sqrt(2*pi/3))
chk("6 embeddable iff kappa >= sqrt(2 pi/3) = %.4f (kappa=1 gives Z = %.4f > 2)" % (kap, float(mp.sqrt(8*pi/3))),
    abs(float(mp.sqrt(8*pi/3))/kap - 2) < 1e-12 and float(mp.sqrt(8*pi/3)) > 2)
ctrl("kappa >= 1 is not the embeddability threshold (kappa = 1 is NOT embeddable)", float(mp.sqrt(8*pi/3))/1.0 <= 2)

# 7. p09: G rho = a0^2 U_v/(8 pi) = 4 a0^2 iff U_v = 32 pi
Uv = sp.symbols('U_v', positive=True); a = sp.symbols('a0', positive=True)
chk("7 solve a0^2 U_v/(8 pi) = 4 a0^2 -> U_v = 32 pi", sp.solve(sp.Eq(a**2*Uv/(8*sp.pi), 4*a**2), Uv) == [32*sp.pi])
ctrl("U_v = 8 pi is not the solution", sp.solve(sp.Eq(a**2*Uv/(8*sp.pi), 4*a**2), Uv) == [8*sp.pi])

print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
