# X53_outer_lensing_law_vs_halos: KiDS-1000 isolated-lens lensing prefers the law's profile over route E's halos. Most of the gap is halo mass normalisation; the R200 edge adds about 60 in χ²

Criteria and ledger: `FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md` (61b837fcd4, committed alone). Result 64af8eb1cf.
`AMENDMENT_A1.md` is post-result and reported only. κ = ½ FITTED. Footings never pooled. Route E's halos are cold dark
energy, not matter. No dark-matter particle. Not "theory closed". Nothing here says the data favour the framework.

**Question.** Brouwer+21 KiDS-1000 isolated lenses (Fig. 3, 4 stellar-mass bins, 0.035–2.6 Mpc, released covariance).
Does the lensing separate (L), the law as fundamental (isolated AQUAL, μ = x/(1+x), phantom with no edge), from (H),
route E? In (H), gravity is Newtonian and cold dark energy sits in Burkert halos at the a₀/(2πG) floor (X38), with
M200 from EM1's SPARC relation, X43's collapse core, and a sharp cut at R200.
- Both models use the same lens baryons: F2's inventory with LePhare + 0.15 masses, cold gas and hot CGM, on the native
  background.
- Nothing is fitted except CFG805's b_eff ≥ 0 per bin, which only enters the two-halo variants.

## Verdict (frozen rule): **OUTER LENSING DISCRIMINATES: LAW**, both footings

**This test prefers the fundamental-law reading over route E's halos.** The claim goes no further than that, and the
caveats below limit what it means.

Δχ² = χ²(H-type) − χ²(L-type), full covariance. Positive means the law fits better. c_f = 4 in all four main rows.

| | canonical | alt |
|---|---|---|
| χ² all radii (60 points): L / H | 160.7 / 823.2 | 127.6 / 819.9 |
| χ² all radii: L2H / H2H | 154.3 / 583.9 | 125.1 / 580.6 |
| **Δχ²(H − L)**, primary R ≤ 0.31 Mpc / all radii | **+130.6 / +662.5** | **+140.3 / +692.3** |
| **Δχ²(H2H − L2H)**, primary / all radii (graded) | **+133.1 / +429.6** | **+144.5 / +455.6** |
| b_eff, all radii: L2H | 0 / 0 / 0.15 / 0.07 | 0 / 0 / 0.10 / 0.01 |
| b_eff, all radii: H2H | 0.25 / 0.37 / 0.65 / 0.69 | 0.25 / 0.37 / 0.65 / 0.69 |
| per-bin Δχ² with 2h, all radii (block-diagonal) | +43.6 / +127.6 / +126.7 / +163.1 | +43.8 / +135.8 / +133.9 / +175.3 |
| S1: 2h exclusion at median R200 (134–220 kpc) | +271.3 LAW | +292.2 LAW |
| S2: b_eff ≤ 1 | +429.6 LAW | +455.6 LAW |
| variant c_f(M) from X48 ng 48: Δχ²(H2H − L2H) primary / all | +136.6 / +433.0 | +151.2 / +462.3 |
| variant R200 at ρ_c(z_eff 0.285): primary / all | +122.9 / +419.3 | +135.6 / +446.6 |
| variant EM1 background B relation: primary / all | +119.9 / +409.8 | +131.9 / +436.4 |

**No model fits well in absolute terms.**
- L: p 4e-11 (canonical) and 9e-7 (alt). H: p ≈ 1e-134.
- Inside 0.31 Mpc, L2H gets p 2e-5 (canonical) and 2e-3 (alt).

**How much c_f matters.**
- With c_f = 4, bins 1–3 lie entirely below the floor/collapse crossover: 10^12.09 canonical, 10^12.43 alt. On
  canonical, bin 4 has 0.248 of its lens weight above it; on alt, none does.
- X48's ng 48 c_f moves the crossover below every lens, so 0.82–1.0 of the weight is above it. That moves Δχ² by only
  +3 to +7.
- So c_f is negligible here.
- No halo saturates.
- Bin-mean log M200: 11.35 / 11.72 / 11.90 / 12.05.

## What drives it (AMENDMENT A1, post-result, reported only)

| (H2H), Δlog M200 profiled | canonical, primary / all | alt, primary / all |
|---|---|---|
| frozen (shift 0), truncated | +133.1 / +429.6 | +144.5 / +455.6 |
| one common shift, truncated (best +0.35 primary / +0.50 all) | **−12.5 / +87.8** | **+12.5 / +129.8** |
| per-bin shifts, truncated | −14.4 / +84.4 | +11.9 / +124.3 |
| one common shift, untruncated (Burkert to 100 R200) | −11.4 / +27.6 | +13.5 / +70.6 |
| per-bin shifts, untruncated | −13.5 / +22.6 | +12.8 / +64.7 |

1. **Most of the frozen gap is normalisation.**
   - EM1's SPARC relation gives halos too light for these lenses. The (H) stack is short already at 0.12–0.31 Mpc:
     bin 2 at 0.311 Mpc gives data 7.55 ± 1.15, L 4.99, H 1.91 Msun/pc².
   - Lensing wants M200 about 0.35 dex (inner) to 0.5 dex (all radii) above what SPARC gives at the same baryonic
     mass.
   - That is a real tension inside route E: its SPARC halos and its lensing halos disagree.
   - Note that (L) itself is high at the innermost point. CFG805's diagnostic shows the same pattern.
2. **With the mass freed, the law still wins at all radii.**
   - Truncated: +84 to +130. Untruncated: +23 to +71. The law has zero mass parameters; (H) has one to four.
   - The sharp R200 edge alone costs about 60 in χ²: 242.2 vs 181.9 canonical, 254.9 vs 195.6 alt.
   - Inside 0.31 Mpc, once the mass is freed, the two models are within about ±13 and the sign flips between footings.
     The inner range does not separate them on shape.

## Where the predictions differ

- **Without 2h.** |L − H| first exceeds 1σ of the data at R ≈ 0.12 Mpc in bins 1–3 (0.09 Mpc for alt bin 1) and at
  0.036 Mpc in bin 4. At 2.6 Mpc the gap is 3.1–5.8σ per point. L/H in bin 2 is 1.08 at 0.035 Mpc, 2.6–2.9 at 0.31 Mpc,
  and 22–24 at 2.6 Mpc.
- **With the fitted two-halo term.** The 2.6 Mpc difference drops to 0.15–0.78σ. The leverage is therefore at
  0.12–1 Mpc, not at the largest radii.

## Systematics

- **The two-halo term can partly mimic the law's tail, but not the reverse.**
  - Fitting b·T2 to (L − H) absorbs 48 % (canonical) and 45 % (alt) of the expected Δχ² (405 / 523), with
    b 0.25–0.69.
  - Fitting it to (H − L) absorbs 0 %.
  - In the frozen fits, H2H takes b 0.25–0.69 and L2H takes ≈ 0.
- **Isolation leakage is not modelled by S1/S2 and is the main caveat for the outer part.** F2's committed numbers show
  the photo-z "isolated" outer signal is set by the environment:
  - S10 − S_strict outer amplitude is +0.74 ± 0.09.
  - B21's spectroscopically isolated GAMA lenses sit at 0.64 ± 0.15 of the KiDS isolated ones.
  - KiDS "all" sits at 1.46 ± 0.06 of the isolated sample.
  - P2's spectroscopically isolated stack lies below the zero-field law beyond 1.1 Mpc.
  - Leakage adds a ~1/R-like excess that the law's tail absorbs. So the outer part of the preference, roughly the
    ~60–130 left after the mass is freed, could be leakage. The inner normalisation result (+131 to +140 at R ≤ 0.31
    Mpc, at EM1 masses) is one-halo dominated and not exposed to it.
- **Inherited from CFG805.** The T1x P_grav template uses ΛCDM-inherited initial conditions, and its σ8 is low by 3.2 %.
  b_eff absorbs the amplitude. Template radii are not re-mapped to the native background (ledger A15).
- **Halo-relation inputs.** The lens M_b for the relation is M★ + cold gas, and SPARC's M_b uses Υ 0.5. F2's ±0.2 dex
  M★ brackets would move M200 by ±0.18 dex, short of the 0.35–0.5 dex needed.

## What a future survey needs

- At face value the present sample is already decisive. The forecast Δχ² between L2H and H2H, with either taken as
  truth, is 212 (canonical) and 287–289 (alt). The lens-number factor needed for Δχ² 25 is 0.09–0.12.
- The limit is systematic, not statistical. Two things are needed:
  1. **Spectroscopic isolation over a large area.** P2 estimated about 10× GAMA's 180 deg² to separate field effects
     at 3σ. That would remove the leakage that can imitate the law's 1/R tail at 0.4–2.6 Mpc.
  2. **A halo-mass normalisation for route E that does not come from SPARC.** For example, satellite kinematics on the
     same lenses would test whether the +0.35 dex inner shortfall belongs to the halos or to the lens M★.
- The discriminating radii are 0.12–1 Mpc. Beyond about 1.5 Mpc the two-halo term erases the difference.

## Checks and MUTATE

- **Step 0 (stop rule): PASS** (`x53_step0.py` reruns the committed scripts unchanged in a temporary copy).
  - CFG801: +197.07 / +753.02 canonical, +234.00 / +813.04 alt.
  - CFG803: dC +0.13 / +2.75.
  - CFG805: +148.70 → +11.06, b_eff 0.20 / 0.24 / 0.53 / 0.53.
- **Main run: 10/10 checks PASS.**
  - K0: step 0.
  - K_B: Burkert closed form.
  - K_2h: CFG805's template values reproduced, −0.53 / 1.80 / 1.57.
  - K_L: F2's L4 reproduced, 160.702 / 127.600.
  - K_N: the phantom is present (L / Newtonian baryons at 2.6 Mpc is 148–383).
  - K_T: truncation, point-mass limit 1e-15.
  - K_R: 0.32 GB.
- **MUTATE** (`X53_MUTATE=1`: no truncation and the law's ν ≡ 1): K_L, K_N and K_T FAIL on both footings, and the run
  exits 1. Under it, the class flips to HALOS (Δχ² −868).
- **Resources.** One thread, nice 15, 75 s per run. Nothing downloaded and nothing written outside this folder.

## Files

- `x53_step0.py`, `.out`, `_results.json`
- `x53_outer_lensing.py`, `.out`, `_results.json`, plus the `_MUTATE` outputs
- `x53_diag_A1.py`, `.out`, `_results.json` (A1)
