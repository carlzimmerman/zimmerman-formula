# REL1 AMENDMENT A1 (POST HOC: after the first full run read the K4 energy check as FAIL), committed alone

TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

**What happened.** The criteria (e495153acf, item K4) set "conservation of its Ostrogradsky energy (drift line 1e-8
relative)" without saying relative to what. The script divided the largest drift by the largest |H_O| seen. H_O starts
at -1e-12 (the eps of the initial data) and stays there, while its five terms (xdot^2/2, -xdot q', q (y - g), g x,
-J(y)) grow to 1e9 near the blow-up; round-off of order 1e-7 in their sum was then divided by |H_O| ~ 1e-7, giving 1.00.
The first run's line therefore read FAIL and its label NO VERDICT (rel1.out of that run, not kept: it was overwritten
by the rerun below; this file quotes it). A diagnostic (no grade) printed the drift at 25 times over the run divided by
the largest term at each time: at most 2.1e-14.

**Change.** The drift is measured at each output time against the largest of H_O's terms at that time (the standard
measure for a conserved sum of large cancelling terms); line unchanged at 1e-8. Nothing else changes: same system,
same initial data, same integrator and tolerances, same stop at |q| = 1 - 1e-9.

**Why it is not a rescue of a fail.** H_O is conserved analytically (dH_O/dt = xdot (xddot + g - q'') + q (x''' - y') = 0
on shell); the check only tests the integrator. It bears on the label only through NO VERDICT; it cannot turn the
runaway into anything else, and KA4 (the growth rate, 1.000000) already passed.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
