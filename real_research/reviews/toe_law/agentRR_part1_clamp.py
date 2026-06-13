"""
agentRR Part 1 — D1: does SATURATION tame the LTI runaway QQ found?

QQ's finding (BOUNDS-BUT-UNSTABLE): a negative-residue (active) LTI Lorentzian gain band on
D(omega,k) = omega^2 - c^2 k^2 - Sigma(omega) opens a UHP pole of the retarded Green function once
the gain g exceeds e_inst ~ O(gamma) ~ 0.015. The intensity grows exponentially e^{+Im(omega) t}.

The laser-physics claim: with a SATURATED gain g_eff = g0/(1 + I/I_sat), the growing mode does NOT
run away. Instead the intensity I climbs until the SATURATED gain g_eff has dropped to exactly the
loss -- the gain CLAMPS. At that operating point Im(omega)=0 (marginal), the pole sits ON the real
axis (steady-state limit cycle), and the LTI runaway is self-limited. This is the standard
above-threshold laser steady state. We verify it as a dynamical system (no quarantined coefficients,
only signs and fixed-point structure).

Model the slowly-varying intensity I(t) = |chi|^2 of the unstable band with the standard laser rate
equation derived from D: the linear growth rate is 2*Im(omega_pole)(g_eff); near threshold
Im(omega_pole) ~ (1/2)(g_eff - loss)/normalization. So

    dI/dt = [ g0/(1 + I/I_sat) - kappa ] * I

with kappa the cold-cavity loss (here the khronon's intrinsic damping), g0 the small-signal
(unsaturated) gain. We show: (i) for g0 > kappa the I=0 fixed point is UNSTABLE (the LTI runaway),
but (ii) a NEW stable fixed point I* = I_sat*(g0/kappa - 1) > 0 appears, and the gain there is
CLAMPED: g_eff(I*) = kappa exactly. The runaway is tamed -- I saturates, it does not blow up.
"""
import sympy as sp

I, Isat, g0, kappa, t = sp.symbols('I I_sat g0 kappa t', positive=True, real=True)

# saturated gain
g_eff = g0/(1 + I/Isat)

# rate equation RHS
f = (g_eff - kappa)*I
print("rate eq  dI/dt = f(I) =", sp.simplify(f))

# fixed points
fps = sp.solve(sp.Eq(f, 0), I)
print("fixed points I* :", fps)

# the nonzero fixed point
Istar = Isat*(g0/kappa - 1)
print("claimed nonzero FP  I* = I_sat*(g0/kappa - 1) =", Istar)
print("check f(I*) = 0 :", sp.simplify(f.subs(I, Istar)))

# gain at the operating point -- the CLAMP
g_at_star = sp.simplify(g_eff.subs(I, Istar))
print("CLAMP: g_eff(I*) =", g_at_star, " (should equal kappa = the loss)")

# stability of each fixed point: sign of f'(I)
fp_prime = sp.diff(f, I)
print("\nf'(I) =", sp.simplify(fp_prime))
print("f'(0)   =", sp.simplify(fp_prime.subs(I, 0)), "  -> sign tells I=0 stability")
print("        for g0>kappa this is POSITIVE => I=0 UNSTABLE (the LTI runaway seed)")
fp_prime_star = sp.simplify(fp_prime.subs(I, Istar))
print("f'(I*)  =", sp.simplify(fp_prime_star), "  -> sign tells I* stability")

# evaluate f'(I*) for g0>kappa numerically to confirm it's negative (stable)
import mpmath as mp
for (g0v, kv, isv) in [(0.05,0.015,1.0),(0.10,0.015,1.0),(1.0,0.015,1.0),(0.030,0.015,2.0)]:
    val = float(fp_prime_star.subs({g0:g0v, kappa:kv, Isat:isv}))
    istar_v = float(Istar.subs({g0:g0v, kappa:kv, Isat:isv}))
    print(f"  g0={g0v}, kappa={kv}, Isat={isv}: I*={istar_v:.4f}, f'(I*)={val:.5f}  (<0 => STABLE clamp)")

print("\n==> D1 VERDICT: above threshold (g0>kappa) the I=0 LTI runaway is unstable, but the")
print("    NONZERO operating point I* is STABLE and the gain there is CLAMPED to the loss kappa.")
print("    Saturation converts QQ's exponential runaway into a self-limited steady state. PASS (D1).")
