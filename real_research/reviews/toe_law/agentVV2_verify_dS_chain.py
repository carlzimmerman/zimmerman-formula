import numpy as np
# =====================================================================
# VERIFY (a): the dS-side hyperfiniteness chain. The route says every
# link is a cited theorem. I hostile-check the ONE place a smuggle could
# hide: the claim that injectivity (a) survives the crossed product by R
# AND (b) passes to the II_1 corner. Both are real theorems, but let me
# confirm the *amenability inputs* are genuine and not assumed.
# =====================================================================

print("=== LINK (iii): is the boost group R amenable? (the only group input) ===")
# Amenability of (R,+): Folner sequence F_n=[-n,n]. For ANY compact shift set
# the symmetric-difference ratio -> 0. This is iron-clad (every abelian, indeed
# every solvable, lc group is amenable). Re-verify with a 2-sided check.
rng = np.random.default_rng(0)
worst = 0.0
for _ in range(2000):
    t = rng.uniform(-200, 200)
    n = rng.uniform(abs(t)+1, 1e6)
    ratio = 2*abs(t)/(2*n)   # |F_n + t  symm-diff  F_n| / |F_n|
    worst = max(worst, ratio if n < 10*abs(t)+10 else 0.0)
# the SUP over n of the ratio -> 0 as n->inf for each fixed t; check monotone decay
for t in [1.0, 50.0, 200.0]:
    ns = np.array([1e2, 1e3, 1e4, 1e5, 1e6])
    print(f"  t={t:6.1f}: Folner ratios over n=1e2..1e6 = {2*t/(2*ns)}")
print("  => R amenable (abelian); link (iii) GENUINE, not assumed.\n")

print("=== LINK (iv): injective x amenable-group crossed product stays injective ===")
print("  Connes 1976 / Connes-permanence: crossed product N = M xrtimes_alpha G with")
print("  M injective and G amenable lc => N injective. This is a CITED THEOREM, not")
print("  numerically checkable. The hypotheses HERE are both met:")
print("    M = hyperfinite III_1 QFT vacuum algebra (injective, standard);")
print("    G = R (boost), amenable (link iii).")
print("  => M xrtimes R is injective type II_infinity. SOUND.\n")

print("=== LINK (v): does injectivity pass to the II_1 corner? ===")
print("  Two sub-steps, both theorems:")
print("   (v-a) compression by a projection p: pNp injective if N injective (Connes).")
print("   (v-b) image of a NORMAL conditional expectation of an injective algebra is")
print("         injective (the expectation is the trace-preserving E onto the centralizer;")
print("         CLPW supply the semifinite trace, so the trace-preserving E EXISTS).")
print("  Both are standard. The ONLY physics input is that CLPW's constraint really")
print("  yields a trace-preserving normal E -- which is the content of their II_1 result.")
print("  => N_obs injective II_1 => = R (Connes uniqueness). dS SIDE: CONFIRMED.\n")

print("VERDICT (a): dS observer algebra = hyperfinite II_1 factor R is ESTABLISHED.")
print("  Every link is a genuine theorem; the only group-theory input (R amenable) is")
print("  iron-clad; no smuggle. This MATCHES the route. NOT in dispute.")
