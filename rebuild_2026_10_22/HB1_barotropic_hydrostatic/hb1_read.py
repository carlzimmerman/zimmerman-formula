#!/usr/bin/env python3
"""HB1 read: checks, Argon's score, gates, universal fluid, physical consistency. Reads this lane's JSON and NR3 MEDIAN's. Rerun gives identical output. kappa = 1/2 FITTED, unused; no a0; not theory closed."""
import json, math, os, sys
import numpy as np
H_ = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(H_); sys.path.insert(0, H_); sys.dont_write_bytecode = True; import hb1_core as H
OUT = []; TG = ("A_c2b_refit", "B_cfg886_bg"); ok = True; RES = {}
def P(s=""): print(s, flush=True); OUT.append(s)
def L(p): return json.load(open(os.path.join(H_, f"hb1_{p}_results.json")))
M = L("MAIN"); G5 = L("G5"); MU = L("MUTATE"); K3 = L("K3"); A215 = L("A215"); N3 = json.load(open(os.path.join(RB, "NR3_ur1_on_nr2", "nr3_MEDIAN_results.json"))); ZN = json.load(open(os.path.join(H_, "hb1_zn4_results.json"))); T = json.load(open(os.path.join(H_, "hb1_test.json"))); R = M["runs"]; S = M["setup"]
def chk(n, v, line):
    global ok
    p = v <= line; ok &= p; RES[n] = v; P(f"{n}: {v:.2e} (line {line:g}) {'PASS' if p else 'FAIL'}")
def spd(a, b): return max(max(abs(a["sparc"][t][k] - b["sparc"][t][k]) for k in ("U", "rms", "tilt")) for t in TG)
def prd(a, b): return max(abs(a["keys"]["preds"][h][k] - b["keys"]["preds"][h][k]) for h in a["keys"]["preds"] for k in a["keys"]["preds"][h])
P("HB1 read; kappa = 1/2 FITTED, unused; no a0 in the cold sector; not theory closed")
P("\n=== checks"); P(f"solver tests hb1_test.py: {'ALL PASS' if T['ok'] else 'FAIL'}"); ok &= T["ok"]
for n in ("EM1|off", "EM1|blum"): chk(f"K1 {n} vs NR3 MEDIAN, SPARC", spd(R[n], N3["runs"][n]), 1e-6); chk(f"K1 {n} vs NR3 MEDIAN, key preds", prd(R[n], N3["runs"][n]), 1e-6)
chk("K2 whole row, M_b x 0 vs EM1|off", spd(R["NULL_Mbx0"], R["EM1|off"]), 1e-4); chk("K2 null sample in the path, FormB_E1", M["stats"]["FormB_E1"]["null_sample_max"], 1e-4)
chk("K3 substeps x 2, Form B", spd(K3["runs"]["K3_nsub4_B"], R["FormB_E1"]), 1e-3); chk("K3 substeps x 2, Form A", spd(K3["runs"]["K3_nsub4_A"], R["FormA"]), 1e-3)
dm = abs(MU["runs"]["MUTATE_Phib_x2_B"]["sparc"][TG[0]]["U"] - R["FormB_E1"]["sparc"][TG[0]]["U"]); dmr = abs(MU["runs"]["MUTATE_Phib_x2_B"]["sparc"][TG[0]]["rms"] - R["FormB_E1"]["sparc"][TG[0]]["rms"]); P(f"MUTATE Phi_b x 2, Form B: |dU| {dm:.3f}, |drms| {dmr:.3f}, U {MU['runs']['MUTATE_Phib_x2_B']['sparc'][TG[0]]['U']:.2f} (frozen line |dU| >= 0.02): {'PASS' if dm >= 0.02 else 'FAIL'}"); RES["MUTATE_dU"] = dm; RES["MUTATE_drms"] = dmr; mut_ok = dm >= 0.02; ok &= mut_ok
gp = max(abs(G5["runs"]["EM1|off"]["keys"]["preds"][h][k] / R["EM1|off"]["keys"]["preds"][h][k] - 1) for h in R["EM1|off"]["keys"]["preds"] for k in R["EM1|off"]["keys"]["preds"][h]); P(f"gas patch bites: G5 EM1|off preds differ from MAIN by up to {gp:.4f}: {'PASS' if gp > 1e-4 else 'FAIL'}"); ok &= gp > 1e-4; RES["gas_patch"] = gp
P(f"ZN4 base: {'PASS' if ZN['ok'] else 'FAIL'}"); ok &= ZN["ok"]
for n, s in M["stats"].items():
    if s["calls"]: P(f"stats {n}: calls {s['calls']}, no root {s['noroot']} ({100 * s['noroot'] / s['calls']:.2f} %), wall {s['wall']}, H_c 5/50/95 {np.round(s['Hc_pct'], 2).tolist()}, a 5/50/95 {np.round(s['xe_pct'], 1).tolist()}, roots {s['roots_hist']}")
def row(n, r, g=None):
    a, b = r["sparc"][TG[0]], r["sparc"][TG[1]]; P(f"{n}: U {a['U']:.2f}/{b['U']:.2f} rms {a['rms']:.4f}/{b['rms']:.4f} tilt {a['tilt']:+.2f}/{b['tilt']:+.2f} bins A {[round(v, 2) for v in a['bins'].values()]} bins B {[round(v, 2) for v in b['bins'].values()]} groups {r['groups']['Z']:+.2f} LT {r['lt'][TG[0]]:+.3f}/{r['lt'][TG[1]]:+.3f}; keys (NR3 gas) {r['keys']['n']} {r['keys']['bad']} X-COP {r['xcop']['mean']:+.3f}, {r['xcop']['rms']:.3f}")
P("\n=== rows, MEDIAN, delta 0, canonical, f* 0.034")
for n, r in R.items(): row(n, r)
row("FormA_215 (A3, sensitivity)", A215["runs"]["FormA_215"])
P("\n=== Argon's prediction, Form A, background A")
pr = dict(U=(0.58, 0.05), tilt=(0.38, 0.08)); bn = [0.95, 0.92, 0.74, 0.44, 0.50, 0.66]; BN = ["20-60", "60-100", "100-150", "150-200", "200-250", "250-400"]
def score(r, lab):
    s = r["sparc"][TG[0]]; it = [("global U", s["U"], 0.58, 0.05), ("tilt", s["tilt"], 0.38, 0.08)] + [(f"U {k}", s["bins"][k], v, 0.08) for k, v in zip(BN, bn)]; o = {}; 
    for n, v, c, e in it: h = abs(v - c) <= e + 1e-12; o[n] = dict(value=v, predicted=c, tol=e, label="HOLDS" if h else "MISSES"); P(f"  {lab} {n}: {v:+.3f}, predicted {c:+.2f} +/- {e:.2f}: {'ARGON PREDICTION HOLDS' if h else 'MISSES'}")
    w = abs(s["tilt"]) <= 0.15 and s["bins"]["150-200"] >= 0.50; P(f"  {lab} withdrawal condition: {'FIRES' if w else 'DOES NOT FIRE'}"); o["withdrawal"] = bool(w); return o
RES["argon_FormA"] = score(R["FormA"], "Form A"); P("Reported, not scored as its prediction:"); RES["argon_FormB"] = score(R["FormB_E1"], "Form B E1"); RES["argon_A2"] = score(R["FormA_Prho"], "Form A P/rho reading"); RES["argon_A215"] = score(A215["runs"]["FormA_215"], "Form A 2.15 coefficient")
P("\n=== clusters, gas +0.005, S-core, edge r_ta, BCG as NR3, f* 0.034")
for n, r in G5["runs"].items():
    z = r["keys"]["Z"]; P(f"{n}: {r['keys']['n']} of 15 {r['keys']['bad']}; G-IN-Mall {z['h0672']['G-IN-Mall']:+.2f} G-OUT-M3 {z['h0672']['G-OUT-M3']:+.2f}/{z['h0686']['G-OUT-M3']:+.2f}; X-COP {r['xcop']['mean']:+.3f}, {r['xcop']['rms']:.3f} {'PASS' if r['xcop']['PASS'] else 'FAIL'}")
P("\n=== against ZN4, native shape, Form B numeric, gas +0.005")
for n, r in ZN["rows"].items(): P(f"{n}: {r['n']} of 15 {r['bad']}; X-COP {r['xcop']['mean']:+.3f}, {r['xcop']['rms']:.3f}; G-OUT-M3 {r['Z']['h0672']['G-OUT-M3']:+.2f}/{r['Z']['h0686']['G-OUT-M3']:+.2f}; stat {r['stat']}")
P("\n=== gates and labels")
def gate(r, rg):
    s = r["sparc"]; g = dict(line=all(s[t]["line"] for t in TG), tilt=all(abs(s[t]["tilt"]) <= 0.15 for t in TG), keys=rg["keys"]["n"] == 15, xcop=rg["xcop"]["PASS"], groups=abs(r["groups"]["Z"]) <= 2, lt=all(abs(r["lt"][t]) <= 0.10 for t in TG)); u = s[TG[0]]["U"], s[TG[1]]["U"]
    if all(g.values()): l = "CLEARS"
    elif g["line"]: l = "SPARC LINE, GATES FAIL"
    elif abs(u[0] - 0.35) >= 0.02 - 1e-9 or abs(u[1] - 0.36) >= 0.02 - 1e-9: l = "MOVES, FAILS"
    else: l = "NO MOVE"
    return g, l
for n, k in (("Form B E1 (PRIMARY)", "FormB_E1"), ("Form A", "FormA")): g, l = gate(R[k], G5["runs"][k]); RES[f"gate_{k}"] = dict(g, label=l); P(f"{n}: {l}; fails {[a for a, b in g.items() if not b]}")
def hi(k): s = R[k]["sparc"][TG[0]]["bins"]; return s["150-200"], s["200-250"]
def spread(ks): return max(max(hi(k)[i] for k in ks) - min(hi(k)[i] for k in ks) for i in (0, 1))
de = spread(("FormB_E1", "FormB_E2", "FormB_E3")); db = spread(("FormB_E1", "FormB_E1_low", "FormB_E1_high")); RES["eos_spread"] = de; RES["branch_spread"] = db; P(f"U at 150-250, E1/E2/E3 spread {de:.3f}: {'[EOS-ABOVE-CENTRE DEPENDENT]' if de > 0.05 else 'not EOS-dependent by the line'}"); P(f"U at 150-250, nearest/lowest/highest spread {db:.3f}: {'[BRANCH-DEPENDENT]' if db > 0.05 else 'not branch-dependent by the line'}. Other columns can differ: see rows")
clr = gate(R["FormB_E1"], G5["runs"]["FormB_E1"])[0]; P(f"Form B E1 clears Upsilon and tilt: {'yes' if clr['line'] and clr['tilt'] else 'no'}; LOW/HIGH/independent grid required only if yes")
P("\n=== effective f = (Q - 1)/(Q_Blum - 1) at r0, 2, 3, 4 R_d, Upsilon 0.5, A; NR4 asks about 0-0.2 at 150-250 km/s")
for lab, e in list(M["eff"].items()) + [("FormA_215", A215["eff"]["FormA_215"])]:
    P(lab + ": " + "; ".join(f"{b} f {np.round(v['f'], 2).tolist()} Q {np.round(v['Qh'], 2).tolist()}" for b, v in e.items()))
P("\n=== continuation in Phi_b, sample of SPARC, 21 steps, Form B E1")
C = M["continuation"]; st = np.array([c["step"] for c in C]); nr = np.array([c["nroots"] for c in C]); P(f"n {len(C)}; largest step in ln H_c: median {np.median(st):.3f}, max {st.max():.3f}; with a step > 0.3 (branch not continuous) {int((st > 0.3).sum())}; roots at full Phi_b: {dict(zip(*[x.tolist() for x in np.unique(nr, return_counts=True)]))}; H_c < 1 in {sum(c['Hc'] < 1 for c in C)}"); RES["continuation"] = dict(n=len(C), discontinuous=int((st > 0.3).sum()), maxstep=float(st.max()))
ms = [k for k in S if k[0].isdigit()]; bs = lambda x: float(H.BS(np.asarray(float(x))))
P("\n=== N's halos at Phi_b = 0: Form A against the core, stability"); RES["halos"] = {}
for k in ms:
    s = S[k]; a = s["a"]; q = 1 - math.asinh(a) / a; g = np.geomspace(1e-3, a, 1200); mt = bs(a); E = H.eos("A", q); o, Hc, st_, _, Ho = H.solve_scaled(g, 0 * g, a, mt, E); i1 = np.interp(0.0, np.log(g), o); i3 = np.interp(math.log(3), np.log(g), o); rs = math.pi * math.sqrt(q); Eb = H.eos("E1"); d = (H.mass_at(g, 0 * g, a, 1.002, Eb) - H.mass_at(g, 0 * g, a, 0.998, Eb)) / 0.004 / mt; Hs = np.geomspace(.02, 50, 500); f = np.array([H.mass_at(g, 0 * g, a, h, Eb) / mt - 1 for h in Hs]); rt = Hs[:-1][f[1:] * f[:-1] < 0]; rat = q / (math.asinh(1) - math.sqrt(.5))
    RES["halos"][k] = dict(a=a, q=q, sinc_over_r0=rs, sinc_over_R200=rs / a, M_r0_ratio=i1 / bs(1), M_3r0_ratio=i3 / bs(3), rho_c_ratio=Hc / q, bare_M_ratio=4 * math.pi * q ** 1.5 / mt, coef=rat, dmdHc=d, roots=rt.tolist()); P(f"1e{k}: a {a:.1f} q {q:.3f}; c_s0^2 = {rat:.2f} G M(r0)/r0; sinc radius {rs:.2f} r0 = {rs / a:.2f} R200; mass held: M(<r0) x {i1 / bs(1):.2f}, M(<3 r0) x {i3 / bs(3):.2f}, central rho x {Hc / q:.2f}; bare K unheld returns M/M_edge {4 * math.pi * q ** 1.5 / mt:.2f}; Form B dm/dH_c at null {d:+.3f}, roots {np.round(rt, 2).tolist()}")
P("\n=== universal fluid"); rho = {k: S[k]["rho_c_kg_m3"] for k in ms}; A = {k: S[k]["A_kms2"] for k in ms}; xg = np.geomspace(1e-2, 1e3, 3000)
def cs2(k):
    r = rho[k] * (1 + xg * xg) ** -1.5; dh = A[k] * (xg / np.sqrt(1 + xg * xg) - np.arcsinh(xg)) / xg ** 2; dr = -3 * xg * rho[k] * (1 + xg * xg) ** -2.5; return r, r * dh / dr
cu = {k: cs2(k) for k in ms}; lo = max(cu[k][0].min() for k in ms); hi_ = min(cu[k][0].max() for k in ms); lg = np.linspace(math.log10(lo), math.log10(hi_), 40); tb = np.array([np.interp(lg, np.log10(cu[k][0][::-1]), np.log10(cu[k][1][::-1])) for k in ms]); sp = tb.max(0) - tb.min(0); P(f"rho_c by mass (kg/m^3): {[f'{rho[k]:.2e}' for k in ms]}; A (km/s)^2 {[f'{A[k]:.2e}' for k in ms]}"); P(f"overlap of densities {lo:.1e} to {hi_:.1e}; spread of c_s^2(rho) between masses, dex: min {sp.min():.2f}, median {np.median(sp):.2f}, max {sp.max():.2f}")
dirr = {}
for k in ms:
    if k == "12": continue
    s = S[k]; a = s["a"]; rr = rho["12"] / rho[k]; aa = A[k] / A["12"]; top = 1 / aa; nt = 200001; dh = top / (nt - 1); Hg = np.arange(nt) * dh; tab = rr * np.interp(Hg * aa, np.arange(H.NT) * H.DH, H.TAB_B); E = (nt, dh, tab, top, rr, 9 * rr * aa, 1, 0.0, top); g = np.geomspace(1e-3, a, 1200); o, Hc, st_, _, _ = H.solve_scaled(g, 0 * g, a, bs(a), E); dirr[k] = None if st_ == 1 else float(np.interp(0.0, np.log(g), o) / bs(1)); P(f"1e12's EOS on 1e{k}, Phi_b = 0, mass held: M(<r0)/core {dirr[k]}")
uni = sp.max() <= 0.1 and all(v is not None and 0.9 <= v <= 1.1 for v in dirr.values()); P(f"LABEL: {'ONE P(rho) ALLOWED' if uni else 'NO UNIVERSAL P(rho)'}"); RES["universal"] = dict(label="ONE" if uni else "NO UNIVERSAL", spread_max=float(sp.max()), direct=dirr); r0s = [S[k]["r0_kpc"] for k in ms]; P(f"one K means one radius at every mass; r0 runs {min(r0s):.1f} to {max(r0s):.1f} kpc, x {max(r0s) / min(r0s):.0f}")
P("\n=== physical consistency"); kpc = 3.0857e19; rc = S["rho_crit_kg_m3"]; OM = S["OM"]; RES["cs"] = {}
xs = np.geomspace(1e-3, 1e4, 200000); Hx = np.arcsinh(xs) / xs; Rx = (1 + xs * xs) ** -1.5; dPdx = Rx * (xs / np.sqrt(1 + xs * xs) - np.arcsinh(xs)) / xs ** 2; Pp = np.cumsum((-dPdx)[::-1] * np.gradient(xs)[::-1])[::-1]; c2x = Rx * ((xs / np.sqrt(1 + xs * xs) - np.arcsinh(xs)) / xs ** 2) / (-3 * xs * (1 + xs * xs) ** -2.5); Gam = c2x * Rx / Pp; j = xs < 3e3; P(f"Form B local Gamma along the core: centre {Gam[10]:.2f}, x 1 {np.interp(1, xs, Gam):.2f}, x 10 {np.interp(10, xs, Gam):.2f}, x 100 {np.interp(100, xs, Gam):.2f}; min {Gam[j].min():.2f}; below 4/3 for x > {xs[j][np.argmax(Gam[j] < 4 / 3)] if (Gam[j] < 4 / 3).any() else 'none'}")
for k in ms:
    a = S[k]["a"]; q = 1 - math.asinh(a) / a; A_ = A[k]; B0 = math.sqrt(A_ / 9); A0 = math.sqrt(A_ * q); xz = lambda z: (rho[k] / (OM * rc * (1 + z) ** 3)) ** (1 / 3); cz = lambda z: math.sqrt(A_ * float(np.interp(xz(z), xs, c2x))); mu = 1 / (S[k]["r0_kpc"] * math.sqrt(q) / 1e3); RES["cs"][k] = dict(B_centre=B0, A_centre=A0, B_z0=cz(0), B_z3=cz(3), mu_per_Mpc=mu); P(f"1e{k}: c_s centre B {B0:.0f}, A {A0:.0f} km/s; Form B at mean density z 0 {cz(0):.0f}, z 3 {cz(3):.0f} km/s (X22 <= 6 at z 3); Form A mu {mu:.0f} /Mpc (BOLTZ1 floors 56.6, 2.04e4, 1.24e8)")
V = "NOT DECIDED (a check failed)" if not ok else "see labels"; P(f"\nCHECKS: {'ALL PASS' if ok else 'A CHECK FAILED: NO VERDICT'}"); RES["checks_ok"] = bool(ok)
RES["zn4"] = ZN["rows"]
json.dump(RES, open(os.path.join(H_, "hb1_results.json"), "w"), indent=1, default=float); open(os.path.join(H_, "hb1.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
