# X20_hosted_dwarf_requirement: what does the required extra in hosted dwarfs track, system by system?

Criteria: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (8a6247efea, committed alone first). `AMENDMENT_A1.md`
(post-result, check code only: K2's oracle; verdict logic untouched). κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10
m s⁻², never pooled. No dark-matter particle. Not "theory closed". Nothing here says the data favour the framework.
Every number is in `x20_hosted_dwarf_requirement.out`, `_results.json` or `x20_per_system.csv`.

## Verdict: UNDECIDED (frozen rule: the footings name different top variables)

- Both footings give **PHYSICAL SELECTOR** in the verdict cell (76 hosted systems, isolated-law baseline B_iso).
- The top variable differs: **log r_half** on canonical (z 6.78) and **log M★** on alt (z 6.65).
- The two are tied within the noise on each footing (canonical M★ ρ −0.601, z 6.8; alt r_half ρ −0.600, z 6.5).
- The frozen rule (§4.6) requires the same V on both footings, so the class is UNDECIDED. In words: the extra orders
  by **low stellar mass / small size**, at 6–7σ, on both footings.
- **Qualifiers:**
  - [EFE-DIFFERS]: on the v3s EFE baseline the top variable becomes log V_rel/V_esc,b (canonical) or log x/e (alt), at
    z 12.
  - [ALL-DIFFERS] (canonical only): with the 13 isolated LG dwarfs added, log M★ leads (z 8.29).
  - Not [CONFOUNDED].
- **Not MEASUREMENT-DRIVEN.** The best measurement variable is the binary-correction flag: z 4.47 / 4.58. It is
  collinear with M★ by construction (mutual ρ −0.83 / −0.87), and the partials split cleanly:
  - best P given the binary flag: −0.439 ± 0.115 (z 3.8) / −0.452 ± 0.110 (z 4.1);
  - binary flag given best P: −0.085 ± 0.128 (z 0.7) / −0.145 ± 0.143 (z 1.0).
- **Not BASELINE-DRIVEN.** On B_iso, 32 / 30 hosted systems are EXTRA.
- **NO per-system separation.** No variable separates EXTRA from NONE on any cell. The best scans leave 18–19 offenders
  of 61 / 62 on B_iso.

## Step 0: X1 reproduced exactly

- **K0.** All 89 systems' B_iso and B_EFE medians and sd equal `x1_per_system.csv`: max |diff| 0.00e+00, 178
  system-footings × 2 baselines.
- **K1.** X1's bootstrap class medians and sd reproduce, max |diff| 0.00e+00 over 40 cells. Examples (canonical,
  B_iso / B_EFE):
  - ultra-faints +0.625 / +1.350;
  - bright M31 +0.249 / +0.578;
  - Crater II −0.443 / +0.494;
  - Antlia II +0.060 / +1.007.

## Top correlations (HOSTED, N = 76; Spearman ρ ± bootstrap sd with E redrawn by s_i; z = |ρ|/sd; canonical / alt)

**B_iso (verdict baseline).**

| variable | ρ_S | z | Kendall τ_b | kind |
|---|---|---|---|---|
| log M★ | −0.601 ± 0.089 / −0.600 ± 0.090 | 6.8 / 6.7 | −0.429 / −0.428 | P |
| log r_half | −0.601 ± 0.089 / −0.600 ± 0.092 | 6.8 / 6.5 | −0.427 / −0.425 | P |
| log V_rel/V_esc,b (CFG939) | +0.527 ± 0.099 / +0.530 ± 0.096 | 5.3 / 5.5 | +0.373 / +0.374 | P |
| log Σ, log x | −0.309 / −0.313 | 2.8 / 2.8 | −0.209 / −0.213 | P |
| log x/e | −0.312 / −0.318 | 2.7 / 2.8 | | P |
| log d_host | −0.245 / −0.251 | 2.2 / 2.2 | | P |
| log e | +0.212 / +0.218 | 1.9 / 1.9 | | P |
| log q (pericentre, N 32) | −0.258 / −0.271 | 1.5 / 1.6 | | P |
| ellipticity (N 74) | +0.082 / +0.084 | 0.7 / 0.7 | | P |
| binary flag | +0.463 ± 0.104 / +0.462 ± 0.101 | 4.5 / 4.6 | +0.381 / +0.380 | M |
| log b (binary factor) | −0.446 / −0.445 | 4.3 / 4.3 | | M |
| source family (Kruskal–Wallis) | H 13.78 / 13.59, p_perm 0.048 / 0.042 | 1.98 / 2.03 | | M |
| log δσ/σ | +0.191 / +0.188 | 1.6 / 1.6 | | M |
| log N★ (N 24) | −0.145 / −0.126 | 0.7 / 0.6 | | M |

**Partials against the complete star-count proxy δσ/σ (HOSTED × B_iso).**
- log M★ given δσ/σ: −0.622 ± 0.092 (z 6.7) / −0.623 (z 6.8). δσ/σ given M★: z 2.1 / 2.1.
- log r_half given δσ/σ: z 6.6 / 6.6.
- log V_rel/V_esc,b given δσ/σ: z 5.0 / 5.1.

**B_EFE (v3s static EFE baseline, qualifier).**
- log V_rel/V_esc,b: ρ +0.804, z 12.4 / 11.9.
- log x/e: ρ −0.800 / −0.802, z 11.5 / 12.1.
- log M★: ρ −0.746 / −0.747, z 10.1 / 10.3.
- log x: z 9.5 / 9.4. log d_host: z 7.0 / 7.1. log e: +0.576, z 6.5.
- Binary flag: z 6.7 / 6.4. Source family: z 3.48 / 3.29.

## Separation (X19's test at the level of single systems: EXTRA vs NONE, AMBIGUOUS dropped)

- **No variable separates on any cell** (both footings, both samples, both baselines).
- **HOSTED × B_iso** (32 EXTRA / 29 NONE canonical; 30 / 32 alt):
  - log r_half: fewest offenders, 18 / 18; AUC 0.28 ± 0.07.
  - log M★: 19 / 19.
  - log V_rel/V_esc,b: 21 / 21; AUC 0.65 / 0.68.
- **HOSTED × B_EFE** (49 / 14 canonical):
  - log M★ and log x/e: 8 offenders; AUC 0.19 and 0.13 ± 0.05.
  - Pericentre q: 1 offender, but only 1 NONE system has an orbit.
- The ordering is strong, but it is a graded trend with large scatter, not a threshold.

## Baseline dependence (HOSTED)

- **Medians.** E is +0.395 on B_iso and +0.851 on B_EFE (canonical); alt +0.352 / +0.810.
- **The difference is the EFE.** ρ(E_EFE − E_iso, log e) = +0.702 on both footings.
- **Labels.** 25 / 24 hosted systems change label between baselines, all toward more extra under the EFE.
  - Crater II: NONE → EXTRA (−0.44 → +0.50).
  - Antlia II: NONE → EXTRA (+0.06 → +1.01).
  - Sagittarius: NONE → EXTRA.
  - Also Boötes II, Grus I, Leo IV, And XXIII, and others. The full list is in the `.out`.
- **What moves and what doesn't.** Under the EFE, host-field variables (e, x/e, d_host) jump from about 2σ to 6–12σ.
  The M★ / r_half ordering is present on both baselines.

## Checks: 7/7 PASS (exit 0, 30 s, 0.357 GB, one thread)

| check | result |
|---|---|
| K0 | per-system draws = `x1_per_system.csv`, max diff 0.00e+00 |
| K1 | X1 class bootstrap medians, max diff 0.00e+00 (40 cells) |
| K2 | oracle: ρ +1.000, z 18.0 / 17.8; Z-oracle separates with 0 offenders (A1) |
| K3 | null random V: false-alarm rate 0.005 (1/200) |
| K4 | Spearman (with ties) = scipy to 1.1e-16 |
| K5 | Plummer V_esc,b closed form vs integral, 2.2e-16 |
| K6 | RSS 0.357 GB |

**MUTATE** (`X20_MUTATE=1`) shuffles the per-system rows of the B_iso and B_EFE draws:
- K0 FAILS (352 mismatches);
- K1 FAILS (40/40);
- K2 FAILS (ρ −0.147 / −0.017, 25 / 26 offenders).
- Result: 4/7, exit 1, verdict UNDECIDED (stop rule).

## Physical reading

- **The ordering is mass and size, not compactness.** Against the isolated law, a hosted dwarf's required extra rises
  steadily toward low stellar mass and small half-light radius. Examples (canonical, E_iso):
  - Segue 1 +1.25, Willman 1 +1.22;
  - Draco +0.63, Ursa Minor +0.57;
  - Fornax −0.09, Leo I −0.03.
- **Surface density and internal acceleration order it only at 2.7–2.8σ.** So X19's "compact vs diffuse" reading is not
  the per-system ordering.
  - Crater II and Antlia II need nothing on B_iso because they are among the most massive and largest hosted systems
    (log M★ 5.51 and 6.13), not because they are diffuse.
- **CFG939's V_rel/V_esc,b** orders at 5.3σ only because V_esc,b ∝ √(M★/r_half) carries the M★ dependence. V_rel is
  nearly constant (ledger A3).
- **What this does not exclude.** A trend with M★ at fixed applied binary correction and fixed δσ/σ is what a residual,
  uncorrected binary or non-equilibrium floor in σ would also produce. Such a floor matters most where σ is 2–4 km/s.
  - Neither the applied binary flag nor δσ/σ accounts for it (partials above).
  - A single-epoch flag is NOT ON DISK (M5), and N★ exists for only 24 systems.
  - So "physical" here means "not explained by the measurement variables the record holds". It does not mean a
    demonstrated physical selector.

## What this does not show

- **Only X1's 89 LG systems are tested.** The Coma UDGs, UMa members, TDGs and DF2/DF4 have no per-system B_EFE solve on
  disk.
- **The orbit-based q comes from Z2** (MW E3 systems with PMs, N 32) and is the only tidal variable.
- **Partial measurement variables.** N★ (24 systems) and a single-epoch flag (none) are missing for most systems.
- **The verdict rule is strict.** A tie between collinear M★ and r_half gives UNDECIDED, as frozen.
- **Not blind** (ledger A7).

## Files and run

- `FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md` (8a6247efea); `AMENDMENT_A1.md`.
- `x20_hosted_dwarf_requirement.py` → `.out`, `_results.json`, `x20_per_system.csv`; `*_MUTATE.*`.

```
OMP_NUM_THREADS=1 PYTHONHASHSEED=0 nice -n 15 python3 rebuild_2026_10_22/X20_hosted_dwarf_requirement/x20_hosted_dwarf_requirement.py               # exit 0
X20_MUTATE=1 OMP_NUM_THREADS=1 PYTHONHASHSEED=0 nice -n 15 python3 rebuild_2026_10_22/X20_hosted_dwarf_requirement/x20_hosted_dwarf_requirement.py  # exit 1
```

Inputs are read only: X1's stage tables and CSV, the LVD, CFG257's tables, Collins 2013 and Z2's per-system CSV. Nothing
was downloaded.
