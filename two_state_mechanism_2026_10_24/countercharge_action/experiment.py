import argparse,json,math
from pathlib import Path
import numpy as np
from field import Field,energy_density,lagrangian
from response import oscillation,rar_limit,equilibrium

G=6.67430e-11
HBAR=1.054571817e-34
C=299792458.
A0=9.3603e-11
GEV_KG=1.782661921e-27
MSUN=1.98847e30
KPC=3.085677581491367e19
ETA=5.364
PROFILES=[(3e5,.3),(1e8,1.),(6e10,3.),(1e14,300.)]


def main(output):
    positions=[[-2.,0.,0.],[2.,0.,0.]];fields=[]
    for N in (17,25,33):
        field=Field(N,24.,1.5)
        for charges in ([40.,-40.],[40.,40.]):
            row=field.solve(positions,charges,background=sum(charges)!=0)
            row['charges']=charges;fields.append(row)
    field=Field(33,24.,1.5);h=.001
    plus=field.solve([[-2.+h,0,0],positions[1]],[40.,-40.])
    minus=field.solve([[-2.-h,0,0],positions[1]],[40.,-40.])
    # Use stationary dual energy; residual diagnostic records variational accuracy.
    fd=-(plus['dual_energy']-minus['dual_energy'])/(2*h)
    force=fields[4]['forces'][0][0]
    force_error=abs(fd-force)/abs(force)
    controls=[]
    for amp in (.05,.3,.7):
        for eps in (1.,.1,.01):
            r=oscillation(amp,eps,30.,1e-9);fine=oscillation(amp,eps,30.,1e-11)
            r['refined']=fine
            r['final_displacement_change']=abs(r['final'][0]-fine['final'][0])
            controls.append(r)
    eps_values=np.geomspace(1e-4,1,17);xs=np.geomspace(1e-4,1e2,61)
    rar=[];scales=[];micro=[]
    for eps in eps_values:
        eps=float(eps)
        for x in xs:
            r=rar_limit(float(x),eps,.05)
            residual=abs(math.log10(equilibrium(x,eps,r)/x)-.05)
            rar.append(dict(x=float(x),epsilon=eps,max_counter_fraction=r,residual_dex=residual))
        for index,(M,b) in enumerate(PROFILES):
            # Independent dimensional calculation of scaling identities.
            M*=MSUN;b*=KPC;m=GEV_KG
            rho=3*ETA*M/(4*math.pi*b**3);n=rho/((1+eps)*m)
            q2=4*math.pi*G*m*m;v2=G*(1+ETA)*M/b
            T=(1+eps)*m*v2/6
            debye=math.sqrt(T/(2*n*q2));omega=math.sqrt(n*q2*(1/m+1/(eps*m)))
            tdyn=math.sqrt(b**3/(G*(1+ETA)*M))
            scales.append(dict(profile_index=index,epsilon=eps,debye_over_b=debye/b,
                               omega_tdyn=omega*tdyn,
                               negative_cold_acceleration_over_g=-(1+1/eps)))
        for mgev in np.geomspace(1e-6,1e19,101):
            m=float(mgev)*GEV_KG;mu=eps*m/(1+eps)
            alpha=G*m*m/(HBAR*C)
            core=math.sqrt(G*m/A0);bohr=HBAR/(mu*C*alpha)
            binding=.5*mu*C*C*alpha*alpha
            ratios=[]
            for M,b in PROFILES:
                v2=G*(1+ETA)*M*MSUN/(b*KPC)
                T=(1+eps)*m*v2/6
                ratios.append(binding/T)
            valid=bool(alpha<.1 and bohr>10*core)
            micro.append(dict(m_GeV=float(mgev),epsilon=eps,alpha_G=alpha,core_m=core,
                              bohr_over_core=bohr/core,binding_over_virial_temperature=ratios,
                              coulomb_applicable=valid))
    valid=[r for r in micro if r['coulomb_applicable']]
    convex=[]
    for e in np.geomspace(1e-6,1e2,41):
        d=e/(1+e)
        convex.append(dict(E_over_D0=float(e),legendre_error=float(abs(e*d-lagrangian(e)-energy_density(d))),
                           minimal_LS_speed_squared=float(1+e)))
    grid_energy=abs(fields[2]['energy']/fields[4]['energy']-1)
    grid_force=abs(fields[2]['forces'][0][0]/force-1)
    max_identity=0.
    for r in scales:
        eps=r['epsilon'];d=(1+eps)/6*math.sqrt((1+ETA)/ETA);w=math.sqrt(3*ETA/(eps*(1+ETA)))
        max_identity=max(max_identity,abs(r['debye_over_b']/d-1),abs(r['omega_tdyn']/w-1))
    summary=dict(field_solves=8,max_gauss_relative=max(r['gauss_relative'] for r in fields+[plus,minus]),
                 max_field_duality_error=max(r['duality_relative'] for r in fields+[plus,minus]),
                 field_force_derivative_error=force_error,grid25_to33_energy_relative=grid_energy,
                 grid25_to33_force_relative=grid_force,
                 repulsive_like_force_x=fields[5]['forces'][0][0],attractive_opposite_force_x=force,
                 max_mode_energy_error=max(max(r['relative_energy_error'],r['refined']['relative_energy_error']) for r in controls),
                 max_mode_refinement_change=max(r['final_displacement_change'] for r in controls),
                 min_mode_zero_crossings=min(r['zero_crossings'] for r in controls),
                 max_rar_inverse_error=max(r['residual_dex'] for r in rar),
                 max_profile_scaling_identity_error=max_identity,
                 microscopic_points=len(micro),coulomb_applicable_points=len(valid),
                 max_applicable_binding_over_T=np.max([r['binding_over_virial_temperature'] for r in valid],axis=0).tolist(),
                 rar_at_x_point1_epsilon_point1=rar_limit(.1,.1,.05))
    assert summary['max_gauss_relative']<2e-6
    assert force>0 and summary['repulsive_like_force_x']<0
    assert force_error<2e-4
    assert summary['max_mode_energy_error']<2e-6
    assert summary['max_mode_refinement_change']<2e-5
    assert summary['max_rar_inverse_error']<1e-10
    assert max_identity<1e-12
    result=dict(summary=summary,field_tests=fields,force_difference=dict(plus=plus,minus=minus,step=h,finite_difference=fd),
                modes=controls,rar=rar,plasma_scales=scales,microscopic=micro,constitutive=convex,
                scope='Necessary-condition tests; no conversion simulation or live galaxy assembly')
    Path(output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();main(a.output)
