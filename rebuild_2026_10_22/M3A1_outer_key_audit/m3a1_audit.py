#!/usr/bin/env python3
"""M3A1 audit (FROZEN_CRITERIA.md): reads the jobs' dumps, X7's per-cluster npz, the extended randoms; computes reach per candidate, stability, joint chi^2, Z_tot, and the label.
    python3 m3a1_audit.py [--mutate]
kappa = 1/2 FITTED; not theory closed."""
import io, json, os, sys, tarfile
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
import numpy as np, warnings; warnings.simplefilter("ignore")
from scipy.interpolate import PchipInterpolator
from scipy.stats import chi2
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB); CJ = os.path.join(HERE, "cache_jobs"); MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
OUT = []; RES = {}; CHK = []
def P(s=""): print(s, flush=True); OUT.append(s)
def check(n, ok, t): CHK.append((n, bool(ok))); P(f"{n} {'PASS' if ok else 'FAIL'}: {t}")
HH = ("h0672", "h0686"); FS = ("0.034", "0.0615"); CELLS = [(f, h) for f in FS for h in HH]; OB = [6, 7]; MB = [3, 4, 5]; IB = [0, 1, 2]
def jb(n, f): return json.load(open(os.path.join(CJ, f"{n}_{f}.json")))
def dp(n, f): return np.load(os.path.join(CJ, f"{n}_{f}_dump.npz"))
X = np.load(os.path.join(RB, "X7_cluster_core_significance", "x7_measure_percluster.npz")); N = len(X["name"]); HI = {"h0672": 1, "h0686": 2}; HX = {"h0672": 0, "h0686": 1}
Mg = np.asarray(X["Mgas500"], float); T3 = np.digitize(Mg, np.quantile(Mg, [1 / 3, 2 / 3])); M3 = np.where(T3 == 2)[0]; ALLI = np.arange(N); zc = np.asarray(X["z"], float); ra = np.asarray(X["ra"], float)
ZN4 = json.load(open(os.path.join(RB, "ZN4_cluster_resolution", "zn4_results.json")))["runs"]
DEV = os.environ.get("M3A1_DEV"); RR = np.load(os.path.join(HERE, "cache_randoms", "arrays.npz") if DEV else os.path.join(HERE, "m3a1_randoms.npz")); P("M3A1 audit, ZN4's chain, gas +0.005; kappa = 1/2 FITTED; not theory closed")
def wb(h, B=None):
    i = HI[h]; W = np.where(X["E"][:, i] < 1e8, 1 / X["E"][:, i] ** 2, 0); B0 = X["den"][:, i].sum(0) / X["den_r"][:, i].sum(0); return W * (B0 if B is None else B)[None, :], W, B0
def nsum(h, D=None, B=None, leak=None):
    i = HI[h]; WB, _, _ = wb(h, B); D = X["D"][:, i] if D is None else D; L = X["leakP"][:, HX[h], 0] if leak is None else leak; return (WB * (D - L))
C = {}
for f, h in CELLS:
    d_ = dp("BASE", f); c = jb("BASE", f)["cells"][h]; C[(f, h)] = dict(V=d_[f"V_{h}"], vC=d_[f"vC_{h}"], cells=c, T3M=d_["T3M"], TID=d_["TID"], I=d_["I"], PATCH=d_["PATCH"], n=d_[f"n_{h}"], d=d_[f"d_{h}"])
# ------------- K1, K2
k1 = 0.0; k1p = 0.0
for f, h in CELLS:
    Z4 = ZN4[f"f* {f}, gas +0.005"]["cells"][h]; c = C[(f, h)]["cells"]; k1 = max(k1, max(abs(c[k]["Z"] - Z4[k]["Z"]) for k in c)); k1p = max(k1p, max(abs(c[k]["pred"] - Z4[k]["pred"]) for k in c))
check("K1", k1 <= 0.01 and k1p <= 1e-6, f"against ZN4: max |d Z| over 15 keys, 4 cells {k1:.1e}, |d pred| {k1p:.1e}; G-OUT-M3 {[round(C[x]['cells']['G-OUT-M3']['Z'], 3) for x in CELLS]}")
k2 = 0.0; k2n = 0.0; k2t = True
for f, h in CELLS:
    q = C[(f, h)]; assert np.array_equal(q["T3M"], T3) or (k2t := False); V = q["V"][:, OB].sum(1); vC = q["vC"][:, OB].sum(1); n = nsum(h)[:, OB].sum(1); k2n = max(k2n, float(np.max(np.abs(n - q["n"][:, 2])) / np.max(np.abs(q["n"][:, 2]))))
    for t in range(3):
        I_ = T3 == t; k = f"G-OUT-M{t + 1}"; c = q["cells"][k]; k2 = max(k2, abs(n[I_].sum() / vC[I_].sum() - c["meas"]), abs(V[I_].sum() / vC[I_].sum() - c["pred"]))
    c = q["cells"]["G-OUT-Mall"]; k2 = max(k2, abs(n.sum() / vC.sum() - c["meas"]), abs(V.sum() / vC.sum() - c["pred"]))
check("K2", k2 <= 1e-6 and k2n <= 1e-9 and k2t, f"own sums reproduce meas, pred on M1-M3, Mall: {k2:.1e}; n from X7's npz {k2n:.1e}; same membership {k2t}")
def base(f, h, k="G-OUT-M3"): return C[(f, h)]["cells"][k]
def reach(z0, z1): return (z0 - z1) / (z0 - 2)
EFF = {}; ROW = []
def effect(eid, lab, Zv, cls_):
    """Zv: dict cell -> Z of the variant; class I effects enter the net."""
    dz = {x: base(*x)["Z"] - Zv[x] for x in CELLS}; rr = {x: reach(base(*x)["Z"], Zv[x]) for x in CELLS}; EFF[eid] = dict(lab=lab, cls=cls_, Z={f"{a}|{b}": v for (a, b), v in Zv.items()}, dZ={f"{a}|{b}": v for (a, b), v in dz.items()}, reach={f"{a}|{b}": v for (a, b), v in rr.items()})
    P(f"  {eid} [{cls_}] {lab}: Z " + " ".join(f"{Zv[x]:+.2f}" for x in CELLS) + f"; reach {min(rr.values()):+.2f} to {max(rr.values()):+.2f}")
def Zdata(nf, sel=M3, key="G-OUT-M3", scale_s=False):
    """shift on the data side at fixed grader s: nf(h) gives per-cluster per-bin n."""
    O = {}
    for f, h in CELLS:
        q = C[(f, h)]; vC = q["vC"][:, OB].sum(1); V = q["V"][:, OB].sum(1); A = nf(h)[sel][:, OB].sum() / vC[sel].sum(); P_ = V[sel].sum() / vC[sel].sum(); c_ = base(f, h, key); O[(f, h)] = (A - P_) / (c_["s"] * (A / c_["meas"] if scale_s else 1.0))
    return O
# ------------- what is in Z
P("\nC2b: what s holds"); X7J = json.load(open(os.path.join(RB, "X7_cluster_core_significance", "x7_analysis_results.json"))); r7 = X7J["bins"]["terciles|canonical|h0672"][2]["OUTER"]
c0 = base("0.034", "h0672"); fr = c0["s"] / c0["meas"]; P(f"  grader's s = X7's s_CAL scaled by A: fractional {fr:.4f}; X7 s_CAL {r7['s_CAL']:.4f}, s_STAT {r7['s_STAT']:.4f} (s_jk {r7['s_jk']:.4f}, s_boot {r7['s_boot']:.4f}), s_leak {r7['s_leak']:.4f}, s_x_exc {r7['s_x_exc']:.4f}, s_RR_exc {r7['s_RR_exc']:.4f}, X2's conservative s_CONS {r7['s_CONS']:.4f}. So Z is statistical only, shear side only: no gas, no slope, no seed, no m, no n(z), and no model error")
P(f"  need at f* 0.034, h 0.672: meas {c0['meas']:.3f}, pred {c0['pred']:.3f}, s {c0['s']:.3f}: pred must rise {c0['meas'] - 2 * c0['s'] - c0['pred']:+.3f} ({(c0['meas'] - 2 * c0['s']) / c0['pred'] - 1:+.1%})")
# ------------- harness effects
P("\nHarness effects (Z in cell order f* 0.034 h 0.672, h 0.686; f* 0.0615 h 0.672, h 0.686)")
for j, lab, cl in (("C1a", "Eddington shift on catalogue gas, Tweedie (M3's Z only; Mall is broken by M1's tail)", "I"), ("C2a", "pointed gas in M3's window, on M3 only", "I"), ("MC0", "miscentring x 0", "bracket"), ("MC2", "miscentring x 2", "bracket")):
    effect(j, lab, {(f, h): jb(j, f)["cells"][h]["G-OUT-M3"]["Z"] for f, h in CELLS}, cl)
    P("     other keys, f* 0.034, h 0.672: " + "; ".join(f"{k} {jb('BASE', '0.034')['cells']['h0672'][k]['Z']:+.2f}>{jb(j, '0.034')['cells']['h0672'][k]['Z']:+.2f}" for k in ("G-OUT-Mall", "G-MID-T3", "G-OUT-M2", "G-OUT-M1")) + f"; X-COP {jb(j, '0.034')['xcop']['mean']:+.3f} {jb(j, '0.034')['xcop']['rms']:.3f}")
zp = jb("C2a_plus", "0.034")["cells"]["h0672"]["G-OUT-M3"]["Z"]; zc2 = jb("C2a", "0.034")["cells"]["h0672"]["G-OUT-M3"]["Z"]; PR = json.load(open(os.path.join(HERE, "m3a1_prep.json"))); GW = PR["gs4"]["window"]; dzdd = (zp - zc2) / GW["se"]; P(f"  C2a's SE {GW['se']:.3f} dex moves Z by {zp - zc2:+.3f}: dZ/dd {dzdd:.1f} per dex on M3 alone")
mz = jb("C1a_MUTATE", "0.034")["cells"]["h0672"]["G-OUT-M3"]["Z"]; b0 = c0["Z"]; c1 = jb("C1a", "0.034")["cells"]["h0672"]["G-OUT-M3"]["Z"]; bm = (mz - b0) * (c1 - b0) < 0 and abs(mz - b0) >= 0.5 * abs(c1 - b0); check("MUTATE a", bm, f"C1a {c1 - b0:+.3f}, sign flipped {mz - b0:+.3f}: {'BITES' if bm else 'DOES NOT BITE'}")
# ------------- boost
P("\nC4a boost: B in OUTER bins, all 326 and M3's own")
for h in HH:
    _, _, B0 = wb(h); i = HI[h]; Bm = X["den"][M3, i].sum(0) / X["den_r"][M3, i].sum(0); P(f"  {h}: B all {B0[6]:.4f} {B0[7]:.4f}; M3's own {Bm[6]:.4f} {Bm[7]:.4f}")
effect("C4a1", "B = 1 in every bin", Zdata(lambda h: nsum(h, B=np.ones(8)), scale_s=True), "bracket")
def Bm3(h): i = HI[h]; return X["den"][M3, i].sum(0) / X["den_r"][M3, i].sum(0)
effect("C4a2", "M3's own B", Zdata(lambda h: nsum(h, B=Bm3(h)), scale_s=True), "I")
# ------------- randoms
P("\nC4d random subtraction"); Rt = RR["Rt"]; Rx = RR["Rx"]; Rv = RR["Rv"]; NA = RR["NA"]; P(f"  extended randoms: {int(NA.sum())}, per cluster {NA.min()}-{NA.max()}; in M3 {int(NA[M3].sum())}")
def Dext(h): i = HI[h]; return X["Draw"][:, i] - Rt[:, HX[h]]
effect("C4d", "extended randoms replace F1's", Zdata(lambda h: nsum(h, D=Dext(h))), "I")
effect("C4d0", "no random subtraction at all", Zdata(lambda h: nsum(h, D=X["Draw"][:, HI[h]])), "bracket")
for f, h in CELLS[:2]:
    q = C[(f, h)]; WB, _, _ = wb(h); i = HI[h]; dn = q["vC"][M3][:, OB].sum()
    for lab, Y in (("F1 randoms t", X["Rmean"][:, i]), ("F1 randoms x", X["Rmeanx"][:, i]), ("extended t", Rt[:, HX[h]]), ("extended x", Rx[:, HX[h]])):
        P(f"  {h} M3 OUTER level, A units, {lab}: {(WB[M3][:, OB] * Y[M3][:, OB]).sum() / dn:+.4f}; bins " + " ".join(f"{(WB[M3][:, [b]] * Y[M3][:, [b]]).sum() / q['vC'][M3][:, [b]].sum():+.4f}" for b in OB))
    nse = np.sqrt((WB[M3][:, OB] ** 2 * Rv[M3, HX[h]][:, OB]).sum()) / dn; wext = (WB[M3][:, OB] * Rt[M3, HX[h]][:, OB]).sum(1); rg = np.random.default_rng(5); iB = rg.integers(0, len(M3), (2000, len(M3))); bs = np.std(wext[iB].sum(1) / q["vC"][M3][:, OB].sum(1)[iB].sum(1)); P(f"  {h} extended t level: random-to-random noise {nse:.4f}, cluster bootstrap {bs:.4f}"); RES[f"ext_noise_{h}"] = float(max(nse, bs))
    F1v = (WB[M3][:, OB] * X["Rmean"][M3, i][:, OB]).sum() / dn; P(f"  {h} F1's level against extended: {F1v - (WB[M3][:, OB] * Rt[M3, HX[h]][:, OB]).sum() / dn:+.4f}")
    P(f"  {h} M3 OUTER A_x {(WB[M3][:, OB] * X['Dx'][M3, i][:, OB]).sum() / dn:+.4f}, A_RR {(WB[M3][:, OB] * X['DRR'][M3, i][:, OB]).sum() / dn:+.4f}; with extended, cross D - level {(WB[M3][:, OB] * (X['Drawx'][M3, i] - Rx[M3, HX[h]])[:, OB]).sum() / dn:+.4f}")
# K4: X11's MID cross field level
NJ = json.load(open(os.path.join(RB, "X11_cross_shear_diagnosis", "x11_analysis_results.json")))["nulls"]; k4 = []
for h in HH:
    q = C[("0.034", h)]; WB, _, _ = wb(h); dn = q["vC"][:, MB].sum(); lvx = (WB[:, MB] * Rx[:, HX[h]][:, MB]).sum() / dn; lvt = (WB[:, MB] * Rt[:, HX[h]][:, MB]).sum() / dn; lF1 = (WB[:, MB] * X["Rmeanx"][:, HI[h]][:, MB]).sum() / dn; J_ = NJ[f"canonical|{h}"]; sc_ = J_["rand_F1"] / lF1; k4.append(max(abs(lvx * sc_ - J_["rand_ext"]), abs(lvt * sc_ - J_["rand_ext_t"]))); P(f"  K4 {h}: template ratio X7 C* / this chain's C* from F1's cross level {sc_:.4f}; extended MID cross {lvx * sc_:+.5f} (X11 {J_['rand_ext']:+.5f}), tangential {lvt * sc_:+.5f} (X11 {J_['rand_ext_t']:+.5f})")
check("K4", max(k4) <= 0.005 and NA.sum() == 6499, f"extended randoms reproduce X11's field levels: max |d| {max(k4):.5f}; accepted {int(NA.sum())} (X11 6499)")
# Other keys under C4d, f* 0.034
for f, h in CELLS[:2]:
    q = C[(f, h)]; n0 = nsum(h)[:, OB].sum(1); n1 = nsum(h, D=Dext(h))[:, OB].sum(1); vC = q["vC"][:, OB].sum(1); V = q["V"][:, OB].sum(1); c = q["cells"]["G-OUT-Mall"]; zm = (n1.sum() / vC.sum() - c["pred"]) / c["s"]; nm = nsum(h)[:, MB].sum(1); nm1 = nsum(h, D=Dext(h))[:, MB].sum(1); vm = q["vC"][:, MB].sum(1); Ik = q["I"][q["TID"] == 2]; ct = q["cells"]["G-MID-T3"]; zt = (nm1[Ik].sum() / vm[Ik].sum() - ct["pred"]) / ct["s"]; P(f"  under C4d, f* {f} {h}: G-OUT-Mall {c['Z']:+.2f} > {zm:+.2f}; G-MID-T3 {ct['Z']:+.2f} > {zt:+.2f}; M1 {q['cells']['G-OUT-M1']['Z']:+.2f} > {(n1[T3 == 0].sum() / vC[T3 == 0].sum() - q['cells']['G-OUT-M1']['pred']) / q['cells']['G-OUT-M1']['s']:+.2f}; M2 {q['cells']['G-OUT-M2']['Z']:+.2f} > {(n1[T3 == 1].sum() / vC[T3 == 1].sum() - q['cells']['G-OUT-M2']['pred']) / q['cells']['G-OUT-M2']['s']:+.2f}")
    RES[f"C4d_other_{f}_{h}"] = dict(Mall=float(zm), T3=float(zt))
# ------------- leak T
P("\nC4e PSF leakage per tile, X7's stored stack")
effect("C4e", "per-tile leakage in place of per-patch", Zdata(lambda h: nsum(h, leak=X["leakT"][:, HX[h], 0])), "I")
for h in HH:
    WB, _, _ = wb(h); i = HI[h]; L = (WB * X["leakT"][:, HX[h], 0])[M3][:, OB].sum(1); Rd = (WB * (X["Rmean"][:, i] - Rt[:, HX[h]]))[M3][:, OB].sum(1); Rc = (WB * X["Rmean"][:, i])[M3][:, OB].sum(1); P(f"  post-result, overlap of C4e and C4d, {h}: per-cluster corr(leakT stack, F1 random - extended) {np.corrcoef(L, Rd)[0, 1]:+.3f}, with F1's random stack {np.corrcoef(L, Rc)[0, 1]:+.3f}; leakT's per-patch partner in A units {(WB * X['leakP'][:, HX[h], 0])[M3][:, OB].sum() / C[('0.034', h)]['vC'][M3][:, OB].sum():+.4f}, per-tile {(WB * X['leakT'][:, HX[h], 0])[M3][:, OB].sum() / C[('0.034', h)]['vC'][M3][:, OB].sum():+.4f}")
# ------------- n(z)
P("\nC4c photo-z, F1's C5d route")
PCH = PchipInterpolator(np.r_[0, 0.295, [0.510, 0.706, 0.934, 1.321, 1.484, 2.330]], np.r_[0, np.sqrt(7.942 ** 3 / (0.295 * (21.863 + (21.863 - 19.455) / (0.706 - 0.510) * (0.510 - 0.295)))), [13.588, 17.351, 21.576, 27.601, 30.512, 38.988]])
HV = {"h0672": 0.672, "h0686": 0.686}
def DM(z, h): return PCH(np.minimum(np.asarray(z, float), 2.33)) * 101.54 / HV[h]
NZ = {}
with tarfile.open(os.path.join(REPO, "..", "_external_data", "kids_lensing_zsplit", "KiDS1000_SOM_N_of_Z.tar.gz")) as tf:
    for m_ in tf.getmembers():
        if m_.name.endswith("_Nz.asc"): t = int(m_.name.split("TOMO")[1][0]); a = np.loadtxt(io.TextIOWrapper(tf.extractfile(m_))); NZ[t] = (a[:, 0], a[:, 1])
SOM = np.loadtxt(os.path.join(REPO, "..", "_external_data", "cfg592_work", "cfg", "SOM_cov_multiplied.asc")); SDZ = np.sqrt(np.diag(SOM))
FC = os.environ["M3A1_KIDS"]; zb = np.load(os.path.join(FC, "zb.npy"), mmap_mode="r")[::20].astype(float); w = np.load(os.path.join(FC, "w.npy"), mmap_mode="r")[::20].astype(float); TB = [0.1, 0.3, 0.5, 0.7, 0.9, 1.2]
def isc(zl, zs, h): DlM = float(DM(zl, h)); DMs = DM(zs, h); return np.clip((DMs - DlM) / DMs, 0, None) * DlM / (1 + zl)
def F(zl, h, dz=0.0):
    s_ = (zb > zl + 0.2) & (zb <= 1.2); i = isc(zl, zb[s_], h); t_ = np.digitize(zb[s_], TB); it = np.zeros_like(i)
    for t in range(1, 6):
        zz, nn = NZ[t]; it[t_ == t] = np.trapz(nn * isc(zl, np.maximum(zz + dz * SDZ[t - 1], 0), h), zz) / np.trapz(nn, zz)
    return float((w[s_] * i ** 2).sum() / (w[s_] * i * it).sum())
GR = np.array([0.05, 0.1, 0.2, 0.3, 0.4, 0.5]); FH = {h: np.array([F(z_, h) for z_ in GR]) for h in HH}; FU = {h: np.array([F(z_, h, 1.0) for z_ in GR]) for h in HH}; FD = {h: np.array([F(z_, h, -1.0) for z_ in GR]) for h in HH}
P(f"  SOM dz sigma per bin {np.round(SDZ[:5], 4).tolist()}; F(z_l) h 0.672 at {GR.tolist()}: {np.round(FH['h0672'], 3).tolist()}; n(z) up 1 sigma {np.round(FU['h0672'], 3).tolist()}, down {np.round(FD['h0672'], 3).tolist()}")
effect("C4c", "SOM bin n(z) in Sigma_crit (F1 calls it a bound; X13 an extreme hypothesis)", Zdata(lambda h: nsum(h) * np.interp(zc, GR, FH[h])[:, None], scale_s=True), "I")
ZU = Zdata(lambda h: nsum(h) * np.interp(zc, GR, FU[h])[:, None], scale_s=True); ZD = Zdata(lambda h: nsum(h) * np.interp(zc, GR, FD[h])[:, None], scale_s=True); dnz = {x: abs(ZU[x] - ZD[x]) / 2 for x in CELLS}; P(f"  n(z) shift +- 1 sigma of KiDS's dz: dZ {[round(v, 3) for v in dnz.values()]}")
P("  C4b m: KiDS's per-bin m is not on disk as a table this lane reads. Provisional ceiling 0.02 of A: dZ " + " ".join(f"{0.02 * base(*x)['meas'] / base(*x)['s']:.2f}" for x in CELLS) + f"; reach {0.02 * c0['meas'] / c0['s'] / (c0['Z'] - 2):.2f} at f* 0.034 h 0.672. Not counted")
# ------------- C3
P("\nC3a joint chi^2, BA1's method")
def keys(W, q, f, h):
    n = nsum(h); vC = q["vC"]; O = {}; I = q["I"]; TID = q["TID"]; band = {"INNER": IB, "MID": MB, "OUTER": OB}
    S = {b: (n[:, ix].sum(1), vC[:, ix].sum(1)) for b, ix in band.items()}
    rr = lambda Ix, b: (W[:, Ix] @ S[b][0][Ix]) / (W[:, Ix] @ S[b][1][Ix])
    KT = np.array([0.0]); xkt = XKT
    def wls(Wt, Xm, nn, dd): F_ = np.einsum("ri,i,ij,ik->rjk", Wt, dd, Xm, Xm); g = np.einsum("ri,ij,i->rj", Wt, Xm, nn); return np.linalg.solve(F_, g[..., None])[..., 0]
    X1 = np.c_[np.ones(len(I)), xkt]
    O["G-IN-all"] = rr(I, "INNER")
    for t in range(3): O[f"G-MID-T{t + 1}"] = rr(I[TID == t], "MID")
    O["G-MID-b"] = wls(W[:, I], X1, S["MID"][0][I], S["MID"][1][I])[:, 1]; O["G-OUT-all"] = rr(I, "OUTER")
    for t in range(3): O[f"G-OUT-T{t + 1}"] = rr(I[TID == t], "OUTER")
    O["G-OUT-b"] = wls(W[:, I], X1, S["OUTER"][0][I], S["OUTER"][1][I])[:, 1]; O["G-OUT-Mall"] = rr(ALLI, "OUTER")
    for t in range(3): O[f"G-OUT-M{t + 1}"] = rr(np.where(T3 == t)[0], "OUTER")
    O["G-IN-Mall"] = rr(ALLI, "INNER"); return O
from astropy.io import fits
E_ = fits.open(os.path.join(REPO, "real_research", "data", "erass1cl_primary_v3.2.fits"))[1].data; idx_ = {str(s_).strip(): k for k, s_ in enumerate(E_["NAME"])}; KT = np.asarray(E_["KT"], float)[np.array([idx_[str(x).strip()] for x in X["name"]])]; I0 = np.where(np.isfinite(KT) & (KT > 0))[0]; XKT = np.log10(KT[I0] / np.median(KT[I0]))
assert np.array_equal(I0, C[("0.034", "h0672")]["I"])
rg = np.random.default_rng(20261031); ix = rg.integers(0, N, size=(2000, N)); WB_ = np.stack([np.bincount(r, minlength=N) for r in ix]).astype(float); WJ = np.array([(C[("0.034", "h0672")]["PATCH"] != p).astype(float) for p in range(30) if np.any(C[("0.034", "h0672")]["PATCH"] == p)])
def joint(cells, ks, R, drop=None, d_override=None):
    d = np.array([cells[k]["meas"] - cells[k]["pred"] for k in ks]) if d_override is None else d_override; s = np.array([cells[k]["s"] for k in ks]); w_, Vv = np.linalg.eigh(R); ok = w_ >= 1e-3 * w_.max(); z = Vv[:, ok].T @ (d / s); c2 = float((z * z / w_[ok]).sum()); return c2, int(ok.sum()), float(chi2.sf(c2, int(ok.sum())))
JR = {}
for f, h in CELLS:
    q = C[(f, h)]; Kb = keys(WB_, q, f, h); Kj = keys(WJ, q, f, h); ks = list(Kb); Xb = np.array([Kb[k] for k in ks]); Xj = np.array([Kj[k] for k in ks]); nj = Xj.shape[1]; Dj = Xj - Xj.mean(1, keepdims=True); Cj = (nj - 1) / nj * Dj @ Dj.T; Rb = np.corrcoef(Xb); Rj = Cj / np.sqrt(np.outer(np.diag(Cj), np.diag(Cj)))
    a = joint(q["cells"], ks, Rb); b = joint(q["cells"], ks, Rj); im = ks.index("G-OUT-M3"); nb = [k for k in ks if k != "G-OUT-M3"]; ii_ = [ks.index(k) for k in nb]; a2 = joint(q["cells"], nb, Rb[np.ix_(ii_, ii_)]); JR[f"{f}|{h}"] = dict(chi2=a[0], dof=a[1], p=a[2], jack_chi2=b[0], jack_p=b[2], noM3=a2[0], noM3_p=a2[2]); P(f"  f* {f} {h}: chi^2 {a[0]:.1f} / {a[1]}, p {a[2]:.2e}; jackknife R {b[0]:.1f}, p {b[2]:.2e}; without G-OUT-M3 {a2[0]:.1f}, p {a2[2]:.2e}; R(M3, Mall) {Rb[im, ks.index('G-OUT-Mall')]:.2f}, R(M3, OUT-T3) {Rb[im, ks.index('G-OUT-T3')]:.2f}, R(M3, MID-T3) {Rb[im, ks.index('G-MID-T3')]:.2f}")
RES["joint"] = JR
P("\nC3b M3 stability, own bootstrap and 30-patch jackknife; Z with s fractional fixed unless said")
def zsel(q, sel, n=None, fr_=None):
    n_ = q["n"][:, 2] if n is None else n; vC = q["vC"][:, OB].sum(1); V = q["V"][:, OB].sum(1); A = n_[sel].sum() / vC[sel].sum(); Pp = V[sel].sum() / vC[sel].sum(); return A, Pp
RG2 = np.random.default_rng(20261102)
STAB = {}
for f, h in CELLS:
    q = C[(f, h)]; c = q["cells"]["G-OUT-M3"]; fr_ = c["s"] / c["meas"]; n = q["n"][:, 2]; vC = q["vC"][:, OB].sum(1); V = q["V"][:, OB].sum(1); nr = (wb(h)[0] * X["D"][:, HI[h]])[:, OB].sum(1); PT = q["PATCH"]
    idn = np.ones(len(M3)); a0 = (idn @ n[M3]) / (idn @ vC[M3]); p0 = (idn @ V[M3]) / (idn @ vC[M3]); k6 = abs((a0 - p0) / c["s"] - c["Z"])
    iB = RG2.integers(0, len(M3), (4000, len(M3))); Ab = n[M3][iB].sum(1) / vC[M3][iB].sum(1); Pb = V[M3][iB].sum(1) / vC[M3][iB].sum(1); Db = Ab - Pb; sA = Ab.std(ddof=1); sD = Db.std(ddof=1); pz = float(np.mean(Db <= 2 * c["s"]))
    Pj = [p_ for p_ in range(30) if np.any(PT[M3] == p_)]; Dj = np.array([zsel(q, M3[PT[M3] != p_])[0] - zsel(q, M3[PT[M3] != p_])[1] for p_ in Pj]); nj = len(Pj); sJ = np.sqrt((nj - 1) / nj * ((Dj - Dj.mean()) ** 2).sum()); Zpatch = [((zsel(q, M3[PT[M3] != p_])[0] - zsel(q, M3[PT[M3] != p_])[1]) / (fr_ * zsel(q, M3[PT[M3] != p_])[0])) for p_ in Pj]
    Lo = []; 
    for i_ in range(len(M3)):
        s_ = np.delete(M3, i_); A_, P_ = zsel(q, s_); Lo.append((A_ - P_) / (fr_ * A_))
    ctr = (n - V)[M3]; od = np.argsort(-ctr); Drop = {}
    nuln = n - (a0 - p0) * V / p0; ctrn = (nuln - V)[M3]; odn = np.argsort(-ctrn); zb_ = lambda sel, nn: (zsel(q, sel, nn)[0] - zsel(q, sel, nn)[1]) / (fr_ * zsel(q, sel, nn)[0])
    for k in (1, 3, 5, 10): Drop[k] = (zb_(np.delete(M3, od[:k]), n), zb_(np.delete(M3, odn[:k]), nuln))
    z_nul = zb_(M3, nuln); k3 = int(np.ceil(0.05 * len(M3))); tr = M3[np.argsort(ctr)[k3:-k3]]; A_t, P_t = zsel(q, tr); iBt = RG2.integers(0, len(tr), (2000, len(tr))); st = (n[tr][iBt].sum(1) / vC[tr][iBt].sum(1) - V[tr][iBt].sum(1) / vC[tr][iBt].sum(1)).std(ddof=1); iso = (A_t - P_t) / st
    subs = {"N": M3[(ra[M3] > 100) & (ra[M3] < 260)], "S": M3[~((ra[M3] > 100) & (ra[M3] < 260))], "z low": M3[zc[M3] < np.median(zc[M3])], "z high": M3[zc[M3] >= np.median(zc[M3])], "gas low": M3[Mg[M3] < np.median(Mg[M3])], "gas high": M3[Mg[M3] >= np.median(Mg[M3])]}
    def zs(sel):
        iB_ = RG2.integers(0, len(sel), (2000, len(sel))); D_ = n[sel][iB_].sum(1) / vC[sel][iB_].sum(1) - V[sel][iB_].sum(1) / vC[sel][iB_].sum(1); A_, P_ = zsel(q, sel); return A_, P_, (A_ - P_) / D_.std(ddof=1), len(sel)
    so = {k: zs(v) for k, v in subs.items()}; nb6 = nsum(h)[:, 6]; nb7 = nsum(h)[:, 7]; bins = {}
    for b, nb in ((6, nb6), (7, nb7)):
        vcb = q["vC"][:, b]; Vb = q["V"][:, b]; iB_ = RG2.integers(0, len(M3), (2000, len(M3))); D_ = nb[M3][iB_].sum(1) / vcb[M3][iB_].sum(1) - Vb[M3][iB_].sum(1) / vcb[M3][iB_].sum(1); A_ = nb[M3].sum() / vcb[M3].sum(); P_ = Vb[M3].sum() / vcb[M3].sum(); bins[b] = (A_, P_, (A_ - P_) / D_.std(ddof=1))
    wsh = np.sort(vC[M3])[::-1] / vC[M3].sum(); neff = vC[M3].sum() ** 2 / (vC[M3] ** 2).sum(); weff = np.average(np.log10(Mg[M3]), weights=V[M3]); zeff = np.average(zc[M3], weights=V[M3])
    STAB[f"{f}|{h}"] = dict(k6=k6, s_grader=c["s"], s_boot_A=sA, s_boot_diff=sD, s_jack_diff=float(sJ), Z_boot_diff=(a0 - p0) / sD, Z_jack_diff=(a0 - p0) / float(sJ), p_below_2s=pz, loo=[min(Lo), max(Lo)], patch=[min(Zpatch), max(Zpatch)], drop={k: list(v) for k, v in Drop.items()}, z_null=z_nul, trim=[A_t, P_t, iso], subs={k: list(v) for k, v in so.items()}, bins={str(k): list(v) for k, v in bins.items()}, neff=neff, lgMg_eff=weff, z_eff=zeff, top5share=float(wsh[:5].sum()), top10share=float(wsh[:10].sum()))
    if f == "0.034": P(f"  {h}: grader s {c['s']:.3f}; own s(A) boot {sA:.3f}; s(A-pred) boot {sD:.3f}, jack {sJ:.3f} > Z {(a0 - p0) / sD:+.2f}, {(a0 - p0) / sJ:+.2f}; bootstrap P(A-pred <= 2 s_grader) {pz:.4f}; leave-one-out Z {min(Lo):+.2f} to {max(Lo):+.2f}; leave-one-patch {min(Zpatch):+.2f} to {max(Zpatch):+.2f}; effective lg Mg {weff:.2f}, z {zeff:.3f}; N_eff of template {neff:.0f}, top 5 hold {wsh[:5].sum():.1%}, top 10 {wsh[:10].sum():.1%}")
    if f == "0.034": P("     drop top k by n - v, real (null): " + "; ".join(f"{k}: {v[0]:+.2f} ({v[1]:+.2f})" for k, v in Drop.items()) + f"; null full {z_nul:+.3f}; 10 % trimmed A {A_t:.3f} pred {P_t:.3f} Z {iso:+.2f}")
    if f == "0.034": P("     splits, A, pred, Z own bootstrap, N: " + "; ".join(f"{k} {v[0]:.2f} {v[1]:.2f} {v[2]:+.2f} ({v[3]})" for k, v in so.items()) + f"; bin 1.42-2.06: {bins[6][0]:.2f} {bins[6][1]:.2f} {bins[6][2]:+.2f}; bin 2.06-3: {bins[7][0]:.2f} {bins[7][1]:.2f} {bins[7][2]:+.2f}")
RES["stability"] = STAB; k6m = max(v["k6"] for v in STAB.values()); check("K6", k6m <= 1e-9, f"identity draw returns full Z: {k6m:.1e}")
znm = max(abs(v["z_null"]) for v in STAB.values()); check("MUTATE d", znm <= 0.05, f"excess removed: |Z| {znm:.3f}")
rs = np.random.default_rng(20261103); perm = rs.permutation(N)[:len(M3)]; q = C[("0.034", "h0672")]; n = q["n"][:, 2]; vC = q["vC"][:, OB].sum(1); V = q["V"][:, OB].sum(1); iB_ = rs.integers(0, len(perm), (2000, len(perm))); Ds = (n[perm][iB_].sum(1) / vC[perm][iB_].sum(1) - V[perm][iB_].sum(1) / vC[perm][iB_].sum(1)).std(ddof=1); zsh = (n[perm].sum() / vC[perm].sum() - V[perm].sum() / vC[perm].sum()) / Ds; zo = STAB["0.034|h0672"]["Z_boot_diff"]; bm = zo - zsh >= 1; check("MUTATE c", bm, f"membership shuffled, own bootstrap Z {zsh:+.2f} against {zo:+.2f}: {'BITES' if bm else 'DOES NOT BITE'}")
few = []
for x in CELLS:
    s = STAB[f"{x[0]}|{x[1]}"]; z0 = base(*x)["Z"]; d3 = s["drop"][5]; few.append(d3[0] <= 2 and abs(s["z_null"] - d3[1]) < 0.5 * (z0 - d3[0]))
# ------------- Z_tot
P("\nC2b Z_tot, quadrature; shifts not applied")
ZB = json.load(open(os.path.join(RB, "ZN4_cluster_resolution", "zn4_boot_results.json")))["draws"]; RES["Ztot"] = {}
OG = {"0.034": (4.38, 4.50), "0.0615": (4.10, 4.22)}
for f, h in CELLS:
    c = base(f, h); zs_ = np.array([ZB[d][f][4][h]["G-OUT-M3"] for d in ZB]); sd_seed = 0.5 * (np.percentile(zs_, 84) - np.percentile(zs_, 16)) * c["s"]; sg = abs(dzdd) * GW["se"] * c["s"]; ssl = 0.5 * (OG[f][1] - OG[f][0]) * c["s"]; sm = 0.02 * c["meas"]; snz = dnz[(f, h)] * c["s"]; sl = abs(EFF["C4e"]["dZ"][f"{f}|{h}"]) * c["s"]; sr = RES.get(f"ext_noise_{h}", 0.0) * c["meas"] / c["meas"]; tot = np.sqrt(c["s"] ** 2 + sg ** 2 + ssl ** 2 + sd_seed ** 2 + sm ** 2 + snz ** 2 + sl ** 2); zt = (c["meas"] - c["pred"]) / tot
    RES["Ztot"][f"{f}|{h}"] = dict(s=c["s"], gas=sg, slope=ssl, seed=sd_seed, m=sm, nz=snz, leak=sl, tot=tot, Z=zt); P(f"  f* {f} {h}: s {c['s']:.3f}, gas {sg:.3f}, slope {ssl:.3f}, seed {sd_seed:.3f}, m {sm:.3f}, n(z) {snz:.3f}, leak {sl:.3f} > total {tot:.3f}, Z_tot {zt:+.2f}")
# ------------- label
P("\nNET"); IDS = [k for k, v in EFF.items() if v["cls"] == "I"]; P(f"  class I effects: {IDS}"); net = {}; netno = {}; lowonly = {}
for x in CELLS:
    kk = f"{x[0]}|{x[1]}"; z0 = base(*x)["Z"]; net[x] = z0 - sum(EFF[i]["dZ"][kk] for i in IDS); netno[x] = z0 - sum(EFF[i]["dZ"][kk] for i in IDS if i != "C2a"); lowonly[x] = z0 - sum(max(EFF[i]["dZ"][kk], 0) for i in IDS)
P("  net Z, all class I as frozen: " + " ".join(f"{net[x]:+.2f}" for x in CELLS)); P("  net Z, C2a out, since C1a and C2a read the same selection: " + " ".join(f"{netno[x]:+.2f}" for x in CELLS)); P("  lowering-only, not graded: " + " ".join(f"{lowonly[x]:+.2f}" for x in CELLS))
P("  net Z without C4c, since F1 calls it a bound, not graded: " + " ".join(f"{net[x] + EFF['C4c']['dZ'][f'{x[0]}|{x[1]}']:+.2f}" for x in CELLS))
mx = {i: max(EFF[i]["reach"].values()) for i in IDS}; P("  largest reach per class I effect: " + ", ".join(f"{i} {v:+.2f}" for i, v in mx.items()))
top = [i for i, v in mx.items() if v >= 1 / 3]; art = all(net[x] <= 2 for x in CELLS); V = "ARTEFACT" if art else "PARTLY" if top else "REAL"; tags = []
netd = np.mean([net[x] - base(*x)["Z"] for x in CELLS]); 
if netd > 0: tags.append("[WORSE THAN STATED]")
if all(v["Z"] <= 2 for v in RES["Ztot"].values()): tags.append("[NOT SIGNIFICANT WITH FULL ERRORS]")
if all(few): tags.append("[FEW-CLUSTER]")
ok = all(a for _, a in CHK); P(f"\nchecks {sum(a for _, a in CHK)} of {len(CHK)}")
P(f"VERDICT{' (NO VERDICT: a check failed)' if not ok else ''}: {V} {' '.join(tags)}; reaching a third: {top}; mean net shift in Z {netd:+.2f}")
RES.update(effects=EFF, verdict=V, tags=tags, checks=dict(CHK), net={f"{a}|{b}": v for (a, b), v in net.items()}, net_noC2a={f"{a}|{b}": v for (a, b), v in netno.items()}, lowering={f"{a}|{b}": v for (a, b), v in lowonly.items()})
if DEV: sys.exit(0)
json.dump(RES, open(os.path.join(HERE, f"m3a1_results{TAG}.json"), "w"), indent=1, default=float); open(os.path.join(HERE, f"m3a1{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
