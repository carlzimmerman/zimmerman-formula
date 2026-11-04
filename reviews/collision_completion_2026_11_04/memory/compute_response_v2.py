"""Finite CC10 recorded-orbit continuum Floquet calculation and controls."""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[k]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
from scipy.integrate import solve_ivp
from response_api_v2 import *

def snapshots():
    early=json.loads((PRIOR/'kinetics/run_leading_two_001/result.json').read_text())['case']
    late=json.loads((PRIOR/'kinetics/run_hybrid_bw_001/result.json').read_text())['case']
    packet=json.loads((PRIOR/'gravity_resonance/run_leading001/result.json').read_text())['packet']
    k=float(packet['local_profile']['radial_curvature_mu2']);omega=math.sqrt(k/62)
    f0=np.asarray(early['final_f_S_number_normalization']);f1=np.asarray(late['final_f_S_number_normalization'])
    rows=[]
    for index in (0,20,40,60,79):
        h=late['history'][index];frac=(h['N']-late['initial_N'])/(late['final_N']-late['initial_N'])
        f=np.exp((1-frac)*np.log(f0)+frac*np.log(f1))
        if index==0:f=f0
        if index==79:f=f1
        rows.append(dict(Tc=h['Tc_over_mu'],xmid=h['x_minimum'],amplitude=(h['x_outer']-h['x_inner'])/2,
                         omega=omega,edges=late['q_edges'],f_number=f,
                         distribution='recorded endpoint' if index in (0,79) else 'log-interpolated endpoint shape, not recorded',
                         history_index=index,N=h['N']))
    return rows

def exact_static_control(snap,radial=3,angular=12,phases=1024):
    d=mode_data(**{k:snap[k] for k in ('xmid','amplitude','omega','Tc','edges','f_number')},radial=radial,angular=angular)
    born=0.;full=0.;linerr=0.;maxincoming=0.
    for th in 2*math.pi*np.arange(phases)/phases:
        x=snap['xmid']+snap['amplitude']*math.cos(th)
        m=float(charged_mass(x));p1=d['p1'];p2=d['p2'];c=d['cosine'];w=d['w']
        e1=np.sqrt(m*m+p1*p1);e2=np.sqrt(m*m+p2*p2)
        ss=2*m*m+2*(e1*e2-p1*p2*c);ds=ss-M*M
        beta=np.sqrt(np.maximum(0,1-4*m*m/ss));aa=144*beta/(32*math.pi*np.sqrt(ss))
        z=np.sum(abs(COEFF)[None,:]**2/(ds[:,None]+1j*M*WIDTH),axis=1)
        b=np.sum(abs(COEFF)[None,:]**2*WIDTH/(ds[:,None]**2+(M*WIDTH)**2),axis=1)
        sig=np.sqrt(ss)/(e1*e2)*LAMBDA*b
        factor=abs(1+1j*M*aa*LAMBDA*z)**2
        born+=float(w@sig)/phases;full+=float(w@(sig/factor))/phases
        maxincoming=max(maxincoming,float(max(aa*LAMBDA)/min(WIDTH)))
        ep=np.sqrt(M*M+p1*p1+p2*p2+2*p1*p2*c)
        exact=((M-2*m)*(M+2*m)+p1*p1+p2*p2+2*p1*p2*c)/(ep+2*m)-p1*p1/(e1+m)-p2*p2/(e2+m)
        linear=d['delta']-d['A']*math.cos(th)
        linerr=max(linerr,float(max(abs(exact-linear)))/min(WIDTH))
    return dict(exact_s_Born=born,exact_s_resummed_incoming=full,
                stationary_incoming_width_multiplier=full/born,
                linear_detuning_error_over_min_width=linerr,
                maximum_incoming_eigenvalue_over_min_neutral_width=maxincoming)

def dephasing(snap,radial=4,angular=16):
    d=mode_data(**{k:snap[k] for k in ('xmid','amplitude','omega','Tc','edges','f_number')},radial=radial,angular=angular)
    period=2*math.pi/snap['omega'];lags=np.linspace(0,5*period,301)
    delta=d['delta'];w=d['w'];mean=float(w@delta);var=float(w@((delta-mean)**2))
    C=np.asarray([w@np.exp(-1j*(delta-mean)*t) for t in lags])
    crossings=np.flatnonzero(abs(C)<math.exp(-1))
    return dict(lag_over_period=(lags/period).tolist(),abs_C=abs(C).tolist(),
                rms_detuning_mu=math.sqrt(var),rms_dephasing_time_over_period=1/(math.sqrt(var)*period),
                first_below_exp_minus_one_over_period=None if not len(crossings) else float(lags[crossings[0]]/period),
                C_at_one_period=float(abs(C[60])),C_at_five_periods=float(abs(C[-1])))

def ode_control(snap):
    # Actual production vector/widths and an actual occupied cell pair.
    m=float(charged_mass(snap['xmid']));dm=charged_mass_derivative(snap['xmid']);q1=2.517216215372447;q2=3.321558463429335;c=.3
    p1=snap['Tc']*q1;p2=snap['Tc']*q2;e1=math.sqrt(m*m+p1*p1);e2=math.sqrt(m*m+p2*p2)
    ep=math.sqrt(M*M+p1*p1+p2*p2+2*p1*p2*c)
    delta=((M-2*m)*(M+2*m)+p1*p1+p2*p2+2*p1*p2*c)/(ep+2*m)-p1*p1/(e1+m)-p2*p2/(e2+m)
    omega=snap['omega'];a=snap['amplitude']*m*dm*(1/e1+1/e2);boost=M/ep
    nmax=int(math.ceil(a/omega+12+4*(a/omega)**(1/3)));ns=np.arange(-nmax,nmax+1)
    b=jv(ns,a/omega)[:,None]*COEFF[None,:]/(WIDTH[None,:]*boost/2+1j*(delta+ns*omega)[:,None])
    target=float(np.sum(abs(b)**2*WIDTH[None,:]*boost))
    # theta-scaled amplitudes omega*a_phys; 30 periods erase initial empty-parent transient.
    def rhs(th,y):return -(WIDTH*boost/(2*omega)+1j*(delta/omega-a/omega*math.cos(th)))*y+COEFF
    th=np.linspace(0,64*math.pi,8193)
    sol=solve_ivp(rhs,[0,64*math.pi],np.zeros(4,complex),t_eval=th,rtol=2e-9,atol=1e-11,max_step=.025)
    cut=th>=60*math.pi;rate=(abs(sol.y[:,cut])**2*WIDTH[:,None]*boost).sum(axis=0)/omega**2
    measured=float(np.trapz(rate,th[cut])/(4*math.pi))
    return dict(success=bool(sol.success),Floquet=target,ODE_last_two_periods=measured,
                relative_difference=abs(measured/target-1),sample_pair_q=[q1,q2],cosine=c,
                transient_periods=30,integrated_periods=32)

def main(out):
    start=time.monotonic();snaps=snapshots();rows=[]
    channels=json.loads((ROOT/'reviews/collision_completion_2026_11_04/cascades/run_basis002/result.json').read_text())['Gamma_by_daughter_pair_CT09_mu']
    for s in snaps:
        args={k:s[k] for k in ('xmid','amplitude','omega','Tc','edges','f_number')}
        r=orbit_response(**args,radial=3,angular=12,phase_nodes=256)
        row={k:v for k,v in s.items() if k not in ('edges','f_number')};row['response']=r
        row['continuum']=dephasing(s,3,12)
        row['channel_exits_mu_minus2']={key:float(np.trace(np.asarray(g)@r['rho_pair']).real) for key,g in channels.items()}
        row['channel_exit_sum_relative']=abs(sum(row['channel_exits_mu_minus2'].values())/float(np.trace(GAMMA@r['rho_pair']).real)-1)
        if s['history_index'] in (0,79):
            fine=orbit_response(**args,radial=5,angular=20,phase_nodes=768)
            row['fine_response']=fine
            row['refinement_dynamic_relative']=abs(r['dynamic_pair_sigma_v']/fine['dynamic_pair_sigma_v']-1)
            row['refinement_static_relative']=abs(r['stationary_pair_sigma_v']/fine['stationary_pair_sigma_v']-1)
            row['static_control']=exact_static_control(s)
            row['analytic_vs_exact_s_Born_relative']=abs(r['stationary_pair_sigma_v']/row['static_control']['exact_s_Born']-1)
            row['ode_control']=ode_control(s)
        rows.append(row)
    rho=np.outer(VECTOR,VECTOR);dt=1e9;final,exitcount=parent_decay_step(rho,dt)
    expected=expm(-GAMMA*dt/2)@rho@expm(-GAMMA*dt/2)
    bound=4*float(np.trace(G@np.linalg.inv(GAMMA)))/(M**3)
    checks=dict(rank_one_production=float(np.linalg.norm(G-LAMBDA*np.outer(VECTOR,VECTOR))/np.linalg.norm(G))<1e-12,
                PSD_parent=all(r['response']['rho_min_eigenvalue']>-1e-6 for r in rows),
                channel_sum=all(r['channel_exit_sum_relative']<1e-12 for r in rows),
                radial_angular_repeat=all(r.get('refinement_dynamic_relative',0)<.03 and r.get('refinement_static_relative',0)<.03 for r in rows),
                fullmatrix_ODE=all(r.get('ode_control',{}).get('relative_difference',0)<.001 for r in rows),
                linear_detuning=all(r.get('static_control',{}).get('linear_detuning_error_over_min_width',0)<.001 for r in rows),
                stationary_s_normalization=all(r.get('analytic_vs_exact_s_Born_relative',0)<.01 for r in rows),
                positive_decay=np.linalg.eigvalsh(final).min()>-1e-14 and exitcount>=0,
                decay_identity=abs(exitcount+float(np.trace(final).real)-1)<1e-12,
                direct_decay_match=float(np.linalg.norm(final-expected))<1e-14,
                passive_gain_bound=all(r['response']['dynamic_pair_sigma_v']<bound*(1+1e-4) for r in rows))
    result=dict(claim_id='CC10_FOUR_STATE_CONTINUUM_FLOQUET_MEMORY',checks={k:bool(v) for k,v in checks.items()},
                assertion_tested='Actual fixed-tree 4-state neutral response to factorized occupied charged continuum, on five saved harmonic late orbits; endpoints use recorded distributions, interiors interpolate endpoint shapes.',
                rows=rows,passive_peak_pair_sigma_bound=bound,
                decay_control=dict(dt=dt,remaining=float(np.trace(final).real),exits=exitcount),
                runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                scope='Leading dilute source, vacuum Γother, linearized actual harmonic orbit. Dynamic charged retarded self-energy omitted; stationary incoming correction quantified. No thermal matching or full occupied cascade/history claim.')
    Path(out).write_text(json.dumps(serialize(result),indent=2)+'\n')
    print(json.dumps(dict(checks=result['checks'],runtime_seconds=result['runtime_seconds'],peak_rss_bytes=result['peak_rss_bytes'],summary=[dict(Tc=r['Tc'],multiplier=r['response']['multiplier'],dynamic=r['response']['dynamic_pair_sigma_v'],static=r['response']['stationary_pair_sigma_v'],C_at_one_period=r['continuum']['C_at_one_period']) for r in rows])))
    assert all(checks.values()), checks

if __name__=='__main__':main(sys.argv[1])
