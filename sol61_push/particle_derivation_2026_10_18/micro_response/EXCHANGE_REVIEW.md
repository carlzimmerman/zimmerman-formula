# Independent narrow algebra audit of the exchange derivation

19 October 2026 UTC. Target: `../micro_exchange/MICRO_EXCHANGE.md`, sections 3–4 and the section 6 diagnostic, SHA-256 `16b968d92881bca4e1156ec92b88118cc0cbde8883b4786e44b8b0cda53c64da` at inspection. Review requested by the parent lane. No exchange file was changed. This is a fresh algebra reconstruction by the response subagent, not a certification of its complete numerical code or a referee report.

**Claim audited:** for the stated dilute same-charge relativistic threshold amplitude and an externally specified static orthonormal host basis, the contact coefficient, distinct-mode exchange matrix element, population signs, energy moments, detailed-balance ratio and auxiliary one-dimensional nonzero overlap follow as written. **Primary verdict: proved as written**, within those explicitly stated model and factorization assumptions. Physical formation or identification with the settled CE082 stock remains conditional on a named input: a self-consistent host and valid population/basis closure. Those applications are not the claim audited here.

## Dependency graph and obligations

| Arrow | Leaf type | Outcome |
|---|---|---|
| relativistic tree amplitude → matched `g_N` and scattering length | internal algebra and external-state convention | passed |
| positive-frequency propagator → RWA difference and missing contact | internal rational identity | passed |
| normal-ordered contact Hamiltonian → distinct-mode `2g_N I` coefficient | bosonic canonical commutation convention | passed |
| matrix element → continuum exchange expression | Golden-rule/occupation-factorization approximation explicitly declared by author | conditional on that named kinetic limit |
| each capture event → reciprocal number and energy moments | exact event stoichiometry and on-shell energy delta | passed |
| Bose occupations → gain/loss fugacity ratio | internal algebra | passed |
| delta host → normalized parity eigenstates and exact overlap | internal wave equation/integrals | passed |
| nonzero auxiliary overlap → physical 3D galaxy rate | no such implication claimed | out of scope |

No external theorem is needed for the algebraic leaves. The Golden-rule continuum and incoherent-state closure are assumptions of the exchange formula, not proved from the finite diagnostic.

## Decisive reconstruction

Write `g=g_N`, `lambda_r=lambda_rep`. For `H_int=(g/2)∫psi†psi†psi psi`, a distinct incoming pair and distinct outgoing pair have two creation orders and two annihilation orders. Its matrix coefficient is `(g/2)×2×2=2g`, multiplying the stated overlap. With relativistic external-state factors `(sqrt(2m))^4=4m²`, the relativistic amplitude is `−8m²g`; equating it to `−4lambda_r` gives `g=lambda_r/(2m²)`. This also gives `a=mg/(4pi)=lambda_r/(8pi m)` and identical-boson cross section `8pi a²=lambda_r²/(8pi m²)`. No missing factor of two was found.

The exact source propagator splits into positive- and negative-frequency pieces as in section 3. The retained positive-frequency piece gives `lambda_RWA=lambda_r+g_s²/[2M(M+2m)]`; the second piece subtracts precisely that extra term. The fractional difference divided by `lambda_min` is `(M−2m)/(2M)`. The contact matching therefore agrees with the complete threshold amplitude. In particular, the old regulated positive-square Hamiltonian should not be described as exactly threshold matched without this extra analytic contact. This distinction has been incorporated into the response derivation.

For the kinetic expression, the factor `1/2` converts the integral over ordered `(p,q)` into an unordered identical incoming pair. The inverse process has the same two identical continuum states, and the same prefactor is correct by relabeling the transition. Its products are

`G=(N_b+1)(1+f_r)f_pf_q`, `L=N_b f_r(1+f_p)(1+f_q)`.

Thus a capture increases `N_b` by one and changes the free count by `+1−2=−1`. With `epsilon_b=−B` and `epsilon_r=epsilon_p+epsilon_q+B`, the bound energy changes by `−B`, the free energy by `+B`, and the sum vanishes. A subsequent escaping particle is a spatial flux. The text already keeps that separate, and already limits the host to static infinite inertia unless recoil/work is included.

Using `1+f_i=exp[beta(epsilon_i−mu_i)]f_i`, the gain/loss ratio is

`G/L=exp{beta[epsilon_b+epsilon_r−epsilon_p−epsilon_q−mu_b+mu_f]}=exp[beta(mu_f−mu_b)]`.

It vanishes as a net current at common chemical potential and has the stated direction away from equilibrium. Coincident discrete modes need different ladder factors; the author explicitly excludes them from the continuum distinct-mode expression.

For the delta host, integrating the Schrödinger equation gives `u'(0+)−u'(0−)=−2kappa u(0)`. The displayed even continuum state has this jump; the odd state is zero at the origin. Their asymptotic amplitudes are `1/sqrt(pi)` with `k>0`, giving delta normalization in the parity sectors. The bound normalization is `kappa∫exp(−2kappa|x|)dx=1`. Direct integration also makes the bound mode orthogonal to the even continuum state, since the cosine and sine Laplace integrals cancel.

For `(kappa,p,q,r)=(2,3,6,7)`, on-shell energy is `9/2+18=−2+49/2`. Product-to-sum on `x>0` reduces the overlap to the four frequencies `(4,10,16,−2)` with signs `(+,+,−,−)`. The reduced coefficient is

`[3/10−3/52+9/130−9/4]/4=−63/130`,

which gives exactly the nonzero expression in (15). Its sign has no rate significance because the Golden-rule term contains its squared modulus. Scaling all momenta together preserves the energy equation and nonzero witness, while the separately stated weak-coupling and NR choices address the diagnostic approximation. This witness establishes neither the host’s origin nor a finite 3D rate.

## Checks, residual gap and strongest safe statement

Inspection used the raw report and the mode definitions; the matrix coefficient, propagator split, Bose-factor ratio, delta boundary conditions and overlap were reconstructed directly. No exchange script or numerical quadrature was rerun. The separate response script checks the propagator identities in exact SymPy arithmetic. The numerical tolerance, claimed tail bound and 128-control enumeration of the exchange run have **not** been independently code-audited here.

No algebraic correction is required in the audited sections. The strongest safe statement is that a specified host can support a reciprocal, energy-accounted, nonzero two-body capture channel whose coupling is matched to the same-charge particle amplitude. The next application check is a specified self-consistent 3D host, incident distribution and matching of its mode energies and mean field. It remains invalid to equate this channel’s existence with production of the required settled density or derivation of its `W`.

Review provenance: independent narrow derivation by a different subagent in the same parent session; same repository and model family, no claim of independent external review. Source hash should be rechecked if the exchange note changes.
