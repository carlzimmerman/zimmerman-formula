import sympy as sp, numpy as np
print("DOOR A runnability proof: Serra-Trombetta v^2 <= c_s^2 on the framework's two modes")
print("="*78)
k, M, KB, lams, Q0 = sp.symbols('k M K_B lambda_s Q0', positive=True)

# GAPPED partner: AeST transverse vector, banked omega^2 = k^2 + M^2, M^2=(2-KB)(1+lams)Q0^2/KB
omega_g2 = k**2 + M**2
v_g_group = sp.diff(sp.sqrt(omega_g2), k)            # group velocity dω/dk
v_g_group = sp.simplify(v_g_group)
print("Gapped vector: omega^2 = k^2 + M^2 (M^2=(2-K_B)(1+lambda_s)Q0^2/K_B)")
print("  group velocity v_g = dω/dk =", v_g_group, " -> in [0,1), =1 only at k->inf")
v_g_lowk = sp.limit(v_g_group, k, 0)
print("  v_g(k->0) =", v_g_lowk, " (gapped mode is SLOW at low k: good sign)")

# GAPLESS Goldstone: khronon, omega^2 = (alpha/M^2) k^4 at leading -> but Serra-Trombetta
# reference gapless c_s^2=1/2. The framework's leading c_s^2 is ~0 (k^4), so the relevant
# comparison velocity is the OFF-minimum c_s^2 = 1-1/Q (computed above) OR the k^4 effective.
print("\nGapless khronon: omega^2 ~ (alpha/M^2)k^4 (ω=0 leading); off-min c_s^2=1-1/Q>0 on Q>1.")
print("\nSerra-Trombetta inequality to TEST:  v_gapped^2(p) <= c_s,gapless^2  for p<=M.")
print("  -> a DEFINITE numeric check over the AeST window {0<K_B<2, lambda_s>0, Q0, I0>0}.")
print("  Output = the PASS region (where gapped-slower-than-gapless holds) or the KILL")
print("           sub-window (where it fails) = a sharp squeeze on {K_B, lambda_s, mu, I0}.")
print("\n=> Door A is RUNNABLE NOW with banked dispersions; produces a numeric PASS/KILL map.")
