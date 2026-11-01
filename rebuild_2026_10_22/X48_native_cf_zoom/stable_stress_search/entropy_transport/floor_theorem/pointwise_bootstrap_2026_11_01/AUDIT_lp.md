# Independent audit of the all-p heat-flux route

Audited artifact: `lp_route.md`, SHA-256
`a3f5b88508bc9c3ef913f41a3dd1960c2b33275798d8671bff0a0ce5c63d09c2`.
Base checkpoint: **X48-DEN-2026-11-01-A**. Observed shared HEAD during
review: `8a293ba8b8411e84c9e37bb9770d1a6f993f606e`.
This audit writes only `AUDIT_lp.md`; it does not edit the proof artifact.

**Primary verdict: proved as written for the scoped local identities,
instantaneous entropy obstructions, and conditional finite-p interior
absorption.** No error was found in (P7)--(P9), the p>2 counterexample,
the new cotangents (P15), the closed-gate construction, or (P24).
The original actual-IVP pointwise bound and (UC) remain incomplete, as
the audited note states. This verdict does not upgrade them.

## 1. Normalized claims and dependencies

The audited claims concern finite internal faces of the unchanged X48 law,
at a fixed `s>0`, in the provisional state box and, for the counterexamples,
strictly inside its tight compression envelope. The discrete difference is
right minus left; `L=-ell*Delta q`, `ell>=0`; all cutoffs may be taken equal
to one on the tested face. Mechanical face conductance is a>0. The claims
are:

1. The complete stress heat cotangent has the exact derivatives (P8)--(P9).
2. For every fixed p>2, no finite constant multiplier of a separate q-p
   gradient dissipation absorbs that cotangent in the gradient-only
   inequality (P13).
3. The displayed stress-dependent quadratic companion creates a mechanical
   cross term that is positive on some actual closed-gate edge states.
4. The constant spatial quadratic companion gives (P24), for every finite
   p>=2, conditional on the stated state box and inherited coefficient
   bounds.

The dependency chain is the local material/transport source formulas,
the state-box and finite-edge coefficient estimates in
`nonlinear_closure_2026_11_01/heat_absorption.md`, the exact stress-weight
heat identity, and the finite-edge algebra in `lp_route.md`. There is no
external regularity theorem or numerical trajectory leaf. The first-energy
theorem is relevant to the proposed eventual iteration; it is not used to
make the instantaneous counterexamples into actual cold-start trajectories.

| Obligation | Audit result |
| --- | --- |
| Reconstruct stress and both heat gates from source definitions | Passed |
| Retain the heat part of the reciprocal-viscosity weight derivative | Passed |
| Verify `alpha_f=beta`, (P8), and fixed-f K derivative (P9) | Passed by independent algebra below |
| Check strict admissibility and actual open gates in (P10) | Passed |
| Check the p>2 divergence and p=2 endpoint | Passed |
| Reconstruct both cotangents of the quadratic companion | Passed |
| Check the new positive mechanical term on an actually closed face | Passed |
| Check the local necessity statement (P18)--(P19) | Passed for its stated all-neighbor, fixed-z spatial criterion |
| Check signed-endpoint coercivity and finite-p absorption constants | Passed, conditional on the pinned inherited bounds |
| Prove the level-gradient evolution term (P27) is controlled | Not addressed by a complete argument |
| Establish all-origin pointwise improvement, common collars, or (UC) | Not proved |

## 2. Independent reconstruction of the stress-coordinate algebra

Fix z and s, and write `r=rho`, `w=W`, `kappa=κ`, `c=1/100`,
`A=2K+c`, and `b=2r/w`. The source formulas give

\[
 \nu=\kappa\frac{2K+c}{K+c},\qquad
 P=b\kappa K,\qquad S=\nu x-2\kappa+b\kappa K.
 \tag{A1}
\]

With `T=f+S_d+2κ`, inversion gives
`x=(T-bκK)/nu`. Since `nu_K=κc/(K+c)^2`, direct substitution yields

\[
 \beta=\frac{c}{rw\kappa A^2},\qquad
 \alpha=\frac1{rw}
       \left\{\frac{c(T/\kappa-bK)}{A^2}
                           +\frac{b(K+c)}A\right\}.
 \tag{A2}
\]

Thus `alpha_f=beta` and `beta_f=0`, with derivatives taken in the
coordinates specified in the proof. For
`M_p=alpha*J_p(f)-beta*|f|^p/p`, the two beta-J_p terms cancel exactly,
leaving `(M_p)_f=(p-1)*alpha*|f|^(p-2)`. This also has the correct
continuous interpretation at f=0 for p>=2.

At fixed f and z, direct differentiation of (A2) gives

\[
 \alpha_K=-\frac{4cT/\kappa+2bc^2}{rw A^3},\qquad
 \beta_K=-\frac{4c}{rw\kappa A^3}.
 \tag{A3}
\]

For positive f=F, therefore,

\[
 (M_p)_K=
 -\frac{4cF^{p-1}}{rw\kappa A^3}
 \left\{S_d+2\kappa+(1-1/p)F+\frac{b\kappa c}{2}\right\}<0.
 \tag{A4}
\]

The sign uses κ>0 at positive active time and S_d>=0. It is not a
derivative at fixed x; replacing the derivative coordinates would destroy
the displayed cancellation. Equation (A4) agrees exactly with (P9).

The complete heat cotangent itself was also checked: differentiating
`V*|f|^p/(p*nu)` gives the heat coefficient
`V*J_p(f)*S_K/nu - V*|f|^p*nu_K/(p*nu^2)`. Dividing by dm*W gives
M_p because `V=dm/rho`. This confirms the beta term and its sign without
assuming a derivative of either heat gate.

## 3. The separate q-p entropy counterexample

At a sufficiently short positive homogeneous reference time, take both
densities equal to rho_d, choose a small positive constant stress error F,
and perturb memory as

\[
 K_l=K_d+\varepsilon/W_d^{3/2},\qquad
 K_r=K_d-\varepsilon/W_d^{3/2}.
 \tag{A5}
\]

For sufficiently small positive epsilon, nonnegative K, the upper memory
bound, and the tight compression envelope are all strict. Inverting (A1)
independently at the two endpoints realizes `f_l=f_r=F`. With
`F=delta*nu_d/4`, the unperturbed compression is `x_d+delta/4`, leaving
room for both small memory perturbations. The existence of a strict
reference memory margin follows from its positive heater and the strict
pre-rounding upper bound in the pinned heat estimate.

Both actual gates are open: `K_l>K_r` and, at equal density,
`psi_l>psi_r`. Accordingly L>0, even though L tends to zero with epsilon.
There is zero mechanical stress dissipation and zero density gradient.
The two relative thermal errors are plus/minus epsilon. Equations (A4)
and (A5) give

\[
 \Delta M_p=-\frac{2\varepsilon}{W_d^{3/2}}(M_p)_K
                    +o(\varepsilon)>0,
 \qquad \Delta J_p(q)=-2\varepsilon^{p-1}.
\]

Dividing the positive stress heat work by the magnitude of q-p heat
dissipation cancels the **actual** luminosity L. The quotient grows as
`[-(M_p)_K/W_d^(3/2)]*epsilon^(2-p)`. This proves the stated failure for
every fixed p>2 and every finite constant multiplier in (P13). At p=2
the quotient is finite, so there is no conflict with quadratic absorption.

This is a valid instantaneous edge-state counterexample to a uniform
gradient-only inequality. It neither supplies a trajectory from the
prescribed virgin data nor refutes an inequality containing additional
local terms or a separate memory-gradient energy.

## 4. Quadratic companion and the closed-gate test

For the companion `lambda*dm*W^(-1/2)*q^2*w(f,s)/2`, the mechanical part
of its derivative is

\[
 \frac\lambda2 dm W^{-1/2}q^2 w_f\nu\mathcal L_r f.
\]

Converting dm to V gives exactly the additional mechanical cotangent
`lambda*rho*nu*W^(-1/2)*q^2*w_f/2` in (P15). Its two heat derivatives
use `q_t|heat=W^(3/2)H` and `f_t|heat=S_KH`; division by dm*W gives
`lambda*w*q` and `lambda*S_K*q^2*w_f/(2W^(3/2))`. Thus both cotangents
in (P15) reconstruct correctly. Derivatives of W are local z evolution,
not omitted heat divergence terms.

At fixed f and z, w_f is fixed, while `q_K=W^(3/2)`. Therefore the
mechanical cotangent has K derivative

\[
 (T_w)_K=\frac\lambda2\rho W^{-1/2}w_f
                \{\nu_Kq^2+2\nu qW^{3/2}\}>0
\]

at the stated q>0, w_f>0 interior state. Choose `Delta K=h>0` and
`Delta f=-t*h`, with positive t small enough that
`(T_w)_K-t*(T_w)_f>0`. The original gradient gate is closed because
K increases outward, independently of the temperature drop. For small
h the leading mechanical work is
`a*t*[(T_w)_K-t*(T_w)_f]*h^2>0`, with no heat or density-gradient work.
This verifies (P17) and its stated scope.

The general necessity statement is local and is also correct: if a smooth
entropy `sum V*e(x,z,K,s)` is to have nonpositive interior spatial work
for **all** neighboring states at fixed z, closed faces force
`partial_K(e_x)|_(f,z)=0`. Otherwise an arbitrarily small signed
`Delta f/Delta K` makes the leading work positive. Writing that
cotangent as G(f,z,s), the coordinate identity `e_x=nu*e_f` integrates
to `e=H(f,z,s)/nu+h(z,K,s)`, with `H_f=G`, as in (P19).
This is not a necessity theorem for dynamic estimates containing
independent spatial-gradient energies or compensating local work.

## 5. Finite-p estimate and its limit

The signed-endpoint inequality (P21) is valid. For like signs its secant
quotient is at least R^(p-2); for opposite signs it is
`R^(p-2)*(1+t^(p-1))/(1+t)>=R^(p-2)/2`, `0<=t<=1`.

Using the inherited coefficient bounds in the exact product difference,
the coefficients before eliminating Delta K can indeed be taken as

\[
 536(p-1)+45000,\qquad 2.8325\,10^8s,\qquad
 6.55\,10^{10}s^2.
\]

For example the two non-alpha contributions to the Delta f coefficient
are each at most `9*s^(-2)*R<=22500`. The two density contributions
are `1.45e7*s` and `2.6875e8*s`. Eliminating Delta K adds
`2.1353e16*s^7` to the density coefficient and changes the thermal
coefficient to `3.6025e10*s^2`. For s<=10^-3 the extra density term is
at most `0.021353*s`. These numbers are below the rounded constants in
(P22).

The stress cross term then spends at most
`sum a*R^(p-2)*(Delta f)^2/8<=D_p/4` and a weighted heat square with
coefficient `2*D_0*A_0^2*p^2*s^4`. The density cross term spends one
weighted heat square and leaves `D_0*B_0^2*s^6/4` times the weighted
density square. The last term spends `C_0*s^2` times the weighted heat
square. Since `R<=A_s`, the multiplier (P23) covers these terms and
leaves exactly the negative shares claimed in (P24). Closed faces cause
no division by ell and present no exceptional case. The argument is
uniform in N under its stated inherited bounds.

The companion's explicit time derivative is correctly
`(2p-4)/s` times its energy, since `A_s^(p-2)` is proportional to
`s^(2p-4)`. This term is not controlled by the interior estimate itself.
Likewise (P27) has the correct factor 1/4 from differentiating the
average of the two level weights.

The p-th-root conclusion in section 6 is accurate: an estimate with a
factor `A_s^(p-2)` and only a fixed additional startup power converges
to the provisional amplitude scale A_s as p tends to infinity. It does
not yield a positive improvement in that scale. This observation does
not rule out a different recurrence, level estimate, or energy; the
note makes only the narrower claim.

## 6. Remaining gap, validation, and review provenance

The smallest displayed new unresolved estimate is control of (P27),
together with its companion level-gradient terms, by energies and
dissipations uniform in N and near the active-level boundary. A proof
of that estimate alone would still have to be assembled with local
reaction, time-weight, and cutoff estimates and then with common
prefix/collar coverage. No implication in this audit presupposes those
missing estimates.

Review consisted of reading the raw proof, reconstructing the derivatives
and cotangents independently from `material.py`, `transport.py`, and
`convective_transport.py`, checking the inherited coefficient hypotheses,
and hand-checking all finite-p roundings above. No physical integration,
grid sampling, or symbolic computation is load-bearing. Scoped whitespace
and mathematical-display checks are supplementary formatting validation.

This is an independent review by the separately delegated radial-route
agent, not the author of `lp_route.md`. The reviewer received the raw
artifact and a request to reconstruct the critical identities, without a
requested verdict. The full upstream proof of the inherited geometric
coefficient bound was not independently reproved here; the conditional
finite-p verdict retains that pinned input as an explicit hypothesis.

Pinned supporting input SHA-256 hashes, paths relative to
`stable_stress_search/`:

| Input | SHA-256 |
| --- | --- |
| `material.py` | `4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390` |
| `collapse.py` | `14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf` |
| `entropy_transport/transport.py` | `2d93b679135ca176a16327f094c114eb1e9dbc21ba4adc56c2e209d60f78ee8c` |
| `entropy_transport/convective_transport.py` | `ee8ac635b8edc91208f1fcc5765aa7e0999a3975f286dd5b52384f75dfe63e97` |
| `entropy_transport/floor_theorem/nonlinear_closure_2026_11_01/heat_absorption.md` | `b98843cec40271ef4a16bdb6c15baf50a43c203d6367fbf3ae72a4d299b74379` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/pointwise_continuation.md` | `a2bc945dc7742faa803b0d7b858096a3424f5945ccef1dc02253c9a850701ea9` |
