#!/usr/bin/env python3
"""RM1 read, per FROZEN_CRITERIA.md. Exit 1 if a check fails. RM1_MUTATE=1 reads the twin. f, delta FITTED; kappa = 1/2 FITTED, unused; not theory closed."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); T = ("A_c2b_refit", "B_cfg886_bg"); MUT = os.environ.get("RM1_MUTATE") == "1"; OUT = []
def P(s): print(s); OUT.append(s)
U = json.load(open(os.path.join(H, "..", "UR2_response_mass_pinch", "ur2_results.json")))["rows"]
def gates(r):
    s = r["sparc"]; g = r["groups"]
    return dict(U=all(0.5 <= s[t]["U"] <= 0.8 and s[t]["rms"] <= 0.110 for t in T), tilt=all(abs(s[t]["tilt"]) <= 0.15 for t in T), groups=g.get("verdict") == "CONSISTENT", lt=all(abs(r["lt"][t]) <= 0.10 for t in T), mass=-0.10 - 1e-9 <= r["delta"] <= 0.14)
def close(a, b, tol): return max(abs(a["sparc"][t][q] - b["sparc"][t][q]) for t in T for q in ("U", "rms")) <= tol
if MUT:
    R = json.load(open(os.path.join(H, "rm1_MUTATE_results.json")))["rows"]; k1 = close(R["G1.0|+0.00"], U["blum|+0.00"], 1e-6); P(f"MUTATE K1 f 1 vs UR2 Blumenthal: {'PASS' if k1 else 'FAIL'}"); open(os.path.join(H, "rm1_MUTATE.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if k1 else 1)
RG, RI = (json.load(open(os.path.join(H, f"rm1_{p}_results.json"))) for p in "GI"); rows = {**RG["rows"], **RI["rows"]}; clu = {**RG["clusters"], **RI["clusters"]}
labs = sorted({k.split("|")[0] for k in rows}, key=lambda s: (s[0], -float(s[1:]))); ds = sorted({r["delta"] for r in rows.values()})
pas = {}; best = None
for lab in labs:
    P(f"\n{lab}: keys {clu[lab]['n']} bad {clu[lab]['bad']} X-COP {clu[lab]['xcop']['mean']:+.3f}, {clu[lab]['xcop']['rms']:.3f}\n  delta U_A/U_B rms tilt_A/B groupsZ verdict LT_A/B failed")
    for d in ds:
        r = rows[f"{lab}|{d:+.2f}"]; G = gates(r); s = r["sparc"]; g = r["groups"]; bad = [k for k, v in G.items() if not v]
        P(f"  {d:+.2f} {s[T[0]]['U']:.2f}/{s[T[1]]['U']:.2f} {s[T[0]]['rms']:.4f} {s[T[0]]['tilt']:+.2f}/{s[T[1]]['tilt']:+.2f} {g.get('Z', g.get('z', float('nan'))):+.2f} {g.get('verdict')} {r['lt'][T[0]]:+.3f}/{r['lt'][T[1]]:+.3f} {','.join(bad) or 'ALL CLEAR'}")
        if not bad: pas.setdefault(lab[0], []).append(f"{lab}|{d:+.2f}")
        if best is None or len(bad) < best[0]: best = (len(bad), lab, d, bad)
P(f"\nCells clearing all five: G {pas.get('G', [])}; I {pas.get('I', [])}")
P(f"Fewest gates failed (first met): {best[0]} at {best[1]}, delta {best[2]:+.2f}: {best[3]}; Upsilon by V_flat (A): " + ", ".join(f"{k} {v:.2f}" for k, v in rows[f'{best[1]}|{best[2]:+.2f}']['sparc'][T[0]]['bins'].items()))
L = "CELLS IN G" if pas.get("G") else "CELLS IN I ONLY" if pas.get("I") else "NO CELL"
k1 = close(rows["G1.0|+0.00"], U["blum|+0.00"], 1e-6); k2 = close(rows["G0.0|+0.00"], U["off|+0.00"], 1e-3); m = rows["G0.5|+0.00"]["sparc"][T[0]]["U"]; k3 = m not in (rows["G1.0|+0.00"]["sparc"][T[0]]["U"], rows["G0.0|+0.00"]["sparc"][T[0]]["U"])
P(f"\n=== LABEL: {L} [NOISE-LIMITED ANCHOR: NR1 PRIMARY only, NR2 unread]\nK1 {k1}; K2 {k2}; K3 {k3}")
open(os.path.join(H, "rm1.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if k1 and k2 and k3 else 1)
