# The existing scalar interaction permits charge demixing

2026-10-13. This provides a conditional route around the **well-mixed** assumption of the preceding annihilation calculation. The specified carrier, reduced to slowly varying particle and antiparticle condensates, has stronger intercomponent than intracomponent repulsion. A sufficiently large uniform two-condensate mixture is therefore linearly unstable to spatial demixing. This is a new application within this research lane of known binary-condensate physics, not new empirical evidence, a manufactured material, or a completed storage mechanism.

## Derivation from the action

The pinned input is the master carrier action, with cubic coupling g, source mass M>2m, Delta=M²-4m² and lambda_tot=g²/Delta+lambda_rep, lambda_rep>0. Resolve both charge signs:

\[
\Phi=\frac{\psi_+e^{-imt}+\psi_-^*e^{imt}}{\sqrt{2m}}.
\]

This adds the antiparticle component omitted from the earlier one-sign nonrelativistic treatment. Let n_±=|psi_±|². Fast-phase averaging gives

\[
\langle|\Phi|^4\rangle=\frac{n_+^2+n_-^2+4n_+n_-}{4m^2}.
\]

Eliminate X at tree level through (Box+M²)X=-g Phi², retaining the fast frequencies but neglecting slow derivatives. The same-sign terms in Phi² have frequencies ±2m and denominator Delta; its mixed term has frequency zero and denominator M². The effective interaction energy is

\[
\mathcal E_{\rm int}=\frac{g_s}{2}(n_+^2+n_-^2)+g_x n_+n_-,
\]
\[
g_s=\frac{\lambda_{\rm tot}-g^2/\Delta}{2m^2}
=\frac{\lambda_{\rm rep}}{2m^2},\qquad
g_x=\frac{\lambda_{\rm tot}-g^2/M^2}{m^2}.
\]

Consequently

\[
\boxed{d\equiv g_x-g_s=\frac{\lambda_{\rm rep}}{2m^2}
+\frac{4g^2}{M^2\Delta}>0.}
\]

The pure quartic limit already has g_x=2g_s. Charge-even forces need not select a sign externally for the many-body state to favor separation. Total charge remains zero; opposite signs occupy different regions, with interface overlap.

This is a low-frequency threshold reduction. It requires chemical potentials, kinetic energies and growth rates in energy units small compared with delta=M-2m, and energies small compared with m. It excludes populating the real source, resonant conversion near its threshold, derivative corrections and quantum loops. Keeping the exact fast-frequency denominator Delta includes contributions not retained by a leading positive-frequency-only source propagator; one should not equate it term-by-term with that truncated earlier Hamiltonian at finite delta/m.

## Linear instability and finite size

For equal uniform per-sign density n, the two Gross-Pitaevskii Bogoliubov branches obey

\[
\omega_\pm^2=\epsilon_k[\epsilon_k+2n(g_s\pm g_x)],\qquad
\epsilon_k=\frac{k^2}{2m}.
\]

The charge-difference branch grows when 0<epsilon_k<2nd. Its maximum growth rate is Gamma_max=nd, at epsilon_k=nd. In SI time divide by hbar. For a periodic box, the first allowed wave number is 2 pi/L, so a growing mode exists only when

\[
L>\frac{2\pi}{\sqrt{4mnd}}.
\]

An exactly uniform classical solution stays uniform without a perturbation; this is a linear instability, not a computed fluctuation seed or completed nonlinear trajectory.

The binary-condensate instability is established background physics: [Timmermans, cond-mat/9709301v2](https://arxiv.org/pdf/cond-mat/9709301), Eqs. (1)–(6), gives the coupled-mode criterion. [Wen et al., arXiv:1204.1256](https://arxiv.org/pdf/1204.1256) explains how confinement and kinetic energy can inhibit separation. Here the model-specific work is the carrier reduction and its coefficients; the finite-box condition explicitly retains kinetic energy.

## A conditional benchmark and competition with annihilation

Choose m=1 MeV, M=2m+5 eV, g=sqrt(0.002) eV and lambda_tot=1e-6, consistent with the preceding weak-source example. For **assumed** coherent densities n=1e12 eV³ per sign:

- g_x/g_s=2.00020002.
- Maximum linear growth is 7.5971e8 s^-1; fastest wavelength is 1.2398 micrometers.
- A periodic length must exceed 0.87666 micrometers. The tested 0.1-micrometer box is stable against this branch; 1- and 10-micrometer boxes admit growing modes.
- The uniform chemical-potential/detuning ratio is 3.00e-7, a necessary screen for eliminating the source.

The previous contact photon annihilation coefficient is a=2 C²m²/pi. In a homogeneous initial mixture, its per-particle loss rate is a n, whereas the peak separation growth is n d. Their ratio is d/a; density cancels. Growth is faster than the initial annihilation rate if

\[
|C|<\sqrt{\frac{\pi d}{2m^2}}=8.8627\times10^{-16}\ \mathrm{eV}^{-2}
\]

at this benchmark. With the explicitly arbitrary C=1e-19 eV^-2, the ratio is 7.85e7. This timescale screen does not fix C or prove survival: nonlinear separation needs many growth times, finite seeds, a sufficiently large trap and persistent condensation. Bosonic correlations, other loss channels and interface annihilation remain uncomputed.

## Research consequence and limits

The earlier dilute well-mixed steady-density result remains valid under its assumptions. It should not be treated as a ceiling on a spatially segregated condensate. Conversely, this calculation does not show that newly photon-produced particles condense or remain captured. Conservative demixing releases interaction energy into motion; it is not automatically cooling. The repulsive model does not provide a self-bound cloud, and an external container is still missing.

The next discriminating computation is a spatial two-sign evolution with annihilation and resolved interfaces, starting from a stated condensate preparation. It can test whether overlap actually decreases before substantial loss and quantify the surviving interface losses. A successful result would still leave manufacture, cooling and trapping to be established.

## Verification

Twenty-six checks pass: fast-phase averaging, source-mediated coefficient identities, an independent 4x4 Bogoliubov eigenproblem at 20 coupling/wave-number pairs, and finite-size/benchmark controls. Three Lean lemmas verify positive sums, the conditional instability sign, and the quadratic maximum-gain inequality. Their scope is algebra, not the effective-action derivation or empirical physics. The manifest pins the input action excerpt and executable calculation; no nonlinear simulation or universal storage proof is claimed.
