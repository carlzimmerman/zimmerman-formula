"""p18: the p17 conditions in Heaviside-Lorentz (rationalised) gravity units, G_H = 4 pi G (Poisson: lap Phi = G_H rho; Einstein: G_mn = 2 G_H T_mn).
Units relabel where pi sits; they cannot change a physical relation. Check: every p17 value k = G rho r^2/c^2 maps to k_H = G_H rho r^2/c^2 = 4 pi k,
the target 1 maps to 4 pi, and the ratio target/natural (= 8 pi/3 for the seven-fold 3/(8 pi) row) is unit-invariant.
Run: python3 p18_heaviside_units.py   |  MUTATE=1: the seven-row value is corrupted to 3/(4 pi) (G_H/G cancels in B, so a conversion mutation could not fail), check B must fail
"""
import os, sys
import sympy as sp
MUTATE = os.environ.get("MUTATE") == "1"
pi = sp.pi
conv = 4 * pi                                            # k_H = (G_H/G) k
p17 = {"C1,C2,C4,C6,C7,C11,C12 (seven rows)": 3 / (4 * pi) if MUTATE else 3 / (8 * pi), "C3,C9": 3 / (16 * pi), "C5": 1 / (16 * pi),
       "C10": 1 / (32 * pi), "C13": 1 / (8 * pi), "C8": 3 * pi / 32, "TARGET (the puzzle)": sp.Integer(1)}
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
print(f"{'condition':40s} {'Gaussian G rho r^2':>20s} {'Heaviside G_H rho r^2':>24s}")
for k, v in p17.items():
    print(f"{k:40s} {str(v):>20s} {str(sp.simplify(conv * v)):>24s}")
tH = sp.simplify(conv * p17["TARGET (the puzzle)"]); nH = sp.simplify(conv * p17["C1,C2,C4,C6,C7,C11,C12 (seven rows)"])
check(f"A in Heaviside units the natural conditions become pi-free rationals (seven rows: {nH}) and the TARGET picks up the pi ({tH})",
      nH.is_rational and not tH.is_rational)
check("B the physical gap target/natural is unit-invariant: 8 pi/3 in both systems",
      sp.simplify(tH / nH - 8 * pi / 3) == 0 and sp.simplify(1 / (3 / (8 * pi)) - 8 * pi / 3) == 0)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
