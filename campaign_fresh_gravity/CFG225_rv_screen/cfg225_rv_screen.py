#!/usr/bin/env python3
"""CFG225 -- EXPLORATORY: the change in gamma-hat attributable to the frozen radial-velocity screen (cut 11) on the in-repo DR3 wide-binary build, and the fraction of pairs it flags.
Frozen criteria: FROZEN_CRITERIA.md here (fd4a2a7a7), committed before any RV value was read.  The DR3 gamma-hat has already been seen (pre-registration 1.6); Amendment 7(e): DR3 numbers are code-path tests, never results;
no verdict words; not a test of any law.  Gaia DR3 radial velocities (about 1 to 5 km/s) cannot measure orbits, only screen triples.  NO NETWORK (socket guard).  NEW file: wp2_variant_full_dr3.py's machinery is exec'd
READ-ONLY up to its main block (three text substitutions: the work dir, the stage-E shift seed offset, writing final.csv); build_catalog.py's frozen_cuts is wrapped IN MEMORY to disable the RV screen; nothing frozen is edited.
Run: python3 campaign_fresh_gravity/CFG225_rv_screen/cfg225_rv_screen.py      (MUTATE=1: thresholds to infinity)"""
import sys, os
sys.dont_write_bytecode = True
import io, json, math, time, contextlib
from pathlib import Path
import numpy as np

MUT = os.environ.pop("MUTATE", "").strip() == "1"
LANE = Path(__file__).resolve().parent
REPO = LANE.parents[1]
DR = REPO / "prep_2026" / "gaia_dr4_prep" / "dr4_ready_1"
T0 = time.time()
OUT, CHK = [], []


def P(s=""):
    print(s, flush=True); OUT.append(s)


def check(name, val, ok):
    CHK.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


P(__doc__.split("Run:")[0].strip())
text = (DR / "wp2_variant_full_dr3.py").read_text()
cut = text.index('P("WP2 full size: primary vs all-source variant base')
head = text[:cut]
for a, b in (('work = src / "wp2_full"', 'work = WORKDIR'), ('seed=r + 1)', 'seed=r + 1 + SHIFT_OFF)'),
             ('rep["final_csv_sha256"] = __import__("hashlib").sha256(buf.getvalue().encode()).hexdigest()',
              'rep["final_csv_sha256"] = __import__("hashlib").sha256(buf.getvalue().encode()).hexdigest(); (work / "final.csv").write_text(buf.getvalue())')):
    assert head.count(a) == 1, a
    head = head.replace(a, b)
ns = {"__file__": str(DR / "wp2_variant_full_dr3.py"), "__name__": "wp2_lib", "WORKDIR": None, "SHIFT_OFF": 0}
exec(compile(head, "wp2_variant_full_dr3.py", "exec"), ns)
B, BASES = ns["B"], ns["BASES"]
sys.path.insert(0, str(DR.parent))
import wide_binary_pipeline as wbp
SRC = BASES["primary"]
WORK = SRC / "wp2_gamma_0_noRV"
KAU = wbp.KAU
ns["N_SHIFT"] = 30
assert B.N_SHIFT == 30

# ---- the forward model (as validate_dr3.v4_gamma) and the estimator
rng0 = np.random.default_rng(20261216)
with contextlib.redirect_stdout(io.StringIO()):
    pop = wbp.make_population(3_000_000, rng0, dr4=False)
    MODS = {"canonical": (wbp.A0_CAN, wbp.model_medians(pop, wbp.A0_CAN, wbp.GRID, rng0)),
            "alt": (wbp.A0_ALT, wbp.model_medians(pop, wbp.A0_ALT, wbp.GRID, rng0))}


def arrays(table, sel=None):
    s = table["sep_kAU"] * KAU; vp = table["v_perp_kms"] * 1e3; Mt = table["M1_msun"] + table["M2_msun"]
    gN = wbp.G * Mt * wbp.MSUN / s ** 2; vt = vp / np.sqrt(wbp.G * Mt * wbp.MSUN / s)
    return (gN, vt) if sel is None else (gN[sel], vt[sel])


def gamma(gN, vt, seed):
    out = {}
    for foot, (a0v, mod) in MODS.items():
        with contextlib.redirect_stdout(io.StringIO()):
            g, sg, *_ = wbp.run_fit(np.log10(gN / a0v), vt, mod, np.random.default_rng(seed), foot)
        out[foot] = (float(g), float(sg))
    return out


def load_table(path):
    import csv
    rows = list(csv.DictReader(open(path)))
    return {k: np.array([float(r[k]) if k not in ("source_id1", "source_id2") else int(r[k]) for r in rows]) for k in rows[0]}


if not MUT:
    # ---- the BEFORE set: the real-settings build with cut 11 disabled (read-only in-memory wrapper)
    WORK.mkdir(exist_ok=True)
    for f in ("stage_A.npz", "stage_B.npz", "stage_C.npz", "stage_D.npz", "stage_E.npz", "stage_F.npz", "AV_sfd98.npz"):
        if not (WORK / f).exists():
            (WORK / f).symlink_to(SRC / "wp2_gamma_0" / f)
    orig_fc = B.frozen_cuts

    class NoRV:
        def __init__(self, S):
            self.S = S
        def __getitem__(self, k):
            if k in ("radial_velocity", "radial_velocity_error"):
                return np.full(len(self.S["ra"]), np.nan)
            return self.S[k]

    B.frozen_cuts = lambda S, a, b, R, extra: orig_fc(NoRV(S), a, b, R, extra)
    ns["WORKDIR"], ns["SHIFT_OFF"] = WORK, 0
    t = time.time()
    with contextlib.redirect_stdout(io.StringIO()):
        rep, sets, gnull, S = ns["build"]("primary", SRC)
    B.frozen_cuts = orig_fc
    P(f"\nBEFORE set (real settings, N_SHIFT = 30, frozen seeds, cut 11 disabled): initial pairs {rep['n_initial_pairs']:,d}; with R {rep['n_R_pairs']:,d}; FINAL {rep['n_final']:,d}  ({time.time() - t:.0f} s)")
    tab = load_table(WORK / "final.csv")
    n_before = len(tab["sep_kAU"])
    ids = np.asarray(S["source_id"]); order = np.argsort(ids); ids_s = ids[order]
    def row(sid):
        pos = np.searchsorted(ids_s, sid)
        assert np.all(ids_s[pos] == sid)
        return order[pos]
    ia, ib = row(tab["source_id1"].astype(np.int64)), row(tab["source_id2"].astype(np.int64))
    rv1, rv2 = np.asarray(S["radial_velocity"])[ia], np.asarray(S["radial_velocity"])[ib]
    erv = np.hypot(np.asarray(S["radial_velocity_error"])[ia], np.asarray(S["radial_velocity_error"])[ib])
    both = np.isfinite(rv1) & np.isfinite(rv2)
    sep_au = tab["sep_kAU"] * 1e3; Mt = tab["M1_msun"] + tab["M2_msun"]
    vc = np.sqrt(wbp.G * Mt * wbp.MSUN / (sep_au * wbp.AU)) / 1e3
    drv = np.abs(rv1 - rv2); T = np.maximum(3 * erv, 3 * vc)
    flag = both & (drv > T)
    np.savez(WORK / "rv_table.npz", both=both, drv=drv, T=T, erv=erv, vc=vc, flag=flag)
    sel = both
    N_rv = int(sel.sum()); n_fl = int((flag & sel).sum())
    P(f"\nBEFORE pairs {n_before:,d}; with both Gaia DR3 RVs (S_RV) {N_rv:,d} ({100 * N_rv / n_before:.1f}%)")
    P(f"  flagged by the screen: {n_fl} of {N_rv} = {100 * n_fl / N_rv:.2f}% of S_RV ({100 * n_fl / n_before:.2f}% of the BEFORE set)")
    P(f"  S_RV medians: sigma_dRV {np.median(erv[sel]):.2f} km/s, v_c {np.median(vc[sel]):.2f} km/s, threshold {np.median(T[sel]):.2f} km/s, |dRV| {np.median(drv[sel]):.2f} km/s; flagged pairs' median |dRV| {np.median(drv[flag & sel]) if n_fl else float('nan'):.1f} km/s")
    # C1: the post hoc flags equal the builder's own cut on the same table (frozen_cuts with RV enabled, other cuts all satisfied by construction)
    a_idx, b_idx = ia, ib
    extra = {"third": np.zeros(n_before, bool)}
    keep, flow, _ = orig_fc(S, a_idx, b_idx, tab["R_chance"], extra)
    rv_step = dict(flow)
    c1 = bool(np.array_equal(keep, ~flag))
    check("C1 the post hoc flags reproduce the builder's own cut 11: frozen_cuts with the RV columns enabled, on the same table, keeps exactly the unflagged pairs", f"{c1}; builder flow ends at {flow[-1][1]} of {n_before} pairs, this lane leaves {int((~flag).sum())}", c1)
    # C-id: in-memory arrays equal the pipeline's ingest_csv
    gN0, vt0, _ = wbp.ingest_csv(str(WORK / "final.csv")); gN1, vt1 = arrays(tab)
    check("C0 the in-memory (g_N, v_tilde) arrays equal wide_binary_pipeline.ingest_csv on the BEFORE table", f"max relative difference {max(np.max(np.abs(gN0 / gN1 - 1)), np.max(np.abs(vt0 / vt1 - 1))):.1e}", max(np.max(np.abs(gN0 / gN1 - 1)), np.max(np.abs(vt0 / vt1 - 1))) < 1e-12)
    gN, vt = arrays(tab)
    Sr = np.flatnonzero(sel)
    # ---- gamma-hat before / after on S_RV, reference rows
    bef = gamma(gN[Sr], vt[Sr], 20261217)
    aft = gamma(gN[Sr][~flag[Sr]], vt[Sr][~flag[Sr]], 20261217)
    allb = gamma(gN, vt, 20261217); alla = gamma(gN[~flag], vt[~flag], 20261217)
    P("\ngamma-hat (the pipeline's estimator, DR3-noise forward model, NON-SCORING)")
    for foot in MODS:
        P(f"  {foot:10s} S_RV before (N = {N_rv}): {bef[foot][0]:.4f} +- {bef[foot][1]:.4f};  S_RV after (N = {N_rv - n_fl}): {aft[foot][0]:.4f} +- {aft[foot][1]:.4f};  change {aft[foot][0] - bef[foot][0]:+.4f}")
        P(f"  {'':10s} whole BEFORE set (N = {n_before}): {allb[foot][0]:.4f} +- {allb[foot][1]:.4f};  whole AFTER set (N = {n_before - n_fl}): {alla[foot][0]:.4f} +- {alla[foot][1]:.4f}")
    flo = None
    if n_fl >= 50:
        try:
            flo = gamma(gN[flag & sel], vt[flag & sel], 20261217)
            for foot in MODS:
                P(f"  {foot:10s} flagged pairs alone (N = {n_fl}): {flo[foot][0]:.4f} +- {flo[foot][1]:.4f}")
        except ValueError as e:
            flo = None
            P(f"  flagged pairs alone (N = {n_fl}): the pipeline's binned fit has no admissible grid point at this N ({str(e)[:60]}): not fitted")
    else:
        P(f"  flagged pairs alone: N = {n_fl} < 50, not fitted")
    # ---- paired bootstrap of the change
    B_ = 100
    rng = np.random.default_rng(225)
    dgam = {f: [] for f in MODS}
    for k in range(B_):
        idx = rng.integers(0, N_rv, size=N_rv)
        fb = flag[Sr][idx]
        g_b = gamma(gN[Sr][idx], vt[Sr][idx], 20261218 + k); g_a = gamma(gN[Sr][idx][~fb], vt[Sr][idx][~fb], 20261218 + k)
        for f in MODS:
            dgam[f].append(g_a[f][0] - g_b[f][0])
    P("\npaired bootstrap of the change (B = 100 resamples of the S_RV pairs; both estimators on the same resample)")
    res = {}
    for foot in MODS:
        d = np.array(dgam[foot]); ch = aft[foot][0] - bef[foot][0]
        P(f"  {foot:10s} change {ch:+.4f}; bootstrap SD of the change {d.std(ddof=1):.4f}; change / sigma_fit(before) {ch / bef[foot][1]:+.3f}; change / bootstrap SD {ch / d.std(ddof=1):+.2f}")
        res[foot] = dict(before=bef[foot], after=aft[foot], change=ch, boot_sd=float(d.std(ddof=1)), whole_before=allb[foot], whole_after=alla[foot], flagged_only=(flo[foot] if flo else None))
    # ---- C2 / C3 planted triples
    rng = np.random.default_rng(2250)
    Sun = Sr[~flag[Sr]]
    from scipy.stats import norm
    n_plant = max(1, int(0.10 * len(Sun)))
    fr_emp, fr_ana, se_ana, fp_ok = [], [], [], []
    rec = {f: [] for f in MODS}
    for rep_i in range(20):
        pl = rng.choice(Sun, size=n_plant, replace=False)
        X = rng.normal(0, 3.0, n_plant)
        d_i = (rv1[pl] - rv2[pl]); T_i = T[pl]
        fl_p = np.abs(d_i + X) > T_i
        ana = norm.cdf((-T_i - d_i) / 3.0) + 1 - norm.cdf((T_i - d_i) / 3.0)
        fr_emp.append(fl_p.mean()); fr_ana.append(ana.mean()); se_ana.append(math.sqrt((ana * (1 - ana)).sum()) / n_plant)
        wx, wy = rng.normal(0, 3.0, n_plant), rng.normal(0, 3.0, n_plant)
        tab2 = {k: v.copy() for k, v in tab.items() if k in ("sep_kAU", "v_perp_kms", "M1_msun", "M2_msun")}
        vnew = np.sqrt((tab2["v_perp_kms"][pl] + wx) ** 2 + wy ** 2)
        tab2["v_perp_kms"][pl] = vnew
        gN2, vt2 = arrays(tab2)
        sel2 = Sr
        flag2 = flag.copy(); flag2[pl] |= fl_p
        c = gamma(gN2[sel2], vt2[sel2], 20261300 + rep_i)
        s_ = gamma(gN2[sel2][~flag2[sel2]], vt2[sel2][~flag2[sel2]], 20261300 + rep_i)
        for f in MODS:
            shift = c[f][0] - bef[f][0]; resid = s_[f][0] - aft[f][0]
            rec[f].append((shift, resid))
    fe, fa, sa = np.mean(fr_emp), np.mean(fr_ana), np.sqrt(np.mean(np.array(se_ana) ** 2) / len(se_ana))
    check("C2 planted triples (10% of the unflagged S_RV pairs, dRV offset N(0, 3 km/s), 20 repeats): the empirical flagged fraction of the planted pairs equals the analytic mean within 3 binomial standard errors", f"empirical {fe:.4f}, analytic {fa:.4f}, SE {sa:.4f}", abs(fe - fa) < 3 * sa)
    ok3 = True
    for f in MODS:
        r = np.array(rec[f]); sh, rs = r[:, 0], r[:, 1]
        frac_removed = 1 - rs.mean() / sh.mean()
        better = float(np.mean(np.abs(rs) < np.abs(sh)))
        P(f"      C3 {f:10s}: planted gamma-hat shift (contaminated minus original) {sh.mean():+.4f} +- {sh.std(ddof=1):.4f} over 20 repeats; shift left after the screen {rs.mean():+.4f} +- {rs.std(ddof=1):.4f}; fraction of the shift removed {frac_removed:.2f}; screened shift smaller in {100 * better:.0f}% of repeats")
        ok3 &= better >= 0.90
    check("C3 planted contamination of gamma-hat (plane-of-sky offsets N(0, 3 km/s) on the same planted pairs): the screened shift is smaller than the contaminated shift in at least 90% of 20 repeats, both footings", f"{ok3}", ok3)
    # ---- POST HOC (written after C3 failed; NOT frozen, reported beside it): the same planting with larger offsets, where the screen has power
    P("\nPOST HOC (after C3 failed; not frozen): planted offsets N(0, sigma) in dRV and in the plane-of-sky velocity, 20 repeats each")
    POST = {}
    for sig_inj in (3.0, 10.0, 30.0):
        rng = np.random.default_rng(2251 + int(sig_inj))
        fr, rec2 = [], {f: [] for f in MODS}
        for rep_i in range(20):
            pl = rng.choice(Sun, size=n_plant, replace=False)
            X = rng.normal(0, sig_inj, n_plant)
            fl_p = np.abs((rv1[pl] - rv2[pl]) + X) > T[pl]
            fr.append(fl_p.mean())
            wx, wy = rng.normal(0, sig_inj, n_plant), rng.normal(0, sig_inj, n_plant)
            tab2 = {k: v.copy() for k, v in tab.items() if k in ("sep_kAU", "v_perp_kms", "M1_msun", "M2_msun")}
            tab2["v_perp_kms"][pl] = np.sqrt((tab2["v_perp_kms"][pl] + wx) ** 2 + wy ** 2)
            gN2, vt2 = arrays(tab2)
            flag2 = flag.copy(); flag2[pl] |= fl_p
            c = gamma(gN2[Sr], vt2[Sr], 20261400 + rep_i); s_ = gamma(gN2[Sr][~flag2[Sr]], vt2[Sr][~flag2[Sr]], 20261400 + rep_i)
            for f in MODS:
                rec2[f].append((c[f][0] - bef[f][0], s_[f][0] - aft[f][0]))
        for f in MODS:
            r = np.array(rec2[f]); sh, rs = r[:, 0], r[:, 1]
            P(f"    sigma {sig_inj:4.0f} km/s, {f:10s}: flagged fraction of the planted pairs {np.mean(fr):.2f}; planted gamma-hat shift {sh.mean():+.4f} +- {sh.std(ddof=1):.4f}; left after the screen {rs.mean():+.4f} +- {rs.std(ddof=1):.4f}; fraction removed {1 - rs.mean() / sh.mean():.2f}; screened shift smaller in {100 * np.mean(np.abs(rs) < np.abs(sh)):.0f}% of repeats")
            POST[f"{sig_inj:.0f}|{f}"] = dict(flagged=float(np.mean(fr)), shift=float(sh.mean()), left=float(rs.mean()))
    P(f"\n{sum(CHK)}/{len(CHK)} controls pass (MUTATE is the separate run); {time.time() - T0:.0f} s")
    P("Reading: EXPLORATORY; the DR3 gamma-hat was already seen; these are code-path numbers on a few thousand pairs with the pipeline's DR3-noise forward model; the change is the screen's effect on the RV-matched subsample only; the screen removes triples with km/s-scale dRV and cannot measure orbits; no verdict words.")
    json.dump(dict(before_n=n_before, S_RV=N_rv, flagged=n_fl, flagged_frac_SRV=n_fl / N_rv, results=res, c2=dict(emp=float(fe), ana=float(fa), se=float(sa)), c3={f: np.array(rec[f]).tolist() for f in MODS},
                   controls=dict(passed=sum(CHK), n=len(CHK)), posthoc=POST, median_sigma_dRV=float(np.median(erv[sel])), median_vc=float(np.median(vc[sel])), median_T=float(np.median(T[sel]))),
              open(LANE / "cfg225_rv_screen_results.json", "w"), indent=1, default=float)
    open(LANE / "cfg225_rv_screen.out", "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if all(CHK) else 1)

# ---- MUTATE: thresholds to infinity
Z = np.load(WORK / "rv_table.npz")
T_inf = np.full_like(Z["T"], np.inf)
flag_m = Z["both"] & (Z["drv"] > T_inf)
tab = load_table(WORK / "final.csv")
gN, vt = arrays(tab)
Sr = np.flatnonzero(Z["both"])
bef = gamma(gN[Sr], vt[Sr], 20261217); aft = gamma(gN[Sr][~flag_m[Sr]], vt[Sr][~flag_m[Sr]], 20261217)
P(f"\nMUTATE: thresholds set to infinity: flagged {int(flag_m.sum())}; gamma-hat change canonical {aft['canonical'][0] - bef['canonical'][0]:.2e}, alt {aft['alt'][0] - bef['alt'][0]:.2e}")
check("MUTATE zero pairs flagged and the change in gamma-hat is exactly 0", f"flagged {int(flag_m.sum())}", int(flag_m.sum()) == 0 and aft["canonical"][0] == bef["canonical"][0] and aft["alt"][0] == bef["alt"][0])
open(LANE / "cfg225_rv_screen_MUTATE.out", "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(CHK) else 1)
