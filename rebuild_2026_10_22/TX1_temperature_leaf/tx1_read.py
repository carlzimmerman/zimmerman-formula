#!/usr/bin/env python3
"""TX1 harvest: exact G1, G3 with amended Z_shape, G2' S line, T-effective test, Z ranking. python3 -I tx1_read.py FOOT ARM LEVEL. BK2's names, hit_str, Gates by import. Output tx1_train_LEVEL_FOOT_ARM.json. kappa = 1/2 FITTED; not theory closed."""
import heapq, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tx1_lib import *
foot, arm, lev = sys.argv[1:4]; cap = dict(T0=1500, TL0=15000, TL1=30000)[lev]; S = install((arm, cap)); mode = "mutate" if arm == "mutate" else f"{arm}_{lev}"
import bk2_read as Rd, bk2_gates as Gg
Rd.xcop = lambda a0, which=None: xrows(a0, which, arm, "ho")
W = os.path.join(LANE, "chunks", f"L2_{foot}_{mode}"); N, oa, oD = Rd.names(W); Gt = Rd.Gates(foot, "real"); a0 = Gt.a0; XT = Gt.XT
if arm in PLANTS:
    for T in (Gt.XH, Gt.SH, Gt.ST65, Gt.ST80, Gt.SH65, Gt.SH80): T["go"] = ev(PLANTS[arm], T)
    Gt.ST["go"] = ev(PLANTS[arm], Gt.ST)
X0 = dict(XT); X0["s2"] = np.zeros(len(XT["gb"])); ST = Gt.ST; seen = set(); Scache = {}; tf0 = tfmax = 2000000
C = dict(hits=0, T_hits=0, F_hits=0, F_skipped=0, distinct_T=0, distinct_F=0, nonfinite=0, decor=0, newton=0, cass=0, g3_line=0, g3_err=0, g3_err_bk2=0, zone=0, s_line=0, s_err=0, s_none=0, train_line=0, train_err=0, train_line_cass=0, train_err_cass=0, F_train_line=0, F_train_err=0); B_ = {True: [], False: []}; keep = []; t0 = time.time(); MAXF = 100000; MAXT = int(os.environ.get("TX1_MAXT", "800000"))
for ln in open(os.path.join(W, "hits.jsonl")):
    C["hits"] += 1
    if C["hits"] % 200000 == 0: print(f"{time.time()-t0:.0f}s", C, flush=True)
    h = json.loads(ln); s, fit = Rd.hit_str(h, N, oa, oD); ist = "s2" in s
    if ist: C["T_hits"] += 1
    else:
        C["F_hits"] += 1
    if ist and C["T_hits"] > MAXT: continue
    if not ist and C["F_hits"] > MAXF: C["F_skipped"] += 1; continue
    try: v = ev(s, XT); dx = np.log10(XT["go"] / v)
    except Exception: C["nonfinite"] += 1; continue
    if not np.all(np.isfinite(dx)): C["nonfinite"] += 1; continue
    k = np.round(dx, 7).tobytes() + (np.float64(np.round(ev(s, ST)[:40], 13).sum()).tobytes())
    if k in seen: continue
    seen.add(k); eff = False
    if ist:
        v0 = ev(s, X0); ef = np.median(np.abs(np.log10(v / v0))) if np.all(v0 > 0) else 9.0; eff = bool(np.isfinite(ef) and ef >= 0.05 or not np.isfinite(ef))
        if not eff: C["decor"] += 1
    C["distinct_T" if eff else "distinct_F"] += 1
    sol = Gt.solar(s)
    if not sol["newton"]: continue
    C["newton"] += 1; C["cass"] += sol["cass"]; x = Gt.xc(s, XT); xb = dict(XT); xb["se"] = XT["se_bk2"]; C["g3_err_bk2"] += Gt.xc(s, xb)["err"] if eff else 0; C["g3_line"] += x["line"] and eff; C["g3_err"] += x["err"] and eff
    if not (x["line"] or x["err"] or x["rms"] <= .15): continue
    C["zone"] += 1; sv = ev(s, ST); ks = np.round(sv, 13).tobytes()
    if ks not in Scache:
        d0 = np.log10(ST["go"] / sv); fx = None
        if np.all(np.isfinite(d0)) and np.sqrt((d0 * d0).mean()) <= .30 and abs(np.median(d0)) <= .10: fx = Gg.s_line(s, a0, 1)
        Scache[ks] = (fx, float(np.sqrt((d0 * d0).mean())))
    sl, rf = Scache[ks]
    if sl is None: C["s_none"] += 1; continue
    C["s_line"] += eff and sl["line"]; se = sl["rms"] <= .110 and sl["ZU"] <= 2; C["s_err"] += eff and se; tl = x["line"] and sl["line"] and sl["tilt_ok"]; te = x["err"] and se and sl["tilt_ok"]
    if eff: C["train_line"] += tl; C["train_err"] += te; C["train_line_cass"] += tl and sol["cass"]; C["train_err_cass"] += te and sol["cass"]
    else: C["F_train_line"] += tl; C["F_train_err"] += te
    z = max(abs(x["Zm"]), x["Zs"], sl["ZU"], 2 * sl["rms"] / .110, 2 * abs(sl["tilt"]) / .15, 2 * rf / .5); row = dict(F=s, T=eff, ef=float(ef) if ist else 0.0, fit=fit, cass=sol["cass"], Zc=sol["Zc"], X=x, S=sl, rms_fixed=rf, Z=float(z))
    H = B_[eff]; it = (-row["Z"], -len(s), s, row)
    if len(H) < 300: heapq.heappush(H, it)
    elif it > H[0]: heapq.heapreplace(H, it)
    if (tl or te) and len(keep) < 3000: keep.append(row)
print("FINAL", foot, arm, lev, C, f"{time.time()-t0:.0f}s", flush=True)
by = {k: sorted((t[3] for t in v), key=lambda a: a["Z"]) for k, v in B_.items()}; json.dump(dict(counts=C, tally=json.load(open(os.path.join(W, "tally.json"))), info=json.load(open(os.path.join(W, "info.json"))), T=by[True], F=by[False][:30], train_pass=keep[:500], n_train_pass=len(keep), s_c=SC), open(os.path.join(LANE, f"tx1_train_{lev}_{foot}_{arm}.json"), "w"), indent=0, default=float)
for a in by[True][:6] + by[False][:3]: print(f"T{int(a['T'])} ef {a['ef']:.2f} Z {a['Z']:.2f} cass {a['cass']} X {a['X']['mean']:+.3f},{a['X']['rms']:.3f} Zm {a['X']['Zm']:+.2f} Zs {a['X']['Zs']:.1f} S {a['S']['rms']:.3f} U {a['S']['U']:.2f} tilt {a['S']['tilt']:+.2f} {a['F'][:100]}")
