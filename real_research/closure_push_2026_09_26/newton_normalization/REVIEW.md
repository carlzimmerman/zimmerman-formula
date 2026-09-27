# Independent review of the measured-Newton normalization branch

Reviewer: the independent lapse/source-response route, 2026-09-26.
Science files were read only. This review adds no numerical scan or changed
action assumption. It compares the derivation with a separately derived
general trace/lapse/U source transfer in `../lapse_kinetic/`.

**Verdict:** the stated normalization construction, frozen scalar reduction,
moving-source preferred-frame formulas, and FRW/vacuum-offset distinction are
correct for the specified exponential-AQUAL khronometric action family. Their
scope needs an explicit pin to the old target after the concurrent spec change.
The result is neither a current `nu_mono` closure nor a universal obstruction.

## Exact inputs and provenance

Reviewed hashes before any subsequent author revision:

- `RESULT.md`: `350f841e4021c4d6b6dd8c02daccadd01334d23201656f9a73633f77f9fa5c55`
- `check.py`: `a4c64c756efed0474dcaac9c72c094a32b040a8a2fc5df209b7b71836bbb5501`
- `PushNewton20260926.lean`: `93078a8127212d04e5730003bcbcd64c87ad054d2ca82d5735d91e6495d2548c`

`run2/manifest.json` passed the installed mathbox validator with `--root`
against current input and result hashes. Its 22 checks and resource limits
are properly recorded. The first failed real-amplitude solve is retained and
the accepted script correctly solves the complexified Fourier system.

The Lean source hash agrees with `lean_attempt1_record.json`. The referenced
log exists and reports eight declarations with only `propext`,
`Classical.choice`, and `Quot.sound`, compiler exit 0. It contains two harmless
linter warnings (unnecessary sequencing and an unused hypothesis); it should
not be described as a warning-free compile. No proof admission is present.
The report currently claims only exit 0 and standard axioms, which is accurate.

## Static normalization and principal dynamics

The identity `-2a^2+F_C=-2C a0^2 G` is an integrated nonrelativistic static
density. Minimal source variation gives measured `G_N=G_bare/C`. Calling it
an exact general-source AQUAL relation is appropriate **within that weak-field
static density**, not as a derivation of the entire relativistic theory's
finite-field equations.

The radial Hessian check correctly distinguishes its transverse and
longitudinal eigenvalues. The bound on
`mu_L=1+(x-1)exp(-x)` and its attained maximum at `x=2` establish the whole
positive-acceleration interval, rather than only sampled points. The separate
Lean proof establishes this exponential inequality. The transverse inequality
is immediate from `0<1-exp(-x)<1` for `x>0`; that particular statement is not
one of the eight named Lean declarations.

The same-action reduction gives
`kappa=2(2+3B)/B`, `cs^2=2(2-E)/(kappa E)`. The `C=1/2,B=1/10` witness
has `kappa=46` and `E_min=1-exp(-2)>0`; its maximum principal speed squared is
`2(1+exp(-2))/(46(1-exp(-2)))<1`. The float check in the script is not needed
for the inequality: `exp(2)>7` already bounds it by `4/69<1`.
At `x=0`, `E=2` and the stiffness vanishes, exactly as the report acknowledges.

The compact planar-source division has the claimed degree at most one. It is
only that generator's contact test. It does not establish absence of
instantaneous physical response for all conserved three-dimensional sources.

## Independent moving-source normalization check

The independent calculation in
`../lapse_kinetic/check_ppn_gyro.py` starts from an enlarged kinetic family,
eliminates the constraints, and then performs the same physical boost with an
independently organized contraction formula. Its accepted
`run_ppn_gyro_001` includes the `r=s=0` specialization as an exact benchmark.
It gives

\[
 {h'_{00}\over8\pi G_N M/k'^2}
 =1+2E v^2+
 {E(E-B+2EB)\over B(2-E)}v^2\cos^2\theta+O(v^4).
\]

The normalization includes all four factors that could have caused an error:
the source density `rho=gamma M`, metric boost, Fourier Jacobian, and
`G_N=G_bare/(1-E/2)`. The Einstein transverse shift contribution is also
included. There is no missing or extra factor of `C` in the final ratios.
Consequently `alpha1=-4E` and the reported `alpha2` are correct. The GR control
vanishes. This review's independent derivation does not rely on importing
the quoted external paper's PPN formula; the report's external citation audit
remains a separate provenance item.

The transverse direction has `omega=0`, so purely scalar velocity mixing
cannot change the isotropic `v^2` coefficient while the static response,
minimal matter metric, and Einstein vector sector are held fixed. Our larger
family changes `alpha2` but leaves the same `alpha1`, independently supporting
the report's statement. This argument is not a restriction on an extension
that changes one of those assumptions.

For the exponential branch, `E_infinity=2(1-C)` and its all-x positive-tangent
window imply the stated strict floor `|alpha1|>8/(exp(2)+1)`. The historical
observational bound is correctly labeled historical; this review does not
turn it into a new 2026 observational analysis.

## Cosmological normalization and constant term

The lapse variation of
`a^3[-(6+9B)H^2/N-2Lambda N]/(16pi G_bare)` yields
`3(1+3B/2)H^2=Lambda+8pi G_bare rho` at `N=1`, so
`G_cosm/G_N=C/(1+3B/2)`. The sign of the asymptotic constant is also correct:
`-2Lambda+4C a0^2=-2(Lambda-2C a0^2)`. The homogeneous background instead has
zero acceleration and `F_C(0)=0`. Therefore the large-acceleration constant
cannot by itself be identified with cosmological dark energy. The report
keeps that distinction and does not claim to derive Lambda.

## Concurrent target change: which conclusions survive

The current spec at commit `9092fc0fd02b904e87c708971335cd63adb18151` has hash
`851e44ab8f8a67f2779f16aa01945b149e62d30a7292b73e7ca2419c2b4e0390` and replaces
the operative kernel with filtered `nu_mono`, adopting criterion B.
`RESULT.md` should state that its exponential-AQUAL calculation is a retained
pinned branch, rather than calling it simply “the target.”

- The exact mathematical construction and its normalization lesson remain
  valid for that branch.
- The bound `C<1/(1+exp(-2))` and resulting preferred-frame floor depend on
  the exponential derivative maximum. They do not automatically apply to
  filtered `nu_mono` without deriving that action's own Hessian and source map.
- The conditional asymptotic formulas `alpha1=-4E_infinity`, the displayed
  `alpha2`, and `G_cosm/G_N` remain relevant to any proposed action actually
  belonging to this same family. They are not inherited merely by naming a
  different phenomenological kernel.
- Under criterion B, an instantaneous leafwise term is not itself a rejection.
  Its boundary prescription and well-posed evolution still need proof. Genuine
  negative kinetic/stiffness and observed preferred-frame conflicts remain
  separate physical problems.

## Symmetric penalty completion: regularity and exact constants

For the positive window define
`m=4[1-C(1+exp(-2))]>0`. The full radial primitive has
`Hess F_C>=m I`, including at the origin where its Hessian is `4I`.
Its expansion `2|a|^2-(4C/(3a0))|a|^3+O(|a|^4)` shows it is globally C2,
although generally not C3.

The proposed symmetric bracket

\[
 B_s(a,w)=F_C(a+w)+F_C(a-w)-2F_C(a)
\]

is globally C2 by composition. It has zero value and first variation at
`w=0`; its quadratic term is `w^t Hess F_C(a) w`. Its integral representation
and derivatives give, with `a` fixed,

\[
 B_s(a,w)\ge m|w|^2,\qquad
 \operatorname{Hess}_w B_s\ge2m I.
\]

Thus the positive auxiliary penalty
`P=r^2 B_s/(2 delta^2)`, for `r!=0,delta!=0`, obeys

\[
 P\ge {r^2m\over2\delta^2}|w|^2,\qquad
 \operatorname{Hess}_wP\ge {r^2m\over\delta^2}I.
\]

These factors of two check out. Strong convexity is in the auxiliary gradient
`w` at fixed acceleration and metric, not jointly in all gravitational fields.
The action contains `-P`; uniqueness is most clearly stated for minimizing
the positive auxiliary functional with fixed boundary/harmonic data.
With `w=DU+a`, its quadratic coefficients are exactly
`zeta_i=r^2 E_i/delta^2` in both tangent directions. It therefore improves the
raw Hessian penalty (not generally C1 off shell at zero acceleration) and the
asymmetric Bregman penalty (C1 globally) without altering the static branch.
The independent exact checks are in `../lapse_kinetic/run_integrated_001`.
No full gravitational constraint or propagation theorem follows just from
this auxiliary convexity calculation.
