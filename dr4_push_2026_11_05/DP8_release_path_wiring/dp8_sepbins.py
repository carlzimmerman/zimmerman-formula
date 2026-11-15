#!/usr/bin/env python3
"""DP8: Amendment 14(c)'s separation-resolved statistic on a catalogue, report-only (criteria FROZEN_CRITERIA.md, 4caa8bc91f). NEW CODE.

Owner decision 2026-11-15b Q8: the statistic is run on release day after the label steps, report-only; it cannot change a
label; if this lane's DR3 code-path check fails the result declares it NOT RUN. Amendment 14(c) defines it "as coded in XR22's
`sepbins`" (real_research/cross_thread_review_2026_09_26/XR22_prereg_statistic.py, a function nested in that script's main(),
written for a simulated population with a Newtonian twin of every pair). On data there is no twin, so 14(c)'s own words are
used: in the projected-separation bins s_proj = [2, 3, 5, 7, 10, 15, 20, 30] kAU,
    r_b = median(vtilde, catalogue) / median(vtilde, the frozen Newtonian model population with the same cuts) - 1,
with its error from a bootstrap over catalogue pairs. Every other choice is XR22's: vtilde < VTCAP on each side, boot = 100,
numpy default_rng(5), the error = SD (ddof 1) of the bootstrap medians / the model median, the model population =
make_population(1,500,000, default_rng(20261216), dr4=True) (XR22's registered estimator), the model vtilde = XR22's vt1.
Catalogue vtilde comes from the frozen pipeline's own ingest_csv; s_proj from the catalogue's sep_kAU column. vtilde and s_proj
carry no a0, so the table is footing-free (one table, not a pooled one). The xi reading of 14(c) is not computed here.
  python3 -B dp8_sepbins.py --catalog CAT.csv --out-json J.json [--tag T]
  python3 -B dp8_sepbins.py --self-test --out-json J.json     (XR22's own sepbins, its source taken by ast and run unedited,
                                                               against this file's function on the model population, B = 1)
DP8_MUTATE=edges moves the 5 kAU edge to 6 kAU (the self-test must then fail).
The frozen pipeline is imported read-only; a socket guard forbids any network access. kappa = 1/2 FITTED; footings never
pooled; not theory closed. Nothing here says the data favour the framework. DR3 numbers are code-path tests, never results.
"""
import sys
sys.dont_write_bytecode = True
import argparse, ast, csv, hashlib, json, os, socket
import numpy as np


def _no_net(*a, **k):
    raise RuntimeError("network access forbidden (DP8 sepbins)")


socket.socket.connect = socket.socket.connect_ex = socket.create_connection = socket.getaddrinfo = _no_net
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "prep_2026", "gaia_dr4_prep"))
import wide_binary_pipeline as wbp  # noqa: E402  (read-only import)

XR22 = os.path.join(ROOT, "real_research", "cross_thread_review_2026_09_26", "XR22_prereg_statistic.py")
EDGES = [2.0, 3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0]
if os.environ.get("DP8_MUTATE") == "edges":
    EDGES = [2.0, 3.0, 6.0, 7.0, 10.0, 15.0, 20.0, 30.0]
NPOP, POPSEED, BOOT, BOOTSEED = 1_500_000, 20261216, 100, 5
HDR = "kappa = 1/2 FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework."


def model_population():
    pop = wbp.make_population(NPOP, np.random.default_rng(POPSEED), dr4=True)
    sk = pop["s_obs"] / wbp.KAU
    vt1 = np.hypot(pop["pmx"] + pop["npmx"], pop["pmy"] + pop["npmy"]) * 4.74e3 * (pop["d_obs"] / 1000.) / pop["vc_obs"]
    return pop, sk, vt1


def sepbins_data(s_data, vt_data, s_model, vt_model, edges=None, boot=BOOT, seed=BOOTSEED):
    """r_b per s_proj bin: median(catalogue vtilde) / median(model vtilde) - 1; bootstrap over catalogue pairs (XR22's recipe)"""
    edges = EDGES if edges is None else edges
    rr = np.random.default_rng(seed)
    rows = []
    for lo_, hi_ in zip(edges[:-1], edges[1:]):
        md = (s_data >= lo_) & (s_data < hi_) & (vt_data < wbp.VTCAP)
        mm = (s_model >= lo_) & (s_model < hi_) & (vt_model < wbp.VTCAP)
        v0, v1 = vt_model[mm], vt_data[md]
        idx = rr.integers(0, md.sum(), (boot, md.sum()))
        sb = np.median(v1[idx], axis=1)
        rows.append(dict(lo=lo_, hi=hi_, n=int(md.sum()), ratio=float(np.median(v1) / np.median(v0) - 1),
                         sig_med=float(sb.std(ddof=1) / np.median(v0)), frac=float(md.sum() / len(s_data)), n_model=int(mm.sum())))
    return rows


def xr22_sepbins_function(pop):
    """XR22's own `sepbins` (nested in its main()), compiled from its source unedited; its free names EST, PL, SEPBINS bound here"""
    src = open(XR22).read()
    tree = ast.parse(src)
    seps = [n for n in tree.body if isinstance(n, ast.Assign) and any(getattr(t, "id", None) == "SEPBINS" for t in n.targets)]
    sepbins_xr22 = ast.literal_eval(seps[0].value)
    main = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main"][0]
    fn = [n for n in ast.walk(main) if isinstance(n, ast.FunctionDef) and n.name == "sepbins"][0]
    mod = ast.Module(body=[fn], type_ignores=[])
    ns = {"np": np, "SEPBINS": sepbins_xr22, "PL": {"KAU": wbp.KAU, "VTCAP": wbp.VTCAP},
          "EST": {"canonical": type("E", (), {"pop": pop})()}}
    exec(compile(mod, XR22, "exec"), ns)
    return ns["sepbins"], sepbins_xr22, ast.get_source_segment(src, fn)


def read_catalogue(path):
    rows = list(csv.DictReader(open(path)))
    s = np.array([float(r["sep_kAU"]) for r in rows])
    gN, vt, _ = wbp.ingest_csv(path)
    return s, vt


def self_test(out_json):
    pop, sk, vt1 = model_population()
    fx, sep_x, src = xr22_sepbins_function(pop)
    rx = fx(np.ones(len(sk)), "canonical")
    rd = sepbins_data(sk, vt1, sk, vt1)
    keys = ("lo", "hi", "n", "ratio", "sig_med", "frac")
    same_rows = len(rx) == len(rd) and all(all(a[k] == b[k] for k in keys) for a, b in zip(rx, rd))
    same_edges = (list(map(float, sep_x)) == EDGES)
    # information only: a constant boost B = 1.21 (vtilde x 1.1), XR22's joint-mask twin vs the data-side separate masks
    g = 1.1
    vtg = np.hypot(g * pop["pmx"] + pop["npmx"], g * pop["pmy"] + pop["npmy"]) * 4.74e3 * (pop["d_obs"] / 1000.) / pop["vc_obs"]
    rx2, rd2 = fx(np.full(len(sk), g * g), "canonical"), sepbins_data(sk, vtg, sk, vt1)
    info = [dict(lo=a["lo"], xr22_ratio=a["ratio"], dp8_ratio=b["ratio"], diff=b["ratio"] - a["ratio"]) for a, b in zip(rx2, rd2)]
    ok = bool(same_rows and same_edges)
    out = dict(test="DP8 C5(i): XR22's own sepbins (unedited source) vs DP8's data-side function, model population as data, B = 1",
               mutate=os.environ.get("DP8_MUTATE"), edges_dp8=EDGES, edges_xr22=list(map(float, sep_x)), edges_equal=same_edges,
               rows_bit_identical=same_rows, rows_xr22=rx, rows_dp8=rd, n_population=int(len(sk)),
               xr22_source_sha256=hashlib.sha256(src.encode()).hexdigest(),
               information_B_1p21=info, passed=ok, note=HDR)
    json.dump(out, open(out_json, "w"), indent=1)
    print(f"DP8 sepbins self-test{' [MUTATE ' + os.environ['DP8_MUTATE'] + ']' if os.environ.get('DP8_MUTATE') else ''}: model population {len(sk):,d} pairs; "
          f"XR22 sepbins source sha256 {out['xr22_source_sha256'][:16]}")
    for a, b in zip(rx, rd):
        print(f"  bin {a['lo']:4.0f}-{a['hi']:4.0f} kAU  XR22 n {a['n']:7d} ratio {a['ratio']:+.6f} sig {a['sig_med']:.6f} | DP8 [{b['lo']:4.0f}-{b['hi']:4.0f}] "
              f"n {b['n']:7d} ratio {b['ratio']:+.6f} sig {b['sig_med']:.6f}  {'identical' if all(a[k] == b[k] for k in keys) else 'DIFFERENT'}")
    print("  information (B = 1.21, joint vs separate masks): max |ratio diff| %.2e" % max(abs(x["diff"]) for x in info))
    print(f"edges equal XR22's SEPBINS: {same_edges}; rows bit-identical: {same_rows}  ->  self-test {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def run(catalog, out_json, tag):
    s, vt = read_catalogue(catalog)
    pop, sk, vt1 = model_population()
    rows = sepbins_data(s, vt, sk, vt1)
    sha = hashlib.sha256(open(catalog, "rb").read()).hexdigest()
    finite = all(np.isfinite(r["ratio"]) and np.isfinite(r["sig_med"]) for r in rows)
    out = dict(statistic="Amendment 14(c) separation-resolved statistic (XR22 sepbins recipe, data side); REPORT-ONLY, cannot change a label "
                         "(OWNER_DECISION_2026-11-15b Q8); a measurement, not a verdict statistic; footing-free (vtilde and s_proj carry no a0)",
               tag=tag, catalogue=os.path.basename(catalog), catalogue_sha256=sha, n_catalogue=int(len(s)),
               model=dict(make_population=NPOP, seed=POPSEED, dr4=True, n_after_selection=int(len(sk))), edges_kAU=EDGES,
               vtcap=float(wbp.VTCAP), boot=BOOT, boot_seed=BOOTSEED, rows=rows, all_finite=bool(finite),
               xi_reading="not computed (Amendment 14(c)'s xi fit against XR22's committed r_b^chain(xi) is outside this step)", note=HDR)
    json.dump(out, open(out_json, "w"), indent=1)
    lines = [f"Amendment 14(c) separation-resolved statistic ({tag or 'untagged'}), report-only; catalogue {os.path.basename(catalog)} "
             f"({len(s):,d} pairs, sha256 {sha[:16]}); model population {len(sk):,d}; boot {BOOT}, seed {BOOTSEED}"]
    for r in rows:
        lines.append(f"  s_proj {r['lo']:4.0f}-{r['hi']:4.0f} kAU  n {r['n']:6d}  r_b {r['ratio']:+.4f} +- {r['sig_med']:.4f}")
    lines.append(HDR)
    open(os.path.splitext(out_json)[0] + ".out", "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0 if finite else 1


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog", default=None); ap.add_argument("--out-json", required=True); ap.add_argument("--tag", default="")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test(a.out_json)
    if not a.catalog:
        raise SystemExit("need --catalog (or --self-test)")
    return run(a.catalog, a.out_json, a.tag)


if __name__ == "__main__":
    sys.exit(main())
