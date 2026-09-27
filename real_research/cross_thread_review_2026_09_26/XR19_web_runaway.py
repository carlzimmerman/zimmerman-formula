#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR19 (2/2) -- DOES THE DARK FLUID'S CONVERSION RUN AWAY THROUGH THE COSMIC WEB?  The web census, F_tot(z), percolation,
the reach, and what a web-wide conversion would cost.

WHY.  XR12 (K, an estimate: F_b(z = 2) -> 0.95 with a cone-enhanced smooth web) and XR16 (B3, a flag: the stimulated
criterion is met in filaments at z = 2 and at the mean density below z ~ 1.2-1.8) left the web open.  XR19_front_physics.py
settles the rules: against its LOCAL pump a daughter's relative velocity only shrinks in an expanding flow (no branching
there, one passage per seed); contracting flows have a zero-strain cone (spontaneous ignition far below the trigger,
calibrated by exact rays) and re-resonance; every accreting halo's infalling pump turns ~85% of its daughters into fast
seeds for the zone around it.  This script puts those rules on a realistic web and asks how much of the WHOLE dark fluid
converts, when, and at what price.  The dark fluid is FL1/FK1's order parameter (a classical field; quanta would be bosons
of m >~ 1.9-5.2e-19 eV); the dark MASS is still required.

THE MODEL (FK1/FP10's rates; nothing new is fitted)
  * The halo budget F_halo(z): XR16's own machinery (AT1's halo model, the fluid's depth, the m = 2e-19 eV cut, K = 60),
    exec'd from XR16's committed text; C1 reproduces XR16's committed history exactly, then the same code is run to z = 0
    and at every normalisation of the band (delta_t scaled; under MUTATE, ungated).
  * The web: a Gaussian field with the record's CLASS P(k) (L357's head, z = 0, Gaussian-smoothed at the cell R_s) on a
    periodic 128^3 grid (R_s = 0.5 Mpc/h; 1 Mpc/h and a second realisation as brackets).  Every Lagrangian cell carries its
    deformation eigenvalues lambda_i; at each epoch d_i = D(z) lambda_i.  Single-stream cells (d_1 < 1) take the
    Zel'dovich density 1/prod(1 - d_i) and strains e_i = H (1 - f d_i/(1 - d_i)); multistream cells (d_1 >= 1) take the
    CIC density and 1D dispersion of the Zel'dovich particles.  Classes: EX (all axes expanding), TA (turned around along
    axis 1, single stream: a zero-strain cone), MS (shell-crossed: kinetic regime).
  * The pump is the SMOOTH carrier: s = 1 - F_halo(z) of the cell density (the halo carrier is F_halo's); s = 1 bracketed.
  * Spontaneous ignition (E_need e-folds from the vacuum): EX along axis 1 with the one-passage sweep integral; TA on the
    cone, cal x C4 G^(3/2)/sqrt(alpha) (cal = XR19_front_physics Z1's min exact/local), Doppler-broadened by a pump
    roughness sigma_r when m v_k sigma_r > G; a compression cap 1/(1 - d_1) <= cap brackets the caustic's reliance; MS
    kinetic (FP10 A5's gamma = sqrt(pi) G^2/(m v_k sigma)), absolute over t_av when gamma W/v_k >= 1 (XR12 S1).
  * Seeded conversion (ln(pump/seed) = g_need e-folds): sources are the halo-hosting (MS) cells and every converted
    TA/MS cell (converging flow: XR19_front_physics B1/I1); an EX cell within the reach of a source converts if its
    passage gain (axis 1, or the isotropic mean strain) >= g_need; a TA/MS cell within reach if its gain >= g_need.  The
    front advances at most v_k dt per step (the causal limit) and the reach is R_beam cells.  Conversion is irreversible.
  * F_tot(z) = running max of F_halo + (1 - F_halo) f_web over z' >= z.
  * Consequences: L319's linear solver (exec'd via L357's head) with S(a) = 1 - F_esc, F_esc = XR16's bias-weighted
    escaped halo fraction + the web part (web daughters leave shallow structures); S8 against FP10 B6's gates (ratio >=
    0.922 strict, 0.899 alt; PAPER34's absolute floors 0.752/0.748); the carrier-sector T^2(k) at KiDS scales; a Limber
    estimate of the CMB lensing power; free streaming; the forest through XR16 B2's committed response range; X-COP.
A0 FOOTINGS.  a0 enters only through the flagship's bound on the normalisation (XR12 W2, committed): the band is
  delta_t0 = 5.31 zeta with zeta in [1.42 (forest), 2.54-2.76 (canonical flagship)] or [1.42, 4.09-4.29] (alt):
  delta_t0 = 7.54-14.6 (canonical, 9.36e-11) and 7.54-22.8 (alt, 1.13e-10).  F_tot is reported at both bands' edges.
PRE-DECLARED (written before this script's first run; informed by the scratch census prototype -- see HISTORY)
  H-W1 at the nominal cell (delta_t0 = 5.31) the smooth web converts: f_web(z = 0) >= 0.5 and f_web(z = 1) >= 0.3 in every
       O(1) bracket (s, sigma_r, cal, kinetic convention, t_av, g_need 1-10, reach 1-4, cap, iso, R_s, realisation), and
       the converted set percolates (largest cluster >= 90% of converted cells) for z <= 1.5.
  H-W2 the web conversion is late, held by the gate: f_web(z = 3) <= 0.1 in every bracket and every delta_t0 in [5.31, 25].
  H-W3 the voids resist: >= 70% of the cells left unconverted at z = 0 (nominal) are all-expanding (EX).
  H-F  F_tot(z = 0) >= 0.7 and F_tot(z = 1) >= 0.55 at both ends of both footings' bands (O(1) choices at nominal).
  H-X  the S8 ratio stays >= 0.899 (alt gate) at the nominal cell.
CHECKS (load-bearing unless marked)
  C1 CONTROL: XR16's committed F(z) history (20 budgets x 13 epochs) reproduced exactly by its own code.
  C2 CONTROL: L319's committed control cell (universal 5 Gyr, 600 km/s: S8 0.786542..., T^2(k=5, z=3) 0.468133...) exactly.
  C3 CONTROL: the grid's eigenvalue statistics: the T-web fractions at threshold 0 equal Doroshkevich's (0.080/0.420/
     0.420/0.080) within 0.01; the grid's rms linear overdensity within 5% of CLASS's sigma(R_s).
  G0 the mean background never converts spontaneously (gain < E_need at every z <= 10).
  W1 = H-W1.  W2 = H-W2.  W3 = H-W3.  F1 = H-F.  X1 = H-X.  Reported: B (the halo budget to z = 0 and across the band),
     the bracket table, P (percolation), R (the reach and generations), X2-X6 (T^2, CMB lensing, free streaming, forest,
     X-COP).
MUTATE=1: the vacuum gate removed (q = 0, a constant coupling), in the web census and in XR16's halo budget alike (C1 still
  reproduces XR16's committed, gated history).  G0 and W2 must FAIL: rc = 1.
SCOPE.  The web is Zel'dovich on a 64-128 Mpc/h box: exact for single streams, CIC-smoothed after shell crossing; no
  back-reaction of the conversion on structure growth; sub-cell halos enter only through F_halo and the smooth fraction s.
  The census is a sub-grid model with brackets, not a simulation: its job is to say whether a runaway happens and how
  robustly, and to give a particle-mesh run its sub-grid rule.  The consequences use linear theory (L319) and order-of-
  magnitude estimates where the record has no machinery.  Constants: none new; eps/m^2 (v_k) FITTED, lambda_0 and q
  DECLARED (FK1); kappa = 1/2 does not enter.
HISTORY (disclosed).  A scratch prototype of the census (not committed) came first: Zel'dovich cells without CIC, then with
  CIC multistream cells, time tracking, halo sources and caps; its numbers informed H-W1..H-X, which were written before
  this script's first run.  In the prototype the spontaneous TA ignition happened mostly near the caustic (median
  compression ~34x), which is why the compression cap and halo-seeded sources are brackets here.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR19_web_runaway.py
(~10-14 min, at most two threads, ~3 GB).  MUTATE=1 runs the gate-free control.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
os.environ["AT1_THREADS"] = "2"; os.environ["L357_THREADS"] = "2"
import sys, json, math, time, io, contextlib, warnings
import numpy as np
from scipy import ndimage
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import XR19_common as X

MUTATE = os.environ.get("MUTATE", "0") == "1"
SMOKE = os.environ.get("XR19_SMOKE", "0") == "1"             # reduced grid and brackets: a code test, never for the record
OUTDIR = os.environ.get("XR19_OUTDIR", HERE) if SMOKE else HERE
Q = 0.0 if MUTATE else X.Q_GATE
SLUG = "XR19_web_runaway"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR19", "part": "2/2 web runaway", "mutate": MUTATE, "checks": {}, "numbers": {}}
_trap = getattr(np, "trapezoid", None) or np.trapz


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name.split(" ")[0]] = {"ok": ok, "claim": name, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 118); P(t); P("=" * 118)
def el(): return f"[{time.time() - T0:.0f}s]"


P(__doc__.split("PRE-DECLARED")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the vacuum gate removed (q = 0) in the web census and the halo budget; G0 and W2 must FAIL ***")
if SMOKE: P("\n  *** XR19_SMOKE=1: 48^3 grids, a code test only; output not for the record ***")

# ============================================================================================ XR16's machinery (its committed text)
P16 = os.path.join(HERE, "XR16_fluid_conversion_surface.py")
_src16 = open(P16).read()
_MC = "# ================================================================================================ C1-C5 controls"
_MB = "# ================================================================================================ B the early conversion budget"
_MB2 = "# ------------------------------------------------------------------------------------------------ B2 the forest bound"
assert _src16.count(_MC) == 1 and _src16.count(_MB) == 1 and _src16.count(_MB2) == 1, "XR16 section markers changed"
_head16 = _src16.split(_MC)[0].replace('P(__doc__.split("CHECKS")[0].strip())', "pass")
_bpart = _MB + _src16.split(_MB)[1].split(_MB2)[0]
_ZB_LINE = "ZB = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0, 8.0, 10.0, 12.0, 15.0] if not SMOKE else [2.0, 3.0, 4.0, 6.0, 10.0]"
assert _bpart.count(_ZB_LINE) == 1
NS = {"__name__": "xr16", "__file__": P16}
_saved = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
with contextlib.redirect_stdout(io.StringIO()):
    exec(_head16, NS)
if _saved is None: os.environ.pop("MUTATE", None)
else: os.environ["MUTATE"] = _saved
assert NS["MUTATE"] is False
NS["at1"] = json.load(open(os.path.join(REPO, "real_research", "acceleration_trigger_2026", "AT1_acceleration_trigger_highz_results.json")))
NS["check"] = lambda *a, **k: True
L57 = NS["A"]["L57"]
G19, LC, S8_LCDM, K_H, T2f, S8_of = L57["G19"], L57["LC"], L57["S8_LCDM"], L57["K_H"], L57["T2f"], L57["S8_of"]
KH57, P057 = L57["KH"], L57["P0"]
_delta_t16 = NS["delta_t"]
P(f"  XR16's head loaded (AT1's machinery, L357's head, L319's solver, CLASS P(k) to {KH57[-1]:.0f} h/Mpc)   {el()}")


def budget(zb, dt_scale=1.0, gated=True):
    """XR16's Part B, exec'd from its committed text, on the epochs zb, with its delta_t(z) scaled (the band) or ungated."""
    if gated:
        NS["delta_t"] = lambda z, s=dt_scale: s * _delta_t16(z)
    else:
        NS["delta_t"] = lambda z, s=dt_scale: s * _delta_t16(z) / NS["Ez2"](z) ** 1.75       # E^4 -> E^(1/2): q = 0
    src = _bpart.replace(_ZB_LINE, "ZB = " + repr([float(x_) for x_ in zb]))
    with contextlib.redirect_stdout(io.StringIO()):
        exec(src, NS)
    NS["delta_t"] = _delta_t16
    return {k_: dict(v_) for k_, v_ in NS["HIST"].items()}


# ============================================================================================ C1 XR16 reproduced
banner("C1  CONTROL: XR16's committed F(z) budget reproduced by its own code (20 budgets x 13 epochs)")
H16 = budget([2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0, 8.0, 10.0, 12.0, 15.0])
ref16 = json.load(open(os.path.join(HERE, "XR16_fluid_conversion_surface_results.json")))["numbers"]["B"]["history"]
dev16, n16 = 0.0, 0
for key, d_ in H16.items():
    for z_, (F_, Fb_) in d_.items():
        r_ = ref16[f"{key[0]}|{key[1]}"][str(z_)]
        dev16 = max(dev16, abs(F_ - r_[0]), abs(Fb_ - r_[1])); n16 += 1
P(f"    {n16} rows; fiducial (m = 2e-19 eV, K = 60) F(4/3/2) = " + "/".join(f"{H16[('fluid m = 2e-19 eV', 60.0)][z_][0]:.3f}" for z_ in (4.0, 3.0, 2.0))
  + f"; max |dev| {dev16:.1e}   {el()}")
OUT["numbers"]["C1"] = dict(rows=n16, max_dev=dev16)
check("C1 CONTROL: XR16's committed F(z) history reproduced exactly by its own Part B (exec'd from its committed text)",
      f"{n16} rows, max |dev| {dev16:.1e}", n16 == 260 and dev16 == 0.0)

# ============================================================================================ C2 L319 reproduced
banner("C2  CONTROL: L319's committed control cell through the loaded solver")
U5 = G19["run"](G19["surv_universal"](5.0), 600.0)
s8u = float(S8_of(T2f(U5, LC, 0.0))); t2u = float(T2f(U5, LC, 3.0)[G19["k5"]])
ref19 = json.load(open(os.path.join(REPO, "real_research", "dark_sector_2026", "L319_lambda_triggered_kicked_decay_results.json")))["numbers"]["control_universal_5Gyr_600"]
P(f"    S8 {s8u!r} (committed {ref19['S8']!r}); T^2(k=5, z=3) {t2u!r} (committed {ref19['T2_k5_z3']!r}); LCDM S8 {S8_LCDM:.4f}   {el()}")
OUT["numbers"]["C2"] = dict(S8=s8u, T2=t2u, S8_LCDM=S8_LCDM)
check("C2 CONTROL: L319's committed universal-decay cell (5 Gyr, 600 km/s) reproduced exactly", f"dS8 {s8u - ref19['S8']:.1e}, "
      f"dT2 {t2u - ref19['T2_k5_z3']:.1e}", s8u == ref19["S8"] and t2u == ref19["T2_k5_z3"])

# ============================================================================================ B the halo budget to z = 0, across the band
banner("B   (reported) THE HALO BUDGET TO z = 0 (XR16's machinery), at every normalisation of the band" + (" -- UNGATED (MUTATE)" if MUTATE else ""))
ZB_EXT = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0, 8.0, 10.0, 12.0, 15.0]
DT0S = {"nominal 5.31": X.DT0_LIN, "forest floor 7.54": 1.42 * X.DT0_LIN, "canonical top 13.5": 2.54 * X.DT0_LIN,
        "canonical top+up 14.6": 2.755 * X.DT0_LIN, "alt top 21.7": 4.09 * X.DT0_LIN, "alt top+up 22.8": 4.29 * X.DT0_LIN, "FK1 upper 25": 25.0}
DT0_16 = float(_delta_t16(0.0))                                                   # XR16's delta_t at z = 0 (5.3100)
FH = {}
for lab, dt0 in DT0S.items():
    hh = budget(ZB_EXT, dt_scale=dt0 / DT0_16, gated=not MUTATE)
    FH[lab] = {z_: v_ for z_, v_ in hh[("fluid m = 2e-19 eV", 60.0)].items()}
    P(f"    {lab:22s}: F_halo(z = 4/3/2/1/0.5/0) = " + "/".join(f"{FH[lab][z_][0]:.3f}" for z_ in (4.0, 3.0, 2.0, 1.0, 0.5, 0.0))
      + "; F_b,esc = " + "/".join(f"{FH[lab][z_][1]:.3f}" for z_ in (4.0, 3.0, 2.0, 1.0, 0.5, 0.0)) + f"   {el()}")
OUT["numbers"]["B"] = {lab: {str(z_): v_ for z_, v_ in d_.items()} for lab, d_ in FH.items()}


def Fhalo_of(lab):
    zz = np.array(sorted(FH[lab])); FF = np.array([FH[lab][z_][0] for z_ in zz]); Fb = np.array([FH[lab][z_][1] for z_ in zz])
    return (lambda z: float(np.interp(z, zz, FF))), (lambda z: float(np.interp(z, zz, Fb)))


# ============================================================================================ G0 the mean background
banner("G0  THE MEAN BACKGROUND: spontaneous gain against E_need" + (" (UNGATED)" if MUTATE else ""))
zb = np.linspace(0, 10, 2001)
ratio = np.array([(1.0 / float(X.rho_t_over_mean(z, X.DT0_LIN, Q))) ** 2 for z in zb])
over = zb[ratio >= 1.0]
P(f"    max spontaneous exponent / E_need at the mean density: {ratio.max():.4f} at z = {zb[ratio.argmax()]:.2f}"
  + (f"; >= 1 (the whole background self-ignites) for z >= {over.min():.2f}" if len(over) else ""))
OUT["numbers"]["G0"] = dict(max_ratio=float(ratio.max()), z_at_max=float(zb[ratio.argmax()]), z_ignite=float(over.min()) if len(over) else None)
check("G0 the mean background never converts spontaneously (its exponent stays below E_need at every z <= 10)",
      f"max {ratio.max():.4f} E_need at z = {zb[ratio.argmax()]:.2f}", ratio.max() < 1.0,
      "the gate's job (FK1 N2); everything the web converts below is structure or seeds")

# ============================================================================================ the web
banner("W   THE WEB CENSUS: a Zel'dovich web on the record's CLASS P(k), time-tracked, seeded, percolation")
Z1J = os.path.join(HERE, "XR19_front_physics_results.json")
CAL = 0.697
if os.path.exists(Z1J):
    _z = json.load(open(Z1J))["numbers"].get("Z", {})
    if _z: CAL = min(v_["ratio"] for v_ in _z.values())
P(f"    cone calibration cal = {CAL:.3f} (XR19_front_physics Z1's min exact/local)")
ZS = [6.0, 5.0, 4.0, 3.5, 3.0, 2.75, 2.5, 2.25, 2.0, 1.75, 1.5, 1.25, 1.0, 0.75, 0.5, 0.25, 0.0]
KM_MPC = 3.0857e19
h = 0.6736


class Web:
    def __init__(self, NG, L, seed):
        self.NG, self.L, self.Rs = NG, L, L / NG
        rng = np.random.default_rng(seed)
        kx = 2 * np.pi * np.fft.fftfreq(NG, d=self.Rs); kz = 2 * np.pi * np.fft.rfftfreq(NG, d=self.Rs)
        KX, KY, KZ = np.meshgrid(kx, kx, kz, indexing="ij"); K2 = KX ** 2 + KY ** 2 + KZ ** 2
        Pg = np.interp(np.sqrt(K2), KH57, P057, left=0, right=0) * np.exp(-K2 * self.Rs ** 2)
        dk = np.fft.rfftn(rng.normal(size=(NG, NG, NG))) * np.sqrt(Pg * NG ** 3 / L ** 3); dk[0, 0, 0] = 0
        K2s = K2.copy(); K2s[0, 0, 0] = 1.0
        self.psi = np.stack([np.fft.irfftn(1j * a / K2s * dk, s=(NG, NG, NG)).astype(np.float32).ravel() for a in (KX, KY, KZ)], -1)
        Tm = np.empty((NG ** 3, 3, 3), np.float64)
        for i, a in enumerate((KX, KY, KZ)):
            for j, b in enumerate((KX, KY, KZ)):
                if j < i: continue
                c = np.fft.irfftn(a * b / K2s * dk, s=(NG, NG, NG)).ravel()
                Tm[:, i, j] = c; Tm[:, j, i] = c
        self.lam = np.linalg.eigvalsh(Tm)[:, ::-1].astype(np.float32); del Tm
        self.sigma = float(np.std(self.lam.sum(1)))
        kk = np.geomspace(1e-4, KH57[-1], 20000)
        self.sigma_class = float(np.sqrt(_trap(kk ** 2 * np.interp(kk, KH57, P057) * np.exp(-kk ** 2 * self.Rs ** 2), kk) / (2 * np.pi ** 2)))
        q = np.stack(np.meshgrid(*(np.arange(NG) * self.Rs,) * 3, indexing="ij"), -1).reshape(-1, 3).astype(np.float32)
        self.st = {}
        for z in ZS:
            D, f = X.Dz(z), X.fz(z); a = 1 / (1 + z); Hk = 100.0 * float(X.E(z))
            pos = (q - D * self.psi) % L
            vel = -(a * Hk * f * D) * self.psi
            (m, px, py, pz, v2), i0, fr = self._cic(pos, [np.ones(NG ** 3), vel[:, 0], vel[:, 1], vel[:, 2], (vel.astype(np.float64) ** 2).sum(1)])
            mm = np.maximum(m, 1e-12)
            s2 = np.maximum(v2 / mm - (px ** 2 + py ** 2 + pz ** 2) / mm ** 2, 0.0) / 3
            self.st[z] = dict(rhoE=self._interp(m, i0, fr).astype(np.float32), sigE=np.sqrt(self._interp(s2, i0, fr)).astype(np.float32))
        del q

    def _cic(self, pos, wl):
        NG = self.NG; g = pos / self.Rs
        i0 = np.floor(g).astype(np.int64); fr = (g - i0).astype(np.float64)
        outs = [np.zeros(NG ** 3) for _ in wl]
        for dx in (0, 1):
            wx = fr[:, 0] if dx else 1 - fr[:, 0]
            for dy in (0, 1):
                wy = fr[:, 1] if dy else 1 - fr[:, 1]
                for dz in (0, 1):
                    wz = fr[:, 2] if dz else 1 - fr[:, 2]
                    idx = (((i0[:, 0] + dx) % NG) * NG + (i0[:, 1] + dy) % NG) * NG + (i0[:, 2] + dz) % NG
                    w = wx * wy * wz
                    for o, wt in zip(outs, wl): o += np.bincount(idx, weights=w * wt, minlength=NG ** 3)
        return outs, i0, fr

    def _interp(self, grid, i0, fr):
        NG = self.NG; out = np.zeros(i0.shape[0])
        for dx in (0, 1):
            wx = fr[:, 0] if dx else 1 - fr[:, 0]
            for dy in (0, 1):
                wy = fr[:, 1] if dy else 1 - fr[:, 1]
                for dz in (0, 1):
                    wz = fr[:, 2] if dz else 1 - fr[:, 2]
                    idx = (((i0[:, 0] + dx) % NG) * NG + (i0[:, 1] + dy) % NG) * NG + (i0[:, 2] + dz) % NG
                    out += wx * wy * wz * grid[idx]
        return out

    def run(self, dt0=X.DT0_LIN, fh_lab="nominal 5.31", m_ev=2e-19, En=None, vk=600.0, s_mode="1-F", sig_r=10.0, cal=None, kconv=1.0,
            t_av=1.0, g_need=3.0, reach=2, cap=np.inf, iso=False, halo_src=True, seeded=True, q=Q, label_z=(3.0, 2.0, 1.5, 1.0, 0.5, 0.0)):
        En = X.ENEED["2e-19"] if En is None else En
        cal = CAL if cal is None else cal
        Fh, _ = Fhalo_of(fh_lab)
        NG, N = self.NG, self.NG ** 3
        conv = np.zeros(N, bool); first = np.full(N, -1.0, np.float32); cls_first = np.zeros(N, np.int8)
        hist = {}; dl = X.delta_split(m_ev, vk)
        for iz, z in enumerate(ZS):
            st = self.st[z]; D, f = X.Dz(z), X.fz(z); H = float(X.H_si(z)); om = float(X.OMz(z))
            d = (D * self.lam).astype(np.float64); dmin = np.minimum(d, 1 - 1e-7)
            ss = d[:, 0] < 1
            rho = np.where(ss, 1.0 / np.prod(1 - dmin, axis=1), st["rhoE"])
            s = 1.0 if s_mode == "1" else 1.0 - Fh(z)
            rr = s * rho / float(X.rho_t_over_mean(z, dt0, q))
            G = float(X.G_t(z, m_ev, vk, En)) * rr
            e, ed = X.zeldovich_strain(dmin, z)
            ta = ss & (e[:, 0] < 0); ex = ss & ~ta; ms = ~ss
            # EX: axis 1 (or the isotropic mean strain), first + second order
            if iso:
                en_, edn_ = e.mean(1), ed.mean(1)
            else:
                en_, edn_ = e[:, 0], ed[:, 0]
            g_ex = X.sweep_gain(G, 2 * dl * np.abs(en_) * H, dl * H * H * (2 * en_ ** 2 - edn_))
            # TA: the cone between axis 1 and axes 2/3 (the smaller alpha), coherent or Doppler-broadened by sigma_r
            best = np.full(N, np.inf)
            for j in (1, 2):
                ok = ta & (e[:, j] > 0)
                ca = np.where(ok, X.cone_alpha_hat(np.minimum(e[:, 0], -1e-12), np.maximum(e[:, j], 1e-12), ed[:, 0], ed[:, j]), np.inf)
                best = np.where(ok & (ca > 0), np.minimum(best, ca), best)
            alpha = dl * H * H * best
            g_cone = cal * X.C4 * G ** 1.5 / np.sqrt(alpha)
            if sig_r > 0:
                Dl = 2 * dl * sig_r / vk
                g_cone = np.where(Dl > G, cal * kconv * X.cone_gain_kinetic(G, alpha, m_ev, vk, sig_r), g_cone)
            capok = (1.0 / (1 - dmin[:, 0])) <= cap
            g_ta_seed = X.sweep_gain(G, 2 * dl * np.abs(e[:, 0]) * H, dl * H * H * (2 * e[:, 0] ** 2 - ed[:, 0]))
            # MS: kinetic
            sig = np.maximum(st["sigE"].astype(np.float64), 1.0)
            gam = kconv * X.kinetic_rate(G, m_ev, vk, sig)
            W_km = (1 / (1 + z)) * self.Rs / h * KM_MPC
            g_ms = np.where(gam * W_km / vk >= 1, (gam - vk / W_km) * t_av / H, gam * W_km / vk)
            sp_ = (ex & (g_ex >= En)) | (ta & capok & (g_cone >= En)) | (ms & (g_ms >= En))
            newsp = sp_ & ~conv
            first[newsp] = z; cls_first[newsp & ex] = 1; cls_first[newsp & ta] = 2; cls_first[newsp & ms] = 3
            conv |= sp_
            if seeded:
                # the causal limit: generations this step = (v_k dt, comoving, in cells) / reach
                if iz > 0:
                    dt_s = (X.t_of_z(z) - X.t_of_z(ZS[iz - 1])) * X.TU
                    adv = vk * dt_s / KM_MPC * (1 + 0.5 * (z + ZS[iz - 1])) * h / self.Rs
                else:
                    adv = reach
                ngen = int(max(1, min(8, math.floor(adv / reach))))
                rad = min(reach, max(adv, 1.0))
                elig = (ex & (g_ex >= g_need)) | (ta & (g_ta_seed >= g_need)) | (ms & (g_ms >= g_need))
                for _ in range(ngen):
                    src = (conv & (ta | ms)) | (ms if halo_src else np.zeros(N, bool))
                    if not src.any(): break
                    pad = int(math.ceil(rad)) + 1
                    dist = ndimage.distance_transform_edt(~np.pad(src.reshape(NG, NG, NG), pad, mode="wrap"))
                    dist = dist[pad:-pad, pad:-pad, pad:-pad].ravel()
                    new = ~conv & elig & (dist <= rad)
                    if not new.any(): break
                    first[new] = z; cls_first[new & ex] = 4; cls_first[new & ta] = 5; cls_first[new & ms] = 6
                    conv |= new
            row = dict(f=float(conv.mean()), ex=float(ex.mean()), ta=float(ta.mean()), ms=float(ms.mean()),
                       ex_conv=float((conv & ex).sum() / max(ex.sum(), 1)))
            if z in label_z:
                lab, nlab = ndimage.label(conv.reshape(NG, NG, NG))
                if nlab:
                    sizes = np.bincount(lab.ravel())[1:]; big = int(sizes.argmax()) + 1
                    bl = (lab == big)
                    span = all(bl.any(axis=tuple(a_ for a_ in range(3) if a_ != ax_))[0] and bl.any(axis=tuple(a_ for a_ in range(3) if a_ != ax_))[-1] for ax_ in range(3))
                    row.update(largest_of_conv=float(sizes.max() / conv.sum()), largest_of_all=float(sizes.max() / N), spans=bool(span))
                else:
                    row.update(largest_of_conv=0.0, largest_of_all=0.0, spans=False)
            hist[z] = row
        unconv = ~conv
        z0 = ZS[-1]
        d0 = (X.Dz(z0) * self.lam).astype(np.float64); e0, _ = X.zeldovich_strain(np.minimum(d0, 1 - 1e-7), z0)
        ex0 = (d0[:, 0] < 1) & (e0[:, 0] >= 0)
        hist["unconv_ex_share"] = float((unconv & ex0).sum() / max(unconv.sum(), 1))
        hist["by_channel"] = {nm: float((cls_first == c_).mean()) for c_, nm in ((1, "spont EX"), (2, "spont TA"), (3, "spont MS"), (4, "seeded EX"), (5, "seeded TA"), (6, "seeded MS"))}
        return hist


def F_tot_of(hist, fh_lab):
    Fh, _ = Fhalo_of(fh_lab)
    zs = [z for z in ZS]
    raw = [Fh(z) + (1 - Fh(z)) * hist[z]["f"] for z in zs]
    out, runmax = {}, 0.0
    for z, v in zip(zs, raw):                                              # ZS runs from high z to low z
        runmax = max(runmax, v); out[z] = runmax
    return out


NGW = 48 if SMOKE else 128
W64 = Web(NGW, 64.0 * NGW / 128, 19)
P(f"    grid {NGW}^3, L = {64.0 * NGW / 128:g} Mpc/h (R_s = 0.5): sigma(delta_lin) = {W64.sigma:.3f} (CLASS {W64.sigma_class:.3f}); Zel'dovich states at {len(ZS)} epochs   {el()}")
tweb = np.bincount((W64.lam > 0).sum(1), minlength=4) / W64.lam.shape[0]
DORO = np.array([0.0798, 0.4202, 0.4202, 0.0798])
OUT["numbers"]["C3"] = dict(tweb=tweb.tolist(), sigma_grid=W64.sigma, sigma_class=W64.sigma_class)
check("C3 CONTROL: the grid's deformation eigenvalues: T-web fractions at threshold 0 (void/sheet/filament/knot) equal "
      "Doroshkevich's Gaussian-field values within 0.01, and the rms linear overdensity is within 5% of CLASS's sigma(R_s)",
      f"T-web {np.round(tweb, 4).tolist()} vs {DORO.tolist()}; sigma {W64.sigma:.3f} vs {W64.sigma_class:.3f}",
      np.max(np.abs(tweb - DORO)) <= 0.01 and abs(W64.sigma / W64.sigma_class - 1) <= 0.05)

RUNS = {}


def do(name, web=None, **kw):
    t1 = time.time()
    web = W64 if web is None else web
    hh = web.run(**kw)
    RUNS[name] = dict(kw={k_: (v_ if not isinstance(v_, float) or math.isfinite(v_) else "inf") for k_, v_ in kw.items()}, hist=hh)
    P(f"    {name:34s}: f_web(z=3/2/1.5/1/0.5/0) = " + "/".join(f"{hh[z]['f']:.3f}" for z in (3.0, 2.0, 1.5, 1.0, 0.5, 0.0))
      + f"; largest cluster/converted (z=1.5/1/0) " + "/".join(f"{hh[z].get('largest_of_conv', float('nan')):.2f}" for z in (1.5, 1.0, 0.0))
      + f"; unconverted EX share {hh['unconv_ex_share']:.2f}   [{time.time() - t1:.0f}s]")
    return hh


P("  the nominal cell (delta_t0 = 5.31, m = 2e-19 eV, v_k 600, s = 1 - F_halo, sigma_r 10, cal, g_need 3, reach 2 cells) and its O(1) brackets:")
nom = do("nominal")
do("no seeding", seeded=False)
do("no halo sources", halo_src=False)
do("pump s = 1", s_mode="1")
do("sigma_r 0 (coherent)", sig_r=0.0)
do("sigma_r 30", sig_r=30.0)
do("cal 0.2", cal=0.2)
do("cap 10", cap=10.0)
do("cap 3", cap=3.0)
do("kinetic x1/2", kconv=0.5)
do("t_av 0.3/H", t_av=0.3)
do("g_need 1", g_need=1.0)
do("g_need 10", g_need=10.0)
do("reach 1", reach=1)
do("reach 4", reach=4)
do("iso strain", iso=True)
do("v_k 575", vk=575.0)
do("v_k 650", vk=650.0)
do("m 1e-17 (E_need 162)", m_ev=1e-17, En=X.ENEED["1e-17"])
do("m 1e-6 (E_need 61)", m_ev=1e-6, En=X.ENEED["1e-06"])
cons = dict(cap=3.0, iso=True, g_need=10.0, kconv=0.5, t_av=0.3, sig_r=30.0, cal=0.2, reach=1)
do("most conservative", **cons)
W64b = Web(NGW, 64.0 * NGW / 128, 7)
do("realisation 2", web=W64b)
do("realisation 2, most conservative", web=W64b, **cons)
del W64b
W128 = Web(NGW, 128.0 * NGW / 128, 19)
P(f"    grid {NGW}^3, L = {128.0 * NGW / 128:g} Mpc/h (R_s = 1.0): sigma = {W128.sigma:.3f} (CLASS {W128.sigma_class:.3f})   {el()}")
do("R_s 1 Mpc/h", web=W128)
do("R_s 1 Mpc/h, most conservative", web=W128, **cons)
del W128
P("  the normalisation band (O(1) choices at nominal, and most conservative):")
for lab, dt0 in DT0S.items():
    if lab == "nominal 5.31": continue
    do(f"dt0 {lab}", dt0=dt0, fh_lab=lab)
    do(f"dt0 {lab}, most conservative", dt0=dt0, fh_lab=lab, **cons)

OUT["numbers"]["runs"] = {k_: dict(kw=v_["kw"], hist={str(z): r_ for z, r_ in v_["hist"].items()}) for k_, v_ in RUNS.items()}

# W1 / W2 / W3
nominal_brackets = [k_ for k_ in RUNS if not k_.startswith("dt0 ")]
fw0 = {k_: RUNS[k_]["hist"][0.0]["f"] for k_ in nominal_brackets}
fw1 = {k_: RUNS[k_]["hist"][1.0]["f"] for k_ in nominal_brackets}
perc = {k_: min(RUNS[k_]["hist"][z].get("largest_of_conv", 0.0) for z in (1.5, 1.0, 0.5, 0.0)) for k_ in nominal_brackets}
check("W1 = H-W1: at the nominal cell the smooth web converts -- f_web(z = 0) >= 0.5 and f_web(z = 1) >= 0.3 in every O(1) "
      "bracket, and the converted set percolates (largest cluster >= 90% of the converted cells) at every z <= 1.5",
      f"f_web(0) {min(fw0.values()):.3f}-{max(fw0.values()):.3f} (min: {min(fw0, key=fw0.get)}); f_web(1) {min(fw1.values()):.3f}-"
      f"{max(fw1.values()):.3f} (min: {min(fw1, key=fw1.get)}); largest cluster >= {min(perc.values()):.2f} (min: {min(perc, key=perc.get)})",
      min(fw0.values()) >= 0.5 and min(fw1.values()) >= 0.3 and min(perc.values()) >= 0.9,
      "the halos' own daughters seed the multistream and turned-around web around them, and turned-around cells ignite on "
      "their own; the converted set is one connected web")
fw3 = {k_: v_["hist"][3.0]["f"] for k_, v_ in RUNS.items()}
check("W2 = H-W2: the web conversion is late, held by the gate -- f_web(z = 3) <= 0.1 in every bracket and at every "
      "normalisation 5.31-25", f"max f_web(3) {max(fw3.values()):.3f} ({max(fw3, key=fw3.get)})", max(fw3.values()) <= 0.1,
      "the gated threshold rho_t/rho_bar = delta_t0 E^4/(1+z)^3 is 36 at z = 3 and 68 at z = 4 (nominal): the web's pump "
      "density is far below it, and the per-passage gain scales as (rho/rho_t)^2")
check("W3 = H-W3: the voids resist -- >= 70% of the cells left unconverted at z = 0 (nominal) are all-expanding (EX)",
      f"unconverted EX share {nom['unconv_ex_share']:.3f}; converted EX fraction at z = 0 {nom[0.0]['ex_conv']:.3f}",
      nom["unconv_ex_share"] >= 0.7, "no re-resonance in expanding flow (XR19_front_physics H1), and the void pump's gain per passage "
      "is below a few e-folds")
P(f"    channels (nominal, fraction of all cells by first conversion): " + ", ".join(f"{k_} {v_:.3f}" for k_, v_ in nom["by_channel"].items()))
OUT["numbers"]["nominal_channels"] = nom["by_channel"]

# ============================================================================================ F F_tot(z), both footings
banner("F   F_tot(z): the halo budget plus the smooth web, running maximum; the band on both footings")
FT = {}
for k_, v_ in RUNS.items():
    lab = v_["kw"].get("fh_lab", "nominal 5.31")
    FT[k_] = F_tot_of(v_["hist"], lab)
for k_ in ("nominal", "most conservative", "pump s = 1", "no seeding") + tuple(k_ for k_ in RUNS if k_.startswith("dt0 ")):
    Fh, _ = Fhalo_of(RUNS[k_]["kw"].get("fh_lab", "nominal 5.31"))
    P(f"    {k_:42s}: F_tot(z=3/2/1.5/1/0.5/0) = " + "/".join(f"{FT[k_][z]:.3f}" for z in (3.0, 2.0, 1.5, 1.0, 0.5, 0.0))
      + "   (halo only " + "/".join(f"{Fh(z):.3f}" for z in (3.0, 2.0, 1.5, 1.0, 0.5, 0.0)) + ")")
OUT["numbers"]["F_tot"] = {k_: {str(z): v for z, v in d_.items()} for k_, d_ in FT.items()}
FOOTB = {"canonical (a0 = 9.3603e-11)": ("dt0 forest floor 7.54", "dt0 canonical top+up 14.6"),
         "alt (a0 = 1.1312e-10)": ("dt0 forest floor 7.54", "dt0 alt top+up 22.8")}
band = {}
for foot, (lo, hi) in FOOTB.items():
    band[foot] = {edge: dict(F0=FT[edge][0.0], F1=FT[edge][1.0], F2=FT[edge][2.0], F0_cons=FT[edge + ", most conservative"][0.0],
                             F1_cons=FT[edge + ", most conservative"][1.0]) for edge in (lo, hi)}
    P(f"    {foot}: band edges " + "; ".join(f"{e_}: F_tot(0/1/2) = {d_['F0']:.3f}/{d_['F1']:.3f}/{d_['F2']:.3f} (most conservative "
                                             f"{d_['F0_cons']:.3f}/{d_['F1_cons']:.3f})" for e_, d_ in band[foot].items()))
OUT["numbers"]["band"] = band
f0min = min(d_["F0"] for b_ in band.values() for d_ in b_.values()); f1min = min(d_["F1"] for b_ in band.values() for d_ in b_.values())
check("F1 = H-F: F_tot(z = 0) >= 0.7 and F_tot(z = 1) >= 0.55 at both ends of both footings' bands (O(1) choices at nominal)",
      f"min F_tot(0) {f0min:.3f}, min F_tot(1) {f1min:.3f} over the four band edges", f0min >= 0.7 and f1min >= 0.55,
      "a0 moves only the band's upper edge (the flagship bound); the runaway's size is set by delta_t0 and z")

# ============================================================================================ R the reach
banner("R   (reported) THE REACH: comoving advance per step (v_k dt) against the cell and the resonance reach")
RR = {}
for iz in range(1, len(ZS)):
    z, zp = ZS[iz], ZS[iz - 1]
    dt_s = (X.t_of_z(z) - X.t_of_z(zp)) * X.TU
    adv = 600.0 * dt_s / KM_MPC * (1 + 0.5 * (z + zp)) * h
    RR[z] = adv
P("    comoving advance of a daughter per step (Mpc/h): " + ", ".join(f"z {zp:g}->{z:g}: {RR[z]:.2f}" for z, zp in zip(ZS[1:], ZS[:-1]) if z in (3.0, 2.0, 1.0, 0.5, 0.0)))
OUT["numbers"]["R"] = {str(k_): v_ for k_, v_ in RR.items()}

# ============================================================================================ X consequences
banner("X   CONSEQUENCES: L319's linear solver with the converted history; free streaming; CMB lensing; forest; X-COP")
a_grid = G19["a_grid"]; zgrid = 1 / a_grid - 1


def S_of(Fesc_z):
    return np.clip(1.0 - np.interp(zgrid, Fesc_z[0], Fesc_z[1], right=0.0), 0.0, 1.0)


def Fesc_hist(runkey):
    lab = RUNS[runkey]["kw"].get("fh_lab", "nominal 5.31")
    Fh, Fb = Fhalo_of(lab)
    zs = np.array(ZS[::-1])
    fe = np.array([min(1.0, Fb(z) + (FT[runkey][z] - Fh(z))) for z in zs])
    fe = np.maximum.accumulate(fe[::-1])[::-1]                              # irreversible in time (monotone from high z to low)
    zz = np.concatenate([zs, [8.0, 10.0, 15.0]]); ff = np.concatenate([fe, [Fb(8.0), Fb(10.0), Fb(15.0)]])
    o = np.argsort(zz)
    return zz[o], ff[o]


XR = {}
kk_ = G19["K_H"]
for key in ("halo only (nominal)", "nominal", "most conservative", "pump s = 1", "dt0 canonical top+up 14.6", "dt0 alt top+up 22.8", "dt0 FK1 upper 25"):
    if key == "halo only (nominal)":
        Fh, Fb = Fhalo_of("nominal 5.31")
        zs = np.array(sorted(FH["nominal 5.31"])); fe = np.array([Fb(z) for z in zs])
        Fz = (zs, fe)
    else:
        Fz = Fesc_hist(key)
    S = S_of(Fz)
    R_ = G19["run"](S, 600.0)
    s8 = float(S8_of(T2f(R_, LC, 0.0)))
    T2 = {z: T2f(R_, LC, z) for z in (0.0, 0.5, 1.0, 2.0, 3.0)}
    t2k = {z: {kq: float(np.interp(math.log(kq), np.log(kk_), T2[z])) for kq in (0.1, 0.3, 1.0, 3.0, 5.0)} for z in T2}
    # CMB lensing (Limber, flat LCDM distances): C_L ratio = int W^2/chi^2 P T^2 / int W^2/chi^2 P
    zz = np.linspace(0.01, 10.0, 600); chi = np.array([_trap(1 / X.E(np.linspace(0, zq, 400)), np.linspace(0, zq, 400)) for zq in zz]) * 2997.92458
    chis = _trap(1 / X.E(np.linspace(0, 1089, 20000)), np.linspace(0, 1089, 20000)) * 2997.92458
    Wk = (chi * (chis - chi) / chis) ** 2 * (1 + zz) ** 2 / chi ** 2
    jz = [int(np.argmin(np.abs(a_grid - 1 / (1 + zq)))) for zq in zz]
    Dg = np.array([L57["DG"](float(zq)) for zq in zz]) if "DG" in L57 else np.ones_like(zz)
    cl = {}
    for Lq in (100.0, 300.0, 1000.0):
        kq = (Lq + 0.5) / chi                                                # h/Mpc (chi in Mpc/h)
        Pz = np.interp(kq, KH57, P057) * Dg ** 2
        T2z = np.array([np.interp(math.log(min(max(kq[i], kk_[0]), kk_[-1])), np.log(kk_), R_[:, jz[i]] ** 2 / LC[:, jz[i]] ** 2) for i in range(len(zz))])
        cl[Lq] = float(_trap(Wk * Pz * T2z, chi) / _trap(Wk * Pz, chi))
    XR[key] = dict(S8=s8, S8_ratio=s8 / S8_LCDM, T2=t2k, CMBlens=cl, Fesc0=float(Fz[1][np.argmin(np.abs(Fz[0]))]))
    P(f"    {key:28s}: F_esc(0) {XR[key]['Fesc0']:.3f}; S8 {s8:.4f} (ratio {s8 / S8_LCDM:.3f}); carrier-sector T^2(k = 0.3/1/3 h/Mpc) at z = 0.5: "
      + "/".join(f"{t2k[0.5][kq]:.3f}" for kq in (0.3, 1.0, 3.0)) + f"; C_L^phiphi ratio L = 100/300/1000: " + "/".join(f"{cl[Lq]:.3f}" for Lq in cl) + f"   {el()}")
OUT["numbers"]["X"] = XR
# FP10 A8's maximal bracket, the same way (everything converts at z_web): a cross-check of the pipeline
MAXB = {}
Fh, Fb = Fhalo_of("nominal 5.31")
for zw in (1.8, 1.2, 0.5):
    zs = np.array(sorted(FH["nominal 5.31"])); fe = np.array([1.0 if z <= zw else Fb(z) for z in zs])
    R_ = G19["run"](S_of((zs, fe)), 600.0)
    MAXB[zw] = float(S8_of(T2f(R_, LC, 0.0)) / S8_LCDM)
fp10w = json.load(open(os.path.join(REPO, "real_research", "derivation_chain_2026", "FP10_internal_splitting_dark_sector_results.json")))["numbers"]["A8"]["S8_web"]
P("    FP10 A8's maximal web bracket (the whole carrier converts at z_web), this pipeline vs FP10's committed: "
  + ", ".join(f"z_web {zw}: {v:.3f} (FP10 {fp10w[str(zw)]:.3f})" for zw, v in MAXB.items()))
OUT["numbers"]["X_maxbracket"] = dict(mine=MAXB, fp10=fp10w)
check("X1 = H-X: the S8 ratio at the nominal cell stays >= 0.899 (FP10 B6's alt gate)", f"{XR['nominal']['S8_ratio']:.4f} (strict gate "
      f"0.922: {'pass' if XR['nominal']['S8_ratio'] >= 0.922 else 'FAIL'}; absolute S8 {XR['nominal']['S8']:.3f} vs PAPER34's floors 0.752/0.748)",
      XR["nominal"]["S8_ratio"] >= 0.899, "S8 weighs k ~ 0.1-0.3 h/Mpc; the daughters' free-streaming scale is near it, so S8 "
      "moves by percents while the small-scale carrier power collapses", load_bearing=True)
# X2 free streaming
FS = {}
for zc in (2.0, 1.0, 0.5):
    v0 = 600.0 / (1 + zc)
    kfs = math.sqrt(1.5 * X.OM) * 100.0 / v0                                  # h/Mpc, today
    aa = np.linspace(1 / (1 + zc), 1.0, 4001)
    chi = float(_trap(600.0 / (1 + zc) / (aa ** 3 * 100.0 * X.E(1 / aa - 1)), aa))  # comoving Mpc/h
    FS[zc] = dict(v_today=v0, k_fs_today=kfs, lambda_fs=2 * math.pi / kfs, chi_to_today=chi)
P("    free streaming of the web daughters: " + "; ".join(f"converted at z = {zc}: {d_['v_today']:.0f} km/s today, k_fs {d_['k_fs_today']:.2f} h/Mpc "
                                                   f"(lambda {d_['lambda_fs']:.0f} Mpc/h), travelled {d_['chi_to_today']:.1f} Mpc/h" for zc, d_ in FS.items()))
P("    against: galaxy r200 ~ 0.1-0.3 Mpc, group ~ 0.5 Mpc, cluster R500 ~ 1 Mpc, the sigma8 sphere 8 Mpc/h: the daughters stream out of every "
  "galaxy and group potential (v_esc < v), are recaptured by clusters (v_esc ~ 2000 km/s) after Hubble cooling, and cluster only above ~20-40 Mpc/h")
OUT["numbers"]["X2_free_streaming"] = FS
check("X2 (reported) free streaming and the carrier-sector matter power at KiDS scales", {k_: {str(z): v for z, v in d_["T2"][0.5].items()} for k_, d_ in XR.items()},
      True, load_bearing=False)
check("X3 (reported) CMB lensing (Limber, linear): C_L^phiphi ratio to LCDM at L = 100/300/1000",
      {k_: d_["CMBlens"] for k_, d_ in XR.items()}, True, "Planck 2018 measures the lensing amplitude to ~2.5% (1 sigma)", load_bearing=False)
# X4 forest: XR16 B2's committed response range per unit F(2)
xr16B2 = json.load(open(os.path.join(HERE, "XR16_fluid_conversion_surface_results.json")))["numbers"]["B2"]["rule_per_F2"]
fr_ = {k_: (FT[k_][2.0] * xr16B2[0], FT[k_][2.0] * xr16B2[1]) for k_ in ("nominal", "most conservative", "pump s = 1", "dt0 canonical top+up 14.6", "dt0 alt top+up 22.8")}
P("    forest (XR16 B2's committed L365-rule response per unit F(2), " + f"{xr16B2[0]:.3f}-{xr16B2[1]:.3f}): projected rule at z = 2 "
  + "; ".join(f"{k_}: F_tot(2) {FT[k_][2.0]:.3f} -> {a_:.3f}-{b_:.3f}" for k_, (a_, b_) in fr_.items()) + " (gate 0.10; halo only 0.027-0.135)")
OUT["numbers"]["X4_forest"] = {k_: list(v_) for k_, v_ in fr_.items()}
check("X4 (reported) the Lyman-alpha forest: the web's z ~ 2 conversion raises F(2) and the projected rule; an extrapolation past "
      "the committed F(2) <= 0.28, as in XR16 B2", {k_: f"{a_:.3f}-{b_:.3f}" for k_, (a_, b_) in fr_.items()}, True, load_bearing=False)
# X5 X-COP (order of magnitude): the share of a z = 0 cluster's carrier accreted after its web converted
XC = {}
for al in (0.6, 0.8, 1.0):
    for zc in (1.0, 1.5):
        late = 1 - math.exp(-al * zc)
        XC[f"alpha {al}, z_web {zc}"] = dict(late_share=late, web_converted_late=late * RUNS["nominal"]["hist"][zc]["f"])
P("    X-COP (order of magnitude): a cluster's carrier accreted after z_web (M ~ exp(-alpha z), XR16's alpha) that arrives already "
  "converted: " + "; ".join(f"{k_}: {v_['web_converted_late']:.2f}" for k_, v_ in XC.items()))
P("    those daughters were Hubble-cooled to ~300-400 km/s before infall, far below a cluster's escape speed (~2000 km/s): they are "
  "recaptured (as XR12's upstream daughters were), on hotter orbits; X-COP's retained fraction moves by less than this share")
OUT["numbers"]["X5_xcop"] = XC
check("X5 (reported) X-COP, order of magnitude only (no re-scoring)", {k_: round(v_["web_converted_late"], 3) for k_, v_ in XC.items()}, True,
      load_bearing=False)

# ============================================================================================ summary
banner("SUMMARY")
nm = RUNS["nominal"]["hist"]
P(f"""  Does the dark fluid's conversion run away through the web?  Partly -- yes through the collapsed and turned-around web at
  z <~ 1.5, no through the voids, and not at z >~ 3.
  Nominal cell: the smooth (non-halo) carrier converts f_web = {nm[3.0]['f']:.2f}/{nm[2.0]['f']:.2f}/{nm[1.0]['f']:.2f}/{nm[0.0]['f']:.2f} at z = 3/2/1/0 (most conservative bracket
  {RUNS['most conservative']['hist'][3.0]['f']:.2f}/{RUNS['most conservative']['hist'][2.0]['f']:.2f}/{RUNS['most conservative']['hist'][1.0]['f']:.2f}/{RUNS['most conservative']['hist'][0.0]['f']:.2f}); with the halos, F_tot = {FT['nominal'][3.0]:.2f}/{FT['nominal'][2.0]:.2f}/{FT['nominal'][1.0]:.2f}/{FT['nominal'][0.0]:.2f} (halo only
  {Fhalo_of('nominal 5.31')[0](3.0):.2f}/{Fhalo_of('nominal 5.31')[0](2.0):.2f}/{Fhalo_of('nominal 5.31')[0](1.0):.2f}/{Fhalo_of('nominal 5.31')[0](0.0):.2f}).  The converted web is one connected set.
  What drives it: the halos' own daughters seed the multistream and turned-around web around them (momentum matching through
  the infall), and turned-around sheets ignite by themselves on the zero-strain cone.  What stops it: expanding flow (no
  re-resonance; the voids keep {1 - nom[0.0]['ex_conv']:.0%} of their carrier), and the gate at high z (rho_t/rho_bar = 36/68 at z = 3/4).
  Across the band: F_tot(0) {f0min:.2f}-{max(d_['F0'] for b_ in band.values() for d_ in b_.values()):.2f}, F_tot(1) {f1min:.2f}-{max(d_['F1'] for b_ in band.values() for d_ in b_.values()):.2f}; S8 ratio {XR['nominal']['S8_ratio']:.3f} (nominal).""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["summary"] = dict(n_checks=len(CH), load_bearing_failed=n_fail, runtime_s=round(time.time() - T0, 1))
suffix = "_MUTATE" if MUTATE else ""
json.dump(OUT, open(os.path.join(OUTDIR, f"{SLUG}_results{'_SMOKE' if SMOKE else ''}{suffix}.json"), "w"), indent=1,
          default=lambda o: (o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating,)) else str(o))))
P(f"\n  checks: {sum(ok for _, ok, _ in CH)}/{len(CH)} pass; load-bearing failures: {n_fail}   {el()}")
sys.exit(1 if n_fail else 0)
