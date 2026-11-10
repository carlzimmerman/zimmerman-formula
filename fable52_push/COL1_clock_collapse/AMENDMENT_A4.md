# COL1 AMENDMENT A4 (post hoc; committed alone, before the diagnostic it defines is run)

**Seen first.** Every graded Part 2 row (3 mu_K x 4 masses x 2 footings, both resolutions), the mu_K 198 and at-rest
brackets, the X_out 16 Mpc check, the damped bracket (after a boundary-velocity fix in the driver, disclosed in RESULT.md)
and the MUTATE arms M2, M2a and M3 end at the centre at 0.063-0.154 Gyr after the mass appears. That is the time at which a
cold test shell anywhere inside the softened core reaches the centre (`col1_focus_check.out`), so the halo radii never
evolve before the frozen run stops.

**What is added (reported diagnostic; it sets no label and changes none).** `col1_outer.py` integrates X14's exact shell
equation for every Lagrangian shell independently, in the law-dominated limit mu_K L << 1:

    r'' = -G M_b s(t) r/(r^2 + eps^2)^{3/2} - G M_X/r^2 - (4 pi/3) G rho_b(t) r + Omega_L H0^2 r + U(G [M_X - (4 pi/3) nbar(t) r^3]/r^2),

M_X = (4 pi/3) nbar0 X^3, U(y) = a0 y/(a0 - |y|), from Hubble flow at z 10 (the primary's start), both footings, the four
masses. In that limit the dust part of the charge is the uniform background (its enclosed share (4 pi/3) nbar r^3), and the
polarization charge inside a shell is what it has gained over the background. A shell's enclosed charge changes only when
that shell itself is crossed, so each trajectory is exact up to its own first crossing; crossings among inner shells do
not change an outer shell's enclosed charge. Read:
- the first crossing among shells whose radius exceeds r_x = 3, 10, 30, 100 kpc at that moment (time and radius);
- for shells never crossed by z = 0: whether they sit static (|v| <= 0.05 v_c, |a| <= 0.05 g over the final 2 Gyr),
  oscillate, or are still falling; and M_N(<r)/M_ph(<r) at 10/30/100/300 kpc at z = 0 counting uncrossed shells only.
Scope: valid where (mu_K r)^2 << 1, so it stands for mu_K = 0.1 per Mpc at every radius read and only for r << 270 kpc at
mu_K = 3.71; it is not run as a substitute for the graded rows. Shells 2400 log-spaced in X from 20 kpc to 8 Mpc.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
