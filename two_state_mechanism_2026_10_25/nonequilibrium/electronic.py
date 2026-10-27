"""Two-center Coulomb Rayleigh-Ritz solver in prolate coordinates."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.special import roots_laguerre,roots_legendre,eval_laguerre,eval_genlaguerre,eval_legendre
from scipy.linalg import eigh

class Electronic:
    def __init__(self,nr,na):
        self.nr=nr;self.na=na
        t,w=roots_laguerre(max(40,2*nr+8));eta,v=roots_legendre(max(64,4*na+8))
        L=np.array([eval_laguerre(i,t) for i in range(nr)])
        DL=np.array([np.zeros_like(t) if i==0 else -eval_genlaguerre(i-1,1,t) for i in range(nr)])-.5*L
        self.t=t;self.w=w;self.L=L;self.DL=DL
        self.eta=eta;self.v=v;self.P=[];self.DP=[]
        for parity in [0,1]:
            degrees=np.arange(parity,2*na,2)
            P=np.array([eval_legendre(l,eta)*np.sqrt((2*l+1)/2) for l in degrees])
            DP=np.array([np.zeros_like(eta) if l==0 else l*(eval_legendre(l-1,eta)-eta*eval_legendre(l,eta))/(1-eta*eta)*np.sqrt((2*l+1)/2) for l in degrees])
            self.P.append(P);self.DP.append(DP)
    def solve(self,R):
        # Fixed hydrogenic exponent: p=R/2, xi=1+t/R. Increasing nr,na removes restriction.
        xi=1+self.t/R;L=self.L;w=self.w
        radial=[(L*(w*xi**n))@L.T for n in range(4)]
        kr=(self.DL*(w*(xi*xi-1)) )@self.DL.T*R*R
        energies=[];coeff=[];res=[]
        for parity in [0,1]:
            P=self.P[parity];DP=self.DP[parity]
            sa=(P*self.v)@P.T;eta2=(P*(self.v*self.eta**2))@P.T
            ka=(DP*(self.v*(1-self.eta**2)))@DP.T
            B=np.kron(radial[2],sa)-np.kron(radial[0],eta2)
            H=2/R**2*(np.kron(kr,sa)+np.kron(radial[0],ka))-4/R*np.kron(radial[1],sa)
            ew,vec=eigh(H,B,subset_by_index=(0,0),check_finite=False,driver='gvx')
            c=vec[:,0];energies.append(float(ew[0]+1/R));coeff.append(c)
            res.append(float(np.linalg.norm(H@c-ew[0]*B@c)/max(np.linalg.norm(H@c),1)))
        angular1=(self.P[0]*(self.v*self.eta))@self.P[1].T
        angular3=(self.P[0]*(self.v*self.eta**3))@self.P[1].T
        dip=R/2*(np.kron(radial[3],angular1)-np.kron(radial[1],angular3))
        return dict(R=float(R),g=energies[0],u=energies[1],dipole=float(abs(coeff[0]@dip@coeff[1])),max_residual=max(res))

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    checks=[]
    for nr,na in [(6,8),(10,14),(14,22),(18,30)]:
        m=Electronic(nr,na)
        checks.append(dict(nr=nr,na=na,rows=[m.solve(R) for R in [.5,1.,2.,4.,8.,16.,32.,64.,120.]]))
        print(nr,na,'R2',checks[-1]['rows'][2],flush=True)
    grid=np.unique(np.r_[np.arange(.2,6.01,.05),np.arange(6.1,16.01,.1),np.arange(16.5,40.01,.5),np.arange(42,120.01,2)])
    curves=[]
    for nr,na in [(10,14),(14,22)]:
        model=Electronic(nr,na);rows=[model.solve(R) for R in grid]
        curves.append(dict(nr=nr,na=na,rows=rows));print('curve',nr,na,len(rows),flush=True)
    result=dict(checks=checks,curves=curves)
    assert max(r['max_residual'] for c in checks for r in c['rows'])<1e-8
    Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
