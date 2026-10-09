# CFG528: the four SLUGGS centrals -- data re-check, hot gas, derived mechanisms

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (5ad8324fa).
- **Script:** `cfg528_mechanism.py` (about 1 s). Outputs `cfg528_mechanism.out` / `_results.json` (6/6 checks).
  MUTATE: `CFG528_MUTATE=1` → `_MUTATE.*` (1/3 pass; two teeth FAIL and are kept, see below).
  Post-freeze diagnostic: `CFG528_POSTFREEZE=1` → `_POSTFREEZE.*`.
- **Settings:** CFG331's machinery exec'd read-only (as CFG466); γ = 3, β = 0 primary; ν_mono; κ = ½ FITTED; footings
  9.36e-11 / 1.13e-10, never pooled. Per-galaxy errors are CFG466's GC bootstrap (statistical only). On-disk data only; nothing
  downloaded. The cold energy's mass is still required. Not "theory closed".

## Frozen verdict: GENUINE TENSION (7.8σ on the less favourable footing, joint best case at γ = 3)

**It is conditional on the GC tracer slope.** The frozen joint best case keeps γ = 3. CFG466 already showed that with γ free
(U[2,4]) plus β = +0.5 under R-own, all four clear (NOT DIAGNOSTIC there). So the tension is robust against every **mass-side**
lever on disk (IMF, distance, hot gas, environment, census edge, round rule, EFE). The only lever that can remove it is the
**tracer** (slope + anisotropy), and that lever is unmeasured for three of the four. The σ values are statistical only.
CFG466's post-freeze headroom: a per-galaxy systematic of 0.05–0.075 dex in σ_los would clear M87, NGC 4365 and NGC 5846 under K0.

## Item 1: data / assumption re-check (offsets in dex; Z = offset/σ_i; can | alt)

| row | centrals' mean | cleared (of 4) | closes? |
|---|---|---|---|
| K0, JAM-law ceiling (record) | +0.224 / +0.213 (Z_class 10.9 / 10.4) | 0 / 0 | no |
| Salpeter population M* | +0.186 / +0.171 | 0 / 0 | no; also INADMISSIBLE (inner excess up to +0.21 dex) |
| Chabrier (= Salp − 0.25) | +0.263 / +0.246 | 0 / 0 | no (lighter than the JAM ceiling for 3 of 4) |
| 2× Chabrier (bottom-heavy) | +0.170 / +0.155 | 0 / 1 | no; INADMISSIBLE (inner excess up to +0.25) |
| ATLAS3D distance | +0.223 / +0.213 | 0 / 0 | no |
| SBF × 0.9 / × 1.1 | +0.230 / +0.218 (can) | 0 | no |
| β = −0.5 / +0.5 (γ = 3) | +0.222 / +0.227 (can) | 0 | no (radial orbits make it slightly worse at γ = 3) |
| all bins | +0.235 / +0.226 | 0 | no |
| R-efe | +0.295 / +0.291 | 0 | worse (E1 PASS) |

- **IMF.** The record's M* is the JAM-law ceiling, which is IMF-neutral and already heavy: it lies 0.14 dex above Chabrier for
  M87, NGC 4374 and NGC 5846, i.e. it already contains a Salpeter-like IMF. Any heavier IMF over-predicts each galaxy's own
  inner JAM mass. Post hoc, nulling each central needs M* × 10^0.59–0.78 (×3.9–6.0) on the ceiling, which would over-predict the
  inner JAM mass by +0.51 to +0.73 dex. A bottom-heavy core with a lighter outside (the measured gradient sense) makes it worse.
- **Distances.** σ_pred barely moves with D: ±10% shifts the offset by about 0.006 dex. No factor in ×0.2–×20 nulls any central.
- **Round rule.** The prediction already is CFG516's round enclosed-mass rule (spherical algebraic law = spherical QUMOND).
  R1: the phantom mass rebuilt from its own density matches to 3.9e-6.
- **Radial range.** The offset is present in every bin choice: outermost bin only +0.240, innermost outer bin +0.208 (can).
- **Not re-checkable on disk.** Per-galaxy GC density slopes for NGC 4365, 4374 and 5846; GC anisotropy for all four. The
  Forbes+17 table-vs-N provenance flag (AUDIT_SLUGGS 1d) is still unresolved.

## Item 2: hot gas (the census counts it as retained baryons)

| row | can | alt | closes? |
|---|---|---|---|
| gas truncated at the measured edge | +0.206 | +0.196 | no |
| gas extrapolated (CFG331 R-bar) | +0.202 | +0.191 | no |
| R-own (host gas + members, CFG331) | +0.198 | +0.187 | no |

- Post hoc, the gas multiplier on the measured profile shape that nulls each central:
  - M87: ×18.5 / ×16.9;
  - NGC 5846: ×35.1 / ×31.0;
  - NGC 4365: ×268 / ×239;
  - NGC 4374: ×196 / ×175.
- M87's Virgo gas is measured to 1.2 Mpc (Urban+11), so M87's gap is not hidden gas beyond the field.
- The L_X correlation on record (cold_mass cm05: partial ρ +0.47 given mass) is carried by group/cluster central status
  (cm07, cm09). It is not the gas's own mass.

## Item 3: derived mechanisms

- **Census edge / supply cap: it never binds.**
  - r_edge = 475–1626 kpc, against outermost GC radii of 22–109 kpc.
  - M_ph(<R_out) is 1–18% of the supply, for both own and host baryons, on both footings.
  - Candidate B puts exactly the law's phantom inside the edge. So the census can only remove mass (where it binds) and never adds any. The prediction is unchanged: +0.202 / +0.191.
- **Round rule:** already applied (item 1).
- **Host ownership** (R-own): a 15% / 16% drop, as in CFG331.
- **Verdict: no derived mechanism.** Every derived reading of candidate B leaves the four centrals at +0.19 to +0.21 dex.

### Template (NOT derived): the host's unsettled cold energy, from the X-COP profile (CFG432)
M_u = Q(r/R500) M_gas,host with Q01 = 10.9 / 10.5 and slope −0.55 / −0.60 (CFG432 JSON). R500 values are recalled and PROVISIONAL (Virgo 0.70 Mpc, NGC 5846 group 0.38 Mpc). It is applied to the host centres only.

**Label: TEMPLATE NO in all four variants.**
- M87 falls from +0.204 to +0.102 (Z 5.9) and NGC 5846 from +0.187 to +0.164. Even the two host centres stay excluded.
- The variants (flat Q inward, R500 × 0.7 and × 1.3) give M87 +0.09 to +0.12.
- Joint best case + template: mean +0.142 / +0.130, cleared 0/4.

## Joint best case (all admissible levers in the law's favour)
The case combines R-own, β = +0.5, the heaviest admissible IMF per galaxy and D × 1.1.
- Means: +0.177 / +0.161.
- Z_class: 8.6 / 7.8.
- Cleared: 0/4 on both footings.

## MUTATE (1/3; FAILS kept as they fell)
- **MA FAIL (narrowly).** Chabrier masses with no gas and no members: 0/4 cleared on both footings, and offsets up to +0.057 above K0. The criterion "every offset ≥ K0" fails in one cell: NGC 4365 alt is −0.007 below K0. NGC 4365's Chabrier mass exceeds its alt-footing JAM ceiling (inner excess +0.018), which the frozen text did not anticipate. The intended tooth fires: the fail is detected when the levers are removed.
- **MB FAIL.** Planting M* × 8 over-shoots. 3 of 4 centrals become REVERSED (Z −2.8 to −4.3), so by the frozen rule the row does not "close".
- **MC PASS.** The template × 0 reproduces CFG331 R-own exactly.

## Disclosures (2026-10-09, after the freeze)
1. **Post-freeze diagnostic PF.** It was added after MB over-shot, to show that the CLOSES criterion can fire. Planted M* × 5 clears 4/4 on both footings with none reversed: PASS (`_POSTFREEZE.*`). It is not a decision row.
2. **The template row's star calibration includes M_u inside r_½.** JAM measures total mass. The frozen text did not specify this.
3. **The joint best case uses β = +0.5 as frozen.** At γ = 3, β = −0.5 is marginally more favourable (−0.002 dex). This does not change the result.
4. **No frozen text was edited.** CFG330, CFG331, CFG466 and the LEDGER are unchanged.

## What would decide it (fetches, owner's go needed; nothing fetched)
The deciding fetch is the tracer, not the mass. Each is a small published table, likely under about 1 MB; sizes to be confirmed at fetch.
- **Per-galaxy GC surface-density profiles** for NGC 4365, 4374 and 5846 (Pota+13 Table/Fig. 6 fits; Kartha+14/16; Hargis & Rhode).
- **GC orbital-anisotropy constraints:** Zhu+14 and Agnello+14 for M87; Pota+15-type analyses for the others.

A group-scale X-ray profile for NGC 5846 would not decide it: it would need ×31–35 the measured gas.

---

# CFG528b (2026-10-09): measured GC density profiles and measured anisotropy

- **Criteria:** `FROZEN_CRITERIA_v2.md`, committed alone first (d7a546f9c). It records the source line for every input.
- **Data:** arXiv LaTeX sources fetched by the coordinating session on the owner's direct approval, held outside git in `../_external_data/cfg528_work/src/`. The log is `FETCH_LOG.md`. Total 26.6 MB, and all SHA-256 values match (control K4).
- **Script:** `cfg528b_measured_tracers.py`, about 100 s. Outputs `.out` / `_results.json` (4/4 checks). MUTATE: `CFG528B_MUTATE=1` (2/2).

## Inputs (details in the criteria)

| galaxy | density | anisotropy |
|---|---|---|
| NGC 4374 | Gómez & Richtler 04: projected Σ ∝ R^−1.09±0.12, so 3D γ = 2.09 | unmeasured, β = 0 |
| NGC 4365 | Blom+12: Sérsic n 2.68, R_e 6.1′ | unmeasured, β = 0 |
| NGC 5846 | Napolitano+14: red + blue Sérsic | red β → 0.43, blue β → 0.15 (Churazov form) |
| M87 | Agnello+14 | Zhu+14: −0.2 → +0.2 → 0 |

At the outer GC bins the measured 3D slopes are:
- M87: 1.87–2.34;
- NGC 4365: 1.87–2.80;
- NGC 4374: 2.09;
- NGC 5846: 2.33–2.83.

## Frozen verdict: GENUINE TENSION, 2.8σ (class statistic, joint best case, alt footing; 3.5σ canonical)

| row | centrals' mean (can / alt) | cleared |
|---|---|---|
| M, K0 (stars only) | +0.181 / +0.171 | 1/4 (NGC 4374, Z 1.7 / 1.5) |
| M, R-bar | +0.155 / +0.143 | 1/4 |
| M, R-own | +0.150 / +0.139 | 1/4 |
| J joint best case (R-own, heaviest admissible IMF, D × 1.1, most favourable quoted ±2σ density and β edges; β ±0.5 for the two unmeasured) | +0.073 / +0.057 | 1/4 |

**Per galaxy in J** (can / alt):
- M87: +0.103 / +0.090 (Z 5.9 / 5.2);
- NGC 4365: +0.137 / +0.120 (Z 6.0 / 5.2);
- NGC 5846: +0.139 / +0.122 (Z 6.3 / 5.5);
- NGC 4374: −0.089 / −0.105 (Z −1.2 / −1.4).

The class Z of 2.8–3.5 is pulled down by NGC 4374 going negative. Three of the four stay individually above 5σ.

## Reading
- **The measured tracers do not support the "shallow slope" escape.**
  - CFG466 found R-own + β = +0.5 + γ free (prior U[2,4]) clears all four.
  - The measured profiles are steeper than that prior's lower edge at the outer bins for NGC 4365 and 5846.
  - NGC 5846's measured β (≤ 0.43, red) is a kinematic measurement, not a free edge.
- **NGC 4374 is the exception.** Its measured slope is shallow (γ 2.09). With σ_i = 0.074 from only 41 GCs, it is not decisive either way.
- **What remains is the same group-central residual,** now about +0.09 to +0.14 dex in three galaxies, after every quoted-uncertainty edge was turned in the law's favour.

**Caveats:**
- The σ_i are statistical only. CFG466's headroom says an extra per-galaxy systematic of about 0.05–0.075 dex (JAM M/L, distance, Hernquist scale) would be needed to clear the three. That is comparable to the J offsets, so the per-galaxy Z values overstate certainty.
- The NGC 5846 and M87 anisotropies come from Newtonian models (NFW or M2M with a dark halo), not from the law's own fit.
- The photometric GC mixture is applied to the spectroscopic sample.
- Zhu+14's β profile was digitised from the text, not from a table.
- NGC 4365 and 4374 have no measured β.

**Controls:**
- K1: the new variable-β solver reproduces CFG331 to 1e-15.
- K2: the Plummer deprojection is exact to 7e-16.
- K3: the M87 Agnello offset reproduces CFG466's C4 (+0.21780 / +0.20620).
- K4: the SHA-256 values match.

**MUTATE:**
- MA: γ = 3 with β = 0 reproduces CFG528 K0 and R-own to 1e-16.
- MB: γ = 4 with β = −0.5 does not close, and every offset rises by +0.05 to +0.12 over row M. PASS.

**Not used:** Kartha+14 (wrong galaxies); Pota+13 (fits in figures only); Agnello+14 per-population β (figures only).

**Still not on disk:** anisotropy for NGC 4365 and 4374 (e.g. Pota+15 / Napolitano+11 PN for NGC 4374). These would tighten the J edges for the two galaxies whose β was set by the ±0.5 bracket.

κ = ½ is fitted. The cold energy's mass is still required. This is not "theory closed".
