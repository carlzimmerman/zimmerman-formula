"""TK1 K4 (split from tk1_a1.py so it runs alongside K1): scalar quadratic action around flat FRW in unitary gauge.
Criteria 98f2ab2b6e. Env TK1_MUTATE = MU3 drops F_thth. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, time
import sympy as sp
MUT = os.environ.get("TK1_MUTATE", "")
out = {"mutate": MUT}
T0 = time.time()
def say(*a):
    print(*a, flush=True)
t, x = sp.symbols("t x", real=True)
Kg = sp.symbols("K", positive=True)
# ---------------------------------------------------------------- K4 quadratic action
say("== K4: scalar quadratic action around flat FRW (unitary gauge)")
eps, kk = sp.symbols("epsilon k", positive=True)
af = sp.Function("a")(t); N0 = sp.Function("N0")(t)
Z = sp.Function("Z")(t); Al = sp.Function("Al")(t); Ps = sp.Function("Ps")(t)
Lam = sp.symbols("Lambda")
FQs, Fths, FQQs, FQths, Fththss, F0s = [sp.Function(nm)(t) for nm in ("FQ", "Fth", "FQQ", "FQth", "Fthth", "F0")]
c_, s_ = sp.cos(kk*x), sp.sin(kk*x)
zeta = eps*Z*c_; alpha = eps*Al*c_; psi = eps*Ps*c_/kk**2
Nfull = N0*(1 + alpha)
Ni = [sp.diff(psi, x), 0, 0]
e2z = sp.exp(2*zeta)
gam_ll = af**2*e2z
gam_uu = 1/(af**2*e2z)
dz = [sp.diff(zeta, x), 0, 0]
def Gam(kidx, i, j):
    return (1 if kidx == i else 0)*dz[j] + (1 if kidx == j else 0)*dz[i] - (1 if i == j else 0)*dz[kidx]
Xc = [x, None, None]
def dsp(f, i):
    return sp.diff(f, x) if i == 0 else 0
DN = [[dsp(Ni[j], i) - sum(Gam(kx, i, j)*Ni[kx] for kx in range(3)) for j in range(3)] for i in range(3)]
Kll = [[((sp.diff(gam_ll, t) if i == j else 0) - DN[i][j] - DN[j][i])/(2*Nfull) for j in range(3)] for i in range(3)]
Ktr4 = sum(gam_uu*Kll[i][i] for i in range(3))
S4 = sum(gam_uu**2*Kll[i][j]**2 for i in range(3) for j in range(3))
R3 = -(4*sp.diff(zeta, x, 2) + 2*sp.diff(zeta, x)**2)/(af**2*e2z)
sqrtg = af**3*sp.exp(3*zeta)
Qb = 1/N0
thb = 3*sp.diff(af, t)/(N0*af)
dQ = 1/Nfull - Qb
dth = Ktr4 - thb
Fexp = F0s + FQs*dQ + Fths*dth + FQQs*dQ**2/2 + FQths*dQ*dth + (0 if MUT == "MU3" else Fththss*dth**2/2)
L4 = Nfull*sqrtg*((S4 - Ktr4**2 + R3)/(4*Kg) - Lam/(2*Kg) + Fexp)
L2raw = sp.diff(L4, eps, 2).subs(eps, 0)/2
Cs, Ss = sp.symbols("Cs Ss")
L2raw = sp.expand(L2raw.subs({sp.cos(kk*x): Cs, sp.sin(kk*x): Ss}))
pol = sp.Poly(L2raw, Cs, Ss)
avg = {(2, 0): sp.Rational(1, 2), (0, 2): sp.Rational(1, 2)}
L2 = 0
for mon, cf in pol.terms():
    L2 += cf*avg.get(mon, 0)
    if mon not in avg and cf != 0 and mon != (1, 1):
        raise SystemExit("unexpected trig monomial %s" % (mon,))
L2 = sp.expand(L2)
say("  L2 built, %d terms, %.1f s" % (len(L2.args), time.time() - T0))
# auxiliary fields
Zd = sp.diff(Z, t)
for f in (Al, Ps):
    assert not L2.has(sp.diff(f, t)), "auxiliary field has a velocity"
sol = sp.solve([sp.diff(L2, Al), sp.diff(L2, Ps)], [Al, Ps], dict=True)[0]
Lz = sp.expand(sp.simplify(L2.subs(sol)))
Az = sp.simplify(Lz.coeff(Zd, 2))
Bz = sp.simplify((Lz - Az*Zd**2).coeff(Zd, 1).coeff(Z, 1))
Cz = sp.simplify((Lz - Az*Zd**2 - Bz*Z*Zd).coeff(Z, 2))
grad = sp.simplify(-Cz + sp.diff(Bz, t)/2)   # L = A Zd^2 - grad Z^2
say("  A_z =", Az)
out["K4_Az"] = str(Az); out["K4_Bz"] = str(Bz); out["K4_Cz"] = str(Cz); out["K4_grad"] = str(grad)
# high-k structure: A_z is checked for k-dependence; grad = g4 k^4 + g2 k^2 + g0 (exact polynomial in k?)
out["K4_Az_has_k"] = bool(Az.has(kk))
say("  A_z depends on k:", out["K4_Az_has_k"])
gradn = sp.together(grad)
num, den = sp.fraction(gradn)
say("  grad denominator has k:", den.has(kk))
pg = sp.Poly(sp.expand(num), kk)
coeffs = {m[0]: sp.simplify(c/den) for m, c in pg.terms()}
say("  powers of k in grad:", sorted(coeffs))
g4 = coeffs.get(4, sp.Integer(0)); g2 = coeffs.get(2, sp.Integer(0)); g0 = coeffs.get(0, sp.Integer(0))
say("  g4 =", g4)
# replace functions of t by symbols for the evaluator
fn = {}
for f_ in (af, N0, FQs, Fths, FQQs, FQths, Fththss, F0s):
    nm = str(f_.func)
    fn[sp.Derivative(f_, (t, 2))] = sp.Symbol(nm + "_dd")
    fn[sp.Derivative(f_, t)] = sp.Symbol(nm + "_d")
for f_ in (af, N0, FQs, Fths, FQQs, FQths, Fththss, F0s):
    fn[f_] = sp.Symbol(str(f_.func))
def tosym(e):
    e = e.subs({k_: v_ for k_, v_ in fn.items() if isinstance(k_, sp.Derivative) and k_.derivative_count == 2})
    e = e.subs({k_: v_ for k_, v_ in fn.items() if isinstance(k_, sp.Derivative)})
    return e.subs({k_: v_ for k_, v_ in fn.items() if not isinstance(k_, sp.Derivative)})
for nm_, e_ in (("Az", Az), ("g4", g4), ("g2", g2), ("g0", g0)):
    out["K4_sym_" + nm_] = sp.srepr(tosym(e_))
# KA-K4: numerator of A_z at F_Qth = 0 is 3 K F_QQ (F_thth - 1/(3K)) (K2c's trace eigenvalue, independent code)
nA, dA = sp.fraction(sp.together(Az))
chk = sp.simplify((nA.subs(FQths, 0)) / (3*Kg*FQQs*(Fththss - 1/(3*Kg))) )
say("  KA-K4: numerator(A_z)|_{F_Qth=0} / [3K F_QQ (F_thth - 1/3K)] =", chk)
out["KA_K4_ratio"] = str(chk)
# KA5 symbolic part: M_2 constant (F_thth = F_Qth = 0): g4 = 0
out["KA5_g4_zero"] = str(sp.simplify(g4.subs({Fththss: 0, FQths: 0})))
say("  KA5: g4 at F_thth = F_Qth = 0:", out["KA5_g4_zero"])
with open(os.path.join(os.path.dirname(__file__), "tk1_k4%s.json" % ("_MUTATE_" + MUT if MUT else "")), "w") as fh:
    json.dump(out, fh, indent=1, default=str)
say("done %.1f s" % (time.time() - T0))
