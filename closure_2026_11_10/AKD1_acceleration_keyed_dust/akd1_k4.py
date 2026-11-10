"""AKD1 K4: scalar quadratic action around flat FRW in unitary gauge, gravity + clock + Lambda, with
F(Q, Y) = F0 + FQ dQ + FQQ dQ^2/2 + FY Y (Y = gamma^ij d_i ln N d_j ln N is second order; FY = candidate + law piece).
TK1's construction (tk1_k4.py, read only) with theta replaced by Y. Criteria d88d310eb1.
Env AKD1_MUTATE = MU3 drops the FY term. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, json, time
import sympy as sp
MUT = os.environ.get("AKD1_MUTATE", "")
HERE = os.path.dirname(os.path.abspath(__file__))
out = {"mutate": MUT}
T0 = time.time()
def say(*a):
    print(*a, flush=True)
t, x = sp.symbols("t x", real=True)
Kg = sp.symbols("K", positive=True)
eps, kk = sp.symbols("epsilon k", positive=True)
af = sp.Function("a")(t); N0 = sp.Function("N0")(t)
Z = sp.Function("Z")(t); Al = sp.Function("Al")(t); Ps = sp.Function("Ps")(t)
Lam = sp.symbols("Lambda")
FQs, FQQs, FYs, F0s = [sp.Function(nm)(t) for nm in ("FQ", "FQQ", "FY", "F0")]
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
def dsp(f, i):
    return sp.diff(f, x) if i == 0 else 0
DN = [[dsp(Ni[j], i) - sum(Gam(kx, i, j)*Ni[kx] for kx in range(3)) for j in range(3)] for i in range(3)]
Kll = [[((sp.diff(gam_ll, t) if i == j else 0) - DN[i][j] - DN[j][i])/(2*Nfull) for j in range(3)] for i in range(3)]
Ktr = sum(gam_uu*Kll[i][i] for i in range(3))
S4 = sum(gam_uu**2*Kll[i][j]**2 for i in range(3) for j in range(3))
R3 = -(4*sp.diff(zeta, x, 2) + 2*sp.diff(zeta, x)**2)/(af**2*e2z)
sqrtg = af**3*sp.exp(3*zeta)
Qb = 1/N0
dQ = 1/Nfull - Qb
Yf = gam_uu*sp.diff(sp.log(Nfull), x)**2
Fexp = F0s + FQs*dQ + FQQs*dQ**2/2 + (0 if MUT == "MU3" else FYs*Yf)
L4 = Nfull*sqrtg*((S4 - Ktr**2 + R3)/(4*Kg) - Lam/(2*Kg) + Fexp)
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
say("== K4: L2 built, %d terms, %.1f s" % (len(L2.args), time.time() - T0))
Zd = sp.diff(Z, t)
for f in (Al, Ps):
    assert not L2.has(sp.diff(f, t)), "auxiliary field has a velocity"
sol = sp.solve([sp.diff(L2, Al), sp.diff(L2, Ps)], [Al, Ps], dict=True)[0]
say("  momentum/Hamiltonian constraints: alpha =", sp.simplify(sol[Al]))
out["K4_alpha_solution"] = str(sp.simplify(sol[Al]))
Lz = sp.expand(sp.simplify(L2.subs(sol)))
Az = sp.factor(sp.simplify(Lz.coeff(Zd, 2)))
Bz = sp.simplify((Lz - Az*Zd**2).coeff(Zd, 1).coeff(Z, 1))
Cz = sp.simplify((Lz - Az*Zd**2 - Bz*Z*Zd).coeff(Z, 2))
grad = sp.simplify(-Cz + sp.diff(Bz, t)/2)
say("  A_z =", Az)
say("  grad =", grad)
out["K4_Az"] = str(Az); out["K4_grad"] = str(grad)
out["K4_Az_has_k"] = bool(Az.has(kk))
gn, gd = sp.fraction(sp.together(grad))
out["K4_grad_den_has_k"] = bool(gd.has(kk))
say("  A_z depends on k:", out["K4_Az_has_k"], "; grad denominator has k:", out["K4_grad_den_has_k"])
# KA2: FY = 0 -> TK1's closed form at F_th = F_Qth = F_thth = 0: A_z = FQQ a^5 / (4 N0 a-dot^2)
ad = sp.diff(af, t)
ka2 = sp.simplify(Az.subs(FYs, 0) - FQQs*af**5/(4*N0*ad**2))
say("  KA2 (FY = 0): A_z - FQQ a^5/(4 N0 a-dot^2) =", ka2)
out["KA2_residual"] = str(ka2)
# KA4 (K4 side): A_z(k)/A_z(0) against the decoupling inertia ratio 1 + 2 FY k_phys^2 / (FQQ Q0^2), k_phys = k/a, Q0 = 1/N0
ratio = sp.simplify(Az/Az.subs(kk, 0))
ka4 = sp.simplify(ratio - (1 + 2*FYs*(kk/af)**2/(FQQs/N0**2)))
say("  KA4 (K4 side): A_z(k)/A_z(0) - [1 + 2 FY (k/a)^2 / (FQQ Q0^2)] =", ka4)
out["KA4_K4_ratio"] = str(ratio); out["KA4_residual"] = str(ka4)
# monotonicity of A_z in FY (printed, not assumed): dA_z/dFY
dAdFY = sp.simplify(sp.diff(Az, FYs) if Az.has(FYs) else sp.Integer(0))
say("  dA_z/dFY =", dAdFY)
out["K4_dAz_dFY"] = str(dAdFY)
# symbols for the evaluator
fn = {}
for f_ in (af, N0, FQs, FQQs, FYs, F0s):
    nm = str(f_.func)
    fn[sp.Derivative(f_, (t, 2))] = sp.Symbol(nm + "_dd")
    fn[sp.Derivative(f_, t)] = sp.Symbol(nm + "_d")
def tosym(e):
    e = e.subs({k_: v_ for k_, v_ in fn.items() if k_.derivative_count == 2})
    e = e.subs({k_: v_ for k_, v_ in fn.items()})
    return e.subs({f_: sp.Symbol(str(f_.func)) for f_ in (af, N0, FQs, FQQs, FYs, F0s)})
out["K4_sym_Az"] = sp.srepr(tosym(Az)); out["K4_sym_grad"] = sp.srepr(tosym(grad))
json.dump(out, open(os.path.join(HERE, "akd1_k4%s.json" % ("_MUTATE_" + MUT if MUT else "")), "w"), indent=1, default=str)
say("done %.1f s" % (time.time() - T0))
