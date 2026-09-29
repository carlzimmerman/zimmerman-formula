#!/usr/bin/env python3
"""M1 -- red-team of lane A item I5 (one-loop SM running of alpha_em to the Planck scale).
Run:    python3 m1_lane_a_running_check.py            (exit 0 iff all checks pass)
MUTATE: python3 m1_lane_a_running_check.py MUTATE     (uses lane A's b_Y = 3/5*41/10; must exit 1)
"""
import sys
from fractions import Fraction as F
import mpmath as mp
mp.mp.dps = 30
MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
fails = []
def chk(name, ok, msg=""):
    print(("[PASS] " if ok else "[FAIL] ") + name + " " + msg)
    if not ok: fails.append(name)

# b_Y from field content (Q = T3 + Y). d alpha_Y^-1/d ln mu = -b_Y/(2 pi).
# b = (2/3) sum_{Weyl} Y^2 + (1/3) sum_{complex scalars} Y^2   (Dirac unit charge: 2/3*2 = 4/3, standard)
gen = [(6, F(1,6)), (3, F(2,3)), (3, F(-1,3)), (2, F(-1,2)), (1, F(-1))]   # (multiplicity, Y) Weyl: Q, u^c-like as (uR), (dR), L, eR
sumY2 = sum(n * y * y for n, y in gen)
bY_content = F(2,3) * 3 * sumY2 + F(1,3) * 2 * F(1,2)**2
print("b_Y from field content =", bY_content, "= %.6f" % float(bY_content))
chk("b_Y(field content) = 41/6", bY_content == F(41, 6))
chk("(5/3)*(41/10) = 41/6 (GUT-normalised b_1 -> alpha_Y normalisation)", F(5,3) * F(41,10) == F(41,6))
bY_laneA = F(3,5) * F(41,10)
print("lane A's script value 3/5*41/10 =", bY_laneA, "= %.4f  (ratio to correct: %.3f)" % (float(bY_laneA), float(bY_laneA / F(41,6))))
chk("lane A's b_Y differs from the correct value", bY_laneA != F(41,6))

bY = mp.mpf(bY_laneA.numerator)/bY_laneA.denominator if MUT else mp.mpf(41)/6
b2 = -mp.mpf(19)/6
# lane A inputs (a3): 1/alpha_em(mZ) = 127.95, sin^2 = 0.23122, mZ = 91.1876 GeV, m_P = 1.22089e19 GeV
aem = mp.mpf('127.95'); s2 = mp.mpf('0.23122'); mZ = mp.mpf('91.1876'); mP = mp.mpf('1.22089e19')
aY0 = aem * (1 - s2); a20 = aem * s2
L = mp.log(mP / mZ)
aYP = aY0 - bY / (2*mp.pi) * L; a2P = a20 - b2 / (2*mp.pi) * L
aemP = aYP + a2P
print("ln(mP/mZ) = %.4f ; 1/alpha_Y(mP) = %.3f ; 1/alpha_2(mP) = %.3f ; 1/alpha_em(mP) = %.3f" % (L, aYP, a2P, aemP))
# lane B printed value at M_Planck with alpha^-1(MZ) = 127.930: 104.917 (one loop)
chk("1/alpha_em(m_P) agrees with lane B (104.917) and lane F (104.94) to 1%", abs(aemP/mp.mpf('104.917') - 1) < 0.01, "got %.3f" % aemP)
chk("1/alpha_em(m_P) is NOT lane A's 132.39", abs(aemP - mp.mpf('132.39')) > 5, "got %.3f" % aemP)

alpha_T = 1/mp.mpf('137.035999177')
k_T = 1/(2*mp.sqrt(alpha_T))
k_P = 1/(2*mp.sqrt(1/aemP))
Z = 2*mp.sqrt(8*mp.pi/3)
print("required k = 1/(2 sqrt(alpha)): Thomson %.4f ; at m_P (this run) %.4f ; Z = %.4f ; Z/k_P = %.4f (offset %.2f %%)" % (k_T, k_P, Z, Z/k_P, 100*(Z/k_P-1)))
chk("post-hoc 'Z within 0.6% of required k at m_P' does not survive (offset > 5%)", abs(Z/k_P - 1) > 0.05, "offset %.2f%%" % (100*abs(Z/k_P-1)))
# sensitivity: how far is the spectrum-dependence from the 1e-3 hit level anyway
print("REPORT: 2-loop shift of alpha_em^-1(m_P) from lane B = 0.67 percent; hit window 0.1 percent -> no relation at m_P could be scored at 1e-3 with one-loop input")
print("SUMMARY: fails =", fails)
sys.exit(1 if fails else 0)
