"""Conservative collective mass coordinate coupled to a live homogeneous field."""
import argparse,json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
CHI=11.220184543019636

def run(N,I,rtol=1e-8,method='DOP853',lam=.5,ti=.1,ef=.01):
    T=20*np.sqrt(I)
    u,w=np.polynomial.legendre.leggauss(N);u=(u+1)/2;w=CHI*u*w/2
    k=CHI/lam;D=ef+CHI*ef/(np.hypot(1,ef)+ef)
    def pol(E):
        rr=np.sqrt(u*u+1+E*E);return w@(E/rr*np.tanh(rr/(2*ti)))
    E0=brentq(lambda E:E+pol(E)-D,0,D,xtol=1e-14)
    b=np.column_stack((u,np.ones(N),np.full(N,-E0)));rr=np.linalg.norm(b,axis=1)
    L=np.tanh(rr/(2*ti));r=-b/rr[:,None]*L[:,None]
    initial=np.r_[r.ravel(),1.,0.]
    def fun(t,y):
        r=y[:-2].reshape(N,3);m,p=y[-2:];E=D-w@r[:,2]
        b=np.column_stack((u,np.full(N,m),np.full(N,-E)))
        return np.r_[(2*np.cross(b,r)).ravel(),p/I,-k*m-w@r[:,1]]
    sol=solve_ivp(fun,(0,T),initial,method=method,rtol=rtol,atol=rtol*.01,t_eval=np.linspace(0,T,1001))
    assert sol.success and abs(sol.t[-1]-T)<1e-12
    a=sol.y[:-2].T.reshape(-1,N,3);m=sol.y[-2];p=sol.y[-1];E=D-a[:,:,2]@w
    energy=E*E/2+a[:,:,0]@(w*u)+m*(a[:,:,1]@w)+k*m*m/2+p*p/(2*I)
    refenergy=ef*ef/2-w@(u*u/np.hypot(u,ef))
    excess=energy[0]-refenergy
    return dict(N=N,I=I,coupling=lam,T=float(T),rtol=rtol,method=method,nfev=sol.nfev,
        initial_field=float(E0),D=float(D),reference_nodal_field=ef,
        initial_energy=float(energy[0]),reference_energy=float(refenergy),initial_energy_excess=float(excess),
        excess_per_occupied_weight=float(excess/sum(w)),maximum_relative_energy_error=float(max(abs(energy-energy[0]))/max(1,abs(energy[0]))),
        maximum_length_error=float(np.max(abs(np.linalg.norm(a,axis=2)-L[None,:]))),
        final_mass=float(m[-1]),last_fifth_mass_RMS=float(np.sqrt(np.mean(m[-201:]**2))),
        final_field=float(E[-1]),last_fifth_mean_field=float(np.mean(E[-201:])),
        last_fifth_field_RMS=float(np.sqrt(np.mean(E[-201:]**2))),
        trace=dict(t=sol.t.tolist(),mass=m.tolist(),field=E.tolist(),energy=energy.tolist()))

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    rows=[run(32,I) for I in [1.,100.,10000.]]
    refinement=[run(N,100.,tol,method) for N,tol,method in [(32,1e-10,'DOP853'),(64,1e-10,'DOP853'),(32,1e-10,'RK45')]]
    assert max(r['maximum_relative_energy_error'] for r in rows+refinement)<1e-5
    with open(a.output,'w') as f:json.dump(dict(runs=rows,refinement=refinement),f,indent=2,allow_nan=False)
    print(json.dumps([{k:v for k,v in r.items() if k!='trace'} for r in rows+refinement]))
if __name__=='__main__':main()
