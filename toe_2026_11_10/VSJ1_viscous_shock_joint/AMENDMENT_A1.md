# VSJ1 AMENDMENT A1 (post hoc; committed alone; written after the first runs were seen, before any gate was graded)

**What was seen before this was written.** The run summaries of the six S-seed runs, the resolution run, the M1 run,
KA1, KA2, KA4, the G2 residuals, and two S-cosmo trial runs (A = 0 and A = 1): VSH1's R_sh and S, R_ta, the frozen
R_st, the outermost hot zone, the charge inside candidate edges (0.69 to 0.86 M_b in S-seed; 1.78 and 13.35 M_b in the
two S-cosmo trials), and the profile of |v|/v_ref against radius. The grader had not been run: no G3, G4 or G5 number
existed. From the charges above the direction of G4 under S-seed can be guessed; that is disclosed.

**As frozen the lane reads NO VERDICT on both footings**, for the reason in item 1: the frozen R_st does not measure
where the clock stands, and S-cosmo's host rule was not tuned under it.

1. **The frozen standing statistic is mis-specified.** S_c(<r) is a cumulative ratio whose denominator is dominated by
   the deep centre (v_ref^2 is 100 times larger at 1 kpc than at 300 kpc). It stays below 0.10 far outside the shock,
   through shells that are in free infall or still expanding: the frozen R_st is 109 / 403 / 872 kpc (S-seed, log M_b
   9 / 10.5 / 11.5) and 502 / 859 kpc (S-cosmo trials), beyond the turnaround radius (58 / 260 / 588 and 372 / 649 kpc)
   in every run, while |v|/v_ref passes 0.10 at 73 to 283 kpc. A region that contains the turnaround radius is not
   standing. **Replacement (A1):** a zone is standing iff |v_zone| <= 0.10 v_ref at that zone. **R_st is the largest
   zone radius inside which at least 95 % of the clock charge sits in standing zones.** M_hot(<r) = Q(<r) for
   r <= R_st, as before. On the runs seen this gives 76 / 144 / 275 kpc (S-seed) and 146 / 283 kpc (S-cosmo trials),
   within 5 % of the outermost hot zone in the shock-capture runs.
2. **Host-mass rule:** unchanged in words (the charge inside the standing region today is the host mass within 10 %);
   it now uses A1's R_st.
3. **KA5** compares A1's R_st between N 300 and N 600.
4. Nothing else changes: the supplies, both host brackets, the gates and their lines (0.10 dex in G3 and G4), G5's three
   radii, the labels, the other known answers and their tolerances, MUTATE.
5. **Reported beside every A1 line:** the same gate with the frozen R_st, for S-seed (the runs carry both). For S-cosmo
   the frozen-R_st host ratio of each A1-tuned run is reported; no second tuning is run.

Also on the record before grading:
- G1 is reproduced at all three masses on both footings (my R_sh 154.0 / 410.5 / 839.2 kpc against VSH1's 153.9 /
  410.3 / 836.6; S 4.0e-5 / 2.1e-5 at 9 and 10.5). The 11.5 runs are N 300, as frozen.
- KA4's shock sits at 0.382 of the turnaround radius against 0.339 (+12.6 %, inside the 15 % line) with slope -2.35.
- The first G2 run printed one FAIL on the extra hydrostatic check (c2): sympy did not reduce ((c0 - Phi)^(3/2))^(5/3)
  because the depth was not declared positive. The check was rewritten with a positive depth h = c0 - Phi and gives 0.
  The five frozen residuals were 0 in both runs.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
