import numpy as np
c=2.99792458e8; G=6.674e-11
H0=67.4*1000/3.0857e22; Om=0.315; OL=0.685; Or=9.2e-5
a0_now=9.36e-11
Mpc=3.0857e22

def E(z): return np.sqrt(Om*(1+z)**3+Or*(1+z)**4+OL)
def H(z): return H0*E(z)

print("="*70)
print("PART D: Is there ANY early-universe MI imprint? (CMB/BBN)")
print("="*70)
# Modified inertia matters when an object's acceleration a <~ a0.
# At recombination z~1089: what are the relevant accelerations?
# 1) cosmic expansion 'acceleration' proxy cH(z)
# 2) gravitational accel of perturbations / baryon-photon fluid
# 3) the acoustic oscillation: sound speed cs ~ c/sqrt(3), oscillation freq ~ k*cs.

z_rec=1089.0
print(f"\nAt recombination z={z_rec}:")
print(f"  cH(z_rec) = {c*H(z_rec):.3e} m/s^2")
# w=-1: a0 const = a0_now. DESI CPL: a0 ~ a0_now * (1+z)^-0.92 -> tiny.
a0_LCDM=a0_now
print(f"  a0 (w=-1, const) = {a0_LCDM:.3e}")
print(f"  a0 / cH(z_rec)   = {a0_LCDM/(c*H(z_rec)):.3e}  (a0 is ~1e7x BELOW cosmic accel)")

# Acoustic-scale acceleration of the baryon-photon fluid:
# Perturbation gravitational accel g_pert ~ G * delta_rho * lambda. 
# delta~1e-5, but more relevant: the restoring acceleration in an oscillating mode.
# Sound horizon r_s ~ 145 Mpc comoving ~ 0.13 Mpc physical at rec.
# Fluid oscillation: a_fluid ~ cs^2 * k = cs^2 / lambda. Peak k ~ 1/r_s.
cs=c/np.sqrt(3)
r_s_phys=0.13*Mpc  # physical sound horizon at recombination
a_acoustic = cs**2 / r_s_phys
print(f"\n  Acoustic restoring accel cs^2/r_s ~ {a_acoustic:.3e} m/s^2")
print(f"  a0/a_acoustic = {a0_LCDM/a_acoustic:.3e}  => a0 is ~{a_acoustic/a0_LCDM:.1e}x SMALLER")
print("  => baryon-photon fluid is DEEPLY Newtonian (a>>a0). NO MI modification of CMB peaks.")

# BBN z~3e8:
z_bbn=3.4e8
print(f"\nAt BBN z={z_bbn:.1e}:")
print(f"  cH(z_bbn) = {c*H(z_bbn):.3e} m/s^2  (enormous)")
print(f"  a0/cH = {a0_now/(c*H(z_bbn)):.2e}  => totally negligible. No BBN imprint.")

print("\nVERDICT Part D: At ALL early epochs every relevant acceleration >>> a0.")
print("  The inverted-horizon bath is utterly subdominant. NO CMB-peak or BBN imprint.")
print("  This is FORCED: a0~sqrt(rho_DE) is tiny early while g_cosmic~sqrt(rho_total) is huge.")
print("  => the framework predicts EARLY universe is EXACTLY standard (a clean null, but a")
print("     CONSEQUENCE: it forbids any early-MOND/EMG-style fix to S8/H0 from THIS a0).")

# The one possibly-new angle: the LOWEST-acceleration structures at modest z.
# Cosmic voids / the turnaround radius of the largest superclusters at z~0-1:
# turnaround accel ~ a0? The deepest-MOND cosmic accel is the supercluster turnaround.
print("\n"+"="*70)
print("PART D2: the LOWEST cosmic acceleration = supercluster turnaround / void edges")
print("="*70)
# turnaround radius where g_infall = a0: r_ta s.t. GM/r^2 = a0.
# For a supercluster M~1e15 Msun: 
Msun=1.989e30
for M in [1e14,1e15,1e16]:
    Mk=M*Msun
    r_ta=np.sqrt(G*Mk/a0_now)
    print(f"  M={M:.0e} Msun: turnaround r where g=a0 is r={r_ta/Mpc:.2f} Mpc")
print("  => Mpc-scale supercluster outskirts ARE in the deep-MOND regime TODAY.")
print("  a0(z) bump (+6% at z~0.4) shifts these turnaround radii by ~+3% (sqrt of 6%).")
print("  NOVEL but BELOW-FLOOR: turnaround-radius / void-size a0(z)-modulation ~3%, swamped by scatter.")
