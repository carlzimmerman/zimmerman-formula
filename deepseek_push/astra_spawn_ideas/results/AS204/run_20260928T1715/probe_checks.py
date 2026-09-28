import numpy as np
import as204_curved_heat_force as m

leaf = m.S3(6)
rng = np.random.default_rng(204)
b = 0.05
csrc = np.zeros(leaf.n)
for l in range(1, leaf.L + 1):
    csrc[leaf._idx(l)] = rng.standard_normal(leaf.dims[l]) / (l + 1) ** 1.5
gu = leaf.grad(csrc)
csrc /= np.sqrt(float(np.sum(gu ** 2 * leaf.w[None, :])))
H0 = leaf.grad(leaf.heat(csrc, b))
supH = float(np.sqrt(np.max(np.sum(H0 ** 2, axis=0))))
csrc *= 2.3374 / supH
H0 = leaf.grad(leaf.heat(csrc, b))
Hm = np.sqrt(np.sum(H0 ** 2, axis=0))
Fv = (m.h_mono(Hm) / np.where(Hm > 0, Hm, 1.0)) * H0
dFc = np.zeros(leaf.n)
for l in range(1, leaf.L + 1):
    gl = leaf.grad_level(l)
    dFc[leaf._idx(l)] = -np.einsum("jg,jag->a", Fv * leaf.w[None, :], gl)
up = leaf.green(dFc); up[0] = 0.0
P_F = leaf.grad(up)
cstar0 = leaf.coeffs(leaf.values(up))
print("sign test: |grad(cstar0)-P_F|max", float(np.max(np.abs(leaf.grad(cstar0) - P_F))))
print("          |grad(cstar0)+P_F|max", float(np.max(np.abs(leaf.grad(cstar0) + P_F))))
# adjoint identity
Nv = 1.0
cSNu = leaf.heat(leaf.coeffs(Nv * leaf.values(up)), b)
vstar = leaf.values(cSNu) / Nv
print("vstar vs values(heat(up)) max abs", float(np.max(np.abs(vstar - leaf.values(leaf.heat(up, b))))))
Wc = np.zeros(leaf.n)
for l in range(1, leaf.L + 1):
    Wc[leaf._idx(l)] = rng.standard_normal(leaf.dims[l]) / (l + 1)
Wf = leaf.values(Wc)
lhs = float(np.sum(leaf.w * Nv * np.sum(vstar * Wf, axis=0)))
rhs = float(np.sum(leaf.w * np.sum(leaf.values(up) * leaf.values(leaf.heat(Wc, b)), axis=0)))
print("adjoint lhs", lhs, "rhs", rhs, "rel", abs(lhs - rhs) / (abs(lhs) + abs(rhs) + 1e-300))
# raw-form with the same objects
l2 = float(np.sum(leaf.w * leaf.values(up) * leaf.values(leaf.heat(Wc, b))))
r2 = float(np.sum(leaf.w * leaf.values(leaf.heat(up, b)) * leaf.values(Wc)))
print("raw-form lhs", l2, "rhs", r2, "rel", abs(l2 - r2) / (abs(l2) + abs(r2) + 1e-300))
# hessian modal identity for mixed cstar
cstar = leaf.coeffs(vstar)
Hv = leaf.hess_field(cstar)
int_hess = float(np.sum(np.einsum("ijg,ijg->g", Hv, Hv) * leaf.w))
m1 = float(np.sum(leaf.lam ** 2 * cstar ** 2))
m2 = float(np.sum(leaf.lam * (leaf.lam - 2.0) * cstar ** 2))
print("int_hess", int_hess, "vs sum lam^2 c^2", m1, "rel", abs(int_hess - m1) / (m1 + 1e-300))
print("      vs sum lam(lam-2) c^2", m2, "rel", abs(int_hess - m2) / (m2 + 1e-300))