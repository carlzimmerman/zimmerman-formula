"""CFG234 attack (d): vector-versus-table consistency (C3 by id), the input-error scan, the two excluded discs (n=14 with table values; n=14 with
the vector's drawn models), and an all-vector version. Reports; exit 0."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CFG234_common import *

t = start("CFG234_attack_d")
B = 10000
df = load_cristal(); d12 = df.loc[ID12]; d14 = df.loc[ID14]
cur, pts, val, out = load_vector()
R = {}
CELLS = [("mono", "canonical"), ("mono", "alt"), ("p2", "canonical"), ("p2", "alt")]

print("== d1: C3 by id at the table R_e (linear-R) ==")
print("id     D_table  D_vec   ratio | Vcirc_table  V_tot,vec  ratio | fDM_table fDM_vec")
d1 = {}
for i in ID14:
    vid = VEC_ALIAS.get(i, i); r = df.loc[i]
    Vt = vec_at(cur, vid, "V_tot", r.Re); Vb = vec_at(cur, vid, "V_bary", r.Re); fv = vec_at(cur, vid, "f_DM", r.Re)
    Dt = 1 / (1 - r.fDM); Dv = (Vt / Vb) ** 2; Vc = np.sqrt(r.Vrot ** 2 + K0 * r.sig ** 2)
    d1[i] = dict(D_table=Dt, D_vec=Dv, V_table=Vc, V_vec=Vt, f_table=r.fDM, f_vec=fv)
    print(f"{i:5s} {Dt:8.3f} {Dv:7.3f} {Dv/Dt:6.3f} | {Vc:8.1f} {Vt:9.1f} {Vt/Vc:6.3f} | {r.fDM:.2f} {fv:.3f}{'   (EXCLUDED)' if i in EXCL else ''}")
R["d1"] = d1

print("\n== d2: input-error scan from cristal_validation.csv (deviations in the table's own sigmas) ==")
val2 = val.copy(); val2["idt"] = val2.id.map(lambda x: {"10a": "10a-E"}.get(x, x))
flag = []
for _, r in val2.iterrows():
    devs = [r.sigma0_dev_in_table_sigmas, r.Re_dev_in_table_sigmas, r.fDM_dev_in_table_sigmas]
    mx = np.nanmax(np.abs(devs))
    print(f"  {r.idt:5s}: sigma_0 {r.sigma0_dev_in_table_sigmas:+7.2f}, R_e {r.Re_dev_in_table_sigmas:+7.2f}, f_DM {r.fDM_dev_in_table_sigmas:+6.2f}  max|dev| {mx:6.2f}{'  <-- > 2' if mx > 2 else ''}{'  (in the 12)' if r.idt in ID12 else '  (excluded / not in the 12)'}")
    if mx > 2: flag.append(r.idt)
print("flagged > 2 table-sigmas:", flag, "| of which in the 12:", [i for i in flag if i in ID12])
# leave out each disc with max|dev| > 1 in the 12 (and each flagged), class unchanged?
maxdev = {r.idt: float(np.nanmax(np.abs([r.sigma0_dev_in_table_sigmas, r.Re_dev_in_table_sigmas, r.fDM_dev_in_table_sigmas]))) for _, r in val2.iterrows()}
loo = {}
for i in [j for j in ID12 if maxdev.get(j, 0) > 1.0] + [j for j in flag if j in ID12]:
    dd = d12.drop(i)
    loo[i] = {law: stat(cell(dd, rival=(law == "rival"))[0], 234, B) for law in ("flat", "rival")}
    print(f"  leave out {i} (max|dev| {maxdev[i]:.2f}): flat {fmt(loo[i]['flat'])} | rival {fmt(loo[i]['rival'])}")
R["d2"] = dict(flagged=flag, loo=loo)

print("\n== d3: include the two excluded discs ==")
base = {}
for k in (3.36, 1.68):
    for kn, ft in CELLS:
        for law in ("flat", "rival"):
            base[(k, kn, ft, law)] = (stat(cell(d12, k=k, kernel=kn, foot=ft, rival=(law == "rival"))[0], 234, B),
                                      stat(cell(d14, k=k, kernel=kn, foot=ft, rival=(law == "rival"))[0], 234, B))
n_change = 0
for key, (s12, s14) in base.items():
    ch = s12["cls"] != s14["cls"]; n_change += ch
    if key[0] == 3.36 or ch:
        print(f"  k={key[0]:4.2f} {key[1]:4s} {key[2]:9s} {key[3]:5s}: n=12 {fmt(s12)} -> n=14 {fmt(s14)}{'   CLASS CHANGES' if ch else ''}")
print("classes that change when 09 and 15 are included (16 cells):", n_change)
riv14 = [base[(k, kn, ft, "rival")][1]["cls"] for k in (3.36, 1.68) for kn, ft in CELLS]
fl14 = [base[(k, kn, ft, "flat")][1]["cls"] for k in (3.36, 1.68) for kn, ft in CELLS]
print("n=14 robustness: rival", riv14, "| flat", fl14)
print("H1 with n=14:", "separation (rival only robustly under)" if all(c == "under" for c in riv14) and len(set(fl14)) > 1 else "changed")
R["d3_table"] = {"|".join(map(str, k)): dict(n12=v[0], n14=v[1]) for k, v in base.items()}
primary_harmless = all(base[(3.36, "mono", "canonical", l)][0]["cls"] == base[(3.36, "mono", "canonical", l)][1]["cls"] for l in ("flat", "rival"))
print("frozen rule: exclusion HARMLESS iff the primary-cell classes of both laws are unchanged:", primary_harmless)

# vector drawn models at the figure's own R_e
print("\n  d3b: n=14 with the vector's drawn models at the figure's own R_e line (D = (V_tot/V_bary)^2, g_bar = V_bary^2 / R):")
vrows = {}
for i in ID14:
    vid = VEC_ALIAS.get(i, i)
    Rfig = float(val[val.id == vid].Re_figure_line_kpc.iloc[0])
    Vt = vec_at(cur, vid, "V_tot", Rfig); Vb = vec_at(cur, vid, "V_bary", Rfig)
    D = (Vt / Vb) ** 2; gb = gacc(Vb, Rfig); z = float(df.loc[i, "z"])
    vrows[i] = dict(R=Rfig, D=D, gbar=gb, z=z)
def vec_delta(ids, rival, kernel="mono", foot="canonical"):
    return np.array([np.log10(vrows[i]["D"]) - np.log10(KERN[kernel](vrows[i]["gbar"] / (A0[foot] * (E_of_z(vrows[i]["z"]) if rival else 1.0)))) for i in ids])
d3b = {}
for nm, ids in (("12", ID12), ("14", ID14)):
    sf = stat(vec_delta(ids, False), 234, B); sr = stat(vec_delta(ids, True), 234, B)
    d3b[nm] = dict(flat=sf, rival=sr)
    print(f"   n={nm}: flat {fmt(sf)} | rival {fmt(sr)}")
for i in EXCL:
    print(f"   {i}: table R_e {df.loc[i,'Re']} vs figure R_e {vrows[i]['R']:.2f} kpc; figure D {vrows[i]['D']:.3f} (table {1/(1-df.loc[i,'fDM']):.3f}); delta flat {vec_delta([i], False)[0]:+.3f}, rival {vec_delta([i], True)[0]:+.3f}")
R["d3b"] = d3b

print("\n== d5: all-vector version at the TABLE R_e (D_vec, g_bar,vec) against the table version, per galaxy ==")
diffs = {"flat": [], "rival": []}
for i in ID14:
    vid = VEC_ALIAS.get(i, i); r = df.loc[i]
    Vt = vec_at(cur, vid, "V_tot", r.Re); Vb = vec_at(cur, vid, "V_bary", r.Re)
    D = (Vt / Vb) ** 2; gb = gacc(Vb, r.Re)
    for law in ("flat", "rival"):
        dv = np.log10(D) - np.log10(nu_mono(gb / (A0["canonical"] * (E_of_z(r.z) if law == "rival" else 1.0))))
        dt = cell(df.loc[[i]], rival=(law == "rival"))[0][0]
        diffs[law].append(dv - dt)
for law in diffs:
    a = np.array(diffs[law]); sel = np.array([i in ID12 for i in ID14])
    print(f"  {law}: median |vector - table| delta, 12 disks {np.median(np.abs(a[sel])):.3f}, max {np.max(np.abs(a[sel])):.3f}; 14: max {np.max(np.abs(a)):.3f} (argmax {ID14[int(np.argmax(np.abs(a)))]})")
vt12 = {law: stat(np.array([np.log10((vec_at(cur, VEC_ALIAS.get(i, i), 'V_tot', df.loc[i, 'Re']) / vec_at(cur, VEC_ALIAS.get(i, i), 'V_bary', df.loc[i, 'Re'])) ** 2) -
                            np.log10(nu_mono(gacc(vec_at(cur, VEC_ALIAS.get(i, i), 'V_bary', df.loc[i, 'Re']), df.loc[i, 'Re']) / (A0['canonical'] * (E_of_z(df.loc[i, 'z']) if law == 'rival' else 1.0))))
                            for i in ID12]), 234, B) for law in ("flat", "rival")}
print("  all-vector (table R_e) 12 disks: flat", fmt(vt12["flat"]), "| rival", fmt(vt12["rival"]))
R["d5"] = dict(vt12=vt12, max_abs_12={law: float(np.max(np.abs(np.array(diffs[law])[np.array([i in ID12 for i in ID14])]))) for law in diffs})
savejson("CFG234_attack_d", R)
sys.exit(0)
