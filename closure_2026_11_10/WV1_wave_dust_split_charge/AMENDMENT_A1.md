# WV1 AMENDMENT A1 (post hoc): KA4(ii)'s observable

Committed alone. **Post hoc**: written after a development run of `wv1_ka.py` showed KA4(ii) FAIL as frozen, and after a
diagnostic run (scratch, not graded) of the check below. No threshold of any graded item changes; no S3 production run
had been started.

## What failed, as frozen

KA4(ii) froze: "this lane's SP solver at nu = 0.2 kpc km/s on a central domain of 100 comoving kpc, run to 0.12 Gyr after
z = 10, puts its central density maximum within 5 % of COL1's focus time at log M_b 10.7 (0.0712 Gyr)". The development
run put the maximum at the end of the run (0.118 Gyr, +66 %). The central density rises steeply through 0.071-0.075 Gyr
(1.7e3 to 2.9e4 times the mean) and then keeps rising, because shells from outside the softening core keep arriving
after the inner shells focus. So the global maximum over the run is not the focusing event. The criterion was wrong;
**KA4(ii) as frozen is recorded as FAIL** and RESULT.md reports the labels both as frozen and under this amendment.

## Replacement (A1)

KA4(ii') the SP solution's Lagrangian radius r_L(t) = a(t) x_L(t), with x_L defined by Psi's comoving mass inside x_L
equal to the mass initially inside comoving x0, must match COL1's test-shell equation (`col1_focus_check.py`'s right-hand
side, shell started at r0 = x0 / 11 in Hubble flow at z = 10) to within 5 % (the frozen KA's tolerance) at
t / t_f = 0.25, 0.5, 0.75 and 0.9, for x0 = 2, 5, 8, 15 and 30 comoving kpc, log M_b 10.7, nu = 0.2 kpc km/s, both
footings. t_f = COL1's focus time recomputed in KA4(i). This checks the solver's dynamics against COL1's before shell
crossing, which is what KA4(ii) was meant to check. MUTATE M5 is unchanged.

What the diagnostic already showed (canonical): every radius within 0.3 % at t/t_f <= 0.9; at t_f the x0 = 2 kpc shell is
at 0.0150 kpc in SP against 0.0048 kpc classically (the focus is regularized at the de Broglie scale), and after t_f the
classical shells pass through the centre while the SP Lagrangian radii stay positive (no shell crossing in the wave's
mass coordinate).

Labels resting on KA4(ii): V1's S3 items (the solver's runs). V2's label does not rest on it (S1c uses QG1's code; S3
for V2 rests on the exact identity and on KA4(i)).

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
