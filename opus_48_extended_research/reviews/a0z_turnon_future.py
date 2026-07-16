import numpy as np
from scipy.integrate import quad

c=2.99792458e8; G=6.674e-11
H0=67.4*1000/3.0857e22; Om=0.315; OL=0.685; Or=9.2e-5
a0_now=9.36e-11
Mpc=3.0857e22

def rho_de_ratio(z,w0,wa):
    a=1.0/(1.0+z)
    return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*(1-a))
def a0_z(z,w0,wa):
    return a0_now*np.sqrt(rho_de_ratio(z,w0,wa))

print("="*70)
print("PART B: The MOND turn-on epoch")
print("="*70)
# 'MOND turn-on' for a SYSTEM = when its internal g_N drops to a0(z), OR
# cosmologically when a0(z) first rises to exceed structure's g.
# Key insight: a0 is set by rho_DE which is ~CONSTANT (w~-1) or DECLINING early.
# So a0 does NOT 'turn on' late by rising; rather STRUCTURE's g_N drops as halos
# virialize at lower density at later times AND a0 itself rises slightly (DESI bump).
# The cosmic MOND-relevance epoch = matter-Lambda equality, where horizon-bath
# (a0~sqrt(rho_DE)) becomes comparable to cosmic-mean gravitational accel.

# Cosmic mean acceleration scale: g_cosmic ~ (4pi/3) G rho_m(z) R_H(z)?
# Better: the deep-MOND regime is reached for a system when g_N < a0.
# For a fixed baryonic system formed at z_f with internal g_N fixed, a0(z) evolution
# only modulates by ~few%. The REAL turn-on is structural.

# Most meaningful cosmological statement: a0(z) vs the Hubble accel cH(z).
# Define g_H(z)=c*H(z). MOND regime relevant when a0(z) ~ order cH(z) i.e. Z~2.
def E(z): return np.sqrt(Om*(1+z)**3+Or*(1+z)**4+OL)  # LCDM for H
print("\nRatio a0(z)/(cH(z)) — the framework says a0=cH_Lambda/Z, Z=2sqrt(8pi/3)=5.79:")
Z=2*np.sqrt(8*np.pi/3)
print(f"  Z = {Z:.4f};  at z=0: cH0/a0 = {c*H0/a0_now:.3f} (full H0, not H_Lambda)")
cHL=c*H0*np.sqrt(OL)  # H_Lambda = H0 sqrt(OL)
print(f"  cH_Lambda/a0 = {cHL/a0_now:.3f}  (matches Z={Z:.2f}) ✓ framework identity")
for z in [0,0.3,0.5,1,2,3,5,10]:
    print(f"  z={z:4.1f}: a0(z)/(cH(z)) [w=-1] = {a0_now/(c*H0*E(z)):.4f}")

print("\n MOND-turn-on (cosmic): a0 ~ cH(z)/Z holds at LATE times; at high z, H(z) grows")
print(" so cH(z) >> a0 => the inverted-horizon bath is SUBDOMINANT to cosmic expansion accel.")
# find z where a0(z=const,w=-1) = cH(z)/Z i.e where E(z)*sqrt(OL)... 
# a0=cH_L/Z, cH(z)/Z = cH0 E(z)/Z. a0/(cH(z)/Z)= (cH_L/Z)/(cH0 E/Z)= sqrt(OL)/E(z).
# =1 when E(z)=sqrt(OL) -> only at... E(z)>=1 always for z>=0, sqrt(OL)<1, never=1 for z>0.
# At z=0 E=1, ratio=sqrt(OL)=0.83. So a0 is ALWAYS below cH(z)/Z except asymptotic future.
print("\n => a0(z)/(cH(z)/Z) = sqrt(OL)/E(z): =0.827 today, ->0 in past, ->1 in far future.")
print("    The horizon-bath scale a0 becomes a FIXED FRACTION of cH only as z->-1 (future).")

print("\n"+"="*70)
print("PART C: FAR FUTURE (Lambda domination, a->inf, z->-1)")
print("="*70)
# w=-1: rho_DE const => a0 -> a0_now EXACTLY. H -> H_dS = H0 sqrt(OL).
H_dS=H0*np.sqrt(OL)
print(f"  H -> H_dS = H0 sqrt(OL) = {H_dS:.4e} s^-1")
print(f"  cH_dS = {c*H_dS:.4e};  cH_dS/Z = {c*H_dS/Z:.4e};  a0_now = {a0_now:.4e}")
print(f"  => asymptotically a0 = cH_dS/Z EXACTLY (the Z identity becomes EXACT, not approx).")
print(f"  Today the identity uses H_Lambda=H0 sqrt(OL) already, so it's exact NOW too in that footing.")
# Far-future structure: all unbound structure recedes; bound halos: g_N fixed, a0 fixed
# => the deep-MOND outskirts FREEZE. RAR becomes EXACTLY stationary.
print("\n  Far-future consequence: rho_DE->const => a0 FREEZES at a0_now.")
print("  Every bound system's RAR becomes PERMANENTLY stationary (a0 no longer drifts).")
print("  Contrast a0~cH (Verlinde): cH->cH_dS=const TOO. Both freeze. NOT a discriminator in far future.")

# DESI CPL far future (z->-1, a->inf): exp(-3wa(1-a)), a->inf => exp(-3wa*(1-inf))=exp(+inf*3wa)
# wa<0 => -3wa>0, (1-a)->-inf => exp(-3wa * -inf)=exp(-inf)=0. rho_DE->0!
print("\n  [DESI CPL far future]: w(a)=w0+wa(1-a), a->inf => w-> w0+wa(-inf)=+inf (wa<0).")
print("  rho_DE(a)~ a^{3(1+w0+wa)} exp(-3wa(1-a)); a->inf, wa<0 => exp(-3wa*(-a)) = exp(3wa*a)->0.")
print("  => DESI CPL literally extrapolated: rho_DE->0 in future => a0->0 => MOND scale VANISHES.")
print("  (Unphysical extrapolation, but it's the literal w0wa content: a thawing-then-vanishing DE.)")
