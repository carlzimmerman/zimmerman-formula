#!/usr/bin/env python3
"""DP1: the NSS-off robustness rung (OWNER_DECISION_2026-11-05b D7 N4.1), NEW CODE ONLY; nothing frozen is edited.

The rung is `build(drop_nss=True, smax_kau=30)`: the registered stage G with the "NSS screen" line removed from the frozen
builder's own frozen_cuts source text (build_variant_catalogue.patched_frozen_cuts, imported read-only) and every other cut,
seed and cache as registered. This wrapper is the same swap as build_variant_catalogue.build, but it passes through the
driver's full option set (cones kinds for cut 13, neighbour tables, seed offset, stage dir), so the rung can be run with the
same cut-13 mode as the DR4 primary build (D7 N9: --cut13 cones-literal).

  python3 -B nss_off_rung.py --self-test                                  (DR3, offline, a few builds)
  python3 -B nss_off_rung.py --dr3-check [--mutate]                       (the FROZEN_CRITERIA.md reproduction run; writes dr3_check[_MUTATE].*)
  python3 -B nss_off_rung.py --release dr3 --cut13 extract-builder --out-csv RUNG.csv [--fit --baseline-csv BASE.csv]
  DR4 (UNTESTED, DR4 does not exist yet): the driver's own options pass through, e.g.
  python3 -B nss_off_rung.py --release dr4 --manifest M.json --cut13 cones-literal --neighbours-manifest NM.json --allow-network \
          --out-csv nss_off_rung_dr4.csv --fit --baseline-csv <primary build csv>

--fit fits the rung CSV by the registered path (wide_binary_pipeline.py --catalog CSV --seed 20261216, via seed_sweep's
fit_via_pipeline_cli); with --baseline-csv the baseline is fitted the same way and the shift, shift / sigma_fit and the
D7 N4.2 reading (|shift| < 1 sigma_fit passes) are reported. --keep-nss is the MUTATE switch (drop_nss=False).
DR3 numbers are code-path tests, never results (Amendment 7(e)). kappa = 1/2 FITTED; not theory closed.
"""
import sys
sys.dont_write_bytecode = True
import argparse, csv, hashlib, io, json, math, os, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PREP = REPO / "prep_2026" / "gaia_dr4_prep"
CFG816 = REPO / "campaign_fresh_gravity" / "CFG816_dr4_r_statistic_scoring"
D2DIR = REPO / "doors_push_2026_10_22" / "D2_wide_binary_fork"
sys.path.insert(0, str(PREP / "dr4_ready_1"))
sys.path.insert(0, str(CFG816))
sys.path.insert(0, str(PREP))
import dry_run_driver as D                      # read-only
import build_variant_catalogue as BV            # read-only (imports the same dry_run_driver module object)
import seed_sweep as SS                         # read-only (fit_via_pipeline_cli: the registered fit path)
import wide_binary_pipeline as wbp              # read-only (functions only; its main() is not run)

PIPE_SHA = "7c884e0e0a4cb9cb5d6280d558cf64c829974ed14143a90261bd6a6fbf3007c9"
VARIANT_SHA = "80c1292457b50104d3408d672eb45f4fbe48e6774ee0a3e8601c2a3ad5050612"
DR3 = REPO / "real_research" / "data" / "widebinaries" / "dr3_extract"
FIT_SEED = 20261216
SIGMA_G = {"canonical": 0.0249, "alt": 0.0211}                     # Q-G50 (seed_sweep_g50_summary.out), frozen in FROZEN_CRITERIA.md
T_ONE = {f: 2 * math.sqrt(2) * s for f, s in SIGMA_G.items()}     # 0.0704 / 0.0597
K_ENS = 8
E_ENS = {f: 2 * math.sqrt(2) * s / math.sqrt(K_ENS) for f, s in SIGMA_G.items()}   # = sigma_G
FOOTS = ("canonical", "alt")
A0 = {"canonical": wbp.A0_CAN, "alt": wbp.A0_ALT}


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def frozen_shas():
    return {p.name: sha256(p.read_bytes()) for p in (PREP / "wide_binary_pipeline.py", PREP / "catalog_builder" / "build_catalog.py",
                                                     PREP / "dr4_ready_1" / "dry_run_driver.py", CFG816 / "build_variant_catalogue.py",
                                                     PREP / "dr4_ready_1" / "seed_sweep.py")}


# ------------------------------------------------------------------ the rung build
def rung_build(drop_nss=True, smax_kau=30, release="dr3", variant="primary", cut13="extract-builder", manifest=None, allow_network=False,
               seed_offset=0, stage_dir=None, cones=None, missing_cones="error", corr_transport="async"):
    """build(drop_nss, smax_kau) with the driver's full option set; the registered frozen_cuts is swapped back in afterwards."""
    orig = D.B.frozen_cuts
    try:
        D.B.frozen_cuts = BV.patched_frozen_cuts(orig, drop_nss, smax_kau)
        csv_bytes, report = D.run(release, variant, cut13, manifest, allow_network, seed_offset=seed_offset, stage_dir=stage_dir, cones=cones,
                                  missing_cones=missing_cones, corr_transport=corr_transport)
    finally:
        D.B.frozen_cuts = orig
    report["variant_switches"] = dict(drop_nss_cut=bool(drop_nss), smax_kAU=int(smax_kau))
    report["rung"] = "NSS-off rung (D7 N4.1)" if (drop_nss and int(smax_kau) == 30) else "NOT the rung (switches differ)"
    return csv_bytes, report


def rows_of(csv_bytes_or_path):
    txt = Path(csv_bytes_or_path).read_text() if not isinstance(csv_bytes_or_path, (bytes, bytearray)) else csv_bytes_or_path.decode()
    return list(csv.DictReader(io.StringIO(txt)))


def rows_to_bytes(rows):
    buf = io.StringIO(newline="")
    w = csv.writer(buf)
    cols = list(rows[0])
    w.writerow(cols)
    for r in rows:
        w.writerow([r[c] for c in cols])
    return buf.getvalue().encode()


def key(r):
    return tuple(sorted((int(r["source_id1"]), int(r["source_id2"]))))


def nss_lookup():
    z = np.load(DR3 / "stage_A.npz")
    sid = z["source_id"]; o = np.argsort(sid, kind="stable"); ss = sid[o]; flag = z["non_single_star"][o] != 0

    def has(pair):
        i = np.searchsorted(ss, np.array(pair))
        return bool(flag[i].any())
    return has


# ------------------------------------------------------------------ the D2 estimator (re-implemented exactly)
def arrays(rows):
    s = np.array([float(r["sep_kAU"]) for r in rows]) * wbp.KAU
    vp = np.array([float(r["v_perp_kms"]) for r in rows]) * 1e3
    Mt = np.array([float(r["M1_msun"]) + float(r["M2_msun"]) for r in rows])
    gN = wbp.G * Mt * wbp.MSUN / s ** 2
    vt = vp / np.sqrt(wbp.G * Mt * wbp.MSUN / s)
    return gN, vt


class D2Estimator:
    """d2_sigma_sys_defs.py's fit: rng(20261216) -> make_population(1e6, dr4=True) -> model medians canonical, alt -> fits in order."""
    def __init__(self):
        rng = np.random.default_rng(20261216)
        pop = wbp.make_population(1_000_000, rng, dr4=True)
        self.MOD = {"canonical": wbp.model_medians(pop, wbp.A0_CAN, wbp.GRID, rng), "alt": wbp.model_medians(pop, wbp.A0_ALT, wbp.GRID, rng)}
        self.state = rng.bit_generator.state
        del pop

    def fit(self, rows, fo, rng):
        gN, vt = arrays(rows)
        med, sig, cnt = wbp.bin_medians(np.log10(gN / A0[fo]), vt, boot=200, rng=rng)
        g, sg, chi2, nb, kap = wbp.fit_gamma(med, sig, self.MOD[fo], wbp.GRID)
        return dict(N=len(rows), gamma=float(g), sigma_fit=float(sg), kappa=float(kap))

    def sequence(self, var_rows):
        """D2's loop: one rng, continued from after the model medians, canonical over all variants then alt."""
        rng = np.random.default_rng(); rng.bit_generator.state = self.state
        return {f"{fo}|{name}": self.fit(rows, fo, rng) for fo in FOOTS for name, rows in var_rows.items()}

    def fit_fresh(self, rows, fo):
        return self.fit(rows, fo, np.random.default_rng(FIT_SEED))


def d2_inputs(v3_rows):
    base = rows_of(DR3 / "wide_binaries_dr3.csv")
    return {"V0 baseline (frozen-cut build)": base,
            "V1 ladder: R_chance < 0.001": [r for r in base if float(r["R_chance"]) < 0.001],
            "V2 ladder: sep 3-20 kAU": [r for r in base if 3.0 <= float(r["sep_kAU"]) < 20.0],
            "V3 NSS-off probe (s < 30 kAU)": [r for r in v3_rows if float(r["sep_kAU"]) < 30.0],
            "V4 build: El-Badry R": rows_of(DR3 / "wide_binaries_dr3_elbadryR.csv"),
            "V5 build: scaled_clean": rows_of(DR3 / "wide_binaries_dr3_scaled_clean.csv")}


V0, V3 = "V0 baseline (frozen-cut build)", "V3 NSS-off probe (s < 30 kAU)"


# ------------------------------------------------------------------ helpers shared by the CLI
def n42_reading(shift, sigma_fit):
    """D7 N4.2: a shift smaller than 1 sigma_fit counts as passing the NSS-off condition."""
    return "passes NSS-off condition (|shift| < 1 sigma_fit)" if abs(shift) < sigma_fit else "shift >= 1 sigma_fit (ladder rule applies as written)"


def pair_compare(rung_rows, probe_rows, has_nss):
    R = {key(r) for r in rung_rows}; Pp = {key(r) for r in probe_rows}
    fR = {p for p in R if has_nss(p)}; fP = {p for p in Pp if has_nss(p)}
    oR, oP = R - fR, Pp - fP
    jac = len(fR & fP) / max(1, len(fR | fP))
    return dict(n_rung=len(R), n_probe=len(Pp), nss_rung=len(fR), nss_probe=len(fP), nss_jaccard=jac,
                other_probe_absent_from_rung=len(oP - oR) / max(1, len(oP)), other_rung_absent_from_probe=len(oR - oP) / max(1, len(oR)))


# ------------------------------------------------------------------ self-test (fast unit checks)
def self_test():
    D.init(False)
    res, ok = {}, True

    def T(name, cond, detail=""):
        nonlocal ok
        ok &= bool(cond); print(f"  [{'PASS' if cond else 'FAIL'}] {name}  {detail}", flush=True); res[name] = bool(cond)
    sh0 = frozen_shas()
    b0, r0 = rung_build(False, 30)
    T("S1 switches off = registered DR3 catalogue (REF_SHA_DR3)", r0["sha256"].startswith(D.REF_SHA_DR3), r0["sha256"][:16])
    b1, r1 = rung_build(True, 30)
    bv, _ = BV.build(True, 30)
    T("S2 rung bytes = build_variant_catalogue.build(True, 30) bytes", b1 == bv, f"{r1['n_pairs']} pairs, {r1['sha256'][:16]}")
    rows = rows_of(b1); has = nss_lookup()
    T("S3 rung: every s in (2, 30) kAU and >= 20 NSS-flagged pairs", all(2 < float(r["sep_kAU"]) < 30 for r in rows) and sum(has(key(r)) for r in rows) >= 20,
      f"NSS-flagged {sum(has(key(r)) for r in rows)}")
    T("S4 registered frozen_cuts restored after the build", D.B.frozen_cuts.__code__.co_filename.endswith("build_catalog.py"))
    try:
        BV.patched_frozen_cuts(lambda: None, True, 30); refused = False
    except Exception:
        refused = True
    T("S5 patching a function without the registered NSS line is refused", refused)
    T("S6 N4.2 reading: 0.05 < 0.055 passes, 0.06 does not", n42_reading(0.05, 0.055).startswith("passes") and not n42_reading(0.06, 0.055).startswith("passes"))
    T("S7 frozen files unchanged", frozen_shas() == sh0 and sh0["wide_binary_pipeline.py"] == PIPE_SHA)
    print("SELF-TEST", "PASSED" if ok else "FAILED")
    (HERE / "nss_off_rung_selftest.json").write_text(json.dumps(res, indent=1) + "\n")
    return 0 if ok else 1


# ------------------------------------------------------------------ the frozen DR3 check
def dr3_check(mutate):
    D.init(False)
    tag = "_MUTATE" if mutate else ""
    drop = not mutate
    lines, checks = [], {}

    def P(s=""):
        print(s, flush=True); lines.append(s)

    def C(cid, cond, detail):
        checks[cid] = dict(passed=bool(cond), detail=detail); P(f"{cid} {'PASS' if cond else 'FAIL'}  {detail}")
    t0 = time.time()
    sh0 = frozen_shas()
    P("=" * 100)
    P(f"DP1 NSS-off rung DR3 reproduction check (NON-SCORING; code-path test)   mutation: {'drop_nss=False (M1)' if mutate else 'none'}")
    P("=" * 100)
    has = nss_lookup()
    # K1-K3, K6
    b_base, r_base = rung_build(False, 30)
    disk = (DR3 / "wide_binaries_dr3.csv").read_bytes()
    C("K1", r_base["sha256"].startswith(D.REF_SHA_DR3) and b_base == disk, f"registered build {r_base['n_pairs']} pairs sha {r_base['sha256'][:16]}; equals on-disk csv {b_base == disk}")
    b_rung, r_rung = rung_build(drop, 30)
    bv, _ = BV.build(drop, 30)
    C("K2", b_rung == bv, f"wrapper == build_variant_catalogue.build({drop}, 30): {b_rung == bv}; rung {r_rung['n_pairs']} pairs sha {r_rung['sha256'][:16]}")
    b_var, r_var = BV.build(True, 50)
    C("K3", r_var["sha256"] == VARIANT_SHA, f"build(True, 50) sha {r_var['sha256'][:16]} vs committed CFG816 variant {VARIANT_SHA[:16]}")
    rung_rows = rows_of(b_rung)
    probe_rows = [r for r in rows_of(b_var) if float(r["sep_kAU"]) < 30.0]
    n_nss = sum(has(key(r)) for r in rung_rows)
    C("K6", all(2 < float(r["sep_kAU"]) < 30 for r in rung_rows) and n_nss >= 20, f"s range [{min(float(r['sep_kAU']) for r in rung_rows):.2f}, {max(float(r['sep_kAU']) for r in rung_rows):.2f}] kAU; NSS-flagged {n_nss}")
    (HERE / f"nss_off_rung_dr3{tag}.csv").write_bytes(b_rung)
    (HERE / f"nss_off_rung_dr3{tag}.csv.manifest.json").write_text(json.dumps(r_rung, indent=1, default=str) + "\n")
    probe_csv = HERE / "work" / "d2_probe_dr3.csv"
    probe_csv.parent.mkdir(exist_ok=True)
    probe_csv.write_bytes(rows_to_bytes(probe_rows))
    # K4: D2 replication
    P(f"\nbuilding the D2 estimator (1e6 master) ... [{time.time() - t0:.0f} s]")
    est = D2Estimator()
    ref = json.loads((D2DIR / "d2_sigma_sys_defs_results.json").read_text())["fits"]
    rep = est.sequence(d2_inputs(rows_of(CFG816 / "wide_binaries_dr3_variant.csv")))
    dmax = max(max(abs(rep[k]["gamma"] - ref[k]["gamma"]), abs(rep[k]["sigma_fit"] - ref[k]["sigma_fit"])) for k in ref)
    C("K4", dmax <= 1e-9 and len(rep) == len(ref) == 12, f"12 D2 fits reproduced, max |delta| {dmax:.2e}")
    REF_SHIFT = {fo: ref[f"{fo}|{V3}"]["gamma"] - ref[f"{fo}|{V0}"]["gamma"] for fo in FOOTS}
    # P1
    pc = pair_compare(rung_rows, probe_rows, has)
    C("P1", pc["nss_jaccard"] >= 0.90 and pc["other_probe_absent_from_rung"] <= 0.05 and pc["other_rung_absent_from_probe"] <= 0.05,
      f"NSS-flagged rung {pc['nss_rung']} / probe {pc['nss_probe']}, Jaccard {pc['nss_jaccard']:.3f} (>=0.90); other pairs: probe absent from rung "
      f"{100 * pc['other_probe_absent_from_rung']:.2f}%, rung absent from probe {100 * pc['other_rung_absent_from_probe']:.2f}% (<=5%)")
    # P2
    seq = est.sequence(d2_inputs(rung_rows))
    p2 = {}
    for fo in FOOTS:
        b, v = seq[f"{fo}|{V0}"], seq[f"{fo}|{V3}"]
        sh = v["gamma"] - b["gamma"]
        p2[fo] = dict(base=b, rung=v, shift=sh, ref_shift=REF_SHIFT[fo], diff=sh - REF_SHIFT[fo], tol=T_ONE[fo], passed=abs(sh - REF_SHIFT[fo]) <= T_ONE[fo],
                      n42=n42_reading(sh, b["sigma_fit"]))
        P(f"  P2 {fo:9s} base {b['gamma']:.4f}+-{b['sigma_fit']:.4f}  rung {v['gamma']:.4f}+-{v['sigma_fit']:.4f} (N {v['N']})  shift {sh:+.4f} vs ref {REF_SHIFT[fo]:+.4f}  "
          f"|diff| {abs(sh - REF_SHIFT[fo]):.4f} <= {T_ONE[fo]:.4f}?  N4.2: {p2[fo]['n42']}")
    C("P2", all(p2[f]["passed"] for f in FOOTS), "; ".join(f"{f} diff {p2[f]['diff']:+.4f}" for f in FOOTS))
    # P3
    P(f"\nregistered fit path (pipeline --catalog, seed {FIT_SEED}) on baseline, rung, probe ... [{time.time() - t0:.0f} s]")
    rung_csv = HERE / f"nss_off_rung_dr3{tag}.csv"
    F3 = {}
    for nm, path in (("base", DR3 / "wide_binaries_dr3.csv"), ("rung", rung_csv), ("probe", probe_csv)):
        F3[nm] = SS.fit_via_pipeline_cli(path, FIT_SEED)
        P(f"  {nm:5s} " + "  ".join(f"{fo} {F3[nm][fo]['g']:.4f}+-{F3[nm][fo]['s']:.4f} (kappa {F3[nm][fo]['kappa']:.4f})" for fo in FOOTS) + f"  pipeline self-test passed: {F3[nm]['self_test_passed']}")
    p3 = {}
    for fo in FOOTS:
        d = F3["rung"][fo]["g"] - F3["probe"][fo]["g"]
        p3[fo] = dict(rung_shift=F3["rung"][fo]["g"] - F3["base"][fo]["g"], probe_shift=F3["probe"][fo]["g"] - F3["base"][fo]["g"], diff=d, tol=T_ONE[fo],
                      passed=abs(d) <= T_ONE[fo], n42=n42_reading(F3["rung"][fo]["g"] - F3["base"][fo]["g"], F3["base"][fo]["s"]))
        P(f"  P3 {fo:9s} rung shift {p3[fo]['rung_shift']:+.4f}, probe shift {p3[fo]['probe_shift']:+.4f}, |rung - probe| {abs(d):.4f} <= {T_ONE[fo]:.4f}?  N4.2: {p3[fo]['n42']}")
    C("P3", all(p3[f]["passed"] for f in FOOTS), "; ".join(f"{f} diff {p3[f]['diff']:+.4f}" for f in FOOTS))
    # P4
    P(f"\nensemble K = {K_ENS} (stage-G seed offsets 1..{K_ENS}) ... [{time.time() - t0:.0f} s]")
    ens = []
    for k in range(1, K_ENS + 1):
        bb, _ = rung_build(False, 30, seed_offset=k)
        bp, _ = rung_build(True, 50, seed_offset=k)
        br, _ = rung_build(drop, 30, seed_offset=k)
        g50 = DR3 / f"seed_k{k}" / "final_g50.csv"
        rb, rp, rr = rows_of(bb), [r for r in rows_of(bp) if float(r["sep_kAU"]) < 30.0], rows_of(br)
        e = dict(k=k, N=dict(base=len(rb), probe=len(rp), rung=len(rr)), base_equals_g50_build=(g50.exists() and bb == g50.read_bytes()), nss_rung=sum(has(key(r)) for r in rr))
        for fo in FOOTS:
            fb, fp, fr = est.fit_fresh(rb, fo), est.fit_fresh(rp, fo), est.fit_fresh(rr, fo)
            e[fo] = dict(base=fb["gamma"], probe=fp["gamma"], rung=fr["gamma"], sigma_fit_base=fb["sigma_fit"])
        ens.append(e)
        P(f"  k={k}  N base/probe/rung {len(rb)}/{len(rp)}/{len(rr)}  base==Q-G50 build {e['base_equals_g50_build']}  " + "  ".join(
            f"{fo}: base {e[fo]['base']:.4f} probe {e[fo]['probe']:+.4f}-b={e[fo]['probe'] - e[fo]['base']:+.4f} rung-b={e[fo]['rung'] - e[fo]['base']:+.4f}" for fo in FOOTS))
    p4 = {}
    for fo in FOOTS:
        d = np.array([e[fo]["rung"] - e[fo]["probe"] for e in ens]); sp = np.array([e[fo]["probe"] - e[fo]["base"] for e in ens])
        sr = np.array([e[fo]["rung"] - e[fo]["base"] for e in ens])
        p4[fo] = dict(mean_rung_minus_probe=float(d.mean()), sd=float(d.std(ddof=1)), tol=E_ENS[fo], passed=abs(d.mean()) <= E_ENS[fo],
                      mean_probe_shift=float(sp.mean()), sd_probe_shift=float(sp.std(ddof=1)), mean_rung_shift=float(sr.mean()), sd_rung_shift=float(sr.std(ddof=1)))
        P(f"  P4 {fo:9s} mean(rung - probe) {d.mean():+.4f} (SD {d.std(ddof=1):.4f}) |.| <= {E_ENS[fo]:.4f}?   mean NSS-off shift: probe {sp.mean():+.4f} (SD {sp.std(ddof=1):.4f}), "
          f"rung {sr.mean():+.4f} (SD {sr.std(ddof=1):.4f})")
    C("P4", all(p4[f]["passed"] for f in FOOTS), "; ".join(f"{f} mean diff {p4[f]['mean_rung_minus_probe']:+.4f}" for f in FOOTS))
    sh1 = frozen_shas()
    C("K5", sh1 == sh0 and sh0["wide_binary_pipeline.py"] == PIPE_SHA, f"frozen sha256 unchanged: {sh1 == sh0}; pipeline {sh0['wide_binary_pipeline.py'][:8]}")
    kok = all(checks[c]["passed"] for c in ("K1", "K2", "K3", "K4", "K5", "K6"))
    pok = all(checks[c]["passed"] for c in ("P1", "P2", "P3", "P4"))
    verdict = ("CODE FAULT" if not kok else ("REPRODUCED" if pok else "NOT REPRODUCED"))
    P(f"\nDP1 DR3 CHECK{' (MUTATE M1)' if mutate else ''}: {verdict}   (K {sum(checks[c]['passed'] for c in checks if c[0] == 'K')}/6, P {sum(checks[c]['passed'] for c in checks if c[0] == 'P')}/4)  [{time.time() - t0:.0f} s]")
    out = dict(mutate=mutate, verdict=verdict, checks=checks, reference_shift=REF_SHIFT, tolerances=dict(T_one=T_ONE, E_ens=E_ENS, sigma_G=SIGMA_G),
               K4_max_delta=dmax, P1=pc, P2=p2, P3=dict(fits={k: {f: v[f] for f in FOOTS} | {"self_test_passed": v["self_test_passed"]} for k, v in F3.items()}, rows=p3),
               P4=p4, ensemble=ens, rung_report=r_rung, frozen_sha256=sh0)
    (HERE / f"dr3_check{tag}.json").write_text(json.dumps(out, indent=1, default=float) + "\n")
    (HERE / f"dr3_check{tag}.out").write_text("\n".join(lines) + "\n")
    return 0 if verdict == ("NOT REPRODUCED" if mutate else "REPRODUCED") else 1


# ------------------------------------------------------------------ CLI (the driver's conventions)
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--dr3-check", action="store_true")
    ap.add_argument("--mutate", action="store_true", help="with --dr3-check: the M1 run (drop_nss=False)")
    ap.add_argument("--release", choices=("dr3", "dr4"), default="dr3")
    ap.add_argument("--variant", choices=("primary", "allsource_15c"), default="primary")
    ap.add_argument("--cut13", choices=("extract-builder", "extract-orbit", "extract-literal", "cones-literal", "cones-orbit"), default="extract-builder",
                    help="pass the SAME mode as the primary build it is compared with (DR4: cones-literal, D7 N9)")
    ap.add_argument("--neighbours", action="append", default=[]); ap.add_argument("--neighbour-pairs", action="append", default=[])
    ap.add_argument("--neighbours-manifest", default=None); ap.add_argument("--missing-cones", choices=("error", "extract-fallback"), default="error")
    ap.add_argument("--manifest", default=None); ap.add_argument("--allow-network", action="store_true")
    ap.add_argument("--corr-transport", choices=("async", "sync"), default="async")
    ap.add_argument("--seed-offset", type=int, default=0); ap.add_argument("--stage-dir", default=None)
    ap.add_argument("--out-csv", default=None)
    ap.add_argument("--keep-nss", action="store_true", help="MUTATE: drop_nss=False (not the rung)")
    ap.add_argument("--fit", action="store_true", help="fit the rung CSV by the registered path (pipeline --catalog, seed 20261216)")
    ap.add_argument("--baseline-csv", default=None, help="with --fit: the primary build's CSV, fitted the same way; the shift and the N4.2 reading are reported")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if a.dr3_check:
        return dr3_check(a.mutate)
    if not a.out_csv:
        raise SystemExit("need --out-csv PATH (or --self-test / --dr3-check)")
    if a.corr_transport == "sync" and not a.allow_network:
        raise SystemExit("--corr-transport sync only matters with --allow-network")
    D.init(a.allow_network)
    manifest = json.loads(Path(a.manifest).read_text()) if a.manifest else None
    if a.neighbours_manifest:
        for e in json.loads(Path(a.neighbours_manifest).read_text()):
            if e.get("include") is True:
                a.neighbours.append(e["neighbours"]); a.neighbour_pairs.append(e["pairs"])
    cones = None
    if a.cut13.startswith("cones-"):
        import cones_cut13
        if not a.neighbours or len(a.neighbours) != len(a.neighbour_pairs):
            raise SystemExit("a cones kind needs --neighbours and --neighbour-pairs (or --neighbours-manifest)")
        cones = cones_cut13.ConeTable.from_files(zip(a.neighbours, a.neighbour_pairs))
    sh0 = frozen_shas()
    csv_bytes, rep = rung_build(not a.keep_nss, 30, a.release, a.variant, a.cut13, manifest, a.allow_network, seed_offset=a.seed_offset, stage_dir=a.stage_dir,
                                cones=cones, missing_cones=a.missing_cones, corr_transport=a.corr_transport)
    Path(a.out_csv).write_bytes(csv_bytes)
    rep.update(out=os.path.basename(a.out_csv), out_sha256=sha256(csv_bytes), frozen_sha256=sh0, dr3_check="dr4_push_2026_11_05/DP1_nss_off_rung/dr3_check.json")
    if a.fit:
        fr = SS.fit_via_pipeline_cli(a.out_csv, FIT_SEED)
        rep["fit"] = {f: fr[f] for f in FOOTS} | {"self_test_passed": fr["self_test_passed"]}
        if a.baseline_csv:
            fb = SS.fit_via_pipeline_cli(a.baseline_csv, FIT_SEED)
            rep["baseline_fit"] = {f: fb[f] for f in FOOTS} | {"self_test_passed": fb["self_test_passed"], "csv_sha256": sha256(Path(a.baseline_csv).read_bytes())}
            rep["nss_off_shift"] = {f: dict(shift=fr[f]["g"] - fb[f]["g"], shift_over_sigma_fit=(fr[f]["g"] - fb[f]["g"]) / fb[f]["s"],
                                            N4_2=n42_reading(fr[f]["g"] - fb[f]["g"], fb[f]["s"])) for f in FOOTS}
    if frozen_shas() != sh0:
        raise SystemExit("a frozen file changed during the run")
    Path(a.out_csv + ".manifest.json").write_text(json.dumps(rep, indent=1, default=str) + "\n")
    print(json.dumps({k: rep.get(k) for k in ("n_pairs", "out_sha256", "variant_switches", "rung", "fit", "nss_off_shift")}, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
