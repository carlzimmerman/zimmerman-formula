# Pump backreaction: stable excitation below a symmetry-breaking threshold

2026-10-13. Previous turn was progress: it derived and published an explicit optical preparation term. This continuation tests backreaction within a three-mode approximation. It does not replace the full spatial Maxwell–matter problem or complete the cold-energy objective.

## Closed mode equations

Retain two counterpropagating photon modes a and c, and the zero-momentum gapped matter mode b. The resonant rotating-wave interaction is

\[
H_{\rm int}=h(b^*ac+ba^*c^*).
\]

All mode amplitudes have occupation |amplitude|². With equal real incident drive amplitudes E, photon number-loss rate kappa and matter number-loss rate gamma,

\[
\dot a=-\kappa a/2-ihbc^*+E,\quad
\dot c=-\kappa c/2-ihba^*+E,\quad
\dot b=-\gamma b/2-ihac.
\]

The coherent conversion is retained in every equation, including depletion and stimulated reverse conversion. Losses are Markov approximations. Gamma here refers to loss into modes outside the three-mode system; explicitly retained optical modes must not be counted again as an independent vacuum decay bath. The physical estimates use the preceding matter width plus its negligible vacuum radiative width as an approximation to unretained losses.

This is a finite-mode model with externally imposed losses and drives. It assumes exact resonance, homogeneous matter, a fixed condensate and a constant coupling. No optical resonator or boundary conditions have been constructed for the hypothetical material.

## Stationary branches and instability

The equal-beam solution has a=c=A real and

\[
b=-iB,\quad B=2hA^2/\gamma,\quad
E=\kappa A/2+2h^2A^3/\gamma.
\]

For a real antisymmetric perturbation delta a=-delta c, linearization gives the exact growth exponent

\[
\lambda_{\rm asym}=-\kappa/2+2h^2A^2/\gamma.
\]

Therefore the equal-beam state loses stability when

\[
A^2>A_{\rm crit}^2=\frac{\kappa\gamma}{4h^2},\qquad
E_{\rm crit}=\kappa A_{\rm crit}.
\]

The resulting unequal-beam stationary branches satisfy

\[
ac=\frac{\kappa\gamma}{4h^2},\quad
a+c=\frac{2E}{\kappa},\quad
b=-i\frac{\kappa}{2h},
\]

or

\[
a,c=\frac E\kappa\mathbin{\pm}
\sqrt{(E/\kappa)^2-\frac{\kappa\gamma}{4h^2}}.
\]

They exist above threshold. The matter occupation on these branches is **clamped at kappa²/(4h²)** instead of growing indefinitely with pump power. Swapping a and c gives the symmetry partner. This is a conditional prediction of these equations, not a claimed novel physical effect or evidence that the repository's proposed material exists.

The full six-real-variable Jacobian was tested at 18 parameter combinations: gamma/kappa=0.1, 1, 10 and E/Ecrit=0.1, 0.5, 0.9, 1.1, 2, 5. The symmetric solutions were stable below threshold and unstable above; the unequal solutions were stable at all nine tested above-threshold points. This is a bounded stability check, not a proof across every detuning and loss ratio. No conclusion about unretained spatial modes follows.

A nonlinear integration at gamma=kappa=h=1 and E=1 starts near the unstable symmetric state, with an antisymmetric seed of 10⁻⁴. It approaches one unequal branch with final amplitude-vector error below 7 × 10⁻¹¹. The equal solution would persist in exact arithmetic without a symmetry-breaking perturbation.

## Energy balance

The interaction conserves Q=|a|²+|c|²+2|b|². With the stipulated pump and losses,

\[
\dot Q=2E\operatorname{Re}(a+c)-\kappa(|a|^2+|c|^2)-2\gamma|b|^2.
\]

At resonance energy equals omega_p Q. The observed matter population and optical output are powered by the external drive. The numerical trajectory satisfies this balance to approximately 6.4 × 10⁻¹⁶ in the dimensionless variables. Asymmetric output does not constitute energy amplification without an input energy source.

## Link to the earlier portal, and physical limits

Matching the coherent drive to the normalized photon amplitudes gives

\[
h=\frac{gV_g\omega_p}{\sqrt{2MV}},\quad
n_{s,\rm crit}=\frac{\kappa^2M}{2(gV_g)^2\omega_p^2},\quad
u_{{\rm beam},\rm crit}=\frac{\kappa\gamma M}{2(gV_g)^2\omega_p}.
\]

Here V is the mode volume; Vg is the dimensionless matter eigenvector vertex, not a volume. Rates in these expressions are in natural energy units. The volume cancels from the critical densities. Intracavity intensity is c times each beam's energy density; it is not the external input intensity, which additionally depends on coupling geometry.

For the preceding dense benchmark, assigning kappa=c/(1 cm) as a rough transit-loss scale gives a critical per-beam intensity about **9.40 × 10¹⁷ W/m²** and a critical excited fraction about **0.0107**. This assignment is only a comparison: a traveling-wave continuum is not equivalent to a three-mode cavity. Even this percent-level excitation can shift a very narrow resonance through nonlinear effects omitted here.

Assigning kappa=10⁶ s⁻¹ instead gives a threshold around **3.13 × 10¹³ W/m²** and an excited fraction around **1.19 × 10⁻¹¹**. Lower optical loss changes the threshold substantially. There is no demonstrated resonator at either loss rate in this hypothetical medium. The calculation therefore supplies a conditional mode-stability criterion, not an engineered operating point.

At the centimeter transit-loss estimate, the earlier diagnostic fractions up to 10⁻⁶ lie below this particular exchange-symmetry threshold. This rules out that specific instability as an immediate contradiction in the reduced model; it does not establish absence of all stimulated channels, static density modulation, thermal effects, finite-size detuning or sideband instabilities.

## Research status

A self-consistent driven three-mode state is now available below threshold, and its first exchange-symmetry instability has been identified. This advances the conditional optical-preparation route. The full goal remains incomplete: the photon portal is hypothetical, the dense condensate is unprepared and unconfined, and gravity has not been derived from this mode model.

The next discriminating calculation is the spatial density response and frequency shift caused by the standing-wave drive. Even a shift much smaller than the optical frequency may exceed the approximately 26 Hz matter linewidth from the previous benchmark. A stable few-mode solution alone does not discharge that requirement.

Scripts, copied input widths, contract and run manifest preserve the actual finite computation. The new nonlinear branch and stability results are numerically checked and analytically self-reviewed, not newly Lean-certified. Prior Lean identities do not certify this truncation or its physical admissibility.
