import math
a0=1.2e-10; G=6.674e-11; c=2.998e8; Msun=1.989e30; AU=1.496e11
# CORRECT mass density (DW Eq 9/10, with c^2 so it equals ~ Omega_dm rho_crit):
rho0 = 45*a0**2/(16*math.pi*G*c**2)
rho_crit = 3*(2.2e-18)**2/(8*math.pi*G)   # H0~67.8 km/s/Mpc = 2.2e-18 /s
print("rho0 =", rho0, "kg/m^3 ;  rho_crit=", rho_crit, " ; rho0/rho_crit=", rho0/rho_crit)
# The mimetic dust CLUSTERS like CDM -> near Sun it reaches the local halo density:
rho_local = 6e-22   # ~0.3 GeV/cm^3 local DM density, the MOST it could be

def C2(rho, L=AU, w=3.7e5):
    # dimensionless coeff of (w.rhat)^2 U in g00 from a dust wake of density rho:
    # wake potential / source potential, (w/c)^2 already carried by the PPN term.
    # C2 ~ G*(rho * L^3 * focusing)/L / (G Msun / L) = rho L^3 focusing / Msun
    U = G*Msun/L; foc = U/w**2
    return rho*(4/3*math.pi*L**3)*foc/Msun

for name,rho in [("rho0(cosmological)",rho0),("rho_local(halo,generous)",rho_local)]:
    print(f"  {name}: C2^mim ~ {C2(rho):.2e}")
print("bounds: |alpha_2|<~1e-7 (LLR),  ~1e-9 (pulsar spin-precession, Shao&Wex)")
print("=> even the generous clustered case is >~10 orders below the pulsar bound.")
