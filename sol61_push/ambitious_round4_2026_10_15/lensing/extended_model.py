import argparse,json,time
from model import *
from scipy.optimize import brentq

def mbfun(x,u):
    x=np.asarray(x);return x**3/(x*x+u*u)**1.5

def mexfun(x,u):
    m=mbfun(x,u);return .5*(np.sqrt(m*m+4*x*x*m)-m)

def dmex(x,u):
    x=np.asarray(x);m=mbfun(x,u);mp=3*x*x*u*u/(x*x+u*u)**2.5
    return .5*((2*m*mp+8*x*m+4*x*x*mp)/(2*np.sqrt(m*m+4*x*x*m))-mp)

def extended(lm,rb,r,order=64):
    old,n,mt,e0,rm=edge(lm);u=rb*1e6/rm
    e=e0 if u==0 else brentq(lambda xx:float(mexfun(xx,u))-SUP*n,e0,e0+10*u+1,xtol=1e-11)
    x=np.asarray(r)*1e6/rm
    cold=SUP*n/(np.pi*x*x);inside=x<e
    if np.any(inside):
        xx=x[inside];umax=np.arccosh(e/xx);nodes,w=GL(order)
        tt=(nodes[None,:]+1)*umax[:,None]/2;radius=xx[:,None]*np.cosh(tt);deriv=dmex(radius,u)
        sig=np.sum(w*deriv/radius,axis=1)*umax/(4*np.pi)
        caps=np.sum(w*deriv*xx[:,None]*np.sinh(tt)**2/np.cosh(tt),axis=1)*umax/2
        cold[inside]=(SUP*n-caps)/(np.pi*xx**2)-sig
    bary=x*x/(np.pi*(x*x+u*u)**2)
    return (cold+bary)*10**lm/rm**2,e*rm/1e6

class ExtFitter(Fitter):
    def predict(self,pars):
        ones=[];twos=[];edges=[]
        for b,lm in enumerate(pars[:4]):
            rb=pars[4+b];one,ex=extended(lm,rb,self.r[b]);ones.append(one)
            twos.append(np.array([v(ex) for v in self.interp]));edges.append(ex)
        ov=np.array(ones).ravel();tv=np.zeros((60,4))
        for b,t in enumerate(twos):tv[b*15:(b+1)*15,b]=t
        wo=solve_triangular(self.chol,ov,lower=True);wt=solve_triangular(self.chol,tv,lower=True)
        bias=nnls(wt,self.wy-wo)[0];res=self.wy-wo-wt@bias
        return res,ov,tv,bias,edges

