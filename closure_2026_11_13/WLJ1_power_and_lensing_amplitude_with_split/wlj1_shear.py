#!/usr/bin/env python3
"""WLJ1 (FROZEN_CRITERIA.md, 03f9823de7) part 3: gates G-C5 (CO1 C5, raw KiDS-1000 d_cold), G-HLF1 (HLF1 Part A, the own list) and
G-P4 (CO2 P4, raw KiDS-1000 at the pinned amplitude) for REF, ADOPT and SPLIT, with the twins and brackets.
CFG592's native machinery, library part executed UNCHANGED from its own path (as co1_shear.py and co2_shear.py do), on CFG596's S0 run.
CO1's `grade` and CO2's response, run_of and fitp are COPIED (source named). Primary: each case's z = 0 ratio held in z. z bracket:
each node's spectrum multiplied by the case's own ratio at that node (z 0, 0.5, 1); the run's "fade" robust variant has no meaning
there and is left out of that bracket (the three others are kept).
  nice -n 10 python3 -I -B wlj1_shear.py   (after wlj1_hm.py) -> wlj1_shear.json, .out, wlj1_shear_MUTATE.json, .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, glob, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(REPO, "campaign_fresh_gravity", "CFG592_cosmic_shear_likelihood", "cfg592_native.py")
code = open(SRC).read(); cut = code.index("# ------------------------------------------------------------------ run\n")
G = {"__file__": SRC, "__name__": "cfg592_native_lib"}
import warnings; warnings.filterwarnings("ignore")
exec(compile(code[:cut], SRC, "exec"), G)
import numpy as np
from scipy.stats import chi2 as CH
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()
Pmat, fit, theory, nuis_spec, support_mask, subset, klass, SURV = (G[k] for k in ("Pmat", "fit", "theory", "nuis_spec", "support_mask", "subset", "klass", "SURV"))
FOOTS = ("canonical", "alt"); S8E = 0.811
HM = json.load(open(os.path.join(HERE, "wlj1_hm.json"))); MU = json.load(open(os.path.join(HERE, "wlj1_hm_MUTATE.json"))); KH = np.array(HM["k"])
CO1D = os.path.join(REPO, "closure_2026_11_09", "CO1_form_b_cosmology_computed"); CO2D = os.path.join(REPO, "closure_2026_11_09", "CO2_form_b_amplitude_pinned")
CO1S = json.load(open(os.path.join(CO1D, "co1_shear.json"))); CO1L = json.load(open(os.path.join(CO1D, "co1_linear.json")))
CO2S = json.load(open(os.path.join(CO2D, "co2_shear.json"))); ROWS = json.load(open(os.path.join(CO2D, "co2_rows.json")))
HLFS = json.load(open(os.path.join(REPO, "closure_2026_11_10", "HLF1_own_halo_list_forest", "hlf1_shear_own.json")))

S0J = json.load(open(glob.glob(os.path.join(G["EXT"], "cfg596_work", "P0", "cfg596_*.json"))[0])); SN = S0J["snap"]
K = np.array(SN["z0"]["k"]); NP_, LBOX = int(S0J["np"]), float(S0J["L"])
PZ = {0.0: np.array(SN["z0"]["P"]), 0.5: np.array(SN["z0.5"]["P"]), 1.0: np.array(SN["z1"]["P"])}
BASE = dict(N=NP_, L=LBOX, k=K, k_lo=float(K[0]), k_hi=float(math.pi * NP_ / (4 * LBOX)))
def onk(R): return np.interp(np.log(np.clip(K, KH[0], KH[-1])), np.log(KH), np.asarray(R, float))
# ---- CO2's response (copied from co2_shear.py)
def a_raw(early, late): return np.log(np.array(SN[late]["P"]) / np.array(SN[early]["P"])) / (2 * math.log(SN[late]["D"] / SN[early]["D"]))
ARAW = {0.0: a_raw("x0.2562", "z0"), 0.5: a_raw("x0.7548", "x0.2562"), 1.0: a_raw("z1", "x0.7548")}
def runmed5(a):
    n = len(a); return np.array([np.median(a[max(0, i - 2):min(n, i + 3)]) for i in range(n)])
ALPHA = {z: np.clip(runmed5(a), 1.0, 3.0) for z, a in ARAW.items()}
# ---- run dicts: held (CO1 / CO2's: B = R(k), nodes the run's) or nodes (each node x the case's own R at that node, B = 1)
def run_held(R, f=1.0, mode="resp"):
    nodes = {z: ((PZ[z] * (f ** ALPHA[z] if mode == "resp" else f),) * 2) for z in PZ}
    return dict(BASE, name="x", foot="-", B=onk(R), nodes=nodes)
def run_nodes(Rz, f=1.0, mode="resp"):
    nodes = {z: ((PZ[z] * (f ** ALPHA[z] if mode == "resp" else f) * onk(Rz[z]),) * 2) for z in PZ}
    return dict(BASE, name="x", foot="-", B=np.ones_like(K), nodes=nodes)
RUN1 = run_held(np.ones_like(KH)); PS0 = Pmat(RUN1, "S0")
def pval(f, N): return float(CH.sf(f["chi2_data"], N))
DS = {}
for sn, S in SURV.items():
    fm = support_mask(S, RUN1, PS0); D = subset(S, S["pubkeep"] & (fm >= 0.9)); DS[sn] = D
    DS[sn + "_s0"] = fit(S, D, PS0)
ka4 = {sn: dict(N=DS[sn]["N"], chi2=DS[sn + "_s0"]["chi2"]) for sn in ("KiDS", "DES")}
ka4_ok = bool(ka4["KiDS"]["N"] == 104 and abs(ka4["KiDS"]["chi2"] - 144.26) <= 0.01 and ka4["DES"]["N"] == 52 and abs(ka4["DES"]["chi2"] - 68.64) <= 0.01)
P(f"WLJ1 part 3: C5 / HLF1 Part A / P4. CFG596 S0 rows: {ka4} -> {'PASS' if ka4_ok else 'FAIL'}. Adopts nothing. kappa = 1/2 FITTED; not theory closed.")

# ---- CO1's grade (copied from co1_shear.py), generalised to a pair of run dicts
def grade(sn, rt, rb, full=True, nodes=False):
    S, D, s0 = SURV[sn], DS[sn], DS[sn + "_s0"]
    Pt, Pb = Pmat(rt, "F"), Pmat(rb, "F")
    ft_, fb = fit(S, D, Pt), fit(S, D, Pb); d = ft_["chi2"] - fb["chi2"]
    out = dict(N=D["N"], chi2_S0=s0["chi2"], chi2_bar=fb["chi2"], chi2_tot=ft_["chi2"], d_cold=d, p_tot=pval(ft_, D["N"]), p_bar=pval(fb, D["N"]))
    if not full: return out
    rob = dict(widen2=fit(S, D, Pt, widen=2.0)["chi2"] - fit(S, D, Pb, widen=2.0)["chi2"],
               noIA=fit(S, D, Pt, ia=False)["chi2"] - fit(S, D, Pb, ia=False)["chi2"],
               DESI=fit(S, D, Pmat(rt, "F", bg="DESI"), bg="DESI")["chi2"] - fit(S, D, Pmat(rb, "F", bg="DESI"), bg="DESI")["chi2"])
    if not nodes: rob["fade"] = fit(S, D, Pmat(rt, "F", boost="fade"))["chi2"] - fit(S, D, Pmat(rb, "F", boost="fade"))["chi2"]
    par = nuis_spec(S, 1.0, True)[3](np.array(fb["x"]))
    mock = theory(S, D, par, Pt, "PM"); null = theory(S, D, par, Pb, "PM")
    tooth = fit(S, D, Pb, data=mock)["chi2"]; tnull = fit(S, D, Pb, data=null)["chi2"]
    out.update(robust=rob, label=klass(d, list(rob.values()), D["N"] >= 10), tooth_chi2=tooth, tooth_null_chi2=tnull, visible=bool(tooth >= 9))
    return out
# ---- CO2's fitp (copied), on a run dict
def fitp(sn, run):
    r = fit(SURV[sn], DS[sn], Pmat(run, "F"))
    return dict(chi2=r["chi2"], chi2_data=r["chi2_data"], p=float(CH.sf(r["chi2_data"], DS[sn]["N"])), A_IA=r["A_IA"])
def lab(p): return "CONSISTENT" if p >= 0.05 else ("TENSION" if p >= 0.0027 else "EXCLUDED AT 3 SIGMA")

def arrs(case, ft, z=0.0, src="cases"):
    """(R_tot, R_bar) of a case at z: REF = (R_bar, R_bar) of ADOPT at z; TWL = R_bar (1 + 2 (R_cold,S2 - 1)); TWB from the twin file."""
    if src == "own":
        a = HM["own"][f"{'ADOPT' if case == 'REF' else case}|{ft}"]
        return (np.array(a["R_bar"]) if case == "REF" else np.array(a["R_tot"])), np.array(a["R_bar"])
    if case == "REF":
        a = HM["cases"][f"ADOPT|{ft}|{z}"]; return np.array(a["R_bar"]), np.array(a["R_bar"])
    if case == "TWL":
        a = HM["cases"][f"S2|{ft}|{z}"]; rb = np.array(a["R_bar"]); return rb * (1 + 2 * (np.array(a["R_cold"]) - 1)), rb
    a = MU["TWB"][f"TWB|{ft}|{z}"] if case == "TWB" else HM["cases"][f"{case}|{ft}|{z}"]
    return np.array(a["R_tot"]), np.array(a["R_bar"])
GRADED = ["REF", "ADOPT", "S1.25", "S2", "S3"]; REPORTED = ["Sinf", "U1.25", "U2", "U3"]; TWINS = ["TWB", "TWL"]
RES = dict(lane="WLJ1", part="G-C5, G-HLF1, G-P4", criteria="03f9823de7", KA=dict(KA_S0_rows=dict(rows=ka4, pass_=ka4_ok)), C5={}, C5_DES={}, C5_zb={}, C5_brackets={},
           HLF1={}, P4={}, P4_zb={}, P4_brackets={}, P4_scan={}, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
MUT = dict(lane="WLJ1", part="twins on C5 and P4", criteria="03f9823de7", C5={}, P4={}, C5_zb={}, P4_zb={}, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
for ft in FOOTS:
    s8 = ROWS["P2"][ft]["sigma8"]; s8u = ROWS["P2"][ft]["CO1_unpinned"]["sigma8"]; s8n = ROWS["brackets"][ft]["one_0p06eV_neutrino"]["sigma8"]; fp = (s8 / S8E) ** 2
    s8c3 = CO1L["C3"][ft]["sigma8"]; fc3 = (s8c3 / S8E) ** 2
    P(f"\n[{ft}] pinned sigma8 {s8:.4f}; CO1 unpinned {s8u:.4f}; neutrino bracket {s8n:.4f}")
    for cs in GRADED + REPORTED + TWINS:
        Rt, Rb = arrs(cs, ft); tgt = MUT if cs in TWINS else RES
        g = grade("KiDS", run_held(Rt), run_held(Rb)); tgt["C5"][f"{cs}|{ft}"] = g
        if cs not in TWINS: RES["C5_DES"][f"{cs}|{ft}"] = grade("DES", run_held(Rt), run_held(Rb), full=False)
        m = fitp("KiDS", run_held(Rt, fp)); c = fitp("KiDS", run_held(Rt, fp, "const"))
        tgt["P4"][f"{cs}|{ft}"] = dict(**m, label=lab(m["p"]), constant_factor=dict(**c, label=lab(c["p"])))
        line = (f"  {cs:6s} C5 d_cold {g['d_cold']:+.3f} robust " + " ".join(f"{k}{v:+.2f}" for k, v in g["robust"].items()) + f" -> {g['label']}; tooth {g['tooth_chi2']:.2f}"
                f" | P4 chi2 {m['chi2']:.3f} p {m['p']:.5f} -> {lab(m['p'])} (const {c['chi2']:.2f}, p {c['p']:.4f})")
        if cs not in ("U1.25", "U2", "U3"):
            Rz = {z: arrs(cs, ft, z) for z in (0.0, 0.5, 1.0)}
            gz = grade("KiDS", run_nodes({z: v[0] for z, v in Rz.items()}), run_nodes({z: v[1] for z, v in Rz.items()}), nodes=True)
            mz = fitp("KiDS", run_nodes({z: v[0] for z, v in Rz.items()}, fp))
            (MUT if cs in TWINS else RES)["C5_zb"][f"{cs}|{ft}"] = gz; (MUT if cs in TWINS else RES)["P4_zb"][f"{cs}|{ft}"] = dict(**mz, label=lab(mz["p"]))
            line += f" | z bracket: d_cold {gz['d_cold']:+.3f} ({gz['label']}), P4 {mz['chi2']:.3f} p {mz['p']:.5f} ({lab(mz['p'])})"
        P(line + f"   [{time.time() - T0:.0f} s]")
        if cs in ("REF", "ADOPT", "S1.25", "S2", "S3", "Sinf"):
            # CO2's brackets on P4; the case's own prefactor-0 layout from wlj1_hm.json
            pre0 = np.array(HM["brackets"][f"pre_0|ADOPT|{ft}"]["R_bar"]) if cs == "REF" else np.array(HM["brackets"][f"pre_0|{cs}|{ft}"]["R_tot"])
            br = dict(one_0p06eV_neutrino=fitp("KiDS", run_held(Rt, (s8n / S8E) ** 2)), prefactor_0_layout=fitp("KiDS", run_held(pre0, fp)),
                      unpinned_sigma8_response=fitp("KiDS", run_held(Rt, (s8u / S8E) ** 2)), constant_factor=c)
            for v in br.values(): v["label"] = lab(v["p"])
            RES["P4_brackets"][f"{cs}|{ft}"] = br
            # CO1's layout brackets on C5 (REF: the bracket's own R_bar both sides, d = 0) and CO1's KiDS amplitude bracket
            cb = {}
            for name in ("pre_1", "pre_0", "galaxy_virial_scope", "gas_core_0.2", "press_schechter", "conc_x0.7", "conc_x1.3"):
                b = HM["brackets"][f"{name}|{'ADOPT' if cs == 'REF' else cs}|{ft}"]; rb_ = np.array(b["R_bar"]); rt_ = rb_ if cs == "REF" else np.array(b["R_tot"])
                cb[name] = grade("KiDS", run_held(rt_), run_held(rb_), full=False)
            a_t = fitp("KiDS", run_held(Rt, fc3, "const")); a_b = fitp("KiDS", run_held(Rb, fc3, "const"))
            cb["amplitude_sigma8_of_C3"] = dict(d_cold=a_t["chi2"] - a_b["chi2"], chi2_tot=a_t["chi2"], chi2_bar=a_b["chi2"], sigma8=s8c3)
            RES["C5_brackets"][f"{cs}|{ft}"] = cb
            P(f"         brackets: C5 d_cold " + " ".join(f"{n}{v['d_cold']:+.2f}" for n, v in cb.items()) + "; P4 p " + " ".join(f"{n} {v['p']:.4f}" for n, v in br.items()) + f"   [{time.time() - T0:.0f} s]")
        if cs in GRADED:
            grid = np.arange(0.70, 0.9001, 0.0125); c2 = np.array([fitp("KiDS", run_held(Rt, (float(s) / S8E) ** 2))["chi2"] for s in grid]); i = int(np.argmin(c2))
            lo_, hi_ = max(i - 2, 0), min(i + 3, len(grid)); co = np.polyfit(grid[lo_:hi_], c2[lo_:hi_], 2); sb = -co[1] / (2 * co[0]); wid = 1 / math.sqrt(co[0])
            RES["P4_scan"][f"{cs}|{ft}"] = dict(best_sigma8=float(sb), width=float(wid), pinned_minus_best_in_widths=float((s8 - sb) / wid))
    # HLF1 Part A: the own list
    for cs in ["REF", "ADOPT", "S1.25", "S2", "S3", "Sinf"]:
        Rt, Rb = arrs(cs, ft, src="own"); RES["HLF1"][f"{cs}|{ft}"] = grade("KiDS", run_held(Rt), run_held(Rb))
        P(f"  own list {cs:6s} C5 d_cold {RES['HLF1'][f'{cs}|{ft}']['d_cold']:+.3f} -> {RES['HLF1'][f'{cs}|{ft}']['label']}")
    # known answers
    a = RES["C5"][f"ADOPT|{ft}"]; s = CO1S["C5"][ft]
    dd = [abs(a["d_cold"] - s["d_cold"]), abs(a["chi2_bar"] - s["chi2_bar"]), abs(a["chi2_tot"] - s["chi2_tot"]), abs(a["tooth_chi2"] - s["tooth_chi2"])] + [abs(a["robust"][k] - s["robust"][k]) for k in s["robust"]]
    RES["KA"][f"KA_G1_{ft}"] = dict(max_abs=max(dd), pass_=bool(max(dd) <= 0.005))
    m = RES["P4"][f"ADOPT|{ft}"]; s2 = CO2S["P4"][ft]; b = RES["P4_brackets"][f"ADOPT|{ft}"]; sb2 = CO2S["brackets"][ft]
    dd = [abs(m["chi2"] - s2["chi2"]), abs(m["constant_factor"]["chi2"] - s2["constant_factor"]["chi2"]), abs(b["one_0p06eV_neutrino"]["chi2"] - sb2["one_0p06eV_neutrino"]["chi2"]),
          abs(b["prefactor_0_layout"]["chi2"] - sb2["prefactor_0_layout"]["chi2"]), abs(b["unpinned_sigma8_response"]["chi2"] - sb2["unpinned_sigma8_response"]["chi2"])]
    RES["KA"][f"KA_G3_{ft}"] = dict(max_abs=max(dd), pass_=bool(max(dd) <= 0.01))
    o = RES["HLF1"][f"ADOPT|{ft}"]; so = HLFS["C5"][ft]; dd = [abs(o["d_cold"] - so["d_cold"])] + [abs(o["robust"][k] - so["robust"][k]) for k in so["robust"]]
    RES["KA"][f"KA_G4_C5_{ft}"] = dict(max_abs=max(dd), pass_=bool(max(dd) <= 0.005))
    r = RES["C5"][f"REF|{ft}"]; RES["KA"][f"KA_R_{ft}"] = dict(d_cold=r["d_cold"], pass_=bool(r["d_cold"] == 0.0))
    P(f"  KA-G1 {RES['KA'][f'KA_G1_{ft}']}; KA-G3 {RES['KA'][f'KA_G3_{ft}']}; KA-G4 (C5) {RES['KA'][f'KA_G4_C5_{ft}']}; KA-R {RES['KA'][f'KA_R_{ft}']}")
RES["KA_ok"] = bool(all(v["pass_"] for v in RES["KA"].values()))
P(f"\nKnown answers all pass: {RES['KA_ok']}   ({time.time() - T0:.0f} s)")
json.dump(RES, open(os.path.join(HERE, "wlj1_shear.json"), "w"), indent=1, default=float)
json.dump(MUT, open(os.path.join(HERE, "wlj1_shear_MUTATE.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "wlj1_shear.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
open(os.path.join(HERE, "wlj1_shear_MUTATE.out"), "w").write("\n".join(l for l in OUT if "TWB" in l or "TWL" in l) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
