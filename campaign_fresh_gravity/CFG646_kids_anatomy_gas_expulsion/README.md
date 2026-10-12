# CFG646: anatomy of CFG596's raw-KiDS exclusion, and the framework's own gas expulsion (the PM omitted it). Expulsion is a FEW-PERCENT effect; it cannot remove the 19–25% excess. CFG596's verdict is unchanged

- **Date:** 2026-10-12. **Declarations** (committed alone, before any code or number): `DECLARATIONS.md`, 3c1c5a42f.
  **Native-run FROZEN CRITERIA + PM spec** (committed alone, NOT RUN): `FROZEN_CRITERIA_NATIVE.md`, 741a8adcc.
- **Settings:** κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 are never pooled. The cold energy's MASS is still
  required; no particle species. Not "theory closed". Parts (i) and (ii) are POST-HOC DIAGNOSTICS and ESTIMATES; they carry
  no verdict.
- **CFG596's verdict is unchanged:** canonical KiDS EXCLUDED (Δχ² +68.7), DES NOT DIAGNOSTIC, alt PENDING.
- **Scripts** (each one process, nice 10):

  | script | outputs | run time / peak RSS |
  |---|---|---|
  | `cfg646_anatomy.py` | `.out` / `.json` | about 80 s |
  | `cfg646_expulsion_hm.py` | `.out` / `.json` | 15 s |
  | `cfg646_expulsion_pm.py [P1 530can 530alt]` | `.out` / `.json` | 2.4 / 3.0 / 2.9 GB, one process per source |
  | `cfg646_propagate.py` | `.out` / `.json` | about 4 min |

  `cfg646_lib.py` exec's cfg596_native.py's library unchanged, which exec's CFG592's library unchanged.
- **Numbers:** every number below is from a committed JSON.

## Bottom line

1. **Anatomy (KiDS canonical, +68.7).**
   - About three quarters of the Δχ² comes from k < 1 h/Mpc, mostly k 0.3–1. The framework spectrum below k = 1 alone gives
     +52.1; above k = 1 alone it gives +14.5.
   - ξ− carries more than ξ+, the high-z pairs 4-5, 5-5 and 4-4 dominate, and both small (≤ 6′) and intermediate (25–50′)
     angles contribute.
   - DES (+22.4) is entirely k < 1 (+22.2 from below k = 1, −0.2 from above).
2. **The PM omits the framework's own expulsion.** CFG596's engine feeds only the retained baryons, f_ret(x)(1 + δ), to the
   MOND input. Its Newtonian source is the FULL particle density (`_finish_phik`: (−1.5 Ω_m/a) δ_k/k²). So the census
   non-retained baryons, f_b(1 − f_ret)(1 + δ), still gravitate as collisionless mass inside every catchment. That is 3.4% of
   all mass at z = 0 and 3.7% at z = 0.5–1 in CFG596 P1.
3. **Moving them out per the record (PRIMARY: CFG632 DIFF) lowers the gravitating P(k) by:**
   - 2–3% at k = 0.3;
   - 3–5% at k = 0.5;
   - 4–8% at k = 1 (deeper at higher z);
   - 5–10% at k = 2.

   The framework's own boost is +19 / +25 / +21 / +10% at k 0.3 / 0.5 / 1 / 2. **At z = 0, expulsion removes roughly 15–30%
   of the excess, not the excess.**
4. **Estimated KiDS canonical Δχ² with expulsion: +51.7 (PM-native DIFF-S) / +53.7 (halo-model DIFF).**
   - All placements give +36 to +62; every one is ≥ 9, the EXCLUDED level (estimate, not a verdict).
   - χ²(F′) stays at p ≤ 8e-5 on the raw data.
   - DES: +18.8 / +18.5, range +3.3 to +22.0 (DES stays NOT DIAGNOSTIC by its tooth).

## (i) Δχ² anatomy (post hoc diagnostic; reproduction gate A0 PASS: +68.726 / +22.365 reproduced exactly)

**Decomposition of the canonical Δχ².** The per-point split is c_i = r_i (C⁻¹r)_i, which sums exactly to χ²_data. "Fixed"
means F evaluated at S0's best-fit nuisances.

| | KiDS (N 104) | DES (N 52) |
|---|---|---|
| total Δχ² | +68.73 = data +54.42, nuisance prior +14.31 | +22.37 = data +16.01, prior +6.36 |
| fixed-nuisance Δχ² | +75.10 | +30.25 |
| ξ+ / ξ− (data part) | +20.0 (n 39) / +34.5 (n 65) | — (no ξ+ kept) / +16.0 (n 52) |
| θ ≤ 6′ / 12–25′ / 50′ / ≥ 100′ | +22.6 / +19.2 / +9.8 / +2.8 | (all kept θ ≥ 28′) 28–57′ −0.2; 71–113′ +14.2; 142–225′ +1.9 |
| top tomographic pairs | 4-5 +26.4, 5-5 +12.9, 4-4 +9.2, 3-4 +5.8 (low-z pairs ≈ 0 or negative) | 3-3 +6.6, 4-4 +5.5, 3-4 +3.1 |
| points by median integrand k: <0.3 / 0.3–0.5 / 0.5–1 / 1–2 / >2 | +0.6 / +8.5 / +25.3 / +18.9 / +1.1 | +2.5 / +14.5 / −1.2 / +0.1 / — |
| Δχ²-weighted integrand k fraction: <0.3 / 0.3–1 / 1–2 / >2 | 0.18 / 0.38 / 0.22 / 0.22 | 0.42 / 0.37 / 0.11 / 0.09 |

**k-swap refits.** Each refit uses the framework spectrum on one side of k_c and S0 on the other.

| k_c (h/Mpc) | KiDS: F only below k_c | KiDS: F only above k_c | DES: F only below | DES: F only above |
|---|---|---|---|---|
| 0.3 | +10.0 | +57.3 | +13.2 | +7.2 |
| 0.5 | +25.0 | +40.8 | +19.1 | +2.4 |
| 1.0 | **+52.1** | **+14.5** | +22.2 | −0.2 |
| 2.0 | +66.7 | +1.7 | +22.4 | −0.1 |

**Reading.**
- On KiDS, 56–79% of the Δχ² sits at k < 1, depending on the split; the k-swap gives 76%. About 42 of it lies in
  k 0.3–1.
- k > 1 carries 21–44%. The k-swap gives +14.5 (21%); the integrand-weighted split gives 44%. A correlated χ² has no unique
  split, and the k-swap is the cleaner of the two.
- k > 2 carries ≤ 2.
- DES is entirely k < 1.
- Expelled gas acts mostly at k ≳ 1, so most of the exclusion comes from scales where expulsion is weakest.
- The F fit also pays +14.3 (KiDS) in nuisance-prior cost: its photo-z shifts try to absorb the excess.

## (ii) Does the PM include the framework's expulsion? NO (read from `cfg596_pm.py`, the CFG527 census engine)

- **The particles are one collisionless species** carrying all of Ω_m. There are no baryon tags.
- **MOND input:** `pr = tab[code] * (1 + delta)`. Only the retained baryons source the phantom (census f_ret per catchment;
  code 0, outside resolved catchments, means f_ret = 1).
- **Newtonian source:** `phik = (-1.5 Om / a) * delta_k / k^2 - src_k / k^2`. delta is the FULL particle density, so the
  non-retained baryons gravitate where the particles are, inside the halos.
- **So the PM keeps the framework's expelled gas in the halos as collisionless mass.** The real sky does not.

## (ii) Framework-native expulsion: placement and estimates

**Placement.**
- **PRIMARY (declared from the record): CFG632 DIFF.** This is the census gas the raw FRB DMs accepted: no one-halo profile,
  the host's large-scale bias kept, mass conserved.
- **Brackets:**
  - SHELL: ρ ∝ r⁻² between r_edge and r_ta (CFG632's bracket).
  - NFW-shaped shell: CFG556 as written, whose drained shell is exactly the non-retained baryons.
  - DIFF-U: uniform, bias 0, maximal removal.
- **"From" side:** the omitted gas follows NFW (primary) or the framework's total profile (bracket).

**Estimate 1, halo model** (CFG556 machinery unchanged; Tinker/NFW-Duffy are CONTEXT ONLY, inside a ratio). Values are
P′/P_BASE at z = 0, where BASE is what the PM does.

| footing, from-shape | variant | k 0.3 | 0.5 | 1 | 2 |
|---|---|---|---|---|---|
| canonical, NFW | **DIFF (PRIMARY)** | **0.974** | **0.964** | **0.956** | **0.940** |
| canonical, NFW | SHELL / NFW-shell | 0.996 / 0.997 | 0.990 / 0.991 | 0.975 / 0.979 | 0.951 / 0.956 |
| canonical, NFW | DIFF-U | 0.913 | 0.933 | 0.944 | 0.935 |
| canonical, MF | DIFF | 0.972 | 0.961 | 0.946 | 0.921 |
| alt, NFW | **DIFF (PRIMARY)** | **0.974** | **0.965** | **0.958** | **0.946** |
| alt, MF | DIFF | 0.972 | 0.961 | 0.947 | 0.925 |

- **Census ε = (1 − f_ret) f_b** is 0.141 / 0.106 / 0.047 / 0.016 at log M_ta 12 / 13 / 14 / 15.
- **The DIFF drop at k = 1** (canonical, −0.044) is all one-halo: log M_ta 14–15 gives −0.023, 13–14 gives −0.016,
  15–16 gives −0.004 and 12–13 gives −0.003. The two-halo term contributes +0.001.
- **Resolved-only expulsion** (M_ta ≥ 2.06e12, the PM's catchments) differs from all-mass by ≤ 0.003 at k ≤ 2.

**Estimate 2, PM-native post-process.**
- **Method:** on each run's own 256³ fields, the engine's own cover_peaks / cover_balls / catch_labels were re-run with
  RMIN 0.78125, census f_ret, Δ_ta(z) and flat a0. Then δ_grav′ = δ_grav − e + place(e).
- **Resolution:** the catchments are rebuilt on a 4× coarser mesh (P1) or 2× coarser (CFG530), so this is an estimate.
- **Grid DIFF-S** is the grid realisation of the declared primary: Gaussian σ = catchment radius, host bias kept.

| source (footing, z) | expelled / all mass | DIFF-S (PRIMARY) k 0.3 / 0.5 / 1 / 2 | DIFF-F | DIFF-U | SHELL |
|---|---|---|---|---|---|
| CFG596 P1 (canonical, z 0) | 0.034 | **0.977 / 0.966 / 0.950 / 0.933** | 0.954 / 0.953 / 0.946 / 0.933 | 0.953 / 0.951 / 0.945 / 0.932 | 0.992 / 0.982 / 0.973 / 0.963 |
| CFG596 P1 (canonical, z 0.5) | 0.037 | 0.973 / 0.958 / 0.940 / 0.921 | 0.938 / 0.936 / 0.934 / 0.921 | 0.939 / 0.936 / 0.933 / 0.920 | 0.996 / 0.976 / 0.962 / 0.943 |
| CFG596 P1 (canonical, z 1) | 0.037 | 0.971 / 0.950 / 0.924 / 0.903 | 0.918 / 0.914 / 0.913 / 0.903 | 0.917 / 0.915 / 0.912 / 0.901 | 1.001 / 0.978 / 0.943 / 0.920 |
| CFG530 N512 (canonical, z 0) | 0.035 | 0.979 / 0.967 / 0.950 / 0.931 | 0.948 / 0.950 / 0.946 / 0.932 | 0.944 / 0.949 / 0.945 / 0.930 | 0.998 / 0.989 / 0.977 / 0.964 |
| CFG530 N512 (**alt**, z 0) | 0.034 | **0.979 / 0.968 / 0.951 / 0.933** | 0.949 / 0.952 / 0.947 / 0.933 | 0.945 / 0.951 / 0.947 / 0.932 | 0.999 / 0.991 / 0.981 / 0.968 |

- The halo model and the PM post-process (z = 0) agree to ≤ 0.007 at k ≤ 1 for the primary, on both footings.
- DIFF-F (field-placed) behaves like DIFF-U: the field it is placed into carries almost no large-scale bias.

**Propagation through cfg596_native's own projection, cuts, nuisances and fit** (`cfg646_propagate.py`; S0 untouched;
ESTIMATE). Baseline Δχ² is KiDS +68.73 and DES +22.37.

| ratio applied to the framework's P_grav nodes | KiDS Δχ²′ (χ²(F′), p) | DES Δχ²′ |
|---|---|---|
| **PM P1 DIFF-S (PRIMARY, per node z)** | **+51.7** (196.0, 5e-6) | **+18.8** |
| HM DIFF from-NFW (PRIMARY, z = 0 held) | +53.7 (198.0, 4e-6) | +18.5 |
| HM DIFF from-MF | +51.4 | +18.2 |
| PM P1 SHELL / HM SHELL | +59.8 / +61.8 | +22.0 / +21.7 |
| PM P1 DIFF-F / DIFF-U | +43.4 / +42.8 | +10.6 / +10.0 |
| HM DIFF-U (maximal removal) | +38.2 / +35.9 (from-MF) | +3.6 / +3.3 |

- In every placement the KiDS canonical Δχ²′ stays ≥ +35.9, and the noIA variant stays ≥ +44.0.
- **Indicative alt, on the CFG530 L100 N512 pipeline-check box** (N_kept 20, held construction; not a verdict box):
  - KiDS alt goes from +30.0 to +24.1 (DIFF-S) and +24.1 (HM DIFF);
  - canonical on that box goes from +23.9 to +18.6.
  - The relative shift is the same on both footings.

**Plain statement.** The framework's own expulsion is real and has the right sign, but it is a few-percent effect at
k 0.3–1: 2–8% depending on k and z, against a 19–25% excess. In the primary placement it removes about a quarter of the
KiDS Δχ² (+68.7 → about +52). It cannot plausibly remove the exclusion: even the maximal-removal extreme leaves +36. The
excess is the settled cold energy (candidate B's supply rule), not the baryons the PM failed to expel.

## (iii) Native run

`FROZEN_CRITERIA_NATIVE.md` (741a8adcc) specifies the run and was committed alone before any engine code.
- **Engine:** cfg646_pm.py, a copy of cfg596_pm.py with switch EXPEL. With EXPEL off no new line executes.
- **With EXPEL on:**
  - e = f_b(1 − f_ret)(1 + δ) on catchment cells is removed from the Newtonian source only;
  - it is re-placed by DIFF-S (brackets DIFF-U and SHELL as separate runs);
  - MOND input, settling, edge, draw and cap are unchanged.
- **Gates:**
  - G-R: bit for bit against CFG596's VEa and VLr with EXPEL off;
  - G-0: tab = 1 null;
  - G-M: mass conservation;
  - G-E: consistency with this lane's post-process (reported);
  - V-M: memory.
- **Scoring:** cfg596_native.py unchanged, against CFG596 P0, with CFG592/596 klass and T-OWN from CFG596.
- **Pre-registered expectation:** KiDS canonical about +52 (+36 to +62).
- No PM was run in this lane (no 256³ smoke either).

## Disclosures (dated 2026-10-12)

- **Grid primary label.** An early docstring of `cfg646_expulsion_pm.py`, written before any number, called DIFF-F the grid
  primary. The committed declarations fix the primary as CFG632 DIFF with the host bias, which DIFF-S realises and DIFF-F
  does not. DIFF-F is the more favourable to the framework (+43.4 vs +51.7). Both are reported, and the docstring was
  corrected with a note.
- **Memory.** Two exploratory runs of `cfg646_expulsion_pm.py` (all three sources in one process, before the streaming and
  slab-wise fixes) peaked at 5.2 and 5.0 GB, above this lane's 3 GB budget. Free + inactive memory was about 31 GB, and the
  1024³ job was not affected. The committed outputs come from the fixed script, one process per source, at 2.4 / 3.0 / 2.9 GB.
  The ratios agree with the exploratory runs to ≤ 1.3e-4.
- **No 1024³ alt run exists** (CFG596 P2 was stopped for CFG636). The alt numbers come from the halo model and CFG530 N512.
- **The halo-model ratios are z = 0 and held in z.** The PM post-process shows the effect deepening with z (k = 1: 0.950 /
  0.940 / 0.924 at z 0 / 0.5 / 1), and the per-node propagation includes that.
- **The post-process ignores back-reaction.** Particles would respond to the shallower halo potentials. The native run in (iii)
  is what measures that.
- **Inherited ingredients, as in CFG592/596:** EH initial spectrum, flat w = −1 background, Δ_ta table, survey nuisance priors,
  massless neutrinos. Tinker08/10 and NFW-Duffy08 enter only the halo-model ratio (CONTEXT ONLY).
