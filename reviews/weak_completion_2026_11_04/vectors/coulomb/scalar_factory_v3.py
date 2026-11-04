"""Common-gas embedding of the controlled cold Sc_0 self-Coulomb operator.

This is an additional elastic channel, not a replacement for full S/F/vector
1<->2. It covers twelve scalar charged modes, same/anticharge colour average,
with separately screened SU3/SU2/U1 direct-t currents. Light-bath terms remain
separate. Call with the physical Sc_0 occupation used to set screening; retain
screen in a nonlinear step and rebuild at its endpoint/predictor as controlled.
"""
import sys,math
from pathlib import Path
import numpy as np
HERE=Path(__file__).parent;ROOT=HERE.parents[3]
sys.path.insert(0,str(HERE));sys.path.insert(0,str(ROOT/'reviews/weak_completion_2026_11_04/integration'))
from elastic_builder_v3 import screening,event_arrays_chunked
from binary_events_v2 import BinaryEvents

def scalar_events(data,T,q,W,f,measure=None,incoming_angles=8,azimuth=2,log_order=2,max_log_span=3.,extra_screening=None):
 q=np.asarray(q);W=np.asarray(W);groups=data['groups'];n=len(q);by={g['id']:i for i,g in enumerate(groups)};gid=by['Sc_0'];m=groups[gid]['mass'];f=np.asarray(f)
 fC=f.reshape(len(groups),n)[gid] if len(f)!=n else f
 md2=screening(q,W,fC,T,m)
 if extra_screening is not None:md2=md2+np.asarray(extra_screening)
 a=event_arrays_chunked(q,W,T,m,md2,incoming_angles=incoming_angles,azimuth=azimuth,log_order=log_order,max_log_span=max_log_span,diagnostic_f=fC);full_measure=(np.repeat([g['degeneracy'] for g in groups],n)*np.tile(W,len(groups))/(2*math.pi**2)) if measure is None else np.asarray(measure);eta=np.repeat([1 if g['kind'] in ('S','V') else -1 for g in groups],n);masses=np.array([g['mass'] for g in groups]);energy=np.sqrt(masses[:,None]**2+(T*q[None,:])**2).ravel();index=a['index']+gid*n;ev=BinaryEvents(index,a['weights'],a['coefficient'],full_measure,energy,eta,groups);ev.q=q;ev.W=W;ev.t=T;ev.masses=masses;ev.energies=energy.reshape(len(groups),n);ev.screening_masses=np.sqrt(md2);ev.kinetic_energy_residual=a['energy_residual'];ev.omitted_incoming_i=a['omitted_incoming_i']+gid*n;ev.omitted_incoming_j=a['omitted_incoming_j']+gid*n;ev.omitted_coefficient=a['omitted_coefficient'];ev.physical_diagnostics=a['diagnostics'];ev.coverage='ColdSc_0selfelasticdirecttleading-log; noothermaterialspeciesorbathscatteringsimplicitlyincluded';return ev
