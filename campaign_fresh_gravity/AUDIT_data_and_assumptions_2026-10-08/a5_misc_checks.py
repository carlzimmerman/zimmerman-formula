#!/usr/bin/env python3
"""AUDIT A5 (read-only): small cross-lane checks.
 (1) CFG438: the unresolved 80-100 km/s blue systemic offset vs Law+12 z = 2.1765.  The script uses the VACUUM H-alpha
     rest wavelength 6564.61 A and the cube is on a vacuum scale (OH check).  If Law+12's z was computed with the AIR rest
     wavelength 6562.80 A, the expected offset is c (6562.80/6564.61 - 1).  Candidate explanation only (not verified).
 (2) CFG434: reading II's 'borderline' escape needs the clumped matter amplitude >= +25% over LCDM (README).  The record's
     adopted growth rule (CFG424/425/439 zero-knob) gives sigma8 +0.2..+0.5% and max|P-1| <= 4% with the phantom
     compensated per catchment, so the escape the README points to (T5's +21..26%) is not the adopted model.
 (3) CFG436: registered slow-rate ratio across T16's lambda window (labels now stale after CFG453) -- spread of the ratio.
 (4) CFG439 README rounds the DE max|P-1| 0.03345 to 0.034; PAPER45 prints 0.033 (both from the same JSON)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.abspath(os.path.join(HERE, ".."))
L, out = [], {}
c = 299792.458
dv = c * (6562.80 / 6564.61 - 1); out["cfg438_air_vac_offset_kms"] = dv
L.append(f"(1) CFG438 air-vs-vacuum H-alpha offset: {dv:+.1f} km/s (observed: 80-100 km/s blue of Law's z) -> consistent; candidate cause, unverified")
g = {}
for lane, f, keys in (("CFG424", "CFG424_turnaround_catchment/cfg424_results.json", ("TA-can", "TA-alt")),
                      ("CFG425", "CFG425_turnaround_catchment_confirm/cfg425_results.json", ("R1 256^3 seed 360", "R2 256^3 seed 361", "R3 512^3 seed 359")),
                      ("CFG439", "CFG439_zero_knob_alt_512/cfg439_results.json", ("A FLAT alt", "B DE canonical"))):
    d = json.load(open(os.path.join(CFG, f)))
    for k in keys: g[f"{lane} {k}"] = (d[k]["s8"], d[k]["pdev"])
s8max = max(v[0] for v in g.values()) - 1; pmax = max(v[1] for v in g.values())
out["zero_knob_s8_excess_max"] = s8max; out["zero_knob_pdev_max"] = pmax
L.append(f"(2) zero-knob growth rule: sigma8 excess <= {100*s8max:.2f}%, max|P-1| <= {pmax:.3f} over {len(g)} runs; "
         f"CFG434 reading II smooth needs clumped amplitude >= +25% (|z|<=2) -> escape NOT available under the adopted rule")
d436 = json.load(open(os.path.join(CFG, "CFG436_chexmate_zslope/cfg436_results.json")))
L.append("(3) CFG436 registered ratio x(bin4)/x(bin3) over lambda 0.0073-0.028: 0.862-0.873 (README table) -> lambda labels stale "
         "(T16 window withdrawn by CFG453) but the prediction moves < 1.3%")
out["cfg436_keys"] = list(d436.keys())[:12]
d439 = json.load(open(os.path.join(CFG, "CFG439_zero_knob_alt_512/cfg439_results.json")))
L.append(f"(4) CFG439 DE canonical max|P-1| = {d439['B DE canonical']['pdev']:.5f} -> rounds to 0.033 (PAPER45 right; CFG439 README's 0.034 is a rounding slip)")
json.dump(out, open(os.path.join(HERE, "a5_misc_checks.json"), "w"), indent=1)
print("\n".join(L)); open(os.path.join(HERE, "a5_misc_checks.out"), "w").write("\n".join(L) + "\n")
