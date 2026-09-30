#!/usr/bin/env python3
"""CFG191_s3_solar_q2 -- item (c): the Solar-System external-field quadrupole Q2 (QUMOND, point Sun) for P2 and nu_RAR.
Own derivation: QUMOND phantom density rho_ph = div[(nu-1) g_N]/(4 pi G), g_N = Sun + uniform external; the interior quadrupole coefficient
I2 = int rho_ph P2/r^3 d^3x (Q2 = 3 G I2). Two of my own routes: (R1) direct divergence (sympy) quadrature; (R2) integration by parts (smooth integrand).
Cross-check: eq-(12) form transcribed in the in-repo g04 (second-hand). No CFG179 file is opened.
MUTATE=1 (M5): g_ext scaled to 0.2 x -> 'all P2 entries > 1' must fail."""
import warnings; warnings.filterwarnings("ignore")
import numpy as np, sympy as sp, math, re
from scipy.optimize import brentq
from numpy.polynomial.legendre import leggauss
from CFG191_common import Run, REPO, rel
np.seterr(all="ignore")
R = Run("CFG191_s3_solar_q2", "item (c): Solar-System quadrupole Q2 of a point Sun in the Galactic field (QUMOND)")
MUT = R.mutate
GM_SUN, AU = 1.32712440018e20, 1.495978707e11
CEIL = 1.6e-27 + 2*1.8e-27
G04 = REPO/"hunt_2026/g04_verify_cassini_q2_adversarial.out"
R.p(f"quoted inputs (in-repo, second-hand for me): Q2 ceiling {CEIL:.1e} s^-2 (Park+2026 1.6+-1.8e-27, 2 sigma); published anchors q(1)=0.094, q(1.5)=0.159, q(2)=0.221 for nu_RAR (Desmond+2024 Fig.1 caption, via {rel(G04)})")
R.p("  Q2 definition: Q2 = 3 G I2 with I2 = int rho_ph P2(cos)/r^3 d^3x (the record's frozen convention, read in the CFG3 header); eq (10): Q2 = -(3 a0^{3/2}/(2 sqrt(GM))) q.")

nu_rar = lambda y: 1/(1 - np.exp(-np.sqrt(y)))
nu_p2 = lambda y: np.sqrt(1 + 1/y)
KERN = {"P2": nu_p2, "nu_RAR": nu_rar}

def eN_of(et, nu):    # Newtonian external field with x = y nu(y) = et
    return brentq(lambda y: y*nu(y) - et, 1e-12, 1e8)

# ---- R2: by parts.  I2~ = (3/4) int_0^inf dv int_-1^1 du (nu(|g|)-1)[e(5u^3-3u) + v^2(1-3u^2)],  |g|^2 = e^2 + v^4 - 2 e u v^2, v = r_M/r
def I2_byparts(e, nu, nx=240, vmax=1000.0, npan=90):
    xg, xw = leggauss(nx); vg, vw = leggauss(12)
    knee = max(4.0, 2*math.sqrt(e))
    edges = np.concatenate([np.linspace(0, knee, npan//2+1)[:-1], np.geomspace(knee, vmax, npan//2+1)])
    tot = 0.0
    for a, b in zip(edges[:-1], edges[1:]):
        vv = 0.5*(b-a)*vg + 0.5*(a+b); ww = 0.5*(b-a)*vw
        V, U = np.meshgrid(vv, xg, indexing="ij")
        g = np.sqrt(np.maximum(e*e + V**4 - 2*e*U*V*V, 1e-300))
        f = (nu(g) - 1)*(e*(5*U**3 - 3*U) + V*V*(1 - 3*U*U))
        tot += float(np.sum(ww[:, None]*xw[None, :]*f))
    return 0.75*tot

# ---- R1: direct divergence with sympy
rs, us, es = sp.symbols("r u e", positive=True)
def build_div(nu_expr):
    gr = -1/rs**2 + es*us
    gt_sin = -es*(1 - us**2)              # sin(theta) * g_theta, g_theta = -e sin(theta)
    y = sp.sqrt(es**2 + rs**-4 - 2*es*us*rs**-2)
    nuu = nu_expr(y) - 1
    Vr = nuu*gr; Vts = nuu*gt_sin
    div = sp.diff(rs**2*Vr, rs)/rs**2 - sp.diff(Vts, us)/rs
    return sp.lambdify((rs, us, es), div, "numpy")
divP2 = build_div(lambda y: sp.sqrt(1 + 1/y))
divRAR = build_div(lambda y: 1/(1 - sp.exp(-sp.sqrt(y))))
def I2_direct(e, divf, nx=600, rmin=1e-3, rmax=1e3, npan=400):
    # I2~ = (1/2) int dr/r int du (div V) P2(u)
    xg, xw = leggauss(nx); rg, rw = leggauss(8)
    edges = np.geomspace(rmin, rmax, npan+1)
    tot = 0.0
    for a, b in zip(edges[:-1], edges[1:]):
        lr = 0.5*(np.log(b)-np.log(a))*rg + 0.5*(np.log(b)+np.log(a)); w_ = 0.5*(np.log(b)-np.log(a))*rw
        r = np.exp(lr)
        Rr, Uu = np.meshgrid(r, xg, indexing="ij")
        d = divf(Rr, Uu, e)
        tot += float(np.sum(w_[:, None]*xw[None, :]*d*0.5*(3*Uu**2 - 1)))
    return 0.5*tot

def Q2_phys(I2t, a0):
    return 3*a0**1.5/math.sqrt(GM_SUN)*abs(I2t)

R.sec("C1  control: nu_RAR anchors and the two routes")
anch = {1.0: 0.094, 1.5: 0.159, 2.0: 0.221}
worst = 0
for et, qp in anch.items():
    e = eN_of(et, nu_rar); q2 = 2*abs(I2_byparts(e, nu_rar)); q1 = 2*abs(I2_direct(e, divRAR))
    worst = max(worst, abs(q2/qp - 1))
    R.p(f"  etilde={et}: published q {qp:.3f} | R2 by-parts {q2:.5f} ({q2/qp-1:+.2%}) | R1 direct-divergence {q1:.5f} ({q1/q2-1:+.2%} vs R2)")
    R.data[f"C1_{et}"] = dict(pub=qp, R2=q2, R1=q1)
R.check("C1a my by-parts route reproduces the published q anchors within 1% with NO fitted constant (Q2 normalisation = eq 10)", worst < 0.01, f"worst {worst:.2%}")
R.check("C1b my direct-divergence route (independent integrand) agrees with the by-parts route within 3% at the three anchors",
        all(abs(2*abs(I2_direct(eN_of(et, nu_rar), divRAR))/(2*abs(I2_byparts(eN_of(et, nu_rar), nu_rar))) - 1) < 0.03 for et in anch))
txt = " ".join(G04.read_text().split())
R.check("C1c the quoted g04 reference row (canonical 9.360e-11 ... 3.0015e-26 5.772) is present in its committed .out", "3.0015e-26 5.772" in txt and "3.2687e-26 6.286" in txt)
ref = {}
for foot, a0, refr in (("canonical", 9.360e-11, 5.772), ("alt", 1.130e-10, 6.286)):
    e = eN_of(2.146e-10/a0, nu_rar); rr = Q2_phys(I2_byparts(e, nu_rar), a0)/CEIL; ref[foot] = rr
    R.p(f"  nu_RAR, g_ext=2.146e-10, a0={a0:.3e}: Q2/ceiling = {rr:.3f} (g04 committed {refr})")
R.check("C1d my nu_RAR ratios at g04's inputs (g_ext 2.146e-10, a0 9.36e-11 / 1.13e-10) reproduce g04's 5.772 / 6.286 within 1.5%", abs(ref["canonical"]/5.772 - 1) < 0.015 and abs(ref["alt"]/6.286 - 1) < 0.015)
# convergence
e0 = eN_of(1.9, nu_p2)
R.p("  convergence (P2, etilde=1.9): by-parts vmax 200/1000/3000 -> " + ", ".join(f"{2*abs(I2_byparts(e0, nu_p2, vmax=v)):.5f}" for v in (200, 1000, 3000)) + "; nx 120/240/480 -> " + ", ".join(f"{2*abs(I2_byparts(e0, nu_p2, nx=n)):.5f}" for n in (120, 240, 480)))

R.sec("C2  HEADLINE TABLE: Q2 / 5.2e-27 s^-2 (QUMOND point Sun)")
scale = 0.2 if MUT else 1.0
if MUT: R.p("  MUTATE M5: g_ext scaled by 0.2")
tab = {}
R.p(f"  {'kernel':7s} {'footing':9s} {'a0':>10s} {'g_ext':>10s} {'etilde':>7s} {'e_N':>7s} {'q':>8s} {'Q2 [s^-2]':>11s} {'/ceiling':>9s}")
for kn, nu in KERN.items():
    for foot, a0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
        for gx in (1.778e-10, 2.146e-10):
            g = gx*scale; et = g/a0; e = eN_of(et, nu); It = I2_byparts(e, nu)
            Q2 = Q2_phys(It, a0); tab[(kn, foot, gx)] = Q2/CEIL
            R.p(f"  {kn:7s} {foot:9s} {a0:10.4e} {g:10.4e} {et:7.3f} {e:7.3f} {2*abs(It):8.5f} {Q2:11.3e} {Q2/CEIL:9.2f}")
R.data["table"] = {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in tab.items()}
p2v = [v for k, v in tab.items() if k[0] == "P2"]; rarv = [v for k, v in tab.items() if k[0] == "nu_RAR"]
R.p(f"  P2 range {min(p2v):.2f}-{max(p2v):.2f}; nu_RAR range {min(rarv):.2f}-{max(rarv):.2f}; union {min(p2v+rarv):.2f}-{max(p2v+rarv):.2f}; README/GATES 4.0-5.7")
R.check("C2a every P2 entry lies in [3.0, 6.5] and > 1 (FAIL of the strict law stands for QUMOND EFE)", all(1 < v and 3.0 <= v <= 6.5 for v in p2v))
R.check("C2b the union over the eight rows covers 4.0-5.7 to +-10% (min <= 4.4 and max >= 5.13)", min(p2v+rarv) <= 4.4 and max(p2v+rarv) >= 5.13, lb=False)
one_kernel_cov = any(min(v) <= 4.4 and max(v) >= 5.13 for v in (p2v, rarv))
R.p(f"  a single kernel alone spans both 4.0 and 5.7 (within 10%)? {one_kernel_cov}")
R.data["single_kernel_covers"] = bool(one_kernel_cov)

R.sec("C3  natural-scale arithmetic: a0/r_M")
for foot, a0, tg in (("canonical", 9.3603e-11, 15.1), ("alt", 1.1312e-10, 20.1)):
    rM = math.sqrt(GM_SUN/a0); v = a0/rM
    R.p(f"  {foot}: r_M = {rM/AU:.0f} AU, a0/r_M = {v:.3e} s^-2 = {v/CEIL:.1f} x ceiling (README {tg})")
    R.check(f"C3 {foot} natural scale {v/CEIL:.1f} x (README {tg}) reproduced", abs(v/CEIL - tg) < 0.3, lb=False)

R.sec("C4  rescue field: g_ext (fraction of V^2/R0 = 2.146e-10) at which Q2 = ceiling")
resc = {}
for kn, nu in KERN.items():
    for foot, a0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
        f = lambda fr: Q2_phys(I2_byparts(eN_of(fr*2.146e-10/a0, nu), nu, nx=120, npan=60), a0)/CEIL - 1
        try: fr = brentq(f, 0.02, 1.0, xtol=1e-3)
        except Exception: fr = float("nan")
        resc[(kn, foot)] = fr; R.p(f"  {kn:7s} {foot:9s}: g_ext fraction {fr:.3f} (g04 for nu_RAR canonical: 0.259)")
R.data["rescue"] = {f"{k[0]}|{k[1]}": v for k, v in resc.items()}

R.sec("C5  dependence audit")
R.p(f"  ratio spread across kernel x footing x g_ext: {min(p2v+rarv):.2f}-{max(p2v+rarv):.2f} (a factor {max(p2v+rarv)/min(p2v+rarv):.2f}); the quoted '4.0-5.7' is not one number.")
R.p("  NOT COVERED: AQUAL (vs QUMOND) Q2; E7's Q2 (no field equation); Jupiter (0.05%, quoted); the 3-D field geometry; ownership (Sun owns no phantom => host tide 1.6-2.6e-31, not recomputed here).")
R.p("  Unrelated quantities: the P2 alpha=1 monopole a0/2 (1279 x the Earth bound) and the host tide.")
R.sec("VERDICT (frozen rule)")
if not MUT:
    verdict = "AGREES WITH QUALIFICATION" if (all(1 < v <= 6.5 for v in p2v)) else "DISAGREES"
    R.finding("(c) Q2", verdict, f"P2 QUMOND Q2/ceiling {min(p2v):.2f}-{max(p2v):.2f}; nu_RAR {min(rarv):.2f}-{max(rarv):.2f}. The FAIL of the strict law stands for a QUMOND-type EFE at every kernel/footing/g_ext tested. The quoted 4.0-5.7 mixes kernels and the g_ext convention (single kernel spans both endpoints: {one_kernel_cov}); rescue field {min(v for v in resc.values() if v==v):.2f}-{max(v for v in resc.values() if v==v):.2f} of V^2/R0.")
R.finish()
