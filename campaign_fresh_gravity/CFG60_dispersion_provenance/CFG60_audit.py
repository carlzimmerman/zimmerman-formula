#!/usr/bin/env python3
"""CFG60 audit: re-reads every cited check id / verdict string from the committed (or named-uncommitted) files.

FROZEN QUESTION (declared verbatim before the table was built):
'Does any committed construction give the cold fluid's velocity dispersion (equivalently its pressure or stress,
C(r) = rho_c r^3 g_tot = (a0/4 pi) M_b(<r)) as set by the ENCLOSED BARYONIC MASS through a dynamical mechanism, as
opposed to being initial data from collapse or a postulate? The answer is one of: YES (name the construction and its
exact hypotheses), NO (with the exact hypothesis boundary of each excluded class and each surviving restatement), or
UNDECIDED (list what was not run). A scoped NO is a valid answer.'

RUBRIC (frozen): D = derives the dispersion/stress dynamically from an action or field equations with no postulate of the
target; P = postulates the target (or its equivalent) and is otherwise consistent; I = the dispersion is initial data
(collapse history / formation), not set by the enclosed mass; X = excluded by a committed script, with the exact hypothesis
of the exclusion; U = untested.

What this script does (documentary only; no physics is computed here):
  1. for every row of ROWS, opens each cited file and checks by regex (whitespace-normalised) that the cited check id /
     verdict / sentence is present;
  2. checks that the markdown table in CFG60_dispersion_provenance.md carries every row id with the same class, and that
     its TALLY line equals the tally computed from ROWS;
  3. prints 'N of N matched' and exits 0 only if every check matched.
MUTATE mode (env MUTATE=1 or argument --mutate): flips '[PASS]' to '[FAIL]' in the first expectation of row A16 (the
exchange-action check E2b), so that expectation must fail to match; the script then must exit 1.

python3 stdlib only.  Never writes inside the repository.
"""
import os
import re
import sys

REPO = os.environ.get("CFG60_REPO", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(HERE, "CFG60_dispersion_provenance.md")
MUTATE = ("--mutate" in sys.argv) or os.environ.get("MUTATE") == "1"

CF = "campaign_fresh_gravity/"
B44 = CF + "CFG44_fluid_target/"
B48 = CF + "CFG48_gap1_switch/"
AN = CF + "closure_map/ACTIONS_AND_NOGOS.md"
AS = "deepseek_push/astra_spawn_ideas/results/"
DS = "deepseek_push/"

# each row: id, construction, class, hypothesis boundary, source string (for the table), [(file, regex, label)]
ROWS = []


def row(rid, name, cls, boundary, source, checks):
    assert cls in "DPIXU", cls
    ROWS.append(dict(id=rid, name=name, cls=cls, boundary=boundary, source=source, checks=checks))


# ---------------------------------------------------------------- CFG44
row("A01", "CFG44 B1: the exact target (T) and its hydrostatics", "P",
    "Spherical, static, Newtonian; fluid feels only the Newtonian potential of all mass. Then hydrostatics is an identity "
    "(any rho_c >= 0 has an isotropic P) and the whole content is the closure C(r). The target itself is written down, not derived.",
    "B1_target_and_hydrostatics.out S1, S2, N2, N4, 14/14; README.md 'the whole content of the target is the closure'",
    [(B44 + "B1_target_and_hydrostatics.out", r"\[PASS\] S1 \(sympy\) point mass", "S1"),
     (B44 + "B1_target_and_hydrostatics.out", r"\[PASS\] N4 rho_c >= 0 and P > 0 on every profile \(hydrostatics is then an identity", "N4"),
     (B44 + "B1_target_and_hydrostatics.out", r"14/14 checks pass; load-bearing failures: 0", "14/14"),
     (B44 + "README.md", r"the whole content of the target is the closure", "README sentence")])
row("A02", "CFG44 B2: universal barotropic P(rho) in g_tot", "X",
    "Single fluid, P a universal function of its own density rho, gravity = Newtonian total field, spherical: required c_s^2 scales as "
    "M_b^e with e in [1/2,1] at fixed rho, spread >= 10^3 over M_b = 1e8-1e14; effective index runs 2 -> 1. Not covered: any stress that is not a function of rho alone.",
    "B2_barotropic_nogo.out E1, E2, E1n, E1m; README.md table row 1",
    [(B44 + "B2_barotropic_nogo.out", r"\[PASS\] E1 \(sympy\) at FIXED rho the required c_s\^2 scales as M\^e", "E1"),
     (B44 + "B2_barotropic_nogo.out", r"\[PASS\] E2 \(sympy\) the required effective index Gamma", "E2"),
     (B44 + "B2_barotropic_nogo.out", r"9/9 checks pass; load-bearing failures: 0", "9/9")])
row("A03", "CFG44 B2: barotropic fluid plus a symmetric second potential / any fixed-kernel force linear in M_b", "X",
    "Universal barotropic fluid with ANY fixed-kernel force linear in M_b: deep regime forces beta = -1, P ~ rho^3; the Newtonian regime then forces g_felt = 0 "
    "(contradicts GR). Poisson-type symmetric forces (a,b scan): target not barotropic-universal. Not covered: non-linear-in-M_b or non-fixed kernels.",
    "B2_barotropic_nogo.out E3, E4, E4i; README.md row 2",
    [(B44 + "B2_barotropic_nogo.out", r"\[PASS\] E3 \(sympy \+ scan\) no symmetric Poisson-type force", "E3"),
     (B44 + "B2_barotropic_nogo.out", r"\[PASS\] E4 \(sympy\) a universal barotropic fluid with ANY fixed-kernel force linear in M_b", "E4")])
row("A04", "CFG44 B3: local closures (constant charge, P = a0 g_N/8piG, field-energy P, sigma^2 = r nu g_N/2); far-shell theorem", "X",
    "Any closure P = Pi(fields local to r), spherical baryons: identical local fields (< 1e-9) at r* with a far shell added outside R', yet (T) pressure differs by "
    "(a0/2) m/(4 pi R'^2) (+65% for a 10 M_b shell at 40 kpc). Off by 0.3-1.4 dex from (T) on extended profiles.",
    "B3_local_closures.out A2 (L1), A3, A6, A7; README.md row 3",
    [(B44 + "B3_local_closures.out", r"\[PASS\] A2 L1: local fields at r\* identical", "A2"),
     (B44 + "B3_local_closures.out", r"\[PASS\] A3 \(T\) is within 0.25 dex of the P2 law", "A3"),
     (B44 + "B3_local_closures.out", r"9/9 checks pass; load-bearing failures: 0", "9/9")])
row("A05", "CFG44 B3: adiabatic maintenance of (T) as baryons are added", "X",
    "Adding baryons outside R' changes no force inside (shell theorem) yet raises the (T) pressure inside by (a0/2) m/(4 pi R'^2): the inner fluid must be heated by "
    "(3/2) Int dP dV = a0 m R'/4 (a0 R'/4 per unit accreted baryon mass; more than V_f^2 once R' > 4 r_M). Excludes an adiabatic (no-exchange) mechanism only.",
    "B3_local_closures.out A2b; README.md row 4",
    [(B44 + "B3_local_closures.out", r"\[PASS\] A2b the \(T\) pressure inside R' rises", "A2b")])
row("A06", "CFG44 B3: (T) as a local tidal closure, rho_c g = (a0/4piG) T_perp", "P",
    "Spherical baryons only (identity, sympy): the enclosed-mass closure IS a local tidal closure, beta = -(1/2) dlnM_b/dlnr. This restates the target, it does not "
    "derive it. Thin exponential disc: the two readings split by 3-15x (estimate, reported, not a claim).",
    "B3_local_closures.out A5a (identity), A5b (reported estimate)",
    [(B44 + "B3_local_closures.out", r"\[PASS\] A5a \(sympy\) for spherical baryons T_perp", "A5a"),
     (B44 + "B3_local_closures.out", r"\[PASS\] \(reported\) A5b \(reported, estimate\) for a thin exponential disc", "A5b")])
row("A07", "CFG44 B3: locally virialised collisionless fluid, sigma_r^2 = V_c^2/2 with beta = -(3/2) rho_b/rhobar_b", "P",
    "Jeans identity derived (residual < 1e-3); beta(r) is POSTULATED and equals the target; f(E,L) >= 0 (anisotropic positivity) is OPEN; spherical, static, Newtonian. "
    "Survives 'as an equilibrium', not as a mechanism.",
    "B3_local_closures.out A4; README.md row 'locally virialised collisionless fluid', 'Not tested: anisotropic f(E,L) positivity'",
    [(B44 + "B3_local_closures.out", r"\[PASS\] A4 the \(T\) fluid is a locally virialised", "A4"),
     (B44 + "README.md", r"β postulated \(equal to the target\)", "README: beta postulated"),
     (B44 + "README.md", r"Not tested: anisotropic f\(E,L\) positivity", "README: not tested")])
row("A08", "CFG44 B4 Q1: state-independent ('field-energy') stress, P = P_b(x) prescribed by the baryons", "X",
    "Linearised radial Euler + continuity (sympy): omega^2 = -i g k, Hadamard ill-posed; the same 'pressure' derived from an action gives zero force (CFG50 W1). "
    "State-dependent temperature P = rho sigma^2(x) is well posed (see A13).",
    "B4_actions_reciprocity.out C1; README.md row 'state-independent field-energy stress'",
    [(B44 + "B4_actions_reciprocity.out", r"\[PASS\] C1 \(sympy\) Q1: a fluid whose stress is a prescribed function of position", "C1")])
row("A09", "CFG44 B4 Q2: (T) imposed as a Lagrange constraint on a barotropic fluid", "X",
    "Newtonian spherical action with multiplier lambda: the multiplier gravitates, g = G(M_b + M_c + 4 pi r^2 lambda rho_c)/r^2; GR + real mass needs lambda rho_c = 0 "
    "(redundant with barotropic, excluded by A02) else M_lambda/M_c reaches >= 0.1 (up to 3.4). Excluded under 'GR + real mass'; not covered if the multiplier may gravitate.",
    "B4_actions_reciprocity.out C2; README.md row 'Lagrange-constraint action'",
    [(B44 + "B4_actions_reciprocity.out", r"\[PASS\] C2 \(sympy \+ numbers\) implementing \(T\) as a Lagrange constraint", "C2")])
row("A10", "CFG44 B4 Q2b: density-slaved fluid, rho_c = rho_T[rho_b]", "X",
    "Static limit is (T) by construction, but the energy E = Int mu rho_T depends on the baryons: virtual-work reaction on baryons -1.2 to -4.2 g_law inward at "
    "0.5-10 h of a compact exponential sphere. Excluded by reciprocity (action-derived); spherical, Newtonian.",
    "B4_actions_reciprocity.out C2b; README.md row 'density-slaved fluid'",
    [(B44 + "B4_actions_reciprocity.out", r"\[PASS\] C2b Q2b the functional-derivative machinery", "C2b")])
row("A11", "CFG44 B4 Q3: the fluid feels the law's phantom potential (E_int = Int rho_c U)", "X",
    "Symmetric coupling => reaction -kappa(y) G M_c(<r)/r^2 on the baryons, 0.11-1.5 g_law (P2, nu_mono), reaching >= 0.3 g_law on the compact exponential sphere; "
    "cited as N11/N13. Not covered: a non-reciprocal (non-action) coupling.",
    "B4_actions_reciprocity.out C3; README.md row 'fluid feels the law's phantom potential (N11/N13)'",
    [(B44 + "B4_actions_reciprocity.out", r"\[PASS\] C3 Q3 the reaction formula", "C3")])
row("A12", "CFG44 B4 Q4: additive law (phantom + cosmic-share cold fluid)", "X",
    "Point mass and the exponential spheres: additive law overshoots g by >= 0.2 dex at 3 r_M (+0.43 dex x=3, +0.68 dex x=1); the fluid = phantom reading exhausts the "
    "cosmic cold share at x_cap = 6.29. A bookkeeping exclusion, not a mechanism.",
    "B4_actions_reciprocity.out C4; README.md last paragraph of the exclusion table",
    [(B44 + "B4_actions_reciprocity.out", r"\[PASS\] C4 Q4 an additive law", "C4"),
     (B44 + "B4_actions_reciprocity.out", r"x_cap = 6\.29", "x_cap")])
row("A13", "CFG44 B4 Q5: temperature-slaved fluid, sigma^2(x) prescribed by the baryons", "P",
    "Well posed (self-adjoint) and the outer profile is an attractor (amplitude x0.5-x4 changes g_tot < 2% at x = 1000), but it POSTULATES sigma_inf^2 = (1/2) sqrt(G a0 M_b) "
    "(the BTFR), the cusp amplitude A = a0/(4 pi G) and the nonlocal Sigma_out. Survives as a restatement; the dispersion is an input.",
    "B4_actions_reciprocity.out C5, C5b; README.md row 'temperature-slaved fluid' ('POSTULATES')",
    [(B44 + "B4_actions_reciprocity.out", r"\[PASS\] C5 Q5 the outer profile is an ATTRACTOR", "C5"),
     (B44 + "B4_actions_reciprocity.out", r"\[PASS\] C5b Q5 on the compact exponential sphere", "C5b"),
     (B44 + "README.md", r"but it POSTULATES σ∞² = ½√\(G a₀ M_b\)", "README: POSTULATES")])

# ---------------------------------------------------------------- CFG50
B50 = CF + "CFG50_tidal_closure/"
row("A14", "CFG50 D1: fluid stress a functional of the tidal tensor of an auxiliary baryon-sourced potential Phi_b (multiplier action)", "X",
    "Newtonian weak-field reduction, Phi_b baryon-sourced through a multiplier, coupling assumed to carry the closure force (f = 1 per unit fluid mass): reciprocity gives "
    "a_react = 8 pi G [F_perp' + (F_perp - F_rr)/r] = O(g_law) (R = 0.03-7.3 g_law at r = 0.3-1 h, M_b = 1e9-1e12; smaller for massive spirals); tidal tensor is divergence-free; "
    "cold fluid has S_int = 0. Relativistic completion (dipole-ghost matrix) OPEN.",
    "D1_action_reciprocity_MUTATE_0.out C1a, C1b, C2a, C2b, C3, C4; README.md",
    [(B50 + "D1_action_reciprocity_MUTATE_0.out", r"\[PASS\] C2a \(sympy\) reciprocity theorem", "C2a"),
     (B50 + "D1_action_reciprocity_MUTATE_0.out", r"\[PASS\] C3 \(numeric\) the ghost-free K-coupling supplies at most f_max < 1", "C3"),
     (B50 + "README.md", r"reaction on the baryons is O\(g_law\)", "README: O(g_law)")])
row("A15", "CFG50 D2: well-posedness / local-EOS / ghost ceiling for the tidal closure", "X",
    "A prescribed stress is ill-posed (omega^2 = -i F.k/rho0); no EOS from LOCAL Phi_b fields has the target as static equilibrium (mu_rho = mu_T = 0 then mu_r inconsistent); "
    "largest ghost-free outward force is 0.505 g_tot (mass-independent), never the full closure; FRW: renormalises inertia by 1 + chi Omega_b H^2 (50-3400 at z = 1100) unless Phi_b built on the overdensity (postulated).",
    "D2_wellposed_nogo_MUTATE_0.out W1, W2, W3a-c, W4; README.md",
    [(B50 + "D2_wellposed_nogo_MUTATE_0.out", r"\[PASS\] W2 \(sympy\) no equation of state whose energy depends on x through LOCAL fields", "W2"),
     (B50 + "D2_wellposed_nogo_MUTATE_0.out", r"\[PASS\] W3c \(numeric\) at the ghost boundary the coupling supplies an OUTWARD force of at most ~0\.5 g_tot", "W3c"),
     (B50 + "README.md", r"does not rescue the fluid", "README verdict")])

# ---------------------------------------------------------------- CFG48
row("A16", "CFG48 G4: CFG44's enclosed-mass exchange written as a bilocal action term", "X",
    "Point-mass baryons (isotropic exterior, beta = 0); fluid shell masses fixed (sigma-slaved) or P-slaved; internal energy (3/2) sigma^2 per unit mass. Reaction on baryons outward "
    "0.06 g_law (x=0.3), 0.4-0.5 (x=1), 11-22 (x=30) vs pass line 0.10 at every x in [0.3,30] (frozen gate GH(b) FAIL); must supply 23-50x the baryons' orbital KE "
    "(18-179x in CFG4's r_ta convention, referee). The action is legal and symmetric and encodes the target as a POSTULATE. Not covered: extended baryons, anisotropic f(E,L), "
    "full operator diagonalisation, Lagrange/density-slaved versions (cited, not rerun).",
    "G4_exchange_action.out E0, E1, E2a, E2b, E3i-iii, 7/7; README.md 'Exact hypotheses'; CFG48_REFEREE.md sec (a)",
    [(B48 + "G4_exchange_action.out", r"\[PASS\] E2b the reaction exceeds 0\.10 g_law somewhere on x in \[0\.3, 30\]", "E2b"),
     (B48 + "G4_exchange_action.out", r"\[PASS\] \(reported\) E1 \(reported\) the exchange must supply 1\.5 r_e/r_M times", "E1"),
     (B48 + "G4_exchange_action.out", r"\[PASS\] E3i the force on a fluid shell and the reaction on a baryon shell", "E3i"),
     (B48 + "README.md", r"\*\*GH\(b\) FAIL\*\*", "README: GH(b) FAIL"),
     (CF + "CFG48_REFEREE.md", r"18.179. the baryons' orbital kinetic energy", "referee 18-179x")])
row("A17", "CFG48 G3: history variable (memory / latch) placed inside an action", "X",
    "Reduced discrete action, history a functional of the path, smooth W, f, one-degree-of-freedom toy (structural statement, not a size): the Euler-Lagrange residual at t depends on "
    "later coordinates (advanced dependence, relative strength >= 1e-4). Not covered: advected labels, doubled-field (Schwinger-Keldysh) actions.",
    "G3_history_action_causality.out H1, H2; README.md 'History (G3)'",
    [(B48 + "G3_history_action_causality.out", r"\[PASS\] H1 the LOCAL and LABEL actions have banded Euler-Lagrange residuals", "H1"),
     (B48 + "G3_history_action_causality.out", r"\[PASS\] H2 the size of the advanced dependence", "H2")])
row("A18", "CFG48 G3: prescribed advected label (ownership / cold-mass state carried as a label)", "I",
    "Causal (banded residual) but the label is prescribed: ownership / state as INITIAL DATA (one unmodelled assignment rule). Says nothing about a mechanism.",
    "G3_history_action_causality.out H1 (label causal); README.md 'the only causal carrier is a prescribed label, i.e. ownership as initial data'",
    [(B48 + "G3_history_action_causality.out", r"\[PASS\] H1 the LOCAL and LABEL actions have banded", "H1"),
     (B48 + "README.md", r"ownership as initial data", "README sentence")])
row("A19", "CFG48 G1: Gauss / Noether: enclosed-mass-dependent dark mass carried by a gated shift-symmetric MOND FIELD (no real fluid)", "X",
    "Spherical, static, Newtonian; two fields (Phi, psi), first-derivative Lagrangian, shift-symmetric, ONLY source rho_b, gate prescribed or baryon-slaved: M_dyn = M_b beyond the edge "
    "(negative shell 3.2e11-1.4e13 Msun); the mass-keeping (phantom-density-gated) form is not variational (Helmholtz, asymmetry proportional to W'); prescribed W breaks momentum "
    "conservation by Delta L grad W. Not covered: a second source with its own stress (a real-mass fluid), non-shift-symmetric couplings.",
    "G1_gauss_noether.out C1, C2a, C3, C4a; README.md 'Gauss (G1 C1-C2)'",
    [(B48 + "G1_gauss_noether.out", r"\[PASS\] C2a \(L1\) both ACTION-DERIVED gated forms give M_dyn = M_b beyond the edge", "C2a"),
     (B48 + "G1_gauss_noether.out", r"\[PASS\] C3 \(sympy\) the flux-gated system is formally self-adjoint", "C3")])
row("A20", "CFG48 G5 lead 3: edge stress supplied by the baryons' own pressure (cosmic-share accounting)", "X",
    "Point-mass P2, z = 0, r_e = 0.4 r_ta, gas at sigma^2 = V_c^2/2: baryons at the cosmic share supply P_b/P_c = Omega_b/Omega_c = 0.186 of the edge stress (short by 5.4); frozen "
    "line (<= 0.25 for M_b to 1e13) is NOT met literally (3 g/a0 = 0.29 at 1e13). Reported PARTIAL in README, classed X here because the frozen line fails as stated.",
    "G5_edge_stress_mediator_wall.out L3c, L3ab; README.md lead 3",
    [(B48 + "G5_edge_stress_mediator_wall.out", r"\[PASS\] L3c the lead's accounting", "L3c"),
     (B48 + "README.md", r"baryons at the cosmic share supply P_b/P_c = Omega_b/Omega_c = 0\.186", "README: 0.186")])
row("A21", "CFG48 G5 lead 4: a massless universal mediator carrying the enclosed-mass stress", "X",
    "Massless universal scalar with force alpha g_N and stress alpha g_N^2/(8 pi G): alpha_req = 546, 118, 55, 25 at M_b = 1e10, 1e12, 1e13, 1e14, i.e. 1e5-1e7 over Cassini's 3e-5; "
    "the mediator's own force on baryons is a0/2 = 3.5-24 g_law. Not covered: screened or non-universal mediators (untested).",
    "G5_edge_stress_mediator_wall.out L4a, L4b; README.md lead 4",
    [(B48 + "G5_edge_stress_mediator_wall.out", r"\[PASS\] L4a alpha_req >= 1e2 for M_b = 1e10\.\.1e12", "L4a"),
     (B48 + "README.md", r"overshoots the law it must reproduce", "README: overshoot")])
row("A22", "CFG48 G6: stability of the nonlocal (Volterra enclosed-mass, top-level ball) gates", "U",
    "Not a dispersion construction: a second-variation stability test of a MOND-sector gate on DE12's 24 layers. Result: Volterra gate (baryon-mass reading) has no negative mode on 48/48; "
    "dynamical-mass reading fails 29/48; local gate control fails 44/48. It removes the DE12/DE13 stability wall as the obstruction for a NONLOCAL enclosed-mass gate; no dispersion "
    "mechanism was built on it. Pre-declared instability hypotheses H_V, H_R, H_V2, H_R2 were false (kept). First variation of the ball gate not fed back (OPEN).",
    "G6_nonlocal_gate_stiffness.out C1, C2, H_V, H_R, H_V2, H_R2 (rc=1, 4 load-bearing failures kept); README.md 'The stability result (G6)'",
    [(B48 + "G6_nonlocal_gate_stiffness.out", r"\[FAIL\] H_V \(pre-declared\) the Volterra gate, baryon-mass reading", "H_V"),
     (B48 + "G6_nonlocal_gate_stiffness.out", r"\[FAIL\] H_R2 \(declared after round 1\)", "H_R2"),
     (B48 + "G6_nonlocal_gate_stiffness.out", r"5/9 checks pass; load-bearing failures: 4", "5/9"),
     (B48 + "README.md", r"Gap 1's obstruction is NOT stability", "README sentence")])

# ---------------------------------------------------------------- CFG43
B43 = CF + "CFG43_fluid_tie/"
row("A23", "CFG43: saturating stress cap P <= P_cap = a0^2/8piG in a barotropic Schutz-Sorkin fluid (one action with the a0-Lambda tie)", "X",
    "Single conserved current, EOS barotropic in nu = rho/rho_Lambda, P <= P_cap, linear growth within 5% of LCDM, cap reached at r_M: entry needs a NEW number nu* (nu* = 1 gives c_s^2 = 6e-3, "
    "growth 5-14% of LCDM; nu* >= 2e4-1e7 needed); one nu* engages the cap over a mass window g0^2 = at most about 11x (referee: 'too strong as a ceiling'; 1e4-1e5 only by stacking "
    "unmotivated choices, F >= 0.01 contradicts hydrostatics), against ~1e4 (BTFR). The action exists (A1: Lambda global, no extra local dof; A2: a0(z) flat, Omega_c initial data) but "
    "cap amplitude, shape and irrotational flow are POSTULATED. Not covered: non-barotropic or phase-space-dependent stress; other cap shapes; four-form variant.",
    "A3_cap_entry_form_and_obstruction.out N1, N2, N3-i, N3-ii, N3-iii-a/b, N5; A1 out H-EOS, H-TIE, H-DIRAC-0/1; A2 out A2-d; README.md 'The obstruction (scoped)', referee para",
    [(B43 + "A3_cap_entry_form_and_obstruction.out", r"\[PASS\] N3-iii-b g0 = nu_M/nu_min", "N3-iii-b"),
     (B43 + "A3_cap_entry_form_and_obstruction.out", r"\[PASS\] N5 CFG2 A2's settled medium has P_d = sqrt", "N5"),
     (B43 + "A1_action_field_equations_dof.out", r"\[PASS\] H-TIE as functions of the HT field", "A1 H-TIE"),
     (B43 + "A2_frw_flat_a0_and_dust_limit.out", r"\[PASS\] A2-d Omega_c0 varies freely with the initial data", "A2-d"),
     (B43 + "README.md", r"at most about \*\*11", "README: 11x"),
     (B43 + "README.md", r"too strong as a ceiling", "README: referee caveat")])

# ---------------------------------------------------------------- uncommitted lanes
row("A24", "CFG49 (UNCOMMITTED, lane in progress): dynamical gate scalar chi with a penalty to a baryon-only invariant", "U",
    "A MOND-sector gate, not a fluid-dispersion construction; results so far are linear stability of chi + baryons: chi's mass cannot remove the uniform-limit instability (S2 theorem), "
    "gradient stiffness closes only k > k_c, the theta-source is a ghost (S6b). Directory is untracked (git status '??'), files still changing; only CV6_A_local_linear.out is cited.",
    "campaign_fresh_gravity/CFG49_gate_scalar/CV6_A_local_linear.out S2, S6b, 12/12 (untracked)",
    [(CF + "CFG49_gate_scalar/CV6_A_local_linear.out", r"\[PASS\] S2 \[load-bearing\] THEOREM", "S2"),
     (CF + "CFG49_gate_scalar/CV6_A_local_linear.out", r"12/12 checks pass; load-bearing failures: 0", "12/12")])
row("A25", "CFG44 gap-2 lane (UNCOMMITTED): non-barotropic / order-parameter (FL1-type) fluid, gates frozen", "U",
    "Only GATES_FROZEN.md exists (untracked): gates G1-G6 and controls A1-A4 declared before any solver; L1 (energy density e(n, chi), chi = |grad u|^2), L2 (baryon-sourced phi_b, not run), "
    "CP (constitutive proxy) named. No script, no .out. This is exactly the class CFG43 says its obstruction does not touch.",
    "campaign_fresh_gravity/CFG44_gap2_order_parameter_fluid/GATES_FROZEN.md (untracked)",
    [(CF + "CFG44_gap2_order_parameter_fluid/GATES_FROZEN.md", r"GATES FROZEN BEFORE ANY SOLVER", "frozen header"),
     (CF + "CFG44_gap2_order_parameter_fluid/GATES_FROZEN.md", r"L2 SECOND FIELD: the cap reads a separate baryon-sourced potential phi_b\. Not run", "L2 not run")])

# ---------------------------------------------------------------- CFG9 / CFG10 / FG004 / CFG2 / CFG5 / B / CFG35
row("A26", "CFG9: locally virialised cold component, sigma^2 = V_c^2/2 at every radius, charge a0/4pi per unit baryonic mass", "P",
    "Point mass, isotropic Jeans, virial state and the charge (K, a0 = 4 pi K/M) are the input; then P2 follows exactly (max dev 8.8e-8) and is the only locally virialised law "
    "(nu_beta family). Outside the baryons only: inside real baryons the law's phantom is ~70% hotter than local virial (S1) and a constant charge overshoots (S2). README: 'The lane is half derived'.",
    "CFG9_local_virial.out D1, D2, D3, S1, S2; CFG9_README.md 'Standing'",
    [(CF + "CFG9_local_virial.out", r"\[PASS\] D1 THEOREM: for a point mass P2's phantom", "D1"),
     (CF + "CFG9_local_virial.out", r"\[PASS\] D2 UNIQUENESS", "D2"),
     (CF + "CFG9_local_virial.out", r"\[PASS\] S2 THE INNER DEMAND", "S2"),
     (CF + "CFG9_README.md", r"The lane is half derived", "README")])
row("A27", "CFG10 principle (ii): shell-theorem charge, rho_c g = (a0/3) rhobar_b(<r)", "P",
    "Spherical-equivalent SPARC envelope, one global Upsilon: matches P2-env within +0.0031/+0.0017 dex (H2 PASS). It IS the target; README: 'Why the cold component takes this distribution. "
    "This needs a dynamical derivation'. A postulate with a data pass.",
    "CFG10_inner_closure.out H2, C3, C4; CFG10_README.md 'What stays open'",
    [(CF + "CFG10_inner_closure.out", r"\[PASS\] H2 PRINCIPLE \(ii\) the shell theorem for the charge", "H2"),
     (CF + "CFG10_README.md", r"Why the cold component takes this distribution", "README open item")])
row("A28", "CFG10 principle (i): pressure Gauss law, 4 pi r^2 P = (a0/2) M_b(<r)", "X",
    "Data-scoped exclusion as the inner principle: SPARC 175 galaxies, CFG4's statistic, one global Upsilon, spherical-equivalent envelope: +0.168/+0.175 dex vs P2-env, kill line "
    "+0.02 crossed; demands rho_c < 0 at a median 25% of radii in 116/175 galaxies. Says nothing about (ii).",
    "CFG10_inner_closure.out H1 (FAIL as declared), R0, R1; CFG10_README.md 'Results'",
    [(CF + "CFG10_inner_closure.out", r"\[FAIL\] H1 PRINCIPLE \(i\) the pressure Gauss law", "H1"),
     (CF + "CFG10_README.md", r"Kill line \(\+0\.02\) crossed", "README")])
row("A29", "CFG7 / FG004: is the max-rule (T5) cold component a relaxed ground state (isothermal)?", "X",
    "Isothermal cold component with T5's amount and one sigma stays within 0.1 dex of the law at g_bar > a0: FAILS (+0.13-0.15 dex overshoot); no universal barotropic P = Pi(g_N) "
    "(cross-galaxy scatter 0.51-0.55 dex at fixed rho); the OUTER phantom (g_bar < 0.1 a0) IS relaxed (sigma^2_Jeans/(V_flat^2/2) = 0.92-1.01) - a diagnosis of the law's phantom, "
    "not a derivation. Pre-declared C2 (nu_mono 1% control) and H3 failed as run.",
    "CFG7_groundstate_fg004.out H1, H2 [FAIL], H4, C2 [FAIL], H3 [FAIL]; CFG7_README.md 'FG004'",
    [(CF + "CFG7_groundstate_fg004.out", r"\[FAIL\] H2 \(pre-declared UNCERTAIN\) THE INNER PHANTOM IS THE GROUND STATE", "H2"),
     (CF + "CFG7_groundstate_fg004.out", r"\[PASS\] H1 THE OUTER PHANTOM IS RELAXED", "H1"),
     (CF + "CFG7_groundstate_fg004.out", r"\[PASS\] \(reported\) H4 \(reported\) NO UNIVERSAL BAROTROPIC EQUATION OF STATE", "H4"),
     (CF + "CFG7_README.md", r"the ground state is not a universal barotropic fluid", "README")])
row("A30", "CFG2_A stress-cap principle: hydrostatic dark medium with P_d = sqrt(P_Lambda P_N) (PRINCIPLE ONLY: INCOMPLETE commit 1cbaea5db)", "P",
    "Point-mass theorem (uniquely P2, BTFR exact, column <= a0/2piG) holds given the POSTULATED pressure law P_d = sqrt(P_Lambda P_N) = a0 g_N/(8 pi G); two readings differ inside extended baryons "
    "(1/sqrt3 for M_b ~ r); H7 records design obstructions (gravity-only P = Pi(|g|) is stress-free in the deep regime; isothermal sphere capped at P_Lambda holds <= M_b/3); H8 settled window FAILS (reported). "
    "Cited as principle only: the commit is marked 'INCOMPLETE ... DO NOT CITE'.",
    "CFG2_A_principle.out H2, H6, H7, H8 [FAIL]; closure_map/ACTIONS_AND_NOGOS.md row 'GR + dark field, no MOND field', sec 4 item 1",
    [(CF + "CFG2_A_principle.out", r"\[PASS\] H2 \[HEADLINE\] THE POINT-MASS THEOREM", "H2"),
     (CF + "CFG2_A_principle.out", r"\[PASS\] H7 THE OBSTRUCTION", "H7"),
     (CF + "CFG2_A_principle.out", r"\[FAIL\] \(reported\) H8 \(reported\) THE SETTLED WINDOW", "H8"),
     (AN, r"CFG2/5 sit in an INCOMPLETE commit", "map: INCOMPLETE commit")])
row("A31", "CFG5 stress cap written at shell crossing / collapse (PRINCIPLE ONLY: INCOMPLETE commit 1cbaea5db)", "I",
    "The cap is 'a fossil of collapse' (single stream carries no stress; cap written at shell crossing via FK1 conversion): the dispersion state is set by collapse history. "
    "CFG5_1 P6 [FAIL] (plateau 0.918), CFG5_2 H2a, C0b [FAIL], CFG5_3 H3c, H3d [FAIL] (deep branch not written; BTFR slope/a0_eff). Fluid-side: SPARC 0.164/0.160 vs 0.145/0.142 dex (map). Principle only.",
    "CFG5_1_principle.out P4, P6 [FAIL], rc=1; CFG5_2_collapse.out H2a [FAIL]; CFG5_3_sparc.out H3c, H3d [FAIL]",
    [(CF + "CFG5_1_principle.out", r"\[PASS\] P4 a single cold stream carries no stress", "P4"),
     (CF + "CFG5_1_principle.out", r"\[FAIL\] P6 \[H1\]", "P6"),
     (CF + "CFG5_2_collapse.out", r"\[FAIL\] H2a the dark-only fossil's maximum dark pull", "H2a"),
     (CF + "CFG5_3_sparc.out", r"\[FAIL\] H3c \(the design constraint\)", "H3c"),
     (CF + "CFG5_3_sparc.out", r"\[FAIL\] H3d the primary fossil's BTFR", "H3d")])
row("A32", "Candidate B, T5 bookkeeping (CFG4 target): 'the cold component IS the law's dark density'; dark mass = max(M_ph, (Omega_c/Omega_b) M_b)", "P",
    "An effective law, no action: T5 is an identity and the max rule is DECLARED. It assumes the fluid supplies the phantom; it does not say why the fluid's stress is set by M_b(<r).",
    "CFG4_README.md T5 row ('the max rule is DECLARED'); CFG4_target.out H1, H2; ACTIONS_AND_NOGOS.md Gap 2",
    [(CF + "CFG4_README.md", r"the max rule is \*\*DECLARED\*\*", "README T5"),
     (CF + "CFG4_target.out", r"\[PASS\] \(reported\) H2 THE ADDITIVE READING FAILS", "H2"),
     (AN, r"\*\*Gap 2\. An action in which the conserved cold fluid itself supplies", "map Gap 2")])
row("A33", "CFG35: 'a bound system keeps the cold mass it collapsed with' (conservation form of T5)", "I",
    "Bookkeeping from T4's conservation (pressureless, conserved): cold mass = collapse-time mass, not a function of the enclosed baryons at later times; fixes the X-ray ellipticals "
    "(H1, H1b PASS) but H2 (do not disturb spirals) FAILS. Initial data from collapse.",
    "CFG35_cold_mass_conservation.out H1, H1b, H2 [FAIL]; CFG35_README.md 'The derivation'; map Gap 2 ('bookkeeping from T4, not a variation')",
    [(CF + "CFG35_cold_mass_conservation.out", r"\[FAIL\] H2 \.\.\.WITHOUT DISTURBING THE SPIRALS", "H2"),
     (CF + "CFG35_README.md", r"a bound system keeps the cold mass it collapsed with", "README")])
row("A34", "Dark-fluid actions FL1-FL3 / FK1 (and the V0 dark slot): complex order parameter, Schroedinger-Poisson with the metric potential u", "I",
    "Conserved NR number, amount = initial data; the fluid is kernel-invisible (feels the Newtonian potential only, L353 reciprocity), so it carries no baryon-tracking charge; "
    "its dispersion is whatever collapse leaves. Passes shell crossing (XR8) with a light radial mode. Cited from the map [S]/[M]; FL1 scripts not reopened here.",
    "closure_map/ACTIONS_AND_NOGOS.md Table 1 row 'Dark-fluid actions FL1-FL3, FK1', Gap 2 evidence",
    [(AN, r"conserved NR number, amount = initial data", "map row"),
     (AN, r"FL1 fluid is kernel-invisible", "map Gap 2")])
row("A35", "Astra CA4-GNC / CA5-GNC-R five-carrier action [UNREVIEWED astra lane]", "I",
    "Five real carriers with a diagonal U(1) conserved 'with exchange E' (AS147); abundance = initial data; a0-vacuum relation an optional input; no dispersion mechanism keyed to enclosed "
    "baryon mass is stated in the map row. Every AS result is 'unreviewed' (hermes worker); label as such.",
    "closure_map/ACTIONS_AND_NOGOS.md Table 1 row 'Astra CA4-GNC / CA5-GNC-R'",
    [(AN, r"abundance = initial data", "map row")])

# ---------------------------------------------------------------- closure_map N-rows that bear on the question
row("A36", "closure_map N9: condensate mu-pincer and no-go H1-H4 [M: memory note only]", "X",
    "Charge dust rho = Q0 n, u = -Q0 Psi, n ~ a^-3, Newtonian growth: cannot be CMB/forest-cold and absent from galaxies; c_s(z=3) >= 20 km/s. Does NOT touch a separate dark field with its own "
    "action (FL1). Source tag [M]: script not reopened by the map's compiler or by me.",
    "closure_map/ACTIONS_AND_NOGOS.md N9",
    [(AN, r"\| N9 \| Condensate mu-pincer and no-go H1-H4 \|", "N9 row"),
     (AN, r"cannot be CMB/forest-cold and absent from galaxies", "N9 hypothesis")])
row("A37", "closure_map N10: Gauss / flux switch (L352 + L346/7/8)", "X",
    "Switch acts on the MOND flux with a local x threshold: phantom is a divergence, M_dyn = M_b beyond the edge, negative shell. Does NOT touch a source-confined density edge or a time-triggered "
    "vacuum gate. (Same statement as A19, from the earlier L352 script.)",
    "closure_map/ACTIONS_AND_NOGOS.md N10 [S] g03_audit_2026/L352",
    [(AN, r"\| N10 \| Gauss / flux switch", "N10 row"),
     (AN, r"M_dyn = M_b beyond the edge", "N10 hypothesis")])
row("A38", "closure_map N11: reciprocity (L353 N2)", "X",
    "A static Lagrangian's species-response matrix is symmetric, so a kernel-invisible component feels no phantom; L321/L322 'additive' law non-Lagrangian. Does NOT touch the FP22 Einstein-frame "
    "coupling (postulated, costs dark-baryon WEP) or the real-mass reading of B.",
    "closure_map/ACTIONS_AND_NOGOS.md N11 [S] g03_audit_2026/L353",
    [(AN, r"\| N11 \| Reciprocity \(L353 N2\)", "N11 row"),
     (AN, r"a kernel-invisible component feels no phantom", "N11 hypothesis")])
row("A39", "closure_map N13: private phantom + LCDM-like dark component double counts (L363)", "X",
    "Isolated-phantom halo model, phantom 4-5x halo mass inside 1 Mpc: shear R 2.9-4.7; mock-based passes retracted. T5's identity (dark = max, no double count) is unscored as a shear row.",
    "closure_map/ACTIONS_AND_NOGOS.md N13 [S] L363, MS3",
    [(AN, r"\| N13 \| Private phantom \+ LCDM-like dark component double counts", "N13 row")])
row("A40", "closure_map N17: shell crossing (XR8, L374)", "X",
    "L374's 1-D test: no single-velocity fluid of any EOS or dispersion order passes. Does NOT touch a complex Cartesian order parameter with a light radial mode (FL1), collisionless phase space, "
    "or Galileon cubic. So a dispersion mechanism must live in a multi-stream / phase-space fluid.",
    "closure_map/ACTIONS_AND_NOGOS.md N17 [S] XR8_README.md",
    [(AN, r"\| N17 \| Shell crossing \(XR8, L374\)", "N17 row"),
     (AN, r"no single-velocity fluid of any EOS or dispersion order passes", "N17 hypothesis")])
row("A41", "closure_map N20: fluid-settling constraints", "X",
    "Gravity-only P = Pi(|g|) is stress-free in the deep regime inside diffuse baryons (BTFR broken by (r_M/R)^2); isothermal sphere capped at P_Lam holds <= M_b/3, nu(1) <= 4/3 < sqrt 2 (CFG2 A6); "
    "no local barotropic P = Pi(g_N) where baryons sit (scatter 0.51-0.55 dex); relaxed component overshoots +0.13..+0.15 dex at g_bar > a0 (FG004). Does NOT touch the shell-theorem charge (CFG10 ii).",
    "closure_map/ACTIONS_AND_NOGOS.md N20 [S] CFG2_A, CFG7_groundstate_fg004.py, CFG10",
    [(AN, r"\| N20 \| Fluid-settling constraints", "N20 row"),
     (AN, r"no local barotropic P = Pi\(g_N\) where baryons sit", "N20 hypothesis")])

# ---------------------------------------------------------------- astra / deepseek (READ-ONLY, unreviewed)
row("A42", "AS080 [UNREVIEWED, deepseek astra_spawn_ideas]: isothermal hydrostatics in an imposed log well gives gamma = C/sigma^2; Poisson self-consistency selects sigma^2 = C/2", "P",
    "Conditional theorem: log well Phi = C ln r (deep-regime potential of the point source, an ansatz in the interior), P = sigma^2 rho, Poisson self-consistency. The result's own limitations: "
    "sigma^2 = C/2 is derived only conditional on {hydrostatics, isothermal EOS, log well, Poisson}; unfiltered kernels only; no attainment, no formation. sigma^2 is an input of an isothermal closure.",
    "deepseek_push/astra_spawn_ideas/results/AS080/run_20260928T131319Z_as080_e004c2aa/result.json (exact_claim, limitations; acceptance_state 'unreviewed')",
    [(AS + "AS080/run_20260928T131319Z_as080_e004c2aa/result.json", r"gamma = 2 iff sigma\^2 = C/2", "exact_claim"),
     (AS + "AS080/run_20260928T131319Z_as080_e004c2aa/result.json", r'"acceptance_state": "unreviewed"', "unreviewed"),
     (AS + "AS080/run_20260928T131319Z_as080_e004c2aa/result.json", r"No propagation, no attainment, no formation", "limits")])
row("A43", "AS081 / AS086 [UNREVIEWED]: static equilibrium bookkeeping (self-source vs imposed well; virial with both surfaces)", "P",
    "Equilibrium relations (rho = A/r^2, sigma^2 = C/2, P = sigma^2 rho, equipartition M_ph(<r_M) = M_b) are 'adopted inputs, not derived'; AS086: sigma^2 = C/2 exactly from the twin-surface virial "
    "with the closure P = sigma^2 rho, 'no dynamics, no time evolution, no attainment of the equilibrium'. Static, Newtonian-integration bookkeeping.",
    "deepseek_push/astra_spawn_ideas/results/AS081/.../result.json (limitations); AS086/AS086-r1-20260928T133517/result.json (limitations)",
    [(AS + "AS081/run_20260928T132023Z_as081-9023b0b5/result.json", r"adopted inputs, not derived here", "AS081 limits"),
     (AS + "AS086/AS086-r1-20260928T133517/result.json", r"no dynamics, no time evolution, no attainment of the equilibrium", "AS086 limits")])
row("A44", "AS087 [UNREVIEWED]: interior finite-shell virial for sigma^2 with a central point baryon", "X",
    "Point baryon M_b at the centre, phantom rho = A/r^2, isothermal closure at both surfaces, imposed log well, r_in/R in {0.01,0.1,0.5}, R/r_M in {0.62,1}: sigma^2 = (C/2) F, F = 1.69-8.46 "
    "(interior virial does NOT reproduce C/2); C/2 only in the deep exterior single-counted local balance or with truncation-consistent bookkeeping. Boundary-condition dependence, not a mechanism.",
    "deepseek_push/astra_spawn_ideas/results/AS087/AS087-r1-20260928T1336Z-dsv4f-hermes/result.json (exact_claim, limitations)",
    [(AS + "AS087/AS087-r1-20260928T1336Z-dsv4f-hermes/result.json", r"interior imposed-log-well virial does NOT reproduce C/2", "exact_claim")])
row("A45", "deepseek_push track (OUTSIDE the named scope; read-only, unreviewed): Q001 'sound-speed identity' sigma_Z^2 = c_s^2 = sqrt(G M_b a0)/2 and Q004", "P",
    "Its own label: 'DERIVED-CONSTITUTIVE' (a constitutive EOS, not a relaxation product), and Q004 'balance selects no sigma^2; sigma^2 = C/2 is an identification input'. By the rubric this is a postulate "
    "of the dispersion. Cited from the state sheet (not reopened).",
    "deepseek_push/CROSS_TRACK_STATESHEET.md line 20 (Q001, Q004)",
    [(DS + "CROSS_TRACK_STATESHEET.md", r"G035's N-body kill resolved as a category error \(constitutive EOS, not a relaxation product\)", "Q001"),
     (DS + "CROSS_TRACK_STATESHEET.md", r"sigma²=C/2 is an identification input", "Q004")])
row("A46", "deepseek_push track (OUTSIDE the named scope; unreviewed): G035 Newtonian free-dust attainment kill and Q009 (equilibrium is neutral, not an attractor)", "X",
    "Newtonian free dust placed in the baryon well does not relax onto the phantom equilibrium (G035, S2 <= 0.30 in the Newtonian control); the capped isothermal phantom is a critical/neutral "
    "equilibrium (omega^2 = 0 exactly), not a strict attractor (G081/Q009). Hypothesis: collisionless Newtonian dust, spherical. The scalar-mediated arm was only pre-registered (A47).",
    "deepseek_push/CROSS_TRACK_STATESHEET.md line 20 (Q009); deepseek_push/G111_relaxation_spec.md sec 1",
    [(DS + "CROSS_TRACK_STATESHEET.md", r"the equilibrium is NEUTRAL, not an attractor; the live kill is G035 dust attainment", "Q009"),
     (DS + "G111_relaxation_spec.md", r"G035's dust-attainment kill stands as the Newtonian control", "G111 sec 1")])
row("A47", "deepseek_push G111: pre-registered relaxation N-body spec (scalar-mediated arm S vs Newtonian arm N) [UNREVIEWED spec]", "U",
    "Frozen spec and a JSON whose keys are spec / question / arms / parameters / acceptance / verdicts (verdicts are about the spec's completeness, V1-V3). No relaxation result is claimed by the spec; "
    "I did not locate an executed G111 run.",
    "deepseek_push/G111_relaxation_spec.md 'PRE-REGISTERED SPEC'; G111_results.json keys",
    [(DS + "G111_relaxation_spec.md", r"PRE-REGISTERED SPEC \(frozen before any G111 run", "G111 spec")])
row("A48", "campaign_fresh_gravity_astra (UNREVIEWED, untracked dir): scalar statics DP1/SD1 and coupled-matter stability MS1", "U",
    "Searched READMEs and stage results for a cold-fluid dispersion or stress set by baryons: none. MS1 is a linear stability test of responsive barotropic matter coupled to a scalar "
    "(Jeans-type growing branch), DP1/SD1 are scalar statics (map row); stage 06 PF1 is a pressure-inference functional for clusters. Not a construction of the dispersion.",
    "campaign_fresh_gravity_astra/stage_04/matter_stability/RESULT.md; closure_map/ACTIONS_AND_NOGOS.md row 'campaign_fresh_gravity_astra scalar'",
    [("campaign_fresh_gravity_astra/stage_04/matter_stability/RESULT.md", r"MS1 result: coupled matter is the missing stability test", "MS1"),
     (AN, r"\*\*campaign_fresh_gravity_astra scalar\*\* \(DP1, SD1, MS1; untracked dir\)", "map row")])

# ---------------------------------------------------------------- Table B: N-rows screened out (do not bear on the dispersion)
for rid, nm, rx, why in [
    ("B01", "closure_map N12: web external field on the kernel", r"\| N12 \| Web external field on the kernel", "kernel/KiDS external-field bound; no fluid stress"),
    ("B02", "closure_map N14: gate as a varied term (DE12/DE13)", r"\| N14 \| Gate as a varied term", "MOND-sector gate stiffness; the switch, not the dispersion"),
    ("B03", "closure_map N15: theta-gate mirror lemma (XR36)", r"\| N15 \| theta-gate mirror lemma", "turnaround gate ghosts; the switch"),
    ("B04", "closure_map N16: dark-sector window (FK1 kick)", r"\| N16 \| Dark-sector window", "kick/conversion window; B needs no kick"),
    ("B05", "closure_map N18: xi irreducible (FP17)", r"\| N18 \| xi irreducible", "threshold-mass theorem; ownership"),
    ("B06", "closure_map N19: kappa", r"\| N19 \| kappa \|", "kappa = 1/2 fitted; no fluid stress"),
]:
    row(rid, nm, "U", "Screened out as not bearing on the frozen question (" + why + "); not a test of the dispersion, so U (untested for this question).",
        "closure_map/ACTIONS_AND_NOGOS.md " + nm.split(":")[0].split()[-1], [(AN, rx, nm.split(":")[0].split()[-1] + " row")])


# =====================================================================================================
def norm(s):
    return re.sub(r"\s+", " ", s)


_cache = {}


def read(rel):
    if rel not in _cache:
        p = rel if os.path.isabs(rel) else os.path.join(REPO, rel)
        try:
            with open(p, encoding="utf-8", errors="replace") as f:
                _cache[rel] = norm(f.read())
        except OSError:
            _cache[rel] = None
    return _cache[rel]


def tally():
    t = {k: 0 for k in "DPIXU"}
    for r in ROWS:
        t[r["cls"]] += 1
    return t


def tally_line():
    t = tally()
    return "TALLY: D=%d P=%d I=%d X=%d U=%d TOTAL=%d" % (t["D"], t["P"], t["I"], t["X"], t["U"], len(ROWS))


def main():
    if "--emit-table" in sys.argv:
        for grp, pred in (("A", lambda r: r["id"].startswith("A")), ("B", lambda r: r["id"].startswith("B"))):
            print("<!-- TABLE %s -->" % grp)
            print("| ID | Construction | Class | Exact hypothesis boundary | Committed source (file, check / verdict id) |")
            print("|---|---|---|---|---|")
            for r in ROWS:
                if pred(r):
                    print("| %s | %s | **%s** | %s | %s |" % (r["id"], r["name"], r["cls"], r["boundary"], r["source"]))
        print(tally_line())
        return 0

    checks = []  # (row id, label, ok, detail)
    mutated = False
    for r in ROWS:
        for i, (f, rx, label) in enumerate(r["checks"]):
            if MUTATE and r["id"] == "A16" and i == 0:
                rx = rx.replace(r"\[PASS\]", r"\[FAIL\]")  # corrupt one expected string
                mutated = True
            txt = read(f)
            if txt is None:
                checks.append((r["id"], label, False, "missing file %s" % f))
                continue
            ok = re.search(norm(rx), txt) is not None
            checks.append((r["id"], label, ok, f))

    # markdown consistency
    md_ok = True
    md_detail = []
    if not os.path.exists(MD):
        md_ok = False
        md_detail.append("markdown file missing")
    else:
        md = open(MD, encoding="utf-8").read()
        for r in ROWS:
            m = re.search(r"^\| %s \| .*? \| \*\*([DPIXU])\*\* \|" % re.escape(r["id"]), md, re.M)
            if not m:
                md_ok = False
                md_detail.append("row %s missing from md table" % r["id"])
            elif m.group(1) != r["cls"]:
                md_ok = False
                md_detail.append("row %s class md=%s script=%s" % (r["id"], m.group(1), r["cls"]))
        if tally_line() not in md:
            md_ok = False
            md_detail.append("TALLY line in md differs from script: %s" % tally_line())
        # the frozen question must appear verbatim
        q = ("Does any committed construction give the cold fluid's velocity dispersion (equivalently its pressure or stress, "
             "C(r) = rho_c r^3 g_tot = (a0/4 pi) M_b(<r)) as set by the ENCLOSED BARYONIC MASS through a dynamical mechanism, as opposed to "
             "being initial data from collapse or a postulate? The answer is one of: YES (name the construction and its exact hypotheses), "
             "NO (with the exact hypothesis boundary of each excluded class and each surviving restatement), or UNDECIDED (list what was not run). "
             "A scoped NO is a valid answer.")
        if norm(q) not in norm(md):
            md_ok = False
            md_detail.append("frozen question not verbatim in md")
    checks.append(("MD", "markdown table ids, classes, TALLY, frozen question", md_ok, "; ".join(md_detail) or MD))

    n = len(checks)
    matched = sum(1 for c in checks if c[2])
    for rid, label, ok, detail in checks:
        if not ok:
            print("  [NO MATCH] %s %s :: %s" % (rid, label, detail))
    print(tally_line())
    print("%d of %d matched%s" % (matched, n, "   (MUTATE mode: one expected string corrupted%s)" % (" in A16/E2b" if mutated else "") if MUTATE else ""))
    return 0 if matched == n else 1


if __name__ == "__main__":
    sys.exit(main())
