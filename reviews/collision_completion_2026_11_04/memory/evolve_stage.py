"""Changing charged shape plus actual massive late neutral cascade on saved orbit.

Conditional stage: recorded scalar orbit, vacuum neutral selfenergies, dilute
final states. Uses occupation-independent K, not an old multiplier. Secondary
cascade is eliminated only at the slow cosmological scale after a delay test;
its full terminal momentum distribution, rest mass, redshift and force remain.
"""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[k]='1'
from pathlib import Path
import json,time,math,resource
import numpy as np
from scipy.integrate import solve_ivp
from scipy.sparse.linalg import splu
from response_api_v3 import *
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/cascades'))
from transfer import build_transfer

def interpolate_table(N,Ns,table):
    i=int(np.clip(np.searchsorted(Ns,N)-1,0,len(Ns)-2));a=(N-Ns[i])/(Ns[i+1]-Ns[i])
    return (1-a)*table[i]+a*table[i+1]

def main(out,kout):
    start=time.monotonic()
    early=json.loads((PRIOR/'kinetics/run_leading_two_001/result.json').read_text())['case']
    late=json.loads((PRIOR/'kinetics/run_hybrid_bw_001/result.json').read_text())['case']
    packet=json.loads((PRIOR/'gravity_resonance/run_leading001/result.json').read_text())['packet']
    data=json.loads((ROOT/'reviews/collision_completion_2026_11_04/cascades/run_network001/result.json').read_text())['cases'][-2]
    channels=json.loads((ROOT/'reviews/collision_completion_2026_11_04/cascades/run_basis002/result.json').read_text())['Gamma_by_daughter_pair_CT09_mu'];data['singlet_channel_Gamma']=channels
    edges=np.asarray(late['q_edges']);W=(edges[1:]**3-edges[:-1]**3)/3;f0=np.asarray(early['final_f_S_number_normalization'])
    history=late['history'];Ns=np.asarray([h['N'] for h in history]);N0=Ns[0]
    omega=math.sqrt(float(packet['local_profile']['radial_curvature_mu2'])/62);H0=history[0]['H_over_oscillation']*omega
    gamma_keys=list(channels);Ks=[];Kstat=[];KC=[];KE=[];KB=[];parentmom=[];refinements=[]
    for i,h in enumerate(history):
        args=dict(xmid=h['x_minimum'],amplitude=(h['x_outer']-h['x_inner'])/2,omega=omega,Tc=h['Tc_over_mu'],edges=edges)
        k=band_kernel(**args,radial=2,angular=12,channels=channels)
        Ks.append(k['K']);Kstat.append(k['K_stationary']);KC.append([k['channel_K'][key] for key in gamma_keys])
        KE.append(k['neutral_exit_energy_rate_pair']);KB.append(k['absolute_energy_exchange_bound_pair']);parentmom.append(k['parent_energy_density_pair'])
        if i in (0,40,79):
            fine=band_kernel(**args,radial=3,angular=20)
            prob=W*f0/float(W@f0)
            refinements.append(dict(history_index=i,relative=abs(float(prob@k['K']@prob)/float(prob@fine['K']@prob)-1)))
    Ks=np.asarray(Ks);Kstat=np.asarray(Kstat);KC=np.asarray(KC);KE=np.asarray(KE);KB=np.asarray(KB);parentmom=np.asarray(parentmom)
    def therm(N):
        Tc=history[0]['Tc_over_mu']*math.exp(-(N-N0));H=H0*math.exp(-2*(N-N0));s=2*math.pi**2/45*106.75*(Tc/.02)**3
        return Tc,H,s
    def evolve(table):
        def rhs(N,y):
            Tc,H,s=therm(N);f=np.exp(y);n=12*Tc**3/(2*math.pi**2)*W*f
            return -(interpolate_table(N,Ns,table)@n)/H
        return solve_ivp(rhs,[Ns[0],Ns[-1]],np.log(f0),t_eval=Ns,rtol=3e-8,atol=2e-9,max_step=.005)
    sol=evolve(Ks);control=evolve(Kstat);fgrid=np.exp(sol.y.T);fgstat=np.exp(control.y.T)
    # Actual one-body cascade terminal map and tested cosmological delay.
    tr=build_transfer(data,angles=6);A=tr['A'];diag=A.diagonal();unstable=np.flatnonzero(diag<0);stable=np.flatnonzero(diag==0)
    AU=A[unstable][:,unstable].tocsc();AZ=A[stable][:,unstable].tocsr();lu=splu(AU)
    terminal={};delay={};energyerr={}
    for key in gamma_keys:
        inj=tr['injection'][key];integrated=-lu.solve(inj[unstable]);T=inj[stable]+AZ@integrated
        second=lu.solve(lu.solve(inj[unstable]));moment=AZ@second
        terminal[key]=T;valid=T>1e-11;delay[key]=float(max(moment[valid]/T[valid])) if np.any(valid) else 0.
        energyerr[key]=abs(float(tr['energies'][stable]@T)/M-1)
    Tmat=np.asarray([terminal[key] for key in gamma_keys]);p=tr['p'];npnode=len(p);ev=tr['events']
    stable_flat=tr['active'][stable];stable_gid=[ev.groups[i//npnode]['id'] for i in stable_flat]
    stable_p=p[stable_flat%npnode]
    stable_mass=np.array([tr['by'][g]['mass'] for g in stable_gid]);stable_dm=np.array([tr['by'][g].get('dm_dx',0.) for g in stable_gid])
    rates=[];event_yield=[];ys=[];ystat=[];workbounds=[];parent_energy=[];max_force_shift=0.;rows=[]
    for i,(h,f,fs) in enumerate(zip(history,fgrid,fgstat)):
        Tc,H,s=therm(Ns[i]);n=12*Tc**3/(2*math.pi**2)*W*f;pair=n[:,None]*n[None,:]
        rc=np.sum(KC[i]*pair[None,:,:],axis=(1,2));src=rc/(H*s)
        rates.append(src);event_yield.append(float(sum(src)));ys.append(2*float(sum(n))/s)
        nstat=12*Tc**3/(2*math.pi**2)*W*fs;ystat.append(2*float(sum(nstat))/s)
        workbounds.append(float(np.sum(KB[i]*pair))/(H*h['action']*omega))
        parent_energy.append(float(np.sum(parentmom[i]*pair)))
        rows.append(dict(N=float(Ns[i]),Tc=Tc,Y_charged=ys[-1],stationary_control_Y=ystat[-1],
             channel_event_yield_per_N={key:float(src[j]) for j,key in enumerate(gamma_keys)},
             physical_channel_event_rate_mu4={key:float(rc[j]) for j,key in enumerate(gamma_keys)},
             collision_energy_exchange_bound_over_field_energy_per_N=workbounds[-1],
             primary_parent_energy_mu4=parent_energy[-1]))
    rates=np.asarray(rates);ys=np.asarray(ys);ystat=np.asarray(ystat)
    # Trapezoid birth cohorts, with exact subsequent massive momentum redshift.
    # Cascade delay <small fraction of one e-fold is checked below; no daughter
    # is assigned radiation unless its actual mass is zero in this tree packet.
    cohorts=[]
    for j in range(len(Ns)-1):
        dn=Ns[j+1]-Ns[j];birth=(Ns[j+1]+Ns[j])/2
        count=(rates[j]+rates[j+1])/2*dn
        cohorts.append((birth,count@Tmat))
    nterminal_yield=np.zeros(len(stable));Efinal=0.;forcefinal=0.;Pfinal=0.;restfinal=0.
    Nend=Ns[-1];Tend,Hend,send=therm(Nend);xfinal=history[-1]['x_minimum'];mfinal=np.maximum(0,stable_mass+stable_dm*(xfinal-XPOLE))
    for birth,count in cohorts:
        redp=stable_p*np.exp(birth-Nend);E=np.sqrt(mfinal*mfinal+redp*redp)
        nterminal_yield+=count;Efinal+=float(count@E);restfinal+=float(count@mfinal)
        forcefinal+=float(count@(mfinal*stable_dm/np.maximum(E,1e-300)))
        Pfinal+=float(count@(redp*redp/(3*np.maximum(E,1e-300))))
    groups={}
    for gid in sorted(set(stable_gid)):
        mask=np.array([g==gid for g in stable_gid]);groups[gid]=dict(number_yield=float(nterminal_yield[mask].sum()),mass_mu=float(tr['by'][gid]['mass']),mass_slope_mu=float(tr['by'][gid].get('dm_dx',0.)))
    kfield=float(packet['local_profile']['radial_curvature_mu2']);forcephys=send*forcefinal
    initialY=float(ys[0]);depleted=float((initialY-ys[-1])/2);integratedevents=float(np.trapz(event_yield,Ns))
    neutral_injected=float(np.trapz(np.sum(rates,axis=1)*M,Ns));redshift_work=neutral_injected-Efinal
    checks=dict(ODE_success=bool(sol.success and control.success),positive=bool(np.all(fgrid>0)),
                carrier_identity=abs(integratedevents/depleted-1)<.01,
                terminal_energy=max(energyerr.values())<1e-9,
                terminal_positive=min(float(T.min()) for T in terminal.values())>-1e-10,
                tested_cosmic_delay=H0*max(delay.values())<.001,
                kernel_refinement=max(r['relative'] for r in refinements)<.03,
                actual_massive_storage=Efinal>=restfinal>=0 and redshift_work>=0,
                work_bound=max(workbounds)<1e-3)
    result=dict(claim_id='CC10_CHANGING_SCALAR_SHAPE_MASSIVE_CASCADE_STAGE',checks=checks,
        rows=rows,q_edges=edges.tolist(),initial_fS=f0.tolist(),final_fS=fgrid[-1].tolist(),stationary_final_fS=fgstat[-1].tolist(),
        final_Y_charged=float(ys[-1]),stationary_control_final_Y=float(ystat[-1]),initial_Y_charged=initialY,
        integrated_pair_event_yield=integratedevents,half_charged_yield_loss=depleted,
        neutral_terminal_group_yields=groups,neutral_final_energy_over_entropy_mu=Efinal,
        neutral_final_rest_energy_over_entropy_mu=restfinal,neutral_final_pressure_over_entropy_mu=Pfinal,
        neutral_final_force_mu3=forcephys,neutral_force_equilibrium_shift=abs(forcephys)/kfield,
        neutral_force_shift_over_recorded_amplitude=abs(forcephys)/(kfield*(history[-1]['x_outer']-history[-1]['x_inner'])/2),
        neutral_energy_injected_over_entropy_mu=neutral_injected,neutral_expansion_work_over_entropy_mu=redshift_work,
        cascade_max_terminal_delay_mu=delay,cascade_max_H_delay=H0*max(delay.values()),
        cascade_terminal_energy_relative_errors=energyerr,kernel_refinements=refinements,
        maximum_collision_work_bound_over_field_energy_per_N=max(workbounds),
        primary_parent_energy_fraction_of_recorded_oscillation=max(parent_energy[i]/(history[i]['action']*omega) for i in range(len(history))),
        scope='New evolving scalar momentum shape with occupation-independent periodic four-state kernel and actual neutral massive cascade terminal momentum cohorts. Recorded slow scalar orbit retained; inverse/quantum occupied medium and dynamic charged/dispersive matching omitted. Cascade eliminated only on tested cosmological scale, not within one orbit. Source-energy discrepancy/action covariance is bounded, not silently assigned to radiation. Not a self-consistent full-history abundance.',
        runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(out).write_text(json.dumps(serialize(result),indent=2)+'\n')
    Path(kout).write_text(json.dumps(dict(claim_id=result['claim_id'],N=Ns.tolist(),Tc=[x['Tc_over_mu'] for x in history],q_edges=edges.tolist(),K=Ks.tolist(),K_stationary=Kstat.tolist(),scope='Occupation-independent vacuum neutral-width Floquet kernels on recorded orbit, radial2/angular12; evolving shape must be contracted afresh.'),separators=(',',':'))+'\n')
    print(json.dumps({k:result[k] for k in ('checks','final_Y_charged','stationary_control_final_Y','cascade_max_H_delay','neutral_force_shift_over_recorded_amplitude','maximum_collision_work_bound_over_field_energy_per_N','runtime_seconds','peak_rss_bytes')}));assert all(checks.values()),checks

if __name__=='__main__':main(*sys.argv[1:])
