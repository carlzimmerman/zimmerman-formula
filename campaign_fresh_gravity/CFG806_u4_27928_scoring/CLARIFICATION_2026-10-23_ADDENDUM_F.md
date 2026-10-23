# CFG806-U4 (U4_27928, programme 2024.1.00100.L, public 2026-11-06): clarification addendum F (2026-10-23; PRE-DATA; owner-approved; nothing frozen edited)

**Status.** Written and committed before any byte of either ALMA programme has been read. The owner approved it on 2026-10-23
("Yes: file ALMA addendum F from the S3 draft into CFG806 and CFG809 as a labelled parallel reading, ledger row included, before
Nov 6."). FROZEN_CRITERIA.md, the earlier clarification files, addenda A–E and every seal are not edited. The same text is filed
in both plan directories (CFG806_u4_27928_scoring and CFG809_gs4_24110_ci21_scoring). Source draft:
`rebuild_2026_10_22/S3_v3_mw_seals/ADDENDUM_F_DRAFT.md`; rule 4's U4 interpolation is added here, before any data.

**Why.** The current best theory (v3, `covariant_push_2026_10_22/THEORY_V3_DRAFT.md`) has the static limit AQUAL,
∇·[μ(|∇Φ|/a₀)∇Φ] = 4πGρ_b with μ = x/(1+x) (E2, C4). Addendum E's n = 1 reading (AG4e, `SEALED_N1.json`, sha256 9802de0d…)
applies ν₁ algebraically to the in-plane Newtonian field of razor-thin discs. That is AQUAL only in spherical symmetry. In a thin
disc the field just off the plane carries the vertical 2πGΣ-type component (exact in the Brada–Milgrom Kuzmin solution), so
AQUAL's in-plane pull at the comparison radius differs from the algebraic one. Lane S3_v3_mw_seals solved AQUAL for the same discs
(checks D1–D5 and D6′ pass; frozen D6 mis-specified, its AMENDMENT A5). Its frozen rule (|Δ log V²_bar,req| ≤ 0.01 dex,
|Δ log M_gas,req| ≤ 0.03 dex, no FLOOR flip) reads **v3 NEEDS ADDENDUM F**:
- GS4_24110: AQUAL's in-plane pull from the stars at R_e is 0.916–0.948 of the algebraic ν₁ value, so v3 needs more baryons:
  +0.029 to +0.046 dex in V²_bar,req (non-FLOOR cells), +0.09 to +0.47 dex in M_gas,req, and 4 FLOOR flips at log M★ 10.89
  (AG4e FLOOR → finite gas requirement).
- U4_27928: |Δ log V²_bar,req| ≤ 0.0009 dex, |Δ log M_gas,req| ≤ 0.055 dex (near FLOOR), no FLOOR flip.

The v3 requirement is sealed in `rebuild_2026_10_22/S3_v3_mw_seals/SEALED_V3_ALMA_AQUAL.json`, sha256
`b5d65a5e17bbce21c3ca2f3cd748169fe736e9b86281ff1329449176e1a8c11d` (`ALMA_V3_HASH.txt`, commit 90f4d517d6).

## Ruling
1. **The verdict kernel stays ν_mono**, as sealed in CFG571 (259f7825c, be27457d…). Every verdict line of this plan is unchanged.
   Addendum E's n = 1 (AG4e) and n = 2 (AG4d) readings stay as filed.
2. **v3's AQUAL-disc requirement is scored as a further labelled parallel reading ('v3 AQUAL disc')**, by the identical rules:
   §3–§5 of FROZEN_CRITERIA.md (1bf70683b), CLARIFICATION_2026-10-21.md and its addenda A and E. Same gates, same measured
   quantities, same σ, same wording, same FLOOR rule, both footings (canonical 9.36e-11, alt 1.13e-10), every branch of the plan.
3. **Never pooled.** This reading is never combined with ν_mono, n = 1, n = 2, the other footing or the other disc (CFG809-GS4).
   Each output line states 'v3 AQUAL disc'.
4. **Requirements; no AQUAL solve after the data are read.** The requirement uses S3's algebra (`s3_alma.py`, `aqual_cell`) with
   the sealed AQUAL/algebraic in-plane ratio C: g_bar,req solves C·ν₁(g_bar/a₀)·g_bar = g_obs; FLOOR iff
   C_stars·ν₁(g★/a₀)·g★ ≥ g_obs; M_gas,req from V²_gas = g_bar,req·R − V★² for the sealed gas rows R_g = R_d and 1.5 R_d.
   - **GS4** (sealed V_c 206 km/s at R_e = 7.39 kpc; sealed log M★ rows 10.89 primary and 10.76): read directly from the seal.
   - **U4** (measured V_c at the frozen R = 2R_e = 8.3 kpc): C_stars and C_final[R_g] are interpolated linearly in V_c between
     the two bracketing sealed grid points (150, 175, …, 300 km/s), per footing, branch and R_g row. Across that grid the sealed
     C lies in 0.985–0.9994; its largest step between neighbouring grid points is 0.008 (alt, L-fb(RAR-eq), R_g = 1.5 R_d, where
     FLOOR gives way to a gas requirement), so V²_bar,req moves by ≤ 0.004 dex under the interpolation; M_gas,req is more
     sensitive only next to FLOOR. This interpolation is a pre-data convention of this labelled reading and carries no verdict
     weight. A measured V_c outside [150, 300] km/s is reported 'not sealed' for this reading.
   - At every sealed grid point the harness must reproduce the sealed logVbar2R_G, logVbar2R_G_Rg=1.5Rd and logMgas values
     (checked in every run; a mismatch stops this reading, never the ν_mono verdict).
5. **Δ_v for this reading** uses V²_bar,req,AQ (the Newtonian in-plane V² of the required AQUAL configuration: Freeman stars plus
   the required exponential gas disc) in place of the algebraic V²_bar,req; V²_bar,meas is unchanged. The R_g = 1.5 R_d branch
   uses the sealed `logVbar2R_G_Rg=1.5Rd`.
6. **Measured gas size (gate G3).** If G3 passes, the AQUAL requirement at the measured R_g is not in the seal; it is reported as
   'not sealed', and only the sealed R_g = R_d / 1.5 R_d rows are scored.
7. **No law-form or theory statement from one disc.** One disc excludes no model.
8. **Harness.** The CFG942 harness gains a 'v3aq' kernel that reads the seal and applies rule 4. The ν_mono, n = 1 and n = 2 paths
   must stay byte-identical in output, and the new kernel is tested on MOCK (both MUTATE controls biting) before 2026-11-06.

## The sealed v3 AQUAL-disc requirement beside AG4e (GS4_24110; log M_gas,req at R_g = R_d; canonical / alt)

| log M★ | branch | AG4e (ν₁ algebraic) | v3 AQUAL disc | Δ log V²_bar,req |
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

U4_27928: on the sealed grid the v3 AQUAL-disc requirement differs from AG4e by ≤ 0.001 dex in V²_bar,req and ≤ 0.055 dex in
M_gas,req (near FLOOR); the full grid is in the seal and in the S3 draft.

κ = ½ FITTED; footings never pooled; cold energy mass required; one disc excludes no model; not theory closed.
