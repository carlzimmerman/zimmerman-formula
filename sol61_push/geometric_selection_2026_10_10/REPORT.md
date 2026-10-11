# Geometric selection: the boundary must do more than normalize the potential

2026-10-10; checkpoint from `0c28ef639`. Target remains a0=(c/2)sqrt(G rho_DE), equivalently Lambda c^4/a0^2=32 pi on the repository's vacuum-density convention. No coefficient derivation or cold-component identification is established here.

**Result:** regularity, a cosmological length, a convex static field energy, and an outer potential condition admit a continuous family of response strengths. This is an explicit counterexample to those conditions being sufficient. It is not a theorem against full relativistic matching, and the ball boundary below is not a cosmological horizon solution.

## A regular counterfamily

Fix L, a nonnegative smooth spherical baryon density of compact support inside L, and a dimensionless epsilon in (0,1). For **every** gamma>0 set a=c²/(gamma L) and

\[
\mu_\epsilon(g)=\sqrt{\frac{g^2+\epsilon^2a^2}{g^2+a^2}},\qquad
W(g)=\int_0^g t\mu_\epsilon(t)\,dt,\qquad
E[\Phi]=\int_{B_L}\left[\frac{W(|\nabla\Phi|)}{4\pi G}+\rho_b\Phi\right]d^3x.
\]

Variation at fixed boundary potential gives div(mu grad Phi)=4 pi G rho_b. The gradient-energy Hessian has tangential eigenvalue mu and radial eigenvalue mu+g mu'. Both are between epsilon and 2. Hence the static operator is uniformly elliptic and the gradient energy strictly convex. These are static properties, not relativistic stability or causal-propagation results.

Writing y=GM_b(<r)/r², regularity removes the radial flux integration constant. The exact positive solution is

\[
\mu_\epsilon(g)g=y,\qquad
g^2=\frac{y^2-\epsilon^2a^2+
\sqrt{(y^2-\epsilon^2a^2)^2+4a^2y^2}}{2},\qquad
\Phi(r)=-\int_r^L g(s)\,ds.
\]

For a smooth filled center, y=kr+O(r³) and g=y/epsilon+O(y³); the radial potential is smooth there. Outside the source, the high-acceleration limit is g≈y. In the intermediate window epsilon a≪g≪a, g²≈ay, giving approximately flat circular speeds with V^4≈GM_b a. The residual epsilon changes the extreme low-acceleration behavior; exact deep scaling down to g=0 is not claimed.

For all gamma the same outer value Phi(L)=0 holds. It fixes the additive potential constant, not a. Now identify L=sqrt(3/Lambda), with rho_DE=Lambda c²/(8 pi G). The intermediate-response coefficient is

\[
\kappa=\frac{a}{c\sqrt{G\rho_{DE}}}
=\frac{\sqrt{8\pi/3}}{\gamma},\qquad
\frac{\Lambda c^4}{a^2}=3\gamma^2.
\]

Thus gamma=sqrt(32 pi/3) gives the requested half, while neighboring gamma give other coefficients under the same regularity and boundary requirements. Selecting that gamma would insert the answer. This is a family of different constitutive actions; it does **not** show that a fully fixed covariant action cannot select a solution parameter.

## What survives of the geometric proposal

The geometric-mean relation r_M²=gamma (GM_b/c²)L follows once a is declared. It does not supply a new selection equation. Ordinary matching of a scalar potential is insufficient; full source-to-cosmology matching remains a different unresolved problem. The earlier [clock calculations](../BOUNDARY_AND_COLD_STATE_2026-10-06.md) already distinguish finite-radius normalization, growing-mode cancellation and cosmological boundary conditions.

There is a known geometric reason for a cubic gradient term: in three spatial dimensions sqrt(h)|D Phi|³ is invariant under h_ij→Omega²h_ij for a weight-zero potential. Its spherical flux produces the square-root mass response. Multiplying that term by an arbitrary constant preserves the invariance. This symmetry fixes an exponent, not its amplitude. This is established mathematics, not new physics: [Milgrom's conformal Poisson analysis](https://arxiv.org/abs/gr-qc/9705003), following [Bekenstein–Milgrom's variational formulation](https://adsabs.harvard.edu/pdf/1984ApJ...286....7B). It is used here as a counterexample class, not as an observational yardstick or replacement for the project's real cold component. The calculation does not reproduce the project's exact exponential kernel.

**Necessary next selection test:** specify the proposed covariant action and its source/clock normalization; vary its vacuum term and response normalization independently. A symmetry, constraint or actual global solvability condition must forbid the independent variation or predict the same operational kappa despite it. Otherwise matching merely selects integration constants while the theory still fits the response strength. Any such candidate also needs regular sources and healthy perturbations; the previous clock branch's problems cannot be cured by choosing the desired coefficient.

## Evidence and resource scope

The proof above constructs the radial solution for arbitrary positive gamma. `check.py` checks its algebraic flux, ellipticity, center limit and asymptotic response for three coefficients, including the target and two alternatives, using a fixed compact polynomial source. All 20 assertions passed; maximum relative flux residual was 4.45e-16, and the manifest validates. The finite checks do not prove the universal statement; the displayed construction does. An independent reader derived and checked the counterfamily. The source/cosmology identification is a stipulated length dictionary; no relativistic field equations were solved.

This checkpoint narrows my earlier global-matching suggestion: geometry may still supply an additional selection law, but a cosmological boundary location and smoothness alone do not. No expensive simulation was launched and no concurrent research lane was modified.
