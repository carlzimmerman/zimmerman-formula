#!/usr/bin/env python3
"""
DOOR E -- the rho_DE^(1/4) CORNER, examined BOTH WAYS (anti-reflexive-dismissal).

In door_E_amount_pin.py, ONE corner of the scan was not a tens-of-orders miss:
setting M = rho_DE^(1/4) ~ 2.24 meV, the displacement-from-the-same-scale
hypotheses gave Omega_dust/Om_L ~ 2.0 (i.e. Omega_dust ~ 1.37), and the inversion
showed the REQUIRED displacement is dQ/M^2 = 0.194 -- an O(1) number, NOT a
tens-of-orders miss. The #1 rule (verify a 'works' AND a 'fails' claim equally;
penalize reflexive dismissal) demands I probe whether this corner is a genuine
near-pin or a tuned coincidence. If rho_dust ~ rho_DE (both ~ meV^4) is FORCED by
the framework, then Omega_dust ~ Omega_DE up to an O(1) -- and 0.2657 = 0.685 *
0.388, so the O(1) needed is 0.388. Is 0.388 a framework number, or a free dial?
"""
import numpy as np

c=2.99792458e8; G=6.67430e-11; hbar=1.054571817e-34; kB=1.380649e-23
Mpc=3.0856775814913673e22; eV=1.602176634e-19
H0=67.4e3/Mpc; Om_L=0.685; Om_dm=0.315-0.0493
H_L=H0*np.sqrt(Om_L); rho_crit=3*H0**2/(8*np.pi*G)
rho_DE=Om_L*rho_crit; rho_dm=Om_dm*rho_crit
Z=np.sqrt(32*np.pi/3); target=Om_dm/Om_L
a0=c**2*np.sqrt(3*Om_L*H0**2/c**2/(32*np.pi))

def E14(rho): return ((rho*c**2)*(hbar*c)**3)**0.25/eV
rhoDE14=E14(rho_DE); rhodm14=E14(rho_dm)
print("="*82)
print("rho_DE^(1/4) CORNER -- both ways")
print("="*82)
print(f"  rho_DE^(1/4) = {rhoDE14*1e3:.4f} meV   rho_dm^(1/4) = {rhodm14*1e3:.4f} meV")
print(f"  rho_dm/rho_DE = Om_dm/Om_L = {target:.4f}   (so rho_dm = 0.388 * rho_DE)")
print(f"  (rho_dm/rho_DE)^(1/4) = {target**0.25:.4f}  -> the meV scales differ by only {(1-target**0.25)*100:.0f}%")
print()
print("  THE BOTH-WAYS POINT: rho_dm and rho_DE are the SAME order (both meV^4); their")
print("  RATIO is 0.388 (the cosmic coincidence). If the GC forced rho_dust = rho_DE")
print("  EXACTLY, Omega_dust would be Om_L (0.685), NOT Om_dm (0.266) -- a factor 0.388 OFF.")
print()
# Is 0.388 a framework number? scan the framework's O(1) constants
print("  Is the needed O(1) = 0.388 a framework number, or a free dial?")
cands = {
    "1/Z":1/Z, "(3/8pi)^1/4":(3/(8*np.pi))**0.25, "3/8pi":3/(8*np.pi),
    "sqrt(3/8pi)":np.sqrt(3/(8*np.pi)), "1/Z^2":1/Z**2, "1-Om_L":1-Om_L,
    "Om_dm/Om_L (=target itself)":target,
}
for k,v in cands.items():
    print(f"    {k:<30}{v:.4f}   {'== 0.388 (within 5%)' if abs(v-target)/target<0.05 else 'no'}")
print()
print("  ONLY the target restated (Om_dm/Om_L) equals 0.388. No INDEPENDENT framework")
print("  constant (1/Z, 3/8pi powers, ...) gives 0.388. So even granting the meV-scale")
print("  COINCIDENCE rho_dust ~ rho_DE, the framework supplies NO number that turns")
print("  'same order' into the precise 0.388 -- that residual O(1) is the free I0/amount.")
print()
print("  AND: 'rho_dust = rho_DE^(1/4)-scaled' is NOT forced. rho_dust = 2 Q0 I0/a^3 with")
print("  I0 a free integration constant (Part 1 of the main door). Choosing M = rho_DE^1/4")
print("  fixes the VEV scale Q0=M^2, but the displacement dQ_0 (hence I0) is still free;")
print("  the corner only 'works' because I0 was IMPLICITLY tuned to make dQ/M^2 ~ 0.19.")
print("  That is the tuning, relocated -- not a pin.")
print()
print("VERDICT (corner): the rho_DE^(1/4) near-coincidence is the well-known cosmic")
print("coincidence rho_dm ~ rho_DE (same meV^4 order), NOT a pin. The framework forces")
print("neither rho_dust=rho_DE nor the residual 0.388; both reduce to the free I0. The")
print("'2.0 ratio' in the main scan is exactly the missing 1/0.388~2.6 factor = the free")
print("amount. Reflexive-dismissal check PASSED: probed hard, still a free constant.")
print(f"  [machine] needed_O1={target:.4f}  framework_supplies_it=False")
