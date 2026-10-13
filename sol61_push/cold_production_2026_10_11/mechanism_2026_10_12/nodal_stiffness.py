"""Static interband bubble, along nodal-ring axis, divided by A."""
from pathlib import Path
import json, math
import numpy as np
from numpy.polynomial.legendre import leggauss
P=Path(__file__).parent
def bubble(m,q,longitudinal,cutoff,nr,nt):
    nodes,weights=leggauss(nr)
    theta=(np.arange(nt)+.5)*2*np.pi/nt
    cost=np.cos(theta)
    edges=sorted(set([0.,q/2,q,2*q,4*q,10*q,cutoff]))
    answer=0.
    for lo,hi in zip(edges[:-1],edges[1:]):
        k=((nodes+1)*(hi-lo)/2+lo)[:,None]
        ea=np.sqrt(k*k+q*q/4-k*q*cost+m*m)
        eb=np.sqrt(k*k+q*q/4+k*q*cost+m*m)
        overlap=k*k-q*q/4+m*m*(1-2*longitudinal)
        kernel=-(1+overlap/(ea*eb))/(ea+eb)
        e=np.sqrt(k*k+m*m)
        zero=-(k*k/e**3 if longitudinal else 1/e)
        integ=np.mean(k*(kernel-zero),axis=1)
        answer+=float(np.dot(weights,integ)*(hi-lo)/2)
    return answer
rows=[];checks={}
for m in [0.,.1,1.]:
 for q in [.2,1.,3.]:
  for longitudinal in [False,True]:
    coarse=bubble(m,q,longitudinal,500*q,100,512)
    fine=bubble(m,q,longitudinal,1000*q,160,1024)
    if m==0: expected=math.pi*q/4
    elif longitudinal:expected=(q*q+4*m*m)/(2*q)*math.atan(q/(2*m))-m
    else:expected=q/2*math.atan(q/(2*m))
    key=f'{m}_{q}_{longitudinal}'
    checks[key+'_positive']=fine>0
    # UV residual is O(q^2/cutoff), not an interval-certified estimate.
    checks[key+'_continuum_comparison']=abs(fine-expected)/expected<.008
    checks[key+'_refinement']=abs(fine-coarse)/expected<.008
    rows.append(dict(gap=m,q=q,longitudinal=longitudinal,coarse=coarse,fine=fine,comparison=expected,relative_error=abs(fine-expected)/expected))
result=dict(checks=checks,all_pass=all(checks.values()),rows=rows,scope='Zero-T, zero-mu two-dimensional energy-plane patch integral along ring axis; excludes ring curvature, generic wavevector, frequency dependence and matter coupling.')
(P/'nodal_stiffness_run'/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2));assert result['all_pass']
