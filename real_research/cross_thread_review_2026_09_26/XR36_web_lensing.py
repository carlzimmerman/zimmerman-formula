#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR36 (part 3) -- THE TURNAROUND GATE IN THE COSMIC WEB: CMB lensing (Planck 2018, ACT DR6), sigma_8 and the Lyman-alpha forest.
How much of the web's MOND phantom survives a gate that is on only where the matter flow has turned around?

WHY.  XR26 (68135cb7a) found that the chain's separator over-lenses the CMB: Planck's 8-400 amplitude 1.149 against
1.011 +- 0.028 on FP13's linear yardstick (+4.9 sigma), 2.13 on the halofit base; passing needs the web's phantom cut to
f* = 0.62 (linear) / 0.18 (halofit).  The candidate (part 1) switches MOND on only where theta_m = div u <= 0.  The per-mode
linear yardstick cannot see a spatial mask: a linear mode's own divergence is 3H(1 - f delta/3) > 0, so on that yardstick the
gate removes the web's phantom by construction -- but the gate reads the LOCAL flow, and at z < 1 much of the web's mass sits in
collapsing sheets, filaments and knots.  This part measures, on a resolved web, what fraction of the phantom's lensing power
the gate keeps, and scores the result with XR26's own machinery.

THE WEB (XR19's grid, reproduced exactly).  A Zel'dovich web on the record's CLASS P(k) (XR16's head), 128^3 Lagrangian cells
of 0.5 Mpc/h (XR19's box, seed 19).  Per cell and epoch the deformation eigenvalues d_i = D(z) lambda_i give the per-axis
expansion e_i = H (1 - f d_i/(1 - d_i)); an axis that has shell-crossed (d_i >= 1) is virialised along that axis (e_i = 0);
theta = e_1 + e_2 + e_3 (the D1 reading of part 2 on the web).  The gates: SHARP (W = 1 where theta <= 0), RAMP
(clip(1 - theta/3H)), ALL3 (every axis contracting: 3-D bound) and the MUTATE (theta <= 3H: the expanding web counted as turned
around).  The phantom is the chain's real-space operator in its local QUMOND form on the CIC density of the Zel'dovich particles
(the all-matter reading of XR26/FP13): delta_ph = -div[W_E (nu_P2(|g_bp|/a0) - 1) g_bp]/(4 pi G rho_bar a), g_bp the band-passed
Newtonian field (FP13's H_S length, and H_K1's 2.9 Omega_L(<K>_h) Mpc), W_E the mass-weighted gate of the cell's matter.  The
gate's keep-fraction f_gate(k, z) = (sqrt(B_g) - 1)/(sqrt(B_u) - 1), B = P(delta + delta_ph)/P(delta), gated vs ungated.
THE LENSING.  XR26's machinery exec'd from its committed source (CLASS P(k, z) at XR26's committed inputs, FP13's growth yardstick,
the Limber integral, Planck 2018 VIII's MV band powers and amplitudes); the chain's per-mode C_eff is multiplied by f_gate(k, z)
in the growth equation and in the Weyl potential.  Two candidates: HYBRID (the separator's yield kept; the gate acts where the
yield is off, z < 0.635) and GATE-ALONE (the yield removed; the gate is the only switch at every z).

PRE-DECLARED (written before this script's first run; the exploratory scratch runs listed under DISCLOSED came first).
 H1 [load-bearing; MUTATE must fail] the HYBRID with the sharp gate passes Planck 2018's conservative lensing (8-400) on XR26's
    LINEAR base: its amplitude lies within 2 sigma of 1.011 +- 0.028 on both footings (expected ~1.01-1.02: f_gate ~ 0.2).
 H2 (reported) on XR26's halofit base the hybrid is marginal or fails (f_gate ~ 0.2 against the budget 0.18).
 H3 (reported) the ramp keeps f ~ 0.5 (passes the linear base, fails halofit); the all-axes (3-D bound) gate keeps f <~ 0.05.
 H4 sigma_8 of the gated hybrid stays inside FP6's band (0.922-1.05) and below FP13's ungated 1.018-1.023.
 H5 (reported) THE FOREST: every forest absorber (1 + delta = 2-11 at z = 2-3) still expands along at least one axis, but the
    trace theta is <= 0 for most absorbers at 1 + delta >= 5 -- a filament collapsing along two axes has turned around by the
    trace while still expanding along its length; so the GATE-ALONE (no yield) fails FP6's forest proxy (<= 0.10) and the hybrid
    keeps the separator's forest (0).
 H6 (reported) THE BOUND REGIONS (sub-grid halos, a halo model): the phantom ADDED on LCDM halos inside r_on = (1-3) R200 raises
    the 8-400 amplitude by >= 10% in the all-matter reading and less in the baryons-only reading -- both overcount if the chain's
    galaxies have no CDM halos (its premise: galaxy lensing is baryons + phantom), so the web term decides.
 H7 (reported) ACT DR6 (A_lens = 1.013 +- 0.023, 40 <= L <= 763; approximate weights, no ACT likelihood on disk): the hybrid lies
    within 2 sigma.
 AMENDMENT (after the first debug run, a MUTATE run, before any recorded run): L4 now weights by Planck's own MV bin errors inside
    ACT's range (the debug run's two brackets, cosmic-variance and flat-ln-L weights, are kept as brackets): the cosmic-variance
    weighting puts most of the weight at L ~ 500-763, which ACT's reconstruction noise does not.

CHECKS
  K  K1 CONTROL: XR26's committed headline R(L) (linear and halofit bases), its 8-400 amplitudes (both footings) and L2b's phantom
     budget f* reproduced with XR26's own code; K2 CONTROL: XR19's committed C3 eigenvalue statistics (T-web fractions, sigma(delta_lin))
     reproduced exactly; K3 CONTROL: this lane's real-space phantom operator reproduces the plane-wave response A = nu + y nu'
     (parallel) and nu (perpendicular) of DE12's C1 (y = 1e-3, 1e-1) to 2%.
  W  W1 (reported) the web census by epoch: turned-around mass fractions (trace, per axis); W2 f_gate(k, z) for every gate and both
     band-pass lengths; W3 (reported) the web's matter by its expansion rate against a KiDS lens's outskirts (part 2's G10).
  L  L1 [H1, headline]; L2 [H2, H3] the other bases and gates; L3 [H6] the bound regions; L4 [H7] ACT DR6.
  S  S1 [H4] sigma_8.   R  R1 [H5] the forest: the absorber census and the gated forest proxy.
  W9 the ledger.
MUTATE=1: the gate is on at theta <= 3H (the expanding web counted as turned around) in the headline: L1 must FAIL (rc = 1).

SCOPE.  Zel'dovich (exact for single streams; shell-crossed axes treated as virialised) on a 64 Mpc/h box at 0.5 Mpc/h: modes
0.15-6 h/Mpc resolved, f_gate held flat outside that range; the real-space-to-per-mode transfer is a ratio (the gate's keep
fraction) applied to XR26's per-mode yardstick, which XR21 found to overstate the real-space boost (a conservative direction
for the gate's pass); all-matter reading (as XR26); no particle-mesh run of this theory exists.  kappa = 1/2 is FITTED
(Z = kappa = 5.7888) and does not enter; both a0 footings carried.  At most 2 threads.

DISCLOSED.  Exploratory scratch runs (not in the repository) came first: the Zel'dovich census with and without the per-axis
virialisation (without it, 57-65% of the mass counts as turned around at z = 0.25 and f_gate ~ 0.77: most shell-crossed
cells are sheets still expanding in their plane), f_gate against the gate's reading scale (0-2 Mpc/h: 0.19-0.23), and the
absorber census at z = 2-3.  H1-H7 were written after them.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR36_web_lensing.py   (MUTATE=1 for the
control; ~5-8 min, ~2 GB).  Writes XR36_web_lensing[_MUTATE].out and _results[_MUTATE].json next to itself.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "2"
import sys, io, json, math, time, contextlib, warnings
warnings.filterwarnings("ignore")
import numpy as np
from scipy.optimize import brentq, minimize
from scipy.integrate import solve_ivp, quad
from scipy.interpolate import CubicSpline, RectBivariateSpline

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CHAIN = os.path.join(REPO, "real_research", "derivation_chain_2026")
MUTATE = os.environ.get("MUTATE", "0") == "1"
NAME = "XR36_web_lensing"
TXT = os.path.join(HERE, NAME + ("_MUTATE.out" if MUTATE else ".out"))
JSN = os.path.join(HERE, NAME + ("_results_MUTATE.json" if MUTATE else "_results.json"))
T_START = time.time()
_trap = getattr(np, "trapezoid", None) or np.trapz


class _Tee:
    def __init__(self, path):
        self._f = open(path, "w", encoding="utf-8")
        self._s = sys.__stdout__

    def write(self, t):
        self._s.write(t)
        self._f.write(t)

    def flush(self):
        self._s.flush()
        self._f.flush()


sys.stdout = _Tee(TXT)
OUT = {"lane": "XR36", "part": "3: the web -- CMB lensing, sigma_8, forest", "mutate": MUTATE, "checks": {}, "numbers": {}, "ledger": []}
CH = []


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)


def el():
    return f"[{time.time() - T_START:.0f} s]"


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing, "name": name}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the headline gate is on at theta <= 3H (the expanding web counted as turned around) -- L1 must FAIL ***")

# ================================================================================================ XR26's machinery (its committed source)
P26 = os.path.join(HERE, "XR26_cmb.py")
S26 = open(P26).read()
R26 = json.load(open(os.path.join(HERE, "XR26_cmb_results.json")))["numbers"]


def cut(a, b):
    ia, ib = S26.index(a), S26.index(b)
    assert S26.count(a) == 1 and S26.count(b) == 1, (a, b)
    return "\n" * S26[:ia].count("\n") + S26[ia:ib]


from classy import Class
X26 = {"np": np, "math": math, "os": os, "json": json, "time": time, "sys": sys, "io": io, "contextlib": contextlib,
       "brentq": brentq, "minimize": minimize, "solve_ivp": solve_ivp, "CubicSpline": CubicSpline, "RectBivariateSpline": RectBivariateSpline,
       "HERE": HERE, "REPO": REPO, "CHAIN": CHAIN, "MUTATE": False, "P": lambda *a, **k: None, "banner": lambda *a, **k: None,
       "el": lambda: "", "check": lambda *a, **k: True, "OUT": {"numbers": {}, "checks": {}}, "Class": Class, "T_START": time.time(),
       "__file__": P26, "__name__": "xr26_readonly"}
K1_26 = R26["K1"]
X26.update(H0_camb=K1_26["H0"], YHE=K1_26["YHe"], cder={"zstar": K1_26["zstar"]})
_t = time.time()
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(cut("def exec_ro(path, stop=None):", 'P(__doc__.strip())'), P26, "exec"), X26)
    exec(compile(cut("# ================================================================================================ inputs (published, committed)",
                     "import camb"), P26, "exec"), X26)
    exec(compile(cut("H_FID = H0_camb / 100.0", "cl_fid = classy_run("), P26, "exec"), X26)
    X26["cl_fid"] = X26["classy_run"](pk={"P_k_max_h/Mpc": 30.0, "z_max_pk": 50.0})
    X26["LENS"] = X26["cl_fid"].lensed_cl(X26["LMAX"])
    exec(compile(cut("# ---- FP13's (H_S) growth yardstick", "f13 = json.load("), P26, "exec"), X26)
    exec(compile(cut("# ---- Limber machinery on CLASS's P18 fiducial", "tL = time.time()"), P26, "exec"), X26)
    X26["LIMB_FID"] = {b: X26["limber_pp"](b) for b in ("NL", "lin")}
    exec(compile(cut("# ================================================================================================ L late-time lensing",
                     'g_head = L2["8-400"]["rows"][(HEAD, "NL")]'), P26, "exec"), X26)
    exec(compile(cut("def amp_for_f(f_, base=\"lin\"):", "FS = [0.0, 0.1, 0.2"), P26, "exec"), X26)
P(f"\n  XR26's machinery exec'd from its committed source (inputs, classy_run at XR26's committed H0/YHe, FP13's yardstick, Limber, "
  f"the L section's growth and band powers, amp_for_f) ({time.time() - _t:.0f} s)")
HEAD = X26["HEAD"]; RL = X26["RL"]; L_G = X26["L_G"]; LIMB_FID = X26["LIMB_FID"]; limber_pp = X26["limber_pp"]
growth_ceff, hs_model, LCDM_MODEL = X26["growth_ceff"], X26["hs_model"], X26["LCDM_MODEL"]
KH, KHF, DI, DIF, A0_9, FOOTS, MODES = X26["KH"], X26["KHF"], X26["DI"], X26["DIF"], X26["A0_9"], X26["FOOTS"], X26["MODES"]
Z_L, GL, bandpowers, PL18_MV, LENS_AMP = X26["Z_L"], X26["GL"], X26["bandpowers"], X26["PL18_MV"], X26["LENS_AMP"]
sigma8_of, S8_LCDM, cutfac, YIELD, yh, Lh, h9 = X26["sigma8_of"], X26["S8_LCDM"], X26["cutfac"], X26["YIELD"], X26["yh"], X26["Lh"], X26["h9"]
M6_26 = X26["M6"]
cl_fid = X26["cl_fid"]

# ================================================================================================ K controls
banner("K  CONTROLS: XR26's lensing numbers; XR19's eigenvalue statistics; the real-space phantom operator")
dev_R = 0.0
for base in ("NL", "lin"):
    ref = R26["L1"]["R"][f"{HEAD} || {base}"]
    for Ls, v in ref.items():
        dev_R = max(dev_R, abs(float(np.interp(int(Ls), L_G, RL[(HEAD, base)])) / v - 1))
dev_A = 0.0
for kk_, v in X26["L2"]["8-400"]["rows"].items():
    refv = R26["L2"]["8-400"]["rows"][f"{kk_[0]} || {kk_[1]}"]["amp"]
    dev_A = max(dev_A, abs(v["amp"] / refv - 1))
amps_f = {b: [X26["amp_for_f"](f_, b) for f_ in R26["L2b"]["f"]] for b in ("lin", "NL")}
dev_f = max(abs(a_ / b_ - 1) for b in ("lin", "NL") for a_, b_ in zip(amps_f[b], R26["L2b"]["amps"][b]))
P(f"    XR26 headline R(L) (lin base) at 100/400/1000: " + "/".join(f"{np.interp(L_, L_G, RL[(HEAD, 'lin')]):.5f}" for L_ in (100, 400, 1000))
  + f"; 8-400 amplitude lin {X26['L2']['8-400']['rows'][(HEAD, 'lin')]['amp']:.6f} (committed {R26['L2']['8-400']['rows'][HEAD + ' || lin']['amp']:.6f}), "
  f"halofit {X26['L2']['8-400']['rows'][(HEAD, 'NL')]['amp']:.6f}; L2b amps at f = 0.2: {amps_f['lin'][2]:.6f} / {amps_f['NL'][2]:.6f}")
check("K1 CONTROL: XR26's machinery (exec'd from its committed source at its committed inputs) reproduces XR26's committed headline R(L) "
      "(8 multipoles, linear and halofit bases), its 8-400 amplitudes (4 variants x 2 bases) and L2b's phantom-budget amplitudes (8 f x 2 bases)",
      f"max relative deviation: R(L) {dev_R:.1e}; amplitudes {dev_A:.1e}; L2b {dev_f:.1e}", max(dev_R, dev_A, dev_f) <= 1e-9)
OUT["numbers"]["K1"] = dict(dev_R=dev_R, dev_A=dev_A, dev_f=dev_f)

# ---- XR19's web (its recipe: XR16's head for the record's CLASS P(k), the Web construction up to the eigenvalues)
sys.path.insert(0, HERE)
import XR19_common as X19
P16 = os.path.join(HERE, "XR16_fluid_conversion_surface.py"); _s16 = open(P16).read()
_MC = "# ================================================================================================ C1-C5 controls"
NS16 = {"__name__": "xr16", "__file__": P16}
_old = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(_s16.split(_MC)[0].replace('P(__doc__.split("CHECKS")[0].strip())', "pass"), NS16)
finally:
    if _old is None:
        os.environ.pop("MUTATE", None)
    else:
        os.environ["MUTATE"] = _old
KH57, P057 = NS16["A"]["L57"]["KH"], NS16["A"]["L57"]["P0"]
NG, LBOX, SEED = 128, 64.0, 19
Rs = LBOX / NG
rng = np.random.default_rng(SEED)
kx = 2 * np.pi * np.fft.fftfreq(NG, d=Rs); kz = 2 * np.pi * np.fft.rfftfreq(NG, d=Rs)
KX, KY, KZ = np.meshgrid(kx, kx, kz, indexing="ij"); K2 = KX ** 2 + KY ** 2 + KZ ** 2
Pg = np.interp(np.sqrt(K2), KH57, P057, left=0, right=0) * np.exp(-K2 * Rs ** 2)
DK0 = np.fft.rfftn(rng.normal(size=(NG, NG, NG))) * np.sqrt(Pg * NG ** 3 / LBOX ** 3); DK0[0, 0, 0] = 0
K2s = K2.copy(); K2s[0, 0, 0] = 1.0
PSI = np.stack([np.fft.irfftn(1j * a_ / K2s * DK0, s=(NG, NG, NG)).astype(np.float32).ravel() for a_ in (KX, KY, KZ)], -1)
Tm = np.empty((NG ** 3, 3, 3), np.float64)
for i, a_ in enumerate((KX, KY, KZ)):
    for j, b_ in enumerate((KX, KY, KZ)):
        if j < i:
            continue
        c_ = np.fft.irfftn(a_ * b_ / K2s * DK0, s=(NG, NG, NG)).ravel()
        Tm[:, i, j] = c_; Tm[:, j, i] = c_
LAM = np.linalg.eigvalsh(Tm)[:, ::-1].astype(np.float32); del Tm
sig_grid = float(np.std(LAM.sum(1)))
kk_ = np.geomspace(1e-4, KH57[-1], 20000)
sig_class = float(np.sqrt(_trap(kk_ ** 2 * np.interp(kk_, KH57, P057) * np.exp(-kk_ ** 2 * Rs ** 2), kk_) / (2 * np.pi ** 2)))
tweb = np.bincount((LAM > 0).sum(1), minlength=4) / LAM.shape[0]
R19 = json.load(open(os.path.join(HERE, "XR19_web_runaway_results.json")))["numbers"]["C3"]
k2_ok = tweb.tolist() == R19["tweb"] and sig_grid == R19["sigma_grid"] and sig_class == R19["sigma_class"]
P(f"    XR19's grid rebuilt: T-web {np.round(tweb, 6).tolist()} (committed {np.round(R19['tweb'], 6).tolist()}); sigma {sig_grid!r} / {sig_class!r}   {el()}")
check("K2 CONTROL: XR19's web rebuilt with its own recipe (XR16's head for the record's CLASS P(k); 128^3, 64 Mpc/h, seed 19) reproduces "
      "XR19's committed C3 exactly: the T-web fractions at threshold 0 and the grid's and CLASS's sigma(delta_lin)",
      f"bit-identical: {k2_ok}", k2_ok)
OUT["numbers"]["K2"] = dict(tweb=tweb.tolist(), sigma_grid=sig_grid, sigma_class=sig_class)

# ---- the real-space phantom operator: DE12 C1's plane-wave response
nu_p2 = lambda y: np.sqrt(1.0 + 1.0 / np.maximum(y, 1e-300))
ynu_p = lambda y: -0.5 / (y * np.sqrt(1.0 + 1.0 / y))                         # y nu'(y) for P2


def phantom_flux(g, a0v, W=None):
    """the local QUMOND phantom flux (nu_P2(|g|/a0) - 1) g, gated by W (cell by cell)."""
    gm = np.sqrt(g[0] ** 2 + g[1] ** 2 + g[2] ** 2); fac = nu_p2(gm / a0v) - 1.0
    if W is not None:
        fac = fac * W
    return [fac * c_ for c_ in g]


N1_ = 48; L1_ = 1.0
k1x = np.fft.fftfreq(N1_, d=L1_ / N1_) * 2 * np.pi
Q1X, Q1Y, Q1Z = np.meshgrid(k1x, k1x, k1x, indexing="ij"); Q2 = Q1X ** 2 + Q1Y ** 2 + Q1Z ** 2; Q2[0, 0, 0] = 1.0
xs1 = np.arange(N1_) * L1_ / N1_
XX, YY, _ZZ = np.meshgrid(xs1, xs1, xs1, indexing="ij")
k3 = {}
for y0 in (1e-3, 1e-1):
    for th, (mx, my) in (("par", (1, 0)), ("perp", (0, 1))):
        eps = 1e-6 * y0
        kv = 2 * np.pi * np.array([mx, my]) / L1_
        drho = eps * np.cos(kv[0] * XX + kv[1] * YY)                          # 4 pi G delta rho (units a0 per length)
        dphiF = -np.fft.fftn(drho) / Q2
        gx = np.real(np.fft.ifftn(1j * Q1X * dphiF)) + y0; gy = np.real(np.fft.ifftn(1j * Q1Y * dphiF)); gz = np.real(np.fft.ifftn(1j * Q1Z * dphiF))
        F1 = phantom_flux([gx, gy, gz], 1.0); F0 = phantom_flux([np.full_like(gx, y0), 0 * gy, 0 * gz], 1.0)
        div = sum(np.real(np.fft.ifftn(1j * QQ * np.fft.fftn(a_ - b_))) for QQ, a_, b_ in zip((Q1X, Q1Y, Q1Z), F1, F0))
        Am = float(np.sum(div * drho) / np.sum(drho * drho)) + 1.0
        Ap = float(nu_p2(y0) + (ynu_p(y0) if th == "par" else 0.0))
        k3[f"{y0:g}/{th}"] = (Am, Ap)
dev3 = max(abs(a_ / b_ - 1) for a_, b_ in k3.values())
P("    plane-wave response: " + ", ".join(f"y = {k_}: measured {a_:.4f}, predicted {b_:.4f}" for k_, (a_, b_) in k3.items()))
check("K3 CONTROL: this lane's real-space phantom operator reproduces DE12 C1's plane-wave response A = nu + y nu' (along the field) "
      "and nu (across) at y = 1e-3 and 1e-1 to 2%", f"max relative deviation {dev3:.1e}", dev3 < 0.02)
OUT["numbers"]["K3"] = {k_: list(v) for k_, v in k3.items()}
P(f"    {el()}")

# ================================================================================================ W the web census and f_gate
banner("W  THE WEB CENSUS AND THE GATE'S KEEP-FRACTION f_gate(k, z) (per-axis virialisation; both band-pass lengths; canonical and alt)")
G_SI, MPC_SI = 6.6743e-11, 3.0857e22
hW = 0.6736; H0W = 100 * hW * 1e3 / MPC_SI; RHOC0W = 3 * H0W ** 2 / (8 * math.pi * G_SI)
OMW = X19.OM; OLW = X19.OL
OmL_W = lambda a: OLW / (OMW / a ** 3 + OLW)
Q_L = np.stack(np.meshgrid(*(np.arange(NG) * Rs,) * 3, indexing="ij"), -1).reshape(-1, 3)
KMAG = np.sqrt(K2)
KB_ = np.geomspace(0.12, 6.0, 21); KC_ = np.sqrt(KB_[1:] * KB_[:-1])
IB_ = np.digitize(KMAG.ravel(), KB_)
WB_ = np.ones_like(K2); WB_[:, :, 1:-1] *= 2


def cic(pos, w):
    g = pos / Rs; i0 = np.floor(g).astype(np.int64); fr = g - i0; out = np.zeros(NG ** 3)
    for dx in (0, 1):
        wx = (1 - fr[:, 0]) if dx == 0 else fr[:, 0]
        for dy in (0, 1):
            wy = (1 - fr[:, 1]) if dy == 0 else fr[:, 1]
            for dz in (0, 1):
                wz = (1 - fr[:, 2]) if dz == 0 else fr[:, 2]
                idx = (((i0[:, 0] + dx) % NG) * NG + ((i0[:, 1] + dy) % NG)) * NG + ((i0[:, 2] + dz) % NG)
                out += np.bincount(idx, weights=w * wx * wy * wz, minlength=NG ** 3)
    return out.reshape(NG, NG, NG)


def pk_bins(fk):
    p = (np.abs(fk) ** 2 * WB_).ravel()
    num = np.bincount(IB_, weights=p, minlength=len(KB_) + 1); den = np.bincount(IB_, weights=WB_.ravel(), minlength=len(KB_) + 1)
    return num[1:len(KB_)] / np.maximum(den[1:len(KB_)], 1e-30)


def census(z):
    """per-cell expansion (in units of H) on the Zel'dovich web: e_i = 1 - f d_i/(1 - d_i), 0 on a shell-crossed axis."""
    D, f = X19.Dz(z), X19.fz(z); d = D * LAM.astype(np.float64)
    e = np.where(d < 1, 1 - f * d / np.where(d < 1, 1 - d, 1.0), 0.0)
    th = e.sum(1) / 3.0                                                        # theta/3H
    crossed = (d >= 1).sum(1)
    rho = np.where(crossed == 0, 1 / np.prod(np.where(d < 1, 1 - d, 1.0), axis=1), np.inf)
    return th, e, crossed, rho


GATES = ("sharp", "ramp", "all3", "mut")


def gate_W(g, th, e):
    if g == "sharp":
        return (th <= 0).astype(float)
    if g == "ramp":
        return np.clip(1 - th, 0.0, 1.0)
    if g == "all3":
        return (e.max(1) <= 0).astype(float)
    if g == "mut":
        return (th <= 1.0 + 0.01).astype(float)
    return np.ones_like(th)


Z_C = [0.0, 0.25, 0.5, 0.64, 1.0, 1.5, 2.0, 3.0]
LAWS = {"H_S": lambda a: float(Lh(a)), "H_K1": lambda a: 2.9 * OmL_W(a)}
FG = {}                                                                       # (law, foot, gate) -> array [z, k]
CEN = {}
tW = time.time()
for z in Z_C:
    a = 1 / (1 + z); D = X19.Dz(z)
    pos = (Q_L - D * PSI.astype(np.float64)) % LBOX
    m = cic(pos, np.ones(len(pos))); delta = m / m.mean() - 1; dk = np.fft.rfftn(delta)
    th, e, crossed, rho = census(z)
    WE = {g: cic(pos, gate_W(g, th, e)) / np.maximum(m, 1e-12) for g in GATES}
    CEN[z] = {g: float(gate_W(g, th, e).mean()) for g in GATES}
    CEN[z].update(crossed=[float(np.mean(crossed == c_)) for c_ in range(4)])
    pref = 4 * math.pi * G_SI * OMW * RHOC0W / a ** 2 * (MPC_SI / hW)          # g_k = pref delta_k/k [k in h/Mpc]
    Pm = pk_bins(dk)
    for law, Lf in LAWS.items():
        Lcom = Lf(a) / a * hW
        hk = 1 - np.exp(-0.5 * K2 * Lcom ** 2)
        g = [np.fft.irfftn(1j * (QQ / K2s) * dk * pref * hk, s=(NG, NG, NG)) for QQ in (KX, KY, KZ)]
        for foot in FOOTS:
            a0v = A0_9[foot]
            Bu = None
            for gname in ("none",) + GATES:
                F = phantom_flux(g, a0v, None if gname == "none" else WE[gname])
                divk = sum(1j * QQ * np.fft.rfftn(Fc) for QQ, Fc in zip((KX, KY, KZ), F))
                B = pk_bins(dk - divk / pref) / Pm
                if gname == "none":
                    Bu = B
                    continue
                fg = (np.sqrt(B) - 1) / np.maximum(np.sqrt(Bu) - 1, 1e-12)
                FG.setdefault((law, foot, gname), np.zeros((len(Z_C), len(KC_))))[Z_C.index(z)] = fg
    P(f"    z = {z:4.2f}: mass on (sharp/ramp/all3/mut) " + "/".join(f"{CEN[z][g]:.3f}" for g in GATES) + "; crossed axes 0/1/2/3 "
      + "/".join(f"{x:.3f}" for x in CEN[z]["crossed"]) + "; f_gate at k = 0.3/1 h/Mpc (H_S, canonical) "
      + ", ".join(f"{g}: {np.interp(0.3, KC_, FG[('H_S', 'canonical', g)][Z_C.index(z)]):.3f}/{np.interp(1.0, KC_, FG[('H_S', 'canonical', g)][Z_C.index(z)]):.3f}"
                  for g in GATES) + f"   ({time.time() - tW:.0f} s)")
check("W1 (reported) THE WEB CENSUS: the mass fraction the gate switches on at each epoch (per-axis virialisation: a shell-crossed axis "
      "contributes 0, the others their Zel'dovich expansion) -- most shell-crossed mass is sheets and filaments still expanding "
      "along their other axes",
      "; ".join(f"z = {z}: sharp {CEN[z]['sharp']:.3f}, ramp {CEN[z]['ramp']:.3f}, all3 {CEN[z]['all3']:.3f}, mut {CEN[z]['mut']:.3f}" for z in (0.25, 1.0, 2.0)),
      True, load_bearing=False)
OUT["numbers"]["W1"] = {str(z): v for z, v in CEN.items()}
OUT["numbers"]["W2"] = {f"{k_[0]}/{k_[1]}/{k_[2]}": v.tolist() for k_, v in FG.items()}
OUT["numbers"]["W2_k"] = KC_.tolist(); OUT["numbers"]["W2_z"] = Z_C
fs025 = {g: float(np.mean(FG[("H_S", "canonical", g)][Z_C.index(0.25)][(KC_ > 0.2) & (KC_ < 1.5)])) for g in GATES}
check("W2 (reported) THE GATE'S KEEP-FRACTION of the web phantom's lensing boost at z = 0.25 (k = 0.2-1.5 h/Mpc, H_S's band-pass, "
      "canonical): sharp ~0.2, ramp ~0.5, all-axes <~ 0.05, MUTATE (theta <= 3H) ~0.9",
      ", ".join(f"{g}: {v:.3f}" for g, v in fs025.items()), True, load_bearing=False)
P(f"    {el()}")

# ---- W3: the web's matter by its expansion rate, against a KiDS lens's outskirts (part 2's G10)
th25, e25, cr25, rho25 = census(0.25)
qs = [0.1, 0.25, 0.5, 0.75, 0.9]
qv = np.quantile(th25, qs)
BRJ = os.path.join(HERE, "XR36_bound_regions_results.json")
w3 = dict(web_quantiles=dict(zip([str(q_) for q_ in qs], qv.tolist())))
if os.path.exists(BRJ):
    g10 = json.load(open(BRJ))["numbers"].get("G10", {})
    rq = g10.get("r_Mpc", [])
    if rq:
        j1 = list(rq).index(1.0); j5 = list(rq).index(0.5)
        for kk_, v in g10["thK"].items():
            w3[f"{kk_}"] = dict(th_05=v[j5], th_10=v[j1], web_frac_on_at_05=float(np.mean(th25 <= v[j5])), web_frac_on_at_10=float(np.mean(th25 <= v[j1])))
P("    the web's matter at z = 0.25 by theta/3H (mass quantiles 10/25/50/75/90%): " + "/".join(f"{x:+.2f}" for x in qv))
rows_w3 = {k_: v for k_, v in w3.items() if k_ != "web_quantiles"}
for kk_, v in rows_w3.items():
    P(f"    lens {kk_}: its outskirts expand at theta/3H = {v['th_05']:.2f} (0.5 Mpc) / {v['th_10']:.2f} (1 Mpc); a gate on at those rates "
      f"switches on {v['web_frac_on_at_05']:.2f} / {v['web_frac_on_at_10']:.2f} of the web's mass")
check("W3 (reported) NO EXPANSION THRESHOLD SEPARATES A KiDS LENS'S OUTSKIRTS FROM THE WEB: the matter at 0.5-1 Mpc around an isolated "
      "lens (part 2, the chain's baryons-only flow) expands at a rate that most of the web's matter does not exceed -- a gate on there is "
      "on across most of the web (the CMB then fails as in XR26)",
      ("; ".join(f"{k_}: web fraction switched on {v['web_frac_on_at_05']:.2f} (0.5 Mpc) / {v['web_frac_on_at_10']:.2f} (1 Mpc)" for k_, v in rows_w3.items()
                 if k_.startswith("canonical")) if rows_w3 else "part 2's results not found (run XR36_bound_regions.py first)"),
      bool(rows_w3) and min(v["web_frac_on_at_10"] for v in rows_w3.values()) >= 0.5, load_bearing=False)
OUT["numbers"]["W3"] = w3

# ================================================================================================ the gated yardstick
kmid = np.log(KC_)


def fg_fun(law, foot, gname):
    """f_gate(k [h/Mpc], a) on a k-grid: linear in ln k inside the resolved range (flat outside), linear in z between census
    epochs (held at z = 3 above it)."""
    tab = FG[(law, foot, gname)]

    def f(khg, a):
        z = 1 / a - 1
        zc = min(max(z, Z_C[0]), Z_C[-1]); j = int(np.searchsorted(Z_C, zc)); j = min(max(j, 1), len(Z_C) - 1)
        w = (zc - Z_C[j - 1]) / (Z_C[j] - Z_C[j - 1])
        row = (1 - w) * tab[j - 1] + w * tab[j]
        return np.clip(np.interp(np.log(khg), kmid, row), 0.0, 1.0)
    return f


two_q9, Om9_, Or9_, H09_, Mpc9_ = X26["two_q"], X26["Om9"], X26["Or9"], X26["H09"], X26["Mpc9"]
LK_ = lambda a: 2.9 * OmL_W(a)                                                  # H_K1's band-pass length (FP19), physical Mpc


def hk1_model(foot):
    """FP19's H_K1 in XR26's yardstick form: band-pass L = 2.9 Omega_L(<K>_h) Mpc, the tied yield c_y = 2."""
    yt = lambda a_: 2.0 * max(0.0, two_q9(a_)) * 1.5 * H09_ ** 2 * (Om9_ / a_ ** 3 + Or9_ / a_ ** 4) * LK_(a_) * Mpc9_ / A0_9[foot]
    return {"hfac": lambda a_, k_: 1.0 - np.exp(-0.5 * (k_ * h9 * LK_(a_) / a_) ** 2),
            "cut": lambda y, a_: cutfac(y, yt(a_), YIELD), "yr": 0.0}


def gated_model(foot, gname, yield_on=True, law="H_S"):
    """the separator's yardstick model (XR26's hs_model for H_S; FP19's H_K1) with C_eff multiplied by f_gate(k, z) of the same
    band-pass law; yield_on=False removes the separator's yield (GATE-ALONE)."""
    base = hs_model(foot) if law == "H_S" else hk1_model(foot)
    fgf = fg_fun(law, foot, gname) if gname != "none" else None

    def cutf(y, a_):
        khg = KHF if len(np.atleast_1d(y)) == len(KHF) else KH
        c_ = base["cut"](y, a_) if yield_on else np.ones_like(np.asarray(y, float))
        return c_ * (fgf(khg, a_) if fgf is not None else 1.0)
    return {"hfac": base["hfac"], "cut": cutf, "yr": 0.0}


def lens_of(model, foot, mode="permode"):
    gr = growth_ceff(model, A0_9[foot], mode, Z_L, KHg=KHF, Dig=DIF, lam=0.0, c2=1e15)
    Bz = np.array([((1 + gr[round(z_, 6)][1]) * gr[round(z_, 6)][0] / GL[round(z_, 6)][0]) ** 2 for z_ in Z_L])
    ib = RectBivariateSpline(np.array(Z_L), np.log(KHF), Bz, kx=1, ky=1)
    Bf = lambda k_h, z_: np.where(z_ > Z_L[-1], 1.0, ib(np.minimum(z_, Z_L[-1]), np.log(np.clip(k_h, KHF[0], KHF[-1])), grid=False))
    out = {}
    for base in ("lin", "NL"):
        Rr = limber_pp(base, Bf) / LIMB_FID[base]
        bl = bandpowers(lambda ll: np.ones_like(ll, float), "8-400")
        bc = bandpowers(lambda ll: np.interp(ll, L_G, Rr), "8-400")
        w = 1 / np.array([b_[3] for b_ in PL18_MV["8-400"]]) ** 2
        amp = float(np.sum(w * bc / bl) / np.sum(w))
        dat = np.array([b_[2] * b_[4] for b_ in PL18_MV["8-400"]]); err = np.array([b_[3] * b_[4] for b_ in PL18_MV["8-400"]])
        out[base] = dict(amp=amp, pull=(amp - LENS_AMP["8-400"][0]) / LENS_AMP["8-400"][1], chi2=float(np.sum(((dat - bc) / err) ** 2)),
                         R={str(L_): float(np.interp(L_, L_G, Rr)) for L_ in (100, 400, 1000, 2000)}, Rarr=Rr)
    out["B_z0"] = {str(kv): float(np.interp(math.log(kv), np.log(KHF), Bz[0])) for kv in (0.1, 0.3, 1.0)}
    return out


# ================================================================================================ L1 the headline
banner("L1  THE HEADLINE: the HYBRID (the separator's yield kept) with the sharp gate, Planck 2018 8-400, XR26's linear base"
       + ("  [MUTATE: theta <= 3H]" if MUTATE else ""))
HEAD_GATE = "mut" if MUTATE else "sharp"
L1 = {}
for foot in FOOTS:
    L1[foot] = lens_of(gated_model(foot, HEAD_GATE), foot)
    P(f"    {foot:9s}: 8-400 amplitude lin {L1[foot]['lin']['amp']:.4f} ({L1[foot]['lin']['pull']:+.2f} sigma), halofit {L1[foot]['NL']['amp']:.4f} "
      f"({L1[foot]['NL']['pull']:+.2f} sigma); R(L) lin at 100/400/1000: " + "/".join(f"{L1[foot]['lin']['R'][L_]:.4f}" for L_ in ("100", "400", "1000"))
      + f"; B(k, 0) at 0.1/0.3/1: " + "/".join(f"{v:.3f}" for v in L1[foot]["B_z0"].values()))
chi_lcdm = R26["L2"]["8-400"]["chi2_lcdm"]
l1_ok = all(abs(L1[f]["lin"]["amp"] - LENS_AMP["8-400"][0]) <= 2 * LENS_AMP["8-400"][1] for f in FOOTS)
check("L1 [H1, HEADLINE; MUTATE must fail] THE HYBRID PASSES PLANCK's CONSERVATIVE LENSING on XR26's linear base: with the web's "
      "per-mode phantom multiplied by the sharp gate's keep-fraction f_gate(k, z), the 8-400 amplitude lies within 2 sigma of "
      f"{LENS_AMP['8-400'][0]} +- {LENS_AMP['8-400'][1]} on both footings (XR26's ungated headline: 1.149, +4.9 sigma)",
      "; ".join(f"{f}: {L1[f]['lin']['amp']:.4f} ({L1[f]['lin']['pull']:+.2f} sigma), Delta chi^2 (9 MV bins) {L1[f]['lin']['chi2'] - chi_lcdm:+.2f}" for f in FOOTS),
      l1_ok, reading=("MUTATE: counting the expanding web as turned around keeps ~90% of the web's phantom -- XR26's failure returns"
                      if MUTATE else "the gate keeps ~20% of the web's phantom: the web's sheets and filaments still expand in their "
                                     "other directions, only knots and converging single streams turn it on"))
OUT["numbers"]["L1"] = {f: {b: {k_: v for k_, v in L1[f][b].items() if k_ != "Rarr"} for b in ("lin", "NL")} for f in FOOTS}
P(f"    {el()}")

# ================================================================================================ L2 other bases, gates, candidates
banner("L2  (reported) THE HALOFIT BASE, THE OTHER GATES, THE GATE ALONE (no yield), H_K1's band-pass, the rms mode")
L2 = {}
for foot in FOOTS:
    for gname in ("ramp", "all3", "sharp"):
        for yon in (True, False):
            for law in ("H_S", "H_K1"):
                if (law == "H_K1" and not (gname == "sharp" and yon)) or (gname == "sharp" and yon and law == "H_S" and not MUTATE):
                    continue
                r_ = lens_of(gated_model(foot, gname, yield_on=yon, law=law), foot)
                L2[f"{foot}/{gname}/{'hybrid' if yon else 'alone'}/{law}"] = {b: dict(amp=r_[b]["amp"], pull=r_[b]["pull"]) for b in ("lin", "NL")}
r_rms = lens_of(gated_model("canonical", "sharp"), "canonical", mode="rms")
L2["canonical/sharp/hybrid/H_S/rms"] = {b: dict(amp=r_rms[b]["amp"], pull=r_rms[b]["pull"]) for b in ("lin", "NL")}
for k_, v in L2.items():
    P(f"    {k_:34s}: lin {v['lin']['amp']:.4f} ({v['lin']['pull']:+.2f} sigma), halofit {v['NL']['amp']:.4f} ({v['NL']['pull']:+.2f} sigma)")
hyb_NL = [L1[f]["NL"]["pull"] for f in FOOTS]
check("L2 [H2, H3] (reported) THE HALOFIT BASE AND THE OTHER GATES: the sharp hybrid on XR26's halofit base; the ramp and all-axes gates; "
      "the gate alone (the yield removed: the gate the only switch at every z); H_K1's band-pass; the rms mode -- within 2 sigma?",
      f"sharp hybrid halofit {L1['canonical']['NL']['amp']:.3f}/{L1['alt']['NL']['amp']:.3f} ({max(hyb_NL):+.1f} sigma); "
      f"ramp hybrid lin {L2['canonical/ramp/hybrid/H_S']['lin']['amp']:.3f}, NL {L2['canonical/ramp/hybrid/H_S']['NL']['amp']:.3f}; "
      f"all3 hybrid lin {L2['canonical/all3/hybrid/H_S']['lin']['amp']:.3f}, NL {L2['canonical/all3/hybrid/H_S']['NL']['amp']:.3f}; "
      f"sharp ALONE lin {L2['canonical/sharp/alone/H_S']['lin']['amp']:.3f}, NL {L2['canonical/sharp/alone/H_S']['NL']['amp']:.3f}",
      max(hyb_NL) <= 2.0, load_bearing=False)
OUT["numbers"]["L2"] = L2
P(f"    {el()}")

# ================================================================================================ L3 bound regions (halo model)
banner("L3  (reported) THE BOUND REGIONS: a halo model of the phantom ADDED on LCDM halos inside r_on = x_on R200 (sub-grid)")
hC = cl_fid.h(); OMc = cl_fid.Omega_m(); RHOM = 2.775e11 * OMc                  # Msun h^2/Mpc^3 (comoving, h units: Msun/h per (Mpc/h)^3)
DELC = 1.686
MH = np.geomspace(1e10, 3e15, 70)                                               # Msun/h
KK = np.geomspace(0.01, 30.0, 70)                                               # h/Mpc
ZH = [0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0]


def sigma_M(M, z):
    R = (3 * M / (4 * math.pi * RHOM)) ** (1 / 3) / hC                          # Mpc
    return np.array([cl_fid.sigma(r_, z) for r_ in np.atleast_1d(R)])


def st_dndlnM(M, z):
    s = sigma_M(M, z); nu_ = DELC / s; a_st, p_st, A_st = 0.707, 0.3, 0.3222
    fnu = A_st * np.sqrt(2 * a_st / math.pi) * (1 + (a_st * nu_ ** 2) ** -p_st) * nu_ * np.exp(-a_st * nu_ ** 2 / 2)
    ls = np.log(s); dls = np.gradient(ls, np.log(M))
    return RHOM / M * fnu * np.abs(dls), nu_


def st_bias(nu_):
    a_st, p_st = 0.707, 0.3
    return 1 + (a_st * nu_ ** 2 - 1) / DELC + 2 * p_st / (DELC * (1 + (a_st * nu_ ** 2) ** p_st))


def nfw_profile(M, z):
    """NFW (Duffy+08 c200, 200 x rho_crit(z)) in comoving Mpc/h: r200, rs, and the enclosed-mass function."""
    Ez2 = OMc * (1 + z) ** 3 + (1 - OMc)
    rho200 = 200 * 2.775e11 * Ez2 / (1 + z) ** 3                                # comoving Msun h^2/Mpc^3
    r200 = (3 * M / (4 * math.pi * rho200)) ** (1 / 3)
    c = 5.71 * (M / 2e12) ** -0.084 * (1 + z) ** -0.47
    rs = r200 / c; mc = math.log(1 + c) - c / (1 + c)
    return r200, rs, (lambda r: M * (np.log(1 + np.minimum(r, r200) / rs) - (np.minimum(r, r200) / rs) / (1 + np.minimum(r, r200) / rs)) / mc)


def ft_of_Menc(r, Menc, k):
    """Fourier transform of a spherical density from its enclosed mass on r (Stieltjes sum of dM sinc(kr))."""
    dM = np.diff(Menc); rm = 0.5 * (r[1:] + r[:-1])
    return np.array([np.sum(dM * np.sinc(kk * rm / math.pi)) for kk in k])


def halo_boost(x_on, reading, a0v):
    """B_halo(k, z) = 1 + [1-halo (2 M u_NFW rho_ph + rho_ph^2) + 2-halo cross] / (rho_bar^2 P_NL): the phantom inside r_on,
    compensated at r_on (the local gate), in the all-matter (the halo's NFW field) or baryons-only (f_b of it) reading."""
    fb = 0.157
    out = np.ones((len(ZH), len(KK)))
    for iz, z in enumerate(ZH):
        a = 1 / (1 + z)
        dn, nu_ = st_dndlnM(MH, z); b_ = st_bias(nu_)
        U_nfw = np.zeros((len(MH), len(KK))); U_ph = np.zeros((len(MH), len(KK)))
        for i, M in enumerate(MH):
            r200, rs, Menc = nfw_profile(M, z)
            r = np.geomspace(1e-4 * r200, x_on * r200, 400)
            Mn = Menc(r)
            # physical Newtonian field of the halo's matter (all) or its baryons (f_b), SI
            rphys = r * a / hC * MPC_SI; Mkg = (Mn / hC) * 1.98892e30
            gN = G_SI * Mkg / rphys ** 2 * (1.0 if reading == "all" else fb)
            Mph = (Mn if reading == "all" else fb * Mn) * (nu_p2(gN / a0v) - 1.0)
            Mph_c = np.concatenate([Mph, [0.0]]); r_c = np.concatenate([r, [r[-1] * 1.0001]])     # compensated at r_on
            U_nfw[i] = ft_of_Menc(np.concatenate([[0.0], r]), np.concatenate([[0.0], Mn]), KK)
            U_ph[i] = ft_of_Menc(np.concatenate([[0.0], r_c]), np.concatenate([[0.0], Mph_c]), KK)
        w = dn * np.gradient(np.log(MH))
        P1 = np.sum(w[:, None] * (2 * U_nfw * U_ph + U_ph ** 2), axis=0) / RHOM ** 2
        I_m = np.sum(w[:, None] * b_[:, None] * U_nfw, axis=0) / RHOM; I_p = np.sum(w[:, None] * b_[:, None] * U_ph, axis=0) / RHOM
        Plin = np.array([cl_fid.pk_lin(k_ * hC, z) * hC ** 3 for k_ in KK]); Pnl = np.array([cl_fid.pk(k_ * hC, z) * hC ** 3 for k_ in KK])
        P2 = Plin * (2 * I_m * I_p + I_p ** 2)
        out[iz] = 1.0 + (P1 + P2) / Pnl
    return out


L3 = {}
tH = time.time()
for reading in ("all", "baryons"):
    for x_on in (1.0, 2.0, 3.0):
        Bh = halo_boost(x_on, reading, A0_9["canonical"])
        ib = RectBivariateSpline(np.array(ZH), np.log(KK), Bh, kx=1, ky=1)
        Bf = lambda k_h, z_, ib=ib: np.where(z_ > ZH[-1], 1.0, ib(np.minimum(z_, ZH[-1]), np.log(np.clip(k_h, KK[0], KK[-1])), grid=False))
        Rr = limber_pp("NL", Bf) / LIMB_FID["NL"]
        bl = bandpowers(lambda ll: np.ones_like(ll, float), "8-400"); bc = bandpowers(lambda ll: np.interp(ll, L_G, Rr), "8-400")
        w = 1 / np.array([b_[3] for b_ in PL18_MV["8-400"]]) ** 2
        amp = float(np.sum(w * bc / bl) / np.sum(w))
        L3[f"{reading}/{x_on}"] = dict(amp=amp, pull=(amp - LENS_AMP["8-400"][0]) / LENS_AMP["8-400"][1],
                                       R={str(L_): float(np.interp(L_, L_G, Rr)) for L_ in (100, 400, 1000)},
                                       B_z025={str(kv): float(np.interp(math.log(kv), np.log(KK), Bh[1])) for kv in (0.1, 0.3, 1.0, 3.0)})
        P(f"    {reading:8s} reading, r_on = {x_on:.0f} R200: 8-400 amplitude (halofit base, halos alone) {amp:.4f} ({L3[f'{reading}/{x_on}']['pull']:+.2f} sigma); "
          f"R(100/400/1000) " + "/".join(f"{v:.3f}" for v in L3[f"{reading}/{x_on}"]["R"].values()) + f"; B(k, 0.25) at 0.1/0.3/1/3 "
          + "/".join(f"{v:.3f}" for v in L3[f"{reading}/{x_on}"]["B_z025"].values()) + f"   ({time.time() - tH:.0f} s)")
check("L3 [H6] (reported) THE BOUND REGIONS: the phantom added on LCDM halos inside r_on = 1-3 R200 (all-matter and baryons-only "
      "readings) moves the 8-400 amplitude by the printed amounts -- an overcount if galaxies carry no CDM halo (the chain's premise)",
      "; ".join(f"{k_}: {v['amp']:.3f} ({v['pull']:+.1f} sigma)" for k_, v in L3.items()),
      all(abs(v["amp"] - LENS_AMP["8-400"][0]) <= 2 * LENS_AMP["8-400"][1] for v in L3.values()), load_bearing=False)
OUT["numbers"]["L3"] = L3
P(f"    {el()}")

# ================================================================================================ L4 ACT DR6
banner("L4  (reported) ACT DR6 LENSING: A_lens = 1.013 +- 0.023 over 40 <= L <= 763 (approximate weights; no ACT likelihood on disk)")
ACT = (1.013, 0.023)
LL = np.arange(40, 764)
L4 = {}
BINS_A = [b_ for b_ in PL18_MV["8-2048"] if b_[0] >= 40 and b_[1] <= 763]            # Planck's MV bins inside ACT's range
for foot in FOOTS:
    for base in ("lin", "NL"):
        Rr = L1[foot][base]["Rarr"]; Rl = np.interp(LL, L_G, Rr)
        wcv = (2 * LL + 1.0); wlog = 1.0 / LL
        bl_ = np.array([np.mean([1.0]) for _ in BINS_A])
        Rb = np.array([np.mean(np.interp(np.arange(lo, hi + 1), L_G, Rr)) for (lo, hi, A_, sA, fid) in BINS_A])
        wb = 1 / np.array([sA for (lo, hi, A_, sA, fid) in BINS_A]) ** 2
        L4[f"{foot}/{base}"] = dict(cv=float(np.sum(wcv * Rl) / np.sum(wcv)), log=float(np.sum(wlog * Rl) / np.sum(wlog)),
                                    planck_bins=float(np.sum(wb * Rb) / np.sum(wb)))
for k_, v in L4.items():
    P(f"    {k_:14s}: amplitude with Planck's MV bin weights over 40-763 {v['planck_bins']:.4f} ({(v['planck_bins'] - ACT[0]) / ACT[1]:+.2f} sigma); "
      f"cosmic-variance weights {v['cv']:.4f} ({(v['cv'] - ACT[0]) / ACT[1]:+.2f}); flat per ln L {v['log']:.4f} ({(v['log'] - ACT[0]) / ACT[1]:+.2f})")
check("L4 [H7] (reported) ACT DR6: the hybrid's lensing amplitude over 40-763 on XR26's linear base within 2 sigma of 1.013 +- 0.023, "
      "with Planck's own MV bin errors as the weights inside ACT's range (the cosmic-variance and flat-ln-L weightings bracket it; "
      "no ACT likelihood or noise curve on disk)", "; ".join(f"{k_}: {v['planck_bins']:.3f} [{v['log']:.3f}-{v['cv']:.3f}]" for k_, v in L4.items()),
      all(abs(L4[f"{f}/lin"]["planck_bins"] - ACT[0]) <= 2 * ACT[1] for f in FOOTS), load_bearing=False)
OUT["numbers"]["L4"] = L4

# ================================================================================================ S1 sigma_8
banner("S1  SIGMA_8 of the gated yardstick (FP6's band 0.922-1.05; FP13's ungated H_S 1.018-1.023)")
S1 = {}
for foot in FOOTS:
    for mode in MODES:
        for lab, mod in (("hybrid", gated_model(foot, HEAD_GATE)), ("alone", gated_model(foot, HEAD_GATE, yield_on=False))):
            S1[f"{foot}/{mode}/{lab}"] = sigma8_of(growth_ceff(mod, A0_9[foot], mode, (0.0,))[0.0][0]) / S8_LCDM
P("    " + "; ".join(f"{k_}: {v:.4f}" for k_, v in S1.items()))
check("S1 [H4] SIGMA_8 of the gated hybrid inside FP6's band (0.922-1.05) and below FP13's ungated 1.018-1.023 (per-mode and rms, both "
      "footings); the gate alone printed", ", ".join(f"{k_}: {v:.4f}" for k_, v in S1.items() if k_.endswith("hybrid")),
      all(0.922 <= v <= 1.05 for k_, v in S1.items() if k_.endswith("hybrid")) and all(v <= 1.0228 for k_, v in S1.items() if k_.endswith("hybrid")))
OUT["numbers"]["S1"] = S1

# ================================================================================================ R1 the forest
banner("R1  (reported) THE FOREST: what 'turned around' means for an absorber, and FP6's forest proxy with the gate alone")
R1c = {}
for z in (2.0, 2.5, 3.0):
    th, e, crossed, rho = census(z)
    nexp = (e > 0).sum(1)
    for lo, hi in ((1, 2), (2, 5), (5, 11), (11, 1e9)):
        msk = (crossed == 0) & (rho >= lo) & (rho < hi)
        R1c[f"{z}/{lo}-{hi:g}"] = dict(mass=float(msk.mean()), TA_trace=float(np.mean(th[msk] <= 0)) if msk.any() else float("nan"),
                                       expanding_ge1_axis=float(np.mean(nexp[msk] >= 1)) if msk.any() else float("nan"),
                                       expanding_1_axis_only=float(np.mean(nexp[msk] == 1)) if msk.any() else float("nan"))
for k_, v in R1c.items():
    P(f"    z = {k_.split('/')[0]}, 1 + delta in [{k_.split('/')[1]}): mass {v['mass']:.3f}; turned around by the trace {v['TA_trace']:.3f}; "
      f"expanding along >= 1 axis {v['expanding_ge1_axis']:.3f} (along exactly one: {v['expanding_1_axis_only']:.3f})")
REF_F = M6_26["REF_F"] if "REF_F" in M6_26 else None
fp = {}
for foot in FOOTS:
    for mode in MODES:
        for lab, yon in (("hybrid", True), ("alone", False)):
            mod = gated_model(foot, HEAD_GATE, yield_on=yon)
            res = growth_ceff(mod, A0_9[foot], mode, (2.0, 3.0), KHg=KHF, Dig=DIF)
            ref = growth_ceff(LCDM_MODEL, A0_9[foot], mode, (2.0, 3.0), KHg=KHF, Dig=DIF)
            fp[f"{foot}/{mode}/{lab}"] = max(M6_26["forest_proxy"]({2.0: res[2.0][0], 3.0: res[3.0][0]}, kF=kF, KHg=KHF,
                                                                   REFg={2.0: ref[2.0][0], 3.0: ref[3.0][0]})[0] for kF in (10.0, 15.0, 20.0))
P("    FP6's forest proxy (<= 0.10): " + "; ".join(f"{k_}: {v:.3g}" for k_, v in fp.items()))
absorb = [v for k_, v in R1c.items() if k_.split("/")[1] in ("2-5", "5-11")]
check("R1 [H5] (reported) THE FOREST: every forest absorber (1 + delta = 2-11, z = 2-3) still expands along >= 1 axis, but the trace "
      "has turned around for most at 1 + delta >= 5; the gate alone (no yield) fails FP6's forest proxy, the hybrid keeps the separator's",
      f"absorbers expanding along >= 1 axis: {min(v['expanding_ge1_axis'] for v in absorb):.3f}-{max(v['expanding_ge1_axis'] for v in absorb):.3f}; "
      f"trace-turned-around at 1 + delta = 5-11: " + "/".join(f"{R1c[f'{z}/5-11']['TA_trace']:.2f}" for z in (2.0, 2.5, 3.0))
      + f"; forest proxy hybrid {max(v for k_, v in fp.items() if k_.endswith('hybrid')):.3g}, alone {max(v for k_, v in fp.items() if k_.endswith('alone')):.3g}",
      max(v for k_, v in fp.items() if k_.endswith("hybrid")) <= 0.10, load_bearing=False)
OUT["numbers"]["R1"] = dict(census=R1c, forest_proxy=fp)
P(f"    {el()}")

# ================================================================================================ W9 the ledger
banner("W9  THE LEDGER")
LEDGER = [
    ("XR36-l", "DERIVED", "on a resolved (Zel'dovich) web the turnaround gate keeps ~20% of the web phantom's lensing boost: most "
     "shell-crossed mass is sheets and filaments still expanding along their other axes", "W1, W2"),
    ("XR36-m", "DERIVED" if l1_ok else "FAILS", "the hybrid (the separator's yield kept, the gate at z < 0.635) against Planck's "
     "conservative lensing on XR26's linear base", "L1"),
    ("XR36-n", "CONSTRAINT", "on XR26's halofit base and with the bound regions added on LCDM halos the verdict depends on the halo "
     "reading (the chain's galaxies have no CDM halos)", "L2, L3"),
    ("XR36-o", "CONSTRAINT", "the forest: absorbers keep expanding along one axis but turn around by the trace; the gate alone cannot "
     "replace the separator's yield at z = 2-3", "R1"),
]
for row in LEDGER:
    OUT["ledger"].append(dict(zip(("link", "status", "what", "basis"), row)))
    P(f"    {row[0]:8s} {row[1]:10s} {row[2]}  [{row[3]}]")
n_pass = sum(1 for c in CH if c[1]); n_lb_fail = sum(1 for c in CH if (not c[1]) and c[2])
P(f"\n{n_pass}/{len(CH)} checks pass; load-bearing failures: {n_lb_fail}   {el()}")
OUT["verdict"] = dict(passed=n_pass, total=len(CH), load_bearing_failures=n_lb_fail)
with open(JSN, "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
sys.stdout.flush()
sys.exit(1 if n_lb_fail else 0)
