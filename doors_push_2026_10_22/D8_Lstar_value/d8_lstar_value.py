"""D8_Lstar_value -- the microscopic value of the stiffness length L*.
Criteria: FROZEN_CRITERIA.md (3327019734; AMENDMENT A1 pre-result ce9340ccbc).
Run:  OMP_NUM_THREADS=1 nice -n 10 python3 -I d8_lstar_value.py      (D8_MUTATE=1: K = 8 pi G in the Gamma=2 relation)
Reads record files read-only; no network; seconds.  kappa = 1/2 FITTED; not theory closed.

Part 1  A76's L* = sigma_c^2/a0 vs AG6D's free-medium Gamma = 2 stiffness (C1 bound), same footing.
Part 2  CFG820's globular chi^2 at the 1e4 K thermal L* (estimator copied verbatim from cfg820.py; not imported,
        because importing cfg820.py would rewrite its outputs).
Part 3  frozen matching rule L*_pred = sigma_gas^2/a0 on gas dispersions found on disk.
"""
import os, sys, json, math, csv
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUT = os.environ.get("D8_MUTATE") == "1"
OUT, CHECKS, RES = [], [], {"lane": "D8_Lstar_value", "mutate": MUT}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(cid, ok, value, thr, what):
    CHECKS.append(dict(id=cid, ok=bool(ok), value=value, threshold=thr, what=what))
    P(f"{cid} {'PASS' if ok else 'FAIL'} {value} {thr}   # {what}")


def R(*p):
    return os.path.join(REPO, *p)


# ---------------------------------------------------------------- constants (sources)
G = 6.67430e-11                      # BRIEF DSF-21 s4
c = 2.99792458e8
PC = 3.0856775814913673e16
MSUN = 1.98892e30                    # labelled; only used for M_sun/pc^3 conversions
KB = 1.380649e-23                    # CODATA
M_P = 1.67262192369e-27              # proton mass; A76's sigma_th route (reproduces 8225.51 m/s)
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}            # doors BRIEF rule 3
A0_820 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}    # CFG820's own footing values (chi^2 re-evaluation only)
T4, MU = 1.0e4, 1.22                                     # the record's premise (A11 s15, A65, A76)
MU_BRACKET = (0.60, 1.40)                                # A76 s3.2
L_CEIL = 90.0                                            # A20 ceiling (LITTLE THINGS cap 93.8 pc)
KPREF = (4.0 if MUT else 2.0) * math.pi * G              # Gamma=2: c_s^2 = KPREF L*^2 rho  (AG6D Part A: 2 pi G)

a76 = json.load(open(R("deepseek_push", "DS_FINAL_2026_10_21", "A76_Lstar_closure", "a76_results.json")))["derived"]
RHO_C = a76["rho_c"]                                     # 2.2565e-27 kg/m^3 (A16/A20/A76)
ag = json.load(open(R("argon_push", "AG6D_stiffness_length_origin", "ag6d_cutoff_results.json")))
agp = json.load(open(R("argon_push", "AG6D_stiffness_length_origin", "ag6d_cutoff_posthoc_results.json")))
L_IC_FROZEN = max(v["L_IC_pc"] for v in ag["L_IC"].values())     # '< 1 pc' (grid floor) -> conservative 1 pc
L_IC_POST = agp["P1_L_IC_pc"]                                       # 0.247 pc (post hoc)

sig_th = math.sqrt(KB * T4 / (MU * M_P))
def cs(Lpc, rho): return math.sqrt(KPREF * (Lpc * PC) ** 2 * rho)
def Lstar(sig, a0): return sig ** 2 / a0 / PC
RES["inputs"] = dict(rho_c=RHO_C, sigma_th_m_s=sig_th, L_IC_frozen_pc=L_IC_FROZEN, L_IC_posthoc_pc=L_IC_POST,
                     a0=A0, a0_cfg820=A0_820, T=T4, mu=MU, L_ceiling_pc=L_CEIL)

P("D8_Lstar_value" + ("   [MUTATE: K = 8 pi G]" if MUT else ""))
P(f"inputs: rho_c {RHO_C:.4e} kg/m^3 (A76); sigma_th(1e4 K, mu 1.22) {sig_th:.3f} m/s; "
  f"AG6D L*_IC frozen < {L_IC_FROZEN} pc, post hoc {L_IC_POST:.4f} pc")
check("K0", abs(sig_th / a76["sigma_th_m_s"] - 1) < 1e-6, f"{sig_th:.4f}", "A76 8225.51 m/s (1e-6)", "thermal width reproduces A76")

# ================================================================ Part 1
P("\n=== Part 1: is A76's L* = sigma_c^2/a0 the same object as AG6D's free-medium EOS stiffness?")
cs24 = cs(24.0, RHO_C)
rel = abs(cs24 / a76["cs_at_24_m_s"] - 1)
check("K1", rel < 1e-3, f"{cs24:.6f} m/s (rel {rel:.2e})", "A76 c_s(24 pc) 0.720398 m/s, rel < 1e-3",
      "A76's gamma=2piG L*^2, c_s^2=gamma rho_c IS AG6D's free-medium Gamma=2 c_s^2 = 2 pi G L*^2 rho_bar")
P(f"   -> A76/A16 evaluate c_s at the COSMIC MEAN rho_c: that is the free medium AG6D C1 tests.")
cs_max = cs(L_IC_FROZEN, RHO_C); cs_max_post = cs(L_IC_POST, RHO_C)
P(f"   AG6D C1: free-medium L* <= {L_IC_FROZEN} pc (frozen) / {L_IC_POST:.3f} pc (post hoc) "
  f"=> c_s(rho_c) <= {cs_max:.4f} / {cs_max_post:.4f} m/s; window floor 24 pc is {24/L_IC_FROZEN:.0f}x / {24/L_IC_POST:.1f}x above")
P1 = dict(cs_24pc_m_s=cs24, cs_rel_vs_A76=rel, cs_max_frozen_m_s=cs_max, cs_max_posthoc_m_s=cs_max_post,
          window_over_LIC_frozen=24 / L_IC_FROZEN, window_over_LIC_post=24 / L_IC_POST, foot={})
k2, k3 = [], []
for f, a0 in A0.items():
    smax = math.sqrt(a0 * L_IC_FROZEN * PC); smax_p = math.sqrt(a0 * L_IC_POST * PC)
    Tmax = MU * M_P * smax ** 2 / KB; Tmax_p = MU * M_P * smax_p ** 2 / KB
    Lth = Lstar(sig_th, a0)
    ratio = sig_th / smax
    cs_th = cs(Lth, RHO_C)
    rho_eq = sig_th ** 2 / (KPREF * (Lth * PC) ** 2)          # where the Gamma=2 sound speed equals sigma_c
    sig_dens = a0 / (2 * math.pi * G)                          # Sigma_M = a0/(2 pi G)
    d = dict(L_th_pc=Lth, sigma_max_frozen_m_s=smax, sigma_max_post_m_s=smax_p, T_max_frozen_K=Tmax, T_max_post_K=Tmax_p,
             sigma_th_over_sigma_max_frozen=ratio, sigma_th_over_sigma_max_post=sig_th / smax_p,
             cs_at_Lth_m_s=cs_th, sigma_th_over_cs=sig_th / cs_th, rho_eq_kg_m3=rho_eq, rho_eq_over_rho_c=rho_eq / RHO_C,
             rho_eq_Msun_pc3=rho_eq / (MSUN / PC ** 3), Sigma_M_Msun_pc2=sig_dens / (MSUN / PC ** 2))
    P1["foot"][f] = d
    P(f"   [{f:9s}] L*_th = {Lth:.3f} pc; free-medium cap sigma_c <= {smax:.1f} m/s (T <= {Tmax:.0f} K at mu 1.22) frozen, "
      f"{smax_p:.1f} m/s ({Tmax_p:.1f} K) post hoc; sigma_th/cap = {ratio:.2f} / {sig_th/smax_p:.2f}")
    P(f"   [{f:9s}] at L*_th: c_s(rho_c) = {cs_th:.4f} m/s, sigma_th/c_s = {sig_th/cs_th:.3e}; Gamma=2 c_s = sigma_th only at "
      f"rho_eq = a0/(2piG L*) = {rho_eq:.3e} kg/m^3 = {d['rho_eq_Msun_pc3']:.2f} Msun/pc^3 = {rho_eq/RHO_C:.3e} rho_c "
      f"(Sigma_M/L*, Sigma_M = {d['Sigma_M_Msun_pc2']:.1f} Msun/pc^2)")
    k2.append(ratio); k3.append((sig_th / cs_th, rho_eq / RHO_C))
check("K2", min(k2) >= 3, f"{min(k2):.3f} (min over footings)", ">= 3 both footings",
      "C1 applied to A76's reading: the 1e4 K sigma_c exceeds the free-medium cap")
check("K3", min(x for x, _ in k3) >= 1e3 and min(y for _, y in k3) >= 1e6,
      f"sigma/c_s {min(x for x,_ in k3):.3e}; rho_eq/rho_c {min(y for _,y in k3):.3e}", ">= 1e3 and >= 1e6",
      "sigma_c is not the free medium's sound speed; the two relations meet only at galactic density")
RES["part1"] = P1

# ================================================================ Part 2 (CFG820 estimator, verbatim constants)
P("\n=== Part 2: CFG820's globular chi^2 at the thermal L* (is the 24 pc floor a measurement?)")
G8, Msun8, kpc8, PC8 = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e16
UPS_V, MW_MB, WID = 1.6, 6.0e10, 0.15
GC = json.load(open(R("campaign_fresh_gravity", "CFG332_globulars_three_routes", "cfg332_globulars_results.json")))["clusters"]
def wolf_sigma(M, rhl, boost=1.0): return np.sqrt(G8 * boost * M * Msun8 / (6.0 * (4.0 / 3.0) * rhl * PC8)) / 1e3
def g_ext(RGC): return G8 * MW_MB * Msun8 / (RGC * kpc8) ** 2
def y_int(g, a0): return G8 * (UPS_V * g["LV"] * Msun8 / 2) / ((4.0 / 3.0) * g["rhl"] * PC8) ** 2 / a0
def nu_arr(y): y = max(float(y), 1e-12); return 1.0 / (-math.expm1(-math.sqrt(y)))
ST_s = np.array([0.01, 0.1, 0.3, 1, 3, 10, 100, 1000]); ST_S = np.array([0.0050, 0.048, 0.134, 0.358, 0.663, 0.894, 0.990, 0.998999])
def Sfun(s):
    if s <= 0.01: return s / 2
    if s >= 1000: return 1 - 1 / s
    return float(np.interp(math.log(s), np.log(ST_s), ST_S))
def pred(g, a0, Lst):
    M = UPS_V * g["LV"]; sN = wolf_sigma(M, g["rhl"]); Blaw = nu_arr(y_int(g, a0) + g_ext(g["RGC"]) / a0)
    if Lst is None: return sN
    rM = math.sqrt(G8 * M * Msun8 / a0) / PC8; lg = Lst ** 2 / (2 * rM); s = (4.0 / 3.0) * g["rhl"] / lg
    return sN * math.sqrt(1 + Sfun(s) * (Blaw - 1))
vU = (math.log(10) * WID / 2) ** 2
def chi2(gcs, a0, L):
    return sum((math.log(g["so"]) - math.log(pred(g, a0, L))) ** 2 / ((g["eso"] / g["so"]) ** 2 + vU) for g in gcs)
prim = [g for g in GC if g["name"] != "Pal 3"]
REF820 = json.load(open(R("campaign_fresh_gravity", "CFG820_stiffness_from_globulars", "cfg820_results.json")))
grid = np.geomspace(5.75, 3000, 400)
P2 = {}
k4 = []
for f, a0 in A0_820.items():
    c = np.array([chi2(prim, a0, L) for L in grid]); cmin = min(c.min(), chi2(prim, a0, None))
    L95g = float(grid[c - cmin <= 3.84].min()); ref = REF820[f"primary (no Pal 3)|{f}"]["L95"]
    k4.append(abs(L95g / ref - 1))
    # fine root of Delta chi2 = 3.84 below the grid L95
    fine = np.geomspace(5.75, 3000, 200001); cf = np.array([chi2(prim, a0, L) for L in fine[(fine > 10) & (fine < 40)]])
    ff = fine[(fine > 10) & (fine < 40)]; cminf = min(cmin, cf.min())
    L95f = float(ff[cf - cminf <= 3.84].min())
    sig = math.sqrt(KB * T4 / (MU * M_P))
    rows = {}
    for lab, mu in (("mu1.22", MU), ("mu0.60", MU_BRACKET[0]), ("mu1.40", MU_BRACKET[1])):
        s = math.sqrt(KB * T4 / (mu * M_P)); L = s ** 2 / a0 / PC
        rows[lab] = dict(L_pc=L, dchi2=chi2(prim, a0, L) - cminf)
    smin = math.sqrt(a0 * L95f * PC); Tmin = MU * M_P * smin ** 2 / KB; mumax = KB * T4 / (M_P * smin ** 2)
    P2[f] = dict(L95_grid_pc=L95g, L95_cfg820_pc=ref, L95_fine_pc=L95f, chi2_min=cminf, thermal=rows,
                 sigma_min_m_s=smin, T_min_K_at_mu122=Tmin, mu_max_at_1e4K=mumax)
    d = rows["mu1.22"]
    cls = "EXCLUDED at 95%" if d["dchi2"] > 3.84 else "allowed"
    P2[f]["class_thermal"] = cls
    P(f"   [{f:9s}] L*_95 grid {L95g:.3f} (CFG820 {ref:.3f}), fine {L95f:.3f} pc; thermal L* {d['L_pc']:.3f} pc: "
      f"dchi2 = {d['dchi2']:.3f} -> {cls}")
    P(f"   [{f:9s}]   mu 0.60: L* {rows['mu0.60']['L_pc']:.2f} pc dchi2 {rows['mu0.60']['dchi2']:.3f};  mu 1.40: L* "
      f"{rows['mu1.40']['L_pc']:.2f} pc dchi2 {rows['mu1.40']['dchi2']:.3f}")
    P(f"C6 [{f}] floor sigma_c >= {smin/1e3:.3f} km/s (T >= {Tmin:.0f} K at mu 1.22; mu <= {mumax:.3f} at 1e4 K)")
    P(f"C5 [{f}] CLASS thermal (1e4 K, mu 1.22): {cls} (dchi2 {d['dchi2']:.3f} vs 3.84)")
check("K4", max(k4) < 5e-3, f"{max(k4):.2e}", "< 5e-3", "CFG820 L*_95 reproduced on its own grid, both footings")
RES["part2"] = P2

# ================================================================ Part 3 (frozen matching rule)
P("\n=== Part 3: frozen matching rule L*_pred = sigma_gas^2/a0 on gas dispersions on disk")
def read_csv(path, col, skip_comment=True):
    vals, bad = [], 0
    with open(path) as fh:
        rows = [l for l in fh if not (skip_comment and l.startswith("#"))]
    for r in csv.DictReader(rows):
        try:
            v = float(r[col])
            if v > 0: vals.append(v)
            else: bad += 1
        except (ValueError, TypeError, KeyError):
            bad += 1
    return vals, bad
def summarize(sig_kms, a0):
    L = np.array([(s * 1e3) ** 2 / a0 / PC for s in sig_kms])
    return dict(n=len(L), median=float(np.median(L)), p16=float(np.percentile(L, 16)), p84=float(np.percentile(L, 84)),
                ratio_84_16=float(np.percentile(L, 84) / np.percentile(L, 16)), L_each=[float(x) for x in L])
def classify(s, f):
    lo = P2[f]["L95_fine_pc"]
    if s["median"] < lo: return f"TENSION (below CFG820 floor {lo:.2f} pc)"
    if s["median"] > L_CEIL: return f"TENSION (above {L_CEIL:.0f} pc ceiling)"
    return "CONSISTENT"
P3 = {}
tdg_path = R("real_research", "data", "tidal_dwarfs", "lelli2015_tdg.csv")
sig_tdg, bad = read_csv(tdg_path, "sigma_HI_kms")
esig_tdg, _ = read_csv(tdg_path, "e_sigma_HI_kms")
xpath = R("real_research", "data", "tdg", "lelli2015_tdgs.csv")
with open(xpath) as fh:
    hdr = next(csv.reader([l for l in fh if not l.startswith("#")]))
xcol = next((h for h in hdr if "sig" in h.lower()), None)
xchk = None
if xcol:
    sx, _ = read_csv(xpath, xcol)
    xchk = dict(col=xcol, values=sx, match=sorted(sx) == sorted(sig_tdg))
P(f"PRIMARY Lelli+2015 tidal dwarfs (z~0, HI 3D models): n = {len(sig_tdg)} (non-numeric/<=0 dropped: {bad}); "
  f"sigma_HI = {sig_tdg} km/s (+- {esig_tdg}); cross-transcription: {xchk}")
P3["primary_tdg"] = dict(file="real_research/data/tidal_dwarfs/lelli2015_tdg.csv", sigma_kms=sig_tdg, e_sigma_kms=esig_tdg,
                         dropped=bad, cross_check=xchk, foot={})
for f, a0 in A0.items():
    s = summarize(sig_tdg, a0); s["class"] = classify(s, f); s["universal_flag"] = s["ratio_84_16"] > 2
    P3["primary_tdg"]["foot"][f] = s
    P(f"P3 [{f:9s}] PRIMARY L*_pred median {s['median']:.1f} pc (16-84: {s['p16']:.1f}-{s['p84']:.1f}; 84/16 = "
      f"{s['ratio_84_16']:.2f}) -> {s['class']}{'; NOT one constant (84/16 > 2)' if s['universal_flag'] else ''}")
SEC = [("KMOS3D Ubler+17", ("real_research", "data", "kmos3d_ubler2017.csv"), "sigma0_kms"),
       ("KROSS Harrison+17", ("real_research", "data", "kross_harrison2017.csv"), "sigma0_kms"),
       ("RC100 Nestor Shachar+23 (CORRECTED)", ("real_research", "data", "rc100_nestorshachar2023_table3_CORRECTED.csv"), "sigma0_kms"),
       ("MSA3D 2026", ("real_research", "data", "msa3d_2026_rotation_curves.csv"), "sigma0"),
       ("Simons+16", ("data_assembly", "high_z_tf_tables", "simons2016_sigma.csv"), "sigma_g_kms")]
P3["secondary_highz"] = {}
for name, p, col in SEC:
    v, b = read_csv(R(*p), col)
    e = dict(file="/".join(p), col=col, dropped=b, foot={})
    for f, a0 in A0.items():
        s = summarize(v, a0); s.pop("L_each"); s["class"] = classify(s, f); e["foot"][f] = s
    P3["secondary_highz"][name] = e
    P(f"P3 SECONDARY (no verdict weight) {name}: n {len(v)} (dropped {b}); median sigma {np.median(v):.1f} km/s -> "
      f"L*_pred median {e['foot']['canonical']['median']:.0f} / {e['foot']['alt']['median']:.0f} pc (can/alt) "
      f"-> {e['foot']['canonical']['class']} / {e['foot']['alt']['class']}")
RES["part3"] = P3

# ---------------------------------------------------------------- window in sigma terms (report)
P("\n=== The window in velocity terms (report)")
WV = {}
for f, a0 in A0.items():
    lo = P2[f]["L95_fine_pc"]
    WV[f] = dict(sigma_lo_kms=math.sqrt(a0 * lo * PC) / 1e3, sigma_hi_kms=math.sqrt(a0 * L_CEIL * PC) / 1e3)
    P(f"   [{f:9s}] L* in [{lo:.2f}, {L_CEIL:.0f}] pc  <=>  sigma_c in [{WV[f]['sigma_lo_kms']:.3f}, {WV[f]['sigma_hi_kms']:.3f}] km/s")
RES["window_sigma"] = WV

npass = sum(c["ok"] for c in CHECKS)
RES["checks"] = CHECKS; RES["n_pass"] = npass; RES["n_checks"] = len(CHECKS)
P(f"\nD8_LSTAR_VALUE COMPLETE: {npass}/{len(CHECKS)} checks PASS.")
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"d8_lstar_value_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"d8_lstar_value{sfx}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == len(CHECKS) else 1)
