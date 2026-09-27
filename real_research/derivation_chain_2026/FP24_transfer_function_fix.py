#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FP24 -- A BUG CORRECTION: THE CHAIN'S LINEAR SPECTRUM MIXES h UNITS.  The hub's XR23 (6b7ab8243) flagged that the chain's
Eisenstein & Hu (1998) no-wiggle transfer function T_EH98 -- first written in the record's L341, copied into FP3, FP6 and FP7,
and run by FP9, FP13, FP14, FP17 and FP19 through FP6's machinery -- is called with k in 1/Mpc but evaluated as if k were in
h/Mpc in one place and in 1/Mpc in another.  This lane pins the error, writes the published form, validates both against
CLASS, and RE-SCORES every committed chain number that depends on the linear spectrum with the corrected function -- same
fits, gates, yardsticks and conventions, only the transfer function swapped (in this lane's own namespace; no committed file
is edited).

THE BUG.  EH98 eqs. (26), (28)-(31), with k in 1/Mpc and the sound horizon s in Mpc:
    q = (k / h) Theta^2 / Gamma_eff,   Gamma_eff = Omega_m h [alpha_G + (1 - alpha_G) / (1 + (0.43 k s)^4)].
  The committed code (FP6:137, FP3:197, FP7:1028; L341 and its record copies) is called as T_EH98(k_h h) and evaluates
    q = k Theta^2 / Gamma_eff          (missing 1/h: q is h = 0.674 times too small)
    ... (0.43 k s / h)^4               (a spurious 1/h: the baryon-suppression step sits at k s = 2.3, not 0.43^-1 = 2.3 h)
  Both errors push power from large to small scales at fixed sigma_8.
THE FIX (two edits per copy, applied to the source text in memory): 0.43 k s / h -> 0.43 k s and q = k ... -> q = (k/h) ....
  The corrected function is the published zero-baryon (no-wiggle) form: it equals colossus's independent implementation to
  machine precision.

FINDINGS (committed -> corrected EH98 [CLASS no-wiggle]; every number on the chain's ALL-MATTER reading, both footings).
  The spectrum: committed/CLASS = 0.44 at 0.01 h/Mpc and 1.29 / 1.50 / 1.65 at 1 / 10 / 100 h/Mpc (fixed sigma_8).  The
    corrected EH98 is within 3.3% of CLASS's no-wiggle broad band on 0.01-20 h/Mpc -- the published FORMULA misses the 2%
    target at 0.041-0.048 and 0.44-5.2 h/Mpc (max at k = 1.2).  CLASS vs CAMB: 0.15%.  Re-scored with CLASS itself, no check moves (S).
  ONE VERDICT FLIPS: FP13 A2 (load-bearing) PASS -> FAIL.  The state's own running is n_eff = 2.21 (nonlinear, delta_c; CLASS
    2.18) and 2.98 (linear), not 2.06 / 2.66: the linear value and the nonlinear scan (2.17-2.31) leave A2's bands, so 'n = 2 is
    the state's own running' is no longer derived.  FP19 carries n = 2 as a postulate and its n window [1, 2.5] still passes.
  Six CONTROL flips, each a reproduction of a number computed on the committed spectrum: FP3 B2, FP6 K1 and FP9 K1 (the LCDM
    yardstick sigma_8 0.8101 -> 0.8080), FP7 B5 (its embedded L341 control; B5's verdict part holds), FP19 K2 / K4 (the hub's
    XR18 coefficients).
  sigma_8 / LCDM, every gate holds: H_Y 1.0128-1.0180 -> 1.0109-1.0154; H_S 1.0184-1.0227 -> 1.0148-1.0184 (now <= 1.02);
    H_K1 1.0117-1.0151 -> 1.0099-1.0127; FP6's (H) 1.0134-1.0191 -> 1.0115-1.0164.  The ungated core still fails: rms
    23.3 / 27.5 -> 21.8 / 25.7 (FP3 B3; FP7 B5 at lambda_eff = 277: 22.1 / 26.1 -> 20.7 / 24.4), per-mode ~17 / ~20 (+-0.2%).
    FP7's linear and per-mode lambda_eff thresholds for sigma_8 <= 1.02 drop 8-11% (linear, k <= 1: 1.07e7 -> 9.5e6; the rms
    physical one is unchanged); the sigma_8-vs-tracking pincer stands (gap x48 -> x42).
  Forest proxy: FP6's (H) 0.0055 -> 0.0029; H_Y 2.8e-7 unchanged; H_S and H_K1 0; H_K1 in real space (H7) 7.7e-4 -> 3.4e-5.
  Windows widen: FP6 H1 43 -> 48 of 81 cells; FP9 H1 28 -> 29 of 48 (22 at sigma_8 <= 1.02, was 18); H_K1's L_Lambda window
    [2.65, 4.6] -> [2.65, >= 5.0] Mpc (the scan ends at 5.0; the sigma_8 = 1.05 edge extrapolates to ~5.06), its
    sigma_8 <= 1.02 part [2.65, 3.0] -> [2.65, 3.3] (interpolated edge 3.24 -> 3.46).  The lower edge (KiDS at z = 0.4) holds.
  FP13's state: A6's 'linear-spectrum systematic' was this bug (linear -13..-42% -> +2..+4.5% against CLASS; nonlinear
    -1..-15% -> -0.4..+3.5%).  H_S's band-pass closes for z >= 13.6 (committed 17.4; CLASS 13.3), and the flagship keeps MOND
    to z_max = 3.79 (was 4.24).
  Unmoved: every KiDS verdict (H_Y and H_K1 exactly; H_S -6.2 / -7.7 -> -6.5 / -8.1 at z = 0.25), SPARC, the Local Group
    failure (R0 1.54 Mpc against the 1.21 edge), FP14 and FP17 (all pass).  FP18's copy (only the 0.43 k s term) moves its
    2-halo spectrum by <= 0.3%, so it is not re-run.

CHECKS
  K  CONTROLS: K1 [load-bearing] the in-memory patch touches exactly the two terms in exactly one T_EH98 per file (FP3, FP6,
     FP7), keeps every line number, and the three copies are the same function (committed and corrected); K2 [load-bearing]
     the harness (the lane's committed source exec'd through the patched reader, writes discarded) reproduces FP3's committed
     checks and numbers exactly when the committed spectrum is served.
  V  VALIDATION: V1 [load-bearing; MUTATE must fail] the corrected T equals EH98's published zero-baryon form (colossus
     modelEisenstein98ZeroBaryon) to 1e-10 at k = 1e-4 - 1e3 h/Mpc; V2 (reported; the task's 2% target) the error vs k of the
     committed and corrected spectra against CLASS's no-wiggle linear spectrum at fixed sigma_8, and the dewiggling's
     sensitivity; V3 (reported) CLASS vs CAMB; V4 (reported) the chain's other EH98 copies: FP1's (correct) and FP18's (only
     the 0.43 k s term wrong) and what that moves.
  R  THE RE-SCORE (reported; committed -> corrected EH98 -> CLASS no-wiggle, each lane's own gates, both footings): R1 FP3,
     R2 FP6, R3 FP7 (B5 + T), R4 FP9, R5 FP13 (+ the state's high-z closure), R6 FP14, R7 FP17, R8 FP19 (+ H_K1's L_Lambda
     window), each a full re-run of the committed code (FP7: its preamble, B5 and T), downstream lanes fed the upstream
     lanes' re-scored JSON; R9 the flip table.
  S  (reported) the EH98 fitting-formula residual: every re-scored check agrees between the corrected EH98 and CLASS's
     no-wiggle spectrum, or the disagreements are listed.
  F  [load-bearing] every re-run completed (no exception) with finite headline numbers.
  M  [MUTATE run only; load-bearing there] the harness with the committed spectrum reproduces every committed check (pass/fail)
     and headline number of every re-scored lane: an end-to-end control.
  H  (reported) the hub's and the record's files that carry the committed form or exec the chain's machinery.
  W  the ledger.
MUTATE=1 replaces the corrected function by the committed one EVERYWHERE: V1 must FAIL (rc = 1) and the re-scores must
reproduce the committed numbers (M).  The CLASS column is not run under MUTATE.  Outputs *_MUTATE.out / *_results_MUTATE.json.

SCOPE.  The linear spectrum only.  Every committed number here uses the ALL-MATTER reading of who feels MOND (FP22's question
is not touched); CMB lensing is FP22's and the hub's XR26 (CLASS-based, independent of T_EH98).  FP4/FP10/FP15/FP16 score S_8
with L319/L357's CLASS-based solver and are not affected.  Linear theory only (the lanes' own halofit where they use it); at
most two worker processes (corrected EH98 and CLASS no-wiggle), one thread each; FP13's own Pool(2) (its Local Group force
tables) runs serially inside its worker (order-preserving, same results).
Run from the lane directory:  python3 FP24_transfer_function_fix.py > FP24_transfer_function_fix.out 2>&1; echo rc=$? >> FP24_transfer_function_fix.out
"""
import os, sys, io, re, json, math, time, builtins, contextlib, subprocess, tempfile, traceback, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
warnings.filterwarnings("ignore")
import numpy as np

np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "FP24_transfer_function_fix"
WORKER = os.environ.get("FP24_WORKER", "")                      # internal: this file re-launched as a re-score worker
LANES_ENV = os.environ.get("FP24_LANES", "all")                  # development switch; the committed runs use 'all'
_REAL_OPEN = builtins.open
_trap = getattr(np, "trapezoid", None) or np.trapz
FOOTS = ("canonical", "alt")
T0 = time.time()

# the chain's cosmology (FP3/FP6/FP7: Planck 2018, no massive neutrino)
h, om_b, om_c, T_CMB, N_EFF, NS, SIG8 = 0.6736, 0.02237, 0.1200, 2.7255, 3.046, 0.965, 0.811
Ob, Oc = om_b / h ** 2, om_c / h ** 2
Om = Ob + Oc
SIG_NW = 0.25                                                    # dewiggling: Gaussian width in ln k on ln(P_CLASS / P_EH)
PATCHED = ("FP3_cosmology_linear.py", "FP6_gate_survey.py", "FP7_aqual_type_repair.py")
_LAMSTR = lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating, np.integer)) else str(o))
PLAN = [  # tag, stem, exec slices (None = whole file), the lane's own json default
    ("FP3", "FP3_cosmology_linear", None, str),
    ("FP6", "FP6_gate_survey", None, str),
    ("FP7", "FP7_aqual_type_repair", [(None, 'banner("A1  THE STATIC'), ('banner("B5  sigma_8 WITH NO GATE', 'banner("B6  STRONG'),
                                      ('banner("T   THE PINCER', 'banner("W   THE LEDGER')], str),
    ("FP9", "FP9_web_galaxy_separator", None, str),
    ("FP13", "FP13_separator_from_state", None, _LAMSTR),
    ("FP14", "FP14_zero_knob_core", None, str),
    ("FP17", "FP17_screening_without_xi", None, str),
    ("FP19", "FP19_hs_repair", None, _LAMSTR),
]
if LANES_ENV != "all":
    PLAN = [p for p in PLAN if p[0] in LANES_ENV.split(",")]


def P(*a):
    print(*a, flush=True)


# ================================================================================================= the source patch
def fn_block(src, name):
    """[i, j) of 'def name(k):' and its indented body (trailing blank lines excluded)."""
    head = f"def {name}(k):\n"
    i = src.index("\n" + head) + 1
    j = i + len(head)
    while j < len(src):
        nl = src.find("\n", j) + 1 or len(src)
        line = src[j:nl]
        if line.strip() and not line.startswith("    "):
            break
        j = nl
    blk = src[i:j].rstrip("\n") + "\n"
    return i, i + len(blk), blk


def fix_block(blk):
    """the two edits: 0.43 k s / h -> 0.43 k s, and q = k Theta^2/Gamma -> q = (k/h) Theta^2/Gamma."""
    m = re.search(r"\(0\.43 \* k \* (s_?) / (h_?)\)", blk)
    hv = m.group(2) if m else "h"
    b2, n1 = re.subn(r"\(0\.43 \* k \* (s_?) / h_?\)", r"(0.43 * k * \1)", blk)
    b3, n2 = re.subn(r"\b(q{1,2}) = k \* (th_?) \* (th_?) / ge\b", lambda mm: f"{mm.group(1)} = (k / {hv}) * {mm.group(2)} * {mm.group(3)} / ge", b2)
    return b3, n1, n2


def class_block(blk):
    n = blk.count("\n")
    return "def T_EH98(k):\n    return __FP24_T__(k)\n" + "    # FP24: CLASS's no-wiggle transfer function, injected\n" * (n - 2)


_PCACHE = {}


def patched_source(path, spec):
    """the committed source with its T_EH98 replaced for this spectrum ('committed' = unchanged)."""
    key = (path, spec)
    if key not in _PCACHE:
        src = _REAL_OPEN(path).read()
        info = dict(n_def=src.count("def T_EH98(k):"))
        if spec == "committed":
            out = src
            info.update(n1=0, n2=0)
        else:
            i, j, blk = fn_block(src, "T_EH98")
            if spec == "fixed":
                nb, n1, n2 = fix_block(blk)
            else:
                nb, n1, n2 = class_block(blk), 1, 1
            out = src[:i] + nb + src[j:]
            info.update(n1=n1, n2=n2, old=blk, new=nb)
        info["same_lines"] = out.count("\n") == src.count("\n")
        _PCACHE[key] = (out, info)
    return _PCACHE[key]


def block_fn(blk, name="T_EH98", extra=None):
    """exec a committed/corrected block with the chain's parameters under both naming conventions (FP6/FP3 and FP7)."""
    ns = dict(math=math, np=np, T_CMB=T_CMB, Om=Om, Ob=Ob, om_b=om_b, h=h, h_=h)
    ns.update(extra or {})
    exec(blk, ns)
    return ns[name]


# ================================================================================================= the harness
class _Sink(io.StringIO):
    """a write into the repository, kept in memory (never reaches the disk); close() keeps the content readable."""

    def __init__(self, reg, p):
        super().__init__()
        reg[p] = self

    def close(self):
        pass


class _BSink(io.BytesIO):
    def __init__(self, reg, p):
        super().__init__()
        reg[p] = self

    def close(self):
        pass


class Harness:
    """builtins.open while a committed lane runs: reads of FP3/FP6/FP7's source get this spectrum's T_EH98; reads of an
    upstream lane's results JSON get this run's re-scored JSON (self.serve); every write into the repository is captured in
    memory (self.written) and never reaches the disk -- the lane's own results JSON is read back from there."""

    def __init__(self, spec):
        self.spec, self.serve, self.written = spec, {}, {}

    def open(self, file, mode="r", *a, **k):
        try:
            p = os.path.abspath(os.fspath(file))
        except TypeError:
            return _REAL_OPEN(file, mode, *a, **k)
        if any(c in mode for c in "wax+"):
            if p.startswith(REPO + os.sep):
                return (_BSink if "b" in mode else _Sink)(self.written, p)
            return _REAL_OPEN(file, mode, *a, **k)
        if "b" not in mode:
            if p in self.serve:
                return io.StringIO(self.serve[p])
            if os.path.dirname(p) == HERE and os.path.basename(p) in PATCHED:
                return io.StringIO(patched_source(p, self.spec)[0])
        return _REAL_OPEN(file, mode, *a, **k)


@contextlib.contextmanager
def harnessed(H):
    old_open, old_env = builtins.open, os.environ.get("MUTATE")
    builtins.open = H.open
    os.environ["MUTATE"] = "0"
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            yield buf
    finally:
        builtins.open = old_open
        if old_env is None:
            os.environ.pop("MUTATE", None)
        else:
            os.environ["MUTATE"] = old_env


def run_lane(H, stem, slices=None):
    path = os.path.join(HERE, stem + ".py")
    ns = {"__file__": path, "__name__": "__main__"}
    rc, err, t0 = None, "", time.time()
    with harnessed(H) as buf:
        try:
            src = builtins.open(path).read()
            if slices is None:
                exec(compile(src, path, "exec"), ns)
            else:
                for a, b in slices:
                    ia = 0 if a is None else src.index(a)
                    ib = len(src) if b is None else src.index(b)
                    exec(compile("\n" * src[:ia].count("\n") + src[ia:ib], path, "exec"), ns)
        except SystemExit as e:
            rc = e.code
        except Exception:
            err = traceback.format_exc()
    return ns, buf.getvalue(), rc, err, time.time() - t0


def verdict_line(txt):
    m = re.findall(r"(\d+)/(\d+) checks pass; load-bearing failures: (\d+)", txt)
    return "/".join(m[-1]) if m else None


# ================================================================================================= spectra
def T_committed_fn():
    return block_fn(fn_block(_REAL_OPEN(os.path.join(HERE, "FP6_gate_survey.py")).read(), "T_EH98")[2])


def T_fixed_fn():
    return block_fn(fn_block(patched_source(os.path.join(HERE, "FP6_gate_survey.py"), "fixed")[0], "T_EH98")[2])


def class_linear(kmax_h=250.0):
    """CLASS's linear P(k, z = 0) [(Mpc/h)^3] on k_h = 1e-4 - 200 h/Mpc for the chain's cosmology (N_ur = 3.046, no ncdm)."""
    from classy import Class
    cl = Class()
    cl.set({"h": h, "omega_b": om_b, "omega_cdm": om_c, "n_s": NS, "A_s": 2.1e-9, "T_cmb": T_CMB, "N_ur": N_EFF,
            "output": "mPk", "P_k_max_h/Mpc": kmax_h, "z_max_pk": 0.0})
    cl.compute()
    LKC = np.linspace(math.log(1e-4), math.log(200.0), 4000)
    KC = np.exp(LKC)
    PC = np.array([cl.pk_lin(k * h, 0.0) for k in KC]) * h ** 3
    s8c = cl.sigma8()
    cl.struct_cleanup()
    cl.empty()
    return LKC, KC, PC, s8c


def dewiggle(LKC, KC, PC, Tref, sig=SIG_NW):
    """no-wiggle CLASS: P_ref x exp(G_sig * ln(P_CLASS/P_ref)), the Gaussian smoothing in ln k (the broad band is CLASS's)."""
    from scipy.ndimage import gaussian_filter1d
    Pref = KC ** NS * np.array([Tref(k * h) for k in KC]) ** 2
    lnR = gaussian_filter1d(np.log(PC / Pref), sig / (LKC[1] - LKC[0]), mode="nearest")
    return Pref * np.exp(lnR), lnR


def make_T_class():
    Tf = T_fixed_fn()
    LKC, KC, PC, _ = class_linear()
    _, lnR = dewiggle(LKC, KC, PC, Tf)

    def T_class(k):
        return Tf(k) * math.exp(0.5 * float(np.interp(math.log(max(k, 1e-30) / h), LKC, lnR)))
    return T_class


def norm_s8(LK, KK, Pk):
    x = 8.0 * KK
    W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
    return Pk * SIG8 ** 2 / _trap(KK ** 3 * Pk * W ** 2 / (2 * np.pi ** 2), LK)


# ================================================================================================= the worker
def fp13_state(H):
    """FP13's module and main()'s body up to its K banner (FP19's load_fp13 recipe), through the harness: the H_S state's
    band-pass length L(z) on its own reading and the redshift above which the band-pass is closed (L at the floor)."""
    path = os.path.join(HERE, "FP13_separator_from_state.py")
    ns = {"__file__": path, "__name__": "fp24_fp13_state"}
    with harnessed(H):
        src = builtins.open(path).read()
        mod = src[:src.index("\ndef main():")]
        body = src[src.index("\ndef main():") + len("\ndef main():"):
                   src.index('    banner("K  CONTROLS: the reused machinery reproduces the record; the halofit, the state, FP11\'s hook")')]
        body = "\n".join(l_[4:] if l_.startswith("    ") else l_ for l_ in body.split("\n"))
        exec(compile(mod, path, "exec"), ns)
        exec(compile(body, path, "exec"), ns)
    out = {}
    AGR, floor = np.asarray(ns["AGR"]), float(ns["XI_FLOOR_MPC"])
    for tag, s_, rd in (("head", ns["HEAD_S"], ns["HEAD_READ"]), ("lin_dc", ns["DELTA_C"], "lin")):
        tab = np.asarray(ns["L_table"](s_, rd), float)
        op = np.where(tab > floor * (1 + 1e-9))[0]                                   # AGR runs from a = 1e-3 up to 1
        zc = 0.0 if not len(op) else (float("inf") if op[0] == 0 else float(1.0 / AGR[op[0] - 1] - 1.0))
        Lk = {str(z): float(np.exp(np.interp(math.log(1 / (1 + z)), np.log(AGR), np.log(np.maximum(tab, 1e-300))))) * 1e3
              for z in (0.0, 0.25, 1.0, 2.5, 6.0, 10.0)}
        out[tag] = dict(s=float(s_), reading=str(rd), z_close=zc, L_kpc=Lk)
    return out


class SerialPool:
    """FP13's multiprocessing Pool(2) (its Local Group force tables) run in-process: this lane's budget is two worker processes,
    and pool.map is order-preserving, so the results are the same (each job hooks FP11's law itself)."""

    def __init__(self, *a, **k):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def map(self, f, it, chunksize=None):
        return [f(x) for x in it]

    def imap(self, f, it, chunksize=None):
        return (f(x) for x in it)

    imap_unordered = imap

    def starmap(self, f, it, chunksize=None):
        return [f(*x) for x in it]

    def close(self):
        pass

    def join(self):
        pass

    def terminate(self):
        pass


def worker(spec, out_path):
    import multiprocessing
    multiprocessing.Pool = SerialPool
    H = Harness(spec)
    if spec == "class":
        builtins.__FP24_T__ = make_T_class()
    res = {}
    lanes = os.environ.get("FP24_WORKER_LANES", "")
    states = [x for x in os.environ.get("FP24_WORKER_STATES", "").split(",") if x]
    for tag, stem, slices, dflt in [p_ for p_ in PLAN if not lanes or p_[0] in lanes.split(",")]:
        H.written = {}
        ns, txt, rc, err, dt = run_lane(H, stem, slices)
        jpath = os.path.join(HERE, f"{stem}_results.json")
        src_json = "written"
        try:
            if jpath in H.written:                     # the lane's own results JSON, exactly as it would have written it
                text = H.written[jpath].getvalue()
                d = json.loads(text)
            else:                                      # FP7 (a partial exec never reaches its write): its module-level OUT
                src_json = "namespace"
                text = json.dumps(ns.get("OUT", {}), default=dflt)
                d = json.loads(text)
        except Exception:
            d, text, err = {}, "", err + "\n[FP24] the lane's results did not parse: " + traceback.format_exc()
        if tag == "FP7":
            base = json.load(_REAL_OPEN(jpath))
            base["numbers"].update(d.get("numbers", {}))
            base["checks"].update(d.get("checks", {}))
            H.serve[jpath] = json.dumps(base, default=str)
        elif d and not err:
            H.serve[jpath] = text
        else:                                          # a failed re-run serves nothing: downstream lanes read the committed file
            H.serve.pop(jpath, None)
        res[tag] = dict(checks=d.get("checks", {}), numbers=d.get("numbers", {}), rc=rc, err=err[-6000:], time=dt,
                        verdict=verdict_line(txt), tail=txt[-2500:], results_from=src_json)
        print(f"[{spec}] {tag}: rc={rc} verdict={res[tag]['verdict']} err={'yes' if err else 'no'} ({dt:.0f} s)", flush=True)
        if err:
            print(err[-3000:], flush=True)
    for st_spec in states:
        key, HH = f"FP13_state_{st_spec}", (H if st_spec == spec else Harness(st_spec))
        if True:
            try:
                t0 = time.time()
                res[key] = fp13_state(HH)
                print(f"[{spec}] {key}: {res[key]} ({time.time() - t0:.0f} s)", flush=True)
            except Exception:
                res[key] = {"err": traceback.format_exc()[-3000:]}
                print(res[key]["err"], flush=True)
    json.dump(res, _REAL_OPEN(out_path, "w"), default=str)


if WORKER:
    worker(WORKER, os.environ["FP24_WORKER_OUT"])
    sys.exit(0)


# ================================================================================================= the parent: helpers
OUT = {"lane": "FP24", "mutate": MUTATE, "checks": {}, "numbers": {}, "ledger": []}
CH = []


def banner(t):
    P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)


def check(name, measured, ok, reading="", load_bearing=True):
    CH.append((name, bool(ok), load_bearing))
    OUT["checks"][name] = {"ok": bool(ok), "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def num(x):
    if isinstance(x, bool) or x is None:
        return x
    if isinstance(x, (int, float)):
        return float(x)
    if isinstance(x, str):
        if x in ("True", "False"):
            return x == "True"
        try:
            return float(x)
        except ValueError:
            return x
    return x


def g(n, *path):
    o = n
    for p_ in path:
        if isinstance(o, dict) and str(p_) in o:
            o = o[str(p_)]
        elif isinstance(o, list) and isinstance(p_, int) and -len(o) <= p_ < len(o):
            o = o[p_]
        else:
            return None
    return num(o)


def checks_by_id(chk):
    out = {}
    for k, v in (chk or {}).items():
        name = str(v.get("name", k)) if isinstance(v, dict) else str(k)
        key = name.split()[0] if name.split() else k
        k2, j = key, 1
        while k2 in out:
            j += 1
            k2 = f"{key}#{j}"
        ok = v.get("ok", v.get("pass")) if isinstance(v, dict) else v
        out[k2] = dict(ok=bool(num(ok)), lb=bool(v.get("load_bearing", True)) if isinstance(v, dict) else True,
                       measured=str(v.get("measured", "")) if isinstance(v, dict) else "", name=name)
    return out


def lane_json(stem):
    return json.load(_REAL_OPEN(os.path.join(HERE, f"{stem}_results.json")))


def fmt(v, nd=4):
    if v is None:
        return "--"
    if isinstance(v, bool):
        return "PASS" if v else "FAIL"
    if isinstance(v, (list, tuple)):
        return "[" + ", ".join(fmt(x, nd) for x in v) + "]"
    if isinstance(v, str):
        return v
    if not math.isfinite(v):
        return str(v)
    if v != 0 and (abs(v) >= 1e5 or abs(v) < 1e-3):
        return f"{v:.3e}"
    return f"{v:.{nd}f}"


def leaves(o, pre=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from leaves(v, f"{pre}/{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaves(v, f"{pre}[{i}]")
    else:
        yield pre, num(o)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the corrected T_EH98 is replaced by the committed one EVERYWHERE -- V1 must FAIL, and the re-scores must "
      "reproduce every committed number (M) ***")
SPEC_MAIN = "committed" if MUTATE else "fixed"

# ================================================================================================= K1 the patch
banner("K1  CONTROL: the in-memory patch (the only change to the committed code)")
k1 = {}
kk_test = np.logspace(-5, 3, 400)
fam_old, fam_new = [], []
for fname in PATCHED:
    path = os.path.join(HERE, fname)
    src = _REAL_OPEN(path).read()
    new, info = patched_source(path, "fixed")
    i, j, blk = fn_block(src, "T_EH98")
    ni, nj, nblk = fn_block(new, "T_EH98")
    outside_same = src[:i] == new[:ni] and src[j:] == new[nj:]
    diff_lines = [(a_, b_) for a_, b_ in zip(blk.split("\n"), nblk.split("\n")) if a_ != b_]
    To, Tn = block_fn(blk), block_fn(nblk)
    fam_old.append(np.array([To(k) for k in kk_test]))
    fam_new.append(np.array([Tn(k) for k in kk_test]))
    k1[fname] = dict(n_def=info["n_def"], edits=(info["n1"], info["n2"]), same_lines=info["same_lines"], outside_same=outside_same,
                     changed_lines=len(diff_lines))
    P(f"    {fname}: T_EH98 defined {info['n_def']}x; edits (0.43 k s term, q term) = {info['n1']}, {info['n2']}; lines kept: "
      f"{info['same_lines']}; rest of the file identical: {outside_same}")
    for a_, b_ in diff_lines:
        P(f"       - {a_.strip()}\n       + {b_.strip()}")
same_old = max(float(np.max(np.abs(f_ / fam_old[0] - 1))) for f_ in fam_old)
same_new = max(float(np.max(np.abs(f_ / fam_new[0] - 1))) for f_ in fam_new)
k1_ok = all(v["n_def"] == 1 and v["edits"] == (1, 1) and v["same_lines"] and v["outside_same"] and 1 <= v["changed_lines"] <= 2
            for v in k1.values()) and same_old < 1e-12 and same_new < 1e-12
check("K1 CONTROL: the patch is exactly the fix -- one T_EH98 per file (FP3, FP6, FP7), the 0.43 k s term and the q term edited "
      "once each, every line number kept, the rest of each file byte-identical; the three committed copies are one function and "
      "so are the three corrected ones",
      f"{ {k_[:4]: v['edits'] for k_, v in k1.items()} }; copies agree to {same_old:.0e} (committed) / {same_new:.0e} (corrected)", k1_ok)
OUT["numbers"]["K1"] = k1

# ================================================================================================= V validation
banner("V  VALIDATION: the corrected T_EH98 against EH98's published form (colossus) and against CLASS / CAMB")
T_old, T_new = T_committed_fn(), T_fixed_fn()
T_use = T_old if MUTATE else T_new                      # MUTATE: the 'corrected' function IS the committed one
from colossus.cosmology import power_spectrum as _cps
KHV = np.logspace(-4, 3, 700)
T_col = _cps.modelEisenstein98ZeroBaryon(KHV, h, Om, Ob, T_CMB)
dv_use = float(np.max(np.abs(np.array([T_use(k * h) for k in KHV]) / T_col - 1)))
dv_old = float(np.max(np.abs(np.array([T_old(k * h) for k in KHV]) / T_col - 1)))
check("V1 THE FIX IS THE PUBLISHED FORM: the corrected T_EH98 equals EH98's zero-baryon (no-wiggle) transfer function eqs. (26), "
      "(28)-(31) as independently implemented in colossus, to 1e-10 at k = 1e-4 - 1e3 h/Mpc; the committed form does not",
      f"max |T/T_colossus - 1|: {'corrected' if not MUTATE else 'corrected (= committed under MUTATE)'} {dv_use:.1e}; committed {dv_old:.2f}",
      dv_use < 1e-10)
OUT["numbers"]["V1"] = dict(dev_corrected=dv_use, dev_committed=dv_old)

tV = time.time()
LKC, KC, PC, s8_class = class_linear()
PCnw, _ = dewiggle(LKC, KC, PC, T_new)
Pold = norm_s8(LKC, KC, KC ** NS * np.array([T_old(k * h) for k in KC]) ** 2)
Pnew = norm_s8(LKC, KC, KC ** NS * np.array([T_new(k * h) for k in KC]) ** 2)
PCn, PCnwn = norm_s8(LKC, KC, PC), norm_s8(LKC, KC, PCnw)
rng = (KC >= 0.01) & (KC <= 20.0)
KLIST = (0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0)
tab = {}
P(f"    CLASS (classy, h = {h}, omega_b = {om_b}, omega_c = {om_c}, n_s = {NS}, T_cmb = {T_CMB}, N_ur = {N_EFF}, no ncdm); each "
  f"spectrum normalised to sigma_8 = {SIG8} (8 Mpc/h top hat); CLASS no-wiggle = Gaussian smoothing (width {SIG_NW} in ln k) of "
  f"ln(P_CLASS/P_EH,corrected) -- the broad band is CLASS's")
P(f"    {'k [h/Mpc]':>10s} {'committed/CLASS_nw':>19s} {'corrected/CLASS_nw':>19s} {'CLASS_full/CLASS_nw':>20s}")
for k in KLIST:
    i = int(np.argmin(np.abs(KC - k)))
    tab[str(k)] = (float(Pold[i] / PCnwn[i]), float(Pnew[i] / PCnwn[i]), float(PCn[i] / PCnwn[i]))
    P(f"    {k:>10g} {tab[str(k)][0]:>19.4f} {tab[str(k)][1]:>19.4f} {tab[str(k)][2]:>20.4f}")
e_old = np.abs(Pold / PCnwn - 1)[rng]
e_new = np.abs(Pnew / PCnwn - 1)[rng]
k_old, k_new = float(KC[rng][np.argmax(e_old)]), float(KC[rng][np.argmax(e_new)])
within2 = KC[rng][e_new <= 0.02]
# the k-ranges where the corrected form is within 2%
segs, cur = [], None
for kv, okv in zip(KC[rng], e_new <= 0.02):
    if okv and cur is None:
        cur = [kv, kv]
    elif okv:
        cur[1] = kv
    elif cur is not None:
        segs.append(cur)
        cur = None
if cur is not None:
    segs.append(cur)
sens = {}
for sg in (0.15, 0.25, 0.5):
    Pnw_s, _ = dewiggle(LKC, KC, PC, T_new, sig=sg)
    sens[str(sg)] = float(np.max(np.abs(Pnew / norm_s8(LKC, KC, Pnw_s) - 1)[rng]))
wig = float(np.max(np.abs(PCn / PCnwn - 1)[rng]))
e_new_wig = float(np.max(np.abs(Pnew / PCn - 1)[rng]))
target_ok = float(e_new.max()) <= 0.02
P(f"    0.01-20 h/Mpc: committed max |dP/P| = {e_old.max():.3f} (at k = {k_old:.3g}); corrected max = {e_new.max():.4f} (at k = {k_new:.3g}); "
  f"within 2% on " + ", ".join(f"[{a_:.3g}, {b_:.3g}]" for a_, b_ in segs) + " h/Mpc")
P(f"    dewiggling width 0.15/0.25/0.5: corrected max {sens['0.15']:.4f}/{sens['0.25']:.4f}/{sens['0.5']:.4f}; CLASS's own BAO "
  f"wiggles {wig:.3f} (corrected vs CLASS with wiggles: {e_new_wig:.3f}); CLASS sigma_8 at A_s = 2.1e-9: {s8_class:.4f}")
check("V2 (reported; the task's 2% target) THE ERROR vs k AGAINST CLASS (no-wiggle vs no-wiggle, fixed sigma_8), committed and "
      "corrected: the corrected EH98 removes the committed error; whether the published no-wiggle FORMULA itself meets 2% of CLASS's "
      "broad band on 0.01-20 h/Mpc is printed (and where it does)",
      f"committed: {tab['0.01'][0]:.3f} / {tab['1.0'][0]:.3f} / {tab['10.0'][0]:.3f} / {tab['100.0'][0]:.3f} at k = 0.01/1/10/100; "
      f"max |dP/P| on 0.01-20: committed {e_old.max():.3f}, corrected {e_new.max():.4f} (k = {k_new:.2f}); 2% target "
      f"{'MET' if target_ok else 'NOT MET'} (within 2%: " + ", ".join(f"{a_:.3g}-{b_:.3g}" for a_, b_ in segs) + ")",
      True, load_bearing=False)
OUT["numbers"]["V2"] = dict(table=tab, max_committed=float(e_old.max()), k_max_committed=k_old, max_corrected=float(e_new.max()),
                            k_max_corrected=k_new, within2_segments=segs, target_2pct_met=target_ok, dewiggle_sensitivity=sens,
                            class_wiggle_amp=wig, corrected_vs_class_full=e_new_wig, sigma8_class_As=s8_class)
# V3 CLASS vs CAMB
try:
    import camb
    pars = camb.CAMBparams()
    pars.set_cosmology(H0=100 * h, ombh2=om_b, omch2=om_c, mnu=0.0, num_massive_neutrinos=0, nnu=N_EFF, TCMB=T_CMB)
    pars.InitPower.set_params(As=2.1e-9, ns=NS)
    pars.set_matter_power(redshifts=[0.0], kmax=40.0)
    rcb = camb.get_results(pars)
    kc_, _, pc_ = rcb.get_matter_power_spectrum(minkh=1e-4, maxkh=25.0, npoints=1500)
    Pcb = np.interp(LKC, np.log(kc_), np.log(pc_[0]))
    okk = KC <= 25.0
    Pcb_n = norm_s8(LKC[okk], KC[okk], np.exp(Pcb[okk]))
    PCn25 = norm_s8(LKC[okk], KC[okk], PC[okk])
    r25 = (KC[okk] >= 0.01) & (KC[okk] <= 20.0)
    d_cc = float(np.max(np.abs(Pcb_n / PCn25 - 1)[r25]))
except Exception as e_:
    d_cc = float("nan")
    P(f"    CAMB unavailable: {e_!r}")
check("V3 (reported) THE REFERENCE: CLASS and CAMB agree on the linear spectrum at fixed sigma_8 (0.01-20 h/Mpc, with wiggles)",
      f"max |P_CAMB/P_CLASS - 1| = {d_cc:.4f}", d_cc < 0.01 if math.isfinite(d_cc) else False, load_bearing=False)
OUT["numbers"]["V3"] = dict(camb_vs_class=d_cc)

# V4 the chain's other copies
src1 = _REAL_OPEN(os.path.join(HERE, "FP1_static_sector.py")).read()
src18 = _REAL_OPEN(os.path.join(HERE, "FP18_kids_vs_hubble_flow_data.py")).read()
T1 = block_fn(fn_block(src1, "T_eh")[2], "T_eh", dict(OmK=Om, hK=h, ObK=Ob))
d_fp1 = float(np.max(np.abs(np.array(T1(KHV * h)) / T_col - 1)))
H70, OM_W9, OB_W9, NS_W9, S8_W9 = 0.70, 0.2793, 0.0463, 0.972, 0.821         # FP18:215 (B21's WMAP9)
T18 = block_fn(fn_block(src18, "_T_nw")[2], "_T_nw", dict(H70=H70, OM_W9=OM_W9, OB_W9=OB_W9))
T18c = _cps.modelEisenstein98ZeroBaryon(KHV, H70, OM_W9, OB_W9, 2.7255)
LK18 = np.linspace(math.log(1e-5), math.log(3e2), 5000)
KK18 = np.exp(LK18)


def _s8n(P0):
    x = KK18 * 8.0 / H70
    W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
    return P0 * S8_W9 ** 2 / _trap(KK18 ** 3 * P0 * W ** 2 / (2 * np.pi ** 2), LK18)


P18 = _s8n(KK18 ** NS_W9 * np.array(T18(KK18)) ** 2)
P18c = _s8n(KK18 ** NS_W9 * _cps.modelEisenstein98ZeroBaryon(KK18 / H70, H70, OM_W9, OB_W9, 2.7255) ** 2)
r18 = P18 / P18c
big = KK18 >= 0.1 * H70
xi_r = {}
for rr in (0.3, 1.0, 3.0):
    wx = np.sinc(KK18 * rr / np.pi) * np.exp(-(KK18 / 40.0) ** 2)
    xi_r[str(rr)] = float(_trap(KK18 ** 3 * P18 * wx, LK18) / _trap(KK18 ** 3 * P18c * wx, LK18))
d18_T = float(np.max(np.abs(np.array(T18(KHV * H70)) / T18c - 1)))
check("V4 (reported) THE CHAIN'S OTHER EH98 COPIES: FP1's T_eh (its E section's 2-halo spectrum) is the published form; FP18's _T_nw "
      "(LCDM's NFW+2h family, WMAP9) has only the 0.43 k s term wrong (k in h/Mpc against s in Mpc), which moves its spectrum by "
      "<= 0.3% at k >= 0.1 h/Mpc and the linear correlation function by <= 0.3% at 0.3-3 Mpc -- below every FP18 verdict's margin; "
      "not re-run",
      f"FP1 vs colossus {d_fp1:.1e}; FP18 T vs colossus max {d18_T:.3f}; FP18 P/P_correct at k >= 0.1 h/Mpc: "
      f"{r18[big].min():.4f}-{r18[big].max():.4f} (k = 0.03 h/Mpc: {float(np.interp(math.log(0.03 * H70), LK18, r18)):.3f}); "
      f"xi_lin ratio at 0.3/1/3 Mpc: " + "/".join(f"{v_:.4f}" for v_ in xi_r.values()),
      d_fp1 < 1e-10 and float(np.max(np.abs(r18[big] - 1))) < 0.005, load_bearing=False)
OUT["numbers"]["V4"] = dict(fp1_dev=d_fp1, fp18_T_dev=d18_T, fp18_P_ratio_kge0p1=[float(r18[big].min()), float(r18[big].max())], fp18_xi_ratio=xi_r)
P(f"    ({time.time() - tV:.0f} s)")

# ================================================================================================= K2 the harness
banner("K2  CONTROL: the harness reproduces a committed lane when the committed spectrum is served (FP3, whole)")
H0h = Harness("committed")
ns3, txt3, rc3, err3, dt3 = run_lane(H0h, "FP3_cosmology_linear")
_p3 = os.path.join(HERE, "FP3_cosmology_linear_results.json")
d3 = {} if err3 else (json.loads(H0h.written[_p3].getvalue()) if _p3 in H0h.written else json.loads(json.dumps(ns3.get("OUT", {}), default=str)))
j3 = lane_json("FP3_cosmology_linear")
cb3, cn3 = checks_by_id(j3["checks"]), checks_by_id(d3.get("checks", {}))
same_ck = sum(1 for k_ in cb3 if k_ in cn3 and cn3[k_]["ok"] == cb3[k_]["ok"])
L_old3 = dict(leaves(j3["numbers"]))
L_new3 = dict(leaves(d3.get("numbers", {})))
nd3, dmax3 = 0, 0.0
for k_, v_ in L_old3.items():
    w_ = L_new3.get(k_)
    if isinstance(v_, float) and isinstance(w_, float) and math.isfinite(v_):
        nd3 += 1
        dmax3 = max(dmax3, abs(w_ - v_) / max(abs(v_), 1e-300) if v_ != 0 else abs(w_))
k2_ok = not err3 and same_ck == len(cb3) == len(cn3) and nd3 > 20 and dmax3 < 1e-9
check("K2 CONTROL: FP3's committed source, exec'd through the harness with the committed spectrum (its own JSON write discarded), "
      "reproduces FP3's committed checks and every committed number",
      f"checks {same_ck}/{len(cb3)} same (re-run has {len(cn3)}); {nd3} numbers, max relative deviation {dmax3:.1e}; rc {rc3}; "
      f"{dt3:.0f} s{'; ERROR ' + err3[-300:] if err3 else ''}", k2_ok)

# ================================================================================================= the workers
banner("R  THE RE-SCORE: every spectrum-dependent chain lane re-run whole through the harness (two workers)")
ALLT = [p_[0] for p_ in PLAN]
if MUTATE:   # the committed spectrum; the lanes split over two workers (upstream JSON served within a worker, else the committed file)
    LAYOUT = [("committed_A", "committed", [t_ for t_ in ALLT if t_ in ("FP6", "FP7", "FP9", "FP19")], []),
              ("committed_B", "committed", [t_ for t_ in ALLT if t_ not in ("FP6", "FP7", "FP9", "FP19")], ["committed"] if "FP13" in ALLT else [])]
else:        # one worker per spectrum column, each running the whole chain in order (upstream JSON served)
    LAYOUT = [("fixed", "fixed", ALLT, ["fixed"] if "FP13" in ALLT else []),
              ("class", "class", ALLT, ["class", "committed"] if "FP13" in ALLT else [])]
specs = sorted({sp_ for _, sp_, _, _ in LAYOUT})
TMP = os.environ.get("FP24_TMP") or tempfile.mkdtemp(prefix="fp24_")       # development switches: FP24_TMP / FP24_REUSE (not
REUSE = os.environ.get("FP24_REUSE", "0") == "1"                            # used by the committed runs, which start fresh)
procs = {}
for wname, sp_, lanes_, states_ in ([] if REUSE else LAYOUT):
    env = dict(os.environ, FP24_WORKER=sp_, FP24_WORKER_OUT=os.path.join(TMP, f"{wname}.json"), FP24_WORKER_LANES=",".join(lanes_) or "none",
               FP24_WORKER_STATES=",".join(states_), MUTATE="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1",
               VECLIB_MAXIMUM_THREADS="1", MKL_NUM_THREADS="1")
    procs[wname] = subprocess.Popen([sys.executable, os.path.abspath(__file__)], cwd=HERE, env=env,
                                    stdout=_REAL_OPEN(os.path.join(TMP, f"{wname}.log"), "w"), stderr=subprocess.STDOUT)
P(f"    workers: " + "; ".join(f"{w_} ({sp_}: {', '.join(l_) or '-'}; FP13 state {', '.join(s_) or '-'})" for w_, sp_, l_, s_ in LAYOUT)
  + f" -- one thread each; logs in {TMP}")
WR, MAIN, CLS, STATES = {}, {}, {}, {}
for wname, sp_, _, _ in LAYOUT:
    pr = procs.get(wname)
    try:
        rc_w = pr.wait(timeout=2700) if pr else "reused"
    except subprocess.TimeoutExpired:
        pr.kill()
        rc_w = "timeout"
    try:
        WR[wname] = json.load(_REAL_OPEN(os.path.join(TMP, f"{wname}.json")))
    except Exception:
        WR[wname] = {}
    P(f"    worker {wname}: rc {rc_w}")
    for ln in _REAL_OPEN(os.path.join(TMP, f"{wname}.log")).read().splitlines():
        if ln.startswith(f"[{sp_}]"):
            P("      " + ln[:260])
    for k_, v_ in WR[wname].items():
        if k_.startswith("FP13_state_"):
            STATES[k_[len("FP13_state_"):]] = v_
        elif sp_ == SPEC_MAIN:
            MAIN[k_] = v_
        elif sp_ == "class":
            CLS[k_] = v_


# ------------------------------------------------------------------------------------------------- per-lane key numbers
def s4(n, *pre):
    return [g(n, *pre, f"('{f}', '{m}')") for f in FOOTS for m in ("rms", "permode")]


def mx(v):
    v = [x for x in (v or []) if isinstance(x, float)]
    return max(v) if v else None


def mn(v):
    v = [x for x in (v or []) if isinstance(x, float)]
    return min(v) if v else None


def fmax_dict(d):
    if not isinstance(d, dict):
        return None
    return mx([num(x) for x in d.values()])


def ll_cross(n, target):
    """H_K1's L_Lambda where the max sigma_8 (both footings, both modes) crosses target, from FP19 B1's scan (linear interp)."""
    sc = (n.get("B1", {}) or {}).get("scan", {})
    pts = sorted((float(LL), mx([num(x) for x in (r.get("s8", {}) or {}).values()])) for LL, r in sc.items())
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if y0 is not None and y1 is not None and y0 <= target < y1:
            return x0 + (target - y0) * (x1 - x0) / (y1 - y0)
    if len(pts) >= 2 and None not in (pts[-1][1], pts[-2][1]) and pts[-2][1] < pts[-1][1] < target:   # beyond the scan's end
        (x0, y0), (x1, y1) = pts[-2], pts[-1]
        return f"{x1 + (target - y1) * (x1 - x0) / (y1 - y0):.2f} (extrap.)"
    return None


def rx(ck, cid, pat):
    m = re.search(pat, ((ck or {}).get(cid) or {}).get("measured", ""))
    return float(m.group(1)) if m else None


MKEYS = {   # numbers each lane prints in a check's measured string but does not store
    "FP6": lambda ck: [("H1 window: cells passing every linchpin gate (of 81)", rx(ck, "H1", r"(\d+) of 81 cells"))],
    "FP9": lambda ck: [("H1 window cells also at sigma_8 <= 1.02", rx(ck, "H1", r"\((\d+) also at sigma_8"))],
    "FP13": lambda ck: [("A2 n_eff, NL scan at s = 1.3/1.5/2.0/2.4/3.0 (A2 band 1.9-2.2)", [rx(ck, "A2", rf"NL scan.*?{re.escape(s_)}: ([0-9.]+)") for s_ in ("1.3", "1.5", "2.0", "2.4", "3.0")]),
                        ("L1 LG timing mass can / alt [1e11 Msun]", [(lambda v: v / 1e11 if v else v)(rx(ck, "L1", r"canonical: M_t = ([0-9.e+]+)")),
                                                                  (lambda v: v / 1e11 if v else v)(rx(ck, "L1", r"alt: M_t = ([0-9.e+]+)"))]),
                        ("L2 LG merged R0 can / alt [Mpc] (edge 1.21: FAILS)", [rx(ck, "L2", r"canonical: ([0-9.]+) Mpc"), rx(ck, "L2", r"alt: ([0-9.]+) Mpc")])],
    "FP19": lambda ck: [("H6 n window: passing n (count of 1.0/1.5/2.0/2.5)", float(len(re.findall(r"[0-9.]+", (re.search(r"n passing \[([^\]]*)\]", ((ck or {}).get("H6") or {}).get("measured", "")) or [None, ""])[1]))))],
}


KEYS = {
    "FP3": lambda n: [
        ("B  LCDM sigma_8 (the yardstick, k <= 20 h/Mpc)", g(n, "B", "sigma8_LCDM")),
        ("B3 ungated core sigma_8/LCDM can rms/pm, alt rms/pm", [g(n, "B", "ungated", f"{f}/{m}") for f in FOOTS for m in ("rms", "permode")]),
        ("C2 on-fraction f_max can rms/pm, alt rms/pm", [g(n, "C2", "fmax", f"{f}/{m}") for f in FOOTS for m in ("rms", "permode")]),
        ("C4a concave gate: max sigma_8/LCDM (D1-D4, both footings/modes; gate 1.02)", fmax_dict((n.get("C4", {}) or {}).get("sigma8_ratio"))),
    ],
    "FP6": lambda n: [
        ("K1 LCDM / ungated rms / per-mode sigma_8", [g(n, "K1", "lcdm"), g(n, "K1", "rms"), g(n, "K1", "permode")]),
        ("E2 web field y at z = 0.25: rms341 / variance", [g(n, "E2", "0.25", "rms341"), g(n, "E2", "0.25", "rms_var")]),
        ("H2 headline sigma_8/LCDM (6: rms, pm, mono)", [g(n, "H2", "s8", f"('{f}', '{m}')") for f in FOOTS for m in ("rms", "permode", "mono_rms")]),
        ("H2 headline forest proxy max (gate 0.10)", fmax_dict((n.get("H2", {}) or {}).get("forest"))),
        ("H2c flagship z_max can / alt", [g(n, "H2c", "canonical"), g(n, "H2c", "alt")]),
        ("B2 n=2 band-pass sigma_8 rms at L = 1/2/3 Mpc", [g(n, "B2", f"2_{L}", "rms") for L in ("1.0", "2.0", "3.0")]),
    ],
    "FP7": lambda n: [
        ("B5 LCDM sigma_8 (yardstick)", g(n, "B5", "S8_LCDM")),
        ("B5 no gate, lambda_eff = 277: sigma_8/LCDM can rms/pm, alt rms/pm", [g(n, "B5", "phys", f"{f}/{m}", "277.4") for f in FOOTS for m in ("rms", "permode")]),
        ("B5 linear sigma_8/LCDM at lambda_eff = 1e7 / 3e7 / 1e8", [g(n, "B5", "linear", k_) for k_ in ("1e+07", "3e+07", "1e+08")]),
        ("B5 lambda_eff threshold (sigma_8 <= 1.02): linear k<=20 / k<=1", [g(n, "B5", "lin_threshold"), g(n, "B5", "lin_threshold_k1")]),
        ("B5 lambda_eff threshold physical: can rms/pm, alt rms/pm", [g(n, "B5", "phys_threshold", f"{f}/{m}") for f in FOOTS for m in ("rms", "permode")]),
        ("T  lambda_sigma8 (most lenient) / gap vs tracking", [g(n, "T", "lambda_sigma8"), g(n, "T", "gap_min")]),
    ],
    "FP9": lambda n: [
        ("H2 (H_Y) sigma_8/LCDM can rms/pm, alt rms/pm", s4(n, "H2", "s8")),
        ("H2 (H_Y) forest proxy max (gate 0.10)", fmax_dict((n.get("H2", {}) or {}).get("forest"))),
        ("H2 (H_Y) flagship dex (min; gate -0.05)", mn([num(x) for x in ((n.get("H2", {}) or {}).get("flag", {}) or {}).values()])),
        ("H2 (H_Y) KiDS d chi^2 (z = 0.25) can / alt", [g(n, "H2", "kids", "canonical"), g(n, "H2", "kids", "alt")]),
        ("H1 window: passing cells (of 48)", len(n.get("H1_window", []) or []) if n.get("H1_window") is not None else None),
        ("H2c flagship z_max can / alt", [g(n, "H2c", "zmax", "canonical"), g(n, "H2c", "zmax", "alt")]),
        ("V  sigma_8's lambda (FP7 B5 k<=1) / forest lambda / flagship lambda", [g(n, "V", "lam_s8"), g(n, "V", "lam_forest"), g(n, "V", "lam_flag")]),
    ],
    "FP13": lambda n: [
        ("H1 (H_S) sigma_8/LCDM can rms/pm, alt rms/pm", s4(n, "H1", "s8")),
        ("H1 (H_S) forest proxy max", fmax_dict((n.get("H1", {}) or {}).get("forest"))),
        ("H1 (H_S) flagship dex (min)", mn([num(x) for x in ((n.get("H1", {}) or {}).get("flag", {}) or {}).values()])),
        ("H1 (H_S) SPARC dex can / alt", [g(n, "H1", "sparc", "canonical"), g(n, "H1", "sparc", "alt")]),
        ("H1 (H_S) KiDS z = 0.25 / 0.4 / 0.7 (can)", [g(n, "H1", "kids", "canonical"), g(n, "H1", "kids04", "canonical"), g(n, "H1", "kids07", "canonical")]),
        ("H1 (H_S) KiDS z = 0.25 / 0.4 / 0.7 (alt)", [g(n, "H1", "kids", "alt"), g(n, "H1", "kids04", "alt"), g(n, "H1", "kids07", "alt")]),
        ("H5 FP9's (H_Y) at z = 0.4: KiDS can / alt (gate +9)", [g(n, "H5", "FP9 (H_Y) itself", "kids04", "canonical"), g(n, "H5", "FP9 (H_Y) itself", "kids04", "alt")]),
        ("H4 flagship MOND to z_max; flagship dex at z = 4 / 5", [g(n, "H4", "zmax"), g(n, "H4", "flag_z", "4.0"), g(n, "H4", "flag_z", "5.0")]),
        ("H4 sub-L P boost z=0, k = 0.3/0.5/1 h/Mpc", [g(n, "H4", "Pboost", "0.0", k_) for k_ in ("0.3", "0.5", "1.0")]),
        ("A2 n_eff (NL/delta_c, lin/delta_c)", [g(n, "A2", "n_eff", "NL_1.686"), g(n, "A2", "n_eff", "lin_1.686")]),
        ("A6 L(z): CLASS/chain - 1, lin z = 0/0.25/1/2.5", [(g(n, "A6", f"{z}_lin", 0) / g(n, "A6", f"{z}_lin", 1) - 1) if g(n, "A6", f"{z}_lin", 1) else None for z in ("0.0", "0.25", "1.0", "2.5")]),
        ("A6 L(z): CLASS/chain - 1, NL  z = 0/0.25/1/2.5", [(g(n, "A6", f"{z}_NL", 0) / g(n, "A6", f"{z}_NL", 1) - 1) if g(n, "A6", f"{z}_NL", 1) else None for z in ("0.0", "0.25", "1.0", "2.5")]),
    ],
    "FP14": lambda n: [
        ("C3 (H_Y) sigma_8/LCDM at the c_2 floor, can rms/pm, alt rms/pm", s4(n, "C3", "s8", "floor")),
        ("C3 forest proxy (floor / c_2 -> oo)", [g(n, "C3", "forest", "floor"), g(n, "C3", "forest", "oo")]),
        ("L  sigma_8 vs lambda = 0/1/100 (can pm)", [g(n, "L", "sigma8_lambda", k_) for k_ in ("0.0", "1.0", "100.0")]),
    ],
    "FP17": lambda n: [
        ("R1 (H_Y) sigma_8/LCDM can / alt (per-mode)", [g(n, "R1", "canonical", "s8"), g(n, "R1", "alt", "s8")]),
        ("R2 sigma_8 factor", g(n, "R2", "s8_factor")),
    ],
    "FP19": lambda n: [
        ("H1 (H_K1) sigma_8/LCDM can rms/pm, alt rms/pm", s4(n, "H1", "s8")),
        ("H1 (H_K1) forest proxy max", fmax_dict((n.get("H1", {}) or {}).get("forest"))),
        ("H1 (H_K1) flagship dex (min) / SPARC can", [mn([num(x) for x in ((n.get("H1", {}) or {}).get("flag", {}) or {}).values()]), g(n, "H1", "sparc", "canonical")]),
        ("H1 (H_K1) KiDS z = 0.25 can/alt; z = 0.4 can/alt", [g(n, "H1", "kids", "canonical"), g(n, "H1", "kids", "alt"), g(n, "H1", "kids@0.4", "canonical"), g(n, "H1", "kids@0.4", "alt")]),
        ("H7 real-space (Stein) sigma_8 can/alt; forest can/alt", [g(n, "H7", "headline", "canonical", "s8"), g(n, "H7", "headline", "alt", "s8"),
                                                                    g(n, "H7", "headline", "canonical", "forest"), g(n, "H7", "headline", "alt", "forest")]),
        ("B1 L_Lambda window [lo, hi] (grid)", g(n, "B1", "window")),
        ("B1 L_Lambda window with sigma_8 <= 1.02 (grid)", g(n, "B1", "window_tight")),
        ("B1 L_Lambda where max sigma_8 = 1.02 / 1.05 (interpolated)", [ll_cross(n, 1.02), ll_cross(n, 1.05)]),
        ("A3 open root sigma_8 can rms/pm, alt rms/pm", s4(n, "A3", "open", "s8")),
        ("H5 flagship z_max; KiDS z = 0.7 can", [g(n, "H5", "zmax"), g(n, "H5", "kids07", "canonical")]),
    ],
}

def fp7_b5_parts(n):
    """FP7 B5's pass condition, split: the CONTROL part reproduces L341's committed yardstick sigma_8 (0.81009, the committed
    spectrum); the VERDICT part is sigma_8 >> 1.02 at lambda_eff = 277 (rms > 10), thresholds > 1e6, the lower gate never binds.
    (B5's lambda_eff -> oo limit is printed by FP7, not stored; it is spectrum-blind: the ratio of a spectrum to itself.)"""
    b = n.get("B5", {}) or {}
    ph, th = b.get("phys", {}) or {}, b.get("phys_threshold", {}) or {}
    le0 = f"{num(b.get('lambda_eff_lambda0')):.4g}" if b.get("lambda_eff_lambda0") is not None else None
    try:
        verdict = (all(num(ph[f"{f}/rms"][le0]) > 10 for f in FOOTS) and num(b["lin_threshold"]) > 1e6
                   and min(num(v_) for v_ in th.values()) > 1e6 and all(num(v_) >= 0.922 for t_ in ph.values() for v_ in t_.values()))
        control = abs(num(b["S8_LCDM"]) / 0.81009 - 1) < 1e-3
    except Exception:
        return None
    return dict(verdict=verdict, control=control, s8=num(b.get("S8_LCDM")))


EMBED = {("FP7", "B5"): fp7_b5_parts}

# ------------------------------------------------------------------------------------------------- the per-lane tables
ALL_FLIPS, RES, S_DIS = [], {}, []
STEM = {p_[0]: p_[1] for p_ in PLAN}
for tag, stem, _, _ in PLAN:
    banner(f"R  {tag}: {stem} -- committed -> {'committed (MUTATE)' if MUTATE else 'corrected EH98'}{'' if MUTATE else ' -> CLASS no-wiggle'}")
    jc = lane_json(stem)
    rm, rcl = MAIN.get(tag, {}), CLS.get(tag, {})
    P(f"    re-run ({SPEC_MAIN}): verdict {rm.get('verdict') or ('partial exec' if tag == 'FP7' else None)} (committed "
      f"{verdict_line(_REAL_OPEN(os.path.join(HERE, stem + '.out')).read())}); rc {rm.get('rc')}; {rm.get('time', 0):.0f} s"
      + (f";  CLASS column: verdict {rcl.get('verdict')}, {rcl.get('time', 0):.0f} s" if rcl else ""))
    if rm.get("err"):
        P("    ERROR (corrected run):\n" + rm["err"][-1500:])
    if rcl.get("err"):
        P("    ERROR (CLASS run):\n" + rcl["err"][-1500:])
    cb, cm, cc_ = checks_by_id(jc["checks"]), checks_by_id(rm.get("checks", {})), checks_by_id(rcl.get("checks", {}))
    if tag == "FP7":
        cb = {k_: v_ for k_, v_ in cb.items() if k_ in cm}
    flips = []
    for k_, v_ in cm.items():
        b_ = cb.get(k_)
        cl_ = cc_.get(k_)
        if b_ is not None and b_["ok"] != v_["ok"]:
            kind, note = ("CONTROL" if "CONTROL" in v_["name"].upper() else "VERDICT"), ""
            if (tag, k_) in EMBED:
                pb, pa = EMBED[(tag, k_)](jc["numbers"]), EMBED[(tag, k_)](rm.get("numbers", {}))
                pc = EMBED[(tag, k_)](rcl.get("numbers", {})) if rcl else None
                if pb and pa and pb["verdict"] == pa["verdict"] and pb["control"] != pa["control"]:
                    kind = "CONTROL"
                note = (f"decomposed: verdict part {fmt(pb and pb['verdict'])} -> {fmt(pa and pa['verdict'])}"
                        + (f" (CLASS {fmt(pc['verdict'])})" if pc else "") + f"; embedded control (L341's yardstick sigma_8 0.81009) "
                        f"{fmt(pb and pb['control'])} -> {fmt(pa and pa['control'])} ({fmt(pa and pa['s8'], 5)})")
            flips.append(dict(lane=tag, id=k_, before="PASS" if b_["ok"] else "FAIL", after="PASS" if v_["ok"] else "FAIL",
                              class_col=("PASS" if cl_["ok"] else "FAIL") if cl_ else "--", load_bearing=v_["lb"],
                              kind=kind, name=v_["name"][:170], note=note,
                              measured_before=b_["measured"][:420], measured_after=v_["measured"][:420],
                              measured_class=(cl_["measured"][:420] if cl_ else "")))
        if cl_ is not None and cl_["ok"] != v_["ok"] and not MUTATE:
            S_DIS.append(dict(lane=tag, id=k_, corrected="PASS" if v_["ok"] else "FAIL", class_col="PASS" if cl_["ok"] else "FAIL",
                              kind="CONTROL" if "CONTROL" in v_["name"].upper() else "VERDICT", name=v_["name"][:120]))
    missing = [k_ for k_ in cb if k_ not in cm]
    ALL_FLIPS += flips
    mk = MKEYS.get(tag, lambda ck: [])
    kb, km = KEYS[tag](jc["numbers"]) + mk(cb), KEYS[tag](rm.get("numbers", {})) + mk(cm)
    kc = (KEYS[tag](rcl.get("numbers", {})) + mk(cc_)) if rcl else None
    P(f"    {'number':66s} {'committed':>30s} {'corrected' if not MUTATE else 're-run':>30s}" + ("" if MUTATE else f" {'CLASS nw':>30s}"))
    rows = []
    for i_, (lab, vb) in enumerate(kb):
        vm = km[i_][1]
        vc = kc[i_][1] if kc else None
        rows.append(dict(label=lab, committed=vb, corrected=vm, class_nw=vc))
        P(f"    {lab[:66]:66s} {fmt(vb):>30s} {fmt(vm):>30s}" + ("" if MUTATE else f" {fmt(vc):>30s}"))
    P(f"    checks: {sum(1 for v_ in cm.values() if v_['ok'])}/{len(cm)} pass after (committed {sum(1 for v_ in cb.values() if v_['ok'])}/{len(cb)});"
      f" flips {len(flips)}" + (f"; not re-run: {missing}" if missing else ""))
    for f_ in flips:
        P(f"    FLIP {f_['id']:6s} {f_['before']} -> {f_['after']} ({f_['kind']}{', load-bearing' if f_['load_bearing'] else ''}; CLASS column {f_['class_col']}): {f_['name'][:120]}")
        P(f"         before: {f_['measured_before'][:300]}")
        P(f"         after:  {f_['measured_after'][:300]}")
        if f_["measured_class"]:
            P(f"         CLASS:  {f_['measured_class'][:300]}")
        if f_.get("note"):
            P(f"         {f_['note']}")
    # the changed measured strings of checks that did not flip (the spectrum-dependent numbers each check prints)
    moved = [(k_, cb[k_]["measured"], v_["measured"]) for k_, v_ in cm.items() if k_ in cb and cb[k_]["ok"] == v_["ok"]
             and cb[k_]["measured"] != v_["measured"]]
    for k_, mb, ma in moved[:40]:
        P(f"    moved {k_:6s} ({'PASS' if cm[k_]['ok'] else 'FAIL'} both): {mb[:150]}\n{'':18s}-> {ma[:150]}")
    RES[tag] = dict(rows=rows, flips=flips, n_checks=len(cm), n_pass=sum(1 for v_ in cm.values() if v_["ok"]),
                    n_pass_committed=sum(1 for v_ in cb.values() if v_["ok"]), verdict=rm.get("verdict"), err=bool(rm.get("err")),
                    class_verdict=rcl.get("verdict") if rcl else None, moved=len(moved))
OUT["numbers"]["R"] = RES

# ------------------------------------------------------------------------------------------------- FP13's state at high z
if "FP13" in STEM:
    banner("R5b FP13's STATE AT HIGH z: where the H_S band-pass closes (L at the filter floor) -- committed vs corrected vs CLASS")
    st_ = {k_: STATES[k_] for k_ in ("committed", "fixed", "class") if k_ in STATES}
    for sp_, v_ in st_.items():
        if "err" in v_:
            P(f"    {sp_}: ERROR {v_['err'][-600:]}")
            continue
        for tg_, r_ in v_.items():
            P(f"    {sp_:9s} {tg_:6s} (s = {r_['s']:.3f}, {r_['reading']}): closed for z >= {r_['z_close']:.2f}; L [kpc] "
              + ", ".join(f"z={z}: {L_:.1f}" for z, L_ in r_["L_kpc"].items()))
    OUT["numbers"]["FP13_state"] = st_

# ------------------------------------------------------------------------------------------------- R9 the flip table
banner("R9  THE FLIP TABLE (every check whose pass/fail changed; CONTROL = a reproduction of a committed/record number)")
vflips = [f_ for f_ in ALL_FLIPS if f_["kind"] == "VERDICT"]
cflips = [f_ for f_ in ALL_FLIPS if f_["kind"] == "CONTROL"]
for f_ in ALL_FLIPS:
    P(f"    {f_['lane']:5s} {f_['id']:6s} {f_['before']} -> {f_['after']}  {f_['kind']:7s} {'LB' if f_['load_bearing'] else 'rep'}  CLASS {f_['class_col']}")
P(f"    verdict flips: {len(vflips)}; control flips: {len(cflips)}")
OUT["numbers"]["flips"] = ALL_FLIPS

# ================================================================================================= S / M / F
if not MUTATE:
    banner("S  THE EH98 FITTING-FORMULA RESIDUAL: corrected EH98 vs CLASS's no-wiggle spectrum, check by check")
    for d_ in S_DIS:
        P(f"    {d_['lane']:5s} {d_['id']:6s} corrected {d_['corrected']} vs CLASS {d_['class_col']} ({d_['kind']}): {d_['name']}")
    nS = sum(len(checks_by_id(CLS.get(t_, {}).get("checks", {}))) for t_ in STEM)
    check("S (reported) THE RESIDUAL IS VERDICT-NEUTRAL: every re-scored check has the same pass/fail with the corrected EH98 and "
          "with CLASS's no-wiggle spectrum (the formula's <= 3-4% broad-band error vs CLASS moves no verdict)",
          f"{len([d_ for d_ in S_DIS if d_['kind'] == 'VERDICT'])} verdict / {len([d_ for d_ in S_DIS if d_['kind'] == 'CONTROL'])} "
          f"control disagreements over {nS} checks" + ("" if not S_DIS else ": " + ", ".join(f"{d_['lane']} {d_['id']}" for d_ in S_DIS)),
          not [d_ for d_ in S_DIS if d_["kind"] == "VERDICT"] and bool(CLS), load_bearing=False)
    OUT["numbers"]["S"] = S_DIS
else:
    banner("M  MUTATE CONTROL: the harness with the committed spectrum reproduces every committed check and headline number")
    dev_m, n_m, ck_m, ck_bad = 0.0, 0, 0, []
    for tag, stem, _, _ in PLAN:
        jc = lane_json(stem)
        cb, cm = checks_by_id(jc["checks"]), checks_by_id(MAIN.get(tag, {}).get("checks", {}))
        for k_, v_ in cm.items():
            if k_ in cb:
                ck_m += 1
                if cb[k_]["ok"] != v_["ok"]:
                    ck_bad.append(f"{tag} {k_}")
        for r_ in RES.get(tag, {}).get("rows", []):
            for a_, b_ in zip(np.atleast_1d(np.array(r_["committed"], dtype=object)), np.atleast_1d(np.array(r_["corrected"], dtype=object))):
                if isinstance(a_, float) and isinstance(b_, float) and math.isfinite(a_):
                    n_m += 1
                    dev_m = max(dev_m, abs(b_ - a_) / max(abs(a_), 1e-12))
    check("M CONTROL (MUTATE): with the committed spectrum the harness reproduces every committed check and headline number of "
          "every re-scored lane (no flips)", f"checks {ck_m - len(ck_bad)}/{ck_m} same{'; differ: ' + ', '.join(ck_bad) if ck_bad else ''}; "
          f"{n_m} headline numbers, max relative deviation {dev_m:.1e}", not ck_bad and ck_m > 100 and n_m > 50 and dev_m < 1e-6)

fin = []
for tag in STEM:
    r_ = RES.get(tag, {})
    for row in r_.get("rows", []):
        for v_ in np.atleast_1d(np.array(row["corrected"], dtype=object)):
            if isinstance(v_, float):
                fin.append(math.isfinite(v_))
errs = [t_ for t_ in STEM if MAIN.get(t_, {}).get("err") or not MAIN.get(t_)] + [f"{t_}(CLASS)" for t_ in STEM if not MUTATE and (CLS.get(t_, {}).get("err") or not CLS.get(t_))]
check("F EVERY RE-RUN COMPLETED: each lane's committed code ran to its end through the harness (no exception) with finite headline "
      "numbers, in every spectrum column",
      f"lanes {len(STEM)} x columns {len(specs)}; errors: {errs or 'none'}; finite headline numbers {sum(fin)}/{len(fin)}",
      not errs and len(fin) > 50 and all(fin))

# ================================================================================================= H other copies
banner("H  THE OTHER COPIES: files that carry the committed form, and files that name the chain's EH98 lanes")
pat_bug = re.compile(r"0\.43 ?\* ?k[a-z_]* ?\* ?s[a-z_]* ?/ ?h")
pat_exec = re.compile(r"(FP6_gate_survey|FP9_web_galaxy_separator|FP13_separator_from_state)\.py")
carry, inherit = [], []
for root, dirs, files in os.walk(os.path.join(REPO, "real_research")):
    dirs[:] = [d_ for d_ in dirs if d_ not in ("__pycache__", ".git")]
    for fn_ in files:
        if not fn_.endswith(".py") or fn_.startswith("FP24_"):
            continue
        pth = os.path.join(root, fn_)
        try:
            s_ = _REAL_OPEN(pth, errors="replace").read()
        except Exception:
            continue
        rel = os.path.relpath(pth, REPO)
        if pat_bug.search(s_):
            carry.append(rel)
        elif pat_exec.search(s_) and "derivation_chain_2026" not in rel:
            inherit.append(rel)
fi_ = os.path.join(REPO, "fable_independent_2026")
if os.path.isdir(fi_):
    for fn_ in os.listdir(fi_):
        if fn_.endswith(".py") and pat_bug.search(_REAL_OPEN(os.path.join(fi_, fn_), errors="replace").read()):
            carry.append(os.path.relpath(os.path.join(fi_, fn_), REPO))
carry, inherit = sorted(carry), sorted(inherit)
P("    carry the committed form (0.43 k s / h):\n      " + "\n      ".join(carry))
P("    name the chain's EH98 lanes (FP6/FP9/FP13: exec'd or read) outside the chain:\n      " + "\n      ".join(inherit))
check("H (reported) THE OTHER COPIES: the record's and the hub's files that carry the committed form, or name the chain's EH98 "
      "lanes (FP6/FP9/FP13) and may inherit it -- not re-scored here (their owners' re-runs); the chain's own lanes are re-scored above",
      f"{len(carry)} carry it; {len(inherit)} name the chain's EH98 lanes",
      True, load_bearing=False)
OUT["numbers"]["H"] = dict(carry=carry, inherit=inherit)

# ================================================================================================= W ledger
banner("W  THE LEDGER")


def rowv(tag, lab_start):
    for r_ in RES.get(tag, {}).get("rows", []):
        if r_["label"].startswith(lab_start):
            return r_
    return None


def rng_s(v, nd=3):
    v = [x for x in np.atleast_1d(np.array(v, dtype=object)) if isinstance(x, float)]
    return "--" if not v else (f"{min(v):.{nd}f}" if abs(max(v) - min(v)) < 10 ** -nd else f"{min(v):.{nd}f}-{max(v):.{nd}f}")


def vfl(tag):
    return [f_["id"] for f_ in ALL_FLIPS if f_["lane"] == tag and f_["kind"] == "VERDICT"]


LEDGER = [
    ("R24a", "DERIVED", f"the corrected T_EH98 is EH98's published zero-baryon form (q = (k/h) Theta^2/Gamma_eff, 0.43 k s; colossus to "
     f"{OUT['numbers']['V1']['dev_corrected']:.0e}); against CLASS's no-wiggle spectrum at fixed sigma_8 it is within "
     f"{OUT['numbers']['V2']['max_corrected']:.1%} on 0.01-20 h/Mpc (the formula's own broad-band error; the 2% target "
     f"{'met' if OUT['numbers']['V2']['target_2pct_met'] else 'NOT met'})", "V1, V2"),
    ("R24b", "FAILS", "the chain's committed T_EH98 (L341 -> FP3/FP6/FP7 -> FP9/FP13/FP14/FP17/FP19) is EH98",
     f"corrected by FP24: q = k Theta^2/Gamma and 0.43 k s/h with k in 1/Mpc; at fixed sigma_8 {tab['0.01'][0]:.2f}x CLASS at 0.01 h/Mpc, "
     f"{tab['1.0'][0]:.2f}/{tab['10.0'][0]:.2f}/{tab['100.0'][0]:.2f}x at 1/10/100 h/Mpc (V2)"),
]
if not MUTATE:
    r7 = rowv("FP7", "B5 no gate")
    r7t = rowv("FP7", "B5 lambda_eff threshold (")
    r7p = rowv("FP7", "B5 lambda_eff threshold physical")
    if r7:
        LEDGER.append(("R24c", "FAILS", f"FP7 B5: sigma_8 with no gate at lambda_eff = 277 (can rms/pm, alt rms/pm): {fmt(r7['committed'], 2)} -> "
                       f"{fmt(r7['corrected'], 2)} x LCDM (still >> 1.02: the ungated AQUAL scalar fails sigma_8)",
                       f"corrected by FP24 (R3); CLASS no-wiggle {fmt(r7['class_nw'], 2)}"))
    if r7t and r7p:
        LEDGER.append(("R24d", "CONSTRAINT", f"FP7 B5/T: sigma_8 <= 1.02 needs lambda_eff >= {fmt(r7t['corrected'], 2)} (linear, k<=20 / k<=1; was "
                       f"{fmt(r7t['committed'], 2)}), physical {fmt(r7p['corrected'], 2)} (was {fmt(r7p['committed'], 2)}); the sigma_8-vs-tracking "
                       f"pincer {'stands' if 'T' not in vfl('FP7') else 'FLIPS'}", "corrected by FP24 (R3)"))
    for tag, lab, link, gate_txt in (("FP9", "H2 (H_Y) sigma_8", "R24e", "H_Y (FP9 headline)"), ("FP13", "H1 (H_S) sigma_8", "R24f", "H_S (FP13 headline)"),
                                     ("FP19", "H1 (H_K1) sigma_8", "R24g", "H_K1 (FP19 headline)"), ("FP14", "C3 (H_Y)", "R24h", "H_Y via FP14 C3")):
        r_ = rowv(tag, lab)
        if r_:
            vv = [x for x in np.atleast_1d(np.array(r_["corrected"], dtype=object)) if isinstance(x, float)]
            inband = bool(vv) and min(vv) >= 0.922 and max(vv) <= 1.05
            LEDGER.append((link, "DERIVED" if inband else "FAILS",
                           f"{gate_txt} sigma_8 gate [0.922, 1.05]: sigma_8/LCDM {rng_s(r_['committed'], 4)} -> {rng_s(r_['corrected'], 4)} (CLASS nw "
                           f"{rng_s(r_['class_nw'], 4)}); <= 1.02: {'yes' if vv and max(vv) <= 1.02 else 'no'}", f"corrected by FP24 (R, {tag} re-run whole)"))
    rw = rowv("FP19", "B1 L_Lambda window [lo")
    rwt = rowv("FP19", "B1 L_Lambda window with")
    rwx = rowv("FP19", "B1 L_Lambda where")
    if rw:
        LEDGER.append(("R24i", "CONSTRAINT", f"H_K1's L_Lambda window {fmt(rw['committed'], 2)} -> {fmt(rw['corrected'], 2)} Mpc (grid); sigma_8 <= 1.02 part "
                       f"{fmt(rwt['committed'], 2)} -> {fmt(rwt['corrected'], 2)}; interpolated sigma_8 = 1.02/1.05 edges {fmt(rwx['committed'], 2)} -> "
                       f"{fmt(rwx['corrected'], 2)} Mpc", "corrected by FP24 (R8)"))
    st_m = (OUT["numbers"].get("FP13_state", {}) or {}).get("fixed", {})
    st_c = (OUT["numbers"].get("FP13_state", {}) or {}).get("committed", {})
    r13 = rowv("FP13", "A6 L(z): CLASS/chain - 1, lin")
    if r13:
        LEDGER.append(("R24j", "FAILS", "FP13 A6's 'linear-spectrum systematic' (CLASS vs the chain's EH98) is a property of the linear reading",
                       f"corrected by FP24: it was the h-units bug -- lin z = 0/0.25/1/2.5: {fmt(r13['committed'], 3)} -> {fmt(r13['corrected'], 3)} (R5)"))
    if st_m and "head" in st_m:
        LEDGER.append(("R24k", "CONSTRAINT", f"H_S's band-pass closes (L at the floor) for z >= {st_m['head']['z_close']:.1f} on its own reading "
                       f"(committed spectrum: {st_c.get('head', {}).get('z_close', float('nan')):.1f}); the JWST-era state moves with the spectrum",
                       "corrected by FP24 (R5b)"))
    r6w, r9w = rowv("FP6", "H1 window"), rowv("FP9", "H1 window: passing")
    if r6w and r9w:
        LEDGER.append(("R24o", "CONSTRAINT", f"the separator windows widen: FP6 (H) {fmt(r6w['committed'], 0)} -> {fmt(r6w['corrected'], 0)} of 81 cells; "
                       f"FP9 (H_Y) {fmt(r9w['committed'], 0)} -> {fmt(r9w['corrected'], 0)} of 48", "corrected by FP24 (R2, R4)"))
    ra2 = rowv("FP13", "A2 n_eff (NL")
    if ra2:
        LEDGER.append(("R24p", "FAILS", "FP13 A2: n = 2 is the state's own running (derived: n_eff 2.06 NL / 2.66 lin within A2's bands)",
                       f"corrected by FP24 (R5): n_eff (NL, lin at delta_c) {fmt(ra2['committed'], 3)} -> {fmt(ra2['corrected'], 3)} (CLASS "
                       f"{fmt(ra2['class_nw'], 3)}); the linear value and the NL scan leave A2's bands, so n = 2 is a postulate, not the state's "
                       f"running (FP19 already carries it as POSTULATED; its n window still passes)"))
    rz = rowv("FP13", "H4 flagship MOND")
    if rz:
        LEDGER.append(("R24q", "CONSTRAINT", f"H_S's price: the 1e11 flagship keeps MOND to z_max {fmt(rz['committed'][0], 2)} -> {fmt(rz['corrected'][0], 2)} "
                       f"(CLASS {fmt(rz['class_nw'][0], 2)})", "corrected by FP24 (R5)"))
    LEDGER.append(("R24r", "OPEN", "the hub's XR18 coefficients (FP19 K2/K4's references) were computed on the committed spectrum: FP19's two "
                   "controls against them now fail; XR18 needs its own re-run", "R8, H"))
    LEDGER.append(("R24l", "OPEN", f"the hub's and the record's files that carry the committed form ({len(carry) - 3} outside the chain) or name the "
                   f"chain's EH98 lanes ({len(inherit)}) are not re-scored here", "H"))
    LEDGER.append(("R24m", "DERIVED", "FP18's _T_nw (only the 0.43 k s term wrong) moves its 2-halo spectrum by <= 0.3% at k >= 0.1 h/Mpc: no FP18 verdict moves; "
                   "FP1's copy is correct; FP4/FP10/FP15/FP16 use CLASS (L319/L357)", "V4, SCOPE"))
LEDGER.append(("R24n", "FITTED", "kappa = 1/2 (Z = 5.7888): the only accepted fitted input; not derived here", "FP0"))
for k_, st, what, why in LEDGER:
    P(f"    {k_:6s} {st:11s} {what}  --  {why}")
OUT["ledger"] = [dict(link=k_, status=st, what=w_, basis=b_) for k_, st, w_, b_ in LEDGER]
check("W (reported) the ledger", f"{len(LEDGER)} links", True, load_bearing=False)

# ================================================================================================= verdict
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
banner("VERDICT")
P(f"  The committed T_EH98 mixes h units (q missing 1/h, a spurious 1/h in 0.43 k s): at fixed sigma_8 it is {tab['0.01'][0]:.2f}x CLASS at "
  f"0.01 h/Mpc and {tab['1.0'][0]:.2f}-{tab['100.0'][0]:.2f}x at 1-100 h/Mpc.  The corrected function is EH98's published form "
  f"(within {OUT['numbers']['V2']['max_corrected']:.1%} of CLASS's no-wiggle broad band on 0.01-20 h/Mpc; the 2% target "
  f"{'met' if OUT['numbers']['V2']['target_2pct_met'] else 'is NOT met by the formula itself'}).")
P(f"  Re-score: {len(vflips)} verdict flip(s), {len(cflips)} control flip(s) across {len(STEM)} lanes"
  + ("" if MUTATE else f"; corrected EH98 vs CLASS no-wiggle: {len([d_ for d_ in S_DIS if d_['kind'] == 'VERDICT'])} verdict disagreement(s)")
  + ".  Not 'closed'.")
P(f"  Time {time.time() - T0:.0f} s.")
fn = os.path.join(HERE, f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json")
json.dump(OUT, _REAL_OPEN(fn, "w"), indent=1, default=_LAMSTR)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {os.path.basename(fn)}")
sys.exit(0 if n_fail == 0 else 1)
