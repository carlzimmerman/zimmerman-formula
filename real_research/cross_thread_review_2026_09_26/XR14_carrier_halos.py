#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR14_carrier_halos.py -- M*'s CARRIER RESOLVED AROUND THE KiDS LENSES: L375's self-consistent spherical shell model with the
carrier's trigger replaced by L388's (the phantom-inclusive x~).  Part 1 of 2 (the halos); XR14_kids_mstar_carrier.py
scores them.  Cross-thread review, 2026-09-26 (night).  Read-only on every other file.

WHY.  XR10's validator finds DE10's KiDS pass (dabce1b73: -37.0/-34.0 hard, -32.3/-29.3 at w = 0.25, 600 km/s) off M* on
the carrier: DE10 re-ran L375's shell model with L375's OWN trigger (the Newtonian matter density, x~ > 5), not M*'s carrier,
which is L388's (78fc5dd81): L377's full construction at L388's cell, whose trigger reads the PHANTOM-INCLUSIVE x~.

THE SHELL MODEL (L375, 7 of its pieces kept exactly): secondary infall on M(z) = M_200 exp[-0.75 (z - 0.25)] from an NFW
(c = 4) at z = 3; new shells at 2 r_200(z) with v_r = -v_200, v_t = 0.4 v_200; exact spherical self-gravity of the
carrier; static baryons = Hernquist M_b + the rest of f_b M_200 as an NFW-shaped CGM, grown with M(z); L390's refitted M_b
(p = 1, x_c0 = 2.5) and L390/DE10's seed rule 1200 + 10 b + int(v_k)//25; N = 60000; 1 Myr leapfrog steps.  L375's halo()
is copied line for line (control C1 of the scoring script: in 'L375' mode it reproduces DE10's committed table and XR9's
cached histograms exactly); only the trigger block is a choice.

THE TRIGGERS (a label per halo; never pooled).  L388's trigger rule is read from L388's / L377's source at run time and
every defining line is asserted verbatim (check T0):
    x~ = 1.5 Omega_m(a) (delta_m + delta_ph) > XC_TRIG,  Gamma = GAMMA_TRIG H,  isotropic kick v_k,
with delta_ph the baryons' QUMOND phantom where the switch is on, rho_ph = (1/4 pi r^2) d/dr [f (nu_mono(g_N,b/a0) - 1)
M_b(<r)] (L377's phantom() in spherical form, the switch edge Gauss-compensated by centred differences as L377's mesh
divergence; C3 checks it against L377's own phantom() on a mesh).  a0 is the footing's: L388 ran canonical only; both are
run here, each carrier scored on its own footing (the canonical carrier on the alt footing is reported as 'as run').
The rule reads "the phantom", so it needs a switch.  L388 used its own, the matter-only reading; M* has one switch, the
MOND-sector gate, and the same-model PM run L396 (pending) feeds the trigger that gate's phantom.  Both are run, labelled:
  'MSPH'  M*'S CARRIER (the XR10 row): L388's trigger rule reading the phantom of M*'S OWN GATE, as L396 does: MS2's
          MOND-sector reading x = 4 pi G (rho_b + rho_ph,all - f_b rho_bar_m)/H^2 (the baryons + their untruncated phantom,
          carrier-blind), MS5's kappa cap x -> min(x, (v_cap/(r H))^2), the vacuum gate at L388's cell, hard, the region
          connected to the centre.
  'L388'  L388'S CARRIER AS WRITTEN: the phantom switched as L377's phantom() switches it at L388's cell, where
          x~_m [Omega_L(a)/Omega_L0]^P_GATE > X_C0 per cell (here per radial bin), x~_m the MATTER-ONLY variable (carrier +
          baryons) -- L388's own branch, a different switch from M*'s (a switch-branch mix inside M*).
  'L375'  L375's own (DE10's carrier; the C1 control): a cold element decays at Gamma = 10 H(z) where
          x~ = (3/2)(rho_tot - rho_bar_m)/rho_crit(z) > 5, rho_tot = carrier + the bin's baryons (Newtonian, no phantom).
  'FK1'   VARIANT (labelled): FK1's field-derived conversion (c2e1fa119).  The pair instability's exponent grows as n^2 on
          the HEAVY (cold) component's own density; with the gated coupling lambda ~ K^(-2q), q = 1.75, the threshold is
          n_t(z) = delta_t0 n_bar_c0 E(z)^(1/2 + 2q) with FK1's delta_t0 = 5 (its N2), sharp (complete at n_t, negligible
          6% below): every cold element in a bin whose cold-carrier density exceeds n_t converts in that step and is kicked
          at v_k.  FK1's sqrt(sigma) halo modulation (an O(1) estimate) is not modelled.

CHECKS (this script)
  T0 CONTROL (trace): L388's cell (X_C0, P_GATE), kicks, rate and mode, and L377's trigger and phantom lines are found
     verbatim in their committed sources; the constants used here are parsed from them.
  C3 CONTROL (the sphere is L377's phantom): for a spherical baryon blob inside a spherical matter profile at z_l = 0.25,
     L377's own phantom() on a 3-d mesh (L388's cell set as L388 sets it) and this script's spherical phantom agree on
     the switched region and on the enclosed phantom mass inside it (10%), and both are Gauss-compensated beyond it.
  H1 (on completion) every planned halo is present and conserves its particle count (n within 1% of the planned N).
MUTATE=1 writes a separate cache (XR14_carrier_halos_results_MUTATE.json): v_k = 0 in every decaying run, one run per
(trigger, bin, footing) at the 600 km/s seed, used for every kick (L388's MUTATE convention).

Run from the repository root, repeat until it reports all halos present (single-threaded, ~1 min per halo):
    XR14_MAXN=12 python3 real_research/cross_thread_review_2026_09_26/XR14_carrier_halos.py   (MUTATE=1 for the control)
"""
import os, sys, json, math, time, re, inspect
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1"); os.environ.setdefault("MKL_NUM_THREADS", "1")
import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.special import erf

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DS = os.path.join(REPO, "real_research", "dark_sector_2026")
FKD = os.path.join(REPO, "real_research", "dark_fluid_kick_2026")
sys.path.insert(0, DS)
from L375_triggered_carrier_galaxy_retention import (G, TU, Om, OL, FB, H0, RHOC0, ZL, ZSTART, RAP, M200_BINS, E, c200,   # noqa: E402
                                                     mfn, t_of_z, z_of_t, r200_of)          # L375's background and hosts (its halo() is not run)
import L377_full_construction_pm as L77                         # noqa: E402  (the module L388 runs, via L379)

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR14_carrier_halos"
CACHE = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
T0 = time.time()
P = lambda *a: print(*a, flush=True)
NPART = int(os.environ.get("XR14_N", "60000"))
MAXN = int(os.environ.get("XR14_MAXN", "12"))
KPC_M = 3.0856775814913673e19
A0_KMS = {f_: L77.A0[f_] / (1e6 / KPC_M) for f_ in ("canonical", "alt")}   # a0 in (km/s)^2/kpc (L377's footings)
V_CAP = 325.0                                                    # km/s (MS3/MS5)
FEET = ("canonical", "alt")
VK_VARIANT = (575.0, 650.0)                                      # FK1's variant: the window's ends

# ================================================================================ T0: L388's trigger, read from its source
SRC388 = open(os.path.join(DS, "L388_linear_gate_pooled.py")).read()
_m = re.search(r"^L79\.L77\.X_C0, L79\.L77\.P_GATE = ([\d.]+), (\d+)", SRC388, re.M)
L77.X_C0, L77.P_GATE = float(_m.group(1)), int(_m.group(2))    # L388's cell, set on L377's module exactly as L388 sets it
_m = re.search(r'cfgs \+= \[\(f"s\{sp\}_\{t\}", sp, sk, L77\.XC_TRIG, v, ([\d.]+), TMP, "(\w+)", L77\.A0\["canonical"\]\)', SRC388)
GAMMA_TRIG, MODE388 = float(_m.group(1)), _m.group(2)          # L388's decay rate (units of H) and L377's run mode
VK = tuple(float(x) for x in re.search(r"^VK = \(([^)]*)\)", SRC388, re.M).group(1).split(","))
XC_TRIG = L77.XC_TRIG                                            # L388's trigger threshold: L377's module constant, as L388 passes it
SRC377_RUN, SRC377_PH = inspect.getsource(L77.run), inspect.getsource(L77.phantom)
T0_LINES = {
    "run: the matter part of x~": (SRC377_RUN, "xt = 1.5 * Om_a(a) * (rho - 1.0)"),
    "run: the phantom read by the trigger": (SRC377_RUN, "xt = xt + 1.5 * Om_a(a) * ph[1]"),
    "run: in mode full": (SRC377_RUN, 'if mode in ("full", "trigger") and ph[1] is not None:'),
    "run: threshold and rate": (SRC377_RUN, "hit = idx[(xp > xc) & (krng.random(len(idx)) < 1 - math.exp(-gamma * Hnorm(a) * dt))]"),
    "run: the isotropic kick": (SRC377_RUN, "pcar[hit] += a * (vk / 100.0) * nh"),
    "phantom: the vacuum gate factor": (SRC377_PH, "gate = (OL / (Om * a ** -3 + OL) / OL) ** P_GATE"),
    "phantom: the matter-only switch": (SRC377_PH, "f = (1.5 * Om_a(a) * (rho - 1.0) * gate > X_C0) if on else np.ones_like(rho, bool)"),
    "phantom: the kernel on the baryons' field": (SRC377_PH, "nu1 = nu_vec(np.sqrt(gb[0] ** 2 + gb[1] ** 2 + gb[2] ** 2) / a0c) - 1.0"),
    "phantom: switched (nu - 1) g_N,b": (SRC377_PH, "w = [np.where(f, nu1 * g, 0.0) for g in gb]"),
    "phantom: delta_ph = -(2a^2/3 Om) div w": (SRC377_PH, "return s.poisson(-a * divw), -(2 * a * a / (3 * Om)) * divw, float(f.mean())"),
    "L388: the cell on L377's module": (SRC388, "L79.L77.X_C0, L79.L77.P_GATE = 2.5, 1"),
}
# FK1's gate exponent and threshold normalisation (its committed N2)
FK1R = json.load(open(os.path.join(FKD, "FK1_kick_as_phase_change_results.json")))["numbers"]["N2"]
Q_FK1 = float(FK1R["q_linear_gate"])                             # 1.75
DT0_FK1 = 5.0                                                    # FK1 N2: delta_t = 5 at z = 0 (the gated case is normalised there)
assert "delta_t = 5" in open(os.path.join(FKD, "FK1_kick_as_phase_change.out")).read()


def gate_factor(z):
    """L377's phantom() gate [Omega_L(a)/Omega_L0]^P_GATE, its own expression and constants (L388's cell)."""
    a = 1.0 / (1.0 + z)
    return (L77.OL / (L77.Om * a ** -3 + L77.OL) / L77.OL) ** L77.P_GATE


def xph_switched(mode, rmid, Mb_mid, xm, z, a0k):
    """the switched phantom the trigger reads, as x~_ph = (3/2) rho_ph / rho_crit(z) at the bin midpoints.
    rmid [kpc], Mb_mid = the baryons' enclosed mass at rmid [Msun], xm = the matter-only switch variable at rmid, a0k in
    (km/s)^2/kpc.  Returns (x~_ph, f)."""
    gN = G * Mb_mid / rmid ** 2                                   # the baryons' Newtonian field
    nu = L77.nu_vec(gN / a0k)                                     # L377's nu_mono (L352's table rebuilt; L377 C2)
    if mode == "L388":                                            # L377's phantom(): f = x~_m gate > X_C0, per cell (bin)
        f = xm * gate_factor(z) > L77.X_C0
    elif mode == "MSPH":                                          # M*'s gate: MS2's MOND-sector door + MS5's kappa cap, hard
        rho_dyn = np.gradient(nu * Mb_mid, rmid) / (4 * math.pi * rmid ** 2)       # baryons + their untruncated phantom
        x = 1.5 * (rho_dyn - FB * Om * RHOC0 * (1 + z) ** 3) / (RHOC0 * E(z) ** 2)
        x = np.minimum(x, (V_CAP / (rmid * H0 * E(z))) ** 2)
        f = x * gate_factor(z) > L77.X_C0
        off = np.where(~f)[0]
        if off.size:
            f[off[0]:] = False                                    # the region connected to the centre (DE10/XR9's gate)
    else:
        raise ValueError(mode)
    Mph = np.where(f, (nu - 1.0) * Mb_mid, 0.0)                   # f (nu - 1) M_b(<r): the switched phantom's enclosed mass
    rho_ph = np.gradient(Mph, rmid) / (4 * math.pi * rmid ** 2)   # centred differences: the edge's compensation over 2 bins
    return 1.5 * rho_ph / (RHOC0 * E(z) ** 2), f


def nt_fk1(z):
    """FK1's conversion threshold on the heavy (cold) carrier's own density [Msun/kpc^3]."""
    return DT0_FK1 * (1 - FB) * Om * RHOC0 * E(z) ** (0.5 + 2 * Q_FK1)


def halo_x(cfg):
    """L375's halo() line for line (alpha = 0.75, grow_b = True, DE10's configuration) with the trigger as a choice:
    mode in {'L375', 'L388', 'MSPH', 'FK1'}; a0k only enters the phantom-inclusive triggers."""
    tag, mode, b, Mb, vk, gam, a0k, N, seed = cfg
    alpha, grow_b = 0.75, True
    rng = np.random.default_rng(seed)
    M0 = M200_BINS[b]; c0 = c200(M0); r0 = r200_of(M0, ZL); rs0 = r0 / c0
    ab = 3.0 * (Mb / 1e11) ** 0.3; Mcgm = max(FB * M0 - Mb, 0.0)
    Mz = (lambda z: M0 * math.exp(-alpha * (z - ZL))) if alpha > 0 else (lambda z: M0)

    def Mst(r, z):                                                   # static baryons (+ CGM), grown with the halo
        f = Mz(z) / M0 if grow_b else 1.0
        return f * (Mb * r ** 2 / (r + ab) ** 2 + Mcgm * np.minimum(mfn(r / rs0) / mfn(c0), 1.0))

    def rho_st(r, z):
        f = Mz(z) / M0 if grow_b else 1.0
        return f * (Mb * ab / (2 * math.pi * r * (r + ab) ** 3) +
                    np.where(r < r0, Mcgm / (4 * math.pi * rs0 ** 3 * mfn(c0)) / ((r / rs0) * (1 + r / rs0) ** 2), 0.0))

    zs = ZSTART if alpha > 0 else 1.1
    m = (1 - FB) * M0 / N                                            # equal-mass carrier shells
    Mi = Mz(zs); ci = 4.0 if alpha > 0 else c0; ri = r200_of(Mi, zs) if alpha > 0 else r0; rsi = ri / ci
    Ni = int(round((1 - FB) * Mi / m))
    u = rng.random(Ni) * mfn(ci); xg = np.geomspace(1e-5, ci, 20000); r = np.interp(u, mfn(xg), xg) * rsi
    rg = np.geomspace(1e-3 * rsi, ri, 4000)
    rho_c = (1 - FB) * Mi / (4 * math.pi * rsi ** 3 * mfn(ci)) / ((rg / rsi) * (1 + rg / rsi) ** 2)
    Mc_r = (1 - FB) * Mi * mfn(rg / rsi) / mfn(ci)
    integ = rho_c * G * (Mst(rg, zs) + Mc_r) / rg ** 2               # Jeans (isotropic), truncated at r_200
    tail = -np.concatenate([[0.0], cumulative_trapezoid(integ[::-1], rg[::-1])])[::-1]
    sg = np.sqrt(np.maximum(np.interp(r, rg, tail / rho_c), 0.0))
    v = rng.normal(size=(Ni, 3)) * sg[:, None]
    vr = v[:, 0].copy(); L = r * np.hypot(v[:, 1], v[:, 2]); cold = np.ones(Ni, bool)

    t0, t1 = t_of_z(zs), t_of_z(ZL)
    dt = 1.0e-3 / TU; nstep = int(math.ceil((t1 - t0) / dt)); dt = (t1 - t0) / nstep
    rmin = 0.05; edges = np.geomspace(0.05, 2e4, 240); rmid = np.sqrt(edges[1:] * edges[:-1])
    vol = 4 / 3 * math.pi * (edges[1:] ** 3 - edges[:-1] ** 3)
    carry = 0.0; t = t0; z = zs; ndec = 0; ndec_ph = 0

    def acc(r, z):
        order = np.argsort(r); rank = np.empty(len(r), int); rank[order] = np.arange(len(r))
        return -G * (Mst(r, z) + m * (rank + 0.5)) / r ** 2 + L ** 2 / r ** 3

    a_ = acc(r, z)
    for i in range(nstep):
        vr += 0.5 * dt * a_
        r = r + dt * vr
        neg = r < rmin; r[neg] = 2 * rmin - r[neg]; vr[neg] = np.abs(vr[neg])
        t += dt; z = z_of_t(t)
        if alpha > 0:                                                # secondary infall on the accretion history
            carry += (1 - FB) * (Mz(z) - Mz(z_of_t(t - dt))) / m
            k = int(carry); carry -= k
            if k > 0:
                Mnow = Mz(z); rn = 2 * r200_of(Mnow, z); v200 = math.sqrt(G * Mnow / r200_of(Mnow, z))
                r = np.concatenate([r, np.full(k, rn) * (1 + 0.05 * rng.random(k))])
                vr = np.concatenate([vr, np.full(k, -v200)]); L = np.concatenate([L, rn * 0.4 * v200 * np.ones(k)])
                cold = np.concatenate([cold, np.ones(k, bool)])
        a_ = acc(r, z)
        vr += 0.5 * dt * a_
        if gam > 0 and cold.any():
            if mode == "FK1":                                        # FK1: the heavy component's own density, sharp threshold
                cntc, _ = np.histogram(r[cold], edges)
                idx = np.where(cold & (np.interp(r, rmid, cntc * m / vol) > nt_fk1(z)))[0]
                hit = idx                                            # complete in the step the threshold is crossed (FK1 N1)
            else:
                cnt, _ = np.histogram(r, edges)
                rho_tot = cnt * m / vol + rho_st(rmid, z)
                xt = 1.5 * (np.interp(r, rmid, rho_tot) - Om * RHOC0 * (1 + z) ** 3) / (RHOC0 * E(z) ** 2)
                if mode == "L375":                                   # L375's trigger, unchanged
                    idx = np.where(cold & (xt > 5.0))[0]
                else:                                                # L388's: + the switched phantom (L377's run, mode 'full')
                    xm = 1.5 * (rho_tot - Om * RHOC0 * (1 + z) ** 3) / (RHOC0 * E(z) ** 2)
                    xph, _ = xph_switched(mode, rmid, Mst(rmid, z), xm, z, a0k)
                    xt0 = xt
                    xt = xt + np.interp(r, rmid, xph)
                    idx = np.where(cold & (xt > XC_TRIG))[0]
                hit = idx[rng.random(len(idx)) < 1 - math.exp(-gam * H0 * E(z) * dt)]
                if mode not in ("L375",) and len(hit):
                    ndec_ph += int(np.sum(xt0[hit] <= XC_TRIG))       # decays the phantom term alone caused
            if len(hit):
                nh = rng.normal(size=(len(hit), 3)); nh /= np.linalg.norm(nh, axis=1)[:, None]
                vt_old = L[hit] / r[hit]
                vr[hit] += vk * nh[:, 0]
                L[hit] = r[hit] * np.hypot(vt_old + vk * nh[:, 1], vk * nh[:, 2])
                cold[hit] = False; ndec += len(hit)
    hist_all, _ = np.histogram(r, edges); hist_cold, _ = np.histogram(r[cold], edges)
    # diagnostics at z_l: the trigger's reach and the phantom's switched region
    cnt = hist_all; rho_tot = cnt * m / vol + rho_st(rmid, z)
    xm = 1.5 * (rho_tot - Om * RHOC0 * (1 + z) ** 3) / (RHOC0 * E(z) ** 2)
    diag = dict(z_end=z, n_decayed=int(ndec), n_decayed_phantom_only=int(ndec_ph))
    if mode in ("L388", "MSPH"):
        xph, f = xph_switched(mode, rmid, Mst(rmid, z), xm, z, a0k)
        xtot = xm + xph
        diag["r_switch_kpc"] = float(rmid[np.where(f)[0].max()]) if f.any() else 0.0
    else:
        xtot = xm
    on = np.where(xtot <= (5.0 if mode == "L375" else XC_TRIG))[0]
    diag["r_trig_kpc"] = float(rmid[on[0] - 1]) if (on.size and on[0] > 0) else 0.0      # the trigger region from the centre
    if mode == "FK1":                                                # the conversion front: all carrier (heavy + products) at n_t
        rc_ = hist_all * m / vol
        off = np.where(rc_ <= nt_fk1(z))[0]
        diag["r_trig_kpc"] = float(rmid[off[0] - 1]) if (off.size and off[0] > 0) else 0.0
    return tag, dict(edges=edges, m=m, hist=hist_all, hist_cold=hist_cold, n=len(r), n_cold=int(cold.sum()),
                     M_ap=float(np.sum(r < RAP)) * m, M_ap_cold=float(np.sum((r < RAP) & cold)) * m, diag=diag)


def plan():
    """{tag: cfg}.  L390's masses (p = 1, x_c0 = 2.5) and DE10's seed rule throughout."""
    R90 = json.load(open(os.path.join(DS, "L390_kids_resolved_linear_gate_results.json")))["numbers"]
    MB = R90["M_b"]["p=1, x_c0=2.5"]
    seed = lambda b, v: 1200 + 10 * b + int(v) // 25
    cf = {}
    for b in range(4):
        cf[f"nodecay_b{b}"] = ("nodecay", "L375", b, MB[b], 650.0, 0.0, 0.0, NPART, 1100 + b)      # L390's no-decay runs
    if not MUTATE:
        for b in range(4):
            for v in (600.0, 650.0):                             # C1: DE10's own halos, L375's trigger
                cf[f"L375_b{b}_v{int(v)}"] = ("L375", "L375", b, MB[b], v, 10.0, 0.0, NPART, seed(b, v))
        for f_ in FEET:
            for b in range(4):
                for v in VK:                                     # L388's trigger, its own (matter-only) switch; each footing's a0
                    cf[f"L388_{f_}_b{b}_v{int(v)}"] = ("L388", "L388", b, MB[b], v, GAMMA_TRIG, A0_KMS[f_], NPART, seed(b, v))
                for v in VK:                                     # M*'s carrier: L388's trigger reading M*'s own gate's phantom
                    cf[f"MSPH_{f_}_b{b}_v{int(v)}"] = ("MSPH", "MSPH", b, MB[b], v, GAMMA_TRIG, A0_KMS[f_], NPART, seed(b, v))
        for b in range(4):
            for v in VK_VARIANT:                                 # variant: FK1's conversion (a0-blind)
                cf[f"FK1_b{b}_v{int(v)}"] = ("FK1", "FK1", b, MB[b], v, GAMMA_TRIG, 0.0, NPART, seed(b, v))
    else:                                                        # v_k = 0, one run per (trigger, bin, footing) at the 600 seed
        for b in range(4):
            for f_ in FEET:
                cf[f"L388_{f_}_b{b}_v0"] = ("L388", "L388", b, MB[b], 0.0, GAMMA_TRIG, A0_KMS[f_], NPART, seed(b, 600.0))
                cf[f"MSPH_{f_}_b{b}_v0"] = ("MSPH", "MSPH", b, MB[b], 0.0, GAMMA_TRIG, A0_KMS[f_], NPART, seed(b, 600.0))
            cf[f"FK1_b{b}_v0"] = ("FK1", "FK1", b, MB[b], 0.0, GAMMA_TRIG, 0.0, NPART, seed(b, 600.0))
    return {k_: (k_,) + c_[1:] for k_, c_ in cf.items()}, MB


C3_L, C3_N = 8.0, 80                                             # C3's mesh: 8 Mpc/h (comoving), 80^3


def c3_mesh():
    """C3: L377's own phantom() on a 3-d mesh (L388's cell) against xph_switched('L388') for one spherical configuration at
    z_l = 0.25: a Gaussian baryon blob (3e11 Msun/h, sigma = 0.15 Mpc/h) inside a matter profile delta(R) = 20/(1 + (R/0.6)^2)
    (R comoving Mpc/h; switch edge ~1.1).  Mesh: 8 Mpc/h, 80^3, L377's code units (periodic, its own Poisson and divergence).
    The sphere works in physical kpc and Msun: r = a R 1000/h."""
    Lb, Nb = C3_L, C3_N
    s = L77.L2.Sim(Lb, Nb, 8)
    g = (np.arange(Nb) + 0.5) * s.d - Lb / 2
    X, Y, Z = np.meshgrid(g, g, g, indexing="ij"); R = np.sqrt(X ** 2 + Y ** 2 + Z ** 2); del X, Y, Z
    Mb, sig = 3e11, 0.15
    blob = np.exp(-0.5 * (R / sig) ** 2); blob *= Mb / blob.sum()
    rb = L77.WB + blob / (L77.RHO_M * s.d ** 3)
    rb -= (rb.mean() - L77.WB)
    rho = 1.0 + 20.0 / (1 + (R / 0.6) ** 2)
    a = 1 / (1 + ZL); a0c = L77.A0["canonical"] / L77.ACC_UNIT
    _, dph, frac = L77.phantom(s, rb, rho, a, a0c)                  # L377's function, L388's cell
    f_mesh = 1.5 * L77.Om_a(a) * (rho - 1.0) * gate_factor(ZL) > L77.X_C0
    re_mesh = float(R[f_mesh].max())
    # the same configuration on this script's radial grid
    h = L77.h
    rq = np.geomspace(5.0, 6000.0, 400)                             # physical kpc
    Rq = rq * h / 1000.0 / a                                        # comoving Mpc/h
    Mb_enc = Mb / h * (erf(Rq / (math.sqrt(2) * sig)) - math.sqrt(2 / math.pi) * (Rq / sig) * np.exp(-0.5 * (Rq / sig) ** 2))
    xm = 1.5 * L77.Om_a(a) * (20.0 / (1 + (Rq / 0.6) ** 2))          # the matter-only switch variable on the same profile
    xph, f_sph = xph_switched("L388", rq, Mb_enc, xm, ZL, A0_KMS["canonical"])
    re_sph = float(Rq[np.where(f_sph)[0].max()])
    gN = G * Mb_enc / rq ** 2
    Mph_an = np.where(f_sph, (L77.nu_vec(gN / A0_KMS["canonical"]) - 1) * Mb_enc, 0.0)            # f (nu - 1) M_b [Msun]
    Mph_bin = np.concatenate([[0.0], cumulative_trapezoid(4 * math.pi * rq ** 2 * xph * RHOC0 * E(ZL) ** 2 / 1.5, rq)])
    rows = []
    for Rs in (0.5, 0.7, 0.9, 1.6, 2.2):
        wgt = np.clip((Rs - R) / s.d + 0.5, 0.0, 1.0)               # cells weighted by the share inside (a one-cell ramp)
        mesh_M = float((dph * wgt).sum()) * L77.RHO_M * s.d ** 3 / h                              # Msun
        rk = Rs * 1000 / h * a
        rows.append(dict(R_Mpc_h=Rs, mesh=mesh_M, sphere_analytic=float(np.interp(rk, rq, Mph_an)),
                         sphere_binned=float(np.interp(rk, rq, Mph_bin) + Mph_an[0])))
    peak = max(abs(r_["sphere_analytic"]) for r_ in rows)
    return dict(edge_mesh_Mpc_h=re_mesh, edge_sphere_Mpc_h=re_sph, switched_fraction_mesh=frac, rows=rows, peak=peak)


if __name__ == "__main__":
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: v_k = 0 in every decaying run (separate cache); the scoring script's H1 must FAIL on it ***")
    # ---------------------------------------------------------------------------------------------- T0
    miss = [k_ for k_, (src, ln) in T0_LINES.items() if ln not in src]
    P(f"\n  T0 (trace) L388's cell X_C0 = {L77.X_C0}, P_GATE = {L77.P_GATE}; trigger XC_TRIG = {XC_TRIG}; rate {GAMMA_TRIG} H; mode "
      f"'{MODE388}'; kicks {VK}; FK1: q = {Q_FK1}, delta_t0 = {DT0_FK1}; lines found verbatim: {len(T0_LINES) - len(miss)}/{len(T0_LINES)}")
    t0ok = (not miss and (L77.X_C0, L77.P_GATE, XC_TRIG, GAMMA_TRIG, MODE388) == (2.5, 1, 5.0, 10.0, "full")
            and VK == (575.0, 600.0, 625.0, 650.0))
    P(f"  [{'PASS' if t0ok else 'FAIL'}] T0 CONTROL: L388's trigger definition is read from its source" + (f"; missing: {miss}" if miss else ""))
    # ---------------------------------------------------------------------------------------------- C3
    c3 = c3_mesh()
    P(f"\n  C3 the sphere vs L377's phantom() on a {C3_N}^3 mesh (z = 0.25, L388's cell, canonical a0): switch edge mesh "
      f"{c3['edge_mesh_Mpc_h']:.3f} / sphere {c3['edge_sphere_Mpc_h']:.3f} comoving Mpc/h (mesh cell {C3_L / C3_N:.3f})")
    for r_ in c3["rows"]:
        P(f"     M_ph(<{r_['R_Mpc_h']:.1f} Mpc/h): mesh {r_['mesh']:.4e}  sphere f(nu-1)M_b {r_['sphere_analytic']:.4e}  "
          f"sphere binned (the trigger's rho_ph integrated) {r_['sphere_binned']:.4e}  Msun")
    ins = [r_ for r_ in c3["rows"] if r_["R_Mpc_h"] < 1.0]
    out_ = [r_ for r_ in c3["rows"] if r_["R_Mpc_h"] > 1.5]
    c3ok = (abs(c3["edge_mesh_Mpc_h"] - c3["edge_sphere_Mpc_h"]) <= C3_L / C3_N + 1e-9
            and all(abs(r_["mesh"] / r_["sphere_analytic"] - 1) < 0.10 and abs(r_["sphere_binned"] / r_["sphere_analytic"] - 1) < 0.10 for r_ in ins)
            and all(abs(r_["mesh"]) < 0.10 * c3["peak"] and abs(r_["sphere_binned"]) < 0.10 * c3["peak"] for r_ in out_))
    P(f"  [{'PASS' if c3ok else 'FAIL'}] C3 CONTROL: same switched region (within one mesh cell), enclosed phantom inside it within 10%, "
      f"both compensated beyond it (< 10% of the peak)")
    # ---------------------------------------------------------------------------------------------- the halos
    cfgs, MB = plan()
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    cache.setdefault("halos", {})
    cache["config"] = dict(N=NPART, alpha=0.75, grow_b=True, seed_rule="1200 + 10 b + int(v_k)//25 (no-decay: 1100 + b)",
                           M_b_L390=MB, cell=dict(X_C0=L77.X_C0, P_GATE=L77.P_GATE), XC_TRIG=XC_TRIG, GAMMA_TRIG=GAMMA_TRIG,
                           kicks=VK, kicks_variants=VK_VARIANT, a0_kms=A0_KMS, fk1=dict(q=Q_FK1, delta_t0=DT0_FK1),
                           v_cap_kms=V_CAP, mutate=MUTATE)
    cache["T0"] = dict(ok=t0ok, missing=miss); cache["C3"] = dict(ok=c3ok, **c3)
    missing = [t for t in cfgs if t not in cache["halos"]]
    P(f"\n  {len(cfgs)} halos planned ({len(cfgs) - len(missing)} cached, {len(missing)} missing); this call runs up to {MAXN}   "
      f"[{time.time() - T0:.0f}s]")
    json.dump(cache, open(CACHE + ".tmp", "w"), indent=0); os.replace(CACHE + ".tmp", CACHE)
    for tag in missing[:MAXN]:
        t1 = time.time()
        _, d = halo_x(cfgs[tag])
        c_ = cfgs[tag]
        cache = json.load(open(CACHE))
        cache["halos"][tag] = dict(mode=c_[1], b=c_[2], Mb=c_[3], v_k=c_[4], gamma=c_[5], a0_kms=c_[6], N=c_[7], seed=c_[8],
                                   m=float(d["m"]), n=int(d["n"]), n_cold=int(d["n_cold"]), M_ap=d["M_ap"], M_ap_cold=d["M_ap_cold"],
                                   hist=[int(x) for x in d["hist"]], hist_cold=[int(x) for x in d["hist_cold"]], diag=d["diag"])
        cache["edges_kpc"] = [float(x) for x in d["edges"]]
        json.dump(cache, open(CACHE + ".tmp", "w"), indent=0); os.replace(CACHE + ".tmp", CACHE)
        dg = d["diag"]
        P(f"    {tag:24s} n = {d['n']}, decayed {dg['n_decayed'] / d['n']:.3f} (phantom-only {dg['n_decayed_phantom_only'] / max(dg['n_decayed'], 1):.3f}), "
          f"M(<0.5 Mpc/h) = {d['M_ap']:.3e}, trigger reach at z_l {dg['r_trig_kpc']:.0f} kpc"
          + (f", phantom switched to {dg['r_switch_kpc']:.0f} kpc" if "r_switch_kpc" in dg else "")
          + f"   [{time.time() - t1:.0f}s; total {time.time() - T0:.0f}s]")
    cache = json.load(open(CACHE))
    still = [t for t in cfgs if t not in cache["halos"]]
    if still:
        P(f"\n  {len(still)} halos still missing: re-run this script.   [{time.time() - T0:.0f}s]")
        sys.exit(0)
    okn = all(abs(cache["halos"][t]["n"] / NPART - 1) < 0.01 for t in cfgs)
    P(f"\n  [{'PASS' if okn else 'FAIL'}] H1 all {len(cfgs)} planned halos present; particle counts within 1% of N: {okn}   "
      f"[{time.time() - T0:.0f}s]")
    sys.exit(0 if (okn and t0ok and c3ok) else 1)
