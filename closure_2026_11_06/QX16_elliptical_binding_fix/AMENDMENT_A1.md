# QX16 amendment A1 (after U1's first print, before any rerun number)

U1 as frozen compared Mtot(1e9 kpc) with Mvir. That statement was ill-posed: an NFW enclosed mass grows as
ln(r) beyond r_s, so Mtot(1e9 kpc) is 6.5-17x Mvir for every row. The ratio says nothing about binding.
U1 as frozen therefore prints FAIL on its Mtot half (u1_check.out, kept). Its Mbar half (rel 3.4e-9 to
4.8e-9 vs 1e-6) and its distinctness test PASS. On the unfixed code both halves FAIL (u1_check_UNFIXED.out):
6 of 7 rows carry NGC6482's model.

A1 replaces the Mtot half with Mtot(Rvir) = Mvir to 1e-3 (Mvir includes the stellar mass; the NFW part is
normalised to Mvir - Mfit at Rvir). Nothing else changes. The check is in u1_check.py; its output goes to
u1_check_A1.out.
