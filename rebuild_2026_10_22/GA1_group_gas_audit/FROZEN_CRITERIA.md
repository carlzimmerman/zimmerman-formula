# GA1_group_gas_audit: FROZEN CRITERIA (committed alone, before any script or number of this lane)

Written 2026-10-28, at the owner's request: "freeze and run a data-only audit of the 14 X-ray-bright groups' hot-gas
masses (eRASS1 Mgas500 and the β-model) and regrade HG2's sign with the audited gas."

**Why.** DS1 (fcc40606a6) found that no rule g_pred = F(g_bar) reaches HG2's negative D. With every group on the law,
D_pred is +0.137. The sign therefore depends on the counted hot gas. HG2 flagged the BRIGHT gas-to-star ratios of 8–14
as high for groups.

**Already known before freezing (disclosed).** A look at the BRIGHT rows' eRASS1 entries shows:
- Two eRASS1 sources are each matched to **two** KT2017 groups: J122946.7+080002 (Virgo / M87) and J124249.5+024117.
- Several sources are at z ≤ 0.012, where eRASS1's extent fits are least reliable.
- Some X-ray temperatures disagree strongly with the group σ.

The rules below were written after that look, and no regraded number was seen.

**Standing rules.**
- κ = ½ FITTED.
- Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled; canonical is primary.
- Cold dark energy is a gravitating w ≈ 0 field component, not matter and not a particle.
- No ΛCDM number enters a rule.
- Not "theory closed". Nothing here may say the data favour the framework.
- No downloads; on-disk data only.

## 1. Audit rules (data only, frozen)

**(a) One source, one group.** An eRASS1 source matched to several KT2017 groups stays BRIGHT only for the group with
the largest Nm (ties go to the smaller centre separation). The other groups are **dropped** from both arms: they are
neither BRIGHT, nor FAINT with zero gas.

**(b) Temperature–dispersion consistency (reported, and graded as variant V-b).**
- β_spec = σ_LOS² / (kT/(μ m_p)), with μ = 0.6, using eRASS1's KT.
- A BRIGHT group with β_spec outside [1/3, 3] is flagged MISMATCHED (σ disagreeing with kT by a factor > 1.73).
- V-b drops the MISMATCHED groups.

**(c) Audited gas mass (PRIMARY): measured XMM group scaling.**
- **Fits:** on Lovisari, Reiprich & Schellenberger 2015 (on disk: `real_research/data/lovisari2015_groups.tsv`;
  20 groups with hydrostatic-independent gas masses from double-β profiles), least-squares
  log Mgas500 = a + b log kT and log R500 = c + d log kT. The R500 values are Lovisari's own, as published.
- **Applied:** to each BRIGHT group's eRASS1 KT, giving Mgas500,aud and R500,aud.
- **h conversion:** Lovisari's h70 values are converted to the native h 0.6856427 (Mgas ∝ h^−5/2, R ∝ h^−1).
- **Reported:** the relation's scatter, propagated as a variant (±1σ_scatter).
- **Disclosed:** Lovisari's R500 is defined from hydrostatic masses. Only its kT relation enters here, as an empirical
  gas extent.
- **Gas inside r:** HG1's β-model (r_c = 0.15 R500, β = 2/3) with R500,aud.
- **Profile check (reported):** the β-model's M(<0.45 R500)/M(<R500), compared with Lovisari's median
  Mgas2500/Mgas500.

**(d) Reported, not graded.**
- The ratio eRASS1 Mgas500 / Mgas500,aud per group.
- Each group's gas-to-star ratio before and after the audit.

## 2. Regrade (canonical primary; alt with its own)

The audited gas changes g_bar for the BRIGHT groups:
- g_bar = G (0.5 M★ + M_gas,aud(<r))/r²;
- for the switch, M_b,tot = M★ + Mgas500,aud.

The same audited rows feed:
- **Measured:** D_meas,aud with its 95 % interval, from HG2's statistic and bootstrap (`hg2.bootstrap`, blue-lens
  reference, the same seed).
- **Predicted:** D_pred,aud under the base picture (HO1(b)'s `group_pred`, CL2 + EM1 switch) and, reported, under all
  groups on the law.

**Verdict (frozen, canonical primary):**

| verdict | condition |
|---|---|
| **GAS AUDIT RECONCILES THE SIGN** | D_pred,aud (base picture) lies inside the audited 95 % interval of D_meas,aud |
| **GAS AUDIT MOVES THE SIGN BUT DOES NOT RECONCILE** | not reconciled, but \|D_pred,aud − D_meas,aud\| is at least 30 % smaller than the unaudited \|0.229 − (−0.294)\| = 0.523 (canonical) |
| **GAS AUDIT DOES NOT HELP** | otherwise |

**Variants (each reported with the same classes, not promoted):**
- V-a: rule (a) only, with eRASS1 gas;
- V-b: (a) + (c) + MISMATCHED dropped;
- V-σ±: the Lovisari scatter at ±1σ.

**Power.** HG2's power rule is re-evaluated on the audited sample and reported. If the audited BRIGHT arm in shared σ
bins falls below HG2's minimum of 6, the class is **UNDERPOWERED**, whatever the numbers say.

## 3. Checks (all must pass) and twin

- **K0 (Step 0).** With no audit, the run reproduces HG2's D −0.294 [−0.511, −0.076] and HO1(b)'s D_pred +0.2293 /
  +0.2011.
- **K1.** The Lovisari fit is reproducible, its coefficients are printed, and its residual rms is reported. Every
  audited BRIGHT row's M_gas,aud(<r) equals Mgas500,aud × the β fraction to 1e-12.
- **K2.** No eRASS1 source is assigned to more than one BRIGHT group after rule (a).
- **K3.** Peak RSS < 1 GB, one thread.
- **Rerun.** The results JSON is byte-identical.
- **MUTATE (`GA1_MUTATE=1`, separate outputs).** Rule (a) is disabled (duplicates kept) while K2 still runs, so K2 must
  fail and the run must exit 1.

**Run:** `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I ga1_group_gas_audit.py`
