# Correction and two final results

## CORRECTION to commit 6f8fb5c7f — H045's Lean DOES compile
I reported "7 sorry, exit 1" for `lean/H045_negative_energy.lean`. That was true
when I checked it mid-run, but Agent I repaired it before finishing.
Re-verified: **exit 0, ZERO sorry**, axioms within {propext, Classical.choice,
Quot.sound}. H045 now carries a valid Lean certificate. My earlier statement
was correct at the time and is now superseded.

## H045 — the crossing, in full
- **u\* = 1.223856281422085**, K\* = 1.497824197576293. Unique (f' > 0 so rho is
  strictly decreasing). c_s^2 stays in (1/2, 1) THROUGH the crossing — it is a
  sign change, not loss of hyperbolicity.
- **Reachable: yes, emphatically.** u >= u\* iff g_N >= 1.9528 a_0 iff
  r <= 0.7157 r_M = 6.76 kpc for M_b = 6e10 Msun — the whole inner galaxy.
  Solar surface: u = 1.46e12, i.e. 10^12 times the crossing.
- **No domain restriction exists — PROVED, not merely not found.** y(u) =
  u - u/(1+u)^2 is strictly increasing (identity: y(b)-y(a) =
  (b-a)[((1+a)(1+b))^2 + ab - 1]/((1+a)^2(1+b)^2), bracket = s(2+s)+ab > 0) and
  y(u) >= u - 1/4, so it is unbounded. Every u in [0,inf) is realized by some
  radius.
- **The disease is wrong-sign gradient energy:** P_X = -f' = -mu_2 < 0 for every
  K > 0 (canonical scalar: +1). Energy unbounded below (no ground state);
  G^00 = -f' < 0 — a ghost despite c_s^2 > 0. H011's S3 "no tachyon" pass used
  rho = 2Kf' - f (the TIMELIKE branch density) on a SPACELIKE branch. H034's
  perfect-fluid form is likewise invalid there (p_r = Lam^4(f - 2Kf') !=
  p_t = Lam^4 f).
- Gravitates: -90 arcsec/century Mercury perihelion vs 0 +/- 0.04. Flipping the
  kinetic sign gives +90 — equally excluded. Needs high-acceleration SCREENING,
  and mu_2 -> 1 is the opposite of decoupling.
- **Two further internal issues flagged (unresolved):**
  1. H034 eq. (II) is SOURCELESS while H008/H011 use the SOURCED form
     div[mu_2 grad phi] = 4 pi G rho_bar.
  2. With phi_dot = 0 the Noether charge density J^0 = f' phi_dot VANISHES, so
     H035's rescue ("the dark mass is the conserved charge") is EMPTY on the
     static branch.

## H046 — n = 2 is NOT forced by health conditions (48 theorems, exit 0, 0 sorry)
The identity that kills it: with K = u^2 and f'(K) = mu(u),
`2K f''(K) = u mu'(u)`, so
    c_s^2 = f'/(f' + 2K f'') = mu/(mu + u mu') = 1/(1 + d ln mu / d ln u).
Health (0 <= c_s^2 <= 1, no ghost, stability) is exactly
`mu > 0 AND mu' >= 0` — a condition on the LOG-SLOPE. The deep slope n is the
AMPLITUDE and cancels out of every health condition identically.

- Healthy kernels with deep slope n exist for EVERY n > 0 (mu_n = 1-(1+u)^{-n});
  n = 1, 2, 3 all verified healthy. Even at fixed n = 2 the shape is not fixed.
- **Forced and new (n-independent):** deep sound speed is exactly 1/2 for any
  healthy k-essence with a linear MOND regime — the measured [1/2, 1) is a
  PREDICTION, not a fit.
- **Sharp bound (family-dependent, flagged):** in the minimal Pade family,
  subluminality gives n <= 2 and positivity n >= 0. Observed n = 2 SATURATES it.
  A bound, not a derivation.
- **Footings differ:** the seesaw n = Lam^2/(a_0 M_Pl) gives 2.000 at the
  canonical a_0 but 1.660 at the alternative — a 20.5% split. Health permits
  both, so it cannot adjudicate footings either.
