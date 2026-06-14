import numpy as np
from scipy.integrate import quad
# Resolve the radial-SIGN of the density-a0 cluster shape (comprehensive review vs playbook).
G=6.674e-11; c=2.998e8; rho_DE=5.835e-27
a0F=0.5*c*np.sqrt(G*rho_DE); Msun=1.989e30; kpc=3.086e19; Mpc=1e3*kpc
M500=5e14*Msun; R500=1.3*Mpc; c500=3.5; rs=R500/c500
def m_nfw(r):
    x=r/rs; return M500*(np.log(1+x)-x/(1+x))/(np.log(1+c500)-c500/(1+c500))
beta=0.65; rc=150*kpc
def rho_gas(r): return (1+(r/rc)**2)**(-1.5*beta)
shape_int=quad(lambda r: rho_gas(r)*4*np.pi*r**2,1*kpc,R500)[0]
rho0=0.12*M500/shape_int
def m_gas(r): return quad(lambda rr: rho0*rho_gas(rr)*4*np.pi*rr**2,1*kpc,r)[0]
print(f"a0_framework={a0F:.3e}")
print(f"{'r/R500':>7} {'eta_field':>9} {'req':>7} {'pred√(rho/rhoDE)':>16} {'eta_after_localrho':>18}")
for r in np.array([0.1,0.2,0.3,0.5,0.7,1.0,1.3])*R500:
    gbar=G*m_gas(r)/r**2; gdyn=G*m_nfw(r)/r**2
    eta_field=gdyn/np.sqrt(gbar*a0F); pred=np.sqrt(rho0*rho_gas(r)/rho_DE)
    eta_after=gdyn/np.sqrt(gbar*a0F*pred)
    print(f"{r/R500:7.2f} {eta_field:9.3f} {eta_field**2:7.1f} {pred:16.2f} {eta_after:18.3f}")
# VERDICT: eta_field AND pred both rise inward (same sign); eta_after flattens to [0.75,1.30] (under-corrects center,
# over-corrects outskirts); does NOT cleanly close; same law breaks SPARC on galaxy disks (the trap).
