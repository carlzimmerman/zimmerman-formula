# POST HOC (after the frozen main and MUTATE runs; not gated). Reuses cfg94's functions.
import os, sys, math, io, contextlib
import numpy as np
buf = io.StringIO()
import types
ns = {"__name__": "cfg94x", "__file__": os.path.abspath("cfg94.py")}
with contextlib.redirect_stdout(buf):
    try:
        exec(compile(open("cfg94.py").read(), "cfg94.py", "exec"), ns)
    except SystemExit:
        pass
c = types.SimpleNamespace(**ns)
out = open("posthoc.out", "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s); out.write(s + "\n")
# (1) identity: E ratio = 2 (a/g_law) sqrt(1+x_e^2)/x_e  (pressure reading, lambda = 3/2)
P("(1) E_c/(1/2 M V_f^2) vs 2 (a_P/g_law(x_e)) sqrt(1+x_e^2)/x_e, and the large-x_e form 2 a/g_law:")
for M in (1e9, 1e10, 1e12):
    xe = c.edge_x(M, "A", "own", "canonical", 0.4)
    a = c.react_closed("P", xe, 1.5)
    P(f"   M={M:.0e}: x_e={xe:.3f}  E ratio = 1.5 x_e = {1.5*xe:.4f};  2 (a/g) sqrt(1+x^2)/x = {2*a*math.sqrt(1+xe**2)/xe:.4f};  2 a/g_law(x_e) = {2*a:.4f}")
# (2) g_law with nu_mono instead of P2 (reaction numerators unchanged: 3/4 a0, sigma formula), ratio over the grid
P("(2) reaction/g_law when g_law is the nu_mono law g_N nu_mono(y) (numerators from the P2 derivation kept; the nu_mono target changes them by O(charge function 1.46 at x=1) -> only the ratio of the two g_law is shown):")
for x in (0.3, 1, 3, 10, 30):
    y = 1 / x**2
    r = float(c.nu_mono(y)) / float(c.nu_p2(y))
    P(f"   x={x:5g}: nu_mono(y)/P2(y) = {r:.4f}  -> a_P/g_mono = {c.react_closed('P', x, 1.5)/r:.4f} (P2: {c.react_closed('P', x, 1.5):.4f})")
# (3) best of the sweep restricted to lambda = 3/2 and the three declared masses
import itertools
best = None
for M, conv, dn, a0n, frac, rd, ref, rng, vm in itertools.product((1e9, 1e10, 1e12), c.convs, c.DTA.keys(), ("canonical", "alt"), (0.31, 0.40, 0.48), ("P", "S"), ("gLaw", "gN"), ("full", "edge"), (1.0, math.sqrt(2), 2.0)):
    xe = c.edge_x(M, conv, dn, a0n, frac)
    R = c.react_max(rd, 1.5, ref, 30.0 if rng == "full" else min(30.0, xe)); E = 1.5 * xe / vm
    s = max(R / 0.1, E)
    if best is None or s < best[0]:
        best = (s, M, conv, dn, a0n, frac, rd, ref, rng, vm, R, E)
P(f"(3) lambda = 3/2, M in {{1e9,1e10,1e12}}: smallest max(R/0.10, E) = {best[0]:.3f}: {best[1:10]}, R = {best[10]:.3f} g, E = {best[11]:.3f}")
best = None
for M, conv, dn, a0n, frac, rd, ref, rng, vm in itertools.product((1e9, 1e10, 1e12), c.convs, c.DTA.keys(), ("canonical", "alt"), (0.31, 0.40, 0.48), ("P", "S"), ("gLaw",), ("full",), (1.0,)):
    xe = c.edge_x(M, conv, dn, a0n, frac)
    R = c.react_max(rd, 1.5, ref, 30.0); E = 1.5 * xe / vm
    s = max(R / 0.1, E)
    if best is None or s < best[0]:
        best = (s, M, conv, dn, a0n, frac, rd, R, E)
P(f"(3b) same, headline definitions only (g_law reference, full x range, V_f^2 = sqrt(GMa0)): smallest = {best[0]:.1f}: {best[1:7]}, R = {best[7]:.2f} g (=E/R structure), E = {best[8]:.2f}")
# (4) does restricting the reaction to x <= x_e help (edge mode) at the declared masses?  x_e >= 10 there, so the max reaction is at the edge
for M in (1e9, 1e10, 1e12):
    xe = c.edge_x(M, "A", "own", "canonical", 0.4)
    P(f"(4) M={M:.0e}: reaction at x_e = {xe:.2f}: P {c.react_closed('P', xe, 1.5):.2f}, sigma {c.react_closed('S', xe, 1.5):.2f} g_law (edge-restricted range still fails)")
