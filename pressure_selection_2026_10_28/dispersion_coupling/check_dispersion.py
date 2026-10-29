"""Finite audit of PN28's explicit dispersion-metric model.

No acceleration target appears in this code. It checks local action algebra,
a specified waterbag constitutive reduction, and homogeneous scalar/outlet
dynamics. It is not a full kinetic, gravitational, or cosmological simulation.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize_scalar
import sympy as sp


# Exact Legendre check in one dimension with two arbitrary positive streams.
n1, n2, F, Z = sp.symbols('n1 n2 F Z', positive=True)
v1, v2, st, sx = sp.symbols('v1 v2 st sx', real=True)
n = n1 + n2
u = (n1*v1+n2*v2)/n
Kv = (n1*(v1-u)**2+n2*(v2-u)**2)/2
Ds = st+u*sx
Lkin = n*u*u/2+Z*Kv+F*F*Ds*Ds/2
mom1, mom2 = sp.diff(Lkin,v1)/n1, sp.diff(Lkin,v2)/n2
pi = sp.diff(Lkin,st)
Legendre = sp.simplify(n1*mom1*v1+n2*mom2*v2+pi*st-Lkin)
positive_energy = n*u*u/2+Z*Kv+pi*pi/(2*F*F)
legendre_residual = sp.simplify(Legendre-positive_energy)
relative_momentum_residual = sp.simplify(mom1-mom2-Z*(v1-v2))

y, B, rho = sp.symbols('y B rho', positive=True)
E = 3*B*(y-1)/2
Umat = B*(y-sp.log(y)-1)
Pmat = sp.simplify(2*E/3-Umat)
dlnrho_dy = sp.Rational(2,5)/y+sp.Rational(3,5)/(y-1)
Aeff = sp.simplify(sp.diff(Pmat,y)/dlnrho_dy)
e_rr = 5*B*(y-1)/(3*rho*rho)
e_rs = -5*B*(y-1)/rho
e_ss = 3*B*(5*y-2)
schur = sp.simplify(e_rr-e_rs*e_rs/e_ss)


def effective(s, K, B=1.0, epsilon=0.0):
    return K*math.exp(-2*s)+B*math.expm1(3*s)-3*B*s + epsilon*B*(math.expm1(6*s)-6*s)

def stationary(s, K, B=1.0, epsilon=0.0):
    return -2*K*math.exp(-2*s)+3*B*math.expm1(3*s)+6*epsilon*B*math.expm1(6*s)

def solve_s(K, B=1.0, epsilon=0.0):
    return brentq(lambda s: stationary(s,K,B,epsilon),0.0,20.0,
                  xtol=3e-14,rtol=3e-14)


equilibria=[]
for K in [0.001,0.01,0.1,1.0,10.0,100.0,10000.0]:
    se=solve_s(K)
    independent=minimize_scalar(lambda s: effective(s,K),bounds=(-4,5),
                                method='bounded',options={'xatol':2e-13})
    ye=math.exp(3*se)
    # Independent fixed-mass/phase-volume derivative: K density scales V^-5/3.
    dh=2e-5
    def total_energy(volume):
        kc=K*volume**(-5.0/3.0)
        return volume*effective(solve_s(kc),kc)
    p_fd=-(total_energy(1+dh)-total_energy(1-dh))/(2*dh)
    p_formula=math.log(ye)
    equilibria.append({
        'K_over_B':K,'s_equilibrium':se,'y':ye,
        'independent_minimizer_s_difference':abs(se-independent.x),
        'conjugate_kinetic_pressure_over_B':ye-1,
        'total_material_pressure_over_B':p_formula,
        'total_pressure_volume_derivative':p_fd,
        'scaled_pressure_derivative_error':abs(p_fd-p_formula)/(1+abs(p_formula)),
        'Aeff_over_B':5*(ye-1)/(5*ye-2),
        'final_relative_energy_over_initial':math.exp(-2*se),
        'predicted_exported_energy':K-effective(se,K),
    })


trajectories=[]
gamma=0.6
for K in [0.03,0.3,3.0,30.0]:
    se=solve_s(K)
    def rhs(t,state):
        sc,speed,out=state
        return [speed,-stationary(sc,K)-gamma*speed,gamma*speed*speed]
    sol=solve_ivp(rhs,[0.0,120.0],[0.0,0.0,0.0],method='DOP853',
                  rtol=2e-11,atol=2e-13,max_step=0.04)
    assert sol.success
    sv,speed,rad=sol.y
    e_rel=K*np.exp(-2*sv)
    e_scalar=0.5*speed**2+np.expm1(3*sv)-3*sv
    trajectories.append({
        'K':K,'s_equilibrium':se,'s_final':float(sv[-1]),
        'speed_final':float(speed[-1]),
        'relative_energy_initial':K,'relative_energy_final':float(e_rel[-1]),
        'scalar_energy_final':float(e_scalar[-1]),
        'exported_energy':float(rad[-1]),
        'predicted_exported_energy':K-effective(se,K),
        'maximum_absolute_energy_ledger_error':float(max(abs(e_rel+e_scalar+rad-K))),
    })


# The finite-frequency calculation uses the explicitly restricted isotropic
# waterbag fluid closure, without gravity. It is not the full Vlasov spectrum.
modes=[]
bm=0.1
cs2=0.64
for ye in [1.001,1.1,2.0,10.0,100.0]:
    rh=ye**0.4*(ye-1)**0.6  # rho_*=1
    err=5*bm*(ye-1)/(3*rh*rh)
    ers=-5*bm*(ye-1)/rh
    ess=3*bm*(5*ye-2)
    cinf=rh*err
    for kval in [0.0,0.001,0.03,0.3,3.0,30.0]:
        aa=cinf*kval*kval
        bb=cs2*kval*kval+ess
        coupling=rh*ers*ers*kval*kval
        hi=(aa+bb+math.sqrt((aa-bb)**2+4*coupling))/2
        determinant=aa*bb-coupling
        lo=determinant/hi
        modes.append({'y':ye,'wave_number':kval,'omega_squared_low':lo,
                      'omega_squared_high':hi,'determinant':determinant})


deformations=[]
for eps in [0.01,0.1,1.0]:
    for K in [1e4,1e8,1e12]:
        se=solve_s(K,epsilon=eps)
        b=math.exp(-2*se)
        up=math.expm1(3*se)-3*se+eps*(math.expm1(6*se)-6*se)
        pressure=2*K*b/3-up
        ess=4*K*b+9*math.exp(3*se)+36*eps*math.exp(6*se)
        pK=2*b/3-20*K*b*b/(3*ess)
        log_slope=(5*K/3)*pK/pressure
        deformations.append({'epsilon':eps,'K_over_B':K,
                             'dlnP_dlnrho':log_slope})


checks={
    'exact_legendre_positive_energy_identity':legendre_residual==0,
    'exact_relative_momentum_metric':relative_momentum_residual==0,
    'exact_total_pressure_identity':sp.simplify(Pmat-B*sp.log(y))==0,
    'exact_log_slope_identity':sp.simplify(Aeff-5*B*(y-1)/(5*y-2))==0,
    'exact_schur_complement_identity':sp.simplify(schur-Aeff/rho**2)==0,
    'independent_scalar_minimizers':max(r['independent_minimizer_s_difference'] for r in equilibria)<1e-7,
    'independent_full_energy_pressure':max(r['scaled_pressure_derivative_error'] for r in equilibria)<2e-7,
    'actual_random_energy_export_in_four_cases':all(r['relative_energy_final']<r['relative_energy_initial'] and r['exported_energy']>0 for r in trajectories),
    'four_reduced_equilibrations':all(abs(r['s_final']-r['s_equilibrium'])<1e-8 and abs(r['speed_final'])<1e-8 for r in trajectories),
    'reciprocal_energy_ledgers':max(r['maximum_absolute_energy_ledger_error']/(1+r['K']) for r in trajectories)<2e-8,
    'conditional_finite_rate_modes_nonnegative':all(r['omega_squared_low']>=-1e-13 and r['omega_squared_high']>0 for r in modes),
    'fixed_vacuum_deformation_reaches_power_law':all(abs(r['dlnP_dlnrho']-1.25)<0.003 for r in deformations if r['K_over_B']==1e12),
}
result={
    'checks':checks,'equilibria':equilibria,'exchange_trajectories':trajectories,
    'conditional_hydrodynamic_modes':modes,'fixed_vacuum_deformations':deformations,
    'software':{'Python':sys.version.split()[0],'NumPy':np.__version__,
                'SciPy':scipy.__version__,'SymPy':sp.__version__},
    'non_claims':[
        'No microscopic selection of the exponential/linear scalar potential or waterbag state',
        'No relation between B and gravitating vacuum energy V',
        'No full Vlasov or self-gravitating perturbation spectrum',
        'No full spatial collapse, cosmology, or derivation of the wave outlet from the three-dimensional parent',
    ],
}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks':checks,'equilibria':equilibria,
                  'exchange_trajectories':trajectories,
                  'fixed_vacuum_deformations':deformations},indent=2))
assert all(checks.values())
