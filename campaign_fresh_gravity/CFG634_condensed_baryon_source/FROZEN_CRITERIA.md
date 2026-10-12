# CFG634 FROZEN CRITERIA: the condensed-baryon source (H-CB)

Committed ALONE, before any CFG634 script exists or any number is computed. Date 2026-10-11.

κ = ½ is FITTED. The two footings (canonical 9.3603e-11, alt 1.1312e-10 m s⁻²; each reused pipeline keeps its own committed
footing values) are reported separately and NEVER pooled. "Cold energy" throughout. No dark-matter particle. The cold energy's
mass is still required. Not "theory closed". Raw data vs framework-native predictions only; ΛCDM / standard-MOND machinery appears
only where a reused lane already carries it, labelled CONTEXT ONLY.

## 1. Hypothesis

**H-CB.** The law's phantom (the profile cold energy settles into, R1) is sourced ONLY by CONDENSED baryons: stars plus
cold/neutral gas (HI, H2). Diffuse hot gas (X-ray emitting, ≳ 1e6 K) gravitates as ordinary Newtonian mass but sources no
phantom. All cold energy that is not settled stays an ordinary collisionless reservoir: total supply 5.364 × (the catchment's
original baryons), minus the settled phantom. No new constant: the split is the measured phase of the baryons.

Everything else is candidate B as the record defines it (THEORY_v1_2026-10-09.md): same law, kernel, a₀, supply, census
f_ret, catchment, round rule, no EFE. The switch still reads baryons (MS1 kept), but only the condensed phase sources the
phantom.

## 2. Prior record (grep done before freezing)

No committed lane has tested "hot gas excluded from the phantom source" inside halos. The closest relatives:
- CFG372 / CFG374 / CFG376 (PM, CFG366 bookkeeping engine, 256³, particle field): the phantom source was Jeans-filtered by
  gas temperature; CFG376 split the collapsed phase into filtered hot halo gas (0.10 of baryons) and unfiltered stars + cold
  gas (0.08). All carry a KNOWN k_J time-dependence BUG (audit 5819dd616); CFG372's pass is WITHDRAWN. Direction only: removing
  hot gas from the source lowered small-scale excess. CFG634 builds on their phase bookkeeping, not their numbers.
- CFG432: the unsettled cold mass in X-COP does NOT have the gas's shape (more concentrated; NFW c = 4 consistent only at
  b = 0.3). This motivates the NFW reservoir bracket.
- CFG543: Tian+26 group M_bar = member stars + observed X-ray gas (paper: median gas-to-baryon about 8% for ellipticals and
  groups). CFG629: candidate B's reservoir closes most of the Bullet main-cluster core mass (NFW c = 4 placeholder).
- KiDS lens masses (Brouwer+21, `lr_lenses.npz` field Mgal = M*(1 + f_cold)) are already stars + cold gas.

## 3. Phase split rule per system (declared from the data columns, before any outcome)

| test | condensed (sources the phantom) | hot (Newtonian only) |
|---|---|---|
| T1 SPARC | the rotmod Vdisk, Vbul, Vgas terms (stars + HI×1.33) | none: the catalogue has no hot term, so 0 |
| T2 Tian+26 groups | 0.92 × M_bar (members' stars + any cold gas) | 0.08 × M_bar (paper's stated median observed X-ray gas fraction). Brackets: hot 0.04 and 0.16 |
| T3 X-COP | MSTAR profile (`*_mstar.fits`, 7 clusters) or the audit's imputed stars (median M*/M_gas at each radius, 5 clusters), exactly as the record's audit builds them | MGAS (`*_fgas_profile.fits`) |
| T4 Bullet | the progenitor stellar component rho_s (CFG625 variants; F26 stars, B2 adds the C06 BCG); Clowe+06 Table 2 aperture Ms | ICM grid gas + cool-core cloud; Clowe+06 aperture MX |
| T5 halo model | max(Moster13 stars, 0.10 f_b M_ta), capped at the retained baryons (0.10 = the census floor = stars + cold gas, the record's condensed retention, CFG543). Bracket HC-2: Moster stars only wherever f_ret > 0.10 | retained baryons minus condensed |
| T6 KiDS | Mgal = M*(1 + f_cold) | none in the record's source |

Cold gas in clusters is taken as 0 (declared). Hot-gas radial shape for T2: primary = the members' Hernquist tracer (as CFG543
treats M_bar); bracket X = β = 2/3 model with r_c = Re, truncated at 5 Re, total 0.08 M_bar inside 5 Re.

## 4. The reservoir (NOT derived; bracketed; every conclusion is labelled with the bracket it needs)

- **R0:** no reservoir inside the measured radii (the record's convention for galaxies and groups, CFG543 P2; merger case L).
- **RI (identity reading):** cold energy inside r = max(settled phantom(<r), 5.364 × M_b(<r)) (the record's cluster convention,
  CFG4 / CFG624 "B identity").
- **RN (NFW placeholder, CFG629 / CFG432):** reservoir mass = supply − settled phantom within r200, distributed as NFW with
  c = 4 (r_s = r200/4) truncated at r200. Concentration brackets c = 3 and c = 5 reported. r200: Ettori+19 R200 (X-COP), the
  progenitor's r200 (Bullet), r200c of the whole catchment mass M_bar/0.10 + supply (groups; an upper bound on how much of the
  reservoir sits inside the members).
- Supply: groups 5.364 M_bar/0.10 (CFG543 P2 containment); X-COP 5.364 M_b(<R200)/0.90 (census f_ret cap; gas and stars
  log-extrapolated from the last three data points if R200 lies beyond the data); Bullet 5.364 M_b (CFG629).

**Joint gate J:** H-CB (and, for comparison, B) is coherent only if ONE reservoir rule passes T2, T3 and T4(b) together. If none
does, the label is NO SINGLE RESERVOIR RULE, and the record's split convention (R0 for groups, RI for clusters) is reported as
the reason.

## 5. Gates and rules (pass / fail per footing; footings never pooled)

**T1 SPARC** (CFG624 G1 harness, CFG487 SPARC code exec'd read-only). PASS if rms_HCB ≤ 0.12 dex and |rms_HCB − rms_B| ≤ 0.005 on
both footings; FAIL if rms > 0.15. Also verify that the rotmod columns carry no hot-gas term. This is a CHECK, not a discovery.

**T2 Tian+26 groups** (CFG543 machinery imported read-only; P2 supply; class-A edge; statistics as CFG543: Z = mean/σ_tot).
Primary cell: R0, hot 0.08, Hernquist hot shape. CLOSES (|Z| < 2) = PASS; |Z| ≥ 2 = FAIL (ABOVE or BELOW). Brackets: hot
0.04 / 0.16, hot shape X, Re conversion k = 1.563 (addendum), reservoir RN and RI. Label RESERVOIR-DEPENDENT if any reservoir
bracket flips the primary label; HOT-FRACTION-DEPENDENT if a hot bracket flips it.

**T3 X-COP** (the record's corrected audit rows as CFG4 / CFG624 read them; stars and gas re-split from the audit's own profile
code). η = M_HSE / M_model at each cluster's last audit radius (the CFG4 headline radius), median over 12, σ = SD/√12.
PASS |η − 1| ≤ 0.20 on both footings; FAIL if η ≥ 1.30 or ≤ 0.77 with |η − 1|/σ ≥ 3 on both; otherwise TENSION. Evaluated for
R0, RI, RN (c = 4 primary; c = 3, 5 reported). Reported, not gates: the inner band 200–420 kpc (same thresholds, labelled),
b = 0.2.

**T4 Bullet** (CFG625 Progenitor625 variants, B1 primary; BASE, B2, B3 reported; Clowe+06 Table 2 apertures via the record's
`bullet_data_table.py`; Σ_crit as CFG4 H5). No merger grid is launched.
- (a) Gas-tied share of the non-baryonic projected mass inside 250 kpc of each BCG: H-CB must be 0 by construction (numerical
  check, ≤ 1e-12). For B, the gas-tied share = 1 − M_ph(stars only)/M_ph(all baryons), reported.
- (b) Aperture convergence contrast (galaxy minus plasma aperture, 100 kpc radius, measured positions; dark components centred
  on the BCGs; aperture baryons from the table): PASS if |Δκ_model − Δκ_obs| ≤ 2σ and Δκ_model > 0 for main AND sub; FAIL if
  either misses by ≥ 3σ; else TENSION. Per reservoir R0 / RI / RN. B at α = ∞ (gas-sourced phantom centred on the plasma) reported
  as comparison.
- (c) Main-cluster projected M(<250 kpc) / Paraficz+16 (PROVISIONAL, recalled) reported with label; within 0.7–1.3 noted. Sub
  reported only (input-mass-limited per CFG629).

**T5 growth proxy** (CFG556 halo model exec'd read-only; CONTEXT ONLY: Tinker08 HMF, Tinker10 bias, Duffy08 concentrations,
Moster13 stars are ΛCDM-inherited; no native verdict). Same profile builder with the phantom sourced by condensed baryons only;
baryons placed exactly as in CFG556 (truncated at B's census edge); the H-CB settling edge from the census formula with the
condensed source (re = r_M,c / ln(1 + M_c/supply)), capped at r_ta; unsettled remainder as in CFG556 (drained shell / NFW).
E = max(R − 1), D = min(R − 1) over 0.05 ≤ k ≤ 1. Class: REMOVED if E ≤ 0.10 and D ≥ −0.10; REDUCED if E ≤ E_B/2; else NOT
REDUCED. Reported: the emergent edge, HC-2, R at k = 0.3 and 1, σ8 ratio.

**T6 KiDS / isolated lenses** (CFG529 / CFG531 record). NO CHANGE if the record's lens source holds no hot gas (verify
Mgal/10^logM − 1 = f_cold ≥ 0 from the catalogue); then the record's CFG529 numbers carry over unchanged. Reported: the share of
the law's boost a hot-gas escape (CFG61 class) keeps under H-CB (hot gas Newtonian only), and whether H-CB touches the KiDS
early-type age signal (CFG585 / CFG631).

## 6. MUTATE controls (all must bite, or the lane is VOID for that gate)

- **M1, hot gas restored to the source** must reproduce the record's candidate-B numbers: T1 = CFG624's B rms (1e-9); T2 R0 =
  CFG543 P2 means (+0.0596 / +0.0435, to 1e-4); T3 R0 = CFG624 NCE η (1.8196 / 1.6787, 1e-6) and RI = CFG4 identity 0.9457
  (1e-6); T4 R0 = CFG625 static B1 tot_p250 ratios (0.323 / 0.169 can), RN BASE = CFG629 (0.84 main); T5 = CFG556 primary E
  (+0.715 / +0.883, 1e-3).
- **M2, all baryons removed from the source** must break galaxies: T1 rms > 0.15 on both footings; T2 must not CLOSE.
- **M3, teeth for T5:** H-CB must differ from B by ≥ 0.01 in R(k = 1) on both footings, or T5 is NOT DIAGNOSTIC.

## 7. Overall verdict rule

- **H-CB FAILS** if T2 or T3 fails under EVERY reservoir bracket, or T1 fails.
- **H-CB SURVIVES (conditional)** if T1 passes and T2, T3, T4(b) pass under one common reservoir rule (J), with that rule named.
- Otherwise **NOT DECIDED (reservoir-limited)**, with each gate's dependence stated.
- T5 can only move the growth reading as CONTEXT. The native verdict needs the PM shear test (spec written in the README; it
  is NOT run here: the 1024³ job occupies the machine).

## 8. Machine and data

One process, < 1.5 GB, nice -n 10; the running cfg596_pm.py and cfg625 jobs are not touched. No downloads. Data used: SPARC
rotmod (via CFG487), Tian+26 VizieR table (CFG540 path), X-COP FITS + Ettori json, Clowe+06 table (record script), KiDS lens
catalogue. Outputs: `cfg634_*.out`, `cfg634_*_results.json`, `_MUTATE` variants.
