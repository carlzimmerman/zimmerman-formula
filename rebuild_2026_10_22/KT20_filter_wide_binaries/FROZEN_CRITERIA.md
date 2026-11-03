# KT20_filter_wide_binaries: FROZEN CRITERIA, committed with KT18 and KT19's criteria, before any of their scripts or numbers

Owner, 2026-11-03: "run one after another". KT17's filter (xi = 0.55 sqrt(G M / a0)) makes a sharp wide-binary prediction. **This lane writes the prediction down; it grades nothing against Gaia.** κ = 1/2 FITTED, held fixed. Both footings, never pooled. Not theory closed. No download. The Gaia DR4 pre-registration is not touched.

**Not blind:** by hand xi is about 4,000-4,400 AU for a solar-mass pair (KT16's r_M at 0.55), so the boost should be suppressed below that separation and approach plain QUMOND well above it.

## Model
Binary of total mass M_tot in {1.0, 1.5} Msun, as a point mass smoothed by a 3D Gaussian of sigma xi (KT16's gh). External field g_e = 1.9e-10 m/s^2 (Galactic field at the Sun, about v_c^2 / R0) and also 2.32e-10 (KT16's value), both reported. Relative acceleration, spherical average, 1D external-field form: g = g_N + (nu(sqrt(g_e^2 + gh^2) / a0) - 1) gh. Output gamma = g / g_N at separations s in {1, 2, 3, 5, 7, 10, 15, 20, 30} kAU, for plain QUMOND (xi = 0) and the filter, and the ratio of their excess (gamma - 1).

## Reported (no label)
- gamma(s) for both models, footings and g_e values.
- s_half: the separation where the filter's excess reaches half the plain excess.
- One plain statement of what the filter predicts that plain QUMOND doesn't, in units a Gaia test could check (the excess at 2-5 kAU versus 10-20 kAU).

## Checks
C1: xi = 0 at large s reproduces nu(sqrt(g_e^2 + g_N^2) / a0) form, 1e-10. C2: the filter's gamma -> plain's for s >> xi (ratio of excess above 0.95 at 30 kAU, or reported if not). MUTATE: nu = 1 gives gamma = 1 everywhere.
