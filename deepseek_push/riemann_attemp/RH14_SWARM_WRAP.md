# RH14 -- THE RAR/ZERO-FREE/DUALITY SWARM: integrated verdict (deepseek, 2026-09-17)

**BOTTOM LINE: RH still not proven, and the swarm now shows WHY the framework cannot
reach it through four more independent doors -- but it produced two NEW Lean-certified
structural facts (the 3-4-1 admissibility with equality ONLY at the classical point;
the doubled-completion no-go with a certified counterexample) and one new exact identity
for the prime gas (M(sigma) = ln zeta(sigma) - ln zeta(2sigma)).**

## THE FOUR LANES (verdicts as landed, artifacts verified on disk)

**RH10 -- the RAR of the zeros (the framework's signature law, first test):**
INCONCLUSIVE by pre-registered power gate: gamma = +0.48 with bootstrap 95% CI
half-width 2.09 (> 0.30 limit), so neither the RAR-holds branch (gamma in [0.85,1.15])
nor the does-not-transfer branch (gamma ~ 0) could fire at the ~500-zero budget.
A = 3.76e-2, q-statistics match the GUE number-variance null (z <= 0.5).  The lane
registered the need for a ~5000-zero budget (the 30k cache, when it lands, is the
execution point) and refuses to over-read.  Honest: the RAR test on the zeros is
POWER-BOUNDED, not decided.

**RH11 -- the zero-free-region route (framework kernel in the 3-4-1 trick):**
FAILS AS A FRAMEWORK IMPROVEMENT -- with a certified reason.  The 3-4-1 scheme
ACCEPTS the framework's Lomax kernels: 61678/63060 (l,u,w) combinations pass with
k(theta) >= 0 for all theta AND positive leading Fourier coefficient (K1 unfired).
BUT every framework kernel is strictly WEAKER than the classical weights:
alpha = (A+C)/B >= 1 certified in Lean with equality ONLY at the classical point
(u -> 0, f = 1), giving c_best = 0.09548 < c_class = 1/9.646 = 0.10367
(ratio 0.921 -- weaker-than-known, registered as such; K2 unfired since
c >= c_class/10).  Lean-certified instantiation of the best integer-l candidate:
(l=3, w=(1,2,1), u=10): 1/1331 + (2/9261)cos t + (1/29791)cos(2t) >= 0, min =
208917200/367215514281 = 5.6892e-4, with the SOS/factor/corner nonnegativity algebra
and the classical trig identity -- lean/RH11L_ker34one.lean, exit 0, zero sorry.
The literal f-sum substitution (Family A) is refused by the scheme (not a trig
polynomial: no Euler-product identity).  THE DISPATCH: the framework kernel CAN sit
in the classical scheme, but the classical choice is provably optimal -- the
framework's kernel gives a provable-but-weaker zero-free region.  No RH claim.

**RH12 -- the prime-gas self-duality:**
K1 CONFIRMED: no normalized prime-gas log-moment crosses 1/2.  New EXACT identity
M(sigma) = sum_p ln(1 + p^-sigma) = ln zeta(sigma) - ln zeta(2sigma) (sympy/mpmath
verified; the divergence at the critical line: M(1/2) = ln zeta(1/2) - ln zeta(1)
diverges because the Euler product fails at s = 1/2 -- the prime gas has NO
partition function at the self-dual temperature T=2, exactly where the functional
equation's axis sits).  S_half = 175.1141 at p < 10^6 (share of the total -> 0,
divergent).  xi(s) = xi(1-s) verified at 40 dps (residual 2e-41).  The raw
(un-normalized) M crosses kappa = 1/2 at sigma* = 1.8383 (no framework axis; the
identity places no special value at 1/2).  Coincidences registered but not claimed:
M(3/2) = 0.7761 vs pi/4 ~ 0.7854; xi(1/2) = 0.49712 vs ln zeta(2) ~ 0.4971.  THE
DISPATCH: the critical line is where the prime gas's partition function CEASES to
exist -- a thermodynamic reading of the boundary, not a proof.

**RH13 -- the doubled completion (Xi x ladder-beta):**
K2 CONFIRMED (pre-registered honest conclusion): P_l(s) = Xi(s) * B(s,l-s) has
zeros EXACTLY = Xi's zeros (B_l is zero-free, adds poles only).  The doubled
symmetry (axes 1/2 AND l/2) does NOT constrain the zeros: certified in Lean via
the h0 = s(1-s) - 1/8 counterexample -- a member of the doubled class whose roots
(a0 ~ 0.8536, b0 ~ 0.1464) are OFF-AXIS.  17 theorems Lean-certified (exit 0, zero
sorry): beta symmetry, the Gamma(l)-cancellation ratio, AXIS A for ANY h with
h(1-s)=h(s) (Xi cancels), AXIS B for any h (B cancels), the ratio involution,
axes-coincide-at-l=1, the off-axis-zeros-in-class counterexample, and the exact
finite Euler-log identity at sigma=1 over {2,3,5,7,11,13} = 192/1001.  Numerics at
30 dps: all 8 checks PASS, residuals <= 4e-31.  THE DISPATCH: two reflection axes,
NO new zero control -- exactly as the referee (RH07) predicted, now proven.

## THE GROWING LEDGER (additions in bold)

  PROVEN (Lean exit 0, zero sorry): the ladder reflection M_l(s)=M_l(l-s); the
  moment identity E[ln(1+u)]_l = 1/(l-1); the axis census pi/pi/8/pi/4; the exact
  Li constants (to 1e-81); **the 3-4-1 admissibility of the framework kernels with
  equality only at the classical point (alpha >= 1); the doubled-completion no-go
  (two axes, no zero control, certified counterexample); the prime-gas identity
  M(sigma) = ln zeta(sigma) - ln zeta(2sigma); the exact finite Euler-log value
  192/1001 at sigma=1.**
  MEASURED: zeros' spacings = GUE (0.6746 vs 0.6711, 1.0 sigma); spine k2,k3 = GUE;
  repulsion CDF 14x off from the ladder; q-statistics = GUE number-variance null.
  KILLED: F1 (50 sigma), F2 (62-570 sigma), F3-repulsion (14x), the class-spin.
  UNDECIDED (power-gated, registered): the RAR of the zeros -- needs the 5e3-5e4
  budget; the pair correlation -- needs the 5e4 cache.
  NOT PROVEN: RH.  The framework's ladder CANNOT reach it through: the spacing law
  (killed), the moment spine (killed), repulsion (killed), the zero-free scheme
  (provably weaker), the doubled symmetry (provably no control), the prime-gas
  moment (provably no crossing at 1/2).

## THE HONEST POSITION (for the user)

The framework's mathematics is now BOUNDED from below and above in the Riemann
direction: below by the certified ladder algebra (real, zero-sorry, kept), above by
six independent no-go/kill results (measured or proven) showing that the framework's
kernel, moments, repulsion, reflection, and prime-gas structure each fail to reach
the zeros' control.  The single most framework-flavored open door left is the RAR
of the zeros at 5e3+ budget (RH10, power-gated) -- the one test the framework's
SIGNATURE law still awaits.  Everything else in this direction is decided or
provably blocked.  No RH claim has ever been made; none is possible from these
results, and the swarm says so plainly.