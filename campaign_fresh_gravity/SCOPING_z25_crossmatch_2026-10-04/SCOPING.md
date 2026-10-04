# SCOPING: galaxies at 2.0 ≤ z ≤ 3.0 with a resolved rotation curve AND an SED/NIRCam M* AND a measured gas tracer (2026-10-04)

> **κ = ½ is FITTED. a₀(z) FLAT is the framework's distinctive law; a₀ ∝ H(z) is the rival. No a₀ is computed here, nothing is fitted, and no sentence says the data favour a law.** Both footings (9.36e-11 / 1.131e-10 m s⁻²) apply to any later run.
> Literature scoping only. About 23 web searches/fetches (arXiv abstract/HTML pages, search snippets), no downloads, nothing saved besides this file. Not committed.
> **How read:** `abs` = arXiv abstract page; `html` = arXiv HTML through a summariser; `snip` = search-result snippet only (**PROVISIONAL**); `rec` = already in this repository's record (lane named). Summariser output is provisional; table rows were matched by position, not by echoing a name.
> Companion to CFG268 (`../CFG268_z25_4_gap_scoping/SCOPING.md`, which covers z 2.5–4). This note covers z 2.0–3.0 and asks only the three-way cross-match.

## Bottom line
1. **No new object turned up.** Every galaxy at 2.0 ≤ z ≤ 3.0 that meets (a)+(b)+(c) even provisionally is **already in the record** (RC100/CFG289, CFG278, CFG227/237 ALPAKA, CFG275, CFG268).
2. **Seven objects pass all three** (several only provisionally; see the shortlist). Two more famous lensed discs (J0901, the Cosmic Eyelash) have CO(1–0) but **fail (a)**: their curves stop at ≈ 1 R_e and ≈ 2.5 kpc.
3. **JWST NIRSpec IFU and VLT ERIS gave nothing in the band.** GA-NIFS targets are at z ≥ 3. MSA-3D is z 0.5–1.7 (arXiv:2606.27853, snip). JADES DR3 is stacks without baryons (arXiv:2609.14071, snip). No ERIS disc paper at z 2–3 was found. None of the shortlisted objects has a NIRCam-resolved M*; all use ground/HST SED masses.
4. **The 41 RC100 galaxies at z 2.00–2.52** (rows 60–100 of `real_research/data/rc100_nestorshachar2023_table3_CORRECTED.csv`) meet (a) and (b), but their gas comes **mostly from scaling relations** (abs, 2209.12199: "Hα or CO rotation curves", no per-galaxy CO count stated). Which rows have a PHIBSS CO(3–2) measurement was **not verified** in this pass.

## Cross-match table
Columns (a) kinematics, (b) M*, (c) gas. "Reach" is in R_e where the source gives it.

| galaxy | z | kinematics (instrument, ref) | outer reach | M* source | gas tracer + ref | lensed? | in record? | gap |
|---|---|---|---|---|---|---|---|---|
| Q2343-BX610 | 2.211 | SINFONI-AO Hα (SINS; RC100 row 78); ALMA CO(4–3) (ALPAKA 14, class "uncertain", html 2303.16227) | RC100: "several R_e" (sample claim, abs); R_e 5.24 kpc | SED (ALPAKA Stardust; RC100) | **CO(1–0) VLA** (Aravena+14; Bolatto+15, abs 1507.05652: four PHIBSS galaxies, BX610 named only in snip, **PROVISIONAL**); CO(3–2) PHIBSS; CO(4–3)+[CI](1–0)+dust 630 µm, ALMA ~20 h (abs 2410.14781: M_mol/M* ≈ 1 in the centre) | no | **rec** (RC100, CFG280, CFG227) | CO kinematic class uncertain; possible AGN; CO(1–0) beam vs disc size not read |
| zC-400569 | 2.240 | SINFONI-AO Hα + ALMA CO(3–2), CO(4–3) (Lelli+23, 2302.00030) | flat to ≈ 8 kpc (snip); R_e 4.31 kpc ⇒ ≈ 1.9 R_e | SED (Liu+19, per CFG278) | **CO(3–2)+CO(4–3)**, multi-line (excitation constrained by the ladder); no CO(1–0) found | no | **rec** (CFG278: FLOOR; RC100 row 85) | SED M* 2.8× the dynamical value (CFG278); no CO(1–0) |
| CLJ1001-130949 / -130891 / -131077 | 2.504 / 2.513 / 2.494 | ALMA CO(3–2), ALPAKA 20/21/19, all "disk" (html) | 2–5 rings per galaxy (sample statement); per-object reach not stated | SED (Stardust) | **CO(1–0) VLA D-config**, Wang+18 (arXiv:1810.10558, snip: 14 members with M* > 10^10.5 detected). **ID-by-ID match to the 14 NOT verified** | no | **rec** (CFG227/237 ALPAKA group) | cluster core (environment); unresolved CO(1–0); one is a starburst (131077) |
| HATLAS J084933-W | 2.407 | ALMA [CI](1–0) (ALPAKA 18, disk); CO(4–3)+[CI] at 0.15″: rotating disc with bar-like radial motions (A&A 2025, doi 10.1051/0004-6361/202554705, snip) | not stated | SED | [CI](1–0), CO(4–3), dust; CO lines incl. CO(1–0) from Ivison+13 (snip says "multiple CO lines"; **CO(1–0) PROVISIONAL**) | weak/none (not checked) | **rec** (CFG227/237) | HyLIRG starburst + AGN; non-circular motions |
| PKS 0529-549 | 2.57 | ALMA [CI] kinematics, mass models (A&A 2025, aa50814-24, snip) | per CFG275 | per CFG275 | **[CI] + CO + dust** (arXiv:2411.04290, snip) | no | **rec** (CFG275: 7/8 floor) | radio-loud AGN host; near-Newtonian (CFG268: y ≈ 8) |
| GS30274 | 2.225 | ALMA CO(3–2) (ALPAKA 15, disk) | not stated | SED | CO(3–2) only (no excitation found) | no | **rec** (CFG227/237) | AGN; no CO(1–0) or ladder |
| COSMOS 3182 | 2.103 | ALMA [CI](2–1) at 2.7σ (ALPAKA 13) | 1 radius used (CFG272) | SED | [CI](2–1) only (weak) | no | **rec** (CFG272: NO ROOT) | low S/N; [CI](2–1) is a poor mass tracer |
| HXMM01-a / -b+c | 2.31 | ALMA CO(7–6) (ALPAKA 16/17: uncertain / merger) | — | SED | CO(7–6); CO(1–0) by Fu+13 **UNVERIFIED** | weak (μ not checked) | rec (2 mentions) | merger; fails (a) |
| Gal3 | 2.935 | ALMA CO(5–4) (ALPAKA 22) | not stated | SED | CO(5–4) only | no | **rec** | starburst; high-J only |
| SDSS J0901+1814 | 2.259 | ALMA CO(3–2) 0.36″ + SINFONI Hα (Liu+23, abs 2211.08488) | **≈ 1 R_e (R_e ≈ 4 kpc)** | SED (RC100 row 87) | **CO(1–0) VLA, resolved** + CO(3–2) (Sharon+19, 1905.09845, snip) | **yes**, μ not read in the abstract | **rec** (RC100, CFG227) | **fails (a)**: reach ≈ R_e; f_DM(R_e) 0.3–0.4 |
| Cosmic Eyelash (SMM J2135-0102) | 2.326 | PdBI CO(6–5) + VLA CO(1–0) (Swinbank+11, 1110.2780) | M_dyn inside 2.5 kpc only | SED | **CO(1–0)** + CO(6–5) | **yes**, μ = 37.5 ± 4.5 (snip) | rec (CFG268 reference only) | **fails (a)**; SMG; lens-model dependent |
| zC-406690 | 2.20 | SINFONI-AO (Genzel+17 falling RC; RC100 row 77) | several R_e | SED | **not found** (scaling relation) | no | **rec** | no measured gas |
| D3a-15504, BX482, zC-400528 + other RC100 z 2–2.5 (41 rows) | 2.00–2.52 | SINFONI/KMOS/LUCI (RC100) | "several R_e" (sample) | SED | mostly scaling; subset CO(3–2) PHIBSS **not verified** | J0901 only | **rec** (RC100/CFG289) | per-row gas provenance |
| Cosmic Horseshoe | 2.381 | no gas kinematics paper found | — | — | — | yes | no | fails (a) and (c) |
| SDP.81 | 3.042 | ALMA CO/dust (Dye+15, Swinbank+15) | ≈ 1.5–6 kpc | — | CO | yes | rec (CFG268) | just outside the band; interacting |

## Ranked shortlist (all three, at least provisionally)
Ranked by gas-tracer quality, then disc regularity, then how secure the match is.
1. **Q2343-BX610** (z 2.211): CO(1–0) VLA (provisional) plus CO(3–2)/(4–3), [CI] and dust. It is the best-documented gas budget in the band. Weaknesses: the CO kinematic class is "uncertain" and it may host an AGN.
2. **CLJ1001-130949, -130891, -131077** (z ≈ 2.50): CO(1–0) VLA, but the match by ID is unverified and the CO(1–0) is unresolved. The CO(3–2) discs are in ALPAKA. They sit in a cluster core.
3. **zC-400569** (z 2.240): CO(3–2)+(4–3) ladder and the flattest, coldest curve (≈ 1.9 R_e). There is no CO(1–0). Already a FLOOR in CFG278.
4. **HATLAS J084933-W** (z 2.407): [CI](1–0)+CO(4–3)+dust, with a provisional CO(1–0). It is a barred, starbursting HyLIRG.
5. **PKS 0529-549** (z 2.57): [CI]+CO+dust, but it is an AGN host. Already CFG275.

Near misses: J0901 (CO(1–0) but reach ≈ R_e), Cosmic Eyelash (CO(1–0) but reach 2.5 kpc), GS30274 (CO(3–2) only), COSMOS 3182 ([CI](2–1) at 2.7σ).

## Count by gas tracer (the 7 shortlisted objects, best tracer each)
- **CO(1–0): 5**: BX610, CLJ1001 ×3, HATLAS-W. **All five are PROVISIONAL**: BX610 is named only in a snippet, the CLJ1001 IDs are unmatched, and HATLAS-W's CO(1–0) is inferred from "multiple CO lines".
- **Mid-J CO with excitation (a ladder): 1**: zC-400569.
- **[CI]: 1**: PKS 0529-549 (with dust).
- **Dust continuum only: 0.**
- **Secure CO(1–0) with a curve reaching ≥ 2 R_e: 0.** The two secure resolved CO(1–0) lensed discs (J0901, the Eyelash) fail the reach test.

## Feasibility of a decisive FLAT vs a₀ ∝ H(z) test at z ≈ 2.5 today
**Not possible today, with any number of these objects.**
- **The ×3 difference shrinks in these galaxies.** At z = 2.5 the rival's a₀ is ≈ 3–3.7× the flat value. But every shortlisted disc is massive and near-Newtonian at its last measured radius: y = g/a₀ ≈ 4–15 in CFG268, CFG272 and CFG278. There the a₀ dependence nearly vanishes.
- **Illustration, not a committed result.** With the simple ν(y) = ½ + √(¼ + 1/y), a ×3 change in a₀ moves g_obs by only ≈ 0.08 dex at y = 5 and ≈ 0.06 dex at y = 10.
- **The baryon budget is far less certain than that.** α_CO alone spans 0.8–4.4 (≈ 0.7 dex) between starburst and Galactic values. Excitation (r₃₁, r₄₁) adds ≈ 0.2–0.3 dex whenever CO(1–0) is missing. SED M* is uncertain by 0.2–0.3 dex, and CFG278's zC-400569 shows a ×2.8 SED-vs-dynamical conflict.
- **The yardstick needs far more than exists.** CFG240's conditioning wall needs N ≈ 20 discs with points down to y ≲ 0.1 and about 0.1 dex baryon calibration to reach 0.1 dex in a₀. The band holds 0 such discs, about 7 provisional all-three objects (none with secure resolved CO(1–0) and ≥ 2 R_e) and 41 RC100 discs whose gas comes mostly from scaling relations.
- **What the record can give.** Floors and upper bounds, as CFG272/275/278 already gave, not a measurement.
- **What a decisive test would need.**
  - Low-mass, gas-rich discs whose outer curves reach y ≲ 0.3, from ALMA [CI]/CO or NIRSpec IFU.
  - Resolved CO(1–0) from the VLA or ALMA Band 1 to fix the gas, together with a dynamically calibrated α_CO.
  - Of order 20 such discs. None is public as of this scoping.
