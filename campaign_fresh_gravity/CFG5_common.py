#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG5_common -- shared machinery for lane CFG5 (the radial acceleration relation as a fossil of collapse).

Nothing here is a result.  It holds:
  * the lane's constants: both a0 footings (charter: 9.3603e-11 canonical, 1.1312e-10 alt), the record's machinery
    footings used only by controls (9.3619e-11 / 1.1279e-10), a Planck-2018 LCDM background (the dark field is cold and
    pressureless before collapse: GDM theorem, FL1 F5), and f_b = Omega_b/Omega_m;
  * the SPARC loader in the record's L61/L92 recipe (Upsilon_d = 0.5, Upsilon_b = 0.7, eV/V < 0.10, >= 3 points);
  * the collapse-time halo population the dark field inherits (NFW halos, a declared concentration-mass relation, a
    declared stellar-to-halo relation) -- the SAME inputs any LCDM control uses;
  * the lane's one physical ingredient, the vacuum stress cap, and the fossil operations built from it
    (inside-out capping, escape against the kick, adiabatic contraction as the bracket);
  * FP20's exact lensing projector, executed read-only from the committed source (never esd_of_M / esd_from_mlens /
    project_M2).
Run nothing from here directly.  All paths are repository-relative.
"""
import os, sys, io, json, math, time, glob, builtins, contextlib, warnings

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "2")                                   # the machine is shared: at most two threads
import numpy as np
from scipy.optimize import brentq

warnings.filterwarnings("ignore", category=RuntimeWarning)
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DATA = os.path.join(REPO, "real_research", "data")
_trap = getattr(np, "trapezoid", None) or np.trapz


def rel(p):
    return os.path.relpath(p, REPO)


# ============================================================================================ constants (SI unless stated)
G = 6.674e-11                    # the record's SPARC value (L61/L92)
G_SI = 6.67430e-11
C_SI = 2.99792458e8
MSUN = 1.989e30
KPC = 3.0857e19
MPC = 3.0857e22
PC = 3.0857e16
GK = 4.30091727e-6               # kpc (km/s)^2 / Msun
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}          # the charter's footings (this lane's own numbers)
FOOT_REC = {"canonical": 9.3619e-11, "alt": 1.1279e-10}      # the record's machinery footings (controls only)
KAPPA = 0.5                      # FITTED (core); Z = 2 sqrt(8 pi/3) = 5.7888
Z_CORE = 2 * math.sqrt(8 * math.pi / 3)

# Planck 2018 (TT,TE,EE+lowE+lensing) -- the cold dark field's linear cosmology is LCDM's (GDM theorem, FL1 F5)
H_LITTLE = 0.6736
OMB_H2, OMC_H2 = 0.02237, 0.1200
OMEGA_NU_H2 = 0.00064            # one massive neutrino of 0.06 eV
OMEGA_M = (OMB_H2 + OMC_H2 + OMEGA_NU_H2) / H_LITTLE ** 2
OMEGA_B = OMB_H2 / H_LITTLE ** 2
OMEGA_L = 1.0 - OMEGA_M
F_B = OMEGA_B / OMEGA_M          # the cosmic baryon fraction
H0_SI = 100 * H_LITTLE * 1e3 / MPC
RHO_CRIT0_SI = 3 * H0_SI ** 2 / (8 * math.pi * G_SI)
RHO_LAMBDA_SI = OMEGA_L * RHO_CRIT0_SI
RHOC0_KPC = 277.5 * H_LITTLE ** 2          # Msun/kpc^3 (= 2.775e11 h^2 Msun/Mpc^3)


def Ez(z):
    return math.sqrt(OMEGA_M * (1 + z) ** 3 + OMEGA_L)


# ============================================================================================ the vacuum stress cap (THE PRINCIPLE)
def P_cap(a0):
    """the stress limit: 8 pi G P_c = a0^2, i.e. P_c = a0^2/(8 pi G) = (kappa^2/8 pi) rho_Lambda c^2 [Pa]."""
    return a0 ** 2 / (8 * math.pi * G_SI)


def g_cap(a0, fb=F_B):
    """the cap the principle writes on the dark field's own pull at collapse, for a collisionless mixture whose baryons still
    follow the dark field (fraction fb): P_d = (1 - fb) g^2/(8 pi G) <= a0^2/(8 pi G) => g_d = (1 - fb) g <= sqrt(1 - fb) a0."""
    return math.sqrt(1.0 - fb) * a0


# ============================================================================================ small utilities
class Lane:
    """check / banner / results bookkeeping in the record's convention (load-bearing failures -> rc = 1)."""

    def __init__(self, slug, lane_id):
        self.slug, self.lane, self.T0 = slug, lane_id, time.time()
        self.MUTATE = os.environ.get("MUTATE", "0") == "1"
        self.CH = []
        self.OUT = {"lane": lane_id, "mutate": self.MUTATE, "checks": {}, "numbers": {}, "ledger": []}

    def P(self, *a):
        print(*a, flush=True)

    def banner(self, t):
        self.P("\n" + "=" * 116 + "\n" + t + "\n" + "=" * 116)

    def el(self):
        return f"[{time.time() - self.T0:.0f}s]"

    def check(self, name, measured, ok, reading="", load_bearing=True):
        ok = bool(ok)
        self.CH.append((name, ok, load_bearing))
        self.OUT["checks"][name.split()[0]] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing, "name": name}
        self.P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
        if reading:
            self.P(f"         reading:  {reading}")
        return ok

    def ledger(self, link, status, text, basis):
        self.OUT["ledger"].append(dict(link=link, status=status, text=text, basis=basis))
        self.P(f"    {link:6s} {status:10s} {text}  --  {basis}")

    def finish(self):
        n_fail = sum(1 for _, ok, lb in self.CH if lb and not ok)
        self.OUT["summary"] = dict(checks_pass=sum(ok for _, ok, _ in self.CH), checks=len(self.CH),
                                   load_bearing_failed=n_fail, runtime_s=round(time.time() - self.T0, 1))
        suffix = "_MUTATE" if self.MUTATE else ""
        path = os.path.join(HERE, f"{self.slug}_results{suffix}.json")
        json.dump(jclean(self.OUT), open(path, "w"), indent=1)
        self.P(f"\n  checks: {sum(ok for _, ok, _ in self.CH)}/{len(self.CH)} pass; load-bearing failures: {n_fail}; "
               f"wrote {rel(path)}   {self.el()}")
        return 1 if n_fail else 0


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


def ro_open(file, mode="r", *a, **k):
    """read-only open for re-executed committed lanes (their file writes are refused)."""
    if any(c in mode for c in "wax+"):
        raise PermissionError(f"CFG5 refuses to write {file!r} from a re-executed lane")
    return builtins.open(file, mode, *a, **k)


@contextlib.contextmanager
def quiet_env(**env):
    old = {k: os.environ.get(k) for k in env}
    os.environ.update({k: str(v) for k, v in env.items()})
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            yield buf
    finally:
        for k, v in old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


# ============================================================================================ SPARC (the record's L61/L92 recipe)
UPS_D, UPS_B = 0.5, 0.7


def read_sparc_master():
    lines = open(os.path.join(DATA, "SPARC_Lelli2016c.mrt"), encoding="latin-1").read().splitlines()
    last = max(i for i, l in enumerate(lines) if l.startswith("-----"))
    rows = {}
    for line in lines[last + 1:]:
        f = line.split()
        if len(f) < 18:
            continue
        try:
            rows[f[0]] = dict(D=float(f[2]), inc=float(f[5]), L36=float(f[7]), Reff=float(f[9]), Rdisk=float(f[11]),
                              MHI=float(f[13]), Vflat=float(f[15]), eVflat=float(f[16]), Q=int(f[17]))
        except ValueError:
            continue
    return rows


def load_sparc(ups_d=UPS_D, ups_b=UPS_B):
    """L92's loader exactly (155 galaxies / 2786 points at the record's Upsilons); keeps the components for re-scaling."""
    master = read_sparc_master()
    gal = []
    for fn in sorted(glob.glob(os.path.join(DATA, "sparc_data", "*_rotmod.dat"))):
        name = os.path.basename(fn).replace("_rotmod.dat", "")
        if name not in master:
            continue
        m = master[name]
        try:
            d = np.loadtxt(fn, comments="#")
        except Exception:
            continue
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        r = d[:, 0] * KPC; Vo = d[:, 1] * 1e3; eV = d[:, 2] * 1e3
        Vg = d[:, 3] * 1e3; Vd = d[:, 4] * 1e3; Vb = d[:, 5] * 1e3
        Vb2 = Vg * np.abs(Vg) + ups_d * Vd * np.abs(Vd) + ups_b * Vb * np.abs(Vb)
        msk = (r > 0) & (Vo > 0) & (Vb2 > 0) & (eV / np.maximum(Vo, 1) < 0.10)
        if msk.sum() < 3:
            continue
        Mstar = ups_d * m["L36"] * 1e9; Mgas = 1.33 * m["MHI"] * 1e9
        gal.append(dict(name=name, r=r[msk], Vo=Vo[msk], eV=eV[msk], Vg=Vg[msk], Vd=Vd[msk], Vbul=Vb[msk],
                        gb=Vb2[msk] / r[msk], go=Vo[msk] ** 2 / r[msk], Mstar=Mstar, Mgas=Mgas, Mb=Mstar + Mgas,
                        inc=m["inc"], Q=m["Q"], D=m["D"], L36=m["L36"], Rdisk=m["Rdisk"], Vflat=m["Vflat"],
                        eVflat=m["eVflat"]))
    return gal


def nu_rar(y):
    y = np.asarray(y, float)
    return 1.0 / (-np.expm1(-np.sqrt(y)))


def nu_simple(y):
    y = np.asarray(y, float)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


def nu_p2(y):
    y = np.asarray(y, float)
    return np.sqrt(1.0 + 1.0 / y)


def _h_rar(y):
    z = np.sqrt(y)
    return y / np.expm1(z)


def nu_mono(y):
    """the record's standing kernel (XC4): nu_RAR up to y* = 2.3374, then the monotone log splice with delta = 0.05."""
    y = np.asarray(y, float)
    from scipy.optimize import brentq as _bq
    dh = lambda t: (2 * np.expm1(math.sqrt(t)) - math.sqrt(t) * (1 + np.expm1(math.sqrt(t)))) / (2 * np.expm1(math.sqrt(t)) ** 2)
    yp = _bq(dh, 1.0, 5.0); hp = _h_rar(yp); delta = 0.05
    ys = _bq(lambda t: dh(t) - delta * hp / (t + yp), 1.0, yp)
    h = np.where(y <= ys, _h_rar(np.maximum(y, 1e-300)), _h_rar(ys) + delta * hp * np.log((y + yp) / (ys + yp)))
    return 1.0 + h / y


# ============================================================================================ the halo population (declared inputs, shared with LCDM)
def m_nfw(x):
    x = np.asarray(x, float)
    return np.where(x < 1e-4, x * x / 2 - 2 * x ** 3 / 3, np.log1p(np.maximum(x, 1e-4)) - np.maximum(x, 1e-4) / (1 + np.maximum(x, 1e-4)))


def c200_dm14(M200_msun, z=0.0):
    """the concentration-mass relation for NFW M200c halos in Planck cosmology (declared; the record's c_dm14, M in Msun/h)."""
    a = 0.520 + (0.905 - 0.520) * math.exp(-0.617 * z ** 1.21)
    b = -0.101 + 0.026 * z
    return 10 ** (a + b * np.log10(np.asarray(M200_msun) * H_LITTLE / 1e12))


def ms_of_mh(Mh, z=0.0):
    """a declared stellar-to-halo mass relation (abundance matching, 2013 form; its z-dependence)."""
    zz = z / (1 + z)
    M1 = 10 ** (11.590 + 1.195 * zz); N = 0.0351 - 0.0247 * zz; be = 1.376 - 0.826 * zz; ga = 0.608 + 0.329 * zz
    return Mh * 2 * N / ((Mh / M1) ** (-be) + (Mh / M1) ** ga)


def mh_of_ms(Ms, z=0.0):
    Ms = max(float(Ms), 1e5)
    return 10 ** brentq(lambda lm: math.log10(ms_of_mh(10 ** lm, z)) - math.log10(Ms), 7.0, 16.5)


def nfw_halo(M200_msun, z=0.0, c=None):
    """r200 [m], rs [m], c and the enclosed-mass function [kg] of a total NFW halo at redshift z."""
    c = float(c200_dm14(M200_msun, z)) if c is None else float(c)
    M = M200_msun * MSUN
    rho_c = RHO_CRIT0_SI * Ez(z) ** 2
    r200 = (3 * M / (4 * math.pi * 200 * rho_c)) ** (1 / 3)
    rs = r200 / c
    Mfun = lambda r: M * m_nfw(np.asarray(r) / rs) / float(m_nfw(c))
    return dict(M=M, r200=r200, rs=rs, c=c, M_of=Mfun, rho_s=M / (4 * math.pi * rs ** 3 * float(m_nfw(c))))


# ============================================================================================ the fossil operations
def cap_inside_out(R, Mprof, Mcap):
    """removal only, inside out: M_new(r) = max(M_new(r-), min(M_new(r-) + dM(r), Mcap(r))).
    It keeps every shell's mass where the cap allows it and removes the excess where it does not (density >= 0)."""
    dM = np.diff(np.concatenate([[0.0], np.asarray(Mprof, float)]))
    dM = np.maximum(dM, 0.0)
    out = np.empty(len(R)); cur = 0.0
    Mcap = np.asarray(Mcap, float)
    for i in range(len(R)):
        cur = max(cur, min(cur + dM[i], Mcap[i]))
        out[i] = cur
    return out


def v_esc_of(R, Mtot, r_out):
    """escape speed [m/s] on the grid R from an enclosed-mass profile truncated at r_out (point mass outside)."""
    R = np.asarray(R, float); Mtot = np.asarray(Mtot, float)
    phi_out = -G_SI * Mtot[-1] / r_out
    integrand = G_SI * Mtot / R ** 2
    # Phi(r) = Phi(r_out) - int_r^r_out g dr
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (integrand[1:] + integrand[:-1]) * np.diff(R))])
    phi = phi_out - (cum[-1] - cum)
    return np.sqrt(np.maximum(-2 * phi, 0.0))


def blumenthal(R, Md_i, Mb_i, Mb_final_fn):
    """adiabatic contraction of the dark shells (circular-orbit invariant r M(r)): r_f [Mb_f(r_f) + Md(r_i)] = r_i [Md(r_i) + Mb_i(r_i)].
    Returns the dark enclosed mass on the final radii (sorted).  Used only as the contraction bracket."""
    R = np.asarray(R, float); Md_i = np.asarray(Md_i, float); Mb_i = np.asarray(Mb_i, float)
    lhs = R * (Md_i + Mb_i)
    f = lambda r: r * (Mb_final_fn(r) + Md_i) - lhs            # increasing in r for every shell
    lo = R * 1e-4
    hi = R.copy()
    for _ in range(60):                                          # expand the bracket where the shell moves out
        bad = f(hi) < 0
        if not bad.any():
            break
        hi = np.where(bad, hi * 1.5, hi)
    flo = f(lo)
    for _ in range(70):                                          # vectorised bisection (relative precision ~1e-21)
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        lo = np.where(fm < 0, mid, lo)
        hi = np.where(fm < 0, hi, mid)
    rf = np.where(flo < 0, 0.5 * (lo + hi), R * 1e-4)
    o = np.argsort(rf)
    return rf[o], Md_i[o]


# ============================================================================================ FP20's exact projector (read-only, from the committed source)
def load_fp20_projector():
    """execute ONLY FP20's projector section (shell_mats, ESDFix, M2Fix, CellFix) from the committed file."""
    p = os.path.join(REPO, "real_research", "derivation_chain_2026", "FP20_esd_projection_fix.py")
    src = open(p).read()
    a = src.index("# ================================================================================================= the projectors")
    b = src.index("# ================================================================================================= the record's projectors (loaded)")
    ns = {"np": np, "math": math, "__name__": "fp20_projectors"}
    exec(compile("\n" * src[:a].count("\n") + src[a:b], p, "exec"), ns)
    return ns


def classy_background(z_max_pk=12.0, kmax=50.0, extra=None):
    """CLASS 3.3.4 in the lane's Planck-2018 LCDM (the cold dark field before collapse)."""
    from classy import Class
    cl = Class()
    pars = {"h": H_LITTLE, "omega_b": OMB_H2, "omega_cdm": OMC_H2, "A_s": 2.1e-9, "n_s": 0.9649, "tau_reio": 0.0544,
            "N_ur": 2.0328, "N_ncdm": 1, "m_ncdm": 0.06, "YHe": 0.2454, "output": "mPk", "P_k_max_h/Mpc": kmax,
            "z_max_pk": z_max_pk}
    if extra:
        pars.update(extra)
    cl.set(pars)
    cl.compute()
    return cl
