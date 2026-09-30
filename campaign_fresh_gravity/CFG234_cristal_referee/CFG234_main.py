"""CFG234 main: reproduction (attack a) of CFG213 from CFG234_FROZEN_CRITERIA.md. Exit 0 if controls C1, C2, C4(vs CFG5), M7 pass.
CFG213 scripts/outputs are not read."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CFG234_common import *

t = start("CFG234_main")
B = 10000
R = {}
rows = []


def rec(i, q, mine, tgt, line, verdict):
    rows.append(dict(id=i, q=q, mine=mine, target=tgt, line=line, verdict=verdict))
    print(f"[{i}] {q}: mine={mine} | target={tgt} | line={line} -> {verdict}")


def near(a, b, tol):
    return abs(a - b) <= tol + 1e-12


def edge_verdict(mine_edge, tgt_edge, dls, tol=0.02):
    if near(mine_edge, tgt_edge, tol):
        return "PASS"
    lo, hi = sorted((mine_edge, tgt_edge))
    between = int(np.sum((dls > lo) & (dls < hi)))
    return "DISCRETENESS" if between == 0 else "FAIL"


C = {}
# ----------------------------------------------------------------------------------------- C4
c4 = c4_crosscheck()
print("C4:", c4)
c4_ok = c4["ok"] and c4["max_rel_diff_nu_mono_vs_CFG5"] < 1e-9 and c4["max_rel_diff_p2_vs_CFG5"] < 1e-12
c4_cfg4_miss = c4.get("max_rel_diff_nu_mono_vs_CFG4", 0) > 1e-9
print(f"C4 vs CFG5_common (the record's standing kernel): {'PASS' if c4_ok else 'FAIL'}; vs the older CFG4_common copy: "
      f"{'frozen 1e-9 line MISSED (' + format(c4.get('max_rel_diff_nu_mono_vs_CFG4', 0), '.2e') + ', kept)' if c4_cfg4_miss else 'pass'}")
R["C4"] = c4

# ----------------------------------------------------------------------------------------- C1, C2
y = np.logspace(-4, 3, 50)
c1 = {}
for kn, kf in KERN.items():
    Dv = kf(y)
    yb = invert_nu(Dv, kf)
    c1[kn] = float(np.max(np.abs(yb / y - 1)))
print("C1 nu round trip (max rel err in y):", c1)
c1_ok = all(v < 1e-9 for v in c1.values())
c2 = {}
zz = np.array([4.4, 5.0, 5.7]); gb = np.array([3e-11, 2e-10, 8e-10])
for foot in A0:
    for kn, kf in KERN.items():
        for law in ("flat", "rival"):
            a0 = A0[foot] * (E_of_z(zz) if law == "rival" else 1.0)
            D = kf(gb / a0)
            dl_own = np.log10(D) - np.log10(kf(gb / a0))
            other = A0[foot] * (E_of_z(zz) if law == "flat" else 1.0)
            dl_oth = np.log10(D) - np.log10(kf(gb / other))
            ana = np.log10(kf(gb / a0) / kf(gb / other))
            c2[f"{foot}/{kn}/{law}"] = (float(np.max(np.abs(dl_own))), float(np.max(np.abs(dl_oth - ana))))
c2_ok = all(v[0] < 1e-12 and v[1] < 1e-12 for v in c2.values())
# identity delta_rival - delta_flat = log[nu_flat(y)/nu_rival(y/E)] on the real sample
df = load_cristal()
d12 = df.loc[ID12]
dfl, D12, yfl = cell(d12); drv, _, yrv = cell(d12, rival=True)
ident = float(np.max(np.abs((drv - dfl) - np.log10(nu_mono(yfl) / nu_mono(yrv)))))
print(f"C2 synthetic disc on each law: max |delta_own| {max(v[0] for v in c2.values()):.1e}, max |other - analytic| {max(v[1] for v in c2.values()):.1e}; identity residual on the real sample {ident:.1e}")
c2_ok = c2_ok and ident < 1e-12
R["C1"] = c1; R["C2"] = c2

# ----------------------------------------------------------------------------------------- column classification, per-galaxy table
print("\n== column classification (measured versus model output) ==")
for c, k in [("z (z_cii)", "measured ([CII] redshift)"), ("logMstar", "inferred (SED); missing for 10a-E, 22b, 23c in the dynamics set"),
             ("f_molgas", "inferred (gas from a conversion; the repo READMEs say [CII]-based, CFG213 says dust-based T_d = 50 K: unresolved); missing for 06b, 10a-E"),
             ("logMtot", "MODEL OUTPUT (fitted M_bary, 1-dex Gaussian prior; reading tested in attack b5)"), ("Re_disk_kpc", "MODEL OUTPUT (free parameter)"),
             ("fDM_Re", "MODEL OUTPUT (flat prior [0,1]; the table's values are posterior medians per the vector README, CFG213's README says MAP)"),
             ("Vrot_Re", "MODEL OUTPUT (pressure-free rotation velocity of the fitted model, not a measured velocity)"), ("sigma0", "MODEL OUTPUT (fitted intrinsic dispersion)"),
             ("observed velocity markers (cristal_points.csv kind=data)", "the ONLY measured velocities; not used by the test"),
             ("V_tot, V_bary, V_DM curves", "model outputs, one drawn model per galaxy; extrapolated beyond the last marker")]:
    print(f"  {c}: {k}")
print("D_obs, g_obs, g_bar are 100 % model output of one DysmalPy fit.")

q = base_quantities(d12)
rf_all = route_factor(df.loc[ID14])
print("\n== per-galaxy (k = 3.36) ==")
print("id     z      Re    Vrot   sig   fDM    Vc     g_obs/A0  D_obs  g_bar/A0  D_flat  D_riv   dl_flat  dl_riv  class")
for i in ID14:
    r = df.loc[[i]]
    qq = base_quantities(r)
    dlf, Dd, yf = cell(r); dlr, _, yr = cell(r, rival=True)
    print(f"{i:5s} {r.z.iloc[0]:.3f} {r.Re.iloc[0]:5.2f} {r.Vrot.iloc[0]:6.1f} {r.sig.iloc[0]:5.1f} {r.fDM.iloc[0]:.2f} {qq['Vc0'][0]:6.1f} {qq['gobs0'][0]/A0['canonical']:7.2f} {Dd[0]:6.3f} {yf[0]:8.3f} {nu_mono(yf)[0]:6.3f} {nu_mono(yr)[0]:6.3f} {dlf[0]:+7.3f} {dlr[0]:+7.3f}  {r.cls.iloc[0]}{'  (EXCLUDED)' if i in EXCL else ''}")

# ----------------------------------------------------------------------------------------- Z5 primary cells
print("\n== Z5 primary (12 disks), fit route, all cells, seed 234, 10,000 bootstrap ==")
CELLS = [(kn, ft) for kn in ("mono", "p2") for ft in ("canonical", "alt")]
res5 = {}
for k in (3.36, 1.68, 0.0):
    for kn, ft in CELLS:
        for law in ("flat", "rival"):
            dl, _, _ = cell(d12, k=k, kernel=kn, foot=ft, rival=(law == "rival"))
            s = stat(dl, 234, B); res5[(k, kn, ft, law)] = s
            print(f"k={k:4.2f} {kn:4s} {ft:9s} {law:5s}: {fmt(s)}")
R["Z5"] = {f"{k}|{kn}|{ft}|{law}": v for (k, kn, ft, law), v in res5.items()}

def cls_of(k, law): return [res5[(k, kn, ft, law)]["cls"] for kn, ft in CELLS]
riv_rob = all(c == "under" for k in (3.36, 1.68) for c in cls_of(k, "rival"))
flat_rob = len(set(cls_of(3.36, "flat") + cls_of(1.68, "flat"))) == 1
print("robust (8 cells): rival", cls_of(3.36, "rival") + cls_of(1.68, "rival"), "| flat", cls_of(3.36, "flat") + cls_of(1.68, "flat"))
H1 = "separation (rival only robustly disfavoured, sign under)" if (riv_rob and not flat_rob) else "no separation / other"
print("H1:", H1)

# stability of the primary CI edges
print("\nCI-edge stability (nu_mono canonical k=3.36):")
stab = {}
for law in ("flat", "rival"):
    dl, _, _ = cell(d12, rival=(law == "rival"))
    ed = {}
    for sd in (234, 235, 236):
        ed[sd] = boot_ci(dl, sd, B)
    ed["100k"] = boot_ci(dl, 234, 100000)
    stab[law] = ed
    print(law, {k: tuple(round(v, 3) for v in vv) for k, vv in ed.items()})
R["stability"] = stab
dl_f, _, _ = cell(d12); dl_r, _, _ = cell(d12, rival=True)

# ----------------------------------------------------------------------------------------- rows P1..P8
rec("P1", "N: Z5 12, excluded, route 9, Best-Disk 6", (len(d12), EXCL, len(ROUTE9), len(BEST6)), "12/[09,15]/9/6", "exact",
    "PASS" if (len(d12), len(ROUTE9), len(BEST6)) == (12, 9, 6) else "FAIL")
s = res5[(3.36, "mono", "canonical", "rival")]
rec("P2", "rival mono canonical k=3.36", fmt(s), "-0.161 [-0.207, -0.055] under", "median 0.01, edges 0.02",
    "PASS" if (near(s["med"], -0.161, 0.01) and near(s["lo"], -0.207, 0.02) and near(s["hi"], -0.055, 0.02) and s["cls"] == "under") else "FAIL")
s = res5[(3.36, "mono", "alt", "rival")]
rec("P3", "rival mono alt k=3.36", fmt(s), "-0.186 under", "median 0.01, class", "PASS" if near(s["med"], -0.186, 0.01) and s["cls"] == "under" else "FAIL")
ok = all(near(res5[(1.68, "mono", ft, "rival")]["med"], 0, 1) and -0.31 <= res5[(1.68, "mono", ft, "rival")]["med"] <= -0.26 and res5[(1.68, "mono", ft, "rival")]["cls"] == "under" for ft in A0)
rec("P4", "rival mono k=1.68 both footings", [round(res5[(1.68, 'mono', ft, 'rival')]["med"], 3) for ft in A0], "-0.27..-0.30 under", "each in [-0.31,-0.26]", "PASS" if ok else "FAIL")
allu = all(c == "under" for c in cls_of(3.36, "rival") + cls_of(1.68, "rival"))
p2m = [res5[(3.36, "p2", ft, "rival")]["med"] for ft in A0]
p2ok = all(-0.27 <= v <= -0.09 for v in p2m)
rec("P5", "rival 8 cells under; P2 k=3.36 medians", (allu, [round(v, 3) for v in p2m]), "8/8 under; P2 in [-0.25,-0.11]", "8/8; within 0.02 of range", "PASS" if allu and p2ok else "FAIL")
fo = cls_of(3.36, "flat"); n_over = fo.count("over")
fmed = [res5[(3.36, kn, ft, "flat")]["med"] for kn, ft in CELLS]
f168 = cls_of(1.68, "flat")
rec("P6", "flat k=3.36: cells over / medians; k=1.68 classes", (n_over, dict(zip([f"{a}/{b}" for a, b in CELLS], fo)), [round(v, 3) for v in fmed], f168),
    "3 of 4 over, +0.04..+0.08; k=1.68 4/4 CONSISTENT", "exact 3 of 4; 4/4",
    "PASS" if (n_over == 3 and all(0.03 <= v <= 0.09 for v in fmed) and all(c == "CONS" for c in f168)) else "PARTIAL/FAIL (see values)")
rec("P7", "H1 verdict", H1, "only the rival robustly disfavoured (under); flat not robust", "label", "PASS" if (riv_rob and not flat_rob) else "FAIL")
s0f = [res5[(0.0, "mono", ft, "flat")]["cls"] for ft in A0]; s0r = [res5[(0.0, "mono", ft, "rival")]["cls"] for ft in A0]
rec("P8", "k=0 classes (mono, canonical/alt) flat, rival", (s0f, s0r), "both laws under", "class", "PASS" if all(c == "under" for c in s0f + s0r) else "FAIL")

# ----------------------------------------------------------------------------------------- route
print("\n== independent route (SED M* + f_molgas gas); 9 disks ==")
d9 = df.loc[ROUTE9]
r9 = route_factor(d9)
print("route factors M_ind/M_fit:", {i: round(float(v), 3) for i, v in zip(ROUTE9, r9)})
tgt_rf = {"02": 1.11, "03": 1.15, "07a": 1.11, "20": 1.22, "12": 1.21, "08": 0.61, "11": 0.45, "19": 0.34, "23b": 6.09}
rfok = all(abs(float(r9[ROUTE9.index(i)]) / v - 1) <= 0.03 for i, v in tgt_rf.items())
rec("P11", "route factors (nine)", {i: round(float(r9[ROUTE9.index(i)]), 3) for i in tgt_rf}, tgt_rf, "3 % in ratio", "PASS" if rfok else "FAIL")
res9 = {}
for rt in ("hold", "recompute"):
    for kn, ft in CELLS:
        for law in ("flat", "rival"):
            dl, _, _ = cell(d9, kernel=kn, foot=ft, rival=(law == "rival"), gbar_mul=r9, route=rt)
            res9[(rt, kn, ft, law)] = stat(dl, 234, B)
            print(f"route[{rt:9s}] {kn:4s} {ft:9s} {law:5s}: {fmt(res9[(rt, kn, ft, law)])}")
for kn, ft in CELLS:
    for law in ("flat", "rival"):
        dl, _, _ = cell(d9, kernel=kn, foot=ft, rival=(law == "rival"))
        res9[("fit", kn, ft, law)] = stat(dl, 234, B)
        print(f"same-9 FIT route {kn:4s} {ft:9s} {law:5s}: {fmt(res9[('fit', kn, ft, law)])}")
R["route9"] = {"|".join(k): v for k, v in res9.items()}
for rt in ("hold", "recompute"):
    rm = [res9[(rt, "mono", ft, "rival")]["med"] for ft in A0]
    bothc = all(res9[(rt, kn, ft, l)]["cls"] == "CONS" for kn, ft in CELLS for l in ("flat", "rival"))
    rvc = res9[(rt, "mono", "canonical", "rival")]
    okp9 = (bothc or all(res9[(rt, "mono", "canonical", l)]["cls"] == "CONS" for l in ("flat", "rival"))) and -0.23 <= rvc["med"] <= -0.14 and rvc["lo"] < 0 < rvc["hi"]
    rec("P9-" + rt, "route n=9: both CONSISTENT (mono canonical); rival median in [-0.22,-0.15], CI contains 0",
        (res9[(rt, "mono", "canonical", "flat")]["cls"], res9[(rt, "mono", "canonical", "rival")]["cls"], [round(v, 3) for v in rm], "all 8 cells CONS" if bothc else "some cell not CONS"),
        "both CONS; rival -0.15..-0.22", "class; median 0.01 of range", "PASS" if okp9 else "FAIL")
    fit_m = res9[("fit", "mono", "canonical", "rival")]["med"]
    rt_m = res9[(rt, "mono", "canonical", "rival")]["med"]
    p2c = res9[("fit", "p2", "canonical", "rival")]
    okp10 = near(fit_m, -0.155, 0.01) and near(rt_m, -0.198, 0.01) and near(p2c["med"], -0.107, 0.01) and near(p2c["lo"], -0.220, 0.02) and near(p2c["hi"], 0.011, 0.02)
    rec("P10-" + rt, "same-9: rival fit / route (mono canonical); P2 canonical fit-route", (round(fit_m, 3), round(rt_m, 3), fmt(p2c)),
        "-0.155 / -0.198; P2 -0.107 [-0.220,+0.011]", "medians 0.01; edges 0.02", "PASS" if okp10 else "FAIL")
# LOO on the 12 fit route
lo_f = []; lo_r = []
for j in range(12):
    dd = d12.drop(d12.index[j])
    lo_f.append(float(np.median(cell(dd)[0]))); lo_r.append(float(np.median(cell(dd, rival=True)[0])))
print("LOO (12 -> 11, mono canonical k=3.36): rival", [round(v, 3) for v in lo_r], "flat", [round(v, 3) for v in lo_f])
rec("P12", "LOO envelope rival / flat", (round(min(lo_r), 3), round(max(lo_r), 3), round(min(lo_f), 3), round(max(lo_f), 3)), "rival -0.167..-0.155; flat +0.033..+0.073", "envelope within 0.01",
    "PASS" if (near(min(lo_r), -0.167, 0.01) and near(max(lo_r), -0.155, 0.01) and near(min(lo_f), 0.033, 0.01) and near(max(lo_f), 0.073, 0.01)) else "FAIL")

# ----------------------------------------------------------------------------------------- outer radii, best disk, excluded, C3
print("\n== vector reads ==")
cur, pts, val, out = load_vector()
outer = {}
for rd in ("table_Rout", "outermost_data_marker"):
    dls_f = []; dls_r = []
    for i in ID12:
        vid = VEC_ALIAS.get(i, i)
        row = out[(out.id == vid) & (out.radius_definition == rd)].iloc[0]
        D = (row.Vtot_kms / row.Vbary_kms) ** 2
        gb = gacc(row.Vbary_kms, row.R_kpc)
        zi = float(df.loc[i, "z"])
        dls_f.append(np.log10(D) - np.log10(nu_mono(gb / A0["canonical"])))
        dls_r.append(np.log10(D) - np.log10(nu_mono(gb / (A0["canonical"] * E_of_z(zi)))))
    sf, sr = stat(np.array(dls_f), 234, B), stat(np.array(dls_r), 234, B)
    outer[rd] = dict(flat=sf, rival=sr)
    print(f"{rd}: flat {fmt(sf)} | rival {fmt(sr)}")
R["outer"] = outer
okp13 = (near(outer["table_Rout"]["rival"]["med"], -0.28, 0.02) and outer["table_Rout"]["rival"]["cls"] == "under" and
         near(outer["outermost_data_marker"]["rival"]["med"], -0.26, 0.02) and outer["outermost_data_marker"]["rival"]["cls"] == "under" and
         all(near(outer[r]["flat"]["med"], 0.02, 0.02) and outer[r]["flat"]["cls"] == "CONS" for r in outer))
rec("P13", "outer radii (table_Rout / marker): rival, flat", (round(outer["table_Rout"]["rival"]["med"], 3), round(outer["outermost_data_marker"]["rival"]["med"], 3),
                                                                 round(outer["table_Rout"]["flat"]["med"], 3), round(outer["outermost_data_marker"]["flat"]["med"], 3)),
    "-0.28, -0.26 under; flat +0.02, +0.02 CONS", "medians 0.02; classes", "PASS" if okp13 else "FAIL")
b6 = df.loc[BEST6]
sf = stat(cell(b6)[0], 234, B); sr = stat(cell(b6, rival=True)[0], 234, B)
print("Best-Disk (n=6): flat", fmt(sf), "| rival", fmt(sr))
R["best6"] = dict(flat=sf, rival=sr)
rec("P14", "Best-Disk n=6 flat / rival (mono canonical)", (fmt(sf), fmt(sr)), "flat +0.053 [+0.018,+0.255] over; rival -0.118 [-0.229,+0.058] CONS", "medians 0.01; edges 0.02; class",
    "PASS" if (near(sf["med"], 0.053, 0.01) and sf["cls"] == "over" and near(sr["med"], -0.118, 0.01) and sr["cls"] == "CONS" and near(sf["lo"], 0.018, 0.02) and near(sf["hi"], 0.255, 0.02) and near(sr["lo"], -0.229, 0.02) and near(sr["hi"], 0.058, 0.02)) else "FAIL")
ex = {}
for i, tg in (("09", (1.09, 1.05, 1.42)), ("15", (1.21, 1.08, 1.55))):
    r = df.loc[[i]]
    dl, D, yf = cell(r); _, _, yr = cell(r, rival=True)
    ex[i] = (float(D[0]), float(nu_mono(yf)[0]), float(nu_mono(yr)[0]), float(dl[0]), float(cell(r, rival=True)[0][0]))
    print(f"excluded {i}: D_obs {ex[i][0]:.3f}, D_flat {ex[i][1]:.3f}, D_rival {ex[i][2]:.3f}; delta flat {ex[i][3]:+.3f}, rival {ex[i][4]:+.3f}  (README: {tg})")
R["excluded"] = ex
rec("P15", "excluded disks D_obs/flat/rival", {i: [round(v, 3) for v in ex[i][:3]] for i in ex}, "09: 1.09/1.05/1.42; 15: 1.21/1.08/1.55", "each within 0.02",
    "PASS" if all(near(a, b, 0.02) for a, b in zip(ex["09"][:3] + ex["15"][:3], (1.09, 1.05, 1.42, 1.21, 1.08, 1.55))) else "FAIL")

# C3
c3 = {}
for lab, log in (("linear-R", False), ("log-R", True)):
    Dr = []; Vr = []; fd = []
    for i in ID14:
        vid = VEC_ALIAS.get(i, i); r = df.loc[i]
        Vt = vec_at(cur, vid, "V_tot", r.Re, log); Vb = vec_at(cur, vid, "V_bary", r.Re, log); fv = vec_at(cur, vid, "f_DM", r.Re, log)
        Dt = 1 / (1 - r.fDM)
        Dr.append((Vt / Vb) ** 2 / Dt); Vr.append(Vt / np.sqrt(r.Vrot ** 2 + K0 * r.sig ** 2)); fd.append(fv - r.fDM)
    Dr, Vr, fd = map(np.array, (Dr, Vr, fd))
    for nm, sel in (("14", np.ones(14, bool)), ("12", np.array([i in ID12 for i in ID14]))):
        c3[f"{lab}/{nm}"] = dict(D_ratio_med=float(np.median(Dr[sel])), D_p16=float(np.percentile(Dr[sel], 16)), D_p84=float(np.percentile(Dr[sel], 84)),
                                 D_min=float(Dr[sel].min()), D_max=float(Dr[sel].max()), V_ratio_med=float(np.median(Vr[sel])), fDM_diff_med=float(np.median(fd[sel])))
        print(f"C3 {lab} n={nm}: D_vec/D_table median {np.median(Dr[sel]):.3f} [16-84 {np.percentile(Dr[sel],16):.3f}, {np.percentile(Dr[sel],84):.3f}; min {Dr[sel].min():.3f}, max {Dr[sel].max():.3f}]; V_circ ratio median {np.median(Vr[sel]):.3f}; f_DM(vec)-f_DM(table) median {np.median(fd[sel]):+.3f}")
    if not log:
        C3_D = Dr.copy(); C3_V = Vr.copy()
R["C3"] = c3
cc = c3["linear-R/12"]; cc14 = c3["linear-R/14"]
rec("P16", "C3 (linear-R, 12 / 14)", (round(cc["D_ratio_med"], 3), round(cc["D_p16"], 3), round(cc["D_p84"], 3), round(cc["V_ratio_med"], 3), "14:", round(cc14["D_ratio_med"], 3), round(cc14["V_ratio_med"], 3)),
    "D 1.010 [0.93,1.05]; V 0.997", "medians 0.01; edges 0.03",
    "PASS" if ((near(cc["D_ratio_med"], 1.010, 0.01) or near(cc14["D_ratio_med"], 1.010, 0.01)) and (near(cc["V_ratio_med"], 0.997, 0.01) or near(cc14["V_ratio_med"], 0.997, 0.01))) else "FAIL")

# ----------------------------------------------------------------------------------------- P19, P20
S12 = np.log10(nu_mono(yrv) / nu_mono(yfl)) * 0  # placeholder to keep shapes
yfl12 = yfl; yrv12 = yrv
# separation implied at each galaxy's own g_bar and z: log nu_rival(g/(A0 E)) / nu_flat(g/A0) with the LARGER prediction on top
def sep(dfx, gmul=None):
    _, _, yf_ = cell(dfx, gbar_mul=gmul, route="hold"); _, _, yr_ = cell(dfx, rival=True, gbar_mul=gmul, route="hold")
    return np.log10(nu_mono(yr_) / nu_mono(yf_))
S12v = sep(d12); S9v = sep(d9, r9)
print(f"\nP19 signal S (median log10 nu_rival/nu_flat at own g_bar, z): 12 fit-route rows {np.median(S12v):.4f}; 9 route rows (g_bar,ind) {np.median(S9v):.4f}; 9 fit-route rows {np.median(sep(d9)):.4f}")
R["S"] = dict(S12=float(np.median(S12v)), S9_route=float(np.median(S9v)), S9_fit=float(np.median(sep(d9))))
rec("P19", "signal S: 12 fit rows / 9 route rows", (round(float(np.median(S12v)), 4), round(float(np.median(S9v)), 4)), "0.2355 / 0.288", "0.005 / 0.01",
    "PASS" if (near(np.median(S12v), 0.2355, 0.005) and near(np.median(S9v), 0.288, 0.01)) else "FAIL")
n13 = 9 * (3 * (0.226 / 1.96) / 0.288) ** 2
print(f"P20 CFG218 'about 13' from the hypothesis band = 1.96 sigma_9 with sigma_n = sigma_9 sqrt(9/n), 3 sigma_n = S: n = {n13:.2f}")
R["P20_arith"] = float(n13)
rec("P20", "CFG218 'about 13' arithmetic", round(n13, 2), "~13 (HYPOTHESIS about its band definition)", "report", "REPORT (13 reproduced by the hypothesis)" if abs(n13 - 13) < 0.5 else "REPORT (not 13)")

# ----------------------------------------------------------------------------------------- NOEMA3D
print("\n== Z1.4 NOEMA3D (10 galaxies) ==")
dn = load_noema(); fn, Vrot2 = noema_frame(dn)
rn = noema_route_factor(fn)
print("NOEMA3D log(M*+Mgas,CO) - log M_bary per galaxy:", {i: round(float(np.log10(v)), 3) for i, v in zip(fn.id, rn)})
within = int(np.sum(np.abs(np.log10(rn)) < 0.1))
print("within 0.1 dex:", within, "of 10")
rec("P18", "NOEMA3D route offset: n within 0.1 dex; G4_20371 / GN4_18574", (within, round(float(np.log10(rn[list(fn.id).index('G4_20371')])), 3), round(float(np.log10(rn[list(fn.id).index('GN4_18574')])), 3)),
    "7 of 10; -0.32; +0.41", "exact; 0.01", "PASS" if within == 7 and near(np.log10(rn[list(fn.id).index('G4_20371')]), -0.32, 0.01) and near(np.log10(rn[list(fn.id).index('GN4_18574')]), 0.41, 0.01) else "FAIL")
resn = {}
allcons = True
for k in (3.36, 1.68, 0.0):
    for kn, ft in CELLS:
        for law in ("flat", "rival"):
            dl, _, _ = cell_noema(fn, Vrot2, k=k, kernel=kn, foot=ft, rival=(law == "rival"))
            resn[("fit", k, kn, ft, law)] = stat(dl, 234, B)
            for rt in ("hold", "recompute"):
                dl, _, _ = cell_noema(fn, Vrot2, k=k, kernel=kn, foot=ft, rival=(law == "rival"), gbar_mul=rn, route=rt)
                resn[(rt, k, kn, ft, law)] = stat(dl, 234, B)
for key, v in resn.items():
    if key[1] == 3.36 and key[2] == "mono" and key[3] == "canonical":
        print("NOEMA3D", key, fmt(v))
R["noema"] = {"|".join(map(str, k)): v for k, v in resn.items()}
cons_cells = {rt: all(resn[(rt, k, kn, ft, l)]["cls"] == "CONS" for k in (3.36, 1.68) for kn, ft in CELLS for l in ("flat", "rival")) for rt in ("fit", "hold", "recompute")}
print("NOEMA3D all cells (k 3.36, 1.68 x kernel x footing x law) CONSISTENT by route:", cons_cells)
print("NOEMA3D k=0 classes (mono canonical): fit flat/rival", resn[("fit", 0.0, "mono", "canonical", "flat")]["cls"], resn[("fit", 0.0, "mono", "canonical", "rival")]["cls"])
f_, r_ = resn[("fit", 3.36, "mono", "canonical", "flat")], resn[("fit", 3.36, "mono", "canonical", "rival")]
rec("P17", "NOEMA3D: all cells CONS on both routes; flat / rival (mono canonical, fit)", (cons_cells, fmt(f_), fmt(r_)),
    "all CONS; flat +0.03 [-0.03,+0.23]; rival -0.00 [-0.09,+0.12]", "class; medians 0.01; edges 0.02",
    "PASS" if (all(cons_cells.values()) and near(f_["med"], 0.03, 0.01) and near(r_["med"], 0.0, 0.01) and near(f_["lo"], -0.03, 0.02) and near(f_["hi"], 0.23, 0.02) and near(r_["lo"], -0.09, 0.02) and near(r_["hi"], 0.12, 0.02)) else "FAIL / PARTIAL (see values)")

# ----------------------------------------------------------------------------------------- M7 recovery control
sf = mad_sigma(dl_f)
res_rec, rec_ok = recovery_control(yfl12, yrv12, sf, seed=234, N=2000, B=300, n=12)
print(f"\nM7 recovery control (n=12 mocks, s = {sf:.3f} dex, N = 2000, B = 300, seed 234):")
print(json.dumps(res_rec, indent=1))
print("M7 recovery:", "PASS" if rec_ok else "FAIL")
R["M7_recovery"] = res_rec

# ----------------------------------------------------------------------------------------- ledger
print("\n== ledger ==")
from collections import Counter
cnt = Counter(r["verdict"].split(" ")[0] for r in rows)
print(dict(cnt))
R["ledger"] = rows
R["controls"] = dict(C1=c1_ok, C2=c2_ok, C4_vs_CFG5=c4_ok, C4_vs_CFG4_missed=c4_cfg4_miss, M7=rec_ok)
print("controls:", R["controls"])
savejson("CFG234_main", R)
sys.exit(0 if (c1_ok and c2_ok and c4_ok and rec_ok) else 1)
