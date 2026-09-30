#!/usr/bin/env python3
"""n04_conversion_and_crossover.py -- turning the de Sitter temperature structure into a MOND-type force law; crossover values; comparison LAST.

Two premise-dependent members are derived with all factors tracked (the derivation of the premises is NOT claimed):
  (i)  'excess temperature'  2 pi (T - T_Lambda) = g_N              (Deser-Levin / Milgrom-type subtraction; lane E, Part A)
  (ii) 'Killing-normalisation split' G_eff = G / sin(theta)          (n03 C5: heat with kappa_obs, temperature the acceleration part T_U only)
       which is identical to Milgrom's other functional  2 pi a dT/da = g_N.
Here a = body's proper acceleration (INPUT identification), g_N = GM/r^2 (Newtonian field of the baryons), H = de Sitter Hubble rate.
D1 identities (ii);  D2 identities (i);  D3 asymptotics (Newtonian tail);  D4 crossover measures;  D5 numbers (comparison only AFTER the derivation is fixed);
D6 pi-parity: a0/H rational  =>  no member can equal the framework's 1/Z.
Exit 0 = all pass.
"""
import sys
import sympy as sp
import mpmath as mp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")
def must_fail(name, cond):
    ok.append(not bool(cond)); print(f"  [{'OK' if not cond else 'FAIL'}] CONTROL (wrong claim must be rejected): {name}")

a, H, g = sp.symbols('a H g', positive=True)
x = sp.symbols('x', positive=True)
T = sp.sqrt(a**2 + H**2) / (2 * sp.pi)
TL = H / (2 * sp.pi)
sinth = a / sp.sqrt(a**2 + H**2)

print("D1  member (ii): G_eff = G/sin(theta)")
check("D1a 2 pi a dT/da = a sin(theta) = a^2/sqrt(a^2+H^2)   (Milgrom's 'a dT/da' functional = the Killing-split member)",
      sp.simplify(2 * sp.pi * a * sp.diff(T, a) - a * sinth) == 0)
gN_ii = a**2 / sp.sqrt(a**2 + H**2)                           # a = G_eff M/r^2 = g_N / sin(theta)  =>  g_N = a sin(theta)
check("D1b a = g_N/sin(theta)  <=>  g_N = a^2/sqrt(a^2+H^2)", sp.simplify(gN_ii - a * sinth) == 0)
a_ii = sp.sqrt((g**2 + sp.sqrt(g**4 + 4 * g**2 * H**2)) / 2)
u2 = (g**2 + sp.sqrt(g**4 + 4 * g**2 * H**2)) / 2            # candidate a^2;  g = a^2/sqrt(a^2+H^2)  <=>  a^4 - g^2 a^2 - g^2 H^2 = 0 (a^2 > 0 root)
check("D1c inverse: a^2 = [g^2 + sqrt(g^4 + 4 g^2 H^2)]/2 solves a^4 = g^2 (a^2 + H^2)  (positive root)", sp.simplify(u2**2 - g**2 * (u2 + H**2)) == 0
      and all(abs(float(gN_ii.subs({a: a_ii.subs({g: gv, H: 1.7}), H: 1.7}).evalf()) - gv) < 1e-12 for gv in (0.01, 0.3, 1.0, 25.0)))
mu_ii = sp.simplify(gN_ii / a)                                # g_N = a mu(a/a0), a0 = H
check("D1d mu(x) = x/sqrt(1+x^2) with x = a/H  (the 'standard' MOND function), slope 1 at 0  =>  a0 = H",
      sp.simplify(mu_ii.subs(a, x * H) - x / sp.sqrt(1 + x**2)) == 0 and sp.limit(x / sp.sqrt(1 + x**2) / x, x, 0) == 1)
check("D1e deep limit  a^2 -> g H  (a0 = H)", sp.simplify(sp.limit(a_ii**2 / (g * H), g, 0, '+') - 1) == 0)
check("D1f Newtonian tail: a - g -> H^2/(2g)", sp.simplify(sp.limit((a_ii - g) * g / H**2, g, sp.oo) - sp.Rational(1, 2)) == 0)

print("D2  member (i): 2 pi (T - T_Lambda) = g_N")
gN_i = 2 * sp.pi * (T - TL)
a_i = sp.sqrt(g**2 + 2 * H * g)
check("D2a inverse: a = sqrt(g^2 + 2 H g) solves sqrt(a^2+H^2) - H = g  (a^2 + H^2 = (g+H)^2)", sp.simplify(a_i**2 + H**2 - (g + H)**2) == 0
      and all(abs(float((gN_i * 2 * sp.pi).subs({a: a_i.subs({g: gv, H: 1.7}), H: 1.7}).evalf()) - 2 * float(sp.pi) * gv) < 1e-12 * max(1, gv) for gv in (0.01, 0.3, 1.0, 25.0)))
check("D2b deep limit: a^2 -> 2 H g  (a0 = 2H); slope of g_N(a) at 0 is a^2/(2H)", sp.simplify(sp.limit(a_i**2 / (g * H), g, 0, '+') - 2) == 0)
check("D2c Newtonian tail: a - g -> H (a CONSTANT offset of size H), next term -H^2/(2g)",
      sp.simplify(sp.limit(a_i - g, g, sp.oo) - H) == 0 and sp.simplify(sp.limit((a_i - g - H) * g, g, sp.oo) + H**2 / 2) == 0)
mu_i = sp.simplify(gN_i / a).subs(a, x * 2 * H)               # a0 = 2H
check("D2d mu(x) = (sqrt(1+4x^2)-1)/(2x)  with x = a/(2H)  (Milgrom 1999 eq 8-9 form)", sp.simplify(mu_i - (sp.sqrt(1 + 4 * x**2) - 1) / (2 * x)) == 0)
must_fail("D2e the two members coincide", sp.simplify(gN_i - gN_ii) == 0)

print("D3  what the Newtonian tail means (definition-independent consequences)")
check("D3a member (ii): correction is O(H^2/g): relative size (H/g)^2/2  -> quadratically small at high acceleration", sp.simplify(sp.limit((a_ii / g - 1) * g**2 / H**2, g, sp.oo) - sp.Rational(1, 2)) == 0)
check("D3b member (i): relative correction H/g: LINEAR, a fixed extra acceleration H everywhere at high g", sp.simplify(sp.limit((a_i / g - 1) * g / H, g, sp.oo) - 1) == 0)

Tmut = sp.sqrt(a**2 + 4 * H**2) / (2 * sp.pi)                # mutated structure: T^2 = (a^2 + 4 H^2)/(4 pi^2)
slope_mut = sp.limit(sp.simplify(2 * sp.pi * a * sp.diff(Tmut, a)) / (a**2 / H), a, 0, '+')     # = 1/2 for this mutation (slope of g_N(a) at 0, in units of a^2/H); the true structure gives 1
must_fail("D3c a mutated temperature structure (a^2 + 4H^2) would still give a0 = H for member (ii)", sp.simplify(slope_mut - 1) == 0)
must_fail("D3d the two members have the same Newtonian tail (constant offset)", sp.simplify(sp.limit(a_ii - g, g, sp.oo) - sp.limit(a_i - g, g, sp.oo)) == 0)

print("D4  crossover measures (all O(H); the T-structure contains exactly ONE model-free scale)")
check("D4a T_U = T_Lambda  <=>  a = H  (theta = 45 deg): the only crossover in the temperature structure itself", sp.solve(sp.Eq(a / (2 * sp.pi), H / (2 * sp.pi)), a) == [H])
sol_i = sp.solve(sp.Eq(gN_i, a / 2), a)
sol_ii = sp.solve(sp.Eq(gN_ii, a / 2), a)
check("D4b half-point mu = 1/2:  (i) a = 4H/3,  (ii) a = H/sqrt(3)", [sp.simplify(s_) for s_ in sol_i] == [sp.Rational(4, 3) * H] and [sp.simplify(s_) for s_ in sol_ii] == [H / sp.sqrt(3)])
print("     slope-defined a0: (i) 2H, (ii) H;  half-point: (i) 1.333H, (ii) 0.577H;  T_U=T_Lambda: H.  The value depends on the (input) functional, not on T.")

print("D7  the LITERAL insertion: exact dS temperature into Jacobson's flat-space steps (heat with kappa = a, T = kappa_obs/2pi): G_eff = G sin(theta)")
gm = sp.symbols('g_N', positive=True)
# Jacobson bookkeeping (n03 C5 pair (a,kobs)):  a = G_eff M/r^2 = g_N sin(theta(a)) = g_N a/sqrt(a^2+H^2)  =>  a = 0  or  sqrt(a^2+H^2) = g_N
sol_lit = sp.solve(sp.Eq(a, gm * a / sp.sqrt(a**2 + H**2)), a)
check("D7a nonzero solution: a^2 = g_N^2 - H^2, real only for g_N >= H", [sp.simplify(s_**2 - (gm**2 - H**2)) for s_ in sol_lit] == [0] * len(sol_lit) and len(sol_lit) >= 1)
# Verlinde-type screen with the exact temperature: F = 2 pi m T = m sqrt(a^2+H^2) balances m g_N  (n03 C3c)
check("D7b Verlinde-type screen (Delta S = 2 pi m Delta x, T = A5/2pi, F = m g_N) gives the SAME relation sqrt(a^2+H^2) = g_N: two bookkeepings, one law",
      sp.simplify(sp.solve(sp.Eq(sp.sqrt(a**2 + H**2), gm), a)[0]**2 - (gm**2 - H**2)) == 0)
check("D7c below g_N = H the root is imaginary (a = 0 only): a sharp threshold at g_N = H, NOT an enhancement -- opposite to MOND",
      sp.simplify(sp.sqrt(gm**2 - H**2).subs(gm, H)) == 0 and sp.simplify(sp.im(sp.sqrt(gm**2 - H**2).subs(gm, H / 2))) != 0)
Gr = sp.simplify(sinth)
check("D7d G_eff/G = a/sqrt(a^2+H^2): 1/sqrt(2) at a = H, -> a/H (gravity switched off) as a -> 0", sp.simplify(Gr.subs(a, H) - 1 / sp.sqrt(2)) == 0 and sp.simplify(sp.limit(Gr / (a / H), a, 0, '+') - 1) == 0)
Zv = sp.sqrt(32 * sp.pi / 3)
th0 = sp.atan(1 / Zv)
print(f"     (for scale: the framework's a0/H = 1/Z sits at theta_0 = arctan(1/Z) = {float(th0*180/sp.pi):.2f} deg, sin(theta_0) = {float(sp.sin(th0)):.4f}; the T-structure singles out theta = 45 deg only)")

print("D5  numbers -- comparison only now, nothing tuned")
mp.mp.dps = 20
c = mp.mpf(299792458); Mpc = mp.mpf('3.0856775814913673e22')
H0 = 67.4e3 / Mpc; OmL = mp.mpf('0.685')
HL = H0 * mp.sqrt(OmL)
Z = mp.sqrt(32 * mp.pi / 3)
a0_sparc = mp.mpf('1.2e-10')                                   # value quoted in lane E e03 (SPARC-type a0), used only as a yardstick
print(f"     c H0 = {float(c*H0):.4e} m/s^2 (H0=67.4)  c H_Lambda = {float(c*HL):.4e}   Z = sqrt(32 pi/3) = {float(Z):.4f}")
tab = [("thermo member (ii): c H", 1), ("thermo member (i):  2 c H", 2), ("Milgrom empirical c H/2pi", 1 / (2 * mp.pi)), ("framework c H/Z", 1 / Z)]
for nm, q in tab:
    for foot, Hf in [("H0", H0), ("H_Lambda", HL)]:
        v = q * c * Hf
        print(f"     {nm:<30s} [{foot:>8s}] = {float(v):.3e} m/s^2   /SPARC(1.2e-10) = {float(v/a0_sparc):6.2f}")
fw_H0, fw_HL = c * H0 / Z, c * HL / Z
check("D5a framework values reproduce the record's two footings: 1.13e-10 (H0) and 9.36e-11 (H_Lambda)", abs(fw_H0 / 1.13e-10 - 1) < 0.005 and abs(fw_HL / 9.36e-11 - 1) < 0.005)
check("D5b member (ii) / framework = Z = 5.789 exactly; member (i) / framework = 2Z = 11.58 (footing-independent)", abs(1 / (1 / Z) - Z) < 1e-12 and abs(2 * Z / Z - 2) < 1e-12)
check("D5c member (ii) is 4.5-5.5x above the SPARC yardstick, member (i) 9-11x (both footings)",
      4.4 < c * HL / a0_sparc < 4.7 and 5.3 < c * H0 / a0_sparc < 5.6 and 8.9 < 2 * c * HL / a0_sparc < 9.2 and 10.8 < 2 * c * H0 / a0_sparc < 11.1)
must_fail("D5e member (ii) lies within 30% of the SPARC yardstick on either footing", abs(c * H0 / a0_sparc - 1) < 0.3 or abs(c * HL / a0_sparc - 1) < 0.3)
sqrtGrho_over_H = mp.sqrt(3 / (8 * mp.pi))                     # sqrt(G rho_L)/H_L
for nm, q in [("member (ii)", 1), ("member (i)", 2), ("framework", 1 / Z)]:
    print(f"     a0/sqrt(G rho_L):  {nm:<12s} = {float(q / sqrtGrho_over_H):.4f}")
check("D5d in the pi-free variable: member (ii) a0/sqrt(G rho_L) = sqrt(8 pi/3) = 2.894 (the record's 'forced kernel' Z), member (i) = 2 sqrt(8pi/3) = 5.789, framework 1/2",
      abs(1 / sqrtGrho_over_H - mp.sqrt(8 * mp.pi / 3)) < 1e-12 and abs(mp.sqrt(8 * mp.pi / 3) - 2.894) < 1e-3 and abs(2 * mp.sqrt(8 * mp.pi / 3) - Z) < 1e-12)
print("     NOTE: 2 sqrt(8pi/3) = Z is an arithmetic coincidence of definitions (Z := 2 sqrt(8pi/3)); it is NOT a sign that member (i) 'contains' the framework: "
      "member (i) is a0 = 2H, the framework is a0 = H/Z.")
Solar = {"g at Saturn (GM_sun/r^2, r = 9.58 AU)": mp.mpf('1.32712440018e20') / (9.58 * mp.mpf('1.495978707e11'))**2}
gS = Solar["g at Saturn (GM_sun/r^2, r = 9.58 AU)"]
print(f"     Solar-System scale (NOT compared with any ephemeris bound here):  g(Saturn) = {float(gS):.3e} m/s^2;  extra a: member (i) = c H0 = {float(c*H0):.2e};  member (ii) = (cH0)^2/(2g) = {float((c*H0)**2/(2*gS)):.2e} m/s^2")

print("D6  pi-parity: any horizon-first member has a0 = q H with q rational; the framework needs q = 1/Z")
q = sp.symbols('q', positive=True)
kappa_fw = sp.Rational(1, 2)
qsol = sp.solve(sp.Eq(q * sp.sqrt(8 * sp.pi / 3), kappa_fw), q)[0]          # a0/sqrt(G rho) = q sqrt(8 pi/3) = kappa
check("D6a q needed = 1/Z = sqrt(3/(32 pi)), q^2 = 3/(32 pi)", sp.simplify(qsol**2 - 3 / (32 * sp.pi)) == 0)
mp.mp.dps = 40
rel = mp.pslq([mp.pi, 1], maxcoeff=10**6, maxsteps=10**6)
check("D6b q^2 = 3/(32 pi) is not rational: no integer relation between pi and 1 (Lindemann; PSLQ finds none up to 1e6)  =>  no rational q, so no member with a0 = q H equals the framework", rel is None)
check("D6c CONTROL: PSLQ does find a relation for a rational-multiple pair (detects when a relation exists)", mp.pslq([mp.mpf(3) / 4, mp.mpf(1)], maxcoeff=10**6) is not None)
check("D6d members (i), (ii) have q = 2, 1: a0^2/(G rho_L) = q^2 (8 pi/3) = 32 pi/3 and 8 pi/3 (one factor of pi each); the framework's value is 1/4 (none)",
      sp.simplify(4 * 8 * sp.pi / 3 - 32 * sp.pi / 3) == 0 and mp.pslq([mp.pi, mp.mpf(1)], maxcoeff=10**6, maxsteps=10**6) is None)

n, npass = len(ok), sum(ok)
print(f"\nn04: {npass}/{n} checks passed")
sys.exit(0 if npass == n else 1)
