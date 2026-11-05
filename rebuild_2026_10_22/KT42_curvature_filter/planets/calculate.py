"""Fixed-law planetary monopole with complete Gaussian curvature adjoint."""
import argparse
from functools import lru_cache
import json
import math
from pathlib import Path
import sys
import time
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE.parent/'solar'))
import calculate_v2 as S
S.leggauss=lru_cache(maxsize=None)(S.leggauss)
LENGTHS_KPC=[.0001,.001,.1,.3]
ECC={'Mars':.093,'Saturn':.054}
YEAR=365.25*86400
MAS=math.pi/(180*3600*1000)


def i1_pair(z,terms=8):
    value=np.zeros_like(z);deriv=np.zeros_like(z)
    for k in range(terms):
        coeff=2*(k+1)/math.factorial(2*k+3)
        value+=coeff*z**(2*k+1)
        deriv+=coeff*(2*k+1)*z**(2*k)
    return value,deriv


class Monopole:
    def __init__(self,eta,ell,width,nr=2000,nm=80,umax=16):
        self.eta,self.ell,self.width,self.nm=eta,ell,width,nm
        self.logu=np.linspace(math.log(1e-11),math.log(umax),nr)
        self.r=width*np.exp(self.logu)
        r=self.r[:,None];mu,w=S.leggauss(nm);mu=mu[None,:]
        self.hr,self.ht,*_=S.softened_tidal(self.r,width)
        s=ell*ell*(self.hr*self.hr+2*self.ht*self.ht)
        h=s[:,None]**S.P;beta=S.P*ell*ell*s[:,None]**(S.P-1)
        g=r**-2;x=g*g+eta*eta+2*g*eta*mu
        _,d1,*_=S.C.base.scaled_R(x+h)
        self.d0=np.sum(beta*x/(x+h)*d1*w,axis=1)

    def A(self,R,plain=False):
        R=np.atleast_1d(R);r=R[:,None];g=r**-2
        mu,w=S.leggauss(self.nm);mu=mu[None,:]
        if plain:h=np.zeros_like(r)
        else:
            hr,ht,*_=S.softened_tidal(r,self.width)
            h=(self.ell*self.ell*(hr*hr+2*ht*ht))**S.P
        x=g*g+self.eta*self.eta+2*g*self.eta*mu
        rm,d1,*_=S.C.base.scaled_R(x+h)
        c=rm+x/(x+h)*d1
        return .5*np.sum(c*(g+self.eta*mu)*w,axis=1)

    def B(self,R,terms=8):
        R=np.atleast_1d(R)[None,:];r=self.r[:,None];a=self.width
        z=r*R/a**2;i,ip=i1_pair(z,terms)
        kernel=np.exp(-.5*((r/a)**2+(R/a)**2))
        bracket=self.hr[:,None]*(-r**4/a**2*i+r**3*R/a**2*ip)+2*r*r*self.ht[:,None]*i
        integrand=math.sqrt(2/math.pi)/(2*a**3)*self.d0[:,None]*kernel*bracket
        return np.trapz(integrand,self.logu,axis=0)

    def total(self,R):return self.A(R)+self.B(R)

    def B_ball(self,R,order=8):
        v,wv=S.leggauss(order);v=(v+1)/2;wv=wv/2
        xi,wx=S.leggauss(order)
        u=(self.r/self.width)[:,None,None];v=v[None,:,None];xi=xi[None,None,:]
        eps=R/self.width
        weights=wv[None,:,None]*wx[None,None,:]*v*v
        ex=np.exp(-.5*(u*u+eps*eps*v*v-2*u*eps*v*xi))
        jr=np.sum(weights*ex*((u-eps*v*xi)**2-1),axis=(1,2))
        jt=np.sum(weights*ex*(eps*eps*v*v*(1-xi*xi)/2-1),axis=(1,2))
        val=-R/(2*math.sqrt(2*math.pi)*self.width**5)*self.r**3*self.d0*(self.hr*jr+2*self.ht*jt)
        return float(np.trapz(val,self.logu))

    def B_linear(self,R):
        a=self.width;u=self.r/a
        value=-R/(3*math.sqrt(2*math.pi)*a**5)*self.r**3*self.d0*np.exp(-.5*u*u)*(self.hr*(u*u-1)-2*self.ht)
        return float(np.trapz(value,self.logu))


def rate(fn,axis,e,n,order):
    t,w=S.leggauss(order);E=math.pi*(t+1);c=np.cos(E);r=axis*(1-e*c)
    return math.sqrt(1-e*e)/(n*axis*e)*float(np.sum(.5*w*fn(r)*(c-e)))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    started=time.monotonic()
    table=json.loads((ROOT/'rebuild_2026_10_22/RQ3_acceptance_v2/tolerances.json').read_text())['PLANETS']
    out=dict(widths_kpc=LENGTHS_KPC,planets=list(ECC),GM_SI=S.C.old.GM,GEXT_SI=S.C.old.GEXT,
             AZ11_GM_for_comparison_only=1.32712440018e20,footings={},checks={},orbital_oracles=[])
    for name,e in ECC.items():
        root=math.sqrt(1-e*e)
        errors=[]
        for fn,oracle in [(lambda r:np.ones_like(r),-root),(lambda r:r,-1.5*root),(lambda r:1/r**2,0.)]:
            errors.append(abs(rate(fn,1,e,1,128)-oracle))
        out['orbital_oracles'].append(dict(planet=name,errors=errors))
    out['checks']['AZ12_three_oracles']=max(max(x['errors']) for x in out['orbital_oracles'])<1e-10
    for foot,a0 in S.C.old.A0.items():
        eta=S.C.old.GEXT/a0;rm=math.sqrt(S.C.old.GM/a0);ell=3*S.C.KPC/rm
        ff=out['footings'][foot]=dict(a0=a0,eta=eta,rM_m=rm,rows=[])
        for width_kpc in LENGTHS_KPC:
            width=width_kpc*S.C.KPC/rm
            coarse=Monopole(eta,ell,width)
            fine=Monopole(eta,ell,width,nr=4000,nm=160,umax=24)
            for planet,e in ECC.items():
                d=table[planet];axis=d['a_au']*S.C.old.AU;R=axis/rm;n=math.sqrt(S.C.old.GM/axis**3)
                sigma=d['dg_tight']*max(d['EPM'],d['INPOP'])/min(d['EPM'],d['INPOP'])
                ga=float(fine.A(R)[0]);gb=float(fine.B(R)[0]);full=(ga+gb)*a0
                low=float(coarse.total(R)[0])*a0
                bb4=fine.B_ball(R,4);bb8=fine.B_ball(R,8)
                b6=float(fine.B(R,6)[0]);blin=fine.B_linear(R)
                plain=float(fine.A(R,plain=True)[0])*a0
                mu,w=S.leggauss(160);u=R**-2;y=np.sqrt(u*u+eta*eta+2*u*eta*mu)
                nu_minus=1/(y*(np.sqrt(.25+1/y)+.5))
                plain_independent=float(.5*np.sum(w*nu_minus*(u+eta*mu)))*a0
                highrate=rate(lambda r:a0*fine.total(r/rm),axis,e,n,128)*YEAR/MAS
                lowrate=rate(lambda r:a0*coarse.total(r/rm),axis,e,n,64)*YEAR/MAS
                const_rate=rate(lambda r:np.ones_like(r)*a0,axis,e,n,128)*YEAR/MAS
                key=f'{foot}|a{width_kpc}|{planet}'
                out['checks'][key+'|radial_convergence']=abs(full-low)/sigma<1e-5
                out['checks'][key+'|orbit_convergence']=abs(highrate-lowrate)/max(d['EPM'],d['INPOP'])<1e-5
                out['checks'][key+'|B_independent']=abs(gb-bb8)<1e-8
                out['checks'][key+'|ball_convergence']=abs(bb8-bb4)<1e-10
                out['checks'][key+'|series_convergence']=abs(gb-b6)<1e-12
                out['checks'][key+'|plain_control']=abs(plain-plain_independent)/a0<1e-12
                row=dict(planet=planet,width_kpc=width_kpc,a_au=d['a_au'],eccentricity=e,
                         A_over_a0=ga,B_over_a0=gb,total_m_s2=full,plain_m_s2=plain,plain_independent_m_s2=plain_independent,
                         radial_sigma_m_s2=sigma,Z_radial=abs(full)/sigma,radial_margin=2-abs(full)/sigma,
                         radial_refinement_Z=abs(full-low)/sigma,B_ball_over_a0=bb8,B_linear_over_a0=blin,
                         B_ball_absolute_error=abs(gb-bb8),B_ball_relative_error=abs(gb-bb8)/max(abs(gb),1e-300),
                         B_linear_remainder=gb-blin,R_over_filter=R/width,max_i1_argument=float(R/width*24),
                         rate_mas_year=highrate,constant_a0_rate_mas_year=const_rate,
                         rate_sigma_mas_year=max(d['EPM'],d['INPOP']),Z_rate=abs(highrate)/max(d['EPM'],d['INPOP']),
                         rate_margin=2-abs(highrate)/max(d['EPM'],d['INPOP']),rate_refinement_Z=abs(highrate-lowrate)/max(d['EPM'],d['INPOP']))
                ff['rows'].append(row)
                print(foot,'a_kpc',width_kpc,planet,'A/a0',ga,'B/a0',gb,'Zradial',row['Z_radial'],'Zrate',row['Z_rate'],flush=True)
    out['checks']['Newtonian_zero']=rate(lambda r:np.zeros_like(r),1,.093,1,128)==0.
    out['all_checks_pass']=all(out['checks'].values())
    out['label']='SUPPLEMENTARY_RADIAL_AND_MONOPOLE_ORBIT_DIAGNOSTICS_FAIL' if out['all_checks_pass'] and all(r['Z_radial']>2 and r['Z_rate']>2 for f in out['footings'].values() for r in f['rows']) else 'NO_VERDICT'
    out['runtime_seconds']=time.monotonic()-started
    out['scope']='Fixed law,16 planet/width/footing rows; original Cassini/MW grades untouched; monopole diagnostics only, no refitted full ephemeris likelihood.'
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print('all checks',out['all_checks_pass'],'label',out['label'],'seconds',out['runtime_seconds'],flush=True)
    if not out['all_checks_pass']:raise SystemExit(1)


if __name__=='__main__':main()
