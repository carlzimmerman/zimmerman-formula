# A smooth charged vacuum edge leaves the constructed causal domain

MC-BOUNDARY-001, 15 October 2026. Direct conditional obstruction for the unchanged current-frame constitutive family. This continues the finite-source local-gate result; it does not exclude every possible gauge medium, sharp boundary or vacuum completion.

## Hypotheses

Keep the electric law and local principal family in [the mode proof](../modes/PROOF.md): D=E/(1+E/D0), D0>0, x=D/D0 in (0,1), p=(1-x)² and t=1-x. Constituents are co-moving at the background point, have positive h_a, sound squares in [0,1), no entrainment, and positive mass-frame weights w_a with sum one. The criterion for the constructed magnetic response to have its causal window is

\[
 h_*>h_{\rm crit}(x),\qquad
 h_*^{-1}=\sum_a\frac{w_a^2}{h_a(1-s_a^2)},\qquad
 h_{\rm crit}=D_0^2\frac{x^3}{(1-x)^2}.
\]

Consider the interior limit r -> R- of a smooth finite-radius boundary. Assume the total included enthalpy tends to zero, sum h_a -> 0, while the electric displacement has a finite nonzero limit D_b with 0<D_b<D0. This applies to a finite, nonscreened spherical charge inventory with continuous D at R and no uncounted surface charge: D_b=Q_enc/(4 pi R²)>0. The weights may vary or approach zero; an absent species is removed before division by its inertia.

## Obstruction

Set a_a=h_a(1-s_a²)>0. Weighted Cauchy gives

\[
 1=\left(\sum_aw_a\right)^2
 \le\left(\sum_a\frac{w_a^2}{a_a}\right)\sum_aa_a,
 \qquad 0<h_*\le\sum_aa_a\le\sum_ah_a.
\]

Therefore h* -> 0. By continuity, hcrit(x) -> hcrit(D_b/D0)>0. Hence h*/hcrit -> 0, and a one-sided neighborhood inside R necessarily fails h*>hcrit. The failure occurs where density is still positive, before asking how to define a frame exactly at zero density.

For the constructed response class 0<beta<t, the perpendicular light-cone Schur function is

\[
 f(\beta)=p-\beta-
 \frac{E^2(t-\beta)^2}{h_*+E^2(t-\beta)},\qquad
 f'(\beta)=-\frac{h_*^2}{[h_*+E^2(t-\beta)]^2}<0.
\]

When h*<hcrit, f(0)<0, so every beta in that class has a supermetric perpendicular propagating principal root. This is the local-gate conclusion proved in the pinned mode analysis. It is not a claim that every alternative constitutive action has a ghost or cannot have an interface. Holding an undepleted finite charge while smoothly removing all the material support cannot remain in this particular healthy branch.

## Quantified alternatives

1. **Screen the net field.** If x -> 0 together with enthalpy, this obstruction no longer follows. With distance delta=R-r, h*~A delta^a and x~B delta^b, A,B>0, b>0,

   \[
   {h_*\over h_{\rm crit}}\sim
   {A\over D_0^2B^3}\delta^{a-3b}.
   \]

   Thus a<3b passes the asymptotic local threshold, a>3b fails it, and equality depends on the coefficient. These are asymptotic gate conditions only. Same-sign nonzero total charge cannot screen itself to zero outside a closed spherical inventory; opposite charges, another source or flux must be counted. A compensated outer shell changes the static force balance and needs its own pressure/flow and material equations.
2. **Retain ambient material support.** If the included enthalpy remains positive outside, the premise sum h_a -> 0 fails. Its species, mass, charge and stress must enter the same dynamics; it is no longer a compact material halo in empty vacuum. Adding neutral matter to the constitutive frame can also give that matter nonminimal constitutive interactions.
3. **Change the phase or boundary action.** A new electric/density response, independent regular support field, or sharp interface is a different candidate. A sharp jump requires actual surface matching, stress and mode conditions. An assigned exterior force law, such as the remnant benchmark, does not derive those conditions.

For example, if a screened boundary has total material density proportional to delta^a with a>0 and net enclosed charge proportional to delta^(a+1), then h*/hcrit can diverge rather than vanish, provided h* has that same material scaling. The example identifies a possible scaling route, not a derived screening shell or a regular off-shell vacuum action. A simultaneous limit along one profile cannot establish well-posedness for nearby independent field/current perturbations.

## Consequence for this checkpoint

The extended-source local-gate witness addresses an inner/source-scale problem. It cannot be truncated with a smooth nonscreened taper and keep this same healthy constitutive branch to vacuum. The next physical candidate must choose and derive one of the alternatives above, then solve the full source and constraint problem. The core, finite supply, live conversion/receiver history, metric and observational obligations remain open.

The universal implication above is a continuity and Cauchy argument. [The exact check](check_boundary.py) verifies its two-species normalization, the Schur derivative, and the power-law identity with four exact limiting controls; finite examples are not its proof. [The recorded run](run_v1/manifest.json) pins this note, the code and the parent mode proof.
