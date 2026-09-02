#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
merger_gate_supported_media_2026.py -- merging clusters as a rigidity / signal-speed meter: what the dark component must be.
================================================================================================================================
A dark medium that holds itself up against gravity (pressure: the polytrope; rigidity: the solid; phonon pressure: a superfluid
core) has a signal speed fixed by that support.  At the stall, elastic stress = weight: mu s = rho g r  =>  c_T^2 = mu/rho = g r/s;
for the polytrope c_s^2 = |Psi| c^2; for a superfluid core c_s ~ v_c.  All are ~ the circular velocity.  A cluster merger moves the
potential wells at v_merge = 3-5 v_c.  Two consequences, both measured:
  (1) LAG.  A supported medium re-pins to a moving well on the crossing time L/c_T; the lensing peak trails the galaxies by
      Delta x ~ v_merge L / c_T.  Bullet cluster (1E 0657-56): lensing peaks coincide with the galaxy concentrations to <~ 50 kpc
      (Clowe+ 2006), core L ~ 200 kpc, subcluster velocity ~ 3000 km/s (Springel & Farrar 2007; shock 4700 km/s, Markevitch 2006).
  (2) NO PASS-THROUGH.  A single-valued medium cannot multistream; two dark cores colliding at Mach v_merge/c_T ~ 5-10 within the
      medium either merge inelastically (one central peak) or would need to store the collision energy elastically and rebound;
      the elastic capacity M c_T^2 falls short of M v_merge^2/2 by (v_merge/c_T)^2/2.  The Bullet has two receding dark peaks.
  (3) WHAT THE PEAKS NEED.  MOND phantom of the subcluster's stars alone vs the lensing mass at the galaxies' position
      (Bradac+ 2006: ~2.3e14 Msun within 250 kpc; stars ~1e13): the ballistic dark mass the peaks require.
Both a_0 footings.  Checks CAN fail.  Both ways: Abell 520 (a dark core AT the gas, Jee+ 2012, contested by Clowe+ 2012) is the
one counter-datum and is recorded, not hidden.
"""
import sys, math
P = lambda *a: print(*a, flush=True); FAILS = []; NCHK = [0]
def check(name, ok, detail=""):
    NCHK[0] += 1; P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))
    if not ok: FAILS.append(name)
def info(s): P("  " + s)
G = 6.674e-11; c = 2.99792458e8; Mpc = 3.0857e22; kpc = Mpc/1e3; Msun = 1.989e30
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
V_MERGE = 3000e3; V_SHOCK = 4700e3; L_CORE = 200*kpc; DX_MAX = 50*kpc          # Bullet: Springel & Farrar 2007; Markevitch 2006; Clowe+ 2006
M_LENS = 2.3e14*Msun; R_LENS = 250*kpc; M_STARS = 1e13*Msun                   # Bradac+ 2006 within 250 kpc; stellar mass ~1e13 (round)
V_C = 1100e3                                                                   # cluster circular velocity scale, (g r)^(1/2) at ~ Mpc
P("="*100); P("A. the signal speed of a supported medium is the circular velocity, whatever supports it"); P("="*100)
d_cl = 1600.0                                                                  # the solid's cluster cap at the G3b sweet spot
cT_solid = math.sqrt(V_C**2/math.log(d_cl))                                    # stall: mu s = rho g r -> c_T^2 = g r / ln(delta)
cs_poly = math.sqrt(0.5*V_C**2)                                                # polytrope: c_s^2 = |Psi| ~ v_c^2/2 (log potential, order unity)
cs_sf = V_C                                                                    # superfluid core: phonon speed ~ v_c to hold the core up
info(f"solid at its stall (delta = {d_cl:.0f}): c_T = sqrt(g r / ln delta) = {cT_solid/1e3:.0f} km/s")
info(f"polytrope in the well:            c_s = sqrt(|Psi|) ~ {cs_poly/1e3:.0f} km/s")
info(f"superfluid core:                  c_s ~ v_c = {cs_sf/1e3:.0f} km/s")
info(f"merger speed {V_MERGE/1e3:.0f} km/s (shock {V_SHOCK/1e3:.0f}): Mach in the medium = {V_MERGE/cT_solid:.1f} (solid), {V_MERGE/cs_poly:.1f} (polytrope), {V_MERGE/cs_sf:.1f} (superfluid)")
check("A1 every supported medium is supersonic in a Bullet-class merger: v_merge / c >= 2.5 for the solid, the polytrope and the superfluid core",
      min(V_MERGE/cT_solid, V_MERGE/cs_poly, V_MERGE/cs_sf) >= 2.5)
P(""); P("="*100); P("B. the lag: a supported medium re-pins on L/c, and trails the galaxies by v_merge L / c"); P("="*100)
for name, cc in (("solid", cT_solid), ("polytrope", cs_poly), ("superfluid", cs_sf)):
    lag = V_MERGE*L_CORE/cc; info(f"{name:11s}: response time L/c = {L_CORE/cc/3.156e16:.2f} Gyr, lag = {lag/kpc:.0f} kpc   (observed peak-galaxy offset <= {DX_MAX/kpc:.0f} kpc)")
need_c = V_MERGE*L_CORE/DX_MAX
info(f"to keep the lag under {DX_MAX/kpc:.0f} kpc the medium needs c >= v_merge L/dx = {need_c/1e3:.0f} km/s = {need_c/c:.3f} c -- a hot medium, which the forest and the CMB forbid (pincer C4, G3)")
check("B1 the lag of every supported medium exceeds the observed peak-galaxy offset by > 10x (Bullet cluster)", min(V_MERGE*L_CORE/cc for cc in (cT_solid, cs_poly, cs_sf))/DX_MAX > 10,
      f"min lag / max offset = {min(V_MERGE*L_CORE/cc for cc in (cT_solid, cs_poly, cs_sf))/DX_MAX:.0f}")
P(""); P("="*100); P("C. no pass-through: elastic capacity vs collision energy"); P("="*100)
ratio = 0.5*V_MERGE**2/cT_solid**2
info(f"solid: E_kin / E_elastic,max ~ v_merge^2 / (2 c_T^2) = {ratio:.0f}: the collision cannot be stored and returned elastically; a supersonic (Mach {V_MERGE/cT_solid:.0f}) impact of two single-valued media shocks and merges into ONE central peak")
info("observed: TWO dark peaks, each on the far side of its gas, receding (Clowe+ 2006; Markevitch+ 2004) -- the cores passed through each other")
check("C1 the solid's elastic capacity falls short of the Bullet's collision energy by > 10x: no rebound, and no pass-through for any single-valued medium", ratio > 10, f"ratio = {ratio:.0f}")
P(""); P("="*100); P("D. what the peaks need: MOND phantom of the stars vs the lensing mass at the galaxies' position"); P("="*100)
for foot, a0 in A0.items():
    gN = G*M_STARS/R_LENS**2; nu = math.sqrt(1 + a0/gN); Mmond = nu*M_STARS
    info(f"{foot:10s}: g_N(stars, 250 kpc) = {gN:.2e} m/s^2 = {gN/a0:.2f} a_0 -> nu = {nu:.2f}, MOND dynamical mass = {Mmond/Msun:.1e} Msun vs lensing {M_LENS/Msun:.1e}: short by {M_LENS/Mmond:.0f}x; ballistic dark mass required ~ {(M_LENS - Mmond)/Msun:.1e} Msun")
short = min(M_LENS/(math.sqrt(1 + a0/(G*M_STARS/R_LENS**2))*M_STARS) for a0 in A0.values())
check("D1 MOND + the subcluster's stars fall short of the lensing peak by > 5x on both footings: the peak is ~2e14 Msun of something that moved ballistically with the galaxies", short > 5, f"min shortfall = {short:.0f}x")
P(""); P("="*100); P("E. the class verdict, and the counter-datum"); P("="*100)
info("supported media (polytrope, solid, superfluid core, any pinned condensate) : c ~ v_c  ->  lag ~ Mpc, no pass-through  ->  EXCLUDED by the Bullet")
info("ballistic particles (CDM, WDM, sterile neutrinos)                          : pass through, no lag                       ->  allowed by the Bullet")
info("linearly superposable waves (fuzzy DM)                                      : solitons pass through with interference       ->  allowed; but the forest needs m >= 2e-20 eV,")
info("                                                                              whose de Broglie length is sub-kpc: it forms galaxy halos like CDM (the pincer's double count returns)")
info("El Gordo (z = 0.87, v ~ 2500 km/s, Menanteau+ 2012): the same lag argument, x0.8 the Bullet's.  Abell 520: a dark core at the gas position (Jee+ 2012),")
info("disputed (Clowe+ 2012); if real it would favour a lagging medium in that one system.  Recorded; it does not remove the Bullet.")
P(""); P("="*100); P("VERDICT"); P("="*100)
P("  Cluster mergers are a signal-speed meter for the dark component, and the reading is unambiguous: whatever carries the ~2e14 Msun")
P("  under the Bullet's galaxies moved with them at 3000 km/s and passed through its twin.  No medium that holds itself up in a well can")
P("  do that -- its speed is the circular velocity, 5-10x too slow -- and no single-valued medium can pass through itself.  The solid,")
P("  the polytrope and the superfluid core all fail here, after passing everything else.  What survives is ballistic (or a superposable")
P("  wave), and ballistic-and-cold forms galaxy halos.  The road to 'no dark matter' ends at the Bullet cluster, from a new direction.")
P(f"\nRESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
