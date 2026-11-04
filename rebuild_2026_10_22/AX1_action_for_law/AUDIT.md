# AX1_action_for_law, Step 1: AUDIT of action classes for the galaxy law (2026-11-04)

**Scope (owner, 11-04).** The theory is the galaxy law g_N = g²/(g + a0), a0 = κc√(Gρ_DE), κ = ½ FITTED. Footings canonical a0 = 9.3603e-11 and alt 1.1312e-10 m/s², never pooled. The question is which action class can give *this* interpolation in galaxies (G1) and pass the Solar System (G2), lensing = dynamics (G3) and GW speed + health (G4), with G5 (a0 ∝ √(Gρ_DE) from the action) graded but not required. CMB and clusters are OUT of scope and stay open; the cluster gap is a requirement, not solved. The cold sector stays retired; nothing here reinstates it. Not blind. Not theory closed. Nothing here says the data favour the framework.

**Post-audit note (same day).** The owner then asked for every class to end with a verdict and lifted the v3s freeze for testing (11-04). So v3s, listed below as "frozen by owner, not regraded", was regraded in `v3s/` (adopts nothing; the 10-24 verdict stands). Final statuses are in `README.md`. This audit's table is left as committed.

**Lane id.** `ls rebuild_2026_10_22 | grep AX1` was empty. `git log --all | grep AX1` finds one hit, 68ffb00ac5 (QUEUE_ROADMAP_2026-11-01), where "AX1" named an axisymmetric Poisson–Jeans solver that was **dropped, not started**, with no folder. This lane takes the id by the coordinator's assignment; the two are unrelated.

**Sources.** Repo lanes are cited by commit (criteria / result). Literature is **PROVISIONAL**: from web-search snippets on 2026-11-04 (full texts not read) or from memory, labelled per row. No downloads.

## 1. What the record already settles, for every class at once

Every class below except the superfluid one reduces, in the static weak field and without a new length scale, to **AQUAL** (∇·[μ(|∇Φ|/a0)∇Φ] = 4πGρ) or **QUMOND** (∇²Φ = ∇·[ν(|∇φ_N|/a0)∇φ_N]) with a free function. So G1 and most of G2 are properties of that static limit, and the record has computed them:

| static fact | number, canonical / alt | source |
|---|---|---|
| Law's μ = x/(1+x) everywhere: constant sunward a0 at every planet | δg ≈ a0 at Saturn = 1.3e4 / 1.6e4 × the 7.0e-15 m/s² Saturn bound | arithmetic on `prep_2026/planetary_doors/BOUNDS.md` (Fienga & Minazzoli 2024 Table 10); Blanchet & Novak 2011's own statement that δg = a0 is ruled out, quoted there |
| A high-g turn-off of the free function (y > 60) removes that monopole and leaves SPARC and Q2 unchanged | Q2 moves ≤ 0.052σ across y_t ∈ [60, 140] | D7b c6a0b6f3c7 / 9542a09f54 |
| Law's μ, Cassini EFE quadrupole Q2, AQUAL | 2.44–4.59× / 2.85–5.19× the Hees+2014 2σ line (9.0e-27 s⁻²) | E2 021ee82abb / 474050bcd8 (PAPER58) |
| Law's μ, Q2, QUMOND | 1.70–3.70× / 1.91–4.03× Hees | D7b |
| Any other static μ that keeps SPARC (n, β, ν_mono, standard, ν_RAR families) | QUMOND: β ≥ 2.5 passes Q2 at all four fields on canonical (0.61–0.95× Hees) and SPARC's graded statistic; alt fails E0 by 1.19–1.23×. AQUAL: no member passes both on either footing (β fails canonical E0 by 1.01–1.12×; n = 8 passes Q2 but fails SPARC at z −6.3) | D7c e9e5349368 / 26b5db080f; E2 R3 |
| Published | RAR vs Solar-System Q2 tension 8.7σ (fiducial), 1.9σ without bulge galaxies | Desmond, Hees & Famaey 2024, MNRAS 530, arXiv:2401.04796 [PROVISIONAL, abstract] |
| A fixed length that regularises the MOND field near each mass passes Q2 by 10⁷–10⁹ | L★ ≥ 24 pc: Q2 ≤ 2.1e-8 of the Hees line, ≤ 3.6e-8 of Park's | D7d a13e418498 / b26f14bb82; C6 1b2ced55a4 / ae428dc252 (v3s family) |

**So the key question has a short answer.** With the law's own μ, every unscreened class fails G2 (monopole by ~10⁴, Q2 by 1.7–5.2×). A high-g turn-off fixes the monopole for free, but Q2 is set at r ≈ 7000 AU where g ≈ a0, the same range SPARC pins. The only ways out on record are (a) a new length that screens inside ~0.02–24 pc of a mass (v3s's L★; the record's filtered-QUMOND rules KT16/KT17), or (b) a QUMOND-type static limit with a sharper μ (β ≥ 2.5), which passes on canonical only, knife-edge. (b) is not "the law" g²/(g+a0); it is a different interpolation that matches SPARC within the law's errors.

## 2. The audit table

G-columns: **P** pass, **F** fail (number), **O** open, **—** not defined. "lit" = literature, PROVISIONAL.

| class | G1 SPARC (law's μ) | G2 Solar System | G3 lensing = dynamics | G4 GW at c, health | G5 a0 from action | verdict | where graded |
|---|---|---|---|---|---|---|---|
| **AQUAL / QUMOND** (non-relativistic), with RAQUAL as its covariant form | P by construction | **F**: Q2 2.44–4.59× (AQUAL) / 1.70–3.70× (QUMOND) canonical; monopole 1.3e4× without a turn-off | **F** for RAQUAL: a conformally coupled scalar adds no light bending, so lensing sees baryons only (Bekenstein & Sanders 1994) [lit, memory]; the non-relativistic theory defines no lensing | — (non-relativistic); RAQUAL's scalar has superluminal propagation (Bekenstein & Milgrom 1984) [lit, memory] | by hand | **FAIL (G2, G3)** | closed here: record numbers above + DHF 2024 |
| **BIMOND** (Milgrom 2009) | P (non-relativistic limit is QUMOND with a free ν) [lit, memory] | law's ν: **F** 1.70–3.70× / 1.91–4.03× (QUMOND); β ≥ 2.5: canonical knife-edge P, alt **F** 1.19–1.23× | P: one metric for matter and light, Φ = Ψ [lit, memory] | **F [lit]**: Chesler & Loeb 2017 (arXiv:1704.05116) conclude "BIMOND in its present form is not an acceptable theory" [snippet; their argument not read] | by hand | goes to Step 2: static escape (b) lives here | `BIMOND/` |
| **TeVeS** (Bekenstein 2004; Skordis 2008/09) | P (AQUAL-type) | F as AQUAL (same Q2) | P by its disformal metric | **F**: GW170817 rules it out; GWs and photons ride different metrics, Shapiro split ~400 days (Boran, Desai, Kahya & Woodard 2018, arXiv:1710.06168; Skordis & Złośnik 2019, arXiv:1905.09465) [lit, snippets] | by hand | **FAIL (G4, published bound)** | closed here |
| **AeST** (Skordis & Złośnik 2021) | P (AQUAL-type with a mass term) [lit, memory] | not published for Q2 (web search found none); record: v9 AeST static branch α1 = −2(K_B+2), moving source α1 = α2 = 0 but the law is lost for moving systems (AS3 9581518967 / 6770f2d8ad) | P by construction [lit, memory] | c_T = c by construction [lit]; record: AeST's sector fails health H1 (X6 fd303cac8b / fbcce8f612) | by hand | goes to Step 2 | `AeST/` |
| **Khronon** (Blanchet & Marsat 2011) | P (MOND Poisson-type limit, arXiv:1107.5264) [lit, snippet] | PPN = GR except α1, α2 (Bonetti & Barausse 2015, arXiv:1502.05554) [lit]; record: static-branch α1 = −4η, unscreened α2 8.7e3–1.5e7 (X15 87867a70a4 / 11f2dceb59, reported as not PPN) | P: same lensing as GR [lit, snippet] | khronometric c_T² = 1/(1−β_kh), β_kh = 0 allowed [lit, memory]; record parent C4 + health C5: conditionally healthy only in C4's literal form | by hand | goes to Step 2 | `khronon/` |
| **Einstein-aether MOND** (Zlosnik, Ferreira & Starkman 2007, F(K)) | P (AQUAL-type) [lit, memory] | F as AQUAL; PPN α1 = −4c14 at c13 = 0 [lit, memory] | P [lit, memory] | **F**: in the MOND limit the GW speed depends on the local potential and cannot be set to c (Chesler & Loeb 2017); GW170817 forces \|c13\| ≤ 1e-15 (Oost, Mukohyama & Wang 2018, arXiv:1802.04303) [lit, snippets] | by hand | **FAIL (G4, published bound)** | closed here |
| **Superfluid-type, effective field only** (Berezhiani & Khoury 2015 phonon P(X) ∝ X^{3/2}, no particle) | **F**: the static force is g = g_N + √(a0 g_N), not the law (ν = 1 + y^{-1/2} vs the law's ν) [lit, memory] | **F**: extra √(a0 g_N) at Saturn = 7.8e-8 / 8.5e-8 m/s², 1.1e7 / 1.2e7 × the 7.0e-15 bound (arithmetic; with no condensate there is no phase boundary to screen it) | **F**: conformal coupling, no extra lensing; BK's lensing needs the particle's mass, which is excluded | not graded (killed above) | by hand | **FAIL (G1, G2, G3)** | closed here |
| **Non-local metric MOND** (Deffayet, Esposito-Farèse & Woodard 2011/2014) | P in the static spherical limit [lit, arXiv:1106.4984] | GR "in the solar-system regime" by construction [lit]; the EFE quadrupole is not given by the published static-spherical form | P: built to give enough lensing [lit] | no GW170817 analysis found [web search] | by hand | goes to Step 2 | `nonlocal/` |
| **v3s** (record's own; AeST/khronon embedding + switched stiffness L★) | P (SPARC rms 0.054 / 0.054, P4) | P screened: 24/24 Cassini cells by 4.8e7–5.1e9 (C6, E2); α1 = α2 = 0 for the β completion (X15) | P at the S4 lensing bound on μ_K | c_T = c (C8); constraint algebra closes (X3); caustics generic (X14) | a0 = c²√(Λ/32π) with κ fitted: by hand | **frozen by owner, not regraded** | `covariant_push_2026_10_22/V3S_FINAL_VERDICT_2026-10-24.md` |
| *Filtered QUMOND (record rules KT16–KT32), not an action* | KT19: ε 0.55 filter survives SPARC | KT16: universal ξ ≥ 0.45 / 0.50 r_M passes Q2; KT17: ε 0.55 passes | not built; LAW_RULE_LEDGER: KiDS lensing fails every rule | not built | by hand | **no action on record; not graded here** | see §4 |

**G5 for every class: a0 is put in by hand.** No class on the list has a term that makes a0 ∝ √(Gρ_DE). KF1 (8f14af0da8 / 5abc2d1ae6) finds nothing forced: κ = 1/(2ξ) only moves the ½ into a forcing length c/√(Gρ). That holds for every row.

**G3 data caveat for every class that passes G3.** Lensing = dynamics means lensing at the law's mass. The law itself is short of KiDS galaxy-galaxy lensing by about 0.09 dex under every grader on record (LE1 7efbb03f3d / 17574fce14). A class that passes G3 inherits that shortfall; G3 as graded here is the theory-internal statement Φ = Ψ.

## 3. Which classes close here, and which go to Step 2

- **Closed in this audit by a published bound or theorem:** AQUAL/QUMOND/RAQUAL (G3 theorem; G2 record + DHF 2024), TeVeS (GW170817), Einstein-aether MOND (Chesler & Loeb 2017; Oost+ 2018), superfluid effective field (G2 by 1e7 against the ephemeris bound, G3 conformal). All four are FAIL.
- **Step 2, each in its own subfolder with its own FROZEN_CRITERIA committed alone first:** BIMOND (its static limit holds the only non-v3s escape, (b); its G4 kill rests on a snippet I did not read), AeST, khronon, non-local metric MOND.
- **v3s:** frozen by owner, not regraded. Its record verdict is the row above.

What a Step 2 grade adds over the table: a fresh QUMOND Q2 engine (independent code) that must reproduce D7b's and D7c's committed numbers before it is trusted, both footings at the exact footing values, the Saturn monopole with and without a turn-off, the class's own extra terms checked for any screening at r ≈ 7000 AU, and G3/G4 read against the class's literature and the record. Not a new SPARC fit: the SPARC grade of a μ change is D7c's committed statistic, read from its JSON.

## 4. The one lead the list does not contain

The record's filtered-QUMOND rules (phantom sourced by baryons smoothed over ξ) pass Cassini for a universal ξ ≥ 0.45 r_M ≈ 3600 AU (KT16 72a296bf17 / 7ed4d5ac0a) and survive SPARC at ε = 0.55 (KT19 94562be676 / 2a379478e7). A universal ξ is a new length that regularises the MOND field near each mass. That is the same mechanism as v3s's L★, written in QUMOND form. No action for it is on record, and no relativistic completion. Whether a smoothed-QUMOND action counts as v3s family is the owner's call; this lane does not open it.
