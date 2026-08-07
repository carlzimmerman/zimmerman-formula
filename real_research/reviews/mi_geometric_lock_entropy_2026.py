#!/usr/bin/env python3
r"""mi_geometric_lock_entropy_2026.py -- LANE L: can Bekenstein-Hawking's 1/4 be the framework's 1/4?

THE TARGET, exactly. The framework needs the de Sitter inertia FLOOR to be
    k = a_0/2 = (1/4) c sqrt(G rho_Lambda) = (c/4)/t_dyn,     t_dyn = 1/sqrt(G rho_Lambda) = 1.6011e18 s
    k = 4.6810e-11 m/s^2  (canonical; ALT footing x 1.2082)
instead of the Gibbons-Hawking value  k = c H_Lambda = c sqrt(8 pi G rho_Lambda / 3) = 5.4194e-10 m/s^2.
The ratio is EXACTLY  c H_Lambda / (a_0/2) = 2 Z = 4 sqrt(8 pi/3) = 8 sqrt(6 pi)/3 = 11.577620072932,
i.e. in crossover language q = a_0/(c H_Lambda) = 2/r the framework needs r = 2Z, against Milgrom 1999's
r = 1 and the conventional 2 pi a_0 ~ c H_Lambda at r = 4 pi = 12.566371.

THE STRUCTURE, which is the whole question: c H_Lambda carries the FRIEDMANN factor 8 pi/3; the floor the
framework needs carries NONE -- it is a bare sqrt(G rho) times 1/4. So Lane L asks the sharpest available
version: the most suggestive geometric 1/4 in physics is Bekenstein-Hawking S = A/4. Is it this 1/4?

WHAT THIS SCRIPT ESTABLISHES (all computed, none asserted):
  L-A  The exact de Sitter horizon data, and the two rival floors to 12 digits; the ratio 2Z is FOOTING-INVARIANT.
  L-B  Holographic equipartition, carried exactly. E = (1/2) N k T with N = A/L_p^2 gives a = c H EXACTLY
       -> a_0 = 2 c H_Lambda, which is EXACTLY Milgrom 1999's coefficient (r = 1). With the BEKENSTEIN-HAWKING
       bit count N = A/(4 L_p^2) it gives a = c H/4 EXACTLY: the 1/4 IS there, but it multiplies c H, so it
       lands sqrt(8 pi/3) = 2.894 times ABOVE the framework's floor. The residual miss is exactly the Friedmann
       factor -- the one thing the framework needs removed.
  L-C  Force route F = T dS/dR = c^4/G exactly (the Planck force, H-independent) -> a in {c H/2, c H, 2 c H}.
  L-D  Padmanabhan's emergence-of-space law reproduces the SECOND FRIEDMANN EQUATION exactly, hence for w = -1
       OUTPUTS H^2 = 8 pi G rho/3. So the 8 pi/3 is not a choice this route makes; it is the route's THEOREM.
  L-E  THE NO-GO, sharpened and exact. Write a = (c^2/L_p) sqrt(X/S). Then c H  <-> X = pi, and the TARGET
       <-> X = 3/128, a rational with NO pi. Any coefficient C in Q(pi) (rational function of pi) gives
       X = C^2 pi, which is rational only if C = sqrt(X/pi) -- and sqrt(pi) is NOT in Q(pi), because pi is
       transcendental (Lindemann 1882) so Q(pi) = Q(x) and x is not a square there. Therefore NO horizon
       construction with a Q(pi) coefficient can hit the target -- while Q(pi) CONTAINS both rivals (r = 1
       and r = 4 pi). Against interest: the number field favours the competitors and excludes the framework.
  L-F  THE GUARD, priced. The discrete choices (dof vs bits, 1/2 vs 1, Komar vs rho V, area vs volume) generate
       the lattice 2^i 3^j; that lattice reaches a GENERIC O(1) target to within a few percent, so a few-percent
       "hit" carries no evidence at all, and the 2Z-vs-4pi discrimination needs better than 7.87%. The closest
       lattice/simple-rational element to the target is r = 12 (Verlinde's a_0 = c H/6, floor c H/12 -> 0.24120
       against 0.25): a 3.52% NEAR MISS, NOT a lock.
  L-G  Reconciliation. This partly REDISCOVERS A CLOSED DOOR: real_research/reviews/desitter_entropy_coefficient.py
       already argued the number-field obstruction heuristically, and real_research/reviews/
       derive_Z_equipartition_attempt.py already got 4 pi/3 (not 1/4) from the bare-radius screen -- both
       reproduced here as checks. Distinct from the CLOSED CKN bridge, which lives at pi^(-1/4) ((3/8pi)^(1/4)
       = 0.5878), not at this lane's pi^(-1/2). And r = 2Z exceeds the independently derived admissibility
       ceiling r_max = 9.0168 (mi_r_admissibility_bound_2026.py), so a lock here would have CONTRADICTED it.

VERDICT: NO exact lock. The 1/4 of Bekenstein-Hawking cannot be the framework's 1/4, because it attaches to an
AREA (hence to c H, hence to 8 pi/3) and not to a bare density rate. kappa = 1/2 remains FITTED, NOT DERIVED.
The one structurally surviving route is the one that never mentions the horizon: rho_Lambda as the ONLY input.

CREDIT (mandatory). nu = sqrt(1+1/y) and the dS-Unruh balance are Milgrom 1999 PLA 253:273 eqs 6-9 (identical
kernel; he fixes a_0_hat = 2 c H_Lambda, i.e. r = 1); his eqs 10-11 give a second coefficient (r = 2); Milgrom
2008 sec 7.3.1 notes the mismatch "isn't necessarily meaningful". a_lambda = c^2 sqrt(Lambda/3): Milgrom 1994
Ann.Phys. 229:384. T = sqrt(a^2+Lambda/3)/2pi: Narnhofer, Peter & Thirring 1996 IJMPB 10:1507. Five-acceleration:
Deser & Levin 1997 CQG 14:L163. S = A/4: Bekenstein 1973, Hawking 1975. dS thermodynamics: Gibbons & Hawking
1977. Holographic equipartition and emergence of space: Padmanabhan 2010 (arXiv:1003.5665), 2012
(arXiv:1206.4916). Verlinde emergent gravity: Verlinde 2016 (arXiv:1611.02269), CONTESTED (Comment
arXiv:1909.01734). The framework's distinctive content is the cH_Lambda/Z COEFFICIENT plus the MI completion.

Exit 0 = every check held. No check(True); every condition below can fail. Floats only for display; every
coefficient is carried exactly in sympy.
"""
from __future__ import annotations

import math
import sys

import sympy as sp

ok: list[tuple[bool, str]] = []


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 112)
    print(f"  {t}")
    print("=" * 112)


# ----------------------------------------------------------------------------------------------------------
# exact symbols and the de Sitter horizon data
# ----------------------------------------------------------------------------------------------------------
H, G, c, hb, eps, pr = sp.symbols("H G c hbar epsilon p", positive=True)
Hd = sp.Symbol("Hdot", real=True)

Lp2 = G * hb / c ** 3                     # Planck length squared
R = c / H                                 # dS horizon radius = c/H = c sqrt(3/Lambda)
A = 4 * sp.pi * R ** 2                    # horizon area = 4 pi c^2/H^2
S = A / (4 * Lp2)                         # Bekenstein-Hawking entropy / k_B  (the 1/4 under test)
N_dof = A / Lp2                           # Padmanabhan surface degrees of freedom (4 x S)
kT = hb * H / (2 * sp.pi)                 # Gibbons-Hawking  k_B T = hbar H / 2 pi
V = 4 * sp.pi * R ** 3 / 3                # Hubble volume
rho_L = 3 * H ** 2 / (8 * sp.pi * G)      # vacuum MASS density from Friedmann

Z = 2 * sp.sqrt(8 * sp.pi / 3)            # 5.788810...
TWOZ = 2 * Z                              # 11.577620072932...  = 4 sqrt(8pi/3) = 8 sqrt(6pi)/3
FOURPI = 4 * sp.pi

# SI constants (CODATA) and the canonical footing anchor
c_ = 2.99792458e8
G_ = 6.67430e-11
hb_ = 1.054571817e-34
T_DYN = 1.6011e18                          # s, = 1/sqrt(G rho_Lambda), canonical
ALT = 1.2082                               # ALT-footing multiplier (rho_total / cH0)
rho_ = 1.0 / (G_ * T_DYN ** 2)
H_ = math.sqrt(8 * math.pi * G_ * rho_ / 3)
k_target_ = c_ / (4 * T_DYN)               # the floor the framework needs
cH_ = c_ * H_                              # the Gibbons-Hawking floor

banner("L-A  THE TWO RIVAL FLOORS, EXACTLY, AND THE FOOTING-INVARIANCE OF THEIR RATIO")

print(f"  canonical footing: t_dyn = {T_DYN:.5g} s -> rho_Lambda = {rho_:.5e} kg/m^3, "
      f"H_Lambda = {H_:.6e} 1/s = {H_*3.0857e19:.2f} km/s/Mpc")
print(f"  framework floor  k = (c/4) sqrt(G rho) = {k_target_:.6e} m/s^2   (brief: 4.6810e-11)")
print(f"  Gibbons-Hawking  k = c H_Lambda        = {cH_:.6e} m/s^2   (brief: 5.4194e-10)")
check(abs(k_target_ / 4.6810e-11 - 1) < 1e-3,
      f"A1 the framework floor reproduces the brief's 4.6810e-11 to {abs(k_target_/4.6810e-11-1)*100:.3f}%")
check(abs(cH_ / 5.4194e-10 - 1) < 1e-3,
      f"A2 c H_Lambda reproduces the brief's 5.4194e-10 to {abs(cH_/5.4194e-10-1)*100:.3f}%")

ratio_sym = sp.simplify((c * H) / (c * sp.sqrt(G * rho_L) / 4))
check(sp.simplify(ratio_sym - TWOZ) == 0,
      f"A3 c H_Lambda / [(1/4) c sqrt(G rho_Lambda)] = {sp.nsimplify(ratio_sym)} = 2Z exactly (symbolic, "
      f"rho_Lambda eliminated via Friedmann)")
check(sp.simplify(TWOZ - 8 * sp.sqrt(6 * sp.pi) / 3) == 0,
      f"A4 2Z = 4 sqrt(8pi/3) = 8 sqrt(6pi)/3 = {float(TWOZ):.12f} (the brief's 11.577620072932)")
check(abs(float(TWOZ) - 11.577620072932) < 5e-12,
      f"A5 2Z matches the brief to 12 digits: {float(TWOZ):.12f}")

# footing invariance: the ratio is a pure number, so the ALT fork cannot move it
ratio_can = cH_ / k_target_
rho_alt = rho_ * ALT ** 2                  # ALT footing scales the RATE by 1.2082 -> density by 1.2082^2
k_alt = c_ / 4 * math.sqrt(G_ * rho_alt)
cH_alt = c_ * math.sqrt(8 * math.pi * G_ * rho_alt / 3)
check(abs(cH_alt / k_alt - ratio_can) < 1e-9 and abs(k_alt / k_target_ - ALT) < 1e-9,
      f"A6 the target ratio is FOOTING-INVARIANT: canonical {ratio_can:.12f} vs ALT {cH_alt/k_alt:.12f} "
      f"(k itself moves by the expected x{ALT}) -- so nothing in this lane depends on the footing fork")
GAP = 1 - float(TWOZ / FOURPI)             # 7.87%, the brief's number (measured from 4 pi)
check(float(TWOZ) < float(FOURPI) and abs(GAP - 0.0787) < 5e-4,
      f"A7 the two published coefficients are only {100*GAP:.2f}% apart in r measured from 4 pi "
      f"({100*float(FOURPI/TWOZ-1):.2f}% measured from 2Z): {float(TWOZ):.6f} vs {float(FOURPI):.6f}. Any lock "
      f"must be EXACT, not 'near'")

banner("L-B  HOLOGRAPHIC EQUIPARTITION, CARRIED EXACTLY  (Padmanabhan 2010)")

print("  Bits vs degrees of freedom is the ONLY place Bekenstein-Hawking's 1/4 can enter, so both are carried.")
print("  E = (1/2) N k_B T,   M = E/c^2,   a = G M/R^2   (in dS,  G M_hor/R^2 and c^2/R coincide).")

E_dof = sp.simplify(sp.Rational(1, 2) * N_dof * kT)
M_dof = sp.simplify(E_dof / c ** 2)
a_dof = sp.simplify(G * M_dof / R ** 2)
check(sp.simplify(E_dof - c ** 5 / (G * H)) == 0 and sp.simplify(M_dof - c ** 2 * R / G) == 0,
      f"B1 N = A/L_p^2 equipartition gives E = c^5/(G H) and M = c^2 R/G exactly (hbar cancels: E = "
      f"{sp.nsimplify(E_dof)})")
check(sp.simplify(a_dof - c * H) == 0,
      f"B2 ... hence a = {sp.nsimplify(a_dof)} = c H EXACTLY -- the Gibbons-Hawking floor, i.e. the value the "
      f"framework needs to REPLACE")
check(sp.simplify(2 * a_dof - 2 * c * H) == 0 and sp.simplify(sp.Rational(2, 1) * a_dof / (c * H)) == 2,
      "B3 the implied crossover is a_0 = 2 k = 2 c H_Lambda, which is EXACTLY Milgrom 1999 PLA 253:273 eqs 6-9 "
      "(r = 1) -- AGAINST INTEREST: the principled equipartition route reproduces Milgrom's coefficient, not "
      "the framework's")

E_bits = sp.simplify(sp.Rational(1, 2) * S * kT)     # N = A/(4 L_p^2) = S
a_bits = sp.simplify(G * E_bits / c ** 2 / R ** 2)
check(sp.simplify(a_bits - c * H / 4) == 0,
      f"B4 with the BEKENSTEIN-HAWKING bit count N = A/(4 L_p^2) = S the SAME construction gives "
      f"a = {sp.nsimplify(a_bits)} = c H/4 EXACTLY -- the 1/4 is genuinely there")

coef_bits_bare = sp.simplify(a_bits.subs(H, sp.sqrt(8 * sp.pi * G * sp.Symbol("rho", positive=True) / 3))
                             / (c * sp.sqrt(G * sp.Symbol("rho", positive=True))))
check(sp.simplify(coef_bits_bare - sp.sqrt(8 * sp.pi / 3) / 4) == 0,
      f"B5 but on the BARE rate that 1/4 reads {sp.nsimplify(coef_bits_bare)} = sqrt(8pi/3)/4 = "
      f"{float(coef_bits_bare):.8f}, NOT 1/4 = 0.25000000")
miss = sp.simplify(coef_bits_bare / sp.Rational(1, 4))
check(sp.simplify(miss - sp.sqrt(8 * sp.pi / 3)) == 0 and abs(float(miss) - 2.89440497) < 1e-7,
      f"B6 THE RESIDUAL MISS IS EXACTLY THE FRIEDMANN FACTOR: got/target = {sp.nsimplify(miss)} = "
      f"sqrt(8pi/3) = {float(miss):.8f} = Z/2. The 1/4 exists; it multiplies the WRONG RATE, because "
      f"S = A/4 attaches to an AREA and the area's radius is 1/H")
check(abs(float(miss) - 1) / GAP > 10,
      f"B7 and the miss is {100*(float(miss)-1):.1f}% ({float(miss):.4f}x) -- {abs(float(miss)-1)/GAP:.0f} "
      f"times the {100*GAP:.2f}% gap that separates 2Z from 4 pi, so this is not even a near miss")

banner("L-C  ENTROPY-PER-LENGTH FORCE ROUTE  F = T dS/dR")

Rs = sp.Symbol("R_s", positive=True)               # the horizon radius as an independent variable
S_of_R = sp.pi * Rs ** 2 / Lp2                     # S = pi R^2/L_p^2  (= A/4L_p^2)
kT_of_R = hb * c / (2 * sp.pi * Rs)                # k_B T = hbar H/2pi with H = c/R
check(sp.simplify(S.subs(H, c / Rs) - S_of_R) == 0 and sp.simplify(kT.subs(H, c / Rs) - kT_of_R) == 0,
      "C0 the radius-variable rewrite of S and T is an identity (checked against the H-variable forms)")
F = sp.simplify(kT_of_R * sp.diff(S_of_R, Rs))
check(sp.simplify(F - c ** 4 / G) == 0,
      f"C1 F = T dS/dR = {sp.nsimplify(F)} = c^4/G EXACTLY -- the Planck (maximum) force, INDEPENDENT of H, so "
      f"it carries no scale of its own and every coefficient comes from the mass you divide by")
M_Lambda = sp.simplify(rho_L * V)
check(sp.simplify(M_Lambda - c ** 3 / (2 * G * H)) == 0,
      f"C2 the vacuum mass inside the Hubble volume is rho_Lambda V = {sp.nsimplify(M_Lambda)} = c^2 R/(2G) -- "
      f"exactly the SCHWARZSCHILD mass of the horizon (an exact dS identity, not a choice)")
a_force_hor = sp.simplify(F / M_dof)
a_force_lam = sp.simplify(F / M_Lambda)
a_grav_lam = sp.simplify(G * M_Lambda / R ** 2)
check(sp.simplify(a_force_hor - c * H) == 0 and sp.simplify(a_force_lam - 2 * c * H) == 0
      and sp.simplify(a_grav_lam - c * H / 2) == 0,
      f"C3 the three mass choices give a = c H, 2 c H, c H/2 -- every one a RATIONAL multiple of c H "
      f"({sp.nsimplify(a_force_hor/(c*H))}, {sp.nsimplify(a_force_lam/(c*H))}, "
      f"{sp.nsimplify(a_grav_lam/(c*H))}), never a sqrt(8pi/3)-free rate")

banner("L-D  PADMANABHAN'S EMERGENCE LAW -- THE 8 pi/3 IS THE ROUTE'S OUTPUT, NOT ITS CHOICE")

dVdt = -4 * sp.pi * c ** 3 * Hd / H ** 4
check(sp.simplify(sp.diff(V, H) * Hd - dVdt) == 0,
      "D1 dV/dt = (dV/dH) Hdot = -4 pi c^3 Hdot/H^4 (differentiated, not asserted)")
N_bulk = -2 * (eps + 3 * pr) * V / kT
# Padmanabhan 2012: dV/dt = L_p^2 (N_sur - N_bulk) in c = 1 units; restoring c gives dV/dt = c L_p^2 (...).
# HAZARD NOTE: the c-restoration is not cosmetic -- omitting it produced a stray H^2/c in D3 and, because two
# errors cancelled under p = -eps, D4 still passed. D3 is the check that caught it. Both are kept.
emergence = sp.Eq(dVdt / (c * Lp2), N_dof - N_bulk)
sol_Hd = sp.solve(emergence, Hd)
check(len(sol_Hd) == 1, "D2 the emergence law solves uniquely for Hdot")
accel_over_a = sp.simplify(sol_Hd[0] + H ** 2)     # a_ddot/a = Hdot + H^2
target_ray = sp.simplify(-4 * sp.pi * G * (eps + 3 * pr) / (3 * c ** 2))
check(sp.simplify(accel_over_a - target_ray) == 0,
      f"D3 the emergence law reproduces the SECOND FRIEDMANN EQUATION exactly: a_ddot/a = "
      f"{sp.nsimplify(accel_over_a)} = -(4 pi G/3)(eps + 3p)/c^2 (hbar and L_p cancel identically)")
H_from = sp.solve(sp.Eq(accel_over_a.subs(pr, -eps), H ** 2), H)
H_pos = [s for s in H_from if sp.simplify(s ** 2 - 8 * sp.pi * G * eps / (3 * c ** 2)) == 0]
check(len(H_pos) >= 1,
      f"D4 for w = -1 it therefore OUTPUTS H^2 = 8 pi G rho/3: the Friedmann factor 8 pi/3 is a THEOREM of the "
      f"holographic route, so the route cannot be asked to drop it. It is what makes the floor c H rather than "
      f"(1/4) c sqrt(G rho)")
check(abs(float(sp.sqrt(8 * sp.pi / 3)) / 0.25 - float(TWOZ)) < 1e-9,
      f"D5 quantitatively: the route's coefficient on the bare rate is sqrt(8pi/3) = "
      f"{float(sp.sqrt(8*sp.pi/3)):.8f} against the target 0.25000000 -- short by exactly 2Z = "
      f"{float(TWOZ):.6f}")

banner("L-E  THE NO-GO, EXACT:  THE TARGET NEEDS pi^(-1/2), AND HORIZON DATA CANNOT SUPPLY IT")

# a = (c^2/L_p) sqrt(X/S).  Solve for X for each candidate.
Lp = sp.sqrt(Lp2)
aP = c ** 2 / Lp
X_of = lambda a_expr: sp.simplify(sp.simplify((a_expr / aP) ** 2 * S))
X_cH = X_of(c * H)
X_tgt = X_of(c * sp.sqrt(G * rho_L) / 4)
check(sp.simplify(X_cH - sp.pi) == 0,
      f"E1 in the variable X defined by a = (c^2/L_p) sqrt(X/S):  c H_Lambda has X = {sp.nsimplify(X_cH)} = pi")
check(sp.simplify(X_tgt - sp.Rational(3, 128)) == 0,
      f"E2 the framework's floor has X = {sp.nsimplify(X_tgt)} = 3/128 -- a RATIONAL, with NO pi. This is the "
      f"brief's structural point made exact: the bare density rate is pi-FREE in entropy variables, because "
      f"the area's 4 pi cancels the Friedmann 8 pi/3 down to a rational")
check(sp.simplify(sp.sqrt(sp.Rational(3, 128) / sp.pi) - 1 / TWOZ) == 0,
      f"E3 consistency: sqrt((3/128)/pi) = 1/(2Z) = {float(1/TWOZ):.12f} = target/(c H_Lambda)")
check(sp.simplify(sp.Rational(3, 128) - sp.Rational(1, 4) ** 2 * sp.Rational(3, 8)) == 0,
      "E4 and 3/128 = (1/4)^2 x (3/8) factorises as [the wanted 1/4]^2 x [inverse Friedmann 3/8] -- so the "
      "whole question is whether a HORIZON construction can supply a bare rational 1/4 outside the area")

# the field-theoretic obstruction
ps = sp.Symbol("pi_val", positive=True)     # pi carried as an unknown, so "pi must be rational" is COMPUTED
Cr = sp.Rational(7, 81)                     # an arbitrary probe rational coefficient on c H
pi_forced = sp.solve(sp.Eq(Cr ** 2 * ps, sp.Rational(3, 128)), ps)
check(len(pi_forced) == 1 and sp.nsimplify(pi_forced[0]).is_rational,
      f"E5 if the coefficient C on c H were RATIONAL then X = C^2 pi = 3/128 forces pi = "
      f"{sp.nsimplify(pi_forced[0])}, a RATIONAL -- contradicting Lindemann 1882 (pi transcendental). So no "
      f"rational multiple of c H is the target, for any rational however contrived")
xx, tt = sp.symbols("x t")
fl = sp.factor_list(tt ** 2 - xx, tt)
irred = len(fl[1]) == 1 and fl[1][0][1] == 1 and sp.degree(fl[1][0][0], tt) == 2
check(irred,
      f"E6 the general statement, computed: pi transcendental (Lindemann) => Q(pi) is isomorphic to the "
      f"rational function field Q(x), and t^2 - x is IRREDUCIBLE over Q(x) (factor_list returns "
      f"{len(fl[1])} factor of degree {sp.degree(fl[1][0][0], tt)}), so x is not a square there and sqrt(pi) is "
      f"NOT in Q(pi). A coefficient C in Q(pi) gives X = C^2 pi rational only if C = sqrt(X/pi), which lies "
      f"OUTSIDE Q(pi). NO-GO for every Q(pi) coefficient")
# and the premise is verified, not assumed: every candidate above has a coefficient in Q(pi) (in fact in Q)
cands = {
    "equipartition, N = A/L_p^2 (Padmanabhan)": a_dof,
    "equipartition, N = A/(4L_p^2) = S (Bekenstein-Hawking bits)": a_bits,
    "F = T dS/dR over the equipartition mass": a_force_hor,
    "F = T dS/dR over rho_Lambda V": a_force_lam,
    "G rho_Lambda V / R^2 (energy density over area)": a_grav_lam,
    "Verlinde de Sitter volume entropy, floor a_0/2 = c H/12": c * H / 12,
}
coeffs = {n: sp.nsimplify(sp.simplify(a / (c * H))) for n, a in cands.items()}
check(all(v.is_rational for v in coeffs.values()),
      f"E7 PREMISE VERIFIED, not assumed: all {len(coeffs)} candidates have coefficients on c H that are "
      f"RATIONAL ({', '.join(str(v) for v in coeffs.values())}) -- so E5/E6 apply to every one of them")
check(all(sp.simplify(a - c * sp.sqrt(G * rho_L) / 4) != 0 for a in cands.values()),
      "E8 and NONE of them equals the target (symbolic inequality, checked candidate by candidate)")
print("\n  {:<62}{:>12}{:>14}{:>12}".format("candidate", "coef x cH", "coef x bare", "r = 2/q"))
print("  " + "-" * 100)
rows = []
for n, a in cands.items():
    C = sp.simplify(a / (c * H))
    bare = sp.simplify(C * sp.sqrt(8 * sp.pi / 3))
    r_val = sp.simplify(1 / C)             # q = a_0/cH = 2k/cH = 2C  ->  r = 2/q = 1/C
    rows.append((n, C, bare, r_val))
    print(f"  {n:<62}{str(sp.nsimplify(C)):>12}{float(bare):>14.8f}{float(r_val):>12.6f}")
print(f"  {'TARGET  (framework floor a_0/2)':<62}{'1/(2Z)':>12}{0.25:>14.8f}{float(TWOZ):>12.6f}")
print(f"  {'rival    (conventional 2 pi a_0 ~ c H_Lambda)':<62}{str(sp.nsimplify(1/FOURPI)):>12}"
      f"{float(sp.sqrt(8*sp.pi/3)/FOURPI):>14.8f}{float(FOURPI):>12.6f}")
nearest = min(rows, key=lambda t: abs(float(t[2]) / 0.25 - 1))
check(all(abs(float(b) - 0.25) > 1e-6 for _, _, b, _ in rows),
      f"E9 no EXACT hit anywhere. Nearest on the bare rate is '{nearest[0]}' at {float(nearest[2]):.8f} vs the "
      f"target 0.25000000, a {100*abs(float(nearest[2])/0.25-1):.2f}% miss")


def in_Qpi(expr, nmax=4):
    """Is expr a rational times an integer power of pi (i.e. the operative subset of Q(pi))?"""
    for n in range(-nmax, nmax + 1):
        v = sp.nsimplify(sp.simplify(expr * sp.pi ** n))
        if v.is_rational:
            return True, -n
    return False, None


C_target = sp.simplify(1 / TWOZ)
C_conv = sp.simplify(1 / FOURPI)               # conventional floor: 2 pi a_0 ~ cH -> k = cH/(4 pi)
tgt_in, _ = in_Qpi(C_target)
conv_in, conv_n = in_Qpi(C_conv)
ghn_in, _ = in_Qpi(sp.Integer(1))
check((not tgt_in) and conv_in and ghn_in,
      f"E10 membership test: the GH coefficient (1) and the CONVENTIONAL floor coefficient 1/(4 pi) = "
      f"rational x pi^({conv_n}) both lie in Q(pi), while the framework's 1/(2Z) does NOT (no rational x pi^n "
      f"with |n| <= 4 equals it). The number field of horizon thermodynamics FAVOURS THE COMPETITORS and "
      f"excludes the framework's coefficient")

banner("L-F  THE GUARD -- FREE CHOICES, PRICED")

print("""  Free choices in the best (equipartition) candidate, counted honestly:
     1. bit count:  N = A/L_p^2 (Padmanabhan dof)  vs  N = A/(4 L_p^2) (Bekenstein-Hawking bits)   [factor 4]
     2. equipartition:  E = (1/2) N k T  vs  E = N k T                                             [factor 2]
     3. mass:  equipartition mass c^2R/G  vs  Komar/vacuum mass rho_Lambda V = c^2R/2G             [factor 2]
     4. surface vs bulk:  area 4 pi R^2  vs  volume (4 pi/3) R^3 / R                               [factor 3]
   NOT free (degenerate in de Sitter, so no credit is taken for them): horizon vs apparent horizon (identical
   for dS), and a = G M/R^2 vs a = c^2/R (identical for the horizon mass). => THREE-to-FOUR genuinely free
   choices, generating the multiplicative lattice 2^i 3^j.""")
FREE_CHOICES = 3
lat = sorted({2 ** i * 3 ** j for i in range(-5, 6) for j in range(-2, 3)})
tgt = float(1 / TWOZ)
best = min(lat, key=lambda v: abs(math.log(v / tgt)))
check(abs(best - tgt) > 1e-12,
      f"F1 the 2^i 3^j lattice reachable from those choices comes closest at {sp.nsimplify(sp.Rational(best))} "
      f"= {best:.8f} against the target {tgt:.8f} -- a {100*abs(best/tgt-1):.2f}% miss and, being RATIONAL, it "
      f"can NEVER be exact (E5)")
# price the freedom: how well does such a lattice hit a GENERIC O(1) target?
probes = [0.05 * (100.0 / 0.05) ** (i / 400.0) for i in range(401)]
misses = [min(abs(math.log(v / t)) for v in lat) for t in probes]
worst, med = max(misses), sorted(misses)[len(misses) // 2]
check(math.exp(med) - 1 < 0.0787,
      f"F2 PRICED: that lattice hits a GENERIC O(1) target to within a MEDIAN of "
      f"{100*(math.exp(med)-1):.2f}% (worst case {100*(math.exp(worst)-1):.2f}%). Since separating 2Z from "
      f"4 pi needs better than 7.87%, a few-percent 'hit' from these choices carries NO evidence at all")
check(math.exp(worst) - 1 > 0.05,
      f"F3 the lattice is nevertheless NOT dense (worst-case {100*(math.exp(worst)-1):.2f}% > 5%), so this is "
      f"an honest pricing of a real freedom, not a claim that the choices can reach anything")
# best simple rational, by continued fractions
from fractions import Fraction
f16 = Fraction(tgt).limit_denominator(16)
check(f16 == Fraction(1, 12) and abs(float(f16) - tgt) > 1e-9,
      f"F4 restricted to denominators a handful of 2s and 3s can build (q <= 16), the best rational is {f16} = "
      f"{float(f16):.8f}, i.e. r = {1/float(f16):.4f} -- EXACTLY Verlinde's a_0 = c H/6 (floor c H/12). Against "
      f"2Z = {float(TWOZ):.4f} that is a {100*abs(1/float(f16)/float(TWOZ)-1):.2f}% NEAR MISS; against "
      f"4 pi = {float(FOURPI):.4f}, {100*abs(1/float(f16)/float(FOURPI)-1):.2f}%. It sits between the two "
      f"rivals and cannot distinguish them, so it is NOT a lock")
errs = [abs(float(Fraction(tgt).limit_denominator(q)) / tgt - 1) for q in (16, 64, 1000, 100000)]
check(errs[0] > errs[1] > errs[2] > errs[3] and errs[3] < 1e-6,
      f"F4b AND THE NEAR-MISS GAME IS UNBOUNDED, which is why only exactness counts: allowing bigger "
      f"denominators drives the miss monotonically to zero -- q<=16: {100*errs[0]:.2f}%, q<=64: "
      f"{100*errs[1]:.2f}% (5/58, whose 58 = 2 x 29 has no entropy origin whatever), q<=1000: "
      f"{100*errs[2]:.4f}%, q<=1e5: {100*errs[3]:.6f}%. A rational can be made to LOOK like the target to any "
      f"precision while never being it (E5)")
check(abs(float(sp.sqrt(8 * sp.pi / 3) / 12) - 0.2412) < 1e-4,
      f"F5 in bare-rate units Verlinde's floor is sqrt(8pi/3)/12 = {float(sp.sqrt(8*sp.pi/3)/12):.8f} against "
      f"0.25000000 -- a 3.52% miss. INDEPENDENT PREDICTION of a construction TUNED to 1/4: none. "
      f"THREE free choices and no independent prediction is NUMEROLOGY, in those words")

banner("L-G  RECONCILIATION -- WHAT IS NEW, WHAT IS A REDISCOVERED CLOSED DOOR")

# reproduce the prior committed result: bare-radius free-fall screen -> 4 pi/3
rho_s = sp.Symbol("rho", positive=True)
R_ff = c / sp.sqrt(G * rho_s)
a_ff = sp.simplify(G * (sp.Rational(4, 3) * sp.pi * R_ff ** 3 * rho_s) / R_ff ** 2)
check(sp.simplify(a_ff / (c * sp.sqrt(G * rho_s)) - 4 * sp.pi / 3) == 0,
      f"G1 REPRODUCES real_research/reviews/derive_Z_equipartition_attempt.py: a screen placed by hand at the "
      f"BARE radius c/sqrt(G rho) gives {sp.nsimplify(a_ff/(c*sp.sqrt(G*rho_s)))} = 4 pi/3 = "
      f"{float(4*sp.pi/3):.8f}, not 1/4 -- off by 16 pi/3 = {float(16*sp.pi/3):.4f}x. Choosing the radius by "
      f"hand does not remove the pi; it moves it")
ckn = (sp.Rational(3, 1) / (8 * sp.pi)) ** sp.Rational(1, 4)
check(abs(float(ckn) - 0.5878) < 1e-4 and sp.simplify(ckn ** 4 - sp.Rational(3, 8) / sp.pi) == 0,
      f"G2 DISTINCT from the CLOSED CKN bridge: that lives at (3/8pi)^(1/4) = {float(ckn):.6f}, a pi^(-1/4) "
      f"object, whereas this lane's target is a pi^(-1/2) object -- different number field, so this is not a "
      f"re-run of the CKN door (which stays closed: 0.5878 is the g* = 1 geometric limit)")
print("""
  PARTLY A REDISCOVERED CLOSED DOOR -- stated plainly, as required.
    real_research/reviews/desitter_entropy_coefficient.py already argued (heuristically) that entropy/horizon
    coefficients are rational x pi^n while Z = sqrt(32 pi/3) carries a square root, hence cannot match. Lane L
    CONFIRMS that door is shut and adds four things it did not have: (i) the exact X-variable statement
    a = (c^2/L_p) sqrt(X/S) with X = pi for c H against X = 3/128 for the target, which shows the target is
    pi-FREE rather than merely 'a square root'; (ii) the Lindemann-based proof that sqrt(pi) is not in Q(pi),
    upgrading the heuristic to a theorem CONDITIONAL on a verified premise (E7); (iii) the exact result that
    Bekenstein-Hawking's 1/4 DOES appear -- as c H/4 -- and misses by exactly sqrt(8pi/3); and (iv) the
    Padmanabhan check D3 showing the 8 pi/3 is the route's OUTPUT (the second Friedmann equation), so it cannot
    be negotiated away.""")

# reconcile with the independently derived admissibility ceiling
R_MAX = 9.0168      # mi_r_admissibility_bound_2026.py, 7 shapes x 220 scales
rs = [float(r) for _, _, _, r in rows]
check(float(TWOZ) > R_MAX and float(FOURPI) > R_MAX,
      f"G3 the admissibility ceiling r_max = {R_MAX} (mi_r_admissibility_bound_2026.py) EXCLUDES both "
      f"r = 2Z = {float(TWOZ):.4f} and r = 4 pi = {float(FOURPI):.4f}; so a lock at 2Z here would have had to "
      f"be reconciled with it. No reconciliation is needed, because no lock was found")
check(all(r <= R_MAX for r in rs if abs(r - 12.0) > 1e-9) and any(r > R_MAX for r in rs),
      f"G4 and every entropy candidate EXCEPT Verlinde's r = 12 is admissible ({sorted(rs)}); two of them, "
      f"r = 1 and r = 2, are EXACTLY Milgrom 1999's eqs 6-9 and eqs 10-11. Two independent structures -- the "
      f"number field and the admissibility bound -- agree in excluding 2Z")

banner("AGAINST INTEREST")
print("""  Recorded because it is the honest direction of the search:
   - Lane L does not merely fail to derive the framework's 1/4; it points at the RIVALS. The number field Q(pi)
     that horizon thermodynamics lives in CONTAINS r = 1 (Milgrom 1999) and r = 4 pi (the conventional
     2 pi a_0 ~ c H_Lambda) and PROVABLY EXCLUDES r = 2Z. The most principled member of the family -- plain
     holographic equipartition, which independently gives Newton's inverse-square law AND, through Padmanabhan's
     emergence law, the Friedmann equation -- lands on a = c H exactly, i.e. a_0 = 2 c H_Lambda, Milgrom's 1999
     coefficient, 11.578x away from the framework's floor.
   - The one place Bekenstein-Hawking's 1/4 does survive is a = c H/4 = 1.355e-10 m/s^2, which is nearer
     McGaugh's fitted a_0 ~ 1.2e-10 than to the framework's floor 4.681e-11. That is a coincidence, not a
     result, and it is recorded so it cannot later be sold as one.
   - The 1/4 cannot travel. S = A/4 attaches the 1/4 to an AREA; an acceleration built from an area enters
     through R ~ sqrt(A), and a square root turns 1/4 into 1/2, not 1/4. (That the square root of the BH 4
     lands on kappa = 1/2 is exactly the kind of resemblance this project has been burned by: it requires
     writing an effective density rho_Lambda/4 or an effective G/4 with no principle behind either, it has no
     independent prediction, and it is reported here as NUMEROLOGY, not as a lead.)
   - kappa = 1/2 is FITTED, NOT DERIVED, and nothing above changes that.

  WHAT REMAINS OPEN (and it is precisely the brief's one structurally open route):
   - A derivation whose ONLY dimensional input is rho_Lambda, that never mentions the horizon, never forms an
     area, and never invokes H. Such a construction has no 8 pi/3 available to it, so it cannot land on c H;
     E2 shows the target is then a bare rational 3/128 = (1/4)^2 (3/8). Lane L closes the HORIZON route and says
     nothing against that one. NEVER 'no open doors'.""")

banner("RESULT")
n = sum(1 for cnd, _ in ok if cnd)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for cnd, m in ok:
        if not cnd:
            print(f"    - {m}")
    sys.exit(1)
print(f"""  Exit 0.  VERDICT: NO EXACT LOCK. Bekenstein-Hawking's 1/4 is not the framework's 1/4. Every horizon
  construction carried here lands on a RATIONAL multiple of c H_Lambda -- {{1/4, 1/2, 1, 2, 1/12}} -- and the
  target, {float(1/TWOZ):.12f} = sqrt((3/128)/pi), is irrational by Lindemann, so the miss is structural and not
  a matter of trying harder. Best near miss: Verlinde's floor c H/12 -> 0.24120 against 0.25, 3.52% off, which
  cannot distinguish 2Z = {float(TWOZ):.6f} from 4 pi = {float(FOURPI):.6f} (they differ by 7.87%). Free choices
  in the best candidate: {FREE_CHOICES}. Independent prediction of a construction tuned to the target: NONE ->
  numerology. kappa = 1/2 remains FITTED, NOT DERIVED.""")
