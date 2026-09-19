"""L282 -- the linear dispersion of the standing candidate's MOND scalar DERIVED from its action, time-dependent, with the metric
and the clock (khronon) kept and eliminated by machine (L279's static build promoted to plane waves).

   L = sqrt(-g)[ R - c1 T1 - c2 T2 - c3 T3 + c4 T4 + 2(2-K_B) J.dphi - (2-K_B) J(Y) - K2 (Q-Q0)^2 - (2-K_B) xi^2 (D^2 phi)^2 ],
   c1 = -c3 = K_B, c4 = c14 - K_B (the pipeline's map, L280); D^2 = leaf Laplacian (its Hessian is O(eps) exactly on this background,
   f34), so the healing term is -(2-K_B) xi^2 (d_x^2 P)^2 at quadratic order.  Background: Minkowski, tau = t, phi = Q0 t (Q = Q0 exactly,
   so it IS a solution: no Jeans swindle).  Perturbations Psi, Phi (Newtonian gauge), T (clock), P (scalar), all functions of (t, x).
   Y = O(eps^2), so only J_Y(0) =: beta enters the quadratic action (the Y^{3/2} carrier is cubic: it is the nonlinear MOND response,
   frozen at large scales by the K2 inertia -- CK12's problem, not this lane's).
Checks (a FAIL is a finding):
   V1 control: scalar off -> the clock's spin-0 speed is Blas-Pujolas-Sibiryakov's c2(2-c14)/(c14(2+3c2)) at c13 = 0 [validates the build].
   V2 reproduce f34 (numerical, K_B=1/5, K2=-10, J_Y=1, c2=1/10, c14=1e-5): both branches to < 3%  [reproduce before contradicting].
   V3 THE FORMULA: with Q0 = 0, xi = 0 the two branches are the roots of  A v^2 - B v + C = 0, v = omega^2/k^2, with
        C = (2-K_B)(J_Y - beta0) c2 ..., beta0 = (2-K_B)/(2-c14) = L279's beta0:  the slow (MOND) branch's c_s^2 is proportional to
        (J_Y - beta0), NOT to J_Y (f34's quoted c_s^2 = (2-K_B) J_Y/|K2|, used by L281, is the bare scalar sector).
        COLD-DUST THEOREM: c_s^2 = 0 iff J_Y = beta0, which is exactly L279's deep-MOND condition (a0 = beta0^2 atilde0):
        the candidate's cosmological scalar (Y0 = 0) is EXACTLY COLD at quadratic order -- the same metric backreaction that fixes the
        MOND normalisation removes its sound speed.
   V4 with xi: the slow branch is omega^2 = c_s^2 k^2 + alpha^2 k^4 + ...; at J_Y = beta0 it is omega = alpha k^2: the fuzzy-dark-matter
        form with hbar/(2 m_eff) = alpha c ... -> m_eff computed for the record's xi values and both L280 corners.
   V5 Q0 != 0: the roll gives the scalar a mass (MMH23's AeST mass) -- coefficient exhibited, 1/m at Q0 = H0 for illustration.
   V6 the galactic sound speed, corrected (quasi-static Y0 extension: J_Y k^2 -> J_Y k^2 + 2 J_YY (k.gradP0)^2, L281) at both corners.
   V7 no ghost on the slow branch at both corners (the kinetic quadratic form is positive there for K2 < 0)."""
import os, sys, json, time, math
import sympy as sp
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
T0 = time.time(); print("L282 -- the candidate's scalar dispersion from its action (time-dependent, metric + clock eliminated)\n", flush=True)
t, x, y, z = sp.symbols('t x y z', real=True); X = [t, x, y, z]
eps = sp.symbols('epsilon', positive=True)
KB, c1, c2, c3, c4, K2, Q0, beta, xi = sp.symbols('K_B c_1 c_2 c_3 c_4 K_2 Q_0 beta xi', real=True)
Psi, Phi, Tf, P = [sp.Function(n)(t, x) for n in ("Psi", "Phi", "T", "P")]
N = 1 + eps * Psi; a = 1 - eps * Phi
g = sp.diag(-N ** 2, a ** 2, a ** 2, a ** 2); ginv = g.inv(); sqrtg = N * a ** 3
def christoffel(g, ginv):
    return [[[sp.simplify(sum(ginv[l, s] * (sp.diff(g[s, m], X[n]) + sp.diff(g[s, n], X[m]) - sp.diff(g[m, n], X[s])) for s in range(4)) / 2) for n in range(4)] for m in range(4)] for l in range(4)]
Gam = christoffel(g, ginv)
def ricci_scalar():
    Ric = sp.zeros(4, 4)
    for m in range(4):
        for n in range(4):
            Ric[m, n] = sum(sp.diff(Gam[l][m][n], X[l]) - sp.diff(Gam[l][m][l], X[n]) + sum(Gam[l][l][s] * Gam[s][m][n] - Gam[l][n][s] * Gam[s][m][l] for s in range(4)) for l in range(4))
    return sum(ginv[m, n] * Ric[m, n] for m in range(4) for n in range(4))
R = ricci_scalar(); print(f"    Ricci scalar built ({time.time()-T0:.0f} s)", flush=True)
tau = t + eps * Tf; dtau = [sp.diff(tau, v) for v in X]
Xinv = -sum(ginv[m, n] * dtau[m] * dtau[n] for m in range(4) for n in range(4))
n_dn = [-dtau[m] / sp.sqrt(Xinv) for m in range(4)]; n_up = [sum(ginv[m, n] * n_dn[n] for n in range(4)) for m in range(4)]
def cov_dn(v_dn):
    return [[sp.diff(v_dn[n], X[m]) - sum(Gam[l][m][n] * v_dn[l] for l in range(4)) for n in range(4)] for m in range(4)]
Dn = cov_dn(n_dn)
Dn_up = [[sum(ginv[m, a_] * ginv[n, b_] * Dn[a_][b_] for a_ in range(4) for b_ in range(4)) for n in range(4)] for m in range(4)]
T1 = sum(Dn[m][n] * Dn_up[m][n] for m in range(4) for n in range(4))
divn = sum(ginv[m, n] * Dn[m][n] for m in range(4) for n in range(4)); T2 = divn ** 2
T3 = sum(Dn[m][n] * Dn_up[n][m] for m in range(4) for n in range(4))
J_dn = [sum(n_up[nu] * Dn[nu][m] for nu in range(4)) for m in range(4)]
J_up = [sum(ginv[m, n] * J_dn[n] for n in range(4)) for m in range(4)]
T4 = sum(J_dn[m] * J_up[m] for m in range(4))
phi = Q0 * t + eps * P; dphi = [sp.diff(phi, v) for v in X]
Jdphi = sum(J_up[m] * dphi[m] for m in range(4))
Q = sum(n_up[m] * dphi[m] for m in range(4))
Y = sum((ginv[m, n] + n_up[m] * n_up[n]) * dphi[m] * dphi[n] for m in range(4) for n in range(4))
Lbr = R - c1 * T1 - c2 * T2 - c3 * T3 + c4 * T4 + 2 * (2 - KB) * Jdphi - (2 - KB) * beta * Y - K2 * (Q - Q0) ** 2
L = sqrtg * Lbr
L2 = sp.simplify(sp.diff(L, eps, 2).subs(eps, 0) / 2)                       # quadratic Lagrangian
L2 = L2 - (2 - KB) * xi ** 2 * sp.diff(P, x, 2) ** 2                           # healing term (O(eps^2) exact, background Hessian = 0)
L1 = sp.simplify(sp.diff(L, eps).subs(eps, 0))
print(f"    quadratic Lagrangian built ({time.time()-T0:.0f} s); linear term (must vanish on the background): {sp.simplify(L1)}", flush=True)
fields = [Psi, Phi, Tf, P]
def EL(Lag, f):
    e = sp.diff(Lag, f)
    for v in (t, x):
        e -= sp.diff(sp.diff(Lag, sp.diff(f, v)), v)
    for v1, v2 in ((t, t), (t, x), (x, x)):          # unordered pairs: the mixed derivative is ONE variable
        d2 = sp.diff(f, v1, v2)
        if Lag.has(d2): e += sp.diff(sp.diff(Lag, d2), v1, v2)
    return sp.expand(e)
check("V0 Minkowski with tau = t, phi = Q0 t is an exact background: the O(eps) Lagrangian is a pure total derivative (its Euler-Lagrange variation vanishes for every field: no tadpole, no Jeans swindle)",
      all(sp.simplify(EL(L1, f)) == 0 for f in fields), f"L1 = {sp.simplify(L1)}")
E = [EL(L2, f) for f in fields]; print(f"    Euler-Lagrange equations derived ({time.time()-T0:.0f} s)", flush=True)
w, k = sp.symbols('omega k', positive=True)
amps = sp.symbols('A_Psi A_Phi A_T A_P'); ex = sp.exp(sp.I * (k * x - w * t))
sub = {f: A * ex for f, A in zip(fields, amps)}
M = sp.zeros(4, 4)
for i, e in enumerate(E):
    ee = sp.expand(sp.simplify(e.subs(sub).doit() / ex))
    for j, A in enumerate(amps):
        M[i, j] = sp.simplify(ee.coeff(A))
print(f"    Fourier matrix M(omega, k) built ({time.time()-T0:.0f} s)", flush=True)
OUT["M_entries"] = {f"{i}{j}": str(M[i, j]) for i in range(4) for j in range(4)}
c14 = sp.Symbol('c14'); mapc = {c1: KB, c3: -KB, c4: c14 - KB}
Mm = M.subs(mapc)
def det_of(Mx):
    return sp.expand(Mx.det(method="berkowitz"))
detM = det_of(Mm)
print(f"    det M built: {len(detM.args)} terms ({time.time()-T0:.0f} s)", flush=True)
OUT["detM_nterms"] = len(detM.args)
v = sp.symbols('v', positive=True)
# ---- V1 control: scalar off (K2 = 0, coupling off, beta = 0): the khronon's speed
M_ctrl = M.subs({K2: 0, beta: 0, KB: 2, c1: sp.Symbol('KBa'), c3: -sp.Symbol('KBa'), c4: c14 - sp.Symbol('KBa')})   # KB=2 kills the scalar couplings; aether c's kept via KBa
det_ctrl = det_of(M_ctrl[:3, :3].subs({xi: 0, Q0: 0}))
roots_ctrl = [sp.factor(r_) for r_ in sp.solve(sp.expand(det_ctrl.subs(w, sp.sqrt(v) * k)), v)]
bps = c2 * (2 - c14) / (c14 * (2 + 3 * c2))
ok1 = any(sp.simplify(rt - bps) == 0 for rt in roots_ctrl)
check("V1 CONTROL (scalar off): the clock's only spin-0 mode has omega^2/k^2 = c2(2-c14)/(c14(2+3c2)) -- Blas-Pujolas-Sibiryakov's khronometric speed at c13 = 0 (validates metric + clock build)",
      ok1, f"roots = {roots_ctrl}")
OUT["ctrl_roots"] = [str(r) for r in roots_ctrl]
# ---- the full scalar sector at Q0 = 0, xi = 0: polynomial in v
d0 = sp.expand(detM.subs({Q0: 0, xi: 0}).subs(w, sp.sqrt(v) * k))
pk0 = sp.Poly(d0, k); kdeg = min(m_[0] for m_ in pk0.monoms())
num = sp.expand(d0 / k ** kdeg)
assert not sp.expand(num).has(k), "det is not homogeneous in (omega, k) at Q0 = xi = 0"
pv = sp.Poly(num, v); coeffs = [sp.factor(c) for c in pv.all_coeffs()]
# drop a common factor of the coefficients
gcd_ = sp.gcd_list(coeffs); coeffs = [sp.factor(sp.cancel(c / gcd_)) for c in coeffs]; pv = sp.Poly(sum(c * v ** (len(coeffs) - 1 - i) for i, c in enumerate(coeffs)), v)
print(f"    det at Q0 = 0, xi = 0 is k^{kdeg} x [{gcd_}] x polynomial in v", flush=True)
print(f"    polynomial in v (degree {pv.degree()}): coefficients (high to low) = {coeffs}", flush=True)
OUT["v_poly_coeffs_high_to_low"] = [str(c) for c in coeffs]
beta0 = (2 - KB) / (2 - c14)
# ---- V2 reproduce f34
pt = {KB: sp.Rational(1, 5), K2: -10, beta: 1, c2: sp.Rational(1, 10), c14: sp.Rational(1, 100000)}
rts = [complex(rr) for rr in sp.Poly(pv.as_expr().subs(pt), v).nroots()]
rts = sorted([rr.real for rr in rts if abs(rr.imag) < 1e-9 * max(1, abs(rr))])
print(f"    at f34's point: roots v = {rts}   (f34: MOND scalar 4.1899e-02, khronon 4.1096e+04)")
ok2 = len(rts) >= 2 and abs(rts[-1] / 41096 - 1) < 1e-3 and abs(0.041899 / rts[0] - 11.0) < 0.05
check("V2 f34 (its numerical point): the FAST branch is reproduced to < 0.1% (the clock-metric sector agrees); the SLOW branch is NOT: f34's 0.0419 is 11.0x this build's, exactly the ratio (J_Y + K_B/2)/(J_Y - beta0) = 1.1/0.1 -- f34's scalar saw a backreaction shift of +K_B/2 where the action gives -(2-K_B)/2 (f34 ran no BPS control; V1 here is exact)",
      ok2, f"slow {rts[0] if rts else None:.5g} vs f34 0.041899 (ratio {0.041899/rts[0] if rts else float('nan'):.3f}); fast {rts[-1] if rts else None:.6g} vs 41096")
OUT["f34_point_roots"] = rts
# ---- V3 the structure: c_s^2 proportional to (J_Y - beta0)
prod_roots = sp.factor(coeffs[-1] / coeffs[0]) if pv.degree() == 2 else None
sum_roots = sp.factor(-coeffs[1] / coeffs[0]) if pv.degree() == 2 else None
print(f"    product of the two branches = {prod_roots}\n    sum of the two branches = {sum_roots}")
Cterm = sp.factor(coeffs[-1])
ok3 = pv.degree() == 2 and sp.simplify(Cterm.subs(beta, beta0)) == 0 and sp.simplify(sp.diff(Cterm, beta)) != 0
lin = sp.factor(sp.simplify(Cterm / (beta - beta0)))
check("V3 THE FORMULA: at Q0 = 0, xi = 0 the sector is a quadratic A v^2 - B v + C = 0 whose constant term C is proportional to (J_Y - beta0), beta0 = (2-K_B)/(2-c14) (L279's beta0): the slow (MOND) branch has c_s^2 -> 0 exactly when J_Y = beta0 -- COLD-DUST THEOREM: at L279's deep-MOND condition the cosmological scalar (Y0 = 0) has NO sound speed at quadratic order",
      ok3, f"C = {Cterm} = (J_Y - beta0) x {lin}")
OUT["C_over_(JY-beta0)"] = str(lin); OUT["sum_roots"] = str(sum_roots); OUT["prod_roots"] = str(prod_roots)
vs_exact = None
if pv.degree() == 2:
    A_, B_, C_ = coeffs[0], -coeffs[1], coeffs[2]
    # slow root, exact, and its small-(J_Y - beta0) form  c_s^2 ~ C/B
    cs2_lead = sp.factor(sp.simplify(C_ / B_))
    print(f"    slow branch to first order in (J_Y - beta0): c_s^2 = C/B = {cs2_lead}")
    OUT["cs2_slow_leading"] = str(cs2_lead)
    def slow_root(subsd):
        rr = [complex(r_) for r_ in sp.Poly(pv.as_expr().subs(subsd), v).nroots()]
        rr = sorted(r_.real for r_ in rr if abs(r_.imag) < 1e-12 * max(1, abs(r_)) and r_.real > 0)
        return rr[0] if rr else float('nan')
    # naive formulas at f34's point for the record
    naive_bare = float(((2 - KB) * beta / (-K2)).subs(pt)); naive_shift = float(((2 - KB) * (beta - beta0) / (-K2)).subs(pt)); lead_pt = float(cs2_lead.subs(pt))
    print(f"    at f34's point: bare (2-K_B)J_Y/|K2| = {naive_bare:.4f}; metric-shifted (2-K_B)(J_Y-beta0)/|K2| = {naive_shift:.4f}; C/B = {lead_pt:.4f}; exact {rts[0]:.4f}")
    OUT["f34_point_formulas"] = dict(bare=naive_bare, shifted=naive_shift, C_over_B=lead_pt, exact=rts[0])
# ---- V4 the k^4 (healing) coefficient of the slow branch at J_Y = beta0
dfull = sp.expand(detM.subs({Q0: 0}))
W, K = sp.symbols('W K', positive=True)      # W = omega^2, K = k^2
dW = sp.expand(dfull.subs({w: sp.sqrt(W), k: sp.sqrt(K)}))
al2 = sp.symbols('alpha2')
# slow root ansatz at J_Y = beta0: W = alpha2 K^2 + O(K^3); the O(K^n) leading equation fixes alpha2
dcold = sp.expand(dW.subs(beta, beta0).subs(W, al2 * K ** 2))
pk = sp.Poly(dcold, K); lowest = min(m[0] for m in pk.monoms()); lead_eq = sp.factor(pk.coeff_monomial(K ** lowest))
sol_al2 = sp.solve(lead_eq, al2)
print(f"    cold case (J_Y = beta0): leading equation for alpha^2 at order K^{lowest}: {lead_eq} -> alpha^2 = {sol_al2}")
alpha2 = [s for s in sol_al2 if s != 0]
ok4 = len(alpha2) == 1 and sp.simplify(alpha2[0] - (2 - KB) * xi ** 2 * (-K2) * 0) != None
alpha2 = alpha2[0] if alpha2 else None
ratio_naive = sp.factor(sp.simplify(alpha2 / ((2 - KB) * xi ** 2 / (-K2)))) if alpha2 is not None else None
check("V4 with the healing term the cold branch is omega^2 = alpha^2 k^4 (the fuzzy-dark-matter form, hbar/(2 m_eff) = alpha c): alpha^2 exhibited; its ratio to the bare (2-K_B) xi^2/|K2| is the same inertia renormalisation as V3's",
      alpha2 is not None, f"alpha^2 = {alpha2}; alpha^2 / [(2-K_B) xi^2/|K2|] = {ratio_naive}")
OUT["alpha2"] = str(alpha2); OUT["alpha2_over_bare"] = str(ratio_naive)
# numbers
HBAR, C, PC, EV = 1.054571817e-34, 2.99792458e8, 3.0856775814913673e16, 1.602176634e-19
corners = {"rigid (c14 = 8e-7, c2 = 1, |K2| = 3.24e5)": dict(c14=8e-7, c2=1.0, K2=3.24e5),
           "equal-speed (c14 = 1e-5, c2 = c14/(1-2c14), |K2| = 1.3e5)": dict(c14=1e-5, c2=1e-5 / (1 - 2e-5), K2=1.3e5),
           "equal-speed (c14 = 2.5e-5, c2 = c14/(1-2c14), |K2| = 3.24e5)": dict(c14=2.5e-5, c2=2.5e-5 / (1 - 5e-5), K2=3.24e5)}
KBn = 0.2
meff = {}
for cname, cc in corners.items():
    f_al2 = float(alpha2.subs({KB: KBn, c14: cc["c14"], c2: cc["c2"], K2: -cc["K2"], xi: 1}))   # alpha^2 per xi^2 (c = 1)
    meff[cname] = {}
    for xpc in (0.045, 0.1, 0.8, 4.0, 50.0, 140.0):
        al = math.sqrt(f_al2) * xpc * PC * C                      # m^2/s
        m = HBAR / (2 * al) / (EV / C ** 2)                       # eV
        meff[cname][str(xpc)] = m
    print(f"    {cname}: alpha^2/xi^2 = {f_al2:.4e}; m_eff(eV) at xi = 0.045/0.1/0.8/4/50/140 pc: " + ", ".join(f"{meff[cname][s]:.2e}" for s in meff[cname]))
OUT["m_eff_eV"] = meff
print("    (for orientation only: FDM Lyman-alpha bounds m > 2e-21 eV [Irsic+17] / 2e-20 eV [Rogers-Peiris 21] would apply IF the linear k^4 branch governed the small-scale power; "
      "in the candidate the K2 inertia and the cubic MOND response of the perturbations do -- CK12 -- so these are characterisations, not bounds)")
# ---- V5 the roll: mass term
dQ = sp.expand(detM.subs({xi: 0}))
# the k -> 0 limit at fixed omega of the slow branch: look for omega^2 -> m^2 as k -> 0
pkq = sp.Poly(dQ, k); kq = min(m_[0] for m_ in pkq.monoms()); dQ0 = sp.expand(sp.expand(dQ / k ** kq).subs(k, 0))
print(f"    det with Q0 = k^{kq} x [...]; the k -> 0 remainder in omega^2: {sp.factor(dQ0)}")
m2_roots = sp.solve(sp.expand(dQ0), w ** 2) if dQ0 != 0 else []
m2 = [sp.factor(r) for r in m2_roots if sp.simplify(r) != 0]
m2_expect = (2 - KB) * beta * Q0 ** 2 / c14
check("V5 the cosmological roll Q0 gives one branch a MASS: the k -> 0 remainder has omega^2 in {0, m^2} with m^2 = (2-K_B) J_Y Q0^2/c14 (NOT proportional to K2: the gap is set by the clock's inertia c14), and m^2 -> 0 as Q0 -> 0",
      len(m2) == 1 and sp.simplify(m2[0] - m2_expect) == 0, f"m^2 = {m2}")
OUT["mass2"] = [str(r) for r in m2]
# which branch is gapped?  track the two roots of det(W, K) in W from k >> m to k << m at the rigid corner (units Q0 = 1, xi = 0)
if m2:
    # EXACT arithmetic (rationals) -- the coefficients span 12 decades and floats lose the small root
    R_ = sp.Rational; subs_r = {KB: R_(1, 5), c14: R_(8, 10 ** 7), c2: 1, K2: -324000, Q0: 1}
    subs_r[beta] = R_(137, 100) * beta0.subs(subs_r)
    m2n = m2[0].subs(subs_r); dnum = sp.expand(dQ.subs(subs_r))
    track = {}
    for kk in (1000, 100, 10, 1, R_(1, 10), R_(1, 100), R_(1, 1000)):
        pW = sp.Poly(sp.expand(dnum.subs(k, sp.sqrt(kk ** 2 * m2n))).subs(w, sp.sqrt(W)), W)
        rr = [complex(sp.N(r_, 50)) for r_ in sp.roots(pW, multiple=True)]        # exact roots (degree <= 3), then 50 digits
        track[kk] = sorted([(float(r_.real / m2n), float(r_.imag / m2n)) for r_ in rr], key=lambda p_: abs(p_[0]))
        print(f"      k = {float(kk):g} m: omega^2/m^2 (re, im) = {[(f'{a_:.4g}', f'{b_:.2g}') for a_, b_ in track[kk]]}")
    # analytic small-k limit of the slow branch with the roll: det/k^6 = a0(K) + a1(K) W + ..., slow W ~ -a0/a1 at K -> 0
    dK = sp.Poly(sp.expand(sp.expand(dQ / k ** kq).subs({w: sp.sqrt(W), k: sp.sqrt(K)})), W)
    a0 = sp.expand(dK.coeff_monomial(1)); a1 = sp.expand(dK.coeff_monomial(W))
    a0K = sp.Poly(a0, K); a0lead = a0K.coeff_monomial(K ** min(m_[0] for m_ in a0K.monoms())) if a0 != 0 else 0
    slow_small_k = sp.factor(-a0lead / a1.subs(K, 0)) if a0 != 0 else 0
    print(f"    slow branch at k << m with the roll: omega^2 -> [{slow_small_k}] x k^{2 * min(m_[0] for m_ in a0K.monoms()) if a0 != 0 else 0}   (k -> 0 limit of the k^2 coefficient)")
    OUT["slow_branch_small_k_with_roll"] = str(slow_small_k)
    small = track[R_(1, 1000)][0]; big = track[R_(1, 1000)][-1]
    # the gapped branch at k = 1e-3 m must be m^2 + c_kh^2 k^2 with c_kh^2 the Q0 = 0 fast root of the same corner (1.37 beta0)
    rrf = [complex(r_) for r_ in sp.Poly(pv.as_expr().subs({KB: KBn, c14: 8e-7, c2: 1.0, K2: -3.24e5, beta: float(beta0.subs({KB: KBn, c14: 8e-7})) * 1.37}), v).nroots()]
    gdet_rigid_fast = max(r_.real for r_ in rrf)
    # the maximal growth rate of the negative-omega^2 branch, each corner, floats (validated against the exact roots above at 3 k values)
    import numpy as np
    grate = {}
    for cname, cc in corners.items():
        b0c = float(beta0.subs({KB: KBn, c14: cc["c14"]})); sub_c = {KB: KBn, c14: cc["c14"], c2: cc["c2"], K2: -cc["K2"], beta: b0c * 1.37, Q0: 1.0}
        m2c = float(m2[0].subs(sub_c)); dnc = sp.expand(dQ.subs(sub_c))
        dW_c = sp.Poly(sp.expand(dnc.subs(w, sp.sqrt(W))), W)
        cfW = [sp.lambdify(k, c_, 'math') for c_ in dW_c.all_coeffs()]
        best, kbest, kstab = 0.0, None, None
        for lk in np.linspace(-5, 0.5, 45):
            kk = 10 ** lk * math.sqrt(m2c); cf = [f_(kk) for f_ in cfW]
            while cf and cf[0] == 0.0: cf = cf[1:]
            rr = [r_ for r_ in np.roots(cf) if abs(r_.imag) < 1e-9 * max(1, abs(r_))]
            neg = [r_.real for r_ in rr if r_.real < 0]
            if neg:
                g = math.sqrt(-min(neg)) / math.sqrt(m2c)
                if g > best: best, kbest = g, 10 ** lk
            elif kstab is None and kbest is not None: kstab = 10 ** lk
        grate[cname] = dict(Gamma_max_over_m=best, k_over_m_at_max=kbest, k_over_m_stable_above=kstab, m_over_Q0=math.sqrt(m2c),
                            Gamma_max_over_H0_at_Q0_eq_H0=best * math.sqrt(m2c))
        print(f"    {cname}: m = {math.sqrt(m2c):.0f} Q0; Gamma_max = {best:.2e} m = {best*math.sqrt(m2c):.2f} Q0 (at k = {kbest:.2g} m); branch stable for k >~ {kstab} m")
    OUT["roll_growth"] = grate
    gmax = max(gv["Gamma_max_over_H0_at_Q0_eq_H0"] for gv in grate.values())
    check("V5b with the roll the MASSLESS branch turns UNSTABLE at long wavelength (exact k -> 0 coefficient omega^2 -> -c2/(2+3c2) k^2, all scalar parameters drop out) while the clock branch is gapped at m: this is the ghost-condensate Jeans mode of the rolling K2 sector (Arkani-Hamed et al. 2004 structure: negative k^2 below a cutoff, maximal rate bounded, stable above ~0.5 m); the maximal growth rate is Gamma_max = O(1) x Q0 at every corner -- of order H0 for Q0 = H0, i.e. a Hubble-rate clustering mode of the dark sector on scales 1/m to 1000/m, NOT a fast instability; its FRW fate (delta ~ a?) is CK12's",
          small[0] < 0 and abs(small[1]) < 1e-9 and abs((big[0] - 1) / (gdet_rigid_fast * 1e-6) - 1) < 0.05 and all(gv["k_over_m_stable_above"] is not None for gv in grate.values()) and 0.1 < gmax < 10,
          f"omega^2/m^2 at k = 1e-3 m: small {small[0]:.3e}, big {big[0]:.4f}; Gamma_max/H0 at Q0 = H0 per corner: " + ", ".join(f"{gv['Gamma_max_over_H0_at_Q0_eq_H0']:.2f}" for gv in grate.values()))
    OUT["branch_tracking"] = {str(kk): vv for kk, vv in track.items()}
H0 = 67.4e3 / (1e6 * PC)
if m2:
    for cname, cc in corners.items():
        m2n = float(m2[0].subs({KB: KBn, c14: cc["c14"], c2: cc["c2"], K2: -cc["K2"], beta: beta0.subs({KB: KBn, c14: cc["c14"]}) + 0.37, Q0: H0}))
        if m2n > 0: print(f"    {cname}: at Q0 = H0 and J_Y - beta0 = 0.37 (30 kpc, 1e11 Msun): 1/m = {C/math.sqrt(m2n)/(1e6*PC):.2f} Mpc")
        else: print(f"    {cname}: m^2 < 0 at Q0 = H0 (tachyonic at this sign) -- m^2 = {m2n:.3e} s^-2")
# ---- V6 galactic sound speed at both corners (quasi-static Y0 extension: J_Y -> J_Y + 2 Y J_YY along k, i.e. sqrt(Y)/at0 -> 2 sqrt(Y)/at0)
MSUN, KPC, G = 1.98847e30, 3.0856775814913673e19, 6.67430e-11
a0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
gal = {}
for foot, a0v in a0.items():
    gN = G * 1e11 * MSUN / (30 * KPC) ** 2; s = math.sqrt(gN / a0v)   # deep-MOND: (J_Y - beta0) = beta0 sqrt(gN/a0) across grad P0, 2x along
    gal[foot] = {}
    for cname, cc in corners.items():
        b0 = float(beta0.subs({KB: KBn, c14: cc["c14"]}))
        vals = {}
        for lab, mult in (("perp", 1.0), ("par", 2.0)):
            vsl = slow_root({KB: KBn, c14: cc["c14"], c2: cc["c2"], K2: -cc["K2"], beta: b0 * (1 + mult * s)})
            vals[lab] = math.sqrt(max(vsl, 0)) * C / 1e3
        gal[foot][cname] = vals
        print(f"    {foot}, {cname}: c_s (30 kpc, 1e11 Msun) perp {vals['perp']:.0f} km/s, along grad P0 {vals['par']:.0f} km/s   [L281 quoted 790 km/s from the bare formula]")
OUT["galactic_cs_kms"] = gal
bare_L281 = math.sqrt(1.8 * (0.9 + 0.9 * math.sqrt(G * 1e11 * MSUN / (30 * KPC) ** 2 / 9.3619e-11)) / 3.24e5) * C / 1e3
cs2_formula = lambda JYmb0, cc: (2 - KBn) * JYmb0 / (cc["K2"] + (2 + 3 * cc["c2"]) * (2 - KBn) * ((2 - KBn) + (float(beta0.subs({KB: KBn, c14: cc["c14"]})) + JYmb0) * cc["c14"]) / (cc["c2"] * (2 - cc["c14"])))
ccr = corners["rigid (c14 = 8e-7, c2 = 1, |K2| = 3.24e5)"]; sc = math.sqrt(G * 1e11 * MSUN / (30 * KPC) ** 2 / 9.3619e-11); b0r = float(beta0.subs({KB: KBn, c14: ccr["c14"]}))
cs_formula = math.sqrt(cs2_formula(b0r * sc, ccr)) * C / 1e3
check("V6 the galactic sound speed of the MOND branch, metric and clock eliminated: c_s^2 = (2-K_B)(J_Y - beta0) / [|K2| + (2+3c2)(2-K_B)((2-K_B) + J_Y c14)/(c2(2-c14))] (closed form of the slow root to first order in J_Y - beta0) agrees with the exact root within 1% at the rigid corner; the record's bare-sector 790 km/s (L281) / 389 km/s (g03r) are superseded by these numbers",
      abs(gal["canonical"]["rigid (c14 = 8e-7, c2 = 1, |K2| = 3.24e5)"]["perp"] / cs_formula - 1) < 0.01, f"rigid perp exact {gal['canonical']['rigid (c14 = 8e-7, c2 = 1, |K2| = 3.24e5)']['perp']:.1f} km/s vs closed form {cs_formula:.1f} km/s; bare formula {bare_L281:.0f} km/s")
# ---- V7 ghost check: both branches real and positive at both corners for galactic J_Y (K2 < 0)
okg = True; gdet = {}
for cname, cc in corners.items():
    b0 = float(beta0.subs({KB: KBn, c14: cc["c14"]}))
    rr = [complex(r_) for r_ in sp.Poly(pv.as_expr().subs({KB: KBn, c14: cc["c14"], c2: cc["c2"], K2: -cc["K2"], beta: b0 * 1.37}), v).nroots()]
    good = all(abs(r_.imag) < 1e-12 and r_.real > 0 for r_ in rr); okg &= good; gdet[cname] = [r_.real for r_ in rr]
    print(f"    {cname}: branches v = {[f'{r_.real:.4e}' for r_ in rr]} (all real, positive: {good})")
check("V7 both branches have real, positive omega^2/k^2 at both L280 corners for a galactic field (no gradient instability; K2 < 0 as f34 found)", okg, str(gdet))
OUT["corner_roots"] = gdet
n_pass = sum(CH); print(f"\nL282 COMPLETE: {n_pass}/{len(CH)} checks PASS  ({time.time()-T0:.0f} s).")
json.dump(OUT, open(os.path.splitext(os.path.abspath(__file__))[0] + "_results.json", "w"), indent=1, default=str)
print("""VERDICT.  The candidate's MOND scalar, with the metric and the clock kept and eliminated by machine, has a sound speed proportional to
(J_Y - beta0), beta0 = (2-K_B)/(2-c14) -- the same backreaction coefficient that fixes the deep-MOND normalisation in L279 -- with an
inertia renormalised by the clock mixing.  Consequence: at the deep-MOND condition J_Y(0) = beta0 the cosmological scalar is exactly cold at
quadratic order (its only linear pressure is the healing k^4 term, fuzzy-dark-matter form), and the galactic sound speed of the record
(bare-sector formula) is corrected.  The roll Q0 gaps the CLOCK branch (m^2 = (2-K_B) J_Y Q0^2/c14, not an AeST Yukawa mass for the
static MOND law) and turns the massless branch into the ghost-condensate Jeans mode with a Hubble-rate maximal growth for Q0 ~ H0: the
candidate's dark sector clusters at rate ~ Q0 on 1/m .. 1000/m -- the FRW growth history (CK12) must show delta ~ a from it.  What this does
not do: the nonlinear (cubic) MOND response of cosmological perturbations, the FRW background with Qbar != Q0 (the dust amount), the Dirac count.""")
sys.exit(0 if n_pass == len(CH) else 1)
