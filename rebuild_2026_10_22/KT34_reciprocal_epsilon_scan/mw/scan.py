#!/usr/bin/env python3
"""Read-only reuse of KT33; epsilon alone changes. Import-safe cached basis scan."""
import argparse
import json
import math
import os
from pathlib import Path
import sys
import time
sys.dont_write_bytecode=True
for v in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[v]='1'
HERE=Path(__file__).resolve().parent
RB=HERE.parents[1]
sys.path.insert(0,str(RB/'KT33_reciprocal_filter/mw'))
import mw_reciprocal as M
import numpy as np


def population():
    out=[c for c in M.cells() if M.C.L.RD_TAG[0]<=c['rd']<=M.C.L.RD_TAG[1] and M.C.L.MSTAR_TAG[0]<=M.rho_cell(c)[1]<=M.C.L.MSTAR_TAG[1]]
    assert len(out)==1375
    return out


def rm(c,foot,gm):
    return math.sqrt(4.30091e-6*(M.rho_cell(c)[1]+gm)/(M.C.A0[foot]*3.0857e19/1e6))


def width(epsilon,r):
    return 0. if epsilon==0 else math.exp(round(math.log(epsilon*r)/.005)*.005)


class Cached:
    def __init__(self,foot,refine,cells):
        self.foot=foot
        self.g,self.mu=M.make_grid(M.C.A0[foot],refine,1)
        self.sol=M.Solver(self.g,self.mu,M.C.A0[foot]);self.cells=cells
        ns=M.C.ns;F=M.C.F;g=self.g;mu=self.mu
        self.keys=[('gas',),('bulge',)]
        for c in cells:
            for k in [('disk',c['rd'],c.get('ht',ns['ZD_THIN'])),('disk',c.get('rdk',c['rd']),c.get('hk',ns['ZD_THICK']))]:
                if k not in self.keys:self.keys.append(k)
        basis=[]
        for key in self.keys:
            if key[0]=='gas':rf=M.gas_density
            elif key[0]=='bulge':
                def rf(R,z):
                    rp=np.maximum(np.sqrt(R*R+(np.abs(z)/ns['Q_B'])**2),1e-7)
                    return ns['RHO0_B']/(1+rp/ns['R0_B'])**ns['ALPHA_B']*np.exp(-(rp/ns['RCUT_B'])**2)
            else:
                _,rd,h=key
                def rf(R,z,rd=rd,h=h):return 1e9/(2*h)*np.exp(-np.abs(z)/h-R/rd)
            basis.append(g.rho_axisym(lambda R,z:rf(R,z)/mu,nq=4))
        self.basis=np.array(basis);self.newton=np.array([self.sol.LU.newton(x) for x in self.basis])
        self.coef=[]
        for c in cells:
            cf=np.zeros(len(basis));cf[0]=1;cf[1]=c['mbb']/F.M_bulge_mcm
            ss=F.params(c['sb'],c['mbb'],c['rd'])['sig_star_R0']*1e6
            ft=F.f_thin if 'fk' not in c else 1-c['fk'];rk=c.get('rdk',c['rd'])
            cf[self.keys.index(('disk',c['rd'],c.get('ht',ns['ZD_THIN'])))]+=ft*ss*math.exp(M.C.R0/c['rd'])/1e9
            cf[self.keys.index(('disk',rk,c.get('hk',ns['ZD_THICK'])))]+=(1-ft)*ss*math.exp(M.C.R0/rk)/1e9
            self.coef.append(cf)
        self.coef=np.array(self.coef)
        self.source_mass=self.coef@(self.basis@g.vol)
        self.verify={}
        for i in (0,24,25,500,1000,1374):
            rf,_=M.rho_cell(cells[i]);literal=g.rho_axisym(lambda R,z:rf(R,z)/mu,nq=4)
            cached=self.combine(self.basis,i)
            err=float(np.max(np.abs(literal-cached))/np.max(literal));assert err<1e-13
            self.verify[str(i)]=err

    def combine(self,basis,i):
        inds=np.flatnonzero(self.coef[i]);return sum(self.coef[i,j]*basis[j] for j in inds)

    def scan(self,epsilon,lmax,cut=120,indices=None,explicit_widths=None):
        gm=M.gas_mass();ids=list(range(len(self.cells))) if indices is None else indices
        radii=[rm(c,self.foot,gm) for c in self.cells]
        widths={i:width(epsilon,radii[i]) for i in ids} if explicit_widths is None else explicit_widths
        groups={}
        for i in ids:groups.setdefault(widths[i],[]).append(i)
        rows=[];max_masserr=0.;maxneg=0.;minrel=0.
        for sig,group in sorted(groups.items()):
            S=self.sol.get_filter(sig,lmax,cut)
            rb=np.array([S.forward(x) for x in self.basis]);pb=np.array([self.sol.LU.newton(x) for x in rb])
            for i in group:
                pn=self.combine(self.newton,i);rx=self.combine(rb,i);px=self.combine(pb,i)
                ph=self.sol.phantom(px);phi=pn+S.adjoint(ph);q=self.sol.evaluate(phi)
                mass=float(np.dot(self.g.vol,rx));negative=float(-np.dot(self.g.vol,np.minimum(rx,0))/mass)
                maxneg=max(maxneg,negative);minrel=min(minrel,float(np.min(rx)/np.max(rx)))
                max_masserr=max(max_masserr,abs(mass/self.source_mass[i]-1))
                recomputed=M.C.lines(q['vc'],q['K'],q['K0'],q['vc_Ou'])
                assert all(q[k]==recomputed[k] for k in (*M.GATE,'Lh'))
                assert max(abs(q[k]-recomputed[k]) for k in ('cK','cO','h','D'))<1e-10
                rows.append(dict(index=i,cell=self.cells[i],xi=sig,RM=radii[i],corrected=q,negative_mass_fraction=negative))
        rows.sort(key=lambda r:r['index'])
        good=[r for r in rows if r['corrected']['all_four']]
        best=min(rows,key=lambda r:r['corrected']['D']);bestou=min(rows,key=lambda r:r['corrected']['cO'])
        summary=dict(n_tested=len(rows),n_pass=len(good),n_strict=sum(r['corrected']['Lh'] for r in good),n_share_012=sum(r['cell'].get('fk')==.12 for r in good),lines={k:sum(r['corrected'][k] for r in rows) for k in (*M.GATE,'Lh')},min_cO=bestou['corrected']['cO'],max_vc=max(r['corrected']['vc'] for r in rows),best_D_index=best['index'],best_Ou_index=bestou['index'],pass_indices=[r['index'] for r in good],max_negative_mass_fraction=maxneg,min_density_over_peak=minrel,max_source_mass_relative_error=max_masserr,n_distinct_widths=len(groups),numerical_tail_gate_passed=maxneg<=1e-5)
        assert max_masserr<1e-10
        return dict(epsilon=epsilon,lmax=lmax,cut=cut,summary=summary,rows=rows)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--eps',type=float,nargs='+',required=True);ap.add_argument('--refine',type=int,default=2);ap.add_argument('--lmax',type=int,default=48);ap.add_argument('--cut',type=float,default=120);ap.add_argument('--feet',nargs='+',default=list(M.C.A0));ap.add_argument('--indices',type=int,nargs='+');args=ap.parse_args()
    start=time.monotonic();cells=population();out=dict(parameters=vars(args),equation='Phi=N rho+S*Phi_ph[S rho]',epsilon_width='exp(round(log(epsilon RM)/.005)*.005), identity at epsilon=0',gas_mass=M.gas_mass(),cells=cells,footings={})
    for foot in args.feet:
        cache=Cached(foot,args.refine,cells);f=dict(grid=dict(nr=cache.g.Nr,nt=cache.g.Nt),basis_keys=cache.keys,basis_density_verification=cache.verify,scans=[])
        out['footings'][foot]=f
        for ep in args.eps:
            row=cache.scan(ep,args.lmax,args.cut,args.indices)
            if ep==.5 and args.refine==2 and args.lmax==48 and args.indices is None:
                prior=json.loads((M.HERE/'grid_refined_run/results.json').read_text())['footings'][foot]['rows']
                er={k:max(abs(x['corrected'][k]-y['corrected'][k]) for x,y in zip(row['rows'],prior)) for k in ('vc','K0','cO','cK')}
                assert max(er.values())<1e-7
                row['KT33_reproduction_max_absolute_errors']=er
            f['scans'].append(row);print(foot,ep,json.dumps(row['summary']), 'seconds',time.monotonic()-start,flush=True)
            Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False))
    out['runtime_seconds']=time.monotonic()-start;Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False))

if __name__=='__main__':main()
