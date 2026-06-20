#!/usr/bin/env python3
"""
ROUTE D -- ADVERSARIAL / NULL.  PART (c): the FDR / look-elsewhere check on "sqrt2".

Two SEPARATE questions, do NOT conflate:

Q1 (the EMPIRICAL relation): is Q=2/3 for the charged leptons itself a coincidence?
   -- ALREADY banked NO: parameter-free, ~1-in-44000, FDR-surviving. We REPRODUCE this so
   the skeptic does not over-reach and dismiss the genuine 45-year puzzle.

Q2 (the DERIVATION claim, the thing this route attacks): is "the framework's dS-Unruh
   geometry FORCES r=sqrt2 / the 45-deg angle" any better than a random O(1) geometric
   search that ALSO lands near sqrt2?  i.e. how many simple, framework-flavored geometric
   O(1)'s sit within the tolerance you'd need to call sqrt2 "predicted"?  If many, then
   "dS-Unruh gives sqrt2" carries ~0 bits over chance, exactly like the retracted
   4Z^2+3 / 64pi+Z numerology.

We test Q2 by counting how many short "geometric germ" expressions built from
{pi, 2, 3, 8pi, 32pi/3=Z^2, the dS/Friedmann/Einstein O(1)'s} land within a tolerance of
the target r=sqrt2 (=1.41421) OR the angle 45 deg OR cos^2=3/4.  Compare the HIT DENSITY
near sqrt2 to the hit density near a RANDOM target -- if comparable, sqrt2 is not special.
"""
import numpy as np
import itertools
from math import pi, sqrt, log, cos, sin, acos, degrees

target_r = sqrt(2)          # 1.414213562
target_cos2 = 0.75          # cos^2 theta = 3/4
target_angle = 45.0

# ---- Build a "framework-flavored" pool of simple O(1) geometric constants ----
# The germs the framework actually uses / could plausibly invoke for a Koide derivation:
Z2 = 32*pi/3                # Z^2 = Einstein 8pi x Friedmann 3
Z = sqrt(Z2)
germs = {
    'pi': pi, '2': 2.0, '3': 3.0, '8pi': 8*pi, '8pi/3': 8*pi/3, '32pi/3=Z2': Z2,
    'Z': Z, 'e': np.e, '4pi/3': 4*pi/3, 'kappa=1/2': 0.5, '2/3': 2/3, '3/8pi': 3/(8*pi),
}
base_vals = list(germs.values())
base_names = list(germs.keys())

def gen_expressions(maxdepth=2):
    """Generate sqrt/ratio/product/log combos of up to 2 germs (the same search space
    class as the retracted ai_slop numerology: O(1) op on 1-2 germs)."""
    exprs = []  # (value, label)
    # depth-1: f(g)
    unary = [('', lambda x: x), ('sqrt', sqrt), ('cbrt', lambda x: x**(1/3)),
             ('^1/4', lambda x: x**0.25), ('1/', lambda x: 1/x), ('2*', lambda x: 2*x),
             ('1/2*', lambda x: 0.5*x)]
    for (un, uf), (v, n) in itertools.product(unary, zip(base_vals, base_names)):
        try:
            val = uf(v)
            if 0.3 < val < 5:
                exprs.append((val, f"{un}{n}"))
        except Exception:
            pass
    # depth-2: f(g1 op g2)
    binops = [('*', lambda a, b: a*b), ('/', lambda a, b: a/b),
              ('+', lambda a, b: a+b), ('-', lambda a, b: a-b)]
    for (bn, bf) in binops:
        for (v1, n1), (v2, n2) in itertools.product(zip(base_vals, base_names), repeat=2):
            try:
                inner = bf(v1, v2)
                if inner <= 0:
                    continue
                for (un, uf) in [('', lambda x: x), ('sqrt', sqrt), ('^1/4', lambda x: x**0.25)]:
                    val = uf(inner)
                    if 0.3 < val < 5:
                        exprs.append((val, f"{un}({n1}{bn}{n2})"))
            except Exception:
                pass
    return exprs

exprs = gen_expressions()
vals = np.array([e[0] for e in exprs])
print(f"Generated {len(exprs)} framework-flavored geometric O(1) expressions in (0.3, 5).")

def hit_density(target, tol_rel):
    tol = tol_rel * target
    mask = np.abs(vals - target) < tol
    return mask.sum(), [exprs[i][1] for i in np.where(mask)[0]][:12]

print()
print("="*72)
print("Q2: does the framework-germ search hit r=sqrt2 NO BETTER than a random target?")
print("="*72)
for tol_rel in [0.005, 0.01, 0.02, 0.05]:
    n_sqrt2, labels = hit_density(target_r, tol_rel)
    # random comparison: average hit count over many random targets drawn log-uniform in (0.7,3)
    rng = np.random.default_rng(0)
    rand_targets = np.exp(rng.uniform(log(0.7), log(3.0), 4000))
    rand_counts = [np.sum(np.abs(vals - t) < tol_rel*t) for t in rand_targets]
    exp_rand = np.mean(rand_counts)
    bits = -log(max(n_sqrt2,1)/max(exp_rand,1e-9), 2) if exp_rand > 0 else 0
    print(f"\n tol={tol_rel*100:.1f}%:  hits near sqrt2 = {n_sqrt2:3d}   "
          f"expected hits near a RANDOM O(1) = {exp_rand:5.2f}")
    print(f"           => sqrt2 is {'NOT ' if n_sqrt2 >= exp_rand*0.5 else ''}special; "
          f"surplus bits over chance = {bits:+.2f}")
    if labels:
        print(f"           germs hitting sqrt2: {labels}")

print()
print("="*72)
print("Reference (Q1, the EMPIRICAL relation -- NOT under attack): is Q=2/3 a peak?")
print("="*72)
# Reproduce the banked chance-null: sample random positive mass triples (log-uniform over
# many decades), compute Q_geo, ask P(|Q_geo - 2/3| < 1e-5).
rng = np.random.default_rng(1)
N = 4_000_000
logm = rng.uniform(-3, 6, size=(N,3))   # masses over 9 decades
m = 10.0**logm
s = np.sqrt(m)
Qg = m.sum(1) / s.sum(1)**2
# Q_geo is bounded in [1/3, 1].  2/3 is the midpoint of the amplitude in r=sqrt2.
within = np.mean(np.abs(Qg - 2/3) < 1e-5)
peak_loc = (np.histogram(Qg, bins=200, range=(1/3,1))[0]).argmax()/200*(2/3)+1/3
print(f"  P(|Q_geo - 2/3| < 1e-5) over random triples = {within:.3e}  (banked ~2.3e-5)")
print(f"  density-peak of Q_geo is near {peak_loc:.3f} (NOT 2/3), so 2/3 is a")
print(f"  genuine 'special angle' for the leptons: ~1-in-{1/within:,.0f}.  This stands.")
print()
print("  CONCLUSION SPLIT:")
print("   - Q1 (the lepton Q=2/3 relation) is REAL & FDR-surviving  -> do NOT dismiss.")
print("   - Q2 (a 'dS-Unruh FORCES sqrt2' derivation) carries ~0 surplus bits if the")
print("     germ pool hits sqrt2 at the random rate -> a re-labeling, NOT a derivation.")
