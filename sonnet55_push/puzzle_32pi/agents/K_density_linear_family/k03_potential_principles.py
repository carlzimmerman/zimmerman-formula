"""k03: which principle could fix W_v = G rho_L / a0^2 = 4 (equivalently c = F(0)/F'(inf) = 32 pi), and does any?

Definitions.  W_v := G rho_L / a0^2  (dimensionless, hbar-free, c-free; in energy-density units rho ~ kg m^-1 s^-2).  The AQUAL
normalisation of k01 gives W_v = c/(8 pi).  The puzzle: W_v = 4.

 A  W_v is a dimensionless invariant of the units group (no hbar, no c): checked by the dimension matrix.
 B  NORMALISATION-INDEPENDENT form of the requirement: c = F(0)/F'(inf) is invariant under F -> lambda F; F(0) alone is not.  So the
    'natural O(1) constant' argument must be applied to the RATIO c, whose natural values (k01) are 0.3-26; the puzzle needs 100.5.
 C  every extremum / first-order / Z2 / Bogomolny principle is blind to the additive constant of the potential (sympy).
 D  the Hamilton-Jacobi (real 'superpotential') form V = 3W^2 - 2W'^2 admits de Sitter critical points with V_* = 3 W_*^2 but leaves W_* free;
    the SUSY form V = e^K(|DW|^2 - 3|W|^2) has V <= 0 at supersymmetric points (algebraic identity, textbook).
 E  Coleman-Weinberg: the one-loop vacuum energy carries hbar; equating it to 4 a0^2/G fixes a MASS, not a number.
 F  parameter counting for the generic scalar-with-potential completion: W_v is a free ratio of two parameters.
Everything here is a NO-GO / LIST of where a principle would have to act.  Nothing is derived.
"""
import sys
import sympy as sp
import mpmath as mp

OK = []


def chk(name, cond):
    OK.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name, flush=True)


mp.mp.dps = 30

# ------------------------------------------------------------------------------------------------ A
print("== A  W_v is a dimensionless, hbar-free, c-free invariant")
L, T, M = sp.symbols('L T M')
dims = {'a0': (1, -2, 0), 'G': (3, -2, -1), 'c': (1, -1, 0), 'hbar': (2, -1, 1), 'rho_energy': (-1, -2, 1)}
names = list(dims)
Mx = sp.Matrix([[dims[n][i] for n in names] for i in range(3)])
ns = Mx.nullspace()
print(f"   parameters {names}: rank {Mx.rank()}, {len(ns)} independent dimensionless invariants")
Wv = {'a0': -2, 'G': 1, 'c': 0, 'hbar': 0, 'rho_energy': 1}
chk("A1 G rho/a0^2 is dimensionless with no c and no hbar in it (rho as an energy density)", Mx * sp.Matrix([Wv[n] for n in names]) == sp.zeros(3, 1))
Wv_bad = {'a0': -2, 'G': 1, 'c': 0, 'hbar': 1, 'rho_energy': 1}
chk("A2 MUTATION: inserting one power of hbar breaks dimensionlessness", Mx * sp.Matrix([Wv_bad[n] for n in names]) != sp.zeros(3, 1))

# ------------------------------------------------------------------------------------------------ B
print("\n== B  the normalisation-independent form: c = F(0)/F'(inf)")
lam = sp.Symbol('lambda', positive=True)
F0, Finf = sp.symbols('F0 Finf', positive=True)
c_ratio = F0 / Finf
chk("B1 c = F(0)/F'(inf) is invariant under F -> lambda F while F(0) alone is not (the 8 pi of Einstein's coupling is a normalisation of F, so 'F(0) = O(1)' is convention-laden and 'c = O(1)' is not)",
    sp.simplify((lam * F0) / (lam * Finf) - c_ratio) == 0 and sp.simplify(lam * F0 - F0) != 0)
# in Milgrom's variable (F_M normalised WITHOUT the 1/(8 pi): F_M -> y/(8 pi) at large y) the vacuum constant is W_v itself
FM_slope_inf = 1 / (8 * sp.pi)
W_needed = 4
chk("B2 in the Milgrom-type normalisation (Newtonian slope 1/(8 pi)) the requirement F_M(0) = 4 reads F_M(0)/F_M'(inf) = 4 * 8 pi = 32 pi: the same c", sp.simplify(W_needed / FM_slope_inf - 32 * sp.pi) == 0)
# natural values of c (recomputed here from closed forms; see k01 for the integrations)
c_nat = {'sharp': mp.mpf(1) / 3, 'mu_n n=3': mp.mpf(1), 'exponential': mp.mpf(2), 'record OR N=5': 2 * mp.mpf(5) ** 2 / (4 * 3)}
cn = lambda n: -(2 / mp.mpf(n)) * mp.gamma(3 / mp.mpf(n)) * mp.gamma(-2 / mp.mpf(n)) / mp.gamma(1 / mp.mpf(n))
c_nat['mu_n n=6'] = cn(6)
# RAR-nu value from k01 (recomputed below by a short quadrature)
xr = lambda y: y / (-mp.expm1(-mp.sqrt(y)))
c_rar = mp.quad(lambda y: xr(y) ** 2 * mp.exp(-mp.sqrt(y)) / (2 * mp.sqrt(y)), [mp.mpf('1e-30'), 1, 10, 100, 1e3, 1e4, 1e5, 1e6])
c_nat['RAR-nu'] = c_rar
print("   values of c for parameter-free, data-shaped mu (finite-c cases), and G rho/a0^2 = c/(8 pi):")
for k_, v_ in c_nat.items():
    print(f"     {k_:14s} c = {mp.nstr(v_, 6):>9s}   W_v = {mp.nstr(v_ / (8 * mp.pi), 5)}")
need = 32 * mp.pi
print(f"   needed: c = 32 pi = {mp.nstr(need, 6)} (W_v = 4);  ratio to the largest natural value (RAR-nu): {mp.nstr(need / c_rar, 4)}")
chk("B3 the parameter-free, data-shaped members with finite c (sharp, mu_n n>=3, exponential, record OR N>=5, RAR-nu) span c = 0.33 ... 26: 32 pi = 100.5 lies a factor >= 3.9 above the largest, i.e. G rho/a0^2 between 0.013 and 1.03 versus the required 4",
    c_nat['sharp'] > 0.33 and c_rar < 27 and need / c_rar > 3.8)
chk("B4 bookkeeping identity: the same coefficient reads 4 in W_v and 32 pi = 100.5 in c; the factor is Einstein's 8 pi (an O(1) F0 in the Poisson normalisation means W_v ~ 1/(8 pi) ~ 0.04)",
    sp.simplify(sp.Integer(4) * 8 * sp.pi - 32 * sp.pi) == 0)

# ------------------------------------------------------------------------------------------------ C
print("\n== C  extremum / first-order / Z2 / Bogomolny principles cannot see the additive constant")
phi, Cc, lam_, v_ = sp.symbols('phi C lambda_q v', real=True)
Vq = lam_ / 4 * (phi ** 2 - v_ ** 2) ** 2                     # symmetric double well, V(+-v) = 0
def stationary(Vfun):
    return sp.solve(sp.diff(Vfun, phi), phi)
chk("C1 stationary points and second derivatives (masses) of V and V + C coincide", sorted(stationary(Vq), key=str) == sorted(stationary(Vq + Cc), key=str) and sp.simplify(sp.diff(Vq + Cc, phi, 2) - sp.diff(Vq, phi, 2)) == 0)
# Bogomolny kink: phi' = sqrt(2 (V - V_min)); the constant cancels
kink_rhs = lambda Vfun, Vmin: sp.sqrt(2 * (Vfun - Vmin))
chk("C2 the Bogomolny equation phi' = sqrt(2 (V - V_min)) is identical for V and V + C (V_min shifts too): tension and profile ignore C",
    sp.simplify(kink_rhs(Vq + Cc, (Vq + Cc).subs(phi, v_)) - kink_rhs(Vq, Vq.subs(phi, v_))) == 0)
# the two 'natural values' of the double well
V0 = sp.simplify(Vq.subs(phi, 0))
chk("C3 the Z2 barrier top V(0) = lambda v^4/4 is a free combination of two couplings (no number): nothing here equals 4 a0^2/G without inserting it",
    sp.simplify(V0 - lam_ * v_ ** 4 / 4) == 0)
sg = sp.Symbol('m2f2', positive=True)
chk("C4 sine-Gordon V = m^2 f^2 (1 - cos(phi/f)): barrier top 2 m^2 f^2 -- free as well", sp.simplify((sg * (1 - sp.cos(sp.pi))) - 2 * sg) == 0)

# ------------------------------------------------------------------------------------------------ D
print("\n== D  Hamilton-Jacobi (real superpotential) form and the SUSY form")
t = sp.Symbol('t')
Wf = sp.Function('W')
ph = sp.Function('varphi')
z = sp.Symbol('z')
Vz = 3 * Wf(z) ** 2 - 2 * sp.diff(Wf(z), z) ** 2
H = Wf(z)                                                   # H = W(phi)
phidot = -2 * sp.diff(Wf(z), z)                             # phi' = -2 W'(phi)  (8 pi G = 1)
friedmann = sp.simplify(3 * H ** 2 - (sp.Rational(1, 2) * phidot ** 2 + Vz))
Hdot = sp.diff(Wf(z), z) * phidot                            # dH/dt = W' phidot
raychaud = sp.simplify(Hdot + sp.Rational(1, 2) * phidot ** 2)
phiddot = sp.diff(phidot, z) * phidot
kg = sp.simplify(phiddot + 3 * H * phidot + sp.diff(Vz, z))
chk("D1 V = 3W^2 - 2W'^2 with H = W(phi), phidot = -2W'(phi) solves Friedmann, Raychaudhuri and Klein-Gordon identically (8 pi G = 1)", friedmann == 0 and raychaud == 0 and kg == 0)
# de Sitter: W' = 0 -> phidot = 0, Hdot = 0, V_* = 3 W_*^2 = Lambda
Wstar = sp.Symbol('W_star', positive=True)
Vstar = sp.simplify(Vz.subs(sp.diff(Wf(z), z), 0).subs(Wf(z), Wstar))
chk("D2 the de Sitter critical point W' = 0 has V_* = 3 W_*^2 = 3 H_*^2 (positive is allowed) -- but W_* is a free constant: the first-order principle relates V_* to H_* (tautology, Friedmann), never to a0", sp.simplify(Vstar - 3 * Wstar ** 2) == 0)
# SUSY: V = e^K(|DW|^2 - 3|W|^2) -> at DW = 0, V = -3 e^K |W|^2 <= 0
eK, Wabs2, DW2 = sp.symbols('eK Wabs2 DW2', nonnegative=True)
Vsusy = eK * (DW2 - 3 * Wabs2)
chk("D3 (textbook algebra) at a supersymmetric point DW = 0 the N=1 sugra potential is V = -3 e^K |W|^2 <= 0: a BPS/SUSY principle gives Minkowski or AdS, never rho_L > 0",
    sp.simplify(Vsusy.subs(DW2, 0) + 3 * eK * Wabs2) == 0 and sp.simplify(Vsusy.subs(DW2, 0).subs({eK: 1, Wabs2: 2})) < 0)

# ------------------------------------------------------------------------------------------------ E
print("\n== E  Coleman-Weinberg: the coefficient carries hbar, so equating it to 4 a0^2/G fixes a mass")
hbar, cc, Gn, a0s, m = sp.symbols('hbar c G a0 m', positive=True)
rho_cw = m ** 4 * cc ** 5 / (64 * sp.pi ** 2 * hbar ** 3)   # one-loop vacuum energy density, ~ (m c^2)^4/(hbar c)^3 / (64 pi^2), J m^-3
W_cw = sp.simplify(Gn * rho_cw / a0s ** 2)
SI = {'a0': (1, -2, 0), 'G': (3, -2, -1), 'c': (1, -1, 0), 'hbar': (2, -1, 1), 'm': (0, 0, 1)}
SYM = {a0s: 'a0', Gn: 'G', cc: 'c', hbar: 'hbar', m: 'm'}
def dim_expr(expr):
    """(L,T,M) exponents of a monomial in the SI symbols."""
    tot = sp.zeros(3, 1)
    for sym, ex in sp.powsimp(sp.expand(expr)).as_powers_dict().items():
        if sym in SYM:
            tot += sp.Matrix(SI[SYM[sym]]) * ex
    return tot
chk("E1 W_cw = G m^4 c^5/(64 pi^2 hbar^3 a0^2) is dimensionless and contains hbar^(-3): it is a function of the field's MASS", dim_expr(W_cw) == sp.zeros(3, 1) and W_cw.has(hbar))
# the mass that would make W_cw = 4 (SI numbers)
Gv, cv_, hv = 6.67430e-11, 2.99792458e8, 1.054571817e-34
for a0v in (9.3619e-11, 1.1279e-10):
    m4 = 4 * 64 * float(sp.pi) ** 2 * hv ** 3 * a0v ** 2 / (Gv * cv_ ** 5)
    mkg = m4 ** 0.25
    print(f"   a0 = {a0v:.4e}: W_cw = 4 needs m c^2 = {mkg * cv_ ** 2 / 1.602176634e-19 * 1e3:.3f} meV")
mev = ((4 * 64 * float(sp.pi) ** 2 * hv ** 3 * 9.3619e-11 ** 2 / (Gv * cv_ ** 5)) ** 0.25) * cv_ ** 2 / 1.602176634e-19 * 1e3
rho_L_Jm3 = 0.685 * 3 * (67.4e3 / 3.0856775814913673e22) ** 2 / (8 * float(sp.pi) * Gv) * cv_ ** 2
rho_L_meV = (rho_L_Jm3 * (hv * cv_) ** 3) ** 0.25 / 1.602176634e-19 * 1e3     # (rho_L (hbar c)^3)^(1/4) in meV
print(f"   rho_L^(1/4) = {rho_L_meV:.3f} meV (rho_L from H0 = 67.4, Omega_L = 0.685)")
chk("E2 the mass a one-loop vacuum needs for W_v = 4 is m c^2 = %.1f meV = (64 pi^2)^(1/4) rho_L^(1/4) with rho_L^(1/4) = %.2f meV (a free field mass; its numerical vicinity to the neutrino scale is the old rho_L^(1/4) fact, not a derivation)" % (mev, rho_L_meV),
    abs(mev - (64 * float(sp.pi) ** 2) ** 0.25 * rho_L_meV) / mev < 0.02 and 10 < mev < 13)
chk("E3 MUTATION: if the one-loop formula lost its hbar^-3 the ratio would not be dimensionless", dim_expr(sp.simplify(Gn * m ** 4 * cc ** 5 / (64 * sp.pi ** 2 * a0s ** 2))) != sp.zeros(3, 1))

# ------------------------------------------------------------------------------------------------ F
print("\n== F  generic completion: W_v is a free ratio")
V0s, Ks, a0g = sp.symbols('V0 K a0g', positive=True)     # V0: vacuum energy density parameter; K = a0^2/(8 pi G) the MOND-sector stiffness
W_free = sp.simplify(Gn * V0s / a0g ** 2)
chk("F1 S = int[R/16piG + (a0^2/8piG) F-term - V0 w(phi)] has W_v = G V0 w_v/a0^2: V0 and a0 enter through independent parameters, so W_v is free unless an extra relation ties them",
    sp.diff(W_free, V0s) != 0 and sp.diff(W_free, a0g) != 0)
# single-scale (Milgrom) completion: both a0 and the vacuum term come from the same length l: a0 = c^2/l, F-term coefficient (c^4/G) l^-2
ell = sp.Symbol('ell', positive=True)
a0_l = cc ** 2 / ell
rho_vac_l = cc ** 4 / (Gn * ell ** 2) * sp.Symbol('F0m')      # (c^4/G) l^-2 F0 (energy density scale, F0 = F(0) in that normalisation)
W_l = sp.simplify(Gn * rho_vac_l / a0_l ** 2)
print(f"   single-length completion: G rho_vac/a0^2 = {sp.simplify(W_l)}  (c-factors as displayed)")
chk("F2 in the single-length completion the ratio is a pure number F0 = F(0) (no free scale): the value is decided by the shape of F alone -- which is exactly the c[mu] of k01",
    sp.simplify(W_l - sp.Symbol('F0m')) == 0)

print(f"\n{sum(OK)}/{len(OK)} checks passed")
sys.exit(0 if all(OK) else 1)
