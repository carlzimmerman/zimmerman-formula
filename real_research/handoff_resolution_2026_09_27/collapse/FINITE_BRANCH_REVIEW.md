# Independent audit of the finite-density branch

Read-only review of `constitutive/FINITE_DENSITY_ACTION.md` and `finite_branch_check.py`. The stated all-density-on-the-supplied-branch claim is correct: for fixed positive Pc,V,ye and every finite y≥ye, the strict boundary inequality c²>V ye sqrt(1+ye)/(ye+2) implies epsilon>P≥0, positive enthalpy and 0<c_s²<c². This is an analytic conditional result, not a sampled numerical inference. It does not select the branch or establish a stable self-gravitating object.

## Exact verification

Let t=sqrt(1+y). Then rho_y=(Pc/V)(y+2)/(2t³)>0 and F'(y)=(y+2)/(2yt)>0. Differentiating the supplied epsilon gives

    h=epsilon_rho=c²+V[F(y)−F(ye)+t],
    rho h−epsilon=Pc(y−ye),
    Q=P_rho=2V t³/(y+2)>0.

Subtracting yields g=h−Q=c²+V[F(y)−F(ye)−yt/(y+2)]. Direct differentiation gives g_y=4Vt/[y(y+2)²]>0. Its minimum on the closed branch is therefore the edge value g(ye)=c²−V ye sqrt(1+ye)/(ye+2). The strict hypothesis makes h>Q>0 on the entire branch. With P and epsilon both energy densities in SI, c_s²/c²=Q/h, so the claimed strict causal sound-speed inequality follows. The ratio approaches unity at large density; the proof gives strict subluminality at each finite y, not a uniform gap below c across an unbounded branch.

Since F is increasing, epsilon≥rho c²+Pc ye>0 and P≥0. At the edge epsilon−P=rho_e c²+Pc ye>0. Its rho derivative equals h−Q>0, proving epsilon>P at every greater density. Consequently epsilon≥|P| and epsilon+P>0: the perfect-fluid dominant, weak and null conditions follow under the stated hypotheses. No unproved EOS extrapolation to 0<rho<rho_e is used.

The parent's executable checks the exact identities needed by this reasoning. Its mutation removes Pc ye from energy, which changes the resulting pressure from Pc(y−ye) to Pc y: finite-pressure, zero-edge-pressure and edge-energy checks fail meaningfully, while derivative identities can remain true. Those surviving derivative identities do not accidentally certify the wrong boundary pressure.

## Action and equilibrium scope

The previous independent review's current-action variation remains valid for this epsilon(rho,s): rho epsilon_rho−epsilon is the pressure, with contravariant J^mu held fixed in metric variation. At fixed material state V(s),ye(s), both normalization changes are legitimate constitutive functions. They are supplied functions, not consequences of the current equation. The Pc ye contribution is a physical vacuum-form term inside the declared material domain; treating the exterior as separately specified vacuum requires an interface/domain prescription. The finite density jump is compatible with zero pressure at a static perfect-fluid surface, but that fact does not provide a moving-boundary variational formulation, phase transition, or stable phase coexistence.

The paragraph beginning **“In the point-baryon equilibrium” must be read as Newtonian Euler–Poisson equilibrium**. Substituting y=G Mb/(a0 r²) and V=sqrt(G Mb a0)/2 reproduces the earlier pressure gradient, rest-mass density and P2 enclosed mass in that regime. The exact Einstein equations instead gravitate epsilon/c² and pressure and require a TOV/static-metric solution. The same P2 radial profile has not been shown to solve that system. Weak-field recovery additionally needs small compactness and internal/pressure energy compared with rho c²; these conditions cannot hold uniformly to the singular point-mass center as y→infinity. Exterior mass retention is correct Newtonian source accounting; an exact relativistic exterior would use the matched gravitational mass, not automatically the integral of rest density alone.

These are scope qualifications, not failures of the constitutive theorem. The document already rejects formation selection, interface well-posedness and gravitational stability claims. Explicitly labeling the quoted equilibrium paragraph Newtonian would remove the main remaining ambiguity.

The useful upgrade is therefore real and limited: after supplying a material edge and energy normalization satisfying one inequality, a conserved-current fluid possesses a positive-energy, dominant-energy-respecting, causal finite-density branch. The derivation establishes neither that the original complex field realizes it nor that cosmological evolution chooses its host-dependent material state, nor that the resulting equilibrium passes the observational gates.

## Follow-up: wording finding resolved

Re-read the updated parent document. Its equilibrium paragraph now explicitly identifies Newtonian Euler–Poisson with rest-mass density, disclaims an exact Einstein/TOV profile, and excludes a uniform weak-field approximation to the singular center. This resolves the wording finding above; the conditional constitutive theorem is unchanged. No further substantive issue was found within the stated scope.

Reviewed updated document SHA256: `1da1f637b383b0bc4e77e035430d2a8ca99e02c4aedbf790eda8d78dca167f01`.
Unchanged checker SHA256: `f498c02a763bd5f5de53dbf1ee6af2fb310fba404140658d8cb98880d0d9e2ee`.
