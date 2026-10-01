from pathlib import Path
import difflib,hashlib,json
p=Path(__file__).resolve().parent;src=p.parent/'kick_moments/engine_exact.py';old=src.read_text();s=old.replace('from exact_moments import kick_moments','from exact_moments import kick_moments\nfrom event_step import localize')
s=s.replace('fgal=None, trigger_cadence=5):','fgal=None, trigger_cadence=1, event_tol=1e-6, max_steps=100000, time_budget=60., late_events=False):')
s=s.replace('    rng = np.random.default_rng(seed)','    if cooling: raise ValueError("Bounded event benchmark implements no-cooling only")\n    if trigger_cadence != 1: raise ValueError("Event benchmark evaluates trigger every accepted step")\n    rng = np.random.default_rng(seed)')
s=s.replace('    T0 = time.time()','    T0 = time.time()\n    events = []\n    initial_mass = float(M.sum())')
needle='    Menc, phi, ids = enclosed()\n    A = accel(Menc)\n    while t < t0:'
insert='''    def pressure():
        dk = np.where(alive & ((kind == 0) | (kind == 2)))[0]
        order = np.argsort(R[dk]); ii = dk[order]
        rs=R[ii];ms=M[ii];vs=V[ii];vt2=(J[ii]/rs)**2;n=len(ii)
        cm=np.r_[0.,np.cumsum(ms)];cmv=np.r_[0.,np.cumsum(ms*vs)]
        cmv2=np.r_[0.,np.cumsum(ms*(vs**2+vt2))]
        lo=np.clip(np.arange(n)-nb,0,n-1);hi=np.clip(np.arange(n)+nb,0,n-1)
        mm=cm[hi+1]-cm[lo];mv=cmv[hi+1]-cmv[lo];mv2=cmv2[hi+1]-cmv2[lo]
        vol=4*math.pi/3*np.maximum(rs[hi]**3-rs[lo]**3,1e-9)
        out=np.zeros(N);out[ii]=(mv2-mv**2/np.maximum(mm,1e-30))/(3*vol)
        return out

    Menc, phi, ids = enclosed()
    A = accel(Menc)
    while t < t0:
        if nstep>=max_steps or time.time()-T0>time_budget:
            raise RuntimeError(f'event integration budget exhausted: steps={nstep}, events={len(events)}, a={float(a_of_t(t))}')
'''
assert needle in s;s=s.replace(needle,insert)
a=s.index('        V += 0.5 * dt * A');b=s.index('        nstep += 1',a)
s=s[:a]+'''        oldR=R.copy();oldV=V.copy();oldA=A.copy()
        coherent=alive & (kind==0) & ((phase==1)|(phase==2))
        phase_margin=np.where(alive & (phase<3),np.where(phase==1,-oldV,oldV),np.inf)
        pstart=pressure() if trigger else np.zeros(N)
        initial_margin=np.r_[phase_margin,np.where(coherent & trigger,Pc-pstart,np.inf)]
        def propose(h):
            nonlocal R,V
            R=np.maximum(oldR+h*(oldV+.5*h*oldA),1e-3)
            me,ph,ii=enclosed();ac=accel(me);V=oldV+.5*h*(oldA+ac)
            return (R.copy(),V.copy(),me,ph,ii,ac)
        def margins(state):
            nonlocal R,V
            R,V=state[0],state[1]
            pm=np.where(alive & (phase<3),np.where(phase==1,-V,V),np.inf)
            pp=pressure() if trigger else np.zeros(N)
            return np.r_[pm,np.where(coherent & trigger,Pc-pp,np.inf)]
        accepted,state,event=localize(propose,margins,initial_margin,dt,relative_tol=event_tol,late=late_events)
        if accepted<1e-12 and t0-t>1e-12 and not (event and event.get('immediate')):raise RuntimeError('event step below declared minimum')
        R,V,Menc,phi,ids,A=state
        t+=accepted
        if event is not None:
            event['t']=t;event['a']=float(a_of_t(t));event['proposal_dt']=dt
            event['phase_residual']=max([abs(V[i]) for i in event['ids'] if i<N] or [0.])
            event['pressure_relative_excess']=max([-x/max(abs(Pc),1e-300) for i,x in zip(event['ids'],event['end']) if i>=N] or [0.])
            events.append(event)
''' +s[b:]
s=s.replace('                galaxy=float(np.sum(gal_M)), fgal=fgal)','                galaxy=float(np.sum(gal_M)), fgal=fgal, events=events,\n                mass_accounting_relative=(float(M.sum())+float(np.sum(gal_M))+budget["escaped"]-initial_mass)/initial_mass)')
(p/'engine_events.py').write_text(s);(p/'engine_events.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),s.splitlines(True),fromfile=str(src),tofile='engine_events.py')))
(p/'provenance.json').write_text(json.dumps({'source':str(src),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'clone_sha256':hashlib.sha256(s.encode()).hexdigest()},indent=2))
