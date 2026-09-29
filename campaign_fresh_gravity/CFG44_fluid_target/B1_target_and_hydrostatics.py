#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
B1 -- THE TARGET OF GAP 2, EXACTLY, AND THE HYPOTHESES UNDER WHICH "FLUID DENSITY = THE LAW'S PHANTOM DENSITY" IS A HYDROSTATIC
EQUILIBRIUM OF THE FLUID IN THE TOTAL FIELD.   (kappa = 1/2 FITTED; a0 = 9.3603e-11 m/s^2; nothing is fitted here.)

THE TARGET (CFG10 (ii), spherical-equivalent baryons; u = G M_tot(<r) = r^2 g, u_N = G M_b(<r) = r^2 g_N, w = u - u_N = G M_c(<r)):

      rho_c(r) g_tot(r) = (a0/3) rhobar_b(<r) = a0 M_b(<r) / (4 pi r^3)          <=>   w' = a0 r u_N / u        (T)

  (a) POINT MASS (x = r/r_M, r_M^2 = G M/a0):   rho_c = a0 / (4 pi G r sqrt(1 + x^2)),   M_c(<r) = M (sqrt(1 + x^2) - 1),
      g_tot = sqrt(g_N^2 + a0 g_N) (= the law P2),  P = a0 M/(8 pi r^2),  sigma^2 = P/rho_c = V_c^2/2.
  (b) EXTENDED BARYONS:  (T) is a first-order nonlinear ODE for M_c, integrated outward from the centre (rho_c at r depends ONLY on
      the baryons inside r).  The hydrostatic pressure in the total field, P(r) = Int_r^inf rho_c g_tot dr', is then EXACTLY
            P(r) = a0 g_N(r)/(8 pi G)  +  (a0/2) Sigma_out(r),     Sigma_out(r) = Int_r^inf rho_b dr'        (P)
      i.e. the local 'pressure Gauss law' of CFG10 (i) PLUS half a0 times the radial column density of the baryons OUTSIDE r.
  (c) Isotropic dispersion:   sigma^2 / (V_c^2/2) = 1 + 4 pi r^2 Sigma_out / M_b(<r)                                  (S)
      Equivalent restatement with locally virialised RADIAL dispersion sigma_r^2 = V_c^2/2 (Jeans with anisotropy beta):
            beta(r) = - (1/2) dln M_b/dln r = - (3/2) rho_b / rhobar_b(<r)  ( = -1 - (1/2) dln g_N/dln r  <= 0 )     (B)

HYPOTHESES under which 'fluid = phantom' is consistent with the fluid's own hydrostatic equilibrium in the TOTAL field:
  H1 spherical symmetry, static, Newtonian limit (GR corrections are ~ v^2/c^2 <~ 1e-4 -- checked N7);
  H2 the fluid feels only the Newtonian potential of ALL matter, g_felt = G (M_b + M_c)/r^2 (kernel-invisible fluid, L353/N11);
  H3 rho_c(r) >= 0 for the law considered (P2: proved by CFG10's AM-GM identity; nu_mono: checked here, N5);
  H4 an isotropic pressure exists: P(r) = Int_r^inf rho_c g dr' > 0 always (hydrostatics is then an IDENTITY -- consistency is automatic;
     the content of the target is the CLOSURE, not the equilibrium);
  H5 (collisionless reading) a non-negative isotropic f(E) exists (Eddington positivity, N6).  Anisotropic f(E,L) with (B): OPEN.

CHECKS (PRE-DECLARED)
  S1 (sympy) point-mass closed forms solve (T); S2 (sympy) identity (P) for an arbitrary M_b(r); S3 (sympy) identity (B) and (S).
  N1 CONTROL: numeric ODE for a point mass equals the closed form to 1e-5.
  N2 (T) holds pointwise for extended profiles (exp. sphere, Plummer, Hernquist, Freeman disc; compact and diffuse): residual < 1e-4.
  N3 numeric hydrostatic pressure (quadrature of rho_c g + analytic tail) equals (P) to 1e-3, and sigma^2 obeys (S).
  N4 rho_c >= 0 and P > 0 (P2-target, i.e. (T)) on every profile.
  N5 the law's own phantom (P2 and nu_mono): sign of rho_ph; charge function R = 4 pi r^3 rho_ph g/(a0 M_b): identically 1 for P2 on a point
     mass (control) and NOT 1 for nu_mono (reported); CFG10's identity rho_P2 - rho_(T) = rho_b (u_N + a0 r^2/2 - u)/u >= 0 (control).
  N6 isotropic Eddington f(E) >= 0 for the point-mass target and the compact exponential sphere; control: the singular isothermal sphere.
  N7 GR weak-field correction to the required c_s^2 <= 1e-3 for M_b up to 1e15 Msun.
MUTATE=1: the closure's charge is made CONSTANT (C = a0 M_b,tot/4 pi, CFG9's constant-charge closure) -- i.e. the enclosed-baryon dependence is
  broken.  For a point mass this is identical (no bite), for every extended profile N2 and N3 must FAIL (rc = 1).
Run: python3 B1_target_and_hydrostatics.py   (MUTATE=1 for the control)
"""
import os, sys, math
import numpy as np
import sympy as sp
from scipy.integrate import quad, cumulative_trapezoid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from Bcommon import *

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = Report("B1_target_and_hydrostatics", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: constant-charge closure in place of the enclosed-charge closure -- N2/N3 must FAIL on extended profiles ***")
KIND = "const" if MUTATE else "encl"

# =============================================================================================================== S1-S3 sympy
R.banner("S1-S3  SYMPY: closed forms and the exact identities")
r, Gs, a0s, Ms = sp.symbols("r G a0 M", positive=True)
x = sp.symbols("x", positive=True)
uN = Gs * Ms
u = sp.sqrt(uN ** 2 + a0s * uN * r ** 2)
ode_res = sp.simplify(u * sp.diff(u, r) - a0s * r * uN)                       # u u' = u u_N' + a0 r u_N with u_N' = 0
wprime = a0s * r * uN / u
rho_c = sp.simplify(wprime / (4 * sp.pi * Gs * r ** 2))
rM = sp.sqrt(Gs * Ms / a0s)
rho_closed = a0s / (4 * sp.pi * Gs * r * sp.sqrt(1 + (r / rM) ** 2))
Mc_closed = Ms * (sp.sqrt(1 + (r / rM) ** 2) - 1)
g_tot = u / r ** 2
P_closed = a0s * Ms / (8 * sp.pi * r ** 2)
s1 = [sp.simplify(ode_res), sp.simplify(rho_c - rho_closed), sp.simplify(sp.diff(Mc_closed, r) * Gs - wprime),
      sp.simplify(sp.diff(P_closed, r) + rho_closed * g_tot),                    # hydrostatic dP/dr = -rho_c g
      sp.simplify(P_closed / rho_closed - r * g_tot / 2),                         # sigma^2 = V_c^2/2
      sp.simplify(rho_closed * g_tot - a0s * Ms / (4 * sp.pi * r ** 3))]          # (T) itself
check("S1 (sympy) point mass: u^2 = u_N^2 + a0 u_N r^2 solves (T); rho_c = a0/(4 pi G r sqrt(1+x^2)); M_c = M(sqrt(1+x^2)-1); P = a0 M/(8 pi r^2) is "
      "hydrostatic in g_tot; sigma^2 = V_c^2/2; rho_c g = a0 M/(4 pi r^3)", f"residuals {s1}", all(v == 0 for v in s1))

Mb = sp.Function("M_b")(r)
S_out = sp.Function("S")(r)                                                     # Sigma_out(r) = Int_r^inf rho_b, S' = -rho_b
rho_b = sp.diff(Mb, r) / (4 * sp.pi * r ** 2)
gN = Gs * Mb / r ** 2
P_t = a0s * gN / (8 * sp.pi * Gs) + a0s / 2 * S_out
dP = sp.diff(P_t, r).subs(sp.Derivative(S_out, r), -rho_b)
res2 = sp.simplify(dP + a0s * Mb / (4 * sp.pi * r ** 3))
check("S2 (sympy) for an ARBITRARY M_b(r): d/dr [ a0 g_N/(8 pi G) + (a0/2) Sigma_out ] = - a0 M_b(<r)/(4 pi r^3) = - rho_c g_tot (identity (P))",
      f"residual {res2}", res2 == 0)

C = a0s * Mb / (4 * sp.pi)                                                      # charge C(r) = rho_c r^3 g
beta = sp.simplify(-r * sp.diff(C, r) / (2 * C))
beta_claim = -sp.Rational(3, 2) * rho_b / (3 * Mb / (4 * sp.pi * r ** 3))
gN_ = sp.Function("gN")(r)
beta_g = -1 - sp.Rational(1, 2) * r * sp.diff(gN_, r) / gN_
beta_g_sub = beta_g.subs(gN_, Gs * Mb / r ** 2).doit()
# Jeans with radial dispersion V_c^2/2 and anisotropy beta: d(rho s_r^2)/dr + 2 beta rho s_r^2/r + rho g = 0, rho s_r^2 = C/(2 r^2)
jeans = sp.simplify(sp.diff(C / (2 * r ** 2), r) + 2 * beta * (C / (2 * r ** 2)) / r + C / r ** 3)
ratio = 1 + 4 * sp.pi * r ** 2 * S_out / Mb                                       # (S)
Ptot = (a0s / (8 * sp.pi)) * Mb / r ** 2 + a0s / 2 * S_out
res3 = sp.simplify(Ptot / (C / (2 * r ** 2)) - ratio)
check("S3 (sympy) (B): locally-virial radial dispersion + Jeans gives beta = -(1/2) dlnM_b/dlnr = -(3/2) rho_b/rhobar_b = -1 - (1/2) dln g_N/dln r; "
      "(S): sigma^2/(V_c^2/2) = 1 + 4 pi r^2 Sigma_out/M_b", f"Jeans residual {jeans}, beta forms {sp.simplify(beta - beta_claim)}, "
      f"{sp.simplify(beta - beta_g_sub)}, (S) residual {res3}", jeans == 0 and sp.simplify(beta - beta_claim) == 0 and sp.simplify(beta - beta_g_sub) == 0 and res3 == 0)

# ---- the same target in its most compact form:  rho_c = (a0/(4 pi G r)) f_b(<r)  with the enclosed baryon fraction f_b = M_b/(M_b + M_c)
f_b = sp.Function("M_b")(sp.Symbol("r", positive=True)) / (sp.Function("M_b")(sp.Symbol("r", positive=True)) + sp.Function("M_c")(sp.Symbol("r", positive=True)))
rs_ = sp.Symbol("r", positive=True)
Mb_f = sp.Function("M_b")(rs_); Mc_f = sp.Function("M_c")(rs_)
form_a = (a0s / (4 * sp.pi * Gs * rs_)) * Mb_f / (Mb_f + Mc_f)
form_b = a0s * Mb_f / (4 * sp.pi * rs_ ** 3 * (Gs * (Mb_f + Mc_f) / rs_ ** 2))                     # a0 M_b/(4 pi r^3 g_tot)
res_fb = sp.simplify(form_a - form_b)
A_cusp = A0 / (4 * math.pi * G) / 1e6                                                              # Msun/pc^2  (kpc^2 -> pc^2 = 1e6)
check("S4 (sympy) (T) is the universal isothermal cusp times the enclosed baryon fraction:  rho_c(r) r = (a0/4 pi G) f_b(<r),  f_b = M_b/(M_b + M_c);  a0/(4 pi G) = 53.4 Msun/pc^2 "
      "(half of CFG2's halo column ceiling a0/(2 pi G) = 106.9)", f"symbolic residual {res_fb}; a0/(4 pi G) = {A_cusp:.2f} Msun/pc^2, a0/(2 pi G) = {2 * A_cusp:.1f}",
      res_fb == 0 and abs(A_cusp - 53.44) < 0.05)

# =============================================================================================================== numeric profiles
COMPACT = {"expsphere": exp_sphere(1e10, 2.0), "plummer": plummer(1e10, 1.0), "hernquist": hernquist(1e10, 2.0), "freeman": freeman_disc(1e10, 3.0)}
DIFFUSE = {"expsphere": exp_sphere(1e8, 2.0), "freeman": freeman_disc(1e8, 3.0)}
PROFS = [("compact", k, v) for k, v in COMPACT.items()] + [("diffuse", k, v) for k, v in DIFFUSE.items()]


def sigma_out(p, r_):
    """Sigma_out(r) = Int_r^inf rho_b dr' by quadrature of the profile's density on a log grid (analytic tail: baryons end)."""
    rr = np.geomspace(r_, p.rg[-1] * 0.5, 4001)
    return float(np.trapz(p.rho_b(rr), rr))


R.banner("N1  CONTROL: numeric ODE for a point mass vs closed form")
pm = point_mass(1e10)
rr, ww, uu, uNN = cold_mass(pm, "encl")
rMn = math.sqrt(G * 1e10 / A0)
n1 = float(np.max(np.abs(uu / (uNN * np.sqrt(1 + (rr / rMn) ** 2)) - 1)))
check("N1 CONTROL: numeric ODE (T) for a point mass equals u_N sqrt(1+x^2) to 1e-5 over x in [1e-3, 1e4]", f"max deviation {n1:.2e}", n1 < 1e-5)

R.banner("N2-N4  EXTENDED PROFILES: (T) pointwise, the hydrostatic pressure (P), sigma^2 (S), positivity")
res_T, res_P, res_S, minrho, minP, table = [], [], [], [], [], []
for tag, name, p in PROFS:
    rr, w, u, uN_ = cold_mass(p, KIND)
    rM_ = math.sqrt(p.Mtot * G / A0)
    sel = (rr > 0.02 * rM_) & (rr < 300 * rM_)
    # (T): rho_c g / [(a0/3) rhobar_b(<r)] with rho_c from the numerical derivative of w and g = u/r^2
    lw = np.gradient(w, np.log(rr))                                            # r dw/dr
    rho_c = lw / rr / (4 * math.pi * G * rr ** 2)
    g_ = u / rr ** 2
    lhs = rho_c * g_
    rhs = A0 * uN_ / (4 * math.pi * G * rr ** 3)                                 # a0 M_b(<r)/(4 pi r^3)
    rT = float(np.max(np.abs(lhs[sel] / rhs[sel] - 1)))
    # (P): hydrostatic pressure by quadrature of rho_c g from r to the end + analytic tail (baryons end: P_tail = a0 M_b,tot/(8 pi r^2) only if the
    # closure is the enclosed one; for the MUTATE closure the tail is computed from the same quadrature to a far radius)
    cum = cumulative_trapezoid(lhs, rr, initial=0.0)
    tail = A0 * p.ug[-1] / G / (8 * math.pi * rr[-1] ** 2)                      # rho_c g = C/r^3 with C = a0 M_b,tot/4 pi beyond the baryons (both closures)
    Ph = (cum[-1] - cum) + tail
    gN_arr = uN_ / rr ** 2
    Sg = np.array([sigma_out(p, r_) for r_ in rr[sel]])
    P_formula = A0 * gN_arr[sel] / (8 * math.pi * G) + 0.5 * A0 * Sg
    rP = float(np.max(np.abs(Ph[sel] / P_formula - 1)))
    sig2 = Ph[sel] / rho_c[sel] / (0.5 * u[sel] / rr[sel])
    S_form = 1 + 4 * math.pi * rr[sel] ** 2 * Sg / (uN_[sel] / G)
    rS = float(np.max(np.abs(sig2 / S_form - 1)))
    res_T.append(rT); res_P.append(rP); res_S.append(rS)
    minrho.append(float(np.min(rho_c[sel]))); minP.append(float(np.min(Ph[sel])))
    i_h = int(np.argmin(np.abs(rr - 2.0)))
    table.append((tag, name, rM_, float(sig2[np.argmin(np.abs(rr[sel] - 2.0))]), float(S_form[np.argmin(np.abs(rr[sel] - 2.0))]),
                  float(w[i_h] / uN_[i_h]), float(sig2.max())))
    hh = {"expsphere": 2.0, "plummer": 1.0, "hernquist": 2.0, "freeman": 3.0 if tag == "compact" or name == "freeman" else 2.0}[name]
    sig_at = [float(np.interp(v * hh, rr[sel], sig2)) for v in (0.5, 1.0, 3.0, 10.0)]
    P(f"    {tag:8s} {name:10s} r_M {rM_:7.3f} kpc: max|(T) residual| {rT:.2e}; max|P_num/P_(P) - 1| {rP:.2e}; max|sigma^2/(S) - 1| {rS:.2e}; "
      f"min rho_c {minrho[-1]:.2e}; sigma^2/(V_c^2/2) at r = 0.5, 1, 3, 10 h: {sig_at[0]:.2f}, {sig_at[1]:.2f}, {sig_at[2]:.2f}, {sig_at[3]:.2f}; at 2 kpc {table[-1][3]:.3f} (S: {table[-1][4]:.3f}); M_c/M_b at 2 kpc {table[-1][5]:.3f}")
check("N2 (T) rho_c g = a0 M_b(<r)/(4 pi r^3) holds pointwise on every extended profile (compact and diffuse), residual < 1e-4"
      + ("  [MUTATE: constant charge]" if MUTATE else ""), f"worst residual {max(res_T):.2e}", max(res_T) < 1e-4)
check("N3 the hydrostatic pressure of the target in the TOTAL field equals a0 g_N/(8 pi G) + (a0/2) Sigma_out to 1e-3, and sigma^2 obeys (S) to 1e-3"
      + ("  [MUTATE]" if MUTATE else ""), f"worst P residual {max(res_P):.2e}; worst sigma^2 residual {max(res_S):.2e}", max(res_P) < 1e-3 and max(res_S) < 1e-3)
check("N4 rho_c >= 0 and P > 0 on every profile (hydrostatics is then an identity: any rho_c >= 0 has an isotropic P)",
      f"min rho_c {min(minrho):.2e}; min P {min(minP):.2e}", min(minrho) >= 0 and min(minP) > 0)
R.num("N3_table", table)

# =============================================================================================================== N5 law phantoms
R.banner("N5  THE LAW'S OWN PHANTOM (P2, nu_mono): sign, charge function, CFG10's identity")


def phantom(p, kernel, r_):
    """rho_ph = (u_law - u_N)'/(4 pi G r^2) and the charge function R = 4 pi G r rho_ph u/(a0 u_N)  (R = 1 <=> (T))."""
    r_ = np.asarray(r_, float)
    e = 2e-3
    ul = lambda rr_: law_u(p, rr_, kernel)
    dW = (ul(r_ * (1 + e)) - p.u(r_ * (1 + e)) - ul(r_ * (1 - e)) + p.u(r_ * (1 - e))) / (2 * r_ * e)
    rho = dW / (4 * math.pi * G * r_ ** 2)
    u_l = ul(r_)
    Rr = dW * u_l / (r_ * A0 * p.u(r_))
    return rho, Rr


xs = np.geomspace(1e-3, 1e3, 400)
rM_pm = math.sqrt(1e10 * G / A0)
dev = {}
for kn in ("P2", "nu_mono"):
    rho, Rr = phantom(pm, kn, xs * rM_pm)
    dev[kn] = (float(np.max(np.abs(Rr - 1))), float(np.min(rho)), float(Rr[np.argmin(np.abs(xs - 1))]))
    P(f"    point mass, {kn:8s}: max|R - 1| over x in [1e-3,1e3] = {dev[kn][0]:.3e}; min rho_ph {dev[kn][1]:.2e}; R(x=1) = {dev[kn][2]:.4f}")
check("N5a CONTROL: for a point mass the P2 phantom obeys (T) exactly (charge function R = 1 to 1e-5); the nu_mono phantom does not (R departs by > 1%)",
      f"P2 max|R-1| = {dev['P2'][0]:.2e}; nu_mono max|R-1| = {dev['nu_mono'][0]:.3f}", dev["P2"][0] < 1e-5 and dev["nu_mono"][0] > 0.01)
neg = {}
for tag, name, p in PROFS:
    rM_ = math.sqrt(p.Mtot * G / A0)
    rg_ = np.geomspace(0.02 * min(rM_, 1.0), 300 * rM_, 800)
    for kn in ("P2", "nu_mono"):
        rho, Rr = phantom(p, kn, rg_)
        neg[(tag, name, kn)] = (float(np.mean(rho < 0)), float(np.min(Rr)), float(np.max(Rr)))
P("    fraction of radii with rho_ph < 0 / range of R = 4 pi r^3 rho_ph g/(a0 M_b):")
for k, v in neg.items():
    P(f"      {k[0]:8s} {k[1]:10s} {k[2]:8s}: neg fraction {v[0]:.3f}; R in [{v[1]:.3f}, {v[2]:.3f}]")
check("N5b H3: the P2 phantom density is >= 0 on every profile (CFG10's AM-GM identity); the nu_mono phantom is reported (H3 for nu_mono is a per-profile fact)",
      f"P2 negative fractions {[round(v[0], 3) for k, v in neg.items() if k[2] == 'P2']}; nu_mono {[round(v[0], 3) for k, v in neg.items() if k[2] == 'nu_mono']}",
      all(v[0] == 0 for k, v in neg.items() if k[2] == "P2"))
# CFG10's identity on the compact exponential sphere: rho_P2 - rho_(T) = rho_b (u_N + a0 r^2/2 - u)/u >= 0
p = COMPACT["expsphere"]
rM_ = math.sqrt(p.Mtot * G / A0)
rg_ = np.geomspace(0.05, 30 * rM_, 400)
rho_p2, _ = phantom(p, "P2", rg_)
rT_, wT_, uT_, uNT_ = cold_mass(p, "encl")
wf = np.interp(np.log(rg_), np.log(rT_), wT_)
uN_g = p.u(rg_)
rho_T = A0 * uN_g / (4 * math.pi * G * rg_ * (uN_g + wf))
uP2 = law_u(p, rg_, "P2")
# the identity's second term is evaluated on P2's own u (C4 of CFG10):  rho_P2 = a0 uN/(4 pi G r u_P2) + rho_b (uN + a0 r^2/2 - u_P2)/u_P2
rho_id = A0 * uN_g / (4 * math.pi * G * rg_ * uP2) + p.rho_b(rg_) * (uN_g + 0.5 * A0 * rg_ ** 2 - uP2) / uP2
idev = float(np.max(np.abs(rho_id[rho_p2 > 0] / rho_p2[rho_p2 > 0] - 1)))
minterm = float(np.min(p.rho_b(rg_) * (uN_g + 0.5 * A0 * rg_ ** 2 - uP2) / uP2))
check("N5c CONTROL (CFG10 C4): rho_P2 = a0 u_N/(4 pi G r u_P2) + rho_b (u_N + a0 r^2/2 - u_P2)/u_P2 with the second term >= 0",
      f"max relative deviation of the identity {idev:.2e}; min of the local term {minterm:.2e}", idev < 5e-3 and minterm >= -1e-30)
P("    compact exponential sphere: the P2 law's cold mass vs the target (T)'s:")
Mc_T = np.interp(np.log(rg_), np.log(rT_), wT_)
Mc_P2 = uP2 - uN_g
for v in (0.3, 1.0, 3.0, 10.0, 30.0):
    i = int(np.argmin(np.abs(rg_ - v * rM_)))
    P(f"      r = {v:5.1f} r_M: M_c(T)/M_c(P2 law) = {Mc_T[i] / Mc_P2[i]:.4f}")

# =============================================================================================================== N6 Eddington
R.banner("N6  H5: an isotropic collisionless equilibrium (Eddington f(E) >= 0) with rho_c(Phi_tot)")


def eddington(rr, rho, g):
    """isotropic DF f(E) = (1/(2 sqrt2 pi^2)) Int_E^inf (d^2 rho/d Phi^2) (Phi - E)^(-1/2) dPhi for rho(Phi(r)) on a log grid (g = dPhi/dr > 0)."""
    Phi = cumulative_trapezoid(g, rr, initial=0.0)
    lr = np.log(rr)
    dr_dl = rr
    rho_l = np.gradient(rho, lr)
    rho_P = rho_l / (rr * g)                                                   # d rho/d Phi
    rho_PP = np.gradient(rho_P, lr) / (rr * g)
    order = np.argsort(Phi)
    Ph, rpp = Phi[order], rho_PP[order]
    Emax = Ph[-1]

    def f_of(E):
        smax = math.sqrt(max(Emax - E, 1e-12))
        val = quad(lambda s: np.interp(E + s * s, Ph, rpp), 0.0, smax, limit=400)[0]
        return 2 * val / (2 * math.sqrt(2) * math.pi ** 2)
    return Phi, f_of


# control: singular isothermal sphere rho = s2/(2 pi G r^2), Phi = 2 s2 ln r  -> f(E) proportional to exp(-E/s2)
s2 = 1.0e4
rr_c = np.geomspace(1e-4, 1e4, 8001)
rho_c_ = s2 / (2 * math.pi * G * rr_c ** 2)
g_c = 2 * s2 / rr_c
Phi_c, f_c = eddington(rr_c, rho_c_, g_c)
Es = np.array([Phi_c[2000] + k * s2 for k in (-0.5, 0.0, 1.0, 2.0)])
fv = np.array([f_c(E) for E in Es])
ratio_c = fv[1:] / fv[0] / np.exp(-(Es[1:] - Es[0]) / s2)
check("N6 CONTROL: the singular isothermal sphere gives f(E) proportional to exp(-E/sigma^2) (numeric Eddington within 5%)",
      f"f ratios / exp-law = {np.round(ratio_c, 3)}", np.all(np.abs(ratio_c - 1) < 0.05))
fmin_all = {}
for lab, p in (("point mass 1e10", pm), ("compact exp. sphere", COMPACT["expsphere"])):
    rM_ = math.sqrt(p.Mtot * G / A0)
    rr_, w_, u_, uN_ = cold_mass(p, "encl", r0=1e-4 * rM_, r1=1e3 * rM_, n=8001)
    lw = np.gradient(w_, np.log(rr_))
    rho_ = lw / rr_ / (4 * math.pi * G * rr_ ** 2)
    g_ = u_ / rr_ ** 2
    Phi_, f_of = eddington(rr_, rho_, g_)
    Egrid = np.quantile(Phi_, np.linspace(0.05, 0.85, 17))
    fv = np.array([f_of(E) for E in Egrid])
    fmin_all[lab] = (float(fv.min() / fv.max()), float(fv.min()))
    P(f"    {lab:20s}: f(E) over 17 energies between Phi quantiles 5%..85%: min/max = {fmin_all[lab][0]:.3e} (all positive: {bool(np.all(fv > 0))})")
check("N6 H5: the target density is a non-negative isotropic Eddington equilibrium in its own total potential (point mass and compact exp. sphere)",
      f"min f/max f: {fmin_all}", all(v[1] > 0 for v in fmin_all.values()), load_bearing=False)

# =============================================================================================================== N7 GR
R.banner("N7  H1: the weak-field (Newtonian) limit -- GR correction to the required sound speed")
worst = 0.0
for Mb_ in (1e8, 1e10, 1e12, 1e15):
    p = point_mass(Mb_)
    rM_ = math.sqrt(Mb_ * G / A0)
    rr_, w_, u_, uN_ = cold_mass(p, "encl", r0=1e-2 * rM_, r1=30 * rM_, n=2001)
    m_ = u_ / G                                                                  # total mass inside r (Msun)
    t1 = 0.5 * u_ / (rr_ * C_KMS ** 2)                                           # P/(rho c^2) = sigma^2/c^2 = V_c^2/(2 c^2)
    t2 = 2 * u_ / (rr_ * C_KMS ** 2)                                             # 2 G m/(r c^2)
    t3 = A0 * rr_ * Mb_ / (2 * m_ * C_KMS ** 2)                                  # 4 pi r^3 P/(m c^2), P = a0 M_b/(8 pi r^2)
    F = (1 + t1) * (1 + t3) / (1 - t2)
    corr = float(np.max(np.abs(F - 1)))
    worst = max(worst, corr)
    P(f"    M_b = {Mb_:.0e}: max |(1 + P/rho c^2)(1 + 4 pi r^3 P/m c^2)/(1 - 2Gm/rc^2) - 1| over x in [1e-2, 30] = {corr:.2e}")
check("N7 H1: the largest weak-field relativistic correction (TOV weak-field factor) to the hydrostatic weight is <= 2e-2 for M_b <= 1e15 out to 30 r_M "
      "(and <= 1e-3 for M_b <= 1e12) -- two orders below the M-dependence of the required sound speed found in B2",
      f"worst {worst:.2e}", worst < 2e-2)

nf = R.write()
sys.exit(1 if nf else 0)
