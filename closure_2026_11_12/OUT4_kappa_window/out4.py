#!/usr/bin/env python3
# OUT-4 (KAPPA WINDOW): does the one theorem T* hold?
#   T*:  a_0 = c^2 / (2 lambda_Lambda),  lambda_Lambda := c / sqrt(G rho_Lambda)
#        (the law's saturation is the surface gravity of the vacuum's Jeans sphere)
#   If T* holds -> kappa = 1/2 exactly and the kappa question is CLOSED.
#
# Criteria: FROZEN_CRITERIA.md, committed alone before this file existed.
# TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing.
# kappa = 1/2 FITTED; not theory closed.  Footings never pooled.

import json
import math
import os
import sys

import sympy as sp

MUT = os.environ.get("OUT4_MUTATE", "0") == "1"

# ------------------------------------------------------------------ constants / background
G = 6.67430e-11
C = 2.99792458e8
MSUN = 1.98847e30
KPC = 3.0856775814913673e19
MPC = 1000.0 * KPC

H0_KMS = 67.36                       # Planck 2018 TT,TE,EE+lowE+lensing (the record's frozen set)
H0 = H0_KMS * 1.0e3 / MPC
OM, OL, OB = 0.3153, 0.6847, 0.0493
RHO_CRIT = 3.0 * H0 ** 2 / (8.0 * math.pi * G)
RHO_LAM = OL * RHO_CRIT

FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
A0_EXT = {"CFG493": 7.8105e-11, "RAR_external": 1.20e-10}

ALLOW_DEX = 0.0411                   # the record's footing separation; pre-registered unchanged

# the vacuum's two natural lengths
LAM_L = C / math.sqrt(G * RHO_LAM)             # the Jeans / light-crossing length  = sqrt(8pi/Lambda)
R_DS = math.sqrt(3.0 / (8.0 * math.pi * G * RHO_LAM / (C * C)))   # de Sitter radius sqrt(3/Lambda)
H_LAM = H0 * math.sqrt(OL)

# ------------------------------------------------------------------ scaffolding
OUT = {}
LINES = []


def say(s=""):
    LINES.append(str(s))
    print(s)


def dex(x):
    return math.log10(x) if x > 0 else float("nan")


CHECKS = []


def check(tag, name, ok, measured, thresh):
    CHECKS.append({"gate": tag, "name": name, "pass": bool(ok),
                   "measured": measured, "threshold": thresh})
    say(f"  {tag:4s} {name}")
    say(f"       measured  : {measured}")
    say(f"       threshold : {thresh}")
    say(f"       verdict   : {'PASS' if ok else 'FAIL'}")
    say()


say("OUT-4 (KAPPA WINDOW): the one theorem T*, and whether it holds.   MUTATE = %d" % (1 if MUT else 0))
say("     criteria FROZEN_CRITERIA.md (57ffe5586a).  kappa = 1/2 FITTED; not theory closed.")
say("     Adopts nothing. Footings never pooled.")
say()

# ------------------------------------------------------------------ background report
say("=== BACKGROUND (reported, not graded) ===")
say(f"  H0 = {H0_KMS:.2f} km/s/Mpc      Omega_m = {OM}  Omega_L = {OL}  Omega_b = {OB}")
say(f"  rho_Lambda = {RHO_LAM:.6e} kg/m^3      rho_crit,0 = {RHO_CRIT:.6e} kg/m^3")
say(f"  c sqrt(G rho_Lambda) = {C*math.sqrt(G*RHO_LAM):.6e} m/s^2")
say(f"  lambda_Lambda = c/sqrt(G rho_Lambda) = {LAM_L:.6e} m = {LAM_L/MPC/1000.0:.4f} Gpc")
say(f"  R_dS = sqrt(3/Lambda)               = {R_DS:.6e} m = {R_DS/MPC/1000.0:.4f} Gpc")
say(f"  l_0  = c^2/a_0 (canonical footing)  = {C*C/FOOT['canonical']:.6e} m")
say()
OUT["background"] = dict(H0=H0, OM=OM, OL=OL, OB=OB, rho_Lam=RHO_LAM, rho_crit=RHO_CRIT,
                         c_sqrt_GrhoL=C * math.sqrt(G * RHO_LAM),
                         lam_L=LAM_L, R_dS=R_DS, H_LAM=H_LAM)

# ================================================================== O1 -- T* is well posed
say("=== O1: T* is well-posed -- the four spellings are one statement (sympy, exact) ===")
a0, k, l0, Lm, cc, gg, rr = sp.symbols("a0 k l0 Lambda c g rho", positive=True)
# lambda_L = c/sqrt(G rho);  kappa = a0/(c sqrt(G rho))
lam = cc / sp.sqrt(gg * rr)
kap = a0 / (cc * sp.sqrt(gg * rr))

# (i) a0 = c^2/(2 lam)   <=>   kappa = 1/2
e1 = sp.simplify(sp.Eq(a0, cc ** 2 / (2 * lam)).lhs - sp.Eq(a0, cc ** 2 / (2 * lam)).rhs)
r1 = sp.simplify((cc ** 2 / (2 * lam)) / (cc * sp.sqrt(gg * rr)))     # kappa implied by T*
# (ii) Lambda l0^2 = 32 pi  with l0 = c^2/a0, Lambda = 8 pi G rho / c^2, a0 = kappa c sqrt(G rho)
Lm_expr = 8 * sp.pi * gg * rr / cc ** 2
l0_expr = cc ** 2 / (k * cc * sp.sqrt(gg * rr))
r2 = sp.simplify(Lm_expr * l0_expr ** 2)
# (iii) rho c^2 = 4 a0^2 / G   at kappa = 1/2
r3 = sp.simplify((rr * cc ** 2) - (4 * (k * cc * sp.sqrt(gg * rr)) ** 2 / gg))

o1_num = float(r1)                        # kappa implied by T*
o1_lhs = sp.simplify(Lm_expr * (cc ** 2 / a0) ** 2)   # Lambda l0^2 in terms of a0
say(f"  T* reads  a0 = c^2/(2 lambda_L);  dividing by c sqrt(G rho) gives  kappa = {r1}")
say(f"  Lambda l_0^2 expressed in kappa  = {sp.simplify(r2)}   -> at kappa=1/2: {sp.simplify(r2.subs(k, sp.Rational(1,2)))}")
say(f"  rho c^2 - 4 a0^2/G  at kappa=1/2  = {sp.simplify(r3.subs(k, sp.Rational(1,2)))}")
o1 = (sp.simplify(r1 - sp.Rational(1, 2)) == 0
      and sp.simplify(r2.subs(k, sp.Rational(1, 2)) - 32 * sp.pi) == 0
      and sp.simplify(r3.subs(k, sp.Rational(1, 2))) == 0)
check("O1", "T* <=> kappa=1/2 <=> Lambda l0^2 = 32 pi <=> rho_L c^2 = 4 a0^2/G",
      o1,
      f"kappa(T*) = {r1}; Lambda l0^2(kappa=1/2) = {sp.simplify(r2.subs(k, sp.Rational(1,2)))}; "
      f"rho c^2 - 4a0^2/G = {sp.simplify(r3.subs(k, sp.Rational(1,2)))}",
      "all three exact (sympy simplify to 0)")
OUT["O1"] = dict(kappa_from_Tstar=str(r1),
                 Lambda_l0sq_at_half=str(sp.simplify(r2.subs(k, sp.Rational(1, 2)))),
                 residual_stress=str(sp.simplify(r3.subs(k, sp.Rational(1, 2)))))

# ================================================================== O2 -- the census (the blocker)
say("=== O2: the census -- the mass-independent charged ring is generated by kappa alone ===")
# dimension vectors, rows (L, M, T)
vecs = {
    "G": sp.Matrix([3, -1, -2]),
    "c": sp.Matrix([1, 0, -1]),
    "rho_Lambda": sp.Matrix([-3, 1, 0]),
    "a_0": sp.Matrix([1, 0, -2]),
    "M_b": sp.Matrix([0, 1, 0]),
}
M0 = sp.Matrix.hstack(vecs["G"], vecs["c"], vecs["rho_Lambda"])
det0 = M0.det()
rk0 = M0.rank()
M1 = sp.Matrix.hstack(vecs["G"], vecs["c"], vecs["rho_Lambda"], vecs["a_0"])
ns1 = M1.nullspace()
M2 = sp.Matrix.hstack(vecs["G"], vecs["c"], vecs["rho_Lambda"], vecs["a_0"], vecs["M_b"])
ns2 = M2.nullspace()
say(f"  rank(G, c, rho_Lambda) = {rk0}   det = {det0}   -> weight-0 subring has NO dimensionless element")
say(f"  nullspace dim of (G,c,rho_L,a_0) = {len(ns1)}   generator(s):")
for v in ns1:
    say(f"      {list(v.T)}   in basis [G, c, rho_L, a_0]")
say(f"  nullspace dim of (G,c,rho_L,a_0,M_b) = {len(ns2)}   generator(s):")
for v in ns2:
    say(f"      {list(v.T)}   in basis [G, c, rho_L, a_0, M_b]")
# expected: the single generator of ns1 is kappa = a0 * (c sqrt(G rho))^-1 -> exponents
#   a0^1 G^-1/2 c^-1 rho^-1/2  -> in basis [G,c,rho,a0]: (-1/2, -1, -1/2, 1)
want = sp.Matrix([sp.Rational(-1, 2), -1, sp.Rational(-1, 2), 1])
# sympy may scale the nullspace vector; test proportionality, not equality
def _prop(v, wv):
    # find the scalar ratio on the first nonzero component, then check all
    for i in range(len(wv)):
        if wv[i] != 0:
            r = sp.simplify(v[i] / wv[i])
            return sp.simplify(v - r * wv) == sp.zeros(len(wv), 1)
    return sp.simplify(v) == sp.zeros(len(wv), 1)
gen_ok = len(ns1) == 1 and _prop(ns1[0], want)
o2 = (rk0 == 3 and det0 != 0 and len(ns1) == 1 and gen_ok and len(ns2) == 2)
check("O2", "the mass-independent dimensionless content of the theory is the single number kappa",
      o2,
      f"rank(G,c,rho_L)={rk0}; nullspace(+a_0) dim={len(ns1)} generator={[str(x) for x in ns1[0]] if ns1 else None}; "
      f"nullspace(+M_b) dim={len(ns2)}",
      "rank 3; +a_0 gives dim 1 generated by kappa; +M_b gives dim 2")
OUT["O2"] = dict(rank_weight0=rk0, det_weight0=str(det0), nullspace_a0=len(ns1), nullspace_Mb=len(ns2))

# ================================================================== O3 -- the number T* returns
say("=== O3: the number T* returns (reported, not graded) ===")
kappa_T = sp.Rational(1, 2)
say(f"  kappa_T* = {kappa_T} = {float(kappa_T)}   (exact, by O1)")
OUT["O3"] = dict(kappa_Tstar=0.5)

# ================================================================== O4 -- is the 1/2 a surface gravity?
say("=== O4: is the 1/2 a SURFACE GRAVITY?  (a sphere of vacuum of radius lambda_L) ===")
# M = (4pi/3) rho_L lam^3 ; R_s = 2 G M / c^2 ;  R_s/lam = 8 pi / 3  exactly (mass- and Lambda-free)
ratio_sym = sp.simplify((2 * gg * (sp.Rational(4, 3) * sp.pi * rr * lam ** 3) / cc ** 2) / lam)
ratio_num = float(ratio_sym)
say(f"  R_schw(lambda_L)/lambda_L = 8 pi/3 = {ratio_sym} = {ratio_num:.6f}   (exact; independent of rho_L, G, c)")
say(f"  a surface gravity c^2/(2R) requires R = R_s.  Measured: R = lambda_L = R_s/{ratio_num:.4f}.")
o4 = abs(ratio_num - 1.0) <= 0.05
check("O4", "c^2/(2 lambda_L) is the surface gravity of the vacuum sphere of radius lambda_L",
      o4, f"R_schw/lambda_L = {ratio_num:.6f}", "|ratio - 1| <= 0.05")
OUT["O4"] = dict(Rs_over_lam=ratio_num)

# ================================================================== O5 -- is lambda_L a horizon?
say("=== O5: is lambda_L a HORIZON radius?  (Schwarzschild-de Sitter, any M >= 0) ===")
# Kottler: f(r) = 1 - 2GM/(c^2 r) - Lambda r^2/3.  A horizon at r needs f(r)=0, i.e.
#   Lambda r^2/3 = 1 - 2GM/(c^2 r) <= 1  ->  r <= sqrt(3/Lambda) = R_dS.
lam_over_Rds = float(sp.simplify(lam / sp.sqrt(3 / Lm_expr)))
say(f"  every SdS horizon obeys r <= R_dS = sqrt(3/Lambda)   (since 2GM/(c^2 r) >= 0)")
say(f"  lambda_L / R_dS = sqrt(8 pi/3) = {lam_over_Rds:.6f}   -> lambda_L is {100*(lam_over_Rds-1):.1f} % BEYOND R_dS")
say(f"  equivalently A_Lambda = 4 pi Lambda lambda_L^2 = {4*sp.pi*sp.simplify(Lm_expr*lam**2)} "
    f"= {float(4*sp.pi*sp.simplify(Lm_expr*lam**2)):.4f}  vs the SdS maximum 12 pi = {float(12*sp.pi):.4f}")
o5 = lam_over_Rds <= 1.0
check("O5", "lambda_L can be a horizon radius of some configuration of the theory",
      o5, f"lambda_L/R_dS = {lam_over_Rds:.6f}; A_Lambda = {float(4*sp.pi*sp.simplify(Lm_expr*lam**2)):.4f} vs max 12 pi",
      "lambda_L/R_dS <= 1  (equivalently A_Lambda <= 12 pi)")
OUT["O5"] = dict(lam_over_RdS=lam_over_Rds,
                 A_Lambda=float(4 * sp.pi * sp.simplify(Lm_expr * lam ** 2)),
                 A_Lambda_max_SdS=float(12 * sp.pi))

# ================================================================== O6 -- the radius ladder
say("=== O6: does lambda_L appear anywhere in the theory's own radius ladder? ===")
MB_REF = 6.0e10 * MSUN
r_M = math.sqrt(G * MB_REF / FOOT["canonical"])
R_TA = (G * MB_REF / H0 ** 2) ** (1.0 / 3.0)          # crude turnaround, reported only
R_FOLD = 0.52 * R_TA
ladder = {
    "r_M (log M_b 10.78, canonical)": r_M,
    "R_ta (same mass)": R_TA,
    "R_fold = 0.52 R_ta (FLD1)": R_FOLD,
    "c/H_0": C / H0,
    "R_dS = c/H_Lambda": R_DS,
    "lambda_Lambda = c/sqrt(G rho_L)": LAM_L,
}
say(f"  {'object':38s} {'m':>14s}  {'/lambda_L':>12s}")
for nm, v in ladder.items():
    say(f"  {nm:38s} {v:14.6e}  {v/LAM_L:12.4e}")
hits = [nm for nm, v in ladder.items()
        if abs(v / LAM_L - 1.0) <= 0.05 and not nm.startswith("lambda_Lambda")]
o6 = len(hits) > 0
check("O6", "some characteristic radius of the theory equals lambda_Lambda",
      o6, f"lambda_L = {LAM_L:.4e} m; nearest non-vacuum radius is R_dS = {R_DS/LAM_L:.4f} lambda_L",
      "some theory radius within 5 % of lambda_L")
OUT["O6"] = dict(ladder={k: v for k, v in ladder.items()}, hits=hits)

# ================================================================== O7 / O8 -- the menus
say("=== O7: the LENGTH menu -- how much freedom does the choice of vacuum length carry? ===")
# Holding T*'s factor at 1/2 and varying ONLY the length L in  a_0 = c^2/(2 L):
#   kappa = c^2/(2 L c sqrt(G rho_L)) = lambda_L / (2 L)     [exact]
lengths = {
    "lambda_Lambda = c/sqrt(G rho_L) (Jeans / light-crossing; T*)": LAM_L,
    "R_dS = sqrt(3/Lambda) (de Sitter)": R_DS,
    "2 R_dS (de Sitter diameter)": 2 * R_DS,
    "c/H_0 (Hubble radius today)": C / H0,
    "c/(2 H_Lambda) (= 2 R_dS)": C / (2 * H_LAM),
}
k_len = {nm: LAM_L / (2.0 * v) for nm, v in lengths.items()}   # factor 1/2 held fixed
say(f"  {'length reading':56s} {'kappa':>10s}  {'dex vs 1/2':>11s}")
for nm, kv in k_len.items():
    say(f"  {nm:56s} {kv:10.5f}  {dex(kv/0.5):11.4f}")
span_len = dex(max(k_len.values()) / min(k_len.values()))
say(f"  span = {span_len:.4f} dex   (allowance {ALLOW_DEX:.4f} dex)   ratio {span_len/ALLOW_DEX:.2f}x")
o7 = span_len <= ALLOW_DEX
check("O7", "the vacuum-length choice is forced", o7,
      f"span {span_len:.4f} dex over {len(lengths)} natural lengths",
      f"span <= {ALLOW_DEX} dex")
OUT["O7"] = dict(kappa_by_length=k_len, span_dex=span_len)

say("=== O8: the FACTOR menu -- how much freedom does the surface-gravity factor carry? ===")
# Holding T*'s length at lambda_L and varying ONLY the factor f in  a_0 = f c^2/lambda_L:
#   kappa = f c^2/(lambda_L c sqrt(G rho_L)) = f     [exact, since lambda_L sqrt(G rho_L) = c]
factors = {
    "1/2  (surface gravity c^2/(2R); T*)": 0.5,
    "1    (acceleration c^2/R)": 1.0,
    "1/(2 pi)  (Unruh/Gibbons-Hawking reading, k03)": 1.0 / (2 * math.pi),
    "1/4  (|Phi|/R of the vacuum ball at R_dS)": 0.25,
    "1/(8 pi)  (Einstein's 8 pi divided out; FINAL-19's f)": 1.0 / (8 * math.pi),
}
k_fac = {nm: f for nm, f in factors.items()}
say(f"  {'factor reading':56s} {'kappa':>10s}  {'dex vs 1/2':>11s}")
for nm, kv in k_fac.items():
    say(f"  {nm:56s} {kv:10.5f}  {dex(kv/0.5):11.4f}")
span_fac = dex(max(k_fac.values()) / min(k_fac.values()))
say(f"  span = {span_fac:.4f} dex   (allowance {ALLOW_DEX:.4f} dex)   ratio {span_fac/ALLOW_DEX:.2f}x")
o8 = span_fac <= ALLOW_DEX
check("O8", "the surface-gravity factor is forced", o8,
      f"span {span_fac:.4f} dex over {len(factors)} natural factors",
      f"span <= {ALLOW_DEX} dex")
OUT["O8"] = dict(kappa_by_factor=k_fac, span_dex=span_fac)

# ================================================================== O9 -- the window
say("=== O9: THE KAPPA WINDOW ===")
s = C * math.sqrt(G * RHO_LAM)
say(f"  c sqrt(G rho_Lambda) = {s:.6e} m/s^2   (Planck 2018 background)")
say()
say("  (a) the MEASUREMENT constraint -- a_0 determinations against the canonical definition")
meas = {}
for nm, a0v in list(FOOT.items()) + list(A0_EXT.items()):
    meas[nm] = a0v / s
    say(f"      {nm:14s} a_0 = {a0v:.6e}  ->  kappa = {meas[nm]:.6f}")
# non-circular only: drop the canonical footing (a_0^can is DEFINED so that kappa=1/2 vs rho_L)
kap_C_meas_lo = 0.4172 - 0.0946       # FINAL-19, CFG493, canonical definition
kap_C_meas_hi = 0.6414 + 0.1283       # FINAL-16 J0, external RAR a_0 = 1.20e-10, syst included
say(f"      window from the two independent a_0 determinations (1 sigma, syst included):")
say(f"          [{kap_C_meas_lo:.4f}, {kap_C_meas_hi:.4f}]   width {dex(kap_C_meas_hi/kap_C_meas_lo):.4f} dex")
say()
say("  (b) the HARD derivation constraints imported from the record (already graded there)")
hard = {
    "FINAL-19 deep-field column, saturation f=1": (2.5066, 2.5066, "22.1 sigma above the measurement"),
    "FINAL-18 fold matching (log M_b 10.45)": (1.19e-3, 1.19e-3, "1.86 dex mass drift; 2.6 dex below"),
    "T*  Lambda-Jeans surface gravity (this lane)": (0.5, 0.5, "O4 FAIL, O5 FAIL -- not load-bearing"),
}
for nm, (lo, hi, note) in hard.items():
    say(f"      {nm:52s} [{lo:.4e}, {hi:.4e}]   {note}")
say()
say("  (c) the MENUS -- these are FREEDOM, not constraints, and are NOT intersected")
menus = {
    "FINAL-17 capacity menu": (0.4607, 2.8944),
    "FINAL-16 formation-epoch menu": (0.3536, 0.7368),
    "this lane's length menu (O7)": (min(k_len.values()), max(k_len.values())),
    "this lane's factor menu (O8)": (min(k_fac.values()), max(k_fac.values())),
}
for nm, (lo, hi) in menus.items():
    say(f"      {nm:52s} [{lo:.4e}, {hi:.4e}]   span {dex(hi/lo):.4f} dex  -- no value selected")
say()
# (i) the window over ALL hard constraints
allc = dict(hard)
allc["measurement (independent)"] = (kap_C_meas_lo, kap_C_meas_hi)
lo_all = max(v[0] for v in allc.values())
hi_all = min(v[1] for v in allc.values())
W_all = (lo_all, hi_all) if lo_all <= hi_all else None
say(f"  (d) W over ALL hard constraints : "
    f"{'EMPTY' if W_all is None else '[%.4f, %.4f]' % W_all}"
    f"   (max of lower edges {lo_all:.4e} vs min of upper edges {hi_all:.4e};"
    f" gap {dex(lo_all/hi_all):.4f} dex)")
# (ii) the window over the constraints the theory SUPPORTS:
#      the fold and the column are REFUTED (not open), and T* is not load-bearing,
#      so the surviving constraint is the measurement alone.
lo_s, hi_s = kap_C_meas_lo, kap_C_meas_hi
wid_s = dex(hi_s / lo_s)
say(f"  (e) W over SUPPORTED constraints: [{lo_s:.4f}, {hi_s:.4f}]"
    f"   width {wid_s:.4f} dex = {wid_s/ALLOW_DEX:.2f}x the {ALLOW_DEX} dex allowance")
say(f"      contains kappa = 1/2 ? {'YES' if lo_s <= 0.5 <= hi_s else 'NO'}"
    f"   (geometric centre {math.sqrt(lo_s*hi_s):.4f})")
o9 = (W_all is not None) and (wid_s <= ALLOW_DEX) and abs(lo_s - 0.5) < 1e-9 and abs(hi_s - 0.5) < 1e-9
check("O9", "T_WINDOW: the kappa window is a single point and that point is 1/2",
      o9,
      f"W(all hard) = {'EMPTY' if W_all is None else '[%.4f,%.4f]' % W_all}; "
      f"W(supported) = [{lo_s:.4f}, {hi_s:.4f}] width {wid_s:.4f} dex = {wid_s/ALLOW_DEX:.2f}x allowance; "
      f"contains 1/2: {'YES' if lo_s <= 0.5 <= hi_s else 'NO'}",
      "a single point, equal to 1/2, within 0.0411 dex")
OUT["O9"] = dict(W_all=None if W_all is None else list(W_all),
                 W_supported=[lo_s, hi_s], width_dex=wid_s,
                 width_over_allowance=wid_s / ALLOW_DEX,
                 contains_half=bool(lo_s <= 0.5 <= hi_s),
                 menus={k: list(v) for k, v in menus.items()},
                 kappa_measurements=meas)

# ================================================================== O10 -- the G_lambda weight audit
say("=== O10: the G_lambda weight audit -- every static-sector relation, weighted ===")
# A relation R = 0 (written as a residual) is G_lambda-COVARIANT of weight w iff, after
# substituting  X -> lam^weight(X) . X  for every symbol, the residual becomes lam^w . R.
# A covariant relation is a FLAT DIRECTION: it is satisfied or not independently of the orbit
# coordinate kappa, so it cannot RETURN a value for kappa.  A relation that would fix kappa
# must mix two different weights (be non-homogeneous).
lam_s = sp.symbols("lam", positive=True)
g_, a0s, rb = sp.symbols("g a0 rho_b", positive=True)
gN, mu, Xm, xx, gc, L1, Sc, P, v4, Mb, kappa = sp.symbols(
    "gN mu X x g_c L1 Sigma_c Pi v4 M_b kappa", positive=True)
# distinct, unambiguous names: sympy identifies symbols by (name, assumptions), so a
# "g" used for Newton's constant would silently collide with the field "g".
GG, CC, RHO, KK = sp.symbols("G_Newton c_light rho_Lambda_ K_coupling", positive=True)

rels = {
    "law (quadratic)   g_N = g^2/(g+a_0)": gN - g_ ** 2 / (g_ + a0s),
    "mu                mu = g/(g+a_0)": mu - g_ / (g_ + a0s),
    "X_L               X(1+X) = x^2": Xm * (1 + Xm) - xx ** 2,
    "cold pull         g_c = a_0 g/(g+a_0)": gc - a0s * g_ / (g_ + a0s),
    "Poisson           div[mu grad Phi] = K rho_b": L1 - KK * rb,
    "universal column  Sigma_c = a_0/(2 pi G)": Sc - a0s / (2 * sp.pi * GG),
    "deep-field stress |Pi| = g^2/(8 pi G)": P - g_ ** 2 / (8 * sp.pi * GG),
    "BTFR              v_inf^4 = G M_b a_0": v4 - GG * Mb * a0s,
    "definition        a_0 = kappa c sqrt(G rho_L)": a0s - kappa * CC * sp.sqrt(GG * RHO),
}
# G_lambda weights.  weight 1: a_0, g, g_N, g_c, rho_b, Sigma_c, M_b, kappa, div[mu grad Phi]
#                    weight 2: v_inf^4, |Pi|   (they go as a_0^2 and g^2)
#                    weight 0: G, c, rho_L, r, x, X, mu, K
# NOTE: the substitution is  X -> lam^w . X  (the symbol stays);  X -> lam  alone would
# collapse the expression and is wrong.
w = {a0s: lam_s * a0s, g_: lam_s * g_, gN: lam_s * gN, gc: lam_s * gc, rb: lam_s * rb,
     Sc: lam_s * Sc, Mb: lam_s * Mb, kappa: lam_s * kappa, L1: lam_s * L1,
     P: lam_s ** 2 * P, v4: lam_s ** 2 * v4}
say("  weights under G_lambda:  lam^1 = {a_0, g, g_N, g_c, rho_b, Sigma_c, M_b, kappa, div[mu grad Phi]},")
say("                           lam^2 = {v_inf^4, |Pi|},   lam^0 = {G, c, rho_L, r, x, X, mu, K}")
say()
say("  A relation fixes kappa only if it MIXES weights.  Testing each for homogeneity:")
say()
weights = {}
n_hom = 0
for nm, res in rels.items():
    scaled = sp.simplify(res.xreplace(w))
    found = None
    for ww in (0, 1, 2):
        if sp.simplify(scaled - lam_s ** ww * res) == 0:
            found = ww
            break
    weights[nm] = found
    if found is not None:
        n_hom += 1
    say(f"      {nm:44s} homogeneous of weight {str(found):>4s}   "
        f"{'-> FLAT DIRECTION' if found is not None else '-> WOULD CONSTRAIN kappa'}")
say()
say(f"  {n_hom}/{len(rels)} relations are G_lambda-homogeneous, i.e. FLAT DIRECTIONS in kappa.")
say( "  The last one -- the definition -- is homogeneous of weight 1 too: that is exactly the")
say( "  statement 'kappa carries weight 1' (FINAL-16 J1 / FINAL-17 A4). It defines kappa; it")
say( "  does not value it.  No relation on the list mixes weights, so none can return a number.")
o10 = n_hom == len(rels)
check("O10", "the G_lambda no-go: no static-sector relation mixes weights, so none fixes kappa",
      o10,
      f"{n_hom}/{len(rels)} relations G_lambda-homogeneous (flat directions); 0 mix weights",
      "all relations homogeneous -- the no-go confirmed, not assumed")
OUT["O10"] = dict(n_homogeneous=n_hom, n_relations=len(rels),
                  weights={k: v for k, v in weights.items()})

# ================================================================== O11 -- footing ledger
say("=== O11: the footing ledger (never pooled) ===")
# both footings are a_0 values against the SAME rho_Lambda (FINAL-17 A5: can 0.500296, alt 0.604611)
kap_can = FOOT["canonical"] / s
kap_alt = FOOT["alt"] / s
sep = dex(kap_alt / kap_can)
say(f"  canonical: a_0 = {FOOT['canonical']:.6e} vs rho_Lambda -> kappa = {kap_can:.6f}  (record 0.500296)")
say(f"  alt      : a_0 = {FOOT['alt']:.6e} vs rho_Lambda -> kappa = {kap_alt:.6f}  (record 0.604611)")
say(f"  separation = {sep:.4f} dex;  the pre-registered allowance is half of it = {sep/2:.4f} dex"
    f"   (record: 0.0411)")
o11 = abs(kap_can - 0.500296) <= 2e-3 and abs(kap_alt - 0.604611) <= 2e-3 and abs(sep / 2 - 0.0411) <= 2e-3
check("O11", "footings reproduce the record's own ledger values, kept separate",
      o11,
      f"kappa_can = {kap_can:.6f}; kappa_alt = {kap_alt:.6f}; separation {sep:.4f} dex "
      f"-> allowance {sep/2:.4f} dex",
      "both within 2e-3 of the record; half-separation within 2e-3 of 0.0411")
OUT["O11"] = dict(kappa_canonical=kap_can, kappa_alt=kap_alt, separation_dex=sep,
                  allowance_dex=sep / 2)

# ================================================================== O12 -- look-elsewhere
say("=== O12: can the measured kappa SELECT 1/2 among simple constants? ===")
kap_obs, kap_err = 0.530, 0.037          # k03's two measurements combined (k05 S3)
cands = {"1/2": 0.5, "1/sqrt(pi)": 1 / math.sqrt(math.pi), "1/sqrt(3)": 1 / math.sqrt(3),
         "sqrt(2)/3": math.sqrt(2) / 3, "sqrt(pi)/3": math.sqrt(math.pi) / 3,
         "sqrt(8pi/3)/(2pi) [k03]": math.sqrt(8 * math.pi / 3) / (2 * math.pi),
         "1/2 sqrt(3/(2pi))": 0.5 * math.sqrt(3 / (2 * math.pi))}
say(f"  measured kappa = {kap_obs} +- {kap_err}   (k03 combined; {kap_err/kap_obs*100:.1f} %)")
for nm, kv in sorted(cands.items(), key=lambda t: abs(t[1] - kap_obs)):
    say(f"      {nm:28s} {kv:8.5f}   {(kv-kap_obs)/kap_err:+6.2f} sigma")
n1 = sum(1 for kv in cands.values() if abs(kv - kap_obs) <= kap_err)
o12 = n1 == 1 and abs(cands["1/2"] - kap_obs) <= kap_err
check("O12", "the data single out 1/2 among simple constants",
      o12,
      f"{n1} of {len(cands)} simple constants within 1 sigma of the measured kappa",
      "exactly one candidate within 1 sigma, and it is 1/2")
OUT["O12"] = dict(n_within_1sigma=n1, n_candidates=len(cands), kappa_obs=kap_obs, kappa_err=kap_err)

# ================================================================== MUTATE sentence
say("=== MUTATE ===")
if MUT:
    say("  FALSE TWIN: 'T* DERIVES kappa = 1/2.'")
    say(f"       O4 (surface gravity) : {'PASS' if o4 else 'FAIL'}   -- R_s/lambda_L = {ratio_num:.4f}")
    say(f"       O5 (horizon)         : {'PASS' if o5 else 'FAIL'}   -- lambda_L/R_dS = {lam_over_Rds:.4f}")
    say(f"       O7 (length menu)     : {'PASS' if o7 else 'FAIL'}   -- {span_len:.4f} dex")
    say(f"       O8 (factor menu)     : {'PASS' if o8 else 'FAIL'}   -- {span_fac:.4f} dex")
    say("       T* is a REWRITING of kappa = 1/2 (O1 is an exact equivalence, not a derivation),")
    say("       its 1/2 is not a surface gravity (O4), and its length is not a horizon (O5).")
    say("       The claim 'T* derives kappa = 1/2' is REJECTED.")
    MUT_OK = False
else:
    say("  Main run. No claim sentence is asserted; the gates speak.")
    MUT_OK = None
say()

# ================================================================== summary
npass = sum(1 for c in CHECKS if c["pass"])
say("=" * 78)
for c in CHECKS:
    say(f"  {c['gate']:4s} {'PASS' if c['pass'] else 'FAIL'}  {c['name']}")
say("=" * 78)
if MUT:
    say(f"OUT4 COMPLETE: {npass}/{len(CHECKS)} checks PASS.   MUTATE twin: the false claim is REJECTED.")
else:
    say(f"OUT4 COMPLETE: {npass}/{len(CHECKS)} checks PASS.")

OUT["checks"] = CHECKS
OUT["n_pass"] = npass
OUT["n_checks"] = len(CHECKS)
OUT["mutate"] = MUT
OUT["verdict"] = {
    "T_star_holds": bool(o4 and o5 and o7 and o8),
    "kappa_Tstar": 0.5,
    "window_supported_dex": wid_s,
    "window_over_allowance": wid_s / ALLOW_DEX,
    "lambda_L_over_R_dS": lam_over_Rds,
    "R_schw_over_lambda_L": ratio_num,
}

with open("out4_MUTATE.json" if MUT else "out4.json", "w") as f:
    json.dump(OUT, f, indent=2, default=str)
with open("out4_MUTATE.out" if MUT else "out4.out", "w") as f:
    f.write("\n".join(LINES) + "\n")

sys.exit(0 if MUT_OK is not False else 1)
