#!/usr/bin/env python3
"""CP1 on BL1's blue lenses: S2's forward model and BL1's profile E, read only. Halo = N (no floor, NR2's eta). V = (G M_b a0)^(1/4), stipulated: KiDS has no V_flat. V_crit 250, n 4 CHOSEN; chi at z = 0 as the rule states. kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json
CH = os.path.dirname(os.path.abspath(__file__)); RB_ = os.path.dirname(CH); BD = os.path.join(RB_, "BL1_blue_lens_halo_mass"); src = open(os.path.join(BD, "bl1_blue.py")).read(); cut = "for foot in FOOTS:\n    F = {}\n"; assert src.count(cut) == 1
sys.argv = [os.path.join(BD, "bl1_blue.py")]; __file__ = os.path.join(BD, "bl1_blue.py"); exec(compile(src[:src.index(cut)], "bl1_head", "exec"))
X39 = open(os.path.join(REB, "X39_baryonic_contraction", "x39_contraction.py")).read(); SGN = 1; exec(X39[X39.index("def contract(r, Mb, M0, F, gnedin=None):"):X39.index('P("\\n=== checks")')])
meff = N["meff"]; NR = json.load(open(os.path.join(REB, "NR2_low_mass_ng80", "nr2_results.json"))); ELM, EV = [10, 11, 12, 13, 14], [21.531 * NR["r10"], 21.531 * NR["r11"], 21.531, 23.536, 22.097]
def eta_n(M): return float(np.interp(math.log10(M), ELM, EV))
def halo_n(foot, Ms, Mc, Mb_tot):
    M200 = 10 ** (BA + BB * (math.log10(Ms + Mc) - 10)); R200 = (3 * M200 / (4 * math.pi * 200 * 2.775e11 * HB ** 2 / 1e18)) ** (1 / 3); Mt = M200 / FC; S = FC * eta_n(Mt) * sigma_coll(Mt); r0 = solve_r0(M200, R200, S); rta = (3 * (M200 + Mb_tot) / (4 * math.pi * DTA * RHOM0)) ** (1 / 3) / (1 + ZT)
    return math.pi * S * r0 ** 2 * B(np.minimum(RG, max(rta, R200)) / r0)
MIX = dict(Vc=250.0, n=4.0, cont=True, mut=False); T2 = {}; CHIS = {}
def table(foot, h, yk, fhot, dcold, dMs):
    key = (foot, h, yk, fhot, dcold, round(dMs, 8), MIX["Vc"], MIX["cont"], MIX["mut"])
    if key in T2: return T2[key]
    tab = np.empty((len(LMG), len(LRT))); R_ = np.exp(LRT) * 1e6
    for gi, lm in enumerate(LMG):
        lm70 = lm - 2 * math.log10(0.70 / h); Ms = 10 ** (lm + dMs); Mc = 10 ** (lm + (-0.69 * lm70 + 6.63) + dcold); Mh_ = fhot * 10 ** lm; V = (Gpc * (Ms + Mc) * a0u(foot)) ** 0.25; xp = math.exp(-(V / MIX["Vc"]) ** MIX["n"]); xc = 1 - xp; CHIS[(foot, lm)] = (V, xp)
        ML, tl = meff(foot, Ms, Mc, Mh_, yk); ds = xp * AQ.delta_sigma(R_, RG, ML, tl)
        if xc > 1e-9 or MIX["mut"]:
            Mb = Ms + Mc + Mh_ * np.minimum(1.0, (RG / 1e5) ** 3); M0 = halo_n(foot, Ms, Mc, Ms + Mc + Mh_); w = 1.0 if MIX["mut"] else xc
            Mf = contract(RG, Mb, w * M0, (Ms + Mc + Mh_) / (w * M0[-1]))[0] if MIX["cont"] else w * M0
            ds = ds + AQ.delta_sigma(R_, RG, (1.0 if MIX["mut"] else xc) * Mb + Mf, "const")
        tab[gi] = np.log(ds)
    T2[key] = tab; return tab
out = dict(K1_S2_L4=d, rows={}); 
STATE.update(mode="E", prof="E", dlm=0.0); a = cell("canonical", "blue", CFG); K6 = abs(a["A"] - 1.053) <= 0.0006; P(f"K6 BL1's route E blue A reproduced with its own table: {a['A']:.4f}: {'PASS' if K6 else 'FAIL'}")
N["table"] = table; ok = (d <= 1e-6) and K6
for nm, v in (("law_limit", dict(Vc=1e7, cont=True, mut=False)), ("primary", dict(Vc=250.0, cont=True, mut=False)), ("no_contraction", dict(Vc=250.0, cont=False, mut=False)), ("MUTATE", dict(Vc=250.0, cont=True, mut=True))):
    MIX.update(v); out["rows"][nm] = {}
    for foot in FOOTS:
        for k in N["CLS"]:
            c = cell(foot, k, CFG); out["rows"][nm].setdefault(foot, {})[k] = dict(A=c["A"], sA=c["sA"], cls=c["cls"], chi2=c["chi2_15_A1"]); P(f"{nm} [{foot} {k}]: A {c['A']:.3f} +- {c['sA']:.3f} [{c['cls']}], chi2(15) {c['chi2_15_A1']:.1f}")
k5 = 0.0
for foot in FOOTS:
    for k in N["CLS"]:
        L = RES["k"]["law"][foot][k]; R = out["rows"]["law_limit"][foot][k]; k5 = max(k5, abs(L["A"] - R["A"]), abs(L["chi2"] - R["chi2"]))
ok &= k5 <= 1e-6; P(f"K5 law limit against S2's L4 A, chi2: max |d| {k5:.1e}: {'PASS' if k5 <= 1e-6 else 'FAIL'}"); out["K5"] = k5; out["K6"] = bool(K6); out["ok"] = bool(ok)
out["chi_by_lm"] = {f"{lm:.1f}": dict(V=CHIS[("canonical", round(lm, 3))][0], chi_pol=CHIS[("canonical", round(lm, 3))][1]) for lm in (9.5, 10.0, 10.5, 10.8, 11.0, 11.5)}; P(str(out["chi_by_lm"]))
g = {f: dict(chi2=out["rows"]["primary"][f]["blue"]["chi2"] <= 35, cls=out["rows"]["primary"][f]["blue"]["cls"]) for f in FOOTS}; out["grade"] = g; P(f"blue grade: {g}")
json.dump(out, open(os.path.join(CH, "cp1_bl1_results.json"), "w"), indent=1, default=float); open(os.path.join(CH, "cp1_bl1.out"), "w").write("\n".join(map(str, OUT)) + "\n"); sys.exit(0 if ok else 1)
