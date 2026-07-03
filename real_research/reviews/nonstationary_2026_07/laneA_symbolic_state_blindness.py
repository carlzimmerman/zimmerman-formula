#!/usr/bin/env python3
"""
laneA_symbolic_state_blindness.py
Lane A, part 1: FREE-FIELD STATE-BLINDNESS AT FINITE TIME (symbolic, exact).

Claim under test: for a worldline coordinate q LINEARLY coupled (q * c_k x_k) to a
bath of harmonic oscillators, the dissipation + mass-renormalization (response)
kernel is the field COMMUTATOR -- a c-number -- at ALL times t, for ANY bath state
(stationary or not, Gaussian or not). The state enters ONLY the noise kernel.

Method: exact Heisenberg-picture operator solution (no perturbation theory, no
stationarity, no Gaussian assumption anywhere in the response derivation).
sympy verifies every step. Exit 0 iff every assertion holds.
"""
import sympy as sp

t, s, u, w, hb = sp.symbols('t s u omega hbar', positive=True)
cc = sp.Symbol('c', positive=True)

# ------------------------------------------------------------------
# normal-ordering helper for noncommutative pairs with central commutator:
#   B*A -> A*B - kappa   (i.e. [A,B] = kappa, kappa central)
# ------------------------------------------------------------------
def normal_order(expr, A, B, kappa):
    expr = sp.expand(expr)
    if expr.is_Add:
        return sp.expand(sp.Add(*[normal_order(a, A, B, kappa) for a in expr.args]))
    c_part, nc_part = expr.args_cnc()
    coeff = sp.Mul(*c_part)
    for i in range(len(nc_part) - 1):
        if nc_part[i] == B and nc_part[i + 1] == A:
            swapped = nc_part[:i] + [A, B] + nc_part[i + 2:]
            reduced = nc_part[:i] + nc_part[i + 2:]
            return normal_order(coeff * (sp.Mul(*swapped) - kappa * sp.Mul(*reduced)),
                                A, B, kappa)
    return expr

# ==================================================================
# STEP 1: exact Heisenberg solution of one driven bath mode
#   x''(t) + w^2 x(t) = -c q(t),  q(t) an ARBITRARY operator-valued source
#   candidate: x(t) = x0 cos(wt) + p0 sin(wt)/w - c Int_0^t sin(w(t-u))/w q(u) du
# ==================================================================
x0, p0 = sp.symbols('x0 p0', commutative=False)
def xfree(tt):
    return x0 * sp.cos(w * tt) + p0 * sp.sin(w * tt) / w

# homogeneous part solves the free EOM identically
assert sp.expand(sp.diff(xfree(t), t, 2) + w**2 * xfree(t)) == 0

# inhomogeneous (memory) part: commutative check suffices (q(u) arbitrary)
q = sp.Function('q')
Ipart = -cc * sp.Integral(sp.sin(w * (t - u)) / w * q(u), (u, 0, t))
resid = sp.simplify(sp.diff(Ipart, t, 2) + w**2 * Ipart + cc * q(t))
assert resid == 0, f"EOM residual nonzero: {resid}"
print("STEP 1  PASS: exact Heisenberg solution verified for ARBITRARY source q(t):")
print("        x(t) = x_free(t) - c Int_0^t [sin(w(t-u))/w] q(u) du   (valid at ALL t)")

# ==================================================================
# STEP 2: the memory kernel IS the free-field commutator (a c-number)
#   [x_free(t), x_free(s)] = i hbar sin(w(s-t))/w  -- no state anywhere
# ==================================================================
comm = normal_order(xfree(t) * xfree(s) - xfree(s) * xfree(t), x0, p0, sp.I * hb)
comm = sp.simplify(comm)
target = sp.I * hb * sp.sin(w * (s - t)) / w
assert sp.simplify(comm - target) == 0, f"commutator mismatch: {comm}"
assert not (comm.has(x0) or comm.has(p0)), "commutator is not a c-number!"
print("STEP 2  PASS: [x_free(t), x_free(s)] = i*hbar*sin(w(s-t))/w  -- a C-NUMBER.")
print("        Back-reaction force on q:  F(t) = -c x(t) = xi(t) + Int_0^t chi(t-u) q(u) du")
print("        chi(t-u) = -c^2 sin(w(t-u))/w = (i/hbar)*c^2*[x_f(t),x_f(u)]  <- response kernel")
print("        xi(t)   = -c x_free(t)                                       <- noise operator")
print("        The response kernel contains NO state information AT ANY TIME t.")
print("        This is an exact OPERATOR identity: it holds for ANY bath state --")
print("        vacuum, thermal, squeezed, non-stationary, even NON-GAUSSIAN.")
print("        Multi-mode: chi(t,u) = -Sum_k c_k^2 sin(w_k(t-u))/w_k (linearity, mode by mode).")
print("        Time-dependent couplings c_k(t): chi(t,u) = -Sum_k c_k(t)c_k(u) sin(w_k(t-u))/w_k")
print("        -- still a c-number. NON-STATIONARY DRIVING cannot make the kernel state-aware.")

# ==================================================================
# STEP 3: where the state DOES live -- the symmetric (noise) correlator.
# General zero-mean Gaussian state of one mode:
#   A = <x0^2>, B = <p0^2>, C = <{x0,p0}>/2   (time-dep. squeezing = generic A,B,C)
# ==================================================================
A, B, C = sp.symbols('A B C', real=True)
S = (A * sp.cos(w * t) * sp.cos(w * s)
     + B * sp.sin(w * t) * sp.sin(w * s) / w**2
     + C * (sp.cos(w * t) * sp.sin(w * s) + sp.sin(w * t) * sp.cos(w * s)) / w)

T, tau = sp.symbols('T tau', real=True)
S_T = sp.expand_trig(S.subs([(t, T + tau / 2), (s, T - tau / 2)]))
dSdT = sp.simplify(sp.diff(S_T, T))

# stationary iff  B = A w^2  and C = 0 (thermal/vacuum-like); generic squeezed: depends on T
assert sp.simplify(dSdT.subs([(B, A * w**2), (C, 0)])) == 0
gen = dSdT.subs([(A, 2), (B, w**2), (C, 0), (tau, 0), (T, sp.pi / (4 * w))])
assert sp.simplify(gen) != 0
print("STEP 3  PASS: symmetric (noise) kernel S(t,s) DOES depend on the state (A,B,C)")
print("        and on T=(t+s)/2 for squeezed/non-stationary states (dS/dT != 0 generically;")
print("        dS/dT == 0 exactly when B=A*w^2, C=0, i.e. vacuum/thermal).")
print("        => Non-stationarity of the STATE shows up ONLY in the NOISE, never the response.")

# ==================================================================
# STEP 4: assemble the theorem statement
# ==================================================================
print()
print("THEOREM (finite-time state-blindness, linear coupling, free bath):")
print("  For H = H_S(q,p) + Sum_k [p_k^2/2 + w_k^2 x_k^2/2] + q Sum_k c_k(t) x_k,")
print("  the exact Heisenberg equations give, at EVERY finite time t,")
print("     q-EOM:  m q'' = -dV/dq + Int_0^t chi(t,u) q(u) du + xi(t)")
print("  with chi a c-number (the commutator). Any induced mass shift delta-m(t),")
print("  transient or asymptotic, is a functional of chi ALONE -> IDENTICAL for the")
print("  dS vacuum, thermal, squeezed, oscillating-squeezed, coherent, or any other state.")
print("  The MOND-sign question for free fields therefore reduces to the c-number kernel,")
print("  which is fixed by the spectral density -- theorems III/IV territory (delta-m >= 0")
print("  without a sub-drive pole). STATE ENGINEERING of free-field inertia: IMPOSSIBLE at all t.")
print()
print("laneA_symbolic_state_blindness: ALL ASSERTIONS PASS")
