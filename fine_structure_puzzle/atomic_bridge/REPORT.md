# Atomic size, baryon mass and alpha: FSP-002

Parent: FSP-001. Assessment: 2026-10-18 America/New_York / 2026-10-19 UTC. **The alpha goal remains open. No value of alpha has been derived.** This phase follows the user's request to investigate atomic size and baryonic mass using the actual framework, without returning to numerical formula searches.

There is a meaningful connection to investigate. The size of an electronic atom depends mainly on electron mass and electromagnetic strength; the proton's mass comes mainly from strong-interaction dynamics. A common microscopic field or a calculable QCD response to cosmic geometry could connect those sectors. We derived two explicit conditional bridges and identified what would make either predictive. Neither bridge is supplied by the frozen gravitational theory yet.

## What the existing framework contributes to an atom

The [frozen canonical theory](../../campaign_fresh_gravity/THEORY_CANONICAL_2026-10-14.md) supplies a macroscopic stiff polarization action and a relation a_M=kappa c sqrt(G rho_DE). It does not specify a quantized electron/proton source, electromagnetic gauge kinetic function or electron Yukawa.

Continuing its static action to a reciprocal microscopic two-body interaction gives, after subtracting a common constant, the local correction

\[
\delta V(r)=\frac{Gm_em_p}{L_*^2}\,r.
\]

This result is conditional on that new microscopic continuation and its boundary matching. It includes the actual stiffness term. The leading short-distance coefficient loses a_M: the cosmic acceleration scale enters nonlinear and environmental matching terms instead. With the conservative L_*=5.75 pc footing, the leading hydrogen 1s–2s shift is approximately 1.16e-78 Hz and the relative mean-radius shift is -7.85e-95. These numbers use measured alpha and masses as diagnostics; they do not predict alpha. A global isotropic screened extension permits an explicit norm bound on the perturbative remainder. That bound does not certify all quantum or anisotropic completions.

For leading Coulomb hydrogen,

\[
a_H=\frac{\hbar}{\mu c\alpha},\qquad
\mu=\frac{m_em_p}{m_e+m_p}.
\]

The logarithmic radius sensitivities are approximately -0.99946 to electron mass and -0.0005443 to proton mass, with the other mass and alpha fixed. Thus identifying a proton mass scale alone does not select atomic size. In a fixed-mass, alpha-independent variational problem H=H_0+alpha V, ground energy is concave in alpha; for attractive atomic Coulomb binding it is strictly decreasing. Atomic energy minimization in this class cannot choose an isolated stable alpha. A nonlinear gauge/scalar/vacuum sector can evade these premises and was therefore tested separately.

Evidence: [hydrogen derivation and run](hydrogen/REPORT.md), [independent action and perturbation review](reviews/HYDROGEN_ACTION_REVIEW.md), [atomic selection claim](coordinator/ATOMIC_SELECTION_CLAIM.md), [cross-review](qcd_mass/ATOMIC_SELECTION_REVIEW.md). The [measurement note](coordinator/MEASUREMENT_BRIDGE.md) explains why atomic recoil or adjusted Bohr-radius data determine alpha observationally without constituting a new microscopic law.

## A concrete QCD–vacuum–mass bridge

The current primary [QCD topological-vacuum proposal, arXiv:2506.14182v4](https://arxiv.org/abs/2506.14182v4), posits Delta epsilon=c_H H Lambda^3 in natural units. Its extension to physical QCD in de Sitter and the coefficient c_H are not calculated in that source. Granting that premise and its asymptotic de Sitter branch, combining it with the framework gives

\[
\boxed{\frac{a_M\hbar^2}{Gc^2m_p^3}
=\kappa\sqrt{\frac{8\pi}{3}}\,
\frac{c_H}{C_p^3}},\qquad
m_p=C_p m_\Lambda.
\]

Here m_Lambda is the mass corresponding to the consistently defined QCD scale. Neither c_H nor C_p is set to one or fitted to the desired alpha. The relation connects the framework's acceleration scale to proton mass through physical matching functions. Electromagnetism affects both functions, so this supplies a specific possible alpha test after their calculation, rather than just a dimensional cube-root coincidence. Applying an asymptotic relation today additionally requires the vacuum evolution.

An exact leading chiral model, retaining electromagnetic contributions to both the hadron mass and vacuum response, shows two useful facts. If light-quark mass remains free, alpha can vary along a local curve preserving proton mass and vacuum acceleration. If that quark mass is independently known and the matching coefficients are calculated, the remaining Jacobian is generically nonzero: those observations can then constrain alpha locally. Independent measured quark masses are legitimate inputs for this correlation test; deriving every Standard Model parameter first is not required. A nonzero Jacobian does not establish a globally unique physical root.

The next quantitative target is the convention-independent ratio R_QCD=c_H/C_p^3 and its electromagnetic response **along the actual independently fixed mass constraints**. A partial derivative at fixed quark/QCD ratios and a derivative at fixed physical quark masses need not coincide. The [final sensitivity note](qcd_mass/CONSTRAINED_SENSITIVITY.md) derives the correct constrained response and its convention invariance. Fitting c_H to dark energy would consume the proposed test.

Evidence: [QCD mechanism, exact discriminator and primary sources](qcd_mass/REPORT.md), [coordinator review](reviews/SCALAR_AND_QCD_REVIEW.md). This candidate has not been added to the frozen framework.

## A common field can connect the gauge and mass sectors

A separately proposed scalar EFT couples a field to the QCD, electromagnetic and mass functions. In an explicitly stipulated IR-matched common-function truncation,

\[
\Lambda=M_U e^{-aB},\quad m_N=C_N\Lambda,
\quad\alpha(0)^{-1}=4\pi k_\gamma B.
\]

If the physical common matching threshold M_U and the matched functions are independently fixed, eliminating B gives

\[
\boxed{\alpha(0)^{-1}
=\frac{4\pi k_\gamma}{a}
\ln\!\left(\frac{C_N M_U}{m_N}\right)}.
\]

This is a possible mass-to-charge bridge, conditional on actual shared dynamics. M_U is a physical boundary scale, not an arbitrary renormalization scale; equality of UV gauge functions does not automatically survive running into this IR relation. The current framework does not derive M_U, the common function, finite thresholds or the scalar potential.

We also found the precise failure if those inputs remain free: an exact family preserves nucleon mass, a leading hydrogen size–mass product, vacuum energy and the QCD scalar profile while changing alpha. The family varies electron mass and physical matching data; it does not preserve every measured laboratory observable or total finite-density scalar curvature. QCD can stabilize a common field without selecting the value of its gauge function. A second two-exponential candidate can select a stationary field value, but it leaves a free amplitude ratio and has a negative vacuum contribution on its stable branch. These are concrete obligations for a future microscopic model, not an exclusion of all such models.

Evidence: [explicit candidate action, family and positive control](scalar_bridge/REPORT.md), [coordinator derivation](reviews/SCALAR_AND_QCD_REVIEW.md).

## Review and next action

Three route agents worked in separate directories. A fourth reviewer independently derived the central action, spectral bound, scalar and QCD identities from the displayed inputs. Its [review](reviews/fresh_atomic/REVIEW.md) records a limitation: a locator search exposed a prior-check summary before derivation, so perfect verdict blindness is not claimed. It audited scripts but did not rerun them or authenticate all external physics. Coordinator and cross-route derivations provide additional checks, with their scopes recorded separately.

Four current bounded calculations completed; the concavity-sign control failed as intended. Their exact records and validator results are in [MANIFEST_VALIDATION.json](reviews/MANIFEST_VALIDATION.json). Symbolic and finite numerical checks establish their declared statements, not uncalculated physical functions or a microscopic completion. Superseded runs and the scalar runner's platform launch failure are preserved. The [reconciliation](reviews/RECONCILIATION.md) identifies current versus historical review claims.

The immediate continuation is to test the QCD cosmological premise and calculate its matched electromagnetic response in a specified scheme and state, with independently selected quark masses. The alternative is one actual common-field microscopic model with a fixed physical threshold and calculated kinetic/vacuum functions. Increasing the precision of the present algebra or searching more formulas near 137 would not supply either missing physical input. See [the continuation](../HANDOFF.md) and [checkpoint FSP-002](../checkpoints/FSP-002.md).
