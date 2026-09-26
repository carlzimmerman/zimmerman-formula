#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L377 -- THE FULL CONSTRUCTION IN THE PARTICLE-MESH COSMOLOGY: the switched phantom sourced by the baryons, felt by the
baryons, and read by the carrier's trigger -- does the virialization-triggered carrier's window survive?

WHY.  L365-L369 ran the carrier in a NEWTONIAN particle-mesh cosmology with the least-trigger estimate x~ >= (3/2) Omega_m(a)
delta_matter (L357/L365's own words): the geometric switch variable x~ = 9(R3 + sigma^2)/(4K^2) of C-H/K's CMC-stiff
foliation (K = 3H) has R3 = 16 pi G rho_dyn with rho_dyn the PHANTOM-INCLUSIVE density (L342).  The phantom only adds
decays.  Inside galaxies that can only help (L376), but around clusters it lowers the carrier's retention, and the window's
X-COP margin is thin (median 0.32 against 0.286, L366).  The baryons' own MOND boost inside bound regions was also never
modelled.  This lane puts both in.

THE CONSTRUCTION ON THE MESH (one realisation, L366's box and seeds (7, 11), 100 Mpc/h, 256^3, 192^3 per species):
  * the kernel reads the BARYONS' Newtonian field only (kernel-invisible carrier, L353): g_N,b = -(1/a) grad phi_b with
    lap phi_b = (3/2) Omega_m delta_b / a (the code's own normalisation, peculiar field, as Llinares/Angus);
  * L359's vacuum-gated switch, the p = 2, x_c0 = 2 cell: f = Theta(u - 2), u = x~_m [Omega_L(a)/Omega_L0]^2, with x~_m the
    matter-only switch variable (the lower branch of L342's bistability, stated);
  * L340's monotone kernel nu_mono (L352's table, rebuilt identically and checked): the phantom field is the curl-free
    part of f (nu - 1) g_N,b (QUMOND): lap Phi_ph = -a div[f (nu - 1) g_N,b]; the phantom's switch edge is Gauss-
    compensated automatically (the divergence of the truncated field, L352);
  * baryons feel grad(phi + Phi_ph); the carrier feels grad(phi) only (L353's reciprocity);
  * the trigger reads the geometric variable x~ = (3/2) Omega_m(a) (delta_matter + delta_ph), delta_ph = -(2a^2/(3 Omega_m))
    div[f (nu - 1) g_N,b] (the shear, which only adds, still dropped); decay at Gamma = 10 H above x_c = 5, kick v_k (L365).
RUNS: LCDM (no phantom, no decay); the phantom with no decay (the boost's own effect); the full construction at v_k = 600,
625, 650, 675, 700 km/s (canonical a_0) and 625, 650, 675 (alternative a_0); the trigger-only variant at 650 (phantom in
the trigger, baryons Newtonian).  Gates exactly as L366/L367/L369 compute them (S_8, forest, clearing, two-sided X-COP,
cosmic shear with the p = 2 cell); KiDS is not re-scored here (L375: resolved retention passes, and the phantom-inclusive
trigger only lowers retention).
PRE-DECLARED (before the run): H: at every kick 600-700 km/s (canonical footing) the phantom-inclusive construction LOWERS
the median cluster retention below L369's Newtonian value for the same realisation (seeds (7, 11)): the least-trigger
estimate overstated cluster retention.
HISTORY.  The first design of this lane asked whether the seed-(7, 11) window survives the phantom.  L369 then showed that
window is a one-realisation artefact (no pooled window over three boxes), so the design was changed BEFORE any main-run
result was seen: the main run was stopped 80 s in, and the first design's control run (v_k = 0) was not used.  The lane now
measures the phantom's DIFFERENTIAL effect on every gate at fixed seeds (the difference is far less noisy than the absolute
gates), against L369's matched Newtonian runs.
CHECKS
  C1 CONTROL: the no-phantom LCDM run reproduces L366's committed LCDM sigma_8 exactly (same code path, same seeds).
  C2 CONTROL: the rebuilt nu_mono table equals L352's nu_vec (loaded unedited) at 60 test points.
  C3 CONTROL (the mesh QUMOND, signs and units): an isolated spherical baryon blob inside a switched sphere gives
     |g_N + g_ph| = nu_mono(g_N/a_0) g_N to within 10% at r = 1, 2, 3 Mpc/h (spherical symmetry makes QUMOND's projection
     exact; the switch edge's compensation leaves the interior field untouched).
  R1 = H.  W (informational): the gate table and each gate's shift against L369 (S_8, forest, clearing, X-COP, shear), the
     phantom's own effect without decay, the trigger-only split, both footings, and an ESTIMATE of the pooled three-box
     gates with the seed-(7, 11) shifts applied to L369's pooled values (labelled as an estimate, not a run).
MUTATE=1: the phantom is switched off in the canonical kicked runs (they become L369's Newtonian runs): the shifts vanish and
R1 must FAIL (rc = 1).
L377_POOL sets the pool size (default 6).

Run from the repository root:  python3 real_research/dark_sector_2026/L377_full_construction_pm.py
"""
import os, sys, json, math, time, io, contextlib, tempfile, shutil
import numpy as np
from multiprocessing import Pool
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import L366_triggered_carrier_cluster_retention as L6           # noqa: E402  (L366's construction and code, unchanged)
import L367_triggered_carrier_cosmic_shear as L7                # noqa: E402

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L377_full_construction_pm"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L377", "mutate": MUTATE, "checks": {}, "numbers": {}}
EXPECT_LOWER = True                                              # H, set before the run (see HISTORY)


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


L2 = L6.L2
Om, Hnorm, Om_a, ZI, h = L6.Om, L6.Hnorm, L6.Om_a, L6.ZI, L6.h
OL = 1 - Om
WB, WC, LBOX, NG, NP, RHO_M = L6.WB, L6.WC, L6.LBOX, L6.NG, L6.NP, L6.RHO_M
KG = L7.KG
ACC_UNIT = 1e5 * (100e3 * h / 3.0857e22)                         # m/s^2 per code unit ((100 km/s) x H0)
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
X_C0, P_GATE, XC_TRIG = 2.0, 2, 5.0                              # L359's p = 2 switch cell; L365's trigger

# ---------------------------------------------------------------------------------- L352's nu_mono table, same construction
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)


def dh_rar(y, e=1e-6):
    return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)


YP = brentq(lambda y: float(dh_rar(y)), 1, 5); HP = float(h_rar(YP))
LYG = np.linspace(-14, 14, 280001); YG = 10 ** LYG; DH = np.maximum(dh_rar(YG), 0.05 * HP / (YG + YP))
HM = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH[1:] + DH[:-1]) * np.diff(YG))])


def nu_vec(y):
    y = np.maximum(np.asarray(y, float), 1e-14)
    return 1.0 + np.interp(np.log10(y), LYG, HM) / y


def phantom(s, rb, rho, a, a0c, on=True):
    """the switched QUMOND phantom of the baryons: returns (Phi_ph, delta_ph, switched fraction)."""
    gate = (OL / (Om * a ** -3 + OL) / OL) ** P_GATE
    f = (1.5 * Om_a(a) * (rho - 1.0) * gate > X_C0) if on else np.ones_like(rho, bool)
    if not f.any():
        return None, None, 0.0
    gb = [-(1.0 / a) * g for g in s.grad(s.poisson(1.5 * Om * (rb - WB) / a))]
    nu1 = nu_vec(np.sqrt(gb[0] ** 2 + gb[1] ** 2 + gb[2] ** 2) / a0c) - 1.0
    w = [np.where(f, nu1 * g, 0.0) for g in gb]
    divw = s.div(w)
    return s.poisson(-a * divw), -(2 * a * a / (3 * Om)) * divw, float(f.mean())


def run(cfg):
    """L369's run (L366/L367's construction) with the phantom: mode 'none' | 'full' | 'trigger'."""
    name, sp, sk, xc, vk, gamma, tmp, mode, a0 = cfg
    a0c = a0 / ACC_UNIT
    s = L2.Sim(LBOX, NG, NP)
    s.deposit = lambda x, w: L6.deposit_fast(s, x, w)
    rng = np.random.default_rng(sp)
    kk = np.sqrt(s.K2); kk[0, 0, 0] = s.kf
    Pk = np.vectorize(lambda q: L2.P_lin(q, ZI))(np.clip(kk, s.kf, 60.0)); Pk[0, 0, 0] = 0
    white = np.fft.fftn(rng.normal(size=(NG, NG, NG)))
    delta0 = np.real(np.fft.ifftn(white * np.sqrt(Pk * NG ** 3 / LBOX ** 3)))
    psi = [-gg for gg in s.grad(s.poisson(delta0))]
    q = (np.arange(NP) + 0.5) * LBOX / NP
    QX, QY, QZ = np.meshgrid(q, q, q, indexing='ij'); Q = np.stack([QX.ravel(), QY.ravel(), QZ.ravel()], 1)
    disp = np.stack([s.interp(pp, Q) for pp in psi], 1)
    del QX, QY, QZ, psi, white, delta0, Pk, kk
    ai = 1 / (1 + ZI); fg = Om_a(ai) ** 0.55
    xb = (Q + disp) % LBOX; pb = ai ** 2 * Hnorm(ai) * fg * disp
    del Q, disp
    xcar, pcar = xb.copy(), pb.copy()
    n = len(xb); cold = np.ones(n, bool)
    krng = np.random.default_rng(sk)
    diag = {}

    def fields(xb, xcar, a):
        rb = s.deposit(xb, np.full(n, WB)) * NG ** 3 / n
        rho = rb + s.deposit(xcar, np.full(n, WC)) * NG ** 3 / n
        ph = phantom(s, rb, rho, a, a0c) if mode != "none" else (None, None, 0.0)
        return rho, ph

    def accel(rho, ph, a):
        gr = s.grad(s.poisson(1.5 * Om * (rho - 1.0) / a))
        ab = -np.stack([s.interp(gg, xb) for gg in gr], 1)
        if mode == "full" and ph[0] is not None:
            ab -= np.stack([s.interp(gg, xb) for gg in s.grad(ph[0])], 1)
        return ab, -np.stack([s.interp(gg, xcar) for gg in gr], 1)

    a = ai; dlna = 0.02; zs = [3.0, 2.0, 0.5, 0.3, 0.0]; out = {}
    rho, ph = fields(xb, xcar, a); ab, ac = accel(rho, ph, a)
    while zs:
        da = a * (np.exp(dlna) - 1); dt = da / (a * Hnorm(a))
        pb += 0.5 * dt * ab; pcar += 0.5 * dt * ac
        xb = (xb + dt * pb / a ** 2) % LBOX; xcar = (xcar + dt * pcar / a ** 2) % LBOX
        a = a + da
        rho, ph = fields(xb, xcar, a)
        if gamma > 0 and cold.any():                                   # L365's trigger on the geometric x~
            xt = 1.5 * Om_a(a) * (rho - 1.0)
            if mode in ("full", "trigger") and ph[1] is not None:
                xt = xt + 1.5 * Om_a(a) * ph[1]
            idx = np.where(cold)[0]
            xp = s.interp(xt, xcar[idx])
            hit = idx[(xp > xc) & (krng.random(len(idx)) < 1 - math.exp(-gamma * Hnorm(a) * dt))]
            if len(hit):
                nh = krng.normal(size=(len(hit), 3)); nh /= np.linalg.norm(nh, axis=1)[:, None]
                pcar[hit] += a * (vk / 100.0) * nh
                cold[hit] = False
        ab, ac = accel(rho, ph, a)
        pb += 0.5 * dt * ab; pcar += 0.5 * dt * ac
        for z in list(zs):
            if 1 / a - 1 <= z + 1e-9:
                rec = {"decayed": float(1 - cold.mean()), "switched": ph[2]}
                if ph[1] is not None:
                    rec["phantom_mass_frac"] = float(np.clip(ph[1], 0, None).sum() / NG ** 3)
                if z >= 2.0:
                    kpar, p1d = s.flux_p1d(xb, pb, a, z)
                    rec.update(kpar=kpar.tolist(), p1d=p1d.tolist())
                    rhoc2 = s.deposit(xcar, np.full(n, 1.0)) * NG ** 3 / n
                    dense = rho > 50.0
                    rec["carrier_in_dense"] = float(rhoc2[dense].sum() / max(rho[dense].sum(), 1e-30))
                elif z == 0.5:
                    rec["pk"] = L7.pk_bins(s, rho - 1.0)
                else:
                    if z == 0.0:
                        rec["sigma8"] = L6.sigma8(s, rho - 1.0)
                    rhoc = s.deposit(xcar, np.full(n, WC)) * NG ** 3 / n
                    np.save(os.path.join(tmp, f"{name}_z{z}_rho.npy"), rho.astype(np.float32))
                    np.save(os.path.join(tmp, f"{name}_z{z}_rhoc.npy"), rhoc.astype(np.float32))
                out[str(z)] = rec; zs.remove(z)
    return name, out


def c3_blob():
    """C3: an isolated spherical baryon blob inside a switched sphere; the mesh phantom must return nu g_N radially."""
    Lb, Nb = 40.0, 128
    s = L2.Sim(Lb, Nb, 8)
    g = (np.arange(Nb) + 0.5) * s.d - Lb / 2
    X, Y, Z = np.meshgrid(g, g, g, indexing='ij'); R = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    Mb, sig = 1e13, 0.3                                           # Msun/h, Mpc/h
    blob = Mb * np.exp(-0.5 * (R / sig) ** 2); blob *= Mb / blob.sum()
    rb = WB + blob / (RHO_M * s.d ** 3)                           # baryon density in units of rho_bar_m (mean WB + blob)
    rb -= (rb.mean() - WB)
    a0c = A0["canonical"] / ACC_UNIT; a = 1.0
    gb = [-(1.0 / a) * gg for gg in s.grad(s.poisson(1.5 * Om * (rb - WB) / a))]
    f = R < 6.0
    nu1 = nu_vec(np.sqrt(gb[0] ** 2 + gb[1] ** 2 + gb[2] ** 2) / a0c) - 1.0
    w = [np.where(f, nu1 * gg, 0.0) for gg in gb]
    Phi = s.poisson(-a * s.div(w))
    gp = [-(1.0 / a) * gg for gg in s.grad(Phi)]
    res = []
    for rq in (1.0, 2.0, 3.0):
        vals = []
        for ax in range(3):
            for sgn in (1, -1):
                idx = [Nb // 2] * 3; idx[ax] = Nb // 2 + sgn * int(round(rq / s.d)) - (1 if sgn < 0 else 0)
                i = tuple(idx); rr_ = R[i]
                gN = abs(gb[ax][i]); gT = abs(gb[ax][i] + gp[ax][i])
                vals.append(gT / (nu_vec(gN / a0c) * gN))
        i1 = (Nb // 2 + int(round(rq / s.d)), Nb // 2, Nb // 2)
        gN_an = 1.5 * Om / (4 * math.pi * RHO_M) * Mb / R[i1] ** 2     # G M / r^2 in code units, at the cell's own radius
        res.append(dict(r=rq, ratio=float(np.mean(vals)), gN_mesh_over_analytic=float(abs(gb[0][i1]) / gN_an)))
    return res


if __name__ == "__main__":
    P(__doc__)
    banner("C2, C3  CONTROLS ON THE KERNEL AND THE MESH QUMOND")
    P60 = os.path.join(REPO, "real_research", "g03_audit_2026", "L360_assembled_construction_kids.py")
    N60 = {"__name__": "l360", "__file__": P60}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open(P60).read().split("BASE = {")[0], N60)
    yt = np.geomspace(1e-6, 1e3, 60)
    d2 = float(np.max(np.abs(nu_vec(yt) / N60["L52"]["nu_vec"](yt) - 1)))
    check("C2 the rebuilt nu_mono table equals L352's nu_vec (loaded unedited) at 60 points", f"max relative deviation {d2:.1e}", d2 < 1e-12)
    c3 = c3_blob()
    for r_ in c3:
        P(f"    r = {r_['r']:.0f} Mpc/h: |g_N + g_ph| / (nu g_N) = {r_['ratio']:.3f};  mesh g_N / (G M / r^2) = {r_['gN_mesh_over_analytic']:.3f}")
    check("C3 the mesh QUMOND returns nu_mono(g_N/a_0) g_N for a spherical baryon blob in a switched sphere (within 10% at "
          "r = 1, 2, 3 Mpc/h) and the mesh g_N matches G M/r^2 (within 10%): signs and units", f"{c3}",
          all(abs(r_["ratio"] - 1) < 0.10 and abs(r_["gN_mesh_over_analytic"] - 1) < 0.10 for r_ in c3))
    OUT["numbers"]["C3"] = c3

    NPOOL = int(os.environ.get("L377_POOL", "6"))
    TMP = tempfile.mkdtemp(prefix="L377_")
    SP, SK = 7, 11
    cfgs = [("lcdm", SP, SK, float("inf"), 0.0, 0.0, TMP, "none", A0["canonical"]),
            ("ph_nodecay", SP, SK, float("inf"), 0.0, 0.0, TMP, "full", A0["canonical"])]
    VKC, VKA = (600.0, 625.0, 650.0, 675.0, 700.0), (625.0, 650.0, 675.0)
    SRC = {}                                                       # display name -> run name
    if MUTATE:                                                     # the phantom off: the kicked runs become L369's
        P("  MUTATE: the phantom is switched off in the canonical kicked runs")
        cfgs = cfgs[:1] + [(f"full_can_v{int(v)}", SP, SK, XC_TRIG, v, 10.0, TMP, "none", A0["canonical"]) for v in VKC]
        SRC.update({c_[0]: c_[0] for c_ in cfgs[1:]})
    else:
        cfgs += [(f"full_can_v{int(v)}", SP, SK, XC_TRIG, v, 10.0, TMP, "full", A0["canonical"]) for v in VKC]
        cfgs += [(f"full_alt_v{int(v)}", SP, SK, XC_TRIG, v, 10.0, TMP, "full", A0["alt"]) for v in VKA]
        cfgs.append(("trig_can_v650", SP, SK, XC_TRIG, 650.0, 10.0, TMP, "trigger", A0["canonical"]))
        SRC.update({c_[0]: c_[0] for c_ in cfgs[1:]})
    P(f"  {len(cfgs)} runs, pool {NPOOL}")
    with Pool(NPOOL) as pool:
        res = dict(pool.map(run, cfgs, chunksize=1))
    P(f"  {len(cfgs)} runs done in {time.time() - T0:.0f}s")

    banner("C1  CONTROL: the no-phantom LCDM run reproduces L366")
    R66 = json.load(open(os.path.join(HERE, "L366_triggered_carrier_cluster_retention_results.json")))["numbers"]
    d1 = abs(res["lcdm"]["0.0"]["sigma8"] / R66["runs"]["lcdm"]["0.0"]["sigma8"] - 1)
    check("C1 the no-phantom LCDM run reproduces L366's committed LCDM sigma_8 (same code path, same seeds)", f"relative deviation {d1:.1e}", d1 < 1e-9)

    # ------------------------------------------------------------------------------ gates, exactly as L366/L367/L369
    TM = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L364_replacement_carrier_cosmic_shear_results.json")))["numbers"]["T_max"]
    est = L6.eps_bounds(); lo = max(v[0] for v in est.values()); hi = min(v[1] for v in est.values())
    s = L2.Sim(LBOX, NG, NP)
    ld = lambda nm, z, f: np.load(os.path.join(TMP, f"{nm}_z{z}_{f}.npy")).astype(float)
    rho_l, rc_l = ld("lcdm", 0.0, "rho"), ld("lcdm", 0.0, "rhoc")
    pk = L6.peaks(s, rho_l)
    Mh = np.array([L6.sphere_sum(s, rho_l, p_, 1.0) * RHO_M for p_ in pk]); sel = Mh >= 1e14
    Mc_l = np.array([L6.sphere_sum(s, rc_l, p_, 1.0) for p_ in pk])
    TAB = {}
    for nm, src in SRC.items():
        r_ = res[src]; L_ = res["lcdm"]
        s8 = r_["0.0"]["sigma8"] / L_["0.0"]["sigma8"]
        fdev = 0.0
        for z in ("3.0", "2.0"):
            kp = np.array(L_[z]["kpar"]); rr = np.array(r_[z]["p1d"]) / np.array(L_[z]["p1d"])
            m = (kp >= 0.2) & (kp <= 2.0); fdev = max(fdev, float(np.max(np.abs(rr[m] - 1))))
        g3 = r_["2.0"]["carrier_in_dense"] / max(L_["2.0"]["carrier_in_dense"], 1e-30)
        eps = np.array([L6.sphere_sum(s, ld(src, 0.0, "rhoc"), p_, 1.0) for p_ in pk]) / Mc_l
        med = float(np.median(eps[sel]))
        T = {q: math.sqrt(r_["0.5"]["pk"][q] / L_["0.5"]["pk"][q]) for q in KG}
        sh = all(T[q] <= TM[f"p=2, x_c0=2.0/{f_}"][str(q)] for q in KG for f_ in ("canonical", "alt"))
        g = dict(S8=s8, forest=fdev, G3=g3, eps_cl=med, T=T, shear=bool(sh), switched_z0=r_["0.0"]["switched"],
                 decayed_z0=r_["0.0"]["decayed"], phantom_mass_frac_z0=r_["0.0"].get("phantom_mass_frac"))
        g["full"] = bool(s8 >= 0.922 and fdev <= 0.10 and (g3 <= 0.30 or nm == "ph_nodecay") and lo <= med <= hi and sh)
        TAB[nm] = g
        P(f"    {nm:15s}: S8 {s8:.3f} | forest {fdev:.3f} | cleared {g3:.2f}{'' if g3 <= 0.3 else ' X'} | X-COP eps {med:.2f}"
          f"{'' if lo <= med <= hi else (' UNDER' if med < lo else ' OVER')} | shear {'ok' if sh else 'X'} (T(1) {T[1.0]:.3f}) | "
          f"switched {g['switched_z0']:.3f}, decayed {g['decayed_z0']:.2f}  =>  {'ALL PASS' if g['full'] else 'no'}")
    shutil.rmtree(TMP, ignore_errors=True)
    OUT["numbers"].update(table=TAB, eps_bounds=dict(lo=lo, hi=hi), n_clusters=int(sel.sum()))
    check("W (informational) the gate table: the phantom's own effect, the full construction on both footings, trigger-only",
          "see table", True, "reported either way", load_bearing=False)

    banner("SHIFTS AGAINST L369's MATCHED NEWTONIAN RUNS (same seeds), AND A POOLED ESTIMATE")
    R69 = json.load(open(os.path.join(HERE, "L369_triggered_carrier_window_realisations_results.json")))["numbers"]
    T7, TP = R69["table"]["7"], R69["table"]["pooled"]
    SH = {}
    for v in VKC:
        t = f"v{int(v)}"; g, n7 = TAB[f"full_can_{t}"], T7[t]
        SH[t] = dict(d_eps=g["eps_cl"] - n7["eps_cl"], r_eps=g["eps_cl"] / n7["eps_cl"], d_G3=g["G3"] - n7["G3"],
                     r_S8=g["S8"] / n7["S8"], d_forest=g["forest"] - n7["forest"])
        est_ = dict(S8=TP[t]["S8"] * SH[t]["r_S8"], G3=TP[t]["G3"] + SH[t]["d_G3"], eps=TP[t]["eps_cl"] * SH[t]["r_eps"])
        est_["window_estimate"] = bool(est_["S8"] >= 0.922 and est_["G3"] <= 0.30 and lo <= est_["eps"] <= hi and TP[t]["forest"] <= 0.10)
        SH[t]["pooled_estimate"] = est_
        P(f"    {t}: X-COP eps {n7['eps_cl']:.3f} -> {g['eps_cl']:.3f} (x{SH[t]['r_eps']:.3f}) | cleared {n7['G3']:.3f} -> {g['G3']:.3f} | "
          f"S8 {n7['S8']:.3f} -> {g['S8']:.3f} | forest {n7['forest']:.3f} -> {g['forest']:.3f}   ||  pooled ESTIMATE: S8 {est_['S8']:.3f}, "
          f"cleared {est_['G3']:.2f}, eps {est_['eps']:.2f} -> {'window' if est_['window_estimate'] else 'no'}")
    OUT["numbers"]["shifts"] = SH

    banner("R1  THE HYPOTHESIS (set before the run; see HISTORY)")
    win = [nm for nm in TAB if nm.startswith("full_can") and TAB[nm]["full"]]
    check("R1 = H: at every kick 600-700 km/s the phantom-inclusive construction lowers the median cluster retention below "
          "L369's Newtonian value for the same seeds", "; ".join(f"{t}: {d['d_eps']:+.3f}" for t, d in SH.items()),
          all(d["d_eps"] < 0 for d in SH.values()) == EXPECT_LOWER)

    banner("VERDICT")
    P(f"""  Full construction on the mesh (switched nu_mono phantom from the baryons, felt by the baryons, read by the trigger):
  seed-(7, 11) window {win or 'none'} (one realisation -- L369: such windows do not survive pooling); pooled estimate with the
  shifts applied: {[t for t, d in SH.items() if d['pooled_estimate']['window_estimate']] or 'none'}.  LIMITS: one realisation, 0.39 Mpc/h mesh (galaxy phantoms sub-cell), the switch on the
  matter-only branch, the shear dropped from x~, the trigger posited (no action).""")

    n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
    json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
    sys.exit(0 if n_fail == 0 else 1)
