# A conditional positive current for a neutral nonrelativistic bath

This addendum preserves the independently reviewed main note at SHA-256
`bb45b6bddef696c689f9e60ca3f4bb608a8ce8914cab694e6027383d675f2fff`.
It addresses a different current: an emergent, charge-even particle count
of a conservative nonrelativistic envelope theory. It is not the exact
microscopic signed U(1) current audited in that note.

**Result:** the leading rotating-wave theory has separate particle and
antiparticle number symmetries, including weighted source-to-daughter
conversion. Their sum is positive and can be dualized even in a neutral
bath. This rescues a restricted reference-density constraint, conditional
on a controlled suppression of number-changing/hard-mode leakage. It does
not derive the rational W, positive exact stress-energy density, that rate
hierarchy, or a one-fluid limit.

## 1. Derivation of the retained conservative theory

Use weakly excited nonrelativistic envelopes with momenta, kinetic energies,
interaction shifts and detuning delta=M-2m small compared with m. Write

\[
 \Phi={e^{-imt}\psi_++e^{imt}\psi_-^*\over\sqrt{2m}},\qquad
 X={e^{-2imt}b_++e^{2imt}b_-^*\over\sqrt{2M}}.                \tag{A1}
\]

Both psi signs describe particles of positive inertial mass m, and both
b signs describe sources of positive mass M. To define the canonical source
envelopes, first reduce the positive/negative frequency branches at their
physical rest frequency M:
X=(exp(-iMt) beta_+ + exp(iMt) beta_-*)/sqrt(2M), dropping the second-time-
derivative terms |dot beta_sigma|^2/(2M) at that NR order. Then rephase
beta_sigma=exp(i delta t)b_sigma. The canonical symplectic term becomes
i(b*dot b-dot b*b)/2-delta|b|^2, and (A1) follows.

This order matters. Direct substitution of (A1) into the relativistic free
X action gives symplectic coefficient 2m/M, mass coefficient
-(M^2-4m^2)/(2M), and |dot b|^2/(2M). Equivalently it is the canonical
rephased NR action plus the discarded remainder
|dot b+i delta b|^2/(2M). Discarding |dot b|^2 alone would miss the
O(delta/M) symplectic correction and the delta^2/(2M) mass correction.
The following is the canonically reduced, rephased NR theory, with its
unretained relativistic time-derivative corrections explicitly excluded.
Averaging the rapidly oscillating interaction terms then gives

\[
 \mathcal L_{\rm env}=\sum_{\sigma=\pm}
 \left[{i\over2}(\psi_\sigma^*\dot\psi_\sigma
                         -\dot\psi_\sigma^*\psi_\sigma)
       +{i\over2}(b_\sigma^*\dot b_\sigma
                         -\dot b_\sigma^*b_\sigma)
       -{|\nabla\psi_\sigma|^2\over2m}
       -{|\nabla b_\sigma|^2\over2M}-\delta |b_\sigma|^2\right]
       -V_{\rm slow},                                      \tag{A2}
\]

\[
 V_{\rm slow}\supset c_3\sum_\sigma
              (b_\sigma^*\psi_\sigma^2+\mathrm{c.c.})
   +k_c(n_+^2+n_-^2+4n_+n_-),\quad
 c_3={g\over2m\sqrt{2M}},\quad k_c={\lambda_{\rm tot}\over4m^2}.
                                                                  \tag{A3}
\]

Here n_sigma=|psi_sigma|^2 and n_bsigma=|b_sigma|^2. The 4 in the elastic
cross interaction follows from the two surviving oscillatory cross products
in |Phi|^4. Modulus potentials/portals yield additional elastic density
terms. This is the direct tree-level RWA before full elastic matching;
fast virtual branches also renormalize its coefficients, as in the root's
same-charge threshold calculation. They do not require violating the
separate number symmetries in the retained conservative soft theory.

Every displayed term is invariant under independent constant angles

\[
 \psi_\sigma\mapsto e^{-i\alpha_\sigma}\psi_\sigma,\qquad
 b_\sigma\mapsto e^{-2i\alpha_\sigma}b_\sigma.                \tag{A4}
\]

This minus-sign convention makes the Noether densities positive in the
symmetrized Schrödinger action. The original exact U(1) is the subgroup
alpha_+=alpha, alpha_-=-alpha. The equal-angle transformation is the new
emergent symmetry; resolving positive and negative frequency envelopes is
part of its definition and is not a new exact local symmetry of Phi,X.

The species equations are

\[
 \dot n_\sigma+\nabla\cdot j_\sigma=2R_\sigma,\qquad
 \dot n_{b\sigma}+\nabla\cdot j_{b\sigma}=-R_\sigma,\qquad
 R_\sigma=2c_3\operatorname{Im}(b_\sigma\psi_\sigma^{*2}),     \tag{A5}
\]

\[
 q_\sigma=n_\sigma+2n_{b\sigma},\quad
 J_\sigma=(q_\sigma,j_\sigma+2j_{b\sigma}),\quad
 \partial_\mu J_\sigma^\mu=0,
 \qquad J_N=J_++J_-,\quad J_Q=J_+-J_-.                      \tag{A6}
\]

The spatial species fluxes are Im(psi* grad psi)/m and Im(b* grad b)/M.
J_N^0 is nonnegative; J_Q is the leading microscopic signed-charge current.
For a neutral bath J_Q can vanish while J_N^0 remains positive.
For an incoherent gas these currents can instead be defined as momentum
integrals of charge-resolved distributions, provided its retained collision
kernels obey the same stoichiometric invariants. No classical condensate
phase or local thermal equilibrium follows merely from that conservation.

The rest-density and flux identities are now

\[
 \rho_{\rm rest}=mJ_N^0+\delta(n_{b+}+n_{b-}),\quad
 \partial_t\rho_{\rm rest}+\nabla\cdot j_{\rm rest}
                      =-\delta(R_++R_-),                    \tag{A7}
\]

\[
 0\leq {\rho_{\rm rest}-mJ_N^0\over\rho_{\rm rest}}
       \leq{\delta\over M}\simeq1.9994\,10^{-4}
       \quad(u_*=0.02),                                    \tag{A8}
\]

whenever the rest density is nonzero and delta>=0. Here n_sigma and
n_bsigma are the physical positive-frequency quasiparticle populations
defined by the canonical NR reduction, not uncorrected instantaneous
relativistic squared amplitudes at frequency 2m. Equation (A8) is an exact
algebraic bound within that NR population/rest-mass dictionary. It does not
establish actual relativistic source accuracy of 1.9994e-4: the additional
soft-frequency, kinetic and interaction corrections need their own bounds
and may be larger. Unlike using mJ_Q^0, this approximation includes
antiparticles. Mediator, pressure and gradient energy also distinguish it
from exact gravity.

## 2. A local dual action and the retained composition degrees of freedom

On a positive-amplitude phase chart, take
psi_sigma=sqrt(n_sigma) exp(i theta_sigma) and
b_sigma=sqrt(n_bsigma) exp[i(2theta_sigma+chi_sigma)]. Let the auxiliary
weighted number flux be bold J_sigma and source flux be ell_sigma. The
first-order phase/flux terms of the same action are

\[
 \mathcal L_1=\sum_\sigma\left[
 -q_\sigma\dot\theta_\sigma-n_{b\sigma}\dot\chi_\sigma
 -\mathbf J_\sigma\cdot\nabla\theta_\sigma
 -\ell_\sigma\cdot\nabla\chi_\sigma
 +{m|\mathbf J_\sigma-2\ell_\sigma|^2\over2n_\sigma}
 +{M|\ell_\sigma|^2\over2n_{b\sigma}}\right]-\mathcal E,
 \quad n_\sigma=q_\sigma-2n_{b\sigma}\geq0.                 \tag{A9}
\]

E includes detuning, (A3), quantum-pressure density gradients, any matched
elastic interactions, and the chosen gravitational coupling. Eliminating
the spatial fluxes returns (A2). Varying each theta yields (A6), so locally

\[
 J_\sigma^\mu={1\over2}\epsilon^{\mu\nu\rho\lambda}
                         \partial_\nu B_{\sigma\rho\lambda}.
                                                                  \tag{A10}
\]

Replacing q_sigma and bold J_sigma by (A10) in (A9), then dropping only the
justified smooth-phase boundary term, is a constructive local two-current
dual action. It retains source occupations, relative conversion phases,
relative particle/antiparticle motion and their positive domains. The
charge-even density constraint is

\[
 \rho_0=mJ_N^0=\nabla\cdot P_N,\qquad
 (P_N)_i={m\over2}\epsilon^{ijk}(B_++B_-)_{jk}.               \tag{A11}
\]

Composition and counterflow cannot generally be removed to make the
single-fluid kinetic term of main-note equation (18). A strong elastic
coflow limit and the removal of occupied sources would be additional
controlled approximations. Gravity can consistently couple to the full
leading rest density in (A7), including its detuning correction, while
rho_0 alone is the conserved reference density of (A11).

Most importantly, B_+ and B_- have independent two-form gauge freedoms.
Their sum gives P_N -> P_N+m curl(Lambda_++Lambda_-). The main note's
compact pure gauge changes W(|P_N|) at fixed J_N and still refutes its
derivation as a bare local dual-potential energy. The positive-current
rescue does not rescue W or supply a constitutive scale.

## 3. Defects of the approximation and required hierarchy

The full microscopic theory has no exact charge-even number symmetry.
The nonresonant terms removed in (A1)-(A3) carry nonzero equal-angle
number and oscillate rapidly. Virtual effects can be matched conservatively
when no hard states are populated. Real processes that release rest energy
into relativistic modes require an open soft-sector description with
explicit number and energy sinks/receivers. Examples include:

| Process | Change of full species-weighted N | Soft NR inventory when final particles are hard |
|---|---:|---:|
| X_+ + X_- -> Phi_+ + Phi_- | -2 | -4 |
| 2 Phi_+ + 2 Phi_- -> Phi_+ + Phi_- | -2 | -4 |
| X_+ + X_- -> ordinary neutral products through an allowed portal | -4 | -4 |

For the first process the two outgoing daughters each have energy M in the
center-of-mass frame and momentum sqrt(M^2-m^2), about sqrt(3)m near
threshold, so they are outside the soft envelope theory. Full weighted
counting includes those two positive daughter quanta and gives -2. A
soft-only EFT loses both incoming source weights and gives -4; conflating
these inventories would miss part of the source defect. All examples
preserve the exact signed U(1) charge. A small rate, rather than exact
forbiddance, must be demonstrated where a channel is kinematically allowed.

For general retained and hard species a state-resolved kinetic equation
gives

\[
 \partial_\mu J_{N,\rm soft}^\mu
    =S_N=\sum_a \Delta N_{a,\rm soft}\,\mathcal R_a
        +S_{\rm injection},\qquad
 \dot N_{\rm soft}+\hbox{boundary flux}=\int S_Nd^3x.         \tag{A12}
\]

The source current plus all receiver currents obey the true signed-charge
and stress-energy Ward identities. If S_N is nonzero, it cannot equal
the divergence of a smooth current of the exact form *dB: that divergence
vanishes identically. One must include a source-carrying current, singular
event/flux defects, or an explicitly open evolution; one cannot retain an
exact fixed-stock four-dimensional dual just by relabeling the density.

The controlled emergent conservation requirement on a formation/evolution
interval is a small fractional integrated number defect, for example

\[
 {1\over N_{\rm soft}(t_0)}
 \int_{t_0}^{t_0+T}dt\int d^3x\,|S_N|\ll1,
 \qquad {k\over m},{|\delta|\over m},
 {\hbox{interaction/kinetic frequencies}\over m}\ll1.        \tag{A13}
\]

For a locally equilibrated single-velocity fluid, one additionally needs
Gamma_el T>>1 while Gamma_number T<<1, with collision time shorter than
the relevant macroscopic variation time. Number-changing 4->2 loss can
be parametrically more dilute than elastic 2->2 scattering; source-pair
annihilation is itself 2->2 and is not suppressed relative to elastic
scattering merely by lowering all densities together. Its source abundance,
coupling and hard-phase-space rate must be computed. Diluteness also has
to coexist with the required occupied/coherent or kinetic state.

No such hierarchy or actual state population has been established by this
addendum. Its exact conclusion is conditional: **if the conservative NR
envelope approximation and small number-defect bound hold, a neutral bath
has a positive conserved reference-density current to leading order.**
This is a viable restricted density route beyond the main note's exact
signed-current dual, with mass corrections and defects displayed. It
leaves the separate physical-response/W and energy-receiver obligations
open. The auxiliary exact coefficient checks are recorded by the bounded
emergent-current run and do not certify (A13).

Evidence: run_emergent_001/manifest.json completed and validates against
current check_emergent.py; 15 exact coefficient/weight/ledger assertions
passed. This supplements the hand derivation, without checking a rate or
population hierarchy. Typographic clarification for the preserved main
note's equation (9): its printed `{cal A}_i=mC_i` denotes the same
\(\mathcal A_i=mC_i\) used in its equations (10), (11) and (18).
