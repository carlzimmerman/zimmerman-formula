# CFG38 — the massive passive regime: SLUGGS globular clusters under B's derived cold-mass rule

Script: `CFG38_sluggs_massive_passive.py`, about 4 s.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. Collapse masses are divided by 100, so the rule becomes the law, and H1 fails (rc = 1).
- The main run passes 4 of 4 and exits 0.

## Question

CFG35 derived the conservation rule from T4. CFG36 fed it measured colour-split collapse masses (Mandelbaum+2016). With those:
- the rule leaves every star-forming spiral on the law;
- it leaves passive disks below log M_* ≈ 11.2 on the law (CFG37);
- it adds collapse debris only above that, on the red sequence.

h50 measured globular-cluster dispersion profiles of 19 SLUGGS early types out to 5–15 R_eff. It found the law low by about 20%, worst in the most massive. That is exactly the regime the rule claims.

## Method (declared before the first run)

- **Machinery:** h50's data, bins and isotropic Jeans machinery (γ = 3 tracer, Hernquist stars, outer bins), exec'd read-only.
- **Rule:** CFG36's red collapse masses and CFG35's conservation form at x_e = 0.40: g = G[ν M_b + f_ex (1 − f_b) M_NFW]/r².
- **Offset:** h50's (the outer-bin mean of log σ_obs/σ_pred). Hot gas is omitted, as in h50.

## Results

**C1 (control):** h50's per-galaxy law offsets are reproduced exactly.

| | canonical | alt | verdict |
|---|---|---|---|
| the law (h50) | +0.080 ± 0.024 (3.3σ) | +0.065 (2.7σ) | |
| **the rule, red collapse masses** | **+0.007 ± 0.017 (0.4σ)** | **+0.002 (0.1σ)** | **H1 PASS** |
| mass trend d(offset)/d log M_* | rule −0.048 ± 0.040 (−1.2σ); law +0.139 ± 0.075 (+1.8σ) | | H2 pass (weak bite: the law is also below 2σ) |

**Where the rule adds mass (10 of 19, all log M_* ≥ 11.2).**

| galaxy | law | rule |
|---|---|---|
| M87 | +0.28 | +0.08 |
| NGC 4374 | +0.21 | +0.02 |
| NGC 5846 | +0.21 | +0.03 |
| NGC 4365 | +0.17 | −0.01 |
| NGC 1407 | +0.16 | −0.09 |
| NGC 4649 | +0.14 | −0.04 |
| NGC 3607 | −0.01 | −0.11 (over-predicted) |

Below log M_* 11.2 the rule equals the law.

**Reported.**
- h50's colour-blind abundance-matched NFW gives −0.110 ± 0.021.
- The blue relation leaves the law's +0.080.
- **Post-hoc (added after the main run):** ΛCDM on the *same* measured red collapse masses (stars plus the full halo, no phantom) gives −0.037 ± 0.017 (−2.1σ).

## Standing

**B's derived conservation rule, fed measured weak-lensing collapse masses and nothing fitted, fits the SLUGGS massive early types (0.4σ).** It removes the law's 3.3σ deficit where the law needs help, and it leaves alone every system where the law already works:
- star-forming spirals (CFG36);
- passive disks below log M_* 11.2 (CFG37);
- the less massive SLUGGS galaxies (here).

Together with the X-ray ellipticals (half-closed, CFG36), this is the first rule in the campaign that treats spirals and massive ellipticals together without breaking either.

**What is still open:**
- UGC 2487 (one massive S0 in SPARC) disagrees at +0.14 dex.
- Groups and clusters cannot be scored non-circularly with the data in the repository.
- The rule inherits the SHMR's systematics: stellar-mass conventions and centrals versus satellites (M87 is a cluster central; NGC 4374, 4365 and 4649 are Virgo members).

Per the standing rule, **this does not say the data favour the framework over ΛCDM.** ΛCDM with the same halos is within about 2σ, and it carries its own modelling freedom (adiabatic contraction, anisotropy, IMF). Nothing here says the theory is closed.
