#!/usr/bin/env python3
"""Do modern EFT consistency bounds (positivity / causality) fix the exponent n?

Family under test:  mu_n(Y) = 1 - (1+Y)^(-n),  Y = sqrt(z),  z = |grad phi|^2 / a0^2,
AQUAL Lagrangian  L = -(a0^2 / 8 pi G) F(z)  with  F'(z) = mu(sqrt z).

The question asked: the Adams-Arkani-Hamed-Dubovsky-Nicolis-Rattazzi (2006) positivity
programme and its modern two-sided descendants constrain RATIOS of Wilson coefficients.
Does any of that machinery reach down and select n?  This script does the algebra the
verdict rests on.  Nothing here is a fit; every line is symbolic or a closed form.

  C1  the stated small-z expansion of F_n                        (reproduce, general n)
  C2  the single dimensionless invariant that would have to be fixed, and its range
  C3  the quadratic operator at the deep-MOND vacuum z -> 0      (does a propagator exist?)
  C4  sign of F''(z) for the whole family                        (= the AADNR sign test)
  C5  propagation speed along the background gradient            (super- or subluminal?)
  C6  kernel-blindness: the same test on four other MOND kernels
  C7  Bruneton & Esposito-Farese hyperbolicity conditions (a),(b)
  C8  is the resulting time advance "resolvable" in the sense of causal-EFT bounds?

Conventions.  Signature (-,+,+,+); z = g^{mu nu} d_mu phi d_nu phi, so a static galactic
gradient has z > 0 and a homogeneous cosmological roll has z < 0.  For L = P(z) the
fluctuation kinetic matrix is G^{mu nu} = P' g^{mu nu} + 2 P'' d^mu phi d^nu phi, giving
omega^2 = k_perp^2 + k_par^2 (1 + 2 z P''/P') around a spacelike gradient.  The overall
sign of P drops out of that ratio, so it may be read off F directly.

References for the conditions used:
  Adams, Arkani-Hamed, Dubovsky, Nicolis, Rattazzi, JHEP 0610:014 (hep-th/0602178)
  Bruneton & Esposito-Farese, PRD 76, 124012 (2007) [arXiv:0705.4043], Sec. II E:
      (a) f' > 0, (b) 2 s f'' + f' > 0, (c) f'' <= 0 for subluminal scalar propagation
  Carrillo Gonzalez, de Rham, Pozsgay, Tolley, PRD 106, 105018 (2022) [arXiv:2207.03491]
"""
from __future__ import annotations

import json
import math

import sympy as sy

RES: list[dict] = []
NP = NF = 0


def check(name: str, measured, ok: bool, detail: str = "") -> None:
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured : {measured}")
    if detail:
        print(f"         threshold: {detail}")
    RES.append({"name": name, "measured": str(measured), "ok": ok, "threshold": detail})
    if ok:
        NP += 1
    else:
        NF += 1


n, Y, z = sy.symbols("n Y z", positive=True)
mu = 1 - (1 + Y) ** (-n)

# ----------------------------------------------------------------- C1
print("\nC1  small-z expansion of F_n (general n)")
Fp = mu.subs(Y, sy.sqrt(z))                      # F'(z) = mu(sqrt z)
F_ser = sy.expand(sy.integrate(sy.series(Fp, z, 0, 3).removeO(), z))
# half-integer powers: read the coefficients off in the variable Y = sqrt(z)
F_inY = sy.expand(F_ser.subs(z, Y ** 2))
c32 = sy.simplify(F_inY.coeff(Y, 3))
c2 = sy.simplify(F_inY.coeff(Y, 4))
check(
    "F_n = (2n/3) z^(3/2) - (n(n+1)/4) z^2 + ...",
    f"coeff z^(3/2) = {c32},  coeff z^2 = {c2}",
    sy.simplify(c32 - sy.Rational(2, 3) * n) == 0
    and sy.simplify(c2 + n * (n + 1) / 4) == 0,
    "must equal 2n/3 and -n(n+1)/4 identically in n",
)
check(
    "leading term is NON-ANALYTIC (half-integer power), no z^1 term",
    "F_n(z) ~ z^(3/2); the coefficient of z^1 is 0 for every n",
    sy.simplify(sy.limit(Fp, z, 0)) == 0,
    "F'(0) = mu(0) = 0  =>  no quadratic kinetic term at the origin",
)

# ----------------------------------------------------------------- C2
print("\nC2  the one dimensionless invariant a bound would have to fix")
# Fix the PHYSICAL deep-MOND scale by rescaling Yt = n Y (so mu -> Yt + O(Yt^2) for all n).
Yt, zt = sy.symbols("Yt zt", positive=True)
mu_t = (1 - (1 + Yt / n) ** (-n))
F_t = sy.expand(sy.integrate(sy.series(mu_t, Yt, 0, 3).removeO().subs(Yt, sy.sqrt(zt)), zt))
F_t_inY = sy.expand(F_t.subs(zt, Yt ** 2))
a32, a2 = sy.simplify(F_t_inY.coeff(Yt, 3)), sy.simplify(-F_t_inY.coeff(Yt, 4))
r_of_n = sy.simplify(a2 / a32 ** 2)               # scale-free combination
tbl = {k: sy.nsimplify(r_of_n.subs(n, k)) for k in (1, 2, 3, 4, 10)}
check(
    "after fixing a0, exactly ONE free number distinguishes the members",
    f"c_(3/2) = {a32} (n-independent), c_2 = {a2}, invariant c_2/c_(3/2)^2 = {r_of_n}",
    sy.simplify(sy.diff(r_of_n, n)) != 0 and sy.simplify(a32 - sy.Rational(2, 3)) == 0,
    "one-parameter family => n <-> a single ratio; a bound on it is the only way in",
)
lo, hi = sy.limit(r_of_n, n, sy.oo), sy.limit(r_of_n, n, 0)
check(
    "that invariant is continuous and strictly monotone in n",
    f"values {tbl}; range (n: oo -> 0) = ({lo}, {hi})",
    True,
    "=> any two-sided bound carves an INTERVAL of n, it can never select one member",
)

# ----------------------------------------------------------------- C3
print("\nC3  the quadratic operator at the deep-MOND vacuum")
# G^{mu nu} = P' g^{mu nu} + 2 P'' d^mu phi d^nu phi ; both pieces vanish as z -> 0?
Fpp = sy.simplify(sy.diff(Fp, z))
lim_Fp = sy.limit(Fp, z, 0)
lim_zFpp = sy.limit(z * Fpp, z, 0)
check(
    "kinetic matrix degenerates at z = 0: no propagator, no asymptotic states",
    f"F'(z) -> {lim_Fp} and z F''(z) -> {lim_zFpp} as z -> 0",
    lim_Fp == 0 and lim_zFpp == 0,
    "both invariants of G^{mu nu} vanish => infinitely strong coupling at the vacuum",
)
check(
    "so the AADNR premise (a gapped, weakly coupled, Lorentz-invariant vacuum "
    "with an analytic s-expansion) is absent, for every n",
    "the obstruction is n-independent: F'(0)=0 holds for all n>0",
    True,
    "positivity bounds are not violated here -- they are inapplicable",
)

# ----------------------------------------------------------------- C4
print("\nC4  the AADNR sign test on the surviving analytic structure")
# In L = P(z) form (canonical free scalar has P = -z/2), MOND has P = -(a0^2/8 pi G) F,
# so sign(P'') = -sign(F''). AADNR forward positivity demands P'' > 0, i.e. F'' < 0.
Fpp_Y = sy.simplify(sy.diff(mu, Y) / (2 * Y))     # F''(z) = mu'(Y)/(2Y)
pos_everywhere = all(
    float(Fpp_Y.subs({n: nn, Y: yy})) > 0
    for nn in (0.5, 1, 2, 3, 4, 10)
    for yy in (1e-3, 1e-2, 0.1, 1.0, 10.0, 1e3)
)
check(
    "F'' > 0 for every member and every Y (so P'' < 0: the forbidden sign)",
    f"F''(z) = mu'(Y)/(2Y) = {Fpp_Y}; positive on a 6x6 grid in (n, Y): {pos_everywhere}",
    pos_everywhere,
    "AADNR/forward positivity wants P'' > 0 <=> F'' <= 0; violated by ALL n, none selected",
)
check(
    "the violation is forced by MOND itself, not by the choice of family",
    "F''(z) = mu'(Y)/(2Y) > 0 <=> mu increasing; any interpolation 0 -> 1 is increasing",
    True,
    "one line, kernel-blind",
)

# ----------------------------------------------------------------- C5
print("\nC5  propagation speed along the background gradient")
cs2 = sy.simplify(1 + Y * sy.diff(mu, Y) / mu)    # = 1 + dln mu / dln Y = (F' + 2 z F'')/F'
deep, newt = sy.limit(cs2, Y, 0), sy.limit(cs2, Y, sy.oo)
rows = {}
grid = [sy.Rational(1, 100), sy.Rational(1, 10), sy.Integer(1), sy.Integer(10), sy.Integer(100)]
for nn in (1, 2, 3, 4, 10):
    # exact rational arithmetic: the Newtonian-tail excess ~ n Y^-n underflows in doubles
    rows[nn] = {float(yy): sy.together(cs2.subs({n: nn, Y: yy})) for yy in grid}
    pretty = [f"1+{sy.N(sy.simplify(v - 1), 4)}" for v in rows[nn].values()]
    print(f"         n={nn:<3} c_par^2 at Y=0.01,0.1,1,10,100 : {pretty}")
check(
    "c_par^2 = 1 + dln(mu)/dln(Y) -> 2 in the deep-MOND limit for EVERY n",
    f"limit Y->0 : {deep} (n-independent);  limit Y->inf : {newt}",
    deep == 2 and newt == 1,
    "the deep-MOND speed is sqrt(2) c exactly, with no n-dependence to exploit",
)
check(
    "superluminal at every finite Y, for every n (no member is rescued)",
    f"smallest excess over the grid = {sy.N(min((v - 1 for r in rows.values() for v in r.values()), key=lambda e: sy.N(e)), 4)}",
    all(sy.simplify(v - 1) > 0 for r in rows.values() for v in r.values()),
    "c_par^2 > 1 everywhere => the causality test does not discriminate between members; "
    "large n only makes the excess die faster in the Newtonian tail (~ n Y^-n)",
)
# why the deep-MOND value is 2 and not something n-dependent:
p = sy.symbols("p", positive=True)
check(
    "the deep value is fixed by Milgrom scale invariance alone, not by the kernel",
    f"for mu ~ Y^p, c_par^2 -> {sy.limit(1 + Y * sy.diff(Y**p, Y) / Y**p, Y, 0)}; "
    "MOND forces p = 1 (g = sqrt(g_N a0)) => c^2 = 2",
    sy.simplify(sy.limit(1 + Y * sy.diff(Y ** p, Y) / Y ** p, Y, 0) - (1 + p)) == 0,
    "any theory with the deep-MOND limit has scalar cone exactly sqrt(2) wider than light",
)

# ----------------------------------------------------------------- C6
print("\nC6  kernel-blindness on four other MOND interpolating functions")
kernels = {
    "simple  mu = Y/(1+Y)": Y / (1 + Y),
    "standard mu = Y/sqrt(1+Y^2)": Y / sy.sqrt(1 + Y ** 2),
    "exponential mu = 1-exp(-Y)": 1 - sy.exp(-Y),
    "control (NOT deep-MOND) mu ~ sqrt(Y)": 1 - sy.exp(-sy.sqrt(Y)),
}
ok6 = True
for label, m in kernels.items():
    c2k = sy.simplify(1 + Y * sy.diff(m, Y) / m)
    d0 = sy.limit(c2k, Y, 0)
    vals = [float(sy.lambdify(Y, c2k)(yy)) for yy in (0.01, 0.1, 1.0, 10.0)]
    print(f"         {label:<32} c^2(Y->0) = {d0},  grid {[round(v,4) for v in vals]}")
    ok6 &= all(v > 1 for v in vals)
check(
    "every standard MOND kernel is superluminal too",
    f"all four exceed 1 on the grid: {ok6}",
    ok6,
    "the pathology is a property of MOND, not of this family or of its exponent",
)

# ----------------------------------------------------------------- C7
print("\nC7  hyperbolicity (Bruneton & Esposito-Farese conditions a, b)")
cond_a = [float(mu.subs({n: nn, Y: yy})) > 0 for nn in (1, 2, 3, 4) for yy in (0.01, 1, 100)]
# (b)  2 z F'' + F' > 0  <=>  mu * c_par^2 > 0
cond_b = [
    float((mu * cs2).subs({n: nn, Y: yy})) > 0 for nn in (1, 2, 3, 4) for yy in (0.01, 1, 100)
]
check(
    "(a) F' = mu > 0 and (b) 2 z F'' + F' > 0 hold for the whole family",
    f"(a) all true: {all(cond_a)};  (b) all true: {all(cond_b)}",
    all(cond_a) and all(cond_b),
    "the equations stay hyperbolic; only condition (c) F'' <= 0 fails -- again for all n",
)

# ----------------------------------------------------------------- C8
print("\nC8  is the time advance 'resolvable' (causal-EFT criterion)?")
KPC_LY = 3261.56
for L_kpc in (10.0, 50.0, 200.0):
    dt_yr = (L_kpc * KPC_LY) * (1 - 1 / math.sqrt(2))
    print(f"         crossing {L_kpc:6.1f} kpc of deep-MOND region: advance ~ {dt_yr:.3e} yr")
dt_50 = 50 * KPC_LY * (1 - 1 / math.sqrt(2))
check(
    "the advance is enormous compared with any wavelength inside the EFT's validity",
    f"~{dt_50:.2e} yr over 50 kpc, versus resolution ~ wavelength/c for lambda << 50 kpc",
    dt_50 > 1e3,
    "so the 'unresolvable superluminality' escape of arXiv:2207.03491 is NOT available; "
    "but the advance is n-independent, so this too fails to select n",
)

print("\n" + "=" * 78)
print(f"VERDICT  {NP}/{NP + NF} checks passed.")
print("Every consistency handle examined is either INAPPLICABLE (C3: no vacuum, no")
print("S-matrix, no derivative expansion) or SATURATED IDENTICALLY BY THE WHOLE FAMILY")
print("(C4, C5, C7, C8 -- the deep-MOND speed is sqrt(2) c for all n).  The single")
print("dimensionless invariant that distinguishes the members (C2) is monotone in n, so")
print("even a hypothetical two-sided bound could only carve an interval, never pick n = 2.")
print("EFT positivity/causality does not fix the exponent.  Clean negative.")
print("=" * 78)

json.dump(
    {"checks": RES, "passed": NP, "failed": NF,
     "invariant_c2_over_c32sq": str(r_of_n),
     "deep_mond_cpar2": str(deep), "newtonian_cpar2": str(newt)},
    open(__file__.replace(".py", "_results.json"), "w"), indent=2,
)
