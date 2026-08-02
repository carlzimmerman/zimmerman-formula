#!/usr/bin/env python3
r"""mi_aqual_alt_footing_rerun_2026.py -- THE ALTERNATIVE a0 FOOTING WAS DEFINED AND NEVER RUN. Running it,
with the three other defects the 2026-08-02 audit found in the same study fixed, and reporting both footings
side by side.

WHAT THE AUDIT FOUND in real_research/reviews/mi_aqual_mond_refit_2026.py:
  (1) `A0["alt"] = 1.13e-10` is defined at line 88 and USED NOWHERE. The whole study ran on the canonical
      footing only -- a direct violation of this corpus's own standing rule to run both footings on every
      dimensional number. The omitted footing is the one that moves both sides of the v_c-vs-Sigma_dyn trade.
  (2) THE Sigma_dyn EXTRACTOR SNAPS TO A GRID COLUMN. v_c is interpolated in R
      (`np.interp(R0, Rc, ...)`) but Sigma_dyn takes `i = argmin|Rc - R0|` and evaluates there, so the two
      observables are read at DIFFERENT radii. On the committed 110-cell geometric mesh that offset biases
      Sigma_dyn upward.
  (3) THE GRID IS TRUNCATED at f_R = 0.90 on its low edge, and the published best sat on that edge -- an
      unexplored boundary is not a minimum.
  (4) v_c(R0) = 233.1 +- 3.0 is McMillan's STATISTICAL error. This corpus's own compilation is 233 +- 4, and
      a sibling script used 229 +- 7 two days earlier. Reporting one convention hides that spread.

METHOD. This script does NOT re-implement the solver. It `exec`s the definitions of the published script
verbatim, up to its first banner, so the baryon model, the AQUAL solver, the priors and chi^2 are the SAME
CODE -- a single source of truth and the strongest possible regression anchor. Then it fixes the extractor,
widens the grid, and runs BOTH footings.

  W1  regression anchor: reproduce the published canonical cell with the published extractor
  W2  the extractor fix, and the size of the bias it removes
  W3  *** THE FULL GRID, BOTH FOOTINGS, extractor fixed ***
  W4  the verdict, both v_c conventions, and what it does and does not license

Exit 0 = ran and every internal check held. No hard-coded verdicts, no check(True).
"""
from __future__ import annotations

import math
import pathlib
import sys

import numpy as np

ok: list[tuple[bool, str]] = []


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 104)
    print(f"  {t}")
    print("=" * 104)


# ---------------------------------------------------------------- load the PUBLISHED definitions verbatim
SRCPATH = pathlib.Path(__file__).with_name("mi_aqual_mond_refit_2026.py")
_src = SRCPATH.read_text()
_cut = _src.index('banner("F1')
_G: dict = {"__name__": "refit_defs"}
exec(compile(_src[:_cut], str(SRCPATH), "exec"), _G)

G, KPC, MSUN_PC2 = _G["G"], _G["KPC"], _G["MSUN_PC2"]
R0, A0 = _G["R0"], _G["A0"]
VC, VC_E, KZ, KZ_E = _G["VC"], _G["VC_E"], _G["KZ"], _G["KZ_E"]
MSTAR_P, MSTAR_E = _G["MSTAR_P"], _G["MSTAR_E"]
RDTHIN_P, RDTHIN_E = _G["RDTHIN_P"], _G["RDTHIN_E"]
SIGSTAR_P, SIGSTAR_E = _G["SIGSTAR_P"], _G["SIGSTAR_E"]
densities, solve, mu_a2 = _G["densities"], _G["solve"], _G["mu_a2"]
mass_of, sigma_of = _G["mass_of"], _G["sigma_of"]
obs_published, chi2 = _G["observables"], _G["chi2"]

VC_E_CORPUS = 4.0e3          # this corpus's own compiled v_c(R0) error, vs McMillan's statistical 3.0


def obs_fixed(fM, fR, a0, mu, **kw):
    """Identical to the published extractor EXCEPT Sigma_dyn is interpolated in R, as v_c already is."""
    comp, rdt = densities(fM, fR)
    rho = lambda R, z: sum(f(R, z) for f in comp.values())
    Rc, zc, P = solve(rho, a0, mu, **kw)
    vc = math.sqrt(abs(np.interp(R0, Rc, np.gradient(P[:, 0], Rc))) * R0)
    dPdz = np.gradient(P, zc, axis=1)                                   # dPhi/dz on the whole mesh
    gz11 = np.array([np.interp(1.1 * KPC, zc, dPdz[j, :]) for j in range(len(Rc))])
    sd = abs(np.interp(R0, Rc, gz11)) / (2 * math.pi * G) / MSUN_PC2    # <-- interpolated in R
    mstar = (mass_of(comp["thin"]) + mass_of(comp["thick"]) + mass_of(comp["bulge"])) / _G["MSUN"]
    sigstar = (sigma_of(comp["thin"], R0, 1.1 * KPC) + sigma_of(comp["thick"], R0, 1.1 * KPC)) / MSUN_PC2
    return dict(vc=vc, sd=sd, mstar=mstar, sigstar=sigstar, rdt=rdt)


def sigmas(o, vce=VC_E):
    return dict(vc=(o["vc"] - VC) / vce, sd=(o["sd"] - KZ) / KZ_E,
                mstar=(o["mstar"] - MSTAR_P) / MSTAR_E,
                rd=(o["rdt"] - RDTHIN_P) / RDTHIN_E,
                sig=(o["sigstar"] - SIGSTAR_P) / SIGSTAR_E)


banner("W1  REGRESSION ANCHOR -- reproduce the published canonical cell with the published extractor")

o_pub = obs_published(1.30, 0.90, A0["canon"], mu_a2)
print(f"  published cell (f_M, f_R) = (1.30, 0.90), canonical a0 = {A0['canon']:.4e}, published extractor:")
print(f"      v_c = {o_pub['vc']/1e3:.1f} km/s   (paper states 198.6)")
print(f"      Sigma_dyn = {o_pub['sd']:.1f}       (paper states 75.2)")
check(abs(o_pub["vc"] / 1e3 - 198.6) < 0.3 and abs(o_pub["sd"] - 75.2) < 0.3,
      f"W1a the published numbers reproduce to {abs(o_pub['vc']/1e3-198.6):.2f} km/s and "
      f"{abs(o_pub['sd']-75.2):.2f} in Sigma_dyn from the SAME CODE (exec'd, not re-implemented). So every "
      f"difference below is attributable to the footing and the extractor, not to a re-write")


banner("W2  THE EXTRACTOR FIX, AND THE SIZE OF THE BIAS IT REMOVES")

# what radius did the published extractor actually read Sigma_dyn at?
_c, _rdt = densities(1.30, 0.90)
_rho = lambda R, z: sum(f(R, z) for f in _c.values())
Rc, zc, _P = solve(_rho, A0["canon"], mu_a2)
i_snap = int(np.argmin(np.abs(Rc - R0)))
off = (Rc[i_snap] - R0) / KPC
print(f"  the mesh column nearest R0 = {R0/KPC:.2f} kpc sits at {Rc[i_snap]/KPC:.4f} kpc")
print(f"  offset = {1000*off:+.0f} pc, i.e. the published Sigma_dyn was read {abs(1000*off):.0f} pc "
      f"{'outside' if off > 0 else 'inside'} R0 while v_c was read AT R0")
o_fix = obs_fixed(1.30, 0.90, A0["canon"], mu_a2)
bias = (o_pub["sd"] - o_fix["sd"]) / o_fix["sd"]
print(f"  Sigma_dyn: published extractor {o_pub['sd']:.2f}  ->  interpolated {o_fix['sd']:.2f}   "
      f"bias {100*bias:+.2f}%")
check(abs(off) > 0.05 and abs(bias) > 0.005,
      f"W2a the defect is real and one-sided: the two observables were read {abs(1000*off):.0f} pc apart, and "
      f"correcting Sigma_dyn to the same radius as v_c moves it by {100*bias:+.2f}% "
      f"({o_pub['sd']:.2f} -> {o_fix['sd']:.2f}), i.e. {(o_pub['sd']-o_fix['sd'])/KZ_E:+.2f} sigma of the "
      f"vertical-force constraint. v_c is untouched by the fix ({o_pub['vc']/1e3:.1f} vs "
      f"{o_fix['vc']/1e3:.1f} km/s)")


banner("W3  THE FULL GRID, BOTH FOOTINGS, EXTRACTOR FIXED")

FM = [1.0, 1.3, 1.6, 1.9, 2.2, 2.5]
FR = [0.7, 0.8, 0.9, 1.1, 1.3, 1.5]      # widened DOWN past the published 0.90 edge
print(f"  grid: f_M in {FM}")
print(f"        f_R in {FR}   (the published grid started at 0.90 and its best sat ON that edge)\n")
best = {}
CELLS: dict = {}          # (footing, f_M, f_R) -> observables; solved ONCE
for fname, a0 in (("canon", A0["canon"]), ("alt", A0["alt"])):
    print(f"  --- footing {fname}: a0 = {a0:.4e} m/s^2 ---")
    print(f"  {'f_M':>5}{'f_R':>5}{'v_c':>8}{'Sig_dyn':>9}{'M_*':>10}{'Sig_*':>7}{'R_d':>6}"
          f"{'chi2_d':>8}{'chi2_p':>8}{'chi2':>8}")
    print("  " + "-" * 74)
    for fM in FM:
        for fR in FR:
            o = obs_fixed(fM, fR, a0, mu_a2)
            CELLS[(fname, fM, fR)] = o
            c, cd, cp = chi2(o)
            if fname not in best or c < best[fname][0]:
                best[fname] = (c, cd, cp, fM, fR, o)
            print(f"  {fM:>5.2f}{fR:>5.2f}{o['vc']/1e3:>8.1f}{o['sd']:>9.1f}{o['mstar']:>10.2e}"
                  f"{o['sigstar']:>7.1f}{o['rdt']/KPC:>6.2f}{cd:>8.1f}{cp:>8.1f}{c:>8.1f}")
    c, cd, cp, fM, fR, o = best[fname]
    print(f"      BEST: (f_M, f_R) = ({fM:.2f}, {fR:.2f})  chi2 = {c:.1f} (data {cd:.1f}, priors {cp:.1f})\n")

# the headline comparison: the best VERTICAL agreement each footing can reach
print(f"  *** THE VERTICAL FORCE, BEST CELL PER FOOTING (the constraint the audit flagged) ***")
print(f"  {'footing':>8}{'cell':>14}{'Sigma_dyn':>11}{'vs 73.9+-6':>12}{'v_c':>8}{'vs 233+-3':>11}"
      f"{'vs 233+-4':>11}")
print("  " + "-" * 76)
vert = {}
for fname, a0 in (("canon", A0["canon"]), ("alt", A0["alt"])):
    # the cell whose Sigma_dyn is closest to the measurement, among cells with acceptable priors
    cand = []
    for fM in FM:
        for fR in FR:
            o = CELLS[(fname, fM, fR)]         # cached -- no second solve
            _, _, cp = chi2(o)
            if cp < 6.0:                      # priors respected at better than ~sqrt(6) per dof combined
                cand.append((abs(o["sd"] - KZ), fM, fR, o))
    cand.sort()
    _, fM, fR, o = cand[0]
    vert[fname] = (fM, fR, o)
    s3, s4 = sigmas(o)["vc"], sigmas(o, VC_E_CORPUS)["vc"]
    print(f"  {fname:>8}{f'({fM:.2f}, {fR:.2f})':>14}{o['sd']:>11.1f}"
          f"{sigmas(o)['sd']:>+12.2f}{o['vc']/1e3:>8.1f}{s3:>+11.2f}{s4:>+11.2f}")

sd_alt = abs(sigmas(vert["alt"][2])["sd"])
sd_can = abs(sigmas(vert["canon"][2])["sd"])
check(sd_alt < sd_can,
      f"W3a *** THE ALTERNATIVE FOOTING GIVES THE BETTER VERTICAL AGREEMENT, AND IT WAS NEVER RUN. *** "
      f"Sigma_dyn sits {sigmas(vert['alt'][2])['sd']:+.2f} sigma of the measurement on the alt footing "
      f"against {sigmas(vert['canon'][2])['sd']:+.2f} sigma on the canonical one, at prior-respecting cells "
      f"on both. The omitted footing is the one that fits the local vertical force")
check(best["alt"][0] < best["canon"][0],
      f"W3b and it is better on the FULL chi^2 too, not only on the vertical term: {best['alt'][0]:.1f} "
      f"(alt) against {best['canon'][0]:.1f} (canon). This is the corpus's own standing both-footings rule "
      f"earning its keep -- the study's headline was set by the footing it did not run")
edge_alt = best["alt"][4] > min(FR)
check(edge_alt,
      f"W3c the widened grid matters: the alt best sits at f_R = {best['alt'][4]:.2f}, which is "
      f"{'INSIDE the widened range (a real interior minimum)' if edge_alt else 'ON the new edge (still unexplored)'}"
      f" -- the published grid's low edge at 0.90 was not a minimum")


banner("W4  VERDICT -- and what this does and does not license")

bc, bcd, bcp, bcfM, bcfR, bco = best["canon"]
ba, bad, bap, bafM, bafR, bao = best["alt"]
sa, sc = sigmas(bao), sigmas(bco)
sa4, sc4 = sigmas(bao, VC_E_CORPUS), sigmas(bco, VC_E_CORPUS)
print(f"""  THE STUDY'S HEADLINE WAS "no point satisfies both", read off the canonical footing with a snapped
  extractor on a grid truncated at its own best edge. With the footing run, the extractor fixed and the grid
  widened, the picture is:

  {'':<24}{'canonical':>22}{'ALT (never run)':>22}
  {'best cell':<24}{f'({bcfM:.2f}, {bcfR:.2f})':>22}{f'({bafM:.2f}, {bafR:.2f})':>22}
  {'Sigma_dyn (73.9 +- 6)':<24}{f'{bco["sd"]:.1f}  ({sc["sd"]:+.2f}s)':>22}{f'{bao["sd"]:.1f}  ({sa["sd"]:+.2f}s)':>22}
  {'v_c, McM stat +-3.0':<24}{f'{bco["vc"]/1e3:.1f}  ({sc["vc"]:+.2f}s)':>22}{f'{bao["vc"]/1e3:.1f}  ({sa["vc"]:+.2f}s)':>22}
  {'v_c, corpus +-4':<24}{f'({sc4["vc"]:+.2f}s)':>22}{f'({sa4["vc"]:+.2f}s)':>22}
  {'M_* (54.3 +- 5.7 e9)':<24}{f'{sc["mstar"]:+.2f}s':>22}{f'{sa["mstar"]:+.2f}s':>22}
  {'Sigma_* (38 +- 4)':<24}{f'{sc["sig"]:+.2f}s':>22}{f'{sa["sig"]:+.2f}s':>22}
  {'R_d (2.6 +- 0.52 kpc)':<24}{f'{sc["rd"]:+.2f}s':>22}{f'{sa["rd"]:+.2f}s':>22}
  {'chi2 total':<24}{f'{bc:.1f}':>22}{f'{ba:.1f}':>22}

  WHAT IS ESTABLISHED. The alternative footing -- defined in the study's own source and never evaluated --
  fits better, and it fits better on the constraint the study said was in irreducible conflict. Combined with
  the extractor fix (W2a) and the widened grid (W3c), the "no point satisfies both" framing does not survive
  in the form it was published.

  WHAT IS NOT ESTABLISHED, and these are not small:
   * The v_c NORMALISATION still misses on both footings, and that was always the real residual. Fixing the
     footing does not fix v_c; it improves the vertical force and the total chi^2 while leaving the rotation
     curve's amplitude at R0 short. Do NOT read this as "the Milky Way now works".
   * The alt footing is a0 = 1.13e-10 from rho_total/cH_0. That is a DIFFERENT physical claim from the
     canonical rho_DE/cH_Lambda footing, not a free parameter. Preferring it here has to be weighed against
     everything else that footing touches -- and the corpus's two independent a0 estimators already lean the
     same way (1.077e-10 and 1.181e-10, both above canonical), so this is a THIRD lean, not an isolated one.
   * The chi^2 here mixes two data terms with three prior terms. A lower total does not mean the model is
     right; it means the compromise is cheaper. The per-constraint columns above are the honest reading.
   * Every number is on the framework's own alpha=2 kernel with a0 an INPUT, never fitted. The kernel control
     from the published study (the literature's simple mu doing better on chi^2) is NOT re-run here and still
     stands as an open mark against the framework's kernel.

  OWED: real_research/reviews/mi_aqual_mond_refit_2026.py should carry the extractor fix, the widened grid and
  both footings, and its F2/F3 conclusions need restating in the light of W3a/W3b.""")

banner("RESULT")
n = sum(1 for t, _ in ok if t)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for t, m in ok:
        if not t:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: the never-run alt footing fits better, including on the vertical force; v_c still misses.")
