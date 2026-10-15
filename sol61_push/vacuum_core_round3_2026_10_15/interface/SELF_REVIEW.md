# Interface control: evidence and exact limits

VC3-INTERFACE-001, 15 October 2026. The authoritative current-action statement
is `PROOF.md` together with `AMENDMENT.md`, checked by `check_interface_v2.py`
and `run_v2`. The frozen v1 run is historical: its Newtonian rho inertia
cannot be combined with the proof's full-current principal-inertia paragraph.
The amendment makes the consistent full-current kinetic convention explicit.

This construction gives actual global equilibrium existence and positive full
radial fluid/interface energy for the specified fixed-core control. Its
existence claim uses a strict finite-ball contraction, not a numerical ODE
profile. Its positivity claim uses a complete quadratic-form lower bound,
not sampled modes, fixed-wall substitutions or a homology matrix.

| Obligation | Evidence or limitation |
|---|---|
| Neutral finite-ball equilibrium with its own gravity | Volterra contraction, q<1/4500; positive density and pressure bounds |
| Count every held source | Compact prescribed central mass Mc and actual charge Q retained separately |
| Exterior independent of material frame | Maxwell action beyond a finite moving material edge, outside all prescribed sources |
| No uncounted pressure reservoir | Boundary load is derived from electric phase energy and an explicit area-energy wall |
| Wall rest energy and gravity | m_w=4pi sigma R^2/c^2; wall/core, wall/fluid and wall self-gravity included |
| Moving finite-density edge | Impermeable Lagrangian boundary, separately conserved neutral mass, explicit wall inertia |
| Radial gauge sector | Gauss fixes radial D; electric phase-boundary work retained; no monopole radiation degree omitted |
| Radial fluid/self-gravity | Full density force and perturbed self-force give the displayed radial operator |
| Positive full radial form | Exact Cauchy/Hardy bounds give C>39/5000 and the corrected positive inertia bound |
| Occupied principal gate | Uniform actual density and D bounds; smooth positive-density center patch |
| Charged-core force balance and motion | Not proved; the core is prescribed and held |
| Nonspherical interface/gauge modes | Not analyzed |
| Wall carrier, surface tension and EOS origin | Chosen continuum inputs |
| Relativistic gravity and junctions | Not proved; defined Newtonian rest-mass gravity/current-kinetic hybrid |
| Formation, abundance and observations | Not computed |

The independent `AUDIT.md` reconstructs the wall-shape/gravity terms, finite
edge mass bookkeeping and the amended full-current inertia. No additional
blocking mathematical issue was found within this restricted model.

The v2 bounded run passed 32 exact symbolic/rational checks. Its manifest
validates against the current bytes. There are no floating-point signs,
random trials or numerical shooting values in this evidence. Exact checks
audit the reductions and constants; the written existence and energy
arguments carry the uniform implications.

This control and the separate dynamical stiff-core atmosphere solve different
models. Their conclusions cannot be joined by putting one theorem's name
beside the other: a combined moving-core/moving-interface equilibrium and
one common energy must still be derived.
