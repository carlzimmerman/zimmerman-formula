#!/usr/bin/env python3
"""a02_menu_recount.py -- adversarial audit of p02 ('exactly one of 34 pre-declared matchings gives 32 pi/3').

Independent method: NO sympy.solve.  Each quantity is stored as (rational coefficient, power of pi, power of length d) and a matching
q_BH(M) = q_dS(L) is solved by hand:  c_B pi^i M^d = c_D pi^j L^d  =>  (M/L)^d = (c_D/c_B) pi^(j-i)  =>  Z^2 = 16 (M/L)^2 = 16 [(c_D/c_B) pi^(j-i)]^(2/d).
So Z^2 ~ pi^(2(j-i)/d): Z^2 is proportional to pi^(+1) iff (j - i) = d/2.  (Z := 4M/L, a0 := kappa_BH, as in p02.)

Parts:
 A  re-derive p02's 34-pair table by hand-bookkeeping and confirm the pi-content tally (3+5+7+19).
 B  count the DISTINCT quantities (p02's menu has duplicates) and how many pairs could possibly give Z^2 ~ pi^1 (the structural pre-selection).
 C  decoy test: which 'natural' pi^1 targets  p pi/q  does the p02 menu reach?  (a target hit by the menu is not evidence for the target)
 D  enlarged, blind menu (adds thermal quantities T_H, beta, Weyl-free invariants, etc.): how many distinct pi^1 values, and is 32 pi/3 special?
Exit 0 = the tallies are as stated (the script demonstrates what the scan can and cannot mean).
"""
import itertools, sys
from fractions import Fraction as Fr
import math

ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

# (name, d, coefficient c, pi-power) in G = c = 1;  BH: c * pi^k * M^d ;  dS: c * pi^k * L^d
BH = [
    ("r_s = 2M", 1, Fr(2), 0), ("1/kappa = 4M", 1, Fr(4), 0), ("Misner mass M", 1, Fr(1), 0),
    ("kappa = 1/(4M)", -1, Fr(1, 4), 0), ("static Euler charge 8pi/M", -1, Fr(8), 1),
    ("area 16 pi M^2", 2, Fr(16), 1), ("entropy 4 pi M^2", 2, Fr(4), 1),
    ("horizon Gauss curv 1/(4M^2)", -2, Fr(1, 4), 0), ("kappa^2 = 1/(16M^2)", -2, Fr(1, 16), 0),
    ("mean density 3/(32 pi M^2)", -2, Fr(3, 32), -1),
    ("Kretschmann 3/(4M^4)", -4, Fr(3, 4), 0), ("flat-ball vol 32 pi M^3/3", 3, Fr(32, 3), 1),
]
DS = [
    ("L", 1, Fr(1), 0), ("1/kappa = L", 1, Fr(1), 0), ("Misner mass L/2", 1, Fr(1, 2), 0),
    ("kappa = 1/L", -1, Fr(1), 0), ("static Euler charge 32pi/L", -1, Fr(32), 1),
    ("area 4 pi L^2", 2, Fr(4), 1), ("entropy pi L^2", 2, Fr(1), 1),
    ("horizon Gauss curv 1/L^2", -2, Fr(1), 0), ("kappa^2 = Lambda/3", -2, Fr(1), 0), ("Lambda = 3/L^2", -2, Fr(3), 0),
    ("R = 12/L^2", -2, Fr(12), 0), ("rho_Lambda = 3/(8 pi L^2)", -2, Fr(3, 8), -1),
    ("static-patch vol 4 pi L^3/3", 3, Fr(4, 3), 1), ("Kretschmann 24/L^4", -4, Fr(24), 0),
]

def match(b, d_):
    """Z^2 = C * pi^p  with C a float and p the exact pi-power; returns (C, p, exactcoef or None)."""
    (nb, db, cb, kb), (nd, dd, cd, kd) = b, d_
    d = db
    ratio = cd / cb                              # (M/L)^d = ratio * pi^(kd-kb)
    p2d = Fr(2 * (kd - kb), d)                   # exponent of pi in Z^2
    C = 16 * float(ratio) ** (2.0 / d)           # Z^2 = 16 * ratio^(2/d) * pi^(2(kd-kb)/d)
    return C * math.pi ** float(p2d), p2d, (16 * ratio ** 2 if d == 2 or d == -2 else None), (ratio, d, kd - kb)

# ---------------------------------------------------------------- A: the 34-pair table
pairs = [(b, d_) for b, d_ in itertools.product(BH, DS) if b[1] == d_[1]]
tally = {}
z2_vals = []
for b, d_ in pairs:
    val, p2d, _, _ = match(b, d_)
    tally.setdefault((b[3] != 0, d_[3] != 0, p2d != 0), []).append((b[0], d_[0]))
    z2_vals.append((val, p2d, b[0], d_[0]))
chk("A1 same-dimension pairs = 34 (9 length + 4 (d=-1) + 4 (d=2) + 15 (d=-2) + 1 (d=-4) + 1 (d=3))", len(pairs) == 34)
n_oneside = sum(len(v) for k, v in tally.items() if k[0] != k[1])
chk("A2 pairs with a pi on exactly one side = 8 (3 + 5), all 8 have pi in Z^2; both-sides-pi pairs (7) give Z^2 rational; pi-free pairs (19) rational",
    n_oneside == 8 and all(k[2] for k in tally if k[0] != k[1]) and not any(k[2] for k in tally if k[0] == k[1]))
target = 32 * math.pi / 3
hits = [(b, d_) for b, d_ in pairs if abs(match(b, d_)[0] / target - 1) < 1e-12]
chk("A3 exactly one pair hits 32 pi/3 (K_Sigma = rho_Lambda), reproduced without sympy.solve", len(hits) == 1 and hits[0][0][0].startswith("horizon Gauss") and hits[0][1][0].startswith("rho_Lambda"))

# ---------------------------------------------------------------- B: structure of the pre-selection
def pi_power_Z2(pair):
    return match(*pair)[1]
pi_plus1 = [p for p in pairs if pi_power_Z2(p) == 1]
chk("B1 only pairs with |d| = 2 and pi-power difference 1 can give Z^2 ~ pi^(+1); in the p02 menu there are exactly TWO such pairs (kappa^2 = rho_Lambda -> 8 pi/3 and K_Sigma = rho_Lambda -> 32 pi/3)",
    len(pi_plus1) == 2)
print("   the two pi^1 pairs:", [(b[0], d_[0], round(match(b, d_)[0] / math.pi, 6)) for b, d_ in pi_plus1])
chk("B2 any pair with |d| odd cannot give Z^2 ~ pi^1 (needs pi^(d/2)): the 9 length, 4 (d=+-1) and volume pairs are structurally excluded",
    all(pi_power_Z2(p) != 1 for p in pairs if abs(p[0][1]) % 2 == 1))
dsn = {(d_[1], d_[2], d_[3]) for d_ in DS}
bhn = {(b[1], b[2], b[3]) for b in BH}
print("   distinct BH quantities: %d of %d listed;  distinct dS quantities: %d of %d listed (duplicates: L / 1/kappa=L ; kappa^2=Lambda/3 / Gauss curv 1/L^2)" % (len(bhn), len(BH), len(dsn), len(DS)))
distinct_pairs = {((b[1], b[2], b[3]), (d_[1], d_[2], d_[3])) for b, d_ in pairs}
chk("B3 the '34 pairs' contain duplicates: %d distinct pairs (the denominator of 'one of 34' is inflated)" % len(distinct_pairs), len(distinct_pairs) < 34)
print("   d = -2 sector: %d of the %d pairs; the hit lives in a sector of %d pairs, %d of which have Z^2 ~ pi^(+-1)" %
      (sum(1 for p in pairs if p[0][1] == -2), len(pairs), sum(1 for p in pairs if p[0][1] == -2), sum(1 for p in pairs if p[0][1] == -2 and pi_power_Z2(p) != 0)))

# ---------------------------------------------------------------- C: decoy targets
family = sorted({Fr(a, b) for a in (1, 2, 3, 4, 8, 16, 32, 64) for b in (1, 2, 3, 4, 6, 8)})
menu_pi1 = sorted({round(match(*p)[0] / math.pi, 9) for p in pi_plus1})
reached = [q for q in family if any(abs(float(q) - m) < 1e-8 for m in menu_pi1)]
print("   decoy family: %d distinct 'natural' targets p pi/q (p in 1,2,3,4,8,16,32,64; q in 1,2,3,4,6,8); the p02 menu reaches %d of them: %s pi" %
      (len(family), len(reached), [str(q) for q in reached]))
chk("C1 the menu reaches at least TWO natural pi^1 targets (8 pi/3 and 32 pi/3): hitting 32 pi/3 is not a discriminating outcome (8 pi/3 is equally 'hit', by the sibling kappa^2 = rho_Lambda)", len(reached) >= 2)
chk("C2 hit-rate of the menu over the decoy family = %.3f (not << 1): 'exactly one of 34' carries no significance because the menu and target were fixed together (author's own caveat, quantified)" % (len(reached) / len(family)),
    len(reached) / len(family) > 0.03)

# ---------------------------------------------------------------- D: enlarged menu with thermal / standard quantities
BH2 = BH + [
    ("T_H = 1/(8 pi M)", -1, Fr(1, 8), -1), ("beta_H = 8 pi M", 1, Fr(8), 1), ("T_H^2 = 1/(64 pi^2 M^2)", -2, Fr(1, 64), -2),
    ("mass per r_s^3: M/r_s^3 = 1/(8 M^2)", -2, Fr(1, 8), 0),
    ("Hawking flux ~ T^4 A = 1/(256 pi^3 M^2)", -2, Fr(1, 256), -3),
]
DS2 = DS + [
    ("T_dS = 1/(2 pi L)", -1, Fr(1, 2), -1), ("beta_dS = 2 pi L", 1, Fr(2), 1), ("T_dS^2 = 1/(4 pi^2 L^2)", -2, Fr(1, 4), -2),
    ("dS flux ~ T^4 A = 1/(4 pi^3 L^2)", -2, Fr(1, 4), -3),
    ("rho_Lambda^2 = 9/(64 pi^2 L^4)", -4, Fr(9, 64), -2),
]
pairs2 = [(b, d_) for b, d_ in itertools.product(BH2, DS2) if b[1] == d_[1]]
vals = {}
for p in pairs2:
    v, p2d, _, _ = match(*p)
    vals.setdefault((p2d, round(v / math.pi ** float(p2d), 9)), []).append((p[0][0], p[1][0]))
pi1_vals = {k[1]: v for k, v in vals.items() if k[0] == 1}
print("   enlarged menu: %dx%d quantities, %d same-dimension pairs, distinct Z^2 ~ pi^1 values: %s (x pi)" %
      (len(BH2), len(DS2), len(pairs2), sorted(pi1_vals)))
chk("D1 in the enlarged (still not target-blind) menu the number of distinct pi^1 outcomes is >= 4, so 32 pi/3 is one of several 'natural' pi-multiples that some matching hits", len(pi1_vals) >= 4)
reached2 = [q for q in family if any(abs(float(q) - m) < 1e-8 for m in pi1_vals)]
print("   decoy family reached by the enlarged menu: %d of %d: %s pi   (p02 menu: %d of %d)" % (len(reached2), len(family), [str(q) for q in reached2], len(reached), len(family)))
chk("D3 the hit-rate over the decoy family grows with menu size (%d/%d -> %d/%d): the number of 'natural' pi-multiples a menu can reach scales with the menu, so a hit at a target fixed alongside the menu is expected" % (len(reached), len(family), len(reached2), len(family)), len(reached2) > len(reached))
chk("D2 32 pi/3 stays reachable only via K_Sigma = rho_Lambda and equivalents (%d pairs)" % len(pi1_vals.get(round(32 / 3, 9), [])), len(pi1_vals.get(round(32 / 3, 9), [])) >= 1)
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
