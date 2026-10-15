# CFG780: structure growth when cold mass converts to dark energy (the PAPER50 surviving branch)

If black holes convert cold mass into dark energy (the cold-only partition that the FRBs allow, PAPER50), late-time growth
changes. Rescoring the 1024³ runs against raw KiDS:

| run | as published | with cold-only conversion (survival 0.894) | half the amount | proportional split |
|---|---|---|---|---|
| T1x canonical | χ² 136.56 (Δχ² vs control −7.70) | 141.23 (+4.66, WORSENS); still CONSISTENT (−3.03 vs control) | 138.78 (NEUTRAL; −5.49) | 141.23 (WORSENS; −3.03) |
| T12 | 146.29 (+2.03) | 152.56 (+6.27, WORSENS); TENSION (+8.30) | — | — |

**Reading:** converting the cold mass costs about 60% of T1x's KiDS gain, but T1x stays consistent and better than the
control. The black-hole-to-dark-energy branch is therefore tolerated by the raw shear data, not favoured.

**First run was buggy:** a missing flatness constant and late-binding closures; it is kept as `cfg780_firstrun_BUGGY.log`.
After the fix: K1 (zero conversion g = 1 to 1e-9) PASS; K2 (growth shape, 0.3%) PASS; the rescore reproduces the stored χ²;
MUTATE outputs are separate.

κ fitted; not theory closed.
