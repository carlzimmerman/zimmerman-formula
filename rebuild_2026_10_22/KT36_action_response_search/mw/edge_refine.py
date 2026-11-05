#!/usr/bin/env python3
"""Refine the closest finite constitutive candidate, without changing its law."""
import argparse,json,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
import constitutive as C
M,E,np=C.M,C.E,C.np

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    start=time.monotonic();cell=E.population()[1359];foot='canonical';ep=.24
    response=C.Response('cutoff',scale=1.587,power=6.3)
    sig=E.width(ep,E.rm(cell,foot,M.gas_mass()))
    out=dict(index=1359,cell=cell,footing=foot,epsilon=ep,response=response.metadata,xi=sig,
             coverage='Closest selected candidate only; not an exhaustive refined population',cases=[])
    for refine,cut in [(2,120),(3,120),(4,120),(3,240)]:
        g,mu=M.make_grid(M.C.A0[foot],refine,1);sol=C.Solver(g,mu,M.C.A0[foot],response)
        row=sol.solve(cell,sig,192,cut)
        rf,_=M.rho_cell(cell);rho=g.rho_axisym(lambda R,z:rf(R,z)/mu,nq=4);rx=sol.get_filter(sig,192,cut).forward(rho)
        mass=float(np.dot(g.vol,rx));neg=float(-np.dot(g.vol,np.minimum(rx,0))/mass)
        err=abs(mass/np.dot(g.vol,rho)-1)
        assert neg<1e-5 and err<1e-10
        out['cases'].append(dict(refine=refine,cut=cut,lmax=192,row=row,negative_mass_fraction=neg,mass_error=err))
        print(refine,cut,{k:row['corrected'][k] for k in ('vc','K0','cO','cK','h','all_four')},flush=True)
    out['all_selected_refinements_fail']=all(not x['row']['corrected']['all_four'] for x in out['cases'])
    out['runtime_seconds']=time.monotonic()-start
    Path(a.output).write_text(json.dumps(out,indent=2,allow_nan=False))

if __name__=='__main__':main()
