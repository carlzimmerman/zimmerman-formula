# OD1_old_disc_ruler: frozen criteria (data-side audit of the disc-mass ruler, no new mechanism)

Written before any script of this lane and before reading any per-galaxy table of the new sources. **NOT BLIND.** Known to me when writing: every number in UR3, SP3, UL1, CFG576-578, and the search-snippet headlines of the sources below: MW K-giants 18.6 and 9.6 km/s against a single 13.0 km/s, "factor of 2" in surface density for NGC 628, V_max(bar)/V_max 0.76 ± 0.14 for NGC 6946. Owner's go, 2026-11-01. kappa = 1/2 FITTED. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework. FG1, UL1, SP3 and the 0.50 line are not edited or moved; changing the line stays the owner's decision.

## Question
SP3 and UL1 read the weighings as wanting the response on, with Υ near 0.3-0.4 at V >= 150 km/s, against the law's 0.46-0.75. DiskMass carries that reading, and it pairs a light-weighted σ_z, partly young stars, with the old stars' scale height. CFG578 named old-population σ_z as the next data. **If σ_z and h_z come from the same old population, are spiral discs light enough for the response, or heavy enough for the law?**

## Sources, closed list
c = σ_old / σ_single at the same place, where σ_single is the one-Gaussian dispersion DiskMass-type spectra read.
- S1 solar neighbourhood K-giants, arXiv:1511.06047
- S2 NGC 628, arXiv:1802.00465
- S3 NGC 6946, arXiv:2010.03991

Each source's own c is taken from its own stated dispersions. If a paper gives only a surface density ratio f at fixed h_z, c = sqrt(f). If a source states several radii, take its stated summary, else the median over radii. A source that gives neither is dropped and that is reported. **Fewer than 2 sources: NO VERDICT.** Each value carries a verbatim quote and where it was read. Values read through a summarising fetch are PROVISIONAL (standing rule) until seen in page text or TeX; the verdict carries [PROVISIONAL] if any c in use is unconfirmed. Other papers found on the way are reported only and don't enter c.

## Statistic
UR3's estimator (CFG576's table and one-zone K_VERT, 30 galaxies, 1.5 h_R, Υ_K fitted to each model's own in-plane speed):
r_old = r / c, since the model's σ with the old h_z must match σ_old = c σ_single. Models aren't refitted: the rotation curve sets Υ_K, and σ_z never enters the fit.
c_mid = median of the sources; c_lo, c_hi = lowest and highest source. Line: 0.90 <= r_old <= 1.10, n >= 27 (UR3's), the same width as before.

Rows, r read from record, not rerun except K1-K2:
| Group | Row | Record r |
|---|---|---|
| LAW | round rule, canonical / alt | CFG576 1.250 / 1.212 |
| LAW | phantom disc, canonical / alt | CFG576 1.475 / 1.475 |
| RESPONSE | hand EM1 Blumenthal | UR3 1.071, n 28 |
| RESPONSE | hand EM1 f_Q 0.872 | SP3 1.088, n 29 |
| RESPONSE | native total EM1 f_Q | SP3 1.080, n 28 at the most |
| RESPONSE | native FC1 EM1 f_Q | SP3 1.052 |
| RESPONSE | NFW c 8.0 f_Q | UL1 1.046, n 28 |
| OFF | hand EM1 off | UR3 1.365, n 30 |
| OFF | native total EM1 off | SP3 1.282 |
| OFF | NFW c 8.0 off | UL1 1.258, n 29 |
| REF | Newton, no halo | CFG576 1.494 |

Primary: all galaxies, so n and the line mean what they meant in UR3. Reported beside it where the per-galaxy r exists: V >= 150 km/s only, same labels, tag [V-DEPENDENT] if it differs.

Implied Υ: Υ_K,old = median per-galaxy (σ_old^2 / (π G K_VERT h_z B)) with gas removed, for B = 1 (Newton), 1.10 (round rule, CFG576), and to 3.6 μm with SP3's bracket K/3.6 = 1.0-1.3. Reported against 0.50 and against the response's 0.32-0.42. Not graded, because B is model-dependent.

## Stresses, reported, can only add tags
- Exact Jeans: r × 1.074 for round rule, × 1.052 for phantom disc (CFG577 / CFG576), × 1.05-1.07 for rows without their own number. [JEANS-DEPENDENT] if a primary row's IN or OUT flips.
- Measured edge-on thickness: S4G h_z / DMS h_z 1.146 (CFG578), r × 1.07. [HZ-DEPENDENT] if it flips.
- Fragility on record: seed range c200 6.25-9.63 from UL1 where it exists.

## Labels, on the group's primary rows: LAW = round rule, canonical; RESPONSE = native total EM1 f_Q and hand EM1 f_Q
- **HEAVY DISCS:** at c_lo, c_mid and c_hi the LAW row is IN, or above the line and closer to it than any RESPONSE row, and the RESPONSE rows are below 0.90. The response's low Υ does not survive same-population dispersions, and SP3's and UL1's reading of DiskMass falls with it.
- **LIGHT DISCS:** at c_lo, c_mid and c_hi both RESPONSE rows are IN and the LAW row is above 1.10. The 0.50 line would be in real trouble at these speeds, and the law with it.
- **NOT SEPARATED:** anything else, including a label that changes across c_lo to c_hi. Report which way c_mid leans, as a lean.
No label is a pass of anything. HEAVY DISCS doesn't confirm the law: the law keeps Milky Way, IC 1613, cluster failures. LIGHT DISCS doesn't rescue route E: tilt, LITTLE THINGS, keys, X-COP, IC 1613 and 60-150 km/s stand. Two external galaxies and one solar neighbourhood set c, carried across 30 others: that is a read-across, and the README must say so.

## Reported, no weight
- NGC 6946 direct: V_max(bar)/V_max against the rows' baryon share, and SPARC's own fitted Υ for NGC 6946 where a row dump exists. One galaxy, ±0.14.
- Whether either source's result assumed its own halo or gravity law on the way to its Σ.

## Checks (failed check: no verdict)
K1 no halo through UR3's code path: r 1.494, Υ_K 0.821.
K2 every record r above read from its file by script, not typed: |d| <= 0.0005 of the record's printed value.
K3 c from each source recomputed by script from the quoted numbers; quote stored in `sources.json`.
K4 bootstrap identity draw returns the full-sample median, for each row with per-galaxy r.
K5 injection: per-galaxy σ_meas replaced by σ_model / (c_inj × 1.0) for a known row, c_inj 1.3: r_old at c = c_inj returns 1 within 0.01.
K6 c = 1 returns the record's r exactly for every row.
MUTATE (`OD1_MUTATE=1`, separate outputs): (a) c × 1/c_mid, i.e. no correction, must not return the same label as the real run unless both are NOT SEPARATED, and must put RESPONSE rows IN; (b) group labels swapped, HEAVY and LIGHT must exchange or stay NOT SEPARATED; (c) one quoted source value × 3 must trip K3.

## Expectation on record
HEAVY DISCS 45 %, NOT SEPARATED 45 %, LIGHT DISCS 10 %. Reason, from the headlines above only: c near 1.4 sends r 1.08 to about 0.76 and r 1.25 to about 0.87, so the law's round rule also lands under the line at the top of c, and a low source could split the label. I expect this to weaken the lead that prompted it.
