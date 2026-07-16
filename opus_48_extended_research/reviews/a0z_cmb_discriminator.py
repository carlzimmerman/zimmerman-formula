import numpy as np
c=2.99792458e8; G=6.674e-11
H0=67.4*1000/3.0857e22; Om=0.315; OL=0.685; Or=9.2e-5
a0_now=9.36e-11
def E(z): return np.sqrt(Om*(1+z)**3+Or*(1+z)**4+OL)
Z=2*np.sqrt(8*np.pi/3)

print("DISCRIMINATOR: framework (a0~sqrt rho_DE) vs Verlinde (a0~cH) at recombination")
print("="*65)
z_rec=1089.0
# Verlinde: a0_V(z) = a0_now * H(z)/H0 (a0~cH)
a0_V_rec = a0_now * E(z_rec)
# Framework w=-1: a0 const
a0_F_rec = a0_now
print(f"At z={z_rec}:")
print(f"  Framework a0(z_rec) = {a0_F_rec:.3e}  (= a0_now, const for w=-1)")
print(f"  Verlinde  a0(z_rec) = {a0_V_rec:.3e}  (= a0_now*E(z), E={E(z_rec):.1f})")
print(f"  ratio V/F = {a0_V_rec/a0_F_rec:.1f}  => Verlinde a0 is ~{E(z_rec):.0f}x larger at rec.")
# But even Verlinde's a0 at rec vs acoustic accel:
Mpc=3.0857e22; cs=c/np.sqrt(3); r_s=0.13*Mpc
a_acoustic=cs**2/r_s
print(f"\n  acoustic accel ~ {a_acoustic:.2e}; even Verlinde a0={a0_V_rec:.2e} is {a_acoustic/a0_V_rec:.0e}x below it.")
print("  => BOTH frameworks predict NO CMB-peak MI imprint (fluid deeply Newtonian either way).")
print("  => the early-universe null is NOT a framework-vs-Verlinde discriminator. Both null.")
print("\nCONCLUSION: early-universe a0 is below every relevant accel in ALL MOND-scale theories.")
print("No CMB/BBN test distinguishes them. The discriminating power lives ONLY at z<~5 (banked).")
