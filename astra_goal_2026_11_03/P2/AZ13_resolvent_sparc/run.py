import sys
from pathlib import Path
import numpy as np
from scipy.linalg import solve_banded
from scipy.special import gammainc
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from record import record
ROOT=Path(__file__).resolve().parents[3]
FILES=sorted(ROOT.glob('real_research/data/sparc_data/*_rotmod.dat'))
TABLE=ROOT/'real_research/data/SPARC_Lelli2016c.mrt'
G=4.30091e-6

def smooth(edges,mass,xi):
    vol=4*np.pi/3*np.diff(edges**3)
    c=.75*np.diff(edges**4)/np.diff(edges**3)
    conduct=4*np.pi*xi**2*edges[1:-1]**2/np.diff(c)
    diag=vol.copy();diag[:-1]+=conduct;diag[1:]+=conduct
    ab=np.zeros((3,len(vol)));ab[1]=diag;ab[0,1:]=-conduct;ab[2,:-1]=-conduct
    u=solve_banded((1,1),ab,mass)
    u=solve_banded((1,1),ab,vol*u)
    return vol*u,float(abs(np.sum(vol*u)/np.sum(mass)-1)),float(np.min(u)/np.max(u))

def nu(y): return .5+np.sqrt(.25+1/y)
def stat(res):
    return {'rms':float(np.sqrt(np.mean([np.mean(r*r) for r in res]))),'median':float(np.median(np.concatenate(res)))}
def gate(s,p):return s['rms']-p['rms']<=.005 and abs(s['median'])<=.05

def calculate():
    tab={}
    for line in TABLE.read_text().splitlines():
        p=line.split()
        if len(p)>=18 and p[1].isdigit():tab[p[0]]=(float(p[7])*1e9,float(p[11]),float(p[13])*1e9)
    galaxies=[]
    for f in FILES:
        name=f.name.replace('_rotmod.dat','');d=np.genfromtxt(f,comments='#')
        if name not in tab or d.ndim!=2 or d.shape[1]<6 or len(d)<3:continue
        d=d[np.argsort(d[:,0])];r,v,ev,vg,vd,vb=d[:,:6].T
        b=vg*abs(vg)+.5*vd*abs(vd)+.7*vb*abs(vb)
        q=(r>0)&(v>0)&(ev>0)&(ev<.1*v)&(b>0)
        if sum(q)<3:continue
        assert r[0]>0,'Profile has zero radius: pre-result amendment needed'
        galaxies.append((name,r,v,b,q,tab[name]))
    edges=np.r_[0,np.geomspace(1e-6,30,2048)];mass=np.zeros(2048);mass[0]=1
    sm,err,pos=smooth(edges,mass,1)
    point_error=float(max(abs(np.interp([1,2,4],edges,np.r_[0,np.cumsum(sm)])-gammainc(3,[1,2,4]))))
    checks=[{'name':'point-source exact kernel','passed':point_error<=.002}, {'name':'population 155 galaxies 2788 points','passed':len(galaxies)==155 and sum(sum(g[4]) for g in galaxies)==2788}]
    feet={};maxmass=err;minpos=pos
    for foot,a0si in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
        a0=a0si*3.0857e19/1e6;plain=[];mut=[];runs={};pergal={}
        for n in [1024,2048]:
            residuals=[]
            for name,r,v,b,q,(lum,rd,mhi) in galaxies:
                mb=.5*lum+1.33*mhi;rd=max(rd,.1);xi=.5*np.sqrt(G*mb/a0)
                edges=np.r_[0,np.geomspace(min(r[0],.01)*.001,r[-1]+30*xi+20*rd,n)]
                mr=np.maximum.accumulate(np.maximum(b*r/G,0))
                me=np.interp(edges,r,mr)
                inside=edges<r[0];me[inside]=mr[0]*(edges[inside]/r[0])**3
                outside=edges>r[-1];x=(edges[outside]-r[-1])/rd
                me[outside]=mr[-1]+max(mb-mr[-1],0)*(-np.expm1(-x)-x*np.exp(-x))
                sm,err,pos=smooth(edges,np.diff(me),xi);maxmass=max(maxmass,err);minpos=min(minpos,pos)
                ratio=np.interp(r[q],edges,np.r_[0,np.cumsum(sm)])/np.interp(r[q],edges,me)
                gb=b[q]/r[q];go=v[q]**2/r[q];gh=gb*ratio
                gm=gb+(nu(gh/a0)-1)*gh
                res=np.log10(go/gm);residuals.append(res)
                if n==2048:
                    pr=np.log10(go/(nu(gb/a0)*gb));plain.append(pr);mut.append(np.log10(go/gb))
                    pergal[name]={'points':int(sum(q)),'rms':float(np.sqrt(np.mean(res**2))),'plain_rms':float(np.sqrt(np.mean(pr**2)))}
            runs[str(n)]=stat(residuals)
        p=stat(plain);m=stat(mut);s=runs['2048'];coarse=runs['1024']
        refine=max(abs(s[k]-coarse[k]) for k in s)
        checks.extend([{'name':foot+' refinement','passed':refine<=.001 and gate(s,p)==gate(coarse,p)}, {'name':foot+' MUTATE rejected','passed':not gate(m,p)}])
        feet[foot]={'label':'PASS' if gate(s,p) else 'FAIL','plain':p,'filtered':s,'MUTATE':m,'refinement':runs,'max_refinement_dex':refine,'rms_margin_dex':.005-(s['rms']-p['rms']),'median_margin_dex':.05-abs(s['median']),'galaxies':pergal}
    gb=np.array([.01,1,100]);a0=1.;z=gb+(nu(gb/a0)-1)*gb
    zero_error=float(max(abs(z-nu(gb/a0)*gb)))
    checks.extend([{'name':'mass conservation','passed':maxmass<=1e-9},{'name':'positive density','passed':minpos>=-1e-12},{'name':'zero-width plain law','passed':zero_error<=1e-12}])
    for c in checks:c['passed']=bool(c['passed'])
    label='PASS' if all(v['label']=='PASS' for v in feet.values()) else 'FAIL'
    if not all(c['passed'] for c in checks):
        label='NO VERDICT'
        for v in feet.values():v['provisional_gate_label']=v['label'];v['label']='NO VERDICT'
    return {'assertion_tested':'Fixed squared-resolvent spherical surrogate preserves frozen SPARC comparison lines','label':label,'footings':feet,'bounds':{'shells':[1024,2048],'galaxies':len(galaxies),'points':int(sum(sum(g[4]) for g in galaxies))},'checks':checks,'control_values':{'point_absolute_error':point_error,'max_mass_relative_error':maxmass,'min_density_over_peak':minpos,'zero_width_error':zero_error},'free_physical_numbers':['kappa=.5 FITTED','stellar M/L .5 and bulge .7 FITTED held','a0 two held footings','helium inventory 1.33 assumed','outer Rd floor .1 kpc assumed','integer resolvent power 2 model choice'], 'residual_risks':['Spherical surrogate, not a disc field solution','Fixed mass-to-light; no full A1/A2 acceptance claim','System-mass xi is not local','No action completion or planetary rescue']}
if __name__=='__main__':record(__file__,calculate,extra_inputs=[str(p.relative_to(ROOT)) for p in [TABLE]+FILES])
