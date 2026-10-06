# Independent retarded-curvature review

**Initial verdict: correct only after a general-dimensional force-normalization correction.** The exact-initial-de-Sitter theorem, local differential representation, full-FRW evolution equations and four-dimensional local-force/vacuum conclusion are correct as stated. The displayed general-dimensional response factor is relative to the **bare GR force coefficient**, not the Einstein–Hilbert action parameter except in four dimensions. This correction is a naming/measurement dictionary obligation, not a change to the derived response factor.

Read-only inputs and exact hashes are in `retarded_review_inputs.json`. I read the report, script, direct final output and retained exact-version Deser–Woodard/Deffayet–Woodard primary text. No peer script was executed and no peer artifacts were changed. Standard evidence records were not yet present at initial review; numerical rows below are inspected output, not independently rerun results.

## 1. Reconstructed equations and exact obstruction

From `L_local=F R+grad X dot grad Y`, variation of `Y` gives `Box X=R`; variation of `X` gives `Box Y=R f'(X)`. The metric variation is

`F G+(g Box-nabla nabla)F+grad_(mu X grad_nu)Y-(g/2)grad X dot grad Y=kappa T`.

Using `Box U=-Uddot-nH Udot`, `G00=n(n-1)H²/2`, and `Gii/a²=-(n-1)Hdot-n(n-1)H²/2` reproduces the report's two metric components, including the **positive half-product in both components**. This agrees with the retained primary Deffayet–Woodard equations (10)–(17). The causal prescription/localized-theory distinction is appropriately explicit: arbitrary homogeneous auxiliary modes would define another model, while a naive retarded single-history action variation need not produce these causal equations.

For exact expanding de Sitter, direct integration of `Xddot+nH Xdot=-n(n+1)H²` with zero data gives the reported secular `X` and strictly negative `Xdot` at every positive time. A constant scalar cannot be assigned a nonzero Box eigenvalue to replace that response.

At fixed vacuum density, subtract the initial Friedmann constraint and eliminate `Xdot Ydot` using the spatial-plus-time equation. The resulting equation is exactly

`Fddot+(2n-1)H Fdot+n(n-1)H²(F-F0)=0`.

Its roots are `-nH` and `-(n-1)H`; zero displacement and velocity give `F=F0` by ordinary linear ODE uniqueness. The sum equation then forces `Xdot Ydot=0`; since `Xdot!=0` for positive times, `Ydot=0`. Retarded `Y(0)=0` makes `Y=0`, hence `f(X)=f(0)` on the entire visited negative branch. The report correctly allows a globally nonconstant smooth function supported only at unvisited positive `X`, different prehistories and asymptotic rather than initially exact de Sitter. Analytic continuation is invoked only under a real-analytic connected-domain assumption.

## 2. Saturating escape and numerical interpretation

For arbitrary evolving `H`, the auxiliary equations imply

`Fddot=f''Xdot²-nH Fdot-2f'R`.

Substituting this into the metric sum equation gives the report's denominator `(n-1)F-4n f'` and numerator, including the matter term `-A_n m` in its chosen `kappa rho_v=A_n` units. The initial Friedmann constraint indeed gives `H(0)=sqrt(1+m0)` when `f(0)=0` and auxiliaries have zero data. The pressureless matter equation is `mdot=-nH m`. Thus the evolution is not an independently imposed constant-H response.

The inspected final output reproduces the printed four-dimensional values: vacuum history `H=.7989247485243549`, `F=1.5667086842926299`, and matter history `H=.8043239622915728`, `F=1.545745480453669`. Their relative Friedmann residual maxima are `6.31024e-11` and `1.46654e-10`. These are consistent numerical controls for the equations, not an all-history convergence proof. Positive `F` and trace denominator are background regularity, not covariant or nonlocal perturbative stability.

## 3. Local force derivation and correction

With metric `ds²=-(1+2Psi)dt²+(1-2Phi)dx²`, the frozen subhorizon trace is

`[-(n-1)Fbar/2+2n pbar] delta R=-kappa delta rho`.

It follows that `delta R=2kappa delta rho/Dbar`, `lap delta F=2pbar delta R`. The independent time component and traceless spatial condition are

`Fbar(n-1)lap Phi-lap delta F=kappa delta rho`,

`Fbar[(n-2)Phi-Psi]=delta F`.

These give the test-force coefficient, divided by the **bare GR Poisson coefficient** `kappa(n-2)/(n-1)`, as

`Q=(1/Fbar)[1-4pbar/((n-2)Dbar)]`.

This matches the script. However if `G_b` is defined by the action `kappa=8piG_b`, the physically measured bare radial-force coefficient is

`G_N,b=8pi(n-2)G_b/[(n-1)Omega_(n-1)]`.

Therefore the correct operational label is `G_N,dyn/G_N,b=Q`. Equivalently `G_N,dyn/G_b=[8pi(n-2)/((n-1)Omega_(n-1))]Q`. The initially reviewed text instead labeled `Q` as `G_dyn/G_b` for all `n>=3`. That identification is correct at `n=3` and requires this prefactor in other dimensions. Ratios to action-equivalent couplings can also be used, but must be named distinctly from measured force coefficients. The general vacuum comparison must use the same bare-force convention.

In four dimensions the formula reduces to `(Fbar-8pbar)/[Fbar(Fbar-6pbar)]`; the lensing combination is `1/Fbar`, and the potential ratio is `(Fbar-4pbar)/(Fbar-8pbar)`. These agree independently. On the numerical late branch, `pbar` vanishes while `Fbar` freezes; the locally measured force coupling and the vacuum-curvature coefficient both renormalize by `1/F_infinity`. Expressing the vacuum relation in measured local units therefore removes the apparent selective suppression. Its static near-zone response remains linear in source mass and supplies no MOND square-root source law.

The derivation needs frozen background, subhorizon quasistatic response after transients settle, nonsingular coefficients and `n>=3` for a nonzero bare dust-force coefficient. The report explicitly states these restrictions.

**Acceptance condition:** repair the general-dimensional operational coupling labels or prefactor. Subject to that repair, the exact theorem and restricted response/escape conclusions are accepted. The missing physical implication remains a healthy causal nonlinear model and boundary history delivering selective vacuum suppression relative to measured local gravity together with the actual MOND source law and acceleration scale; this report does not provide it.

## Repair acceptance and added late-segment result

The current report and script now distinguish `G_EH,b` from `G_N,b` and state the sphere-flux conversion explicitly. The general local factor is correctly labeled `G_N,dyn/G_N,b`. Repaired hashes are appended separately in `retarded_review_inputs.json`; the earlier hashes and initial correction verdict remain preserved. **The corrected report is accepted within its stated scope.** Fresh execution provenance must be evaluated on its repaired script, not inferred from the initially inspected direct output.

I also independently checked its added indefinitely sustained exact-de-Sitter segment theorem. With arbitrary finite inherited auxiliary data, the same metric ODE gives `F=F_Lambda+C_n exp(-nH tau)+C_(n-1) exp(-(n-1)H tau)`. Independently `Xdot` tends to the nonzero constant `-(n+1)H`. The vacuum sum forces `Ydot=(Fddot-HFdot)/Xdot` to tend to zero; `Fdot=f' Xdot+Ydot` then gives `f'->0`. Thus relative local-force and Einstein-prefactor renormalizations both tend to `1/F_Lambda`. Translating the action coefficient to force units gives precisely `H²=2Omega_(n-1)G_N,dyn,infinity rho_v/[n(n-2)]`. This is a necessary late relation on an exact segment, not proof that every asymptotically de Sitter trajectory obeys the needed decay conditions.

The added frozen diagnostic is also correct: for `Q=Fbar G_N,dyn/G_N,b`, `cap=(n-1)²/[n(n-2)]`, direct subtraction gives `cap-Q=(n-1)Fbar/[n(n-2)Dbar]>0` when `Fbar,Dbar>0`. If `Q>0`, reciprocation gives `1/Q>n(n-2)/(n-1)²`, including `3/4` at `n=3`. This compares instantaneous prefactor and force renormalizations, not the evolving cosmological vacuum response. The corrected report expressly retains that distinction.
