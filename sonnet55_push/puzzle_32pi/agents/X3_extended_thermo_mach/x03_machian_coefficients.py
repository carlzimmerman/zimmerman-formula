#!/usr/bin/env python3
"""x03: exact Machian coefficients: Sciama's vector-potential toy, Brans-Dicke static uniform ball, and the expanding-universe
version of the same integral (arXiv:2308.04503 App. A).  Predeclared: PREDECLARED.md, PART B (B-S, B-BD, B-E).
c = 1 inside formulas; c is restored in the printed statements.  Controls must FAIL when the claim is mutated."""
import sympy as sp
from sympy import pi, sqrt, Rational as Rat, symbols, simplify
import mpmath as mp
import sys

PASS = FAIL = CO = CB = 0


def chk(n, c, d=""):
    global PASS, FAIL
    if c: PASS += 1; print("  ok  ", n, d)
    else: FAIL += 1; print("  FAIL", n, d)


def ctrl(n, c, d=""):
    global CO, CB
    if not c: CO += 1; print("  ctrl-ok ", n, d)
    else: CB += 1; print("  CTRL-BAD", n, d)


def zero(e): return sp.simplify(e) == 0


r, R, G, rho, w, phi0 = symbols('r R G rho omega phi0', positive=True)
omg = symbols('omega_', real=True)

print("== B-S: Sciama's toy, Phi = -G rho int_{r<R} dV/r ==")
Phi = -G * rho * sp.integrate(4 * pi * r ** 2 / r, (r, 0, R))
chk("Phi(R) = -2 pi G rho R^2 (uniform density, 1/r kernel)", zero(Phi + 2 * pi * G * rho * R ** 2))
I_of = lambda RR, rr_: 2 * pi * G * rr_ * RR ** 2            # I := |Phi|/c^2 (c = 1)
Grho = symbols('Grho', positive=True)                        # G * rho_L
HL2 = 8 * pi * Grho / 3                                       # Friedmann, flat, rho = rho_L
RH = 1 / sqrt(HL2)
Rstar = 1 / sqrt(Grho)
RS = 1 / sqrt(2 * pi * Grho)                                  # Sciama closure I = 1
I_H = simplify(2 * pi * Grho * RH ** 2)
I_star = simplify(2 * pi * Grho * Rstar ** 2)
chk("I(R_H) = 3/4 for any flat universe (R_H = c/H, H^2 = 8 pi G rho/3): the pi's cancel", I_H == Rat(3, 4))
chk("I(R*) = 2 pi (R* = c/sqrt(G rho))", simplify(I_star - 2 * pi) == 0)
chk("Sciama closure radius R_S/R_H = 2/sqrt3 (1.1547) and R_S/R* = 1/sqrt(2 pi)", simplify(RS / RH - 2 / sqrt(3)) == 0 and simplify(RS / Rstar - 1 / sqrt(2 * pi)) == 0)
chk("R_H/R* = sqrt(3/(8 pi)) = 0.3455 (the puzzle horizon radius R* is 2.894 Hubble radii)", simplify(RH / Rstar - sqrt(3 / (8 * pi))) == 0)
ctrl("mutation: Sciama's closure I = 1 is met at the Hubble radius", I_H == 1)
# sign of the vacuum's active mass density in the Newtonian toy: rho + 3 p = -2 rho_L for p = -rho_L
rhoL = symbols('rhoL', positive=True)
active = rhoL + 3 * (-rhoL)
Phi_vac = -G * active * sp.integrate(4 * pi * r ** 2 / r, (r, 0, R))
chk("premise flag: the GR active density of vacuum energy is rho + 3p = -2 rho_L, so the toy potential of the vacuum is +4 pi G rho_L R^2 > 0 (negative inertia), "
    "opposite in sign and twice the size of the potential with +rho_L (which the puzzle uses)", zero(Phi_vac - 4 * pi * G * rhoL * R ** 2))

print("\n== B-BD: Brans-Dicke static uniform ball (weak-field derivation from the field equations) ==")
# BD field equation (opened paper arXiv:1204.3455, Eq. 16): R_ij - g_ij R/2 = (8 pi/phi) T_ij + (omega/phi^2)(...) + (1/phi)(phi_;ij - g_ij box phi);
# scalar equation Eq. 18: box phi = 8 pi T/(2 omega + 3).  Linearise about phi0, static, eta = diag(-1,1,1,1).
rho_, p_, box = symbols('rho_ p_ box')
T = -rho_ + 3 * p_                          # trace of the perfect fluid (signature -+++)
box_phi = 8 * pi * T / (2 * omg + 3)
eta00 = -1
G00 = (8 * pi * rho_ + (0 - eta00 * box_phi)) / phi0            # phi0 G_00 = 8 pi T_00 + (d0 d0 phi - eta_00 box phi), static
Rtr = (3 * box_phi - 8 * pi * T) / phi0                           # trace: -R phi0 = 8 pi T - 3 box  => R
# G_mu nu = R_mu nu - (1/2) eta_mu nu R  =>  R_mu nu = G_mu nu + (1/2) eta_mu nu R
R00 = sp.simplify(G00 + Rat(1, 2) * eta00 * Rtr)
chk("R_00 (BD linearised, static) = [8 pi rho + 4 pi T (2 omega + 2)/(2 omega + 3)]/phi0",
    zero(R00 - (8 * pi * rho_ + 4 * pi * T * (2 * omg + 2) / (2 * omg + 3)) / phi0))
R00_dust = sp.simplify(R00.subs(p_, 0))
Geff = sp.simplify(R00_dust / (4 * pi * rho_))               # R_00 = laplacian(Phi_N) = 4 pi G rho
chk("dust: G = (2 omega + 4)/((2 omega + 3) phi0)  (Brans-Dicke's relation, derived)", zero(Geff - (2 * omg + 4) / ((2 * omg + 3) * phi0)))
chk("GR limit omega -> infinity: G phi0 -> 1", sp.limit((2 * omg + 4) / (2 * omg + 3), omg, sp.oo) == 1)
ctrl("mutation: the Newtonian potential obeys nabla^2 Phi = 8 pi G rho (would change G by 2)", zero(R00_dust / (8 * pi * rho_) - (2 * omg + 4) / ((2 * omg + 3) * phi0)))
# scalar potential at the centre of a uniform ball of radius R: nabla^2 phi = 8 pi T/(2 omega + 3) with T = -rho (dust)
def phi_center(sourceT, RR):
    S = 8 * pi * sourceT / (2 * omg + 3)          # nabla^2 phi = S  (static); phi(0) = -(1/4 pi) int S/r dV
    return sp.simplify(-(1 / (4 * pi)) * sp.integrate(S * 4 * pi * r, (r, 0, RR)))
phi_dust = phi_center(-rho, R)
phi_vac = phi_center(-4 * rhoL, R)               # a cosmological-constant fluid p = -rho_L has T = -rho + 3p = -4 rho_L
chk("phi(0) = 4 pi rho R^2/(2 omega + 3) for a uniform dust ball", zero(phi_dust - 4 * pi * rho * R ** 2 / (2 * omg + 3)))
chk("phi(0) = 16 pi rho_L R^2/(2 omega + 3) when the source is the vacuum-energy trace T = -4 rho_L", zero(phi_vac - 16 * pi * rhoL * R ** 2 / (2 * omg + 3)))
X = symbols('X', positive=True)                    # X := G rho R^2 / c^2
Md = sp.solve(sp.Eq((2 * omg + 4) / (2 * omg + 3), 4 * pi * X / (2 * omg + 3)), X)[0]
Mv = sp.solve(sp.Eq((2 * omg + 4) / (2 * omg + 3), 16 * pi * X / (2 * omg + 3)), X)[0]
chk("Mach relation, dust source:   G rho R^2/c^2 = (omega + 2)/(2 pi)", zero(Md - (omg + 2) / (2 * pi)))
chk("Mach relation, vacuum trace:  G rho_L R^2/c^2 = (omega + 2)/(8 pi)", zero(Mv - (omg + 2) / (8 * pi)))
print("   (the 'ball' coefficient carries one 1/pi; Friedmann's G rho_L R_H^2 = 3/(8 pi) carries the same 1/pi)")
# needed omega for each cutoff
def omega_needed(target_X, dust=True):
    return sp.simplify(sp.solve(sp.Eq((omg + 2) / (2 * pi) if dust else (omg + 2) / (8 * pi), target_X), omg)[0])
cut = {"R_H (Hubble)": 3 / (8 * pi), "R* = c/sqrt(G rho_L)": Rat(1), "2 R* = c^2/a0 (Rindler distance of a0)": Rat(4)}
print("   omega needed so that the Mach relation holds at each cutoff:")
tab = {}
for nm, X_ in cut.items():
    wd, wv = omega_needed(X_, True), omega_needed(X_, False)
    tab[nm] = (wd, wv)
    print(f"     {nm:42s} dust: omega = {wd} = {float(wd):.5f}    vacuum-trace: omega = {wv} = {float(wv):.5f}")
chk("Hubble cutoff needs a RATIONAL omega: dust -5/4, vacuum-trace +1 (the pi's cancel)", tab["R_H (Hubble)"][0] == Rat(-5, 4) and tab["R_H (Hubble)"][1] == 1)
chk("cutoff R* needs omega = 2 pi - 2 (dust) or 8 pi - 2 (trace): irrational", tab["R* = c/sqrt(G rho_L)"][0] - (2 * pi - 2) == 0 and tab["R* = c/sqrt(G rho_L)"][1] - (8 * pi - 2) == 0)
chk("cutoff 2R* (the a0 Rindler distance) needs omega = 8 pi - 2 (dust) or 32 pi - 2 (trace)", tab["2 R* = c^2/a0 (Rindler distance of a0)"][0] - (8 * pi - 2) == 0 and tab["2 R* = c^2/a0 (Rindler distance of a0)"][1] - (32 * pi - 2) == 0)
PRINCIPLED = [Rat(-3, 2), Rat(-4, 3), Rat(-1), Rat(-1, 2), Rat(0)]           # declared principled (conformal, 5D-KK, string, ..., f(R)/KK)
LIST = PRINCIPLED + [Rat(1, 2), Rat(1), Rat(3, 2), Rat(2)]                  # all declared values (positive ones carry NO principle)
hit_list = [(nm, k, v) for nm, (wd, wv) in tab.items() for k, v in (("dust", wd), ("trace", wv)) if v in LIST]
hit_princ = [(nm, k, v) for nm, k, v in hit_list if v in PRINCIPLED]
print(f"   needed omegas that are in the declared list: {hit_list};  in the PRINCIPLED sub-list: {hit_princ}")
chk("no needed omega lies in the principled sub-list {-3/2,-4/3,-1,-1/2,0} (the one list hit, omega = +1, carries no principle and is a Hubble-cutoff/Friedmann-class rational)",
    len(hit_princ) == 0 and len(hit_list) == 1 and hit_list[0][2] == 1)
# algebraic-ness of the implied cutoff ratio and of a_c/(cH): R_c/R_H
RcRH_dust = sp.simplify(sqrt((omg + 2) / (2 * pi) / (3 / (8 * pi))))
RcRH_vac = sp.simplify(sqrt((omg + 2) / (8 * pi) / (3 / (8 * pi))))
chk("R_c/R_H = sqrt(4 (omega+2)/3) (dust) or sqrt((omega+2)/3) (vacuum trace): the pi's cancel", zero(RcRH_dust - sqrt(4 * (omg + 2) / 3)) and zero(RcRH_vac - sqrt((omg + 2) / 3)))
Zs = sqrt(32 * pi / 3)
okalg = all(sp.nsimplify(RcRH_dust.subs(omg, wv_)).is_algebraic and sp.nsimplify(RcRH_vac.subs(omg, wv_)).is_algebraic for wv_ in [Rat(-1), Rat(0), Rat(1), Rat(3, 2), Rat(5, 7)])
chk("for every rational omega tested R_c/R_H is algebraic, whereas the puzzle needs R_c/R_H = Z = sqrt(32 pi/3), transcendental (sympy: not algebraic)", okalg and Zs.is_algebraic is False)
chk("with a_c = c^2/R_c: a_c^2/(G rho_L c^2) = 8 pi/(omega+2) (vacuum trace) or 2 pi/(omega+2) (dust); = 1/4 iff omega = 32 pi - 2 or 8 pi - 2",
    zero(sp.solve(sp.Eq(8 * pi / (omg + 2), Rat(1, 4)), omg)[0] - (32 * pi - 2)) and zero(sp.solve(sp.Eq(2 * pi / (omg + 2), Rat(1, 4)), omg)[0] - (8 * pi - 2)))
ctrl("mutation: a rational omega gives a_c^2/(G rho_L c^2) = 1/4", any(abs(float(8 * pi / (wr + 2)) - 0.25) < 1e-9 for wr in [Rat(k, 4) for k in range(-5, 400)] if wr != -2))

print("\n== B-E: the same integral in an expanding universe (arXiv:2308.04503 Appendix A; opened) ==")
mp.mp.dps = 25
def I_exp(Om, Or, OL, kind):
    E = lambda a: Om * a ** -3 + Or * a ** -4 + OL
    dEta = lambda a: 1 / (a ** 2 * mp.sqrt(E(a)))                   # H0 = 1, c = 1
    eta = lambda a: mp.quad(dEta, [a, 1])
    if kind == 'lum':
        f = lambda a: a ** 4 * E(a) * eta(a) * dEta(a)
    else:
        f = lambda a: a ** 2 * E(a) * eta(a) * dEta(a)
    return mp.mpf(3) / 2 * mp.quad(f, [0, 1e-6, 1e-3, 0.1, 1])      # 4 pi G rho_cr0 / H0^2 = 3/2
I_eds = I_exp(1, 0, 0, 'lum'); I_lcdm = I_exp(0.27, 8.24e-5, 0.73, 'lum'); I_lam = I_exp(0, 0, 1, 'lum')
print(f"   luminosity-distance version: EdS {mp.nstr(I_eds,8)}, LCDM(0.27/0.73, Or=8.24e-5) {mp.nstr(I_lcdm,8)}, pure Lambda {mp.nstr(I_lam,8)}")
chk("reproduces the paper's LCDM value 0.416 (luminosity distance) from its stated integrand", abs(I_lcdm - mp.mpf('0.416')) < 5e-4)
chk("EdS (matter-dominated) gives exactly 1/2 from the same integrand, NOT the paper's stated 'exactly 1' (paper statement not reproduced; factor 2)", abs(I_eds - mp.mpf(1) / 2) < 1e-12)
chk("pure Lambda (luminosity distance) gives exactly 1/4 = (3/2)(1/6): finite, rational; proper distance diverges log at a -> 0", abs(I_lam - mp.mpf(1) / 4) < 1e-12)
# proper distance on pure Lambda: integrand (3/2) a^2 eta deta -> int (1/a - 1) da diverges
aeps = [mp.mpf('1e-2'), mp.mpf('1e-4'), mp.mpf('1e-6')]
vals = [mp.mpf(3) / 2 * mp.quad(lambda a: a ** 2 * ((1 / a - 1)) * (1 / a ** 2), [ae, 1]) for ae in aeps]
chk("proper-distance version on pure Lambda diverges logarithmically (1.5 * ln(1/a_min) growth)", vals[1] - vals[0] > 6 and vals[2] - vals[1] > 6, f"{[mp.nstr(v, 6) for v in vals]}")
print("   => the coefficient of Sciama's integral in an expanding universe depends on the distance measure (luminosity vs proper), on the matter content and on the lower cutoff:")
print(f"      3/4 (sharp Hubble sphere), 0.416 (LCDM, luminosity), 1/2 (EdS, luminosity), 1/4 (Lambda, luminosity), diverges (proper, Lambda). None is 1; none contains a0.")

print("\n== premise counts (each premise = something not implied by the formulation's field equations) ==")
prem = {
    "B-S Sciama toy": ["gravito-electromagnetic analogy with the force law F = G m1 m2 a/(c^2 r) (coefficient 1)", "uniform density rho (which one: matter? vacuum with which sign, Tolman rho+3p?)",
                       "cutoff radius (Hubble sphere c/H)", "Newtonian retarded integral in an expanding, non-static universe", "the closure postulate |Phi| = c^2 (I = 1)"],
    "B-BD Brans-Dicke": ["omega (free)", "static uniform ball (no expansion, no Lambda-background solution)", "cutoff radius", "which stress-energy trace sources phi (dust vs vacuum p = -rho)", "Mach postulate G phi = (2 omega + 4)/(2 omega + 3) with phi the cosmic value"],
    "B-E expanding-universe integral": ["distance measure (luminosity vs proper)", "lower cutoff (a -> 0 divergence for matter)", "weights a^4 rho/r (not derived from a field equation in that paper)", "closure I = 1"],
}
for k, v in prem.items():
    print(f"   {k}: {len(v)} premises: " + "; ".join(v))
print("   (bookkeeping only: not counted as a check)")
print(f"\n== TOTAL: {PASS} pass, {FAIL} fail; controls rejected {CO}, not rejected {CB} ==")
sys.exit(0 if FAIL == 0 and CB == 0 else 1)
