# CFG809-GS4 (GS4_24110, programme 2025.1.01377.L, public 2026-11-28): clarification addendum E (2026-10-22; PRE-DATA; owner-approved; nothing frozen edited)

**Status.** Written and committed before any byte of either ALMA programme has been read. The owner approved it on 2026-10-22
("yes to all", in reply to a list that included "ALMA 'addendum E': adds n = 1 and n = 2 as labelled parallel readings"; relayed by
the doors-push coordinator). FROZEN_CRITERIA.md, the earlier clarification files and the seals are not edited. The same text is filed
in both plan directories (CFG806_u4_27928_scoring and CFG809_gs4_24110_ci21_scoring).

**Why.** The canonical law (THEORY_CANONICAL_2026-10-21_DRAFT §1: g_N = g²/(g + a0)) is the n = 1 law. Its ALMA prediction is sealed
(argon_push/AG4e_n1_alma_seal/SEALED_N1.json, sha256 9802de0d…), as is n = 2's (argon_push/AG4d_n2_alma_seal/SEALED_N2.json, sha256
d64727b5…). Until now the governing plans scored only CFG571's ν_mono seal, so neither sealed law form had a governing reading
(doors_push_2026_10_22/D4_alma_status, f81efdcf6).

## Ruling
1. **The verdict kernel stays ν_mono**, as sealed in CFG571 (259f7825c, be27457d…). Every verdict line of this plan is unchanged.
2. **n = 1 (AG4e) and n = 2 (AG4d) are scored as labelled parallel readings**, by the identical rules: §3–§5 of FROZEN_CRITERIA.md (966d50a87), CLARIFICATION_2026-10-21.md and its addenda A–D.
   Same gates, same measured quantities, same σ, same wording, same FLOOR rule, both footings (canonical 9.36e-11, alt 1.13e-10),
   every branch of the plan.
3. **Never pooled.** A parallel reading is never combined with ν_mono, with the other law form, with the other footing, or with the
   other disc (CFG806-U4). Each output line states its kernel.
4. **Requirements.** At the measured V_c (U4) or the sealed V_c 206 km/s (GS4) the requirement is computed with CFG571's head,
   executed read-only, with its kernel swapped to ν₁ = (1 + √(1 + 4/y))/2 (n = 1) or ν₂ = √(1 + 1/y) (n = 2), as AG4e/AG4d did.
   At the sealed grid points it must reproduce SEALED_N1.json / SEALED_N2.json exactly (checked in every run; a mismatch stops that
   kernel's reading).
5. **No law-form statement from GS4 alone.** Under CFG809 §4 every n = 1 vs n = 2 separation on GS4 is ≤ 0.51σ even with perfect
   data (D4_alma_status). A law-form reading is reported per disc and is a demonstration, never an exclusion.
6. **Canonical rows.** The canonical statement's §6 ALMA rows should quote the n = 1 requirement beside the ν_mono one.

κ = ½ FITTED; footings never pooled; cold energy mass required; one disc excludes no model; not theory closed.
