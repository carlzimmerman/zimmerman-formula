# CC10 four-state continuum response contract

Base shared checkpoint fd417eea045a0b6259b8efff5e20ca62a2e14f7e. Own scope is
`memory/` only. Fixed e=.003, mu=2e6 GeV, xi=.02 leading pole packet.

The first finite assertion is the period-averaged, weak-source neutral
four-state response on the **recorded harmonic late orbits**, integrated
against the recorded cell-constant charged scalar distributions and isotropic
pair angles. Production Gram and absorptive neutral matrices are the actual
tree packet. This compares stationary local inverse response with the periodic
retarded response, with delayed neutral occupation and neutral decay exits.
It also computes the charged continuum characteristic function rather than
identifying correlation time with neutral lifetime.

Routes: (1) Floquet sideband continuum response (first uncertain bridge:
linearization of pair detuning on the recorded tiny orbit); (2) direct complex
ODE response, independently checking Floquet normalization and finite-time
transients; (3) passive-matrix energy bound, checking what can be said without
an uncontrolled local collision reduction. Start with (1), then use (2) for
load-bearing controls. A full in-medium charged retarded self-energy and
occupied/inverse baths are excluded from the first model, and must remain
explicit limitations. The charged incoming width omission is measured against
the existing static fully resummed packet.

Use endpoints Tc=1e-5 and 1e-6 with exact recorded fS. Interior late-window
points may use explicitly labeled log-interpolation of endpoint shapes;
they are not recorded intermediate distributions. Cell occupations remain
constant within each radial cell; numerical quadrature is varied within cells.
No ultraviolet continuum model or thermal mass is invented.

Every finite run uses a new v2 record, one numerical thread, wall<=240s,
CPU<=235s, measured RSS; no address-space or affinity limit. Inputs include
script and exact data closure. No Git mutation, prior-scope edits, installation,
queue, portal, or external message. Finite controls do not establish a coupled
cosmological history, matched mass spectrum, or global trapping claim.
