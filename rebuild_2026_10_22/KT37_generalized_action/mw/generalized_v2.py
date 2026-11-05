"""Covariant finite-volume angular trace fixing v1's radial-symmetry defect.

Htt = Ltheta - cot(theta)/r Dtheta + Dr/r, where Ltheta=Divt Dt is
W-self-adjoint and annihilates angular constants. Hpp is unchanged, so
Htt+Hpp has exactly that compatible angular trace. All complete Hessian
operators retain their weighted transpose in the action derivative.
"""
from generalized import Generalized as _First, M,E,L,np
from scipy.sparse import diags


class Generalized(_First):
    def __init__(self,solver):
        super().__init__(solver)
        g=self.g
        angular=(g.Divt@g.Dt).tocsr()
        connection=diags(np.cos(g.t2d)/(g.r2d*np.sin(g.t2d)))@g.Cth
        htheta=(angular-connection+diags(1/g.r2d)@g.Crr).tocsr()
        self.hess=(self.hess[0],self.hess[1],htheta,self.hess[3])
