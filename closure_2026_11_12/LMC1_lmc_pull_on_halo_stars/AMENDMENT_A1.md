# LMC1 AMENDMENT A1 (2026-11-12, written before the re-run)

## What happened

Run 1 (`lmc1_run1_K6_FAIL.out`) stopped at the bracket check K6, before any simulation and before any star
was read. Route (ii), the kernel applied to the LMC's baryons at the strength of the Milky Way's baryonic
field at the LMC (r_GC 49.08 kpc, g_b 3.85e-12 m/s^2), gives nu = 5.4505 on canonical and 5.9363 on alt.
With the frozen variant baryon mass 3.0e9 on canonical this is M_eff = 1.635e10, below the frozen floor
1.7e10 x 0.99 = 1.683e10. Every other route lands inside: (i) 1.70e10 measured, upper end 2.54e10 / 2.33e10
(Jacobi variant 3.49e10 / 3.35e10); (ii) at 3.2e9: 1.74e10 / 1.90e10; (iii) 1.74e10 / 1.89e10.

## Why the change

The brief's rule: if a route lands outside the bracket, stop and write an amendment. The route numbers say the
framework's own LMC sits at the LOW end of the frozen bracket (three routes at 1.6e10 to 1.9e10) and the
measured rotation curve sets the floor at 1.70e10. The variant point 1.635e10 is 4 per cent below it. The
bracket is widened downward, not moved: a wider bracket can only make the label more fragile, not less.

## Changes (nothing else changes)

A1.1 The low end of the M_eff bracket is 1.6e10 Msun (was 1.7e10). Central 2.5e10 and high 4e10 unchanged.
     FRAGILE is now tested at 1.6e10 and 4e10.
A1.2 K6 window: every route number must lie in [1.6e10 x 0.99, 4e10 x 1.01].
A1.3 Disclosed reading of the routes: the central 2.5e10 is the upper end of route (i)'s equal-field
     continuation; routes (ii) and (iii) both sit near 1.7e10 to 1.9e10. The low end is therefore the
     framework's most direct estimate, and the result at 1.6e10 is reported beside the central label.

The failed output is kept. The script change is the bracket constant only (`MASSES["low"]` and the K6 window).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
