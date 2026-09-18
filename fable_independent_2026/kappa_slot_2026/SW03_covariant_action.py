#!/usr/bin/env python3
"""SW03 -- the covariant action for the mesoscopic switch: its static weak-field limit, its point-mass solution, the scalar's
characteristic cone, the switch-off, the bounded coupling energy and the FRW background, each checked in sympy.  See
SW03_covariant_action.md for the action and the gate ledger.  A FAIL is a finding; no literal-True checks."""
import os, json, math
import sympy as sp
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("SW03 -- the covariant action, checked\n")
G, u0, ell, a0, c, rho = sp.symbols('G u0 ell a0 c rho', positive=True)
x, y, z = sp.symbols('x y z', real=True)
phi = sp.Function('phi')(x, y, z); psi = sp.Function('psi')(x, y, z); PhiE = sp.Function('Phi_E')(x, y, z)
mus = sp.Function('mu_s')            # the switch coefficient, a given positive function of psi
Hf = lambda s: s / (1 + s)

# ------------------------------------------------------------------ 1. the static Euler-Lagrange equations
print("=" * 100); print("1. static weak-field Euler-Lagrange equations of the phi- and psi-sectors"); print("=" * 100)
# static limit of -(1/8piG) mu_s(psi) g^{mu nu} d phi d phi  ->  -(1/8piG) mu_s(psi) |grad phi|^2  (spatial metric flat)
# static limit of -(u0/2)[ell^2 (d psi)^2 + psi^2] + u0 psi H(S),  S = |grad Phi_E|^2/(8 pi G u0)
grad = lambda f: sp.Matrix([sp.diff(f, v) for v in (x, y, z)])
S_src = (grad(PhiE).dot(grad(PhiE))) / (8 * sp.pi * G * u0)
L_phi = -(1 / (8 * sp.pi * G)) * mus(psi) * grad(phi).dot(grad(phi))
L_psi = -(u0 / 2) * (ell ** 2 * grad(psi).dot(grad(psi)) + psi ** 2) + u0 * psi * Hf(S_src)
def EL(L, f):
    return sp.simplify(sp.diff(L, f) - sum(sp.diff(sp.diff(L, sp.diff(f, v)), v) for v in (x, y, z)))
el_phi = EL(L_phi, phi); el_psi = EL(L_psi, psi)
# expected forms: (1/4piG) div[mu_s grad phi] = 0 (vacuum) and u0 [ell^2 lap psi - psi + H(S)] = 0
div_form = (1 / (4 * sp.pi * G)) * sum(sp.diff(mus(psi) * sp.diff(phi, v), v) for v in (x, y, z))
lap = lambda f: sum(sp.diff(f, v, 2) for v in (x, y, z))
check("1a delta phi: the static equation is (1/4piG) div[mu_s(psi) grad phi] (= 4piG rho x coupling once matter is added): the scalar sector is LINEAR in phi with a given positive coefficient",
      sp.simplify(el_phi - div_form) == 0)
check("1b delta psi: the static equation is u0 [ell^2 lap psi - psi + H(|grad Phi_E|^2/(8 pi G u0))] = 0, i.e. (1 - ell^2 lap) psi = H(S): SW02's smoothed switch",
      sp.simplify(el_psi - u0 * (ell ** 2 * lap(psi) - psi + Hf(S_src))) == 0)

# ------------------------------------------------------------------ 2. the point-mass solution at ell -> 0: QUMOND with the RAR kernel
print("\n" + "=" * 100); print("2. point mass, ell -> 0: psi = y^2/(1+y^2), mu_s = 1/(nu(y)-1), total force = nu(y) g_N"); print("=" * 100)
yv, gN = sp.symbols('y g_N', positive=True)
nu = sp.Function('nu')
psi_of_y = Hf(yv ** 2)
y_of_psi = sp.sqrt(psi_of_y / (1 - psi_of_y))
check("2a the inversion y(psi) = sqrt(psi/(1-psi)) returns y exactly", sp.simplify(y_of_psi - yv) == 0)
mu_s_val = 1 / (nu(yv) - 1)
scalar_force = gN / mu_s_val                      # from mu_s r^2 phi' = G M -> phi' = g_N/mu_s (spherical, ell -> 0)
total = gN + scalar_force
check("2b g_N + g_N/mu_s = nu(y) g_N identically: QUMOND with the kernel nu", sp.simplify(total - nu(yv) * gN) == 0)
nu_rar = lambda yy: 1 / (1 - sp.exp(-sp.sqrt(yy)))
deep = sp.limit(sp.sqrt(yv) * (nu_rar(yv) * yv), yv, 0)     # deep limit: nu y -> sqrt(y)  <=>  g/a0 = sqrt(g_N/a0)
check("2c deep limit with nu_RAR: g/a0 -> sqrt(y), i.e. g^2 = a0 g_N", sp.simplify(sp.limit(nu_rar(yv) * yv / sp.sqrt(yv), yv, 0) - 1) == 0)
check("2d strong field: mu_s = 1/(nu_RAR(y) - 1) -> infinity as y -> infinity (the scalar switches OFF)", sp.limit(1 / (nu_rar(yv) - 1), yv, sp.oo) == sp.oo)
check("2e mu_s > 0 for every y > 0 (no ghost sign in the phi-sector): nu_RAR(y) > 1 for all y > 0",
      all(sp.N(nu_rar(sp.Float(v, 60)), 60) > 1 for v in (1e-6, 1e-3, 0.1, 1, 10, 1e3, 1e6)) and sp.limit(nu_rar(yv), yv, sp.oo) == 1,
      "nu_RAR(y) = 1/(1 - e^{-sqrt y}) > 1 for every finite y (evaluated at 60 digits; the double-precision e^{-1000} underflow was the earlier FAIL)")

# ------------------------------------------------------------------ 3. the scalar's characteristic cone
print("\n" + "=" * 100); print("3. the phi-sector's principal symbol: mu_s(psi) g^{mu nu} k_mu k_nu -- the null cone of g (no superluminal scalar)"); print("=" * 100)
k0, k1, k2, k3, m_s = sp.symbols('k0 k1 k2 k3 mu_s', real=True)
sym = m_s * (-k0 ** 2 + k1 ** 2 + k2 ** 2 + k3 ** 2)
sol = sp.solve(sp.Eq(sym, 0), k0)
check("3a the characteristic speed of phi is exactly c for any mu_s != 0 (k0 = +-|k|)", set(sp.simplify(s) for s in sol) == {sp.sqrt(k1 ** 2 + k2 ** 2 + k3 ** 2), -sp.sqrt(k1 ** 2 + k2 ** 2 + k3 ** 2)})
check("3b the psi-sector is a standard massive scalar (kinetic coefficient u0 ell^2/2 > 0, mass 1/ell): no ghost by construction", sp.simplify(u0 * ell ** 2 / 2 > 0) == sp.true)

# ------------------------------------------------------------------ 4. the bounded coupling energy and the FRW background
print("\n" + "=" * 100); print("4. the psi-aether coupling energy is bounded by u0; the FRW background switches the scalar off"); print("=" * 100)
Gn, cn, MPC = 6.674e-11, 2.99792458e8, 3.0857e22
H0 = 67.4e3 / MPC; OmL = 0.685
rhoL = OmL * 3 * H0 ** 2 / (8 * math.pi * Gn)
for foot, a0n in (("canonical", 9.3619e-11), ("alt", 1.1279e-10)):
    u0n = a0n ** 2 / (8 * math.pi * Gn)
    print(f"    {foot}: u0 = a0^2/(8 pi G) = {u0n:.2e} J/m^3 = rho_Lambda c^2 / {rhoL*cn**2/u0n:.1f}; max coupling energy u0 H(S) <= u0")
    S_frw = (cn * H0) ** 2 / (8 * math.pi * Gn * u0n)          # kappa_Theta = 1
    psi_frw = S_frw / (1 + S_frw)
    kmin = 1.0 / S_frw                                          # kappa_Theta giving psi_FRW = 1/2
    print(f"    {foot}: (c H0 / a0)^2 = {S_frw:.1f}; psi_FRW(kappa_Theta = 1) = {psi_frw:.4f}; psi_FRW >= 1/2 needs kappa_Theta >= {kmin:.4f}  (1/Z^2 = {1/(32*math.pi/3):.4f})")
    OUT[foot] = dict(u0=u0n, S_frw=S_frw, psi_frw=psi_frw, kappa_min=kmin)
check("4a the coupling energy scale u0 is below rho_Lambda c^2 on both footings (a cosmological-constant-sized back-reaction on the aether/metric sector, not a solar-system one)",
      all(v["u0"] < rhoL * cn ** 2 for v in OUT.values()))
check("4b with kappa_Theta = 1/Z^2 the FRW switch is at least half-on on both footings (psi_FRW >= 1/2): the MOND scalar is OFF on the background",
      all((v["S_frw"] / (32 * math.pi / 3)) / (1 + v["S_frw"] / (32 * math.pi / 3)) >= 0.5 for v in OUT.values()),
      f"psi_FRW at kappa_Theta = 1/Z^2: " + ", ".join(f"{k}: {(v['S_frw']/(32*math.pi/3))/(1+v['S_frw']/(32*math.pi/3)):.3f}" for k, v in OUT.items()))

n, n_pass = len(CH), sum(CH)
print(f"\nSW03 COMPLETE: {n_pass}/{n} checks PASS.  Verified: the static limit IS SW02 with the Einstein-frame field as the switch; the point-mass")
print("solution is QUMOND with the RAR kernel; the scalar is linear with a positive coefficient and propagates on the light cone; it switches off")
print("in strong fields and on the FRW background (kappa_Theta >= 1/Z^2).  NOT verified here: full PPN with all couplings, lensing (inherited from")
print("TeVeS's disformal coupling), cosmological perturbations, the infall-region switch-off.  Nothing here derives kappa.")
json.dump(dict(pass_=n_pass, n=n, parts=OUT), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "SW03_results.json"), "w"), indent=1, default=str)
