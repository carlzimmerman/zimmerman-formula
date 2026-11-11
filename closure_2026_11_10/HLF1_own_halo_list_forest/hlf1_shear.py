#!/usr/bin/env python3
"""HLF1 copy of closure_2026_11_09/CO1_form_b_cosmology_computed/co1_shear.py (CO1 commit 020522140a lineage), unchanged except: input / output
file names carry the halo list HLF1_LIST=inherited|own (HLF1 FROZEN_CRITERIA 123947b9dc, A.3). Original docstring follows.
CO1 (FROZEN_CRITERIA.md 020522140a, AMENDMENT_A1 5e1496298d) part 3: row C5, the redistribution on raw KiDS-1000 xi+-.
CFG592's native machinery, library part executed UNCHANGED (data, published covariance, n(z), published cuts, support cut,
nuisances, fit, klass), on CFG596's S0 run (L100 N1024; nodes z = 0, 0.5, 1). Models:
  S0            the record's Newtonian run (form B's stated dynamics);
  S0 x R_bar    the cold reference with the same baryons (layout Rb of co1_hm.py);
  S0 x R_tot    form B's layout.
Statistic d_cold = chi2(S0 x R_tot) - chi2(S0 x R_bar); robustness set widen2, noIA, fade, DESI; label by klass.
Tooth: data := form B's prediction at the Rb best-fit nuisances, refitted with S0 x R_bar (VISIBLE if chi2_min >= 9).
M1: CFG556's candidate-B primary R(k) in place of form B's, against S0 (must be >= 9 on KiDS, canonical).

  nice -n 10 python3 co1_shear.py     -> co1_shear.json, co1_shear.out      (run co1_hm.py, and co1_linear.py for the amplitude bracket, first)
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing. Inherited halo list in R (flagged in the criteria)."""
import os, sys, json, math, glob, time
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
LIST = os.environ.get("HLF1_LIST", "inherited")
SRC = os.path.join(REPO, "campaign_fresh_gravity", "CFG592_cosmic_shear_likelihood", "cfg592_native.py")
code = open(SRC).read(); cut = code.index("# ------------------------------------------------------------------ run\n")
G = {"__file__": SRC, "__name__": "cfg592_native_lib"}
exec(compile(code[:cut], SRC, "exec"), G)
import numpy as np
from scipy.stats import chi2 as CH
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()
Pmat, fit, theory, nuis_spec, support_mask, subset, klass, SURV = (G[k] for k in ("Pmat", "fit", "theory", "nuis_spec", "support_mask", "subset", "klass", "SURV"))
FOOTS = ("canonical", "alt")
HM = json.load(open(os.path.join(HERE, f"hlf1_hm_{LIST}.json"))); KH = np.array(HM["k"])
LINF = os.path.join(HERE, f"hlf1_linear_{LIST}.json"); LIN = json.load(open(LINF)) if os.path.exists(LINF) else None

S0J = json.load(open(glob.glob(os.path.join(G["EXT"], "cfg596_work", "P0", "cfg596_*.json"))[0]))
ZK = {0.0: "z0", 0.5: "z0.5", 1.0: "z1"}
K = np.array(S0J["snap"]["z0"]["k"]); NP_, LBOX = int(S0J["np"]), float(S0J["L"])
NODES = {z: (np.array(S0J["snap"][key]["P"]), np.array(S0J["snap"][key]["P"])) for z, key in ZK.items()}
BASE = dict(N=NP_, L=LBOX, k=K, k_lo=float(K[0]), k_hi=float(math.pi * NP_ / (4 * LBOX)), nodes=NODES)
def onk(R): return np.interp(np.log(np.clip(K, KH[0], KH[-1])), np.log(KH), np.asarray(R, float))
def run_of(R, name): return dict(BASE, name=name, foot="-", B=onk(R))
RUN1 = run_of(np.ones_like(KH), "S0")
PS0 = Pmat(RUN1, "S0"); PS0d = Pmat(RUN1, "S0", bg="DESI")
RES = dict(lane="CO1", part="C5 raw KiDS-1000 (DES Y3 reported)", criteria="020522140a", amendment_A1="5e1496298d", S0=S0J["tag"], k_lo=BASE["k_lo"], k_hi=BASE["k_hi"],
           note="kappa = 1/2 FITTED; not theory closed; adopts nothing; inherited halo list in R", KA={}, S0_rows={}, C5={}, DES_reported={}, brackets={}, MUTATE={"M1": {}})
P(f"CO1 part 3: the redistribution on raw cosmic shear. S0 run {S0J['tag']} (k {BASE['k_lo']:.3f}-{BASE['k_hi']:.3f} h/Mpc). kappa = 1/2 FITTED; not theory closed.")

def pval(f, N): return float(CH.sf(f["chi2_data"], N))
def strip(f): return {k: v for k, v in f.items() if k not in ("t", "x", "dz")}
DS = {}
for sn, S in SURV.items():
    f = support_mask(S, RUN1, PS0); keep = S["pubkeep"] & (f >= 0.9); D = subset(S, keep); DS[sn] = D
    s0 = fit(S, D, PS0); RES["S0_rows"][sn] = dict(N=D["N"], N_published=int(S["pubkeep"].sum()), **strip(s0), p=pval(s0, D["N"]))
    DS[sn + "_s0"] = s0
    P(f"S0 on {sn}: N_kept {D['N']} of {int(S['pubkeep'].sum())} published; chi2 {s0['chi2']:.2f} (p {pval(s0, D['N']):.3f}), A_IA {s0['A_IA']:.2f}   [{time.time() - T0:.0f} s]")
ka4 = dict(KiDS=dict(N=DS["KiDS"]["N"], chi2=DS["KiDS_s0"]["chi2"], N_ref=104, chi2_ref=144.26), DES=dict(N=DS["DES"]["N"], chi2=DS["DES_s0"]["chi2"], N_ref=52, chi2_ref=68.64))
for v in ka4.values(): v["pass_"] = bool(v["N"] == v["N_ref"] and abs(v["chi2"] - v["chi2_ref"]) <= 0.01)
RES["KA"]["KA4"] = ka4
P("KA4 CFG596's S0 rows reproduced: " + "; ".join(f"{sn} N {v['N']} ({v['N_ref']}), chi2 {v['chi2']:.2f} ({v['chi2_ref']})" for sn, v in ka4.items())
  + f" -> {'PASS' if all(v['pass_'] for v in ka4.values()) else 'FAIL'}")

def grade(sn, Rtot, Rbar, full=True):
    S, D, s0 = SURV[sn], DS[sn], DS[sn + "_s0"]; rt, rb = run_of(Rtot, "B"), run_of(Rbar, "Rb")
    Pt, Pb = Pmat(rt, "F"), Pmat(rb, "F")
    ft_, fb = fit(S, D, Pt), fit(S, D, Pb); d = ft_["chi2"] - fb["chi2"]
    out = dict(N=D["N"], chi2_S0=s0["chi2"], chi2_bar=fb["chi2"], chi2_tot=ft_["chi2"], d_cold=d, d_bar_vs_S0=fb["chi2"] - s0["chi2"], d_tot_vs_S0=ft_["chi2"] - s0["chi2"],
               p_S0=pval(s0, D["N"]), p_bar=pval(fb, D["N"]), p_tot=pval(ft_, D["N"]), A_IA=dict(S0=s0["A_IA"], bar=fb["A_IA"], tot=ft_["A_IA"]))
    if not full: return out
    rob = dict(widen2=fit(S, D, Pt, widen=2.0)["chi2"] - fit(S, D, Pb, widen=2.0)["chi2"],
               noIA=fit(S, D, Pt, ia=False)["chi2"] - fit(S, D, Pb, ia=False)["chi2"],
               fade=fit(S, D, Pmat(rt, "F", boost="fade"))["chi2"] - fit(S, D, Pmat(rb, "F", boost="fade"))["chi2"],
               DESI=fit(S, D, Pmat(rt, "F", bg="DESI"), bg="DESI")["chi2"] - fit(S, D, Pmat(rb, "F", bg="DESI"), bg="DESI")["chi2"])
    par = nuis_spec(S, 1.0, True)[3](np.array(fb["x"]))
    mock = theory(S, D, par, Pt, "PM"); null = theory(S, D, par, Pb, "PM")
    tooth = fit(S, D, Pb, data=mock)["chi2"]; tnull = fit(S, D, Pb, data=null)["chi2"]
    out.update(robust=rob, label=klass(d, list(rob.values()), D["N"] >= 10), tooth_chi2=tooth, tooth_null_chi2=tnull, visible=bool(tooth >= 9))
    return out

for ft in FOOTS:
    pri = HM["primary"][ft]
    P(f"\n[{ft}] R_cold on the run's k: " + ", ".join(f"k {kk:g}: {np.interp(kk, KH, np.array(pri['R_cold'])):.3f}" for kk in (0.3, 0.5, 1, 2, 3, 5, 8)))
    for sn in ("KiDS", "DES"):
        g = grade(sn, pri["R_tot"], pri["R_bar"]); (RES["C5"] if sn == "KiDS" else RES["DES_reported"])[ft] = g
        P(f"  {sn}: N {g['N']}; chi2 S0 {g['chi2_S0']:.2f} (p {g['p_S0']:.3f}), S0 x R_bar {g['chi2_bar']:.2f} (p {g['p_bar']:.3f}), S0 x R_tot {g['chi2_tot']:.2f} (p {g['p_tot']:.3f}) "
          f"-> d_cold {g['d_cold']:+.2f}; robust " + str({k_: round(v, 2) for k_, v in g["robust"].items()}) + f" -> {g['label']}" + ("" if sn == "KiDS" else " (reported)"))
        P(f"      tooth: form B's own prediction refitted with the cold reference: chi2_min {g['tooth_chi2']:.2f} (null {g['tooth_null_chi2']:.2f}) -> "
          f"{'VISIBLE' if g['visible'] else 'NOT VISIBLE'} to {sn};  A_IA S0 {g['A_IA']['S0']:.2f}, Rb {g['A_IA']['bar']:.2f}, B {g['A_IA']['tot']:.2f}   [{time.time() - T0:.0f} s]")
    # M1
    m1 = {}
    for sn in ("KiDS", "DES"):
        S, D, s0 = SURV[sn], DS[sn], DS[sn + "_s0"]; fm = fit(S, D, Pmat(run_of(HM["MUTATE"]["M1_candB_R"][ft], "candB"), "F"))
        m1[sn] = dict(d=fm["chi2"] - s0["chi2"], bites=bool(fm["chi2"] - s0["chi2"] >= 9))
    RES["MUTATE"]["M1"][ft] = m1
    P(f"  M1 candidate B's halo-model R(k) against S0: KiDS d {m1['KiDS']['d']:+.2f} -> {'bites' if m1['KiDS']['bites'] else 'DOES NOT BITE'}; DES d {m1['DES']['d']:+.2f} (reported)")
    # brackets (KiDS, main fit only)
    br = {}
    for name, b in HM["brackets"][ft].items():
        g = grade("KiDS", b["R_tot"], b["R_bar"], full=False); br[name] = dict(d_cold=g["d_cold"], chi2_tot=g["chi2_tot"], chi2_bar=g["chi2_bar"])
    m4 = HM["MUTATE"]["M4"][ft]; g4 = grade("KiDS", m4["R_tot"], pri["R_bar"], full=False); br["M4_cluster_rule_lagrangian_scope"] = dict(d_cold=g4["d_cold"], chi2_tot=g4["chi2_tot"], chi2_bar=g4["chi2_bar"])
    if LIN is not None:
        s8 = LIN["C3"][ft]["sigma8"]; fac = (s8 / 0.811) ** 2; S, D = SURV["KiDS"], DS["KiDS"]
        rt, rb = run_of(pri["R_tot"], "B"), run_of(pri["R_bar"], "Rb")
        a0_, ab, at_ = fit(S, D, PS0 * fac), fit(S, D, Pmat(rb, "F") * fac), fit(S, D, Pmat(rt, "F") * fac)
        br["amplitude_sigma8_of_C3"] = dict(sigma8=s8, factor=fac, chi2_S0=a0_["chi2"], chi2_bar=ab["chi2"], chi2_tot=at_["chi2"], d_cold=at_["chi2"] - ab["chi2"], p_tot=pval(at_, D["N"]))
        # POST HOC (added after C2's amplitude was seen, reported only): the same with the amplitude PR4 lensing measures, sigma8 sqrt(A)
        s8l = s8 * math.sqrt(LIN["C2"][ft]["A"]); facl = (s8l / 0.811) ** 2
        l0, lb, lt = fit(S, D, PS0 * facl), fit(S, D, Pmat(rb, "F") * facl), fit(S, D, Pmat(rt, "F") * facl)
        RES.setdefault("posthoc", {})[ft] = dict(amplitude_lensing_calibrated=dict(sigma8=s8l, factor=facl, chi2_S0=l0["chi2"], chi2_bar=lb["chi2"], chi2_tot=lt["chi2"],
                                                                                   d_cold=lt["chi2"] - lb["chi2"], p_tot=pval(lt, D["N"])))
    RES["brackets"][ft] = br
    P("  brackets, KiDS d_cold (reported): " + "; ".join(f"{n} {v['d_cold']:+.2f}" for n, v in br.items() if n != "amplitude_sigma8_of_C3"))
    if LIN is not None:
        a = br["amplitude_sigma8_of_C3"]
        P(f"  amplitude bracket (S0 scaled to sigma8 {a['sigma8']:.4f}, factor {a['factor']:.4f}): chi2 S0 {a['chi2_S0']:.2f}, S0 x R_bar {a['chi2_bar']:.2f}, S0 x R_tot {a['chi2_tot']:.2f} "
          f"(p {a['p_tot']:.4f}); d_cold {a['d_cold']:+.2f}   [{time.time() - T0:.0f} s]")
        a = RES["posthoc"][ft]["amplitude_lensing_calibrated"]
        P(f"  POST HOC, reported (amplitude as PR4 lensing measures it, sigma8 {a['sigma8']:.4f}, factor {a['factor']:.4f}): chi2 S0 {a['chi2_S0']:.2f}, S0 x R_bar {a['chi2_bar']:.2f}, "
          f"S0 x R_tot {a['chi2_tot']:.2f} (p {a['p_tot']:.4f}); d_cold {a['d_cold']:+.2f}")
RES["KA_ok"] = bool(all(v["pass_"] for v in ka4.values()))
P(f"\nKnown answer KA4 passes: {RES['KA_ok']}; M1 bites on KiDS canonical: {RES['MUTATE']['M1']['canonical']['KiDS']['bites']}   ({time.time() - T0:.0f} s)")
json.dump(RES, open(os.path.join(HERE, f"hlf1_shear_{LIST}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"hlf1_shear_{LIST}.out"), "w").write("\n".join(OUT) + "\n")
