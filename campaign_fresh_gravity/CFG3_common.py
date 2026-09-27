#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG3_common -- shared machinery for lane CFG3 (vacuum-regulated gravity from one founding principle).

THE PRINCIPLE (stated once here; derived from in CFG3_principle.py):
  "The vacuum answers matter that has fallen behind it."  Empty space has its own expansion rate, H_Lambda =
  sqrt(8 pi G rho_Lambda / 3), and its own energy density rho_Lambda.  Matter that still expands at least as fast as empty
  space would (the Hubble flow, the whole linear web: H(z) > H_Lambda always) is carried along, and gravity there is plain GR.
  Matter that has fallen behind (local expansion rate theta/3 < H_Lambda at some time: every bound system and its infall
  zone) holds the vacuum back, and the vacuum answers that matter's gravity, as a whole region, in the region's own free
  fall.  It answers as a bath at its own free-fall rate a0/c = kappa sqrt(G rho_Lambda): each free-fall mode of the ordinary
  matter is amplified by its Bose occupation.  The dark component is a state of the vacuum itself and is not answered.
  The answer is coherent only above a length l* (the vacuum state's own Airy length at a0, TIED to the dark field's mass).

This file holds: paths and constants (FP0's committed a0 pair), the kernels (the derived Bose kernel; the record's nu_RAR,
nu_mono, P2 for controls; the Fermi-Dirac MUTATE kernel), the run/output harness (.out, _results.json, MUTATE suffixes),
the read-only exec harness (file writes refused, MUTATE=0 inside), the flat-LCDM background and growth used by the gate
model, EH98 (no-wiggle, copied from FP1 E with attribution) for sigma(R), the gate-radius model (the principle's region edge,
theta = 3 H_Lambda, from exact spherical shells around the mean linear profile of a halo's Lagrangian patch), and Moster,
Naab & White 2013's stellar-to-halo relation (a data-derived mapping, used only to place KiDS lenses' Lagrangian patches).
No file outside campaign_fresh_gravity/CFG3_* is written by any CFG3 script.
"""
import os, sys, io, json, math, time, contextlib, builtins, warnings
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "2"
warnings.filterwarnings("ignore")
import numpy as np

np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CHAIN = os.path.join(REPO, "real_research", "derivation_chain_2026")
HUB = os.path.join(REPO, "real_research", "cross_thread_review_2026_09_26")
HUNT = os.path.join(REPO, "hunt_2026")
MUTATE = os.environ.get("MUTATE", "0") == "1"
FOOTS = ("canonical", "alt")
_trap = getattr(np, "trapezoid", None) or np.trapz

# ------------------------------------------------------------------------------------------------ constants (SI)
C_SI, G_SI = 299792458.0, 6.67430e-11
MSUN = 1.98892e30
PC = 3.0856775814913673e16
KPC, MPC = 1e3 * PC, 1e6 * PC
AU = 1.495978707e11
HBAR = 1.054571817e-34
EV = 1.602176634e-19
# FP0's committed pair (the chain's footings) and the vacuum quantities
_FP0 = json.load(open(os.path.join(CHAIN, "FP0_core_postulates_results.json")))["numbers"]
A0 = {"canonical": float(_FP0["a0_canonical"]), "alt": float(_FP0["a0_rho_total"])}
RHO_L = float(_FP0["rho_Lambda"])
H_L = float(_FP0["H_Lambda"])
Z_FP0 = float(_FP0["Z"])
H0_FP0 = 67.4e3 / MPC
OML_FP0 = 0.6847
# the cosmology of the record's KiDS harness (FP1 E / L355: Planck 2018), used by the gate model, KiDS and the halo model
H_KIDS = 0.6736
OB_K, OC_K = 0.02237 / H_KIDS ** 2, 0.1200 / H_KIDS ** 2
OM_K = OB_K + OC_K
OL_K = 1.0 - OM_K
H0_K = 100 * H_KIDS * 1e3 / MPC
SIG8_K, NS_K = 0.8111, 0.9649
RHO_CRIT_K = 3 * H0_K ** 2 / (8 * math.pi * G_SI)
RHOM0_MSUN_MPC3 = OM_K * RHO_CRIT_K * MPC ** 3 / MSUN


# ------------------------------------------------------------------------------------------------ kernels
def nu_bose(y):
    """THE DERIVED KERNEL: nu = 1 + n_BE(x), x = t_vac/t_dyn = sqrt(y) (CFG3_principle D2)."""
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 1.0 + 1.0 / np.expm1(np.sqrt(y))


def nu_rar(y):
    """the record's nu_RAR, literally as FP1 writes it (identical to nu_bose: 1/(1 - e^-x) = 1 + 1/(e^x - 1))."""
    y = np.maximum(np.asarray(y, float), 1e-12)
    return 1.0 / (-np.expm1(-np.sqrt(y)))


def nu_fermi(y):
    """the MUTATE statistics: Fermi-Dirac occupation instead of Bose (no classical enhancement: nu -> 3/2 at y -> 0)."""
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 1.0 + 1.0 / (np.exp(np.minimum(np.sqrt(y), 700.0)) + 1.0)


def nu_p2(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return np.sqrt(1.0 + 1.0 / y)


def _h_rar(y):
    y = np.asarray(y, float)
    return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)


def _dh_rar(y, e=1e-6):
    return (_h_rar(y * (1 + e)) - _h_rar(y * (1 - e))) / (2 * y * e)


def _build_mono():
    """nu_mono exactly as FP1_static_sector.py:132-145 builds it (L340's construction), copied with attribution."""
    from scipy.optimize import brentq
    y_p = brentq(lambda y: float(_dh_rar(y)), 1.0, 5.0)
    h_p = float(_h_rar(y_p))
    lyg = np.linspace(-14, 14, 280001)
    yg = 10 ** lyg
    dh = np.maximum(_dh_rar(yg), 0.05 * h_p / (yg + y_p))
    hm = float(_h_rar(yg[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (dh[1:] + dh[:-1]) * np.diff(yg))])
    return lyg, hm, y_p


_LYG, _HM, Y_PEAK = _build_mono()


def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-14)
    return 1.0 + np.interp(np.log10(y), _LYG, _HM) / y


# ------------------------------------------------------------------------------------------------ run harness
class _Tee:
    def __init__(self, fh):
        self.fh, self.so = fh, sys.__stdout__

    def write(self, s):
        self.so.write(s); self.fh.write(s)

    def flush(self):
        self.so.flush(); self.fh.flush()


def jclean(o):
    if isinstance(o, dict):
        return {str(k): jclean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jclean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)):
        return float(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.ndarray):
        return [jclean(v) for v in o.tolist()]
    if isinstance(o, float) and not math.isfinite(o):
        return str(o)
    return o


class Run:
    """stdout tee'd to <slug>.out (or _MUTATE.out); checks; numbers; ledger; finish() writes <slug>_results[_MUTATE].json."""

    def __init__(self, slug, doc):
        self.slug, self.t0 = slug, time.time()
        outdir = os.environ.get("CFG3_OUTDIR", HERE)                          # development runs go to scratch (disclosed)
        self.out_path = os.path.join(outdir, slug + ("_MUTATE.out" if MUTATE else ".out"))
        self.json_path = os.path.join(outdir, slug + ("_results_MUTATE.json" if MUTATE else "_results.json"))
        self._fh = open(self.out_path, "w")
        sys.stdout = _Tee(self._fh)
        self.OUT = {"lane": "CFG3", "script": slug, "mutate": MUTATE, "checks": {}, "numbers": {}, "ledger": []}
        self.CH = []
        self.P(doc.strip())
        self.P(f"\n  inputs: a0 = {A0['canonical']:.4e} (canonical) / {A0['alt']:.4e} (alt) m/s^2 [FP0]; rho_Lambda = {RHO_L:.4e} kg/m^3; "
               f"H_Lambda = {H_L:.4e} 1/s; Z = {Z_FP0:.6f} (kappa = 1/2 FITTED)")

    @staticmethod
    def P(*a):
        print(*a, flush=True)

    def banner(self, t):
        self.P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)

    def el(self):
        return f"[{time.time() - self.t0:.0f} s]"

    def check(self, name, measured, ok, load_bearing=True, reading=None):
        ok = bool(ok)
        self.CH.append((name, ok, load_bearing))
        key = name.split()[0]
        k2, j = key, 1
        while k2 in self.OUT["checks"]:
            j += 1; k2 = f"{key}#{j}"
        self.OUT["checks"][k2] = {"ok": ok, "measured": str(measured), "load_bearing": bool(load_bearing), "name": name}
        self.P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
        if reading:
            self.P(f"         reading:  {reading}")
        return ok

    def num(self, key, val):
        self.OUT["numbers"][key] = jclean(val)

    def ledger(self, tag, status, text, where=""):
        self.OUT["ledger"].append(dict(tag=tag, status=status, text=text, where=where))
        self.P(f"    {tag:8s} {status:11s} {text}" + (f"  --  {where}" if where else ""))

    def finish(self):
        n = len(self.CH)
        npass = sum(1 for c in self.CH if c[1])
        lbf = [c[0].split()[0] for c in self.CH if (not c[1]) and c[2]]
        rep_f = [c[0].split()[0] for c in self.CH if (not c[1]) and not c[2]]
        rc = 1 if lbf else 0
        self.OUT.update(n_checks=n, n_pass=npass, load_bearing_failures=lbf, reported_failures=rep_f, rc=rc,
                        seconds=round(time.time() - self.t0, 1))
        with open(self.json_path, "w") as fh:
            json.dump(jclean(self.OUT), fh, indent=1)
        self.P(f"\n  {npass}/{n} checks pass; load-bearing failures: {len(lbf)} {lbf if lbf else ''}; reported failures: "
               f"{rep_f if rep_f else 'none'}; wrote {os.path.basename(self.json_path)} ({time.time() - self.t0:.0f} s)")
        self.P(f"rc = {rc}")
        sys.stdout = sys.__stdout__
        self._fh.close()
        return rc


# ------------------------------------------------------------------------------------------------ read-only exec harness
def _ro_open(file, mode="r", *a, **k):
    if any(c in mode for c in "wax+"):
        raise PermissionError(f"CFG3 refuses to write {file!r} from a re-executed record file")
    return builtins.open(file, mode, *a, **k)


@contextlib.contextmanager
def lane_env():
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


def exec_slices(path, slices, ns=None, name="lane"):
    """exec [start, stop) slices of a committed source in ONE namespace (file writes refused, MUTATE=0, stdout captured);
    start/stop are marker strings (first occurrence) or None.  Line numbers are preserved for tracebacks."""
    src = open(path).read()
    ns = {"__file__": path, "__name__": name} if ns is None else ns
    ns["open"] = _ro_open
    with lane_env() as buf:
        for (a, b) in slices:
            ia = 0 if a is None else src.index(a)
            ib = len(src) if b is None else src.index(b, ia)
            code = "\n" * src[:ia].count("\n") + src[ia:ib]
            exec(compile(code, path, "exec"), ns)
    return ns, buf.getvalue()


# ------------------------------------------------------------------------------------------------ background and growth (flat LCDM)
def E_of_a(a, om=OM_K, ol=OL_K):
    return np.sqrt(om / np.asarray(a, float) ** 3 + ol)


def growth_D(a, om=OM_K, ol=OL_K):
    """linear growth, D(1) = 1 (Heath's integral for flat LCDM)."""
    def raw(a1):
        aa = np.linspace(1e-5, a1, 20001)
        return E_of_a(a1, om, ol) * _trap(1.0 / (aa * E_of_a(aa, om, ol)) ** 3, aa)
    a = np.atleast_1d(np.asarray(a, float))
    d1 = raw(1.0)
    return np.array([raw(x) / d1 for x in a]) if a.size > 1 else raw(float(a[0])) / d1


def growth_f(a, om=OM_K, ol=OL_K, eps=1e-4):
    return (math.log(growth_D(a * (1 + eps), om, ol)) - math.log(growth_D(a * (1 - eps), om, ol))) / (math.log(1 + eps) - math.log(1 - eps))


# ------------------------------------------------------------------------------------------------ EH98 (FP1 E's T_eh, copied with attribution)
def T_eh(k):
    """FP1_static_sector.py:768-775 (EH98 no-wiggle), k in 1/Mpc."""
    th = 2.7255 / 2.7; omh2 = OM_K * H_KIDS * H_KIDS; fb = OB_K / OM_K
    s_ = 44.5 * np.log(9.83 / omh2) / np.sqrt(1 + 10 * (OB_K * H_KIDS * H_KIDS) ** 0.75)
    aG = 1 - 0.328 * np.log(431 * omh2) * fb + 0.38 * np.log(22.3 * omh2) * fb ** 2
    Gm = OM_K * H_KIDS * (aG + (1 - aG) / (1 + (0.43 * k * s_) ** 4)); q = k * th ** 2 / (Gm * H_KIDS)
    L_ = np.log(2 * np.e + 1.8 * q); C_ = 14.2 + 731 / (1 + 62.5 * q)
    return L_ / (L_ + C_ * q * q)


def W_th(x):
    x = np.asarray(x, float)
    out = np.empty_like(x)
    sm = x < 1e-3
    out[sm] = 1 - x[sm] ** 2 / 10
    xl = x[~sm]
    out[~sm] = 3 * (np.sin(xl) - xl * np.cos(xl)) / xl ** 3
    return out


KK = np.geomspace(1e-5, 200, 40000)                                                 # 1/Mpc
PK0 = KK ** NS_K * T_eh(KK) ** 2
PK0 *= SIG8_K ** 2 / _trap(PK0 * W_th(KK * 8 / H_KIDS) ** 2 * KK ** 2 / (2 * math.pi ** 2), KK)


def sigma2_cross(R1, R2):
    """<Delta_lin(<R1) Delta_lin(<R2)> at z = 0 (top-hats, comoving Mpc)."""
    return _trap(PK0 * W_th(KK * R1) * W_th(KK * R2) * KK ** 2, KK) / (2 * math.pi ** 2)


# ------------------------------------------------------------------------------------------------ the gate-radius model
DELTA_C = 1.686


def lagrangian_radius(Mh_msun):
    return (3 * Mh_msun / (4 * math.pi * RHOM0_MSUN_MPC3)) ** (1 / 3)


def gate_radius(Mh_msun, z_obs, n_shell=500, n_step=3000, a_i=0.02, xmax=30.0, threshold=None, profile_scale=1.0):
    """THE PRINCIPLE'S REGION EDGE around an isolated halo patch of Lagrangian mass Mh at redshift z_obs.
    Shells (Lagrangian radii R = 1.02 .. xmax R_L) start at a_i on the growing mode of the MEAN linear profile around a
    patch that collapses at z_obs, Delta_lin(<R, z_obs) = delta_c sigma_x^2(R, R_L)/sigma^2(R_L), and move under
    r'' = -(Om/2) R^3/r^2 + OL r (units H0 = 1, Mpc).  Outside the gated region gravity is GR and the phantom is
    compensated (net zero), so the edge is set by this Newtonian flow.  The fluid expansion theta = r^-2 d(r^2 v)/dr is
    tracked; a shell is gated once theta has dropped below 3 H_Lambda (hysteresis: once behind, always behind).
    Returns physical radii at z_obs [Mpc]: r_g (outermost contiguous gated shell), r_ta (outermost v <= 0 shell), and the
    Lagrangian mass inside r_g."""
    om, ol = OM_K, OL_K
    thr = 3 * math.sqrt(ol) if threshold is None else threshold                   # 3 H_Lambda / H0
    RL = lagrangian_radius(Mh_msun)
    R = RL * np.geomspace(1.02, xmax, n_shell)
    a_o = 1.0 / (1.0 + z_obs)
    Dz = growth_D(a_o)
    s2L = sigma2_cross(RL, RL)
    D0 = np.array([sigma2_cross(r_, RL) for r_ in R]) / s2L * DELTA_C / Dz * profile_scale   # Delta_lin(<R) at z = 0
    Di = growth_D(a_i)
    fi = growth_f(a_i)
    d_i = D0 * Di
    r = a_i * R * (1 - d_i / 3)
    v = E_of_a(a_i) * r * (1 - fi * d_i / 3)
    R3 = R ** 3
    lna = np.linspace(math.log(a_i), math.log(a_o), n_step)
    dl = lna[1] - lna[0]
    collapsed = np.zeros(n_shell, bool)
    theta_min = np.full(n_shell, np.inf)

    def rhs(lna_, r_, v_):
        E = float(E_of_a(math.exp(lna_)))
        rr = np.maximum(r_, 1e-6)
        return v_ / E, (-(om / 2) * R3 / rr ** 2 + ol * rr) / E

    def theta_of(r_, v_):
        q = r_ ** 2 * v_
        th = np.full_like(r_, np.nan)
        th[1:-1] = (q[2:] - q[:-2]) / ((r_[2:] - r_[:-2]) * r_[1:-1] ** 2)
        th[0] = (q[1] - q[0]) / ((r_[1] - r_[0]) * r_[0] ** 2)
        th[-1] = (q[-1] - q[-2]) / ((r_[-1] - r_[-2]) * r_[-1] ** 2)
        return th

    for i in range(n_step - 1):
        l0 = lna[i]
        k1r, k1v = rhs(l0, r, v)
        k2r, k2v = rhs(l0 + dl / 2, r + dl / 2 * k1r, v + dl / 2 * k1v)
        k3r, k3v = rhs(l0 + dl / 2, r + dl / 2 * k2r, v + dl / 2 * k2v)
        k4r, k4v = rhs(l0 + dl, r + dl * k3r, v + dl * k3v)
        r = r + dl / 6 * (k1r + 2 * k2r + 2 * k3r + k4r)
        v = v + dl / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        newc = (r < 0.02 * R * math.exp(lna[i + 1])) & ~collapsed
        collapsed |= newc | ~np.isfinite(r)
        r = np.where(collapsed, np.maximum(np.nan_to_num(r, nan=1e-3), 1e-3 * R), r)
        v = np.where(collapsed, 0.0, v)
        if i % 5 == 0 or i == n_step - 2:
            th = theta_of(r, v)
            ok = ~collapsed & np.isfinite(th)
            theta_min = np.where(ok, np.minimum(theta_min, th), theta_min)
    gated = collapsed | (theta_min < thr)
    idx = int(np.argmin(gated)) - 1 if not gated.all() else n_shell - 1       # outermost of the contiguous gated block
    idx = max(idx, 0)
    ta = np.where((v <= 0) | collapsed)[0]
    ita = int(ta.max()) if ta.size else 0
    return dict(r_g=float(r[idx]), R_g=float(R[idx]), M_g=float(4 * math.pi / 3 * RHOM0_MSUN_MPC3 * R[idx] ** 3),
                r_ta=float(r[ita]), R_ta=float(R[ita]), RL=float(RL), edge_at_grid_end=bool(idx == n_shell - 1),
                Delta_lin_edge=float(D0[idx] * Dz), theta_edge=float(theta_min[idx]), thr=float(thr))


# ------------------------------------------------------------------------------------------------ Moster, Naab & White 2013 (ApJ 770, 57), Table 1
def mstar_of_mh(Mh, z):
    zz = z / (1 + z)
    M1 = 10 ** (11.590 + 1.195 * zz); N = 0.0351 - 0.0247 * zz; b = 1.376 - 0.826 * zz; g = 0.608 + 0.329 * zz
    Mh = np.asarray(Mh, float)
    return 2 * N * Mh / ((Mh / M1) ** (-b) + (Mh / M1) ** g)


def mh_of_mstar(Ms, z):
    lg = np.linspace(9.0, 16.0, 7001)
    ms = mstar_of_mh(10 ** lg, z)
    return 10 ** np.interp(np.log10(Ms), np.log10(ms), lg)
