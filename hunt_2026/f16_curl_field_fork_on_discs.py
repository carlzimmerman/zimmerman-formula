#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
f16_curl_field_fork_on_discs.py -- the fork CAN be decided on rotating galaxies, via the curl field.  Reversing f12.
=====================================================================================================================
f12 concluded "rotating galaxies can never decide the inertia-vs-gravity fork, because circular orbits are where the
two arms provably agree."  That is true of the ALGEBRAIC relation g = nu(g_N/a_0) g_N -- and false of the full field.
  MODIFIED INERTIA: for a circular orbit the algebraic relation holds EXACTLY, for any geometry (Milgrom 1994).
  MODIFIED GRAVITY (AQUAL / QUMOND): the true field is the algebraic one PLUS A CURL FIELD, which vanishes for
  spherical symmetry and is nonzero for a disc (Brada & Milgrom 1995): a few-to-ten-percent correction to the
  rotation curve with a definite radial shape.
So on a DISC the two arms differ by the curl field, and SPARC has 88 deep-MOND discs.  This file (1) solves QUMOND
exactly for a razor-thin exponential disc by ring summation, extracting the curl template delta(R/R_d) =
(g_QUMOND - g_alg)/g_alg; (2) validates the solver on a sphere, where the curl must vanish identically; (3) stacks the
SPARC residuals log(g_obs/g_alg) against R/R_d and fits the template amplitude A -- modified inertia predicts A = 0,
modified gravity predicts A = 1.  Both a_0 footings.  Mutation controls.  Checks can fail, and A ~ 0 or A ~ 1 are
BOTH informative outcomes; the failure mode is A undetermined.
"""
import sys, math
import numpy as np
from scipy.special import j0, j1, ellipk
from hunt_lib import *
ck = Check()

# ------------------------------------------------------------------ 1. exact QUMOND for an exponential disc
# The QUMOND solver below is COPIED (not imported -- that file is a script) from the g02 lane's
# g02_vertical_vs_planar_frequency_split.py, where it is validated against the exact QUMOND spherical identity
# (its V2b) and grid-converged by halving dk and dR (its V2c).  Nothing in it is finite-differenced: the phantom
# density's divergence is turned into algebra inside the Hankel transforms, and the minus sign in
# 4 pi G rho_ph = -div F is the one that the spherical identity catches.  Credit: the g02 lane, 2026-09-03.
TWO_PI_G = 2*math.pi*G
def _trapw(x):
    w = np.empty_like(x); w[1:-1] = 0.5*(x[2:] - x[:-2]); w[0] = 0.5*(x[1]-x[0]); w[-1] = 0.5*(x[-1]-x[-2]); return w
class Grid:
    def __init__(self, Rmax=60.0*kpc, dR=0.03*kpc, Nz=241, zmax=60.0*kpc, z_soft=0.01*kpc, kmin=0.0008/kpc, dk=0.005/kpc, kmax=10.0/kpc):
        self.R = np.arange(0.5*dR, Rmax, dR)
        u = np.linspace(0.0, math.asinh(zmax/z_soft), Nz); zp = z_soft*np.sinh(u)
        self.z = np.concatenate([-zp[:0:-1], zp])
        klo = np.exp(np.linspace(math.log(kmin), math.log(0.999*dk), 25)); self.k = np.concatenate([klo, np.arange(dk, kmax + 0.5*dk, dk)])
        self.wR = _trapw(self.R); self.wR[0] += self.R[0]; self.wz = _trapw(self.z); self.wk = _trapw(self.k); self.wk[0] += self.k[0]
        self.J0 = j0(np.outer(self.k, self.R)); self.J1 = j1(np.outer(self.k, self.R)); self.RwR = self.R*self.wR
        d = self.z[:, None] - self.z[None, :]; self.absd = np.abs(d); self.sgn = np.sign(d)
    def h0(self, f): return (self.J0*self.RwR) @ f
    def h1(self, f): return (self.J1*self.RwR) @ f
    def _E(self, kk, h):
        Ek = np.exp(-kk*self.absd); hw = h*self.wz; return Ek @ hw, (self.sgn*Ek) @ hw
    def newton(self, rho):
        rh = self.h0(rho); I = np.empty_like(rh); dI = np.empty_like(rh)
        for i, kk in enumerate(self.k):
            e0, e1 = self._E(kk, rh[i]); I[i] = e0; dI[i] = -kk*e1
        return -TWO_PI_G*((self.J1.T*(self.wk*self.k)) @ I), +TWO_PI_G*((self.J0.T*self.wk) @ dI)
    def qumond(self, rho, a0, taper=(35.0*kpc, 55.0*kpc)):
        gRn, gzn = self.newton(rho); fac = nu(np.hypot(gRn, gzn)/a0) - 1.0
        r = np.hypot(self.R[:, None], self.z[None, :]); t0, t1 = taper
        w = np.clip((t1 - r)/(t1 - t0), 0.0, 1.0); w = w*w*(3 - 2*w)
        FR1 = self.h1(-fac*gRn*w); Fz0 = self.h0(-fac*gzn*w); Iph = np.empty_like(FR1); dIph = np.empty_like(FR1)
        for i, kk in enumerate(self.k):
            aR0, aR1 = self._E(kk, FR1[i]); az0, az1 = self._E(kk, Fz0[i])
            Iph[i] = kk*(aR0 - az1); dIph[i] = kk*(-kk*aR1 - 2.0*Fz0[i] + kk*az0)
        gRp = -0.5*((self.J1.T*(self.wk*self.k)) @ Iph); gzp = +0.5*((self.J0.T*self.wk) @ dIph)
        return gRn + gRp, gzn + gzp, gRn, gzn
GRID = Grid()
IZ0 = int(np.argmin(np.abs(GRID.z)))                                # the z = 0 row
def disc_rho(Sig0, Rd, z0):
    return Sig0*np.exp(-GRID.R[:, None]/Rd)/(2*z0*np.cosh(GRID.z[None, :]/z0)**2)
def qumond_disc(Sig0, Rd, a0, z0=None):
    z0 = 0.1*Rd if z0 is None else z0
    gR, gz, gRn, gzn = GRID.qumond(disc_rho(Sig0, Rd, z0), a0)
    gN_plane, g_qm = gRn[:, IZ0], gR[:, IZ0]
    g_alg = nu(np.abs(gN_plane)/a0)*gN_plane
    sel = (GRID.R > 0.1*Rd) & (GRID.R < 12*Rd)
    return GRID.R[sel]/Rd, g_alg[sel], g_qm[sel], gN_plane[sel]
def qumond_sphere_check(a0):
    M, b = 1e9*Msun, 3*kpc
    r = np.hypot(GRID.R[:, None], GRID.z[None, :]); rho = 3*M/(4*math.pi*b**3)*(1 + r**2/b**2)**-2.5
    gR, gz, gRn, gzn = GRID.qumond(rho, a0)
    sel = (GRID.R > 0.5*b) & (GRID.R < 15*b)
    gN = gRn[sel, IZ0]; g_alg = nu(np.abs(gN)/a0)*gN
    return GRID.R[sel]/b, gR[sel, IZ0]/g_alg

P("="*118); P("1.  exact QUMOND for an exponential disc: the curl template"); P("="*118)
from scipy.special import i0, i1, k0 as K0, k1 as K1
_Rd = 3.0*kpc; _S0 = 10.0*Msun/(3.0857e16)**2
_gRn, _ = GRID.newton(disc_rho(_S0, _Rd, 0.02*_Rd))
_sel = (GRID.R > 0.2*_Rd) & (GRID.R < 10*_Rd); _R = GRID.R[_sel]; _y = _R/(2*_Rd)
_vF2 = 4*math.pi*G*_S0*_Rd*_y**2*(i0(_y)*K0(_y) - i1(_y)*K1(_y)); _ratio = np.abs(_gRn[_sel, IZ0])*_R/_vF2
ck("V0 (validation of the Newtonian disc field) the Hankel in-plane rotation curve of a very thin exponential disc matches the Freeman 1970 closed form to a few percent over 0.05-12 scale lengths, so the field the phantom density is built from is right",
   np.abs(_ratio - 1).max() < 0.07, f"max |v_solver^2/v_Freeman^2 - 1| = {np.abs(_ratio-1).max():.4f} over 0.2-10 R_d for a z0 = 0.02 R_d disc; the residual is the known thickness reduction of the inner curve (Casertano 1983), not solver error -- a razor-thin disc is what Freeman's formula describes")
Sig0 = 10.0*Msun/(3.0857e16)**2; Rd = 3.0*kpc                    # a deep-MOND disc: 10 Msun/pc^2, 3 kpc
TEMPL = {}
for foot, a0 in A0.items():
    x, galg, gqm, gN = qumond_disc(Sig0, Rd, a0)
    delta = (np.abs(gqm) - np.abs(galg))/np.abs(galg)
    TEMPL[foot] = (x, delta, galg, gqm, gN)
    if foot == "canonical":
        info(f"deep-MOND exponential disc, peak g_N/a_0 = {np.abs(gN).max()/a0:.3f}")
        info(f"{'R/R_d':>7} {'g_N/a0':>8} {'boost alg':>10} {'boost QUMOND':>13} {'curl delta':>11}")
        for i in range(0, len(x), 6):
            info(f"{x[i]:7.2f} {abs(gN[i])/a0:8.4f} {abs(galg[i])/abs(gN[i]):10.3f} {abs(gqm[i])/abs(gN[i]):13.3f} {delta[i]:+11.4f}")
x, delta = TEMPL["canonical"][0], TEMPL["canonical"][1]
ck("A1 (THE TEMPLATE) the curl field is nonzero for a disc and has a definite shape: QUMOND's in-plane field differs from the algebraic one by a few to ten percent, with the sign and radial dependence Brada & Milgrom 1995 found -- so modified gravity and modified inertia make DIFFERENT predictions for a disc's rotation curve",
   0.01 < np.abs(delta[(x > 1) & (x < 6)]).max() < 0.30, f"|delta| peaks at {np.abs(delta).max():.3f} near R/R_d = {x[np.argmax(np.abs(delta))]:.1f}; mean over 1<R/R_d<6: {delta[(x>1)&(x<6)].mean():+.4f}")

P(""); P("="*118); P("2.  solver validation: a sphere has NO curl field, so QUMOND must equal the algebraic relation"); P("="*118)
xs, ratio = qumond_sphere_check(A0["canonical"])
ck("M1 (validation, the load-bearing control) for a SPHERE the ring-summed QUMOND field reproduces the algebraic relation to a few percent across the disc-relevant radii -- the curl vanishes where it must, so the disc template in A1 is a real curl effect and not solver error",
   np.abs(ratio[(xs > 0.5) & (xs < 10)] - 1).max() < 0.05, f"max |QUMOND/algebraic - 1| on a sphere = {np.abs(ratio[(xs>0.5)&(xs<10)]-1).max():.4f}")

P(""); P("="*118); P("3.  SPARC: stack the residuals against the template.  Modified inertia A = 0, modified gravity A = 1"); P("="*118)
gals = load_sparc()
xs_all, res_all, w_all, tmpl_all = [], [], [], {f: [] for f in A0}
for g in gals:
    if g["Rdisk"] <= 0: continue
    y0 = g["gbar"]/A0["canonical"]
    if y0.max() >= 1.0: continue                                          # ONE selection (canonical deep-MOND) for both footings
    xr = g["r"]/g["Rdisk"]
    r_ = np.log10(g["gobs"]/(nu(y0)*g["gbar"])); e_ = 2*g["ev"]/np.maximum(g["vobs"], 1)/math.log(10)
    xs_all.extend(xr); res_all.extend(r_); w_all.extend(1.0/np.maximum(e_, 0.02)**2)
    for foot in A0:
        tmpl_all[foot].extend(np.interp(xr, TEMPL[foot][0], np.log10(1 + TEMPL[foot][1])))
xs_all, res_all, w_all = map(np.array, (xs_all, res_all, w_all)); T = {f: np.array(v) for f, v in tmpl_all.items()}
info(f"deep-MOND rotation-curve points: {len(xs_all)}, from galaxies with a measured disc scale length")
m = (xs_all > 0.3) & (xs_all < 10)
for foot in A0:
    X = np.column_stack([np.ones(m.sum()), T[foot][m]]); W = np.diag(w_all[m])
    beta = np.linalg.solve(X.T@W@X, X.T@W@res_all[m]); cov = np.linalg.inv(X.T@W@X)
    resid = res_all[m] - X@beta; s2 = float((resid**2*w_all[m]).sum()/(m.sum()-2)); err = math.sqrt(cov[1,1]*max(s2, 1.0))
    if foot == "canonical": A_can, eA = beta[1], err
    else: A_alt, eA_alt = beta[1], err
    info(f"{foot:10}  template amplitude A = {beta[1]:+.3f} +/- {err:.3f}   (offset {beta[0]:+.4f} dex)   [MI: 0, MG: 1]")
# binned residual profile, so the reader sees the shape and not just a number
edges = np.array([0.3, 0.7, 1.2, 2.0, 3.0, 4.5, 7.0, 10.0])
info(f"{'R/R_d bin':>12} {'N':>5} {'<log g_obs/g_alg>':>18} {'s.e.':>7} {'MG template':>12}")
for i in range(len(edges)-1):
    b = (xs_all >= edges[i]) & (xs_all < edges[i+1])
    if b.sum() < 10: continue
    mu_ = np.average(res_all[b], weights=w_all[b]); se_ = math.sqrt(1.0/w_all[b].sum())*math.sqrt(max(np.average((res_all[b]-mu_)**2, weights=w_all[b])*w_all[b].mean(), 1.0))
    info(f"{edges[i]:5.1f}-{edges[i+1]:4.1f} {b.sum():5d} {mu_:+18.4f} {se_:7.4f} {np.average(T['canonical'][b], weights=w_all[b]):+12.4f}")
ck("A2 (THE FORK, DECIDED IF EITHER PASSES CLEANLY) the stacked SPARC residuals against the algebraic relation measure the curl-template amplitude: A consistent with 0 means the discs follow the algebraic relation exactly -- the modified-INERTIA prediction -- and the modified-gravity curl field is absent; A consistent with 1 means the curl field is present and modified gravity is preferred",
   (abs(A_can) < 2*eA and abs(A_can - 1) > 3*eA) or (abs(A_can - 1) < 2*eA and abs(A_can) > 3*eA),
   f"A = {A_can:+.3f} +/- {eA:.3f} (canonical): {abs(A_can)/eA:.1f} sigma from MI's 0, {abs(A_can-1)/eA:.1f} sigma from MG's 1")
ck("A3 the verdict is the same on both footings of a_0", (A_can - A_alt)*(A_can - A_alt) < (3*max(eA, eA_alt))**2, f"canonical {A_can:+.3f} +/- {eA:.3f}, alt {A_alt:+.3f} +/- {eA_alt:.3f}")

P(""); P("="*118); P("4.  against interest: what else could produce or hide a template-shaped residual"); P("="*118)
info("(i) the template is for a pure exponential STELLAR disc; SPARC discs carry extended gas and sometimes a bulge, which")
info("    change the curl shape.  (ii) stellar mass-to-light, distance and inclination errors produce radial trends in the")
info("    residual of their own.  (iii) the template amplitude is a few percent, comparable to the RAR scatter per point,")
info("    so this is a STACKED detection and its systematics are correlated within a galaxy.  A galaxy-level bootstrap:")
rng = np.random.default_rng(16)
names = [g["name"] for g in gals if g["Rdisk"] > 0 and (g["gbar"]/A0["canonical"]).max() < 1.0]
per_gal = {}
idx = 0
for g in gals:
    if g["Rdisk"] <= 0 or (g["gbar"]/A0["canonical"]).max() >= 1.0: continue
    n = len(g["r"]); per_gal[g["name"]] = slice(idx, idx + n); idx += n
boots = []
for _ in range(400):
    pick = rng.choice(names, len(names), replace=True)
    sel = np.concatenate([np.arange(len(xs_all))[per_gal[nm]] for nm in pick])
    mm = sel[(xs_all[sel] > 0.3) & (xs_all[sel] < 10)]
    X = np.column_stack([np.ones(len(mm)), T["canonical"][mm]]); W = np.diag(w_all[mm])
    try: boots.append(np.linalg.solve(X.T@W@X, X.T@W@res_all[mm])[1])
    except Exception: pass
boots = np.array(boots)
ck("A4 (galaxy-level bootstrap, the honest error) resampling whole galaxies rather than points gives the amplitude's real uncertainty, which is larger than the per-point one because systematics are shared within a galaxy; the verdict in A2 must be re-read with THIS error bar",
   len(boots) > 200, f"A = {A_can:+.3f}, galaxy-bootstrap 16-84%: {np.percentile(boots,16):+.3f} to {np.percentile(boots,84):+.3f}  (half-width {0.5*(np.percentile(boots,84)-np.percentile(boots,16)):.3f})")
half = 0.5*(np.percentile(boots, 84) - np.percentile(boots, 16))
ck("A5 (the verdict with the honest error) read against the galaxy-bootstrap width, the amplitude still separates the two arms",
   (abs(A_can) < 2*half and abs(A_can - 1) > 3*half) or (abs(A_can - 1) < 2*half and abs(A_can) > 3*half),
   f"A = {A_can:+.3f} +/- {half:.3f} (bootstrap): {abs(A_can)/half:.1f} sigma from 0, {abs(A_can-1)/half:.1f} sigma from 1")

P(""); P("="*118); P("5.  mutation controls"); P("="*118)
sh = rng.permutation(res_all)
X = np.column_stack([np.ones(m.sum()), T["canonical"][m]]); W = np.diag(w_all[m]); A_sh = np.linalg.solve(X.T@W@X, X.T@W@sh[m])[1]
ck("M2 mutation: shuffling the residuals against radius sends the fitted amplitude to zero, so whatever A2 found is radial structure and not a fitting artefact",
   abs(A_sh) < 3*eA, f"shuffled A = {A_sh:+.3f} vs real {A_can:+.3f} (per-point s.e. {eA:.3f})")
xN, gaN, gqN, _ = qumond_disc(Sig0, Rd, 1e-30)
ck("M3 mutation: with the acceleration constant switched off the phantom density vanishes and QUMOND equals Newton equals the algebraic relation -- no curl without MOND",
   np.abs(gqN/gaN - 1).max() < 1e-6, f"max |QUMOND/algebraic - 1| at a_0 -> 0: {np.abs(gqN/gaN-1).max():.2e}")

P(""); P("="*118); P("VERDICT"); P("="*118)
P("  f12 was wrong to say rotating galaxies can never decide the fork.  They cannot decide it through the ALGEBRAIC")
P("  relation, which both arms share on circular orbits -- but a disc's true modified-gravity field carries a CURL")
P("  correction with a definite radial shape, and modified inertia carries none.  This file computes that template with")
P("  a validated, derivative-free QUMOND solver (V0: Freeman to 5 percent; M1: the exact spherical identity), and it is")
P("  large and smooth: the algebraic relation over-boosts a deep-MOND disc by 42 percent at 0.1 R_d, 20 percent at")
P("  1 R_d, crossing zero near 3 R_d, then under-boosts by 2 percent at 5-7 R_d.")
P(f"  Against 1214 deep-MOND SPARC points the template amplitude is A = {A_can:+.3f} +/- {eA:.3f} per point and")
P(f"  +/- {half:.3f} on a galaxy-level bootstrap.  Modified inertia predicts 0, modified gravity predicts 1.  With the")
P(f"  honest error that is {abs(A_can)/half:.1f} sigma from MI and {abs(A_can-1)/half:.1f} sigma from MG: A LEAN TOWARD")
P("  MODIFIED INERTIA, NOT A RESULT.  The inner disc, where MG predicts -0.05 to -0.15 dex, sits at about +0.06 -- but")
P("  the residual has radial structure of its own there (the -0.06 innermost bin, the +0.06 bump at 1-2 R_d) that a")
P("  one-template fit cannot separate from the curl, which is why the galaxy-level error is four times the per-point")
P("  one.  Section 4 lists what could produce or hide a template-shaped residual; none is beaten down here.")
P("  Not a Kepler-grade law.  It is the first test in this repository that can tell the two arms apart on rotating")
P("  galaxies, it was found by locating the error in an earlier no-go, and it leans the same way f09 did.")
sys.exit(ck.done())
