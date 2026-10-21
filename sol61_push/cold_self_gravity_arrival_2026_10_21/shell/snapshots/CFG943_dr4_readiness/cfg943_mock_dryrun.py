#!/usr/bin/env python3
"""CFG943 task 3: MOCK dry run of the frozen Gaia DR4 wide-binary scoring (FROZEN_CRITERIA.md section 3).

  python3 -B cfg943_mock_dryrun.py --build-model   (first, separate process) master + model medians -> cfg943_model_medians.npz
  python3 -B cfg943_mock_dryrun.py            classes A0 A1 B1 B2 B3 C D at N_cat = 30,000, K = 100, both statistics
                                               -> cfg943_mock_dryrun.out / _results.json
  python3 -B cfg943_mock_dryrun.py --scan     R-only power scan, N_cat = 30k / 100k / 300k, classes A0 B1 B2 B3, K = 100
                                               -> cfg943_scan.out / _results.json
  python3 -B cfg943_mock_dryrun.py --mutate   MUTATE: planted x1.2 step at x > 1, N_cat = 300,000; must be R KILLED (exit 1 = bites)
                                               -> cfg943_mock_dryrun_MUTATE.out / _results.json
Every number is a MOCK; nothing is a measurement.  Frozen code is imported read-only; CFG825's once-only paths are never called.
kappa = 1/2 FITTED; footings never pooled.
"""
import sys
sys.dont_write_bytecode = True
import os, json, math, time, argparse
import numpy as np
import cfg943_common as C
from cfg943_common import W, R825, ARMC, A14

OUT = []
SMOKE = os.environ.get("CFG943_SMOKE") == "1"          # wiring test only: K = 2, small master, outputs to a scratch dir, never the lane files
OUTDIR = os.environ.get("CFG943_SMOKE_DIR", "/tmp") if SMOKE else C.HERE
KREP = 2 if SMOKE else 100
MODEL_NPZ = "cfg943_model_medians.npz"


def P(s=""):
    OUT.append(s); print(s, flush=True)


CLASSES = ["A0_NEWTON", "A1_NEWTON_CUTS", "B1_MOND_BENCH", "B2_MOND_STEP", "B3_ARM_A_FLOOR", "C_CFG740", "D_FALSIFIER_EDGE"]
REG_C, REG_14 = ARMC.registered(), A14.registered()
FLOOR = {"canonical": W.GAMMA_TARGET, "alt": W.GAMMA_TARGET_ALT}


def row_class(s):
    if "guard zone" in s: return "GUARD(>1.23,no verdict)"
    if "z_C >= 3" in s: return "FALSIFICATION_ROW"
    if "2 <= z_C < 3" in s: return "DISFAVOURED_2-3"
    if "|z_C| < 2" in s: return "CONSISTENT_ROW"
    if "-3 < z_C <= -2" in s: return "BELOW_2-3"
    if "z_C <= -3" in s: return "SUBNEWTON_ROW"
    return "?"


def gamma_fit(c, a0, mod, rng, sel=None):
    ly = np.log10(c["g_proj"] / a0); vt = c["vt"]
    if sel is not None:
        ly, vt = ly[sel], vt[sel]
    med, sig, cnt = W.bin_medians(ly, vt, boot=200, rng=rng)
    g, sg, chi2, nb, kap = W.fit_gamma(med, sig, mod, W.GRID)
    return float(g), float(sg), float(kap), int(nb)


def one_repeat(cls, ci, k, mods, B):
    rng = np.random.default_rng([943, ci, k])
    c = C.make_catalogue(30000, rng, cls)
    rec = dict(N=len(c["vt"]))
    for foot, a0 in (("canonical", W.A0_CAN), ("alt", W.A0_ALT)):
        g, sg, kap, nb = gamma_fit(c, a0, mods[foot], rng)
        skau = c["s_obs"] / W.KAU
        g2, sg2, kap2, _ = gamma_fit(c, a0, mods[foot], rng, sel=(skau > 3) & (skau < 20))
        log = C.fit_line(foot, g, sg)
        rowtxt = [r for r in ARMC.report(log, REG_C) if r.startswith("[ArmC] c") or r.startswith("[ArmC] a")][0]
        a14 = [r for r in A14.report(A14.parse(log), REG_14) if r.startswith("[A14] c") or r.startswith("[A14] a")][0]
        st = math.hypot(round(sg, 4), REG_C["s_sys"]); zc = (round(g, 4) - 1.0) / st
        assert f"z_C = (gamma_hat - 1.000)/sigma_tot = {zc:+.2f}" in rowtxt, (rowtxt, zc)      # tool and arithmetic agree
        zA = (round(g, 4) - FLOOR[foot]) / st
        rec[foot] = dict(g=g, sg=sg, kappa=kap, bins=nb, g_sep=g2, sg_sep=sg2, sigma_tot=st, z_C=zc,
                         row=row_class(rowtxt), a14=a14.split("interval: ")[1].split("  [")[0],
                         armA_falsified_z=(zA < -3), armA_below_1056=(g < W.GAMMA_A_FALSIFIED_BELOW),
                         kappa_in=(W.KAPPA_WINDOW[0] <= kap <= W.KAPPA_WINDOW[1]),
                         sep_rung_ok=(abs(g2 - g) < sg))
        rec[foot]["stab_eval_ok"] = rec[foot]["kappa_in"] and rec[foot]["sep_rung_ok"]
    t = C.pair_table(c)
    res, final, txt = C.r_score(t, rng, B, f"MOCK {cls} rep {k}", quiet=(k != 0))
    p = res["primary"]
    rec["R"] = dict(label=final, ok=p["ok"], R=p.get("R"), sigma_R=p.get("sigma_R"), sigma_boot=p.get("sigma_boot"),
                    sigma_tot=p.get("sigma_tot"), N=p.get("N"), n_num=p.get("n_num"), n_den=p.get("n_den"),
                    f_tail=(p.get("f_tail_num"), p.get("f_tail_den")), f_tail_events=p.get("f_tail_events"),
                    f_tail_diff_sigma=p.get("f_tail_diff_sigma"), cls_primary=p.get("cls"),
                    fp_a0_can=res["a0=9.36e-11"].get("R"), fp_a0_alt=res["a0=1.13e-10"].get("R"))
    return rec, (txt if k == 0 else "")


def summarize(cls, recs):
    K = len(recs); s = dict(K=K)
    lab = [r["R"]["label"] for r in recs]
    s["R_label_rates"] = {L: lab.count(L) / K for L in sorted(set(lab))}
    Rv = np.array([r["R"]["R"] for r in recs if r["R"]["ok"]])
    s["R_mean"], s["R_rms"] = float(Rv.mean()), float(Rv.std(ddof=1))
    s["sigma_R_mean"] = float(np.mean([r["R"]["sigma_R"] for r in recs]))
    s["sigma_boot_mean"] = float(np.mean([r["R"]["sigma_boot"] for r in recs]))
    s["N_R_mean"] = float(np.mean([r["R"]["N"] for r in recs]))
    s["n_num_mean"] = float(np.mean([r["R"]["n_num"] for r in recs])); s["n_den_mean"] = float(np.mean([r["R"]["n_den"] for r in recs]))
    s["kill_threshold_R_mean"] = float(np.mean([1 + max(0.01, 3 * r["R"]["sigma_R"]) for r in recs]))
    s["R_primary_cls_KILLED_rate"] = float(np.mean([r["R"]["cls_primary"] == "KILLED" for r in recs]))
    s["R_contam_limited_rate"] = float(np.mean([str(r["R"]["label"]).startswith("CONTAMINATION") for r in recs]))
    s["R_footing_branch_mean"] = dict(can=float(np.nanmean([r["R"]["fp_a0_can"] for r in recs])), alt=float(np.nanmean([r["R"]["fp_a0_alt"] for r in recs])))
    for foot in ("canonical", "alt"):
        g = np.array([r[foot]["g"] for r in recs]); sg = np.array([r[foot]["sg"] for r in recs])
        rows = [r[foot]["row"] for r in recs]
        fals = np.array([r[foot]["row"] == "FALSIFICATION_ROW" for r in recs])
        stab = np.array([r[foot]["stab_eval_ok"] for r in recs])
        s[foot] = dict(g_mean=float(g.mean()), g_rms=float(g.std(ddof=1)), sg_mean=float(sg.mean()),
                       kappa_mean=float(np.mean([r[foot]["kappa"] for r in recs])),
                       kappa_in_rate=float(np.mean([r[foot]["kappa_in"] for r in recs])),
                       sep_rung_ok_rate=float(np.mean([r[foot]["sep_rung_ok"] for r in recs])),
                       row_rates={x: rows.count(x) / K for x in sorted(set(rows))},
                       falsification_row_rate=float(fals.mean()),
                       falsification_row_with_eval_stability_rate=float((fals & stab).mean()),
                       armA_falsified_rate=float(np.mean([r[foot]["armA_falsified_z"] for r in recs])),
                       armA_below_1056_rate=float(np.mean([r[foot]["armA_below_1056"] for r in recs])),
                       a14_rates={x: [r[foot]["a14"] for r in recs].count(x) / K for x in sorted(set(r[foot]["a14"] for r in recs))},
                       grid_edge_rate=float(np.mean((np.abs(g - 0.90) < 1e-9) | (np.abs(g - 1.50) < 1e-9))))
    R_kill = np.array([r["R"]["label"] == "KILLED" for r in recs])
    g_kill = np.array([(r["canonical"]["row"] == "FALSIFICATION_ROW") and r["canonical"]["stab_eval_ok"] for r in recs])
    s["kill_R_rate"] = float(R_kill.mean()); s["kill_gamma_canonical_rate"] = float(g_kill.mean())
    s["kill_any_route_rate"] = float((R_kill | g_kill).mean())
    survive = np.array([(r["R"]["label"] not in ("KILLED",) and not str(r["R"]["label"]).startswith("CONTAMINATION"))
                        and r["canonical"]["row"] == "CONSISTENT_ROW" and r["alt"]["row"] == "CONSISTENT_ROW" for r in recs])
    s["framework_consistent_rate"] = float(survive.mean())
    return s


def verdict(cls, s):
    if cls in ("A0_NEWTON", "A1_NEWTON_CUTS", "C_CFG740"):
        ok = s["framework_consistent_rate"] >= 0.95 and s["kill_R_rate"] <= 0.01
        return "PASS (framework consistent)" if ok else "FAIL"
    if cls.startswith("B"):
        return "KILL TRIGGERS" if s["kill_any_route_rate"] >= 0.95 else "POWER GAP"
    return "information"


def main_classes():
    C.start_watchdog()
    h0 = C.frozen_hashes()
    P("CFG943 MOCK dry run (every number below is a MOCK, never a result). kappa = 1/2 FITTED; footings never pooled.")
    P(f"frozen files hashed before: {len(h0) - 1}; CFG825 DR4 once-only slot exists: {h0['DR4_SLOT_EXISTS']}")
    t0 = time.time()
    mp = os.path.join(OUTDIR, MODEL_NPZ)
    z = np.load(mp)
    mods = {"canonical": (z["can_med"], z["can_sig"]), "alt": (z["alt_med"], z["alt_sig"])}
    assert np.array_equal(z["grid"], W.GRID)
    import hashlib
    msha = hashlib.sha256(open(mp, "rb").read()).hexdigest()
    P(f"model medians loaded from {MODEL_NPZ} (built by --build-model in a separate process: frozen make_population master of {int(z['nm']):,} pairs, "
      f"{int(z['n_sel']):,} after selection, seed 20261216; sha256 {msha[:16]})")
    # K1 replica identity (and K1b: the boost path equals the frozen vtilde_of)
    a = W.make_population(50000, np.random.default_rng(12345), dr4=True)
    b, ex = C.mock_population(50000, np.random.default_rng(12345), dr4=True)
    k1 = set(a) == set(b) and all(np.array_equal(a[k], b[k]) for k in a)
    cb = dict(b); cb.update(ex)
    vt_mine, _ = C.velocities(cb, C.BOOSTS["B1_MOND_BENCH"](cb))
    k1b = np.array_equal(vt_mine, W.vtilde_of(a, W.GAMMA_MOND, W.A0_CAN))
    P(f"K1 replica == frozen make_population (all {len(a)} fields, byte-identical): {'PASS' if k1 else 'FAIL'}; "
      f"K1b class-boost path == frozen vtilde_of(1.33, canonical): {'PASS' if k1b else 'FAIL'}")
    # K6: the memory-lean model medians against the frozen model_medians on a small master
    sm = W.make_population(200000, np.random.default_rng(777), dr4=True)
    fz_med, fz_sig = W.model_medians(sm, W.A0_CAN, W.GRID, np.random.default_rng(1))
    ln_med, ln_sig = C.lean_model_medians(sm, W.A0_CAN, W.GRID, np.random.default_rng(2))
    okb = np.isfinite(fz_sig) & np.isfinite(ln_sig)
    ratio = ln_sig[okb] / fz_sig[okb]
    k6 = bool(np.array_equal(fz_med, ln_med, equal_nan=True) and np.array_equal(np.isfinite(fz_sig), np.isfinite(ln_sig)) and np.all((ratio > 0.7) & (ratio < 1.43)))
    del sm
    P(f"K6 lean model medians: grid medians identical to the frozen model_medians: {np.array_equal(fz_med, ln_med, equal_nan=True)}; "
      f"bootstrap sigma ratio lean/frozen per bin {np.round(ratio, 2).tolist()} (100-resample estimates, expected within ~0.7-1.4) -> {'PASS' if k6 else 'FAIL'}")
    k3, d3 = R825.control_C3()
    P(f"K3 CFG825 class arithmetic (its C3) via import: {'PASS' if k3 else 'FAIL'}  kill thresholds {d3['kill_threshold_R']}")
    allres = dict(lane="CFG943", mode="classes", N_cat=30000, K=KREP, smoke=SMOKE, controls=dict(K1=k1, K1b=k1b, K3=k3, K6=k6), model_npz_sha256=msha, classes={})
    for ci, cls in enumerate(CLASSES):
        recs = []
        for k in range(KREP):
            rec, txt = one_repeat(cls, ci, k, mods, 2000 if k == 0 else 300)
            if txt:
                P(f"--- showcase {cls} repeat 0 (B = 2000), CFG825 score() block verbatim:")
                for line in txt.rstrip().splitlines():
                    P("    " + line)
                P(f"    gamma-hat repeat 0: canonical {rec['canonical']['g']:.4f} +- {rec['canonical']['sg']:.4f} kappa {rec['canonical']['kappa']:.4f} row {rec['canonical']['row']}; "
                  f"alt {rec['alt']['g']:.4f} +- {rec['alt']['sg']:.4f} row {rec['alt']['row']}")
            recs.append(rec)
            C.guard(cls)
        s = summarize(cls, recs); s["verdict"] = verdict(cls, s)
        allres["classes"][cls] = dict(summary=s, repeats=recs)
        P(f"=== {cls}: VERDICT {s['verdict']}  ({time.time() - t0:.0f} s, peak RSS {C.rss_mb():.0f} MB)")
        P(f"    R: mean {s['R_mean']:.4f} rms {s['R_rms']:.4f}; sigma_R {s['sigma_R_mean']:.4f} (boot {s['sigma_boot_mean']:.4f}); "
          f"N_R {s['N_R_mean']:.0f} (num {s['n_num_mean']:.0f} / den {s['n_den_mean']:.0f}); kill needs R >= {s['kill_threshold_R_mean']:.3f}; "
          f"labels {s['R_label_rates']}; primary-class KILLED {s['R_primary_cls_KILLED_rate']:.2f}, relabelled CONTAMINATION-LIMITED {s['R_contam_limited_rate']:.2f}; "
          f"footing branches R {s['R_footing_branch_mean']['can']:.4f} (9.36e-11) / {s['R_footing_branch_mean']['alt']:.4f} (1.13e-10)")
        for foot in ("canonical", "alt"):
            f = s[foot]
            P(f"    gamma-hat {foot}: mean {f['g_mean']:.4f} rms {f['g_rms']:.4f} sigma_fit {f['sg_mean']:.4f}; kappa {f['kappa_mean']:.4f} (in window {f['kappa_in_rate']:.2f}); "
              f"sep rung ok {f['sep_rung_ok_rate']:.2f}; Arm C rows {f['row_rates']}; falsification row {f['falsification_row_rate']:.2f} "
              f"(with evaluable stability {f['falsification_row_with_eval_stability_rate']:.2f}); Arm A falsified (z < -3 vs floor {FLOOR[foot]}) {f['armA_falsified_rate']:.2f}; "
              f"A14 intervals {f['a14_rates']}; grid-edge fits {f['grid_edge_rate']:.2f}")
        P(f"    kill rates: R KILLED {s['kill_R_rate']:.2f}; gamma-hat Arm C/settling falsification (canonical, evaluable stability) {s['kill_gamma_canonical_rate']:.2f}; "
          f"any route {s['kill_any_route_rate']:.2f}; framework-consistent rate {s['framework_consistent_rate']:.2f}")
    a0, a1 = allres["classes"]["A0_NEWTON"]["summary"], allres["classes"]["A1_NEWTON_CUTS"]["summary"]
    dg = a1["canonical"]["g_mean"] - a0["canonical"]["g_mean"]; dR = a1["R_mean"] - a0["R_mean"]
    asym_ok = abs(dg) < 0.5 * a0["canonical"]["sg_mean"] and abs(dR) < 0.5 * a0["sigma_R_mean"]
    allres["A1_vs_A0"] = dict(d_gamma_canonical=dg, d_gamma_alt=a1["alt"]["g_mean"] - a0["alt"]["g_mean"], d_R=dR, pass_=asym_ok)
    P(f"A1 vs A0 (catalogue cuts 4+15 the forward model lacks): d gamma-hat canonical {dg:+.4f} (0.5 sigma_fit = {0.5 * a0['canonical']['sg_mean']:.4f}), "
      f"alt {allres['A1_vs_A0']['d_gamma_alt']:+.4f}; d R {dR:+.4f} (0.5 sigma_R = {0.5 * a0['sigma_R_mean']:.4f}) -> {'PASS' if asym_ok else 'FLAG: data/model selection asymmetry'}")
    h1 = C.frozen_hashes()
    k4 = h0 == h1 and not h1["DR4_SLOT_EXISTS"]
    allres["controls"]["K4_frozen_unchanged_and_dr4_slot_absent"] = k4
    allres["controls"]["K5_peak_rss_MB"] = C.rss_mb()
    P(f"K4 frozen files unchanged and CFG825 DR4 slot absent: {'PASS' if k4 else 'FAIL'}; K5 peak RSS {C.rss_mb():.0f} MB (< 900)")
    json.dump(allres, open(os.path.join(OUTDIR, "cfg943_mock_dryrun_results.json"), "w"), indent=1, default=float)
    open(os.path.join(OUTDIR, "cfg943_mock_dryrun.out"), "w").write("\n".join(OUT) + "\n")
    return 0 if (k1 and k1b and k3 and k4 and k6) else 2


def scan_worker(cls, n, k0, k1):
    """One block of repeats in its own process (heap fragmentation grows RSS over many repeats); one JSON line per repeat."""
    C.start_watchdog()
    ci = 100 + CLASSES.index(cls) if cls in CLASSES else 199
    for k in range(k0, k1):
        rng = np.random.default_rng([943, ci, n, k])
        c = C.make_catalogue(n, rng, cls, chunk=C.CHUNK if n <= 30000 else 50_000)    # smaller generator chunks above 30k (memory)
        res, final, _ = C.r_score(C.pair_table(c), rng, 300, f"{cls} {n} {k}")
        p = res["primary"]
        print(json.dumps(dict(k=k, label=final, R=p["R"], sigma_R=p["sigma_R"], N=p["N"], n_num=p["n_num"], n_den=p["n_den"])), flush=True)
        del c, res
        C.guard(cls)
    print(json.dumps(dict(peak_rss_MB=C.rss_mb())), flush=True)
    return 0


def main_scan(mutate=False):
    """Sequential driver: each block of repeats runs in a fresh worker process (one at a time); this process only aggregates."""
    import subprocess
    h0 = C.frozen_hashes()
    out = dict(lane="CFG943", mode="MUTATE" if mutate else "scan", rows=[])
    plan = [("MUTATE_STEP_1p2", 300000, 20)] if mutate else [(cls, n, 100) for n in (30000, 100000, 300000)
                                                              for cls in ("A0_NEWTON", "B1_MOND_BENCH", "B2_MOND_STEP", "B3_ARM_A_FLOOR")]
    if SMOKE:
        plan = [(c_, n_, 2) for c_, n_, _ in plan]
    P(f"CFG943 {'MUTATE (planted x1.2 step at x > 1; must be R KILLED)' if mutate else 'R-only power scan'} -- MOCK numbers only")
    t0 = time.time(); worker_peak = 0.0
    env = dict(os.environ, OMP_NUM_THREADS="1")
    for cls, n, K in plan:
        bs = 25 if n <= 30000 else 10 if n <= 100000 else 3
        recs = []
        for k0 in range(0, K, bs):
            r = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "--scan-worker", cls, str(n), str(k0), str(min(K, k0 + bs))],
                               capture_output=True, text=True, env=env)
            if r.returncode != 0:
                P(f"  WORKER FAILED ({cls} {n} {k0}): rc {r.returncode}; {r.stderr.strip()[-300:]}")
                json.dump(out, open(os.path.join(OUTDIR, ("cfg943_mock_dryrun_MUTATE" if mutate else "cfg943_scan") + "_FAILED.json"), "w"), indent=1, default=float)
                return 3
            for line in r.stdout.splitlines():
                d = json.loads(line)
                if "peak_rss_MB" in d:
                    worker_peak = max(worker_peak, d["peak_rss_MB"])
                else:
                    recs.append(d)
        labs = [d["label"] for d in recs]; sR = [d["sigma_R"] for d in recs]
        row = dict(cls=cls, N_cat=n, K=K, R_mean=float(np.mean([d["R"] for d in recs])), R_rms=float(np.std([d["R"] for d in recs], ddof=1)),
                   sigma_R_mean=float(np.mean(sR)), N_R_mean=float(np.mean([d["N"] for d in recs])),
                   n_num_mean=float(np.mean([d["n_num"] for d in recs])), n_den_mean=float(np.mean([d["n_den"] for d in recs])),
                   kill_threshold_R=float(1 + max(0.01, 3 * np.mean(sR))),
                   label_rates={L: labs.count(L) / K for L in sorted(set(labs))}, KILLED_rate=labs.count("KILLED") / K, repeats=recs)
        out["rows"].append(row)
        P(f"  {cls:16s} N_cat {n:6d}: N_R {row['N_R_mean']:.0f} (num {row['n_num_mean']:.0f} / den {row['n_den_mean']:.0f}); R {row['R_mean']:.4f} rms {row['R_rms']:.4f}; "
          f"sigma_R {row['sigma_R_mean']:.4f} -> kill needs R >= {row['kill_threshold_R']:.3f}; labels {row['label_rates']}  ({time.time() - t0:.0f} s, worker peak RSS {worker_peak:.0f} MB)")
    h1 = C.frozen_hashes()
    k4 = h0 == h1 and not h1["DR4_SLOT_EXISTS"]
    out["K4"] = k4; out["worker_peak_rss_MB"] = worker_peak
    P(f"K4 frozen files unchanged and CFG825 DR4 slot absent: {'PASS' if k4 else 'FAIL'}; worker peak RSS {worker_peak:.0f} MB")
    stem = "cfg943_mock_dryrun_MUTATE" if mutate else "cfg943_scan"
    rc = 0
    if mutate:
        r = out["rows"][0]; bites = r["KILLED_rate"] >= 0.95
        out["bites"] = bites
        P(f"MUTATE: KILLED in {r['KILLED_rate']:.2f} of {r['K']} repeats -> {'BITES (the kill path works on mocks)' if bites else 'DOES NOT BITE: dry run NOT DIAGNOSTIC'}")
        rc = 1 if bites else 0
    json.dump(out, open(os.path.join(OUTDIR, f"{stem}_results.json"), "w"), indent=1, default=float)
    open(os.path.join(OUTDIR, f"{stem}.out"), "w").write("\n".join(OUT) + "\n")
    return rc if k4 else 2

def main_build_model():
    """Separate process (memory): the frozen make_population master (3,000,000 pairs, chunks of 125,000, seed 20261216) and the
    lean model medians on both footings, saved to cfg943_model_medians.npz (small)."""
    C.start_watchdog()
    t0 = time.time()
    NM = 250_000 if SMOKE else 3_000_000
    keys = ("pmx", "pmy", "npmx", "npmy", "d_obs", "g_true", "g_proj", "vc_obs")      # what vtilde_of / model medians read
    master = C.chunked_frozen_population(NM, np.random.default_rng(20261216), keys=keys, dr4=True)
    nsel = len(master["g_proj"])
    P(f"master (frozen make_population, {NM:,} pairs in chunks of {C.CHUNK_MASTER:,}, seed 20261216): {nsel} pairs after selection; peak RSS {C.rss_mb():.0f} MB")
    mrng = np.random.default_rng(20261216 + 1)
    cm, cs = C.lean_model_medians(master, W.A0_CAN, W.GRID, mrng)
    am, as_ = C.lean_model_medians(master, W.A0_ALT, W.GRID, mrng)
    np.savez(os.path.join(OUTDIR, MODEL_NPZ), can_med=cm, can_sig=cs, alt_med=am, alt_sig=as_, grid=W.GRID, nm=NM, n_sel=nsel)
    P(f"model medians built and saved ({time.time() - t0:.0f} s); peak RSS {C.rss_mb():.0f} MB; model sigma canonical {np.round(cs, 4).tolist()}")
    open(os.path.join(OUTDIR, "cfg943_build_model.out"), "w").write("\n".join(OUT) + "\n")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--scan", action="store_true"); ap.add_argument("--mutate", action="store_true"); ap.add_argument("--build-model", action="store_true"); ap.add_argument("--scan-worker", nargs=4)
    a = ap.parse_args()
    sys.exit(scan_worker(a.scan_worker[0], int(a.scan_worker[1]), int(a.scan_worker[2]), int(a.scan_worker[3])) if a.scan_worker else main_build_model() if a.build_model else main_scan(mutate=True) if a.mutate else main_scan() if a.scan else main_classes())
