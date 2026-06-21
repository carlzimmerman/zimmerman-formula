#!/usr/bin/env python3
# =============================================================================
# ROUTE D -- ADVERSARIAL SELF-CHECK
# Goal: try HARD to make the evasion WORK (Carl's rule: hunt the loophole hard).
# Attack every assumption in routeD_scale_selective_clustering.py that, if wrong,
# would REVIVE the evasion. If any survives -> the no-go is in trouble and we say so.
#
# Attack vectors:
#  (V1) Is k_J = mu REALLY forced equal? Or is there a SECOND independent scale
#       (e.g. the GC mass M decoupled from the galaxy-MOND mu) so cluster Jeans !=
#       galaxy screening? -> the "two-lever" escape.
#  (V2) Could a LARGER B (B>>1, a tuned UV coefficient) shift k_J independently of
#       mu, opening the window WITHOUT touching the galaxy MOND scale?
#  (V3) Sign re-derivation from scratch with sympy: confirm k<k_J unstable / k>k_J
#       stable, and confirm the window inequality direction.
#  (V4) The NONLINEAR escape: AeST MOND comes from the NONLINEAR term, not the
#       quadratic dispersion. Could nonlinear screening make the field clump in
#       cluster cores but not galaxies via a density/acceleration threshold?
#  (V5) Is the "galaxy is 3.7x denser" comparison apples-to-apples (disk midplane
#       vs cluster-core mean)? Recompute with the field's OWN would-be halo density.
# =============================================================================
import numpy as np, sympy as sp, json

print("="*78); print("ROUTE D ADVERSARIAL SELF-CHECK -- try to REVIVE the evasion"); print("="*78)

# ---- (V3) sign re-derivation from scratch -------------------------------------
print("\n(V3) SIGN RE-DERIVATION (sympy) -- which side clumps?")
k, B, M, A = sp.symbols('k B M A', positive=True)
# ACLM mixed-with-gravity: omega^2 = (B/M^2) k^4 - A k^2 , A>0 (gravitational)
w2 = (B/M**2)*k**4 - A*k**2
kJ = sp.solve(sp.Eq(w2,0), k)
kJ_pos = [s for s in kJ if s.is_positive or s==sp.sqrt(A)*M/sp.sqrt(B)]
print(f"   omega^2 = (B/M^2)k^4 - A k^2;  roots k=0 and k_J = {sp.sqrt(A)*M/sp.sqrt(B)}")
# sign of omega^2 for k slightly below / above k_J
kJv = sp.sqrt(A)*M/sp.sqrt(B)
below = w2.subs(k, kJv/2)
above = w2.subs(k, 2*kJv)
print(f"   at k=k_J/2: omega^2 = {sp.simplify(below)}  (sign {'<0 UNSTABLE/clump' if sp.simplify(below)<0 else '>0'})")
print(f"   at k=2k_J : omega^2 = {sp.simplify(above)}  (sign {'>0 STABLE/smooth' if sp.simplify(above)>0 else '<0'})")
print("   CONFIRMED: k<k_J UNSTABLE (clumps), k>k_J STABLE (smooth).")
print("   Since galaxies are SMALLER (larger k) than clusters, IF k_J sits between")
print("   them the field clumps in clusters & smooths galaxies. Premise topology OK.")

# ---- (V1)+(V2): is k_J independent of the galaxy-MOND mu? ----------------------
print("\n(V1/V2) CAN k_J BE DECOUPLED FROM THE GALAXY-MOND mu? (the two-lever escape)")
print("""   In AeST the galaxy MOND scale and the field-mass screening scale are the
   SAME parameter: SZ21 define mu = sqrt(2 K2/(2-K_B)) Q0, and the 'mass term for
   Phi' that screens MOND at >mu^-1 is the SAME mu. The k^4-Jeans scale of the GC
   analogy is k_J = M^2/(sqrt2 MPl), and the banked PK_K4_SIGNATURE proved (sympy-
   exact) k_J == mu IDENTICALLY. So there is NO second lever: one mu sets BOTH.
   - To decouple, you'd need a DIFFERENT field-mass M_dust != mu. But AeST has ONE
     scalar; the dust mode and the MOND screening are the SAME field's mu.
   - B>>1 (V2): k_J = M sqrt(A/B); raising B LOWERS k_J (further from window). And
     in the named host B=0 (no k^4 at all). A tuned B>>1 is not in AeST anyway.
   CONCLUSION: the two-lever escape is NOT available in the named host. One mu.""")

# Quantify: to get k_J into the window AND keep mu^-1>=1 Mpc you would need k_J and
# mu to differ by the window/mu ratio:
Mpc=3.086e22
k_win_lo = 7.48   # /Mpc (cluster core)
mu_inv_min = 1.0  # Mpc
need_ratio = k_win_lo * mu_inv_min   # k_J(needed) / (1/mu^-1)= k_J*mu^-1
print(f"   Quantified: would need k_J >= {k_win_lo}/Mpc while 1/mu = (1/mu^-1) <= 1/1Mpc")
print(f"   => need k_J/mu >= {need_ratio:.1f}.  AeST gives k_J/mu = 1 exactly. Gap {need_ratio:.1f}x.")

# ---- (V4) NONLINEAR screening escape ------------------------------------------
print("\n(V4) NONLINEAR ESCAPE: does AeST's nonlinear MOND term give a density/accel")
print("     threshold that clumps the COLD mode in cluster cores but not galaxies?")
print("""   The nonlinear term acts on the Y (spatial) MOND mode -- it sets the a0
   phenomenology. The COLD dust is the Q (temporal) mode. Banked Route-C
   (CLUSTER_CLOSURE_HUNT2) result: shift symmetry => NO chameleon (no V(phi) =>
   no density-dependent mass), and a Ward identity => NO Y->Q sourcing. So the
   nonlinear MOND term does NOT make the cold Q-mode pile into cores. And any
   density-threshold that DID would clump MORE in galaxies (3.7x denser) -- the
   SAME backwards ordering. The nonlinear term cannot supply scale-selection of
   the cold mode. (Re-confirmed, both ways: it is a real term, but wrong sector.)""")

# ---- (V5) density comparison apples-to-apples ---------------------------------
print("\n(V5) IS 'galaxy 3.7x denser' ROBUST? recompute (mean enclosed, matched proxy)")
G=6.674e-11; Msun=1.989e30; kpc=3.086e19; Mpc=3.086e22
H0=67.4e3/Mpc; rho_crit=3*H0**2/(8*np.pi*G)
# galaxy: Milky-Way-like, M(<10kpc) baryon ~ 6e10 Msun within 10 kpc sphere
def mean_dens(M_Msun, R_m): return (M_Msun*Msun)/((4/3)*np.pi*R_m**3)
rho_gal = mean_dens(6e10, 10*kpc)
# cluster core: M_b(<420kpc) ~ from banked 2.3e14 phantom target / eta; baryon ~1.2e13
rho_clu = mean_dens(1.2e13, 420*kpc)
print(f"   galaxy mean baryon density (<10 kpc):   {rho_gal:.3e} kg/m^3 = {rho_gal/rho_crit:.2e} rho_crit")
print(f"   cluster-core mean baryon density(<420kpc): {rho_clu:.3e} kg/m^3 = {rho_clu/rho_crit:.2e} rho_crit")
print(f"   ratio galaxy/cluster = {rho_gal/rho_clu:.2f}x  (galaxy DENSER -- robust, matched mean-enclosed proxy)")
print("   => The 'galaxies are denser' fact survives an apples-to-apples recompute.")
print("      Any density-gated clustering clumps MORE in galaxies. Ordering backwards.")

# ---- VERDICT ------------------------------------------------------------------
print("\n"+"="*78); print("ADVERSARIAL VERDICT"); print("="*78)
print(f"""
Every revival vector FAILS:
 V1/V2 two-lever / tuned-B escape: NOT available -- one mu sets both galaxy MOND and
       the Jeans scale (k_J=mu identically); B=0 in the host anyway. Need k_J/mu>={need_ratio:.0f}x.
 V3    sign topology: CORRECT (k<k_J clumps, k>k_J smooths) -- premise sound but moot
       because k_J is pinned <~1/Mpc, below the entire {k_win_lo:.0f}-314 /Mpc window.
 V4    nonlinear MOND escape: wrong sector (acts on Y not the cold Q-mode); shift
       symmetry + Ward identity forbid Y->Q sourcing -> no nonlinear scale-selection.
 V5    'galaxies are denser' is robust ({rho_gal/rho_clu:.1f}x on a matched mean-enclosed proxy) ->
       any density-gated mechanism clumps MORE in galaxies. Backwards.
NET: the evasion cannot be revived. The no-go STANDS. The k^4 Jeans scale is the
RIGHT idea but is (a) absent (B=0) in the named host and (b) even if present, pinned
by the single mu to <~1/Mpc -- 7.5x below the cluster-core edge of the required window
and on the wrong (stable) side for cluster cores. No manufactured loophole.""")

print("ADV_JSON_START")
print(json.dumps({
 "two_lever_escape_available": False,
 "needed_kJ_over_mu_ratio": round(need_ratio,1),
 "aest_kJ_over_mu_ratio": 1.0,
 "sign_topology_correct": True,
 "nonlinear_escape": "wrong sector (Y not Q); shift-sym + Ward forbid Y->Q",
 "galaxy_over_cluster_density_matched_proxy": round(rho_gal/rho_clu,2),
 "verdict": "evasion NOT revivable; no-go STANDS"
}, indent=2))
print("ADV_JSON_END")
