"""3D static branch of the NEW causal medium; reuses only grid/source operators."""
import sys
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'countercharge_action'))
from field import Field as Grid
from medium import dielectric,lagrangian


class CollectiveField(Grid):
    def solve(self,positions,charges,background=False,chi=10.):
        rho,derivatives=self.sources(positions,charges,background);shape=rho.shape
        def objective(flat):
            phi=self.precondition(flat.reshape(shape));E=-self.grad(phi);D=dielectric(E,chi)
            value=np.sum(lagrangian(np.linalg.norm(E,axis=-1),chi)-rho*phi)/(1+chi)
            gradient=self.precondition(self.div(D)-rho)/(1+chi)
            return value,gradient.ravel()
        initial=self.precondition(rho).ravel()/(1+chi)
        sol=minimize(objective,initial,jac=True,method='L-BFGS-B',
                     options={'gtol':1e-10,'ftol':1e-15,'maxiter':500,'maxls':40})
        phi=self.precondition(sol.x.reshape(shape));E=-self.grad(phi);D=dielectric(E,chi)
        ell=lagrangian(np.linalg.norm(E,axis=-1),chi)
        H=float(np.sum(np.sum(E*D,axis=-1)-ell)*self.dv)
        dual=float(np.sum(rho*phi-ell)*self.dv)
        residual=float(np.linalg.norm(self.div(D)-rho)/np.linalg.norm(rho))
        if residual>2e-6:raise RuntimeError(f'{sol.message}: Gauss residual {residual}')
        forces=[(-np.sum(phi[...,None]*der,axis=(0,1,2))*self.dv).tolist() for der in derivatives]
        return dict(N=self.N,chi=chi,energy=H,dual_energy=dual,gauss_relative=residual,
                    duality_relative=abs(H-dual)/max(H,1e-30),forces=forces,
                    total_free_charge=float(rho.sum()*self.dv),max_E=float(np.max(np.linalg.norm(E,axis=-1))),
                    iterations=sol.nit,optimizer_success=bool(sol.success))
