#!/usr/bin/env python3
"""
K_AUDIT (result) -- LOOPHOLE 1 of the channel-B no-go does NOT break; it closes harder.

Attempted escape: a beyond-Bekenstein (higher-derivative / DHOST) coupling that cancels the
anisotropic slip GW-safely, evading the conformal+disformal dichotomy the original no-go used.

Outcome: the NULL-CONE LEMMA closes it without Bekenstein, coupling-independently.

  1. Photons are conformally invariant in 4D: light sees only the CONFORMAL class of the metric it
     couples to. GW170817 fixes c_light = c_GW (to ~1e-15).
  2. Lorentzian causal-structure theorem: two metrics with identical null cones are CONFORMALLY
     related. So GW-safe  <=>  g_matter = Omega^2(x) g_grav -- for ANY coupling (higher-derivative,
     DHOST, curvature), because it constrains the causal structure, not the coupling's form.
  3. Under that (forced) conformal relation the ONLY freedom is a scalar shift domega(phi):
     lensing potential (Phi+Psi) is INVARIANT; dynamical potential Phi -> Phi + domega. Universal
     lensing=dynamics then needs domega = (Psi-Phi)/2 -- a universal function of phi -- but the slip
     (Phi-Psi) solves lap(Phi-Psi) ~ traceless d_i phi d_j phi, not proportional to phi. No universal
     domega(phi) cancels it. (Same wall as conformal in the original no-go, now for ALL couplings.)
  4. MAGNITUDE: channel B needs an O(1) slip (a whole second channel; slope 1->2). Any non-conformal
     (anisotropic) piece able to cancel an O(1) slip is O(1) strength -> c_GW - c_light = O(1), ~1e15x
     the GW170817 bound. Not a fine tuning -- a catastrophic violation.

Run: python3 opus_48_extended_research/kappa_audit_2026/K_AUDIT_loophole1_closure.py   (sympy)
"""
import sympy as sp

Phi, Psi, dw = sp.symbols('Phi Psi domega', real=True)
Phi_t, Psi_t = Phi + dw, Psi - dw                         # GW-forced conformal shift
lensing = sp.simplify(Phi_t + Psi_t)                      # light deflection ~ (Phi+Psi)
need = sp.solve(sp.Eq(lensing, 2*Phi_t), dw)[0]           # lensing=dynamics <=> Phi+Psi = 2 Phi_dyn

print("="*90)
print("LOOPHOLE 1 (beyond-Bekenstein coupling) -- attempt to break it")
print("="*90)
print(f"  GW-forced conformal relation g_matter = Omega^2 g_grav (null-cone lemma; coupling-free).")
print(f"  lensing potential (Phi+Psi) under conformal = {lensing}   [INVARIANT]")
print(f"  dynamical potential Phi -> {Phi_t}")
print(f"  universal lensing=dynamics requires domega = {need} = (Psi-Phi)/2, a universal fn of phi;")
print(f"  the slip (Phi-Psi) ~ solution of lap = traceless d_i phi d_j phi is NOT a fn of phi -> fails.")
print(f"  and the slip to cancel is O(1) -> any anisotropic (non-conformal) cancellation is an O(1)")
print(f"  GW170817 violation (~1e15 x the bound).")
assert sp.simplify(lensing - (Phi + Psi)) == 0 and sp.simplify(need - (Psi - Phi)/2) == 0

print("\nVERDICT: loophole 1 CLOSES (generic case). The no-go is now coupling-INDEPENDENT: GW-safe")
print("forces the matter metric conformal to the graviton metric (any derivative order), and conformal")
print("cannot cancel the anisotropic O(1) slip that engages channel B. Higher-derivative/DHOST does not")
print("help -- the constraint is on the null cone, not the Lagrangian's form.")
print("\nRESIDUAL SLIVER (honest, not fully excluded): a fine-tuned DHOST-degenerate construction that")
print("keeps c_GW=c_light while carrying an O(1) UNSCREENED slip. But that is exactly the fifth-force")
print("slip the post-GW170817 DHOST class suppresses, and it would still have to deliver gamma=1")
print("unscreened AND slope 2 simultaneously. A dedicated DHOST-degeneracy scan is the one thing that")
print("would kill it outright; the null-cone + O(1)-magnitude arguments close the generic case.")
print("\n=> channel-B no-go now stands against loophole 1. Remaining open: loophole 2 (non-metric")
print("second channel -- abandons PD01's identification) and loophole 3 (non-universal gamma).")
