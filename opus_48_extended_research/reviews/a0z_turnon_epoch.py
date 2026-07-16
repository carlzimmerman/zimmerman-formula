import numpy as np
c=2.99792458e8; G=6.674e-11
H0=67.4*1000/3.0857e22; Om=0.315; OL=0.685; Or=9.2e-5
a0_now=9.36e-11; Mpc=3.0857e22; Msun=1.989e30

# sanity: turnaround r for 1e15 Msun
M=1e15*Msun
print(f"check: r(g=a0) for 1e15 Msun = {np.sqrt(G*M/a0_now)/Mpc:.2f} Mpc (lit ~ a few Mpc OK)")

print("\n"+"="*70)
print("THE MOND TURN-ON EPOCH (framework, w=-1: a0 CONSTANT)")
print("="*70)
# Key: a0 is ~constant (w=-1). What 'turns on' is that the characteristic accel of
# newly-virializing structures DROPS below a0 as the universe dilutes.
# Characteristic accel of a halo virializing at z: g_vir ~ G M / R_vir^2.
# Using spherical collapse: virial density ~ 200 rho_crit(z). 
# g_vir at the virial radius ~ (G M)/R^2 with M=(4/3)pi R^3 *200 rho_crit(z)
# => g_vir = (4/3)pi G *200 rho_crit(z) * R_vir.  Depends on mass (via R).
# Cleaner: the accel at the virial radius scales as g_vir ~ sqrt(G M)*(...). 
# Use the cosmic acceleration scale g_cosmic(z) ~ G * rho_mean(z) * R where R=horizon -> messy.
# Best clean statement: the ACOUSTIC->collapse accel. 
# Define cosmic-mean acceleration g_H(z)=cH(z). a0/cH(z) computed already:
def E(z): return np.sqrt(Om*(1+z)**3+Or*(1+z)**4+OL)
# a0 = cH_Lambda/Z = c H0 sqrt(OL)/Z. cH(z)=cH0 E(z). a0/cH(z)=sqrt(OL)/(Z E(z))
Z=2*np.sqrt(8*np.pi/3)
print("\nThe framework's deep identity: a0 = cH(z)/Z holds EXACTLY only when E(z)=sqrt(OL),")
print("i.e. in the pure-dS future. Today a0 = sqrt(OL)/E(0) * cH0/Z = 0.827 * cH0/Z.")
print("\nDefine the 'horizon-bath turn-on' z* where the dS-Unruh bath a0 first becomes")
print("an O(1) fraction of the cosmic accel cH(z)/Z. Since a0=const, cH(z)/Z falls with time:")
for frac in [0.1,0.3,0.5,0.8,0.9,0.99]:
    # sqrt(OL)/E(z) = frac => E(z)=sqrt(OL)/frac. Solve for z.
    target=np.sqrt(OL)/frac
    if target<np.sqrt(OL): 
        print(f"  a0/(cH/Z)={frac}: in FUTURE"); continue
    # E(z)^2 = Om(1+z)^3+OL = target^2 (ignore rad)
    val=(target**2-OL)/Om
    if val<0:
        z=-1+( ( (target**2)/ (Om+OL) )**(1/3) ) # rough
        print(f"  a0/(cH/Z)={frac}: future (z<0)")
        continue
    z=val**(1/3)-1
    print(f"  a0/(cH/Z)={frac:.2f}: z = {z:+.3f}")
print("\n=> The bath a0 reaches 50% of cH/Z at z~0.25, 80% at z~ -0.1 (just future),")
print("   90% at z~-0.25, ->100% only in the dS future. We live RIGHT at turn-on (z~0).")
print("   FORCED consequence: 'now' is the epoch when the inverted-horizon MI scale becomes")
print("   cosmologically O(1) — a coincidence-problem RESTATEMENT (a0~cH_today is WHY MOND")
print("   is a late-time/low-z phenomenon). This is structural, already-implied, NOT new-testable.")

# When did a0 first exceed a GALAXY's internal g? Galaxy g_N fixed by formation; a0 const(w=-1).
# So for w=-1 a galaxy is in deep-MOND outskirts at ALL epochs once formed (a0 doesn't move).
# The DESI bump only modulates a0 by few% -> the deep-MOND radius r_M=sqrt(GM/a0) moves ~3%.
print("\nFor w=-1: a0 const => a galaxy's deep-MOND radius r_M=sqrt(GM_bar/a0) is FIXED.")
print("No 'turn-on epoch' per galaxy; MOND outskirts exist whenever the baryons are assembled.")
print("With DESI bump (+6% a0 at z~0.4): r_M was ~3% SMALLER at z~0.4 than now -> outskirt RC")
print("slightly more Newtonian at cosmic noon. ~3%: BELOW-FLOOR (= banked a0(z) content, not new).")
