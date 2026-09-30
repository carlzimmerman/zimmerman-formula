"""CFG237 attack 4: the CRISTAL independent-route (class L) medians from the tables, an independent code path (curves + PCHIP, R_out from
Rout/Re x Re instead of the summary file), a perturbation test, LOO, route scatter. Exit 0. (The 1e-16 'equality' is scored in phase 2 from CFG227's code.)"""
import sys
from scipy.interpolate import PchipInterpolator
from CFG237_common import *

t = start("CFG237_cristal_route")
ck = Checks()
R = {}
cr = load_cristal(); det = cr.loc[DETECTED6]
vec = load_vec_outer()
cur = pd.read_csv(os.path.join(VEC, "cristal_curves.csv"), dtype={"id": str})
dyn = pd.read_csv(os.path.join(AT, "cristal2025_dynamics.csv")).set_index("id")

# ---- path A: rows as in main (summary file)
A_re = cristal_Re_rows(det); A_ro = cristal_Rout_rows(det, vec, "table_Rout")
medA = {}
for lab, rows in (("R_e", A_re), ("R_out", A_ro)):
    medA[lab] = {l: float(np.median(delta(rows["gobs"], rows["gind"], rows["z"], l, D=rows["Dind"]))) for l in LAWNAMES}
    print(f"A [{lab}]: " + "  ".join(f"{l} {medA[lab][l]:+.4f}" for l in LAWNAMES))

# ---- path B: independent code: curves (PCHIP in R) at R = (Rout/Re) x Re from the dynamics table; R_e rows from the curves at R_e too
def curve_at(i, which, Rk, kind="pchip"):
    c = cur[(cur.id == i) & (cur.curve == which)].sort_values("R_kpc").drop_duplicates("R_kpc")
    x = c.R_kpc.values; y = c.value.values
    if kind == "pchip": return float(PchipInterpolator(x, y, extrapolate=True)(Rk))
    return float(np.interp(Rk, x, y))

def rows_B(radius, kind):
    g_obs = []; g_bar_fit = []; gi = []; Di = []; zs = []; Rs = []
    for i in DETECTED6:
        Re = float(dyn.loc[i, "Rout_over_Re"]) * float(dyn.loc[i, "Re_disk_kpc"]) if radius == "Rout" else float(dyn.loc[i, "Re_disk_kpc"])
        Vt = curve_at(i, "V_tot", Re, kind); Vb = curve_at(i, "V_bary", Re, kind)
        go = gacc(Vt, Re); gf = gacc(Vb, Re)
        Mst = 10 ** cr.loc[i, "logMstar"]; f = cr.loc[i, "f_molgas"]
        rho = (Mst / (1 - f)) / 10 ** cr.loc[i, "logMtot"]
        g_obs.append(go); g_bar_fit.append(gf); gi.append(gf * rho); Di.append(go / (gf * rho)); zs.append(cr.loc[i, "z"]); Rs.append(Re)
    return dict(gobs=np.array(g_obs), gind=np.array(gi), Dind=np.array(Di), z=np.array(zs), R=np.array(Rs))

print("\nB [independent path: curves + interpolation; R_out = Rout/Re x Re]")
medB = {}
for radius in ("Re", "Rout"):
    for kind in ("pchip", "linear"):
        rb = rows_B(radius, kind)
        m = {l: float(np.median(delta(rb["gobs"], rb["gind"], rb["z"], l, D=rb["Dind"]))) for l in LAWNAMES}
        medB[(radius, kind)] = m
        ref = medA["R_e" if radius == "Re" else "R_out"]
        print(f"   {radius:4s} {kind:6s}: " + "  ".join(f"{l} {m[l]:+.4f} ({m[l] - ref[l]:+.1e})" for l in LAWNAMES))
R["A"] = medA; R["B"] = {f"{k[0]}_{k[1]}": v for k, v in medB.items()}
ref_Rout = A_ro["R"]; rb = rows_B("Rout", "pchip")
print("   R_out per disc: summary file", np.round(ref_Rout, 3), "| Rout/Re x Re", np.round(rb["R"], 3))
dmax_re = max(abs(medB[("Re", k)][l] - medA["R_e"][l]) for k in ("pchip", "linear") for l in LAWNAMES)
dmax_ro = max(abs(medB[("Rout", k)][l] - medA["R_out"][l]) for k in ("pchip", "linear") for l in LAWNAMES)
print(f"   max |independent-path median - path A median|: R_e {dmax_re:.2e}; R_out {dmax_ro:.2e}")
ck.add("independent code path reproduces the R_e medians to 1e-3 (curves vs table values at R_e)", dmax_re < 1e-3, f"{dmax_re:.2e}")
ck.add("independent code path reproduces the R_out medians to 0.01 (frozen median line)", dmax_ro < 0.01, f"{dmax_ro:.2e}")
R["indep_path_max_diff"] = dict(Re=dmax_re, Rout=dmax_ro)

# ---- perturbation test: f_molgas +0.05 on one disc at a time
print("\nperturbation: f_molgas +0.05 on one disc (R_e, FLAT median)")
base = medA["R_e"]["FLAT"]
for i in DETECTED6:
    d2 = det.copy(); d2.loc[i, "f_molgas"] = d2.loc[i, "f_molgas"] + 0.05
    rows = cristal_Re_rows(d2)
    m = float(np.median(delta(rows["gobs"], rows["gind"], rows["z"], "FLAT", D=rows["Dind"])))
    print(f"   {i}: median FLAT {m:+.4f} (shift {m - base:+.4f})")

# ---- LOO and the six
print("\nleave-one-out, FLAT and Hz medians (R_e / R_out)")
loo = {}
for lab, rows in (("R_e", A_re), ("R_out", A_ro)):
    dF = delta(rows["gobs"], rows["gind"], rows["z"], "FLAT", D=rows["Dind"]); dH = delta(rows["gobs"], rows["gind"], rows["z"], "Hz", D=rows["Dind"])
    print(f"   {lab}: per-disc FLAT {np.round(dF, 3)}  Hz {np.round(dH, 3)}")
    for j, i in enumerate(DETECTED6):
        keep = [k for k in range(6) if k != j]
        print(f"      drop {i}: FLAT {np.median(dF[keep]):+.3f} Hz {np.median(dH[keep]):+.3f}")
    loo[lab] = dict(dF=dF, dH=dH)
R["loo"] = loo

# ---- route facts
print("\nroute facts: rho = M_ind/M_fit:", dict(zip(DETECTED6, np.round(A_re['rho'], 2))), "; discs with D_ind < 1 (R_e):", [i for i, x in zip(DETECTED6, A_re["Dind"]) if x < 1], "; R_out:", [i for i, x in zip(DETECTED6, A_ro["Dind"]) if x < 1])
print("z of the six:", dict(zip(DETECTED6, np.round(A_re["z"], 3))), "; above z=5:", [i for i, z in zip(DETECTED6, A_re["z"]) if z > 5])
print("what is independent: M*, f_molgas (normalisation of g_bar). What is NOT: V_tot (model V), V_bary curve shape and R_e (DysmalPy fit), sigma_0, the pressure correction.")
# the route uses the fit's V_bary curve shape: how much of g_bar,ind is the fit?  Re-normalise: g_bar,ind/g_bar,fit = rho (0.34-1.22)
print(f"   rho spread: min {A_re['rho'].min():.2f}, max {A_re['rho'].max():.2f}; log10 sd {np.std(np.log10(A_re['rho'])):.3f} dex")
ck.add("C1 six class-A discs", len(DETECTED6) == 6)
savejson("CFG237_cristal_route", R)
print(f"\nSUMMARY: {len(ck.rows)} lines, {ck.n_fail()} FAIL")
sys.exit(0)
