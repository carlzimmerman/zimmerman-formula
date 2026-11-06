# QX5 iter a2: class a's lead on galaxies inside a cluster potential (Coma UDGs)

Frozen before any a2 number. Kappa = 1/2 FITTED; not theory closed. Post-result test (AMENDMENTS A1/A2): it can
kill class a's lead or keep it alive; it cannot make class a a PASS.

Model. Class a multiplies every phantom by F(|Phi|/c^2). A UDG at 3-D distance d_mean in Coma sits at Coma's
potential depth (>= 2e-5 from the beta-model alone, inside the cluster block of the key). Its internal dispersion
is then sigma_F^2 = sigma_N^2 + F (sigma_v3^2 - sigma_N^2), where:
- sigma_v3 is S1's v3s prediction in Coma's measured field at d_mean (E_v3_dmean in s1_coma_per_galaxy.csv,
  E-W estimator, the 9 CFG933-admitted UDGs, per footing);
- sigma_N is the Newtonian value from the same Plummer Jeans machinery (d10_solver.jeans on plummer_gN, imported
  read-only).
Per galaxy E_F = E_v3 - ln[r_N + F (1 - r_N)], with r_N = sigma_N^2 / sigma_v3^2.

F values (generous to the lead): F_med = X-COP's median required F (4.09 canonical, 3.66 alt) and F_max = X-COP's
largest (5.67 / 5.06). Reported, not graded: the F that would make the mean E_F = 0.

Statistic and errors: mean E_F over the 9, divided by sigma_tot = hypot(se, sigma_sys) taken from S1's
'S4 v3 dmean' row for the floor Lstar (stated approximation: E_F is E_v3 shifted by a near-uniform log term).

Lines (both footings):
- LEAD KILLED (class a DEAD-BY-MEMBERS) if z = mean E_F / sigma_tot >= 3 even at F_max on both footings.
- LEAD ALIVE (still CLUSTER-SET, not a pass) if |z| < 3 at F_med on both footings.
- UNDECIDED otherwise.

Known answer: F = 1 reproduces S1's mean E_v3_dmean (canonical +2.581, alt +2.481) to 1e-6.
MUTATE (separate output): F = 30 must drive the mean E_F below +1.0, so the statistic can see a large F.
