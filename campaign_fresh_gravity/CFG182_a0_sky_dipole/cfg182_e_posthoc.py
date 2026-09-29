#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG182 part E -- POST-HOC diagnostics, written AFTER parts A-D had run and their results were seen.  Nothing here is a
pass line or changes a verdict; every number is labelled post hoc.

E1  Why the MUTATE recovery was 0.15 rather than 0.20 (part B, M1 passed at the edge of its tolerance).  The same injection
    is applied at the curve level to (a) the real profile curves, (b) quadratic curves with the real centres and widths,
    (c) quadratic curves with every centre on the fitted model (no residuals), (d) quadratic curves all centred at one
    value (no dipole, no residuals); and the per-galaxy curve minima are compared with the injected shifts.
E2  The Hubble-flow subsample's best direction (part B: (259, 46)) lies near the CMB dipole: its amplitude along the CMB
    direction, with bootstrap sigma and a within-subsample permutation p, next to the independent-distance subsample.
E3  The galaxy-to-galaxy scatter of the per-galaxy a0 (part B: tau = 0.34 dex): the largest pulls, and the dipole with
    the ten largest-|pull| galaxies removed.
Run:  python3 campaign_fresh_gravity/CFG182_a0_sky_dipole/cfg182_e_posthoc.py
"""
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg182_common as C

if C.MUTATE:
    print("part E has no MUTATE mode (post-hoc diagnostics only)")
    sys.exit(0)
R = C.Run("cfg182_e_posthoc")
P, banner, check = R.P, R.banner, R.check
P(__doc__.split("Run:")[0].strip())
ST7 = [np.zeros(3)] + [0.3 * s * e for e in np.eye(3) for s in (1, -1)]
rng = np.random.default_rng(1850)
z = np.load(os.path.join(C.HERE, "cfg182_a_profiles.npz"))
zm = np.load(os.path.join(C.HERE, "cfg182_a_profiles_MUTATE.npz"))
sel = z["clean"]
g = z["grid"]
n = z["n"][sel]
fD = z["fD"][sel]
names = z["names"][sel]
cv = C.Curves(g, z["chi_nu_mono"][sel], z["npt"][sel])
cvm = C.Curves(g, zm["chi_nu_mono"][sel], zm["npt"][sel])
Dinj = zm["D_inj"]
A = lambda r: float(np.linalg.norm(r["theta"]))
bm = lambda k: rng.multinomial(k, np.full(k, 1.0 / k)).astype(float)

banner("E1  MUTATE RECOVERY ATTENUATION (post hoc)")
r0 = C.fit_template(cv, n, starts=ST7)
xm = r0["L"] + np.log10(1 + n @ r0["theta"])
cases = {"real curves, curve-level injection": cv,
         "quadratic, real centres and widths": C.Curves(g, (g[None, :] - cv.xhat[:, None]) ** 2 / cv.sig[:, None] ** 2, None,
                                                        birge=False),
         "quadratic, centres on the fitted model": C.Curves(g, (g[None, :] - xm[:, None]) ** 2 / cv.sig[:, None] ** 2, None,
                                                            birge=False),
         "quadratic, one centre (no dipole)": C.Curves(g, (g[None, :] + 9.95) ** 2 / cv.sig[:, None] ** 2, None, birge=False)}
E1 = {}
for lab, c in cases.items():
    a = C.fit_template(c, n, starts=ST7)
    b = C.fit_template(c, n, delta=np.log10(1 + n @ Dinj), starts=ST7)
    mv = b["theta"] - a["theta"]
    E1[lab] = {"amp": float(np.linalg.norm(mv)), "angle": C.angle_deg(mv, Dinj), "proj": float(mv @ Dinj / 0.2)}
    P(f"  {lab:42s} move {np.linalg.norm(mv):.4f} at {C.angle_deg(mv, Dinj):5.1f} deg (projection on the injected axis "
      f"{mv @ Dinj / 0.2:.4f})")
rpl = C.fit_template(cvm, n, starts=ST7)
mv = rpl["theta"] - r0["theta"]
P(f"  {'real curves, POINT-level injection (part B M1)':42s} move {np.linalg.norm(mv):.4f} at {C.angle_deg(mv, Dinj):5.1f} deg")
inj = np.log10(1 + n @ Dinj)
ok = (cv.xhat > g[0] + 0.01) & (cv.xhat < g[-1] - 0.01)
sl = np.polyfit(inj[ok], (cvm.xhat - cv.xhat)[ok], 1)[0]
P(f"  per-galaxy curve minima move by {sl:.3f} x the injected shift (slope over {ok.sum()} galaxies with interior minima)")
P("  reading: the per-galaxy injection is carried through the profiles almost exactly (slope ~1; point level ~ curve level);"
  "\n  the global fit returns ~0.77 of it because the multiplicative dipole log10(1 + D.n) is fitted to per-galaxy values that"
  "\n  scatter far beyond their widths (the second-order terms residual x d2 log(1 + D.n)/dD2 are not small); with no"
  "\n  residuals the recovery is exact.  The Neyman A95 of part B is built by injecting into the same over-dispersed real"
  "\n  curves, so it already includes this attenuation.")
R.num("E1", {**E1, "point_level": {"amp": float(np.linalg.norm(mv)), "angle": C.angle_deg(mv, Dinj)}, "min_shift_slope": sl})

banner("E2  HUBBLE-FLOW SUBSAMPLE vs THE CMB DIPOLE DIRECTION (post hoc)")
dcmb = C.unitvec(264.0, 48.3)
E2 = {}
for lab, idx in (("H f_D=1", np.where(fD == 1)[0]), ("I f_D=2,3,5", np.where(np.isin(fD, [2, 3, 5]))[0])):
    cs = cv.subset(idx)
    ns = n[idx]
    rf = C.fit_template(cs, ns, starts=ST7)
    a_c = float(C.fit_template(cs, (ns @ dcmb)[:, None])["theta"][0])
    s_c = float(np.std([C.fit_template(cs, (ns @ dcmb)[:, None], w=bm(len(idx)))["theta"][0] for _ in range(1000)]))
    nul_free = np.array([A(C.fit_template(cs, ns[rng.permutation(len(idx))])) for _ in range(2000)])
    nul_c = np.array([C.fit_template(cs, (ns[rng.permutation(len(idx))] @ dcmb)[:, None])["theta"][0] for _ in range(2000)])
    p_free = (1 + np.sum(nul_free >= A(rf))) / 2001
    p_c = (1 + np.sum(np.abs(nul_c) >= abs(a_c))) / 2001
    E2[lab] = {"A_free": A(rf), "lb_free": C.lb_of(rf["theta"]), "angle_to_cmb": C.angle_deg(rf["theta"], dcmb),
               "p_free": p_free, "A_cmb": a_c, "sig_cmb": s_c, "p_cmb_two_sided": p_c}
    P(f"  {lab:12s} N = {len(idx):3d}: free A = {A(rf):.3f} toward {tuple(round(v, 1) for v in C.lb_of(rf['theta']))} "
      f"({C.angle_deg(rf['theta'], dcmb):.1f} deg from the CMB dipole), within-subsample permutation p = {p_free:.3f}; "
      f"along the CMB direction A = {a_c:+.3f} +- {s_c:.3f}, two-sided permutation p = {p_c:.3f}")
P("  reading (post hoc): the Hubble-flow galaxies' best direction sits near our own motion relative to the CMB, which is"
  "\n  where a Hubble-distance frame error would put an a0 dipole (a0 ~ D^2 at fixed data); it is not significant in this"
  "\n  sample and it is absent from the TRGB/Cepheid/SNIa galaxies.  A hint to watch, not a finding.")
R.num("E2", E2)

banner("E3  GALAXY-TO-GALAXY SCATTER OF a0 and the dipole without the ten largest pulls (post hoc)")
L0 = C.fit_const(cv)["L"]
pull = (cv.xhat - L0) / cv.sig
o = np.argsort(-np.abs(pull))
P(f"  per-galaxy best log a0: MAD-sigma {1.4826 * np.median(np.abs(cv.xhat - np.median(cv.xhat))):.3f} dex vs median width "
  f"{np.median(cv.sig):.3f}; galaxies with |pull| > 3: {int(np.sum(np.abs(pull) > 3))}/{cv.N}")
P("  largest pulls: " + ", ".join(f"{names[i]} {pull[i]:+.1f} (f_D {fD[i]})" for i in o[:10]))
keep = np.sort(o[10:])
r_k = C.fit_template(cv.subset(keep), n[keep], starts=ST7)
nul = np.array([A(C.fit_template(cv.subset(keep), n[keep][rng.permutation(len(keep))])) for _ in range(2000)])
pk = (1 + np.sum(nul >= A(r_k))) / 2001
P(f"  without them: A = {A(r_k):.3f} toward {tuple(round(v, 1) for v in C.lb_of(r_k['theta']))}, permutation p = {pk:.3f}")
R.num("E3", {"mad_sigma": 1.4826 * np.median(np.abs(cv.xhat - np.median(cv.xhat))), "median_width": np.median(cv.sig),
             "n_pull_gt3": int(np.sum(np.abs(pull) > 3)), "top10": [[str(names[i]), float(pull[i]), int(fD[i])] for i in o[:10]],
             "A_without_top10": A(r_k), "lb_without_top10": C.lb_of(r_k["theta"]), "p_without_top10": pk})
check("E0 post-hoc diagnostics ran (no pass line here)", "done", True, load_bearing=False)
sys.exit(R.finish())
