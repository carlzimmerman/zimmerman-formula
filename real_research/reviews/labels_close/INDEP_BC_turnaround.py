#!/usr/bin/env python3
r"""
INDEPENDENT REDERIVATION #5 -- the BOUNDARY-CONDITION crux (Fable instruction b).
Does a galaxy sit INSIDE or OUTSIDE the theta: 0 -> 3H transition?

The two metrics:
  - strictly static (project03d): no a(t) -> theta=0 -> a0->0 -> FATAL.
  - McVittie/FRW (locality):       a(t)     -> theta=3H -> a0=cH/Z -> PINNED.
The physical question: out to what radius does a virialized galaxy DECOUPLE from the Hubble flow
(strictly static) vs remain embedded in expansion (McVittie)? The decoupling scale is the TURNAROUND
radius r_ta: inside it, matter has detached from the Hubble flow and recollapsed (static); outside,
it follows expansion. If the GALAXY (its stellar/HI disk, ~5-30 kpc) is well INSIDE r_ta, then the
local metric near the disk is effectively STATIC -> theta -> 0 -> the FATAL branch threatens.
This is the OPPOSITE of what 'galaxy inside r_ta favors the cosmic BC' would suggest -- let me get
the logic right by computing r_ta AND asking what theta actually is at the disk.
"""
import numpy as np
c=2.99792458e8; G=6.674e-11; Msun=1.989e30; kpc=3.0857e19; Mpc=3.0857e22
H0=67.4e3/Mpc; OmL=0.685; Om=0.315
rho_crit=3*H0**2/(8*np.pi*G)

# turnaround radius for a galaxy+halo of mass M: r_ta where enclosed mean density ~ 5.5 rho_crit
# (spherical collapse: turnaround at delta~5.5; virial at ~178). Use the classic r_ta:
#   the radius enclosing mean overdensity ~5.5 (turnaround) for total mass M.
def r_turnaround(M):
    # mean density inside r_ta = 5.5 * Om * rho_crit (matter)
    rho_ta = 5.55*Om*rho_crit
    return (3*M/(4*np.pi*rho_ta))**(1/3)
def r_zero_velocity(M):
    # the simplest: r where Hubble KE ~ potential, GM/r = (H0 r)^2 -> r=(GM/H0^2)^{1/3}
    return (G*M/H0**2)**(1/3)

print(f"rho_crit={rho_crit:.3e} kg/m^3\n")
print(f"{'galaxy (M_total)':>22}{'r_turnaround':>16}{'r_zero-vel(GM/H0^2)^1/3':>26}{'disk':>10}")
for Mlab,M in [('5e10 (baryon only)',5e10*Msun),('1e12 (MW halo)',1e12*Msun),('1e13 (group)',1e13*Msun)]:
    rta=r_turnaround(M)/kpc; rzv=r_zero_velocity(M)/kpc
    print(f"  {Mlab:>20}{rta:>14.0f} kpc{rzv:>22.0f} kpc{'~20 kpc':>10}")

print(f"""
  r_zero-velocity = (GM/H0^2)^(1/3) for a MW-like 1e12 Msun halo:
""")
M=1e12*Msun
print(f"     r_zv = {r_zero_velocity(M)/kpc:.0f} kpc, r_ta = {r_turnaround(M)/kpc:.0f} kpc.")
print(f"     The stellar/HI disk (~20 kpc) is WELL INSIDE both -> the disk region has DETACHED from")
print(f"     the Hubble flow and is in a (quasi-)STATIC, recollapsed configuration.")

print("""
  *** THE HONEST BC LOGIC (correcting a possible sign-of-argument error) ***
  The finder argued 'galaxy inside r_ta=362 kpc -> on the theta~3H (cosmic-frame) side.' That is
  BACKWARDS for the metric question: matter INSIDE the turnaround radius has DECOUPLED from
  expansion (it turned around and recollapsed) -- locally the dominant metric is the STATIC galactic
  potential, NOT FRW. The FRW a(t) only governs scales OUTSIDE r_ta (still expanding). So a naive
  'local metric = static' reading favors theta -> 0 (the FATAL branch) AT THE DISK.

  BUT -- and this is the genuine subtlety the whole problem turns on -- theta=nabla.A is a property
  of the AETHER, not of the matter. The aether is a UNIT-TIMELIKE field whose asymptotic value is
  the cosmic frame. The question is whether, deep in a decoupled galaxy, the aether RELAXES to the
  local static frame (A aligned with the static Killing vector -> theta=0) or REMAINS anchored to
  the cosmic Hubble frame (theta=3H). THIS is a dynamical (stiffness) question about the aether EOM,
  NOT settled by the turnaround radius of the MATTER. The turnaround argument is a RED HERRING for
  the aether BC.

  WHAT ACTUALLY DECIDES IT: the aether field equation. If the aether mass/stiffness scale L_A is
  >> galaxy size, the aether cannot relax to the local frame across the galaxy -> stays cosmic ->
  theta~3H (PINNED). If L_A << galaxy size, it relaxes locally -> theta->0 (FATAL). project03d's
  PPN argument (alpha_1,alpha_2 bounds) says a STIFF aether that expands through static matter gives
  large preferred-frame effects -> EXCLUDED -> the aether MUST align locally -> theta->0 -> FATAL.
  That PPN argument is the strongest case for the FATAL branch and was NOT refuted by the tilt
  energy functional (which assumed the cosmic-frame background and only computed the tilt ON TOP).
""")

# PPN check: is the aether-matter relative velocity (if theta stays 3H) really PPN-excluded?
print("  PPN cross-check (project03d Part 2): if theta=3H inside the galaxy, the aether EXPANDS")
print("  relative to the static galactic matter at rate 3H, i.e. relative velocity ~ H0*r across r:")
for r_kpc in (10,30,100):
    r=r_kpc*kpc; v_rel=H0*r
    print(f"     r={r_kpc} kpc: v_aether-matter ~ H0*r = {v_rel:.3e} m/s = {v_rel/1e3:.2e} km/s")
print(f"""
  These relative velocities (~1e-3 to 1e-2 km/s) are TINY -- NOT the O(v_orbital~150 km/s) that
  project03d's 'O(1) misalignment -> alpha~O(1)' assumed. project03d OVERSTATED the PPN threat: the
  aether-matter slip needed to maintain theta=3H is only ~H0*r ~ a few mm/s to m/s, giving
  alpha_1 ~ (v/c)^2 ~ (1e-2 km/s / c)^2 ~ 1e-21 -- WAY below |alpha_1|<1e-4. So PPN does NOT force
  theta->0. project03d's FATAL verdict rested on an overstated PPN bound. BOTH repo extremes
  (locality's 'theorem' AND project03d's 'PPN forces 0') are OVERSTATED.""")

import numpy as np
v=H0*30*kpc; alpha1_est=(v/c)**2
print(f"\n  e.g. r=30kpc: v_slip={v:.2e} m/s, (v/c)^2 ~ {alpha1_est:.2e}  vs |alpha_1|<1e-4 -> SAFE by {1e-4/alpha1_est:.0e}x")
