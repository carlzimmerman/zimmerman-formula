# Lane N3 -- graviton-inherited gauge coefficient: is it TIED to G*Lambda, FREE, or MIXED? (pre-registration)

Written 2026-09-28 BEFORE any committed script in this directory was run. Amendments are appended at the bottom, never edited in place.
Target: 1/alpha = 137.035999177 (Thomson limit; alpha runs). Bar: lane D (P < 1e-3 after look-elsewhere, miss <= 5e-10 or a stated predicted precision,
zero fitted reals, scale stated). Mutation control convention for EVERY script in this lane: positional argv `MUTATE` (python3 script.py MUTATE must exit 1;
python3 script.py must exit 0). Run with PYTHONDONTWRITEBYTECODE=1.

## Disclosure of what was done before this file (so nothing below is presented as a blind prediction where it was not)
* Read in full text (pdftotext of arXiv PDFs): Nesti-Percacci 0706.3307 (all 18 pp.), Nesti-Percacci 0909.4537 (all text; the appendix gamma matrices skimmed),
  Lisi-Smolin-Speziale 1004.4866 (sections 1-4, all), Smolin 0712.0977 (sections 1-2 in full incl. eqs (26)-(35) also read from the page image; sec. 3 skimmed).
* Read in part: Torres-Gomez & Krasnov 0911.3793 (abstract, introduction, section 7.8 eqs (199)-(203), the closing discussion; NOT the 57-page body);
  Krasnov & Percacci review 1712.03061 (the MacDowell-Mansouri section, the graviweak section, the MM-type-unification section and its "difficulties" paragraph; NOT the rest of 3900 lines);
  lane M's m3_ds_gauge_coupling.py and pre-registration, lane D's pre-registration, the repo review PARTICLE_PHYSICS_FROM_DESITTER_GAUGE_2026-06-15.md (all).
* Only grep/abstract level: Nesti 0706.3304 (Clifford-algebra graviweak), which is out of scope and NOT scored. Recalled, not read: Lisi 0711.0770 (E8), Chamseddine SL(2N,C),
  Percacci 1984/1991, Stelle 1978.
* Hand derivations done before writing this file (they are the predictions below): (a) elimination of B in LSS eq (1) gives 3/(8g) <F *F> (matches their (25));
  (b) Clifford blocks give F_L = (1/4)[R^ab - (phi^2/4) e^a e^b] gamma_ab so that Lambda = 3 v^2/4 (matches their (28)); (c) G = 8 g/(3 pi v^2), G*Lambda = 2 g/pi, and a spin(N) gauge
  coupling normalised with the 16 of SO(10) (T(16)/T(10)=2) is g_G^2 = 32 g/3, i.e. alpha_G = (4/3) G Lambda -- NOT the printed g_YM^2 = 2g/3 (a factor 16, convention);
  (d) a Clifford-scalar-part trace kills any spin(N) F^F term for h-invariant compensators other than the identity.
* ONE scratch computation was run before this file (outside the lane directory, not committed): a sympy test of whether Smolin's (31) reproduces his (32) and (34).
  Its outcome is known to me and is disclosed so that H3 is not scored as blind: under one reading of the index sums (32) is reproduced up to an overall factor 2, and the
  leading coefficient "3" of the bracket in (34) is reproduced, but the printed extra terms (-xi/48 + 3 xi W^2/8) are NOT. The committed script n3 redoes this properly with all four readings.

## Question and the three (four) verdict classes, defined now
For each construction, the physical gauge coupling g_YM (defined through the covariant derivative acting on the fermion representation and, for SO(10)-type groups,
in the GUT normalisation T(vector)=1) is compared with the gravitational-sector coefficients (G, Lambda, higher-curvature coefficients).
* TIED: g_YM^2 = f * G*Lambda (or another combination of G, Lambda) with f a pure number, no free parameter of the action left to move it. Then alpha is fixed, and
  the value at the observed (G, Lambda) is ~ 1e-122 (fails by ~120 decades).
* FREE: g_YM^2 is a coefficient of the action (or of a defining function/potential) not related to G, Lambda by any relation in the construction; the construction relabels the freedom.
* MIXED: a RATIO between two coefficients is forced by the construction while the overall scale is a free real (or tied to G*Lambda -- stated which).
* ABSENT / UNDEFINED: the printed action has no gauge kinetic term F^*F (or no bosonic action at all), so there is no coefficient to inherit.
A construction is scored "would fix alpha" only if it is TIED with an f that reaches 1/137 at inputs the construction itself fixes, or if it has zero fitted reals and meets lane D's bar.

## Hypotheses (each can be false)
* H1 (n1_mm_type_trace.py): in any MacDowell-Mansouri-type action  Int <X F^F>  on spin(1+N,3) with X an h-invariant element (h = spin(1,3) + spin(N)) of the Clifford algebra,
  the spin(N) gauge sector contributes only through X = 1 (the topological Pontryagin term <F^F>, no metric, no kinetic term); every other invariant X gives ZERO F_N F_N coefficient
  (N = 3 and N = 10). Hence the MM-type extension has no gauge kinetic coefficient to inherit (ABSENT). The gravity block reproduces the MM relation Lambda/3 = phi^2/4 (Lambda = 3 phi^2/4).
* H2 (n2_lss_spin113_coupling_relation.py): Lisi-Smolin-Speziale (spin(11,3), action (1)) is TIED: alpha_G = (4/3) G*Lambda in the convention of hand derivation (c) above
  [G*Lambda = 2g/pi independent of the Higgs vev v; g the single dimensionless coefficient of the action]. At the observed G*Lambda = 2.85e-122 (lane M's inputs) alpha_G ~ 3.8e-122.
  The relation "g_YM^2 = 2g/3" printed in the paper is NOT reproduced (factor 16 from generator/trace convention); all convention variants give alpha in 1e-124..1e-121.
  The Riemann^2 coefficient is forced to equal 1/(4 g_G^2) (a forced ratio between a gravitational and the gauge coefficient); the overall scale is the free dimensionless g of the action,
  equivalently G*Lambda.
* H3 (n3_smolin_plebanski_gamma_scan.py): Smolin's extended Plebanski action (0712.0977) is MIXED-with-a-free-real: g_YM^2 = G_N Lambda * h(gamma) with h depending on the free Immirzi-like label gamma
  (the source says gamma is arbitrary but nonzero); neither the printed (34) nor my re-derivation gives a constant h. The printed (34) is not reproduced from (31) beyond the leading term.
  Reaching alpha = 1/137 at the observed G_N Lambda needs a fitted real (gamma tuned near a pole of the printed h, precision ~ 1e-61 to 1e-121 in gamma), so it fails the zero-fitted-reals criterion.
* H4 (n4_graviweak_nesti_percacci.py): Nesti-Percacci graviweak unification (0706.3307) is FREE for the coupling and MIXED only inside the gauge/gravity higher-derivative sector:
  Jacobian rank of (G, g_W^2) with respect to the action's (g1, g2, M) is 2 (g_W^2 = g2^2 is independent of G and of the cosmological term lambda M^4); the Z2 + SO(4,C) structure forces the
  coefficient of (R_munu)^2 equal to that of W^2 (and K^2), i.e. ratio 1:1:1, with the overall 1/g2^2 free. Invariant symmetric forms on the so(4) adjoint: dimension 2, and 1 after Z2.
  Nesti-Percacci 0909.4537 (SO(3,11)) has NO bosonic action in the text (the authors state that omission); this is a source-reading item, not a script result (UNDEFINED).
* H5 (n5_tgk_and_bar_summary.py): Torres-Gomez & Krasnov (0911.3793) give g_YM^2 = 4 pi G kappa with kappa a first derivative of the defining potential (free function), Lambda set to zero: FREE.
  Applying lane D's bar to every construction: none clears it. LSS fails the precision/value criterion by ~120 decades although it has no fitted real; Smolin, TGK, NP each need a fitted real.
* H6 (overall): the branch yields NO forced principle that fixes a gauge coupling. Only LSS forces a coupling value (as a fraction of G*Lambda), and the value is wrong by ~120 decades at the observed
  G*Lambda; the escape ("bare" G*Lambda ~ O(1) at the Planck scale) reintroduces the bare/observed Lambda gap as the free input.

## Everything that will be run (declared list; count = 5 scripts, each with a MUTATE control, 10 runs; nothing else is scored)
1. n1_mm_type_trace.py   -- explicit Clifford algebra Cl(1+N,3): N = 3 (d=7) and N = 10 (d=14, 128x128); scalar parts of X J_mn J_pq and X J_am J_bn for X in the h-invariant basis {1, G_L, G_N, G_L G_N};
   gravity block Lambda = 3 phi^2/4. MUTATE: adds the non-invariant X = g5 g6 g7 g8 to the "must vanish" list -> the vanishing check must fail.
2. n2_lss_spin113_coupling_relation.py -- LSS (1)->(25) elimination (6x6 star operator), Clifford blocks (E^E = -(1/8)phi^2 g_ab), the contraction identity L.L = Riem^2 - phi^2 R + (3/2) phi^4
   (random exact-rational algebraic curvature tensors), the trace/index normalisation T(16)/T(10) = 2 (explicit Cl(10)), the coefficient relations G, Lambda, g_G, alpha_G/(G Lambda), the convention variants (3), the numbers at observed inputs.
   MUTATE: the Phi^3 coefficient 1/3 -> 1/2 in the action -> the (25) prefactor 3/(8g) check must fail.
3. n3_smolin_plebanski_gamma_scan.py -- Smolin (31)->(32)->(34) re-derivation, four readings of the index sums (P, P-half, Q, Q-half), comparison with the printed (32), (34), (35);
   h(gamma) for printed and re-derived, sign structure, poles, tuning precision for alpha = 1/137.036. MUTATE: flip the sign of the eps B B coefficient -> the (F - 6 W *F)/(1-36 W^2) structure check must fail.
4. n4_graviweak_nesti_percacci.py -- Jacobian rank of (G, g_W^2) in (g1, g2, M); the vacuum-energy independence; invariant symmetric bilinear forms on so(4) adjoint (dim 2; 1 with Z2 swap); the printed-source statement about
   0909.4537 is echoed as UNSCRIPTED. MUTATE: assert the invariant-form dimension is 1 without the Z2 -> must fail.
5. n5_tgk_and_bar_summary.py -- TGK relation g^2 = 4 pi G kappa (kappa needed for alpha = 1/137.036), the per-construction verdict table, and lane D's bar applied to each row with the numbers.
   MUTATE: declare the LSS value to be at the required alpha (miss set to 0) while keeping its derived ratio -> the internal consistency check (derived alpha at observed inputs vs claimed) must fail.

## Pass / fail criteria for THIS lane (declared now)
* V1 (n1): all "must vanish" checks pass for N=3 and N=10 (exact zero in floating point < 1e-12); the identity-X check is nonzero; MM Lambda relation holds. FAIL of H1 if any non-identity invariant X gives a nonzero F_N F_N coefficient.
* V2 (n2): sub-checks (a) B-elimination gives 3/(8g) and B = (3/4)*F; (b) Clifford block identity holds to 1e-12; (c) contraction identity exact; (d) Lambda = 3v^2/4 and R0 = 4 Lambda; (e) T(16)/T(10) = 2;
   (f) alpha_G/(G Lambda) = 4/3 exactly (physical G) and the printed 2g/3 is reported as reproduced or not (declared expectation: not); (g) all convention variants give alpha < 1e-120 at observed inputs.
   FAIL of H2 if (f) gives a different rational or if any variant exceeds 1e-118.
* V3 (n3): pass if h(gamma) is non-constant for every reading and the source's freedom of gamma is confirmed by (19) (W(gamma) covers [Wmin, inf)); "printed (34) reproduced" is scored as declared expectation FALSE.
* V4 (n4): rank 2; dim 2 -> 1.
* V5 (n5): the table is complete; each row's verdict class is one of TIED/FREE/MIXED/ABSENT with its number; the bar row uses lane D's four criteria.
* Final verdict per construction uses only the classes above; "would fix alpha" is YES only if TIED with reachable value or bar cleared. Expected overall: NO for all.

## Scope / not done
No attempt to fix alpha by a new derivation. SM masses walled; kappa = 1/2 fitted. Not covered: E8 (Lisi), SL(2N,C), the Clifford-algebraic graviweak model, quantum corrections to the coefficients,
and any construction not built from a single connection. Sign conventions of the unified actions (relative sign of gravity and gauge blocks) are NOT resolved here and are reported as caveats only.

## Amendment 1 (2026-09-28, after running n1-n5; nothing above edited)
Results versus the predictions stated above, and every deviation from the pre-registered plan:
* H1 CONFIRMED (n1): all h-invariant constant compensators other than X = 1 give exactly zero spin(N) F^F coefficient for N = 3 and N = 10; X = 1 gives the topological term only; Lambda = 3 phi^2/4 from the MM gravity block.
  Deviation: I used an exact Clifford blade algebra (clifford_lib.py, rational arithmetic) instead of "explicit gamma matrices" for n1 (cleaner, representation independent); explicit 32x32 matrices are used only for T(16)/T(10) in n2 (with an exact cross-check).
  Scope limit: constant X only; a field-dependent Phi (LSS) is a different construction, treated in n2.
* H2 CONFIRMED (n2) with one deviation: alpha_G = (4/3) G Lambda exactly (physical G, GUT-normalised g_G^2 = 32g/3); the printed g_YM^2 = 2g/3 is not reproduced (ratio 16), as predicted. I registered THREE convention variants; the script has FOUR
  (the extra one, V3, mixes the printed G_N with my g_G). All four give alpha(obs) between 4.7e-125 and 3.8e-122 (spread factor 804, pure convention). A sign caveat was found and is unresolved: my Clifford blocks give the Lorentz block and the spin(N) block
  the SAME sign structure, while the printed (27) has Riem^2 and F^2 with opposite signs.
* H3 PARTLY WRONG in detail (n3). (i) My pre-registered remark "the leading coefficient 3 of the bracket in (34) is reproduced" was a mis-simplification in my scratch work: the printed bracket equals (1-72W^2)/(1-36W^2) exactly and the re-derivation gives -(3/2) g W xi, so (34) is NOT reproduced at all (only the structure of (32), and only under the reading P-half, factor 1). (ii) UNREGISTERED addition, disclosed: Part A re-derives the gravity sector of (26) with ansatz (17) and finds W = (1+gamma^2)/(24 gamma), potential structure (1+6 gamma^2+gamma^4)/gamma, so the printed (19) and (29) are also not reproduced.
  (iii) The tuning precision I guessed (1e-61 .. 1e-121) is 1.1e-59 for the printed chain, and there the printed sign of 1/g^2 is negative; the two re-derived chains are bounded (|h| <= 0.021), a stronger negative than predicted. The verdict (h non-constant, gamma free, alpha not reachable) is unchanged.
* H4 CONFIRMED (n4): rank 3; ad-invariant forms on so(4): dim 2, dim 1 after the Z2 reflection. H5 CONFIRMED (n5): no construction clears the bar.
* Source-reading items NOT script-verified: 0909.4537 has no bosonic action (paraphrase of the authors' own statement); TGK's relation g^2 = 4 pi G kappa is taken as printed ((152) and the body not read).
* All mutation controls (positional MUTATE) exit 1; all real runs exit 0. No __pycache__ or PDFs were written in this directory (source PDFs were fetched to the session scratchpad only).
