# COOL1_cooling_threshold: FROZEN CRITERIA (committed alone, before any script or number)

κ = ½ FITTED (unused in the cold branch). Footings never pooled. Cold dark energy is a gravitating w ≈ 0 field component, never a particle. Not theory closed. Nothing here says the data favour the framework. Source of the idea: an outside AI's scrambled text (QUEUE_ROADMAP_2026-11-01 item 9); treated as a claim to test.

## Record check (done before this file)
- No lane derives PAPER64's T from cooling. T is "located by data" (PAPER64 §"What is fitted"); "T from L" was withdrawn (CSM1).
- Nearby, none the same door: MF1 (H2, lg M_f, not derived; the gas-density assumption decided it); CFG934 (T_vir = 1e4 K floor, PARTIAL); CFG930 (energy ordering inverted); CFG640 and CFG369/370 (t_cool = r/V as a split or gate inside a run, on the law's V, not a threshold for T); CFG581 (hidden-gas t_cool); GT1 (gas-state rule on hot atmospheres: FAILS); LC1, UR1 (gas cooling contracts the cold fluid).
- PAPER64's T belongs to the switch picture. Working rule N (owner 10-31) has no such switch, so a derived T would feed PAPER64's picture, not N. Stated in the README whatever comes out.

## Question
Does t_cool(r_s) = t_dyn(r_s), with H-He cooling, virial temperature and the native background and baryon fraction, give the switch mass T ≈ 10^12.3? How much of the answer is input choice? Does it have anything to do with where a cold halo is absent?

## Target and its width (from the record, not from me)
- T is in M200c units from EM1's relation, summed over a basin (BS1), z = 0.
- Lower edge 12.19: LEE1 ("T ≳ 12.19"). Upper edge on the basin key 12.39: BS1, LG's log M_basin 12.3925 must exceed T. **W = [12.19, 12.39], width 0.20 dex.**
- Wider reading W' = [12.19, 12.6]: LEE1's mass-key box, top is the box edge, not a measured edge. Reported, not primary.
- T has a target on canonical only: LEE1's alt is 0/24 at every T.

## Rule, primary (no astrophysical input, fixed before any number)
For halo mass M = M200c at redshift z:
- R = R200c(M, z), V² = GM/R, T = μ m_p V²/(2k), μ = 0.59 (fully ionised H-He, CFG934's value).
- Isothermal gas: ρ_gas(r) = f_g M/(4π R r²), f_g = native f_b = 0.15685, X = 0.76, r_s = R. n's from CIE fractions.
- t_cool = (3/2) n k T / (n_e n_H Λ(T, Z)), t_dyn = r_s/V (the record's, CFG640).
- Λ, Z = 0: analytic collisional-ionisation-equilibrium H-He. Rates and cooling terms from Katz, Weinberg & Hernquist (1996) Tables 1-2, after Cen (1992) and Black (1981). PROVISIONAL: recalled published formulas, checked against the record's AtomDB value (K2). AtomDB files are not on disk now (`find` found none) and there is no new download.
- Λ, Z > 0: Λ_HHe + (Z/0.3)[Λ_TN − Λ_HHe]₊, Λ_TN = the record's Tozzi & Norman (2001) Z = 0.3 fit with CFG370's normalisation (CFG640's `lam_cool`). Linearity in Z is an approximation (lines scale with Z).
- **M_thr = the largest M with t_cool ≤ t_dyn.** Above it no mass cools by this criterion.
- Background: CFG654 A1 native set, h 0.67770, Ω_m 0.31040, Ω_r 9.106e-5, f_b 0.15685, flat.

## Which z, stated before computing
1. **z = 0:** T is a z = 0 mass of a z = 0 object (BS1's basin today). Row P0.
2. **Formation:** the core rule is set at collapse, so a cooling rule about halo presence belongs at formation. Row Pf: z_half(M0) from AE1's Lacey-Cole table on X43's σ(M) (1e10 1.33, 1e11 1.14, 1e12 0.94, 1e14 0.56), M at that epoch = M0/2. Reported as the z = 0 descendant mass M0: M0/2 = M_thr(z_half(M0)). Row Pfs: AE1's z(f_s), M = 0.1441 M0 (table 1e10 2.19, 1e11 1.89, 1e12 1.58, clamped above 1e12, disclosed).
Neither is chosen by landing. P0 and Pf are both primary; a split verdict is reported as split.

## Sensitivity runs (one at a time from P0 and from Pf; no scan for a landing)
- Z/Zsun: 0, 0.03, 0.1, 0.3, 1 (FREE: no native value; a real halo's gas has been enriched)
- f_g/f_b: 1, 0.5, 0.2 (FREE at 1e12: the native value is an upper bound, hot CGM mass is not measured here)
- r_s/R: 1, 0.5, 0.3, 0.1 (FREE, set by the shock's location)
- z: 0, 0.5, 1, 2, 3, 4, instantaneous
- Density form: isothermal at r_s vs uniform ρ = f_g 200 ρ_c (Rees-Ostriker's sense)
- t_dyn: r/V vs free-fall (π/2√2) r/V
- Halo definition: M200c vs native Δ_vir (CFG934's table, reported converted to M200c by isothermal scaling)
- Shock form: Birnboim-Dekel stability. γ_eff > 10/7 (γ = 5/3) requires t_cool,post > 1.4 r_s/|u₁|, i.e. ρ₀ r_s Λ/(μ-free units) /u₀³ < 0.0126. Derive the coefficient in the script (K3). u₀ = √2 V, T₁ = 3 μ m_p u₀²/(16 k), ρ₁ = 4ρ₀, ρ₀ = isothermal f_g ρ at r_s.
- Spread: range of log M_thr over the FREE inputs Z, f_g, r_s (each one-at-a-time, and all at the corners), at fixed z; compared with W's 0.20 dex.

## Footings
- **Cold (halo) branch:** no a₀ enters V or T. The same number on both footings by construction; say so, it isn't a test. Background is one native set.
- **Law (no halo) branch:** below T PAPER64's system has no halo, so its gas sits in V⁴ = G a₀ f_b M, flat. Same gas, radius R200c (of the label M), a₀ today held flat, disclosed. Canonical 9.3603e-11, alt 1.1312e-10. This is the a₀ law, not the cold sector; it doesn't break the owner's 10-31 rule and it isn't a rule proposal. Reported to see whether the threshold depends on footing and whether the two branches agree.

## Labels (frozen)
Threshold, by row:
- **DERIVED** only if P0 and Pf both land in W and the free-input spread at fixed z is ≤ 0.20 dex.
- **CHOICE-DEPENDENT:** a primary row misses W, or spread > 0.20 dex, but some listed input set lands in W. Any such input set is reported as a choice.
- **NOT REACHED:** no listed input set lands in W.
Link: **LINK EXISTS** only if a stated rule or action in the record couples the gas's radiative state to the presence of the cold fluid, with the right sign. Otherwise **NO LINK**, and the missing link is named. An energy ledger is computed: radiated energy against the cold halo's binding energy at T, and the direct test against BS1's own membership: per-halo t_cool applied to MW (11.880), M31 (12.151), M33 (11.093), LMC (10.709) and the LG basin (12.3925).

Record pass lines (SPARC, keys, groups, X-COP, LITTLE THINGS): no rule is proposed unless the label is DERIVED and the link exists. T values in W are already covered by LEE1 and BS1's graded runs, so nothing is regraded here. If DERIVED, the regrade on N's terms is a separate frozen lane.

## Checks (failed check: no verdict)
- K1 Baseline: reproduce CFG934's M_cool(z = 0, T_vir 1e4 K, μ 0.59, Δ_vir 303.9) = 2.338e9 and z = 2, 5.792e8 within 0.2 % (constants differ slightly in the last place).
- K2 Λ(1 keV, Z = 0) within 15 % of CFG581's committed AtomDB value 8.917e-24; Λ(0.12 keV) Z=1/Z=0 within a factor 1.5 of CFG581's 30.1.
- K3 The 0.0126 coefficient re-derived in the script from γ_eff = 10/7, |d| < 1e-3 relative to (9/32)/22.4.
- K4 CIE fractions sum to 1 per element, at every T on the grid; ionised limit μ → 0.59 at 1e7 K within 1 %.
- K5 Direct t_cool/t_dyn at the solved M_thr = 1 within 1e-6.
- K6 Scaling: at fixed T, t_cool/t_dyn ∝ r_s/R and ∝ 1/f_g, to 1e-10.

## MUTATE
Λ/10, separate output (`_MUTATE`). Must move M_thr by > 0.3 dex in the primary, downward; else the threshold isn't reading Λ.

## Disclosure and expectation (not blind)
Rees-Ostriker and Birnboim-Dekel's ~1e12 is known, and so is T. A hand estimate was made before this file: at z = 0, Z = 0, r_s = R200 and fair-share gas, t_cool/t_dyn is about 40 at 2e12 M☉, so **I expect the primary to land near 1e11, about 1 dex under T**, and r_s ≈ 0.1 R with Z ≈ 0.3 to give about order 1 at 2e12. I expect CHOICE-DEPENDENT, with a free-input spread over 1 dex, and NO LINK: the record's only channel from cooling to the cold fluid is contraction (LC1), which raises its density, the wrong sign for absence; GT1's gas-state rule already failed; and the basin key is nonlocal while cooling is per halo.

Script `cool1.py`; runs in seconds, one thread, `nice -n 15`. Commit exact paths, local only.
