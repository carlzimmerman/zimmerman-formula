# Deeper FRB sample audit: the 114-object result contains an explicit localization bracket

**Checked 2026-09-27.** The [2026 Nature Astronomy version of record](https://www.nature.com/articles/s41550-026-02957-9) reports a 114-FRB analysis of baryonic feedback. I inspected the [authors' public catalog](https://github.com/krittisharma/dmz_spk_sharma2026/blob/6651975039b25c2ac6853527699bb6d54722f5a0/data/frb_results/frb_sample.csv) at commit `6651975039b25c2ac6853527699bb6d54722f5a0` and checked the selection in their [MCMC code](https://github.com/krittisharma/dmz_spk_sharma2026/blob/6651975039b25c2ac6853527699bb6d54722f5a0/mcmc_funcs.py). The catalog has **127 unique FRB rows**, so loading every row would not reproduce the paper.

| `sharma_sample` flag | Rows | Median `z` | Redshift range | Meaning in the authors' code |
|---|---:|---:|---:|---|
| `yes` | **92** | `0.2623` | `0.0087–2.1480` | Fiducial sample when `SAMPLE_EXTENDED != Yes` |
| `unclear` | **22** | `0.0756` | `0.0039–0.3238` | Added when `SAMPLE_EXTENDED=Yes`; all 22 catalog notes say `Arcmin-localization.` |
| `no` | **13** | `0.1918` | `0.0008–0.5310` | Excluded from both |

Thus the **114-object extended sample is `92 yes + 22 unclear`**, exactly matching the version-of-record count. The localization bracket is material: 22/114 = **19.3%** of the extended objects have an explicit uncertainty flag, and all of those lie at `z≤0.3238`. Any use of this FRB result as an external baryonic-feedback prior for DES/SPT lensing should compare the authors' *fiducial* and *extended* posterior products, including host-DM and localization assumptions, before treating its matter-power suppression band as fixed. The authors' [README](https://github.com/krittisharma/dmz_spk_sharma2026) lists separate posterior arrays and an HMcode run excluding the CHIME subarcminute-to-arcminute localizations. The catalog alone does not provide a gravity measurement or a feedback posterior.

The [standard-library audit script](frb_sample_audit.py) reproduces these counts and verifies the CSV SHA-256 `ff14bf90d455a4bcf9c5b98a7ea533c299ec78a12ac4428246d4bcffa0ef83c2`. Its [JSON result](frb_sample_audit_result.json) records subgroup redshift and DM summaries. Reproduce from the pinned author file:

```sh
curl -fL https://raw.githubusercontent.com/krittisharma/dmz_spk_sharma2026/6651975039b25c2ac6853527699bb6d54722f5a0/data/frb_results/frb_sample.csv -o /tmp/frb_sample.csv
python3 real_research/sol_data_search/frb_sample_audit.py /tmp/frb_sample.csv
```

This is a **selection audit**, not a re-fit of FRB likelihoods or proof that 22 localizations are wrong. Its immediate mathematical value is to define the two specific posterior products that must be compared when using FRBs to break the baryonic-feedback versus modified-gravity degeneracy in lensing.
