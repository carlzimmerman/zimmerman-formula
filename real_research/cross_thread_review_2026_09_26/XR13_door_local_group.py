#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR13_door_local_group.py -- THE PER-OBJECT DOOR, part 2 of 3: the Local Group's zero-velocity radius R_0 with the Milky Way
and M31 as two partitioned MOND regions (not one merged point mass), and the Milky Way--M31 timing (hunt item 13) under
the same partition.  Independent cross-thread review (2026-09-26/27).  Read-only on every committed file: XR6's LG
definitions are loaded exactly as XR9 loaded them (main never run); XR9's kappa-form edge function is copied verbatim; the
merged shell model is XR4/XR6/XR9's and its committed numbers are the controls.

THE DOOR (XR13_door_environment.py has the full statement).  The Milky Way and M31 are each their own MOND region, cut at
the watershed of the MOND-sector density; neither reads the other's baryons in its kernel.

THE MODEL (the task's specification, reading 'T').  XR4/k02's point-mass + Lambda shell model generalised to two
partitioned regions, axisymmetric: a Hubble-flow tracer on a fixed ray at angle theta from the MW->M31 axis (origin at the
baryonic barycentre) moves radially under the MOND phantom of the ONE galaxy whose watershed basin it is in (inside that
galaxy's own kappa-form switch edge, XR6's 2% tanh edge), both galaxies' Newtonian baryons and carriers (M_d = 5.36 M_b x
retained(z), XR4's histories none/decay/full), and Lambda.
   * The watershed of two isolated deep-MOND MOND-sector densities (rho = A_i/r_i^2, A_i ~ sqrt(M_i)) is scale-free: it is
     computed once in units of the separation d (descent flow from the saddle) and checked against direct gradient ascent.
   * The pair's separation d(t) is prescribed: 'kinematic' (the Newtonian radial timing orbit ending at 0.78 Mpc, -110 km/s:
     the observed pair history; timing mass 4.8e12) or 'door-own' (the pair's own orbit under the door).
   * R_0(theta) is found with a root-finder built for two regions (XR6's run_cells can lock onto the chaotic inner crossings of
     tracers that start inside the pair; C2b shows the new one returns XR6's merged numbers): the outermost zero-velocity
     tracer that ends outside the pair (r > 0.6 Mpc), bisected, with a continuity check.  The gated number is the solid-angle
     mean over the 6 of 8 Gauss-Legendre rays with |cos theta| <= 0.9 (90% of the sky; the two rays within 16 deg of the axis
     graze a galaxy early on, where a fixed radial ray is not a valid model); the all-ray mean, median and perpendicular value
     are reported beside it.
   * Masses: M_b(LG) = 1.145e11 and 1.72e11 (XR9's), MW:M31 = 1:2 (KD's and item 13's 6e10 : 1.2e11) and 1:1 (reported).
   * References computed with the same machinery: M* as ONE point (XR9's, the control) and M* as TWO points in one merged region
     (QUMOND on their summed Newtonian field), which separates the partition's effect from the geometry's.
   * The tracers are galaxies too, so under rule (1) each sits in a hole of its host's region; the host's phantom inside a
     small hole is (1 - N) of the unperturbed one (N: 1/3 for a sphere, ~0.15 at the uphill end of a cone-shaped basin, 1 for a
     fully screened tracer).  D_f = 0.85, 2/3, 0 are run (reported).
READING P (reported beside T): L361/L370 build the phantom as the curl-free projection of f V, so a bounded, curved watershed
leaks part of each galaxy's phantom into the other's basin AND makes each region lopsided: the Gauss layer on the cut face
carries negative phantom mass and repels its own galaxy from the partner.  Both are computed (a volume integral of the
dipole kernel, checked by Gauss cancellation) against the region's size r_e/d, and the pair's timing is run with them.
MEASURED: R_0 = 0.96 +- 0.03 Mpc; band |log10(R_0/0.96)| <= 0.10 (XR4's).  Timing: 0.78 Mpc, -110 km/s (item 13's values;
van der Marel+2012: -109.3 +- 4.4 km/s).

CHECKS
  C1 CONTROL: XR9's committed merged R_0 at the cell (p = 1, x_c0 = 2.5, kappa-form numerical edge; 2 footings x 2 M_b x 3
     histories) is reproduced exactly with XR6's run_cells.
  C2 CONTROL: the two-region integrator in merged mode reproduces the same twelve numbers (1e-9): it is XR6's where the door
     is off.   C2b CONTROL: the two-region root-finder returns XR6's merged R_0 in the merged case (1e-6).
  C3 CONTROL: hunt item 13's radial MOND timing is reproduced with its own scheme (h76_h13_h36_h63.py): -223 / -241 km/s.
  W1 the watershed separatrix: the saddle at z_s = 1/(1 + q^(1/3)); 200 random points per mass ratio assigned to the same basin
     as direct gradient ascent.
  C5 CONTROL: the projection integral leaves no field outside an uncut ball (L361's Gauss cancellation, 1%).
  D4 [load-bearing; MUTATE must fail] THE DOOR SPLITS THE LOCAL GROUP: every scored cell's R_0 differs from XR9's merged R_0 by
     more than 2%.
  G4 (reported, pre-declared) (d) FLIPS: the scored R_0 on the model's own 'decay' history lands within +-0.10 dex of 0.96 on
     both footings for some M_b (the task's expectation: only partway, ~+0.13 dex).
  P1 (reported, pre-declared) reading T is the door's most favourable reading for R_0 (reading P's tracer pull >= T's).
  T1 / T1P (reported) THE MW--M31 TIMING UNDER THE DOOR, readings T and P; T2 the same for M*.
MUTATE=1 merges the regions again (the scored R_0 is XR9's merged one): D4 must FAIL (rc = 1).

SCOPE.  Radial motion along fixed rays (tangential forces dropped, as in every shell model); point-mass galaxies; the
watershed from deep-MOND isothermal profiles (exact beyond r_M ~ 10 kpc); the carrier as point masses at the galaxies (XR4's
upper bound on its effect); d(t) prescribed.  Reading P's tables are built at today's separation and scaled with d; its
tracer comparison is at today's geometry only.  A prescribed partition does not conserve momentum (each region's
projected field pushes the pair's centre of mass), which is one face of the door having no action.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR13_door_local_group.py   (MUTATE=1)
"""
import os, sys, json, math, time, io, contextlib, warnings, itertools
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1"); os.environ.setdefault("MKL_NUM_THREADS", "1")
import numpy as np
from scipy.integrate import solve_ivp
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
DOOR = not MUTATE
SLUG = "XR13_door_local_group"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR13 part 2 (the Local Group: R_0 and the timing)", "mutate": MUTATE, "door_in_scored_column": DOOR,
               "checks": {}, "numbers": {}}
V_CAP = 325e3
CELL = (1.0, 2.5)
R0M, BAND = 0.96, 0.10
D_LG, V_LG = 0.78, -110.0                          # item 13's values (h76_h13_h36_h63.py); vdM12: -109.3 +- 4.4 km/s
EV_LG = 4.4
NRAY = 8


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}")
    P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 118); P(t); P("=" * 118)


def load(path, cuts, name):
    """XR9_environment.py's loader, verbatim."""
    ns = {"__name__": name, "__file__": path}
    src = open(path).read().replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False")
    with contextlib.redirect_stdout(io.StringIO()):
        for a_, b_ in cuts:
            chunk = src if a_ is None else src.split(a_)[1]
            chunk = chunk if b_ is None else chunk.split(b_)[0]
            exec(chunk, ns)
    return ns


# ------------------------------------------------------------------ the watershed of two isothermal MOND-sector densities
def separatrix(q, smax=3000.0):
    """MW at z = 0, M31 at z = 1 (units of d), rho = 1/r1^2 + q/r2^2 (q = A_M31/A_MW = sqrt(M_M31/M_MW)).  Descent flow
    from the saddle along its stable manifold (the transverse direction).  Returns (r, phi) about the saddle, z_s."""
    zs = 1.0 / (1.0 + q ** (1 / 3))

    def f(p):
        x, z = p; r1 = x * x + z * z; r2 = x * x + (z - 1) ** 2
        g = np.array([-2 * x / r1 ** 2 - 2 * q * x / r2 ** 2, -2 * z / r1 ** 2 - 2 * q * (z - 1) / r2 ** 2])
        return -g / np.linalg.norm(g)

    p = np.array([1e-4, zs]); pts = [p.copy()]; s = 0.0; h = 1e-3
    while s < smax:
        k1 = f(p); k2 = f(p + h / 2 * k1); k3 = f(p + h / 2 * k2); k4 = f(p + h * k3)
        p = p + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4); s += h; pts.append(p.copy())
        h = min(0.02 * max(1.0, math.hypot(p[0], p[1] - zs)), 5.0)
    pts = np.array(pts)
    return np.hypot(pts[:, 0], pts[:, 1] - zs), np.arctan2(pts[:, 0], pts[:, 1] - zs), zs, pts


def ascend(p0, q):
    p = np.array(p0, float)
    for _ in range(400000):
        x, z = p; r1 = x * x + z * z; r2 = x * x + (z - 1) ** 2
        if r1 < 1e-4: return 0
        if r2 < 1e-4: return 1
        g = np.array([-2 * x / r1 ** 2 - 2 * q * x / r2 ** 2, -2 * z / r1 ** 2 - 2 * q * (z - 1) / r2 ** 2])
        p = p + max(0.002 * min(math.sqrt(r1), math.sqrt(r2), 1.0), 1e-4) * (1 + 0.02 * math.sqrt(min(r1, r2))) * g / np.linalg.norm(g)
    return -1


def proj_field(target, zc, Mi, Re, basin_fn, a0, inside=False, at_centre=False, nr=150, nth=150, nph=40, rmin=1e-3):
    """L361/L370's phantom field of ONE partitioned region at a target point: the curl-free projection of f V, V the galaxy's
    own (untruncated, spherical) phantom acceleration, f the region = ball(zc, Re) cut by basin_fn(rho, z) (lengths in Mpc,
    axisymmetric about the z axis; target = (rho_t, z_t)).  For a target OUTSIDE the region: g = int_region [V/|u|^3 -
    3 u (u.V)/|u|^5]/(4 pi) dV' (the region acts as a body polarised by V; u = target - x').  For a target INSIDE the region
    (inside=True): g = V(target) - the same integral over ball minus region (the exterior of the ball adds nothing inside it,
    by spherical symmetry).  at_centre=True: the region's field at its own galaxy's centre (the full ball gives zero there by
    symmetry, so g = - the integral over ball minus region): the self-force of a lopsided region.  Returns (g_rho, g_z)."""
    Gs, Ms, Mp = 6.674e-11, 1.989e30, 3.0857e22
    nuR = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-12))))
    re_ = np.geomspace(rmin, Re, nr + 1); rm = np.sqrt(re_[1:] * re_[:-1]); dr = np.diff(re_)
    ce = np.linspace(-1, 1, nth + 1); cm = 0.5 * (ce[1:] + ce[:-1]); dc = np.diff(ce)
    ph = (np.arange(nph) + 0.5) * 2 * math.pi / nph; dph = 2 * math.pi / nph
    rt, zt = target; g = np.zeros(2)
    for i in range(nr):
        r = rm[i]; st = np.sqrt(1 - cm ** 2); rho_p = r * st; z_p = zc + r * cm
        inb = basin_fn(rho_p, z_p)
        use = ~inb if (inside or at_centre) else inb
        if not use.any(): continue
        gN = Gs * Mi * Ms / (r * Mp) ** 2; Vm = (nuR(gN / a0) - 1.0) * gN
        xp = rho_p[:, None] * np.cos(ph)[None, :]; yp = rho_p[:, None] * np.sin(ph)[None, :]; zp = np.broadcast_to(z_p[:, None], xp.shape)
        Vx = -Vm * xp / r; Vy = -Vm * yp / r; Vz = -Vm * (zp - zc) / r
        ux = rt - xp; uy = -yp; uz = zt - zp; u = np.sqrt(ux ** 2 + uy ** 2 + uz ** 2)
        uV = ux * Vx + uy * Vy + uz * Vz
        w = (r ** 2 * dr[i]) * (dc[:, None] * dph) * use[:, None]
        g += np.array([np.sum((Vx / u ** 3 - 3 * ux * uV / u ** 5) * w), np.sum((Vz / u ** 3 - 3 * uz * uV / u ** 5) * w)]) / (4 * math.pi)
    if at_centre:
        return -g
    if inside:
        rr = math.hypot(rt, zt - zc); gN = Gs * Mi * Ms / (rr * Mp) ** 2; Vm = (nuR(gN / a0) - 1.0) * gN
        g = np.array([-Vm * rt / rr, -Vm * (zt - zc) / rr]) - g
    return g


if __name__ == "__main__":
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE: P("\n  *** MUTATE=1: the Milky Way and M31 are merged into one region again; D4 must FAIL ***")
    MK = "# ============================================================================================ "
    LG = load(os.path.join(HERE, "XR6_lg_zero_velocity_mond_sector.py"), [(None, MK + "C1 / C2 controls")], "xr6lg")
    XR9 = json.load(open(os.path.join(HERE, "XR9_environment_results.json")))["numbers"]["LG"]["p1_x2.5"]
    G, Mpc, Msun, H0, OM_M, OM_L, FB = (LG[k_] for k_ in ("G", "Mpc", "Msun", "H0", "OM_M", "OM_L", "FB"))
    A0L6, LNA_TAB, run_cells, dnu_mono, nuL, retained = LG["A0"], LG["LNA_TAB"], LG["run_cells"], LG["dnu_mono"], LG["nu"], LG["retained"]
    RATIO_D = LG["RATIO_D"]
    P(f"  XR6's LG definitions loaded (main not run)   [{time.time() - T0:.0f}s]")
    MB_LG = 1.145e11; MBS = (MB_LG, 1.5 * MB_LG); HISTS = ("none", "decay", "full")
    SPLITS = {"1:2": 1.0 / 3.0, "1:1": 0.5}                         # the Milky Way's share of the LG's baryons

    def edge_numeric_k(Mb, a0, z, xc0, p, wfac=1.0):
        """XR9_environment.py's edge_numeric_k, verbatim (MS5's kappa cap)."""
        E2 = OM_M * (1 + z) ** 3 + OM_L; H = H0 * math.sqrt(E2); Omz = OM_M * (1 + z) ** 3 / E2
        r = np.geomspace(1e-5 * Mpc, 40.0 * Mpc, 6000)
        GM = G * Mb * Msun; y = GM / (r ** 2 * a0)
        D = -2.0 * GM ** 2 * dnu_mono(y) / (r ** 5 * a0)
        x = 1.5 * Omz * FB + D / H ** 2
        xc = xc0 * E2 ** p * wfac
        on = (x >= xc) & (r <= V_CAP / (H * math.sqrt(xc)))
        ion = np.where(on)[0]
        if ion.size == 0:
            return 0.0
        i0 = ion[0]; off = np.where(~on[i0:])[0]
        i1 = len(r) - 1 if off.size == 0 else i0 + off[0]
        return math.sqrt(r[i1 - 1] * r[i1])

    def table_k(Mb, a0, xc0=CELL[1], p=CELL[0]):
        return np.array([edge_numeric_k(Mb, a0, 1.0 / math.exp(l) - 1.0, xc0, p) for l in LNA_TAB])

    # ============================================================================================ C1 / C2 controls
    banner("C1-C3  CONTROLS: XR9's merged R_0 (XR6's run_cells), the two-region integrator in merged mode, item 13's timing")
    TABM = {(f, Mb): table_k(Mb, A0L6[f]) for f in A0L6 for Mb in MBS}
    ctl = [dict(foot=f, Mb=Mb, a0=A0L6[f], xc0=CELL[1], p=CELL[0], hist=h, edge="ms_num", table=TABM[(f, Mb)])
           for f in A0L6 for Mb in MBS for h in HISTS]
    Rc = run_cells(ctl)
    RMERGED = {f"{c['foot']}/{c['Mb']:.3e}/{c['hist']}": float(v) for c, v in zip(ctl, Rc)}
    d1 = max(abs(RMERGED[k_] / XR9["R0"][k_ + "/ms_num"] - 1) for k_ in RMERGED)
    check("C1 CONTROL: XR9's committed merged R_0 at the cell (kappa-form numerical edge; 2 footings x 2 M_b x 3 histories) is "
          "reproduced exactly with XR6's run_cells", f"max relative difference {d1:.1e}; canonical/1.145e11: none "
          f"{RMERGED['canonical/1.145e+11/none']:.4f}, decay {RMERGED['canonical/1.145e+11/decay']:.4f} Mpc", d1 < 1e-12)

    # ---- the two-region integrator (XR6's integrate generalised; merged mode = one galaxy at the origin)
    N_STEP, A_START = 2000, 0.02
    LN = np.linspace(math.log(A_START), 0.0, N_STEP + 1); HSTEP = LN[1] - LN[0]
    LH = np.concatenate([np.stack([LN[:-1], LN[:-1] + HSTEP / 2], axis=1).ravel(), [0.0]])     # nodes at i and i + 1/2
    ZH = 1.0 / np.exp(LH) - 1.0
    RET = {h: np.array([float(retained(np.array(z_), h)) for z_ in ZH]) for h in HISTS}

    def build(cells):
        """per-cell parameter arrays for integrate2; each cell: foot, a0, Mtot, fMW, hist, mode, theta, Df, dtab (pair
        separation [m] on LNA grid), tabs.  mode 'merged': one galaxy at the barycentre (XR6's model); 'merged2': the two
        galaxies as point masses in ONE merged region (QUMOND on their summed Newtonian field, the LG's edge); 'door': two
        partitioned regions, each with its own edge.  A batch must be one mode."""
        modes = set(c["mode"] for c in cells); assert len(modes) == 1, modes
        mode = modes.pop(); two = mode in ("door", "merged2")
        Pm = dict(mode=mode, a0=np.array([c["a0"] for c in cells])[:, None],
                  M1=np.array([(c["Mtot"] * c["fMW"] if two else c["Mtot"]) * Msun for c in cells])[:, None],
                  M2=np.array([(c["Mtot"] * (1 - c["fMW"]) if two else 0.0) * Msun for c in cells])[:, None],
                  sin=np.array([math.sin(c.get("theta", 0.0)) for c in cells])[:, None],
                  cos=np.array([math.cos(c.get("theta", 0.0)) for c in cells])[:, None],
                  Df=np.array([c.get("Df", 1.0) for c in cells])[:, None])
        Pm["door"] = np.full((len(cells), 1), mode == "door")
        Pm["f31"] = Pm["M2"] / np.maximum(Pm["M1"] + Pm["M2"], 1e-300)
        Pm["fmw"] = Pm["M1"] / np.maximum(Pm["M1"] + Pm["M2"], 1e-300)
        Pm["RE1"] = np.array([np.interp(LH, LNA_TAB, c["tabs"]["MW" if mode == "door" else "merged"]) for c in cells])
        Pm["RE2"] = np.array([np.interp(LH, LNA_TAB, c["tabs"]["M31"]) if mode == "door" else np.full(LH.shape, np.inf) for c in cells])
        Pm["D"] = np.array([np.interp(LH, LNA_TAB, c["dtab"]) if two else np.zeros(LH.shape) for c in cells])
        Pm["RET"] = np.array([RET[c["hist"]] for c in cells])
        Pm["q"] = [c.get("q") for c in cells]
        return Pm

    SEPS = {}

    def basin31(Pm, x_perp, dz1, D):
        """smooth weight of M31's basin at a point (x_perp, dz1 = axial offset from the MW) given the separation D."""
        w = np.zeros_like(x_perp)
        for q_ in set(q for q in Pm["q"] if q is not None):
            rr_, ph_, zs_ = SEPS[q_][:3]
            sel = np.array([q == q_ for q in Pm["q"]])
            dd = np.maximum(D[sel], 1e-30)
            rt, zt = x_perp[sel] / dd, dz1[sel] / dd - zs_
            rp = np.hypot(rt, zt); php = np.arctan2(rt, zt)
            w[sel] = 0.5 * (1.0 + np.tanh((np.interp(rp, rr_, ph_) - php) / 0.01))
        return w

    def integrate2(Pm, ri):
        a0, M1, M2 = Pm["a0"], Pm["M1"], Pm["M2"]
        r = ri.copy()
        u = H0 * math.sqrt(OM_M / A_START ** 3 + OM_L) * r
        dead = np.zeros_like(r, dtype=bool)

        def acc(j, rr):
            l = LH[j]; a = math.exp(l); E2 = OM_M / a ** 3 + OM_L; H = H0 * math.sqrt(E2)
            rr = np.maximum(rr, 1e-6 * Mpc)
            D = Pm["D"][:, j:j + 1]; re1 = Pm["RE1"][:, j:j + 1]; re2 = Pm["RE2"][:, j:j + 1]; rt = Pm["RET"][:, j:j + 1]
            xp = rr * Pm["sin"]; xz = rr * Pm["cos"]
            dz1 = xz + Pm["f31"] * D; r1 = np.sqrt(xp ** 2 + dz1 ** 2); c1 = (xp * Pm["sin"] + dz1 * Pm["cos"]) / r1
            gN1 = G * M1 / r1 ** 2
            with np.errstate(invalid="ignore", over="ignore"):
                w1 = np.where(np.isinf(re1), 1.0, 0.5 * (1.0 - np.tanh((r1 - re1) / (0.02 * np.where(np.isinf(re1), 1.0, np.maximum(re1, 1e-30))))))
            if Pm["mode"] == "door":
                dz2 = xz - Pm["fmw"] * D; r2 = np.sqrt(xp ** 2 + dz2 ** 2); c2 = (xp * Pm["sin"] + dz2 * Pm["cos"]) / np.maximum(r2, 1e-30)
                gN2 = G * M2 / np.maximum(r2, 1e-30) ** 2
                with np.errstate(invalid="ignore", over="ignore"):
                    w2 = 0.5 * (1.0 - np.tanh((r2 - re2) / (0.02 * np.maximum(re2, 1e-30))))
                wb2 = basin31(Pm, xp, dz1, np.broadcast_to(D, xp.shape)); wb1 = 1.0 - wb2
                ph1 = (nuL(gN1 / a0) - 1.0) * gN1 * w1 * wb1 * Pm["Df"]
                ph2 = (nuL(gN2 / a0) - 1.0) * gN2 * w2 * wb2 * Pm["Df"]
                g1 = gN1 + ph1 + G * RATIO_D * rt * M1 / r1 ** 2
                g2 = gN2 + ph2 + G * RATIO_D * rt * M2 / np.maximum(r2, 1e-30) ** 2
                aR = -g1 * c1 - g2 * c2
            elif Pm["mode"] == "merged2":
                dz2 = xz - Pm["fmw"] * D; r2 = np.sqrt(xp ** 2 + dz2 ** 2); r2 = np.maximum(r2, 1e-30)
                gx = -G * M1 * xp / r1 ** 3 - G * M2 * xp / r2 ** 3; gz = -G * M1 * dz1 / r1 ** 3 - G * M2 * dz2 / r2 ** 3
                gmag = np.hypot(gx, gz)
                with np.errstate(invalid="ignore", over="ignore"):
                    wM = np.where(np.isinf(re1), 1.0, 0.5 * (1.0 - np.tanh((rr - re1) / (0.02 * np.where(np.isinf(re1), 1.0, np.maximum(re1, 1e-30))))))
                fac = wM * nuL(gmag / a0) + (1.0 - wM)
                aR = fac * (gx * Pm["sin"] + gz * Pm["cos"]) + RATIO_D * rt * (gx * Pm["sin"] + gz * Pm["cos"])
            else:
                aR = -(w1 * nuL(gN1 / a0) * gN1 + (1 - w1) * gN1 + G * RATIO_D * rt * M1 / rr ** 2)
            return aR + OM_L * H0 ** 2 * rr, H

        for i in range(N_STEP):
            j = 2 * i
            a1, H1 = acc(j, r);                     k1r, k1u = u / H1, a1 / H1
            a2, H2 = acc(j + 1, r + HSTEP * k1r / 2); k2r, k2u = (u + HSTEP * k1u / 2) / H2, a2 / H2
            a3, H3 = acc(j + 1, r + HSTEP * k2r / 2); k3r, k3u = (u + HSTEP * k2u / 2) / H3, a3 / H3
            a4, H4 = acc(j + 2, r + HSTEP * k3r);     k4r, k4u = (u + HSTEP * k3u) / H4, a4 / H4
            r = r + HSTEP * (k1r + 2 * k2r + 2 * k3r + k4r) / 6
            u = u + HSTEP * (k1u + 2 * k2u + 2 * k3u + k4u) / 6
            dead |= r <= 1e-5 * Mpc
            r = np.where(dead, 1e-5 * Mpc, r); u = np.where(dead, -1.0, u)
        return r, u

    def run_cells2(cells, K=24, iters=6):
        """XR6's run_cells (XR4:105-127) on integrate2."""
        Pm = build(cells); nc = len(cells)
        lo = np.full(nc, math.log(0.001 * Mpc)); hi = np.full(nc, math.log(30.0 * Mpc)); ok = np.ones(nc, dtype=bool)
        for _ in range(iters):
            x = lo[:, None] + (hi - lo)[:, None] * np.linspace(0.0, 1.0, K)[None, :]
            r, u = integrate2(Pm, np.exp(x))
            for k in range(nc):
                s = np.sign(u[k]); idx = np.where((s[:-1] < 0) & (s[1:] > 0))[0]
                if len(idx) == 0:
                    ok[k] = False; continue
                j = idx[-1]; lo[k], hi[k] = x[k, j], x[k, j + 1]
        r, u = integrate2(Pm, np.exp(np.stack([lo, hi], axis=1)))
        f = -u[:, 0] / (u[:, 1] - u[:, 0])
        R0 = (r[:, 0] + f * (r[:, 1] - r[:, 0])) / Mpc
        R0[~ok] = np.nan
        R0[(r[:, 0] <= 2e-5 * Mpc) | (np.abs(r[:, 1] / np.maximum(r[:, 0], 1e-30) - 1) > 0.05)] = np.nan
        return R0

    R_PAIR = 0.6                                                          # Mpc: a tracer must end outside the pair today

    def run_cells3(cells, K=160, nbis=40, lo_ri=0.004, hi_ri=0.3):
        """the zero-velocity tracer for two partitioned regions.  XR6's run_cells picks the last u sign change on a 24-point
        grid over 4.5 decades of r_i; with two galaxies the tracers that start inside the pair's early extent have chaotic
        radial histories with many sign changes, and that grid can lock onto an inner one.  Here: a K-point grid over the
        physical range of r_i (a = 0.02), the OUTERMOST - to + crossing whose tracer ends outside the pair today (r > R_PAIR),
        bisected nbis times; the final bracket must be continuous (end radii within 5%) or the ray is NaN."""
        Pm = build(cells); nc = len(cells)
        x = np.linspace(math.log(lo_ri * Mpc), math.log(hi_ri * Mpc), K)[None, :].repeat(nc, 0)
        r, u = integrate2(Pm, np.exp(x))
        lo = np.full(nc, np.nan); hi = np.full(nc, np.nan)
        for k in range(nc):
            s = np.sign(u[k]); idx = np.where((s[:-1] < 0) & (s[1:] > 0) & (r[k, 1:] > R_PAIR * Mpc))[0]
            if len(idx): lo[k], hi[k] = x[k, idx[-1]], x[k, idx[-1] + 1]
        ok = np.isfinite(lo)
        for _ in range(nbis):
            mid = np.where(ok, 0.5 * (lo + hi), math.log(0.05 * Mpc))
            r1, u1 = integrate2(Pm, np.exp(mid)[:, None])
            neg = u1[:, 0] < 0
            lo = np.where(ok & neg, mid, lo); hi = np.where(ok & ~neg, mid, hi)
        r2, u2 = integrate2(Pm, np.exp(np.stack([np.where(ok, lo, 0.0), np.where(ok, hi, 0.0)], axis=1)))
        f = -u2[:, 0] / (u2[:, 1] - u2[:, 0])
        R0 = (r2[:, 0] + f * (r2[:, 1] - r2[:, 0])) / Mpc
        R0[~ok] = np.nan
        R0[np.abs(r2[:, 1] / np.maximum(r2[:, 0], 1e-30) - 1) > 0.05] = np.nan
        return R0

    cm = [dict(foot=f, a0=A0L6[f], Mtot=Mb, fMW=1.0, hist=h, mode="merged", theta=0.0, tabs={"merged": TABM[(f, Mb)]}, dtab=None)
          for f in A0L6 for Mb in MBS for h in HISTS]
    Rm2 = run_cells2(cm)
    d2 = max(abs(v / RMERGED[f"{c['foot']}/{c['Mtot']:.3e}/{c['hist']}"] - 1) for c, v in zip(cm, Rm2))
    check("C2 CONTROL: the two-region integrator in merged mode (one galaxy at the barycentre with the LG's mass and edge) "
          "reproduces XR9's twelve merged R_0 -- where the door is off it is XR6's integrator", f"max relative difference {d2:.1e}",
          d2 < 1e-9)
    Rm3 = run_cells3(cm)
    d2b = max(abs(v / RMERGED[f"{c['foot']}/{c['Mtot']:.3e}/{c['hist']}"] - 1) for c, v in zip(cm, Rm3))
    check("C2b CONTROL: this lane's two-region root-finder (fine grid over the physical r_i range, outermost crossing outside the "
          "pair, bisection, continuity check) returns XR6's merged R_0 in the merged case", f"max relative difference {d2b:.1e}",
          d2b < 1e-6)
    P(f"    [{time.time() - T0:.0f}s]")

    # ---- C3: item 13 with its own scheme (h76_h13_h36_h63.py lines 69-88, reimplemented)
    sys.path.insert(0, os.path.join(REPO, "hunt_2026"))
    from hunt_lib import nu_s, H0 as H0h, OM_L as OM_Lh, G as Gh, Mpc as Mpch, Msun as Msunh, A0 as A0h   # noqa: E402
    t0h = 13.8e9 * 3.156e7

    def h76_timing(M_msun, a0, law="mond", carrier=None, nit=80):
        """item 13's radial two-body integration (h76): from r = 1e19 m at t = 0 with the v0 that puts r(t0) at 0.78 Mpc.
        law 'mond': g = nu(g_N,b/a0) g_N,b (item 13) + the carrier's Newtonian pull; 'newton': g = g_N,b + carrier (the door:
        two separate regions attract as real masses).  carrier = (t grid, retained fraction on it) or None."""
        def rhs(t, y):
            r, v = y; r = max(r, 1e18)
            gN = Gh * M_msun * Msunh / r ** 2
            g = gN * nu_s(gN / a0) if law == "mond" else gN
            if carrier is not None:
                g += RATIO_D * float(np.interp(t, carrier[0], carrier[1])) * gN
            return [v, -g + OM_Lh * H0h ** 2 * r]

        def shoot(v0):
            return solve_ivp(rhs, (0, t0h), [1e19, v0], rtol=1e-9, atol=1e3, dense_output=True, max_step=t0h / 2000)
        lo, hi = 1e3, 3e6
        for _ in range(nit):
            mid = 0.5 * (lo + hi); s = shoot(mid)
            if s.y[0][-1] < D_LG * Mpch: lo = mid
            else: hi = mid
        s = shoot(0.5 * (lo + hi))
        return s.y[0][-1] / Mpch, s.y[1][-1] / 1e3

    T13 = {f: h76_timing(6.0e10 + 1.2e11, A0h[f]) for f in A0h}
    check("C3 CONTROL: hunt item 13's radial MOND timing (M_b = 1.8e11, test-particle MOND, no carrier) is reproduced with its "
          "own scheme: -223 / -241 km/s at 0.78 Mpc", f"canonical {T13['canonical'][1]:+.1f} km/s at {T13['canonical'][0]:.3f} Mpc; "
          f"alt {T13['alt'][1]:+.1f}", abs(T13["canonical"][1] + 223) < 1.0 and abs(T13["alt"][1] + 241) < 1.0)
    P(f"    [{time.time() - T0:.0f}s]")

    # ============================================================================================ W1 the watershed
    banner("W1  THE WATERSHED OF THE MILKY WAY AND M31 (isolated deep-MOND MOND-sector densities, A ~ sqrt(M_b))")
    W1 = {}
    for sp_, fmw in SPLITS.items():
        q = math.sqrt((1 - fmw) / fmw)
        rr_, ph_, zs_, pts = separatrix(q)
        SEPS[q] = (rr_, ph_, zs_)
        rng = np.random.default_rng(7); bad = 0; n = 200
        for _ in range(n):
            P_ = rng.uniform([0.01, -2.5], [3.0, 3.5])
            pred = 1 if math.atan2(P_[0], P_[1] - zs_) < np.interp(math.hypot(P_[0], P_[1] - zs_), rr_, ph_) else 0
            bad += int(pred != ascend(P_, q))
        ang = math.degrees(math.atan2(pts[-1][0], -pts[-1][1]))
        frac_mw = (1 - math.cos(math.radians(ang))) / 2
        W1[sp_] = dict(q=q, z_saddle=zs_, closed_form=1 / (1 + q ** (1 / 3)), mismatches=bad, n=n,
                       mw_basin_halfangle_deg=ang, mw_sky_fraction_far=frac_mw)
        P(f"    MW:M31 = {sp_}: saddle at {zs_:.4f} d from the MW; the MW's basin far away is a cone of half-angle {ang:.1f} deg about "
          f"the -axis ({100 * frac_mw:.0f}% of the sky); basin assignment vs direct ascent: {bad}/{n} mismatches")
    check("W1 the watershed separatrix: the saddle sits at z_s = 1/(1 + q^(1/3)) and the curve assigns 200 random points per mass "
          "ratio to the same basin as direct gradient ascent", "; ".join(f"{k_}: {v_['mismatches']}/{v_['n']} mismatches" for k_, v_ in W1.items()),
          all(v_["mismatches"] == 0 for v_ in W1.values()))
    OUT["numbers"]["watershed"] = W1

    # ============================================================================================ the pair's history d(t)
    banner("THE PAIR'S HISTORY d(t): the kinematic timing orbit (0.78 Mpc, -110 km/s today) and the door's own orbit")

    def pair_orbit(mass_fn, ri_grid, store=False, acc_fn=None):
        """relative orbits on LN (XR4's scheme): Newtonian with mass_fn(z) [Msun], or a general law acc_fn(l, r) -> (acc, H);
        returns r, u at every LN node (store=True) or at the first and last node only."""
        r = ri_grid.copy(); u = H0 * math.sqrt(OM_M / A_START ** 3 + OM_L) * r
        R_ = [r.copy()]; U_ = [u.copy()]; dead = np.zeros_like(r, dtype=bool)

        def acc(l, rr):
            if acc_fn is not None:
                return acc_fn(l, np.maximum(rr, 1e-6 * Mpc))
            a = math.exp(l); H = H0 * math.sqrt(OM_M / a ** 3 + OM_L)
            rr = np.maximum(rr, 1e-6 * Mpc)
            return -G * mass_fn(1.0 / a - 1.0) * Msun / rr ** 2 + OM_L * H0 ** 2 * rr, H
        for i in range(N_STEP):
            l = LN[i]
            a1, H1 = acc(l, r);                  k1r, k1u = u / H1, a1 / H1
            a2, H2 = acc(l + HSTEP / 2, r + HSTEP * k1r / 2); k2r, k2u = (u + HSTEP * k1u / 2) / H2, a2 / H2
            a3, H3 = acc(l + HSTEP / 2, r + HSTEP * k2r / 2); k3r, k3u = (u + HSTEP * k2u / 2) / H3, a3 / H3
            a4, H4 = acc(l + HSTEP, r + HSTEP * k3r);         k4r, k4u = (u + HSTEP * k3u) / H4, a4 / H4
            r = r + HSTEP * (k1r + 2 * k2r + 2 * k3r + k4r) / 6; u = u + HSTEP * (k1u + 2 * k2u + 2 * k3u + k4u) / 6
            dead |= r <= 1e-5 * Mpc; r = np.where(dead, 1e-5 * Mpc, r); u = np.where(dead, -1.0, u)
            if store or i == N_STEP - 1:
                R_.append(r.copy()); U_.append(u.copy())
        return np.array(R_), np.array(U_)

    GRID = np.geomspace(1e-4 * Mpc, 0.2 * Mpc, 300)
    DEAD = 1.0001e-5 * Mpc

    def fit_branch(mass_fn, branch, precise=False, masses=None, acc_fn=None):
        """the initial separation whose orbit is at D_LG today on the given branch.  'recede': the receding orbit through D_LG
        (r_today monotone in r_i).  'approach': bound orbits that turned around and are falling back through D_LG today; they
        occupy the narrow r_i interval between orbits that have already collapsed and orbits still expanding, so the
        collapse boundary is found on the grid and the crossing is bisected inside it.  masses: an array of trial masses
        (Msun, constant in time) evaluated together, returning u_today per mass (used to fit the timing mass)."""
        if masses is not None:
            R_, U_ = pair_orbit(lambda z: np.asarray(masses, float)[:, None], np.tile(GRID, (len(masses), 1)))
            rf, uf = R_[-1], U_[-1]
            lo = np.full(len(masses), np.nan); hi = np.full(len(masses), np.nan)
            for m_ in range(len(masses)):
                dead = rf[m_] <= DEAD
                kk = np.where(dead[:-1] & ~dead[1:])[0]
                if kk.size: lo[m_], hi[m_] = GRID[kk[-1]], GRID[kk[-1] + 1]
            ok = np.isfinite(lo)
            for _ in range(45):
                mid = np.sqrt(np.where(ok, lo * hi, 1.0))
                R1, U1 = pair_orbit(lambda z: np.asarray(masses, float), mid)
                left = (R1[-1] <= DEAD) | ((U1[-1] < 0) & (R1[-1] < D_LG * Mpc))
                lo = np.where(ok & left, mid, lo); hi = np.where(ok & ~left, mid, hi)
            R1, U1 = pair_orbit(lambda z: np.asarray(masses, float), np.sqrt(np.where(ok, lo * hi, 1.0)))
            return np.where(ok & (U1[-1] < 0), U1[-1] / 1e3, np.nan), np.where(ok, R1[-1] / Mpc, np.nan)
        R_, U_ = pair_orbit(mass_fn, GRID, acc_fn=acc_fn)
        rf, uf = R_[-1], U_[-1]
        if branch == "recede":                                            # monotone in r_i: dead / falling / receding short of D
            crit = lambda r_, u_: (r_ <= DEAD) | (u_ <= 0) | (r_ < D_LG * Mpc)
        else:                                                             # dead / falling back but not yet down to D
            crit = lambda r_, u_: (r_ <= DEAD) | ((u_ < 0) & (r_ < D_LG * Mpc))
        c = crit(rf, uf)
        kk = np.where(c[:-1] & ~c[1:])[0]
        if kk.size == 0:
            return None
        lo, hi = GRID[kk[0]], GRID[kk[0] + 1]
        for _ in range(45 if precise else 30):
            mid = math.sqrt(lo * hi); R1, U1 = pair_orbit(mass_fn, np.array([mid]), acc_fn=acc_fn)
            if bool(crit(R1[-1], U1[-1])[0]): lo = mid
            else: hi = mid
        R2, U2 = pair_orbit(mass_fn, np.array([math.sqrt(lo * hi)]), store=True, acc_fn=acc_fn)
        good = abs(R2[-1, 0] / (D_LG * Mpc) - 1) < 1e-3 and ((U2[-1, 0] > 0) if branch == "recede" else (U2[-1, 0] < 0))
        if not good:
            return None                                                  # this branch does not pass D_LG today
        return dict(ri=math.sqrt(lo * hi), r=R2[:, 0], r_today=float(R2[-1, 0] / Mpc), u_today=float(U2[-1, 0] / 1e3))

    # (P1) kinematic: the Newtonian timing mass that gives -110 km/s at 0.78 Mpc on the first approach
    MG = np.geomspace(1.5e12, 1.5e13, 16)
    u_m, r_m = fit_branch(None, "approach", masses=MG)
    okm = np.isfinite(u_m)
    MG2 = np.geomspace(float(np.exp(np.interp(V_LG, u_m[okm][::-1], np.log(MG[okm])[::-1]))) / 1.15,
                       float(np.exp(np.interp(V_LG, u_m[okm][::-1], np.log(MG[okm])[::-1]))) * 1.15, 16)
    u_m2, _ = fit_branch(None, "approach", masses=MG2)
    ok2 = np.isfinite(u_m2)
    MT = float(np.exp(np.interp(V_LG, u_m2[ok2][::-1], np.log(MG2[ok2])[::-1])))
    KIN = fit_branch(lambda z: MT, "approach", precise=True)
    P(f"    kinematic (P1): the Newtonian timing mass for -110 km/s at 0.78 Mpc (first approach, Lambda, from the Hubble flow at "
      f"a = 0.02) is {MT:.3e} Msun (item 13: 'needs 5e12'); today {KIN['r_today']:.3f} Mpc at {KIN['u_today']:+.1f} km/s; max "
      f"separation {KIN['r'].max() / Mpc:.3f} Mpc   [{time.time() - T0:.0f}s]")
    DT = {"kinematic": np.interp(LNA_TAB, LN, KIN["r"])}
    # (P2) the door's own: Newtonian baryons + carrier (whichever branch passes 0.78 Mpc today)
    OWN = {}
    for Mb in MBS:
        for h in HISTS:
            mf = (lambda z, Mb=Mb, h=h: Mb * (1.0 + RATIO_D * float(retained(np.array(z), h))))
            ap = fit_branch(mf, "approach", precise=(h == "decay"))
            rc = fit_branch(mf, "recede", precise=(h == "decay" and ap is None))
            OWN[f"{Mb:.3e}/{h}"] = dict(approach=None if ap is None else ap["u_today"], recede=None if rc is None else rc["u_today"])
            if h == "decay":
                DT[f"door/{Mb:.3e}"] = np.interp(LNA_TAB, LN, (ap if ap is not None else rc)["r"])
    P("    the door's own pair (Newtonian baryons + carrier) at 0.78 Mpc today: " + "; ".join(
        f"M_b {k_.split('/')[0]} {k_.split('/')[1]}: approach " + (f"{v_['approach']:+.1f}" if v_["approach"] is not None else "none")
        + ", recede " + (f"{v_['recede']:+.1f}" if v_["recede"] is not None else "none") + " km/s" for k_, v_ in OWN.items()))
    OUT["numbers"]["pair_history"] = dict(timing_mass_Msun=MT, kinematic_today=[KIN["r_today"], KIN["u_today"]],
                                          kinematic_max_sep_Mpc=float(KIN["r"].max() / Mpc), door_own_today_kms=OWN)
    P(f"    [{time.time() - T0:.0f}s]")

    # ============================================================================================ R_0 with two regions
    banner(f"(d) R_0 WITH TWO PARTITIONED REGIONS: {NRAY} Gauss-Legendre rays per cell; the primary cells, the split and d(t) "
           "variants, and the tracer-hole variants in one batch")
    xg, wg = np.polynomial.legendre.leggauss(NRAY)                       # nodes in cos(theta)
    THETAS = np.arccos(xg)
    TABG = {}
    for f in A0L6:
        for Mb in MBS:
            for sp_, fmw in SPLITS.items():
                for share in (fmw, 1 - fmw):
                    key = (f, round(Mb * share, 3))
                    if key not in TABG: TABG[key] = table_k(Mb * share, A0L6[f])
    P(f"    {len(TABG)} kappa-form edge tables for the single galaxies   [{time.time() - T0:.0f}s]")

    def door_cells(tag, Df, sp_, dt_, hists):
        fmw = SPLITS[sp_]; q = math.sqrt((1 - fmw) / fmw); cells = []
        for f in A0L6:
            for Mb in MBS:
                dtab = DT["kinematic"] if dt_ == "kinematic" else DT[f"door/{Mb:.3e}"]
                for h in hists:
                    for th in THETAS:
                        cells.append(dict(tag=tag, foot=f, a0=A0L6[f], Mtot=Mb, fMW=fmw, hist=h, mode="door", theta=float(th), Df=Df,
                                          q=q, dtab=dtab, tabs={"MW": TABG[(f, round(Mb * fmw, 3))], "M31": TABG[(f, round(Mb * (1 - fmw), 3))]}))
        return cells

    CD = (door_cells("T/1:2/kinematic", 1.0, "1:2", "kinematic", HISTS)
          + door_cells("T/1:1/kinematic", 1.0, "1:1", "kinematic", ("decay",))
          + door_cells("T/1:2/door-own d(t)", 1.0, "1:2", "door", ("decay",))
          + door_cells("holes D_f=0.85/1:2/kinematic", 0.85, "1:2", "kinematic", ("decay",))
          + door_cells("holes D_f=2/3/1:2/kinematic", 2.0 / 3.0, "1:2", "kinematic", ("decay",))
          + door_cells("screened D_f=0/1:2/kinematic", 0.0, "1:2", "kinematic", ("decay",)))
    R0s = run_cells3(CD)
    CM2 = [dict(c, mode="merged2", tag="M* two points/1:2/kinematic", tabs={"merged": TABM[(c["foot"], c["Mtot"])]})
           for c in CD if c["tag"] == "T/1:2/kinematic"]
    R0m2 = run_cells3(CM2)
    P(f"    {len(CD) + len(CM2)} rays integrated   [{time.time() - T0:.0f}s]")
    VALID = np.abs(xg) <= 0.9                                          # the declared validity cut (90% of the sky)

    def stats(v_):
        v_ = np.array(v_)
        m8 = float(np.sum(wg * v_) / 2.0) if np.all(np.isfinite(v_)) else float("nan")
        vv, ww = v_[VALID], wg[VALID]
        m6 = float(np.sum(ww * vv) / np.sum(ww)) if np.all(np.isfinite(vv)) else float("nan")
        return dict(R0_rays=v_.tolist(), mean=m6, mean_all_rays=m8, median=float(np.nanmedian(v_)),
                    perpendicular=float(np.mean(v_[np.argsort(np.abs(xg))[:2]])), min=float(np.nanmin(v_)), max=float(np.nanmax(v_)),
                    dex=math.log10(m6 / R0M) if np.isfinite(m6) else float("nan"),
                    dex_all_rays=math.log10(m8 / R0M) if np.isfinite(m8) else float("nan"))

    RD = {}
    for c, v in list(zip(CD, R0s)) + list(zip(CM2, R0m2)):
        RD.setdefault(f"{c['tag']}/{c['foot']}/{c['Mtot']:.3e}/{c['hist']}", []).append(float(v))
    RD = {k_: stats(v_) for k_, v_ in RD.items()}
    P("    solid-angle-mean R_0 [Mpc] over the rays with |cos theta| <= 0.9 (90% of the sky; the two rays within 16 deg of the MW-M31")
    P("    axis graze a galaxy early on and are reported, not averaged), dex from 0.96; [all 8 rays | median | perpendicular]; merged M*:")
    for k_, v_ in RD.items():
        parts = k_.split("/"); f, Mb, h = parts[-3], parts[-2], parts[-1]
        mk = f"{f}/{Mb}/{h}"
        P(f"      {'/'.join(parts[:-3]):28s} {f:9s} {Mb} {h:5s}: {v_['mean']:.3f} {v_['dex']:+.3f} dex  [{v_['mean_all_rays']:.3f} | "
          f"{v_['median']:.3f} | {v_['perpendicular']:.3f}]   merged {RMERGED[mk]:.3f} ({math.log10(RMERGED[mk] / R0M):+.3f})")
    OUT["numbers"]["R0_door"] = RD
    OUT["numbers"]["R0_merged"] = RMERGED
    OUT["numbers"]["rays_theta_deg"] = np.degrees(THETAS).tolist()
    OUT["numbers"]["rays_weight"] = wg.tolist()

    # ---- the scored column and the gate (primary: reading T, MW:M31 1:2, kinematic d(t))
    prim = {k_.replace("T/1:2/kinematic/", ""): v_ for k_, v_ in RD.items() if k_.startswith("T/1:2/kinematic/")}
    if DOOR:
        SC = {k_: v_["mean"] for k_, v_ in prim.items()}
    else:
        SC = {k_: RMERGED[k_] for k_ in prim}
    dmin = min(abs(SC[k_] / RMERGED[k_] - 1) for k_ in SC)
    check("D4 THE DOOR SPLITS THE LOCAL GROUP: in the scored configuration every cell's solid-angle-mean R_0 differs from XR9's "
          "merged R_0 by more than 2% -- MUTATE (merged) must fail", f"smallest relative change {dmin:.3f}", dmin > 0.02)
    dex_dec = {k_: math.log10(v_ / R0M) for k_, v_ in SC.items() if k_.endswith("/decay")}
    inb = any(all(abs(dex_dec[f"{f}/{Mb:.3e}/decay"]) <= BAND for f in A0L6) for Mb in MBS)
    alld = [v_["dex"] for k_, v_ in RD.items() if k_.startswith("T/") and v_["dex"] == v_["dex"]]
    m2 = [v_["dex"] for k_, v_ in RD.items() if k_.startswith("M* two points") and v_["dex"] == v_["dex"]]
    check("G4 (reported, pre-declared) (d) FLIPS: the scored solid-angle-mean R_0 on the model's own 'decay' carrier history lands "
          "within +-0.10 dex of 0.96 on both footings for some M_b (MW:M31 = 1:2, kinematic d(t))",
          "decay: " + ", ".join(f"{k_.split('/')[0]}/{float(k_.split('/')[1]):.3e} {v_:+.3f}" for k_, v_ in dex_dec.items())
          + f" dex; every reading-T variant (split, d(t), histories) {min(alld):+.3f} to {max(alld):+.3f}; M* as two points in one "
          f"region {min(m2):+.3f} to {max(m2):+.3f}; merged M* (one point) "
          f"{min(math.log10(v_ / R0M) for v_ in RMERGED.values()):+.3f} to {max(math.log10(v_ / R0M) for v_ in RMERGED.values()):+.3f}",
          inb, load_bearing=False)

    # ============================================================================================ reading P
    banner("P  THE PARTITION AS L361/L370 BUILD IT: each region's phantom is the curl-free projection of f V, so a bounded, curved "
           "watershed leaks part of each galaxy's phantom into the other's basin and makes each region lopsided (reading T sets both "
           "to zero)")
    fmw_ = SPLITS["1:2"]; q12 = math.sqrt((1 - fmw_) / fmw_); rrS, phS, zsS = SEPS[q12]

    def in31(rho, z, d_=D_LG):                                           # z measured from the MW [Mpc]
        rt_, zt_ = rho / d_, z / d_ - zsS
        return np.arctan2(rt_, zt_) < np.interp(np.hypot(rt_, zt_), rrS, phS)
    inMW = lambda rho, z: ~in31(rho, z)
    Vph = lambda M, r_mpc, a0: float((nuL(G * M * Msun / (r_mpc * Mpc) ** 2 / a0) - 1.0) * G * M * Msun / (r_mpc * Mpc) ** 2)
    Mmw0, M310 = MB_LG * fmw_, MB_LG * (1 - fmw_)
    gau = []
    for t_ in ((0.0, 1.6), (1.1, 1.0), (1.5, 0.0)):
        gg = proj_field(t_, 0.0, Mmw0, 1.3, lambda rho, z: np.ones_like(rho, bool), A0L6["canonical"])
        gau.append(float(np.hypot(*gg) / Vph(Mmw0, math.hypot(*t_), A0L6["canonical"])))
    check("C5 CONTROL (the projection integral): a region that is a full ball (no watershed cut) leaves no phantom field outside "
          "itself -- L361's Gauss cancellation -- at three outside points, to 1% of the uncut phantom there",
          f"|g|/V = {max(gau):.1e} (worst of three)", max(gau) < 0.01)
    RHO = np.array([0.3, 0.45, 0.5, 0.6, 0.8, 1.0, 1.25, 1.6, 2.0, 2.5, 3.2, 4.5, 6.0])
    a0c = A0L6["canonical"]
    L1 = np.array([proj_field((0.0, D_LG), 0.0, Mmw0, rh * D_LG, inMW, a0c)[1] for rh in RHO]) / Vph(Mmw0, D_LG, a0c)
    S1 = np.array([proj_field((0.0, 0.0), 0.0, Mmw0, rh * D_LG, inMW, a0c, at_centre=True)[1] for rh in RHO]) / Vph(Mmw0, D_LG, a0c)
    L2 = np.array([proj_field((0.0, 0.0), D_LG, M310, rh * D_LG, in31, a0c)[1] for rh in RHO]) / Vph(M310, D_LG, a0c)
    S2 = np.array([proj_field((0.0, D_LG), D_LG, M310, rh * D_LG, in31, a0c, at_centre=True)[1] for rh in RHO]) / Vph(M310, D_LG, a0c)
    # the pull toward the partner per unit of each galaxy's own phantom at d: region MW acts on M31 (-L1) and on the MW (+S1);
    # region M31 acts on the MW (+L2) and on M31 (-S2); the relative (closing) acceleration gains V_MW (-L1 + S1) + V_31 (L2 - S2)
    KMW, K31 = -L1 + S1, L2 - S2
    P("    per unit of the galaxy's own phantom at d, against its region's radius r_e/d (the watershed fixed at 0.47 d from the MW):")
    P("      r_e/d:            " + " ".join(f"{x_:6.2f}" for x_ in RHO))
    P("      MW region on M31 " + " ".join(f"{-x_:+6.3f}" for x_ in L1) + "   (the leak across the watershed)")
    P("      MW region on MW  " + " ".join(f"{x_:+6.3f}" for x_ in S1) + "   (the lopsided region's self-pull toward M31)")
    P("      M31 region on MW " + " ".join(f"{x_:+6.3f}" for x_ in L2))
    P("      M31 region on M31" + " ".join(f"{-x_:+6.3f}" for x_ in S2))
    re0 = {f: (TABG[(f, round(Mmw0, 3))][-1] / Mpc, TABG[(f, round(M310, 3))][-1] / Mpc) for f in A0L6}
    k0 = {f: (float(np.interp(re0[f][0] / D_LG, RHO, KMW)), float(np.interp(re0[f][1] / D_LG, RHO, K31))) for f in A0L6}
    P(f"    today (M_b 1.145e11, 1:2): r_e(MW) = {re0['canonical'][0]:.2f} Mpc, r_e(M31) = {re0['canonical'][1]:.2f} Mpc (canonical): the "
      f"closing phantom pull is {k0['canonical'][0]:.2f} x the MW's and {k0['canonical'][1]:.2f} x M31's own phantom at d (reading T: 0, 0; "
      f"merged M*: the combined baryons' full phantom)")
    # the tracers at z = 0 (R = 1.3 Mpc from the barycentre): the projected phantom pull against reading T's
    zb = (1 - fmw_) * D_LG
    TRP = {}
    for f in A0L6:
        reM, re3 = re0[f]
        for th_deg in (10, 40, 70, 90, 110, 140, 170):
            th = math.radians(th_deg); rt_, zt_ = 1.3 * math.sin(th), zb + 1.3 * math.cos(th)
            nrad = np.array([math.sin(th), math.cos(th)])
            in_mw = bool(inMW(np.array([rt_]), np.array([zt_]))[0]) and math.hypot(rt_, zt_) < reM
            in_31 = bool(in31(np.array([rt_]), np.array([zt_]))[0]) and math.hypot(rt_, zt_ - D_LG) < re3
            gP = (proj_field((rt_, zt_), 0.0, Mmw0, reM, inMW, A0L6[f], inside=in_mw)
                  + proj_field((rt_, zt_), D_LG, M310, re3, in31, A0L6[f], inside=in_31))
            if in_mw:
                gT = -Vph(Mmw0, math.hypot(rt_, zt_), A0L6[f]) * np.array([rt_, zt_]) / math.hypot(rt_, zt_)
            elif in_31:
                gT = -Vph(M310, math.hypot(rt_, zt_ - D_LG), A0L6[f]) * np.array([rt_, zt_ - D_LG]) / math.hypot(rt_, zt_ - D_LG)
            else:
                gT = np.zeros(2)
            TRP[f"{f}/{th_deg}"] = dict(P_inward=float(-gP @ nrad), T_inward=float(-gT @ nrad),
                                        ratio=float((gP @ nrad) / (gT @ nrad)) if abs(gT @ nrad) > 0 else float("nan"))
    P("    tracers at 1.3 Mpc today, inward phantom pull reading P / reading T: " + "; ".join(
        f"{k_.split('/')[1]} deg {v_['ratio']:.2f}" for k_, v_ in TRP.items() if k_.startswith("canonical")))
    rP = [v_["ratio"] for v_ in TRP.values() if v_["ratio"] == v_["ratio"]]
    ths = np.radians([10, 40, 70, 90, 110, 140, 170])
    est = {f: float(np.sum(np.sin(ths) * np.sqrt([TRP[f"{f}/{t_}"]["ratio"] for t_ in (10, 40, 70, 90, 110, 140, 170)])) / np.sum(np.sin(ths)))
           for f in A0L6}
    check("P1 (reported, pre-declared) READING T IS THE DOOR'S MOST FAVOURABLE READING FOR R_0: under the exact projection the "
          "tracers feel at least reading T's phantom pull in every direction today (the partner's phantom leaks into their basin)",
          f"P/T = {min(rP):.2f}-{max(rP):.2f} over 7 directions x 2 footings (below 1 near the perpendicular: the Gauss layer on the "
          f"cut face repels); solid-angle estimate of R_0(P)/R_0(T) with R_0 ~ pull^(1/2) (XR9's M_b scaling): "
          + ", ".join(f"{f} {v_:.3f} ({math.log10(v_):+.3f} dex)" for f, v_ in est.items()), min(rP) >= 0.98, load_bearing=False)
    OUT["numbers"]["reading_P"] = dict(r_e_over_d=RHO.tolist(), MW_on_M31=(-L1).tolist(), MW_self=S1.tolist(), M31_on_MW=L2.tolist(),
                                       M31_self=(-S2).tolist(), closing_today=k0, tracers_z0=TRP, gauss_control=gau,
                                       R0_ratio_P_over_T_estimate=est)
    P(f"    [{time.time() - T0:.0f}s]")

    # ============================================================================================ the timing
    banner("T1-T2  THE MILKY WAY--M31 TIMING UNDER THE DOOR AND UNDER M* (XR4's Hubble-flow scheme; item 13's own scheme beside it)")

    def mstar_acc(Mb, a0, h):
        """M*: the pair inside the merged LG region feels item 13's test-particle MOND inside the region's own kappa-form edge
        (XR6's 2% tanh edge) plus the carrier's Newtonian pull; beyond the edge, Newtonian."""
        tab = table_k(Mb, a0)

        def acc(l, rr):
            a = math.exp(l); H = H0 * math.sqrt(OM_M / a ** 3 + OM_L); z = 1.0 / a - 1.0
            re = float(np.interp(l, LNA_TAB, tab)); w = 0.5 * (1.0 - np.tanh((rr - re) / (0.02 * max(re, 1e-30))))
            gN = G * Mb * Msun / rr ** 2
            ret = float(retained(np.array(z), h))
            return -(w * nuL(gN / a0) * gN + (1 - w) * gN + G * RATIO_D * ret * Mb * Msun / rr ** 2) + OM_L * H0 ** 2 * rr, H
        return acc

    TIM = {}
    for Mb, hs in ((MB_LG, ("decay",)), (1.5 * MB_LG, ("decay",)), (1.8e11, ("none", "decay"))):
        for h in hs:
            for f in A0L6:
                ap = fit_branch(None, "approach", acc_fn=mstar_acc(Mb, A0L6[f], h))
                rc = fit_branch(None, "recede", acc_fn=mstar_acc(Mb, A0L6[f], h)) if ap is None else None
                TIM[f"Mstar/{Mb:.3e}/{h}/{f}"] = dict(branch="approach" if ap else ("recede" if rc else "none"),
                                                     u_today=(ap or rc or {}).get("u_today"))
    def doorP_acc(Mb, a0, h, f, leak_only=False):
        """the door, reading P: Newtonian baryons + carrier + the closing phantom pull of the two lopsided, leaking regions,
        V_MW(d) K_MW(r_e,MW/d) + V_31(d) K_31(r_e,31/d) (the z = 0-geometry tables, the watershed scaled with d)."""
        tMW, t31 = TABG[(f, round(Mb * fmw_, 3))], TABG[(f, round(Mb * (1 - fmw_), 3))]

        def acc(l, rr):
            a = math.exp(l); H = H0 * math.sqrt(OM_M / a ** 3 + OM_L); z = 1.0 / a - 1.0
            dd = rr / Mpc
            k1 = np.interp(float(np.interp(l, LNA_TAB, tMW)) / Mpc / dd, RHO, -L1 if leak_only else KMW, left=0.0)
            k2 = np.interp(float(np.interp(l, LNA_TAB, t31)) / Mpc / dd, RHO, L2 if leak_only else K31, left=0.0)
            g1 = G * Mb * fmw_ * Msun / rr ** 2; g2 = G * Mb * (1 - fmw_) * Msun / rr ** 2
            ph = k1 * (nuL(g1 / a0) - 1.0) * g1 + k2 * (nuL(g2 / a0) - 1.0) * g2
            ret = float(retained(np.array(z), h))
            return -((g1 + g2) * (1.0 + RATIO_D * ret) + ph) + OM_L * H0 ** 2 * rr, H
        return acc

    for Mb in MBS:
        for f in A0L6:
            ap = fit_branch(None, "approach", acc_fn=doorP_acc(Mb, A0L6[f], "decay", f))
            rc = fit_branch(None, "recede", acc_fn=doorP_acc(Mb, A0L6[f], "decay", f)) if ap is None else None
            TIM[f"door reading P/{Mb:.3e}/decay/{f}"] = dict(branch="approach" if ap else ("recede" if rc else "none"),
                                                             u_today=(ap or rc or {}).get("u_today"))
        ap = fit_branch(None, "approach", acc_fn=doorP_acc(Mb, A0L6["canonical"], "decay", "canonical", leak_only=True))
        rc = fit_branch(None, "recede", acc_fn=doorP_acc(Mb, A0L6["canonical"], "decay", "canonical", leak_only=True)) if ap is None else None
        TIM[f"door reading P, leak only/{Mb:.3e}/decay/canonical"] = dict(branch="approach" if ap else ("recede" if rc else "none"),
                                                                          u_today=(ap or rc or {}).get("u_today"))
    for k_, v_ in OWN.items():
        TIM[f"door/{k_}"] = dict(branch="approach" if v_["approach"] is not None else "recede",
                                 u_today=v_["approach"] if v_["approach"] is not None else v_["recede"])
    for f, x_ in T13.items():
        TIM[f"item13 (h76 scheme)/1.800e+11/none/{f}"] = dict(branch="approach", u_today=x_[1])
    for k_, v_ in TIM.items():
        P(f"    {k_:44s}: {v_['u_today']:+7.1f} km/s at 0.78 Mpc ({v_['branch']})" if v_["u_today"] is not None else f"    {k_:44s}: none")
    vd = [v_["u_today"] for k_, v_ in TIM.items() if k_.startswith("door/")]
    vp = [v_["u_today"] for k_, v_ in TIM.items() if k_.startswith("door reading P/") and v_["u_today"] is not None]
    vm = [v_["u_today"] for k_, v_ in TIM.items() if k_.startswith("Mstar/") and v_["u_today"] is not None]
    P(f"    measured: {V_LG:+.0f} km/s (vdM12 -109.3 +- 4.4); the Newtonian timing mass that reproduces it: {MT:.2e} Msun")
    check("T1 (reported) THE MW--M31 TIMING UNDER THE DOOR, READING T: two partitioned regions attract as Newtonian real masses "
          "(baryons + carrier), so the pair barely decelerates: at 0.78 Mpc today it recedes or falls back at a few km/s, missing "
          "the measured -110 km/s by more than 20 sigma", f"reading T: {min(vd):+.1f} to {max(vd):+.1f} km/s over M_b 1.1-1.7e11 "
          f"and the three carrier histories (a0-blind); closest {(min(vd) - V_LG) / EV_LG:.0f} sigma from -109.3 +- 4.4",
          min(vd) - V_LG > 20 * EV_LG, load_bearing=False)
    check("T1P (reported) THE SAME UNDER READING P (the exact projection: leak + lopsided self-pull, z = 0-geometry tables): the "
          "measured approach lies within 3 sigma", f"reading P: " + (f"{min(vp):+.1f} to {max(vp):+.1f} km/s (decay, M_b 1.1-1.7e11, both "
          "footings)" if vp else "no orbit reaches 0.78 Mpc"), bool(vp) and min(abs(v_ - V_LG) for v_ in vp) <= 3 * EV_LG,
          load_bearing=False)
    check("T2 (reported) M* (the pair inside one merged region) falls together faster than measured: the approach at 0.78 Mpc is "
          "more negative than -110 km/s in every M* variant (item 13: over-predicted by the simple radial model; the published "
          "MOND reading is a past close encounter, Zhao+2013, which the door's Newtonian pair cannot have had)",
          f"M* (XR4 scheme, edge + carrier): {min(vm):+.0f} to {max(vm):+.0f} km/s; item 13 (h76 scheme, no edge/carrier) "
          f"{T13['canonical'][1]:+.0f}/{T13['alt'][1]:+.0f}", len(vm) > 0 and max(vm) < V_LG, load_bearing=False)
    OUT["numbers"]["timing"] = TIM
    P(f"    [{time.time() - T0:.0f}s]")

    # ============================================================================================ summary
    banner("SUMMARY (scored column: " + ("the door, reading T, MW:M31 1:2, kinematic d(t)" if DOOR else "M*, merged (MUTATE)") + ")")
    for k_, v_ in SC.items():
        P(f"  {k_:44s} R_0 = {v_:.3f} Mpc ({math.log10(v_ / R0M):+.3f} dex)")
    P(f"  timing at 0.78 Mpc: door {min(vd):+.1f} to {max(vd):+.1f} km/s | M* {min(vm):+.0f} to {max(vm):+.0f} | measured -110")
    nlb = sum(1 for _, ok, lb in CH if lb and not ok)
    OUT["numbers"]["scored_R0"] = SC
    OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
    fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
    json.dump(OUT, open(fn, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}   "
      f"[{time.time() - T0:.0f}s]")
    sys.exit(1 if nlb else 0)
