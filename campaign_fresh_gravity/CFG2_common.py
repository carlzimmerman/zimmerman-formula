#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG2_common -- shared machinery for lane CFG2 (GR plus a vacuum-regulated dark field).

Nothing here is a result.  It holds:
  * the base: a0 = kappa c sqrt(G rho_Lambda) on the two footings, read from the chain's committed FP0 JSON (canonical
    9.3603e-11, alt 1.1312e-10 m/s^2); kappa = 1/2 is FITTED; Z = 2 sqrt(8 pi/3) = 5.7888 (Z == kappa's form); the
    vacuum stress scale P_Lambda = a0^2/(8 pi G) = kappa^2 rho_Lambda c^2/(8 pi) that the lane's principle uses;
  * the run harness every CFG2 script uses: a tee to the script's own .out (MUTATE=1 -> *_MUTATE.out), named checks with a
    load-bearing flag, the verdict line, rc = 1 on a load-bearing failure, and *_results[_MUTATE].json;
  * a read-only executor for the record's committed scripts (file writes refused, MUTATE forced to 0 inside, stdout
    captured) -- the pattern FP20 and CFG4 use;
  * the kernels: P2 = sqrt(1 + 1/y) (the framework's own law), nu_mono (FP1's committed definition, exec'd read-only),
    nu_RAR (reference only);
  * SPARC: the 175 rotmod files and the Lelli et al. 2016 master table, and the record's RAR statistic (FP1 C0/C2 =
    real_research/rar_framework_a0_mlfit.py's: weighted rms of log g_obs - log g_model, weights (V/e_V)^2 clipped at
    1 km/s, Upsilon_bul = 1.4 Upsilon_disk, one global Upsilon_disk profiled on 0.30-1.20 step 0.01);
  * the lane's galaxy laws in the spherical (enclosed-mass) reading of the rotmod baryons, vectorised over the Upsilon grid:
      E  the field-stress law (algebraic): |g|^2 = |g_N|^2 + a0 |g_N|  (= P2 at every radius);
      F  the medium-pressure law: hydrostatic dark fluid with P_d = a0 |g_N| / (8 pi G), g_N the enclosed-baryon field;
      Pi the gravity-only pressure law P_d = Pi(|g|) that reproduces P2 exactly around a point mass;
      S  stress saturation (P_d = min(|g|^2, a0^2)/(8 pi G), the stress-free branch);
      T  thermal: an isothermal dark sphere with central pressure P_Lambda and sigma^4 = G M_b a0 / 4;
  * the record's LambdaCDM conventions (copied with attribution): Moster+2013's stellar-to-halo relation as the record
    inverts it (hunt_2026/h84_eg_1to5Mpc.py, prep_2026/rar_origin_2026/rar_origin_detector_2026.py), the Dutton & Maccio
    2014 concentration, the record's Planck-2018 cosmology (hunt_2026/hunt_lib.py);
  * FP20's exact spherical projector (exec'd from FP20's committed source): the only projector CFG2 uses.

Run nothing from here directly.
"""
import os
import sys
import io
import json
import math
import time
import builtins
import contextlib

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
import numpy as np
from scipy.optimize import brentq

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
AU = 1.495978707e11
KAPPA = 0.5                                                   # FITTED (never derived)
Z_FRAME = 2.0 * math.sqrt(8.0 * math.pi / 3.0)               # 5.7888; Z == kappa's form
_FP0 = json.load(open(os.path.join(CHAIN, "FP0_core_postulates_results.json")))["numbers"]
A0 = {"canonical": float(_FP0["a0_canonical"]), "alt": float(_FP0["a0_rho_total"])}
RHO_LAMBDA = float(_FP0["rho_Lambda"])
FOOTS = ("canonical", "alt")
assert abs(A0["canonical"] - 9.3603e-11) < 1e-15 and abs(A0["alt"] - 1.1312e-10) < 1e-15
P_LAMBDA = {f: A0[f] ** 2 / (8 * math.pi * G_SI) for f in FOOTS}                      # the vacuum stress scale [Pa]
SIGMA_M = {f: A0[f] / (2 * math.pi * G_SI) / (MSUN / PC ** 2) for f in FOOTS}     # a0/(2 pi G) [Msun/pc^2]
GK = G_SI * MSUN / KPC / 1e6                                  # G in kpc (km/s)^2 / Msun
A0K = {f: A0[f] * KPC / 1e6 for f in FOOTS}                   # a0 in (km/s)^2 / kpc
KPC_REC = 3.0857e19                                          # the record's kpc in its SPARC statistic (FP1 C0/C2, rar_framework_a0_mlfit)
A0K_REC = {f: A0[f] * KPC_REC / 1e6 for f in FOOTS}          # a0 in (km/s)^2/kpc as the record's statistic sees it


# ------------------------------------------------------------------------------------------------ run harness
class Run:
    """one script's run: tee to its own .out, named checks, results JSON, verdict and exit code."""

    def __init__(self, slug, lane="CFG2"):
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
        raise PermissionError(f"CFG2 refuses to write {file!r} from a re-executed committed script")
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
    """the framework's own law P2: g = sqrt(g_N^2 + g_N a0), i.e. nu = sqrt(1 + 1/y)."""
    y = np.maximum(np.asarray(y, float), 1e-300)
    return np.sqrt(1.0 + 1.0 / y)


def nu_rar(y):
    """the exponential RAR shape 1/(1 - exp(-sqrt y)) -- reference only."""
    y = np.maximum(np.asarray(y, float), 1e-12)
    return 1.0 / (-np.expm1(-np.sqrt(y)))


_FP1 = os.path.join(CHAIN, "FP1_static_sector.py")
_KNS, _ = exec_slices(_FP1, [("def _h_rar(y):", "KER, KNAME = ")],
                      ns={"np": np, "math": math, "brentq": brentq}, name="fp1_kernels")
nu_mono = _KNS["nu_mono"]                                     # FP1's committed nu_mono (L340's table), exec'd read-only


# ------------------------------------------------------------------------------------------------ SPARC
UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2)             # the record's Upsilon grid (FP1 C2)


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
        if len(tok) != 19:
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


def vbar2_grid(g, ups=UPS):
    """V_bar^2 [(km/s)^2] on (Upsilon grid, radii): the record's baryon model (Upsilon_bul = 1.4 Upsilon_disk)."""
    U = np.asarray(ups, float)[:, None]
    return np.sign(g["Vgas"])[None, :] * g["Vgas"][None, :] ** 2 + U * g["Vdisk"][None, :] ** 2 + 1.4 * U * g["Vbul"][None, :] ** 2


def mass_budget(g, ups=UPS):
    """total baryonic mass [Msun] per Upsilon: Upsilon (L36 - L_bul) + 1.4 Upsilon L_bul + 1.33 M_HI (L_bul from the rotmod
    bulge at the last radius, which a compact bulge has fully enclosed); and the stellar mass."""
    m = g["meta"]
    Lbul = float(g["R"][-1] * g["Vbul"][-1] ** 2 / GK)
    Ld = max(m["L36"] * 1e9 - Lbul, 0.0)
    U = np.asarray(ups, float)
    Mstar = U * Ld + 1.4 * U * Lbul
    return Mstar + 1.33 * m["MHI"] * 1e9, Mstar


def rar_sums(g, V2model, Vb2):
    """the record's per-galaxy weighted SSR and weight for model V^2 on the Upsilon grid (points with g_bar, g_obs, g_model > 0)."""
    R = g["R"]
    go = (g["Vobs"] * 1e3) ** 2 / (R * KPC_REC)
    gb = Vb2 * 1e6 / (R[None, :] * KPC_REC)
    gm = V2model * 1e6 / (R[None, :] * KPC_REC)
    ok = (gb > 0) & (go[None, :] > 0) & np.isfinite(gb) & (g["Vobs"][None, :] > 0) & (gm > 0) & np.isfinite(gm)
    w = 1.0 / (np.clip(g["eV"], 1, None) / np.clip(g["Vobs"], 1, None)) ** 2
    with np.errstate(divide="ignore", invalid="ignore"):
        r = np.where(ok, np.log10(np.where(ok, go[None, :], 1.0)) - np.log10(np.where(ok, gm, 1.0)), 0.0)
    S = np.sum(np.where(ok, w[None, :] * r ** 2, 0.0), axis=1)
    W = np.sum(np.where(ok, w[None, :], 0.0), axis=1)
    return S, W


def best_ups(S, W, wg=None):
    """profile one global Upsilon: (rms, Upsilon, index)."""
    wg = np.ones(S.shape[0]) if wg is None else wg
    with np.errstate(all="ignore"):                          # macOS Accelerate raises spurious FP flags inside matmul
        mse = np.sum(wg[:, None] * S, axis=0) / np.sum(wg[:, None] * W, axis=0)
    i = int(np.argmin(mse))
    return math.sqrt(mse[i]), float(UPS[i]), i


# ------------------------------------------------------------------------------------------------ the lane's galaxy laws
def law_E(Vb2, R, a0k, kernel=nu_p2):
    """field-stress law, algebraic at each radius: V^2 = V_bar^2 nu(g_N/a0) (P2: |g|^2 = |g_N|^2 + a0|g_N|)."""
    gN = Vb2 / R[None, :]
    with np.errstate(divide="ignore", invalid="ignore"):
        V2 = np.where(gN > 0, Vb2 * kernel(np.where(gN > 0, gN, 1.0) / a0k), Vb2)
    return V2


def _grid_mass(Vb2, R, nfine=4000, inner=0.2):
    """enclosed baryonic 'spherical-equivalent' mass M_b(<r) = r V_bar^2 / G on a fine log grid (log-log interpolation of the
    rotmod points; M_b ~ r^3 inside the first point; clipped at 1e-3 Msun where V_bar^2 <= 0)."""
    rr = np.geomspace(R[0] * inner, R[-1], nfine)
    Mb = np.maximum(R[None, :] * Vb2 / GK, 1e-3)
    lr = np.log(R)
    lrr = np.log(rr)
    out = np.empty((Mb.shape[0], nfine))
    for i in range(Mb.shape[0]):
        out[i] = np.exp(np.interp(lrr, lr, np.log(Mb[i])))
    inn = rr < R[0]
    out[:, inn] = Mb[:, :1] * (rr[None, inn] / R[0]) ** 3
    return rr, out


def _integrate(rr, rhs, M0):
    """midpoint (RK2) integration of dM_d/dr = rhs(i, r, M_d) on the grid, vectorised over rows; M_d clipped >= 0 growth."""
    Md = np.zeros((M0.shape[0], len(rr)))
    for i in range(1, len(rr)):
        h = rr[i] - rr[i - 1]
        k1 = np.maximum(rhs(i - 1, rr[i - 1], Md[:, i - 1], 0.0), 0.0)
        k2 = np.maximum(rhs(i - 1, rr[i - 1] + 0.5 * h, Md[:, i - 1] + 0.5 * h * k1, 0.5), 0.0)
        Md[:, i] = Md[:, i - 1] + h * k2
    return Md


def _interp_rows(rr, Md, R):
    return np.array([np.interp(R, rr, Md[i]) for i in range(Md.shape[0])])


def law_F(Vb2, R, a0k, nfine=4000):
    """medium-pressure law: a static dark fluid in hydrostatic equilibrium in the total field whose pressure is the geometric
    mean of the vacuum stress and the baryons' field stress, P_d = a0 g_N/(8 pi G), g_N = G M_b(<r)/r^2 (enclosed).
    dP/dr = -rho g  =>  dM_d/dr = (a0 r^2/(2 G)) (-dg_N/dr) / g   (dark medium absent where g_N rises)."""
    rr, Mb = _grid_mass(Vb2, R, nfine)
    gN = GK * Mb / rr[None, :] ** 2
    dgN = np.gradient(gN, rr, axis=1)

    def rhs(i, r, Md, frac):
        gNi = gN[:, i] + frac * (gN[:, i + 1] - gN[:, i]) if frac else gN[:, i]
        dgi = dgN[:, i] + frac * (dgN[:, i + 1] - dgN[:, i]) if frac else dgN[:, i]
        gt = gNi + GK * Md / r ** 2
        return (a0k * r * r / (2 * GK)) * np.maximum(-dgi, 0.0) / gt
    Md = _integrate(rr, rhs, Mb)
    return Vb2 + GK * _interp_rows(rr, Md, R) / R[None, :]


def Pi_prime(g, a0k):
    """Pi(g) = (a0/(16 pi G))(sqrt(a0^2 + 4 g^2) - a0): the pressure-of-total-field law that is P2 around a point mass; Pi'(g)."""
    return (a0k / (16 * math.pi * GK)) * 4 * g / np.sqrt(a0k ** 2 + 4 * g ** 2)


def law_Pi(Vb2, R, a0k, nfine=4000, saturate=False):
    """gravity-only pressure law P_d = Pi(|g|) (the dark medium responds to its own support acceleration only), hydrostatic:
    dM_d/dr = Pi'(g) (2 M r - r^2 M_b') / (Pi'(g) r^2 + M/(4 pi)).  saturate=True uses the sharp cap
    P_d = min(g^2, a0^2)/(8 pi G) (stress saturation S: Pi' = g/(4 pi G) below a0, 0 above)."""
    rr, Mb = _grid_mass(Vb2, R, nfine)
    dMb = np.gradient(Mb, rr, axis=1)

    def rhs(i, r, Md, frac):
        Mbi = Mb[:, i] + frac * (Mb[:, i + 1] - Mb[:, i]) if frac else Mb[:, i]
        dMbi = dMb[:, i] + frac * (dMb[:, i + 1] - dMb[:, i]) if frac else dMb[:, i]
        M = Mbi + Md
        g = GK * M / r ** 2
        if saturate:
            Pp = np.where(g < a0k, g / (4 * math.pi * GK), 0.0)
        else:
            Pp = Pi_prime(g, a0k)
        return Pp * (2 * M * r - r * r * dMbi) / (Pp * r * r + M / (4 * math.pi))
    Md = _integrate(rr, rhs, Mb)
    return Vb2 + GK * _interp_rows(rr, Md, R) / R[None, :]


def law_T(Vb2, R, a0k, Mb_tot, cap=1.0, nfine=3000):
    """thermal: an isothermal dark sphere in the total potential, sigma^4 = G M_b a0/4 (the BTFR temperature), central
    pressure cap * P_Lambda (rho_0 = cap a0^2/(8 pi G sigma^2)); integrated from the centre (RK2 in r)."""
    rr, Mb = _grid_mass(Vb2, R, nfine, inner=0.05)
    sig2 = np.sqrt(GK * np.asarray(Mb_tot, float) * a0k / 4.0)[:, None]               # (km/s)^2
    rho0 = cap * a0k ** 2 / (8 * math.pi * GK * sig2)                                 # Msun/kpc^3
    Md = np.zeros_like(Mb)
    psi = np.zeros_like(Mb)
    r0 = rr[0]
    Md[:, 0] = (4 * math.pi / 3) * rho0[:, 0] * r0 ** 3
    for i in range(1, len(rr)):
        h = rr[i] - rr[i - 1]
        r = rr[i - 1]
        f1m = 4 * math.pi * r * r * rho0[:, 0] * np.exp(-psi[:, i - 1])
        f1p = GK * (Mb[:, i - 1] + Md[:, i - 1]) / (r * r * sig2[:, 0])
        rm = r + 0.5 * h
        Mbm = 0.5 * (Mb[:, i - 1] + Mb[:, i])
        f2m = 4 * math.pi * rm * rm * rho0[:, 0] * np.exp(-(psi[:, i - 1] + 0.5 * h * f1p))
        f2p = GK * (Mbm + Md[:, i - 1] + 0.5 * h * f1m) / (rm * rm * sig2[:, 0])
        Md[:, i] = Md[:, i - 1] + h * f2m
        psi[:, i] = psi[:, i - 1] + h * f2p
    return Vb2 + GK * _interp_rows(rr, Md, R) / R[None, :]


# ------------------------------------------------------------------------------------------------ the record's LambdaCDM conventions
H_LIB = 0.674                                                  # hunt_2026/hunt_lib.py (Planck 2018)
H0_LIB = 100 * H_LIB * 1e3 / MPC
OM_B_LIB = 0.02237 / H_LIB ** 2
OM_C_LIB = 0.1200 / H_LIB ** 2
OM_M_LIB = OM_B_LIB + OM_C_LIB
OM_L_LIB = 1 - OM_M_LIB
RHO_CRIT_LIB = 3 * H0_LIB ** 2 / (8 * math.pi * G_SI)       # kg/m^3


def moster_ratio(Mh):
    """Moster, Naab & White 2013 z = 0 stellar-to-halo ratio as the record writes it (rar_origin_detector_2026.py:86)."""
    M1 = 10 ** 11.59
    N = 0.0351
    beta = 1.376
    gam = 0.608
    return 2 * N / ((Mh / M1) ** (-beta) + (Mh / M1) ** gam)


def Mh_of_Mstar(Ms):
    """the record's inversion: M_200 [Msun] for a stellar mass [Msun]."""
    f = lambda lm: math.log10(moster_ratio(10 ** lm) * 10 ** lm) - math.log10(Ms)
    return 10 ** brentq(f, 6.0, 16.5)


def c_DM14(Mh, z=0.0):
    """Dutton & Maccio 2014 c200 (Planck), M in Msun; z-dependence as hunt_2026/h84_eg_1to5Mpc.py writes it."""
    a = 0.520 + 0.385 * math.exp(-0.617 * max(z, 1e-6) ** 1.21)
    b = -0.101 + 0.026 * z
    return 10 ** (a + b * math.log10(Mh * H_LIB / 1e12))


def rho_crit_z(z):
    return RHO_CRIT_LIB * (OM_M_LIB * (1 + z) ** 3 + OM_L_LIB)


def R200_of(M200, z=0.0):
    """R_200 [m] for M_200 [Msun] (200 x critical)."""
    return (3 * M200 * MSUN / (4 * math.pi * 200 * rho_crit_z(z))) ** (1.0 / 3.0)


def M_nfw(r, M200, c, z=0.0):
    """NFW enclosed mass [Msun] at r [m]."""
    R2 = R200_of(M200, z)
    x = c * np.asarray(r, float) / R2
    return M200 * (np.log1p(x) - x / (1 + x)) / (math.log1p(c) - c / (1 + c))


def settled_capacity(Mb, R, a0):
    """the settled (P2) dark mass inside radius R [m] around baryons Mb [Msun] (monopole): sqrt(Mb^2 + a0 Mb R^2/G) - Mb."""
    MbK = Mb * MSUN
    return (math.sqrt(MbK ** 2 + a0 * MbK * R ** 2 / G_SI) - MbK) / MSUN


def scope(Mstar, Mb, a0, z=0.0):
    """the scope rule: a bound system settles iff the settled state can hold its accreted dark mass inside R_200.
    Returns (eta_avail = M_dark,accreted / capacity, M200, R200 [m])."""
    M200 = Mh_of_Mstar(Mstar)
    R2 = R200_of(M200, z)
    Mdacc = (OM_C_LIB / OM_M_LIB) * M200
    return Mdacc / settled_capacity(Mb, R2, a0), M200, R2


# ------------------------------------------------------------------------------------------------ FP20's exact projector
_FP20 = os.path.join(CHAIN, "FP20_esd_projection_fix.py")
_PNS, _ = exec_slices(_FP20, [("def shell_mats(edges, Rv):", "# ================================================================================================= the record's projectors (loaded)")],
                      ns={"np": np, "math": math}, name="fp20_projectors")
shell_mats = _PNS["shell_mats"]
ESDFix = _PNS["ESDFix"]
