#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FP20 -- A BUG CORRECTION: THE RECORD'S KiDS 'LEAD GRADE' PROJECTION UNDER-PROJECTS.  FP18 (K2b) found that FP6's esd_of_M --
the Abel projection that turns a spherical mass profile into the KiDS-1000 excess surface density Delta Sigma(R) -- is low on a
singular isothermal sphere by 59% at 35 kpc and by 5-14% at 0.3-2.6 Mpc.  That function (the same code, copied) scores the
KiDS gate of FP6, FP9, FP11, FP12, FP13, FP1 E, FP14 and FP17, and of the record's L355 / L357 / AT1 / AT3 (switch-free).
This lane derives the correct projection, finds the bug exactly, validates every projector in use against analytic profiles,
and RE-SCORES every committed KiDS number of the chain with the corrected projection -- same data, covariance, fits,
2-halo treatment and conventions, only the projection swapped (in this lane's own namespace; no committed file is edited).

THE PROJECTION (derived).  For a spherical excess density rho(r) with enclosed mass M(<r), truncated at r_t (the record's grid
end, 30 Mpc) plus a central point mass M_b:
    Sigma(R)        = 2 Int_R^{r_t} rho(r) r dr / sqrt(r^2 - R^2)                     (integrable 1/sqrt singularity at r = R)
    M_2D(<R)        = M_b + M(<R) + Int_R^{r_t} 4 pi r^2 rho(r) [1 - sqrt(1 - R^2/r^2)] dr   (no singularity)
    Delta Sigma(R)  = M_2D(<R)/(pi R^2) - Sigma(R).
  Written for uniform-density shells (edges r_k, masses m_k = M(<r_{k+1}) - M(<r_k); exact for piecewise-constant rho and
  second-order in the grid for smooth rho): a shell contributes Sigma = 2 rho_k [sqrt((r_{k+1}^2 - R^2)_+) - sqrt((r_k^2 - R^2)_+)]
  and M_2D = m_k - (4 pi/3) rho_k [(r_{k+1}^2 - R^2)_+^{3/2} - (r_k^2 - R^2)_+^{3/2}] (evaluated as R^2 (r^2 + r s + s^2)/(r + s),
  s = sqrt(r^2 - R^2), to avoid cancellation).  The 1/sqrt singularity is integrated analytically and M_2D needs no inner
  extrapolation.  The mass inside the first grid radius (1 kpc) is kept as a central point.  THIS IS THE CORRECTED PROJECTION.

THE BUG (identified here, B section).  esd_of_M (FP6:356; FP1:707; L355:110; BS2's esd_from_M) computes
    Sig = W @ rho    with W the TRAPEZOID rule on the grid points r_j > R(1 + 1e-7) of 2 r/sqrt(r^2 - R^2)          (defect B)
    M_2D(<R) = 2 pi Int_{R_0}^{R} Sig R' dR' + pi R_0^2 Sig(R_0),   R_0 = 20 kpc                                   (defect A)
  (A) the projected mass inside R_0 = 20 kpc is taken as a uniform disc of surface density Sig(R_0); for an isothermal
      (Sigma ~ 1/R) profile the true value is 2 pi R_0^2 Sig(R_0): HALF the inner projected mass is lost.  The loss is a
      point-mass-like deficit ~ (R_0/R) Sigma(R): -57% at 35 kpc falling to -1% at 2.6 Mpc on the SIS.  A compact mass passed
      as extended (Mb = 0) inside R_0 is lost ENTIRELY.
  (B) the trapezoid skips the segment [R, r_1] next to the 1/sqrt(r - R) end point and mis-weights the first node; the error
      in Sigma(R) depends on where R falls between grid nodes (-6% .. +12% on the SIS), and Delta Sigma = M_2D/(pi R^2) - Sigma
      inherits it point by point (it is -12% at 2.6 Mpc on the SIS).
  L352's project_M2 (used by L352, L359, L360, AT3's switched gate, FP4/FP10/FP15/FP16 via kids_switched, DE8, DE10 and the hub's
  XR9/XR14/XR28/XR29) shares defect B but not A: its inner term is 2 pi R_0^2 Sig(R_0) (R_0 = 5 kpc), exact only for Sigma ~ 1/R,
  and its annulus average reads M_2D only (which smooths B's scatter): -3% on the SIS, -3..+11% on NFW halos, and up to +187% /
  -123% at 35 kpc on the cored or hollowed carrier templates those lanes project.

CHECKS
  K  CONTROLS: K0 the record's P1 projections (FP6, FP1 E [= FP14/FP17's], L355 [= L357/AT1/AT3's]) are the same function;
     K1 the harness reproduces each lane's committed KiDS numbers with the committed projection.
  V  THE ANALYTIC STANDARD: V1 [load-bearing; MUTATE must fail] the corrected projection reproduces the singular isothermal
     sphere, NFW (Wright & Brainerd 2000) and a point mass (as the analytic term and as a compact extended mass) to < 0.1%
     at the 15 KiDS radii, as point values and as annulus averages; V2 [load-bearing] the committed projection's errors
     (FP18 K2b confirmed); V3 (reported) every projector's error vs R (FP6/FP1/L355, L352, DE8, FP18, FP20) on every profile
     and on the chain's own P2 phantom; V4 (reported) the P2 family's error stated plainly; V5 (reported) the 2-halo templates.
  B  [load-bearing] THE ANATOMY: defect A alone, defect B alone, both fixed.
  R  THE RE-SCORE (reported; before -> after, with each lane's own gate): R1 FP6 (full re-run), R2 FP9 (full re-run),
     R3 FP13 (H_S at z = 0.25/0.4/0.7, its variants and windows), R4 FP12, R5 FP11, R6 FP1 E (full re-run of the E section),
     R7 FP14/FP17 (full re-runs), R8 L355 (full re-run; the 'web-blind kernel' claim), R9 the P2 family (L352, L360 full
     re-run, DE8 C1), R11 AT3's gate and switch-free KiDS at its window cells (its retention profiles recomputed; FP4 C4 and FP10
     B4 estimated from its shifts), R10 the flip table.
  F  [load-bearing] every re-score completed with finite numbers.
  H  (reported) the hub's lanes (XR*.py) and the record's files that use either projection.
  W  the ledger.
MUTATE=1 replaces the corrected projection by the committed one EVERYWHERE: V1 must FAIL (rc = 1), and every re-score must
reproduce the committed numbers (no flips) -- an end-to-end control of the harness.  Outputs *_MUTATE.out / *_results_MUTATE.json.

SCOPE.  The projection only: data (Brouwer+2021 Fig. 3, full covariance in its corrected (m,n,i,j) order), M_b profiling,
2-halo templates and caps, point values (P1 lanes) vs annulus averages (P2 lanes), truncation at the grid end (30 Mpc), every
lane's gate: all as committed.  The 2-halo templates carry their own inner-disc approximation (V5 prices it).  No particle-mesh
run; each re-run is the lane's committed code exec'd in this lane's namespace with the projection swapped, file writes refused.
Run from the lane directory:  python3 FP20_esd_projection_fix.py > FP20_esd_projection_fix.out 2>&1; echo rc=$? >> FP20_esd_projection_fix.out
"""
import os, sys, io, re, json, math, time, glob, builtins, contextlib, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
warnings.filterwarnings("ignore")
import numpy as np

np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "FP20_esd_projection_fix"
SECTIONS = os.environ.get("FP20_SECTIONS", "all")                                  # development switch; the committed runs use 'all'
OUT = {"lane": "FP20", "mutate": MUTATE, "checks": {}, "numbers": {}, "ledger": []}
CH = []
T0 = time.time()
_trap = getattr(np, "trapezoid", None) or np.trapz
FOOTS = ("canonical", "alt")


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)


def el():
    return f"[{time.time() - T0:.0f} s]"


def check(name, measured, ok, load_bearing=True, reading=None):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing, "name": name}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def want(sec):
    return SECTIONS == "all" or sec in SECTIONS.split(",")


def jclean(o):
    if isinstance(o, dict):
        return {str(k): jclean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jclean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)):
        return float(o)
    if isinstance(o, np.ndarray):
        return [jclean(v) for v in o.tolist()]
    if isinstance(o, float) and not math.isfinite(o):
        return str(o)
    return o


P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the 'corrected' projection is replaced by the committed one everywhere -- V1 must FAIL, and every re-score "
      "must reproduce the committed numbers (no flips) ***")


# ================================================================================================= the harness
def _ro_open(file, mode="r", *a, **k):
    if any(c in mode for c in "wax+"):
        raise PermissionError(f"FP20 refuses to write {file!r} from a re-executed lane")
    return builtins.open(file, mode, *a, **k)


@contextlib.contextmanager
def lane_env():
    """MUTATE=0 in the environment (the lanes read it at exec time) and their stdout captured."""
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


def exec_slices(path, slices, hooks=None, name="lane", ns=None):
    """exec [start, stop) slices of a committed source in ONE namespace (file writes refused); hooks[i](ns) runs after slice i."""
    src = open(path).read()
    ns = {"__file__": path, "__name__": name, "open": _ro_open} if ns is None else ns
    ns.setdefault("open", _ro_open)
    hooks = hooks or {}
    with lane_env() as buf:
        for i, (a, b) in enumerate(slices):
            ia = 0 if a is None else (src.index(a) if isinstance(a, str) else a)
            ib = len(src) if b is None else (src.index(b) if isinstance(b, str) else b)
            code = "\n" * src[:ia].count("\n") + src[ia:ib]                          # keep the line numbers
            exec(compile(code, path, "exec"), ns)
            if i in hooks:
                hooks[i](ns)
    return ns, buf.getvalue()


def lane_json(rel):
    p = os.path.join(REPO, rel) if not os.path.isabs(rel) else rel
    return json.load(open(p))


def checks_by_id(chk):
    """{id: (ok, lb, measured, name)} from a list of (name, ok, lb[, measured]) or a committed JSON 'checks' dict."""
    out = {}
    if isinstance(chk, dict):
        items = [(v.get("name", k), v.get("ok", v.get("pass")), v.get("load_bearing", True), v.get("measured", "")) for k, v in chk.items()]
    else:
        items = [(t[0], t[1], t[2], t[3] if len(t) > 3 else "") for t in chk]
    for name, ok, lb, meas in items:
        key = name.split()[0]
        k2, j = key, 1
        while k2 in out:
            j += 1; k2 = f"{key}#{j}"
        out[k2] = (bool(ok), bool(lb), str(meas), name)
    return out


def check_flips(new_list, old_dict):
    new, old = checks_by_id(new_list), checks_by_id(old_dict)
    fl = []
    for k, (ok, lb, meas, name) in new.items():
        if k in old and old[k][0] != ok:
            fl.append(dict(id=k, before="PASS" if old[k][0] else "FAIL", after="PASS" if ok else "FAIL", load_bearing=lb,
                           name=name[:160], measured_before=old[k][2][:300], measured_after=meas[:300]))
    return fl


# ================================================================================================= the projectors
def shell_mats(edges, Rv):
    """uniform-density shells between consecutive edges [m] seen at projected radii Rv [m]:
    S[i, k] = Sigma(Rv_i) per unit mass of shell k [1/m^2]; C[i, k] = fraction of shell k's mass inside the cylinder Rv_i."""
    r1, r2 = edges[:-1][None, :], edges[1:][None, :]
    R = np.asarray(Rv, float)[:, None]
    V3 = r2 ** 3 - r1 ** 3

    def s(r):
        return np.sqrt(np.clip(r * r - R * R, 0.0, None))

    def g(r):                                                                     # r^3 - (r^2 - R^2)_+^{3/2}, cancellation-free
        ss = s(r)
        return np.where(r > R, R * R * (r * r + r * ss + ss * ss) / (r + ss), r ** 3)
    return 2.0 * (s(r2) - s(r1)) / ((4 * math.pi / 3) * V3), (g(r2) - g(r1)) / V3


class ESDFix:
    """drop-in for the P1 esd_of_M(M, Mb) on a grid (rr -> Rp): exact uniform-shell projection, core mass kept."""

    def __init__(self, rr, Rp, PCm, MS):
        S, C = shell_mats(rr, Rp)
        self.KD = C / (math.pi * Rp[:, None] ** 2) - S
        self.S, self.C, self.rr, self.Rp, self.conv = S, C, rr, Rp, PCm ** 2 / MS

    def __call__(self, M, Mb):
        Mext = np.asarray(M, float) - Mb
        return (self.KD @ np.diff(Mext) + (Mext[0] + Mb) / (math.pi * self.Rp ** 2)) * self.conv

    def M2(self, M, Mb):
        Mext = np.asarray(M, float) - Mb
        return self.C @ np.diff(Mext) + Mext[0] + Mb

    def Sig(self, M, Mb):
        return self.S @ np.diff(np.asarray(M, float) - Mb)


class M2Fix:
    """drop-in for L352's project_M2(rho) (node densities on rr -> M_2D on Rp): trapezoid shell masses, exact shells."""

    def __init__(self, rr, Rp):
        self.C = shell_mats(rr, Rp)[1]; self.rr = rr

    def __call__(self, rho):
        rho = np.asarray(rho, float); q = 4 * math.pi * self.rr ** 2 * rho
        return self.C @ (0.5 * (q[1:] + q[:-1]) * np.diff(self.rr)) + self.core(rho)

    def core(self, rho):
        """the mass inside the first node from node values alone: rho ~ r^-gamma continued inward, gamma from the first two
        nodes (clipped to [0, 2.5]): 4 pi rho_0 r_0^3/(3 - gamma) -- exact for a uniform core, an NFW cusp and an SIS."""
        r0, r1 = self.rr[0], self.rr[1]
        if rho[0] <= 0:
            return 0.0
        gam = float(np.clip(-math.log(rho[1] / rho[0]) / math.log(r1 / r0), 0.0, 2.5)) if rho[1] > 0 else 0.0
        return 4 * math.pi * rho[0] * r0 ** 3 / (3 - gam)


class CellFix:
    """drop-in for DE8's m2_of_rho(rho_cells) (finite-volume cells between faces -> M_2D on Rp): exact shells = cells."""

    def __init__(self, faces, Rp):
        self.C = shell_mats(faces, Rp)[1]; self.V4 = 4 * math.pi * (faces[1:] ** 3 - faces[:-1] ** 3) / 3.0

    def __call__(self, rho_cells):
        return self.C @ (np.asarray(rho_cells, float) * self.V4)


# ================================================================================================= the record's projectors (loaded)
KIDS_DIR = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar")
RD = np.genfromtxt(os.path.join(KIDS_DIR, "Fig-3_Lensing-rotation-curves_Massbin-1.txt"), comments="#")[:, 0]   # the 15 radii [Mpc]
P6 = os.path.join(HERE, "FP6_gate_survey.py")
P1 = os.path.join(HERE, "FP1_static_sector.py")
P9 = os.path.join(HERE, "FP9_web_galaxy_separator.py")
P13 = os.path.join(HERE, "FP13_separator_from_state.py")
P14 = os.path.join(HERE, "FP14_zero_knob_core.py")
P17 = os.path.join(HERE, "FP17_screening_without_xi.py")
P55 = os.path.join(REPO, "real_research", "g03_audit_2026", "L355_kernel_invisible_kids.py")
P52 = os.path.join(REPO, "real_research", "g03_audit_2026", "L352_switch_gauss_compensation.py")
P60 = os.path.join(REPO, "real_research", "g03_audit_2026", "L360_assembled_construction_kids.py")
PDE8 = os.path.join(REPO, "real_research", "dark_energy_2026", "DE8_kids_sigma_axis_both_branches.py")
FP1_KIDS = ("# ---- KiDS: L355's machinery", "w0 = np.zeros(len(ES)); w0[0] = 1.0")

M6 = exec_slices(P6, [(None, 'banner("K  CONTROLS')], name="fp6_machinery")[0]          # FP6's machinery (the P1 projection)
GK = {"np": np, "math": math, "os": os, "REPO": REPO, "G_SI": 6.67430e-11, "_trap": _trap}
GK = exec_slices(P1, [FP1_KIDS], name="fp1_kids", ns=GK)[0]                               # FP1 E's copy (FP14/FP17's GK)
L55 = exec_slices(P55, [(None, "LYT = np.linspace(-9.5, 6.5, 1601)")], name="l355_head")[0]   # L355's projection (L357/AT1/AT3)
L52 = {"__name__": "l352", "__file__": P52, "open": _ro_open}
with lane_env():
    exec(open(P52).read().split("real_mode = ")[0].replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), L52)
D8 = exec_slices(PDE8, [(None, 'banner("C1-C3  CONTROLS')], name="de8_head")[0]                     # DE8 up to its C1 (C0 run inside)
RR, RP, MPCm, PCm, MS = M6["RR"], M6["RP"], M6["MPCm"], M6["PCm"], M6["MS6"]
assert np.array_equal(RR, GK["rrK"]) and np.array_equal(RP, GK["Rp"]) and np.array_equal(RR, L55["rr"]) and np.array_equal(RP, L55["Rp"])
FIX1 = ESDFix(RR, RP, PCm, MS)                                                            # the corrected P1 projection
esd_bug6, esd_bug1, esd_bug55 = M6["esd_of_M"], GK["esd_of_M"], L55["esd_of_M"]
if MUTATE:
    fix6, fix1 = esd_bug6, esd_bug1
else:
    fix6 = lambda M, Mb: (RP / MPCm, FIX1(M, Mb))
    fix1 = FIX1
rr2, Rp2, LOGSTEP = L52["rr"], L52["Rp"], L52["LOGSTEP"]
annulus_esd, project_M2_bug = L52["annulus_esd"], L52["project_M2"]
FIX2 = M2Fix(rr2, Rp2)
fix2 = project_M2_bug if MUTATE else FIX2
FACES = np.concatenate([[D8["rlo"]], D8["rf"], [D8["rr"][-1] ** 2 / D8["rf"][-1]]])
FIXC = CellFix(FACES, D8["Rp"])
fixc = D8["m2_of_rho"] if MUTATE else FIXC
P(f"\n  loaded (read-only): FP6's machinery (esd_of_M), FP1 E's KiDS machinery (esd_of_M; exec'd by FP14/FP17), L355's head "
  f"(esd_of_M; loaded by L357/AT1/AT3), L352's machinery (project_M2 + annulus_esd; L359/L360/AT3/DE8), DE8's head "
  f"(esd_from_mlens); grids r = {RR[0] / MPCm:g}-{RR[-1] / MPCm:g} Mpc x {len(RR)}, P1 R = {RP[0] / MPCm:g}-{RP[-1] / MPCm:g} x {len(RP)}, "
  f"P2 R = {Rp2[0] / MPCm:g}-{Rp2[-1] / MPCm:g} x {len(Rp2)}   {el()}")


# ================================================================================================= the analytic standard
G_SI = 6.6743e-11
VSIS = 200e3
KSIS = VSIS ** 2 / G_SI                                                                   # SIS: M(<r) = K r  [kg/m]
RT = RR[-1]                                                                               # the record's truncation (30 Mpc)


def sis_M(r):
    return KSIS * np.minimum(r, RT)


def sis_ds(Rm):                                                                            # truncated SIS, exact [Msun/pc^2]
    x = Rm / RT
    return KSIS / (math.pi * Rm) * ((1 - np.sqrt(1 - x * x)) / x + np.arccos(x) / 2) * PCm ** 2 / MS


def sis_M2(Rm):
    return KSIS * (RT - np.sqrt(RT * RT - Rm * Rm) + Rm * np.arccos(Rm / RT))


RHOC_Z = 2.775e11 * 0.70 ** 2 * (0.2793 * 1.25 ** 3 + 1 - 0.2793) * MS / MPCm ** 3        # B21's WMAP9 rho_crit(0.25) [kg/m^3]
NFW_SET = ((0.5e12, 8.0), (3e12, 4.0), (1e13, 2.0))                                      # FP18 K2's halos [Msun, c]


def nfw_par(M200, c):
    r200 = (3 * M200 * MS / (4 * math.pi * 200 * RHOC_Z)) ** (1 / 3); rs = r200 / c
    rhos = M200 * MS / (4 * math.pi * rs ** 3 * (math.log(1 + c) - c / (1 + c)))
    return rs, rhos


def nfw_M(r, M200, c):
    rs, rhos = nfw_par(M200, c); x = np.minimum(r, RT) / rs
    return 4 * math.pi * rhos * rs ** 3 * (np.log(1 + x) - x / (1 + x))


def nfw_ds_wb(Rm, M200, c):
    """Wright & Brainerd (2000) Delta Sigma of the untruncated NFW [Msun/pc^2] (their eqs. 11-16)."""
    rs, rhos = nfw_par(M200, c); out = []
    for x in np.atleast_1d(Rm) / rs:
        if x < 1 - 1e-6:
            at = math.atanh(math.sqrt((1 - x) / (1 + x)))
            g = 8 * at / (x * x * math.sqrt(1 - x * x)) + 4 / (x * x) * math.log(x / 2) - 2 / (x * x - 1) + 4 * at / ((x * x - 1) * math.sqrt(1 - x * x))
        elif x < 1 + 1e-6:
            g = 10 / 3 + 4 * math.log(0.5)
        else:
            at = math.atan(math.sqrt((x - 1) / (1 + x)))
            g = 8 * at / (x * x * math.sqrt(x * x - 1)) + 4 / (x * x) * math.log(x / 2) - 2 / (x * x - 1) + 4 * at / ((x * x - 1) ** 1.5)
        out.append(rs * rhos * g)
    return np.array(out) * PCm ** 2 / MS


def nfw_M2(Rm, M200, c):
    """the untruncated NFW projected mass 4 pi rho_s r_s^3 h(x) (Bartelmann 1996; W&B 2000's mean surface density)."""
    rs, rhos = nfw_par(M200, c); x = np.atleast_1d(np.asarray(Rm, float)) / rs
    h = np.where(x < 1, np.arccosh(1 / np.minimum(x, 1 - 1e-12)) / np.sqrt(np.maximum(1 - x * x, 1e-300)),
                 np.arccos(1 / np.maximum(x, 1 + 1e-12)) / np.sqrt(np.maximum(x * x - 1, 1e-300)))
    return 4 * math.pi * rhos * rs ** 3 * (np.log(x / 2) + h)


def nfw_ds_quad(Rm, M200, c):
    """the grid-truncated NFW (r <= 30 Mpc) by adaptive quadrature -- shows the truncation is irrelevant at 1e-5."""
    from scipy.integrate import quad
    rs, rhos = nfw_par(M200, c); rho = lambda r: rhos / ((r / rs) * (1 + r / rs) ** 2); out = []
    for R in np.atleast_1d(Rm):
        zmax = math.sqrt(RT * RT - R * R); f = lambda z: rho(math.sqrt(R * R + z * z))
        sig = 2 * (quad(f, 0, R, limit=400, epsrel=1e-11)[0] + quad(f, R, zmax, limit=400, epsrel=1e-11)[0])
        hfun = lambda r: 4 * math.pi * r * r * rho(r) * (1 - math.sqrt(max(1 - R * R / (r * r), 0.0)))
        m2 = float(nfw_M(np.array([R]), M200, c)[0]) + quad(hfun, R, RT, limit=800, points=[p_ for p_ in (R * 1.0001, R * 1.01, R * 1.1, 2 * R, 10 * R) if p_ < RT], epsrel=1e-11)[0]
        out.append(m2 / (math.pi * R * R) - sig)
    return np.array(out) * PCm ** 2 / MS


MPT = 1e11 * MS                                                                          # the point mass
A_CMP = 3.0e-3 * MPCm                                                                    # a compact uniform sphere, radius 3 kpc


def cmp_M(r):
    return MPT * np.minimum(1.0, (r / A_CMP) ** 3)


A0C = M6["A0"]["canonical"]
nu_p2 = M6["nu_p2"]


def phantom_M(r, Mb):                                                                     # the chain's isolated P2 law (kernel, no band-pass)
    return Mb * nu_p2(G_SI * Mb / (r ** 2 * A0C))


RRF = np.geomspace(1e-4, 30.0, 16000) * MPCm                                            # 4x finer, 10x deeper: the reference grid
FIXF = ESDFix(RRF, RD * MPCm, PCm, MS)
FIXF2 = M2Fix(RRF, Rp2)


def at_rd(Rq, v):
    return np.interp(RD, Rq, v)


def ann(M2_on_Rp2, Rq=Rp2):
    """the record's exact annulus average (L352's annulus_esd), bin by bin at the data radii."""
    return annulus_esd(lambda R: np.interp(np.log(R), np.log(Rq), M2_on_Rp2), RD)


def ann_fun(M2fun):
    return annulus_esd(M2fun, RD)


# the record's projectors as functions of a profile (M on the record's grid, M_b) -> Delta Sigma at the 15 radii
def p1_bug(Mfun, Mb):
    return at_rd(RP / MPCm, esd_bug6(Mfun(RR), Mb)[1])


def p1_fix(Mfun, Mb):
    return at_rd(RP / MPCm, fix6(Mfun(RR), Mb)[1])


def p2_bug_M(Mfun, Mb):
    """L352's model_M2 path, committed: node densities from np.gradient(M - M_b), then project_M2."""
    M = Mfun(rr2); M2 = project_M2_bug(np.gradient(M - Mb, rr2) / (4 * math.pi * rr2 ** 2)) + Mb
    return ann(M2)


def p2_fix_M(Mfun, Mb):
    """the corrected model_M2 path: shells straight from M (no gradient round trip)."""
    M = Mfun(rr2)
    M2 = (p2_M2_direct(M, Mb) if not MUTATE else project_M2_bug(np.gradient(M - Mb, rr2) / (4 * math.pi * rr2 ** 2)) + Mb)
    return ann(M2)


def p2_fix_rho(rhofun, Mb):
    """the corrected density path (carrier templates: node densities on r): trapezoid shells, exact projection."""
    return ann(fix2(rhofun(rr2)) + Mb)


def p2_M2_direct(M, Mb):
    Mext = np.asarray(M, float) - Mb
    return FIX2.C @ np.diff(Mext) + Mext[0] + Mb


def de8_with(m2f, Mfun, Mb):
    Mext = Mfun(D8["rf"]) - Mb                                                            # the extended mass inside the interior faces
    Mf = np.concatenate([[0.0], Mext, [Mext[-1]]])
    rho = np.diff(Mf) / (4 * math.pi * D8["V"])
    M2 = m2f(rho) + Mb
    return ann(M2, D8["Rp"])


def p2_exact_mfun(Mfun, Mb):                                                              # the exact annulus average via the fine shells
    M = Mfun(RRF); Mext = M - Mb
    M2 = FIXF2.C @ np.diff(Mext) + Mext[0] + Mb
    return ann(M2)


def sis_rho(r):
    return np.where(r <= RT, KSIS / (4 * math.pi * r ** 2), 0.0)


def nfw_rho(r, M200, c):
    rs, rhos = nfw_par(M200, c)
    return np.where(r <= RT, rhos / ((r / rs) * (1 + r / rs) ** 2), 0.0)


def phantom_rho(r, Mb):                                                                   # d[M_b (nu_P2 - 1)]/dr / (4 pi r^2), exact
    y = G_SI * Mb / (r ** 2 * A0C)
    return A0C / (4 * math.pi * G_SI * r) / np.sqrt(1 + 1 / y)


# the carrier templates of the P2 lanes (L360's post-decay halo of KiDS bin 4: capped / cleared NFW, cut at r200) -- densities with jumps
_Om52, _OL52, _rc52 = L52["Om"], L52["OL"], L52["rho_crit0"]
_rhoc_zl = _rc52 * (_Om52 * 1.25 ** 3 + _OL52)
_FB52 = 0.02237 / (0.02237 + 0.1200)


def carrier_rho(r, M200=5.55e12, pc=1.0, pic="cap", xv0=700.0):
    """L360's carrier_esd density (L360:84-96): (1 - f_b) NFW(M200, c) of the bin's Moster host, capped at / cleared above the trigger
    density at x_v,eff = x_v0 E(0.25)^(2 p_c), cut at r200."""
    c = 10 ** (0.905 - 0.101 * math.log10(M200 / (1e12 / 0.6736)))
    r200 = (3 * M200 * MS / (4 * math.pi * 200 * _rhoc_zl)) ** (1 / 3); rs = r200 / c
    rho_s = M200 * MS / (4 * math.pi * rs ** 3 * (math.log(1 + c) - c / (1 + c)))
    rho = np.where(r < r200, rho_s / ((r / rs) * (1 + r / rs) ** 2), 0.0)
    rv = (_Om52 * 1.25 ** 3 / (_Om52 * 1.25 ** 3 + _OL52) + 2 / 3 * xv0 * (_Om52 * 1.25 ** 3 + _OL52) ** pc) * _rhoc_zl
    rc = (1 - _FB52) * rho
    return np.where(rho >= rv, 0.0, rc) if pic == "cleared" else np.minimum(rc, rv)


_RC60 = np.geomspace(1e-5, 30.0, 60000) * MPCm                                          # the carriers' mass: a 60000-node integral


def carrier_Mfun(**kw):
    q = 4 * math.pi * _RC60 ** 2 * carrier_rho(_RC60, **kw)
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (q[1:] + q[:-1]) * np.diff(_RC60))])
    return lambda r: np.interp(np.asarray(r, float), _RC60, cum)


PROFILES = {}
PROFILES["SIS V=200"] = dict(M=sis_M, Mb=0.0, rho=sis_rho, point=sis_ds(RD * MPCm), ann=ann_fun(sis_M2))
for (M200, cc) in NFW_SET:
    PROFILES[f"NFW {M200:.1e} c{cc:g}"] = dict(M=lambda r, M200=M200, cc=cc: nfw_M(r, M200, cc), Mb=0.0, rho=lambda r, M200=M200, cc=cc: nfw_rho(r, M200, cc),
                                                point=nfw_ds_wb(RD * MPCm, M200, cc), ann=ann_fun(lambda R, M200=M200, cc=cc: nfw_M2(R, M200, cc)))
PROFILES["point 1e11 (M_b term)"] = dict(M=lambda r: MPT + 0.0 * r, Mb=MPT, rho=lambda r: 0.0 * r, point=MPT / (math.pi * (RD * MPCm) ** 2) * PCm ** 2 / MS,
                                         ann=ann_fun(lambda R: MPT + 0.0 * R))
PROFILES["point 1e11 (compact, as extended)"] = dict(M=cmp_M, Mb=0.0, rho=None, point=MPT / (math.pi * (RD * MPCm) ** 2) * PCm ** 2 / MS,
                                                     ann=ann_fun(lambda R: MPT + 0.0 * R))
for lm in (10.5, 11.0):
    Mb_ = 10 ** lm * MS
    PROFILES[f"P2 phantom 1e{lm:g} (+M_b)"] = dict(M=lambda r, Mb_=Mb_: phantom_M(r, Mb_), Mb=Mb_, rho=lambda r, Mb_=Mb_: phantom_rho(r, Mb_),
                                                   point=FIXF(phantom_M(RRF, Mb_), Mb_), ann=p2_exact_mfun(lambda r, Mb_=Mb_: phantom_M(r, Mb_), Mb_),
                                                   fine_ref=True)
for pic, xv0 in (("cap", 700.0), ("cleared", 1000.0)):
    Mc_ = carrier_Mfun(pic=pic, xv0=xv0); Mf_ = Mc_(RRF)
    PROFILES[f"carrier {pic} x_v0={xv0:g} (L360 bin 4)"] = dict(M=Mc_, Mb=0.0, rho=lambda r, pic=pic, xv0=xv0: carrier_rho(r, pic=pic, xv0=xv0),
                                                              point=FIXF(Mf_, 0.0), ann=ann(FIXF2.C @ np.diff(Mf_) + Mf_[0]), fine_ref=True, jumps=True)

# ================================================================================================= V  the analytic standard
if want("V"):
    banner("V  THE ANALYTIC STANDARD: every projector in use against the singular isothermal sphere, NFW (Wright & Brainerd 2000) and a "
           "point mass, at the 15 KiDS radii")
    # FP18's own projection (K2), imported read-only
    with lane_env():
        sys.path.insert(0, HERE)
        import FP18_kids_vs_hubble_flow_data as F18
    G_KMS = F18.G_KMS
    f18 = {}
    ks18 = VSIS ** 2 / 1e6 / (G_KMS * 1e12)
    f18["SIS V=200"] = F18.esd_of(lambda r: ks18 * np.minimum(np.asarray(r, float), RT / MPCm))
    for (M200, cc) in NFW_SET:
        rs, rhos = nfw_par(M200, cc)
        f18[f"NFW {M200:.1e} c{cc:g}"] = F18.esd_of(lambda r, M200=M200, cc=cc: nfw_M(np.asarray(r, float) * MPCm, M200, cc) / MS / 1e12)
    f18["point 1e11 (M_b term)"] = F18.esd_of(lambda r: 0.1 + 0.0 * np.asarray(r, float))
    f18["point 1e11 (compact, as extended)"] = F18.esd_of(lambda r: cmp_M(np.asarray(r, float) * MPCm) / MS / 1e12)
    for lm in (10.5, 11.0):
        Mb_ = 10 ** lm * MS
        f18[f"P2 phantom 1e{lm:g} (+M_b)"] = F18.esd_of(lambda r, Mb_=Mb_: phantom_M(np.maximum(np.asarray(r, float), 1e-9) * MPCm, Mb_) / MS / 1e12)
    for nm, pr in PROFILES.items():
        if pr.get("jumps"):
            f18[nm] = F18.esd_of(lambda r, pr=pr: pr["M"](np.asarray(r, float) * MPCm) / MS / 1e12)
    ERR = {}
    for nm, pr in PROFILES.items():
        e = {}
        e["P1 committed (FP6/FP1/L355, point)"] = p1_bug(pr["M"], pr["Mb"]) / pr["point"] - 1
        e["P2 L352 project_M2 (annulus)"] = p2_bug_M(pr["M"], pr["Mb"]) / pr["ann"] - 1
        if pr["rho"] is not None:
            e["P2 L352 project_M2, node rho (annulus)"] = ann(project_M2_bug(pr["rho"](rr2)) + pr["Mb"]) / pr["ann"] - 1
        e["DE8 esd_from_mlens (annulus)"] = de8_with(D8["m2_of_rho"], pr["M"], pr["Mb"]) / pr["ann"] - 1
        e["FP18 shell_kernel (point)"] = f18[nm] / pr["point"] - 1
        e["FP20 fix, P1 grid (point)"] = p1_fix(pr["M"], pr["Mb"]) / pr["point"] - 1
        e["FP20 fix, P2 M-path (annulus)"] = p2_fix_M(pr["M"], pr["Mb"]) / pr["ann"] - 1
        if pr["rho"] is not None:
            e["FP20 fix, P2 rho-path (annulus)"] = p2_fix_rho(pr["rho"], pr["Mb"]) / pr["ann"] - 1
        e["FP20 fix, DE8 cells (annulus)"] = de8_with(fixc, pr["M"], pr["Mb"]) / pr["ann"] - 1
        ERR[nm] = e
    # the NFW truncation (the reference is W&B's untruncated formula; the record truncates at 30 Mpc)
    ntr = float(np.max(np.abs(nfw_ds_quad(RD[::2] * MPCm, 3e12, 4.0) / nfw_ds_wb(RD[::2] * MPCm, 3e12, 4.0) - 1)))
    P(f"    reference checks: the NFW truncation at 30 Mpc changes Delta Sigma by {ntr:.1e} (quad vs W&B); the SIS's by "
      f"{float(np.max(np.abs(sis_ds(RD * MPCm) / (KSIS / (4 * RD * MPCm) * PCm ** 2 / MS) - 1))):.1e}; the chain's phantom references are the "
      f"fix on a 4x finer, 10x deeper grid")
    P("\n    error of each projector vs R [%] at the KiDS radii " + ", ".join(f"{x:.3f}" for x in RD) + " Mpc:")
    for nm, e in ERR.items():
        P(f"    -- {nm}")
        for pj, v in e.items():
            P(f"       {pj:38s} " + " ".join(f"{100 * x:+7.2f}" for x in v) + f"   | max |.| {100 * np.max(np.abs(v)):.2f}%")
    OUT["numbers"]["V_errors_percent"] = {nm: {pj: [100 * float(x) for x in v] for pj, v in e.items()} for nm, e in ERR.items()}
    OUT["numbers"]["V_radii_Mpc"] = RD.tolist()
    fix_keys = ("FP20 fix, P1 grid (point)", "FP20 fix, P2 M-path (annulus)", "FP20 fix, P2 rho-path (annulus)", "FP20 fix, DE8 cells (annulus)")
    smooth = [nm for nm in ERR if not PROFILES[nm].get("jumps") and not nm.startswith("P2 phantom")]
    jumpy = [nm for nm in ERR if PROFILES[nm].get("jumps")]
    vmax = {k: max(float(np.max(np.abs(ERR[nm][k]))) for nm in smooth if k in ERR[nm]) for k in fix_keys}
    vmax_ph = {k: max(float(np.max(np.abs(ERR[nm][k]))) for nm in ERR if nm.startswith("P2 phantom") and k in ERR[nm]) for k in fix_keys}
    check("V1 THE CORRECTED PROJECTION REPRODUCES THE ANALYTIC PROFILES: the singular isothermal sphere (V = 200 km/s), three NFW halos "
          "(Wright & Brainerd 2000; FP18 K2's), a 1e11 Msun point mass as the analytic term AND as a compact (3 kpc) sphere passed as "
          "extended mass, to < 0.1% at all 15 KiDS radii -- as point values on the P1 grid (FP6/FP1/L355 lanes), as annulus averages on "
          "L352's grid from the mass profile (model_M2's path) and from node densities (the carrier templates' path), and on DE8's cells; "
          "the chain's P2 phantom agrees with a 4x finer grid to < 0.1%",
          "max |error| " + ", ".join(f"{k.split(', ')[1]}: {100 * v:.3f}%" for k, v in vmax.items()) + "; phantom vs the fine grid "
          + ", ".join(f"{k.split(', ')[1]}: {100 * v:.3f}%" for k, v in vmax_ph.items()),
          max(vmax.values()) < 1e-3 and max(vmax_ph.values()) < 1e-3)
    cj = {k: max(float(np.max(np.abs(ERR[nm][k]))) for nm in jumpy if k in ERR[nm]) for k in ("FP20 fix, P2 rho-path (annulus)", "FP20 fix, DE8 cells (annulus)",
                                                                                               "FP20 fix, P1 grid (point)", "FP20 fix, P2 M-path (annulus)")}
    cb = {nm: (100 * float(np.min(ERR[nm]["P2 L352 project_M2, node rho (annulus)"])), 100 * float(np.max(ERR[nm]["P2 L352 project_M2, node rho (annulus)"])))
          for nm in jumpy}
    check("V1b THE CORRECTED PROJECTION HANDLES THE P2 LANES' CARRIER TEMPLATES (L360's capped and cleared NFW halos: flat cores, hollows "
          "and the cut at r200 -- densities with jumps, read from their node values as the lanes do) to < 0.5% of a 60000-node reference, "
          "where the committed L352 path errs by up to the printed amount at 35 kpc",
          "fix: " + ", ".join(f"{k.split(', ')[1]}: {100 * v:.3f}%" for k, v in cj.items()) + " | committed P2 on node densities: "
          + "; ".join(f"{nm}: {a:+.0f}..{b:+.0f}%" for nm, (a, b) in cb.items()), max(cj.values()) < 5e-3)
    OUT["numbers"]["V1b_carrier_P2_error_percent"] = cb
    e_sis = ERR["SIS V=200"]["P1 committed (FP6/FP1/L355, point)"]
    fp18_k2b = F18.OUT if hasattr(F18, "OUT") else None
    b6_ref = {0.035: -0.586, 0.3035: -0.104, 0.7625: -0.049, 2.6035: -0.139}                # FP18 K2b's printed values (RD[::2]) and ledger
    dev_k2b = max(abs(float(np.interp(R, RD, e_sis)) - v) for R, v in b6_ref.items())
    check("V2 THE BUG IS REAL (FP18 K2b confirmed): the committed P1 projection (FP6 esd_of_M = FP1 E's = L355's) under-projects the "
          "singular isothermal sphere at every KiDS radius: <= -50% at 35 kpc, <= -3% everywhere, with FP18's printed values reproduced",
          "SIS: " + ", ".join(f"R {R:.2f}: {100 * v:+.1f}%" for R, v in zip(RD[::2], e_sis[::2])) + f" (FP18 K2b's values reproduced to {100 * dev_k2b:.1f} pp)",
          e_sis[0] < -0.50 and float(np.max(e_sis)) < -0.03 and dev_k2b < 0.01)
    p2max = {nm: (100 * float(np.min(ERR[nm]["P2 L352 project_M2 (annulus)"])), 100 * float(np.max(ERR[nm]["P2 L352 project_M2 (annulus)"])))
             for nm in ERR if not nm.startswith("point 1e11 (M_b")}
    d8max = {nm: (100 * float(np.min(ERR[nm]["DE8 esd_from_mlens (annulus)"])), 100 * float(np.max(ERR[nm]["DE8 esd_from_mlens (annulus)"])))
             for nm in ERR if not nm.startswith("point 1e11 (M_b")}
    sel = [nm for nm in ERR if nm.startswith(("SIS", "NFW", "P2 phantom"))]
    car = {nm: (100 * float(np.min(ERR[nm]["P2 L352 project_M2, node rho (annulus)"])), 100 * float(np.max(ERR[nm]["P2 L352 project_M2, node rho (annulus)"])))
           for nm in ERR if PROFILES[nm].get("jumps")}
    p2_over2 = any(abs(x) > 0.02 for nm in sel for x in ERR[nm]["P2 L352 project_M2 (annulus)"])
    d8_over2 = any(abs(x) > 0.02 for nm in sel for x in ERR[nm]["DE8 esd_from_mlens (annulus)"])
    check("V4 (reported) THE P2 FAMILY (L352's project_M2 + annulus_esd: L352, L359, L360, AT3's switched gate, FP4/FP10 via AT3, DE8's "
          "esd_from_mlens, DE10 and the hub's XR9/XR14) is NOT exact either: it shares the trapezoid Abel defect (B) but not the inner-disc "
          "defect (A); on the SIS it under-projects by ~2-3%, on NFW halos and the chain's phantom by -3% at large R and up to +5..+11% "
          "at 35 kpc (its inner term 2 pi R_0^2 Sig(R_0) is exact only for Sigma ~ 1/R) -- "
          + ("MORE than 2% (said plainly)" if (p2_over2 or d8_over2) else "within 2%") + "; on the CARRIER TEMPLATES (flat-cored or "
          "hollowed halos) the same inner term is wrong by up to +187% / -123% at 35 kpc (V1b), so every carrier-bearing KiDS score "
          "of the P2 lanes moves (R9, R11); a compact mass passed as extended is lost entirely",
          "L352: " + "; ".join(f"{nm}: {a:+.2f}..{b:+.2f}%" for nm, (a, b) in p2max.items() if nm in sel) + " | DE8: "
          + "; ".join(f"{nm}: {a:+.2f}..{b:+.2f}%" for nm, (a, b) in d8max.items() if nm in sel) + " | carriers (node densities): "
          + "; ".join(f"{nm}: {a:+.0f}..{b:+.0f}%" for nm, (a, b) in car.items()), True, load_bearing=False)
    OUT["numbers"]["V4"] = dict(L352=p2max, DE8=d8max, over_2pct=dict(L352=p2_over2, DE8=d8_over2))
    # V5: the 2-halo templates (kept as the record builds them) -- their own inner-disc term, priced against an exact inner integral
    Rext = np.geomspace(1e-5, 6.0, 3000)
    S1 = GK["rho_m_z"] * np.array([GK["w_proj"](R) for R in Rext]) / 1e12                   # FP1 E / L355 units: 1e12 Msun/Mpc^2
    M21 = (np.concatenate([[0], np.cumsum(0.5 * (S1[1:] * Rext[1:] + S1[:-1] * Rext[:-1]) * np.diff(Rext))]) * 2 * math.pi + math.pi * Rext[0] ** 2 * S1[0]) * 1e12
    ex1 = np.interp(RD, Rext, M21 / (math.pi * (Rext * 1e6) ** 2) - S1)
    S2 = L52["rho_m_z"] * np.array([L52["w_proj"](R) for R in Rext])                        # L352 units: Msun/Mpc^2
    M22 = np.concatenate([[0], np.cumsum(0.5 * (S2[1:] * Rext[1:] + S2[:-1] * Rext[:-1]) * np.diff(Rext))]) * 2 * math.pi + math.pi * Rext[0] ** 2 * S2[0]
    ex2 = annulus_esd(lambda R: np.interp(np.log(R), np.log(Rext * MPCm), M22 * MS), RD)
    t1, t2 = np.asarray(GK["T2H"][0]), np.asarray(L52["twoh_cache"][0])
    sd = np.genfromtxt(os.path.join(KIDS_DIR, "Fig-3_Lensing-rotation-curves_Massbin-1.txt"), comments="#")
    err1 = sd[:, 3] / sd[:, 4]
    check("V5 (reported) THE 2-HALO TEMPLATES (kept as the record builds them): FP1 E / L355's (pi R_0^2 Sig(R_0) at 20 kpc) and L352's (the same "
          "at 5 kpc) against an exact inner integral of the same xi_lin projection: the absolute error per unit bias is far below the data errors "
          "(the 2-halo Sigma is flat inside 50 kpc, where the inner disc is right)",
          f"FP1/L355 T2H: max |d| {float(np.max(np.abs(t1 - ex1))):.2e} Msun/pc^2 (max rel {float(np.max(np.abs(t1 / ex1 - 1))):.1%}); L352 twoh_cache: max |d| "
          f"{float(np.max(np.abs(t2 - ex2))):.2e} (max rel {float(np.max(np.abs(t2 / ex2 - 1))):.1%}); smallest bin-1 data error {float(np.min(err1)):.2f} Msun/pc^2",
          True, load_bearing=False)
    OUT["numbers"]["V5"] = dict(T2H_abs=float(np.max(np.abs(t1 - ex1))), twoh_abs=float(np.max(np.abs(t2 - ex2))))
    P(f"    {el()}")

# ================================================================================================= B  the anatomy of the bug
if want("B"):
    banner("B  THE ANATOMY: defect A (the inner disc pi R_0^2 Sig(R_0), R_0 = 20 kpc) and defect B (the trapezoid Abel integral)")
    R0g = RP[0]

    def p1_variant(Mfun, Mb, inner, abel):
        M = Mfun(RR)
        rho = np.gradient(M - Mb, RR) / (4 * math.pi * RR ** 2)
        Sig = M6["_WP"] @ rho if abel == "trapezoid" else FIX1.Sig(M, Mb)
        Mc = np.concatenate([[0], np.cumsum(0.5 * (Sig[1:] * RP[1:] + Sig[:-1] * RP[:-1]) * np.diff(RP))]) * 2 * math.pi
        if inner == "pi R0^2 Sig(R0)":
            Mc = Mc + math.pi * R0g ** 2 * Sig[0]
        else:                                                                             # the exact projected extended mass inside R_0
            Mc = Mc + float(FIX1.M2(M, Mb)[0] - Mb)
        return at_rd(RP / MPCm, (Mc / (math.pi * RP ** 2) - Sig + Mb / (math.pi * RP ** 2)) * PCm ** 2 / MS)
    ANAT = {}
    for nm in ("SIS V=200", "NFW 3.0e+12 c4", "P2 phantom 1e11 (+M_b)", "point 1e11 (compact, as extended)"):
        pr = PROFILES[nm]; ANAT[nm] = {}
        for inner in ("pi R0^2 Sig(R0)", "exact"):
            for abel in ("trapezoid", "exact"):
                ANAT[nm][(inner, abel)] = p1_variant(pr["M"], pr["Mb"], inner, abel) / pr["point"] - 1
        P(f"    -- {nm}: error [%] at the KiDS radii")
        for k_, v in ANAT[nm].items():
            lab = {("pi R0^2 Sig(R0)", "trapezoid"): "committed (A and B)", ("exact", "trapezoid"): "A fixed, B kept",
                   ("pi R0^2 Sig(R0)", "exact"): "B fixed, A kept", ("exact", "exact"): "both fixed"}[k_]
            P(f"       {lab:22s} " + " ".join(f"{100 * x:+7.2f}" for x in v) + f"   | max |.| {100 * np.max(np.abs(v)):.2f}%")
    OUT["numbers"]["B_anatomy_percent"] = {nm: {f"{k_[0]} | {k_[1]}": [100 * float(x) for x in v] for k_, v in d.items()} for nm, d in ANAT.items()}
    a_only = ANAT["SIS V=200"][("pi R0^2 Sig(R0)", "exact")]; b_only = ANAT["SIS V=200"][("exact", "trapezoid")]
    both = max(float(np.max(np.abs(ANAT[nm][("exact", "exact")]))) for nm in ANAT)
    check("B1 THE BUG IS TWO DEFECTS, BOTH NEEDED TO EXPLAIN IT: (A) alone (exact Abel, the committed inner disc) gives the -57% at 35 kpc "
          "falling as R_0/R; (B) alone (exact inner mass, the committed trapezoid) gives scattered -2..-6% errors and the -12% at 2.6 Mpc; "
          "fixing both reproduces the analytic profiles (< 0.1%) -- the missing term is the inner projected mass, the integration limits "
          "are the trapezoid's skipped [R, r_1] segment at the 1/sqrt end point; there is NO line-of-sight truncation defect (30 Mpc "
          "changes Delta Sigma by < 1e-4)",
          f"SIS: A alone {100 * a_only[0]:+.1f}% at 35 kpc, {100 * a_only[-1]:+.1f}% at 2.6 Mpc; B alone {100 * np.min(b_only):+.1f}..{100 * np.max(b_only):+.1f}% "
          f"({100 * b_only[-1]:+.1f}% at 2.6 Mpc); both fixed: max {100 * both:.3f}% over SIS, NFW, the phantom and the compact mass",
          a_only[0] < -0.5 and abs(a_only[-1]) < 0.02 and float(np.min(b_only)) < -0.02 and b_only[-1] < -0.08 and both < 1e-3)
    P(f"    {el()}")


# ================================================================================================= helpers for the re-score
def interp_cross(xs, ys, level):
    """the first downward crossing of `level` by piecewise-linear ys(xs) (FP6 B5 / FP9 I5's rule); nan if none."""
    for i in range(len(xs) - 1):
        if ys[i] > level >= ys[i + 1]:
            return xs[i] + (level - ys[i]) * (xs[i + 1] - xs[i]) / (ys[i + 1] - ys[i])
    return float("nan")


TABLE = []                                                                                # (lane, item, footing, before, after, gate, verdict change)


def row(lane, item, foot, before, after, gate=None, sense="le"):
    """one before/after row; gate: the lane's own threshold (sense 'le': pass iff value <= gate; 'gt': pass iff value > gate)."""
    vb, va = (float(before) if before is not None else float("nan")), float(after)
    if gate is None:
        vd = ""
    else:
        pb = (vb <= gate) if sense == "le" else (vb > gate)
        pa = (va <= gate) if sense == "le" else (va > gate)
        vd = f"{'PASS' if pb else 'FAIL'} -> {'PASS' if pa else 'FAIL'}" + ("  ** FLIP **" if pb != pa else "")
    TABLE.append(dict(lane=lane, item=item, foot=foot, before=vb, after=va, gate=gate, sense=sense, verdict=vd))
    return va


def show_rows(lane):
    for r in TABLE:
        if r["lane"] == lane:
            g = "" if r["gate"] is None else f" (gate {'<=' if r['sense'] == 'le' else '>'} {r['gate']:g})"
            P(f"    {r['item'][:66]:66s} {r['foot'][:9]:9s} {r['before']:+10.3f} -> {r['after']:+10.3f}{g:16s} {r['verdict']}")


FLIPS = {}
RERUN = {}


def summarize_rerun(lane, ns, old_json):
    fl = check_flips(ns["CH"], old_json["checks"])
    FLIPS[lane] = fl
    P(f"    {lane}: re-run with the corrected projection -- {sum(1 for c in ns['CH'] if c[1])}/{len(ns['CH'])} of its own checks pass "
      f"(committed: {sum(1 for v in old_json['checks'].values() if v.get('ok', v.get('pass')))}/{len(old_json['checks'])}); checks that change verdict: "
      + (", ".join(f"{f_['id']} {f_['before']}->{f_['after']}{'' if f_['load_bearing'] else ' (rep.)'}" for f_ in fl) or "none"))
    return fl


# ================================================================================================= K  controls
if want("K"):
    banner("K  CONTROLS: one function under four names; the harness reproduces the committed KiDS numbers with the committed projection")
    rng = np.random.default_rng(20260927)
    dk0 = 0.0
    for _ in range(20):
        Mb_ = 10 ** rng.uniform(9.5, 11.8) * MS
        M = Mb_ + np.cumsum(np.abs(rng.normal(size=len(RR)))) * Mb_ / len(RR) * rng.uniform(0.1, 30)
        a, b, c3 = esd_bug6(M, Mb_)[1], esd_bug1(M, Mb_), esd_bug55(M, Mb_)
        dk0 = max(dk0, float(np.max(np.abs(a - b) / np.abs(a))), float(np.max(np.abs(a - c3) / np.abs(a))))
    src_same = all(s_ in open(p_).read() for p_, s_ in ((P6, "* 2 * math.pi + math.pi * RP[0] ** 2 * Sig[0]"), (P1, "* 2 * math.pi + math.pi * Rp[0] ** 2 * Sig[0]"),
                                                        (P55, "+ math.pi * Rp[0]**2 * Sig[0]")))
    check("K0 CONTROL: the P1 projection is ONE function under four names -- FP6's esd_of_M, FP1 E's (exec'd by FP14 and FP17 as GK), "
          "L355's (loaded by L357, hence AT1 and AT3's switch-free KiDS), and BS2's esd_from_M it was copied from: same grids (r = 1e-3..30 Mpc "
          "x 4000, R = 0.02..4 Mpc x 240), same trapezoid Abel matrix, same inner disc pi R_0^2 Sig(R_0)",
          f"max relative difference over 20 random profiles {dk0:.1e}; inner-disc term present in all three sources: {src_same}",
          dk0 < 1e-12 and src_same)
    # K1: the committed numbers, recomputed through this harness with the committed projection
    F6J, F9J, F13J, F12J, F1J = (lane_json(os.path.join(HERE, f)) for f in ("FP6_gate_survey_results.json", "FP9_web_galaxy_separator_results.json",
                                                                            "FP13_separator_from_state_results.json", "FP12_local_volume_groups_r0_results.json",
                                                                            "FP1_static_sector_results.json"))
    kc = M6["kids_class"]
    k1 = {}
    for f in FOOTS:
        base = kc(M6["A0"][f])
        k1[("FP6 B5 isolated P2", f)] = (base, F6J["numbers"]["B5"][f"{f}_None"])
        k1[("FP6 H2 headline", f)] = (kc(M6["A0"][f], 1.3, M6["y_th_z"]((1e-6, 4.0, 4), 0.25)) - base, F6J["numbers"]["H2"]["kids"][f])
    dK1 = max(abs(a - b) for a, b in k1.values())
    P("    " + "; ".join(f"{k_[0]} {k_[1]}: {a:+.4f} vs committed {b:+.4f}" for k_, (a, b) in k1.items()))
    check("K1 CONTROL: with the committed projection this harness reproduces the committed KiDS numbers exactly (FP6's isolated P2 chi^2 and "
          "(H) headline here; FP9, FP12, FP13, FP1 E, L355 and L352 each reproduced in their R section before the swap)",
          f"max |d chi^2| {dK1:.1e}", dK1 < 1e-6)
    P(f"    {el()}")

FAILS = []


def guard(lane, fn):
    try:
        return fn()
    except Exception as ex:                                                             # recorded; F fails if any re-score breaks
        FAILS.append((lane, f"{type(ex).__name__}: {ex}"))
        P(f"    !! {lane}: re-score raised {type(ex).__name__}: {str(ex)[:300]}")
        return None


# ================================================================================================= R1  FP6 (full re-run)
def r1_fp6():
    banner("R1  FP6 (the (H) combination; KiDS lead grade): the committed script re-run with the corrected projection")
    old = lane_json(os.path.join(HERE, "FP6_gate_survey_results.json"))
    ns, txt = exec_slices(P6, [(None, 'banner("K  CONTROLS'), ('banner("K  CONTROLS', "json.dump(OUT, open(os.path.join(HERE, f\"FP6_gate_survey_results")],
                          hooks={0: lambda n: n.__setitem__("esd_of_M", fix6)}, name="fp6_rerun")
    RERUN["FP6"] = dict(text=txt)
    on = old["numbers"]
    nn = json.loads(json.dumps(jclean(ns["OUT"]["numbers"]), default=str))
    row("FP6", "K2 L341 F7 control: nu_mono untruncated chi^2 (was 118.0)", "can", on["K2"]["none"], nn["K2"]["none"])
    row("FP6", "K2 L341 F7 control: cut at 1 Mpc (was 106.8)", "can", on["K2"]["1.0"], nn["K2"]["1.0"])
    row("FP6", "K2 L341 F7 control: cut at 0.5 Mpc (was 223.0)", "can", on["K2"]["0.5"], nn["K2"]["0.5"])
    for f in FOOTS:
        row("FP6", "B5 isolated P2 chi^2 (the KiDS base)", f, on["B5"][f"{f}_None"], nn["B5"][f"{f}_None"])
        for L25 in (0.5, 0.75, 1.0, 1.3, 1.6):
            row("FP6", f"B5 d chi^2 at L(0.25) = {L25} Mpc", f, on["B5"][f"{f}_{L25}"], nn["B5"][f"{f}_{L25}"], 9.0)
    xs = [0.3, 0.4, 0.5, 0.6, 0.75, 1.0, 1.3, 1.6, 2.0]
    LK = {}
    for f in FOOTS:
        LK[f] = (interp_cross(xs, [on["B5"][f"{f}_{x}"] for x in xs], 9.0), interp_cross(xs, [nn["B5"][f"{f}_{x}"] for x in xs], 9.0))
        row("FP6", "B5 KiDS floor L_KiDS [Mpc] (d chi^2 = +9 crossing)", f, LK[f][0], LK[f][1])
    for n_ in (1, 2, 3, 4):
        for f in FOOTS:
            po, pn = on["B6"]["pincer"][f"{n_}_{f}"], nn["B6"]["pincer"][f"{n_}_{f}"]
            row("FP6", f"B6 n={n_}: R0 at the KiDS floor [Mpc] (edge 1.21; pincer needs >)", f, po["R0_at_LKiDS"], pn["R0_at_LKiDS"], M6["LG_EDGE"], "gt")
            row("FP6", f"B6 n={n_}: KiDS d chi^2 at L_LG (R0 = 0.96)", f, po["KiDS_at_LLG"], pn["KiDS_at_LLG"], 9.0)
    for k_ in ("1.3_3e-07", "1.3_1e-06", "1.3_3e-06", "1.6_1e-06", "2.0_1e-06", "2.0_3e-06"):
        L25, y25 = k_.split("_")
        ko = on["H1"][f"2.0_{L25}_4.0_{y25}"]["kids"]; kn = nn["H1"][f"2.0_{L25}_4.0_{y25}"]["kids"]
        row("FP6", f"H1 KiDS column, L(0.25) = {L25}, y_th(0.25) = {y25}", "can", ko, kn, 9.0)
    win_o = [k_ for k_, v in on["H1"].items() if (max(v["s8"].values()) <= 1.05 and min(v["s8"].values()) >= 0.922 and max(v["forest"].values()) <= 0.10
                                                  and abs(v["flag"]) <= 0.05 and v["kids"] <= 9.0)]
    win_n = [k_ for k_, v in nn["H1"].items() if (max(v["s8"].values()) <= 1.05 and min(v["s8"].values()) >= 0.922 and max(v["forest"].values()) <= 0.10
                                                  and abs(v["flag"]) <= 0.05 and v["kids"] <= 9.0)]
    row("FP6", "H1 window: cells passing every gate (of 81; H1 needs >= 3)", "can", len(win_o), len(win_n), 2.5, "gt")
    for f in FOOTS:
        row("FP6", "H2 the (H) HEADLINE: KiDS d chi^2 (gate <= +9)", f, on["H2"]["kids"][f], nn["H2"]["kids"][f], 9.0)
    fl = summarize_rerun("FP6", ns, old)
    OUT["numbers"]["R1_FP6"] = dict(L_KiDS={f: list(v) for f, v in LK.items()}, window=[len(win_o), len(win_n)],
                                    headline={f: [on["H2"]["kids"][f], nn["H2"]["kids"][f]] for f in FOOTS}, flips=fl)
    show_rows("FP6")
    P(f"    {el()}")
    return True


# ================================================================================================= R2  FP9 (full re-run)
def r2_fp9():
    banner("R2  FP9 (the (H_Y) separator; FP11/FP12/FP13's baseline): the committed script re-run with the corrected projection")
    old = lane_json(os.path.join(HERE, "FP9_web_galaxy_separator_results.json"))
    mark_k = "# ================================================================================================= K  CONTROLS"
    mark_end = "json.dump(OUT, open(os.path.join(HERE, f\"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json\")"
    ns, txt = exec_slices(P9, [(None, mark_k), (mark_k, mark_end)], hooks={0: lambda n: n["M6"].__setitem__("esd_of_M", fix6)}, name="fp9_rerun")
    RERUN["FP9"] = dict(text=txt)
    on, nn = old["numbers"], jclean(ns["OUT"]["numbers"])
    for f in FOOTS:
        row("FP9", "K1 control: FP6's headline KiDS through FP9's exec (tracks FP6 H2)", f, on["K1"]["kids"][f], nn["K1"]["kids"][f])
    for f in FOOTS:
        for L25 in (1.0, 1.3):
            row("FP9", f"I5 d chi^2 at L(0.25) = {L25} Mpc (band-pass alone)", f, on["I5"]["kids"][str((f, L25))], nn["I5"]["kids"][str((f, L25))], 9.0)
        row("FP9", "I5 KiDS floor L_KiDS [Mpc] (route (i); FP11 X1 / FP12 'KiDS needs >= ~1.2')", f, on["I5"]["L_kids"][f], nn["I5"]["L_kids"][f])
    for y25 in ("3e-07", "1e-06", "2e-06", "3e-06"):
        for L25 in ("1.3", "1.6"):
            ko = on["H1"][f"2.0_{L25}_4.0_{y25}"]["kids"]; kn = nn["H1"][f"2.0_{L25}_4.0_{y25}"]["kids"]
            row("FP9", f"H1 KiDS column, L(0.25) = {L25}, y_th(0.25) = {y25}", "can", ko, kn, 9.0)
    row("FP9", "H1 window: cells passing every gate (of 48; H1 needs >= 10)", "can", len(on["H1_window"]), len(nn["H1_window"]), 9.5, "gt")
    for f in FOOTS:
        row("FP9", "H2 the (H_Y) HEADLINE at z = 0.25: KiDS d chi^2 (gate <= +9)", f, on["H2"]["kids"][f], nn["H2"]["kids"][f], 9.0)
    for k_ in on["H3"]:
        for f in FOOTS:
            row("FP9", f"H3 LG R0 at (n, L(0.25)) = {k_} [Mpc] (unchanged: no KiDS input)", f, on["H3"][k_][f], nn["H3"][k_][f])
    for f in FOOTS:
        row("FP9", "D6 route (ii): KiDS needs the web on-fraction f(0.25) >=", f, on["D6"]["f_KiDS"][f], nn["D6"]["f_KiDS"][f])
    for ell in ("1.0", "3.0", "10.0"):
        row("FP9", f"V2 Yukawa: KiDS d chi^2 at ell = {ell} Mpc (can)", "can", on["V2"]["kids"][ell], nn["V2"]["kids"][ell], 9.0)
    row("FP9", "V2 Yukawa: KiDS needs ell >= [Mpc]", "can", on["V2"]["ell_KiDS"], nn["V2"]["ell_KiDS"])
    LK = {f: (on["I5"]["L_kids"][f], nn["I5"]["L_kids"][f]) for f in FOOTS}
    fl = summarize_rerun("FP9", ns, old)
    OUT["numbers"]["R2_FP9"] = dict(L_KiDS={f: list(v) for f, v in LK.items()}, window=[len(on["H1_window"]), len(nn["H1_window"])],
                                    window_cells_after=nn["H1_window"], headline={f: [on["H2"]["kids"][f], nn["H2"]["kids"][f]] for f in FOOTS}, flips=fl)
    show_rows("FP9")
    P(f"    {el()}")
    return True


if want("R1"):
    NS6 = guard("FP6", r1_fp6)
if want("R2"):
    NS9 = guard("FP9", r2_fp9)



# ================================================================================================= R3  FP13 (targeted: the state separator)
def load_fp13():
    """FP13's module and main()'s body up to its K banner, exec'd read-only (XR18_state_separator's recipe)."""
    src = open(P13).read()
    mod = src[:src.index("\ndef main():")]
    body = src[src.index("\ndef main():") + len("\ndef main():"):
               src.index('    banner("K  CONTROLS: the reused machinery reproduces the record; the halofit, the state, FP11\'s hook")')]
    body = "\n".join(l_[4:] if l_.startswith("    ") else l_ for l_ in body.split("\n"))
    ns = {"__file__": P13, "__name__": "fp13_machinery", "open": _ro_open}
    with lane_env():
        exec(compile(mod, P13, "exec"), ns)
        exec(compile(body, P13, "exec"), ns)
    return ns


def r3_fp13():
    banner("R3  FP13 (the state separator H_S; the chain's current headline): KiDS at z = 0.25 / 0.4 / 0.7, its variants and windows")
    F13 = lane_json(os.path.join(HERE, "FP13_separator_from_state_results.json"))["numbers"]
    ns = load_fp13()
    m6 = ns["M6"]; kc = ns["kids_class"]; A0 = ns["A0"]; YI = ns["YIELD"]
    L_table, fun_of, yth_state = ns["L_table"], ns["fun_of"], ns["yth_state"]
    OmL_a, OmL_z = ns["OmL_a"], ns["OmL_z"]
    LH_tab = L_table(ns["HEAD_S"], ns["HEAD_READ"]); Lh = fun_of(LH_tab)
    yh = yth_state(LH_tab, ns["HEAD_READ"], ns["HEAD_SWITCH"], ns["HEAD_CY"])[0]
    LL9 = ns["ns9"]["LL_of"](1.3, 2.0)
    L9 = lambda a: LL9 * OmL_a(a)
    y9 = lambda a: 1e-6 * (OmL_z(0.25) / OmL_a(a)) ** 4.0
    y9d = {f: y9 for f in FOOTS}
    ystep = yth_state(LH_tab, ns["HEAD_READ"], "step", 1.0)[0]
    yeq = yth_state(LH_tab, ns["HEAD_READ"], "eq", 1.0)[0]
    Llin13 = L_table(1.3, "lin"); Lf13 = fun_of(Llin13); ylin13 = yth_state(Llin13, "lin", "ramp", 1.0)[0]
    yoff = {f: (lambda a: 0.0) for f in FOOTS}
    A3S = [("NL", s_) for s_ in (1.0, 1.2, 1.3, 1.5, ns["DELTA_C"], 2.0, 2.4, 2.6, 2.7)] + [("lin", s_) for s_ in (1.0, 1.1, 1.2, 1.4, 1.6, 1.65, ns["DELTA_C"], 1.75)]
    A3T = {}
    for rd, s_ in A3S:
        Lt = L_table(s_, rd); A3T[(rd, s_)] = (fun_of(Lt), yth_state(Lt, rd, "ramp", 1.0)[0])
    A7T = {}
    for fH in (1.0, 0.6, 0.44, 0.34, 0.2):
        ns["STATE"]["fH"] = [((lambda q: q[0] + fH * q[1])(ns["halofit"](ns["D2LIN"][i], ns["AGR"][i], split=True))
                              if ns["sig2"](ns["RMIN"], ns["D2LIN"][i]) > 1.0 else ns["D2LIN"][i]) for i in range(len(ns["LNA"]))]
        Lt = L_table(ns["DELTA_C"], "fH"); A7T[fH] = (fun_of(Lt), yth_state(Lt, "fH", "ramp", 1.0)[0])
    ns["STATE"].pop("fH", None)
    L025_h3 = F13["H3"]["L025"]

    def kz(L, yd, f, z, KB):
        a = 1 / (1 + z); yv = yd[f](a) if isinstance(yd, dict) else yd(a)
        return kc(A0[f], L(a), yv, YI) - KB[f]

    def score(proj):
        m6["esd_of_M"] = proj
        KB = {f: kc(A0[f]) for f in FOOTS}
        r = {"KB": KB}
        for f in FOOTS:
            for z in (0.25, 0.4, 0.7):
                r[("H_S", f, z)] = kz(Lh, yh, f, z, KB)
                r[("step", f, z)] = kz(Lh, ystep, f, z, KB)
                r[("eq onset", f, z)] = kz(Lh, yeq, f, z, KB)
                r[("first y~1 (yield off)", f, z)] = kz(Lh, yoff, f, z, KB)
                r[("lin s=1.3", f, z)] = kz(Lf13, ylin13, f, z, KB)
                r[("FP9 H_Y", f, z)] = kz(L9, y9d, f, z, KB)
            r[("H3 L_sc", f, 0.25)] = kc(A0[f], L025_h3, yh[f](0.8), YI) - KB[f]
            for (rd, s_), (Lf, ysd) in A3T.items():
                r[(f"A3 {rd} s={s_:.3f} FP9 yield", f, 0.25)] = kz(Lf, y9d, f, 0.25, KB)
                r[(f"A3 {rd} s={s_:.3f} state yield", f, 0.25)] = kz(Lf, ysd, f, 0.25, KB)
            for fH, (Lf, ysd) in A7T.items():
                for z in (0.25, 0.4):
                    r[(f"A7 one-halo x{fH}", f, z)] = kz(Lf, ysd, f, z, KB)
        m6["esd_of_M"] = esd_bug6_13
        return r
    esd_bug6_13 = m6["esd_of_M"]
    fixf = (lambda M, Mb: (m6["RP"] / m6["MPCm"], FIX1(M, Mb))) if not MUTATE else esd_bug6_13
    B, A = score(esd_bug6_13), score(fixf)
    # control: the committed numbers with the committed projection
    ctl = [(B[("H_S", f, 0.25)], F13["H1"]["kids"][f]) for f in FOOTS] + [(B[("H_S", f, 0.4)], F13["H1"]["kids04"][f]) for f in FOOTS] \
        + [(B[("H_S", f, 0.7)], F13["H1"]["kids07"][f]) for f in FOOTS] + [(B[("H3 L_sc", f, 0.25)], F13["H3"]["kids"][f]) for f in FOOTS] \
        + [(B[("FP9 H_Y", f, 0.4)], F13["H5"]["FP9 (H_Y) itself"]["kids04"][f]) for f in FOOTS] \
        + [(B[("step", f, 0.4)], F13["H5"]["step"]["kids04"][f]) for f in FOOTS] \
        + [(B[("lin s=1.3", f, 0.4)], F13["H5"]["linear reading, s = 1.3"]["kids04"][f]) for f in FOOTS] \
        + [(B[(f"A7 one-halo x{fH}", f, 0.4)], F13["A7"][str(fH)]["kids04"][f]) for fH in (1.0, 0.6, 0.44, 0.34, 0.2) for f in FOOTS]
    for (rd, s_) in A3S:
        for yl in ("FP9 yield", "state yield"):
            ref = F13["A3"][f"{rd}_{s_:.3f}_{yl}"]["kids"]
            ctl += [(B[(f"A3 {rd} s={s_:.3f} {yl}", f, 0.25)], ref[f]) for f in FOOTS]
    dctl = max(abs(a - b) for a, b in ctl)
    P(f"    control: {len(ctl)} committed FP13 KiDS numbers recomputed with the committed projection: max |d chi^2| {dctl:.1e}")
    OUT["numbers"]["R3_control_max_dev"] = dctl
    for f in FOOTS:
        row("FP13", "base: isolated P2 chi^2 (FP13's KB)", f, B["KB"][f], A["KB"][f])
    for z in (0.25, 0.4, 0.7):
        for f in FOOTS:
            row("FP13", f"H1 the H_S HEADLINE: KiDS d chi^2 at z = {z} (gate <= +9)", f, B[("H_S", f, z)], A[("H_S", f, z)], 9.0)
    for f in FOOTS:
        row("FP13", "H3 self-consistent L_sc (L(0.25) = 2.06 Mpc): KiDS", f, B[("H3 L_sc", f, 0.25)], A[("H3 L_sc", f, 0.25)], 9.0)
    for v_ in ("FP9 H_Y", "step", "lin s=1.3", "eq onset", "first y~1 (yield off)"):
        for z in (0.25, 0.4):
            for f in FOOTS:
                row("FP13", f"H5/C2 variant '{v_}': KiDS at z = {z}", f, B[(v_, f, z)], A[(v_, f, z)], 9.0)
    for fH in (1.0, 0.6, 0.44, 0.34, 0.2):
        for z in (0.25, 0.4):
            for f in FOOTS:
                row("FP13", f"A7 one-halo x{fH}: KiDS at z = {z}", f, B[(f"A7 one-halo x{fH}", f, z)], A[(f"A7 one-halo x{fH}", f, z)], 9.0)
    # the A3 windows, recomputed with the committed other gates
    win = {}
    for tag, R_ in (("before", B), ("after", A)):
        for rd in ("NL", "lin"):
            for yl in ("FP9 yield", "state yield"):
                cells = []
                for (rd2, s_) in A3S:
                    if rd2 != rd:
                        continue
                    ok_ = dict(F13["A3"][f"{rd}_{s_:.3f}_{yl}"]["ok"])
                    ok_["KiDS"] = max(R_[(f"A3 {rd} s={s_:.3f} {yl}", f, 0.25)] for f in FOOTS) <= 9.0
                    if all(ok_.values()):
                        cells.append(round(s_, 3))
                win[(tag, rd, yl)] = cells
    for rd in ("NL", "lin"):
        for yl in ("FP9 yield", "state yield"):
            for (rd2, s_) in A3S:
                if rd2 == rd:
                    for f in FOOTS:
                        row("FP13", f"A3 {rd} s = {s_:.3f} ({yl}): KiDS at z = 0.25", f, B[(f"A3 {rd} s={s_:.3f} {yl}", f, 0.25)],
                            A[(f"A3 {rd} s={s_:.3f} {yl}", f, 0.25)], 9.0)
    P("    A3 windows (s passing all five gates; the other gates as committed): " + "; ".join(
        f"{rd}/{yl}: {win[('before', rd, yl)]} -> {win[('after', rd, yl)]}" for rd in ("NL", "lin") for yl in ("FP9 yield", "state yield")))
    dc = round(ns["DELTA_C"], 3)
    a3a_b = dc in win[("before", "NL", "FP9 yield")] and dc in win[("before", "NL", "state yield")]
    a3a_a = dc in win[("after", "NL", "FP9 yield")] and dc in win[("after", "NL", "state yield")]
    a7s = {tag: [fH for fH in (1.0, 0.6, 0.44, 0.34, 0.2) if F13["A7"][str(fH)]["all"] and max(R_[(f"A7 one-halo x{fH}", f, 0.25)] for f in FOOTS) <= 9
                 and max(R_[(f"A7 one-halo x{fH}", f, 0.4)] for f in FOOTS) <= 9] for tag, R_ in (("before", B), ("after", A))}
    h1_b = all(B[("H_S", f, 0.25)] <= 9 for f in FOOTS); h1_a = all(A[("H_S", f, 0.25)] <= 9 for f in FOOTS)
    h1s_b = all(B[("H_S", f, z)] <= 9 for f in FOOTS for z in (0.25, 0.4)); h1s_a = all(A[("H_S", f, z)] <= 9 for f in FOOTS for z in (0.25, 0.4))
    FLIPS["FP13"] = [dict(id=k_, before="PASS" if b_ else "FAIL", after="PASS" if a_ else "FAIL", load_bearing=lb_, name=nm_)
                     for k_, b_, a_, lb_, nm_ in (("H1", h1_b, h1_a, True, "H_S passes KiDS at z = 0.25 (with the other four gates as committed)"),
                                                  ("H1+z0.4", h1s_b, h1s_a, False, "H_S passes KiDS at z = 0.25 AND 0.4 (the lens-spread check)"),
                                                  ("A3a", a3a_b, a3a_a, True, "delta_c inside both NL windows"),
                                                  ("A7-spread", a7s["before"] == a7s["after"], True, False, f"A7 one-halo factors passing + KiDS@0.4: {a7s['before']} -> {a7s['after']}"))
                     if b_ != a_]
    P(f"    FP13 verdicts: H1 (H_S, z = 0.25) {'PASS' if h1_b else 'FAIL'} -> {'PASS' if h1_a else 'FAIL'}; with z = 0.4 {'PASS' if h1s_b else 'FAIL'} -> "
      f"{'PASS' if h1s_a else 'FAIL'}; A3a (delta_c in both NL windows) {a3a_b} -> {a3a_a}; A7 factors passing + z = 0.4: {a7s['before']} -> {a7s['after']}")
    OUT["numbers"]["R3_FP13"] = dict(windows={f"{k_[0]}/{k_[1]}/{k_[2]}": v for k_, v in win.items()}, A7_spread=a7s,
                                     headline={f"{f}/{z}": [B[("H_S", f, z)], A[("H_S", f, z)]] for f in FOOTS for z in (0.25, 0.4, 0.7)},
                                     control_max_dev=dctl, flips=FLIPS["FP13"])
    show_rows("FP13")
    P(f"    {el()}")
    return dict(B=B, A=A, dctl=dctl)


# ================================================================================================= R4  FP12 (targeted)
def r4_fp12():
    banner("R4  FP12 (the Local Volume groups' R0): the (H_Y) KiDS row, the knobs' KiDS cost (U1) and the outer-profile cut (U2)")
    with lane_env():
        sys.path.insert(0, HERE)
        import FP12_local_volume_groups_r0 as F12
    F12J = lane_json(os.path.join(HERE, "FP12_local_volume_groups_r0_results.json"))["numbers"]
    m6 = F12.M6; kc, kchi = m6["kids_class"], m6["kids_chi2"]; A0, HEAD, YI = F12.A0, F12.HEAD, F12.YIELD
    OmL_z = F12.OmL_z
    yz = lambda z, y25=HEAD["y25"], pp=HEAD["pp"]: y25 * (OmL_z(0.25) / OmL_z(z)) ** pp
    bug = m6["esd_of_M"]
    fixf = (lambda M, Mb: (m6["RP"] / m6["MPCm"], FIX1(M, Mb))) if not MUTATE else bug

    def score(proj):
        m6["esd_of_M"] = proj
        try:
            KB = {f: kc(A0[f]) for f in FOOTS}
            r = {"KB": KB}
            for f in FOOTS:
                r[("HY", f)] = kc(A0[f], HEAD["L25"], yz(0.25), YI) - KB[f]
                kn = F12J["U"]["knobs"][f]
                r[("kids_L", f)] = kc(A0[f], kn["L25"], yz(0.25), YI) - KB[f]
                r[("kids_y", f)] = kc(A0[f], HEAD["L25"], yz(0.25, kn["y25"]), YI) - KB[f]
                for fsc in (1.0, 0.3, 0.5, 0.8):
                    def Mf(Mb, f=f, fsc=fsc):
                        return Mb + np.interp(m6["RR"], F12.RG, F12.phantom(Mb, A0[f], HEAD["L25"] * F12.MPC, yz(0.25), YI) * F12.fprof(fsc)(F12.RG))
                    r[("kids_f", f, fsc)] = kchi(Mf) - KB[f]
            return r
        finally:
            m6["esd_of_M"] = bug
    B, A = score(bug), score(fixf)
    ctl = [(B[("kids_L", f)], F12J["U"]["knobs"][f]["kids_L"]) for f in FOOTS] + [(B[("kids_y", f)], F12J["U"]["knobs"][f]["kids_y"]) for f in FOOTS] \
        + [(B[("kids_f", f, x)], F12J["U"]["kids_f"][f"{f}/{x}"]) for f in FOOTS for x in (1.0, 0.3, 0.5, 0.8)]
    dctl = max(abs(a - b) for a, b in ctl)
    P(f"    control: FP12's committed U1/U2 KiDS numbers with the committed projection: max |d chi^2| {dctl:.1e}")
    for f in FOOTS:
        row("FP12", "K7 the (H_Y) headline KiDS (= FP9 H2)", f, B[("HY", f)], A[("HY", f)], 9.0)
        row("FP12", "U1 knob L(0.25) -> stack R0: KiDS cost (knob fails iff > +9)", f, B[("kids_L", f)], A[("kids_L", f)], 9.0, "gt")
        row("FP12", "U1 knob y_th(0.25) -> stack R0: KiDS cost (knob fails iff > +9)", f, B[("kids_y", f)], A[("kids_y", f)], 9.0, "gt")
        for x in (0.3, 0.5, 0.8, 1.0):
            row("FP12", f"U2 outer-profile cut f = {x}: KiDS d chi^2", f, B[("kids_f", f, x)], A[("kids_f", f, x)], 9.0)
    u1_b = all(B[(k_, f)] > 9 for k_ in ("kids_L", "kids_y") for f in FOOTS); u1_a = all(A[(k_, f)] > 9 for k_ in ("kids_L", "kids_y") for f in FOOTS)
    FLIPS["FP12"] = [] if u1_b == u1_a else [dict(id="U1", before="PASS" if u1_b else "FAIL", after="PASS" if u1_a else "FAIL", load_bearing=True,
                                                  name="U1 the chain's own knobs cannot do the universal fix (both cost KiDS > +9)")]
    OUT["numbers"]["R4_FP12"] = dict(control_max_dev=dctl, U1=[u1_b, u1_a], flips=FLIPS["FP12"],
                                     rows={f"{k_}": [B[k_], A[k_]] for k_ in B if k_ != "KB"})
    show_rows("FP12")
    P(f"    {el()}")
    return dict(dctl=dctl)


# ================================================================================================= R6  FP1 E (full re-run of the E section)
def r6_fp1():
    banner("R6  FP1 E (the KiDS-EFE pincer; the tolerances FP11 P1 and FP12 quote): FP1's header + E section re-run with the corrected projection")
    old = lane_json(os.path.join(HERE, "FP1_static_sector_results.json"))
    mA = "# ================================================================================================ A  static reduction"
    mE = "# ================================================================================================ E  (c) KiDS-EFE pincer"
    mL = "LYT = np.linspace(-9.5, 6.5, 1601)"
    mW = "# ================================================================================================ W ledger"
    ns, txt = exec_slices(P1, [(None, mA), (mE, mL), (mL, mW)], hooks={1: lambda n: n.__setitem__("esd_of_M", fix1)}, name="fp1_E_rerun")
    RERUN["FP1E"] = dict(text=txt)
    oE3, nE3 = old["numbers"]["E3"], jclean(ns["OUT"]["numbers"]["E3"])
    oE4, nE4 = old["numbers"]["E4"]["fits"], jclean(ns["OUT"]["numbers"]["E4"]["fits"])
    e0 = ns["e0"]
    e0_ref = {"canonical": (116.3, 233.4, 548.3), "alt": (107.5, 241.0, 561.6)}
    for f in FOOTS:
        row("FP1E", "E0 control: nu_mono (L355's a0) isolated chi^2 (L355 K1)", f, e0_ref[f][0], e0[f][0])
        row("FP1E", "E0 control: baryons-only kernel d chi^2 (L355 K2)", f, e0_ref[f][1], e0[f][1])
        row("FP1E", "E3 P2 isolated chi^2 (the base)", f, oE3[f]["KiDS_ref"], nE3[f]["KiDS_ref"])
        row("FP1E", "E3 KiDS TOLERANCE e (3D rms, a0), no 2-halo (+9 crossing)", f, oE3[f]["e_KiDS_no2h"] * 1e4, nE3[f]["e_KiDS_no2h"] * 1e4)
        row("FP1E", "E3 KiDS TOLERANCE e (3D rms, 1e-4 a0), 2-halo A <= 2", f, oE3[f]["e_KiDS_2h"] * 1e4, nE3[f]["e_KiDS_2h"] * 1e4)
        row("FP1E", "E3 the LG needs e (1e-4 a0; unchanged) / KiDS tolerates (2-halo): ratio", f, oE3[f]["ratio_central"], nE3[f]["ratio_central"], 1.0, "gt")
        row("FP1E", "E3 band-edge need / 2-halo tolerance (the loosest reading)", f, oE3[f]["ratio_generous"], nE3[f]["ratio_generous"], 1.0, "gt")
        row("FP1E", "E3 KiDS at the core's own baryonic web field (FAIL iff > +9)", f, oE3[f]["KiDS_own_baryons"], nE3[f]["KiDS_own_baryons"], 9.0, "gt")
        row("FP1E", "E3 KiDS at the core's own all-matter web field", f, oE3[f]["KiDS_own_all"], nE3[f]["KiDS_own_all"], 9.0, "gt")
        row("FP1E", "E3 KiDS at Brouwer's quiet field, baryons, 2-halo", f, oE3[f]["KiDS_quiet_field"]["baryons"][1], nE3[f]["KiDS_quiet_field"]["baryons"][1], 9.0, "gt")
        row("FP1E", "E4 2-halo amplitude FREE, baryons-only field", f, oE4[f]["Ainf"], nE4[f]["Ainf"], 9.0, "gt")
        row("FP1E", "E4 2-halo amplitude FREE, all-matter field", f, oE4[f]["Ainf_all"], nE4[f]["Ainf_all"], 9.0, "gt")
    fl = summarize_rerun("FP1 E", ns, {"checks": {k_: v for k_, v in old["checks"].items() if k_.split()[0] in [c[0].split()[0] for c in ns["CH"]]}})
    OUT["numbers"]["R6_FP1E"] = dict(E3={f: {k_: [oE3[f][k_], nE3[f][k_]] for k_ in ("KiDS_ref", "e_KiDS_no2h", "e_KiDS_2h", "ratio_central", "ratio_strict",
                                                                                 "ratio_generous", "KiDS_own_baryons", "KiDS_own_all")} for f in FOOTS},
                                     E4={f: {k_: [oE4[f][k_], nE4[f][k_]] for k_ in ("A2", "Ainf", "Ainf_all")} for f in FOOTS}, flips=fl)
    show_rows("FP1E")
    P(f"    {el()}")
    return dict(E3=nE3)


# ================================================================================================= R5  FP11 (derived from R2 and R6)
def r5_fp11(fp9, fp1):
    banner("R5  FP11 (the Local Group flyby): its KiDS rows are FP9's H2 (K7, G1) and FP1 E3's tolerances (P1) -- re-read from R2 and R6")
    F11J = lane_json(os.path.join(HERE, "FP11_local_group_flyby_results.json"))["numbers"]
    for f in FOOTS:
        if fp9 is not None:
            r_ = [t for t in TABLE if t["lane"] == "FP9" and t["item"].startswith("H2 the (H_Y) HEADLINE") and t["foot"] == f][0]
            row("FP11", "K7/G1 the (H_Y) KiDS row (= FP9 H2)", f, r_["before"], r_["after"], 9.0)
        if fp1 is not None:
            p1 = F11J["P1"][f]
            row("FP11", "P1 the LG's needed e / KiDS's 2-halo tolerance (pincer holds iff > 1)", f, p1["e_needed"] / p1["KiDS_2h"],
                p1["e_needed"] / fp1["E3"][f]["e_KiDS_2h"], 1.0, "gt")
            row("FP11", "P1 band-edge need / KiDS's 2-halo tolerance (reported)", f, p1["e_band_edge"] / p1["KiDS_2h"],
                p1["e_band_edge"] / fp1["E3"][f]["e_KiDS_2h"], 1.0, "gt")
    fl = []
    if fp1 is not None:
        b_ = all(F11J["P1"][f]["e_needed"] > F11J["P1"][f]["KiDS_2h"] for f in FOOTS)
        a_ = all(F11J["P1"][f]["e_needed"] > fp1["E3"][f]["e_KiDS_2h"] for f in FOOTS)
        if b_ != a_:
            fl.append(dict(id="P1", before="PASS" if b_ else "FAIL", after="PASS" if a_ else "FAIL", load_bearing=True, name="P1 the pincer is not relieved"))
    FLIPS["FP11"] = fl
    OUT["numbers"]["R5_FP11"] = dict(flips=fl)
    show_rows("FP11")


# ================================================================================================= R7  FP14 / FP17 (full re-runs)
def r7_fp14_17():
    banner("R7  FP14 and FP17 (the zero-knob core; screening without xi): the committed scripts re-run with FP1 E's projection corrected in their GK")
    out = {}
    for lane, path, jf in (("FP14", P14, "FP14_zero_knob_core_results.json"), ("FP17", P17, "FP17_screening_without_xi_results.json")):
        old = lane_json(os.path.join(HERE, jf))
        mW = 'W0K = np.zeros(len(GK["ES"]))'
        mJ = "json.dump(OUT, open(os.path.join(HERE, f\"{SLUG}_results.json\""
        ns, txt = exec_slices(path, [(None, mW), (mW, mJ)], hooks={0: lambda n: n["GK"].__setitem__("esd_of_M", fix1)}, name=f"{lane.lower()}_rerun")
        RERUN[lane] = dict(text=txt)
        ref_p2 = {"canonical": 110.6, "alt": 102.4}
        for f in FOOTS:
            row(lane, "K control: P2 isolated chi^2 (FP1 E's machinery)", f, ref_p2[f], ns["KI_P2"][f])
            row(lane, "Newtonian (MOND off) minus P2: KiDS d chi^2 (X2 / V3 need > +500)", f, 1230.3 - ref_p2[f], ns["KI_N"][f] - ns["KI_P2"][f], 500.0, "gt")
        if lane == "FP17":
            V3o, V4o = old["numbers"]["V3"]["kids"], old["numbers"]["V4"]["kids_at_gw_ceiling"]
            for f in FOOTS:
                row(lane, "V3 BDEF with k^(1/4) = c/H: KiDS d chi^2 vs P2 (FAIL iff > +500)", f, V3o[f] - ref_p2[f], ns["ki_b_free"][f] - ns["KI_P2"][f], 500.0, "gt")
                row(lane, "V4 BDEF at the GW170817 ceiling: KiDS d chi^2", f, V4o[f], ns["ki_b_top"][f] - ns["KI_P2"][f], 9.0)
        out[lane] = summarize_rerun(lane, ns, old)
        show_rows(lane)
    OUT["numbers"]["R7"] = {k_: dict(flips=v) for k_, v in out.items()}
    P(f"    {el()}")


# ================================================================================================= R8  L355 (full re-run)
def r8_l355():
    banner("R8  L355 (KiDS for the kernel-invisible construction; the record's 'KiDS needs a web-blind kernel'): re-run with the corrected projection")
    old = lane_json(P55.replace(".py", "_results.json"))
    mL = "LYT = np.linspace(-9.5, 6.5, 1601); YT = 10**LYT"
    ns, txt = exec_slices(P55, [(None, mL), (mL, 'banner("VERDICT")')], hooks={0: lambda n: n.__setitem__("esd_of_M", fix1)}, name="l355_rerun")
    RERUN["L355"] = dict(text=txt)
    on, nn = old["numbers"], jclean(ns["OUT"]["numbers"])
    for f in FOOTS:
        row("L355", "K1 isolated-MOND base chi^2 (nu_mono, L355's a0)", f, on["K1"][f], nn["K1"][f])
        for fld in ("linear-theory (16 Mpc)", "Brouwer+21 quiet (e = 0.003 a0)"):
            row("L355", f"K2 baryons-only kernel deficit, {fld[:22]} (K2 needs >= +100/+50)", f, on["K2"][f"{f}/{fld}"], nn["K2"][f"{f}/{fld}"])
        for fd0 in ("0.8", "0.9"):
            row("L355", f"K3 + carrier (f_d(0) = {fd0}) + 2-halo at the OWN field (construction fails iff > +9)", f,
                on["K3"][f"{f}/linear-theory (16 Mpc)/{fd0}"][0], nn["K3"][f"{f}/linear-theory (16 Mpc)/{fd0}"][0], 9.0, "gt")
        row("L355", "K4 best carrier fraction f_s at the own field (K4: <= 0.1)", f, on["K4"][f"{f}/linear-theory (16 Mpc)"][1], nn["K4"][f"{f}/linear-theory (16 Mpc)"][1], 0.1)
        row("L355", "K4 d chi^2 at the best f_s (still misses iff > +9)", f, on["K4"][f"{f}/linear-theory (16 Mpc)"][0], nn["K4"][f"{f}/linear-theory (16 Mpc)"][0], 9.0, "gt")
    fl = summarize_rerun("L355", ns, old)
    OUT["numbers"]["R8_L355"] = dict(K1={f: [on["K1"][f], nn["K1"][f]] for f in FOOTS}, K2={k_: [on["K2"][k_], nn["K2"][k_]] for k_ in on["K2"]},
                                     K3={k_: [on["K3"][k_][0], nn["K3"][k_][0]] for k_ in on["K3"]}, K4={k_: [on["K4"][k_], nn["K4"][k_]] for k_ in on["K4"]}, flips=fl)
    show_rows("L355")
    P(f"    {el()}")
    return nn


# ================================================================================================= R9  the P2 family
def model_M2_factory(L, direct):
    """L352's model_M2 (L352:180-193) with its projection selectable: direct=True projects M itself with exact shells."""
    rr_, Rp_, G_, MPCm_ = L["rr"], L["Rp"], L["G"], L["MPCm"]

    def model_M2(Mb, a0, xc, mode, z):
        M = Mb * L["nu_vec"](G_ * Mb / rr_ ** 2 / a0); re = None
        if xc and mode != "none":
            rho_dyn = np.gradient(M, rr_) / (4 * math.pi * rr_ ** 2)
            rho_bar = L["Om"] * L["rho_crit0"] * (1 + z) ** 3
            on = 4 * math.pi * G_ * (rho_dyn - rho_bar) / L["Hz"](z) ** 2 >= xc
            it = int(np.where(on)[0].max()) if on.any() else 0; re = rr_[it]
            M = np.where(np.arange(len(rr_)) > it, M[it], M)
        if direct and not MUTATE:
            M2c = FIX2.C @ np.diff(M - Mb) + (M[0] - Mb)
        else:
            M2c = L["project_M2"](np.gradient(M - Mb, rr_) / (4 * math.pi * rr_ ** 2))
        m_sh = -(M[-1] - Mb) if (mode == "compensated" and re is not None) else 0.0

        def f(R, M2c=M2c, m_sh=m_sh, re=re):
            val = np.interp(np.log(R), np.log(Rp_), M2c) + Mb
            return val + (L["shell_M2"](m_sh, re, R) if m_sh else 0.0)
        return f, (re / MPCm_ if re is not None else None)
    return model_M2


def r9_p2():
    banner("R9  THE P2 FAMILY (L352's projection: L352/L359/L360, AT3's switched gate, FP4/FP10 via AT3, DE8 -> DE10 -> XR9/XR14): re-scored cells")
    assert np.array_equal(L52["rr"], rr2) and np.array_equal(L52["Rp"], Rp2)
    orig = L52["model_M2"]
    # control: the copy with the committed projection is L352's model_M2
    mine = model_M2_factory(L52, direct=False)
    Rg = np.geomspace(0.03, 2.8, 50) * MPCm; dmax = 0.0
    for (lm, xc, mode) in ((10.5, 0.0, "none"), (11.0, 3.2477, "compensated"), (10.2, 5.0, "retained")):
        f1, _ = orig(10 ** lm * L52["MS"], L52["A0"]["canonical"], xc, mode, 0.25); f2, _ = mine(10 ** lm * L52["MS"], L52["A0"]["canonical"], xc, mode, 0.25)
        dmax = max(dmax, float(np.max(np.abs(f1(Rg) / f2(Rg) - 1))))
    P(f"    control: this lane's copy of L352's model_M2 with the committed projection reproduces L352's (max rel diff {dmax:.1e})")
    XE = 3.2477                                                                          # AT3's common cell x_c,eff(0.25) (AT3 C-banner)

    def fits(direct):
        L52["model_M2"] = model_M2_factory(L52, direct); L52["_PROF"].clear(); L52["_ESD"].clear()
        try:
            r = {}
            for f in FOOTS:
                a0 = L52["A0"][f]
                r[("base+2h", f)] = L52["fit_model"](a0, 0.0, "none", True)[0]
                r[("base no-2h", f)] = L52["fit_model"](a0, 0.0, "none", False)[0]
                r[("compensated x_c 3.2477 +2h", f)] = L52["fit_model"](a0, XE, "compensated", True)[0] - r[("base+2h", f)]
                r[("compensated x_c 5 +2h (L352 Z3)", f)] = L52["fit_model"](a0, 5.0, "compensated", True)[0] - r[("base+2h", f)]
                r[("retained x_c 5 no-2h (L342 B4)", f)] = L52["fit_model"](a0, 5.0, "retained", False)[0] - r[("base no-2h", f)]
            return r
        finally:
            L52["model_M2"] = orig; L52["_PROF"].clear(); L52["_ESD"].clear()
    B, A = fits(False), fits(True)
    ref = {"canonical": 174.30, "alt": 166.92}
    dctl = max(abs(B[("base+2h", f)] - ref[f]) for f in FOOTS)
    P(f"    control: L352's unswitched base chi^2 with the committed projection {B[('base+2h', 'canonical')]:.2f} / {B[('base+2h', 'alt')]:.2f} "
      f"(committed 174.30 / 166.92, as printed by DE8/L360/AT3)")
    for f in FOOTS:
        row("P2", "L352 unswitched base chi^2 (+2-halo)", f, B[("base+2h", f)], A[("base+2h", f)])
        row("P2", "L352 unswitched base chi^2 (no 2-halo)", f, B[("base no-2h", f)], A[("base no-2h", f)])
        row("P2", "AT3 common cell x_c,eff 3.2477, NO carrier (FP10 B4's cleared halos): d chi^2", f, B[("compensated x_c 3.2477 +2h", f)],
            A[("compensated x_c 3.2477 +2h", f)], 4.0)
        row("P2", "L352 Z3 compensated x_c = 5 +2-halo: d chi^2 (Z3: disfavoured iff > +9)", f, B[("compensated x_c 5 +2h (L352 Z3)", f)],
            A[("compensated x_c 5 +2h (L352 Z3)", f)], 9.0, "gt")
        row("P2", "L342 B4 retained x_c = 5, no 2-halo (control): d chi^2", f, B[("retained x_c 5 no-2h (L342 B4)", f)], A[("retained x_c 5 no-2h (L342 B4)", f)])
    # L360 full re-run (the assembled construction: switch cells x carrier cells, amplitude 1) -- the same code path as AT3's gate
    old60 = lane_json(P60.replace(".py", "_results.json"))

    def hook60(n):
        L = n["L52"]
        L["model_M2"] = model_M2_factory(L, True); L["_PROF"].clear(); L["_ESD"].clear()
        n["project_M2"] = fix2
    ns60, txt60 = exec_slices(P60, [(None, 'BASE = {f_: fit_model('), ('BASE = {f_: fit_model(', 'banner("VERDICT")')], hooks={0: hook60}, name="l360_rerun")
    RERUN["L360"] = dict(text=txt60)
    o60, n60 = old60["numbers"], jclean(ns60["OUT"]["numbers"])
    shifts = []
    for k_ in o60["M2"]:
        for f in FOOTS:
            b_, a_ = o60["M2"][k_]["dchi2"][f], n60["M2"][k_]["dchi2"][f]
            shifts.append(a_ - b_)
            row("L360", f"M2 pair {k_}: d chi^2 (gate <= +4)", f, b_, a_, 4.0)
    for k_ in o60["M1"]:
        row("L360", f"M1 undecayed carrier {k_}: d chi^2 (control: > +100)", "", o60["M1"][k_], n60["M1"][k_], 100.0, "gt")
    fl60 = summarize_rerun("L360", ns60, old60)
    np_b = sum(1 for v in o60["M2"].values() if v["ok"]); np_a = sum(1 for v in n60["M2"].values() if v["ok"])
    P(f"    L360: pairs passing KiDS (<= +4, both footings) {np_b} -> {np_a} of {len(o60['M2'])}; d chi^2 shift of the carrier pairs "
      f"{min(shifts):+.2f}..{max(shifts):+.2f}")
    # DE8 C1 (the isolated QUMOND ODE path through esd_from_mlens), the committed projection vs the corrected cells
    esdm_orig = D8["esd_from_mlens"]

    def esd_from_mlens_fix(Mb, Mext_face, b):
        Mf = np.concatenate([[0.0], Mext_face, [Mext_face[-1]]])
        M2 = fixc(np.diff(Mf) / (4 * math.pi * D8["V"]))
        return D8["annulus_esd"](lambda R, M2=M2: np.interp(np.log(R), np.log(D8["Rp"]), M2) + Mb, D8["Rd"][b])
    de8 = {}
    for tag, fn in (("before", esdm_orig), ("after", esd_from_mlens_fix)):
        D8["esd_from_mlens"] = fn; D8["_ESD"].clear()
        try:
            for f in FOOTS:
                de8[(tag, f)] = D8["fit_cell"](f, "none", 1.0, 1.0, None, 0.0, None)
        finally:
            D8["esd_from_mlens"] = esdm_orig; D8["_ESD"].clear()
    for f in FOOTS:
        row("P2", "DE8 C1: isolated QUMOND via the ODE + esd_from_mlens, chi^2", f, de8[("before", f)], de8[("after", f)])
        row("P2", "DE8 C1 minus L352's base (same projection before/after): d chi^2", f, de8[("before", f)] - B[("base+2h", f)], de8[("after", f)] - A[("base+2h", f)])
    # AT3's rows (its gate: the switched fit at the common cell with its retained carriers, <= +4): committed values, and the bound
    at3 = []
    try:
        t_ = open(os.path.join(REPO, "real_research", "acceleration_trigger_2026", "AT3_acceleration_trigger_full_gates.out")).read()
        at3 = [(float(a), float(b), float(c), float(d)) for a, b, c, d in re.findall(r"KiDS \(p1_x2\.5\) ([+-][\d.]+)/([+-][\d.]+) \(switch-free ([+-][\d.]+)/([+-][\d.]+)\)", t_)]
    except OSError:
        pass
    sh_nc = {f: A[("compensated x_c 3.2477 +2h", f)] - B[("compensated x_c 3.2477 +2h", f)] for f in FOOTS}
    if at3:
        P(f"    AT3: {len(at3)} committed rows, switched KiDS (its gate, <= +4) max {max(r_[0] for r_ in at3):+.1f} (can) / {max(r_[1] for r_ in at3):+.1f} (alt); "
          f"its window cells are re-scored exactly in R11 (its other rows fail X-COP, the flagship, galaxies or Harvey regardless)")
    FLIPS["L360"] = fl60
    OUT["numbers"]["R9_P2"] = dict(model_M2_copy_dev=dmax, L352={f"{k_[0]}/{k_[1]}": [B[k_], A[k_]] for k_ in B}, L360_pairs=[np_b, np_a, len(o60["M2"])],
                                   L360_shift=[min(shifts), max(shifts)] if shifts else None, DE8_C1={f"{k_[0]}/{k_[1]}": v for k_, v in de8.items()},
                                   no_carrier_shift=sh_nc, AT3_rows_committed=at3, flips_L360=fl60, control_base_dev=dctl)
    for ln in ("P2", "L360"):
        show_rows(ln)
    P(f"    {el()}")
    return dict(dctl=dctl, dmax=dmax)


# ================================================================================================= run the re-scores
R3 = guard("FP13", r3_fp13) if want("R3") else None
R4 = guard("FP12", r4_fp12) if want("R4") else None
R6 = guard("FP1 E", r6_fp1) if want("R6") else None
if want("R5"):
    guard("FP11", lambda: r5_fp11(NS9 if want("R2") else None, R6))
if want("R7"):
    guard("FP14/FP17", r7_fp14_17)
R8 = guard("L355", r8_l355) if want("R8") else None
R9 = guard("P2 family", r9_p2) if want("R9") else None


# ================================================================================================= R11  AT3 (exact, at its window cells)
def r11_at3():
    banner("R11  AT3 (the acceleration-triggered carrier): its KiDS GATE (L360's switched fit with AT3's retained carriers, <= +4) and its "
           "switch-free KiDS (reported; L357 -> L355's P1 projection), re-scored EXACTLY at the two window cells")
    PAT3 = os.path.join(REPO, "real_research", "acceleration_trigger_2026", "AT3_acceleration_trigger_full_gates.py")
    os.environ["AT3_THREADS"] = "2"; os.environ["FAST"] = "0"
    ns = exec_slices(PAT3, [(None, "# ================================================================================================ C1 control")], name="at3_head")[0]
    L57, N60 = ns["L57"], ns["N60"]
    M200_KIDS, c200_55, RHOC_ZL, ZL, LOGMS = ns["M200_KIDS"], ns["c200_55"], ns["RHOC_ZL"], ns["ZL"], ns["LOGMS"]
    nfw21, hernquist, retained_acc, KPC_M, FBa = ns["nfw21"], ns["hernquist"], ns["retained_acc"], ns["KPC_M"], ns["FB"]
    rr55, Rd55, Rp55, MPC55, MS55 = ns["rr55"], ns["Rd55"], ns["Rp55"], ns["MPCm"], ns["MS"]
    PAIRS = ((0.1, 600.0), (0.03, 600.0))                                                 # AT3's window cells (W1: window_except_shear)
    FUS = (0.0, 0.15, 0.25)
    jobs = [(yv0, va, b) for yv0, va in PAIRS for b in range(4)]

    def job(j):
        yv0, va, b = j
        M200 = M200_KIDS[b]; c = float(c200_55(M200)); Mn, r200, rs = nfw21(M200, c, RHOC_ZL)
        pro = np.geomspace(0.02 * rs, 0.999 * r200, 40)
        Mb_fn = hernquist(1.3 * 10 ** LOGMS[b], 3.0); rv = ns["r_v_profile"](Mb_fn, ns["yv_eff"](yv0, ZL))
        ratio_p, _ = retained_acc(Mb_fn, M200, c, list(pro), rv, va, RHOC_ZL, N=8000)      # AT3 a_retention's KiDS loop, verbatim
        return j, (pro, np.asarray(ratio_p))
    from concurrent.futures import ThreadPoolExecutor
    with lane_env():
        with ThreadPoolExecutor(2) as ex:
            PR = dict(ex.map(job, jobs))
    P(f"    retention profiles of the 4 KiDS hosts at the window cells {PAIRS} recomputed with AT3's own functions (N = 8000)   {el()}")

    def kidsT(pair, esd):
        T = []
        for b in range(4):
            pro, ratio_p = PR[(pair[0], pair[1], b)]
            M200 = M200_KIDS[b]; c = float(c200_55(M200)); Mn, r200, rs = nfw21(M200, c, RHOC_ZL)
            r_kpc = rr55 / KPC_M
            Mc = (1 - FBa) * Mn(np.minimum(r_kpc, r200)) * np.interp(np.log(r_kpc), np.log(pro), ratio_p)
            T.append(np.interp(Rd55[b], Rp55 / MPC55, esd(Mc * MS55 + 1.0, 1.0)))
        return T
    # the committed rows (AT3's .out), for the control
    t_ = open(PAT3.replace(".py", ".out")).read()
    COM = {}
    for yv0, va, fu, a, b, c3, d in re.findall(r"y_v0 ([\d.]+) \(q [\d.]+\) v_A +(\d+) f_U ([\d.]+): .*?KiDS \(p1_x2\.5\) ([+-][\d.]+)/([+-][\d.]+) \(switch-free ([+-][\d.]+)/([+-][\d.]+)\)", t_):
        COM[(float(yv0), float(va), float(fu))] = (float(a), float(b), float(c3), float(d))
    base60_bug = dict(ns["BASE60"])
    L55fix = None
    if not MUTATE:
        mL = "LYT = np.linspace(-9.5, 6.5, 1601); YT = 10**LYT"
        L55fix = exec_slices(P55, [(None, mL), (mL, "# ============================================================================================ K1 control")],
                             hooks={0: lambda n: n.__setitem__("esd_of_M", FIX1)}, name="l355_fixed_head")[0]
    res = {}
    for tag in ("before", "after"):
        fixed = tag == "after" and not MUTATE
        L52n = N60["L52"]; orig_m2, orig_pm2 = L52n["model_M2"], N60["project_M2"]
        saved57 = (L57["L55"], L57["fit55"], L57["REF55"])
        try:
            if fixed:
                L52n["model_M2"] = model_M2_factory(L52n, True); L52n["_PROF"].clear(); L52n["_ESD"].clear()
                N60["project_M2"] = FIX2
                ns["BASE60"] = {f: ns["fit_model60"](ns["A052"][f], 0.0, "none", True)[0] for f in FOOTS}
                L57["L55"], L57["fit55"] = L55fix, L55fix["fit"]
                L57["REF55"] = {f: L55fix["fit"](f, L57["W0"], 0.0, False)[0] for f in FOOTS}
            for pair in PAIRS:
                T = kidsT(pair, FIX1 if fixed else L57["esd_of_M"])
                profs = [PR[(pair[0], pair[1], b)] for b in range(4)]
                for fu in FUS:
                    fzl = ns["fU_of_z"](fu, ZL)
                    with lane_env():
                        ksw = ns["kids_switched"](profs, 1 - fzl)
                        ks = L57["kids_score"]([t * (1 - fzl) for t in T])
                    res[(tag, pair, fu)] = (ksw["canonical"], ksw["alt"], ks[("web-blind kernel", "canonical")]["dchi2"], ks[("web-blind kernel", "alt")]["dchi2"])
            if fixed:
                res[("base", tag)] = dict(ns["BASE60"])
        finally:
            L52n["model_M2"], N60["project_M2"] = orig_m2, orig_pm2; L52n["_PROF"].clear(); L52n["_ESD"].clear()
            ns["BASE60"] = base60_bug
            L57["L55"], L57["fit55"], L57["REF55"] = saved57
    dctl = max(abs(res[("before", pair, fu)][i] - COM[(pair[0], pair[1], fu)][i]) for pair in PAIRS for fu in FUS for i in range(4))
    P(f"    control: the committed AT3 rows reproduced with the committed projections to {dctl:.2f} (the .out prints 0.1)")
    for pair in PAIRS:
        for fu in FUS:
            b_, a_ = res[("before", pair, fu)], res[("after", pair, fu)]
            for i, f in enumerate(FOOTS):
                row("AT3", f"GATE y_v0 {pair[0]} v_A {pair[1]:.0f} f_U {fu}: switched KiDS (<= +4)", f, b_[i], a_[i], 4.0)
            for i, f in enumerate(FOOTS):
                row("AT3", f"switch-free y_v0 {pair[0]} v_A {pair[1]:.0f} f_U {fu} (reported, <= +9)", f, b_[2 + i], a_[2 + i], 9.0)
    shifts3 = [res[("after", p_, fu)][i] - res[("before", p_, fu)][i] for p_ in PAIRS for fu in FUS for i in (0, 1)]
    sh_nc = OUT["numbers"].get("R9_P2", {}).get("no_carrier_shift", {f: float("nan") for f in FOOTS})
    fp10 = lane_json(os.path.join(HERE, "FP10_internal_splitting_dark_sector_FULL_results.json"))["numbers"]["B4"]
    for v_ in fp10:
        for f in FOOTS:
            row("FP10", f"B4 v_k {v_} in place (halos converted whole): + the no-carrier shift (ESTIMATE)", f, fp10[v_]["inplace"][f],
                fp10[v_]["inplace"][f] + sh_nc[f], 4.0)
    fp4 = lane_json(os.path.join(HERE, "FP4_kick_from_action_results.json"))["numbers"]["C4"]["dchi2"]
    for f in FOOTS:
        row("FP4", "C4 (reported) kept halos: + the largest shift of AT3's retained carriers (ESTIMATE)", f, fp4[f], fp4[f] + max(shifts3), 4.0)
    P(f"    the corrected projection moves AT3's retained-carrier gate by {min(shifts3):+.2f}..{max(shifts3):+.2f}; used as the ESTIMATE for FP4 C4 "
      f"(kept halos) and, with no carrier ({sh_nc['canonical']:+.2f}/{sh_nc['alt']:+.2f}), for FP10 B4 (halos converted whole)")
    win_b = [(p_, 0.25) for p_ in PAIRS if all(v <= 4.0 for v in res[("before", p_, 0.25)][:2])]
    win_a = [(p_, 0.25) for p_ in PAIRS if all(v <= 4.0 for v in res[("after", p_, 0.25)][:2])]
    FLIPS["AT3"] = [] if len(win_a) == len(win_b) else [dict(id="W1", before="PASS" if win_b else "FAIL", after="PASS" if win_a else "FAIL",
                                                            load_bearing=True, name=f"W1 window cells passing the KiDS gate: {win_b} -> {win_a}")]
    P(f"    AT3's window (the cells that pass every gate but shear) keeps its KiDS pass at: {win_a or 'NO cell'} (committed: {win_b})")
    OUT["numbers"]["R11_AT3"] = dict(control_max_dev=dctl, shift_range=[min(shifts3), max(shifts3)], rows={f"{k_[0]}|{k_[1][0]}|{k_[1][1]}|{k_[2]}": v for k_, v in res.items() if k_[0] != "base"},
                                     window=[[list(map(str, w)) for w in win_b], [list(map(str, w)) for w in win_a]], flips=FLIPS["AT3"])
    for ln in ("AT3", "FP10", "FP4"):
        show_rows(ln)
    P(f"    {el()}")
    return dict(dctl=dctl)


R11 = guard("AT3", r11_at3) if want("R11") else None

# ================================================================================================= R10  the table and the flips
banner("R10  THE BEFORE -> AFTER TABLE (every re-scored KiDS number; each lane's own gate) AND THE VERDICT FLIPS")
flip_rows = [r_ for r_ in TABLE if "FLIP" in r_["verdict"]]
P(f"    {len(TABLE)} rows re-scored; {len(flip_rows)} cross their lane's gate:")
for r_ in flip_rows:
    P(f"      {r_['lane']:5s} {r_['item'][:80]:80s} {r_['foot'][:9]:9s} {r_['before']:+9.2f} -> {r_['after']:+9.2f}  {r_['verdict']}")
P("    the lanes' OWN checks that change verdict when their committed code is re-run with the corrected projection:")
CONTROL_IDS = {"FP6": {"K2"}, "FP9": {"K1"}, "FP14": {"K5"}, "FP17": {"K1"}, "FP1 E": {"E0"}, "L355": {"K1"}, "L360": {"M0"}}
for lane, fl in FLIPS.items():
    for f_ in fl:
        kind = "control pinned to a committed (buggy) number" if f_["id"] in CONTROL_IDS.get(lane, set()) else "VERDICT"
        P(f"      {lane:6s} {f_['id']:10s} {f_['before']} -> {f_['after']}  [{kind}{'' if f_['load_bearing'] else ', reported'}]  {f_['name'][:110]}")
OUT["numbers"]["R10_table"] = TABLE
OUT["numbers"]["R10_flips"] = FLIPS
n_ver = sum(1 for lane, fl in FLIPS.items() for f_ in fl if f_["id"] not in CONTROL_IDS.get(lane, set()))
if MUTATE:
    same = all(abs(r_["after"] - r_["before"]) < 1e-6 or not (math.isfinite(r_["after"]) and math.isfinite(r_["before"])) for r_ in TABLE
               if r_["lane"] not in ("FP1E", "FP14", "FP17", "AT3", "FP10", "FP4"))
    P(f"    MUTATE control: with the committed projection everywhere the re-scores reproduce the committed numbers: {same}")
check("R10 (reported) THE FLIP TABLE: every committed KiDS number of the chain in scope re-scored with the corrected projection (FP6, FP9, "
      "FP11, FP12, FP13, FP1 E, FP14, FP17) plus the record's L355 and the P2 family's cells (L352, L360, DE8 C1; AT3/FP4/FP10 bounded); "
      "gate crossings and the lanes' own check flips listed above",
      f"{len(TABLE)} rows; {len(flip_rows)} gate crossings; {n_ver} of the lanes' own verdict checks flip (controls pinned to committed numbers excluded)",
      True, load_bearing=False)

# ================================================================================================= F  completeness
nonfinite = [(r_["lane"], r_["item"]) for r_ in TABLE if not math.isfinite(r_["after"]) and "NOT re-scored" not in r_["item"] and "R0 at the KiDS floor" not in r_["item"]
             and "at L_LG" not in r_["item"]]
check("F EVERY RE-SCORE COMPLETED: no lane's re-run raised, and every re-scored number is finite (FP6 B6's interpolations outside their "
      "tabulated range are the stated exception)",
      f"errors: {FAILS or 'none'}; non-finite: {nonfinite[:6] or 'none'}", not FAILS and not nonfinite and len(TABLE) > 0)


# ================================================================================================= H  who uses the two projections
banner("H  THE HUB'S LANES (XR*.py) AND THE CHAIN'S OTHER LANES THAT USE EITHER PROJECTION (a scan of the committed sources; not re-scored here)")
P1_SRC = ("FP6_gate_survey", "FP9_web_galaxy_separator", "FP13_separator_from_state", "FP1_static_sector", "FP11_local_group_flyby", "FP12_local_volume_groups_r0",
          "L355_kernel_invisible_kids", "L357_virialization", "AT1_acceleration_trigger", "AT3_acceleration_trigger", "BS2_efe_vs_switch", "L341_chk_frw_gate")
P1_CALL = ("esd_of_M", "kids_class", "kids_chi2", "kids_isolated", "kids_score", "gates(", "kfit(")
P2_CALL = ("project_M2", "annulus_esd", "esd_from_mlens", "model_esd", "esd_bin", "fit_model", "fit_cell", "fit_comb", "kids_switched")
AFFECTED_JSON = ("FP1_static_sector_results", "FP6_gate_survey_results", "FP9_web_galaxy_separator_results", "FP13_separator_from_state_results",
                 "FP11_local_group_flyby_results", "FP12_local_volume_groups_r0_results", "L355_kernel_invisible_kids_results", "L361_bound_region_kernel_results",
                 "L360_assembled_construction_kids_results", "DE8_kids_sigma_axis_both_branches_results", "DE10_kids_converged_model_results",
                 "AT3_acceleration_trigger_full_gates_results", "XR9_", "XR14_")


def scan(paths):
    out = {}
    for pth in paths:
        try:
            src = open(pth).read()
        except OSError:
            continue
        lines = src.split("\n")
        first = lambda tok: next((i + 1 for i, l_ in enumerate(lines) if tok in l_ and not l_.lstrip().startswith("#")), None)
        p1 = [t for t in P1_CALL if first(t)]
        p2 = [t for t in P2_CALL if first(t)]
        srcs = [t for t in P1_SRC if first(t)]
        js = [t for t in AFFECTED_JSON if first(t)]
        kid = bool(re.search(r"kids|KiDS|KIDS", src))
        cls = []
        if p1 and (srcs or "esd_of_M" in p1):
            cls.append("P1 (computes with FP6/FP1/L355's esd_of_M)")
        if p2:
            cls.append("P2 (computes with L352's project_M2 / DE8's esd_from_mlens)")
        if js and kid:
            cls.append("reads committed KiDS numbers of an affected lane")
        if cls:
            out[os.path.relpath(pth, REPO)] = dict(classes=cls, calls={t: first(t) for t in p1 + p2}, loads=srcs, json=js)
    return out


HUB = scan(sorted(glob.glob(os.path.join(REPO, "real_research", "cross_thread_review_2026_09_26", "XR*.py"))))
CHAIN = scan(sorted(p_ for p_ in glob.glob(os.path.join(HERE, "FP*.py")) if not os.path.basename(p_).startswith("FP20")))
for lab, d in (("hub (cross_thread_review_2026_09_26)", HUB), ("chain (derivation_chain_2026)", CHAIN)):
    P(f"    -- {lab}: {len(d)} files")
    for f_, v in d.items():
        P(f"       {os.path.basename(f_):44s} {'; '.join(v['classes'])}  [" + ", ".join(f"{k_}:{ln}" for k_, ln in list(v["calls"].items())[:5])
          + (f"; json: {', '.join(v['json'][:3])}" if v["json"] else "") + "]")
OUT["numbers"]["H_scan"] = dict(hub=HUB, chain=CHAIN)
check("H (reported) THE HUB'S LANES ARE NOT FREE OF IT: the scan lists every XR lane that computes KiDS with either projection (directly or "
      "through a lane's exec'd machinery) or reads an affected lane's committed KiDS numbers; the P2 users compute carrier templates, where "
      "the P2 error is largest (V1b); the hub re-scores them",
      "; ".join(f"{os.path.basename(k_)}: {'/'.join(c.split(' ')[0] for c in v['classes'])}" for k_, v in HUB.items()), True, load_bearing=False)


# ================================================================================================= W  the ledger
def tb(lane, prefix, foot):
    for r_ in TABLE:
        if r_["lane"] == lane and r_["item"].startswith(prefix) and r_["foot"] == foot:
            return r_["before"], r_["after"]
    return float("nan"), float("nan")


def fmt2(lane, prefix, d=1):
    (b1, a1), (b2, a2) = tb(lane, prefix, "canonical"), tb(lane, prefix, "alt")
    return f"{b1:+.{d}f}/{b2:+.{d}f} -> {a1:+.{d}f}/{a2:+.{d}f}"


def fmt_cells(cells):
    return ", ".join("|".join(f"{float(x):g}" for x in c_[0].strip("()").split(", ")) + f"|{c_[1]}" for c_ in cells) or "none"


banner("W  THE LEDGER: what this lane settles (both footings; 'corrected by FP20' marks a committed claim re-scored here)")
at3w = OUT["numbers"].get("R11_AT3", {}).get("window", [[], []])
l360p = OUT["numbers"].get("R9_P2", {}).get("L360_pairs", [float("nan")] * 3)
l360s = OUT["numbers"].get("R9_P2", {}).get("L360_shift") or [float("nan")] * 2
at3s = OUT["numbers"].get("R11_AT3", {}).get("shift_range", [float("nan")] * 2)
win13 = OUT["numbers"].get("R3_FP13", {}).get("windows", {})
LEDGER = [
    ("F20a", "the correct KiDS projection: Delta Sigma(R) = M_2D(<R)/(pi R^2) - Sigma(R) with exact uniform-shell kernels (the 1/sqrt end point "
             "integrated analytically, the inner projected mass carried exactly, the mass inside the first node kept); it reproduces the SIS, NFW "
             "(Wright & Brainerd 2000), a point mass and the P2 lanes' cored/hollow carrier templates to < 0.1% (< 0.2% where the input has jumps)",
     "DERIVED", "V1, V1b"),
    ("F20b", "the record's P1 projection (FP6 esd_of_M = FP1 E's [FP14/FP17] = L355's [L357/AT1/AT3] = BS2's) is accurate", "FAILS",
     "corrected by FP20: -59% at 35 kpc on the SIS, -3..-14% at 0.3-2.6 Mpc; defect A (inner disc pi R_0^2 Sig(R_0), R_0 = 20 kpc) + defect B "
     "(trapezoid over the 1/sqrt end point); no truncation defect (V2, B1)"),
    ("F20c", "L352's P2 projection (L352/L359/L360, AT3's gate, FP4/FP10/FP15/FP16 via kids_switched, DE8/DE10, XR9/XR14) is accurate", "FAILS",
     "corrected by FP20: -3% (SIS) to +11% (NFW) on halos, up to +187% / -123% at 35 kpc on cored / hollowed carrier templates (V4, V1b)"),
    ("F20d", f"FP6's (H) headline passes KiDS (<= +9): d chi^2 {fmt2('FP6', 'H2 the (H) HEADLINE')}", "DERIVED",
     "corrected by FP20 (R1: FP6 re-run whole; its only check that flips is K2, the control pinned to L341 F7's buggy 118.0)"),
    ("F20e", f"FP9's (H_Y) headline at z = 0.25 passes KiDS: {fmt2('FP9', 'H2 the (H_Y) HEADLINE')} (inherited by FP11 K7/G1, FP12 K7)", "DERIVED",
     "corrected by FP20 (R2: FP9 re-run whole; its window stays 28/48; only the K1 control flips)"),
    ("F20f", f"FP13's H_S passes KiDS at z = 0.25 ({fmt2('FP13', 'H1 the H_S HEADLINE: KiDS d chi^2 at z = 0.25')}) and 0.4 "
             f"({fmt2('FP13', 'H1 the H_S HEADLINE: KiDS d chi^2 at z = 0.4')})", "DERIVED", "corrected by FP20 (R3; controls reproduce 92 committed numbers)"),
    ("F20g", f"FP9's own (H_Y) at z = 0.4 (FP13 H5): {fmt2('FP13', 'H5/C2 variant ' + chr(39) + 'FP9 H_Y' + chr(39) + ': KiDS at z = 0.4')} -- still FAILS the lens spread",
     "FAILS", "corrected by FP20 (R3)"),
    ("F20h", f"the KiDS floor on the band-pass length: L_KiDS {fmt2('FP9', 'I5 KiDS floor', 2)} Mpc; the KiDS-LG pincer (FP6 B6/H3, FP9 H3, FP11 X1, "
             "FP12 U1: the LG needs L(0.25) ~ 0.5-0.6 Mpc, KiDS costs +250..+300 there) is unchanged", "CONSTRAINT", "corrected by FP20 (R1, R2, R4)"),
    ("F20i", f"FP1 E3's KiDS tolerance on the lenses' external field (2-halo, 1e-4 a0): {fmt2('FP1E', 'E3 KiDS TOLERANCE e (3D rms, 1e-4 a0), 2-halo')}; "
             f"no 2-halo {fmt2('FP1E', 'E3 KiDS TOLERANCE e (3D rms, a0), no 2-halo')} (x1e-4); the LG needs {fmt2('FP11', 'P1 the LG')} times more "
             f"(FP11 P1 holds); the band-edge reading (reported) {fmt2('FP11', 'P1 band-edge', 2)}x crosses 1", "CONSTRAINT", "corrected by FP20 (R6, R5)"),
    ("F20j", "FP13's A3 threshold windows narrow (the other gates as committed): " + "; ".join(
        f"{k_.split('/', 1)[1]}: {win13.get('before/' + k_.split('/', 1)[1], '?')} -> {v}" for k_, v in win13.items() if k_.startswith("after/"))
     + "; delta_c stays inside both nonlinear windows (A3a holds)", "CONSTRAINT", "corrected by FP20 (R3)"),
    ("F20k", f"L355's 'KiDS needs a web-blind kernel': the baryons-only deficit {fmt2('L355', 'K2 baryons-only kernel deficit, linear-theory')} and the "
             f"carrier + 2-halo {fmt2('L355', 'K3 + carrier (f_d(0) = 0.8)')} -- the claim survives, stronger", "CONSTRAINT", "corrected by FP20 (R8)"),
    ("F20l", f"L360's assembled construction: pairs passing KiDS {l360p[0]} -> {l360p[1]} of {l360p[2]} (the carrier templates move d chi^2 by "
             f"{l360s[0]:+.0f}..{l360s[1]:+.0f}); the M2 claim (some pairs pass) survives", "CONSTRAINT", "corrected by FP20 (R9: L360 re-run whole)"),
    ("F20m", f"AT3's KiDS gate at its window cells (switched fit, <= +4): passing cells {fmt_cells(at3w[0])} -> {fmt_cells(at3w[1])} (d chi^2 moves "
             f"{at3s[0]:+.1f}..{at3s[1]:+.1f}); its switch-free KiDS (reported) improves", "FAILS" if (at3w[0] and not at3w[1]) else "CONSTRAINT",
     "corrected by FP20 (R11: AT3's retention profiles recomputed with its own functions; FP4 C4 and FP10 B4 are estimates from these shifts)"),
    ("F20n", "the P2 lanes downstream of DE8 (DE10's converged model, the hub's XR9 and XR14 ON-M* KiDS pass) carry the carrier-template error "
             "(V1b) and must be re-scored with the corrected projection; so must FP15/FP16 (uncommitted, kids_switched)", "OPEN", "V4, V1b, R9, H"),
    ("F20o", f"the isolated-P2 KiDS base itself: P1 lanes {fmt2('FP6', 'B5 isolated P2 chi^2')} (the lead grade flattered the inner phantom); P2 lanes "
             f"(nu_mono, 2-halo) {fmt2('P2', 'L352 unswitched base chi^2 (+2-halo)')} -- every gate here is a difference to its lane's base",
     "CONSTRAINT", "R1, R9"),
    ("F20p", "the P1 lanes score point values at the bin centres, not B21's annulus averages (a ~1-2% convention, unchanged here); "
             "the 2-halo templates keep their own inner-disc approximation (V5)", "OPEN", "scope"),
]
for k_, what, status, why in LEDGER:
    P(f"    {k_:5s} {status:11s} {what}  --  {why}")
OUT["ledger"] = [dict(link=k_, what=w, status=s_, basis=b_) for k_, w, s_, b_ in LEDGER]
check("W (reported) the ledger", f"{len(LEDGER)} links", True, load_bearing=False)

# ================================================================================================= verdict
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
banner("VERDICT")
P(f"""  THE BUG.  FP6's esd_of_M (one function, also FP1 E's -> FP14/FP17 and L355's -> L357/AT1/AT3) loses half the projected mass
  inside 20 kpc for any cuspy profile (defect A: -57% at 35 kpc on the SIS, falling as 20 kpc/R) and integrates the 1/sqrt end point
  of the Abel integral with a trapezoid that skips [R, r_1] (defect B: -2..-14%, grid-aligned, -12% at 2.6 Mpc).  There is no
  truncation defect.  L352's project_M2 (the P2 family) shares B and replaces A by 2 pi R_0^2 Sig(R_0), exact only for Sigma ~ 1/R:
  -3% on the SIS, +11% on NFW halos, up to +187% / -123% on the cored or hollowed carrier templates.  The corrected projection
  matches every analytic profile to < 0.1%.
  THE RE-SCORE.  The chain's KiDS verdicts that decide its status do not flip: FP6 (H), FP9 (H_Y) and FP13 (H_S at z = 0.25 and
  0.4) still pass within +9, FP9's H_Y still fails at z = 0.4, the KiDS floor on L(0.25) and the KiDS-LG pincer are unchanged, FP1's
  field tolerances tighten by 10-30% and the LG still needs ~8x more field than KiDS allows.  What moves: FP13's threshold windows narrow at
  their edges, FP11 P1's band-edge reading crosses 1, L355's 'web-blind kernel' deficit grows, and -- in the P2 family -- the
  carrier templates: L360's passing pairs go {l360p[0]} -> {l360p[1]} of {l360p[2]}; AT3's window cells keep their KiDS pass
  ({fmt_cells(at3w[1])}; d chi^2 moves {at3s[0]:+.1f}..{at3s[1]:+.1f}).  The isolated-P2 base chi^2 of the P1 lanes rises by
  ~+29 (the lead grade flattered the inner phantom).  The hub's P2 users (DE10, XR9, XR14, XR28, XR29) carry the carrier-template error and must be re-scored.
  Not 'closed'.  Time {time.time() - T0:.0f} s.""")
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), n_fail, time.time() - T0
fn = os.path.join(HERE, f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json")
with builtins.open(fn, "w") as fh:
    json.dump(jclean(OUT), fh, indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {os.path.basename(fn)}")
sys.exit(0 if n_fail == 0 else 1)
