"""Idealized controlled decoupling; no assertion that q(t) can be actuated."""
import json
import math
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
prior = json.loads((ROOT/'sol61_push/coherent_threshold_feedback_2026_10_13/run_verified/results.json').read_text())
cal = prior['calibration']
fstar, gamma, kappa, tau_star = (cal[k] for k in ['fstar','gamma_over_D0','kappa_over_D0','tau_star'])
D0 = cal['D0_eV']
checks = []


def check(name, condition):
    checks.append({'name':name,'passed':bool(condition)})
    assert condition, name


class Model:
    def __init__(self,n=4096,cutoff=120,L=5):
        dq=math.sqrt(cutoff)/n
        p=(np.arange(n)+.5)*dq
        self.e=p*p
        self.v=np.sqrt(gamma*math.exp(1/L)/(2*math.pi)*2*p*p*np.exp(-self.e/L)*dq)
        self.V=np.linalg.norm(self.v)
        self.u=self.v/self.V
        self.a=1+0j
        self.b=np.zeros(n,dtype=complex)
        self._dt=None

    def clone(self):
        other=object.__new__(Model)
        other.__dict__=self.__dict__.copy()
        other.b=self.b.copy()
        return other

    def data(self,q):
        weights=np.abs(self.b)**2
        B=float(weights.sum())
        K=float(self.e@weights)
        C=float(2*np.real(np.conj(self.a)*(self.v@self.b)))
        selfenergy=kappa*B*B/2
        return {'B':B,'kinetic':K,'coherence':C,'repulsion':selfenergy,
                'norm':abs(self.a)**2+B,'energy':abs(self.a)**2+K+selfenergy+q*C}

    def step(self,dt,q):
        if dt!=self._dt:
            self._dt=dt
            self._phase=np.exp(-.5j*self.e*dt)
            self._source=np.exp(-.5j*dt)
        B=float(np.vdot(self.b,self.b).real)
        self.a*=self._source
        self.b*=self._phase*np.exp(-.5j*kappa*B*dt)
        bright=self.u@self.b
        co,si=math.cos(q*self.V*dt),math.sin(q*self.V*dt)
        old_a=self.a
        self.a=co*old_a-1j*si*bright
        self.b+=self.u*((co-1)*bright-1j*si*old_a)
        B=float(np.vdot(self.b,self.b).real)
        self.a*=self._source
        self.b*=self._phase*np.exp(-.5j*kappa*B*dt)


def prepare(dt,n=4096,cutoff=120):
    model=Model(n,cutoff)
    count=math.ceil(tau_star/dt)
    actual_dt=tau_star/count
    for _ in range(count):
        model.step(actual_dt,1)
    return model


def ramp(prepared,duration,dt):
    model=prepared.clone()
    start=model.data(1)
    work=0.0
    max_residual=0.0
    if duration==0:
        work=-start['coherence']
        end=model.data(0)
        max_residual=abs(end['energy']-start['energy']-work)/fstar
    else:
        count=math.ceil(duration/dt)
        actual_dt=duration/count
        for j in range(count):
            q0=math.cos(math.pi*j/(2*count))**2
            qm=math.cos(math.pi*(j+.5)/(2*count))**2
            q1=math.cos(math.pi*(j+1)/(2*count))**2
            # Exact work of parameter jumps at fixed state; intervening
            # constant-q substeps do no external work.
            work+=(qm-q0)*model.data(q0)['coherence']
            model.step(actual_dt,qm)
            after=model.data(q1)
            work+=(q1-qm)*after['coherence']
            residual=abs(after['energy']-start['energy']-work)/fstar
            max_residual=max(max_residual,residual)
        end=model.data(0)
    B_before_hold=end['B']
    for _ in range(100):
        model.step(.1,0)
    held=model.data(0)
    check('decoupled population stationary '+str((duration,dt)),abs(held['B']/B_before_hold-1)<1e-11)
    check('norm '+str((duration,dt)),abs(held['norm']-1)<1e-10)
    check('work balance '+str((duration,dt)),max_residual<1e-4)
    return {'duration_tau':duration,'requested_dt':dt,'initial_B_over_fstar':start['B']/fstar,
            'final_B_over_fstar':end['B']/fstar,'retained_fraction_of_initial_B':end['B']/start['B'],
            'work_over_D0_fstar':work/fstar,
            'work_balance_max_error_over_D0_fstar':max_residual,
            'final_kinetic_over_D0_fstar':end['kinetic']/fstar,
            'final_repulsion_over_D0_fstar':end['repulsion']/fstar,
            'relative_pair_energy_if_isolated_dilution_eV':D0*(end['kinetic']+end['repulsion'])/end['B']}


prepared=prepare(.01)
start=prepared.data(1)
reference=prior['runs'][2]['rows'][100]['B_over_fstar']
check('preparation reproduces prior population',abs(start['B']/fstar-reference)<1e-6)
rows=[ramp(prepared,d,.01) for d in [0,.1,1,10,50]]
finer=prepare(.005)
fine_rows=[ramp(finer,d,.005) for d in [1,10,50]]
max_population_difference=max(abs(a['final_B_over_fstar']-b['final_B_over_fstar']) for a,b in zip(rows[2:],fine_rows))
max_work_difference=max(abs(a['work_over_D0_fstar']-b['work_over_D0_fstar']) for a,b in zip(rows[2:],fine_rows))
check('time refinement population',max_population_difference<2e-5)
check('time refinement switching work',max_work_difference<2e-5)
wide=ramp(prepare(.01,n=8192,cutoff=160),50,.01)
check('grid/cutoff refinement population',abs(wide['final_B_over_fstar']-rows[-1]['final_B_over_fstar'])<2e-5)
check('grid/cutoff refinement work',abs(wide['work_over_D0_fstar']-rows[-1]['work_over_D0_fstar'])<2e-5)

result={'all_pass':all(c['passed'] for c in checks),'checks':checks,'calibration':cal,
        'initial':start,'rows':rows,'fine_rows':fine_rows,'grid_refinement_row':wide,
        'max_time_refinement_population_difference':max_population_difference,
        'max_time_refinement_work_difference':max_work_difference,
        'non_claims':['q(t) is an extra imposed control, not supplied by the particle action',
                      'Decoupling source conversion leaves the repulsive interaction in place',
                      'Isolated dilution energy is conditional and excludes parent center-of-mass motion',
                      'No confinement, measured particles, lab-cold payload or physical apparatus demonstrated']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'all_pass':result['all_pass'],'checks':len(checks),'rows':rows,
                  'time_refinement_population':max_population_difference,'time_refinement_work':max_work_difference}))
