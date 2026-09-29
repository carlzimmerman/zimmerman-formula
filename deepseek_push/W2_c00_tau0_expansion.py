#!/usr/bin/env python3
"""W2 -- exact thin-window law c00(q) = A0 + A1*q (Z11 door; owns W2_*).

Door: MC7 (exit 0) measured c00(q) = lim_{tau0->0} E[D]/tau0 by extrapolation,
refuted the MC4 line, left the extrapolation model UNSETTLED. This lane derives
the thin-window law EXACTLY.

Pre-registered chain (Z11-WAVE_BRIEF.md, BEFORE any run): D = sum_j l_j
(1 - u_j.u_final); single-scatter dominance at O(tau0); E[mu_Thomson]=0;
c00(q) = E[ int_0^W s k(s) ds ], k(s) = 1 + q(r^2 + 2(p.u)s + s^2),
W = -(p.u) + sqrt((p.u)^2 + 1 - r^2); p volume-uniform, u isotropic.
=> A0 = E[W^2/2], A1 = E[r^2 W^2/2 + 2(p.u)W^3/3 + W^4/4].

Kills (pre-registered): K1 exact-vs-quadrature 1e-11 rel (two methods);
K2 parity vs MC7 measured c00 at q in {0,1,3}, any |z|>3 -> REJECTED exit 1.
K3 scope test at q=6 (refit MC7 smallest-4-tau0 points; records, no gate).
Honest scope: c1(q) NOT derived (W3 candidate); Lean cert = LR8 candidate.
"""
import json, os, sys, time
import numpy as np
from scipy.special import roots_legendre

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "W2_c00_tau0_expansion.out")
RESF = os.path.join(HERE, "W2_results.json")
_T0 = time.time(); LOG = []
def log(m):
    line = "[%7.1fs] %s" % (time.time() - _T0, m); LOG.append(line); print(line, flush=True)
def finish(rc, verdict, extra=None):
    RES = dict(title="W2 exact thin-window law c00(q)=A0+A1*q",
               pre_registration="Z11-WAVE_BRIEF.md (W2 door, registered before any run)",
               verdict=verdict, exit=rc, elapsed_s=round(time.time()-_T0,1), log=LOG)
    if extra: RES.update(extra)
    json.dump(RES, open(RESF, "w"), indent=1, default=str)
    with open(OUT, "a") as f: f.write("\n".join(LOG) + "\nVERDICT: %s (exit %d)\n" % (verdict, rc))
    print("VERDICT: %s (exit %d)" % (verdict, rc)); sys.exit(rc)

# ---------- K1: sympy exact A0, A1 via the cylindrical reduction ----------
log("K1: sympy exact derivation, cylindrical (rho,z) reduction")
import sympy as sp
x, w = sp.symbols("x w", positive=True, real=True)   # x = rho in [0,1]; z = s*w, s = sqrt(1-x^2)
s = sp.sqrt(1 - x**2)
# z-substitution z -> s*w on [-1,1], dz = s*dw; measure (3/(4pi)) * 2pi * x dx * dz
# integrand core: f(s - z) with z = s*w  => f(s(1-w))
Wexpr = s*(1 - w)
f_A0 = Wexpr**2 / 2
f_A1 = (x**2 + (s*w)**2) * Wexpr**2 / 2 + 2*(s*w)*Wexpr**3 / 3 + Wexpr**4 / 4
def cyl_exact(f):
    # inner: integrate over w in [-1,1], multiply by dz-factor s; then (3/2) * x over rho
    inner = sp.integrate(sp.expand(f * s), (w, -1, 1))
    outer = sp.integrate(sp.expand(sp.Rational(3, 2) * x * inner), (x, 0, 1))
    return sp.simplify(outer)
A0_ex = cyl_exact(f_A0)
A1_ex = cyl_exact(f_A1)
log("K1: sympy A0 = %s = %s" % (A0_ex, sp.nsimplify(A0_ex)))
log("K1: sympy A1 = %s = %s" % (A1_ex, sp.nsimplify(A1_ex)))
A0v, A1v = float(A0_ex), float(A1_ex)

# two independent quadratures: mpmath nested quad + Gauss-Legendre
import mpmath as mp
mp.mp.dps = 40
sm = lambda rho: mp.sqrt(1 - rho*rho)
g0 = lambda z, rho: (sm(rho) - z)**2 / 2
g1 = lambda z, rho: ((rho*rho + z*z)*(sm(rho)-z)**2)/2 + 2*z*(sm(rho)-z)**3/3 + (sm(rho)-z)**4/4
inner0 = lambda rho: mp.quad(lambda zz: g0(zz, rho), [-sm(rho), sm(rho)])
inner1 = lambda rho: mp.quad(lambda zz: g1(zz, rho), [-sm(rho), sm(rho)])
A0_mp = mp.mpf(3)/2*mp.quad(lambda r: r*inner0(r), [0, 1])
A1_mp = mp.mpf(3)/2*mp.quad(lambda r: r*inner1(r), [0, 1])
# Gauss-Legendre (numpy) nested, 2D
ng = 400
t_gl, w_gl = roots_legendre(ng)
rho_g = 0.5*(1 - t_gl); wr = 0.5*w_gl
z_g = t_gl[None, :]*np.sqrt(1 - rho_g**2)[:, None]; wz = w_gl[None, :]
s_g = np.sqrt(1 - rho_g**2)[:, None]
G0 = (s_g - z_g)**2 / 2
G1 = ((rho_g[:,None]**2 + z_g**2)*(s_g-z_g)**2)/2 + 2*z_g*(s_g-z_g)**3/3 + (s_g-z_g)**4/4
sJac = s_g  # dz = s*dt Jacobian for the z-substitution
A0_gl = 1.5*np.sum(wr[:,None]*wz*rho_g[:,None]*sJac*G0)
A1_gl = 1.5*np.sum(wr[:,None]*wz*rho_g[:,None]*sJac*G1)
rel = lambda a, b: abs(float(a) - float(b))/max(abs(float(b)), 1e-300)
r0mp, r1mp, r0gl, r1gl = rel(A0_mp, A0v), rel(A1_mp, A1v), rel(A0_gl, A0v), rel(A1_gl, A1v)
log("K1: mpmath dev A0 %.2e  A1 %.2e ; GL(400) dev A0 %.2e  A1 %.2e (gate 1e-11)" % (r0mp, r1mp, r0gl, r1gl))
if max(r0mp, r1mp, r0gl, r1gl) > 1e-11:
    finish(1, "K1 FIRED: exact-vs-quadrature mismatch", dict(A0=str(A0_ex), A1=str(A1_ex)))
log("K1 PASS: A0 = %s, A1 = %s (exact rationals)" % (A0_ex, A1_ex))

# ---------- K2: parity vs MC7 measured c00 at q in {0,1,3} ----------
m7 = json.load(open(os.path.join(HERE, "MC7_results.json")))
sel = m7["sel"]; QS = [0.0, 1.0, 3.0, 6.0, 10.0]
k2 = {}
for q in QS:
    key = next(k for k in (str(q), str(int(q)), q) if k in sel)
    c00_ex = A0v + A1v*q
    zsc = abs(float(sel[key]["c00"]) - c00_ex)/float(sel[key]["se00"])
    k2[q] = dict(exact=c00_ex, mc7=float(sel[key]["c00"]), se=float(sel[key]["se00"]), z=float(zsc))
    log("K2: q=%g: exact %.6f vs MC7 %.6f+-%.6f, z=%.2f %s" % (q, c00_ex, k2[q]["mc7"], k2[q]["se"], zsc,
        "GATE" if q in (0.0, 1.0, 3.0) else "scope"))
for q in (0.0, 1.0, 3.0):
    if k2[q]["z"] > 3:
        finish(1, "K2 FIRED at q=%g (z=%.2f > 3): exact c00(q)=A0+A1*q REJECTED" % (q, k2[q]["z"]), dict(k2=k2))
log("K2 PASS at q in {0,1,3}; q in {6,10} recorded as scope (MC7 extrapolation bias)")

# ---------- K3: scope test at q=6 -- O(tau0) extrapolation bias? ----------
pts = m7["meas"]["6.0"]["points"] if "6.0" in m7["meas"] else m7["meas"][6.0]["points"]
sub = sorted(pts, key=lambda p: p[0])[:4]
ts = np.array([p[0] for p in sub]); ys = np.array([p[1] for p in sub]); ses = np.array([p[2] for p in sub])
Wm = np.diag(1/ses**2); Amat = np.vstack([np.ones_like(ts), ts]).T
ata = Amat.T@Wm@Amat; cov = np.linalg.inv(ata)
sol = np.linalg.solve(ata, Amat.T@Wm@ys)
i6, se6 = float(sol[0]), float(np.sqrt(cov[0, 0]))
exact6 = A0v + A1v*6
z6 = abs(i6 - exact6)/se6
log("K3: q=6 refit (4 smallest tau0): intercept %.6f+-%.6f vs exact %.6f, z=%.2f" % (i6, se6, exact6, z6))
k3 = dict(intercept=i6, se=se6, exact=exact6, z=float(z6),
          note="fire => O(tau0)-bias explanation insufficient at q=6; records only")

finish(0, "BANKED: exact thin-window law c00(q) = A0 + A1*q, A0 = %s, A1 = %s "
          "(K1 two-method quadrature <= 1e-11; K2 z = %.2f/%.2f/%.2f at q = 0/1/3); "
          "q in {6,10} scope recorded (K3 z=%.2f). Successors: W3 (exact c1(q)), "
          "LR8 (Lean certs of A0/A1)" % (A0_ex, A1_ex, k2[0.0]["z"], k2[1.0]["z"], k2[3.0]["z"], z6),
       dict(A0=str(A0_ex), A1=str(A1_ex), k2=k2, k3=k3,
            quad=dict(A0_mpmath=str(A0_mp), A1_mpmath=str(A1_mp), A0_gl=str(A0_gl), A1_gl=str(A1_gl))))
