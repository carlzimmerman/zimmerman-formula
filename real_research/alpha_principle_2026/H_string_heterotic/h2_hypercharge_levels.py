#!/usr/bin/env python3
"""H2 -- Kac-Moody level of hypercharge, k_Y = 2 sum a_i^2 (Dienes Eq. 5.7), from explicit charge-lattice embeddings, and what the level does and does not fix.
Pre-registered L1-L5 in H0_PREREGISTRATION.md.  Inputs read (full text): Dienes hep-th/9602045 Sect. 5.1-5.3 (Eq. 5.1-5.7, 5.17-5.19, 5.22).
Run: python3 h2_hypercharge_levels.py [MUTATE]   (MUTATE: k_Y = sum a_i^2, i.e. the factor 2 of Eq. 5.7 dropped; L1 must FAIL, exit 1)"""
import sys, itertools
from fractions import Fraction as F
from collections import Counter

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
checks = []
def chk(name, ok, info=""):
    checks.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")

def kY(a):
    return (1 if MUT else 2)*sum(x*x for x in a)

# ---- L1: 16 of SO(10), spinor weights (+-1/2)^5 with an even number of minus signs
a = [F(1, 3)]*3 + [F(1, 2)]*2
half = F(1, 2)
states = [q for q in itertools.product([half, -half], repeat=5) if sum(1 for x in q if x < 0) % 2 == 0]
Ys = Counter(sum(ai*qi for ai, qi in zip(a, q)) for q in states)
print("L1 hypercharge multiset on the 16 (Y = a.q):", dict(sorted(Ys.items())))
SM16 = Counter({F(1, 6): 6, F(-2, 3): 3, F(1, 3): 3, F(-1, 2): 2, F(1): 1, F(0): 1})   # Q, u^c, d^c, L, e^c, nu^c  (Y_eR^c = +1 normalisation)
chk("L1a the 16 reproduces the SM hypercharge multiset (Q 1/6 x6, u^c -2/3 x3, d^c 1/3 x3, L -1/2 x2, e^c 1, nu^c 0)", Ys == SM16)
k5 = kY(a)
print(f"   k_Y = {'sum' if MUT else '2 sum'} a_i^2 = {k5}")
chk("L1b k_Y = 5/3 exactly for the SU(5)/SO(10) embedding", k5 == F(5, 3))

# ---- L2: Dienes Eq. 5.18/5.19 (hypercharge with Z/4 moding): rows as printed
a2 = [F(5, 12)]*3 + [F(3, 8)]*2
rows = {"Q_L": ([F(-1, 2), F(-1, 2), F(1, 2), 0, 1], F(1, 6)),
        "u_R": ([F(1, 4), F(1, 4), F(-3, 4), F(-3, 4), F(-3, 4)], F(-2, 3)),
        "d_R": ([F(3, 4), F(3, 4), F(-1, 4), F(-1, 4), F(-1, 4)], F(1, 3)),
        "L_L": ([F(-1, 4), F(-1, 4), F(-1, 4), F(-3, 4), F(1, 4)], F(-1, 2)),
        "e_R": ([F(1, 2)]*5, F(1)),
        "H+": ([F(1, 4), F(1, 4), F(1, 4), F(3, 4), F(-1, 4)], F(1, 2)),
        "H-": ([F(-1, 4), F(-1, 4), F(-1, 4), F(-3, 4), F(1, 4)], F(-1, 2))}
okrows = True
for nme, (Q, Yexp) in rows.items():
    Y = sum(ai*F(qi) for ai, qi in zip(a2, Q))
    okrows &= (Y == Yexp)
    print(f"   {nme}: Y = {Y} (expected {Yexp})")
k77 = kY(a2)
print(f"   k_Y = {k77}")
chk("L2a Dienes 5.18 rows give the SM hypercharges under Y = 5/12 (Q1+Q2+Q3) + 3/8 (Q4+Q5)", okrows)
chk("L2b k_Y = 77/48 < 5/3 for this Z/4 embedding (Dienes: 'kY = 77/48')", k77 == F(77, 48))

# ---- L3: tree-level ratios from the levels
print("\nL3 tree-level ratios at the string scale (alpha_i = alpha_G/k_i):")
print("   k_Y      k_2  sin^2 theta_W(M_s)=k_2/(k_2+k_Y)   alpha_em(M_s)/alpha_G = 1/(k_2+k_Y)")
for ky in (F(5, 3), F(77, 48), F(11, 3), F(14, 3)):
    k2 = F(1)
    print(f"   {str(ky):8s} {k2}    {k2/(k2+ky)} = {float(k2/(k2+ky)):.5f}                    {1/(k2+ky)} = {float(1/(k2+ky)):.5f}")
chk("L3 k_Y = 5/3, k_2 = 1 gives sin^2 theta_W = 3/8 and alpha_em = (3/8) alpha_G (matches lane G)", (F(1)/(F(1)+F(5, 3)) == F(3, 8)) and (F(1, 1)/(F(1) + F(5, 3)) == F(3, 8)))
print("   => the level changes alpha_em(M_s)/alpha_G by O(1) factors (0.384 ... 0.176 over the listed values) and is a DISCRETE embedding choice; it does not fix alpha_G.")

# ---- L4: modular invariance + no fractionally charged colour-neutral states, Dienes Eq. 5.22:  k3/3 + k2/4 + kY/4 = 0 (mod 1)
print("\nL4 allowed k_Y from k3/3 + k2/4 + kY/4 = 0 mod 1 (kY < 6):")
mins = {}
for (k2, k3) in ((1, 1), (2, 2)):
    allowed = []
    n = 0
    while True:
        ky = F(4*n) - F(4*k3, 3) - F(k2)
        if ky > 6: break
        if ky > 0: allowed.append(ky)
        n += 1
    mins[(k2, k3)] = min(allowed)
    print(f"   (k2,k3)=({k2},{k3}): k_Y in {[str(x) for x in allowed]}")
chk("L4 minimum allowed k_Y is 5/3 for (1,1) and 10/3 for (2,2) (Dienes: 5.23 and the following text)", mins[(1, 1)] == F(5, 3) and mins[(2, 2)] == F(10, 3))

# ---- L5: Green-Schwarz counting: dimension 496
dim_so32 = 32*31//2
dim_e8 = 248
chk("L5 dim SO(32) = 496 = dim E8 x E8 (the anomaly-cancelling groups; an INTEGER statement)", dim_so32 == 496 and 2*dim_e8 == 496)
print("   Statement of structure (RECALLED, Green-Schwarz 1984, not derived here): anomaly cancellation quantises the gauge group and the coefficients of the counterterm; the dilaton enters the")
print("   gauge kinetic term as e^{-2 phi} tr F^2 and is untouched by the cancellation, so the GS condition adds no equation for the coupling (same 'integer, not real' verdict as lane G).")

nfail = sum(1 for _, ok in checks if not ok)
print(f"\nSUMMARY: {len(checks)-nfail}/{len(checks)} checks pass" + (" [MUTATE]" if MUT else ""))
sys.exit(1 if nfail else 0)
