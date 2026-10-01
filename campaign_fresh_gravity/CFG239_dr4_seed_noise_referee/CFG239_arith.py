#!/usr/bin/env python3
"""CFG239 arithmetic note: what '5 to 9%' was.  Reads only saved CFG239 outputs; no repo file is touched.
r = sigma_build / sigma_fit (measured, DR3 code-path, Amdt 7(e)); sigma_tot = sqrt(sigma_fit^2 + sigma_sys^2);
B = sigma_build / sigma_tot; understatement = sqrt(sigma_tot^2 + sigma_build^2)/sigma_tot - 1 = sqrt(1 + B^2) - 1."""
import json, re
from pathlib import Path
H = Path(__file__).resolve().parent
g = json.loads((H / "CFG239_c3_fits_g100.json").read_text())["g101"]
cmp_ = (H / "CFG239_post_compare.out").read_text()
m = re.findall(r"G-only SEED\+0\.\.50 \[(can|alt)\] n=51 .*? mean sigma_fit ([0-9.]+)\s+SD/sigma_fit ([0-9.]+)", cmp_)
g50 = {k: (float(s), float(r)) for k, s, r in m}
c5 = (H / "CFG239_c5_posthoc.out").read_text()
m = re.findall(r"pooled G-only \[(can|alt)\] n=151 .*? mean sigma_fit ([0-9.]+)\s+SD/sigma_fit ([0-9.]+)", c5)
pool = {k: (float(s), float(r)) for k, s, r in m}
out = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); out.append(s)
def row(label, sf, r, ss):
    st = (sf**2 + ss**2) ** .5; sb = r * sf; B = sb / st
    P(f"  {label:44s} sigma_fit {sf:.4f}  r {r:.3f}  sigma_sys {ss:.2f}  sigma_tot {st:.4f}  sigma_build {sb:.4f}  B=sb/stot {B:.3f}  "
      f"sqrt(1+B^2)-1 = {((1+B*B)**.5-1)*100:.1f}%   B^2/(1+B^2) = {B*B/(1+B*B)*100:.1f}%")
P("CFG239 arithmetic note | DR3 numbers are code-path tests only (Amdt 7(e))")
P("Measured r (SD(gamma-hat)/mean sigma_fit): K=100 G-only can/alt", round(g['can']['ratio'],3), round(g['alt']['ratio'],3),
  "| SEED+0..50 set", g50['can'][1], g50['alt'][1], "| 151 pooled", pool['can'][1], pool['alt'][1])
P("\n(1) what I wrote: sqrt(1 + r^2) - 1 with NO sigma_sys (i.e. relative to sigma_fit): r = 0.333 -> %.1f%%, r = 0.437 -> %.1f%%; also r=0.33 -> %.1f%%, 0.44 -> %.1f%%" %
  tuple(((1 + r*r)**.5 - 1) * 100 for r in (0.333, 0.437, 0.33, 0.44)))
P("    r itself x 100 would be 33 to 44%; r^2/(1+r^2) would be 10% to 16%: NOT what was written.")
for ss in (0.02, 0.0):
    P(f"\n(2) at DR3's N (my runs' mean sigma_fit), sigma_sys = {ss}")
    row("low end: alt, K=100 (r 0.333)", g['alt']['mean_sigma'], g['alt']['ratio'], ss)
    row("high end: canonical, SEED+0..50 (r 0.437)", g50['can'][0], g50['can'][1], ss)
    row("generic 0.33 at 0.0514", 0.0514, 0.33, ss)
    row("generic 0.44 at 0.0568", 0.0568, 0.44, ss)
    row("canonical K=100 (r 0.358)", g['can']['mean_sigma'], g['can']['ratio'], ss)
    row("rev-3 reference: sigma_fit 0.0557, r 0.30", 0.0557, 0.30, ss)
for ss in (0.02, 0.0):
    P(f"\n(3) at the pre-registered DR4 sigma_fit = 0.019 (prereg line 631: sigma_fit ~ 0.019, sigma_tot ~ 0.028), sigma_sys = {ss}")
    for r in (0.30, 0.333, 0.437, 0.44):
        row(f"r {r}", 0.019, r, ss)
(H / "CFG239_arith.out").write_text("\n".join(out) + "\n")
