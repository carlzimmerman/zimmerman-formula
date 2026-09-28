# CFG37 — the passive-disk test of B's derived cold-mass rule

Script: `CFG37_passive_disks.py`, about 4 s.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. Collapse masses are divided by 100, and H2 fails.
- The main run exits 1 because H2 failed. In this lane the MUTATE control is uninformative, because the main run fails H2 too (see below).

## Data

den Heijer+2015 (A&A 581, A98, Table 1) is now transcribed to `real_research/data/denheijer2015_etg_hi_tfr.tsv`. It was fetched with the owner's approval from the arXiv source (378 kB). It gives the HI circular velocity at the outermost point of the rotation curve for 16 ATLAS3D early-type galaxies, at 8–28 kpc (3.4–13.7 R_eff).

## Method

CFG36's machinery is exec'd read-only (Mandelbaum's red collapse masses, the conservation form, x_e = 0.40).
- Stars: L_r × (M/L)_SFH, plus 1.33 M_HI.
- Radius: 15 kpc (the sample mean), bracketed by 8 and 28 kpc.
- Floor: the galaxy-to-galaxy error, the IMF (Salpeter vs Chabrier) and the radius.

## Results

- **C1 (control):** the table checks out (16 galaxies; NGC 3941 at i = 57°, v = 148 km/s).
- **H1 passed: the law fits the passive disks.** log(v_obs/v_law) = **+0.026 ± 0.085 (0.3σ)** canonical, +0.011 (0.1σ) alt. The dynamical (JAM) M/L gives the same (+0.027).
- **H2 failed: the rule adds nothing to these galaxies.** Their stellar masses are 10^10.3–10^10.9. The red collapse masses (1.6–4.2 × 10¹²) are fully consumed by the law's phantom, so f_ex = 0 in all 16 and the rule's prediction equals the law's. There is no extra mass for the data to reject.

## Standing

**The law passes an independent test.** Early-type galaxies with extended HI discs follow B's galaxy law to 3–14 effective radii, as the star-forming spirals do.

**The derived conservation rule is untested here.** It adds mass only above log M_* ≈ 11.2 on the red sequence, where there are:
- one SPARC S0 (UGC 2487), which rejects it at +0.14 dex;
- the X-ray ellipticals, which want about half of it (CFG36).

Deciding it needs massive passive disks (log M_* > 11.2) with extended HI or tracer kinematics. That sample is rare, and none is in the repository.

Nothing here says the theory is closed.
