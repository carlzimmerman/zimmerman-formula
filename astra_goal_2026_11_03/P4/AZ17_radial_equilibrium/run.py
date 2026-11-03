from pathlib import Path
import sys
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from record import record

class Grid:
    def __init__(self,n,R):
        self.n=n;self.R=R;e=np.linspace(0,R,n+1);a=e[:-1];b=e[1:];self.r=(a+b)/2
        self.vol=4*np.pi/3*(b**3-a**3)
        self.A=1.5*(b*b-a*a)/(b**3-a**3)
        self.B=3*((b**5-a**5)/5-a**3*(b*b-a*a)/2)/(b**3-a**3)**2
        self.c=4*np.pi*e[1:]**2/np.r_[np.diff(self.r),R-self.r[-1]]**3
        self.r2=.6*(b**5-a**5)/(b**3-a**3)
    def binding(self,m,mutate=False):
        prev=np.cumsum(m)-m
        W=-np.sum(self.A*m*prev+self.B*m*m)
        outer=np.cumsum((self.A*m)[::-1])[::-1]-self.A*m
        pot=-(self.A*prev+(1 if mutate else 2)*self.B*m+outer)
        return W,pot
    def evaluate(self,u,mutate=False,details=False):
        S=np.dot(self.vol,u**4);scale=S**(-.25);p=u*scale;m=self.vol*p**4
        delta=np.diff(np.r_[p,0.]);F=np.sum(self.c*delta**4)
        face=4*self.c*delta**3;g=-face.copy();g[1:]+=face[:-1]
        W,pot=self.binding(m,mutate);g+=4*self.vol*p**3*pot
        gu=scale*(g-self.vol*p**3*np.dot(g,p))
        if details:return F,W,p,m,gu
        return F+W,gu

def calculate():
    g=Grid(16,5);u=np.exp(-g.r*g.r/8)+.01;direction=np.cos(g.r*.7)+.3
    E,grad=g.evaluate(u);_,bad=g.evaluate(u,True)
    fd=[(g.evaluate(u+h*direction)[0]-g.evaluate(u-h*direction)[0])/(2*h) for h in [1e-5,5e-6]]
    analytic=np.dot(grad,direction);mutation=np.dot(bad,direction)
    grad_error=max(abs(np.array(fd)/analytic-1));mut_error=abs(mutation/fd[-1]-1)
    uniform=g.vol/sum(g.vol);uniformW=g.binding(uniform)[0]
    checks=[('uniform sphere exact binding',abs(uniformW/(-3/(5*g.R))-1)<=1e-12),('normalized energy gradient',grad_error<=1e-5),('MUTATE self derivative rejected',mut_error>1e-3)]
    rows=[];previous=None;stored512=None
    for n,R in [(256,20),(512,20),(1024,20),(512,30)]:
        grid=Grid(n,R)
        initial=previous if R==20 else stored512
        u=np.exp(-grid.r**2/4) if initial is None else np.interp(grid.r,initial[0],initial[1],right=0)
        u=u/np.dot(grid.vol,u**4)**.25
        sol=minimize(grid.evaluate,u,jac=True,method='L-BFGS-B',bounds=[(0,None)]*n,options={'maxiter':4000,'maxls':40,'ftol':1e-15,'gtol':1e-8,'maxcor':20})
        F,W,p,m,gu=grid.evaluate(sol.x,details=True)
        projected=gu.copy();projected[(sol.x<=1e-14)&(gu>0)]=0
        row={'N':n,'outer':R,'optimizer_success':bool(sol.success),'message':str(sol.message),'iterations':int(sol.nit),'energy':float(F+W),'F':float(F),'W':float(W),'mass_error':float(abs(sum(m)-1)),'virial_residual':float(abs(4*F+W)/abs(W)),'projected_gradient':float(max(abs(projected))),'rms_radius':float(np.sqrt(np.dot(m,grid.r2))),'outer_last_10pct_mass':float(sum(m[grid.r>.9*R]))}
        rows.append(row);previous=(grid.r,p)
        if n==512 and R==20:stored512=previous
        print('completed',n,R,row['optimizer_success'],row['virial_residual'],flush=True)
    for r in rows:
        tag=str(r['N'])+'/'+str(r['outer'])
        checks.extend([(tag+' optimizer',r['optimizer_success'] and r['projected_gradient']<1e-5),(tag+' mass',r['mass_error']<1e-12),(tag+' virial',r['virial_residual']<.005)])
    changes={}
    for tag,a,b in [('mesh',rows[1],rows[2]),('boundary',rows[1],rows[3])]:
        changes[tag]={k:abs(b[k]/a[k]-1) for k in ['energy','rms_radius']}
        checks.append((tag+' refinement',max(changes[tag].values())<.01))
    B=1/(2*np.sqrt(np.pi));rs=(120*np.sqrt(np.pi)/256)**(1/3);upper=-3*B/(4*rs)
    checks.append(('Gaussian upper bound',rows[2]['energy']<=upper+.001*abs(upper)))
    checks=[{'name':k,'passed':bool(v)} for k,v in checks];label='PASS' if all(c['passed'] for c in checks) else 'NO VERDICT'
    return {'assertion_tested':'Resolved radial variational stationary candidate for the pure quartic-gradient energy','label':label,'footings':{k:{'label':label,'scope':'Synthetic equilibrium only; a0 cancels','empirical_rows':'NOT EVALUABLE'} for k in ['canonical','alt']},'checks':checks,'bounds':{'grids':[[r['N'],r['outer']] for r in rows],'maxiter':4000,'units':'G=M=256lambda=1'},'runs':rows,'refinement_changes':changes,'controls':{'uniform_binding':uniformW,'gradient_relative_error':float(grad_error),'MUTATE_relative_error':float(mut_error),'Gaussian_upper_bound':float(upper)},'free_physical_numbers':['lambda physical value FITTED undetermined','total field mass and initial state undetermined FITTED if selected','kappa=.5 FITTED'],'residual_risks':['Radial energy stationary candidate only; no global uniqueness or nonradial stability proof','Finite box and discretized density','No time evolution, baryonic well, covariant completion or empirical contraction prediction']}
if __name__=='__main__':record(__file__,calculate)
