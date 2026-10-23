import json,sys,numpy as np
from scipy.special import spherical_jn
M0=130257985.45037776;ell=.4404221297174536;t0=.012074272908402984
G=4.30091727003628e-6;H0=.0674;Om=.315;fc=1-1/6.364;rho0=fc*3*H0**2*Om/(8*np.pi*G);unit=M0/(4*np.pi*ell**3);vunit=ell/(t0*1.0227121650537077);rows=[]
for K in [.01,.025,.05,.1]:
 sigma=np.sqrt(K)*(rho0/unit)**(1/3)*vunit;D=2*sigma/(67.4*np.sqrt(Om))*(np.sqrt(1101)-1)
 kernel={str(k):float(3*spherical_jn(1,k*np.sqrt(5)*D)/(k*np.sqrt(5)*D)) for k in [.1,1,1/.04037934389859046]}
 rows.append(dict(K=K,sigma_today_kms=sigma,sigma_z1100_kms=1101*sigma,one_component_comoving_displacement_Mpc=D,displacement_over_seed=D/.04037934389859046,ballistic_density_kernel=kernel))
json.dump(dict(assumption='Uniform primordial waterbag with the same fine-grained occupancy as the proposed equilibrium; EdS, no gravitational deflection in kernel. Not a coupled growth prediction.',rho0_Msun_kpc3=rho0,rows=rows),open(sys.argv[1],'w'),indent=2);print(rows)
