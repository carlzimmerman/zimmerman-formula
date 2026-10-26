"""Conservative branch/line event ledger, not a physical DR rate calculator.

Leading infinite-nuclear-mass Coulomb energies, consistent with old photon ledger.
Do not combine unmodified with finite-mass scattering thresholds.
"""
import numpy as np

def event_sources(D,dr_events,line_event):
    """Net DR events to 1s+1s,1s+2s,1s+2p; net2p->1s+photon event.

    Reverse events may be negative. Caller must derive rates/detailed balance.
    Returns x,c,a1,a2s,a2p,t,K,gamma. No default or manufactured collision rate.
    """
    r=np.asarray(dr_events,dtype=float)
    if r.shape!=(3,) or not np.all(np.isfinite(r)) or not np.isfinite(D) or not np.isfinite(line_event):raise ValueError('Finite specified events required')
    g,s,p=r;l=line_event
    return np.array([0,-sum(r),2*g+s+p+l,s,p-l,-sum(r),(.5-D)*g+(.125-D)*(s+p),l])

def line_event(alpha,a1,a2p,occupation,coefficient=.03901844231062337):
    """2p triplet aggregate ↔1s photon mode, clamped Coulomb E1 limit.

    Time in atomic units. occupation is photon phase-space occupation, NOT
    photons per atom. It must be computed from the radiation spectral density.
    The statistical factor3 counts magnetic p orbitals; equal electron-spin
    multiplicities cancel. 2s one-photon decay is forbidden and absent here.
    """
    if min(alpha,a1,a2p,occupation,coefficient)<0 or not all(np.isfinite(x) for x in [alpha,a1,a2p,occupation,coefficient]):raise ValueError('Nonnegative finite inputs required')
    return coefficient*alpha**3*(a2p*(1+occupation)-3*a1*occupation)
