# CFG212 — BUDHIES external-field pre-flight: can the HI widths near A963/A2192 separate an EFE-merge law from B's isolated law? FROZEN CRITERIA

Written 2026-09-29 in the calculation chat, at the orchestrator's request, before any CFG212 number. **κ = ½ FITTED, NOT DERIVED.**
- This is a POWER pre-flight. It uses the galaxies' positions, redshifts and the published cluster masses, and NO W50.
- A W50 test is frozen and run later only if this pre-flight says it has power.

## What was seen before this was written

- The orchestrator's reading of B (not a committed formula), under FG001 (CFG11, T5): "members' cold components are lumps inside [the group's phantom], never added on top".
  - So B predicts that a member disc's W50 at fixed M_b equals the isolated-law value (no EFE suppression).
  - The exception is tidal stripping, which is not modelled.
  - The EFE-merge law predicts suppression, through ν evaluated with the cluster's g_ext.
- The data chat's inputs (`data_assembly/BUDHIES_PREFLIGHT_2026-09-29.md`, d5d584788; summariser reads, UNVERIFIED): centres, masses, dispersions, extents and the HI-mass limit, with the conflicts it lists.
- **Disclosure.** While checking the column format of `budhies_joined.csv` I displayed its first two data rows, which include W20/W50 for two galaxies (A963 #1 and #2). No other W50 has been seen, and none enters this pre-flight.

## Inputs (declared on input-side grounds)

| input | primary | optimistic bracket (more EFE) |
|---|---|---|
| A963 M200 | 8.92e14 M☉ (X-ray, Martino+2014 via Haines+2018) | 1.4e15 ("total", BUDHIES IV) |
| A2192 M200 | 2.27e14 M☉ (A2192_1a, Jaffé+2013) | 3.3e14 (2.3e14 h⁻¹ at h = 0.7) |
| centres | BUDHIES IV Table 1 for both | A2192 at Jaffé+2013's luminosity-weighted centre (reported) |
| mass profile | NFW, c200 = 4 (declared) | |
| membership | cluster field as tabulated; \|Δv\| = c\|z_HI − z_cl\|/(1 + z_cl) < 3σ, σ = 993 (A963, newer) / 653 (A2192) | σ = 1350 for A963 (older) |
| 3D distance | r = R_proj × √(3/2) (the isotropic mean deprojection) | r = R_proj (maximum EFE) |
| internal field at the HI edge | y_int = g_N,int/a₀ = 0.3 | 0.1 (a weaker internal field gives more EFE); 1.0 reported |
| per-galaxy noise in log W50 (no inclinations) | σ = 0.20 dex | 0.15 |
| cosmology for distances | flat ΛCDM, H₀ = 70, Ω_m = 0.3 | |

- Other members of each field are counted with an effect of zero.

## Model

- **External field.** The observed total cluster field at r is g_ext,obs = G M_NFW(<r)/r². Its Newtonian-equivalent y_ext solves ν(y_ext) y_ext = g_ext,obs/a₀, i.e. the law holding for the cluster with whatever mass it has.
- **B, the isolated law:** g_iso = ν(y_int) y_int a₀.
- **Merge, the EFE law:**
  - Primary, perpendicular form (in-plane internal field perpendicular to g_ext): g_EFE = ν(√(y_int² + y_ext²)) y_int a₀.
  - Variant, parallel form: [ν(y_int + y_ext)(y_int + y_ext) − ν(y_ext) y_ext] a₀.
- **Kernel:** P2, ν = √(1 + 1/y) (the framework's law, as in CFG200). ν_mono is a variant. The canonical footing a₀ = 9.36e-11 is primary; alt is reported.
- **Per-galaxy effect:** Δ_i = ½ log₁₀(g_EFE / g_iso), the predicted log V shift of merge relative to B at the HI edge (≤ 0).
- **Power:** S_opt = √(Σ Δ_i²) / σ. This is the separation of the optimal known-template linear test, an UPPER bound on any real test's power.
- **Also reported:** members within 1 and 2 Mpc projected of each centre; the median and minimum Δ_i; the fraction of Σ Δ² from within 1 Mpc; the HI-mass limit's rise toward the field edge (qualitative, from the note).

## Decision rows

- **P1.** If S_opt < 3 in the OPTIMISTIC cell (every optimistic bracket at once): "NON-DIAGNOSTIC: no W50 test is frozen".
- **P2.** If S_opt ≥ 3 in the PRIMARY cell: "a W50 test may be frozen next". Its own criteria would add the M*/L (factor ~2), W50→V_flat and stripping systematics.
- **Otherwise:** "power only under optimistic inputs: not run unless the inputs are tightened (verified masses, M500, a membership catalogue)".
- **Reported:** the full grid (masses × deprojection × y_int × σ × form × kernel × footing).

## Controls

- **C1.** With the cluster masses set to 0, every Δ_i = 0 and S_opt = 0.
- **C2.** The kernel limits: ν(y) → 1 as y → ∞, and √y ν(y) → 1 as y → 0. In the strong-field limit y_ext ≫ y_int, g_EFE/g_iso → ν(y_ext)/ν(y_int).
- **C3.** R_proj for the table's first galaxy, recomputed by hand from its RA/Dec and the centre, agrees with the code to 1e-6 Mpc.
- **MUTATE=1.** The A963 mass is multiplied by 100. S_opt must rise above its main-run value, so the machinery responds to the external field. Outputs are written separately.
