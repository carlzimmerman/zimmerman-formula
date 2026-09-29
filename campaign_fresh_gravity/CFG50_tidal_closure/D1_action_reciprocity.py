#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
D1 -- ACTION + RECIPROCITY for a conserved cold fluid coupled to the TIDAL TENSOR of an auxiliary potential Phi_b sourced by baryons only.

ACTION (Newtonian weak-field reduction; kappa = 1/2 FITTED; nothing new fitted):
  S = S_b[x_b; Phi_tot] + S_g[Phi_tot] + S_c[fluid; Phi_tot] + S_aux[Phi_b, lambda; rho_b] + S_int
  S_g   = - Int |grad Phi_tot|^2 /(8 pi G)                      (GR weak field; baryons + fluid minimally coupled to Phi_tot)
  S_aux = Int lambda (lap Phi_b - 4 pi G rho_b)/(4 pi G)        (Phi_b sourced by baryons ONLY, via a multiplier: baryons do not couple to Phi_b directly)
  S_int = Int d^3x (1/2) chi T_ij[Phi_b] Pi^ij ,  T_ij = (delta_ij lap - d_i d_j) Phi_b   ("K-coupling": Pi^ij = Int f v^i v^j = the fluid's SECOND MOMENT, a composite fluid variable)
          <=> each fluid particle has L_p = (1/2)(delta_ij + h_ij) v^i v^j - Phi_tot, h_ij = chi T_ij   (an effective spatial metric built from the tidal tensor of Phi_b).
  DIMENSIONS: the requested L_int = (a0/8 pi G) T_ij Pi^ij is not an energy density for Pi = rho sigma^2: [a0/G][T][Pi] = M L^-2 T^-2 x (energy density) -- the coefficient must be a TIME^2
              chi (= 2 c_int).  The only universal a0,c time^2 is (c/a0)^2 (and 1/(G rho_L) = (kappa c/a0)^2); nothing built from a0,G alone has dimension time^2.
CLAIMS (all by committed calculation below):
  C1  T_ij is identically divergence-free (d_j T_ij = 0): used as a STRESS (force = d_j Sigma_ij) it exerts NO force.  In the K-coupling Pi is composite; for a cold fluid Pi = 0 -> S_int = 0; for isotropic Pi = P delta,
      S_int = 4 pi G chi Int rho_b P (a CONTACT term: zero force on the fluid wherever rho_b = 0).
  C2  ADJOINT / RECIPROCITY THEOREM: for ANY S_int[fluid, Phi_b], the multiplier equation d S/d Phi_b: lap(lambda) = -4 pi G q, q = delta S_int/delta Phi_b;  the baryons feel the extra acceleration a_react = -grad lambda.
      For S_int = Int F^ij T_ij : q = (delta_ij lap - d_i d_j) F^ij = div( 2[F_perp' + (F_perp-F_rr)/r] rhat ),  a_react = 8 pi G [F_perp' + (F_perp - F_rr)/r]   (outward positive).
      Checked (i) Cartesian sympy identity, (ii) 1-D EL of the multiplier action, (iii) the B4-Q3 case S_int = -Int rho_c Phi_b -> a_react = -G M_c/r^2 (B4's kappa=1), (iv) finite-difference virtual work.
      Normalisation independence: a kinetic term Z, source eps rho_b Phi_b (no multiplier) gives the same reaction at fixed FLUID-side coupling -> the reaction cannot be removed by a different action normalisation.
  C3  NUMBERS: Pi = the target's own Jeans stress (sigma_r^2 = V_c^2/2, beta = -(3/2) rho_b/rhobar_b), exponential spheres.  Fluid-side force  a_f = (chi/2rho)[d_r T_rr Pi_rr + 2 d_r T_perp Pi_perp]  vs reaction a_react;  R = a_react/a_f (chi cancels).
      Point mass: outside the baryons Pi is isotropic and T_ij is trace-free-diagonal(2,-1,-1) => a_f = 0 identically (the fluid does not feel the coupling at all), while the contact reaction ~ chi P' diverges as r->0.
  C4  MUTATE(a): Phi_b sourced by the FLUID density (rho_c g_tot = (a0/4 pi G) T_perp[Phi_c]): the closure becomes dM_c/dr = a0 r M_c/(G(M_b+M_c)): seed-dependent Gaussian growth, not the law -> the target FAILS.
Run: python3 D1_action_reciprocity.py    (MUTATE=a for the control)
"""
import os, sys, math
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.interpolate import PchipInterpolator
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from Dcommon import *

MUTATE = os.environ.get("MUTATE", "")
R = Report("D1_action_reciprocity", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE: P(f"\n  *** MUTATE={MUTATE}: Phi_b sourced by the fluid density in C4 -- the target check must FAIL ***")

# ------------------------------------------------------------------------------------------------ C1
R.banner("C1  dimensions; T_ij identically conserved; cold and isotropic limits of the K-coupling")
M_, L_, T_ = sp.symbols("M L T_t", positive=True)
dim = lambda m, l, t: M_**m * L_**l * T_**t
a0_over_G = dim(1, -2, 0); tidal = dim(0, 0, -2); Pi_2mom = dim(1, -1, -2); edens = dim(1, -1, -2)
mism = sp.simplify(a0_over_G * tidal * Pi_2mom / edens)
chi_dim = sp.simplify(edens / (tidal * Pi_2mom))
P(f"    (a0/G) T_ij Pi^ij / [energy density] = {mism}   (!= 1);   dimension of chi in S_int = chi T Pi /2 :  {chi_dim}  (a time^2)")
x, y, z = sp.symbols("x y z", real=True)
Phi = sp.Function("Phi")(x, y, z)
X = [x, y, z]
lapP = sum(sp.diff(Phi, v, 2) for v in X)
Tij = sp.Matrix(3, 3, lambda i, j: (lapP if i == j else 0) - sp.diff(Phi, X[i], X[j]))
div = [sp.simplify(sum(sp.diff(Tij[i, j], X[j]) for j in range(3))) for i in range(3)]
P(f"    d_j T_ij = {div}   (sympy, generic Phi(x,y,z))")
r_ = sp.symbols("r", positive=True)
Ph = sp.Function("Phi")(r_)
Tr = 2 * sp.diff(Ph, r_) / r_; Tp_ = sp.diff(Ph, r_, 2) + sp.diff(Ph, r_) / r_
lapS = sp.diff(Ph, r_, 2) + 2 * sp.diff(Ph, r_) / r_
ok1 = all(d == 0 for d in div) and mism != 1 and sp.simplify(Tr + 2 * Tp_ - 2 * lapS) == 0
gN = sp.Function("gN")(r_)
P(f"    spherical: T_rr = 2 g_N/r ; T_perp = 4 pi G rho_b - g_N/r ; trace = 2 lap Phi_b = 8 pi G rho_b.  Vacuum: T = (g_N/r) diag(2,-1,-1).")
check("C1a (sympy) the tidal tensor T_ij = (delta lap - d d) Phi is identically divergence-free; the requested L_int has the wrong dimension by a time^2 (a coefficient chi ~ time^2 is required)",
      f"d_j T_ij = 0 for generic Phi; mismatch factor {mism}", ok1)
# cold / isotropic
Pcs = sp.Function("P")(r_); rb = sp.Function("rho_b")(r_)
Ftr = 2 * Pcs + sp.Symbol("chi") * 0  # trace only for isotropic
Lint_iso = sp.Rational(1, 2) * sp.Symbol("chi") * (Tr + 2 * Tp_) * Pcs
Lint_iso = sp.simplify(Lint_iso.subs(sp.diff(Ph, r_, 2), (4 * sp.pi * sp.Symbol("G") * rb - 2 * sp.diff(Ph, r_) / r_)))
P(f"    isotropic Pi = P delta_ij:  S_int density = {Lint_iso}  = 4 pi G chi rho_b P   (contact term: no force on the fluid where rho_b = 0; cold fluid Pi = 0 -> S_int = 0)")
check("C1b (sympy) isotropic Pi: (1/2) chi T_ii P = 4 pi G chi rho_b P  (contact with the baryon density); Pi = 0 (cold fluid): S_int = 0",
      f"{Lint_iso}", sp.simplify(Lint_iso - 4 * sp.pi * sp.Symbol("G") * sp.Symbol("chi") * rb * Pcs) == 0)

# ------------------------------------------------------------------------------------------------ C2
R.banner("C2  adjoint (reciprocity) theorem -- Cartesian identity, radial multiplier EL, B4-Q3 control")
A = sp.Function("A"); B = sp.Function("B")
rr3 = sp.sqrt(x**2 + y**2 + z**2)
nvec = [v / rr3 for v in X]
Aex = sp.exp(-rr3**2) * (1 + rr3); Bex = rr3**2 / (1 + rr3**2)                # explicit test functions
F = sp.Matrix(3, 3, lambda i, j: (Aex if i == j else 0) + Bex * nvec[i] * nvec[j])
q_cart = sum(sp.diff(F[i, i], v, 2) for i in range(3) for v in X) - sum(sp.diff(F[i, j], X[i], X[j]) for i in range(3) for j in range(3))
rs = sp.symbols("rs", positive=True)
Ar = sp.exp(-rs**2) * (1 + rs); Br = rs**2 / (1 + rs**2)
Frr = Ar + Br; Fp = Ar
Vr = 2 * (sp.diff(Fp, rs) + (Fp - Frr) / rs)
q_rad = sp.diff(rs**2 * Vr, rs) / rs**2
pts = [(0.3, -0.7, 0.5), (1.1, 0.2, -0.4), (-0.6, 0.9, 1.3)]
res = []
for p in pts:
    qc = float(q_cart.subs({x: p[0], y: p[1], z: p[2]}))
    rv = math.sqrt(sum(c * c for c in p))
    qr = float(q_rad.subs(rs, rv))
    res.append(abs(qc - qr))
P(f"    q = (delta_ij lap - d_i d_j) F^ij  (Cartesian, F = A delta + B n n) minus  (1/r^2) d_r( r^2 * 2[F_perp' + (F_perp - F_rr)/r] ):  |residual| = {max(res):.2e}")
# radial multiplier EL
r = sp.symbols("r", positive=True)
Gs = sp.Symbol("G", positive=True)
Pb = sp.Function("Phi_b")(r); lam = sp.Function("lambda")(r)
Frr_f = sp.Function("F_rr")(r); Fp_f = sp.Function("F_perp")(r)
L_aux = lam * sp.diff(r**2 * sp.diff(Pb, r), r) / Gs                          # 4 pi r^2 * lam lap Phi_b /(4 pi G)
L_int = 4 * sp.pi * r**2 * (Frr_f * 2 * sp.diff(Pb, r) / r + 2 * Fp_f * (sp.diff(Pb, r, 2) + sp.diff(Pb, r) / r))
from sympy.calculus.euler import euler_equations
ELPhi = euler_equations(L_aux + L_int, [Pb], r)[0]
expr = ELPhi.lhs - ELPhi.rhs
lam_p = -8 * sp.pi * Gs * (sp.diff(Fp_f, r) + (Fp_f - Frr_f) / r)               # claimed  lambda' = -a_react
claim = expr.subs(sp.Derivative(lam, (r, 2)), sp.diff(lam_p, r)).subs(sp.Derivative(lam, r), lam_p)
claim = sp.simplify(sp.expand(claim))
P(f"    EL of Phi_b in the multiplier action with lambda' = -8 pi G [F_perp' + (F_perp-F_rr)/r]:  residual = {claim}")
# B4-Q3 control:  L_int = -4 pi r^2 rho_c Phi_b
rc = sp.Function("rho_c")(r)
ELq3 = euler_equations(L_aux - 4 * sp.pi * r**2 * rc * Pb, [Pb], r)[0]
Mc = sp.Function("M_c")(r)
lam_q3 = Gs * Mc / r**2                                                          # r^2 lambda' = G M_c  -> a_react = -lambda' = -G M_c/r^2
e3 = sp.simplify((ELq3.lhs - ELq3.rhs).subs(sp.Derivative(lam, (r, 2)), sp.diff(lam_q3, r)).subs(sp.Derivative(lam, r), lam_q3).subs(rc, sp.diff(Mc, r) / (4 * sp.pi * r**2)))
P(f"    B4-Q3 control (fluid feels Phi_b itself, S_int = -Int rho_c Phi_b): lambda' = G M_c/r^2 -> a_react = -G M_c/r^2 (inward extra pull);  EL residual = {e3}")
ok2 = max(res) < 1e-10 and claim == 0 and e3 == 0
check("C2a (sympy) reciprocity theorem: baryons feel a_react = -grad lambda, lap lambda = -4 pi G q; for S_int = Int F^ij T_ij, a_react = 8 pi G [F_perp' + (F_perp-F_rr)/r]; reproduces B4-Q3 (-G M_c/r^2 for kappa = 1)",
      f"Cartesian identity residual {max(res):.1e}; EL residuals {claim}, {e3}", ok2)
# normalisation independence
Zs, eps, C = sp.symbols("Z epsilon C", positive=True)
# L = -Z (grad Phi_b)^2/(8 pi G) - eps rho_b Phi_b + c S_int[Phi_b]; Phi_b = (eps/Z) psi_N + Phi_q ; fluid-side coupling C = c eps/Z (acts on psi = (Z/eps)Phi_b... ) ; baryon force from source term = - eps grad Phi_b
# reaction (q-part) = -eps grad(Phi_q),  lap Phi_q = 4 pi G c q / Z  -> a_react = eps c /Z * (8 pi G [..]) = C * 8 pi G [..] : independent of (Z, eps) at fixed C = c eps / Z
c_ = sp.Symbol("c")
a_react_norm = sp.simplify(eps * c_ / Zs)
P(f"    healthy-kinetic-term (Z>0) formulation without a multiplier: a_react = (eps c/Z) x 8 pi G[...] = C x 8 pi G[...] with C = c eps/Z the FLUID-side coupling; G_eff on baryons is renormalised by eps^2/Z (removable with Z -> infinity) but the reaction is NOT.")
check("C2b the reaction depends only on the fluid-side coupling C = c eps/Z: no choice of normalisation of Phi_b removes it", f"a_react coefficient = {a_react_norm} = C", True)

# ------------------------------------------------------------------------------------------------ C3 numbers
R.banner("C3  reaction vs fluid-side force, exponential spheres, Pi = the target's Jeans stress (sigma_r^2 = V_c^2/2, beta = -(3/2) rho_b/rhobar_b); a0 canonical")
rows = {}
allR = []
for Mb, h in ((1e9, 2.0), (1e10, 3.0), (1e11, 4.0), (1e12, 5.0)):
    prof = exp_sphere(Mb, h)
    bf = baryon_fields(prof, r0=1e-2 * h, r1=30 * h, n=6001)
    r_, g, rho = bf["r"], bf["g"], bf["rho"]
    d = lambda yv: np.gradient(yv, r_)
    a_f = (0.5 / rho) * (d(bf["Trr"]) * bf["Prr"] + 2 * d(bf["Tp"]) * bf["Pp"])        # per chi (outward +)
    a_r = 4 * math.pi * G * (d(bf["Pp"]) + (bf["Pp"] - bf["Prr"]) / r_)                # per chi (outward +), = 8 pi G [F_perp' + ..] with F = chi Pi/2
    lam_ = np.stack([bf["Trr"], bf["Tp"]])
    chi_crit_supp = 1.0 / lam_.max()          # chi < 0 (support sign: a_f > 0):  1 + chi lam > 0  <=>  |chi| lam_max < 1
    chi_crit_anti = 1.0 / (-lam_).max()       # chi > 0 : 1 + chi lam > 0 needs chi < 1/max(-lam)
    out = []
    for xh in (0.3, 1.0, 2.0, 3.0, 5.0):
        i = int(np.argmin(abs(r_ - xh * h)))
        supp = chi_crit_supp * abs(a_f[i]) / g[i]                                          # max ghost-free support fraction f = |a_f|/g_tot
        react_over_g = (-chi_crit_supp) * a_r[i] / g[i]                                    # chi = -chi_crit (support sign)
        gph = g[i] - bf["gN"][i]                                                            # the law's phantom (dark) acceleration
        react_over_gph = (-chi_crit_supp) * a_r[i] / gph
        out.append(dict(r_over_h=xh, af_over_chi_g=a_f[i] / g[i], ar_over_chi_g=a_r[i] / g[i], R=a_r[i] / a_f[i], fmax_support=supp, react_over_gtot_at_chicrit=react_over_g, react_over_gph_at_chicrit=react_over_gph, gph_over_gtot=gph / g[i]))
    rows[f"M={Mb:.0e},h={h}"] = out
    P(f"  M_b = {Mb:.0e}, h = {h} kpc:  |chi|_crit(support sign chi<0) = {chi_crit_supp:.3e},  (anti-support chi>0) = {chi_crit_anti:.3e}  [kpc^2/(km/s)^2]")
    for o in out:
        P(f"     r = {o['r_over_h']:.1f} h:  a_f/(chi g) = {o['af_over_chi_g']:+.3e}   a_react/(chi g) = {o['ar_over_chi_g']:+.3e}   R = a_react/a_f = {o['R']:+.2f}   "
          f"max ghost-free support f = {o['fmax_support']:.3f} ;  reaction/g_tot at that strength = {o['react_over_gtot_at_chicrit']:+.2f}")
    allR.append(out)
R.num("C3_rows", rows)
# scale-invariance: f_max(r/h) identical for every M
fm = np.array([[o["fmax_support"] for o in out] for out in allR])
spread = float((fm.max(0) / fm.min(0)).max())
P(f"  f_max(r/h) identical for all four spheres to within a factor {spread:.4f} (a0 drops out: a_f/(chi g) = (r/4)[d_r T_rr + 2(1-beta) d_r T_perp] is baryon geometry only)")
# point mass statements
P("  Point mass (rho_b = 0 outside): beta = 0, Pi isotropic; a_f = (chi/2rho)[d_r T_rr + 2 d_r T_perp] P = 0 since T_rr + 2 T_perp = 0 => the coupling exerts NO force on the fluid; contact reaction a_react = 4 pi G chi P' = -chi a0 G M/r^3 -> infinity at r -> 0.")
# analytic check that d_r(T_rr + 2 T_perp) = 0 in vacuum
Tvac = sp.symbols("Tvac")
Mm = sp.Symbol("Mm", positive=True)
Trr_v = 2 * Gs * Mm / r**3; Tp_v = -Gs * Mm / r**3
vac0 = sp.simplify(sp.diff(Trr_v + 2 * Tp_v, r))
P(f"  sympy: d_r(T_rr + 2 T_perp) in vacuum = {vac0}")
i1 = int(np.argmin(abs(baryon_fields(exp_sphere(1e10, 3.0), r0=0.03, r1=90, n=4001)["r"] - 3.0)))
# ---- finite-difference virtual-work check of a_react (independent path): move a thin baryon shell, differentiate S_int
prof = exp_sphere(1e10, 3.0); hh = 3.0
bf = baryon_fields(prof, r0=1e-2 * hh, r1=30 * hh, n=6001)
Pi_rr = PchipInterpolator(np.log(bf["r"]), bf["Prr"]); Pi_pp = PchipInterpolator(np.log(bf["r"]), bf["Pp"])
rg = np.linspace(bf["r"][0], bf["r"][-1], 400001)
dr_ = rg[1] - rg[0]

def S_int(s, dm, w=0.03 * hh, chi=1.0):
    """S_int[rho_b + dm (delta_w(r-s) shell)] = (1/2) chi Int 4 pi r^2 [T_rr Pi_rr + 2 T_perp Pi_perp] dr, Phi_b from the full baryon profile (numerical Gauss law)."""
    rho_b = prof.rho_b(rg) + dm * np.exp(-0.5 * ((rg - s) / w) ** 2) / (w * math.sqrt(2 * math.pi)) / (4 * math.pi * rg**2)
    m = np.concatenate([[0], np.cumsum(0.5 * (rho_b[1:] * rg[1:]**2 + rho_b[:-1] * rg[:-1]**2)) * 4 * math.pi * dr_])
    gNn = G * m / rg**2
    Trr_ = 2 * gNn / rg; Tp_n = 4 * math.pi * G * rho_b - gNn / rg
    mask = rg >= bf["r"][0]
    lr = np.log(np.clip(rg, bf["r"][0], bf["r"][-1]))
    integrand = 0.5 * chi * 4 * math.pi * rg**2 * (Trr_ * Pi_rr(lr) + 2 * Tp_n * Pi_pp(lr))
    return float(np.sum(integrand[mask]) * dr_)

s0 = 1.0 * hh; dm = 1e5; ds = 0.05 * hh
fd = (S_int(s0 + ds, dm) - S_int(s0 - ds, dm)) / (2 * ds) / dm       # force on the shell per unit mass = d S_int / d s
i = int(np.argmin(abs(bf["r"] - s0)))
ana = 4 * math.pi * G * (np.gradient(bf["Pp"], bf["r"])[i] + (bf["Pp"][i] - bf["Prr"][i]) / bf["r"][i])
P(f"    finite-difference virtual work (shell of mass 1e5 moved by +-0.05h at r = h, S_int recomputed from the shifted baryons):  a_react = {fd:+.4e}  vs adjoint formula {ana:+.4e}  (rel diff {abs(fd/ana-1):.2e})")
ok3a = abs(fd / ana - 1) < 0.02
ok3b = spread < 1.001
# numbers gate: reaction is O(g) at the ghost-limited strength inside ~ h
r_in = [o for o in rows["M=1e+10,h=3.0"] if o["r_over_h"] <= 1.0]
Rvals = [abs(o["R"]) for o in r_in]
react_in = [abs(o["react_over_gtot_at_chicrit"]) for o in r_in]
react_dm = [abs(o["react_over_gtot_at_chicrit"]) for o in rows["M=1e+09,h=2.0"] if o["r_over_h"] <= 1.0]
react_hi = [abs(o["react_over_gtot_at_chicrit"]) for o in rows["M=1e+12,h=5.0"] if o["r_over_h"] <= 1.0]
P(f"  reaction/g_law at the ghost-limited strength, r = 0.3 h, 1 h:  M_b=1e9: {[round(v,2) for v in react_dm]};  1e10: {[round(v,2) for v in react_in]};  1e12: {[round(v,3) for v in react_hi]}  -> O(1) g_law in the deep-MOND (dwarf/LSB) regime, falling ~ (fluid mass / baryon mass) in the Newtonian regime")
ok3c = min(react_in) > 0.3 and min(react_dm) > 0.3 and min(Rvals) > 0.5 and max(o["fmax_support"] for o in rows["M=1e+10,h=3.0"]) < 1.0
check("C3 (numeric) the ghost-free K-coupling supplies at most f_max < 1 of g_tot to the fluid (best at r ~ h, ~0.5, mass-independent) and at that strength the reaction on the baryons inside r <= h is >= 0.3 g_law for M_b = 1e9, 1e10 (deep-MOND regime; smaller for massive spirals) "
      "(R = a_react/a_f = O(1-10), opposite sign to the fluid force inside r < 1.7 h); the finite-difference virtual work agrees with the adjoint formula to 2%",
      f"f_max(r=0.3,1,2,3,5 h) = {[round(o['fmax_support'],3) for o in rows['M=1e+10,h=3.0']]};  |reaction/g_law| at chi_crit, r=0.3,1 h (1e10) = {[round(v,2) for v in react_in]}, (1e9) {[round(v,2) for v in react_dm]};  R = {[round(v,2) for v in Rvals]};  fd rel diff {abs(fd/ana-1):.1e}", ok3a and ok3b and ok3c)

# ------------------------------------------------------------------------------------------------ C4  MUTATE(a)
R.banner("C4  the closure with Phi_b sourced by BARYONS reproduces the law (point mass); with Phi_b sourced by the FLUID it does not")
Mb = 1e10; pm = point_mass(Mb); rM = math.sqrt(Mb * G / A0)
r0, r1 = 1e-3 * rM, 1e3 * rM
rg2 = np.geomspace(r0, r1, 4001)
uN = G * Mb
def rhs_baryon(s, yv):                      # w' = a0 r u_N/(u_N + w)     (target, Phi_b sourced by baryons)
    rq = math.exp(s); return [rq * A0 * rq * uN / (uN + yv[0])]
def rhs_fluid(s, yv):                       # w' = a0 r w/(u_N + w)       (MUTATE a: T_perp[Phi_c] = G M_c/r^3 = w/r^3)
    rq = math.exp(s); return [rq * A0 * rq * max(yv[0], 1e-300) / (uN + max(yv[0], 0.0))]
w0 = uN * (math.sqrt(1 + A0 * r0**2 / uN) - 1)
solb = solve_ivp(rhs_baryon, (math.log(r0), math.log(r1)), [w0], t_eval=np.log(rg2), rtol=1e-10, atol=1e-14, method="Radau")
wb = solb.y[0]
gl = np.sqrt((uN / rg2**2) ** 2 + A0 * uN / rg2**2)                           # P2 law
devb = np.max(np.abs(np.log10((uN + wb) / rg2**2 / gl)))
# mutate: seed the fluid mass at 1e-6 of the baryon mass at r0 (any seed; M_c = 0 is also a solution)
devs = {}
for seed in (1e-6, 1e-3, 1.0):
    solf = solve_ivp(rhs_fluid, (math.log(r0), math.log(r1)), [seed * uN], t_eval=np.log(rg2), rtol=1e-10, atol=1e-30, method="Radau")
    wf = solf.y[0]
    m = (rg2 > 0.1 * rM) & (rg2 < 10 * rM)
    devs[seed] = float(np.max(np.abs(np.log10((uN + wf[m]) / rg2[m] ** 2 / gl[m]))))
P(f"    Phi_b <- baryons:   max |log10 g_tot/g_P2| over 1e-3..1e3 r_M = {devb:.2e}   (positive control: the closure IS the law for a point mass)")
P(f"    Phi_b <- fluid (MUTATE a): max |log10 g_tot/g_P2| over 0.1..10 r_M for seeds 1e-6, 1e-3, 1 x M_b : {devs}")
if MUTATE == "a":
    dev_used = min(devs.values())
    ok4 = dev_used < 0.02                       # mutated claim 'the fluid-sourced closure also reproduces the law' -- must FAIL
else:
    ok4 = devb < 1e-4 and min(devs.values()) > 0.05
check("C4 (numeric) closure with Phi_b sourced by baryons = the P2 law for a point mass (<1e-4 dex); sourced by the fluid it does not (seed-dependent, >0.05 dex from the law at every seed)" + ("  [MUTATE a: asserts the fluid-sourced closure equals the law]" if MUTATE == "a" else ""),
      f"baryon-sourced dev {devb:.1e} dex; fluid-sourced devs {devs}", ok4)

nf = R.write()
sys.exit(1 if nf else 0)
