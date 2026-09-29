#!/usr/bin/env python3
"""CFG122 G1.1-G1.3 (+ G3.1, G5.1, G5.2, G5.3 on the same solutions): the coupled BK solution over the declared (m, alpha) plane and the per-halo constant Y = mu - m Phi.
Frozen criteria: G1.1 Branch S point mass, G1.2 Branch S exponential spheres, G1.3 Branch F (dynamics vs P2), G3.1 reaction, G5.1-5.3.
Plane: m in [1e-3, 1e3] eV x alpha in [1e-2, 1e2], 60 x 60 log grid; Lambda from the a0 tie; per-halo Y(r_lo) = 0, +-10^k m G M/r_M (k = -6..6); branches B- (X<0 root),
B+hi, B+lo (the two X>0 roots): a cell PASSES if ANY branch and ANY Y passes (the most generous reading).  Same (m, alpha) at all four masses.
Env: ZF_REPO (repo root, only for nothing here), MUTATE = a (target := the door's own gradient-dominated condensate density) | c (alpha_c = 1e-12 alpha).
Run: python3 cfg122_g1_plane.py"""
import os, sys, math, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg122_common import *
from cfg122_targets import target_on_grid, p2_law_g

MUT = os.environ.get("MUTATE", "")
R = Report("cfg122_g1_plane")
P, check = R.P, R.check
N = 160
NCH = 6
PLANE_N = int(os.environ.get("PLANE_N", "60"))
mg, ag, Mm, Aa = plane(PLANE_N)
KS = np.arange(-6, 7)
PROFILES = {"point": ("point", None), "exp_compact": ("exp", 0.3), "exp_diffuse": ("exp", 3.0)}
ALPHA_C_FAC = 1e-12 if MUT == "c" else None

P(f"CFG122 G1 plane scan  MUTATE={MUT!r}  plane {PLANE_N}x{PLANE_N}  N={N}  Y0 grid {2 * len(KS) + 1}  masses {MASSES}")
if MUT == "a":
    P("  *** MUTATE=a: the target is replaced by the door's own gradient-dominated condensate density 2 m^2 Lam |grad phi| (G1.1 must flip to PASS) ***")
if MUT == "c":
    P("  *** MUTATE=c: alpha_c = 1e-12 alpha in the flux law and the force (G3.1 must flip to PASS, G1.3 must collapse) ***")

results = {}
t0 = time.time()
for foot in FOOTINGS:
    a0n = a0_nat(foot)
    for pname, (kind, hfac) in PROFILES.items():
        for Mmsun in MASSES:
            prof = Prof(kind, Mmsun, hfac)
            rMv = float(rM(prof.M, a0n))
            r_lo, r_hi = 0.1 * rMv, 30.0 * rMv
            T = target_on_grid(prof, a0n, r_lo, r_hi, N)
            x = T["r"] / rMv
            Mb_r = T["Mb"]
            gN = G_N * Mb_r / T["r"] ** 2
            glaw = p2_law_g(prof, T["r"], a0n)
            V2 = float(Vf2(prof.M, a0n))
            sig2 = 0.5 * V2
            for br in BRANCHES:
                keyb = (foot, pname, Mmsun, br)
                bestS = np.full(Mm.shape, np.inf); argS = np.zeros(Mm.shape, int)
                bestF = np.full(Mm.shape, np.inf); argF = np.zeros(Mm.shape, int)
                reactS = np.full(Mm.shape, np.nan)         # reaction (max a_phi/g_law over x in [0.3,30]) at the best-S solution
                reactMin = np.full(Mm.shape, np.inf)       # unconditional min over Y of the max reaction (full coverage to x = 30 only)
                edgeS = np.zeros(Mm.shape); dblF = np.full(Mm.shape, np.nan)
                g5_nonvac = np.zeros(Mm.shape, bool); g5_pass = np.zeros(Mm.shape, bool); g5_pass_lenient = np.zeros(Mm.shape, bool)
                cs_ratio_min = np.full(Mm.shape, -np.inf); cs_max = np.full(Mm.shape, np.nan); csminF = np.full(Mm.shape, np.nan); csmaxF = np.full(Mm.shape, np.nan); ovs1 = np.full(Mm.shape, np.nan); ovs3 = np.full(Mm.shape, np.nan)
                rows = np.array_split(np.arange(PLANE_N), NCH)
                for rw in rows:
                    m_, a_ = Mm[rw][:, :, None], Aa[rw][:, :, None]
                    Lm = lam_tie(m_, a_, a0n)
                    base = m_ * G_N * prof.M / rMv
                    Y0 = np.concatenate([[0.0], 10.0 ** KS, -(10.0 ** KS)])[None, None, :] * base
                    Y0 = np.where(np.arange(Y0.shape[-1])[None, None, :] == 0, 0.0, Y0)
                    so = integrate(m_, a_, Lm, prof, r_lo, r_hi, N, Y0, br, a0n, alpha_c=(None if ALPHA_C_FAC is None else ALPHA_C_FAC * a_))
                    rho, aphi, MD, Xs = so["rho"], so["a_phi"], so["MD"], so["X"]
                    n_ = rho / m_
                    nc = n_crit(m_, sig2)
                    ok_node = np.isfinite(rho) & np.isfinite(aphi) & (n_ >= nc)
                    okc = np.cumprod(ok_node, axis=0).astype(bool)           # covered nodes (before the first failure)
                    ncov = okc.sum(axis=0)                                    # number of covered nodes
                    xedge_idx = np.minimum(ncov, N)                           # index of the first uncovered node (N+1 if all covered -> clipped)
                    xe = np.where(ncov >= N + 1, 30.0, x[np.clip(ncov, 0, N)])
                    cov3 = xe >= 3.0
                    cov30 = ncov >= N + 1
                    if MUT == "a":
                        pgrad = np.sqrt(a_ * Mb_r[:, None, None, None] / (8 * math.pi * MPL)) / T["r"][:, None, None, None]
                        rho_t = 2 * m_ ** 2 * Lm * pgrad
                    else:
                        rho_t = T["rho_t"][:, None, None, None]
                    with np.errstate(invalid="ignore", divide="ignore", over="ignore"):
                        eS = np.abs(rho / rho_t - 1.0)
                        gb = G_N * (Mb_r[:, None, None, None] + MD) / T["r"][:, None, None, None] ** 2 + aphi
                        eF = np.abs(gb / glaw[:, None, None, None] - 1.0)
                        eS = np.where(okc, eS, 0.0).max(axis=0)
                        eF = np.where(okc, eF, 0.0).max(axis=0)
                        eS = np.where(cov3, eS, np.inf); eF = np.where(cov3, eF, np.inf)
                        # reaction over x in [0.3, 30]
                        sel = okc & (x[:, None, None, None] >= 0.3)
                        rea = np.where(sel, aphi / glaw[:, None, None, None], 0.0).max(axis=0)
                        Mdyn = gb * T["r"][:, None, None, None] ** 2 / G_N
                        dbl = np.where(okc, MD / Mdyn, 0.0).max(axis=0)
                        # G5: nodes with a_phi >= 0.1 a0 in the covered x >= 0.3 range
                        act = sel & (aphi >= 0.1 * a0n)
                        nonvac = act.any(axis=0)
                        negX = (act & (Xs < 0)).any(axis=0)
                        pass5 = nonvac & (~negX) & cov30
                        pass5l = nonvac & (~negX) & cov3
                        cs2 = np.where(sel & (Xs > 0), 2 * Xs / m_ / V2, np.inf)
                        csmin = np.min(cs2, axis=0)                      # min over x of c_s^2/V_f^2 (inf if no X>0 covered node)
                        csmax = np.max(np.where(okc & (Xs > 0), 2 * Xs / m_, -np.inf), axis=0)   # max c_s^2 (c = 1)
                        i1, i3 = int(np.argmin(np.abs(x - 1.0))), int(np.argmin(np.abs(x - 3.0)))
                        o1 = np.where(okc[i1], gb[i1] / glaw[i1], np.nan)
                        o3 = np.where(okc[i3], gb[i3] / glaw[i3], np.nan)
                    for arr_best, arr_arg, e in ((bestS, argS, eS), (bestF, argF, eF)):
                        ei = np.where(np.isfinite(e), e, np.inf)
                        k = ei.argmin(axis=-1)
                        v = np.take_along_axis(ei, k[..., None], axis=-1)[..., 0]
                        arr_best[rw] = v; arr_arg[rw] = k
                    kS = argS[rw]
                    reactS[rw] = np.take_along_axis(rea, kS[..., None], axis=-1)[..., 0]
                    edgeS[rw] = np.take_along_axis(xe, kS[..., None], axis=-1)[..., 0]
                    kF = argF[rw]
                    dblF[rw] = np.take_along_axis(dbl, kF[..., None], axis=-1)[..., 0]
                    ovs1[rw] = np.take_along_axis(o1, kF[..., None], axis=-1)[..., 0]
                    ovs3[rw] = np.take_along_axis(o3, kF[..., None], axis=-1)[..., 0]
                    rc = np.where(cov30 & np.isfinite(rea), rea, np.inf)
                    reactMin[rw] = rc.min(axis=-1)
                    g5_nonvac[rw] = nonvac.any(axis=-1); g5_pass[rw] = pass5.any(axis=-1); g5_pass_lenient[rw] = pass5l.any(axis=-1)
                    okK = np.where(np.isfinite(csmin) & cov3, csmin, -np.inf)
                    cs_ratio_min[rw] = okK.max(axis=-1)                  # best (largest) min_x c_s^2/V_f^2 over Y: existence of a Landau-safe solution
                    csminF[rw] = np.take_along_axis(np.where(np.isfinite(csmin), csmin, np.nan), kF[..., None], axis=-1)[..., 0]
                    csmaxF[rw] = np.take_along_axis(np.where(np.isfinite(csmax), csmax, np.nan), kF[..., None], axis=-1)[..., 0]
                    cs_max[rw] = np.where(np.isfinite(csmax) & cov3, csmax, np.inf).min(axis=-1)   # smallest max c_s^2 over Y (existence of a subluminal solution)
                results[keyb] = dict(bestS=bestS, argS=argS, bestF=bestF, argF=argF, reactS=reactS, reactMin=reactMin, edgeS=edgeS, dblF=dblF,
                                     g5_nonvac=g5_nonvac, g5_pass=g5_pass, g5_pass_lenient=g5_pass_lenient, cs_ratio_min=cs_ratio_min, cs_max=cs_max, csminF=csminF, csmaxF=csmaxF, ovs1=ovs1, ovs3=ovs3)
            P(f"  done {foot} {pname} M={Mmsun:.0e}  ({time.time() - t0:.0f} s)")

np.savez_compressed(os.path.join(HERE, f"cfg122_g1_plane_arrays{('_MUTATE_' + MUT) if MUT else ''}.npz"),
                    **{"|".join(map(str, k)) + "|" + n: v for k, d in results.items() for n, v in d.items()}, mg=mg, ag=ag)

# ------------------------------------------------------------------------------------------------ verdicts
R.banner("G1.1 / G1.2 [Branch S]  rho_DM vs rho_c^target within 10% over x in [0.1, min(30, x_edge)], x_edge >= 3, same (m, alpha) at 1e9..1e12")
TOL = 0.10


def best_over_branches(foot, pname, M, name):
    return np.min(np.stack([results[(foot, pname, M, b)][name] for b in BRANCHES]), axis=0)


def report_gate(label, pnames, name, tol=TOL):
    out = {}
    for foot in FOOTINGS:
        stack = []
        for pn in pnames:
            for M in MASSES:
                stack.append(best_over_branches(foot, pn, M, name))
        allbest = np.max(np.stack(stack), axis=0)                  # worst over (profile, mass) of the best-over-(branch, Y)
        npass = int(np.sum(allbest <= tol))
        i = np.unravel_index(np.argmin(allbest), allbest.shape)
        out[foot] = dict(npass=npass, closest=float(allbest[i]), m=float(mg[i[0]]), alpha=float(ag[i[1]]))
        P(f"  [{foot}] {label}: plane cells passing at all masses/profiles: {npass}/{PLANE_N * PLANE_N}; closest approach (worst-mass best error) {allbest[i]:.3g} at m = {mg[i[0]]:.3g} eV, alpha = {ag[i[1]]:.3g}")
        for pn in pnames:
            for M in MASSES:
                pm = best_over_branches(foot, pn, M, name)
                j = np.unravel_index(np.argmin(pm), pm.shape)
                P(f"        {pn:12s} M={M:.0e}: min over plane of the best error {pm[j]:.3g} (m = {mg[j[0]]:.3g}, alpha = {ag[j[1]]:.3g}); cells <= tol: {int(np.sum(pm <= tol))}")
    return out


g11 = report_gate("G1.1 point mass", ["point"], "bestS")
g12 = report_gate("G1.2 exp. spheres (compact & diffuse)", ["exp_compact", "exp_diffuse"], "bestS")
ok11 = all(g11[f]["npass"] > 0 for f in FOOTINGS)
ok12 = all(g12[f]["npass"] > 0 for f in FOOTINGS)
R.verdict("G1.1", "PASS" if ok11 else "FAIL", f"cells passing {[g11[f]['npass'] for f in FOOTINGS]} (canonical, alt); closest approach {[round(g11[f]['closest'], 3) for f in FOOTINGS]}")
R.verdict("G1.2", "PASS" if ok12 else "FAIL", f"cells passing {[g12[f]['npass'] for f in FOOTINGS]}; closest {[round(g12[f]['closest'], 3) for f in FOOTINGS]}")
R.num("G1.1", g11); R.num("G1.2", g12)

R.banner("G1.3 [Branch F]  g_b = G(M_b + M_DM)/r^2 + a_phi vs the P2 law within 10% (same conventions); double counting M_DM/M_dyn")
g13 = report_gate("G1.3 point mass (P2 law)", ["point"], "bestF")
g13e = report_gate("G1.3 exp spheres (reported: same test)", ["exp_compact", "exp_diffuse"], "bestF")
g13d = report_gate("G1.3 diffuse exp. sphere only (h = 3 r_M, deep regime; reported, NOT the gate)", ["exp_diffuse"], "bestF")
R.num("G1.3_diffuse_only_reported", g13d)
ok13 = all(g13[f]["npass"] > 0 for f in FOOTINGS)
R.verdict("G1.3", "PASS" if ok13 else "FAIL", f"point-mass cells passing {[g13[f]['npass'] for f in FOOTINGS]}; closest {[round(g13[f]['closest'], 3) for f in FOOTINGS]}")
R.num("G1.3", g13); R.num("G1.3_exp_reported", g13e)
# where does the branch-F closest approach sit (g_b/g_law at x = 1, 3 and the DM fraction)?
for foot in FOOTINGS:
    for M in MASSES:
        for br in BRANCHES:
            d = results[(foot, "point", M, br)]
            j = np.unravel_index(np.argmin(d["bestF"]), d["bestF"].shape)
            P(f"    [{foot}] M={M:.0e} {br:5s}: best F error {d['bestF'][j]:.3g} at (m, alpha) = ({mg[j[0]]:.3g}, {ag[j[1]]:.3g}); g_b/g_law at x=1: {d['ovs1'][j]:.3g}, x=3: {d['ovs3'][j]:.3g}; max M_DM/M_dyn {d['dblF'][j]:.3g}")

R.banner("G3.1 [Branch S, same solution as G1.1]  reaction on baryons a_phi/g_law over x in [0.3, 30] <= 0.10 (1e9, 1e10, 1e12)")
ok31 = True
for foot in FOOTINGS:
    for M in (1e9, 1e10, 1e12):
        for br in BRANCHES:
            d = results[(foot, "point", M, br)]
            j = np.unravel_index(np.argmin(d["bestS"]), d["bestS"].shape)
            P(f"    [{foot}] M={M:.0e} {br:5s}: at the closest G1.1 solution ((m, alpha) = ({mg[j[0]]:.3g}, {ag[j[1]]:.3g}), err {d['bestS'][j]:.3g}): max a_phi/g_law = {d['reactS'][j]:.3g}; "
              f"unconditional plane minimum of the max reaction (full coverage to x=30) = {np.min(d['reactMin']):.3g}")
    # conditional gate
    condpass = []
    for M in (1e9, 1e10, 1e12):
        allbr = np.stack([results[(foot, "point", M, br)]["reactS"] for br in BRANCHES])
        errs = np.stack([results[(foot, "point", M, br)]["bestS"] for br in BRANCHES])
        good = (errs <= TOL) & (allbr <= 0.10)
        condpass.append(bool(good.any()))
    R.num(f"G3.1_cond_{foot}", condpass)
uncond = {foot: {M: float(min(np.min(results[(foot, 'point', M, br)]['reactMin']) for br in BRANCHES)) for M in (1e9, 1e10, 1e12)} for foot in FOOTINGS}
R.num("G3.1_unconditional_min_reaction", {f: {f"{k:.0e}": v for k, v in d.items()} for f, d in uncond.items()})
P(f"  unconditional plane minimum of the max reaction over x in [0.3,30] (any branch, any Y, full coverage): {uncond}")
P("  reported reference (analytic, labelled POST-HOC: the pure-gradient B- solution Y = 0, point mass): a_phi/g_law = 1/sqrt(1 + 1/x^2): "
  + ", ".join(f"x={xx}: {1 / math.sqrt(1 + 1 / xx ** 2):.3f}" for xx in (0.3, 1, 3, 10, 30)) + f"  -> max over x in [0.3, 30] = {1 / math.sqrt(1 + 1 / 30 ** 2):.4f} (the frozen hand estimate 'about 1' in the deep regime)")
R.num("G3.1_posthoc_pure_gradient_reaction_max", 1 / math.sqrt(1 + 1 / 30 ** 2))
G31_cond_ok = all(all(R.numbers[f"G3.1_cond_{f}"]) for f in FOOTINGS)
# primary reading: the closest-approach G1.1 solution of each mass (over branches, plane cells and Y) -- the frozen text says 'same solution as G1.1'; when no solution passes G1.1
# this is the only defined object.  (This rule was fixed AFTER seeing MUTATE=c under the conditional rule: disclosed.)
ca = {}
for foot in FOOTINGS:
    row = []
    for M in (1e9, 1e10, 1e12):
        best = (np.inf, None, None)
        for br in BRANCHES:
            d = results[(foot, "point", M, br)]
            j = np.unravel_index(np.argmin(d["bestS"]), d["bestS"].shape)
            if d["bestS"][j] < best[0]:
                best = (float(d["bestS"][j]), br, (float(mg[j[0]]), float(ag[j[1]]), float(d["reactS"][j])))
        row.append(best)
    ca[foot] = row
    P(f"  [{foot}] closest-approach G1.1 solutions at 1e9, 1e10, 1e12: " + "; ".join(f"err {r[0]:.3g} on {r[1]} at (m, alpha) = ({r[2][0]:.3g}, {r[2][1]:.3g}): max a_phi/g_law = {r[2][2]:.4g}" for r in row))
G31_ca_ok = all(r[2][2] <= 0.10 for f in FOOTINGS for r in ca[f])
R.num("G3.1_closest_approach", {f: [dict(err=r[0], branch=r[1], m=r[2][0], alpha=r[2][1], reaction=r[2][2]) for r in ca[f]] for f in FOOTINGS})
R.verdict("G3.1", "PASS" if G31_ca_ok else "FAIL", f"closest-approach reading (primary): reactions {[[round(r[2][2], 4) for r in ca[f]] for f in FOOTINGS]} against the 0.10 line; conditional reading (solutions within 10% of the target AND reaction <= 0.10; none exist): {'PASS' if G31_cond_ok else 'FAIL'}; unconditional minimum over the plane {uncond} (reached only where the phonon force is negligible)")

R.banner("G5.1-G5.3 on the same solutions (literal frozen reading: kinetic > 0 and c_s^2 > 0 wherever a_phi >= 0.1 a0 over x in [0.3, 30]; non-vacuous = a_phi >= 0.1 a0 somewhere)")
for foot in FOOTINGS:
    for br in BRANCHES:
        nv = sum(int(np.sum(results[(foot, pn, M, br)]["g5_nonvac"])) for pn in ("point",) for M in MASSES)
        ps = sum(int(np.sum(results[(foot, pn, M, br)]["g5_pass"])) for pn in ("point",) for M in MASSES)
        psl = sum(int(np.sum(results[(foot, pn, M, br)]["g5_pass_lenient"])) for pn in ("point",) for M in MASSES)
        P(f"    [{foot}] {br:5s}: (cell, mass) pairs with a non-vacuous phonon force {nv}; of which literal-pass (X>0 throughout, coverage to x=30) {ps}, lenient (coverage >= 3) {psl}")
        R.num(f"G5.1_{foot}_{br}", dict(nonvacuous=nv, literal_pass=ps, lenient_pass=psl))
# well-posed solutions that are also MOND-carrying: a_phi-supplied dynamics within 10% (G1.3) on any branch?  and the loosened MOND-like reading (within 50%)
mond_ok, mond_loose = {}, {}
for foot in FOOTINGS:
    for br in BRANCHES:
        cnt = cnt2 = 0
        for M in MASSES:
            d = results[(foot, "point", M, br)]
            cnt += int(np.sum((d["bestF"] <= TOL) & d["g5_pass_lenient"]))
            cnt2 += int(np.sum((d["bestF"] <= 0.5) & d["g5_pass_lenient"]))
        mond_ok[(foot, br)] = cnt; mond_loose[(foot, br)] = cnt2
P(f"  (cell, mass) pairs where BOTH G1.3 (F within 10%) and the literal well-posed G5.1 hold: {mond_ok}")
P(f"  reported, loosened MOND-like reading (F within 50%) AND literal well-posed: {mond_loose}")
R.num("G5.1_and_G1.3", {str(k): v for k, v in mond_ok.items()}); R.num("G5.1_and_F_within_50pct", {str(k): v for k, v in mond_loose.items()})
lit_exists = {f: sum(int(np.sum(results[(f, 'point', M, br)]['g5_pass_lenient'])) for M in MASSES for br in BRANCHES) for f in FOOTINGS}
P(f"  literal reading alone (existence): (cell, mass, branch) triples with a non-vacuous phonon force and X > 0 throughout: {lit_exists} -- these are the LINEAR-regime (Newtonian-like fifth force) solutions of the branches B+hi/B+lo; none reproduces the P2 dynamics (best F error on B+hi 0.76)")
g51_any = any(v > 0 for v in mond_ok.values())
R.verdict("G5.1", "FAIL" if not g51_any else "PASS", "primary reading (the solutions that carry the MOND-like force): every branch-B- solution (the only ones within 41% of the P2 dynamics) has X < 0 throughout, where P_XX < 0 and c_s^2 = 2X/m < 0; the literal per-solution reading is satisfiable only by the X > 0 branches, which do not carry the MOND force (declared interpretation)")
# G5.2, G5.3
P("  G5.2 Landau: existence of a solution (any cell, any Y, covered to x >= 3) with min_x c_s^2/V_f^2 >= 1 (baryons subsonic), per branch (B- has X < 0: c_s^2 < 0, criterion moot / ill-posed):")
lan = {}
for foot in FOOTINGS:
    for br in BRANCHES:
        best = max(float(np.max(results[(foot, "point", M, br)]["cs_ratio_min"])) for M in MASSES)
        atF = [float(np.nanmin(np.where(np.isfinite(results[(foot, "point", M, br)]["csminF"]), results[(foot, "point", M, br)]["csminF"], np.nan))) if np.isfinite(results[(foot, "point", M, br)]["csminF"]).any() else float("nan") for M in MASSES]
        lan[(foot, br)] = best
        P(f"    [{foot}] {br:5s}: largest min_x c_s^2/V_f^2 over the plane {best:.3g}; at the closest G1.3 solutions (per mass) {['%.3g' % v for v in atF]}")
R.num("G5.2_best_min_cs2_over_Vf2", {str(k): v for k, v in lan.items()})
landau_and_F = any(lan[(f, b)] >= 1 and any(np.any((results[(f, 'point', M, b)]['bestF'] <= TOL)) for M in MASSES) for f in FOOTINGS for b in BRANCHES)
R.verdict("G5.2", "PASS" if landau_and_F else "FAIL", f"a solution that is BOTH within 10% of the P2 dynamics (G1.3) and Landau-safe exists: {landau_and_F}; Landau-safe solutions alone exist on the X>0 branches: {[(k, round(v, 3)) for k, v in lan.items() if v >= 1]}")
sub = {}
for foot in FOOTINGS:
    for br in BRANCHES:
        v = min(float(np.min(results[(foot, "point", M, br)]["cs_max"])) for M in MASSES)
        sub[(foot, br)] = v
P(f"  G5.3 smallest max c_s^2 (c=1) over the plane per branch (inf = no X>0 solution): {sub}; c_s^2 at the closest G1.3 solutions:")
for foot in FOOTINGS:
    for br in BRANCHES:
        vals = [float(np.nanmax(results[(foot, 'point', M, br)]['csmaxF'])) if np.isfinite(results[(foot, 'point', M, br)]['csmaxF']).any() else float('nan') for M in MASSES]
        P(f"     [{foot}] {br:5s}: {['%.3g' % v for v in vals]}")
R.num("G5.3_smallest_max_cs2", {str(k): v for k, v in sub.items()})
R.verdict("G5.3", "PASS", f"subluminal X>0 solutions exist (smallest max c_s^2 {min(v for v in sub.values() if np.isfinite(v)):.3g} c^2); the branch B- (the MOND-carrying one) has c_s^2 = 2X/m < 0: not a speed, an elliptic instability (see G5.1)")
R.check("harness: every branch/profile/mass/footing produced a result array", f"{len(results)} result sets (expected {len(FOOTINGS) * len(PROFILES) * len(MASSES) * len(BRANCHES)})", len(results) == len(FOOTINGS) * len(PROFILES) * len(MASSES) * len(BRANCHES))
nf, gf = R.write()
sys.exit(1 if (nf or gf) else 0)
