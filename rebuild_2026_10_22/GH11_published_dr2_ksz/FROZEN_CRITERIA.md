# GH11_published_dr2_ksz: FROZEN CRITERIA (committed alone, before opening the paper)

**Question.** Is Zhang's gas continuing to about 1.8 R_vir (route E's need on KiDS lensing, GH2) compatible with the published DESI DR2 × ACT DR6 BGS kSZ measurement at MW stellar mass (arXiv:2604.19745)? Their S/N is well above GH8's, with no pipeline of ours. No part of the paper has been read past a search summary.

**Inputs from the paper: raw measurements only.**
- The stacked kSZ CAP profile T̂(θ) with errors, covariance if published, in the stellar-mass bin(s) overlapping Zhang's log M★ 10.5–11, plus the bin's z, median mass, beam and aperture definition.
- Their velocity correction as they report it, which is needed to read T̂ at all. Disclosed as inherited: it rests on their fiducial cosmology.
- **Not used:** their gas fractions, fitted profiles, halo masses or any ΛCDM-simulation interpretation. Those may be quoted as context, labelled, never graded.

**Order of data preference.** Published machine-readable tables, then tables printed in the paper. Figure digitisation only if neither exists, then labelled DIGITISED and class capped at INDICATIVE.

**Template.** GH7's code read-only: Zhang's β 0.43, r_c 6 kpc, 1.84 M★ in R_vir, μ_e 1.14, cut at k 1, 1.8, 3, plus GH10's F1 and F2 tapers. Beam, θ grid and CAP definition set to the paper's. Evaluated on GH7's native background.

**Mass scale, both reported.**
- **As published:** their stellar mass taken at face value.
- **GH9 shift:** only if they use the same CIGALE masses; otherwise stated as unknown.
The class at k 1.8 is read at each; a class that differs is MASS-LIMITED, not a result.

**Grade.** A = best-fit amplitude using their covariance (diagonal if none, then disclosed and class capped at INDICATIVE). Primary sharp k 1.8.
- **BELOW NEED:** A + 2σ < 1 at sharp k 1.8, F1 and F2, at Zhang's mass in R_vir and at same total mass.
- **ABOVE NEED:** A − 2σ > 1 for those same templates.
- **MEETS NEED:** |A − 1| ≤ 2σ with A/σ ≥ 3 for those same templates.
- **FORM-DEPENDENT:** templates disagree.
- **NOT COMPARABLE:** no bin overlapping 10.5–11, or T̂ cannot be put in template units.
A/σ < 3 is also labelled NO DETECTION at that template.

**Also reported.** χ² at best A per template and vs null. Whether a two-halo term is removed in their T̂; if it isn't, it adds to the signal, so a low A is firmer and a high A weaker. Comparison with GH8's A.

**Checks.**
- **K1:** template harness at GH8's settings reproduces GH9's D1 sharp model table for one cell to 1e-6.
- **K2:** every extracted number traced to a table or equation in the source, listed in the README; rechecked by a second independent read of those lines.
- **K3:** units test: a template in the paper's units reproduces any stated CAP conversion or stated expected amplitude, if the paper gives one; else stated as unavailable.
- **MUTATE:** doubling the template halves A; shuffled T̂ angle order is reported.

**Limits stated up front.** Not our pipeline, so nothing here hardens GH8 and it does not reopen DR1. Stellar-mass and centrals selection will differ from Zhang's. Their velocity correction and cosmology are inherited. A result is about this one column; it does not retire any route or make the law win.

κ = ½ FITTED; c_f EXTERNAL. Footings are not at issue in this column and are not pooled. Not theory closed. Nothing here says the data favour the framework. Cold dark energy is a gravitating field component, never a particle.
