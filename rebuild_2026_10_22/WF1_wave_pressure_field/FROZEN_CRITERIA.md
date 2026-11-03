# WF1_wave_pressure_field: FROZEN CRITERIA, committed alone before any script or number

Launched under the owner's 2026-11-02 instruction to launch search lanes without asking. This is a classical scalar field of mass parameter m, a gravitating field component. Production as a particle isn't assumed. The no-particle rule's lift covers HF1 only and this lane doesn't lean on it. It adopts nothing and reinstates nothing from the retired cold sector; any adoption is the owner's call. kappa = 1/2 FITTED. No LambdaCDM input in a grade. Not theory closed. Nothing here says the data favour the framework.

**Not blind.** Read first: HF1, VW1, DF2, DF3. Their lesson: density-keyed pressure either collapses or stays out; gradient keys are ungraded.

## What the record already has, not repeated
- CFG119, CFG159: an SP ground state with baryons doesn't *produce* the law's target, by 4 dex at best. Different question. Here the law stays, and the field sits beside it.
- CFG230 D07, CFG242: the same, as a replacement for the law.
- CFG293: CFG288's wave field at m >= 2e-20 eV has no right-sign window on satellites; it uses a simulation soliton relation. Here m is below that window, with no such relation.
- CFG474: if the field dominates ultra-faints, a published heating bound gives m >= 3e-19 eV, conditional on domination and a virialised halo. Cited, not used as a grade. If m here is light enough for ultra-faints not to hold it, that bound's premise changes; stated, not resolved.
- DW2 row 15: a single-m core with a disc-exclusion role, closed on G1. Not read as binding here because its setting differs; if this lane's disc result is the same mechanism I say so.

## Field
Klein-Gordon, one parameter m, no self-interaction. **One m and one abundance across all gates.** Declared m grid, eV: 1e-26, 3e-26, 1e-25, 3e-25, 1e-24, 3e-24, 1e-23, 3e-23, 1e-22, 1e-21.

## Gate 1, early universe
DF2's patched CLASS copied to this lane's external work dir, with RF5's channels and lines unchanged (HF1 A1 R2: p >= 1e-3 gates, G-A0, S - S_min <= 25 against 2324.03). Effective sound speed c_s^2(k, a) = q / (1 + q), q = (k / 2 m a)^2, Hu, Barkana and Gruzinov's form, capped at 1/3 by DF2's patch, which matters only at q near 1, reported. Newtonian gauge, as DF2.

**Onset, stated.** Before 3H = m the field is frozen, w = -1, and it isn't dust. X34's turn-on is synchronous only and DF2's patch is Newtonian, so the fluid runs as dust from the start, with onset z_osc computed for each m from 3H = m on the cell's own background. RF5's window measured the size of this: dust turned on at z_on in [3e4, 1e6] is indistinguishable within the window, and later fails. So a cell with z_osc >= 3e4 reads directly, with the difference between z_on 3e4 and 1e6 from RF5's table printed as the approximation's size. A cell with z_osc < 3e4 reads **UNDETERMINED, onset outside RF5's window**, with its no-onset number printed as optimistic. No shooting is used; w = O((H/m)^2) neglected after onset.

Flow as DF2: screen every m at RF5's parameters, then fit each m with screen S - S_min <= 2000, at most two fits at once. Reported: k_half against the cold cell, P(k) ratio at z 0.

## Gate 2, clusters, and gate 3, galaxies
Lines as HF1's A1 R5 and R6, unchanged: X-COP all seven, FG1's X line; keys 15 of 15, either h, template mode, f* 0.034, gas +0.005, CRG1's code read-only, f* 0.0615 and DA1's forms beside. SPARC rms <= 0.110, Upsilon 0.50-0.80, tilt <= 0.15, SB slope |Z| <= 2, LT <= 0.10, groups CONSISTENT. Dwarfs, MW, IC 1613 reported; they stay with the law. Canonical primary, alt beside.

**Profile, one rule for every system.** Law g = nu(g_N/a0) g_N on baryons + field. Potential Phi from that g.
- *Core.* Spherical ground state of -(hbar^2 / 2 m^2) lap psi + Phi psi = E psi, self-consistent, with mass M_s. Simulation core-halo relations aren't used.
- *M_s rule, equal velocity.* <v^2> of the ground state = 2 (E - <Phi>) equals 3 sigma^2. Sigma as HF1 R4: sigma^2 = V_max^2 / 2, V_max of the model inside the system's radius, never an observed value. So the core is as hot as what surrounds it. If <v^2> exceeds 3 sigma^2 as M_s goes to 0, M_s = 0. M_s can't exceed the fair share.
- *Envelope.* rho_env = rho_1 exp(-(Phi - Phi(r_ta)) / sigma^2) inside r_ta. Total rho_f = max(rho_s, rho_env). rho_1 from M_f(<r_ta) = fair share (omega_f / omega_b) M_b(<r_ta), CRG1's chain and r_ta, M_f constant beyond, as R4.
- *Too wide to bind.* If the ground state's rms radius exceeds 0.5 r_ta, the system doesn't hold the field: M_f = 0, counted and reported. That's a stated rule, since a wall at r_ta would otherwise set the state.
- *Bracket.* sigma x 0.5 and x 2 in the M_s rule and the envelope, on the selected m, reported. Fair share is an upper bound on retention, stated. No retention scan here.
- *Selection.* HF1's R3 over m passing gate 1, on train only: X-COP positions 0, 2, 4, 6 and SPARC odd names; if none passes both, smallest |mean| on X-COP train; ties by lowest S. If none passes gate 1, the same over all m with numbers, and gates 2 and 3 run as numbers only.

## Gate 3b, forest warning, no verdict
Linear P(k) ratio at z 3 across the raw forest's k range, stated. No particle-mesh run; disk about 16 GB free, compute_queue refuses below 30. Gate 4 structure isn't run. No forest verdict is claimed either way.

## Controls
- CLASS: m 1e-12 eV reproduces RF5's cell, |dplik| <= 0.1, and the patch at c_s 0.
- k_half scales as m^(1/2) between m 1e-23 and 1e-22 at fixed parameters, ratio sqrt(10) within 30 %, and k_half within a factor of 3 of the analytic Jeans value at z 0.
- SP, Newtonian, no baryons, dimensionless: virial 2T + W = 0 within 0.5 %, a solver-independent test; eigenvalue and half-mass radius against the values I recall from Moroz, Penrose and Tod 1998 (E = -0.163 G^2 M^2 m^3 / hbar^2, r_half = 3.93 hbar^2 / (G M m^2)), within 1 %; say if my recollection is what's off, using the virial test as referee.
- Fair share within 1 %. Grid doubling of M_f(R500) within 1 %. Law limit at zero fair share: X-COP +0.467, 0.476, SPARC rms 0.0541.
- MUTATE: m x 16 at fixed M_s and no baryons moves r_half by 16^-2 within 1 %. In CLASS, m x 16 moves k_half by about 4. Planted over-dense field, fair share x 100 and m large, must fail gate 3. Separate outputs.
- Failed checks mean NO VERDICT at that gate.

## Labels
**DEAD AT gate**, first gate failed for every m; **SURVIVES TO gate**; **PASSES at m, rows failing**. A family result on these inputs, not a no-go theorem. A pass is a description that needs an origin, and states of the system aren't shown reachable.

## Liabilities, beside any label
No action couples this field to the a0 law. Whether these equilibria are reachable isn't computed: no formation history, no granule heating, no rotation. Published forest and dwarf bounds on this family exist, and they're LambdaCDM-conditional: cited, not used as a grade. MW and IC 1613 stay with the law. The Bullet: a wave field is collisionless on large scales, so offsets hold by construction when lambda is well below the merger's scale, checked by number at the selected m.

## My expectation, on record
Hand arithmetic, rough: de Broglie length near 1.2 kpc (1e-22 eV / m)(250 km/s / sigma), so at m near 1e-24 eV a disc at 150 km/s sits inside about 200 kpc and a cluster at 1000 km/s has about 30 kpc; k_J at equality near 1 /Mpc. I expect gate 1 to pass from a few 1e-25 eV up. I expect discs to pass at low m and Upsilon to fall at high m, as VW1. I expect clusters to fail anyway, X-COP near HF1's +0.18 and keys near 3 of 15, because the fair-share envelope is what overshoots and a 30 kpc core doesn't touch it. So: SURVIVES TO gate 1, numbers fail at gate 2, and groups below the law as HF1.

## Rules
Post-result changes go in an amendment, disclosed as such. No downloads. Nice 10, at most two fits, under 1 GB, delete nothing.
