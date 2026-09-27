# The first-principles derivation chain -- status ledger

Assembled by `run_chain.py` on 2026-09-27 01:13. A lane counts only if its main run has a verdict and its MUTATE control flips (rc = 1). Status meanings: DERIVED (varied out of the chain above it, with a script), POSTULATED (an input), FITTED (a constant set by data), CONSTRAINT (a derived requirement on a lower link), OPEN (owed), FAILS (derived and contradicted by data).

## Lanes

| lane | checks | load-bearing failures | main rc | MUTATE rc | contract |
|---|---|---|---|---|---|
| FP0_core_postulates | 6/6 | 0 | 0 | 1 | ok |
| FP1_static_sector | 24/24 | 0 | 0 | 1 | ok |
| FP2_relativistic_consistency | 17/17 | 0 | 0 | 1 | ok |
| FP3_cosmology_linear | 27/28 | 0 | 0 | 1 | ok |
| FP4_kick_from_action | 24/25 | 0 | 0 | 1 | ok |
| FP5_dof_and_a0_field | 24/24 | 0 | 0 | 1 | ok |
| FP6_gate_survey | 31/32 | 0 | 0 | 1 | ok |

## Links

| lane | link | status | what | basis |
|---|---|---|---|---|
| FP0 | L0a | DERIVED | the FORM a0 ~ c sqrt(G rho) | C1: unique from (G, c, rho), |det| = 2 |
| FP0 | L0b | POSTULATED | which density: rho_Lambda | physics input; the same form on rho_m or rho_local spans 609x |
| FP0 | L0c | FITTED | kappa = 1/2 (equivalently Z = 5.7888) | not derived by any route tried; the data prefer kappa ~ 0.56-0.64 |
| FP0 | L1a | POSTULATED | the galaxy law g_obs = sqrt(g_bar^2 + g_bar a0) | form = Milgrom 1999 Eq. 9; the coefficient is the framework's |
| FP0 | L1b | DERIVED | deep limit, BTFR v^4 = G M a0, slope s(y), sum rule 3/2 | R1, from L1a |
| FP0 | L1c | CONSTRAINT | the a0/2 tail vs the planets | R2: the action's kernel must reach Newton faster (alpha >~ 1.5) |
| FP0 | L2a | DERIVED | a0(z) flat (rho_Lambda, w = -1) | R3, from L0 + P3 |
| FP0 | L2b | POSTULATED | a0 as a field (a0^2 = kappa^2 G (-p_Q)) | a chosen promotion; the action has to produce it |
| FP0 | L3 | OPEN | the covariant action (root) | next lane: chosen after the candidate map; everything below is varied out of it |
| FP0 | L4-L10 | OPEN | static limit/kernel, lensing, PPN, c_T = 1, stability, cosmology, clusters | each derived from L3 or it fails |
| FP1 | L3 | POSTULATED | the root action: the ungated C-H/K core (C-H + alpha_c a^2 - c_2 (K - <K>)^2, beta = 0) | chosen root (coordinator's redirect); one covariant, spatially nonlocal classical action |
| FP1 | L4a | DERIVED | static weak-field law: psi = Phi; lap u = 4 pi G rho; lap Phi = 4 pi G rho + S* div[(nu(|grad S u|/a0) - 1) grad S u] | A1-A3 (sympy EL of the core; discrete adjoint): QUMOND with a double heat filter = T-B, produced by an action |
| FP1 | L4b | DERIVED | which function sets nu: only the kernel function q (q' = nu - 1); alpha_c renormalises G by <= 2e-7; c_2 static-inert; the filter passes harmonic external fields with gain 1 | A2, A5, B1, E2 |
| FP1 | L4c | DERIVED | P2 embeds exactly: q_P2(s^2) = ((2s+1)/2) sqrt(s^2+s) - (1/4) ln(2s+1+2 sqrt(s^2+s)) - s^2; healthy (C_T, C_L > 0) with no repair | B2, B4 (sympy) |
| FP1 | L4d | POSTULATED | the kernel is P2 (not nu_mono) | P2 = the framework's L1a; SPARC at fixed a0 prefers the nu_RAR shape by <= 0.01 dex rms (C2, reported) |
| FP1 | L4e | DERIVED | the RAR in P2's regime (galaxies, y <= 110): the core's law equals P2 | B1, B3, C1: filter correction <= 3e-5 even at xi = 1 pc |
| FP1 | L4f | DERIVED | Solar System (Cassini Q2, Saturn monopole, Earth/Mars ephemeris) under the double filter: pass for xi >= 0.029 / 0.032 pc (P2), 0.034 / 0.037 pc (nu_mono); the Saturn monopole binds | D0-D4 (g02 machinery, read-only) |
| FP1 | L4g | POSTULATED | xi, the heat filter's length | a new constant, floor-bounded by the Solar System (D2); not derived |
| FP1 | L4h | FAILS | the strict law (xi -> 0): Cassini Q2 4.0-7.6x the ceiling (P2 and nu_mono, both footings, 3 fields), the P2 tail 1279x / 1545x the Earth bound | D1: the filter, not the kernel, meets FP0's L1c constraint |
| FP1 | L1c' | DERIVED | FP0's L1c (the kernel must reach Newton faster than 1/(2y)) is discharged by the heat filter: P2 keeps alpha = 1 | D4: Earth and Mars anomalies below their bounds at the floor |
| FP1 | L4i | FAILS | the KiDS-EFE pincer inside the ungated core | E2-E4: no in-core knob moves the field in nu's argument; the core's own field fails KiDS; a free 2-halo does not help |
| FP1 | L4j | OPEN | a resolution of the KiDS-EFE pincer | E5: needs an LG-vs-isolated-lens field split the local law cannot make; a selection-aware field is not expected to supply it |
| FP1 | L4k | OPEN | beyond static order: 1PN metric (beta, alpha_1, alpha_2), causality of the leaf filter, Dirac count, cosmology | other lanes; ACTION.md's own warnings stand |
| FP2 | L3-FP2 | POSTULATED | root action for the relativistic lanes: the ungated C-H/K core (C-H + BPS khronon, beta = 0, leaf-averaged lambda-term, nu_mono) | coordinator's choice after the root-action map; the leaf average and alpha_c a^2, c_2 terms are chosen, not derived |
| FP2 | L5a | DERIVED | the heat filter in the linear theory: C_eff = e^{-xi^2 k^2} C, C_T = nu - 1, C_L = nu - 1 + y nu' | A2, sympy dsolve |
| FP2 | L5b | DERIVED | the core's quadratic action = L340's block; C-H sector instantaneous and shift-free | A1, symbolic second variation |
| FP2 | L7 | DERIVED | tensor speed c_T = 1 (GW170817) | A3: omega^2 = k^2, no C-H or khronon term in the TT sector |
| FP2 | L6a | DERIVED | PPN gamma = 1 | B3 (every C_eff); KM3 at 1PN |
| FP2 | L6b | DERIVED | PPN beta = 1 | KM3 P2 (inherited; the C-H sector is filtered off at 1 AU, B4) |
| FP2 | L6c | DERIVED | PPN alpha_3 = 0 | B3: the g_0j and g_00 readings of alpha_1 agree with the C-H sector live |
| FP2 | L6d | DERIVED | PPN alpha_1 = -4 alpha_c - 8 C_eff/(1+C_eff) | B3 closed form; B4 C-H part <= 1e-11 at 1 AU |
| FP2 | L6e | DERIVED | PPN alpha_2 (closed form, KM2 amplification inside) | B3; B2 reproduces Yagi+14 at C = 0 |
| FP2 | L6f | CONSTRAINT | alpha_c <= 3.2e-9 (|alpha_1| < 1e-5, |alpha_2| < 1.6e-9) | B4; alpha_c is a free coupling |
| FP2 | L8a | DERIVED | moving-source tracking (L330 gate): the omega -> 0 response is static MOND iff c_2 != 0 | C1, C2 |
| FP2 | L8b | DERIVED | health on the static MOND background needs the monotone kernel nu_mono | C3 (Krein, frozen coefficients) |
| FP2 | L8c | CONSTRAINT | tracking floor c_2 >= 7.29e-3 (3 x 600 km/s where C <= 100) | C4 |
| FP2 | L9a | DERIVED | Planck-era cap on c_2 vs the tracking floor: the leaf-averaged lambda-term is c_2-inert in linear cosmology (G_eff/G_cos = 1/(1 - alpha_c/2), no slip); the published caps do not apply | D1-D3 (linear equations, MOND sector off in the web); a Boltzmann-level fit is owed |
| FP2 | L9b | OPEN | c_2 upper edge (BBN 0.067 in L340) -- removed with G_cos = G; no ceiling found at linear order | D3; strong coupling / nonlinear khronon not checked here |
| FP2 | L9c | FAILS | the ungated core's own linear cosmology (C -> oo at zero gradient) | D4 + L341 (sigma_8 18-27, inherited); needs the vacuum gate -- independent of c_2 |
| FP2 | L10 | OPEN | nonlinear well-posedness, strong coupling of the full core | XC1-XC3 scoped it; not re-derived here |
| FP3 | G1a | DERIVED | FRW background of the core (leaf average): Friedmann = GR, G_cos = G | A1 sympy minisuperspace; A2 control |
| FP3 | G1b | DERIVED | a0 absent from the background; a0(z)/a0(0) = 1 (canonical reading) | A3; both footings |
| FP3 | G1c | POSTULATED | the dark mass on FRW: cold, w = 0, Omega_c | declared field initial data (FP4 owns it) |
| FP3 | G1d | DERIVED | the core's MOND energy around FRW: O(eps^(3/2)), infinite zero-field tangent | B1 sympy; FP5's pinned U |
| FP3 | G1e | FAILS | ungated core in linear cosmology: sigma_8 18-27 | B2 (L341 reproduced), B3 at FP0's footings |
| FP3 | G1f | DERIVED | well-posed on FRW iff the gated tangent W C_T < (2 - alpha_c)/alpha_c | C0 on FP5's committed E(C) |
| FP3 | G1g | DERIVED | a local gate has a non-negative second variation iff it is concave; leaf averages add none | C1 static symbol + local pressure + leaf-average lemma |
| FP3 | G1h | CONSTRAINT | sigma_8 within 2% caps the web's MOND on-fraction at ~2e-3 (3e-2 if spent at z <= 0.5) | C2, L341 yardstick, both footings |
| FP3 | G1i | DERIVED | chord bound: a stable local gate's on-fraction <= (rho/rho_bar) x its web value | C3 theorem |
| FP3 | G1j | POSTULATED | the concave gate W = w(rho_dyn/rho_*(<K>_h)): the form and rho_* | chosen inside the class G1g allows; rho_* bounded by C2-C4 |
| FP3 | G1k | DERIVED | sigma_8 within 2% with the flagship on (M_b <= 1e11, z <= 2.5) or the dwarf RAR tail; stable, unique | C4a-C4d (D1, D3), given G1j |
| FP3 | G1l | FAILS | L* outskirts (1e11 beyond ~70 kpc), 1e12 at the flagship radius, KiDS 1 Mpc, galaxies at z >~ 4 | C4b/C4b'/C4e: the chord bound spends the sigma_8 budget |
| FP3 | G1m | OPEN | the z = 2.5-3 IGM under the concave gate (force boost 11-28% for D1) | C4e; a P1D run owed; likely fails |
| FP3 | G1n | FAILS | the concave gate's MOND tangent on FRW (FP5 strict) | C4f: W(FRW) > 0; the band y < y* shrinks, survives |
| FP3 | G1o | DERIVED | leaf-average global factor: no local second variation | C1 lemma, C8a |
| FP3 | G1p | FAILS | convex local ramp (the proposal; p = 1, x_c = 2.5 declared) | C8c anti-pressure; C8d RAR without plateau |
| FP3 | G1q | FAILS | tracking (khronon c_s) as the switch | C6: sigma_8 vs KM2's moving-source pole |
| FP3 | G1r | FAILS | K-floor with backreaction | C7: delta K/K = O((s/kappa)^4) |
| FP3 | G1s | FAILS | G-1 by any local gate on the MOND energy | T: FP5 x second variation x data trilemma |
| FP3 | G1t | OPEN | a MOND term with ZERO zero-field tangent on a field with its own inertia (AQUAL-type, O(eps^3)) | B1 + C0: meets FP5 by order counting with no gate; not in the core (its kernel reads the constrained U) |
| FP4 | L10a | FAILS | the dark mass and the clusters' missing mass as a STATE of the core's own fields (g, tau, U, W, L, lambda_0) | A1-A5: the clock has no charge and one gapless mode; the auxiliaries are constrained; the metric's PBHs fail the gates |
| FP4 | L10b | DERIVED | the clock carries no conserved charge (n.dn/d(d tau) = 0; FRW action independent of tau-dot) | check A1 |
| FP4 | L10c | DERIVED | U, W, L, lambda_0 are constrained (zero kinetic Hessian with lapse and shift) | check A2 |
| FP4 | L10d | DERIVED | the clock's one mode: omega^2 = c_2 k^2/(C(2 + 3c_2)); its quanta are radiation (p = rho/3) at >= 1800 km/s | check A3 |
| FP4 | L10e | FAILS | the metric's cold state (primordial black holes): sources u, cannot be kicked; fails X-COP, galaxies, flagship | check A4 |
| FP4 | L10f | POSTULATED | the minimal addition: one nearly free complex scalar (2 real d.o.f.) + one mass m >= 1.9-5.2e-19 eV; amount = initial data | check A5 (XR8, FL1, L383) |
| FP4 | L10g | DERIVED | reciprocity: a dark coupling V(I) multiplies the phantom by (1 - delta) where the dark state sits | check B1 |
| FP4 | L10h | FAILS | a coupling to the clock's acceleration reads the multiplier Phi: the constraint turns singular at O(1) strength | check B2 |
| FP4 | L10i | FITTED | a coupling to the clock's K is spatially blind in bound regions; the kick speed is the splitting eps/m^2 = v^2/(2c^2 - v^2) | check B3 (FK1's eps = 1.84-2.35e-6, set by the 575-650 window) |
| FP4 | L10j | DERIVED | the kick velocity scale from the action: only a ceiling, v_cap(r_t) = 2 sqrt(delta) (G M_b a0)^(1/2)/v_d ~ (G M_b a0)^(1/4) at delta = 1 on real z = 2.5 halos, host-proportional | checks B4, B5 |
| FP4 | L10k | FAILS | clearing galaxies with the core's own energy: needs delta > 1 (phantom reversed) and is anti-selective (clusters first) | check B5 |
| FP4 | L10l | FITTED | the ~600 km/s window: not predicted; (G M a0)^(1/4) in it only for a 0.28-dex band near 1e13 Msun (a selection) | check B6 |
| FP4 | L10m | FAILS | the derived mechanism on the gates (delta = 1, with the reciprocal term): the kept halos switch their phantoms off, so it passes what LCDM passes (z = 0 galaxies, X-COP in the natural reading, cosmic shear, forest, S_8, Harvey by proxy; KiDS in the upper bound without the term) and fails the framework's distinctive flagship at z = 2.5 in every reading | checks C1-C7 |
| FP4 | L10n | FAILS | the knife-edge: the derived kick neither lands in 575-675 nor widens the window | check K1 |
| FP4 | L10o | OPEN | derivative/current couplings of the dark state to the core; an acceleration-gated conversion rate's own reciprocal distortion; the varied region gate's onset (V0, obstructed: CV3/DE12/DE13) | not computed here |
| FP5 | G-2a | DERIVED | canonical count of the ungated C-H/K core: 2 tensor + 1 khronon scalar, 0 vector (N = 3) | A1-A3 (primary structure, second-class auxiliaries, Dirac bookkeeping) + B1 (deg det, frozen principal order) |
| FP5 | G-2b | DERIVED | the nonlocal heat filter (W, L, lambda_0) adds no mode, no free data, no first-class constraint | A3 (kernel-independent heat determinant) + B2 (Schur complement = sigma_n^2 C) |
| FP5 | G-2c | DERIVED | leaf average: lambda = 1 + c_2 on k != 0, GR on k = 0; Legendre map invertible on every mode | A2, K3 |
| FP5 | G-2d | DERIVED | no ghost (c_2 > 0) and c_T = 1 | B3 |
| FP5 | G-2e | DERIVED | gradient stability on the nonzero-field branch: 0 < E < 2 above g* = y* a0 (y* ~ (alpha_c/2)^2) | C1 |
| FP5 | G-2f | FAILS | well-posed linearisation at an open zero-field region (the ungated core's own FRW) | C2 (U pinned) + C3 (alpha_eff = 2 + alpha_c > 2: Hadamard ill-posed); amplitude saturates at y ~ y* (C4) |
| FP5 | G-2g | OPEN | nonlinear strong hyperbolicity of GR + BPS khronon (alpha_c > 0, beta = 0, lambda = 1 + c_2) | C5 settles the linear frozen symbol only |
| FP5 | L2b | POSTULATED | a0 as a field: a0 tied to Lambda by the core's own dynamics | D1-D5: no term links them; a free a0-field is flat on FRW and kills MOND in galaxies; K = 3H gives the dead rival |
| FP5 | L0c | FITTED | kappa = 1/2 (Lambda/alpha^2 = 32 pi) | D5; k01-k03 |
| FP5 | K-xi | CONSTRAINT | filter length xi | E: Solar-System floors 0.031/0.045 pc canonical, <= ~100 pc |
| FP5 | K-ac | CONSTRAINT | khronon alpha_c | E: [9.6e-14, 3.2e-9] |
| FP5 | K-c2 | OPEN | khronon c_2 (tracking floor vs Planck-era ceilings on perturbations) | E: L340 vs L350 |
| FP5 | K-dark | OPEN | dark mass as a state of the core's fields | D1: absent from the core |
| FP6 | G6a | DERIVED | the band-pass as an action: C-H's heat branch read at two diffusion times; linear theory C_eff = C (e^{-xi^2k^2/2} - e^{-L^2k^2/2})^2; no mode added | S1 (exact elimination), S2 (Schur, kernel-free det) |
| FP6 | G6b | DERIVED | (b) and (e) escape FP3's lemma: no multiplier on the MOND energy, no W''(dX)^2 term; health = monotone phantom (C_T, C_L >= 0) x h^2 | S3, S4; the energy-multiplied cut-off control carries c'' |
| FP6 | G6c | DERIVED | FRW linearisation per class: ungated and band-pass-alone ill-posed; (e1) well-posed iff y_r > 2.6e-18; cut-off classes exactly GR + BPS on FRW (G_eff = G/(1 - alpha_c/2), no slip) | S5 on FP2's committed block; S6 order counting |
| FP6 | G6d | FAILS | class (e) alone (any kernel of the local field and the epoch): linear growth | E2-E3: the web's field at z = 0.25 lies in KiDS/SPARC's range; the most generous kernel gives sigma_8 >= 1.15 |
| FP6 | G6e | DERIVED | (b) Gauss compensation: every isolated system weighs its baryons beyond ~2L | B1 (the record's L352 edge: the band-passed input vanishes beyond ~L, the output filter keeps the monopole zero) |
| FP6 | G6f | DERIVED | (b) late-time growth: sigma_8 <= 1.05 needs L shrinking as Omega_L^(n/2), n >= 2 | B2 |
| FP6 | G6g | FAILS | (b) alone: the forest (z = 2-3) against the 1e11 flagship (z = 2.5) | B3-B4: 1/k_F ~ 28 kpc < L_flag ~ 50 kpc -- a scale overlap no L(z) removes |
| FP6 | G6h | FAILS | (b): the KiDS-LG pincer | B5-B6: transformed from the EFE into the truncation scale (the LG needs L(0.25) ~ 0.5 Mpc, KiDS >= ~1.2 Mpc); not resolved |
| FP6 | G6i | POSTULATED | the combination (H): band-passed argument + running field floor, both through Omega_L(<K>_h) | chosen after the survey; five declared constants (H4) |
| FP6 | G6j | DERIVED | (H) meets the linchpin: MOND tangent zero on FRW and E < 2 at every field, sigma_8 within 2%, forest proxy <= 10%, flagship <= 0.05 dex (to z ~ 3.0), SPARC and the Sun untouched, KiDS lead grade | H1-H2c, given G6i and its constants (forest a linear proxy, KiDS lead grade) |
| FP6 | G6k | FAILS | (H): the Local Group's zero-velocity radius (the pincer) | H3: R0 = 1.3-1.5 Mpc at every KiDS-passing cell |
| FP6 | G6l | POSTULATED | (H)'s constants L_Lambda, n, y_Lambda, p', m | declared; windows set by KiDS, the flagship, the forest and sigma_8 (H1) |
| FP6 | G6m | FAILS | classes (a), (c), (d): local multiplier gates | FP3's lemma (C1, C3, C5, C7, T), CV4; (d) S7: symbol zero wherever W' > 0 |
| FP6 | G6n | OPEN | (H) beyond linear order: the sub-L web keeps C_eff ~ 0.6 at k <= 0.5 h/Mpc and ~12 at 20 h/Mpc today (cosmic shear, halo masses); the flux P1D (PM); full KiDS (2-halo, and the isolated lenses' band-passed external field, estimated <~ 2e-4 a0 but not computed); the carrier in galaxies; nonlinear well-posedness of a Mpc-range leafwise filter | not computed here (no PM run in this lane) |

Totals: DERIVED 44, POSTULATED 13, FITTED 4, CONSTRAINT 6, OPEN 13, FAILS 22
