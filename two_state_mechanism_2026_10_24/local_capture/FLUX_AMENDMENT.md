# Incoming-flux correction before final interpretation

Versions 1–3 conserve collision energy/momentum and invert their impulses
exactly. That is not by itself a phase-space detailed-balance check. If the
normal speeds are a before and b after, the speed-map Jacobian is a/b.
Collision flux a da = b db is preserved, whereas a velocity-independent
encounter rate does not supply that factor. Treat those transport runs as
exploratory and do not infer physical state selection from them.

Version 4 retains the calibrated v3 circulation statistic and adds incoming
normal speed to the reaction hazard:

    gamma = 10 sqrt(G rho_b) |vnormal| / vref,
    vref = sqrt(G M_b,neighbors / h).

All factors except |vnormal| depend only on positions and masses; they agree
under the reverse event. The baryon partner proposal weights also depend only
on positions. The flux measure is therefore correct for this central normal-
speed map in the continuous-time encounter limit. This is not a derivation of
the cross section or a claim of full microscopic detailed balance: internal
state degeneracies, finite-time multiple events and omitted degrees of freedom
remain assumptions. Test half the event interval to expose discretization.

The positive receiver for baryon cooling is unchanged and is explicitly
irreversible. Corrected runs are labeled run_*_v4; do not pool versions.
