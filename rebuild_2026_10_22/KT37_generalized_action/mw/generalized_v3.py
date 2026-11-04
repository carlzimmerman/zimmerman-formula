"""Same compatible FV Hessian as v2, evaluated in factored stable form.

Angular stiffness Ktheta=-Dt.T Wface Dt is symmetric by construction;
Ltheta=W^-1 Ktheta. Scalar angular differences and tangential-stress
differences are formed before large weighted sums, preserving radial symmetry.
"""
from generalized import Generalized as _First, M,E,L,np
from scipy.sparse import diags


class Generalized(_First):
    def __init__(self,solver):
        super().__init__(solver)
        g=self.g
        area=np.pi*(g.re[1:]**2-g.re[:-1]**2)[:,None]*np.sin(g.te[1:-1])[None,:]
        distance=g.rc[:,None]*(g.tc[1:]-g.tc[:-1])[None,:]
        self.face_weight=(area*distance).ravel()
        self.angular_stiffness=(-g.Dt.T@diags(self.face_weight)@g.Dt).tocsr()
        angular=diags(1/g.vol)@self.angular_stiffness
        self.connection=np.cos(g.t2d)/(g.r2d*np.sin(g.t2d))
        htheta=(angular-diags(self.connection)@g.Cth+diags(1/g.r2d)@g.Crr).tocsr()
        self.hess=(self.hess[0],self.hess[1],htheta,self.hess[3])

    def angular_apply(self,value):
        g=self.g
        return -(g.Dt.T@(self.face_weight*(g.Dt@value)))/g.vol

    def fields(self,psi):
        g=self.g;dr,dt=g.Crr,g.Cth
        gr=dr@psi;gt=dt@psi
        radial=gr/g.r2d;connection=self.connection*gt
        return np.array([gr,gt]),np.array([
            dr@gr,
            .5*(dt@gr-gt/g.r2d+dr@gt),
            self.angular_apply(psi)-connection+radial,
            radial+connection])

    def source(self,psi,ell,newtonian=False,fields=None):
        gg,hh=self.fields(psi) if fields is None else fields
        A,B,e,z=self.coefficients(gg,hh,ell,newtonian)
        g=self.g;w=g.vol;dr,dt=g.Crr,g.Cth
        first=dr.T@(w*A[0])+dt.T@(w*A[1])
        wr=w*B[0];cross=w*B[1]
        second=dr.T@(dr.T@wr)
        # Mixed component occurs twice; its symmetrized 1/2 cancels that two.
        second+=dr.T@(dt.T@cross)+dt.T@(dr.T@cross-cross/g.r2d)
        second-=g.Dt.T@(self.face_weight*(g.Dt@B[2]))
        second+=dt.T@(w*self.connection*(B[3]-B[2]))
        second+=dr.T@(w*(B[2]+B[3])/g.r2d)
        source=-(first+second)/w
        return source,dict(energy=-float(w@e)/(8*np.pi),
            gradient_source_norm=float(np.linalg.norm(first/w)),hessian_source_norm=float(np.linalg.norm(second/w)),
            z_min=float(z.min()),z_max=float(z.max()),finite=bool(np.all(np.isfinite(source))))
