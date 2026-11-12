#!/usr/bin/env python3
"""FRZ2 copy of FRZ1 frz1_forest.py; reads FRZ2 hm/*.json (FRZ2 FROZEN_CRITERIA.md). Original header:
A0Z1 edit: the pipeline is FRZ2's, unchanged; only the file names and the lane id change (FROZEN_CRITERIA.md d9adb0feaa).
FRZ1 (FROZEN_CRITERIA.md, 1835d8fb7d): the forest gate of HLF1 Part B (copied from
closure_2026_11_10/HLF1_own_halo_list_forest/hlf1_forest.py; the pipeline set-up and form B's own reference unchanged) fed with
R_cold(k, z_i) from frz1_hm.json at each DESI redshift bin.
  KA2 R = 1 -> 0; KA3 CO1's z = 0 R_cold held -> HLF1's reading H; reading L (graded), reading V and the brackets (reported).
  HLF1_MUTATE=1: MZ1 (3 keV thermal-relic cutoff) -> frz1_forest_<foot>_MUTATE.json
  HLF1_FOOT=canonical|alt nice -n 19 python3 frz1_forest.py -> frz1_forest_<foot>.json / .out
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
RES = dict(lane="A0Z1", part="forest at z", footing=FOOT, criteria="d9adb0feaa", note="kappa = 1/2 FITTED; not theory closed; adopts nothing", KA={}, MUTATE={})
def dump():
    json.dump(RES, open(os.path.join(HERE, f"a0z1_forest_{FOOT}{SUF}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"a0z1_forest_{FOOT}{SUF}.out"), "w").write("\n".join(OUT) + "\n")

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


ZJ = {float(z): int(np.argmin(abs(ZG - z))) for z in FD["ZB"]}
def Rkz_z(rows, cut10=False):
    """rows: {z_bin: R_cold list on CO1's k grid}; each ZG column gets the R of its nearest DESI bin."""
    zb = np.array(sorted(float(z) for z in rows)); out = np.empty((len(KG), len(ZG))); kh = KG / HB
    for j, zz in enumerate(ZG):
        zn = zb[int(np.argmin(abs(zb - zz)))]; R = np.interp(np.log(kh), np.log(KH), np.asarray(rows[f"{zn:.1f}" if f"{zn:.1f}" in rows else str(zn)], float))
        if cut10: R = np.where(kh > KH[-1], 1.0, R)
        out[:, j] = np.sqrt(np.maximum(R, 0.0))
    return out
ns["M"] = MB; ns["REFBG"] = BGB
ONE = np.ones((len(KG), len(ZG)))
if MUT:
    OmC = pr["oc"] / HB ** 2; mk = 3.0; NUV = 1.12
    al = 0.049 * mk ** -1.11 * (OmC / 0.25) ** 0.11 * (HB / 0.7) ** 1.22 / HB
    T = (1 + (al * KG) ** (2 * NUV)) ** (-5 / NUV); m1 = forest_eval(FD, BGB, np.repeat(T[:, None], len(ZG), 1))
    RES["MUTATE"]["MZ1"] = dict(m_keV=mk, **m1, bites=bool(m1["dchi2"] > 4))
    P(f"[{FOOT}] MZ1 3 keV thermal-relic cutoff: dchi2 {m1['dchi2']:.1f} -> {'bites' if m1['dchi2'] > 4 else 'DOES NOT BITE'}")
    dump(); sys.exit(0)
from scipy.linalg import cho_factor
cf, lower = FD["CF"]; Ufac = np.tril(cf).T if lower else np.triu(cf); CFULL = Ufac.T @ Ufac
def perz(Rkz):
    o = {}
    for z in FD["ZB"]:
        s_ = FD["zs"] == z
        sub = dict(FD, ZB=np.array([z]), zs=FD["zs"][s_], ks=FD["ks"][s_], Pd=FD["Pd"][s_], NB=int(s_.sum()), CF=cho_factor(CFULL[np.ix_(s_, s_)]))
        o[f"{z:.1f}"] = forest_eval(sub, BGB, Rkz)["dchi2"]
    return o
k2 = forest_eval(FD, BGB, ONE)
RES["KA"]["KA2"] = dict(dchi2=k2["dchi2"], md5_ok=RES["data"]["md5_ok"], pass_=bool(k2["dchi2"] == 0.0 and RES["data"]["md5_ok"]))
HLF1H = {"canonical": 160.74, "alt": 1025.57}
k3 = forest_eval(FD, BGB, Rkz_from(HM["primary"][FOOT]["R_cold"]))
RES["KA"]["KA3"] = dict(dchi2=k3["dchi2"], hlf1=HLF1H[FOOT], pass_=bool(abs(k3["dchi2"] - HLF1H[FOOT]) <= 0.01))
P(f"[{FOOT}] KA2 R = 1: dchi2 {k2['dchi2']:.1e} -> {'PASS' if RES['KA']['KA2']['pass_'] else 'FAIL'}; KA3 held z = 0 R_cold: {k3['dchi2']:.2f} against HLF1 {HLF1H[FOOT]} -> {'PASS' if RES['KA']['KA3']['pass_'] else 'FAIL'}")
import glob
RES["cases"] = {}
for fn in sorted(glob.glob(os.path.join(HERE, "hm", f"*_{FOOT}.json"))):
    J = json.load(open(fn)); name = J["case"]; rows = J["rows"]
    Rz = {z: v["R_cold"] for z, v in rows.items()}; RZ = Rkz_z(Rz); r_ = forest_eval(FD, BGB, RZ)
    RES["cases"][name] = dict(dchi2=r_["dchi2"], status=r_["status"], label="PASSES" if r_["dchi2"] <= 4 else "FAILS",
                              f_z3=rows["3.0"]["f"], R_cold_z3_k135=rows["3.0"]["R_cold_at"])
    P(f"[{FOOT}] {name:8s}: dchi2 {r_['dchi2']:12.3f} -> {RES['cases'][name]['label']}")
dump()
