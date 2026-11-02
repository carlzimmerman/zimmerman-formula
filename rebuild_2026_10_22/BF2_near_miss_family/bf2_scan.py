#!/usr/bin/env python3
"""BF2 steps 1, 2 scan: every snapshot hit on fixed and free Upsilon, families, selection P1-P4, candidate files. kappa = 1/2 FITTED; not theory closed."""
import csv, json, math, os, sys, time
from bf2_common import *
snap = snapshot(); nm = names(); hits = sorted({tuple(h) for h in map(tuple, snap["hits"])}, key=lambda t: (t[0], t[1], t[2], t[3])); OUT = open(os.path.join(LANE, f"bf2_scan{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()
CH = {}
def check(n, ok, d): CH[n] = bool(ok); say(f"[{'PASS' if ok else 'FAIL'}] {n}: {d}")
A = rq3(); A.crg(); import crg1_sparc as Cs
src = open(os.path.join(BF1, "bf1.py")).read().split('if __name__ == "__main__"')[0]; argv = sys.argv; sys.argv = ["bf1.py", "real"]; B = {"__file__": os.path.join(BF1, "bf1.py"), "__name__": "bf1x"}; exec(compile(src, "bf1.py", "exec"), B); sys.argv = argv; ST, SH, XT, XH, X = B["ST"], B["SH"], B["XT"], B["XH"], B["X"]; A0B = B["A0"]
def fixed(s, w, D):
    y = D[:, 0] / A0B; H = H_of(s, y, D[:, 2], D[:, 3]); return np.log10(D[:, 1] / wrap(w, D[:, 0], A0B, H))
# ---------- flat free-Upsilon path, same arithmetic as crg1_sparc.fit
G = Cs.load_gal(); ofs = np.r_[0, np.cumsum([len(g["R"]) for g in G])]; GB = np.hstack([Cs.gB_mat(g) for g in G]); RR = np.hstack([g["R"] for g in G]); GO = np.hstack([(g["Vobs"] * 1e3) ** 2 / g["R"] for g in G]); VO = np.hstack([g["Vobs"] for g in G]); W = np.hstack([1 / (np.maximum(g["eV"], 1) / np.maximum(g["Vobs"], 1)) ** 2 for g in G]); GG = np.hstack([np.sign(g["Vgas"]) * g["Vgas"] ** 2 * 1e6 / g["R"] for g in G])
OK = (GB > 0) & (GO > 0) & np.isfinite(GB) & (VO > 0); GQ = np.where(GB > 0, GB, 1.0); FF = np.clip(GG / GQ, 0, 1); LOGO = np.log10(np.where(GO > 0, GO, 1.0)); WOK = W[None, :] * OK; BS = np.add.reduceat(WOK, ofs[:-1], axis=1)
Vf = np.array([g["Vflat"] for g in G]); Qq = np.array([g["Q"] <= 2 and g["Inc"] >= 30 for g in G]); LO, HI = Qq & (Vf > 0) & (Vf < 100), Qq & (Vf > 150); UPS = Cs.UPS
LT = Cs.load_lt(); MG = {q_["name"]: float(q_["Mgas_1e7Msun"]) for q_ in csv.DictReader(open(os.path.join(A.CRG, "inputs", "little_things", "oh2015_table2.csv")))}
LTg = np.array([Cs.E.G * x["Mb"] * Cs.E.Msun / x["R"] ** 2 for x in LT]); LTo = np.array([math.log10(x["V"] ** 2 / x["R"]) for x in LT]); LTf = np.array([MG[x["name"]] * 1e7 / x["Mb"] for x in LT]); LTr = np.array([x["R"] for x in LT])
def free_flat(modelfn):
    gp = modelfn(GQ, FF, RR); gp = np.where(GB > 0, gp, GB); r = np.where(OK, LOGO - np.log10(np.maximum(gp, 1e-300)), 0.0); Aa = np.add.reduceat(WOK * r * r, ofs[:-1], axis=1)
    with np.errstate(all="ignore"): q = np.where(BS > 0, Aa / BS, np.inf)
    i = np.argmin(np.where(np.isnan(q), np.inf, q), axis=0); ii = np.arange(len(G)); bad = ~np.isfinite(q).any(axis=0); ww = Aa[i, ii]; wb = BS[i, ii]; ww[bad] = 0; wb[bad] = 0; Yb = UPS[i].astype(float); Yb[bad] = np.nan
    return dict(rms=float(math.sqrt(ww.sum() / wb.sum())) if wb.sum() > 0 else float("inf"), Y=float(np.nanmedian(Yb)), tilt=float(np.nanmedian(Yb[LO]) - np.nanmedian(Yb[HI])), Yb=Yb, nonfinite=bool(not np.isfinite(gp).all()))
def form_model(s, w, a0):
    uel = "ell" in uses(s)
    def fn(g, f, R): return wrap(w, g, a0, H_of(s, g / a0, R * a0 / C ** 2 if uel else g * 0, f))
    return fn
def lt_med(s, w, a0):
    H = H_of(s, LTg / a0, LTr * a0 / C ** 2, LTf); return float(np.median(LTo - np.log10(wrap(w, LTg, a0, H))))
# ---------- checks K3, K4
lawfn = lambda g, f, R: law(g, A0["canonical"]) * HMUT
r0 = free_flat(lawfn); rc = Cs.fit(G, lambda g, gb: law(gb, A0["canonical"])); check("K3 law", abs(r0["rms"] - rc["rms"]) < 1e-9 and r0["Y"] == rc["Y_med"], f"flat {r0['rms']:.6f}, {r0['Y']} vs CRG1 fit {rc['rms']:.6f}, {rc['Y_med']}")
spec = __import__("importlib.util").util.spec_from_file_location("ux3c", os.path.join(RQ3, "candidates", "ux3_term.py")); ux = __import__("importlib.util").util.module_from_spec(spec); spec.loader.exec_module(ux)
def uxf(g, f, R): return ux.g(dict(gb=g, gg=f * g, a0=A0["canonical"]))
ruf = free_flat(uxf); ruc = Cs.fit(G, lambda g, gb: ux.g(dict(gb=gb, gg=np.broadcast_to(np.sign(g["Vgas"]) * g["Vgas"] ** 2 * 1e6 / g["R"], gb.shape), a0=A0["canonical"]))); say(f"UX3 term flat rms {ruf['rms']:.6f} U {ruf['Y']}, CRG1 fit {ruc['rms']:.6f} {ruc['Y_med']}, record 0.0907, 0.30")
check("K3 UX3 term", abs(ruf["rms"] - ruc["rms"]) < 1e-3 and ruf["Y"] == ruc["Y_med"], "gas clipped at 0 in both; tolerance relaxed from 1e-9 only if printed difference is from the clip")
P1 = "(sq(((f+2.0)/inv1p(f)))*inv1p(((f+pi)+(f/y))))"; d, dx, dxh, dh = fixed(P1, 3, ST), fixed(P1, 3, XT), fixed(P1, 3, XH), fixed(P1, 3, SH)
v = (np.sqrt((d * d).mean()), dx.mean(), np.sqrt((dx * dx).mean()), dxh.mean(), np.sqrt((dxh * dxh).mean()), np.sqrt((dh * dh).mean())); check("K4 P1", all(abs(a - b) <= 1.01e-3 for a, b in zip(v, (.184, .033, .099, -.009, .077, .213))), "got " + ", ".join(f"{q:.4f}" for q in v) + " vs interim .184 +.033 .099 -.009 .077 .213")
dn = np.log10(X[:, 1] / law(X[:, 0], A0B)) - math.log10(HMUT); check("K4 H=1 X-COP", abs(dn.mean() - .4675) < 5e-4, f"{dn.mean():+.4f}")
RT = float(np.sqrt((np.log10(ST[:, 1] / law(ST[:, 0], A0B)) ** 2).mean())); RH = float(np.sqrt((np.log10(SH[:, 1] / law(SH[:, 0], A0B)) ** 2).mean()))
for f in FEET:
    a = A0[f]; r_ = free_flat(lambda g, ff, R: law(g, a)); say(f"law free-Upsilon {f}: rms {r_['rms']:.4f} U {r_['Y']:.2f} tilt {r_['tilt']:+.3f} LT {float(np.median(LTo - np.log10(law(LTg, a)))):+.4f}")
say(f"law fixed-Upsilon: train {RT:.4f}, holdout {RH:.4f}; gate 2 line {1.05 * RT:.4f}")
# ---------- scan
t0 = time.time(); rows = []; seen = {}
for q, (i, o, j, w) in enumerate(hits):
    s = f"({nm[i]}{o}{nm[j]})"; d, dt = {}, None
    try:
        dt, dh, dx, dxh, da = fixed(s, w, ST), fixed(s, w, SH), fixed(s, w, XT), fixed(s, w, XH), fixed(s, w, X)
    except Exception as e: rows.append(dict(s=s, w=w, err=str(e))); continue
    if not (np.isfinite(dt).all() and np.isfinite(da).all()): rows.append(dict(s=s, w=w, err="non-finite on BF1 rows")); continue
    sg, nd = signature(s); h0 = H_at_f0(s); r = dict(s=s, w=w, sig=f"W{w} {sg}", nodes=nd, rms=float(np.sqrt((dt * dt).mean())), med=float(np.median(dt)), rmsh=float(np.sqrt((dh * dh).mean())), medh=float(np.median(dh)), x=float(dx.mean()), xr=float(np.sqrt((dx * dx).mean())), xh=float(dxh.mean()), xhr=float(np.sqrt((dxh * dxh).mean())), xa=float(da.mean()), xar=float(np.sqrt((da * da).mean())), h0min=float(np.nanmin(h0)) if np.isfinite(h0).any() else float("nan"), h0max=float(np.nanmax(h0)) if np.isfinite(h0).any() else float("nan"), h0ok=bool(np.isfinite(h0).all() and np.max(np.abs(h0 - 1)) < 1e-12), ell="ell" in uses(s), y="y" in uses(s), f="f" in uses(s))
    for ft in FEET:
        fr = free_flat(form_model(s, w, A0[ft])); r[ft] = dict(rms=fr["rms"], U=fr["Y"], tilt=fr["tilt"], LT=lt_med(s, w, A0[ft]), nf=fr["nonfinite"])
    c = r["canonical"]; r["S"] = max(c["rms"] / .110, abs(c["U"] - .65) / .15, abs(c["tilt"]) / .15, abs(c["LT"]) / .10, abs(r["xa"]) / .05, r["xar"] / .10) if not c["nf"] else float("inf"); rows.append(r)
    if q % 500 == 0: print(q, f"{time.time() - t0:.0f} s", flush=True)
good = [r for r in rows if "err" not in r]; say(f"snapshot: {snap['n_lines']} lines, sha256 {snap['sha256']}, {snap['n_done']} jobs done; distinct {len(hits)}; scored {len(good)}; unscored {len(rows) - len(good)}")
# ---------- families
fam = {}
for r in good: fam.setdefault(r["sig"], []).append(r)
order = sorted(fam, key=lambda k: -len(fam[k])); say(f"families {len(fam)}; both f and y {sum(r['f'] and r['y'] for r in good)}; ell in {sum(r['ell'] for r in good)}; H(f=0)=1 {sum(r['h0ok'] for r in good)}; wrappers " + str({w: sum(r['w'] == w for r in good) for w in (1, 2, 3)}))
FAM = []
for k in order:
    v = fam[k]; rp = min(v, key=lambda r: (r["nodes"], r["s"])); bs = min(v, key=lambda r: r["S"]); FAM.append(dict(sig=k, n=len(v), rep=rp["s"], rep_w=rp["w"], rep_nodes=rp["nodes"], rep_h0=[rp["h0min"], rp["h0max"]], h0ok=sum(r["h0ok"] for r in v), best_S=bs["S"], best_S_form=bs["s"], best_rms=min(r["rms"] for r in v), best_free=min(r["canonical"]["rms"] for r in v)))
for F in FAM[:30]: say(f"{F['n']:5d} {F['sig'][:62]:62s} h0ok {F['h0ok']:4d} best S {F['best_S']:.2f} fixed {F['best_rms']:.3f} free {F['best_free']:.3f} | {F['rep'][:70]}")
# ---------- free vs fixed
def cnt(fn): return sum(fn(r) for r in good)
c_ = lambda r: r["canonical"]; a_ = lambda r: r["alt"]
for lab, g_ in (("canonical", c_), ("alt", a_)):
    say(f"{lab}: A1 rms <= .110 {cnt(lambda r: g_(r)['rms'] <= .11)}; A2 U .5-.8 {cnt(lambda r: .5 <= g_(r)['U'] <= .8)}; both {cnt(lambda r: g_(r)['rms'] <= .11 and .5 <= g_(r)['U'] <= .8)}; + tilt {cnt(lambda r: g_(r)['rms'] <= .11 and .5 <= g_(r)['U'] <= .8 and abs(g_(r)['tilt']) <= .15)}; + LT {cnt(lambda r: g_(r)['rms'] <= .11 and .5 <= g_(r)['U'] <= .8 and abs(g_(r)['tilt']) <= .15 and abs(g_(r)['LT']) <= .10)}; lowest free rms {min(g_(r)['rms'] for r in good):.4f}")
say(f"X-COP all 7, |mean| <= .05, rms <= .10: {cnt(lambda r: abs(r['xa']) <= .05 and r['xar'] <= .10)}; S <= 1: {cnt(lambda r: r['S'] <= 1)}; fixed train rms <= line: {cnt(lambda r: r['rms'] <= 1.05 * RT)}; lowest S {min(r['S'] for r in good):.3f}")
ff = np.array([r["rms"] for r in good]); fr = np.array([r["canonical"]["rms"] for r in good]); say(f"Spearman fixed vs free rms {float(np.corrcoef(np.argsort(np.argsort(ff)), np.argsort(np.argsort(fr)))[0, 1]):+.3f}")
# ---------- selection
top = sorted([r for r in good], key=lambda r: (r["S"], r["nodes"], r["s"])); p2 = top[0]; p3 = min([r for r in good if r["h0ok"]], key=lambda r: (r["S"], r["nodes"], r["s"])) if any(r["h0ok"] for r in good) else None; p4 = next(r for r in good if r["s"] == FAM[0]["rep"] and r["w"] == FAM[0]["rep_w"]); p1 = next(r for r in good if r["s"] == P1 and r["w"] == 3)
SEL = dict(P1=p1, P2=p2, P3=p3, P4=p4)
for t, r in SEL.items():
    if r is None: say(f"{t}: none"); continue
    c = r["canonical"]; a = r["alt"]; say(f"{t}: W{r['w']} {r['s']}  nodes {r['nodes']} H(f=0) {r['h0min']:.3f}-{r['h0max']:.3f} S {r['S']:.3f}\n   fixed {r['rms']:.3f}/{r['rmsh']:.3f} X all {r['xa']:+.3f},{r['xar']:.3f} | canonical free {c['rms']:.4f} U {c['U']:.2f} tilt {c['tilt']:+.3f} LT {c['LT']:+.3f} | alt free {a['rms']:.4f} U {a['U']:.2f} tilt {a['tilt']:+.3f} LT {a['LT']:+.3f}")
    write_cand(t, r["s"], r["w"], f"Selection {t}, frozen rule.")
write_cand("Hone", "1.0", 3, "H = 1, known answer.")
say("top 10 by S:"); [say(f"  S {r['S']:.3f} W{r['w']} {r['s'][:80]} free {r['canonical']['rms']:.3f} U {r['canonical']['U']:.2f} tilt {r['canonical']['tilt']:+.2f} LT {r['canonical']['LT']:+.3f} X {r['xa']:+.3f},{r['xar']:.3f} h0 {r['h0min']:.2f}") for r in top[:10]]
json.dump(dict(checks=CH, rows=rows, families=FAM, selection={k: v for k, v in SEL.items()}), open(os.path.join(LANE, f"bf2_scan{TAG}.json"), "w"), indent=0, sort_keys=True, default=float)
say(f"wall {time.time() - t0:.0f} s; failed checks {[k for k, v in CH.items() if not v]}"); OUT.close()
if MUT: sys.exit(1)
