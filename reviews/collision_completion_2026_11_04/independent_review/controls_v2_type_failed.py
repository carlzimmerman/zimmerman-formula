"""Independent bounded CC10 algebra, Fourier, and normalization controls.

This reviews finite models. It does not evolve a cosmological history.
"""
import os, sys
sys.dont_write_bytecode = True
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"
import json, math, time, resource
from pathlib import Path
import numpy as np
from scipy.linalg import solve_banded

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "reviews/collision_completion_2026_11_04"
for part in ("statistics", "cascades", "integration", "memory", "neutral_loop"):
    sys.path.insert(0, str(BASE / part))
import quantum as qt
from quantum_v2 import event_sweep
from generic_orbit import GenericOrbit, T0
from vertices import VertexBackground
import response_api_v4 as mem
import loop


def quantum_controls():
    q, W = qt.make_grid(8)
    rows = []
    for x in (2., 5., 25.4000254000381):
        ev = qt.conversion_events(x, .004, q, W, angles=4)
        f = qt.equilibrium(ev, .007)
        fwd, rev, _, _ = ev.products(f)
        odd = np.log(f / (1 + ev.eta * f))
        affinity_direct = -np.asarray(ev.S.T @ odd).ravel()
        h = f * np.linspace(.8, 1.2, len(f))
        flux = ev.flux(h)
        entropy_gradient = np.log((1 + ev.eta * h) / h)
        dS_direct = float(entropy_gradient @ (ev.S @ flux))
        dS_events = float(flux @ ev.affinity(h))
        rows.append(dict(x=x, events=len(flux), energy=float(np.max(abs(ev.energy @ ev.S))),
                         equilibrium=float(np.sum(ev.coefficient * abs(fwd-rev)) / np.sum(ev.coefficient * (fwd+rev))),
                         affinity_error=float(np.max(abs(affinity_direct-ev.affinity(f)))),
                         entropy_direct=dS_direct, entropy_event=dS_events))
    ev = qt.ReactionEvents([[0,1,2,3,4]], [[1,.5,.5,.5,.5]], [.7], [1,2,3,4,5], [4,1,3,1,3], [-1,1,1,-1,-1])
    tests=[]
    for f in (np.array([.9,0.,0.,0.,0.]), np.array([0.,.8,.2,.7,.4]), np.array([.3,.8,.2,1.,1.])):
        before=qt.entropy(f, ev.measure, ev.eta)
        out,_=event_sweep(ev,f,1e7)
        tests.append(dict(min=float(out.min()), maxferm=float(out[ev.eta<0].max()),
                          energy_change=float(ev.energy @ (ev.measure*(out-f))),
                          entropy_change=qt.entropy(out,ev.measure,ev.eta)-before,
                          flux_initial=float(ev.flux(f)[0])))
    return dict(local=rows, stiff_boundary_events=tests)


def field_controls():
    bg=VertexBackground(BASE/'cascades/run_vertices001/result.json')
    nodes,weights=np.polynomial.legendre.leggauss(4);q=[];W=[]
    for lo,hi in zip([0.,.1,1.,5.,20.],[.1,1.,5.,20.,80.]):
        qq=(lo+hi)/2+(hi-lo)*nodes/2;q.extend(qq);W.extend((hi-lo)*weights*qq**2/2)
    q=np.asarray(q);W=np.asarray(W);model=GenericOrbit(bg,q,W,phase_nodes=24)
    Y,orb=model.initial(1e-35)
    dh=1e-4
    plus=model.orbit(0,Y*(1+dh),E=orb['E'])
    minus=model.orbit(0,Y*(1-dh),E=orb['E'])
    derivative=(plus['J']-minus['J'])/(2*dh)
    expected=-T0**3*float((orb['weights']@orb['gas']['energy'])@Y)/orb['omega']
    x=orb['xmid'];hx=1e-5
    gasder=(model.gas(x+hx,0,Y)['rho'][0]-model.gas(x-hx,0,Y)['rho'][0])/(2*hx)
    return dict(action_population_derivative=derivative, action_expected=expected,
                action_derivative_relative=abs(derivative/expected-1),
                gas_force_derivative_relative=abs(gasder/model.gas(x,0,Y)['force'][0]-1),
                kinetic_action_identity_relative=abs(float(orb['weights']@orb['kin2'])/(orb['omega']*orb['J'])-1))


def fourier_controls():
    late=json.loads((mem.PRIOR/'kinetics/run_hybrid_bw_001/result.json').read_text())['case']
    packet=json.loads((mem.PRIOR/'gravity_resonance/run_leading001/result.json').read_text())['packet']
    omega=math.sqrt(packet['local_profile']['radial_curvature_mu2']/62)
    rows=[]
    for idx in (0,40,79):
        h=late['history'][idx]; x=h['x_minimum']; Afield=(h['x_outer']-h['x_inner'])/2
        data=mem.cell_modes(x,Afield,omega,h['Tc_over_mu'],[0.,1.,3.,5.],radial=2,angular=4)
        j=len(data['delta'])//2; delta=data['delta'][j]; A=data['A'][j]; b=data['boost'][j]
        z=A/omega; K=max(64,math.ceil(abs(z)+40)); ns=np.arange(-K,K+1)
        coeff=[]
        for gamma,v in zip(mem.WIDTH,mem.COEFF):
            ab=np.zeros((3,len(ns)),complex)
            ab[1]=gamma*b/2+1j*(delta+ns*omega)
            ab[0,1:]=-1j*A/2; ab[2,:-1]=-1j*A/2
            rhs=np.zeros(len(ns),complex);rhs[K]=v
            coeff.append(solve_banded((1,1),ab,rhs))
        a=np.array(coeff)
        rate=float(np.sum(mem.WIDTH[:,None]*b*abs(a)**2))
        current=float(2*np.real(mem.COEFF.conj()@a[:,K]))
        coscurrent=float(np.real(mem.COEFF.conj()@(a[:,K-1]+a[:,K+1])))
        power=-A*coscurrent
        nmax=math.ceil(z+12+4*z**(1/3)); nn=np.arange(-nmax,nmax+1)
        rr=mem.jv(nn,z)[:,None]*mem.COEFF[None,:]/(mem.WIDTH[None,:]*b/2+1j*(delta+nn*omega)[:,None])
        rn=np.sum(mem.WIDTH[None,:]*b*abs(rr)**2,axis=1)
        f_rate=float(rn.sum()); f_power=float((nn*omega)@rn); f_ledger=float((delta+nn*omega)@rn)
        # This uses the original phase equation's Fourier amplitudes, rather than
        # the Bessel representation used by the production implementation.
        ledger=data['EN'][j]*rate-((data['EN'][j]-delta)*current+A*coscurrent)
        peak=mem.LAMBDA/(data['e1'][j]*data['e2'][j]*mem.M)*float(np.sum(abs(mem.COEFF)**2/mem.WIDTH))
        rows.append(dict(history_index=idx,K=K,z=z, rate_relative=abs(rate/f_rate-1),
                         source_exit_relative=abs(current/rate-1),
                         scalar_power_relative=abs(power-f_power)/max(abs(f_power),A*rate*1e-8),
                         ledger_relative_to_detuning=abs(ledger-f_ledger)/max(A*rate,1e-300),
                         tail_amplitude_relative=float(np.linalg.norm(a[:,[0,-1]])/np.linalg.norm(a)),
                         physical_sigma_v=float(data['pref'][j]*rate), mode_peak_bound=peak))
    # Independent at-rest spectral normalization using |kappa|^2_physical=2G.
    m=mem.M/2
    amplitude_squared=2*mem.LAMBDA
    spectral=amplitude_squared/(8*m*m*mem.M)*4*float(np.sum(abs(mem.COEFF)**2/mem.WIDTH))
    pinned=json.loads((mem.PRIOR/'microphysics/run_pole002/result.json').read_text())['sigma_pair_v_at_rest_mu_minus2']
    return dict(rows=rows, physical_real_Gram_factor=2,
                at_rest_spectral_sigma_v=spectral, pinned_pole_sigma_v=pinned,
                at_rest_normalization_relative=abs(spectral/pinned-1))


def separate_forms(t):
    if t >= .7:
        if t<=1: f=math.asin(math.sqrt(t))**2
        else:f=-.25*(math.log((1+math.sqrt(1-1/t))/(1-math.sqrt(1-1/t)))-1j*math.pi)**2
        return ((f-t)/t**2,2*(t+(t-1)*f)/t**2,-(2*t*t+3*t+3*(2*t-1)*f)/t**2,2*f/t)
    c=[0.]+[.5*4.**n/(n*n*math.comb(2*n,n)) for n in range(1,100)]
    a0=sum(c[n]*t**(n-2) for n in range(2,100))
    af=2*sum((c[n-1]-c[n])*t**(n-2) for n in range(2,100))
    av=-2-sum((6*c[n-1]-3*c[n])*t**(n-2) for n in range(2,100))
    ap=2*sum(c[n]*t**(n-1) for n in range(1,100))
    return a0,af,av,ap


def loop_controls():
    x=25.4000254000381;e=.003
    d,s,cube,yuk,K,qs,qf,qv,ms,mf,mv,physical,G,control,beta=loop.build(x,e)
    pinned=json.loads((BASE/'neutral_loop/run004/result.json').read_text())['cases'][2]
    rows=[]
    for name in ('S8_0','S3_0'):
        group=next(g for g in s['groups'] if g['id']==name); ext=group['indices'];M=group['mass']
        even=np.zeros((len(ext),12,12),complex);odd=even.copy()
        for mass,Q,V,kind in ((ms,qs,cube[ext],'scalar'),(mf,qf,yuk[:,:,ext].transpose(2,0,1),'fermion'),(mv,qv,K[ext],'vector')):
            products=[[ (Q[b]@Q[c]+Q[c]@Q[b])/2 for c in range(12)] for b in range(12)]
            for i,m in enumerate(mass):
                if m<1e-10 or (kind=='scalar' and not physical[i]): continue
                a0,af,av,ap=separate_forms(M*M/(4*m*m))
                # Explicit index sum, independent of the einsum implementation.
                for b in range(12):
                    for c in range(12):
                        P=products[b][c]
                        trace=np.sum(V[:,:,i]*P[i,:][None,:],axis=1)
                        if kind=='fermion':
                            tr=np.sum(V[:,:,i].real*P[i,:][None,:],axis=1)
                            ti=np.sum(V[:,:,i].imag*P[i,:][None,:],axis=1)
                            even[:,b,c]+=tr*af/(2*m);odd[:,b,c]+=ti*ap/(2*m)
                        else: even[:,b,c]+=trace*(a0 if kind=='scalar' else av)/(4*m*m)
        width=d['g']**4*M**3/(4096*math.pi**5)*float(np.sum(abs(even)**2+abs(odd)**2))/len(ext)
        ref=next(v for v in pinned['states'] if v['id']==name)['width']
        rows.append(dict(id=name,width=width,reference_width=ref,relative=abs(width/ref-1)))
    # Explicit transverse photon polarizations: amplitudes -2cM^2 for xx,yy.
    c=.7; M=1.3; sum_amp2=2*(2*c*M*M)**2
    identical=sum_amp2/(32*math.pi*M);mixed=sum_amp2/(16*math.pi*M)
    return dict(width_reconstruction=rows, scalar_photon_width_relative=abs(identical/(c*c*M**3/(4*math.pi))-1),
                mixed_over_identical=mixed/identical, beta=beta, model_controls=control)


def main(out):
    start=time.monotonic()
    result=dict(quantum=quantum_controls(),field=field_controls(),memory=fourier_controls(),loop=loop_controls())
    result['runtime_seconds']=time.monotonic()-start
    result['peak_rss_bytes_macos']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    checks=dict(quantum_energy=max(r['energy'] for r in result['quantum']['local'])<1e-12,
                quantum_detailed_balance=max(r['equilibrium'] for r in result['quantum']['local'])<1e-12,
                quantum_entropy=all(r['entropy_direct']>=0 and abs(r['entropy_direct']-r['entropy_event'])<1e-12 for r in result['quantum']['local']),
                quantum_boundaries=all(r['min']>=-1e-12 and r['maxferm']<=1+1e-12 and r['entropy_change']>=-1e-12 for r in result['quantum']['stiff_boundary_events']),
                field_derivatives=result['field']['action_derivative_relative']<.002 and result['field']['gas_force_derivative_relative']<1e-6,
                fourier_rate=max(r['rate_relative'] for r in result['memory']['rows'])<1e-8,
                fourier_work=max(r['scalar_power_relative'] for r in result['memory']['rows'])<1e-5,
                fourier_ledger=max(r['ledger_relative_to_detuning'] for r in result['memory']['rows'])<1e-5,
                memory_normalization=result['memory']['at_rest_normalization_relative']<1e-10,
                gauge_widths=max(r['relative'] for r in result['loop']['width_reconstruction'])<1e-7)
    result['checks']=checks
    Path(out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(checks=checks,runtime_seconds=result['runtime_seconds'],peak_rss_bytes_macos=result['peak_rss_bytes_macos'])))
    assert all(checks.values()),checks


if __name__=='__main__':main(sys.argv[1])
