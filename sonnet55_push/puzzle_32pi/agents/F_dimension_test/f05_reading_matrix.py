#!/usr/bin/env python3
"""f05_reading_matrix.py -- the record's five d-dependences of kappa, re-derived, extended by what f01-f04 determine, and put through gates.

kappa(d) is defined by a0 = kappa c sqrt(G_D rho_L) (G_D the Einstein coupling).  Z_d = c H/a0 = Z_f(d)/kappa(d) with the forced kernel
Z_f(d) = R*/L = 4 sqrt(pi/(d(d-1)))  (from H^2 = 16 pi G rho/(d(d-1)), f01).  Convention-free quantity: Z_d (or a0/(c^2 sqrt(Lambda))).

Candidates (name -> kappa(d)); 'D' = what physics fixes, 'P' = a premise or choice that the physics does not fix:
  R1   two static channels, COUNT = 2 in every d (PD02)                          kappa = 1/2              count D (f01 D1: numerator -2 for all d); kappa = 1/count is P
  R1w  the two channels carry weights 1 : 1/(d-2) (f01 B-L); weighted count      kappa = (d-2)/(d-1)      NOT in the record; shows count vs weighted count is P
  R2   record's PD11 'Tolman count d-1'                                          kappa = 1/(d-1)          MIS-GENERALISED (f01 D2): rho + d p is not the D-dim active density
  R2c  D-dim Tolman/Komar count normalised to dust, 2/(d-2)                      kappa = (d-2)/2          D (f01 A) ; kappa = 1/count is P
  R3   Tangherlini surface gravity at r_s = R* = c/sqrt(G rho_L)                 kappa = (d-2)/2          kappa_sg D (f01 C-kBH); r_s = R* is P (r_s = 1/H is D but misses d=3)
  R3h  same d=3 statement 'K_Sigma = rho' as horizon Ricci scalar = Lambda/4pi   kappa = sqrt((d-2)/(2(d-1)))  P (equally natural extension of the d=3 formula)
  R4   enthalpy premise (2/3) d/(d+1)                                            kappa = (2/3) d/(d+1)    the 2/3 and the bath are P (M5-B, its own leak)
  R5   fixed Z (the ratio cH/a0 is d-independent)                                kappa = sqrt(3/(2d(d-1)))  P
  R6   kappa = 1/2 in units of the NEWTONIAN coupling G_N = 2(d-2)G_D/(d-1)      kappa = (1/2) sqrt(2(d-2)/(d-1))  P (convention of G)
  RV   volume-law elastic reading, derived in f03                                Z_V = d(d-1)/(d-2)       D given its heuristic premises; NOT 1/2 at d = 3
Gates:  F flat curve with the fixed s=1 kernel (f02) ; P pi-count of the topological form (f04) ; E the a0-horizon is an object of its own Lambda universe
(Schwarzschild-Tangherlini-de Sitter has a horizon: mass <= Nariai mass, generalising p06) ; N the MOND transition radius of a fixed mass stays finite as d -> 2+
(the Newtonian force itself vanishes there) ; the dim SO(d) identity.
Exit 0 = the table is what it says, gates computed, controls behave.
"""
import sys
import math
import itertools
import numpy as np
import sympy as sp

OK = []
def check(name, cond):
    OK.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")

d = sp.symbols('d', positive=True)
Zf = 4 * sp.sqrt(sp.pi / (d * (d - 1)))
cands = {
    "R1  two channels (count 2)":        sp.Rational(1, 2) + 0 * d,
    "R1w weighted channels":             (d - 2) / (d - 1),
    "R2  Tolman 'd-1' (record)":         1 / (d - 1),
    "R2c Tolman D-dim, dust-norm.":      (d - 2) / 2,
    "R3  Tangherlini, r_s = R*":         (d - 2) / 2,
    "R3h horizon Ricci scalar = L/4pi":  sp.sqrt((d - 2) / (2 * (d - 1))),
    "R4  enthalpy premise":              sp.Rational(2, 3) * d / (d + 1),
    "R5  fixed Z":                       sp.sqrt(sp.Rational(3, 2) / (d * (d - 1))),
    "R6  kappa=1/2 in G_N units":        sp.Rational(1, 2) * sp.sqrt(2 * (d - 2) / (d - 1)),
    "RV  volume-law (derived, f03)":     Zf / (d * (d - 1) / (d - 2)),
}

# ------------------------------------------------------------------ derivations of the two new extensions
print("Derivations")
rs, Lam, Gr = sp.symbols('r_s Lambda Gr', positive=True)
# R3h: horizon-sphere Ricci scalar (d-1)(d-2)/r_s^2 = Lambda/(4 pi); a0 = (d-2)/(2 r_s); kappa = a0/sqrt(Lambda/8pi)
r_s_val = sp.sqrt(4 * sp.pi * (d - 1) * (d - 2) / Lam)
a0_val = (d - 2) / (2 * r_s_val)
kap_h = sp.simplify(a0_val / sp.sqrt(Lam / (8 * sp.pi)))
check("R3h  (d-1)(d-2)/r_s^2 = Lambda/(4 pi)  =>  kappa = sqrt((d-2)/(2(d-1))); equals 1/2 at d = 3 (it IS the d = 3 statement K = rho, 2K = R_Sigma = Lambda/4 pi)",
      sp.simplify(kap_h**2 - (d - 2) / (2 * (d - 1))) == 0 and sp.simplify(kap_h.subs(d, 3) - sp.Rational(1, 2)) == 0)
# R6: a0 = 1/2 sqrt(G_N rho) with G_N = 2 (d-2) G_D/(d-1)
GN_over_GD = 2 * (d - 2) / (d - 1)
check("R6   kappa_D = (1/2) sqrt(G_N/G_D) = (1/2) sqrt(2(d-2)/(d-1)); equals 1/2 at d = 3", sp.simplify(sp.Rational(1, 2) * sp.sqrt(GN_over_GD) - cands["R6  kappa=1/2 in G_N units"]) == 0 and sp.simplify(GN_over_GD.subs(d, 3)) == 1)
check("R1w  Phi:Psi = (d-2):1 (f01 B) so the summed lensing weight relative to Phi is (d-1)/(d-2); kappa = its inverse = (d-2)/(d-1); equals 1/2 at d = 3",
      sp.simplify(1 / ((d - 1) / (d - 2)) - cands["R1w weighted channels"]) == 0 and sp.simplify(cands["R1w weighted channels"].subs(d, 3)) == sp.Rational(1, 2))
check("R3   with r_s = 1/H (the radius at which a rho-ball is its own Tangherlini horizon, f01 C-Hub) kappa_sg gives a0 = (d-2) H/2, i.e. Z = 2/(d-2) = 2 at d = 3, NOT the anchor Z = 5.789: excluded as a reading of the d=3 fact",
      sp.simplify((2 / (d - 2)).subs(d, 3) - 2) == 0 and abs(2 - math.sqrt(32 * math.pi / 3)) > 3)

# ------------------------------------------------------------------ the table
print("\nkappa(d)   [d = 2 and d = 4 are the controls]")
dl = list(range(2, 9))
print(f"  {'candidate':<34}" + "".join(f"{'d=' + str(x):>9}" for x in dl))
tab = {}
for nm, ex in cands.items():
    row = []
    for x in dl:
        try:
            v = float(ex.subs(d, x))
        except Exception:
            v = float('nan')
        row.append(v)
    tab[nm] = row
    print(f"  {nm:<34}" + "".join(f"{v:>9.4f}" for v in row))
at3 = {nm: float(ex.subs(d, 3)) for nm, ex in cands.items()}
check("T1  nine of the ten candidates equal exactly 1/2 at d = 3; only the volume-law RV does not (0.4824, Z = 6)",
      sum(abs(v - 0.5) < 1e-12 for v in at3.values()) == 9 and abs(at3["RV  volume-law (derived, f03)"] - 0.5) > 0.01)
spread4 = [tab[nm][2] for nm in tab]
check("T2  d = 4 control: the candidates spread over %.3f .. %.3f, so d = 3 cannot say which is right" % (min(spread4), max(spread4)), max(spread4) - min(spread4) > 0.5)
distinct = {nm for nm in cands if nm not in ("R2c Tolman D-dim, dust-norm.",)}
check("T3  R2c and R3 are the SAME function (d-2)/2: the D-dim Tolman/Komar count and the Tangherlini surface gravity agree for every d (both are the Gauss-law exponent d-2)",
      sp.simplify(cands["R2c Tolman D-dim, dust-norm."] - cands["R3  Tangherlini, r_s = R*"]) == 0)
check("T5  R3h and R6 are the SAME function sqrt((d-2)/(2(d-1))): 'horizon Ricci scalar = Lambda/4pi' and 'kappa = 1/2 in Newtonian-coupling units' coincide for every d",
      sp.simplify(cands["R3h horizon Ricci scalar = L/4pi"]**2 - cands["R6  kappa=1/2 in G_N units"]**2) == 0)
check("T4  R1 (count) and R2c/R3 (dust-normalised / horizon) separate for d != 3: 1/2 vs (d-2)/2 agree ONLY at d = 3", sp.solve(sp.Eq((d - 2) / 2, sp.Rational(1, 2)), d) == [3])


# ------------------------------------------------------------------ what class B (kappa = (d-2)/2) says geometrically
print("\nWhat R3 / R2c say geometrically")
rM, rS, Rst, Mm, Gd_, Om_, kk = sp.symbols('r_M r_s R_star M G_D Omega kappa', positive=True)
dsym = sp.symbols('dsym', positive=True)
# g_N(r) = 8 pi G (d-2) M /((d-1) Omega r^(d-1)),  r_s^(d-2) = 16 pi G M/((d-1) Omega)  =>  g_N = (d-2) r_s^(d-2)/(2 r^(d-1));  a0 = kappa/R*
gN_r = (dsym - 2) * rS**(dsym - 2) / (2 * rM**(dsym - 1))
sol_rM = sp.solve(sp.Eq(gN_r, kk / Rst), rM**(dsym - 1))
rM_pow = sp.simplify(sp.solve(sp.Eq((dsym - 2) * rS**(dsym - 2) / (2 * sp.Symbol('X', positive=True)), kk / Rst), sp.Symbol('X', positive=True))[0])
check("B-r  g_N(r_M) = a0 = kappa/R* gives r_M^(d-1) = (d-2) r_s^(d-2) R*/(2 kappa); kappa = (d-2)/2 is EXACTLY r_M^(d-1) = r_s^(d-2) R* (the d-dim form of the record's r_M^2 = r_s R*, no d-dependent coefficient); kappa = 1/2 gives coefficient (d-2)",
      sp.simplify(rM_pow - (dsym - 2) * rS**(dsym - 2) * Rst / (2 * kk)) == 0 and sp.simplify(rM_pow.subs(kk, (dsym - 2) / 2) - rS**(dsym - 2) * Rst) == 0 and sp.simplify(rM_pow.subs(kk, sp.Rational(1, 2)) - (dsym - 2) * rS**(dsym - 2) * Rst) == 0)

# ------------------------------------------------------------------ dim SO(d)
print("\ndim SO(d) lock")
kap = sp.symbols('kappa', positive=True)
dimSO = d * (d - 1) / 2
Zd2 = (Zf / kap)**2
check("S1  for ANY kappa: Z_d^2 dim SO(d) kappa^2 = 8 pi  (Friedmann: G_00 = dim SO(d) H^2 = 8 pi G rho)  -- dim SO(d) carries no information about kappa", sp.simplify(Zd2 * dimSO * kap**2 - 8 * sp.pi) == 0)
check("S2  the record's Z_d^2 = 32 pi/dim SO(d) is therefore exactly Friedmann geometry with kappa = 1/2 imposed in every d (R1); with R3 it would read 32 pi/((d-2)^2 dim SO(d))",
      sp.simplify(Zd2.subs(kap, sp.Rational(1, 2)) - 32 * sp.pi / dimSO) == 0 and sp.simplify(Zd2.subs(kap, (d - 2) / 2) - 32 * sp.pi / ((d - 2)**2 * dimSO)) == 0)
G00_coeff = sp.simplify(d * (d - 1) / 2)
check("S3  control: dim SO(d) = d(d-1)/2 equals the coefficient of H^2 in G_00 for d = 2..5 (3, 6, 10 at d = 3, 4, 5 -> 1, 3, 6, 10)", [G00_coeff.subs(d, k) for k in (2, 3, 4, 5)] == [1, 3, 6, 10])

# ------------------------------------------------------------------ Gate E : embedding
print("\nGate E  the a0-horizon inside its own de Sitter universe: mass ratio M_s/M_Nariai = (r_s/L)^(d-2) / [(2/(d-2)) ((d-2)/d)^(d/2)], r_s/L = (d-2) Z_f/(2 kappa)  (<= 1 needed)")
def mass_ratio(dd, kv):
    rsL = (dd - 2) * 4 * math.sqrt(math.pi / (dd * (dd - 1))) / (2 * kv)
    muN = (2 / (dd - 2)) * ((dd - 2) / dd)**(dd / 2)
    return rsL**(dd - 2) / muN
print(f"  {'candidate':<34}" + "".join(f"{'d=' + str(x):>10}" for x in range(3, 13)))
passE = {}
for nm, ex in cands.items():
    if nm.startswith("RV"):
        continue
    row = []
    for x in range(3, 13):
        kv = float(ex.subs(d, x))
        row.append(mass_ratio(x, kv))
    passE[nm] = [v <= 1 for v in row]
    print(f"  {nm:<34}" + "".join(f"{v:>10.3g}" for v in row))
check("E1  p06 reproduced: at d = 3 with kappa = 1/2 the mass ratio is 3 sqrt3 Z/4 = 7.52 (> 1: no horizon)", abs(mass_ratio(3, 0.5) - 3 * math.sqrt(3) * math.sqrt(32 * math.pi / 3) / 4) < 1e-9)
check("E2  every candidate fails gate E at d = 3 (nothing here singles out d = 3 as a place where the a0-horizon is real)", not any(v[0] for v in passE.values()))
where = {nm: [3 + i for i, v in enumerate(row) if v] for nm, row in passE.items()}
print("      d at which gate E is passed (3..12):", {k: v for k, v in where.items() if v})

# ------------------------------------------------------------------ Gate N : d -> 2+
print("\nGate N  MOND transition radius r_M^(d-1) = 8 pi G_D (d-2) M/((d-1) Omega a0) (from f01 Gauss law) as d -> 2+ :  r_M^(d-1) ~ (d-2)/kappa(d)")
for nm, ex in cands.items():
    lim = sp.limit((d - 2) / ex, d, 2, '+')
    print(f"    {nm:<34} lim (d-2)/kappa = {lim}")
finiteN = {nm: (sp.limit((d - 2) / ex, d, 2, '+') not in (0, sp.oo, sp.zoo)) for nm, ex in cands.items() if not nm.startswith("RV")}
proportional = sorted(k for k, v in finiteN.items() if v)
check("N1  kappa proportional to (d-2) keeps r_M finite and non-zero as d -> 2+: exactly R1w, R2c, R3 (RV also, computed above); R1, R2, R3h, R4, R5, R6 send it to 0 "
      "[soft gate: d is an integer here; it only records which d-dependences inherit the Gauss-law factor (d-2)]",
      proportional == sorted(["R1w weighted channels", "R2c Tolman D-dim, dust-norm.", "R3  Tangherlini, r_s = R*"]) and sp.limit((d - 2) / cands["RV  volume-law (derived, f03)"], d, 2, '+') not in (0, sp.oo))

# ------------------------------------------------------------------ gates F and P (reading independent)
print("\nGates F and P (reading-independent)")
check("F1  gate F (flat rotation curve with the fixed s = 1 kernel, f02: d ln v/d ln r = (3-d)/4): zero only at d = 3 -- identical for every candidate",
      [k for k in range(2, 12) if sp.Rational(3 - k, 4) == 0] == [3])
def AL_over_U(dv, kv):
    Om = 2 * sp.pi**sp.Rational(dv, 2) / sp.gamma(sp.Rational(dv, 2))
    return sp.simplify(Om * (2 * sp.pi * (dv - 2)**2 / kv**2)**sp.Rational(dv - 1, 2) / ((4 * sp.pi)**((dv + 1) // 2) * sp.factorial((dv + 1) // 2)))
check("P1  gate P (f04): A Lambda^((d-1)/2)/U_(d+1) = (rational) pi^((d-3)/2)/kappa^(d-1): 1/(4 kappa^2) at d = 3, (9/4) pi/kappa^4 at d = 5, so an algebraic kappa passes at d = 3 only; "
      "RV: kappa_V^2 = 2 pi/27 gives 27/(8 pi) at d = 3 (never 1)",
      sp.simplify(AL_over_U(3, kap) - 1 / (4 * kap**2)) == 0 and sp.simplify(AL_over_U(5, kap) - sp.Rational(9, 4) * sp.pi / kap**4) == 0
      and sp.simplify(AL_over_U(3, sp.sqrt(2 * sp.pi / 27)) - sp.Rational(27, 8) / sp.pi) == 0 and sp.simplify(AL_over_U(3, sp.Rational(1, 2))) == 1)

# ------------------------------------------------------------------ pairwise crossings
print("\nPairwise crossings kappa_i(d) = kappa_j(d): every pair of candidates normalised to 1/2 at d = 3 crosses there BY CONSTRUCTION")
names = [nm for nm in cands if not nm.startswith("RV")]
pairs = list(itertools.combinations(names, 2))
cross3 = 0
extra = []
for a_, b_ in pairs:
    diff = sp.simplify(cands[a_] - cands[b_])
    if sp.simplify(diff.subs(d, 3)) == 0:
        cross3 += 1
    f = sp.lambdify(d, cands[a_] - cands[b_], 'numpy')
    grid = np.linspace(2.02, 12, 4000)
    with np.errstate(all='ignore'):
        vv = np.array(f(grid), dtype=float) * np.ones_like(grid)
    vv = np.where(np.isfinite(vv), vv, np.nan)
    for i in range(len(grid) - 1):
        if np.isfinite(vv[i]) and np.isfinite(vv[i + 1]) and vv[i] * vv[i + 1] < 0 and abs(grid[i] - 3) > 0.05:
            extra.append((a_.split()[0], b_.split()[0], round(float(grid[i]), 2)))
check("X1  all %d pairs cross at d = 3 (%d/%d): the record's 'lock at d = 3' is guaranteed by normalisation, not a finding" % (len(pairs), cross3, len(pairs)), cross3 == len(pairs))
print("      additional crossings away from d = 3 (pair, d):", extra)

print(f"\n  {sum(OK)}/{len(OK)} checks held.")
sys.exit(0 if all(OK) else 1)
