# Can photon pair production accumulate cold material?

2026-10-13. Result: the leading photon contact interaction has a reverse annihilation channel. In a specified dilute, well-mixed, neutral gas with continuously supplied beams, increasing the common coupling speeds both processes and leaves their steady density unchanged. This is a conditional kinetic calculation, not a universal inventory bound or an experimental result.

## Reverse process

Use the same real coefficient C in L_int=-C |phi|² F² as the preceding photon-manufacture package. The incoming unpolarized photon average for production was 2 C² s². Crossing to phi + anti-phi -> gamma + gamma removes the incoming photon average, giving a final polarization sum 8 C² s². Include the identical-photon final-state factor 1/2:

\[
\sigma_{\rm ann}=\frac{C^2s}{4\pi\beta},\qquad
\sigma_{\rm ann}v_{\rm M}=\frac{C^2s}{2\pi},\qquad v_{\rm M}=2\beta.
\]

Here v_M is the invariant-flux (Moller) relative velocity in the pair center of mass, not a claim that either particle moves faster than light. Thus, at leading nonrelativistic order,

\[
a\equiv\langle\sigma_{\rm ann}v\rangle=\frac{2C^2m^2}{\pi}.
\]

The production/annihilation cross-section ratio is beta²/2 at equal s. These normalizations use [PDG Kinematics (2024), Eq. 49.33 and its identical-final-state prescription](https://pdg.lbl.gov/2024/reviews/rpp2024-rev-kinematics.pdf), as checked in the preceding package. The source supports phase space, not the model. The amplitude itself is the stated contact truncation. Other interactions or form factors can change the result.

## Explicit kinetic assumptions

Assume two equal counterpropagating, unpolarized photon beams, each with number density n_gamma and energy E_gamma=m+K. Assume all produced pairs are captured, become an incoherent, spatially mixed nonrelativistic gas, and have negligible Bose occupation factors; emitted photons escape. Set n_phi=n_antiphi=n, initially zero. Neglect additional annihilation channels, beam depletion and matter-induced changes in the amplitude. These are strong idealizations, including an externally supplied trap and mixing mechanism; they are not a constructed apparatus.

The two labeled beam populations have relative flux 2c. Their collision rate has no extra factor 1/2. Each reaction supplies one particle of each sign. In natural units,

\[
R=2n_\gamma^2\sigma_{\rm prod},\qquad
\dot n=R-a n^2-\ell n.
\]

In SI, multiply production cross sections by (hbar c)² and the annihilation coefficient by (hbar c)² c; the production flux is 2c n_gamma² sigma_SI. The one-body loss rate ell is nonnegative. It represents escape or other removal equally for both species; extraction into a separate product reservoir would require its own accounting.

With ell=0 and C nonzero,

\[
n_{\rm eq}=\sqrt{R/a}=n_\gamma\frac{E_\gamma}{m}\sqrt{\frac{\beta}{2}},\qquad
n(t)=n_{\rm eq}\tanh(\sqrt{Ra}\,t).
\]

The formula uses the leading cold annihilation coefficient and retains the exact production threshold. Relative kinetic corrections to a are omitted. The limit C=0 is singular for the equilibrium interpretation: with zero source and zero sink the empty state remains empty. For small C, the equilibrium may take far longer than any useful time to approach.

For ell>0 the positive steady root is

\[
n_+=\frac{2R}{\sqrt{\ell^2+4aR}+\ell}\le\sqrt{R/a}.
\]

Coupling cancellation applies to the ell=0 equilibrium of this model. With fixed nonzero ell, changing C can change the steady density, which remains below that ideal equilibrium. Time-dependent beams/couplings, separation, quantum coherence, stimulated processes and dense phases are outside this result.

## Energy-density diagnostic

Let rho=2m n (with consistent SI mass conversion) include both species. The ideal equilibrium rest-energy density relative to total beam energy density is

\[
\frac{u_{\rm matter}}{u_{\rm beams}}=\sqrt{\beta/2},\qquad
I_{\rm each}=\frac{\rho c^3}{\sqrt{2\beta}}.
\]

This is the local beam throughput needed by the stipulated steady model, not absorbed power or a fundamental minimum over every production strategy. At m=1 MeV, K=1 eV per product, and a deliberately low total material density rho=1e-9 kg/m³, it gives I_each=5.0663e17 W/m². The rough matter occupation diagnostic n(2 pi hbar/p)³ is 1.89e-7, so this example does not already fail that necessary dilute-gas screen. It does not verify the assumed mixing, distribution width, photon occupation, field control or achievable beams.

The same diagnostic at K=1 micro-eV gives occupation about 189; that table row is outside the nondegenerate approximation and is retained explicitly as a failed applicability screen. It is not an allowed cold operating point of this model. No extrapolation to the earlier 3.31e8 kg/m³ condensate is justified.

For the K=1 eV illustration, arbitrary coefficients C=1e-25, 1e-22 and 1e-19 eV^-2 give 90%-filling times 7.063e22, 7.063e16 and 7.063e10 seconds respectively, at the same ideal steady density. These are scaling examples, not measured or matched couplings. Their small C s values screen the single contact amplitude only; they do not validate an ultraviolet completion or the complete background-field expansion.

## What would evade this bottleneck?

A viable proposal must change a stated assumption, then calculate the consequence. Possibilities include physically separating the two charge signs, converting newly produced particles into a distinct protected storage state, or controlling production and storage with different interactions. The existing charge-even polarizability does not itself provide sign selection. None of these possibilities has been implemented here. They also need a source of trapping or dissipation to establish a localized cold distribution.

The next physical question is therefore whether an explicit extension supplies a production interaction and a storage mechanism whose losses are independently controlled. Replacing the common C with a larger arbitrary number does not answer that question.

## Verification scope

Sixteen symbolic/numerical checks pass, including the reverse-process normalization, coupling cancellation, four loss cases compared with analytic ODE solutions, and SI energy bookkeeping. Three Lean lemmas verify common-factor cancellation, the conditional steady-state loss bound and paired charge-rate cancellation. Lean certifies these algebraic statements under their hypotheses; it does not certify the scattering derivation, kinetic approximation, field existence or a device. See `run/manifest.json` and `lean_record.json` for reproducibility.
