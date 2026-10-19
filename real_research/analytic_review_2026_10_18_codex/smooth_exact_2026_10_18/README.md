# Exact smooth finite halo with radial dispersion

18 October 2026. Checkpoint ZAR-2026-10-18-04, continuing [the warm halo checkpoint](../warm_radial_2026_10_18/README.md) from Git baseline `3c01aa2861bf576f4c2d942251eb9d2f89cae108`.

**The circular-orbit pileup can be removed while keeping the exact original density profile.** For the fixed hollow target and its stated core condition, an analytic construction gives bounded nonnegative smooth distributions with genuine radial dispersion, the same finite boundary, and the same coupled gravitational forces. Their radial accessible linear evolution has the conserved positive energy bound and now admits classical smooth solutions and ordinary L1 perturbation control.

| Requirement | Result |
|---|---|
| Both population densities and enclosed masses | Exactly the original profiles, including the constant fraction |
| Law annulus, amplitude and circular-speed curve | Exactly preserved within the same spherical deep-cubic model |
| Inner and outer boundaries and exterior matching | Exactly preserved; no wall, escaped tail or surface layer |
| Distribution | Bounded nonnegative C-infinity function of compact support; no circular ridge |
| Energy monotonicity | F_E < 0 wherever the physical distribution is positive |
| Radial dispersion | Positive throughout the interior and uniformly positive on the closed law annulus; cools to zero at the edges |
| Stability | Uniform linear accessible radial energy bound, ordinary L1 control and classical evolution for smooth initial data |
| Stronger dynamics | Uniform Ck, nonlinear and nonspherical stability remain open |

The mechanism is a broad positive warm component plus a smaller density correction. Each Fourier component of the correction uses an appropriate narrow family of eccentric orbits. Its amplitude and first energy derivative are both small enough to preserve positivity and monotonicity of the total distribution. An explicit weighted inverse makes the density match exact. The target's exponential taper controls every derivative at the finite boundaries.

This is an analytic existence theorem at each fixed sufficiently small positive width. No finite orbit library, numerical fit, simulation or limiting physical calculation was run. There is no bound uniform as the width tends to zero; the circular cold limit remains singular. The construction selects a family of allowed temperatures, without deriving a measured or preferred temperature.

Preserving the law means preserving density, acceleration and circular speed. Dark velocity moments still obey the pressure correction on the law annulus, <v_perp^2> = v_c^2 + r d(sigma_r^2)/dr. The proof retains the previous positive point baryon mass, 0 < f < 1, strong core condition, smooth exponential taper, deep-cubic response and separate populations. It is not a full interpolating or nonspherical theory.

[EXACT_SMOOTH_INVERSE.md](EXACT_SMOOTH_INVERSE.md) proves the density inverse, positivity, smoothness, confinement and radial width. [CLASSICAL_RADIAL_STABILITY.md](CLASSICAL_RADIAL_STABILITY.md) gives the stability and classical-flow statement. [AUDIT_AND_ROUTES.md](AUDIT_AND_ROUTES.md) records the checked implications, route outcomes and remaining scope; [CHECKPOINT.json](CHECKPOINT.json) pins the inputs and artifact revisions.

Only this new checkpoint directory was written. Existing research files and Claude's calculations were left untouched. No scientific scripts or heavy computations were executed. No claim of global mathematical novelty, empirical success, parameter selection or a completed physical theory is made.
