# Independent bounded review of L216 / PAPER25

The normalized claim is: the stated cuscuton/projected-gradient action, with
the L215 matter metric, admits a Solar-System solution whose residual clock
misalignment obeys the quoted preferred-frame bound when
`s0 >= approximately 1.5e7`, leaving no obstruction to this construction from
the Solar System apart from explaining that parameter and its interaction
scale.

**Primary verdict: incomplete, with the smallest missing implication being
the derivation and solution of the correctly normalized, coupled clock
equation from the proposed action.** The displayed clock equation and its
gain do not follow from the action as used. In particular, the advertised
linear enhancement by `s0` disappears even in the paper's frozen-W truncation
when the physical tilt is normalized consistently. This finding refutes that
specific enhancement argument; it does not prove the construction impossible.

Review date: 2026-09-12. Target base: `486edc78eaed87647c0b605cdbebccb996a464cf`.
No source manuscript, old computation, or shared status was edited. L216,
L215, PAPER25, and the two prior audit reports used here were confirmed
unchanged from that base. The working repository advanced independently to
`e1c8071de5e4fb52243d5d6e7bfd12d7540f2a28` by the recorded run; its manifest
truthfully records that execution HEAD and the individual before/after hashes.
The raw audited inputs remain preserved by their base Git objects; the run
also preserves a fresh original-script stdout and JSON in its own directory.

## Claim card and dependency graph

Conventions: signature `-+++`, a timelike clock with `s>0`,
`n_mu=-partial_mu tau/s`, `Q=n^mu partial_mu chi`,
`X=-partial chi . partial chi`, and `Y=Q^2-X`. Photons and matter are assumed
minimally coupled to `gtilde=Cg+D n n`, with `C>0,C-D>0`. PAPER25 specifies only
the leading factors `C=1-2 varphi`, `D=-4 varphi`. Its high-acceleration and
uniform-density stellar surrogates are additional hypotheses, not solutions
of the coupled action. Its nonzero scalar potential and nonzero physical
Newtonian potential are required when dividing to form potential ratios.

The claimed chain is:

1. Leading metric expansion plus baseline `Phi=Psi` gives equal physical
   potential shifts, and locks `b=2a` for nonzero `varphi`.
2. A presumed `W0=0` decoupling branch permits freezing the scalar and varying
   only `s`, giving an isotropic clock stiffness `W`.
3. An assumed high-acceleration scalar profile gives `W proportional to r^-4`
   and an assigned surface gain `24 s0/fs`.
4. A vacuum dipole exponent transfers that gain to one AU; an assumed local
   residual formula `1/(1+D)` converts it into clock alignment.
5. A one-component PPN identification supplies `alpha1=8fs` and the residual
   threshold. Inverting then yields `s0 approximately 1.5e7`.
6. Earlier stability, source, and propagation conclusions are presumed to
   survive the new matter coupling and background.

The algebra in steps 1 and the exponent calculation in step 4 is valid under
its hypotheses. Steps 2, 3's physical interpretation, 4's matching, 5's PPN
identification, and 6's transfer are not established.

| Obligation | Status | Exact supported scope or gap |
|---|---|---|
| `b=2a` lock | Passed conditionally | Leading weak-field shifts, nonzero scalar, baseline no slip; not arbitrary finite potentials or baseline anisotropic stress |
| No pure clock time kinetic term in `s` | Passed | Quadratic expansion about a timelike affine clock; not a complete metric/scalar constraint analysis or proof of ellipticity |
| `W` is the physical tilt stiffness | Failed | It is `s0 W` even when Y is frozen; varying Y adds further terms |
| `W0=0` removes clock response | Failed in inherited principal surrogate | Its own response is `sigma/pi=s/q`, not zero, for nonzero q and W_Y |
| Physical gain `24 s0/fs` | Failed as derived | Algebraic ratio is correct, but inconsistent perturbation normalization makes it the wrong physical gain |
| Exterior exponent | Passed conditionally | `p=(sqrt(17)-1)/2` for an isotropic positive weight proportional to r^-4 and the decaying l=1 branch |
| Interior-to-AU alignment | Not addressed | No interior solution, angular matching, or justification of applying saturation after exterior decay |
| `alpha1=8fs` | Not established | A nonzero O(varphi w) mixed metric term is identified; full PPN matching is absent |
| Common photon/tensor cones | Failed conditionally | For unchanged g tensor cone, nonzero D gives distinct cones even with exact alignment |
| `s0>=1.5e7` | Not established | Conditional arithmetic only; physical antecedents fail or remain uncomputed |
| Strong-coupling cutoff | Not addressed | A coefficient ratio is not a canonically normalized interaction scale |

## Decisive local normalization check

PAPER25 section 3 / L216 lines 67-80 uses `tau=t+psi`, thereby setting the
background clock rate to one. Sections 4-6 / lines 89-173 then insert a W
proportional to `1/s0` while continuing to identify `grad psi` with physical
tilt. For general rate, use

\[
\tau=s_0(t+\pi),\qquad
s=s_0\left(1+\dot\pi-\tfrac12|\nabla\pi|^2\right)+O(\pi^3),
\qquad n_i=-\partial_i\pi+O(\pi^2).
\]

Consequently, if W really were fixed in the variation,

\[
\mathcal L^{(2)}_{sW}=-\frac{s_0W}{2}|\nabla\pi|^2.
\]

The matter metric depends on the unit direction n, so its physical tilt
source contains no compensating `s0`. Using precisely PAPER25's assigned
surface potential, density, and W therefore gives

\[
\frac{4\varphi_s\rho_s}{s_0W(R)}=\frac{24}{f_s},
\]

not `24 s0/fs`. Equivalently, with `tau=s0 t+psi`, the quadratic coefficient
is `W/s0` and physical tilt is `grad psi/s0`; both factors must be retained.
This is a discrepancy in the power of `s0`, not a factor-of-two convention.
The value `24/fs` is a correction to a local surrogate, not a replacement
prediction for actual solar alignment.

The paper's large variable is `s0=|d tau|`, not the distinct scalar velocity
`Q=n.d chi`. A field relabeling `tau'=A tau`, `A>0`, has `s'=A s` and leaves
n, X, and Y invariant. The same action is represented by
`W'(Y,tau')=W(Y,tau'/A)/A`, with P and V composed with `tau'/A`.
Thus `sW` and the matter metric stay invariant while the numerical clock
rate changes. An operational interpretation of "ten million times proper
time" requires an explicit fixed normalization of coefficient functions and
the clock. This does not say that changing s0 while holding a fixed action
unchanged is a symmetry. It does show why a physical bound needs invariant
normalization combinations. PAPER25 already fixes `s0 k` through its
high-acceleration matching.

## The projected invariant cannot be frozen during clock variation

In a local flat frame set `chi=q t+v.x`, `tau=s0(t+pi)` and consider static
tilt `z=grad pi`, with `|z|<1`. The exact expression is

\[
Y=\frac{(q-\mathbf v\cdot\mathbf z)^2}{1-|\mathbf z|^2}
-q^2+|\mathbf v|^2.
\]

Write `Wstar=W(|v|^2,tau)` and evaluate its Y derivatives at that point.
Expanding through total degree two in z gives

\[
\begin{split}
Y&=|\mathbf v|^2-2q\mathbf v\cdot\mathbf z
+q^2|\mathbf z|^2+(\mathbf v\cdot\mathbf z)^2+O(z^3),\\
\mathcal L^{(2)}_{sW}
&=s_0\left[\left(-\frac{W_\star}{2}+q^2W_Y\right)|\mathbf z|^2
+(W_Y+2q^2W_{YY})(\mathbf v\cdot\mathbf z)^2\right].
\end{split}
\]

There is also a linear term `-2 s0 q W_Y v.z`. The negative Hessian of this
local spatial quadratic form has eigenvalues

\[
K_\perp=s_0(W_\star-2q^2W_Y),\qquad
K_\parallel=s_0[W_\star-2q^2W_Y
-2|\mathbf v|^2(W_Y+2q^2W_{YY})].
\]

These are contributions of the first-derivative `sW` term only, with metric
and scalar frozen for this diagnostic. They are sufficient to disprove the
claimed derivation by holding W fixed. They are not the full on-shell
gravitational principal operator, and `Wstar` here must not silently be
identified with an effective background combination involving cubic terms.
The script uses the symbol `W0` for this local Taylor value only.

The prior `../../principal_gate/REPORT.md`, section 6, separately records
that its inherited quadratic system has `C=(W0-2q^2W_Y)/s`, `B=2qW_Y` and
`sigma/pi=-B/C=s/q` at `W0=0`. Removing W_Y from one reduced scalar coefficient
is not vanishing clock response. PAPER25's opening claim repeats this
already-audited conflation.

The matter variation is also only asserted in L216's comment at line 86.
Expanding the displayed point-particle metric to first order in varphi and
second order in aligned small tilt z and matter velocity v gives the
tilt-dependent matter Lagrangian

\[
\mathcal L_{m,\mathrm{tilt}}=-2\rho\varphi z^2-4\rho\varphi vz.
\]

The quadratic tilt term contributes at the same order in the linearized
clock equation as the claimed drag response. Its sign must be tracked with
the signed potential; substituting a positive potential magnitude is not a
derivation of an attractive alignment operator.

## The exterior exponent does not determine the alignment amplitude

For the assumed isotropic vacuum equation with W proportional to `r^-4`,
`pi=g(r) cos(theta)` gives `r^2 g''-2r g'-2g=0`; the decaying root and quoted
exponent are correct. This fixes neither the normalization nor the angular
clock-velocity field. In particular `grad(g cos(theta))` has radial and
tangential coefficients `g'` and `g/r`, so a scalar gain is not by itself a
uniform vector alignment condition.

Even granting an illustrative surface saturation `tilt(R)/v=D_R/(1+D_R)`,
linear propagation gives `(D_R/(1+D_R)) (R/r)^p`. PAPER25 instead uses
`D_R (R/r)^p/(1+D_R (R/r)^p)`. These differ parametrically when the surface
gain is large. At `D_R=48` and one AU they are respectively `0.0002232072`
and `0.01081883`. This illustration does not assign either result to the
full theory; it proves the missing amplitude matching cannot be replaced by
the indicial exponent alone. The paper's own equation has no distributed
stellar matter source outside the star that would justify a local algebraic
balance at one AU. The growing exterior solution and the transition out of
the assumed high-acceleration regime also require an actual outer match.

## Physical PPN and propagation gates

The leading metric expansion proves equal shifts only if the unmodified
Einstein-frame solution has `Phi=Psi`. Its "exact" ratio means exact in that
linearized algebra, for arbitrary relative scalar share while all potentials
remain weak. It is not an all-order theorem. Nonzero scalar amplitude is
required for the `b=2a` equivalence; the Lean statement includes that condition.

The new mixed metric component is a valid kinematic O(varphi w) term.
However standard PPN matching uses the whole metric in a fixed gauge and
the measured Newtonian potential. The coefficient of `w_i U` contains
`alpha1-2alpha2`, with additional velocity and tensor potentials. Hence
assigning that one component to `alpha1/2` does not derive `alpha1=8fs`.
The identification of `fs` with a fraction of the *measured total* potential,
the scalar/EH contributions to measured G, and the spatially varying clock
solution must be settled. `fs approximately 1` at high acceleration is an
assumption of these lanes, not a universal MOND requirement.
[Will, arXiv:1403.7377v1, section 3.2 and Box 2](https://arxiv.org/html/1403.7377v1#S3.SS2).

Source record: Clifford M. Will, *The Confrontation between General Relativity
and Experiment*, arXiv:1403.7377v1, 28 March 2014, checked 12 September 2026.
The author's primary presentation of the PPN framework was inspected in
full-context HTML for Box 2, including its definitions of w, U, physical G,
and gauge. The source states the framework; its application to PAPER25 is
the audit's comparison above. No current-best observational bound or novelty
claim is made. No local copy was created. DOI/PMC access attempts failed;
the exact arXiv version succeeded. The paper's supplied `1e-4` threshold is
retained only as an input to arithmetic.

The prior cone calculation was re-run independently of L216. In the local
clock frame, minimally coupled Maxwell propagation has

\[
\frac{c_\gamma^2}{c_T^2}=\frac{C-D}{C},\qquad
\widetilde g(k,k)=D(n\cdot k)^2\quad\text{for }g(k,k)=0.
\]

Here `c_T` is the unchanged g tensor cone, previously derived on the aligned
homogeneous branch. For nonzero null k and timelike n, `n.k` is nonzero.
Exact clock alignment therefore cannot identify the two cones for `D!=0`.
For the L215 leading metric, the photon-to-tensor speed-squared ratio is
`1+4 varphi+O(varphi^2)`. Combining nonzero equal shifts with common cones
fails for this shift-only repair with the baseline g cone unchanged.
This is not an empirical GW170817 exclusion without a propagation profile
and emission model, nor a claim about arbitrary inhomogeneous tensor
characteristics. It is a separate physical gate that PAPER25's clock-rate
number does not address.

## Strong coupling and the inherited sound-speed statement

The arithmetic `mrel=1e-4/(s0-1)` and `PX/d=1/mrel` reproduces the quoted
small margin and large ratio when the unestablished rate is inserted.
A large kinetic coefficient alone neither proves strong coupling nor
establishes weak coupling. The required calculation is the constrained
quadratic action plus cubic and higher interactions on the same background,
canonical normalization, and comparison of the resulting interaction scales
with the spatial and temporal scales being used. No such calculation is
performed in L216; `PX/d>1e6` is an arbitrary flag, not a cutoff criterion.

The statement that `cs^2=-w/(2-mrel)` is independent of s0 is not exact when
`mrel=w/(s0-1)` is imposed. Its dependence becomes small at large s0 but does
not vanish. With the positive `w=1e-4` used for the numerical substitution,
this expression is negative. L213 explicitly calls that its zero-gradient
criticality driver; it must not be relabeled as a positive scalar-stability
test. No health result is transferred here to the changed disformal branch.

## Computation and certificate scope

`check_clock_claims.py` ran the original script unchanged in a separate
working directory, preserving its raw output. L216 returned 8/8 PASS and its
fresh results JSON equals the committed JSON. Its assertions check supplied
expressions and comparisons, including treating violation of an observational
threshold as a passing diagnostic. This is faithful reproduction, not
independent validation of those expressions as field equations.

The new script checks 15 local identities/controls, including the independent
34-check disformal-cone derivation. All passed. The physical-tilt and
projected-Y computations use exact symbolic arithmetic through quadratic
order in all three tilt components; a spatial rotation aligns the background
scalar gradient with the first axis. The numerical surrogate uses only the
paper's solar radius, one AU, residual threshold, and illustrative D=48.

The four Lean statements in `Mondlean.lean` lines 1275-1308 prove: coefficient
locking given equal shifts and nonzero scalar; an algebraic ratio; a root of
an assigned polynomial; and inversion given an assumed residual inequality.
They do not formalize clock variation, stellar matching, the identification
of alpha1, physical tensor/photon propagation, or the rate's normalization.
Lean was not recompiled for this bounded review; its declarations were read
to determine their exact assumptions and conclusions.

Run evidence: `run_001/manifest.json`, `run_001/results.json`, and
`run_001/L216.stdout.txt`. The version-2 manifest records actual argv,
before/after input hashes, output hashes, Python 3.9.6, SymPy 1.14.0,
macOS arm64, a 60-second wall cap, one cooperative library thread, and a
1 MiB output cap. Runtime was 0.75444 seconds, exit 0. No random samples,
hard memory cap, CPU affinity, or new package installation was used.
`validate_manifest.py .../run_001/manifest.json --root <repository>` returned
`valid evidence record; mathematical interpretation requires review`.
The complete regeneration argv is in the manifest; choose a fresh output
directory if rerunning via the bounded runner.

The exact arithmetic inversion within PAPER25's assumptions is
`s0 >= 14628851.387690246`; the script's large-gain approximation gives
`14629034.250618378`. This negligible approximation is not the material
problem: the physical antecedents of that inequality are missing.

The strongest safe statement is that the nonzero disformal weak-field
metric gives the displayed equal scalar shifts and mixed metric component;
the assigned r^-4 dipole operator has the stated exponent; and the paper's
conditional numerical arithmetic is reproducible. The Solar-System
alignment bound on clock rate is unestablished. The cheapest next decisive
step is to derive the complete clock/scalar/matter variation in consistent
physical-tilt variables before attempting any stellar integration, then
check whether the proposed cosmological/stellar branch exists with that same
action. This review does not change or reconstruct those coefficient
functions and does not supply a new field-theory completion.

Skills used: Mathbox proof audit, computation audit, literature check, and a
proofreading self-review of this note. The proofreading pass changed no
mathematical claims in the original manuscript; its coverage is this new
review only.
