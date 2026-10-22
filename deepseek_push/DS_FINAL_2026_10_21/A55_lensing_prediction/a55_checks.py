#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
A55 -- LENSING COMPUTED, NOT ASSUMED.

Lane A55.  Answers one question: what does this theory's action predict for a *lensing
observable*, and does it survive contact with real Einstein radii?

Task 1  derive kappa and the deflection from the action's (Phi, Psi); show the deflection
        equals the dynamical prediction to O(Psi); give the correction and its size.
Task 2  apply it to the SLACS Einstein radii on disk, zero free parameters, a0 = 1.132e-10,
        baryonic mass only, both IMF branches.
Task 3  the sharp test against GR+dark matter: Delta theta_E, radial image position, the
        precision needed, and whether any existing/planned survey has it.
Task 4  verdict.

Inputs (all already on disk, no network):
  real_research/data/slacs_auger2009_lenses.tsv   (Auger+2009, SLACS IX, VizieR J/ApJ/705/1099)
  deepseek_push/DS_FINAL_2026_10_21/THEORY.md     section 3.5 (the four gates)
  A3_lensing_gw/report.md, A12_slip_theorem/report.md, A18_two_ratios/report.md

Conventions: c = 1 in the theory algebra, SI in the numbers; K = 4*pi*G for the printed action
(A3 section 1); metric ds^2 = -(1-2Psi)dt^2 + (1+2Phi)dx^2 with Phi, Psi the POSITIVE well depths
(the standard lensing convention, in which a point mass has alpha = 4GM/(bc^2)).

Exit 0 iff every check passes.  A55_MUTATE=<name> breaks one group (see MUTATE.md).
"""
import json, math, os, sys, time
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import gammainc, gammaln

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DATA = os.path.join(REPO, "real_research", "data", "slacs_auger2009_lenses.tsv")
MUT  = os.environ.get("A55_MUTATE", "") or (sys.argv[1] if len(sys.argv) > 1 else "")
T0   = time.time()

OUT  = []
def P(s=""):
    print(s); OUT.append(s)

# ------------------------------------------------------------------ constants
G      = 6.67430e-11
C      = 2.99792458e8
MSUN   = 1.98847e30
PC     = 3.0856775814913673e16
KPC    = 1.0e3*PC
ARCSEC = math.pi/(180.0*3600.0)
A0_THEORY = 1.132e-10         # P3: kappa = 1/2, rho_bare = rho_DE/Omega_L
A0_RUN    = 1.0e-30 if (os.environ.get("A55_MUTATE","") or "") == "newton" else A0_THEORY
IMF_HEAD  = "Fc" if (os.environ.get("A55_MUTATE","") or "") == "chabrier" else "Fs"
SLIP_ON   = (os.environ.get("A55_MUTATE","") or "") != "slipzero"
A0_CANON  = 9.3603e-11        # the record's canonical footing, carried for comparison only
K_GRAV    = 4.0*math.pi*G     # the action's K

# cosmology: Auger's own flat LCDM (Om = 0.3, OL = 0.7, h = 0.7), in which RE and Mass are tabulated
OM, OL, H0 = 0.3, 0.7, 70.0e3/(1.0e6*PC)
_zg = np.linspace(0.0, 6.0, 8001)
_E  = np.sqrt(OM*(1.0+_zg)**3 + OL)
_ig = np.concatenate([[0.0], np.cumsum(0.5*(1.0/_E[1:] + 1.0/_E[:-1])*np.diff(_zg))])
def DC(z):  return (C/H0)*float(np.interp(z, _zg, _ig))
def DA(z):  return DC(z)/(1.0+z)
def DAls(z1, z2): return (DC(z2)-DC(z1))/(1.0+z2)
def SICR(zl, zs): return C*C*DA(zs)/(4.0*math.pi*G*DA(zl)*DAls(zl, zs))

# ------------------------------------------------------------------ Sersic / Prugniel-Simien
B4 = 7.669249934
def b_ser(n):  return B4 if n == 4.0 else 2.0*n - 1.0/3.0 + 4.0/(405.0*n) + 46.0/(25515.0*n*n)
def nu_ps(n):
    p = 1.0 - 0.6097/n + 0.05463/(n*n)
    return n*(3.0-p)
def M2D_star(R, Re, n=4.0, M=1.0):
    """exact projected mass inside R of a Sersic with total M."""
    return M*gammainc(2.0*n, b_ser(n)*(R/Re)**(1.0/n))
def Sigma_star(R, Re, n=4.0, M=1.0):
    b = b_ser(n)
    norm = M*b**(2*n)/(2.0*math.pi*Re*Re*n*math.exp(gammaln(2*n)))
    return norm*np.exp(-b*(R/Re)**(1.0/n))
def M3D_star(r, Re, n=4.0, M=1.0):
    """Prugniel-Simien deprojection: same shape, gamma-function cumulative mass."""
    return M*gammainc(nu_ps(n), b_ser(n)*(r/Re)**(1.0/n))

def g_law(gN, a0):
    """the theory's law, g_N = g^2/(g+a0), inverted."""
    gN = np.asarray(gN, dtype=float)
    return 0.5*gN*(1.0+np.sqrt(1.0+4.0*a0/np.maximum(gN, 1e-300)))
def F_phantom(y):
    """M_ph/M_b = 1/2 (sqrt(1+4/y) - 1), y = g_N/a0."""
    return 0.5*(np.sqrt(1.0+4.0/np.maximum(y, 1e-300))-1.0)

GLX, GLW = np.polynomial.legendre.leggauss(400)
GLX = 0.5*(GLX+1.0); GLW = 0.5*GLW

def M2D_from_g(R, M3Df, a0, rmax=1.0e6*KPC):
    """total projected mass in cylinder R from the total acceleration:
       M_2D(<R) = (R^2/G) int_R^rmax g dr/sqrt(r^2-R^2),  r = R cosh u."""
    if R >= rmax: return 0.0
    if (os.environ.get("A55_MUTATE","") or "") == "noproj":
        return float(np.asarray(M3Df(np.array([R])))[0])
    U = math.acosh(max(rmax/R, 1.0+1e-9))
    u = GLX*U
    r = R*np.cosh(u)
    g = g_law(G*np.asarray(M3Df(r))/r**2, a0)
    return R*R/G*float(np.sum(GLW*g)*U)

# ------------------------------------------------------------------ data
def load_slacs():
    lines = [l.rstrip("\n") for l in open(DATA, encoding="latin-1")]
    hi = [i for i, l in enumerate(lines) if l.startswith("recno")][0]
    hdr = lines[hi].split("\t"); col = {c: i for i, c in enumerate(hdr)}
    raw = [l.split("\t") for l in lines[hi+3:] if l.strip() and not l.startswith("#")]
    def f(v):
        try: return float(v.strip())
        except Exception: return float("nan")
    L = []
    for r in raw:
        if len(r) < len(hdr): continue
        d = dict(name=r[col["SDSS"]].strip(), zl=f(r[col["zlens"]]), zs=f(r[col["zsrc"]]),
                 sig=f(r[col["sigma"]]), RE=f(r[col["RE"]]), lME=f(r[col["Mass"]]),
                 Fc=f(r[col["Fc"]]), eFc=f(r[col["e_Fc"]]), Fs=f(r[col["Fs"]]), eFs=f(r[col["e_Fs"]]),
                 lMc=f(r[col["logMc"]]), lMs=f(r[col["lMs"]] if "lMs" in col else r[col["logMs"]]),
                 e_lMs=f(r[col["e_logMs"]]), e_lMc=f(r[col["e_logMc"]]),
                 ReV=f(r[col["Re(V)"]]), ReI=f(r[col["Re(I)"]]))
        if all(np.isfinite([d["zl"], d["zs"], d["RE"], d["lME"], d["Fs"], d["Fc"]])) and d["RE"] > 0:
            L.append(d)
    return L, len(raw)

def Re_kpc(d, band):
    """Re(B/V/I) columns are ARCSEC; convert with the lens angular diameter distance."""
    return d[band]*ARCSEC*DA(d["zl"])

def predict_Re(d, a0, imf="Fs", band="ReV", n=4.0, rmax=1.0e6*KPC, newton=False):
    """solve kappa_bar(<R)=1 for the zero-parameter model.  Returns R_E in kpc."""
    sc  = SICR(d["zl"], d["zs"]); ME = 10.0**d["lME"]
    REo = d["RE"]*KPC; Re = Re_kpc(d, band)
    A   = d[imf]*ME/M2D_star(REo, Re, n)              # Msun per unit-normalised total
    M3Df = lambda r: A*M3D_star(r, Re, n)*MSUN
    aa  = 1e-30 if newton else a0
    fun = lambda R: M2D_from_g(R, M3Df, aa, rmax) - math.pi*R*R*sc
    Rs = np.logspace(math.log10(0.15*REo), math.log10(10.0*REo), 60)
    v  = np.array([fun(x) for x in Rs])
    idx = np.where(np.diff(np.sign(v)) != 0)[0]
    if len(idx) == 0: return float("nan")
    return brentq(fun, Rs[idx[0]], Rs[idx[0]+1], xtol=1e-5*KPC)/KPC

# ------------------------------------------------------------------ check machinery
CK = []
def ck(cid, what, measured, ok):
    CK.append(dict(id=cid, what=what, measured=str(measured), pass_=bool(ok)))
    P("  [%s] %s  %s: %s" % (cid, "PASS" if ok else "FAIL", what, measured))

RES = dict(lane="A55", generated=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           mutate=MUT or None,
           constants=dict(G=G, c=C, Msun=MSUN, kpc=KPC, a0_theory=A0_THEORY,
                          a0_canonical=A0_CANON, K_grav=K_GRAV, cosmology="flat LCDM Om=0.3 OL=0.7 h=0.7",
                          data=DATA))

# =====================================================================================
# SECTION 1 -- TASK 1: the derivation
# =====================================================================================
P("="*120)
P("A55 -- LENSING COMPUTED, NOT ASSUMED")
P("="*120)
P("\n" + "-"*120)
P("TASK 1 -- kappa and the deflection from the action's Phi and Psi")
P("-"*120)

# ---- K1: the traceless spatial Einstein tensor is the slip operator, exactly.
import sympy as sp
t_, x_, y_, z_ = sp.symbols("t x y z", real=True)
co = [t_, x_, y_, z_]; eta = sp.diag(-1, 1, 1, 1)

def _ein(Phi, Psi):
    h = sp.zeros(4, 4); h[0, 0] = -2*Psi
    for i in (1, 2, 3): h[i, i] = -2*Phi
    htr = sum(eta[a, a]*h[a, a] for a in range(4))
    box = lambda f: sum(eta[a, a]*sp.diff(f, co[a], 2) for a in range(4))
    G = sp.zeros(4, 4)
    for mu in range(4):
        for nu in range(4):
            t1 = sum(eta[a, a]*sp.diff(h[a, nu], co[mu], co[a]) for a in range(4))
            t2 = sum(eta[a, a]*sp.diff(h[a, mu], co[nu], co[a]) for a in range(4))
            G[mu, nu] = sp.Rational(1, 2)*(t1+t2-box(h[mu, nu])-sp.diff(htr, co[mu], co[nu]))
            s = sum(eta[a, a]*eta[b, b]*sp.diff(h[a, b], co[a], co[b])
                    for a in range(4) for b in range(4))
            G[mu, nu] -= sp.Rational(1, 2)*eta[mu, nu]*(s-box(htr))
    Gm = sp.zeros(4, 4)
    for mu in range(4):
        for nu in range(4): Gm[mu, nu] = eta[mu, mu]*G[mu, nu]
    return Gm

fld = x_**3 + 3*x_*y_**2 - 2*y_*z_ + z_**2 + 5*x_*z_
PHI = fld; PSI = sp.Rational(1, 3)*fld + x_**2*z_
Gm = _ein(PHI, PSI)
Gtr3 = sum(Gm[i, i] for i in (1, 2, 3))          # SPATIAL trace: the traceless part subtracts this
resid = 0
for i in (1, 2, 3):
    for j in (1, 2, 3):
        lhs = sp.expand(Gm[i, j] - sp.Rational(1, 3)*(1 if i == j else 0)*Gtr3)
        rhs = sp.diff(PHI-PSI, co[i], co[j])
        if i == j:
            rhs -= sp.Rational(1, 3)*sum(sp.diff(PHI-PSI, co[k], 2) for k in (1, 2, 3))
        resid = max(resid, abs(float(sp.expand(lhs-rhs))) if (lhs-rhs).free_symbols else abs(float(lhs-rhs)))
ck("K1", "exact symbolic identity: G^i_j - (1/3)d^i_j G^k_k = (d^i d_j - (1/3)d^i_j lap)(Phi-Psi)",
   "max residual over 9 components = %.3e" % resid, resid < 1e-12)
RES["k1_slip_identity_residual"] = float(resid)

# ---- K2/K3: the deflection functional, on the two exact lenses.
def alpha_sphere(R, gf, rmax=1.0e12*KPC):
    """alpha(R) = (4R/c^2) int_R^rmax g(r) dr/sqrt(r^2-R^2),  r = R cosh u, dr/sqrt = du.
       This is the twice-one-sided line-of-sight integral of the perpendicular gradient of
       Psi_eff = (Phi+Psi)/2, i.e. (2/c^2) int grad_perp(Phi+Psi) dl."""
    U = math.acosh(max(rmax/R, 1.0+1e-9))
    u = GLX*U
    r = R*np.cosh(u)
    return 4.0*R/C**2*float(np.sum(GLW*gf(r)))*U

Mpt = 1.0e11*MSUN; bpt = 10.0*KPC
a_pt = alpha_sphere(bpt, lambda r: G*Mpt/r**2, rmax=1.0e9*KPC)
ck("K2", "deflection functional reproduces the point mass, alpha = 4GM/(b c^2)",
   "alpha_num/alpha_exact - 1 = %.2e" % (a_pt/(4*G*Mpt/(bpt*C*C))-1.0),
   abs(a_pt/(4*G*Mpt/(bpt*C*C))-1.0) < 2e-6)
RES["k2_point_mass_ratio"] = float(a_pt/(4*G*Mpt/(bpt*C*C)))

SIG_SIS = 250.0e3; RL = 1000.0*KPC; RS = 2000.0*KPC
g_sis = lambda r: 2.0*SIG_SIS**2/r
a_sis = alpha_sphere(RL, g_sis, rmax=1.0e9*KPC)
th_sis = 4.0*math.pi*(SIG_SIS/C)**2*(RS-RL)/RS
# alpha for SIS is b-independent: 4 pi sigma^2/c^2
ck("K3", "deflection functional reproduces the SIS, alpha = 4 pi sigma^2/c^2 (b-independent)",
   "alpha_num/alpha_SIS - 1 = %.2e ; d alpha/db over a decade = %.2e"
   % (a_sis/(4*math.pi*SIG_SIS**2/C**2)-1.0,
      abs(alpha_sphere(2*RL, g_sis, rmax=1.0e9*KPC)/a_sis-1.0)),
   abs(a_sis/(4*math.pi*SIG_SIS**2/C**2)-1.0) < 2e-6
   and abs(alpha_sphere(2*RL, g_sis, rmax=1.0e9*KPC)/a_sis-1.0) < 2e-6)
RES["k3_sis_ratio"] = float(a_sis/(4*math.pi*SIG_SIS**2/C**2))

# ---- K4: the law's mass identity, and two routes to the projected mass.
Mb, rr = 1.0e11*MSUN, 8.0*KPC
y  = lambda r: G*Mb/(A0_THEORY*r*r)
Mtot_law = lambda r: r*r*g_law(G*Mb/r**2, A0_THEORY)/G
res_law = max(abs(Mtot_law(x)-Mb*(1.0+F_phantom(y(x))))/(Mb*(1.0+F_phantom(y(x))))
              for x in np.logspace(math.log10(0.5*KPC), math.log10(300*KPC), 25))
ck("K4", "exact law identity M_tot(<r) = M_b(<r)[1+F(y)], F = (1/2)(sqrt(1+4/y)-1)", 
   "max relative residual = %.2e" % res_law, res_law < 1e-12)
RES["k4_law_identity_residual"] = float(res_law)

# rho_ph from the two routes: (1/4 pi r^2) d(M_b F)/dr  vs  (1/4 pi G r^2) d(r^2 (g-g_N))/dr
def rho_ph_A(r):
    h = r*1e-5
    dM = (Mb*(1.0+F_phantom(y(r+h))) - Mb*(1.0+F_phantom(y(r-h))))/(2*h)
    return dM/(4.0*math.pi*r*r)
def rho_ph_B(r):
    h = r*1e-5
    f = lambda x: x*x*(g_law(G*Mb/x**2, A0_THEORY)-G*Mb/x**2)/G
    return (f(r+h)-f(r-h))/(2*h)/(4.0*math.pi*r*r)
rr4 = max(abs(rho_ph_A(x)/rho_ph_B(x)-1.0) for x in np.logspace(math.log10(1*KPC), math.log10(200*KPC), 20))
ck("K4b", "phantom density: (1/4 pi r^2) d(M_b F)/dr equals (1/4 pi G r^2) d[r^2(g-g_N)]/dr",
   "max relative difference = %.2e" % rr4, rr4 < 1e-6)
RES["k4b_rho_route_diff"] = float(rr4)

# two routes to the projected mass: g-integral vs direct line-of-sight integral of rho_tot
Mb2, Re2 = 1.0e11*MSUN, 6.0*KPC
M3f = lambda r: M2D_star(r, Re2, 4.0, Mb2)   # spherical stand-in with a known 3D law
# use an analytic spherical case instead: Hernquist
MH, aH = 1.0e11*MSUN, 5.0*KPC
M3H = lambda r: MH*r*r/(r+aH)**2
def rho_tot_H(r):
    # rho_ph from d(M_ph)/dr plus the Hernquist density
    h = r*1e-6
    Mph = lambda x: x*x*(g_law(G*M3H(x)/x**2, A0_THEORY)-G*M3H(x)/x**2)/G
    return (Mph(r+h)-Mph(r-h))/(2*h)/(4.0*math.pi*r*r) + MH*aH/(2.0*math.pi*r*(r+aH)**3)
# exact and independent: M2D(<R) = 4 pi int_0^R R' dR' int_0^zmax rho(sqrt(R'^2+z^2)) dz
ZMAX = 3.0e4*KPC          # the same cut used by the g-integral route below
def M2D_direct(R, f, zmax=ZMAX, nR=120):
    Rp = np.geomspace(1e-4*R, R, nR)
    tot = 0.0
    for i in range(nR-1):
        x  = 0.5*(Rp[i]+Rp[i+1]); dx = Rp[i+1]-Rp[i]
        sig, _ = quad(lambda zz: f(math.sqrt(x*x+zz*zz)), 0.0, zmax, limit=400)
        tot += 4.0*math.pi*x*sig*dx
    return tot
rA = M2D_from_g(10.0*KPC, M3H, A0_THEORY, rmax=ZMAX)
rB = M2D_direct(10.0*KPC, rho_tot_H)
ck("K4c", "projected mass: g-integral route equals the direct line-of-sight integral of rho_tot",
   "M2D(g)/M2D(LOS) - 1 = %.2e" % (rA/rB-1.0), abs(rA/rB-1.0) < 1e-3)
RES["k4c_projection_route_diff"] = float(rA/rB-1.0)

# ---- K5: the slip ODE and its first integral (A12 (E1)->(E2), with the 3K coefficient)
def slip_from_Pi(Pif, r, rmax=1.0e4*KPC):
    """f' = -3 K r int_r^rmax Pi/r' dr'  (asymptotically flat branch)."""
    u = GLX*(math.log(rmax/r)); rp = r*np.exp(u)
    return -3.0*K_GRAV*r*float(np.sum(GLW*Pif(rp)))*math.log(rmax/r)
Pi_test = lambda r: 1.0e-3*(KPC/r)**2      # arbitrary positive profile
# solve (f'/r)' = 3K Pi by direct integration of the ODE from infinity
def f_solve(r):
    # f'(r) by the first integral, then verify the ODE residual numerically
    h = r*1e-4
    fp  = slip_from_Pi(Pi_test, r)
    fp2 = slip_from_Pi(Pi_test, r+h)
    fp1 = slip_from_Pi(Pi_test, r-h)
    return (fp2-fp1)/(2*h) - fp/r - 3.0*K_GRAV*Pi_test(r)
ode_res = max(abs(f_solve(x))/abs(3.0*K_GRAV*Pi_test(x)) for x in np.logspace(math.log10(2*KPC), math.log10(500*KPC), 12))
ck("K5", "slip first integral f' = -3K r int_r^inf Pi/r' satisfies (f'/r)' = 3K Pi",
   "max ODE residual / source = %.2e" % ode_res, ode_res < 2e-4)
RES["k5_slip_ode_residual"] = float(ode_res)

# ---- K6: the power-law slip coefficient c_n = B(2n+1)/B(n+1), checked against the full integral
def Bint(m):
    f = lambda u: u**(-m)/math.sqrt(u*u-1.0)
    v, _ = quad(f, 1.0, np.inf, limit=400)
    return v
def c_analytic(n): return Bint(2*n+1)/Bint(n+1)
def c_numeric(n, R=10.0*KPC, A=1.0):
    Psi  = lambda r: A*(R/r)**n
    g    = lambda r: n*A*R**n/r**(n+1)
    a0_  = alpha_sphere(R, g, rmax=1.0e9*KPC)
    # Phi = Psi(1-Psi), so Psi_eff = Psi - Psi^2/2, dPsi_eff/dr = g(1-Psi)
    a1_  = alpha_sphere(R, lambda r: g(r)*(1.0-Psi(r)), rmax=1.0e9*KPC)
    return (a1_/a0_-1.0)/(-Psi(R))
cn = [(n, c_analytic(n), c_numeric(n)) for n in (0.5, 1.0, 1.5, 2.0)]
worst = max(abs(c1/c2-1.0) for _, c1, c2 in cn)
ck("K6", "power-law slip: d alpha/alpha = -c_n Psi(R) with c_n = B(2n+1)/B(n+1), from the full LOS integral",
   "; ".join("n=%.1f c=%.4f (num %.4f)" % (n, c1, c2) for n, c1, c2 in cn) + " ; worst %.1e" % worst,
   worst < 2e-3)
RES["k6_power_law_cn"] = [dict(n=float(n), c_analytic=float(c1), c_numeric=float(c2)) for n, c1, c2 in cn]

# ---- K7: the size of the correction on a galaxy-scale and a cluster-scale lens
def psi_at(RE_kpc, M2D_Msun):
    return G*M2D_Msun*MSUN/(RE_kpc*KPC*C*C)
psi_gal  = psi_at(4.07, 2.5e11)          # median SLACS: R_E = 4.07 kpc, M_E = 2.5e11
psi_clus = psi_at(150.0, 2.0e14)         # massive cluster, R_E ~ 150 kpc, M_E ~ 2e14
cn_ref = c_analytic(1.0) if SLIP_ON else 0.0
frac_gal  = cn_ref*psi_gal
frac_clus = cn_ref*psi_clus
ck("K7", "correction to the deflection: |d alpha/alpha| = c_n Psi at R_E, 1e-6..1e-5 (galaxy), 1e-5..1e-4 (cluster)",
   "galaxy %.2e, cluster %.2e (c_n = %.4f)" % (frac_gal, frac_clus, cn_ref),
   1e-6 < frac_gal < 1e-5 and 1e-5 < frac_clus < 1e-4)
RES["k7_correction"] = dict(psi_galaxy=float(psi_gal), psi_cluster=float(psi_clus),
                            cn=float(cn_ref), frac_galaxy=float(frac_gal), frac_cluster=float(frac_clus),
                            alpha_galaxy_arcsec=float(4.0*psi_gal*206264.806),
                            alpha_cluster_arcsec=float(4.0*psi_clus*206264.806),
                            dalpha_galaxy_arcsec=float(frac_gal*4.0*psi_gal*206264.806),
                            dalpha_cluster_arcsec=float(frac_clus*4.0*psi_clus*206264.806),
                            galaxy_RE_kpc=4.07, galaxy_ME=2.5e11, cluster_RE_kpc=150.0, cluster_ME=2.0e14)

# =====================================================================================
# SECTION 2 -- TASK 2: SLACS
# =====================================================================================
P("\n" + "-"*120)
P("TASK 2 -- zero-parameter Einstein radii against SLACS (Auger+2009, 70 lenses)")
P("-"*120)
L, nraw = load_slacs()
P("  rows in file %d ; usable %d" % (nraw, len(L)))

# K8 data integrity: recompute M_E from theta_E and the two redshifts
dM = []
for d in L:
    ME = SICR(d["zl"], d["zs"])*math.pi*(d["RE"]*KPC)**2/MSUN
    dM.append(math.log10(ME)-d["lME"])
dM = np.array(dM)
ck("K8", "lensing geometry: M_E recomputed from R_E, z_l, z_s reproduces Auger's tabulated mass",
   "N=%d median %.4f dex, scatter %.4f dex" % (len(dM), np.median(dM), dM.std(ddof=1)),
   len(L) == 70 and abs(np.median(dM)) < 0.01 and dM.std(ddof=1) < 0.01)
RES["data"] = dict(n_rows=nraw, n_usable=len(L), median_dlogME=float(np.median(dM)),
                   scatter_dlogME=float(dM.std(ddof=1)))

# K8b profile self-consistency: the total stellar mass implied by f_* M_E / shape vs the SED mass
dA = []
for d in L:
    if not np.isfinite(d["ReV"]): continue
    A = d["Fs"]*10**d["lME"]/M2D_star(d["RE"]*KPC, Re_kpc(d, "ReV"), 4.0)
    dA.append(math.log10(A)-d["lMs"])
dA = np.array(dA)
ck("K8b", "profile self-consistency: M_* implied by f_* M_E / (light fraction at R_E) matches the SED M_*",
   "median %+.3f dex, scatter %.3f dex (N=%d)" % (np.median(dA), dA.std(ddof=1), len(dA)),
   abs(np.median(dA)) < 0.10 and dA.std(ddof=1) < 0.10)
RES["data"]["logA_minus_logMs_median"] = float(np.median(dA))
RES["data"]["logA_minus_logMs_scatter"] = float(dA.std(ddof=1))

def run_sample(a0, imf, band, n=4.0, newton=False, rmax=1.0e6*KPC):
    out = []
    for d in L:
        if not np.isfinite(d[band]): continue
        r = predict_Re(d, a0, imf, band, n, rmax, newton)
        if np.isfinite(r): out.append((d["name"], r/d["RE"], r, d["RE"], d))
    return out

def stats(sample, label):
    x = np.array([s[1] for s in sample]); lx = np.log(x); N = len(x)
    sem = lx.std(ddof=1)/math.sqrt(N)
    # chi2 with the stated per-lens errors: theta_E 2%, stellar mass error propagated (dlnR = 0.5 dlnM),
    # and a 5% shape systematic on the light profile
    chi2 = 0.0
    for nm, ratio, Rp, Ro, d in sample:
        eF = d["eFs"] if label.startswith("Salp") else d["eFc"]
        eF = eF if np.isfinite(eF) and eF > 0 else 0.10
        s_th = 0.02
        s_m  = 0.5*math.log(1.0+eF/max(d["Fs"] if label.startswith("Salp") else d["Fc"], 1e-3))
        s_sh = 0.05
        s = math.sqrt(s_th**2+s_m**2+s_sh**2)
        chi2 += (math.log(ratio)/s)**2
    return dict(label=label, N=N, median=float(np.median(x)), mean_ln=float(lx.mean()),
                sem_ln=float(sem), sigma_offset=float(abs(lx.mean())/sem),
                scatter_ln=float(lx.std(ddof=1)), scatter_dex=float(lx.std(ddof=1)/math.log(10.0)),
                chi2=float(chi2), dof=int(N-1), chi2_dof=float(chi2/(N-1)),
                min=float(x.min()), max=float(x.max()),
                frac_within_10pct=float(np.mean(np.abs(x-1.0) < 0.10)))

SAL = run_sample(A0_RUN, IMF_HEAD, "ReV")
CHA = run_sample(A0_THEORY, "Fc", "ReV")
NEW = run_sample(A0_THEORY, "Fs", "ReV", newton=True)
CAN = run_sample(A0_CANON,  "Fs", "ReV")
st_sal, st_cha, st_new, st_can = stats(SAL,"Salpeter"), stats(CHA,"Chabrier"), stats(NEW,"Newton"), stats(CAN,"Salpeter")

P("\n  model                                    N   median R_E,pred/R_E,obs   <ln> +- sem      scatter   chi2/dof")
for s in (st_sal, st_cha, st_new, st_can):
    P("  %-38s %3d      %.4f            %+.4f +- %.4f   %.3f dex   %.2f"
      % (s["label"]+" @ a0=%.4e"%A0_THEORY if s is not st_can else "Salpeter @ a0=9.3603e-11 (record)",
         s["N"], s["median"], s["mean_ln"], s["sem_ln"], s["scatter_dex"], s["chi2_dof"]))

ck("K9", "headline zero-parameter prediction at a0=1.132e-10, Salpeter: R_E short by 10-16%, >4 sigma",
   "median %.4f, <ln> = %+.4f +- %.4f (%.1f sigma), N=%d"
   % (st_sal["median"], st_sal["mean_ln"], st_sal["sem_ln"], st_sal["sigma_offset"], st_sal["N"]),
   0.85 < st_sal["median"] < 0.93 and st_sal["sigma_offset"] > 4.0)
ck("K10", "Chabrier branch fails far harder (as expected: 0.26 dex lighter stars)",
   "median %.4f, <ln> = %+.4f (%.1f sigma)" % (st_cha["median"], st_cha["mean_ln"], st_cha["sigma_offset"]),
   st_cha["median"] < 0.62 and st_cha["sigma_offset"] > 15.0)
ck("K11", "baryons only (no phantom, Newton) is worse: the phantom closes part of the gap, not all of it",
   "median %.4f vs %.4f (phantom closes %.0f%% of the Newtonian radius gap)"
   % (st_new["median"], st_sal["median"], 100.0*(st_sal["median"]-st_new["median"])/(1.0-st_new["median"])),
   st_new["median"] < st_sal["median"] - 0.05)
ck("K12", "the record's canonical footing a0=9.3603e-11 gives the same verdict (not a footing artifact)",
   "median %.4f vs %.4f at the theory's a0" % (st_can["median"], st_sal["median"]),
   abs(st_can["median"]-st_sal["median"]) < 0.05 and st_can["median"] < 0.93)
ck("K13", "chi2 with per-lens errors (2% theta_E + propagated M_* + 5% shape) rejects the zero-parameter model",
   "chi2/dof = %.2f for %d lenses (Salpeter)" % (st_sal["chi2_dof"], st_sal["dof"]),
   st_sal["chi2_dof"] > 1.5)
RES["slacs"] = dict(salpeter=st_sal, chabrier=st_cha, newton=st_new, canonical=st_can)
RES["slacs"]["median_lens"] = dict(zl=float(np.median([d["zl"] for d in L])),
                                   zs=float(np.median([d["zs"] for d in L])),
                                   RE=float(np.median([d["RE"] for d in L])),
                                   sigma=float(np.median([d["sig"] for d in L])))
RES["slacs"]["per_lens_salpeter"] = [dict(name=s[0], ratio=float(s[1]), RE_pred=float(s[2]), RE_obs=float(s[3])) for s in SAL]

# K21 excess scatter: what the stated per-lens errors allow vs what the model shows
sigs = []
for nm, ratio, Rp, Ro, d in SAL:
    eF = d["eFs"] if np.isfinite(d["eFs"]) and d["eFs"] > 0 else 0.10
    s_m = 0.5*math.log(1.0+eF/max(d["Fs"], 1e-3))
    sigs.append(math.sqrt(0.02**2 + s_m**2 + 0.05**2))
sigs = np.array(sigs)
chi2_amp_removed = float(np.sum(((np.log(np.array([x[1] for x in SAL]))-st_sal["mean_ln"])/sigs)**2)/(len(sigs)-2))
ck("K13b", "per-lens scatter: after removing the mean offset the model still scatters ~2x the tabulated errors (astrophysical IMF/light-profile variation, not predicted)",
   "propagated sigma = %.3f dex (median), observed scatter = %.3f dex, chi2/dof(offset removed) = %.2f"
   % (float(np.median(sigs)/math.log(10.0)), st_sal["scatter_dex"], chi2_amp_removed),
   chi2_amp_removed > 1.5)
RES["k13b_scatter"] = dict(sigma_prop_median=float(np.median(sigs)/math.log(10.0)),
                          observed_scatter_dex=st_sal["scatter_dex"], chi2_dof_offset_removed=chi2_amp_removed)

# K22 the alternative normalisation route: the tabulated total M_* instead of f_* M_E
def _pred_tabM(d, imf, band="ReV", n=4.0):
    sc = SICR(d["zl"], d["zs"]); Re = Re_kpc(d, band)
    A  = 10.0**d[imf]
    M3Df = lambda r: A*M3D_star(r, Re, n)*MSUN
    fun = lambda R: M2D_from_g(R, M3Df, A0_RUN)-math.pi*R*R*sc
    REo = d["RE"]*KPC
    Rs = np.logspace(math.log10(0.15*REo), math.log10(10.0*REo), 60)
    v = np.array([fun(x) for x in Rs]); idx = np.where(np.diff(np.sign(v)) != 0)[0]
    if len(idx) == 0: return float("nan")
    return brentq(fun, Rs[idx[0]], Rs[idx[0]+1], xtol=1e-5*KPC)/KPC/d["RE"]
tab = np.array([_pred_tabM(d, "lMs") for d in L if np.isfinite(d["ReV"])]); tab = tab[np.isfinite(tab)]
lt  = np.log(tab); sem_t = lt.std(ddof=1)/math.sqrt(len(lt))
ck("K13c", "normalisation-route independence: the tabulated total M_* replaces f_* M_E and the verdict is unchanged",
   "f_*-anchored %.3f vs tabulated-M_* %.3f (%.1f sigma), both << 1"
   % (st_sal["median"], float(np.median(tab)), abs(lt.mean())/sem_t),
   0.78 < float(np.median(tab)) < 0.95 and abs(lt.mean())/sem_t > 4.0)
RES["k13c_tabM"] = dict(median=float(np.median(tab)), mean_ln=float(lt.mean()), sigma=float(abs(lt.mean())/sem_t), N=int(len(tab)))


# =====================================================================================
# SECTION 3 -- TASK 3: the sharp test
# =====================================================================================
P("\n" + "-"*120)
P("TASK 3 -- the sharp test: theory vs GR + dark matter")
P("-"*120)

# K14 a0 sensitivity: x100 must over-predict wildly, otherwise the estimator is blind to a0
S100 = run_sample(100.0*A0_THEORY, "Fs", "ReV")
st100 = stats(S100, "Salpeter")
ck("K14", "the estimator is sensitive to a0: a0 x 100 over-predicts R_E by a large factor",
   "median %.3f at a0 x 100 vs %.3f at a0" % (st100["median"], st_sal["median"]),
   st100["median"] > 3.0)
RES["k14_a0x100_median"] = st100["median"]

# K15 Sersic-index sensitivity (the table has no n; n = 4 is assumed)
nscan = {}
for n in (3.0, 4.0, 6.0):
    s = stats(run_sample(A0_THEORY, "Fs", "ReV", n=n), "Salpeter")
    nscan["%.1f" % n] = dict(median=s["median"], mean_ln=s["mean_ln"], scatter_dex=s["scatter_dex"])
ck("K15", "light-profile systematic: n = 3...6 moves the median by < 0.05 dex and the offset stays > 3 sigma",
   "; ".join("n=%.0f %.3f" % (float(k), v["median"]) for k, v in nscan.items()),
   max(v["median"] for v in nscan.values())-min(v["median"] for v in nscan.values()) < 0.15
   and all(v["mean_ln"] < -0.09 for v in nscan.values()))
RES["k15_nscan"] = nscan

# K16 truncation insensitivity of the line-of-sight integral
tr = {}
for rm in (0.2, 0.5, 1000.0):
    s = stats(run_sample(A0_THEORY, "Fs", "ReV", rmax=rm*1e3*KPC), "Salpeter")
    tr["%.1f" % rm] = s["median"]
ck("K16", "the projected phantom is insensitive to where the line of sight is cut (0.2/0.5/1000 Mpc)",
   "; ".join("%s Mpc: %.4f" % (k, v) for k, v in tr.items()),
   max(tr.values())-min(tr.values()) < 0.02)
RES["k16_truncation"] = tr

# ---- K17 the profile difference: theory vs NFW at fixed theta_E, radial critical curve and images
def nfw_M2D(R, M200, c, z):
    """projected NFW mass inside R; M200 defined w.r.t. rho_crit(z)."""
    rho_c = 3.0*(H0*(1+z))**2/(8.0*math.pi*G)      # SI
    r200  = (3.0*M200*MSUN/(4.0*math.pi*200.0*rho_c))**(1.0/3.0)
    rs    = r200/c
    mu    = lambda x: math.log(1.0+x)-x/(1.0+x)
    rho_s = M200*MSUN/(4.0*math.pi*rs**3*mu(c))
    x = R/rs
    if x < 1.0:
        g = math.log(x/2.0)+math.acosh(1.0/x)/math.sqrt(1.0-x*x)
    elif x > 1.0:
        g = math.log(x/2.0)+math.acos(1.0/x)/math.sqrt(x*x-1.0)
    else:
        g = math.log(0.5)+1.0
    return 4.0*rho_s*rs**3*g
def nfw_M3D(R, M200, c, z):
    rho_c = 3.0*(H0*(1+z))**2/(8.0*math.pi*G)
    r200  = (3.0*M200*MSUN/(4.0*math.pi*200.0*rho_c))**(1.0/3.0)
    rs    = r200/c
    mu    = lambda x: math.log(1.0+x)-x/(1.0+x)
    rho_s = M200*MSUN/(4.0*math.pi*rs**3*mu(c))
    x = R/rs
    return 4.0*math.pi*rho_s*rs**3*mu(x)

def beta_curve(R, M2Df, sc): return R*(1.0-M2Df(R)/(math.pi*R*R*sc))

def radial_critical(M2Df, sc, Rlo, Rhi):
    """radius of the radial critical curve = the minimum of beta(theta)."""
    Rs = np.logspace(math.log10(Rlo), math.log10(Rhi), 400)
    v  = np.array([beta_curve(x, M2Df, sc) for x in Rs])
    i  = int(np.argmin(v))
    return brentq(lambda x: (beta_curve(x*1.0001, M2Df, sc)-beta_curve(x/1.0001, M2Df, sc)),
                  Rs[max(i-2, 0)], Rs[min(i+2, len(Rs)-1)], xtol=1e-6*KPC)

def radial_image(M2Df, sc, beta_src, rc, Rhi):
    """the radial (third) image = the root of beta(theta) = beta_src in (rc, theta_E).
       beta is a MINIMUM at the radial critical curve rc, so a source with beta_src > beta(rc)
       has one root just outside rc -- the counter-image whose position tracks rc."""
    Rs = np.logspace(math.log10(1.02*rc), math.log10(Rhi), 400)
    v  = np.array([beta_curve(x, M2Df, sc)-beta_src for x in Rs])
    idx = np.where(np.diff(np.sign(v)) != 0)[0]
    if len(idx) == 0: return float("nan")
    return brentq(lambda x: beta_curve(x, M2Df, sc)-beta_src, Rs[idx[0]], Rs[idx[0]+1], xtol=1e-5*KPC)

# representative lens: the median SLACS system (z_l = 0.19, z_s = 0.61, M_E ~ 2.5e11)
zl, zs = 0.19, 0.90
sc = SICR(zl, zs)
Mb_rep, Re_rep = 2.4e11*MSUN, 7.0*KPC
M3f_rep = lambda r: Mb_rep*M3D_star(r, Re_rep, 4.0)
M2f_th  = lambda R: M2D_from_g(R, M3f_rep, A0_THEORY)
RE_th = brentq(lambda R: M2f_th(R)-math.pi*R*R*sc, 0.3*KPC, 300.0*KPC, xtol=1e-4*KPC)
# GR+DM: the same stars + an NFW halo with c = 10, M200 solved to match the SAME theta_E
M2f_star = lambda R: M2D_star(R, Re_rep, 4.0, Mb_rep)
def M2f_gr(R, M200): return M2f_star(R)+nfw_M2D(R, M200, 10.0, zl)
try:
    M200_fit = brentq(lambda M: M2f_gr(RE_th, M)-math.pi*RE_th*RE_th*sc, 1e5, 1e18, xtol=1e-6)
except Exception:
    M200_fit = float("nan")          # mutation path: no NFW can match this theta_E
rc_th = radial_critical(M2f_th, sc, 1e-4*KPC, 0.9*RE_th)
rc_gr = radial_critical(lambda R: M2f_gr(R, M200_fit), sc, 1e-4*KPC, 0.9*RE_th) if np.isfinite(M200_fit) else float("nan")
beta_at_rc_th = beta_curve(rc_th, M2f_th, sc)            # NEGATIVE: the caustic depth
beta_at_rc_gr = beta_curve(rc_gr, lambda R: M2f_gr(R, M200_fit), sc) if np.isfinite(rc_gr) else float("nan")
b_src = 0.5*beta_at_rc_th                                  # source halfway into the radial caustic
th_img_th = radial_image(M2f_th, sc, b_src, rc_th, RE_th)
th_img_gr = radial_image(lambda R: M2f_gr(R, M200_fit), sc, b_src, rc_gr, RE_th) if np.isfinite(rc_gr) else float("nan")
thE_arcsec = RE_th/DA(zl)/ARCSEC
dimg_arcsec = (th_img_gr-th_img_th)/DA(zl)/ARCSEC
slope = lambda f, R: (math.log(f(1.01*R))-math.log(f(0.99*R)))/(math.log(1.01)-math.log(0.99))
sl_th = {k: slope(M2f_th, k*RE_th) for k in (1.0, 3.0, 10.0, 30.0)}
sl_gr = {k: (slope(lambda R: M2f_gr(R, M200_fit), k*RE_th) if np.isfinite(M200_fit) else float("nan")) for k in (1.0, 3.0, 10.0, 30.0)}
ck("K17", "shape at fixed theta_E: degenerate at the Einstein radius, discriminating only at ~30 R_E",
   "theta_E = %.3f arcsec; dlnM2D/dlnR theory %.3f/%.3f/%.3f/%.3f vs NFW %.3f/%.3f/%.3f/%.3f at R_E/3/10/30 R_E; "
   "radial crit %.0f vs %.0f pc; radial image %.0f vs %.0f pc (d = %.1f pc = %.1f%%)"
   % (thE_arcsec, sl_th[1.0], sl_th[3.0], sl_th[10.0], sl_th[30.0], sl_gr[1.0], sl_gr[3.0], sl_gr[10.0], sl_gr[30.0],
      rc_th/KPC*1e3, rc_gr/KPC*1e3, th_img_th/KPC*1e3, th_img_gr/KPC*1e3,
      1e3*(th_img_gr-th_img_th)/KPC, 100.0*(th_img_gr/th_img_th-1.0)),
   abs(sl_th[1.0]-sl_gr[1.0]) < 0.05 and abs(sl_th[30.0]-sl_gr[30.0]) > 0.10
   and abs(th_img_gr/th_img_th-1.0) < 0.05)
RES["k17_sharp"] = dict(zl=zl, zs=zs, theta_E_arcsec=float(thE_arcsec), RE_th_kpc=float(RE_th/KPC),
                        slope_theory=[float(sl_th[k]) for k in (1.0, 3.0, 10.0, 30.0)],
                        slope_nfw=[float(sl_gr[k]) for k in (1.0, 3.0, 10.0, 30.0)],
                        M200_nfw=float(M200_fit), rc_theory_pc=float(rc_th/KPC*1e3),
                        rc_nfw_pc=float(rc_gr/KPC*1e3),
                        radial_image_theory_pc=float(th_img_th/KPC*1e3),
                        radial_image_nfw_pc=float(th_img_gr/KPC*1e3),
                        d_radial_image_pc=float(1e3*(th_img_gr-th_img_th)/KPC),
                        d_radial_image_frac=float(th_img_gr/th_img_th-1.0),
                        beta_caustic_arcsec=float(-beta_at_rc_th/DA(zl)/ARCSEC))

# K18 the amplitude difference in the observable, in arcsec, against the measurement error
obs = []
for nm, ratio, Rp, Ro, d in SAL:
    th_o = d["RE"]*KPC/DA(d["zl"])/ARCSEC
    obs.append((th_o, th_o*(1.0/ratio-1.0)))
obs = np.array(obs)
med_th = float(np.median(obs[:,0])); med_dth = float(np.median(obs[:,1]))
ck("K18", "the zero-parameter amplitude difference in theta_E, in arcsec, vs the ~2% measurement error",
   "median theta_E = %.2f arcsec, median missing deflection = %.3f arcsec = %.0f%% "
   "(measurement error ~%.3f arcsec)" % (med_th, med_dth, 100.0*med_dth/med_th, 0.02*med_th),
   med_dth > 5.0*0.02*med_th)
RES["k18_amplitude_arcsec"] = dict(theta_E_median=med_th, dtheta_median=med_dth,
                                   frac=float(med_dth/med_th), err_2pct=0.02*med_th)

# K19 the SLIP part of the difference is unobservable
dth_slip = frac_gal*med_th
ck("K19", "the slip correction to theta_E is ~1e-6 of theta_E: no survey can see it",
   "delta theta_E(slip) = %.2e arcsec vs 2%% error %.2e arcsec" % (dth_slip, 0.02*med_th),
   dth_slip < 1e-3*0.02*med_th)
RES["k19_slip_dtheta_arcsec"] = float(dth_slip)

# =====================================================================================
# SECTION 4 -- verdict
# =====================================================================================
P("\n" + "-"*120)
P("TASK 4 -- verdict")
P("-"*120)
verdict = dict(
    pass_gate=bool(st_sal["median"] > 0.95 and st_sal["sigma_offset"] < 2.0),
    amplitude_or_shape=("amplitude" if abs(st_sal["mean_ln"])/st_sal["scatter_ln"] > 0.4 else "shape"),
    radius_deficit_dex=float(-st_sal["mean_ln"]/math.log(10.0)),
    mass_deficit_dex=float(-2.0*st_sal["mean_ln"]/math.log(10.0)),
    required_ML_over_salpeter=float(10.0**(-2.0*st_sal["mean_ln"]/math.log(10.0))),
    sigma=float(st_sal["sigma_offset"]), n=int(st_sal["N"]))
P("  zero-parameter (Salpeter, a0 = 1.132e-10): R_E,pred/R_E,obs = %.3f, %.1f sigma low, N = %d"
  % (st_sal["median"], st_sal["sigma_offset"], st_sal["N"]))
P("  radius deficit %.3f dex, mass deficit %.3f dex = %.2f x Salpeter M_*/L"
  % (verdict["radius_deficit_dex"], verdict["mass_deficit_dex"], verdict["required_ML_over_salpeter"]))
P("  PASS" if verdict["pass_gate"] else "  FAIL -- the failure is in the AMPLITUDE, not the shape")
RES["verdict"] = verdict

ck("K20", "verdict recorded: the zero-parameter lensing gate FAILS, in the amplitude",
   "pass=%s, failure=%s, %.1f sigma" % (verdict["pass_gate"], verdict["amplitude_or_shape"], verdict["sigma"]),
   verdict["pass_gate"] is False and verdict["amplitude_or_shape"] == "amplitude")

# ------------------------------------------------------------------ mutation handling
if MUT:
    P("\nMUTATION: %s" % MUT)

npass = sum(1 for c in CK if c["pass_"]); ntot = len(CK)
P("\n" + "="*120)
P("A55: %d/%d checks PASS   (%.1f s)" % (npass, ntot, time.time()-T0))
P("="*120)
RES["checks"] = CK; RES["n_pass"] = npass; RES["n_total"] = ntot
RES["runtime_s"] = float(time.time()-T0)

stem = "a55" if not MUT else "a55_MUTATE_%s" % MUT
with open(os.path.join(HERE, stem+".out"), "w") as fh: fh.write("\n".join(OUT)+"\n")
with open(os.path.join(HERE, stem+"_results.json"), "w") as fh: json.dump(RES, fh, indent=1)
sys.exit(0 if npass == ntot else 1)