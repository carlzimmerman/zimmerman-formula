# X2 pre-declared menu (written and hashed BEFORE any script of this lane was run)

Lane X2: gravitational analogues of collective frequencies / screening lengths (plasma, Jeans, Debye, wave-breaking).
Conventions: c = 1 in formulas (restored in text). Held fixed variable: **G rho_Lambda** (name of the variable, per audit H3);
Lambda := 8 pi G rho_Lambda (Einstein). Reference unit s := c sqrt(G rho_Lambda). Target a0 = s/2, so
ratio(entry) := (entry in units of s) / (1/2) = 2 x coefficient. Exact hit := ratio == 1 as an exact symbolic number.
Target-blind disclosure (BRIEF rule 1): the menu below was written by a person who knows the target; by hand I already
know (before running anything) that W4 = c^2/lambda_J is the closest entry at 2/sqrt(pi) = 1.128 and that no entry
is expected to hit exactly. The table is reported once, ranked, with decoy calibration (below); no entry may be added or
removed after the hash is written (each script re-checks the hash).

## Family V: acceleration = c * omega  (rate omega; 'c omega' is the only acceleration a rate defines when the only speed is c)
V1 omega = H_Lambda = sqrt(Lambda/3)              de Sitter e-fold rate
V2 omega = sqrt(Lambda)                           Einstein-static-universe (Eddington) instability rate of dust + vacuum
V3 omega = sqrt(2 Lambda)                         listed in the task ('Lambda instability rate'); no derivation of a physical rate with this value is claimed
V4 omega = omega_J = sqrt(4 pi G rho_Lambda)      gravitational plasma / Jeans frequency (also the Dawson cold wave-breaking acceleration c*omega_J by the plasma analogy; not a separate entry)
V5 omega = sqrt(4 pi G rho_Lambda / 3)            oscillation / Kepler frequency inside a uniform density
V6 omega = 1/t_ff, t_ff = sqrt(3 pi/(32 G rho_Lambda)) = (pi/2)/sqrt(8 pi G rho_Lambda/3)   uniform pressureless sphere free fall

## Family W: acceleration = c^2 / lambda with lambda = 2 pi c/omega (the wavelength of the mode; Jeans length for V4 with c_s = c)
W1..W6: the same six omegas as V1..V6.  W4 is the Jeans acceleration c^2/lambda_J, lambda_J = c sqrt(pi/(G rho_Lambda)) with c_s = c
(c_s = c because the vacuum is Lorentz invariant, so c is the only speed available; c_s^2 = w = -1 would make lambda_J imaginary).

## Family P: acceleration = omega^2 * ell  (frequency squared times a length; the 'omega^2 x length' of the task)
omega^2 in { 4 pi G rho_Lambda, 4 pi G rho_Lambda/3, H_Lambda^2 = 8 pi G rho_Lambda/3, Lambda = 8 pi G rho_Lambda }
ell in { R*/2, R* }, R* = c/sqrt(G rho_Lambda).           8 entries: P1..P8 (omega^2 index major, ell minor).
(ell = c/omega reproduces family V and is not repeated.)

## Family R: reference / planted (not collective)
R1 c^2/R*      = 2 a0  (rational ratio 2; R* = 1/sqrt(G rho_Lambda) is the puzzle's own length, not a collective scale)
R2 c^2/(2 R*)  = a0    (PLANTED: the target itself; the scan must flag it as a hit; used as the positive control)

Total 6 + 6 + 8 + 2 = 22 entries.

## Non-menu items (derived, not scanned)
- linear response of the vacuum: k_J^2 = 4 pi G (rho+p)/c_s^2 -> 0 exactly at p = -rho  (script x01/x02)
- 'what it would take' inputs (x03) are computed AFTER the target is known and are labelled inputs, not results

## Scan design
- exact hit: sympy exact equality ratio == 1.  near: |ratio - 1| < 0.13 (data-band descriptor only, not evidence).
- decoy calibration: for 400 log-spaced multipliers t in [0.2, 5] (target := t * a0) count entries within +-13% of t*a0;
  report the count at t = 1 and its percentile among all t; plus a shuffled-menu control (each entry's coefficient multiplied by an
  independent seeded log-uniform factor in [1/3, 3]) to show that 'a nearest entry within ~13%' occurs at high rate for a menu of this size.
- pi-class: ratio written as (algebraic) x pi^e; report e.  Controls: mutate 4 pi -> 8 pi in V4, must move the ratio; planted R2 must hit.

## Derivation checks declared for x01-x03 (each with a control that must fail)
x01: general-(w, c_s^2) sub-horizon fluid equation in the Newtonian gauge; known limits (dust; radiation; clustering-dark-energy ratio
     (1+w)/(1-3w) for c_s = 0 in matter domination); Heath growth of dust in dust + vacuum; gravity enters the vacuum's own
     perturbation dynamics only through (1+w); ESU rate; 4 pi G (rho+3p) = -Lambda (task says -2 Lambda: to be checked).
x02: SdS/Kottler is an exact vacuum + Lambda solution and its O(M) part carries no modification; hydrostatic Green's functions
     (Jeans/anti-screening cos, Yukawa) for (rho+p) != 0; linear response => force linear in M (BTFR slope 2, not 4).
x03: what a linear response would need to give a 1/r force with MOND coefficient at a single mass; the nonlinear-medium scale.
