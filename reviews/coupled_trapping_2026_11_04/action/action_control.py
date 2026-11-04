"""Independent finite control of phase-selective collision action drift."""
import sys, os
sys.dont_write_bytecode = True
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[key] = '1'
import json, math, time, resource
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp


def run(beta, gamma, rtol):
    k, alpha, m0, n0, amp0 = 1., .7, 2., 1., .8
    omega0 = math.sqrt(k + alpha*n0)
    period0 = 2*math.pi/omega0
    end = 80*period0
    I0 = math.pi*omega0*amp0**2
    E0 = .5*(k+alpha*n0)*amp0**2 + n0*m0

    def full(t, y):
        x, v, n, rad = y
        loss = -gamma*n*(1+beta*x*x)
        eps = m0 + .5*alpha*x*x
        return [v, -(k+alpha*n)*x, loss, -eps*loss]

    def avg(t, y):
        n, action = y
        w = math.sqrt(k+alpha*n)
        A2 = action/(math.pi*w)
        nd = -gamma*n*(1+beta*A2/2)
        Id = -(2*math.pi/w)*gamma*n*alpha*beta*A2*A2/16
        return [nd, Id]

    def wrong(t, y):
        n, action = y
        w = math.sqrt(k+alpha*n)
        A2 = action/(math.pi*w)
        return [-gamma*n*(1+beta*A2/2), 0.]

    # Read endpoints at an exact microscopic turning point to suppress the
    # fast O(gamma/omega) phase error in comparing the two slow descriptions.
    def turning(t, y):
        return y[1]
    turning.direction = -1
    sol = solve_ivp(full, [0,end], [amp0,0,n0,0], rtol=rtol, atol=rtol*1e-3,
                    max_step=period0/35, dense_output=True, events=turning)
    endpoint = float(sol.t_events[0][-1])
    x,v,n,rad = sol.sol(endpoint)
    omega = math.sqrt(k+alpha*n)
    Ifull = math.pi*(v*v+omega*omega*x*x)/omega
    slow = solve_ivp(avg,[0,endpoint],[n0,I0],rtol=rtol,atol=rtol*1e-3)
    bad = solve_ivp(wrong,[0,endpoint],[n0,I0],rtol=rtol,atol=rtol*1e-3)
    yy=sol.sol(np.linspace(0,endpoint,4001))
    energy=.5*yy[1]**2+.5*(k+alpha*yy[2])*yy[0]**2+m0*yy[2]+yy[3]
    return dict(beta=beta,gamma=gamma,rtol=rtol,endpoint=endpoint,
                full_action=Ifull,averaged_action=float(slow.y[1,-1]),
                constant_action=float(bad.y[1,-1]),initial_action=I0,
                full_number=float(n),averaged_number=float(slow.y[0,-1]),
                relative_action_error=abs(Ifull/slow.y[1,-1]-1),
                relative_number_error=abs(n/slow.y[0,-1]-1),
                relative_energy_ledger_error=float(np.max(abs(energy/E0-1))),
                action_drift=float(Ifull-I0),
                constant_action_error=abs(Ifull/bad.y[1,-1]-1),
                minimum_sink_weight=float(min(1+beta*yy[0]**2)),
                success=bool(sol.success and slow.success and bad.success))


def main(output):
    start=time.monotonic()
    rows=[run(beta,gamma,rtol) for beta in (-.8,0.,.8)
          for gamma in (1e-4,2e-4) for rtol in (2e-9,2e-11)]
    checks=dict(integrations_completed=all(r['success'] for r in rows),
                nonnegative_sink=all(r['minimum_sink_weight']>0 for r in rows),
                energy_ledger=max(r['relative_energy_ledger_error'] for r in rows)<1e-6,
                action_average=max(r['relative_action_error'] for r in rows)<2e-5,
                number_average=max(r['relative_number_error'] for r in rows)<2e-5,
                action_sign=all(r['action_drift']*r['beta']<0 for r in rows if r['beta']),
                phase_independent_limit=max(abs(r['action_drift']/r['initial_action'])
                                           for r in rows if not r['beta'])<1e-6,
                missing_covariance_detected=all(r['constant_action_error']>
                    20*r['relative_action_error'] for r in rows if r['beta']))
    repeats=[]
    for beta in (-.8,0,.8):
        for gamma in (1e-4,2e-4):
            rr=[r for r in rows if r['beta']==beta and r['gamma']==gamma]
            repeats.append(abs(rr[0]['full_action']/rr[1]['full_action']-1))
    checks['tolerance_repeat']=max(repeats)<2e-6
    checks={key:bool(value) for key,value in checks.items()}
    result=dict(claim_id='CT09_ACTION_COVARIANCE_CONTROL',checks=checks,cases=rows,
                interpretation='Finite analytic oscillator control, not SU5 kinetics. Phase-selective depletion changes scalar action by a covariance term.',
                runtime_seconds=time.monotonic()-start,
                peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(checks=checks,runtime_seconds=result['runtime_seconds'],peak_rss_bytes=result['peak_rss_bytes'])))
    assert all(checks.values()), checks

if __name__=='__main__':
    main(sys.argv[1])
