"""Evaluate the unmodified action equation at recorded leading final states."""
import sys
sys.dont_write_bytecode=True
import json, math, time, resource
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'reviews/coupled_trapping_2026_11_04'
sys.path.insert(0,str(BASE/'kinetics'))
from accurate import Accurate, LocalPotential
from two_species import PREF

def main(out):
    start=time.monotonic();rows=[]
    point=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal_kinetic/run_stationary_002/result.json').read_text())['points'][1]
    spin=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal/run_static_001/result.json').read_text())['points'][1]['spins'][0]
    packet=json.loads((BASE/'gravity_resonance/run_leading001/result.json').read_text())['packet'];r=packet['global_profile']
    point=dict(point,grid=r['grid'],T0_potential_mu4=r['V0_origin_subtracted_mu4'],origin_force=r['origin_force'],origin_curvature=r['origin_curvature'],mu_GeV=packet['mu_GeV'])
    for name in ('run_leading_two_001','run_leading_fine_001'):
        run=json.loads((BASE/'kinetics'/name/'result.json').read_text())['case'];bins=run['bulk_bins'];h=run['history'][-1]
        model=Accurate(point,spin,bins=bins,orbitn=16,absorbing=True);model.v=LocalPotential(model.v,packet['local_profile']);model.grid=np.unique(np.r_[0,np.linspace(.001,10,100),np.linspace(10,40,180)]);model.setup()
        f=np.r_[run['final_f_F'],run['final_f_S_number_normalization']];u=f*np.tile(model.W,2)/model.norm
        orb=model.orbital(h['N'],f,J=h['action']);w=orb['weights'];t=orb['t'];Bs=[]
        for x in orb['xs']:
            B,_=model.conversion(float(x),t)
            B-=np.diag(np.r_[model.kernel(float(x),t)@f[:model.n]/(t**3*model.W),model.scalar_kernel(float(x),t)@f[model.n:]/(t**3*model.W)])
            Bs.append(B)
        Bs=np.array(Bs);Bavg=np.einsum('k,kij->ij',w,Bs);cu=np.einsum('kij,j->ki',Bs,u);cavg=Bavg@u;eavg=w@orb['en'];ecavg=w@(orb['en']*cu)
        cov=PREF*t**3*model.norm*float(sum(ecavg-eavg*cavg));term=orb['period']/(2*math.pi*model.H(h['N'])*h['action'])*cov
        logJ=math.log(h['action']/model.J0);raw=-3+term;used=max(-3,raw) if logJ<-20 else raw
        rows.append(dict(run=name,logJ=logJ,collision_action_covariance_term=term,raw_dlogJ_dN=raw,implemented_dlogJ_dN=used,clamp_active=bool(raw!=used),period=orb['period']))
    result=dict(assertion_tested='At recorded finalf and J, compare derived actioncovariance equation to low-action clamp in unmodified implementation.',cases=rows,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Two finalstates only. No newtrajectory or repair. Doesnotquantify integratedhistorydifference.')
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

if __name__=='__main__':main(sys.argv[1])
