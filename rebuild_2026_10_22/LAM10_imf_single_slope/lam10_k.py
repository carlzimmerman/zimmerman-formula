"""LAM10 K1 and K2 (criteria e70770e272): LAM9's 300 synthetic sums, rebuilt exactly with LAM9's code (same donors, Gamma_b_in
and seeds; alpha_in checked against LAM9's record), each fitted with the single-slope chi2 profile in variants A and B; K2 refits
the first 100 (variant A) with h4 +- 0.03. Job contract: SIGTERM or compute_queue/YIELD -> exit 75 at a synthetic boundary;
--resume continues; lines fsync'd.
  python3 -I lam10_k.py --shard K --nshard N [--resume]
  python3 -I lam10_k.py --summarize                     lam10_k.out, lam10_k.json, lam10_k_rows.json in this folder
κ = ½ FITTED; not theory closed."""
import os, sys, json, signal, time, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[_v] = "1"
warnings.filterwarnings("ignore", message=".*encountered in matmul", category=RuntimeWarning)
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from ppxf.ppxf import ppxf
import lam10_core as C
L9 = C.L9
QY = os.path.join(L9.ROOT, "compute_queue", "YIELD"); KD = os.path.join(C.WORK, "k"); os.makedirs(KD, exist_ok=True)
L9W = os.path.join(L9.EXT, "lam9_work_2026_11_04", "w")
stop = False
def _term(*_):
    global stop; stop = True
signal.signal(signal.SIGTERM, _term); signal.signal(signal.SIGINT, _term)
arg = sys.argv[1:]
def opt(k, d=None): return arg[arg.index(k) + 1] if k in arg else d
def plan(): return json.load(open(os.path.join(C.L9DIR, "lam9_k_rows.json")))["rows"]

def run(k, nk):
    S = L9.sample(); wave, narrow = L9.load_stack(); out = os.path.join(KD, f"lam10_k.s{k}of{nk}.jsonl"); L9.read_jsonl(out, repair=True)
    done = {r["i"] for r in L9.read_jsonl(out)}; mine = [q for q in plan() if q["i"] % nk == k and q["i"] not in done]
    print(f"K shard {k}/{nk}: {len(mine)} to do", flush=True)
    if not mine: sys.exit(0)
    T = L9.tlib(); ug = np.unique(T["gamma"])
    with open(out, "a") as fo:
        for q in mine:
            if stop or os.path.exists(QY): print("yield: exit 75", flush=True); fo.close(); sys.exit(75)
            t0 = time.time(); pf = q["donor"]; kin = S["FIT"][pf]; p = L9.prep(S["path"][pf], narrow); tpl, lam_t, n_t = L9.templates_for(p)
            W = np.load(os.path.join(L9W, f"{pf}_A.npz")); wb = W["wb"].astype(float); mp = W["mpoly"].astype(float); chi2a = float(W["chi2a"])
            WL = wb.reshape(L9.REG_DIM).sum(axis=2); w_in = np.zeros(L9.REG_DIM); w_in[:, :, int(np.argmin(np.abs(ug - q["gamma_in"])))] = WL; w_in = w_in.ravel()
            r = dict(i=q["i"], third=q["third"], donor=pf, gamma_in=q["gamma_in"], seed=q["seed"])
            try:
                a_in = L9.summary(w_in, n_t)["alpha"]; r["alpha_in"] = a_in; r["alpha_in_lam9"] = q["alpha_in"]
                pc = ppxf((tpl @ w_in)[:, None], p["flux"] / mp, p["noise"] / mp, L9.VELSCALE, L9.kin_start(kin), moments=6, fixed=[1] * 6, degree=-1, mdegree=0,
                          goodpixels=p["goodA"], lam=p["lam"], lam_temp=lam_t, quiet=True)
                syn = pc.bestfit * mp * (1 + narrow[p["idx"]])
                syn = syn + np.random.default_rng(q["seed"]).normal(0, 1, syn.size) * np.where(p["noise"] < 1e9, p["noise"], 0) * np.sqrt(max(chi2a, 1.0))
                for v in ("A", "B"): r[v] = C.profile(p, tpl, lam_t, n_t, kin, v, flux=syn)
                if q["i"] < 100:
                    for sg, dh in (("p", 0.03), ("m", -0.03)): r[f"alpha_h4{sg}"] = C.profile(p, tpl, lam_t, n_t, kin, "A", flux=syn, dh4=dh)["alpha"]
                r["status"] = "ok"
            except Exception as ex: r["status"] = f"error: {ex}"
            r["sec"] = round(time.time() - t0, 1); L9.append_jsonl(fo, r)
    sys.exit(0)

def lines(dg, da):
    return dict(gamma_bias=float(np.median(dg)), gamma_rms=float(np.sqrt(np.mean(dg ** 2))), lalpha_bias=float(np.median(da)), lalpha_rms=float(np.sqrt(np.mean(da ** 2))))
def summarize():
    rows = []
    for fn in sorted(os.listdir(KD)):
        if fn.endswith(".jsonl"): rows += L9.read_jsonl(os.path.join(KD, fn), repair=True)
    rows = sorted({r["i"]: r for r in rows}.values(), key=lambda r: r["i"]); ok = [r for r in rows if r["status"] == "ok"]
    rel = max(abs(r["alpha_in"] / r["alpha_in_lam9"] - 1) for r in ok) if ok else float("nan"); repro = bool(rel <= 1e-9)
    json.dump(dict(note="κ = ½ FITTED; not theory closed. One row per K synthetic (lam10_k.py).", rows=rows), open(os.path.join(HERE, "lam10_k_rows.json"), "w", encoding="utf-8"),
              indent=0, ensure_ascii=False, default=float)
    P = json.load(open(os.path.join(C.L9DIR, "lam9_prepare.json"))); S = L9.sample()
    iqr = float(np.subtract(*np.percentile([S["FIT"][r["plateifu"]]["h4"] for r in P["rows"] if r["step5"]], [75, 25])))
    O = [f"LAM10 K control: {len(ok)} of {len(rows)} synthetics ok (300 planned). κ = ½ FITTED; not theory closed.",
         f"reproduction of LAM9's alpha_in: max relative difference {rel:.1e} (<= 1e-9): {'PASS' if repro else 'FAIL -> NO VERDICT'}"]
    R = {"note": "κ = ½ FITTED; not theory closed", "n": len(rows), "n_ok": len(ok), "repro_max_rel": rel, "repro_pass": repro}
    for v in ("A", "B"):
        dg = np.array([r[v]["gamma_best"] - r["gamma_in"] for r in ok]); da = np.array([np.log10(r[v]["alpha"] / r["alpha_in"]) for r in ok])
        L = lines(dg, da); p_ = abs(L["gamma_bias"]) <= 0.15 and L["gamma_rms"] <= 0.40 and abs(L["lalpha_bias"]) <= 0.03 and L["lalpha_rms"] <= 0.10
        sig = np.array([r[v]["sigma"] for r in ok]); fin = np.isfinite(sig) & (sig > 0); pull = dg[fin] / sig[fin]
        edges = sum(1 for r in ok if r[v]["edge"]); dchi = np.array([r[v]["lalpha_chi"] - np.log10(r["alpha_in"]) for r in ok])
        R[f"K1_{v}"] = dict(**L, PASS=bool(p_ and len(rows) == 300), slope=float(np.polyfit([r["gamma_in"] for r in ok], [r[v]["gamma_best"] for r in ok], 1)[0]),
                            edge_hits=int(edges), sigma_undefined=int((~fin).sum()), sigma_median=float(np.median(sig[fin])), pull_rms=float(np.sqrt(np.mean(pull ** 2))),
                            beside_lalpha_bias=float(np.median(dchi)), beside_lalpha_rms=float(np.sqrt(np.mean(dchi ** 2))))
        Q = R[f"K1_{v}"]
        O.append(f"K1 variant {v}: Gamma_b bias {Q['gamma_bias']:+.3f} (|.| <= 0.15), rms {Q['gamma_rms']:.3f} (<= 0.40); log alpha bias {Q['lalpha_bias']:+.4f} dex (|.| <= 0.03), "
                 f"rms {Q['lalpha_rms']:.4f} (<= 0.10): {'PASS' if Q['PASS'] else 'FAIL'}")
        O.append(f"   slope {Q['slope']:.3f}; edge hits {Q['edge_hits']}; sigma undefined {Q['sigma_undefined']}; median sigma(Gamma_b) {Q['sigma_median']:.3f}; pull rms {Q['pull_rms']:.2f}; "
                 f"beside (log alpha at chi2-weighted mean Gamma_b, ungraded): bias {Q['beside_lalpha_bias']:+.4f} rms {Q['beside_lalpha_rms']:.4f}")
        R[f"by_gamma_in_{v}"] = {}
        for gi in sorted(set(r["gamma_in"] for r in ok)):
            q = [r for r in ok if r["gamma_in"] == gi]; Lq = lines(np.array([r[v]["gamma_best"] - gi for r in q]), np.array([np.log10(r[v]["alpha"] / r["alpha_in"]) for r in q]))
            R[f"by_gamma_in_{v}"][f"{gi:.1f}"] = dict(n=len(q), **Lq)
            O.append(f"   Gamma_b_in {gi:.1f}: n {len(q)}, Gamma_b bias {Lq['gamma_bias']:+.3f} rms {Lq['gamma_rms']:.3f}; log alpha bias {Lq['lalpha_bias']:+.4f} rms {Lq['lalpha_rms']:.4f}")
        R[f"by_sn_third_{v}"] = {}
        for t in range(3):
            q = [r for r in ok if r["third"] == t]; Lq = lines(np.array([r[v]["gamma_best"] - r["gamma_in"] for r in q]), np.array([np.log10(r[v]["alpha"] / r["alpha_in"]) for r in q]))
            R[f"by_sn_third_{v}"][str(t + 1)] = dict(n=len(q), **Lq)
            O.append(f"   S/N third {t + 1}: n {len(q)}, Gamma_b bias {Lq['gamma_bias']:+.3f} rms {Lq['gamma_rms']:.3f}; log alpha bias {Lq['lalpha_bias']:+.4f} rms {Lq['lalpha_rms']:.4f}")
    k2 = [r for r in ok if "alpha_h4p" in r]
    b = float(np.median([(np.log10(r["alpha_h4p"]) - np.log10(r["alpha_h4m"])) / 0.06 for r in k2])) if k2 else float("nan"); lean = 0.69 * np.log(10) * abs(b) * iqr
    R["K2"] = dict(n=len(k2), b=b, iqr_h4=iqr, lean_ln=float(lean), PASS=bool(lean <= 0.01 and len(k2) == 100))
    O.append(f"K2 h4 leak: n {len(k2)}, b {b:+.4f} dex per unit h4; lean {lean:.4f} ln (IQR {iqr:.4f}; <= 0.01): {'PASS' if R['K2']['PASS'] else 'FAIL'}")
    print("\n".join(O), flush=True); open(os.path.join(HERE, "lam10_k.out"), "w", encoding="utf-8").write("\n".join(O) + "\n")
    json.dump(R, open(os.path.join(HERE, "lam10_k.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False); return R

if __name__ == "__main__":
    if "--summarize" in arg: summarize()
    else: run(int(opt("--shard", "0")), int(opt("--nshard", "1")))
