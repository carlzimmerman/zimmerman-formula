import argparse,json,math
from pathlib import Path
import numpy as np
from medium import source,prediction,gap_quadrature,normal_modes,nonlinear
from collective_field import CollectiveField

G=6.67430e-11;A0=9.3603e-11;MSUN=1.98847e30;KPC=3.085677581491367e19;ETA=5.364
PROFILES=[(3e5,.3),(1e8,1.),(6e10,3.),(1e14,300.)]


def main(output):
    x=np.geomspace(1e-4,100.,121);y=x*x/(1+x);scans=[]
    for floor in (0.,1e-6,1e-4,.01,.1):
        for chi in np.geomspace(1,1e4,81):
            pred=np.array([prediction(float(a),float(chi),floor) for a in y])
            residual=np.log10(pred/x)
            scans.append(dict(chi=float(chi),floor=floor,max_error=float(np.max(abs(residual))),
                              rms_error=float(np.sqrt(np.mean(residual**2))),
                              residual_dex=residual.tolist()))
    best=min((r for r in scans if r['floor']==0),key=lambda r:r['max_error'])
    chi=best['chi'];fraction=chi/(1+chi)
    linear=[]
    for N in (16,32):
        s,w,n=gap_quadrature(N,10.)
        for k in np.geomspace(1e-3,1e3,31):
            omega=2*s;strength=10*w*omega**2
            frequencies,velocities=normal_modes(float(k),omega,strength,math.sqrt(1.1))
            linear.append(dict(N=N,k=float(k),max_speed=float(np.max(abs(velocities))),
                               highest_frequency=float(frequencies[-1]),
                               near_zero_frequency=float(np.min(abs(frequencies)))))
    # Exact single-resonance polariton benchmark, no free plasma.
    exact_errors=[]
    for k in (.01,.1,1.,10.,100.):
        w,_=normal_modes(k,np.array([2.]),np.array([3.]),0.)
        positive=w[w>1e-9]
        c=k*k+4+3;disc=np.sqrt(c*c-16*k*k)
        low2=8*k*k/(c+disc);high2=(c+disc)/2
        exact_errors.append(float(np.max(abs(positive/np.sqrt([low2,high2])-1))))
    nonlinear_runs=[]
    for D in (.1,.5,1.):
        r=nonlinear(D,10.,32,30.,1e-8);fine=nonlinear(D,10.,32,30.,1e-10)
        r['refined']=fine;r['final_change']=float(np.max(abs(np.array(r['final'])-fine['final'])))
        nonlinear_runs.append(r)
    positions=[[-2.,0.,0.],[2.,0.,0.]];fields=[]
    for N in (17,25,33):
        f=CollectiveField(N,24.,1.5)
        for charges in ([400.,-400.],[400.,400.]):
            r=f.solve(positions,charges,background=sum(charges)!=0)
            r['charges']=charges;fields.append(r)
    f=CollectiveField(33,24.,1.5);h=.001
    plus=f.solve([[-2+h,0,0],positions[1]],[400.,-400.]);minus=f.solve([[-2-h,0,0],positions[1]],[400.,-400.])
    fd=-(plus['dual_energy']-minus['dual_energy'])/(2*h)
    force_error=abs(fd/fields[4]['forces'][0][0]-1)
    # Physical inventory/oscillator-strength necessary conditions; optimistic all-mass budget.
    physical=[];eps=.1;age=10e9*365.25*86400
    for i,(M,b) in enumerate(PROFILES):
        M*=MSUN;b*=KPC;rho=3*ETA*M/(4*math.pi*b**3)
        tdyn=math.sqrt(b**3/(G*(1+ETA)*M))
        ellmin=(1+eps)*fraction**2*A0/(8*math.pi*G*rho)
        omega_max=math.sqrt(12*math.pi*G*rho/(eps*fraction))
        # Relevant critical modes have gap s~E/Ecut=x/f; mixing frequency sqrt2*Omega*s.
        relevant_bound=math.sqrt(2)*omega_max*1e-4/fraction
        physical.append(dict(profile_index=i,rho_available_kg_m3=rho,tdyn_Gyr=tdyn/(365.25*86400*1e9),
                             minimum_dipole_length_kpc=ellmin/KPC,minimum_length_over_b=ellmin/b,
                             maximum_cutoff_frequency_tdyn=omega_max*tdyn,
                             maximum_relevant_frequency_tdyn_at_x1e4=relevant_bound*tdyn,
                             maximum_relevant_frequency_age10Gyr_at_x1e4=relevant_bound*age,
                             screened_plasma_frequency_tdyn=math.sqrt(3*ETA/(eps*(1+ETA))),
                             screened_debye_over_b=(1+eps)/6*math.sqrt((1+ETA)/ETA)))
    summary=dict(static_parameter_points=len(scans),source_points=len(x),
                 best_static={k:best[k] for k in ['chi','floor','max_error','rms_error']},
                 static_points_below_point05=sum(r['max_error']<.05 for r in scans),
                 max_linear_group_speed=max(r['max_speed'] for r in linear),
                 max_exact_polariton_error=max(exact_errors),
                 max_coarse_energy_error=max(r['energy_error'] for r in nonlinear_runs),
                 max_refined_energy_error=max(r['refined']['energy_error'] for r in nonlinear_runs),
                 max_refined_norm_error=max(r['refined']['norm_error'] for r in nonlinear_runs),
                 max_nonlinear_final_refinement=max(r['final_change'] for r in nonlinear_runs),
                 max_counter_speed=max(r['max_speed'] for r in nonlinear_runs),
                 max_field_gauss=max(r['gauss_relative'] for r in fields+[plus,minus]),
                 field_force_derivative_error=force_error,
                 field_energy_refinement=abs(fields[2]['energy']/fields[4]['energy']-1),
                 field_force_refinement=abs(fields[2]['forces'][0][0]/fields[4]['forces'][0][0]-1),
                 like_charge_force_x=fields[5]['forces'][0][0],opposite_charge_force_x=fields[4]['forces'][0][0])
    assert summary['max_linear_group_speed']<=1+1e-12
    assert summary['max_exact_polariton_error']<1e-8
    assert summary['max_refined_energy_error']<1e-7
    assert summary['max_refined_norm_error']<1e-8
    assert summary['max_nonlinear_final_refinement']<1e-5
    assert summary['max_counter_speed']<1
    assert force_error<2e-4
    assert summary['like_charge_force_x']<0<summary['opposite_charge_force_x']
    result=dict(summary=summary,static_scan=scans,x_values=x.tolist(),linear_modes=linear,
                nonlinear=nonlinear_runs,field_tests=fields,field_difference=[plus,minus],physical_bounds=physical,
                scope='Causal field candidate and necessary conditions; no ionization or galaxy assembly simulation')
    Path(output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(summary,indent=2));print(json.dumps(physical,indent=2))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();main(a.output)
