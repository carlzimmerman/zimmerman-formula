INTERP 0022 -- seed: "torsion of the nu0 window quantizes the Cabibbo angle;
the CKM CP phase (~1.14 rad) is the shadow of the binding-epoch wall z=10.8;
what ONE dimensionless number do both bullets share?"

CHARITABLE READING
Both bullets are the same claim in two dressings: the torsion of the nu0 window
is a single dimensionless winding, tau, that flavor dynamics sample at two
harmonics. Bullet 1 reads tau off theta_C; bullet 2 reads tau off the resonance
(delta, z). The wildcard (shared number) is that ONE torsion winding tau -- not
two independent constants.

QUANTITIES (both footings on any dimensional anchor; here all dimensionless)
  theta_C = 0.2250 rad (Cabibbo; PDG sin^2 = 0.0502 -> theta_C = 0.2249)
  delta   = 1.14 rad   (CKM CP phase, ~65 deg)
  z_bind  = 10.8       (binding-epoch redshift wall)
  derived: delta*z = 1.14*10.8 = 12.31 -> delta*z/pi = 3.92  (a 4-pi resonance)
  derived: delta/theta_C = 1.14/0.225 = 5.07                 (a 5-th harmonic)

SHARED NUMBER (wildcard answer)
  tau = the nu0-window torsion winding. Hypothesis: it is ONE real number that
  governs BOTH bullets. Concretely posited:
     tau = theta_C = 0.2250 (bullet 1 fixes tau)
     and  delta*z = 4*pi      (bullet 2: the CP phase is the 4-pi shadow of z)
  i.e. delta = 4*pi/z = 1.163 rad.

TEST (exact, falsifiable)
  T1 (bullet 1): tau == theta_C within PDG band.
  T2 (bullet 2): delta measured vs 4*pi/z_bind = 4*pi/10.8 = 1.163 rad.
        PDG delta = 1.14 rad -> deviation = 2.0%.
  T3 (the wildcard): T1 and T2 must use the SAME tau with no free fit -- the
        prediction 4*pi/z must be written WITHOUT theta_C, then compared to delta.
        Both T1, T2, T3 must hold at <= 3% with ZERO fitted prefactor.

WHAT KILLS IT
  - If delta*z/pi is not ~4 (here 3.92: 2% off the 4-pi resonance) OR
  - if delta/theta_C is not a clean small integer (5.07, not 5) OR
  - if forcing the single tau makes T1 and T2 require DIFFERENT values
    (theta_C=0.225 vs 4*pi/z=1.163/... two different taus) -> DISCARD.
  Kill band: any bullet off by >3% with no free parameter. A loose ~2% is a
  NEAR-MISS, not a hit -- flag for refine-once, do NOT count as derived.

STATUS: candidate. Blind referee grades. Note 4 vs 5 integer tension = the
honest near-miss risk; that tension is itself the discriminator.
