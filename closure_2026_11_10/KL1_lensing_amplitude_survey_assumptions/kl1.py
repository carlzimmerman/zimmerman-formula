#!/usr/bin/env python3
"""KL1 (FROZEN_CRITERIA.md 99a42c78ef): the rows A0 to ALL for one footing, on raw KiDS-1000 and DES Y3 (as on disk).
Order frozen: A0 (CO2 replayed; KA0, KA4) -> A1 (neutrino floor; baseline) -> A2 (covariance at the model; KA2) -> A3 (RB1's gas)
-> A4 (redshift calibration) -> A5 (brackets against) -> ALL = A1 + A2 + A3, with A2's / A3's edges, A4 and each A5 on ALL.
Each row: chi^2, chi^2_data, N, p, label (CO2's lines), the survey's best sigma8 and width, the gap; KiDS delta-z pulls.
Checkpointed per row in parts/rows_<footing>.json (a restart skips finished rows).

  OMP_NUM_THREADS=1 nice -n 10 python3 kl1.py canonical            (after kl1_fit_nu.py, kl1_nu.py, kl1_gas.py)
  KL1_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 kl1.py canonical    -> parts/rows_<footing>_MUTATE.json (MA2, MA3's chi^2, MP4)
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing. Gravity-only S0 box; inherited halo list in R."""
import os, sys, json, math, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import kl1_lib as K1
FT = sys.argv[1]; assert FT in K1.FOOTS
MUT = os.environ.get("KL1_MUTATE", "0") == "1"
HERE = K1.HERE; T0 = time.time()
OUTF = os.path.join(HERE, "parts", f"rows_{FT}{'_MUTATE' if MUT else ''}.json")
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)
SURV, NS, G = K1.SURV, K1.NS, K1.G
HM, ROWS = K1.HM, K1.ROWS
NU = json.load(open(os.path.join(HERE, "kl1_nu.json"))); GAS = json.load(open(os.path.join(HERE, "kl1_gas.json")))
S8_CO2 = ROWS["P2"][FT]["sigma8"]; S8_NU = NU["A1"][FT]["sigma8_nu"]
R = dict(co1=np.array(HM["primary"][FT]["R_tot"]), gas_rta=np.array(GAS["rows"][FT]["rta_table"]["R_tot"]),
         gas_r200c=np.array(GAS["rows"][FT]["r200c_table"]["R_tot"]), gas_power=np.array(GAS["rows"][FT]["rta_power"]["R_tot"]))
if MUT: R["gas_mut"] = np.array(json.load(open(os.path.join(HERE, "kl1_gas_MUTATE.json")))["rows"][FT]["R_tot"])

# ------------------------------------------------------------------ node-spectrum variants (A5a long modes, A1s neutrino shape)
K, SN = K1.K, K1.SN; PZ0 = K1.PZ0
def load200(rel):
    J2 = json.load(open(os.path.join(G["EXT"], *rel))); S2 = J2["snap"]; k2 = np.array(S2["z0"]["k"]); out = {}; med = {}
    for z, key in ((0.0, "z0"), (0.5, "z0.5"), (1.0, "z1")):
        p2 = np.exp(np.interp(np.log(K), np.log(k2), np.log(np.array(S2[key]["P"]))))
        m = (K >= 0.5) & (K <= 1.0) & (K <= k2[-1]); med[z] = float(np.median(p2[m] / PZ0[z][m]))
        o = PZ0[z].copy(); lo = K < 0.5; o[lo] = p2[lo]; o[~lo] = o[~lo] * med[z]; out[z] = o
    return out, med
PZV = {None: PZ0}
PZV["A5a"], MED_A5a = load200(("cfg411_work", "cfg411_S0_Rc3_MIXA_FLAT_canonical_N512.json"))
PZV["A5a_b"], MED_A5a_b = load200(("cfg424_work", "cfg424_S0_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N512_seed360.json"))
_shape = np.interp(np.log(K), np.log(np.array(NU["k_hMpc"])), np.array(NU["A1"][FT]["shape_factor"]))
PZV["A1s"] = {z: PZ0[z] * _shape for z in PZ0}

def Pm_of(Rk, s8, pz):
    K1.setP(PZV[pz]); return K1.Pmat(K1.run_of(Rk, (s8 / K1.S8E) ** 2, "resp"), "F")

# ------------------------------------------------------------------ A2 machinery (per survey; the fiducial comes from row A0)
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
    sdv = np.sqrt(np.diag(ctx["Cp"])); sgv = np.sqrt(np.diag(ctx["Gf"]))
    rp = ctx["Cp"] / np.outer(sdv, sdv); rg = ctx["Gf"] / np.outer(sgv, sgv); iu = np.triu_indices(len(sdv), 1)
    out["median_abs_dr"] = float(np.median(np.abs(rp - rg)[iu]))
    out["pass_"] = bool(out["i_pass"] is True and out["ii_pass"] is True)
    return out
def cov_model(sn, ctx, Pm, kmask, gamma):
    S = SURV[sn]; kept = np.where(kmask)[0]; kp = np.array([ctx["pos"][int(g)] for g in kept])
    G1, _ = K1.gauss_cov(S, kept, K1.cell_full(S, Pm)); xi = K1.xi_nominal(S, Pm)
    s = np.clip(xi[kept] / ctx["xi_fid"][kept], 0.5, 3.0)
    C = G1 / ctx["area"] + ctx["R"][np.ix_(kp, kp)] * np.outer(s, s) ** (gamma / 2.0)
    try:
        Lc = np.linalg.cholesky(C)
    except np.linalg.LinAlgError:
        return None, None, None
    Ci = np.linalg.inv(C); return Ci, float(2 * np.sum(np.log(np.diag(Lc)))), dict(s_median=float(np.median(s)), s_max=float(np.max(s)))

# ------------------------------------------------------------------ one row
def run_row(name, st, sn):
    S = SURV[sn]
    if sn == "DES" and st.get("ia") == "eta": return dict(na="DES already carries the redshift power of the alignment")
    kmask = K1.keep_mask(sn, st.get("thr", 0.9), st.get("khalf", False)); D = K1.subset(S, kmask)
    Rk, pz, cv = R[st["R"]], st.get("pz"), st.get("cov")
    ctx = None
    if cv is not None:
        ctx = CTX[sn] if cv.get("fid", 0.0) == 0.0 else make_ctx(sn, CTX[sn]["s8_fid"] + cv["fid"], CTX[sn]["area"])
    def ev(s8, with_ld=False):
        Pm = Pm_of(Rk, s8, pz); Ci, ld, info = (None, None, None)
        if cv is not None:
            Ci, ld, info = cov_model(sn, ctx, Pm, kmask, cv["gamma"])
            if Ci is None: return dict(chi2=float("nan"), p=float("nan"), not_pd=True)
        r = K1.fit(S, D, Pm, widen=st.get("widen", 1.0), ia=st.get("ia", "nla"), Cinv=Ci)
        if ld is not None: r["logdet"] = ld; r["cov_s"] = info
        return r
    tgt = st["s8"]; out = dict(settings={k: v for k, v in st.items()}, N=D["N"], target_sigma8=tgt)
    main = ev(tgt); out["at_target"] = main
    if main.get("not_pd"): out["label"] = "NO VERDICT (covariance not positive definite)"; return out
    out["label"] = main["label"]
    if st.get("scan", False):
        cache = {}
        def evc(s):
            k = round(s, 6)
            if k not in cache: cache[k] = ev(s)
            return cache[k]
        sc = K1.scan(evc); best = ev(sc["best_sigma8"])
        out["scan"] = sc; out["best"] = best; out["best_sigma8"] = sc["best_sigma8"]; out["width"] = sc["width"]
        out["gap_widths"] = (tgt - sc["best_sigma8"]) / sc["width"]; out["dchi2_target_vs_best"] = main["chi2"] - best["chi2"]
        if cv is not None:                                    # reported: the full Gaussian likelihood (ln det added)
            ss = np.array(sorted(cache)); c2 = np.array([cache[s]["chi2"] + cache[s]["logdet"] for s in ss]); i = int(np.argmin(c2))
            lo_, hi_ = max(i - 2, 0), min(i + 3, len(ss)); co = np.polyfit(ss[lo_:hi_], c2[lo_:hi_], 2)
            sb = float(-co[1] / (2 * co[0])) if co[0] > 0 else float(ss[i]); wd = 1 / math.sqrt(co[0]) if co[0] > 0 else float("nan")
            out["with_logdet"] = dict(best_sigma8=sb, width=wd, gap_widths=(tgt - sb) / wd, edge_hit=bool(i in (0, len(ss) - 1)),
                                      d_minus2lnL_target_vs_min=float(main["chi2"] + main["logdet"] - np.polyval(co, sb)))
    return out
def show(name, sn, o):
    if "na" in o: P(f"  {name:12s} {sn:4s}: n/a ({o['na']})"); return
    m = o["at_target"]
    if m.get("not_pd"): P(f"  {name:12s} {sn:4s}: covariance NOT positive definite -> NO VERDICT"); return
    s = (f"  {name:12s} {sn:4s}: sigma8 {o['target_sigma8']:.4f}: chi2 {m['chi2']:.2f} (data {m['chi2_data']:.2f}, N {m['N']}), p {m['p']:.2e} -> {m['label']}")
    if "best_sigma8" in o:
        s += f"; best {o['best_sigma8']:.4f} +- {o['width']:.4f} (p {o['best']['p']:.3f}), gap {o['gap_widths']:+.2f} widths, Delta chi2 {o['dchi2_target_vs_best']:+.2f}"
        if o["scan"]["edge_hit"]: s += " [EDGE]"
    if "with_logdet" in o: s += f"; with ln det: best {o['with_logdet']['best_sigma8']:.4f} +- {o['with_logdet']['width']:.4f}, gap {o['with_logdet']['gap_widths']:+.2f}"
    if "dz_pulls" in m: s += "; dz pulls " + " ".join(f"{v:+.2f}" for v in m["dz_pulls"])
    if "eta" in m: s += f"; eta {m['eta']:+.2f}"
    s += f"   [{time.time() - T0:.0f} s]"; P(s)

# ------------------------------------------------------------------ rows, in the frozen order
c2g = lambda g, f=0.0: dict(gamma=g, fid=f)
ROWS_SPEC = [
    ("A0", dict(s8=S8_CO2, R="co1", scan=True)),
    ("A1", dict(s8=S8_NU, R="co1", scan=True)),
    ("A2", dict(s8=S8_NU, R="co1", cov=c2g(2), scan=True)),
    ("A2_g0", dict(s8=S8_NU, R="co1", cov=c2g(0))), ("A2_g3", dict(s8=S8_NU, R="co1", cov=c2g(3))),
    ("A2_fid-0.02", dict(s8=S8_NU, R="co1", cov=c2g(2, -0.02))), ("A2_fid+0.02", dict(s8=S8_NU, R="co1", cov=c2g(2, +0.02))),
    ("A3", dict(s8=S8_NU, R="gas_rta", scan=True)),
    ("A3_R200c", dict(s8=S8_NU, R="gas_r200c")), ("A3_power", dict(s8=S8_NU, R="gas_power")),
    ("A4", dict(s8=S8_NU, R="co1", widen=2.0, scan=True)),
    ("A5a", dict(s8=S8_NU, R="co1", pz="A5a", scan=True)), ("A5a_b", dict(s8=S8_NU, R="co1", pz="A5a_b")),
    ("A5b", dict(s8=S8_NU, R="co1", khalf=True, scan=True)),
    ("A5c1", dict(s8=S8_NU, R="co1", ia="off", scan=True)), ("A5c2", dict(s8=S8_NU, R="co1", ia="eta", scan=True)),
    ("A5d0.8", dict(s8=S8_NU, R="co1", thr=0.8, scan=True)), ("A5d0.7", dict(s8=S8_NU, R="co1", thr=0.7, scan=True)),
    ("A1s", dict(s8=S8_NU, R="co1", pz="A1s")),
    ("ALL", dict(s8=S8_NU, R="gas_rta", cov=c2g(2), scan=True)),
    ("ALL_g0", dict(s8=S8_NU, R="gas_rta", cov=c2g(0))), ("ALL_g3", dict(s8=S8_NU, R="gas_rta", cov=c2g(3))),
    ("ALL_R200c", dict(s8=S8_NU, R="gas_r200c", cov=c2g(2))), ("ALL_power", dict(s8=S8_NU, R="gas_power", cov=c2g(2))),
    ("ALL_A4", dict(s8=S8_NU, R="gas_rta", cov=c2g(2), widen=2.0)),
    ("ALL_A5a", dict(s8=S8_NU, R="gas_rta", cov=c2g(2), pz="A5a", scan=True)), ("ALL_A5a_b", dict(s8=S8_NU, R="gas_rta", cov=c2g(2), pz="A5a_b")),
    ("ALL_A5b", dict(s8=S8_NU, R="gas_rta", cov=c2g(2), khalf=True, scan=True)),
    ("ALL_A5c1", dict(s8=S8_NU, R="gas_rta", cov=c2g(2), ia="off", scan=True)), ("ALL_A5c2", dict(s8=S8_NU, R="gas_rta", cov=c2g(2), ia="eta", scan=True)),
    ("ALL_A5d0.8", dict(s8=S8_NU, R="gas_rta", cov=c2g(2), thr=0.8, scan=True)), ("ALL_A5d0.7", dict(s8=S8_NU, R="gas_rta", cov=c2g(2), thr=0.7, scan=True)),
]
RES = json.load(open(OUTF)) if os.path.exists(OUTF) else dict(lane="KL1", criteria="99a42c78ef", foot=FT, note="kappa = 1/2 FITTED; not theory closed; adopts nothing; gravity-only S0; inherited halo list in R",
                                                              target_sigma8=dict(CO2=S8_CO2, A1=S8_NU), A5a_deficit=dict(CFG411=MED_A5a, CFG424=MED_A5a_b), KA={}, rows={}, MUTATE={})
def save(): json.dump(RES, open(OUTF, "w"), indent=1, default=float)
P(f"KL1 [{FT}] {'MUTATE ' if MUT else ''}rows. Targets: CO2 pinned sigma8 {S8_CO2:.4f}; with the neutrino floor {S8_NU:.4f}. N kept: KiDS {K1.DS['KiDS']['N']}, DES {K1.DS['DES']['N']}.")
P(f"  A5a box-size factor above k 0.5 (median P_L200 / P_L100 over 0.5-1.0), nodes z 0 / 0.5 / 1: CFG411 " + " / ".join(f"{v:.3f}" for v in MED_A5a.values())
  + "; CFG424 " + " / ".join(f"{v:.3f}" for v in MED_A5a_b.values()))

def ensure_ctx():
    for sn in SURV:
        if sn in CTX: continue
        fid = RES["rows"]["A0"][sn]["best_sigma8"]; CTX[sn] = make_ctx(sn, fid)
        if not MUT:
            k = ka2(CTX[sn]); RES["KA"].setdefault("KA2", {})[sn] = k
            P(f"  KA2 {sn}: fiducial sigma8 {fid:.4f}; area {k['area_deg2']:.1f} deg^2 (from {k['n_noise']} noise-dominated points); (i) published/mine 16-84 % "
              f"{k.get('i_q16', float('nan')):.3f}-{k.get('i_q84', float('nan')):.3f} -> {k['i_pass']}; (ii) {k['n_signal']} signal-dominated: median {k.get('ii_median', float('nan')):.3f}, "
              f"min {k.get('ii_min', float('nan')):.3f} -> {k['ii_pass']}; median |r_pub - r_mine| {k['median_abs_dr']:.3f} -> {'PASS' if k['pass_'] else 'FAIL'}")

if not MUT:
    # KA4: CO2's response check (KA5 there) replayed
    ka4 = {str(z): float(np.median(NS["ARAW"][z][K < 0.12])) for z in (0.0, 0.5, 1.0)}
    RES["KA"]["KA4"] = dict(median_alpha_below_k012=ka4, pass_=bool(all(abs(v - 1) <= 0.15 for v in ka4.values())))
    for name, st in ROWS_SPEC:
        if name in RES["rows"] and all(sn in RES["rows"][name] for sn in SURV): continue
        if st.get("cov") is not None: ensure_ctx()
        RES["rows"][name] = {sn: run_row(name, st, sn) for sn in SURV}
        for sn in SURV: show(name, sn, RES["rows"][name][sn])
        if name == "A0":
            a, d = RES["rows"]["A0"]["KiDS"], RES["rows"]["A0"]["DES"]; ref = dict(canonical=(157.89, 0.7358, 0.0162, 74.69), alt=(159.35, 0.7341, 0.0161, 74.67))[FT]
            ka0 = dict(chi2=a["at_target"]["chi2"], best=a["best_sigma8"], width=a["width"], des=d["at_target"]["chi2"], N=(a["N"], d["N"]), ref=ref,
                       pass_=bool(abs(a["at_target"]["chi2"] - ref[0]) <= 0.01 and abs(a["best_sigma8"] - ref[1]) <= 5e-4 and abs(a["width"] - ref[2]) <= 5e-4
                                  and abs(d["at_target"]["chi2"] - ref[3]) <= 0.01 and a["N"] == 104 and d["N"] == 52))
            RES["KA"]["KA0"] = ka0
            P(f"  KA0 CO2 replayed: chi2 {ka0['chi2']:.3f} (CO2 {ref[0]}), best {ka0['best']:.4f} +- {ka0['width']:.4f} (CO2 {ref[1]} +- {ref[2]}), DES {ka0['des']:.3f} (CO2 {ref[3]}), "
              f"N {ka0['N']} -> {'PASS' if ka0['pass_'] else 'FAIL'};  KA4 response {ka4} -> {'PASS' if RES['KA']['KA4']['pass_'] else 'FAIL'}")
        save()
else:
    base = json.load(open(os.path.join(HERE, "parts", f"rows_{FT}.json")))
    RES["rows"]["A0"] = base["rows"]["A0"]; ensure_ctx()
    # MA2: KA2 with every n_i halved must FAIL (ii)
    for sn in SURV:
        S = SURV[sn]; ctx = CTX[sn]; pub = ctx["pub"]; Pm = Pm_of(R["co1"], ctx["s8_fid"], None)
        G1, N1 = K1.gauss_cov(S, pub, K1.cell_full(S, Pm), ng_scale=0.5); dg = np.diag(G1); nf = np.diag(N1) / dg; dp = np.diag(ctx["Cp"])
        nd = nf >= 0.8; area = float(1.0 / np.median(dp[nd] / dg[nd])); m = dict(pub=pub, pos=ctx["pos"], area=area, ratio=dp / (dg / area), nfrac=nf, Cp=ctx["Cp"], Gf=G1 / area)
        k = ka2(m); RES["MUTATE"].setdefault("MA2", {})[sn] = dict(**k, bites=bool(k["ii_pass"] is False))
        P(f"  MA2 {sn} n halved: (ii) median {k.get('ii_median', float('nan')):.3f}, min {k.get('ii_min', float('nan')):.3f} -> {'FAILS, so the arm bites' if k['ii_pass'] is False else 'DOES NOT BITE'}")
    # MA3, chi^2 half: f_ret = 0.2 at the A1 target
    for sn in ("KiDS",):
        o = run_row("MA3", dict(s8=S8_NU, R="gas_mut"), sn); c_a1 = base["rows"]["A1"][sn]["at_target"]["chi2"]
        RES["MUTATE"]["MA3_chi2"] = dict(chi2=o["at_target"]["chi2"], A1=c_a1, d=o["at_target"]["chi2"] - c_a1, bites=bool(abs(o["at_target"]["chi2"] - c_a1) >= 2))
        P(f"  MA3 KiDS chi2 with f_ret = 0.2: {o['at_target']['chi2']:.2f} against A1's {c_a1:.2f} -> {'bites' if abs(o['at_target']['chi2'] - c_a1) >= 2 else 'DOES NOT BITE'}")
    # MP4: ALL's settings at sigma8 0.90 must still give KiDS p < 0.0027
    for sn in SURV:
        o = run_row("MP4", dict(s8=0.90, R="gas_rta", cov=c2g(2)), sn); RES["MUTATE"].setdefault("MP4", {})[sn] = dict(**o["at_target"], bites=bool(o["at_target"]["p"] < 0.0027))
        P(f"  MP4 {sn} ALL at sigma8 0.90: chi2 {o['at_target']['chi2']:.2f}, p {o['at_target']['p']:.2e} -> {'bites' if o['at_target']['p'] < 0.0027 else 'DOES NOT BITE'}"
          + ("" if sn == "KiDS" else " (reported; the frozen arm is KiDS)"))
    save()
K1.setP(PZ0)
P(f"done ({time.time() - T0:.0f} s)")
open(OUTF.replace(".json", ".out"), "a").write("\n".join(LOG) + "\n")
