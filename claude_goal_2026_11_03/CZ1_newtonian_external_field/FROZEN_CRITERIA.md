# CZ1_newtonian_external_field: FROZEN CRITERIA (before any script or number beyond the hand estimates below)

Owner, 2026-11-03: "now you do it too", the hardest-problems push run alongside astra's goal (`ASTRA_GOAL_2026-11-03_HARDEST_PROBLEMS.md`, P2 and P5). Lane prefix CZ, folder `claude_goal_2026_11_03/`; no other session's file is edited.

κ = ½ FITTED, held fixed. Footings never pooled. No cold component, no particle. No download. Not theory closed. Nothing here says the data favour the framework.

## The suspected defect
QUMOND: ∇²Φ = ∇·[ν(|∇Φ_N|/a0) ∇Φ_N], with Φ_N the Newtonian potential of **all** baryons. Near a satellite, ∇Φ_N = g_N,int + **g_N,ext**, where g_N,ext is the host's **Newtonian** field. In the 1D quadrature approximation used by the KT lanes, the internal field is g = g_N + (ν(√(g_N,ext² + g_h²)/a0) − 1) g_h.

KT15, KT17, KT25, KT26, KT27 and KT28 set the external term to `ge = (200 km/s)² / D`, the host's **MOND** (observed) field, inside ν. In the external-field-dominated limit that gives a boost ν(g_e/a0) ≈ (a0/g_e)^½, where McGaugh and Milgrom (2013) give a0/g_e. KT27's criteria say the external field is "added in quadrature to the Newtonian field", so the intent was the Newtonian term. KT27/KT28 also build ξ_loc from ν(g_q)·g_q with g_q = √(g_N² + ge²), so the MOND external field is boosted a second time there. The Cassini integral (KT16/KT25/KT27) puts the observed Galactic field 2.32e-10 m s⁻² in the same slot.

## Part A: form check (analytic, numbers printed)
- **K0.** For a weak test system (y_int → 0) in a uniform field with Newtonian strength y_Ne = g_Ne/a0 ∈ {0.003, 0.01, 0.03}: the corrected form's boost is ν(y_Ne). The McGaugh–Milgrom boost is a0/g_e with g_e = ν(y_Ne) g_Ne. The KT form's boost is ν(g_e/a0). Print all three.
- **Label A: DEFECT CONFIRMED** if the KT form's boost differs from McGaugh–Milgrom by more than 30 % at y_Ne = 0.01, and the corrected form agrees with it to within 10 %. **NO DEFECT** otherwise; in that case the rest of the lane is reported but carries no label.
- Hand estimate: y_Ne 0.01 → ν 10.5, g_e/a0 0.105, ν(0.105) 3.6, ratio about 0.34. Expect DEFECT CONFIRMED.

## Part B: the 24 dwarfs (graded)
KT27's dwarf model, copied verbatim (Plummer, McConnachie 2012 extract on disk, Υ_V ∈ [1, 3] in 41 steps, gas 1.33 M_HI, pass when some Υ gives |σ_pred − σ_obs| ≤ 2 e_σ). Modes: plain (ξ 0), const ½ r_M (KT25), const 0.55 r_M (KT17's ε), local (KT27's row-wise ξ_loc), at_a (ξ_loc(a), one value). Both footings.

External-field variants:
- **E0, reproduction:** ge = 200²/D on MW satellites, others 0. It must reproduce KT27's counts exactly (plain 15/15, const ½ r_M 15/15, local 14/14 canonical/alt) and Fornax local 5.0/5.1 km/s (**K1**).
- **E1, corrected, KT scope:** g_Ne = G M_MW,b / D² on MW satellites only, M_MW,b = 7.0e10 M☉ (KT15's frozen value), D heliocentric as in KT15. This is the only change from E0. Sanity check **K2**, reported only: the law's own MOND field ν(y_Ne) g_Ne at D = 76, 147 and 250 kpc beside 200²/D.
- **E2, both hosts, all 24:** g_Ne = |Σ_h G M_h r̂_h / d_h²| over the MW and M31, vector sum of Newtonian fields (exact in QUMOND's ν argument), positions from UNGC (Karachentsev 2013 on disk: RA, Dec, Dist) through astropy galactocentric coordinates (R0 8.178 kpc). M_M31,b = 0.6 L_K + 1.33 M_HI from UNGC's M31 row (FD1's Υ_K). Dwarfs without a UNGC match keep E1's value (disclosed by name).

Labels, per footing, E1 primary, E2 beside:
- **REFERENCE CHANGES** if the plain count under E1 differs from KT15/KT27's 15/24; **REFERENCE STANDS** otherwise.
- **KT27 DWARF FAIL IS AN ARTEFACT** (alt, the footing KT27 graded) if the local mode under E1 passes ≥ 15/24 **and** reaches the corrected plain count minus 1, **and** Fornax passes; **KT27 DWARF FAIL STANDS** otherwise.
- **KT25 DWARF ROW**, canonical: const ½ r_M under E1 against the corrected plain count. **HOLDS** if it reaches ≥ plain − 1; **FALLS** otherwise. KT17 0.55 r_M is reported the same way.
- Hand estimate: Fornax g_Ne/a0 ≈ 0.004 (alt) against KT15's 0.078, so MW-satellite predictions rise toward the isolated case. KT15's isolated plain count is 19/24, so the corrected plain count should land between 15 and 19. Which way the local mode moves is not known.

## Part C: Cassini under the Newtonian Galactic field (graded, both directions)
KT27's Cassini integral (qcas, KT16's), copied verbatim, with η replaced by η_N = g_N,gal/a0, where g_N,gal solves ν(g_N/a0) g_N = 2.32e-10 m s⁻² on each footing (the law inverted, framework-native). Arms: const ½ r_M (KT25 R1 reference 0.481 canonical / 1.06 alt), const 0.55 r_M, local.
- **K3:** with η = 2.32e-10/a0, R1 reproduces KT27's 0.481 / 1.06.
- Per arm and footing: PASS if Q2 ≤ 5.2e-27 s⁻² (KT16's ceiling), FAIL otherwise. Reported beside the E0 value, so a correction that **hurts** Cassini is stated as plainly as one that helps.
- Hand estimate: at the Sun y ≈ 2, ν ≈ 1.2, so η_N is about 0.8 of η. ν − 1 grows, so Q2 is expected to rise by tens of percent, against KT25 canonical.

## Part D: IC 1613 (stated, not graded)
The Newtonian Local Group field at IC 1613 (MW + M31 baryons as in E2) beside IC 1613's own g_N/a0 at r½ from FD1's PRIMARY inputs, and the resulting shift in FD1's E using the corrected form. Hand estimate: g_Ne/a0 ≈ 6e-4 against about 0.02, so the shift is ≲ 0.001 dex. That would close the external-field lever named in `FAILURES_LITERATURE_REVIEW_2026-10-28.md` §1 (it compared a MOND external field with a Newtonian internal one).

## Checks
K0–K3 as above. **MUTATE:** ν ≡ 1 (Newton) in every arm, written to separate `_MUTATE` outputs, exit 1; expected to fail K1 and most dwarf rows. Peak RSS printed (budget 1 GB, one thread). The dwarf-count changes are the deliverable; MW cells and SPARC carry no external field and aren't rerun.

## What this lane can't say
A count rising under E1 doesn't make the filter a theory: the KT lanes' MW, Cassini and SPARC rows stand as graded, except where Part C changes Cassini. The 1D quadrature form ignores QUMOND's anisotropic factor; that stays a stated approximation on both the KT lanes and this one.
