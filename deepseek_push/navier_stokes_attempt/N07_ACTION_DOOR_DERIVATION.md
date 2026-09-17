# N07 — THE ACTION DOOR: DERIVATION (D1–D4, executed 2026-09-17)

Lane: `N07_action_door.py` (run: `python3 N07_action_door.py | tee N07_action_door.out`).
Registration: `N07_ACTION_DOOR.md`. Launch rung: G031 the GR fluid action
(THE_THEORY.md L5); equilibrium spine: THE_EQUILIBRIUM_THEORY.md; the
a0/2-cap certificate: `lean/NSE_a0line.lean` (`a0cap_bound`, zero sorry).
Constants: a0 = 9.3619e-11 m/s^2 (MEASURED), G = 6.674e-11, M_sun = 1.989e30 kg,
M_b = 1e10 M_sun, kpc = 3.086e19 m. All gates PASS (15/15); a FAIL would have
been a finding.

## D1 — THE CUSP (the static dark sector already carries an axis singularity)

The G031 isothermal chain, re-verified sympy-exact inside the lane:

    sigma^2 = G M_b/(2 r_M) = sqrt(G M_b a0)/2            (Zimmerman temperature)
    rho_ph  = sigma^2/(2 pi G r^2) = sqrt(G M_b a0)/(4 pi G r^2)   (V1, V2 PASS)

(a) **exact 1/r^2**: rho_ph · r^2 = sqrt(G M_b a0)/(4 pi G), r-independent
    (sympy exact) — a pure cusp at r = 0, time-independent: the equilibrium
    phantom is a STATIONARY density singularity at every baryon centre.
(b) **enclosed mass**: M_ph(r) = 4 pi int r'^2 rho_ph dr' = 2 sigma^2 r/G ~ r
    (sympy exact): the cusp is integrable — M_ph(0) = 0, M_ph(r) finite at
    every r — while rho_ph -> inf as 1/r^2 (density singular, mass finite).
(c) **the Law's structure**: g_ph = G M_ph/r^2 = sqrt(G M_b a0)/r and
    g_ph/g_N = r/r_M EXACTLY (sympy): phantom subdominant inside r_M
    (the Newtonian face, g_N > a0), dominant outside, crossing at r_M.

Numbers (M_b = 1e10): r_M = 3.8586 kpc; M_ph(r_M) = M_b = 1.0000e10 M_sun;
g_N(r_M) = g_ph(r_M) = a0 = 9.3619e-11 (relative diff 0.0); rho_ph(1 kpc) =
1.396e-20 kg/m^3 = 0.206 M_sun/pc^3. Gates: **G40 PASS** (cusp 1/r^2, sympy),
**G41 PASS** (g_ph/g_N = r/r_M, symbolic; subdominance + crossing).

## D2 — THE CAUSTIC CHANNEL (the framework's singular sector is the dark dust)
The phantom is pressureless: its dynamics are the dust problem. The monkey
rung is the classical collapsing sphere r'' = -G M/r^2, r(0) = r0, r'(0) = 0.
First integral (1/2)r'^2 = G M(1/r - 1/r0); the quadrature via
r = r0 cos^2(theta) integrates EXACTLY (sympy):
    t_coll = int_0^{r0} dr/sqrt(2GM(1/r - 1/r0)) = (pi/2) sqrt(r0^3/(2 G M))

Numerical verification (RK4 to r -> 0, extrapolated crossing): t_coll =
3.246426e14 s vs closed form 3.246419e14 s = 1.0287e7 yr, |rel| = 2.2e-6,
energy drift 3.0e-10 over the commensurate bulk. **The sphere reaches r = 0 in
finite time — a density caustic.** Classical textbook result (Newtonian dust
collapse; Lemaître 1927; GR analogue Oppenheimer–Snyder 1939; pressureless
caustic formation, e.g. Zel'dovich–Shandarin pancakes — cited as textbook).

The Jeans clock on the phantom's OWN profile, tau_ff = 1/sqrt(G rho_ph):

    r [kpc]   rho_ph [kg/m^3]   tau_ff [yr]
    1         1.396e-20         3.2832e+07
    3         1.551e-21         9.8497e+07
    10        1.396e-22         3.2832e+08

Gate **G42 PASS**: tau_ff(1 kpc) = 3.28e7 yr in [1e6, 1e9] yr (the door's D4
window) — the deep sector responds 1–2 orders below galactic dynamics:
quasi-static equilibrium reading holds, and the clock is fast enough to
mediate the a0-line in flows.

## D3 — THE TRANSFER (the door's kill analysis)

(a) **The reaction is capped exactly**: the phantom's reaction on baryons is
|g_ph| = g_obs - g_N = sqrt(g_N^2 + a0 g_N) - g_N <= a0/2 for ALL g_N >= 0 —
the Lean-certified `a0cap_bound` (NSE_a0line.lean, 11 theorems, zero sorry).
Lane check (stable form a0·u/(u + sqrt(u^2+u)), u = g_N/a0 in [1e-8, 1e8],
65536 points): max = 4.680949988e-11 m/s^2 = a0/2·(1 - 2.5e-9); sympy limit
g_ph/a0 -> 1/2 exact; (x + a/2)^2 - (x^2 + a x) = a^2/4 >= 0 exact.
**G43 PASS** (1e-12 relative tolerance). The cap is an asymptote: the grid
approaches it as 1/(4 g_N/a0); the identity's approach is certified exactly.
(b) **The bounded-perturbation read**: a force density bounded by a0/2
everywhere is N02's sub-regularizing class (the certified a0/2-capped drag:
cannot close the enstrophy gap). The phantom dust can pile up at its own
centre in finite time (D2) — a bounded (L^inf <= a0/2) forcing on the baryon
fluid. **The caustic is CONFINED to the dark sector; the baryon Clay problem
stays on the Newtonian face: KILL K-1 FIRES.**
(c) **The residual (honest)**: away from the equilibrium closure the action's
dynamics are NOT committed — the G03 action door is OPEN. IF the
nonequilibrium coupling can exceed the measured cap a0/2, D3 OPENS and the
baryon transfer lives (K-2): registered, measurement-awaited, exactly like
the kappa pair (N03, kappa <= 2.6e-8, survival-gated). **G45 PASS** (the
residual is stated in the lane's own text). This lane proves K-1 on the
MEASURED reaction law; it does not prove the action cannot outrun the law
off-equilibrium.
(d) **The toy (the kill made visual)**: a viscous baryon layer in a fixed well
at r_b = 0.15 pc (deep cusp, M0 = M_ph(r_b) = 3.89e5 M_sun), driven by a
collapsing phantom with the registered profile M_ph(t) = M0/(1 - t/t_c),
t_c = tau_ff(1 kpc) = 3.2832e7 yr, run to ln(M_ph(t_f)/M0) = 25 (t_f = (1-e^-25) t_c):
du/ds = (g_eff - gamma u) t_c e^-s, gamma = 1/(6 t_c), u(0) = 100 m/s,
identical grid and ICs for both panels (same seed, exactly).

    CAPPED   (g_eff = min(G M_ph/r_b^2, a0/2)): u(t_f) = 4.476e4 m/s = 44.8 km/s  FINITE
    UNCAPPED (g_eff = G M_ph/r_b^2):            u(t_f) = 6.198e10 m/s = 2.07e2 c  unbounded

The uncapped response grows like the LOG of the phantom's mass
(du/d ln(M_ph/M0) = 2.4952e9 m/s per e-fold over the last decade, the g0·t_c
class); the capped response is flat (4.9e-3 m/s per e-fold). **G44 PASS**:
capped/initial = 4.48e2 < 1e4; free/capped = 1.385e6 > 1e6. The baryon speed
at t -> t_c: FINITE with the cap enforced, unbounded with the cap relaxed
(the toy is an illustration of the transfer channel; no speed-of-light
imposed — the contrast is the content).

## THE KILL BOX AND THE VERDICT

| Gate | Content | Measured | Status |
|---|---|---|---|
| G40 | cusp exact 1/r^2 (sympy) | rho_ph·r^2 = sqrt(G M_b a0)/(4 pi G) | PASS |
| G41 | g_ph/g_N = r/r_M (symbolic) | exact; crossing at r_M = 3.86 kpc | PASS |
| G42 | tau_ff(1 kpc) in [1e6, 1e9] yr | 3.2832e7 yr | PASS |
| G43 | max g_ph <= a0/2 (1e-12 rel) | a0/2·(1 - 2.5e-9) | PASS |
| G44 | toy: capped < 1e4, free > 1e6 | 4.48e2 / 1.385e6 | PASS |
| G45 | G03-open residual stated | tokens in file | PASS |

K-1 (die by measurement) **fires**: the reaction is the measured law and the
law is capped at a0/2 exactly — the phantom's caustic is confined to the dark
sector, the baryon Clay problem stays on the Newtonian face. K-2 (live by
action) is **registered, measurement-awaited**: the G03 action's
nonequilibrium coupling is the only route that could reopen D3.

THE TRANSFER: bounded by the measured a0/2 cap: the phantom dust caustic
is CONFINED to the dark sector; the baryon Clay problem stays on the
Newtonian face (K-1 fires); the live remainder is the G03 action (K-2,
measurement-awaited).