"""p51: Padmanabhan's holographic equipartition as the missing premise for r* = c/sqrt(G rho_Lambda).
Premise: a sphere of radius r with surface temperature T = hbar a/(2 pi c k) is in equilibrium when N_sur = N_bulk, with N_sur = 4 pi r^2/l_P^2 (l_P^2 = hbar G/c^3)
and N_bulk = 2|E_Komar|/(k T), E_Komar = |rho + 3p/c^2| c^2 V = 2 rho c^2 (4 pi r^3/3) for vacuum (p = -rho c^2). Apply it to the a0 horizon: a = a0 = c^2/(2r).
Variants: (i) bulk counted without the Komar factor 2 (|E| = rho c^2 V); (ii) N_sur = A/(4 l_P^2) (entropy normalisation). Target: G rho r^2 = c^2.
Run: python3 p51_holographic_equipartition.py  |  MUTATE=1: drop hbar from T only (hbar must then NOT cancel: check H fails)
"""
import os, sys
import sympy as sp
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
r, rho, G, c, hb, k = sp.symbols("r rho G c hbar k", positive=True)
lP2 = hb * G / c**3; a0 = c**2 / (2 * r)
T = (1 if MUTATE else hb) * a0 / (2 * sp.pi * c * k)
V = 4 * sp.pi * r**3 / 3
cases = {"standard (Komar 2 rho, N_sur = A/l_P^2)": (4 * sp.pi * r**2 / lP2, 2 * (2 * rho * c**2 * V) / (k * T)),
         "variant: no Komar factor": (4 * sp.pi * r**2 / lP2, 2 * (rho * c**2 * V) / (k * T)),
         "variant: N_sur = A/(4 l_P^2)": (4 * sp.pi * r**2 / (4 * lP2), 2 * (2 * rho * c**2 * V) / (k * T))}
vals = {}
for nm, (Ns, Nb) in cases.items():
    sol = sp.solve(sp.Eq(Ns, Nb), rho)[0]
    kk = sp.simplify(G * sol * r**2 / c**2)
    vals[nm] = kk
    print(f"   {nm:42s}: G rho r^2 / c^2 = {kk}  (= {float(kk) if kk.is_number else kk}; target 1)")
check("H hbar cancels in the equipartition condition (a classical relation, as a0 requires)", all(not v.has(hb) for v in vals.values()))
check("T none of the equipartition variants gives G rho r*^2 = c^2: the standard case gives 3/(16 pi) = p17's C3 value", all(sp.simplify(v - 1) != 0 for v in vals.values())
      and sp.simplify(vals["standard (Komar 2 rho, N_sur = A/l_P^2)"] - sp.Rational(3, 16) / sp.pi) == 0)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
