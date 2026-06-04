#!/usr/bin/env python3
"""
DOOR 7 worked: derive a0 from the entanglement-equilibrium volume-law term. Where it forces, where it doesn't.
=============================================================================================================
The overlooked LIVE door (UNIFICATION_DOORS_LEDGER.md). After DSSYK forcing of Z was COMPUTED TO FAIL, this is
the cleanest remaining route to DERIVE a0: the entanglement-equilibrium formalism (Jacobson 2016 +
Bueno-Min-Speranza-Visser 2017) absorbs a modified entropy functional AS an equilibrium condition -- avoiding the
non-equilibrium obstacle that kills the Clausius route (Door 4). Worked honestly here.

THE MECHANISM (volume-law vs area-law, the de Sitter dark-energy entropy):
  area-law entropy  S_A(r) = A/4G = pi r^2 / G       (UV / Ryu-Takayanagi; -> Einstein)
  volume-law term   S_V(r) = s * (4pi/3) r^3, with s = S_dS/V_dS = 3/(4 G L)  (de Sitter entropy filling the volume)
  => S_V/S_A = r/L : the VOLUME law overtakes the AREA law exactly at r = L = c/H (the de Sitter radius).
THE SCALE IS FORCED: the crossover is at the Hubble/de Sitter scale, so the emergent acceleration is a0 ~ c^2/L = cH.
This is robust and geometric -- it is WHY a0 ~ cH, and it is the cleanest derivation of the SCALE.

THE COEFFICIENT (Verlinde 2016's elastic/displacement calculation of the same volume-law):
  apparent dark mass M_D^2(r) = (a0 r^2)/(6G) d(r M_b)/dr  =>  g_D = sqrt(a0 g_b / 6),  a0 = cH.
  i.e. the effective MOND scale is a_M = cH/6  ->  cH/a_M = 6  (the 1/6 = the d=4 strain/volume integral).

COMPARE: cH/a0:  Verlinde volume-law = 6.00 ;  framework Z = 2sqrt(8pi/3) = 5.789 ;  Unruh-thermal = 2pi = 6.283.
=> the cleanest thermodynamic route (entanglement volume-law) lands on the GEOMETRIC O(1)~6 -- within 4% of the
framework's Z, NOT on a wildly different number. It CONFIRMS the scale and the geometric character; it does NOT
force the exact 32pi (the coefficient is the volume-integral value 6, route/detail-dependent).

HONEST: (i) the SCALE a0~cH is FORCED by the volume/area crossover at the de Sitter radius -- a genuine derivation.
(ii) The COEFFICIENT comes out ~6 (Verlinde), in the framework's cluster, but not exactly 32pi -- so even the
cleanest route reproduces, not forces, Z. (iii) Door 7 caveat: extracting a0 requires relaxing Jacobson's
FIXED-volume constraint (the volume term is the constraint, not a contribution) -- a real modification, exactly
Verlinde's dynamical-volume move. So Door 7 is LIVE for the scale+cluster, still route-bound for the exact coeff.
Needs numpy.
"""
import numpy as np

c = 2.998e8; G = 6.674e-11; Mpc = 3.086e22
H0 = 67.4e3/Mpc; L = c/H0
Z = 2*np.sqrt(8*np.pi/3)


def main():
    print("#"*94); print("# Door 7 worked: entanglement-equilibrium volume-law -> a0"); print("#"*94 + "\n")

    print("="*94); print("(1) THE SCALE IS FORCED: volume law overtakes area law at r = L (de Sitter radius)"); print("="*94)
    for r_over_L in (0.01, 0.1, 1.0, 10.0):
        print(f"   r/L = {r_over_L:>5}:  S_volume/S_area = r/L = {r_over_L:>5}  {'<- crossover (dark energy / a0 kicks in)' if r_over_L==1 else ''}")
    print(f"   => crossover at r = L = c/H0 = {L:.3e} m. Emergent scale a0 ~ c^2/L = cH0 = {c**2/L:.3e} m/s^2.")
    print(f"      The de Sitter radius FORCES a0 ~ cH -- the cleanest derivation of the SCALE. [genuine]\n")

    print("="*94); print("(2) THE COEFFICIENT: Verlinde's volume-law elastic calc gives cH/a0 = 6"); print("="*94)
    print(f"   M_D^2 = (a0 r^2/6G) d(r M_b)/dr -> g_D = sqrt(a0 g_b/6), a0=cH => effective a_M = cH/6.")
    print(f"   {'route':<42}{'cH/a0':>8}")
    print(f"   {'entanglement volume-law (Verlinde 2016)':<42}{6.00:>8.3f}")
    print(f"   {'framework Z = 2 sqrt(8pi/3)':<42}{Z:>8.3f}")
    print(f"   {'Unruh / thermal (2pi)':<42}{2*np.pi:>8.3f}")
    print(f"   {'observed cH0/a0 (a0=1.2e-10)':<42}{c*H0/1.2e-10:>8.3f}")
    print(f"   => the cleanest thermodynamic route gives 6.00 -- {100*abs(6-Z)/Z:.0f}% from the framework's {Z:.2f}, in the")
    print(f"      same geometric O(1)~6 cluster. It CONFIRMS the cluster; it does NOT single out 32pi.\n")

    print("="*94); print("(3) THE DOOR-7 NUANCE (why it's 'live' not 'closed')"); print("="*94)
    print("""   * Pure Jacobson 2016 holds VOLUME FIXED -> the volume term drops out (it's the constraint), so it gives
     NO a0 by itself. Extracting a0 needs the volume entropy made DYNAMICAL (Verlinde's displacement move) --
     a genuine modification of the maximal-entanglement hypothesis, not a free read-off.
   * Bueno-Min-Speranza-Visser 2017: modifying the entropy FUNCTIONAL returns modified field equations AS an
     equilibrium condition (NO non-equilibrium production term) -- this is why the entanglement route is CLEANER
     than the Clausius route (Door 4), which needed a dissipative term. So the volume-law term is admissible here.
   * Net: Door 7 is LIVE -- it forces the SCALE (a0~cH, from the de Sitter crossover) and lands the coefficient
     in the framework's cluster (~6), via a cleaner formalism than Clausius -- but it does NOT force the exact Z.\n""")

    print("="*94); print("VERDICT"); print("="*94)
    print(f"""  Worked honestly, Door 7 DERIVES THE SCALE a0 ~ cH (the volume/area entropy crossover sits exactly at the de
  Sitter radius -- a genuine, geometric result) and gives the COEFFICIENT ~6 (Verlinde's volume-law elastic
  factor), within 4% of the framework's Z=5.789 and squarely in the geometric O(1)~6 cluster. It is the cleanest
  thermodynamic home (no non-equilibrium obstacle, unlike Clausius). But it does NOT force the exact 32pi -- the
  coefficient is the volume-integral value, route/detail-dependent -- and it requires relaxing Jacobson's fixed-
  volume constraint. So: the SCALE is now derived three independent ways (Friedmann, de Sitter crossover, DSSYK
  freezing-mechanism); the exact COEFFICIENT Z=2sqrt(8pi/3) remains reproduced-in-the-cluster, not uniquely forced.""")
    print("#"*94)


if __name__ == "__main__":
    main()
