# Clock constraint operator: exact reduction and all-domain principal positivity

2026-09-10. Continuation of `nonlinear_transport/` at `a4335bb54`;
latest competing commit inspected: `cb471a825` (L166 necessity certificate).
**Full relativistic MOND theory: OPEN.** This is a clock-sector result, not a
MOND action, empirical certification, or a claim of worldwide novelty.

## Same action, explicit scope

In signature −+++ and units c=1, the action being tested is

\[
S=\int\sqrt{-g}\,[M^2(R-2\Lambda)/2+P(X,\tau)
+\sqrt{X_\tau}W(Y,\tau)-V(\tau)]+S_m[g,\psi],
\]

where \(X=-\partial\chi^2\), \(X_\tau=-\partial\tau^2>0\),
\(n_\mu=-\partial_\mu\tau/\sqrt{X_\tau}\),
\(Q=n\cdot\partial\chi\), and \(Y=Q^2-X\ge0\).
The tested initial data omit ordinary matter. χ is openly a matter/clock
degree of freedom, not a hidden auxiliary mode or a particle-CDM addition.

Use the functions and clock history derived in `../nonlinear_transport/README.md`:

\[
P=-\frac U2\log\frac{U-2dX}{U-2dq^2},\quad
W=U+2d\ell(\sqrt{1+Y/\ell}-1),\quad V=U,
\]
\[
U=mqA,\quad d=\frac{AU}{2q(qA+U)},\quad
\ell=q^2m/2,\quad q=Q_c/(1+m),\quad A=I/a^3.
\]

The positive functions are reconstructed, not derived microphysical constants.
Neither the exponential MOND kernel nor κ=1/2 follows from this action.
No environment-dependent a₀ is introduced.

## Actual functional bracket

In clock gauge τ=t, \(H_0=-\int\sqrt h W\). The primary constraints are
\(p_N,p_i\); secondaries are \(C,H_i\). Spatial covariance and the Lorentz-invariant
P(X) lapse sector give the usual spatial momentum term in \(\{C[N],C[M]\}\).
The next constraint is

\[
T=\sqrt h(V_\tau-P_\tau)-\frac{\pi W}{M^2}
-\frac{4W_Y}{M^2}(\pi_{ij}\chi^i\chi^j-\tfrac12\pi Y)
-2Q\partial_i(\sqrt h W_Y\chi^i).
\]

Preservation gives \(E[N]=\partial_\tau T+\{T,H_0\}+\{T,C[N]\}=0\).
The computed lapse block is \(\Delta N=\{T,C[N]\}\).
`derive.py` builds the spatial Ricci tensor from Christoffels, varies the
canonical Hamiltonian, obtains T from H₀, and takes its full spatial-jet
Fréchet derivative. It retains three independent diagonal metric components
depending on x; this is **plane symmetry, not an unrestricted 3D computation**.

The exact result is \(\Delta N=a_2N''+a_1N'+a_0N\), with
\(a_1=\partial_xa_2\). An independent geometric expression for a₀ agrees
identically. Off-shell Hamiltonian-constraint terms in that expression are
essential and are retained. No rank or determinant is assigned by hand.

The associated covariant spatial principal tensor is

\[
S^{ij}=(W-2Q^2W_Y)h^{ij}-(2W_Y+4Q^2W_{YY})\chi^i\chi^j.
\]

The longitudinal coefficient agrees exactly with the functional bracket.
The tensor form also agrees with the preceding action-level local
characteristic calculation. A full 3D functional/formal bridge is still open.

## Strongest new result: all-domain principal positivity

Let \(r=\sqrt{1+Y/\ell}\ge1\), \(D=U-2dX>0\), and \(W_0=U-2d\ell\).
Differentiating W, using \(Q^2=X+Y\), and diagonalizing the rank-one spatial
tensor gives the two eigenvalues

\[
\boxed{S_\perp=W_0(1-r^{-1})+D/r,\qquad
S_\parallel=W_0(1-r^{-3})+D/r^3.}
\]

For the stationary coefficients,

\[
W_0=\frac{mqA(2+m)}{2(1+m)}>0.
\]

Thus both eigenvalues are positive for **every finite point in the regular
domain**, not merely for a finite sample. `ellipticity.py` derives these
identities by symbolic differentiation; `Ellipticity.lean` certifies the
identities and inequalities over the reals (five theorems, no `sorry`).
Lean does not formalize the Einstein variation or infer empirical validity.

At Y=0 both eigenvalues equal D. They can approach zero as D→0, so this
is pointwise ellipticity, **not a uniform bound up to the logarithm boundary**.
A negative-domain control in the script deliberately violates D>0 and
returns negative eigenvalues. No exclusion of that domain is concealed.

## Zero mode, global inverse, and the conditional count

Before any division by a spatial wavenumber the functional result gives

\[
a_2=a\frac{U^2}{qA+U},\qquad
-a_0=\frac{9a^3A^2H^2(1-v)}B>0,
\]

on the finite expanding homogeneous branch, where
\(B=A/q+2A^2/U>0\), \(v<1\) is the previously defined clock-history
variable (not a wave speed). Consequently the homogeneous lapse operator
has a positive k=0 gap as well as positive k≠0 eigenvalues. No H=0 condition
was imposed. `DiracKernel.lean` proves positivity of this expression and
the conditional bracket-kernel elimination.

For a periodic compact domain, uniform S>0 and a uniformly positive
zeroth-order coefficient of −Δ would imply coercivity on H¹. Existence and
uniqueness then require the functional-space realization, coefficient
regularity and boundary hypotheses; positive lapse requires an additional
source/positivity argument. The draft `CoerciveInverse.lean` **did not compile**:
a required cached mathlib object is missing. It is not counted as evidence.
Even a successful abstract build would not supply those physical hypotheses.

The mode block has the form

\[
\begin{pmatrix}0&0&0&-\Delta\\0&0&-\Delta&\gamma\\
0&\Delta&0&\xi\\\Delta&-\gamma&-\xi&0\end{pmatrix}.
\]

SymPy computes determinant Δ⁴ and generic rank four. In function space the
Lean kernel theorem instead makes injectivity of Δ an explicit hypothesis.
If the genuine operator is invertible, preserving E fixes the pN multiplier;
there would be four second-class constraints and six spatial first-class
constraints, giving three modes (two tensors plus χ) from the 22-dimensional
clock-gauge phase space. **This is a conditional count, not completed global
Dirac closure.** The plane-symmetric lapse equation including its source is
now solved numerically on the eight slices below; their evolution and the
unrestricted 3D equation remain open.

## Nonlinear constraint data and numerical evidence

Off-shell distortions on periodic meshes 32, 64, 128 include a negative
lowest eigenvalue at amplitude 0.05. Such data violate the constraints and
cannot reject the physical branch. They motivated `constraint_data.py`:
solve C=T=Hₓ=0 first, using a conformally flat plane metric, nonzero shear,
χ=εq cos(x), and an independently solved constant Q.

Four amplitudes (0, .001, .01, .05), each at 8 and 16 spectral modes,
give eight solutions. Mean conformal log and shear are fixed to zero;
mean χ charge is **not** fixed across the family. The grid is oversampled
eightfold. Eigenvalues are those of a symmetric flux-form discretization.

At ε=.05, 16 modes, 128 points:

- max Hamiltonian residual: 1.075×10⁻¹²;
- max momentum residual: 3.190×10⁻¹²;
- max tertiary residual: 3.416×10⁻¹⁸;
- minimum principal coefficient: 8.163×10⁻⁴;
- minimum geometric mass coefficient: 5.055×10⁻³;
- minimum discretized eigenvalue: 5.135×10⁻³;
- solved Q: .9096508256; mean charge: .1001746935.

All eight data sets have positive tested kinetic/domain/principal/mass
quantities and eigenvalues. Residuals improve from approximately 10⁻⁸
at 8 modes to 10⁻¹² at 16 modes for the largest amplitude.
These are floating-point spectral solutions, not interval-certified continuum
data, empirical measurements, or a 3D nonlinear evolution proof.

## Next gate attacked: actual preservation source and positive lapse

`lapse_source.py` independently reconstructs the constrained data and operator,
then computes F₀=(∂τT+{T,H₀})/√h. Define Z=Kᵢⱼχⁱχʲ,
J=∇ᵢ(w₁χⁱ), w₁=∂W/∂Y, and B=2P_X+4Q²P_XX. The zero-lapse
Hamiltonian and explicit-clock flows give

\[
\dot Q_0=-2(J+QP_{\tau X})/B,\quad
\dot K_0=(-3W/2+w_1Y)/M^2,\quad
\dot Z_0=(-WY/2-w_1Y^2)/M^2,
\]

and hence

\[
F_0=V_{\tau\tau}-P_{\tau\tau}+W_\tau K-2(\partial_\tau w_1)Z
-2Q\nabla_i[(\partial_\tau w_1)\chi^i]
+\frac{4(J+QP_{\tau X})^2}{B}
+\frac{-3W^2/2+2Ww_1Y+2w_1^2Y^2}{M^2}.
\]

Clock derivatives of the reconstructed coefficients are calculated from the
previously derived history ODE, at fixed X,Y; the additional Q flow accounts
for fixed canonical momentum. The metric H₀ flows are checked against
canonical differentiation. Solve **−ΔN=√h F₀**, rather than assigning N=1.

All eight slices have positive source and lapse. At ε=.05 and 16 modes:
**.99554516 ≤ N ≤ 1.00643902**, with linear-system residual 3.36×10⁻¹⁶.
The homogeneous run independently recovers N=1 to roundoff. Reversing the
source reverses the solved lapse sign, a mutation control. The largest-amplitude
8-to-16-mode lapse extrema change by about 5×10⁻⁶. The independent reconstructed
operator agrees with the earlier one within the explicit tolerance.
This closes a finite initial-slice check, not preservation for finite time.

## Reproduction and actual exits

`run_001/checks.json` records exact argv, working directories, output and
exit status for six commands. The three computation manifests record the repository
revision, dirty state, input hashes, results, environment and resource bounds.

| Check | Exit | Meaning |
|---|---:|---|
| sample_operator.py (also runs derive.py) | 0 | exact plane bracket checks; off-shell signs reported honestly |
| constraint_data.py | 0 | all eight finite solves and reported regularity gates |
| DiracKernel.lean | 0 | two conditional algebraic proofs |
| CoerciveInverse.lean draft | 1 | missing mathlib object; no certificate |
| stationary.py regression | 0 | preceding action/profile/characteristic checks |
| Stationarity.lean regression | 0 | preceding coefficient proofs |
| ellipticity.py | 0 | exact principal-eigenvalue reduction and controls |
| Ellipticity.lean | 0 | five real-algebra proofs |
| lapse_source.py | 0 | eight sourced lapse solves; homogeneous and source-reversal controls |

The first suite exits **1 / INCOMPLETE**, deliberately preserving the draft
failure. The separate ellipticity and lapse runs exit 0. A valid provenance manifest
does not turn a failed suite into a successful one.

Regenerate into fresh directories using the actual commands in the manifests,
or invoke `run_checks.py --result-file <fresh>/checks.json` and
`run_ellipticity.py --result-file <fresh>/checks.json` from the repo root.
No global dependency install or operating-system tuning was performed.

## Next unavoidable calculation

Evolve these constraint-satisfying data while solving the sourced lapse
equation at each step; verify preservation, positive lapse, and distance from
the logarithm boundary. Then certify the full 3D operator/inverse and
interaction/caustic behavior.
The MOND coupling must be added at action level and the entire constraint
chain recomputed: this clock-sector certificate cannot be transferred to an
AeST or f32 action by juxtaposition. CMB, lensing, PPN, measured G, the
global a₀ relation and Lyα remain separate, unresolved same-action gates.

Mathbox computation-audit and proof-audit self-review separated exact algebra,
conditional Lean proofs, numerical evidence, and physical obligations. Final
proofreading covered this new report; no unrelated research was rewritten.
Carl Zimmerman's primordial-clock direction motivated this line of work;
the new computations here neither derive κ=1/2 nor claim a new law of nature.

## First-principles requirement (Carl's explicit clarification)

This action is a reconstructed mathematical testbed, not the requested final
derived theory. It is not enough to tune functions until the gates pass.
A proposed completion must state its independent physical/symmetry principles,
show which operators and coefficients they determine, distinguish free
parameters from predictions, and derive the observational laws from that same
action. In particular, assuming the exponential kernel or the coefficient
identity that makes κ=1/2 is not a derivation of either. The present proofs
establish consequences of this chosen action; they do not establish why nature
must choose it. No empirical closure is asserted.
