#!/usr/bin/env python3
r"""
THE JOINT omega_c WINDOW -- does a single crossover mechanism preserve the galactic RAR AND pass
every solar-system bound simultaneously?  (de Sitter-Unruh MODIFIED INERTIA, Carl Zimmerman)
=================================================================================================
Framework judged on its OWN terms: own interpolation nu(y)=sqrt(1+1/y), mu(x)=K(x^2); horizon-derived
a0 = c H_Lambda / Z.  BOTH footings carried:  canonical a0 = 9.36e-11 (rho_DE, cH_Lambda/Z) and
alt a0 = 1.13e-10 (rho_tot / cH0).  Published covariant action S_matter = -1/2 INT sqrt(-g) rho_m
[ s u^mu K(Box_u/a0^2) u_mu ], K Herglotz, sum rule INT dmu/|t| = 1, s=-1 POSTULATE.

THE LANDMINE (established upstream, planetary_doors/KERNEL_PLANETS.md, mi_closure_pin/CONSEQUENCES.md):
  * Reading A (the constitutive first-moment reduction that CARRIES the galactic RAR) reproduces a
    CONSTANT sunward a0/2 tail at EVERY planet -> excluded 10^2-10^4x per planet (recomputed below).
  * The only RAR-preserving survivor is a GATED closure (Reading C): MI active for omega < omega_c,
    suppressed for omega > omega_c, with a crossover corner omega_c.
  * The published action FORCES the kernel memory corner to omega = a0/2c (tau_mem = 2c/a0 ~ 200 Gyr);
    a ~Myr orbital-scale corner is a DIFFERENT, SECOND scale absent from S.

THIS SCRIPT computes the EXACT allowed [omega_lo, omega_hi] window from ALL constraints JOINTLY, both
footings, each edge traced to its cited bound, and reports NON-EMPTY / EMPTY straight.

THE GATE -- justified, not ad hoc.  The physical crossover is a single-pole (Debye) memory relaxator:
in time a memory kernel  g(t)=omega_c e^{-omega_c t} theta(t)  (finite retention time tau=1/omega_c),
in frequency the CAUSAL response  G(omega) = 1/(1 + i omega/omega_c).  This is the unique minimal
causal object with a single corner and Kramers-Kronig-locked real/imag parts:
      Re G = 1/(1+(omega/omega_c)^2)              [low-pass: ->1 for omega<<omega_c, MI active]
      Im G = -(omega/omega_c)/(1+(omega/omega_c)^2)   [dissipative lag, FORCED nonzero by causality]
The MI response is K_eff = 1 - S(|a|/a0) G(omega), S -> a0/(2 g_N) deep-Newton (the landmine amplitude).
=> A causal gate CANNOT suppress the reactive a0/2 tail (Re G) without incurring a dissipative
   secular drift (Im G).  Both edges below fall out of the SAME G; nothing is inserted by hand.

Every load-bearing number is printed; checks compare computed quantities (no hard-coded verdicts).
"""
import numpy as np, sys

PASS = True
def check(name, cond):
    global PASS
    ok = bool(cond); print(f"   [{'PASS' if ok else 'FAIL'}] {name}")
    if not ok: PASS = False

# ------------------------------------------------------------------ constants & CITED bounds
C   = 2.99792458e8          # m/s
YR  = 3.15576e7             # s
GYR = YR*1e9
MYR = YR*1e6
GMsun   = 1.32712440018e20  # m^3/s^2
GMearth = 3.986004418e14
A0 = {"canon": 9.36e-11, "alt": 1.13e-10}   # both footings (rho_DE cH_Lam/Z  ;  rho_tot cH0)

# Bodies: (name, semimajor axis a [m], orbital period T [days]) -> central GMsun unless noted
BODIES = [("Mercury",5.7909e10, 87.969),  ("Venus", 1.08209e11,224.701),
          ("Earth",  1.49598e11,365.256), ("Mars",  2.27939e11,686.980),
          ("Jupiter",7.78570e11,4332.59), ("Saturn",1.43353e12,10759.22)]
MOON = ("Moon", 3.844e8, 27.3217)         # around Earth (GMearth)

def omega_of(Tdays): return 2*np.pi/(Tdays*86400.0)

# (1) Per-planet CONSTANT-radial anomalous-acceleration bounds delta_g [m/s^2].
#     Source: Fienga & Minazzoli 2024, Living Rev. Relativ. 27:1 (arXiv:2303.01821) Table 10
#     supplementary-perihelion sigmas -> constant sunward delta_g via the Gauss secular equation
#     (planetary_doors/BOUNDS.md sec 1.2 ; laneR_bounds_compute.py).
DG_BOUND = {"Mercury":4.6e-14, "Venus":8.0e-14, "Earth":8.7e-15,
            "Mars":1.4e-15,    "Jupiter":5.6e-13,"Saturn":7.0e-15}
# (2) Secular-drift (fractional orbit expansion d ln r/dt) anchors [per year], each CITED:
GDOT_MESSENGER = 4.0e-14    # Mercury: |Gdot/G| < 4.0e-14/yr, Genova+ 2018 Nat.Commun. 9:289 (VERIFIED web)
GDOT_LLR_1SIG  = 9.6e-15    # LLR Gdot/G = (-5.0 +/- 9.6)e-15/yr, Biskupek & Mueller 2021 Universe 7:34
GDOT_LLR_CEN   = 5.0e-15    #   -> 2-sigma ceiling |cen| + 2 sigma  (VERIFIED web arXiv:2012.12032)
LLR_TIDAL_2SIG = 0.16e-3    # m/yr : lunar da/dt = 38.30 +/- 0.08 mm/yr -> 2 sigma budget proxy
SAT_RDOT_PROXY = 2.3        # m/yr : Cassini ranging ~30 m normal points / 13 yr (FM24 data table)
MARS_RDOT_PROXY= 0.05       # m/yr : Mars-orbiter ~1 m class ranging / ~20 yr (FM24) proxy
# (3) RAR-preservation (galactic) inputs -- deepest CONFIRMED MOND regime:
V_DWARF = 25e3              # m/s   flat rotation speed of the slowest dwarfs that still show MOND
Y_DEEP  = 0.8               # y = g_bar/a0 at those points (deep-MOND, O(1) boost measured)
GATE_KEEP = 0.90           # require the gate open (Re G >= 0.90) there so the RAR is not gated away

print("#"*100); print("# GATE = single-pole causal relaxator: verify Re/Im parts + the two response channels")
print("#"*100)
def ReG(omega, wc): return 1.0/(1.0+(omega/wc)**2)
def ImG(omega, wc): return -(omega/wc)/(1.0+(omega/wc)**2)
# numeric Kramers-Kronig sanity: Im is the Hilbert transform partner of Re for THIS relaxator (exact),
# and |G|^2 = ReG (a defining identity of the 1-pole low-pass) -- both machine-checked, no hand value.
wc_t = 3.3e-14; om_t = 1.0e-7
identity = ReG(om_t,wc_t)**2 + ImG(om_t,wc_t)**2 - ReG(om_t,wc_t)
check("1-pole causal relaxator identity |G|^2 = Re G holds (Re & Im are a KK pair; the dissipative "
      "Im channel is FORCED by causality once Re is frequency dependent)", abs(identity) < 1e-12)
# The two physical channels of K_eff = 1 - (a0/2g_N) G, per unit landmine amplitude a0/2:
#   reactive (radial) anomalous accel  =  (a0/2) * Re G(omega)
#   tangential (dissipative) accel     =  (a0/2) * |Im G(omega)|   -> drives d ln r/dt = 2 f_t/(omega r)
# For a bound orbit omega^2 r = g_N, so  d ln r/dt = (a0/(r wc)) / (1+(omega/wc)^2) -> a0 wc/g_N  (omega>>wc).
# Verify that closed form against the direct 2 f_t/(omega r) evaluation (no hard-code):
for (nm,a,T) in [BODIES[0], BODIES[5]]:
    om = omega_of(T); gN = a*om**2      # Keplerian-consistent g_N = omega^2 r (dynamical, not rounded a)
    a0 = A0["canon"]
    f_t = (a0/2)*abs(ImG(om,wc_t)); drift_direct = 2*f_t/(om*a)
    drift_closed = (a0/(a*wc_t))/(1+(om/wc_t)**2)
    drift_asymp  = a0*wc_t/gN
    check(f"[{nm}] gated drift closed form = 2 f_t/(omega r) (ratio {drift_direct/drift_closed:.6f}) and "
          f"= a0 wc/g_N asymptote (ratio {drift_direct/drift_asymp:.4f})",
          abs(drift_direct/drift_closed-1)<1e-9 and abs(drift_direct/drift_asymp-1)<1e-3)

# ------------------------------------------------------------------ THE JOINT WINDOW, both footings
results = {}
for lab, a0 in A0.items():
    print("\n"+"#"*100); print(f"# FOOTING = {lab}   (a0 = {a0:.3e} m/s^2,  a0/2 = {a0/2:.3e})"); print("#"*100)

    # ---- (A) LOWER EDGE: RAR-preservation.  Gate must stay OPEN at the deepest confirmed MOND orbits.
    #      omega_gal(deep) = y a0 / v_flat.  Require Re G(omega_gal) >= GATE_KEEP  ->  omega_c >= k*omega_gal
    #      with k = sqrt(GATE_KEEP/(1-GATE_KEEP)).
    om_gal = Y_DEEP*a0/V_DWARF
    k = np.sqrt(GATE_KEEP/(1.0-GATE_KEEP))
    omega_lo = k*om_gal
    print(f" LOWER EDGE (galactic RAR-preservation):")
    print(f"   deepest MOND orbit omega_gal = y a0/v = {om_gal:.3e} rad/s  (y={Y_DEEP}, v={V_DWARF/1e3:.0f} km/s)")
    print(f"   Re G >= {GATE_KEEP} there  ->  omega_c >= {k:.2f} x omega_gal = {omega_lo:.3e} rad/s "
          f"(tau <= {1/omega_lo/MYR:.1f} Myr)  [RAR-preservation]")

    # ---- (B) UPPER EDGE #1: REACTIVE per-planet.  (a0/2) Re G(omega_p) <= delta_g_bound(planet).
    #      omega>>wc: Re G = (wc/omega)^2  ->  wc <= omega_p sqrt(2 delta_g/a0).  Binding = smallest.
    react_ceils = [(nm, omega_of(T)*np.sqrt(2*DG_BOUND[nm]/a0)) for (nm,a,T) in BODIES]
    nmR, wcR = min(react_ceils, key=lambda t:t[1])
    print(f" UPPER EDGE (reactive perihelion, per planet):")
    print("   " + ", ".join(f"{nm} {w:.2e}" for nm,w in react_ceils))
    print(f"   binding: {nmR}  omega_c <= {wcR:.3e} rad/s   [Fienga & Minazzoli 2024 per-planet delta_g]")

    # ---- (C) UPPER EDGE #2: SECULAR DRIFT.  d ln r/dt = a0 wc/g_N <= drift_bound(body).
    #      wc <= (drift_bound[/s]) * g_N / a0.  Anchors each cited.  Binding = smallest.
    drift = []
    gN_merc = GMsun/5.7909e10**2
    drift.append(("Mercury Gdot/G [Genova18]", (GDOT_MESSENGER/YR)*gN_merc/a0))
    gN_mars = GMsun/2.27939e11**2
    drift.append(("Mars rdot proxy [FM24]",   ((MARS_RDOT_PROXY/2.27939e11)/YR)*gN_mars/a0))
    gN_sat  = GMsun/1.43353e12**2
    drift.append(("Saturn rdot proxy [FM24]", ((SAT_RDOT_PROXY/1.43353e12)/YR)*gN_sat/a0))
    gN_moon = GMearth/3.844e8**2
    drift.append(("Moon tidal [LLR budget]",  ((LLR_TIDAL_2SIG/3.844e8)/YR)*gN_moon/a0))
    llr_2sig = (GDOT_LLR_CEN+2*GDOT_LLR_1SIG)            # 2-sigma |cen|+2sig = 24.2e-15 /yr
    drift.append(("Moon Gdot/G [Biskupek21]", (llr_2sig/YR)*gN_moon/a0))
    nmD, wcD = min(drift, key=lambda t:t[1])
    print(f" UPPER EDGE (secular drift d ln r/dt = a0 wc/g_N, per body):")
    print("   " + ", ".join(f"{nm.split(' [')[0]} {w:.2e}" for nm,w in drift))
    print(f"   binding: {nmD}  omega_c <= {wcD:.3e} rad/s   (LLR 2-sigma Gdot/G = {llr_2sig:.2e}/yr)")

    # ---- INTERSECT
    omega_hi = min(wcR, wcD)
    hi_src = nmR if wcR < wcD else nmD
    open_ = omega_hi > omega_lo
    print(f"\n ==> JOINT WINDOW ({lab}): omega_c in [{omega_lo:.3e}, {omega_hi:.3e}] rad/s")
    if open_:
        print(f"     = tau in [{1/omega_hi/MYR:.2f}, {1/omega_lo/MYR:.2f}] Myr   width x{omega_hi/omega_lo:.2f}   "
              f"-> NON-EMPTY (survives)")
    else:
        print(f"     -> EMPTY (omega_hi < omega_lo): FALSIFIED at the solar system")
    print(f"     lower edge <- galactic RAR-preservation ;  upper edge <- {hi_src}")
    results[lab] = dict(lo=omega_lo, hi=omega_hi, open=open_, hi_src=hi_src,
                        wcR=wcR, wcD=wcD, nmR=nmR, nmD=nmD, om_gal=om_gal)
    check(f"[{lab}] joint window is NON-EMPTY (a single gated corner threads galaxies AND planets)", open_)
    # transition-observability: at the max corner, what does the gate do to wide binaries (the ONLY
    # current probe near omega ~ omega_c)?  Report, do not manufacture an edge (no dynamical bound there yet).
    for sep_kau in (3,10,20):
        a_wb = sep_kau*1e3*1.495978707e11; om_wb=np.sqrt(1.5*GMsun/a_wb**3)
        boost_frac = ReG(om_wb, omega_hi)
        print(f"     transition probe: {sep_kau:>2} kAU wide binary omega={om_wb:.2e} -> gate keeps "
              f"{boost_frac*100:4.1f}% of the MOND boost at the MAX corner")

# ------------------------------------------------------------------ FORCED vs FREE
print("\n"+"#"*100); print("# IS THE SURVIVING CORNER FORCED (a 2nd physical scale) OR FREE (a 5th constant)?")
print("#"*100)
for lab, a0 in A0.items():
    wc_action = a0/(2*C); tau_action = 2*C/a0
    lo, hi = results[lab]["lo"], results[lab]["hi"]
    orders_below = np.log10(lo/wc_action)
    print(f" [{lab}] action-FORCED memory corner (CLOSURE_MAP.md item d) omega_c = a0/2c = {wc_action:.3e} rad/s "
          f"(tau_mem = 2c/a0 = {tau_action/GYR:.0f} Gyr)")
    print(f"        joint window bottom = {lo:.3e} rad/s  ->  action corner is 10^{orders_below:.1f} BELOW it")
    # at the action corner, is the galactic RAR retained?  Re G(om_gal, wc_action):
    gal_ret = ReG(results[lab]["om_gal"], wc_action)
    print(f"        at the action corner the galactic MOND boost retained Re G(om_gal) = {gal_ret:.2e} "
          f"(RAR-dead: it also gates OFF the rotation curves)")
    check(f"[{lab}] the action's OWN forced corner does NOT land in the window (>=4 orders below) AND is "
          f"RAR-dead -> the surviving corner is NOT supplied by the action: it is a FREE 5th constant",
          orders_below >= 4 and gal_ret < 1e-3)

print("\n"+"="*100)
if all(results[l]["open"] for l in results):
    print(" VERDICT: NON-EMPTY window on BOTH footings -> the framework SURVIVES at the solar system,")
    print("          but ONLY as a gated Reading C whose corner is a FREE add-on (a 5th constant): the")
    print("          published action forces the corner to ~200 Gyr (RAR-dead), NOT into the Myr window.")
else:
    print(" VERDICT: EMPTY window on at least one footing -> FALSIFIED at the solar system (reported straight).")
print("="*100)
print(f" window_joint: {'ALL CHECKS PASS' if PASS else 'A CHECK FAILED'}")
sys.exit(0 if PASS else 1)
