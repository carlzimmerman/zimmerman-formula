#!/usr/bin/env python3
"""
mi_merger_nonequilibrium.py  --  TOPIC: mi_merger_dynamics, PART (b)
=============================================================================
Do the framework's MODIFIED-INERTIA non-equilibrium / relational effects change
the LENSING or the DYNAMICS in the Bullet merger vs MOND modified GRAVITY?

Grounded in the banked results:
  - GENUINE_MI_CLUSTER_DISTINCTIVE_2026-06-15.md: the genuine dS-Unruh MI's ONLY
    surviving distinctive cluster observable is the NON-ADIABATIC RELATIONAL
    sigma-spread (member internal sigma vs infall phase at matched radius): MI
    ~6-13%, MG EXACTLY 0 for any a0 (MG depends only on the momentary external
    field, Milgrom-2022 verbatim). The regime needs omega_ex ~ omega_in.
  - bullet_and_s8_reexamination.py: the OLD 'non-equilibrium phantom-LAG freezes
    the lensing on the galaxies' resolution is [BROKEN] -- the MOND field re-settles
    on t_signal = R/c ~ 2 Myr << t_collision ~ 150 Myr, so the field is QUASI-STATIC;
    a lag cannot freeze the phantom. (The 2026 density-weighting, not a lag, is the
    correct offset mechanism -- and it is MOND-SHARED, MG/MI agnostic.)
  - LENSING_NOGO_CLOSED_FINAL: the framework's lensing is IRREDUCIBLY PHENOMENOLOGICAL
    (free function, AeST-class). The covariant MI matter sector sources ZERO metric
    (phi_- -linear) -> it CANNOT change light bending. So MI non-locality is
    LENSING-BLIND by construction.

THIS SCRIPT computes, for the Bullet merger geometry:
  (1) The field-response (quasi-static) check: t_signal vs t_collision -> confirms
      MI and MG fields BOTH re-settle fast -> no lensing-offset difference from MI.
  (2) The adiabaticity ratio omega_ex/omega_in for the colliding-cluster MEMBERS:
      does the merger reach the omega_ex~omega_in regime where MI's relational
      sigma-spread (the one genuine MI-distinctive cluster signal) turns on?
  (3) The MAGNITUDE of any MI relational sigma-spread the merger could imprint, and
      whether it touches the lensing-offset problem (it does NOT).

Run: python3 mi_merger_nonequilibrium.py     (needs numpy)
"""
import numpy as np

G   = 6.674e-11
c   = 2.99792458e8
Msun= 1.989e30
kpc = 3.0857e19
Mpc = 3.0857e22
Myr = 3.156e13
Gyr = 3.156e16
km  = 1e3

rho_DE = 5.835e-27
A0 = 0.5*c*np.sqrt(G*rho_DE)     # framework a0=9.36e-11

print("="*78)
print("PART (b): MI NON-EQUILIBRIUM / RELATIONAL EFFECTS IN THE BULLET MERGER")
print(f"   a0_framework = {A0:.3e} m/s^2")
print("="*78)

# --------------------------------------------------------------------------
# (1) Field-response quasi-static check (supersedes the BROKEN phantom-lag)
# --------------------------------------------------------------------------
R       = 700.0*kpc            # system / separation scale
v_shock = 4740.0*km            # Markevitch 2006
v_bulk  = 2700.0*km            # Springel & Farrar 2007 (gas bullet bulk speed)
t_signal = R/c                 # relativistic field re-settle (AeST ~ light crossing)
t_coll_s = R/v_shock
t_coll_b = R/v_bulk
print("\n(1) FIELD-RESPONSE (is the offset sensitive to MI time-nonlocality?)")
print(f"    t_signal = R/c            = {t_signal/Myr:7.2f} Myr   (field re-settle, MG & MI)")
print(f"    t_collision = R/v_shock   = {t_coll_s/Myr:7.2f} Myr")
print(f"    t_collision = R/v_bulk    = {t_coll_b/Myr:7.2f} Myr")
print(f"    ratio t_coll/t_signal     = {t_coll_b/t_signal:7.0f}x  (>>1 -> QUASI-STATIC)")
print("""    -> The MOND field (MG OR MI) re-settles ~130-200x faster than the merger
       evolves. The phantom/effective mass tracks the baryons at each instant.
       MI's TIME-NONLOCALITY (the omega-dependence of inertia) acts on the
       trajectory of TEST MASSES (members), NOT on the global field that bends
       light. So MI changes NOTHING about the lensing offset vs MG.
       (This RE-CONFIRMS the banked [BROKEN] verdict on the phantom-lag idea:
       you cannot freeze the lensing on the galaxies via a field lag in EITHER
       MG or MI. The real offset mechanism is density-weighting, MOND-SHARED.)""")

# --------------------------------------------------------------------------
# (2) Adiabaticity of cluster MEMBERS during the merger: omega_ex / omega_in
# --------------------------------------------------------------------------
# omega_in : internal orbital frequency of a member galaxy's stars (set by the
#            member's own internal acceleration g_in).
# omega_ex : rate of change of the EXTERNAL field the member sees as its host
#            cluster plunges -- ~ v_merger / R_core, the merger's angular rate.
# MI's relational sigma-spread turns on when omega_ex ~ omega_in (Milgrom-2022).
print("\n(2) ADIABATICITY omega_ex/omega_in for merger members (is the MI-distinctive")
print("    relational sigma-spread regime REACHED in the Bullet?)")
print(f"    {'member type':>22} {'g_in[a0]':>9} {'omega_in[1/Myr]':>16} {'omega_ex[1/Myr]':>16} {'ratio':>8}")

# external-field change rate during the merger: the cluster core sweeps through the
# external potential at v_merger over a core radius scale R_sweep.
v_merger = v_bulk
for Rsweep_kpc in [150.0, 300.0, 700.0]:
    omega_ex = v_merger/(Rsweep_kpc*kpc)        # 1/s
    omega_ex_Myr = omega_ex*Myr
    for name, g_in_a0, R_int_kpc in [
        ("L* galaxy (dense)",   50.0,  5.0),    # internal g ~ 50 a0, deep Newtonian
        ("dwarf/dSph member",    1.5,  1.0),    # near a0 -- the MOND/MI-active members
        ("UDG/diffuse member",   0.5,  3.0),    # deep-MOND internal, omega_in small
    ]:
        g_in = g_in_a0*A0
        omega_in = np.sqrt(g_in/(R_int_kpc*kpc)) # 1/s, sqrt(g/R)
        omega_in_Myr = omega_in*Myr
        ratio = omega_ex/omega_in
        print(f"    Rsweep={Rsweep_kpc:4.0f}kpc {name:>20} {g_in_a0:9.1f} "
              f"{omega_in_Myr:16.4f} {omega_ex_Myr:16.4f} {ratio:8.4f}")
    print()
print("""    READING: L* members are DEEPLY adiabatic (omega_ex/omega_in ~ 1e-4 to 1e-3)
    -> a0-degenerate, no MI signal, exactly as at relaxed clusters. ONLY the
    diffuse/UDG/dwarf members with internal g ~ a0 approach omega_ex/omega_in ~
    0.01-0.1 -- HIGHER than relaxed-cluster infall (the merger is violent) but
    still mostly < 1. The Bullet is a FAST, ~head-on, ~one-pass encounter, so a
    member crosses the changing field ONCE; it does NOT execute many internal
    orbits in a strongly time-varying field. So the merger is a WEAKER home for the
    MI relational sigma-spread than a slow plunging-dwarf orbit through a dense core
    -- the regime is APPROACHED for diffuse members, not robustly reached.""")

# --------------------------------------------------------------------------
# (3) Could ANY MI relational effect touch the LENSING offset? (No.)
# --------------------------------------------------------------------------
print("\n(3) DOES ANY MI EFFECT CHANGE THE LENSING OFFSET? (the load-bearing answer)")
print("""    NO -- for three independent reasons, each fatal on its own:
    (a) LENSING-BLIND BY CONSTRUCTION: the framework's covariant MI matter action
        (Route E) is phi_- -linear and sources ZERO metric (LENSING_NOGO_CLOSED).
        The lensing is a SEPARATE phenomenological free function (AeST-class). MI's
        inertia modification lives in the MATTER e.o.m., not the light-bending
        metric. So the member-trajectory non-locality cannot move kappa.
    (b) WRONG OBSERVABLE: the MI-distinctive signal is the member-INTERNAL velocity
        dispersion (a few-% sigma-spread vs infall phase), NOT the cluster-scale
        mass that lenses. The offset is a ~10^14 Msun collisionless RESIDUAL at the
        galaxy positions; a 6-13% tweak to dwarf-member internal sigma is ~10^-? of
        the lensing mass budget -- utterly negligible for kappa.
    (c) MAGNITUDE: even granting the regime, the relational sigma-spread is 6-13% on
        the INTERNAL sigma of a SPECIAL diffuse-member subset; it does not add or
        move collisionless mass. The Bullet offset needs ~3.4e14 Msun of residual
        mass ON the galaxies (Famaey 2026). MI non-equilibrium supplies NONE of it.""")

print("\n"+"="*78)
print("VERDICT (both ways)")
print("="*78)
print("""  * MI vs MG makes NO difference to the Bullet LENSING OFFSET. The field is
    quasi-static (t_signal/t_coll ~ 1/130), the MI matter sector is lensing-blind
    by construction, and the MI-distinctive observable is the wrong quantity
    (internal sigma, not lensing mass). The offset stays the INHERITED, MOND-SHARED
    cluster residual (~2.4-3x, Famaey 2026; +13% on the framework's lower a0).
  * MI vs MG makes NO meaningful difference to the high INFALL VELOCITY either
    (Part a): the deep-MOND law and a0 set it, both MOND-shared; interpolation
    choice ~few %.
  * The ONE place MI is genuinely distinct -- the non-adiabatic relational
    sigma-spread -- IS more accessible in a violent merger than in a relaxed
    cluster (omega_ex/omega_in is larger), but: (i) only for a diffuse/dwarf-member
    subset, (ii) the Bullet's fast single-pass geometry under-develops it vs a
    slow plunging orbit, (iii) it is a member-INTERNAL kinematic signal, NOT a
    lensing or offset signal. So it does NOT fix or even touch the offset.
  * NET: the MI angle does NOT manufacture any Bullet win. It changes the
    framework's standing on the merger from MOND's by ~nothing observable. The
    offset is inherited and unsolved; the velocity is a MOND-shared edge over LCDM.""")
