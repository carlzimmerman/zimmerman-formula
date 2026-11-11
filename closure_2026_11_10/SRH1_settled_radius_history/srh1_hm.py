#!/usr/bin/env python3
"""SRH1 (FROZEN_CRITERIA.md, 5ed8a37ec6): G1 forest, halo-model part. A copy of FZS1's fzs1_hm.py (73defd766f) with only the
case list, the z = 0 table and the output names changed: R_set = f x R_fold(z, M_b), FZS1's layout and cap unchanged.
FRZ1's frz1_hm.py is executed unchanged up to its "checkpointed run" marker, from its own path (read-only); FLD1's run files
are read read-only.  Cases: KA_T (r_ta), KA_0, the frozen f grid, MU1 (f 10), MU3a (z reversed at f 0.6), tilts.
  nice -n 10 python3 srh1_hm.py -> srh1_hm.json / .out, srh1_hm_MUTATE.json   (checkpoint srh1_hm_partial.json; SIGTERM-safe)
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
    if callable(fac): fac = fac(z)
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
PART = os.path.join(HERE, "srh1_hm_partial.json")
RES = json.load(open(PART)) if os.path.exists(PART) else dict(cases={}, KA={}, z0_table={})
def save(): json.dump(RES, open(PART, "w"))
def on_term(sig, frm):
    save(); print("SIGTERM: checkpoint written; rerun to resume", flush=True); sys.exit(143)
signal.signal(signal.SIGTERM, on_term)
P("SRH1 G1 halo model, R_set = f R_fold. kappa = 1/2 FITTED; not theory closed.")
FGRID = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.90, 1.00, 1.25, 1.50, 2.00]
fname = lambda f: f"f{f:.2f}"

# KA-F (FZS1's, unchanged)
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

# KA-Z0 (FZS1's) and the z = 0 table at every f (reported) + KA-Z0' (f = 1 against FZS1's table)
CO1 = json.load(open(os.path.join(REPO, "closure_2026_11_09", "CO1_form_b_cosmology_computed", "co1_hm.json")))
FZT = json.load(open(os.path.join(REPO, "closure_2026_11_10", "FZS1_forest_settled_radius", "fzs1_hm.json")))["z0_table"]
set_z(0.0); kz0 = {}
for ft in FOOTS:
    if f"KAZ0|{ft}" not in RES["KA"]:
        Rt, _, _, _ = ratios_S(ft, 0.0, fac=math.inf); RES["KA"][f"KAZ0|{ft}"] = float(np.max(np.abs(Rt / np.array(CO1["primary"][ft]["R_tot"]) - 1)))
    kz0[ft] = RES["KA"][f"KAZ0|{ft}"]
    for f in [0.0] + FGRID:
        key = f"{ft}|{fname(f)}"
        if key in RES["z0_table"]: continue
        Rt1, Rb1, Rc1, inf = ratios_S(ft, 0.0, fac=f)
        RES["z0_table"][key] = dict(R_tot_at_k1_3=at(Rt1, (1.0, 3.0)), R_cold_at_k1_3=at(Rc1, (1.0, 3.0))); save()
    P(f"z = 0 R_tot at k 1 / 3 [{ft}] (CO1 {at(np.array(CO1['primary'][ft]['R_tot']), (1.0, 3.0))}): " + "; ".join(f"{f:.2f}: {RES['z0_table'][ft + '|' + fname(f)]['R_tot_at_k1_3'][0]:.4f} / {RES['z0_table'][ft + '|' + fname(f)]['R_tot_at_k1_3'][1]:.4f}" for f in [0.0] + FGRID))
kzp = max(abs(a - b) for ft in FOOTS for a, b in zip(RES["z0_table"][f"{ft}|f1.00"]["R_tot_at_k1_3"], FZT[ft]["R_tot_at_k1_3"]))
RES["KA"]["KA_Z0"] = dict(max_rel=kz0, pass_=bool(max(kz0.values()) <= 1e-10)); RES["KA"]["KA_Z0_f1"] = dict(max_abs=kzp, pass_=bool(kzp <= 1e-4))
P(f"KA-Z0 R_set = r_ta against CO1: {kz0} -> {'PASS' if RES['KA']['KA_Z0']['pass_'] else 'FAIL'}; KA-Z0 f = 1 against FZS1's table: max |d| {kzp:.1e} -> {'PASS' if RES['KA']['KA_Z0_f1']['pass_'] else 'FAIL'}")

# KA-M at z = 3 (FZS1's)
set_z(3.0); err = 0.0; mono = True
for ft in FOOTS:
    for fac, opt in ((1.0, {}), (0.6, {}), (2.0, {})):
        fn = lay_S(ft, 3.0, fac, **opt)
        for hb in L["HB"]:
            r, Mx, _ = fn(hb)
            err = max(err, abs(Mx[-1] - hb["Mta"]) / hb["Mta"]); mono = mono and bool(np.all(np.diff(Mx) >= -1e-9 * hb["Mta"]))
RES["KA"]["KA_M"] = dict(max_rel=err, monotone=mono, pass_=bool(err <= 1e-9 and mono))
P(f"KA-M z = 3: max |M_S(r_ta) - M_ta| / M_ta {err:.1e}, non-decreasing {mono} -> {'PASS' if RES['KA']['KA_M']['pass_'] else 'FAIL'}")
save()

FZ = json.load(open(os.path.join(FRZ, "frz1_hm.json")))
ZREV = dict(zip(ZB, ZB[::-1]))
CASES = [("KA_T", dict(fac=math.inf)), ("KA_0", dict(fac=0.0))] + [(fname(f), dict(fac=f)) for f in FGRID] \
    + [("MU1_f10", dict(fac=10.0)), ("MU3a_zrev_f0.60", dict(fac=0.6, zrev=True))]
for beta in (-1.0, -0.5, 0.5):
    for f0 in (0.5, 0.75, 1.0):
        CASES.append((f"tilt_b{beta:+.1f}_f{f0:.2f}", dict(fac=(lambda z, f0=f0, beta=beta: f0 * (1 + z) ** beta))))
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
        P(f"  {name:22s} {ft:9s} R_cold at k 1/3/5/10: z 2.2 " + "/".join(f"{x:.4f}" for x in rows["2.2"]["R_cold_at"]) + "; z 3.0 "
          + "/".join(f"{x:.4f}" for x in rows["3.0"]["R_cold_at"]) + "; z 4.4 " + "/".join(f"{x:.4f}" for x in rows["4.4"]["R_cold_at"]) + f"   [{time.time() - T0:.0f} s]")
kt = {}; k0 = {}
for ft in FOOTS:
    kt[ft] = max(float(np.max(np.abs(np.array(RES["cases"][f"KA_T|{ft}"][str(z)]["R_cold"]) / np.array(FZ["cases"][f"primary|{ft}"][str(z)]["R_cold"]) - 1))) for z in ZB)
    k0[ft] = max(float(np.max(np.abs(np.array(RES["cases"][f"KA_0|{ft}"][str(z)]["R_cold"]) - 1))) for z in ZB)
RES["KA"]["KA_T_hm"] = dict(max_rel=kt, pass_=bool(max(kt.values()) <= 1e-10)); RES["KA"]["KA_0_hm"] = dict(max_abs=k0, pass_=bool(max(k0.values()) <= 1e-12))
P(f"KA-T (halo model) R_set = r_ta against FRZ1's stored primary R_cold: {kt} -> {'PASS' if RES['KA']['KA_T_hm']['pass_'] else 'FAIL'}")
P(f"KA-0 (halo model) R_set = 0: max |R_cold - 1| {k0} -> {'PASS' if RES['KA']['KA_0_hm']['pass_'] else 'FAIL'}")
d = lambda c, z: abs(RES["cases"][f"{c}|canonical"][z]["R_cold_at"][3] - 1)
p22, r22, p44, r44 = d("f0.60", "2.2"), d("MU3a_zrev_f0.60", "2.2"), d("f0.60", "4.4"), d("MU3a_zrev_f0.60", "4.4")
mu3 = dict(z2_2=[p22, r22], z4_4=[p44, r44], bites=bool(r22 <= 0.8 * p22 and r44 >= 1.2 * p44))
P(f"MU3a z reversed at f 0.6, |R_cold(k 10) - 1| canonical: z 2.2 {p22:.5f} -> {r22:.5f}; z 4.4 {p44:.5f} -> {r44:.5f} -> {'bites' if mu3['bites'] else 'DOES NOT BITE'}")
MU = dict(MU3a=mu3, cases={k: v for k, v in RES["cases"].items() if k.startswith("MU")})
json.dump(dict(lane="SRH1", MUTATE=MU, note="kappa = 1/2 FITTED; not theory closed; adopts nothing"), open(os.path.join(HERE, "srh1_hm_MUTATE.json"), "w"), indent=1)
RES.update(lane="SRH1", criteria="5ed8a37ec6", k=KK.tolist(), z_bins=ZB, f_grid=FGRID, note="kappa = 1/2 FITTED; not theory closed; adopts nothing",
           cases={k: v for k, v in RES["cases"].items() if not k.startswith("MU")})
json.dump(RES, open(os.path.join(HERE, "srh1_hm.json"), "w"), indent=1)
open(os.path.join(HERE, "srh1_hm.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
os.remove(PART); P(f"done ({time.time() - T0:.0f} s)")
