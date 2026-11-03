# KT16_filtered_phantom_cassini: FROZEN CRITERIA, committed alone before any script or number

Owner, 2026-11-03: "keep pushing". KT14/KT15's filtered QUMOND (phantom sourced by rho smoothed over xi): universal xi = 2 kpc passes the Milky Way on alt but is HURT by dwarfs; scaled xi = 0.2154 r_M passes both. Owed next: Cassini. κ = 1/2 FITTED and held fixed. Both footings, never pooled. Not theory closed. No download.

**Not blind.** By hand (KT15 README): inside xi the Sun's smoothed field is linear and below the Galaxy's, so the quadrupole scales about as (r_M/xi)^3. **I expect the scaled arm to FAIL by roughly 100x, and universal 2 kpc to pass trivially.**

## Integral
Sun as a point mass smoothed by a 3D Gaussian: gh(r) = (G M / r^2) [erf(r / (sqrt2 xi)) - sqrt(2/pi) (r/xi) exp(-r^2 / 2 xi^2)]. External field g_e along z. Simple nu (board law). In units G M = a0 = 1 (r_M = 1, eta = g_e / a0):
q = 1.5 * integral_0^inf dr / r^2 * integral_-1^1 dmu A(r, mu) [eta (3 mu - 5 mu^3) + gh (1 - 3 mu^2)], A = nu(sqrt(eta^2 + gh^2 + 2 eta gh mu)) - 1,
the same integral as KT5/KT7's `q()` with v = 1/r and gh = 1/r^2 when xi = 0 (derived from Phi_ph,zz(0) by parts). Q2 = q * 1.5 a0 / r_M; ceiling 5.2e-27 s^-2; g_e = 2.32e-10 m/s^2 as in KT7.

## Arms
xi/r_M,sun in: 0 (plain); 0.2154 (KT15's A2 eps); universal 2 kpc, i.e. 2 kpc / r_M,sun; plus the threshold: the smallest xi/r_M passing the ceiling, by bisection, per footing (reported, not a fit to data).

## Labels, per footing
- **SCALED FILTER PASSES CASSINI / FAILS CASSINI (x times ceiling)** for eps = 0.2154.
- **UNIVERSAL 2 kpc PASSES / FAILS.**
- **THRESHOLD:** xi/r_M needed, and what eps that implies against the Milky Way's 0.2154.

## Checks
C1: xi = 0 with simple nu reproduces KT7's `q()` (dblquad) at the same eta on both footings, relative 1e-3. C2: gh -> G M / r^2 for r >> xi and -> 0.2660 G M r / xi^3 for r << xi, 1e-6. C3: converged in r and mu resolution (doubling each moves q by under 1e-3 relative). MUTATE: nu = 1 must give q = 0; separate output, exit 1.

Register row after the result. Seconds.
