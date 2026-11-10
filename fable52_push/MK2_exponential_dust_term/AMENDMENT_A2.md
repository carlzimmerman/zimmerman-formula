# MK2 AMENDMENT A2 (POST HOC; committed alone)

**Post hoc in this sense.** The first graded run of rows c and d had started. It crashed at its first known answer
(KA4) before any gate value or interval was printed. I read only one thing from its part file: which systems had no
no-dust starting state.

**What was found.** Six gas-only group brackets (HCG62, S0805, A194, WBL154, IC1262, A3390) had no capped state even
with no dust. The criteria's cap is local: the charge ends where C(r) = X_cl M_b(r). For these groups the law's own
charge, C/M_b = nu - 1, is above 5.41 at every radius. In the deep-MOND core M_b(r) is small, so the ratio starts
above the share, and the cap function never crosses from below. For HCG62, C/M_b is 27 at 1 kpc, 5.7 at 20 kpc, 7.0 at
R2500 and 7.5 at R500. So the local cap has no first crossing.

**The rule now.** Form B's share belongs to the whole system, not to each radius.
- **Global cap:** the charge ends at r_c, where C(r_c) = X M_b,tot. Here M_b,tot is the system's baryon mass inside
  R_sys, and baryons are truncated at R_sys:
  - X-COP: R_sys = R200 (Ettori 2019; CO1's scope, the cluster share inside R200);
  - groups: R_sys = 1.5 R500 (QX2's fallback for R200);
  - galaxies (rows e, f, h): the Hernquist total (M_b,tot = 1 in units of M_b).
  Since C(r) starts at zero and grows, the first crossing is well defined.
- **Beyond r_c:** M_L = M_b(r) + C(r_c), Newtonian, and Phi -> 0 at infinity, as before.
- For a point mass this is identical to the criteria's rule (ONE1's construction). Every gate radius (X-COP to
  0.7 R500; groups at R2500 and R500) is inside R_sys.
- The KiDS row's frozen known answer (ONE1's numbers at no dust) is unaffected, because A1 applies the dust as a
  difference on top of ONE1's point mass.

**What is discarded.** The first graded run's part file (`parts/rows/graded_canonical.json`) is deleted, not used. M-NOCAP
(A1 section 3) has no cap and is unchanged.

No line, gate, grid or known answer changes.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
