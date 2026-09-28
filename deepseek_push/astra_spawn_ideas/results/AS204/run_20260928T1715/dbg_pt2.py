import numpy as np
import as204_curved_heat_force as m

leaf = m.S3(4)
c = np.zeros(leaf.n)
ic = leaf._idx(2)
c[ic.start] = 1.0
g0 = 3
xx = leaf.x[g0]

gA = leaf.grad_ambient(c)
Hv = leaf.hess_field(c)
gAx = np.einsum("jg,jg->g", gA, leaf.x.T)
Hxx = np.einsum("ijg,jg->ig", Hv, leaf.x.T)
J = -Hv.copy()
for i in range(4):
    J[:, i, :] += (Hxx[i][None, :] + gA[i][None, :]) * leaf.x.T
    J[i, i, :] += gAx

Jx = J[:, :, g0] @ leaf.x[g0]
tr = float(np.sum(J[:, :, g0] ** 2))
xxf = float(np.sum(Jx * Jx))
xJx = float(Jx @ xx)
formula = tr - 2.0 * xxf + xJx * xJx
print("point", g0, "x", np.round(xx, 4))
print("Tr", tr, "||Jx||^2", xxf, "xJx", xJx, "formula", formula)

# direct: ON frame tangent basis
Tb = np.eye(4) - np.outer(xx, xx)
uu, _ = np.linalg.qr(Tb)
uu = uu[:, :3]
eps = 1e-5

def grad_ambient_at(cv, pts):
    pts = np.atleast_2d(pts)
    Gp = pts.shape[0]
    gl = [np.zeros((4, 1, Gp))]
    # basis values at pts
    Vs = [np.ones((1, Gp))]
    for l in range(1, leaf.L + 1):
        vp = Vs[-1]
        nl = vp.shape[0]
        cand = np.stack([pts[:, i, None] * vp.T for i in range(4)], axis=1).reshape(Gp, 4 * nl)
        Vs.append(leaf.Q[l] @ cand.T)
        cg = np.zeros((4, 4 * nl, Gp))
        for i in range(4):
            seg = slice(i * nl, (i + 1) * nl)
            cg[:, seg, :] = np.where(np.arange(4)[:, None, None] == i, vp[None, :, :], 0.0)
            cg[:, seg, :] += pts[:, i][None, None, :] * gl[-1]
        gl.append(np.einsum("ab,jbg->jag", leaf.Q[l], cg))
    g = np.zeros((4, Gp))
    for l in range(1, leaf.L + 1):
        cc = cv[leaf._idx(l)]
        if np.any(cc):
            g += np.einsum("a,jag->jg", cc, gl[l])
    return g

def Aext(p):
    gp_ = grad_ambient_at(c, p)[:, 0]
    return -(gp_ - (gp_ @ p) * p)

val = 0.0
terms = []
for a in range(3):
    u = uu[:, a]
    xpp = xx + eps * u; xpm = xx - eps * u
    xpp /= np.linalg.norm(xpp); xpm /= np.linalg.norm(xpm)
    duA = (Aext(xpp) - Aext(xpm)) / (2 * eps)
    duA = duA - np.dot(duA, xx) * xx
    terms.append(float(np.sum(duA ** 2)))
    val += terms[-1]
print("direct val", val, "terms", terms)
print("rel gap", abs(val - formula) / (abs(val) + 1e-30))
# isolate pieces: derivative of -g  and of +(g.x)x
def A1(p):
    return -grad_ambient_at(c, p)[:, 0]
def A2(p):
    gp_ = grad_ambient_at(c, p)[:, 0]
    return (gp_ @ p) * p
u = uu[:, 0]
xpp = (xx + eps * u); xpm = (xx - eps * u)
xpp /= np.linalg.norm(xpp); xpm /= np.linalg.norm(xpm)
dA1 = (A1(xpp) - A1(xpm)) / (2 * eps)
dA2 = (A2(xpp) - A2(xpm)) / (2 * eps)
print("FD d(-g)    =", np.round(dA1, 6))
print("-(Hess.u)   =", np.round(-(Hv[:, :, g0] @ u), 6))
print("FD d((g.x)x)=", np.round(dA2, 6))
g0v = gA[:, g0]
Hessx = Hv[:, :, g0] @ xx
gx = float(g0v @ xx)
term2 = (Hessx + g0v) * (xx @ u) * 0 + ((Hessx + g0v) * u) * np.array([1, 1, 1, 1])  # placeholder
# analytic: d/dx[(g.x)x] = (Hess.u . x + g.u)x + (g.x)u
a = (Hv[:, :, g0] @ u) @ xx + g0v @ u
an2 = a * xx + gx * u
print("analytic    =", np.round(an2, 6))
print("g.x =", gx, " g.u =", float(g0v @ u), "  (Hess.u).x =", float((Hv[:, :, g0] @ u) @ xx))