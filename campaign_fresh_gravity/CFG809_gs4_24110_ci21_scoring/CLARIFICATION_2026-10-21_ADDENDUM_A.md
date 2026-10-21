# CFG809 clarification, addendum A (2026-10-21, later the same day; still before any programme 2025.1.01377.L data)

This addendum corrects one sentence of `CLARIFICATION_2026-10-21.md` (35ea5e1be) and adds two readings. The earlier file is not
edited. The scoring rules of FROZEN_CRITERIA.md are unchanged.

## 1. Correction: A-G4's "stated now" sentence was wrong on most branches
`CLARIFICATION_2026-10-21.md` said, under A-G4, that with CFG572's routes fixed:
- the framework's verdict is NOT ROBUST for every CI21 value;
- so this disc can neither support nor disfavour the framework;
- only the rivals' FLOOR tension can come out ROBUST.

That sentence generalised the CFG942 10-20 scan, which covered one branch only: canonical, M★ 10.89, R_g = R_d. The full scan of all
eight M★ × gas-shape × footing branches (CFG942 harness, 826ebb739, MOCK) shows it does not hold in general:
- On the six branches where the framework is not FLOOR (M★ 10.76, both shapes and footings; M★ 10.89 with R_g = 1.5 R_d), F-DESI and/or
  F-flat read ROBUST at 15–17 of 20 CI21 values.
- On the alt footing at M★ 10.89 (both shapes), the framework's F-flat is FLOOR, and its FLOOR tension is ROBUST at every CI21 value.

**Corrected statement (governs from now):** the per-model ROBUST rule stands as decided. On most branches the framework's
verdict CAN come out ROBUST. A ROBUST verdict can be either wording: "consistent with" or "in tension with", including a robust
FLOOR tension for F-flat on the alt footing at M★ 10.89. Either way it is a single-disc demonstration and never an exclusion. Only
on the canonical, M★ 10.89, R_g = R_d branch is the framework NOT ROBUST at every CI21 value. The harness prints this per-branch
statement in place of the withdrawn sentence.

## 2. MUTATE continuum (new reading; A-G11 context)
In MUTATE, the continuum for the shifted window is the median of the channels that are line-free relative to BOTH the shifted
window and the true line. Channels within ±600 km/s of z = 1.9975 are excluded from it. Reason: the frozen text calls for
"line-free channels", and the true line channels are not line-free. Including them over-subtracts and makes the control easier to
pass. The bite criterion (the shifted flux below 3σ) is unchanged.

The +1000 km/s fallback (A-G11) can itself fall outside a 1.875 GHz window centred on 270 GHz. In that case MUTATE reports NOT
RUNNABLE (exit 2) and the run says it has no MUTATE control. The record holds no window edges to check this in advance.

## 3. Items of the clarification the harness must still print (not new decisions)
These were decided in `CLARIFICATION_2026-10-21.md` but are not yet implemented:
- A-G1: the ±0.1 dex information line.
- A-G16: after a G1 failure, the continuum is measured in the R_e circle, not the noise mask.
- A-G4: the other CFG572 branches shown in the score table.
- CFG806-U4: A-X3 (CFG571's Δ_m on M_bar, information) and A-U17 (the ~10% C2 false-failure note beside a C2 failure).

κ = ½ fitted; footings never pooled; cold energy mass required; not theory closed.
