#!/usr/bin/env python3
"""FZS1 (FROZEN_CRITERIA.md, 73defd766f): R_cold(k, z) at the DESI P1D bins with the law's layout only inside the settled
radius R_set(z, M_b) = FLD1's R_fold, the cold reference outside, the enclosed cold mass at R_set conserved.
FRZ1's frz1_hm.py is executed unchanged up to its "checkpointed run" marker, from its own path (read-only); its rgrid is
wrapped at call time to insert R_set as a node. FLD1's run files are read read-only.
  KA-F, KA-T, KA-0, KA-M, KA-Z0; cases primary, x0.5, x2, readingV; MUTATE MS1 (x10), MS2 (z reversed); z = 0 table.
  Checkpoints every case to fzs1_hm_partial.json (restartable; SIGTERM exits cleanly).
  nice -n 10 python3 fzs1_hm.py -> fzs1_hm.json / .out, fzs1_hm_MUTATE.json
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, json, math, time, signal
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FRZ = os.path.join(REPO, "closure_2026_11_10", "FRZ1_forest_redistribution_at_z")
FLD = os.path.join(REPO, "fable52_push", "FLD1_fold_reach")
SRC = os.path.join(FRZ, "frz1_hm.py"); code = open(SRC).read()
cut = code.index("# ------------------------------------------------------------------ checkpointed run\n")
F = {"__file__": SRC, "__name__": "frz1_lib"}
exec(compile(code[:cut], SRC, "exec"), F)
L = F["L"]; layout, set_z, v_vir, Xsh, M_L, bar_cum = (F[k] for k in ("layout", "set_z", "v_vir", "Xsh", "M_L", "bar_cum"))
FB, h, KK, VST, ZB, FOOTS = (F[k] for k in ("FB", "h", "KK", "VST", "ZB", "FOOTS"))
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()

# ------------------------------------------------------------------ R_set from FLD1's files (section 1 item 2)
MASSES = [6.5, 7, 8, 9, 9.4, 10, 10.45, 10.7, 10.9, 11.2, 11.5, 12]
FT = {f: {M: np.array(json.load(open(os.path.join(FLD, "runs", f"hubble_{f}_M{M:g}_zi10_N2400.json")))["series"]) for M in MASSES} for f in FOOTS}
def at_z(S, z):
    o = np.argsort(S[:, 1]); return float(np.interp(z, S[o, 1], S[o, 2]))
_RT = {}
def rfold_kpc(foot, z, lM):
    key = (foot, round(z, 6))
    if key not in _RT: _RT[key] = np.array([at_z(FT[foot][M], z) for M in MASSES])
    R = _RT[key]
    if lM < MASSES[0]: return float(R[0] * 10 ** ((lM - MASSES[0]) / 3))
    if lM > MASSES[-1]: return float(R[-1] * 10 ** ((lM - MASSES[-1]) / 3))
    if np.any(R <= 0): return float(np.interp(lM, MASSES, R))
    return float(10 ** np.interp(lM, MASSES, np.log10(R)))

# ------------------------------------------------------------------ the settled layout (section 1 item 3)
CUR = [0.0]; _rg = F["rgrid"]
def rgrid_S(hb, rmax):
    r = _rg(hb, rmax); R = CUR[0]
    return np.unique(np.concatenate([r, [R]])) if 0 < R < rmax else r
F["rgrid"] = rgrid_S
def regime(hb, foot): return "cluster" if v_vir(hb) > VST[foot] else "galaxy"
def Mb_fold(hb, foot):
    return FB * hb["M200c"] if regime(hb, foot) == "cluster" else (1 - FB) * hb["Mta"] / Xsh(foot)
def Bar(hb, foot, r, gal_scope="lag", clu_scope="r200c", rc_fac=0.1):
    if regime(hb, foot) == "galaxy":
        Rs, Ms = (hb["rta"], hb["Mta"]) if gal_scope == "lag" else (hb["r200"], hb["M"])
        Mb = (1 - FB) * Ms / Xsh(foot); shape = M_L(hb, np.minimum(r, Rs)) / Ms
        return Mb + (FB * Ms - Mb) * shape
    Ms = hb["M200c"] if clu_scope == "r200c" else hb["Mta"]
    return bar_cum(hb, FB * Ms, r, hb["r200c"], rc_fac)
def rset_com(hb, foot, z, fac=1.0, zfold=None):
    """R_set in FRZ1's comoving Mpc/h, capped at r_ta; fac = inf -> r_ta."""
    if fac == 0: return 0.0
    if math.isinf(fac): return hb["rta"]
    zf = z if zfold is None else zfold
    R = fac * rfold_kpc(foot, zf, math.log10(Mb_fold(hb, foot) / h)) * 1e-3 * (1 + z) * h
    return min(R, hb["rta"])
def lay_S(foot, z, fac=1.0, zfold=None, **opt):
    optR = {k: v for k, v in opt.items() if k in ("gal_scope", "clu_scope", "rc_fac")}
    def fn(hb):
        R = rset_com(hb, foot, z, fac, zfold); CUR[0] = R
        rB, MB, inf = layout(hb, foot, mode="B", **opt); rR, MR, _ = layout(hb, foot, mode="Rb", **optR); CUR[0] = 0.0
        if R <= 0 or inf["regime"] == "L": return rR, MR, dict(inf, R_set=R)
        assert len(rB) == len(rR) and np.array_equal(rB, rR)
        bar = Bar(hb, foot, rB, **optR); CB, CR = MB - bar, MR - bar
        i = int(np.argmin(abs(rB - R))); assert abs(rB[i] / R - 1) < 1e-12
        s = CR[i] / CB[i]
        return rB, np.where(rB <= rB[i], bar + s * CB, bar + CR), dict(inf, R_set=R, s=float(s))
    return fn
def ratios_S(foot, z, fac=1.0, zfold=None, **opt):
    optR = {k: v for k, v in opt.items() if k in ("gal_scope", "clu_scope", "rc_fac")}
    CUR[0] = 0.0
    Ustd = L["U_std"](); Pstd, _, _ = L["spectra_std"](Ustd)
    UL, _ = L["U_set"](lambda hb: layout(hb, foot, mode="L")); PLta, _, _ = L["spectra_ta"](UL)
    UR, _ = L["U_set"](lambda hb: layout(hb, foot, mode="Rb", **optR)); PR, _, _ = L["spectra_ta"](UR)
    US, inf = L["U_set"](lay_S(foot, z, fac, zfold, **opt)); PS, _, _ = L["spectra_ta"](US)
    Rtot = 1 + (PS - PLta) / Pstd; Rbar = 1 + (PR - PLta) / Pstd
    return Rtot, Rbar, Rtot / Rbar, inf
def at(R, ks=(1.0, 3.0, 5.0, 10.0)): return [float(np.interp(k, KK, R)) for k in ks]

# ------------------------------------------------------------------ checkpointed run
PART = os.path.join(HERE, "fzs1_hm_partial.json")
RES = json.load(open(PART)) if os.path.exists(PART) else dict(cases={}, KA={})
def save(): json.dump(RES, open(PART, "w"))
def on_term(sig, frm):
    save(); print("SIGTERM: checkpoint written; rerun to resume", flush=True); sys.exit(143)
signal.signal(signal.SIGTERM, on_term)
P("FZS1 halo model with a settled radius. kappa = 1/2 FITTED; not theory closed.")

# KA-F
TAB = {9.4: (62, 21, 7.6), 10.45: (139, 48, 17.2), 10.7: (169, 58, 21.0), 10.9: (197, 68, 24.5)}
kaf = []; okf = True
for M, vals in TAB.items():
    got = [rfold_kpc("canonical", z, M) for z in (0, 2, 4)]
    for g, v in zip(got, vals):
        tol = 0.06 if isinstance(v, float) else 0.6
        okf = okf and abs(g - v) <= tol
    kaf.append((M, [round(g, 2) for g in got], vals))
RES["KA"]["KA_F"] = dict(rows=kaf, pass_=bool(okf))
P("KA-F FLD1 R_fold canonical z 0/2/4 (kpc): " + "; ".join(f"{M}: {g} vs {v}" for M, g, v in kaf) + f" -> {'PASS' if okf else 'FAIL'}")

# KA-Z0 and the z = 0 table
CO1 = json.load(open(os.path.join(REPO, "closure_2026_11_09", "CO1_form_b_cosmology_computed", "co1_hm.json")))
set_z(0.0); z0 = {}; kz0 = {}
for ft in FOOTS:
    Rt, _, _, _ = ratios_S(ft, 0.0, fac=math.inf); kz0[ft] = float(np.max(np.abs(Rt / np.array(CO1["primary"][ft]["R_tot"]) - 1)))
    Rt1, Rb1, Rc1, inf = ratios_S(ft, 0.0, fac=1.0)
    z0[ft] = dict(R_tot_at_k1_3=at(Rt1, (1.0, 3.0)), R_cold_at_k1_3=at(Rc1, (1.0, 3.0)), CO1_R_tot_at_k1_3=at(np.array(CO1["primary"][ft]["R_tot"]), (1.0, 3.0)))
RES["KA"]["KA_Z0"] = dict(max_rel=kz0, pass_=bool(max(kz0.values()) <= 1e-10)); RES["z0_table"] = z0
P(f"KA-Z0 z = 0, R_set = r_ta against CO1's R_tot: {kz0} -> {'PASS' if RES['KA']['KA_Z0']['pass_'] else 'FAIL'}")
for ft in FOOTS:
    P(f"z = 0 under the rule [{ft}]: R_tot at k 1 / 3 = {z0[ft]['R_tot_at_k1_3'][0]:.4f} / {z0[ft]['R_tot_at_k1_3'][1]:.4f} (CO1 {z0[ft]['CO1_R_tot_at_k1_3'][0]:.4f} / {z0[ft]['CO1_R_tot_at_k1_3'][1]:.4f})")

# diagnostic: R_set against r200m at two masses
for z in (2.2, 3.0, 4.4):
    set_z(z); row = []
    for M in (1e11, 1e12):
        hb = min(L["HB"], key=lambda b: abs(math.log(b["M"] / M))); R = rset_com(hb, "canonical", z)
        row.append(f"M {hb['M']:.2e}: R_set {R:.4f} Mpc/h com = {R / ((1 + z) * h) * 1e3:.1f} kpc phys, R_set/r200m {R / hb['r200']:.3f}, R_set/r_ta {R / hb['rta']:.3f}, {regime(hb, 'canonical')}")
    P(f"z {z}: " + " | ".join(row))

# KA-M at z = 3
set_z(3.0); err = 0.0; mono = True
for ft in FOOTS:
    for fac, opt in ((1.0, {}), (2.0, {}), (1.0, dict(gal_scope="vir"))):
        fn = lay_S(ft, 3.0, fac, **opt)
        for hb in L["HB"]:
            r, Mx, _ = fn(hb)
            err = max(err, abs(Mx[-1] - hb["Mta"]) / hb["Mta"]); mono = mono and bool(np.all(np.diff(Mx) >= -1e-9 * hb["Mta"]))
RES["KA"]["KA_M"] = dict(max_rel=err, monotone=mono, pass_=bool(err <= 1e-9 and mono))
P(f"KA-M z = 3: max |M_S(r_ta) - M_ta| / M_ta {err:.1e}, non-decreasing {mono} -> {'PASS' if RES['KA']['KA_M']['pass_'] else 'FAIL'}")
save()

FZ = json.load(open(os.path.join(FRZ, "frz1_hm.json")))
ZREV = dict(zip(ZB, ZB[::-1]))
CASES = [("KA_T", dict(fac=math.inf)), ("KA_0", dict(fac=0.0)), ("primary", dict(fac=1.0)), ("x0.5", dict(fac=0.5)), ("x2", dict(fac=2.0)),
         ("readingV", dict(fac=1.0, gal_scope="vir")), ("MS1_x10", dict(fac=10.0)), ("MS2_zrev", dict(fac=1.0, zrev=True))]
for name, o in CASES:
    for ft in FOOTS:
        key = f"{name}|{ft}"
        if key in RES["cases"]: continue
        rows = {}
        for z in ZB:
            set_z(z); oo = {k: v for k, v in o.items() if k != "zrev"}
            if o.get("zrev"): oo["zfold"] = ZREV[z]
            Rt, Rb, Rc, inf = ratios_S(ft, z, **oo)
            ss = [i.get("s") for i in inf if i.get("s") is not None]
            rows[str(z)] = dict(R_cold=Rc.tolist(), R_tot_at=at(Rt), R_cold_at=at(Rc), s_min_max=[min(ss), max(ss)] if ss else None)
        RES["cases"][key] = rows; save()
        P(f"  {name:9s} {ft:9s} R_cold at k 1/3/5/10: z 2.2 " + "/".join(f"{x:.4f}" for x in rows["2.2"]["R_cold_at"]) + "; z 3.0 "
          + "/".join(f"{x:.4f}" for x in rows["3.0"]["R_cold_at"]) + "; z 4.4 " + "/".join(f"{x:.4f}" for x in rows["4.4"]["R_cold_at"]) + f"   [{time.time() - T0:.0f} s]")
# KA-T and KA-0 on the halo model
kt = {}; k0 = {}
for ft in FOOTS:
    kt[ft] = max(float(np.max(np.abs(np.array(RES["cases"][f"KA_T|{ft}"][str(z)]["R_cold"]) / np.array(FZ["cases"][f"primary|{ft}"][str(z)]["R_cold"]) - 1))) for z in ZB)
    k0[ft] = max(float(np.max(np.abs(np.array(RES["cases"][f"KA_0|{ft}"][str(z)]["R_cold"]) - 1))) for z in ZB)
RES["KA"]["KA_T_hm"] = dict(max_rel=kt, pass_=bool(max(kt.values()) <= 1e-10)); RES["KA"]["KA_0_hm"] = dict(max_abs=k0, pass_=bool(max(k0.values()) <= 1e-12))
P(f"KA-T (halo model) R_set = r_ta against FRZ1's stored primary R_cold: {kt} -> {'PASS' if RES['KA']['KA_T_hm']['pass_'] else 'FAIL'}")
P(f"KA-0 (halo model) R_set = 0: max |R_cold - 1| {k0} -> {'PASS' if RES['KA']['KA_0_hm']['pass_'] else 'FAIL'}")
# MS2 bite (halo model, canonical, k 10)
d = lambda c, z: abs(RES["cases"][f"{c}|canonical"][z]["R_cold_at"][3] - 1)
p22, r22, p44, r44 = d("primary", "2.2"), d("MS2_zrev", "2.2"), d("primary", "4.4"), d("MS2_zrev", "4.4")
ms2 = dict(z2_2=[p22, r22], z4_4=[p44, r44], bites=bool(r22 <= 0.8 * p22 and r44 >= 1.2 * p44))
P(f"MS2 z reversed, |R_cold(k 10) - 1| canonical: z 2.2 {p22:.5f} -> {r22:.5f}; z 4.4 {p44:.5f} -> {r44:.5f} -> {'bites' if ms2['bites'] else 'DOES NOT BITE'}")
MU = dict(MS2=ms2, cases={k: v for k, v in RES["cases"].items() if k.startswith("MS")})
json.dump(dict(lane="FZS1", MUTATE=MU, note="kappa = 1/2 FITTED; not theory closed; adopts nothing"), open(os.path.join(HERE, "fzs1_hm_MUTATE.json"), "w"), indent=1)
RES.update(lane="FZS1", criteria="73defd766f", k=KK.tolist(), z_bins=ZB, note="kappa = 1/2 FITTED; not theory closed; adopts nothing",
           cases={k: v for k, v in RES["cases"].items() if not k.startswith("MS")})
json.dump(RES, open(os.path.join(HERE, "fzs1_hm.json"), "w"), indent=1)
open(os.path.join(HERE, "fzs1_hm.out"), "w").write("\n".join(OUT) + "\n")
os.remove(PART); P(f"done ({time.time() - T0:.0f} s)")
