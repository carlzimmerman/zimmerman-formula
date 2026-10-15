# Source and force dictionary for the conditional multi-current candidate

Checkpoint MC-2026-10-15-01, base `5c06d239febe644b9f485477b4c2f93390a23b3e`. This fixes the meanings used in this package. It does not select these meanings as amendments to the frozen canonical theory.

## Variables and frame membership

For each included dark constituent, J_a is its number current, m_a>0 its assigned rest mass and q_a its signed gauge charge. Define the rest-mass current M=sum m_a J_a and charge current Q=sum q_a J_a. They are separate physical quantities. Rest mass alone is not the complete relativistic stress or energy.

The principal calculation chooses the constitutive frame from the two specified dark-material currents only:

\[
 K^\mu=m_\chi J_\chi^\mu+m_S J_S^\mu,\qquad
 U^\mu=K^\mu/\sqrt{-K^2}.
\]

Ordinary baryons are outside K and all other constitutive arguments of that calculation. Adding a neutral free dark constituent to K gives it constitutive interactions through U even if its minimal gauge charge is zero. Such a changed frame membership needs a new action and mode calculation. Including ordinary baryons would likewise change the model.

Use F=dA, signature -+++, c=1 and the current coupling +q_a J_a.A with phases transforming theta_a -> theta_a-q_a lambda. This fixes the positive Gauss convention. Define the electric and magnetic fields relative to the chosen varied U. The finite-density calculation assumes U exists; it supplies no extension at K=0.

## Rest-mass and charge sources

In a leading spherical rest comparison, let M_a(<r) be the actual enclosed rest mass of species a. Write

\[
 \zeta=\sqrt{4\pi G}=q_\chi/m_\chi,\quad
 b_a={q_a/m_a\over\zeta},\quad
 g_c={G\over r^2}\sum_a M_a,\quad
 u_Q=\zeta D={G\over r^2}\sum_a b_aM_a.
\]

Here D is the radial electric displacement from Gauss law, not an inferred halo mass. A positive massive neutral species enters g_c but has b_a=0. Opposite charge contributes negatively to u_Q while its rest mass remains positive in g_c. Field energy and stress enter the relativistic metric in addition to these rest-mass terms.

For the specified scalar constitutive law,

\[
 D={E\over1+E/D_0},\quad D_0=a_0/\zeta,\quad
 \zeta E={u_Q\over1-u_Q/a_0}.
\]

On the positive electric branch 0<u_Q<a0, the leading radial acceleration of a pressureless resting species is

\[
 a_a=-g_b-g_c+b_a{u_Q\over1-u_Q/a_0}.
\]

Pressure, transverse current-frame forces, reaction recoil and relativistic metric corrections are additional terms outside this rest comparison. A radial collinear boost of a pure electric field leaves its material electric invariant unchanged; that fact supports the restricted radial test, not arbitrary relative motion.

The old single-species reduction requires g_c=u_Q, which is a structural identity for all independent mixtures only when every included charged material species has q_a/m_a=zeta and no additional massive neutral stock is counted in that identity. Then chi rest balance is g_b=u_Q²/(a0-u_Q), and neutral baryons respond to g=g_b+u_Q. For unequal ratios the resulting baryon force is not automatically the old algebraic law.

## Conversion and field evolution

For reactions with stoichiometric coefficients nu_ar and rates R_r,

\[
 \nabla_\mu J_a^\mu=\sum_r\nu_{ar}R_r,\qquad
 \nabla_\mu Q^\mu=0\quad\Longleftrightarrow\quad
 \sum_aq_a\nu_{ar}=0\quad\text{for each independent reaction}.
\]

The corresponding rest-mass source is sum_a m_a nu_ar R_r and need not vanish for an energy-conserving reaction. Four-momentum conservation must include photons, binding, constitutive energy, all receivers and any gravity/source work. The actual illustrative neutron portal changes the sum of rest masses and therefore cannot use the equal-mass tether/free continuity equations unchanged.

Gauge polarization P_Q=D/zeta satisfies div P_Q=rho_Q/zeta. Its evolution includes the Maxwell curl term as well as charge current. Canonical tethered mass displacement P_t instead has div P_t=rho_t-rhobar_t. With local mass transfer S from t to f, its old source-free evolution needs a correction C_t satisfying

\[
 \operatorname{div}C_t=-S-\partial_t\bar\rho_t.
\]

These two polarizations coincide only under their declared source, reference and longitudinal/electrostatic assumptions. A background subtraction is not an uncounted physical compensating charge. The [conversion proof](conversion/REPORT.md) derives the precise compatibility and boundary conditions.

## Nonspherical and exterior interpretation

The candidate action sources its gauge field with actual charge and its metric with actual stress. It does not define positive cold matter by taking a raw norm-weighted divergence of a baryon-only force field. Consequently the negative raw-target witness in the preceding certification record is a constraint on that different interpretation, not a derivation or rejection of this candidate.

This distinction is not a nonspherical completion: the coupled equations, host/basin construction, phase selection and finite-domain interfaces still have to be solved. The remnant work calculation explicitly assigns an exterior scalar force law because the carrier-defined material frame has no supplied vacuum limit. No global halo, source restriction or lensing prediction is inferred from this dictionary.
