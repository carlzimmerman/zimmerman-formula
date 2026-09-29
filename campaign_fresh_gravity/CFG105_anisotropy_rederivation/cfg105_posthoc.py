#!/usr/bin/env python3
"""CFG105 POST HOC (declared as such, written after seeing the main run: the Osipkov-Merritt row moved the law by 3 sigma).
Reuses the top of cfg105_aniso.py (solver + baseline; controls run again) without modifying it.  Diagnostics only; no pass lines."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "cfg105_aniso.py")).read().split('if STAGE == "controls":')[0]
os.environ["STAGE"] = "controls"; os.environ["MUTATE"] = "0"
exec(compile(src, "cfg105_aniso_top", "exec"))
class AnisoSat(Aniso):
    """saturating Osipkov-Merritt: beta(r) = bm r^2/(r^2+ra^2); ln F = bm ln(r^2+ra^2)."""
    def __init__(self, ra, bm): self.ra, self.bm = ra, bm
    def beta(self, r): return self.bm * r ** 2 / (r ** 2 + self.ra ** 2)
    def lnF(self, r): return self.bm * np.log(r ** 2 + self.ra ** 2)
def ln_nu_cut(gamma, rc): return lambda r: -gamma * np.log(r) - (r / rc) ** 2
def runx(f, mk_an, mk_ln):
    res = {"law": {}, "rule": {}}
    for n in SEL:
        for m in ("law", "rule"):
            res[m][n] = gal_offset(n, f, m, mk_ln(n), mk_an(n))
    return summ(res)
def line(s): return f"law {s['law'][0]:+.4f} ({sg(s['law']):+.2f}s) rule {s['rule'][0]:+.4f} ({sg(s['rule']):+.2f}s)"
P("\n== P0 outer-bin projected radii in units of R_e (bins entering the offset) ==")
x = np.concatenate([BINS[n]["Rb"][BINS[n]["out"]] / BINS[n]["Re"] for n in SEL])
P(f"  N bins {len(x)}; R/Re percentiles 10/50/90/max: {np.percentile(x,10):.1f} {np.percentile(x,50):.1f} {np.percentile(x,90):.1f} {x.max():.1f}")
P("\n== P1 saturating OM: beta(r) = bm r^2/(r^2+ra^2), canonical | alt ==")
for bm in (0.5, 0.75):
    for k in (1, 3, 10):
        P(f"  bm {bm} ra {k:2d} Re: " + " | ".join(line(runx(f, lambda n, k=k, bm=bm: AnisoSat(k * BINS[n]['Re'], bm), lambda n: ln_nu_power(GAM[n]))) for f in FOOTS))
P("\n== P2 outer tracer cutoff  nu = r^-gamma_i exp[-(r/rc)^2], rc = 20 Re / 50 Re / none ==")
for lbl, an_of in (("beta=0", lambda n: const_beta(0.0)), ("beta=+0.5", lambda n: const_beta(0.5)), ("beta=+0.9", lambda n: const_beta(0.9)),
                   ("OM ra=3Re", lambda n: om_beta(3 * BINS[n]['Re'])), ("OM ra=10Re", lambda n: om_beta(10 * BINS[n]['Re']))):
    for kc in (20, 50, None):
        P(f"  {lbl:10s} rc={('%dRe' % kc) if kc else 'none':5s}: " + " | ".join(line(runx(f, an_of, (lambda n, kc=kc: ln_nu_cut(GAM[n], kc * BINS[n]['Re']) if kc else ln_nu_power(GAM[n])))) for f in FOOTS))
P("\n== P3 rule with the nulling beta: leave rule ==")
P("done")
open(os.path.join(HERE, "cfg105_posthoc.out"), "w").write("\n".join(out_lines) + "\n")
