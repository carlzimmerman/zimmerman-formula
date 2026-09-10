# Physical action audit — 2026-09-10

## Verdict and provenance

**Historical CAM: DEAD as the claimed attractive-MOND action.
Minimal sign-corrected fork: OPEN with scalar and lapse-ellipticity
obstructions; not a complete gravity theory.**

The claims from a5fd5fdad and the counterterm proposal were checked against
the physical matter action, EH curvature reduction, multiplier identity,
and coupled lapse/shift/scalar Hamiltonian. Passing the old surrogate tests
did not validate these bridges. L108/L109's reproduction of that surrogate
does not repair its action mismatch. L110's background inference does not
certify cosmological perturbations. This report supersedes the old wording.

Carl supplied the exponential-law target, acceleration-scale framework, and
primordial-clock direction. The erroneous action-to-test claims came from
this assistant's work; they are not consequences of Carl's fitted coefficient.
Independent read-only audits in this task reconstructed the multiplier and
clock calculations. Novelty of the obstruction statements is unestablished.

## Physical source and coefficients

The minimally coupled particle action fixes
\[
 -m\sqrt{1+2\Phi-v^2}=-m-m\Phi+\tfrac12mv^2+\cdots.
\]
Thus matter supplies \(-\rho\Phi\). Keeping positive EH tensor energy
does not permit flipping only this source sign.

Direct Christoffel/Ricci expansion of the isotropic four-metric restricted
to one coordinate, and integration by parts, give
\[
 {\cal L}_{EH}^{(2)}=M^2[(\Psi')^2-2\Phi'\Psi'].
\]
The raw and integrated expressions have identical higher-derivative Euler
equations in both potentials. The old difference-square block adds
\(M^2(\Phi')^2\), a real acceleration operator.

Independently varying the \((\eta,\sigma)\) family in ACTION.md gives
\[
 E_\Psi=2M^2(\Phi''-\Psi''),\quad E_\ell=u'-\Phi',
\]
\[
 E_\Phi=2M^2\Psi''-2\eta M^2\Phi''+\ell'-\rho,\quad
 E_u=-[2\sigma M^2\mu(u'/a_0)u'+\ell]'.
\]
After variation, under boundary data removing harmonic slip,
\[
 \partial_x\{[1-\eta-\sigma\mu]\Phi'\}=\rho/(2M^2).
\]
The original \((0,2)\) yields \(1-2\mu\); the counterterm proposal \((1,2)\)
yields \(-2\mu\), a repulsive source relation. Matching for all \(y\) requires
\[
 \eta=1,\quad \sigma=-1,\quad G_N=\frac1{8\pi M^2}.
\]
Lean proves this coefficient implication for equality over \(0<\mu<1\).
It is matching, not a first-principles derivation of the kernel or \(\kappa\).
The previous circular-orbit series remains a conditional consequence of
exponential AQUAL, not empirical validation or a newly established Kepler law.
Leading no-slip follows from the metric equation in this approximation;
full PPN gamma, beta and preferred-frame parameters are uncomputed.

## Exact multiplier redundancy

Write \(B_i=D_i u-a_i\). The tensor constraint
\([D_{(i}B_{j)}]^{TF}=0\) follows from \(B_i=0\). On closed leaves, compact
support, or boundary conditions removing the surface term,
\[
 \int\sqrt h(\ell^jB_j+\Lambda^{ij}D_iB_j)
 =\int\sqrt h(\ell^j-D_i\Lambda^{ij})B_j.
\]
The bulk redundancy is \(\delta\Lambda^{ij}=T^{ij}\),
\(\delta\ell^j=D_iT^{ij}\). Boundary charges need separate analysis.
At finite Fourier \(k\), vector rank is one and adding tensor rows leaves
it one; the zero-mode rank is recomputed as zero.

In unitary gauge \(B_i=\partial_i(u-\ln N)\). The linear tensor constraint
contains \(\delta u-\Phi\), not \(\Phi-\Psi\). A counterexample to the
constraint implication is \(N=1,u=0,h_{ij}=e^{-2\Psi(\mathbf x)}\delta_{ij}\)
with small smooth compact-supported nonzero \(\Psi\). Both multiplier
constraints vanish, though \(\Phi=0\ne\Psi\). This is not asserted to solve
the complete metric equations.

At fixed \(N,u\), the spatial metric variation of the multiplier block
vanishes on \(B_i=0\); it cannot cancel an independent on-shell TF stress.
The old \(S_{TF}z+k^2\Lambda z\) block has no derived identification of \(z\)
with metric slip. Its claimed stress-cancellation evidence is withdrawn.

## Actual coupled scalar Dirac calculation

For the repaired action with \(C=V=0\), choose unitary clock gauge, spatial
scalar gauge \(h_{ij}=e^{2\zeta}\delta_{ij}\), \(N=1+n\), and covariant
shift \(N_i=\partial_iB\). At Minkowski \(Q=O(y^3)\). For \(k\ne0\),
\[
 L_k=M^2[-3\dot\zeta^2-2k^2B\dot\zeta
       +k^2\zeta^2+2k^2n\zeta+\eta k^2n^2],
\]
\[
 H_c=-\frac{(p+2M^2k^2B)^2}{12M^2}
     -M^2k^2(\zeta^2+2n\zeta+\eta n^2).
\]
Only PRIMARY multipliers enter \(H_T=H_c+v_Bp_B+v_np_n\).
Primaries are \(p_B,p_n\); secondaries are equivalent at nonzero \(k\) to
\(p+2M^2k^2B,\ \zeta+\eta n\). The normalized Poisson matrix is
\[
 \begin{pmatrix}
 0&0&-2M^2k^2&0\\0&0&0&-\eta\\
 2M^2k^2&0&0&-1\\0&\eta&1&0
 \end{pmatrix}.
\]
The script computes the unnormalized determinant
\(16(M^2)^4\eta^2k^{12}/9\), rank four, zero first-class and four
second-class constraints in this gauge-fixed scalar sector.
Preservation fixes \(v_B=-n-\zeta\),
\(v_n=(p+2M^2k^2B)/(6M^2\eta)\); all residuals vanish, with no tertiary.
The remaining scalar pair satisfies
\[
 \{\zeta,p\}_D=1,\quad H_{\rm red}^{(2)}
 =M^2k^2(1-\eta)\zeta^2/\eta.
\]
At \(\eta=1\), the Hamiltonian vanishes but the rank stays four.
Lean verifies that the normalized bracket map has no null vector for
nonzero \(M^2,k,\eta\). Zero quadratic energy does not remove the pair.
This is not the old all-auxiliary toy count or a full nonlinear DOF proof.

## First nonlinear scalar interaction

For \(N=e^n\), set \(S_{ij}=B_{ij}-\zeta_iB_j-\zeta_jB_i+
\delta_{ij}\zeta_kB_k\). The exact conformal ADM kinetic action is
Legendre-transformed before expansion. First-order stationary auxiliary
solutions are \(n_1=-\zeta,\Delta B_1=p/(2M^2)\); higher auxiliary corrections
do not enter the cubic Hamiltonian because the quadratic one is stationary
on these solutions. With periodic/decaying boundaries and harmonic modes
excluded,
\[
 H^{(3)}=-\frac1{4M^2}\int(\Delta\zeta)|\nabla\Delta^{-1}p|^2
       +\frac{2M^2}{3a_0}\int|\nabla\zeta|^3.
\]
The norm-cubed term uses positive amplitude scaling, not an analytic cubic
Taylor expansion at zero gradient. For \(\zeta=A\cos2x,p=P\cos x\) on
\([0,2\pi]\), the kinetic term is \(-\pi AP^2/(2M^2)\).
Scalar interactions survive the quadratic degeneracy. A cubic sign alone
does not establish a ghost or full nonlinear instability.

## Scoped no-go for a globally elliptic lapse

The minimal repair has \(F=2M^2a_0^2[1-(1+y)e^{-y}]\). At fixed ADM spatial
metric and momentum, EH is linear in \(N\). Direct differentiation of
\(NF(|\nabla N|/N)\) gives
\[
 \frac{\partial^2(NF)}{\partial(\partial_iN)\partial(\partial_jN)}
 =\frac{2M^2e^{-y}}N(h^{ij}-y\hat a^i\hat a^j).
\]
Thus, up to overall sign, the lapse-constraint bracket has principal symbol
\[
 \boxed{{\cal P}_N(k)=\frac{2M^2e^{-y}}N
 [k_\perp^2+(1-y)k_\parallel^2].}
\]
It is elliptic for \(0\le y<1\), radial-degenerate at \(y=1\), and
nonelliptic for \(y>1\). Every \(y>1\) has the nonzero characteristic covector
\((1,\sqrt{y-1})\). Lean verifies the mixed signature and all-\(y>1\) witness.

Therefore the minimal acceleration-only Einstein-clock completion of this
exponential law cannot have a uniformly elliptic lapse across all
accelerations. Positive MOND flux stiffness \(\mu,\mu+y\mu'\) belongs to
a different operator. Extra operators or canonical constraints change the
assumptions. This is a local principal statement, not proof of a global
kernel, ghost, or universal no-go for relativistic MOND.

## Homogeneous modes and remaining gates

For \(C(\tau)\sqrt X-V(\tau)\), varying before lapse fixing gives
\[
 \rho_\tau=V,\quad p_\tau=C\sqrt X-V,\quad
 E_\tau=-V'-C\nabla_\mu n^\mu.
\]
The claimed \(C=V=C_0e^{-3H\tau}\) satisfies the clock equation on prescribed
de Sitter but has positive dust energy \(C\). Bare vacuum de Sitter fails
the coupled Friedmann equation unless \(C_0=0\).

The \(k=0\) quadratic Minkowski primary chain is recomputed without dividing
by \(k\); it does not replace nonlinear FLRW constraints. Independent
minisuperspace lapse variation yields
\(3M^2H^2=M^2\Lambda+\rho+V\). For \(C=V=0\) expanding backgrounds exist.
Cosmological perturbations, observations, and homogeneous nonlinear
constraint closure remain unproved.

The next construction must change both the actual scalar constraint
algebra and the lapse operator while preserving physical static variation.
Adding a derivative of an existing constraint supplies no independent
constraint. Full PPN, causal response, nonlinear/background-dependent
stability, and the \(a_0\)-\(\Lambda\) derivation remain uncertified.

## Literature and reproduction

The repaired action maps to Blanchet & Marsat,
[arXiv:1107.5264v1](https://arxiv.org/pdf/1107.5264v1), Eq. (2.4), by
\(f(a)=\Lambda-a^2+a_0^2Q(a/a_0)\), \(M^2=(8\pi G)^{-1}\).
Their Eqs. (2.7),(4.6) have \(\mu=1+f'(a)/(2a)\), giving the same law.
This is known architecture after notation translation. Checked 2026-09-10
against the primary PDF. Search scope: “Blanchet Marsat preferred foliation
acceleration action” and adjacent khronometric MOND results; not a global
novelty search. No source PDF retained. Our obstruction derivations do not
depend on unverified claims from an abstract.

Run in this directory:

    python3 -B physical_action_audit.py
    python3 -B physical_action_audit.py --require-closure
    python3 -B cuscuton_acceleration_mond_gate.py
    python3 -B cuscuton_acceleration_mond_gate.py --historical-block-only
    python3 -B -m unittest -v test_cuscuton_acceleration_mond.py
    python3 -B run_cuscuton_acceleration_lean.py
    python3 -B clock_principal_gate.py
    python3 -B kepler_prediction_gate.py
    python3 -B eh_static_reduction_gate.py

Audit success means the obstructions reproduce. Closure and historical
action-bridge commands must fail. Historical-only success checks surrogate
algebra; clock-gate success checks frozen-metric kinematics only.
Lean prints accepted axioms and uses no sorry or custom physical axiom.
See run_002/manifest.json and stdout.txt for pinned inputs, actual versions,
commands, test statuses and log hashes.
