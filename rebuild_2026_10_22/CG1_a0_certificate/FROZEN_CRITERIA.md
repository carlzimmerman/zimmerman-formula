# CG1_a0_certificate: frozen criteria

Written and committed alone, before any script or number of this lane. kappa = 1/2 FITTED. Not theory closed. The cold sector stays retired and nothing here reinstates it. Footings canonical 9.3603e-11, alt 1.1312e-10 m/s^2, both reported, never pooled.

**Not blind.** Already read: BK1 README and its numbers (a0 5.5 bits with the mismatch corrected at 5 %, 0 local, about 6 span, 92 % of shallow trees decompose); `project_atomos` gate, `calibrate.py`, ENGINE_REVERSE_ENGINEERING, GATE_SPEC; the FDR scripts it names; `real_research/reviews/mi_a0_profile_likelihood_milgrom_footing_2026.{py,out}` (best a0 1.0766e-10 on the framework kernel, Dchi2 63.90 at canonical, 5.34 at cH0/2pi, 7.04 at alt); the kappa ledger's menu (2pi, 6 land in its window at about the expected rate). Hand expectation: a0's row stops being CERTIFIED; the new kernel test gives few bits, because at 5 % precision a small registry covers the O(1) band.

## Part A. The gate
Corrected copy in `gate/`, `project_atomos` untouched. Repairs, each stated in the patch:
- **A1** structural-null target separate from the coefficient: a0's null is compared with a0, in acceleration units. Kernel value stays in gate B.
- **A2** scale guard: target outside the null's support fails gate A as NULL-SCALE-MISMATCH. Never infinite bits.
- **A3** P = 0 of N is reported as P < 3/N, finite bits, never inf.
- **A4** gate A requires the relation to land in the window. It did not check this.
- **A5** gate B's coefficient test accepted any implied free number in 0.05-20, so nearly every scalar. Replaced with: implied free number must be p/q, p, q <= 4.
- **A6** comparative route: arithmetic kept as in the lineage (`koide_fdr_sqrt2.py`), but docstring and tell say the opposite of the arithmetic, so wording is corrected. Printed values show which it is.
- **A7** gate B's places and gate C's counts are declarations, not checks. Not repairable here. Each verdict prints DECLARED, NOT VERIFIED.

Runs: **R0** original gate, must reproduce 8/8 and a0 bits inf. **R1** A1 only, the minimal repair. **R2** all repairs, a0 once per footing at the suite's target 1.2e-10 tolerance 5 %.

**Same bar matrix.** Every row through a0's null (free factor log-uniform +- 1 dex about its relation, at the row's own tolerance); a0's kernel through the negatives' germ-pool route at 5 %; the negatives at their actual closeness rather than tolerance 1e-3; Koide's null over mass ranges of [-2,4], [-3,5], [-1,3.5] decades. Bits are as computed, no multiplier unless stated.

**Separation labels, frozen.** `SEPARATES`: on R2 a0 CERTIFIED, Koide REAL-PUZZLE-RE-LABELED, all negatives dead, and no negative reaches a0's bits in the same-bar matrix. `SEPARATES KOIDE ONLY`: Koide holds, a0 not certified or negatives match or beat a0 under a0's null. `DOES NOT SEPARATE`: otherwise. I do not edit the required statuses in the suite to get a PASS; if a0's row fails, that is reported as failed.

## Part B. The kernel test
Scalar: x = a0 / (c R), R the rate. R is read from the footings: R_alt = Z 1.1312e-10 / c, R_can = Z 9.3603e-11 / c, Z = sqrt(32 pi / 3). No other cosmological input.

**Registry, six places, frozen:** Einstein 8pi (E), FRW 3 (F), Unruh / Gibbons-Hawking 2pi (U), Gauss / Poisson 4pi (P), sphere volume 4pi/3 (V), area law 4 (A).
A member is kappa x product of place^e. Classes:
- **T**, a0's own: exactly 2 distinct places, each |e| = 1/2, kappa in {1, 2, 1/2}. a0 is 1/2 x E^-1/2 x F^1/2.
- **S**, one place: |e| in {1/2, 1}, kappa in {1, 2, 1/2}.
- **W**: 2 places, |e| in {1/2, 1}, kappa p/q with p, q <= 4.

**Scrambled scalars.** x log-uniform over +- 1 dex about 1/Z (also +- 0.5 dex), 2e6 draws, seed fixed, same fractional window. P(w) = fraction with a member of the class in the window. Also exact interval coverage as a check. Bits = -log2 P if the real formula is inside the window, else 0, and "no hit" is printed. Per footing, never pooled.
**Scrambled registry.** Six places replaced with log-uniform [2, 30], 20000 draws, real window: fraction with a class T member in it.
**Strict reading.** Friedmann is the 00 component of Einstein on FRW, and its 8pi is Einstein's. If E, F is not two independent places, a0 is not in T. Reported as a second row, T minus the pair (E, F).
**Power.** The w at which P(w) = 2^-10 per class; bits a true formula gets at each real window.

**Windows.** W1 +- 2 sigma_boot about the best a0 (framework kernel). W2 envelope of the three kernels' 2 sigma_boot ranges. W3 1.2e-10 +- 40 % (McGaugh+16 systematic 20 %, recalled, PROVISIONAL). W4 +- 5 %, the suite's.

## Part C. SPARC likelihood
`real_research/data/sparc_data`, procedure of the record's script: Upsilon free per galaxy on its grid, bulge 1.4 x, sig_int calibrated to chi2/dof = 1 at its a0. Vectorised. Reference kernel g_obs^2 = g_bar^2 + g_bar a0 (framework's own). Sensitivity kernels: McGaugh ν, simple ν. A wrong kernel moves a0, so a0's value here is conditional on kernel.
Errors: Dchi2 = 1 points-independent; record's sqrt(N/n) clustered; **bootstrap over galaxies**, 2000 resamples, seed fixed, sigma_boot, the one used for windows.

**Rivals, a0 = c R / N, each on both rates:** N = Z (framework); 2pi (Milgrom cH0/2pi on R_alt; Milgrom 1999 c^2 sqrt(Lambda/3)/2pi on R_can); 6 (Verlinde 2017); 8/sqrt3 (the search's sibling c^2 sqrt(Lambda)/8); 4pi. Attributions from the record, formulas recalled where it is silent, PROVISIONAL. Excluded, because they need an LCDM background: particle horizon and van Putten's q form.

**Net bits.** Bits_i = log2[ L_i / integral L p(ln x) ], L from Dchi2/(N/n), p log-uniform +- 1 dex; Penalty_i = log2(distinct members of the smallest class holding it); Net = Bits - Penalty. Also rank of each among all members of S union W by Dchi2.

**Verdict labels, frozen.** `STANDS OUT`: Z inside W1 on both footings, best Net among rivals on both, and class T bits >= 10 on W1. `FITS ON ONE FOOTING, NOT SPECIAL`: inside W1 on just one footing, or inside on both without the rest. `DOES NOT FIT`: outside W1 on both.
These grade the coefficient's specialness only. They don't grade the law's shape, and kappa stays FITTED whichever comes out.

## Part D. Citations
List committed files or papers citing the certificate (calibration verdict, CERTIFIED a0, "forced kernel" as evidence, atomos gate). No edits. Classified by whether they rest on gate A.

## Checks
K1 reproduce record: sig_int 0.0808, Dchi2 63.90 at 9.3614e-11, 5.34 at cH0/2pi (+- 0.3). K2 R0 reproduces 8/8, bits inf. K3 Monte Carlo P within 4 sigma of exact coverage. K4 PLANT: synthetic SPARC with a0 = alt footing and Gaussian sig_int recovers it within 2 sigma_boot. K5 a0 member exactly in class T on real registry. K6 RSS < 4 GB, one thread.
**MUTATE** (`--mutate`): gate A with the mismatch restored behind A2 must trip the guard; registry E = 7pi must lose a0 from T (K5 fails); a0 grid x 1.25 must fail K1. Exit nonzero expected. Separate outputs named `_MUTATE`.
Rerun byte-identical. Any failure published under these labels.
