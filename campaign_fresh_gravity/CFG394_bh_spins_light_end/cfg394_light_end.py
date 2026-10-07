#!/usr/bin/env python3
"""CFG394 -- BH spins near 1e9 Msun vs the light end (2.0-4.4e-20 eV) of the wave-field window.
Frozen: FROZEN_CRITERIA.md (5aff6a7ba). Executes CFG367's committed cfg367_superradiance.py byte-for-byte
(sha256 check) with __file__ pointed at a run directory under runs/, so it reads that directory's
bh_spins_reynolds2021.csv and writes its outputs there. Inputs: spins_compiled_3e8_3e9.csv (per-measurement,
transcribed by position), comb_updates.csv (2019-2026 re-measurements of CFG367 rows, R2 lowest edge)."""
import os, csv, json, math, hashlib, shutil, contextlib, io

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "CFG367_superradiance_window")
CODE_SHA = "d78a38121a865094d8d333108533bd67e378f6c7aabc0ad6edcf74ae8bb0237e"
CSV_SHA = "6b3b1c496c4194b7bbe453baf07ab87287c6499608b65b5c6dd5c91f5d41d963"
LIGHT = (2.012653280876046e-20, 4.3452552089909754e-20)   # CFG367 committed surviving[0]
FIELDS = ["set", "name", "mass_1e6", "err_lo", "err_hi", "approx", "spin_lo", "spin_text"]
LOG, CH, OUT = [], [], {"lane": "CFG394", "frozen": "5aff6a7ba", "light_end": LIGHT}


def P(s=""):
    print(s); LOG.append(s)


def check(n, ok, v=""):
    CH.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {n} {v}")


code = open(os.path.join(SRC, "cfg367_superradiance.py"), "rb").read()
check("C0 CFG367 code sha256 identical", hashlib.sha256(code).hexdigest() == CODE_SHA, hashlib.sha256(code).hexdigest()[:16])
if hashlib.sha256(code).hexdigest() != CODE_SHA:
    raise SystemExit("code hash mismatch: stop (frozen rule)")


def run(tag, rows, mutate=False, csv_bytes=None):
    d = os.path.join(HERE, "runs", tag); os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "bh_spins_reynolds2021.csv")
    if csv_bytes is not None:
        open(p, "wb").write(csv_bytes)
    else:
        with open(p, "w", newline="") as f:
            w = csv.DictWriter(f, FIELDS); w.writeheader(); [w.writerow(r) for r in rows]
    os.environ["CFG367_MUTATE"] = "1" if mutate else "0"
    ns = {"__file__": os.path.join(d, "cfg367_superradiance.py"), "__name__": "__main__"}
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            exec(compile(code, ns["__file__"], "exec"), ns); rc = 0
        except SystemExit as e:
            rc = e.code
    os.environ["CFG367_MUTATE"] = "0"
    res = json.load(open(os.path.join(d, "cfg367_superradiance" + ("_MUTATE" if mutate else "") + "_results.json")))
    check(f"C2 [{tag}{' MUTATE' if mutate else ''}] CFG367 internal checks pass (exit {rc})", rc == 0)
    return res, ns


def overlap(ivs, lo, hi):
    return [(max(a, lo), min(b, hi)) for a, b in ivs if b >= lo and a <= hi]


def surv(ivs, lo, hi):
    out, cur = [], lo
    for a, b in sorted(overlap(ivs, lo, hi)):
        if a > cur: out.append((cur, a))
        cur = max(cur, b)
    if cur < hi: out.append((cur, hi))
    return out


def fmt(iv):
    return "; ".join(f"[{a:.2e}, {b:.2e}]" for a, b in iv) or "none"


# ---- C1: CFG367 reproduces from its own CSV (byte-identical copy)
cb = open(os.path.join(SRC, "bh_spins_reynolds2021.csv"), "rb").read()
check("C1a CFG367 CSV sha256 identical", hashlib.sha256(cb).hexdigest() == CSV_SHA)
ref = json.load(open(os.path.join(SRC, "cfg367_superradiance_results.json")))
ctl, NS = run("CONTROL_CFG367", None, csv_bytes=cb)
check("C1 control reproduces CFG367 committed intervals exactly (smbh, xrb, primary, primary+secondary, per_object)",
      all(ctl[k] == ref[k] for k in ("smbh", "xrb", "primary", "primary+secondary", "per_object")))

# ---- compile: R1/R2 lower edges, tiers
comp = list(csv.DictReader(open(os.path.join(HERE, "spins_compiled_3e8_3e9.csv"))))


def lower_edge(r):
    k, v = r["spin_kind"], float(r["spin_val"])
    if k == "i90": return v - float(r["spin_elo"])
    if k == "i1s": return v - 1.645 * float(r["spin_elo"])
    if k == "ll": return v
    if k == "ul": return 0.0          # an upper limit sets no floor
    raise ValueError(k)


objs = {}
for r in comp:
    if r["used"] != "1": continue
    o = objs.setdefault(r["name"], {"r": r, "edges": []}); o["edges"].append((max(lower_edge(r), 0.0), r["spin_ref"], r["spin_model"]))
tierA, tierB, table = [], [], []
P("\nCOMPILATION (S2: 3e8 <= M <= 3e9 Msun; R2 lowest lower edge across accepted models/papers)")
for n, o in objs.items():
    r = o["r"]; c = float(r["mass_1e6"]); lo = min(o["edges"])
    if lo[0] >= 0.5 and r["mass_method"] in ("reverberation", "dynamical"):
        tier = "A"; row = dict(set="smbh", name=n, mass_1e6=c, err_lo=r["mass_elo_1e6"], err_hi=r["mass_ehi_1e6"], approx=0, spin_lo=round(lo[0], 4), spin_text=f"R2 lowest ({lo[1]})")
        tierA.append(row)
    elif lo[0] >= 0.5:
        tier = "B"; row = dict(set="smbh", name=n, mass_1e6=c, err_lo=round(c * (1 - 10**-0.4), 3), err_hi=round(c * (10**0.4 - 1), 3), approx=0, spin_lo=round(lo[0], 4), spin_text=f"R2 lowest ({lo[1]}); mass 0.4 dex (R4)")
        tierB.append(row)
    else:
        tier = "FAIL"
    why = {"A": "robust", "B": f"spin ok, mass {r['mass_method']} -> indicative", "FAIL": f"lowest lower edge {lo[0]:.3f} < 0.5 ({lo[1]}: {lo[2]})"}[tier]
    table.append(dict(name=n, M=c * 1e6, method=r["mass_method"], edges=[(round(e, 3), a, b) for e, a, b in o["edges"]], lowest=lo[0], tier=tier, why=why))
    P(f"  {n:12s} M={c * 1e6:.2e} ({r['mass_method']}); edges {[round(e[0], 3) for e in o['edges']]} -> lowest {lo[0]:.3f}; TIER {tier}: {why}")
OUT["compilation"] = table

# ---- alpha values at the light end for each compiled object (central mass and CFG367 mass_range as run)
P("\nALPHA at the light-end edges (alpha = 7.49e9 M m); Omega_H(a_lo) = l=1 superradiance ceiling")
al = {}
for t in table:
    a_lo = t["lowest"]; rp = 1 + math.sqrt(max(1 - a_lo**2, 0)); OH = a_lo / (2 * rp)
    al[t["name"]] = {"alpha_2.0e-20": NS["ALPHA_K"] * t["M"] * LIGHT[0], "alpha_4.35e-20": NS["ALPHA_K"] * t["M"] * LIGHT[1], "Omega_H": OH}
    P(f"  {t['name']:12s} alpha {al[t['name']]['alpha_2.0e-20']:.3f} .. {al[t['name']]['alpha_4.35e-20']:.3f}; Omega_H(a_lo={a_lo:.2f}) = {OH:.3f}")
OUT["alpha"] = al

# ---- runs
for tag, rows in (("RUN_A", tierA), ("RUN_AB", tierA + tierB)):
    res, _ = run(tag, rows)
    ex = overlap(res["primary"]["excluded_in_window"], *LIGHT); sv = surv(res["primary"]["excluded_in_window"], *LIGHT)
    v = "LIGHT END CLOSED" if not sv else ("NARROWED" if ex else "STAYS OPEN")
    OUT[tag] = {"n_objects": len(rows), "objects": [r["name"] for r in rows], "excluded_light": ex, "surviving_light": sv, "verdict": v,
                "excluded_full_window": res["primary"]["excluded_in_window"], "per_object": res["per_object"]}
    P(f"\n{tag} ({len(rows)} objects: {', '.join(r['name'] for r in rows) or 'none'}): light end excluded {fmt(ex)}; surviving {fmt(sv)}; VERDICT {v}"
      + ("" if tag == "RUN_A" else " (indicative)"))
    for n, iv in res["per_object"].items():
        P(f"     {n}: excludes {fmt(iv)}")

mres, _ = run("RUN_AB", tierA + tierB, mutate=True)
check("MUTATE spins 0 on RUN_AB list -> union empty", not mres["smbh"] and not mres["xrb"])

# RUN_COMB: CFG367 rows, 2019-2026 re-measurements replace the spin (never add), plus new TIER A rows
upd = {r["name"]: r for r in csv.DictReader(open(os.path.join(HERE, "comb_updates.csv")))}
base = list(csv.DictReader(open(os.path.join(SRC, "bh_spins_reynolds2021.csv"))))
comb, seen = [], set()
for r in base:
    r = dict(r)
    if r["name"] in upd:
        seen.add(r["name"]); r["spin_text"] = f"was {r['spin_lo']}; {upd[r['name']]['basis']}"; r["spin_lo"] = upd[r["name"]]["new_spin_lo"]
    comb.append(r)
check("COMB: every update matched a CFG367 row by name", seen == set(upd), f"{sorted(set(upd) - seen)}")
comb += [r for r in tierA if r["name"] not in {b["name"] for b in base}]
res, _ = run("RUN_COMB", comb)
for key in ("primary", "primary+secondary"):
    ex = overlap(res[key]["excluded_in_window"], *LIGHT); sv = surv(res[key]["excluded_in_window"], *LIGHT)
    OUT[f"RUN_COMB_{key}"] = {"excluded_light": ex, "surviving_light": sv, "excluded_in_window": res[key]["excluded_in_window"], "surviving": res[key]["surviving"]}
P(f"\nRUN_COMB (CFG367 rows, {len(upd)} spins superseded by 2019-2026 lowest edges; indicative):")
P(f"  primary excluded in window: {fmt(res['primary']['excluded_in_window'])}")
P(f"  primary surviving pieces:   {fmt(res['primary']['surviving'])}")
P(f"  CFG367 primary excluded was: {fmt(ref['primary']['excluded_in_window'])}")
OUT["RUN_COMB_per_object_low"] = {n: iv for n, iv in res["per_object"].items() if iv and iv[0][0] < 3e-19}

# ---- decider: hypothetical single hole, same CFG367 functions (mass_range + excluded), 9-point mass grid
P("\nDECIDER (hypothetical hole run through CFG367's own mass_range/excluded; fraction of [2.01e-20, 4.35e-20] excluded)")
import numpy as np
mg = np.logspace(math.log10(LIGHT[0]), math.log10(LIGHT[1]), 200); dec = []
for M9 in (0.6, 0.8, 1.0, 1.2, 1.5, 2.0):
    for e in (0.1, 0.2, 0.3):
        for a in (0.7, 0.9, 0.98):
            r = dict(set="smbh", mass_1e6=str(M9 * 1e3), err_lo=str(e * M9 * 1e3), err_hi=str(e * M9 * 1e3), approx="0")
            lo, hi = NS["mass_range"](r); Ms = np.logspace(math.log10(lo), math.log10(hi), 9)
            mask = np.array([all(NS["excluded"](m, M, a, NS["TAU"]["smbh"]) for M in Ms) for m in mg])
            ex = [(float(mg[i]), float(mg[i])) for i in np.where(mask)[0]]
            dec.append(dict(M=M9 * 1e9, frac_err_1sig=e, a_lo=a, frac_excluded=float(mask.mean()),
                            lo=float(mg[mask][0]) if mask.any() else None, hi=float(mg[mask][-1]) if mask.any() else None))
for d in dec:
    if d["frac_excluded"] > 0:
        P(f"  M={d['M']:.1e} +/-{d['frac_err_1sig']:.0%} (1sig) a>={d['a_lo']}: excludes {d['frac_excluded']:.0%} [{d['lo']:.2e}, {d['hi']:.2e}]")
OUT["decider"] = dec
full = [d for d in dec if d["frac_excluded"] > 0.99]
P(f"  configurations closing the whole light end alone: {len(full)}")

P(f"\n{sum(CH)}/{len(CH)} checks pass")
open(os.path.join(HERE, "cfg394_light_end.out"), "w").write("\n".join(LOG) + "\n")
json.dump(OUT, open(os.path.join(HERE, "cfg394_light_end_results.json"), "w"), indent=1)
raise SystemExit(0 if all(CH) else 1)
