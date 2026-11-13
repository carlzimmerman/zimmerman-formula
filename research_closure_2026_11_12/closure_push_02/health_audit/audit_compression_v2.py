#!/usr/bin/env python3
"""Independent endpoint and tangent-vector audit, without candidate imports."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.linalg import solve

C=1e6;GAMMA=1e-8;K0=1e4


def quantities(n,P,deriv):
    Pi=deriv(P);u=np.maximum(Pi,0);f=np.exp(u**3);h=n-Pi
    lp=3*u*u;lpp=6*u
    x=h*f/(2*C)
    ep=f*(-2*h+lp*h*h)/(4*C)+GAMMA*u
    epp=f*(2-4*lp*h+(lpp+lp*lp)*h*h)/(4*C)+GAMMA*(Pi>0)
    epn=f*(-1+lp*h)/(2*C)
    S=1/f;Sp=-lp*S;Spp=(9*u**4-6*u)*S
    A=2*C*S;b=2*C*x*Sp;c=1+b;D=C*x*x*Spp-GAMMA*(Pi>0)
    return dict(Pi=Pi,u=u,f=f,h=h,x=x,ep=ep,epp=epp,epn=epn,S=S,Sp=Sp,Spp=Spp,A=A,c=c,D=D)


def inspect(run,p):
    data=np.load(p/'compression_sources'/(run+'_results.npz'))
    record=json.loads((p/'compression_sources'/(run+'_results.json')).read_text())
    N=record['N'];modes=np.fft.fftfreq(N,1/N);modes[N//2]=0;k=modes*K0
    deriv=lambda f:np.fft.ifft(1j*k*np.fft.fft(f)).real
    inverse=lambda f:np.fft.ifft(np.divide(np.fft.fft(f),1j*k,out=np.zeros(N,complex),where=k!=0)).real
    theta=data['theta'];n0,v0=np.split(data['initial_state'],2);n1,v1=np.split(data['final_state'],2)
    def bump(center,width):
        r=np.angle(np.exp(1j*(theta-center)))/width
        z=np.zeros(N);j=np.abs(r)<1;z[j]=np.exp(1-1/(1-r[j]**2));return z
    up,down=bump(0,.55),bump(np.pi,2.3)
    P0=inverse(.86*(up-down*up.sum()/down.sum()));P1=data['final_P']
    rows=[]
    for label,n,v,P in [('initial',n0,v0,P0),('final',n1,v1,P1)]:
        z=quantities(n,P,deriv);WP=P/(1-np.abs(P))
        residual=-deriv(z['ep'])+WP
        fPhi=np.divide(-np.fft.fft(n),k*k,out=np.zeros(N,complex),where=k!=0)
        phi=np.fft.ifft(fPhi).real
        W=-np.abs(P)-np.log1p(-np.abs(P))
        energy=np.mean(n*v*v/2+z['h']**2*z['f']/(4*C)+W+GAMMA*z['u']**2/2+(n-n.mean())*phi/2)
        j=int(np.argmax(z['Pi']))
        rows.append({'label':label,'energy_mean':float(energy),'charge_mean':float(n.mean()),
                     'constraint_abs':float(np.max(abs(residual))),'minimum_charge':float(n.min()),
                     'max_Pi':float(z['Pi'].max()),'max_D':float(z['D'].max()),
                     'min_fixed_charge_P_hessian':float(z['epp'].min()),
                     'hessian_identity_abs':float(np.max(abs(z['A']*z['epp']-(z['c']**2-z['A']*z['D'])))),
                     'peak_highk_cs2':float(-n[j]*z['D'][j]/(z['A'][j]*z['epp'][j]))})
        if label=='initial':
            target=4*C*z['S']*(inverse(WP)-.15/C-GAMMA*z['u'])
            disc=1+3*z['u']**2*target
            low=-target/(1+np.sqrt(disc))
            rows[-1]['initial_charge_construction_error']=float(np.max(abs(n-(z['Pi']+low))))
        else:
            # Differentiate the actual nonlinear P stationarity equation in
            # time. No unstable continuation is integrated by this audit.
            Dmatrix=np.fft.ifft(1j*k[:,None]*np.fft.fft(np.eye(N),axis=0),axis=0).real
            Jacobian=-Dmatrix@(z['epp'][:,None]*Dmatrix)+np.diag(1/(1-np.abs(P))**2)
            Jacobian=(Jacobian+Jacobian.T)/2
            ndot=-deriv(n*v)
            Pdot=solve(Jacobian,deriv(z['epn']*ndot),assume_a='pos')
            pidot=deriv(Pdot);xdot=(ndot-z['c']*pidot)/z['A']
            Sppp=(-6+54*z['u']**3-27*z['u']**6)*z['S']
            Ddot=2*C*z['x']*z['Spp']*xdot+C*z['x']**2*Sppp*pidot
            tangent_res=Jacobian@Pdot-deriv(z['epn']*ndot)
            rows[-1].update(peak_Ddot=float(Ddot[j]),peak_Pidot=float(pidot[j]),
                            peak_ndot=float(ndot[j]),tangent_constraint_abs=float(np.max(abs(tangent_res))))
    return {'run':run,'N':N,'dt':record['dt'],'event_bracket':record['event_bracket'],'states':rows,
            'energy_relative_drift':abs(rows[1]['energy_mean']/rows[0]['energy_mean']-1),
            'charge_abs_drift':abs(rows[1]['charge_mean']-rows[0]['charge_mean'])}


def main(output):
    p=Path(__file__).parent;rows=[inspect(name,p) for name in ['compression256','compression512','compression512half']]
    checks={'reconstructed_initial_charge':max(r['states'][0]['initial_charge_construction_error'] for r in rows)<1e-10,
            'endpoint_constraints':max(z['constraint_abs'] for r in rows for z in r['states'])<2e-10,
            'Hamiltonian_Hessian_identity':max(z['hessian_identity_abs'] for r in rows for z in r['states'])<1e-12,
            'initial_D_nonpositive':all(r['states'][0]['max_D']<=0 for r in rows),
            'final_D_positive':all(r['states'][1]['max_D']>0 for r in rows),
            'positive_charge_and_auxiliary_Hessian':all(z['minimum_charge']>0 and z['min_fixed_charge_P_hessian']>0 for r in rows for z in r['states']),
            'negative_final_principal_coefficient':all(r['states'][1]['peak_highk_cs2']<0 for r in rows),
            'positive_tangent_Ddot_at_entry':all(r['states'][1]['peak_Ddot']>0 for r in rows),
            'energy_relative_drift_small':max(r['energy_relative_drift'] for r in rows)<1e-8,
            'charge_conserved':max(r['charge_abs_drift'] for r in rows)<1e-12}
    coarse=np.load(p/'compression_sources/compression256_results.npz');fine=np.load(p/'compression_sources/compression512_results.npz');half=np.load(p/'compression_sources/compression512half_results.npz')
    nf,vf=np.split(fine['final_state'],2);nh,vh=np.split(half['final_state'],2);nc,vc=np.split(coarse['final_state'],2)
    comparison={'spatial_final_charge_difference':float(np.max(abs(nc-nf[::2]))),
                'time_halving_final_charge_difference':float(np.max(abs(nh-nf))),
                'time_halving_final_velocity_difference':float(np.max(abs(vh-vf)))}
    result={'checks':checks,'all_pass':all(checks.values()),'count':len(checks),'rows':rows,'comparison':comparison,
            'scope':'Independent finite-NR endpoint and differentiated-constraint audit; no fullGR trajectory or continuum convergence proof'}
    Path(output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert result['all_pass']


if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--output',required=True);main(a.parse_args().output)
