"""KT39 energy with curvature alone heat filtered; full finite adjoint."""
from pathlib import Path
import sys
sys.dont_write_bytecode = True
RB = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RB/'KT39_power_curvature/mw'))
import power_model as J
from refine import grid
from scipy.sparse import eye
from scipy.sparse.linalg import splu
M, E, L, np = J.M, J.E, J.L, J.np


class Heat:
    """Backward-Euler approximation of Gaussian heat, and exact W adjoint."""
    def __init__(self, g, width, steps=16):
        if width < 0 or steps < 1:
            raise ValueError('nonnegative physical width and positive steps required')
        self.g, self.width, self.steps = g, width, steps
        self.lu = None if width == 0 else splu(
            (eye(g.n, format='csc')-width**2/(2*steps)*g.Lap).tocsc())

    def forward(self, value):
        value = np.array(value, copy=True)
        if self.lu is not None:
            for _ in range(self.steps):
                value = self.lu.solve(value)
        return value

    def adjoint(self, value):
        if self.lu is None:
            return np.array(value, copy=True)
        value = np.array(self.g.vol*value, copy=True)
        for _ in range(self.steps):
            value = self.lu.solve(value, trans='T')
        return value/self.g.vol


class Filtered(J.PowerCurvature):
    def __init__(self, solver, width, steps=16):
        super().__init__(solver)
        self.filter = Heat(self.g, width, steps)

    def fields(self, psi):
        gg, _ = super().fields(psi)
        _, hh = super().fields(self.filter.forward(psi))
        return gg, hh

    def source(self, psi, ell, newtonian=False, fields=None):
        gg, hh = self.fields(psi) if fields is None else fields
        A, B, e, z = self.coefficients(gg, hh, ell, newtonian)
        g = self.g; w = g.vol; dr, dt = g.Crr, g.Cth
        first = dr.T@(w*A[0])+dt.T@(w*A[1])
        wr = w*B[0]; cross = w*B[1]
        second = dr.T@(dr.T@wr)
        second += dr.T@(dt.T@cross)+dt.T@(dr.T@cross-cross/g.r2d)
        second -= g.Dt.T@(self.face_weight*(g.Dt@B[2]))
        second += dt.T@(w*self.connection*(B[3]-B[2]))
        second += dr.T@(w*(B[2]+B[3])/g.r2d)
        # Hbar = H T psi: transpose order is T* H*, not H* alone.
        source = -first/w-self.filter.adjoint(second/w)
        return source, dict(energy=-float(w@e)/(8*np.pi),
            gradient_source_norm=float(np.linalg.norm(first/w)),
            hessian_source_norm=float(np.linalg.norm(self.filter.adjoint(second/w))),
            z_min=float(z.min()), z_max=float(z.max()),
            finite=bool(np.all(np.isfinite(source))))
