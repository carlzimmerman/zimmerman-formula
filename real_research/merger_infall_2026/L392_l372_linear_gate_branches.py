#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L392 -- L372'S TWO-MODE CARRIER RE-SCORED SAME-CELL AT THE LINEAR GATE (p = 1, x_c0 = 2.5), EACH SWITCH VARIABLE ON ITS OWN.

WHY.  L372's committed window ("passes forest, S_8, X-COP, galaxies, KiDS and Harvey on the alternative set") joins two
  kernel setups (cross-lane review XR1; scope note 8850550c4): KiDS was scored through L357 -> L355 with NO switch, Harvey at
  L370's p = 1, x_c0 = 1.5 cell with an absolute-density matter mask, canonical footing only.  The construction now sits at
  the linear gate p = 1, x_c0 = 2.5 (DE1/DE2; L388-L390), and the switch variable has two readings that must never be pooled:
    MATTER     the gate reads the matter density (baryons + carrier), background-subtracted;
    CURVATURE  the gate reads the dynamical (curvature) density: matter + the phantom of the switch-everywhere field -- the
               untruncated dynamical density, as L352 and DE1 compute the edge -- background-subtracted.  (L395's "onbranch"
               cell iterates the MASKED phantom to self-consistency instead; the two agree away from the edge layer but are
               not operationally identical -- never pool them either.)
  This lane re-scores L372's window cells at the linear gate on each reading separately, with KiDS switched (L360's fit and
  data) and Harvey through L370's solver and region operator (L361), the reading applied to BOTH stages of each branch.
WHAT IS RE-SCORED.  Only the switch-dependent gates.  Forest, S_8, X-COP and galaxies are switch-free in L372 (L319's
  solver; the retained carrier inside clusters and galaxies; X-COP's R500 lies deep inside any switched region) and are
  read from L372's committed results.  Cells: L372's window, f_U(0) = 0.25 with v_G = 750, 900, 1050 km/s (G: L357's
  cleared picture at x_v0 = 2000, vacuum-gated p = 2; U: L319's law at 3000 km/s).
METHOD.
  KiDS: L372's own carrier templates (kids_templates_vk, U-scaled), added to L360's switched model at the cell's
    x_c,eff(0.25) (L359's K1 entry, as L360/L390), 2-halo free, Delta chi^2 against L360's unswitched baseline.  The edge
    is set per branch from the lens's own density (L375's resolved baryons -- Hernquist, a = 3 kpc (M_b/1e11)^0.3, plus the
    rest of f_b M200 as an NFW-shaped CGM -- plus the bin's retained carrier; the ESD keeps L352's point-mass baryons), the
    region connected to the centre, compensated as L352.  (A first code test with a bare stellar Hernquist and no CGM put
    the matter-branch edges at 0.15-0.34 Mpc: the CGM fills the region the cleared carrier leaves, so it is included.)  L352's own edge rule
    (the phantom density alone, outermost switched radius) is reported alongside as L360's reference.
  Harvey: L372's harvey() re-implemented (its processed carrier, its U factor at z = 0.4, its eight configurations) with the
    branch's mask in the 1-D lensing-mass root AND the 3-D phantom map; the region operator is L370's (each region's phantom
    from its own baryons).  Canonical footing for every cell; the alternative footing for the central cell.  Every result
    records the resolved model (cell, p, x_c0, x_c,eff, footing, a0, the branch's switch variable, the operator).
PRE-DECLARED (before any run).  H: L372's window survives same-cell at the linear gate on EACH reading: on the matter
  branch some window cell passes KiDS (Delta chi^2 <= +4, both footings; L390's standard) and Harvey (excess beta <= +0.10
  on all three estimators, canonical), with its committed switch-free gates; and likewise on the curvature branch.
CHECKS
  C1 CONTROL: L372's templates rebuilt here give L372's committed switch-free (L355) KiDS scores, and the KiDS data radii and
     host masses of L355 and L360 coincide (the templates feed L360's fit unchanged).
  C2 CONTROL: the branch-aware lens model in L352's own edge mode reproduces L360's switched fit (same templates) exactly.
  C3 CONTROL: the branch-aware Harvey in L370's own mode at L372's cell (p = 1, x_c0 = 1.5; absolute mask; canonical)
     reproduces L372's committed Harvey numbers for (0.25, 750).
  C4 the cell took effect: x_c,eff(0.4) of every Harvey job equals 2.5 E(0.4)^2; the KiDS x_c,eff(0.25) is L359's entry.
  RA = H on the matter branch;  RB = H on the curvature branch (never pooled).  Each is scored on two conventions for the
     lens's matter beyond r200 -- cut at r200 (the templates as built) and continued as the host's NFW (infall, CGM) -- split
     AFTER the first main run: with the cut, the matter-branch KiDS edge sat exactly at r200 (0.145-0.343 Mpc), a truncation
     artefact, so both conventions are reported as separate cells (RA[r200], RA[nfw], RB[r200], RB[nfw]), never pooled.
     (Harvey's halos extend to L370's 2.5 R200 in both branches.)
  W  (reported) L360's reference edge rule; the edges; the alternative footing; the switch-free gates carried from L372.
MUTATE=1 scores an INTACT carrier (no decay: L357's template at x_v0 -> infinity, f_U = 0) on both branches: KiDS must reject
  it and RA, RB flip (Harvey is not run under MUTATE and never counts as a pass).  FAST=1 is a code test (coarse Harvey grid, one cell); it writes nothing here.
SCOPE (sigma).  Harvey's region operator is L370's, which drops L361's web self-term (sigma = 0).  V0 (chk_v0_2026, CV1/CV2)
  finds sigma physical (L361's action and V0 use sigma = 1), and the cross-thread review XR5 measured that the sigma = 1 far
  edge layer moves a projected substructure centroid by 4.1 kpc against 0.52 kpc at sigma = 0 -- up to delta beta ~ 0.03-0.07
  at these 60-120 kpc offsets.  Every Harvey number here is sigma = 0; a 3-D sigma = 1 operator (a screened solve with a
  mask-dependent M^2) is not built here.
L392_POOL sets the Harvey pool (default 2: each job holds a 400^3 grid).

Run from the repository root:  python3 real_research/merger_infall_2026/L392_l372_linear_gate_branches.py
"""
import os, sys, json, math, time, io, contextlib, tempfile
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
FAST = os.environ.get("FAST", "0") == "1"
SLUG = "L392_l372_linear_gate_branches" + ("_MUTATE" if MUTATE else "") + ("_FAST" if FAST else "")
OUTDIR = tempfile.gettempdir() if FAST else HERE
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L392", "cell": "p=1, x_c0=2.5", "mutate": MUTATE, "checks": {}, "numbers": {}}
EXPECT = {"matter": True, "curvature": True}                          # H, set before any run
CELL, P_C, XC0 = "p1_x2.5", 1.0, 2.5
CELL_L372 = "p1_x1.5"
CELLS = [(0.25, 750.0)] if FAST else [(0.25, 750.0), (0.25, 900.0), (0.25, 1050.0)]
CENTRAL = CELLS[0] if FAST else (0.25, 900.0)
XV0, PIC, V_U = 2000.0, "cleared", 3000.0
BRANCHES = ("matter", "curvature")
KIDS_TOL, KIDS_TOL_L355 = 4.0, 9.0
HARV_BETA, HARV_ERR = -0.04, 0.07
EST = ("100", "150", "fit")
P72 = os.path.join(HERE, "L372_gated_slow_kick_carrier.py")
P70 = os.path.join(HERE, "L370_boosted_infall_mergers.py")
P60 = os.path.join(REPO, "real_research", "g03_audit_2026", "L360_assembled_construction_kids.py")
NH = 160 if FAST else 400


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 116); P(t); P("=" * 116)


def _quiet_exec(src, ns):
    mut, fast = os.environ.get("MUTATE", "0"), os.environ.get("FAST", "0")
    os.environ["MUTATE"], os.environ["FAST"] = "0", "0"               # the loaded lanes' own switches stay off
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(src, ns)
    finally:
        os.environ["MUTATE"], os.environ["FAST"] = mut, fast
    ns["MUTATE"] = False
    return ns


def load72():
    """L372's definitions only (the L357 machinery, x_eff, kids_templates_vk, fU_of_z): none of its runs."""
    s = open(P72).read()
    head = s.split("# ================================================================================================ C1")[0]
    head = head.replace('P(__doc__.split("CHECKS")[0].strip())', "pass")
    return _quiet_exec(head, {"__name__": "l372", "__file__": P72})


def carrier_profiles(N, x_eff_zl, picture, vk, scale=1.0):
    """kids_templates_vk (L372) line for line, also returning each bin's retained-carrier density [Msun/kpc^3] on r [kpc]."""
    T, prof = [], []
    for b in range(4):
        M200 = N["M200_KIDS_57"][b]; c = float(N["c200_55_57"](M200))
        Mn, r200, rs = N["nfw21_57"](M200, c, N["RHOC_ZL_57"])
        pro = np.geomspace(0.02 * rs, 0.999 * r200, 40)
        rv_ = N["rho_thr_57"](x_eff_zl, N["ZL_57"], N["RHOC_ZL_57"])
        Mb_fn = N["hernquist_57"](1.3 * 10 ** N["LOGMS_57"][b], 3.0)
        if np.isfinite(x_eff_zl):
            _, ratio_p, _ = N["retained_core_57"](Mb_fn, M200, c, r200, 0.0, vk, rv_, picture, rhoc=N["RHOC_ZL_57"], probes=pro, N=8000)
        else:
            ratio_p = np.ones_like(pro)                               # MUTATE: the intact carrier
        r_kpc = N["rr55_57"] / N["KPC_M_57"]
        Mc = scale * (1 - N["FB_57"]) * Mn(np.minimum(r_kpc, r200)) * np.interp(np.log(r_kpc), np.log(pro), ratio_p)
        dS = N["esd_of_M_57"](Mc * N["MS_57"] + 1.0, 1.0)
        T.append(np.interp(N["Rd55_57"][b], N["Rp55_57"] / N["MPCm_57"], dS))
        rho = np.maximum(np.gradient(Mc, r_kpc) / (4 * math.pi * r_kpc ** 2), 0.0)
        rho_s = M200 / (4 * math.pi * rs ** 3 * N["mfn_57"](c))
        rho_nfw = scale * (1 - N["FB_57"]) * rho_s / ((r_kpc / rs) * (1 + r_kpc / rs) ** 2)
        prof.append(dict(r=r_kpc, r200=r200, rho_r200=rho,                 # the template's own profile (zero beyond r200)
                         rho_nfw=np.where(r_kpc < r200, rho, rho_nfw)))     # continued beyond r200 as the host's NFW (infall)
    return T, prof


# ================================================================================================ Harvey (workers)
_W = {}


def _harvey_setup():
    """per worker: L372's definitions, L370's head, its Harvey helpers, and the branch-aware solver pieces."""
    if _W:
        return _W
    N72 = load72()
    s70 = open(P70).read()
    head70 = s70.split("# ============================================================================================================ C1")[0]
    head70 = head70.replace('P(__doc__.split("CHECKS")[0].strip())', "pass")
    G70 = _quiet_exec(head70, {"__name__": "l370", "__file__": P70})
    G70["SWITCH"][CELL] = (P_C, XC0)                                 # the linear gate, added here (L370's file untouched)
    GH = G70["Grid"](NH, 10000.0)
    G70.update(dict(GH=GH, DXH=GH.dx, NH=NH, LH=10000.0))
    exec(s70[s70.index("def centroid(S, x0, y0, Rap, it=12):"):s70.index("HB = []")], G70)
    _W.update(N72=N72, G70=G70, GH=GH)
    return _W


def _lensing_branch(G70, H, a0, cell, branch, kernel=True):
    """L370's RealHalo.lensing with the branch's switch variable (branch 'L370' = L370's own absolute matter mask)."""
    RG, GK, cum_mass, nu_mono, x_ceff = (G70[k] for k in ("RG", "GK", "cum_mass", "nu_mono", "x_ceff"))
    Mb, Mr = cum_mass(H.rho_b), cum_mass(H.rho)
    nu1 = nu_mono(GK * Mb / RG ** 2 / a0) - 1.0
    xce = x_ceff(H.z, cell)
    if branch == "L370":
        inside = (1.5 * H.rho / H.rhoc) >= xce
    else:
        rbar = G70["Om"] * (1 + H.z) ** 3 * G70["RHOC0"]
        rho_sw = H.rho + (np.gradient(nu1 * Mb, RG) / (4 * math.pi * RG ** 2) if branch == "curvature" else 0.0)
        inside = (1.5 * (rho_sw - rbar) / H.rhoc) >= xce
    f = np.cumprod(inside).astype(float)                              # the region connected to the centre
    Mph = f * nu1 * Mb if kernel else 0.0 * Mb
    ML = Mr + Mph
    diff = ML - 200 * H.rhoc * 4 / 3 * math.pi * RG ** 3
    i = int(np.argmax((diff[:-1] > 0) & (diff[1:] <= 0)))
    R200L = RG[i] - diff[i] * (RG[i + 1] - RG[i]) / (diff[i + 1] - diff[i])
    return dict(M200L=float(np.interp(R200L, RG, ML)), R200L=float(R200L),
                edge=float(RG[int(np.argmin(f))]) if f.min() == 0 else float(RG[-1]))


def _phantom_branch(G70, grid, rb, rreal, z, a0, cell, centres, branch):
    """L370's phantom_felt with the branch's switch variable; returns the phantom density for lensing and the model record."""
    from scipy import ndimage
    x_ceff, Ez2, RHOC0, nu_mono, GK = (G70[k] for k in ("x_ceff", "Ez2", "RHOC0", "nu_mono", "GK"))
    if branch == "L370":
        _, _, rph, _ = G70["phantom_felt"](grid, rb, rreal, z, a0, cell, centres)
        return rph
    rhoc_z = RHOC0 * Ez2(z); rbar = G70["Om"] * (1 + z) ** 3 * RHOC0
    rho_sw = rreal.copy()
    if branch == "curvature":                                        # the switch-everywhere phantom of all baryons
        gw = grid.field(rb); mag = np.sqrt(gw[0] ** 2 + gw[1] ** 2 + gw[2] ** 2)
        fac = nu_mono(mag / a0) - 1.0
        gph = grid.project([fac * g_ for g_ in gw]); del gw, mag, fac
        rho_sw += -grid.divergence(gph) / (4 * math.pi * GK); del gph
    mask = (1.5 * (rho_sw - rbar) / rhoc_z) >= x_ceff(z, cell)
    del rho_sw
    lab, _ = ndimage.label(mask)
    labs = sorted({int(lab[c]) for c in centres if lab[c] > 0})
    rho_ph = np.zeros_like(rb)
    for L_ in labs:                                                   # L361: each region's phantom from its own baryons
        f = (lab == L_)
        gw = grid.field(rb * f); mag = np.sqrt(gw[0] ** 2 + gw[1] ** 2 + gw[2] ** 2)
        fac = f * (nu_mono(mag / a0) - 1.0)
        gph = grid.project([fac * g_ for g_ in gw]); del gw, mag, fac
        rho_ph += -grid.divergence(gph) / (4 * math.pi * GK)
        del gph, f
    return rho_ph


def harvey_job(args):
    """L372's harvey() for one (cell, branch, footing), the branch applied to the lensing root and the phantom map."""
    (fu, vg), branch, footing, cell, RES = args
    W = _harvey_setup(); N72, G70, GH = W["N72"], W["G70"], W["GH"]
    from scipy.optimize import brentq
    from scipy.interpolate import PchipInterpolator
    RealHalo, cum_mass, m_in, RG, paint_at, centroid, nfw_fit_centre = (G70[k] for k in (
        "RealHalo", "cum_mass", "m_in", "RG", "paint_at", "centroid", "nfw_fit_centre"))
    model = G70["resolve_cell"](cell, footing, 0.4)
    a0 = model["a0"]; ZH, DXH, XSUB = 0.4, GH.dx, 400.0
    RHOC_H = N72["RHOC0_KPC_57"] * N72["Ez2_57"](ZH)
    us = 1.0 if MUTATE else 1 - N72["fU_of_z"](fu, ZH)
    xv = float("inf") if MUTATE else XV0

    def ratio_profile(H):                                             # L372's, line for line
        Mb_tab = cum_mass(H.rho_b)
        Mb_fn = lambda r: np.interp(np.asarray(r, float), RG, Mb_tab)
        pro = np.geomspace(10.0, 2.0 * H.R200, 24)
        if not np.isfinite(xv):
            return pro, np.ones_like(pro)
        rv_ = N72["rho_thr_57"](N72["x_eff"](xv, ZH), ZH, RHOC_H)
        _, q, _ = N72["retained_core_57"](Mb_fn, H.M200, H.c, H.R200, 0.0, vg, rv_, PIC, rhoc=RHOC_H, probes=pro)
        return pro, np.asarray(q)

    def solve_processed(M200L, fgas, fstar):                          # L372's, with the branch's lensing root
        pro, q = ratio_profile(RealHalo(M200L, ZH, fgas, fstar, "intact"))
        f = PchipInterpolator(np.log(pro), np.clip(q, 0.0, 2.0))

        def build(M):
            H = RealHalo(M, ZH, fgas, fstar, "intact")
            Mc0 = cum_mass(H.rho_c)
            qr = np.where(RG < pro[0], q[0], np.where(RG > pro[-1], q[-1], f(np.log(np.clip(RG, pro[0], pro[-1])))))
            H.rho_c = us * np.maximum(np.gradient(qr * Mc0, RG) / (4 * math.pi * RG ** 2), 0.0)
            H.rho = H.rho_b + H.rho_c
            return H
        M = brentq(lambda M: _lensing_branch(G70, build(M), a0, cell, branch)["M200L"] - M200L, 0.2 * M200L, 6.0 * M200L, rtol=1e-6)
        return build(M)
    ic0 = NH // 2; icx = int(round((XSUB + 10000.0 / 2) / DXH))
    Hm = solve_processed(1e15, 0.125, 0.015)
    bm = paint_at(Hm.rho_b, 0.0, 0.0, m_in(Hm.rho_b, 1e9)); cm = paint_at(Hm.rho_c, 0.0, 0.0, m_in(Hm.rho_c, 1e9))
    rph = _phantom_branch(G70, GH, bm, bm + cm, ZH, a0, cell, [(ic0, ic0, ic0)], branch)
    SMAIN = (bm + cm + rph).sum(axis=2) * DXH; del rph
    beta = {e: [] for e in EST}; core = {}; edges = {}
    edges["main_1d"] = _lensing_branch(G70, Hm, a0, cell, branch)["edge"]
    for Msub in (1e14, 3e14):
        Hs = solve_processed(Msub, 0.10, 0.02)
        edges[f"{Msub:.0e}_1d"] = _lensing_branch(G70, Hs, a0, cell, branch)["edge"]
        core[f"{Msub:.0e}"] = m_in(Hs.rho_c, 150.0) / m_in(Hs.rho_b, 150.0)
        ss = paint_at(Hs.rho_s, XSUB, 0.0, m_in(Hs.rho_s, 1e9)); cs = paint_at(Hs.rho_c, XSUB, 0.0, m_in(Hs.rho_c, 1e9))
        for key, r_ in RES.items():
            if r_["Msub"] != Msub:
                continue
            gs = paint_at(Hs.rho_g, r_["gx"], r_["gy"], m_in(Hs.rho_g, 1e9))
            rb = bm + ss + gs; rreal = rb + cm + cs
            rph = _phantom_branch(G70, GH, rb, rreal, ZH, a0, cell, [(ic0, ic0, ic0), (icx, ic0, ic0)], branch)
            S = (rreal + rph).sum(axis=2) * DXH - SMAIN
            for Rap in (100.0, 150.0):
                cx, cy = centroid(S, XSUB, 0.0, Rap)
                beta[f"{Rap:.0f}"].append(((cx - XSUB) * r_["ux"] + cy * r_["uy"] - r_[f"LCDM_{Rap:.0f}"]) / r_["dSG"])
            fx, fy = nfw_fit_centre(S, XSUB, 0.0)
            beta["fit"].append(((fx - XSUB) * r_["ux"] + fy * r_["uy"] - r_["LCDM_fit"]) / r_["dSG"])
            del gs, rb, rreal, rph, S
        del ss, cs
    b = {e: float(np.mean(v)) for e, v in beta.items()}
    model.update(branch=branch, switch_variable={"L370": "absolute matter density (L370)",
                 "matter": "matter density, background-subtracted",
                 "curvature": "matter + the switch-everywhere phantom (untruncated dynamical density), background-subtracted"}[branch],
                 us=us, NH=NH)
    return ((fu, vg), branch, footing, cell), dict(beta=b, core=core, edges=edges, model=model,
                                                   ok=all(b[e] <= HARV_BETA + 2 * HARV_ERR for e in EST))


def lcdm_reference():
    """L372's LCDM reference maps (the same components, all real): branch- and cell-independent."""
    W = _harvey_setup(); G70, GH = W["G70"], W["GH"]
    paint_at, centroid, nfw_fit_centre, m_in = (G70[k] for k in ("paint_at", "centroid", "nfw_fit_centre", "m_in"))
    XSUB, DXH = 400.0, GH.dx
    RES = {}
    for Msub in (1e14, 3e14):
        for dSG in (60.0, 120.0):
            for orient in ("perp", "toward_main"):
                gx, gy = (XSUB, dSG) if orient == "perp" else (XSUB - dSG, 0.0)
                ux, uy = ((0.0, 1.0) if orient == "perp" else (-1.0, 0.0))
                HsL, _ = G70["solve_real"](Msub, 0.4, G70["A0K"]["canonical"], CELL_L372, "intact", fgas=0.10, fstar=0.02, kernel=False)
                SL = (paint_at(HsL.rho_c + HsL.rho_s, XSUB, 0.0, m_in(HsL.rho_c + HsL.rho_s, 1e9))
                      + paint_at(HsL.rho_g, gx, gy, m_in(HsL.rho_g, 1e9))).sum(axis=2) * DXH
                r_ = dict(Msub=Msub, gx=gx, gy=gy, ux=ux, uy=uy, dSG=dSG)
                for Rap in (100.0, 150.0):
                    cx, cy = centroid(SL, XSUB, 0.0, Rap); r_[f"LCDM_{Rap:.0f}"] = (cx - XSUB) * ux + cy * uy
                fx, fy = nfw_fit_centre(SL, XSUB, 0.0); r_["LCDM_fit"] = (fx - XSUB) * ux + fy * uy
                RES[f"{Msub:.0e}|{dSG:.0f}|{orient}"] = r_
    return RES


if __name__ == "__main__":
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE: P("\n  *** MUTATE=1: an intact carrier (no decay) on both branches -- KiDS must reject it and RA, RB flip ***")
    if FAST: P("\n  *** FAST=1: code test (coarse Harvey grid, one cell); nothing is written here ***")
    R72 = json.load(open(os.path.join(HERE, "L372_gated_slow_kick_carrier_results.json")))["numbers"]

    # --------------------------------------------------------------------------------------- KiDS
    banner("KiDS  L372's carrier on L360's switched model at the linear gate, each branch's edge")
    N72 = load72()
    ZL = N72["ZL_57"]
    N60 = _quiet_exec(open(P60).read().split("BASE = {")[0], {"__name__": "l360", "__file__": P60})
    L52 = N60["L52"]
    fit_comb60, fit_model60, A052, XE59 = N60["fit_comb"], N60["fit_model"], N60["A0"], N60["XE59"]
    rr, Rp, Rd, Ed, Sd, Ci, LM, twoh = (L52[k] for k in ("rr", "Rp", "Rd", "Ed", "Sd", "Ci", "LM", "twoh_cache"))
    project_M2, annulus_esd, shell_M2, nu_vec, Gsi, Hz = (L52[k] for k in ("project_M2", "annulus_esd", "shell_M2", "nu_vec", "G", "Hz"))
    Om52, rho_crit0, MS, MPCm = (L52[k] for k in ("Om", "rho_crit0", "MS", "MPCm"))
    FOOT = ("canonical", "alt")
    BASE = {f_: fit_model60(A052[f_], 0.0, "none", True)[0] for f_ in FOOT}
    XE = round(XE59[(P_C, XC0)], 4)
    KPC_M = N72["KPC_M_57"]
    c200_60, mfn_60, FB_60, M200_60, rhoc_zl_60 = (N60[k] for k in ("c200", "mfn", "FB", "M200_BINS", "rhoc_zl"))
    M200_H = list(N72["M200_KIDS_57"])                                 # the carrier templates' hosts (L355's Moster+13 masses)

    def rho_baryons_L375(b, Mb, conv):
        """the lens's baryons as L375 resolves them [kg/m^3 on rr]: Hernquist (a = 3 kpc (M_b/1e11)^0.3) + the rest of
        f_b M200 as an NFW-shaped CGM inside r200 (the switch reads these; the ESD keeps L352's point mass)."""
        M200 = M200_H[b]; c = float(N72["c200_55_57"](M200)); r200 = (3 * M200 * MS / (4 * math.pi * 200 * rhoc_zl_60)) ** (1 / 3)
        rs = r200 / c
        ab = 3.0 * (Mb / MS / 1e11) ** 0.3 * KPC_M
        Mcgm = max(FB_60 * M200 - Mb / MS, 0.0) * MS
        rho_h = Mb * ab / (2 * math.pi * rr * (rr + ab) ** 3)
        rho_g = Mcgm / (4 * math.pi * rs ** 3 * mfn_60(c)) / ((rr / rs) * (1 + rr / rs) ** 2)
        return rho_h + (np.where(rr < r200, rho_g, 0.0) if conv == "r200" else rho_g)

    def model_M2_branch(Mb, a0, xc, z, rho_c_si, branch, b=0):
        """L352's model_M2 (compensated) with the edge from the branch's switch variable ('reference' = L352's own rule)."""
        M = Mb * nu_vec(Gsi * Mb / rr ** 2 / a0)
        rho_bar = Om52 * rho_crit0 * (1 + z) ** 3
        rho_ph = np.gradient(M, rr) / (4 * math.pi * rr ** 2)          # the untruncated phantom (point baryons add none at r > 0)
        if branch == "reference":
            on = 4 * math.pi * Gsi * (rho_ph - rho_bar) / Hz(z) ** 2 >= xc
            it = int(np.where(on)[0].max()) if on.any() else 0
        else:
            br_, conv = branch.split("|")
            rho_sw = rho_baryons_L375(b, Mb, conv) + rho_c_si[conv][b] + (rho_ph if br_ == "curvature" else 0.0)
            on = 4 * math.pi * Gsi * (rho_sw - rho_bar) / Hz(z) ** 2 >= xc
            off = np.where(~on)[0]
            it = (max(int(off[0]) - 1, 0) if len(off) else len(rr) - 1)  # the region connected to the centre
        re = rr[it]
        M = np.where(np.arange(len(rr)) > it, M[it], M)
        M2c = project_M2(np.gradient(M - Mb, rr) / (4 * math.pi * rr ** 2))
        m_sh = -(M[-1] - Mb)

        def f(R, M2c=M2c, m_sh=m_sh, re=re):
            return np.interp(np.log(R), np.log(Rp), M2c) + Mb + shell_M2(m_sh, re, R)
        return f, re / MPCm
    _ESDB = {}

    def fit_branch(a0, xc, TC, rho_c_bins, branch, tag):
        """L360's fit_comb (fs = 1) with the branch-aware lens model; returns chi^2, the best log M_b and the edges."""
        mods, lms, res_ = [], [], []
        for b in range(4):
            best = None
            for lm in LM:
                key = (tag, branch, b, round(lm, 3), a0, xc)
                if key not in _ESDB:
                    f, re = model_M2_branch(10 ** lm * MS, a0, xc, 0.25, rho_c_bins, branch, b)
                    _ESDB[key] = (annulus_esd(f, Rd[b]), re)
                mk0, re = _ESDB[key]
                mk0 = mk0 + TC[b]
                t2 = twoh[b]; w = 1 / Sd[b] ** 2
                A = float(np.clip(np.sum(w * t2 * (Ed[b] - mk0)) / np.sum(w * t2 * t2), 0.0, 20.0)); mk = mk0 + A * t2
                c_ = float(np.sum(((Ed[b] - mk) / Sd[b]) ** 2))
                if best is None or c_ < best[0]: best = (c_, mk, lm, re)
            mods.append(best[1]); lms.append(best[2]); res_.append(best[3])
        dv = np.concatenate(Ed) - np.concatenate(mods)
        return float(dv @ Ci @ dv), lms, res_

    TEMPL, RHOC = {}, {}
    for (fu, vg) in CELLS:
        fu_eff = 0.0 if MUTATE else fu
        xv_zl = float("inf") if MUTATE else N72["x_eff"](XV0, ZL)
        fzl = N72["fU_of_z"](fu_eff, ZL)
        T, prof = carrier_profiles(N72, xv_zl, PIC, vg, scale=1.0 - fzl)
        TEMPL[(fu, vg)] = T
        RHOC[(fu, vg)] = {conv: [np.interp(np.log(rr), np.log(pr["r"] * KPC_M), pr[f"rho_{conv}"] * MS / KPC_M ** 3,
                                           left=pr[f"rho_{conv}"][0] * MS / KPC_M ** 3, right=0.0) for pr in prof]
                          for conv in ("r200", "nfw")}
    # C1: the templates and the data radii
    rd_same = all(np.allclose(N72["Rd55_57"][b], Rd[b], rtol=1e-12, atol=0.0) for b in range(4)) and \
        all(abs(N72["M200_KIDS_57"][b] / M200_60[b] - 1) < 0.01 for b in range(4))       # same radii; hosts to L360's 3 figures
    c1 = {}
    if not MUTATE:
        for (fu, vg) in CELLS:
            ks = N72["kids_score_57"](TEMPL[(fu, vg)])
            got = {f_: ks[("web-blind kernel", f_)]["dchi2"] for f_ in FOOT}
            ref = {f_: R72["part2"][f"{fu}|{vg}"]["kids"][f"web-blind kernel|{f_}"] for f_ in FOOT}
            c1[f"{fu}|{vg}"] = max(abs(got[f_] - ref[f_]) for f_ in FOOT)
    check("C1 CONTROL: L372's templates rebuilt here give its committed switch-free (L355) KiDS scores, and the KiDS data radii "
          "of L355 and L360 coincide", f"max |difference| {max(c1.values()) if c1 else float('nan'):.1e} over {len(c1)} cells; "
          f"radii identical {rd_same}", rd_same and (MUTATE or (c1 and max(c1.values()) < 1e-6)))
    # C2: the branch-aware model in L352's own edge mode reproduces L360's fit
    c0 = CELLS[0]
    ref60 = {f_: fit_comb60(A052[f_], XE, TEMPL[c0], [1.0])[0] for f_ in FOOT}
    mine = {f_: fit_branch(A052[f_], XE, TEMPL[c0], RHOC[c0], "reference", c0)[0] for f_ in FOOT}
    d2 = max(abs(mine[f_] - ref60[f_]) for f_ in FOOT)
    check("C2 CONTROL: the branch-aware lens model in L352's own edge mode reproduces L360's switched fit with the same templates",
          f"max |chi^2 difference| {d2:.1e}", d2 < 1e-6)
    KD = {}
    KBR = ("reference", "matter|r200", "matter|nfw", "curvature|r200", "curvature|nfw")
    for (fu, vg) in CELLS:
        for br in KBR:
            row = {}
            for f_ in FOOT:
                c2_, lms, res_ = fit_branch(A052[f_], XE, TEMPL[(fu, vg)], RHOC[(fu, vg)], br, (fu, vg))
                row[f_] = dict(dchi2=c2_ - BASE[f_], logMb=lms, edges_Mpc=res_)
            KD[(fu, vg, br)] = row
            P(f"    f_U(0) {fu:.2f} v_G {vg:5.0f}  {br:15s}: KiDS Delta chi^2 {row['canonical']['dchi2']:+7.1f} / {row['alt']['dchi2']:+7.1f}; "
              f"edges (Mpc, canonical) {[round(e_, 3) if e_ else None for e_ in row['canonical']['edges_Mpc']]}")
    P(f"    x_c,eff(0.25) = {XE} (L359's K1 entry); 2.5 E(0.25)^2 = {XC0 * N72['Ez2_57'](0.25):.4f}   [{time.time() - T0:.0f}s]")

    # --------------------------------------------------------------------------------------- Harvey
    banner("HARVEY  L372's harvey() at the linear gate, each branch in the lensing root and the phantom map")
    RES = {}
    if not MUTATE:
        _harvey_setup()
        RES = lcdm_reference()
        P(f"    LCDM reference maps done ({len(RES)} configurations)   [{time.time() - T0:.0f}s]")
    jobs = []
    if not MUTATE:
        jobs.append(((0.25, 750.0), "L370", "canonical", CELL_L372, RES))    # C3: L372's own setup
    for c_ in CELLS:
        for br in BRANCHES:
            jobs.append((c_, br, "canonical", CELL, RES))
    if not FAST:
        for br in BRANCHES:
            jobs.append((CENTRAL, br, "alt", CELL, RES))
    if MUTATE:
        jobs = []                                                      # the flip is KiDS's; Harvey is not run (never a pass)
    _W.clear()                                                         # workers rebuild their own grids
    import pickle
    CKPT = os.path.join(tempfile.gettempdir(), f"{SLUG}_harvey_ckpt.pkl")
    if os.environ.get("L392_RESUME", "0") == "1" and os.path.exists(CKPT):
        HV = pickle.load(open(CKPT, "rb"))
        P(f"    RESUMED the Harvey jobs from {CKPT}")
    else:
        with Pool(int(os.environ.get("L392_POOL", "2"))) as pool:
            HV = dict(pool.map(harvey_job, jobs, chunksize=1))
        pickle.dump(HV, open(CKPT, "wb"))
    P(f"    {len(jobs)} Harvey jobs done   [{time.time() - T0:.0f}s]")
    for k_, h_ in HV.items():
        (c_, br, f_, cell_) = k_
        P(f"    {c_} {br:9s} {f_:9s} {cell_}: excess beta " + "/".join(f"{h_['beta'][e]:+.3f}" for e in EST)
          + f"; carrier/baryons(<150 kpc) {h_['core']['1e+14']:.2f}/{h_['core']['3e+14']:.2f}; x_c,eff(0.4) {h_['model']['x_c_eff']:.3f}"
          + f" -> {'PASS' if h_['ok'] else 'FAIL'}")
    if not MUTATE:
        c3k = ((0.25, 750.0), "L370", "canonical", CELL_L372)
        refH = next(v for k, v in R72["harvey"].items() if "0.25" in k and "750" in k)
        d3 = max(abs(HV[c3k]["beta"][e] - refH["beta"][e]) for e in EST)
        check("C3 CONTROL: the branch-aware Harvey in L370's own mode at L372's cell (p = 1, x_c0 = 1.5; absolute mask; "
              "canonical) reproduces L372's committed Harvey numbers for (0.25, 750)",
              f"max |difference| {d3:.1e} (L372 {refH['beta']}, here {HV[c3k]['beta']})", d3 < (1e-2 if FAST else 1e-6))
    xce_new = [h_["model"]["x_c_eff"] for (c_, br, f_, cell_), h_ in HV.items() if cell_ == CELL]
    Ez2_04 = N72["Ez2_57"](0.4)
    check("C4 the cell took effect: x_c,eff(0.4) of every linear-gate Harvey job equals 2.5 E(0.4)^2",
          f"{sorted(set(round(x, 6) for x in xce_new))} vs {XC0 * Ez2_04:.6f}", all(abs(x - XC0 * Ez2_04) < 1e-6 for x in xce_new))

    # --------------------------------------------------------------------------------------- verdicts
    banner("RA, RB  THE HYPOTHESIS ON EACH BRANCH (set before any run; never pooled)")
    SF = {}
    for (fu, vg) in CELLS:
        r = R72["part2"][f"{fu}|{vg}"]
        T2 = min(r["t2"], r["t3"])
        gal_max = max(abs(v) for f_ in r["gal_shift"] for v in r["gal_shift"][f_].values())
        SF[(fu, vg)] = dict(forest=bool(T2 >= 0.9), S8_alt=bool(r["S8"] >= 0.748), xcop_alt=bool(all(r["xcop"][f_]["alt"] for f_ in FOOT)),
                            gal=bool(gal_max <= 0.06), S8=r["S8"])
    VER = {}
    for br in BRANCHES:
        for conv in ("r200", "nfw"):
            kb = f"{br}|{conv}"; passing = []
            for (fu, vg) in CELLS:
                sf = SF[(fu, vg)]
                kd = KD[(fu, vg, kb)]
                k_ok = all(kd[f_]["dchi2"] <= KIDS_TOL for f_ in FOOT)
                h_ = HV.get(((fu, vg), br, "canonical", CELL))
                h_ok = bool(h_ and h_["ok"])                             # not run (MUTATE) is never a pass
                ok = sf["forest"] and sf["S8_alt"] and sf["xcop_alt"] and sf["gal"] and k_ok and h_ok
                fails = [n for n, bad in (("forest", not sf["forest"]), ("S8", not sf["S8_alt"]), ("X-COP", not sf["xcop_alt"]),
                                          ("galaxies", not sf["gal"]), ("KiDS", not k_ok), ("Harvey", not h_ok)) if bad]
                P(f"    {kb:15s} f_U(0) {fu:.2f} v_G {vg:5.0f}: KiDS {kd['canonical']['dchi2']:+.1f}/{kd['alt']['dchi2']:+.1f}; Harvey fit "
                  f"{(format(h_['beta']['fit'], '+.3f') if h_ else 'not run')} -> {'PASSES EVERY GATE' if ok else 'fails ' + ', '.join(fails)}")
                if ok:
                    passing.append((fu, vg))
            VER[kb] = passing
            check(f"R{'A' if br == 'matter' else 'B'}[{conv}] = H on the {br} branch, lens matter {'cut at r200' if conv == 'r200' else 'continued as NFW'}: "
                  f"some window cell passes KiDS (<= +{KIDS_TOL:g}, both footings) and Harvey (canonical), with its committed switch-free gates",
                  f"passing cells: {passing or 'none'}", bool(passing) == EXPECT[br])
    check("W (reported) L360's reference edge rule, the edges, the alternative footing, the switch-free gates", "see above", True,
          load_bearing=False)
    OUT["numbers"].update(
        cells=[list(c_) for c_ in CELLS], x_c_eff_kids_0p25=XE, kids={f"{k[0]}|{k[1]}|{k[2]}": v for k, v in KD.items()},
        kids_base=BASE, harvey={f"{k[0][0]}|{k[0][1]}|{k[1]}|{k[2]}|{k[3]}": v for k, v in HV.items()},
        switch_free_from_L372={f"{k[0]}|{k[1]}": v for k, v in SF.items()}, verdict=VER,
        model=dict(cell=CELL, p=P_C, x_c0=XC0, kids_x_c_eff=XE, kernel="nu_mono (L352/L340)", carrier="Newtonian only (L353)",
                   branches=dict(matter="matter density (baryons + carrier), background-subtracted, region connected to the centre",
                                 curvature="matter + the switch-everywhere phantom (the untruncated dynamical density), background-"
                                           "subtracted, region connected to the centre",
                                 reference="L352's own KiDS edge (the phantom density alone, outermost switched radius)"),
                   harvey_operator="L370/L361 region kernel (each region's phantom from its own baryons)",
                   kids_operator="L352/L360 spherical switched lens (compensated), baryons a point mass in the ESD, Hernquist "
                                 "(a = 3 kpc) in the switch variable"))
    banner("VERDICT")
    n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    json.dump(OUT, open(os.path.join(OUTDIR, SLUG + "_results.json"), "w"), indent=1,
              default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    P(f"  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {SLUG}_results.json   "
      f"[{time.time() - T0:.0f}s]")
    P(f"rc={0 if n_fail == 0 else 1}")
    sys.exit(0 if n_fail == 0 else 1)
