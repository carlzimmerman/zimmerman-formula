# CFG490 FROZEN CRITERIA: the G9-violating arm of the fork. Does ONE direct baryon-cold coupling deliver supply + edge + temperature, and survive the bounds a direct coupling must face?

Committed alone, before any script exists. **LABELLED EXPERIMENT** (owner, 2026-10-08: "no problem with experimenting new
ideas"). This lane tests arm (a) of the fork in WORKING_MODEL_SETTLED_PHANTOM_2026-10-06.md. **Every coupling scored here
violates G9 (CFG329: matter couples to the metric only) by construction.** kappa = 1/2 is FITTED. Both footings
(a0 = 9.3603e-11 and 1.1312e-10 m/s^2) are scored separately and never pooled. The cold fluid's MASS is still required and its
amount (Omega_c/Omega_b = S = 5.364) is an input. If a coupling needs a field quantum, that is stated plainly as a
dark-matter particle. No knob scans for a pass (the one scan below is the declared window test of one coupling). Never
"theory closed". Offline theory + numerics; no downloads; only committed record files are read (read-only).

## Why this lane (the record, 10-08)

The G9 arm failed three ways: CFG461 (no G9 mechanism sets sigma^4 = G M_b a0/4), CFG462 (the khronon lapse has no f_b, so it
cannot stop settling at r_edge = r_M/ln(1/(1 - f_b)) = 5.8498 r_M; the edge appears only if the supply is exactly the share),
CFG488 (co-settling enforces the per-galaxy supply 5.364 M_b only through a shared baryon-cold label = a direct coupling;
gravity carries a 1/N signal). The question: does the MINIMAL direct coupling that would enforce the supply rule
("each galaxy settles exactly S x its own baryons, within the edge") also give the edge and the temperature, with at most
one new constant, and does it survive EP / fifth-force, Solar System, binary pulsars, the Bullet Cluster, CMB/BAO and the
DR3 / no-EFE results?

## Common set-up (copied from CFG462/CFG488)

- Units: G = M_b = a0(true) = 1; lengths in r_M = sqrt(G M_b/a0), per footing. Cells: M_b = 1e9, 10^10.5, 10^11.5 Msun x
  {canonical, alt} = 6 cells. Kernel nu_mono (FP1's committed table via CFG4_common, read-only). f_b = 1/(1 + S);
  x_edge = 1/ln(1 + 1/S) = 5.8498 (the growth fix's edge, used for every host, as in CFG462/CFG488).
- Hosts: point mass (scored), Hernquist a = 0.3 r_M (scored, CFG462's host), a = 1 r_M (reported).
- Law target: M_ph(<r) = (nu(M_b(<r)/r^2) - 1) M_b(<r).
- Catchment supply (scored): S_cat = 23.63 M_b (CFG488 K4: cold inside r_ta from CFG118); CFG462's 22.6 reported.
  r_ta = 236 kpc (M_b/1e9)^(1/3) (CFG462's constant from CFG118), x_ta = r_ta/r_M per cell.
- Settling drive: the record's F-H flow (CFG462), outward velocity v = D [g_N(g) - g_b] + (coupling terms below), equilibria
  solved pointwise in enclosed mass. The F-H mobility D (CFG381's +1 fluid-khronon coupling) and its energy sink are
  INHERITED from the G9 arm; they are listed, not counted against any coupling, and the sink stays NOT SUPPLIED (CFG462).

## The couplings (written explicitly; all scored, none dropped)

- **C1 BK phonon coupling (the owner's named form).** Berezhiani-Khoury EFT as frozen in CFG122:
  P(X) = (2 Lambda (2m)^(3/2)/3) X sqrt|X|, L_int = -(alpha Lambda/M_Pl) theta rho_b, a0 tie a0 = alpha^3 Lambda^2/M_Pl
  (N_a = 1). Gradient branch: rho_DM = 2 m^2 Lambda sqrt(kappa_BK), kappa_BK = alpha M_b(<r)/(8 pi M_Pl r^2) (CFG154,
  re-derived with sympy here). Scored at its BEST case: the one constant combination m^2/alpha set to centre the six cells'
  log supply misses (point mass). "BK edge" = radius where the condensate mass reaches S M_b; "BK supply" = condensate mass
  inside x_edge over S M_b. The MOND force is the phonon force on baryons (a direct force).
- **C2 neutralising U(1) (the minimal LAGRANGIAN enforcer).** A massless vector A_mu coupled to baryon number and to the
  cold fluid's number current with opposite signs: L_int = -A_mu (e_b J_B^mu - e_c J_c^mu). FRW homogeneity + isotropy forbid
  a background field, so Gauss's law forces zero mean charge: e_c n_c = e_b n_B, i.e. per unit mass eps_c = eps_b/S (DERIVED,
  0 constants). One constant: alpha_N = e_b^2/(4 pi G m_u^2) (nucleon-nucleon repulsion in units of gravity); then
  alpha_bc = alpha_N/S, alpha_cc = alpha_N/S^2. Force on cold, outward: alpha_cc G (M_c(<r) - S M_b(<r))/r^2. The galaxy
  is neutral (supply = S M_b) exactly where the cap holds. Equilibrium with F-H (weight w = 1, the mismatch's gravitational
  field energy): r^2 g_N((M_b(<r) + m)/r^2) - M_b(<r) + alpha_cc (m - S M_b(<r)) = 0 for m = M_c(<r); settled profile
  min(m*, S_cat) on [r_min, x_ta]; if m*(x_ta) < S_cat the rest stays unsettled at x_ta.
- **C3 supply-transfer gate (the owner's "transfer term in the continuity equations"; the minimal RULE-level enforcer).**
  Two cold components, settled s and unsettled u:
  d_t rho_s + div(rho_s v_s) = +J, d_t rho_u + div(rho_u v_u) = -J, J = Gamma rho_u Theta(-E.g_hat), with E the composition
  field, div E = 4 pi G (s_gate rho_b - rho_c) (all baryons, all cold). Settled cold follows F-H; Gamma is identified with the
  inherited settling rate (projection limit, not counted). Spherical equilibrium: settled = law inside the first radius where
  M_ph(<r) = s_gate M_b(<r); supply = s_gate M_b(<r_e).
  - **C3a:** E is an auxiliary, non-dynamical field and s_gate is inserted (= S). No force on anything.
  - **C3b:** E is C2's gauged U(1) field (s_gate = S derived by FRW neutrality); the gate reads only sign(E.g), so the
    delivery does not depend on alpha_N, which is scored at 0.5 x the tightest bound's alpha_N limit.
- **C4 drag (momentum-exchange coupling; the literal "cold stays with its baryons" in the momentum equations).**
  d_t v_c = ... - Gamma_c (v_c - v_b), Gamma_c = rho_b kappa_d |v_rel|, kappa_d = sigma_T/(m_chi + m_p) (one constant).
  A drag vanishes for static configurations, so the scored (static) equilibrium is F-H + CAT; the "locked transient"
  (cold traces baryons, M_c(<r) = S M_b(<r)) is reported. Scored constant kappa_d,req = the value that locks the cold to its
  partner baryons within one dynamical time at the edge: kappa_d,req = 1/(rho_b,p(x_edge) x_edge), rho_b,p = rho_ph(x_edge)/S.

## Constant-counting rules (frozen)

(i) Every parameter in the coupling's Lagrangian or transfer law counts +1. (ii) A parameter fixed by a stated mechanism
(FRW neutrality of a gauged charge) counts 0. (iii) A number that must equal an existing input (Omega_c/Omega_b) with no
mechanism counts +1 and sets the flag R ("the edge definition written as a coupling", CFG488 finding 5). (iv) Inherited
settling-drive constants (D, the sink coupling) and kappa are listed, not counted. (v) BK's a0 tie removes Lambda (as in
CFG122); m, alpha and the condensate's relaxation rate remain (count 3; 2 if the rate is waived).

## DELIVERS (per coupling; all 5 gates in all 12 host x cell combinations)

- D-sup: |log10(M_s(<E)/(S M_b,total))| <= 0.05 (M_b,total: the galaxy's own baryons, as CFG462's SHARE and CFG488).
- D-edge: |log10(E/x_edge)| <= 0.05, E = radius enclosing 99.9% of the settled cold mass (CFG488) [C1: the BK edge].
- D-T: |log10(sigma^4/sigma_t^4)| <= 0.1, sigma^2 = G M_tot(<E)/(2E) (CFG461's R0, baryons + settled cold), sigma_t^4 =
  G M_b a0/4. Cold-only reported. Stated in advance: under the F-H target drive the settled region carries the law, so
  M_tot(<E)/E is close to the law's value for ANY far edge; D-T then follows the law, not the edge. It is scored as frozen.
- D-law: max |M_s(<r)/M_ph(<r) - 1| <= 0.05 on [0.1, 0.8] x_edge (CFG488 P1b).
- D-count: <= 1 new constant by the rules above.
- Labels: PASS; PASS-R (passes with flag R); PASS-NA (passes, but the delivery is independent of the coupling's magnitude
  and G-REAL fails); FAIL.
- **G-REAL** (scored for any magnitude-independent delivery): a local, thermally activated realisation of the gate has
  open/closed contrast ~ W/sigma_e^2, W = the composition force's work per unit cold mass across the 0.05-dex shell just
  inside the edge, sigma_e^2 = G M_tot(<r_e)/(2 r_e). PASS iff contrast >= 1 at the scored constant.
- **C2 window (declared scan, not a fit):** alpha_N on logspace(-8, 8, 161). C2 DELIVERS iff some alpha_N passes all gates in
  all combinations. Reported, normalisation-free (gravity-normalised) thresholds: alpha_law,grav = largest alpha_N with the
  coupling force <= 5% of gravity on the cold fluid over [0.1, 0.8] x_edge; alpha_cap,grav = smallest alpha_N whose
  repulsion on a cold excess of eps = 10^0.05 - 1 of the share at the edge equals gravity's pull there. The window ratio of
  the scan is invariant under the F-H weight w (both thresholds scale with alpha_N/w).

## SURVIVES (per coupling at its scored constant; one verdict per bound)

Scored constants: C1 best case; C2 alpha_N,req = alpha_cap,grav (point mass; min over cells); C3a none; C3b 0.5 x tightest
limit; C4 kappa_d,req. Verdicts: PASS / FAIL / CONDITIONAL (depends only on inherited, non-coupling physics) / VACUOUS (no
listed bound is sensitive: coupling x 100 flips none) / N-C (not computed, reason given). Inputs marked U are recalled from
the literature, UNVERIFIED; the record's own values are used where it has them.

- B1 Eot-Wash (Be-Ti, Earth source): |eta| <= 3.9e-13 (U: (0.3 +- 1.8)e-13, 2-sigma envelope). Delta(B/mu) from recalled
  isotope masses (U: 9Be 9.0121831 u, 48Ti 47.94794 u (record CFG122)).
- B2 MICROSCOPE (Ti-Pt, Earth): the record's frozen |eta| <= 1e-15 (CFG122); the recalled final result's 2-sigma envelope
  7e-15 reported (U). Delta(B/mu)_Ti,Pt from the record's isotope masses (CFG122: 9.052e-4).
- B3 Solar System: Cassini |gamma - 1| <= 2.3e-5 (record); ephemeris sunward-anomaly ceiling 1.27e-5 a0 (record), applied to
  the composition-dependent part for a vector (Saturn, H/He-rich, vs the rocky planets that fix GM_sun).
- B4 binary pulsars: CFG291's committed systems and fractional Pb-dot windows (J1738+0333, J0348+0432, J0737-3039A/B).
  Vector dipole power / GR quadrupole = (5/48) alpha_N Delta_B^2 (c/v)^2, Delta_B = difference of B m_u/M. NS: B m_u/M =
  (1 + BE/M) m_u/m_n, BE/M = 0.6 beta/(1 - beta/2), beta = GM/(R c^2), R = 12 km (bracket 11-13 km reported; U). He WD:
  4 m_u/m(4He) (U).
- B5 Bullet (record: Clowe 2006 Table 2 via CFG4_clusters; offsets 209.4 / 194.1 kpc, 100-kpc plasma masses 6.6e12 /
  5.8e12 Msun). Time since pericentre t = 0.2 Gyr scored (conservative for forces), 0.1 reported (U). Forces: the extra
  displacement of the cold peak toward the plasma, (1/2) alpha_bc G M_pl t^2/d^2, must be <= 0.25 d. Drag: optical depth of
  the main plasma column kappa_d M_pl/(pi (100 kpc)^2) <= 0.3.
- B6 CMB/BAO: long-range forces: the relative-mode coupling alpha_N/S^2 (the change of the cold growth source at
  recombination) <= 0.01 (declared ESTIMATE, not a published bound); drag: kappa_d <= 5e-3 cm^2/g (U, recalled Planck
  velocity-independent DM-proton bound; 5e-2 reported); BK: CFG122 G2 (UNDECIDED; option (a) excluded).
- B7 DR3 / no-EFE (CFG447 7.7 sigma, PAPER44, Amendment 21): PASS iff the coupling keeps the material phantom (no direct
  MOND force on baryons) AND its own baryon-baryon force leaves bound pairs (alpha_bb < 1). A coupling that carries the MOND
  force itself FAILS (the triangle: with an EFE it fails the cluster satellites, chi^2 99.7/5; without, DR3).
- SURVIVES = every bound PASS (CONDITIONAL allowed, labelled; VACUOUS labelled).

## Reported (not verdict inputs)

Clusters (CFG488: free placement u = 0 vs [0.433, 0.628]/[0.368, 0.584]; in-place 0.452/0.389); the energy sink (CFG462);
G9 (FAIL by construction, all); particle requirements; C3b's composition-field external-field effect on satellites;
C3b's sensitivity to hot-CGM baryons (the gauged charge counts ALL baryons); the scalar + vector cancellation loophole
(baryon-baryon force cancelled, baryon-cold kept) and why it does not escape B2; the seesaw inequality.

## Controls (main run exits 0 iff all pass)

- K1 (sympy): (a) for any set of same-spin exchange fields, alpha_bc^2 <= alpha_bb alpha_cc (Gram determinant >= 0);
  (b) FRW neutrality gives eps_c/eps_b = 1/S per unit mass and the C2 force law from the perfect-square charge energy;
  (c) C2's neutral point: m* = S at x_edge for every alpha_N (point mass); (d) BK supply exponent d ln(M_DM/M_b)/d ln M_b = 1/2;
  (e) R0: (1 + S)^2 ln^2(1 + 1/S) = 1.1835; (f) the dipole ratio 5/48.
- K2: C2 at alpha_N = 0 reproduces CFG462's committed F-H CAT edge (Hernquist 0.3, S_cat = 22.6) to 1e-4 relative.
- K3: C3 point-mass edge = 5.8498 r_M to 1e-6; nu_mono inverse round trip <= 1e-9.
- K4: C2 roots nondecreasing in r for every scanned alpha_N (else flagged and projected); root residual <= 1e-8.
- K5: CFG122's Delta(B/mu)_Ti,Pt = 9.052e-4 and its Reading-B MICROSCOPE eta 3.106e-9 reproduced; CFG291's J1738 GR Pb-dot
  -2.746e-14 reproduced (Peters-Mathews).

## MUTATE (CFG490_MUTATE=1; exit 1 iff the teeth are detected)

(M-a) every coupling set to zero must lose the edge (|log10(E/x_edge)| > 0.05 in some combination); (M-b) every coupling with
a force strength, at 100 x its scored constant, must violate at least one bound. C3a has no strength to scale: reported
VACUOUS, not a failure of the teeth. Teeth detected iff (M-a) holds for all five and (M-b) for C1, C2, C3b, C4.

## Expectations (stated in advance; not blind)

C1 FAIL both (supply exponent 1/2: ~1.3 dex over the cells; Solar System per CFG122). C2: window closed by ~3 dex (law needs
alpha_N <~ 0.1-0.3, the cap ~1e2-1e3); at the cap strength every bound but Cassini fails, MICROSCOPE by ~14 dex. C3a PASS-R and
VACUOUS. C3b PASS-NA, G-REAL contrast ~1e-14; SURVIVES at its scored alpha_N. C3 on Hernquist a = 0.3 may miss D-sup (~ -0.04
to -0.05 dex, baryons beyond the edge); if it does, C3 is FAIL on the scored hosts. C4 FAIL (static equilibrium = the uncoupled
CAT fill; locked transient breaks the law; CMB by several dex).

## Verdict lines

Per coupling: DELIVERS label; SURVIVES label with per-bound verdicts; constant count. Lane: "arm (a) DELIVERS" only if some
coupling is a clean PASS; PASS-R / PASS-NA are reported as such, never as a clean pass.

## Outputs

`cfg490_direct_coupling.py` -> `cfg490.out`, `cfg490_results.json`; MUTATE -> `cfg490_MUTATE.out`,
`cfg490_results_MUTATE.json`; `README.md` (plain, states that this arm violates G9 by construction and what that would mean).
Committed locally, not pushed.
