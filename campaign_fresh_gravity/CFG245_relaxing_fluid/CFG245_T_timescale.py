#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG245 Gate T -- TIMESCALE (frozen criteria `CFG245_FROZEN_CRITERIA.md`, section 3, committed before this script).

The frozen simple relaxation model, order by order in Gamma*tau, applied to the committed CFG244 passive bound cumulative masses
(read-only JSON; no CFG118/CFG244 code is imported or run):
    R-FLUX-2:  M_c(<r;tau) = M_target + e (M_inf - M_target),  e = exp(-Gamma tau),  M_target = min(M_ph, S)
    R-FLUX-1:  M_c = M_inf + (1 - e) max(M_target - M_inf, 0)
T-G1 (BINDING): R_cum = M_c/M_ph in [0.90, 1.10] on every 0.1-dex bin centre in x = [0.3, 20], every mass, for at least one q, both footings,
                noise guard as CFG244 (a bin fails only beyond max(shell-bootstrap sd, |R_5k - R_20k|), both scaled by the relaxation factor).
T-RAR (reported): Delta = log10[(M_b+M_c)/(M_b+M_ph)] on x in [0.3, 10]; D1 = max|Delta|, D2 = max_x(max_M - min_M Delta); lines 0.048 / 0.10 dex.
T3 (reported, a prediction only, NEVER a data preference): delta(z) = 2 log10[f(z)/f(0)], f = 1 - exp(-Gamma t(z)).
Verdict uses the FAVOURABLE bracket tau_gal = t_0.  Score all three declared rates; a FAIL binds only if it fails for all three (both footings).

Run: ZF_REPO=<repo> python3 CFG245_T_timescale.py ; MUTATE=MT1|MT2a|MN1|MN2 python3 CFG245_T_timescale.py
Exit: main 0; MUTATE exits 1 when the control bites, 0 when it does not.
"""
import os, sys, math
sys.dont_write_bytecode = True
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG245_common as K

MUT = os.environ.get("MUTATE", "").strip()
SLUG = "CFG245_T_timescale"
R = K.Report(SLUG, MUT or None)
XC = K.XC
MASK_G1 = (XC >= 0.3) & (XC <= 20.0)
MASK_RAR = (XC >= 0.3) & (XC <= 10.0)
MASK_EXT = (XC > 10.0)
TAU_FAV, TAU_CEN, TAU_UNF = K.T0, 10.5, 7.0
LINE_STRICT, LINE_LOOSE = 0.048, 0.10
ZLIST = (0.3, 0.85, 1.5, 2.5, 4.4, 5.5)


def load(foot, kernel):
    """passive products with the kernel's own M_ph; returns {q: {M: dict}}"""
    out = {}
    for q in K.QS:
        out[q] = {}
        for M in K.MASSES:
            p = K.passive(M, q, foot)
            Mph = M * K.Mph_point(p["x"], kernel)
            sc = p["Mph"] / Mph
            d = dict(p)
            d.update(Mph=Mph, R=p["Minf"] / Mph, R5=p["R5"] * sc, boot=p["boot"] * sc)
            if MUT == "MT1":
                d["Minf"] = Mph.copy(); d["R"] = np.ones_like(Mph); d["R5"] = np.ones_like(Mph)
            out[q][M] = d
    return out


def g1_q(PQ, e, mode, mask=MASK_G1):
    """T-G1 for one bracket q across the four masses: (pass, max |R-1|, n guarded failures)"""
    maxdev, nfail, nfail_ng = 0.0, 0, 0
    for M, p in PQ.items():
        Mc = K.relaxed_Mc(p["Minf"], p["Mph"], p["S"], e, mode)
        Rc = Mc / p["Mph"]
        d = np.abs(Rc - 1.0)[mask]
        fac = e if mode == "two" else 1.0
        guard = (np.maximum(p["boot"], np.abs(p["R"] - p["R5"])) * fac)[mask]
        ex = np.maximum(0.0, d - 0.10)
        nfail += int((ex > guard).sum()); nfail_ng += int((ex > 0).sum())
        maxdev = max(maxdev, float(d.max()))
    return nfail == 0, maxdev, nfail, nfail_ng


def g1(P, e, mode):
    res = {q: g1_q(P[q], e, mode) for q in K.QS}
    ok = any(v[0] for v in res.values())
    return ok, res


def rar_q(PQ, e, mode, mask=MASK_RAR):
    Dl = []
    for M, p in PQ.items():
        Mc = K.relaxed_Mc(p["Minf"], p["Mph"], p["S"], e, mode)
        Dl.append(K.delta_dex(Mc, p["Mph"], M)[mask])
    Dl = np.array(Dl)
    D1 = float(np.abs(Dl).max()); D2 = float((Dl.max(axis=0) - Dl.min(axis=0)).max())
    return D1, D2, Dl


def rar(P, e, mode, mask=MASK_RAR):
    res = {q: rar_q(P[q], e, mode, mask)[:2] for q in K.QS}
    cat = "FAIL"
    if any(a <= LINE_STRICT and b <= LINE_STRICT for a, b in res.values()):
        cat = "PASS"
    elif any(a <= LINE_LOOSE and b <= LINE_LOOSE for a, b in res.values()):
        cat = "AMBIGUOUS"
    return cat, res


def req_gt(fn, grid):
    """smallest Gamma*tau in grid such that fn(e) holds at it and at every larger grid value (robust threshold)"""
    ok = [fn(math.exp(-g)) for g in grid]
    last = None
    for i in range(len(grid) - 1, -1, -1):
        if ok[i]:
            last = grid[i]
        else:
            break
    return last


GRID = np.round(np.arange(0.0, 30.0001, 0.01), 4)


def run(kernel, foot, mode="two", tau=TAU_FAV, gamma_override=None, full=True):
    P = load(foot, kernel)
    rts = K.rates(foot)
    out = {}
    for c in K.CAND:
        G = rts[c] if gamma_override is None else gamma_override
        gt = G * tau
        e = math.exp(-gt) if not math.isinf(gt) else 0.0
        ok, res = g1(P, e, mode)
        cat, rr = rar(P, e, mode)
        d = dict(rate=G, gt=gt, e=e, G1=("PASS" if ok else "FAIL"),
                 G1_by_q={str(q): dict(ok=v[0], maxdev=v[1], guarded_fail_bins=v[2], unguarded_fail_bins=v[3]) for q, v in res.items()},
                 RAR=cat, RAR_by_q={str(q): dict(D1=v[0], D2=v[1]) for q, v in rr.items()})
        if full:
            # required Gamma*tau (in Gamma*tau units and in H_Lambda at tau = t_0), best q for each line
            def fg1(ee, q=None):
                return any(g1_q(P[qq], ee, mode)[0] for qq in K.QS)
            d["req_G1"] = req_gt(fg1, GRID)
            def f048(ee):
                return any(a <= LINE_STRICT and b <= LINE_STRICT for a, b in (rar_q(P[qq], ee, mode)[:2] for qq in K.QS))
            def f10(ee):
                return any(a <= LINE_LOOSE and b <= LINE_LOOSE for a, b in (rar_q(P[qq], ee, mode)[:2] for qq in K.QS))
            d["req_RAR048"] = req_gt(f048, GRID)
            d["req_RAR10"] = req_gt(f10, GRID)
            # extension [10,30], capped target
            ext = {}
            for q in K.QS:
                Dl = np.array([K.delta_dex(K.relaxed_Mc(p["Minf"], p["Mph"], p["S"], e, mode), p["Mph"], M)[MASK_EXT] for M, p in P[q].items()])
                ext[str(q)] = dict(D1=float(np.abs(Dl).max()), D2=float((Dl.max(axis=0) - Dl.min(axis=0)).max()))
            d["RAR_ext_10_30"] = ext
        out[c] = d
    return out


def main():
    mut_tag = f"  (MUTATE {MUT})" if MUT else ""
    R.banner("CFG245 Gate T -- TIMESCALE (frozen model; point cores; committed CFG244 passive products read-only)" + mut_tag)
    R.P(f"  H_Lambda = {K.HL:.6f} /Gyr (1/H_L = {1/K.HL:.3f} Gyr), t_0 = {K.T0:.4f} Gyr (Planck-2018 inputs H0 = {K.H0}, Omega_m = {K.OM}), rho_Lambda = {K.RHO_L:.3f} Msun/kpc^3")
    R.P(f"  a0 footings: canonical {K.A0_SI['canonical']:.4e}, alt {K.A0_SI['alt']:.4e} m/s^2; kappa = 1/2 FITTED; masses {', '.join(f'{m:.0e}' for m in K.MASSES)} Msun; q = {K.QS}")
    R.P(f"  T-G1 grid: {int(MASK_G1.sum())} bin centres x in [{XC[MASK_G1].min():.3f}, {XC[MASK_G1].max():.2f}]; T-RAR grid x in [{XC[MASK_RAR].min():.3f}, {XC[MASK_RAR].max():.2f}]")

    kernel_primary = "P2"
    allres = {}
    # ---------------------------------------------------------------- controls
    R.banner("CONTROLS (reproduction)")
    ctl = {}
    # C-T1 tabulated residuals
    tab = {"G-H": {"canonical": 0.455, "alt": 0.455}, "G-a": {"canonical": 0.873, "alt": 0.849}, "G-b": {"canonical": 0.762, "alt": 0.720}}
    ok_t1 = True
    for f in K.FOOTS:
        for c in K.CAND:
            e = math.exp(-K.rates(f)[c] * K.T0)
            ok_t1 &= abs(e - tab[c][f]) < 0.002
    ctl["C-T1"] = ok_t1
    R.cell("C-T1 residual fractions e^(-Gamma t_0) equal the frozen table (0.455 / 0.873,0.849 / 0.762,0.720 within 0.002)", "PASS" if ok_t1 else "FAIL",
           "; ".join(f"{c} {f}: {math.exp(-K.rates(f)[c]*K.T0):.4f}" for c in K.CAND for f in K.FOOTS))
    # C-T0: Gamma = 0 reproduces CFG244 numbers
    A2mask = (XC >= 0.3) & (XC <= 30.0)
    rng = {}
    for f in K.FOOTS:
        mx = []
        for q in K.QS:
            m = 0.0
            for M in K.MASSES:
                p = K.passive(M, q, f)
                m = max(m, float(np.abs(p["R"] - 1.0)[A2mask].max()))
            mx.append(m)
        rng[f] = (min(mx), max(mx))
    comm = {"canonical": (8.0, 10.7), "alt": (6.8, 9.8)}
    ok_a2 = all(abs(round(rng[f][0], 1) - comm[f][0]) < 1e-9 and abs(round(rng[f][1], 1) - comm[f][1]) < 1e-9 for f in K.FOOTS)
    # exponent p from the rank estimator R_s (kpc) vs M
    pcomm = {0.05: 0.343, 0.1: 0.339, 0.2: 0.327}
    pm = {}
    for q in K.QS:
        Rs = [K.passive(M, q, "canonical")["Rs_z0"] for M in K.MASSES]
        pm[q] = float(np.polyfit(np.log10(K.MASSES), np.log10(Rs), 1)[0])
    ok_p = all(abs(pm[q] - pcomm[q]) < 6e-4 for q in K.QS)
    # target identity vs the sims' own target
    dd = 0.0
    for q in K.QS:
        for M in K.MASSES:
            p = K.passive(M, q, "canonical")
            dd = max(dd, float(np.abs(p["McT"] / p["Mph"] - 1).max()))
    ok_tgt = dd < 1e-6
    ctl["C-T0"] = bool(ok_a2 and ok_p and ok_tgt)
    R.cell("C-T0 Gamma = 0 reproduces CFG244's committed Gate A numbers (README.md lines 27, 88; displayed precision) and its target",
           "PASS" if ctl["C-T0"] else "FAIL",
           f"A2 largest |ratio-1| over brackets: canonical {rng['canonical'][0]:.2f}-{rng['canonical'][1]:.2f} (committed 8.0-10.7), alt {rng['alt'][0]:.2f}-{rng['alt'][1]:.2f} (6.8-9.8); "
           f"exponent p = {pm[0.05]:.4f} / {pm[0.1]:.4f} / {pm[0.2]:.4f} (committed 0.343 / 0.339 / 0.327); max |M_ph(mine)/target_sims - 1| = {dd:.2e} (< 1e-6). "
           "The frozen text said 'to 1e-9': the committed README quotes 1-3 decimals, so the reproduction is at DISPLAYED precision (disclosed).")

    # ---------------------------------------------------------------- main numbers
    kernels = ["P2", "nu_mono"] if MUT in ("", "MN1") else ["P2"]
    for kern in kernels:
        for f in K.FOOTS:
            allres[(kern, f)] = run(kern, f)
    for mode in ("one",):
        for f in K.FOOTS:
            allres[("P2-R-FLUX-1", f)] = run("P2", f, mode="one")

    # ---------------------------------------------------------------- T-G1 first
    R.banner("T-G1 (BINDING: shared G1 line, cumulative amount R_cum in [0.90, 1.10], x in [0.3, 20]) -- Gamma*tau and residual fraction per candidate")
    R.P(f"  favourable bracket tau_gal = t_0 = {TAU_FAV:.3f} Gyr (relaxation active since the start: deliberately generous)")
    R.P("  kernel P2, R-FLUX-2 (primary)")
    R.P(f"  {'cand':5s} {'footing':10s} {'rate /Gyr':>11s} {'Gamma*tau':>10s} {'residual e':>11s} {'T-G1':>6s} {'max|R-1| q=.05/.1/.2':>26s} {'req Gamma*tau':>14s} {'req /H_L':>9s}")
    for f in K.FOOTS:
        for c in K.CAND:
            d = allres[("P2", f)][c]
            md = "/".join(f"{d['G1_by_q'][str(q)]['maxdev']:.2f}" for q in K.QS)
            rq = d["req_G1"]
            R.P(f"  {c:5s} {f:10s} {d['rate']:11.6f} {d['gt']:10.4f} {d['e']:11.4f} {d['G1']:>6s} {md:>26s} {('%.2f' % rq) if rq is not None else 'none<=30':>14s} {('%.2f' % (rq / (K.HL * TAU_FAV))) if rq is not None else '-':>9s}")
    R.P("  (the unguarded failing-bin count and the guarded count per q are in the JSON; the noise guard never rescued a bin if the two counts are equal)")
    ng = {(f, c): [allres[('P2', f)][c]['G1_by_q'][str(q)]['guarded_fail_bins'] for q in K.QS] for f in K.FOOTS for c in K.CAND}
    nu = {(f, c): [allres[('P2', f)][c]['G1_by_q'][str(q)]['unguarded_fail_bins'] for q in K.QS] for f in K.FOOTS for c in K.CAND}
    R.P("  guarded / unguarded failing bins (q = .05/.1/.2), all masses pooled: " + "; ".join(f"{c} {f}: {ng[(f,c)]} / {nu[(f,c)]}" for f in K.FOOTS for c in K.CAND))

    # verdict per candidate: FAIL on both footings => FAIL; PASS on both => PASS; else AMBIGUOUS
    cand_cat = {}
    for c in K.CAND:
        cs = [allres[("P2", f)][c]["G1"] for f in K.FOOTS]
        cand_cat[c] = "FAIL" if all(x == "FAIL" for x in cs) else ("PASS" if all(x == "PASS" for x in cs) else "AMBIGUOUS")
    binding = all(v == "FAIL" for v in cand_cat.values())
    survivors = [c for c, v in cand_cat.items() if v != "FAIL"]
    R.P("")
    R.cell("T-G1 verdict (a FAIL binds only if it fails for ALL THREE declared rates on BOTH footings)", "FAIL (BINDING)" if binding else "NOT BINDING",
           "per candidate: " + ", ".join(f"{c} {v}" for c, v in cand_cat.items()) + ("; survivors carried: " + (", ".join(survivors) if survivors else "none")))

    # ---------------------------------------------------------------- T-RAR
    R.banner("T-RAR (reported; the owner's question: the RAR at SPARC precision?), x in [0.3, 10], D1 = max|Delta|, D2 = mass spread at fixed x (dex)")
    R.P("  lines: PASS <= 0.048 (record's RAR intrinsic bound), AMBIGUOUS <= 0.10 (SPARC rms), FAIL otherwise; a lean is not a pass")
    R.P(f"  {'kernel/mode':14s} {'cand':5s} {'footing':10s} {'D1/D2 q=.05':>14s} {'q=.1':>14s} {'q=.2':>14s} {'category':>10s} {'req Gt(.048)':>13s} {'req Gt(.10)':>12s} {'req/H_L (.048;.10)':>20s}")
    for key in [("P2", None), ("nu_mono", None), ("P2-R-FLUX-1", None)]:
        if key[0] == "nu_mono" and ("nu_mono", "canonical") not in allres:
            continue
        for f in K.FOOTS:
            for c in K.CAND:
                d = allres[(key[0], f)][c]
                s = " ".join(f"{d['RAR_by_q'][str(q)]['D1']:6.3f}/{d['RAR_by_q'][str(q)]['D2']:5.3f}" for q in K.QS)
                r1, r2 = d["req_RAR048"], d["req_RAR10"]
                R.P(f"  {key[0]:14s} {c:5s} {f:10s} {s} {d['RAR']:>10s} {('%.2f' % r1) if r1 is not None else 'none':>13s} {('%.2f' % r2) if r2 is not None else 'none':>12s} "
                    f"{(('%.2f' % (r1/(K.HL*TAU_FAV))) if r1 is not None else '-') + ' ; ' + (('%.2f' % (r2/(K.HL*TAU_FAV))) if r2 is not None else '-'):>20s}")
    R.P("  extension x in [10, 28.2] with the supply-capped target (reported): D1/D2 per q, P2 two-sided")
    for f in K.FOOTS:
        for c in K.CAND:
            d = allres[("P2", f)][c]["RAR_ext_10_30"]
            R.P(f"    {c:5s} {f:10s} " + "  ".join(f"q={q}: {d[str(q)]['D1']:.3f}/{d[str(q)]['D2']:.3f}" for q in K.QS))
    # sensitivities of tau
    R.P("  sensitivity (reported, never in the verdict): tau_gal = 10.5 Gyr (central) and 7 Gyr (unfavourable), P2 two-sided")
    sens = {}
    for tau in (TAU_CEN, TAU_UNF):
        for f in K.FOOTS:
            r = run("P2", f, tau=tau, full=False)
            sens[(tau, f)] = r
            R.P(f"    tau={tau:5.1f} {f:10s} " + "; ".join(f"{c}: Gt={r[c]['gt']:.3f} e={r[c]['e']:.3f} G1 {r[c]['G1']} RAR {r[c]['RAR']} D1(.1)={r[c]['RAR_by_q']['0.1']['D1']:.3f}" for c in K.CAND))

    # ---------------------------------------------------------------- the deviation table at the extremes (for comparison with the frozen hand numbers)
    R.banner("Hand-estimate comparison: Delta (dex) at x about 1.12 and x about 28.2, q = 0.1, canonical (frozen: G-H +0.017..+0.165 / -0.138..-0.072; G-a +0.033..+0.276 / -0.321..-0.152)")
    iq = 0.1
    hand = {}
    for c in K.CAND:
        e = allres[("P2", "canonical")][c]["e"]
        v1, v2 = [], []
        for M in K.MASSES:
            p = K.passive(M, iq, "canonical")
            Mc = K.relaxed_Mc(p["Minf"], p["Mph"], p["S"], e, "two")
            dl = K.delta_dex(Mc, p["Mph"], M)
            v1.append(dl[10]); v2.append(dl[24])
        hand[c] = (min(v1), max(v1), min(v2), max(v2))
        R.P(f"  {c}: x=1.12  Delta in [{min(v1):+.3f}, {max(v1):+.3f}];  x=28.2  Delta in [{min(v2):+.3f}, {max(v2):+.3f}]  (e = {e:.3f})")
    pas = {M: K.passive(M, iq, "canonical") for M in K.MASSES}
    R.P("  passive R_cum at x=1.12: " + ", ".join(f"{M:.0e}: {pas[M]['R'][10]:.3f}" for M in K.MASSES) + "; at x=28.2: " + ", ".join(f"{M:.0e}: {pas[M]['R'][24]:.3f}" for M in K.MASSES))

    # ---------------------------------------------------------------- T3
    R.banner("T3 -- a0_eff(z) of this class (a PREDICTION of the model; it says NOTHING about which a0(z) law the data favour)")
    R.P("  delta(z) = 2 log10[f(z)/f(0)], f(z) = 1 - exp(-Gamma t(z)) (deep regime: M_c ~ sqrt(a0), a0_eff ~ f^2); Planck-2018 t(z)")
    rival = {z: math.log10(math.sqrt(K.OM * (1 + z) ** 3 + K.OL)) for z in ZLIST}
    tlaw = {z: math.log10(K.t_of_z(z) / K.T0) for z in ZLIST}
    R.P("  record's scored laws, numbers only: flat 0.00; a0 ~ H(z): " + ", ".join(f"z={z}: {rival[z]:+.2f}" for z in ZLIST) + "; T law t(z)/t_0: " + ", ".join(f"z={z}: {tlaw[z]:+.2f}" for z in ZLIST))
    t3 = {}
    for f in K.FOOTS:
        for c in K.CAND:
            G = K.rates(f)[c]
            row = {}
            for z in ZLIST:
                fz = 1 - math.exp(-G * K.t_of_z(z)); f0 = 1 - math.exp(-G * K.T0)
                row[z] = 2 * math.log10(fz / f0)
            t3[(f, c)] = row
            d25 = row[2.5]
            cat = "INDISTINGUISHABLE FROM FLAT" if abs(d25) < 0.10 else ("INSIDE THE CALIBRATION BAND (non-diagnostic)" if abs(d25) <= 0.30 else
                  "OUTSIDE THE CALIBRATION BAND: steeper than the T law, opposite in sign to a0 proportional to H(z)")
            R.P(f"  {c:5s} {f:10s} " + " ".join(f"z={z}: {row[z]:+.3f}" for z in ZLIST) + f"   -> {cat}")
    R.P("  the z = 0 value f(0) < 1 means the fitted kappa would be kappa_true f(0); kappa = 1/2 stays FITTED.  Reading: prediction only; the record's own T-law verdict was not robust (STANDING_2026-09-29.md:104).")

    # ---------------------------------------------------------------- MUTATE
    cells = dict(T_G1_binding=("FAIL" if binding else "NOT BINDING"))
    summary = dict(binding_fail=bool(binding) and not MUT, cand_cat=cand_cat, survivors=survivors)
    if MUT:
        base_cat = ("FAIL" if binding else "NOT BINDING")
        if MUT in ("MT1", "MT2a"):
            if MUT == "MT2a":
                # Gamma = infinity: e = 0 for every candidate
                cc = {}
                for f in K.FOOTS:
                    r = run("P2", f, gamma_override=float("inf"), full=False)
                    for c in K.CAND:
                        cc.setdefault(c, []).append(r[c]["G1"])
                mut_cat = {c: ("FAIL" if all(x == "FAIL" for x in v) else ("PASS" if all(x == "PASS" for x in v) else "AMBIGUOUS")) for c, v in cc.items()}
                mut_binding = all(v == "FAIL" for v in mut_cat.values())
            else:
                mut_binding = binding        # MT1 already fed the target as the passive state inside load()
            R.P(f"  MUTATE {MUT}: T-G1 binding verdict {'FAIL' if mut_binding else 'NOT BINDING (PASS)'} (baseline frozen expectation: FAIL)")
            bites = (not mut_binding)
            R.finish(dict(binding_fail=False, mutate_bites=bool(bites)))
            K.exit_mutate(bites, True)
        if MUT == "MN1":
            cats_p = tuple(allres[("P2", "canonical")][c]["RAR"] for c in K.CAND)
            cats_m = tuple(allres[("nu_mono", "canonical")][c]["RAR"] for c in K.CAND)
            R.P(f"  MUTATE MN1: T-RAR categories P2 {cats_p} vs nu_mono {cats_m}")
            bites = cats_p != cats_m
            R.finish(dict(binding_fail=False, mutate_bites=bool(bites)))
            K.exit_mutate(bites, False)
        if MUT == "MN2":
            cats_c = tuple(allres[("P2", "canonical")][c]["G1"] for c in K.CAND)
            cats_a = tuple(allres[("P2", "alt")][c]["G1"] for c in K.CAND)
            R.P(f"  MUTATE MN2: T-G1 categories canonical {cats_c} vs alt {cats_a}")
            bites = cats_c != cats_a
            R.finish(dict(binding_fail=False, mutate_bites=bool(bites)))
            K.exit_mutate(bites, False)
        raise SystemExit(f"MUTATE {MUT} is not a Gate T control")

    summary.update(cells=cells, controls=ctl, hand=hand)
    # JSON numbers
    R.numbers = dict(
        T0=K.T0, HL=K.HL,
        T_G1={f"{f}|{c}": {k: v for k, v in allres[('P2', f)][c].items() if k in ("rate", "gt", "e", "G1", "G1_by_q", "req_G1", "req_RAR048", "req_RAR10")} for f in K.FOOTS for c in K.CAND},
        T_RAR={f"{key}|{f}|{c}": {k: v for k, v in allres[(key, f)][c].items() if k in ("RAR", "RAR_by_q", "RAR_ext_10_30", "req_RAR048", "req_RAR10")}
               for key in ("P2", "nu_mono", "P2-R-FLUX-1") for f in K.FOOTS for c in K.CAND},
        T_G1_mode_one={f"{f}|{c}": allres[("P2-R-FLUX-1", f)][c]["G1"] for f in K.FOOTS for c in K.CAND},
        T3={f"{f}|{c}": {str(z): v for z, v in row.items()} for (f, c), row in t3.items()},
        laws=dict(rival={str(z): v for z, v in rival.items()}, T={str(z): v for z, v in tlaw.items()}),
        sens={f"{tau}|{f}": {c: dict(gt=r[c]["gt"], e=r[c]["e"], G1=r[c]["G1"], RAR=r[c]["RAR"]) for c in K.CAND} for (tau, f), r in sens.items()})
    R.cell("Gate T outcome", "FAIL (BINDING)" if binding else "PASS/AMBIGUOUS for " + ", ".join(survivors),
           "T-G1 per candidate: " + ", ".join(f"{c} {v}" for c, v in cand_cat.items()))
    R.finish(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
