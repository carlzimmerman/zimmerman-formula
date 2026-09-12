#!/usr/bin/env python3
"""L193 -- WHAT THE CRITICAL SURFACE IS: an exact stress-tensor degeneracy, not just a vanishing sound speed.

L192 found that the clock-scalar sound speed rises with the background gradient invariant Y and crosses zero where
    N = 2 P_X (1 - D) - 2 s0 W_Y = 0,   D = 2 Q^2 W_Y / W.
While that was being written astra began an independent audit of the same action from all ten inverse-metric variations
(qwen_claude_field_theory/closure_2026/clock_response_repair_2026/l192_stress_audit_2026, read-only, not run here) and its
symbolic step records the identity det(T^mixed_tx - L I) = -s0 b^2 W N. This script verifies that INDEPENDENTLY, with its own
implementation, because it changes what the critical surface means.

Two verifications, both symbolic (sympy, exact):
  A. Vary the frozen action density with respect to the inverse metric in the same 4x4 setting and confirm the stress tensor is
     T_00 = 2 P_X Q^2 - P + V, T_11 = L + 2(P_X - s0 W_Y) b^2, T_22 = T_33 = L, T_01 = 2 P_X Q b, with L = P - V + s0 W and
     b = |grad_perp chi| = sqrt(Y). This is the content the interpretation rests on and it is checked, not assumed.
  B. Form the MIXED tensor T^mu_nu and show det(T_tx - L I) = -s0 b^2 W N exactly, so that N = 0 is precisely the condition for a
     THIRD eigenvalue to equal L (the transverse pair already do). At N = 0 the sector's stress is isotropic -- perfect-fluid form --
     at the same point where its perturbations stop propagating. Isotropic stress plus zero sound speed is exactly what a clustering
     cold component is, and both arrive together on one surface fixed by the action.
No literal-True checks; no numerics enter (this is an off-shell algebraic identity)."""
import sympy as sy
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("=" * 118 + "\nL193 THE CRITICAL SURFACE IS A STRESS DEGENERACY (independent verification)\n" + "=" * 118)
e = sy.symbols("epsilon", real=True); Q, b = sy.symbols("Q b", real=True); s0 = sy.symbols("s0", positive=True)
P, PX, V, W, WY = sy.symbols("P P_X V W W_Y", real=True)
eta = sy.diag(-1, 1, 1, 1); tau = sy.Matrix([s0, 0, 0, 0]); chi = sy.Matrix([Q, b, 0, 0])
L = P - V + s0*W
# ---- A. the stress tensor from all ten inverse-metric variations ----
calc = sy.zeros(4)
for i in range(4):
    for j in range(i, 4):
        dirn = sy.zeros(4); dirn[i, j] = 1; dirn[j, i] = 1
        inv = eta + e*dirn
        s = sy.sqrt(-(tau.T*inv*tau)[0]); X = -(chi.T*inv*chi)[0]; cross = (tau.T*inv*chi)[0]
        Yv = -X + cross**2/s**2
        lag = P + PX*(X - (Q**2 - b**2)) - V + s*(W + WY*(Yv - b**2))      # first jets fix a first metric variation exactly
        dens = lag/sy.sqrt(-inv.det()); mult = 1 if i == j else 2
        calc[i, j] = calc[j, i] = sy.simplify(-sy.Rational(2, mult)*sy.diff(dens, e).subs(e, 0))
expected = sy.diag(2*PX*Q**2 - P + V, L + 2*(PX - s0*WY)*b**2, L, L)
expected[0, 1] = expected[1, 0] = 2*PX*Q*b
resid = sy.simplify(calc - expected)
check("V1 [stress tensor, independently derived] all ten inverse-metric variations of the frozen action reproduce the stress tensor whose transverse block is L and whose x-x entry carries the combination (P_X - s0 W_Y)",
      resid == sy.zeros(4), f"residual matrix is exactly zero; T_00 = {sy.simplify(calc[0,0])}, T_11 - L = {sy.simplify(calc[1,1] - L)}, T_01 = {sy.simplify(calc[0,1])}")
check("V2 [the transverse pair] two eigenvalues of the mixed stress are already equal to L = P - V + s0 W, independently of the gradient: the y and z directions are degenerate for any background",
      sy.simplify((eta*calc)[2, 2] - L) == 0 and sy.simplify((eta*calc)[3, 3] - L) == 0 and all(sy.simplify((eta*calc)[i, j]) == 0 for i in (2, 3) for j in range(4) if j != i),
      "rows 2 and 3 of the mixed tensor are exactly L on the diagonal and zero off it")
# ---- B. the degeneracy identity ----
mixed = eta*calc
N = 2*PX*(1 - 2*Q**2*WY/W) - 2*s0*WY
det_tx = sy.factor(sy.simplify((mixed[:2, :2] - L*sy.eye(2)).det()))
ident = sy.simplify(det_tx + s0*b**2*W*N)
print(f"    det(T^mixed_tx - L I) = {det_tx}")
print(f"    - s0 b^2 W N          = {sy.simplify(-s0*b**2*W*N)}")
check("V3 [THE IDENTITY, verified independently] det(T^mixed_tx - L I) = - s0 b^2 W N exactly, with N the very combination whose vanishing L192 identified as the critical gradient: the sound-speed numerator IS the determinant of the time-space block of the stress tensor shifted by L",
      ident == 0, "difference simplifies to exactly zero")
check("V4 [what the critical surface therefore is] on N = 0 a THIRD eigenvalue of the mixed stress equals L, so the stress tensor takes perfect-fluid form: the sector's anisotropic stress vanishes at the same surface on which its perturbations stop propagating",
      sy.simplify(det_tx.subs(WY, sy.solve(sy.Eq(N, 0), WY)[0])) == 0,
      f"solving N = 0 gives W_Y = {sy.simplify(sy.solve(sy.Eq(N, 0), WY)[0])}, and substituting it makes the shifted determinant vanish identically, so L is a repeated eigenvalue on that surface")
check("V5 [and it is not trivial] away from that surface the time-space block is NOT degenerate: the shifted determinant is proportional to b^2, so a background WITHOUT a gradient (b = 0) is degenerate for a different reason and carries no information -- the degeneracy that matters is the one reached at finite gradient",
      sy.simplify(det_tx.subs(b, 0)) == 0 and sy.simplify(sy.diff(det_tx, b, 2)) != 0,
      "det vanishes at b = 0 for every N, and its second derivative in b is non-zero, so finite gradient is what makes N = 0 the non-trivial condition")
print("    READING: L192 gave the critical gradient a dynamical meaning (zero sound speed, two-sided attractor). This identity gives it an\n"
      "    algebraic one, off shell and independent of any background history: the same surface is where the sector's stress becomes isotropic.\n"
      "    Isotropic stress with non-propagating perturbations is precisely a clustering cold component.\n"
      "    LIMITS: the first-jet form of the density used for the variation (exact for a first metric variation, as in the audit); a single spatial\n"
      "    direction carries the gradient; no claim about the background history, the amount of the sector, or any gate.")
print(f"\nL193 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
