"""Admissible full-sphere axial-linear manufactured Hessian control."""
import argparse,json,time
from pathlib import Path
from types import SimpleNamespace
import generalized_v3 as J
np,M=J.np,J.M

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();start=time.monotonic()
    out={'domain':'full sphere; scalar z is admissible at both poles; equator is interior','rows':[],'all_checks_pass':False}
    for refinement in [1,2,3,4,5]:
        g=M.C.PS.Grid(M.C.PS.log_edges(.02,100,30*refinement),M.C.PS.theta_edges(48*refinement,full=True,stretch_min=.002/refinement))
        model=J.Generalized(SimpleNamespace(g=g));r,t=g.r2d,g.t2d
        ii=np.arange(g.n)//g.Nt;jj=np.arange(g.n)%g.Nt
        use=(ii>=2)&(ii<g.Nr-2)
        regions={'poles':use&((jj<2)|(jj>=g.Nt-2)),'equator':use&(abs(jj-g.Nt//2)<=2),'interior':use&(jj>=2)&(jj<g.Nt-2)}
        hh=model.fields(r*np.cos(t))[1]*r
        row={'refine':refinement,'component_scaled_errors':{reg:{name:float(np.max(abs(hh[i,mask]))) for i,name in enumerate(['rr','rt','tt','pp'])} for reg,mask in regions.items()}}
        out['rows'].append(row)
        a.output.write_text(json.dumps(out,indent=2)+'\n')
    for reg in regions:
        first=max(out['rows'][0]['component_scaled_errors'][reg].values());last=max(out['rows'][-1]['component_scaled_errors'][reg].values())
        assert last<first and last<.01
    out['all_checks_pass']=True;out['runtime_seconds']=time.monotonic()-start;a.output.write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
