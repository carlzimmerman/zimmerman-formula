import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import json,math,time,resource
from pathlib import Path
import mpmath as mp
import numpy as np
from scipy.optimize import minimize_scalar
from radial_metric import calculate as radial
ROOT=Path(__file__).resolve().parents[3];TP3=ROOT/'reviews/finite_matching_2026_11_01'
sys.path.insert(0,str(TP3/'gauge_diagrams'))
from full import calculate as vacuum
from current import calculate as angular
from pressure_scan import cw
mp.mp.dps=55

def main(path):
    start=time.monotonic();parent=json.load(open(TP3/'run_pressure/result.json'));cache={};out=[];leading=[]
    def raw(lx,e):
        key=(float(lx).hex(),e)
        if key not in cache:
            x=math.exp(float(lx));xr=7.367143721278508/math.sqrt(31*e);Q2=e/31+(e*xr)**2;g=math.sqrt(29/200)*e;v=vacuum(x,e,e,g,1.,Q2,True);c=angular(x,e,e,g,1.,Q2);r=radial(x,e,e,g,1.,Q2)
            cache[key]=dict(V=cw(mp.mpf(x),mp.mpf(e),mp.mpf(e),mp.sqrt(mp.mpf(29)/200)*mp.mpf(e))+mp.mpf(v['V2_reduced']),F=mp.mpf(v['F_tree']+v['deltaF_heavy']+c['total']),Ah=mp.mpf(v['deltaF_heavy']),Atree=mp.mpf(v['F_tree']),Ar=mp.mpf(r['total']),radial=r)
        return cache[key]
    def coeff(lx,e,h):
        pts=[raw(lx+j*h,e) for j in (-2,-1,0,1,2)];mid=pts[2];d1=lambda key:(pts[0][key]-8*pts[1][key]+8*pts[3][key]-pts[4][key])/(12*h);d2=lambda key:(-pts[0][key]+16*pts[1][key]-30*pts[2][key]+16*pts[3][key]-pts[4][key])/(12*h*h)
        return dict(A=mid['Atree']+mid['Ar']+d1('Ah')-mid['Ah'],F=mid['F'],Fs=d1('F'),Vss=d2('V'),Vs=d1('V'),Agraph=mid['Ar'],Aheavy=d1('Ah')-mid['Ah'],radial=mid['radial'])
    for e in (.01,.03):
        rec=next(r for r in parent['cases'] if r['e']==e and r['scheme']=='finite_matched' and r['interpolation_nodes']==29 and r['stencil_h']==.0025);lx0=math.log(rec['X_min']);vacrows=[];circular=[]
        for hh in (.005,.0025):
            h=mp.mpf(hh);c=coeff(lx0,e,h);A,F,Fs,Vss=c['A'],c['F'],c['Fs'],c['Vss'];m2=Vss/(2*A);m=mp.sqrt(m2);coupling=Fs/(2*F*mp.sqrt(2*A));width=coupling**2*m**3/(32*mp.pi);r=c['radial'];gap=min(x for x in (r['min_positive_scalar_m2'],r['min_positive_fermion_m2'],r['min_positive_vector_m2']) if x is not None)
            vacrows.append(dict(stencil_h=hh,A=float(A),F=float(F),A_graph=float(c['Agraph']),A_heavy=float(c['Aheavy']),m2=float(m2),m=float(m),v_phase=float(mp.sqrt(F)),g_sigma_phase=float(coupling),Gamma_phase=float(width),stationarity_log_displacement=float(abs(c['Vs']/Vss)),min_massive_loop_m2=gap,m2_over_min_massive=float(m2/gap),A_positive=bool(A>0),F_positive=bool(F>0)))
        for state in rec['samples'][2:4]:
            ratio=state['X_over_min'];c=coeff(lx0+math.log(ratio),e,mp.mpf('.0025'));A=float(c['A']);N=state['Omega_ss'];D=state['fixed_charge_D'];C=state['partial_susceptibility'];w=state['omega2'];vt=state['n']/(math.sqrt(w)*C);mass=N/(2*A);mix=(D-N)/(2*A);gap=D/(2*A)
            def lower(x,v=vt):
                S=(1+v)*x+1;prod=v*x*(x+mass/gap);disc=max(0,S*S-4*prod);return 2*prod/(S+math.sqrt(disc))
            row=dict(X_over_min=ratio,A=A,radial_mass_parameter2=mass,mixing2=mix,radial_phase_gap2=gap,vtheta2=vt,IR_cs2_from_dispersion=vt*N/D,IR_cs2_recorded=state['cs2_IR'],omega=math.sqrt(w))
            if N<0:
                cut=-mass/gap;opt=minimize_scalar(lambda t:lower(t),bounds=(0,cut),method='bounded',options={'xatol':1e-13});growth=math.sqrt(max(0,-opt.fun*gap));expected=abs(mass)/(2*math.sqrt(mix));opt1=minimize_scalar(lambda t:lower(t,1.),bounds=(0,cut),method='bounded',options={'xatol':1e-13});g1=math.sqrt(max(0,-opt1.fun*gap));row.update(k_cut=math.sqrt(-mass),k_peak=math.sqrt(opt.x*gap),Gamma_max=growth,Gamma_over_background_omega=growth/math.sqrt(w),v1_peak_control_error=abs(g1/expected-1),stable_grid=None)
            else:row.update(stable_grid=all(lower(x)>0 for x in np.geomspace(1e-8,1e4,100)),Gamma_max=0,k_cut=0,k_peak=0)
            rr=c['radial'];mm=min(x for x in (rr['min_positive_scalar_m2'],rr['min_positive_fermion_m2'],rr['min_positive_vector_m2']) if x is not None);row.update(min_massive_loop_m2=mm,omega2_over_min_massive=w/mm,kcut2_over_min_massive=row['k_cut']**2/mm,growth2_over_min_massive=row['Gamma_max']**2/mm);circular.append(row)
        # Leading weak expressions are analytic scaling of the exact one-loop shape,
        # not a new lower-e float spectral extrapolation.
        ee=mp.mpf(e);x0=mp.mpf('7.3671437212785083116194')/mp.sqrt(31*ee);g=mp.sqrt(mp.mpf(29)/200)*ee;u=lambda s:cw(x0*mp.exp(s),ee,ee,g);vss=mp.diff(u,0,2);vsss=mp.diff(u,0,3);A0=31*x0*x0;mass=mp.sqrt(vss/(2*A0));coupling=1/mp.sqrt(2*A0);gamma=coupling**2*mass**3/(32*mp.pi)
        leading.append(dict(e=e,m_over_e_3half=float(mass/ee**mp.mpf('1.5')),v_times_sqrt_e=float(mp.sqrt(A0*ee)),g_over_sqrt_e=float(coupling/mp.sqrt(ee)),Gamma_over_e_11half=float(gamma/ee**mp.mpf('5.5')),anharmonic_ratio_per_eta=float(vsss/vss-3)))
        out.append(dict(e=e,X_min=rec['X_min'],vacuum=vacrows,circular_states=circular,relative_mass_stencil_change=abs(vacrows[0]['m']/vacrows[1]['m']-1),relative_coupling_stencil_change=abs(vacrows[0]['g_sigma_phase']/vacrows[1]['g_sigma_phase']-1)))
    checks=dict(two_couplings=len(out)==2,positive_vacuum_metric=all(r['A_positive'] and r['F_positive'] for c in out for r in c['vacuum']),vacuum_stationarity_below_1e_5=all(r['stationarity_log_displacement']<1e-5 for c in out for r in c['vacuum']),metric_stencil_repeats=all(max(c['relative_mass_stencil_change'],c['relative_coupling_stencil_change'])<1e-4 for c in out),IR_matches_thermodynamic=all(abs(r['IR_cs2_from_dispersion']-r['IR_cs2_recorded'])<1e-10 for c in out for r in c['circular_states']),stable_positive_N_grid=all(c['circular_states'][0]['stable_grid'] for c in out),unstable_v1_peak_control=all(c['circular_states'][1]['v1_peak_control_error']<1e-8 for c in out),weak_scaling_constants_match=max(abs(leading[0][k]/leading[1][k]-1) for k in ('m_over_e_3half','v_times_sqrt_e','g_over_sqrt_e','Gamma_over_e_11half'))<1e-12)
    result=dict(claim_id='TP04_RADIAL_DYNAMICS',checks=checks,cases=out,leading_weak_constants=leading,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,non_claims=['Charged dispersion omits q-activated additional radial higherderivative matching','Vacuum pole is local fixed-gauge matched truncation, not gaugevariation/nonlocal proof','No scale,density,lifetime or halo selected'])
    Path(path).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
