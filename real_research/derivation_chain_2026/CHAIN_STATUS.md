# The first-principles derivation chain -- status ledger

Assembled by `run_chain.py` on 2026-09-27 11:22. A lane counts only if its main run has a verdict and its MUTATE control flips (rc = 1). Status meanings: DERIVED (varied out of the chain above it, with a script), TIED (an input implemented as an exact action-level relation, coupling chosen), POSTULATED (an input), FITTED (a constant set by data), CONSTRAINT (a derived requirement on a lower link), OPEN (owed), FAILS (derived and contradicted by data).

## Lanes

| lane | checks | load-bearing failures | main rc | MUTATE rc | contract |
|---|---|---|---|---|---|
| FP0_core_postulates | 7/7 | 0 | 0 | 1 | ok |
| FP1_static_sector | 24/24 | 0 | 0 | 1 | ok |
| FP2_relativistic_consistency | 17/17 | 0 | 0 | 1 | ok |
| FP3_cosmology_linear | 27/28 | 0 | 0 | 1 | ok |
| FP4_kick_from_action | 24/25 | 0 | 0 | 1 | ok |
| FP5_dof_and_a0_field | 24/24 | 0 | 0 | 1 | ok |
| FP6_gate_survey | 31/32 | 0 | 0 | 1 | ok |
| FP7_aqual_type_repair | 23/24 | 0 | 0 | 1 | ok |
| FP8_current_coupling_kick | 22/22 | 0 | 0 | 1 | ok |
| FP9_web_galaxy_separator | 36/36 | 0 | 0 | 1 | ok |
| FP10_internal_splitting_dark_sector | 31/31 | 0 | 0 | 1 | ok |
| FP11_local_group_flyby | 22/22 | 0 | 0 | 1 | ok |
| FP12_local_volume_groups_r0 | 23/23 | 0 | 0 | 1 | ok |
| FP13_separator_from_state | 30/31 | 0 | 0 | 1 | ok |
| FP14_zero_knob_core | 27/27 | 0 | 0 | 1 | ok |
| FP15_zero_knob_dark_sector | 32/32 | 0 | 0 | 1 | ok |
| FP16_daughter_reaccretion | 31/33 | 0 | 0 | 1 | ok |
| FP17_screening_without_xi | 28/28 | 0 | 0 | 1 | ok |
| FP18_kids_vs_hubble_flow_data | 20/20 | 0 | 0 | 1 | ok |
| FP19_hs_repair | 24/24 | 0 | 0 | 1 | ok |
| FP20_esd_projection_fix | 12/12 | 0 | 0 | 1 | ok |
| FP21_isolated_spiral_lensing | 18/19 | 0 | 0 | 1 | ok |

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
| FP0 | L2a' | DERIVED | a0(z) ~ sqrt(rho_DE(z)) for evolving dark energy: -0.10 dex at z = 2.5 under DESI (vs the rival +0.58) | R3b, from P1 + the measured w(z); reproduces L273. Postulate level only: an ACTION-level field tie reads sqrt(V), V = (rho - p)/2, not sqrt(rho_DE) (XR20, a075ad7f7): +0.051 dex at z = 1, -0.034 at z = 2.5 under DESI DR2 + CMB + DESY5; DESI's w = -1 crossing needs a ghost; a healthy thawing field gives +0.07..+0.16 dex at z = 2.5; with a true Lambda a0 is flat |
| FP0 | L2b | TIED | a0 tied to Lambda inside the action | the Henneaux-Teitelboim unimodular multiplier (XR20, a075ad7f7): d Lambda = 0 is a field equation, so a0 = kappa c sqrt(G rho_Lambda) holds on every solution, no local mode (1 global DOF), FRW and PPN untouched; the coupling alpha(Lambda) = kappa sqrt(Lambda/8 pi) is chosen and kappa FITTED; a separate matter vacuum energy would shift the observed Lambda but not a0 (-0.023 dex at 0.1 rho_Lambda) |
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
| FP7 | R7a | POSTULATED | the repaired root: the core with C-H's U-sector replaced by (2 - alpha_c) h(2a - Dchi)Dchi - 2 alpha^2 J_P2(|Dphi|^2/alpha^2) + 2 lambda (n.dphi)^2, chi = S_h phi (khronon terms, leaf average, filter kept) | the coordinator's repair of FP3's G1t; the inertia's form is the suggested a0-free (n.dphi)^2 |
| FP7 | R7b | DERIVED | the chassis is forced: 2a^2 - (2 - alpha_c)|Dchi - a|^2 (no Newtonian term in phi's equation, GR + BPS Newtonian limit); C-H's sign pins its field to Newton (QUMOND) | A1 (sympy EL of the static density) |
| FP7 | R7c | DERIVED | the filter must sit on the chassis (chi = S phi): J on S phi needs S^{-1}; filtering both cancels | A1b (discrete adjoint + Fourier gains) |
| FP7 | R7d | DERIVED | static law: psi = Phi, Phi = Phi_N[G_N] + S phi, div(mu_s grad phi) = 4 pi G S rho (two-field AQUAL); P2 exact in spherical symmetry; C_T, C_L > 0; C^Q = 1/C^phi | A1, A2 |
| FP7 | R7e | DERIVED | thin exponential discs: AQUAL vs QUMOND <= 0.035 dex (y = 0.01-100, R >= 0.3 R_d), <= 0.008 dex after profiling Upsilon (SPARC median error 0.037 dex): not resolvable by SPARC | A3 (dual Kacanov; Plummer control) |
| FP7 | R7f | DERIVED | Solar System under the double filter: AQUAL floors 0.0243 / 0.0268 pc (Saturn monopole binds; QUMOND 0.0294/0.0316); strict law excluded by its a0/2 tail (1279x / 1545x) | A4 (dual AQUAL; g02 read-only; FP1 reproduced) |
| FP7 | R7g | DERIVED | FRW background = GR (chassis, J vanish; phibar-dot ~ a^-3, declared 0); a0 absent | B1 |
| FP7 | R7h | DERIVED | zero tangent: J is O(eps^3) around FRW and drops out of linear order | B2 |
| FP7 | R7i | DERIVED | zero-field well-posedness restored: omega^2 = 0 (marginal) + omega^2 > 0; E(C_phi) in (alpha_c, 2] (FP5's E > 2 band gone) | B3 (the naive chassis re-opens a growing band: MUTATE) |
| FP7 | R7j | DERIVED | linear cosmology: no slip; G_eff/G_N = 1 + (2/5)(ck/aH)^2/lambda_eff (matter era), inertia-limited; lambda_eff = lambda + (2+3c_2)/c_2 | B4 (sub-horizon reduction of the action's FRW equations) |
| FP7 | R7k | FAILS | sigma_8 with no gate: lambda_eff <= 277 gives L341's ~ 20x; sigma_8 <= 1.02 needs lambda_eff >= 1.1e+07 | B5 + T (linear and physical-amplitude yardsticks, both footings) |
| FP7 | R7l | DERIVED | strong coupling: Lambda_sc -> 0 at exact zero field; ell_sc <= ~1 mm in real backgrounds (tree level) | B6 (reported); the quantum zero-field question is OPEN |
| FP7 | R7m | DERIVED | stability: no ghost, no gradient instability for monotone J (T = diag(4(2+3c_2)/c_2, 4 lambda), det V ~ C_phi); FC-KH's (yq)' obstruction absent | C1, C2 |
| FP7 | R7n | DERIVED | tracking: omega -> 0 gives static MOND iff c_2 C_phi != 0; c_s^2 = C_phi/lambda_eff; lambda = 0 reproduces c_2 >= 7.29e-3 | C3 |
| FP7 | R7o | DERIVED | c_T = 1 (exact on flat space; ~1e-41 on MOND backgrounds) | D1 |
| FP7 | R7p | DERIVED | PPN: gamma = 1, alpha_3 = 0, closed-form alpha_1, alpha_2; filtered = khronometric; alpha_c <= 3.2e-9 unchanged; beta = 1 inherited | D2 (FP2's pipeline) |
| FP7 | R7q | DERIVED | mode count N = 4 (lambda > 0) / 3 (lambda = 0); the filter adds none | E1 |
| FP7 | R7r | DERIVED | the fourth mode is not harmful (fifth force, PPN, Cherenkov, GW170817): the spec's limit is a preference | E2 (reported) |
| FP7 | R7s | FAILS | lambda (the MOND scalar's inertia): sigma_8 needs >= 1e7, tracking <= 2.8e4: EMPTY | T |
| FP7 | R7t | OPEN | a web-vs-galaxy separation of the scalar's response (a new scale ~ Mpc in its inertia, or a density-read gate) | T; with the zero tangent a gate need not vanish on FRW, so FP3's convexity lemma no longer binds -- FP3's chord bound (L* outskirts, KiDS) does; untested |
| FP7 | R7u | OPEN | nonlinear well-posedness; the L340 H4 O(Phi/c^2) lobes for the new sector; KiDS-EFE with AQUAL's EFE; Boltzmann-level cosmology | not computed here |
| FP8 | L10o.1 | DERIVED | the task's current: J.n = n_d (clock-frame density), J^i = -n_d v^i | check A1 |
| FP8 | L10o.2 | DERIVED | gauge reduction: -|dPsi|^2 + gA.J == -|DPsi|^2 + g^2 A.A|Psi|^2; J.d chi is pure gauge at O(g) and FP4's density class at O(g^2); J.n f is an electrostatic density coupling | check A2 |
| FP8 | L10o.3 | DERIVED | kinetic couplings: -F(I) g^mn dPsi*dPsi is the density coupling V = c^2[(1+F)^(-1/2) - 1] (|F| = 2.0 x FK1's eps/m^2 for 575-650 km/s); spatial/anisotropic members change only the inertia | check A3 |
| FP8 | L10o.4 | DERIVED | THE ENERGY-RECIPROCITY IDENTITY: the energy any coupling takes from the MOND sector is -Int S.d_t grad u, S its source in the MOND equation; <= max(delta) x the MOND field energy | check A4 |
| FP8 | L10o.5 | DERIVED | exact back-reactions: S = -2 rho_d V' u'/a0^2 (density), 2 g (d_t n_d) u'/a0^2 (rate), -G' rho_d w^2 u'/a0^2 (inertia), g j (F + 2IF') (current) | check A5 |
| FP8 | L10o.6 | FAILS | class-wide: unbinding the flagship's dark mass costs 7.2-11.9x the host's whole MOND field energy (4.9-8.7x with the baryons' kinetic energy added): any MOND-powered clearing needs delta > 1 where the dark state sits (beyond H4's health boundary) | check B0 |
| FP8 | L10o.7 | FAILS | linear spatial-current (magnetic) couplings: no work in a static host; the re-direction floor fails the flagship | check B1 |
| FP8 | L10o.8 | FAILS | velocity-weighted couplings at FP4's delta = 1 cap (density, inertia, anisotropic inertia): fail the flagship in the slow and sudden readings, both footings | check B2 (B3: an unattainable pericentre-timed envelope with FP4's cap clears 3 of 18 member-host cells (['inertia']); with the health-enforced cap: 0) |
| FP8 | L10o.9 | FAILS | ordering: every MOND-sector coupling clears clusters before z = 2.5 galaxies (anti-selective) | check B4 |
| FP8 | L10o.10 | FAILS | the rate member g J_perp.grad chi == -g n_d d_t chi: silent in static halos (escapes the static reciprocity), right ordering by growth rate, but delta >= B0's ratio during the clearing (ill-posed core); clock-frame dependent | checks A5, B5, H4 |
| FP8 | L10o.11 | FITTED | velocity scale: host-proportional ceilings or a fitted strength per member; the 575-675 km/s window not predicted | check B6 |
| FP8 | L10o.12 | DERIVED | health: current members luminal (tachyonic beyond g|A| = m); every velocity-weighted kicker is superluminal (the weighting theorem); all I-members off on FRW | checks H1-H3 |
| FP8 | L10o.13 | DERIVED | FP4's ceiling delta = 1 is the core's own health boundary: FP5's (N, U) determinant vanishes at delta* = 1 + O(1e-9) | check H4 |
| FP8 | L10o.14 | FAILS | the best healthy coupling (-F(I) g^mn dPsi*dPsi) = FP4's density class: passes what LCDM passes, fails the flagship | check G1 (FP4's committed rows) |
| FP8 | L10o.15 | FITTED | the honest minimal price of a working kick: FK1's eps (FITTED, eps/m^2 = 1.84-2.35e-6 for 575-650 km/s: energy from the dark field's own splitting, S = 0) + its trigger's constants (the conversion coupling and gate exponent q, DECLARED) + the initial misalignment (initial data) + m | FK1 (committed); this lane's no-go for every MOND-sector source |
| FP8 | L10o.16 | OPEN | not scored here: zero-net redistributors in a GROWING host (betatron-like magnetic members, sign-changing weights) beyond B1's static floor; velocity couplings nonlinear in Psi (outside the low-order class; ill-defined for a multistreaming wave field); the superluminal members' KiDS / cosmic-shear / forest / Harvey rows (moot: their flagship and X-COP fail); the rate member's residual clock-frame dipole under khronon tracking | not computed |
| FP9 | R9a | DERIVED | the band-pass sits on the chassis, chi = (S_xi - S_L) phi (J on B phi needs 1/h^2, unbounded at both ends) | A1 (discrete adjoint + Fourier gains) |
| FP9 | R9b | DERIVED | band-passed AQUAL block: roots >= 0, det V = 16 C_phi k^4 (2 - a_c)/a_c for every h, E in [a_c, 2] | A2 (this lane's re-derivation of FP7 B3, reproduced exactly: K2) |
| FP9 | R9c | DERIVED | at lambda = 0 the formal linear response is h-independent (the khronon carries the mode); the band-pass acts through J's amplitude or lambda > 0 | A3 (FP7's slow root and static law, sigma -> h) |
| FP9 | R9d | FAILS | route (i), the band-pass alone: sigma_8, flagship, SPARC, KiDS pass; the forest FAILS (scale overlap survives the repair) | I1-I6 (both footings, both modes, inertia at the tracking edge) |
| FP9 | R9e | DERIVED | the yield floor J_Y = J_P2 + 2 y_th sqrt(Y): unique statics, C_T > 0, C_L >= 0; lowest order of J; no shape constant | Y1, Y4 |
| FP9 | R9f | DERIVED | the yield is admissible on the AQUAL root (E -> 2 marginal) and not on the QUMOND core (E -> 2 + a_c) | Y2 |
| FP9 | R9g | DERIVED | FRW with the yield: phi frozen, GR + BPS at linear order, linear yardstick = 1; lambda = 0 allowed | Y3 |
| FP9 | R9h | POSTULATED | the separator (H_Y): band-pass (L_Lambda, n) + yield (y_Lambda, p'), both through Omega_L(<K>_h) | chosen after the survey: the fewest declared constants found |
| FP9 | R9i | DERIVED | (H_Y) meets sigma_8 (phys; linear = 1), forest (linear proxy), flagship, SPARC, KiDS (lead grade), E in the BPS window | H1-H2b, given R9h (forest a proxy, KiDS lead grade) |
| FP9 | R9j | CONSTRAINT | (H_Y)'s constant windows: L(0.25) >= ~1.2 Mpc; y_th(0.25) <~ 3e-6; 4e-3 <~ y_th(2.5) <~ 0.03 | H1, H4 |
| FP9 | R9k | FAILS | (H_Y): the Local Group's zero-velocity radius (the KiDS-LG pincer) | H3: R0 = 1.4-1.5 Mpc at every KiDS-passing cell |
| FP9 | R9l | FAILS | route (ii), a concave density gate on the AQUAL block: stable iff concave; KiDS needs f(0.25) >~ 0.65, the flagship f(2.5) >~ 3.6e-3: its 2-constant running gives sigma_8 ~ 1.09; a step history (>= 3 constants) gives 1.04 with G_eff ~ 3 on all scales at z <~ 0.3 | D1-D6 (chord bound x AQUAL sensitivity; the step's failure is the linear-scale lensing amplitude) |
| FP9 | R9m | FAILS | route (iii): no host-independent Mpc length from (a0, Lambda, G, c); Yukawa: sigma_8 vs KiDS screening; lambda(k): forest vs tracking | V1-V3 |
| FP9 | R9n | POSTULATED | the four constants of (H_Y) | declared inside R9j's windows; none derived |
| FP9 | R9o | OPEN | beyond linear order: the sub-L web (linear P boost at k >= 0.3 h/Mpc; cosmic shear/S8, halo masses), dense z ~ 2 IGM lumps above the yield (flux P1D), full KiDS (2-halo, lens-redshift spread), the running yield's z ~ 2.8 switch-off, non-analytic zero-field EFT | H2c (reported); no PM run in this lane |
| FP10 | L11a | POSTULATED | the dark sector's action: S_Psi with eps Re(Phi^2) + lambda(K)(Im Phi^2)^2 on one complex field (FK1 + FL2), L353's pair for kernel invisibility | FK1/FL2 (committed); FP4 L10f |
| FP10 | L11b | DERIVED | masses m_H^2 - m_L^2 = 2 eps, Z2 x Z2, kick v_k = sqrt(2 eps/(m^2 + eps)), latent heat v_k^2/2 | check A1 |
| FP10 | L11c | DERIVED | S = 0: the dark action does not touch the MOND sector; the kick's energy is the rest-energy difference; energy selectivity (galaxies before clusters) | check A2 (FP8's B0 costs) |
| FP10 | L11d | DERIVED | pair vertex lambda/(4 m_H m_L), G = lambda n_H/(2 m_H m_L), growth sqrt(G^2 - D^2) | check A3 |
| FP10 | L11e | DERIVED | Hubble sweep pi G^2/(4 H Delta); trigger n_t ~ H^(2q + 1/2); no spontaneous background conversion for q = 7/4 | check A4 |
| FP10 | L11f | DERIVED | the halo gain: gamma = sqrt(pi) G^2/(m v_k sigma), S_c = (2/sqrt(pi)) H Int (rho/rho_t)^2 e^{-(Dv/sigma)^2} dl/sigma (the design's C = sqrt(pi)) | check A5 |
| FP10 | L11g | DERIVED | where/when: fronts at >= 0.95 r200 for z <= 2.5; not mass-selective; one-shot at each progenitor's collapse | checks A6, A7 |
| FP10 | L11h | FITTED | the splitting eps/m^2 = 1.84-2.35e-6 | checks C1-C3 (kappa^19 = numerology) |
| FP10 | L11i | POSTULATED | the trigger's lambda_0 and q (values re-used from the switch's x_c0, p) | check C4 |
| FP10 | L11j | DERIVED | the flagship z = 0.5-2.5 in FK1's history reading (<= 0.074 dex); fails in place with the intact well at M_b 1e11 | check B1 |
| FP10 | L11k | DERIVED | z = 0 galaxies, KiDS, S_8 (ratio >= 0.922) | checks B2, B4, B6 |
| FP10 | L11l | FAILS | X-COP and cosmic shear IN PLACE (AT3's machinery): one splitting keeps clusters' carrier | checks B3, B8 |
| FP10 | L11m | OPEN | X-COP, cosmic shear and Harvey in the optimistic history reading / the PM proxy | checks B3, B5, B8 (reading-dependent; FK1's own particle-mesh run decides) |
| FP10 | L11n | OPEN | the forest (budget >= 4x AT2's; projection straddles 10%) | check B7 |
| FP10 | L11o | OPEN | the web (seeded stimulation, super-threshold filaments) and the escaped daughters' re-accretion into r_F | check A8; B1's reading |
| FP11 | F11a | DERIVED | the MW-M31 two-body force of the chain's static law (FP7 root, FP9 H_Y): Newton + each body's isolated band-passed phantom + the interaction field P(1 - S_L)[X(g1 + g2) - X(g1) - X(g2)] | K3: kernel = FP6's phantom, momentum conserved, deep limit = Milgrom's two-body formula, test-particle limit; K4 multipoles |
| FP11 | F11b | DERIVED | (H_Y) switches the pair's MOND off at early times (running yield) and truncates it beyond ~2L(z) (band-pass); the pair coasts until the MOND switch-on | the force tables (T) and the matched orbits (O); XR13's 'Newtonian pair' and 'M*' bracket this law |
| FP11 | F11c | DERIVED | the timing: (H_Y) reaches -109.3 km/s on the FIRST approach at M_b = 1.65e+11 / 1.37e+11 (can/alt, conv. A), inside the baryonic window: a flyby is NOT required | T1 (conv. A = the chain's point masses + Lambda from the Hubble flow; B and C in T3; sensitivity T5) |
| FP11 | F11d | DERIVED | a past MW-M31 flyby is EXCLUDED by (H_Y): no approaching branch with a past pericentre for M_b <= 1e+12; with v_t = 17-82 km/s the last apocentre 962-1017 kpc, 3.5-4.8 Gyr ago; the first pericentre 3.5-3.8 Gyr ahead at 26-189 kpc | T2, O1 (2-D, J conserved from today) |
| FP11 | F11e | FAILS | the plain root law (no separator) has no timing solution at the LG's baryonic mass: its first approach is too fast; the plain law's flyby needs M_b = 3.32e+11-5.60e+11 = 1.9-3.2x the nominal baryons; the MOND-literature flyby (Zhao+2013) is reproduced with a0 = 1.2e-10 and their interpolation | T4, K6, O2 |
| FP11 | F11f | POSTULATED | dynamical friction and flyby energy loss set to zero (no halos in the galaxy sector; the (H_Y) orbit has no past pericentre) | scope; stellar friction at the future pericentre is not computed |
| FP11 | F11g | POSTULATED | the timing idealisation: point masses from the Hubble flow at a = 0.02 (the chain's XR4 convention), J treated as conserved from today | T3 / T5 measure how far the background term, the carrier and the start epoch move it |
| FP11 | F11h | FAILS | R0 at the timing-matched mass: HY/A/canonical 1.53, HY/A/alt 1.52, HY/B/canonical 1.57 Mpc vs 0.96 +- 0.03 -- the timing pins M_b a0, and with it R0 | R1, R2, R4 |
| FP11 | F11i | FAILS | a flyby does not resolve the R0 overshoot: none exists in (H_Y), and the only matched flyby (the plain law, at its larger timing mass) has a larger R0; the flyby's own effect on R0 is small | R3 |
| FP11 | F11j | CONSTRAINT | the KiDS-LG pincer at the timing mass: the LG would need e = 2.4e-03-3.6e-03 a0 in the kernel; KiDS tolerates <= 3.7e-04-5.2e-04 (2-halo); (H_Y)'s band-pass passes no uniform field | P1 (FP1 E3's tolerances, committed) |
| FP11 | F11k | DERIVED | the flagship, SPARC, KiDS (and sigma_8, forest) gates are unchanged -- no action term was added | G1, K7 |
| FP11 | F11l | FAILS | the LG alone, timing imposed: lengths L(0.25) passing timing + R0: canonical: none, alt: none (canonical scan 0.6-1.3 Mpc, alt at 1.3); KiDS needs L(0.25) >= ~1.2 Mpc | X1 (merged pair; yield, n unchanged) |
| FP11 | F11m | OPEN | open: the AQUAL-vs-QUMOND curl part of the two-body force (near pericentre only), the neighbours' tidal field (M81, Cen A, IC 342), the CGM's baryons (raise M_b, R0 and the timing speed), a 3-D fit of the full local Hubble flow, and an LG-scale action term that separates the pair's mutual MOND (fixed by the timing) from the outer flow (R0) | scope; not computed here |
| FP12 | F12a | DERIVED | the chain's R0 of an isolated group ((H_Y)): M81 1.37/1.41, Cen A 1.35/1.39, M83 1.24/1.28, IC 342 1.38/1.43 Mpc (can/alt) at k02's baryons; d log R0/d log M_b = 0.19 | R1, K5 (FP11's tracer machinery = FP6's shells), K1-K3 (FP9/FP11 reproduced) |
| FP12 | F12b | POSTULATED | the groups as merged point masses on their own Hubble flow from a = 0.02, no neighbour tides; binary geometry <= +0.016 (FP11 R2); baryons = k02's UNGC accounting (0.6 L_K + 1.33 M_HI) with a band (Upsilon_K 0.5-1.0, aperture 0.7-1.5 Mpc, x1.4 unseen gas) | M1, K4 (k02 re-derived), K8 |
| FP12 | F12c | CONSTRAINT | the record's UNGC R0 of M81, Cen A, M83 and IC 342 (k02) are not measurements: they move by more than twice their bootstrap error under window / distance-quality changes; the published R0 (read at source) carry the test | S1 (and the record's XR4 N2, k_dimensional K3.2/K3.3) |
| FP12 | F12d | FAILS | the overshoot is NOT the Local Group's alone: M81 +0.19/+0.20, IC 342 +0.19/+0.20, the 14-group stack +0.12/+0.14 dex, like the LG's +0.20/+0.20 (FP11); LG, M81 and IC 342 share one offset (+0.200, chi^2 p = 0.93); with K&K 2018's own eq.-14 estimator on the model the stack reads +0.08/+0.10 and the same paper's LG +0.13/+0.15 dex (stack minus LG -0.048) | V1, V4, V5 |
| FP12 | F12e | DERIVED | Cen A is matched: -0.02/-0.00 dex alone, +0.02/+0.04 with M83's baryons -- the one group whose measured R0 is as large as the chain's | V2 |
| FP12 | F12f | FAILS | the verdict by the declared rule: MIXED (mean delta +0.140/+0.149, scatter 0.104/0.101 dex over LG, M81, Cen A, IC 342; common offset without Cen A +0.200, chi^2 p = 0.93; with it p = 1.4e-03) | V3, V4 (robustness: MIXED) |
| FP12 | F12g | CONSTRAINT | the universal fix needs the phantom beyond ~0.3 Mpc cut to f = 0.29-0.43 (all epochs), or no phantom before z_on = 0.14-0.22; KiDS d chi^2 at f = 0.3: +346/+340 (<= +9 allowed); SPARC's outer points move <= 4e-03 dex | U2 |
| FP12 | F12h | FAILS | no action-level term of the chain supplies it: L(0.25) -> 0.56 Mpc costs KiDS +263 (and FP9's SPARC gate 0.031 dex vs 0.01), y_th(0.25) -> 8.6e-05 costs KiDS +146 (can); with f = 0.3 the MW-M31 timing mass becomes 1.13e+12, 1.01e+12 (window <= 2.4e+11) | U1, U2, FP11 X1 |
| FP12 | F12i | FAILS | no universal outer profile fits Cen A and the rest: Cen A needs f in [0.88, 1.40], the others <= 0.46; the measured R0 are not a function of M_b alone | U3 |
| FP12 | F12j | OPEN | open: M83 has no published R0 (the chain predicts 1.24/1.28 Mpc); one estimator (eq. 14) refit around every group from the same catalogue; a two-body Cen A/M83 model (an LG analog); what separates Cen A (its binary, its off-sheet position, its mass budget); an action term that weakens the time-integrated pull on infall regions ~3x while KiDS's isolated lenses keep the full phantom | scope; not computed here |
| FP13 | R13a | DERIVED | no length from (a0, c, G, Lambda, hbar, m, xi) has an Mpc size at natural exponents AND the web's running (n_eff >= 2); FP9's n = 2 form needs a declared acceleration a0 Z^-3.38 | S1 (dimension census); S2 numerology rates |
| FP13 | R13b | POSTULATED | the state-length form: B[state] with <(S_B delta_m)^2>_h = s^2 -- the heat branch read out on the matter density; a leaf average (no local variation), closed on exact FRW | A1 |
| FP13 | R13c | DERIVED | n eliminated: the web's nonlinear scale runs as Omega_L^(n_eff/2), n_eff = 2.06 (actual field) / 2.66 (linear), inside FP9's [2, 2.7] | A2 |
| FP13 | R13d | CONSTRAINT | the threshold window: nonlinear reading s in ~[1.3, 2.6], linear ~[1.1, 1.65]; delta_c inside the nonlinear only; s = 1 excluded (sigma_8) | A3a-A3c, A6 |
| FP13 | R13e | FAILS | the dynamical readout (D_i a^i, phantom included): the separator feeds on its own phantom; no threshold window | A4 |
| FP13 | R13f | CONSTRAINT | the matter readout D_i(a^i - D^i chi) is required, and its feedback is mild (the headline is a fixed point) | A4, H3 |
| FP13 | R13g | FAILS | the MOND-sector energy, the unsmoothed variance and the heat relaxation depth set no web length of their own | A5 |
| FP13 | R13h | FAILS | the dark field's scales at m >= 1.9e-19 eV: sub-kpc, n_eff <= 0.65, kernel-invisible (no coupling) | B1 |
| FP13 | R13i | FAILS | p' as a power of any state measure: the yield's 3.1-decade rise exceeds every measure's (<= 1 decade) without a declared exponent and normalisation | C1 |
| FP13 | R13j | FAILS | y_th at the web's rms alone: 3-3.8 decades above KiDS's ceiling (KiDS +870..+1200, SPARC) | D1 |
| FP13 | R13k | POSTULATED | the state yield y_th = <|g_bp|^2>_h^(1/2)/a0 x max(0, 2q): the web's own rms while the leaf decelerates (c_y = 1, ramp) | C2, D2 |
| FP13 | R13l | DERIVED | (H_S) passes sigma_8, the forest proxy, the flagship, SPARC and KiDS on both footings and modes; E in the BPS window at every epoch | H1, H2, H3 |
| FP13 | R13m | CONSTRAINT | FP7's lambda > 0 is required at exact zero field (band-pass closed and yield zero on FRW); its value is free | A1 |
| FP13 | R13n | DERIVED | the MW-M31 timing with baryons only survives (H_S) on both footings | L1, K4 |
| FP13 | R13o | FAILS | the Local Group's R0 ~1.54 Mpc (edge 1.21): the state band-pass is longer today; the KiDS-LG pincer is untouched | L2 |
| FP13 | R13p | POSTULATED | the remaining choices: s = delta_c (a GR number applied to the actual field), c_y = 1, the q = 0 ramp -- natural, windowed, chosen after scoring | F |
| FP13 | R13q | OPEN | the nonlinear reading rests on halofit LCDM, not a PM run of this theory, and on halos staying LCDM-like (FP10's clearing thins them: the five gates hold to 20% of LCDM's one-halo power, the z = 0.4 lens check to ~45%: A7); lensing of lenses at z_l > 0.64 and galaxies below ~1e-2 a0 at 0.64 < z < 3 (new predictions); KiDS beyond lead grade (lens-z spread, 2-halo); the Local Group | A7, H4, H5, L2 |
| FP14 | F14a | DERIVED | lambda = 0 passes every gate FP7/FP9 scored: statics, Solar System, SPARC, KiDS, flagship, FRW, sigma_8 and forest (H_Y), health (one scalar), tracking (best), PPN (alpha_2's lag gone), c_T, N = 3 | L2, L4 (this lane's block; FP9's machinery) |
| FP14 | F14b | DERIVED | at lambda = 0 the action has the exact gauge symmetry phi -> phi + f(tau): FRW's phibar is gauge, FP7's declared 'phibar-dot = 0' is eliminated | L1 (generic ADM metric, FRW minisuperspace) |
| FP14 | F14c | CONSTRAINT | lambda = 0 needs FP9's yield at exact zero field (else phi = A_n/sigma: the backward heat operator) | L3 |
| FP14 | F14c' | DERIVED | at lambda = 0 the chassis field chi gains an equal-time response (zero at lambda > 0): Newtonian-strength, EFE-blind to O(alpha_c C_phi); the MOND enhancement still arrives only through the propagating pole | L4 (source response of the block; L318 criterion B admits it) |
| FP14 | F14d | DERIVED | no scored observable depends on alpha_c beyond O(alpha_c) <= 1.6e-09; the Solar-System alphas vanish as alpha_c -> 0; FP5's y* does not exist on the AQUAL root | A1 |
| FP14 | F14e | FAILS | alpha_c -> 0+: the UV khronon becomes instantaneous (rank change) and strongly coupled, k_sc ~ alpha_c^(3/4): alpha_c = 0 excluded | A2, A3 (XC1's formula, reproduced) |
| FP14 | F14f | POSTULATED | alpha_c is a REGULATOR in [alpha_sc, 3.2e-9] (alpha_sc = 3e-41 .. 8e-16 by the probe criterion): nonzero, value unobservable | A (verdict): a UV requirement, not a fitted constant |
| FP14 | F14g | OPEN | the L340 H4 O(Phi/c^2) lobe floor on alpha_c for the AQUAL root | A4 (L340's scaling: 7e-19..6e-11 over the xi window, inside it) |
| FP14 | F14h | DERIVED | c_2 -> oo is regular: -c_2 (K - <K>_h)^2 -> -2 mu (K - <K>_h); Minkowski (det = 2 lim det/c_2, T -> diag(12, 4 lambda), V unchanged, same count, second-class multiplier pair) and FRW (HS identity, Q = 0, mu finite, dust unchanged, G_eff = 1/(1 - alpha_c/2)) | C1, C1b (the MUTATE plain K^2 freezes the expansion) |
| FP14 | F14i | DERIVED | c_2 -> oo does NOT reproduce the York/CMC kill: a0 not tied to K, the scalar propagates (alpha_c keeps the lapse dynamical), the response's equal-time part is c_2-independent (no new instantaneous channel) and EFE-blind, G_eff = G_N, Cassini unchanged; the York-like limit is the double limit alpha_c -> 0, excluded by strong coupling | C2 |
| FP14 | F14j | DERIVED | in the limit: tracking 1,800 -> 17,309 km/s (C^Q = 100), outskirts alpha_2 v^2 11.7% -> 0.13%, sigma_8/forest (H_Y) unchanged (<= 7e-06), c_T = 1, k_sc finite | C3, C4 (the cubic mixing analysis at c_2 -> oo is OPEN) |
| FP14 | F14k | POSTULATED | the c_2 term replaced by the CMC constraint (c_2 eliminated) | C (verdict): the zero-knob choice of a regular limit |
| FP14 | F14k' | OPEN | not covered for the c_2 -> oo root: nonlinear well-posedness, the cubic strong-coupling analysis with metric mixing, and the khronon's binary-pulsar radiation at lambda_BPS -> oo (only the PPN bounds were scored) | scope; the same items are open at finite c_2 |
| FP14 | F14l | FAILS | xi from (a0, Lambda, G, c): only (c^2/a0)(8 pi/kappa^2)^e_L; O(1) coefficient = 31 Gpc; 6 integer-power hits in the window are numerology | X1 (sympy nullspace) |
| FP14 | F14m | FAILS | field-dependent xi(g) = (c^2/g)(a0/g)^s: galaxies (SPARC 0.275 dex, KiDS +1120), Solar System (readout-gradient force 3e+02x the ephemeris gate at the Earth for the lead; every s fails), FC-KH-type gradient instability | X2, X3, X3b |
| FP14 | F14n | FAILS | |Phi|-based xi: gauge-ambiguous and a floor/ceiling pincer (m <= 0.69 vs >= 1.42) | X4 (reported) |
| FP14 | F14o | FAILS | dropping the filter by a kernel change: healthy kernels keep >= 0.26 a0 at the planets (671x); Cassini Q2 is an EFE/transition statement (tail cuts < 3%); only unhealthy sharp kernels (P2_n n = 4) pass | X5 (theorem + FP1's Q2 integral) |
| FP14 | F14p | CONSTRAINT | xi is the gravity core's one remaining knob, bounded to [0.0243/0.0268 pc, ~100 pc] | X (verdict); FP7 A4 floors |
| FP14 | F14q | DERIVED | the core's count beyond (kappa, G, Lambda): 1 knob (xi) + 1 regulator (alpha_c); eliminated c_2, lambda, phibar-dot | F |
| FP15 | L15a | DERIVED | FK1's K-gate is (Omega_L(<K>_h)/Omega_L0)^q on CMC leaves: the trigger's running VARIABLE is the separator's own | check T1 |
| FP15 | L15b | DERIVED | the trigger's EXPONENT is not fixed by the action: three inequivalent identifications with FP9's p' (q = 3.75, 4, 4.75) | check T1 |
| FP15 | L15c | DERIVED | the anchor law: at a fixed z = 2.5 threshold, R(z) falls to z = 0 monotonically iff q >= 1/Omega_m0 - 1/4 = 2.94 | check T2 |
| FP15 | L15d | FAILS | sharing the exponent: every identification puts delta = 10 filaments above the trigger at every flagship anchor, and the cosmic mean at W2's (FP10's A4 fails): the web runaway made categorically worse | check T3 (T3c: S_8 below the strict 0.922 in both web brackets; X-COP/Harvey lose the optimistic reading) |
| FP15 | L15e | FITTED | q is set by data, not shared: at the dark-mass floor the forest needs q >= ~1.75 (canonical; 1.5 alt) and A4 q <~ 2.9; keeping delta = 10 filaments below the trigger needs q <~ 1.75 -- FK1's declared 7/4 is where the two meet; degenerate with zeta at z = 2.5 | check T3b |
| FP15 | L15f | FITTED | zeta = f_t (lambda_0's normalisation): pinned between the forest and the flagship (canonical band <= 1.25 wide at the floor mass, XR12's resolved reading); a decade on FP10's no-cap reading; no dimensionless map to y_Lambda | checks M1, M2, T3b |
| FP15 | L15g | DERIVED | the yield onset as the trigger (-lambda_0 g(Y)(Im Phi^2)^2): exactly off on FRW and in the z >= 2.5 IGM (phi frozen), so q is not needed -- its job is done by the separator's p' | check T4a |
| FP15 | L15h | POSTULATED | the yield-onset gate's form g (width tied to y_th) | check T4a |
| FP15 | L15i | CONSTRAINT | the yield-onset gate's reciprocal flux at the yield surface during conversion (delta_Y >> 1 at the floor; <= 0.1 needs a much heavier dark mass) | check T4b |
| FP15 | L15j | OPEN | the yield-onset cell on the gates: mass-selective budget, forest, S_8 and the flagship's later passage (T4c-T4d); the cluster gates keep FP10's reading-dependence | checks T4c, T4d, T5 |
| FP15 | L15k | DERIVED | eps is the only Z4-odd term (Phi -> i Phi): multiplicatively renormalised, generated by nothing present | check E1 |
| FP15 | L15l | DERIVED | no present coupling induces eps (pair, leaf average: 0; frame coupling: a relabelling; vacuum/Hubble scales: <= 1e-28 at the floor) | check E2 |
| FP15 | L15m | FITTED | eps/m^2 = 1.84-2.35e-6 set by the flagship (lower) and Harvey (upper); kappa^19 is numerology | checks E3, E4 |
| FP15 | L15n | FITTED | m: pinned near its floor on the canonical footing (the forest's minihalos vs the flagship's cap), open on alt; unpinned on FP10's no-cap reading | checks M1, M2 |
| FP15 | L15o | CONSTRAINT | m <~ 1 eV (Bose occupation of the pump) | check M3 |
| FP15 | L15p | OPEN | a mechanism for m (the ties m_P^a mu^(1-a) that land in the window are numerology) | check M5 |
| FP15 | L15q | POSTULATED | the amount (as LCDM's omega_c) and the misalignment (~16% prior): initial data | checks N1, N2 |
| FP15 | L15r | OPEN | XR19's seeded web runaway (FK1's band top is seed-stimulable at the mean for z <~ 0.5), the forest proxy's ~2x systematic, the own-density cap in FP10's reading, the chain's own spherical-collapse numbers (XR23) as a derived threshold, and a particle-mesh run with the trigger | scope; not computed here |
| FP15 | L15s | DERIVED | lambda_0's normalisation is not shared with the yield: a0^2 = kappa^2 c^2 G rho_Lambda maps y_th a0 to a density >= 5 decades too low; a0/(4 pi G L) needs a coefficient and runs as q = 3/4 | check T1b |
| FP15 | L15t | OPEN | the yield-onset gate on FP13's H_S: the web is MOND-on below z = 0.635, so zeta alone holds the late web; the q-running stays unnecessary; the flagship's passage comes earlier | check T4e |
| FP15 | L15u | FAILS | a dark trigger keyed to FP13's state with no new constant (the q-sign onset and/or the local nonlinearity at delta_c): the onset is global (flagship or background fail) and delta_c sits below the web's filaments (the web converts) | check T6 (a), (b) |
| FP15 | L15w | FAILS | sharing the threshold delta_t0 (XR19's dominant lever) with GR spherical collapse: the gates' band sits between the turnaround (9 pi^2/16) and the virial (18 pi^2) contrasts, and neither they nor 1 + delta_c land in it | check T6d (the chain's own collapse, XR23, is pending: OPEN in L15r) |
| FP15 | L15v | FAILS | the spherical-collapse partner Delta = 18 pi^2 as the trigger (no zeta, no q): web- and background-safe, fails the flagship's own-density cap on both footings and the forest (early z >= 4 conversion); the flagship passes only on FP10's no-cap reading | check T6 (c) |
| FP16 | L16a | DERIVED | the daughters' dynamics: Newtonian orbits in the expanding background (FP4/L353's kernel-invisible pair; FP10 A1's isotropic kick); peculiar speed ~ 1/a, comoving reach ~0.72-0.79 v_inf/H0 = 6.2-7.6 Mpc from any z_e = 2-6 | A1, C0c |
| FP16 | L16b | DERIVED | the ordering: the reach exceeds the Lagrangian radius of every host <= 1e13 Msun and sits well inside every cluster's >= 3e14 Msun -- galaxies lose their daughters, clusters keep them (turnover near 1e14) | A1 |
| FP16 | L16c | DERIVED | the emission: FK1's halo-collapse trigger sends out the cosmic share of every host's carrier (~0.45); the rest is bound in sub-halos or converts at the host's own front | A2, C0a |
| FP16 | L16d | POSTULATED | the semi-analytic model: spherical symmetry, one EPS MAH per mass (Correa; alpha = 0.8 for the flagship), the constrained mean outer profile with a 3-node environment ensemble, tangential kick j v_c (j 0.15-0.35) at turnaround, the barrier-shifted ST emission with host-sized halos excluded, window averaging -- biases in V2 | C0d, C0g, C0h |
| FP16 | L16e | FITTED | the PM emulation's M_eff = 1e11.90 Msun, fitted to the PM's global decay history (validation only) | C0f |
| FP16 | L16f | CONSTRAINT | the validation is PARTIAL: the model OVER-predicts the committed PM's retention in every bin (massive end +0.07 to +0.11 -- V1's 0.10 tolerance fell where |offset| > 0.10; 6e13-2.5e14 +0.17 to +0.40); the direction strengthens the cluster failures, so the PM-calibrated reading removes it; the PM's own massive halos fail X-COP (V4) | V1-V4 |
| FP16 | L16g | DERIVED | where the daughters go: clusters (M0 >= 4e14) hold 0.52-0.58 of their own escaped daughters inside r200 by z = 0; the flagship hosts <= 0.002; at z = 2.5 the escaped daughters are almost all in the field | R1, R2, R3 |
| FP16 | L16h | DERIVED | the flagship z = 0.5-2.5 with re-accretion: max |shift| 0.0439 dex (the residue is the host's own in-place conversion, not recaptured daughters); z = 0 galaxies, KiDS and S_8 pass | G1, G2, G4, G6 |
| FP16 | L16i | FAILS | X-COP with re-accretion at every kick 575-650 km/s, both footings, raw and PM-calibrated: the A2319-mass cluster keeps eps(R500) 0.91-0.93 -- FP10's optimistic reading (0.42-0.46) is excluded | G3 |
| FP16 | L16j | FAILS | cosmic shear at the 1.75 Mpc cap with the modelled retention (raw 1.33-1.43) | G7 |
| FP16 | L16k | FAILS | Harvey with re-accretion: 575 FAIL (fit +0.101), 650 FAIL (fit +0.141) -- hollow cores, loaded outskirts | G5 |
| FP16 | L16l | FAILS | the window with the modelled re-accretion: EMPTY (cells raw 0/8, PM-calibrated 0/8) | G9 |
| FP16 | L16m | CONSTRAINT | X-COP would need v_k ~1047 km/s (strict) / ~913 km/s (non-thermal) with re-accretion -- where L372's pincer (Harvey) and S_8 are unscored | G10 |
| FP16 | L16p | FAILS | with XR19's web channel (f_web from its F_tot: nominal, most conservative, turned-around shells) X-COP still fails the strict window: eps(R500) 0.82-0.92 raw, 0.74-0.80 PM-calibrated; the proto-cluster's own web daughters sit 0.21-0.27 inside R500 -- the Hubble-cooled population is recaptured.  Only the turned-around web + calibration corner enters L354's non-thermal window (turned 575, turned 600, turned 625, turned 650), where Harvey (halo-only) fails | G11, G11b |
| FP16 | L16n | OPEN | the forest (projection 0.027-0.136, not established); the web runaway (a daughter beam detunes after sigma/H ~ 0.1-0.3 Mpc, but most escaped mass exits resonant: a propagating front is neither forced nor excluded -- XR19) | G8, A3 |
| FP16 | L16o | OPEN | what the model cannot see: 3-D structure (filaments, mergers, centre offsets), the PM-calibrated offsets measured at z = 0 applied at z = 0.05-0.5, the web's own conversion (XR12/XR19) -- a PM run with FK1's trigger and re-accretion (XR21) decides | V2, X1 |
| FP17 | F17a | DERIVED | the strict law's Cassini Q2 is made at 1695-7280 AU (y_N 1.7-22, C <= 3e-12): the Sun at its own EFE transition, at the same y as galaxy interiors | M1 (f28's integrand, cumulative; FP14 X5 reproduced) |
| FP17 | F17b | DERIVED | at fixed y a local key sees only C ~ M^(1/2) (Buckingham); SPARC at the same y has C >= 4e-09: every Solar-System screening is a threshold MASS in [~1, ~2e+07] Msun | M2 (sympy nullspace; SPARC) |
| FP17 | F17c | FAILS | no O(1) mass from (a0, Lambda, G, c) in the window: M_H (8 pi/kappa^2)^D needs D in [-12.1, -8.5]; 4 integer hits and the Chandrasekhar-type 1.85 Msun (needs m_p) are NUMEROLOGY | M3 |
| FP17 | F17d | DERIVED | every constant-free construction puts the threshold mass at 1e20-1e22 Msun (galaxies screened); in-window rows carry a fitted length or are numerology | M4 |
| FP17 | F17e | FAILS | cubic Galileon, r_c = c/H_Lambda: r_V(1e11 Msun) = 502-1034 kpc (the '~70 kpc' is low), r_V/r_M >= 45: galaxies screened | V1 (sympy flux) |
| FP17 | F17f | FAILS | cubic Galileon on P2 (Route 2 on the AQUAL root): constant-free R_* screens SPARC; for ANY R_* the window is empty (>= 2e+06): P2's pole beats a 1/r Galileon flux | V2 (K5: Route 2 reproduced) |
| FP17 | F17g | FAILS | BDEF's Riemann Galileon on P2 beats the pole (interior force c^2 r/sqrt(8k)); with k^(1/4) = c/H it fails SPARC, KiDS and the flagship | V3, R1 |
| FP17 | F17h | CONSTRAINT | BDEF with k fitted: k^(1/4) >= 104 kpc (Saturn), SPARC to ~13 Mpc, GW170817 (estimate) <= ~379 kpc: a REPLACEMENT of xi, not an elimination | V4 (reported) |
| FP17 | F17i | OPEN | the tie k = L(0)^4 to FP9's separator length: Solar System and SPARC pass, GW170817 missed by the static-gradient c_T estimate | V4 (an estimate; the Paul term's c_T on a static gradient is not derived here) |
| FP17 | F17j | FAILS | de Broglie hbar/(m v) = 0.006-0.050 pc (verified); at FP10's kick speed <= 0.0175 pc, below the floor (monopole 1.9x) | B1 |
| FP17 | F17k | FAILS | xi_q = ((hbar/m)^2/a0)^(1/3) = 1.6-3.3 pc, the unique c-free length from (hbar/m, a0), inside the window: NUMEROLOGY (no action couples the heat depth to m); SHARED only by postulate | B2, B4, R2 |
| FP17 | F17l | FAILS | a readout keyed to the dark field's local coherence is absent where FP10 cleared the field (SPARC discs, dwarfs): MOND off, and S != 0 | B3 (FP10's retained fractions) |
| FP17 | F17m | FAILS | density (Ricci) keys: the planets' vacuum is no denser than a galaxy disc; the vacuum ratio needs a new small threshold | C1 |
| FP17 | F17n | FAILS | tidal (Weyl) keys need ell_* in [21, 238] kpc -- a new length | C2 |
| FP17 | F17o | DERIVED | a curvature-keyed readout depth: V_11 = 4k^2 (2 - alpha_c)(1 + u)^2/(2 - (2 - alpha_c)(1 + u)^2), u = K_2 k^2: unstable unless saturated (the FC-KH lesson at one more derivative) | C3 (sympy, FP14's block) |
| FP17 | F17p | OPEN | not derived here: the Paul term's c_T on static gradients, the Galileon-lapse mixing (FC-KH for R_0i0j couplings), BDEF's stability, a leaf-projected Galileon's second-order property | R1, V4 |
| FP17 | F17q | CONSTRAINT | xi remains the gravity core's one knob; physically it encodes the stellar mass scale (a0 xi^2/G in [0.4, 7e6] Msun) | F (verdict) |
| FP17 | F17r | OPEN | keys on the EXTERNAL field (outside theorem M): relational (Theorem 8), threshold FITTED in the record (ESCREEN), a local angle proxy is direction-dependent around the Sun; they screen every EFE-dominated system alike | C5 (reported, not pursued) |
| FP18 | F18a | DERIVED | the model-independent bound: for any non-negative spherical excess density Delta Sigma(R) <= M(<R)/(pi R^2), so KiDS's stacked lenses give M(<R) >= pi R^2 Delta Sigma(R) with no profile assumed (voids outside R change it by < 0.07 Msun/pc^2) | K7 (2000 random profiles), B1 |
| FP18 | F18b | CONSTRAINT | the published R0 errors omit the velocity scatter: K&K 2018's +-0.02 (stack) is their 5%-distance Monte Carlo (reproduced: +-0.025); the bootstrap of their own estimator on their own Table 7 gives +-0.12 (LG, Table 4: +-0.10); FP12's fit form V = H R [1 - (R0/R)^(1/2)] is not K&K's eq. (14) (it returns R0 = 0.72 on K&K's own table) | K4, E1 |
| FP18 | F18c | CONSTRAINT | at face value NO static spherical profile fits KiDS's isolated lenses (at the LV centrals' masses) and the LV Hubble flow: T = 102 (stack + LG, honest R0 errors; 370 with the quoted ones); every family fails, LCDM's NFW(+2h) included (KiDS-fitted profiles turn around at R0 = 1.65-2.26 Mpc vs 0.91-0.93); the velocities themselves reject the KiDS-implied flow at p ~ 6e-49; within R <= 0.3 Mpc the two agree (T = 2.4 / 3.1) -- the disagreement lives at 0.3-2.6 Mpc, where B21 flag photo-z isolation | B1, F1, F2, L1, H1, S, V1 |
| FP18 | F18d | FITTED | the comparability systematics (galaxy type, photo-z isolation leakage, stellar-mass scale, R0 method, eq. 4 coefficient, epoch/h), profiled jointly under declared priors, bring the joint T to 7.5 (2.3 sigma; inflated covariance 7.4; extreme corner 4.8); each alone leaves it >= 34 (S1); at the optimum M* -0.28 dex, R0 +0.077 dex, type -0.07 dex beyond the data-based factor, leakage -0.10 dex; the direct velocity test agrees (profiled p = 0.24) but only with a local H ~ 115 km/s/Mpc -- held at the flow's own point-mass value it gives p = 1e-02 | S1, S2, H1 |
| FP18 | F18e | OPEN | the verdict by the declared rule: UNDECIDED | V1, V2 |
| FP18 | F18f | CONSTRAINT | for the chain: at face value KiDS itself, read as a static Lagrangian profile, demands R0 = 1.65-2.26 Mpc for the stack / LG centrals -- above the chain's own 1.24/1.28 (stack) and 1.53/1.52 (LG) (FP12), so the chain's R0 overshoot is not a refutation of its outer profile by this pair; after the systematics the reconciled target is R0 ~ 1.03-1.13 Mpc with the LV centrals' lensing beyond 0.3 Mpc -0.54 to -0.48 dex from B21's published bins, of which -0.25 to -0.18 dex is the measured spiral-vs-mixed (red/blue) difference at fixed M* -- a type dependence the chain's universal law does not produce; the rest are measurement systematics that would move the chain's own KiDS target too | F2, S, D1, FP12 |
| FP18 | F18g | CONSTRAINT | the escape for a field (non-Lagrangian) theory: an outer pull weaker over the flow's history than its lensing today; with the stack's KiDS profile (Lagrangian R0 1.88, Eulerian-static 1.73) R0 = 0.93 needs the outer mass to switch on only after z_on = 0.14, later than KiDS's own lenses (<z> = 0.25) -- the same z_on FP12 found for the chain | D1, FP12 U2 |
| FP18 | F18h | OPEN | open: the deciding measurement is like-for-like -- the lensing Delta Sigma(0.3-1.5 Mpc) of spectroscopically isolated SPIRAL centrals at M_gal ~ 10^10.4-10.8 (the LV analogs; the record holds the KiDS-1000 shear catalogue and a re-measurement pipeline, reviews/lensing_rar/lr_esd_remeasure.py), and on the flow side R0 with its bootstrap error plus a group bulk-flow model for the companion velocities | S, H1 |
| FP18 | F18i | OPEN | the record's KiDS lead-grade projection (FP6 esd_of_M, used by FP6/FP9/FP11/FP12's KiDS numbers) under-projects: on a singular isothermal sphere it is -59% at 35 kpc, -10% at 0.3 Mpc, -5% at 0.76 Mpc, -14% at 2.6 Mpc (this lane's exact projection: < 0.5%); those lanes' KiDS chi2 are not re-scored here | K2, K2b |
| FP19 | FP13-A1 | FAILS | FP13 A1's claim that the leaf-averaged state term adds no local term to the field equations | corrected by XR18 N3 (53854a459): the O(V) leaf integral makes dS/d delta an O(1) local force with coefficient R_B ~ 7-8 at z <= 0.635; the psi-constraint symbol k^2(1 - R_B) changes sign on k = 0.12-1.62 h/Mpc |
| FP19 | R19a | DERIVED | a stationary depth (dS/dB = 0) removes the O(1) mean-field term exactly (envelope identity); the psi-constraint keeps its symbol; a rank-one global term remains, O(1/V) per plane wave (N^-3 on independent leaves), at a nondegenerate root | A1 (lattice; K3 reproduces XR18 N3b; recomputed band 0.12-1.62 h/Mpc, K2) |
| FP19 | R19b | FAILS | H_S's own action has no finite stationary B: dS/dB = V 4 pi G rho^2 I(B) > 0 at every B (opening the band-pass always adds MOND binding); its stationary points, the closed and the fully open band-pass, fail SPARC/KiDS and sigma_8; on exact FRW S is B-independent (degenerate) | A2, A3 |
| FP19 | R19c | FAILS | a zero-mode cost mu 4 pi G rho^2 B gives a finite stationary B with the state's late-time running, but mu ~ 50-92 is no natural number (delta_c traded for a fit), and the yield era closes the band-pass: the forest-flagship pincer leaves no (mu, y*) cell, FP13's yield and the tied yield fail too, the galaxies' own MOND rate is far too small (halo reading), and switching the cost off opens the web | A4, A5 |
| FP19 | R19d | CONSTRAINT | a Newtonian-order read of the nonlinear scale is destabilising wherever no yield is on (z <= z_q0): more variance -> longer L -> more MOND binding, with strength ~ the web's MOND response C^Q ~ 1/sqrt(y_web) ~ 10 -> R_B ~ 7 > 1 (for the variance read computed; for other nonlinear-scale reads the sign argument, not a computation) | K2, A1, A2 |
| FP19 | R19e | DERIVED | a zero-mode (<K>_h) read adds a mean-field term at k = 0 only: the plane-wave second variation is exactly the chassis's (lattice) and the global term is (v/c)^2-small where its size is defined (rho_extra/rho_bar <= 1.9e-05 Gaussian, <= 5.9e-08 halo with a yield; the no-yield halo sum does not converge in its mass cutoff, raw <= 5.0e-03) | B4, H3, H4, K4 |
| FP19 | R19f | DERIVED | no zero-mode derivation of the separator length: lengths from (a0, c, G, H) are c/H (a0/cH)^p; the n = 2 family's hits in the window [2.65, 4.6] Mpc are numerology (80% chance for kappa powers) | B1 (FP9 V1, FP13 S1) |
| FP19 | R19g | POSTULATED | the tied yield y_th = max(0, 2q) (<K>_h^2/3 - Lambda) L/alpha = max(0, 2q) 8 pi G rho_bar L/a0 (the Hamiltonian constraint's normalisation; per-mode window c_y in [0.7, 0.85, 1.0, 1.5, 2.0, 3.0, 5.0, 8.0, 9.0] x 4 pi G rho_bar L/a0) -- eliminates y_Lambda and p'; chosen after scoring: of four natural normalisations only this one passes both the per-mode gates and the real-space forest (the Poisson one fails the latter) | B3, H7 |
| FP19 | R19h | CONSTRAINT | L_Lambda in [2.65, 4.6] Mpc (sigma_8 <= 1.05 above, KiDS at z = 0.4 below; [2.65, 3.0] with sigma_8 <= 1.02); FP9's 2.46 is excluded by KiDS at z = 0.4 | B1, H6 |
| FP19 | R19i | DERIVED | H_K1 (L_Lambda = 2.9) passes sigma_8, the forest, the flagship, SPARC and KiDS at z = 0.25 and 0.4 on both footings and modes, E in the BPS window, and the psi-constraint symbol is positive for every k at z = 0-2.5 on both footings (lattice confirmed); the real-space operator's sigma_8 and forest pass too (Stein) | H1-H4, H7 |
| FP19 | R19j | CONSTRAINT | lambda > 0 is a regulator under H_K1 (the yield vanishes for z < z_q0, as under H_S; FP14's lambda = 0 elimination needs a yield at exact zero field) | structural; XR18 Q2 |
| FP19 | R19k | POSTULATED | n = 2 (the state's running, FP13 A2) and the q = 0 ramp (FP13 C2) | H6 |
| FP19 | R19l | OPEN | the forest beyond the linear proxy: the headline's yield (y_th(2.5) = 7.6e-03) turns MOND on in 0/27 of FP13's z = 2-3 IGM test lumps (H_S 0/27, H_K with y* = 0.013 0/27); KiDS for lenses at z_l > 0.64 (a prediction: large chi^2 at 0.7); the sub-L P boost and cosmic shear (PM); the Local Group's R0 (still failing); cold matter at the yield surfaces (XR18 B4b) at the headline's yield; the baryons-only reading (FP22; every number here is the all-matter reading); a khronon-shear read of the web's velocities (a (v/c)-suppressed candidate for the length, not computed here) | H5; XR18; XR21 |
| FP19 | R19n | CONSTRAINT | the separator's yield must sit above the real-space band-passed rms field at z = 2-3, not just the per-mode fields: FP9's rule is optimistic there (XR21); the Stein yardstick sets c_y >~ 1.3 for the tied yield, and b_real/b_per-mode < 1 for sigma_8 (this lane's Stein vs XR21's box printed) | H7, B3; XR21 stage 1 (ea9eeea08) |
| FP19 | R19m | FITTED | kappa = 1/2 (Z = 5.7888): the only accepted fitted input; not derived here | FP0 |
| FP20 | F20a | DERIVED | the correct KiDS projection: Delta Sigma(R) = M_2D(<R)/(pi R^2) - Sigma(R) with exact uniform-shell kernels (the 1/sqrt end point integrated analytically, the inner projected mass carried exactly, the mass inside the first node kept); it reproduces the SIS, NFW (Wright & Brainerd 2000), a point mass and the P2 lanes' cored/hollow carrier templates to < 0.1% (< 0.2% where the input has jumps) | V1, V1b |
| FP20 | F20b | FAILS | the record's P1 projection (FP6 esd_of_M = FP1 E's [FP14/FP17] = L355's [L357/AT1/AT3] = BS2's) is accurate | corrected by FP20: -59% at 35 kpc on the SIS, -3..-14% at 0.3-2.6 Mpc; defect A (inner disc pi R_0^2 Sig(R_0), R_0 = 20 kpc) + defect B (trapezoid over the 1/sqrt end point); no truncation defect (V2, B1) |
| FP20 | F20c | FAILS | L352's P2 projection (L352/L359/L360, AT3's gate, FP4/FP10/FP15/FP16 via kids_switched, DE8/DE10, XR9/XR14) is accurate | corrected by FP20: -3% (SIS) to +11% (NFW) on halos, up to +187% / -123% at 35 kpc on cored / hollowed carrier templates (V4, V1b) |
| FP20 | F20d | DERIVED | FP6's (H) headline passes KiDS (<= +9): d chi^2 -1.0/-3.2 -> -1.5/-0.6 | corrected by FP20 (R1: FP6 re-run whole; its only check that flips is K2, the control pinned to L341 F7's buggy 118.0) |
| FP20 | F20e | DERIVED | FP9's (H_Y) headline at z = 0.25 passes KiDS: -2.4/-5.6 -> -2.6/-1.9 (inherited by FP11 K7/G1, FP12 K7) | corrected by FP20 (R2: FP9 re-run whole; its window stays 28/48; only the K1 control flips) |
| FP20 | F20f | DERIVED | FP13's H_S passes KiDS at z = 0.25 (-6.2/-7.7 -> -8.6/-10.3) and 0.4 (-7.8/-10.7 -> -8.8/-9.7) | corrected by FP20 (R3; controls reproduce 92 committed numbers) |
| FP20 | F20g | FAILS | FP9's own (H_Y) at z = 0.4 (FP13 H5): +20.6/+18.3 -> +19.2/+20.3 -- still FAILS the lens spread | corrected by FP20 (R3) |
| FP20 | F20h | CONSTRAINT | the KiDS floor on the band-pass length: L_KiDS +1.23/+1.17 -> +1.23/+1.24 Mpc; the KiDS-LG pincer (FP6 B6/H3, FP9 H3, FP11 X1, FP12 U1: the LG needs L(0.25) ~ 0.5-0.6 Mpc, KiDS costs +250..+300 there) is unchanged | corrected by FP20 (R1, R2, R4) |
| FP20 | F20i | CONSTRAINT | FP1 E3's KiDS tolerance on the lenses' external field (2-halo, 1e-4 a0): +5.2/+3.7 -> +4.7/+3.1; no 2-halo +2.3/+1.7 -> +1.7/+1.2 (x1e-4); the LG needs +7.0/+6.6 -> +7.8/+7.9 times more (FP11 P1 holds); the band-edge reading (reported) +0.93/+0.90 -> +1.04/+1.07x crosses 1 | corrected by FP20 (R6, R5) |
| FP20 | F20j | CONSTRAINT | FP13's A3 threshold windows narrow (the other gates as committed): NL/FP9 yield: [1.686, 2.0, 2.4, 2.6, 2.7] -> [1.686, 2.0, 2.4]; NL/state yield: [1.3, 1.5, 1.686, 2.0, 2.4, 2.6] -> [1.3, 1.5, 1.686, 2.0, 2.4, 2.6]; lin/FP9 yield: [1.2, 1.4, 1.6, 1.65] -> [1.2, 1.4, 1.6]; lin/state yield: [1.1, 1.2, 1.4, 1.6, 1.65] -> [1.1, 1.2, 1.4, 1.6, 1.65]; delta_c stays inside both nonlinear windows (A3a holds) | corrected by FP20 (R3) |
| FP20 | F20k | CONSTRAINT | L355's 'KiDS needs a web-blind kernel': the baryons-only deficit +233.4/+241.0 -> +283.7/+304.4 and the carrier + 2-halo +130.6/+144.7 -> +173.9/+189.5 -- the claim survives, stronger | corrected by FP20 (R8) |
| FP20 | F20l | CONSTRAINT | L360's assembled construction: pairs passing KiDS 70 -> 35 of 96 (the carrier templates move d chi^2 by +13..+22); the M2 claim (some pairs pass) survives | corrected by FP20 (R9: L360 re-run whole) |
| FP20 | F20m | CONSTRAINT | AT3's KiDS gate at its window cells (switched fit, <= +4): passing cells 0.1|600|0.25, 0.03|600|0.25 -> 0.1|600|0.25, 0.03|600|0.25 (d chi^2 moves +0.7..+6.1); its switch-free KiDS (reported) improves | corrected by FP20 (R11: AT3's retention profiles recomputed with its own functions; FP4 C4 and FP10 B4 are estimates from these shifts) |
| FP20 | F20n | OPEN | the P2 lanes downstream of DE8 (DE10's converged model, the hub's XR9 and XR14 ON-M* KiDS pass) carry the carrier-template error (V1b) and must be re-scored with the corrected projection; so must FP15/FP16 (uncommitted, kids_switched) | V4, V1b, R9, H |
| FP20 | F20o | CONSTRAINT | the isolated-P2 KiDS base itself: P1 lanes +112.3/+105.6 -> +141.6/+134.9 (the lead grade flattered the inner phantom); P2 lanes (nu_mono, 2-halo) +174.3/+166.9 -> +159.9/+153.0 -- every gate here is a difference to its lane's base | R1, R9 |
| FP20 | F20p | OPEN | the P1 lanes score point values at the bin centres, not B21's annulus averages (a ~1-2% convention, unchanged here); the 2-halo templates keep their own inner-disc approximation (V5) | scope |
| FP21 | F21a | CONSTRAINT | the like-for-like lens sample exists and is small: 2M++ (spectroscopic, K <= 12.5, complete in both KiDS regions) holds 2,036 galaxies in the KiDS-1000 footprint (z >= 0.01), 621 at 10.4 <= log M_gal <= 10.8 with the LV centrals' own mass mapping (0.6 L_K + Boselli gas; UNGC L_K reproduced to -0.008 dex), 227 LATE-labelled; only 108 are the brightest within 3 Mpc / +-500 km/s, 52 of them LATE (the primary) | K4, S, T1 |
| FP21 | F21b | CONSTRAINT | the pipeline (exact spherical geometry, c, m = B21's 1+K, dilution model, randoms, jackknife) reproduces B21's published bins 2 / 3 from the record's photometric reconstruction at A = 0.91 +- 0.10 / 1.15 +- 0.09 with B21's convention (no boost); applying the boost measured against uniform randoms gives 1.00 / 1.28 (K6 as first declared FAILS for bin 3) -- that boost is confounded by the lens samples' mask selection, and is inactive for the 2M++ lenses (B <= 1 in the band); cross-shear and random nulls pass | K1, K5, K6, K6b |
| FP21 | F21c | CONSTRAINT | the measurement: the primary sample's Delta Sigma over 0.26-1.62 Mpc is 5.60 +- 3.73 Msun/pc^2 (S/N 1.5), A = 2.19 +- 1.46 of B21's mixed-type isolated lenses at the same mass; all types isolated A = 2.37 +- 1.18; group centrals (1 Mpc) A = 1.18 +- 0.78 | D1, D2, D3, C1 |
| FP21 | F21d | CONSTRAINT | against the flow (R0 = 0.919 +- 0.080 Mpc): the band Delta Sigma allowed is <= 0.96 (rigorous, any profile) / 0.57 (any NFW); the primary's mass-matched band is 5.67 +- 3.78; the joint free-profile T = 2.86 (p 0.09); at B21's precision the flow tolerates at most A_rec = 0.31 of the mixed-type profile (all radii scaled) at face value -- FP18's -0.5 dex reconciliation, recovered independently | C2, C3 |
| FP21 | F21e | OPEN | the verdict by the declared rule: UNDECIDED | V1 |
| FP21 | F21f | CONSTRAINT | FP18's comparability systematics tested directly (L_K masses as the LV's, spectroscopic isolation, z ~ 0): no sample is measurably BELOW B21's mixed level -- isolated all types A = 2.37 +- 1.18, group centrals 1.18 +- 0.78, the primary 2.19 +- 1.46, non-isolated 1.90 +- 0.77 (isolated and non-isolated do not differ measurably); FP18's reconciled level A ~ 0.3 lies 0.8-1.8 sigma below the isolated samples -- a lean against reconciliation, not a result | D3, C1 |
| FP21 | F21g | OPEN | for the chain's universal law (R0 = 1.24-1.53 Mpc for the stack / LG, FP12; no type dependence possible): nothing moves: FP18's standing holds -- the chain's R0 = 1.24-1.53 Mpc overshoot of the LV is neither confirmed as a law-specific failure nor excused as a data-data pincer; the chain's universal law cannot produce a type dependence, so a future RECONCILED would FAIL it | V1, FP12, FP18 |
| FP21 | F21h | OPEN | for LCDM: unchanged: LCDM's KiDS-fitted halos turn around at 1.65-2.26 Mpc (FP18 L1); a type split in halo mass at fixed M* is standard LCDM, so a future RECONCILED would be comfortable for it | V1, FP18 L1 |
| FP21 | F21i | OPEN | what would decide it: ~2084 spectroscopically isolated late-type centrals at LV-central mass at z ~ 0.03 (3 sigma between A = 1 and A_rec = 0.31), or ~13978 at z ~ 0.1-0.4; the on-disk 2M++ holds 52; GAMA DR4 (G09/G12/G15/G23, r < 19.65) or SDSS DR7 spectroscopy over KiDS-N is the next step, and fetching it needs the user's go | V2 |
| FP21 | F21j | FITTED | the type cut is FITTED to labels, not to lensing: GAaP u - r < 2.35 (no 6dF-FP early type below it; ~70% of HI-rich spirals) -- at z ~ 0.026 it is a bulge colour, so LATE is spiral-enriched, not morphological | T1 |

Totals: DERIVED 127, TIED 1, POSTULATED 30, FITTED 15, CONSTRAINT 41, OPEN 44, FAILS 78
