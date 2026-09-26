#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L373 -- L372's TWO-MODE CARRIER IN THE PARTICLE-MESH COSMOLOGY (the full construction, three realisations pooled): does the
carrier that passes Harvey and X-COP in the static machinery survive real assembly histories?

WHY.  L372 found a two-mode carrier passing forest, S_8, X-COP, galaxies, KiDS and Harvey on the alternative threshold set:
  U  a spatially uniform late decay, Gamma_U = Gamma_0 [Omega_L(a)/Omega_L,0]^2 (L319's law), f_U(0) = 0.25, daughters at
     v_U = 3000 km/s -- it depletes every host by nearly the same fraction and keeps its cusp (X-COP);
  G  a vacuum-gated density-triggered decay with a SLOW kick v_G = 750-1050 km/s -- galaxies lose their daughters, groups and
     clusters recapture theirs (Harvey).
  but with L357/L321's STATIC full-depth retention.  L366/L369 showed that assembly history can overturn the static proxy,
  and that a single box is not enough (L369: L366's window was a one-realisation artefact).  This lane runs both modes in the
  record's most complete particle-mesh construction, on the record's three realisations.
WHAT THE CARRIER IS.  The mesh follows the carrier with tracer points, exactly as it follows the baryons, and cannot tell a
  particle species from a field state: every gate below reads only where the mass is.  On the record's no-particle reading
  (the ghost-condensate thread: one scalar whose Y-mode gives a_0 and whose Q-mode is a cold a^-3 dust -- the CMB constrains a
  fluid, not a particle) the carrier is that dust, and the two modes are the dust being heated as the vacuum takes over (both
  rates scale with Omega_L(a)).  Here the heating is put in by hand; no action produces it yet, and the reading keeps the
  record's two liabilities of the mode: the w_0 squeeze, and caustics (a single-valued flow cannot multistream as these
  tracers do).

METHOD.  L377's run() (the full construction: the switched nu_mono QUMOND phantom sourced by the baryons and felt by them,
  L359's p = 2 switch, the phantom-inclusive trigger, the carrier Newtonian per L353), copied with three changes:
  * mode U: every cold carrier particle decays with probability 1 - exp(-Gamma_U(a) dt) (Gamma_0 set so that 1 - S(today) =
    f_U(0)), kicked isotropically by v_U = 3000 km/s;
  * mode G: L377's trigger x~ > x_c = 5 is GATED by the vacuum as in L357/L372: x_c,eff(a) = x_c [Omega_L,0/Omega_L(a)]^2,
    rate 10 H, slow kick v_G.  The 0.39 Mpc/h mesh cannot resolve L357's x_v0 = 1000-2000 thresholds; x_c = 5 is the record's
    mesh proxy for the trigger (L365/L366), so G here is the mesh transcription of L372's G, as L366 transcribed L365;
  * a z = 0.4 snapshot (Harvey's epoch); densities saved at z = 2 (L379's fixed cells), 0.4 and 0 (L377's z = 0.3 snapshot
    is not needed and is dropped; the step sequence is unchanged).
  Seeds (7, 11), (17, 21), (29, 33) as L369/L378; canonical a_0.  Cells per realisation: LCDM, and the two-mode carrier at
  f_U(0) = 0.25 with v_G = 750, 900, 1050 km/s, and f_U(0) = 0.20 and 0.30 at 900 km/s (L372: 0.20 fails X-COP, 0.30 the
  conservative S_8 bound; the mesh computes S_8 with both kicks and the real decay times directly).
GATES (pre-declared; L378's arithmetic where it exists, pooled over the three realisations):
  S_8       mean sigma_8 ratio to the matched LCDM run >= 0.922 (strict) / 0.899 (alternative);
  forest    summed flux P1D, max |ratio - 1| on k_par 0.2-2 h/Mpc at z = 3 and 2 <= 0.10;
  X-COP     median carrier retention inside 1 Mpc/h of all >= 1e14 Msun/h halos at z = 0 inside L354's two-sided bounds;
  shear     L364's p = 2 transfer ceilings at z = 0.5 (both footings);
  Harvey    run on every pooled cell passing X-COP (the pincer's other side), with the group retention MEASURED at z = 0.4
            (pooled medians inside 1 Mpc/h of LCDM's peaks with M(<1 Mpc/h) in 5e13-1e14 and 1.5e14-3e14 Msun/h for the 1e14
            and 3e14 Msun substructures, >= 3e14 for the main cluster) through L371's machinery with its two core shapes S1
            (the cusp, scaled) and S2 (phase-mixed daughters at v_G): population-mean excess beta <= +0.10 (Harvey's -0.04 +
            2 x 0.07, as L372) on all three estimators, both shapes.
  REPORTED, NOT GATED: the z = 2 dense-cell clearing, as the record's G3 and on L379's fixed cells (LCDM's dense cells) -- the
  vacuum gate keeps high-z halos by design (L357's stated price: RC100 and the flagship); galaxies and KiDS lie below the mesh
  (L372's static values).
CHECKS
  C1 CONTROL: the (7, 11) LCDM run reproduces L366's committed LCDM sigma_8 exactly (same code path, same seeds).
  C2 CONTROL: the Harvey stage's phantom and lensing-mass solve use the mesh runs' switch cell (p = 2, x_c0 = 2).
  R1 THE WINDOW SURVIVES ASSEMBLY (pre-declared hypothesis: yes): a cell passes S_8 (alternative), forest, X-COP, shear and
     Harvey (both shapes) pooled over the three realisations.
  W  (reported) per-realisation and pooled gate tables; group retention at z = 0.4 and cluster retention at z = 0 against L372's
     static values; G3.
MUTATE=1 switches mode U off in every decaying run: the clusters recapture and X-COP must fail, R1 flips (rc = 1).  As in
  L378, the MUTATE run is made only if R1 passes in the main run.
SCOPE.  The switch cell is L377's (p = 2, x_c0 = 2).  DE1 (c8bb50813) finds this cell fails the flat-a0 flagship at
  M_b = 1e11 on the canonical footing, and the particle-mesh track has moved to p = 1, x_c0 = 2.5 (L388): the verdict here
  holds for the p = 2 cell only.  The mesh and the Harvey stage use DIFFERENT phantom operators even at the matched cell
  (L377: the Newtonian field of all baryons, response masked, background-subtracted gate; L370/L361: each bound region's
  phantom from its own baryons, absolute-density mask) -- the open item 1 of the 2026-09-26 peer review; both are
  recorded in the results.  The Harvey stage carries its matched intact-carrier control (kernel on, carrier intact).
CORRECTION (before any Harvey result).  The first main run's Harvey stage inherited L370's default switch cell with its
  header (SW_DEF = p = 1, x_c0 = 1.5: thresholds 2.32 against the mesh's 4.79 at z = 0.4) in both phantom maps and the
  lensing-mass solve -- the defect that withdrew L381 (flagged by a peer session).  It was stopped 50 minutes into its only
  Harvey cell, before any Harvey number; the mesh runs were kept (checkpoint), the switch cell is now the mesh's (C2), and
  the gates and Harvey were re-scored from the checkpoint (L373_RESUME=1).  The automatic MUTATE run never started.
L373_POOL sets the pool size (default 6; a parallel session shares the machine).  After the mesh runs, their measurements are
  pickled to the system temp directory; L373_RESUME=1 re-scores from that checkpoint without re-running the mesh.  L373_SMOKE=1 is a code test on a 64^3 mesh,
  one realisation, one cell, Harvey forced, nothing written to this directory.

Run from the repository root:  python3 real_research/merger_infall_2026/L373_two_mode_carrier_pm.py
"""
import os, sys, json, math, time, tempfile, shutil, io, contextlib, warnings
import numpy as np
from multiprocessing import Pool
warnings.filterwarnings("ignore", category=RuntimeWarning)

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DS = os.path.join(REPO, "real_research", "dark_sector_2026")
sys.path.insert(0, DS)
import L377_full_construction_pm as L77                        # noqa: E402  (L377's full construction and helpers, unchanged)

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L373_two_mode_carrier_pm"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L373", "mutate": MUTATE, "checks": {}, "numbers": {}}
EXPECT_WINDOW = True                                             # R1, set before the run
L6, L7, L2 = L77.L6, L77.L7, L77.L2
Om, OL, Hnorm, Om_a, ZI, h = L77.Om, L77.OL, L77.Hnorm, L77.Om_a, L77.ZI, L77.h
WB, WC, LBOX, NG, NP, RHO_M, KG = L77.WB, L77.WC, L77.LBOX, L77.NG, L77.NP, L77.RHO_M, L77.KG
SMOKE = os.environ.get("L373_SMOKE", "0") == "1"
SEEDS = ((7, 11),) if SMOKE else ((7, 11), (17, 21), (29, 33))
if SMOKE:
    NG, NP = 64, 48
    L6.NG = NG                                                     # L366's sphere_sum reads its module's NG
V_U, P_U, P_G = 3000.0, 2, 2
CELLS = [(0.25, 900.0)] if SMOKE else [(0.20, 900.0), (0.25, 750.0), (0.25, 900.0), (0.25, 1050.0), (0.30, 900.0)]
TAGS = [f"u{int(round(100 * fu))}_g{int(vg)}" for fu, vg in CELLS]


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 116); P(t); P("=" * 116)


def gamma0_U(fu0):
    """Gamma_0 (code time units, H0 = 1) so that 1 - exp(-Gamma_0 int [Omega_L(a)/Omega_L0]^2 dt) = f_U(0), L319's law."""
    if fu0 <= 0: return 0.0
    a = np.geomspace(1 / (1 + ZI), 1.0, 20001)
    w = ((OL / (Om * a ** -3 + OL)) / OL) ** P_U / (a * Hnorm(a))
    I = float(np.sum(0.5 * (w[1:] + w[:-1]) * np.diff(a)))
    return -math.log(1 - fu0) / I


def run2(cfg):
    """L377's run() with mode U (uniform, v_U), the vacuum gate on mode G's trigger, and a z = 0.4 snapshot."""
    name, sp, sk, xc, vg, gamma, fu0, tmp, mode, a0 = cfg
    a0c = a0 / L77.ACC_UNIT
    g0U = gamma0_U(fu0)
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
    urng = np.random.default_rng(sk + 1000)                           # mode U's own stream (the G stream stays L377's)
    nU = 0

    def fields(xb, xcar, a):
        rb = s.deposit(xb, np.full(n, WB)) * NG ** 3 / n
        rho = rb + s.deposit(xcar, np.full(n, WC)) * NG ** 3 / n
        ph = L77.phantom(s, rb, rho, a, a0c) if mode != "none" else (None, None, 0.0)
        return rho, ph

    def accel(rho, ph, a):
        gr = s.grad(s.poisson(1.5 * Om * (rho - 1.0) / a))
        ab = -np.stack([s.interp(gg, xb) for gg in gr], 1)
        if mode == "full" and ph[0] is not None:
            ab -= np.stack([s.interp(gg, xb) for gg in s.grad(ph[0])], 1)
        return ab, -np.stack([s.interp(gg, xcar) for gg in gr], 1)

    a = ai; dlna = 0.02; zs = [3.0, 2.0, 0.5, 0.4, 0.0]; out = {}
    rho, ph = fields(xb, xcar, a); ab, ac = accel(rho, ph, a)
    while zs:
        da = a * (np.exp(dlna) - 1); dt = da / (a * Hnorm(a))
        pb += 0.5 * dt * ab; pcar += 0.5 * dt * ac
        xb = (xb + dt * pb / a ** 2) % LBOX; xcar = (xcar + dt * pcar / a ** 2) % LBOX
        a = a + da
        rho, ph = fields(xb, xcar, a)
        gate = ((OL / (Om * a ** -3 + OL)) / OL) ** P_G
        if g0U > 0 and cold.any():                                     # mode U: uniform, rate Gamma_0 [Omega_L/Omega_L0]^2
            idx = np.where(cold)[0]
            pU = 1 - math.exp(-g0U * ((OL / (Om * a ** -3 + OL)) / OL) ** P_U * dt)
            hit = idx[urng.random(len(idx)) < pU]
            if len(hit):
                nh = urng.normal(size=(len(hit), 3)); nh /= np.linalg.norm(nh, axis=1)[:, None]
                pcar[hit] += a * (V_U / 100.0) * nh
                cold[hit] = False; nU += len(hit)
        if gamma > 0 and cold.any():                                   # mode G: L377's trigger, gated by the vacuum
            xt = 1.5 * Om_a(a) * (rho - 1.0)
            if mode in ("full", "trigger") and ph[1] is not None:
                xt = xt + 1.5 * Om_a(a) * ph[1]
            idx = np.where(cold)[0]
            xp = s.interp(xt, xcar[idx])
            hit = idx[(xp * gate > xc) & (krng.random(len(idx)) < 1 - math.exp(-gamma * Hnorm(a) * dt))]
            if len(hit):
                nh = krng.normal(size=(len(hit), 3)); nh /= np.linalg.norm(nh, axis=1)[:, None]
                pcar[hit] += a * (vg / 100.0) * nh
                cold[hit] = False
        ab, ac = accel(rho, ph, a)
        pb += 0.5 * dt * ab; pcar += 0.5 * dt * ac
        for z in list(zs):
            if 1 / a - 1 <= z + 1e-9:
                rec = {"decayed": float(1 - cold.mean()), "decayed_U": nU / n, "switched": ph[2]}
                if z >= 2.0:
                    kpar, p1d = s.flux_p1d(xb, pb, a, z)
                    rec.update(kpar=kpar.tolist(), p1d=p1d.tolist())
                    rhoc2 = s.deposit(xcar, np.full(n, 1.0)) * NG ** 3 / n
                    dense = rho > 50.0
                    rec["carrier_in_dense"] = float(rhoc2[dense].sum() / max(rho[dense].sum(), 1e-30))
                    if z == 2.0:                                           # L379's fixed-cell clearing needs the fields
                        np.save(os.path.join(tmp, f"{name}_z2.0_rho.npy"), rho.astype(np.float32))
                        np.save(os.path.join(tmp, f"{name}_z2.0_rhoc.npy"), rhoc2.astype(np.float32))
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


# ================================================================================================ Harvey (L371's machinery)
def harvey_block(EPSM, VKG):
    """L371's machinery, loaded unedited (its functions), with the group retention measured here and the S2 kick = v_G.
    EPSM = {1e14: eps, 3e14: eps, 1e15: eps}.  Returns the population-mean excess beta for shapes S1 and S2."""
    s71 = open(os.path.join(HERE, "L371_harvey_slow_kick_carrier.py")).read()
    s70 = open(os.path.join(HERE, "L370_boosted_infall_mergers.py")).read()
    head70 = s70.split("# ============================================================================================================ C1")[0]
    head70 = head70.replace('P(__doc__.split("CHECKS")[0].strip())', "pass")
    mut, os.environ["MUTATE"] = os.environ.get("MUTATE", "0"), "0"
    G = {"__name__": "l371", "__file__": os.path.join(HERE, "L371_harvey_slow_kick_carrier.py")}
    exec(head70, G); G["MUTATE"] = False
    # the switch cell must be the mesh runs' (L377: p = 2, x_c0 = 2), not L370's default (p = 1, x_c0 = 1.5)
    SWK = f"p{L77.P_GATE:g}_x{L77.X_C0:.1f}"
    assert tuple(G["SWITCH"][SWK]) == (float(L77.P_GATE), float(L77.X_C0)), SWK
    G["SW_DEF"] = SWK
    os.environ["MUTATE"] = mut
    G.update(dict(RealHalo=G["RealHalo"], os=os, json=json, math=math, np=np, time=time, REPO=REPO, HERE=HERE))
    from scipy.optimize import brentq
    from scipy.interpolate import PchipInterpolator
    G.update(brentq=brentq, PchipInterpolator=PchipInterpolator)
    ZH, NH, LH = 0.4, (120 if SMOKE else 400), 10000.0
    GH = G["Grid"](NH, LH); DXH = GH.dx
    G.update(ZH=ZH, NH=NH, LH=LH, GH=GH, DXH=DXH, XSUB=400.0, HARV_BETA=-0.04, HARV_ERR=0.07, FGAS_S=0.10, FSTAR_S=0.02,
             RN=1000.0 / G["h"] / (1 + ZH), VK=VKG, EPS={"med": EPSM})
    exec(s70[s70.index("def centroid(S, x0, y0, Rap, it=12):"):s70.index("HB = []")], G)          # L370's Harvey helpers
    exec(s71[s71.index("def q_static(args):"):s71.index("# ================================================================================================ S2's shape")], G)
    GATES = np.array([25.0, 50.0, 100.0, 150.0, 250.0, 400.0, 700.0, G["RN"]])
    QTAB = {}
    for Ml in (1e14, 3e14, 1e15):
        fg, fs = (0.10, 0.02) if Ml < 1e15 else (0.125, 0.015)
        H0 = G["RealHalo"](Ml, ZH, fg, fs, "intact")
        QTAB[Ml] = (GATES, np.array(G["q_static"]((H0.M200, H0.c, G["cum_mass"](H0.rho_b), GATES))))
    paint_at, centroid, nfw_fit_centre, phantom_felt, m_in = (G[k] for k in ("paint_at", "centroid", "nfw_fit_centre", "phantom_felt", "m_in"))
    A0K, SW_DEF = G["A0K"], G["SW_DEF"]
    CONF = [(Msub, dSG, orient) for Msub in (1e14, 3e14) for dSG in (60.0, 120.0) for orient in ("perp", "toward_main")]
    RES = {}
    for (Msub, dSG, orient) in CONF:
        gx, gy = (400.0, dSG) if orient == "perp" else (400.0 - dSG, 0.0)
        ux, uy = ((0.0, 1.0) if orient == "perp" else (-1.0, 0.0))
        HsL = G["solve_l366"](Msub, "intact", 1.0, None, 0.10, 0.02, kernel=False)
        SL = (paint_at(HsL.rho_c + HsL.rho_s, 400.0, 0.0, m_in(HsL.rho_c + HsL.rho_s, 1e9))
              + paint_at(HsL.rho_g, gx, gy, m_in(HsL.rho_g, 1e9))).sum(axis=2) * DXH
        res = dict(gx=gx, gy=gy, ux=ux, uy=uy, dSG=dSG)
        for Rap in (100.0, 150.0):
            cx, cy = centroid(SL, 400.0, 0.0, Rap); res[f"L_{Rap:.0f}"] = (cx - 400.0) * ux + cy * uy
        fx, fy = nfw_fit_centre(SL, 400.0, 0.0); res["L_fit"] = (fx - 400.0) * ux + fy * uy
        RES[(Msub, dSG, orient)] = res
    ic0 = NH // 2; icx = int(round((400.0 + LH / 2) / DXH))
    OUTB = {}
    for shape in ("intact", "S1", "S2"):                           # intact: the matched control (the kernel's own shift)
        Hm = G["solve_l366"](1e15, shape, EPSM[1e15], QTAB[1e15], 0.125, 0.015)
        bm = paint_at(Hm.rho_b, 0.0, 0.0, m_in(Hm.rho_b, 1e9)); cm = paint_at(Hm.rho_c, 0.0, 0.0, m_in(Hm.rho_c, 1e9))
        _, _, rph, _ = phantom_felt(GH, bm, bm + cm, ZH, A0K["canonical"], SW_DEF, [(ic0, ic0, ic0)])
        SMAIN = (bm + cm + rph).sum(axis=2) * DXH
        beta = {e: [] for e in ("100", "150", "fit")}; core = {}
        for Msub in (1e14, 3e14):
            Hs = G["solve_l366"](Msub, shape, EPSM[Msub], QTAB[Msub], 0.10, 0.02)
            core[Msub] = m_in(Hs.rho_c, 150.0) / m_in(Hs.rho_b, 150.0)
            ss = paint_at(Hs.rho_s, 400.0, 0.0, m_in(Hs.rho_s, 1e9)); cs = paint_at(Hs.rho_c, 400.0, 0.0, m_in(Hs.rho_c, 1e9))
            for (Ms_, dSG, orient) in CONF:
                if Ms_ != Msub:
                    continue
                r_ = RES[(Msub, dSG, orient)]
                gs = paint_at(Hs.rho_g, r_["gx"], r_["gy"], m_in(Hs.rho_g, 1e9))
                rb = bm + ss + gs; rreal = rb + cm + cs
                _, _, rph, _ = phantom_felt(GH, rb, rreal, ZH, A0K["canonical"], SW_DEF, [(ic0, ic0, ic0), (icx, ic0, ic0)])
                S = (rreal + rph).sum(axis=2) * DXH - SMAIN
                for Rap in (100.0, 150.0):
                    cx, cy = centroid(S, 400.0, 0.0, Rap)
                    beta[f"{Rap:.0f}"].append(((cx - 400.0) * r_["ux"] + cy * r_["uy"] - r_[f"L_{Rap:.0f}"]) / dSG)
                fx, fy = nfw_fit_centre(S, 400.0, 0.0)
                beta["fit"].append(((fx - 400.0) * r_["ux"] + fy * r_["uy"] - r_["L_fit"]) / dSG)
                del gs, rb, rreal, rph
            del ss, cs
        del bm, cm, SMAIN
        b = {e: float(np.mean(v)) for e, v in beta.items()}
        OUTB[shape] = dict(beta=b, core=core, ok=all(b[e] <= -0.04 + 2 * 0.07 for e in b), switch=SW_DEF)
    return OUTB


def harvey_job(args):
    """one cell's Harvey block (a Pool task)."""
    t, EPSM, vg = args
    with contextlib.redirect_stdout(io.StringIO()):
        return t, harvey_block(EPSM, vg)


if __name__ == "__main__":
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE: P("\n  *** MUTATE=1: mode U switched off in every decaying run -- X-COP must fail and R1 must flip ***")
    if SMOKE: P("\n  *** L373_SMOKE=1: code test on a 64^3 mesh, one realisation, one cell; nothing is written here ***")
    NPOOL = int(os.environ.get("L373_POOL", "6"))
    CKPT = os.path.join(tempfile.gettempdir(), f"L373_ckpt{'_MUTATE' if MUTATE else ''}{'_SMOKE' if SMOKE else ''}.pkl")
    RESUME = os.environ.get("L373_RESUME", "0") == "1" and os.path.exists(CKPT)
    TMP = tempfile.mkdtemp(prefix="L373_")
    cfgs = []
    for sp, sk in SEEDS:
        cfgs.append((f"s{sp}_lcdm", sp, sk, float("inf"), 0.0, 0.0, 0.0, TMP, "none", L77.A0["canonical"]))
        cfgs += [(f"s{sp}_{t}", sp, sk, L77.XC_TRIG, vg, 10.0, 0.0 if MUTATE else fu, TMP, "full", L77.A0["canonical"])
                 for t, (fu, vg) in zip(TAGS, CELLS)]
    P(f"\n  {len(cfgs)} runs, pool {NPOOL}; mode U: Gamma_0 = " + ", ".join(f"{gamma0_U(fu):.3f} H0 (f_U(0) = {fu:.2f})"
                                                                         for fu in sorted({c[0] for c in CELLS})))
    if RESUME:                                                     # the mesh runs are the slow part: resume after them
        import pickle
        res, M, GRP = (lambda d: (d["res"], d["M"], d["GRP"]))(pickle.load(open(CKPT, "rb")))
        P(f"  RESUMED from {CKPT} (the mesh runs and their measurements, unchanged)")
    else:
        with Pool(NPOOL) as pool:
            res = dict(pool.map(run2, cfgs, chunksize=1))
        P(f"  {len(cfgs)} runs done in {time.time() - T0:.0f}s")

    # ------------------------------------------------------------------------------------------ C1
    banner("C1  CONTROL")
    s66 = json.load(open(os.path.join(DS, "L366_triggered_carrier_cluster_retention_results.json")))["numbers"]["runs"]["lcdm"]["0.0"]["sigma8"]
    d1 = abs(res["s7_lcdm"]["0.0"]["sigma8"] / s66 - 1)
    check("C1 CONTROL: the (7, 11) LCDM run reproduces L366's committed LCDM sigma_8 (same code path, same seeds)",
          f"relative deviation {d1:.1e}", d1 < 1e-9)

    # ------------------------------------------------------------------------------------------ measurements
    TM = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L364_replacement_carrier_cosmic_shear_results.json")))["numbers"]["T_max"]
    est = L6.eps_bounds(); lo = max(v[0] for v in est.values()); hi = min(v[1] for v in est.values())
    s = L2.Sim(LBOX, NG, NP)
    ld = lambda nm, z, f: np.load(os.path.join(TMP, f"{nm}_z{z}_{f}.npy")).astype(float)
    if not RESUME:
        M, GRP = {}, {}
        for sp, _ in SEEDS:
            Lr = f"s{sp}_lcdm"
            M[sp], GRP[sp] = {}, {}
            dl = ld(Lr, 2.0, "rho") > 50.0                                 # LCDM's dense cells at z = 2: L379's fixed cells
            fix_l = float(ld(Lr, 2.0, "rhoc")[dl].sum())
            for z in (0.0, 0.4):
                rho_l, rc_l = ld(Lr, z, "rho"), ld(Lr, z, "rhoc")
                pk = L6.peaks(s, rho_l) if z == 0.0 else L6.peaks(s, rho_l, npk=60)   # z = 0 exactly as L378
                Mh = np.array([L6.sphere_sum(s, rho_l, p_, 1.0) * RHO_M for p_ in pk])
                Mc_l = np.array([L6.sphere_sum(s, rc_l, p_, 1.0) for p_ in pk])
                for t in TAGS:
                    eps = np.array([L6.sphere_sum(s, ld(f"s{sp}_{t}", z, "rhoc"), p_, 1.0) for p_ in pk]) / Mc_l
                    if z == 0.0:
                        r_ = res[f"s{sp}_{t}"]
                        M[sp][t] = dict(s8=r_["0.0"]["sigma8"] / res[Lr]["0.0"]["sigma8"],
                                        p1d={zz: (np.array(r_[zz]["p1d"]), np.array(res[Lr][zz]["p1d"]), np.array(res[Lr][zz]["kpar"])) for zz in ("3.0", "2.0")},
                                        cid=(r_["2.0"]["carrier_in_dense"], res[Lr]["2.0"]["carrier_in_dense"]),
                                        fix=(float(ld(f"s{sp}_{t}", 2.0, "rhoc")[dl].sum()), fix_l),
                                        pk=({qq: r_["0.5"]["pk"][qq] for qq in KG}, {qq: res[Lr]["0.5"]["pk"][qq] for qq in KG}),
                                        eps_sel=eps[Mh >= 1e14], decU=r_["0.0"]["decayed_U"], dec=r_["0.0"]["decayed"],
                                        dec_z04=(r_["0.4"]["decayed_U"], r_["0.4"]["decayed"]))
                    else:
                        GRP[sp][t] = dict(M=Mh, eps=eps)
        shutil.rmtree(TMP, ignore_errors=True)
        import pickle
        pickle.dump(dict(res=res, M=M, GRP=GRP), open(CKPT, "wb"))
        P(f"  checkpoint written: {CKPT}")
    else:
        shutil.rmtree(TMP, ignore_errors=True)

    def gates(rows):                                             # L378's gate arithmetic, plus L379's fixed-cell clearing
        s8 = float(np.mean([r["s8"] for r in rows])); fdev = 0.0
        for z in ("3.0", "2.0"):
            px = sum(r["p1d"][z][0] for r in rows); pl = sum(r["p1d"][z][1] for r in rows); kp = rows[0]["p1d"][z][2]
            m = (kp >= 0.2) & (kp <= 2.0); fdev = max(fdev, float(np.max(np.abs(px[m] / pl[m] - 1))))
        g3 = sum(r["cid"][0] for r in rows) / max(sum(r["cid"][1] for r in rows), 1e-30)
        g3f = sum(r["fix"][0] for r in rows) / max(sum(r["fix"][1] for r in rows), 1e-30)
        eps = np.concatenate([r["eps_sel"] for r in rows]); med = float(np.median(eps)) if len(eps) else float("nan")
        T = {qq: math.sqrt(sum(r["pk"][0][qq] for r in rows) / sum(r["pk"][1][qq] for r in rows)) for qq in KG}
        sh = all(T[qq] <= TM[f"p=2, x_c0=2.0/{f_}"][str(qq)] for qq in KG for f_ in ("canonical", "alt"))
        return dict(S8=s8, forest=fdev, G3=g3, G3_fixed=g3f, eps_cl=med, n_cl=int(len(eps)), shear=bool(sh),
                    s8_ok=s8 >= 0.899, s8_strict=s8 >= 0.922, forest_ok=fdev <= 0.10, xcop_ok=bool(lo <= med <= hi))

    banner("GATES: per realisation and pooled (X-COP two-sided %.3f-%.3f; S8 >= 0.922 strict / 0.899 alt; forest <= 0.10)" % (lo, hi))
    TAB = {}
    for key, rows_of in [(str(sp), lambda t, sp=sp: [M[sp][t]]) for sp, _ in SEEDS] + [("pooled", lambda t: [M[sp][t] for sp, _ in SEEDS])]:
        TAB[key] = {}
        for t in TAGS:
            g = gates(rows_of(t)); TAB[key][t] = g
            P(f"    {key:>6s} {t:10s}: S8 {g['S8']:.3f}{'' if g['s8_ok'] else ' X'} | forest {g['forest']:.3f}{'' if g['forest_ok'] else ' X'} | "
              f"X-COP eps {g['eps_cl']:.3f}{'' if g['xcop_ok'] else (' UNDER' if g['eps_cl'] < lo else ' OVER')} (n={g['n_cl']}) | "
              f"shear {'ok' if g['shear'] else 'X'} | z = 2 clearing (reported) own-set {g['G3']:.2f}, fixed cells {g['G3_fixed']:.2f}")
    for t in TAGS:
        P(f"    decayed by z = 0 ({t}): " + ", ".join(f"box {sp}: U {M[sp][t]['decU']:.3f} / all {M[sp][t]['dec']:.3f}" for sp, _ in SEEDS))
    GR = {}                                                        # group retention at z = 0.4, pooled
    for t in TAGS:
        Ms = np.concatenate([GRP[sp][t]["M"] for sp, _ in SEEDS]); Es = np.concatenate([GRP[sp][t]["eps"] for sp, _ in SEEDS])
        b1 = (Ms >= 5e13) & (Ms < 1e14); b3 = (Ms >= 1.5e14) & (Ms < 3e14); bm = Ms >= 3e14
        GR[t] = {1e14: float(np.median(Es[b1])) if b1.any() else float("nan"), 3e14: float(np.median(Es[b3])) if b3.any() else float("nan"),
                 1e15: float(np.median(Es[bm])) if bm.any() else float("nan"), "n": (int(b1.sum()), int(b3.sum()), int(bm.sum()))}
        P(f"    retention inside 1 Mpc/h at z = 0.4 ({t}): 5e13-1e14 {GR[t][1e14]:.2f} (n={GR[t]['n'][0]}), 1.5e14-3e14 "
          f"{GR[t][3e14]:.2f} (n={GR[t]['n'][1]}), >= 3e14 {GR[t][1e15]:.2f} (n={GR[t]['n'][2]})")

    # ------------------------------------------------------------------------------------------ Harvey
    banner("HARVEY (L371's machinery) on every pooled cell passing X-COP, with the retention measured at z = 0.4")
    todo = []
    for (fu, vg), t in zip(CELLS, TAGS):
        if TAB["pooled"][t]["xcop_ok"] or SMOKE:
            fb = next((GR[t][k] for k in (3e14, 1e14, 1e15) if np.isfinite(GR[t][k])), 1.0)
            todo.append((t, {k: (GR[t][k] if np.isfinite(GR[t][k]) else fb) for k in (1e14, 3e14, 1e15)}, vg))
    HV = {}
    if todo:
        with Pool(min(int(os.environ.get("L373_HPOOL", "2")), len(todo))) as pool:   # 400^3 QUMOND grids: memory-bound
            HV = dict(pool.map(harvey_job, todo, chunksize=1))
    for t, EPSM, vg in todo:
        P(f"    {t}: retention used {EPSM[1e14]:.2f}/{EPSM[3e14]:.2f}/{EPSM[1e15]:.2f}; excess beta (100/150/fit) intact "
          + "/".join(f"{HV[t]['intact']['beta'][e]:+.3f}" for e in ("100", "150", "fit")) + "; S1 "
          + "/".join(f"{HV[t]['S1']['beta'][e]:+.3f}" for e in ("100", "150", "fit")) + "; S2 "
          + "/".join(f"{HV[t]['S2']['beta'][e]:+.3f}" for e in ("100", "150", "fit"))
          + f"; core carrier/baryons(<150 kpc) S1 {HV[t]['S1']['core'][1e14]:.2f}/{HV[t]['S1']['core'][3e14]:.2f}"
          + f" -> {'PASS' if HV[t]['S1']['ok'] and HV[t]['S2']['ok'] else 'FAIL'}")
    if not todo:
        P("    no pooled cell passes X-COP: Harvey not run")
    P(f"    [{time.time() - T0:.0f}s]")

    SW_MESH = f"p{L77.P_GATE:g}_x{L77.X_C0:.1f}"
    used = sorted({HV[t][sh]["switch"] for t in HV for sh in HV[t]})
    check("C2 CONTROL: the Harvey stage's switch cell is the mesh runs' (L377: p = %d, x_c0 = %.1f)" % (L77.P_GATE, L77.X_C0),
          f"mesh {SW_MESH}; Harvey {used or 'not run (no cell passes X-COP)'}", all(u == SW_MESH for u in used))

    # ------------------------------------------------------------------------------------------ verdict
    banner("R1  THE HYPOTHESIS (set before the run)")
    ok_all = lambda t: (TAB["pooled"][t]["s8_ok"] and TAB["pooled"][t]["forest_ok"] and TAB["pooled"][t]["xcop_ok"]
                        and TAB["pooled"][t]["shear"] and t in HV and HV[t]["S1"]["ok"] and HV[t]["S2"]["ok"])
    WIN = [t for t in TAGS if ok_all(t)]
    WIN_strict = [t for t in WIN if TAB["pooled"][t]["s8_strict"]]
    FAILS = {t: [nm for nm, bad in (("S8", not TAB["pooled"][t]["s8_ok"]), ("forest", not TAB["pooled"][t]["forest_ok"]),
                                    ("X-COP", not TAB["pooled"][t]["xcop_ok"]), ("shear", not TAB["pooled"][t]["shear"]),
                                    ("Harvey", t in HV and not (HV[t]["S1"]["ok"] and HV[t]["S2"]["ok"]))) if bad] for t in TAGS}
    for t in TAGS:
        P(f"    pooled {t}: {'PASSES EVERY GATE' if t in WIN else 'fails ' + ', '.join(FAILS[t])}")
    check("R1 = H: the two-mode carrier's window survives assembly -- a pooled cell passes S_8 (alt), forest, X-COP, shear and "
          "Harvey (both core shapes)", f"window {WIN or 'none'} (with strict S_8: {WIN_strict or 'none'})",
          bool(WIN) == EXPECT_WINDOW)
    check("W (reported) the gate tables, group and cluster retention, and the z = 2 clearing (not gated: the vacuum gate "
          "keeps high-z halos by design)", "see above", True, load_bearing=False)
    E04 = (Om * 1.4 ** 3 + OL)
    OUT["numbers"]["model"] = dict(
        switch=dict(p=L77.P_GATE, x_c0=L77.X_C0, x_c_eff_z04=L77.X_C0 * E04 ** L77.P_GATE, harvey_key=SW_MESH),
        mesh_operator="L377 phantom(): Newtonian field of ALL baryons, constitutive response masked by the switch; gate on the "
                      "background-subtracted contrast 1.5 Omega_m(a) (rho/rho_bar - 1) [Omega_L(a)/Omega_L0]^p > x_c0",
        harvey_operator="L370 phantom_felt() (L361): each bound region's phantom from its OWN baryons; mask on the absolute "
                        "density 1.5 rho / (rho_c0 E^2) >= x_c0 E^(2p) -- a different operator from the mesh's even at the "
                        "matched cell (peer review 2026-09-26, NEXT_CALCULATIONS item 1)",
        kernel="nu_mono (L352)", a0_footing="canonical", carrier="Newtonian only (L353)",
        retention_epochs=dict(xcop="z = 0, inside 1 Mpc/h of LCDM's peaks", harvey="z = 0.4, pooled medians by mass bin"),
        harvey_shapes=["intact (matched control)", "S1 (scaled cusp)", "S2 (phase-mixed daughters at v_G)"],
        scope="the p = 2, x_c0 = 2 cell only: DE1 (c8bb50813) finds this cell fails the flat-a0 flagship at M_b = 1e11 on "
              "the canonical footing; the particle-mesh track has moved to p = 1, x_c0 = 2.5 (L388)")
    OUT["numbers"].update(table=TAB, groups_z04={t: {str(k): v for k, v in d.items()} for t, d in GR.items()},
                          harvey={t: {sh: dict(beta=v["beta"], ok=v["ok"], core={str(k): c for k, c in v["core"].items()})
                                      for sh, v in d.items()} for t, d in HV.items()},
                          window=WIN, window_strict_S8=WIN_strict, fails=FAILS, eps_bounds=dict(lo=lo, hi=hi),
                          decayed={t: {str(sp): dict(U=M[sp][t]["decU"], total=M[sp][t]["dec"], z04=M[sp][t]["dec_z04"])
                                       for sp, _ in SEEDS} for t in TAGS},
                          cells={t: dict(f_U0=fu, v_G=vg, v_U=V_U) for t, (fu, vg) in zip(TAGS, CELLS)})
    banner("VERDICT")
    n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
    P(f"  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}   [{time.time() - T0:.0f}s]")
    if SMOKE:
        P("  smoke test: no results written")
    else:
        outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
        json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
        P(f"  wrote {outname}")
    P(f"rc={0 if n_fail == 0 else 1}")
    sys.exit(0 if n_fail == 0 else 1)
