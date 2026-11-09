"""PJ1 gate G7 (FROZEN_CRITERIA.md e3c9bc7d3c): the component's clustered weight at z 1100 is scale-dependent, w(k) = S(Phi(k))/R_cmb
with Phi(k) the linear (Weyl) potential at recombination, run through F1A's machinery (CAMB theory at F1A's B2 footing best fit,
own CamSpec-NPIPE reader) against raw Planck TT/TE/EE bandpowers to ell 2500. Delta chi^2 vs the constant-weight F1A fit <= 10.

Theory with a k-dependent clustering fraction: for a grid of constant weights w_i the CMB source transfer functions Delta_ell(k) are
computed with CAMB on the SAME background (omega_cdm = w omega_d clusters; the remaining (1 - w) omega_d is a smooth w = 0,
c_s^2 = 1 fluid carried in CAMB's dark-energy fluid together with Lambda through a tabulated w(a); F1A's G4 is the record's statement
that a c_s^2 = 1 component does not cluster). Each k mode of the linear theory evolves independently, so the gated spectrum is
C_ell = 4 pi int dln k Delta_ell^{w(k)}(k)^2 P_R(k) with Delta interpolated across the weight grid at w(k). Lensing by the w = 1
potential (camb.correlations). Known answers: the assembly at w = 1 reproduces CAMB's own unlensed and lensed spectra; F1A's PA
chi^2 at the B2 best fit is reproduced. Both footings separately. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, time, gc
import numpy as np
from scipy.optimize import minimize
from scipy.interpolate import CubicSpline
import pj1 as J

LMAX_T = 3500; LMAX_LIKE = 2500; DL_BIN = 10
W_GRID = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
PHS_CMB = sorted(set(J.PHS_GRID) | {1.5e-5, 1e-4, 3e-4})          # grid + the x10 KA-replay values
Z_REC = 1100.0
P = J.P
FOOT_SEL = os.environ.get("PJ1_FOOT")                 # one footing per process (parallel), merged by the grader
REFIT_FEV = int(os.environ.get("PJ1_REFIT_FEV", "40"))   # Nelder-Mead budget per refit (each evaluation is 11 CAMB runs)

class CamSpec2500:
    """Own binned CamSpec NPIPE 12.6 likelihood (F1A's reader, extended): TT 143x143 30-2000, 217x217 and 143x217 500-2500, TE and EE
    30-2000; bins of DL_BIN consecutive multipoles per spectrum; covariance B C B^T from the unified covariance; P-ACT foreground model
    (power-law residual per TT spectrum, calibrations), nuisances profiled with F1A's bounds and priors."""
    RANGES = {"143x143": (30, 2000), "217x217": (500, 2500), "143x217": (500, 2500), "TE": (30, 2000), "EE": (30, 2000)}
    SPEC_NAMES = ["100x100", "143x143", "217x217", "143x217", "TE", "EE"]
    def __init__(self, CS):
        rng = [l.split() for l in open(os.path.join(CS, "like_NPIPE_12.6_unified_data_ranges.txt"), encoding="utf-8-sig") if l.strip()]
        spectra = np.loadtxt(os.path.join(CS, "like_NPIPE_12.6_unified_spectra.txt"))
        off = 0; idx = []; self.blocks = []; data = []; starts = []; cnt = 0
        for name, lmn, lmx in rng:
            lmn, lmx = int(lmn), int(lmx); n = lmx - lmn + 1
            if name in self.RANGES:
                a, b = self.RANGES[name]; ells = np.arange(max(a, lmn), min(b, lmx) + 1)
                idx.append(off + ells - lmn); data.append(spectra[ells, self.SPEC_NAMES.index(name)])
                nb = int(math.ceil(len(ells) / DL_BIN)); st = cnt + np.arange(nb) * DL_BIN; starts.append(st)
                self.blocks.append((name, ells, cnt, nb)); cnt += len(ells)
            off += n
        self.nX = off; self.idx = np.concatenate(idx); self.n = len(self.idx); self.starts = np.concatenate(starts); self.nb = len(self.starts)
        d = np.concatenate(data); self.cnts = np.diff(np.concatenate([self.starts, [self.n]])).astype(float)
        self.d = np.add.reduceat(d, self.starts) / self.cnts
        # covariance: rows read by seeking (float32, no mapped pages held) and binned on the fly, so no n x n array is ever resident
        Cb = np.zeros((self.nb, self.n)); rowbin = np.searchsorted(self.starts, np.arange(self.n), side="right") - 1
        with open(os.path.join(CS, "like_NPIPE_12.6_unified_cov.bin"), "rb") as fh:
            for i, r_ in enumerate(self.idx):
                fh.seek(int(r_) * off * 4); Cb[rowbin[i]] += np.fromfile(fh, dtype=np.float32, count=off)[self.idx]
        Cb = np.add.reduceat(Cb, self.starts, axis=1) / (self.cnts[:, None] * self.cnts[None, :])
        self.Ci = np.linalg.inv(0.5 * (Cb + Cb.T)); self.ells_by_block = {name: ells for name, ells, _, _ in self.blocks}
    def model_vec(self, D, nu):
        Ap, a143, a217, a1x2, n143, n217, n1x2, cTE, cEE = nu
        amp = {"143x143": (a143, n143), "217x217": (a217, n217), "143x217": (a1x2, n1x2)}; out = []
        for name, ells, _, _ in self.blocks:
            if name in amp: a, t = amp[name]; m = (D["tt"][ells] + a * (ells / 1500.0) ** t) / Ap ** 2
            elif name == "TE": m = D["te"][ells] / (cTE * Ap ** 2)
            else: m = D["ee"][ells] / (cEE * Ap ** 2)
            out.append(m)
        m = np.concatenate(out); return np.add.reduceat(m, self.starts) / self.cnts
    def chi2(self, D, nu):
        r = self.d - self.model_vec(D, nu); return float(r @ self.Ci @ r)
    @staticmethod
    def prior(nu): return ((nu[0] - 1) / 0.0025) ** 2 + ((nu[7] - 1) / 0.01) ** 2 + ((nu[8] - 1) / 0.01) ** 2
    BOUNDS = [(0.9, 1.1), (0, 50), (0, 50), (0, 50), (0, 5), (0, 5), (0, 5), (0.9, 1.1), (0.9, 1.1)]
    X0 = np.array([1.0, 10.0, 20.0, 10.0, 1.0, 1.0, 1.0, 1.0, 1.0])
    def profile(self, D, x0=None):
        f = lambda x: self.chi2(D, x) + self.prior(x); best = None
        for s in ([x0] if x0 is not None else []) + [self.X0]:
            r = minimize(f, s, method="L-BFGS-B", bounds=self.BOUNDS, options=dict(maxiter=400))
            if best is None or r.fun < best.fun: best = r
        return float(best.fun), best.x

def run_cmb(RES):
    import camb
    from camb import correlations
    from camb.dark_energy import DarkEnergyFluid
    F1 = J.load_prefix(os.path.join(J.CL7, "F1A_primary_cmb_audit", "f1a.py"), "# ------------------------------------------------------------------ KA", "f1a_lib")
    TCMB, OMR, footing_h, camb_theory, PA = F1["TCMB"], F1["OMR"], F1["footing_h"], F1["camb_theory"], F1["PA"]
    LIK = CamSpec2500(F1["CS"]); P(f"Planck-2500 likelihood: {LIK.n} multipoles in {LIK.nb} bins of {DL_BIN}  [{time.time()-J.T0:.0f}s {J.rss():.2f}GB]")
    RES["likelihood"] = dict(ranges=LIK.RANGES, n_ell=LIK.n, n_bins=LIK.nb, dl=DL_BIN)
    def params(pr, w, lmax=LMAX_T, transfer=False):
        """CAMB params on F1A's background: clustering omega_c = w omega_d; smooth (1 - w) omega_d as a c_s^2 = 1, w(a)-tabulated fluid with Lambda."""
        h, ob, od = pr["h"], pr["ob"], pr["oc"]; p = camb.CAMBparams()
        p.set_cosmology(H0=100 * h, ombh2=ob, omch2=max(w * od, 1e-7), tau=pr["tau"], mnu=0.0, num_massive_neutrinos=0, nnu=3.046, TCMB=TCMB)
        if w < 1.0:
            h2 = h * h; Os = od * (1.0 - w) / h2; OL = 1.0 - (ob + max(w * od, 1e-7)) / h2 - OMR / h2 - Os
            a = np.logspace(-8, 0, 600); wa = -OL / (OL + Os * a ** -3)
            de = DarkEnergyFluid(); de.set_w_a_table(a, wa); p.DarkEnergy = de
        p.InitPower.set_params(As=math.exp(pr["lnA"]) * 1e-10, ns=pr["ns"])
        if transfer: p.set_matter_power(redshifts=[Z_REC], kmax=3.0); p.WantCls = False
        else: p.set_for_lmax(lmax, lens_potential_accuracy=1); p.NonLinear = camb.model.NonLinear_none
        return p
    def transfer_set(pr):
        """CMB source transfers Delta_ell(k) for each weight on W_GRID (same background), the w = 1 lensing potential and spectra."""
        out = []; q0 = None; extra = {}
        for w in W_GRID:
            p = params(pr, w); r = camb.get_results(p); td = r.get_cmb_transfer_data("scalar"); q = np.array(td.q); L = np.array(td.L, int); D = np.array(td.delta_p_l_k)
            if q0 is None: q0 = q; L0 = L
            elif not (len(q) == len(q0) and np.allclose(q, q0, rtol=1e-6)):
                D = np.array([[np.interp(np.log(q0), np.log(q), D[s, i]) for i in range(D.shape[1])] for s in range(D.shape[0])])
            out.append(D.astype(np.float32))          # transfers held in float32 (RSS < 1 GB); KA_C1/KA_C2 grade the assembly against CAMB at 5e-3
            if w == 1.0:
                extra["clpp"] = r.get_lens_potential_cls(LMAX_T)[:, 0]; extra["unlensed"] = r.get_unlensed_scalar_cls(LMAX_T, CMB_unit="muK"); extra["lensed"] = r.get_total_cls(LMAX_T, CMB_unit="muK")
                extra["PR"] = p.scalar_power(q0)
        return dict(q=q0, L=L0, D=np.array(out), **extra)
    def assemble(ts, wk):
        """C_ell^{TT,EE,TE} (unlensed, muK^2 D_ell) for the per-k clustered weight wk on ts['q']; Delta interpolated linearly across W_GRID."""
        Wg = np.array(W_GRID); wk = np.clip(wk, 0.0, 1.0); j = np.clip(np.searchsorted(Wg, wk) - 1, 0, len(Wg) - 2); t = (wk - Wg[j]) / (Wg[j + 1] - Wg[j])
        Dk = ts["D"][j, :, :, np.arange(len(wk))] * (1 - t)[:, None, None] + ts["D"][j + 1, :, :, np.arange(len(wk))] * t[:, None, None]   # (nk, nsrc, nL)
        Dk = np.moveaxis(Dk, 0, -1); lnq = np.log(ts["q"]); PR = ts["PR"]; L = ts["L"]
        def C(a, b): return 4 * math.pi * np.trapz(Dk[a] * Dk[b] * PR[None, :], lnq, axis=1)
        fac = L * (L + 1) / (2 * math.pi) * (TCMB * 1e6) ** 2; ell = np.arange(LMAX_T + 1); out = {}
        f2 = (L - 1.0) * L * (L + 1.0) * (L + 2.0)                     # CAMB's E transfer carries no sqrt((l+2)!/(l-2)!): EE x f2, TE x sqrt(f2)
        for key, (a, b, pf) in (("tt", (0, 0, 1.0)), ("ee", (1, 1, f2)), ("te", (0, 1, np.sqrt(f2)))):
            y = np.zeros(LMAX_T + 1); y[2:] = CubicSpline(L, C(a, b) * fac * pf)(ell[2:]); out[key] = y
        return out
    def lens(unl, clpp):
        cls = np.zeros((LMAX_T + 1, 4)); cls[:, 0] = unl["tt"]; cls[:, 1] = unl["ee"]; cls[:, 3] = unl["te"]
        lc = correlations.lensed_cls(cls, clpp[:LMAX_T + 1], lmax=LMAX_T); return {"tt": lc[:, 0], "ee": lc[:, 1], "te": lc[:, 3]}
    def phi_rms(pr, q):
        """Weyl potential rms per ln k at z 1100 on the w = 1 cosmology: sqrt(k^3 P_Weyl/(2 pi^2))/k^2 (CAMB's Weyl transfer is k^2 (phi+psi)/2)."""
        r = camb.get_results(params(pr, 1.0, transfer=True)); PK = r.get_matter_power_interpolator(var1="Weyl", var2="Weyl", nonlinear=False, hubble_units=False, k_hunit=False)
        kk = np.clip(q, 1.1e-4, 2.9); Pw = np.array([PK.P(Z_REC, float(k)) for k in kk]); return np.sqrt(kk ** 3 * Pw / (2 * math.pi ** 2)) / kk ** 2
    def weight(phi, q, PHS, p, R, RJ0=None, form=None, cut=None):
        w = J.S_of(phi, PHS, p, 1.0)
        if cut == "physical": w = w / (1.0 + (q * (1 + Z_REC) * J.RJ_of(phi, RJ0, PHS, p, form)) ** 4)     # R_J a proper length; k comoving
        elif cut == "comoving": w = w / (1.0 + (q * RJ0) ** 4)
        return w * (R / J.RF[FOOT_NOW[0]] if R is not None else 1.0)
    FOOT_NOW = [None]
    for f in ([FOOT_SEL] if FOOT_SEL else J.FOOTS):
        FOOT_NOW[0] = f; R_ = {}; RES[f] = R_; fit = json.load(open(os.path.join(J.CL7, "F1A_primary_cmb_audit", "parts", f"fit_B2_{f}_cold.json"))); pr = dict(fit["pars"])
        R_["B2_best_fit"] = pr; R_["R_cmb"] = J.RF[f]
        # known answers
        ka = {}
        g = PA(camb_theory(**pr)); ka["KA_C3_f1a_PA_chi2_at_B2_best_fit"] = dict(PA=g["PA"], f1a=fit["chi2"]["PA"], d=g["PA"] - fit["chi2"]["PA"])
        F1["_L"].clear(); gc.collect()                # F1A's Planck-2000 + ACT likelihood objects are only needed for KA_C3; freed (RSS < 1 GB)
        ts = transfer_set(pr); unl1 = assemble(ts, np.ones(len(ts["q"]))); len1 = lens(unl1, ts["clpp"])
        sl = slice(30, LMAX_LIKE + 1); ka["KA_C1_unlensed_assembly_vs_camb"] = dict(max_rel_tt=float(np.max(np.abs(unl1["tt"][sl] / ts["unlensed"][sl, 0] - 1))), max_rel_ee=float(np.max(np.abs(unl1["ee"][sl] / ts["unlensed"][sl, 1] - 1))))
        ka["KA_C2_lensed_assembly_vs_camb"] = dict(max_rel_tt=float(np.max(np.abs(len1["tt"][sl] / ts["lensed"][sl, 0] - 1))), max_rel_ee=float(np.max(np.abs(len1["ee"][sl] / ts["lensed"][sl, 1] - 1))))
        # fluid route check: w = 0.999 through the fluid vs Lambda at w = 1
        r999 = camb.get_results(params(pr, 0.999)).get_total_cls(LMAX_T, CMB_unit="muK"); ka["KA_C4_fluid_w0p999_vs_Lambda"] = dict(max_rel_tt=float(np.max(np.abs(r999[sl, 0] / ts["lensed"][sl, 0] - 1))))
        c_direct, _ = LIK.profile({"tt": ts["lensed"][:, 0], "ee": ts["lensed"][:, 1], "te": ts["lensed"][:, 3]}); c_w1, nu1 = LIK.profile(len1)
        ka["KA_C5_planck2500_chi2"] = dict(direct_camb=c_direct, assembled_w1=c_w1, d=c_w1 - c_direct, n_bins=LIK.nb)
        ka["pass_"] = bool(ka["KA_C1_unlensed_assembly_vs_camb"]["max_rel_tt"] <= 5e-3 and ka["KA_C2_lensed_assembly_vs_camb"]["max_rel_tt"] <= 5e-3 and abs(ka["KA_C3_f1a_PA_chi2_at_B2_best_fit"]["d"]) <= 3.0
                           and ka["KA_C4_fluid_w0p999_vs_Lambda"]["max_rel_tt"] <= 5e-3 and abs(ka["KA_C5_planck2500_chi2"]["d"]) <= 5.0)
        R_["KA"] = ka; P(f"[{f}] KA: " + json.dumps(J.clean(ka))[:600] + f"  [{time.time()-J.T0:.0f}s {J.rss():.2f}GB]")
        if not ka["pass_"]: P(f"[{f}] KA FAIL: stop"); continue
        R_["chi2_constant_weight"] = c_w1
        phi = phi_rms(pr, ts["q"]); q = ts["q"]
        R_["phi_rms_table"] = {f"{k:g}": float(np.interp(k, q, phi)) for k in (1e-3, 3e-3, 0.01, 0.02, 0.05, 0.1, 0.14, 0.2, 0.3, 0.5)}
        chis = r_results = None
        # the grid of (Phi_*, p) at the fixed B2 best fit, S-only (frozen G7 statistic); the as-written point with the reported variants
        grid = []
        for PHS in PHS_CMB:
            for p_ in J.P_GRID:
                wk = weight(phi, q, PHS, p_, None); D = lens(assemble(ts, wk), ts["clpp"]); c, _ = LIK.profile(D, nu1); d = c - c_w1
                row = dict(PHS=PHS, p=p_, dchi2=d, status="PASS" if d <= 10 else "FAIL", w_at_k={f"{k:g}": float(np.interp(k, q, wk)) for k in (0.01, 0.05, 0.1, 0.14, 0.2, 0.3)},
                           on_grid=PHS in J.PHS_GRID)
                grid.append(row); P(f"[{f}] G7 Phi_* {PHS:g} p {p_}: dchi2 {d:+.1f} -> {row['status']}; w(k) " + " ".join(f"{k}:{v:.2f}" for k, v in row["w_at_k"].items()) + f"  [{time.time()-J.T0:.0f}s {J.rss():.2f}GB]")
                R_["grid"] = grid; J.dump(f"cmb{'_' + FOOT_SEL if FOOT_SEL else ''}_partial.json", RES)
        asw = dict(PHS=J.ASW["PHS"], p=J.ASW["p"]); var = {}
        for form in J.FORMS:
            for cut in ("physical", "comoving"):
                wk = weight(phi, q, asw["PHS"], asw["p"], None, RJ0=J.ASW["RJ0"], form=form, cut=cut); D = lens(assemble(ts, wk), ts["clpp"]); c, _ = LIK.profile(D, nu1)
                var[f"form {form} k^4 cutoff {cut} R_J"] = dict(dchi2=c - c_w1, w_at_k={f"{k:g}": float(np.interp(k, q, wk)) for k in (0.01, 0.05, 0.1, 0.2, 0.3)})
        wk = weight(phi, q, asw["PHS"], asw["p"], J.R_ALT); D = lens(assemble(ts, wk), ts["clpp"]); c, _ = LIK.profile(D, nu1); var["R_cmb 4.4 reported (weight x 4.4/R)"] = dict(dchi2=c - c_w1, w_max=float(wk.max()))
        R_["as_written_variants_reported"] = var; P(f"[{f}] as-written variants: " + json.dumps(J.clean({k: v['dchi2'] for k, v in var.items()})))
        # refit (verify the fail as hard as a win): 5 cosmological parameters, Nelder-Mead, at the as-written gate and at the most favourable grid gate
        best_grid = min([r for r in grid if r["on_grid"]], key=lambda r: r["dchi2"])
        R_["refit"] = {}
        for tag, PHS, p_ in (("as_written", asw["PHS"], asw["p"]), ("most_favourable_grid", best_grid["PHS"], best_grid["p"])):
            d0 = [r for r in grid if r["PHS"] == PHS and r["p"] == p_][0]["dchi2"]
            if d0 <= 10: R_["refit"][tag] = dict(PHS=PHS, p=p_, skipped="no-refit dchi2 already <= 10", dchi2_norefit=d0); continue
            lo = np.array([0.0215, 0.0, 1.5, 0.80, 0.01]); hi = np.array([0.0230, 0.40, 4.5, 1.30, 0.15]); state = dict(best=(d0 + c_w1, None), n=0, x0=nu1)
            def fun(x):
                xc = np.clip(x, lo, hi); pen = float(np.sum((x - xc) ** 2)) * 1e6; pr2 = dict(h=footing_h(f, xc[0], xc[1]), ob=xc[0], oc=xc[1], lnA=xc[2], ns=xc[3], tau=xc[4])
                try:
                    ts2 = transfer_set(pr2); ph2 = phi_rms(pr2, ts2["q"]); wk2 = weight(ph2, ts2["q"], PHS, p_, None); D2 = lens(assemble(ts2, wk2), ts2["clpp"]); c2, nu2 = LIK.profile(D2, state["x0"]); state["x0"] = nu2
                except Exception as e: c2 = 1e9
                state["n"] += 1
                if c2 + pen < state["best"][0]: state["best"] = (c2 + pen, xc.tolist())
                if state["n"] % 10 == 0: P(f"[{f}]   refit {tag} eval {state['n']}: chi2 {c2:.1f} (best {state['best'][0]:.1f}) [{time.time()-J.T0:.0f}s {J.rss():.2f}GB]")
                return c2 + pen
            s = np.array([pr["ob"], pr["oc"], pr["lnA"], pr["ns"], pr["tau"]]); step = np.array([3e-4, 0.01, 0.05, 0.02, 0.02])
            simplex = [s] + [s + np.eye(5)[i] * step[i] for i in range(5)]
            minimize(fun, s, method="Nelder-Mead", options=dict(initial_simplex=np.array(simplex), maxfev=REFIT_FEV, xatol=1e-5, fatol=0.05))
            cb, xb = state["best"]; R_["refit"][tag] = dict(PHS=PHS, p=p_, dchi2_norefit=d0, chi2_refit=cb, dchi2_refit=cb - c_w1, theta_refit=xb, nfev=state["n"],
                                                             status="PASS" if cb - c_w1 <= 10 else "FAIL")
            P(f"[{f}] refit {tag}: dchi2 no-refit {d0:+.1f} -> refit {cb - c_w1:+.1f} after {state['n']} evals -> {R_['refit'][tag]['status']}")
            J.dump(f"cmb{'_' + FOOT_SEL if FOOT_SEL else ''}_partial.json", RES)
    RES["peak_rss_GB"] = J.rss(); RES["seconds"] = time.time() - J.T0; RES["criteria"] = J.CRIT; RES["note"] = J.NOTE; RES["W_GRID"] = W_GRID; RES["PHS_CMB"] = PHS_CMB
    RES["refit_budget_evals"] = REFIT_FEV; J.dump(f"cmb{'_' + FOOT_SEL if FOOT_SEL else ''}.json", RES)
    pp = os.path.join(J.PARTS, "cmb_partial.json")
    if os.path.exists(pp): os.remove(pp)
    P(f"cmb done {RES['seconds']:.0f} s, peak RSS {RES['peak_rss_GB']:.2f} GB")
