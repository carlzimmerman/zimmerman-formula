#!/usr/bin/env python3
"""HLF1 (FROZEN_CRITERIA.md, 123947b9dc) Part B: the forest row computed for form B.
The record's pipeline is executed read-only: closure_2026_11_09/SS1_self_shielded_conversion/ss1_cosmo.py up to its "run" marker, in
its own namespace (as WM1's wm1_cosmo.py does); its SIGTERM handler is replaced so nothing is ever written into SS1's folder.
  KA-B2  WM1's MN-W row replayed against the pipeline's own reference (stored relic m_eV, T_ncdm).
  Reported: form B's own spectrum against the pipeline's original reference (A_s placeholder 2.0e-9: not a gate).
  Then the pipeline's reference M / REFBG are replaced by form B's own CLASS (F1A B2 cold fit) and its background:
  KA-B1  R = 1 -> 0;  reading H (CO1's R_cold held);  reading F (the record's fade);  reported: H with R = 1 above 10 h/Mpc, H with
  the own-list R_cold (hlf1_hm_own.json).
  HLF1_MUTATE=1: MB1 (3 keV thermal-relic cutoff), MB2 (CFG556 candidate B's R held) -> hlf1_forest_<foot>_MUTATE.json
  HLF1_FOOT=canonical|alt nice -n 19 python3 hlf1_forest.py  -> hlf1_forest_<foot>.json / .out
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, json, math, time, io, contextlib, signal
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FOOT = os.environ.get("HLF1_FOOT", "canonical"); assert FOOT in ("canonical", "alt")
MUT = os.environ.get("HLF1_MUTATE", "0") == "1"; SUF = "_MUTATE" if MUT else ""
SS1 = os.path.join(REPO, "closure_2026_11_09", "SS1_self_shielded_conversion")
CO1 = os.path.join(REPO, "closure_2026_11_09", "CO1_form_b_cosmology_computed")
WM1 = os.path.join(REPO, "closure_2026_11_09", "WM1_warm_component_law_baryons")
F1AD = os.path.join(REPO, "closure_2026_11_07", "F1A_primary_cmb_audit")
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
RES = dict(lane="HLF1", part="B forest", footing=FOOT, criteria="123947b9dc", note="kappa = 1/2 FITTED; not theory closed; adopts nothing", KA={}, MUTATE={})
def dump():
    json.dump(RES, open(os.path.join(HERE, f"hlf1_forest_{FOOT}{SUF}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"hlf1_forest_{FOOT}{SUF}.out"), "w").write("\n".join(OUT) + "\n")

# ------------------------------------------------------------------ the record's pipeline, read-only
os.environ["SS1_FOOT"] = FOOT; os.environ.pop("SS1_MUTATE", None)
sys.path.insert(0, SS1); src = open(os.path.join(SS1, "ss1_cosmo.py")).read(); cut = src.index("# ================================================================== run")
ns = {"__file__": os.path.join(SS1, "ss1_cosmo.py"), "__name__": "ss1c_hlf1"}; _a = sys.argv; sys.argv = ["ss1_cosmo.py"]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:cut], "ss1c", "exec"), ns)
sys.argv = _a
def on_term(sig, frm):
    P("SIGTERM: stopped; nothing partial is written (rerun from the start: every step is minutes long)"); sys.exit(143)
signal.signal(signal.SIGTERM, on_term)
Class, KG, ZG, forest_setup, forest_eval, BASE, PREF = (ns[k] for k in ("Class", "KG", "ZG", "forest_setup", "forest_eval", "BASE", "PREF"))
M_REF, REFBG_REF = ns["M"], ns["REFBG"]; CLIGHT = 299792.458
FD = forest_setup()
RES["data"] = dict(md5=FD["md5"], md5_ok=FD["md5"] == "33d7fc21bfd3d745ed71a0bbe80ca433", n_points=FD["NB"], z_bins=[float(z) for z in FD["ZB"]])
P(f"[{FOOT}] DESI DR1 P1D: {FD['NB']} points, z {FD['ZB'][0]:.1f}-{FD['ZB'][-1]:.1f}, md5 ok {RES['data']['md5_ok']}; pipeline loaded  [{time.time() - T0:.0f} s]")

def class_bg(Mx):
    b = Mx.get_background(); z = b['z'][::-1]; Hh = b['H [1/Mpc]'][::-1] * CLIGHT; DM = b['comov. dist.'][::-1]; m = z <= 3600
    return dict(z=z[m], H=Hh[m], DM=DM[m])

# ------------------------------------------------------------------ form B's own linear model (F1A B2 cold fit; CO1's class_B settings, P_k_max 210)
pr = json.load(open(os.path.join(F1AD, "parts", f"fit_B2_{FOOT}_cold.json")))["pars"]
MB = Class()
MB.set({'output': 'tCl,lCl,mPk', 'l_max_scalars': ns["LMAX"] + 100, 'h': pr["h"], 'omega_b': pr["ob"], 'omega_cdm': pr["oc"], 'A_s': math.exp(pr["lnA"]) * 1e-10,
        'n_s': pr["ns"], 'tau_reio': pr["tau"], 'N_ur': 3.046, 'T_cmb': 2.7255, 'P_k_max_1/Mpc': 210.0, 'z_max_pk': ns["ZPK"]})
MB.compute(); BGB = class_bg(MB); HB = pr["h"]
RES["formB_pars"] = pr; RES["formB_sigma8"] = float(MB.sigma8())
P(f"[{FOOT}] form B (F1A B2 cold): h {HB:.4f} omega_b {pr['ob']:.5f} omega_d {pr['oc']:.4f} ln1e10As {pr['lnA']:.4f} n_s {pr['ns']:.4f} tau {pr['tau']:.4f}; sigma8 {MB.sigma8():.4f}  [{time.time() - T0:.0f} s]")
PBG = np.array([[MB.pk_lin(k, z) for z in ZG] for k in KG])

HM = json.load(open(os.path.join(CO1, "co1_hm.json"))); KH = np.array(HM["k"])
def Rkz_from(Rpow, fade=False, cut10=False):
    """amplitude ratio on KG (1/Mpc) x ZG from a power ratio on CO1's k grid (h/Mpc)."""
    kh = KG / HB; R = np.interp(np.log(kh), np.log(KH), np.asarray(Rpow, float))
    if cut10: R = np.where(kh > KH[-1], 1.0, R)
    out = np.empty((len(KG), len(ZG)))
    for j, z in enumerate(ZG):
        f = max(0.0, 1.0 - z) if fade else 1.0
        out[:, j] = np.sqrt(np.maximum(1.0 + f * (R - 1.0), 0.0))
    return out

if not MUT:
    # KA-B2: WM1's MN-W row, against the pipeline's own reference
    st = json.load(open(os.path.join(WM1, "parts", f"cosmo_W_{FOOT}.json")))
    rel = st["relic"]; WP = dict(BASE, omega_cdm=1e-7, N_ncdm=1, m_ncdm=rel["m_eV"], T_ncdm=rel["T_ncdm"], deg_ncdm=1.0, tol_ncdm_bg=1e-10)
    Mw = Class(); Mw.set(WP); Mw.compute(); PW = np.array([[Mw.pk_lin(k, z) for z in ZG] for k in KG]); Mw.struct_cleanup()
    fw = forest_eval(FD, REFBG_REF, np.sqrt(PW / PREF)); want = st["MN"]["MNW_forest"]["dchi2"]
    RES["KA"]["KA_B2"] = dict(dchi2=fw["dchi2"], stored=want, rel=fw["dchi2"] / want - 1, pass_=bool(abs(fw["dchi2"] / want - 1) <= 1e-4))
    P(f"[{FOOT}] KA-B2 WM1 MN-W replay: {fw['dchi2']:.2f} against stored {want:.2f} (rel {fw['dchi2'] / want - 1:+.1e}) -> {'PASS' if RES['KA']['KA_B2']['pass_'] else 'FAIL'}  [{time.time() - T0:.0f} s]")
    # reported: form B's own spectrum against the pipeline's original reference (not a gate)
    fx = forest_eval(FD, BGB, np.sqrt(PBG / PREF))
    RES["reported_vs_pipeline_reference"] = dict(fx, note="QX15 shape with A_s 2.0e-9 placeholder; not a gate")
    P(f"[{FOOT}] reported: form B's own spectrum against the pipeline's original reference (A_s placeholder 2.0e-9): dchi2 {fx['dchi2']:.1f} "
      f"(ratio {fx['r_min']:.4f}-{fx['r_max']:.4f}); not a gate")

# ------------------------------------------------------------------ form B's own spectrum as the reference
ns["M"] = MB; ns["REFBG"] = BGB
ONE = np.ones((len(KG), len(ZG)))
if MUT:
    OmC = pr["oc"] / HB ** 2; mk = 3.0; NUV = 1.12
    al = 0.049 * mk ** -1.11 * (OmC / 0.25) ** 0.11 * (HB / 0.7) ** 1.22 / HB
    T = (1 + (al * KG) ** (2 * NUV)) ** (-5 / NUV); m1 = forest_eval(FD, BGB, np.repeat(T[:, None], len(ZG), 1))
    RES["MUTATE"]["MB1"] = dict(m_keV=mk, alpha_Mpc=al, **m1, bites=bool(m1["dchi2"] > 4))
    P(f"[{FOOT}] MB1 3 keV thermal-relic cutoff (alpha {al:.4f} Mpc): dchi2 {m1['dchi2']:.1f} -> {'bites' if m1['dchi2'] > 4 else 'DOES NOT BITE'}")
    m2 = forest_eval(FD, BGB, Rkz_from(HM["MUTATE"]["M1_candB_R"][FOOT]))
    RES["MUTATE"]["MB2"] = dict(**m2, bites=bool(m2["dchi2"] > 4))
    P(f"[{FOOT}] MB2 CFG556 candidate B's R held: dchi2 {m2['dchi2']:.1f} -> {'bites' if m2['dchi2'] > 4 else 'DOES NOT BITE'}  [{time.time() - T0:.0f} s]")
    dump(); sys.exit(0)

k1 = forest_eval(FD, BGB, ONE)
RES["KA"]["KA_B1"] = dict(dchi2=k1["dchi2"], pass_=bool(abs(k1["dchi2"]) <= 1e-9 and RES["data"]["md5_ok"]))
P(f"[{FOOT}] KA-B1 form B's own spectrum against itself, R = 1: dchi2 {k1['dchi2']:.1e} -> {'PASS' if RES['KA']['KA_B1']['pass_'] else 'FAIL'}")
Rc = HM["primary"][FOOT]["R_cold"]
rH = forest_eval(FD, BGB, Rkz_from(Rc)); rF = forest_eval(FD, BGB, Rkz_from(Rc, fade=True))
RES["reading_H"] = rH; RES["reading_F"] = rF
P(f"[{FOOT}] reading H (CO1's R_cold held): dchi2 {rH['dchi2']:.2f} (ratio {rH['r_min']:.5f}-{rH['r_max']:.5f}) -> {rH['status']} (gate <= 4)")
P(f"[{FOOT}] reading F (the record's fade): dchi2 {rF['dchi2']:.2e} (ratio {rF['r_min']:.5f}-{rF['r_max']:.5f}) -> {rF['status']} (gate <= 4)")
rC = forest_eval(FD, BGB, Rkz_from(Rc, cut10=True)); RES["reported_H_R1_above_10"] = rC
P(f"[{FOOT}] reported: reading H with R = 1 above 10 h/Mpc: dchi2 {rC['dchi2']:.2f}")
# per-z decomposition of reading H (reported)
perz = {}
for z in FD["ZB"]:
    s_ = FD["zs"] == z
    sub = dict(FD, ZB=np.array([z]), zs=FD["zs"][s_], ks=FD["ks"][s_], Pd=FD["Pd"][s_], NB=int(s_.sum()))
    from scipy.linalg import cho_factor
    cf, lower = FD["CF"]; Ufac = np.tril(cf).T if lower else np.triu(cf)
    Cz = (Ufac.T @ Ufac)[np.ix_(s_, s_)]; sub["CF"] = cho_factor(Cz)
    perz[f"{z:.1f}"] = forest_eval(sub, BGB, Rkz_from(Rc))["dchi2"]
RES["reading_H_per_z"] = perz
P(f"[{FOOT}] reading H per z (own block of the covariance; reported): " + " ".join(f"{k}:{v:.1f}" for k, v in perz.items()))
OWNF = os.path.join(HERE, "hlf1_hm_own.json")
if os.path.exists(OWNF):
    ro = forest_eval(FD, BGB, Rkz_from(json.load(open(OWNF))["primary"][FOOT]["R_cold"])); RES["reported_H_own_list"] = ro
    P(f"[{FOOT}] reported: reading H with Part A's own-list R_cold: dchi2 {ro['dchi2']:.2f}")
ok = RES["KA"]["KA_B1"]["pass_"] and RES["KA"]["KA_B2"]["pass_"]
lab = ("FOREST ROW HOLDS" if (rH["dchi2"] <= 4 and rF["dchi2"] <= 4) else "FOREST ROW FAILS" if (rH["dchi2"] > 4 and rF["dchi2"] > 4) else "NO VERDICT")
RES["label_before_mutate"] = lab if ok else "NO VERDICT"; RES["KA_ok"] = ok
P(f"[{FOOT}] Part B label before the MUTATE file is read: {RES['label_before_mutate']}  [{time.time() - T0:.0f} s]")
dump()
