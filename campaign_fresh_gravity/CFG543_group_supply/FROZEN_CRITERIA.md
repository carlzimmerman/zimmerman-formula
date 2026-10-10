# CFG543 FROZEN CRITERIA (2026-10-09): the group supply gap — mechanism, or data/assumption error?

Committed alone, before any σ prediction of this lane is computed. κ = ½ is FITTED. Footings a0 = 9.36e-11 (can) and
1.13e-10 (alt) m s⁻² (CFG540's values), reported separately, never pooled. Kernel ν(y) = 1/(1 − e^(−√y)). Round enclosed-mass
rule, no EFE. Cold energy settles by CFG541 class A (inside-out fill to the catchment's exhaustion radius). The cold energy's
mass is still required. No dark-matter particle. Not "theory closed". No downloads; other lanes are imported read-only.

## 0. The gap (record)

CFG540 (Tian+2026 BFJR, 63 groups): Δ̄ = log σ_obs − log σ_law = +0.153 / +0.145 (census point-mass edge), +0.118 / +0.105
(supply-cap edge, post-freeze), +0.010 / −0.010 (law, no edge). CFG541 T2b (class-A edge): +0.118 / +0.106 ± 0.021; its
supply scan needs ×5 / ×3 the census supply. Owner's rule: a failure needs a mechanism or a scope statement, plus a data
re-check.

**Pre-freeze disclosures (dated 2026-10-09; no σ prediction or residual of this lane has been computed).**
- I read the TSV header: the only definitions on disk are "log10(baryonic mass)", "Effective radius/mean radius",
  "log10(velocity dispersion)", "log10(5*Re*sigma_e^2/G)". No ReadMe or paper text is on disk.
- I cross-matched the 63 groups crudely (brightest Kourkchi & Tully 2017 galaxy within 30′, on-disk
  `real_research/data/kt2017_*.tsv`; Virgo is one KT group, so Virgo matches are wrong). For 51 matched groups with ≥ 4
  members: median Tian Re / KT Rg ("projected virial radius") = 1.00; median σ_Tian/σ_KT = 0.72; median logMbar − log L_K =
  +0.18 dex. I noticed that NGC 4936 is in both Tian (logMbar 11.99) and the on-disk Lovisari+2015 X-ray group table
  (Mgas,500 = 1.69e12, h70).
- I have read CFG541's supply scan (×3 → +0.057 / +0.040; ×5 → +0.040 / +0.023).

## 1. Data re-check (D; reported, D1 feeds the verdict)

- **D1 hot gas in M_bar.** From on-disk data only: (i) NGC 4936: Tian M_bar vs Lovisari Mgas,500. If M_bar < Mgas,500,
  M_bar cannot contain the group's hot gas → **D1 = HOT GAS EXCLUDED (at least for that group)**; else NOT EXCLUDED.
  (ii) Descriptive: logMbar − log L_K (KT, crude match) by group type; a stars(+cold gas) census gives M/L_K ≈ 0.5–1.5.
- **D2 Re.** The header says "Effective radius/mean radius"; Re ≈ KT's projected virial radius (D0 above). Reported as: Re is
  a group-scale projected size estimator, not a measured half-mass radius. The conversion brackets are in §3 (R2–R4).
- **D3 σ.** Whole-group line-of-sight member dispersion (CFG540's aperture ∞). Reported, no change.

## 2. Model (one code path for every configuration)

Per group: tracer = members, Hernquist with projected half-mass radius R_e (primary R_e = catalogue Re; a = R_e/1.8153),
mass M_cat = 10^logMbar. Total baryons M_b(<r) = members + hot gas (if any). Phantom M_ph(<r) = (ν(G M_b(<r)/(r² a0)) − 1) M_b(<r).
Class-A edge: the phantom is frozen at the first radius where M_ph(<r) reaches the supply M_sup (CFG540 post-freeze "cap" =
CFG541 T2b). σ² = ⟨r g(r)⟩_tracer / 3 (aperture ∞, any β). Log grid r/a ∈ [1e-5, 1e5], 3000 points (CFG540's).

**Hot gas geometry (declared; derived from on-disk Lovisari+2015 where possible):** β-model, β = 2/3 (declared standard),
ρ ∝ [1 + (r/r_c)²]⁻¹, truncated at R_t. r_c/R500 = the value that reproduces the Lovisari sample median Mgas,2500/Mgas,500 at
the median R2500/R500 (computed in the script). R500 per group from an OLS fit log R500 = A + B log Mgas,500 on the 20 Lovisari
groups, evaluated at the group's hot mass inside R500. Primary: all hot gas inside R_t = R500. Variant G2: R_t = 2 R500 (same
total, so about half inside R500).

**Hot-gas mass (declared sources, no fit):**
- **H1 (census-internal, primary).** The census f_ret counts all retained baryons, gas + stars (CFG416 declared text; R4). Its
  galaxy-scale value 0.10 (fret_of below 10^12.5 h⁻¹ M⊙) is the condensed (stars + cold gas) retention. If Tian's M_bar is the
  condensed component, the consistent turnaround mass is M_ta = M_cat h / (f_cond f_b16) with f_cond = 0.10, the retained total
  is M_tot = f_ret(M_ta) f_b16 M_ta / h and M_hot = M_tot − M_cat = M_cat (f_ret/f_cond − 1). Supply M_sup = 5.364 M_tot / f_ret =
  5.364 M_cat / f_cond. Brackets f_cond = 0.07 and 0.13 (PAPER45 low census; the record's cm08 galaxy level).
- **H2 (single measured anchor).** M_hot = M_cat × (the ratio Mgas,500 / M_bar measured for NGC 4936 (Lovisari over Tian, computed in
  the script)), applied to every group, inside R500; supply = 5.364 M_tot / fret_census(M_tot).

## 3. Configurations (all per footing)

- **C0 control:** M_cat only, supply 5.364 M_cat / fret_census(M_cat), class-A edge. Must reproduce CFG540 post-freeze
  cap_variant means (+0.1181 / +0.1054) to |diff| < 0.003, and the no-edge run CFG540's +0.0100 / −0.0101 to < 0.003.
- **(a) hot gas:** **P1** = H1 (hot gas in the law + consistent supply), **P3** = H2.
- **(b) radius:** C0 with R_e = Re/k: **R2** k = 1.052 (Re = projected pairwise harmonic mean radius of a Hernquist system,
  6a/π; checked by Monte Carlo in the script, K3), **R3** k = 2.104 (Re = N²/Σ_{i<j} 1/R_ij convention, twice R2), **R4**
  k = 3.305 (Re = the 3D gravitational radius r_g = 6a). Brackets of the unknown definition, not fits. Also applied to P1, P2.
- **Mechanisms (derived):**
  - **(i) progenitor containment, P2.** Every progenitor catchment lies inside the group's z = 0 turnaround sphere (matter that
    has collapsed into a progenitor has turned around), and class A conserves cold-energy mass with no return. So the group's
    catchment ≥ Σ progenitor catchments, and the cumulative supply cannot exceed the z = 0 catchment content (bound, factor
    1.00). If the group's condensed baryons were assembled in galaxy-scale progenitors at the census floor, the catchment is
    ≥ 5.364 M_cat / 0.10. **P2** = M_cat only (no hot gas: "M_bar complete" reading), supply 5.364 M_cat / f_cond, f_cond = 0.10
    (brackets 0.07 / 0.13). Partition variant **P2h**: half of M_cat in one progenitor at its own fret_census, half at 0.10.
  - **Max-concentration bound (any redistribution, incl. merger-delivered overfill):** with total cold ≤ M_sup, g(r) ≤
    G[M_b(<r) + M_sup]/r². Reported for C0 and P2 as Δ_min.
  - **(ii) catchment growth:** the z = 0 catchment is the largest to date (turnaround mass grows monotonically); EdS
    self-similar infall gives r_ta ∝ t^(8/9), M_ta ∝ t^(2/3), so the catchment at z = 1 / 2 holds (1+z)⁻¹ = 0.50 / 0.33 of z = 0.
    Reported as a factor ≤ 1 (cannot raise the supply).
  - **(iii) f_ret check:** per group, CFG540's f_ret (fret_census of M_cat) vs the H1-consistent f_ret(M_ta); the containment
    inconsistency count: groups whose CFG540 M_ta is smaller than M_cat h/(0.10 f_b16) (the galaxy-floor progenitor sum).
- Each configuration also reports the needed supply factor (scan ×1–×50 of its own supply) as information only.

## 4. Statistics (CFG540's)

Δ_i = log σ_obs − log σ_pred; class mean Δ̄, SE = sd/√63; σ_sys = s̄ × 0.10 (s = d log σ_pred / d log M_cat, numerical, the
whole chain re-run at +0.01 dex); σ_tot = √(SE² + σ_sys²); Z = Δ̄/σ_tot. Per configuration and footing: **CLOSES** if |Z| < 2;
**ABOVE** if Z ≥ 2; **BELOW (over-corrects)** if Z ≤ −2.

## 5. Verdict (per footing; the lane verdict lists every label that applies)

- **DATA-ISSUE (stars-only M_bar fed to the gas+stars census)** if D1 = HOT GAS EXCLUDED and P1 CLOSES.
- **MECHANISM FOUND (progenitor containment)** if P2 CLOSES.
- **GENUINE TENSION (Z)** if neither P1 nor P2 closes and the max-concentration bound on P2 still gives Z ≥ 2; the Z of P1 and
  P2 is reported.
- **NOT DIAGNOSTIC** if the outcome differs between footings, or if P1 or P2 closes only inside one bracket (f_cond, G2, R2–R4)
  while the primary does not, or if P1 over-corrects (BELOW) while P2 is ABOVE.
- Appended "(Re-DEPENDENT)" if any R2–R4 variant changes the label of P1 or P2.
- No supply factor is adopted; the scan is information only. If the result rests on f_cond = 0.10 being the condensed fraction
  of groups, that is stated as the inherited input.

## 6. Checks (must pass before verdicts are read)
- K1 = C0 reproduction (above). K2 deep-MOND point mass: σ⁴ = (4/81) G M a0 to < 0.01 dex for M_cat, no gas, no edge, at
  y < 1e-3. K3 Monte-Carlo Hernquist projected pairwise harmonic radius / R_e = 1.052 ± 0.01. K4 the hot-gas β-model reproduces
  the Lovisari median Mgas,2500/Mgas,500 to 1e-6.

## 7. MUTATE (`CFG543_MUTATE=1`, outputs `_MUTATE.*`); each must bite as stated
- M1 supply × 0.3 on P1 and P2: Δ̄ must rise by ≥ 0.02 dex on both footings.
- M2 σ shuffled across the 63 groups (200 shuffles, seed 543), P2: rms(Δ) must exceed the true rms in ≥ 95% of shuffles
  (per-group tracking). If it does not, per-group tracking is reported as NOT DEMONSTRATED (class mean only).
- M3 Newtonian (ν = 1) on P1 and P2: must not CLOSE.
