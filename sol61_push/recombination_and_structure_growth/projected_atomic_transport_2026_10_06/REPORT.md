# Atomic transport on the admitted projected-action background

Base c1449c08768f6ea7553ea0ecbc7c6653f4651bb8. This continues Claude-associated recombination/kernel work through the already derived full homogeneous projected-action branch. It changes the expansion source, rather than imposing another ad hoc percent change in H. It does not establish a cold component or close 32pi.

## Mathematical dictionary

The parent FRW derivation admits own-metric conserved ordinary matter with constant Q and interaction stress exactly a cosmological constant. In n=3, Q=chi=1, the visible branch therefore has

H(z)^2=H100^2[omega_r(1+z)^4+(omega_b+omega_c)(1+z)^3+omega_lambda].

The actual baryon-only model sets omega_c=0. A declared ordinary cold-matter reference sets omega_c=.1200. Both keep omega_b=.02237, massless Neff=3.046, T0=2.7255 K, Yp=.245 and the SAME omega_lambda=.3113251256005444. Consequently H0 changes; holding H0 fixed instead would insert a different vacuum. The second metric admits the empty-sector reconstruction given in the parent report; no extra homogeneous dust is supplied by the interaction.

Hydrogen density is nH(z)=(1-Yp)3H100^2 omega_b(1+z)^3/(8pi G mH), independent of the gravitational cold reference. Atomic rates are the identical hydrogen three-level functions ported from the cached Peebles/Seager laboratory, including separate matter/radiation temperatures, detailed-balance photoionization, Ly-alpha escape and the two-photon channel. Only nH, saha and solve were extracted from the earlier script; its top-level experiment is never imported or executed. Exact source hashes are in provenance.json, and its sources.json identifies authenticated primary copies. This is an effective hydrogen model with helium mass bookkeeping but no helium electron history, multilevel corrections, reionization, or CMB likelihood.

For the peak scale factor a*, the sound horizon is

r_s(a*)=c/H100 integral_0^a* da/[sqrt(3(1+Rb0 a)) sqrt(omega_r+omega_m a+omega_lambda a^4)],

Rb0=3 rho_b0 c^2/(4 a_rad T0^4). This has a finite radiation limit at a=0. It is a background acoustic scale, not a calculated temperature power spectrum. Visibility integrates optical depth only above z=50; the no-reionization omitted residual upper bound is reported per run. A bounded 0.25 redshift grid determines the peak, not a continuum-precision peak certificate.

## Decisive separation

The main bounded runs give the cold reference half ionization z=1272.680, visibility peak z=1089.0, sound horizon 144.521 Mpc; the admitted baryon-only branch gives 1290.622, 1078.5 and 196.787 Mpc. Residual x_e(z=200) is respectively .000377210 and .000195183. Neutralization therefore survives removal of ordinary cold matter in this laboratory, while the sound horizon increases by about 36.2 percent. This cannot substitute for an actual cold gravitational source or structure-growth transfer calculation. No observational exclusion is inferred from these toy values alone.

At fixed Q, Lambda=chi A a0^2/(2c^4). The exact local expansion derivative is

d ln H/d ln A = (1/2) omega_lambda/[omega_r(1+z)^4+omega_b(1+z)^3+omega_lambda].

Its maximum on z in [800,1500] is 5.421e-9. Monotonicity makes the z=800 endpoint the exact interval maximum for positive densities. This is an expansion sensitivity bound, not a theorem bounding every possible new atomic interaction. Doubling the declared vacuum changes the computed ionization history by less than 4e-10 here; tightening ODE tolerance changes it by less than 2e-9. Recombination's expansion clock has negligible leverage to select a vacuum coefficient of order 32pi.

For declared a0=9.3603e-11 m/s^2 and this empirical reference vacuum, one can infer A=201.2455, close to 64pi=201.0619. That is a re-expression of independently inserted cosmological parameters and a0, NOT a selection equation, new coincidence discovery, or closure proof. The input vacuum remains a free parameter.

## Evidence and remaining implication

The script checks physical ionization, solver tolerance, background acoustic shift, exact vacuum sensitivity, and fixed hydrogen density. Controls substitute cold mass for hydrogen or retain the reference H after removing cold; they are intended to fail discriminating assertions. One failed preflight is preserved: the central finite difference used a step too small for a roughly 1e-9 derivative. Its cancellation was corrected by a larger log step and a declared absolute tolerance; the analytic derivative is unchanged. Standard fresh manifests, runtime caps and check outcomes are recorded in RUNS.md. Finite output is not a proof of general atom or perturbation dynamics.

The next necessary arrow is a regular admitted cold source plus its perturbative transfer through this same background, or an explicitly changed clock/matter action that supplies one. A successful chemical history does not establish that arrow. Claude's phenomenological cold readers and cutoff fits remain useful leads, but their reported growth gates cannot be inserted as this action's transfer function.
