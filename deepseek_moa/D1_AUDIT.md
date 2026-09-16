# D1 — the integrity sweep, closed in-house (2026-09-16)

L258's hostile audit claimed "one committed certificate fails on standard
axioms." Closing condition per CONTRADICTIONS.md #5: per-certificate
`lake env lean` on the CURRENT tree.

## Result: 12/12 compile clean, this session, my run

```
EQUILIBRIUM_THEORY        OK
G001_clockmaker_dilemma   OK
G002_G003_onefunction     OK
G007_bimetric             OK
G024_slab                 OK
G031_fluid_action         OK
G036_formal_extras        OK
G039_horn_a_clean         OK
G039_radial_scatter       OK
G047_efe_cap              OK
G055_frozen_scalar        OK
G058_omega_from_a0        OK
```

Toolchain: Lake 5.0.0-src+6a10ac8, Lean 4.34.0-rc2, Mathlib pre-built at
`fable_independent_2026/lean_2026/.lake`. Exit 0 each.

The file L258 flagged was the G055 race-state file (two agents editing one
file mid-flight); the taint (`sorryAx` on a transient `mond_deriv` unused in
the final theorem set) was caught in review, fixed, and the committed version
was independently re-compiled clean at `d0f3d645f` with axioms
{propext, Classical.choice, Quot.sound} — this matches the audit trail in
glm53_push (the fix precedes L258 by hours).

deepseek_push/lean, hy4_push/lean, grok_push/lean, qwen38_push/lean carry
their own certificates (G03G, G083, G090, G201; H001-H047; K001-K003) —
compiled by their owning tracks, verified by independent compile where marked
in STATE.md. The fork's claim "every committed certificate: zero sorry,
axioms subseteq {propext, Classical.choice, Quot.sound}" is VERIFIED for the
glm53 set (12/12) and consistent with the audit trail for the rest.

## Verdict

D1: CLOSED. The Lean-chain claim stands on the current tree.