# Author self-review (not independent acceptance)

Applied mathbox:proof-audit to the completed bounded argument and
mathbox:proofread-math in self-review mode. Primary author audit verdict:
**proved as written for the precise contained-cone claim**, pending separate
independent review. This is not a claim that the metadata verifier checks proof.

Claim card: all positive coefficients and a compatible smooth background are
fixed; Vmax>15cs/2; choose 15cs/2<V<Vmax and 15/2<B<Bcap<V/cs. For sufficiently
small epsilon, exact C1,1 packet data admit a compatible solution on K_e through
kappa epsilon/V, and no positive C1 solution on that same K_e survives through
B epsilon/V. Constants are epsilon-uniform only. Both field speeds may exceed V.

Dependency graph:
- Full Q/fluid/scale source and chart: pinned FGF054 Section 2 and FGF051
  Sections 2,7, rederived in DERIVATION Section 2.
- Local C1,1 start: pinned FGF051 Section 4, explicitly instantiated in Section 7.
- Difference-quotient structure: pinned FGF048 Sections 4--5 and FGF051 Section 6;
  fixed-V estimates, margins and endpoint traces reconstructed in Section 7.
- New cone amplitude bootstrap -> new varying-background field comparison ->
  new exterior acoustic bootstrap -> exact flux capacity identity -> upper
  contradiction. These are internal proof leaves, not externally imported facts.
- Scope and zero-V check: explicit exact substitutions, not simulations.

| Obligation | Result | Exact evidence |
|---|---|---|
| Ten task ancestry hashes before source use | passed | first metadata check returned ten PASS entries |
| Fixed physical coefficients and dimensional time | passed | Sections 1,2,8; epsilon and V independent |
| All field/acoustic travel inside source domain | passed | Hrad=3+S Bcap/V; radius >=3e; strict S bounds |
| Incoming density/scale sources retained | passed | H_i in (2.3), K includes exp(q), h_chi and scale terms |
| Upper estimates without solution-gradient hypotheses | passed | (3.4) contains z0_X only, plus source amplitudes |
| Actual field-background estimate | passed | dz initial zero; (3.5), g-g0<=Cg t |
| Actual exterior fluid O(e^2) | passed | (4.2) exact advective terms; bootstrap actual speed magnitude <eta/2 |
| Exterior path entrance directions | passed | right speed <h_a and left speed >-h_a imply backward containment |
| No assumed walls or exact stationary patch | passed | both wedge paths reach initial exterior; field arrivals allowed |
| M,P,I boundary signs | passed | integration by parts and alternate Delta=int(D-X)n check |
| Pressure/mass/field flux accounting | passed | (5.1)--(6.6), no separate flux set to zero |
| Remainder versus moment margin | passed | e^3,e^4,e^6,e^4 versus positive mu e^2 |
| Actual sub-ceiling velocity and density | passed | (3.2),(3.3) with strict epsilon margins |
| Exact polynomial joins | passed | ||f'||=8/(3sqrt(3)); Lip(f')=8; no smoothing |
| Fresh same-cone lower time and compatible restart | passed | (7.1)--(7.3), trace construction, restrict to K_e |
| Zero-velocity negative control | passed | H exact, all fluxes and P0 zero; no division by V |
| Physical tuple / maximal-germ / endpoint classification | out of scope | explicitly not inferred |
| Separate independent audit of this raw proof | not addressed by author | required before promotion |

Adversarial checks performed analytically:
1. Derived both centered fluid equations independently. The hydrostatic piece
   -g0 cancels -c^2 q0_X, but the +/-c v q0_X terms remain.
2. Reversed the moving-inner-edge direction in thought: if it moved slower
   than an acoustic family, backward paths could meet it and require data.
   The strict actual velocity bootstrap gives the correct faster-edge direction.
3. Differentiated Delta directly and via ell M-I; both give ell j(A)-P.
4. Differentiated field momentum: (gA-W)_X=gA_X+Tscale k; the scale force
   cancels it with the required sign. Both pA and Jwk energy fluxes survive.
5. Made field speeds arbitrarily large while keeping them finite: Hrad and
   constants grow, but every epsilon threshold remains positive. No factor
   c/field_speed or field_speed/V is required to be small.
6. Checked lower-time equality case: the a priori first/higher derivative bounds
   provide actual endpoint traces for each fixed e, so a restart exists even
   at kappa e/V. No uniform individual restart time is claimed.

Conservative proofreading covered the complete new derivation and all equations.
Routine clarification: the O(e) field momentum estimate applies throughout I,
not merely its endpoints, which justifies Fm=O(e^2). No other mathematical-token
changes were made during proofreading. No unresolved typo or internal implication
was identified. This self-review can share the author's conceptual errors;
independent review remains mandatory.

Strongest safe statement is the bounded cone theorem above. The cheapest next
check is an independent raw-proof audit of (3.4),(4.1)--(4.3),(5.2) and Section 7,
with the final proof and result hashes pinned. No additional sweep is needed.
