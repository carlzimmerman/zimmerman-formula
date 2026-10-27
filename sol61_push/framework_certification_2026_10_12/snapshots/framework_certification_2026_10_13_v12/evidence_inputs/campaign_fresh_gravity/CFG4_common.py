#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG4_common -- shared machinery for lane CFG4 (the target law derived from the evidence).

Nothing here is a result.  It holds:
  * the base constants: a0 = kappa c sqrt(G rho_Lambda) on the two footings, read from the chain's committed FP0 JSON
    (canonical 9.3603e-11, alt 1.1312e-10 m/s^2); kappa = 1/2 is FITTED; Z = 2 sqrt(8 pi/3) = 5.7888 (Z == kappa's form);
  * the run harness every CFG4 script uses: a tee that writes the script's own .out (MUTATE=1 writes *_MUTATE.out), named
    checks with a load-bearing flag, the verdict line 'N/M checks pass; load-bearing failures: K', rc = 1 when a
    load-bearing check fails, and the results JSON (*_results.json / *_results_MUTATE.json);
  * a read-only executor for the record's committed scripts (file writes refused, MUTATE forced to 0 inside, stdout
    captured), the pattern FP20 uses;
  * the kernels: P2 (the framework's own nu = sqrt(1 + 1/y)), nu_mono (the chain's monotone repair of nu_RAR, exec'd from
    FP1's committed source, the kernel the 09-26 decision adopted), nu_RAR (the exponential RAR shape, reference only), and
    a one-parameter transition family nu_beta(y) = (1 + y^-beta)^(1/(2 beta)) (beta = 1 is P2);
  * the SPARC loader (175 rotmod files + the Lelli et al. 2016 master table in real_research/data);
  * FP20's exact spherical projector (exec'd from FP20's committed source): the only projector CFG4 uses.

Run nothing from here directly.
"""
import os
import sys
import io
import re
import json
import math
import time
import builtins
import contextlib

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CHAIN = os.path.join(REPO, "real_research", "derivation_chain_2026")
HUB = os.path.join(REPO, "real_research", "cross_thread_review_2026_09_26")
DATA = os.path.join(REPO, "real_research", "data")
MUTATE = os.environ.get("MUTATE", "0") == "1"
_trap = getattr(np, "trapezoid", None) or np.trapz

# ------------------------------------------------------------------------------------------------ constants (SI)
C_SI = 299792458.0
G_SI = 6.67430e-11
MSUN = 1.98847e30
PC = 3.0856775814913673e16
KPC = 1e3 * PC
MPC = 1e6 * PC
KAPPA = 0.5                                                   # FITTED (never derived)
Z_FRAME = 2.0 * math.sqrt(8.0 * math.pi / 3.0)               # 5.7888; Z == kappa's form (a0 = c H0 sqrt(Omega_L)/Z)
_FP0 = json.load(open(os.path.join(CHAIN, "FP0_core_postulates_results.json")))["numbers"]
A0 = {"canonical": float(_FP0["a0_canonical"]), "alt": float(_FP0["a0_rho_total"])}
RHO_LAMBDA = float(_FP0["rho_Lambda"])
FOOTS = ("canonical", "alt")
assert abs(A0["canonical"] - 9.3603e-11) < 1e-15 and abs(A0["alt"] - 1.1312e-10) < 1e-15
SIGMA_M = {f: A0[f] / (2 * math.pi * G_SI) / (MSUN / PC ** 2) for f in FOOTS}     # a0/(2 pi G) in Msun/pc^2


# ------------------------------------------------------------------------------------------------ run harness
class Run:
    """one script's run: tee to its own .out, named checks, results JSON, verdict and exit code."""

    def __init__(self, slug, lane="CFG4"):
        self.slug = slug
        self.mutate = MUTATE
        suf = "_MUTATE" if MUTATE else ""
        self.out_path = os.path.join(HERE, f"{slug}{suf}.out")
        self.json_path = os.path.join(HERE, f"{slug}_results{suf}.json")
        self._f = builtins.open(self.out_path, "w", encoding="utf-8")
        self._stdout = sys.stdout
        sys.stdout = self
        self.t0 = time.time()
        self.OUT = {"lane": lane, "script": slug, "mutate": MUTATE, "checks": {}, "numbers": {}, "ledger": []}
        self.CH = []

    # file-like interface for the tee
    def write(self, t):
        self._stdout.write(t)
        self._f.write(t)

    def flush(self):
        self._stdout.flush()
        self._f.flush()

    def P(self, *a):
        print(*a, flush=True)

    def banner(self, t):
        self.P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)

    def el(self):
        return f"[{time.time() - self.t0:.0f} s]"

    def check(self, name, measured, ok, load_bearing=True, reading=""):
        ok = bool(ok)
        key = name.split()[0]
        k2, j = key, 1
        while k2 in self.OUT["checks"]:
            j += 1
            k2 = f"{key}#{j}"
        self.CH.append((k2, ok, load_bearing))
        self.OUT["checks"][k2] = {"ok": ok, "load_bearing": load_bearing, "measured": str(measured), "name": name}
        self.P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
        if reading:
            self.P(f"         reading:  {reading}")
        return ok

    def num(self, key, value):
        self.OUT["numbers"][key] = jclean(value)
        return value

    def ledger(self, tag, status, text, where):
        self.OUT["ledger"].append({"id": tag, "status": status, "text": text, "where": where})
        self.P(f"    {tag:8s} {status:11s} {text}  --  {where}")

    def finish(self):
        npass = sum(1 for _, ok, _ in self.CH if ok)
        nlb = sum(1 for _, ok, lb in self.CH if (not ok) and lb)
        self.OUT["summary"] = {"n_checks": len(self.CH), "n_pass": npass, "load_bearing_failures": nlb,
                               "failed": [k for k, ok, _ in self.CH if not ok], "seconds": round(time.time() - self.t0, 1)}
        with builtins.open(self.json_path, "w", encoding="utf-8") as fh:
            json.dump(jclean(self.OUT), fh, indent=1, sort_keys=False)
        self.P(f"\n  {npass}/{len(self.CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(self.json_path)} "
               f"({time.time() - self.t0:.0f} s)")
        rc = 1 if nlb else 0
        self.P(f"rc = {rc}")
        sys.stdout = self._stdout
        self._f.close()
        return rc


def jclean(o):
    """make an object JSON-safe (numpy scalars/arrays, tuples as keys, inf/nan as strings)."""
    if isinstance(o, dict):
        return {(k if isinstance(k, str) else str(k)): jclean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jclean(v) for v in o]
    if isinstance(o, np.ndarray):
        return jclean(o.tolist())
    if isinstance(o, (np.floating,)):
        o = float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, float):
        if math.isnan(o) or math.isinf(o):
            return str(o)
        return o
    return o


# ------------------------------------------------------------------------------------------------ read-only execution
def _ro_open(file, mode="r", *a, **k):
    if any(c in mode for c in "wax+"):
        raise PermissionError(f"CFG4 refuses to write {file!r} from a re-executed committed script")
    return builtins.open(file, mode, *a, **k)


@contextlib.contextmanager
def quiet_env():
    """MUTATE=0 inside the committed code (it reads the variable at exec time); its stdout captured."""
    old = os.environ.get("MUTATE")
    os.environ["MUTATE"] = "0"
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            yield buf
    finally:
        if old is None:
            os.environ.pop("MUTATE", None)
        else:
            os.environ["MUTATE"] = old


def exec_slices(path, slices, ns=None, name="committed"):
    """exec [start, stop) slices of a committed source in ONE namespace (writes refused; line numbers kept)."""
    src = builtins.open(path).read()
    ns = {"__file__": path, "__name__": name, "open": _ro_open} if ns is None else ns
    ns.setdefault("__file__", path)
    ns.setdefault("__name__", name)
    ns["open"] = _ro_open
    with quiet_env() as buf:
        for a, b in slices:
            ia = 0 if a is None else (src.index(a) if isinstance(a, str) else a)
            ib = len(src) if b is None else (src.index(b, ia) if isinstance(b, str) else b)
            code = "\n" * src[:ia].count("\n") + src[ia:ib]
            exec(compile(code, path, "exec"), ns)
    return ns, buf.getvalue()


# ------------------------------------------------------------------------------------------------ kernels
def nu_p2(y):
    """the framework's own law P2: g_obs = sqrt(g_bar^2 + g_bar a0), i.e. nu = sqrt(1 + 1/y)."""
    y = np.maximum(np.asarray(y, float), 1e-300)
    return np.sqrt(1.0 + 1.0 / y)


def nu_rar(y):
    """the exponential RAR shape 1/(1 - exp(-sqrt y)) -- a reference description of the data's shape, not a base."""
    y = np.maximum(np.asarray(y, float), 1e-12)
    return 1.0 / (-np.expm1(-np.sqrt(y)))


def nu_beta(y, beta):
    """one-parameter transition family (1 + y^-beta)^(1/(2 beta)): deep limit y^-1/2 for every beta, P2 at beta = 1,
    high-y tail 1 + y^-beta/(2 beta).  An effective description of the data's transition sharpness, nothing more."""
    y = np.maximum(np.asarray(y, float), 1e-300)
    return np.exp(np.log1p(y ** (-beta)) / (2.0 * beta))


_FP1 = os.path.join(CHAIN, "FP1_static_sector.py")
_KNS, _ = exec_slices(_FP1, [("def _h_rar(y):", "KER, KNAME = ")],
                      ns={"np": np, "math": math, "brentq": __import__("scipy.optimize", fromlist=["brentq"]).brentq},
                      name="fp1_kernels")
nu_mono = _KNS["nu_mono"]                                    # FP1's committed nu_mono (L340's table), exec'd read-only
Y_PEAK_RAR = float(_KNS["Y_P"])                              # 2.5396: where nu_RAR's phantom h = y (nu - 1) peaks

KERNELS = {"P2": nu_p2, "nu_mono": nu_mono}


# ------------------------------------------------------------------------------------------------ SPARC
def load_sparc():
    """the 175 rotmod files (the record's order: sorted file names) and the master table (Lelli, McGaugh & Schombert 2016)."""
    d_ = os.path.join(DATA, "sparc_data")
    gal = []
    for f in sorted(os.listdir(d_)):
        if not f.endswith("_rotmod.dat"):
            continue
        try:
            d = np.genfromtxt(os.path.join(d_, f), comments="#")
        except Exception:
            continue
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        gal.append(dict(name=f.replace("_rotmod.dat", ""), R=d[:, 0], Vobs=d[:, 1], eV=d[:, 2], Vgas=d[:, 3], Vdisk=d[:, 4],
                        Vbul=d[:, 5]))
    tab = {}
    keys = ("T", "D", "eD", "fD", "Inc", "eInc", "L36", "eL36", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat",
            "eVflat", "Q")
    for line in builtins.open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
        tok = line.split()
        if len(tok) != 19:                                    # the data rows: name, 17 numbers, the reference string
            continue
        try:
            vals = [float(t) for t in tok[1:18]]
        except ValueError:
            continue
        row = dict(zip(keys, vals))
        for k in ("T", "fD", "Q"):
            row[k] = int(row[k])
        tab[tok[0]] = row
    for g in gal:
        g["meta"] = tab.get(g["name"])
    return gal


# ------------------------------------------------------------------------------------------------ FP20's exact projector
_FP20 = os.path.join(CHAIN, "FP20_esd_projection_fix.py")
_PNS, _ = exec_slices(_FP20, [("def shell_mats(edges, Rv):", "# ================================================================================================= the record's projectors (loaded)")],
                      ns={"np": np, "math": math}, name="fp20_projectors")
shell_mats = _PNS["shell_mats"]
ESDFix = _PNS["ESDFix"]
