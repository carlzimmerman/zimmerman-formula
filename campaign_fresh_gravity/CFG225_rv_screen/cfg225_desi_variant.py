#!/usr/bin/env python3
"""CFG225 -- EXPLORATORY: the change in gamma-hat attributable to the frozen radial-velocity screen (cut 11) on the in-repo DR3 wide-binary build, and the fraction of pairs it flags.
Frozen criteria: FROZEN_CRITERIA.md here (fd4a2a7a7) and its Addendum 1 (17e1d4c97), committed before any DESI RV was combined with any pair.  The DR3 gamma-hat has already been seen (pre-registration 1.6); Amendment 7(e): DR3 numbers are code-path tests, never results;
no verdict words; not a test of any law.  Gaia DR3 radial velocities (about 1 to 5 km/s) cannot measure orbits, only screen triples.  NO NETWORK (socket guard).  NEW file: wp2_variant_full_dr3.py's machinery is exec'd
READ-ONLY up to its main block (three text substitutions: the work dir, the stage-E shift seed offset, writing final.csv); build_catalog.py's frozen_cuts is wrapped IN MEMORY to disable the RV screen; nothing frozen is edited.
Run: python3 campaign_fresh_gravity/CFG225_rv_screen/cfg225_desi_variant.py      (MUTATE=1: thresholds and the variable cut to infinity)"""
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


DM = os.path.join(REPO, "data_assembly", "desi_mws")


def rdc(path):
    import csv
    return list(csv.DictReader(open(path, newline="")))


def ff(x):
    try:
        v = float(str(x).strip())
        return v if math.isfinite(v) else float("nan")
    except (TypeError, ValueError):
        return float("nan")


# ---- the BEFORE build (as the primary: cut 11 disabled; the stage caches are reused)
WORK.mkdir(exist_ok=True)
for f_ in ("stage_A.npz", "stage_B.npz", "stage_C.npz", "stage_D.npz", "stage_E.npz", "stage_F.npz", "AV_sfd98.npz"):
    if not (WORK / f_).exists():
        (WORK / f_).symlink_to(SRC / "wp2_gamma_0" / f_)
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
with contextlib.redirect_stdout(io.StringIO()):
    rep, sets, gnull, S = ns["build"]("primary", SRC)
B.frozen_cuts = orig_fc
tab = load_table(WORK / "final.csv")
n_before = len(tab["sep_kAU"])
ids = np.asarray(S["source_id"]); order = np.argsort(ids); ids_s = ids[order]


def row(sid):
    pos = np.searchsorted(ids_s, sid)
    assert np.all(ids_s[pos] == sid)
    return order[pos]


sid1, sid2 = tab["source_id1"].astype(np.int64), tab["source_id2"].astype(np.int64)
ia, ib = row(sid1), row(sid2)
g1, g2 = np.asarray(S["radial_velocity"])[ia], np.asarray(S["radial_velocity"])[ib]
ge1, ge2 = np.asarray(S["radial_velocity_error"])[ia], np.asarray(S["radial_velocity_error"])[ib]
sep_au = tab["sep_kAU"] * 1e3; Mt = tab["M1_msun"] + tab["M2_msun"]
vc = np.sqrt(wbp.G * Mt * wbp.MSUN / (sep_au * wbp.AU)) / 1e3
P(f"\nBEFORE set (as the primary): {n_before:,d} pairs")
if MUT:
    both0_ = np.isfinite(g1) & np.isfinite(g2)
    flag_m = np.zeros(n_before, bool)
    varf_m = np.zeros(n_before, bool)
    Sp_m = np.flatnonzero(both0_)
    gN_, vt_ = arrays(tab)
    b_ = gamma(gN_[Sp_m], vt_[Sp_m], 20261217); a_ = gamma(gN_[Sp_m][~flag_m[Sp_m]], vt_[Sp_m][~flag_m[Sp_m]], 20261217); v_ = gamma(gN_[Sp_m][(~flag_m & ~varf_m)[Sp_m]], vt_[Sp_m][(~flag_m & ~varf_m)[Sp_m]], 20261217)
    P(f"MUTATE: thresholds and the variable cut set to infinity: flagged {int(flag_m.sum())}, variable {int(varf_m.sum())}; gamma-hat change canonical {a_['canonical'][0] - b_['canonical'][0]:.2e} / {v_['canonical'][0] - b_['canonical'][0]:.2e}, alt {a_['alt'][0] - b_['alt'][0]:.2e} / {v_['alt'][0] - b_['alt'][0]:.2e}")
    check("MUTATE nothing flagged and every change in gamma-hat is exactly 0", "True", int(flag_m.sum()) == 0 and int(varf_m.sum()) == 0 and a_["canonical"][0] == b_["canonical"][0] and v_["alt"][0] == b_["alt"][0])
    open(LANE / "cfg225_desi_variant_MUTATE.out", "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if all(CHK) else 1)

# ---- DESI RVs per component (recommended cuts; floor 1 km/s bright / main, 2 km/s backup; 2 km/s for all as the sensitivity)
dm = rdc(os.path.join(DM, "desi_mws_matches.csv"))
good = [r for r in dm if ff(r["success"]) == 1 and ff(r["rvs_warn"]) == 0 and r["rr_spectype"].strip() == "STAR" and ff(r["vsini"]) < 30 and math.isfinite(ff(r["vrad"])) and math.isfinite(ff(r["vrad_err"]))]
best = {}
for r in good:
    k = int(r["source_id"])
    if k not in best or ff(r["sn_r"]) > ff(best[k]["sn_r"]):
        best[k] = r
P(f"DESI matches: {len(dm)} rows; {len(good)} pass the recommended cuts; {len(best)} distinct components with a good RV")


def desi_rv(sid, floor_all=None):
    r = best.get(int(sid))
    if r is None:
        return float("nan"), float("nan")
    fl = floor_all if floor_all is not None else (2.0 if r["program"].strip() == "backup" else 1.0)
    return ff(r["vrad"]), math.sqrt(ff(r["vrad_err"]) ** 2 + fl ** 2)


def combine(floor_all=None):
    v1, e1, v2, e2 = g1.copy(), ge1.copy(), g2.copy(), ge2.copy()
    from1, from2 = np.zeros(n_before, bool), np.zeros(n_before, bool)
    for k in range(n_before):
        if not math.isfinite(v1[k]):
            d, e = desi_rv(sid1[k], floor_all)
            if math.isfinite(d):
                v1[k], e1[k], from1[k] = d, e, True
        if not math.isfinite(v2[k]):
            d, e = desi_rv(sid2[k], floor_all)
            if math.isfinite(d):
                v2[k], e2[k], from2[k] = d, e, True
    both = np.isfinite(v1) & np.isfinite(v2)
    erv = np.hypot(e1, e2)
    T = np.maximum(3 * erv, 3 * vc)
    flag = both & (np.abs(v1 - v2) > T)
    return both, flag, T, v1 - v2, (from1 | from2)


both0 = np.isfinite(g1) & np.isfinite(g2)
T0_ = np.maximum(3 * np.hypot(ge1, ge2), 3 * vc)
flag0 = both0 & (np.abs(g1 - g2) > T0_)
both, flag, T, dv, fromD = combine()
bothF, flagF, TF, dvF, fromDF = combine(floor_all=2.0)
n0, n1 = int(both0.sum()), int(both.sum())
P(f"S_RV (Gaia on both components): {n0:,d}; S_RV+ (Gaia or DESI on both): {n1:,d} (gain {n1 - n0}; pairs using at least one DESI RV: {int((both & fromD).sum())})")
P(f"extended screen flags {int(flag.sum())} of {n1} = {100 * flag.sum() / n1:.2f}% (Gaia-only primary: {int(flag0.sum())} of {n0} = {100 * flag0.sum() / n0:.2f}%); flagged pairs that use a DESI RV: {int((flag & fromD).sum())} of {int((both & fromD).sum())}")
P(f"  with the 2 km/s floor for every DESI RV: flags {int(flagF.sum())}; flagged pairs that use a DESI RV {int((flagF & fromDF).sum())}")

# ---- RV-variable candidates from the single epochs
ep = rdc(os.path.join(DM, "desi_mws_epochs.csv"))
byid = {}
for r in ep:
    if ff(r["success"]) == 1 and ff(r["rvs_warn"]) == 0 and math.isfinite(ff(r["vrad"])) and math.isfinite(ff(r["vrad_err"])):
        byid.setdefault(int(r["source_id"]), []).append((ff(r["vrad"]), ff(r["vrad_err"])))


def chi2dof(v, e, floor=1.0):
    w = 1.0 / (np.asarray(e) ** 2 + floor ** 2); v = np.asarray(v)
    m = (w * v).sum() / w.sum()
    return float((w * (v - m) ** 2).sum() / (len(v) - 1))


var_ids = set(); n_multi = 0
for k_, lst in byid.items():
    if len(lst) >= 2:
        n_multi += 1
        if chi2dof([a for a, _ in lst], [b for _, b in lst]) > 3.0:
            var_ids.add(k_)
P(f"single-epoch stars with >= 2 good epochs: {n_multi}; RV-variable candidates (chi2/dof > 3 at a 1 km/s floor): {len(var_ids)}")
varf = np.array([(int(a) in var_ids) or (int(b) in var_ids) for a, b in zip(sid1, sid2)])
Sp = np.flatnonzero(both)
P(f"pairs with a variable component: {int(varf.sum())} of the BEFORE set; in S_RV+: {int((varf & both).sum())}; also RV-flagged: {int((varf & flag).sum())}")

# ---- C1: on pairs with Gaia RVs on both components the variant's flags equal the primary's exactly
c1 = bool(np.array_equal(flag[both0], flag0[both0]))
check("C1 on the pairs with Gaia RVs on both components the variant's flags equal the primary's exactly", f"{c1} ({int(both0.sum())} pairs)", c1)
# ---- gamma-hat before / after the extended screen / after the screen plus the variable flag, all on S_RV+
gN, vt = arrays(tab)
def g3(sel_idx, fl, vf, seed):
    m_ext = ~fl[sel_idx]; m_var = m_ext & ~vf[sel_idx]
    return (gamma(gN[sel_idx], vt[sel_idx], seed), gamma(gN[sel_idx][m_ext], vt[sel_idx][m_ext], seed), gamma(gN[sel_idx][m_var], vt[sel_idx][m_var], seed))
gb, ga, gv = g3(Sp, flag, varf, 20261217)
NB_ = len(Sp)
P("\ngamma-hat on S_RV+ (the pipeline's estimator, DR3-noise forward model, NON-SCORING)")
for foot in MODS:
    P(f"  {foot:10s} before (N = {NB_}): {gb[foot][0]:.4f} +- {gb[foot][1]:.4f};  after the extended screen (N = {int((~flag[Sp]).sum())}): {ga[foot][0]:.4f} +- {ga[foot][1]:.4f} (change {ga[foot][0] - gb[foot][0]:+.4f});  after screen + variable flag (N = {int(((~flag) & (~varf))[Sp].sum())}): {gv[foot][0]:.4f} +- {gv[foot][1]:.4f} (change {gv[foot][0] - gb[foot][0]:+.4f})")
gbF, gaF, gvF = g3(np.flatnonzero(bothF), flagF, varf, 20261217)
P(f"  floor sensitivity (2 km/s for every DESI RV; S_RV+ N = {int(bothF.sum())}): canonical change after the extended screen {gaF['canonical'][0] - gbF['canonical'][0]:+.4f}, after screen + variable {gvF['canonical'][0] - gbF['canonical'][0]:+.4f}; alt {gaF['alt'][0] - gbF['alt'][0]:+.4f}, {gvF['alt'][0] - gbF['alt'][0]:+.4f}")
rng = np.random.default_rng(2252)
d1, d2 = {f: [] for f in MODS}, {f: [] for f in MODS}
for k in range(100):
    idx = rng.integers(0, NB_, size=NB_)
    sel = Sp[idx]
    fb = flag[sel]; vb = varf[sel]
    m_ext = ~fb; m_var = m_ext & ~vb
    g_b = gamma(gN[sel], vt[sel], 20261500 + k); g_a = gamma(gN[sel][m_ext], vt[sel][m_ext], 20261500 + k); g_v = gamma(gN[sel][m_var], vt[sel][m_var], 20261500 + k)
    for f in MODS:
        d1[f].append(g_a[f][0] - g_b[f][0]); d2[f].append(g_v[f][0] - g_b[f][0])
P("\npaired bootstrap of the changes (B = 100 resamples of the S_RV+ pairs)")
RESV = {}
for foot in MODS:
    a_, v_ = np.array(d1[foot]), np.array(d2[foot])
    c1_, c2_ = ga[foot][0] - gb[foot][0], gv[foot][0] - gb[foot][0]
    P(f"  {foot:10s} extended screen: change {c1_:+.4f} (bootstrap SD {a_.std(ddof=1):.4f}; {c1_ / gb[foot][1]:+.3f} sigma_fit; {c1_ / a_.std(ddof=1):+.2f} SD);  screen + variable flag: change {c2_:+.4f} (SD {v_.std(ddof=1):.4f}; {c2_ / gb[foot][1]:+.3f} sigma_fit; {c2_ / v_.std(ddof=1):+.2f} SD)")
    RESV[foot] = dict(before=gb[foot], after_ext=ga[foot], after_var=gv[foot], change_ext=c1_, sd_ext=float(a_.std(ddof=1)), change_var=c2_, sd_var=float(v_.std(ddof=1)))
# ---- C2 planted triples among S_RV+ (frozen: 10% of the unflagged pairs, dRV ~ N(0, 3 km/s), 20 repeats)
from scipy.stats import norm
rng2 = np.random.default_rng(2253)
Sun = Sp[~flag[Sp]]; npl = max(1, int(0.10 * len(Sun)))
fe, fa, sa = [], [], []
for _ in range(20):
    pl = rng2.choice(Sun, size=npl, replace=False); X = rng2.normal(0, 3.0, npl)
    flp = np.abs(dv[pl] + X) > T[pl]
    ana = norm.cdf((-T[pl] - dv[pl]) / 3.0) + 1 - norm.cdf((T[pl] - dv[pl]) / 3.0)
    fe.append(flp.mean()); fa.append(ana.mean()); sa.append(math.sqrt((ana * (1 - ana)).sum()) / npl)
sE, sA = float(np.mean(fe)), float(np.mean(fa)); sseA = math.sqrt(np.mean(np.array(sa) ** 2) / 20)
check("C2 planted triples among S_RV+ (10% of the unflagged pairs, dRV offset N(0, 3 km/s), 20 repeats): the empirical flagged fraction equals the analytic mean within 3 binomial SE", f"empirical {sE:.4f}, analytic {sA:.4f}, SE {sseA:.4f}", abs(sE - sA) < 3 * sseA)
# ---- C3 the variable rule on synthetic stars
rng3 = np.random.default_rng(2254)
errs = np.array([e for lst in byid.values() for _, e in lst])
fp = []; hit = []
for nep in (2, 3, 4, 5):
    flagged = 0
    for _ in range(2000):
        e = rng3.choice(errs, nep); v = rng3.normal(0, np.sqrt(e ** 2 + 1.0))
        flagged += chi2dof(v, e) > 3.0
    fp.append(flagged / 2000)
for nep in (3, 4, 5):
    flagged = 0
    for _ in range(2000):
        e = rng3.choice(errs, nep); ph = rng3.uniform(0, 2 * np.pi, nep)
        v = 5.0 * np.sin(ph) + rng3.normal(0, np.sqrt(e ** 2 + 1.0))
        flagged += chi2dof(v, e) > 3.0
    hit.append(flagged / 2000)
check("C3 the variable rule: synthetic constant-RV stars (scatter = tabulated error + 1 km/s floor) are flagged in fewer than 5% on average over 2 to 5 epochs, and a planted 5 km/s semi-amplitude in at least 90% with 3 to 5 epochs", f"false-positive rate by epochs 2/3/4/5: {[round(x, 3) for x in fp]} (mean {np.mean(fp):.3f}); detection 3/4/5 epochs {[round(x, 3) for x in hit]}", np.mean(fp) < 0.05 and min(hit) >= 0.90)
P(f"\n{sum(CHK)}/{len(CHK)} controls pass (MUTATE is the separate run); {time.time() - T0:.0f} s")
P("Reading: EXPLORATORY; the DR3 gamma-hat was already seen; these are code-path numbers on a few thousand pairs with the pipeline's DR3-noise forward model; the DESI top-up adds few pairs and its RVs (systematic floor 1 to 2 km/s) cannot measure orbits; the variable flag is a candidate list; no verdict words.")
json.dump(dict(n_before=n_before, n_S_RV=n0, n_S_RVplus=n1, flagged_ext=int(flag.sum()), flagged_gaia=int(flag0.sum()), variable_pairs=int(varf.sum()), variable_components=len(var_ids), results=RESV, c3=dict(fp=fp, hit=hit)),
          open(LANE / "cfg225_desi_variant_results.json", "w"), indent=1, default=float)
open(LANE / "cfg225_desi_variant.out", "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(CHK) else 1)
