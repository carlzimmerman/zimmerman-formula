#!/usr/bin/env python3
"""CFG258 POST HOC (labelled; not in the frozen criteria): how large is the formal error of the E1 / E2 fit against the empirical scatter of the fitted slope, in the primary cell C0?
Why: the README's reading of the 'formal 5 sigma' of the quoted anchored slope rests on the formal error being far below the empirical one (the CFG219 lesson: a statistic that does not see the shared and correlated terms is too confident).
Reuses cfg258_preflight's generator and fits unchanged (the main run's seeds are NOT reused: seeds 6001.. below).  Reporting only: no decision of the main run depends on this file.
Cases (canonical footing, C0 design: N = 130, z ~ U[0.02, 0.09], 6 random points per galaxy, sigma_V/V = 0.07):
  FLAT truth, level 'off' (no shared draw) and level 'B';  E1 with the anchor at the TRUTH (no anchor error), E1 with a library anchor (as the main run), E2.
Quantities: median formal sigma_b; empirical SD of b-hat; their ratio; the fraction of mocks with a formal z = b-hat / sigma_formal above 3 and above 5 (a calibrated statistic gives 0.13 % and 0.00003 %);
the slope shift per unit z that a SHARED offset in the sample's log10 a0 of 0.02 dex would produce, in units of the formal sigma."""
import os, sys, json, math, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import cfg258_preflight as X

T0 = time.time()
LOG = []
def P(s=""):
    print(s, flush=True); LOG.append(str(s))

M = int(os.environ.get("CFG258_FORMAL_M", "1500"))
foot = "canonical"
th0 = math.log10(X.A0[foot])
cell = X.CELLS["C0"]
X.ANCHOR["canonical"] = X.anchor_library("canonical", X.NS_LIB)
lib = X.ANCHOR["canonical"]
P(f"CFG258 POST HOC: formal against empirical error of the fitted slope, cell C0 (canonical), FLAT truth, {M} mocks per level; seeds 6001 (off), 6002 (B)")
P(f"  anchor library: {lib.size} realizations, mean {lib.mean():+.4f} dex, sd {lib.std(ddof=1):.4f} dex")

RES = {}
for level, seed in ((None, 6001), ("B", 6002)):
    rng = np.random.default_rng(seed)
    b1t = np.empty(M); f1t = np.empty(M); b1l = np.empty(M); f1l = np.empty(M); b2 = np.empty(M); f2 = np.empty(M)
    for m_ in range(M):
        sh = X.draw_shared(rng, level)
        s = X.gen(X.POOL, rng, "M", foot, "FLAT", cell, sh=sh)
        thS = th0 + lib[rng.integers(len(lib))]
        r1t = X.fit(s, th0, "E1", theta_fixed=th0)               # anchor exactly at the truth
        r1l = X.fit(s, th0, "E1", theta_fixed=thS)               # anchor drawn from the library (as the main run)
        r2 = X.fit(s, th0, "E2")
        b1t[m_], f1t[m_], b1l[m_], f1l[m_], b2[m_], f2[m_] = r1t[1], r1t[2], r1l[1], r1l[2], r2[1], r2[2]
    nm = "off" if level is None else "B"
    RES[nm] = {}
    for key, b, f in (("E1 anchor at truth", b1t, f1t), ("E1 library anchor", b1l, f1l), ("E2 free theta, b", b2, f2)):
        ok = np.isfinite(b) & np.isfinite(f) & (f > 0)
        z = b[ok] / f[ok]
        d = dict(n=int(ok.sum()), mean_b=float(b[ok].mean()), sd_b=float(b[ok].std(ddof=1)), median_formal=float(np.median(f[ok])),
                 ratio_sd_over_formal=float(b[ok].std(ddof=1) / np.median(f[ok])), frac_z_gt3=float(np.mean(z > 3)), frac_z_gt5=float(np.mean(z > 5)), frac_abs_z_gt3=float(np.mean(np.abs(z) > 3)))
        RES[nm][key] = d
        P(f"  level {nm:3s} | {key:20s}: mean b-hat {d['mean_b']:+.2f}, SD {d['sd_b']:.2f}, median formal sigma {d['median_formal']:.2f} (SD / formal = {d['ratio_sd_over_formal']:.1f}); "
          f"formal z > 3: {100 * d['frac_z_gt3']:.1f} %, z > 5: {100 * d['frac_z_gt5']:.2f} %, |z| > 3: {100 * d['frac_abs_z_gt3']:.1f} %  (calibrated: 0.13 %, 0.00003 %, 0.27 %)")

# a shared offset d (dex) in the sample's log10 a0 shifts the E1 slope by about (10**d - 1) / z_eff; read the effective lever noiselessly (FLAT truth, an offset planted as a shared sample-mix offset tausel, lever R_sel = +1 dex per dex)
cell_d = X.design_cell(cell)
sh0 = dict(X.ZERO)
b_0 = X.nl_fit(cell, foot, "FLAT", sh0, "E1")
RES["lever"] = {}
for d in (0.01, 0.02, 0.035, 0.05, 0.116):
    sh = dict(X.ZERO); sh["tausel"] = d
    b_d = X.nl_fit(cell, foot, "FLAT", sh, "E1")
    RES["lever"][str(d)] = float(b_d - b_0)
f_med = RES["off"]["E1 anchor at truth"]["median_formal"]
P("")
P("  noiseless shift of the E1 slope (per unit z) for a shared offset d in the sample's log10 a0 (a 1,000-galaxy design, FLAT truth), and that shift in units of the median formal sigma of E1 (anchor at truth, no shared draw):")
for d, v in RES["lever"].items():
    P(f"     d = {float(d):.3f} dex: shift {v:+.2f} per unit z = {v / f_med:.1f} formal sigma")
P(f"  (the main run's E1 FLAT total scatter at level B was 5.07 per unit z; at level A 2.18; statistics only 1.54)")
RES["seconds"] = time.time() - T0
P(f"  ({RES['seconds']:.0f} s)")
json.dump(RES, open(os.path.join(HERE, "cfg258_posthoc_formal_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg258_posthoc_formal.out"), "w").write("\n".join(LOG) + "\n")
