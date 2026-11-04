"""LAM11 runner and summary (criteria c6f59aea4c). Six runs (M0, M_Na, M_CaT, M_TiO, M_IMF, M_blue) of LAM10's single-slope
profile on 100 real sums and 100 synthetics (lam11_sample.json). Job contract: SIGTERM or compute_queue/YIELD -> exit 75 at a
job boundary; --resume continues; lines fsync'd. Freed memory is returned to the system after every profile.
  python3 -I lam11_run.py --shard K --nshard N [--resume]
  python3 -I lam11_run.py --summarize MUTATE      lam11_MUTATE.out / .json (Gamma_b shuffled across galaxies within each run)
  python3 -I lam11_run.py --summarize             lam11.out / lam11.json (statistics, K0, K1, labels)
κ = ½ FITTED; not theory closed."""
import os, sys, json, signal, time, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[_v] = "1"
warnings.filterwarnings("ignore", message=".*encountered in matmul", category=RuntimeWarning)
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from scipy.stats import spearmanr
import lam11_core as M
L9 = M.L9
QY = os.path.join(L9.ROOT, "compute_queue", "YIELD"); FD = os.path.join(M.WORK, "runs"); os.makedirs(FD, exist_ok=True)
SEED = 20261106; NB = 2000
stop = False
def _term(*_):
    global stop; stop = True
signal.signal(signal.SIGTERM, _term); signal.signal(signal.SIGINT, _term)
arg = sys.argv[1:]
def opt(k, d=None): return arg[arg.index(k) + 1] if k in arg else d
SAMPLE = json.load(open(os.path.join(HERE, "lam11_sample.json")))
def jobs(): return [("real", p) for p in SAMPLE["real"]] + [("syn", i) for i in SAMPLE["synthetic"]]

def run(k, nk):
    S = L9.sample(); wave, narrow = L9.load_stack(); out = os.path.join(FD, f"lam11.s{k}of{nk}.jsonl"); L9.read_jsonl(out, repair=True)
    done = {(r["kind"], str(r["id"]), r["run"]) for r in L9.read_jsonl(out)}
    plan = {q["i"]: q for q in json.load(open(os.path.join(M.L9DIR, "lam9_k_rows.json")))["rows"]}
    mine = [jb for n_, jb in enumerate(jobs()) if n_ % nk == k]
    todo = [jb for jb in mine if not all((jb[0], str(jb[1]), r) in done for r in M.RUNS)]
    print(f"shard {k}/{nk}: {len(mine)} jobs, {len(todo)} to do; {M.mem()}", flush=True)
    if not todo: sys.exit(0)
    with open(out, "a") as fo:
        for n_, (kind, ident) in enumerate(todo):
            if stop or os.path.exists(QY): print("yield: exit 75", flush=True); fo.close(); sys.exit(75)
            t0 = time.time()
            if kind == "real":
                pf = ident; kin = S["FIT"][pf]; p = L9.prep(S["path"][pf], narrow); tpl, lam_t, n_t = L9.templates_for(p); flux = None; extra = {}
            else:
                q = plan[ident]; pf = q["donor"]; kin = S["FIT"][pf]; p = L9.prep(S["path"][pf], narrow); tpl, lam_t, n_t = L9.templates_for(p)
                flux, a_in = M.build_syn(q, S, narrow, tpl, lam_t, n_t, p); extra = dict(gamma_in=q["gamma_in"], alpha_in=a_in, alpha_in_lam9=q["alpha_in"])
            for r_ in M.RUNS:
                if (kind, str(ident), r_) in done: continue
                rec = dict(kind=kind, id=ident, run=r_, **extra)
                try:
                    pp, good = M.run_inputs(p, r_); f = None if flux is None else flux[:len(pp["lam"])]
                    rec.update(status="ok", **M.profile_r(pp, tpl, lam_t, n_t, kin, good, flux=f))
                    if r_ != "M0": rec.pop("chi2_regions", None)
                except Exception as ex: rec["status"] = f"error: {ex}"
                M.relieve(); rec["sec"] = round(time.time() - t0, 1); L9.append_jsonl(fo, rec)
            if n_ % 5 == 0: print(f"  job {n_ + 1}/{len(todo)} done; {M.mem()}", flush=True)
    print(f"shard done; {M.mem()}", flush=True); sys.exit(0)

def spear_ci(g, x, seed=SEED):
    rho = float(spearmanr(g, x).statistic); rg = np.random.default_rng(seed); n = len(g); bs = []
    for _ in range(NB):
        i = rg.integers(0, n, n); bs.append(spearmanr(g[i], x[i]).statistic)
    return rho, [float(v) for v in np.nanpercentile(bs, [2.5, 97.5])]

def summarize(mode):
    rows = []
    for fn in sorted(os.listdir(FD)):
        if fn.endswith(".jsonl"): rows += L9.read_jsonl(os.path.join(FD, fn), repair=True)
    R = {}
    for r in rows: R[(r["kind"], str(r["id"]), r["run"])] = r
    S = L9.sample(); idx = {p: i for i, p in enumerate(S["pifu"])}; sig = S["K"]["sig"]
    L10 = {r["plateifu"]: r for r in json.load(open(os.path.join(M.L10DIR, "lam10_fits.json")))["A"]}
    t3 = SAMPLE["sigma_tercile_edges"]; real = SAMPLE["real"]
    O = [f"LAM11 summary, mode {mode}. κ = ½ FITTED; not theory closed."]; RES = {"lane": "LAM11", "mode": mode, "note": "κ = ½ FITTED; not theory closed"}
    errs = sum(1 for r in rows if r["status"] != "ok"); O.append(f"lines {len(rows)} (planned {len(jobs()) * len(M.RUNS)}), errors {errs}")
    rgm = np.random.default_rng(SEED); stats = {}
    for run in M.RUNS:
        rr = [R.get(("real", p, run)) for p in real]; ok = [x for x in rr if x and x["status"] == "ok"]
        g = np.array([x["gamma_best"] for x in ok]); ls = np.log10([sig[idx[x["id"]]] for x in ok]); ed = np.array([x["j"] == 0 for x in ok])
        if mode == "MUTATE": g = g[rgm.permutation(len(g))]
        rho, ci = spear_ci(g, ls)
        st = dict(n=len(ok), edge_fraction=float(ed.mean()), median_gamma=float(np.median(g)), spearman=rho, spearman_ci=ci, median_alpha_ku2=float(np.median([x["alpha_ku2"] for x in ok])))
        st["removes"] = bool(st["edge_fraction"] < 0.15 and ci[1] >= 0)
        l10e = np.array([L10[x["id"]]["j"] == 0 for x in ok]); ter = np.array([int(np.searchsorted(t3, sig[idx[x["id"]]], side="right")) for x in ok])
        st["edge_by_lam10_status"] = {"was_edge": float(ed[l10e].mean()), "was_not": float(ed[~l10e].mean())}
        st["edge_by_sigma_third"] = [float(ed[ter == t].mean()) for t in range(3)]
        stats[run] = st
        O.append(f"[{run}] n {st['n']}: edge fraction {st['edge_fraction']:.2f}; median Gamma_b {st['median_gamma']:.2f}; Spearman(Gamma_b, log sigma) {rho:+.3f} "
                 f"[{ci[0]:+.3f}, {ci[1]:+.3f}]; removes the pile-up: {st['removes']}" + ("" if mode == "MUTATE" else
                 f"; median alpha_KU2 {st['median_alpha_ku2']:.2f}; edge share was-edge/was-not {st['edge_by_lam10_status']['was_edge']:.2f}/{st['edge_by_lam10_status']['was_not']:.2f}, "
                 f"by sigma third {np.round(st['edge_by_sigma_third'], 2).tolist()}"))
    RES["runs"] = stats
    if mode == "MUTATE":
        ok_m = all(stats[r]["spearman_ci"][0] <= 0 <= stats[r]["spearman_ci"][1] for r in M.RUNS); RES["MUTATE_pass"] = bool(ok_m)
        O.append(f"MUTATE: Spearman interval includes 0 in every run: {'PASS' if ok_m else 'FAIL'}")
    else:
        # M0's per-region chi2 gain of Gamma_b 0.3 over 1.3
        i03, i13 = int(np.argmin(np.abs(M.GAM - 0.3))), int(np.argmin(np.abs(M.GAM - 1.3))); gains = {k: [] for k in ("Na", "CaT", "TiO", "blue_other", "red_other")}
        for p in real:
            x = R.get(("real", p, "M0"))
            if x and x["status"] == "ok":
                for k in gains: gains[k].append(x["chi2_regions"][i13][k] - x["chi2_regions"][i03][k])
        tot = sum(sum(v) for v in gains.values()); RES["M0_gain"] = {k: dict(median=float(np.median(v)), share=float(sum(v) / tot) if tot else float("nan")) for k, v in gains.items()}
        O.append("M0 chi2 gain of Gamma_b 0.3 over 1.3 by region (median per galaxy; share of the summed gain): " +
                 "; ".join(f"{k} {v['median']:+.1f} ({v['share']:+.2f})" for k, v in RES["M0_gain"].items()) + f"; summed gain {tot:+.0f}")
        # K0
        d = [abs(R[("real", p, "M0")]["gamma_best"] - L10[p]["gamma_best"]) for p in real if ("real", p, "M0") in R]
        dj = sum(1 for p in real if ("real", p, "M0") in R and R[("real", p, "M0")]["j"] != L10[p]["j"]); k0 = len(d) == 100 and max(d) <= 1e-9 and dj == 0
        RES["K0"] = dict(n=len(d), max_abs_diff=float(max(d)) if d else float("nan"), j_mismatch=dj, PASS=bool(k0))
        O.append(f"K0 reproduction of LAM10 (M0 Gamma_best, grid index): n {len(d)}, max |diff| {max(d):.1e}, index mismatches {dj}: {'PASS' if k0 else 'FAIL'}")
        # K1
        k1 = True; RES["K1"] = {}
        rep = [abs(R[("syn", str(i), "M0")]["alpha_in"] / R[("syn", str(i), "M0")]["alpha_in_lam9"] - 1) for i in SAMPLE["synthetic"] if ("syn", str(i), "M0") in R]
        for run in M.RUNS:
            ss = [R.get(("syn", str(i), run)) for i in SAMPLE["synthetic"]]; ok = [x for x in ss if x and x["status"] == "ok"]
            ef = float(np.mean([x["j"] == 0 for x in ok])) if ok else float("nan"); k1 &= (len(ok) == 100 and ef <= 0.05)
            RES["K1"][run] = dict(n=len(ok), edge_fraction=ef, median_dgamma=float(np.median([x["gamma_best"] - x["gamma_in"] for x in ok])),
                                  median_dlalpha=float(np.median([np.log10(x["alpha"] / x["alpha_in"]) for x in ok])))
            O.append(f"K1 [{run}] synthetics n {len(ok)}: edge fraction {ef:.2f} (<= 0.05); median dGamma_b {RES['K1'][run]['median_dgamma']:+.3f}; median dlog alpha {RES['K1'][run]['median_dlalpha']:+.4f}")
        RES["K1_PASS"] = bool(k1); RES["K1_alpha_in_repro_max_rel"] = float(max(rep)) if rep else float("nan")
        O.append(f"K1 (no mask creates edge hits): {'PASS' if k1 else 'FAIL'}; synthetic alpha_in vs LAM9 max relative difference {RES['K1_alpha_in_repro_max_rel']:.1e}")
        mp = os.path.join(HERE, "lam11_MUTATE.json"); mut = json.load(open(mp))["MUTATE_pass"] if os.path.exists(mp) else None
        Rm = {r: stats[r]["removes"] for r in M.RUNS}; singles = [r for r in ("M_Na", "M_CaT", "M_TiO") if Rm[r]]
        blue_share = RES["M0_gain"]["blue_other"]["share"]
        if not (k0 and k1) or mut is False: lab = "NOT DIAGNOSED"
        elif singles == ["M_Na"]: lab = "DRIVEN BY Na"
        elif singles and "M_Na" not in singles: lab = "DRIVEN BY TiO/CaT (" + ", ".join(s[2:] for s in singles) + ")"
        elif len(singles) >= 2 or Rm["M_IMF"]: lab = "MIXED"
        elif Rm["M_blue"]: lab = "DRIVEN BY THE RED END, OUTSIDE THE IMF WINDOWS"
        elif blue_share > 0.5: lab = "DRIVEN BY BLUE"
        else: lab = "NOT DIAGNOSED"
        if mut is None: lab += " (PROVISIONAL: MUTATE not run)"
        RES["label"] = lab; RES["MUTATE_pass"] = mut; O.append(f"MUTATE: {mut}\nLABEL: {lab}")
    sfx = "" if mode == "REAL" else f"_{mode}"
    print("\n".join(O), flush=True); open(os.path.join(HERE, f"lam11{sfx}.out"), "w", encoding="utf-8").write("\n".join(O) + "\n")
    json.dump(RES, open(os.path.join(HERE, f"lam11{sfx}.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=float)

if __name__ == "__main__":
    if "--summarize" in arg: summarize("MUTATE" if "MUTATE" in arg else "REAL")
    else: run(int(opt("--shard", "0")), int(opt("--nshard", "1")))
