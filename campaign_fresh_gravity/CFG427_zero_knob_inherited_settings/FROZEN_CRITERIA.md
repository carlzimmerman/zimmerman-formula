# CFG427 FROZEN CRITERIA: does the zero-knob growth fix depend on the two inherited settings? (256³)
(owner 2026-10-07: "launch more". Committed before any run.)

CFG424's rule has no tuned radius or catchment. Two settings are inherited from the engine lineage, not tuned here:
- the T1 switch width ε = 0.077;
- the MIX-A gas-phase filter (cool 0.28 / hot 0.54 / collapsed 0.18).

This lane varies each one.

**Engine.** cfg424_pm.py, RC = 0, f_ret ≡ 1, canonical, seed 359. The engine gains a CFG424_EPS environment option; the default is unchanged.

**Runs.**
- E1: ε = 0.0385 (half);
- E2: ε = 0.154 (double);
- G1: the MIX-B filter (cool 0.57 / hot 0.25 / collapsed 0.18);
- G2: HOT1 (all gas hot, the extreme filter).

**Decision (CFG361 cuts, vs CFG359 S0).**
- **INSENSITIVE:** all four are GROWTH OK. Neither inherited setting is needed for the pass.
- **SENSITIVE (named):** a run fails, and the setting that breaks it is named.

**Reported:** the spread of max|P−1| against CFG424-canonical (0.027).
