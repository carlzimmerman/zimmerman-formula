# Sourced vacuum and the future event horizon have opposite trends

Claim scope: spatially flat, expanding Einstein-Friedmann spacetime containing positive pressureless matter (baryons plus the primordial cold component) and a vacuum component with pressure minus its energy density. Energy may transfer from matter to vacuum, with S=dot(rho_V)>=0. Total stress-energy is conserved. Assume expansion continues and the future event-horizon integral exists. These are the homogeneous sourced-vacuum comparison assumptions, not a theorem about every cold-medium or modified-gravity completion.

Write mass densities in SI. Conservation and Friedmann's equations give

\[
\dot\rho_m+3H\rho_m=-S,\qquad\dot\rho_V=S,
\quad H^2=\frac{8\pi G}{3}(\rho_m+\rho_V),
\quad\dot H=-4\pi G\rho_m\le0.
\]

Thus H is nonincreasing, including during vacuum production. For any finite time t, express the physical event-horizon radius as

\[
R_E(t)=c\,a(t)\int_t^\infty\frac{dt'}{a(t')}
=c\int_0^\infty\exp\left[-\int_0^sH(t+u)du\right]ds.
\]

Since H(t+u)<=H(t), the integrand is at least exp[-H(t)s]. Therefore

\[
R_E(t)\ge c/H(t),\qquad \dot R_E=HR_E-c\ge0.
\]

The inequalities are strict if H decreases over a future interval, as it does with positive primordial pressureless cold matter in this comparison. An infinite horizon is excluded by the stated hypothesis; in that case an inverse-horizon force scale vanishes and is not the proposed positive scale.

Now compare two proposed laws with positive constant coefficients:

\[
a_\rho=\kappa c\sqrt{G\rho_V},\qquad
a_E=\beta c^2/R_E.
\]

For rho_V>0 their logarithmic derivatives are

\[
\frac{\dot a_\rho}{a_\rho}=\frac{S}{2\rho_V}\ge0,
\qquad
\frac{\dot a_E}{a_E}=\frac{c}{R_E}-H\le0.
\]

They cannot be the same function on an interval with strict production or strict horizon growth. Matching their values at one epoch is insufficient. With positive pressureless matter the event-horizon trend is strict, even when S=0. The flat-space apparent/Hubble horizon R_A=c/H likewise grows, so a scale proportional to c²/R_A=cH also has the opposite trend to growing vacuum density.

The auxiliary vacuum curvature length

\[
L_V=c/\sqrt{8\pi G\rho_V/3}
\]

instead SHRINKS when vacuum is produced. Consequently a_rho=alpha c²/L_V, alpha=kappa sqrt(3/(8pi)), remains an algebraic identity. What fails is identifying L_V with the actual event horizon in the evolving matter-filled spacetime. In an asymptotic de Sitter state with S->0 and matter dilution, all three lengths approach the same value and the familiar geometric dictionary is recovered.

This is a geometric mechanism discriminator under explicit conservation assumptions. It does not reject the density law, prove the horizon law, derive kappa, select a microscopic vacuum source, or address non-Einstein backgrounds or additional negative-pressure/NEC-violating matter. Numerical histories are checks and examples; the inequalities above are the analytical argument.
