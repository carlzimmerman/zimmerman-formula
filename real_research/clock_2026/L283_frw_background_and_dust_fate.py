"""L283 (CK12) -- the standing candidate's FRW background DERIVED from its action, and the fate of its dark 'dust'.

Part A, FRW minisuperspace (N(t), a(t), clock tau = t, scalar phi(t), generic Q-potential F(Q)):
   A1 on FRW the clock is geodesic (J^mu = 0) and the scalar's leaf gradient vanishes (Y = 0): the coupling and J(Y) drop out exactly.
   A2 Friedmann from the lapse: 3(1 + 3c2/2) H^2 = 8 pi G [rho_m + rho_phi], rho_phi = (Q F_Q - F)/(16 pi G):  G_cosmo = G/(1 + 3c2/2)
      (Carroll-Lim's khronometric value at c13 = 0), so G_cosmo/G_N = (1 - c14/2)/(1 + 3c2/2) and BBN (|dG/G| < 0.1) needs c2 < 0.07.
   A3 the scalar equation is d/dt[a^3 F_Q] = 0 exactly: F_Q propto a^-3 (AeST's conservation law, reproduced for this action).
   A4 quadratic well F = K2 (Q - Q0)^2 (the action as written): rho_phi = K2 (2 Q0 q + q^2)/(16 pi G), q propto a^-3 -- DUST plus a STIFF
      a^-6 term of the OPPOSITE sign (K2 < 0 is the healthy sign, f34/L282, so dust > 0 needs q < 0 and the stiff term is negative);
      BBN (|rho_stiff| < 0.1 rho_rad at T ~ 1 MeV) needs |K2| Q0^2 >= S_min = (15/2) Om_dm^2/(Om_r a_BBN^2) H0^2 ~ 1e23 H0^2.
Part B, the static lapse mass (Minkowski build of L282, omega = 0, matter source): the roll gives the NEWTONIAN potential a mass
      mu_Psi^2 = 2|K2| Q0^2 (1 + ...)/(2 - c14) -- Yukawa or oscillatory decided by the machine -- so 1/mu_Psi <= sqrt((2-c14)/(2 S_min)) c/H0.
   B1 THE PINCER (K2-independent: both bounds depend on the product |K2| Q0^2): the quadratic-well dust forces 1/mu_Psi <= ~0.01 pc,
      against Newtonian gravity verified to >= Mpc.  The K2 (Q-Q0)^2 dust of the action AS WRITTEN is dead in this candidate.
Part C, the constructive replacement: a quartic well F = -(Q-Q0)^4/Lambda^2 (healthy sign): F_Q propto a^-3 gives q propto a^-1,
      rho_phi = [4 Q0 |q|^3 + 3 q^4]/Lambda^2/(16 pi G) = DUST + a RADIATION-like term (dark radiation, bounded by Delta N_eff), and the
      lapse mass today mu_Psi^2 = |F_QQ(q)| Q0^2 (...) shrinks as a^-2: the pincer opens into a WINDOW with a LOCK
      Delta N_eff x (1/mu_Psi)^2 = fixed by Om_dm, Om_r -- a two-sided near-term test (CMB-S4 vs the lensing-RAR turnover scale).
      General n: correction propto a^{-3n/(n-1)}; n = 2 stiff, n = 4 radiation, n -> inf dust.
A FAIL is a finding; thresholds are the derived/measured statements, never tuned."""
import os, sys, json, time, math
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
T0 = time.time(); print("L283 (CK12) -- FRW background and the fate of the dust\n", flush=True)
C, PC, MPC, AU = 2.99792458e8, 3.0856775814913673e16, 3.0856775814913673e22, 1.495978707e11
# ---------------- Part A: minisuperspace
t, x, y, z = sp.symbols('t x y z', real=True); X = [t, x, y, z]
KB, c1, c2, c3, c4, G, pi_ = sp.symbols('K_B c_1 c_2 c_3 c_4 G pi', real=True); c14 = sp.Symbol('c14')
N, a, ph = sp.Function('N')(t), sp.Function('a')(t), sp.Function('phi')(t)
F = sp.Function('F'); Jf = sp.Function('J')
g = sp.diag(-N ** 2, a ** 2, a ** 2, a ** 2); ginv = g.inv(); sqrtg = N * a ** 3
Gam = [[[sp.simplify(sum(ginv[l, s] * (sp.diff(g[s, m], X[n]) + sp.diff(g[s, n], X[m]) - sp.diff(g[m, n], X[s])) for s in range(4)) / 2) for n in range(4)] for m in range(4)] for l in range(4)]
Ric = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        Ric[m, n] = sum(sp.diff(Gam[l][m][n], X[l]) - sp.diff(Gam[l][m][l], X[n]) + sum(Gam[l][l][s] * Gam[s][m][n] - Gam[l][n][s] * Gam[s][m][l] for s in range(4)) for l in range(4))
R = sp.simplify(sum(ginv[m, n] * Ric[m, n] for m in range(4) for n in range(4)))
tau = t; dtau = [sp.diff(tau, v) for v in X]
Xinv = -sum(ginv[m, n] * dtau[m] * dtau[n] for m in range(4) for n in range(4))
n_dn = [-dtau[m] / sp.sqrt(Xinv) for m in range(4)]; n_up = [sum(ginv[m, n] * n_dn[n] for n in range(4)) for m in range(4)]
Dn = [[sp.diff(n_dn[n], X[m]) - sum(Gam[l][m][n] * n_dn[l] for l in range(4)) for n in range(4)] for m in range(4)]
Dn_up = [[sum(ginv[m, a_] * ginv[n, b_] * Dn[a_][b_] for a_ in range(4) for b_ in range(4)) for n in range(4)] for m in range(4)]
T1 = sp.simplify(sum(Dn[m][n] * Dn_up[m][n] for m in range(4) for n in range(4)))
divn = sp.simplify(sum(ginv[m, n] * Dn[m][n] for m in range(4) for n in range(4))); T2 = divn ** 2
T3 = sp.simplify(sum(Dn[m][n] * Dn_up[n][m] for m in range(4) for n in range(4)))
J_dn = [sp.simplify(sum(n_up[nu] * Dn[nu][m] for nu in range(4))) for m in range(4)]
J_up = [sum(ginv[m, n] * J_dn[n] for n in range(4)) for m in range(4)]
T4 = sp.simplify(sum(J_dn[m] * J_up[m] for m in range(4)))
dphi = [sp.diff(ph, v) for v in X]
Jdphi = sp.simplify(sum(J_up[m] * dphi[m] for m in range(4)))
Q = sp.simplify(sum(n_up[m] * dphi[m] for m in range(4)))
Y = sp.simplify(sum((ginv[m, n] + n_up[m] * n_up[n]) * dphi[m] * dphi[n] for m in range(4) for n in range(4)))
check("A1 on FRW the clock is geodesic (J^mu = 0 for every component) and the scalar's leaf gradient vanishes (Y = 0): the coupling 2(2-K_B)J.dphi and J(Y) drop out of the background exactly; Q = phi'/N",
      all(sp.simplify(j) == 0 for j in J_dn) and sp.simplify(Y) == 0 and sp.simplify((Q - sp.diff(ph, t) / N).subs(N, sp.Symbol('N_pos', positive=True))) == 0, f"J = {J_dn}, Y = {Y}, Q = {Q}")
rho_m = sp.Function('rho_m')(a)                                          # minimally coupled fluid, rest energy per comoving volume a^3 rho_m(a)
Lbr = R - c1 * T1 - c2 * T2 - c3 * T3 + c4 * T4 + 2 * (2 - KB) * Jdphi - (2 - KB) * Jf(Y) - F(Q)
L = sqrtg * Lbr - 16 * pi_ * G * N * a ** 3 * rho_m
L = L.subs({c1: KB, c3: -KB, c4: c14 - KB})
def EL(Lag, f):
    e = sp.diff(Lag, f) - sp.diff(sp.diff(Lag, sp.diff(f, t)), t)
    d2 = sp.diff(f, t, 2)
    if Lag.has(d2): e += sp.diff(sp.diff(Lag, d2), t, 2)
    return sp.simplify(e)
EN = EL(L, N); Ea = EL(L, a); Eph = EL(L, ph)
H = sp.Symbol('H'); Qs = sp.Symbol('Q')
def gauge(e):    # N = 1, a'/a = H, phi' = Q
    e = e.subs(sp.Derivative(ph, t), Qs).subs(sp.Derivative(a, t), H * a)
    return sp.simplify(e.subs(N, 1).doit())
EN1 = sp.simplify(gauge(EN.doit()).subs(sp.Derivative(a, t), H * a))
# Friedmann: EN1 = 0  -> solve for H^2
FN = sp.expand((EN1 / a ** 3).subs(Jf(0), 0))                       # J(0) = 0: the carrier carries no cosmological constant (L279's J = beta Y + ...)
Hsol = sp.solve(FN, H ** 2)
print(f"    lapse equation (N = 1): {FN}\n    H^2 = {Hsol}   ({time.time()-T0:.0f} s)")
FQ = sp.Derivative(F(Qs), Qs)
rho_phi = (F(Qs) - Qs * FQ) / (16 * pi_ * G)                        # k-essence sign: L = -F(Q) => rho = F - Q F_Q (checked: F = 2 Lambda gives rho = Lambda/8 pi G)
fried = 8 * pi_ * G * (rho_m + rho_phi) / (3 * (1 + 3 * c2 / 2))
ok2 = len(Hsol) == 1 and sp.simplify(Hsol[0].subs(sp.Derivative(F(Qs), Qs), FQ) - fried) == 0
check("A2 Friedmann from the lapse: 3(1 + 3c2/2) H^2 = 8 pi G [rho_m + rho_phi] with rho_phi = (F - Q F_Q)/(16 pi G): G_cosmo = G/(1 + 3c2/2), Carroll-Lim's khronometric value at c13 = 0 (c14 and K_B drop out of the background); with G_N = G/(1 - c14/2) (L279): G_cosmo/G_N = (1 - c14/2)/(1 + 3c2/2)",
      ok2, f"H^2 = {Hsol}")
Gratio = (1 - c14 / 2) / (1 + 3 * c2 / 2)
c2_bbn = sp.solve(sp.Eq(Gratio.subs(c14, 0), sp.Rational(9, 10)), c2)[0]
print(f"    BBN |G_cosmo/G_N - 1| < 0.1  =>  c2 < {c2_bbn} = {float(c2_bbn):.4f}  (the rigid corner's c2 = 1 is EXCLUDED here: G_cosmo/G_N = {float(Gratio.subs({c2: 1, c14: 8e-7})):.3f}); the equal-speed locus c2 ~ 1e-5 is untouched")
OUT["c2_bbn_max"] = float(c2_bbn)
check("A2b the rigid corner as quoted (c2 = 1) has G_cosmo/G_N = 0.40: excluded by BBN; the rigid corner survives only with c2 < 0.074 (c2 is free there, L280); the equal-speed locus (c2 = c14/(1-2c14) ~ 1e-5) passes",
      float(Gratio.subs({c2: 1, c14: 8e-7})) < 0.9 and float(Gratio.subs({c2: 2.5e-5, c14: 2.5e-5})) > 0.999, f"G_cosmo/G_N: c2 = 1 -> {float(Gratio.subs({c2: 1, c14: 8e-7})):.3f}; equal-speed -> {float(Gratio.subs({c2: 2.5e-5, c14: 2.5e-5})):.6f}")
# scalar equation
Eph1 = sp.simplify(Eph.doit().subs(N, 1))
cons = sp.simplify(sp.diff(a ** 3 * sp.Derivative(F(sp.Derivative(ph, t)), sp.Derivative(ph, t)), t))
ok3 = sp.simplify(Eph1 + cons) == 0 or sp.simplify(Eph1 - cons) == 0
check("A3 the scalar equation on FRW is d/dt[a^3 F_Q(Q)] = 0 exactly (F_Q propto a^-3): the coupling and J(Y) contribute nothing, the conservation law is the potential's alone",
      ok3, f"phi-eq = {Eph1}")
# A4: the quadratic well
K2, Q0, q = sp.symbols('K_2 Q_0 q', real=True)
Fq = K2 * (Qs - Q0) ** 2
rho_quad = sp.expand((Fq - Qs * sp.diff(Fq, Qs)).subs(Qs, Q0 + q))
check("A4 quadratic well F = K2 (Q - Q0)^2: 16 pi G rho_phi = -K2 (2 Q0 q + q^2) = |K2| (2 Q0 q + q^2) for the healthy K2 < 0, q = Q - Q0 propto a^-3 -- dust (2|K2| Q0 q, positive for q > 0) plus a POSITIVE stiff a^-6 term |K2| q^2 (kination-like)",
      sp.simplify(rho_quad + K2 * (2 * Q0 * q + q ** 2)) == 0, f"16 pi G rho_phi = {rho_quad}")
# BBN bound on |K2| Q0^2 (K2-independent combination): |stiff|/rad at a_BBN < 0.1
Om_dm, Om_r, aBBN, H0 = 0.26, 9.1e-5, 2.5e-10, 67.4e3 / 3.0856775814913673e22
# dust today: 2|K2| Q0 |q0| /(16 pi G) = Om_dm rho_c = 3 Om_dm H0^2/(8 pi G)  ->  |K2| Q0 |q0| = 3 Om_dm H0^2
# stiff/dust = |q|/(2 Q0) = |q0| a^-3/(2 Q0) = 3 Om_dm H0^2 a^-3 /(2 |K2| Q0^2);  dust/rad = (Om_dm/Om_r) a
stiff_over_rad = lambda S_over_H02, a_: 3 * Om_dm / (2 * S_over_H02) * a_ ** -3 * (Om_dm / Om_r) * a_     # S = |K2| Q0^2
S_min = 3 * Om_dm * (Om_dm / Om_r) * aBBN ** -2 / (2 * 0.1)
print(f"    BBN: |rho_stiff|/rho_rad(a_BBN = {aBBN:g}) < 0.1  =>  |K2| Q0^2 >= S_min = {S_min:.3e} H0^2  (i.e. Q0 >= {math.sqrt(S_min/3.24e5):.2e} H0 at |K2| = 3.24e5; {math.sqrt(S_min/1.3e5):.2e} H0 at 1.3e5)")
OUT["S_min_over_H0sq"] = S_min
check("A4b the stiff term against BBN (rho_stiff/rho_rad = 3 Om_dm^2 H0^2/(2 S Om_r a^2) with S = |K2| Q0^2): S >= S_min = 15 (Om_dm^2/Om_r) a_BBN^-2 H0^2 = 1.8e23 H0^2 -- for the record's |K2| window this is Q0 >= 7e8 H0 (the roll would have to be ~1e9 times the Hubble rate; L279/L282 assumed Q0 ~ H0)",
      abs(S_min / (15 * Om_dm ** 2 / Om_r * aBBN ** -2) - 1) < 1e-9 and math.sqrt(S_min / 3.24e5) > 1e8, f"S_min = {S_min:.3e} H0^2; Q0,min = {math.sqrt(S_min/3.24e5):.2e} H0 (|K2| = 3.24e5)")
# ---------------- Part B: static lapse mass from the Minkowski build (L282 machinery), omega = 0, matter source
from clock_action_build import build_fourier_matrix
M, S = build_fourier_matrix(); print(f"    Minkowski Fourier matrix rebuilt ({time.time()-T0:.0f} s)", flush=True)
w, k, Q0s, K2s, betas, c2s, c14s, KBs, xis = S['w'], S['k'], S['Q0'], S['K2'], S['beta'], S['c2'], S['c14'], S['KB'], S['xi']
M0 = M.subs({w: 0, xis: 0})
# source: the lapse equation carries +16 pi G rho (L279's Hamiltonian constraint 4 lap Phi - 2 c14 lap Psi = 16 pi G rho + ...); row 0 is the Psi equation.
rho_k = sp.Symbol('rho_k')
sign_row0 = sp.sign(M0[0, 1].subs({K2s: -1, Q0s: 0, c14s: 0, KBs: 0, c2s: 0, betas: 0}).subs(k, 1))   # orientation of the Phi-Laplacian term in row 0
src = sp.Matrix([sign_row0 * 16 * pi_ * G * rho_k, 0, 0, 0])
sol = M0.LUsolve(src)
Psi_k = sp.factor(sp.simplify(sol[0])); P_k = sp.factor(sp.simplify(sol[3]))
print(f"    static lapse response Psi(k) = {Psi_k}")
print(f"    static scalar response P(k)   = {P_k}   ({time.time()-T0:.0f} s)")
OUT["Psi_k_static"] = str(Psi_k); OUT["P_k_static"] = str(P_k)
den = sp.denom(sp.together(sol[0])); num = sp.numer(sp.together(sol[0]))
den_k = sp.Poly(sp.expand(den), k); num_k = sp.Poly(sp.expand(num), k)
print(f"    denominator in k: degree {den_k.degree()}, coefficients {[sp.factor(c) for c in den_k.all_coeffs()]}")
# Newtonian control: Q0 = 0; the scalar in its Newtonian regime is J_Y -> infinity (the carrier's J_Y = beta + sqrt(Y)/atilde0 grows with the field)
beta0s = (2 - KBs) / (2 - c14s)
Geff_raw = sp.factor(sp.simplify(sol[0].subs(Q0s, 0) * k ** 2 / (4 * pi_ * G * rho_k)))
sgn = sp.sign(sp.limit(Geff_raw, betas, sp.oo).subs(c14s, 0))                                  # orient the source so that the Newtonian limit is attractive: Psi = -4 pi G_eff rho/k^2
Geff = sp.factor(sgn * Geff_raw); Geff_newton = sp.limit(Geff, betas, sp.oo)
check("B0 control (Q0 = 0): the static lapse is Psi = -4 pi G_eff rho/k^2 with G_eff = G_N J_Y/(J_Y - beta0), G_N = G/(1 - c14/2): Newton's G_N when the scalar is switched off (J_Y -> infinity) and singular at J_Y -> beta0 (the deep-MOND onset, where the linear response gives way to the nonlinear law of L279)",
      sp.simplify(Geff_newton - 1 / (1 - c14s / 2)) == 0 and sp.simplify(Geff - betas / ((1 - c14s / 2) * (betas - beta0s))) == 0, f"G_eff/G = {Geff}; J_Y -> inf: {Geff_newton}")
# with the roll: the denominator's k-structure. Expect  k^2 [ (2-c14)(...) k^2  +/- mass^2 ]  ->  read mu^2 as the ratio
mu2_candidates = sp.solve(sp.expand(den).subs(k ** 2, sp.Symbol('kk')), sp.Symbol('kk'))
mu2 = [sp.factor(-r_) for r_ in mu2_candidates if sp.simplify(r_) != 0]           # k^2 = -mu^2 poles => Yukawa if mu^2 > 0
print(f"    poles of the static lapse response in k^2: {mu2_candidates}  ->  Yukawa mass^2 candidates mu^2 = -k^2_pole = {mu2}")
OUT["mu2"] = [str(m_) for m_ in mu2]
# the pole of the static response: k^2 = -K2 Q0^2 beta/((2-c14)(beta - beta0)) -> for K2 < 0 and beta > beta0 (the stable linear regime) the pole sits at REAL k: Helmholtz, not Yukawa
kk = sp.Symbol('kk')
pole_list = sp.solve(sp.expand(sp.denom(Psi_k)).subs(k ** 2, kk), kk)
pole = sp.factor(sp.simplify(pole_list[0])) if len(pole_list) == 1 else None
expect_pole = -K2s * Q0s ** 2 * betas / ((2 - c14s) * (betas - beta0s))
ok_mu = sp.simplify(pole - expect_pole) == 0
check("B1 with the roll the static NEWTONIAN potential acquires a scale: Psi(k) = -8 pi G J_Y rho / [(2-c14)(J_Y - beta0) k^2 + K2 Q0^2 J_Y] (hand-derivable from the three static equations: the Hamiltonian constraint with the roll term -2 K2 Q0^2 Psi, Phi = Psi, P = Psi/J_Y), pole at k^2 = |K2| Q0^2 J_Y/((2-c14)(J_Y - beta0)) -- REAL k for the healthy K2 < 0 in the stable regime J_Y > beta0: the potential OSCILLATES beyond 1/mu_Psi (Helmholtz, the AeST/MMH23 behaviour), with mu_Psi^2 -> |K2| Q0^2/(2-c14) in the Newtonian regime J_Y >> beta0",
      ok_mu, f"pole k^2 = {pole}; Psi(k) = {Psi_k}")
OUT["pole_k2"] = str(pole)
# 1/mu at the BBN floor: mu^2 >= |K2| Q0^2/(2-c14) = S/(2-c14) with S >= S_min H0^2  (K2-independent!)
L_max = math.sqrt((2 - 1e-5) / S_min) * C / H0
L_H0 = {K2v: math.sqrt((2 - 1e-5) / K2v) * C / H0 / MPC for K2v in (1.3e5, 3.24e5)}
print(f"    Newtonian-regime 1/mu_Psi at Q0 = H0: {L_H0[3.24e5]:.2f} Mpc (|K2| = 3.24e5), {L_H0[1.3e5]:.2f} Mpc (1.3e5)  [the MMH23-type scale];  at the BBN floor S_min: 1/mu_Psi <= {L_max/PC:.4f} pc = {L_max/AU:.0f} AU, for EVERY K2")
OUT["L_max_pc"] = L_max / PC; OUT["L_at_Q0_H0_Mpc"] = L_H0
check("B2 THE PINCER (K2-independent): BBN's stiff-term floor |K2| Q0^2 >= S_min and the potential's scale mu_Psi^2 = |K2| Q0^2/(2-c14) depend on the SAME product, so 1/mu_Psi <= sqrt((2-c14)/S_min) c/H0 = 0.015 pc: the quadratic-well dust would make the Newtonian potential oscillate beyond ~3000 AU, against Solar-System, binary, Galactic, cluster and lensing gravity out to Mpc -- the K2 (Q - Q0)^2 dust of the action AS WRITTEN is DEAD in this candidate",
      L_max / PC < 0.1, f"1/mu_Psi <= {L_max/PC:.4f} pc")
# ---------------- Part C: the constructive replacement -- a steeper well
Lam, n = sp.symbols('Lambda n', positive=True)
def well(nn):      # F = -(Q-Q0)^n / Lambda^(n-2), healthy sign (F_QQ < 0 as K2 < 0)
    return -(Qs - Q0) ** nn / Lam ** (nn - 2)
rows = {}
for nn in (2, 3, 4, 6):
    Fn = well(nn); rho_n = sp.expand((Fn - Qs * sp.diff(Fn, Qs)).subs(Qs, Q0 + q))
    FQn = sp.diff(Fn, Qs).subs(Qs, Q0 + q)               # propto a^-3  ->  q propto a^{-3/(n-1)}
    exp_q = sp.Rational(-3, nn - 1); exp_corr = nn * exp_q            # q^n propto a^{-3n/(n-1)}
    FQQn = sp.diff(Fn, Qs, 2).subs(Qs, Q0 + q)
    rows[nn] = dict(rho=str(rho_n), q_exp=str(exp_q), corr_exp=str(exp_corr), FQQ=str(sp.factor(FQQn)))
    print(f"    n = {nn}: 16 pi G rho_phi = {rho_n};  q propto a^{exp_q}, correction term propto a^{exp_corr};  F_QQ = {sp.factor(FQQn)}")
OUT["wells"] = rows
check("C1 general well F = -(Q-Q0)^n/Lambda^(n-2): rho_phi = n Q0 (-q)^(n-1)... the dust term is Q0 F_Q propto a^-3 for every n and the correction (n-1) F propto q^n propto a^{-3n/(n-1)}: n = 2 stiff (a^-6), n = 3 a^-4.5, n = 4 RADIATION-like (a^-4), n -> inf dust-like; the quadratic case is the WORST",
      rows[2]["corr_exp"] == "-6" and rows[4]["corr_exp"] == "-4" and rows[3]["corr_exp"] == "-9/2" and rows[6]["corr_exp"] == "-18/5")
# n = 4 numbers: rho = [4 Q0 (-q)^3 + 3 q^4]/Lambda^2 (q < 0): dust D = 4 Q0 |q|^3/Lambda^2 = 16 pi G rho_dm = 6 Om_dm H0^2 ; dark radiation / dust = 3|q|/(4 Q0)
rho4 = sp.expand((well(4) - Qs * sp.diff(well(4), Qs)).subs(Qs, Q0 + q))
check("C2 quartic well F = -(Q-Q0)^4/Lambda^2 (F_QQ = -12 q^2/Lambda^2 < 0, healthy): 16 pi G rho_phi = (4 Q0 q^3 + 3 q^4)/Lambda^2, q > 0, q propto a^-1 -- dust PLUS positive dark radiation (ratio 3q/(4Q0) today, constant relative to photons+neutrinos), and the potential's scale from B1 with |K2| -> |F_QQ|/2 = 6 q^2/Lambda^2: mu_Psi^2 = 6 q^2 Q0^2/(Lambda^2 (2-c14)) = (3/2) D Q0/(q (2-c14)), D = 16 pi G rho_dm = 6 Om_dm H0^2 -- it SHRINKS as a^-2",
      sp.simplify(rho4 - (4 * Q0 * q ** 3 + 3 * q ** 4) / Lam ** 2) == 0 and sp.simplify(sp.diff(well(4), Qs, 2).subs(Qs, Q0 + q) + 12 * q ** 2 / Lam ** 2) == 0, f"16 pi G rho = {rho4}")
# the lock: Delta N_eff vs 1/mu_Psi (n = 4).  f_dr = rho_dr/rho_rad(today) = (3q/(4 Q0)) (Om_dm/Om_r);  mu^2 = (3/2) D Q0/(q (2-c14))  ->  q/Q0 = (3/2) D/(mu^2 (2-c14))
# Delta N_eff = f_dr / 0.1347 (one extra neutrino species at N_eff = 3.044 is 13.47% of the radiation density)
D = 6 * Om_dm; f_nu = 7 / 8 * (4 / 11) ** (4 / 3) / (1 + 3.044 * 7 / 8 * (4 / 11) ** (4 / 3))
def dNeff_of_L(L_Mpc, c14v=1e-5):
    mu2_H0 = (C / H0 / (L_Mpc * MPC)) ** 2                  # mu^2 in H0^2
    q_over_Q0 = 1.5 * D / (mu2_H0 * (2 - c14v))
    return (3 * q_over_Q0 / 4) * (Om_dm / Om_r) / f_nu
lock = {L_: dNeff_of_L(L_) for L_ in (1, 3, 5, 10, 20, 30)}
print(f"    THE LOCK (n = 4): Delta N_eff = {dNeff_of_L(10):.3f} x (1/mu_Psi / 10 Mpc)^2;  table: " + ", ".join(f"{L_} Mpc -> {v:.3f}" for L_, v in lock.items()))
OUT["lock_dNeff_vs_L"] = lock
L_planck = 10 * math.sqrt(0.3 / dNeff_of_L(10)); L_s4 = 10 * math.sqrt(0.06 / dNeff_of_L(10))
print(f"    Planck (Delta N_eff < 0.3): 1/mu_Psi < {L_planck:.1f} Mpc;  CMB-S4 (sensitivity 0.06): tests 1/mu_Psi > {L_s4:.1f} Mpc;  the lensing-RAR (KiDS to ~1-3 Mpc) wants 1/mu_Psi >~ 1-3 Mpc")
OUT["L_planck_max_Mpc"] = L_planck; OUT["L_s4_Mpc"] = L_s4
check("C3 the quartic well opens a WINDOW where the quadratic well had none: Planck's Delta N_eff < 0.3 gives 1/mu_Psi < ~18 Mpc while the lensing-RAR wants >~ 1-3 Mpc; the LOCK Delta N_eff = 0.09 (1/mu_Psi/10 Mpc)^2 (number printed above) ties a CMB-S4-measurable quantity to the potential's oscillation scale -- a two-sided near-term test of the replacement",
      1 < L_planck < 50 and dNeff_of_L(3) < 0.3 < dNeff_of_L(30), f"Delta N_eff(1/mu = 3 Mpc) = {dNeff_of_L(3):.3f}, (12 Mpc) = {dNeff_of_L(12):.3f}, (30 Mpc) = {dNeff_of_L(30):.2f}")
n_pass = sum(CH); print(f"\nL283 COMPLETE: {n_pass}/{len(CH)} checks PASS  ({time.time()-T0:.0f} s).")
json.dump(OUT, open(os.path.splitext(os.path.abspath(__file__))[0] + "_results.json", "w"), indent=1, default=str)
print("""VERDICT.  The candidate's FRW background is Carroll-Lim's (G_cosmo = G/(1+3c2/2): the rigid corner needs c2 < 0.074; the equal-speed locus
is untouched) with the scalar's conservation law a^3 F_Q = const.  The dust of the action as written -- the quadratic well K2 (Q-Q0)^2 --
is DEAD by a K2-independent pincer: its stiff a^-6 companion forces |K2| Q0^2 >= 1.8e23 H0^2 at BBN, and the same product sets the
oscillation scale of the Newtonian potential (the lapse shifts the scalar's clock rate, the well penalises it), 1/mu_Psi <= 0.015 pc.
The replacement is a steeper well: F = -(Q-Q0)^4/Lambda^2 turns the companion into dark radiation and the scale into a shrinking one, with
the lock Delta N_eff = 0.094 (1/mu_Psi / 10 Mpc)^2 -- Planck allows 1/mu_Psi < 18 Mpc, lensing wants >~ 1-3 Mpc, CMB-S4 decides above ~8 Mpc.
Not done: the perturbations of the quartic dust (its kinetic coefficient F_QQ -> 0 at late times: strong-coupling question), the
Goldstone growth mode of L282 on FRW, the Dirac count.""")
sys.exit(0 if n_pass == len(CH) else 1)
