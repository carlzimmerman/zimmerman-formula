"""p60: systematic principle search with a look-elsewhere base rate.  Units c = G = rho_Lambda = 1, so the target is a0 = 1/2 (a0 = (1/2) c sqrt(G rho_Lambda)).
Grammar (every item is a standard physical quantity; nothing is fitted):
  radii R: r1 = 1/sqrt(G rho) (pi-free vacuum length), rH = sqrt(3/(8 pi G rho)) (de Sitter horizon), rL = 1/sqrt(Lambda) = 1/sqrt(8 pi G rho)
  masses at R: ball (4pi/3)rho R^3, active vacuum 2x ball (rho + 3p), cube rho R^3, half-S^3 proper volume pi^2 rho R^3, BH mass R/2 (r_s = R)
  accelerations at R: G M/R^2 for each mass; c^2/R; c^2/(2R) (Newtonian BH surface gravity); de Sitter repulsion (Lambda/3) c^2 R
  principle forms: a0 = A ; a0 = A^2/B (deep-MOND matching g = sqrt(a0 g_N)) ; a0 = sqrt(A B)
Report: every distinct form giving EXACTLY 1/2, the number of distinct rational outputs, and how often 1/2 occurs vs other simple rationals (base rate).
A hit is a CANDIDATE principle only: it must then be checked physically (lensing / Cassini / derivability). Nothing here derives kappa.
Run: python3 p60_principle_grammar_search.py | MUTATE=1 sets the target to 1/3 (the hit list must change -> check H fails)
"""
import os, sys, itertools
import sympy as sp
from collections import Counter
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
pi = sp.pi
target = sp.Rational(1, 3) if MUTATE else sp.Rational(1, 2)
R = {"r1": sp.Integer(1), "rH": sp.sqrt(3 / (8 * pi)), "rL": 1 / sp.sqrt(8 * pi)}
Lam = 8 * pi
A = {}
for rn, r in R.items():
    masses = {"ball": sp.Rational(4, 3) * pi * r**3, "active": sp.Rational(8, 3) * pi * r**3, "cube": r**3, "S3half": pi**2 * r**3, "BH": r / 2}
    for mn, m in masses.items(): A[f"GM_{mn}/R^2@{rn}"] = sp.simplify(m / r**2)
    A[f"c^2/R@{rn}"] = 1 / r; A[f"c^2/2R@{rn}"] = 1 / (2 * r); A[f"dS(Lambda R/3)@{rn}"] = sp.simplify(Lam * r / 3)
names = list(A)
forms = {}
for n in names: forms[f"a0 = {n}"] = A[n]
for n1, n2 in itertools.product(names, names):
    if n1 != n2:
        forms[f"a0 = ({n1})^2/({n2})"] = sp.simplify(A[n1]**2 / A[n2])
for n1, n2 in itertools.combinations(names, 2):
    forms[f"a0 = sqrt({n1} * {n2})"] = sp.simplify(sp.sqrt(A[n1] * A[n2]))
vals = {k: sp.nsimplify(sp.simplify(v)) for k, v in forms.items()}
rat = {k: v for k, v in vals.items() if v.is_rational}
hits = [k for k, v in rat.items() if sp.simplify(v - target) == 0]
print(f"   grammar: {len(names)} accelerations, {len(forms)} principle forms, {len(rat)} give a RATIONAL a0 (pi-free), {len(set(rat.values()))} distinct rationals")
cnt = Counter(rat.values())
print("   most common rational outputs: " + ", ".join(f"{v}: {c}" for v, c in cnt.most_common(10)))
print(f"   forms giving exactly {target}: {len(hits)}")
for h in hits: print("     " + h)
simple = [sp.Rational(p, q) for p in range(1, 5) for q in range(1, 5)]
share = cnt[target] / max(1, sum(cnt[s] for s in set(simple)))
print(f"   base rate: {target} takes {cnt[target]} of the {sum(cnt[s] for s in set(simple))} hits on simple rationals p/q (p,q <= 4) = {share:.2f}")
check("H the hit list is non-empty and every hit evaluates to the target", len(hits) > 0 and all(sp.simplify(vals[h] - sp.Rational(1, 2)) == 0 for h in hits))
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
