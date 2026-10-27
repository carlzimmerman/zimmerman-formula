# Fresh bounded exchange reconstruction

20 October 2026. Reviewer: sibling agent `/root/existing_scalar_attraction`
in the same session and model family. The reviewer was given the raw
`occupied_landscape/LANDSCAPE.md:490-524` formulas and asked to reconstruct
the two-static-occupation Hamiltonian, self shifts, pair double difference,
and three-dimensional point-packet Fourier coefficient. The reviewer was
also asked to treat the closed density change `rho_t-rho_f`. The present
proof and its proposed coefficient were not supplied in that request.

**Normalized claim and verdict: proved as written for the static regulated
harmonic bath.** This is a fresh derivation of RESULT (2)-(9), not a review
of physical formation, same-species projection, memory closure, or the
entire report.

The reviewer reconstructed

\[
 \lambda_{i q}=\gamma\sqrt{n_0\epsilon_q/(V E_q)}\rho_i(-q),\qquad
 \delta E=-\sum_q{|n_1\lambda_{1q}+n_2\lambda_{2q}|^2\over E_q}.
\]

Subtracting the four sectors leaves

\[
 U_{11}-U_{10}-U_{01}+U_{00}
 =-{2\gamma^2n_0\over V}\sum_q{\epsilon_q\over E_q^2}
                  \operatorname{Re}[\rho_1(q)^*\rho_2(q)].
\]

With all standard `q` modes counted once and
`E_q^2=epsilon_q(epsilon_q+2g2 n0)`, the continuum Fourier integral gives

\[
 U(R)=-{m\gamma^2n_0\over\pi R}e^{-\kappa_B R},\qquad
 \kappa_B^2=4mg_2n_0,\quad R>0.
\]

Thus `gamma=2g2` produces coefficient `-4m g2^2 n0/(pi R)`. The factor
two is the cross term of the square, rather than a doubled momentum count.
Point self shifts are ultraviolet divergent, while the nonzero-separation
cross shift is finite. The reviewer required consistently regulated self
energies and a supported stable bath.

For closed conversion, replace both densities by the signed differences
`Delta rho_i=rho_ti-rho_fi`. The reviewer confirmed that the cross sign is
not fixed; equal conserved charge gives `Delta rho_i(0)=0`, and a zero
density difference gives zero coupling. A spatial added-particle attraction
does not by itself establish conversion memory. No scientific numerical
control was run for this audit; all checks are direct algebra and Fourier
normalization.

Coverage: factor, sign formula, Fourier coefficient/range, self subtraction,
and closed-conversion dictionary. No all-orders bath, gravity, lifetime,
or empirical pass was reviewed. No original input was edited.
