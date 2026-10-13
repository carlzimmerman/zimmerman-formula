"""CFG651: does THEORY v2's condensed-source rule (A5) predict the early-type age signal? Criteria: FROZEN_CRITERIA.md (5a24ec013).
POST-HOC mechanism test (the signal was already seen in CFG585/586/631/700).
Executes cfg585_age.py's head UNEDITED (masks, CFG531 estimator and law code, as CFG700 does). A copy of CFG531's law_vecs (law_vecs_df: M_p = M_g + M* Delta f directly, since f_cold > 1 at low M*; C5 checks identity) rebuilds the own
law profile with a per-group condensed-source shift (10^dl - 1 = Delta f). No new constant.
MUTATE (CFG651_MUTATE=1, *_MUTATE outputs): M1 all-baryon source, M2 200 shuffled-age relabellings, M3 linearity.
Run: nice -n 10 python3 cfg651_predict.py ; CFG651_MUTATE=1 nice -n 10 python3 cfg651_predict.py
"""
import os, io, sys, json, math, time, contextlib, resource
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
ROOT = os.path.dirname(LANES)
MUTATE = os.environ.get("CFG651_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT, CHECKS = [], []
try:
    os.nice(10)
except OSError:
    pass


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(c, m):
    CHECKS.append((bool(c), m)); P(f"  [{'PASS' if c else 'FAIL'}] {m}"); return bool(c)


def rss_gb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9   # macOS: bytes


for v in ("CFG585_MUTATE", "CFG531_MUTATE"):
    os.environ.pop(v, None)
path = os.path.join(LANES, "CFG585_age_settling", "cfg585_age.py")
ns = {"__file__": path, "__name__": "head"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(open(path).read().split('P("=" * 100)')[0], path, "exec"), ns)
U, F30, TYP, LMSL, esd_loo, comps, all_bands = (ns[k] for k in ("U", "F30", "TYP", "LMSL", "esd_loo", "comps", "all_bands"))
OLD5, YOUNG5 = ns["OLD"], ns["YOUNG"]                       # CFG585 masks (five quintile residuals)
G = esd_loo.__globals__                                     # CFG531 namespace
law_vecs, TAB, GSEL, GS, GM, GZ, gi = (G[k] for k in ("law_vecs", "TAB", "GSEL", "GS", "GM", "GZ", "gi"))
own_mix, gstack, MEAS, FOOTS = G["own_mix"], G["gstack"], G["MEAS"], G["FOOTS"]
NG = len(GM)
LZ = np.load(os.path.join(ROOT, "real_research", "data", "lensing_rar", "lr_lenses.npz"))
MGAL = LZ["Mgal"].astype(float)
assert np.allclose(LZ["logM"], LMSL)

# ---- LePhare SFR, same exact RA/Dec match as cfg585's head
Lp, o_, ix_ = ns["Lp"], ns["o"], ns["ix"]
SFR = np.array(Lp["SFR_BEST"], "f8")[o_[ix_]]
assert np.allclose(np.array(Lp["MAG_ABS_u"] - Lp["MAG_ABS_r"], "f8")[o_[ix_]], U)

# ---- CFG700 masks (ten-bin stratified tertiles; code copied from cfg700_raw.py)
C = F30 & (TYP == 1)
qb = np.quantile(LMSL[C], np.linspace(0, 1, 11)); qb[-1] += 1e-9
BIN_IDX = [np.where(C & (LMSL >= qb[i]) & (LMSL < qb[i + 1]))[0] for i in range(10)]


def tertiles(perm_rng=None):
    ter = np.full(len(U), -1)
    for idx in BIN_IDX:
        dc = U[idx] - np.median(U[idx])
        if perm_rng is not None:
            dc = perm_rng.permutation(dc)
        o = np.argsort(dc, kind="stable"); n = len(idx)
        for k in range(3):
            ter[idx[o[k * n // 3:(k + 1) * n // 3]]] = k
    return [(ter == k) & C for k in range(3)]


YOUNG7, MID7, OLD7 = tertiles()
K9 = list(range(6, 15))
dall, Call, _ = esd_loo(C)
W = 1.0 / np.diag(Call)

P("=" * 100)
P(f"CFG651  A5 condensed source vs the early-type age signal (POST-HOC mechanism test)  {'*** MUTATE ***' if MUTATE else 'PRIMARY'}")
P("=" * 100)

# ---- controls C1, C3, C4
P("--- controls")
do, _, _ = esd_loo(OLD7); dy, _, _ = esd_loo(YOUNG7)
A_meas = math.log10((W[K9] @ do[K9]) / (W[K9] @ dy[K9]))
J700 = json.load(open(os.path.join(LANES, "CFG700_raw_esd_age", "cfg700_results.json")))
S_A = J700["null"]["K9"]["sd"]
check(abs(A_meas - J700["A"]["K9"]["A"]) < 1e-4, f"C1 CFG700 measured A(K9) reproduced {A_meas:+.5f} vs {J700['A']['K9']['A']:+.5f}")
cov = np.mean(SFR[C] > -50)
check(cov >= 0.98, f"C3 SFR coverage in f30 early {cov:.4f} (>= 0.98)")
check(abs(np.median(LMSL[OLD7]) - np.median(LMSL[YOUNG7])) < 0.02, f"C4 OLD/YOUNG median log M* diff {np.median(LMSL[OLD7]) - np.median(LMSL[YOUNG7]):+.4f}")

# ---- per-lens condensed shifts
fcold = MGAL / 10 ** LMSL - 1.0
logS = SFR - LMSL
S = np.where(SFR > -50, 10 ** logS, np.nan)
DF_R2 = np.zeros(len(U))
for idx in BIN_IDX:
    s = S[idx].copy(); s[~np.isfinite(s)] = np.nanmedian(s)
    DF_R2[idx] = fcold[idx] * s / s.mean() - fcold[idx]

sys.path.insert(0, os.path.join(LANES, "CFG515_census_edge_resolution"))
import cfg515_lib as L515
chi_age = max(r["chi_age"] for r in json.load(open(os.path.join(LANES, "CFG640_phase_source_pm", "cfg640_split.json")))["rows"])
FRET = np.array([L515.fret_census(float(GM[g]))[0] for g in range(NG)])
LMTA = np.array([L515.fret_census(float(GM[g]))[1] for g in range(NG)])
HOTSH = (FRET - 0.10) * (GM / 0.10) / 10 ** GS              # census-retained hot share in units of the group's M*
P(f"\ncensus: f30 groups log M_ta [Msun/h] range {LMTA[GSEL].min():.2f}-{LMTA[GSEL].max():.2f}; f_ret > 0.10 in "
  f"{np.mean(FRET[GSEL] > 0.10 + 1e-12):.3f} of f30 groups; chi_age,max = {chi_age:.4f}")


def group_df(df_lens, mask):
    """plain mean of Delta f_i * M*_i / M*_g over lenses in mask, per group (0 where empty)."""
    m = mask & np.isfinite(df_lens)
    num = np.bincount(gi[m], weights=df_lens[m] * 10 ** (LMSL[m] - GS[gi[m]]), minlength=NG)
    n = np.bincount(gi[m], minlength=NG)
    return np.where(n > 0, num / np.maximum(n, 1), 0.0)


def law_vecs_df(Mg, zl, lms, df):
    """CFG531 law_vecs copied with ONE change: M_p = M_g + M* df directly (df may be < -1 where f_cold > 1, i.e. stars only),
    instead of M* (10^dl - 1). Bin radii stay fixed by the data's M_gal (Mnode = M_g), as in law_vecs. Kernel mono, a0 x 1."""
    C_, A0F, SHMRS, rt_weights, fin, truncate = (G[k] for k in ("C", "A0F", "SHMRS", "rt_weights", "fin", "truncate"))
    nu = C_.nu_mono
    Mp = Mg + 10 ** lms * df
    Wt = {s: rt_weights(f"{s}_W30", lms, zl) for s in SHMRS}
    out = np.zeros((2, 3, 15))
    for i, foot in enumerate(FOOTS):
        a0 = A0F[foot]
        rta = C_.r_ta_law(Mp, a0, zl)
        r = np.geomspace(1e-4, rta, 1500)
        Md = Mp * (nu(C_.G_MPC * Mp / r ** 2 / a0) - 1.0)
        out[i, 0] = fin(Mg, Mp, r, Md)
        for j, s in enumerate(SHMRS):
            out[i, 1 + j] = fin(Mg, Mp, r, truncate(r, Md, Wt[s]))
    return out


_g0 = int(GSEL[len(GSEL) // 2])
_a = law_vecs((float(GM[_g0]), float(GZ[_g0]), float(GS[_g0]), math.log10(1.1), "mono", 1.0, float(GS[_g0])))
_b = law_vecs_df(float(GM[_g0]), float(GZ[_g0]), float(GS[_g0]), 0.1)
check(np.max(np.abs(_a / _b - 1)) < 1e-12, f"C5 copied law_vecs_df = CFG531 law_vecs at df = 0.1 (max rel {np.max(np.abs(_a / _b - 1)):.1e})")

NEXT = [0]


def build_table(dfg, label):
    """exact own-law table with M_p = M_g + M* dfg[g] (both footings, mono), via law_vecs_df (CFG531 law_vecs copy)."""
    name = f"cfg651_{NEXT[0]}"; NEXT[0] += 1
    if np.all(np.abs(dfg[GSEL]) < 1e-15):
        TAB[name] = TAB["d0"].copy()
    else:
        rows = [law_vecs_df(float(GM[g]), float(GZ[g]), float(GS[g]), float(dfg[g])) for g in GSEL]
        TAB[name] = np.array(rows)
    P(f"  table {name} ({label}) built  t={time.time() - T0:.0f}s  peak RSS {rss_gb():.2f} GB")
    return name


def own_stack(name, foot, mask, c="A"):
    return gstack(own_mix(c, foot, "LAW_RTA", MEAS["f30"], name, "moster"), mask)


def A_of(nO, nY, foot):
    oo, oy = own_stack(nO, foot, OLD7), own_stack(nY, foot, YOUNG7)
    return math.log10((W[K9] @ oo[K9]) / (W[K9] @ oy[K9]))


# ---- CFG585 estimator weight vectors (secondary statistic)
WV, EPS_MEAS = {}, {}
for nm, mk in (("OLD", OLD5), ("YOUNG", YOUNG5)):
    dcl, Ccl, _ = esd_loo(mk)
    for foot in FOOTS:
        fb = all_bands(dcl, Ccl, comps("A", foot, mk))
        WV[(nm, foot)] = np.array(fb["K9"]["wvec"]); EPS_MEAS[(nm, foot)] = fb["K9"]["eps"]
J585 = json.load(open(os.path.join(LANES, "CFG585_age_settling", "cfg585_results.json")))["R"]
D_meas = {f: (J585[f"D|A|{f}|K9"]["D"], J585[f"D|A|{f}|K9"]["sig"]) for f in FOOTS}
d_rep = EPS_MEAS[("OLD", "canonical")] - EPS_MEAS[("YOUNG", "canonical")]
check(abs(d_rep - D_meas["canonical"][0]) < 1e-3, f"C2 CFG585 D(A, canonical, K9) reproduced {d_rep:+.4f} vs {D_meas['canonical'][0]:+.4f}")
base = "d0"


def D_of(nO, nY, foot):
    out = []
    for nm, mk, tn in (("OLD", OLD5, nO), ("YOUNG", YOUNG5, nY)):
        dv = own_stack(tn, foot, mk) - own_stack(base, foot, mk)
        out.append(float(WV[(nm, foot)] @ dv[K9]))
    return out[0] - out[1]


def classify(pred, meas, sig):
    if pred < -0.1 * sig or abs(pred - meas) > 3 * sig:
        cl = "FAILS"
    elif pred > 0 and abs(pred - meas) <= 2 * sig:
        cl = "CONSISTENT"
    else:
        cl = "TENSION"
    mech = "ACCOUNTS FOR" if pred >= meas / 2 else ("DOES NOT ACCOUNT" if pred < meas / 4 else "PARTIAL")
    return cl, mech


RES = dict(lane="CFG651", criteria="5a24ec013", posthoc=True, mutate=MUTATE, A_meas=A_meas, A_sig=S_A,
           D_meas={f: list(v) for f, v in D_meas.items()}, chi_age_max=chi_age,
           settings="kappa = 1/2 FITTED; footings never pooled; nu_mono; cold energy mass still required; not theory closed")

P("\n--- per-lens shift summaries (Delta f in units of M*)")
for nm, mk in (("OLD7", OLD7), ("YOUNG7", YOUNG7), ("OLD5", OLD5), ("YOUNG5", YOUNG5)):
    P(f"  {nm:6s} R2 mean Delta f {np.mean(DF_R2[mk]):+.4f}  (record f_cold mean {np.mean(fcold[mk]):.4f}; median log sSFR "
      f"{np.median(logS[mk & (SFR > -50)]):+.2f})")

ROUTES = {}
if not MUTATE:
    ROUTES["R2"] = (DF_R2, DF_R2)
    ROUTES["R1"] = ("R1", None)
    ROUTES["R3a"] = (2.0 * fcold, -fcold)
    ROUTES["R3b"] = ("R3b", None)
else:
    ROUTES["M1_Sall"] = (np.zeros(len(U)), np.zeros(len(U)))   # condensed <-> hot at fixed retained total: source unchanged

nb = {f: A_of(base, base, f) for f in FOOTS}
P(f"\nequal-source law baseline A_base (composition only): " + " / ".join(f"{f} {nb[f]:+.5f}" for f in FOOTS))
RES["A_base"] = nb
RES["routes"] = {}
for rname, (dO, dY) in ROUTES.items():
    if isinstance(dO, str):
        gO = {"R1": HOTSH * chi_age, "R3b": HOTSH}[dO] * (np.bincount(gi[OLD7 | OLD5], minlength=NG) > 0)
        gO7 = gO5 = gO; gY7 = gY5 = np.zeros(NG)
    else:
        gO7, gY7, gO5, gY5 = group_df(dO, OLD7), group_df(dY, YOUNG7), group_df(dO, OLD5), group_df(dY, YOUNG5)
    tO7, tY7 = build_table(gO7, f"{rname} OLD7"), build_table(gY7, f"{rname} YOUNG7")
    if np.allclose(gO5, gO7) and np.allclose(gY5, gY7):
        tO5, tY5 = tO7, tY7
    else:
        tO5, tY5 = build_table(gO5, f"{rname} OLD5"), build_table(gY5, f"{rname} YOUNG5")
    rr = {}
    for f in FOOTS:
        A = A_of(tO7, tY7, f); D = D_of(tO5, tY5, f)
        clA = classify(A, A_meas, S_A); clD = classify(D, D_meas[f][0], D_meas[f][1])
        rr[f] = dict(A_pred=A, A_incr=A - nb[f], D_pred=D, verdict_A=clA, verdict_D=clD)
        P(f"  [{rname} {f:9s}] A_pred {A:+.5f} (increment {A - nb[f]:+.5f}) vs A_meas {A_meas:+.4f} +- {S_A:.4f} -> {clA[0]} / {clA[1]};"
          f"  D_pred {D:+.4f} vs {D_meas[f][0]:+.4f} +- {D_meas[f][1]:.4f} -> {clD[0]} / {clD[1]}")
    RES["routes"][rname] = rr
    RES["routes"][rname]["mean_group_df"] = dict(OLD7=float(np.mean(gO7[GSEL])), YOUNG7=float(np.mean(gY7[GSEL])))

if not MUTATE:
    P("\n--- verdicts (PRIMARY = R2, statistic A; secondary D)")
    for f in FOOTS:
        r = RES["routes"]["R2"][f]
        P(f"  {f:9s}: PRIMARY {r['verdict_A'][0]} ({r['verdict_A'][1]} the signal); secondary D {r['verdict_D'][0]} ({r['verdict_D'][1]})")
    for f in FOOTS:
        best = max(RES["routes"][k][f]["A_incr"] for k in ("R1", "R3a", "R3b"))
        cant = best < A_meas - 2 * S_A
        P(f"  ceiling [{f}]: largest R1/R3 increment {best:+.5f} vs meas - 2 sigma {A_meas - 2 * S_A:+.4f} -> "
          f"{'A5 CANNOT PRODUCE the signal by any allocation within the record cold gas and census' if cant else 'ceiling reaches the 2 sigma band'}")
        RES.setdefault("ceiling", {})[f] = dict(best_incr=best, cannot=bool(cant))
    RES["verdict"] = {f: RES["routes"]["R2"][f]["verdict_A"] for f in FOOTS}
else:
    P("\n--- M1 all-baryon source")
    for f in FOOTS:
        r = RES["routes"]["M1_Sall"][f]
        check(abs(r["A_incr"]) < 1e-6 and abs(r["D_pred"]) < 1e-6, f"M1 [{f}] S-all A increment {r['A_incr']:+.2e}, D {r['D_pred']:+.2e} (0 to 1e-6)")
    P("\n--- M3 linearity (derivative table, Delta f = +-0.05) and M2 shuffled ages")
    tP = build_table(np.full(NG, 0.05), "deriv +0.05"); tM = build_table(np.full(NG, -0.05), "deriv -0.05")
    DER = (TAB[tP] - TAB[tM]) / 0.10


    def lin_table(dfg):
        name = f"cfg651_lin{NEXT[0]}"; NEXT[0] += 1
        TAB[name] = TAB["d0"] + DER * dfg[GSEL][:, None, None, None]
        return name

    gO7, gY7 = group_df(DF_R2, OLD7), group_df(DF_R2, YOUNG7)
    tO, tY = build_table(gO7, "R2 OLD7 exact"), build_table(gY7, "R2 YOUNG7 exact")
    lO, lY = lin_table(gO7), lin_table(gY7)
    real_lin = {}
    for f in FOOTS:
        ex = A_of(tO, tY, f) - nb[f]; li = A_of(lO, lY, f) - nb[f]; real_lin[f] = li
        check(abs(li - ex) <= max(0.10 * abs(ex), 1e-4), f"M3 [{f}] R2 increment exact {ex:+.6f} vs linear {li:+.6f}")
    rng = np.random.default_rng(651)
    nul = {f: [] for f in FOOTS}
    for i in range(200):
        y, mi, o = tertiles(rng)
        a, b = lin_table(group_df(DF_R2, o)), lin_table(group_df(DF_R2, y))
        for f in FOOTS:
            oo, oy = own_stack(a, f, o), own_stack(b, f, y)
            o0, y0 = own_stack(base, f, o), own_stack(base, f, y)
            nul[f].append(math.log10((W[K9] @ oo[K9]) / (W[K9] @ oy[K9])) - math.log10((W[K9] @ o0[K9]) / (W[K9] @ y0[K9])))
        del TAB[a], TAB[b]
    for f in FOOTS:
        v = np.array(nul[f])
        check(abs(v.mean()) < v.std() / 3, f"M2 [{f}] shuffled-age R2 increment mean {v.mean():+.2e} vs sd/3 {v.std() / 3:.2e}")
        rank = float(np.mean(v <= real_lin[f]))
        P(f"    real-label linear increment {real_lin[f]:+.2e}; fraction of shuffles <= real {rank:.3f}")
        RES.setdefault("M2", {})[f] = dict(mean=float(v.mean()), sd=float(v.std()), real=real_lin[f], frac_le_real=rank)

RES["peak_rss_gb"] = rss_gb(); RES["elapsed_s"] = round(time.time() - T0, 1); RES["checks"] = CHECKS
P(f"\nchecks: {sum(c for c, _ in CHECKS)}/{len(CHECKS)} pass   peak RSS {rss_gb():.2f} GB   {time.time() - T0:.0f} s")
json.dump(RES, open(os.path.join(HERE, f"cfg651_results{TAG}.json"), "w"), indent=1, default=lambda x: x.tolist() if hasattr(x, "tolist") else str(x))
open(os.path.join(HERE, f"cfg651_predict{TAG}.out"), "w").write("\n".join(OUT) + "\n")
