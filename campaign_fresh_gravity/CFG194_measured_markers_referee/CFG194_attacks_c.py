#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG194 attacks C-a..C-e (error model, sign-flip, mocks under three laws) and D1-D2 (the kept C2' failure).
Written from CFG194_FROZEN_CRITERIA.md alone.
    ZF_REPO=<repo> python3 CFG194_attacks_c.py [seed] > CFG194_attacks_c_seed<seed>.out       (seed 194 and 195; N = 10,000 per world and family)
    CFG194_NMOCK=<n> overrides N for a quick test."""
import sys
import json
import math
import time
import numpy as np
from scipy import stats
from CFG194_lib import *   # noqa
import CFG194_lib as L

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 194
NMOCK = int(os.environ.get("CFG194_NMOCK", "10000"))
t_start = time.time()
AS = M.load_sparc_anchor()
mk = load_markers()
sg = load_sigma()
mcur = load_model_curves()
S_model = M.load_kurvs(inc_col="inc_star_deg")
I = {int(r["kurvs_id"]): r for r in read_rows("data_assembly/arxiv_tables/kurvs2023_integrated.csv")}
Vt = {int(r["kurvs_id"]): r for r in read_rows("data_assembly/arxiv_tables/kurvs2023_velocities_at_radii.csv")}
SP1 = spec_s(1.0)
RES = {"seed": SEED, "N": NMOCK}
prim_S, info = build(rule_primary, mk=mk, sg=sg)
cp = cells_three(prim_S, AS, SP1)
P("=" * 100)
P(f"CFG194 attacks C/D.  seed={SEED} N={NMOCK}  repo=<repo>")
P("=" * 100)
P("primary:", fmt_cells(cp))

# ------------------------------------------------------------------ C-a marker consistency with the model curve
P("\n-- C-a: measured V_out against the digitised model curve read at R_out (both deprojected by sin i_SFR)")
Vm = np.array([abs(np.interp(info[j]["side"] * info[j]["R"], mcur[k]["R"], mcur[k]["v"])) / math.sin(math.radians(fnum(I[k]["inc_sfr_deg"]))) for j, k in enumerate(IDS)])
Vmeas = np.array([x["V"] for x in info])
eV = np.array([x["eV"] for x in info])
pull = (Vmeas - Vm) / eV
chi2 = float(np.sum(pull ** 2))
p = float(stats.chi2.sf(chi2, 10))
rms = float(np.sqrt(np.mean(pull ** 2)))
P("  pulls:", [round(x, 2) for x in pull])
P(f"  chi2 = {chi2:.2f} for 10 dof, p = {p:.3f}; rms pull {rms:.2f}; mean pull {pull.mean():+.2f}; fractional (meas/model-1) mean {np.mean(Vmeas/Vm-1):+.3f}")
pm = cells_three(S_model, AS, SP1)
P(f"  pooled chi2/dof inside pool (flat): model-value run {pm['flat']['chi2dof']:.2f}, measured primary {cp['flat']['chi2dof']:.2f}")
RES["C_a"] = dict(chi2=chi2, p=p, rms=rms, pulls=pull.tolist(), chi2dof_model=pm["flat"]["chi2dof"], chi2dof_meas=cp["flat"]["chi2dof"])

# ------------------------------------------------------------------ C-b sign-flip test
P("\n-- C-b: sign-flip test of the value-only shift (baseline = model curve at R_out; primary errors and sigma held fixed)")
S_base = copy.copy(prim_S)
S_base.V = Vm.copy()


def shift_for(eps):
    S_ = copy.copy(prim_S)
    S_.V = Vm * (Vmeas / Vm) ** eps
    c = cells_three(S_, AS, SP1)
    return np.array([c[l]["dprime"] for l in LAWS])


base_dp = np.array([cells_three(S_base, AS, SP1)[l]["dprime"] for l in LAWS])
obs_shift = shift_for(np.ones(10)) - base_dp
P("  observed value-only shifts (flat, rival, T):", obs_shift.round(4))
rng = np.random.default_rng(SEED)
NF = 10000
sim = np.zeros((NF, 3))
for i in range(NF):
    e = rng.choice([-1.0, 1.0], 10)
    sim[i] = shift_for(e) - base_dp
pv = [float(np.mean(np.abs(sim[:, j]) >= abs(obs_shift[j]))) for j in range(3)]
P(f"  random signs N={NF}: sd of the shift {sim.std(axis=0).round(4)}; two-sided p (flat, rival, T) = {np.round(pv,3)}")
ex = []
for m in range(1024):
    e = np.array([1.0 if (m >> b) & 1 else -1.0 for b in range(10)])
    ex.append(shift_for(e) - base_dp)
ex = np.array(ex)
pe = [float(np.mean(np.abs(ex[:, j]) >= abs(obs_shift[j]))) for j in range(3)]
P(f"  exact enumeration (1024 sign vectors): p (flat, rival, T) = {np.round(pe,3)}")
RES["C_b"] = dict(obs=obs_shift.tolist(), sd=sim.std(axis=0).tolist(), p_random=pv, p_exact=pe)

# ------------------------------------------------------------------ C-d error variants
P("\n-- C-d: error-model variants (decision cell)")
CD = {}


def rec(nm, S_, extra_sig=None):
    c = cells_three(S_, AS, SP1)
    d = {}
    for l in LAWS:
        sgm = c[l]["sigma"] if extra_sig is None else math.sqrt(c[l]["sigma"] ** 2 + extra_sig[l] ** 2)
        d[l] = dict(dprime=c[l]["dprime"], sigma=sgm, z=c[l]["dprime"] / sgm)
    cl = M.classify(d["flat"]["z"], d["rival"]["z"])
    CD[nm] = dict(d, cls=cl)
    P(f"  {nm:60s}" + " ".join(f"{l}:{d[l]['dprime']:+.3f}+-{d[l]['sigma']:.3f}({d[l]['z']:+.2f})" for l in LAWS) + f"  {cl}")


rec("E1 mean bar (primary)", prim_S)
S_, _ = build(rule_primary, mk=mk_err(mk, "max"), sg=sg)
rec("E2 larger bar", S_)
S_, _ = build(rule_primary, mk=mk_err(mk, "min"), sg=sg)
rec("E3 smaller bar", S_)
S_, _ = build(rule_primary, mk=mk, sg=sg, err_mult=1.5)
rec("E4 errors x 1.5 (correlated neighbours)", S_)
S_, _ = build(rule_primary, mk=mk, sg=sg, err_floor=5.0)
rec("E5 5 km/s floor in quadrature", S_)
Sp, _ = build(rule_primary, mk=mk, sg=sg, vscale=1.01)
cpl = cells_three(Sp, AS, SP1)
sys_add = {l: abs(cpl[l]["dprime"] - cp[l]["dprime"]) / math.log(1.01) * 0.03 for l in LAWS}
rec("E6 common V-scale error ln s ~ N(0, 0.03) as covariance", prim_S, extra_sig=sys_add)
P("  (E6 added sigma:", {l: round(v, 4) for l, v in sys_add.items()}, ")")
RES["C_d"] = CD

# ------------------------------------------------------------------ C-e mocks
P("\n-- C-e: mock null worlds, three laws x families; truth = real baryons, sigma_out, R_out, marker errors; analysis = primary pipeline")
extra_scale = math.sqrt(max(0.0, rms ** 2 - 1.0))
P(f"  N1x extra per-marker scatter factor sqrt(max(0, rms_pull^2 - 1)) = {extra_scale:.3f} (x marker error)")
sp_an = SP1
AP = M.anchor_pool(sp_an, 0.0, "canonical", AS)
am, ae, _ = AP["flat"]
am_off = am
P(f"  mock worlds carry the anchor's z=0 pipeline offset {am_off:+.4f} dex (first draft of this script omitted it: flat-truth ideal mocks then sat at Delta' = -0.069; kept as a note)")


def analyse(S_, want_T=True):
    po = M.per_object(S_, sp_an, DEC_MU, 0.0, "canonical")
    out = []
    for key in ("flat", "H"):
        m, e, c = M.pool(po["d_" + key], po["e_" + key])
        out.append((m - am, math.sqrt(e ** 2 + ae ** 2)))
    if want_T:
        with law_ctx(E_T):
            po = M.per_object(S_, sp_an, DEC_MU, 0.0, "canonical")
        m, e, c = M.pool(po["d_H"], po["e_H"])
        out.append((m - am, math.sqrt(e ** 2 + ae ** 2)))
    return out


LAWF = {"flat": E_flat, "rival": L._E_RIVAL, "T": L.E_T}
A0c = M.A0["canonical"]


def truth_vobs(S_t, law, rng_, family):
    """returns the noiseless observed (deprojected) velocity V_obs for the truth world."""
    n = len(S_t.ids)
    St = copy.copy(S_t)
    if family in ("N1", "N1x"):
        mu = 1.0 * 10.0 ** (0.3 * rng_.standard_normal(n))
        St.mgas_abs = mu * 10.0 ** S_t.logM
        af = np.exp(0.4 * rng_.standard_normal(n)) * math.exp(0.2 * rng_.standard_normal())
    else:
        St.mgas_abs = None
        af = np.ones(n)
    gb = M.gbar(St, DEC_MU, 0.0)
    a = A0c * LAWF[law](S_t.z)
    g = M.gpred(gb, a) * 10.0 ** am_off      # the world carries the pipeline's own z = 0 offset (SPARC anchor), as CFG165's mocks did
    Vc2 = g * (S_t.R * M.KPC) / 1e6
    x = S_t.R / S_t.Reff - 1.0
    al = M.alpha_K(x) * af
    V2 = np.maximum(Vc2 - al * S_t.sig ** 2, 0.0025 * Vc2)
    return np.sqrt(V2)


def run_world(S_t, law, family, N, seed, status_n=1000):
    rng_ = np.random.default_rng(seed)
    res = np.zeros((N, 3, 2))
    Tal = 0
    for i in range(N):
        v0 = truth_vobs(S_t, law, rng_, family)
        noise = rng_.standard_normal(len(v0)) * S_t.eV
        if family == "N1x":
            noise = noise + rng_.standard_normal(len(v0)) * S_t.eV * extra_scale
        Sm = copy.copy(S_t)
        Sm.mgas_abs = None
        Sm.V = np.maximum(v0 + noise, 1.0)
        a = analyse(Sm)
        res[i] = np.array(a)
        if i < status_n:
            be = break_even(Sm, AS, sp_an, "T")
            Tal += (status(be) == "allowed")
    return res, Tal / min(status_n, N)


def summarise(res, Tfrac):
    z = res[:, :, 0] / res[:, :, 1]
    cls = [M.classify(z[i, 0], z[i, 1]) for i in range(len(z))]
    fr = {c: cls.count(c) / len(cls) for c in sorted(set(cls))}
    return dict(mean=res[:, :, 0].mean(axis=0).tolist(), sd=res[:, :, 0].std(axis=0).tolist(), mean_sigma=res[:, :, 1].mean(axis=0).tolist(),
                P_zflat_ge_obs=float(np.mean(z[:, 0] >= cp["flat"]["z"])), classes=fr, P_lean_rival=fr.get("lean rival", 0.0),
                T_allowed_frac=Tfrac, dflat=res[:, 0, 0].tolist())


def lr(dfl_a, dfl_b, x):
    """density ratio a/b at x: gaussian and KDE."""
    ga = stats.norm.pdf(x, np.mean(dfl_a), np.std(dfl_a)) / stats.norm.pdf(x, np.mean(dfl_b), np.std(dfl_b))
    ka = stats.gaussian_kde(dfl_a)(x)[0] / max(stats.gaussian_kde(dfl_b)(x)[0], 1e-300)
    return float(ga), float(ka)


MOCK = {}
fams = ["ideal", "N1"] + (["N1x"] if rms > 1.0 else [])
templates = [("meas", prim_S), ("modelerr", S_model)]
for tname, St in templates:
    for fam in fams:
        if tname == "modelerr" and fam == "N1x":
            continue
        for law in LAWS:
            t0 = time.time()
            res, Tf = run_world(St, law, fam, NMOCK, SEED * 1000 + 7 * len(fam) + {"flat": 1, "rival": 2, "T": 3}[law] + (0 if tname == "meas" else 500))
            sm = summarise(res, Tf)
            MOCK[f"{tname}|{fam}|{law}"] = sm
            P(f"  {tname:8s} {fam:5s} truth={law:6s} mean Delta' " + " ".join(f"{v:+.3f}" for v in sm["mean"]) + f"  sd_flat {sm['sd'][0]:.3f}  P(z_flat>={cp['flat']['z']:.2f})={sm['P_zflat_ge_obs']:.3f}  P(lean rival)={sm['P_lean_rival']:.3f}  T allowed@s=1: {sm['T_allowed_frac']:.2f}  [{time.time()-t0:.0f}s]")
P("\n  classes per world:")
for k, v in MOCK.items():
    P(f"   {k:22s}", {c: round(f, 3) for c, f in v["classes"].items()})
P("\n  likelihood ratios at the observed primary Delta'_flat = %+.4f (Gaussian, KDE):" % cp["flat"]["dprime"])
LRS = {}
for tname, _ in templates:
    for fam in fams:
        if f"{tname}|{fam}|flat" not in MOCK:
            continue
        df = np.array(MOCK[f"{tname}|{fam}|flat"]["dflat"])
        for law in ("rival", "T"):
            a = np.array(MOCK[f"{tname}|{fam}|{law}"]["dflat"])
            g_, k_ = lr(a, df, cp["flat"]["dprime"])
            LRS[f"{tname}|{fam}|{law}/flat"] = (g_, k_)
            P(f"   {tname:8s} {fam:5s} {law}-truth / flat-truth: {g_:8.2f}  {k_:8.2f}")
P("\n  frozen informativeness rule (P(lean rival | flat) < 0.05 and P(lean rival | rival) > 0.3):")
RULE = {}
for tname, _ in templates:
    for fam in fams:
        if f"{tname}|{fam}|flat" not in MOCK:
            continue
        pf, pr, pt = (MOCK[f"{tname}|{fam}|{l}"]["P_lean_rival"] for l in ("flat", "rival", "T"))
        ok = pf < 0.05 and pr > 0.3
        RULE[f"{tname}|{fam}"] = dict(P_flat=pf, P_rival=pr, P_T=pt, ok=ok)
        P(f"   {tname:8s} {fam:5s} P(lean rival | flat)={pf:.3f}  | rival)={pr:.3f}  | T)={pt:.3f}  -> {'JUSTIFIED' if ok else 'NOT justified'}")
for k in MOCK:
    MOCK[k].pop("dflat")
RES["C_e"] = dict(mock=MOCK, LR=LRS, rule=RULE, rms_pull=rms, fams=fams)

# ------------------------------------------------------------------ D: the kept C2' failure
P("\n-- D2: repairs of C2' (labelled post hoc); primary and V-b rows; decision cell")
D = {}


def rows(tag, mk_=mk, sg_=sg, drops=None, ids=None, sigmode="interp"):
    out = {}
    for nm, rule, kw in (("primary", rule_primary, dict(sigmode=sigmode)), ("V-a", rule_outerk, dict(k=3)), ("V-b", rule_bothsides, {}),
                         ("V-c", rule_primary, dict(allow_clipped=True, sigmode=sigmode))):
        S_, i_ = build(rule, ids=ids, mk=mk_, sg=sg_, drops=drops, **kw)
        c = cells_three(S_, AS, SP1)
        out[nm] = dict(cls=classes(c), z={l: c[l]["z"] for l in LAWS}, n=len(S_.ids))
    Sd_, _ = build(rule_primary, ids=ids, mk=mk_, sg=sg_, drops=drops, inc_col="inc_star_deg", sigmode=sigmode)
    c = cells_three(Sd_, AS, SP1)
    out["V-d"] = dict(cls=classes(c), z={l: c[l]["z"] for l in LAWS}, n=len(Sd_.ids))
    D[tag] = out
    P(f"  {tag:58s}" + " | ".join(f"{n}: {d['cls'][:9]:9s} {d['z']['flat']:+.2f} {d['z']['rival']:+.2f} {d['z']['T']:+.2f}" for n, d in out.items()))


rows("D0 as run (C2' unrepaired)")
off17 = float(np.median([R - sg[17]["R"][np.sign(sg[17]["R"]) == np.sign(R)][np.argmin(np.abs(sg[17]["R"][np.sign(sg[17]["R"]) == np.sign(R)] - R))] for R in mk[17]["R"] if True][:19]))
sg_sh = {k: dict(v) for k, v in sg.items()}
sg_sh[17] = dict(sg[17]); sg_sh[17]["R"] = sg[17]["R"] + off17
P(f"  KURVS-17 constant offset R_v - R_sigma (median of nearest-neighbour differences): {off17:+.4f} kpc")
rows("D2(i) KURVS-17 sigma profile shifted by its offset", sg_=sg_sh)
rows("D2(ii) sigma from the nearest sigma marker (no interpolation)", sigmode="nearest")
rows("D2(iii) KURVS-17 dropped", ids=[k for k in IDS if k != 17])
# (iv) KURVS-3's extra markers: those velocity markers whose nearest sigma marker is > 0.5 kpc away
drops = {}
for k in IDS:
    d = np.zeros(len(mk[k]["R"]), bool)
    for j, R in enumerate(mk[k]["R"]):
        m_ = np.sign(sg[k]["R"]) == np.sign(R)
        if np.min(np.abs(sg[k]["R"][m_] - R)) > 0.5:
            d[j] = True
    drops[k] = d
P("  velocity markers with no sigma counterpart (> 0.5 kpc):", {k: mk[k]["R"][d].round(2).tolist() for k, d in drops.items() if d.any()})
rows("D2(iv) markers with no sigma counterpart dropped from the velocity lists", drops=drops)
used = {}
for nm, rule, kw in (("primary", rule_primary, {}), ("V-b", rule_bothsides, {}), ("V-c", rule_primary, dict(allow_clipped=True))):
    _, i_ = build(rule, mk=mk, sg=sg, **kw)
    for x in i_:
        for j in np.where(drops.get(x["id"], np.zeros(0, bool)))[0]:
            if abs(abs(mk[x["id"]]["R"][j]) - x["R"]) < 0.02 and np.sign(mk[x["id"]]["R"][j]) == (x["side"] if x["side"] != 0 else np.sign(mk[x["id"]]["R"][j])):
                used.setdefault(nm, []).append(x["id"])
P("  discs where a dropped marker is the outer point (primary, V-b, V-c):", used)
base = D["D0 as run (C2' unrepaired)"]
mx, chg = 0.0, []
for tag, out in D.items():
    if tag.startswith("D0"):
        continue
    for nm in ("primary", "V-b"):
        for l in LAWS:
            mx = max(mx, abs(out[nm]["z"][l] - base[nm]["z"][l]))
        if out[nm]["cls"] != base[nm]["cls"]:
            chg.append((tag, nm, out[nm]["cls"]))
P(f"  largest |dz| over D2 (i-iv), primary and V-b rows: {mx:.3f}; class changes: {chg}")
P(f"  C2' is {'IMMATERIAL' if mx <= 0.10 and not chg else 'MATERIAL (in the frozen sense)'} (line: no class change and |dz| <= 0.10)")
mx2 = 0.0
for tag, out in D.items():
    if tag.startswith("D0") or tag.startswith("D2(iii)"):
        continue
    for nm in ("primary", "V-a", "V-b", "V-c", "V-d"):
        for l in LAWS:
            mx2 = max(mx2, abs(out[nm]["z"][l] - base[nm]["z"][l]))
chg2 = [(tag, nm) for tag, out in D.items() if not tag.startswith("D0") and not tag.startswith("D2(iii)") for nm in out if out[nm]["cls"] != base[nm]["cls"]]
P(f"  (post hoc) without D2(iii), which drops a disc rather than repairing the radius mismatch: largest |dz| over all five rows {mx2:.3f}; class changes {chg2}")
RES["D2"] = dict(rows=D, max_dz=mx, max_dz_without_iii=mx2, class_changes_without_iii=chg2, class_changes=chg, offset17=off17, immaterial=(mx <= 0.10 and not chg))

with open(os.path.join(HERE, f"CFG194_attacks_c_results_seed{SEED}.json"), "w") as f:
    json.dump(RES, f, indent=1, default=jdefault)
P(f"\ndone in {time.time()-t_start:.0f} s")
