#!/usr/bin/env python3
"""UX7 read: labels, margins, ranks, gas vs M500, random-shape control, checks. kappa = 1/2 FITTED; not theory closed."""
from ux7_common import *
from ux7_grade import fitrows, scan, checks, ctrl, mut, kf
from scipy.stats import chi2
OUT = []; R = dict(rows={}, rank={}, sep={}, ctrl={}, scan={}, checks={}); HH = ("h0672", "h0686"); FEET = ("canonical", "alt")
def P(s=""): print(s, flush=True); OUT.append(str(s))
def chk(k, ok, m): R["checks"][k] = bool(ok); P(f"{k} {'PASS' if ok else 'FAIL'}: {m}")
def J(*a): return json.load(open(os.path.join(*a)))
K = {t: J(HERE, f"ux7_keys_{t}.json") for t in ("g005_f034", "g005_f0615", "g0_f034", "MUTATE_g005_f034")}; FI = J(HERE, "ux7_fit.json"); FM = J(HERE, "ux7_fit_MUTATE.json"); U3 = J(RB, "UX3_cluster_gas_term", "ux3_keys_g005_f034.json")
def eig(Rm):
    w, V = np.linalg.eigh(np.array(Rm)); ok = w >= 1e-3 * w.max(); return w[ok], V[:, ok]
def joint(Z, ks, Rm):
    w, V = eig(Rm); z = V.T @ np.array([Z[k] for k in ks]); c = float((z * z / w).sum()); return c, len(w), float(chi2.sf(c, len(w)))
def cell(t, f, mutstr):
    r = K[t][f"R1|c0|{f}|{mutstr}"]; Rr = K[t]["R"][f]; o = dict(n=r["n"], bad=r["bad"], Z=r["Z"]); wz = 0
    for h in HH:
        ks = Rr[h]["keys"]; a = joint(r["Z"][h], ks, Rr[h]["R_boot"]); b = joint(r["Z"][h], ks, Rr[h]["R_jack"]); w = max(ks, key=lambda x: abs(r["Z"][h][x])); o[h] = dict(chi2=a[0], dof=a[1], p=a[2], jack=b[2], M3=r["Z"][h]["G-OUT-M3"], worst=w, wz=r["Z"][h][w], T3=r["Z"][h]["G-MID-T3"], OA=r["Z"][h]["G-OUT-all"])
    o["w"] = max(abs(o[h]["wz"]) for h in HH); o["pmin"] = min(o[h]["p"] for h in HH); o["jmin"] = min(o[h]["jack"] for h in HH); return o
def ms(f, x, src="", mult=1.): return f"{x}{src}:{kf(f, x) * mult:.8g}"
P("UX7. Every form FITTED, k on X-COP train only; discs not graded. Primary cell gas +0.005, f* 0.034. Worst |Z| over both h; margin = worst |Z| - 2")
ALL = FORMS + RIV; SRC = lambda x: "L" if x in RIV else ""
for f in FEET:
    P(f"\n=== {f}"); R["rows"][f] = {}
    for x in ALL:
        c = {t: cell(t, f, ms(f, x, SRC(x))) for t in ("g005_f034", "g005_f0615", "g0_f034")}; p = c["g005_f034"]; X = FI[f]["forms"][x]; o = dict(k=X["k"], x=X["xpass"], cells=c); R["rows"][f][x] = o
        P(f"{x:3s} k {X['k']:<8.4g} keys {p['n']:2d} (f* .0615 {c['g005_f0615']['n']}, gas 0 {c['g0_f034']['n']}); worst |Z| {p['w']:.2f} margin {p['w'] - 2:+.2f} [{p['h0672']['worst'].replace('G-', '')}]; M3 {p['h0672']['M3']:+.2f},{p['h0686']['M3']:+.2f}; T3 {p['h0672']['T3']:+.2f}; OUT-all {p['h0672']['OA']:+.2f},{p['h0686']['OA']:+.2f}; chi2 {p['h0672']['chi2']:.1f},{p['h0686']['chi2']:.1f}; p {p['h0672']['p']:.2g},{p['h0686']['p']:.2g}; jack {p['jmin']:.2g}; X-COP {'PASS' if X['xpass'] else 'FAIL'} unseen {X['hold'][0]:+.3f},{X['hold'][1]:.3f} all {X['all'][0]:+.3f},{X['all'][1]:.3f}; over 2: {','.join(s.replace('G-', '') for s in p['bad'])}")
    # rank
    A_ = sorted(ALL, key=lambda x: -R["rows"][f][x]["cells"]["g005_f034"]["pmin"]); B_ = sorted(ALL, key=lambda x: R["rows"][f][x]["cells"]["g005_f034"]["w"]); S_ = sorted(ALL, key=lambda x: (A_.index(x) + B_.index(x), B_.index(x))); R["rank"][f] = S_; P("rank: " + " > ".join(S_))
    # labels
    F0w = R["rows"][f]["F0"]["cells"]["g005_f034"]["w"]
    for x in ALL:
        o = R["rows"][f][x]; p = o["cells"]["g005_f034"]; allc = o["cells"].values()
        if not o["x"]: l = "X-COP FAIL"
        elif all(c["n"] == 15 and c["pmin"] >= .05 and c["jmin"] >= .05 for c in allc): l = "PASS"
        elif 15 - p["n"] <= 1 and p["w"] <= 2.30 and p["pmin"] >= .05: l = "NEAR MISS"
        elif p["w"] <= F0w - .25: l = "IMPROVED"
        else: l = "NO GAIN"
        o["label"] = l
    P("labels: " + ", ".join(f"{x} {R['rows'][f][x]['label']}" for x in ALL))
    for x in RIV: q = cell("g005_f034", f, ms(f, x, "c")); R["rows"][f][x + "c"] = q; P(f"{x}c catalogue M500, report, NOT independent: keys {q['n']}; worst {q['w']:.2f}; M3 {q['h0672']['M3']:+.2f}; OUT-all {q['h0672']['OA']:+.2f}; chi2 {q['h0672']['chi2']:.1f}, p {q['pmin']:.2g}; over 2 {','.join(q['bad'])}")
    # scan
    for x in ALL:
        s = {m: cell("g005_f034", f, ms(f, x, SRC(x), m)) for m in (.7, .85, 1.15, 1.3)}; s[1.] = R["rows"][f][x]["cells"]["g005_f034"]; b = min(s, key=lambda m: s[m]["w"]); R["scan"][f"{f}|{x}"] = {str(m): dict(n=s[m]["n"], w=s[m]["w"], p=s[m]["pmin"]) for m in s}; P(f"  scan {x}: " + " ".join(f"x{m}: {s[m]['n']}/{s[m]['w']:.2f}" for m in (.7, .85, 1., 1.15, 1.3)) + f"; best worst |Z| {s[b]['w']:.2f} at x{b}; any 15: {any(s[m]['n'] == 15 for m in s)}")
    # control
    Cr = []
    for i, (p_, q_, t_) in enumerate(controls()):
        c = cell("g005_f034", f, f"P:{p_:.5f}:{q_:.5f}:{t_:.5f}:{FI[f]['ctrl'][i]['k']:.8g}"); Cr.append(dict(pqt=(p_, q_, t_), n=c["n"], w=c["w"], p=c["pmin"], x=FI[f]["ctrl"][i]["xpass"], hm=FI[f]["ctrl"][i]["hold_margin"], am=FI[f]["ctrl"][i]["all_margin"]))
    listed = [x for x in FORMS if R["rows"][f][x]["x"]]; bw = min(R["rows"][f][x]["cells"]["g005_f034"]["w"] for x in listed); bx = min(listed, key=lambda x: R["rows"][f][x]["cells"]["g005_f034"]["w"]); bp = R["rows"][f][bx]["cells"]["g005_f034"]["pmin"]; nx = sum(c["x"] and c["w"] <= bw for c in Cr); nf = sum(c["w"] <= bw for c in Cr); nn = sum(c["x"] and c["w"] <= bw and c["p"] >= bp for c in Cr); R["ctrl"][f] = dict(best=bx, bw=bw, bp=bp, frac_x=nx / 40, frac_any=nf / 40, frac_xp=nn / 40, rows=Cr, x_pass=sum(c["x"] for c in Cr), w_sorted=sorted(c["w"] for c in Cr), n15=sum(c["n"] == 15 for c in Cr), n15x=sum(c["n"] == 15 and c["x"] for c in Cr), n14=sum(c["n"] >= 14 for c in Cr))
    P(f"control, 40 random shapes: X-COP pass {R['ctrl'][f]['x_pass']}; best listed X-COP-passing form {bx}, worst |Z| {bw:.2f}, p {bp:.2g}. Draws passing X-COP at or under that worst |Z|: {nx}/40 = {nx / 40:.3f}; ignoring X-COP {nf}/40 = {nf / 40:.3f}; X-COP and worst and p {nn}/40. Draws with 15 keys {R['ctrl'][f]['n15']} (with X-COP {R['ctrl'][f]['n15x']}), >=14 keys {R['ctrl'][f]['n14']}. Control worst |Z| 5/50/95 % {np.percentile(R['ctrl'][f]['w_sorted'], [5, 50, 95]).round(2).tolist()}; {'NOT EARNED over arbitrary shape' if nx / 40 >= .1 else 'fraction under 0.10'}")
    srt = sorted(Cr, key=lambda c: c["w"])[:5]; P("  lowest control draws: " + "; ".join(f"p {c['pqt'][0]:.2f} q {c['pqt'][1]:.2f} t {c['pqt'][2]:.2f}: {c['n']} keys, |Z| {c['w']:.2f}, joint {c['p']:.2g}, X-COP {'pass' if c['x'] else 'fail'} (margins {c['hm']:+.3f},{c['am']:+.3f})" for c in srt))
# separation
P("\nGas vs M500. Dchi2 = chi2(M500) - chi2(gas); sd = 2 sqrt(d'R^-1 d), predictions fixed; F = forecast separation")
for a, b in (("R1", "F0"), ("R2", "F5"), ("R1", "F1"), ("R2", "F7")):
    frozen = (a, b) in (("R1", "F0"), ("R2", "F5")); rows = {}
    for f in FEET:
        for h in HH:
            Za = K["g005_f034"][f"R1|c0|{f}|{ms(f, a, 'L')}"]["Z"][h]; Zb = K["g005_f034"][f"R1|c0|{f}|{ms(f, b)}"]["Z"][h]; Rr = K["g005_f034"]["R"][f][h]; ks = Rr["keys"]; w, V = eig(Rr["R_boot"]); d = np.array([Za[k] - Zb[k] for k in ks]); dd = float((((V.T @ d) ** 2) / w).sum()); ca = joint(Za, ks, Rr["R_boot"])[0]; cb = joint(Zb, ks, Rr["R_boot"])[0]; D = ca - cb; sd = 2 * math.sqrt(dd); Fc = math.sqrt(dd) / 2; rows[f"{f}|{h}"] = dict(D=D, sd=sd, F=Fc, sig=D / sd if sd else 0.); P(f"  {a} vs {b} {f} {h}: Dchi2 {D:+.1f} +- {sd:.1f} ({D / sd:+.2f} sigma); F {Fc:.2f}")
    if any(r["F"] < 3 for r in rows.values()): l = "NOT SEPARABLE"
    elif all(abs(r["sig"]) >= 3 for r in rows.values()) and len({r["D"] > 0 for r in rows.values()}) == 1: l = "GAS BETTER" if rows["canonical|h0672"]["D"] > 0 else "M500 BETTER"
    else: l = "NOT SEPARATED"
    R["sep"][f"{a}|{b}"] = dict(rows=rows, label=l, frozen=frozen); P(f"  {a} vs {b}: {l}{'' if frozen else ' (post-result pair, no label protection)'}")
# checks
P(""); G = K["g005_f034"]; d = 0.
for f, k in (("canonical", 13.286788), ("alt", 14.250573)):
    a = G[f"R1|c0|{f}|F0:{k:.8g}"]["Z"]; b = U3[f"R1|c0|{f}|k{k:.6f}"]["Z"]; d = max(d, max(abs(a[h][q] - b[h][q]) for h in HH for q in a[h]))
chk("K1", d <= 1e-9, f"F0 at UX3's k vs UX3 keys per key: max |dZ| {d:.1e}"); chk("K2", max(abs(FI[f]["forms"]["F0"]["k"] - J(RB, "UX3_cluster_gas_term", "ux3_kfit.json")[f]) for f in FEET) <= 1e-5, "F0 fit vs ux3_kfit")
L0 = U3["R1|c0|canonical|k0.000000"]["Z"]; d = max(abs(G[f"R1|c0|canonical|{x}:0"]["Z"][h][q] - L0[h][q]) for x in FORMS + ["R1L", "R2L"] for h in HH for q in L0[h]); chk("K3", d <= 1e-9, f"every form at k 0 vs law: max |dZ| {d:.1e}")
a = G["R1|c0|canonical|F3:10"]["Z"]; b = G["R1|c0|canonical|F0:10.34"]["Z"]; d = max(abs(a[h][q] - b[h][q]) for h in HH for q in a[h]); chk("K4", d <= 1e-9, f"F3 k vs F0 k(1+f*): max |dZ| {d:.1e}")
a = G["R1|c0|canonical|R1G:10"]["Z"]["h0672"]; b = G["R1|c0|canonical|F0:10"]["Z"]["h0672"]; d = max(abs(a[q] - b[q]) for q in a); chk("K5", d <= .02, f"R1 with M500 = gas vs F0, h 0.672: max |dZ| {d:.3f}")
Mm = J(HERE, "ux7_mass.json"); chk("K6", abs(Mm["K6"]) <= .15, f"median lg(M_L/M_HSE) on X-COP in eRASS1 {Mm['K6']:+.3f}"); chk("K7", Mm["N"] >= 30, f"calibration N {Mm['N']}")
M_ = K["MUTATE_g005_f034"]; mx = all(not FM[f]["forms"][x]["xpass"] for f in FEET for x in ALL); chk("MUT-X", mx, "k x 3: every form fails X-COP")
for f in FEET:
    for x in RIV:
        a = M_[f"R1|c0|{f}|{x}S:{kf(f, x):.8g}"]["Z"]["h0672"]; b = G[f"R1|c0|{f}|{ms(f, x, 'L')}"]["Z"]["h0672"]; d = max(abs(a[q] - b[q]) for q in a); P(f"MUT M_L shuffled {x} {f}: keys {M_[f'R1|c0|{f}|{x}S:{kf(f, x):.8g}']['n']} vs {G[f'R1|c0|{f}|{ms(f, x, chr(76))}']['n']}; max |dZ| {d:.2f}; G-OUT-M3 {a['G-OUT-M3']:+.2f} vs {b['G-OUT-M3']:+.2f}"); R["checks"][f"MUT-S {x} {f}"] = bool(d > .3)
P("MUT k x 3 keys: " + "; ".join(f"{f} {x} {M_[f'R1|c0|{f}|{x}{SRC(x)}:{3 * kf(f, x):.8g}']['n']}" for f in FEET for x in ALL))
P(f"\nchecks {sum(R['checks'].values())}/{len(R['checks'])}; failed: {[k for k, v in R['checks'].items() if not v]}")
json.dump(R, open(os.path.join(HERE, "ux7_read.json"), "w"), indent=0, default=float); open(os.path.join(HERE, "ux7_read.out"), "w").write("\n".join(OUT) + "\n")
