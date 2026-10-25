"""BO radial levels and energy-normalized dipole continuum, no fitted rates."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.linalg import eigh_tridiagonal
from scipy.special import spherical_jn,spherical_yn
BASE=Path(__file__).resolve().parent
MU=50.;MUAX=100.*101/201

class Curves:
    def __init__(self,order=1,join=40.):
        data=json.loads((BASE/'run_electronic/results.json').read_text())['curves'][order]['rows']
        self.join=join
        r=np.array([x['R'] for x in data]);self.s={k:CubicSpline(r,[x[k] for x in data]) for k in ['g','u','dipole']}
    def value(self,r,key):
        r=np.asarray(r);z=self.s[key](np.clip(r,.2,self.join))
        if key=='dipole':
            # Polarization correction vanishes at infinity; match value at join.
            tail=r/2+(self.s[key](self.join)-self.join/2)*(self.join/r)**2
        else:
            # Hydrogenic polarization tail -alpha_pol/(2R^4), alpha_pol=9/2.
            # C6 is fixed by continuity at join, not fitted to an environment.
            c6=(self.s[key](self.join)+.5+2.25/self.join**4)*self.join**6
            tail=-.5-2.25/r**4+c6/r**6
            z=np.where(r<.2,1/r+(self.s[key](.2)-5),z)
        return np.where(r>self.join,tail,z)

def levels(curves,h=.02,L=120.):
    r=np.arange(h,L,h);off=np.full(len(r)-1,-1/(2*MU*h*h));rows=[];waves=[]
    for J in range(40):
        v=curves.value(r,'g')+.5+J*(J+1)/(2*MU*r*r)
        if min(v)>=0:break
        e,w=eigh_tridiagonal(v+1/(MU*h*h),off,select='v',select_range=(-1,-1e-10),check_finite=False)
        for i,E in enumerate(e):
            rows.append(dict(J=J,v=i,D=float(-E),weight=2*J+1));waves.append(w[:,i]/np.sqrt(h))
    return r,rows,np.array(waves)

def continuum(curves,h,L,energies,rows,waves,r):
    """Numerov regular solutions; match exact free spherical Bessel pair."""
    strength=np.zeros((len(rows),len(energies)));tail_errors=[]
    n=int(round(L/h));rr=np.arange(1,n+1)*h
    pot=curves.value(rr,'u')+.5
    dip=curves.value(r,'dipole');k=np.sqrt(2*MU*energies)
    for J in range(max(x['J'] for x in rows)+2):
        ids=[i for i,x in enumerate(rows) if abs(x['J']-J)==1]
        if not ids:continue
        weights=np.array([(rows[i]['J']+1 if J>rows[i]['J'] else rows[i]['J'])/(2*rows[i]['J']+1) for i in ids])
        integrands=waves[ids]*dip
        v=pot+J*(J+1)/(2*MU*rr**2)
        # Leading regular Coulomb solution, arbitrary common amplitude.
        a=np.ones(len(k));b=np.full(len(k),2.**(J+1)*(1+MU*2*h/(J+1))/(1+MU*h/(J+1)))
        overlap=h*(integrands[:,0,None]*a+integrands[:,1,None]*b)
        last=[a.copy(),b.copy()]
        q0=2*MU*(energies-v[0]);q1=2*MU*(energies-v[1]);fac=h*h/12
        for idx in range(2,n):
            q2=2*MU*(energies-v[idx])
            c=(2*(1-5*fac*q1)*b-(1+fac*q0)*a)/(1+fac*q2)
            if idx<len(r):overlap+=h*integrands[:,idx,None]*c
            a,b=b,c;q0,q1=q1,q2
            if idx>=n-5:last.append(c.copy())
        y=np.array(last[-5:]);der=(25*y[-1]-48*y[-2]+36*y[-3]-16*y[-4]+3*y[-5])/(12*h)
        z=k*rr[-1];f=z*spherical_jn(J,z);g=z*spherical_yn(J,z)
        fp=k*(spherical_jn(J,z)+z*spherical_jn(J,z,True));gp=k*(spherical_yn(J,z)+z*spherical_yn(J,z,True))
        A=(b*gp-der*g)/k;B=(der*f-b*fp)/k
        norm=np.sqrt(2*MU/(np.pi*k))/np.hypot(A,B)
        strength[ids]+=weights[:,None]*(overlap*norm)**2
    return strength

def run(h=.02,L=800.,ne=640,order=1,join=40.):
    curves=Curves(order,join);r,rows,w=levels(curves,h)
    en=np.geomspace(1e-10,2.,ne)
    s=continuum(curves,h,L,en,rows,w,r)
    ts=np.geomspace(1e-7,.08,100)
    rates=[];means=[]
    for T in ts:
        D=np.array([x['D'] for x in rows])[:,None];deg=np.array([x['weight'] for x in rows])
        q=(en[None,:]+D)**3*s*np.exp(-en[None,:]/T)
        integ=np.trapz(q,en,axis=1)
        rates.append((4/3*deg*(2*np.pi/MUAX)**1.5*T**-1.5*integ).tolist())
        means.append((np.trapz(q*en,en,axis=1)/np.maximum(integ,1e-300)).tolist())
    assert np.all(np.isfinite(s)) and np.min(s)>=0
    return dict(h=h,match_radius=L,ne=ne,electronic_order=order,tail_join=join,levels=rows,energies=en.tolist(),strength=s.tolist(),temperatures=ts.tolist(),k_over_alpha3=rates,mean_incident_energy=means)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--h',type=float,default=.02);p.add_argument('--match',type=float,default=800);p.add_argument('--ne',type=int,default=640);p.add_argument('--order',type=int,default=1);p.add_argument('--join',type=float,default=40);a=p.parse_args()
    d=run(a.h,a.match,a.ne,a.order,a.join)
    Path(a.output).write_text(json.dumps(d)+'\n')
    print('levels',len(d['levels']),'ground',d['levels'][0],'total k/alpha^3 endpoints',np.sum(d['k_over_alpha3'],axis=1)[[0,-1]])
if __name__=='__main__':main()
