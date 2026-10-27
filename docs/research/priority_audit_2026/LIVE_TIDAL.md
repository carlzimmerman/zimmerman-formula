# Live narrow results: tidal identity and compact pairs

Audit date: September 9, 2026. This is a literature/provenance check, not a fresh full proof or physics-suite rerun. **No exact external duplicate was identified in the bounded search. These remain candidates for narrow original calculations, not established globally novel laws.** Their static assumptions survive the later references inspected; their empirical validity and relativistic completion remain open.

## Exact claims and dates

Write `s_e=y(1-exp(-y))`, `lambda=1+(y-1)exp(-y)`, where `s_e` is the filtered Newtonian background divided by `a0`, not automatically the measured physical acceleration.

1. **Central tidal identity:** `Q2/D=2y/[5(3lambda-y)]`, with `Q2=H_perp-H_parallel`, `D=tr(H)`, and `H` the additional potential's central Hessian. The division-free version is `(15A+5B)Q2+2BD=0`, `A=nu-1`, `B=s_e nu'`. It is filter-amplitude/mass independent for a spherical perturbing source, isotropic convergent regularization, constant nonzero background and linear constitutive response. It is not an exact nonlinear Solar-System identity. At `D=0`, use the division-free equation.

   Earliest committed exact formula located: **`3466d9d229c7cf2172e14859bc4cf02dd14d094a`**, author=committer **2026-09-04T21:54:29-04:00**, `qwen_claude_field_theory/closure_2026/g02b_tidal_identity_crosscheck.py`. The full derivation package `filtered_tidal_relation_2026/` first enters **`d21a0db774a5eb39569296df6a7e2138256dc1f6`**, author=committer **2026-09-05T07:12:14-04:00**; its report internally dates the calculation September 4.

2. **Orbital translation:** `(omega_r^2-omega_phi^2)/(omega_phi^2-omega_z^2)=3(5lambda-y)/(2y)`. This is the same tidal result translated through standard epicyclic derivatives, not an independent theoretical discovery. It additionally requires a small harmonic-core circular orbit perpendicular to the fixed background, infinitesimal oscillations and positive frequency squares. First located in **`d21a0db774a5eb39569296df6a7e2138256dc1f6`**, same timestamp, `two_body_frequency_2026/REPORT.md` and `binary_frequency.py`.

3. **Isolated Gaussian compact-pair coefficient:** `r_ddot=-GM r/r^3-h(M)r+...`, `h(M)~(2/9)sqrt(GMa0)/xi^2`, `M=m1+m2`. Both source positions are varied; the leading relative coefficient is mass-ratio independent at fixed positive mass fractions. This requires `GM/(a0 xi^2)->0` and `r/xi->0`, separately from external-field dominance. The comparable-mass derivation first enters **`d21a0db774a5eb39569296df6a7e2138256dc1f6`**. Its parent one-source `2/9` coefficient and `r_eq^6~(81/4)GM xi^4/a0` occur in **`4fed8bfa6d4bd9e1c7199bc2d686bd7679ce4944`**, author=committer **2026-09-04T20:58:02-04:00**, `smoothed_onset_action_2026/REPORT.md`. These leading deep-MOND coefficients are not unique fingerprints of the exponential interpolation function.

## What survives later checks

The two reports retain the conditional static results. Later G03 review explicitly restricts G02b's nonlinear numerical agreement to approximately 1.43%/0.58%; it is not a nonlinear theorem. The Gaussian C-H completion later encounters nonuniform/singular quadratic-lift and causal-response obstructions. September 9's lapse-variation obstruction concerns the separate rotated-MMG action. None of these inspected texts derives a contradiction of the specified static tidal or compact-pair asymptote. Conversely, their survival does not clear metric coupling, causal propagation, realistic environmental corrections, measurability or observational tests. No claimed PASS count was used as proof here.

## Prior-art comparison and search limits

[Banik–Zhao, v2, equation 24](https://arxiv.org/pdf/1509.08457v2) supplies the unfiltered external-field operator: their `nu_ext K0` is this report's `B`; subtracting Newtonian gravity gives `A`. The central filtered ratio is a formal corollary of this operator plus isotropic angular averages. The inspected passage does not state the regularized central identity.

[Zhao–Li–Bienayme, v2, equation 13](https://arxiv.org/html/1007.1278v2) gives a different mass-ratio-dependent inverse-distance anomalous force; [Milgrom 2012, equation 13](https://arxiv.org/pdf/1205.1317v3) gives a separation-cubed anomaly, not this Gaussian harmonic coefficient. [Pflamm-Altenburg 2025](https://arxiv.org/html/2509.01493v1) treats complete unfiltered QUMOND binaries, not this added-scale compact limit. General nonlocal-QUMOND architecture is already permitted by [Milgrom 2023, section II.2](https://arxiv.org/html/2305.01589v2).

English searches included `QUMOND central tidal ratio filtering`, `MOND three-frequency squared-frequency relation`, `MOND Gaussian two body 2/9`, and date-bounded March 9–September 9 variants for tidal smoothing, epicyclic/vertical ratios and Gaussian harmonic forces. Search results and the primary passages above yielded no exact match; this does not establish absence across the literature.

The repository associates these results with [Zenodo 22347632](https://doi.org/10.5281/zenodo.22347632), dated September 5 in its index. Independent server timestamps/deposited contents were not authenticated here. Git dates alone do not establish public priority; see [PROVENANCE.md](PROVENANCE.md).
