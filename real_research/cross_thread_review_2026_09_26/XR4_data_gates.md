# XR4 — orphaned empirical tests, and what the current construction does to the standing liabilities

Cross-thread review, 2026-09-26. Read-only on every committed file. The four `XR4_*.py` scripts next to this file are new, each runs in 2–20 s, and each carries a control that reproduces a committed number. Both a0 footings are used throughout (canonical 9.36e-11, alt 1.13e-10 m s⁻²).

"The construction" means L359's vacuum-gated switch, L361's bound-region kernel and a carrier. In the regime tested here the kernel is ν_RAR, which ν_mono equals below y = 2.54 and matches to 0.01 dex everywhere (commit 9092fc0fd).

## Ranking: decisiveness × cheapness

| Rank | Test | Status before this review | What XR4 finds | Cost to close | Decisive? |
|---|---|---|---|---|---|
| 1 | **Local Group zero-velocity radius under the construction** | Never run for the construction. The ~30-group version was never run, and cannot be (item 1). | L361 screens out the external-field rescue. The gated edge only partly compensates, so **R₀ = 1.28–1.62 Mpc against 0.96 ± 0.03 (+0.13 to +0.23 dex)** across the DE2 window, on both footings and for any carrier history. | Done here (19 s). Next step is a two-body (MW + M31) or PM check of the spherical model. | Yes, on one system, at about 2–4σ once model systematics are included. |
| 2 | **The two 09-03 EFE liabilities under L361** | Never re-scored (no file after 09-03 cites `k_contrarian_*`). | Dwarfs: **unchanged, 3.9–4.5σ** (in-region circumgalactic gas only makes it worse). Clusters: the slope drops to 2.4–2.9σ in the committed form, or 3.5–4.2σ in the QUMOND subtract form. **The zero point rises to 2.8–3.1σ.** Not a rescue. | Hours: a 3-D QUMOND disc-in-a-uniform-field factor with the repo's own solver. | Yes. The form ambiguity is worth about 1σ and is the thing to settle. |
| 3 | **Gas in active filaments at z ≲ 1** (L357–L361 open item 1) | Never computed. The "×8–12" appears only in docs (df81d0b72) and has no script. | The ×8–12 is reproduced as arithmetic. Filaments with δ ≳ 4–6 are ACTIVE at z ≤ 0.5 under the DE2 gate. The force there is ×3.5–10 and infall takes 3–6 Gyr, less than the time since z = 1, so an O(1) response is expected. | About a day: extend the L347/L359 PM machinery to z = 0 with the switch on in filaments. The data are published but not on disk (the ACT+Planck y-map is). | Likely yes. Filament y and low-z line widths respond at O(1). |
| 4 | **Blind map-level tSZ score** | The map IS on disk (`deepseek_push/Z06_data/ilc_actplanck_ymap.fits`, 1.78 GB, gitignored). Two of four clusters were staged on 09-16. The promised verdict "by 2026-10-07" (`deepseek_push/Z06_tsz_pull.out:72`) is not delivered. | Two defects. A2319's "JOINT" verdict compares the prediction with a synthetic copy of itself, not with data (`Z06_tsz_pull.out:44`). The registered window (−1.7, −0.9) belongs to the pre-carrier phantom-zone model, and the construction's own tSZ slope has never been derived. | About a day, plus deriving the construction's prediction first. | Only for the superseded model, as registered. |
| 5 | **Brouwer+21 all-galaxy lensing (Fig. A4)** | The data are on disk (`real_research/data/lensing_rar/brouwer2021_rar/Fig-A4_*`). They were used only by 09-03 hunt scripts on isolated MOND. Flagged as not done at `real_research/generated_phantom_2026/README.md:32`. | Not run here; it needs a satellite/central halo model. | 1–2 days on L363's halo model. | Moderate. L363 cosmic shear already fails L361, and GP5 closes GP4. |
| 6 | Dated external gates | See item 5 | No change | — | — |

## Item 1: zero-velocity radii of Local Volume groups

**What was run (all 09-03, commit d4343a4b3):**
- `hunt_2026/k02_lambda_edge_zvs.out:72,74`: isolated deep MOND over-predicts by ×2.03 (canonical) / ×2.13 (alt) on 5 groups.
- `k04_lambda_edge_efe_closed`: the external field needed is 0.39× the external field supplied.
- `k07e`: the LG alone.
- `k_dimensional_turnaround_groups` (7 groups): only the LG gives a stable R₀. Its Monte Carlo recovers a known R₀ to 0.066 dex around the LG but only to 0.22–0.37 dex around external groups, because the ~100 km s⁻¹ flow scatter is the limit (`.out:72,78`).
- With the LG's own measured external field, standard MOND lands at −0.094 dex (`.out:191–192`).
- The Kourkchi–Tully R_2t trap is recorded and avoided (`k02_lambda_edge_zvs.out`, check K02e).

**The follow-up premise does not hold.** "~30 groups → σ ≈ 0.068 dex, a 4.5σ decision" (`predictions_2026/SECOND_LAW_HUNT_2026.md:570–573`) is 0.371/√30. `XR4_ungc_group_census.py` applies k_dimensional's own selection to all 161 UNGC main disturbers:
- 58–59 have ≥ 8 usable Hubble-flow galaxies.
- **Only 6–8 pass the stability criterion.** Most of those are LG members (NGC 205, LMC, M33, NGC 3109) re-measuring the LG flow, or small hosts inside larger groups (M82, NGC 4449, NGC 4244).
- The control reproduces the committed N for all 7 groups and R₀(LG) = 0.906.
- The ensemble test is not runnable on the catalogue on disk.

A small documentation nit: the committed code fits from R = 0.15 Mpc (`k_dimensional_turnaround_groups.py:161`), while its text says 0.7 Mpc (`:157`). This changes nothing for the LG (0.906 either way). It does change N for external groups (for example M81: 29 → 20).

**The LG alone now tests the construction.** L361 screens every field from outside a bound region (`real_research/g03_audit_2026/L361_bound_region_kernel.py:26–30`), so the external-field rescue used on 09-03 is unavailable. `XR4_lg_zero_velocity_construction.py` uses k02's point-mass + Λ shell model with three changes:
- the phantom exists only inside r_e(z) = v_f/(H √(x_c0 E^{2p} + 1.5 Ω_m(z))), DE1's closed form;
- beyond r_e a shell feels Newtonian gravity from baryons + carrier only;
- the carrier is placed inside the shell, which is an upper bound on its effect.

Controls:
- k02's 1.929 / 2.021 Mpc are reproduced exactly;
- the Newtonian 3.178e12 M☉ inversion (1.176 Mpc) is reproduced;
- step convergence holds to 0.0%;
- kernel-off makes every gate cell identical (0.388 Mpc);
- a reversed gate moves R₀ back toward isolated MOND.

Results:

| M_b (M☉) | footing | isolated MOND | DE2 window p = 1, x_c0 = 2.0 / 2.5 / 2.97 |
|---|---|---|---|
| 1.145e11 (k02: stars + cold gas) | canonical / alt | 1.93 / 2.02 | 1.40 / 1.33 / 1.28 — 1.46 / 1.40 / 1.34 |
| 1.72e11 (with CGM / M31 stellar mass) | canonical / alt | 2.14 / 2.24 | 1.55 / 1.48 / 1.42 — 1.62 / 1.55 / 1.49 |

- The carrier moves R₀ by less than 3% (none, decay or kept).
- Only one cell enters the pre-declared ±0.10 dex band: p = 2, x_c0 = 2.97 at the lower mass (1.19 Mpc, +0.09 dex). That cell lies above DE1's flagship cap on p (p_max = 1.89 / 1.99 at x_c0 = 2.5, falling with x_c0; `DE1_vacuum_gate_flagship.out:111–112`).
- The mass slope stays 0.251, because the edge scales like v_f.
- Against 0.96 ± 0.03 plus about 0.05 dex of model systematics (the same model gives ΛCDM an LG mass of about 1.7–1.9e12), this is **a 2–4σ liability, and a new one**: the construction trades the KiDS pass for the Local Group's Hubble flow.

## Item 2: the EFE liability under L361

**What L361 says.** Inside a region, w is the Newtonian potential of all in-region baryons, so the EFE is standard QUMOND sourced by baryons. Fields from outside are screened. Both samples sit inside their host's region: the edge is ~2 Mpc for the LG and ~8–10 Mpc for PSZ2 clusters. `XR4_efe_under_region_kernel.py` found 0% of cluster members beyond the edge.

**(ii) Local Volume dwarfs.** The committed test already used host baryons (`hunt_2026/k_contrarian_dwarfefe.py:57–58`), so **the construction predicts the same EFE**:
- statistic C: −0.1006 / −0.1026 against the observed +0.0800 ± 0.0467, which is 3.87 / 3.90σ (control reproduced);
- adding in-region hot gas (hosts ×1.5 / ×2) gives 4.20–4.48σ;
- screening the 2 dwarfs beyond 1.2 Mpc changes nothing.

**(i) Cluster infall.** The committed prediction fed ν the Newtonian equivalent of the TRUE SZ-mass field (`k_contrarian_clusterbtfr.py:200`). L361 instead reads e_N = f_b(r) g_true, the cluster's baryons.
- **This is not a weaker EFE.** e_N is 1.9× (canonical) / 2.3× (alt) larger at the median member, but it scales ∝ g_true (d log e_N/d log g_e = 0.88–1.00) instead of ∝ g_true² (1.85–1.87).
- **Slope:** −0.070 to −0.086 in the committed scalar-sum form (2.4–2.9σ, from 4.5σ); −0.104 to −0.123 in the QUMOND 1-D subtract form (3.5–4.2σ; the committed prescription in that form gives 6.6σ).
- **Zero point (members − field):** predicted −0.038 to −0.040 against −0.0119 ± 0.0092, which is 2.8–3.1σ (the committed value was 2.4σ).
- The pre-declared check E2 FAILS: the liability is not materially weakened.
- Combined with the dwarfs, the EFE stays at about 4.5–6σ in quadrature, treating the two samples as independent.

**What would settle the cluster channel:**
- the angle-averaged 3-D QUMOND EFE factor for a disc (the scalar-sum vs subtract ambiguity is about 1σ; a validated derivative-free QUMOND solver already exists, `hunt_2026/f16_curl_field_fork_on_discs.py:185`);
- per-cluster measured f_gas(r) instead of a template;
- resolved rotation curves, to remove the W50 and stripping confound the committed script itself lists.

**Consistent, not decisive.** L361 predicts zero web-EFE for isolated galaxies. That matches KiDS (e_N < 2.6e-5, `hunt_2026/k_dimensional_efe_break.out:204`), by construction, and the WALLABY null (`hunt_2026/h28_chae_efe_wallaby.out`), which is underpowered (N ≈ 1313 needed).

## Item 3: Brouwer+21 Fig. A4

**Status:** never run against GP1–GP4 or L361.
- The all/isolated split is measured: +0.40 dex (+152%) at the lowest g_bar (`hunt_2026/h111_h112_kids_ml_machine.out:107–115`).
- The construction must reproduce it with region phantoms, the in-region EFE on satellites, and host terms.
- **Cost:** a central/satellite halo model built on L363's region-phantom halo model, about 1–2 days.
- **Priority:** moderate. It is the natural independent check of any cosmic-shear repair, but L363 already fails L361-assembled.

## Item 4: active-filament gas at z ≲ 1

**Status:** open and uncomputed (`real_research/reviews/THE_THEORY_AS_IT_STANDS_2026-09-22.md:65`). No low-z forest or filament-stack data are on disk.

`XR4_filament_gate_arithmetic.py` reproduces the recorded numbers: ν = 54–93, force ×9.3–15.5, infall 17–30 → 5.7–7.6 Gyr at z = 0, δ = 1–5, R = 1 Mpc. It also shows the untested population is large:
- the DE2 gate activates δ ≥ 3.7–6.3 at z = 0–0.5 (density-only x̃, an upper bound);
- in such filaments the force is ×3.5–10 and infall takes 3.2–5.9 Gyr, shorter than the 7.9 Gyr since z = 1.

**Deciders:**
- low-z Lyα (HST/COS P1D and the b–N distribution);
- filament tSZ stacks (published LRG-pair measurements; the ACT+Planck y-map on disk could give a new stack with a pair catalogue).

**Cost:** about a day of PM work, then published comparisons. **Plausibly decisive.**

## Item 5: dated external gates (as the repo records them)

| Gate | Date / gate | Evidence |
|---|---|---|
| Gaia DR4 wide binaries (frozen pre-registration; Amdt 11: Arm A 1.1614–1.1814 / 1.1917–1.2267, Arm B ceilings 1.0450 / 1.0300) | **2026-12-02** release; analyses ~Q1–Q3 2027, gated on triple rejection. L361 keeps the Sun and wide binaries in the Galaxy's field (R2), so the registration is untouched. | `STANDING.md:118` (HEAD); `real_research/DATA_GATE_PREREGISTRATION_2026.md:161–164` |
| Euclid DR1 weak-lensing RAR (+ A-6 cluster kink, A-7 isolated lenses) | Nov 2026 images only; shear catalogues mid-2027 at the earliest; Brouwer-style VAC ~late 2027–28 | `DATA_GATE_PREREGISTRATION_2026.md:69–76`; `PREDICTIONS_LEDGER_2026-09-02.md:36–37` |
| z ≈ 2.5 deep-MOND BTFR zero point (0.00 vs +0.33 dex) | Data-gated: 0 of the 2–4 clean rotators needed; new NIRSpec + ALMA time required, no date in the repo (DOI 10.5281/zenodo.22563139) | `STANDING.md:119` (HEAD); `THE_THEORY_AS_IT_STANDS…:344`; commit 9f7572c58 (Z2ETA) |
| Blind map-level tSZ | Data on disk; "by 2026-10-07" self-deadline | `THE_THEORY_AS_IT_STANDS…:345`; `deepseek_push/Z06_tsz_pull.out:72` |
| Cluster lensing cores; COS1 outer WL slope | Need HST / stacked shear beyond R500; data gate not met | `THE_THEORY_AS_IT_STANDS…:346`; commit e9e792d03 |
| DESI DR3 w(z) gate / Rubin–LSST SN | ~2026–27 / ~2027+ | `real_research/predictions/README.md:58`; `PREDICTIONS_LEDGER…:33` |
| Gaia DR4 asteroids (SME s̄^μν) | Ships 2026-12-02; verdict ~2028–32 | `DATA_GATE_PREREGISTRATION_2026.md:230–232` |
| BIG-SPARC environmental fork; WALLABY/MaNGA directional EFE | Not public; public data but N ≥ 560 needed (weeks) | `PREDICTIONS_LEDGER…:34,38` |
| ELT/HARMONI a0(z) | Early–mid 2030s | `DATA_GATE_PREREGISTRATION_2026.md:261` |

## Files created (only these)

- `XR4_data_gates.md`
- `XR4_efe_under_region_kernel.py` / `.out` / `_results.json`: 5/6 checks pass. E2 fails by pre-declaration. The first run had a units bug (the edge screened every member); it was caught by the 100% flag and fixed, and guard G1 was added.
- `XR4_lg_zero_velocity_construction.py` / `.out` / `_results.json`: 5/6. Z2 fails, which is the finding. The first version used a fixed radius grid that could not resolve the zero-velocity shell; it was replaced by bracketing.
- `XR4_ungc_group_census.py` / `.out` / `_results.json`: 1/2. N2 fails, which is the finding.
- `XR4_filament_gate_arithmetic.py` / `.out` / `_results.json`: 2/2.
