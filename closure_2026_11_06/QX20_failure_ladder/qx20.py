#!/usr/bin/env python3
"""QX20 (criteria f3967a1aa9): which single measured variable does the plain-law offset ladder track?
python3 qx20.py [--mutate]   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json, math, csv
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUT = "--mutate" in sys.argv; TAG = "qx20_MUTATE" if MUT else "qx20"; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
# QX5 loaders (QX16-fixed), read-only: execute qx5.py's source up to its sample-building line
src = open(os.path.join(REPO, "closure_2026_11_06", "QX5_cluster_terms", "qx5.py")).read()
cut = src.index("XC, SP, EL, LE, GR = ")
NS = {"__file__": os.path.join(REPO, "closure_2026_11_06", "QX5_cluster_terms", "qx5.py"), "__name__": "qx5_lib"}
_argv = sys.argv; sys.argv = [sys.argv[0]]; exec(compile(src[:cut], "qx5_lib", "exec"), NS); sys.argv = _argv
G, MS, KPC, C = NS["G"], NS["MS"], NS["KPC"], NS["C"]
A0, glaw, phi_from, tail_phi = NS["A0"], NS["glaw"], NS["phi_from"], NS["tail_phi"]
XC, SP, EL, GR = NS["xcop"](), NS["sparc"](), NS["ellipticals"](), NS["groups"]()
S1 = os.path.join(REPO, "rebuild_2026_10_22", "S1_v3_hosted_small")
UROWS = list(csv.DictReader(open(os.path.join(S1, "s1_coma_per_galaxy.csv"))))
R1 = json.load(open(os.path.join(S1, "s1_v3_hosted_small_results.json")))["coma"]
FST = 0.5
VARS = ["V1_Mb", "V2_vobs", "V3_fgas", "V4_gN", "V5_r_over_rM", "V6_depth"]
KA = {"canonical": dict(X=0.467499, E=0.209888, S=0.027383, G0=0.358644, G1=0.195519),
      "alt": dict(X=0.434523, E=0.188763, S=-0.000603, G0=0.320274, G1=0.158280)}

def build(a0, newton=False, fst=FST):
    law = (lambda gN: gN) if newton else (lambda gN: glaw(gN, a0))
    H, S, U = [], [], []
    for g in SP:  # SPARC (zero anchor)
        r, V = g["R"], g["V"]; gobs = V ** 2 / r; gbar = g["vb2"] / r; gl = law(gbar)
        Mtot_b = g["vb2"][-1] * r[-1] / G
        for i in range(len(r)):
            Mb = g["vb2"][i] * r[i] / G
            S.append(dict(D=math.log10(gobs[i] / gl[i]), V1_Mb=Mb / MS, V2_vobs=V[i] / 1e3,
                          V3_fgas=min(max(g["vg2"][i] / g["vb2"][i], 0.0), 1.0), V4_gN=gbar[i] / a0,
                          V5_r_over_rM=r[i] / math.sqrt(G * Mtot_b / a0), V6_depth=phi_from(r, gobs, i, Mtot_b, a0) / C ** 2))
    for e in EL:  # ellipticals, Kroupa, 2/4/8 Re
        rg = np.linspace(2 * e["Re"], 8 * e["Re"], 400) * KPC
        gt = np.array([G * e["Mtot"](x / KPC) * MS / x ** 2 for x in rg]); Mbt = e["Mbar"](1e9)
        for m in (2, 4, 8):
            r = m * e["Re"]; rm = r * KPC; Mb = e["Mbar"](r); Mo = e["Mtot"](r)
            gN = G * Mb * MS / rm ** 2; Ml = law(gN) * rm ** 2 / G / MS; i = int(np.argmin(abs(rg - rm)))
            H.append(dict(cls="E", D=math.log10(Mo / Ml), V1_Mb=Mb, V2_vobs=math.sqrt(G * Mo * MS / rm) / 1e3, V3_fgas=0.0,
                          V4_gN=gN / a0, V5_r_over_rM=rm / math.sqrt(G * Mbt * MS / a0),
                          V6_depth=phi_from(rg, gt, i, e["Mbar"](8 * e["Re"]) * MS, a0) / C ** 2))
    for z in XC:  # X-COP
        rm = z["r_kpc"] * KPC; gN = G * z["M_b"] * MS / rm ** 2; Ml = law(gN) * rm ** 2 / G / MS
        hr = z["hr"] * KPC; gh = G * z["hM"] * MS / hr ** 2; i = int(np.searchsorted(hr, rm))
        dep = (float(np.trapz(np.concatenate([[G * z["M_obs"] * MS / rm ** 2], gh[i:]]), np.concatenate([[rm], hr[i:]])))
               + tail_phi(z["Mb_last"][0] * MS, z["Mb_last"][1] * KPC, a0)) / C ** 2
        H.append(dict(cls="X", D=math.log10(z["M_obs"] / Ml), V1_Mb=z["M_b"], V2_vobs=math.sqrt(G * z["M_obs"] * MS / rm) / 1e3,
                      V3_fgas=z["M_gas"] / z["M_b"], V4_gN=gN / a0, V5_r_over_rM=rm / math.sqrt(G * z["Mb_last"][0] * MS / a0), V6_depth=dep))
    for gp in GR:  # groups
        sl = math.log(gp["M5"] / gp["M25"]) / math.log(gp["R5"] / gp["R25"])
        for j, p in enumerate(gp["pts"]):
            rm = p["r_kpc"] * KPC; Mb = p["M_gas"] * (1 + fst); gN = G * Mb * MS / rm ** 2; Ml = law(gN) * rm ** 2 / G / MS
            rr = np.linspace(p["r_kpc"], gp["R5"], 200) * KPC; Mr = gp["M25"] * (rr / (gp["R25"] * KPC)) ** sl
            dep = ((float(np.trapz(G * Mr * MS / rr ** 2, rr)) if j == 0 else 0.0) + tail_phi(gp["g5"] * MS, gp["R5"] * KPC, a0)) / C ** 2
            H.append(dict(cls="G", D=math.log10(p["M_obs"] / Ml), V1_Mb=Mb, V2_vobs=math.sqrt(G * p["M_obs"] * MS / rm) / 1e3,
                          V3_fgas=1 / (1 + fst), V4_gN=gN / a0, V5_r_over_rM=rm / math.sqrt(G * gp["g5"] * (1 + fst) * MS / a0), V6_depth=dep))
    return H, S

def udgs(f, a0):
    out = []
    for r in UROWS:
        if r["footing"] != f: continue
        Ms = float(r["Mstar"]); rh = 4 / 3 * float(r["Re_kpc"]) * KPC
        out.append(dict(D=float(r["E_v3_dmean"]) / math.log(10), V1_Mb=Ms, V2_vobs=float(r["sigma"]), V3_fgas=0.0,
                        V4_gN=G * Ms / 2 * MS / rh ** 2 / a0, V5_r_over_rM=rh / math.sqrt(G * Ms * MS / a0), V6_depth=None))
    return out

BGRID = np.round(np.arange(-3, 3.0001, 0.01), 2)
def fitpl(v, D):
    vm = float(np.median(v)); best = None
    for b in BGRID:
        with np.errstate(divide="ignore", invalid="ignore"):
            x = (v / vm) ** b if b != 0 else np.ones_like(v)
        if not np.all(np.isfinite(x)): continue          # e.g. f_gas = 0 with b < 0 (first-run nan, disclosed)
        A = max(float((x * D).sum() / (x * x).sum()), 0.0); rms = float(np.sqrt(((D - A * x) ** 2).mean()))
        if best is None or rms < best[2]: best = (A, float(b), rms)
    return dict(A=best[0], b=best[1], rms=best[2], vmed=vm)
def pred(m, v):
    v = np.asarray(v, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        x = np.where(v > 0, (v / m["vmed"]) ** m["b"], 0.0 if m["b"] > 0 else np.inf) if m["b"] != 0 else np.ones_like(v)
    return m["A"] * x

RES = dict(tag=TAG, criteria="f3967a1aa9", note="kappa = 1/2 FITTED; not theory closed", fst_primary=FST)
for f, a0 in A0.items():
    H, S = build(a0, newton=MUT)
    Dh = np.array([h["D"] for h in H]); Ds = np.array([s["D"] for s in S]); Sobs = float(Ds.mean())
    cm = {c: float(np.mean([h["D"] for h in H if h["cls"] == c])) for c in "EXG"}
    R = dict(n_hot=len(H), n_sparc=len(S), class_means=cm, sparc_mean=Sobs)
    if not MUT:
        H0, _ = build(a0, fst=0.0); H1, _ = build(a0, fst=1.0)
        g0 = float(np.mean([h["D"] for h in H0 if h["cls"] == "G"])); g1 = float(np.mean([h["D"] for h in H1 if h["cls"] == "G"]))
        k = KA[f]; d = max(abs(cm["X"] - k["X"]), abs(cm["E"] - k["E"]), abs(Sobs - k["S"]), abs(g0 - k["G0"]), abs(g1 - k["G1"]))
        U = udgs(f, a0); um = float(np.mean([u["D"] for u in U])); ka2 = abs(um - R1[f"{f}|S4 v3 dmean L*floor E-W"]["meanE"] / math.log(10))
        st = R1[f"{f}|S4 v3 dmean L*floor E-W"]; usig = math.hypot(st["se"], st["sigma_sys"]) / math.log(10)
        R.update(KA1_maxdiff=d, KA1=bool(d <= 1e-6 + 5e-7), groups_fst0=g0, groups_fst1=g1, udg_mean=um, udg_sigma_dex=usig, KA2=bool(ka2 <= 1e-9), KA2_diff=ka2)
        P(f"[{f}] KA1 class means X {cm['X']:+.6f} E {cm['E']:+.6f} S {Sobs:+.6f} G(f*0) {g0:+.6f} G(f*1) {g1:+.6f} G(f*0.5) {cm['G']:+.6f}: max|d| {d:.1e} -> {'PASS' if R['KA1'] else 'FAIL'}")
        P(f"[{f}] KA2 UDG mean {um:+.4f} dex (sigma {usig:.3f}): |d| {ka2:.1e} -> {'PASS' if R['KA2'] else 'FAIL'}")
    else:
        P(f"[{f}] NEWTON baseline: class means X {cm['X']:+.3f} E {cm['E']:+.3f} G {cm['G']:+.3f}; SPARC mean {Sobs:+.3f}")
    R["vars"] = {}
    for vn in VARS:
        v = np.array([h[vn] for h in H], float); vs = np.array([s[vn] for s in S], float)
        m = fitpl(v, Dh); zp = float(np.mean(pred(m, vs))); zgap = zp - Sobs
        lo, hi = np.percentile(v, 5), np.percentile(v, 95); ov = (vs >= lo) & (vs <= hi); hv = (v >= lo) & (v <= hi)
        nov = int(ov.sum())
        if nov < 20: shape = "SEPARATED"; step = None
        else:
            step = float(np.median(Dh[hv]) - np.median(Ds[ov])); shape = "STEP" if abs(step) > 0.10 else ("ONE CURVE" if abs(zgap) <= 0.057 else "NO STEP, ANCHOR MISSED")
        Hok = m["rms"] <= 0.10; Zok = bool(np.isfinite(zgap) and abs(zgap) <= 0.057)
        e = dict(fit=m, H=bool(Hok), Z=Zok, sparc_pred=zp, Z_gap=zgap, n_overlap=nov, step=step, shape=shape)
        if not MUT and vn != "V6_depth":
            U = udgs(f, a0); up = float(np.mean(pred(m, [u[vn] for u in U]))); e.update(udg_pred=up, udg_gap_sigma=(up - R["udg_mean"]) / R["udg_sigma_dex"])
        if not MUT:  # M1 shuffle (all variables reported; graded for the best)
            rng = np.random.default_rng(20261106); cnt = 0
            for _ in range(200):
                if fitpl(rng.permutation(v), Dh)["rms"] <= m["rms"]: cnt += 1
            e["shuffle_frac"] = cnt / 200
        R["vars"][vn] = e
        P(f"[{f}] {vn:14s} hot fit A {m['A']:.3f} b {m['b']:+.2f} rms {m['rms']:.3f} ({'H ok' if Hok else 'H FAIL'}); SPARC pred {zp:+.3f} vs obs {Sobs:+.3f} gap {zgap:+.3f} ({'Z ok' if Zok else 'Z FAIL'}); "
          f"overlap {nov} -> {shape}{'' if step is None else f' (hot-SPARC {step:+.3f})'}"
          + (f"; UDG pred {e['udg_pred']:+.3f} vs {R['udg_mean']:+.3f} ({e['udg_gap_sigma']:+.1f} sig)" if "udg_pred" in e else ("; UDG N/A" if not MUT else ""))
          + (f"; shuffle frac {e['shuffle_frac']:.3f}" if "shuffle_frac" in e else ""))
    RES[f] = R

if not MUT:
    pr = [vn for vn in VARS if all(RES[f]["vars"][vn]["H"] and RES[f]["vars"][vn]["Z"] for f in A0)]
    rank = sorted(VARS, key=lambda vn: (vn not in pr, max(abs(RES[f]["vars"][vn]["Z_gap"]) if np.isfinite(RES[f]["vars"][vn]["Z_gap"]) else 9 for f in A0),
                                        max(RES[f]["vars"][vn]["fit"]["rms"] for f in A0)))
    best = rank[0]; inf = all(RES[f]["vars"][best]["shuffle_frac"] <= 0.05 for f in A0)
    RES.update(predictive=pr, ranking=rank, best=best, best_informative=inf,
               label=(f"TRACKED BY {best}" if pr and inf else ("NO SINGLE VARIABLE" if not pr else f"{best} PREDICTIVE BUT NOT INFORMATIVE (shuffle)")))
    P("RANKING: " + ", ".join(rank)); P(f"best {best}: shuffle informative {inf}")
    P(f"LABEL: {RES['label']}")
else:
    allZfail = all(not RES[f]["vars"][vn]["Z"] for f in A0 for vn in VARS)
    RES["M2_bites"] = allZfail; P(f"M2 Newton: Z fails for every variable on both footings: {'BITES' if allZfail else 'NO BITE'}")
json.dump(RES, open(os.path.join(HERE, f"{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"{TAG}.out"), "w").write("\n".join(OUT) + "\n")
