# X69_split_vs_cored_nfw: FROZEN CRITERIA (committed alone, before any script or graded number)

**Source.** The external model's final-mile spec, Task 2 (relayed by the owner, 10-29). It asks for two zero-knob halo
shapes side by side, both with outer scale r_s = S r_c and S ≡ max(1, Σ_core/Σ_M). X68 ran T1-A once, on canonical
only and reported only (b1041ea643..99028a0bb8: groups Z +1.83, three inner keys OVER). This lane grades both shapes on
both footings, and adds X-COP hydrostatic masses.

**Standing:**
- κ = ½ FITTED. Footings never pooled. Not "theory closed". Nothing here may say the data favour the framework.
- Route E, Newtonian; cold dark energy is not matter.
- c_f = 4 (η = 14.83) EXTERNAL, not refit.
- S = Σ_core/Σ_M ties the outer halo to a₀. X68 rejected that choice for its own frozen hypothesis. It is run here
  because the spec asks for it, and the label says so.

## Hypotheses (everything else is X43, 00bc1a7950)

Σ_core = ρ₀ r_c = max(a₀/(2πG), η Σ_coll(M)), X43's rule. With x = r/r_c and r_s = S r_c:

- **T1-A, split Burkert:** ρ = Σ_core r_s² / ((r + r_c)(r² + r_s²)).
  M(r) = 4π Σ r_c² S²/(S²+1) [ln(1+x) + (S²/2) ln(1+x²/S²) − S arctan(x/S)]. At S = 1 this is X43's Burkert exactly.
- **T1-B, cored NFW:** ρ = Σ_core r_s² / ((r + r_c)(r + r_s)²).
  M(r) = 4π Σ r_c² S²/(S−1)² [ln(1+x) + (S²−2S) ln(1+x/S) − S(S−1) x/(x+S)].
  At S = 1 it is ρ = Σ r_c²/(r + r_c)³, with M = 4π Σ r_c² [ln(1+x) + 2/(1+x) − 1/(2(1+x)²) − 3/2].
  - The spec applies T1-B to every halo, so floor galaxies (S = 1) change shape too. That is graded as it stands.
- **Normalization:** r_c is solved so the mass inside X43's outer radius equals X43's mass (R200 for SPARC and groups,
  r_ta for clusters and X-COP). With no root, that halo FALLS BACK to X43's Burkert, and the fallback is counted.

## Harnesses (read-only)

- **Lensing, groups, SPARC:** X68's script (99028a0bb8), executed read-only up to its main loop. The X30 cluster shear
  stack carries the gas and stars. Bands: INNER, MID, and OUTER (1.42–3 Mpc).
- **X-COP hydrostatic masses:** HO1's grader (91cc5c3bd4), executed read-only up to its grade block, with X43's core
  rule substituted for CL2's. The baryons are X-COP's own measured gas and stars. Points sit at x = 0.1, 0.2, 0.3,
  0.5, 0.7 and 1.0 R500.
  - The committed grid stops at R500. The spec's R500–R200 band is not built here, so x = 1.0 is the outer point.

## Gate (per shape, per footing; the class needs both footings to agree)

- **G1, X-COP outer:** |mean Δ at x = 1.0 R500| ≤ 0.05 dex.
- **G2, lensing outskirts:** all MID and OUTER keys (G-MID-*, G-OUT-*; 13 keys) have |Z| ≤ 2 in both h cells.
- **G3, inner core not broken:**
  - G-IN-all and G-IN-Mall have |Z| ≤ 2 in both h cells;
  - the X-COP inner mean (x = 0.1, 0.2) has |Δ| no worse than the X43-Burkert baseline in the same harness by more than
    0.05 dex.
- **Verdicts:** **PASSES** = G1 ∧ G2 ∧ G3. **FAILS** = the list of failed gates, with sign. **UNDECIDED** = more than
  25 % of cluster cells or X-COP halos fall back.

**Reported, not graded:**
- SPARC rms and line on both backgrounds, and groups Z, for each shape;
- X-COP 35-point mean / rms and per-x table;
- the S distribution and fallbacks;
- every key's Z against X43.

## Checks (all must pass, else UNDECIDED, exit 1)

- **K0:** both harnesses reproduce their sources with the split off: X68's K0x43 (X43 exact), and HO1(a) with CL2's
  rule (mean −0.002, rms 0.126).
- **K1:** both closed forms match quadrature to 1e-6 at S = 1, 3, 10. T1-A at S = 1 equals X43's Burkert.
- **K2:** a solved r_c returns the target mass to 1e-8.
- **K3:** peak RSS < 2 GB, single thread. X48 A4 is live, so no heavy compute.

MUTATE: S → 2S (outer scale doubled), with separate outputs. It must change at least one cluster pred by more than
0.01, otherwise the harness is insensitive.
