"""CFG237 misc attacks: gas bracket crossings, S1 leave-one-out, ALPAKA variants, kernels/footings, CRISTAL pressure variants, lean labels. Exit 0."""
import sys
from CFG237_common import *

t = start("CFG237_attacks_misc")
ck = Checks()
R = {}
d = load_s1(); P0 = s1_points(d)
cr = load_cristal(); det = cr.loc[DETECTED6]; vec = load_vec_outer()

def label(s):
    return "excludes 0 (above)" if s["lo"] > 0 else ("excludes 0 (below)" if s["hi"] < 0 else "contains 0 -> not a detection")

print("== (a) gas-bracket: sign of each law's median across the band ==")
def s1_med(tau, law):
    Pt = s1_points(d, tau=tau); return float(np.median(delta(Pt["gobs"], Pt["gbar"], Pt["z"], law)))
def crs_med(lab, tau, law):
    rows = cristal_Re_rows(det, tau=tau) if lab == "R_e" else cristal_Rout_rows(det, vec, "table_Rout", tau=tau)
    return float(np.median(delta(rows["gobs"], rows["gind"], rows["z"], law, D=rows["Dind"])))
grid = np.linspace(-0.671, 0.671, 135)
cross = {}
for name, fn in (("S1", s1_med), ("CRISTAL R_e", lambda t_, l: crs_med("R_e", t_, l)), ("CRISTAL R_out", lambda t_, l: crs_med("R_out", t_, l))):
    row = {}
    for law in LAWNAMES:
        v = np.array([fn(tt, law) for tt in grid])
        row[law] = bool(v.min() < 0 < v.max())
    cross[name] = row
    print(f"   {name}: median crosses 0 inside +-0.671 for: " + ", ".join(f"{l} {row[l]}" for l in LAWNAMES))
R["crossings"] = cross
ck.add("CFG227 claim: for CRISTAL class L every law's median crosses zero inside the outer band (R_e and R_out, four laws)", all(cross["CRISTAL R_e"].values()) and all(cross["CRISTAL R_out"].values()), str(cross))
print("   inner band +-0.213 (CRISTAL R_e):", {l: (round(crs_med('R_e', -0.213, l), 3), round(crs_med('R_e', 0.213, l), 3)) for l in LAWNAMES})

print("\n== (c) S1 leave-one-out (FLAT, Hz medians) ==")
dF = delta(P0["gobs"], P0["gbar"], P0["z"], "FLAT"); dH = delta(P0["gobs"], P0["gbar"], P0["z"], "Hz")
base = np.median(dF)
for j, i in enumerate(d.alessid):
    keep = [k for k in range(9) if k != j]
    mF = float(np.median(dF[keep])); mH = float(np.median(dH[keep]))
    print(f"   drop {i}: FLAT {mF:+.3f} ({mF - base:+.3f}), Hz {mH:+.3f}")
loo = [float(np.median(dF[[k for k in range(9) if k != j]]) - base) for j in range(9)]
print(f"   max |shift| {max(abs(x) for x in loo):.3f}")
R["S1_loo"] = loo
print("   sign of the S1 median under LOO: all negative" if all(np.median(dF[[k for k in range(9) if k != j]]) < 0 for j in range(9)) else "   sign changes under LOO")

print("\n== (d) ALPAKA variants ==")
al = load_alpaka()
for ratio in (1.0, 1.2, 1.23, 1.5, 2.0):
    Pa = alpaka_points(al, rext_over_re=ratio); m = np.isfinite(Pa["gbar"])
    dl = delta(Pa["gobs"][m], Pa["gbar"][m], Pa["z"][m], "FLAT")
    print(f"   R_ext/R_e = {ratio}: median upper bound {np.median(dl):+.3f}, range {dl.min():+.3f} to {dl.max():+.3f}")
Pa = alpaka_points(al); m = np.isfinite(Pa["gbar"])
dl = delta(Pa["gobs"][m], Pa["gbar"][m], Pa["z"][m], "FLAT")
print("   bound direction: a gas mass can only RAISE g_bar and LOWER delta; so the stars-only delta is an upper bound; discs whose bound is already below 0:", int(np.sum(dl < 0)), "of", int(m.sum()))
R["alpaka_neg"] = int(np.sum(dl < 0))

print("\n== (f) kernels and footings (medians; CI labels) ==")
rc = rc100_rows(load_rc100("corrected"))
sets = {"S1": (P0["gobs"], P0["gbar"], P0["z"], None), "RC100 z>=2": (rc["gobs"], rc["gbar"], rc["z"], None)}
rR = cristal_Re_rows(det); rO = cristal_Rout_rows(det, vec, "table_Rout")
sets["CRISTAL L R_e"] = (rR["gobs"], rR["gind"], rR["z"], rR["Dind"]); sets["CRISTAL L R_out"] = (rO["gobs"], rO["gind"], rO["z"], rO["Dind"])
for nm, (go, gb, zz, D) in sets.items():
    for foot in ("canonical", "alt"):
        for kern in ("mono", "p2"):
            out = []
            for law in ("FLAT", "Hz"):
                s = boot(delta(go, gb, zz, law, foot=foot, kern=kern, D=D))
                out.append(f"{law} {s['med']:+.3f} [{s['lo']:+.3f},{s['hi']:+.3f}]")
            print(f"   {nm:16s} {foot:9s} {kern:5s}: " + " | ".join(out))

print("\n== CRISTAL R_e pressure variants k = 3.36 / 1.68 / 0 (class L, D_ind = g_obs/g_bar,ind with g_bar,ind held at the k=3.36 value, as CFG213's H-g) ==")
base_rows = cristal_Re_rows(det, k=K0)
for k_ in (K0, 1.68, 0.0):
    rows = cristal_Re_rows(det, k=k_)
    gobs_k = rows["gobs"]; gind_fixed = base_rows["gind"]
    Dk = gobs_k / gind_fixed
    print(f"   k={k_}: FLAT {np.median(delta(gobs_k, gind_fixed, rows['z'], 'FLAT', D=Dk)):+.3f}  Hz {np.median(delta(gobs_k, gind_fixed, rows['z'], 'Hz', D=Dk)):+.3f}")

print("\n== (g) lean-is-not-a-detection labels (canonical, nu_mono, 10,000 bootstrap, seed 237) ==")
for nm, (go, gb, zz, D) in sets.items():
    for law in ("FLAT", "Hz"):
        s = boot(delta(go, gb, zz, law, D=D))
        print(f"   {nm:16s} {law:5s}: {fs(s)} -> {label(s)}" + ("   [class D: flagged, never scored]" if nm.startswith("RC100") else ""))
savejson("CFG237_attacks_misc", R)
print(f"\nSUMMARY: {len(ck.rows)} lines, {ck.n_fail()} FAIL")
for r_ in ck.rows:
    if not r_[1]: print("   FAILED:", r_[0], "::", r_[2])
sys.exit(0)
