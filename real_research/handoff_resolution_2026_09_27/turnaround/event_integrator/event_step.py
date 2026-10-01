"""Bracketed event localization on the unaccepted KDK trial map."""
import numpy as np

def localize(propose, margins, initial, dt, relative_tol=1e-6, min_dt=1e-12, max_bisect=40, late=False):
    already=(initial<0)&np.isfinite(initial)
    if np.any(already):
        state=propose(0.)
        return 0.,state,dict(bisections=0,bracket_width=0.,lo=0.,hi=0.,ids=np.where(already)[0].tolist(),start=initial[already].tolist(),end=initial[already].tolist(),immediate=True)
    state=propose(dt);end=margins(state)
    crossed=(initial>=0)&(end<0)&np.isfinite(initial)
    if not np.any(crossed):return dt,state,None
    if late:return dt,state,dict(bisections=0,bracket_width=dt,lo=0.,hi=dt,ids=np.where(crossed)[0].tolist(),start=initial[crossed].tolist(),end=end[crossed].tolist())
    lo=0.;hi=dt;steps=0
    while hi-lo>max(min_dt,relative_tol*dt) and steps<max_bisect:
        mid=(lo+hi)/2;s=propose(mid);m=margins(s)
        if np.any((initial>=0)&(m<0)&np.isfinite(initial)):hi=mid;state=s;end=m
        else:lo=mid
        steps+=1
    crossed=(initial>=0)&(end<0)&np.isfinite(initial)
    return hi,state,dict(bisections=steps,bracket_width=hi-lo,lo=lo,hi=hi,ids=np.where(crossed)[0].tolist(),start=initial[crossed].tolist(),end=end[crossed].tolist())
