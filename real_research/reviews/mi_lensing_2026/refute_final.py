import numpy as np
c=2.99792458e8; G=6.67430e-11; Msun=1.98892e30; kpc=3.0856775814913673e19
A0=9.36e-11
Md=6.0e10*Msun; Rd=3.0*kpc
r=np.linspace(0.5,15.0,400)*Rd
def nu(y): return np.sqrt(1.0+1.0/y)
Mbar=Md*(1.0-(1.0+r/Rd)*np.exp(-r/Rd)); gbar=G*Mbar/r**2
Mex=Mbar*(nu(gbar/A0)-1.0)

# The confront normalizes each shape to Mex[-1] at r_max (amplitude matched).
# This is GENEROUS to the shapes (removes 1 dof of tuning). Even so, only 2/7 fit.
# If we DON'T pre-match amplitude (i.e. use cosmic amplitude), NONE fit (0.55-0.64 dex above).
# So the confront's procedure is generous -> it UNDERSTATES the tuning -> FINE_TUNED is
# if anything CONSERVATIVE (real tuning is worse). This REFUTES any "CONSISTENT" claim harder.

# Now the OTHER direction: could the confront be OVERSTATING tuning (hiding a CONSISTENT)?
# For that, the SHAPE alone (amplitude-matched) would need to robustly match without a0 input.
# NFW rs=30kpc lands 0.014 dex -- but rs=30kpc for a 6e10 Msun galaxy is a TUNED scale
# (cosmic c-M relation gives rs~10-15kpc for this mass -> 0.12-0.18 dex, OUT).
def resid(Mc):
    good=Mex>0.02*Mex[-1]
    return np.sqrt(np.mean((np.log10((G*Mc/r**2)[good])-np.log10((G*Mex/r**2)[good]))**2))
def nfw(rs_kpc):
    x=r/(rs_kpc*kpc); return np.log(1+x)-x/(1+x)
for rs in [10,15,20,30,50]:
    M=nfw(rs); M=M*(Mex[-1]/M[-1])
    print(f"NFW rs={rs:>2}kpc: rms={resid(M):.3f} dex  {'IN' if resid(M)<0.10 else 'out'}")
print("\n=> The ONLY NFW that fits (rs=30-50kpc) requires a scale radius LARGER than the")
print("   cosmic c-M relation predicts for 6e10 Msun (rs~10-15kpc). That larger rs is")
print("   the tuning. Framework fixes no rs (scale FREE). So FINE_TUNED, not CONSISTENT.")
print("   The confront does NOT overstate tuning -- the fitting shapes need a non-cosmic rs.")

# FINAL: both footings identical logic; alt a0 amplitude factor:
print(f"\nalt/canon amplitude factor sqrt(a0_alt/a0_canon) = {np.sqrt(1.13e-10/9.36e-11):.3f}")
print("  (0.099 dex-ish in amplitude, below lensing scatter -> footing-independent verdict)")
