"""Post-memory passive future charged floor, independently integrated RD tail."""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[k]='1'
import json,math,time,resource
from pathlib import Path
import numpy as np
from scipy.integrate import quad,solve_ivp
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/memory'))
from response_api_v4 import *

def actual_pair_average(width,args,f):
    d=mode_data(**args,f_number=f,radial=2,angular=12)
    gamma,V=np.linalg.eigh(width);coeff=V.T@VECTOR
    z=d['z'];nm=int(math.ceil(float(max(z))+12+4*float(max(z))**(1/3)))
    rate=0.;Jsum=np.zeros(len(z))
    for n in range(-nm,nm+1):
        j2=jv(n,z)**2;Jsum+=j2
        rr=coeff[None,:]/(gamma[None,:]*d['boost'][:,None]/2+1j*(d['delta']+n*args['omega'])[:,None])
        rate+=float(np.sum(d['w']*d['pref']*j2*d['boost']*np.sum(gamma[None,:]*abs(rr)**2,axis=1)))
    return dict(pair_sigma_v_mu_minus2=rate,weighted_Bessel_sum=float(d['w']@Jsum),
                omitted_number_fraction=d['omitted_number_fraction'],max_boost_error=float(max(1-d['boost'])))

def periodic_matrix_control(width,omega,xmid,amp,kind,seed):
    rng=np.random.default_rng(seed);size=float(np.linalg.norm(width,2))
    Hs=[]
    for k in range(3):
        r=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));Hs.append((r+r.conj().T)*size/4)
    A=2*charged_mass_derivative(xmid)*amp
    def operator(theta):
        if kind=='perfect_peak':return width/2
        m=float(charged_mass(xmid+amp*math.cos(theta)));beta=math.sqrt(max(0,1-4*m*m/M**2))
        incoming=144*G*beta/(32*math.pi*M)
        H=-A*math.cos(theta)*np.eye(4)
        if kind=='noncommuting':H=H+Hs[0]+Hs[1]*math.cos(theta)+Hs[2]*math.sin(theta)
        return (width+incoming)/2+1j*H
    def rhs(theta,y):
        K=y[:16].reshape(4,4);b=y[16:];L=operator(theta)/omega
        return np.r_[(-L@K).ravel(),-L@b+VECTOR]
    initial=np.r_[np.eye(4).ravel(),np.zeros(4)].astype(complex)
    fundamental=solve_ivp(rhs,[0,2*math.pi],initial,rtol=2e-11,atol=1e-13,max_step=.02)
    final=fundamental.y[:,-1];K=final[:16].reshape(4,4);b=final[16:]
    x0=np.linalg.solve(np.eye(4)-K,b)
    theta=np.linspace(0,2*math.pi,2049)
    orbit=solve_ivp(lambda th,x:-(operator(th)/omega)@x+VECTOR,[0,2*math.pi],x0,t_eval=theta,rtol=2e-11,atol=1e-13,max_step=.02)
    aa=orbit.y/omega
    hazard=np.einsum('at,ab,bt->t',aa.conj(),width,aa).real
    source=2*np.einsum('a,at->t',VECTOR,aa.real)
    rate=float(np.trapz(hazard,theta)/(2*math.pi));peak=4*float(VECTOR@np.linalg.solve(width,VECTOR))
    if kind=='perfect_peak':incoming_hazard=np.zeros(len(theta))
    else:
        betas=np.sqrt(np.maximum(0,1-4*charged_mass(xmid+amp*np.cos(theta))**2/M**2))
        incoming_hazard=144*betas/(32*math.pi*M)*np.einsum('at,ab,bt->t',aa.conj(),G,aa).real
    identity=float(np.trapz(hazard+incoming_hazard-source,theta)/(2*math.pi))/peak
    return dict(kind=kind,output_over_passive_peak=rate/peak,normalized_energy_identity_error=abs(identity),
                periodic_boundary_relative=float(np.linalg.norm(orbit.y[:,-1]-x0)/np.linalg.norm(x0)),ODE_success=bool(fundamental.success and orbit.success))

def main(out):
    start=time.monotonic();base=ROOT/'reviews/collision_completion_2026_11_04';old=ROOT/'reviews/coupled_trapping_2026_11_04'
    stage=json.loads((base/'memory/run_stage001/result.json').read_text());sm=json.loads((base/'memory/run_stage001/manifest.json').read_text())
    prior=json.loads((old/'kinetics/run_hybrid_bw_001/result.json').read_text())['case'];end=prior['history'][-1]
    packet=json.loads((old/'gravity_resonance/run_leading001/result.json').read_text())['packet']
    pole=json.loads((old/'microphysics/run_pole002/result.json').read_text());medium=json.loads((old/'microphysics/run_medium001/result.json').read_text())
    assert sm['run']['status']=='completed' and all(stage['checks'].values())
    Y=float(stage['final_Y_charged']);mu=float(prior['mu_GeV']);Tc=float(stage['rows'][-1]['Tc']);xi=.02;gs=106.75;Mbar=2.435e18
    Tend=Tc*mu/xi;s_end=2*math.pi**2/45*gs*Tend**3;H_end=math.sqrt(math.pi**2*gs/90)*Tend**2/Mbar
    omega=math.sqrt(float(packet['local_profile']['radial_curvature_mu2'])/62)
    recorded_H=end['H_over_oscillation']*omega*mu
    amp=(end['x_outer']-end['x_inner'])/2;center_offset=abs(end['x_minimum']-XPOLE)
    xmin=min(end['x_inner'],XPOLE-amp-center_offset);mmin=float(charged_mass(xmin));m0=M/2
    massfactor=m0*m0/(mmin*mmin)
    mass_average=quad(lambda u:math.exp(-u)*m0*m0/float(charged_mass(XPOLE-center_offset-amp*math.exp(-1.5*u)))**2,0,50,epsabs=1e-13,epsrel=1e-13)[0]+math.exp(-50)
    # Inherited legacy present-temperature constants are used only to show
    # the negligible finite-present versus infinite-RD-tail difference.
    Ttoday=2.3486541805581e-13;gs_today=3.909;a_today=Tend/Ttoday*(gs/gs_today)**(1/3)
    gate=.1*.44e-9/(float(pole['mC'])*mu);given_gate=5.680375574e-16
    gamma_models=[('vacuum',np.asarray(pole['Gamma_other_matrix_mu'])),('all_FFS_blocked',np.asarray(medium['Gamma_SSS_matrix_mu']))]
    f=np.asarray(stage['final_fS']);rows=[];future=[];controls=[]
    for label,width in gamma_models:
        peak=4*float(np.trace(G@np.linalg.inv(width)))/(M**3)
        sigma=peak*massfactor/(mu*mu);L_analytic=s_end*sigma/(2*H_end)
        L_scale=quad(lambda a:s_end*sigma/(2*H_end*a*a),1,np.inf,epsabs=.001,epsrel=2e-13)[0]
        L_log=quad(lambda u:s_end*sigma/(2*H_end)*math.exp(-u),0,50,epsabs=.001,epsrel=2e-13)[0]+L_analytic*math.exp(-50)
        coefficient=(2*math.pi**2/45*gs)*sigma*Mbar/(2*math.sqrt(math.pi**2*gs/90))
        L_temperature=quad(lambda T:coefficient,0,Tend,epsabs=.001,epsrel=2e-13)[0]
        L_shrinking=s_end*(peak/(mu*mu))/(2*H_end)*mass_average
        floor=1/(1/Y+L_analytic);floor_shrink=1/(1/Y+L_shrinking)
        invsqrt_ev,V=np.linalg.eigh(width);invsqrt=(V*(1/np.sqrt(invsqrt_ev))[None,:])@V.T
        beta=math.sqrt(max(0,1-4*mmin*mmin/M**2));Gin=144*G*beta/(32*math.pi*M)
        epsilon=float(np.linalg.eigvalsh(invsqrt@Gin@invsqrt).max())
        required=(1/gate-1/Y)/L_analytic
        rows.append(dict(width_choice=label,sigma_peak_mu_minus2=peak,mass_floor_corrected_peak_mu_minus2=peak*massfactor,
             sigma_max_GeV_minus2=sigma,future_loss_integral_upper=L_analytic,
             scale_factor_quadrature=L_scale,log_scale_quadrature=L_log,temperature_quadrature=L_temperature,
             finite_present_integral=L_analytic*(1-1/a_today),shrinking_amplitude_integral=L_shrinking,
             charged_future_yield_floor=floor,charged_future_floor_over_gate=floor/gate,
             shrinking_amplitude_yield_floor=floor_shrink,required_additional_peak_multiplier=required,
             local_charged_relative_form_bound=epsilon,
             local_charged_rate_ratio_interval=[max(0,1-epsilon)**2,(1+epsilon)**2],
             local_charged_scope='Additional positive local ΓC cannot raise the global passive peak, independent of this small-form bracket. Nonlocal/dispersive kernel not bounded.'))
        for scale in (1.,2.,10.,100.):
            args=dict(xmid=XPOLE+(end['x_minimum']-XPOLE)/scale**3,amplitude=amp/scale**1.5,omega=omega,Tc=Tc/scale,edges=stage['q_edges'])
            r=actual_pair_average(width,args,f)
            future.append(dict(width_choice=label,scale_factor_from_endpoint=scale,actual_frozen_shape_response=r,
                          ratio_to_nominal_peak=r['pair_sigma_v_mu_minus2']/peak))
        for j,kind in enumerate(('perfect_peak','physical_GammaC','noncommuting')):
            controls.append(dict(width_choice=label,**periodic_matrix_control(width,omega,end['x_minimum'],amp,kind,20261104+j)))
    checks=dict(completed_preferred_endpoint=sm['run']['status']=='completed',
        actual_temperature=Tend>99.999 and Tend<100.001,
        recorded_H_normalization=abs(recorded_H/H_end-1)<1e-6,
        charged_gate_matches=abs(gate/given_gate-1)<1e-9,
        endpoint_above_gate=Y>gate,
        positive_widths=all(np.linalg.eigvalsh(w).min()>0 for _,w in gamma_models),
        peak_inputs=abs(rows[0]['sigma_peak_mu_minus2']/pole['sigma_pair_v_at_rest_mu_minus2']-1)<1e-10 and abs(rows[1]['sigma_peak_mu_minus2']/medium['sigma_pair_v_all_FFS_blocked_uniform_bound_mu_minus2']-1)<1e-10,
        independent_tail_integrals=all(max(abs(r[k]/r['future_loss_integral_upper']-1) for k in ('scale_factor_quadrature','log_scale_quadrature','temperature_quadrature'))<1e-11 for r in rows),
        physical_future_response_bounded=all(r['ratio_to_nominal_peak']<=massfactor*(1+1e-10) for r in future),
        Bessel_normalization=all(abs(r['actual_frozen_shape_response']['weighted_Bessel_sum']-1)<1e-12 for r in future),
        full_matrix_passivity=all(r['ODE_success'] and r['output_over_passive_peak']<=1+1e-8 and r['normalized_energy_identity_error']<1e-5 and r['periodic_boundary_relative']<1e-7 for r in controls),
        both_future_floors_above_gate=all(r['charged_future_floor_over_gate']>1 for r in rows))
    result=dict(claim_id='CC10_POST_MEMORY_PASSIVE_FUTURE_ENVELOPE',checks={k:bool(v) for k,v in checks.items()},
        endpoint_Y_charged=Y,mu_GeV=mu,Tc_end_over_mu=Tc,T_SM_end_GeV=Tend,
        entropy_density_end_GeV3=s_end,H_RD_end_GeV=H_end,H_recorded_end_GeV=recorded_H,
        charged_10percent_gate=gate,given_gate=given_gate,endpoint_over_gate=Y/gate,
        charged_pole_mass_GeV=float(pole['mC'])*mu,orbit_amplitude_end=amp,center_offset_end=center_offset,
        assumed_future_mass_floor_mu=mmin,uniform_mass_prefactor=massfactor,
        shrinking_amplitude_integrated_mass_prefactor=mass_average,legacy_a_today=a_today,
        comparisons=rows,actual_future_response_controls=future,full_matrix_periodic_controls=controls,
        conclusion='Enhanced memory does not remove the charged failure in this specified conditional post-memory passive fixed-pole continuation, even granting every fermionic exit completely blocked and the maximal peak forever.',
        scope='Preferred evolving-fS endpoint, factorized symmetric pair ensemble, fixed G and declared positive neutral widths, retained cold-well mass envelope, constant-g radiation normalization. No additional pair-loss channels, new early history, active/inverse medium, entropy production or nonlocal/dispersive matching theorem.',
        runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(out).write_text(json.dumps(serialize(result),indent=2)+'\n');print(json.dumps({k:result[k] for k in ('checks','T_SM_end_GeV','entropy_density_end_GeV3','H_RD_end_GeV','endpoint_over_gate','uniform_mass_prefactor','comparisons','runtime_seconds','peak_rss_bytes')}));assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1])
