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
lat_ignatiev = 79 + 50/60.0         # his PRD 77 102001: phi ~= +/- 79 deg 50' = 79.83 deg
print(f"  cancellation latitude: cos(lat) = a_orb/a_spin(eq) -> lat = {lat_star:.2f} deg")
print(f"     -> REPRODUCES Ignatiev's PRD value phi = 79 deg 50' = {lat_ignatiev:.2f} deg")
print(f"        (agreement {abs(lat_star-lat_ignatiev):.2f} deg; residual = his as=a1+a2 budget + constants).")
dadt = omega * a_orb                # sweep rate of the residual through zero
for name,a0 in [("canonical",A0_C),("alt",A0_A)]:
    dt = 2*a0/dadt
    print(f"  window sweep-rate da/dt = {dadt:.2e} m/s^3 -> |a|<a0 window = {dt*1e3:.2f} ms  [{name} a0={a0:.3e}]")
DT_WIN = 2*A0_C/dadt

print(f"\n  FRAME ROBUSTNESS (corrected 2026-07-20 against Ignatiev 2008 full text):")
print(f"  Ignatiev works in the GALACTIC frame S0 and his budget EXPLICITLY includes")
print(f"  a2 = the Sun's galactocentric acceleration (his Eq. 3.2, as = a1 + a2).")
print(f"  The cancellation is VECTORIAL with the event time t_p a free knob: the")
print(f"  spin+orbital resultant sweeps and cancels the galactocentric vector too")
print(f"  ({a_gal/A0_C:.2f} a0_canon / {a_gal/A0_A:.2f} a0_alt -- absorbed into a timing/location shift,")
print(f"  off-equinox < a few days by his continuity theorem: >= 2 exact zeros/yr).")
print(f"  A prior scalar-magnitude-sum reading ('galactocentric term floors the")
print(f"  budget above a0 -> no window') is WRONG and is retracted. Local-Group")
print(f"  frame shift negligible (Andromeda < 1e-12 m/s^2, his footnote 2).")
print(f"  The real fork he states: Galactic-frame a0 vs INVARIANT (lab-frame) a0;")
print(f"  he shows the invariant version internally inconsistent (acceleration")
print(f"  addition forces mu==1, his Eqs. 2.1-2.3) and experimentally ruled out.")

print()
print("="*78)
print("2. THE KINEMATIC-MI BLIP (what a short-memory kinematic MI predicts)")
print("="*78)
# naive rigid-body estimate: during the window the residual force ~ m*a0 acts on
# deep-MOND-reduced inertia; displacement ~ (1/2) a0 dt^2 as the floor estimate
for name,a0 in [("canonical",A0_C),("alt",A0_A)]:
    dt = 2*a0/dadt
    print(f"  naive rigid-body floor [{name}]: dx ~ (1/2) a0 dt^2 = {0.5*a0*dt**2:.1e} m")
dx_naive = 0.5*A0_C*DT_WIN**2
print(f"  Ignatiev's full interferometer treatment (PRL 98 101101): dx ~ 1e-14 m")
# THE SUSPENSION BRIDGE (closes the ~3-order gap QUANTITATIVELY, from his Secs. V-VI):
# the deep-window VELOCITY IMPULSE dv ~ a0*dt is displayed by the suspension as
# dx ~ a0*dt/omega0 with omega0 = 4.1 1/s (LIGO, f0=0.65 Hz, his stated value).
# The naive (1/2)a0 dt^2 is the IN-window displacement -- not what an interferometer records.
omega0 = 4.1                        # LIGO suspension angular frequency, his value
for name,a0 in [("canonical",A0_C),("alt",A0_A)]:
    dt = 2*a0/dadt
    print(f"  suspension bridge [{name}]: dx ~ a0*dt/omega0 = {a0:.3e}*{dt:.2e}/{omega0} = {a0*dt/omega0:.1e} m")
print(f"  -> the bridge REPRODUCES his ~1e-14 m amplitude from our own window numbers")
print(f"     (and explains his a0^2 scaling, since dt is itself prop. to a0).")
# per-footing blip TARGETS scaled from his Fig. 1 (0.95e-14 m at a0=1e-10, ~a0^2 scaling;
# also 1.4e-14 at 1.2e-10, 3.8e-14 at 2e-10, max ~0.76 s after t_p):
for name,a0 in [("canonical",A0_C),("alt",A0_A)]:
    print(f"  Fig.-1-scaled blip target [{name}]: 0.95e-14*(a0/1e-10)^2 = {0.95e-14*(a0/1e-10)**2:.2e} m")
print(f"  (his 1e-14 uses HIS mu(z)=z/sqrt(1+z^2) + LIGO omega0; target mu- and")
print(f"   suspension-dependent at O(1).)")
print(f"  Either is in reach of LIGO-class metrology (~1e-19 m/rtHz); the required site")
print(f"  (~80 deg: Svalbard 78N / Antarctic Dome A 80.4S) has never hosted one (2007->).")

print()
print("="*78)
print("3. FRAMEWORK NULL, ROUTE A -- the proper-acceleration variable does not blink")
print("="*78)
# effective gravity at the cancellation latitude (International Gravity Formula):
lat_r = np.radians(lat_star)
g_lat = 9.780327*(1 + 0.0053024*np.sin(lat_r)**2 - 0.0000058*np.sin(2*lat_r)**2)
print(f"  proper acceleration at lat {lat_star:.1f} deg: g = {g_lat:.2f} m/s^2 (polar gravity,")
print(f"  reduced centrifugal; the 9.81 standard value shifts the offset only in its 3rd digit)")
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
for name,a0 in [("canonical",A0_C),("alt",A0_A)]:
    dt = 2*a0/dadt; d = dt/tau
    print(f"  window/memory duty factor [{name}] = {dt:.1e}/{tau:.1e} = {d:.1e} -> dx ~ 1e-14 x {d:.0e} = {1e-14*d:.0e} m")
print(f"  EVEN IF one (wrongly) fed the kinematic variable into the framework kernel,")
print(f"  the ms window is averaged over ~203 Gyr of memory: blip suppressed to ~1e-36 m")
print(f"  on either footing ({np.log10(1e-19/(1e-14*duty)):.0f} orders below a LIGO-class 1e-19 m/rtHz floor).")
print(f"  NOTE this linear duty x 1e-14 figure is a CONSERVATIVE UPPER BOUND: the kernel")
print(f"  smooths the INPUT, so the kernel-averaged kinematic acceleration moves")
print(f"  fractionally by only ~dt/tau ~ {duty:.0e} and never leaves the Newtonian")
print(f"  regime even instantaneously -- the hybrid never enters deep MOND at all.")
print(f"  Dead twice over, independently.")

print()
print("="*78)
print("5. CONSISTENCY -- existing lab nulls do NOT discriminate (both readings pass)")
print("="*78)
a_lat = 5e-14
print(f"  Gundlach et al. 2007 (PRL 98 150801): F=ma holds at lateral {a_lat:.0e} m/s^2.")
print(f"  Framework: proper accel {g_E} m/s^2 -> predicts Newton to ~5e-12 -> PASSES.")
print(f"  Kinematic MI: spin accel at Seattle latitude ~ {a_spin_eq*np.cos(np.radians(47.6)):.2e} m/s^2 >> a0")
print(f"  outside windows -> also PASSES. Only the SHLEM window separates them.")
print(f"  (Per Ignatiev's own consistency argument: Gundlach-class lab tests rule out")
print(f"   the INVARIANT/lab-frame-a0 kinematic version; SHLEM tests the GALACTIC-frame")
print(f"   version; neither touches proper-acceleration MI outside the window.)")

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
