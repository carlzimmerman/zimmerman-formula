#!/usr/bin/env python3
"""Unit tests for the lane-B grid solver pieces.
A: multipole projection + radial Green integrals on a SYNTHETIC axisymmetric source
   rho = A * P2(xi) * gaussian(ln r) -> Q2 analytic = (12 pi G/5) Int rho2/r dr (1D quad).
   (tests the l=2 extraction machinery end-to-end incl. trapz-on-log-grid)
B: closed-form rho_ph vs brute-force numerical divergence of F = delta(Y) g
   (tests the g.grad(delta) algebra)
C: sanity - the SPHERICAL (l=0) enclosed phantom mass at large r for the raw law
   must approach M_ph(<r) = delta(y(r)) * M  (flux theorem)
"""
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy import integrate

G = 6.674e-11; Msun = 1.989e30; GM = G*Msun; AU = 1.495978707e11
A0 = 9.362e-11
C_DEEP = 0.98224

# ---------- pieces copied from laneB_q2_solve (kept in sync manually) ----------
def rho_ph_closed(r, xi, delta, dln, eN, a0):
    ge = eN*a0
    gs = GM/r**2
    Y2 = gs**2 + ge**2 - 2.0*gs*ge*xi
    Yp = np.sqrt(Y2); y = Yp/a0
    dY = delta(y); dlnY = dln(y)
    dprime = dY*dlnY/Yp
    gdot = dprime * gs/(Yp*r) * (2.0*(gs-ge*xi)**2 - ge**2*(1.0-xi**2))
    return -gdot/(4.0*np.pi*G)   # rho_ph = -div[delta g]/(4piG)  (div g = -4piG rho)

def q2_from_source(rho_fn, r_eval, rmin, rmax, Nr=6000, Nxi=300):
    r = np.logspace(np.log10(rmin), np.log10(rmax), Nr)
    xi, w = leggauss(Nxi)
    R = r[:, None]; XI = xi[None, :]
    rho = rho_fn(R, XI)
    P2 = 0.5*(3.0*XI**2-1.0)
    S2 = 2.5*np.sum(rho*P2*w[None, :], axis=1)
    lnr = np.log(r)
    m_in = r <= r_eval; m_out = r >= r_eval
    I_in = np.trapz(S2[m_in]*r[m_in]**5, x=lnr[m_in]) if m_in.sum() > 3 else 0.0
    I_out = np.trapz(S2[m_out], x=lnr[m_out])
    return (12.0*np.pi*G/5.0)*(I_in/r_eval**5 + I_out)

# =========================== TEST A: synthetic source ===========================
print("TEST A: synthetic rho = A*P2(xi)*exp(-(ln(r/rc))^2/(2 s^2))")
Aamp, rc, s = 1e-12, 500*AU, 0.5
def rho_syn(R, XI):
    return Aamp*0.5*(3*XI**2-1)*np.exp(-np.log(R/rc)**2/(2*s**2))
# analytic: rho2(r) = A*exp(...)  (since (5/2)Int P2^2 dxi = (5/2)(2/5)=1)
# interior Q2 at r_eval << rc:  Q2 = (12 pi G/5) Int rho2/r dr
# Int rho2/r dr = Int A exp(-u^2/2s^2) du (u=ln r/rc) = A s sqrt(2 pi)  (exact)
Q2_exact = 12*np.pi*G/5 * Aamp*s*np.sqrt(2*np.pi)
Q2_grid = q2_from_source(rho_syn, 9.58*AU, 1*AU, rc*1e3)
print(f"  Q2 exact = {Q2_exact:.6e}   Q2 grid = {Q2_grid:.6e}   ratio = {Q2_grid/Q2_exact:.6f}")
assert abs(Q2_grid/Q2_exact-1) < 1e-3, "TEST A FAILED"
print("  PASS\n")

# =========================== TEST B: divergence check ===========================
print("TEST B: closed-form rho_ph vs numerical div[delta(Y) g]/(4 pi G)")
def d_simple(y): return np.sqrt(0.25+1.0/y)-0.5
def dln_simple(y):
    # d(delta)/dy = -1/(2 y^2 sqrt(1/4+1/y));  dln = (y/delta) d(delta)/dy
    return -1.0/(2.0*y*np.sqrt(0.25+1.0/y)*d_simple(y))
eN = 1.2742; a0 = 1.20e-10
ge = eN*a0
def F(r, th):   # components of delta(Y)*g in spherical coords
    xi = np.cos(th)
    gs = GM/r**2
    Y = np.sqrt(gs**2+ge**2-2*gs*ge*xi)
    dl = d_simple(Y/a0)
    Fr = dl*(-gs+ge*xi); Fth = dl*(-ge*np.sin(th))
    return Fr, Fth
rt = np.sqrt(GM/ge)
rng = np.random.default_rng(1)
maxrel = 0.0
for r0, th0 in [(0.3*rt, 1.0), (1.0*rt, 0.5), (1.0*rt, 2.5), (3.0*rt, 1.2),
                (0.1*rt, 2.0), (10*rt, 0.8), (1.5*rt, 3.0), (0.7*rt, 0.2)]:
    h = 1e-5
    Frp, _ = F(r0*(1+h), th0); Frm, _ = F(r0*(1-h), th0)
    d_r2Fr = ((r0*(1+h))**2*Frp - (r0*(1-h))**2*Frm)/(2*r0*h)
    _, Ftp = F(r0, th0+h); _, Ftm = F(r0, th0-h)
    d_sinFt = (np.sin(th0+h)*Ftp - np.sin(th0-h)*Ftm)/(2*h)
    div = d_r2Fr/r0**2 + d_sinFt/(r0*np.sin(th0))
    rho_num = -div/(4*np.pi*G)
    rho_cl = rho_ph_closed(r0, np.cos(th0), d_simple, dln_simple, eN, a0)
    rel = abs(rho_num/rho_cl-1)
    maxrel = max(maxrel, rel)
    print(f"  r={r0/rt:5.2f} r_t, th={th0:.2f}:  rho_num={rho_num:+.6e}  rho_closed={rho_cl:+.6e}  rel={rel:.2e}")
assert maxrel < 1e-4, "TEST B FAILED"
print("  PASS\n")

# =========================== TEST C: flux theorem ===============================
print("TEST C: l=0 enclosed phantom mass vs delta(y)*M (flux theorem), raw law")
def d_raw(y): return C_DEEP*y**-0.5
def dln_raw(y): return -0.5 + 0*y
eN2 = 1.148
for rf in (0.03, 0.1, 0.3):
    r_chk = rf*np.sqrt(GM/(eN2*A0))
    # M_ph(<r) = Int rho_ph dV over sphere; use grid
    r = np.logspace(np.log10(0.05*AU), np.log10(r_chk), 4000)
    xi, w = leggauss(200)
    R = r[:, None]; XI = xi[None, :]
    rho = rho_ph_closed(R, XI, d_raw, dln_raw, eN2, A0)
    S0 = 0.5*np.sum(rho*w[None, :], axis=1)          # (1/2)Int rho dxi = monopole density
    Mph = np.trapz(4*np.pi*r**3*S0, x=np.log(r))
    y_r = (GM/r_chk**2)/A0
    Mflux = d_raw(y_r)*Msun                           # + external-flux correction O((ge/gs)^2)
    print(f"  r={rf:4.2f} r_t:  M_ph(grid)={Mph/Msun:.4e} Msun   delta*M={Mflux/Msun:.4e}   ratio={Mph/Mflux:.4f}")
print("  (ratio -> 1 at small r where the Sun dominates the flux)")
print("\nALL UNIT TESTS DONE")
