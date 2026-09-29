#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG172D_A3 -- THE OBSTRUCTION TEST under the replacement (frozen criteria 2.1: O1, O2, the zeta-interval test), controls C4, M1, M4, M5.

Grid (DE12's): point-mass baryons M_b = 1e10, 1e11, 1e12; z = 0.25, 1, 2.5, 4; both footings; gate widths w = 0.25 and 1; c2 = 7.3e-3 and 0.067
(L340's window ends); gas c_s = 37 / 117 / 10 km/s.  The gas around each system is DE12's f_b (NFW + mean) continued past r200.
ARMS (never pooled):  d1 (gate-sourced, no new term);  d2 lin and d2 sat (the explicit source, one constant zeta) in the FROZEN 'even' gate variable
u_theta = D(theta) E^-2, D = (thetabar/theta)^2 - 1  AND in a monotone SENSITIVITY variant ('mono': f = 1 for theta <= 0), added after the
even variant was found band-pass (see README: wrong expectation kept).
B (the gate's coefficient dL/df) is taken from V0's own static solution with the prescribed original gate (a reference solve per cell): a
declared approximation for the zeta scan ('frozen B', as DE12).  The scan is an EXISTENCE test (interval intersection), never a fit.
Run:  ZF_REPO=<repo> python3 CFG172D_A3_obstruction.py     (a few minutes)
"""
import os, sys, json, math, time
import numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG172D_common as C
import CFG172D_solver as S

MUT = os.environ.get("MUTATE")
R = C.Report("CFG172D_A3_obstruction", MUT)
P, banner, check = R.P, R.banner, R.check
P(__doc__.split("Run:")[0].strip()); P(f"\n  repo: {C.rel(C.REPO)}   MUTATE={MUT}")
T0 = time.time()
ZS = (0.25, 1.0, 2.5, 4.0); MBS = (1e10, 1e11, 1e12); FOOTS = ("canonical", "alt")
WS = (0.25, 1.0); C2S = (7.3e-3, 0.067)
CS37, CS117, CS10 = C.CS["1e5K"], C.CS["1e6K"], C.CS["cold10"]
KM = 1e3

# ============================================================================================ C4  reproduce DE12 (V0's original gate)
banner("C4  CONTROL: this lane's re-implementation of DE12 (V0's ORIGINAL gate, MOND-sector reading A+) reproduces DE12's committed numbers")
J = json.load(open(os.path.join(C.REPO, "real_research", "dark_energy_2026", "DE12_mond_sector_gate_stiffness_results.json")))
bud = J["numbers"]["budget"]
worst = 0.0; z25 = []
for k, v in bud.items():
    z, Mb, foot = k.split("/")
    c = S.de12_cell(float(z), float(Mb), foot, 0.25)
    worst = max(worst, abs(c["c_gate_max"] / v["c_gate_max"] - 1), abs(c["Gamma_over_H"] / v["Gamma_over_H"] - 1) if v["Gamma_over_H"] else 0)
    if z == "0.25":
        z25.append(c)
check("C4 DE12's 24 cells (c_gate_max, Gamma/H) reproduced to 2%", f"max relative deviation {worst:.2e}", worst < 0.02)
mn_c = min(c["c_gate_max"] for c in z25); mn_g = min(c["Gamma_over_H"] for c in z25)
P(f"  original gate, z = 0.25, w = 0.25: min c_gate = {mn_c / KM:.0f} km/s, min Gamma(k = 1/kpc)/H = {mn_g:.1e} (record: 1526 km/s, 2.0e4)")
R.num("original_gate_z025", dict(min_c_gate_kms=mn_c / KM, min_Gamma_over_H=mn_g))

# ---------------------------------------------------------------------------------------------- helpers on the solver grid
RK = np.geomspace(1.0, 2.0e4, 1500)          # kpc


def profile_rho_contrast(z, Mb):
    """gas density contrast above the mean baryon density (Msun/kpc^3), DE12's gas (f_b NFW) on the kpc grid, and the total gas density"""
    hs = C.host(Mb, z)
    r_si = RK * C.KPC
    rho_nfw = hs["rho_s"] / ((r_si / hs["rs"]) * (1 + r_si / hs["rs"])**2)
    rho_bar = C.Om * C.rho_crit0 * (1 + z)**3
    conv = S.KPC3_OVER_MS
    return C.FB * rho_nfw * conv, C.FB * (rho_nfw + rho_bar) * conv, C.FB * rho_bar * conv


def reference_B(z, Mb, foot, w, m=1 / 100.0):
    """V0's own static solution with the prescribed original gate (DE12's t(r)), returning B (brace units), the a0^2 q part, and t(r)"""
    a0 = C.A0_FOOT[foot]
    tr = S.de12_transition(z, Mb, foot, w)
    t = np.interp(np.log(RK), np.log(tr["r"] / C.KPC), tr["t"])
    f, _, _ = C.Wd(t)
    sol = S.solve_v0(RK, f, a0, Mb, "point", m=m)
    Bb, Bq = S.Bbrace(sol, a0, m=m)
    return Bb, Bq, t, f, sol


def layer_c_eff(z, Mb, w, c2, Bb, rho_c, rho_tot, zeta, kind, variant):
    """the fully-eliminated second variation on the layer: c_eff^2 = rho * 16 pi G zeta^2 h'^2 / (theta_L^2 |L_thth|); returns per-r arrays"""
    y, nro = S.theta_root(z, w, c2, Bb, rho_c, zeta, kind=kind, variant=variant, ND=2500)
    f, fy, fyy, t, u = S.gate_from_y(y, z, w, variant=variant)
    tb = S.theta_bar_kpc(z)
    vth = (tb / S.THETA_L_KPC) * (y - 1)
    hv, h1, h2 = S.hfun(vth, kind)
    Lthth = -2 * c2 + Bb * fyy / tb**2 - (16 * math.pi * S.G * rho_c / S.CKMS**2) * zeta * h2 / S.THETA_L_KPC**2
    c2eff = rho_tot * 16 * math.pi * S.G * zeta**2 * h1**2 / (S.THETA_L_KPC**2 * np.maximum(np.abs(Lthth), 1e-300))
    lay = (t > 0) & (t < 1)
    return dict(y=y, f=f, t=t, nroots=nro, Lthth=Lthth, c_eff=np.sqrt(c2eff), layer=lay)


# ============================================================================================ reference solutions and d1
banner("REFERENCE: V0's own B = dL/df on the original-gate layer; and d1 (gate-sourced compaction)")
REF = {}
for z in ZS:
    for Mb in MBS:
        for foot in FOOTS:
            for w in WS:
                REF[(z, Mb, foot, w)] = reference_B(z, Mb, foot, w)
# how big is V0's B compared with the a0^2 q part alone (DE7 / frozen criteria assume ~ a0^2 q)
rat = []
for (z, Mb, foot, w), (Bb, Bq, t, f, sol) in REF.items():
    lay = (t > 0.02) & (t < 0.98)
    if lay.any():
        rat.append(np.median(Bb[lay] / Bq[lay]))
P(f"  B / (2 a0^2 q/c^4) on the transition layers of the original gate (median per cell): min {min(rat):.3g}, median {np.median(rat):.3g}, max {max(rat):.3g}"
  f"   (the record's DE7 says 'within ~10%'; frozen criteria 1.5/3.1 used B ~ 2 alpha^2 q)")
R.num("B_over_Bq_layer", dict(min=min(rat), median=float(np.median(rat)), max=max(rat)))
check("(reported) V0's full B on the layers is within 10% of the a0^2 q part alone (the record's DE7 statement)", f"median ratio {np.median(rat):.3g}, range [{min(rat):.3g}, {max(rat):.3g}]",
      abs(np.median(rat) - 1) < 0.10, load_bearing=False)

# d1:   continuation branch, and the alternative branches (S-curve) if the gate were pushed into its transition
d1 = {}
for (z, Mb, foot, w), (Bb, Bq, t, f, sol) in REF.items():
    for c2 in C2S:
        tb = S.theta_bar_kpc(z)
        # (i) the equation on the continuation branch: f' = 0 at theta = thetabar => theta = thetabar exactly => f = 0 everywhere
        # (ii) alternative branches at each r: roots of  2 c2 tb^2 delta + B f_y(y(delta)) = 0 with delta > 0
        dl = np.geomspace(1e-9, 1e6, 6000); y = 1 - dl
        fy = S.gate_from_y(y, z, w, variant="even")[1]; fyy = S.gate_from_y(y, z, w, variant="even")[2]
        G_ = 2 * c2 * tb**2 * dl[None, :] + Bb[:, None] * fy[None, :]
        sgn = np.sign(G_); nchg = np.sum(sgn[:, 1:] * sgn[:, :-1] < 0, axis=1)
        alt = nchg >= 1
        # (iii) the hypothetical stability margin at the layer (if theta were placed there): 2 c2 vs B f_theta_theta with y from t(r)
        lay = (t > 0.0) & (t < 1.0)
        E2z = C.E2(z)
        ygl = 1 / np.sqrt(1 + E2z * (2.5 * (1 + 2 * w * (t - 0.5)))) if lay.any() else np.array([])
        ratio = 0.0
        if lay.any():
            uu = 2.5 * (1 + 2 * w * (t[lay] - 0.5)); yy = 1 / np.sqrt(1 + E2z * uu)
            _, fy_l, fyy_l, _, _ = S.gate_from_y(yy, z, w, variant="even")
            ratio = float(np.max(Bb[lay] * fyy_l / tb**2 / (2 * c2)))
        # (iv) the bump the gate source would produce if the local theta sat at the layer: |B f_y| / (2 c2 tb^2)
        bump = float(np.max(np.abs(Bb[lay] * S.gate_from_y(1 / np.sqrt(1 + E2z * 2.5 * (1 + 2 * w * (t[lay] - 0.5))), z, w)[1]) / (2 * c2 * tb**2))) if lay.any() else 0.0
        d1[(z, Mb, foot, w, c2)] = dict(frac_r_with_alt_branch=float(np.mean(alt)), max_stab_ratio=ratio, max_bump_if_at_layer=bump,
                                        f_on_continuation=0.0, c_eff=0.0)
# d1 ALTERNATIVE (S-curve) branch: where does the stable upper root put the gate ON, in terms of the local acceleration y = g_N/a0?
alt_info = {}
for (z, Mb, foot, w), (Bb, Bq, t, f, sol) in REF.items():
    a0 = C.A0_FOOT[foot]; rM = math.sqrt(S.G * Mb / a0)
    for c2 in C2S:
        y_alt, nro = S.theta_root(z, w, c2, Bb, np.zeros_like(Bb), 0.0, kind="lin", variant="even", ND=3000, branch="upper")
        f_alt = S.gate_from_y(y_alt, z, w, variant="even")[0]
        on = f_alt > 0.5
        yN = S.G * Mb / RK**2 / a0
        alt_info[(z, Mb, foot, w, c2)] = dict(frac_on=float(np.mean(on)), r_max_on_over_rM=float(RK[on].max() / rM) if on.any() else 0.0,
                                              yN_min_on=float(yN[on].min()) if on.any() else None, f_max=float(f_alt.max()))
ons = [v for v in alt_info.values() if v["frac_on"] > 0]
P(f"  d1 ALTERNATIVE (upper, stable S-curve) branch: gate reaches f > 1/2 somewhere in {len(ons)}/{len(alt_info)} cells; "
  f"outermost radius with f > 1/2: median {np.median([v['r_max_on_over_rM'] for v in ons]) if ons else 0:.3g} r_M, max {max([v['r_max_on_over_rM'] for v in ons]) if ons else 0:.3g} r_M; "
  f"lowest local acceleration y = g_N/a0 with f > 1/2: median {np.median([v['yN_min_on'] for v in ons]) if ons else float('nan'):.3g}, min {min([v['yN_min_on'] for v in ons]) if ons else float('nan'):.3g} "
  f"(the law needs the gate ON down to y ~ 1e-3)")
R.num("d1_alt_branch", {f"{k[0]}/{k[1]:.0e}/{k[2]}/w{k[3]}/c2{k[4]}": v for k, v in alt_info.items()})
alt_any = [v["frac_r_with_alt_branch"] for v in d1.values()]
rat_st = [v["max_stab_ratio"] for v in d1.values()]
P(f"  d1: continuation branch has theta = thetabar exactly (f' = 0 there) => f = 0 at every radius in every one of {len(d1)} cells; c_eff = 0 (no baryon coupling, frozen B)")
P(f"  d1: alternative branches of the local equation (S-curve) exist at some r in {sum(a > 0 for a in alt_any)}/{len(alt_any)} cells (fraction of radii with an extra root: max {max(alt_any):.2f})")
P(f"  d1: hypothetical margin  B f_thth / (2 c2)  on the original layer if theta were placed there: max over cells {max(rat_st):.3g}; cells with ratio > 1 (fold): "
  f"{sum(v['max_stab_ratio'] > 1 for v in d1.values())}/{len(d1)}")
bumps = np.array([v["max_bump_if_at_layer"] for v in d1.values()])
P(f"  d1: |delta theta|/thetabar the gate source could make IF theta sat at the layer: median {np.median(bumps):.2e}, max {bumps.max():.2e}  (needed depletion 0.5-0.9)")
R.num("d1", {f"{k[0]}/{k[1]:.0e}/{k[2]}/w{k[3]}/c2{k[4]}": v for k, v in d1.items()})
check("HYPOTHESIS (frozen 3.1: bump <~ 2e-3 at the edge): the gate-sourced bump, IF theta sat at the layer, is at most 1e-2 of the depletion the gate needs in every cell", f"max bump {bumps.max():.2e}", bumps.max() < 1e-2, load_bearing=False)
d1_blind = True

if MUT == "M5":
    banner("M5 (prescribed gate, f not varied): the record's data-pass mode: no stiffness, O2 by construction")
    ok_all = True; nrow = 0; n_ok = 0; fails_m5 = []
    for (z, Mb, foot, w), (Bb, Bq, t_ref, f_ref, sol) in REF.items():
        rho_c, rho_tot, rho_bar_b = profile_rho_contrast(z, Mb)
        a0 = C.A0_FOOT[foot]; rM = math.sqrt(S.G * Mb / a0)
        i3 = int(np.argmin(np.abs(RK - 3 * rM))); web = (rho_c / rho_bar_b) <= 5.0
        o2 = (f_ref[i3] >= 0.99) and (f_ref[web].max() <= 0.01 if web.any() else True)
        ok_all &= bool(o2); nrow += 1; n_ok = (n_ok if "n_ok" in dir() else 0) + int(bool(o2))
        if not o2:
            fails_m5.append(f"z{z}/{Mb:.0e}/{foot}/w{w}")
    P(f"  prescribed original gate: O1 passes trivially (no varied gate, no stiffness); O2 (f(3 r_M) >= 0.99, web off) holds in {n_ok}/{nrow} cells (fails: {fails_m5[:12]}{' ...' if len(fails_m5) > 12 else ''}): the prescribed original gate itself is not ON at 3 r_M at high z and large M (DE1\'s flagship-edge problem)")
    check("M5 with the gate prescribed (not varied) O1 and O2 both pass in every cell: the obstruction is a property of VARYING the gate", f"O2 all cells: {ok_all}", not ok_all)
    R.write()
    P(f"\n  MUTATE=M5: control {'BITES' if ok_all else 'DOES NOT BITE'}"); sys.exit(1 if ok_all else 0)

# ============================================================================================ d2 scan
banner("d2: THE zeta-INTERVAL TEST (existence, not a fit) -- O2 (region selective) against O1 (stable), four coupling/gate variants")
ZETA = np.geomspace(1e-9, 1e2, 45)
VARS = (("lin", "mono"),) if MUT else (("lin", "even"), ("sat", "even"), ("lin", "mono"), ("sat", "mono"))
res = {}
for (kind, variant) in VARS:
    tv = time.time()
    per_cell = {}
    for (z, Mb, foot, w), (Bb, Bq, t_ref, f_ref, sol) in REF.items():
        if MUT == "M5":
            pass
        rho_c, rho_tot, rho_bar_b = profile_rho_contrast(z, Mb)
        a0 = C.A0_FOOT[foot]; rM = math.sqrt(S.G * Mb / a0)
        i3 = int(np.argmin(np.abs(RK - 3 * rM))); i30 = int(np.argmin(np.abs(RK - 30 * rM)))
        web = (rho_c / rho_bar_b) <= 5.0
        for c2 in C2S:
            for zeta in ZETA:
                if MUT == "M2":
                    zeta_eff = 0.0
                elif MUT == "M3":
                    zeta_eff = -zeta
                else:
                    zeta_eff = zeta
                c2_eff = c2 * (0.01 if MUT == "M4" else 1.0)
                Bb_use = np.zeros_like(Bb) if MUT == "M5" else Bb
                out = layer_c_eff(z, Mb, w, c2_eff, Bb_use, rho_c, rho_tot, abs(zeta_eff) if zeta_eff != 0 else 0.0, kind, variant) if zeta_eff >= 0 else None
                if zeta_eff < 0:
                    # sign flip: theta is increased where matter is: no depletion, gate never turns on
                    per_cell.setdefault((z, Mb, foot, w, c2), []).append(dict(zeta=zeta, f3=0.0, f30=0.0, web_max=0.0, ceff=0.0, nroots_max=0, ceff_layer_any=False))
                    continue
                f3 = float(out["f"][i3]); f30 = float(out["f"][i30]); webf = float(out["f"][web].max()) if web.any() else 0.0
                lay = out["layer"]
                ce = float(out["c_eff"][lay].max()) if lay.any() else 0.0
                per_cell.setdefault((z, Mb, foot, w, c2), []).append(dict(zeta=zeta, f3=f3, f30=f30, web_max=webf, ceff=ce,
                                                                         nroots_max=int(out["nroots"].max()), ceff_layer_any=bool(lay.any())))
    res[(kind, variant)] = per_cell
    P(f"    variant {kind}/{variant}: scanned {len(per_cell)} cells x {len(ZETA)} zeta values   [{time.time() - tv:.0f} s]")

# per-cell and joint verdicts
SUM = {}
for key, per_cell in res.items():
    kind, variant = key
    cells = {}
    joint_ok = np.ones((2, len(WS), len(ZETA)), bool) if False else {}
    for (z, Mb, foot, w, c2), rows in per_cell.items():
        f3 = np.array([r_["f3"] for r_ in rows]); webf = np.array([r_["web_max"] for r_ in rows])
        ce = np.array([r_["ceff"] for r_ in rows]); nr = np.array([r_["nroots_max"] for r_ in rows])
        f30a = np.array([r_["f30"] for r_ in rows])
        o2 = (f3 >= 0.99) & (webf <= 0.01)
        o2r = (f30a >= 0.99) & (webf <= 0.01)                     # ADDED (not frozen): the gate also reaches 30 r_M, the end of the G1 grid
        o1 = (ce <= CS37 / KM) & (nr <= 1)
        zmin = float(ZETA[np.argmax(o2)]) if o2.any() else None
        zreach = float(ZETA[np.argmax(o2r)]) if o2r.any() else None
        # zeta_max: the largest zeta such that O1 holds for all zeta' <= zeta
        bad = np.where(~o1)[0]
        zmax = float(ZETA[bad[0] - 1]) if len(bad) and bad[0] > 0 else (float(ZETA[-1]) if not len(bad) else None)
        both = o1 & o2
        both_r = o1 & o2r
        cells[(z, Mb, foot, w, c2)] = dict(zeta_min=zmin, zeta_reach=zreach, zeta_max_stable=zmax, o2_any=bool(o2.any()), both_any=bool(both.any()), reach_any=bool(o2r.any()), both_reach_any=bool(both_r.any()), o2r=o2r,
                                          ceff_at_zmin=(float(ce[np.argmax(o2)]) if o2.any() else None), o1=o1, o2=o2, ce=ce)
    SUM[key] = cells
    n_c = len(cells)
    n_o2 = sum(c["o2_any"] for c in cells.values()); n_both = sum(c["both_any"] for c in cells.values())
    # joint: one zeta for ALL cells at a given (w, c2)
    joint = {}
    for w in WS:
        for c2 in C2S:
            sel = [c for k_, c in cells.items() if k_[3] == w and k_[4] == c2]
            AND_o2 = np.all([c["o2"] for c in sel], axis=0); AND_o1 = np.all([c["o1"] for c in sel], axis=0); AND_o2r = np.all([c["o2r"] for c in sel], axis=0)
            joint[(w, c2)] = dict(o2_all=bool(AND_o2.any()), o1_all=bool(AND_o1.any()), both=bool((AND_o2 & AND_o1).any()), reach_all=bool(AND_o2r.any()), both_reach=bool((AND_o2r & AND_o1).any()))
    cmin = [c["ceff_at_zmin"] for c in cells.values() if c["ceff_at_zmin"] is not None]
    ratios = [c["zeta_min"] / c["zeta_max_stable"] for c in cells.values() if c["zeta_min"] and c["zeta_max_stable"]]
    n_reach = sum(c["reach_any"] for c in cells.values()); n_both_reach = sum(c["both_reach_any"] for c in cells.values())
    P(f"\n  [{kind}/{variant}] ADDED (not frozen) reach test: the gate ON (f >= 0.99) out to 30 r_M for SOME zeta in {n_reach}/{n_c} cells; together with O1 (c_eff <= 37 km/s) in {n_both_reach}/{n_c}; "
      f"jointly (one zeta, all cells): {sum(j['both_reach'] for j in joint.values())}/{len(joint)} (w,c2) combinations")
    P(f"\n  [{kind}/{variant}] cells {n_c}: O2 achievable for SOME zeta in {n_o2}/{n_c}; O1 & O2 together for some zeta in {n_both}/{n_c}; "
      f"joint (one zeta, all 24 (z,M,foot) cells): both-holds in {sum(j['both'] for j in joint.values())}/{len(joint)} (w,c2) combinations")
    if cmin:
        P(f"    c_eff at the smallest zeta that makes the gate region-selective (zeta_min): median {np.median(cmin):.3g} km/s, min {min(cmin):.3g}, max {max(cmin):.3g}  (gas 37/117 km/s)")
    if ratios:
        P(f"    zeta_min/zeta_max (>1 means the intervals do not meet): median {np.median(ratios):.3g}, min {min(ratios):.3g}, max {max(ratios):.3g}")
    R.num(f"summary_{kind}_{variant}", dict(n_reach=n_reach, n_both_reach=n_both_reach, joint_reach={f"w{k[0]}/c2{k[1]}": v["both_reach"] for k, v in joint.items()}, n_cells=n_c, n_o2=n_o2, n_both=n_both, joint={f"w{k[0]}/c2{k[1]}": v for k, v in joint.items()},
                                          ceff_at_zmin_median=float(np.median(cmin)) if cmin else None,
                                          ratio_median=float(np.median(ratios)) if ratios else None,
                                          ratio_min=float(min(ratios)) if ratios else None))
    SUM[key]["_joint"] = joint

zref = {}
for (kind_, variant_), cells_ in SUM.items():
    cc = cells_.get((0.25, 1e11, "canonical", 0.25, 7.3e-3))
    zref[f"{kind_}/{variant_}"] = (cc["zeta_min"] if cc else None)
R.num("zeta_min_reference", zref)
P(f"  zeta_min of the reference cell (1e11, z = 0.25, canonical, w = 0.25, c2 = 7.3e-3): {zref}")
# hand pincer prediction: -c_s^2/c^2 = 3 c2 Delta^2 eps_L/eps_b  evaluated on the mono/lin variant at the layer for the reference cell
banner("PINCER (hand formula) against the numbers: reference cell (1e11, z = 0.25, canonical, w = 0.25, c2 = 7.3e-3), d2 lin/mono")
z, Mb, foot, w, c2 = 0.25, 1e11, "canonical", 0.25, 7.3e-3
Bb = REF[(z, Mb, foot, w)][0]; rho_c, rho_tot, rho_bar_b = profile_rho_contrast(z, Mb)
# zeta_min from the scan
c_ref = SUM[("lin", "mono")][(z, Mb, foot, w, c2)]
zmin = c_ref["zeta_min"]
P(f"  zeta_min (reference cell, lin/mono) = {zmin}")
if zmin:
    out = layer_c_eff(z, Mb, w, c2, Bb, rho_c, rho_tot, zmin, "lin", "mono")
    lay = out["layer"]
    ce_num = float(out["c_eff"][lay].max()) if lay.any() else float("nan")
    i_l = np.where(lay)[0][np.argmax(out["c_eff"][lay])] if lay.any() else 0
    Delta = (1 - S.theta_bar_kpc(z) * 0 - out["y"][i_l]) * S.theta_bar_kpc(z) / S.THETA_L_KPC
    eb_over_eL = rho_tot[i_l] / S.RHO_L_KPC
    hand = math.sqrt(3 * c2 * Delta**2 / eb_over_eL) * S.CKMS
    P(f"  at the layer point of max c_eff: r = {RK[i_l]:.0f} kpc, eps_b/eps_L = {eb_over_eL:.3g}, Delta = {Delta:.3g}; c_eff(numerical) = {ce_num:.4g} km/s; "
      f"hand pincer sqrt(3 c2 Delta^2 eps_L/eps_b) c = {hand:.4g} km/s (they differ by the gate's fold factor 1/|L_thth|/2c2 and by the exact h')")
    R.num("pincer_reference", dict(zeta_min=zmin, c_eff_numeric_kms=ce_num, c_eff_hand_kms=hand, Delta=Delta, eb_over_eL=eb_over_eL))

# ============================================================================================ verdicts
banner("VERDICT GRAMMAR (per arm; frozen criteria 2.1):  REMOVED iff O1 PASS and O2 PASS and O3 PASS in the same cell with the same constants")
VERD = {}
VERD["d1"] = dict(O1="PASS (stable because blind: continuation branch f = 0, c_eff = 0; hypothetical fold ratio max %.3g)" % max(rat_st),
                  O2="FAIL (f = 0 at every radius on the continuation branch in all cells)", verdict="MOVED (blind)")
for key, cells in SUM.items():
    kind, variant = key
    n_c = len(cells) - 1
    n_o2 = sum(c["o2_any"] for k_, c in cells.items() if k_ != "_joint")
    n_both = sum(c["both_any"] for k_, c in cells.items() if k_ != "_joint")
    jb = sum(j["both"] for j in cells["_joint"].values())
    cm = [c["ceff_at_zmin"] for k_, c in cells.items() if k_ != "_joint" and c["ceff_at_zmin"] is not None]
    if jb > 0:
        v = "REMOVED in the joint sense in %d/8 (w,c2) combinations (independent re-derivation REQUIRED)" % jb
    elif n_both > 0:
        v = "per-cell zeta exists in %d/%d cells but no single zeta serves all cells: STILL PRESENT (cell-tuned only)" % (n_both, n_c)
    else:
        v = "STILL PRESENT (no zeta satisfies O1 and O2 in any cell)"
    VERD[f"d2_{kind}_{variant}"] = dict(O1=f"c_eff at zeta_min median {np.median(cm) if cm else float('nan'):.3g} km/s (line 37 km/s)",
                                        O2=f"achievable for some zeta in {n_o2}/{n_c} cells", joint_both=jb, verdict=v)
for k_, v in VERD.items():
    R.verdict(k_, v["verdict"], "; ".join(str(v[x]) for x in ("O1", "O2") if x in v))
R.num("verdicts", VERD)

# ============================================================================================ M1 restore the original gate
banner("M1 (restore the original gate): V0's original gate on the same cells gives the record's obstruction (STILL PRESENT); reported for the table")
if MUT == "M1":
    check("M1 with the original gate the obstruction bites (min c_gate > 117 km/s and Gamma/H > 1e3 on every z = 0.25 galaxy layer)",
          f"min c_gate {mn_c / KM:.0f} km/s, min Gamma/H {mn_g:.1e}", not (mn_c > CS117 and mn_g > 1e3))
else:
    check("(control) with V0's original gate the record's obstruction is reproduced on every z = 0.25 galaxy layer (the positive control of the obstruction)",
          f"min c_gate {mn_c / KM:.0f} km/s > 117; min Gamma/H {mn_g:.1e} > 1e3", mn_c > CS117 and mn_g > 1e3)

nf = R.write()
if MUT:
    if MUT == "M1":
        bitten = (mn_c > CS117 and mn_g > 1e3)
    elif MUT == "M2":     # ζ = 0: O2 must fail in every cell
        bitten = all(not c["o2_any"] for key in SUM for k_, c in SUM[key].items() if k_ != "_joint")
    elif MUT == "M3":     # sign flip: O2 must fail in every cell
        bitten = all(not c["o2_any"] for key in SUM for k_, c in SUM[key].items() if k_ != "_joint")
    elif MUT == "M4":     # c2 x 0.01: |c_s| must drop but stay above 117 km/s in at least one cell
        bitten = any((c["ceff_at_zmin"] or 0) > CS117 / KM for key in SUM for k_, c in SUM[key].items() if k_ != "_joint")
    elif MUT == "M5":     # B = 0 (prescribed-like gate: no gate stiffness): the ζ-interval must open more
        bitten = True
    else:
        bitten = False
    P(f"\n  MUTATE={MUT}: control {'BITES' if bitten else 'DOES NOT BITE'}")
    sys.exit(1 if bitten else 0)
sys.exit(0 if nf == 0 else 1)
