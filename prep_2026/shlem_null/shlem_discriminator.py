#!/usr/bin/env python3
"""
THE SHLEM NULL DISCRIMINATOR -- which acceleration variable does inertia listen to?

Ignatiev (PRL 98, 101101, 2007; PRD 77, 102001, 2008): for KINEMATIC modified-inertia
MOND (the MOND variable = the body's coordinate acceleration in the preferred frame),
twice a year at latitude ~80 deg the Earth's spin-centripetal and orbital accelerations
cancel for ~ms, dropping a bench-mounted body's kinematic acceleration below a0 -> a
spontaneous-displacement blip (his full treatment: ~1e-14 m interferometer signal).

THIS framework (de Sitter-Unruh MODIFIED INERTIA): inertia responds to the dS-Unruh
bath at the body's PROPER acceleration, T(a) = (hbar/2 pi k c) sqrt(a^2 + (c H_L)^2).
A bench-mounted mass is SUPPORTED: proper acceleration = g = 9.81 m/s^2 at ALL times,
completely unchanged by the kinematic cancellation -> the framework predicts an EXACT
NULL in the SHLEM transient channel, independently frozen by its committed ~203-Gyr
memory kernel. SHLEM therefore discriminates WITHIN the modified-inertia class.

Every number below is computed from scratch. Both a0 footings carried.
"""
import numpy as np

# constants
c    = 2.99792458e8
G    = 6.67430e-11
Lam  = 1.089e-52                    # Planck 2018 cosmological constant, 1/m^2
Z    = np.sqrt(32*np.pi/3)          # 5.78881 (posited)
A0_C = c**2*np.sqrt(Lam/(32*np.pi)) # canonical footing
H0   = 67.66e3/3.0856776e22        # SI
A0_A = c*H0/Z                       # alt footing
g_E  = 9.81

print("="*78)
print("1. THE IGNATIEV WINDOW -- reproduced from first principles (kinematic budget)")
print("="*78)
R_E   = 6.371e6
omega = 2*np.pi/86164.0             # sidereal spin rate
a_spin_eq = omega**2 * R_E          # spin centripetal at equator
AU=1.495978707e11; yr=3.1557e7
a_orb = (2*np.pi/yr)**2 * AU        # Earth orbital centripetal
V_gal, R_gal = 233e3, 8.2*3.0856776e19
a_gal = V_gal**2/R_gal              # galactocentric centripetal
print(f"  spin centripetal (equator) = {a_spin_eq:.3e} m/s^2")
print(f"  Earth orbital              = {a_orb:.3e} m/s^2")
print(f"  galactocentric             = {a_gal:.3e} m/s^2  (= {a_gal/A0_C:.2f} a0_canon, {a_gal/A0_A:.2f} a0_alt)")
lat_star = np.degrees(np.arccos(a_orb/a_spin_eq))
print(f"  cancellation latitude: cos(lat) = a_orb/a_spin(eq) -> lat = {lat_star:.1f} deg")
print(f"     -> REPRODUCES Ignatiev's '~80 deg N/S' spots (his PRL: 80 deg).")
dadt = omega * a_orb                # sweep rate of the residual through zero
for name,a0 in [("canonical",A0_C),("alt",A0_A)]:
    dt = 2*a0/dadt
    print(f"  window sweep-rate da/dt = {dadt:.2e} m/s^3 -> |a|<a0 window = {dt*1e3:.2f} ms  [{name} a0={a0:.3e}]")
DT_WIN = 2*A0_C/dadt

print(f"\n  FRAME CAVEAT (fork, stated honestly): the windows exist only on the")
print(f"  free-fall-relative kinematic reading (Ignatiev's; the galactic free-fall")
print(f"  drops out). On an absolute-CMB-frame reading the galactocentric term")
print(f"  ({a_gal/A0_C:.1f} a0_canon / {a_gal/A0_A:.1f} a0_alt) floors the budget ABOVE a0 -> no window at all.")

print()
print("="*78)
print("2. THE KINEMATIC-MI BLIP (what a short-memory kinematic MI predicts)")
print("="*78)
# naive rigid-body estimate: during the window the residual force ~ m*a0 acts on
# deep-MOND-reduced inertia; displacement ~ (1/2) a0 dt^2 as the floor estimate
dx_naive = 0.5*A0_C*DT_WIN**2
print(f"  naive rigid-body floor: dx ~ (1/2) a0 dt^2 = {dx_naive:.1e} m")
print(f"  Ignatiev's full interferometer treatment (PRL 98 101101): dx ~ 1e-14 m")
print(f"  (the ~3-order gap = his suspended-mirror/response treatment vs the rigid floor;")
print(f"   we quote HIS number as the kinematic-MI target and the naive floor as the min).")
print(f"  Either is in reach of LIGO-class metrology (~1e-19 m/rtHz); the required site")
print(f"  (~80 deg: Svalbard 78N / Antarctic Dome A 80.4S) has never hosted one (2007->).")

print()
print("="*78)
print("3. FRAMEWORK NULL, ROUTE A -- the proper-acceleration variable does not blink")
print("="*78)
for name,a0 in [("canonical",A0_C),("alt",A0_A)]:
    y = g_E/a0
    delta = 1/(2*y)   # nu(y)=sqrt(1+1/y) -> fractional deviation a0/(2g), static
    print(f"  [{name}] y = g/a0 = {y:.3e} -> static inertia deviation = {delta:.2e} (calibration-absorbed)")
print(f"  During the window the support force is UNCHANGED: proper accel = g at all times.")
print(f"  The SHLEM observable is the time-tagged TRANSIENT; every framework variable")
print(f"  (proper accel, bath temperature) is constant through the window ->")
print(f"  TRANSIENT PREDICTION = 0 EXACTLY (not merely suppressed).")

print()
print("="*78)
print("4. FRAMEWORK NULL, ROUTE B -- the committed memory kernel freezes ms windows")
print("="*78)
H_L = c*np.sqrt(Lam/3)
tau = 2*Z/H_L
print(f"  H_Lambda = {H_L:.3e} 1/s  ->  tau_mem = 2Z/H_Lambda = {tau:.2e} s = {tau/3.156e16:.0f} Gyr")
duty = DT_WIN/tau
print(f"  window/memory duty factor = {DT_WIN:.1e}/{tau:.1e} = {duty:.1e}")
print(f"  EVEN IF one (wrongly) fed the kinematic variable into the framework kernel,")
print(f"  the ms window is averaged over ~203 Gyr of memory: blip suppressed by ~{duty:.0e}")
print(f"  -> dx ~ 1e-14 x {duty:.0e} = {1e-14*duty:.0e} m. Dead twice over, independently.")

print()
print("="*78)
print("5. CONSISTENCY -- existing lab nulls do NOT discriminate (both readings pass)")
print("="*78)
a_lat = 5e-14
print(f"  Gundlach et al. 2007 (PRL 98 150801): F=ma holds at lateral {a_lat:.0e} m/s^2.")
print(f"  Framework: proper accel {g_E} m/s^2 -> predicts Newton to ~5e-12 -> PASSES.")
print(f"  Kinematic MI: spin accel at Seattle latitude ~ {a_spin_eq*np.cos(np.radians(47.6)):.2e} m/s^2 >> a0")
print(f"  outside windows -> also PASSES. Only the SHLEM window separates them.")

print()
print("="*78)
print("VERDICT (pre-registered, both ways)")
print("="*78)
print("  SHLEM blip SEEN at Ignatiev magnitude+timing  -> the framework's proper-")
print("    acceleration coupling AND its 203-Gyr kernel are BOTH falsified (dual kill).")
print("  SHLEM NULL -> short-memory kinematic MI killed; framework CONSISTENT but NOT")
print("    confirmed (null shared with modified gravity, whose EFE also predicts null,")
print("    and with plain Newton). A kill-condition-only observable for the framework.")
print("  a0's value and Z remain postulates; the discriminator tests the VARIABLE, not the value.")
print("EXIT 0")
