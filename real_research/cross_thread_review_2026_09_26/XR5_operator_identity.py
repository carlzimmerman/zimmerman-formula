#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR5 -- WHICH FORCE OPERATOR?  The action's region-local phantom (L361) against the particle-mesh operator (L377) and the
merger operator (L370), on one controlled test bed.

WHY.  The 2026-09-26 peer review (peer_review_2026_09_26/dark_sector/REPORT.md, 'Additional bridge'; NEXT_CALCULATIONS.md
item 1) found that the PM runs (retention, L377 -> L380/L386/L388) and the Harvey+2015 merger runs (L370 -> L371/L372/L373,
AT3) use different phantom operators, and no controlled error bound links either to the action.  This lane measures the
difference directly.

THE THREE OPERATORS (read from the code, not from the review; file:line).  f = gated switch, rho_b = baryons.
 (A) L361_bound_region_kernel.py:16-32 (field equations derived in R0, :86-122).  M^2 = m^2 (1 - f);
       (lap - M^2) w = 4 pi G f rho_b ;  (lap - M^2) P = div[f (nu(|grad w|/a0) - 1) grad w] + M^2 w ;
     in-region baryons move in phi + f P, web gas and the carrier in phi.  Dirichlet limit m -> inf: w = P = 0 outside the
     active set; finite 1/m = 0.2, 0.5 Mpc solved as written.  Gate: L359's geometric variable, the density CONTRAST
     1.5 (rho - rho_bar_m)/rho_c(z) (L359:107 'xs = 1.5 * L7.Om_a(a) * delta'; L377:119-120).
 (B) L377_full_construction_pm.py:117-127 (phantom): gate on the background-subtracted contrast (:119-120, p = 2, x_c0 = 2 at
     :94); the Newtonian field of ALL baryons on the mesh, 'poisson(1.5*Om*(rb - WB)/a)' (:123); the constitutive response
     masked to active cells (:124-125); curl-free projection 'poisson(-a*divw)' (:126-127) with L362's central-difference
     grad/div (L362:104-108) and spectral Poisson (L362:100-102); felt by ALL baryons (:163-164), the carrier Newtonian
     (:165); the trigger reads the phantom density (:176-178).
 (C) L370_boosted_infall_mergers.py:286-307 (phantom_felt): mask on the ABSOLUTE real density '1.5 * rreal / (RHOC0 *
     Ez2(z)) >= x_ceff' (:290; the docstring :19 states the contrast); connected regions labelled (:291-292), and only regions
     containing a given centre get a phantom; each region's field from its OWN baryons 'grid.field(rb * f)' (:296); masked
     response (:297-299); spectral projection (:301); felt only inside that region (:302-303); lensing density
     -div(gph)/(4 pi G) (:304-305).  L371:79-80, L372:252-253, L373:221-249 and AT3:322 load this machinery.
 All three use nu_mono (L340:104-117; L377:97-114 rebuilds it on a wider table; L370:136-155 identically).

METHOD.  (1) Identity: my 3-D re-implementations of (B) and (C) are checked against the ORIGINAL functions, loaded from their
source files unedited (L377's phantom() and L362's Sim via the AST; L370's head exec'd exactly as L373:221-240 does) on a
small periodic box.  (2) All configurations below are axisymmetric, so the continuum operators are solved on a 2-D (R, z)
finite-volume mesh (stretched, far boundary at ~400 Mpc = free space), 10-25 kpc cells where it matters -- resolution the
3-D codes cannot afford.  (3) The 2-D solver is validated on exact solutions (spherical QUMOND, the Kelvin image, the
uniformly polarised ball, L361's own screening transmission) and a no-gate control where the three operators must coincide.
TEST BED.  A cluster region built with L370's RealHalo recipe (carrier NFW + beta-model gas + stars, 30% Hernquist BCG):
real M200 = 1.2e15 Msun, c = 4, M_b(<1 Mpc) = 6.9e13 Msun; BCG scale 50 kpc for the mesh.  Perturbations: (i) a similar
cluster at d = 3, 5 Mpc and 13 Mpc; (ii) a uniform external baryonic field g_e/a0 = 0.001, 0.003, 0.01, 0.03 (read by (B)
only; (A) and (C) are blind to it by construction); (iii) a merger pair (two M200 = 6e14 halves) at 0.5 and 1.0 Mpc, one
connected region vs the counterfactual two-region labelling; (iv) L370's Harvey configuration, toward-main orientation
(axisymmetric), z = 0.4.  Gate cells (p, x_c0) = (1, 2.5) and (2, 2) at z = 0 and 0.4; both a0 footings.

CHECKS (load-bearing unless marked).  K1 kernel = L340's (<= 1e-10).  I1 my (B) = L377's phantom().  I2 my (C) = L370's
phantom_felt().  I3 3-D no-gate identity (B = C with one whole-box region).  S1 spherical QUMOND for every operator.  S2 the
Dirichlet (A) w-field = the Kelvin image solution.  S3 the projection of a uniform field in a ball = 1/3 of it.  S4 L361's
screening transmission (exact l = 1 formula and L361's committed R1 numbers).  S5 no-gate control: A, B, C coincide
(assert).  X-SCREEN a separated similar cluster enters (B) at first order and (A, 1/m <= 0.5 Mpc) only through the screened
gap.  R1 convergence of the retention observables over three meshes.  H1 Harvey: operators agree on beta to <= 0.002.
MUTATE=1 drops the screening (M^2 = 0 in the finite-m operator): S4 and X-SCREEN must FAIL (rc = 1).
SCOPE.  Static fields on prescribed densities (no evolution, no trigger dynamics); axisymmetric configurations (Harvey's
'perp' orientation is not computed); nu_mono only; the relativistic lensing embedding is not derived -- lensing = the
Laplacian of the phantom potential, as L370 does.  No file other than stdout is written.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR5_operator_identity.py
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, json, math, time, ast, io, contextlib, warnings
import numpy as np
import scipy.sparse as sps
import scipy.fft as sfft
from scipy.sparse.linalg import splu
from scipy import ndimage
from scipy.optimize import brentq
from scipy.special import spherical_in, spherical_kn
from scipy.interpolate import RegularGridInterpolator
warnings.filterwarnings("ignore", category=RuntimeWarning)

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH = []


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 118); P(t); P("=" * 118)


P(__doc__.split("CHECKS (load")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the screening is dropped (M^2 = 0 in the finite-m operator): S4 and X-SCREEN must FAIL ***")

# ============================================================================================ constants (L370's cosmology)
G = 4.30091727e-9                                                     # Mpc (km/s)^2 / Msun
MPC_M = 3.0856775814913673e22
A0SI = {"canonical": 9.3619e-11, "alt": 1.1279e-10}                   # both footings always (L370:126, L377:93)
A0 = {k: v * MPC_M / 1e6 for k, v in A0SI.items()}                   # (km/s)^2 / Mpc
FOOTS = ("canonical", "alt")
h = 0.6736; omb, omc = 0.02237, 0.1200
Ob, Oc = omb / h ** 2, omc / h ** 2; Om = Ob + Oc; Orad = 4.18e-5 / h ** 2 * (1 + 0.2271 * 3.046); OL = 1 - Om - Orad
Ez2 = lambda z: Om * (1 + z) ** 3 + OL
RHOC0 = 277.5 * h ** 2 * 1e9                                          # Msun / Mpc^3
rho_crit = lambda z: RHOC0 * Ez2(z)
rho_mbar = lambda z: Om * RHOC0 * (1 + z) ** 3
X_thr = lambda z, p, xc0: xc0 * Ez2(z) ** p                           # L359: x_c,eff = x_c0 E^(2p) (L370:161)
FOURPIG = 4 * math.pi * G
GATES = [(0.0, 1, 2.5), (0.0, 2, 2.0), (0.4, 1, 2.5), (0.4, 2, 2.0)]
gname = lambda gt: f"z={gt[0]:.1f} p={gt[1]} x_c0={gt[2]:g}"
R4 = (0.1, 0.25, 0.5, 1.0)


# ============================================================================================ K  the kernel (L340's nu_mono)
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar(y, e=1e-6):
    return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)
Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0); H_P = float(h_rar(Y_P)); DELTA = 0.05
LYG = np.linspace(-12, 12, 240001); YG = 10 ** LYG
DH_MONO = np.maximum(dh_rar(YG), DELTA * H_P / (YG + Y_P))
H_MONO = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH_MONO[1:] + DH_MONO[:-1]) * np.diff(YG))])
def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-12); return 1.0 + np.interp(np.log10(y), LYG, H_MONO) / y
def nu_rar(y):
    y = np.maximum(np.asarray(y, float), 1e-12); return 1.0 / (-np.expm1(-np.sqrt(y)))


def ast_extract(path, funcs=(), assigns=(), classes=()):
    """compile selected top-level definitions of a source file WITHOUT running the file (no import, no simulation)."""
    src = open(path).read(); tree = ast.parse(src); nodes = []
    for n in tree.body:
        if isinstance(n, ast.FunctionDef) and n.name in funcs:
            nodes.append(n)
        elif isinstance(n, ast.ClassDef) and n.name in classes:
            nodes.append(n)
        elif isinstance(n, ast.Assign):
            tg = []
            for t in n.targets:
                tg += [t.id] if isinstance(t, ast.Name) else [e.id for e in getattr(t, "elts", []) if isinstance(e, ast.Name)]
            if set(tg) & set(assigns):
                nodes.append(n)
    got = [(getattr(n, "name", None) or ast.get_source_segment(src, n).split("=")[0].strip(), n.lineno) for n in nodes]
    return compile(ast.Module(body=nodes, type_ignores=[]), path, "exec"), got


banner("K  THE KERNEL: nu_mono exactly as L340 defines it")
P40 = os.path.join(REPO, "real_research", "g03_audit_2026", "L340_filtered_khronon_completion.py")
code40, got40 = ast_extract(P40, funcs=("h_rar", "dh_rar", "nu_rar", "nu_mono"),
                            assigns=("Y_P", "H_P", "DELTA", "LYG", "YG", "DH_MONO", "H_MONO"))
N40 = {"np": np, "brentq": brentq}; exec(code40, N40)
P(f"    L340 definitions loaded unedited from the source (no execution of the script): {got40}")
yt = np.logspace(-6, 4, 4001)
dK1 = float(np.max(np.abs(nu_mono(yt) / N40["nu_mono"](yt) - 1)))
check("K1 this lane's nu_mono equals L340's (loaded from L340's source) on 4001 points y = 1e-6..1e4", f"max |ratio - 1| = {dK1:.1e}",
      dK1 <= 1e-10)
dev = np.abs(nu_mono(yt) / nu_rar(yt) - 1)
yy = np.linspace(0.5, Y_P, 200001); y_take = float(yy[np.argmax(dh_rar(yy) < DELTA * H_P / (yy + Y_P))])
d_low, d_yp = float(dev[yt <= 2.33].max()), float(dev[yt < Y_P].max())
check("K2 nu_mono = nu_RAR below the phantom peak y_p (as stated): exact to the table's quadrature (<= 1e-8) up to where the "
      "monotone floor takes over, and within 3e-4 up to y_p", f"y_p = {Y_P:.4f}; floor takes over at y = {y_take:.4f}; "
      f"max dev y <= 2.33: {d_low:.1e}; y < y_p: {d_yp:.1e}", d_low <= 1e-8 and d_yp <= 3e-4,
      "the statement 'nu_mono = nu_RAR below y_p' is exact only below y = 2.337; cluster fields here are y ~ 0.01-1")
P77 = os.path.join(REPO, "real_research", "dark_sector_2026", "L377_full_construction_pm.py")
code77, got77 = ast_extract(P77, funcs=("h_rar", "dh_rar", "nu_vec", "phantom"), assigns=("YP", "HP", "LYG", "YG", "DH", "HM", "X_C0"))
N77 = {"np": np, "math": math, "brentq": brentq}; exec(code77, N77)
dK3 = float(np.max(np.abs(N77["nu_vec"](yt) / nu_mono(yt) - 1)))
P(f"    (reported) L377's rebuilt table (log y in -14..14, 280001 points) vs L340's nu_mono: max |ratio - 1| = {dK3:.1e};"
  f" L377 gate cell X_C0, P_GATE = {N77['X_C0']}, {N77['P_GATE']}")

# ============================================================================================ I  3-D identity with the originals
banner("I  IDENTITY: my 3-D re-implementations of (B) and (C) against the ORIGINAL functions (small periodic box)")
P62 = os.path.join(REPO, "real_research", "g03_audit_2026", "L362_forest_pincer_convergence.py")
code62, got62 = ast_extract(P62, classes=("Sim",))
exec(code62, N77)
P(f"    loaded unedited: L377 {got77}; L362 {got62}")
Om77 = 0.3138; OL77 = 1 - Om77; WB77 = Ob / Om
N77.update(Om=Om77, OL=OL77, WB=WB77, Om_a=lambda a: Om77 * a ** -3 / (Om77 * a ** -3 + OL77))
ACC_UNIT = 1e5 * (100e3 * h / 3.0857e22)                              # L377:92


def B3D(L, NG, rb, rho, a, a0c, p, xc0, nu, fd=True, on=True, Om_=Om77, OL_=OL77, WB_=WB77):
    """operator (B) written independently from L377:117-127's description (FD grad/div as L362, or spectral)."""
    d = L / NG; k = np.fft.fftfreq(NG, d=d) * 2 * np.pi
    KX, KY, KZ = np.meshgrid(k, k, k, indexing="ij"); K2 = KX ** 2 + KY ** 2 + KZ ** 2; K2[0, 0, 0] = 1.0
    def pois(s):
        f = -np.fft.fftn(s) / K2; f[0, 0, 0] = 0.0; return np.real(np.fft.ifftn(f))
    if fd:
        grad = lambda f: [(np.roll(f, -1, i) - np.roll(f, 1, i)) / (2 * d) for i in range(3)]
        div = lambda v: sum((np.roll(v[i], -1, i) - np.roll(v[i], 1, i)) / (2 * d) for i in range(3))
    else:
        grad = lambda f: [np.real(np.fft.ifftn(1j * KK * np.fft.fftn(f))) for KK in (KX, KY, KZ)]
        div = lambda v: sum(np.real(np.fft.ifftn(1j * KK * np.fft.fftn(vv))) for KK, vv in zip((KX, KY, KZ), v))
    Om_a_ = Om_ * a ** -3 / (Om_ * a ** -3 + OL_)
    gate = (1.0 / (Om_ * a ** -3 + OL_)) ** p
    f = (1.5 * Om_a_ * (rho - 1.0) * gate > xc0) if on else np.ones_like(rho, bool)
    gb = [-(1.0 / a) * gg for gg in grad(pois(1.5 * Om_ * (rb - WB_) / a))]
    nu1 = nu(np.sqrt(gb[0] ** 2 + gb[1] ** 2 + gb[2] ** 2) / a0c) - 1.0
    dv = div([np.where(f, nu1 * gg, 0.0) for gg in gb])
    return pois(-a * dv), -(2 * a * a / (3 * Om_)) * dv, float(f.mean())


# L377's phantom() on a small box: rho = 1 + two blobs, baryons tracing, a = 1/1.4
NG3, L3 = 32, 24.0
x3 = (np.arange(NG3) + 0.5) * L3 / NG3
X3, Y3, Z3 = np.meshgrid(x3, x3, x3, indexing="ij")
blob = lambda c, s, A: A * np.exp(-((X3 - c[0]) ** 2 + (Y3 - c[1]) ** 2 + (Z3 - c[2]) ** 2) / (2 * s * s))
rho3 = 1.0 + blob((12, 12, 12), 1.2, 400.0) + blob((12, 12, 18.5), 0.9, 150.0) + blob((5, 17, 7), 1.5, 8.0)
rb3 = WB77 * rho3 * (1 + 0.1 * np.cos(2 * np.pi * X3 / L3))
s77 = N77["Sim"](L3, NG3, 8)
a3 = 1 / 1.4; a0c = A0SI["canonical"] / ACC_UNIT
Phi_o, dph_o, fr_o = N77["phantom"](s77, rb3, rho3, a3, a0c)
Phi_m, dph_m, fr_m = B3D(L3, NG3, rb3, rho3, a3, a0c, N77["P_GATE"], N77["X_C0"], N77["nu_vec"])
dI1 = max(float(np.max(np.abs(Phi_o - Phi_m)) / np.max(np.abs(Phi_o))), float(np.max(np.abs(dph_o - dph_m)) / np.max(np.abs(dph_o))))
check("I1 my operator (B) reproduces L377's phantom() (loaded unedited) on a 32^3 box with a switched region: potential and "
      "phantom density", f"max relative deviation {dI1:.1e}; switched fraction {fr_o:.4f} vs {fr_m:.4f}", dI1 <= 1e-10 and fr_o == fr_m,
      "confirms (B) = all-baryon Newtonian field, response masked on the background-subtracted contrast, FD projection")

# L370's head, exactly as L373:221-240 loads it
P70 = os.path.join(REPO, "real_research", "merger_infall_2026", "L370_boosted_infall_mergers.py")
s70 = open(P70).read()
head70 = s70.split("# ============================================================================================================ C1")[0]
head70 = head70.replace('P(__doc__.split("CHECKS")[0].strip())', "pass")
_mut = os.environ.get("MUTATE", "0"); os.environ["MUTATE"] = "0"
N70 = {"__name__": "l370_head", "__file__": P70}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(head70, P70, "exec"), N70)
os.environ["MUTATE"] = _mut
N70["MUTATE"] = False; N70["WK"] = 1
dK4 = float(np.max(np.abs(N70["nu_mono"](yt) / nu_mono(yt) - 1)))
P(f"    L370's head loaded (lines 1-{head70.count(chr(10))}; kernel identical to L340's: max dev {dK4:.1e}); SWITCH = {N70['SWITCH']}, SW_DEF = {N70['SW_DEF']}")


def C3D(N, Lk, rb, rreal, z, a0k, sw, centres, nu):
    """operator (C) written independently from L370:286-307's description (spectral, per labelled region)."""
    dx = Lk / N; k = 2 * np.pi * sfft.fftfreq(N, d=dx); kz = 2 * np.pi * sfft.rfftfreq(N, d=dx)
    kx, ky, kzz = k[:, None, None], k[None, :, None], kz[None, None, :]; k2 = kx ** 2 + ky ** 2 + kzz ** 2; k2[0, 0, 0] = 1.0
    GK = G * 1e3                                                        # kpc (km/s)^2 / Msun
    def field(r):
        pk = -4 * np.pi * GK * sfft.rfftn(r) / k2; pk[0, 0, 0] = 0
        return [sfft.irfftn(-1j * kk * pk, s=r.shape) for kk in (kx, ky, kzz)]
    def proj(F):
        Fk = [sfft.rfftn(f) for f in F]; dt = (kx * Fk[0] + ky * Fk[1] + kzz * Fk[2]) / k2; dt[0, 0, 0] = 0
        return [sfft.irfftn(kk * dt, s=F[0].shape) for kk in (kx, ky, kzz)]
    def dvg(F):
        Fk = [sfft.rfftn(f) for f in F]; return sfft.irfftn(1j * (kx * Fk[0] + ky * Fk[1] + kzz * Fk[2]), s=F[0].shape)
    pz, xz = N70["SWITCH"][sw]
    mask = 1.5 * rreal / (N70["RHOC0"] * N70["Ez2"](z)) >= xz * N70["Ez2"](z) ** pz
    lab, nl = ndimage.label(mask)
    gf = [np.zeros_like(rb) for _ in range(3)]; rp = np.zeros_like(rb)
    for L_ in sorted({int(lab[c]) for c in centres if lab[c] > 0}):
        f = lab == L_
        gw = field(rb * f); mg = np.sqrt(sum(g_ ** 2 for g_ in gw)); fac = f * (nu(mg / a0k) - 1.0)
        gph = proj([fac * g_ for g_ in gw])
        for i in range(3):
            gf[i] += f * gph[i]
        rp += -dvg(gph) / (4 * np.pi * GK)
    return gf, [int(lab[c]) for c in centres], rp, nl


GR70 = N70["Grid"](32, 16000.0)
xk = GR70.x
XK, YK, ZK = np.meshgrid(xk, xk, xk, indexing="ij")
bl = lambda c, s, A: A * np.exp(-((XK - c[0]) ** 2 + (YK - c[1]) ** 2 + (ZK - c[2]) ** 2) / (2 * s * s))
rreal3 = bl((0, 0, 0), 900.0, 3e6) + bl((0, 0, 3000.0), 700.0, 1.5e6) + bl((-5000.0, 4000.0, 0), 600.0, 1.2e6)   # Msun/kpc^3
rb3k = 0.15 * rreal3
cen = [(16, 16, 16), (16, 16, 22), (6, 24, 16)]
out_o = N70["phantom_felt"](GR70, rb3k, rreal3, 0.4, N70["A0K"]["canonical"], "p2_x2.0", cen)
out_m = C3D(32, 16000.0, rb3k, rreal3, 0.4, N70["A0K"]["canonical"], "p2_x2.0", cen, N70["nu_mono"])
sc = max(float(np.max(np.abs(g_))) for g_ in out_o[0])
dI2 = max(max(float(np.max(np.abs(a_ - b_))) for a_, b_ in zip(out_o[0], out_m[0])) / sc,
          float(np.max(np.abs(out_o[2] - out_m[2])) / np.max(np.abs(out_o[2]))))
check("I2 my operator (C) reproduces L370's phantom_felt() (L370's head loaded unedited, as L373 does) on a 32^3 box with "
      "three clusters: felt field, labels and lensing density", f"max relative deviation {dI2:.1e}; labels {out_o[1]} vs "
      f"{out_m[1]}; regions {out_o[3]} vs {out_m[3]}", dI2 <= 1e-10 and out_o[1] == out_m[1] and out_o[3] == out_m[3],
      "confirms (C) = mask on the absolute density, each labelled region's own baryons, spectral projection, felt in-region")
# I3: the 3-D no-gate identity (C with one whole-box region against B's algorithm on the same baryons, L370 units), and the
# two codes' discretisations (L377's central differences against spectral derivatives)
gfC, labC, rpC, nlC = C3D(32, 16000.0, rb3k, np.full_like(rb3k, 1e30), 0.4, N70["A0K"]["canonical"], "p2_x2.0", cen, N70["nu_mono"])
dxk = 16000.0 / 32; kk1 = 2 * np.pi * sfft.fftfreq(32, d=dxk); kz1 = 2 * np.pi * sfft.rfftfreq(32, d=dxk)
kxB, kyB, kzB = kk1[:, None, None], kk1[None, :, None], kz1[None, None, :]; k2B = kxB ** 2 + kyB ** 2 + kzB ** 2; k2B[0, 0, 0] = 1.0
pkB = -4 * np.pi * (G * 1e3) * sfft.rfftn(rb3k) / k2B; pkB[0, 0, 0] = 0
gB = [sfft.irfftn(-1j * kk * pkB, s=rb3k.shape) for kk in (kxB, kyB, kzB)]              # field of ALL baryons (B's source)
facB = N70["nu_mono"](np.sqrt(sum(g_ ** 2 for g_ in gB)) / N70["A0K"]["canonical"]) - 1.0
FkB = [sfft.rfftn(facB * g_) for g_ in gB]; dtB = (kxB * FkB[0] + kyB * FkB[1] + kzB * FkB[2]) / k2B; dtB[0, 0, 0] = 0
gphB = [sfft.irfftn(kk * dtB, s=rb3k.shape) for kk in (kxB, kyB, kzB)]                  # projection, felt everywhere
dI3 = max(float(np.max(np.abs(a_ - b_))) for a_, b_ in zip(gfC, gphB)) / max(float(np.max(np.abs(b_))) for b_ in gphB)
dFDs = {}
for NGx in (32, 64):                                                  # 0.75 and 0.375 Mpc/h cells (L377's mesh: 100/256 = 0.39)
    xx = (np.arange(NGx) + 0.5) * L3 / NGx; XX, YY, ZZ = np.meshgrid(xx, xx, xx, indexing="ij")
    bb = lambda c, s, A: A * np.exp(-((XX - c[0]) ** 2 + (YY - c[1]) ** 2 + (ZZ - c[2]) ** 2) / (2 * s * s))
    rhox = 1.0 + bb((12, 12, 12), 1.2, 400.0) + bb((12, 12, 18.5), 0.9, 150.0) + bb((5, 17, 7), 1.5, 8.0)
    rbx = WB77 * rhox * (1 + 0.1 * np.cos(2 * np.pi * XX / L3))
    Psp = B3D(L3, NGx, rbx, rhox, a3, a0c, 2, 2.0, nu_mono, fd=False, on=False)[0]
    Pfd = B3D(L3, NGx, rbx, rhox, a3, a0c, 2, 2.0, nu_mono, fd=True, on=False)[0]
    dFDs[L3 / NGx] = float(np.max(np.abs(Pfd - Psp)) / np.max(np.abs(Psp)))
dFD = dFDs[L3 / 64]
check("I3 3-D no-gate control: with f = 1 everywhere and no external source, (C) with one whole-box region and (B)'s algorithm "
      "(all baryons, response everywhere, felt everywhere) are the same operator", f"max relative deviation {dI3:.1e}; regions {nlC}",
      dI3 <= 1e-10 and nlC == 1,
      "(reported) the two codes' DISCRETISATIONS differ even where the operators coincide: L377's central-difference grad/div "
      "vs spectral derivatives move the phantom potential of the same cluster pair by " +
      ", ".join(f"{v:.1%} at {k:.3f} Mpc/h cells" for k, v in dFDs.items()) + " (L377's mesh: 0.39 Mpc/h)")


# ============================================================================================ the 2-D axisymmetric finite-volume solver
def axis_edges(anchor, xmin, xmax, zones, growth=1.1):
    """cell edges containing `anchor`; zones = [(lo, hi, h)] target spacings; geometric growth (<= growth per cell) elsewhere."""
    def target(x):
        t = np.inf
        for lo, hi, hh in zones:
            if lo <= x <= hi:
                t = min(t, hh)
        return t
    hmin = min(z_[2] for z_ in zones); out = []
    for sgn, lim in ((1, xmax), (-1, xmin)):
        e = [anchor]; hprev = hmin
        while (e[-1] < lim) if sgn > 0 else (e[-1] > lim):
            x = e[-1]
            hh = min(target(x + sgn * 0.5 * hprev), hprev * growth)
            ta = target(x + sgn * hh)
            if np.isfinite(ta):
                hh = min(hh, ta * growth)
            e.append(x + sgn * hh); hprev = hh
        out.append(np.array(e))
    up, dn = out
    return up if xmin == anchor else np.concatenate([dn[::-1][:-1], up])


class Grid2D:
    """cells (i, j) = annulus [re_i, re_i+1] x slab [ze_j, ze_j+1]; u = 0 ghosts at the far boundary (~400 Mpc: free space)."""
    def __init__(self, re, ze):
        self.re, self.ze = np.asarray(re, float), np.asarray(ze, float)
        self.nr, self.nz = len(re) - 1, len(ze) - 1; self.N = self.nr * self.nz
        self.rc = 0.5 * (self.re[1:] + self.re[:-1]); self.zc = 0.5 * (self.ze[1:] + self.ze[:-1])
        self.dr = np.diff(self.re); self.dz = np.diff(self.ze)
        self.ar = math.pi * (self.re[1:] ** 2 - self.re[:-1] ** 2)
        self.V = self.ar[:, None] * self.dz[None, :]
        self.AR = 2 * math.pi * self.re[1:, None] * self.dz[None, :]
        self.DRc = np.empty(self.nr); self.DRc[:-1] = np.diff(self.rc); self.DRc[-1] = self.re[-1] - self.rc[-1]
        self.AZ = np.repeat(self.ar[:, None], self.nz + 1, axis=1)
        self.DZc = np.empty(self.nz + 1); self.DZc[1:-1] = np.diff(self.zc)
        self.DZc[0] = self.zc[0] - self.ze[0]; self.DZc[-1] = self.ze[-1] - self.zc[-1]
        self.cR = self.AR / self.DRc[:, None]; self.cZ = self.AZ / self.DZc[None, :]
        self.RR, self.ZZ = np.meshgrid(self.rc, self.zc, indexing="ij")
        self.K = self._stiffness(); self._lu = None; self._paint = {}; self._w = {}

    def _stiffness(self):
        nr, nz = self.nr, self.nz; I = np.arange(self.N).reshape(nr, nz); diag = np.zeros((nr, nz)); rows, cols, vals = [], [], []
        c = self.cR[:-1]; diag[:-1] -= c; diag[1:] -= c
        rows += [I[:-1].ravel(), I[1:].ravel()]; cols += [I[1:].ravel(), I[:-1].ravel()]; vals += [c.ravel(), c.ravel()]
        diag[-1] -= self.cR[-1]
        c = self.cZ[:, 1:-1]; diag[:, :-1] -= c; diag[:, 1:] -= c
        rows += [I[:, :-1].ravel(), I[:, 1:].ravel()]; cols += [I[:, 1:].ravel(), I[:, :-1].ravel()]; vals += [c.ravel(), c.ravel()]
        diag[:, 0] -= self.cZ[:, 0]; diag[:, -1] -= self.cZ[:, -1]
        rows.append(I.ravel()); cols.append(I.ravel()); vals.append(diag.ravel())
        return sps.csc_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(self.N, self.N))

    def solve_free(self, rhs):
        if self._lu is None:
            self._lu = splu(self.K.tocsc(), permc_spec="MMD_AT_PLUS_A")
        return self._lu.solve(np.ascontiguousarray(rhs.ravel())).reshape(self.nr, self.nz)

    def lu_dirichlet(self, mask):
        sel = np.flatnonzero(mask.ravel())
        return sel, splu(self.K[sel][:, sel].tocsc(), permc_spec="MMD_AT_PLUS_A")

    def solve_dirichlet(self, fac, rhs):
        sel, lu = fac; u = np.zeros(self.N); u[sel] = lu.solve(np.ascontiguousarray(rhs.ravel()[sel]))
        return u.reshape(self.nr, self.nz)

    def lu_screened(self, M2):
        return splu((self.K - sps.diags(self.V.ravel() * M2.ravel())).tocsc(), permc_spec="MMD_AT_PLUS_A")

    def face_grads(self, u):
        gR = np.empty((self.nr, self.nz)); gR[:-1] = (u[1:] - u[:-1]) / self.DRc[:-1, None]; gR[-1] = -u[-1] / self.DRc[-1]
        gZ = np.empty((self.nr, self.nz + 1)); gZ[:, 1:-1] = (u[:, 1:] - u[:, :-1]) / self.DZc[None, 1:-1]
        gZ[:, 0] = u[:, 0] / self.DZc[0]; gZ[:, -1] = -u[:, -1] / self.DZc[-1]
        return gR, gZ

    def cell_grads(self, gR, gZ):
        inner = np.vstack([np.zeros((1, self.nz)), gR[:-1]])           # the axis face carries zero flux
        return 0.5 * (inner + gR), 0.5 * (gZ[:, :-1] + gZ[:, 1:])

    def grad_cells(self, u):
        return self.cell_grads(*self.face_grads(u))

    def tangential(self, GR, GZ):
        tR = np.empty((self.nr, self.nz)); w = (self.re[1:-1] - self.rc[:-1]) / np.diff(self.rc)
        tR[:-1] = (1 - w)[:, None] * GZ[:-1] + w[:, None] * GZ[1:]; tR[-1] = GZ[-1]
        tZ = np.empty((self.nr, self.nz + 1)); wz = (self.ze[1:-1] - self.zc[:-1]) / np.diff(self.zc)
        tZ[:, 1:-1] = (1 - wz)[None, :] * GR[:, :-1] + wz[None, :] * GR[:, 1:]; tZ[:, 0] = GR[:, 0]; tZ[:, -1] = GR[:, -1]
        return tR, tZ

    def face_masks(self, mask):
        fR = np.zeros((self.nr, self.nz), bool); fR[:-1] = mask[:-1] | mask[1:]
        fZ = np.zeros((self.nr, self.nz + 1), bool); fZ[:, 1:-1] = mask[:, :-1] | mask[:, 1:]
        return fR, fZ

    def flux_sum(self, FR, FZ):
        fl = self.AR * FR; out = fl.copy(); out[1:] -= fl[:-1]; flz = self.AZ * FZ
        return out + flz[:, 1:] - flz[:, :-1]

    def lap(self, u):
        return (self.K @ u.ravel()).reshape(self.nr, self.nz) / self.V


def qumond_flux(g2, u, mask, a0, gext=0.0, nu=nu_mono):
    """face values of F = f (nu(|g|/a0) - 1) g, g = -grad u + gext z^; boundary faces carry the interior flux, so the edge
    layer sits in the first inactive cell (the same place for every operator)."""
    gR, gZ = g2.face_grads(u); GR, GZ = g2.cell_grads(gR, gZ); tR, tZ = g2.tangential(GR, GZ)
    aRR, aZR, aRZ, aZZ = -gR, -tR + gext, -tZ, -gZ + gext
    fR, fZ = g2.face_masks(mask)
    FR = np.where(fR, (nu(np.sqrt(aRR ** 2 + aZR ** 2) / a0) - 1.0) * aRR, 0.0)
    FZ = np.where(fZ, (nu(np.sqrt(aRZ ** 2 + aZZ ** 2) / a0) - 1.0) * aZZ, 0.0)
    return FR, FZ


def op_B(g2, rb_all, mask, a0, gext=0.0, phi=None):
    """(B) L377: field of ALL baryons (+ uniform external), response masked, free-space projection, felt by all baryons."""
    if phi is None:
        phi = g2.solve_free(FOURPIG * rb_all * g2.V)
    fs = g2.flux_sum(*qumond_flux(g2, phi, mask, a0, gext))
    Phi = g2.solve_free(-fs); GR, GZ = g2.grad_cells(Phi)
    return dict(pot=Phi, gR=-GR, gZ=-GZ, rho_ph=-fs / (FOURPIG * g2.V), felt=np.ones_like(mask, bool))


def op_C(g2, rb, regions, a0):
    """(C) L370: per labelled region its own baryons' field, response masked, free-space projection, felt in that region."""
    gR = np.zeros((g2.nr, g2.nz)); gZ = np.zeros_like(gR); rp = np.zeros_like(gR); pot = np.zeros_like(gR); felt = np.zeros_like(gR, bool)
    for m in regions:
        w = g2.solve_free(FOURPIG * rb * m * g2.V)
        fs = g2.flux_sum(*qumond_flux(g2, w, m, a0))
        Phi = g2.solve_free(-fs); GR, GZ = g2.grad_cells(Phi)
        gR += np.where(m, -GR, 0.0); gZ += np.where(m, -GZ, 0.0); pot += np.where(m, Phi, 0.0)
        rp += -fs / (FOURPIG * g2.V); felt |= m
    return dict(pot=pot, gR=gR, gZ=gZ, rho_ph=rp, felt=felt)


def op_AD(g2, rb, mask, a0, fac=None):
    """(A) L361, Dirichlet limit: w = P = 0 outside the active set (at the first inactive cell); felt inside."""
    fac = fac if fac is not None else g2.lu_dirichlet(mask)
    w = g2.solve_dirichlet(fac, FOURPIG * rb * g2.V)
    P_ = g2.solve_dirichlet(fac, -g2.flux_sum(*qumond_flux(g2, w, mask, a0)))
    GR, GZ = g2.grad_cells(P_)
    return dict(pot=P_, gR=np.where(mask, -GR, 0.0), gZ=np.where(mask, -GZ, 0.0), rho_ph=g2.lap(P_) / FOURPIG, felt=mask, w=w)


def op_Am(g2, rb, mask, a0, minv, lu=None):
    """(A) L361 at finite screening length 1/m, as written.  MUTATE drops the screening (M^2 = 0)."""
    M2 = np.zeros((g2.nr, g2.nz)) if MUTATE else np.where(mask, 0.0, 1.0 / minv ** 2)
    lu = lu if lu is not None else g2.lu_screened(M2)
    w = lu.solve(np.ascontiguousarray((FOURPIG * rb * mask * g2.V).ravel())).reshape(g2.nr, g2.nz)
    fs = g2.flux_sum(*qumond_flux(g2, w, mask, a0))
    P_ = lu.solve(np.ascontiguousarray((-fs + g2.V * M2 * w).ravel())).reshape(g2.nr, g2.nz)
    GR, GZ = g2.grad_cells(P_)
    return dict(pot=P_, gR=np.where(mask, -GR, 0.0), gZ=np.where(mask, -GZ, 0.0), rho_ph=g2.lap(P_) / FOURPIG, felt=mask, w=w)


# ---------------------------------------------------------------------------------------------- observables
def sample(g2, F, R, Z):
    it = RegularGridInterpolator((g2.rc, g2.zc), F, bounds_error=False, fill_value=None)
    return it(np.stack([np.maximum(np.asarray(R, float), g2.rc[0]), np.asarray(Z, float)], -1))

GLC, GLCW = np.polynomial.legendre.leggauss(24)
def shell(g2, res, z0, r):
    """shell averages at radius r around (0, z0): radial phantom force (monopole), z-force (the net push), potential."""
    st = np.sqrt(1 - GLC ** 2); R, Z = r * st, z0 + r * GLC
    gR, gZ = sample(g2, res["gR"], R, Z), sample(g2, res["gZ"], R, Z)
    return 0.5 * np.sum(GLCW * (gR * st + gZ * GLC)), 0.5 * np.sum(GLCW * gZ), 0.5 * np.sum(GLCW * sample(g2, res["pot"], R, Z))

def point_gr(g2, res, z0, r, th):
    R, Z = r * math.sin(th), z0 + r * math.cos(th)
    return float(sample(g2, res["gR"], [R], [Z])[0]) * math.sin(th) + float(sample(g2, res["gZ"], [R], [Z])[0]) * math.cos(th)

def perp_weights(g2, z0, Rap, ngl=8):
    """cell volume inside the cylinder y^2 + (z - z0)^2 < Rap^2 (line of sight along x, perpendicular to the axis)."""
    key = (round(z0, 6), Rap)
    if key in g2._w:
        return g2._w[key]
    W = np.zeros((g2.nr, g2.nz)); x, wx = np.polynomial.legendre.leggauss(ngl)
    def S(rho, Y):
        Yc = np.minimum(Y, rho); safe = np.where(rho > 0, rho, 1.0)
        return np.where(rho > 0, 2 * (Yc * np.sqrt(np.maximum(rho ** 2 - Yc ** 2, 0)) + rho ** 2 * np.arcsin(np.clip(Yc / safe, 0, 1))), 0.0)
    for j in range(g2.nz):
        lo, hi = max(g2.ze[j], z0 - Rap), min(g2.ze[j + 1], z0 + Rap)
        if hi <= lo:
            continue
        t = 0.5 * (hi + lo) + 0.5 * (hi - lo) * x; wt = 0.5 * (hi - lo) * wx
        Y = np.sqrt(np.maximum(Rap ** 2 - (t - z0) ** 2, 0.0))
        W[:, j] = ((S(g2.re[1:, None], Y[None, :]) - S(g2.re[:-1, None], Y[None, :])) * wt[None, :]).sum(1)
    g2._w[key] = W
    return W


# ---------------------------------------------------------------------------------------------- the cluster (L370's RealHalo recipe)
RG1 = np.geomspace(1e-4, 60.0, 12000)
def cum_mass(rho):
    integ = 4 * math.pi * RG1 ** 2 * rho; seg = 0.5 * (integ[1:] + integ[:-1]) * np.diff(RG1)
    return np.concatenate([[integ[0] * RG1[0] / 3.0], integ[0] * RG1[0] / 3.0 + np.cumsum(seg)])
def c_dm14(Mh, z):                                                    # L370:130-132
    a = 0.520 + (0.905 - 0.520) * math.exp(-0.617 * z ** 1.21); b = -0.101 + 0.026 * z
    return 10 ** (a + b * np.log10(Mh / 1e12))

class Halo:
    """L370:190-217 (intact carrier): carrier NFW + beta-model gas + stars (30% Hernquist BCG, 70% NFW-traced), BMO n = 2
    taper at 2.5 R200, normalised within R200(z_def)."""
    def __init__(self, M200, z_def, fgas, fstar, c=None, a_bcg=0.05):
        self.M200 = M200; self.R200 = (3 * M200 / (4 * math.pi * 200 * rho_crit(z_def))) ** (1 / 3)
        self.c = float(c if c is not None else c_dm14(M200 * h, z_def))
        rs, rt = self.R200 / self.c, 2.5 * self.R200; T = (rt ** 2 / (RG1 ** 2 + rt ** 2)) ** 2
        nfw = T / ((RG1 / rs) * (1 + RG1 / rs) ** 2); gas = T / (1 + (RG1 / (0.12 * self.R200)) ** 2)
        bcg = T / ((RG1 / a_bcg) * (1 + RG1 / a_bcg) ** 3)
        m_in = lambda prof: float(np.interp(self.R200, RG1, cum_mass(prof)))
        self.rho_c = (1 - fgas - fstar) * M200 * nfw / m_in(nfw); self.rho_g = fgas * M200 * gas / m_in(gas)
        self.rho_s = fstar * M200 * (0.3 * bcg / m_in(bcg) + 0.7 * nfw / m_in(nfw))
        self.rho_b = self.rho_g + self.rho_s; self.rho = self.rho_b + self.rho_c
        self.Mb, self.Mr = cum_mass(self.rho_b), cum_mass(self.rho)

GLX, GLW = np.polynomial.legendre.leggauss(4)
def paint(g2, prof, zc0=0.0, key=None):
    """cell average of a spherical profile centred on the axis at z = zc0 (4 x 4 Gauss points per cell, R-weighted)."""
    if key is not None and (key, zc0) in g2._paint:
        return g2._paint[(key, zc0)]
    lr, lp = np.log(RG1), np.log(np.maximum(prof, 1e-300)); out = np.zeros((g2.nr, g2.nz))
    for a, wa in zip(GLX, GLW):
        R = g2.rc[:, None] + 0.5 * a * g2.dr[:, None]
        for c, wc in zip(GLX, GLW):
            r = np.sqrt(R ** 2 + (g2.zc[None, :] + 0.5 * c * g2.dz[None, :] - zc0) ** 2)
            out += 0.25 * wa * wc * np.where(r > RG1[-1], 0.0, np.exp(np.interp(np.log(np.maximum(r, RG1[0])), lr, lp))) * (R / g2.rc[:, None])
    if key is not None:
        g2._paint[(key, zc0)] = out
    return out

def regions(g2, dens, X, centres, absolute=False, z=0.0):
    """connected active regions containing the given centres; contrast gate (A, B) or L370's absolute-density gate (C_abs)."""
    m = 1.5 * (dens + (rho_mbar(z) if absolute else 0.0)) / rho_crit(z) >= X
    lab, n = ndimage.label(m)
    ls = {int(lab[0, np.argmin(np.abs(g2.zc - zc))]) for zc in centres} - {0}
    regs = [lab == L_ for L_ in ls]
    return sorted(regs, key=lambda r_: float(g2.ZZ[r_].mean()))          # ordered along z (the main cluster first)


def make_grid(hf, hm, fine_R=1.2, fine_z=(-1.2, 1.2), mid_R=7.0, mid_z=(-7.5, 19.5), far=400.0, growth=1.1):
    re = axis_edges(0.0, 0.0, far, [(0.0, fine_R, hf), (0.0, mid_R, hm)], growth)
    ze = axis_edges(0.0, -far, far, [(fine_z[0], fine_z[1], hf), (mid_z[0], mid_z[1], hm)], growth)
    return Grid2D(re, ze)

HC = Halo(1.2e15, 0.0, 0.125, 0.015, c=4.0)                           # the test cluster
HH = Halo(6.0e14, 0.0, 0.125, 0.015, c=4.5)                           # the merger halves
Mb1 = lambda r: float(np.interp(r, RG1, HC.Mb))
P(f"\n  test cluster: real M200 {HC.M200:.2e} Msun, R200 {HC.R200:.2f} Mpc, c {HC.c}; M_b(<1 Mpc) {Mb1(1.0):.2e}, M_b(<R200) "
  f"{Mb1(HC.R200):.2e}; g_N,b/a0 (canonical) at 0.1/0.25/0.5/1 Mpc = " +
  "/".join(f"{G * Mb1(r) / r ** 2 / A0['canonical']:.3f}" for r in R4))

# ============================================================================================ S  2-D solver validation
banner("S  THE 2-D SOLVER AGAINST EXACT SOLUTIONS, AND THE NO-GATE CONTROL")
GP = make_grid(0.025, 0.1)
P(f"    production mesh: {GP.nr} x {GP.nz} = {GP.N} cells; 25 kpc for R, |z| < 1.2 Mpc; 100 kpc out to R = 7, z = -7.5..19.5 "
  f"Mpc; geometric to {GP.re[-1]:.0f} Mpc")
rb_iso = paint(GP, HC.rho_b, 0.0, "Cb"); rr_iso = paint(GP, HC.rho, 0.0, "Cr")
gt0 = (0.4, 2, 2.0); X0 = X_thr(*gt0)
m_iso = regions(GP, rr_iso, X0, [0.0], z=0.4)[0]
a0c_ = A0["canonical"]
S1ops = {"A_D": op_AD(GP, rb_iso, m_iso, a0c_), "A_1/m=0.2": op_Am(GP, rb_iso, m_iso, a0c_, 0.2),
         "A_1/m=0.5": op_Am(GP, rb_iso, m_iso, a0c_, 0.5), "B": op_B(GP, rb_iso, m_iso, a0c_), "C": op_C(GP, rb_iso, [m_iso], a0c_)}
worst = {}
for r in (0.1, 0.25, 0.5, 1.0, 2.0):
    gN = G * Mb1(r) / r ** 2; ex = -(nu_mono(gN / a0c_) - 1) * gN
    for k_, v_ in S1ops.items():
        worst[(k_, r)] = abs(shell(GP, v_, 0.0, r)[0] / ex - 1)
P("    shell-averaged phantom force / exact QUMOND (nu - 1) g_N:  " + "; ".join(
    f"r={r}: " + ", ".join(f"{k_} {1 - worst[(k_, r)]:.4f}" for k_ in ("A_D", "B", "C")) for r in (0.1, 0.25, 0.5, 1.0, 2.0)))
s1 = max(worst[(k_, r)] for k_ in S1ops for r in (0.25, 0.5, 1.0, 2.0)); s1c = max(worst[(k_, 0.1)] for k_ in S1ops)
check("S1 an isolated spherical cluster (gate z = 0.4, p = 2): every operator (A Dirichlet, A at 1/m = 0.2 and 0.5, B, C) "
      "returns the exact spherical QUMOND phantom (nu - 1) g_N within 0.5% at 0.25-2 Mpc and 2% at 0.1 Mpc (4 cells)",
      f"max deviation {s1:.1e} (0.25-2 Mpc), {s1c:.1e} (0.1 Mpc)", s1 <= 5e-3 and s1c <= 2e-2,
      "in spherical symmetry the three operators are the same continuum object; this fixes the mesh's absolute accuracy")

# S2: Kelvin image for the Dirichlet w
mS = (GP.RR ** 2 + GP.ZZ ** 2) < 1.0 ** 2
Reff = 1.0 + 0.5 * 0.025
aS, mSm, bS = 0.5, 1e13, 0.02
rbS = paint(GP, 3 * mSm / (4 * math.pi * bS ** 3) * (1 + (RG1 / bS) ** 2) ** -2.5, aS)
wD = GP.solve_dirichlet(GP.lu_dirichlet(mS), FOURPIG * rbS * GP.V)
GRD, GZD = GP.grad_cells(wD)
errs, img_frac = [], []
ast_ = Reff ** 2 / aS
def gexact(R_, Z_, img=True):
    """Plummer direct field + the Kelvin image of its (point) mass for the grounded sphere of radius Reff."""
    d1 = math.hypot(R_, Z_ - aS); d2 = math.hypot(R_, Z_ - ast_); s1 = (d1 * d1 + bS * bS) ** 1.5
    gR_ = -G * mSm * R_ / s1 + (G * mSm * (Reff / aS) * R_ / d2 ** 3 if img else 0)
    gZ_ = -G * mSm * (Z_ - aS) / s1 + (G * mSm * (Reff / aS) * (Z_ - ast_) / d2 ** 3 if img else 0)
    return np.array([gR_, gZ_])
for (R_, Z_) in ((0.0, -0.4), (0.4, 0.0), (0.3, -0.3), (0.0, 0.1)):
    Re_ = max(R_, GP.rc[0])                                           # on the axis the mesh value sits at the first cell centre
    num = -np.array([float(sample(GP, GRD, [Re_], [Z_])[0]), float(sample(GP, GZD, [Re_], [Z_])[0])])
    ex_ = gexact(Re_, Z_); errs.append(np.linalg.norm(num - ex_) / np.linalg.norm(ex_))
    img_frac.append(np.linalg.norm(ex_ - gexact(Re_, Z_, False)) / np.linalg.norm(ex_))
check("S2 the Dirichlet-limit w of operator (A) equals the exact image solution for an off-centre mass in a spherical region "
      "(Kelvin image q' = -q R/a at R^2/a) within 2% at four interior points", f"errors {[f'{e:.1e}' for e in errs]}; the image "
      f"term is {min(img_frac):.0%}-{max(img_frac):.0%} of the field there", max(errs) <= 0.02,
      "the Dirichlet w differs from the free-space field of the region's baryons by exactly these images")

# S3: uniformly polarised ball
mB = (GP.RR ** 2 + GP.ZZ ** 2) < 1.0 ** 2
fR_, fZ_ = GP.face_masks(mB); F0 = 1.0
PhB = GP.solve_free(-GP.flux_sum(np.zeros((GP.nr, GP.nz)), np.where(fZ_, F0, 0.0)))
_, GZB = GP.grad_cells(PhB)
vals3 = [-float(sample(GP, GZB, [R_], [Z_])[0]) for (R_, Z_) in ((0.0, 0.0), (0.3, 0.2), (0.0, -0.5), (0.5, 0.0))]
e3 = max(abs(v / (F0 / 3) - 1) for v in vals3)
check("S3 the curl-free projection used by (B) and (C) returns 1/3 of a uniform field confined to a ball (the demagnetising "
      "factor of a sphere) within 2%", f"g_ph/F0 = {[round(v, 4) for v in vals3]}", e3 <= 0.02,
      "a boosted EXTERNAL field inside a region enters (B) through exactly this projection")

# S4: L361's screening transmission (the l = 1 w-field through an inactive gap)
P61 = os.path.join(REPO, "real_research", "g03_audit_2026", "L361_bound_region_kernel.py")
code61, got61 = ast_extract(P61, funcs=("transmission",))
N61 = {"np": np, "MUTATE": False, "spherical_in": spherical_in, "spherical_kn": spherical_kn}; exec(code61, N61)
J61 = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L361_bound_region_kernel_results.json")))["numbers"]
GT = make_grid(0.025, 0.1, fine_R=3.6, fine_z=(-3.6, 3.6), mid_R=5.0, mid_z=(-5.0, 5.0), far=200.0)
rT = np.sqrt(GT.RR ** 2 + GT.ZZ ** 2)
gapT = (rT >= 1.0) & (rT < 3.0)
def ghost_rhs(g2, fn):
    """RHS for ghost values u = fn(R, z) on the far boundary."""
    b = np.zeros((g2.nr, g2.nz))
    b[-1, :] -= g2.cR[-1, :] * fn(g2.re[-1], g2.zc)
    b[:, 0] -= g2.cZ[:, 0] * fn(g2.rc, g2.ze[0]); b[:, -1] -= g2.cZ[:, -1] * fn(g2.rc, g2.ze[-1])
    return b
TT = {}
for mi in (0.2, 0.3, 0.5):
    M2T = np.zeros((GT.nr, GT.nz)) if MUTATE else np.where(gapT, 1.0 / mi ** 2, 0.0)
    wT = GT.lu_screened(M2T).solve(ghost_rhs(GT, lambda R_, Z_: Z_ + 0 * R_).ravel()).reshape(GT.nr, GT.nz)
    _, GZT = GT.grad_cells(wT)
    TT[mi] = float(np.mean([sample(GT, GZT, [R_], [Z_])[0] for (R_, Z_) in ((0.0, 0.0), (0.3, 0.2), (0.2, -0.3))]))
ex61 = {mi: N61["transmission"](mi, 1.0, 3.0) for mi in TT}
js61 = {mi: J61["R1"]["transmission"][f"{mi:g}"] for mi in TT}
e4 = max(abs(TT[mi] / ex61[mi] - 1) for mi in TT)
check("S4 SCREENING: the finite-m operator transmits into a region (R_e = 1 Mpc) the fraction of an external uniform w-field "
      "that L361's exact l = 1 solution gives through a 2 Mpc inactive gap (its function loaded unedited; its committed R1 "
      "numbers) within 5%", "; ".join(f"1/m = {mi}: mesh {TT[mi]:.3e}, L361 exact {ex61[mi]:.3e}, L361 JSON {js61[mi]:.3e}"
                                     for mi in TT), e4 <= 0.05,
      "the gap screens as exp[-m (R_2 - R_e)]; with the screening dropped (MUTATE) the full field enters")

# S5: no-gate control
mall = np.ones((GP.nr, GP.nz), bool)
nog = {"A_D path": op_AD(GP, rb_iso, mall, a0c_), "A_m path": op_Am(GP, rb_iso, mall, a0c_, 0.2),
       "B": op_B(GP, rb_iso, mall, a0c_), "C": op_C(GP, rb_iso, [mall], a0c_)}
ref_ = nog["B"]; d5 = 0.0
for k_, v_ in nog.items():
    for fld in ("pot", "gR", "gZ", "rho_ph"):
        d5 = max(d5, float(np.max(np.abs(v_[fld] - ref_[fld])) / np.max(np.abs(ref_[fld]))))
assert d5 <= 1e-9, f"no-gate control failed: {d5}"
check("S5 NO-GATE CONTROL (asserted): one region, f = 1 everywhere, no external source -- operators A (Dirichlet and finite-m "
      "code paths), B and C coincide in potential, force and lensing density", f"max relative deviation {d5:.1e}", d5 <= 1e-9,
      "every difference reported below comes from the gate: the source restriction, the boundary condition, who feels it")

# ============================================================================================ E  the region edge
banner("E  THE REGION EDGE: L377/L361's contrast gate against L370's absolute-density gate (same density field)")
EDGE = {}
for gt in GATES:
    z_, p_, x_ = gt; X_ = X_thr(*gt)
    sub = 1.5 * HC.rho / rho_crit(z_) - X_; ab = 1.5 * (HC.rho + rho_mbar(z_)) / rho_crit(z_) - X_
    Rs = float(RG1[np.argmax((sub < 0) & (RG1 > 0.01))]); Ra = float(RG1[np.argmax((ab < 0) & (RG1 > 0.01))])
    EDGE[gt] = (Rs, Ra)
    P(f"    {gname(gt)}: threshold x_c,eff = {X_:.3f} -> contrast delta_th = {X_ / (1.5 * Om * (1 + z_) ** 3 / Ez2(z_)):.2f}; "
      f"edge {Rs:.3f} Mpc (contrast) vs {Ra:.3f} Mpc (absolute): +{Ra / Rs - 1:.1%}; g_N,b/a0 at the edge "
      f"{G * Mb1(Rs) / Rs ** 2 / A0['canonical']:.4f}")
P("    On L370's painted halos (no cosmic mean in the density) the absolute formula at L370:290 coincides with the contrast gate "
  "if the painted profile is read as an overdensity; read as the total density (or fed a PM field with the mean) it moves "
  "the edge outward by the amounts above.")
Jl = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L361_bound_region_kernel_results.json")))["numbers"]["R3"]
ge_lin = Jl["baryons only (L353/L355)"]["kernel_field_rms_a0"]
ge_nb = G * 1e14 / 5.0 ** 2 / A0["canonical"]
P(f"    REALISTIC EXTERNAL BARYONIC FIELD: linear-theory baryons-only rms at lenses (L355 via L361 R3's committed JSON) "
  f"{ge_lin['canonical']:.4f} a0 canonical / {ge_lin['alt']:.4f} alt; a 1e14 Msun baryonic neighbour at 5 Mpc gives "
  f"{ge_nb:.4f} a0  =>  realistic g_e ~ 0.001-0.006 a0; 0.01 = a close massive neighbour; 0.03 exceeds the all-matter rms "
  f"({Jl['total field (BS2' + chr(39) + 's construction)']['kernel_field_rms_a0']['canonical']:.3f} a0).")

# ============================================================================================ X  the operator comparison
banner("X  THE OPERATOR COMPARISON (production mesh): every operator against the action's Dirichlet limit A_D")
CONFS = {"iso": [(HC, "C", 0.0)], "nb3": [(HC, "C", 0.0), (HC, "C", 3.0)], "nb5": [(HC, "C", 0.0), (HC, "C", 5.0)],
         "nb13": [(HC, "C", 0.0), (HC, "C", 13.0)], "pair0.5": [(HH, "H", -0.25), (HH, "H", 0.25)],
         "pair1.0": [(HH, "H", -0.5), (HH, "H", 0.5)]}
GEXT = (0.001, 0.003, 0.01, 0.03)


def observe(g2, res, rr, z0, rd, rb_main=None, zs=None):
    """probes around the main cluster (z0): shell-averaged radial phantom force and z-force at r = 0.1-1 Mpc, the radial force
    at theta = 0, 90, 180 deg, the projected (perpendicular) lensing mass in R = 0.1-1 Mpc; and, on a shell of radius rd
    centred at zs (inside the region), the phantom well depth and the enclosed phantom mass (Gauss)."""
    o = {}; zs = z0 if zs is None else zs
    for r in R4:
        mono, dip, _ = shell(g2, res, z0, r)
        o[("F", r)] = mono; o[("D", r)] = dip
        o[("Fpt", r)] = [point_gr(g2, res, z0, r, th) for th in (0.0, 0.5 * math.pi, math.pi)]
        W = perp_weights(g2, z0, r)
        o[("Lph", r)] = float((res["rho_ph"] * W).sum()); o[("Lre", r)] = float((rr * W).sum())
    mono_d, _, pot_d = shell(g2, res, zs, rd)
    o["depth"] = pot_d - float(sample(g2, res["pot"], [0.0], [zs])[0])
    o["Mph_in"] = -rd ** 2 * mono_d / G
    o["Mph_tot"] = float((res["rho_ph"] * g2.V).sum())
    if rb_main is not None:
        sel = (g2.RR ** 2 + (g2.ZZ - z0) ** 2) < 0.5 ** 2
        o["push"] = float((rb_main * g2.V * res["gZ"])[sel].sum() / (rb_main * g2.V)[sel].sum())
    return o


def diffs(o, oref):
    """fractional differences vs the reference: monopole force, worst-direction radial force and net push (both relative to
    the reference's shell-averaged phantom force at that radius), lensing mass (relative to the total lensing mass)."""
    d = {}
    for r in R4:
        d[("F", r)] = o[("F", r)] / oref[("F", r)] - 1
        d[("Fpt", r)] = max(abs(a_ - b_) for a_, b_ in zip(o[("Fpt", r)], oref[("Fpt", r)])) / abs(oref[("F", r)])
        d[("D", r)] = (o[("D", r)] - oref[("D", r)]) / abs(oref[("F", r)])
        d[("L", r)] = (o[("Lph", r)] - oref[("Lph", r)]) / (oref[("Lre", r)] + oref[("Lph", r)])
    d["depth"] = o["depth"] / oref["depth"] - 1
    d["Mph_in"] = o["Mph_in"] / oref["Mph_in"] - 1
    return d


def fmt(d, keys=("F", "Fpt", "D", "L")):
    return " | ".join(f"{k_} " + "/".join(f"{d[(k_, r)]:+.1e}" for r in R4) for k_ in keys) + f" | depth {d['depth']:+.1e}"


def run_matrix(g2, confs, gates, foots, verbose=True, want_ext=True):
    TAB = {}
    for cname, cs in confs.items():
        rb_c = [paint(g2, hh.rho_b, zc, key + "b") for hh, key, zc in cs]; rr_c = [paint(g2, hh.rho, zc, key + "r") for hh, key, zc in cs]
        rb, rr = sum(rb_c), sum(rr_c); z0 = cs[0][2]
        phi = g2.solve_free(FOURPIG * rb * g2.V)
        phi_all = g2.solve_free(FOURPIG * rr * g2.V)                  # the carrier's potential (Newtonian, all real matter)
        for gt in gates:
            z_, p_, x_ = gt; X_ = X_thr(*gt)
            regs = regions(g2, rr, X_, [c[2] for c in cs], z=z_); regsA = regions(g2, rr, X_, [c[2] for c in cs], absolute=True, z=z_)
            mask = np.any(regs, axis=0); maskA = np.any(regsA, axis=0)
            if cname.startswith("pair"):                              # depth / Gauss shell centred on the pair, inside its region
                zs, rd = 0.0, 0.9 * float(min(g2.RR[mask].max(), -g2.ZZ[mask].min(), g2.ZZ[mask].max()))
            else:
                zs, rd = z0, 0.9 * EDGE[gt][0]
            carrier_depth = shell(g2, dict(gR=phi_all, gZ=phi_all, pot=phi_all), zs, rd)[2] - float(sample(g2, phi_all, [0.0], [zs])[0])
            facD = g2.lu_dirichlet(mask)
            M2s = {mi: (np.zeros((g2.nr, g2.nz)) if MUTATE else np.where(mask, 0.0, 1.0 / mi ** 2)) for mi in (0.2, 0.5)}
            lus = {mi: g2.lu_screened(M2s[mi]) for mi in (0.2, 0.5)}
            info = dict(n_regions=len(regs), n_regions_abs=len(regsA), z_extent=(float(g2.ZZ[mask].min()), float(g2.ZZ[mask].max())),
                        R_extent=float(g2.RR[mask].max()), R_extent_abs=float(g2.RR[maskA].max()),
                        Mb_region=float((rb * mask * g2.V).sum()), Mb_all=float((rb * g2.V).sum()), carrier_depth=carrier_depth,
                        rd=rd, zs=zs, Mb_rd=float((rb * g2.V)[(g2.RR ** 2 + (g2.ZZ - zs) ** 2) < rd ** 2].sum()))
            if len(regs) > 1:
                gap = float(g2.ZZ[regs[1]].min() - g2.ZZ[regs[0]].max())
                info["gap"] = gap
            for foot in foots:
                a0_ = A0[foot]
                R = {"A_D": op_AD(g2, rb, mask, a0_, facD), "A_0.2": op_Am(g2, rb, mask, a0_, 0.2, lus[0.2]),
                     "A_0.5": op_Am(g2, rb, mask, a0_, 0.5, lus[0.5]), "B": op_B(g2, rb, mask, a0_, 0.0, phi),
                     "C": op_C(g2, rb, regs, a0_), "C_abs": op_C(g2, rb, regsA, a0_)}
                if cname.startswith("pair"):
                    R["C_two"] = op_C(g2, rb, [mask & (g2.ZZ < 0), mask & (g2.ZZ >= 0)], a0_)
                O = {k_: observe(g2, v_, rr, z0, rd, rb_c[0], zs) for k_, v_ in R.items()}
                if cname.startswith("pair"):                          # the phantom part of the pair force on cluster 2's baryons
                    for k_, v_ in R.items():
                        O[k_]["F2"] = float((rb_c[1] * g2.V * v_["gZ"]).sum() / (rb_c[1] * g2.V).sum())
                ext = {}
                if want_ext and cname == "iso":
                    for ge in GEXT:
                        rBe = op_B(g2, rb, mask, a0_, ge * a0_, phi)
                        oe = observe(g2, rBe, rr, z0, rd, rb_c[0], zs)
                        rx = 1.25 * EDGE[gt][0]                        # B's phantom felt by out-of-region baryons (A, C: zero)
                        oe["ext_field"] = max(math.hypot(float(sample(g2, rBe["gR"], [rx * math.sin(t_)], [rx * math.cos(t_)])[0]),
                                                         float(sample(g2, rBe["gZ"], [rx * math.sin(t_)], [rx * math.cos(t_)])[0]))
                                              for t_ in (0.0, 0.25 * math.pi, 0.5 * math.pi))
                        ext[ge] = oe
                TAB[(cname, gt, foot)] = dict(O=O, ext=ext, info=info)
                if verbose and foot == "canonical":
                    P(f"  {cname:8s} {gname(gt)} [{foot}]: {info['n_regions']} region(s) contrast / {info['n_regions_abs']} absolute; "
                      f"z-extent {info['z_extent'][0]:.2f}..{info['z_extent'][1]:.2f} Mpc, R-extent {info['R_extent']:.2f} "
                      f"(absolute {info['R_extent_abs']:.2f}){'; gap ' + format(info['gap'], '.2f') + ' Mpc' if 'gap' in info else ''}; "
                      f"kernel source M_b: region {info['Mb_region']:.2e}, all baryons {info['Mb_all']:.2e}")
                    for k_ in [k for k in R if k != "A_D"]:
                        P(f"      {k_:6s} - A_D: {fmt(diffs(O[k_], O['A_D']))}")
                    if ext:
                        for ge, oe in ext.items():
                            dd = diffs(oe, O["B"])
                            P(f"      B(g_e={ge:<5g}) - B(0): {fmt(dd)} | push {oe['push'] / (ge * a0_):+.2f} g_e | phantom "
                              f"felt outside the region at 1.25 R_e: {oe['ext_field'] / (ge * a0_):.2f} g_e")
            del facD, lus
    return TAB


TX = run_matrix(GP, CONFS, GATES, FOOTS)
P(f"  [{time.time() - T0:.0f}s]")

# ---------------------------------------------------------------------------------------------- summaries
def mx(d, k_):
    return max(abs(d[(k_, r)]) for r in R4)

banner("X  SUMMARY: max |fractional difference| vs A_D over both footings and all four gate cells")
P("    columns: 'mono' = shell-averaged radial phantom force at r = 0.1-1 Mpc (the retention core; = enclosed phantom mass);"
  " 'depth' = phantom well depth centre -> 0.9 R_e; 'M_ph(0.9Re)' = phantom mass enclosed at 0.9 R_e (outskirts); 'worst-dir'"
  " = max over theta = 0/90/180 deg of the radial-force change / the shell-averaged force; 'push' = shell-averaged z-force"
  " change (the net push along the axis) / the shell-averaged force; 'lensing' = projected (perpendicular) lensing mass"
  " change / the total lensing mass, R = 0.1-1 Mpc")
rows = []
for cname in CONFS:
    for op in ("A_0.2", "A_0.5", "B", "C", "C_abs"):
        vals = [diffs(TX[(cname, gt, f)]["O"][op], TX[(cname, gt, f)]["O"]["A_D"]) for gt in GATES for f in FOOTS]
        rows.append((cname, op, max(mx(d, "F") for d in vals), max(abs(d["depth"]) for d in vals), max(abs(d["Mph_in"]) for d in vals),
                     max(mx(d, "Fpt") for d in vals), max(mx(d, "D") for d in vals), max(mx(d, "L") for d in vals)))
P(f"    {'config':8s} {'operator':7s} {'mono':>9s} {'depth':>9s} {'M_ph(0.9Re)':>12s} {'worst-dir':>10s} {'push':>9s} {'lensing':>9s}")
for r_ in rows:
    P(f"    {r_[0]:8s} {r_[1]:7s} {r_[2]:9.1e} {r_[3]:9.1e} {r_[4]:12.1e} {r_[5]:10.1e} {r_[6]:9.1e} {r_[7]:9.1e}")
EXT = {}
for ge in GEXT:
    vals = [diffs(TX[("iso", gt, f)]["ext"][ge], TX[("iso", gt, f)]["O"]["B"]) for gt in GATES for f in FOOTS]
    push = [TX[("iso", gt, f)]["ext"][ge]["push"] / (ge * A0[f]) for gt in GATES for f in FOOTS]
    exf = [TX[("iso", gt, f)]["ext"][ge]["ext_field"] / (ge * A0[f]) for gt in GATES for f in FOOTS]
    EXT[ge] = (max(mx(d, "F") for d in vals), max(abs(d["depth"]) for d in vals), max(abs(d["Mph_in"]) for d in vals),
               max(mx(d, "Fpt") for d in vals), max(mx(d, "L") for d in vals), min(push), max(push), min(exf), max(exf))
    P(f"    iso+g_e={ge:<5g} B(g_e) - B(0) [A and C do not see g_e]: mono {EXT[ge][0]:.1e}  depth {EXT[ge][1]:.1e}  M_ph(0.9Re) "
      f"{EXT[ge][2]:.1e}  worst-dir {EXT[ge][3]:.1e}  lensing {EXT[ge][4]:.1e}; net phantom push on the baryons (<0.5 Mpc) "
      f"{EXT[ge][5]:.2f}-{EXT[ge][6]:.2f} g_e; phantom felt by out-of-region baryons at 1.25 R_e {EXT[ge][7]:.2f}-{EXT[ge][8]:.2f} g_e")
# B's net push separates baryons from the carrier (which feels only phi): L370's equilibrium-offset estimate dx = a / (4/3 pi G rho50)
r50 = 0.05; gN50 = G * Mb1(r50) / r50 ** 2
rho50 = (float(np.interp(r50, RG1, HC.Mr)) + (nu_mono(gN50 / A0["canonical"]) - 1) * Mb1(r50)) / (4 / 3 * math.pi * r50 ** 3)
DX_EQ = {ge: EXT[ge][6] * ge * A0["canonical"] / (4 / 3 * math.pi * G * rho50) * 1e3 for ge in (0.003, 0.01)}
P(f"    B's push displaces the main cluster's baryons from its carrier by ~{DX_EQ[0.003]:.1f} kpc at g_e = 0.003 ({DX_EQ[0.01]:.1f} kpc at "
  f"0.01; L370's estimator dx = a/(4/3 pi G rho50), rho50 = {rho50:.2e} Msun/Mpc^3 real + phantom); A and C: 0")
# the discretisation floor: isolated sphere, where A_D = B = C exactly in the continuum
fl = [diffs(TX[("iso", gt, f)]["O"][op], TX[("iso", gt, f)]["O"]["A_D"]) for gt in GATES for f in FOOTS for op in ("B", "C")]
FLOOR = dict(F=max(mx(d, "F") for d in fl), L=max(mx(d, "L") for d in fl), depth=max(abs(d["depth"]) for d in fl),
             M=max(abs(d["Mph_in"]) for d in fl))
P(f"    NUMERICAL FLOOR (isolated sphere, where A_D = B = C exactly in the continuum): mono {FLOOR['F']:.1e}, depth "
  f"{FLOOR['depth']:.1e}, M_ph(0.9Re) {FLOOR['M']:.1e}, lensing {FLOOR['L']:.1e} (the staircase edge layer in the line of sight)")
gauss = max(abs(TX[k_]["O"][op]["Mph_tot"]) / TX[k_]["info"]["Mb_all"] for k_ in TX for op in TX[k_]["O"])
P(f"    GAUSS: net phantom mass over the whole domain / M_b <= {gauss:.1e} for every operator and configuration (each region's "
  f"phantom is compensated at its own edge); enclosed at 0.9 R_e (isolated, canonical): " + ", ".join(
    f"{gname(gt)} {TX[('iso', gt, 'canonical')]['O']['A_D']['Mph_in'] / TX[('iso', gt, 'canonical')]['info']['Mb_rd']:.2f} M_b(<0.9Re)"
    for gt in GATES))
for gt in GATES:
    t_ = TX[("iso", gt, "canonical")]; O = t_["O"]
    cd, pd = t_["info"]["carrier_depth"], O["A_D"]["depth"]
    P(f"    WELL DEPTH {gname(gt)} (isolated, canonical, centre -> 0.9 R_e): carrier (Newtonian phi, all operators) "
      f"{cd:.3e} (km/s)^2 [v_esc {math.sqrt(2 * cd):.0f} km/s]; baryons add the phantom {pd:.3e} (A_D) -- B {O['B']['depth'] / pd - 1:+.1e}, "
      f"C {O['C']['depth'] / pd - 1:+.1e}; with g_e = 0.003 B {t_['ext'][0.003]['depth'] / pd - 1:+.1e}")
# the edge definition and the region labelling
ea = [diffs(TX[(c_, gt, f)]["O"]["C_abs"], TX[(c_, gt, f)]["O"]["C"]) for c_ in ("iso", "pair1.0") for gt in GATES for f in FOOTS]
P(f"    EDGE DEFINITION (C_abs - C, same operator, edge +5-6%): lensing mass change at R = 0.1/0.25/0.5/1 Mpc up to " +
  "/".join(f"{max(abs(d[('L', r)]) for d in ea):.1e}" for r in R4) + f"; monopole force {max(mx(d, 'F') for d in ea):.1e} (shell theorem)")
t_ = TX[("nb13", GATES[0], "canonical")]["info"]
P(f"    EDGE DEFINITION flips the labelling: nb13 at {gname(GATES[0])} is {t_['n_regions']} regions under the contrast gate and "
  f"{t_['n_regions_abs']} under the absolute one (the neighbour enters C_abs's kernel at first order: see the nb13 rows)")
for cname in ("pair0.5", "pair1.0"):
    for gt in (GATES[0], GATES[3]):
        O = TX[(cname, gt, "canonical")]["O"]
        P(f"    {cname} {gname(gt)}: phantom pull on cluster 2's baryons (km/s)^2/Mpc: A_D {O['A_D']['F2']:.4e}, B {O['B']['F2']:.4e} "
          f"({O['B']['F2'] / O['A_D']['F2'] - 1:+.1e}), C {O['C']['F2']:.4e} ({O['C']['F2'] / O['A_D']['F2'] - 1:+.1e}); the same pair "
          f"labelled as two touching regions (split at the midplane) C_two {O['C_two']['F2']:+.4e}" +
          (" (sign reversed: the split plane's negative edge layer repels)" if O['C_two']['F2'] * O['C']['F2'] < 0 else
           f" ({O['C_two']['F2'] / O['C']['F2'] - 1:+.0%})"))

# X-SCREEN: a separated similar cluster
scr = []
for gt in GATES:
    for f in FOOTS:
        t_ = TX[("nb13", gt, f)]; O = t_["O"]
        if t_["info"]["n_regions"] < 2:
            continue
        dB = max(abs(O["B"][("F", r)] / O["A_D"][("F", r)] - 1) + abs(O["B"][("D", r)] - O["A_D"][("D", r)]) / abs(O["A_D"][("F", r)]) for r in R4)
        dA = max(abs(O["A_0.5"][("F", r)] / O["A_D"][("F", r)] - 1) + abs(O["A_0.5"][("D", r)] - O["A_D"][("D", r)]) / abs(O["A_D"][("F", r)]) for r in R4)
        di = TX[("iso", gt, f)]["O"]
        dAi = max(abs(di["A_0.5"][("F", r)] / di["A_D"][("F", r)] - 1) + abs(di["A_0.5"][("D", r)] - di["A_D"][("D", r)]) / abs(di["A_D"][("F", r)]) for r in R4)
        scr.append((gt, f, t_["info"]["gap"], dB, dA, dAi))
for s_ in scr:
    P(f"    nb13 {gname(s_[0])} [{s_[1]}]: gap {s_[2]:.2f} Mpc; response to the neighbour: B {s_[3]:.2e}, A(1/m = 0.5) {s_[4]:.2e} "
      f"(isolated A(0.5) - A_D {s_[5]:.1e}; L361 transmission for this gap ~{N61['transmission'](0.5, 5.0, 5.0 + s_[2]):.1e})")
okS = len(scr) > 0 and all(s_[4] <= 0.1 * s_[3] + 1e-6 for s_ in scr)
check("X-SCREEN a similar cluster 13 Mpc away in its own region: (B)'s kernel reads it (its field, ~3e-3 a0, enters at first "
      "order), while (A) at 1/m = 0.5 Mpc sees it only through the screened gap (response < 10% of B's)",
      f"{len(scr)} separated cells; max B {max(s_[3] for s_ in scr) if scr else float('nan'):.2e}, max A(0.5) "
      f"{max(s_[4] for s_ in scr) if scr else float('nan'):.2e}", okS,
      "a separated region is an external field for (B) and nothing for (A) and (C)")

# ============================================================================================ R  convergence
banner("R  CONVERGENCE: three meshes (cells 50/35/25 kpc inner, 200/140/100 kpc outer), gate z = 0.4 p = 2, canonical")
CONV = {}
for (hf, hm) in ((0.05, 0.2), (0.035, 0.14), (0.025, 0.1)):
    g2 = GP if hf == 0.025 else make_grid(hf, hm)
    T_ = TX if hf == 0.025 else run_matrix(g2, {k_: CONFS[k_] for k_ in ("iso", "nb5", "pair1.0")}, [GATES[3]], ["canonical"], verbose=False)
    row = {}
    for cname in ("iso", "nb5", "pair1.0"):
        O = T_[(cname, GATES[3], "canonical")]["O"]; d = diffs(O["B"], O["A_D"])
        row[cname] = (mx(d, "F"), abs(d["depth"]), mx(d, "D"), mx(d, "L"), O["A_D"][("F", 1.0)])
    O = T_[("iso", GATES[3], "canonical")]
    for ge in (0.003, 0.01):
        d = diffs(O["ext"][ge], O["O"]["B"]); row[f"ext{ge}"] = (mx(d, "F"), abs(d["depth"]), mx(d, "D"), mx(d, "L"), O["ext"][ge]["push"] / (ge * a0c_))
    CONV[hf] = row
    P(f"    cells {hf * 1e3:.0f}/{hm * 1e3:.0f} kpc ({g2.N} cells): " + "; ".join(
        f"{k_} B-ref mono {v[0]:.2e} depth {v[1]:.1e} dip {v[2]:.1e} lens {v[3]:.1e}" + (f" push {v[4]:.3f} g_e" if k_.startswith("ext") else "")
        for k_, v in row.items()))
cm = max(abs(CONV[0.025][k_][0] - CONV[0.035][k_][0]) for k_ in CONV[0.025])
cd = max(abs(CONV[0.025][k_][2] - CONV[0.035][k_][2]) for k_ in CONV[0.025])
check("R1 the retention observables converge: between the two finest meshes the B-vs-A monopole force differences move by "
      "< 1e-3 and the dipole (net push) differences by < 3e-3 (fractions of the phantom force)", f"max change: mono {cm:.1e}, dipole {cd:.1e}",
      cm < 1e-3 and cd < 3e-3, "the lensing-mass differences are floor-limited (the staircase edge layer) and reported, not gated")

# ============================================================================================ H  Harvey
banner("H  HARVEY+2015 (L370's configuration, toward-main orientation, z = 0.4): the substructure's lensing centroid")
ZH = 0.4
def harvey_grid(hf, hm):
    re = axis_edges(0.0, 0.0, 400., [(0, 0.35, hf), (0, 6.0, hm)])
    ze = axis_edges(0.0, -400., 400., [(-0.15, 0.65, hf), (-6.0, 6.5, hm)])
    return Grid2D(re, ze)

def sky_rows(g2, rho, ys, jsel):
    Y2 = ys[:, None] ** 2
    Pm = 2 * (np.sqrt(np.maximum(g2.re[None, 1:] ** 2 - Y2, 0)) - np.sqrt(np.maximum(g2.re[None, :-1] ** 2 - Y2, 0)))
    return Pm @ rho[:, jsel]

def centroid_z(g2, S, ys, jsel, zc0, Rap, it=25):
    zl, zh = g2.ze[jsel], g2.ze[jsel + 1]
    wy = np.full(len(ys), ys[1] - ys[0]); wy[0] *= 0.5; wy[-1] *= 0.5; wy *= 2.0
    zc = zc0
    for _ in range(it):
        Yz = np.sqrt(np.maximum(Rap ** 2 - ys ** 2, 0.0))[:, None]
        lo = np.maximum(zl[None, :], zc - Yz); hi = np.minimum(zh[None, :], zc + Yz); L_ = np.clip(hi - lo, 0, None)
        zc = float((S * 0.5 * (hi ** 2 - lo ** 2) * (L_ > 0) * wy[:, None]).sum() / (S * L_ * wy[:, None]).sum())
    return zc

def lensing_1d(H, z, a0, p, xc0):                                     # L370:219-234 (the region connected to the centre)
    inside = (1.5 * H.rho / rho_crit(z)) >= X_thr(z, p, xc0); f = np.cumprod(inside).astype(float)
    ML = H.Mr + f * (nu_mono(G * H.Mb / RG1 ** 2 / a0) - 1.0) * H.Mb
    diff = ML - 200 * rho_crit(z) * 4 / 3 * math.pi * RG1 ** 3
    i = int(np.argmax((diff[:-1] > 0) & (diff[1:] <= 0)))
    return float(np.interp(RG1[i] - diff[i] * (RG1[i + 1] - RG1[i]) / (diff[i + 1] - diff[i]), RG1, ML))

def solve_real(M200L, z, a0, p, xc0, fgas, fstar):                   # L370:237-242
    M = brentq(lambda M: lensing_1d(Halo(M, z, fgas, fstar, a_bcg=0.03), z, a0, p, xc0) - M200L, 0.2 * M200L, 3.0 * M200L, rtol=1e-6)
    return Halo(M, z, fgas, fstar, a_bcg=0.03)

def harvey(g2, gt, foot, Msub, dSG, ops, rs_list=(1.5,), gexts=(0.003, -0.003, 0.01, -0.01)):
    z_, p_, x_ = gt; X_ = X_thr(*gt); a0_ = A0[foot]
    Hm = solve_real(1e15, ZH, a0_, p_, x_, 0.125, 0.015); Hs = solve_real(Msub, ZH, a0_, p_, x_, 0.10, 0.02)
    bm, cm_ = paint(g2, Hm.rho_b), paint(g2, Hm.rho_c)
    ss, cs = paint(g2, Hs.rho_s, 0.4), paint(g2, Hs.rho_c, 0.4); gs = paint(g2, Hs.rho_g, 0.4 - dSG)
    rb = bm + ss + gs; rr = rb + cm_ + cs
    reg = lambda d_, ab=False: regions(g2, d_, X_, [0.0], absolute=ab, z=ZH)[0]
    mk, mk0, mkA, mk0A = reg(rr), reg(bm + cm_), reg(rr, True), reg(bm + cm_, True)
    R = {}
    if "A_D" in ops: R["A_D"] = (op_AD(g2, rb, mk, a0_), op_AD(g2, bm, mk0, a0_))
    if "A_0.2" in ops: R["A_0.2"] = (op_Am(g2, rb, mk, a0_, 0.2), op_Am(g2, bm, mk0, a0_, 0.2))
    if "A_0.5" in ops: R["A_0.5"] = (op_Am(g2, rb, mk, a0_, 0.5), op_Am(g2, bm, mk0, a0_, 0.5))
    if "C" in ops: R["C"] = (op_C(g2, rb, [mk], a0_), op_C(g2, bm, [mk0], a0_))
    if "C_abs" in ops: R["C_abs"] = (op_C(g2, rb, [mkA], a0_), op_C(g2, bm, [mk0A], a0_))
    if "B" in ops:
        R["B"] = (op_B(g2, rb, mk, a0_), op_B(g2, bm, mk0, a0_))
        for ge in gexts:
            R[f"B{ge:+g}"] = (op_B(g2, rb, mk, a0_, ge * a0_), op_B(g2, bm, mk0, a0_, ge * a0_))
    ys = np.linspace(0, 0.16, 161); jsel = np.flatnonzero((g2.zc > 0.2) & (g2.zc < 0.62))
    d3 = np.sqrt(g2.RR ** 2 + (g2.ZZ - 0.4) ** 2)
    out = {}
    for rs in rs_list:
        T_ = np.ones_like(rr) if rs is None else (d3 < rs).astype(float)
        Sre = sky_rows(g2, (rr - bm - cm_) * T_, ys, jsel)
        out[("none", rs)] = [(0.4 - centroid_z(g2, Sre, ys, jsel, 0.4, Ra)) * 1e3 for Ra in (0.1, 0.15)]
        for k_, (rA, rM) in R.items():
            S = Sre + sky_rows(g2, (rA["rho_ph"] - rM["rho_ph"]) * T_, ys, jsel)
            out[(k_, rs)] = [(0.4 - centroid_z(g2, S, ys, jsel, 0.4, Ra)) * 1e3 for Ra in (0.1, 0.15)]
    return out, (Hm.M200, Hs.M200)

GH = harvey_grid(0.01, 0.1)
P(f"    mesh {GH.nr} x {GH.nz} = {GH.N} cells, 10 kpc cells over R < 0.35, z = -0.15..0.65 Mpc; lensing map = projected (real + "
  f"phantom) minus the main cluster alone (as L370:666/678), centroids iterated in 100 and 150 kpc apertures; the region's far "
  f"edge layer is excluded by keeping matter within r_s = 1.5 Mpc of the substructure (see the NOISE diagnostic)")
OPS = ("A_D", "A_0.2", "A_0.5", "B", "C", "C_abs")
HV = {}
for gt in (GATES[3], GATES[2]):
    for foot in FOOTS:
        for Msub in (1e14, 3e14):
            for dSG in (0.06, 0.12):
                out, ms = harvey(GH, gt, foot, Msub, dSG, OPS)
                HV[(gt, foot, Msub, dSG)] = out
                ref = out[("A_D", 1.5)]
                P(f"    {gname(gt)} [{foot}] sub {Msub:.0e} (real M200 {ms[1]:.2e}; main {ms[0]:.2e}) dSG {dSG * 1e3:.0f} kpc: shift toward "
                  f"main (100/150 kpc) A_D {ref[0]:.3f}/{ref[1]:.3f} kpc, excess beta vs no phantom "
                  f"{(ref[0] - out[('none', 1.5)][0]) / (dSG * 1e3):+.4f}/{(ref[1] - out[('none', 1.5)][1]) / (dSG * 1e3):+.4f}; d_beta vs A_D: "
                  + ", ".join(f"{k_} {(v[0] - ref[0]) / (dSG * 1e3):+.1e}/{(v[1] - ref[1]) / (dSG * 1e3):+.1e}"
                              for (k_, rs), v in out.items() if rs == 1.5 and k_ not in ("A_D", "none")))
dbeta = {}
for key_, out in HV.items():
    dSG = key_[3]; ref = out[("A_D", 1.5)]
    for (k_, rs), v in out.items():
        if rs == 1.5 and k_ not in ("A_D", "none"):
            dbeta.setdefault(k_, []).append(max(abs(v[i] - ref[i]) / (dSG * 1e3) for i in (0, 1)))
DB = {k_: max(v) for k_, v in dbeta.items()}
P("    max |d_beta| vs A_D over configurations and apertures: " + ", ".join(f"{k_} {v:.1e}" for k_, v in DB.items()))
# stability in r_s and in resolution, and the NOISE diagnostic
out_rs, _ = harvey(GH, GATES[3], "canonical", 1e14, 0.06, ("A_D", "B", "C"), rs_list=(1.0, 1.5, 2.0, None), gexts=())
P("    r_s stability (1e14, 60 kpc, z = 0.4 p = 2): " + "; ".join(
    f"r_s {rs}: " + ", ".join(f"{k_} {out_rs[(k_, rs)][0]:.3f}" for k_ in ("A_D", "B", "C")) for rs in (1.0, 1.5, 2.0)))
noise = {}
for (hf, hm) in ((0.01, 0.1), (0.01, 0.05)):
    g2 = GH if hm == 0.1 else harvey_grid(hf, hm)
    for gt in (GATES[3], GATES[2]):
        o_ = out_rs if (hm == 0.1 and gt == GATES[3]) else harvey(g2, gt, "canonical", 1e14, 0.06, ("A_D", "B", "C"), rs_list=(1.5, None), gexts=())[0]
        noise[(hm, gt)] = {k_: (o_[(k_, None)][0], o_[(k_, 1.5)][0]) for k_ in ("A_D", "B", "C")}
        P(f"    NOISE (far edge layer INCLUDED) outer cells {hm * 1e3:.0f} kpc, {gname(gt)}: 100-kpc shift " +
          ", ".join(f"{k_} {v[0]:.3f} kpc (excluded: {v[1]:.3f})" for k_, v in noise[(hm, gt)].items()))
spread = max(abs(v[0] - v[1]) for d_ in noise.values() for v in d_.values())
spreadBC = max(abs(d_[k_][0] - d_[k_][1]) for d_ in noise.values() for k_ in ("B", "C"))
P(f"    NOISE summary: including the far edge layer moves the 100-kpc centroid by up to {spread:.2f} kpc (A_D) and "
  f"{spreadBC:.2f} kpc (B, C: the operator of the L370-family runs), i.e. d_beta up to {spreadBC / 60:.3f} at a 60 kpc offset")
res_ = {}
for (hf, hm) in ((0.02, 0.2), (0.015, 0.15)):
    o_ = harvey(harvey_grid(hf, hm), GATES[3], "canonical", 1e14, 0.06, ("A_D", "B", "C"), rs_list=(1.5,), gexts=(0.003,))[0]
    res_[hf] = o_
    P(f"    resolution {hf * 1e3:.0f}/{hm * 1e3:.0f} kpc: shift A_D {o_[('A_D', 1.5)][0]:.3f}, B {o_[('B', 1.5)][0]:.3f}, C {o_[('C', 1.5)][0]:.3f}, "
      f"B(+0.003) {o_[('B+0.003', 1.5)][0]:.3f} kpc")
hv_ok = all(v <= 2e-3 for k_, v in DB.items() if k_ in ("A_0.2", "A_0.5", "B", "C", "C_abs", "B+0.003", "B-0.003"))
check("H1 HARVEY: with the far edge layer excluded, every operator (A at 1/m = 0.2/0.5, B, C, C_abs, and B with a realistic "
      "external field g_e = +/-0.003 a0) gives the Dirichlet operator's substructure centroid to |d_beta| <= 0.002 (Harvey's "
      "sigma_beta = 0.07; L381's S2 margin 0.0086)", ", ".join(f"{k_} {v:.1e}" for k_, v in DB.items()), hv_ok,
      f"the far edge layer, projected along the line of sight, moved the same centroid by up to {spread:.2f} kpc (A_D) and "
      f"{spreadBC:.2f} kpc (B, C) on these staircase meshes -- a numerical effect far larger than any operator effect (README)")

# ============================================================================================ V  verdict
banner("VERDICT")
real = [r_ for r_ in rows if r_[1] == "B"]
b_mono, b_depth, b_mph = max(r_[2] for r_ in real), max(r_[3] for r_ in real), max(r_[4] for r_ in real)
b_push_m = max(r_[6] for r_ in real if r_[0] in ("nb3", "nb5")); b_push_s = max(r_[6] for r_ in real if r_[0] == "nb13")
neg = [TX[(c_, gt, f)]["O"]["B"][("F", 1.0)] / TX[(c_, gt, f)]["O"]["A_D"][("F", 1.0)] - 1 for c_ in ("nb3", "nb5", "nb13", "pair0.5", "pair1.0")
       for gt in GATES for f in FOOTS]
neg += [TX[("iso", gt, f)]["ext"][ge]["F", 1.0] / TX[("iso", gt, f)]["O"]["B"][("F", 1.0)] - 1 for gt in GATES for f in FOOTS for ge in GEXT]
n_weaker = sum(1 for v in neg if v < 0)
Lea = max(max(abs(d[("L", 1.0)]) for d in ea), 0.0)
P(f"""  (a) CLUSTER RETENTION IN THE PM BOXES.  The carrier moves in phi under all three operators, so the operator reaches
      retention only through the phantom that the trigger reads and the baryons feel.  B against the action's A:
      * the retention core (r = 0.1-1 Mpc): the phantom monopole agrees to <= {b_mono:.1e} over merged neighbours (3, 5 Mpc),
        a separated neighbour (13 Mpc) and merger pairs, and to <= {EXT[0.003][0]:.1e} under a realistic external baryonic field
        (0.003 a0; {EXT[0.01][0]:.1e} at 0.01 a0, second order in g_e); the phantom well depth to <= {max(b_depth, EXT[0.003][1]):.1e}
        ({EXT[0.01][1]:.1e} at 0.01 a0).  Numerical floor {FLOOR['F']:.0e}; converged (R1).  For scale, at L377's own cell size
        the discretisation alone (its central differences vs spectral, I3) moves the phantom potential by {dFD:.1%}.
      * the outskirts: the phantom enclosed at 0.9 R_e differs by up to {b_mph:.1e} (the separated neighbour) and
        {EXT[0.003][2]:.1e} at g_e = 0.003 ({EXT[0.01][2]:.1e} at 0.01) -- B's external-field effect, which A does not have.
      * first order in g_e, B adds what A and C do not have: a net phantom push on the region's baryons of
        {EXT[0.003][5]:.1f}-{EXT[0.003][6]:.1f} g_e (a baryon-carrier offset of only ~{DX_EQ[0.003]:.1f} kpc at 0.003 a0) and a phantom field of
        {EXT[0.003][7]:.1f}-{EXT[0.003][8]:.1f} g_e felt by baryons outside the region; the pull toward a separated neighbour
        (<= {b_push_s:.1%} of the phantom force; A: screened).  With MERGED neighbours B and C agree with each other and exceed
        A's pull by <= {b_push_m:.1%} of the phantom force (A's Dirichlet images).
      VERDICT (a): B is a controlled approximation to A for cluster retention inside ~1 Mpc -- error <= {max(b_mono, EXT[0.003][0]):.0e}
      of the phantom monopole at realistic external fields (<= {max(b_mono, EXT[0.01][0]):.0e} up to 0.01 a0) -- and not beyond
      that: in the outskirts and in anything first order in the external field it is a different operator.
      DIRECTION: in {n_weaker}/{len(neg)} perturbed cases B's phantom at 1 Mpc is WEAKER than A's (the EFE and the reading of
      separated structure), so switching B -> A strengthens the phantom slightly: marginally more trigger decays, retention
      marginally LOWER, by an amount far inside the X-COP margin (median 0.32 vs 0.286).
  (b) HARVEY OFFSETS.  With the far edge layer excluded, B, C, C_abs and A (1/m = 0.2, 0.5, inf) agree on the substructure's
      lensing centroid to |d_beta| <= {max(DB[k_] for k_ in ('A_0.2', 'A_0.5', 'B', 'C', 'C_abs')):.0e}; a realistic external field in B
      moves beta by <= {max(DB['B+0.003'], DB['B-0.003']):.0e} ({max(DB['B+0.01'], DB['B-0.01']):.0e} at 0.01 a0), with the sign of its
      direction, so it averages out over orientations.  VERDICT (b): B is a controlled approximation to A for Harvey, and so
      is C; the bound 2e-3 is far below Harvey's sigma_beta = 0.07 and L381's S2 margin 0.0086.  Switching operators does not
      move the Harvey statistic.
  WHAT MATTERS MORE THAN THE OPERATOR.  (1) Region labelling: the same merger pair labelled as two touching regions reverses
      the phantom pull, and L370's absolute-density gate merges the 13 Mpc neighbour into one region at z = 0 (p = 1) where
      the contrast gate keeps two.  (2) The edge definition (absolute vs contrast, +5-6% in radius) changes the projected
      lensing mass at 1 Mpc by up to {Lea:.1e}, more than a realistic external field does ({EXT[0.003][4]:.1e}).  (3) Numerics: the
      region's far edge layer, projected along the line of sight, moved a substructure's centroid by up to {spread:.1f} kpc
      (A_D) and {spreadBC:.1f} kpc (B, C) on staircase meshes -- d_beta up to {spreadBC / 60:.3f} for the operator the L370-family
      Harvey runs use, the size of L381's S2 margin (0.0086); a Harvey map must exclude that layer or show it converged.""")
n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}   [{time.time() - T0:.0f}s]")
sys.exit(0 if n_fail == 0 else 1)
