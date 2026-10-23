# DRAFT — ALMA clarification addendum F (v3's AQUAL-disc reading) — lane S3_v3_mw_seals, for the coordinator

**Status: DRAFT, not filed.** Written in `rebuild_2026_10_22/S3_v3_mw_seals/` only. Filing it in `CFG806_u4_27928_scoring/` and
`CFG809_gs4_24110_ci21_scoring/` needs the owner's approval (as addendum E did). It must be committed before any byte of either
programme is read (U4: 2026-11-06; GS4: 2026-11-28). FROZEN_CRITERIA.md, the clarification files, addenda A–E and every seal stay
untouched.

**Why.** v3's static limit is AQUAL with μ = x/(1+x) (E2, C4). Its spherical form is ν₁, which AG4e sealed (`SEALED_N1.json`,
sha256 9802de0d…) by applying ν₁ algebraically to the in-plane Newtonian field of razor-thin discs. In a disc AQUAL is not that
algebraic rule: the field magnitude just off the plane includes the vertical 2πGΣ-type component (the Brada–Milgrom Kuzmin
solution makes this exact), so at the comparison radius AQUAL's in-plane pull differs from the algebraic one. Lane S3 solved
AQUAL for the same discs (`s3_partD_alma.py`, `s3_alma.py`, `s3_aqual.py`; checks D1–D5 and D6′ pass; frozen D6 mis-specified,
AMENDMENT A5). By its frozen rule (|Δ log V²_bar,req| ≤ 0.01 dex, |Δ log M_gas,req| ≤ 0.03 dex, no FLOOR flip) the result is:
**v3 NEEDS ADDENDUM F** (max |Δ log V²_bar,req| 0.046 dex, max |Δ log M_gas,req| 0.47 dex, 4 FLOOR flips).

- GS4_24110|10.89: max |Δ log V²_bar,req| 0.0291 dex, max |Δ log M_gas,req| 0.451 dex, FLOOR flips 4 → needs addendum F.
- GS4_24110|10.76: max |Δ log V²_bar,req| 0.0458 dex, max |Δ log M_gas,req| 0.465 dex, FLOOR flips 0 → needs addendum F.
- U4_27928: max |Δ log V²_bar,req| 0.0009 dex, max |Δ log M_gas,req| 0.055 dex, FLOOR flips 0 → needs addendum F.

**What changes, physically.** At GS4's comparison radius (R_e = 1.68 R_d) AQUAL's in-plane pull from the stars is 0.916–0.948 of the algebraic ν₁ value, so v3 needs MORE baryons there than AG4e: +0.029 to +0.046 dex in V²_bar,req (non-FLOOR cells), which becomes +0.09 to +0.47 dex in M_gas,req and turns 4 AG4e FLOOR cells (GS4 log M★ 10.89) into finite gas requirements. At U4's radius (2 R_e = 3.36 R_d) the ratio is 0.9983–0.9994: V²_bar,req moves by ≤ 0.001 dex, but the gas requirement still moves by up to 0.055 dex in near-FLOOR cells, which is what fails the frozen 0.03 dex line for U4.

## Proposed ruling (mirrors addendum E)
1. **The verdict kernel stays ν_mono** (CFG571), and addendum E's n = 1 (AG4e) and n = 2 (AG4d) readings stay as filed.
2. **v3's AQUAL-disc requirement is scored as a further labelled parallel reading**, by the identical rules (§3–§5 of each plan's
   FROZEN_CRITERIA.md, CLARIFICATION_2026-10-21.md and addenda A–E): same gates, measured quantities, σ, wording, FLOOR rule, both
   footings, every branch. The requirement is read from `rebuild_2026_10_22/S3_v3_mw_seals/SEALED_V3_ALMA_AQUAL.json`
   (sha256 `b5d65a5e17bbce21c3ca2f3cd748169fe736e9b86281ff1329449176e1a8c11d`, `ALMA_V3_HASH.txt`), never recomputed after the data are read.
3. **Δ_v for this reading** uses V²_bar,req,AQ (the Newtonian in-plane V² of the required AQUAL configuration: Freeman stars +
   the required exponential gas disc) in place of the algebraic V²_bar,req; V²_bar,meas is unchanged. For the R_g = 1.5 R_d branch the
   sealed `logVbar2R_G_Rg=1.5Rd` is used.
4. **Never pooled** with ν_mono, n = 1, n = 2, the other footing or the other disc. Each output line states 'v3 AQUAL disc'.
5. **Measured gas size (gate G3).** If G3 passes, the AQUAL requirement at the measured R_g is NOT in the seal; it is then reported
   as 'not sealed' and only the sealed R_g = R_d / 1.5 R_d rows are scored.
6. **No law-form or theory statement from one disc.** One disc excludes no model.

## The sealed v3 AQUAL-disc requirement beside AG4e (log M_gas,req, R_g = R_d; canonical / alt)

### GS4_24110

| log M★ | branch | AG4e (ν₁ algebraic) can / alt | v3 AQUAL disc can / alt | Δ log V²_bar,req can / alt |
|---|---|---|---|---|
| 10.89 | BH-k3 | 9.61 / FLOOR | 9.98 / 9.72 | +0.029 / +0.033 |
| 10.89 | E | FLOOR / FLOOR | FLOOR / FLOOR | +0.040 / +0.044 |
| 10.89 | E-CCBH | FLOOR / FLOOR | FLOOR / FLOOR | +0.040 / +0.044 |
| 10.89 | F-DESI | 9.53 / FLOOR | 9.96 / 9.66 | +0.029 / +0.033 |
| 10.89 | F-flat | FLOOR / FLOOR | 9.77 / 9.10 | +0.032 / +0.036 |
| 10.89 | L-fb(RAR-eq) | FLOOR / FLOOR | FLOOR / FLOOR | +0.054 / +0.058 |
| 10.89 | R-H | FLOOR / FLOOR | FLOOR / FLOOR | +0.055 / +0.059 |
| 10.76 | BH-k3 | 10.38 / 10.29 | 10.47 / 10.40 | +0.029 / +0.033 |
| 10.76 | E | 9.98 / 9.62 | 10.21 / 10.04 | +0.041 / +0.046 |
| 10.76 | E-CCBH | 10.01 / 9.67 | 10.22 / 10.06 | +0.041 / +0.045 |
| 10.76 | F-DESI | 10.37 / 10.27 | 10.46 / 10.39 | +0.029 / +0.033 |
| 10.76 | F-flat | 10.30 / 10.18 | 10.42 / 10.33 | +0.032 / +0.036 |
| 10.76 | L-fb(RAR-eq) | FLOOR / FLOOR | FLOOR / FLOOR | +0.057 / +0.061 |
| 10.76 | R-H | FLOOR / FLOOR | FLOOR / FLOOR | +0.059 / +0.063 |

### U4_27928

| V_c | branch | AG4e (ν₁ algebraic) can / alt | v3 AQUAL disc can / alt | Δ log V²_bar,req can / alt |
|---|---|---|---|---|
| 150 | BH-k3 | FLOOR / FLOOR | FLOOR / FLOOR | +0.000 / +0.001 |
| 150 | E | FLOOR / FLOOR | FLOOR / FLOOR | +0.001 / +0.001 |
| 150 | E-CCBH | FLOOR / FLOOR | FLOOR / FLOOR | +0.001 / +0.001 |
| 150 | F-DESI | FLOOR / FLOOR | FLOOR / FLOOR | +0.000 / +0.001 |
| 150 | F-flat | FLOOR / FLOOR | FLOOR / FLOOR | +0.000 / +0.001 |
| 150 | L-fb(RAR-eq) | FLOOR / FLOOR | FLOOR / FLOOR | +0.001 / +0.001 |
| 150 | R-H | FLOOR / FLOOR | FLOOR / FLOOR | +0.001 / +0.001 |
| 175 | BH-k3 | FLOOR / FLOOR | FLOOR / FLOOR | +0.000 / +0.000 |
| 175 | E | FLOOR / FLOOR | FLOOR / FLOOR | +0.001 / +0.001 |
| 175 | E-CCBH | FLOOR / FLOOR | FLOOR / FLOOR | +0.001 / +0.001 |
| 175 | F-DESI | FLOOR / FLOOR | FLOOR / FLOOR | +0.000 / +0.001 |
| 175 | F-flat | FLOOR / FLOOR | FLOOR / FLOOR | +0.000 / +0.001 |
| 175 | L-fb(RAR-eq) | FLOOR / FLOOR | FLOOR / FLOOR | +0.001 / +0.001 |
| 175 | R-H | FLOOR / FLOOR | FLOOR / FLOOR | +0.001 / +0.001 |
| 200 | BH-k3 | FLOOR / FLOOR | FLOOR / FLOOR | +0.000 / +0.000 |
| 200 | E | FLOOR / FLOOR | FLOOR / FLOOR | +0.001 / +0.001 |
| 200 | E-CCBH | FLOOR / FLOOR | FLOOR / FLOOR | +0.001 / +0.001 |
| 200 | F-DESI | FLOOR / FLOOR | FLOOR / FLOOR | +0.000 / +0.000 |
| 200 | F-flat | FLOOR / FLOOR | FLOOR / FLOOR | +0.000 / +0.001 |
| 200 | L-fb(RAR-eq) | FLOOR / FLOOR | FLOOR / FLOOR | +0.001 / +0.001 |
| 200 | R-H | FLOOR / FLOOR | FLOOR / FLOOR | +0.001 / +0.001 |
| 225 | BH-k3 | 9.67 / 9.03 | 9.67 / 9.06 | +0.000 / +0.000 |
| 225 | E | FLOOR / FLOOR | FLOOR / FLOOR | +0.001 / +0.001 |
| 225 | E-CCBH | FLOOR / FLOOR | FLOOR / FLOOR | +0.001 / +0.001 |
| 225 | F-DESI | 9.65 / 8.96 | 9.66 / 8.98 | +0.000 / +0.000 |
| 225 | F-flat | 9.53 / FLOOR | 9.53 / FLOOR | +0.000 / +0.001 |
| 225 | L-fb(RAR-eq) | FLOOR / FLOOR | FLOOR / FLOOR | +0.001 / +0.001 |
| 225 | R-H | FLOOR / FLOOR | FLOOR / FLOOR | +0.001 / +0.001 |
| 250 | BH-k3 | 10.36 / 10.28 | 10.37 / 10.28 | +0.000 / +0.000 |
| 250 | E | 10.20 / 10.05 | 10.20 / 10.05 | +0.000 / +0.001 |
| 250 | E-CCBH | 10.20 / 10.05 | 10.20 / 10.05 | +0.000 / +0.001 |
| 250 | F-DESI | 10.36 / 10.28 | 10.36 / 10.28 | +0.000 / +0.000 |
| 250 | F-flat | 10.34 / 10.24 | 10.34 / 10.24 | +0.000 / +0.000 |
| 250 | L-fb(RAR-eq) | 9.83 / 9.25 | 9.83 / 9.27 | +0.001 / +0.001 |
| 250 | R-H | 9.25 / FLOOR | 9.28 / FLOOR | +0.001 / +0.001 |
| 275 | BH-k3 | 10.64 / 10.60 | 10.64 / 10.60 | +0.000 / +0.000 |
| 275 | E | 10.55 / 10.49 | 10.55 / 10.49 | +0.000 / +0.000 |
| 275 | E-CCBH | 10.55 / 10.49 | 10.55 / 10.49 | +0.000 / +0.000 |
| 275 | F-DESI | 10.64 / 10.60 | 10.64 / 10.60 | +0.000 / +0.000 |
| 275 | F-flat | 10.63 / 10.58 | 10.63 / 10.58 | +0.000 / +0.000 |
| 275 | L-fb(RAR-eq) | 10.41 / 10.29 | 10.41 / 10.30 | +0.001 / +0.001 |
| 275 | R-H | 10.30 / 10.14 | 10.30 / 10.14 | +0.001 / +0.001 |
| 300 | BH-k3 | 10.83 / 10.80 | 10.83 / 10.80 | -0.000 / +0.000 |
| 300 | E | 10.77 / 10.72 | 10.77 / 10.72 | +0.000 / +0.000 |
| 300 | E-CCBH | 10.77 / 10.72 | 10.77 / 10.72 | +0.000 / +0.000 |
| 300 | F-DESI | 10.83 / 10.79 | 10.83 / 10.79 | -0.000 / +0.000 |
| 300 | F-flat | 10.82 / 10.78 | 10.82 / 10.78 | +0.000 / +0.000 |
| 300 | L-fb(RAR-eq) | 10.67 / 10.60 | 10.67 / 10.61 | +0.000 / +0.001 |
| 300 | R-H | 10.61 / 10.52 | 10.61 / 10.53 | +0.001 / +0.001 |

κ = ½ FITTED; footings never pooled; cold energy mass required; one disc excludes no model; not theory closed.
