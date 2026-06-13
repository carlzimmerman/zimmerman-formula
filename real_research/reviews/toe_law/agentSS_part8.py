"""
agentSS Part 8 — does the ratio EVER land on the edge surface, and the k-resolution question.

(1) The edge equation is G = 4 j3/j2^2 (agentRR). For the QNM line, G is the gain AMPLITUDE (a SEPARATE
    knob from the shape) and 4 j3/j2^2 = 8 Delta (the shape ratio). So the edge eq becomes
        G = 8 Delta.
    This is ONE equation relating TWO free quantities (gain amplitude G, probe dimension Delta).
    => a codim-1 surface in (G, Delta): for ANY Delta there is a G that satisfies it (G=8Delta), and
       vice versa. It is SATISFIABLE but only on a tuned line -> PERMITS. Confirms agentRR's codim-1.

    Moreover saturation (agentRR Route 1) pins G to gain=loss (G_sat^stab = kappa-related), an
    INDEPENDENT condition. Forcing needs G_sat^stab = 8 Delta identically -> two unrelated quantities
    (loss kappa-set vs probe-dimension-set) -> generically unequal -> agentRR's "roam 10-266x".

(2) THE k-RESOLUTION / CLAMP (brief's 2nd load-bearing requirement + agentRR's 4th condition): does the
    dS structure supply an INTRINSIC k-dependence that keeps the off-center fold-band poles in the LHP
    (which scalar saturation cannot)? The QNM ladder Gamma_n = sinh((Delta+n)lambda) is indexed by the
    DESCENDANT number n, NOT by spatial momentum k. The static-patch SL(2,R) acts on the (time/energy)
    spectral data; it carries NO spatial-k label (the sphere SO(3) carries angular l, but l is the
    multipole on the horizon sphere, not the khronon's spatial wavenumber k in the dispersion
    omega^2(k)). So the modular/SL(2,R) structure does NOT k-resolve the clamp: the symmetry is in the
    frequency/descendant sector, decoupled from the k that the fold lives in.
"""
import sympy as sp
import mpmath as mp
mp.mp.dps=30

print("=== (1) Edge eq for the QNM line: G = 8 Delta (codim-1, satisfiable but tuned) ===")
# Is there a Delta where 8Delta sits in a 'natural' fold-window? G_sat just needs to equal the shape
# ratio; the fold WINDOW constraint is sigma6/sigma6* in (1,4/3) which is about the gain SHAPE producing
# a bounded (not ghost, not monotone) fold -- a SEPARATE narrow window. Check the QNM line's own
# sigma6/sigma6* if we feed (j2,j3)=(j2, j3) and G into agentRR's geometry.
# sigma4=-G j2 c^2, sigma6=+G j3 c^2, sigma6*=sigma4^2/(4c^2)=G^2 j2^2 c^2/4.
# sigma6/sigma6* = (G j3 c^2)/(G^2 j2^2 c^2/4) = 4 j3/(G j2^2) = (4 j3/j2^2)/G = 8Delta/G.
# Fold window: 1 < 8Delta/G < 4/3  => 6 Delta < G < 8 Delta.
print("  sigma6/sigma6* = 8 Delta / G.  Fold (bounded, no-ghost) window 1<...<4/3  =>  6 Delta < G < 8 Delta.")
print("  => a NONEMPTY but NARROW G-band (width 2 Delta, i.e. 25% of G) for each Delta. SATISFIABLE,")
print("     but G must be hand-placed in (6Delta,8Delta) AND equal the saturation value AND the edge")
print("     value simultaneously -> still tuned, multiple independent conditions on one knob.")
print()
# numeric demo for a couple Delta
for Dv in [0.5,1.0,2.0]:
    print(f"   Delta={Dv}: fold-window G in ({6*Dv:.2f}, {8*Dv:.2f}); edge-exact G=8Delta={8*Dv:.2f} sits at the")
    print(f"            sigma6/sigma6*=1 EDGE (the soft sonic-edge limit), boundary of the window.")
print()
print("=== (2) k-resolution: the symmetry sector carries NO spatial k ===")
print("  Gamma_n = sinh((Delta+n)lambda) indexed by descendant n; SL(2,R) acts on time/energy data;")
print("  SO(3) carries horizon-sphere multipole l, NOT the khronon spatial wavenumber k of omega^2(k).")
print("  => the dS isometry/modular structure does NOT supply the k-resolved (non-Markovian) clamp that")
print("     agentRR's 4th condition needs. The clamp k-structure is decoupled from the static-patch")
print("     symmetry. => the symmetry route does NOT deliver the k-resolved clamp either.")
