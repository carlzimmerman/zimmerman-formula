"""p20a: effective-metric machinery and branch A1 (the cosmological sound horizon). Criteria: SETUP.md (frozen first).
Machinery: for L = P(X), X = -(1/2) g^{mn} d_m phi d_n phi, perturbations see G^{mn} = P_X g^{mn} - P_XX d^m phi d^n phi; on a timelike background the
sound speed is c_s^2 = P_X/(P_X + 2 X P_XX). Checked: canonical P = X -> 1; P = X^n -> 1/(2n-1); DBI.
A1: homogeneous rolling phi(t) in de Sitter (H^2 = Lambda/3): the acoustic metric is de Sitter with horizon r_h = c_s/H; kappa (Killing vector unit at the origin)
= H, so kappa r_h = c_s; with the acoustic-time normalisation kappa = H/c_s, kappa r_h = 1. Test against kappa r = 1/2 and Lambda r^2 = 8 pi.
Run: python3 p20a_machinery_A1.py  |  MUTATE=1: drop the factor 2 in c_s^2 (check M2 must fail)
"""
import os, sys
import sympy as sp
MUTATE = os.environ.get("MUTATE") == "1"
X, n, b, cs, H, L = sp.symbols("X n b c_s H Lambda", positive=True)
res = []
def check(nm, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + nm)
two = 1 if MUTATE else 2
cs2 = lambda P: sp.simplify(sp.diff(P, X) / (sp.diff(P, X) + two * X * sp.diff(P, X, 2)))
check("M1 canonical P = X: c_s^2 = 1", sp.simplify(cs2(X) - 1) == 0)
check("M2 P = X^n: c_s^2 = 1/(2n - 1)", sp.simplify(cs2(X**n) - 1 / (2 * n - 1)) == 0)
check("M3 DBI P = -b sqrt(1 - 2X/b): c_s^2 = 1 - 2X/b", sp.simplify(cs2(-b * sp.sqrt(1 - 2 * X / b)) - (1 - 2 * X / b)) == 0)

# A1: acoustic metric ds^2 = -c_s^2 dt^2 + e^{2Ht} dx^2 -> static form; horizon where the static g_tt vanishes
r, t = sp.symbols("r t", positive=True)
gtt_static = -(cs**2 - H**2 * r**2)             # acoustic static patch: -(c_s^2 - H^2 r^2) dt^2 + ...
rh = sp.solve(sp.Eq(gtt_static, 0), r)[0]
kap_t = sp.Abs(sp.simplify(sp.diff(-gtt_static, r).subs(r, rh) / (2 * cs)))   # magnitude (cosmological horizon: g_tt falls outward)   # surface gravity for d_t (normalised so g_tt -> -c_s^2 at the origin: unit in acoustic proper time)
kap_T = sp.simplify(kap_t / cs)
print(f"   A1: r_h = {rh}; kappa (d_t) = {kap_t}; kappa (acoustic time) = {kap_T}; kappa r_h = {sp.simplify(kap_t*rh)} / {sp.simplify(kap_T*rh)}")
sol_cs = sp.solve(sp.Eq(L * rh**2, 8 * sp.pi).subs(H, sp.sqrt(L / 3)), cs)
print(f"   Lambda r_h^2 = 8 pi needs c_s = {sol_cs} = {[float(s) for s in sol_cs]} (in units of c)")
check("A1-1 the area condition Lambda r_h^2 = 8 pi needs a SUPERLUMINAL sound speed (c_s = sqrt(8 pi/3) = 2.894 c): violates criterion 4",
      all(float(s) > 1 for s in sol_cs))
kr = [sp.simplify(kap_t * rh), sp.simplify(kap_T * rh)]
check(f"A1-2 kappa r_h = {kr[0]} or {kr[1]} (both normalisations): never 1/2 at the c_s the area needs -> A1 FAILS criterion 1",
      all(abs(abs(float(k.subs(cs, sol_cs[0]).subs(H, 1))) - 0.5) > 0.1 for k in kr))
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
