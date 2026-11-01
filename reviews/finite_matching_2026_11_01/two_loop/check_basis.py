import sys,json,math,time,resource
from pathlib import Path
import numpy as np
from model import build_model,graph_weights,grouped
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'gauge_diagrams'))
from full import nonvector
from vertices import gauge_parts

def rotation(masses):
    groups,_=grouped(masses);rot=np.eye(len(masses));c=math.cos(math.pi/7);s=math.sin(math.pi/7)
    for item in groups:
        ids=item['indices']
        for a,b in zip(ids[::2],ids[1::2]):rot[a,a]=rot[b,b]=c;rot[a,b]=-s;rot[b,a]=s
    return rot

def rotated(d):
    out=dict(d);rs=rotation(d['mS2']);rf=rotation(d['mF2']);rv=rotation(d['mV2'])
    out['O']=d['O']@rs;out['U']=d['U']@rf;out['Ov']=d['Ov']@rv
    out['cubic']=np.einsum('ai,bj,ck,abc->ijk',rs,rs,rs,d['cubic'],optimize=True)
    out['yukawa']=np.einsum('Iu,Jv,IJa,ab->uvb',rf,rf,d['yukawa'],rs,optimize=True)
    yr=np.einsum('pab,ai,bj->pij',d['YR'],rs,rs,optimize=True)
    sm=np.einsum('pab,ai,bj->pij',d['Sm'],rs,rs,optimize=True)
    yd=np.diagonal(yr,axis1=1,axis2=2);sd=np.diagonal(sm,axis1=1,axis2=2)
    out['quartic_iijj']=2*(yd.conj().T@yd).real+4*np.sum(abs(yr)**2,axis=0)+sd.T@sd+2*np.sum(sm**2,axis=0)
    return out

def graphs(d,Q2):
    nv,diag=nonvector(d,Q2)
    gv=gauge_parts(d['z'],d['R'],d['g'],d['mS2'],d['O'],d['mF'],d['U'],d['mV2'],d['Ov'],Q2)
    return dict(nv,**gv['parts'])

def main(path):
    start=time.monotonic();e=.03;z=7.367143721278508;X=z/math.sqrt(31*e);Q2=e/31+(e*X)**2
    d=build_model(X,e,e,math.sqrt(29/200)*e,1);r=rotated(d)
    wa=graph_weights(d);wb=graph_weights(r)
    weight_err={k:float(np.max(abs(wa[k]-wb[k])))/max(float(np.max(abs(wa[k]))),1e-300) for k in ['SSS','SS','FFS','barFFS']}
    ga=graphs(d,Q2);gb=graphs(r,Q2);norm=sum(abs(v) for v in ga.values())
    graph_error={k:abs(v-gb[k])/max(norm,1e-300) for k,v in ga.items()}
    e2=.01;X2=z/math.sqrt(31*e2);q2=e2/31+(e2*X2)**2
    scaled=graphs(build_model(X2,e2,e2,math.sqrt(29/200)*e2,1),q2)
    scale_errors={k:abs(scaled[k]-(e2/e)**4*v)/max(norm*(e2/e)**4,1e-300) for k,v in ga.items()}
    susy=build_model(1.7,.03,.03,0,0);sp,sd=nonvector(susy,.021)
    susy_rel=abs(sum(sp.values()))/max(sum(abs(v) for v in sp.values()),1e-300)
    checks={'four_graph_weight_rotation':max(weight_err.values())<1e-8,
            'ten_finite_graph_rotation':max(graph_error.values())<1e-8,
            'ten_graph_e4_scaling':max(scale_errors.values())<1e-8,
            'ungauged_fullSU5_SUSY':susy_rel<1e-9}
    out={'claim_id':'FM_BASIS_SCALING','checks':checks,'weight_rotation_relative_errors':weight_err,
         'finite_graph_rotation_normalized_errors':graph_error,'finite_graph_scaling_normalized_errors':scale_errors,
         'reference_parts_loop_stripped':ga,'scaled_parts_loop_stripped':scaled,
         'ungauged_SUSY_parts':sp,'ungauged_SUSY_relative_residual':susy_rel,
         'runtime_seconds':time.monotonic()-start,'peak_RSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'non_claims':['No pressure endpoints evaluated in this control','Finite numerical checks are not all-parameter proof']}
    Path(path).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1])
