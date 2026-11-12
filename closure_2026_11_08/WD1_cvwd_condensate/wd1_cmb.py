#!/usr/bin/env python3
"""WD1 gate G7 (FROZEN_CRITERIA.md 0cd6ef1dcb): primary CMB through F1A's machinery at CONSTANT weight. A fully clustered cold
component of amount f = 4.40 x omega_b on each footing's background (F1A's B2 best fit, omega_d = R omega_b with R 5.41): the
clustering part omega_c = 4.40 omega_b, the remainder (R - 4.40) omega_b a smooth c_s^2 = 1, w(a)-tabulated fluid carried with
Lambda (F1A G4: a c_s^2 = 1 component does not cluster; the same construction as PJ1's constant-weight grid). Raw Planck TT/TE/EE
bandpowers to ell 2500 (PJ1's CamSpec-NPIPE 12.6 reader, imported read-only), nuisances profiled; Delta chi^2 vs the F1A
constant-weight fit (w = 1) <= 10, before and after the 5-parameter refit (ob, od, lnA, ns, tau with h from F1A's footing closure;
the clustered amount held at 4.40 ob, od >= 4.40 ob). Reported beside: the proposal's own background (od = 4.40 ob exactly, no
smooth remainder) refitted over the other four parameters.
KA5: F1A's PA chi^2 at the B2 best fit is reproduced (|d| <= 3, PJ1 KA_C3), and the Planck-2500 chi^2 of CAMB's own lensed
spectra at w = 1 reproduces PJ1's recorded value (|d| <= 0.5).
    WD1_FOOT=canonical|alt python3 wd1_cmb.py  -> parts/cmb_<footing>.json (one footing per process, as PJ1)
kappa = 1/2 FITTED; not theory closed; footings never pooled; adopts nothing."""
import os, sys, json, math, time, gc
import numpy as np
from scipy.optimize import minimize
import wd1 as W
J = W.J; P = W.P
from pj1_cmb import CamSpec2500, LMAX_T, LMAX_LIKE, DL_BIN
FOOT_SEL = os.environ.get("WD1_FOOT")
REFIT_FEV = int(os.environ.get("WD1_REFIT_FEV", "150"))
PJ1_DIRECT = {"canonical": 1072.2293042795445, "alt": 1071.5108424755642}      # PJ1 KA_C5 direct_camb (parts/cmb_<f>.json), the record's Planck-2500 chi^2 at w = 1

def run_cmb(RES):
    import camb
    from camb.dark_energy import DarkEnergyFluid
    F1 = J.load_prefix(os.path.join(J.CL7, "F1A_primary_cmb_audit", "f1a.py"), "# ------------------------------------------------------------------ KA", "f1a_lib")
    TCMB, OMR, footing_h, camb_theory, PA = F1["TCMB"], F1["OMR"], F1["footing_h"], F1["camb_theory"], F1["PA"]
    LIK = CamSpec2500(F1["CS"]); P(f"Planck-2500 likelihood: {LIK.n} multipoles in {LIK.nb} bins of {DL_BIN}  [{time.time()-W.T0:.0f}s {W.rss():.2f}GB]")
    RES["likelihood"] = dict(ranges=LIK.RANGES, n_ell=LIK.n, n_bins=LIK.nb, dl=DL_BIN)
    def params(pr, w):
        """CAMB on the footing background: clustering omega_c = w omega_d; the smooth (1 - w) omega_d as a c_s^2 = 1 fluid with Lambda through a tabulated w(a)."""
        h, ob, od = pr["h"], pr["ob"], pr["oc"]; p = camb.CAMBparams()
        p.set_cosmology(H0=100 * h, ombh2=ob, omch2=max(w * od, 1e-7), tau=pr["tau"], mnu=0.0, num_massive_neutrinos=0, nnu=3.046, TCMB=TCMB)
        if w < 1.0:
            h2 = h * h; Os = od * (1.0 - w) / h2; OL = 1.0 - (ob + max(w * od, 1e-7)) / h2 - OMR / h2 - Os
            a = np.logspace(-8, 0, 600); wa = -OL / (OL + Os * a ** -3)
            de = DarkEnergyFluid(); de.set_w_a_table(a, wa); p.DarkEnergy = de
        p.InitPower.set_params(As=math.exp(pr["lnA"]) * 1e-10, ns=pr["ns"]); p.set_for_lmax(LMAX_T, lens_potential_accuracy=1); p.NonLinear = camb.model.NonLinear_none
        return p
    def lensed(pr, w):
        r = camb.get_results(params(pr, w)); c = r.get_total_cls(LMAX_T, CMB_unit="muK"); return {"tt": c[:, 0], "ee": c[:, 1], "te": c[:, 3]}
    for f in ([FOOT_SEL] if FOOT_SEL else W.FOOTS):
        R_ = {}; RES[f] = R_; fit = json.load(open(os.path.join(J.CL7, "F1A_primary_cmb_audit", "parts", f"fit_B2_{f}_cold.json"))); pr = dict(fit["pars"]); R = W.RF[f]
        R_["B2_best_fit"] = pr; R_["R_cmb"] = R; w_as = W.F_COSMIC * pr["ob"] / pr["oc"]; R_["w_as_written"] = w_as
        ka = {}
        g = PA(camb_theory(**pr)); ka["KA5a_f1a_PA_chi2_at_B2_best_fit"] = dict(PA=g["PA"], f1a=fit["chi2"]["PA"], d=g["PA"] - fit["chi2"]["PA"])
        F1["_L"].clear(); gc.collect()
        D1 = lensed(pr, 1.0); c_w1, nu1 = LIK.profile(D1)
        ka["KA5b_planck2500_chi2_w1"] = dict(mine=c_w1, pj1_direct=PJ1_DIRECT[f], d=c_w1 - PJ1_DIRECT[f])
        ka["pass_"] = bool(abs(ka["KA5a_f1a_PA_chi2_at_B2_best_fit"]["d"]) <= 3.0 and abs(ka["KA5b_planck2500_chi2_w1"]["d"]) <= 0.5)
        R_["KA"] = ka; P(f"[{f}] KA5: " + json.dumps(W.clean(ka)) + f"  [{time.time()-W.T0:.0f}s {W.rss():.2f}GB]")
        if not ka["pass_"]: P(f"[{f}] KA5 FAIL: stop"); continue
        R_["chi2_constant_weight_w1"] = c_w1
        # the as-written point: 4.40 omega_b clustered on the footing background, no refit
        D = lensed(pr, w_as); c_as, nu_as = LIK.profile(D, nu1); d_as = c_as - c_w1
        R_["as_written"] = dict(w=w_as, clustered_over_ob=W.F_COSMIC, smooth_over_ob=R - W.F_COSMIC, chi2=c_as, dchi2_norefit=d_as, status_norefit="PASS" if d_as <= 10 else "FAIL")
        P(f"[{f}] G7 as written (w {w_as:.4f}): dchi2 {d_as:+.1f} (no refit) -> {R_['as_written']['status_norefit']}  [{time.time()-W.T0:.0f}s {W.rss():.2f}GB]")
        W.dump(f"cmb_{f}_partial.json", RES)
        # refits (verify the fail as hard as a win): (1) 5 parameters, clustered amount held at 4.40 ob, od >= 4.40 ob; (2) the proposal's own background od = 4.40 ob, 4 parameters
        R_["refit"] = {}
        for tag, tied in (("five_parameter_footing_background", False), ("proposal_background_od_eq_4p4_ob", True)):
            lo = np.array([0.0215, 0.0, 1.5, 0.80, 0.01]); hi = np.array([0.0230, 0.40, 4.5, 1.30, 0.15]); state = dict(best=(1e99, None), n=0, x0=nu_as)
            def fun(x):
                xc = np.clip(x, lo, hi); ob = xc[0]; od = max(xc[1], W.F_COSMIC * ob) if not tied else W.F_COSMIC * ob
                pen = float(np.sum((x - xc) ** 2)) * 1e6 + (0.0 if tied else float(max(W.F_COSMIC * ob - xc[1], 0.0) ** 2) * 1e6)
                pr2 = dict(h=footing_h(f, ob, od), ob=ob, oc=od, lnA=xc[2], ns=xc[3], tau=xc[4]); w2 = W.F_COSMIC * ob / od
                try: c2, nu2 = LIK.profile(lensed(pr2, min(w2, 1.0)), state["x0"]); state["x0"] = nu2
                except Exception: c2 = 1e9
                state["n"] += 1
                if c2 + pen < state["best"][0]: state["best"] = (c2 + pen, dict(pr2, w=w2))
                if state["n"] % 10 == 0: P(f"[{f}]   refit {tag} eval {state['n']}: chi2 {c2:.1f} (best {state['best'][0]:.1f}) [{time.time()-W.T0:.0f}s {W.rss():.2f}GB]")
                return c2 + pen
            s = np.array([pr["ob"], pr["oc"] if not tied else W.F_COSMIC * pr["ob"], pr["lnA"], pr["ns"], pr["tau"]]); step = np.array([3e-4, 0.01 if not tied else 0.0, 0.05, 0.02, 0.02])
            simplex = [s] + [s + np.eye(5)[i] * step[i] for i in range(5) if step[i] > 0]
            if tied:   # 4 free parameters: Nelder-Mead over (ob, lnA, ns, tau) with od tied inside fun
                def fun4(y): return fun(np.array([y[0], W.F_COSMIC * y[0], y[1], y[2], y[3]]))
                s4 = np.array([pr["ob"], pr["lnA"], pr["ns"], pr["tau"]]); st4 = np.array([3e-4, 0.05, 0.02, 0.02]); sim4 = [s4] + [s4 + np.eye(4)[i] * st4[i] for i in range(4)]
                minimize(fun4, s4, method="Nelder-Mead", options=dict(initial_simplex=np.array(sim4), maxfev=REFIT_FEV, xatol=1e-5, fatol=0.05))
            else:
                minimize(fun, s, method="Nelder-Mead", options=dict(initial_simplex=np.array(simplex), maxfev=REFIT_FEV, xatol=1e-5, fatol=0.05))
            cb, xb = state["best"]; R_["refit"][tag] = dict(chi2_refit=cb, dchi2_refit=cb - c_w1, theta_refit=xb, nfev=state["n"], status="PASS" if cb - c_w1 <= 10 else "FAIL")
            P(f"[{f}] refit {tag}: dchi2 no-refit {d_as:+.1f} -> refit {cb - c_w1:+.1f} after {state['n']} evals -> {R_['refit'][tag]['status']}; theta {json.dumps(W.clean(xb))}")
            W.dump(f"cmb_{f}_partial.json", RES)
        R_["G7"] = dict(status=R_["refit"]["five_parameter_footing_background"]["status"], dchi2_norefit=d_as, dchi2_refit=R_["refit"]["five_parameter_footing_background"]["dchi2_refit"],
                        dchi2_refit_proposal_background=R_["refit"]["proposal_background_od_eq_4p4_ob"]["dchi2_refit"])
    RES["peak_rss_GB"] = W.rss(); RES["seconds"] = time.time() - W.T0; RES["criteria"] = W.CRIT; RES["note"] = W.NOTE; RES["refit_budget_evals"] = REFIT_FEV; RES["mutate"] = W.MUTATE
    W.dump(f"cmb_{FOOT_SEL if FOOT_SEL else 'both'}.json", RES)
    for f in ([FOOT_SEL] if FOOT_SEL else W.FOOTS):
        pp = os.path.join(W.PARTS, f"cmb_{f}_partial.json")
        if os.path.exists(pp): os.remove(pp)
    P(f"cmb done {RES['seconds']:.0f} s, peak RSS {RES['peak_rss_GB']:.2f} GB")

if __name__ == "__main__":
    P(f"WD1 cmb ({FOOT_SEL or 'both'}). Criteria {W.CRIT}. f {W.F_COSMIC} x omega_b clustered on the footing background (R {W.RF['canonical']:.4f} / {W.RF['alt']:.4f}). {W.NOTE}; footings never pooled; adopts nothing.")
    run_cmb({})
