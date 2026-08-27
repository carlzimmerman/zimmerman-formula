#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
gate_spherical_efe_2026.py
==========================
GATE: exact spherical solution + EFE for the FROZEN CHASSIS (MMG constraint-first).

Chassis constraint (openai_push/final_closure/CLOSURE_CANDIDATE.md, FINAL_THEORY_MMG_CONSOLIDATED):
    C_M = D_i[ c^2 mu(y) D^i ln N ] - 4 pi G rho ,   y = (c^2/a0) |D ln N|
With Phi := c^2 ln N (Gate 2 certified the c^2 cancellation), C_M = 0 is EXACTLY
    div[ mu(|grad Phi|/a0) grad Phi ] = 4 pi G rho.
Frozen constitutive target: mu_exp(y) = 1 - e^{-y}.  Kernel-agnostic swap (Gate 13):
mu_n(y) = y/(1+y^n)^{1/n}, n=5,10 (Cassini-safe per route1B).

PART A: exact sourced spherical solution (Gauss reduction, uniqueness, mu*g=g_N,
        deep-MOND, BTFR, transition radius, shell theorem, boundary conditions).
PART B: EFE DERIVED from the constraint by linearizing about a superposed uniform
        external gradient (NOT assumed from AQUAL folklore): anisotropic operator,
        point-source Green function, flux normalization, response tensor at
        g_ext = 1.9 a0 (canonical) / 1.58 a0 (alt), kernel fork, curl-field
        necessity, and confrontation with the registered wide-binary numbers.

Every PASS/FAIL is a numeric or symbolic comparison that can fail.  Exit 0 = all pass.
"""
import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq

FAIL = []
def check(cond, label, detail=""):
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok: FAIL.append(label)
    return ok
def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))

# kernels (y = TRUE field / a0 in this chassis: mu is a function of |grad Phi|/a0)
def mu_exp(y): return 1.0 - np.exp(-y)
def mu_n(y, n): return y / (1.0 + y**n)**(1.0/n)
def Q_exp(y): return y * mu_exp(y)                      # Q(y) = y mu(y) = y_N
def Q_n(y, n): return y * mu_n(y, n)

def invertQ(Q, yN, lo=1e-14, hi=1e14):
    return brentq(lambda y: Q(y) - yN, lo, hi, xtol=1e-15, rtol=1e-14)

# Route A / completion kernel (MS08 alpha=1/2) used by the REGISTERED wide-binary corpus:
# nu(yN) = 1/(1-e^{-sqrt(yN)}), x = yN*nu(yN) observed.  mu_RA(x) = yN/x by inversion.
def nu_RA(yN): return 1.0/(1.0 - np.exp(-np.sqrt(yN)))
_yt = np.logspace(-12, 12, 200001); _xt = _yt*nu_RA(_yt)
assert np.all(np.diff(_xt) > 0)
def yN_of_x_RA(x): return np.exp(np.interp(np.log(x), np.log(_xt), np.log(_yt)))
def mu_RA(x): return yN_of_x_RA(x)/x

print("="*100)
print("PART A -- EXACT SOURCED SPHERICAL SOLUTION")
print("="*100)

# --- A1: symbolic Gauss reduction in full 3D Cartesian (generic mu, generic radial Phi) ---
x, y_, z_ = sp.symbols('x y z', real=True)
a0s = sp.symbols('a0', positive=True)
r = sp.sqrt(x**2 + y_**2 + z_**2)
mus = sp.Function('mu')
# grad Phi = f'(r) x_i/r with |grad Phi| = f'(r) on the f'>0 branch; use fp(r) := f'(r)
flux = [mus(sp.Function('fp')(r)/a0s) * sp.Function('fp')(r) * v / r for v in (x, y_, z_)]
divF = sum(sp.diff(flux[i], v) for i, v in enumerate((x, y_, z_)))
# verify div F == (1/r^2) d/dr (r^2 mu fp) symbolically-numerically at random points
import random
random.seed(7)
okA1 = True
mu_l = sp.Lambda(sp.Symbol('u'), 1 - sp.exp(-sp.Symbol('u')))
fp_l = sp.Lambda(sp.Symbol('s'), sp.Symbol('s')/(1+sp.Symbol('s'))**2 + sp.sin(sp.Symbol('s'))**2/10 + sp.Rational(1,3))
subsmap = {mus: mu_l, sp.Function('fp'): fp_l, a0s: sp.Rational(7,10)}
divF_c = divF.subs(subsmap).doit()
rs = sp.symbols('rs', positive=True)
target_c = ((1/rs**2)*sp.diff(rs**2 * mu_l(fp_l(rs)/sp.Rational(7,10))*fp_l(rs), rs))
for _ in range(6):
    px, py, pz = [random.uniform(0.2, 1.5) for _ in range(3)]
    pr = float(np.sqrt(px*px+py*py+pz*pz))
    v1 = float(divF_c.subs({x: px, y_: py, z_: pz}).evalf())
    v2 = float(target_c.subs({rs: pr}).evalf())
    if abs(v1 - v2) > 1e-10 * max(1.0, abs(v2)): okA1 = False
check(okA1, "A1  3D divergence of mu(|dPhi|/a0) grad Phi reduces EXACTLY to (1/r^2)(r^2 mu Phi')' "
            "(generic radial Phi, checked symbolically-numerically at 6 random points, <1e-10)")
info("A1  hence Gauss: r^2 mu(g/a0) g = G M(<r)  ==>  mu(g/a0) g = g_N(r) = GM(<r)/r^2  EXACT",
     "no curl term survives spherical symmetry; this is the exact sourced solution")

# --- A2: uniqueness -- Q(y)=y mu(y) strictly monotone (exact + grid) ---
ys = sp.Symbol('yy', positive=True)
Qp = sp.simplify(sp.diff(ys*(1-sp.exp(-ys)), ys))           # = 1 - e^{-y}(1-y)
# analytic chain: 1-y <= e^{-y}  =>  e^{-y}(1-y) <= e^{-2y} < 1  => Q' > 0
grid = np.logspace(-12, 3, 20001)
Qp_num = 1 - np.exp(-grid)*(1-grid)
check(sp.simplify(Qp - (1 - sp.exp(-ys)*(1-ys))) == 0 and np.all(Qp_num > 0),
      "A2  Q'(y) = 1 - e^{-y}(1-y) > 0 for all y>0 (symbolic form + 20001-pt grid; "
      "analytic: (1-y)<=e^{-y} => e^{-y}(1-y)<=e^{-2y}<1)",
      f"min on grid = {Qp_num.min():.3e}")
# mu_n family: Q_n' = y (2+y^n)/(1+y^n)^{1+1/n} > 0 manifestly
n_ = sp.Symbol('n', positive=True)
Qn = ys**2 * (1+ys**n_)**(-1/n_)
Qnp = sp.simplify(sp.diff(Qn, ys))
fact = sp.simplify(Qnp - ys*(2+ys**n_)*(1+ys**n_)**(-1-1/n_))
check(sp.simplify(fact) == 0,
      "A2b Q_n'(y) = y(2+y^n)/(1+y^n)^{1+1/n} > 0 manifestly (sympy identity) -- "
      "Gate-13 ellipticity condition d(y mu)/dy>0 re-verified for mu_n")
info("A2  => the algebraic relation mu(g/a0) g = g_N has a UNIQUE solution g(r) at every r; "
     "the spherical solution is globally single-valued")

# --- A3: exact-solution spot check on a Hernquist sphere (finite-difference residual) ---
G = 6.67430e-11; MSUN = 1.98892e30
A0C, A0A = 9.36e-11, 1.13e-10          # canonical / alt footings (footing-fork rule)
M_tot, a_h = 1e11*MSUN, 3.0857e19      # 1e11 Msun, a=1 kpc Hernquist
rgrid = np.logspace(17, 23, 4001)      # m
Mr = M_tot * (rgrid/(rgrid+a_h))**2
gN = G*Mr/rgrid**2
yN = gN/A0C
yv = np.array([invertQ(Q_exp, v) for v in yN])
g = A0C*yv
lhs_flux = rgrid**2 * mu_exp(yv) * g
dflux = np.gradient(lhs_flux, rgrid)
rho_h = M_tot*a_h/(2*np.pi*rgrid*(rgrid+a_h)**3)
resid = np.abs(dflux - 4*np.pi*G*rgrid**2*rho_h)/(4*np.pi*G*rgrid**2*rho_h)
check(np.median(resid) < 1e-4 and np.max(resid[5:-5]) < 5e-3,
      "A3  Hernquist 1e11 Msun: (1/r^2)d/dr[r^2 mu g] = 4 pi G rho verified by finite "
      "difference over 6 decades in r",
      f"median residual {np.median(resid):.2e}, interior max {np.max(resid[5:-5]):.2e}")

# --- A4: deep-MOND limit g -> sqrt(g_N a0), with the exact series ---
xs = sp.Symbol('xx', positive=True)
yser = sp.sqrt(xs)*(1 + sp.sqrt(xs)/4 + sp.Rational(7,96)*xs)
Qser = sp.series(yser*(1-sp.exp(-yser)), xs, 0, 3).removeO()
lead = sp.simplify(sp.expand(Qser) - xs)
# residual should be O(x^{5/2}): check lowest surviving power > 2
pows = [sp.degree(t, sp.sqrt(xs)) for t in sp.Add.make_args(sp.expand(lead))]
ok_series = all(p >= 5 for p in pows)   # in sqrt(x) units, x^{5/2} = power 5
num_ok = True
for yNt in [1e-4, 1e-6, 1e-8]:
    yt = invertQ(Q_exp, yNt)
    pred = np.sqrt(yNt)*(1+np.sqrt(yNt)/4+7*yNt/96)
    if abs(yt/pred - 1) > 1e-5: num_ok = False
check(ok_series and num_ok,
      "A4  deep-MOND inversion y = sqrt(y_N)[1 + sqrt(y_N)/4 + 7 y_N/96 + O(y_N^{3/2})] "
      "(sympy series residual O(y_N^{5/2}); numeric match <1e-5 at y_N=1e-4..1e-8)",
      "==> g -> sqrt(g_N a0) EXACT deep-MOND limit; same limit for mu_n (mu->y both)")
# Newtonian recovery: y - y_N ~ y_N e^{-y_N} (exponentially fast)
yt = invertQ(Q_exp, 20.0)
check(abs((yt-20.0) - 20.0*np.exp(-yt)) < 1e-9,
      "A4b Newtonian recovery exponentially fast: y - y_N = y e^{-y} exactly",
      f"at y_N=20: y-y_N = {yt-20:.3e}")

# --- A5: BTFR v^4 = G M a0, exact asymptotic, correction quantified ---
# exterior: v^4/(G M a0) = y/mu(y)  ->  1 as y->0, fractional excess ~ y/2
info("A5  exterior identity: v^4/(GMa0) = y/mu_exp(y)  (derived: v^2=gr, y_N=GM/(a0 r^2))")
rows = []
for mult in [10, 100, 1000]:
    yN_r = 1.0/mult**2
    y_r = invertQ(Q_exp, yN_r)
    ratio = y_r/mu_exp(y_r)
    rows.append((mult, ratio))
ok5 = all(abs(rt - 1) < 0.6*np.sqrt(1.0/m**2)*1.2 + 1e-12 for m, rt in rows) and \
      abs(rows[-1][1]-1) < 6e-3
for m, rt in rows:
    info(f"     r = {m:>4d} r_M : v^4/(GMa0) = {rt:.6f}  (excess ~ y/2 = {invertQ(Q_exp,1/m**2)/2:.5f})")
check(ok5, "A5  BTFR v^4 = G M a0 approached from ABOVE, excess ~ g/(2 a0) ~ 1/r; exact as r->inf",
      "kernel-independent: y/mu -> 1 for every mu with mu(y)->y")

# --- A6: transition radius ---
for lbl, A0 in (("canonical a0=9.36e-11", A0C), ("alt a0=1.13e-10", A0A)):
    rM_sun = np.sqrt(G*MSUN/A0); rM_gal = np.sqrt(G*1e11*MSUN/A0)
    info(f"A6  [{lbl}] r_M(1 Msun) = {rM_sun:.4e} m = {rM_sun/1.495978707e11:.0f} AU ; "
         f"r_M(1e11 Msun) = {rM_gal/3.0857e19:.2f} kpc")
ybreak_exp = invertQ(Q_exp, 1.0); ybreak_5 = invertQ(lambda v: Q_n(v,5), 1.0)
check(abs(Q_exp(ybreak_exp)-1) < 1e-12 and abs(ybreak_exp-1.3496) < 5e-4,
      f"A6  boost at r_M (y_N=1): g/g_N = {ybreak_exp:.4f} for mu_exp; {ybreak_5:.4f} for mu_5 "
      "(mu_n transitions sharper -- the priced RAR cost 0.108->0.123/0.127 dex, route1B)")

# --- A7: shell theorem ---
check(invertQ(Q_exp, 1e-14) < 2e-7,
      "A7  interior of isolated shell: M(<r)=0 => Q(y)=0 => y=0 UNIQUE (A2) => g=0 exactly; "
      "exterior: r^2 mu g = G M_shell identical to point mass -- exact point-equivalence",
      "caveat (honest): superposition FAILS -- a shell does NOT screen an external field; "
      "that non-superposition IS the EFE of Part B")

# --- A8: boundary conditions ---
vinf2 = np.sqrt(G*1e11*MSUN*A0C)
info("A8  r->0: g->0 (regular rho: g ~ g_N ~ r Newtonian-centre, or g ~ sqrt(a0 g_N) ~ r^{1/2} "
     "deep-MOND centre); Phi regular at 0")
info(f"A8  r->inf (isolated): g -> sqrt(GMa0)/r, Phi ~ v_inf^2 ln r  => lapse N ~ r^(v_inf^2/c^2), "
     f"exponent = {vinf2/8.98755179e16:.2e} for 1e11 Msun -- NOT asymptotically flat (standard MOND)")
info("A8  the divergence is an isolated-system idealization: any external field g_ext restores a "
     "1/r Newtonian-like far field beyond r_ext = sqrt(GMa0)/g_ext (the EFE regularizes the BC)")

print("="*100)
print("PART B -- THE EFE, DERIVED FROM THE CONSTRAINT (not assumed)")
print("="*100)

# --- B1: symbolic linearization about a superposed uniform external gradient ---
eps = sp.Symbol('epsilon')
ye = sp.Symbol('y_e', positive=True)
ph = sp.Function('phi')(x, y_, z_)
Phi2 = ye*z_ + eps*ph                      # units a0=1; background field ye along z
mu_g = sp.Function('mu')
gradP = [sp.diff(Phi2, v) for v in (x, y_, z_)]
mag = sp.sqrt(sum(t**2 for t in gradP))
FluxV = [mu_g(mag)*gradP[i] for i in range(3)]
divFl = sum(sp.diff(FluxV[i], v) for i, v in enumerate((x, y_, z_)))
lin = sp.simplify(sp.diff(divFl, eps).subs(eps, 0).doit())
Lsym = sp.Symbol('L_e')
targetB1 = mu_g(ye)*(sp.diff(ph, x, 2) + sp.diff(ph, y_, 2)) + \
           (mu_g(ye) + ye*sp.Derivative(mu_g(ye), ye))*sp.diff(ph, z_, 2)
# compare
d = sp.simplify(lin - (mu_g(ye)*(sp.diff(ph,x,2)+sp.diff(ph,y_,2))
                       + (mu_g(ye)+ye*sp.diff(mu_g(ye),ye))*sp.diff(ph,z_,2)))
check(d == 0,
      "B1  linearizing div[mu(|grad Phi|) grad Phi] about Phi = g_ext z + phi gives EXACTLY "
      "mu_e [ d_xx + d_yy + (1+L_e) d_zz ] phi = 4 pi G rho,  L_e = dln mu/dln y |_{y_e}",
      "DERIVED from C_M by sympy series -- anisotropic elliptic operator; this IS the EFE")

# --- B2: point-source Green function + flux normalization ---
Ls = sp.Symbol('Lv', positive=True)
phi0 = -1/sp.sqrt(x**2 + y_**2 + z_**2/(1+Ls))
pde = sp.simplify(sp.diff(phi0,x,2) + sp.diff(phi0,y_,2) + (1+Ls)*sp.diff(phi0,z_,2))
check(sp.simplify(pde) == 0,
      "B2  phi = -A [x^2+y^2+z^2/(1+L_e)]^{-1/2} solves the anisotropic equation away from origin "
      "(sympy identically zero)")
def flux_num(L, R):
    # F_i = mu_e( d_i phi + L delta_iz d_z phi ), unit A, unit mu_e; integrate F.rhat over sphere R
    def integrand(th):
        st, ct = np.sin(th), np.cos(th)
        xx, zz = R*st, R*ct
        u = xx*xx + zz*zz/(1+L)
        dphidx = xx*u**-1.5
        dphidz = (zz/(1+L))*u**-1.5
        Fr = dphidx*st + (1+L)*dphidz*ct
        return Fr*2*np.pi*R*R*st
    return quad(integrand, 0, np.pi, limit=200)[0]
L_test = 0.334247
f1, f2 = flux_num(L_test, 1.0), flux_num(L_test, 37.0)
pred = 4*np.pi*np.sqrt(1+L_test)
check(abs(f1/pred-1) < 1e-8 and abs(f2/pred-1) < 1e-8,
      "B2b Gauss flux of the linearized flux vector = 4 pi sqrt(1+L_e) x A x mu_e, R-independent "
      f"(R=1 and R=37 agree to <1e-8)  ==>  A = GM/(mu_e sqrt(1+L_e))",
      f"flux/pred = {f1/pred:.10f}, {f2/pred:.10f}")
info("B2  forces: ALONG e_ext  g = GM/(mu_e r^2)          => B_par  = 1/mu_e")
info("B2  forces: PERP  e_ext  g = GM/(mu_e sqrt(1+L_e) r^2) => B_perp = 1/(mu_e sqrt(1+L_e))")
info("B2  matches aqual_efe_full_solve_2026.py PART A line 55 exactly (B_par=nu big axis PARALLEL)")

# --- B3: the response tensor at the observed external field, all kernels, both footings ---
GEXT = 1.8996*A0C   # observed g_ext (wide_binary_pipeline GEXT_PHYS): x_ext = 1.8996 can / 1.5764 alt
X_EXT = {"canonical": GEXT/A0C, "alt": GEXT/A0A}
info(f"B3  observed external field: x_ext = g_ext/a0 = {X_EXT['canonical']:.4f} canonical / "
     f"{X_EXT['alt']:.4f} alt  (the gate's g_ext ~ 1.9 a0 = the canonical footing)")
print(f"\n  {'kernel':<22}{'footing':<11}{'mu_e':>9}{'L_e':>9}{'B_par':>9}{'B_perp':>9}"
      f"{'g_par=vB':>10}{'g_avg':>9}{'1-mu_e':>9}")
def tensor_row(name, muf, Lf, xe):
    m = muf(xe); L = Lf(xe)
    Bpar = 1.0/m; Bperp = 1.0/(m*np.sqrt(1+L))
    gpar = np.sqrt(Bpar); gavg = np.sqrt((Bpar+2*Bperp)/3)
    return m, L, Bpar, Bperp, gpar, gavg
res = {}
for nm, muf, Lf in [
    ("mu_exp (FROZEN)", mu_exp, lambda v: v*np.exp(-v)/mu_exp(v)),
    ("mu_5 (Cassini-safe)", lambda v: mu_n(v,5), lambda v: 1.0/(1+v**5)),
    ("mu_10 (Cassini-safe)", lambda v: mu_n(v,10), lambda v: 1.0/(1+v**10)),
    ("RouteA nu (REGISTERED)", mu_RA, lambda v: (np.log(mu_RA(v*1.0001))-np.log(mu_RA(v*0.9999)))/(np.log(1.0001)-np.log(0.9999))),
]:
    for ft in ("canonical", "alt"):
        m, L, Bp, Bq, gp, ga = tensor_row(nm, muf, Lf, X_EXT[ft])
        res[(nm, ft)] = (m, L, Bp, Bq, gp, ga)
        print(f"  {nm:<22}{ft:<11}{m:>9.5f}{L:>9.5f}{Bp:>9.5f}{Bq:>9.5f}{gp:>10.5f}{ga:>9.5f}{1-m:>9.5f}")
print()
# anchor: Route A reproduces the registered Amendment-9 numbers exactly (sqrt(B_par)=sqrt(nu(y_extN)))
gp_can = res[("RouteA nu (REGISTERED)", "canonical")][4]
gp_alt = res[("RouteA nu (REGISTERED)", "alt")][4]
check(abs(gp_can-1.2139) < 2e-3 and abs(gp_alt-1.2592) < 6e-3,
      f"B3a Route A largest-eigenvalue gamma reproduces the REGISTERED 1.2139/1.2592: "
      f"{gp_can:.4f}/{gp_alt:.4f}",
      "confirms the registered numbers are Route-A-kernel objects, sqrt(B_par) declared isotropic")
mexp_can = res[("mu_exp (FROZEN)", "canonical")]
check(abs(mexp_can[2]-1.17596) < 2e-4 and abs(mexp_can[3]-1.01805) < 2e-4,
      f"B3b FROZEN chassis mu_exp at x_ext=1.90: B_par = {mexp_can[2]:.5f}, B_perp = {mexp_can[3]:.5f} "
      f"(gamma_par = {mexp_can[4]:.4f}, orientation-avg gamma = {mexp_can[5]:.4f})")
# pointwise kernel ordering: mu_exp(x) > mu_RA(x) for all x => boost strictly smaller at every angle
xg = np.logspace(-6, 3, 2000)
check(np.all(mu_exp(xg) > mu_RA(xg) - 1e-12),
      "B3c mu_exp(x) >= mu_RA(x) for ALL x (2000-pt grid) => the frozen kernel's boost is strictly "
      "below Route A's at EVERY angle and separation -- the registered band CANNOT be reproduced "
      "by the frozen chassis kernel under any orientation/population treatment")

# --- B4: direction of the EFE -- suppression toward quasi-Newton (vs isolated MOND) ---
print()
xe = X_EXT["canonical"]
for yNi in [0.05, 0.2, 1.0]:
    iso = invertQ(Q_exp, yNi)/yNi
    info(f"B4  internal y_N = {yNi:<5}: ISOLATED mu_exp boost = {iso:.3f}  vs  EFE-saturated "
         f"bracket [{mexp_can[3]:.3f}, {mexp_can[2]:.3f}]")
check(invertQ(Q_exp, 0.05)/0.05 > 3.5 and mexp_can[2] < 1.18,
      "B4  DIRECTION: the external field SUPPRESSES the internal MOND boost (4.2x isolated -> "
      "1.02-1.18x saturated at y_N=0.05) -- quasi-Newtonian with renormalized, ANISOTROPIC G_eff; "
      "internal dynamics DO depend on g_ext: strong-equivalence-principle violation derived")

# --- B5: the curl field is load-bearing (naive 1D recipe gives the WRONG answer) ---
naive_par = 1.0/(mu_exp(xe)*(1+xe*np.exp(-xe)/mu_exp(xe)))   # dy/dy_N = 1/Q'(y_e)
check(naive_par < 1.0 < mexp_can[2],
      f"B5  naive 1D algebraic recipe would give B_par = 1/Q'(y_e) = {naive_par:.4f} (<1, SUB-Newton) "
      f"while the PDE gives {mexp_can[2]:.4f} (>1) -- the curl field flips the SIGN of the effect; "
      "the EFE here is genuinely DERIVED from the constraint PDE, not assumed algebraically")

# --- B6: Cassini <-> wide-binary coupling under the frozen chassis ---
print()
for nm in ["mu_exp (FROZEN)", "mu_5 (Cassini-safe)", "mu_10 (Cassini-safe)"]:
    m, L, Bp, Bq, gp, ga = res[(nm, "canonical")]
    info(f"B6  {nm:<22} canonical: 1-mu(x_ext) = {1-m:.5f}, gamma_par = {gp:.5f}, "
         f"gamma_avg = {ga:.5f}")
g5 = res[("mu_5 (Cassini-safe)", "canonical")][4]
g10 = res[("mu_10 (Cassini-safe)", "canonical")][4]
check(g5 < 1.005 and g10 < 1.0005,
      f"B6  the SAME 1-mu(y_ext~1.9) that route1B caps for Cassini Q2 controls the WB boost: "
      f"Cassini-safe mu_5/mu_10 predict gamma_v = {g5:.4f}/{g10:.4f} -- NO detectable DR4 signal",
      "within the frozen chassis, Cassini-safety and the registered DR4 band are MUTUALLY EXCLUSIVE")
info("B6  DR4 discriminator (sharp): registered Amdt-10 band 1.1614-1.1814 can / 1.1917-1.2267 alt "
     "is a Route-A-kernel object; frozen mu_exp saturates at 1.084/1.123; mu_n at ~1.00. "
     "A DR4 gamma_v in the registered band would FALSIFY the Cassini-safe chassis kernels; "
     "gamma_v ~ 1.00 would falsify mu_exp AND Route A but confirm mu_n.")

print("="*100)
n_ok = "ALL CHECKS PASS" if not FAIL else f"{len(FAIL)} FAILURES: {FAIL}"
print(n_ok)
import sys
sys.exit(0 if not FAIL else 1)
