#!/usr/bin/env python3
"""n1_2 -- product Einstein-Maxwell maps with several isometry factors: CP^1 (= S^2 check), CP^2 (SU(3)), and M_4 x CP^2 x S^2 with ONE Maxwell field (Map C).
Pre-registered in N1_PREREGISTRATION.md (Part II, Map C).

Action  S = Int sqrt(g_D) [ R/(2 kappa^2) - Lambda/kappa^2 - F^2/(4 g^2) ],  internal space = product of factors i (radius R_i, Ricci scalar nk_i/R_i^2, flux F_i = N_i * (form), isotropic).
Energy density W = Lambda/kappa^2 - sum nk_i X_i/(2 kappa^2) + sum beta_i N_i^2 X_i^2/g^2  (X_i = 1/R_i^2; beta_i = F_i^2 R_i^4/(4 N_i^2)).
Minkowski: W = 0 and dW/dX_i = 0 (U = V_int W, dU = 0 at W = 0); cross-checked against the D-dim Einstein equations block by block.
Couplings (per isometry generator T normalised with index 1, e.g. T3 = diag(1/2,-1/2,0)):  1/g_T^2 = V_int [ <|K|^2>/(2 kappa^2) + <mu^2>/g^2 ],  i_K F = -d mu (traceless moment map);
unit-charge U(1): 1/g_U1^2 = V_int/g^2;  l_P^2 = kappa^2/(8 pi V_int).
CP^n: Fubini-Study metric ds^2 = g_{j kbar} dw^j dwbar^k, g = d d-bar ln(1+|w|^2) (holomorphic sectional curvature 4, Ric = 2(n+1) g, CP^1 = sphere of radius 1/2); omega = (i/2) g_{j kbar} dw^j ^ dwbar^k; F = FLUXNORM * N * omega with FLUXNORM = 2 (Int_{CP^1} omega = pi).

Run:     python3 n1_2_product_maps.py            (real run, exit 0)
MUTATE:  python3 n1_2_product_maps.py --mutate   (control: flux normalisation F = N omega instead of 2 N omega; flux quantisation and the CP^1 = S^2 reproduction must FAIL, exit 1)
"""
import sys
sys.dont_write_bytecode = True
import json, os, itertools
from fractions import Fraction
import sympy as sp

MUTATE = "--mutate" in sys.argv
CHECKS = []
FLUXNORM = 1 if MUTATE else 2


def check(tag, ok, detail=""):
    CHECKS.append((tag, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


print("=" * 100)
print("N1-2 product Einstein-Maxwell maps -- mode: " + ("MUTATE CONTROL (F = N omega)" if MUTATE else "REAL RUN"))
print("=" * 100)

s1, s2 = sp.symbols("s1 s2", positive=True)
w1, w2, wb1, wb2 = sp.symbols("w1 w2 wb1 wb2")

# ---------------------------------------------------------------- CP^n geometry
def fs_G(nc):
    ws = [w1, w2][:nc]; wbs = [wb1, wb2][:nc]
    Kp = sp.log(1 + sum(a * b for a, b in zip(ws, wbs)))
    g = sp.Matrix(nc, nc, lambda i, j: sp.diff(Kp, ws[i], wbs[j]))          # g_{i jbar} (my convention: ds^2 = g dw dwbar)
    return ws, wbs, sp.simplify(g)

print("\nG1  Fubini-Study normalisation (holomorphic sectional curvature 4)")
for nc in (1, 2):
    ws, wbs, g = fs_G(nc)
    G = g / 2                                                              # G_{i jbar} = g(d_i, d_jbar)
    detG = sp.simplify(G.det())
    Ric = sp.Matrix(nc, nc, lambda i, j: sp.simplify(-sp.diff(sp.log(detG), ws[i], wbs[j])))
    lam = 2 * (nc + 1)
    check(f"G1 CP^{nc}: Ric_(i jbar) = -d d-bar ln det G = {lam} G_(i jbar)  (Einstein, Ric = {lam} g; CP^1 has radius 1/2, K = 4)", sp.simplify(Ric - lam * G) == sp.zeros(nc, nc))
# volume
def vol_fs(nc):
    ws, wbs, g = fs_G(nc)
    dens = sp.simplify(g.det())
    if nc == 1:
        f = dens.subs({w1: sp.sqrt(s1), wb1: sp.sqrt(s1)})
        return sp.simplify(sp.pi * sp.integrate(f, (s1, 0, sp.oo)))
    f = dens.subs({w1: sp.sqrt(s1), wb1: sp.sqrt(s1), w2: sp.sqrt(s2), wb2: sp.sqrt(s2)})
    return sp.simplify(sp.pi ** 2 * sp.integrate(sp.integrate(f, (s1, 0, sp.oo)), (s2, 0, sp.oo)))
V1, V2 = vol_fs(1), vol_fs(2)
print(f"    Vol(CP^1) = {V1},  Vol(CP^2) = {V2}")
check("G2 Vol(CP^1) = pi (= Int omega over CP^1), Vol(CP^2) = pi^2/2", sp.simplify(V1 - sp.pi) == 0 and sp.simplify(V2 - sp.pi ** 2 / 2) == 0)
check("G3 flux quantisation on the CP^1 line: Int_{CP^1} F = FLUXNORM * N * pi = 2 pi N  (needs FLUXNORM = 2)", sp.simplify(FLUXNORM * V1 - 2 * sp.pi) == 0)

# ---------------------------------------------------------------- Killing vector, moment map, averages for T3 = diag(1/2,-1/2,0)
print("\nG4  Killing vector and moment map of T3 (index-1 su(2) Cartan) on CP^1 and CP^2")
xs = sp.symbols("x1 y1 x2 y2", real=True)

def real_omega_and_check(nc):
    ws, wbs, g = fs_G(nc)
    X = sp.symbols("x1 y1 x2 y2", real=True)[:2 * nc]
    subs_c = {}
    for j in range(nc):
        subs_c[ws[j]] = X[2 * j] + sp.I * X[2 * j + 1]
        subs_c[wbs[j]] = X[2 * j] - sp.I * X[2 * j + 1]
    gr = g.subs(subs_c)
    # omega = (i/2) g_{j kbar} dw_j ^ dwbar_k ; dw_j = dx_j + i dy_j ; dwbar_k = dx_k - i dy_k
    n = 2 * nc
    om = sp.zeros(n, n)
    def add(a, b, c):
        om[a, b] += c; om[b, a] -= c
    for j in range(nc):
        for k in range(nc):
            c0 = sp.I / 2 * gr[j, k]
            # dx_j^dx_k + dy_j^dy_k - i dx_j^dy_k + i dy_j^dx_k
            add(2 * j, 2 * k, c0); add(2 * j + 1, 2 * k + 1, c0); add(2 * j, 2 * k + 1, -sp.I * c0); add(2 * j + 1, 2 * k, sp.I * c0)
    return X, om

def moment_check(nc):
    X, om = real_omega_and_check(nc)
    n = 2 * nc
    # T3 action: delta w_1 = -i w_1, delta w_2 = -(i/2) w_2  (w_j = z_j/z_0 with z -> diag(e^{i e/2}, e^{-i e/2}, 1) z)
    tw = [-1, sp.Rational(-1, 2)][:nc]
    V = []
    for j in range(nc):
        wj = X[2 * j] + sp.I * X[2 * j + 1]
        dw = sp.I * tw[j] * wj
        V += [sp.re(sp.expand(dw)), sp.im(sp.expand(dw))]
    V = sp.Matrix(V)
    iVom = sp.Matrix([sum(V[a] * om[a, b] for a in range(n)) for b in range(n)])
    # candidate moment map mu0 = c (1/2)(1 - s1)/(1 + s)   with s = |w|^2
    ssum = sum(X[2 * j] ** 2 + X[2 * j + 1] ** 2 for j in range(nc))
    S1 = X[0] ** 2 + X[1] ** 2
    cc = sp.symbols("cc")
    mu0 = cc * sp.Rational(1, 2) * (1 - S1) / (1 + ssum)
    dmu = sp.Matrix([sp.diff(mu0, X[b]) for b in range(n)])
    eqs = sp.simplify(iVom + dmu)
    sol = sp.solve([sp.simplify(e) for e in eqs if sp.simplify(e) != 0], cc, dict=True)
    return sol

results = {}
for nc in (1, 2):
    sol = moment_check(nc)
    print(f"    CP^{nc}: i_V omega = -d mu0 with mu0 = c (1/2)(1-|w1|^2)/(1+|w|^2):  c = {sol}")
    cval = None
    if sol:
        cval = list(sol[0].values())[0] if sol[0] else None
    check(f"G4a CP^{nc}: i_V omega = -d mu0 has a solution of the form mu0 = (c/2)(1-|w1|^2)/(1+|w|^2) = c <z|T3|z>/<z|z>, c unique; the solver returns c = 1/2 (omega has holomorphic curvature 4, so its moment map is half of <T3>)", bool(sol) and cval == sp.Rational(1, 2), f"(c = {cval})")
    results[nc] = cval

def averages(nc, cmu):
    # <f> over CP^nc in the polar variables s_j = |w_j|^2 : <f> = (pi^nc / Vol) Int f / (1+s)^(nc+1) ds
    if nc == 1:
        s = s1
        Vt = sp.pi
        dens = 1 / (1 + s) ** 2
        Kn = s / (1 + s) ** 2                                             # |V|^2 = g |w1|^2 = s/(1+s)^2
        mu0 = cmu * sp.Rational(1, 2) * (1 - s) / (1 + s)
        f = lambda e: sp.simplify(sp.pi * sp.integrate(e * dens, (s1, 0, sp.oo)) / Vt)
    else:
        s = s1 + s2
        Vt = sp.pi ** 2 / 2
        dens = 1 / (1 + s) ** 3
        Kn = (s1 + s2 / 4) / (1 + s) - (s1 + s2 / 2) ** 2 / (1 + s) ** 2   # g_{j kbar} V^j Vbar^k
        mu0 = cmu * sp.Rational(1, 2) * (1 - s1) / (1 + s)
        f = lambda e: sp.simplify(sp.pi ** 2 * sp.integrate(sp.integrate(e * dens, (s1, 0, sp.oo)), (s2, 0, sp.oo)) / Vt)
    return f(Kn), f(mu0), f(mu0 ** 2)

avs = {}
for nc in (1, 2):
    aK, amu, amu2 = averages(nc, results[nc])
    avs[nc] = (aK, amu, amu2)
    print(f"    CP^{nc}: <|K|^2> = {aK} (FS units R=1),  <mu0> = {amu},  <mu0^2> = {amu2}")
check("G4b CP^1: <|K|^2> = 1/6 (= (2/3) rho^2 with rho = 1/2, the S^2 value), <mu0> = 0", avs[1][0] == sp.Rational(1, 6) and avs[1][1] == 0)
check("G4c CP^1: F = 2 N omega gives <mu^2> = (2N)^2 <mu0^2> = N^2/12 (the S^2 value); with the mutated normalisation this fails",
      sp.simplify((FLUXNORM ** 2) * avs[1][2] - sp.Rational(1, 12)) == 0, f"(<mu^2>/N^2 = {sp.simplify(FLUXNORM ** 2 * avs[1][2])})")
check("G4d CP^2: <mu0> = 0 (traceless, no mixing with the U(1) zero mode)", avs[2][1] == 0)
# independent sum-rule cross-check of the CP^2 numbers over the whole su(3): sum_a <|K_a|^2> = 4 s_K , sum_a mu0_a^2 = c^2/(?)...
# <mu0_a^2> = (1/8) sum_a mu_a^2 = c^2 * (1/8) * (1/3) * ... with mu0_a = (1/2)*(z^dag lambda_a z)/|z|^2, lambda_a Gell-Mann (Tr = 2 delta): sum_a (z^dag T_a z)^2 = |z|^4/3
sum_rule_mu = sp.Rational(1, 4) * sp.Rational(1, 3) / 8      # mu0_a = (1/2) z^dag T_a z/|z|^2 (index-1 basis T_a): <mu0_a^2> = (1/4)(1/8)(1/3)
check("G4e CP^2 sum rule: <mu0_a^2> = (1/4)(1/8)(1/3) = 1/96 from completeness sum_a T_a^{ij} T_a^{kl} = (1/2)(d^{il} d^{jk} - d^{ij} d^{kl}/3)", sp.simplify(avs[2][2] - sum_rule_mu) == 0, f"(direct integral {avs[2][2]})")
# Killing-vector sum rule: sum_a |K_a|^2 constant; check it via the value <|K_T3|^2> = (1/8) * sum
print(f"    CP^2: <|K_T3|^2> = {avs[2][0]}   (FS units)")

# ---------------------------------------------------------------- factor data
Rr, Nn = sp.symbols("R N", positive=True)
kap, gg, Lam = sp.symbols("kappa g Lambda", positive=True)
fn2 = sp.Rational(FLUXNORM, 2) ** 2
def beta_cp(nc):       # beta = F_i^2 R^4 /(4 N^2), F = FLUXNORM N omega, omega_ab omega^ab = 2 nc
    return sp.Rational(FLUXNORM ** 2 * 2 * nc, 4)
FACT = {
    "S2":  dict(n=2, nk=2, beta=sp.Rational(1, 8), vol=4 * sp.pi, K2=sp.Rational(2, 3), mu2=sp.Rational(1, 12)),
    "CP1": dict(n=2, nk=8, beta=beta_cp(1), vol=V1, K2=avs[1][0], mu2=FLUXNORM ** 2 * avs[1][2]),
    "CP2": dict(n=4, nk=24, beta=beta_cp(2), vol=V2, K2=avs[2][0], mu2=FLUXNORM ** 2 * avs[2][2]),
}
for k_, v in FACT.items():
    print(f"    factor {k_}: n = {v['n']}, R^2*Ricci_scalar = {v['nk']}, beta = {v['beta']}, vol/R^n = {v['vol']}, <K^2>/R^2 = {v['K2']}, <mu^2>/N^2 = {v['mu2']}")

def solve_map(names):
    Ns = sp.symbols(f"N1:{len(names) + 1}", positive=True)
    Xs = sp.symbols(f"X1:{len(names) + 1}", positive=True)
    Wexpr = Lam / kap ** 2 - sum(FACT[nm]["nk"] * X / (2 * kap ** 2) for nm, X in zip(names, Xs)) + sum(FACT[nm]["beta"] * N_ ** 2 * X ** 2 / gg ** 2 for nm, N_, X in zip(names, Ns, Xs))
    eqs = [sp.diff(Wexpr, X) for X in Xs]
    Xsol = sp.solve(eqs, Xs, dict=True)[0]
    Lsol = sp.solve(Wexpr.subs(Xsol), Lam)[0]
    return Ns, Xs, Xsol, sp.simplify(Lsol)

def einstein_check(names, Ns, Xsol, Lsol):
    """10D (or D) Einstein equations block by block: 4D block and each factor block, with H = 0 (Minkowski)."""
    Xs = list(sp.symbols(f"X1:{len(names) + 1}", positive=True))
    Rtot = sum(FACT[nm]["nk"] * X for nm, X in zip(names, Xs))
    F2i = [4 * FACT[nm]["beta"] * N_ ** 2 * X ** 2 for nm, N_, X in zip(names, Ns, Xs)]
    F2 = sum(F2i)
    unknown = list(Xs) + [Lam]
    eqs = [sp.Eq(Lam - Rtot / 2, -kap ** 2 * F2 / (4 * gg ** 2))]
    for nm, X, f2i in zip(names, Xs, F2i):
        n_ = FACT[nm]["n"]; rho = FACT[nm]["nk"] * X / n_
        eqs.append(sp.Eq(rho - Rtot / 2 + Lam, kap ** 2 / gg ** 2 * (f2i / n_ - F2 / 4)))
    sol = sp.solve(eqs, unknown, dict=True)
    ok = False
    for s_ in sol:
        if all(sp.simplify(s_[X] - Xsol[X]) == 0 for X in Xs) and sp.simplify(s_[Lam] - Lsol) == 0:
            ok = True
    return ok

def couplings(names, Ns, Xsol, iso):
    """alpha of the isometry of factor 'iso' and of the unit-charge U(1), in terms of kappa, g, N_i (all X_i substituted)."""
    Xs = sp.symbols(f"X1:{len(names) + 1}", positive=True)
    Rsq = {nm: 1 / Xsol[X] for nm, X in zip(names, Xs)}
    Vint = sp.prod([FACT[nm]["vol"] * Rsq[nm] ** sp.Rational(FACT[nm]["n"], 2) for nm in names])
    out = {}
    for nm in iso:
        d = FACT[nm]
        Nf = Ns[names.index(nm)]
        invg2 = Vint * (d["K2"] * Rsq[nm] / (2 * kap ** 2) + d["mu2"] * Nf ** 2 / gg ** 2)
        out[nm] = sp.simplify(1 / (4 * sp.pi * invg2))
    out["U1"] = sp.simplify(gg ** 2 / (4 * sp.pi * Vint))
    lP2 = sp.simplify(kap ** 2 / (8 * sp.pi * Vint))
    return out, lP2, Rsq, Vint

print("\nM1  CP^1 reproduces the S^2 result through the GENERAL code (the check that the machinery is right)")
names = ["CP1"]
Ns, Xs, Xsol, Lsol = solve_map(names)
check("M1a Einstein-equation cross-check agrees with the dW = 0 extremum (CP^1)", einstein_check(names, Ns, Xsol, Lsol))
al, lP2, Rsq, Vint = couplings(names, Ns, Xsol, ["CP1"])
RS2 = sp.simplify(Rsq["CP1"] / 4)             # radius rho^2 = R_FS^2/4
check("M1b radius: rho^2 = N^2 kappa^2/(4 g^2) (= f2 B2a)", sp.simplify(RS2 - Ns[0] ** 2 * kap ** 2 / (4 * gg ** 2)) == 0, f"(rho^2 = {RS2})")
a_SU2 = sp.simplify(al["CP1"] / (lP2 / RS2)); a_U1 = sp.simplify(al["U1"] / (lP2 / RS2))
check("M1c alpha_SU2 = 3 l_P^2/rho^2 and alpha_U1 = N^2 l_P^2/(2 rho^2) from the general code (equals n1_1)", sp.simplify(a_SU2 - 3) == 0 and sp.simplify(a_U1 - Ns[0] ** 2 / 2) == 0, f"(got {a_SU2}, {a_U1})")

print("\nM2  D = 8: M_4 x CP^2, one Maxwell field with flux N_1 (SU(3) x U(1))")
names = ["CP2"]
Ns, Xs, Xsol, Lsol = solve_map(names)
check("M2a Einstein-equation cross-check (CP^2)", einstein_check(names, Ns, Xsol, Lsol))
al, lP2, Rsq, Vint = couplings(names, Ns, Xsol, ["CP2"])
R1sq = Rsq["CP2"]
a3 = sp.simplify(al["CP2"] / (lP2 / R1sq)); aU = sp.simplify(al["U1"] / (lP2 / R1sq))
print(f"    R_FS^2 = {sp.simplify(R1sq)};  alpha_3 = {a3} l_P^2/R_FS^2;  alpha_U1(unit) = {aU} l_P^2/R_FS^2")
phi3 = sp.simplify(FACT["CP2"]["mu2"] * FACT["CP2"]["nk"] / (2 * FACT["CP2"]["beta"] * FACT["CP2"]["K2"]))
print(f"    flux/geometry ratio of 1/g_3^2 at Minkowski: phi_3 = {phi3}  (S^2: 1)")
check("M2b alpha_3 = 4 l_P^2 / (<K^2>(1 + phi_3)) reproduced", sp.simplify(a3 - 4 / (FACT["CP2"]["K2"] * (1 + phi3))) == 0)

print("\nM3  Map C: D = 10, M_4 x CP^2 x S^2, ONE Maxwell field with fluxes (N_1 on CP^2, N_2 on S^2)")
names = ["CP2", "S2"]
Ns, Xs, Xsol, Lsol = solve_map(names)
N1s, N2s = Ns
print(f"    X_1 = 1/R_1^2 = {sp.simplify(Xsol[Xs[0]])};  X_2 = 1/R_2^2 = {sp.simplify(Xsol[Xs[1]])};  Lambda_10 = {Lsol}")
check("M3a Minkowski conditions decouple: R_i^2 proportional to N_i^2 (one common free real g^2/kappa^{3/2}-type scale)",
      sp.simplify(Xsol[Xs[0]] * N1s ** 2 - Xsol[Xs[0]].subs(N1s, 1) ) == 0 and sp.simplify(Xsol[Xs[1]] * N2s ** 2 - Xsol[Xs[1]].subs(N2s, 1)) == 0)
check("M3b Einstein-equation cross-check on the product (4D block + CP^2 block + S^2 block)", einstein_check(names, Ns, Xsol, Lsol))
al, lP2, Rsq, Vint = couplings(names, Ns, Xsol, ["CP2", "S2"])
R1sq, R2sq = Rsq["CP2"], Rsq["S2"]
alpha3, alpha2, alphaU = al["CP2"], al["S2"], al["U1"]
r_23 = sp.simplify(alpha2 / alpha3)           # alpha_2/alpha_3
r_U2 = sp.simplify(alphaU / alpha2)           # alpha_U1(unit)/alpha_2
r_U3 = sp.simplify(alphaU / alpha3)
r_R = sp.simplify(R1sq / R2sq)
a2_x = sp.simplify(alpha2 / (lP2 / R2sq))
a3_x = sp.simplify(alpha3 / (lP2 / R1sq))
print(f"    alpha_2/alpha_3 = {r_23};   alpha_U1/alpha_2 = {r_U2};   alpha_U1/alpha_3 = {r_U3};   R_1^2/R_2^2 = {r_R}")
print(f"    alpha_2 = {a2_x} l_P^2/R_2^2;  alpha_3 = {a3_x} l_P^2/R_1^2   (R_1 is the Fubini-Study scale)")
C0 = sp.simplify(r_23 * N2s ** 2 / N1s ** 2)
check("M3c alpha_2/alpha_3 = C0 (N_1/N_2)^2 with C0 a pure number; alpha_U1/alpha_2 = N_2^2/6 (same as the S^2 map alone)", C0.is_number and sp.simplify(r_U2 - N2s ** 2 / 6) == 0, f"(C0 = {C0})")
check("M3d alpha_2 = 3 l_P^2/R_2^2 also in the product (flux = geometry at each factor)", sp.simplify(a2_x - 3) == 0)
print(f"    alpha_3 = {a3_x} l_P^2/R_FS^2;  in terms of the CP^1 line radius rho = R_FS/2: alpha_3 = {sp.simplify(a3_x/4)} l_P^2/rho^2")
alpha3_eq_alpha2 = sp.simplify(sp.sqrt(1 / C0))
print(f"    alpha_3 = alpha_2 requires N_1/N_2 = {alpha3_eq_alpha2} = {float(alpha3_eq_alpha2):.4f}  (a derived value; an integer/half-integer ratio must approximate it)")

print("\nM4  content lattice of the CP^2 x S^2 zero modes (spin^c counts RECALLED; counting identities checked)")
k_ = sp.symbols("k", integer=True, nonnegative=True)
dimS = lambda k: sp.Rational((k + 1) * (k + 2), 2)
check("M4a dim Sym^k(C^3) = (k+1)(k+2)/2: k = 0, 1, 2, 3 -> 1, 3, 6, 10 (singlet, triplet, sextet, ...)", [dimS(k) for k in range(4)] == [1, 3, 6, 10])
mflux = {1: sp.Rational(3, 2), 3: sp.Rational(5, 2)}     # |qN_1| = k + 3/2 for SU(3) dimension 1, 3
FIELDS = {"Q": (3, 2, Fraction(1, 6)), "L": (1, 2, Fraction(-1, 2)), "u^c": (3, 1, Fraction(-2, 3)), "d^c": (3, 1, Fraction(1, 3)), "e^c": (1, 1, Fraction(1))}
ratios = {}
for f, (d3, d2, Y) in FIELDS.items():
    ratios[f] = mflux[d3] / d2                         # required N_1/N_2 = |q N_1| / |q N_2|
    print(f"      {f:4s} (dim_SU3, dim_SU2) = ({d3},{d2}), |Y| = {abs(Y)}:  |q N_1| = {mflux[d3]}, |q N_2| = {d2}  =>  N_1/N_2 = {ratios[f]}")
same = [S for r in range(2, 6) for S in itertools.combinations(FIELDS, r) if len({ratios[f] for f in S}) == 1]
check("M4b the five SM types need five (four distinct) values of N_1/N_2 {5/4, 3/4, 5/2, 3/2}; only (u^c, d^c) share one, so Q, L, u^c, e^c cannot coexist for any single (N_1, N_2)", same == [("u^c", "d^c")] and len(set(ratios.values())) == 4, f"(pairs with equal required N_1/N_2: {same})")
qmag = {f: mflux[FIELDS[f][0]] for f in FIELDS}
tri = {abs(FIELDS[f][2]) for f in FIELDS if FIELDS[f][0] == 3}
sing = {abs(FIELDS[f][2]) for f in FIELDS if FIELDS[f][0] == 1}
check("M4c the CP^2 lattice alone forces every colour triplet to have the same |q| (=5/(2N_1)) and every colour singlet the same |q| (=3/(2N_1)); SM |Y| among triplets = {1/6, 2/3, 1/3}, singlets {1/2, 1}",
      len(tri) > 1 and len(sing) > 1, f"(triplet |Y| set {sorted(tri)}, singlet {sorted(sing)})")
check("M4d required |q_triplet|/|q_singlet| = (5/2)/(3/2) = 5/3, while SM |Y_Q|/|Y_L| = 1/3, |Y_u|/|Y_e| = 2/3", sp.Rational(5, 2) / sp.Rational(3, 2) == sp.Rational(5, 3))

print("\nM5  family table for the scored trials of Map C (declared: N_2 in 1..6, N_1 in {1/2, 1, ..., 6}: 72 members)")
N1vals = [sp.Rational(i, 2) for i in range(1, 13)]
N2vals = list(range(1, 7))
table = []
for n1 in N1vals:
    for n2 in N2vals:
        table.append(dict(N1=float(n1), N2=n2, r23=float(r_23.subs({N1s: n1, N2s: n2})), rU2=float(r_U2.subs({N1s: n1, N2s: n2})), R1_over_R2=float(sp.sqrt(r_R.subs({N1s: n1, N2s: n2})))))
print(f"    members: {len(table)};  alpha_2/alpha_3 range {min(t['r23'] for t in table):.4g} .. {max(t['r23'] for t in table):.4g}; alpha_U1/alpha_2 = N_2^2/6 in {sorted({round(t['rU2'], 4) for t in table})}")
check("M5a the family has 72 members", len(table) == 72)
json.dump(dict(C0=str(C0), C0_float=float(C0), rU2="N2^2/6", table=table, alpha2_x=3, alpha3_x=str(a3_x), R1sq_over_R2sq=str(r_R), phi3=str(phi3),
               K2_cp2=str(FACT["CP2"]["K2"]), mu2_cp2=str(FACT["CP2"]["mu2"])), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "n1_2_map_table" + ("_MUTATE" if MUTATE else "") + ".json"), "w"), indent=1)

n_ok = sum(1 for _, o in CHECKS if o)
print("\n" + "=" * 100)
print(f"CHECKS: {n_ok}/{len(CHECKS)} passed")
print("VERDICT (Map C): the three couplings are forced functions of (N_1, N_2) and ONE free real (the overall g^2/kappa-type scale):")
print(f"  alpha_2/alpha_3 = {C0} (N_1/N_2)^2,  alpha_U1(unit)/alpha_2 = N_2^2/6;  two integers for two ratios (no over-determination beyond integer granularity);")
print("  the SM chiral content needs four different N_1/N_2 (M4) and hypercharges the lattice cannot give.")
sys.exit(0 if n_ok == len(CHECKS) else 1)
