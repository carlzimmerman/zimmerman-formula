"""CFG237 main: S1 (Amvrosiadis), CRISTAL class L / D, RC100 z>=2, ALPAKA stars-only, band shifts, sensitivities, controls.
MUTATE modes handled here: 2 (alpha_CO x2 on S1), 3 (common-mode +0.30 dex on all S and L gas), 5 (band applied to the stars instead of gas),
7 (R_e x1.5 on S1), 8 (g_obs x1.5 on every point). Exit 0 (main) / 1 when a designated line FAILS in a MUTATE run."""
import sys
from CFG237_common import *

t = start("CFG237_main")
ck = Checks()
R = {}
mut = MODE

# ------------------------------------------------------------------ controls that do not depend on the data
print("\n== C3 Freeman disc ==")
yy = np.linspace(0.2, 3, 4000); Rd = 1.0
f = yy ** 2 * (special.i0(yy) * special.k0(yy) - special.i1(yy) * special.k1(yy))
Mtest = 1e11; Rd_test = 3.0
v2 = disc_v2(yy * 2 * Rd_test, Mtest, Rd_test)
peak = v2.max() / (G * Mtest * MSUN / (Rd_test * KPC))
ck.add("C3 Freeman peak V^2 = 0.3872 GM/R_d to 0.003", abs(peak - 0.3872) < 0.003, f"peak={peak:.5f} at y={yy[np.argmax(f)]:.3f}")
for mult in (50, 500):
    g = disc_g(mult * Rd_test, Mtest, Rd_test); gk = G * Mtest * MSUN / (mult * Rd_test * KPC) ** 2
    print(f"   far field r={mult} R_d: g/(GM/r^2) = {g / gk:.6f}")
g50 = disc_g(50 * Rd_test, Mtest, Rd_test) / (G * Mtest * MSUN / (50 * Rd_test * KPC) ** 2) - 1
g500 = disc_g(500 * Rd_test, Mtest, Rd_test) / (G * Mtest * MSUN / (500 * Rd_test * KPC) ** 2) - 1
ck.add("C3 far field 500 R_d to 1e-4", abs(g500) < 1e-4, f"{g500:.3e}")
ck.add("C3 far field 50 R_d to 1e-3 (the frozen-in-CFG227 clause; expected FAIL, kept)", abs(g50) < 1e-3, f"{g50:.3e}", expected_fail=True)
R["C3"] = dict(peak=peak, far50=g50, far500=g500)

print("\n== C4p laws ==")
zz = np.array([1, 2, 2.5, 4.5, 5.5])
Fp = F_proxy(zz)
print("   proxy F:", np.round(Fp, 3), "target 1.23 1.77 2.16 4.52 6.20")
ck.add("C4p proxy F(z) within 1% of CFG222 README values", np.all(np.abs(Fp / np.array([1.23, 1.77, 2.16, 4.52, 6.20]) - 1) < 0.01))
Fm = F_mdec(np.array([1, 2, 3.0]))
print("   M-DEC:", np.round(Fm, 4), "target 0.9889 0.8739 0.7750")
ck.add("C4p M-DEC within 0.002 of CFG223 README values", np.all(np.abs(Fm - np.array([0.9889, 0.8739, 0.7750])) < 0.002))
R["laws"] = dict(proxy=Fp, mdec=Fm, E=E_of_z(zz))

try:                      # labelled shared: import of the repo kernel
    sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
    import CFG4_common as C4  # noqa
    y = np.logspace(-6, 4, 2001)
    dif = float(np.max(np.abs(C4.nu_mono(y) / nu_mono(y) - 1)))
    a0m = abs(float(C4.A0["canonical"]) - A0["canonical"]) < 1e-15
    print(f"   [shared] max rel diff nu_mono vs CFG4_common = {dif:.2e}; a0 match {a0m}")
    ck.add("C5k nu_mono equals CFG4_common (shared object, labelled)", dif < 1e-7 and a0m, f"{dif:.2e}")
except Exception as e:
    print("   CFG4_common import failed:", repr(e)[:120])

# ------------------------------------------------------------------ S1
print("\n== S1 Amvrosiadis (class S), nine sources 2<=z<=5 ==")
d = load_s1()
print("ids:", list(d.alessid), "| z:", np.round(d.z.values, 3))
kw = dict()
if mut == "2": kw["alpha"] = 1.84
if mut == "3": kw["bias_gas"] = 0.30
if mut == "5": kw["bias_star"] = 0.30       # the 'band' applied to the stars
if mut == "7": kw["s"] = 1.5
if mut == "8": kw["gobs_mul"] = 1.5
ck.add("C1 S1 N = 9 and ids", list(d.alessid) == S1_IDS)
P = s1_points(d, **kw)
print("   r_e (kpc):", np.round(P["re"], 2))
print("   g_obs/a0:", np.round(P["gobs"] / A0["canonical"], 2))
print("   g_bar/a0:", np.round(P["gbar"] / A0["canonical"], 2))
print("   D       :", np.round(P["D"], 3))
print("   gas share of g_bar:", np.round(P["g_gas"] / P["gbar"], 2))
S1 = {}
for law in LAWNAMES:
    dl = delta(P["gobs"], P["gbar"], P["z"], law)
    S1[law] = dict(stat=boot(dl, SEED), stat2=boot(dl, SEED2), dl=dl)
    print(f"   delta_{law:5s}: {fs(S1[law]['stat'])}   (seed 238: [{S1[law]['stat2']['lo']:+.3f}, {S1[law]['stat2']['hi']:+.3f}])")
Dmed = float(np.median(P["D"])); nD = int(np.sum(P["D"] < 1))
print(f"   median D = {Dmed:.3f}; n(D<1) = {nD} of 9")
print("   per-galaxy delta_FLAT:", np.round(S1["FLAT"]["dl"], 3))
R["S1"] = dict(D_med=Dmed, n_Dlt1=nD, **{l: dict(S1[l]["stat"]) for l in LAWNAMES}, D=P["D"], dl_flat=S1["FLAT"]["dl"], dl_hz=S1["Hz"]["dl"])
for foot in ("alt",):
    for kern in ("mono", "p2"):
        for law in ("FLAT", "Hz"):
            dl = delta(P["gobs"], P["gbar"], P["z"], law, foot=foot, kern=kern)
            print(f"   [{foot},{kern}] delta_{law}: {fs(boot(dl))}")
for kern in ("p2",):
    for law in ("FLAT", "Hz"):
        dl = delta(P["gobs"], P["gbar"], P["z"], law, kern=kern)
        print(f"   [canonical,{kern}] delta_{law}: {fs(boot(dl))}")

# targets (README, read in phase 1) -- medians within 0.01 dex
def tgt(name, val, target, tol=0.01):
    ok = abs(val - target) <= tol
    ck.add(f"S1 target {name}", ok, f"mine {val:+.4f} vs CFG227 README {target:+.3f} (diff {val - target:+.4f})")
    return ok

if mut in ("", "2", "3", "5", "7", "8"):
    tgt("delta_FLAT median", S1["FLAT"]["stat"]["med"], -0.310)
    tgt("delta_PROXY median", S1["PROXY"]["stat"]["med"], -0.338)
    tgt("delta_Hz median", S1["Hz"]["stat"]["med"], -0.373)
    tgt("delta_MDEC median", S1["MDEC"]["stat"]["med"], -0.306)
    tgt("median D", Dmed, 0.52, 0.01)
    ck.add("S1 n(D<1) = 7 of 9", nD == 7, f"mine {nD}")
    print("   FLAT CI edges vs README [-0.664, +0.171]: mine", fs(S1["FLAT"]["stat"]), "| adjacent order stats? lo:",
          edge_adjacent(S1["FLAT"]["dl"], S1["FLAT"]["stat"]["lo"], -0.664), " hi:", edge_adjacent(S1["FLAT"]["dl"], S1["FLAT"]["stat"]["hi"], 0.171))

if mut == "2":
    P0 = s1_points(d)
    Dpred = P0["D"] / (1 + P0["g_gas"] / P0["gbar"])
    ck.add("M2 bite-check: algebra D' = D/(1 + gas share) equals the mutated D to 1e-9 (should PASS: the mutation is applied, not hidden)", np.max(np.abs(Dpred / P["D"] - 1)) < 1e-9)
if mut == "7":
    P0 = s1_points(d)
    ck.add("M7 bite-check: D scales exactly x1.5 (algebra: D proportional to R_e at fixed V, M) (should PASS)", np.max(np.abs(P["D"] / P0["D"] - 1.5)) < 1e-9)

# sensitivities
print("\n-- S1 sensitivities (beside, never substituted) --")
Pp = s1_points(d, k=K0)
for law in ("FLAT", "Hz"):
    print(f"   V_c^2 = V^2 + 3.36 sigma^2: delta_{law} {fs(boot(delta(Pp['gobs'], Pp['gbar'], Pp['z'], law)))}  median D {np.median(Pp['D']):.3f}")
R["S1_press"] = dict(FLAT=boot(delta(Pp["gobs"], Pp["gbar"], Pp["z"], "FLAT")), Hz=boot(delta(Pp["gobs"], Pp["gbar"], Pp["z"], "Hz")), D=float(np.median(Pp["D"])))
P2r = s1_points(d, mstar_mult=2)
for law in ("FLAT", "Hz"):
    print(f"   stars at R_e,* = 2 R_e,CO: delta_{law} {fs(boot(delta(P2r['gobs'], P2r['gbar'], P2r['z'], law)))}  median D {np.median(P2r['D']):.3f}")
R["S1_star2"] = dict(FLAT=boot(delta(P2r["gobs"], P2r["gbar"], P2r["z"], "FLAT")), D=float(np.median(P2r["D"])))
if mut in ("", "2", "3", "5", "7", "8"):
    tgt("pressure variant delta_FLAT", R["S1_press"]["FLAT"]["med"], -0.241)
    tgt("pressure variant delta_Hz", R["S1_press"]["Hz"]["med"], -0.295)
    tgt("stars at 2 R_e delta_FLAT", R["S1_star2"]["FLAT"]["med"], -0.216)
    tgt("stars at 2 R_e median D", R["S1_star2"]["D"], 0.62)

print("\n-- S1 gas-shift (band) medians, all four laws --")
bandS = {}
for tau in (-0.671, -0.213, 0.0, 0.213, 0.671):
    kwt = dict(kw); kwt["tau"] = tau
    Pt = s1_points(d, **kwt)
    row = {l: float(np.median(delta(Pt["gobs"], Pt["gbar"], Pt["z"], l))) for l in LAWNAMES}
    bandS[tau] = row
    print(f"   tau {tau:+.3f}: " + "  ".join(f"{l} {row[l]:+.3f}" for l in LAWNAMES) + f"  median D {np.median(Pt['D']):.3f}")
R["S1_band"] = bandS
if mut in ("", "2", "3", "5", "7", "8"):
    tgt("outer band flat median at +0.671 (README: -0.70)", bandS[0.671]["FLAT"], -0.70, 0.02)
    tgt("outer band flat median at -0.671 (README: -0.24)", bandS[-0.671]["FLAT"], -0.24, 0.02)

# C2 placement, C4 direction
print("\n-- controls on S1 --")
Pc = s1_points(d)
ok2 = True; ok2b = True
for law in LAWNAMES:
    gobs_syn = Pc["gbar"] * nu_mono(Pc["gbar"] / (A0["canonical"] * LAWS[law](Pc["z"])))
    for l2 in LAWNAMES:
        dl = delta(gobs_syn, Pc["gbar"], Pc["z"], l2)
        if l2 == law: ok2 &= bool(np.max(np.abs(dl)) < 1e-9)
        elif law in ("FLAT", "Hz") and l2 in ("FLAT", "Hz"): ok2b &= bool(np.min(np.abs(dl)) > 1e-3)
ck.add("C2 placement: delta = 0 to 1e-9 under the true law; FLAT/Hz differ under the other", ok2 and ok2b)
okdir = True
for tau in (0.05, 0.3):
    Pt = s1_points(d, tau=tau)
    okdir &= bool(np.all(delta(Pt["gobs"], Pt["gbar"], Pt["z"], "FLAT") < delta(Pc["gobs"], Pc["gbar"], Pc["z"], "FLAT")))
ck.add("C4 band direction: tau>0 lowers delta at every S1 point", okdir)
P8 = s1_points(d, gobs_mul=1.5)
sh = delta(P8["gobs"], P8["gbar"], P8["z"], "FLAT") - delta(Pc["gobs"], Pc["gbar"], Pc["z"], "FLAT")
ck.add("M8-style shift: g_obs x1.5 shifts every delta by +0.17609 to 1e-9", np.max(np.abs(sh - math.log10(1.5))) < 1e-9)

# M8-style shift on the other point sets (frozen M8: every point in my code)
_rc = rc100_rows(load_rc100("corrected")); _al = alpaka_points(load_alpaka()); _mk = np.isfinite(_al["gbar"])
_cr = cristal_Re_rows(load_cristal().loc[DETECTED6])
_ok = True
for go, gb, zz, D_ in ((_rc["gobs"], _rc["gbar"], _rc["z"], None), (_al["gobs"][_mk], _al["gbar"][_mk], _al["z"][_mk], None), (_cr["gobs"], _cr["gind"], _cr["z"], _cr["Dind"])):
    a_ = delta(go, gb, zz, "FLAT", D=D_); b_ = delta(go * 1.5, gb, zz, "FLAT", D=None if D_ is None else D_ * 1.5)
    _ok &= bool(np.max(np.abs((b_ - a_) - math.log10(1.5))) < 1e-9)
ck.add("M8-style shift on RC100, ALPAKA and CRISTAL L rows: g_obs x1.5 shifts every delta by +0.17609 to 1e-9", _ok)

# ------------------------------------------------------------------ CRISTAL
print("\n== CRISTAL class L (independent route, six dust-detected discs) and class D (fit route) ==")
cr = load_cristal()
det = cr.loc[DETECTED6]
cm = {}
for lab, rows_fn in (("R_e", lambda tau: cristal_Re_rows(det, tau=tau)),
                     ("R_out", lambda tau: cristal_Rout_rows(det, load_vec_outer(), "table_Rout", tau=tau))):
    row = rows_fn(0.0)
    cm[lab] = {}
    for law in LAWNAMES:
        dl = delta(row["gobs"], row["gind"], row["z"], law, D=row["Dind"])
        cm[lab][law] = boot(dl, SEED)
        print(f"   L {lab:5s} {law:5s}: {fs(cm[lab][law])}")
    print(f"   L {lab}: rho =", np.round(row["rho"], 2), " D_ind =", np.round(row["Dind"], 2), "ids", list(row["ids"]))
    sb = {}
    for tau in (-0.671, -0.213, 0.213, 0.671):
        rt = rows_fn(tau)
        sb[tau] = {l: float(np.median(delta(rt["gobs"], rt["gind"], rt["z"], l, D=rt["Dind"]))) for l in LAWNAMES}
        print(f"      tau {tau:+.3f}: " + "  ".join(f"{l} {sb[tau][l]:+.3f}" for l in LAWNAMES))
    cm[lab]["band"] = sb
R["CRISTAL_L"] = cm
for lab, (f_t, p_t, h_t) in {"R_e": (0.117, -0.085, -0.144), "R_out": (0.106, -0.136, -0.203)}.items():
    tgt(f"CRISTAL L {lab} flat", cm[lab]["FLAT"]["med"], f_t); tgt(f"CRISTAL L {lab} proxy", cm[lab]["PROXY"]["med"], p_t); tgt(f"CRISTAL L {lab} Hz", cm[lab]["Hz"]["med"], h_t)
tgt("CRISTAL L R_e band +0.671 flat (README +0.26 .. -0.20: lower end -0.20)", cm["R_e"]["band"][0.671]["FLAT"], -0.20, 0.02)
tgt("CRISTAL L R_e band -0.671 flat (+0.26)", cm["R_e"]["band"][-0.671]["FLAT"], 0.26, 0.02)
tgt("CRISTAL L R_out band +0.671 flat (-0.16)", cm["R_out"]["band"][0.671]["FLAT"], -0.16, 0.02)
tgt("CRISTAL L R_out band -0.671 flat (+0.24)", cm["R_out"]["band"][-0.671]["FLAT"], 0.24, 0.02)

print("   -- class D: fit route (rho = 1), R_e twelve discs (09, 15 excluded) and R_out six discs --")
r12 = cristal_Re_rows(cr.loc[ID12])
Dfit = {}
for law in ("FLAT", "PROXY", "Hz"):
    Dfit[law] = boot(delta(r12["gobs"], r12["gfit"], r12["z"], law, D=r12["Dfit"]))
    print(f"   D R_e (12) {law}: {fs(Dfit[law])}")
r6 = cristal_Rout_rows(det, load_vec_outer(), "table_Rout")
for law in ("FLAT", "PROXY", "Hz"):
    print(f"   D R_out (same six, fit) {law}: {fs(boot(delta(r6['gobs'], r6['gfit'], r6['z'], law, D=r6['Dfit'])))}")
R["CRISTAL_D_Re12"] = Dfit
ck.add("C1 CRISTAL: 14 modelled, 12 fit-route R_e rows, 6 class-A", len(cr) == 14 and len(r12["ids"]) == 12 and len(det) == 6)

# ------------------------------------------------------------------ RC100
print("\n== RC100 z>=2 (class D, flagged) ==")
for which in ("corrected", "committed"):
    rc = load_rc100(which)
    rr = rc100_rows(rc)
    n = len(rr["z"])
    print(f"   [{which}] N(z>=2) = {n}")
    st = {law: boot(delta(rr["gobs"], rr["gbar"], rr["z"], law)) for law in ("FLAT", "PROXY", "Hz")}
    for law in st: print(f"     {law}: {fs(st[law])}")
    R["RC100_" + which] = st
    if which == "corrected":
        ck.add("C1 RC100 corrected z>=2 N = 41", n == 41, f"{n}")
        tgt("RC100 z>=2 flat", st["FLAT"]["med"], 0.008); tgt("RC100 z>=2 Hz", st["Hz"]["med"], -0.105)
rcc = load_rc100("committed"); rcr = load_rc100("corrected")
zz2 = rcr[rcr.z >= 2].idx.values
diffc = rcr[rcr.changed_cells.notna() & (rcr.changed_cells.astype(str) != "")]
print("   corrected-table changed rows among z>=2:", sorted(set(diffc.idx.values) & set(zz2)))

# ------------------------------------------------------------------ ALPAKA
print("\n== ALPAKA ten discs (stars-only; g_bar lower limit; delta upper bound) ==")
al = load_alpaka()
print("   ids:", list(al.id), " with M*:", int(al.mstar_1e10msun.notna().sum()))
ck.add("C1 ALPAKA ten discs, nine with M*", len(al) == 10 and int(al.mstar_1e10msun.notna().sum()) == 9)
both = pd.read_csv(os.path.join(AT, "alpaka1_digitised", "alpaka1_outer_summary.csv")).R_ext_over_Re.dropna()
print(f"   median R_ext/R_e of the galaxies with both (all z): {np.median(both):.3f} (n={len(both)}); frozen uses 1.2")
for a in (0.0, 1.68, 3.36):
    Pa = alpaka_points(al, alpha_p=a)
    m = np.isfinite(Pa["gbar"])
    dl = delta(Pa["gobs"][m], Pa["gbar"][m], Pa["z"][m], "FLAT")
    print(f"   alpha={a}: delta_FLAT upper bound median {np.median(dl):+.3f}, range {dl.min():+.3f} to {dl.max():+.3f}; n={m.sum()}")
    if a == 0.0:
        R["ALPAKA"] = dict(med=float(np.median(dl)), lo=float(dl.min()), hi=float(dl.max()), dl=dl, ids=Pa["ids"][m])
        print("     per-disc:", dict(zip(Pa["ids"][m].tolist(), np.round(dl, 2).tolist())))
tgt("ALPAKA median delta_FLAT upper bound", R["ALPAKA"]["med"], -0.08)
print(f"   range vs README (-0.59 to +0.22): mine {R['ALPAKA']['lo']:+.3f} to {R['ALPAKA']['hi']:+.3f}")

# ------------------------------------------------------------------ C5 bootstrap coverage of my estimator
print("\n== C5 bootstrap coverage of the 95% CI on flat-truth mocks (sigma = 0.15) ==")
rng = np.random.default_rng(SEED)
for n in (6, 9, 41):
    hit = 0; N = 600
    for _ in range(N):
        x = rng.normal(0, 0.15, n)
        s = boot(x, int(rng.integers(1, 10 ** 9)), 400)
        hit += (s["lo"] <= 0 <= s["hi"])
    print(f"   n={n}: coverage {hit / N:.3f}")
    ck.add(f"C5 coverage n={n} in [0.88, 0.98]", 0.88 <= hit / N <= 0.98, f"{hit / N:.3f}")

savejson("CFG237_main", R)
nf = ck.n_fail()
print(f"\nSUMMARY: {len(ck.rows)} lines, {nf} FAIL")
for r_ in ck.rows:
    if not r_[1]: print("   FAILED" + (" (expected, kept)" if r_[3] else "") + ":", r_[0], "::", r_[2])
if mut:
    print("MUTATE", mut, "bites" if nf > 0 else "DOES NOT BITE")
    sys.exit(1 if nf > 0 else 0)
sys.exit(0)
