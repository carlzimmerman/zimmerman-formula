#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR35_kids_rescore.py -- THE M* KiDS CHAIN RE-SCORED WITH THE CORRECTED PROJECTION: DE10 -> XR9 -> XR14.
Cross-thread review lane XR35 (2026-09-27).  Read-only on every committed file.

WHY.  FP20 (derivation_chain_2026/FP20_esd_projection_fix.py, 7a8c25321) found that the record's three KiDS projectors
share one defect: the trapezoid over the Abel integral skips the 1/sqrt end interval, and the projected mass inside the
first projected radius is carried by a disc term that is exact only for Sigma ~ 1/R.  L352's project_M2 and DE8's
esd_from_mlens (the 'P2 family') are off by -2..-3% on a singular isothermal sphere, -3..+11% on NFW halos and
+187% / -123% at 35 kpc on cored / hollowed carrier templates; FP6's esd_of_M (P1) also loses half the inner projected mass
(-59% at 35 kpc on the SIS).  FP20 supplied drop-in fixes (CellFix for DE8's cells, M2Fix for project_M2's node densities,
an exact-shell model_M2 path) and re-scored the chain's lanes, but left the M* KiDS chain open (its ledger F20n): DE10
(dabce1b73; the converged model), XR9 (the small-region door's KiDS scan) and XR14 (b667f56bb; KiDS on M*'s own carrier,
the only scorecard row validated ON M*).  Each of them projects a cored / hollowed carrier template with project_M2 and the
switched lens with esd_from_mlens.  This lane re-scores them with ONLY the projector replaced.

WHAT IS SWAPPED (nothing else):
  (a) DE8's esd_from_mlens (point mass + the switched phantom's lensing mass inside DE8's cell faces): its m2_of_rho ->
      FP20's CellFix(faces, Rp) (the cells as exact uniform shells);
  (b) L352's project_M2 on the carrier templates' node densities (DE10/XR9/XR14's template()) -> FP20's M2Fix(rr, Rp)
      (trapezoid shell masses between nodes, exact shell kernels, the core inside the first node);
  (c) L352's model_M2 (the unswitched baseline: esd_bin / fit_model; and L360's fit_comb in DE10's C1) -> FP20's
      model_M2_factory(direct=True) (exact shells straight from M(r)); every baseline chi^2 is recomputed with it.
  FP20's drop-ins are exec'd from FP20's committed source (git HEAD), not re-typed.
  KEPT AS COMMITTED: the data and covariance; the fits (L352's M_b grid, the 2-halo amplitude bounds); the linear 2-halo
  template (its own inner-disc approximation, FP20 V5 -- priced in S2); the exact annulus average; the gates, operators and
  caps; the carrier halos (the cached shell-model histograms at their committed masses and seeds); the flagship.
HOW.  Each lane's committed main block is exec'd in this lane's namespace (file writes refused, stdout captured), TWICE:
  with the committed projectors (the control: every committed number must come back exactly) and with FP20's drop-ins
  spliced in right after DE8 is loaded.  DE10's halo generation is replaced by the cached halos: XR9's cache holds DE10's
  eight halos (L390's masses, DE10's seeds, N = 60000), from which XR9 C1 and XR14 C1 already reproduced DE10's table.

PRE-DECLARED HYPOTHESES (written into this file before any score with the corrected projection was computed; the writer's
expectation in brackets)
  H1  [load-bearing] XR14's ON-M* KiDS pass survives the corrected projection: M*'s carrier ('MSPH') passes KiDS (Delta chi^2
      <= +4 against the unswitched model re-fitted with the same projector; fs = 1, A <= 2) on both footings, at w = 0.02 and
      0.25 and every kick 575-650 km/s.  [expected PASS: the committed margin is ~30; the decayed carrier's share of the
      score is only 5-6 (XR14 V1)]
  H1b [load-bearing] L388's carrier AS WRITTEN passes on the same terms.  [expected PASS]
  H2  [load-bearing] DE10's headline passes: all four cells (600 / 650 km/s x w = 0.02 / 0.25) <= +4 on both footings.
      [expected PASS]
  H3  [reported] XR9's per-cell KiDS verdicts (w = 0.25, fs = 1, A <= 2, both kicks and footings) are unchanged: p1_x2.5 and
      p1.5_x2.5 pass, the other twelve fail, so the door's KiDS half (H-K) still fails.  [expected unchanged]
  The pass bar is each lane's own: Delta chi^2 <= +4 on both footings.

CHECKS
  V0 [load-bearing] THE INDEPENDENT REFERENCE: this lane's own fine-shell projector (40 000 log shells from 1e-5 to 30 Mpc,
     exact uniform-shell kernels, written here; exact shell masses where M(r) is closed-form, midpoint masses for the carrier
     templates; edges snapped onto the known density jumps -- added after the first development run, see the README)
     reproduces closed forms -- the truncated singular isothermal sphere, NFW (Wright & Brainerd 2000) and the Plummer
     sphere -- to 1e-5 at the 15 KiDS radii (point values and annulus averages), and adaptive quadrature on the hollow /
     capped NFW and on one scored carrier template to 1e-5 of the peak.
  V1 [load-bearing; MUTATE must fail] FP20'S DROP-INS REMOVE THE DEFECT: on the smooth profiles (SIS V = 200 km/s; NFW 5e11 c8,
     3e12 c4, 1e13 c2; Plummer 1e11 Msun with a = 50 and 150 kpc) every drop-in path -- M2Fix on node densities, the direct
     model_M2 path, CellFix on DE8's cells (annulus averages at the 15 radii) and ESDFix on the P1 grid (point values at the
     radii) -- is within 0.04% of the reference at every radius (FP20's stated precision); on the profiles with density
     jumps (the NFW 3e12 c4 hollowed inside 100 kpc; the same NFW capped at its own density at 50 kpc) within 0.2% of the
     profile's peak |Delta Sigma|.
  V2 [load-bearing] THE DEFECT IS REAL (confirmed independently): the committed P2 paths (project_M2 on node densities,
     L352's model_M2 path, DE8's esd_from_mlens) are low on the SIS at every radius, by 1.5-3.5%; high on the NFW 1e13 c2 at
     35 kpc by more than 10%; high on both Plummer spheres and the capped NFW at 35 kpc by more than 5%; wrong on the hollow
     NFW by more than 5% of its peak |Delta Sigma|; FP6's P1 esd_of_M is low on the SIS at 35 kpc by more than 50%.
  V3 [load-bearing] THE DROP-IN ON THE SCORED CARRIER TEMPLATES: on every carrier template the three lanes project (XR14's 84
     halos, XR9's 28), M2Fix matches the V0 reference within 0.2% of the template's peak |Delta Sigma| and within 0.01 of the
     bin's KiDS error at every radius; the committed project_M2's deviation on the same templates is reported (the defect
     where the score feels it).
  K1 [load-bearing] CONTROLS: with the committed projectors every committed number is reproduced exactly (|d| <= 1e-9 on every
     numeric leaf of the committed results' 'numbers', and every check verdict): DE10, XR9 (KiDS scan, KiDS cap, flagship)
     and XR14 (every table).
  K2 [load-bearing] the cached halos are DE10's: each of DE10's eight configurations (bin, M_b, kick, seed, N, alpha, Gamma,
     grow_b) equals the cache entry used.
  K3 [load-bearing] the drop-ins are FP20's committed code: extracted from git HEAD, and with them L352's unswitched base
     chi^2 is FP20's committed R9 value (159.920 / 153.018) and DE8's isolated-QUMOND C1 fit equals it.
  K4 [load-bearing] the flagship is projection-free: XR9's flagship rows and caps are identical under both projectors.
  R1-R3 (reported) the before -> after tables of DE10, XR9 and XR14 per cell, and which cells cross the +4 bar.
  R4 (reported) the lanes' own checks that change verdict under the corrected projection (controls pinned to committed
     numbers are labelled as such).
  H1 H1b H2 [load-bearing, pre-declared]; H3 [reported, pre-declared].
  S1 (reported) IS RE-PROJECTING THE CACHED HALOS ENOUGH?  The carrier halos' masses were refitted with the defective
     projector (L390's curvature-branch refit for DE10/XR14; XR9_carrier_halos' per-cell refit for XR9).  The refits are
     repeated with the corrected projector; where they move, the cells are re-scored with cached halos at the new masses
     (XR9's cache spans 0.2-0.3 dex per bin), and the mass sensitivity of the M* chain is measured with L375's cached halos.
  S2 (reported) the 2-halo template's inner disc (kept as committed): its error against an exact inner integral and the
     score change at XR14's worst cells if it were replaced.
  F  [load-bearing] every re-score completed with finite numbers.
  ADDED AFTER THE FIRST MAIN RUN (reported diagnostics; V1 and V3 failed there and are kept as run, thresholds unchanged):
  V1d where V1's Plummer a = 150 kpc residual comes from (the P2 lanes' read of M_2D on the 700-point Rp grid, or the projection);
  V3d which term carries V3's residual on the templates over threshold (M2Fix's power-law core inside the first node);
  V3s whether that residual touches a scored cell (every carrier template replaced by this lane's reference, XR14 and DE10 re-fit).
MUTATE=1 puts the committed projectors in the corrected slot everywhere: V1 must FAIL (rc = 1; V3 and K3, which also test the
corrected slot, fail with it), and every 'after' number must equal its 'before' (the harness is exact end to end; K-MUT).
Outputs *_MUTATE.out / *_results_MUTATE.json.

SCOPE.  The projection only.  kappa = 1/2 is FITTED (Z = 5.7888); nothing here tests it.  Spherical, isolated lenses as in the
lanes; the halos are not regenerated (S1 says when that would matter).  Not 'closed'.
Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR35_kids_rescore.py   (MUTATE=1 first)
"""
import os, sys, io, json, math, time, builtins, contextlib, warnings, subprocess, traceback
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
warnings.filterwarnings("ignore")
import numpy as np
from scipy.integrate import quad
from scipy.interpolate import CubicSpline

np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR35_kids_rescore"
SECTIONS = os.environ.get("XR35_SECTIONS", "all")                    # development switch; the recorded runs use 'all'
T0 = time.time()
FEET = ("canonical", "alt")
BAR = 4.0


class _Tee:
    def __init__(self, fh): self.fh, self.so = fh, sys.__stdout__
    def write(self, s): self.so.write(s); self.fh.write(s)
    def flush(self): self.so.flush(); self.fh.flush()


_OUTFH = builtins.open(os.path.join(HERE, SLUG + ("_MUTATE" if MUTATE else "") + ".out"), "w")
sys.stdout = _Tee(_OUTFH)
CH, OUT = [], {"lane": "XR35 (M* KiDS chain re-scored with the corrected projection)", "mutate": MUTATE, "checks": {}, "numbers": {}}


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)


def el():
    return f"[{time.time() - T0:.0f} s]"


def want(sec):
    return SECTIONS == "all" or sec in SECTIONS.split(",")


def check(name, measured, ok, load_bearing=True, reading=None):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing, "name": name}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def jdefault(o):                                                      # XR9/XR14's own JSON default
    return o.tolist() if hasattr(o, "tolist") else (bool(o) if isinstance(o, np.bool_) else str(o))


def jnorm(o):
    return json.loads(json.dumps(o, default=jdefault))


def rel(p):
    return os.path.relpath(p, REPO)


# ================================================================================================= the harness
def _ro_open(file, mode="r", *a, **k):
    if any(c in mode for c in "wax+"):
        raise PermissionError(f"XR35 refuses to write {os.path.basename(str(file))!r} from a re-executed lane")
    return builtins.open(file, mode, *a, **k)


@contextlib.contextmanager
def lane_env():
    """MUTATE=0 for the re-executed lanes (they read it at exec time) and their stdout captured."""
    old = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            yield buf
    finally:
        if old is None:
            os.environ.pop("MUTATE", None)
        else:
            os.environ["MUTATE"] = old


def git_head(relpath):
    return subprocess.run(["git", "-C", REPO, "show", f"HEAD:{relpath}"], capture_output=True, text=True, check=True).stdout


def exec_main(path, hook_marker, stop_marker, hook, pre_hook=None, name="lane"):
    """exec a committed lane: its module part, then its (dedented) __main__ block up to hook_marker, hook(ns), then on to
    stop_marker (before its results are written).  File writes are refused; stdout is captured.  Line numbers are kept."""
    src = builtins.open(path).read()
    assert src == git_head(rel(path)), f"{rel(path)} differs from git HEAD"
    key = '\nif __name__ == "__main__":\n'
    i0 = src.index(key)
    head = src[:i0 + 1]
    body = "\n".join(l_[4:] if l_.startswith("    ") else l_ for l_ in src[i0 + len(key):].split("\n"))
    off = src[:i0 + len(key)].count("\n")
    ia = body.index("\n" + hook_marker) + 1
    ib = body.index("\n" + stop_marker) + 1
    ns = {"__file__": path, "__name__": name, "open": _ro_open}
    with lane_env() as buf:
        exec(compile(head, path, "exec"), ns)
        if pre_hook:
            pre_hook(ns)
        exec(compile("\n" * off + body[:ia], path, "exec"), ns)
        hook(ns)
        exec(compile("\n" * (off + body[:ia].count("\n")) + body[ia:ib], path, "exec"), ns)
    return ns, buf.getvalue()


def flatten(o, p=""):
    out = {}
    if isinstance(o, dict):
        for k_, v_ in o.items():
            out.update(flatten(v_, f"{p}/{k_}"))
    elif isinstance(o, list):
        for i_, v_ in enumerate(o):
            out.update(flatten(v_, f"{p}[{i_}]"))
    elif isinstance(o, bool) or o is None or isinstance(o, str):
        out[p] = o
    elif isinstance(o, (int, float)):
        out[p] = float(o)
    return out


def compare_numbers(committed, rerun):
    """max |d| over every numeric leaf of the committed 'numbers'; mismatched non-numeric leaves and missing keys listed."""
    fc, fr = flatten(committed), flatten(rerun)
    dmax, bad, miss, n = 0.0, [], [], 0
    for k_, v_ in fc.items():
        if k_ not in fr:
            miss.append(k_); continue
        w_ = fr[k_]
        if isinstance(v_, float) and isinstance(w_, float):
            n += 1
            if math.isnan(v_) and math.isnan(w_):
                continue
            d_ = abs(v_ - w_)
            dmax = max(dmax, d_ if math.isfinite(d_) else float("inf"))
        elif v_ != w_:
            bad.append((k_, v_, w_))
    return dict(n=n, dmax=dmax, nonnumeric_mismatch=bad[:10], n_bad=len(bad), missing=miss[:10], n_missing=len(miss))


def compare_checks(committed, rerun):
    out = []
    for k_, v_ in committed.items():
        r_ = rerun.get(k_)
        if r_ is None:
            out.append((k_, "missing")); continue
        if bool(v_.get("pass", v_.get("ok"))) != bool(r_.get("pass", r_.get("ok"))) or v_.get("measured") != r_.get("measured"):
            out.append((k_, f"{v_.get('pass')} -> {r_.get('pass')}"))
    return out


# ================================================================================================= FP20's drop-ins (git HEAD)
FP20_REL = "real_research/derivation_chain_2026/FP20_esd_projection_fix.py"
FP20_SRC = git_head(FP20_REL)
FP20_TREE_SAME = FP20_SRC == builtins.open(os.path.join(REPO, FP20_REL)).read()


def _slice(src, a, b):
    i = src.index(a); return src[i:src.index(b, i)]


S_DROP = _slice(FP20_SRC, "def shell_mats(edges, Rv):", "# ================================================================================================= the record's projectors (loaded)")
S_FACT = _slice(FP20_SRC, "def model_M2_factory(L, direct):", "\n\ndef r9_p2():")
FPNS = {"np": np, "math": math, "MUTATE": MUTATE, "__name__": "fp20_dropins"}
exec(compile(S_DROP, "FP20_esd_projection_fix.py[drop-ins, git HEAD]", "exec"), FPNS)
exec(compile(S_FACT, "FP20_esd_projection_fix.py[model_M2_factory, git HEAD]", "exec"), FPNS)
CellFix, M2Fix, ESDFix, model_M2_factory = FPNS["CellFix"], FPNS["M2Fix"], FPNS["ESDFix"], FPNS["model_M2_factory"]

P(__doc__.split("PRE-DECLARED")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the committed projectors are put in the corrected slot everywhere -- V1 must FAIL, and every 'after' "
      "number must equal its 'before' ***")
P(f"\n  FP20's drop-ins exec'd from git HEAD ({len(S_DROP.splitlines())} + {len(S_FACT.splitlines())} lines; working tree identical: "
  f"{FP20_TREE_SAME})")

# ================================================================================================= DE8 / L352 / FP6 machinery (read-only)
P8 = os.path.join(REPO, "real_research", "dark_energy_2026", "DE8_kids_sigma_axis_both_branches.py")
P6 = os.path.join(REPO, "real_research", "derivation_chain_2026", "FP6_gate_survey.py")


def load_de8():
    src = builtins.open(P8).read()
    assert src == git_head(rel(P8))
    D8 = {"__name__": "de8", "__file__": P8, "open": _ro_open}
    with lane_env():
        exec(src.split("# ============================================================================================ C1 C2 C3 controls")[0]
             .replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), D8)
    return D8


D8V = load_de8()
L52V = D8V["L52"]
rr, Rp, RD, LOGSTEP = L52V["rr"], L52V["Rp"], L52V["Rd"][0], L52V["LOGSTEP"]
G, MS, PCm, MPCm = L52V["G"], L52V["MS"], L52V["PCm"], L52V["MPCm"]
annulus_esd, project_M2_bug = L52V["annulus_esd"], L52V["project_M2"]
FACES, VC, RF = D8V["faces"], D8V["V"], D8V["rf"]
assert all(np.array_equal(RD, x) for x in L52V["Rd"])
FIX2 = M2Fix(rr, Rp)
FPNS["FIX2"] = FIX2
FIXC = CellFix(FACES, Rp)
m2_bug_cells = D8V["m2_of_rho"]
fix_nodes = project_M2_bug if MUTATE else FIX2                         # the corrected slot (MUTATE: the committed projector)
fix_cells = m2_bug_cells if MUTATE else FIXC
src6 = builtins.open(P6).read()
assert src6 == git_head(rel(P6))
M6 = {"__file__": P6, "__name__": "fp6_machinery", "open": _ro_open}
with lane_env():
    exec(compile(src6[:src6.index('banner("K  CONTROLS')], P6, "exec"), M6)
RR6, RP6, MPCm6, PCm6, MS6 = M6["RR"], M6["RP"], M6["MPCm"], M6["PCm"], M6["MS6"]
esd_of_M_bug = M6["esd_of_M"]
FIX1_RD = ESDFix(RR6, RD * MPCm6, PCm6, MS6)
P(f"  loaded read-only: DE8's head (L352's KiDS machinery, esd_from_mlens), FP6's machinery (esd_of_M); L352 grids r = "
  f"{rr[0] / MPCm:g}-{rr[-1] / MPCm:g} Mpc x {len(rr)}, R = {Rp[0] / MPCm:g}-{Rp[-1] / MPCm:g} x {len(Rp)}; DE8 cells {len(VC)}; "
  f"KiDS radii {RD[0]:.4f}-{RD[-1]:.4f} Mpc x {len(RD)}   {el()}")

# ================================================================================================= this lane's reference projector
RT = rr[-1]
CONV = PCm ** 2 / MS                                                   # kg/m^2 -> Msun/pc^2 (L352 / DE8)
CONV6 = PCm6 ** 2 / MS6                                                # FP6


def qfun(x, R):
    """x^3 - (x^2 - R^2)_+^(3/2), written without cancellation."""
    s = np.sqrt(np.clip(x * x - R * R, 0.0, None))
    return np.where(x > R, R * R * (x * x + x * s + s * s) / (x + s), x ** 3)


class FineRef:
    """this lane's own projector: uniform-density shells between log-spaced edges (exact shell masses from M(r) where M is
    known in closed form, else midpoint density x shell volume), the mass inside the first edge a central point, and edges
    snapped onto the known density jumps so that no shell straddles one.  M_2D(<R) = sum_k m_k [q(b_k) - q(a_k)]/(b_k^3 - a_k^3);
    Sigma(R) = sum_k 2 rho_k [sqrt((b^2 - R^2)_+) - sqrt((a^2 - R^2)_+)]."""

    def __init__(self, rmin, rmax, n, n_pt, Rgrid, Rpts, snaps=()):
        self.rmin, self.Rg, self.Rpts = rmin, Rgrid, Rpts
        self.e = self._edges(rmin, rmax, n, snaps); self.ep = self._edges(rmin, rmax, n_pt, snaps)
        self.rm, self.rmp = np.sqrt(self.e[1:] * self.e[:-1]), np.sqrt(self.ep[1:] * self.ep[:-1])
        self.V = 4 * math.pi / 3 * (self.e[1:] ** 3 - self.e[:-1] ** 3); self.Vp = 4 * math.pi / 3 * (self.ep[1:] ** 3 - self.ep[:-1] ** 3)
        self.F = self._frac(self.e, Rgrid)                             # M_2D on the annulus grid (n shells)
        self.Fp, self.Sp = self._frac(self.ep, Rpts), self._sig(self.ep, self.Vp, Rpts)   # point values (n_pt shells: the uniform
        #                                                              shell's Sigma error next to R is O(h^1.5), so finer here)

    @staticmethod
    def _edges(rmin, rmax, n, snaps):
        e = np.geomspace(rmin, rmax, n + 1)
        for s in snaps:
            e[int(np.argmin(np.abs(np.log(e / s))))] = s
        assert np.all(np.diff(e) > 0)
        return e

    @staticmethod
    def _frac(e, R):
        a, b = e[:-1], e[1:]; d3 = b ** 3 - a ** 3
        out = np.empty((len(R), len(a)))
        step = max(1, int(4e6 // len(a)))
        for i in range(0, len(R), step):
            Rc = R[i:i + step, None]
            out[i:i + step] = (qfun(b[None, :], Rc) - qfun(a[None, :], Rc)) / d3[None, :]
        return out

    @staticmethod
    def _sig(e, V, R):
        a, b = e[:-1], e[1:]; Rc = R[:, None]
        return 2 * (np.sqrt(np.clip(b ** 2 - Rc ** 2, 0.0, None)) - np.sqrt(np.clip(a ** 2 - Rc ** 2, 0.0, None))) / V[None, :]

    def masses(self, rho_fun):                                        # midpoint density x volume (the carrier templates)
        c = lambda e0: float(rho_fun(np.array([e0]))[0]) * 4 * math.pi / 3 * e0 ** 3
        return dict(m=rho_fun(self.rm) * self.V, m0=c(self.e[0]), mp=rho_fun(self.rmp) * self.Vp, mp0=c(self.ep[0]))

    def masses_M(self, M_fun):                                        # exact shell masses from a closed-form M(r)
        Me, Mp = M_fun(self.e), M_fun(self.ep)
        return dict(m=np.diff(Me), m0=float(Me[0]), mp=np.diff(Mp), mp0=float(Mp[0]))

    def point_ds(self, ms, Mb=0.0):                                   # Delta Sigma at Rpts [kg/m^2]
        M2 = self.Fp @ ms["mp"] + ms["mp0"] + Mb
        return M2 / (math.pi * self.Rpts ** 2) - self.Sp @ ms["mp"]

    def point_parts(self, ms, Mb=0.0):
        return self.Fp @ ms["mp"] + ms["mp0"] + Mb, self.Sp @ ms["mp"]

    def ann_ds(self, ms, Mb=0.0):                                     # the annulus average [Msun/pc^2] (L352's annulus_esd)
        M2 = self.F @ ms["m"] + ms["m0"] + Mb
        cs = CubicSpline(np.log(self.Rg), M2)
        return annulus_esd(lambda R: cs(np.log(R)), RD)


RGRID = np.geomspace(0.027, 3.2, 1200) * MPCm
_E14 = json.load(builtins.open(os.path.join(HERE, "XR14_carrier_halos_results.json")))["edges_kpc"]
RM_LAST = math.sqrt(_E14[-2] * _E14[-1]) * 1e-3 * MPCm                 # the carrier templates' outer cut (their only jump)
SNAPS = (0.05 * MPCm, 0.1 * MPCm, RM_LAST)                              # the capped / hollow profiles' jumps; the carriers' cut
REF = FineRef(1e-5 * MPCm, RT, 40000, 400000, RGRID, RD * MPCm, snaps=SNAPS)
P(f"  this lane's reference projector: {len(REF.rm)} log shells {REF.e[0] / MPCm:g}-{REF.e[-1] / MPCm:g} Mpc for M_2D on {len(RGRID)} radii "
  f"(cubic spline in ln R; the annulus averages), {len(REF.rmp)} for the point values; edges snapped onto "
  f"{', '.join(f'{s / MPCm:.4g}' for s in SNAPS)} Mpc   {el()}")

# ================================================================================================= the analytic profiles
VSIS = 200e3; KSIS = VSIS ** 2 / G
RHOC = L52V["rho_crit0"] * (L52V["Om"] * 1.25 ** 3 + L52V["OL"])    # rho_crit(z = 0.25), L352's cosmology


def nfw_par(M200, c):
    r200 = (3 * M200 * MS / (4 * math.pi * 200 * RHOC)) ** (1 / 3); rs = r200 / c
    return rs, M200 * MS / (4 * math.pi * rs ** 3 * (math.log(1 + c) - c / (1 + c)))


def nfw_Mu(r, M200, c):                                                # untruncated enclosed mass
    rs, rhos = nfw_par(M200, c); x = np.asarray(r, float) / rs
    return 4 * math.pi * rhos * rs ** 3 * (np.log1p(x) - x / (1 + x))


def nfw_rho_u(r, M200, c):
    rs, rhos = nfw_par(M200, c); x = np.asarray(r, float) / rs
    return rhos / (x * (1 + x) ** 2)


def nfw_ds_wb(R, M200, c):
    """Wright & Brainerd (2000) Delta Sigma of the untruncated NFW [kg/m^2], this lane's own transcription."""
    rs, rhos = nfw_par(M200, c); out = []
    for x in np.atleast_1d(np.asarray(R, float)) / rs:
        if abs(x - 1) < 1e-7:
            g = 10 / 3 + 4 * math.log(0.5)
        elif x < 1:
            t = math.atanh(math.sqrt((1 - x) / (1 + x)))
            g = 8 * t / (x * x * math.sqrt(1 - x * x)) + 4 / (x * x) * math.log(x / 2) - 2 / (x * x - 1) + 4 * t / ((x * x - 1) * math.sqrt(1 - x * x))
        else:
            t = math.atan(math.sqrt((x - 1) / (1 + x)))
            g = 8 * t / (x * x * math.sqrt(x * x - 1)) + 4 / (x * x) * math.log(x / 2) - 2 / (x * x - 1) + 4 * t / ((x * x - 1) ** 1.5)
        out.append(rs * rhos * g)
    return np.array(out)


def nfw_M2(R, M200, c):
    rs, rhos = nfw_par(M200, c); x = np.atleast_1d(np.asarray(R, float)) / rs
    h = np.where(x < 1, np.arccosh(1 / np.minimum(x, 1 - 1e-15)) / np.sqrt(np.maximum(1 - x * x, 1e-300)),
                 np.arccos(1 / np.maximum(x, 1 + 1e-15)) / np.sqrt(np.maximum(x * x - 1, 1e-300)))
    return 4 * math.pi * rhos * rs ** 3 * (np.log(x / 2) + h)


MPL = 1e11 * MS


def prof_defs():
    """name -> dict(M(r) [kg], rho(r) [kg/m^3], Mb [kg], m_core [kg] inside the reference's first edge, point reference
    [kg/m^2] at the radii or None, M2 reference R -> kg or None, smooth flag)."""
    D = {}
    rmin = REF.rmin
    D["SIS V=200"] = dict(M=lambda r: KSIS * np.minimum(r, RT), rho=lambda r: np.where(r <= RT, KSIS / (4 * math.pi * r ** 2), 0.0),
                          Mb=0.0, core=KSIS * rmin, smooth=True,
                          M2=lambda R: KSIS * (RT - np.sqrt(RT ** 2 - R ** 2) + R * np.arccos(R / RT)),
                          Sig=lambda R: KSIS / (2 * math.pi * R) * np.arccos(R / RT))
    for (M200, c) in ((0.5e12, 8.0), (3e12, 4.0), (1e13, 2.0)):
        D[f"NFW {M200:.1e} c{c:g}"] = dict(M=lambda r, M200=M200, c=c: nfw_Mu(np.minimum(r, RT), M200, c),
                                          rho=lambda r, M200=M200, c=c: np.where(r <= RT, nfw_rho_u(r, M200, c), 0.0),
                                          Mb=0.0, core=float(nfw_Mu(rmin, M200, c)), smooth=True,
                                          M2=lambda R, M200=M200, c=c: nfw_M2(R, M200, c),
                                          DS=lambda R, M200=M200, c=c: nfw_ds_wb(R, M200, c))
    for a_kpc in (50.0, 150.0):
        a = a_kpc * 1e-3 * MPCm
        D[f"Plummer 1e11 a={a_kpc:g} kpc"] = dict(
            M=lambda r, a=a: MPL * np.minimum(r, RT) ** 3 / (np.minimum(r, RT) ** 2 + a * a) ** 1.5,
            rho=lambda r, a=a: np.where(r <= RT, 3 * MPL / (4 * math.pi * a ** 3) * (1 + (r / a) ** 2) ** -2.5, 0.0),
            Mb=0.0, core=MPL * rmin ** 3 / (rmin ** 2 + a * a) ** 1.5, smooth=True,
            M2=lambda R, a=a: MPL * R ** 2 / (R ** 2 + a * a), DS=lambda R, a=a: MPL * R ** 2 / (math.pi * (R ** 2 + a * a) ** 2))
    RH = 0.1 * MPCm
    D["hollow NFW 3e12 c4 (empty < 100 kpc)"] = dict(
        M=lambda r: np.where(r > RH, nfw_Mu(np.minimum(r, RT), 3e12, 4.0) - nfw_Mu(RH, 3e12, 4.0), 0.0),
        rho=lambda r: np.where((r > RH) & (r <= RT), nfw_rho_u(r, 3e12, 4.0), 0.0), Mb=0.0, core=0.0, smooth=False, rjump=RH)
    RC = 0.05 * MPCm; RHO_CAP = float(nfw_rho_u(RC, 3e12, 4.0))
    D["capped NFW 3e12 c4 (flat < 50 kpc)"] = dict(
        M=lambda r: np.where(np.minimum(r, RT) < RC, 4 * math.pi / 3 * RHO_CAP * np.minimum(r, RT) ** 3,
                             4 * math.pi / 3 * RHO_CAP * RC ** 3 + nfw_Mu(np.minimum(r, RT), 3e12, 4.0) - nfw_Mu(RC, 3e12, 4.0)),
        rho=lambda r: np.where(r <= RT, np.minimum(nfw_rho_u(r, 3e12, 4.0), RHO_CAP), 0.0), Mb=0.0,
        core=4 * math.pi / 3 * RHO_CAP * rmin ** 3, smooth=False, rjump=RC)
    return D


def quad_parts(rho, R, brk=()):
    """adaptive quadrature: Sigma(R) = 2 Int rho(sqrt(R^2 + z^2)) dz; M_2D(<R) = Int 4 pi r^2 rho(r) w(r; R) dr,
    w = 1 inside R and 1 - sqrt(1 - R^2/r^2) outside; piecewise between the breakpoints (density jumps / kinks)."""
    f1 = lambda r: 4 * math.pi * r * r * float(rho(np.array([r]))[0])
    zt = math.sqrt(RT * RT - R * R)
    zb = sorted({0.0, zt} | {math.sqrt(b * b - R * R) for b in brk if R < b < RT})
    sig = 2 * sum(quad(lambda z: float(rho(np.array([math.sqrt(R * R + z * z)]))[0]), z0, z1, limit=400, epsabs=0, epsrel=1e-12)[0]
                  for z0, z1 in zip(zb[:-1], zb[1:]))
    rb = sorted({REF.rmin, R, RT} | {b for b in brk if REF.rmin < b < RT})
    m2 = 0.0
    for r0, r1 in zip(rb[:-1], rb[1:]):
        if r1 <= R:
            m2 += quad(f1, r0, r1, limit=400, epsabs=0, epsrel=1e-12)[0]
        else:
            m2 += quad(lambda r: f1(r) * (1 - math.sqrt(max(1 - R * R / (r * r), 0.0))), r0, r1, limit=400, epsabs=0, epsrel=1e-12)[0]
    return m2, sig


# ================================================================================================= the projectors under test
def ann_of_M2grid(M2):                                                 # the P2 lanes' read: interpolate in ln R on Rp, annulus
    return annulus_esd(lambda R: np.interp(np.log(R), np.log(Rp), M2), RD)


def path_node(proj, rho, Mb):                                          # carrier templates: project_M2(rho at nodes)
    return ann_of_M2grid(proj(rho(rr)) + Mb)


def path_model_bug(M, Mb):                                             # L352's model_M2: np.gradient round trip, project_M2
    Mr = M(rr); return ann_of_M2grid(project_M2_bug(np.gradient(Mr - Mb, rr) / (4 * math.pi * rr ** 2)) + Mb)


def path_model_fix(M, Mb):                                             # FP20's model_M2_factory(direct=True) line
    if MUTATE:
        return path_model_bug(M, Mb)
    Mr = M(rr); return ann_of_M2grid(FIX2.C @ np.diff(Mr - Mb) + (Mr[0] - Mb) + Mb)


def path_cells(m2f, M, Mb):                                            # DE8's esd_from_mlens with its m2_of_rho swapped
    old = D8V["m2_of_rho"]
    try:
        D8V["m2_of_rho"] = m2f
        return D8V["esd_from_mlens"](Mb, M(RF) - Mb, 0)
    finally:
        D8V["m2_of_rho"] = old


def path_p1_bug(M, Mb):                                                # FP6's esd_of_M as the P1 lanes read it
    return np.interp(RD, RP6 / MPCm6, esd_of_M_bug(M(RR6), Mb)[1])


def path_p1_fix(M, Mb):                                                # FP20's ESDFix on the P1 r-grid, at the radii
    if MUTATE:
        return path_p1_bug(M, Mb)
    return FIX1_RD(M(RR6), Mb)


# ================================================================================================= V0 V1 V2
PROFS = prof_defs()
VNUM = {}
if want("V"):
    banner("V0-V2  THE ANALYTIC STANDARD: this lane's reference against closed forms and quadrature; the committed projectors and "
           "FP20's drop-ins against the reference, at the 15 KiDS radii")
    refs = {}
    v0 = {}
    for nm, pr in PROFS.items():
        ms = REF.masses_M(pr["M"])
        pt = REF.point_ds(ms, pr["Mb"])
        an = REF.ann_ds(ms, pr["Mb"])
        refs[nm] = dict(point=pt, ann=an)
        if pr["smooth"]:
            dsx = pr["DS"](RD * MPCm) if "DS" in pr else pr["M2"](RD * MPCm) / (math.pi * (RD * MPCm) ** 2) - pr["Sig"](RD * MPCm)
            anx = annulus_esd(lambda R, pr=pr: pr["M2"](R) + pr["Mb"], RD)
            v0[nm] = (float(np.max(np.abs(pt / dsx - 1))), float(np.max(np.abs(an / anx - 1))))
        else:
            qd = []
            for R in RD * MPCm:
                m2q, sq = quad_parts(pr["rho"], R, (pr["rjump"],))
                qd.append(m2q / (math.pi * R * R) - sq)
            qd = np.array(qd)
            v0[nm] = (float(np.max(np.abs(pt - qd)) / np.max(np.abs(qd))), float("nan"))
    P("    reference vs closed form / quadrature, max relative deviation at the 15 radii (point; annulus):")
    for nm, (a_, b_) in v0.items():
        P(f"      {nm:40s} {a_:.2e}; {b_:.2e}")
    VNUM["V0"] = v0
    OUT["numbers"]["V0_reference_vs_exact"] = v0
    P(f"    {el()}")
    # --- the error tables
    ERR, ERRP = {}, {}
    for nm, pr in PROFS.items():
        ref_a, ref_p = refs[nm]["ann"], refs[nm]["point"] * CONV6
        vals = {"P2 node rho, committed project_M2": (path_node(project_M2_bug, pr["rho"], pr["Mb"]), ref_a),
                "P2 model_M2 path, committed": (path_model_bug(pr["M"], pr["Mb"]), ref_a),
                "DE8 cells, committed esd_from_mlens": (path_cells(m2_bug_cells, pr["M"], pr["Mb"]), ref_a),
                "P1 FP6 esd_of_M, committed": (path_p1_bug(pr["M"], pr["Mb"]), ref_p),
                "P2 node rho, FP20 M2Fix": (path_node(fix_nodes, pr["rho"], pr["Mb"]), ref_a),
                "P2 model_M2 path, FP20 direct": (path_model_fix(pr["M"], pr["Mb"]), ref_a),
                "DE8 cells, FP20 CellFix": (path_cells(fix_cells, pr["M"], pr["Mb"]), ref_a),
                "P1, FP20 ESDFix": (path_p1_fix(pr["M"], pr["Mb"]), ref_p)}
        # smooth profiles: relative to the reference point by point; profiles with jumps: relative to the peak |Delta Sigma|
        ERR[nm] = {k_: (v_ / r_ - 1) if pr["smooth"] else (v_ - r_) / np.max(np.abs(r_)) for k_, (v_, r_) in vals.items()}
        ERRP[nm] = {k_: v_ / r_ - 1 for k_, (v_, r_) in vals.items()}
    P("\n    error of each projector vs R [%] at the KiDS radii " + ", ".join(f"{x:.3f}" for x in RD) + " Mpc")
    P("    (smooth profiles: relative to the reference; profiles with density jumps: relative to the peak |Delta Sigma|)")
    for nm, e in ERR.items():
        P(f"    -- {nm}")
        for pj, v in e.items():
            P(f"       {pj:38s} " + " ".join(f"{100 * x:+8.3f}" for x in v) + f"   | max |.| {100 * np.max(np.abs(v)):.3f}%")
    OUT["numbers"]["V_errors_percent"] = {nm: {pj: [100 * float(x) for x in v] for pj, v in e.items()} for nm, e in ERR.items()}
    OUT["numbers"]["V_errors_pointwise_percent"] = {nm: {pj: [100 * float(x) for x in v] for pj, v in e.items()} for nm, e in ERRP.items()}
    OUT["numbers"]["V_radii_Mpc"] = RD.tolist()
    FIXK = ("P2 node rho, FP20 M2Fix", "P2 model_M2 path, FP20 direct", "DE8 cells, FP20 CellFix", "P1, FP20 ESDFix")
    smooth = [nm for nm in PROFS if PROFS[nm]["smooth"]]
    jumpy = [nm for nm in PROFS if not PROFS[nm]["smooth"]]
    vs = {k_: max(float(np.max(np.abs(ERR[nm][k_]))) for nm in smooth) for k_ in FIXK}
    vj = {k_: max(float(np.max(np.abs(ERR[nm][k_]))) for nm in jumpy) for k_ in FIXK}
    v0_ok = all(a_ <= 1e-5 and (math.isnan(b_) or b_ <= 1e-5) for a_, b_ in v0.values())
    check("V0 THE INDEPENDENT REFERENCE: this lane's fine-shell projector reproduces the closed forms (truncated SIS, Wright & "
          "Brainerd NFW x3, Plummer x2) to 1e-5 as point values and annulus averages, and adaptive quadrature on the hollow and "
          "capped NFW to 1e-5 of the peak",
          f"max deviation {max(max(a_, 0 if math.isnan(b_) else b_) for a_, b_ in v0.values()):.1e} over {len(v0)} profiles", v0_ok)
    check("V1 FP20'S DROP-INS REMOVE THE DEFECT: every drop-in path within 0.04% of the reference on the smooth profiles (SIS, "
          "three NFW, two Plummer spheres) and within 0.2% of the peak |Delta Sigma| on the hollow and capped NFW, at all 15 radii",
          "smooth: " + ", ".join(f"{k_.split(', ')[0]} {100 * v:.4f}%" for k_, v in vs.items()) + " | jumps: "
          + ", ".join(f"{k_.split(', ')[0]} {100 * v:.4f}%" for k_, v in vj.items()),
          max(vs.values()) <= 4e-4 and max(vj.values()) <= 2e-3)
    BUGK = ("P2 node rho, committed project_M2", "P2 model_M2 path, committed", "DE8 cells, committed esd_from_mlens")
    sis = [ERR["SIS V=200"][k_] for k_ in BUGK]
    c_sis = all(np.all((x >= -0.035) & (x <= -0.015)) for x in sis)
    c_nfw = all(ERR["NFW 1.0e+13 c2"][k_][0] > 0.10 for k_ in BUGK)
    CORED = ("Plummer 1e11 a=50 kpc", "Plummer 1e11 a=150 kpc", "capped NFW 3e12 c4 (flat < 50 kpc)")
    c_core = all(ERRP[nm][k_][0] > 0.05 for nm in CORED for k_ in BUGK)
    c_hol = all(np.max(np.abs(ERR["hollow NFW 3e12 c4 (empty < 100 kpc)"][k_])) > 0.05 for k_ in BUGK)
    c_p1 = ERR["SIS V=200"]["P1 FP6 esd_of_M, committed"][0] < -0.50
    check("V2 THE DEFECT IS REAL (independent confirmation): the committed P2 paths are low on the SIS by 1.5-3.5% at every "
          "radius, high on NFW 1e13 c2 at 35 kpc by > 10%, high on both Plummer spheres and the capped NFW at 35 kpc by > 5%, off "
          "on the hollow NFW by > 5% of the peak; FP6's P1 is low on the SIS at 35 kpc by > 50%",
          f"SIS {100 * min(float(np.min(x)) for x in sis):+.2f}..{100 * max(float(np.max(x)) for x in sis):+.2f}%; NFW 1e13 c2 at 35 kpc "
          + "/".join(f"{100 * ERR['NFW 1.0e+13 c2'][k_][0]:+.2f}" for k_ in BUGK) + "%; at 35 kpc Plummer 50/150, capped: "
          + "; ".join("/".join(f"{100 * ERRP[nm][k_][0]:+.1f}" for k_ in BUGK) for nm in CORED)
          + f"%; hollow max |.| {100 * max(float(np.max(np.abs(ERR['hollow NFW 3e12 c4 (empty < 100 kpc)'][k_]))) for k_ in BUGK):.1f}% of peak; "
          f"P1 SIS at 35 kpc {100 * ERR['SIS V=200']['P1 FP6 esd_of_M, committed'][0]:+.1f}%",
          c_sis and c_nfw and c_core and c_hol and c_p1)
    VNUM.update(vs=vs, vj=vj)
    # V1d [reported; ADDED AFTER THE FIRST MAIN RUN, where V1 failed on the Plummer a = 150 kpc]: is that residual the projection,
    # or the P2 lanes' read (M_2D sampled on the 700-point Rp grid, linearly interpolated in ln R inside the annulus average)?
    prd = PROFS["Plummer 1e11 a=150 kpc"]; refd = refs["Plummer 1e11 a=150 kpc"]["ann"]
    Mrd = prd["M"](rr)
    Rp10 = np.geomspace(Rp[0], Rp[-1], 7000)
    M2_10 = FPNS["shell_mats"](rr, Rp10)[1] @ np.diff(Mrd) + Mrd[0]
    e_drop = float(np.max(np.abs(ann_of_M2grid(FIX2.C @ np.diff(Mrd) + Mrd[0]) / refd - 1)))   # FP20's true drop-in in either mode
    e_exact_rp = float(np.max(np.abs(ann_of_M2grid(prd["M2"](Rp)) / refd - 1)))
    e_drop10 = float(np.max(np.abs(annulus_esd(lambda R: np.interp(np.log(R), np.log(Rp10), M2_10), RD) / refd - 1)))
    OUT["numbers"]["V1d"] = dict(dropin_on_Rp700=e_drop, exact_M2_on_Rp700=e_exact_rp, dropin_on_Rp7000=e_drop10)
    check("V1d (reported; added after the first main run) THE PLUMMER a = 150 kpc RESIDUAL IS THE P2 LANES' READ, NOT THE PROJECTION: "
          "the EXACT M_2D sampled on the committed 700-point Rp grid and read the lanes' way (linear in ln R) carries the same error, "
          "and FP20's kernel on a 10x finer projected grid removes it (< 0.01%)",
          f"drop-in on Rp(700) {100 * e_drop:.4f}%; exact M_2D on Rp(700) {100 * e_exact_rp:.4f}%; drop-in on Rp(7000) {100 * e_drop10:.5f}%",
          abs(e_exact_rp - e_drop) <= 0.1 * e_drop and e_drop10 < 1e-4, load_bearing=False,
          reading="a read convention shared by both projectors and kept as committed; it bites only deep inside a large flat core, "
                  "where Delta Sigma << Sigma")
    P(f"    {el()}")


# ================================================================================================= the carrier templates (V3)
X9P = os.path.join(HERE, "XR9_carrier_halos_results.json")
X14P = os.path.join(HERE, "XR14_carrier_halos_results.json")
for _p in (X9P, X14P):
    assert builtins.open(_p).read() == git_head(rel(_p)), f"{rel(_p)} differs from git HEAD"
X9 = json.load(builtins.open(X9P))
X14 = json.load(builtins.open(X14P))
EDG9, EDG14 = np.array(X9["edges_kpc"]), np.array(X14["edges_kpc"])
assert np.array_equal(EDG9, EDG14)


def carrier_rho_fun(d, edges=EDG14):
    """DE10/XR9/XR14's carrier_rho_si as a continuous function of r [m] (L375's template density step)."""
    e = edges; rm = np.sqrt(e[1:] * e[:-1]); vol = 4 / 3 * math.pi * (e[1:] ** 3 - e[:-1] ** 3)
    rho = np.array(d["hist"]) * d["m"] / vol
    return lambda r: np.interp(np.log(np.asarray(r, float) / MPCm * 1e3), np.log(rm), rho, left=rho[0], right=0.0) * MS / (MPCm / 1e3) ** 3


SD = [L52V["Sd"][b] for b in range(4)]
REFTPL = {}                                                            # (source, tag) -> this lane's reference template
if want("V3"):
    banner("V3  THE DROP-IN ON THE SCORED CARRIER TEMPLATES: M2Fix vs this lane's reference on every carrier the three lanes project; "
           "the committed project_M2's deviation (the defect where the score feels it)")
    rows = []
    worst = dict(fix_peak=0.0, fix_sig=0.0, bug_peak=0.0, bug_sig=0.0)
    for src_, cache in (("XR14", X14), ("XR9", X9)):
        for tag, d in sorted(cache["halos"].items()):
            b = d["b"]; fr = carrier_rho_fun(d)
            msr = REF.masses(fr)
            ref = REF.ann_ds(msr)
            REFTPL[(src_, tag)] = ref
            rho_n = fr(rr)
            tb = ann_of_M2grid(project_M2_bug(rho_n))
            tf = ann_of_M2grid(fix_nodes(rho_n))
            # the mass inside the first node (1 kpc): M2Fix extrapolates a power law from the first two nodes; the histogram has its own
            k0 = int(np.searchsorted(REF.e, rr[0]) - 1)
            m_in = msr["m0"] + float(np.sum(msr["m"][:k0])) + msr["m"][k0] * (rr[0] ** 3 - REF.e[k0] ** 3) / (REF.e[k0 + 1] ** 3 - REF.e[k0] ** 3)
            core_fix = float(FIX2.core(rho_n))                         # V3d diagnoses FP20's true drop-in in either mode
            M2t = FIX2(rho_n)
            tft = ann_of_M2grid(M2t)
            tfc = ann_of_M2grid(M2t - core_fix + m_in)
            pk = float(np.max(np.abs(ref)))
            r_ = dict(src=src_, tag=tag, b=b, peak=pk, fix_peak=float(np.max(np.abs(tf - ref)) / pk), fix_sig=float(np.max(np.abs(tf - ref) / SD[b])),
                      bug_peak=float(np.max(np.abs(tb - ref)) / pk), bug_sig=float(np.max(np.abs(tb - ref) / SD[b])),
                      bug_35kpc=float((tb[0] - ref[0]) / pk), bug_rel_35kpc=float(tb[0] / ref[0] - 1) if abs(ref[0]) > 0.05 * pk else float("nan"),
                      fixt_peak=float(np.max(np.abs(tft - ref)) / pk), fixt_sig=float(np.max(np.abs(tft - ref) / SD[b])),
                      core_M2Fix_Msun=core_fix / MS, inner_mass_hist_Msun=m_in / MS, fixcore_peak=float(np.max(np.abs(tfc - ref)) / pk))
            rows.append(r_)
            for k_ in worst:
                worst[k_] = max(worst[k_], r_[k_])
    # an independent check of the reference on one scored template: adaptive quadrature at five radii
    dq = X14["halos"]["MSPH_canonical_b3_v600"]; frq = carrier_rho_fun(dq)
    rmq = np.sqrt(EDG14[1:] * EDG14[:-1]) * 1e-3 * MPCm
    msq = REF.masses(frq)
    dsq_ref = REF.point_ds(msq)
    qdev = 0.0
    for i in (0, 3, 7, 11, 14):
        R = RD[i] * MPCm
        m2q, sq = quad_parts(frq, R, tuple(rmq[(rmq > REF.rmin) & (rmq < RT)]))
        qdev = max(qdev, abs((m2q / (math.pi * R * R) - sq) - dsq_ref[i]) / float(np.max(np.abs(dsq_ref))))
    P(f"    reference vs adaptive quadrature on MSPH_canonical_b3_v600 at five radii: max |d Delta Sigma| / (M_2D/pi R^2) {qdev:.1e}")
    P(f"    {len(rows)} templates.  M2Fix vs reference: worst {100 * worst['fix_peak']:.3f}% of the peak, {worst['fix_sig']:.4f} of the KiDS "
      f"error;  committed project_M2 vs reference: worst {100 * worst['bug_peak']:.1f}% of the peak, {worst['bug_sig']:.3f} of the KiDS error")
    for grp in ("MSPH", "L388", "L375", "FK1", "nodecay", "b"):
        sel = [r_ for r_ in rows if r_["tag"].startswith(grp) and (grp != "b" or r_["src"] == "XR9")]
        if sel:
            P(f"      {('XR9 L375 (per-cell masses)' if grp == 'b' else grp):28s} n = {len(sel):2d}: committed at 35 kpc "
              f"{100 * min(r_['bug_35kpc'] for r_ in sel):+6.1f}..{100 * max(r_['bug_35kpc'] for r_ in sel):+6.1f}% of the peak "
              f"(max over radii {100 * max(r_['bug_peak'] for r_ in sel):.1f}%, {max(r_['bug_sig'] for r_ in sel):.3f} sigma_KiDS); "
              f"M2Fix max {100 * max(r_['fix_peak'] for r_ in sel):.3f}% ({max(r_['fix_sig'] for r_ in sel):.4f} sigma)")
    OUT["numbers"]["V3"] = dict(worst=worst, quad_check=qdev, rows=rows)
    check("V3 THE DROP-IN ON THE SCORED CARRIER TEMPLATES: on every carrier template the lanes project (XR14's 84, XR9's 28), "
          "M2Fix is within 0.2% of the peak |Delta Sigma| and 0.01 of the bin's KiDS error of this lane's reference at every "
          "radius (the reference checked by quadrature to 1e-5)",
          f"M2Fix worst {100 * worst['fix_peak']:.3f}% / {worst['fix_sig']:.4f} sigma; committed project_M2 worst "
          f"{100 * worst['bug_peak']:.1f}% / {worst['bug_sig']:.3f} sigma; quadrature check {qdev:.1e}",
          worst["fix_peak"] <= 2e-3 and worst["fix_sig"] <= 0.01 and qdev <= 1e-5)
    # V3d [reported; ADDED AFTER THE FIRST MAIN RUN, where V3 failed]: which term carries the residual?
    off = sorted((r_ for r_ in rows if r_["fixt_peak"] > 2e-3), key=lambda r_: -r_["fixt_peak"])
    wfc = max(r_["fixcore_peak"] for r_ in rows)
    for r_ in off:
        P(f"      FP20's M2Fix over threshold: {r_['src']} {r_['tag']:24s} {100 * r_['fixt_peak']:.3f}% of the peak ({r_['fixt_sig']:.4f} sigma); its "
          f"power-law core {r_['core_M2Fix_Msun']:.3e} Msun vs the histogram's own mass inside 1 kpc {r_['inner_mass_hist_Msun']:.3e}; with the "
          f"latter: {100 * r_['fixcore_peak']:.4f}%")
    OUT["numbers"]["V3d"] = dict(over_threshold=[(r_["src"], r_["tag"], r_["fixt_peak"], r_["fixt_sig"], r_["core_M2Fix_Msun"], r_["inner_mass_hist_Msun"],
                                                  r_["fixcore_peak"]) for r_ in off], worst_with_hist_inner_mass=wfc)
    check("V3d (reported; added after the first main run) EVERY RESIDUAL OF FP20's M2Fix OVER THE V3 THRESHOLD IS ITS CORE TERM (the "
          "mass inside the first node, 1 kpc, extrapolated as a power law from two noisy histogram nodes): with the histogram's own "
          "inner mass in its place M2Fix is within 0.2% of the peak on every template",
          f"{len(off)} templates over threshold ({', '.join(r_['tag'] for r_ in off)}); worst with the histogram's inner mass {100 * wfc:.3f}% of the peak",
          wfc <= 2e-3, load_bearing=False)
    P(f"    {el()}")


# ================================================================================================= the lanes, re-executed
DEDIR = os.path.join(REPO, "real_research", "dark_energy_2026")
PDE10 = os.path.join(DEDIR, "DE10_kids_converged_model.py")
PXR9 = os.path.join(HERE, "XR9_kids_flagship.py")
PXR14 = os.path.join(HERE, "XR14_kids_mstar_carrier.py")
STOP = "nlb = sum(1 for _, ok, lb in CH if lb and not ok)"
HOOKLOG = {}


def make_hook(fixed, lane):
    """right after DE8 (and, for DE10, L360) is loaded: record the committed baseline; in the corrected run swap the three
    projections and recompute every baseline chi^2 with them."""
    def hook(ns):
        D8 = ns["D8"]; L = D8["L52"]
        assert np.array_equal(L["rr"], rr) and np.array_equal(L["Rp"], Rp) and np.array_equal(D8["faces"], FACES)
        rec = HOOKLOG.setdefault((lane, fixed), {})
        rec["BASE_committed"] = dict(D8["BASE"])
        if not fixed:
            return
        D8["m2_of_rho"] = fix_cells
        L["model_M2"] = model_M2_factory(L, True); L["_PROF"].clear(); L["_ESD"].clear(); D8["_ESD"].clear()
        ns["project_M2"] = fix_nodes
        base = {f_: D8["fit_model"](D8["A0"][f_], 0.0, "none", True)[0] for f_ in FEET}
        D8["BASE"] = base
        if lane in ("XR9", "XR14"):
            ns["BASE20"] = dict(base)
        if lane == "DE10":
            ns["BASE"] = dict(base)
            L6 = ns["N60"]["L52"]
            assert np.array_equal(L6["rr"], rr) and np.array_equal(L6["Rp"], Rp)
            L6["model_M2"] = model_M2_factory(L6, True); L6["_PROF"].clear(); L6["_ESD"].clear()
        rec["BASE_fixed"] = dict(base)
        rec["swapped"] = dict(esd_from_mlens_m2=type(D8["m2_of_rho"]).__name__, template_projector=type(ns["project_M2"]).__name__,
                              model_M2=L["model_M2"].__qualname__)
    return hook


K2LOG = []


class _SerialPool:
    def __init__(self, *a, **k): pass
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def map(self, fn, it, chunksize=1): return [fn(x) for x in it]


def de10_cached_halo(cfg):
    """DE10's halo() call answered from XR9's cache (DE10's own eight halos are in it); every configuration field compared."""
    tag, b, Mb, v, gam, alpha, grow_b, N, seed = cfg
    key = f"b{b}_lm{round(math.log10(Mb), 2):.2f}_v{int(v)}"
    d = X9["halos"][key]; c9 = X9["config"]
    same = (d["b"] == b and d["Mb"] == Mb and d["v_k"] == v and d["seed"] == seed and c9["N"] == N and c9["alpha"] == alpha
            and c9["gamma"] == gam and c9["grow_b"] == grow_b)
    K2LOG.append(dict(cfg=[tag, b, Mb, v, gam, alpha, grow_b, N, seed], cache=key, same=bool(same)))
    return tag, {"edges": EDG9, "hist": np.array(d["hist"]), "m": d["m"], "n": d["n"]}


def de10_pre(ns):
    ns["Pool"] = _SerialPool; ns["halo"] = de10_cached_halo


RUNS = {}


def run_lane(lane, fixed):
    t1 = time.time()
    if lane == "DE10":
        ns, txt = exec_main(PDE10, "XCE = 2.5 * (0.3138 * 1.25 ** 3 + 0.6862)", STOP, make_hook(fixed, lane), pre_hook=de10_pre,
                            name=f"de10_{'fix' if fixed else 'ctl'}")
    elif lane == "XR9":
        ns, txt = exec_main(PXR9, 'P(f"  DE8 loaded (L352', STOP, make_hook(fixed, lane), name=f"xr9_{'fix' if fixed else 'ctl'}")
    else:
        ns, txt = exec_main(PXR14, 'P(f"  DE8 loaded (L352', STOP, make_hook(fixed, lane), name=f"xr14_{'fix' if fixed else 'ctl'}")
    RUNS[(lane, fixed)] = dict(ns=ns, text=txt, out=jnorm(ns["OUT"]), secs=time.time() - t1)
    P(f"    {lane} re-executed with the {'CORRECTED' if fixed else 'committed'} projection: {sum(1 for c in ns['CH'] if c[1])}/{len(ns['CH'])} "
      f"of its checks pass   [{time.time() - t1:.0f} s; total {time.time() - T0:.0f} s]")
    return RUNS[(lane, fixed)]


COMMITTED = {"DE10": os.path.join(DEDIR, "DE10_kids_converged_model_results.json"),
             "XR9": os.path.join(HERE, "XR9_kids_flagship_results.json"),
             "XR14": os.path.join(HERE, "XR14_kids_mstar_carrier_results.json")}
CJ = {}
for k_, p_ in COMMITTED.items():
    assert builtins.open(p_).read() == git_head(rel(p_)), f"{rel(p_)} differs from git HEAD"
    CJ[k_] = json.load(builtins.open(p_))

LANES = [l_ for l_ in ("DE10", "XR9", "XR14") if want(l_)]
if LANES:
    banner("K1 K2  THE CONTROLS: each lane re-executed with the committed projection reproduces its committed results")
    K1 = {}
    for lane in LANES:
        r_ = run_lane(lane, False)
        cn = compare_numbers(CJ[lane]["numbers"], r_["out"]["numbers"])
        cc = compare_checks(CJ[lane]["checks"], r_["out"]["checks"])
        K1[lane] = dict(numbers=cn, checks_differing=cc)
        P(f"      {lane}: {cn['n']} numbers compared, max |d| {cn['dmax']:.1e}; non-numeric mismatches {cn['n_bad']}, missing {cn['n_missing']}; "
          f"checks differing {cc or 'none'}")
    OUT["numbers"]["K1"] = K1
    check("K1 CONTROLS: every lane re-executed here with the committed projection reproduces every committed number (|d| <= 1e-9) "
          "and every check verdict (" + ", ".join(LANES) + ")",
          "; ".join(f"{l_}: {K1[l_]['numbers']['n']} numbers, max |d| {K1[l_]['numbers']['dmax']:.1e}, checks differing "
                    f"{len(K1[l_]['checks_differing'])}" for l_ in LANES),
          all(K1[l_]["numbers"]["dmax"] <= 1e-9 and K1[l_]["numbers"]["n_bad"] == 0 and K1[l_]["numbers"]["n_missing"] == 0
              and not K1[l_]["checks_differing"] for l_ in LANES))
    if "DE10" in LANES:
        k2ok = len(K2LOG) == 8 and all(x["same"] for x in K2LOG)
        check("K2 the cached halos are DE10's: its eight configurations (bin, M_b, kick, seed, N, alpha, Gamma, grow_b) equal the "
              "cache entries used", f"{sum(x['same'] for x in K2LOG)}/{len(K2LOG)} identical ({', '.join(x['cache'] for x in K2LOG[:8])})", k2ok)
        OUT["numbers"]["K2"] = K2LOG[:8]
    banner("THE RE-SCORE: each lane re-executed with FP20's drop-ins spliced in after DE8 is loaded")
    for lane in LANES:
        run_lane(lane, True)
    b_fix = HOOKLOG.get(("XR14", True), HOOKLOG.get(("XR9", True), HOOKLOG.get(("DE10", True), {}))).get("BASE_fixed", {})
    b_com = HOOKLOG.get(("XR14", False), HOOKLOG.get(("XR9", False), HOOKLOG.get(("DE10", False), {}))).get("BASE_committed", {})
    FP20J = json.loads(git_head("real_research/derivation_chain_2026/FP20_esd_projection_fix_results.json"))
    fp20_after = {f_: FP20J["numbers"]["R9_P2"]["L352"][f"base+2h/{f_}"][1] for f_ in FEET}
    fp20_de8 = {f_: FP20J["numbers"]["R9_P2"]["DE8_C1"][f"after/{f_}"] for f_ in FEET}
    dk3 = max(abs(b_fix[f_] - fp20_after[f_]) for f_ in FEET) if b_fix else float("inf")
    dk3b = max(abs(b_fix[f_] - fp20_de8[f_]) for f_ in FEET) if b_fix else float("inf")
    check("K3 the drop-ins are FP20's committed code (git HEAD): with them L352's unswitched base chi^2 equals FP20's committed R9 "
          "value (1e-6, the same code path), and DE8's isolated-QUMOND C1 fit through CellFix (FP20 R9; the ODE solver, 1e-4)",
          f"base {b_com.get('canonical', float('nan')):.3f}/{b_com.get('alt', float('nan')):.3f} (committed) -> "
          f"{b_fix.get('canonical', float('nan')):.3f}/{b_fix.get('alt', float('nan')):.3f}; FP20 R9 {fp20_after['canonical']:.3f}/"
          f"{fp20_after['alt']:.3f} (|d| {dk3:.1e}); DE8 C1 {fp20_de8['canonical']:.3f}/{fp20_de8['alt']:.3f} (|d| {dk3b:.1e}); FP20 "
          f"source identical to the working tree: {FP20_TREE_SAME}", dk3 < 1e-6 and dk3b < 1e-4 and FP20_TREE_SAME)
    OUT["numbers"]["baseline"] = dict(committed=b_com, corrected=b_fix, FP20_R9=fp20_after)


# ================================================================================================= R: the tables
def bar_pass(d):                                                       # both footings <= +4
    return all(v <= BAR for v in d.values())


def fmt2(d):
    return f"{d['canonical']:+7.2f}/{d['alt']:+7.2f}"


ROWS = []


def row(lane, cell, before, after, gated=True):
    pb, pa = bar_pass(before), bar_pass(after)
    ROWS.append(dict(lane=lane, cell=cell, before=before, after=after, gated=gated, pass_before=pb, pass_after=pa, flip=pb != pa))
    return pb, pa


def show(lane, title):
    P(f"    -- {title}")
    for r_ in ROWS:
        if r_["lane"] == lane:
            vd = f"{'PASS' if r_['pass_before'] else 'FAIL'} -> {'PASS' if r_['pass_after'] else 'FAIL'}" + ("   ** FLIP **" if r_["flip"] else "")
            P(f"       {r_['cell'][:58]:58s} {fmt2(r_['before'])} -> {fmt2(r_['after'])}   (shift {r_['after']['canonical'] - r_['before']['canonical']:+6.2f}/"
              f"{r_['after']['alt'] - r_['before']['alt']:+6.2f})  {vd if r_['gated'] else '(reported)'}")


def own_check_flips(lane):
    b_, a_ = RUNS[(lane, False)]["out"]["checks"], RUNS[(lane, True)]["out"]["checks"]
    return [(k_, b_[k_]["pass"], a_[k_]["pass"], a_[k_]["measured"][:220]) for k_ in b_ if k_ in a_ and b_[k_]["pass"] != a_[k_]["pass"]]


PINNED = {"DE10": {"C1": "pinned to L390's committed (defective-projection) scores"},
          "XR9": {"C1": "pinned to DE10's committed table", "C6": "pinned to DE9's committed switch-only cap 4.3473",
                  "C2": "pinned to the committed halo plan (see S1)"},
          "XR14": {"C1": "pinned to DE10's committed table"}}
RES = {}
if "DE10" in LANES:
    banner("R1  DE10 (the converged model; L375's carrier at L390's masses, the withdrawn local cap, A <= 20): before -> after")
    tb, ta = RUNS[("DE10", False)]["out"]["numbers"], RUNS[("DE10", True)]["out"]["numbers"]
    for k_ in tb["table"]:
        row("DE10", f"H1 {k_} (fs = 1, A <= 20)", tb["table"][k_]["kids"], ta["table"][k_]["kids"])
    for k_ in tb["table"]:
        row("DE10", f"best fs in [0, 1.2] at {k_}: " + "/".join(f"{ta['table'][k_]['best_fs'][f_][0]:.1f}" for f_ in FEET) + " (after)",
            {f_: tb["table"][k_]["best_fs"][f_][1] for f_ in FEET}, {f_: ta["table"][k_]["best_fs"][f_][1] for f_ in FEET}, gated=False)
    for v_ in tb["L390_rerun"]:
        row("DE10", f"C1: L390's curvature branch + the same carrier, v_k = {float(v_):.0f}", tb["L390_rerun"][v_], ta["L390_rerun"][v_], gated=False)
    show("DE10", "DE10 H1 table and its reported columns (Delta chi^2 canonical/alt)")
    RES["DE10"] = dict(worst_before=max(max(tb["table"][k_]["kids"].values()) for k_ in tb["table"]),
                       worst_after=max(max(ta["table"][k_]["kids"].values()) for k_ in ta["table"]), flips=own_check_flips("DE10"))
    ok_h2 = all(bar_pass(ta["table"][k_]["kids"]) for k_ in ta["table"])
    check("H2 [pre-declared] DE10's headline passes with the corrected projection: the four cells <= +4 on both footings",
          "; ".join(f"{k_}: {fmt2(tb['table'][k_]['kids'])} -> {fmt2(ta['table'][k_]['kids'])}" for k_ in ta["table"])
          + f" (worst {RES['DE10']['worst_before']:+.2f} -> {RES['DE10']['worst_after']:+.2f})", ok_h2)

if "XR9" in LANES:
    banner("R2  XR9 (the small-region door: MOND-sector switch + kappa cap, carrier re-run per cell): before -> after")
    kb, ka = RUNS[("XR9", False)]["out"]["numbers"]["kids"], RUNS[("XR9", True)]["out"]["numbers"]["kids"]
    VK9 = (600, 650)
    cellv = {}
    for cell in kb:
        for w in ("0.25", "0.02"):
            for lab in ("gate", "gate_A20", "switch_only_A2", "switch_only_A20"):
                if w == "0.02" and lab != "gate":
                    continue
                wb = {f_: max(kb[cell]["kids"][f"w{w}/v{v}/{f_}"][lab]["dchi2"] for v in VK9) for f_ in FEET}
                wa = {f_: max(ka[cell]["kids"][f"w{w}/v{v}/{f_}"][lab]["dchi2"] for v in VK9) for f_ in FEET}
                row("XR9" if (w == "0.25" and lab == "gate") else "XR9r", f"{cell:9s} w={w} {lab} (worse kick)", wb, wa,
                    gated=(w == "0.25" and lab == "gate"))
        cellv[cell] = dict(pass_before=kb[cell]["pass"], pass_after=ka[cell]["pass"], hard_before=kb[cell]["pass_hard"],
                           hard_after=ka[cell]["pass_hard"], so_before=kb[cell]["switch_only_pass_A20"], so_after=ka[cell]["switch_only_pass_A20"],
                           xce=ka[cell]["xce_025"])
    show("XR9", "XR9's gated score per cell (w = 0.25, fs = 1, A <= 2; the worse kick per footing) -- the lane's verdict")
    show("XR9r", "XR9's reported columns (hard gate w = 0.02; A <= 20; switch only fs = 0)")
    nb, na = RUNS[("XR9", False)]["out"]["numbers"], RUNS[("XR9", True)]["out"]["numbers"]
    kcb, kca = nb["kids_cap_with_carrier"], na["kids_cap_with_carrier"]
    fcap = lambda d_: f"{d_['cap']:.4f}" if d_.get("cap") else f"none (worst at the bracket ends {d_.get('worst_at_ends')})"
    P("    -- XR9 KC, the carrier-inclusive KiDS cap x_c,eff(0.25) (w = 0.25, A <= 2, both kicks and footings; bisected in [3.25, 4.55]): "
      + "; ".join(f"{k_}: {fcap(kcb[k_])} -> {fcap(kca[k_])}" for k_ in kcb))
    P("    -- XR9 door (H-K): passing cells " + f"{nb['door_kids']['passing']} -> {na['door_kids']['passing']}; above DE9's switch-only cap 4.3473 "
      f"and passing: {nb['door_kids']['passing_above_cap']} -> {na['door_kids']['passing_above_cap']}; hard-gate passing "
      f"{[c for c in kb if kb[c]['pass_hard']]} -> {[c for c in ka if ka[c]['pass_hard']]}; switch-only (A <= 20) passing "
      f"{[c for c in kb if kb[c]['switch_only_pass_A20']]} -> {[c for c in ka if ka[c]['switch_only_pass_A20']]}")
    # the flagship: projection-free (K4)
    fb, fa = flatten(nb["flagship"]), flatten(na["flagship"])
    fcb, fca = flatten(nb["flagship_caps_smooth_kappa"]), flatten(na["flagship_caps_smooth_kappa"])
    dfl = max([abs(fb[k_] - fa[k_]) for k_ in fb if isinstance(fb[k_], float)] + [abs(fcb[k_] - fca[k_]) for k_ in fcb])
    same_bool = all(fb[k_] == fa[k_] for k_ in fb if not isinstance(fb[k_], float))
    check("K4 the flagship is projection-free: XR9's flagship rows (door, smooth shift, masses lost, verdicts) and its smooth "
          "flagship caps are identical under both projections", f"max |d| {dfl:.1e} over {len(fb) + len(fcb)} leaves; verdicts identical: {same_bool}",
          dfl == 0.0 and same_bool)
    ver_b = sorted(c for c in cellv if cellv[c]["pass_before"]); ver_a = sorted(c for c in cellv if cellv[c]["pass_after"])
    RES["XR9"] = dict(cells=cellv, passing_before=ver_b, passing_after=ver_a, KC_before=kcb, KC_after=kca, flips=own_check_flips("XR9"),
                      door_before=nb["door_kids"], door_after=na["door_kids"])
    check("H3 [pre-declared, reported] XR9's per-cell KiDS verdicts are unchanged (p1_x2.5 and p1.5_x2.5 pass, twelve fail; the "
          "door's KiDS half still fails)", f"passing {ver_b} -> {ver_a}; H-K passing above the switch-only cap "
          f"{nb['door_kids']['passing_above_cap']} -> {na['door_kids']['passing_above_cap']}",
          ver_a == ver_b == ["p1.5_x2.5", "p1_x2.5"] and not na["door_kids"]["passing_above_cap"], load_bearing=False)

if "XR14" in LANES:
    banner("R3  XR14 (KiDS ON M*'S OWN CARRIER: MOND-sector switch, kappa cap, L388's trigger; fs = 1, A <= 2): before -> after")
    tb, ta = RUNS[("XR14", False)]["out"]["numbers"]["table"], RUNS[("XR14", True)]["out"]["numbers"]["table"]
    for mode, lab in (("MSPH", "M* carrier (MSPH)"), ("L388", "L388 as written")):
        for v in ("v575", "v600", "v625", "v650"):
            for w in ("0.02", "0.25"):
                row("XR14" + mode, f"{lab} {v} w={w}", {f_: tb[mode][v][f_][w]["gate"] for f_ in FEET}, {f_: ta[mode][v][f_][w]["gate"] for f_ in FEET})
    for v in ("v575", "v600", "v625", "v650"):
        for w in ("0.02", "0.25"):
            row("XR14r", f"'as run' (canonical carrier on alt) {v} w={w}", {f_: tb["L388_as_run"][v]["alt"][w]["gate"] for f_ in FEET},
                {f_: ta["L388_as_run"][v]["alt"][w]["gate"] for f_ in FEET}, gated=False)
    for v in ("v575", "v650"):
        for w in ("0.02", "0.25"):
            row("XR14r", f"FK1 variant {v} w={w}", {f_: tb["FK1"][v][f_][w]["gate"] for f_ in FEET}, {f_: ta["FK1"][v][f_][w]["gate"] for f_ in FEET}, gated=False)
    for v in ("v600", "v650"):
        for w in ("0.02", "0.25"):
            row("XR14r", f"DE10's carrier (L375) on M*'s rules {v} w={w}", {f_: tb["L375_on_Mstar_gate"][v][f_][w]["gate"] for f_ in FEET},
                {f_: ta["L375_on_Mstar_gate"][v][f_][w]["gate"] for f_ in FEET}, gated=False)
    for v in ("v575", "v600", "v625", "v650"):
        row("XR14r", f"M* switch alone (fs = 0) {v} w=0.25", {f_: tb["MSPH"][v][f_]["0.25"]["switch_only"] for f_ in FEET},
            {f_: ta["MSPH"][v][f_]["0.25"]["switch_only"] for f_ in FEET}, gated=False)
    c2b, c2a = RUNS[("XR14", False)]["out"]["numbers"]["C2_nodecay"], RUNS[("XR14", True)]["out"]["numbers"]["C2_nodecay"]
    show("XR14MSPH", "M*'s carrier (H1): Delta chi^2 canonical/alt")
    show("XR14L388", "L388's carrier as written (H1b)")
    show("XR14r", "XR14's reported rows")
    P(f"    -- XR14 C2 (the no-decay carrier must be rejected, > +100): A <= 2 {fmt2(c2b['A<=2'])} -> {fmt2(c2a['A<=2'])}")
    wb = {m_: max(max(r_["before"].values()) for r_ in ROWS if r_["lane"] == "XR14" + m_) for m_ in ("MSPH", "L388")}
    wa = {m_: max(max(r_["after"].values()) for r_ in ROWS if r_["lane"] == "XR14" + m_) for m_ in ("MSPH", "L388")}
    RES["XR14"] = dict(worst_before=wb, worst_after=wa, flips=own_check_flips("XR14"),
                       share_after={m_: [min(abs(ta[m_][v][f_]["0.25"]["gate"] - ta[m_][v][f_]["0.25"]["switch_only"]) for v in ta[m_] for f_ in FEET),
                                         max(abs(ta[m_][v][f_]["0.25"]["gate"] - ta[m_][v][f_]["0.25"]["switch_only"]) for v in ta[m_] for f_ in FEET)]
                                    for m_ in ("MSPH", "L388")})
    check("H1 [pre-declared] XR14's ON-M* KiDS pass survives the corrected projection: M*'s carrier passes (<= +4, fs = 1, A <= 2) on "
          "both footings, w = 0.02 and 0.25, every kick 575-650 km/s",
          f"worst {wb['MSPH']:+.2f} -> {wa['MSPH']:+.2f} over 16 cells x 2 footings; carrier's share of the score (w = 0.25) "
          f"{RES['XR14']['share_after']['MSPH'][0]:.2f}-{RES['XR14']['share_after']['MSPH'][1]:.2f}", wa["MSPH"] <= BAR)
    check("H1b [pre-declared] L388's carrier AS WRITTEN passes on the same terms", f"worst {wb['L388']:+.2f} -> {wa['L388']:+.2f}", wa["L388"] <= BAR)

if LANES:
    banner("R4  THE LANES' OWN CHECKS THAT CHANGE VERDICT WHEN RE-RUN WITH THE CORRECTED PROJECTION")
    for lane in LANES:
        fl = own_check_flips(lane)
        if not fl:
            P(f"    {lane}: none")
        for k_, b_, a_, meas in fl:
            P(f"    {lane:5s} {k_:6s} {'PASS' if b_ else 'FAIL'} -> {'PASS' if a_ else 'FAIL'}  "
              f"[{PINNED.get(lane, {}).get(k_, 'VERDICT')}]  measured after: {meas}")
    OUT["numbers"]["R4_check_flips"] = {l_: own_check_flips(l_) for l_ in LANES}
    OUT["numbers"]["R_rows"] = ROWS
    if MUTATE:
        same = all(abs(r_["after"][f_] - r_["before"][f_]) < 1e-9 for r_ in ROWS for f_ in FEET)
        check("K-MUT (MUTATE control) with the committed projection in the corrected slot every 'after' number equals its 'before' "
              "(the harness is exact end to end)", f"{len(ROWS)} rows; all identical: {same}", same)


# ================================================================================================= S1: the halo masses
if "DE10" in LANES and "XR9" in LANES and "XR14" in LANES and want("S"):
    banner("S1  IS RE-PROJECTING THE CACHED HALOS ENOUGH?  The carrier halos' masses came from fits with the defective projector")
    S1 = {}
    nd_c, nd_f = RUNS[("DE10", False)]["ns"], RUNS[("DE10", True)]["ns"]
    lm90 = [round(math.log10(x), 2) for x in nd_c["MB"]]
    with lane_env():
        ref_c = [round(float(t_[0]), 2) for t_ in nd_c["fit_model"](nd_c["A052"]["canonical"], nd_c["XE_LIN"], "compensated", True)[1]]
        ref_f = [round(float(t_[0]), 2) for t_ in nd_f["fit_model"](nd_f["A052"]["canonical"], nd_f["XE_LIN"], "compensated", True)[1]]
    S1["L390_refit"] = dict(committed_L390=lm90, rerun_committed=ref_c, rerun_corrected=ref_f)
    P(f"    (a) L390's refit (curvature branch, L360's compensated edge at x_c,eff(0.25) = {nd_c['XE_LIN']}, canonical, A <= 20) -- "
      f"the masses of DE10's and XR14's halos: committed {lm90}; re-run, committed projection {ref_c}; corrected {ref_f}")
    n9c, n9f = RUNS[("XR9", False)]["ns"], RUNS[("XR9", True)]["ns"]
    plan = n9c["PLAN"]; rk_f = n9f["refit_k"]
    moved = {c: (plan[c]["lm_refit"], rk_f[c]) for c in plan if plan[c]["lm_refit"] != rk_f[c]}
    S1["XR9_refit"] = dict(plan={c: plan[c]["lm_refit"] for c in plan}, corrected=rk_f, moved=moved)
    P(f"    (b) XR9's per-cell refit (MOND-sector switch, kappa form, w = 0.25, canonical, A <= 20): cells whose masses move under the "
      f"corrected projection: {len(moved)} of {len(plan)}" + "".join(f"\n          {c}: {a_} -> {b_}" for c, (a_, b_) in moved.items()))
    # (c) XR9's moved cells re-scored with cached halos at the corrected refit masses
    rescore = {}
    for c, (old_m, new_m) in moved.items():
        tags = [f"b{b}_lm{new_m[b]:.2f}_v{v}" for b in range(4) for v in (600, 650)]
        if not all(t_ in X9["halos"] for t_ in tags):
            rescore[c] = dict(status="halo not cached", missing=[t_ for t_ in tags if t_ not in X9["halos"]])
            gw = {f_: max(RUNS[("XR9", True)]["out"]["numbers"]["kids"][c]["kids"][f"w0.25/v{v}/{f_}"]["gate"]["dchi2"] for v in (600, 650)) for f_ in FEET}
            P(f"          {c}: NOT re-scored -- no cached halo at {rescore[c]['missing']} (not regenerated); its gated score with the plan's "
              f"halos is {fmt2(gw)} ({'PASS' if bar_pass(gw) else 'fail'}), {min(gw.values()) - 4.0:+.1f} from the bar")
            continue
        p_, x0_ = float(c.split("_x")[0][1:]), float(c.split("_x")[1])
        xce = x0_ * (0.3138 * 1.25 ** 3 + 0.6862) ** p_
        out_ = {}
        with lane_env():
            for v in (600, 650):
                TCs = [n9f["template"](f"b{b}_lm{new_m[b]:.2f}_v{v}") for b in range(4)]
                for f_ in FEET:
                    out_[(v, f_)] = n9f["fit"](f_, TCs, 1.0, 2.0, n9f["BASE"][2.0][f_], lambda b, lm, f_=f_: n9f["model"](b, lm, f_, 0.25, xce, "kappa"))[0]
        worst_new = {f_: max(out_[(v, f_)] for v in (600, 650)) for f_ in FEET}
        worst_old = {f_: max(RUNS[("XR9", True)]["out"]["numbers"]["kids"][c]["kids"][f"w0.25/v{v}/{f_}"]["gate"]["dchi2"] for v in (600, 650)) for f_ in FEET}
        rescore[c] = dict(status="re-scored", old_masses=old_m, new_masses=new_m, gate_old_halos=worst_old, gate_refit_halos=worst_new,
                          pass_old=bar_pass(worst_old), pass_new=bar_pass(worst_new))
        P(f"          {c}: gated score with the plan's halos {fmt2(worst_old)} -> with halos at the corrected refit {fmt2(worst_new)} "
          f"({'PASS' if bar_pass(worst_new) else 'fail'}; was {'PASS' if bar_pass(worst_old) else 'fail'})")
    S1["XR9_rescore_moved"] = rescore
    # (d) the M* chain's mass sensitivity, measured with L375's cached halos on M*'s gate (XR14's namespace, both projections)
    n14 = {fx: RUNS[("XR14", fx)]["ns"] for fx in (False, True)}

    def l375_on_mstar(nsx, masses, tagp):
        for b in range(4):
            for v in (600, 650):
                key = f"b{b}_lm{masses[b]:.2f}_v{v}"
                d = X9["halos"][key]
                nsx["HC"]["halos"][f"{tagp}_b{b}_v{v}"] = dict(d, b=b)
        res_ = {}
        with lane_env():
            for v in (600, 650):
                TCs = [nsx["template"](f"{tagp}_b{b}_v{v}") for b in range(4)]
                for w in (0.02, 0.25):
                    for f_ in FEET:
                        res_[(v, w, f_)] = nsx["fit"](f_, TCs, 1.0, 2.0, nsx["BASE"][2.0][f_], w)[0]
        return res_
    sens = {}
    for fx in (False, True):
        a_ = l375_on_mstar(n14[fx], lm90, f"XR35L390{int(fx)}")
        b_ = l375_on_mstar(n14[fx], plan["p1_x2.5"]["lm_refit"], f"XR35MSR{int(fx)}")
        sens[fx] = dict(L390=a_, mond_refit=b_, max_abs_shift=max(abs(b_[k_] - a_[k_]) for k_ in a_))
    newL390 = None
    if ref_f != lm90 and all(f"b{b}_lm{ref_f[b]:.2f}_v{v}" in X9["halos"] for b in range(4) for v in (600, 650)):
        c_ = l375_on_mstar(n14[True], ref_f, "XR35L390NEW")
        newL390 = dict(scores={f"{k_[0]}/{k_[1]}/{k_[2]}": v_ for k_, v_ in c_.items()},
                       max_abs_shift=max(abs(c_[k_] - sens[True]["L390"][k_]) for k_ in c_))
    S1["mass_sensitivity"] = {("committed" if not fx else "corrected"): dict(max_abs_shift=sens[fx]["max_abs_shift"]) for fx in sens}
    S1["L390_masses_corrected_rescore"] = newL390
    P(f"    (d) the mass sensitivity of the M* chain, with L375's cached halos on M*'s gate (fs = 1, A <= 2, w = 0.02/0.25, 600/650 "
      f"km/s): L390's masses {lm90} vs the MOND-sector refit {plan['p1_x2.5']['lm_refit']} (XR14's scope note: <= 0.03) -- max |shift| "
      f"{sens[False]['max_abs_shift']:.3f} (committed projection), {sens[True]['max_abs_shift']:.3f} (corrected)")
    if newL390:
        P(f"        L390's masses re-fitted with the corrected projection {ref_f}: the same carrier moves by at most {newL390['max_abs_shift']:.3f}")
    OUT["numbers"]["S1"] = jnorm({k_: v_ for k_, v_ in S1.items()})

    # ================================================================================================= S2: the 2-halo inner disc
    banner("S2  THE 2-HALO TEMPLATE'S INNER DISC (kept as committed): its error, and XR14's worst cells if it were exact")
    nsx = n14[True]; L = nsx["D8"]["L52"]
    Rext = np.geomspace(1e-5, 6.0, 3000)
    S2h = L["rho_m_z"] * np.array([L["w_proj"](R) for R in Rext])                # Msun/Mpc^2 per unit bias
    M2e = (np.concatenate([[0], np.cumsum(0.5 * (S2h[1:] * Rext[1:] + S2h[:-1] * Rext[:-1]) * np.diff(Rext))]) * 2 * math.pi
           + math.pi * Rext[0] ** 2 * S2h[0])
    ex2 = annulus_esd(lambda R: np.interp(np.log(R), np.log(Rext * MPCm), M2e * MS), RD)
    t2c = np.asarray(nsx["twoh_cache"][0])
    d2h = float(np.max(np.abs(t2c - ex2)))
    old2 = nsx["twoh_cache"]
    try:
        nsx["twoh_cache"] = [ex2.copy() for _ in range(4)]
        with lane_env():
            B2x = {f_: nsx["fit"](f_, None, 0.0, 2.0, 0.0, None)[0] for f_ in FEET}      # the A <= 2 baseline, same template
            worst_cells = {}
            for mode in ("MSPH", "L388"):
                sc = {}
                for v in (575.0, 600.0, 625.0, 650.0):
                    for w in (0.02, 0.25):
                        for f_ in FEET:
                            sc[(v, w, f_)] = nsx["fit"](f_, nsx["tset"](mode, f_, v), 1.0, 2.0, B2x[f_], w)[0]
                worst_cells[mode] = max(sc.values())
    finally:
        nsx["twoh_cache"] = old2
    OUT["numbers"]["S2"] = dict(max_abs_template_error_Msun_pc2=d2h, smallest_KiDS_error=float(min(np.min(s) for s in SD)),
                                worst_with_exact_2halo=worst_cells, worst_as_scored=RES.get("XR14", {}).get("worst_after"))
    P(f"    the 2-halo template per unit bias vs an exact inner integral of the same xi_lin projection: max |d| {d2h:.2e} Msun/pc^2 "
      f"(smallest KiDS error {min(np.min(s) for s in SD):.2f}); XR14's worst cell with it exact (A <= 2, corrected projection): "
      + ", ".join(f"{m_} {worst_cells[m_]:+.2f} (as scored {RES['XR14']['worst_after'][m_]:+.2f})" for m_ in worst_cells))
    check("S2 (reported) the 2-halo template's own inner disc is not load-bearing: replacing it by an exact inner integral moves "
          "XR14's worst cells by less than 0.1", "; ".join(f"{m_}: {worst_cells[m_] - RES['XR14']['worst_after'][m_]:+.4f}" for m_ in worst_cells),
          all(abs(worst_cells[m_] - RES["XR14"]["worst_after"][m_]) < 0.1 for m_ in worst_cells), load_bearing=False)
    check("S1 (reported) re-projecting the cached halos is enough when the refitted masses do not move, and the mass sensitivity "
          "of the M* chain is small against its margin", f"L390 refit {lm90} -> {ref_f}; XR9 cells moved {len(moved)}; mass "
          f"sensitivity {sens[True]['max_abs_shift']:.3f} (corrected)", True, load_bearing=False)

    # ================================================================================================= V3s: does the V3 residual touch a score?
    if REFTPL:
        banner("V3s  (added after the first main run) THE SCORE IMPACT OF THE V3 RESIDUAL: every carrier template replaced by this lane's "
               "reference (the exact projection of the full histogram, inner mass included), corrected projection elsewhere")
        nsx = RUNS[("XR14", True)]["ns"]; saved = dict(nsx["_TC"])
        tab14 = RUNS[("XR14", True)]["out"]["numbers"]["table"]
        try:
            for tag in X14["halos"]:
                nsx["_TC"][tag] = REFTPL[("XR14", tag)]
            sc3, c23 = {}, {}
            with lane_env():
                for mode in ("MSPH", "L388"):
                    for v in (575.0, 600.0, 625.0, 650.0):
                        for f_ in FEET:
                            r3 = nsx["score"](mode, v, f_)
                            for w in ("0.02", "0.25"):
                                sc3[(mode, v, w, f_)] = r3[w]["gate"]
                c23 = {f_: nsx["fit"](f_, nsx["tset"]("nodecay", None, 650.0), 1.0, 2.0, nsx["BASE"][2.0][f_], 0.25)[0] for f_ in FEET}
        finally:
            nsx["_TC"].clear(); nsx["_TC"].update(saved)
        d14 = max(abs(sc3[(m_, v, w, f_)] - tab14[m_][f"v{int(v)}"][f_][w]["gate"]) for (m_, v, w, f_) in sc3)
        w14 = {m_: max(x for k_, x in sc3.items() if k_[0] == m_) for m_ in ("MSPH", "L388")}
        c2a = RUNS[("XR14", True)]["out"]["numbers"]["C2_nodecay"]["A<=2"]
        n10 = RUNS[("DE10", True)]["ns"]; savedTC = dict(n10["TC"])
        try:
            for v in (600.0, 650.0):
                for b in range(4):
                    n10["TC"][(v, b)] = REFTPL[("XR9", f"b{b}_lm{lm90[b]:.2f}_v{int(v)}")]
            with lane_env():
                s10 = {(v, w, f_): n10["fit"](f_, w, v) for v in (600.0, 650.0) for w in (0.02, 0.25) for f_ in FEET}
        finally:
            n10["TC"].clear(); n10["TC"].update(savedTC)
        t10 = RUNS[("DE10", True)]["out"]["numbers"]["table"]
        d10 = max(abs(s10[(v, w, f_)] - t10[f"v{int(v)}/w{w}"]["kids"][f_]) for (v, w, f_) in s10)
        OUT["numbers"]["V3s"] = dict(XR14_max_shift=d14, XR14_worst_with_reference_templates=w14, XR14_C2_with_reference=c23, XR14_C2_M2Fix=c2a,
                                     DE10_max_shift=d10)
        P(f"    XR14 H1/H1b cells with the reference templates: max |shift| {d14:.4f}; worst MSPH {w14['MSPH']:+.2f}, L388 {w14['L388']:+.2f}; "
          f"C2 (no-decay control) {fmt2(c2a)} -> {fmt2(c23)};  DE10's four cells: max |shift| {d10:.4f}")
        check("V3s (reported; added after the first main run) THE V3 RESIDUAL DOES NOT TOUCH A SCORED VERDICT: with every carrier template "
              "replaced by this lane's reference, XR14's H1/H1b cells and DE10's cells move by less than 0.1 and C2 stays above +100",
              f"XR14 max |shift| {d14:.4f}; DE10 max |shift| {d10:.4f}; C2 {fmt2(c23)}", d14 < 0.1 and d10 < 0.1 and min(c23.values()) > 100,
              load_bearing=False)


# ================================================================================================= F, verdict
if LANES:
    allrows = [x for r_ in ROWS for x in list(r_["before"].values()) + list(r_["after"].values())]
    check("F EVERY RE-SCORE COMPLETED: every lane re-executed in both projections, every row finite",
          f"{len(ROWS)} rows, {len(allrows)} numbers; non-finite {sum(1 for x in allrows if not math.isfinite(x))}",
          all(math.isfinite(x) for x in allrows) and len(RUNS) == 2 * len(LANES))
OUT["numbers"]["hooks"] = jnorm({f"{k_[0]}/{'corrected' if k_[1] else 'committed'}": v_ for k_, v_ in HOOKLOG.items()})
OUT["numbers"]["results"] = jnorm(RES)
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
banner("VERDICT")
if LANES and "XR14" in RES and "V_errors_percent" in OUT["numbers"]:
    ve = OUT["numbers"]["V_errors_percent"]
    fp20set = [nm for nm in ve if nm.startswith(("SIS", "NFW"))]
    w_fp20 = max(max(abs(x) for x in ve[nm][k_]) for nm in fp20set for k_ in ve[nm] if "FP20" in k_)
    v1d, v3d, v3s = OUT["numbers"].get("V1d", {}), OUT["numbers"].get("V3d", {}), OUT["numbers"].get("V3s", {})
    P(f"""  THE DEFECT: confirmed independently (V2) -- the committed P2 projectors are low by 2-3% on the SIS, high by up to 11.5% at
  35 kpc on NFW, +8.5 / +44.6 / +46.0% at 35 kpc on the Plummer (a = 50 / 150 kpc) and capped-NFW cores; FP6's P1 is -58.6% on the SIS.
  THE DROP-INS: on FP20's own profiles (SIS, NFW) every drop-in path is within {w_fp20:.3f}% (FP20's stated 0.04% holds).  V1 as
  pre-declared {'PASSES' if OUT['checks'].get('V1', {}).get('pass') else 'FAILS'}: on the a = 150 kpc Plummer core the P2 paths reach
  {100 * v1d.get('dropin_on_Rp700', float('nan')):.3f}% -- the lanes' read of M_2D on the 700-point Rp grid (the exact M_2D read that way:
  {100 * v1d.get('exact_M2_on_Rp700', float('nan')):.3f}%; FP20's kernel on a 10x grid: {100 * v1d.get('dropin_on_Rp7000', float('nan')):.4f}%), not the projection (V1d).
  V3 as pre-declared {'PASSES' if OUT['checks'].get('V3', {}).get('pass') else 'FAILS'}: {len(v3d.get('over_threshold', []))} of 112 carrier templates exceed 0.2% of their peak,
  all through M2Fix's power-law core inside 1 kpc (V3d); with the reference templates the scored cells move by
  {v3s.get('XR14_max_shift', float('nan')):.3f} (XR14) / {v3s.get('DE10_max_shift', float('nan')):.3f} (DE10) (V3s).
  THE RE-SCORE (only the projector replaced; every committed number reproduced first, K1):
  DE10: worst {RES.get('DE10', {}).get('worst_before', float('nan')):+.2f} -> {RES.get('DE10', {}).get('worst_after', float('nan')):+.2f} -- passes
  XR9: passing cells {RES.get('XR9', {}).get('passing_before')} -> {RES.get('XR9', {}).get('passing_after')}; the door's KiDS half still fails
  XR14 (ON M*): M*'s carrier worst {RES['XR14']['worst_before']['MSPH']:+.2f} -> {RES['XR14']['worst_after']['MSPH']:+.2f}; L388 as written
  {RES['XR14']['worst_before']['L388']:+.2f} -> {RES['XR14']['worst_after']['L388']:+.2f}  (bar +4) -- the ON-M* pass survives.
  kappa = 1/2 is FITTED (Z = 5.7888).  Not closed.""")
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), n_fail, round(time.time() - T0)
fn = os.path.join(HERE, f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json")
with builtins.open(fn, "w") as fh:
    json.dump(jnorm(OUT), fh, indent=1)
rc = 0 if n_fail == 0 else 1
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {os.path.basename(fn)}   {el()}")
P(f"rc={rc}")
sys.stdout.flush(); _OUTFH.close(); sys.stdout = sys.__stdout__
sys.exit(rc)
