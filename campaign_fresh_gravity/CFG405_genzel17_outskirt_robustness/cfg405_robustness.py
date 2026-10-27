"""CFG405: does CFG402's residual Genzel+2017 tension survive outskirt cuts and inclination shifts? Criteria: FROZEN_CRITERIA.md (217aaa88ea).
Reuses CFG401's shape/data code (exec'd read-only, as CFG402); CFG402's statistic, vectorised over (a0, f).
Run: nice python3 cfg405_robustness.py ; MUTATE=1 halves the errors in V0 (S must scale x3-x5; rc 1). Single thread."""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, math, json, re, numpy as np
MYDIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUTATE") == "1"
os.environ.pop("MUTATE", None)                         # CFG401's own MUTATE flag must stay off
D401 = os.path.join(MYDIR, "..", "CFG401_genzel17_gas_shape")
src = open(os.path.join(D401, "cfg401_gas_shape.py")).read()
exec(src.split('LF = np.linspace(-3, 3, 601)')[0].replace('HERE = os.path.dirname(os.path.abspath(__file__))', f'HERE = "{D401}"'))
# exec defines: T1, FWHM, A0, E, de, gshape, C4, rows (cfg400_points.csv), data (CFG401's built dicts), KPC

out_lines, controls = [], []
def P(s=""): print(s); out_lines.append(s)
def K(name, ok, val): controls.append({"name": name, "pass": bool(ok), "value": val}); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")

LF = np.linspace(-4, 3, 701); SC = np.logspace(-3, 2, 251)      # CFG402's grids
GALS = list(data.keys())
FOOTS = list(A0.keys())

def build(g, inc=None):
    """CFG401's construction for one galaxy at inclination inc (default Table 1); keeps file order and signed offsets."""
    z, kpa, inc0, Rh, s0, bt, vc, ms, mb = T1[g]
    inc = inc0 if inc is None else inc
    allv = [(float(r["offset_arcsec"]), float(r["value"]), float(r["err"])) for r in rows if r["galaxy"] == g and r["kind"] == "v"]
    off, R, V, eV = [], [], [], []
    for o, v, e in allv:
        if abs(o) < FWHM:
            continue
        off.append(o); R.append(abs(o) * kpa); V.append(abs(v) / math.sin(math.radians(inc))); eV.append(max(e, 1.0) / math.sin(math.radians(inc)))
    off, R, V, eV = map(np.array, (off, R, V, eV))
    vc2 = V**2 + 3.36 * s0**2 * (R / Rh)
    return dict(g=g, z=z, inc=inc, off=off, R=R, gobs=vc2 * 1e6 / (R * KPC), elog=np.sqrt((2 * V * eV / vc2 / math.log(10)) ** 2 + 0.05**2),
                Rh=Rh, bt=bt, fgas=1 - ms / mb, rp=max(o for o, _, _ in allv if o > 0), rm=max(-o for o, _, _ in allv if o < 0))

def sub(d, keep):
    keep = np.asarray(sorted(keep), int)
    e = dict(d); e.update(off=d["off"][keep], R=d["R"][keep], gobs=d["gobs"][keep], elog=d["elog"][keep]); e["keep"] = tuple(keep.tolist())
    return e

_cache = {}
def penalties(d, foot, tag=""):
    """CFG402's per-galaxy penalties: chi2 at the law's a0 minus chi2 min over SC, f profiled on LF; None if < 4 points (dropped)."""
    if len(d["R"]) < 4:
        return None
    key = (d["g"], d["inc"], d.get("keep"), foot, tag)
    if key in _cache:
        return _cache[key]
    gb = gshape(d["R"], d["Rh"], d["bt"], d["fgas"])
    GN = gb[None, :] * 10 ** LF[:, None] * 1e11                     # (LF, n)
    lg, el = np.log10(d["gobs"]), d["elog"]
    def chi_at(a0s):                                                # a0s: 1-D array; returns min over f for each
        a0s = np.asarray(a0s, float)
        nu = np.where(a0s[:, None, None] == 0, 1.0, C4.nu_mono(GN[None] / np.where(a0s == 0, 1.0, a0s)[:, None, None]))
        return np.min(np.sum(((lg - np.log10(nu * GN[None])) / el) ** 2, axis=-1), axis=1)
    a0f = A0[foot]; prof = chi_at(a0f * SC); cmin = float(prof.min())
    z = d["z"]
    r = dict(DE=float(chi_at([a0f * de(z)])[0]) - cmin, RIVAL=float(chi_at([a0f * E(z)])[0]) - cmin, NEWTON=float(chi_at([0.0])[0]) - cmin,
             best=float(SC[int(np.argmin(prof))]), n=int(len(d["R"])))
    _cache[key] = r
    return r

def cls(S): return "REAL" if S >= 9 else ("WEAK" if S >= 4 else "NOISE")

def score(dsets, foot, tag=""):
    rowsg, S = {}, {"DE": 0.0, "RIVAL": 0.0, "NEWTON": 0.0}; dropped = []
    for g in GALS:
        r = penalties(dsets[g], foot, tag)
        if r is None:
            dropped.append(g); rowsg[g] = None; continue
        rowsg[g] = r
        for k in S: S[k] += r[k]
    return dict(rows=rowsg, S=S["DE"], S_RIVAL=S["RIVAL"], S_NEWTON=S["NEWTON"], cls=cls(S["DE"]), dropped=dropped)

def show(name, res):
    for foot in FOOTS:
        x = res[foot]
        P(f"  {name} | {foot}: S_DE {x['S']:.2f} ({x['cls']})  S_RIVAL {x['S_RIVAL']:.2f}  S_NEWTON {x['S_NEWTON']:.2f}  dropped {x['dropped'] or '-'}")
        for g in GALS:
            r = x["rows"][g]
            P(f"      {g:11s} " + ("DROPPED (< 4 points)" if r is None else f"n {r['n']:2d}  best a0 x{r['best']:.3f}  DE {r['DE']:6.2f}  RIVAL {r['RIVAL']:6.2f}  Newton {r['NEWTON']:6.2f}"))

P("CFG405 outskirt / inclination robustness of CFG402's residual tension" + ("  (MUTATE: errors halved in V0)" if MUT else ""))
P("=" * 100)
full = {g: build(g) for g in GALS}
outer = {g: int(np.argmax(np.abs(full[g]["off"]))) for g in GALS}

# ---- controls K1, K2
P("\nCONTROLS")
k2 = all(np.array_equal(full[g][k], data[g][k]) for g in GALS for k in ("R", "gobs", "elog"))
K("K2 identity: rebuild at Table 1 inclination equals CFG401's data bit for bit (R, g_obs, elog; all six)", k2, k2)
V0 = {f: score({g: sub(full[g], range(len(full[g]["R"]))) for g in GALS}, f) for f in FOOTS}
ref = open(os.path.join(D401, "cfg402.out")).read().split("stars-only")[0]
refrows = {}
for blk in ref.split("gas2Rd (primary) | ")[1:]:
    foot = blk.split()[0]
    refrows[foot] = {m.group(1): float(m.group(2)) for m in re.finditer(r"^\s+(\S+ \S+)\s+best a0 x[\d.]+ \| Delta chi2: DE\s+([-\d.]+)", blk, re.M)}
    refrows[foot]["SUM"] = float(re.search(r"SUM: DE ([-\d.]+)", blk).group(1))
k1d = max(abs(V0[f]["rows"][g]["DE"] - refrows[f][g]) for f in FOOTS for g in GALS)
k1s = max(abs(V0[f]["S"] - refrows[f]["SUM"]) for f in FOOTS)
K("K1 V0 reproduces CFG402 per-galaxy DE penalties (<= 0.01) and sums 7.99 / 9.63 (<= 0.01)", k1d <= 0.01 and k1s <= 0.01,
  f"max per-galaxy |diff| {k1d:.4f}; sums {V0['canonical']['S']:.4f} / {V0['alt']['S']:.4f}")

if MUT:
    half = {g: dict(sub(full[g], range(len(full[g]["R"])))) for g in GALS}
    for g in GALS: half[g]["elog"] = half[g]["elog"] / 2
    Vm = {f: score(half, f, "half") for f in FOOTS}
    ratios = {f: Vm[f]["S"] / V0[f]["S"] for f in FOOTS}
    ok = all(3 <= r <= 5 for r in ratios.values())
    K("MUTATE errors halved in V0: S must scale x3-x5 on both footings", ok, {f: round(r, 3) for f, r in ratios.items()})
    json.dump({"lane": "CFG405", "mutate": True, "ratios": ratios, "controls": controls}, open(os.path.join(MYDIR, "cfg405_results_MUTATE.json"), "w"), indent=1)
    open(os.path.join(MYDIR, "cfg405_MUTATE.out"), "w").write("\n".join(out_lines) + "\n")
    sys.exit(1)

# ---- K3 planted outskirt defect (planted on the canonical DE law; graded on canonical, alt reported)
plant = {}
for g in GALS:
    d = sub(full[g], range(len(full[g]["R"])))
    a0 = A0["canonical"] * de(d["z"])
    gb = gshape(d["R"], d["Rh"], d["bt"], d["fgas"])
    GN = gb[None, :] * 10 ** LF[:, None] * 1e11
    model = C4.nu_mono(GN / a0) * GN
    j = int(np.argmin(np.sum(((np.log10(d["gobs"]) - np.log10(model)) / d["elog"]) ** 2, axis=1)))
    gp = model[j].copy(); gp[outer[g]] *= 0.6
    d["gobs"] = gp; plant[g] = d
P0 = {f: score(plant, f, "plant") for f in FOOTS}
P1 = {f: score({g: sub(plant[g], [i for i in range(len(plant[g]["R"])) if i != outer[g]]) for g in GALS}, f, "plant") for f in FOOTS}
K("K3 planted outskirt defect: V0 S_plant >= 4 and V1 S_plant <= 0.5 (canonical, the planted footing)",
  P0["canonical"]["S"] >= 4 and P1["canonical"]["S"] <= 0.5,
  f"canonical {P0['canonical']['S']:.2f} -> {P1['canonical']['S']:.3f}; alt (reported) {P0['alt']['S']:.2f} -> {P1['alt']['S']:.3f}")
valid = all(c["pass"] for c in controls)

# ---- variants
keepV1 = {g: [i for i in range(len(full[g]["R"])) if i != outer[g]] for g in GALS}
keepV2 = {g: [i for i in range(len(full[g]["R"])) if abs(full[g]["off"][i]) <= min(full[g]["rp"], full[g]["rm"])] for g in GALS}
P("\nSELECTIONS (beyond-FWHM points; offsets in arcsec)")
for g in GALS:
    o = full[g]["off"]
    P(f"  {g:11s} n {len(o):2d}  r+ {full[g]['rp']:.3f}  r- {full[g]['rm']:.3f} | V1 drops {o[outer[g]]:+.3f} | V2 drops "
      + (", ".join(f"{o[i]:+.3f}" for i in range(len(o)) if i not in keepV2[g]) or "none"))
V = {"V0": V0}
V["V1"] = {f: score({g: sub(full[g], keepV1[g]) for g in GALS}, f) for f in FOOTS}
V["V2"] = {f: score({g: sub(full[g], keepV2[g]) for g in GALS}, f) for f in FOOTS}
for nm, di in (("V3-", -10), ("V3+", +10)):
    built = {g: build(g, min(85, max(10, T1[g][2] + di))) for g in GALS}
    V[nm] = {f: score({g: sub(built[g], range(len(built[g]["R"]))) for g in GALS}, f) for f in FOOTS}
b4 = {g: (build(g, 54.5) if g == "zC 400569" else full[g]) for g in GALS}
V["V4 (reported)"] = {f: score({g: sub(b4[g], range(len(b4[g]["R"]))) for g in GALS}, f) for f in FOOTS}
P("\nVARIANTS (CFG402 statistic; primary shape)")
for nm, res in V.items():
    show(nm, res)

# ---- nulls
def null(seed, picker, ndraw=200):
    rng = np.random.default_rng(seed); S = {f: [] for f in FOOTS}
    for _ in range(ndraw):
        ds = {g: sub(full[g], picker(g, rng)) for g in GALS}
        for f in FOOTS:
            S[f].append(score(ds, f)["S"])
    return {f: np.array(v) for f, v in S.items()}
def pick1(g, rng):
    cand = [i for i in range(len(full[g]["R"])) if i != outer[g]]
    j = int(rng.choice(cand)); return [i for i in range(len(full[g]["R"])) if i != j]
short = set()
def pick2(g, rng):
    n = len(full[g]["R"]); k = n - len(keepV2[g]); kept = keepV2[g]
    keff = min(k, max(len(kept) - 4, 0))
    if keff < k: short.add((g, k, keff))
    if keff == 0: return list(range(n))
    drop = set(int(x) for x in rng.choice(kept, size=keff, replace=False)); return [i for i in range(n) if i not in drop]
N1 = null(405, pick1); N2 = null(4052, pick2)
P("\nNULLS (200 draws each)")
special = {}
for nm, N, Vn in (("N1 (vs V1)", N1, "V1"), ("N2 (vs V2)", N2, "V2")):
    sp = all(V[Vn][f]["S"] < np.percentile(N[f], 5) for f in FOOTS)
    special[Vn] = sp
    for f in FOOTS:
        q = np.percentile(N[f], [5, 16, 50, 84, 95])
        P(f"  {nm} | {f}: {Vn} S {V[Vn][f]['S']:.2f} vs null pct 5/16/50/84/95 = " + " / ".join(f"{x:.2f}" for x in q)
          + f"; frac of null <= {Vn}: {np.mean(N[f] <= V[Vn][f]['S']):.3f}")
    P(f"  -> {Vn} SPECIAL: {sp}")
for g, k, keff in sorted(short):
    P(f"  N2 note: {g} V2 drops {k}, null drops {keff} (4-point rule)")

# ---- reading
graded = ["V1", "V2", "V3-", "V3+"]
noise = {v: [f for f in FOOTS if V[v][f]["cls"] == "NOISE"] for v in graded}
if not valid:
    reading = "INVALID (a control failed; nothing is read)"
elif all(len(noise[v]) == 2 for v in ("V1", "V2")) and special["V1"] and special["V2"]:
    reading = "OUTSKIRT-DRIVEN"
elif not any(noise[v] for v in graded):
    reading = "ROBUST"
else:
    hit = [v for v in graded if noise[v]]
    note = []
    if set(hit) <= {"V3-", "V3+"}: note.append("inclination-sensitive")
    if any(v in hit for v in ("V1", "V2")) and not all(special[v] for v in ("V1", "V2") if v in hit): note.append("point-count-sensitive, not outskirt-specific")
    reading = "FRAGILE, NOT ATTRIBUTED (NOISE in: " + ", ".join(f"{v} [{'/'.join(noise[v])}]" for v in hit) + (("; " + "; ".join(note)) if note else "") + ")"
P("\nREADING (frozen): " + reading)
P(f"  zC 406690 DE penalty by variant (canonical / alt): " + "; ".join(
    f"{v} " + " / ".join("drop" if V[v][f]["rows"]["zC 406690"] is None else f"{V[v][f]['rows']['zC 406690']['DE']:.2f}" for f in FOOTS) for v in V))
P(f"\n{sum(c['pass'] for c in controls)}/{len(controls)} controls pass")

json.dump({"lane": "CFG405", "mutate": False, "controls": controls, "valid": valid, "reading": reading,
           "variants": {v: {f: {k: x[k] for k in ("S", "S_RIVAL", "S_NEWTON", "cls", "dropped", "rows")} for f, x in r.items()} for v, r in V.items()},
           "plant": {"V0": {f: P0[f]["S"] for f in FOOTS}, "V1": {f: P1[f]["S"] for f in FOOTS}},
           "nulls": {nm: {f: {"pct": dict(zip(["5", "16", "50", "84", "95"], np.percentile(N[f], [5, 16, 50, 84, 95]).tolist())), "draws": N[f].tolist()} for f in FOOTS}
                     for nm, N in (("N1", N1), ("N2", N2))},
           "special": special, "selections": {g: {"off": full[g]["off"].tolist(), "V1_keep": keepV1[g], "V2_keep": keepV2[g]} for g in GALS}},
          open(os.path.join(MYDIR, "cfg405_results.json"), "w"), indent=1)
open(os.path.join(MYDIR, "cfg405.out"), "w").write("\n".join(out_lines) + "\n")
sys.exit(0 if valid else 2)
