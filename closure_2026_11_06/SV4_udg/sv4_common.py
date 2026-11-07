"""SV4 shared helpers: load the record's inputs read-only and solve the action's exact static field.

UD1/UD2 data and baryons, and QX4's density builders, are obtained by executing QX4's iter1_exact_aqual.py up to its
'graded runs' marker in its own namespace (QX4 itself loads UD1/UD2 read-only). No file of UD1/UD2/QX4 is written.
Solver: closure_2026_11_06/QX4_udg/aqual.py (QX8 used it read-only). kappa = 1/2 FITTED; not theory closed.
"""
import contextlib, io, json, os, sys
import numpy as np
from scipy.interpolate import RegularGridInterpolator
from scipy.stats import chi2 as CHI2

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
QX4 = os.path.join(ROOT, "closure_2026_11_06", "QX4_udg")
sys.path.insert(0, QX4)
import aqual as A  # noqa: E402

FOOT = dict(canonical=9.3603e-11, alt=1.1312e-10)
RUNG_TOP, RUNG_LOW = (480, 144), (240, 72)
CONV = A.CONV


def nu(y):
    y = np.maximum(y, 1e-30); return 0.5 + np.sqrt(0.25 + 1.0 / y)


def chi2p(v, e, m):
    c = float(np.sum(((np.asarray(v) - np.asarray(m)) / np.asarray(e)) ** 2)); return c, float(CHI2.sf(c, len(v)))


def load_qx4():
    path = os.path.join(QX4, "iter1_exact_aqual.py")
    src = open(path).read(); cut = src.index("# =================================================================== graded runs")
    ns = dict(__file__=path, __name__="qx4_import")
    old = sys.argv; sys.argv = [path, "main"]
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src[:cut], path, "exec"), ns)
    finally:
        sys.argv = old
    return ns


def qx4_record():
    return json.load(open(os.path.join(QX4, "iter1.json")))


class Field:
    """Exact AQUAL solution on a QX4 grid, with V(R, Z)^2 = R dPhi/dR at fixed Z anywhere in the solved volume."""

    def __init__(self, rho, rmin, rmax, a0_si, rung=RUNG_TOP, mu_one=False, M=None):
        self.g = A.Grid(rmin, rmax, *rung, p=3)
        self.M = self.g.deposit(rho) if M is None else M
        self.Phi, self.res, self.it = A.solve(self.g, self.M, A.a0_kpc(a0_si), mu_one=mu_one)
        g, P = self.g, self.Phi
        dlnr = np.gradient(P, g.xc, axis=0)                       # dPhi/dln r
        # mirror across the plane: theta' = pi - theta, Phi even, dPhi/dtheta odd
        t_ext = np.concatenate([g.tc, (np.pi - g.tc[::-1])])
        P_ext = np.concatenate([P, P[:, ::-1]], axis=1)
        dth = np.gradient(P_ext, t_ext, axis=1)
        dl_ext = np.concatenate([dlnr, dlnr[:, ::-1]], axis=1)
        r = g.rc[:, None]; st = np.sin(t_ext)[None, :]; ct = np.cos(t_ext)[None, :]
        dPdR = st * dl_ext / r + ct * dth / r
        self._dPdR = RegularGridInterpolator((g.xc, t_ext), dPdR, bounds_error=False, fill_value=None)

    def midplane(self, R):
        return A.midplane_vc(self.g, self.Phi, np.asarray(R, float))

    def V_RZ(self, R, Z):
        R = np.asarray(R, float); Z = np.asarray(Z, float)
        r = np.sqrt(R * R + Z * Z); t = np.arctan2(R, np.abs(Z))
        pts = np.stack([np.log(r).ravel(), t.ravel()], axis=1)
        v2 = R.ravel() * self._dPdR(pts)
        return np.sqrt(np.maximum(v2, 0)).reshape(R.shape)


def los_factor(field, rho, Rk, inc_deg, smax_fac=6.0, h=1.0, ns=801):
    """C_k = <rho V(R,Z) x0/R> / <rho V(R,0) x0/R> along the LOS through the major-axis sky point x0 = R_k."""
    i = np.radians(inc_deg); out = []
    for x0 in np.atleast_1d(Rk):
        smax = smax_fac * h / max(np.cos(i), 1e-3)
        s = np.linspace(-smax, smax, ns)
        R = np.sqrt(x0 ** 2 + (s * np.sin(i)) ** 2); Z = s * np.cos(i)
        w = rho(R, Z) * x0 / R
        num = np.trapz(w * field.V_RZ(R, Z), s); den = np.trapz(w * field.V_RZ(R, np.zeros_like(Z)), s)
        out.append(num / den)
    return np.array(out)


class Log:
    def __init__(self): self.lines = []

    def __call__(self, *a):
        s = " ".join(str(x) for x in a); self.lines.append(s); print(s, flush=True)

    def save(self, path, res):
        open(path + ".out", "w").write("\n".join(self.lines) + "\n")
        json.dump(res, open(path + ".json", "w"), indent=1, sort_keys=True, default=float)
