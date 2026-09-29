#!/usr/bin/env python3
"""Q1 -- Salam-Sezgin (6D N=(1,0) gauged supergravity) on M_4 x S^2: vacuum, flux number, flat direction.
Pre-registered in Q3_PREREGISTRATION.md (written before this script was run).  Tests H1, H2, H5.

Bosonic action (hep-th/0307238 eq. 2.1, hep-th/0307052 eq. 2.1; H_(3) = 0 on the vacuum), overall factor 1/(2 kappa_6^2):
    L = R - (1/4)(d phi)^2 - (1/4) e^{phi/2} F_MN F^MN - c g^2 e^{-phi/2},   with c = 8  and every fermion of charge g.
Here p denotes the constant dilaton vev.  c = 8 is the Salam-Sezgin value (potential 8 g^2 e^{-phi/2}); the control changes it.

Run:   python3 q1_ss_vacuum_and_flat_direction.py            (real run, exits 0)
       python3 q1_ss_vacuum_and_flat_direction.py --mutate   (control: potential coefficient 8 g^2 -> 7 g^2, i.e. the SUSY tie between
                                                              the potential and the fermion charge is broken; must FAIL a check, exit 1)
"""
import sys
sys.dont_write_bytecode = True
import sympy as sp

MUTATE = "--mutate" in sys.argv
CHECKS = []


def check(tag, ok, detail=""):
    CHECKS.append((tag, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


cval = sp.Integer(7) if MUTATE else sp.Integer(8)
print("=" * 100)
print("Q1 Salam-Sezgin M_4 x S^2 vacuum -- mode: " + ("MUTATE CONTROL (potential coefficient 7 g^2 instead of 8 g^2)" if MUTATE else "REAL RUN (potential 8 g^2 e^{-phi/2}, charge g)"))
print("=" * 100)

g, R, f, p, kap2 = sp.symbols("g R f p kappa2", positive=True)
N = sp.symbols("N", positive=True)
gch = g                                                   # fermion charge = g (source: 'the fermions all carry charge g')
c = cval

# ------------------------------------------------------------------ A1/A2: field equations (source eq. 2.2, potential coefficient generalised to c g^2)
print("\nA1  6D field equations (hep-th/0307238 eq. 2.2, H=0, constant dilaton) on M_4 x S^2(R), F_ab = f eps_ab, F^2 = 2 f^2")
E = sp.exp(p / 2)
Emm = sp.Eq(0, sp.Rational(1, 2) * E * (0 - sp.Rational(1, 8) * 2 * f ** 2) + c / 4 * g ** 2 / E)              # R_{mu nu} = 0
Eab = sp.Eq(1 / R ** 2, sp.Rational(1, 2) * E * (f ** 2 - sp.Rational(1, 8) * 2 * f ** 2) + c / 4 * g ** 2 / E)  # R_ab = (1/R^2) g_ab
Edl = sp.Eq(0, sp.Rational(1, 4) * E * 2 * f ** 2 - c * g ** 2 / E)                                            # box phi = 0
f2_from_mm = sp.solve(Emm, f ** 2)[0]
f2_from_dl = sp.solve(Edl, f ** 2)[0]
print(f"    f^2 from (mu nu): {sp.simplify(f2_from_mm)};   f^2 from (dilaton): {sp.simplify(f2_from_dl)}")
check("A1a (mu nu) and (dilaton) equations give the SAME f^2 for every p (3 equations, 2 unknowns, consistent)", sp.simplify(f2_from_mm - f2_from_dl) == 0)
R2s = sp.Symbol("R2", positive=True)
R2 = sp.solve(sp.Eq(1 / R2s, Eab.rhs.subs(f, sp.sqrt(f2_from_mm))), R2s)[0]
R2 = sp.simplify(R2)
print(f"    R^2 = {R2}")
check("A1b radius: R^2 = e^{p/2}/(c g^2)  (c=8: e^{p/2}/(8 g^2); source (5.1) R = e^{-phi0/4}/(2 sqrt2 g), phi_hat = -phi)", sp.simplify(R2 - E / (c * g ** 2)) == 0)
check("A1c flux density f^2 = 2 c g^2 e^{-p}  (c=8: 16 g^2 e^{-p}; ABPQ F_mn F^mn = 8 g1^2 e^{2phi} in their convention)", sp.simplify(f2_from_mm - 2 * c * g ** 2 * sp.exp(-p)) == 0)

# ------------------------------------------------------------------ A3: the flux number
print("\nA3  flux number seen by the charge-g fermions:  N = g_ch * oint F / (2 pi) = 2 g_ch R^2 f")
Nflux = sp.simplify(2 * gch * R2 * sp.sqrt(f2_from_mm))
print(f"    N = {Nflux}   (independent of p: no free flux integer; it is fixed by the potential coefficient c and the charge)")
check("A3a N is independent of the dilaton vev p", sp.simplify(sp.diff(Nflux, p)) == 0)
check("A3b N = 1 exactly (potential coefficient 8 g^2 with fermion charge g forces the minimal monopole)", sp.simplify(Nflux - 1) == 0,
      f"[N = 2 sqrt2 /sqrt(c) = {sp.nsimplify(Nflux)}]")

# ------------------------------------------------------------------ A4: Killing-spinor twist, independent of the field equations
print("\nA4  gauge-covariantly constant spinor on S^2 (the SUSY twist): spin connection versus charge-g monopole")
th, ph = sp.symbols("theta phi_", real=True)
# orthonormal frame e1 = R dtheta, e2 = R sin(theta) dphi:  de2 = R cos(theta) dtheta ^ dphi = -omega^2_1 ^ e1  =>  omega^{21} = cos(theta) dphi
omega21 = sp.cos(th)
# spinor (sigma3 = +1 component): (d + (i/2) omega_12 sigma3 - i g A) = 0  =>  g A_phi = (1/2) omega_12 = -(1/2) cos(theta)
gA_phi = -sp.Rational(1, 2) * omega21                     # omega_12 = -omega_21 = -cos(theta) dphi ; (i/2)omega_12 = -(i/2) cos dphi  => g A = -(1/2) cos dphi
gF_thph = sp.diff(gA_phi, th)                             # g F_{theta phi}
flux = sp.integrate(sp.integrate(gF_thph, (th, 0, sp.pi)), (ph, 0, 2 * sp.pi))
print(f"    g A_phi = {gA_phi};  g F_theta_phi = {gF_thph};  g oint F = {sp.simplify(flux)}")
check("A4 |g oint F| = 2 pi  (N = 1 from the spin connection alone; agrees with A3b from the field equations)", sp.simplify(abs(flux) - 2 * sp.pi) == 0)

# ------------------------------------------------------------------ A5: reduced 4D potential, critical set
print("\nA5  reduced 4D Einstein-frame potential V_E(R, p) with flux number N (charge g):  V_E = (R0/R)^4 U,  U = 4 pi R^2 V_6")
R0 = sp.symbols("R0", positive=True)
Nn = sp.symbols("Nn", positive=True)
q = Nn / (2 * gch * R ** 2)
V6 = (1 / (2 * kap2)) * (-2 / R ** 2 + sp.Rational(1, 2) * E * q ** 2 + c * g ** 2 / E)
U = 4 * sp.pi * R ** 2 * V6
VE = (R0 / R) ** 4 * U
dVR = sp.simplify(sp.diff(VE, R).subs(R0, R))
dVp = sp.simplify(sp.diff(VE, p).subs(R0, R))
u = sp.symbols("u", positive=True)           # u = e^{p/2}
dVp_u = sp.simplify(dVp.subs(E, u).subs(sp.exp(p), u ** 2).subs(sp.exp(-p / 2), 1 / u))
sol_u = sp.solve(sp.Eq(dVp_u, 0), u)
print(f"    dV/dp = 0 gives e^(p/2) = {sol_u}")
crit_ok = False
resid_R = None
if sol_u:
    uu = sol_u[0]
    dVR_u = sp.simplify(dVR.subs(sp.exp(-p / 2), 1 / u).subs(sp.exp(p / 2), u).subs(sp.exp(p), u ** 2).subs(sp.exp(-p), 1 / u ** 2))
    resid_R = sp.simplify(dVR_u.subs(u, uu))
    print(f"    dV/dR on the dV/dp = 0 curve: {sp.factor(resid_R)}")
    # for the physical case N=1 (c=8) this must vanish identically in R (a critical CURVE); for general N it leaves a residual
    resid_N1 = sp.simplify(resid_R.subs(Nn, 1))
    resid_Ngen = sp.simplify(resid_R)
    print(f"    N = 1 : residual = {sp.factor(resid_N1)};   general N: residual = {sp.factor(resid_Ngen)}")
    crit_ok = (resid_N1 == 0)
check("A5a for N = 1 the critical conditions dV/dR = dV/dp = 0 are satisfied on a whole CURVE (one free parameter: the dilaton vev)", crit_ok)
if resid_R is not None:
    N2_ne = [s for s in sp.solve(sp.Eq(resid_R, 0), Nn)]
    print(f"    values of N admitting a critical point at all: {N2_ne}")
    check("A5b a critical point exists only for N = 1 (no free flux integer, no dS/AdS critical point for N != 1)", N2_ne == [1])

# V_E on the curve and Hessian
if sol_u and crit_ok:
    uu = sol_u[0].subs(Nn, 1)
    Vcurve = sp.simplify(VE.subs(R0, R).subs(Nn, 1).subs(sp.exp(-p / 2), 1 / u).subs(sp.exp(p / 2), u).subs(u, uu))
    print(f"    V_E on the critical curve = {Vcurve}")
    check("A5c V_E = 0 exactly on the whole critical curve (flat, Minkowski, for every dilaton vev)", Vcurve == 0)
    # Hessian wrt (R, p), R0 = R after differentiation
    H = sp.Matrix([[sp.diff(VE, a, b) for b in (R, p)] for a in (R, p)]).subs(R0, R).subs(Nn, 1)
    H = H.applyfunc(sp.simplify)
    uR = sp.simplify(uu)
    pR = sp.simplify(2 * sp.log(uR))
    Hc = H.subs(p, pR).applyfunc(sp.simplify)
    detH = sp.simplify(Hc.det())
    trH = sp.simplify(Hc.trace())
    print(f"    Hessian on the curve: det = {detH}, trace = {trH}")
    check("A5d Hessian on the curve has det = 0 (exactly one flat direction, rank <= 1)", detH == 0)
    check("A5e the other eigenvalue is positive (trace > 0 for g, kappa2 > 0): the R-p combination transverse to the curve is stabilised",
          sp.simplify(trH).is_positive is True or all(sp.N(trH.subs({g: gv, kap2: kv, R: Rv})) > 0 for gv in (0.3, 1, 2) for kv in (0.5, 1, 3) for Rv in (0.4, 1, 2.5)))
    # the curve: R^2 = e^{p/2}/(8 g^2); confirm it
    check("A5f the critical curve is R^2 = e^{p/2}/(8 g^2) -- same as the field-equation vacuum (A1b)", sp.simplify(uR - (8 * g ** 2 * R ** 2)) == 0)

# ------------------------------------------------------------------ A7: the vanishing of the 4D cosmological constant (source (2.5)-(2.6))
print("\nA7  cosmological constant vanishes for every smooth Poincare/dS/AdS-invariant solution (source (2.5)-(2.6)); algebra check of (2.5) -> (2.6)")
rho = sp.symbols("rho", real=True)
W = sp.Function("W")(rho)
a = sp.Function("a")(rho)
ph_f = sp.Function("phi")(rho)
Lam = sp.symbols("Lambda_4", real=True)
Xs = sp.Function("X")(rho)


def lap(h):        # scalar Laplacian on ds^2 = drho^2 + a^2 dpsi^2
    return sp.diff(a * sp.diff(h, rho), rho) / a


def div_grad(B, h):  # nabla . (B nabla h)
    return sp.diff(a * B * sp.diff(h, rho), rho) / a


eq25a = lap(W ** 4) / W ** 4 - 4 * Lam / W ** 2         # = X   (source 2.5, first line)
eq25b = div_grad(W ** 4, ph_f) / W ** 4                 # = X   (source 2.5, second line)
lhs26 = div_grad(W ** 4, ph_f - 4 * sp.log(W)) + 4 * Lam * W ** 2   # source (2.6)
diff_eq = sp.simplify((eq25b - eq25a) * W ** 4 - lhs26)
check("A7 (2.5b)-(2.5a) equals (2.6): nabla(W^4 nabla(phi - 4 log W)) + 4 Lambda W^2 = 0; integrating over compact Y gives Lambda int W^2 = 0", diff_eq == 0)

# ------------------------------------------------------------------ A8: anomaly-cancelling matter arithmetic quoted in ABPQ p.6
print("\nA8  anomaly-freedom arithmetic quoted in hep-th/0304256 p. 6: n_H = dim G + 244 for G = E6 x E7 x U(1)")
dimG = 78 + 133 + 1
check("A8 dim(E6 x E7 x U(1)) = 212 and n_H = 456 (the quaternionic manifold Sp(456,1)/(Sp(456) x Sp(1)) of the source)", dimG == 212 and dimG + 244 == 456)

n_ok = sum(1 for _, o in CHECKS if o)
print("\n" + "=" * 100)
print(f"CHECKS: {n_ok}/{len(CHECKS)} passed")
print("VERDICT (q1):")
print("  * H1: the potential coefficient 8 g^2 is tied to the fermion charge g; with it the M_4 x S^2 field equations are consistent for EVERY dilaton vev, V = 0 exactly, and the flux number is forced to N = 1.")
print("        Lambda_6 is therefore NOT a free tunable: in lane F's variables Lambda_6 = 2 g_F^2/(N^2 kappa^2) holds automatically at N = 1 (checked in q3).")
print("  * H2: the critical set of the reduced potential is a CURVE R^2 = e^{p/2}/(8 g^2). The dilaton vev p (equivalently chat) is a modulus with V = 0 exactly: NOT fixed.")
print("  * H5 (part): Hessian rank 1 with one positive direction; the flat direction is exact at tree level (protected by 4D N=1 per the source; the lifting mechanism is not addressed here).")
sys.exit(0 if n_ok == len(CHECKS) else 1)
