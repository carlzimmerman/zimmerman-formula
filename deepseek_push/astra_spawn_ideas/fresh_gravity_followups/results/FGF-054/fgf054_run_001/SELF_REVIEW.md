# Author self-review, not independent acceptance

Normalized claim: conditional on fixed physical coefficients/background and
Vmax>(15/2)max(cs,b*,sqrt(J/sigma)), the exact finite-V shrinking C1,1 packet
has an actual lower classical time and a whole-packet upper classical time
proportional to epsilon/V, with actual positive field/density bounds and
evolved matter speed strictly below Vmax on every existing interval.

Primary self-review verdict: **correct only after the stated parameter and
domain restriction**. The stronger unconditional finite-speed implication
is not claimed. An independent reviewer must pin the frozen proof and result.

Dependency chain:

- Fixed compatible Q/scale/isothermal equations and exact chart (inherited
  pinned derivations, reconstructed in Section 2).
- Internal local characteristic start/restart (FGF051 Section 4) plus fresh
  derivative scaling P=Uv/delta and C1,1 trace (Section 3).
- Background-speed cone uniqueness with full unknown-gradient term, explicit
  collar radius, and open compatible gluing (Section 4).
- Centered pressure invariants -> uniform-in-width positive density -> actual
  complete field-source bound -> strict chart and evolved speed margin
  (Section 5; no circular use of a future lifespan).
- Full pressure/field momentum conservation and transfer -> strict capacity
  contradiction with coefficient B>15/2 (Section 6).
- Shared-domain maximal germ and inactive cap (Section 7).

Obligation matrix:

| Obligation | Result | Evidence |
|---|---|---|
| All ten task source pins checked before use | Passed | input_pins.json; replay verifier |
| Fixed units and epsilon-independent coefficients | Passed | Section 2; no v0 substitution |
| Positive c and exact polynomial C1,1 joins | Passed | Sections 2--3 |
| Lower existence includes higher seminorm and trace | Passed | (3.3)--(3.4), pinned local iteration |
| Collar time/space margin | Passed | eta>0, radii 1-eta/4 and 3eta/4 |
| Unknown speed is not quietly bounded by S | Passed | comparison uses H speeds and U_X coefficient |
| Q and scale compatibility and gauges | Passed | Section 2 and open collar gluing |
| No pressure or density-source deletion | Passed | (2.3), (5.1)--(5.3), (6.1)--(6.3) |
| Actual evolved speed and density | Passed | (5.2), (5.4)--(5.5) |
| Full time interval is not assumed to exist | Passed | bounds restricted to existing branches |
| Capacity coefficient and transfer order | Passed | 16/15 B-8; transfer O(delta^3) |
| Explicit positive width threshold | Passed | (6.6) with strict state/domain inequalities |
| Same germ, lower/upper and inactive cap | Passed | Section 7 |
| Energy, both field fluxes, pressure stress | Passed | (6.1), (7.1), moving-boundary identities |
| Hydrostatic control | Passed | V=0 is treated separately, no division by zero |
| Physical population of conditional cell | Not established | coefficient/background evidence absent |
| General finite-V upper bound below threshold | Incomplete | exact stationary-moment obstruction in Section 8 |
| Shock type, physical closure, evolving reference | Out of scope | Section 8 |

Pressure-invariant signs were checked with rtilde,stilde having identical
source -g. Their common interval implies |q-q*|<=Uv/(2c)+Deltav/c and
|v|<=Uv+Deltav; the factor 1/2 in the density exponent is intentional.
Field momentum signs were reconstructed directly: mf_t+Sf_X=ng, while
the fluid has -ng. The hydrostatic pressure stress cancels the background
field stress at the endpoints rather than vanishing separately.

The moment threshold was recomputed algebraically with symmetric radius a:
(8/15)B>a^2 and SB/Uv<a-1; a^2/(a-1)>=4. This is an exact analytic check,
not a mathematical executable computation or a sharp PDE threshold claim.

Conservative mathematical proofreading skill applied in self-review mode to
the complete new DERIVATION.md and companion notes. Routine edits: symbol
separation B_Q versus horizon B and explicit physical/dimensionless speed
conventions. Mathematical-token typo changes after drafting: none. No
unresolved syntax/notation issue identified. This self-review does not
replace the separate requested audit. No external-source theorem leaf exists.
