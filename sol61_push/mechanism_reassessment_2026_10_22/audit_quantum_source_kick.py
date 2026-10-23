"""Independent Gaussian quadrature and gradient checks of the exact kick map."""
from pathlib import Path
import json,sys
import numpy as np
from scipy.special import roots_hermite
from quantum_source_kick import residual_potential,residual_force,phase_kick
P=Path(__file__).resolve().parent;O=P/sys.argv[1];O.mkdir(exist_ok=True)
x,w=roots_hermite(7);w=w/np.sqrt(np.pi);C=np.array([.02,.03,.04,.05]);q=.28;c=.03;lam=.00881292
coords=np.meshgrid(x,x,x,x,indexing='ij');weights=np.meshgrid(w,w,w,w,indexing='ij');weight=np.prod(weights,axis=0);fields=np.array([np.sqrt(2*C[i])*coords[i] for i in range(4)])
V=residual_potential(fields,q,C[:2],c);V4=residual_potential(fields,0,C[:2],0);V3=V-V4;force=residual_force(fields,q,C[:2],c)
expected=lambda a:np.sum(weight*a)
S3=expected(V3*V3);S4=expected(V4*V4)
number_force=sum(C[i]*expected(force[i]**2) for i in range(4))/lam**2
number_wick=(3*S3+4*S4)/lam**2
# A generic stronger cubic coefficient is used only to expose all algebraic signs.
direction=np.array([.23,-.13,.47,-.37])[:,None,None,None,None];eps=1e-5
fd=(residual_potential(fields+eps*direction,q,C[:2],c)-residual_potential(fields-eps*direction,q,C[:2],c))/(2*eps)
exact=-np.sum(force*direction,axis=0)
kick=phase_kick(fields,.05,.01,q,C[:2],c);reverse=phase_kick(fields,-.05,.01,q,C[:2],c)
checks=dict(residual_mean_zero=abs(expected(V))<1e-14,force_mean_zero=max(abs(expected(f)) for f in force)<1e-14,Gaussian_number_identity=abs(number_force/number_wick-1)<1e-12,cubic_quartic_orthogonal=abs(expected(V3*V4))<1e-14,potential_gradient=np.max(abs(fd-exact))<1e-8,kick_unitary=abs(abs(kick)-1)<1e-14,inverse_kick=abs(kick*reverse-1)<1e-14)
out=dict(checks={k:bool(v) for k,v in checks.items()},all_pass=bool(all(checks.values())),number_coefficient_from_force=number_force,number_coefficient_from_Wick_sectors=number_wick,gradient_max_absolute_error=float(np.max(abs(fd-exact))),scope='Single-point algebra and Gaussian integration benchmark for the non-Gaussian potential substep. Generic test parameters, not a cosmological trajectory or physical inverse reaction rate.')
(O/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
