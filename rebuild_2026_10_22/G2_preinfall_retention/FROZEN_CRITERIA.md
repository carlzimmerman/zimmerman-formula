# G2_preinfall_retention FROZEN CRITERIA (2026-10-22): does a "pre-infall retention rule" (PAPER36 transplanted to satellites) close the dwarf-satellite gap?

Written and committed alone (with `ASSUMPTION_LEDGER.md`), before any script or number of this lane. Rules:
`rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`, `BRIEF_E_AUDIT.md`. κ = ½ FITTED. Footings
9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold energy, no particle. Never "theory closed". Never "the data favour the
framework". Every run `OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, minutes. No downloads. CFG960 untouched.

**Not blind.** Seen before freezing: E3 (+0.89 ± 0.13 dex canonical / +0.85 alt above the screened prediction, L★ = 24 pc,
45/46 systems), E6 (catchment not fixed by the dynamics; chemistry floor L_min median 38), CFG936 (TDGs/DF2/DF4 at Newton
under zero supply), CFG939 (S4 free population not derivable), CFG888 (extra cold energy has no law self-boost), CFG842,
PAPER36 / CFG35 text. No number of this lane was computed before this commit. The hypothesis is an outside suggestion.

## 0. The hypothesis (H-PIR)

- ζ = 1: a system that collapsed before falling into its host keeps the cold mass it collapsed with, inside its tidal radius
  (PAPER36's "the cold component keeps its collapse mass").
- ζ = 0: a system formed after infall, or stripped below its tidal radius, keeps none (TDGs, NGC 1052-DF2/DF4 → Newton).
- Claim: zero new constants; brings the satellites to the screened prediction without breaking TDGs and UFDs.

## 1. The rule, transplanted literally from PAPER36 eq. (1) (CFG35 conservation form)

For a ζ = 1 system with collapse mass M_coll, collapse profile m_P(r) (fraction of M_coll inside r) and tidal radius r_t:

- retained cold: M_c,ret(<r) = (1 − f_b) M_coll m_P(min(r, r_t));
- f_ex = max(0, 1 − M_ph(<r_t) / M_c,ret(<r_t))   (PAPER36's M_ph,edge → the phantom inside the tidal edge);
- **M_pred(<r12) = (M*/2)·B_scr + f_ex·M_c,ret(<r12)**, with (M*/2)·B_scr exactly E3's screened prediction (L★ = 24 pc;
  baryons + tethered phantom).
- ζ = 0: M_pred(<r12) = M*/2 (Newton; no supply, so no phantom; CFG936 route (i)).
- ζ assignment (the suggestion's own criterion): ζ = 0 iff z_coll ≤ z_inf (formed after infall) or r_t,peri ≤ r12
  (stripped inside the half-light radius); otherwise ζ = 1.

Inputs the rule needs and the brackets used (no fitting, no scan to target):

| input | cells | class |
|---|---|---|
| M_coll | FREE: M_b/f_b (f_ret = 1, present baryons only); CHEM-cons / CHEM-nom: L_min·M_b/f_b with E6's L_min at (log y −0.5, W2) / (+0.1, W1), read-only from `e6_per_system.csv`; CENSUS: M_b/(f_b·0.10); SHMR: Moster+13 (PAPER36's own route; formula of `hunt_2026/h48`, extrapolated below its 1e9 grid) | FREE native floor; CHEM conditional (SURVEY-CAL + MODEL); CENSUS, SHMR ΛCDM-PROCESSED |
| m_P(r) | TH: virialised top-hat, uniform inside r_vir with ρ = 18π² ρ̄_m(z_coll); B85: self-similar secondary infall M ∝ r^{3/4} inside the same r_vir; NFW: Dutton–Macciò c(M) at z = 0, R200c (PAPER36's own, h48 formula) | TH, B85 FRAMEWORK-NATIVE (GR dust outside the law ball, E6 D1); NFW ΛCDM-PROCESSED |
| z_coll | {6, 10, 15} bracket (UFD stars ancient; no per-system native value) | MODEL BRACKET |
| z_inf | MW satellites with LVD PMs: apocentre in the framework host law field (MW baryons 6e10), infall when the host turnaround radius R_ta(t) = R_ta0 (t/t0)^{8/9} reaches r_apo; R_ta0 ∈ {0.83, 1.10} Mpc. No PM (M31 hosts): r_apo ∈ [d, 2d], r_peri ∈ [0.3 d, d] | RAW PMs + SURVEY-CAL solar motion; R_ta0 SURVEY/record (CFG548 K4 1.05–1.09 Mpc LG flow; MW-only scaled by (½)^{1/3}) |
| r_t | Jacobi radius at pericentre in the host law field: M_sat(<r_t) = (Ω² − dg/dr) r_t³/G, M_sat = M_b + max(M_ph, M_c,ret) | FRAMEWORK-NATIVE law; host baryon masses SURVEY-CAL/external |
| f_b | Ω_b/Ω_m = 1/(1 + 5.364) | ΛCDM-PROCESSED (Planck; CFG886 recovered via BAO+BBN, not pinned) |

**Primary native cell (fixed now):** CHEM-cons × TH × z_coll = 10 on the systems with an LVD [Fe/H] (E6's 36 / 37);
FREE × TH × z_coll = 10 on all 45 / 46. The native set = {FREE, CHEM-cons, CHEM-nom} × {TH, B85} × {6, 10, 15}.

## 2. Statistic

O = median over systems of log10(M_dyn / M_pred), clean primary data exactly as E3 (LVD σ × Arroyo-Polonio free-f binary
ratio, Υ_V = 2, Wolf 3σ²r12/G, r12 = 4/3 R_e), uncertainty s from bootstrap over systems × per-system MC (σ, R_e,
distance modulus). Per footing.

## 3. Checks (script prints `Kn PASS/FAIL value threshold`)

- K1: own LVD pipeline gives N = 45 / 46 and E3's clean-primary offset above the screened prediction, +0.89 / +0.85 within
  0.03 dex.
- K2: per-system B_scr and M_dyn equal E3's `e3_per_system.csv` to ≤ 1e-6 relative (canonical).
- K3: limits: M_coll → 0 returns the screened prediction exactly; ζ = 0 returns Newton exactly.
- K4: orbit roots: E − Φ(r) − L²/2r² = 0 at r_peri and r_apo to ≤ 1e-8 relative; computed Galactocentric distance vs LVD
  `distance_gc` median |Δ| ≤ 2 %.
- K5: per-system L_req recomputed here equals E6's `L_req_F1` within 1 % (median).
- K6: the rule moves the offset: |O_rule − O_E3| > 0.01 dex in at least one native cell (MUTATE M_coll → 0 must FAIL K6).

## 4. Verdict lines (per footing; the verdict is the native set's)

- **CLOSES THE GAP:** |O| ≤ 2s at the primary native cell AND in every native cell AND no breakage (§5).
- **PARTIAL:** at the primary native cell O is reduced by ≥ 0.2 dex vs E3 but |O| > 2s (report the fraction closed
  1 − O/O_E3 and the native-set range), or it closes at the primary but not across the native set.
- **FAILS:** primary native O reduced by < 0.2 dex, or the native cells overshoot (O < −2s) or break §5.
- **RESTS ON A NON-NATIVE INPUT:** added (not exclusive) if CENSUS, SHMR or NFW cells close (|O| ≤ 2s) where the native set
  does not; name the input.

## 5. Breakage tests (gating for CLOSES)

- B1 TDGs (6 Lelli+15): the rule's criterion gives ζ = 0 (formed from tidal debris after the interaction) → Newton;
  residual vs Newton read from CFG936's committed JSON / recomputed from `real_research/data/tidal_dwarfs/lelli2015_tdg.csv`;
  breaks if the ζ assigned by the criterion leaves them > 2σ from the data.
- B2 DF2/DF4 (CFG657 table: M*, R_e, σ, ages 8.3/10.7 Gyr; host NGC 1052 baryons 1e11 external, projected distances from
  CFG657 positions at 20 Mpc): test whether the criterion itself gives ζ = 0 (r_t at projected distance ≤ r12, i.e. stripped);
  if it gives ζ = 1, compute the ζ = 1 prediction (FREE × TH × z 10 and CENSUS) and call it broken if σ_pred exceeds the
  observed upper 2σ.
- B3 UFD overshoot: in the primary native cell, number of the 45 with M_pred > M_dyn at > 2σ (per-system MC); broken if ≥ 5;
  compact UFDs (Segue 1, Willman 1, Carina III) listed.
- B4 (reported, not gating): isolated LVD local-field dwarfs (ζ = 1 by construction, never infall), same statistic vs
  their observed σ.

## 6. Mutation

`--mutate`: M_coll → 0 in every cell. K6 must FAIL and the verdict must return E3's offset. Output `*_MUTATE.*`.

## AMENDMENT A1 (PRE-RESULT, before any script output of this lane)

Reading E3's code (not its numbers) shows `e3_per_system.csv` stores per-system **MC medians** (E3's own seeded RNG), not
central values. A ≤ 1e-6 identity is impossible with an independent pipeline. K2 is replaced by: this lane's per-system MC
medians of B_scr and M_dyn vs the CSV, **median |relative difference| ≤ 2 % and max ≤ 10 %** (canonical). Nothing else
changes.
