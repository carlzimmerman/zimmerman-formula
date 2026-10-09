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
