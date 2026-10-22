# FGF047 report

Outcome: supports_scoped_claim, pending independent review.

For every fixed finite N satisfying the inherited support gate, the exact
compact C1,1 velocity and hydrostatic field/density data admit a positive-time
local classical solution of the actual one-dimensional diagnostic Q/scale/
isothermal-fluid equations on a regular positive-gradient patch. DERIVATION.md
constructs it directly, including the field response; no general PDE existence
theorem is imported.

The two Q coordinates are phi_t±h(g,chi), h_g=sqrt(B_g/tau). Their equations
retain B_chi k/tau and both induced h_chi(w∓b k) terms. Two scale-wave
coordinates and a zero-speed chi coordinate complete the diagonal system.
Coincident block speeds do not remove the coordinate basis. The characteristic
iteration preserves uniform first-derivative and Lipschitz-gradient bounds;
C0 contraction plus explicit interpolation gives a spacetime C1 limit. Its
same-point distance from initial data stays in a chosen coefficient box,
propagating g>=g_-/2 and positive density/scale bounds. Compatibility follows
from time-integrated k_t=w_x and g_t=phi_tx, then reconstructs C2 fields.
Backward cones remain strictly in the physical patch, and local uniqueness
removes exterior-extension dependence on common characteristic domains.

The local energy contains matter, n phi interaction, both field kinetic
terms, W, the scale gradient term, and U. The Q and scale fluxes are
-phi_t B/C and -J chi_t chi_x/C; exchanges +n phi_t, -n phi_t-T chi_t/C,
and +T chi_t/C cancel. Moving intervals retain their boundary terms. The
zero-velocity hydrostatic control solves every equation and has zero flux.

The guaranteed time is explicit in actual normalized data/coefficient norms
and the state-chart margin. No large-N exponent, fixed-force breakdown,
shock, crossing, wall, global solution or physical theory completion is
claimed. Both dimensional a0 backgrounds and fixed versus evolving reference
histories remain distinct. Dynamic chi does not establish the physical
pointwise vacuum-scale relation or the required two gravitational DOF.

## Provenance and review

All nine task ancestry pins matched. FGF046 author text was initially read
before the pin check; proof development followed the successful check.
No new stage34 proof or reviewer files were read. Primary AS ownership was
reported distinct by the coordinator and was not touched. Writes are confined
to this run directory. There were zero mathematical executable computations,
no network, installations, service launches, commits, numerical tests or
observational runs. Commands in result.json are empty under the proof-only
exception; metadata reads/hashing/writes are administrative, not experiments.

Proof-audit author self-review verdict: proved as written for the exact local
claim. The dependency graph and obligation matrix are in DERIVATION.md.
Independent review and orchestrator acceptance remain outstanding.

Mathematical proofreading used mathbox:proofread-math in self-review mode on
the complete newly authored derivation and this report. Routine edits: none.
Mathematical-token changes: none. Unresolved proofreading issues: none.
Validation is the administrative hash/JSON check recorded in result.json;
no typesetting compilation applies to these Markdown artifacts.

The next substantive mathematical question is whether the fixed-force
compressive mechanism survives evolving Q/scale feedback. The present result
supplies its local branch but no feedback estimates or upper lifespan bound.
