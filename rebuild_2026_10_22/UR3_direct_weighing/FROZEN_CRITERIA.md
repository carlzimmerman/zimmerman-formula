# UR3_direct_weighing: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** UR2 leaves EM1 + response failing on one number, Υ about 0.30–0.35, worst at 150–250 km/s, while SPARC's line assumes 0.50–0.80 from stellar populations. Two weighings don't use that line: DiskMass's vertical dispersions and the Milky Way's star counts and K_z. Do they accept what the response asks for?

**The Υ line is not moved here.** UR1 and UR2 keep their fail whatever this finds. This asks whether the line's premise is under independent pressure, and it can come out against the response.

**Disclosed before the freeze. Not blind.**
- CFG576–578: at measured h_z every earlier model over-predicts σ_z: Newton r 1.494 at Υ_K 0.821, round rule 1.21–1.25 at 0.40–0.45. That front closed without a pass, read as a measured σ_z systematic from young tracers (Aniyan+16 type). h120: DiskMass sits 0.27 dex below population synthesis.
- RG1: native N on McMillan baryons V_c 202.8 against Eilers 229.1 ± 4.6, K_z 67.9, passes K_z. **My hand estimate, from McMillan's V_b 177 and K_z,b 62 with the halo term × 1.9: V_c near 225, K_z near 73, so V_c may rescue while K_z goes over.** That estimate is why the Milky Way is here.
- UR1's response at r₀, 150–250 km/s: 1.92.

**Expectation on record, mine.** DiskMass: r falls, about 1.1–1.25, because the halo takes more of the rotation; reaching 1 is possible but unlikely. Milky Way: V_c improves a lot and K_z fails high. Most likely reading: the response helps one and hurts the other.

## Common
UR1's path, NR1 PRIMARY's η, EM1 at δ 0 (+0.10 reported, per UR2), canonical, background A primary, B reported. Modes: off, Blumenthal (primary), Gnedin. No a₀ or κ enters any route E number. The S(M200) table comes from the grader's `sig_core`, written to JSON and read by both parts.

## Part A, DiskMass, 30 galaxies, same estimator as CFG576
At 1.5 h_R (primary) and 2.2 h_R: find Υ_K where g_bar(Υ_K) + g_c(R; Υ_K) = V_rot²/R, CFG576's tanh curve and its g_bar. M200 from EM1 with lg M_b at Υ_K = 0.5 plus gas, **BY HAND** (K to 3.6 µm taken as 1; ±0.1 dex on lg M_b reported). Contraction uses the baryons at that Υ_K. σ_pred² = π G k h_z Σ B, k 1.5, B = 1 + g_c h_z / (R K_N), CFG576's RM form with g_c replacing the phantom term.
- All 30 kept. Fewer than 27 fitted: NOT DECIDED.
- **REACHED:** median r in [0.90, 1.10] at 1.5 h_R. **NOT REACHED** otherwise, with r and Υ_K stated.
- A pass is conditional: a young-tracer systematic would move σ_z up and r down, so r 1 at DMS's σ_z is not agreement with an old-population σ_z. CFG577's Jeans integral raises r by 5–7 %: reported as a stated shift, not applied. The G-cal window is not reused.

## Part B, Milky Way, GD3/RG1's grader
McMillan and the X5 box cells, halo term contracted. Baryons are spherical in the response, M_b(<r) = V_b²r/G from the plane speeds: **BY HAND**. Lines unchanged: V_c |−229.1| ≤ 9.2 and within 2σ of Eilers, K_z χ², K_z(R₀) 66.4 ± 4.4, Oort/outer χ², through `classify`. McMillan stays marked ΛCDM-PROCESSED. Box classes: FEASIBLE IN PRIORS, WIDE PRIORS ONLY, or infeasible as RG1 words them.

## Overall reading (Blumenthal)
- **BOTH WEIGHINGS ACCEPT:** A REACHED and B feasible. Then Υ near 0.3 has two independent supports and the conflict is with population synthesis. Still not a pass of anything.
- **SPLIT:** one of them. Name it.
- **NEITHER:** response refused at 150–250 km/s independently of SPARC's line.

## Checks
K1 Part A estimator, no halo: CFG576's Newton r 1.494 and Υ_K 0.821, |d| ≤ 0.002. K2 Part A mode off, g_c = 0 and no response code path differences: M0 passes through unchanged. K3 Part B mode off at RG1's own S table reproduces RG1's McMillan V_c 202.8 and K_z 67.9, |d| ≤ 0.1. K4 contraction identity with M_b 0. MUTATE: M_b × 2 in the response moves Υ_K and K_z.

Inherits NR1's ANCHOR-DEPENDENT low masses, though these galaxies are mostly above them. NR2 unread. One thread, nice 15, under 1 GB. κ = ½ FITTED, unused in route E. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.
