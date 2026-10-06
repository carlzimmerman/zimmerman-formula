# Independent nonminimal common-cosmology trace audit

Accepted within the common mirrored-fluid and first-order response scope. I independently reconstructed the conformal matter variation and general-n exchange signs, the radiation and dust constant-field tests, the Friedmann expansion counting and the zero-initial-data retarded solution. The slow-memory inference is supported; neither an instantaneous algebraic rule nor actual recombination follows. No blocking correction was found.

## Frozen pins and current evidence

Author-observed HEAD `8d829a2cfeac401f2bd5abcf62c584377dd7980a`. Inspected SHA-256:

- REPORT.md: `7e7f8038713c221e870ccd237f62d2f48be5f9c2d60dea01097edf14be996a1d`
- checks.py: `2f9d2f27e62cbae95bb4e6b3ae52f1ab2e0dc3b4f1784090be0054739352a06c`
- contract.json: `e41b9068129b984d2e145d73830f81c9dd27f4435993fc87f9540ab7c510d34b`
- provenance.json: `f5e3969afe5a6ce9c417efa40325933f21a6d6a229f5e9a088118685fac1fd52`

The nonminimal action, retained slope proof and dynamical cutoff are fully pinned in that provenance and were independently read/audited as parent dependencies. I independently validated main_a, control_radiation_a, control_dust_a and control_adiabatic_a: all four current manifests validate. Main21/21 and controls21/22 are bounded implementation evidence, not the analytic derivation. This peer file is outside execution inputs; no author scientific input was modified.

## Actual variation and conserved matter signs

The exact exchange-even coincidence sector is Einstein gravity with coefficient M0, canonical psi, potential U and matter metric A_m² g_E. This sector is consistent with identical mirrored Jordan fluids, not ordinary-visible-only matter. At fixed Einstein metric, delta g_J=2alpha_m g_J delta psi and the matter stress definition gives delta S_m=integral sqrt(−g_E) alpha_m T_E delta psi. Combining with the canonical field gives Box psi−U_psi+alpha_m T_E=0.

The canonical scalar stress divergence is (Box psi−U_psi)partial^nu psi=−alpha_m T_E partial^nu psi. The opposite matter divergence therefore has the report’s +alpha_m T_E partial^nu psi sign. For T_E=−(1−nw)rho and homogeneous signature−+++, partial^0 psi=−psi_dot, this becomes rho_dot+nH(1+w)rho=alpha_m(1−nw)rho psi_dot. The scalar equation is psi_ddot+nHpsi_dot+U_psi=−alpha_m(1−nw)rho. Multiplying by psi_dot gives the opposite energy exchange exactly.

A second independent check uses Jordan conservation: rho_E=A_m^(n+1)rho_J and a_J=A_m a_E imply rho_E proportional to A_m^(1−nw)a_E^(−n(1+w)). Its derivative reproduces the exchange row. The rate conversion H_J=(H_E+alpha_m psi_dot)/A_m also follows directly from a_J and dt_J=A_m dt_E; it cannot be omitted when assigning a physical cosmological rate.

## Constant field and first-order background test

For empty matter vacuum, U_psi=0 admits the stated constant scalar de-Sitter solution. Radiation w=1/n has zero trace and zero exchange exactly, so the same field value persists for any positive ideal-radiation density on the radiation-plus-vacuum Friedmann solution. This is not a statement that every matter vacuum stress is traceless: an additional w=−1 fluid would have trace−(n+1)rho and change the stationary condition. The report’s vacuum is the specified scalar-potential vacuum.

At the same minimum, nonzero dust gives psi_ddot=−alpha_m,0 rho_d>0 initially, because p_A=2q_F/(d−2)>0 and the declared canonical orientation makes alpha_m,0<0. It cannot remain constant there. This establishes the initial direction toward increasing u; it is not a general monotonicity claim throughout nonlinear evolution. A matter-dependent extremum must include the changing conserved rho_d and its conformal psi dependence.

Adding rho_d,initial=epsilon U0 with vacuum scalar initial displacement/velocity zero gives delta psi=O(epsilon). Dust exchange is alpha_m rho_d psi_dot=O(epsilon²), hence rho_d=epsilon U0 exp(−nN)+O(epsilon²). At a scalar minimum, both its kinetic energy and potential deviation start at O(epsilon²). The dust correction to H is O(epsilon), but multiplying zero background scalar velocity or the O(epsilon) response affects the forced scalar equation only at O(epsilon²). Radiation remains exactly trace-free. This correctly justifies using the exact radiation-plus-vacuum background in the first-order scalar equation while still admitting the Friedmann dust correction in the full initial data.

Writing R=R0 exp[−(n+1)N] gives H_bar,N/H_bar=−(n+1)R/[2(1+R)]. Also U0/(M0 H_vac²)=n(n−1)/2. These two identities reproduce every coefficient and source factor of the displayed x_N equation. It is a controlled formal small-epsilon calculation on a fixed finite N interval. It does not certify relative accuracy against a dust density that becomes exponentially tiny, nor uniform accuracy at arbitrary future time. Scalar stress of order epsilon² can eventually exceed the much smaller epsilon exp(−nN) dust correction while both remain tiny relative to U0; that does not invalidate the stated first-order field response, but it prevents reading its late ratio as a full relative-density prediction.

## Independent retarded solution and memory

For R0=0, factor the operator as (D_N−lambda_+)(D_N−lambda_-), where lambda_++lambda_-=−n and lambda_+lambda_-=mu². Convolving the positive retarded Green kernel [exp(lambda_+N)−exp(lambda_-N)]/(lambda_+−lambda_-) with S exp(−nN) gives
X=S/mu²[exp(−nN)−lambda_+ exp(lambda_+N)/Delta+lambda_- exp(lambda_-N)/Delta].
This independently matches the report. At N=0 the bracket vanishes; its first derivative also vanishes using the two root identities. Applying the operator leaves exactly S exp(−nN). Positive forcing and positive Green kernel make X>0 for N>0.

The stable quadratic mass bound0<mu²<(n−1)/2 makes n²−4mu²>(n−1)²+1>0, so the roots are real negative. The characteristic polynomial at−1/2 is mu²−n/2+1/4<−1/4, while its value at0 is positive. Therefore −1/2<lambda_+<0. The slow coefficient−S lambda_+/(mu²Delta) is positive and nonzero. The retarded history consequently has a tail slower than a_E^(−1/2), while dust decays as a_E^(−n).

The special X_inst=S exp(−nN)/mu² is indeed an exact particular solution in constant H: its second derivative and n-friction term cancel. It has nonzero prepared initial displacement and velocity, so it is not the zero-initial-data response. Thus the calculation does not prove that no special density-tracking preparation exists. It proves that retarded vacuum preparation has a nonzero homogeneous memory coefficient and an unbounded ratio to that particular solution. In radiation history the cancellation no longer holds because H_N/H is nonzero; the separate bounded integration is appropriate.

The light mass inference is limited to the quadratic F class. It implies overdamping compared with nH friction, not generic rapid relaxation to a density-defined minimum. It is an actual stationary common canonical mass, not the earlier rolling potential-curvature ratio. Other F, prepared homogeneous modes or a different matter sector change the premise.

## Numerical and physical scope

The stable numerical example uses the actual retained integral and declared F0=1,c_F=10,gamma=.1, not an inserted target cutoff. The root, negative conformal charge and mu² about0.9104 are consistent with the previously audited vacuum formulas. The two-tolerance DOP853 integrations cover the declared eight e-folds and R0=0,10 with conserved first-order dust forcing. The vacuum solution is also compared with the independent exact response. The small quoted delta u concerns epsilon=10^-5; the enormous retarded/instantaneous ratio concerns an exponentially small denominator and is not a large physical field or observed cold abundance. No rigorous finite-epsilon error certificate is supplied.

Actual dust is an independently specified matter input here; its trace-driven cutoff response does not create that dust or determine its abundance. Ideal fluid radiation is not an atomic/photon transport model. Ordinary-visible-only backgrounds, relative metric/common-clock admission, perturbation growth and recombination remain absent. The Jordan action a0 is fixed; evolving F, cutoff and frame rates cannot be converted into an operational observed a0 or total-density law without the separate sourced equations and calibration. Neither the trace mechanism nor this initial preparation selects32pi.
