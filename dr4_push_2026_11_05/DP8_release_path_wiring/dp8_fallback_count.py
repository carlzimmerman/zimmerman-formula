#!/usr/bin/env python3
"""DP8: the number of NSS-off rung pairs handled by the missing-cones fallback (criteria FROZEN_CRITERIA.md, 4caa8bc91f). NEW CODE.

Owner decision 2026-11-15b Q2: pairs of the NSS-off rung that reach cut 13 with no cone are handled with
`--missing-cones extract-fallback` (nss_off_rung.py, step G11) / `--rung-missing-cones extract-fallback` (the seed-mean sweep,
step G11S), and the number of fallback pairs is stated in the result. This reads the counts the tools already record:
  --rung-manifest  <rung csv>.manifest.json written by nss_off_rung.py (its 'cut13_cones' block, from cones_cut13.flags)
  --sweep-json     the sweep's <out>.json (dp7_seed_mean.py: 'bias_bound', the k = 0 rung)
and writes one JSON plus printed lines. Exit 1 if a given input has no cones block, or its policy is not extract-fallback.
Offline; reads two JSON files. kappa = 1/2 FITTED; footings never pooled; not theory closed. Nothing here says the data favour
the framework.
"""
import sys
sys.dont_write_bytecode = True
import argparse, json, os


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--rung-manifest", default=None)
    ap.add_argument("--sweep-json", default=None)
    ap.add_argument("--out-json", required=True)
    ap.add_argument("--tag", default="")
    a = ap.parse_args(argv)
    out, ok, lines = dict(tag=a.tag, decision="OWNER_DECISION_2026-11-15b Q2 (fallback for the rung's uncovered pairs)",
                          note="kappa = 1/2 FITTED; footings never pooled; not theory closed"), True, []
    if not (a.rung_manifest or a.sweep_json):
        raise SystemExit("give --rung-manifest and/or --sweep-json")
    if a.rung_manifest:
        m = json.load(open(a.rung_manifest))
        cc = m.get("cut13_cones")
        if not cc:
            ok = False
            lines.append(f"G11 rung ({os.path.basename(a.rung_manifest)}): NO cut-13 cones block (cut13 = {m.get('cut13')}); fallback count not available")
            out["g11_rung"] = dict(file=os.path.basename(a.rung_manifest), cut13=m.get("cut13"), cones_block=False)
        else:
            pol = cc.get("missing_policy")
            ok &= (pol == "extract-fallback")
            out["g11_rung"] = dict(file=os.path.basename(a.rung_manifest), cut13=m.get("cut13"), n_pairs_reaching_cut13=cc.get("n_pairs"),
                                   n_covered=cc.get("n_covered"), n_without_cone=cc.get("n_missing"), policy=pol,
                                   n_flagged_by_fallback=cc.get("n_flagged_fallback"), n_flagged_by_cones=cc.get("n_flagged_cones"),
                                   final_rung_pairs=m.get("n_pairs"))
            lines.append(f"G11 rung: {cc.get('n_missing')} of {cc.get('n_pairs')} pairs reaching cut 13 had no cone; policy {pol}; "
                         f"the fallback flagged {cc.get('n_flagged_fallback')}; the cones flagged {cc.get('n_flagged_cones')} of {cc.get('n_covered')} covered"
                         + ("" if pol == "extract-fallback" else "  [NOT the decided fallback]"))
    if a.sweep_json:
        s = json.load(open(a.sweep_json))
        bb = s.get("bias_bound")
        if not bb:
            ok = False
            lines.append(f"seed-mean sweep ({os.path.basename(a.sweep_json)}): no bias_bound block (cut13 {s.get('cut13')}); fallback count not available")
            out["sweep_rung_k0"] = dict(file=os.path.basename(a.sweep_json), cut13=s.get("cut13"), cones_block=False)
        else:
            pol = bb.get("policy")
            ok &= (pol == "extract-fallback") and (s.get("rung_missing_cones") == "extract-fallback")
            out["sweep_rung_k0"] = dict(file=os.path.basename(a.sweep_json), release=s.get("release"), K=s.get("K"), cut13=s.get("cut13"),
                                        rung_missing_cones=s.get("rung_missing_cones"), n_without_cone=bb.get("rung_n_missing"),
                                        n_covered=bb.get("rung_n_covered"), policy=pol, n_flagged_by_fallback=bb.get("fallback_flagged"),
                                        cones_flag_rate=bb.get("cones_flag_rate"), expected_flagged_if_cones_existed=bb.get("expected_flagged_by_cones"))
            lines.append(f"seed-mean sweep (k = 0 rung; the set is seed-independent): {bb.get('rung_n_missing')} pairs without a cone; policy {pol}; "
                         f"the fallback flagged {bb.get('fallback_flagged')}; ~{(bb.get('expected_flagged_by_cones') or 0):.2f} expected had cones existed")
    out["policy_is_extract_fallback"] = bool(ok)
    json.dump(out, open(a.out_json, "w"), indent=1)
    for s_ in lines:
        print(s_)
    print("fallback policy as decided (2026-11-15b Q2): " + ("yes" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
