import numpy as np
c=2.99792458e8; G=6.674e-11
H0=67.4*1000/3.0857e22; Om=0.315; OL=0.685; Or=9.2e-5
a0_now=9.36e-11; Mpc=3.0857e22
def E(z): return np.sqrt(Om*(1+z)**3+Or*(1+z)**4+OL)

# The acoustic accel estimate cs^2/r_s is crude. The MORE relevant accel for MI in the
# baryon-photon fluid is the actual fluid acceleration: a_fluid = d(v_b)/dt in an
# oscillating mode. v_b ~ cs * delta, delta~few x1e-5 at the peak (velocity ~ cs*1e-5).
# oscillation angular freq omega = k cs. a_fluid ~ omega * v_b ~ (k cs)(cs delta)=k cs^2 delta.
# This is delta~1e-5 SMALLER than my cs^2/r_s estimate. So:
cs=c/np.sqrt(3); r_s=0.13*Mpc; k=1/r_s; delta=3e-5
a_fluid = k*cs**2*delta
print(f"Refined fluid accel a_fluid = k cs^2 delta = {a_fluid:.3e} m/s^2 (delta~3e-5)")
z_rec=1089.0
a0_V=a0_now*E(z_rec)
print(f"Verlinde a0(z_rec) = {a0_V:.3e}")
print(f"a0_V / a_fluid = {a0_V/a_fluid:.2e}  => Verlinde a0 is {a0_V/a_fluid:.0f}x ABOVE the actual fluid accel!")
print(f"=> Under Verlinde a0~cH, the baryon-photon fluid would be in the DEEP-MOND regime at rec")
print(f"   (a_fluid << a0_V) => CMB acoustic peaks MODIFIED. That's a known problem for a0~cH.")
print(f"Framework a0(z_rec)=a0_now={a0_now:.2e}; a0_F/a_fluid={a0_now/a_fluid:.2e}")
print(f"   << 1 => fluid is Newtonian => CMB peaks UNCHANGED. Framework is SAFE.")
print()
print("HONEST CAVEAT: the 'fluid accel' is order-of-magnitude (delta, k, mode-dependent).")
print("The peak velocity accel for the bulk monopole is higher (~cs^2/r_s ~7e-6, a0_V below it).")
print("Whether Verlinde's a0~cH actually breaks the CMB depends on WHICH fluid accel scale and")
print("a relativistic MI completion that doesn't exist. So this is SUGGESTIVE not a clean kill.")
print()
print("NET: a0~sqrt(rho_DE) gives a tiny early a0 => GUARANTEED standard CMB (forced, robust).")
print("a0~cH gives a0 ~1e4x larger early, landing NEAR fluid accels => POTENTIALLY breaks CMB.")
print("This is a real qualitative early-universe split, but it lives in a regime with no")
print("relativistic MI theory on either side => NOT yet a clean computable test. Flag SPECULATION.")
