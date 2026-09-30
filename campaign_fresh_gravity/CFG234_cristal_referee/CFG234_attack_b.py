"""CFG234 attack (b): the independent route (SED M* + gas), its gas bracket, blended components, alias/provenance, the M_bary reading test,
NOEMA3D gas bracket, and the post-freeze strict-class-A subsets (dust-DETECTED gas). Reports; exit 0."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CFG234_common import *

t = start("CFG234_attack_b")
B = 10000
df = load_cristal(); d9 = df.loc[ROUTE9]
R = {}


def mind(d, g=1.0, zp=0.0):
    f = d.f_molgas.values
    return 10 ** (d.logMstar.values + zp) * (1.0 + g * f / (1.0 - f))


def run(d, rmul, rt, kernel="mono", foot="canonical"):
    return {law: stat(cell(d, kernel=kernel, foot=foot, rival=(law == "rival"), gbar_mul=rmul, route=rt)[0], 234, B) for law in ("flat", "rival")}


def line(tag, res):
    return f"{tag}: flat {fmt(res['flat'])} | rival {fmt(res['rival'])}"


print("== b4: alias and provenance map (which table row feeds which id) ==")
smp = pd.read_csv(os.path.join(AT, "cristal2025_sample.csv")).set_index("id")
for i in ID14:
    sid = SAMPLE_ALIAS.get(i, i); vid = VEC_ALIAS.get(i, i)
    host = smp.loc[sid, "name"]
    sib = [j for j in smp.index if j != sid and j[:2] == sid[:2]]
    print(f"dyn {i:5s} -> sample/kin {sid:5s} | vector {vid:4s} | host '{host}' | M* {df.loc[i,'logMstar']} f_molgas {df.loc[i,'f_molgas']} | sibling components in the sample: {sib}")
print("Note: dynamics `10a-E` = vector `10a` (validation.csv R_e and sigma_0 match 10a-E, not sample `10a`); dynamics `09` = sample/kin `09a`.\n"
      "23a/23b/23c share one host name (DEIMOS_COSMOS_818760); 04a/04b, 06a/06b, 22a/22b likewise: a per-component SED M* is only as good as the deblending.")

print("\n== b1: route under both readings (mono canonical, n=9) ==")
r9 = route_factor(d9)
b1 = {}
for rt in ("hold", "recompute"):
    b1[rt] = run(d9, r9, rt); print(line(f"reading {rt}", b1[rt]))
b1["fit"] = {law: stat(cell(d9, rival=(law == "rival"))[0], 234, B) for law in ("flat", "rival")}; print(line("same 9, fit route", b1["fit"]))
R["b1"] = b1
print("Reading matching CFG213's README (both CONSISTENT on the route; rival -0.15..-0.22): recompute (D_ind = g_obs/g_bar,ind). The literal 'hold f_DM' reading leaves the rival DISFAVOURED-under.")

print("\n== b2: gas bracket x {1/3,1/2,1,2,3} x M* zero point {-0.2,0,+0.2} dex; mono; both footings; both readings ==")
GS = [1 / 3, 0.5, 1.0, 2.0, 3.0]; ZP = [-0.2, 0.0, 0.2]
b2 = {}
for foot in ("canonical", "alt"):
    for rt in ("recompute", "hold"):
        print(f"-- footing {foot}, reading {rt}: cell = (gas, M*zp): flat median/class | rival median/class")
        for zp in ZP:
            for g in GS:
                rm = mind(d9, g, zp) / 10 ** d9.logMtot.values
                res = run(d9, rm, rt, foot=foot)
                b2[f"{foot}|{rt}|{g:.3f}|{zp}"] = res
                print(f"   g={g:.2f} zp={zp:+.1f}: flat {res['flat']['med']:+.3f} {res['flat']['cls']:5s} | rival {res['rival']['med']:+.3f} {res['rival']['cls']:5s}")
R["b2"] = b2
for foot in ("canonical",):
    for rt in ("recompute", "hold"):
        for law in ("flat", "rival"):
            cl = {k: v[law]["cls"] for k, v in b2.items() if k.startswith(f"{foot}|{rt}|")}
            meds = [v[law]["med"] for k, v in b2.items() if k.startswith(f"{foot}|{rt}|")]
            m0 = b2[f"{foot}|{rt}|1.000|0.0"][law]["med"]
            shift = b2[f"{foot}|{rt}|2.000|0.0"][law]["med"] - b2[f"{foot}|{rt}|0.500|0.0"][law]["med"]
            print(f"SUMMARY {foot} {rt} {law}: classes over the 15 cells {sorted(set(cl.values()))} (counts { {c: list(cl.values()).count(c) for c in sorted(set(cl.values()))} }); median range [{min(meds):+.3f},{max(meds):+.3f}]; "
                  f"shift g 1/2 -> 2 at zp 0: {shift:+.3f}; half-range of the 15 medians (sigma_sys candidate) {(max(meds)-min(meds))/2:.3f}")
R["b2_sigma_sys"] = {f"{rt}|{law}": (max(v[law]["med"] for k, v in b2.items() if k.startswith(f"canonical|{rt}|")) - min(v[law]["med"] for k, v in b2.items() if k.startswith(f"canonical|{rt}|"))) / 2
                     for rt in ("recompute", "hold") for law in ("flat", "rival")}
# smallest gas factor that changes each law's class (fine scan, zp = 0)
print("\nb2 fine scan of the gas factor g (zp = 0), mono canonical: class of each law")
gs_fine = 10 ** np.arange(-1.0, 1.001, 0.05)
scan = {}
for rt in ("recompute", "hold"):
    prev = None
    for g in gs_fine:
        rm = mind(d9, g, 0.0) / 10 ** d9.logMtot.values
        res = run(d9, rm, rt)
        cur = (res["flat"]["cls"], res["rival"]["cls"])
        scan[f"{rt}|{g:.3f}"] = dict(flat=res["flat"], rival=res["rival"])
        if cur != prev:
            print(f"  [{rt:9s}] g = {g:.3f}: flat {res['flat']['cls']:5s} ({res['flat']['med']:+.3f}), rival {res['rival']['cls']:5s} ({res['rival']['med']:+.3f})")
            prev = cur
R["b2_scan"] = scan

print("\n== b3: blended components and upper-limit gas ==")
sets = {"9 (CFG213 route set)": ROUTE9,
        "8 (drop 23b: SED M* of a 3-component host, route factor 6.1)": [i for i in ROUTE9 if i != "23b"],
        "6 dust-DETECTED (02 03 07a 11 19 20; post-freeze class-A CRISTAL subset)": DETECTED6,
        "3 upper-limit-gas discs only (08 12 23b)": ["08", "12", "23b"],
        "7 (9 minus 08 and 12)": [i for i in ROUTE9 if i not in ("08", "12")],
        "8 (9 minus 08)": [i for i in ROUTE9 if i != "08"], "8 (9 minus 12)": [i for i in ROUTE9 if i != "12"]}
b3 = {}
for nm, ids in sets.items():
    d = df.loc[ids]; rf = route_factor(d)
    fit = {law: stat(cell(d, rival=(law == "rival"))[0], 234, B) for law in ("flat", "rival")}
    rc = run(d, rf, "recompute"); hd = run(d, rf, "hold")
    b3[nm] = dict(fit=fit, recompute=rc, hold=hd)
    print(f"-- {nm} (n={len(ids)})")
    print("   ", line("fit route ", fit)); print("   ", line("route recompute", rc)); print("   ", line("route hold", hd))
    p2 = {law: stat(cell(d, kernel='p2', rival=(law == 'rival'), gbar_mul=rf, route='recompute')[0], 234, B) for law in ("flat", "rival")}
    alt = run(d, rf, "recompute", foot="alt")
    print("   ", line("route recompute P2 canonical", p2)); print("   ", line("route recompute mono alt", alt))
    b3[nm]["p2"] = p2; b3[nm]["alt"] = alt
R["b3"] = b3

print("\n== b5: is logMtot the fitted baryon mass? vector V_bary^2 R / G against 10^logMtot ==")
cur, pts, val, out = load_vector()
b5 = {}
ratios_out = []; ratios_far = []
for i in ID14:
    vid = VEC_ALIAS.get(i, i)
    row = out[(out.id == vid) & (out.radius_definition == "outermost_data_marker")].iloc[0]
    Mv = (row.Vbary_kms * 1e3) ** 2 * (row.R_kpc * KPC) / G / MSUN
    Mfit = 10 ** df.loc[i, "logMtot"]
    Rc, Vb = vec_curve(cur, vid, "V_bary")
    Rf = Rc.max(); Vf = float(Vb[-1])
    Mf = (Vf * 1e3) ** 2 * (Rf * KPC) / G / MSUN
    # peak of V_bary^2 R/G at R > R_e
    Vt = np.interp(np.linspace(0.2, Rc.max(), 400), Rc, Vb); Rg = np.linspace(0.2, Rc.max(), 400)
    Mpk = float(np.max((Vt * 1e3) ** 2 * (Rg * KPC) / G / MSUN))
    ratios_out.append(Mv / Mfit); ratios_far.append(Mf / Mfit)
    b5[i] = dict(M_vec_outer_over_Mtot=Mv / Mfit, M_vec_Rmax_over_Mtot=Mf / Mfit, Rmax=Rf, M_vec_peak_over_Mtot=Mpk / Mfit)
    print(f"  {i:5s}: V_bary^2 R/G at the outermost marker / 10^logMtot = {Mv / Mfit:5.2f}; at the curve end (R = {Rf:5.1f} kpc) {Mf / Mfit:5.2f}; peak over R {Mpk / Mfit:5.2f}")
ro = np.array(ratios_out); rfar = np.array(ratios_far)
sel = np.array([i in ID12 for i in ID14])
print(f"median ratio at the outermost marker: 14 {np.median(ro):.2f}, 12 {np.median(ro[sel]):.2f}; at the curve end: 14 {np.median(rfar):.2f}, 12 {np.median(rfar[sel]):.2f}")
med_ok = 0.4 <= np.median(ro[sel]) <= 1.3
refuted = np.median(ro[sel]) > 1.5 or np.median(ro[sel]) < 0.3
print("frozen line: reading supported if median (outermost marker) in [0.4, 1.3]:", med_ok, "| refuted if outside [0.3, 1.5]:", refuted)
R["b5"] = dict(per_id=b5, med_outer_12=float(np.median(ro[sel])), med_end_12=float(np.median(rfar[sel])), supported=bool(med_ok), refuted=bool(refuted))

print("\n== b6: NOEMA3D gas bracket (M_gas,CO x {1/2,1,2}), both readings ==")
dn = load_noema(); fn, Vrot2 = noema_frame(dn)
b6 = {}
for g in (0.5, 1.0, 2.0):
    Mi = 10 ** fn.logMstar.values + g * 10 ** fn.logMgas.values
    rn = Mi / 10 ** fn.logMbary.values
    for rt in ("recompute", "hold"):
        res = {law: stat(cell_noema(fn, Vrot2, rival=(law == "rival"), gbar_mul=rn, route=rt)[0], 234, B) for law in ("flat", "rival")}
        b6[f"{g}|{rt}"] = res
        print(f"  gas x{g} [{rt:9s}]: {line('', res)}")
R["b6"] = b6

# route bias table for the README
print("\nb-summary: the route bias implied by the bracket (median shift of delta_rival per 0.30 dex in gas) :",
      {rt: b2[f'canonical|{rt}|2.000|0.0']['rival']['med'] - b2[f'canonical|{rt}|0.500|0.0']['rival']['med'] for rt in ("recompute", "hold")})
savejson("CFG234_attack_b", R)
sys.exit(0)
