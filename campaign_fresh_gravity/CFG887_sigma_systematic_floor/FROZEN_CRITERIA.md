# CFG887 — FROZEN CRITERIA: is CFG880's "clump σ not universal" result driven by measurement systematics?

Frozen before any comparison of σ values between catalogues (owner block 880–889). κ = ½ fitted; not theory closed.

## Why
CFG880 found intrinsic scatter s_int = 0.38 in the clump σ between dwarfs (NOT UNIVERSAL, both footings). Its post-hoc floor scan
shows the class holds with a per-dwarf systematic floor of 10–15% in σ and becomes UNDECIDED at ≥ 20%. Whether the real
systematic is that large is measurable: the repo holds independent compilations of the same dwarfs' σ.

## Data (repo only; nothing downloaded)
- LVD (real_research/data/dsph/lvd_dwarf_{mw,m31,local_field}.csv): vlos_sigma, vlos_sigma_em/_ep (upper limits excluded).
- McConnachie 2012 (real_research/data/dsph/mcconnachie2012_dsph.csv): sigma*, e_sigma*.
- Collins et al. 2013 (real_research/data/dsph/collins2013_m31_dsph.tsv): sigV, E_sigV, e_sigV; sigV = 0 rows excluded (upper limits).
- Name matching by a fixed normaliser (lower case; "(I)" → "I"; "Segue I/II" → "Segue 1/2"; "And " → "Andromeda "; parenthesised
  long names dropped, e.g. "LGS 3 (Local Group Suspect 3)" → "LGS 3"; "M32" → "M 32"; "Sagittarius dSph" → the LVD Sagittarius row).
  Unmatched names are listed, not forced.

## Statistic
For each catalogue pair (LVD–M12, LVD–C13) and for both pooled: d_i = ln(σ_LVD/σ_other), e_i² = (ē_LVD/σ_LVD)² + (ē_other/σ_other)²
with ē the mean of the two error sides. Maximum likelihood for d_i ~ N(μ, e_i² + s_x²) gives the extra (unreported) scatter s_x;
68/95% profile intervals; bootstrap check.
- **Primary floor** f = s_x/√2 (the extra scatter shared equally by the two catalogues). **Conservative floor** f_c = s_x (all of it
  attributed to one measurement). Both use the pooled pair set; the LVD–M12 set alone is reported.
- Then CFG880's hierarchical fit (its code exec'd unchanged; same sample of 83, same model, profile likelihood) with f (and f_c) added
  in quadrature to both error sides, as CFG880's V5 / post-hoc floor did, on both footings.

## Classes (canonical primary; the alternative footing must agree, else the weaker class)
- **CFG880 STANDS:** NOT UNIVERSAL at f and at f_c.
- **CFG880 FRAGILE:** NOT UNIVERSAL at f but UNDECIDED (or UNIVERSAL) at f_c.
- **SYSTEMATICS-LIMITED:** not NOT UNIVERSAL at f.
Also reported: f's 95% upper value used as the floor (a pessimistic variant), and the floor at which the class would change (from
CFG880's scan: between 0.15 and 0.20).

## Controls
- K1: with floor 0 the exec'd fit reproduces CFG880's committed canonical s_int (0.380) and its 95% interval to < 1e-9, and floor
  0.10 reproduces CFG880's post-hoc floor-0.10 line.
- MUTATE (`CFG887_MUTATE=1`): all d_i doubled (inter-catalogue disagreement ×2) → s_x must roughly double and the class must not be
  STANDS unless the doubled floor is still < 0.15.

## Disclosed limits (fixed now)
M12 values are older than LVD's: differences mix genuine measurement systematics (membership, binaries, small samples, instrument
offsets) with improvements from more data. That makes the inter-catalogue scatter an upper-leaning proxy for today's per-dwarf
systematic. Shared systematics (both catalogues using the same stars) are invisible to this test and make it lower-leaning. Both
directions are stated; neither is corrected.
