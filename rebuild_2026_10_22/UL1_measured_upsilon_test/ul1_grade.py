#!/usr/bin/env python3
"""UL1 gate (FROZEN_CRITERIA.md). Reads rows/, ul1_est.json. --mutate writes ul1_MUTATE.out only. kappa = 1/2 FITTED, unused; not theory closed; no pass of route E is claimed or tested."""
import json, math, os, pickle, sys
import numpy as np
sys.argv, ARGS = [sys.argv[0]], sys.argv[1:]
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); sys.path.insert(0, HERE); import ul1_core as C
MUT = "--mutate" in ARGS; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
G = C.load(); UPS = C.UPS; IR = C.IREC; TG = C.TG; NG = len(G); BINS = ("60-100", "100-150", "150-200", "200-250", "250-400"); ALLB = ("20-60",) + BINS
vf = np.array([q["meta"]["Vflat"] for q in G]); Qs = np.array([(q["meta"]["Q"] <= 2 and q["meta"]["Inc"] >= 30 and q["meta"]["Vflat"] > 0) for q in G]); fb = np.array([q["Vbul"][-1] ** 2 / max(q["Vdisk"][-1] ** 2 + q["Vbul"][-1] ** 2, 1e-9) for q in G]); TOT = 1 + 0.4 * fb
def lohi(b): return tuple(float(a) for a in b.split("-"))
SEL = {b: Qs & (vf >= lohi(b)[0]) & (vf < lohi(b)[1]) for b in ALLB}
EST = json.load(open(os.path.join(HERE, "ul1_est.json")))
def best(wr2, ws, idx=None):
    m = np.where(ws > 0, wr2 / np.maximum(ws, 1e-300), np.inf)
    if idx is not None: m2 = np.full_like(m, np.inf); m2[:, idx] = m[:, idx]; m = m2
    return np.argmin(m, axis=1), m
def stats(wr2, ws, iu): i = np.arange(NG); return math.sqrt(wr2[i, iu].sum() / ws[i, iu].sum()), float(np.median(UPS[iu]))
def tilt(u): return float(np.median(u[Qs & (vf < 100)]) - np.median(u[Qs & (vf > 150)]))
RNG = lambda: np.random.default_rng(1)
def boot(u, B=2000):
    r = RNG(); n = len(u)
    if n == 0: return np.nan
    return float(np.std(np.log10(np.median(u[r.integers(0, n, (B, n))], axis=1))))
def binvals(u):  # model values, total-light equivalent
    return {b: dict(m=float(np.median((u * TOT)[SEL[b]])), U=float(np.median(u[SEL[b]])), n=int(SEL[b].sum()), e=boot((u * TOT)[SEL[b]]), Vmed=float(np.median(vf[SEL[b]]))) for b in ALLB}
def gate(bv, et):
    """et: estimator table for X; returns level, shape, detail."""
    m = np.log10([bv[b]["m"] for b in BINS]); mu = np.log10([et[b]["mu"] for b in BINS]); h = np.array([math.sqrt(max(bv[b]["e"], 1.25 * et[b]["sig"] / math.sqrt(bv[b]["n"])) ** 2 + 0.04 ** 2) for b in BINS]); d = m - mu; Z = d / h; lev = bool(np.all(np.abs(Z) <= 2))
    w = 1 / h ** 2; off = float((w * d).sum() / w.sum()); chi = float((((d - off) / h) ** 2).sum())
    def slope(y, V): x = np.log10(V); X = (w * x).sum() / w.sum(); s = (w * (x - X) * (y - (w * y).sum() / w.sum())).sum() / (w * (x - X) ** 2).sum(); return float(s), float(1 / math.sqrt((w * (x - X) ** 2).sum()))
    s, es = slope(m, [bv[b]["Vmed"] for b in BINS]); sX, _ = slope(mu, [et[b]["Vmed"] for b in BINS]); st = np.diff(m) - np.diff(mu); sh = np.sqrt(h[:-1] ** 2 + h[1:] ** 2); stepok = bool(np.all(np.abs(st) <= 2 * sh)); a, b_, c = chi <= 9.49, bool(s > 0 and abs(s - sX) <= 2 * es), stepok
    return dict(level=lev, shape=bool(a and b_ and c), Z=Z.tolist(), off=off, chi=chi, a=bool(a), slope=s, eslope=es, slopeX=sX, b=bool(b_), c=bool(c), steps=(st / sh).tolist(), h=h.tolist())
def lab(g): return "CONSISTENT" if g[0] and g[1] else "LEVEL ONLY" if g[0] else "SHAPE ONLY" if g[1] else "NOT"
def rowgrade(wr2s, ests, idx=None):
    o = {}
    for t in TG:
        iu, m = best(wr2s[t][0], wr2s[t][1], idx); u = UPS[iu]; bv = binvals(u); o[t] = dict(bv=bv, g={x: gate(bv, {b_: ests[b_][x] for b_ in BINS}) for x in ("Taylor", "GSWLC")}, iu=iu, m=m)
    r = {x: (all(o[t]["g"][x]["level"] for t in TG), all(o[t]["g"][x]["shape"] for t in TG)) for x in ("Taylor", "GSWLC")}; return o, r
PR = EST["primary"]
if MUT:
    PRo = {x: 0 for x in ()}
    PR = json.loads(json.dumps(PR))  # reverse the trend across gated bins
    for x in ("Taylor", "GSWLC"):
        mus = [PR[b][x]["mu"] for b in BINS][::-1]
        for b, v in zip(BINS, mus): PR[b][x]["mu"] = v
ROWN = ["hand_off", "hand_fq", "hand_blum", "hand_gnedin", "nat_off", "nat_fq", "nat_blum", "nat_gnedin", "fc1_off", "fc1_fq", "law_canonical", "law_alt"]; D = {}
for n in ROWN + ["nat_fq_mb2", "hand_fq_self", "nat_fq_self"]:
    z = np.load(os.path.join(HERE, "rows", n + ".npz")); D[n] = dict({t: (z[f"{t}_wr2"], z[f"{t}_ws"]) for t in TG}, lt=z["lt"])
# Checks
ok = True; S3 = json.load(open(os.path.join(RB, "SP3_starting_point", "sp3_hand_results.json")))["runs"]; names = [q["name"] for q in G]
for n, k, want in (("hand_off", "EM1|off", None), ("hand_blum", "EM1|blum", None)):
    d = 0.0; db = 0.0
    for t in TG:
        iu, _ = best(*D[n][t], IR); w = S3[k]["Ugal"][t]; d = max(d, max(abs(UPS[iu][i] - w[names[i]]) for i in range(NG))); u = UPS[iu]; rec = S3[k]["sparc"][t]["bins"]; db = max(db, max(abs(np.median(u[SEL[b]]) - rec[b]) for b in rec)) ; rm, um = stats(*D[n][t], iu); db = max(db, abs(rm - S3[k]["sparc"][t]["rms"]), abs(um - S3[k]["sparc"][t]["U"])); dt = abs(tilt(u) - S3[k]["sparc"][t]["tilt"]); db = max(db, dt)
    k1 = d <= 1e-6 and db <= 1e-6; ok &= k1; P(f"K1 {n} record grid vs SP3/NR3: per-galaxy {d:.1e}, bins, rms, U, tilt {db:.1e}: {'PASS' if k1 else 'FAIL'}")
    dl = max(abs(D[n]["lt"][i] - S3[k]["lt"][TG[i]]) for i in (0, 1)); k4 = dl <= 0.001; ok &= k4; P(f"K4 {n} LT |d| {dl:.1e}: {'PASS' if k4 else 'FAIL'}")
cell = json.load(open(os.path.join(RB, "SP3_starting_point", "cells", "EM1_tot_f0.872_m1_d+0.0000.json"))); ce2 = json.load(open(os.path.join(RB, "SP3_starting_point", "cells", "EM1_tot_f0_m1_d+0.0000.json")))
for n, ce in (("nat_fq", cell), ("nat_off", ce2)):
    db = 0
    for t in TG: iu, _ = best(*D[n][t], IR); u = UPS[iu]; rec = ce["sp3"]["binsU"][t]; db = max(db, max(abs(np.median(u[SEL[b]]) - rec[b]) for b in rec))
    k2 = db <= 0.0051; ok &= k2; P(f"K2 {n} record grid bins vs SP3 cell: max |d| {db:.4f}: {'PASS' if k2 else 'FAIL'}")
P4R = dict(canonical=(0.054087447879939264, 0.52), alt=(0.05371798965550355, 0.44))
for f in P4R:
    iu, _ = best(*D["law_" + f][TG[0]], IR); rm, um = stats(*D["law_" + f][TG[0]], iu); k3 = abs(rm - P4R[f][0]) <= 1e-6 and abs(um - P4R[f][1]) <= 0.005; ok &= k3; P(f"K3 law {f}: rms {rm:.6f} U {um:.2f}: {'PASS' if k3 else 'FAIL'}")
k7 = EST["K7"] <= 0.001; ok &= k7; P(f"K7 estimators vs SP3 {EST['K7']:.1e}: {'PASS' if k7 else 'FAIL'}")
# Injection K5/K6 on nat_fq: true U from mu_X(V) or flat, eV noise
def inject(truth, seed):
    W = {}
    for t in TG:
        wr = np.zeros((NG, len(UPS))); ws = np.zeros((NG, len(UPS))); rng = np.random.default_rng(seed)
        for i, q in enumerate(G):
            gh = pickle.load(open(os.path.join(HERE, "cache_rows", f"gh_{t}_{q['name']}.pkl"), "rb")).astype(float); ut = truth(q, i); iu = int(np.argmin(abs(UPS - ut))); g = np.maximum(q["GB"][:, iu] + gh[:, iu], 1e-300); V = np.sqrt(g * q["Rm"]) / 1e3; Vs = V + q["eV"] * rng.standard_normal(len(V)); GOs = np.where(Vs > 0, (Vs * 1e3) ** 2 / q["Rm"], 0.0); wr[i], ws[i] = C.mse_of(q, np.log10(np.maximum(q["GB"] + gh, 1e-300)), GOs)
        W[t] = (wr, ws)
    return W
def mut(x, b_est):
    Vm = np.array([b_est[b][x]["Vmed"] for b in BINS]); mu = np.array([b_est[b][x]["mu"] for b in BINS]); return lambda q, i: float(np.interp(math.log10(max(q["meta"]["Vflat"], 30)), np.log10(Vm), mu)) / TOT[i]
for x in ("Taylor", "GSWLC"):
    for seed in (11, 12):
        _, r = rowgrade(inject(mut(x, EST["primary"]), seed), PR if MUT else EST["primary"]); c = all(r[x]); P(f"{'MUTATE reversed-trend gate' if MUT else 'K5'} injection true {x}, seed {seed}: LEVEL {r[x][0]} SHAPE {r[x][1]}{'' if MUT else ': ' + ('PASS' if c else 'FAIL')}")
        if MUT: ok &= not c
        else: ok &= c
if not MUT:
    _, r = rowgrade(inject(lambda q, i: 0.50, 21), PR); k6 = not all(r["Taylor"]); ok &= k6; P(f"K6 power, flat true 0.50 vs Taylor: LEVEL {r['Taylor'][0]} SHAPE {r['Taylor'][1]}: {'PASS' if k6 else 'FAIL'}; vs GSWLC: LEVEL {r['GSWLC'][0]} SHAPE {r['GSWLC'][1]}")
if MUT:
    z = best(*D["nat_fq"][TG[0]])[0]; z2 = best(*D["nat_fq_mb2"][TG[0]])[0]; dd = max(abs(np.median(UPS[z][SEL[b]]) - np.median(UPS[z2][SEL[b]])) for b in BINS); ok &= dd >= 0.02; P(f"MUTATE M_b x 2 in the response: max bin dU {dd:.3f}: {'PASS' if dd >= 0.02 else 'FAIL'}; all mutate {'PASS' if ok else 'FAIL'}"); open(os.path.join(HERE, "ul1_MUTATE.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
P(f"Checks: {'ALL PASS' if ok else 'FAILED, NO VERDICT'}")
# Grade
RES = {}
P("\nEstimators, gated bins:  " + "  ".join(BINS)); 
for x in ("Taylor", "GSWLC"): P(f"  {x:7s} " + "  ".join(f"{PR[b][x]['mu']:.3f}" for b in BINS) + "   sigma dex " + " ".join(f"{PR[b][x]['sig']:.3f}" for b in BINS))
for n in ROWN:
    o, r = rowgrade(D[n], EST["primary"]); RES[n] = {}; L = {x: lab(r[x]) for x in r}; P(f"\n=== {n}: Taylor {L['Taylor']}; GSWLC {L['GSWLC']}")
    for t in TG:
        iu = o[t]["iu"]; irec, _ = best(*D[n][t], IR); rm, um = stats(*D[n][t], iu); rm2, um2 = stats(*D[n][t], irec); ti, ti2 = tilt(UPS[iu]), tilt(UPS[irec]); bv = o[t]["bv"]; recU = {b: float(np.median(UPS[irec][SEL[b]])) for b in ALLB}; lt = float(D[n]["lt"][TG.index(t)]) if not np.isnan(D[n]["lt"][TG.index(t)]) else None
        P(f" {t[:1]} wide U med {um:.2f} rms {rm:.4f} tilt {ti:+.2f} | record grid U {um2:.2f} rms {rm2:.4f} tilt {ti2:+.2f} LT {('%+.3f' % lt) if lt is not None else 'n/a'}")
        P("   U bins " + " ".join(f"{bv[b]['U']:.2f}" for b in ALLB) + " | record " + " ".join(f"{recU[b]:.2f}" for b in ALLB) + " | U_tot " + " ".join(f"{bv[b]['m']:.2f}" for b in ALLB))
        for x in ("Taylor", "GSWLC"):
            g = o[t]["g"][x]; bad = [b for b, z in zip(BINS, g["Z"]) if abs(z) > 2]; P(f"   {x}: Z " + " ".join(f"{z:+.1f}" for z in g["Z"]) + f" bad {bad}; offset {g['off']:+.3f} chi2 {g['chi']:.1f}{'' if g['a'] else ' X'}; slope {g['slope']:+.2f}+-{g['eslope']:.2f} vs {g['slopeX']:+.2f}{'' if g['b'] else ' X'}; steps " + " ".join(f"{z:+.1f}" for z in g["steps"]) + ("" if g["c"] else " X"))
        env = [bool(bv[b]["m"] >= PR[b]["Taylor"]["mu"] * 10 ** (-2 * o[t]["g"]["Taylor"]["h"][i]) and bv[b]["m"] <= PR[b]["GSWLC"]["mu"] * 10 ** (2 * o[t]["g"]["GSWLC"]["h"][i])) for i, b in enumerate(BINS)]; P(f"   ENVELOPE (report) {env}")
        RES[n][t] = dict(U=um, rms=rm, tilt=ti, U_rec=um2, rms_rec=rm2, tilt_rec=ti2, lt=lt, bins=bv, rec=recU, gate={x: {k: v for k, v in o[t]["g"][x].items()} for x in o[t]["g"]})
    RES[n]["label"] = L
# constraint width on primary rows, and mask caveat
P("\nConstraint width by bin (median half-width of U per galaxy, Delta chi2 = 1 scaled; n at wide-grid ends; n at the record's 0.30 floor)")
for n in ("hand_fq", "nat_fq", "nat_off", "law_canonical"):
    wr, ws = D[n][TG[0]]; iu, m = best(wr, ws); H = []
    for i, q in enumerate(G):
        mn = m[i, iu[i]]; nn = int(q["OK"][:, iu[i]].sum()); inn = np.where(m[i] <= mn * (1 + 1 / max(nn - 1, 1)))[0]; H.append(0.5 * (UPS[inn.max()] - UPS[inn.min()]))
    H = np.array(H); irec, _ = best(wr, ws, IR); P(f" {n}: " + "; ".join(f"{b} n{int(SEL[b].sum())} width {np.median(H[SEL[b]]):.2f}, ends {int(((iu == 0) | (iu == len(UPS) - 1))[SEL[b]].sum())}, floor {int((irec == IR[0])[SEL[b]].sum())}" for b in ALLB)); RES[n]["width"] = {b: float(np.median(H[SEL[b]])) for b in ALLB}
# mask stress: fit only on points valid at every U
P("\nMask stress, nat_fq A: U fit on points valid at all U; gas-dominant dwarfs lose negative-gas radii at low U in the record's mask. And: stars vs gas")
fst = np.array([0.5 * q["meta"]["L36"] / (0.5 * q["meta"]["L36"] + 1.33 * q["meta"]["MHI"]) for q in G]); P(" share of baryons in stars at 0.5, median by bin: " + " ".join(f"{b} {np.median(fst[SEL[b]]):.2f}" for b in ALLB))
wr, ws = D["nat_fq"][TG[0]]; frac = []
for i, q in enumerate(G): iu_ = best(wr, ws)[0][i]; frac.append(ws[i, iu_] / max(ws[i].max(), 1e-300))
frac = np.array(frac); P(f" galaxies whose best U drops > 10 % of the weight through the mask: {int((frac[Qs] < 0.9).sum())} of {int(Qs.sum())}")
# stresses on estimators for primary rows
P("\nGate under estimator stresses (report, no label moves), primary rows:")
for sn in ("w20", "D60", "common"):
    for n in ("hand_fq", "nat_fq", "law_canonical"):
        o, r = rowgrade(D[n], EST[sn]); P(f" {sn} {n}: Taylor {lab(r['Taylor'])}, GSWLC {lab(r['GSWLC'])}")
# self Mb, mb2
P("\nStress, M_b self-consistent (no label): U bins A, LT not rerun")
for n in ("hand_fq_self", "nat_fq_self"):
    o, r = rowgrade(D[n], EST["primary"]); iu = o[TG[0]]["iu"]; irec, _ = best(*D[n][TG[0]], IR); rm, um = stats(*D[n][TG[0]], iu); P(f" {n}: U {um:.2f} rms {rm:.4f} tilt {tilt(UPS[iu]):+.2f}; bins " + " ".join(f"{o[TG[0]]['bv'][b]['U']:.2f}" for b in ALLB) + f"; Taylor {lab(r['Taylor'])}, GSWLC {lab(r['GSWLC'])}; Z T " + " ".join(f"{z:+.1f}" for z in o[TG[0]]["g"]["Taylor"]["Z"]) + "; chi2 " + f"{o[TG[0]]['g']['Taylor']['chi']:.1f}, {o[TG[0]]['g']['GSWLC']['chi']:.1f}")
pri = {x: [n for n in ("nat_fq", "hand_fq") if RES[n]["label"][x] == "CONSISTENT"] for x in ("Taylor", "GSWLC")}; hit = [x for x in pri if pri[x]]
V = "NO VERDICT (check failed)" if not ok else (f"RESPONSE CONSISTENT WITH MEASURED UPSILON {hit}" if hit else "RESPONSE NOT CONSISTENT WITH MEASURED UPSILON"); P(f"\nVERDICT: {V}; rows CONSISTENT: " + str({n: RES[n]["label"] for n in ROWN})); RES["verdict"] = V
json.dump(RES, open(os.path.join(HERE, "ul1_results.json"), "w"), indent=0, default=float); open(os.path.join(HERE, "ul1.out"), "w").write("\n".join(OUT) + "\n")
