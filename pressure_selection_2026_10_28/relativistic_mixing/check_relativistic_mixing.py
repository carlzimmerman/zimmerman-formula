#!/usr/bin/env python3
"""PN28 bounded relativistic mixture checks. No gravity or EOS fit is performed."""
import json, math, sys
from pathlib import Path
import numpy as np
import scipy
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import kve
import sympy as s

PI=math.pi
def logZ(z):
    """log integral d^3p exp[-z(sqrt(1+p^2)-1)], m=c=1."""
    if z<1e-6:
        return math.log(8*PI)-3*math.log(z)+z-z*z/4
    if z>1e5:
        a=[15/8,105/128,-945/3072,31185/98304]
        S=1+sum(v/z**(j+1) for j,v in enumerate(a))
        return 1.5*math.log(2*PI)-1.5*math.log(z)+math.log(S)
    return math.log(4*PI)+math.log(float(kve(2,z)))-math.log(z)

def D(z):
    if z<1e-6:
        return 3-z+z*z/2
    if z>1e5:
        a=[15/8,105/128,-945/3072,31185/98304]
        S=1+sum(v/z**(j+1) for j,v in enumerate(a))
        return 1.5+sum((j+1)*v/z**(j+1) for j,v in enumerate(a))/S
    return 3+z*(float(kve(1,z)/kve(2,z))-1)

def independent_level_integrals(z):
    # w=z*E. Large-z scaling keeps the integral's size moderate.
    def wgt(w):
        if z>=1:
            return (1+w/z)*math.sqrt(w*(2+w/z))*math.exp(-w)
        return (w+z)*math.sqrt(w*(w+2*z))*math.exp(-w)
    j=quad(wgt,0,np.inf,epsabs=2e-12,epsrel=2e-12,limit=150)[0]
    e=quad(lambda w:w*wgt(w),0,np.inf,epsabs=2e-12,epsrel=2e-12,limit=150)[0]/j
    p=quad(lambda w:w*(w+2*z)/(3*(w+z))*wgt(w),0,np.inf,
           epsabs=2e-12,epsrel=2e-12,limit=150)[0]/j
    lq=math.log(4*PI)-3*math.log(z)+math.log(j)+(1.5*math.log(z) if z>=1 else 0)
    return lq,e,p

def I_integral(zmin,zmax):
    low,high=math.log(zmin),math.log(zmax)
    edges=sorted(set([low,high]+[x for x in [-14,0,12] if low<x<high]))
    return sum(quad(lambda u:D(math.exp(u)),a,b,epsabs=2e-9,epsrel=2e-11,limit=100)[0]
               for a,b in zip(edges,edges[1:]))

def spectrum(p,zmin,zmax):
    E=p*p/(math.hypot(1,p)+1)
    center=-math.log(E)
    low,high=math.log(zmin),math.log(zmax)
    edges=sorted(set([low,high]+[u for u in [center-8,center,center+8,0] if low<u<high]))
    # A_mix=1; rescale to prevent a large/small final integrand.
    reference=3/(2*PI)*p**-5 if p<1 else 3/(4*PI)*p**-4
    value=0.0
    for lo,hi in zip(edges,edges[1:]):
        value+=quad(lambda u:math.exp(u-math.exp(u)*E-logZ(math.exp(u))-math.log(reference)),
                    lo,hi,epsabs=3e-10,epsrel=3e-10,limit=100)[0]
    return value, 4*PI*p**3*E*(reference*value)

def main():
    output=Path(sys.argv[1]); checks={}
    p,m,c,E=s.symbols('p m c E',positive=True)
    kinetic=s.sqrt(m*m*c**4+p*p*c*c)-m*c*c
    checks['pointwise_pressure_energy_ratio']=bool(s.simplify(
        (p*s.diff(kinetic,p)-kinetic*(kinetic+2*m*c*c)/(kinetic+m*c*c)))==0)
    z=s.symbols('z',positive=True)
    # Primitive derivative for the large-z log expansion is checked separately numerically.
    rows=[]
    for zv in [1e-8,1e-4,.1,1.,10.,1e3,1e8]:
        li,ei,pi=independent_level_integrals(zv)
        rows.append({'z':zv,'logZ_residual':logZ(zv)-li,'D':D(zv),
                     'independent_mean_zE':ei,'D_residual':D(zv)-ei,'pressure_equipartition':pi})
    checks['partition_vs_independent_energy_measure']=max(abs(r['logZ_residual']) for r in rows)<2e-10
    checks['energy_vs_independent_energy_measure']=max(abs(r['D_residual']) for r in rows)<2e-10
    checks['pressure_equipartition']=max(abs(r['pressure_equipartition']-1) for r in rows)<2e-11
    checks['level_pressure_energy_bound']=all(1.5<r['D']<3 for r in rows)

    spans=[]
    for low,high in [(1e-8,1e-4),(1e-3,1e3),(1e4,1e10),(1e-120,1e12)]:
        exact=logZ(low)-logZ(high); integrated=I_integral(low,high)
        spans.append({'zmin':low,'zmax':high,'I_log_partition_ratio':exact,'I_integrated_D':integrated,
                      'relative_residual':integrated/exact-1,'D_bar':exact/math.log(high/low)})
    checks['mixture_energy_partition_identity']=max(abs(r['relative_residual']) for r in spans)<2e-10

    tails=[]
    for regime,lo,hi,ps in [('NR',1e3,1e12,[1e-4,3e-4,1e-3]),('UR',1e-12,1e-3,[1e5,3e5,1e6])]:
        for pv in ps:
            ratio,spectral=spectrum(pv,lo,hi)
            tails.append({'regime':regime,'p_over_mc':pv,'f_over_asymptotic':ratio,
                          'dK_dlnp_over_A_mix':spectral,'zmin':lo,'zmax':hi})
    checks['NR_and_UR_intermediate_tails']=max(abs(r['f_over_asymptotic']-1) for r in tails)<3e-5
    checks['energy_plateau_both_limits']=max(abs(r['dK_dlnp_over_A_mix']/3-1) for r in tails)<3e-5

    # Counterfamily: fixed K=1 and R=1e6, with beta/C adjusted. Density is free.
    fixed_energy=[]; lr=math.log(1e6)
    for high in [1e-3,1.,1e3,1e9]:
        low=high/1e6; I=logZ(low)-logZ(high); a=1/I
        fixed_energy.append({'R':1e6,'K':1.,'zmax':high,'zmin':low,'A_mix':a,
            'P':a*lr,'rho_c2':a*(high-low),'D_bar':I/lr})
    checks['fixed_energy_span_allows_varying_A']=fixed_energy[-1]['A_mix']/fixed_energy[0]['A_mix']>1.99

    # Conditional control ONLY; both identifications below are inherited unproved assumptions.
    lr=1/0.00353241107337; target=.0023294580123; cond=[]
    for density_contrast in [1e3,1e6,1e9]:
        fun=lambda u:(logZ(math.exp(u-lr))-logZ(math.exp(u)))/(math.exp(u)*(1-math.exp(-lr)))-1/density_contrast
        high=math.exp(brentq(fun,-5,45,xtol=1e-12)); low=high*math.exp(-lr)
        I=logZ(low)-logZ(high); a=1/I
        cond.append({'rho_over_rhoLambda':density_contrast,'zmax':high,'zmin':low,'I':I,'D_bar':I/lr,
                     'A_mix_over_V_if_K_equals_V':a,'ratio_to_canonical_target':a/target,
                     'ratio_to_NR_near_match':a/(2/(3*lr)),
                     'specific_energy_constraint_relative_residual':(I/(high-low))*density_contrast-1})
    checks['conditional_energy_density_solved']=max(abs(r['specific_energy_constraint_relative_residual']) for r in cond)<2e-11
    assert all(checks.values()),checks
    result={'claim_id':'PN28_RELATIVISTIC_PHASE_MIXING','checks':checks,'level_integrals':rows,
            'mixture_integrals':spans,'tail_checks':tails,'fixed_K_and_R_counterfamily':fixed_energy,
            'conditional_old_near_match':{'derived_identifications':False,'lnR':lr,'canonical_target':target,
                'NR_A_over_K':2/(3*lr),'UR_A_over_K':1/(3*lr),'rows':cond},
            'software':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'sympy':s.__version__},
            'non_claims':['No derivation of gamma=C/eta','No identification of kinetic and vacuum energy',
                'No phase-density to spatial-density mapping','No spatial EOS inferred from momentum tails',
                'No quantum or full excluded-occupancy inversion','No self-gravitating relativistic equilibrium']}
    output.write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))

if __name__=='__main__': main()
