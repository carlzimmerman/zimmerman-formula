#!/usr/bin/env python3
"""UX3 read: keys table, Part C shear-to-shear amplitude, checks. kappa = 1/2 FITTED; not theory closed."""
import json, math, os
import numpy as np
from scipy.stats import chi2
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); OUT = []; R = dict(keys={}, C={}); CH = {}
def P(s=""): print(s, flush=True); OUT.append(str(s))
def chk(k, ok, m): CH[k] = bool(ok); P(f"{k} {'PASS' if ok else 'FAIL'}: {m}")
def J(*a): return json.load(open(os.path.join(*a)))
HH = ("h0672", "h0686"); FEET = ("canonical", "alt"); KF = J(HERE, "ux3_kfit.json"); PI2 = math.pi ** 2
def joint(Z, ks, Rm):
    z0 = np.array([Z[k] for k in ks]); w, V = np.linalg.eigh(Rm); ok = w >= 1e-3 * w.max(); z = V[:, ok].T @ z0; c2 = float((z * z / w[ok]).sum()); d = int(ok.sum()); return c2, d, float(chi2.sf(c2, d))
M3 = J(RB, "M3A1_outer_key_audit", "m3a1_results.json")["Ztot"]
K = {t: J(HERE, f"ux3_keys_{t}.json") for t in ("g005_f034", "g005_f0615", "g0_f034", "MUTATE_g005_f034")}; LW = {t: J(RB, "LW1_law_scorecard", f"lw1_keys_{t}.json") for t in ("g005_f034", "g005_f0615")}
d1 = 0.
for t in LW:
    for f in FEET:
        a = K[t][f"R1|c0|{f}|k0.000000"]; b = LW[t][f"R1|c0|{f}"]; d1 = max(d1, max(abs(a["Z"][h][k] - b["Z"][h][k]) for h in HH for k in a["Z"][h]))
chk("K1", d1 <= 1e-9, f"k = 0 vs LW1 per key, both footings, both f*: max |dZ| {d1:.1e}")
def kname(f, k): return f"R1|c0|{f}|k{(KF[f] if k == 'kfit' else k):.6f}"
P("\nKeys. Over-2 keys in either h. Z per h. FITTED rows only; the switch doesn't enter (theta = 1)")
for t, ks, fs in (("g005_f034", [PI2, "kfit", .7 * PI2, 1.3 * PI2, PI2 / 1.7, PI2 * 1.7], "0.034"), ("g005_f0615", [PI2, "kfit"], "0.0615"), ("g0_f034", [PI2, "kfit"], "0.034"), ("MUTATE_g005_f034", [3 * PI2, 3 * KF["canonical"]], "0.034")):
    for f in FEET:
        for k in ks:
            n = kname(f, k); r = K[t][n]; Rr = K[t]["R"][f]; lab = "kfit" if k == "kfit" else f"{k / PI2:.3f}pi2" if t != "MUTATE_g005_f034" else f"{k:.2f}"; cc = {}
            for h in HH:
                rk = Rr[h]["keys"]; a = joint(r["Z"][h], rk, np.array(Rr[h]["R_boot"])); b = joint(r["Z"][h], rk, np.array(Rr[h]["R_jack"])); zm = r["Z"][h]["G-OUT-M3"]; s = r["tmpl"][h]["G-OUT-M3"][1]; q = M3[f"{fs}|{h}"]; tot = float(np.sqrt(s ** 2 + q["slope"] ** 2 + q["m"] ** 2 + q["nz"] ** 2 + q["leak"] ** 2)); w = max(rk, key=lambda x: abs(r["Z"][h][x])); cc[h] = dict(M3=zm, Ztot_nogas=zm * s / tot, worst=[w, r["Z"][h][w]], chi2=a[0], dof=a[1], p=a[2], jack_p=b[2], Z=r["Z"][h])
            R["keys"][f"{t}|{f}|{lab}"] = dict(n=r["n"], bad=r["bad"], cells=cc, groups=r["groups"]); o = cc
            P(f"[{t} {f} {lab} k {float(n.split('|k')[1]):.3f}] {r['n']} of 15; over 2: {', '.join(r['bad'])}"); P("    " + " | ".join(f"{h}: M3 {o[h]['M3']:+.2f}, worst {o[h]['worst'][0]} {o[h]['worst'][1]:+.2f}, chi2 {o[h]['chi2']:.1f}/{o[h]['dof']} p {o[h]['p']:.1e}, jack p {o[h]['jack_p']:.1e}" for h in HH))
            if t == "g005_f034" and k in (PI2, "kfit"): P("    Z h0672: " + ", ".join(f"{x.replace('G-','')} {r['Z']['h0672'][x]:+.2f}" for x in rk))
mv = abs(K["MUTATE_g005_f034"][kname("canonical", 3 * PI2)]["Z"]["h0672"]["G-OUT-M3"] - K["g005_f034"][kname("canonical", PI2)]["Z"]["h0672"]["G-OUT-M3"]); chk("MUT-keys", mv > .5, f"k x 3 moves G-OUT-M3 by {mv:.2f}")
# Part C
X = np.load(os.path.join(RB, "X7_cluster_core_significance", "x7_measure_percluster.npz")); names = [str(x).strip() for x in X["name"]]; N = len(names); D = np.load(os.path.join(HERE, "cache_g005_f034", "dump.npz")); L = np.load(os.path.join(RB, "LM1_law_missing_mass_map", "cache_BASE_f034", "dump.npz")); PATCH = L["PATCH"]; OK = J(HERE, "ux3_okabe.json"); idx = np.array([names.index(n) for n in OK]); Mg0 = np.asarray(X["Mgas500"], float); chk("K-names", list(D["names"]) == names, "grader order = X7 order")
HI = {"h0672": 1, "h0686": 2}; HX = {"h0672": 0, "h0686": 1}; RC = L["RC"]
def nsum(h):
    i = HI[h]; W = np.where(X["E"][:, i] < 1e8, 1 / X["E"][:, i] ** 2, 0); B0 = X["den"][:, i].sum(0) / X["den_r"][:, i].sum(0); return W * B0[None, :] * (X["D"][:, i] - X["leakP"][:, HX[h], 0]), W
dk5 = np.nanmax(np.abs(D["VLAW_canonical_h0672"][idx] - L["V_canonical_h0672"][idx]) / (np.abs(L["V_canonical_h0672"][idx]) + 1e-12)); chk("K5", dk5 <= 1e-3, f"law mass through the Part C path vs LM1's V: max relative |d| {dk5:.1e}; frozen as 1e-9 absolute, see README")
K4 = D["K4"]; chk("K4", abs(np.median(K4) - 1) < 1e-6 and K4.std() < 1e-6, f"grader Mb(R500)/(1+f*) / catalogue gas: median {np.median(K4):.4f}, sd {K4.std():.4f}, range {K4.min():.4f}-{K4.max():.4f}")
BANDS = {"all": range(8), "0.18-0.26": (0, 1), "0.38-0.81": (2, 3, 4), "1.18-2.49": (5, 6, 7)}
def amp(n, W, V, U, bins, ix):
    m = np.zeros((N, 8), bool); m[np.ix_(ix, list(bins))] = True; m &= (W > 0) & np.isfinite(V) & np.isfinite(U); w = np.where(m, 1 / np.where(W > 0, W, 1), 0); return (n * U * w)[m].sum() / (V * U * w)[m].sum()
def boot(n, W, V, U, bins, nb=2000, seed=20261102):
    rg = np.random.default_rng(seed); v = amp(n, W, V, U, bins, idx); w = lambda ix: np.where(np.isin(np.arange(N), ix), 1, 0)
    bb = []
    for _ in range(nb):
        c = np.bincount(rg.integers(0, len(idx), len(idx)), minlength=len(idx)); sel = idx; m = np.zeros((N, 8), bool); m[np.ix_(sel, list(bins))] = True; mm = m & (W > 0) & np.isfinite(V) & np.isfinite(U); cw = np.zeros(N); cw[sel] = c; wt = np.where(mm, 1 / np.where(W > 0, W, 1), 0) * cw[:, None]; bb.append((n * U * wt)[mm].sum() / (V * U * wt)[mm].sum())
    jk = [amp(n, W, V, U, bins, idx[PATCH[idx] != q]) for q in np.unique(PATCH[idx])]; sj = float(np.sqrt((len(jk) - 1) / len(jk) * ((np.array(jk) - np.mean(jk)) ** 2).sum())); return float(v), float(np.std(bb)), sj
for h in HH:
    n, W = nsum(h); R["C"][h] = {}; P(f"\nPart C, {h}, N {len(idx)}. A = KiDS shear / Okabe HSC NFW. Frozen estimator weights by the noisy V; IV weights by the law's V, which holds no Okabe noise")
    for tag in ("raw", "eq17", "trunc", "cat"):
        V = D[f"VOK_{tag}_canonical_{h}"]; U = D[f"VLAW_canonical_{h}"]; Vra = D[f"VOK_{tag}_alt_{h}"]
        if tag == "raw": chk(f"K-footing {h}", np.nanmax(np.abs(V[idx] - Vra[idx]) / (np.abs(V[idx]) + 1e-12)) < .03, f"Okabe V canonical vs alt: max relative {np.nanmax(np.abs(V[idx] - Vra[idx]) / (np.abs(V[idx]) + 1e-12)):.3e}")
        for bn, b in BANDS.items():
            f0 = boot(n, W, V, V, b); iv = boot(n, W, V, U, b); R["C"][h][f"{tag}|{bn}"] = dict(frozen=f0, iv=iv); P(f"  {tag:5s} {bn:10s} frozen A {f0[0]:.3f} +- {f0[1]:.3f} boot, {f0[2]:.3f} jack | IV A {iv[0]:.3f} +- {iv[1]:.3f}, {iv[2]:.3f}")
# noise attenuation, mock
n, W = nsum("h0672"); Vc = D["VOK_cat_canonical_h0672"]; rg = np.random.default_rng(1); s = np.array([OK[x]["s"] / OK[x]["M500"] for x in OK]); att = []
for _ in range(1000):
    Vn = Vc.copy(); Vn[idx] = Vc[idx] * np.maximum(1 + rg.normal(0, s), .05)[:, None]; b = range(8); m = np.zeros((N, 8), bool); m[np.ix_(idx, list(b))] = True; m &= W > 0; w = 1 / np.where(W > 0, W, 1); att.append((Vc * Vn * w)[m].sum() / (Vn * Vn * w)[m].sum())
U0 = D["VLAW_canonical_h0672"]; attiv = []; rg = np.random.default_rng(2)
for _ in range(1000):
    Vn = Vc.copy(); Vn[idx] = Vc[idx] * np.maximum(1 + rg.normal(0, s), .05)[:, None]; m = np.zeros((N, 8), bool); m[np.ix_(idx, range(8))] = True; m &= W > 0; w = 1 / np.where(W > 0, W, 1); attiv.append((Vc * U0 * w)[m].sum() / (Vn * U0 * w)[m].sum())
P(f"Mock, same, IV estimator returns {np.mean(attiv):.3f} (median {np.median(attiv):.3f}) for true A = 1"); R["C"]["atten_iv"] = float(np.mean(attiv))
Vs = D["VOK_raw_canonical_h0672"].copy(); pm = np.random.default_rng(5).permutation(len(idx)); Vs[idx] = Vs[idx][pm]; ms = {b: (amp(n, W, Vs, Vs, BANDS[b], idx), amp(n, W, Vs, U0, BANDS[b], idx)) for b in BANDS}; P("MUTATE Part C, Okabe V shuffled among clusters: " + ", ".join(f"{b} frozen {v[0]:.3f} IV {v[1]:.3f}" for b, v in ms.items())); R["C"]["mutate_shuffle"] = ms; a0_ = amp(n, W, D["VOK_raw_canonical_h0672"], D["VOK_raw_canonical_h0672"], BANDS["all"], idx); chk("MUT-C", abs(ms["all"][0] - a0_) > .1, f"frozen all moves {a0_:.3f} to {ms['all'][0]:.3f}")
R["C"]["atten"] = dict(mean=float(np.mean(att)), s_med=float(np.median(s))); P(f"\nMock, catalogue mass as truth, Okabe's own errors (median {np.median(s):.2f}) on V: frozen estimator returns {np.mean(att):.3f} for true A = 1. ATTENUATED: frozen label is biased low by this")
f0 = R["C"]["h0672"]["raw|all"]["frozen"]; iv = R["C"]["h0672"]["raw|all"]["iv"]
def lab(a, sb): sg = math.hypot(sb, .1); return ("SHEAR GAP" if (1 - a) / sg >= 3 else "NOT A SHEAR GAP" if abs(a - 1) / sg < 2 and sg <= .15 else "UNRESOLVED"), sg
R["C"]["label_frozen"] = lab(f0[0], max(f0[1:])); R["C"]["label_iv"] = lab(iv[0], max(iv[1:])); P(f"Label, frozen estimator: {R['C']['label_frozen']}; post-result IV: {R['C']['label_iv']}")
G = J(RB, "GM1_gas_tied_missing_mass", "gm1_results.json")["ans"]["canonical"]["post"]; G2 = G
ov = G["overlap35"]; ML = ov["M_Mg"] - ov["Okabe"]; a_ = iv[0]; P(f"GM1's 35: HSC dM/Mg {ov['Okabe']:.2f}, KiDS {ov['KiDS']:.2f}, M/Mg {ov['M_Mg']:.2f}, law {ML:.2f}. Scaling HSC mass by IV A: dM/Mg {ov['M_Mg'] * a_ - ML:.2f} +- {ov['M_Mg'] * max(iv[1:]):.2f}. ratio HSC/KiDS on that route {ov['Okabe'] / max(ov['M_Mg'] * a_ - ML, .1):.2f}"); R["C"]["dM_from_A"] = ov["M_Mg"] * a_ - ML
# 35 vs matched in gas, KiDS's own Q
for foot in FEET:
    e = n - L[f"V_{foot}_h0672"]; VNg = L[f"VN_{foot}_h0672"] / 1.034; x = RC[None, :] / L["R500_h0672"][:, None]; oth = np.setdiff1d(np.arange(N), idx); lg = np.log10(Mg0); mt = np.array([oth[np.argsort(np.abs(lg[oth] - lg[i]))[:3]] for i in idx]).ravel()
    for lo, hi in ((.2, .5), (.5, 1.), (1., 2.)):
        m = (x >= lo) & (x < hi); E_ = (e * m).sum(1); V_ = (VNg * m).sum(1); rg = np.random.default_rng(3); fq = lambda ix: E_[ix].sum() / V_[ix].sum(); ba = [fq(rg.choice(idx, len(idx))) for _ in range(2000)]; bb = [fq(rg.choice(mt, len(mt))) for _ in range(2000)]; P(f"  KiDS Q {foot} x {lo}-{hi}: the 35 {fq(idx):.2f} +- {np.std(ba):.2f}; matched others (3 each) {fq(mt):.2f} +- {np.std(bb):.2f}; all {fq(np.arange(N)):.2f}"); R["C"][f"Q|{foot}|{lo}"] = [float(fq(idx)), float(np.std(ba)), float(fq(mt)), float(np.std(bb))]
# post-result: constant multiplier row, and groups/off-sample at x 1
if os.path.exists(os.path.join(HERE, "ux3_keys_POST_const_f034.json")):
    KC = J(HERE, "ux3_keys_POST_const_f034.json"); CA = J(HERE, "ux3_constA.json")
    for f in FEET:
        r = KC[f"R1|c0|{f}|a{CA[f]:.6f}"]; Rr = KC["R"][f]; a = {h: joint(r["Z"][h], Rr[h]["keys"], np.array(Rr[h]["R_boot"])) for h in HH}; P(f"POST constant multiplier {f} H = {CA[f]:.3f} (X-COP train, no gas tie): {r['n']} of 15; over 2: {', '.join(r['bad'])}; M3 {r['Z']['h0672']['G-OUT-M3']:+.2f}, {r['Z']['h0686']['G-OUT-M3']:+.2f}; chi2 {a['h0672'][0]:.1f}, {a['h0686'][0]:.1f}; p {a['h0672'][2]:.1e}, {a['h0686'][2]:.1e}"); R[f"const|{f}"] = dict(n=r["n"], bad=r["bad"], chi2=[a[h][0] for h in HH], p=[a[h][2] for h in HH])
GS = 6.674e-11; MSs = 1.989e30; A0s = dict(canonical=9.3603e-11, alt=1.1312e-10); rhoz = 3 * (70e3 / 3.0857e22) ** 2 * (.3 * 1.1 ** 3 + .7) / (8 * math.pi * GS)
from scipy.optimize import brentq
def Mx1(Mg, k, a0):
    Mb = Mg * 1.034 * MSs
    def M_(r): gb = GS * Mb / r ** 2; lw = .5 * gb + math.sqrt(.25 * gb * gb + a0 * gb); return lw * (1 + k * (gb / 1.034) / a0) * r * r / GS
    r = brentq(lambda r: M_(r) - 4 / 3 * math.pi * r ** 3 * 500 * rhoz, 1e21, 3e23); return M_(r) / MSs
for f in FEET:
    t = " | ".join(f"lg Mg {math.log10(m):.0f}: law {Mx1(m, 0, A0s[f]) / m:.1f}, pi2 {Mx1(m, PI2, A0s[f]) / m:.1f}, kfit {Mx1(m, KF[f], A0s[f]) / m:.1f}" for m in (1e12, 1e13, 1e14, 1e15)); P(f"M/Mg at R500, z 0.1, {f}: {t}"); R[f"Mx1|{f}"] = t
R["checks"] = CH; json.dump(R, open(os.path.join(HERE, "ux3_read.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "ux3_read.out"), "w").write("\n".join(OUT) + "\n"); P(f"\nchecks {sum(CH.values())}/{len(CH)}")
