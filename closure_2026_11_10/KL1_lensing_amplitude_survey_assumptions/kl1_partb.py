#!/usr/bin/env python3
"""KL1 PART B (FROZEN_CRITERIA_PARTB.md d26939ed4f, AMENDMENT_PB1 7787483300): KiDS-Legacy's raw xi+- through the same machinery
and gate, one footing. The release is untrusted data: this script lives in the lane, is run with python3 -I, and takes the
release folder as an argument. Nothing shipped in the release is executed; its .ini files are read as text.
  Generic KiDS-style loader (N bins, the release's own bins, cuts and decorrelated delta-z prior), checked on KiDS-1000 (KB2).
  Rows B0 (CO2's target) / B1 (A1's) / B2 (A2's covariance at the model) / B3 (A3's gas) / BALL = B1 + B2 + B3, and BALL with
  A5c1 (alignment off) and A5a (long modes); KB1-KB4; MUTATE MB1, MB2 -> parts/partb_<footing>_MUTATE.json.

  OMP_NUM_THREADS=1 nice -n 10 python3 -I kl1_partb.py <footing> <release folder>      (after Part A's rows)
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing. Gravity-only S0 box; inherited halo list in R."""
import os, sys, json, math, time, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import astropy.io.fits as fits
import kl1_lib as K1
FT, REL = sys.argv[1], os.path.abspath(sys.argv[2]); assert FT in K1.FOOTS
T0 = time.time(); LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)
G, SURV = K1.G, K1.SURV

# ------------------------------------------------------------------ the generic KiDS-style loader and nuisances
def load_generic(name, fn, e_lo, e_hi, cut_p, cut_m, Lchol, mu_u):
    F = fits.open(fn); cov = np.array(F["COVMAT"].data, float); nzt = F["NZ_SOURCE"].data; hd = F["NZ_SOURCE"].header
    rows = [(s, int(r["BIN1"]), int(r["BIN2"]), int(r["ANGBIN"]), float(r["ANG"]), float(r["VALUE"])) for s, ext in (("+", "xiP"), ("-", "xiM")) for r in F[ext].data]
    nb = int(F["xiP"].header["N_ZBIN_1"]); e = np.geomspace(e_lo, e_hi, int(F["xiP"].header["N_ANG"]) + 1)
    keep = np.array([(cut_p[0] <= r[4] <= cut_p[1]) if r[0] == "+" else (cut_m[0] <= r[4] <= cut_m[1]) for r in rows])
    S = dict(name=name, generic=True, cov=cov, rows=rows, pubkeep=keep, zmid=np.array(nzt["Z_MID"], float), nz=[np.array(nzt[f"BIN{i+1}"], float) for i in range(nb)],
             nbin=nb, edges=list(zip(e[:-1], e[1:])), angbin0=min(r[3] for r in rows), L=Lchol, mu_u=np.asarray(mu_u, float),
             sig_e=np.array([hd[f"SIG_E_{i+1}"] for i in range(nb)], float), ngal=np.array([hd[f"NGAL_{i+1}"] for i in range(nb)], float))
    S["Hp"], S["Hm"], S["Ap"], S["Am"] = G["hankel"](S["edges"])     # as CFG592's survey loop
    S["pairs"] = [(a, b) for a in range(1, nb + 1) for b in range(a, nb + 1)]; pid = {p: i for i, p in enumerate(S["pairs"])}
    S["ip_all"] = np.array([pid[(min(r[1], r[2]), max(r[1], r[2]))] for r in rows]); S["ia_all"] = np.array([r[3] - S["angbin0"] for r in rows])
    S["isp_all"] = np.array([r[0] == "+" for r in rows]); S["b1_all"] = np.array([r[1] for r in rows]) - 1; S["b2_all"] = np.array([r[2] for r in rows]) - 1
    S["d_all"] = np.array([r[5] for r in rows]); S["Jp_raw"], S["Jm_raw"], S["Om_bin"] = K1._jbar(S)
    return S
_orig_spec = G["nuis_spec"]
def nuis_spec_gen(S, widen, ia):
    if not S.get("generic"): return _orig_spec(S, widen, ia)
    nb = S["nbin"]; mu = S["mu_u"]
    x0 = np.r_[mu, 0.5 if ia else 0.0]; lo = np.r_[mu - 5 * widen, -6.0 if ia else 0.0]; hi = np.r_[mu + 5 * widen, 6.0 if ia else 0.0]
    unpack = lambda x: dict(dz=S["L"] @ x[:nb], A=float(x[nb])); prior = lambda x: float(np.sum(((x[:nb] - mu) / widen) ** 2))
    return x0, lo, hi, unpack, prior
G["nuis_spec"] = nuis_spec_gen                                  # support_mask, C_ell helpers and K1.fit look it up here
def register(S):
    SURV[S["name"]] = S; K1.SUP[S["name"]] = K1.support_mask(S, K1.RUN1, K1.PS0)
    K1.SUP_HALF[S["name"]] = K1.support_mask(S, dict(K1.RUN1, k_hi=K1.RUN1["k_hi"] / 2), K1.PS0)
def pulls(S, x, widen=1.0): return [float(v) for v in (np.asarray(x[:S["nbin"]]) - S["mu_u"]) / widen]

# KiDS-1000 through the generic loader (KB2)
import glob
_k = SURV["KiDS"]; _kfn = glob.glob(os.path.join(G["WORK"], "kids", "*", "data_fits", "xipm_KIDS1000_*.fits"))[0]
K1G = load_generic("K1000gen", _kfn, 0.5, 300.0, (0.5, 300.0), (4.0, 300.0), _k["L"], _k["mu_u"])
register(K1G)
# KiDS-Legacy (AMENDMENT_PB1 items 1-5)
ini = open(os.path.join(REL, "chains_and_config_files", "xipm", "KiDS_Legacy_priors.ini")).read()
MU_LEG = [float(re.search(rf"uncorr_bias_{i}\s*=\s*gaussian\s+(\S+)\s+1\.0", ini).group(1)) for i in range(1, 7)]
NZC = np.loadtxt(os.path.join(REL, "data", "Nz_covariance.txt")); L_LEG = np.linalg.cholesky(NZC)
LEG = load_generic("Legacy", os.path.join(REL, "data", "KiDS_Legacy_xipm.fits"), 2.0, 300.0, (2.0, 300.0), (4.0, 300.0), L_LEG, MU_LEG)
register(LEG)

# ------------------------------------------------------------------ inputs from Part A
HM, ROWS = K1.HM, K1.ROWS
NU = json.load(open(os.path.join(HERE, "kl1_nu.json"))); GAS = json.load(open(os.path.join(HERE, "kl1_gas.json")))
PA = json.load(open(os.path.join(HERE, "parts", f"rows_{FT}.json")))
S8_CO2 = ROWS["P2"][FT]["sigma8"]; S8_NU = NU["A1"][FT]["sigma8_nu"]
R = dict(co1=np.array(HM["primary"][FT]["R_tot"]), gas_rta=np.array(GAS["rows"][FT]["rta_table"]["R_tot"]))
K, PZ0 = K1.K, K1.PZ0
def load200(rel):
    J2 = json.load(open(os.path.join(G["EXT"], *rel))); S2 = J2["snap"]; k2 = np.array(S2["z0"]["k"]); out = {}
    for z, key in ((0.0, "z0"), (0.5, "z0.5"), (1.0, "z1")):
        p2 = np.exp(np.interp(np.log(K), np.log(k2), np.log(np.array(S2[key]["P"])))); m = (K >= 0.5) & (K <= 1.0) & (K <= k2[-1]); med = float(np.median(p2[m] / PZ0[z][m]))
        o = PZ0[z].copy(); lo = K < 0.5; o[lo] = p2[lo]; o[~lo] = o[~lo] * med; out[z] = o
    return out
PZV = {None: PZ0, "A5a": load200(("cfg411_work", "cfg411_S0_Rc3_MIXA_FLAT_canonical_N512.json"))}
def Pm_of(Rk, s8, pz):
    K1.setP(PZV[pz]); return K1.Pmat(K1.run_of(Rk, (s8 / K1.S8E) ** 2, "resp"), "F")

# ------------------------------------------------------------------ A2 machinery (copied from kl1.py, unchanged)
CTX = {}
def make_ctx(sn, s8_fid, area=None):
    S = SURV[sn]; pub = np.where(S["pubkeep"])[0]
    Pm = Pm_of(R["co1"], s8_fid, None); C = K1.cell_full(S, Pm)
    G1, N1 = K1.gauss_cov(S, pub, C); Cp = S["cov"][np.ix_(pub, pub)]
    dg, dn, dp = np.diag(G1), np.diag(N1), np.diag(Cp); nf = dn / dg
    if area is None:
        nd = nf >= 0.8; area = float(1.0 / np.median(dp[nd] / dg[nd])) if nd.sum() else float("nan")
    Gf = G1 / area; ratio = dp / np.diag(Gf); xi = K1.xi_nominal(S, Pm)
    return dict(pub=pub, pos={int(g): i for i, g in enumerate(pub)}, area=area, R=Cp - Gf, xi_fid=xi, ratio=ratio, nfrac=nf, s8_fid=s8_fid, Gf=Gf, Cp=Cp)
def ka2(ctx):
    nd = ctx["nfrac"] >= 0.8; sd = ctx["nfrac"] < 0.5; r = ctx["ratio"]
    out = dict(n_noise=int(nd.sum()), n_signal=int(sd.sum()), area_sr=ctx["area"], area_deg2=ctx["area"] * (180 / math.pi) ** 2)
    if nd.sum() >= 5:
        q16, q84 = np.percentile(r[nd], [16, 84]); out.update(i_q16=float(q16), i_q84=float(q84), i_pass=bool(q16 >= 0.85 and q84 <= 1.15))
    else: out.update(i_pass=None)
    if sd.sum() >= 5:
        out.update(ii_median=float(np.median(r[sd])), ii_min=float(np.min(r[sd])), ii_pass=bool(0.95 <= np.median(r[sd]) <= 1.6 and np.min(r[sd]) >= 0.80))
    else: out.update(ii_pass=None)
    out["pass_"] = bool(out["i_pass"] is True and out["ii_pass"] is True)
    return out
def cov_model(sn, ctx, Pm, kmask, gamma):
    S = SURV[sn]; kept = np.where(kmask)[0]; kp = np.array([ctx["pos"][int(g)] for g in kept])
    G1, _ = K1.gauss_cov(S, kept, K1.cell_full(S, Pm)); xi = K1.xi_nominal(S, Pm)
    s = np.clip(xi[kept] / ctx["xi_fid"][kept], 0.5, 3.0)
    C = G1 / ctx["area"] + ctx["R"][np.ix_(kp, kp)] * np.outer(s, s) ** (gamma / 2.0)
    try: Lc = np.linalg.cholesky(C)
    except np.linalg.LinAlgError: return None, None
    return np.linalg.inv(C), float(2 * np.sum(np.log(np.diag(Lc))))
def run_row(sn, st):
    S = SURV[sn]; kmask = K1.keep_mask(sn, 0.9, False); D = K1.subset(S, kmask)
    Rk, pz, cv = R[st["R"]], st.get("pz"), st.get("cov")
    def ev(s8):
        Pm = Pm_of(Rk, s8, pz); Ci, ld = (None, None)
        if cv is not None:
            Ci, ld = cov_model(sn, CTX[sn], Pm, kmask, cv)
            if Ci is None: return dict(chi2=float("nan"), p=float("nan"), not_pd=True)
        r = K1.fit(S, D, Pm, ia=st.get("ia", "nla"), Cinv=Ci); r["dz_pulls"] = pulls(S, r["x"])
        if ld is not None: r["logdet"] = ld
        return r
    tgt = st["s8"]; out = dict(settings=dict(st), N=D["N"], target_sigma8=tgt); main = ev(tgt); out["at_target"] = main
    if main.get("not_pd"): out["label"] = "NO VERDICT (covariance not positive definite)"; return out
    out["label"] = main["label"]
    if st.get("scan", True):
        cache = {}
        def evc(s):
            k = round(s, 6)
            if k not in cache: cache[k] = ev(s)
            return cache[k]
        sc = K1.scan(evc); best = ev(sc["best_sigma8"])
        out.update(scan=sc, best=best, best_sigma8=sc["best_sigma8"], width=sc["width"], gap_widths=(tgt - sc["best_sigma8"]) / sc["width"], dchi2_target_vs_best=main["chi2"] - best["chi2"])
        if cv is not None:
            ss = np.array(sorted(cache)); c2 = np.array([cache[s]["chi2"] + cache[s]["logdet"] for s in ss]); i = int(np.argmin(c2))
            lo_, hi_ = max(i - 2, 0), min(i + 3, len(ss)); co = np.polyfit(ss[lo_:hi_], c2[lo_:hi_], 2)
            sb = float(-co[1] / (2 * co[0])) if co[0] > 0 else float(ss[i]); wd = 1 / math.sqrt(co[0]) if co[0] > 0 else float("nan")
            out["with_logdet"] = dict(best_sigma8=sb, width=wd, gap_widths=(tgt - sb) / wd)
    return out
def show(name, sn, o):
    m = o["at_target"]
    if m.get("not_pd"): P(f"  {name:10s} {sn}: covariance NOT positive definite -> NO VERDICT"); return
    s = f"  {name:10s} {sn}: sigma8 {o['target_sigma8']:.4f}: chi2 {m['chi2']:.2f} (data {m['chi2_data']:.2f}, N {m['N']}), p {m['p']:.2e} -> {m['label']}"
    if "best_sigma8" in o:
        s += f"; best {o['best_sigma8']:.4f} +- {o['width']:.4f} (p {o['best']['p']:.3f}), gap {o['gap_widths']:+.2f} widths, Delta chi2 {o['dchi2_target_vs_best']:+.2f}" + (" [EDGE]" if o["scan"]["edge_hit"] else "")
    if "with_logdet" in o: s += f"; with ln det: best {o['with_logdet']['best_sigma8']:.4f}, gap {o['with_logdet']['gap_widths']:+.2f}"
    s += "; dz pulls " + " ".join(f"{v:+.2f}" for v in m["dz_pulls"]) + f"   [{time.time() - T0:.0f} s]"; P(s)

# ------------------------------------------------------------------ run
RES = dict(lane="KL1", part="B", criteria="d26939ed4f", amendment_PB1="7787483300", foot=FT, note="kappa = 1/2 FITTED; not theory closed; adopts nothing; gravity-only S0; inherited halo list in R",
           target_sigma8=dict(CO2=S8_CO2, A1=S8_NU), N_kept=dict(Legacy=int(K1.keep_mask("Legacy").sum()), K1000gen=int(K1.keep_mask("K1000gen").sum())), KB={}, rows={})
MUTR = dict(lane="KL1", part="B MUTATE", foot=FT, note="kappa = 1/2 FITTED; not theory closed", arms={})
P(f"KL1 PART B [{FT}]: KiDS-Legacy xi+- ({len(LEG['rows'])} points, {LEG['nbin']} bins; {int(LEG['pubkeep'].sum())} inside the published cuts; {RES['N_kept']['Legacy']} kept by the support cut). "
  f"Targets: CO2 {S8_CO2:.4f}; neutrino floor {S8_NU:.4f}.")
# KB1
sums = [float(np.sum(n)) for n in LEG["nz"]]; beyond = [float(np.sum(n[LEG["zmid"] > 3.5]) / np.sum(n)) for n in LEG["nz"]]
pd_ = bool(np.all(np.linalg.eigvalsh(LEG["cov"]) > 0)); n_ok = bool(len(LEG["rows"]) == 378 and LEG["cov"].shape == (378, 378) and LEG["nbin"] == 6 and len(LEG["pairs"]) == 21)
RES["KB"]["KB1"] = dict(points=len(LEG["rows"]), bins=LEG["nbin"], cov_pd=pd_, nz_sums=sums, nz_beyond_3p5=beyond, mu_u=MU_LEG, dz_prior_mean_shift=(L_LEG @ np.array(MU_LEG)).tolist(),
                        pass_=bool(n_ok and pd_ and all(abs(s - 1) <= 0.01 for s in sums)))
P(f"  KB1 loader: {len(LEG['rows'])} points, {LEG['nbin']} bins, covariance positive definite {pd_}; n(z) weights sum to " + ", ".join(f"{s:.4f}" for s in sums)
  + f"; beyond z 3.5: " + ", ".join(f"{b:.1e}" for b in beyond) + f"; prior-mean shifts in z " + " ".join(f"{v:+.4f}" for v in L_LEG @ np.array(MU_LEG))
  + f" -> {'PASS' if RES['KB']['KB1']['pass_'] else 'FAIL'}")
# KB2: Part A's KA0 through the generic loader on KiDS-1000
D2 = K1.subset(K1G, K1.keep_mask("K1000gen")); r2 = K1.fit(K1G, D2, Pm_of(R["co1"], S8_CO2, None)); ref = dict(canonical=157.89, alt=159.35)[FT]
RES["KB"]["KB2"] = dict(chi2=r2["chi2"], ref=ref, N=D2["N"], pass_=bool(abs(r2["chi2"] - ref) <= 0.01 and D2["N"] == 104))
P(f"  KB2 KiDS-1000 through the generic loader at CO2's target: chi2 {r2['chi2']:.3f} (CO2 {ref}), N {D2['N']} -> {'PASS' if RES['KB']['KB2']['pass_'] else 'FAIL'}")
SPEC = [("B0", dict(s8=S8_CO2, R="co1")), ("B1", dict(s8=S8_NU, R="co1")), ("B2", dict(s8=S8_NU, R="co1", cov=2.0)), ("B3", dict(s8=S8_NU, R="gas_rta")),
        ("BALL", dict(s8=S8_NU, R="gas_rta", cov=2.0)), ("BALL_A5c1", dict(s8=S8_NU, R="gas_rta", cov=2.0, ia="off")), ("BALL_A5a", dict(s8=S8_NU, R="gas_rta", cov=2.0, pz="A5a"))]
for name, st in SPEC:
    if st.get("cov") is not None and "Legacy" not in CTX:
        CTX["Legacy"] = make_ctx("Legacy", RES["rows"]["B0"]["best_sigma8"]); k = ka2(CTX["Legacy"]); RES["KB"]["KB3"] = k
        P(f"  KB3 Legacy covariance: fiducial sigma8 {CTX['Legacy']['s8_fid']:.4f}; area {k['area_deg2']:.1f} deg^2 (Wright et al. quote 967.4, context); (i) 16-84 % "
          f"{k.get('i_q16', float('nan')):.3f}-{k.get('i_q84', float('nan')):.3f} -> {k['i_pass']}; (ii) median {k.get('ii_median', float('nan')):.3f}, min {k.get('ii_min', float('nan')):.3f} -> {k['ii_pass']}"
          f" -> {'PASS' if k['pass_'] else 'FAIL'}")
    RES["rows"][name] = run_row("Legacy", st); show(name, "Legacy", RES["rows"][name])
    json.dump(RES, open(os.path.join(HERE, "parts", f"partb_{FT}.json"), "w"), indent=1, default=float)
a0 = PA["rows"]["A0"]["KiDS"]; b0 = RES["rows"]["B0"]
RES["KB"]["KB4"] = dict(KiDS1000_best=a0["best_sigma8"], KiDS1000_width=a0["width"], Legacy_best=b0["best_sigma8"], Legacy_width=b0["width"], published_Legacy_S8="0.815 +0.016 -0.021 (Wright et al. 2025; context)")
P(f"  KB4 (context): best sigma8 for form B's spectrum: KiDS-1000 {a0['best_sigma8']:.4f} +- {a0['width']:.4f}; KiDS-Legacy {b0['best_sigma8']:.4f} +- {b0['width']:.4f} "
  f"(shift {(b0['best_sigma8'] - a0['best_sigma8']) / a0['width']:+.2f} KiDS-1000 widths); Legacy's published S8 0.815 +0.016 -0.021")
# MUTATE
o = run_row("Legacy", dict(s8=0.90, R="gas_rta", cov=2.0, scan=False)); MUTR["arms"]["MB1"] = dict(**o["at_target"], bites=bool(o["at_target"]["p"] < 0.0027))
P(f"  MB1 (MUTATE) BALL at sigma8 0.90: chi2 {o['at_target']['chi2']:.2f}, p {o['at_target']['p']:.2e} -> {'bites' if o['at_target']['p'] < 0.0027 else 'DOES NOT BITE'}")
k1000_shift = _k["L"] @ _k["mu_u"]; zm_k = [float(np.sum(n * _k["zmid"]) / np.sum(n)) for n in _k["nz"]]; zm_l = [float(np.sum(n * LEG["zmid"]) / np.sum(n)) for n in LEG["nz"]]
mapped = np.array([k1000_shift[int(np.argmin([abs(a - b) for a in zm_k]))] for b in zm_l]); mu_alt = np.linalg.solve(L_LEG, mapped)
mu_keep = LEG["mu_u"].copy(); LEG["mu_u"] = mu_alt
o = run_row("Legacy", dict(s8=S8_NU, R="co1")); LEG["mu_u"] = mu_keep
b1 = RES["rows"]["B1"]; mv = (o["best_sigma8"] - b1["best_sigma8"]) / b1["width"]
MUTR["arms"]["MB2"] = dict(mapped_shifts=mapped.tolist(), best_sigma8=o["best_sigma8"], width=o["width"], B1_best=b1["best_sigma8"], move_in_widths=mv, bites=bool(abs(mv) >= 0.5))
P(f"  MB2 (MUTATE) KiDS-1000's prior shifts on Legacy's bins ({' '.join(f'{v:+.4f}' for v in mapped)}): best sigma8 {o['best_sigma8']:.4f} against B1's {b1['best_sigma8']:.4f}: "
  f"{mv:+.2f} widths -> {'bites' if abs(mv) >= 0.5 else 'DOES NOT BITE'}")
K1.setP(PZ0)
json.dump(RES, open(os.path.join(HERE, "parts", f"partb_{FT}.json"), "w"), indent=1, default=float)
json.dump(MUTR, open(os.path.join(HERE, "parts", f"partb_{FT}_MUTATE.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "parts", f"partb_{FT}.out"), "w").write("\n".join(LOG) + f"\ndone ({time.time() - T0:.0f} s)\n")
P(f"done ({time.time() - T0:.0f} s)")
