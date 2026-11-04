# NV1 Amendment A2, 2026-11-04: POST-CONTROL, before any real fit

Written after reading `nv1_controls.out`. No real fit, gate or card has been computed.

The controls script printed "E2 controls FAILED". The cause is a check I added in the code that the frozen text does not contain: a **reverse** comparison on the S card (every row the plain law computes on S must also be computed by the zero-weight E2 rule). It fails by construction. The plain law computes rows the E2 loader cannot reach at all: A11 (law-only AQUAL cache), the Milky Way and DiskMass rows, the old gates (A20-A26, B2) and the planets' block calls without a name or with NaN gas. Those rows are NOT COMPUTABLE for any E2 rule, as frozen (candidate loader: "anything else ... NaN, RQ3 reads NOT COMPUTABLE").

Every control as frozen passes, on both footings:
1. Known answer: X-COP +0.4675 (35 rows), LITTLE THINGS −0.0252.
2. Zero-weight E2 rule: on U, the 8 rows it computes match RQ3's law card (0 mismatches; the other 88 are NOT COMPUTABLE, the SPARC block through DDO064 and UGC03546); on S, the 18 rows it computes match the plain law on the same S card (0 mismatches).
3. Checker: planted bump flagged (2677 violations), zero rule clean.
4. Admissible plant: converged, checker clean, gates 3-4 pass (G3 SPARC 0.123 / 0.196, G4 −0.001).
5. Planted non-local boost: true E recovers dm/dE 0.168 against the planted 0.176 and passes gates 3-4; shuffled E fails gate 1 and gate 3 (X-COP +0.30-0.31) and its SPARC-even rms is 0.145 against 0.121 (ratio 0.83 ≤ 0.85).

**Change:** the control flag used by `real` is recomputed as frozen (controls 1-5 above, control 2 forward only). The reverse S comparison stays in `nv1_controls.json` (`S_rev`), reported, not gated; the printed "FAILED" is kept in `nv1_controls.out` and the as-run flag is stored as `ok_as_run`. Nothing else changes.

κ = ½ FITTED; not theory closed.
