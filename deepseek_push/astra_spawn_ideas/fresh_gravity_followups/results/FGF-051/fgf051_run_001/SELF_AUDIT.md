# Author self-audit and mathematical proofreading

Primary verdict: **proved as written for the bounded local claim**, pending
independent review. This is self-review after author derivation, not a blind
second proof. Full-cone compression remains incomplete.

## Claim card

For each fixed compatible positive-background Q/scale/isothermal-fluid branch,
there exist N0 and positive N-independent edge width/time/speed constants
such that the unchanged C1,1 data admit the actual coupled local classical
solution on both stated shrinking edge cones through k_edge (L/v0)N^-7/2.
The cones contain fixed inner strips and all specified initial v=b0 and
v=b0+cs intersections; all positive-velocity packet acoustic/Q intersections
are included. The possible zero-velocity exterior b0=cs class is explicitly
excluded from the coverage assertion, not excluded from the data. For each
fixed B_*, sufficiently large N gives the full comparison time there.

## Dependency graph

Pinned exact equations/data and compatible background -> exact edge algebra
and bounded auxiliary extension -> direct characteristic start -> block
state/gradient bootstrap -> linear C1,1 bound -> exact compatible trace and
restart -> uniform local time -> contained cone and one-sided uniqueness ->
local response/adverse budget. Energy follows directly from the actual
compatible equations. Only initial formulas and framework scope are inherited;
no unproved whole-time existence theorem is used as a leaf.

## Obligation matrix

- Exact original joins and dimensional scaling: passed, (3.1)-(3.5), (2.3).
- Initial speed intersections with variable b0: passed, u^2<=v and full
  positive-value list (3.3); exterior b0=c qualification retained.
- Actual pressure, scale and Q equations: passed, all seven rows (2.4).
- Fixed-N start rather than real-speed assertion: passed, (4.1)-(4.2),
  contraction and spatial derivative interpolation.
- N-independent state and first-gradient estimates: passed, (5.1)-(5.5).
- Complete C1,1 propagation at joins: passed, (6.1)-(6.2), finite differences.
- Endpoint and restart rather than conditional a priori estimate: passed,
  (6.3), uniform time traces, same construction at compatible endpoint.
- Off-constraint algebra: passed. Subtraction gives g_theta=p_X; addition
  has +b h_chi(chi_X-k), removed only after scale constraint propagation.
- Full source B_X=C exp(q)+tau phi_thetatheta: passed, (7.2).
- Finite speed and genuine outer buffer: passed, (5.3), (9.1).
- Incoming fast core/exterior independence: passed via (9.2); comparison
  uses U speeds and finite V gradients on common compact cone, no prior
  bound on V speed and no lateral condition.
- Density and source gradients: passed, (8.1)-(8.2).
- Field feedback and adverse sign: passed, weak derivative argument in
  (8.4) and integrated constants 1/2,1/6 in (8.6).
- Moving-boundary energy: passed, (10.1)-(10.3), both field fluxes retained.
- Exact hydrostatic control: passed against all four equations (2.2).
- Evolving reference versus fixed branches: passed, explicit protocol work.
- Full-cone bounds, future resonances and physical closure: not addressed;
  explicitly out of the local theorem and left open.

## Decisive self-checks

Recomputed the edge identity v=u^2(2-u/sqrt N)^2, derivative
4u(2-u/sqrt N)(1-u/sqrt N), and second-derivative scale N^7=P^2.
Recomputed the characteristic signs R_+ at -b and R_- at +b.
Recomputed equation (9.2) by subtracting along U: the speed-difference term
has minus sign and multiplies V_X. Recomputed the response integral:
integrating Hz0 theta+(D_z/2)P^2 theta^2 gives Hz0 Theta^2/2+
D_z P^2 Theta^3/6. Recomputed dimensions for the adverse integral v0/L.
These are analytic checks, not executed finite tests.

Proofreading skill used in self-review mode over the entire new derivation
and this report: notation P versus coefficient bounds K1,K2, physical cs
versus dimensionless c, source coefficient C versus temporary generic bounds,
field p versus vacuum pressure, and signs/units were checked. Routine edits:
none after the proof draft. Mathematical-token typographical changes: none.
The acoustic exterior qualification is a deliberate mathematical scope
statement already in the draft, not a silent proofreading repair.

No literature theorem is an unchecked external leaf. This proof remains an
author candidate until an independent record pins and assesses it. Cheapest
next check is an independent reconstruction of the one-sided cone uniqueness
and C1,1 restart, followed separately by a core/interface estimate if accepted.
