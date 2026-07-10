#!/usr/bin/env python3
import numpy as np
from methodA_ode import setup, solve_beta, J2_bulklimit, phantom_moment, nu
S=setup(9.36e-11,2.2,K0hat=0.5)
x0,J20=J2_bulklimit(S)
for b in [3e-3,3e-2,0.1,0.33]:
    xb,J2b,ok=solve_beta(S,b)
    # local P-wave prediction: J2 = Jt2 * kt/(kt+4b)
    kt=S['kt'](xb); Jt2=S['Jt2_of'](xb); Jloc=Jt2*kt/(kt+4*b)
    # compare in the sourcing shell rho~0.3..3
    m=(xb>0.3)&(xb<3.0)
    ratio_bvp_loc=np.trapz((J2b/Jloc)[m],xb[m])/np.trapz(np.ones(m.sum()),xb[m])
    # amplitude ratio vs analytic bulk in shell
    Jt2_0=np.interp(xb,x0,J20)
    amp=np.trapz((J2b/Jt2_0)[m],xb[m])/(xb[m][-1]-xb[m][0])
    print(f"b={b:6.3f} ok={ok} | <J2_bvp/J2_loc>_shell={ratio_bvp_loc:.3f}  <J2_bvp/Jt2>_shell={amp:.3f}"
          f"  pot-w={phantom_moment(S,xb,J2b,'pot')/phantom_moment(S,x0,J20,'pot'):.3f}"
          f"  dens-w={phantom_moment(S,xb,J2b,'density')/phantom_moment(S,x0,J20,'density'):.3f}")
# where is J2 concentrated? print profile
xb,J2b,ok=solve_beta(S,0.33)
y0=S['y0'](xb); W=(nu(y0)-1)*xb; Psi=W*J2b
for rr in [0.05,0.2,0.5,1,2,5,10]:
    i=np.argmin(abs(xb-rr))
    print(f"  rho={rr:5.1f} r={rr*S['r_t']/1.496e11:7.0f}AU  Jt2={S['Jt2_of'](np.array([rr]))[0]:+.3e}"
          f"  J2_bvp={J2b[i]:+.3e}  W={W[i]:.3e}  Psi={Psi[i]:+.3e}")
