#!/usr/bin/env python3
"""KL1R (FROZEN_CRITERIA.md 1792bd07ea): rows X0, X1, X2, X3, XALL for one survey (Legacy = Part B's B rows; DES = Part A's A rows on
DES Y3) and one footing, with KA2 / KB3, MA2, MA2b, MA3 (chi^2 part), MB1, MB2 (Legacy) and the BALL brackets.
Needs parts/nu_<foot>.json (kl1r_nu.py) and parts/gas.json (kl1r_gas.py).

  nice -n 15 python3 -I kl1r_grade.py Legacy canonical   -> parts/grade_Legacy_canonical.json
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing. Gravity-only S0 box; inherited halo list."""
import os, sys, json, time, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl1r_lib as K
import numpy as np
sv, ft = sys.argv[1], sys.argv[2]; assert sv in ("Legacy", "DES") and ft in ("canonical", "alt")
T0 = time.time(); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
S = K.load_legacy() if sv == "Legacy" else K.des()
RUN1 = K.run_of(K.ONE, K.S8E); PS0 = K.Pmat(RUN1, "S0"); fm = K.support_k(S, RUN1, PS0)
keep = S["pubkeep"] & (fm >= 0.9); D = K.subset(S, keep); N = D["N"]
ROWS = json.load(open(os.path.join(K.CO2D, "co2_rows.json"))); NU = json.load(open(os.path.join(K.HERE, "parts", f"nu_{ft}.json")))
GAS = json.load(open(os.path.join(K.HERE, "parts", "gas.json")))
s8_pin = ROWS["P2"][ft]["sigma8"]; s8_nu = NU["sigma8_target"]
Rt = K.HM["primary"][ft]["R_tot"]; Rg = GAS["R"][ft]["rta_ladder"]
P(f"KL1R {sv} [{ft}]: {N} points kept of {int(S['pubkeep'].sum())} published-kept ({len(S['rows'])} in the file); targets: CO2 pin {s8_pin:.4f}, neutrino refit {s8_nu:.4f} "
  f"(CMB cost {NU['cmb_cost']:+.2f})")
RES = dict(lane="KL1R", criteria="1792bd07ea", survey=sv, foot=ft, N=N, n_published_kept=int(S["pubkeep"].sum()), s8_pin=s8_pin, s8_nu=s8_nu, rows={}, brackets={}, MUTATE={},
           note="kappa = 1/2 FITTED; not theory closed; adopts nothing; gravity-only S0 box; inherited halo list")

def row(R, s8, cov=None, ia=True, gamma=2.0, mu=None, Dd=None):
    Pm = K.Pm_of(R, s8); Ci = ld = None
    if cov is not None:
        Ci, ld = cov.cinv(Pm, gamma)
        if Ci is None: return dict(sigma8=s8, not_pd=True)
    r = K.fit_any(S, D if Dd is None else Dd, Pm, ia=ia, Cinv=Ci, mu=mu)
    p = K.pval(r["chi2_data"], N)
    return dict(sigma8=s8, chi2=r["chi2"], chi2_data=r["chi2_data"], p=p, label=K.lab(p), A_IA=r["A_IA"], pulls=r["pulls"], lndet=ld)
def scan_of(R, cov=None, ia=True, mu=None, lndet=False):
    cache = {}
    def c2(g):
        rr = row(R, g, cov, ia=ia, mu=mu); cache[g] = rr
        return rr["chi2"] if not rr.get("not_pd") else 1e9
    sc = K.scan(c2)
    if lndet and cov is not None:
        gs = sorted(cache); v = np.array([cache[g]["chi2"] + cache[g]["lndet"] for g in gs]); sb, wid, _, i = K.parabola(np.array(gs), v)
        sc["with_lndet"] = dict(best=sb, width=wid, at_edge=bool(i in (0, len(gs) - 1)))
    return sc
def report(name, r, sc, target):
    gap = (target - sc["best"]) / sc["width"]; bst = row(*sc["_args"](sc["best"])) if "_args" in sc else None
    out = dict(**r, best_sigma8=sc["best"], width=sc["width"], gap_widths=gap, scan_at_edge=sc["at_edge"], scan=dict(grid=sc["grid"], chi2=sc["chi2"]))
    if bst is not None: out.update(dchi2_target_vs_best=r["chi2"] - bst["chi2"], pulls_at_best=bst["pulls"], p_at_best=bst["p"])
    if "with_lndet" in sc: out["with_lndet"] = sc["with_lndet"]
    RES["rows"][name] = out
    P(f"  {name:5s} sigma8 {r['sigma8']:.4f}: chi2 {r['chi2']:.2f} (data {r['chi2_data']:.2f}), p {r['p']:.3f} -> {r['label']}; best sigma8 {sc['best']:.4f} +- {sc['width']:.4f}"
      f"{' (EDGE)' if sc['at_edge'] else ''}; gap {gap:+.2f} widths; Delta chi2 {out.get('dchi2_target_vs_best', float('nan')):+.2f}; A_IA {r['A_IA']:.2f}; "
      f"pulls at target {np.round(r['pulls'], 2).tolist()}" + (f"; ln det scan best {sc['with_lndet']['best']:.4f} +- {sc['with_lndet']['width']:.4f}" if "with_lndet" in sc else "")
      + f"   [{time.time() - T0:.0f} s]")
    return out

# ---- X0, X1 (published covariance, R_tot)
sc0 = scan_of(Rt); sc0["_args"] = lambda g: (Rt, g)
r0 = row(Rt, s8_pin); report("X0", r0, sc0, s8_pin)
r1 = row(Rt, s8_nu); report("X1", r1, sc0, s8_nu)
best0 = sc0["best"]
# ---- the covariance at the model (fiducial: X0's best sigma8, R_tot)
cov = K.CovModel(S, K.Pm_of(Rt, best0), keep); RES["KA2"] = cov.ka2
k2 = cov.ka2
P(f"  KA2/KB3 at fiducial sigma8 {best0:.4f}: area {k2['area_deg2']:.1f} deg^2; (i) {k2['n_noise']} noise-dominated points"
  + (f", 16-84% {k2['i_p16']:.3f} to {k2['i_p84']:.3f}" if k2["i_eval"] else ", NOT EVALUABLE") + f" -> {k2['i_pass']}; (ii) {k2['n_signal']} signal-dominated points"
  + (f", median {k2['ii_median']:.3f}, min {k2['ii_min']:.3f}" if k2["ii_eval"] else ", NOT EVALUABLE") + f" -> {k2['ii_pass']}; (iii) median |dr| {k2['iii_median_abs_dr']:.3f}; KA2 {'PASS' if k2['pass_'] else 'FAIL'}")
Pfid = K.Pm_of(Rt, best0)
for nm, ns in (("MA2_halved", 0.5), ("MA2b_doubled", 2.0)):
    m = K.ka2(S, Pfid, nscale=ns); m = {a: b for a, b in m.items() if a not in ("G_area1", "N_area1")}
    m["bites"] = bool(m["ii_eval"] and m["ii_pass"] is False); RES["MUTATE"][nm] = m
    P(f"  {nm}: (i) {m['n_noise']} pts" + (f" {m['i_p16']:.3f}-{m['i_p84']:.3f} pass {m['i_pass']}" if m["i_eval"] else " NOT EVALUABLE") + f"; (ii) {m['n_signal']} pts"
      + (f" median {m['ii_median']:.3f} min {m['ii_min']:.3f} pass {m['ii_pass']}" if m["ii_eval"] else " NOT EVALUABLE") + f" -> {'bites' if m['bites'] else 'DOES NOT BITE'}")
# ---- X2 (covariance at the model, R_tot), X3 (gas, published), XALL
sc2 = scan_of(Rt, cov); sc2["_args"] = lambda g: (Rt, g, cov); r2 = row(Rt, s8_nu, cov); report("X2", r2, sc2, s8_nu)
sc3 = scan_of(Rg); sc3["_args"] = lambda g: (Rg, g); r3 = row(Rg, s8_nu); report("X3", r3, sc3, s8_nu)
scA = scan_of(Rg, cov, lndet=True); scA["_args"] = lambda g: (Rg, g, cov); rA = row(Rg, s8_nu, cov); report("ALL", rA, scA, s8_nu)
# ---- MUTATE
mb1 = row(Rg, 0.90, cov); RES["MUTATE"]["MB1_MP4"] = dict(**mb1, bites=bool(mb1["p"] < 0.0027))
P(f"  MB1 / MP4 sigma8 0.90 under ALL: chi2 {mb1['chi2']:.2f}, p {mb1['p']:.2e} -> {'bites' if mb1['p'] < 0.0027 else 'DOES NOT BITE'}")
Rm = GAS["R"][ft]["MA3_rta_0.2"]; ma3 = row(Rm, s8_nu); d3 = ma3["chi2"] - r1["chi2"]
RES["MUTATE"]["MA3_chi2"] = dict(chi2=ma3["chi2"], chi2_X1=r1["chi2"], dchi2=d3, bites=bool(abs(d3) >= 2), R_part_bites=GAS["MA3"][ft]["R_part_bites"])
P(f"  MA3 f_ret 0.2 at the X1 target: chi2 {ma3['chi2']:.2f} against {r1['chi2']:.2f} (Delta {d3:+.2f}, needs |.| >= 2) -> {'bites' if abs(d3) >= 2 else 'DOES NOT BITE'}; R part {'bites' if GAS['MA3'][ft]['R_part_bites'] else 'DOES NOT BITE'}")
if sv == "Legacy":
    K0 = K.load_k1000(); k_shift = K.SURV["KiDS"]["L"] @ K.SURV["KiDS"]["mu_u"]
    zbar = lambda SS: [float(np.sum(SS["zmid"] * n) / np.sum(n)) for n in SS["nz"]]
    zl, zk = zbar(S), zbar(K0); shifts = S["L"] @ S["mu_u"]; got = {}
    for i, z in enumerate(zk): got.setdefault(int(np.argmin(np.abs(np.array(zl) - z))), []).append(float(k_shift[i]))
    new = shifts.copy()
    for j, v in got.items(): new[j] = float(np.mean(v))
    muK = np.linalg.solve(S["L"], new)
    scB = scan_of(Rt, mu=muK); mv = (scB["best"] - best0) / sc0["width"]
    RES["MUTATE"]["MB2"] = dict(z_mean_legacy=zl, z_mean_k1000=zk, map={str(k): v for k, v in got.items()}, shifts_legacy=shifts.tolist(), shifts_new=new.tolist(), mu_new=muK.tolist(),
                                best=scB["best"], width=scB["width"], move_widths=mv, bites=bool(abs(mv) >= 0.5))
    P(f"  MB2 KiDS-1000 prior means (Legacy bin means z {np.round(zl, 3).tolist()}, K1000 {np.round(zk, 3).tolist()}; mapping {got}): best sigma8 {scB['best']:.4f} against {best0:.4f}: "
      f"move {mv:+.2f} widths (needs |.| >= 0.5) -> {'bites' if abs(mv) >= 0.5 else 'DOES NOT BITE'}")
# ---- brackets on ALL (reported)
br = {}
for g in (0.0, 3.0): br[f"gamma_{g:g}"] = row(Rg, s8_nu, cov, gamma=g)
for d_ in (-0.02, 0.02):
    cv = K.CovModel(S, K.Pm_of(Rt, best0 + d_), keep); br[f"fid_{d_:+.2f}"] = row(Rg, s8_nu, cv)
br["A5c1_alignment_off"] = row(Rg, s8_nu, cov, ia=False)
br["gas_edge_R200c"] = row(GAS["R"][ft]["r200c_ladder"], s8_nu, cov); br["gas_powerlaw_fret"] = row(GAS["R"][ft]["rta_powerlaw"], s8_nu, cov)
for nm, rel in K.A5A_RUNS.items():
    K.set_nodes(K.a5a_nodes(rel)); br[nm] = row(Rg, s8_nu, cov); K.set_nodes(K.PZ0)
for nm, b in br.items():
    P(f"  bracket {nm:22s}: chi2 {b['chi2']:.2f}, p {b['p']:.3f} -> {b['label']}")
sca = scan_of(Rg, cov, ia=False); br["A5c1_alignment_off"].update(best_sigma8=sca["best"], width=sca["width"], gap_widths=(s8_nu - sca["best"]) / sca["width"])
P(f"  A5c1 scan: best {sca['best']:.4f} +- {sca['width']:.4f}, gap {(s8_nu - sca['best']) / sca['width']:+.2f}")
RES["brackets"] = br
RES["runtime_s"] = time.time() - T0
json.dump(RES, open(os.path.join(K.HERE, "parts", f"grade_{sv}_{ft}.json"), "w"), indent=1, default=float)
open(os.path.join(K.HERE, "parts", f"grade_{sv}_{ft}.out"), "w").write("\n".join(OUT) + "\n"); P(f"done ({time.time() - T0:.0f} s)")
