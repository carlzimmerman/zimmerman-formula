"""Lane Y, script 1: Part S of PREDECLARED.md (static bookkeeping: F_Lambda, M_H, the mass menu, Verlinde's factor).
Exact (sympy).  Every claim has a control that must fail.  Writes y01_results.json."""
import json
import os
import sympy as sp
from common import Ledger, HERE

L_ = Ledger("y01_static_bookkeeping")
pi = sp.pi
c, G, Lam, H, Lh = sp.symbols("c G Lambda H L", positive=True)

# ----------------------------------------------------------------------------- S1
print("\n== S1: vacuum tension across the de Sitter horizon, in units of F_max ==")
Fmax = c**4 / (4 * G)
rho_e = Lam * c**4 / (8 * pi * G)               # vacuum energy density (= -pressure), SI-like
Lsq = 3 / Lam                                     # L^2 = 3/Lambda (length^2), H = c/L
F_L = rho_e * 4 * pi * Lsq                        # pressure x horizon area
ratio = sp.simplify(F_L / Fmax)
L_.check(f"F_Lambda = P * A_H = {sp.simplify(F_L)} = {ratio} F_max", sp.simplify(ratio - 6) == 0)
L_.check("F_Lambda has no Lambda left (Lambda cancels between rho ~ Lambda and A ~ 1/Lambda)", not F_L.has(Lam))
# Buckingham Pi: exponents of (c, G, Lambda) in the basis (M, L, T)
dimmat = sp.Matrix([[0, 1, -1],      # c      = L T^-1
                    [-1, 3, -2],     # G      = M^-1 L^3 T^-2
                    [0, -2, 0]])     # Lambda = L^-2
L_.check(f"(c, G, Lambda) have independent dimensions (det = {dimmat.det()}): NO dimensionless combination, so any force built from them is a pure number x c^4/G",
         dimmat.det() != 0)
hbar_row = sp.Matrix([[1, 2, -1]])   # hbar = M L^2 T^-1
dimmat4 = dimmat.col_join(hbar_row)
L_.must_fail("control: adding hbar WOULD allow a dimensionless combination (Planck) -- the claim 'no combination' is about (c,G,Lambda) only",
             dimmat4.T.nullspace() == [])
# equivalence with Friedmann
rho_s, Hs = sp.symbols("rho H", positive=True)
Fsol = sp.solve(sp.Eq(rho_s * 4 * pi * (c / Hs) ** 2, 6 * Fmax), rho_s)[0]
L_.check(f"F_Lambda = 6 F_max  <=>  rho = {sp.simplify(Fsol)}  i.e. H^2 = 8 pi G rho/(3 c^2) (the Friedmann relation): S1 carries no information beyond Einstein's 8 pi and the sphere's 4 pi",
         sp.simplify(Fsol - 3 * Hs**2 * c**2 / (8 * pi * G)) == 0)
# mutations
F_mut_rho = (Lam * c**4 / (4 * pi * G)) * 4 * pi * Lsq / Fmax
F_mut_area = rho_e * 2 * pi * Lsq / Fmax
L_.must_fail("mutation rho_L = Lambda/(4 pi) must NOT still give 6 (gives 12)", sp.simplify(F_mut_rho - 6) == 0)
L_.must_fail("mutation area 4 pi -> 2 pi must NOT still give 6 (gives 3)", sp.simplify(F_mut_area - 6) == 0)
L_.must_fail("mutation F_max -> c^4/(2G) (deficit 4 pi G mu) must NOT still give 6 (gives 3)", sp.simplify(F_L / (c**4 / (2 * G)) - 6) == 0)
# D dimensions (Gibbons: no D>4 analogue as a pure number)
D = sp.symbols("D", positive=True)
Om = lambda n: 2 * pi ** (sp.Rational(n + 1, 2)) / sp.gamma(sp.Rational(n + 1, 2))  # area of unit S^n
def FL_D(Dv):
    Lam_D = sp.Rational((Dv - 1) * (Dv - 2), 2) / Lh**2      # Lambda = (D-1)(D-2)/(2 L^2)
    rho = Lam_D * c**4 / (8 * pi * G)
    return sp.simplify(rho * Om(Dv - 2) * Lh ** (Dv - 2) / (c**4 / (4 * G)))
vals = {Dv: FL_D(Dv) for Dv in (4, 5, 6)}
print("   F_Lambda / (c^4/4G) in D dimensions:", vals)
L_.check("D = 4: pure number 6; D = 5, 6: carry L^(D-4) (no pure number), as Gibbons notes for n > 4 (bound only on F/D^(n-4))",
         sp.simplify(vals[4] - 6) == 0 and vals[5].has(Lh) and vals[6].has(Lh))

# ----------------------------------------------------------------------------- S2
print("\n== S2: Hubble-radius mass and its field ==")
MH = c**3 / (2 * G * H)
Ls = c / H
gH = G * MH / Ls**2
L_.check("Schwarzschild mass of r_s = L: M_H = c^2 L/(2G) = c^3/(2 G H)", sp.simplify(2 * G * MH / c**2 - Ls) == 0)
L_.check("g_H = G M_H/L^2 = c H/2", sp.simplify(gH - c * H / 2) == 0)
L_.check("F_max/M_H = c H/2", sp.simplify(Fmax / MH - c * H / 2) == 0)
rho_H = 3 * H**2 * c**2 / (8 * pi * G)
L_.check("M_H = rho_L (4 pi/3) L^3 / c^2 (vacuum mass of the Hubble ball)", sp.simplify(rho_H / c**2 * sp.Rational(4, 3) * pi * Ls**3 - MH) == 0)
L_.must_fail("control: g_H is NOT c H/6", sp.simplify(gH - c * H / 6) == 0)

# ----------------------------------------------------------------------------- S3
print("\n== S3: the fixed mass menu, q = F_max/(M c H) ==")
Lg = sp.symbols("Lg", positive=True)   # geometric G = c = 1: L = 1/H
def q_of(M):   # G = c = 1, L = 1 (H = 1)
    return sp.simplify(sp.Rational(1, 4) / M)
rho1 = 3 / (8 * pi)                    # rho_L L^2 with G = c = L = 1 : rho = 3H^2/(8 pi)
r = sp.symbols("r", positive=True)
Vslice = sp.integrate(4 * pi * r**2 / sp.sqrt(1 - r**2), (r, 0, 1))
menu = {
    "M_a  rho (4pi/3) L^3 (Hubble-ball vacuum mass)": rho1 * sp.Rational(4, 3) * pi,
    "M_b  Komar mass of the dS horizon kappa*A/(4 pi) = L": (1 / sp.Integer(1)) * (1 * 4 * pi * 1) / (4 * pi),
    "M_c  Nariai mass L/(3 sqrt 3)": 1 / (3 * sp.sqrt(3)),
    "M_d  Lambda zero-force sphere at r = L: M = Lambda L^3/3": sp.Rational(3, 1) * 1 / 3,
    "M_e  rho A_H L (built after noting q = 1/6; VOID as evidence)": rho1 * 4 * pi * 1,
    "M_f  rho x proper volume of the static-patch slice (pi^2 L^3)": rho1 * Vslice,
    "M_g  rho x volume of the full S^3 (2 pi^2 L^3)": rho1 * 2 * pi**2,
}
L_.check(f"static-patch slice volume = pi^2 L^3 (sympy integral gives {Vslice})", sp.simplify(Vslice - pi**2) == 0)
qs = {}
for k, M in menu.items():
    qv = q_of(sp.nsimplify(M) if False else M)
    qs[k] = qv
    print(f"   {k:70s} M = {sp.nsimplify(M)} L/G   q = {qv}  = {float(qv):.6f}   Z = {sp.simplify(1/qv)} = {float(1/qv):.5f}")
L_.check("M_a gives q = 1/2", sp.simplify(list(qs.values())[0] - sp.Rational(1, 2)) == 0)
L_.check("M_b and M_d give q = 1/4 (Komar horizon mass = zero-force mass = 2 M_H)",
         sp.simplify(list(qs.values())[1] - sp.Rational(1, 4)) == 0 and sp.simplify(list(qs.values())[3] - sp.Rational(1, 4)) == 0)
L_.check("M_c (Nariai) gives q = 3 sqrt 3/4 = 1.299 (acceleration above H)", sp.simplify(list(qs.values())[2] - 3 * sp.sqrt(3) / 4) == 0)
L_.check("M_e gives q = 1/6 exactly, and M_e = F_Lambda L/c^2 = 3 M_H  (a0 = c H F_max/F_Lambda: the '6' is F_Lambda/F_max, so the mass is the input)",
         sp.simplify(list(qs.values())[4] - sp.Rational(1, 6)) == 0)
L_.check("M_f gives q = 2/(3 pi) (Z = 3 pi/2 = 4.712) and M_g gives q = 1/(3 pi) (Z = 3 pi = 9.42): the proper-volume masses carry pi and hit no target",
         sp.simplify(list(qs.values())[5] - 2 / (3 * pi)) == 0 and sp.simplify(list(qs.values())[6] - 1 / (3 * pi)) == 0)
targets = {"T6": sp.Rational(1, 6), "T2": sp.Rational(1, 2), "TF": sp.sqrt(3 / (32 * pi))}
decoys = {f"1/{n}": sp.Rational(1, n) for n in (3, 4, 5, 7, 8, 9, 10, 12)}
S_out = []
for k, qv in qs.items():
    lab = [t for t, tv in targets.items() if sp.simplify(qv - tv) == 0]
    dl = [d for d, dv in decoys.items() if sp.simplify(qv - dv) == 0]
    S_out.append({"entry": k, "q": str(qv), "q_float": float(qv), "target_hits": lab, "decoy_hits": dl,
                  "rational": bool(qv.is_rational)})
print("   target/decoy hits per entry:", [(o["entry"][:3], o["target_hits"], o["decoy_hits"]) for o in S_out])
nrat = sum(o["rational"] for o in S_out)
L_.check(f"S3 census: {nrat} of 7 masses give a rational q (1/2, 1/4, 1/4, 1/6 ...), 2 give pi-rational q, 1 gives an irrational algebraic q; exactly one target hit (M_e, void as evidence), one T2 hit (M_a = the trivial g_H), decoy hit 1/4 twice",
         nrat == 4 and sum(1 for o in S_out if o["target_hits"]) == 2 and sum(1 for o in S_out if "1/4" in o["decoy_hits"]) == 2)
L_.must_fail("control: no menu entry gives TF (a transcendental sqrt(3/32 pi)): the menu is a rational/pi-rational list", any("TF" in o["target_hits"] for o in S_out))
L_.must_fail("control: no entry gives the decoy 1/7 or 1/5 (a decoy hit at the same rate would signal a menu that hits anything)",
             any(("1/7" in o["decoy_hits"] or "1/5" in o["decoy_hits"]) for o in S_out))

# ----------------------------------------------------------------------------- S4 Verlinde
print("\n== S4: Verlinde's a_M/a0 = (d-3)/((d-2)(d-1)) from eqs (1.5)-(1.7) of 1611.02269 ==")
dd, a0V, gB, gD, SB, SD, Gs = sp.symbols("d a0V gB gD SigmaB SigmaD G", positive=True)
# (1.6): Sigma = (d-2)/(d-3) g/(8 pi G);  (1.5): Sigma_D^2 = a0 Sigma_B /(8 pi G (d-1))
eq_rel = sp.Eq(SD**2, a0V * SB / (8 * pi * Gs * (dd - 1)))
sub = {SD: (dd - 2) / (dd - 3) * gD / (8 * pi * Gs), SB: (dd - 2) / (dd - 3) * gB / (8 * pi * Gs)}
lhs = sp.simplify(eq_rel.lhs.subs(sub)); rhs = sp.simplify(eq_rel.rhs.subs(sub))
gD2 = sp.solve(sp.Eq(lhs, rhs), gD)[0]
aM = sp.simplify(gD2**2 / gB / a0V)
L_.check(f"a_M/a0 = {sp.factor(aM)}  (matches (1.7))", sp.simplify(aM - (dd - 3) / ((dd - 2) * (dd - 1))) == 0)
L_.check("the 8 pi G of (1.5) and of (1.6) cancel: a_M/a0 is pi-free and G-free (the 6 is (d-2)(d-1)/(d-3) at d = 4)", not aM.has(pi) and not aM.has(Gs))
tab = {d: sp.simplify(aM.subs(dd, d)) for d in range(3, 8)}
print("   a_M/a0 for d = 3..7:", tab)
L_.check("d = 4 gives 1/6 exactly; d = 5 also gives 1/6 (the d-dependence does not single out d = 4 by itself); d = 3 gives 0",
         tab[4] == sp.Rational(1, 6) and tab[5] == sp.Rational(1, 6) and tab[3] == 0)
L_.must_fail("control: a_M/a0 at d = 4 is NOT 1/2 (the 'Hubble-sphere field' value); the two 'rationals' are different objects", tab[4] == sp.Rational(1, 2))
# does the F_Lambda-type number (D-1)(D-2) agree with Verlinde's (d-1)(d-2)/(d-3) beyond D = 4 ?
FV = (dd - 1) * (dd - 2) / (dd - 3)
Fpure = (dd - 1) * (dd - 2)
agree = [d for d in range(3, 9) if d != 3 and sp.simplify(FV.subs(dd, d) - Fpure.subs(dd, d)) == 0]
L_.check(f"Verlinde's Z_V(d) = (d-1)(d-2)/(d-3) equals the horizon-force number (D-1)(D-2) only at d = 4 (agreement set in 3..8: {agree}); F_Lambda/F_max = 6 has no D>4 analogue as a pure number",
         agree == [4])

out = {"S1_ratio_FL_over_Fmax": int(ratio), "S3": S_out, "S4_aM_over_a0": {str(k): str(v) for k, v in tab.items()}}
json.dump(out, open(os.path.join(HERE, "y01_results.json"), "w"), indent=1)
L_.finish()
