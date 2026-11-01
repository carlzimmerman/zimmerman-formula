# TP01-SC coordinator review

Target: determine whether the existing nine LC1 pairs provide a measured
spin–contraction relation and whether the declared conditional transfer can
remove the HS1 tilt while retaining the rotation-curve normalization.

Verdict: the proposed rescue is **not supported in this tested setup**.
This is a finite numerical conclusion, not an exclusion of all spin-dependent
baryonic physics. Review provenance: coordinator code/derivation review and
orthogonal statistical reconstruction; no new particle evolution.

## Data and construction obligations

Passed: the code checks all nine seed/grid/mass/softening identities and the
LC1 disc-axis match to the actual pre-disc angular momentum. The cumulative
profile, smooth-core grid fit, spherical-contraction readout and spin
reproduce the stored LC1/HS1 values. The joint response uses a common z=0
epoch; it never multiplies an initial core strength by a final response.
Original data and simulation code remain inputs, not newly verified physical
laws. Fits near the softening cut, artificial steady discs, one mass and
isolated initial spheres restrict interpretation.

The initial rigid-motion check selected one different boundary particle
after floating-point rotation. Run 002 separately reports that effect and
tests exact invariance on the identical particle mask; the science rows
are unchanged. The failed run remains historical evidence.

## Independent statistical checks

`run_reconciliation/` recomputes permutation tails using integer average
ranks, independently of the author's floating-point rank covariance. All
9! permutations are counted. It also reconstructs three leave-one-out
prediction scores by the PRESS/QR identity rather than explicit deleted
refits. Its completed v2 manifest validates current inputs.

- f_Q versus initial spin: rho=-0.20, exact two-sided p=0.613404.
- f_Q versus initial concentration: rho=0.766667, p=0.021390, but the six-test
  Holm adjustment is 0.128340. This is not a selected discovery.
- Predicting final log S from initial log S has held-out skill 0.841390.
  Adding spin reduces it to 0.782694; spin alone has skill -0.052000.
- Contraction changes S–spin rho from -0.45 to -0.283333 and reduces final
  log-strength scatter from 0.099340 to 0.078126 dex.

The negative result is absence of incremental prediction in these nine
seeds, not evidence that the true population correlation is exactly zero.

## Conditional forward calculation

The forward shell equation is

    r_i M0(r_i)(1+F) = r_f [Mb(r_f)+M0(r_i)].

For nonnegative, nondecreasing masses and r_i>=r_f/(1+F), the left-minus-
right function increases with r_i. The stated lower bracket is nonpositive;
the R200 upper bracket is nonnegative for r_f<=R200 and Mb<=F M200.
The code uses this bracket and separately holds the total outer mass fixed.
Its high-resolution comparison to the inherited shell interpolation passes.
The NR1 and latest NR2 scalar baselines are explicitly reproduced before
interpreting transfer results. Run 004's completed manifest validates.

The pairing is preserved; no independent scatter amplitude or contraction
strength is optimized. The perfect inverse-spin/brightness association is
an expressly stipulated capacity test. It does not measure galaxy spins.
The transfer assumes one-mass homology and the N smooth-core mass/profile
mapping; it is not the OP3 native cumulative profile.

Within that setup, the paired idealized ranking flattens HS1 but requires
median Upsilon around 0.40 on each background, outside [0.50,0.80].
Ranking scatter without the measured contraction can pass the scalar
normalization, but restoring the measured response loses it. The selected
fixed transfers therefore do not pass jointly. This is not an exhaustive
optimization over all admissible spin maps or feedback histories.

## Remaining implication

A physical continuation needs independently specified angular-momentum
retention, environmental torques or feedback that changes the measured
response, followed by the same joint gates. No such new interaction or
new production run was supplied by this checkpoint. Another freely chosen
rank correlation would not test the missing implication.
