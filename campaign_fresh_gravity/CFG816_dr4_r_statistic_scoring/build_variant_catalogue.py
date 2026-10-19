#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
build_variant_catalogue.py -- the R-analysis input of CFG825 (dir CFG816_dr4_r_statistic_scoring): the registered stage G with TWO cuts changed.  NEW CODE ONLY; nothing registered is edited.

WHAT IS CHANGED (and nothing else)
  1. the "NSS screen" (cut 12, `~nss`) is REMOVED, so pairs with a non-single-star component stay in the catalogue and carry their per-star flag (make_pair_table.py joins it; the NSS-screened
     branch of cfg816_r.py then differs from the primary, as the frozen criteria intend);
  2. the "2<s<30 kAU" cut becomes "2<s<50 kAU", so the numerator cap of the frozen primary (s <= 50 kAU) is reachable.
  Every other cut, the triple search (whose 30 kAU radius is UNCHANGED, see the declaration), R_chance < 0.01, the correlation caches, the seeds and the driver's copied stage G are the registered ones.

HOW (no copy to drift): the variant of `build_catalog.frozen_cuts` is made from the registered function's OWN SOURCE TEXT with two exactly-asserted string replacements, executed in the builder's module
namespace, and swapped in only for the duration of the call. The SELF-TEST proves the mechanism: with both switches OFF the build reproduces the registered DR3 catalogue BYTE FOR BYTE
(the driver's REF_SHA_DR3), and the added pairs of each switch are checked to be exactly the pairs that switch should add.

  python3 build_variant_catalogue.py --self-test                     (DR3, offline; four builds of about 20 s each; needs the on-disk DR3 extract)
  python3 build_variant_catalogue.py --out PATH.csv                  (DR3 variant catalogue + PATH.csv.manifest.json; both switches ON)
  python3 build_variant_catalogue.py --release dr4 --manifest M.json --allow-network --out PATH.csv   (DR4: the driver's own options pass through; UNTESTED, DR4 does not exist yet)

DR3 numbers are code-path tests, never results (Amendment 7(e)).
"""
import os, sys, io, csv, json, hashlib, inspect, argparse, contextlib
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PREP = ROOT / "prep_2026" / "gaia_dr4_prep"
sys.path.insert(0, str(PREP / "dr4_ready_1"))
import dry_run_driver as D                                  # read-only; defines functions and constants at import (init() does the real work)

NSS_LINE = '        "NSS screen": ~nss,\n'
SEP_LINE = '"2<s<30 kAU": (sep_au > 2000) & (sep_au < 30000),'


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def patched_frozen_cuts(orig_fn, drop_nss, smax_kau):
    """the registered frozen_cuts with the two edits, built from its source text"""
    src = inspect.getsource(orig_fn)
    if drop_nss:
        assert src.count(NSS_LINE) == 1, "the NSS cut line is not where it was: refusing to patch"
        src = src.replace(NSS_LINE, "")
    if int(smax_kau) != 30:
        assert src.count(SEP_LINE) == 1, "the separation cut line is not where it was: refusing to patch"
        src = src.replace(SEP_LINE, f'"2<s<{int(smax_kau)} kAU": (sep_au > 2000) & (sep_au < {int(smax_kau) * 1000}),')
    ns = D.B.__dict__
    exec(compile(src, "<variant frozen_cuts>", "exec"), ns)       # defines frozen_cuts in the builder's own namespace (all its globals resolve as registered)
    return ns["frozen_cuts"]


def build(drop_nss, smax_kau, release="dr3", variant="primary", cut13="extract-builder", manifest=None, allow_network=False, corr_transport="async"):
    orig = D.B.frozen_cuts
    try:
        D.B.frozen_cuts = patched_frozen_cuts(orig, drop_nss, smax_kau)
        csv_bytes, report = D.run(release, variant, cut13, manifest, allow_network, corr_transport=corr_transport)
    finally:
        D.B.frozen_cuts = orig
    report["variant_switches"] = dict(drop_nss_cut=bool(drop_nss), smax_kAU=int(smax_kau))
    return csv_bytes, report


def pairs_of(csv_bytes):
    rows = list(csv.DictReader(io.StringIO(csv_bytes.decode())))
    return {(int(r["source_id1"]), int(r["source_id2"])): float(r["sep_kAU"]) for r in rows}


def self_test():
    """V1 proves the mechanism (byte-identical with both switches off). V2-V8 check the INTENDED differences against the measured Monte-Carlo flip noise.
    NOTE (2026-10-18): a first version of this test expected each variant to be an exact superset of the registered catalogue; that expectation was WRONG. The registered stage G draws a seeded
    Monte-Carlo velocity-error cut over the pair array, so ANY change of the pair array shifts the stream and flips about 2.2-2.6% of marginal pairs each way (Amendment 18's measured
    sensitivity). A pure reseed of the registered build reproduces that rate (V2), so the checks separate the intended additions from the flips."""
    D.init(False)                                           # socket guard ON: no network
    ext = D.extract_dir("dr3", "primary")
    z = np.load(ext / "stage_A.npz")
    sid = z["source_id"]; order = np.argsort(sid, kind="stable"); ss = sid[order]; nss_col = z["non_single_star"]
    def has_nss(pair):
        i = order[np.searchsorted(ss, np.array(pair))]
        return bool((nss_col[i] != 0).any())
    res, ok = {}, True
    def T(name, cond, detail=""):
        nonlocal ok
        ok &= bool(cond); print(f"  [{'PASS' if cond else 'FAIL'}] {name}  {detail}"); res[name] = bool(cond)
    def parts(P, reg):
        lost = set(reg) - set(P); add = set(P) - set(reg)
        f = {p for p in add if has_nss(p)}; w = {p for p in add if P[p] >= 30 and p not in f}; o = add - f - w
        return lost, f, w, o
    b0, r0 = build(False, 30)
    T("V1 both switches OFF reproduces the registered DR3 catalogue byte for byte (REF_SHA_DR3)", r0["sha256"].startswith(D.REF_SHA_DR3), f"{r0['n_pairs']:,d} pairs, sha256 {r0['sha256'][:16]}")
    reg = pairs_of(b0); n = len(reg)
    T("V0 the registered catalogue has no NSS-flagged component and no pair at or beyond 30 kAU (so every such pair in a variant is an intended addition)",
      not any(has_nss(p) for p in reg) and max(reg.values()) < 30, f"max s {max(reg.values()):.2f} kAU")
    base = []
    try:
        for k in (1, 2):
            bk, _ = D.run("dr3", "primary", "extract-builder", None, False, seed_offset=k); Pk = pairs_of(bk)
            lost, f, w, o = parts(Pk, reg); base.append((len(lost) / n, len(o) / n, len(f) + len(w)))
        base_lost = max(b[0] for b in base); base_add = max(b[1] for b in base)
        T("V2 BASELINE: reseeding the REGISTERED build alone flips 1-4% of pairs each way and adds no NSS-flagged or wide pair", all(0.01 <= b[0] <= 0.04 and 0.01 <= b[1] <= 0.04 and b[2] == 0 for b in base),
          "; ".join(f"seed+{k}: lost {100*b[0]:.2f}%, added {100*b[1]:.2f}%" for k, b in zip((1, 2), base)))
    except Exception as e:
        print("  [NOT RUN] V2 baseline (seed_offset builds unavailable):", repr(e)[:140]); base_lost = base_add = 0.04; ok = False
    out = {}
    for name, (dn, sm) in {"nss": (True, 30), "wide": (False, 50), "both": (True, 50)}.items():
        b, _ = build(dn, sm); out[name] = pairs_of(b)
    ln, fn, wn, on = parts(out["nss"], reg)
    T("V3 NSS cut dropped alone: it adds NSS-flagged pairs (all s < 30 kAU) and no wide pair", len(fn) >= 20 and all(out["nss"][p] < 30 for p in fn) and len(wn) == 0, f"+{len(fn)} NSS-flagged ({100*len(fn)/n:.2f}% of registered)")
    T("V4 ... the rest of the change is flip noise: lost and other-added within baseline + 1 percentage point", len(ln) / n <= base_lost + 0.01 and len(on) / n <= base_add + 0.01, f"lost {100*len(ln)/n:.2f}%, other-added {100*len(on)/n:.2f}%")
    lw, fw, ww, ow = parts(out["wide"], reg)
    T("V5 cap 50 kAU alone: it adds wide pairs (30 <= s < 50 kAU, none NSS-flagged) and no NSS-flagged pair", len(ww) >= 1 and all(30 <= out["wide"][p] < 50 for p in ww) and len(fw) == 0,
      f"+{len(ww)} wide pairs, separations {sorted(round(out['wide'][p], 1) for p in ww)} kAU")
    T("V6 ... the rest is flip noise within baseline + 1 percentage point", len(lw) / n <= base_lost + 0.01 and len(ow) / n <= base_add + 0.01, f"lost {100*len(lw)/n:.2f}%, other-added {100*len(ow)/n:.2f}%")
    lb, fb, wb, ob = parts(out["both"], reg)
    jac = lambda A, B: len(A & B) / max(1, len(A | B))
    T("V7 both switches: the NSS-flagged additions agree with the NSS-only build (Jaccard >= 0.9) and the wide additions with the cap-only build (overlap >= half)",
      jac(fb, fn) >= 0.9 and len(wb & ww) >= 0.5 * min(len(wb), len(ww)), f"NSS-flagged {len(fb)} (Jaccard {jac(fb, fn):.2f}); wide {len(wb)} (overlap {len(wb & ww)})")
    P = out["both"]
    T("V8 both switches: separations lie in (2, 50) kAU, some exceed 30, and the flip noise is within baseline + 1 pp", min(P.values()) >= 2 and max(P.values()) < 50 and max(P.values()) > 30 and len(lb) / n <= base_lost + 0.01 and len(ob) / n <= base_add + 0.01,
      f"[{min(P.values()):.2f}, {max(P.values()):.2f}] kAU; lost {100*len(lb)/n:.2f}%, other-added {100*len(ob)/n:.2f}%")
    try:
        patched_frozen_cuts(lambda: None, True, 30); refused = False
    except Exception:
        refused = True
    T("V9 patching a function whose source does not contain the registered cut lines is refused", refused)
    print("SELF-TEST", "PASSED" if ok else "FAILED")
    json.dump(dict(self_test=res, n_registered=n, nss_flagged_added=len(fb), wide_added=len(wb), baseline_flip=[dict(lost=b[0], added=b[1]) for b in base], n_variant=len(P), max_sep_kAU=max(P.values())),
              open(HERE / "build_variant_selftest.json", "w"), indent=1)
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true"); ap.add_argument("--out")
    ap.add_argument("--release", default="dr3", choices=("dr3", "dr4")); ap.add_argument("--variant", default="primary", choices=("primary", "allsource_15c"))
    ap.add_argument("--manifest"); ap.add_argument("--allow-network", action="store_true"); ap.add_argument("--corr-transport", default="async", choices=("async", "sync"))
    a = ap.parse_args()
    if a.self_test:
        sys.exit(self_test())
    if not a.out:
        sys.exit("need --out PATH (or --self-test)")
    D.init(a.allow_network)
    man = json.loads(Path(a.manifest).read_text()) if a.manifest else None
    csv_bytes, rep = build(True, 50, a.release, a.variant, "extract-builder", man, a.allow_network, a.corr_transport)
    Path(a.out).write_bytes(csv_bytes)
    rep.update(out=os.path.basename(a.out), out_sha256=sha256(csv_bytes),
               patched_files=dict(build_catalog_sha256=sha256(Path(D.B.__file__).read_bytes()), dry_run_driver_sha256=sha256(Path(D.__file__).read_bytes())),
               changes=["NSS screen removed", "2<s<30 kAU -> 2<s<50 kAU"], unchanged_note="the triple search keeps its registered 30 kAU radius; all other cuts as registered")
    json.dump(rep, open(a.out + ".manifest.json", "w"), indent=1, default=str)
    print(json.dumps({k: rep[k] for k in ("n_pairs", "out_sha256", "variant_switches")}, indent=1)); print("wrote", a.out)


if __name__ == "__main__":
    main()
