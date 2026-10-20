# CFG886 — rebuild Ω_c/Ω_b = 5.364 and the census f_ret without the Planck ΛCDM fit

Criteria: `FROZEN_CRITERIA.md` (07170a203, committed alone before any script; owner block 880–889). Run:
`OMP_NUM_THREADS=1 nice -n 10 python3 cfg886.py` (about 25 s, one core, < 1 GB), then `CFG886_MUTATE=dh10` for the control
(it reads the main run's JSON). κ = ½ fitted. a0 enters none of T1–T4, so both footings give identical numbers there; the
footings differ only in T5. Repo data only; nothing was downloaded.

## Result

**5.364 RECOVERED under BAO + BBN with flat a0 (R = 5.27 ± 0.22, z −0.42). NOT PINNED across H0 options: SH0ES gives
6.12 ± 0.32 (+14%, TENSION z +2.36). Without the flat-a0 assumption, BAO + BBN do not pin R at all (2.9–8.1). f_ret
provenance: MIXED.**

| option | h | Ω_m | ω_m | R = ω_c/ω_b | class | f_b = ω_b/ω_m |
|---|---|---|---|---|---|---|
| **(a) DESI DR2 BAO + BBN, flat a0 (X ≡ 1), primary** | 0.6856 ± 0.0052 | 0.2976 ± 0.0085 | 0.1399 | **5.272 ± 0.218** (68% 5.06–5.49) | **5.364 RECOVERED** | 0.1589 ± 0.0055 |
| (b) SH0ES 73.04 ± 1.04 + BAO-shape Ω_m + BBN ω_b | 0.7304 ± 0.0104 | 0.2975 ± 0.0085 | 0.1587 | **6.122 ± 0.321** (68% 5.80–6.44) | TENSION | 0.1401 ± 0.0063 |

- **T1 ω_b from D/H** (PDG 2024, (2.547 ± 0.029) × 10⁻⁵, as cited in XR26; N_eff 3.044). PRIMAT 2024 gives 0.021826 and
  PArthENoPE 2017 gives 0.022584 (Marcucci rates 0.021872). **Primary (midpoint) 0.02221 ± 0.00044.** The 3.4% gap between
  the two codes is the largest error term (half of it, 0.00038, is carried as a systematic). Cooke+18 D/H gives 0.02232 ± 0.00044.
- **T2(a)** h r_d = 101.53 ± 0.72 Mpc, r_d = 148.1 ± 1.5 Mpc, ω_c = 0.1171 ± 0.0048. χ²_min 10.55 for 13 numbers.
  Variants, all RECOVERED:
  - CFG682's conditional Ω_m prior: 5.415 ± 0.162.
  - Cooke+18 D/H: 5.258 ± 0.218.
  - PRIMAT alone 5.323; PArthENoPE alone 5.222. The nuclear-rate choice moves R by ±0.05.
  - Σm_ν = 0: 5.329 ± 0.219.
- **T2(b)** The ruler that (b) implies is r_d = 139.1 ± 2.2 Mpc. BBN + BAO give 148.1 ± 1.5, which is 3.4σ away (the Hubble
  tension; not resolved here). If the local ladder is right, one of the early-universe assumptions E1–E4 fails. With CFG682's
  conditional Ω_m, (b) gives 6.39 ± 0.31 (NOT RECOVERED). Reported only, both too wide to be informative: TDCOSMO 2025
  (71.6 ± 3.6) gives 5.86 ± 0.73 and the standard sirens (68.0 ± 4.1) give 5.19 ± 0.78.
- **T3 classes.** Recovery uses (a) primary: **5.364 RECOVERED** (precision 4.1%; Planck's own ±0.065 on 5.364 is stated, not
  added). Pinning: the (b) central value 6.122 lies outside 5.364 × [0.90, 1.10] = [4.83, 5.90], so **NOT PINNED**. The spread
  (b) − (a) is +15.8% of 5.364.
- **V5: free dark energy, no flat-a0 assumption.** This reuses CFG682's committed fixed-Ω_m best fits; their χ² values are
  reproduced exactly. At each fit the ruler q is profiled, and h is solved with the BBN r_d. χ² is flat across Ω_m 0.24–0.36
  (BAO 3.24–3.43). Over that range R runs from **2.95 to 8.06** (BAO) and from 2.88 to 7.73 (BAO + SN). So the rebuild rests
  entirely on constant ρ_DE. Under the tracking rule, that is the framework's flat a0, but it is also ΛCDM's background.
  **Nothing here can favour the framework over ΛCDM.**

**Early-universe assumptions in (a).** These are assumptions, not results:
- E1 standard BBN;
- E2 N_eff = 3.044;
- E3 GR before recombination, with **cold energy behaving as pressureless matter before recombination**;
- E4 standard recombination;
- E5 cold mass conserved after recombination (CFG253 bounds late creation at about 3%);
- E6 flat space.

The CMB anisotropy fit is not used. T_CMB is the FIRAS value. Σm_ν = 0.06 eV is the oscillation minimum, not a CMB fit.

## f_ret (T4): MIXED

| segment | class | why |
|---|---|---|
| G: galaxy floor 0.10 (log M_ta < 12.5 Msun/h) | **CLEAN** (on the repo's evidence), **not traceable in repo** | See below. |
| C: group/cluster ramp (0.55 at 10^13.5, 0.85 at 10^14.5, cap 0.90) | **UNDETERMINED** | Hand-set in CFG416 ("from the census and group/cluster baryon fractions, stated in advance"). There is no table, script or derivation anywhere in the record. The record's group/cluster fractions use Newtonian hydrostatic M500 over Planck f_b (CFG379). In the framework those masses include the law's phantom. The mapping from R500 to the turnaround catchment (r_ta ≈ 5–13 R200, CFG656) is not documented. |

Segment G in more detail:
- It is the cosmic-mean census of Shull, Smith & Danforth 2012, recalled and PROVISIONAL (CFG525). There is no census table in
  the repo; 13 lane files cite Shull.
- No halo mass enters. M_ta comes from the framework's own fixed point, M_ta = M_b h/(f_ret f_b). No abundance matching, no
  NFW fit and no ΛCDM mass function is involved, as far as the repo shows. How Shull's ICM share was computed cannot be checked
  here.
- Applying a cosmic mean to every catchment assumes that every baryon belongs to some catchment.
- The quoted 10% includes hot gas in groups and clusters. The galaxies-only value is 0.07, yet CFG634 HC-1 labels the 0.10
  floor "stars + cold gas".

**What can be rebuilt.**
- **The census denominator.** A census fraction scales as h/ω_b. Rebuilt, f_ret moves 0.10 → 0.1025 (a) / 0.1092 (b). This
  assumes the census used the record's h 0.674 and ω_b 0.02237; its own adopted values are not in the repo.
- **The stock S/M_b = R/f_ret** (record 53.64).
  - Ratio-only: 52.72 (a), 61.22 (b).
  - Census-consistent, where ω_b cancels (S/M_b = 10 (ω_c/0.02237)(0.674/h)): 51.45 (a), 56.08 (b).
- **The f_ret values themselves.** No ΛCDM-free source exists for them in the repo. The framework derivation failed (CFG806).

## Sensitivity of record results (T5, report only)

- **CFG876, supply-capped variant** (a reported row there):
  - The stock changes from 53.64 to between 50.5 and 61.2.
  - E moves by ≤ 0.004: canonical −0.183 to −0.189, against the record's −0.185. N_fail stays 2 canonical and 2–3 alt.
  - The class is BROKEN in every case. Insensitive.
- **CFG878 stock note.** The M_b below which a universal clump exceeds the stock moves from 9.8e4 to 8.6e4–1.04e5 Msun
  canonical (alt 6.9e4–8.4e4). "Ultra-faints (M_b ≲ 1e5) cannot draw the clump from today's baryons" is unchanged.
- **CFG804 (KiDS catchment supply).** The stock per bin scales with R·N: −1.7% (a), +14% (b). Every bin, in every case, stays
  above CFG803's demand (16.1–21.5 M_b); the smallest is 29.8. So the primary "SUFFICES" would not flip on R alone. The edges
  (∝ R N) move by the same fractions. **Finding (unit convention):**
  - CFG804 solves M_ta = M_b/(f_ret f_b) in Msun. CFG416 and CFG515 declared the ramp in Msun/h, a 0.171 dex shift.
  - In the declared convention the canonical bins get N = 10.0 / 10.0 / 9.4 / 7.0, instead of CFG804's 10.0 / 8.8 / 7.4 / 5.6.
    That is 13–28% more supply in bins 2–4.
  - This is the conservative direction for CFG804's primary pass. A rerun is needed to see whether its all-radii shortfall
    changes.
- **CFG650/654 shear engines.** These read the ratio through FB = ω_b/(ω_b + ω_c) in the census edge
  r_M(f_ret f_b M_ta)/ln(1 + f_ret f_b/(1 − f_b)). At fixed M_ta the edge changes by ×0.990 (a) or ×1.078 (b). The engines
  also carry other Planck inputs: h 0.6736, ω_c 0.1200/0.1202, n_s, σ8 or A_s, and θ*. A CMB-free rerun would need this lane's
  ω_c **and** a non-CMB power-spectrum amplitude, which the record does not have. So those engines cannot be made CMB-free with
  this lane alone.

## Controls

| control | result |
|---|---|
| K1i R(0.02237, 0.1200) | 5.364327 (PASS) |
| K1ii CAMB r_d at the Planck pair (N_eff 3.044) | 147.102 Mpc, +0.035% vs 147.05 (PASS) |
| K1ii′ XR26's exact settings | 147.0491 vs 147.049 (PASS, reported) |
| K2a BAO identity | CFG681 X ≡ 1 minimum reproduced (χ² 10.55149, Ω_m 0.29703); CFG682's 49 fixed-Ω_m χ² values reproduced exactly (PASS) |
| K2b analytic background vs CAMB | 1.2e-6 (PASS) |
| K2c r_d spline vs CAMB | 2.4e-6; h-dependence 1e-7 (PASS) |
| K3 BBN | round trip 3e-15; reproduces CFG654's ω_b 0.021932 (σ 0.000217); PArthENoPE gives D/H 2.5875e-5 at Planck's ω_b (PASS) |
| K4 grid adequacy | edge mass ≤ 4e-31; ≥ 5.7 grid steps per sd (PASS) |
| K5 CFG876 read-only exec | committed E reproduced exactly (PASS) |
| K6 CFG804 fixed point | N 10.00 / 8.83 / 7.35 / 5.62 (PASS) |

**MUTATE (D/H × 1.10):** ω_b falls 5.74% (frozen window 4–8%). R(a) rises 3.44% to 5.454 (window +1% to +6%). R(b) + 1 rises
by 1.06088 against the expected 1.06090. **PASS: the control bites in the expected direction and size.**

## Disclosures

- **Post-run fix 1.** The first run (`cfg886_RUN1_v5bracket.*`, kept) bracketed V5's h solve on [0.50, 0.95]. That bracket
  leaves the r_d spline's ω_c range at the Ω_m ends, so 17 of 49 rows came out NaN. The bracket now follows the spline range.
  Every number outside V5 is identical between the runs.
- **Post-run fix 2** (cosmetic). The T4 evidence counts now exclude this lane's own files. RUN1 counted them: 15 vs 13 Shull
  citations.
- **CFG682's Ω_m = 0.3085 ± 0.0075 is a forecast row.** It is conditional on an assumed 0.02 dex flat-a0 measurement at
  z = 2.33, which does not exist. It is used here only as a labelled variant. The clean "flat a0 at all z" value is BAO-only
  X ≡ 1: 0.2976 ± 0.0085. CFG885 (a parallel lane) uses 0.3085 as its native no-CMB Ω_m, which inherits this condition.
- **Hand expectations** written in the criteria were R(a) ≈ 5.2–5.3 and R(b) ≈ 6.1–6.4. Both came true. The classes were
  expected.
- PArthENoPE has no theory-error column, so PRIMAT's relative error was applied to it. PArthENoPE's ΔN = 0 may mean 3.046
  (≤ 1e-5 in ω_b).
- In V5 the background radiation follows CFG681's convention (h 0.68, 3.046 massless), at a level of about 1e-4. V5 has no
  error bars; it reports the central values on a flat χ² curve.
- The f_ret classes are a documentary judgement from files read before the freeze (listed in the criteria), not a blind test.
- κ fitted; cold energy mass required; not theory closed.
