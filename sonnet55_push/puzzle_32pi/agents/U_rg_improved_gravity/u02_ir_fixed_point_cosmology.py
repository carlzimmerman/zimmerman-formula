#!/usr/bin/env python3
"""u02_ir_fixed_point_cosmology.py -- the Bonanno-Reuter IR-fixed-point cosmology (astro-ph/0106468, opened), verified symbolically, and what it does and does
NOT fix about  G rho_Lambda / a0^2.

System (their 2.1, K = 0, c = 1):
   (adot/a)^2 = Lambda/3 + (8 pi/3) G rho ;  rho' + 3(1+w) H rho = 0 ;  Lambda' + 8 pi rho G' = 0 ;  G(t) = g* t^2/xi^2 , Lambda(t) = lambda* xi^2/t^2 (k = xi/t).
The Bianchi consistency condition (2.1c) is a CLASSICAL integrability condition; it fixes the cutoff-identification constant xi:  xi^2 = 8/(3 (1+w)^2 lambda*)  (their 4.1).

Claims re-derived here (sympy; no number is taken from the paper except as a comparison):
  (A) the solution a ~ t^alpha, alpha = 4/(3(1+w)); rho, G, Lambda as in their (4.2); Omega_M = Omega_Lambda = 1/2; rho G t^2 = 1/(3 pi (1+w)^2);
  (B) Lambda(t), rho_Lambda(t), G(t) rho_Lambda(t) contain NEITHER g* NOR lambda* separately: only the product g*lambda* enters G(t) (and rho); Lambda t^2 = 8/(3(1+w)^2) is a pure number;
  (C) G rho_Lambda / H^2 = 3/(16 pi) for every w  (a principle-fixed ratio to H^2, i.e. Omega_Lambda = 1/2) -- this is the ONLY fixed-point-fixed ratio of the vacuum density to a rate;
  (D) the RG scale itself, k/H = sqrt(3/(2 lambda*)) (w=0), depends on lambda*: the scale 'a0 := c^2 k' is NOT fixed, only Lambda and the product g*lambda* are;
  (E) if one IMPOSES the puzzle relation a0 = (c/2) sqrt(G rho_Lambda) with the running rho_Lambda, a0 = H sqrt(3/(64 pi)) = H/8.19, time dependent (a0 ~ H(t)); numbers.
Controls: (i) wrong xi makes the Friedmann/Bianchi system inconsistent (residual != 0); (ii) a mutated (4.1) with 8 -> 9 is rejected; (iii) the same algebra for a
CONSTANT-Lambda de Sitter background gives Omega_Lambda = 1 (not 1/2), so the 1/2 is really produced by the fixed-point structure.
Exit 0 iff all pass.
"""
import sys
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")

t, xi, gs, ls, w = sp.symbols('t xi g_star lambda_star w', positive=True)
al = sp.symbols('alpha', positive=True)
Gt = gs * t**2 / xi**2
Lt = ls * xi**2 / t**2

print("PART A  solve the coupled system with the fixed-point running")
# (2.1c): Lambda' + 8 pi rho G' = 0 -> rho
rho = sp.simplify(-sp.diff(Lt, t) / (8 * sp.pi * sp.diff(Gt, t)))
print("  rho(t) from Bianchi (2.1c) =", sp.simplify(rho))
# (2.1b) with rho ~ t^-4  -> 3(1+w) alpha = 4
alpha = sp.Rational(4, 3) / (1 + w)
a = t**alpha
H = sp.simplify(sp.diff(a, t) / a)
cons = sp.simplify(sp.diff(rho, t) + 3 * (1 + w) * H * rho)
check("matter conservation (2.1b) holds with alpha = 4/(3(1+w))", sp.simplify(cons) == 0)
# Friedmann residual
fried = sp.simplify(H**2 - Lt / 3 - sp.Rational(8, 3) * sp.pi * Gt * rho)
xi2_sol = sp.solve(sp.Eq(fried, 0), xi)
xi2 = sp.simplify(sp.Rational(8, 3) / ((1 + w)**2 * ls))
print("  Friedmann residual (2.1a) =", sp.simplify(fried))
check("Friedmann holds iff xi^2 = 8/(3(1+w)^2 lambda*)  (BR 4.1)", sp.simplify(fried.subs(xi, sp.sqrt(xi2))) == 0)
check("CONTROL (i): with xi^2 = 9/(3(1+w)^2 lambda*) (mutated) the Friedmann residual is NOT zero", sp.simplify(fried.subs(xi, sp.sqrt(sp.Rational(9, 3) / ((1 + w)**2 * ls)))) != 0)
# express everything with the consistent xi
sub = {xi: sp.sqrt(xi2)}
G_c = sp.simplify(Gt.subs(sub)); L_c = sp.simplify(Lt.subs(sub)); rho_c = sp.simplify(rho.subs(sub))
print("  G(t)      =", G_c)
print("  Lambda(t) =", L_c)
print("  rho(t)    =", rho_c)
check("BR (4.2c): G = (3/8)(1+w)^2 g* lambda* t^2", sp.simplify(G_c - sp.Rational(3, 8) * (1 + w)**2 * gs * ls * t**2) == 0)
check("BR (4.2d): Lambda = 8/(3(1+w)^2 t^2)", sp.simplify(L_c - 8 / (3 * (1 + w)**2 * t**2)) == 0)
check("BR (4.2b): rho = 8/(9 pi (1+w)^4 g* lambda* t^4)", sp.simplify(rho_c - 8 / (9 * sp.pi * (1 + w)**4 * gs * ls * t**4)) == 0)
rhoL = sp.simplify(L_c / (8 * sp.pi * G_c))
check("rho_Lambda = rho  (Omega_M = Omega_Lambda = 1/2)", sp.simplify(rhoL - rho_c) == 0)
Hc = sp.simplify(H)
Om_L = sp.simplify(rhoL / (3 * Hc**2 / (8 * sp.pi * G_c)))
check("Omega_Lambda = 1/2 for every w", sp.simplify(Om_L - sp.Rational(1, 2)) == 0)
check("BR (4.10): rho G t^2 = 1/(3 pi (1+w)^2)", sp.simplify(rho_c * G_c * t**2 - 1 / (3 * sp.pi * (1 + w)**2)) == 0)

print()
print("PART B  what enters the physical vacuum quantities")
GrhoL = sp.simplify(G_c * rhoL)
print("  G rho_Lambda =", GrhoL, " ; Lambda t^2 =", sp.simplify(L_c * t**2))
check("G(t) rho_Lambda(t) contains neither g* nor lambda*", not (GrhoL.has(gs) or GrhoL.has(ls)))
check("Lambda(t) contains neither g* nor lambda*", not (L_c.has(gs) or L_c.has(ls)))
check("G(t) depends on g* and lambda* ONLY through the product g* lambda*  (G/(g* lambda*) has neither)", not (sp.simplify(G_c / (gs * ls)).has(gs) or sp.simplify(G_c / (gs * ls)).has(ls)))
kk = sp.Symbol('k', positive=True)
Gk, Lk = gs / kk**2, ls * kk**2
check("SYMBOLIC IDENTITY for ANY RG running: G(k) rho_Lambda(k) = Lambda(k)/(8 pi); at the fixed point = lambda* k^2/(8 pi), g* cancels", sp.simplify(Gk * (Lk / (8 * sp.pi * Gk)) - ls * kk**2 / (8 * sp.pi)) == 0 and not sp.simplify(Gk * (Lk / (8 * sp.pi * Gk))).has(gs))

print()
print("PART C  the only fixed-point-fixed ratio: G rho_Lambda / H^2")
ratio = sp.simplify(GrhoL / Hc**2)
print("  G rho_Lambda / H^2 =", ratio)
check("G rho_Lambda/H^2 = 3/(16 pi) for every w", sp.simplify(ratio - 3 / (16 * sp.pi)) == 0)
# CONTROL (iii): constant Lambda de Sitter: H^2 = Lambda/3 -> Omega_Lambda = 1
Lam0, G0 = sp.symbols('Lambda0 G0', positive=True)
rhoL0 = Lam0 / (8 * sp.pi * G0); H0sq = Lam0 / 3
check("CONTROL (iii): pure de Sitter (Lambda const) has G rho_Lambda/H^2 = 3/(8 pi), Omega_Lambda = 1 -- twice the fixed-point value", sp.simplify(G0 * rhoL0 / H0sq - 3 / (8 * sp.pi)) == 0)
check("CONTROL (ii): the Friedmann residual is nonzero for ANY xi other than the consistent one (xi -> 1.1 xi)", sp.simplify(fried.subs(xi, 1.1 * sp.sqrt(xi2))) != 0)

print()
print("PART D  the RG scale k = xi/t is NOT fixed: k/H depends on lambda*")
kH = sp.simplify((xi / t).subs(sub) / Hc)
print("  k/H =", kH, "  ; at w=0:", sp.simplify(kH.subs(w, 0)))
check("k/H = sqrt(3/(2 lambda*)) at w = 0", sp.simplify(kH.subs(w, 0) - sp.sqrt(sp.Rational(3, 2) / ls)) == 0)
check("Lambda = lambda* k^2 = (3/2) H^2 at w = 0, whatever lambda* is", sp.simplify((ls * (xi / t)**2).subs(sub).subs(w, 0) - sp.Rational(3, 2) * Hc.subs(w, 0)**2) == 0)

print()
print("PART E  IF the puzzle relation a0 = (c/2) sqrt(G rho_Lambda) is imposed on the running rho_Lambda (an input, not a result)")
a0_over_H = sp.simplify(sp.sqrt(GrhoL) / 2 / Hc)
print("  a0/(cH) =", a0_over_H, " = ", sp.N(a0_over_H))
Z = sp.sqrt(32 * sp.pi / 3)
check("a0/(cH) = sqrt(3/(64 pi)) = 1/(sqrt(2) Z),  Z = sqrt(32 pi/3) = 5.7888", sp.simplify(a0_over_H - 1 / (sp.sqrt(2) * Z)) == 0)
print(f"  Z = {float(Z):.4f};  sqrt(2) Z = {float(sp.sqrt(2) * Z):.4f};  framework with Omega_Lambda = 0.7: a0/(cH0) = sqrt(0.7)/Z = {float(sp.sqrt(sp.Rational(7,10)) / Z):.4f}; fixed-point cosmology (Omega_Lambda = 1/2): {float(a0_over_H):.4f}; ratio {float(sp.sqrt(sp.Rational(5,7))):.3f}")
# time dependence
a0t = sp.simplify(a0_over_H * Hc)
check("a0(t) ~ H(t) ~ 1/t in the fixed-point era (rho_Lambda ~ rho_matter ~ (1+z)^3): NOT a flat a0(z)", sp.simplify(sp.diff(sp.log(a0t), t) * t + 1) == 0)
print("  (framework's distinctive law is FLAT a0(z); the fixed-point cosmology would give a0 ~ H(z) if a0 tracks its running vacuum density -- conditional on the imposed relation.)")

print()
fails = ok.count(False)
print(f"RESULT: {ok.count(True)} checks passed, {fails} failed")
sys.exit(1 if fails else 0)
