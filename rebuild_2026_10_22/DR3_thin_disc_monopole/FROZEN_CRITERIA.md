# DR3_thin_disc_monopole: FROZEN CRITERIA (committed alone, before any script or number)

**Source.** An outside text claims all response runs use spherical M_b(<r), and that the true monopole of a thin disc in the contraction, with the exact midplane force kept for stars, "cuts the 150-250 km/s pinch in half" with zero parameters. A claim under test; its "+18 %" and "half" are unverified.

**Question.** On NR3 MEDIAN's path, what do EM1 + Blumenthal and EM1 + Gnedin read when SPARC's contraction takes the true monopole of the disc instead of GB r²/G?

## Record check, done before this freeze
- **Force: nothing to add.** `q["GB"]` is built from SPARC's V_gas, V_disk, V_bul, which are thin-disc midplane forces from the measured profiles. The midplane "+18 %" for stars is already counted on SPARC.
- **Contraction:** CN1's path takes M_b = max-accumulated GB r²/G. That is not "spherical M_b" as the claim says and not the monopole either. For an exponential disc, GB r²/G is below the monopole inside about 1 R_d and above it from there out to many R_d. This arithmetic is from the Freeman formula, stated to be checked in K3; no SPARC grade seen.
- **No lane has tested this.** RM1's criteria name "disc geometry" only as one of the proposals its envelope f covers. It has no monopole run.
- **LC1:** its live disc is Miyamoto-Nagai a = R_d, b = 0.2 R_d. Its Blumenthal denominator is M_d [1 − a/√(r² + a²)], which is the Kuzmin disc's true monopole. So LC1's f_Q 0.872 is already measured against a monopole, and it is not the same factor as DR3's change. Its carry to SPARC (LC1's table) multiplied GB r²/G's response by a number measured against a monopole.
- **UR3:** DiskMass's M_b is also v² r/G; the Milky Way's is V_c² r/G, "spherical baryons BY HAND". UR3's stress: Blumenthal becomes FEASIBLE IN PRIORS at M_b × 0.7.
- Groups (Hernquist), clusters and X-COP (spherical gas) have no disc. LITTLE THINGS' M_b ∝ r² inside R is already a uniform disc's monopole. These don't change, which K5 checks.

## Rule (no new number)
M_b(<r) in the contraction = disc mass within cylindrical R = r + spherical bulge within r. GB stays the force in every fit. The cold mass stays spherical. No a₀ in the cold sector.
- **Stellar disc (primary):** Υ · 2π∫ SBdisk R dR, from SPARC's rotmod SBdisk on the rotmod radii, SB flat inside the first point. **Variant EXP (reported):** exponential with the table's Rdisk, same integrated light.
- **Bulge:** 1.4 Υ V_bul² r/G, which is its monopole.
- **Gas (primary):** rotmod has no gas surface density. Exponential disc of mass 1.33 M_HI whose HI surface density is 1 M☉/pc² at the table's RHI (root with RHI > 2 R_g; x = 2 where none; V_gas² r/G kept where RHI is 0; counts reported). This assumes a shape, BY HAND, no fitted number. **Variant GASKEPT (reported):** V_gas² r/G as now.
- Inside the first point and outside the last: CN1's rules unchanged (r², then log interpolation to the total over a factor 3).

## Runs, NR3 MEDIAN's inputs, canonical, f★ 0.034, both backgrounds
EM1 off; EM1 Blumenthal and Gnedin with DR3 off (baselines); **DR3 Blumenthal (primary), DR3 Gnedin (primary)**; variants EXP and GASKEPT, Blumenthal; DR3 Blumenthal × LC1's f_Q 0.872 applied as RM1 family G (reported: LC1 is on top of a monopole, one 1e12 number carried by hand).

## Pass lines (the record's)
SPARC rms ≤ 0.110 and Υ 0.50–0.80, both backgrounds; |tilt| ≤ 0.15; 15 keys |Z| ≤ 2 on measured gas +0.005; X-COP |mean| ≤ 0.05, rms ≤ 0.10; groups |Z| ≤ 2; LITTLE THINGS |median E| ≤ 0.10. Keys and X-COP cannot move here.

**The claim's own line, "half".** Gap to Υ 0.50 in the 150–200 and 200–250 bins, against the same mode's DR3-off row, cut by at least half in both bins and both backgrounds. On NR3's Blumenthal row (0.30, 0.365) that means Υ ≥ 0.40 and ≥ 0.4325. Grid floor 0.30 stated: the 150–200 bin sits on it, so its true gap may be larger.

## Labels (Blumenthal and Gnedin each)
- **SPARC SIDE CLEARS:** line, tilt, groups, LITTLE THINGS all pass. Not a whole pass.
- **HALVED, STILL FAILS:** the half line met, some gate fails.
- **NOT HALVED, MOVES:** either pinch bin moves ≥ 0.02 in either background, half line unmet.
- **NO MOVE:** otherwise.

## Reported, not graded
1. **Effective response** on SPARC: (Q_DR3 − 1)/(Q_off − 1) at r₀, and at 2, 3, 4 R_d, by V_flat bin, Υ 0.5.
2. **LC1 read-across.** On a 1e12 NFW start with LC1's M_d, R_d, Msim, c: Q from the Kuzmin monopole (reproduce LC1's Q Blumenthal), Q from v² r/G of the same disc. From these: what the live disc's f is relative to the rotation-mass formula, compared with DR3's ratio. Consistent means the DR3 ratio falls inside LC1's seed range after that conversion. If the Kuzmin Q doesn't reproduce within 5 % at 2, 3, 4 R_d, no read-across number is given.
3. **UR3, read across:** DiskMass (exponential monopoles of its stellar, atomic, molecular discs, UR3's bulge) and the Milky Way (monopole integrated from each cell's density), Blumenthal and Gnedin, on UR3's own lines. Doesn't enter the label.

## Checks; failed check, no verdict
K1 DR3 off: EM1 off and Blumenthal rows equal NR3 MEDIAN's in Υ, rms, tilt, bins, |d| ≤ 1e-6. K2 integrator on an exponential SB: 1 − (1+x)e⁻ˣ within 1e-3 at x 1, 2, 5. K3 Freeman: GB r²/G over monopole at x 0.5, 2.2, 5 stated; above 1 at 2.2 and 5, below 1 at 0.5. K4 SB integrated against L[3.6], median ratio within 15 % of 1. K5 keys' preds, X-COP, groups, LITTLE THINGS identical to the DR3-off row, |d| ≤ 1e-6. MUTATE monopole × 2 to separate output: Υ must move ≥ 0.02. UR3 read-across reproduces UR3's primary rows with the monopole switched off, |d| ≤ 1e-3.

## Limits
Spherical cold response is kept; a disc's real orbit-averaging isn't derived beyond the monopole, and LC1 is one mass. EM1 fitted. Core shape by hand. Gas shape by hand. Scale height ignored in the monopole, a small effect at r ≫ h.

**Not blind.** NR3, UR1, UR2, UR3, RM1, LC1 are read. RM1's G map at f 0.8 reads bins 0.32, 0.41 on NR1's anchors.

**Expectation on record, mine.** NOT HALVED, MOVES, for both modes. Monopole is about 25 % below GB r²/G through 2–5 R_d, effective response about 0.8–0.9, Blumenthal Υ about 0.38–0.40, bins about 0.32–0.35 and 0.40. DiskMass's r rises. The Milky Way's Blumenthal class may rise to FEASIBLE IN PRIORS, as UR3's × 0.7 stress suggests.

One thread, nice 15. κ = ½ FITTED, unused. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.
