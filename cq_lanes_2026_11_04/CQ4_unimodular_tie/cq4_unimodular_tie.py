#!/usr/bin/env python3
"""
CQ4_unimodular_tie -- sympy checks of every equation used in derivation.md.

kappa = 1/2 FITTED; not theory closed.  Footings canonical 9.3603e-11 and alt 1.1312e-10 m/s^2, never pooled.
Criteria: FROZEN_CRITERIA.md (commit 1118e49b50), committed alone before this script.  Not blind.

Action (form U, the v3s instance; Lambda(x) and the vector density B^mu(x) are the only new fields):
    S = (c^3/16 pi G) Int d^4x { sqrt(-g) [R - 2 J(Y; Lambda) + 2 K(Q)] + 2 Lambda d_mu B^mu } - (gamma_L/2) Int sqrt(-g) (D.P)^2 + S_m
    J(Y; Lambda) = Lambda - 2 alpha^2 Lambda [u - ln(1+u)],   u = sqrt(Y / (alpha^2 Lambda)),   alpha dimensionless.
Form G (generic): any MOND sector whose only scale is the multiplier, J = Lambda j(Y/Lambda).
Symbolic part in c = 1 units; Lambda_v = 8 pi G rho_v / c^2 is a matter vacuum energy in geometric units (1/m^2).

Lines marked [OK]/[BAD] are script-integrity checks (BAD = the script is broken, the lane does not grade).
Lines marked [PASS]/[FAIL] are the frozen gates (FAIL is a result).
Literature in comments is from memory and PROVISIONAL.
"""
import math, sys
import sympy as sp

BAD = []
def check(name, ok, detail=""):
    print(f"  [{'OK ' if ok else 'BAD'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok:
        BAD.append(name)

GATES = {}
def gate(name, ok, detail=""):
    GATES[name] = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)

def is_zero(e):
    return sp.simplify(e) == 0

print("=" * 110)
print("CQ4_unimodular_tie -- a0 tied to the Henneaux-Teitelboim multiplier; kappa = 1/2 FITTED; not theory closed")
print("=" * 110)

t, x, y, z = X = sp.symbols('t x y z', real=True)
Lam = sp.Function('Lam')(*X)                          # the multiplier field Lambda(x)
Bs = [sp.Function(f'B{m}')(*X) for m in range(4)]     # vector density B^mu(x)
sg = sp.Function('sqrtg')(*X)                         # sqrt(-g); the metric is varied separately (E5)
divB = sum(sp.diff(Bs[m], X[m]) for m in range(4))

# ---------------------------------------------------------------- K0: Henneaux-Teitelboim alone
print("\nK0 [known answer] HT sector alone: L = sqrt(-g)(-2 Lambda) + 2 Lambda d_mu B^mu")
L_HT = -2*sg*Lam + 2*Lam*divB
eB0 = [sp.euler_equations(L_HT, [Bs[m]], X)[0].lhs for m in range(4)]
eL0 = sp.euler_equations(L_HT, [Lam], X)[0].lhs
check("K0a  B^mu equation is -2 d_mu Lambda = 0 (Lambda constant)", all(is_zero(eB0[m] + 2*sp.diff(Lam, X[m])) for m in range(4)))
check("K0b  Lambda equation is d_mu B^mu = sqrt(-g) (unimodular volume)", is_zero(eL0 - (-2*sg + 2*divB)))

# ---------------------------------------------------------------- E1-E2: with the tie, generic J(Y, Lambda)
print("\nE1-E2  with the tie: L = -2 sqrt(-g) J(Y, Lambda) + 2 Lambda d_mu B^mu, J generic")
Yf = sp.Function('Y')(*X)
Jf = sp.Function('J')
L_tie = -2*sg*Jf(Yf, Lam) + 2*Lam*divB
eB = [sp.euler_equations(L_tie, [Bs[m]], X)[0].lhs for m in range(4)]
eL = sp.euler_equations(L_tie, [Lam], X)[0].lhs
E1 = all(is_zero(eB[m] + 2*sp.diff(Lam, X[m])) for m in range(4))
check("E1   B^mu equation unchanged by the tie: d_mu Lambda = 0 exactly, whatever J is", E1)
check("E2   Lambda equation: d_mu B^mu = sqrt(-g) dJ/dLambda|_Y  (fixes B only)", is_zero(eL - (-2*sg*sp.diff(Jf(Yf, Lam), Lam) + 2*divB)))

# ---------------------------------------------------------------- E3: dJ/dLambda, generic and v3s
print("\nE3   dJ/dLambda at fixed Y")
Ys, Ls, al, Us = sp.symbols('Y Lambda alpha U', positive=True)
jf = sp.Function('j')
Jgen = Ls*jf(Ys/Ls)
check("E3a  form G: J = Lambda j(Y/Lambda) gives dJ/dLambda = j - y j'(y), y = Y/Lambda",
      is_zero(sp.diff(Jgen, Ls) - (jf(Ys/Ls) - Ys*sp.diff(jf(Ys/Ls), Ys))))
u = sp.sqrt(Ys/(al**2*Ls))
Jv = Ls - 2*al**2*Ls*(u - sp.log(1 + u))
hU = 2*(Us - sp.log(1 + Us)) - Us**2/(1 + Us)
toU = {Ys: Us**2*al**2*Ls}
check("E3b  form U: dJ/dLambda = 1 - alpha^2 h(u), h(u) = 2(u - ln(1+u)) - u^2/(1+u)",
      is_zero((sp.diff(Jv, Ls) - 1).subs(toU) + al**2*hU))
ser = sp.series(hU, Us, 0, 5).removeO()
check("E3c  h(u) = u^3/3 - u^4/2 + ... near u = 0", is_zero(ser - (Us**3/3 - Us**4/2)))
hnum = sp.lambdify(Us, hU, 'math')
grid = [10**(k/10) for k in range(-30, 31)]
check("E3d  h(u) > 0 for u in [1e-3, 1e3] (61 log points)", all(hnum(v) > 0 for v in grid), f"min h = {min(hnum(v) for v in grid):.3e} at u = 1e-3")

# ---------------------------------------------------------------- K1: v3s's law and kappa = 1/2
print("\nK1 [known answer] v3s's J: 1 + J' = u/(1+u) (simple-mu static law), a0 = c^2 alpha sqrt(Lambda)")
check("K1a  1 + dJ/dY = u/(1+u)", is_zero((1 + sp.diff(Jv, Ys) - u/(1 + u)).subs(toU)))
check("K1b  J(0; Lambda) = Lambda (the vacuum value the multiplier carries)", is_zero(sp.limit(Jv, Ys, 0) - Ls))

# ---------------------------------------------------------------- E4: parent equations at constant Lambda
print("\nE4   at Lambda = const the remaining field equations are the parent's (stand-in field phi, Y = (d phi)^2)")
phi = sp.Function('phi')(*X)
L0 = sp.Symbol('Lambda0', positive=True)
Yphi = -sp.diff(phi, t)**2 + sum(sp.diff(phi, v)**2 for v in (x, y, z))
L_field = -2*sg*Jv.subs({Ys: Yphi, Ls: Lam}) + 2*Lam*divB
L_const = -2*sg*Jv.subs({Ys: Yphi, Ls: L0})
e_field = sp.euler_equations(L_field, [phi], X)[0].lhs
e_const = sp.euler_equations(L_const, [phi], X)[0].lhs
diff_e = (e_field.subs(Lam, L0).doit() - e_const)
phi_c = x + y/2 + z/3 + t*x/10
sg_c = 1 + x**2/10
alv = 1/sp.sqrt(32*sp.pi)
val = diff_e.subs({phi: phi_c, sg: sg_c}).doit().subs({t: sp.Rational(1, 3), x: sp.Rational(1, 2), y: sp.Rational(1, 5), z: sp.Rational(1, 7), al: alv, L0: 2})
val = abs(sp.N(val, 30))
check("E4   EL_phi[Lambda(x)] at Lambda(x) = Lambda0 minus EL_phi[Lambda0] = 0 (test configuration, 30 digits)", val < 1e-25, f"|difference| = {float(val):.1e}")
check("E4b  the 2 Lambda d_mu B^mu term contains no metric (zero stress tensor)", not (2*Lam*divB).has(sg))

# ---------------------------------------------------------------- E5: the cosmological term (Jacobi's formula)
print("\nE5   d det(g)/d g_ij = det(g) (g^-1)_ji, so -2 sqrt(-g) J(0) gives J(0) g_mu_nu = Lambda g_mu_nu in the metric equation")
M = sp.Matrix(4, 4, sp.symbols('m0:16'))
D, adj = M.det(), M.adjugate()
check("E5   Jacobi's formula on a general 4x4 matrix", all(sp.expand(sp.diff(D, M[i, j]) - adj[j, i]) == 0 for i in range(4) for j in range(4)))

# ---------------------------------------------------------------- S, G5a, G5b, G5c: scale relation
print("\nS / G5   scale relation: kappa^2 = a0^2 / (c^2 G rho_Lambda,obs),  rho_Lambda,obs = Lambda_obs c^2/(8 pi G),  Lambda_obs = Lambda + Lambda_v")
c_, G_, Lm, Lv, Lobs = sp.symbols('c G Lambda_m Lambda_v Lambda_obs', positive=True)
a0 = al*c_**2*sp.sqrt(Lm)
kappa2 = sp.simplify((a0**2/(c_**2*G_*Lobs*c_**2/(8*sp.pi*G_))).subs(Lm, Lobs - Lv))
check("S1   kappa^2 = 8 pi alpha^2 (1 - Lambda_v/Lambda_obs) = 8 pi alpha^2 (1 - rho_v/rho_Lambda,obs)", is_zero(kappa2 - 8*sp.pi*al**2*(1 - Lv/Lobs)), f"kappa^2 = {kappa2}")
check("S2   v3s value alpha^2 = 1/(32 pi), rho_v = 0 gives kappa = 1/2", is_zero(sp.sqrt(kappa2.subs({al: alv, Lv: 0})) - sp.Rational(1, 2)))
S_ok = E1 and not BAD
gate("S    static weak-field limit = the parent law with a0 = alpha c^2 sqrt(Lambda); kappa^2 in closed form", S_ok)
a_, b_, d_ = sp.symbols('a b d')
# [G]^a [c]^b [Lambda]^d = m s^-2 ; dimensions (mass, length, time): G = (-1, 3, -2), c = (0, 1, -1), Lambda = (0, -2, 0)
sol = sp.solve([-a_, 3*a_ + b_ - 2*d_ - 1, -2*a_ - b_ + 2], [a_, b_, d_], dict=True)
G5a = sol == [{a_: 0, b_: 2, d_: sp.Rational(1, 2)}]
gate("G5a  form: the only acceleration built from G, c, Lambda is (number) x c^2 sqrt(Lambda), so a0 ~ c sqrt(G rho)", G5a, f"exponents {sol}")
dk_da = sp.diff(kappa2, al)
dJ_dal = sp.simplify(sp.diff(Jv, al).subs(toU) + 2*al*Ls*hU)
check("G5b' alpha promoted to a field: dJ/dalpha = -2 alpha Lambda h(u), zero only at u = 0 (kills the MOND sector)", dJ_dal == 0)
gate("G5b  number: kappa fixed by the action (no free constant left)", not (dk_da != 0), f"d kappa^2/d alpha = {sp.simplify(dk_da)}; alpha has no field equation")
dk_dv = sp.simplify(sp.diff(kappa2, Lv))
gate("G5c  tie to the observed vacuum: d kappa^2 / d rho_v = 0 at fixed rho_Lambda,obs", dk_dv == 0, f"d kappa^2/d Lambda_v = {dk_dv}")

# ---------------------------------------------------------------- C1: shift symmetry and renormalisation
print("\nC1   renormalisation: HT + vacuum is invariant under Lambda -> Lambda + delta, Lambda_v -> Lambda_v - delta (up to a total derivative)")
sgs, dvs, dl = sp.symbols('sqrtg divB delta', positive=True)
L_GR = lambda Lmult, Lvac: -2*sgs*Lmult - 2*sgs*Lvac + 2*Lmult*dvs
check("C1a  without the tie: Delta L = 2 delta d_mu B^mu (a total derivative), metric equations unchanged",
      is_zero(L_GR(Ls + dl, Lv - dl) - L_GR(Ls, Lv) - 2*dl*dvs))
L_T = lambda Lmult, Lvac: -2*sgs*Jv.subs(Ls, Lmult) - 2*sgs*Lvac + 2*Lmult*dvs
brk = sp.series((L_T(Ls + dl, Lv - dl) - L_T(Ls, Lv) - 2*dl*dvs).subs(toU), dl, 0, 2).removeO()
brk_expect = 2*sgs*dl*al**2*hU
check("C1b  with the tie: Delta L - total derivative = 2 sqrt(-g) delta alpha^2 h(u) + O(delta^2), nonzero for u > 0",
      is_zero(sp.simplify(brk - brk_expect.subs(toU))))
dlogk = 0.099                                           # KC1: current primary measurement, +/-0.099 dex in kappa
r_lo, r_hi = 1 - 10**(2*dlogk), 1 - 10**(-2*dlogk)
print(f"    window: kappa^2/kappa0^2 = 1 - r, r = rho_v/rho_Lambda,obs;  |log kappa - log kappa0| <= {dlogk} dex needs {r_lo:.3f} <= r <= {r_hi:.3f}")
Gn, cn, hbar, mec2 = 6.67430e-11, 2.99792458e8, 1.054571817e-34, 8.1871057769e-14
m4 = mec2**4/(hbar*cn)**3                               # (m_e c^2)^4/(hbar c)^3, J/m^3
rho_e = 6/(64*math.pi**2)*m4                            # MS-bar one-loop, Dirac fermion, mu = m_e  [PROVISIONAL formula]
drho = m4/(8*math.pi**2)                                # d rho_e / d ln mu                             [PROVISIONAL formula]
print(f"    electron one-loop vacuum energy (MS-bar, mu = m_e): {rho_e:.3e} J/m^3;  d/d ln(mu): {drho:.3e} J/m^3")
ratios = {}
for f, a0n in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
    uL = 4*a0n**2/Gn                                    # rho_Lambda c^2 = 4 a0^2/G at kappa = 1/2 (FITTED); size illustration only
    ratios[f] = (rho_e/uL, drho/uL)
    print(f"    {f:9s}: rho_Lambda c^2 = {uL:.4e} J/m^3;  rho_e/rho_Lambda = {rho_e/uL:.2e};  per e-fold of mu: {drho/uL:.2e}")
C1_ok = is_zero(brk) and dk_dv == 0                     # absorbed only if the shift is a symmetry and kappa^2 ignores rho_v
gate("C1   the tie survives a vacuum-energy shift (absorbed with no change in kappa)", C1_ok,
     f"kappa^2 moves by -8 pi alpha^2 delta rho_v/rho_Lambda; window |r| <~ {r_hi:.2f}-{-r_lo:.2f} vs electron loop "
     f"{ratios['canonical'][0]:.1e} (canonical), {ratios['alt'][0]:.1e} (alt)")

# ---------------------------------------------------------------- MUTATE: k04's flux tie
print("\nMUTATE  tie a0 to the four-form flux q (k04) instead: the conserved quantity is dF/dq, which depends on Y")
q, Zc, be, Yq = sp.symbols('q Z beta Y_q', positive=True)
uq = sp.sqrt(Yq)/(be*q)
F = -Zc*q**2/2 + 2*be**2*q**2*(uq - sp.log(1 + uq))    # -P(q) - J_MOND(Y; a_geo = beta q)
FqY, Fqq = sp.diff(F, q, Yq), sp.diff(F, q, 2)
pt = {Zc: 8, be: 1, q: 1, Yq: 1}                        # k04's Z = 8 beta^2, u = 1
dq_dY = float(sp.N((-FqY/Fqq).subs(pt)))
fb_mut = abs(dq_dY) > 1e-6
print(f"    MUTATE: dq/dY at u = 1, Z = 8 beta^2: {dq_dY:+.4f} (q, hence a0, follows the local MOND invariant)")
fb_mult = sp.diff(2*Ls, Ys) == 0 and E1
print(f"    multiplier: conserved quantity 2 Lambda, d(2 Lambda)/dY = 0; d_mu Lambda = 0 exactly (E1)")
check("MUTATE  feedback found for the flux tie and exactly none for the multiplier tie", fb_mut and fb_mult)

# ---------------------------------------------------------------- H1-H3: health
print("\nH    health of the (Lambda, B) sector")
vel = [sp.diff(Lam, t)] + [sp.diff(Bs[m], t) for m in range(4)]
Hm = sp.Matrix(5, 5, lambda i, j: sp.diff(L_tie, vel[i], vel[j]))
check("H1a  velocity Hessian of (Lambda, B^mu) is zero: no kinetic term, so no sign to get wrong", Hm == sp.zeros(5, 5))
check("H1b  momentum conjugate to B^0 is 2 Lambda (a first-order pair; one global mode)", is_zero(sp.diff(L_tie, vel[1]) - 2*Lam))
w = {}
for i in range(4):
    for j in range(i + 1, 4):
        w[(i, j)] = sp.Function(f'w{i}{j}')(*X)
om = [[(w[(i, j)] if i < j else (-w[(j, i)] if i > j else 0)) for j in range(4)] for i in range(4)]
dBg = [sum(sp.diff(om[m][n], X[n]) for n in range(4)) for m in range(4)]
check("H1c  gauge symmetry B^mu -> B^mu + d_nu omega^[mu nu]: d_mu B^mu unchanged (3 of 4 components are gauge)", is_zero(sum(sp.diff(dBg[m], X[m]) for m in range(4))))
H1 = not any(n.startswith('H1') for n in BAD)
gate("H1   no ghost: the tie adds no kinetic term; the parent's health is inherited (v3s: V3W W4, V3X W4c)", H1)
gate("H2   no new long-range force: d_mu Lambda = 0 on shell, so delta Lambda = 0 locally (only the global zero mode)", E1)
gate("H3   c_T = c: the added terms carry no metric derivative; tensor sector = the parent's (v3s, beta = 0: c_T = c)",
     not (2*Lam*divB).has(sg) and E1)

# ---------------------------------------------------------------- C2: time dependence (reported)
print("\nC2   time dependence (reported, not graded): d_mu Lambda = 0, so the tied vacuum has w = -1 exactly and")
print("     a0(z)/a0(0) = 1 at every z, whatever any other dark-energy component does.")

# ---------------------------------------------------------------- label
print("\n" + "-" * 110)
if BAD:
    label = "NOT GRADED (script check failed)"
elif not (GATES["H1   no ghost: the tie adds no kinetic term; the parent's health is inherited (v3s: V3W W4, V3X W4c)"] and GATES[[k for k in GATES if k.startswith("H2")][0]] and GATES[[k for k in GATES if k.startswith("H3")][0]]):
    label = "UNHEALTHY"
elif not GATES[[k for k in GATES if k.startswith("S ")][0]]:
    label = "NO GO"
elif all(GATES[[k for k in GATES if k.startswith(p)][0]] for p in ("G5a", "G5b", "G5c", "C1 ")):
    label = "TIE DERIVED (healthy)"
else:
    label = "TIE BY HAND (no gain over AX1)"
print("gates: " + ", ".join(f"{k.split()[0]} {'PASS' if v else 'FAIL'}" for k, v in GATES.items()))
print(f"script checks: {'all OK' if not BAD else 'BAD: ' + '; '.join(BAD)}")
print(f"RESULT: {label}")
print("kappa = 1/2 FITTED; not theory closed.")
sys.exit(1 if BAD else 0)
