#!/usr/bin/env python3
"""CK02 -- the replacement coupling: what the clock sector must do instead, computed.
(1) A disformal split between the metric gravity acts on and the metric photons ride is RELATIONAL: for g~ = g + B n n the graviton
    and photon cones differ by B/2 whichever sector carries B (sympy on the two cones), so 'moving the disformal term into the
    gravitational sector' cannot rescue PAPER24 sec. 5 -- the only cure is one metric for every species.
(2) With matter, photons and gravitons on ONE metric the GW170817 photon-graviton delay is identically zero (the cones coincide),
    and the force law must come from the AeST-type coupling carried by the clock's constraint (matter minimal on g), the
    construction of FINAL_THEORY_CANDIDATE_2026-09-05 (f30-f35, g03b-g03h).
(3) In that construction the scalar's alpha_1 drag is -4(2 - K_B)/(J_Y(1 + xi^2 k^2) + 1) (f31/f31c, exact propagator form): at
    Saturn with the record's ephemeris floor xi >= 4.00 pc (L47) it is <= 1e-9 for every K_B, J_Y on the ladder -- NO clock
    alignment is needed, so PAPER25's floor s_0 >= 1.5e7 is withdrawn with the coupling that required it; the sector's own
    positivity bound s_0 >= 2 (PAPER24 sec. 3) stands.
(4) Which PAPER24/25 results stand and which fall (records located in the tex files).  Both a0 footings where a0 enters; a FAIL is a finding."""
import os, json, math
import sympy as sp
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("CK02 -- the replacement coupling for the clock sector\n")
# ------------------------------------------------------------------ 1. the split is relational
print("=" * 100); print("1. g~ = g + B n n: the photon cone (on g~) vs the graviton cone (on g), in the clock's rest frame"); print("=" * 100)
B = sp.symbols('B', positive=True); k0 = sp.symbols('k0', real=True); k1 = sp.symbols('k1', positive=True)
g = sp.diag(-1, 1, 1, 1); n_dn = sp.Matrix([-1, 0, 0, 0]); gt = g + B * n_dn * n_dn.T
kvec = sp.Matrix([k0, k1, 0, 0])
cone_gt = sp.solve(sp.Eq((kvec.T * gt.inv() * kvec)[0], 0), k0)
v2_gt = [sp.simplify((c / k1) ** 2) for c in cone_gt]                                   # both roots share the speed squared
split = sp.series(sp.sqrt(1 - B) - 1, B, 0, 2).removeO()
check("1a photons on g~ move at sqrt(1 - B) relative to gravitons on g (whose cone is |k0| = |k1|): the cones differ by B/2 at first order, exactly as the record's gw170817_check found",
      len(cone_gt) == 2 and all(sp.simplify(v2 - (1 - B)) == 0 for v2 in v2_gt) and sp.simplify(split + B / 2) == 0, f"v_photon^2 = {v2_gt[0]}, split = {split}")
# the 'other assignment': gravity on g~ (EH built from g~), photons on g = g~ - B n n
gt2 = g; g2 = gt2 - B * n_dn * n_dn.T            # now photons ride g2 = g~ - B n n while gravitons ride g~ = g
cone_ph2 = sp.solve(sp.Eq((kvec.T * g2.inv() * kvec)[0], 0), k0); v_ph2 = max(abs(sp.simplify(c / k1)) for c in cone_ph2)
split2 = sp.series(v_ph2 - 1, B, 0, 2).removeO()
check("1b moving the disformal term to the gravitational sector only flips the sign of the split (photons faster by B/2): the difference is a property of the PAIR of metrics, so no assignment of the term removes it -- one metric for every species is the only cure",
      sp.simplify(split2 - B / 2) == 0, f"other assignment: v_photon - v_graviton = {split2}")
# ------------------------------------------------------------------ 2. one metric: zero delay
print("\n" + "=" * 100); print("2. one metric: the photon and graviton cones coincide for every potential, so the GW170817 delay is identically zero"); print("=" * 100)
U, V = sp.symbols('U V', real=True)
gm = sp.diag(-(1 - 2 * U), 1 + 2 * V, 1 + 2 * V, 1 + 2 * V)       # any weak-field metric, potentials U (time) and V (space), shared
cone_m = sp.solve(sp.Eq((kvec.T * gm.inv() * kvec)[0], 0), k0)
v2_m = [sp.simplify((c / k1) ** 2) for c in cone_m]                 # both roots give the same speed squared
check("2a on one metric the photon's coordinate speed sqrt((1 - 2U)/(1 + 2V)) is the graviton's too: the arrival difference is 0 for any U, V (including the phantom's log potential): GW170817 satisfied by structure, not by a number",
      len(cone_m) == 2 and all(sp.simplify(v2 - (1 - 2 * U) / (1 + 2 * V)) == 0 for v2 in v2_m), f"v^2 = {v2_m[0]} for both roots")
# ------------------------------------------------------------------ 3. the alpha_1 drag in the screened single-metric coupling at Saturn
print("\n" + "=" * 100); print("3. the scalar's alpha_1 drag -4(2 - K_B)/(J_Y (1 + xi^2 k^2) + 1) at Saturn (k = 1/r) with xi = 4.00 pc (L47) and xi = 0.03 pc (g03d)"); print("=" * 100)
PC, AU = 3.0857e16, 1.496e11; r_sat = 9.5 * AU
rows = {}
for xi_pc in (4.00, 0.03):
    for KB in (0.2, 0.5):
        for JY in (1.0, 11.0):
            XI2 = (xi_pc * PC / r_sat) ** 2; drag = -4 * (2 - KB) / (JY * (1 + XI2) + 1)
            rows[(xi_pc, KB, JY)] = drag
            print(f"    xi = {xi_pc:5.2f} pc, K_B = {KB}, J_Y = {JY:4.0f}: (xi k)^2 = {XI2:.1e} -> alpha_1 drag = {drag:.1e}")
OUT["alpha1_drag"] = {f"xi{k[0]}/KB{k[1]}/JY{k[2]}": v for k, v in rows.items()}
check("3a at the L47 floor xi = 4.00 pc the scalar's alpha_1 drag at Saturn is <= 1e-9 on the whole (K_B, J_Y) ladder: 1e5 below the bound with NO clock alignment; the aether's own alpha_1 = -4 c_14 is what remains (c_14 <= 2.5e-5)",
      all(abs(v) <= 1e-9 for k, v in rows.items() if k[0] == 4.00), f"max |drag| at 4 pc = {max(abs(v) for k, v in rows.items() if k[0] == 4.00):.1e}")
check("3b even at the g03d floor xi = 0.03 pc the drag is <= 2e-5 (below 1e-4): the screening, not the alignment, closes the gate on every floor on the record; PAPER25's s_0 >= 1.5e7 was the price of the dead coupling",
      all(abs(v) <= 2e-5 for k, v in rows.items() if k[0] == 0.03), f"max |drag| at 0.03 pc = {max(abs(v) for k, v in rows.items() if k[0] == 0.03):.1e}")
# ------------------------------------------------------------------ 4. what stands, what falls (records)
print("\n" + "=" * 100); print("4. PAPER24/25: what stands and what falls"); print("=" * 100)
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); P = os.path.join(ROOT, "qwen_claude_field_theory", "papers_2026")
t24 = open(os.path.join(P, "PAPER24_the_decoupling_locus_2026.tex")).read(); t25 = open(os.path.join(P, "PAPER25_a_clock_that_must_run_fast_2026.tex")).read()
ledger = [("PAPER24 sec 2-3: the decoupling locus W_0 = 0, rho_3/rho = 1/(s_0 - 1), s_0 >= 2, pi_3/pi_grav <= 0.044", "STANDS", "statements about the sector's background, no matter coupling involved"),
          ("PAPER24 sec 4: a_0 = lambda^3/(12 pi G beta s_0) from lambda phi rho_m", "FALLS", "normalisation of the dead coupling; in the single-metric coupling a_0 enters through J's argument scale and the static law is the T-B double filter's (g03d)"),
          ("PAPER24 sec 5: gamma = 1 from the disformal matter metric; alpha_1 = 8 f_s; v_residual <= 4.6 m/s", "FALLS", "the disformal matter metric is excluded by GW170817 (CK01): photon-graviton delay 1.8-2.3 yr"),
          ("PAPER25 entirely: the alignment, s_0 >= 1.5e7, m_rel = 6.8e-12, P_X/d = 1.5e11", "FALLS", "the requirement was the price of the dead coupling; in the screened single-metric coupling the scalar's alpha_1 drag is <= 1e-9 with no alignment (Part 3)"),
          ("L217's flat-a_0 drift ceiling w <= 5.7e-7 and L223's board for the force-law coupling", "FALLS", "both used a_0 = lambda^3/(12 pi G beta s_0); the acoustic ceiling w <= 1e-4 (L201) stands"),
          ("L186-L201 cold clustering sector; L224/L225 forest and growth", "STANDS", "no matter coupling enters; a_0 does not enter")]
for a, b, c in ledger: print(f"    {b:6s} {a}\n           {c}")
OUT["ledger"] = ledger
check("4a the records: PAPER24's sec 5 and PAPER25's abstract state the disformal coupling in their own words (located), and the ledger above has 2 STANDS / 4 FALLS entries (a count of the table, not a physics result)",
      "disformal coupling along a unit timelike vector" in t24 and "disformally along the clock's own unit timelike direction" in t25 and sum(1 for _, st, _ in ledger if st == "STANDS") == 2 and sum(1 for _, st, _ in ledger if st == "FALLS") == 4)
n, n_pass = len(CH), sum(CH)
print(f"\nCK02 COMPLETE: {n_pass}/{n} checks PASS.")
print("""VERDICT (constructive).  The clock sector keeps its cosmology and loses only its force-law coupling.  The replacement is fixed by two
computed facts: (i) a disformal split is relational, so every species must ride ONE metric; (ii) on one metric the force law has to be
sourced through the clock's constraint (matter minimal on g, the AeST mechanism carried by the clock) with the scalar screened inside
xi -- the 2026-09-05 construction, which already passes the quadrupole (g03d), gamma = 1 (f32/f33), alpha_1 = -4 c_14 (f33), health at
the corner (f34), c_T = c, and, by Part 3, needs no clock alignment: the ten-million clock rate of PAPER25 was the price of the dead
coupling and is withdrawn with it.  What the merged construction still owes (CLOCK_WORK_ORDER CK05-CK15): the Ward identity, the
Dirac count, FLRW with the clock, ONE number for xi_min, the alpha_2 reconciliation, causality, perturbations, the galactic solve.
Nothing here derives kappa.""")
json.dump(dict(pass_=n_pass, n=n, **OUT), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "CK02_results.json"), "w"), indent=1, default=str)
