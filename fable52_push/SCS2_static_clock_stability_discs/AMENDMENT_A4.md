# SCS2 AMENDMENT A4 (post hoc, AFTER the graded frozen-fit route-1 run; committed alone, before any A4 number)

TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed.

**What changes.** Route 1 gets a second local fit, run beside the frozen one, not in place of it.
- The polynomial is a cubic in the grid's own coordinates: (ln r - ln r_0, theta - theta_0) for axisymmetric backgrounds,
  and (ln r - ln r_0, theta - theta_0, phi - phi_0) in 3D.
- It is fitted over the same 5 x 5 (5 x 5 x 5) cell stencil at the same frozen points.
- The Cartesian derivatives of Phi up to third order come from the exact chain rule (sympy).
- Everything downstream is unchanged: N's tensors, the symbol, the hand form, growth, free fall and r/v_c.

The A4 fit is graded against the frozen KA1 with the frozen 1 % line, and the MUTATE arms are rerun with it. Outputs carry
the suffix _A4. Both fits are reported.
- If KA1 passes with the A4 fit, route 1's labels are read from the A4 run.
- If KA1 fails with it too, route 1 stays NO VERDICT and so do the labels that need it.

Nothing else changes: no line, background, map, route-2 setting, MUTATE arm or label rule.

**Why, and what was seen first (post hoc).**
- KA1 (the point mass at log M_b 10.45, 30 kpc, kr 1e3) was missing from the route-1 script. It was added after the main
  frozen-point run had started and was run alone (scs2_wkb_KA1.json). With the frozen fit (a cubic in R - R_0, z - z_0),
  omega^2 r^2 comes out 3.9 % above SCS1's in every direction and on both footings: 1.1593e-7 against 1.1154e-7 radial,
  5.1734e-8 against 4.9785e-8 tangential (canonical). The line is 1 %. **KA1 FAILS with the frozen fit.**
- The background is not the cause. At that cell (r = 31.4 kpc, theta = 44.8 degrees) the solver's finite-volume D.P is
  0.75 % below the closed-form phantom density of the point mass, and |grad Phi| is 0.25 % below.
- The cause is the fit's truncation. The stencil spans ln r +- 0.30 and theta +- 9.7 degrees, too wide for a cubic in
  Cartesian offsets to give second derivatives of a field that goes like ln r to 1 %.
- Seen in the same runs, at the frozen points:
  - At the reference points, where D.P is large, G from the frozen fit agrees with the grid's D.P to 2-3 %.
  - At the most negative cells of the external-field brackets it is 0.06 to 0.47 of the grid's value, and one of six has
    the opposite sign (the MUTATE M1 run, log M_b 10.45, 0.1 a0).
  - Those cells lie near the null of the total field, where the field turns over the stencil.
- In (ln r, theta) the point mass's potential is close to linear in ln r, so a cubic there has a much smaller truncation
  error. That is the reason for the choice. It is also the most natural one: the solver's own coordinates.
- I have not run the A4 fit on anything before committing this amendment.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
