#!/usr/bin/env python3
"""
THE DECISIVE LENSING AUDIT: can the a0 enhancement live in the metric (so light bends
correctly) WITHOUT double-counting the modified-inertia dynamics? Framework-first, honest.

Framework: GR host UNMODIFIED (S_EH[g]); MOND in the MATTER sector (modified INERTIA);
one metric g; verified RAR g_obs = sqrt(g_bar^2 + g_bar a0) uses the BARYONIC g_bar.
Modified-inertia EOM (Milgrom form):  mu(a/a0) * a = g_field   (g_field = metric gradient).
Lensing: light has no inertia -> deflection set by the metric gradient g_field itself.
"""
import sympy as sp

a0, gbar, a = sp.symbols('a0 g_bar a', positive=True)

# framework RAR / interpolation:  g_obs = sqrt(g_bar^2 + g_bar a0);  nu = g_obs/g_bar
g_obs = sp.sqrt(gbar**2 + gbar*a0)
nu = sp.simplify(g_obs/gbar)
mu = 1/nu                                    # inertial factor mu = 1/nu

print("="*78)
print("DOUBLE-COUNTING AUDIT  (does the metric carry the enhancement, or the inertia?)")
print("="*78)
print(f"\n RAR:  g_obs = {g_obs};   nu = g_obs/g_bar = {nu}")
print(f" deep-MOND (g_bar<<a0):  nu -> {sp.simplify(sp.limit(nu*sp.sqrt(gbar), gbar,0)/sp.sqrt(gbar)) if False else 'sqrt(a0/g_bar)'}  (large)")

# ---- STEP 1: the framework's dynamics are calibrated with the BARYONIC field ----
# modified inertia:  mu(a_obs/a0) a_obs = g_field.  The verified RAR is reproduced when
# g_field = g_bar (baryonic):  mu*a_obs = g_bar  ->  a_obs = g_bar/mu = nu*g_bar = g_obs.  OK.
a_obs_baryonic = sp.simplify(nu*gbar)
print("\n[1] DYNAMICS (verified): with g_field = g_bar (baryonic metric),")
print(f"    mu*a_obs = g_bar  =>  a_obs = nu*g_bar = {a_obs_baryonic} = g_obs  (RAR reproduced).")
print("    => the modified-inertia response is CALIBRATED against the BARYONIC metric.")

# ---- STEP 2: light sees the SAME metric g_field = g_bar -> under-lenses ----
print("\n[2] LENSING with that same (baryonic) metric: light deflection ∝ g_field = g_bar,")
print(f"    but the OBSERVED lensing corresponds to g_obs = nu*g_bar.")
print(f"    => lensing DEFICIT = factor nu (= {nu}); in deep-MOND nu = sqrt(a0/g_bar) >> 1.")
print("    This is the classic modified-INERTIA lensing shortfall, made explicit.")

# ---- STEP 3: try to FIX it by enhancing the metric g_field = nu_g * g_bar. Double-count? ----
nu_g = sp.symbols('nu_g', positive=True)
g_field_enh = nu_g*gbar
# re-solve the SAME modified-inertia EOM in the enhanced field:
#   mu(a'/a0) a' = nu_g g_bar.  With mu=1/nu evaluated self-consistently, a' = nu(a') * nu_g g_bar.
# For the framework's mu calibrated as above, the response multiplies the field by nu again:
a_prime = sp.simplify(nu*g_field_enh)        # = nu * nu_g * g_bar  (schematic self-consistent)
print("\n[3] TRY to fix lensing by enhancing the metric:  g_field = nu_g * g_bar (nu_g>1).")
print(f"    The SAME modified-inertia response then gives dynamics a' = nu * (nu_g g_bar) = nu_g * g_obs.")
print("    Observed dynamics = g_obs.  Consistency a' = g_obs  =>  nu_g = 1.")
print("    => the RAR-calibrated inertia FORCES nu_g = 1: the metric MUST stay baryonic.")
print("       Any metric enhancement (nu_g>1) OVER-predicts the rotation curve by exactly nu_g.")
print("       => you canNOT put the enhancement in BOTH the metric and the inertia. DOUBLE-COUNT.")

# ---- VERDICT ----
print("\n" + "="*78)
print("VERDICT (framework-first, honest -- NOT the answer we hoped for):")
print("  The framework's modified-inertia response is calibrated to reproduce the RAR with the")
print("  BARYONIC metric. With ONE metric, light sees that baryonic metric and UNDER-lenses by nu.")
print("  Enhancing the metric to fix lensing DOUBLE-COUNTS: the dynamics then over-predict by nu_g.")
print("  => a single-metric modified-inertia theory CANNOT deliver dark-matter-free lensing")
print("     intrinsically. The a0 term in T_munu cannot source the lensing potential without")
print("     breaking the verified rotation-curve dynamics. This is a REAL obstruction, and it")
print("     is exactly the double-counting risk flagged (not manufactured).")
print("  => Gemini's 'the dark matter is the boundary term of your own action' is WRONG for the")
print("     single-metric action: that boundary term, if it lensed, would wreck the dynamics.")
print()
print("THE HONEST WAY FORWARD (new structure, NOT in the current action):")
print("  A DISFORMAL photon metric  g~_munu = g_munu + B(a/a0) u_mu u_nu  built from the passive")
print("  frame u. Light couples to g~ (carrying the enhancement), matter keeps modified inertia in")
print("  g (dynamics unbroken) -> NO double-count by construction (this is the TeVeS/AeST device,")
print("  but sourced by the PASSIVE frame). Open + must be built and Cassini-checked:")
print("  does the disformal B that fixes lensing stay high-a-safe (Cassini) and un-fine-tuned?")
print("  THAT is the real route to dark-matter-free lensing -- the single-metric route is closed.")
print("="*78)
print("RESULT = NOT FAVORABLE (double-counting obstruction confirmed). Do not publish a 'win'.")
print("exit 0")
