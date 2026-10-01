#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG243_hierarchy_posthoc -- GATE 4 (HIERARCHY), run as a POST-HOC EXTRA: the frozen stop rule halted the lane at COSMIC, so nothing here is part of the
frozen verdict.  Frozen text: CFG243_FROZEN_CRITERIA.md section 2, Gate 4 (H1-H4).

TOY (frozen, with its declared departures): a host (a point mass of 1e12 Msun, or the same mass as a uniform sphere of radius 300 kpc for the 'inside the host'
row) and a satellite core of 1e9 Msun on a circular orbit at d = 30 or 100 kpc; a cloud of N = 3000 pressureless baryon TEST particles around the satellite
(radii 1-4 kpc, outward radial speed v = sqrt(G M_s / r) so that each decelerates and turns around at 2 r).  theta_b = tr(A) with A_ij = d v_i/d x_j integrated EXACTLY
along each trajectory by the tangent dynamics dA/dt = -A.A - Hessian(Phi) (single-stream, test particles: no noise, no estimator).  The same cloud is run in isolation
(host off).  The source (version U: every downward zero of theta_b; version F: the first only) creates dust Q m_p with Q = a0 / (3 g_loc), g_loc = the particle's total
acceleration magnitude (host + satellite): the AMT-2 closure with the peculiar field.  The cloud's own gravity and the cosmic expansion are neglected (timescales ~1 Gyr).
H1: dust created in the satellite (with host)/(isolated), both for the amplitude-weighted amount and the number of firing particles; pass iff <= 0.10 at every row.
H2: accreted satellite: extra dust created by the already-turned-around baryons while they fall through the host, U versus F (F: none by the flag).
H3: top-level, not bottom-level ownership: excursion-set (sharp-k random walks, sigma^2(M) from CLASS) for baryons that end in a 1e12 Msun system turning around at z = 0:
    the mass of the first turned-around system containing each baryon (the walk's maximum fixes the earliest time).  Pass iff >= 90% have M_fc >= 0.1 M_final.
H4: the status of the flag (text).
MUTATE=4: the source is given the host's membership (n = 1 for baryons in a host): H1 must flip FAIL -> PASS (a prescribed label, CFG48 G3: PARTIAL).
"""
import os, sys, math, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import CFG243_common as C

np.seterr(all="ignore")          # the single-stream tangent integration diverges at caustics (expected; counts after a caustic are dropped)
R = C.Run("CFG243_hierarchy_posthoc")
P = R.P
MUT = R.mutate
P(__doc__.strip())
P("\n  *** POST-HOC: the frozen stop rule halted the lane at COSMIC; nothing below is part of the frozen verdict ***")
G = C.G
A0 = C.A0
rng = np.random.default_rng(2430)
Ms, MH = 1e9, 1e12
SOFT_S, SOFT_H = 0.3, 1.0


def hess_point(dx, M, soft):
    r2 = (dx ** 2).sum(axis=1) + soft ** 2
    I = np.eye(3)[None]
    return G * M * (I / r2[:, None, None] ** 1.5 - 3.0 * dx[:, :, None] * dx[:, None, :] / r2[:, None, None] ** 2.5)


def acc_point(dx, M, soft):
    r2 = (dx ** 2).sum(axis=1) + soft ** 2
    return -G * M * dx / r2[:, None] ** 1.5


def make_host(kind):
    """returns (acc(x), hess(x), enclosed mass at d) of the host, centred on the origin."""
    if kind == "none":
        return (lambda x: np.zeros_like(x)), (lambda x: np.zeros((x.shape[0], 3, 3))), (lambda d: 0.0)
    if kind == "point":
        return (lambda x: acc_point(x, MH, SOFT_H)), (lambda x: hess_point(x, MH, SOFT_H)), (lambda d: MH)
    Rh = 300.0
    kk = G * MH / Rh ** 3
    return (lambda x: -kk * x), (lambda x: np.broadcast_to(kk * np.eye(3), (x.shape[0], 3, 3)).copy()), (lambda d: MH * (d / Rh) ** 3)


def run_cloud(host_kind, d, N=3000, T_gyr=2.0, dt_myr=1.0, seed=7, label=""):
    rg = np.random.default_rng(seed)
    acc_h, hess_h, Menc = make_host(host_kind)
    vc = math.sqrt(G * Menc(d) / d) if host_kind != "none" else 0.0
    # satellite on a circular orbit in the x-y plane (host frame); isolated: at rest at the origin
    def xs_of(t):
        if host_kind == "none":
            return np.zeros(3), np.zeros(3)
        om = vc / d
        return np.array([d * math.cos(om * t), d * math.sin(om * t), 0.0]), np.array([-vc * math.sin(om * t), vc * math.cos(om * t), 0.0])
    xs0, vs0 = xs_of(0.0)
    # cloud: radii 1-4 kpc, isotropic; outward radial speed sqrt(G Ms / r) (turnaround at 2 r); A from the flow field v_r(r) n
    n = rg.standard_normal((N, 3)); n /= np.linalg.norm(n, axis=1)[:, None]
    r = rg.uniform(1.0, 4.0, N)
    vr = np.sqrt(G * Ms / r)
    x = xs0[None] + r[:, None] * n
    v = vs0[None] + vr[:, None] * n
    vrp = -0.5 * vr / r
    nn = n[:, :, None] * n[:, None, :]
    A = vrp[:, None, None] * nn + (vr / r)[:, None, None] * (np.eye(3)[None] - nn)
    dt = dt_myr * 1e-3 / C.GYR_PER_KPC_KMS * 1e-0       # Myr -> kpc/(km/s)
    dt = dt_myr * 1e-3 / C.GYR_PER_KPC_KMS
    nsteps = int(T_gyr / (dt * C.GYR_PER_KPC_KMS))

    def field(x, t):
        xs, _ = xs_of(t)
        a = acc_h(x) + acc_point(x - xs[None], Ms, SOFT_S)
        H = hess_h(x) + hess_point(x - xs[None], Ms, SOFT_S)
        return a, H

    th_prev = np.trace(A, axis1=1, axis2=2)
    crossed = np.zeros(N, int)
    first = np.zeros(N, bool)
    g_first = np.full(N, np.nan)
    dustU = 0.0; dustF = 0.0
    t = 0.0
    q_first = np.zeros(N)
    for it in range(nsteps):
        # RK4 on (x, v, A)
        def f(x_, v_, A_, t_):
            a_, H_ = field(x_, t_)
            return v_, a_, -(A_ @ A_) - H_
        k1 = f(x, v, A, t)
        k2 = f(x + 0.5 * dt * k1[0], v + 0.5 * dt * k1[1], A + 0.5 * dt * k1[2], t + 0.5 * dt)
        k3 = f(x + 0.5 * dt * k2[0], v + 0.5 * dt * k2[1], A + 0.5 * dt * k2[2], t + 0.5 * dt)
        k4 = f(x + dt * k3[0], v + dt * k3[1], A + dt * k3[2], t + dt)
        x = x + dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        v = v + dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        A = A + dt / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])
        t += dt
        th = np.trace(A, axis1=1, axis2=2)
        down = (th_prev > 0) & (th <= 0) & np.isfinite(th) & np.isfinite(th_prev)
        if down.any():
            a_, _ = field(x, t)
            g = np.linalg.norm(a_, axis=1)
            Q = A0 / (3.0 * np.maximum(g, 1e-12))
            crossed += down
            newf = down & (~first)
            q_first[newf] = Q[newf]
            first |= newf
            dustU += float(Q[down].sum())
            dustF += float(Q[newf].sum())
        th_prev = th
    return dict(n_first=int(first.sum()), n_cross=int(crossed.sum()), dustF=dustF, dustU=dustU, N=N,
                med_cross=float(np.median(crossed[first])) if first.any() else 0.0, host=host_kind, d=d,
                frac_first=float(first.mean()))


R.banner("controls")
# control: the exact tangent dynamics reproduce a finite-difference velocity divergence for a radial Kepler flow (isolated, no host) at t = 0 and after a short time
test = run_cloud("none", 0.0, N=400, T_gyr=0.02, dt_myr=0.5, seed=3)
R.check("C1 the integrated tangent dynamics fire no source in the first 20 Myr of a freely expanding Kepler cloud (theta_b > 0)", test["n_cross"] == 0, f"{test['n_cross']} crossings")

R.banner("H1 (embedded: a formed-embedded cloud turning around inside a host) and the unflagged count")
cases = [("isolated", "none", 0.0), ("host point 30 kpc", "point", 30.0), ("host point 100 kpc", "point", 100.0), ("inside the host (uniform sphere R = 300 kpc, d = 100)", "uniform", 100.0)]
res = {}
for lab, kind, d in cases:
    t0 = time.time()
    res[lab] = run_cloud(kind, d, N=3000, T_gyr=2.0, dt_myr=1.0, seed=7)
    r_ = res[lab]
    P(f"  {lab:55s}: {r_['n_first']:4d}/{r_['N']} clouds particles fire; crossings (U) {r_['n_cross']:5d} (median per firing particle {r_['med_cross']:.1f}); dust F = {r_['dustF']:.4g}, U = {r_['dustU']:.4g} (Q m_p units); {time.time() - t0:.0f} s")
iso = res["isolated"]
tab = {}
for lab, kind, d in cases[1:]:
    r_ = res[lab]
    amp_F = r_["dustF"] / iso["dustF"]; amp_U = r_["dustU"] / iso["dustU"]; cnt = r_["n_first"] / iso["n_first"]
    tab[lab] = dict(amp_F=amp_F, amp_U=amp_U, count=cnt)
    P(f"  {lab:55s}: dust(host)/dust(isolated): F {amp_F:.3f}, U {amp_U:.3f}; firing-particle count ratio {cnt:.3f}")
R.num("H1", tab)
if MUT == "4":
    P("  *** MUTATE=4: the source is given the host's membership (n = 1 for baryons inside a host): dust(host) = 0 ***")
    h1_vals = [0.0 for _ in tab]
else:
    h1_vals = [max(v["amp_F"], v["count"]) for v in tab.values()]
h1_pass = all(v <= 0.10 for v in h1_vals)
R.check("H1 created dust in a satellite inside a host <= 0.10 of the isolated amount (every row, amplitude and count)", h1_pass,
        "; ".join(f"{k.split(' (')[0]}: amp {v['amp_F']:.2f}, count {v['count']:.2f}" for k, v in tab.items()) + ("  [MUTATE=4: label]" if MUT == "4" else ""), kind="result")

R.banner("H2 (accreted): do the already-turned-around baryons create more when they fall through the host?")
P("  The single-stream tangent integration above stops at the first caustic (A -> infinity: its crossing counts are lower bounds), so the multi-crossing multiplicity is taken from the")
P("  G0-b shell toy (CFG243_g0_legality_posthoc_results.json): the median number of downward theta_b crossings per inner shell over 13.8 Gyr.")
gj = os.path.join(C.HERE, "CFG243_g0_legality_posthoc_results.json")
if os.path.exists(gj):
    mcross = json.load(open(gj))["numbers"]["G0ab"]["1e+10"]["med_cross"]["0.05"]
else:
    mcross = float("nan")
extraU = mcross - 1.0
P(f"  unflagged (U): a baryon element that already turned around fires again at each later downward crossing: median {mcross:.1f} crossings, i.e. {extraU:.1f} times the first-crossing dust created again; "
  f"flagged (F): 0 by the flag (a prescribed label: CFG48 G3 PARTIAL)")
R.num("H2", dict(median_crossings=mcross, extra_over_first=extraU))
h2_U = extraU <= 0.10
R.check("H2 the unflagged source creates nothing further for baryons that already turned around (<= 0.10 of the first-crossing dust)", h2_U,
        f"{extraU:.1f} of the first-crossing dust (from the G0-b multiplicity)", kind="result")
R.check("H2F the flagged source creates nothing further (0 by construction)", True, "F: prescribed label, not derived", kind="result")
P("  The satellite keeps what it owned: the dust is conserved, so 'keeps >= 0.90' is the conservation of the created component (tidal stripping of the dust "
  "is not computed here; reported as not covered).")

R.banner("H3 (top-level, not bottom-level ownership): excursion-set first-crossing mass for baryons in a 1e12 Msun system turning around at z = 0")
c = C.class_cosmo([0])
Mg = np.geomspace(1e5, 1e15, 161)
ks, D2 = C.delta2(c, 0, "d_m")
sig = np.array([C.sigma_R(ks, D2, C.R_of_M(M)) for M in Mg])
S_ = sig ** 2
iM = int(np.argmin(np.abs(np.log(Mg / 1e12))))
dta0 = C.DELTA_TA_FROZEN[0]
res3 = {}
for Mmin in (1e5, 1e6, 1e7):
    sel = (Mg >= Mmin * 0.999) & (np.arange(len(Mg)) >= iM)
    Sg = S_[::-1][::-1]
    idx = np.where((np.arange(len(Mg)) >= 0) & (Mg <= 1e12 + 1) & (Mg >= Mmin * 0.999))[0]   # smaller masses = larger S
    idx = idx[::-1]                       # from M_final downward in mass (S increasing)
    Sg = S_[idx]
    dS = np.diff(Sg)
    nw = 20000
    steps = rng.standard_normal((nw, len(dS))) * np.sqrt(dS)[None]
    walk = dta0 + np.concatenate([np.zeros((nw, 1)), np.cumsum(steps, axis=1)], axis=1)
    amax = np.argmax(walk, axis=1)
    Mfc = Mg[idx][amax]
    frac = float(np.mean(Mfc >= 0.1 * 1e12))
    # amplitude Q ~ a0/(3 g_loc), g_loc = G M/r_ta^2 at the system's own turnaround (mean density contrast delta_ta, background rho_m(a))
    Lc = C.load_c7().LCDM
    zfc = np.zeros(len(Mfc))
    Dmax = walk[np.arange(nw), amax]
    Dz = np.clip(C.DELTA_TA_FROZEN[10] / np.maximum(Dmax, 1e-9), 1e-3, 1.0)          # D(z)/D(0) at the earliest turnaround (EdS threshold at high z)
    afc = np.interp(Dz, [float(Lc.D(a)) for a in np.geomspace(0.01, 1, 200)], np.geomspace(0.01, 1, 200))
    one_d = np.array([float(Lc.one_plus_delta_ta(a)) for a in afc])
    rho_m = C.OMEGA_M * C.RHOC0_KPC / afc ** 3
    r_ta = (3.0 * Mfc / (4 * math.pi * rho_m * one_d)) ** (1.0 / 3.0)
    g = G * Mfc / r_ta ** 2
    Q = A0 / (3.0 * g)
    r_ta_f = (3.0 * 1e12 / (4 * math.pi * C.OMEGA_M * C.RHOC0_KPC * float(Lc.one_plus_delta_ta(1.0)))) ** (1.0 / 3.0)
    Qf = A0 / (3.0 * G * 1e12 / r_ta_f ** 2)
    res3[Mmin] = dict(frac_top=frac, med_Mfc=float(np.median(Mfc)), p10=float(np.percentile(Mfc, 10)), p90=float(np.percentile(Mfc, 90)),
                      med_zfc=float(np.median(1.0 / afc - 1)), Qratio_mean=float(np.mean(Q) / Qf))
    P(f"  M_min = {Mmin:.0e}: fraction with M_fc >= 0.1 M_final = {frac:.4f}; median M_fc = {res3[Mmin]['med_Mfc']:.3g} (p10 {res3[Mmin]['p10']:.3g}, p90 {res3[Mmin]['p90']:.3g}) Msun; "
      f"median earliest-turnaround z = {res3[Mmin]['med_zfc']:.1f}; mean Q(M_fc)/Q(M_final) = {res3[Mmin]['Qratio_mean']:.3g}")
R.num("H3", res3)
h3_pass = res3[1e5]["frac_top"] >= 0.9
R.check("H3 >= 90% of the baryons first turn around inside a system of >= 0.1 of the final mass (top-level, not bottom-level, ownership)", h3_pass,
        f"{res3[1e5]['frac_top']:.4f} (M_min 1e5); {res3[1e6]['frac_top']:.4f} (1e6); {res3[1e7]['frac_top']:.4f} (1e7)", kind="result")
P("  H4 (status of the flag): n is an advected scalar with a first-order transport equation along u_b (causal), initialised to 0 at the start and set at the first "
  "theta_b crossing of each baryon element.  Inside an action it is a history variable: CFG48 G3 FAIL (advanced dependence 8.5e-4 and 1.7e-2). As a prescribed advected label: "
  "CFG48 G3 PARTIAL (a postulate, ownership as initial data).  It is not derived from the baryon state.")

R.banner("HIERARCHY verdict")
P(f"  H1 {'PASS' if h1_pass else 'FAIL'}; H2 (unflagged) {'PASS' if h2_U else 'FAIL'}, (flagged) PASS as a label; H3 {'PASS' if h3_pass else 'FAIL'}")
R.verdict("HIERARCHY (post hoc)", "PASS" if (h1_pass and h3_pass) else "FAIL",
          f"H1 {'PASS' if h1_pass else 'FAIL'} (unflagged); H2 unflagged {'PASS' if h2_U else 'FAIL'}, flagged PASS only as a prescribed label; H3 {'PASS' if h3_pass else 'FAIL'}")

if MUT == "4":
    mc = R.main_cells()
    R.finish([mc.get("H1 created dust in a satellite inside a host <= 0.10 of the isolated amount (every row, amplitude and count)") is False, h1_pass])
else:
    R.finish()
