"""AS2 diagnostic (NOT a gate, added after the gate run; see Amendment 2): is CPR's Table 1 n = 1 row consistent with CPR's own Table 2
n = 1 exponents and with CPR's closed form 'george' (which as2_gcpr.py reproduces exactly at R^0, R^1, R^2)?
Evaluates the n = 1 pure-gravity beta functions (my derivation == george / 725760) and the critical exponents at (a) the root found by
as2_gcpr.py and (b) CPR's printed Table 1 point (g~0, g~1) = (5.226e-3, -20.140e-3)."""
import sys
sys.dont_write_bytecode = True
import numpy as np
import sympy as sp
import as2_common as A
import as2_gcpr as G

HK = G.heat_kernels()
X = A.X_gravity(HK, with_eta=True, order_f=1)
bet = A.beta_system(X, 1)
f = sp.lambdify([A.g0, A.g1], bet)
J = sp.lambdify([A.g0, A.g1], sp.Matrix(bet).jacobian([A.g0, A.g1]))
roots, _, _ = A.find_roots(bet, 1, grid=True)
print("n = 1 pure gravity, CPR scheme: all real roots from the 10 x 15 grid:")
for r in roots:
    glb = A.to_glb(r)
    print(f"  g~ = ({r[0]:.7f}, {r[1]:.7f})  Lambda~ = {glb[1]:.6f}  G~ = {glb[0]:.6f}  theta = {np.round(-np.linalg.eigvals(np.array(J(*r), dtype=float)), 4)}")
pt = (5.226e-3, -20.140e-3)
print(f"\nCPR Table 1 n = 1 printed point g~ = {pt}: Lambda~ = {pt[0]/(-2*pt[1]):.5f}, G~ = {-1/(16*np.pi*pt[1]):.5f}")
print(f"  beta functions there: {np.array(f(*pt))}  (nonzero: not a fixed point of the flow that reproduces 'george')")
print(f"  critical exponents there: {np.round(-np.linalg.eigvals(np.array(J(*pt), dtype=float)), 4)}  vs CPR Table 2 n = 1: 2.382 +- 2.168 i")
alt = (5.226e-3, -20.214e-3)
print(f"\nhypothesis 'misprint -20.214 -> -20.140': at g~ = {alt}: betas {np.array(f(*alt))}; Lambda~ = {alt[0]/(-2*alt[1]):.5f}, G~ = {-1/(16*np.pi*alt[1]):.5f}")
