# SD1 intake: candidate preserved, narrow algebra checked, independent audit required

Origin: existing Astra agent `/root/dynamics_precision`; this was not a
DeepSeek execution. Parent: stage-three DP1. Received 2026-09-27. Raw artifacts
remain in `campaign_fresh_gravity_astra/stage_04/scale_dynamics/`.
Exact hashes and validated manifest are pinned by the companion intake receipt.

The coordinator read the raw derivation and report and independently reran the
manifest validator, which passed. This checks file/command provenance, not the
complete numerical implementation. The worker reports 21 passing finite
checks; the coordinator has not independently reproduced its nonlinear solver.

## Algebra checked by the coordinator

With W=a²w(g/a), differentiation at fixed g gives a W_a=2W-gb.
Hence T=-aW_a=gb-2W, T_g=g b_g-b=q, and b_chi=-q for a=a_ref exp(chi).
The chi action variation yields J chi_tt/v_chi²-J Laplacian chi+U'=T.
Its energy source +T chi_t/(4piG) cancels the gravitational source
-T chi_t/(4piG). These signs follow directly from the displayed action.

At equilibrium U'=T and with U=S0(cosh(2chi)-1)/4, the field Schur quantity is

    U''-2T+gq-q²/b_g
      = S0 exp(-2chi)+q(g-q/b_g)
      = S0 exp(-2chi)+Bq/b_g.

For positive B, b_g and q this is positive. This is a field-sector quadratic
claim on the stated uniform-gradient source-free background. It is not
responsive-matter or global stability.

The core-vacuum mismatch is substantive. If rho_Lambda is pointwise constant
and the actual local a obeys the core relation, chi cannot vary. But a uniform
static chi requires the same U' at locations where T varies with field
magnitude. The illustrative construction therefore changes the literal scale
interpretation. Calling a_ref a vacuum scale does not by itself repair that.

If the added potential alone is identified with rho_Lambda c², the pointwise
core identity forces U_total=4pi a_ref² exp(2chi)/kappa². Its derivative cannot
vanish at a finite positive vacuum. This conclusion is conditional on that
canonical action and potential-only identification; it is not a no-go for all
scale sectors or the user's entire framework.

## Disposition

`candidate_received; provenance_validated; narrow_algebra_checked`.
No empirical acceptance, no historical novelty claim, no promotion of the
environmental scale modification into the user's accepted framework. The raw
candidate is sufficient input for an independent audit, so FGF-010 can be
released specifically as an audit task with exact hashes. A downstream task
that assumes the full candidate true still requires its own acceptance gate.

The outer-boundary and coupled scale-fluid proposals remain possible
continuations. The independent audit should precede adopting their premises.
