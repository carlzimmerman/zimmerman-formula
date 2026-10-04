# CFG326: CFG323 extended with Alabi+16 GC density slopes

**Frozen criteria:** `FROZEN_CRITERIA.md`, commit c4aff2ac5, sha256 `b613ce0719fe5a5afacc2e253a178dc6a4c86f2eae3a653aa41c41e2a411409b`. It was written after the owner-approved download ("yeah download Alabi+16 too boss", orchestrator chat, 2026-10-03) and before any Alabi+16 table value was read. The method text was read with its digits masked.

**Fixed inputs:** CFG323's method, statistic, decision rule (e), kernel ν_mono, κ = ½, both footings (9.36e-11 | 1.13e-10). No knob scans. CFG323 is exec'd read-only and never retro-fixed.

## Bottom line

**Alabi+16 adds no measured GC density profiles. Its per-galaxy γ values are outputs of its γ–log M* relation, so coverage stays 4/16 and the frozen verdict is CFG323's: NOT SIGNIFICANT.**

- **Test T0.** 22 of Alabi's 23 γ values equal γ = −0.63 log M* + 9.81 within print rounding (max |r| 0.009, budget about 0.068). That includes all 15 of the CFG55 16 that Alabi lists.
  - The one exception is NGC 1407 (+0.098). It is not in the 16, and the γ text does not name it, so it is UNATTRIBUTED and unused.
  - NGC 4459 is not in Alabi+16 at all.
- A relation value carries nothing about the galaxy beyond its stellar mass. That is the route CFG111 already scored. By the frozen rule it is not a measurement, and it enters only the reported row R-A16.

### Primary (identical to CFG323 by construction; coverage N = 4/16)

| split | footing | N | mean (dex) | Z_stat | Z_sys | class |
|---|---|---|---|---|---|---|
| ALL | canonical | 16 | +0.0920 | 4.41 | **2.07** | WEAKENED |
| ALL | alt | 16 | +0.0826 | 4.01 | **1.85** | NOT SIGNIFICANT |
| NO-CENTRALS | canonical | 12 | +0.0620 | 2.96 | 1.21 | NOT SIGNIFICANT |
| NO-CENTRALS | alt | 12 | +0.0532 | 2.56 | 1.03 | NOT SIGNIFICANT |
| CENTRALS | canonical | 4 | +0.1817 | 10.78 | 4.82 | FAIL CONFIRMED |
| CENTRALS | alt | 4 | +0.1707 | 9.74 | 4.40 | FAIL CONFIRMED |

**Verdict (rule (e), the weaker footing): NOT SIGNIFICANT [measured-tracer coverage 4/16]: NO NEW MEASURED COVERAGE.**

### Reported row R-A16 (Alabi relation γ on the 11 galaxies without a CFG323 profile; not a decision row)

| split | footing | mean (dex) | Z_stat | Z_sys (±0.5 around γ_i) | Z_sys (±rms 0.29) |
|---|---|---|---|---|---|
| ALL | canonical | +0.0831 | 4.31 | 1.83 | 2.15 |
| ALL | alt | +0.0736 | 3.87 | 1.61 | 1.90 |
| NO-CENTRALS | canonical | +0.0589 | 2.76 | 1.15 | 1.25 |
| NO-CENTRALS | alt | +0.0500 | 2.36 | 0.97 | 1.06 |
| CENTRALS | canonical | +0.1558 | 18.4 | 2.99 | 3.86 |
| CENTRALS | alt | +0.1443 | 16.0 | 2.69 | 3.48 |

- The relation gives the massive centrals shallower tracers (γ ≈ 2.57–2.62 instead of 3). That lowers NGC 4365, 4374 and 5846 by about 0.03–0.04 dex each, and the ALL mean by about 0.009 dex.
- The centrals' excess stays at +0.14 to +0.16 dex. It reaches FAIL-class only with the rms band; with the ±0.5 band it is WEAKENED.
- **R-A16all** also replaces CFG323's four profiles with Alabi's relation γ: ALL Z_sys 1.54 / 1.32.

## Controls (main run 4/4; MUTATE run 4/5, the MUTATE FAIL kept)

| ID | Result |
|---|---|
| K1 | With Alabi switched off, both the re-run CFG323 namespace and this lane's scorer reproduce every committed CFG323 stat (mean, Z_stat, Z_sys; all subsets, both footings) to 0.0. Same class. |
| K2 | **PASS, but weak.** Alabi vs CFG323 outer slopes agree within 2√(σ_A² + σ_323²): NGC 2768 −0.30 vs ±0.62, NGC 3607 +0.16 vs ±1.15, M87 +0.54 vs ±1.09.<br>NGC 1023 is vacuous (±170), because its n − 1σ = 0.30 profile has an absurd slope.<br>σ_A is the relation rms 0.29, since T0 says RELATION. The control tests the relation, not a measurement. |
| K3 | 23 table rows, the same set as the Fig. 1 caption's 23. The equation and rms were parsed. |
| K4 | CFG323's C1–C6 and P1 pass again in the re-run namespace (7/7). |
| T0 | 22 RELATION, 1 UNATTRIBUTED (NGC 1407, not in the 16), 0 MEASURED. |
| M1 | **FAIL (kept): "MUTATE INSENSITIVE".** A cyclic shift of the Alabi γ moves R-A16's ALABI-COVERED mean by only −0.0042 dex (alt −0.0043), with no class change.<br>Per-galaxy offsets do move (ALL Z_sys 1.83 → 1.74). The subset mean barely moves because a permutation keeps the same set of slopes. |

## Disclosures

- **VizieR.** There is no Alabi+16 catalogue: J/MNRAS/460/3838 returns 404. A J/MNRAS/460 listing query (142,212 bytes, logged) returned only other papers' catalogues. That file is outside the approval and was deleted unread, apart from its catalogue-name lines.
- Alabi+16 tabulates no per-galaxy γ errors. Under the frozen rule a measured slope with no error would contribute 0 to σ_meas. That case did not arise.
- K2's NGC 1023 limit is vacuous. It is reported as it fell.

## Files and run commands

| File | Content |
|---|---|
| `cfg326_alabi16.py` | The lane script (~80 s, one process). It execs CFG323's script read-only up to its MUTATE block. |
| `cfg326_alabi16.out`, `_results.json` | Main run, 4/4. |
| `cfg326_alabi16_MUTATE.out`, `_MUTATE_results.json` | MUTATE run, 4/5 (M1 FAIL kept). |
| `cfg326_alabi16_transcribed.tsv` (`_MUTATE` copy) | Alabi table columns (1), (9), (12) and the relation, parsed by script. |
| `cfg326_cfg323_rerun_transcribed.tsv` (`_MUTATE` copy) | CFG323's side file from the read-only re-run, redirected here. |
| `cfg326_fetch.py` | The capped, logged fetch helper (CFG323 pattern; 20 MB cap, 10 MB per file). |
| `FETCH_LOG_CFG326.md`, `FETCH_MANIFEST_CFG326.jsonl` | The fetch log. |

```
python3 campaign_fresh_gravity/CFG326_sluggs_alabi16/cfg326_alabi16.py
CFG326_MUTATE=1 python3 campaign_fresh_gravity/CFG326_sluggs_alabi16/cfg326_alabi16.py
```

## Fetch manifest

- Files are stored under `../_external_data/sluggs_tracers/`, outside the repo; paths are relative to the repo root.
- Total: **1,744,350 bytes** (cap 20 MB). The arXiv source size was checked with `curl -I` (headers only, 1,554,597 bytes) and is not logged.
- **Identity check:** arXiv 1605.06101, "The SLUGGS Survey: The mass distribution in early-type galaxies within five effective radii and beyond", by Alabi, Forbes, Romanowsky and Brodie (2016). Read from the abstract page's citation metadata, it matches Alabi + SLUGGS + GC mass.

| label | url | file | bytes | sha256 | status |
|---|---|---|---|---|---|
| Alabi+16 arXiv abs (identity check) | https://arxiv.org/abs/1605.06101 | ../_external_data/sluggs_tracers/alabi16/1605.06101_abs.html | 47,258 | e9e7c1db4303be054a86eba1d69b39f53d454bff7001680c0764b1bdcfb2c676 | http 200 |
| Alabi+16 arXiv source | https://arxiv.org/e-print/1605.06101 | ../_external_data/sluggs_tracers/arxiv_src/1605.06101.tar.gz | 1,554,597 | ec87fd0d86cd36e2bdb61c349b5cb8b7ab2e9a2639431dd530b91fa3ed9d9151 | http 200 |
| ReadMe J/MNRAS/460/3838 | https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/460/3838/ReadMe | ../_external_data/sluggs_tracers/readme/J_MNRAS_460_3838_ReadMe | 283 | f5a8d05b5522789f86414a523fb831d1a9c6969437c4053644d4d092a6ea84ae | http 404 |
| VizieR J/MNRAS/460 listing | https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/MNRAS/460*&-meta.all | (deleted: no Alabi catalogue, other papers only) | 142,212 | 47dee94c1a094d5c8aa3e5b204c2b16e20584e7375925bf3b1bcaee8f7dcf176 | http 200 |
