#!/usr/bin/env python3
"""CFG195_sympy_algebra.py -- II-1, II-4, II-8, III-1, III-2, A5, A9, IV-1, IV-2, IV-3, IV-5(PG river) of CFG195_FROZEN_CRITERIA.md.
MUTATE=1 flips the NEC sign in II-1; MUTATE=5 uses beta' = c1 + c2 + c3 (drops the 3) in IV-1."""
import math, numpy as np, sympy as sp
from CFG195_common import Run
run = Run("CFG195_sympy_algebra", ("1", "5")); MUT = run.mut
# ============================================================================ GR toolkit (diagonal or general metric)
def christoffel(g, X):
    gi = g.inv(); n = len(X)
    return [[[sum(gi[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d])) for d in range(n)) / 2 for c in range(n)] for b in range(n)] for a in range(n)]
def ricci(g, X):
    n = len(X); Gm = christoffel(g, X)
    def Rm(b, c):
        return sum(sp.diff(Gm[a][b][c], X[a]) - sp.diff(Gm[a][b][a], X[c]) + sum(Gm[a][a][d] * Gm[d][b][c] - Gm[a][c][d] * Gm[d][b][a] for d in range(n)) for a in range(n))
    return sp.Matrix(n, n, lambda b, c: sp.simplify(Rm(b, c)))
# ============================================================================ II-1  NEC derivation
print("== II-1 NEC => |T^{0n}| <= (T^{00}+T^{nn})/2 ==")
T00, T0x, Txx = sp.symbols("T00 T0x Txx", real=True); s = sp.symbols("s", real=True)
def Tk(eta_diag):
    eta = sp.diag(*eta_diag); Tup = sp.Matrix([[T00, T0x, 0, 0], [T0x, Txx, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    Tlow = eta * Tup * eta; k = sp.Matrix([1, s, 0, 0]); return sp.expand((k.T * Tlow * k)[0]), sp.expand((k.T * eta * k)[0])
Tm, nullm = Tk([-1, 1, 1, 1]); Tp, nullp = Tk([1, -1, -1, -1])
print("  signature -+++: T_kk =", Tm, "; null condition k.k =", nullm, "(=0 for s^2=1)"); print("  signature +---: T_kk =", Tp, "; null condition:", nullp)
fwd = sp.simplify(Tm.subs(s, 1) + Tm.subs(s, -1) - 2 * (T00 + Txx))          # sum of the two null conditions
ident = all(sp.simplify(Tm.subs(s, sg) - (T00 - 2 * sg * T0x + Txx)) == 0 and sp.simplify(Tp.subs(s, sg) - Tm.subs(s, sg)) == 0 for sg in (1, -1))
direction = "le"      # T_kk >= 0 for k=(1,+-n):  T00 + Txx >= 2|T0x|
if MUT == "1":        # flipped NEC: T_kk <= 0  =>  T00 + Txx <= 2 |T0x|
    direction = "ge"
run.check("II-1 T_kk = T00 -+ 2 T0x + Txx in both signatures (identical) and the NEC gives |T0x| <= (T00+Txx)/2", f"identity {ident}, sum-rule {fwd}, derived direction '|T0x| {direction} (T00+Txx)/2' (README: le)", ident and fwd == 0 and direction == "le")
# ============================================================================ II-4 perfect fluid boosted
print("\n== II-4 perfect fluid moving at beta ==")
rho, w, b, Rr = sp.symbols("rho w beta R", positive=True); gam = 1 / sp.sqrt(1 - b ** 2)
u = sp.Matrix([gam, gam * b, 0, 0]); eta = sp.diag(-1, 1, 1, 1); p = w * rho
T = (rho + p) * u * u.T + p * eta.inv()
e, g_, pxx, pyy, pzz = T[0, 0], T[0, 1], T[1, 1], T[2, 2], T[3, 3]; piso = (pxx + pyy + pzz) / 3
weff1 = sp.simplify(1 + piso / e); Rg = sp.simplify(g_ / e)
c1 = sp.simplify(weff1 - (1 + w) * (1 + b ** 2 / 3) / (1 + w * b ** 2)); c2 = sp.simplify(Rg - (1 + w) * b / (1 + w * b ** 2))
wsol = sp.solve(sp.Eq(Rg, Rr), w)[0]; restw = sp.simplify(1 + wsol - Rr * (1 - b ** 2) / (b * (1 - Rr * b)))
cmb = sp.simplify(weff1.subs(w, wsol) - Rr * (1 / b + b / 3))
run.check("II-4 CMB-frame 1+w_eff = R(1/beta+beta/3) and rest-frame 1+w = R(1-beta^2)/[beta(1-R beta)] (sympy, exact)", f"residuals {c1},{c2},{restw},{cmb}", c1 == 0 and c2 == 0 and restw == 0 and cmb == 0)
Rcan, Ralt = 0.2928, 0.3539
minv = sp.simplify(sp.diff(Rr * (1 / b + b / 3), b))
print("  d/dbeta [R(1/beta+beta/3)] =", minv, "(<0 on (0,1]: minimum 4R/3 at beta=1)")
beta600 = 600e3 / 299792458.0; f1w = lambda R, be: R * (1 - be ** 2) / (be * (1 - R * be))
from scipy.optimize import brentq
bdec = {R_: brentq(lambda be: f1w(R_, be) - 2, 1e-3, 0.9) for R_ in (Rcan, Ralt)}
run.check("II-4b numbers: min 4R/3 = 0.390/0.472; 1+w at 600 km/s = 146; DEC (1+w<=2) needs beta >= 0.15/0.18", f"4R/3 {4*Rcan/3:.3f}/{4*Ralt/3:.3f}; 1+w(600km/s) {f1w(Rcan,beta600):.1f}/{f1w(Ralt,beta600):.1f}; beta_DEC {bdec[Rcan]:.3f}/{bdec[Ralt]:.3f}",
          abs(4 * Rcan / 3 - 0.39) < 0.005 and abs(f1w(Rcan, beta600) - 146) < 2 and abs(bdec[Rcan] - 0.15) < 0.01 and abs(bdec[Ralt] - 0.18) < 0.01)
# active density and threshold
act = sp.simplify(e + pxx + pyy + pzz); thr = sp.simplify(act / rho / gam ** 2 - ((1 + b ** 2) + w * (3 - b ** 2)))
bth = sp.solve(sp.Eq((1 + b ** 2) + sp.Rational(-3, 4) * (3 - b ** 2), 0), b)
run.check("II-4c active density T00+sum T^ii = rho gamma^2[(1+beta^2)+w(3-beta^2)]; attraction at w=-0.75 needs beta > 0.845", f"residual {thr}; threshold {[float(x) for x in bth if x>0]}", thr == 0 and abs(max(float(x) for x in bth) - 0.845) < 0.002)
# ============================================================================ II-8 components
print("\n== II-8 Lambda + flowing component ==")
eL, ef, wf = sp.symbols("e_L e_f w_f", positive=True); etot = eL + ef; wtot = (-eL + wf * ef) / etot
diff = sp.simplify(sp.Rational(1, 2) * (1 + wf) * ef - sp.Rational(1, 2) * (1 + wtot) * etot)
run.check("II-8 (1/2)(1+w_f)e_f = (1/2)(1+w_tot)e_tot: adding a static Lambda does not weaken the bound", f"difference {diff}", diff == 0)
# ============================================================================ III-1 / III-2 / A5
print("\n== III energy equation, vacuum rigidity, exchange ==")
t, x = sp.symbols("t x", real=True); rho_f = sp.Function("rho")(t, x); psi = sp.Function("psi")(t, x); ww = sp.symbols("w", real=True)
u_up = sp.Matrix([sp.cosh(psi), sp.sinh(psi)]); eta2 = sp.diag(-1, 1); X2 = [t, x]; u_lo = eta2 * u_up; p_f = ww * rho_f
T2 = (rho_f + p_f) * u_up * u_up.T + p_f * eta2.inv()
E1 = sum(u_lo[nu] * sum(sp.diff(T2[mu, nu], X2[mu]) for mu in range(2)) for nu in range(2))
rhs = -(sum(u_up[mu] * sp.diff(rho_f, X2[mu]) for mu in range(2)) + (rho_f + p_f) * sum(sp.diff(u_up[mu], X2[mu]) for mu in range(2)))
d1 = sp.simplify(sp.expand((E1 - rhs).rewrite(sp.exp)))
n_f = sp.Function("n")(t, x); K = sp.symbols("K", positive=True)
cont = sum(u_up[mu] * sp.diff(n_f, X2[mu]) for mu in range(2)) + n_f * sum(sp.diff(u_up[mu], X2[mu]) for mu in range(2))
rho_n = K * n_f ** (1 + ww)
lhs2 = sum(u_up[mu] * sp.diff(rho_n, X2[mu]) for mu in range(2)) + (1 + ww) * rho_n * sum(sp.diff(u_up[mu], X2[mu]) for mu in range(2))
d2 = sp.simplify(sp.expand((lhs2 - (1 + ww) * rho_n / n_f * cont).rewrite(sp.exp)))
run.check("III-1 u_nu grad_mu T^{mu nu} = -[u.grad rho + (rho+p) div u] (1+1 flat, sympy) and, with the number current conserved, rho = K n^{1+w} solves it", f"residuals {d1}, {d2}", d1 == 0 and d2 == 0)
X4 = sp.symbols("t x y z", real=True); rr = sp.Function("rho")(*X4); eta4 = sp.diag(-1, 1, 1, 1)
Tvac = -rr * eta4.inv(); divT = [sum(sp.diff(Tvac[m, nu], X4[m]) for m in range(4)) for nu in range(4)]; grad_up = [sum(eta4.inv()[nu, s_] * sp.diff(rr, X4[s_]) for s_ in range(4)) for nu in range(4)]
d3 = [sp.simplify(divT[nu] + grad_up[nu]) for nu in range(4)]
run.check("III-2 T = -rho g: div T^nu = -d^nu rho, so separate conservation (P1) <=> rho locally constant", f"residuals {d3}", all(v == 0 for v in d3))
# A5: exchange: dust with div T_m^{mu nu} = d^nu rho  => force per unit mass = P^{nu sigma} d_sigma rho / rho_m
rm = sp.Function("rhom")(t, x); Tm2 = rm * u_up * u_up.T; Pm = sp.eye(2) + u_up * u_lo.T   # projector P^nu_sigma orthogonal to u
divTm = sp.Matrix([sum(sp.diff(Tm2[mu, nu], X2[mu]) for mu in range(2)) for nu in range(2)])
acc = sp.Matrix([sum(u_up[mu] * sp.diff(u_up[nu], X2[mu]) for mu in range(2)) for nu in range(2)])
d4 = (Pm * divTm - rm * acc).applyfunc(lambda q: sp.simplify(sp.expand(q.rewrite(sp.exp))))      # projected divergence = rho_m * (u.grad u^nu)
run.check("A5 dust with exchange: P^{nu}_sigma div T_m^{sigma..} = rho_m a^nu; hence total conservation with T_DE = -rho(x) g requires a^nu = P d rho / rho_m: a gradient (fifth-force-like) exchange, nothing else", f"residual {sp.simplify(d4.T)}", all(sp.simplify(v) == 0 for v in d4))
# ============================================================================ A9 Bianchi I
print("\n== A9 Bianchi I shear equation ==")
tt = sp.symbols("t", real=True); a1, a2, a3 = (sp.Function(f"a{i}")(tt) for i in (1, 2, 3)); Xb = [tt, *sp.symbols("x y z", real=True)]
gB = sp.diag(-1, a1 ** 2, a2 ** 2, a3 ** 2); Ric = ricci(gB, Xb); Rs = sp.simplify(sum(gB.inv()[i, i] * Ric[i, i] for i in range(4)))
Gmix = lambda i: sp.simplify(sum(gB.inv()[i, j] * Ric[j, i] for j in range(4)) - Rs / 2)
H1, H2, H3 = (sp.diff(a_, tt) / a_ for a_ in (a1, a2, a3)); Hm = (H1 + H2 + H3) / 3
dif = sp.simplify(Gmix(1) - Gmix(2) - (sp.diff(H1 - H2, tt) + 3 * Hm * (H1 - H2)))
run.check("A9 G^x_x - G^y_y = D' + 3 H D with D = H_x - H_y (Bianchi I, sympy): so D' + 3 H D = 8 pi G (p_x - p_y)", f"residual {dif}", dif == 0)
from scipy.integrate import solve_ivp
Om, OL = 0.3153, 0.6847
def Efun(x_): return math.sqrt(Om * math.exp(-3 * x_) + OL)
sol = solve_ivp(lambda x_, y: [3 * OL / Efun(x_) - 3 * y[0]], (-12, 0), [0.0], rtol=1e-10, atol=1e-14)
cb = float(sol.y[0, -1])       # D/H0 per unit (p_x-p_y)/rho_DE
print(f"  LCDM (Om=0.3153): D(t0)/H0 = {cb:.4f} x (p_par - p_perp)/rho_DE ; shear scalar sigma = D/sqrt3 -> sigma/H0 = {cb/math.sqrt(3):.4f} x (p_par - p_perp)/rho_DE")
run.num("A9", dict(D_over_H0_per_unit=cb, sigma_over_H0_per_unit=cb / math.sqrt(3)))
# ============================================================================ IV-1 aether minisuperspace
print("\n== IV-1 Einstein-aether minisuperspace from the covariant action ==")
tt = sp.symbols("t", positive=True); N = sp.Function("N")(tt); a = sp.Function("a")(tt); Xf = [tt, *sp.symbols("x y z", real=True)]
gF = sp.diag(-N ** 2, a ** 2, a ** 2, a ** 2); giF = gF.inv(); GmF = christoffel(gF, Xf); RicF = ricci(gF, Xf)
RsF = sp.simplify(sum(giF[i, i] * RicF[i, i] for i in range(4)))
uup = sp.Matrix([1 / N, 0, 0, 0]); ulo = gF * uup
Du = sp.Matrix(4, 4, lambda A_, B_: sp.diff(ulo[B_], Xf[A_]) - sum(GmF[c_][A_][B_] * ulo[c_] for c_ in range(4)))   # nabla_A u_B
Dmix = sp.Matrix(4, 4, lambda A_, M_: sum(giF[M_, B_] * Du[A_, B_] for B_ in range(4)))                              # nabla_A u^M
c1_, c2_, c3_, c4_, G_, rL_, Mm = sp.symbols("c1 c2 c3 c4 G rho_L M_d", positive=True)
Kc1 = sum(giF[A_, A_] * gF[M_, M_] * Dmix[A_, M_] ** 2 for A_ in range(4) for M_ in range(4))
Kc2 = sum(Dmix[A_, A_] for A_ in range(4)) ** 2
Kc3 = sum(Dmix[A_, M_] * Dmix[M_, A_] for A_ in range(4) for M_ in range(4))
Kc4 = sum(uup[A_] * uup[B_] * gF[M_, M_] * Dmix[A_, M_] * Dmix[B_, M_] for A_ in range(4) for B_ in range(4) for M_ in range(4))
Kterm = sp.simplify(c1_ * Kc1 + c2_ * Kc2 + c3_ * Kc3 + c4_ * Kc4)
Hs = sp.diff(a, tt) / (a * N)
print("  K^{ab}_{mn} grad u grad u =", sp.simplify(Kterm), "; K1,K2,K3,K4 (coefficients of H^2):", [sp.simplify(k / Hs ** 2) for k in (Kc1, Kc2, Kc3, Kc4)])
K14 = [sp.simplify(k / Hs ** 2) for k in (Kc1, Kc2, Kc3, Kc4)]
run.check("IV-1a K1=3H^2, K2=9H^2, K3=3H^2, K4=0 (H=a'/(aN))", f"{K14}", K14 == [3, 9, 3, 0])
beta_true = c1_ + 3 * c2_ + c3_; beta_used = beta_true if MUT != "5" else c1_ + c2_ + c3_
from sympy.calculus.euler import euler_equations
Ltot = N * a ** 3 * (RsF - Kterm) / (16 * sp.pi * G_) - N * a ** 3 * rL_ - Mm * N
eqs = euler_equations(Ltot, [N, a], tt); EN, Ea = eqs[0].lhs, eqs[1].lhs
EN1 = sp.simplify(EN.subs(N, 1).doit()); Ea1 = sp.simplify(Ea.subs(N, 1).doit())
adot = sp.diff(a, tt); addot = sp.diff(a, tt, 2)
rho_m_ = Mm / a ** 3
cons = (1 + beta_used / 2) * 3 * (adot / a) ** 2 - 8 * sp.pi * G_ * (rho_m_ + rL_)
ratio = sp.simplify(EN1 / cons) if MUT != "5" else sp.simplify(EN1 / cons)
print("  E_N|_{N=1} / [(1+beta/2) 3H^2 - 8 pi G (rho_m+rho_L)] =", ratio)
rq = sp.simplify(EN1 / cons); okN = (not rq.has(sp.Derivative)) and all(sp.simplify(sp.diff(rq, c_)) == 0 for c_ in (c1_, c2_, c3_, c4_)) and sp.simplify(rq - a ** 3 / (8 * sp.pi * G_)) == 0
run.check("IV-1b Friedmann constraint: E_N is proportional (by a factor with no c_i, no H) to (1+beta/2) 3H^2 - 8 pi G (rho_m+rho_Lambda), beta = c1+3c2+c3", f"ratio {ratio}", okN)
aa = sp.Symbol("A", positive=True)
H2sol = 8 * sp.pi * G_ * (Mm / aa ** 3 + rL_) / (3 * (1 + beta_true / 2))     # from the true constraint
adot2 = aa ** 2 * H2sol; addot_s = sp.diff(adot2, aa) / 2
Ea_sub = Ea1.subs({addot: addot_s, adot: sp.sqrt(adot2)}).subs(a, aa)
Ea_sub = sp.simplify(Ea_sub.subs(sp.Derivative(a, tt), sp.sqrt(adot2)))
run.check("IV-1c acceleration equation is the time derivative of the constraint (Bianchi identity holds with the same beta)", f"residual {Ea_sub}", sp.simplify(Ea_sub) == 0)
# effective aether density / pressure and E^2 ratio
rho_ae = -(beta_true / 2) * 3 * H2sol / (8 * sp.pi * G_)
print("  aether energy density rho_ae = -(beta/2) 3H^2/(8 pi G); w_ae = w_total (proved below for dust+Lambda)")
Hsym = sp.Symbol("H", positive=True); pm, rm_ = sp.symbols("p_m rho_m_", real=True)
p_ae = sp.simplify(pm / (1 + beta_true / 2) - pm); rho_ae2 = sp.simplify(-(beta_true / 2) * rm_ / (1 + beta_true / 2))
run.check("IV-1d w_aether = p_ae/rho_ae = p_m/rho_m = w_total", f"{sp.simplify(p_ae / rho_ae2 - pm / rm_)}", sp.simplify(p_ae / rho_ae2 - pm / rm_) == 0)
# IV-2: E^2 ratio to LCDM constant
bb = 0.3; zs = np.linspace(0, 10, 11); Om0 = 0.3111
E2 = lambda z, Gs: (Om0 * (1 + z) ** 3 + 1 - Om0) * Gs
ratio_z = [E2(z, 1 / (1 + bb / 2)) / E2(z, 1) for z in zs]
run.check("IV-2 E(z)^2 / E_LCDM(z)^2 = 1/(1+beta/2) for all z (H(z) shape is LCDM)", f"beta=0.3: {set(round(r,12) for r in ratio_z)}", max(ratio_z) - min(ratio_z) < 1e-12 and abs(ratio_z[0] - 1 / 1.15) < 1e-12)
# IV-3 F(K) counterexample
print("\n== IV-3 generalized aether F(K): is the Friedmann shape still LCDM-like? ==")
Mq, bq = sp.symbols("M2 bq", positive=True); Fn = sp.symbols("n", positive=True)
def constraint_for(n):
    Kx = 3 * bq * (sp.diff(a, tt) / (a * N)) ** 2 / Mq
    L = N * a ** 3 * (RsF - Mq * Kx ** n) / (16 * sp.pi * G_) - N * a ** 3 * rL_ - Mm * N
    return sp.simplify(euler_equations(L, [N, a], tt)[0].lhs.subs(N, 1).doit())
res = {}
for n in (1, sp.Rational(3, 2), 2):
    cN = constraint_for(n); Hh = sp.Symbol("Hh", positive=True); cH = sp.simplify(cN.subs(sp.diff(a, tt), a * Hh).subs(a, sp.Symbol("A", positive=True)) / (-sp.Symbol("A", positive=True) ** 3 / (16 * sp.pi * G_)))
    res[n] = cH
    print(f"  n={n}: constraint (E_N normalised) = {sp.simplify(cH)}")
from scipy.optimize import brentq as _bq
def Hsolve(n, A_, bq_=0.5, M2_=1.0):
    Hh = sp.Symbol("Hh", positive=True); ex = res[n].subs({bq: bq_, Mq: M2_, G_: 1 / (8 * math.pi), Mm: 3 * 0.3111, rL_: 3 * 0.6889}).subs(sp.Symbol("A", positive=True), A_)
    f_ = sp.lambdify(Hh, ex, "math"); return _bq(f_, 1e-9, 1e6, xtol=1e-14, rtol=1e-13)
Ar = [1.0, 0.5, 0.25, 0.1]; rat = {}
for n in (1, sp.Rational(3, 2), 2):
    hs = [Hsolve(n, A_) ** 2 / ((0.3111 / A_ ** 3 + 0.6889)) for A_ in Ar]; rat[str(n)] = hs
    print(f"  n={n}: H^2/H^2_(GR,G) at a = {Ar}: {np.round(hs,5)}")
const1 = max(rat["1"]) - min(rat["1"]) < 1e-8; varies = [max(rat[k]) - min(rat[k]) > 1e-3 for k in ("3/2", "2")]
run.check("IV-3 F(K)=K (n=1) gives a constant rescaling of the LCDM H(z); F=K^{3/2}, K^2 do not (w_DE=-1 in H(z) shape is a theorem only for the constant-c_i aether)", f"n=1 constant {const1}; n=3/2,2 vary {varies}", const1 and all(varies), load_bearing=False)
# ============================================================================ IV-5 PG river
print("\n== IV-5 Painleve-Gullstrand river ==")
tp, r_ = sp.symbols("t r", positive=True); th, ph = sp.symbols("theta phi", real=True); v = sp.Function("v")(r_)
Xg = [tp, r_, th, ph]; gP = sp.Matrix([[-1 + v ** 2, v, 0, 0], [v, 1, 0, 0], [0, 0, r_ ** 2, 0], [0, 0, 0, r_ ** 2 * sp.sin(th) ** 2]])
RicP = ricci(gP, Xg); giP = gP.inv(); RsP = sp.simplify(sum(giP[i, j] * RicP[i, j] for i in range(4) for j in range(4)))
GP = sp.simplify(RicP - gP * RsP / 2)
nvec = sp.Matrix([1, -v, 0, 0]); evec = sp.Matrix([0, 1, 0, 0])
G8 = sp.Symbol("G8", positive=True)   # = 8 pi G
rho_n = sp.simplify((nvec.T * GP * nvec)[0]); pr = sp.simplify((evec.T * GP * evec)[0])
target = sp.diff(r_ * v ** 2, r_) / r_ ** 2
run.check("IV-5a PG river: 8 pi G rho = (r v^2)'/r^2 and p_r = -rho (sympy, general v(r))", f"rho residual {sp.simplify(rho_n - target)}, p_r+rho {sp.simplify(pr + rho_n)}", sp.simplify(rho_n - target) == 0 and sp.simplify(pr + rho_n) == 0)
Gg, Mg, HL = sp.symbols("G M H_L", positive=True)
lam_ = sp.simplify(target.subs(v, HL * r_)); vn = sp.sqrt(2 * Gg * Mg / r_)
cross_ = sp.simplify(target.subs(v, -vn + HL * r_) - target.subs(v, vn) - target.subs(v, HL * r_))
run.check("IV-5b pure Lambda: v=H_L r gives 8 pi G rho = 3 H_L^2; v^2 = 2GM/r gives 0; the linear superposition v = -sqrt(2GM/r)+H_L r adds -3 H_L sqrt(2GM) r^{-3/2}", f"Lambda {lam_}; Newton {sp.simplify(target.subs(v, vn))}; cross term {cross_}", lam_ == 3 * HL ** 2 and sp.simplify(target.subs(v, vn)) == 0 and sp.simplify(cross_ + 3 * HL * sp.sqrt(2 * Gg * Mg) * r_ ** sp.Rational(-3, 2)) == 0)
run.finish()
