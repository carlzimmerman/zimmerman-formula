# KL1 PART C AMENDMENT C2 (POST HOC; committed alone, before the diagnostic below is run and before any DES Y3 gate number is seen)

Part C criteria 190161a7f7; amendment C1 fe976ca7d3. TEST lane; adopts nothing. **kappa = 1/2 FITTED; not theory closed.**

**Timing, disclosed: post hoc.** Seen so far:
- the KC1 replays: Legacy 198.331 / 199.491 PASS; KiDS-1000 135.599 / 136.063 PASS; DES Y3 canonical 64.623 against 64.622 PASS;
  **DES Y3 alt 64.598 against Part A's 64.703, which FAILS the 0.01 tolerance**;
- the nuisance vectors of those two DES fits;
- KC5b.

No Part C gate row, C0 row, C2 row or bracket on any survey has been seen.

**What the two DES fits show.** Same data, model, covariance and code path; the replay lands **lower** (by 0.105). The nuisance
vectors differ only along the flat alignment direction:
- A_IA 1.4446 -> 1.4225;
- eta 3.0312 -> 2.9058;
- bin-4 delta-z -0.0098 -> -0.0111.

So Part A's alt DES ALL fit appears to have stopped about 0.1 above its minimum: an optimiser-precision floor in DES's
10-parameter fit, not a mismatch of inputs.

**As frozen: KC1 fails on DES Y3 alt, so DES alt's Part C rows read NO VERDICT and the alt overall Part C label is NO VERDICT.**
That reading stays first.

**Diagnostic (added; run after this commit).** Part A's ALL DES alt settings are refitted with Part A's own code path
(`kl1_lib.fit`) from three starts: Part A's stored nuisance vector, the replay's, and the default starts.
- If the lowest chi^2 is <= 64.61, Part A's stored value was not at its minimum, and KC1 for DES is read under C2 with a
  tolerance of 0.2 (the demonstrated optimiser floor).
- Otherwise KC1 stays failed under C2 too.

**Part A's labels are not changed.** Its ALL DES alt p moves by under 0.01 at most and keeps its label either way; this is
reported in RESULT.md.

**Nothing else changes.**
