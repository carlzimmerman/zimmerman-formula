#!/usr/bin/env python3
"""r01_ball_geometry.py -- Jacobson (arXiv:1505.04753) small-ball geometry with every numeric factor tracked and verified.

Claims verified (n = d-1 spatial dimensions; l = geodesic radius; R = spatial Ricci scalar at the centre; Omega_k = area of the unit k-sphere):
 G1  exact spheres/hyperboloids S^n(L), H^n(L):  A = Omega_{n-1} l^{n-1} [1 - R l^2/(6n)],  V = Omega_{n-1} l^n/n [1 - R l^2/(6(n+2))]   (n = 2..7)
 G2  anisotropic exact examples S^2(a) x R^{n-2}: same coefficients with R = 2/a^2 (only the scalar curvature enters)
 G3  random algebraic Riemann tensors (Kulkarni-Nomizu squares, Lorentzian, d = 4,5,6): first Bianchi holds; R_slice = R_ijij = 2 G_00 (K = 0 slice);
     the Riemann-normal-coordinate metric h_ij = delta_ij - (1/3) R_ikjl x^k x^l gives A and V of the coordinate ball with the SAME coefficients (numerical quadrature)
 G4  symbolic chain in general d:  dV|_l = -Omega l^{d+1} R/(6(d-1)(d+1)),  dA|_l = d(dV)/dl,  dA|_V = dA - (d-2) dV/l = -Omega l^d R/(2(d^2-1)) = -Omega l^d G_00/(d^2-1)
     and dA|_V / dA|_l = 3/(d+1) (the paper's remark)
 G5  CONTROLS: a wrong ball-volume coefficient 1/(6(n+1)) (instead of 1/(6(n+2))) is REJECTED by G1 and changes the derived Einstein coefficient away from 8 pi;
     dropping the fixed-volume correction changes it by (d+1)/3 (the paper's remark) -- both detected.
Exit 0 = all pass.
"""
import sys
import numpy as np
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")
def must_fail(name, cond):
    ok.append(not bool(cond)); print(f"  [{'OK' if not cond else 'FAIL'}] CONTROL (wrong claim must be rejected): {name}")

def Om(k):   # area of the unit k-sphere in R^{k+1}
    return 2 * sp.pi ** sp.Rational(k + 1, 2) / sp.gamma(sp.Rational(k + 1, 2))

l, L = sp.symbols('l L', positive=True)
s = sp.symbols('s', positive=True)

# ------------------------------------------------------------------------------------------------ G1
print("G1  exact constant-curvature balls (sympy series)")
for n in range(2, 8):
    for name, fn, Rs in (("S^n", sp.sin, sp.Integer(n * (n - 1)) / L**2), ("H^n", sp.sinh, -sp.Integer(n * (n - 1)) / L**2)):
        A = Om(n - 1) * (L * fn(l / L)) ** (n - 1)
        integrand = Om(n - 1) * (L * fn(s / L)) ** (n - 1)
        Vser = sp.integrate(sp.series(integrand, s, 0, n + 3).removeO(), (s, 0, l))
        cA = sp.simplify(sp.series(A, l, 0, n + 2).removeO() / (Om(n - 1) * l ** (n - 1)) - (1 - Rs * l**2 / (6 * n)))
        cV = sp.simplify(Vser / (Om(n - 1) * l**n / n) - (1 - Rs * l**2 / (6 * (n + 2))))
        # remainder must start at l^4
        cA_ok = sp.simplify(sp.series(cA, l, 0, 4).removeO()) == 0
        cV_ok = sp.simplify(sp.series(cV, l, 0, 4).removeO()) == 0
        check(f"{name} n={n}: A and V coefficients -R/(6n), -R/(6(n+2)) with R = +-n(n-1)/L^2", cA_ok and cV_ok)
        if name == "S^n" and n == 3:
            # control: the mutated volume coefficient must be rejected
            cVm = sp.simplify(sp.series(Vser / (Om(n - 1) * l**n / n) - (1 - Rs * l**2 / (6 * (n + 1))), l, 0, 4).removeO())
            must_fail("G5a S^3 volume with coefficient 1/(6(n+1))", cVm == 0)

# ------------------------------------------------------------------------------------------------ G2
print("G2  anisotropic exact examples: only the scalar curvature enters")
a = sp.symbols('a', positive=True)
psi, u, z = sp.symbols('psi u z', positive=True)
# n = 3: S^2(a) x R.  distance^2 = (a theta)^2 + z^2.  sphere u = l sin(psi), z = l cos(psi); dA = 2 pi a sin(u/a) * l dpsi
A3 = 2 * sp.pi * a * l * sp.integrate(sp.series(sp.sin(l * sp.sin(psi) / a), l, 0, 6).removeO(), (psi, 0, sp.pi))
A3s = sp.expand(sp.series(sp.expand(A3), l, 0, 5).removeO())
target3 = sp.expand(4 * sp.pi * l**2 * (1 - (2 / a**2) * l**2 / (6 * 3)))
check("S^2(a) x R (n=3): A = 4 pi l^2 [1 - l^2/(9 a^2)]  (R = 2/a^2)", sp.simplify(A3s - target3) == 0)
# volume: int 2 pi a sin(u/a) du dz over u^2+z^2<=l^2, polar coordinates (rho, psi), u = rho sin(psi), z = rho cos(psi), psi in [0,pi]
rho = sp.symbols('rho', positive=True)
integ = 2 * sp.pi * a * sp.series(sp.sin(rho * sp.sin(psi) / a), rho, 0, 6).removeO() * rho
V3 = sp.integrate(sp.integrate(sp.expand(integ), (psi, 0, sp.pi)), (rho, 0, l))
V3s = sp.expand(V3)
target3V = sp.expand(sp.Rational(4, 3) * sp.pi * l**3 * (1 - (2 / a**2) * l**2 / (6 * 5)))
check("S^2(a) x R (n=3): V = (4 pi/3) l^3 [1 - l^2/(15 a^2)]  (R = 2/a^2, n+2 = 5)", sp.simplify(sp.series(V3s - target3V, l, 0, 6).removeO()) == 0)
# n = 4: S^2(a) x R^2.  sphere: u = l sin(psi), |z| = l cos(psi), psi in [0,pi/2];  dA = 4 pi^2 a sin(u/a) |z| l dpsi
A4 = 4 * sp.pi**2 * a * l**2 * sp.integrate(sp.series(sp.sin(l * sp.sin(psi) / a), l, 0, 6).removeO() * sp.cos(psi), (psi, 0, sp.pi / 2))
A4s = sp.expand(sp.series(sp.expand(A4), l, 0, 6).removeO())
target4 = sp.expand(2 * sp.pi**2 * l**3 * (1 - (2 / a**2) * l**2 / (6 * 4)))
check("S^2(a) x R^2 (n=4): A = 2 pi^2 l^3 [1 - l^2/(12 a^2)]", sp.simplify(A4s - target4) == 0)
# flat control: R^3 with a periodic direction has R = 0 -> no l^2 correction (trivially exact); mutated: claim R = 3/a^2 must fail
target3m = sp.expand(4 * sp.pi * l**2 * (1 - (3 / a**2) * l**2 / (6 * 3)))
must_fail("G2c S^2(a) x R with a wrong scalar curvature 3/a^2", sp.simplify(A3s - target3m) == 0)

# ------------------------------------------------------------------------------------------------ G3
print("G3  random algebraic curvature tensors in d = 4, 5, 6 (Lorentzian): R_slice = 2 G_00, RNC ball coefficients")
rng = np.random.default_rng(20260929)

def kn(h, k):   # Kulkarni-Nomizu product (h ^ k)_{abcd} = h_ac k_bd + h_bd k_ac - h_ad k_bc - h_bc k_ad
    return (np.einsum('ac,bd->abcd', h, k) + np.einsum('bd,ac->abcd', h, k)
            - np.einsum('ad,bc->abcd', h, k) - np.einsum('bc,ad->abcd', h, k))

def random_riemann(d):
    Rm = np.zeros((d,) * 4)
    for _ in range(4):
        h = rng.normal(size=(d, d)); h = h + h.T
        Rm += rng.normal() * kn(h, h)
    return Rm   # all indices down

for d in (4, 5, 6):
    n = d - 1
    eta = np.diag([-1.0] + [1.0] * n)
    Rm = random_riemann(d)
    bianchi = Rm + np.einsum('abcd->acdb', Rm) + np.einsum('abcd->adbc', Rm)
    check(f"d={d}: first Bianchi identity R_a[bcd] = 0 holds for the construction", np.max(np.abs(bianchi)) < 1e-12)
    Ric = np.einsum('ac,abcd->bd', eta, Rm)          # eta^{ac} R_abcd
    Rsc = np.einsum('bd,bd->', eta, Ric)
    G00 = Ric[0, 0] - 0.5 * eta[0, 0] * Rsc
    Rslice = sum(Rm[i, j, i, j] for i in range(1, d) for j in range(1, d))
    check(f"d={d}: R_slice = R_ijij = 2 G_00 (relative error {abs(Rslice - 2 * G00) / abs(2 * G00):.1e})", abs(Rslice - 2 * G00) < 1e-10 * (1 + abs(G00)))
    must_fail(f"G5b d={d}: R_slice = G_00 (missing factor 2)", abs(Rslice - G00) < 1e-10 * (1 + abs(G00)))
    Rsp = Rm[1:, 1:, 1:, 1:]                          # spatial components R_ikjl
    Ricsp = np.einsum('ikil->kl', Rsp)
    Rspatial = np.trace(Ricsp)
    check(f"d={d}: spatial Ricci scalar equals R_slice", abs(Rspatial - Rslice) < 1e-12 * (1 + abs(Rslice)))
    if d == 4:
        # numerical quadrature of the RNC ball: h_ij = delta_ij - (1/3) R_ikjl x^k x^l on S^2 x radial
        nth, nph = 60, 120
        xg, wg = np.polynomial.legendre.leggauss(nth)     # cos(theta)
        ph = (np.arange(nph) + 0.5) * 2 * np.pi / nph
        CT, PH = np.meshgrid(xg, ph, indexing='ij')
        ST = np.sqrt(1 - CT**2)
        nvec = np.stack([ST * np.cos(PH), ST * np.sin(PH), CT], axis=-1).reshape(-1, 3)
        w = (np.outer(wg, np.ones(nph)) * (2 * np.pi / nph)).reshape(-1)
        def hmat(x):   # x: (N,3) coordinate points
            return np.eye(3)[None] - (1.0 / 3.0) * np.einsum('ikjl,Nk,Nl->Nij', Rsp, x, x)
        def area(lv):
            x = lv * nvec
            hm = hmat(x)
            det = np.linalg.det(hm)
            hinv = np.linalg.inv(hm)
            tilt = np.sqrt(np.einsum('Nij,Ni,Nj->N', hinv, nvec, nvec))
            return lv**2 * np.sum(w * np.sqrt(det) * tilt)
        def volume(lv, nr=40):
            xr, wr = np.polynomial.legendre.leggauss(nr)
            tot = 0.0
            for rr, wr_ in zip(0.5 * lv * (xr + 1), 0.5 * lv * wr):
                x = rr * nvec
                tot += wr_ * rr**2 * np.sum(w * np.sqrt(np.linalg.det(hmat(x))))
            return tot
        vals = []
        for lv in (0.2, 0.1, 0.05):
            cA = (area(lv) / (4 * np.pi * lv**2) - 1) / lv**2
            cV = (volume(lv) / (4 * np.pi * lv**3 / 3) - 1) / lv**2
            vals.append((lv, cA, cV))
        cA0 = -Rspatial / (6 * 3); cV0 = -Rspatial / (6 * 5)
        eA = abs(vals[-1][1] - cA0) / abs(cA0); eV = abs(vals[-1][2] - cV0) / abs(cV0)
        check(f"d=4 random tensor: (A/A_flat - 1)/l^2 -> -R/(6n) = {cA0:.6f} (l=0.05: {vals[-1][1]:.6f}, rel {eA:.1e})", eA < 5e-3)
        check(f"d=4 random tensor: (V/V_flat - 1)/l^2 -> -R/(6(n+2)) = {cV0:.6f} (l=0.05: {vals[-1][2]:.6f}, rel {eV:.1e})", eV < 5e-3)
        # convergence: error should shrink ~ l^2
        eA2 = abs(vals[0][1] - cA0); eA3 = abs(vals[-1][1] - cA0)
        check(f"d=4: error shrinks like l^2 (ratio {eA2 / max(eA3, 1e-300):.1f} ~ 16)", 10 < eA2 / max(eA3, 1e-300) < 22)
        # control: the coefficient -R/(6(n+1)) for the volume fails
        cVm = -Rspatial / (6 * 4)
        must_fail("G5c d=4 random tensor: volume coefficient -R/(6(n+1))", abs(vals[-1][2] - cVm) / abs(cVm) < 5e-3)

# ------------------------------------------------------------------------------------------------ G4
print("G4  symbolic chain in general d")
d = sp.symbols('d', positive=True)
Omg, Rr, G00, Gn, T00 = sp.symbols('Omega R G00 G T00')
dV_l = -Omg * l**(d + 1) * Rr / (6 * (d - 1) * (d + 1))
dA_l = sp.diff(dV_l, l)
dA_V = dA_l - (d - 2) / l * dV_l
check("dA|_l = d(dV|_l)/dl = -Omega l^d R/(6(d-1))", sp.simplify(dA_l + Omg * l**d * Rr / (6 * (d - 1))) == 0)
check("dA|_V = -Omega l^d R/(2(d^2-1))", sp.simplify(dA_V + Omg * l**d * Rr / (2 * (d**2 - 1))) == 0)
check("dA|_V = -Omega l^d G_00/(d^2-1) with R = 2 G_00", sp.simplify(dA_V.subs(Rr, 2 * G00) + Omg * l**d * G00 / (d**2 - 1)) == 0)
check("dA|_V / dA|_l = 3/(d+1)", sp.simplify(dA_V / dA_l - 3 / (d + 1)) == 0)
# flat-space fixed-volume correction uses A'(l) = (d-2) Omega l^{d-3}, V'(l) = Omega l^{d-2}
check("fixed-V coefficient (d-2)/l = A'(l)/V'(l) in flat space", sp.simplify(((d - 2) * Omg * l**(d - 3)) / (Omg * l**(d - 2)) - (d - 2) / l) == 0)
# with the modular energy term (2 pi <X>): chain to the Einstein coefficient (uses r02's M1: int xi dV = Omega l^d/(d^2-1))
dX = Omg * l**d / (d**2 - 1) * T00
chain = sp.solve(sp.Eq(dA_V.subs(Rr, 2 * G00) / (4 * Gn) + 2 * sp.pi * dX, 0), G00)[0]
check("chain (1/4G) dA|_V + 2 pi dX = 0  =>  G_00 = 8 pi G T_00 for every d", sp.simplify(chain - 8 * sp.pi * Gn * T00) == 0)
# --- G5 controls on the chain
mut_vol = -Omg * l**(d + 1) * Rr / (6 * (d - 1) * (d + 2))            # wrong ball-volume coefficient
mut_A_V = sp.diff(mut_vol, l) - (d - 2) / l * mut_vol
mut_chain = sp.solve(sp.Eq(mut_A_V.subs(Rr, 2 * G00) / (4 * Gn) + 2 * sp.pi * dX, 0), G00)[0]
must_fail("G5d wrong ball-volume coefficient 1/(6(d-1)(d+2)) still gives 8 pi G", sp.simplify(mut_chain - 8 * sp.pi * Gn * T00) == 0)
print("      (mutated coefficient gives G_00 = c T_00 with c/(8 pi G) =", sp.simplify(mut_chain / (8 * sp.pi * Gn * T00)), ")")
noV = dA_l.subs(Rr, 2 * G00)
nochain = sp.solve(sp.Eq(noV / (4 * Gn) + 2 * sp.pi * dX, 0), G00)[0]
check("dropping the fixed-volume correction changes the coefficient by exactly 3/(d+1)  (paper: 'off by (d+1)/3')",
      sp.simplify(nochain / (8 * sp.pi * Gn * T00) - 3 / (d + 1)) == 0)
must_fail("G5e fixed-radius area variation still gives 8 pi G", sp.simplify(nochain - 8 * sp.pi * Gn * T00) == 0)
for dd in (3, 4, 5, 10):
    val = sp.simplify((chain / (Gn * T00)).subs(d, dd))
    check(f"d={dd}: numeric coefficient of G T_00 = 8 pi ({sp.N(val, 10)})", sp.simplify(val - 8 * sp.pi) == 0)

print(f"\nr01: {sum(ok)}/{len(ok)} checks passed")
sys.exit(0 if all(ok) else 1)
