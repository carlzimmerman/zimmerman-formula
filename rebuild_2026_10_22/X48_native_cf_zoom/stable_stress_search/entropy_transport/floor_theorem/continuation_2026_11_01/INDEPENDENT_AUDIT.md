# Independent audit of the three startup continuations

**Normalized claim.** For the exact `ConvectiveCollapse` IVP specified in
`../TARGET.md` and the transport README, prove
\[
 \exists T>0\quad\forall N\ge32\quad\forall s\in[0,T]\quad
 \forall i\le\lceil N/4\rceil:\quad
 x_i(t_a+s)=C_i(t_a+s)\ge4.                         \tag{UC}
\]
Here every exact solution has positive ordered-shell geometry on the interval,
the initial sphere is \(\rho=1/4,R=1,u=-r/4,K=0\), and all physical
coefficients are fixed at the values in the README. The activation data are
\(\rho_i(t_a)=1,K_i(t_a)=0,x_i(t_a)=C_a\), with the common exact dust
formula for \(C_a\). A time depending on \(N\), a bound at sampled times,
an arbitrary-state example, or a theorem for a different linear system does
not establish this claim.

**Primary verdict: incomplete, with the smallest missing implication being
a localized, pointwise-in-time bound on compression for the full nonlinear
startup trajectory, uniform in \(N\).** None of the three notes proves UC.
Their principal partial results below pass in their stated scopes. No
specified-IVP counterexample is provided by these notes or by this audit.
The new leading-model pointwise smoothing theorem is valid; it must not be
mistaken for the missing nonlinear, boundary-forced estimate.

This is a fresh proof audit of `effective_flux.md`,
`all_mesh_certificate.md`, and the finalized `entropy_energy.md`, using
the proof-audit skill. Only this audit file was written. The original
preservation/global-continuation results and historical finite probes are
dependencies or context, not claims newly certified by this audit.

## Dependency graph and obligation matrix

The dependencies are:

1. Exact source law and ordered geometry give the stress, continuity,
   compression, and heat identities.
2. Those identities give the primitive/Green equation without spatial
   derivatives of the constitutive coefficients.
3. An assumed compression-amplitude bound gives actual-geometry coefficient
   bounds, weighted scalar energy, and the boundary barrier.
4. The exact Duhamel identity separates that boundary barrier from an
   unbounded nonlinear constitutive/heat term, called (AC).
5. Independently, fixed or homogeneous leading systems give the spectral
   contraction, coupled gradient energy, and Nash-based pointwise smoothing.
6. Exact heat-edge differentiation and positive reduced stiffness expose
   a possible nonlinear energy structure, but leave its commutator,
   time-dependent weights, and cutoff work unestimated.
7. No implication from steps 2--6 to unconditional UC is supplied. The
   existing conditional UC-to-entropy-floor reduction cannot supply UC
   itself.

All leaves audited here are elementary internal algebra, finite-dimensional
ODE/linear algebra, or stated hypotheses. No external regularity theorem or
finite trajectory computation is a proof leaf.

| Obligation | Result | Scope or restriction |
| --- | --- | --- |
| Full stress and compression identities, including outer half mass | passed | Exact finite semidiscrete law on valid geometry |
| Primitive, tail momentum identity, Green inversion, Volterra identity | passed | Active-branch restriction and full-branch correction retained |
| Stieltjes memory estimate and conditional cubic-memory bound | passed | Requires the stated compression bootstrap |
| Actual-geometry form and weighted energy estimates | passed | Requires the stated amplitude bound on the graph used |
| Actual-geometry boundary barrier | passed | Global \(\lvert x\rvert\le10\), \(T=10^{-3}\); includes \(\lceil N/4\rceil\) |
| Actual-geometry Duhamel and time integration by parts | passed | Identities; neither proves (AC) |
| Leading density-memory spectral contraction | passed | Fixed selfadjoint graph, regular compatible data, \(0<\alpha<3\) |
| Full heat-edge variation and local-gradient principal matrix | passed | The two are explicitly distinguished; switching faces use one-sided derivatives |
| Positive heat-reduced density stiffness | passed | \(\rho>1,x>2,K\ge0\) |
| Heat/stress conductance ratio and spatial pairing | passed | Pairing identity, not a complete nonlinear energy derivative |
| Density-gradient energy | passed | Scalar \(c>0\); stated weight signs and homogeneous boundary conditions |
| Uniform radial Nash and leading-model pointwise smoothing | passed | Fixed homogeneous graph; regular-data leading system; actual \(C_a>16/3\) |
| Nonlinear commutator, weight/cutoff work, and forced pointwise closure | not addressed | Explicitly retained as open in the notes |
| Establishment of the common-time compression bootstrap | not addressed | Cannot be inferred from its own conditional consequences |
| UC for the specified IVP | not addressed | The required uniform implication is absent |

## Independent reconstruction of the decisive identities

### Exact stress and derivative-free flux

The code gives, in the normalized units,
\[
 S=P+\kappa(x-2)_++\kappa g(K)x,\quad
 \kappa=\tfrac12\rho Wh,\quad P=K\rho^2h,\quad
 g=K/(K+.01),\qquad \rho'=\rho x.
\]
The memory term is signed; replacing it by a positive-part stress would
change the law. Direct differentiation of the joining polynomial gives
\(W'=h\), hence
\[
 F=(W^2-9/4)/4,\qquad F'=Wh/2,\qquad \dot F=\kappa x.
\]
The identity
\[
 S=(1+g)\dot F-2\kappa+P+\kappa(2-x)_+
\]
is valid on every branch. The stated bounds
\(3(\rho-1)^3/8\le F\le(\rho-1)^3\) on \(1\le\rho\le2\)
follow by setting \(W-3/2=\delta^3(1-\delta/2)\).

Write \(A_i=4\pi r_i^2\), retaining \(\mu_N=dm/2\). Differentiation
of \(J_i=\sum_{j\ge i}\mu_ju_j/A_j\) gives
\[
 J_i'=S_i-B_i,\qquad
 B_i=\sum_{j\ge i}\mu_j
 \left[\frac{Gm_j}{4\pi r_j^4}+\frac{2u_j^2}{4\pi r_j^3}\right]\ge0.
\]
There is no sign or boundary-term omission: the stress telescopes to
\(S_i\), whereas a truncated tail retains its endpoint stress. Moreover
\(J_i-J_{i+1}=\mu_i u_i/A_i\), so \(L_rJ=x\).
The zero-exterior summation identity
\(\langle f,-L_rf\rangle_V=\sum a_i(\Delta f_i)^2\) proves invertibility
and the finite-graph minimum principle proves positivity of
\(G_r=(-L_r)^{-1}\). Thus \(J=-G_rx\), with exactly the sign used in
the note.

On a cell with \(x\ge c>2\), \(F\) is increasing and
\(M=\int g\,dF\) lies between zero and \(g_*F\). This proves the
integrated-stress bounds without a bound on \(K'\) or heat-flux variation.
Combining the identities gives
\[
 G_{r(s)}x(s)+F(\rho(s))
 =G_{r(0)}C_a\mathbf1+\int_0^sB
   +2\int_0^s\kappa-\int_0^sP-M.
\]
On other branches the additional right-side term is
\(-\int\kappa(2-x)_+\). The memory and pressure corrections are
\(O(s^6)\) under the stated common compression bootstrap; that bootstrap
has not been derived. The prefix-maximum argument is legitimate because
the outward flux cannot import heat from outside a prefix, and a prefix
maximum cannot receive heat from a smaller inward value.

This Green equation does not control instantaneous \(x\) from potential
amplitudes. The note's single-site potential has amplitude \(O(N^{-2})\)
and \((L_rZ)_k=-D\) at a fixed positive material radius; its compatible
velocity perturbations have amplitude \(O(N^{-1})\). Its geometry remains
valid. It is an admissible-state obstruction to an inversion estimate, not
a solution from the specified initial sphere.

### Moving geometry, barrier, and exact Duhamel equation

Telescoping cell volumes gives
\[
 \frac{u_i}{r_i}=-\frac{\sum_{j\le i}V_jx_j}{3\sum_{j\le i}V_j},\qquad
 V_i'/V_i=-x_i,\qquad a_i'/a_i=4u_i/r_i.
\]
Consequently the exponential volume/radius/conductance bounds require only
compression amplitudes, with no spatial derivative of compression.
The relative-form bounds and the weighted scalar energy follow directly
by Cauchy--Schwarz and summation by parts. In the exponential-weighted
identity the outer Dirichlet edge has only its negative energy term. The
coefficient \(C_\lambda\) in (10a) bounds all internal endpoint costs.
The final (10b) statement correctly restricts its extra
\(e^{-\lambda d}\) factor to ordered separated source/observation sets.

For the actual-graph barrier, the drift cancellation is
\[
 (r_i^4-r_{i-1}^4)/V_i\le r_i/\pi.
\]
It gives the stated rates, while bounded cell volumes give their symmetric
sum. With \(\lambda=9\), the coefficient of \(s^2\) is below
\(4\cdot10^6\). The worst requested cell obeys
\(i/N\le9/32\), and
\[
 b_i\le12e^{-207/32+1/750}<1/48.
\]
The last strict inequality is elementary: the exponent magnitude exceeds
\(32/5\), and the positive exponential series through degree 11 gives
\(e^{32/5}>576\). The proof treats \(b_N\le12\) as the comparison
boundary, so the special outer mass is not replaced by a full mass.
This result assumes \(\lvert x_i\rvert\le10\) on the entire graph.

With \(w=x_d-x\), \(S^{lin}=S_d-\nu_dw\), \(\delta S=S-S^{lin}\),
and ghost \(w_{N+1}=S_d/\nu_d\), direct substitution gives
\[
 w'=\nu_dL_rw+(R_d-R)-L_r\delta S.
\]
The actual propagator is positive and an infinity-norm contraction. Its
Duhamel formula and \(R\ge0\) give the upper bound
\[
 w_i\le b_i+47s+
 \left[-\int_0^sP_r(s,v)L_r(v)\delta S(v)\,dv\right]_i.
\]
There is no moving-conductance remainder in this formulation. The
alternative formula for \(z=\delta S/\nu_d\) has the correct signs:
\[
 -\int_\eta^sP_rL_r\delta S
 =z(s)-P_r(s,\eta)z(\eta)-\int_\eta^sP_rz'.
\]
It follows from \(\partial_vP_r=-P_r\nu_dL_r\) without assuming that
generators at different times commute. The fixed-\(N\) limit
\(z(\eta)\to0\) supplies no uniform estimate on the last integral.

### Leading density-memory spectral, energy, and smoothing results

For \(L=-\lambda\), the leading regular system reduces under
\(z=\lambda s^3/3\) to
\[
 w_z=-(w+\alpha y),\quad 3zy_z=w-y,\quad
 zw_{zz}+(z+1/3)w_z+(1+\alpha)w/3=0.
\]
Let \(a=(1+\alpha)/3,b=1/3\), and
\(d\mu\propto t^{a-1}(1-t)^{b-a}dt\). Integration by parts gives
\(zg''+(z+b+1)g'+ag=0\), with \(g=\int e^{-zt}d\mu\).
Then \(f=g+3zg'\) satisfies both spectral equations with \(y=g\).
Since \(-3e^{-4/3}\le(1-3q)e^{-q}\le1\), the stated spectral
\(L^2\) contraction follows for \(0<\alpha<3\). This statement is
not an infinity-norm contraction.

The density-gradient energy (30) is also exact. Differentiating
\(\|\xi\|_V^2/(2c)+\mathscr D(\zeta)/2\) gives the mixed terms
\(-\sum a\Delta\xi\Delta\zeta\) and its opposite. The remaining
four terms are exactly those displayed in (30). Its signs require the
stated hypotheses on \(V',a',c'\); its singular leading specialization
is an identity for \(s>0\), not an unproved finite activation-energy bound.
The source-law expansions give the recorded \(k_2,c_1\) and
\(c_1/k_2=2(C_a-2)/C_a\).

The final section of `entropy_energy.md` supplies a valid additional result.
At fixed homogeneous geometry the edge resistance tail is
\(O((i/N)^{-1/3})\), including the doubled outer conductance. Its
superlevel estimate and layer-cake calculation give exactly
\[
 \|f\|_2^{10/3}\le C_N\mathscr D(f)\|f\|_1^{4/3}.
\]
The notation \(C_N\) denotes a constant independent of mesh count in that
note. The energy differential inequality and selfadjoint duality then
give the \(t^{-3/4}\) heat-semigroup bound. Integrating the exact beta
representation against it is valid when \(a>3/4\). The rational bound
\(C_a^2>329593/11520>256/9\) verifies that condition for this IVP's
coefficients. Thus both leading fields have the claimed
\(O(s^{-9/4})\), mesh-uniform \(L^2\)-to-pointwise bound for regular
initial data. No arbitrary-forcing or nonlinear approximation theorem
follows from this regular-data multiplier.

### Heat variation, stiffness, and the unclosed nonlinear energy

The exact face derivatives in `entropy_energy.md` (11)--(16) were checked
from the full outgoing luminosity, including both positive-part switches,
the entropy-gradient gate, both density gates, area, centroid separation,
and the cell \(1/W\) denominator. In particular \(L_{z_r}\) has no
fixed sign. When both driving drops vanish the first derivative is zero;
when only one vanishes a one-sided first derivative need not vanish.
Therefore a positive heat diffusivity at a completely homogeneous state
would be a surrogate, not its actual linearization.

The local-gradient matrix (20) has eigenvalues
\(\nu,J_K/W,0\), as stated. It is explicitly distinguished from the
complete finite-edge Jacobian. Differentiating the entropy-gradient gate
adds the \(b_qJ\) term to \(J_K\); discarding it would be an incorrect
linearization. The exact constitutive formula is
\[
 \begin{split}
 S_z-S_K\psi_z/\psi_K={}&
 \kappa\{[(1+g)x-2](1+w+j)-\tfrac32wxg(1-g)\}\\
 &+P(2+j-\tfrac32w),\quad
 w=\rho h/W\in[0,1],\quad j=\rho h'/h\ge0.
 \end{split}
\]
Writing \(x=2+e\) proves the stated lower bound
\(\kappa[(x-2)+g]+P/2>0\). Since
\(0\le J_z/J_K\le\psi_z/\psi_K\), the same bound applies to the
heat-reduced stiffness. This is positive constitutive stiffness, not
an estimate on the variable nonlinear propagator.

The centroid formula gives \(4\pi r_i^2d_i\ge V_i/4\), hence
\(\ell_i/a_i\le4D\rho_i h_i h_{i+1}b_i\) at every internal face.
The spatial pairing (24) is correct with the now-explicit tests of
\(S'_{spatial}=\nu L_rS+S_KH\) and
\(\psi'_{heat}=W^{3/2}H\). Its exterior stress work is
\(-a_Nf_NS_N\), not a silently vanishing boundary term.
The conditional \(\alpha\le536\) estimate and
\(\ell\bar\alpha^2/a\le1.4\cdot10^{10}s^4\le.014\) check out.

Splitting \(\Delta(\alpha f)\) leaves exactly the commutator (27).
The displayed Young inequality is valid. Bounded \(\alpha\) gives a
raw difference bound but no mesh-uniform control of the resulting
conductance-weighted term by capacity energy. Neither that term nor the
state-dependent weight derivatives and cutoff work is bounded here.
Calling (24) itself a completed time-dependent energy inequality would
therefore be an invalid inference; the finalized note does not do so.

## Exact remaining gap and strongest safe statement

One sufficient completion would prove (AC) on \(0<s\le10^{-3}\) for
the actual law and establish its compression/geometry bootstrap without
assuming UC. Then
\[
 x_i\ge C_a-1/48-.047-1>4
\]
would follow, including \(\lceil N/4\rceil\). Even using only
\(C_a>21/4\), the displayed lower bound exceeds four by
\(1093/6000\). Neither required input is established.

The energy route instead needs a nonlinear localized estimate controlling
(27), weight derivatives and boundary/cutoff work, followed by a forced
pointwise estimate for the actual fields. The new Nash theorem legitimately
provides a fixed-graph leading-model building block; it does not perform
these transfers. This is the smallest missing implication identified by
the proofs, not a claim that these particular sufficient routes are
necessary for every possible proof of seeding.

The strongest safe statement is the conjunction of the exact identities,
conditional actual-geometry scalar estimates, positive full-symbol
stiffness, and the stated leading-system contraction/energy/smoothing
theorems. The original all-mesh startup claim and its unconditional
entropy-floor consequence remain open. The cheapest decisive next check
is a proof of the missing nonlinear forcing/commutator estimate with its
actual bootstrap and boundary conditions; additional sampled grids do
not test that universal implication.

## Verification, independence, and pinned revisions

The audit reconstructed the identities from the four source files before
accepting the proposed reductions. A further isolated reviewer read only
the raw law and independently checked the frozen full-heat symbol and
effective-stiffness sign before receiving any author proof. Its result was
checked against the exact edge formulas above. Agreement between reviewers
is not used as a substitute for these derivations.

Checks used direct reads, `rg`/file discovery, SHA-256 evaluation, elementary
exact arithmetic, and exact SymPy expansion of the primitive and compression
square identity. Rational checks verified the final \(19/12\) activation
bound, barrier margin, and the conditional heat-cross coefficient. No
trajectory was integrated, no new grid run was made, no old finite result
was promoted to proof, and no source or author proof note was edited by
this audit. No applicable project `AGENTS.md` or `.mathbox` ledger was found
in the inspected scope.

The following SHA-256 values identify the exact audited revisions. Paths
are relative to `stable_stress_search/`; moving shared Git HEAD is not
used as the mathematical revision identifier.

| Input | SHA-256 |
| --- | --- |
| `material.py` | `4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390` |
| `collapse.py` | `14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf` |
| `entropy_transport/transport.py` | `2d93b679135ca176a16327f094c114eb1e9dbc21ba4adc56c2e209d60f78ee8c` |
| `entropy_transport/convective_transport.py` | `ee8ac635b8edc91208f1fcc5765aa7e0999a3975f286dd5b52384f75dfe63e97` |
| `entropy_transport/README.md` | `8719a07f915902b829030d178636e27602f362c0f0b0e4e9e5d02039f575d2f6` |
| `entropy_transport/DERIVATION.md` | `e08312d0dc3be7f3f2d225ca938a7872ceec6d4c2532db2102f54c7a984910da` |
| `entropy_transport/floor_theorem/TARGET.md` | `93792a4df2982bb70bbb68be3878405dbd3f8e2ea735c5f586ce0b28b2394b14` |
| `entropy_transport/floor_theorem/seed_route.md` | `752944eb3c0c7ff87007b5ca1c3f5a46bb768d8215645914ad6b211cebcd053d` |
| `entropy_transport/floor_theorem/startup_energy_route.md` | `06630aecae84c9b618e84c1ddded3f2025f7a89f7dca634bbbb05f50d0e2380b` |
| `entropy_transport/floor_theorem/STATUS.md` | `d05a94e8f701f0e1d5076dc9c3fbaf7468bb8b5822a493e64e275d867ae712f6` |
| `entropy_transport/floor_theorem/continuation_2026_11_01/effective_flux.md` | `ba03913a2d497fcefc346b8f04cc0da2d128a3f7dee34ee535c36155459f3ba3` |
| `entropy_transport/floor_theorem/continuation_2026_11_01/all_mesh_certificate.md` | `15582ff1b45a715fccc5c84cd4883fa533ce714fb77b7ef091aa53205ba69a18` |
| `entropy_transport/floor_theorem/continuation_2026_11_01/entropy_energy.md` | `bb4429ad5f3c9345d2c6d44a7864c407e273caad13ed3643fac5aa822c9990e3` |
