#!/usr/bin/env python3
"""CFG238 MUTATE controls M1-M8 (frozen section 7). Usage: MUTATE=k python3 CFG238_MUTATE.py. Exit 1 when the control bites (a pass line fails as frozen), 0 when it does not bite."""
import sys
from CFG238_common import *
import CFG238_d_anchor as DA

mode = os.environ.get("MUTATE")
if mode not in [str(i) for i in range(1, 9)]:
    raise SystemExit("set MUTATE=1..8")
outp, jp = out_paths("CFG238_MUTATE")
T = Tee(outp)
banner(T, f"CFG238 MUTATE M{mode}")
R = {}
bites = []   # (line id, bool failed-as-frozen)


def bite(lid, failed, msg):
    bites.append((lid, failed))
    T(f"  [{'BITE (line fails)' if failed else 'no bite (line holds)'}] {lid}: {msg}")


SW = {("ad", "aCO"): (0.056, 0.050), ("dax", "aCO"): (0.004, 0.072), ("xa", "aCO"): (-0.002, 0.066), ("dax", "XCI"): (-0.039, 0.080),
      ("xa", "XCI"): (-0.026, 0.064), ("xd", "XCI"): (-0.104, 0.066), ("ad", "kappaH"): (-0.056, 0.042), ("dax", "GDR"): (-0.025, 0.078), ("xd", "GDR"): (-0.084, 0.066)}
SO = {("ad", "aCO"): (-0.124, 0.032), ("ad", "kappaH"): (0.117, 0.028), ("dax", "XCI"): (0.181, 0.043), ("dax", "GDR"): (0.216, 0.052)}

if mode == "1":
    T("M1: add 0.25 log10(1+z) to every log alpha_CO of the ad and daX tables")
    for combo in (("ad", "aCO"), ("dax", "aCO")):
        A = factor_arrays(*combo, "fb")
        m = np.isfinite(A["L"])
        base = slope_fit(A, True, 4000, 238)
        A2 = dict(A); A2["y"] = A["y"] + 0.25 * A["x"]
        mut = slope_fit(A2, True, 4000, 238)
        dshift = mut["b"] - base["b"]
        T(f" {combo}: b {base['b']:+.6f} -> {mut['b']:+.6f} (shift {dshift:+.9f}; OLS linearity predicts +0.25); SD {mut['b_boot_sd']:.3f}; |b/SD| {abs(mut['b'] / mut['b_boot_sd']):.1f}; c unchanged: {abs(mut['c'] - base['c']) < 1e-9}")
        bite(f"slope-consistent-with-zero:{combo}", abs(mut["b"]) >= 2 * mut["b_boot_sd"], f"|b/SD| = {abs(mut['b'] / mut['b_boot_sd']):.1f} >= 2")
        R[str(combo)] = dict(shift=dshift)
    # identity of the tampered alpha_CO in the ad table: residual logMH2 - (log aCO + logLCO + J)
    rows, _ = joined("ad")
    res0, res1 = [], []
    for r in rows:
        a, L, J, mh = fl(r["aCO"]), fl(r["logLCO"]), fl(r["JCorr"]), fl(r["logMH2"])
        if None in (a, L, J, mh) or a <= 0:
            continue
        res0.append(mh - (math.log10(a) + L + J)); res1.append(mh - (math.log10(a) + 0.25 * math.log10(1 + r["_z"]) + L + J))
    bite("identity-residual-SD<0.01", np.std(res1, ddof=1) >= 0.01, f"ad CO identity SD {np.std(res0, ddof=1):.5f} -> {np.std(res1, ddof=1):.4f} with the injected factor drift")
    R["identity_sd"] = (float(np.std(res0, ddof=1)), float(np.std(res1, ddof=1)))

elif mode == "2":
    T("M2: permute z globally among galaxies (seed 2383) in every table")
    rng = np.random.default_rng(2383)
    for combo in COMBOS:
        A = factor_arrays(*combo, False)
        z = A["z"].copy(); z = z[rng.permutation(len(z))]
        A2 = dict(A); A2["z"] = z; A2["x"] = np.log10(1 + z)
        wo = slope_fit(A2, False, 4000, 238)
        wl = slope_fit(A2, True, 4000, 238)
        T(f" {combo}: without L_IR b {wo['b']:+.3f} +- {wo['b_boot_sd']:.3f} ({wo['b'] / wo['b_boot_sd']:+.1f} sigma); with L_IR b {wl['b']:+.3f}, c {wl['c']:+.3f} +- {wl['c_boot_sd']:.3f}")
        if combo in SO:
            bite(f"H-B4:{combo}", not (abs(wo["b"] / wo["b_boot_sd"]) >= 2), f"shuffled-z without-L slope {wo['b'] / wo['b_boot_sd']:+.1f} sigma (README-like >= 2 sigma needed)")
        if combo == ("ad", "aCO"):
            T(f"   L_IR coefficient with shuffled z: {wl['c']:+.3f} (README -0.058 +- 0.012; estimate said it stays)")
            bite("H-B5", abs(wl["c"] + 0.058) > 0.01, f"L_IR coefficient {wl['c']:+.3f} vs -0.058 (tolerance 0.01): the frozen expectation was that it stays")

elif mode == "3":
    T("M3: swap tracers: Stripe82 CO <-> dust; NOEMA3D CO <-> [CI]")
    d, S = s82_d()
    ds = -d
    st0, st1 = msd(d), msd(ds)
    T(f" Stripe82 mean {st0['mean']:+.4f} -> {st1['mean']:+.4f}; K {Kfun(st0['mean'], st0['se']):.6f} -> {Kfun(st1['mean'], st1['se']):.6f}")
    bite("H-A2a sign", not abs(st1["mean"] - (-0.068)) <= 0.01, f"mean {st1['mean']:+.3f} vs README -0.068")
    bite("H-A2d K (expected to hold)", not abs(Kfun(st1["mean"], st1["se"]) - 0.038) <= 0.01, "K is symmetric in the sign of mu (documented blindness)")
    NO_ = [r for r in load_noema() if r["ok"] == 1]
    cc = np.array([r["CO_t1"] - r["CI"] for r in NO_]); cc2 = -cc
    T(f" NOEMA3D CO-CI mean {cc.mean():+.4f} -> {cc2.mean():+.4f}; K {Kfun(cc.mean(), msd(cc)['se']):.6f} -> {Kfun(cc2.mean(), msd(cc2)['se']):.6f}")
    bite("H-A4d sign", not abs(cc2.mean() - 0.126) <= 0.01, f"CO-CI {cc2.mean():+.3f} vs README +0.126")
    bite("H-A4f K (expected to hold)", not abs(Kfun(cc2.mean(), msd(cc2)["se"]) - 0.070) <= 0.01, "K unchanged")

elif mode == "4":
    T("M4: common-mode +0.30 dex on all three NOEMA3D tracer masses; z-dependent common mode 0.30 log10(1+z) on all Dunne masses; +0.30 dex on gas masses in the anchors")
    NO_ = [r for r in load_noema() if r["ok"] == 1]
    cd0 = np.array([r["CO_t1"] - r["dust"] for r in NO_]); cc0 = np.array([r["CO_t1"] - r["CI"] for r in NO_]); id0 = np.array([r["CI"] - r["dust"] for r in NO_])
    cd1 = np.array([(r["CO_t1"] + 0.3) - (r["dust"] + 0.3) for r in NO_]); cc1 = np.array([(r["CO_t1"] + 0.3) - (r["CI"] + 0.3) for r in NO_]); id1 = np.array([(r["CI"] + 0.3) - (r["dust"] + 0.3) for r in NO_])
    dmax = max(np.abs(cd1 - cd0).max(), np.abs(cc1 - cc0).max(), np.abs(id1 - id0).max())
    h0 = np.array(hat(cc0, cd0, id0)); h1 = np.array(hat(cc1, cd1, id1))
    T(f" max change of any pair difference {dmax:.2e}; hat variances change {np.abs(h1 - h0).max():.2e}")
    bite("agreement-unchanged (expected to hold: the diagnostic is blind)", dmax > 1e-9 or np.abs(h1 - h0).max() > 1e-9, "d_AB and hat unchanged to 1e-9")
    # z-dependent common mode in Dunne tables: the raw luminosity ratios and identity residuals are unchanged by construction
    rows, _ = joined("ad")
    r0, r1 = [], []
    for r in rows:
        l8, lc, J = fl(r["logL850"]), fl(r["logLCO"]), fl(r["JCorr"])
        if None in (l8, lc, J):
            continue
        r0.append(l8 - lc - J); r1.append((l8 + 0.3 * math.log10(1 + r["_z"])) - (lc + 0.3 * math.log10(1 + r["_z"])) - J)
    T(f" raw ratio log(L850/L'CO) change under a common z-dependent shift of both luminosities: {np.abs(np.array(r1) - np.array(r0)).max():.2e}")
    bite("raw-ratio-unchanged (expected to hold)", np.abs(np.array(r1) - np.array(r0)).max() > 1e-9, "shared shift cancels in the ratio")
    # anchors
    q0 = DA.amv_q(0.0)[0]; q1 = DA.amv_q(0.3)[0]
    s0 = DA.s82_q(0.0)[0]; s1 = DA.s82_q(0.3)[0]
    f0, f1 = float((q0 < 0).mean()), float((q1 < 0).mean())
    g0, g1 = float((s0 < 0).mean()), float((s1 < 0).mean())
    T(f" anchor inequality, share violating: Amvrosiadis {f0:.3f} -> {f1:.3f}; Stripe82 {g0:.3f} -> {g1:.3f}")
    bite("anchor-line (share violating must change)", (f1 - f0) >= 0.05 or (g1 - g0) >= 0.05, f"Amvrosiadis {f0:.3f} -> {f1:.3f}, Stripe82 {g0:.3f} -> {g1:.3f}")

elif mode == "5":
    T("M5: random tracer: replace every galaxy's L850 by a shuffled partner within its L_IR bin (ad table), then apply the toy optimiser")
    EDGES = [10.5, 11.0, 11.5, 12.0, 12.5]

    def merge_bins(idx, minN):
        idx = idx.copy(); changed = True
        while changed:
            changed = False
            u = sorted(set(idx.tolist()))
            for k, b in enumerate(u):
                if (idx == b).sum() < minN and len(u) > 1:
                    idx[idx == b] = u[k - 1] if k > 0 else u[k + 1]; changed = True; break
        return idx

    def within_sd(Ltr, ratio):
        b = merge_bins(np.digitize(Ltr, EDGES), 10); ss = 0.0; dof = 0
        for g in set(b.tolist()):
            v = ratio[b == g]; ss += ((v - v.mean()) ** 2).sum(); dof += len(v) - 1
        return math.sqrt(ss / dof)

    rows, _ = joined("ad")
    La, Lb, LIR = [], [], []
    for r in rows:
        a, b = fl(r["logL850"]), fl(r["logLCO"]); Lv = r["_LIRm"] if r["_LIRm"] is not None else r["_LIRo"]
        if None in (a, b, Lv):
            continue
        La.append(a); Lb.append(b); LIR.append(Lv)
    La, Lb, LIR = map(np.array, (La, Lb, LIR))
    bins = merge_bins(np.digitize(LIR, EDGES), 10)
    rng = np.random.default_rng(2386)

    def shuffled():
        out = La.copy()
        for g in set(bins.tolist()):
            ii = np.where(bins == g)[0]; out[ii] = La[rng.permutation(ii)]
        return out

    real = within_sd(LIR, La - Lb)
    # the mutated 'real' series is itself a shuffled series; compare with a fresh shuffle
    La_mut = shuffled()
    sd_mut = within_sd(LIR, La_mut - Lb)
    sd_ref = float(np.mean([within_sd(LIR, np.where(True, shuffled(), 0) - Lb) for _ in range(100)]))
    ratio_mut = sd_mut / sd_ref
    ma, mb, da, db, r_ = toy_optimise(La_mut, Lb, 0.6, -13.0, 0.5)
    agree = float(np.max(np.abs(ma - mb)))
    T(f" toy optimiser on the random-tracer series: max |mass_a - mass_b| {agree:.1e}; within-bin ratio SD: real {real:.3f}, random-tracer series {sd_mut:.3f}, fresh-shuffle reference {sd_ref:.3f}; ratio {ratio_mut:.2f}")
    bite("masses-agree (expected to hold)", agree >= 1e-12, f"agreement {agree:.1e}")
    bite("H-C8b real/shuffled < 0.8", not (ratio_mut < 0.8), f"random-tracer series ratio {ratio_mut:.2f} (real data gave {real / sd_ref:.2f})")

elif mode == "6":
    T("M6: correlated tracer errors (rho = 0.5 between CO and dust) in the N = 300 hat mock; truth sigma (0.10, 0.15, 0.20)")
    rng = np.random.default_rng(2385)
    sg = np.array([0.10, 0.15, 0.20]); C = np.diag(sg ** 2); C[0, 2] = C[2, 0] = 0.5 * sg[0] * sg[2]
    e = rng.normal(0, 1, (300, 3)) @ np.linalg.cholesky(C).T
    vA, vB, vC = hat(e[:, 0] - e[:, 1], e[:, 0] - e[:, 2], e[:, 1] - e[:, 2])
    rec = np.array([sgn_sqrt(vA), sgn_sqrt(vB), sgn_sqrt(vC)])
    T(f" recovered sigma {rec.round(3).tolist()} vs true {sg.tolist()} (ratios {np.round(rec / sg, 2).tolist()})")
    bite("C5 recovery within 15%", not bool(np.all(np.abs(rec / sg - 1) < 0.15)), f"ratios {np.round(rec / sg, 2).tolist()}")

elif mode == "7":
    T("M7: Stripe82 slope set to +1.2 (ACE's own), and Stripe82 restricted to Z >= 8.70")
    AC = [r for r in load_ace() if r["both"]]
    Rg = np.array([r["logMdust"] - math.log10(r["Mmol"] * 1e10) for r in AC]); ZA = np.array([r["OH"] for r in AC])
    S = load_s82()
    Rs = np.array([r["logMdust"] - r["logMgas_CO"] for r in S if r["logMdust"] is not None and r["logMgas_CO"] is not None])
    Zs = np.array([r["Z_12logOH"] for r in S if r["logMdust"] is not None and r["logMgas_CO"] is not None])
    seA = Rg.std(ddof=1) / math.sqrt(15)
    D12 = float((Rg - (Rs.mean() + 1.2 * (ZA - Zs.mean()))).mean())
    T(f" offset at s = +1.2: {D12:+.3f}, K {Kfun(D12, seA):.3f}")
    bite("H-B6 K=0.34", not abs(Kfun(D12, seA) - 0.34) <= 0.01, f"K {Kfun(D12, seA):.3f}")
    m = Zs >= 8.70
    b, *_ = ols(np.column_stack([np.ones(m.sum()), Zs[m]]), Rs[m])
    Dsub = float((Rg - (b[0] + b[1] * ZA)).mean())
    T(f" Z >= 8.70 OLS slope {b[1]:+.2f}, offset {Dsub:+.3f} (full sample -0.671)")
    bite("H-B6 OLS offset -0.67", not abs(Dsub + 0.67) <= 0.01, f"offset {Dsub:+.3f}")

elif mode == "8":
    T("M8: add 0.10 dex to the SMG-flagged rows of every factor (no z trend planted)")
    for combo in COMBOS:
        A = factor_arrays(*combo, "fb")
        smg = A["F"][:, FLAGS.index("SMG")] == 1
        base = slope_fit(A, True, 4000, 238)
        A2 = dict(A); A2["y"] = A["y"] + 0.10 * smg
        mut = slope_fit(A2, True, 4000, 238)
        wo0 = slope_fit(A, False, 4000, 238); wo1 = slope_fit(A2, False, 4000, 238)
        T(f" {combo}: N SMG {int(smg.sum())}; with L_IR b {base['b']:+.3f} -> {mut['b']:+.3f} ({mut['b'] / mut['b_boot_sd']:+.1f} sigma); without L_IR {wo0['b']:+.3f} -> {wo1['b']:+.3f} ({wo1['b'] / wo1['b_boot_sd']:+.1f} sigma)")
        bite(f"slope-consistent-with-zero:{combo}", abs(mut["b"]) >= 2 * mut["b_boot_sd"], f"|b/SD| {abs(mut['b'] / mut['b_boot_sd']):.1f}")

bit = [lid for lid, f in bites if f]
expected_hold = [lid for lid, f in bites if ("expected to hold" in lid)]
# a line labelled '(expected to hold)' is a line that must NOT fail; it counts as a bite only when it does fail (contradiction of the algebra)
effective = [lid for lid, f in bites if f and ("expected to hold" not in lid)]
T(f"\nM{mode}: lines that fail as frozen (bites): {effective}; lines expected to hold that failed: {[l for l, f in bites if f and 'expected to hold' in l]}")
bit_all = len(effective) > 0
T(f"M{mode} control {'BITES' if bit_all else 'DOES NOT BITE'} (exit {1 if bit_all else 0})")
R["bites"] = bites
dump(jp, R)
T.close()
sys.exit(1 if bit_all else 0)
