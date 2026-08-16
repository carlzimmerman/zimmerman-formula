# INTERP 0018 — deciphering seed_0018.txt

SEED (3 bullets):
1. Resonance M_lens/M_dyn = 29 at the f = 1/3 fixed point might set n_s = 0.9649.
2. The pi-free part of m_W/m_Z (0.8814) may be the shadow of the transition
   z_t = nu0^(-1/3) - 1 in [17,35].
3. WILDCARD: what single dimensionless number do BOTH bullets share if true?

CHARITABLE DECODE
- Bullet 1 (cosmo sector): a mass-ratio resonance R = M_lens/M_dyn = 29, evaluated AT
  the fixed point f = 1/3, is claimed to predict the scalar spectral index
  n_s = 0.9649 (~ Planck 0.9649).
- Bullet 2 (SM sector): a cube-root phase transition z_t = nu0^(-1/3) - 1 in [17,35]
  "casts a shadow" equal to the pi-free part of the electroweak mass ratio,
  0.8814 (true m_W/m_Z = cos(theta_W) ~ 0.877; 0.8814 read as the pre-pi intermediate).
- WILDCARD ANSWER (charitable): the shared number is 1/3. The cube-root / fixed-point
  structure appears in BOTH bullets (bullet 1: f = 1/3; bullet 2: nu0^(-1/3)). A single
  cube-root map M read at f* = 1/3 is proposed as the common parent of both numbers.

HYPOTHESIS (one, falsifiable)
H18: A single dimensionless master number, the fixed-point value f* = 1/3, governs BOTH
sectors through ONE analytic cube-root map M, read in two branches:
  - cosmo: n_s            = M_+(f*, R)   with R = 29      -> predicts 0.9649
  - SM:    pi-free(m_W/m_Z) = M_-(f*, z_t)                -> predicts 0.8814
with f* = 1/3 held IDENTICAL across sectors and <= 2 total free dimensionless constants.

EXACT TEST
1. Solve M_+(1/3, 29) = 0.9649 and M_-(1/3, z_t) = 0.8814 from ONE functional form M
   with a branch label sigma in {+,-}.
2. Numerically verify z_t = nu0^(-1/3) - 1 in [17,35] for the nu0 that reproduces the
   SM branch (i.e. nu0^(-1/3) in [18,36]).
3. Internal consistency: both branches must reuse the SAME f* = 1/3 and the same
   <= 2 constants. No per-sector re-fitting of f*.

KILL CRITERIA
- No single M(f*=1/3, <=2 constants) hits BOTH 0.9649 and 0.8814 within 2x tol -> DISCARD.
- z_t lands outside [17,35] -> DISCARD.
- The two sectors require DIFFERENT f* (the "shared 1/3" is not actually shared)
  -> REFUTED (wildcard premise dead).
- 0.8814 cannot be tied to a pre-pi intermediate of cos(theta_W) ~ 0.877 (the "pi-free"
  reading fails) -> REFUTED.

FOOTINGS
Seed is dimensionless; a0 footings (9.3619e-11 / 1.1279e-10) not directly invoked. If
nu0 is dimensional, evaluate z_t at BOTH footings; H18 stands only if both give
z_t in [17,35].

NOTE: not tested here -- a separate blind session referees it. No claim that any number
is derived; 0.8814 and 0.9649 are fit targets, not results.
