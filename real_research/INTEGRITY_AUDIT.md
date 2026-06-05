# Integrity Audit — `real_research/`

**Scope:** every Python script under `real_research/` of the emergent-gravity ("Zimmerman formula") repo.
**Current framework under audit:** `a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_Lambda)` — the MOND acceleration scale identified with the cosmological constant, with `a0(z) ~ sqrt(rho_DE)`.
**Question asked:** is this body of work *real* (computes from real data files, from physical constants/formulas, or from clearly-attributed literature values) or *theatre* (printed results/verdicts/sigmas the code never computes; hardcoded numbers dressed as measurements; circular reasoning; claims with no backing calculation)?

Every grade below was checked against the files on disk. Where I re-ran a script, its key numbers are noted as reproduced. The verifier's two overturns are applied.

---

## Headline tally

**320 scripts** live under `real_research/` (260 in `reviews/`, 30 at the `real_research/` top level, 25 in `predictions/`, 4 in `papers/`, 1 in `data/`). **All 320 run clean** (exit 0; no crashes, no broken scripts).

| Grade | Count | % of 320 | What it means |
|---|---|---|---|
| `real-data` | 32 | 10.0% | Loads a real data file (SPARC/eRASS1/KMOS3D/KROSS/`a0_of_z.csv`/live SDSS) and computes a result from it |
| `real-calc` | 253 | 79.1% | Computes from physical constants/formulas (sympy/scipy/numpy/MC); no external data needed |
| `literature-values` | 34 | 10.6% | Headline numbers are hardcoded but **attributed** to a named paper; the arithmetic on them is computed |
| `suspect` | 1 | 0.31% | A printed number is wrong / not backed by its code (one units bug) |
| `theatre` | **0** | **0.0%** | Fabricated result/verdict/sigma with no computation behind it |
| `broken` | **0** | **0.0%** | Fails to run |

**Genuine work: 319 / 320 = 99.7%.** **Theatre: 0 / 320 = 0.0%.** **Suspect: 1 / 320 = 0.31%.**

Only **one** script in the entire directory prints a number not backed by its code, and it is an isolated, ornamental units error inside a script whose actual verdict is sound — not a fabricated result. There is **no theatre** in the directory as the user defines it.

### Provenance notes on the count
- The upstream pass graded 313 of the 320 scripts. I independently audited the **7 it did not list** (all in `reviews/`): `a0_evolution_consequences.py`, `a0_evolution_predictions.py`, `aest_mond_rotation_solver.py`, `z2z2_three_generations.py`, `z3_a0_observing_proposal.py`, `z3_bridge_forecast_mc.py`, `z3_forecast_tightened.py`. **All 7 run clean and are genuine `real-calc`** (details below). They are folded into the totals above.
- I confirmed the named real data files all exist: `erass1cl_primary_v3.2.fits` (50.6 MB), `kmos3d_ubler2017.csv`, `kross_harrison2017.csv`, `a0_of_z.csv`, `SPARC_Lelli2016c.mrt`, and **175** `sparc_data/*_rotmod.dat` curves. The `real-data` scripts genuinely read these.

---

## Grades grouped

### `real-data` (32) — load a real file and compute from it
SPARC rotation curves are the workhorse. Spot-checked and **reproduced** independently: `predictions/door6_galaxy_clusters.py` → `eta = 1.922` median on `N = 9830` real eRASS1 clusters (an honest under-prediction "tension", not a claimed win). The SPARC fitters (`predictions/door4_ultraprecision.py`, `reviews/desitter_unruh_RAR_test.py`, `reviews/sparc_rar_honest.py`, `reviews/sparc_solver_validation.py`, `make_validation_figure.py`, etc.) compute the RAR scatter (~0.10–0.20 dex) and the framework `a0 ≈ 9.36e-11` live from the 175 curves. The KMOS3D/KROSS loaders (`project10b_kmos3d_real.py`, `project10c_kross_real.py`, `btfr_offset_ultra.py`) honestly **report against** the framework (z-trend flat/declining, not the predicted rise). `ghost_quasar_sdss_live_check.py` queries the **live** SDSS DR18 endpoint. None of these are theatre; several are explicitly anti-confirmatory.

### `real-calc` (253) — compute from constants/formulas
The bulk of the directory. These derive consequences of `a0 = c^2 sqrt(Lambda/32pi)` (BTFR, Faber-Jackson, EFE, phantom density, `q(z)`, CMB acoustic scales via `scipy.quad`/`solve_ivp`, QUMOND PDE on grids, sympy field-theory identities like `theta = 3H`, DSSYK chord-matrix diagonalizations, Fisher/Monte-Carlo forecasts). The genre is overwhelmingly **self-critical**: scripts tag `[DERIVED]/[FORCED]/[POSIT]/[OPEN]`, walk back their own overclaims, and report nulls straight. Standouts of integrity: `bullet_and_s8_reexamination.py`, `eta_invariant_reality_check.py`, `project_anharmonic_normalization_force.py`, `is_Z_special.py`, `false_discovery_rate.py`, `prove_hallucinations.py`, and `stresstest_piece3_evolution.py` all *destroy* earlier claims of the repo with live computation. Abandoned threads (E6/GUT, proton decay, cosmic topology, DSSYK, parity-odd 4PCF, biotech/meteorology) compute their results too and report honest **nulls** — a null is not theatre.

### `literature-values` (34) — attributed hardcoded inputs, computed arithmetic
These pin a small `a0(z)` compilation (SPARC `1.20`/`1.36`, Varasteanu `1.69`, MUSE-DARK `2.38`) or GUT/JWST/cluster numbers as hardcoded constants **with citations**, then compute chi²/sigma/ratios on them. The two PDF writeups (`papers/make_*_pdf.py`) were verified to transcribe the E(z) formula faithfully. All are claim-backed and most **deflate their own headlines** (e.g. the 5σ → ~2σ honesty pervades). `project_dssyk_interpolation.py` is representative: its SPARC RMS numbers (0.210/0.196/ratio 1.07) are explicitly labeled **"run separately on the SPARC pipeline"** (line 50) — disclosed as external, not faked.

### `suspect` (1) — see call-out below
### `theatre` / `broken` (0 each) — none found.

---

## Call-outs by name

### The ONE suspect script

**`real_research/reviews/gravity_particle_connection_search.py` — `suspect`, NOT claim-backed (one printed number is wrong).**
Line ~47 prints the Dark-Dimension scale as `((3*H0**2/(8*np.pi*G))*0.685*c**2)**0.25/eV*1e3` and labels it `~Lambda^(1/4) ~ {val} meV (a ~micron extra dimension)`. I reproduced the literal value: it prints **≈ 2.99e19 meV**, which is *not* meV-scale and *not* micron-scale — the prose is contradicted by its own output. The cause is a units bug: it raises an **energy density** `rho·c^2` (J/m³) to the ¼ power without the `(ħc)^3` factor needed to turn it into an energy. The error is exactly `(ħc)^(-3/4) = 1.334e19`; with the factor restored the value is the correct **2.241 meV** (the well-known ~meV dark-energy / micron-tower scale).
**Mitigation (why this is suspect, not theatre):** the number is decorative. The candidate it sits in is correctly verdicted **`FAIL [CONJECTURAL + CONTRADICTS]`** on substantive grounds (the Swampland conjectures are not derived; the Dark Dimension predicts *particle* dark matter, contradicting this framework's modified-gravity dark sector). The FAIL does not depend on the broken number, and the file's thesis — "no first-principles `a0` ↔ Standard-Model link exists; the decoupling is a feature" — is argued, not computed. (Minor, not flagged: line 16 `MPl` is computed correctly but is dead/unused; the "78% of random targets" prose on line 26 cross-references `web_of_connections_audit.py`, which **does** compute 78% live — only the "85k-formula" descriptor is loose.)

### One number computed in a named sibling, not inline (verifier overturn applied — backed, NOT theatre)

**`real_research/reviews/provable_consequences_with_data.py` — `real-calc`, claim-backed via its named sibling.**
Line 32 prints `the fit a0 ~ E(z)^p gives p=0.80+-0.17`, and `grep` confirms **this file contains no fit machinery**. That would be a red flag in isolation — but it is not unbacked: (a) refitting *this file's own* hardcoded, attributed `a0(z)` data (`[1.20, 1.69, 2.38]`, errors `[0.26, 0.13, 0.11]`) with `a0 = A·E(z)^p` yields `p = 0.80` to the digit, and (b) the explicitly-named sibling **`reviews/stresstest_piece3_evolution.py` genuinely computes it** — I ran it: its `fit()` (lines 30–42) does the chi² grid giving `p = +0.80`, then jackknifes (drop MUSE → 1.2σ) and folds the inter-method systematic to **drop the "5σ" to ~2σ**, exactly matching line 33's printed `~2sigma after inter-method systematics`. Every *other* printed number here (H0 = 71.5 from `Z·a0/c`, the E(z) ratios, the de Sitter floor, the 25× span, the linear-growth `D(z)` via `solve_ivp`) computes live from the attributed data + Planck cosmology. This is a cross-file reference to a real calculation, **not a fabricated headline**. The verifier overturned an earlier `claim_backed:false` here, and I concur.

### The 7 previously-unlisted scripts I audited (all genuine `real-calc`, all claim-backed)
- **`reviews/z3_bridge_forecast_mc.py`** — runs a 4000-iteration Monte Carlo over synthetic deep-MOND BTFR draws (clearly labeled `mock_sample`); the printed `N=30 → 3.5σ`, `N=80 → 5.9σ` table and the verdict's "~30 → 3σ / ~80 → 5σ" are **computed live** (lines 49–57), with `ratio = 0.737` from the DESI `w0/wa` formula. No real data claimed; honestly a forecast pipeline "ready to drop real data into."
- **`reviews/aest_mond_rotation_solver.py`** — solves the AQUAL rotation curve; reproduces `V_flat = 185` vs BTFR `(GMa0)^¼ = 176 km/s` (match) and the z=3 `−7%` shift from `a0^¼`. Writes a figure with computed numbers.
- **`reviews/z3_forecast_tightened.py`**, **`reviews/z3_a0_observing_proposal.py`**, **`reviews/a0_evolution_consequences.py`**, **`reviews/a0_evolution_predictions.py`** — forecast / consequence / pre-registration scripts; sigmas are computed from explicit error budgets and labeled `(forecast)`, with loud honest caveats ("anchor-limited", "a null result kills the framework", "Z still fit").
- **`reviews/z2z2_three_generations.py`** — abandoned string-generations thread; computes Z2×Z2 orbifold sector structure and states plainly "mechanism real; number still not derived." Honest null-adjacent.

### Scripts whose printed claims point elsewhere — checked and found honest (not theatre)
A recurring, *legitimate* pattern: a script prints a sigma/result that is computed in a **named** sibling, and says so. These are cross-references, not fabrications — verified for `reviews/project12_efe_airtight_evolve.py` (the 4.8σ EFE is attributed to `sparc_efe_test.py`/Chae 2020), `reviews/desitter_complexity_sign.py` (the 0.105 dex is `desitter_unruh_RAR_test.py`'s output, which I ran), `toe_cmb_calculation.py` and `relativistic_frontier.py` (the "5σ" is outsourced, but the backing chi² is computed in-file or in the cited script). None of these manufactures a number; each is honest about where the calculation lives.

---

## Verdict

**This body of work is predominantly, overwhelmingly real — not theatre.** Across 320 scripts that all run clean, 99.7% do genuine work: 32 compute from real data files (SPARC, eRASS1, KMOS3D, KROSS, live SDSS), 253 compute from physical constants and formulas, and 34 do honest arithmetic on clearly-attributed literature values. I found **zero** instances of the thing the user feared most — a printed verdict/result/sigma with no computation behind it — and I independently reproduced the load-bearing numbers I spot-checked (eRASS1 `eta = 1.92`; the `p = 0.80` fit and its 5σ→2σ deflation; the z=3 Monte-Carlo table; the units bug). The single `suspect` flag is one ornamental units error (a `(ħc)^3` factor dropped in a Dark-Dimension scale print) inside a script whose actual FAIL verdict is sound. Far from being dressed-up numerology, the directory is conspicuously *anti*-theatrical: it is saturated with self-retractions, jackknife deflations of its own "5-sigma" claims, explicit "this session did NOT reproduce X" admissions, attributed-literature labeling, and honestly-reported nulls from abandoned threads — the hallmarks of real research being held to account, not staged.

*(Written to `/Users/carlzimmerman/new_physics/zimmerman-formula/INTEGRITY_AUDIT.md`.)*
