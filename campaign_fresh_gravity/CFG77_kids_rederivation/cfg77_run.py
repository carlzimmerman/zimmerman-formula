# CFG77 runner.  Pass lines are in CFG77_FROZEN.md (written before any headline number was computed).
import os, sys, json, math, time
import numpy as np
import cfg77_lib as L
from scipy.stats import chi2 as chi2d
t0 = time.time()
RES = {}
def P(*a): print(*a, flush=True)
def check(name, ok, detail):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         {detail}"); RES.setdefault("checks", {})[name] = bool(ok)
def rel(a, b): return float(np.max(np.abs(np.asarray(a) / np.asarray(b) - 1)))

P("=" * 100); P("CONTROLS"); P("=" * 100)
dat = L.load_data("Color"); dsr = L.load_data("Sersic")

# ---- K1 covariance controls
def chi2_all(dd):
    l, e = np.arange(15), np.arange(15, 30)
    D = dd["d"][e] - dd["d"][l]
    CD = dd["C"][np.ix_(e, e)] + dd["C"][np.ix_(l, l)] - dd["C"][np.ix_(e, l)] - dd["C"][np.ix_(l, e)]
    return D, CD
D15, CD15 = chi2_all(dat)
c_solve = float(D15 @ np.linalg.solve(CD15, D15))
Lc = np.linalg.cholesky(CD15); wv = np.linalg.solve(Lc, D15); c_chol = float(wv @ wv)
c_inv = float(D15 @ np.linalg.inv(CD15) @ D15)
# direct 30x30 route: transform matrix T (15x30), C_D = T C T^T
T = np.hstack([-np.eye(15), np.eye(15)]); CD_T = T @ dat["C"] @ T.T
c_T = float((T @ dat["d"]) @ np.linalg.solve(CD_T, T @ dat["d"]))
c15_sers = float((lambda D, CD: D @ np.linalg.solve(CD, D))(*chi2_all(dsr)))
diag_dev = float(np.max(np.abs(np.sqrt(np.diag(dat["C"])) / dat["err"] - 1)))
K1ok = max(abs(c_solve / c_chol - 1), abs(c_solve / c_inv - 1), abs(c_solve / c_T - 1)) < 1e-8
check("K1 covariance: solve = Cholesky = inverse = 30x30 transform (1e-8); diag vs error col 1e-3; 15-bin split 119.9/69.1 +-0.5",
      K1ok and diag_dev < 1e-3 and abs(c_solve - 119.9) < 0.5 and abs(c15_sers - 69.1) < 0.5,
      f"u-r {c_solve:.3f} (chol {c_chol:.3f}, inv {c_inv:.3f}, T {c_T:.3f}); Sersic {c15_sers:.3f}; sqrt(diag C)/err-1 max {diag_dev:.1e}; colour-file min values {dat['mins']}")
P("         late/early g_bar columns identical:", np.allclose(dat["g"], dat["g2"]))

# ---- K2 projector
k = 1e12
r = np.geomspace(1e-4, 1e4, 8000); R = np.array([0.01, 0.1, 1.0, 5.0])
sis = rel(L.dsigma(R, r, k * r), k / (4 * R))
M0 = 3e11
pm = rel(M0 / (math.pi * R ** 2 * 1e0), M0 / (math.pi * R ** 2))     # point mass handled analytically (identity), reported only
rs, rhos = 0.2, 1e15                                                  # Msun/Mpc^3
rr = np.geomspace(1e-5 * rs, 1e4 * rs, 12000)
x_ = rr / rs; Mn = 4 * math.pi * rhos * rs ** 3 * (np.log1p(x_) - x_ / (1 + x_))
Rn = np.array([0.02, 0.1, 0.2, 0.5, 1.0, 2.0])
def wb(R):
    """Wright & Brainerd 2000 NFW: mean Sigma(<x) = 4 rho_s r_s/x^2 [ln(x/2) + F(x)], Sigma(x) = 2 rho_s r_s/(x^2-1) [1 - F(x)],
    F = arccosh(1/x)/sqrt(1-x^2) (x<1), arccos(1/x)/sqrt(x^2-1) (x>1), 1 at x=1  (first draft of this control had an incomplete formula -- disclosed)"""
    out = []
    for xx in R / rs:
        if xx < 1: F = math.acosh(1 / xx) / math.sqrt(1 - xx ** 2)
        elif xx > 1: F = math.acos(1 / xx) / math.sqrt(xx ** 2 - 1)
        else: F = 1.0
        mean = 4 * rhos * rs / xx ** 2 * (math.log(xx / 2) + F)
        sig = 2 * rhos * rs / 3 if xx == 1 else 2 * rhos * rs / (xx ** 2 - 1) * (1 - F)
        out.append(mean - sig)
    return np.array(out)
nfw = rel(L.dsigma(Rn, rr, Mn), wb(Rn))
# explicit point-mass check via dsigma with m0 only (no shells)
pmcheck = rel(L.dsigma(R, np.array([1e-4, 2e-4]), np.array([0.0, 0.0]), m0=M0), M0 / (math.pi * R ** 2))
eds = L.one_plus_delta_ta(1.0, Om=1.0)
check("K2 projector: SIS k/(4R) 1e-3; NFW vs Wright&Brainerd 1e-3; point mass exact; EdS 1+delta_ta = 9pi^2/16 (1e-3)",
      sis < 1e-3 and nfw < 1e-3 and pmcheck < 1e-9 and abs(eds / (9 * math.pi ** 2 / 16) - 1) < 1e-3,
      f"SIS {sis:.1e}; NFW {nfw:.1e}; point mass {pmcheck:.1e}; EdS {eds:.6f} vs {9*math.pi**2/16:.6f}; LCDM 1+delta_ta(z=0) = {L.dta(0.0):.3f}, (z=0.25) {L.dta(0.25):.3f}")

# ---- K3 law mass independence at fixed g_bar (untruncated, deep regime)
def law_ds_at_g(M, g_si, foot="canonical"):
    a0 = L.A0[foot]; g = g_si / L.SI_ACC; Rm = math.sqrt(L.G_MPC * M / g)
    r_ = np.geomspace(1e-5, 60.0, 5000); y = L.G_MPC * M / r_ ** 2 / a0
    Md = M * (L.nu_mono(y) - 1.0)
    return float(L.dsigma(np.array([Rm]), r_, Md, m0=Md[0])[0] + M / (math.pi * Rm ** 2)) * 1e-12, Rm
rows = []
for g_si in (1e-13, 1e-12):
    a, Ra = law_ds_at_g(1e10, g_si); b, Rb = law_ds_at_g(1e11, g_si)
    sis_val = math.sqrt(L.A0["canonical"] * g_si / L.SI_ACC) / (4 * L.G_MPC) * 1e-12       # dark SIS value; plus baryon g/(pi G)
    rows.append((g_si, abs(a / b - 1), a, b, Ra, Rb))
check("K3 law deep regime: DeltaSigma(g_bar) mass-independent (1e10 vs 1e11) to 3% at 1e-13, 1e-12 (untruncated)",
      all(x[1] < 0.03 for x in rows), "; ".join(f"g={x[0]:.0e}: rel diff {x[1]:.1e} (DS {x[2]:.4f}/{x[3]:.4f} Msun/pc2, R {x[4]:.3f}/{x[5]:.3f} Mpc)" for x in rows))

# ---- lenses, groups, K1 set
len_ = L.load_lenses()
grp = L.make_groups(len_)
gmid = dat["g"] / L.SI_ACC
med = {}
for c in (0, 1):
    Mg = len_["Mgal"][len_["typ"] == c]
    med[c] = np.array([np.median(np.sqrt(L.G_MPC * Mg / gm)) for gm in gmid])
K1 = np.where((med[0] < 0.3) & (med[1] < 0.3))[0]
P("  lens counts late/early:", int((len_["typ"] == 0).sum()), int((len_["typ"] == 1).sum()),
  "median logM late/early %.3f %.3f" % (np.median(len_["logM"][len_["typ"] == 0]), np.median(len_["logM"][len_["typ"] == 1])))
P("  K1 =", list(K1), " median R late/early (Mpc):", np.round(med[0][K1], 3), np.round(med[1][K1], 3))

# ---- K4 grouped stack vs exact per-lens (400 random lenses)
rng = np.random.default_rng(77)
sub = rng.choice(len(len_["z"]), 400, replace=False)
mask = np.zeros(len(len_["z"]), bool); mask[sub] = True
gs = L.make_groups(len_, sel=mask, dlogm=0.01, dz=0.03)
exact = {}
for c in (0, 1):
    idx = sub[len_["typ"][sub] == c]
    ex = dict(n=np.ones(len(idx)), Mgal=len_["Mgal"][idx], logM=len_["logM"][idx], z=len_["z"][idx])
    exact[c] = L.stack(ex, L.law_profile(ex, "canonical"))
    grpd = L.stack(gs[c], L.law_profile(gs[c], "canonical"))
    exact[c] = (exact[c], grpd)
dev = max(np.max(np.abs(exact[c][1][K1] / exact[c][0][K1] - 1)) for c in (0, 1))
# and vs the coarser default grouping on the full sample (resolution test): 0.02 dex / 0.06 z
check("K4 grouped stacking vs exact per-lens on 400 random lenses (1%, K1 bins)", dev < 0.01,
      f"max rel dev {dev:.1e} (subsample has groups ~1 lens each, so this tests the group machinery, not the gridding); full-sample resolution test follows")

def full_stacks(grp_, model, **kw):
    if model == "law":
        return [L.stack(grp_[c], L.law_profile(grp_[c], kw["foot"], f_hot=(kw.get("f_hot", 0.0) if c == 1 else 0.0))) for c in (0, 1)]
    return [L.stack(grp_[0], L.lcdm_profile(grp_[0], "blue")), L.stack(grp_[1], L.lcdm_profile(grp_[1], "red"))]

P("=" * 100); P("HEADLINE: LAW  (foot, f_hot)"); P("=" * 100)
K1l = list(K1)
zero_chi2, D_obs, CD, _ = L.diff_stat(dat, K1l)
P(f"  zero-model chi2 (D_obs^T C_D^-1 D_obs on K1, 7 dof) = {zero_chi2:.3f}")
RES["zero_model_chi2"] = zero_chi2
law = {}
for foot in ("canonical", "alt"):
    st = full_stacks(grp, "law", foot=foot)
    c2 = L.diff_stat(dat, K1l, st[0], st[1])[0]
    law[foot] = (st, c2)
    P(f"  {foot:9s}: chi2_L = {c2:.3f}/7 (p {chi2d.sf(c2, 7):.2e});  max|D_L|/sigma_D = {np.max(np.abs((st[1]-st[0])[K1]/np.sqrt(np.diag(CD)))):.2e}")
    RES[f"chi2_L_{foot}"] = c2
st = law["canonical"][0]
P("  law stack K1 (Msun/pc2)  late:", np.round(st[0][K1], 3), " early:", np.round(st[1][K1], 3))
P("  data stack late:", np.round(dat["d"][K1], 3), " early:", np.round(dat["d"][K1 + 15], 3))
P("  all-15 law chi2 (canonical):", round(L.diff_stat(dat, list(range(15)), st[0], st[1])[0], 2))

P("  f_hot ladder (canonical), early lenses only:")
lad = {}
for f in (0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0):
    s = full_stacks(grp, "law", foot="canonical", f_hot=f)
    lad[f] = L.diff_stat(dat, K1l, s[0], s[1])[0]
P("   ", ", ".join(f"{f}: {v:.2f}" for f, v in lad.items()))
RES["ladder"] = {str(k): v for k, v in lad.items()}

P("=" * 100); P("LCDM CONTROL (CFG67 comparator)"); P("=" * 100)
sL = full_stacks(grp, "lcdm")
c_l = L.diff_stat(dat, K1l, sL[0], sL[1])[0]
# amplitude vs colour-blind law (0 = law): Ahat = D'C^-1 (Dobs - DL) / D'C^-1 D, D = D_Lambda - D_L
Dm = (sL[1] - sL[0])[K1] - (law["canonical"][0][1] - law["canonical"][0][0])[K1]
_, Dobs, CDk, _ = L.diff_stat(dat, K1l)
Ci = np.linalg.inv(CDk); DL_ = (law["canonical"][0][1] - law["canonical"][0][0])[K1]
Ahat = float(Dm @ Ci @ (Dobs - DL_) / (Dm @ Ci @ Dm)); sA = float((Dm @ Ci @ Dm) ** -0.5)
P(f"  chi2_Lambda = {c_l:.3f}/7 (p {chi2d.sf(c_l, 7):.3f});  Ahat = {Ahat:.3f} +- {sA:.3f} (stat; the +-0.1 dex floor not repeated)")
P("  LCDM stack K1 late:", np.round(sL[0][K1], 3), " early:", np.round(sL[1][K1], 3))
RES["chi2_lcdm"] = c_l; RES["Ahat"] = Ahat; RES["sigA_stat"] = sA
# H3 absolute (reported)
ee = L.diff_stat  # unused
Kk = np.asarray(K1l)
def abs_chi2(idx, mod):
    r_ = dat["d"][idx] - mod[Kk]; C_ = dat["C"][np.ix_(idx, idx)]; return float(r_ @ np.linalg.solve(C_, r_))
P(f"  absolute K1: LCDM early {abs_chi2(Kk+15, sL[1]):.1f}, late {abs_chi2(Kk, sL[0]):.1f};  law early {abs_chi2(Kk+15, st[1]):.1f}, late {abs_chi2(Kk, st[0]):.1f}")

P("=" * 100); P("K5 SWAP (early/late DATA swapped; models keep their classes)"); P("=" * 100)
sw_law = L.diff_stat(dat, K1l, st[0], st[1], swap=True)[0]
sw_lcdm = L.diff_stat(dat, K1l, sL[0], sL[1], swap=True)[0]
check("K5 swap: law chi2 barely moves (|delta|<0.5); LCDM rises to > 100 (README: 124.1)", abs(sw_law - law["canonical"][1]) < 0.5 and sw_lcdm > 100,
      f"law {law['canonical'][1]:.2f} -> {sw_law:.2f}; LCDM {c_l:.2f} -> {sw_lcdm:.2f}")
RES["swap"] = dict(law=sw_law, lcdm=sw_lcdm)

P("=" * 100); P("K6 MUTATE (early-type M_* and M_gal x2)"); P("=" * 100)
lenm = L.load_lenses(mutate=True); grm = L.make_groups(lenm)
stm = full_stacks(grm, "law", foot="canonical"); sLm = full_stacks(grm, "lcdm")
cm_law = L.diff_stat(dat, K1l, stm[0], stm[1])[0]; cm_lcdm = L.diff_stat(dat, K1l, sLm[0], sLm[1])[0]
check("K6 MUTATE: LCDM chi2 moves by > 1.0; law chi2 predicted to stay within 1.0 (mass independence)", abs(cm_lcdm - c_l) > 1.0 and abs(cm_law - law["canonical"][1]) < 1.0,
      f"law {law['canonical'][1]:.3f} -> {cm_law:.3f}; LCDM {c_l:.3f} -> {cm_lcdm:.3f}")
RES["mutate"] = dict(law=cm_law, lcdm=cm_lcdm)

P("=" * 100); P("REPRODUCTION TABLE"); P("=" * 100)
tgt = [("chi2_L canonical", law["canonical"][1], 28.1), ("chi2_L alt", law["alt"][1], 28.1)] + \
      [(f"ladder f_hot={f}", lad[f], v) for f, v in zip((0.0, 0.25, 0.5, 1.0, 1.5), (28.1, 18.2, 10.0, 4.8, 4.1))] + [("LCDM chi2", c_l, 6.5)]
for n, v, t in tgt:
    d = v - t; tag = "EXACT" if abs(d) <= 0.15 else ("APPROX" if abs(d) <= 1.0 else "NON-REPRODUCED")
    P(f"  {n:22s} mine {v:8.3f}   CFG {t:6.1f}   diff {d:+.3f}   {tag}")
    RES.setdefault("repro", {})[n] = (v, t, tag)

# ---- attack runs
if os.environ.get("ATTACK", "1") == "1":
    P("=" * 100); P("ATTACK RUNS (reported)"); P("=" * 100)
    # K1 choice
    for name, Kx in (("K1 (7 bins, 8-14)", list(range(8, 15))), ("bins 6-14 (9)", list(range(6, 15))), ("bins 9-14 (6)", list(range(9, 15))),
                     ("bins 10-14 (5)", list(range(10, 15))), ("bins 11-14 (4)", list(range(11, 15))), ("bins 8-11", [8, 9, 10, 11]), ("bins 12-14", [12, 13, 14]),
                     ("all 15", list(range(15)))):
        c_ = L.diff_stat(dat, Kx, law["canonical"][0][0], law["canonical"][0][1])[0]; z_ = L.diff_stat(dat, Kx)[0]
        cl_ = L.diff_stat(dat, Kx, sL[0], sL[1])[0]
        P(f"  {name:20s} law {c_:7.2f}/{len(Kx)} (p {chi2d.sf(c_, len(Kx)):.1e}); zero-model {z_:7.2f}; LCDM {cl_:7.2f}")
    # per-bin normalised difference
    P("  per-bin (D_obs - D_L)/sigma_D on K1:", np.round(((Dobs - DL_) / np.sqrt(np.diag(CDk))), 2))
    P("  eigen-mode contributions to chi2_L on K1 (whitened residuals^2):", np.round(np.linalg.solve(np.linalg.cholesky(CDk), Dobs - DL_) ** 2, 2))
    # M* floor / IMF (baryon mass scale)
    P("  M_* floor and IMF-like baryon-mass rescales (law, LCDM), canonical:")
    for name, kw in (("early M* +0.1 dex", dict(logm_shift_early=0.1)), ("early M* -0.1 dex", dict(logm_shift_early=-0.1)),
                     ("M_gal x0.7 both (IMF)", dict(mgal_scale=(0.7, 0.7))), ("M_gal x1.5 both", dict(mgal_scale=(1.5, 1.5))),
                     ("early M_gal x1.5 only", dict(mgal_scale=(1.0, 1.5))), ("early M_gal x0.7 only", dict(mgal_scale=(1.0, 0.7)))):
        lx = L.load_lenses(**kw); gx = L.make_groups(lx)
        s_l = full_stacks(gx, "law", foot="canonical"); s_c = full_stacks(gx, "lcdm")
        P(f"    {name:24s} law {L.diff_stat(dat, K1l, s_l[0], s_l[1])[0]:7.2f}   LCDM {L.diff_stat(dat, K1l, s_c[0], s_c[1])[0]:7.2f}")
    # lens-sample selection (isolation proxy): drop the most massive lenses, redshift halves
    P("  lens-sample proxies (isolation cannot be re-cut from the file; these vary the lens mix):")
    for name, sel in (("z<0.3", len_["z"] < 0.3), ("z>=0.3", len_["z"] >= 0.3), ("logM<=10.9", len_["logM"] <= 10.9), ("logM>10.3", len_["logM"] > 10.3)):
        gx = L.make_groups(len_, sel=sel)
        s_l = full_stacks(gx, "law", foot="canonical"); s_c = full_stacks(gx, "lcdm")
        P(f"    {name:12s} law {L.diff_stat(dat, K1l, s_l[0], s_l[1])[0]:7.2f}   LCDM {L.diff_stat(dat, K1l, s_c[0], s_c[1])[0]:7.2f}")
    # gridding resolution
    g2 = L.make_groups(len_, dlogm=0.03, dz=0.1)
    s2 = full_stacks(g2, "law", foot="canonical"); P(f"  coarser grouping (0.03 dex, dz 0.1): law chi2 {L.diff_stat(dat, K1l, s2[0], s2[1])[0]:.3f} (default {law['canonical'][1]:.3f})")
    # f_hot with R from M_true (alternative reading): bracket
    P("  f_hot ladder, alt reading (pair radius R from M_true too) -- implemented as early M_gal x(1+f) everywhere:")
    for f in (0.0, 0.5, 1.0, 1.5):
        lx = L.load_lenses(mgal_scale=(1.0, 1 + f)); gx = L.make_groups(lx); s_ = full_stacks(gx, "law", foot="canonical")
        P(f"    f={f}: {L.diff_stat(dat, K1l, s_[0], s_[1])[0]:.2f}")
    # Sersic
    P(f"  Sersic split (law): {L.diff_stat(dsr, K1l, law['canonical'][0][0], law['canonical'][0][1])[0]:.2f}/7 (CFG61 R1: 20.9)")

json.dump(RES, open("cfg77_results.json", "w"), indent=1, default=float)
P(f"\n{sum(RES['checks'].values())}/{len(RES['checks'])} controls pass; {time.time()-t0:.0f}s")
