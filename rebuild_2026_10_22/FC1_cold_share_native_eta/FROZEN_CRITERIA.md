# FC1_cold_share_native_eta: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** X48's zooms evolve all of Ω_m as collisionless dust (`rhom = Om ...`, each particle one cell of the mean total density), and X43's Σ_coll uses the same total ρ_m. So η_native Σ_coll(M) read from them (X77, X81, CE1) is the surface density of **total matter** in a halo of **total mass** M. The grader uses that number as the surface density of the **cold** halo alone and then adds the baryons on top (SPARC `GB + Mh`; clusters `Mb + Mh`; X43/X73 `solve_r0(Mfair, rta, s)`). Does converting to the cold share remove CE1's failure?

**Rule, no free parameter.**

S_cold(M_cold) = max( Σ_a0 , f_c η_conv(M_t) Σ_coll(M_t) ), with M_t = M_cold / f_c and f_c = R_nat / (1 + R_nat)

- R_nat = NAT_RRAT = (Ω_m − Ω_b)/Ω_b from the native background already in X73 (0.2976016, h 0.6856427, ω_b 0.0223081), which gives f_c ≈ 0.8406. It is not fitted, and no other value is tried for grading.
- SPARC and groups convert both S and the mass argument. Clusters already pass total mass (`Mfair + Mb`), so only S changes there.
- η_conv is CE1's committed table, median and 68 % ends, unchanged. The floor is unchanged.
- The cold fluid stays in the same shape, so at fixed total a halo keeps the zoom's r₀: scaling M and S together leaves `solve_r0` unchanged.

**Origin of the idea, stated plainly.** I noticed this after CE1, SH1, CL5 and BH1 had shown a required softening of 0.81–0.85 at every mass. It is post-hoc in origin. It is not blind. Its protection is that it has no knob: 1 − Ω_b/Ω_m was fixed before any of those lanes, and the record's grep finds no earlier treatment of this factor in these lanes.

## Grade (X74's grader text unchanged except the two conversions above)
Canonical is the primary footing. Alt runs the same way and is reported under its own label; X78 already traces its SPARC failure to the law.

Runs: f★ 0.034 and 0.0615, each at CE1's median table and at its p16 and p84 tables.

- **COLD-SHARE PASS:** all grader lines pass (SPARC line on both backgrounds, groups, 15 cluster keys in both h cells) at median, p16 and p84, at both f★.
- **KNIFE EDGE:** the median passes at both f★, and at least one end fails.
- **F★-DEPENDENT:** the median passes at one f★ only.
- **COLD-SHARE FAIL:** the median fails at both f★. List the failing keys and their direction.

Cluster inputs stay at ng 48 until A4. The label carries that qualifier, and the same grade is rerun on CE1's A4 tables when they exist. If the A4 label differs, A4's stands.

## Reported, not graded
1. Factor on S only, without the mass-argument conversion.
2. LS1's table by V_flat (median Υ, ΔV at Υ 0.50), both footings, with ET1's S_need intervals.
3. Milky Way (X79's text with this rule), both footings.
4. KiDS (X79's text, η scaled; the mass-argument conversion is not applied there and hardly matters beyond 100 kpc).

## Checks (any failure makes the verdict NOT DECIDED)
- **K1:** factor 1 and no mass conversion reproduce CE1's committed SPARC rms and median Υ and its cluster predictions, both footings, f★ 0.034, max |d| ≤ 1e-9.
- **K2:** `solve_r0(f_c M, R, f_c S)` equals `solve_r0(M, R, S)` to 1e-9 at three masses.
- **K3:** the grader's printed η at 10¹², 10¹³, 10¹⁴ equals f_c × CE1's table within 1e-3 in the mass-converted run's own factor (checked at the nodes of the η table).
- **K4:** background A's own cold share (1 − fb) agrees with f_c within 0.01, printed. Zoom code uses total Ω_m, verified by reading `x48_zoom.py`, quoted in the README.
- **MUTATE:** factor 0.5 must raise SPARC median Υ and lower the G-IN-Mall prediction, compared with the graded run.

## What this cannot show
- The baryons are dust in the zooms. Gas that stays hot and extended would let the cold fluid expand further. Baryons that condense would contract it (X39: full Blumenthal contraction breaks SPARC). Neither is in this rule, and neither is excluded by a pass.
- The floor physics is not in the zooms. The floor remains by hand.
- It does not address KiDS's halo-mass gap, the Milky Way, dwarfs, or the alt footing unless the reported lines show otherwise.
- A pass would remove the need for a cluster softening source at this level. It would not derive κ, and it would not show the data favour the framework.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. Not theory closed.
