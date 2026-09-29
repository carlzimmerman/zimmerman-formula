from cfg102_common import *
GF=cost_setup(*FLAG); GS=cost_setup(SUN[0],SUN[1],SUN[2])
print("POST-HOC exploration (not in frozen doc): flagship/Sun costs vs mu at fixed m2")
for m2 in (1e-16,1e-12):
    for mu in (1e24,1e25,1e26,3e26,1e27,3e27,1e28,3e28,1e29):
        chi,iF=solve_chi0(GF,mu,m2); fc=flagship_costs(GF,phi_chi(GF,iF,m2))
        chi,iS=solve_chi0(GS,mu,m2); sc=sun_cost(GS,phi_chi(GS,iS,m2))
        print(f"m2={m2:.0e} mu={mu:.0e}: Phi_F={fc['phi_over_vf2']:+.4g} F/gM={fc['force_over_gM']:+.4g} Sun={sc:+.4g} conv={iF['converged'] and iS['converged']}")
