"""Necessary capture-work/supply and exact circular-orbit response tests.

Prescribed final cold profiles, not a coherent-field capture simulation.
"""
import json, math, hashlib, time, resource
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import cumulative_trapezoid, solve_ivp
from scipy.optimize import brentq
import survey as s

HERE=s.HERE;ROOT=s.ROOT;G=s.G
def main():
    start=time.time();survey=json.loads((HERE/'survey_results.json').read_text())
    prevpath=ROOT/'sol61_push/cold_data_constraints_2026_10_24/results.json'
    pins=[Path(__file__),HERE/'CONTRACT.md',HERE/'survey_results.json',HERE/'survey_receipt.json',prevpath]
    before={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in pins}
    prev=json.loads(prevpath.read_text());models=[];response=[];hidden_envelopes=[]
    sext=min((r for r in survey['continuous_best'] if r['footing']=='canonical' and r['beta']==0 and r['tracer_taper_pc'] is None),key=lambda r:r['nll'])
    for name in ['Draco','Sextans','Fornax','Leo I']:
        gal=prev['galaxies'][name];a=float(gal['observations']['rhalf_sph_physical'])
        p=gal['populations'][0];ms=p['stellar_mass'];mf=p['formed_mass']
        if name=='Sextans':
            ms=survey['stellar_mass'];mf=ms/.59 # explicit approximate surviving fraction sensitivity
            b=sext['cold_scale_pc'];mc=sext['cold_mass'];radii=survey['tracer_scales_pc']
        else:
            b=a;radii=[a];extra=gal['moments']['canonical'][0]['residual_variance']
            mc=extra*32*a/(math.pi*G) # same-scale cold Plummer exact kernel
        # Optimistic supply identity at Rc=5.364; no measured initial catchment.
        Bmin=max(ms,mc/5.364) # formed mass can exceed the initial reservoir through recycling
        dk=1/math.sqrt(b*b+a*a)-1/math.sqrt(b*b+(5*a)**2)
        required={str(v):v*v/(2*G*dk) for v in [5,10,20,30]}
        models.append(dict(name=name,stellar_mass=ms,formed_mass=mf,cold_mass=mc,cold_scale_pc=b,
            min_initial_baryons=Bmin,min_initial_baryons_over_formed=Bmin/mf,
            gas_mass_for_optimally_timed_contraction_capture=required,
            max_infinity_speed_at_min_reservoir=math.sqrt(2*G*Bmin*dk),
            cold_retention_needed_if_initial_baryons_200_times_formed=mc/(5.364*200*mf),
            cold_retention_needed_if_initial_baryons_10_times_formed=mc/(5.364*10*mf)))
        # Equal capture need not mean equal central mass. Diagnose the envelope
        # size needed to hide a common supply normalization from the global moment.
        # These constructed profiles are not formation predictions or stable states.
        if name!='Sextans':
            xx,ww=leggauss(256);theta=(xx+1)*math.pi/4;ww*=math.pi/4
            def coldvar(bb,mm):
                I=np.sum(ww*3*np.sin(theta)**2*np.cos(theta)/(1+(bb/a)**2*np.tan(theta)**2)**1.5)
                return G*mm/(3*a)*I
            supply=5.364*.5*200*mf
            b_hide=brentq(lambda bb:coldvar(bb,supply)-extra,.01,1e6)
            hidden_envelopes.append(dict(name=name,common_initial_baryons_per_formed=200.,common_cold_retention=.5,
                total_cold_mass=supply,required_Plummer_scale_pc=b_hide,
                cold_inside_stellar_projected_half_light_radius=supply*a**3/(a*a+b_hide*b_hide)**1.5,
                warning='single global moment construction only; radial data, tides, distribution function and assembly untested'))
        # Sources of baryonic potential; field cold and tracer stars remain distinct.
        components=[(ms/len(radii),ar) for ar in radii]
        # Cold field is neutral under Xi. Its marginal centrifugal diagnostic
        # must use the Newtonian stellar+cold potential, not the stellar force law.
        phi_cold_at_core=-G*mc/math.sqrt(a*a+b*b)-sum(G*m/math.sqrt(a*a+ar*ar) for m,ar in components)
        jcrit=a*math.sqrt(-2*phi_cold_at_core)
        models[-1].update(core_radius_for_barrier_pc=a,marginal_specific_angular_momentum_barrier_pc_kms=jcrit,
            maximum_impact_parameter_at_vinf10_pc=jcrit/10,
            angular_condition='eta^2*l*(l+1) < -2*r_core^2*Phi_Newtonian(r_core); spherical source growth supplies no torque')
        # Final virial energy of the target Plummer cold density in the remaining
        # Newtonian stellar potential. These are positive-energy field-wave fluxes,
        # not assumed colliding particles. Gas has left in this reference budget.
        xq,wq=leggauss(256);tq=(xq+1)*math.pi/4;wq*=math.pi/4
        rq=b*np.tan(tq);dmq=3*np.sin(tq)**2*np.cos(tq)*wq
        Ustar=sum(float(np.sum(dmq*(-G*m/np.sqrt(rq*rq+ar*ar)))) for m,ar in components)
        Wstar=sum(float(np.sum(dmq*G*m*rq*rq/(rq*rq+ar*ar)**1.5)) for m,ar in components)
        bound_specific=-3*math.pi*G*mc/(64*b)+Ustar+.5*Wstar
        qmax=5.364*200*mf/mc-1
        budgets=[]
        for vin in [5.,10.,20.]:
            ein=.5*vin*vin
            for vout in [20.,30.,50.]:
                eout=.5*vout*vout
                qneed=(ein-bound_specific)/(eout-ein) if eout>ein else None
                budgets.append(dict(v_infinity=vin,v_out_infinity=vout,escaped_over_final_mass=qneed,
                    initial_cold_mass=None if qneed is None else mc*(1+qneed),
                    fits_200_times_formed_supply=qneed is not None and qneed<=qmax))
        models[-1].update(final_cold_virial_energy_per_mass=bound_specific,
            max_escaped_over_final_mass_from_200_times_formed_supply=qmax,
            no_net_external_work_wave_energy_budget=budgets,
            minimum_outgoing_speed_for_vinf10_at_full_supply=math.sqrt(2*(50+(50-bound_specific)/qmax)) if qmax>0 else None)
        def gb(r):
            gn=sum(G*m*r/(r*r+ar*ar)**1.5 for m,ar in components)
            return .5*(gn+np.sqrt(gn*gn+4*s.A0['canonical']*gn))
        def gc(r):return G*mc*r/(r*r+b*b)**1.5
        grid=np.geomspace(.001,1e7,32768)
        pot=cumulative_trapezoid(gb(grid),grid,initial=0.)
        phi0=lambda r:np.interp(np.log(r),np.log(grid),pot)
        phic=lambda r:-G*mc/np.sqrt(r*r+b*b)
        for ar in radii:
            # Deterministic stationary tangential ensemble, bounded to r<6a.
            n=128;umax=6**3/(1+6**2)**1.5
            u=(np.arange(n)+.5)/n*umax;r0=ar/np.sqrt(u**(-2/3)-1)
            ell2=r0**3*gb(r0)
            rad_ad=np.array([brentq(lambda r:r**3*(gb(r)+gc(r))-ll,rr*1e-4,rr) for rr,ll in zip(r0,ell2)])
            tc=math.sqrt(ar/float(gb(ar))) # pc/(km/s)
            def ode(t,y):
                r=y[:n];vr=y[n:]
                return np.r_[vr,ell2/r**3-gb(r)-gc(r)]
            t_eval=np.linspace(0,40*tc,401)
            sol=solve_ivp(ode,[0,40*tc],np.r_[r0,np.zeros(n)],method='DOP853',rtol=1e-8,atol=1e-9,t_eval=t_eval)
            assert sol.success and np.min(sol.y[:n])>0
            r=sol.y[:n];vr=sol.y[n:];speed2=vr*vr+ell2[:,None]/r**2
            E=.5*speed2+phi0(r)+phic(r)
            E0=.5*ell2/r0**2+phi0(r0)+phic(r0)
            Escale=ell2/r0**2+abs(phic(r0))
            drift=float(np.max(abs(E-E0[:,None])/Escale[:,None]))
            assert drift<1e-4
            response.append(dict(name=name,tracer_scale_pc=ar,initial_tangential_equilibrium=True,
                tracers=n,stellar_orbit_time_proxy_Myr=tc*.977792,
                adiabatic_median_radius_ratio=float(np.median(rad_ad)/np.median(r0)),
                adiabatic_variance_trace_ratio=float(np.mean(ell2/rad_ad**2)/np.mean(ell2/r0**2)),
                impulsive_late_median_radius_ratio=float(np.median(np.median(r[:,201:],axis=0))/np.median(r0)),
                impulsive_late_variance_trace_ratio=float(np.mean(speed2[:,201:])/np.mean(ell2/r0**2)),
                max_post_impulse_energy_drift=drift,
                impulse_work_per_stellar_mass=float(np.mean(phic(r0))),
                cold_growth_is_prescribed_not_captured=True))
    out=dict(scope='necessary supply/capture-work inequalities and counterfactual circular stellar response; not demonstrated cold capture',
        models=models,stellar_response=response,equal_capture_hidden_envelope_diagnostic=hidden_envelopes,
        equations={'supply':'Mc <= Rc fc Mb_initial; Rc assumed 5.364',
            'capture':'v_inf^2/2 <= G Mg [1/sqrt(r^2+ag_in^2)-1/sqrt(r^2+ag_out^2)]',
            'field_work':'dEc/dt = integral rho_c partial_t Phi_b dV, plus boundary flux; cold self-field energy included once',
            'adiabatic_circular':'r_i^3 g_i(r_i)=r_f^3 g_f(r_f)',
            'post_growth_star_energy':'vr^2/2+L^2/(2r^2)+Phi_b,law(r)+Phi_c(r) conserved'})
    (HERE/'capture_results.json').write_text(json.dumps(out,indent=2)+'\n')
    after={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in pins}
    assert before==after
    receipt=dict(seconds=time.time()-start,peak_RSS_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        hashes=after,input_hashes_before=before,input_hashes_after=after,
        result_hash=hashlib.sha256((HERE/'capture_results.json').read_bytes()).hexdigest())
    (HERE/'capture_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
