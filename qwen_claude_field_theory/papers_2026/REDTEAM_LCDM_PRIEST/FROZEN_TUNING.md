# Frozen before any tuning number: how far the knobs go

Hypothetical rival exercise, not a framework result, not a derivation. Every knob is disclosed. kappa = 1/2 FITTED; not theory closed.

**Question:** how close can LCDM-style knobs bring a disc population to the law at a0 = 9.3625e-11, and what does each step cost?

**Population:** deterministic discs at 8 halo masses, log M200 10 to 12.7, on the base cosmology of `lib.py`. No scatter.

**Targets**
- T1 level: stack-fitted a within 1 % of a0.
- T2 mass independence: per-mass fitted a spread at most 0.05 dex.
- T3 shape: rms of log g_total minus log g_law, at 0.5 to 5 R_d, at most 0.02 dex.
- T4 slope: d ln a / d ln rho_DE = 0.50 +- 0.05, at fixed omega_m, omega_b, A_s.
- T5 constancy: implied kappa within 5 % of 0.5 at (OL, H0) = (0.70, 67.4), (0.685, 73), (0.65, 73).
- T6 redshift: a(z)/a(z=0) inside the law's band at z = 1, 1.5, 2.33: [0.76, 1.03], [0.71, 1.12], [0.33, 1.21].

**Tiers**
- Tier 1, plausible ranges (my judgement, not from a cited compilation): c(M) norm +-0.11 dex, c(M) slope +-0.05; SHMR norm +-0.18 dex, log M1 +-0.3, beta +-0.4, gamma +-0.2; contraction fraction 0 to 1; disc size norm +-0.2 dex, size mass slope +-0.2; gas norm +-0.3 dex, gas slope +-0.2. Eleven knobs in all.
- Tier 2, the same knobs with ranges tripled, contraction -1 to 1 (negative means expansion).
- Tier 3, Tier 2's best plus c multiplied by (rho_DE / rho_DE0)^p, p solved for T4. Then a separate c shift per cosmology and per redshift, solved for T5 and T6.
- Tier 4, free-form halo: M_DM(r) = r^2 (g_law - g_bar) / G for each galaxy. T1 to T3 hold by construction. Report the positive-density check and the departure from NFW.

**AMENDMENT A1, after the first run's numbers, disclosed as such.** Tier 2's rms of 0.0000 looked degenerate. A1 prints the acceleration coverage of the tuned discs. It also reruns Tiers 1 to 3 with the fit range extended from 0.5 R_d out to where g_bar = 0.03 a0 (or 0.9 R200 if that comes first), so the tuner can't stay out of the low-acceleration regime the law is about. The first run stays on record in `tune.out`. The rerun is `tune_A1.out`. Targets and knob ranges are unchanged.

**Reported whichever way it lands:** pass or fail per target, knob values, knobs at their bounds. A pass at Tier 3 or 4 is a statement about how much freedom there is. It is not evidence for or against the law or LCDM.
