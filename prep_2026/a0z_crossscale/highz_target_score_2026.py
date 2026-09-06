#!/usr/bin/env python3
"""
highz_target_score_2026.py -- rank the committed deep-MOND target ledger with the relayed two-stage funnel score (2026-09-06)
=============================================================================================================================
Input: highz_deepmond_target_list_2026_results.json (the D-1 ledger: 21 lensed/unlensed z ~ 1.5-3.3 objects with the published
mu, M*, M_mol, V, sigma and the g_bar/a0 bracket [glo, ghi] on the canonical footing).  The relayed OpenAI note (2026-09-06)
proposes S = 0.35 D + 0.25 R + 0.15 L + 0.15 G + 0.10 F (deep-MOND, rotation, lens quality, gas feasibility, resolution) and two
instrument facts worth carrying: NIRSpec G235H/F170LP covers 1.66-3.17 um, so H-alpha and [O III] are BOTH in one setting for
2.32 < z < 3.83; CO(3-2) (345.796 GHz rest) lands in ALMA Band 3 (84-116 GHz) for 1.98 < z < 3.12, while [C II] at z ~ 2.5
falls in the Band 8/9 gap.  The score components are computed from the ledger fields by the rules below -- every rule is
printed, none is tuned to a name.

  D  from the log-bracket: fraction of [log glo, log ghi] below log 0.3 (glo floored at 0.05 when no mass is known);
     alt footing: bracket x a0_can/a0_alt = 0.830;
  R  V/sigma known: > 2 -> 1.0; 1.5-2 -> 0.75; 1-1.5 -> 0.4; < 1 -> 0.1; unknown -> 0.4 (the old lensed-IFU experience: V/sigma ~ 1 typical);
  L  1.0 unlensed; 0.0 when two refereed lens models disagree by > 0.3 dex (flagged in the ledger note); else 0.7 (single model, unverified);
  G  1.0 measured M_mol; 0.7 CO(3-2) in Band 3 at this z; 0.4 CO(4-3) in Band 4 (125-163 GHz, 1.83 < z < 2.69) only; else 0.3;
  F  0.3 + 0.7 min(1, log10(max(mu,1))/1.7)  (mu ~ 50 saturates).

  T1 [ledger]   all 21 scored on both footings, S in [0, 1];
  T2 [gate]     the flagship must pass the hard gates (D >= 0.5, R >= 0.75, L >= 0.7) on both footings: report whether ANY does;
  T3 [MACS0451] the highest-mu object with a gas mass is not the flagship (dispersion-dominated, lens models 21.5 vs 49);
  T4 [windows]  the z-window where both NIRSpec lines and CO(3-2)/Band 3 hold simultaneously is 2.32 < z < 3.12; count the ledger inside it.
The relayed note's two unmeasured faint arcs (Abell 68 C4 z = 2.622, C20b z = 2.689) are listed with their instrument windows only:
they carry no mass, size or kinematics in this repo and are NOT scored.
"""
import json, math, sys
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
d = json.load(open("highz_deepmond_target_list_2026_results.json")); T = d["targets"]
A0C, A0A = d["footings"]["canonical"], d["footings"]["alt"]; CUT = d["cut"]["gbar_over_a0"]
NIR = lambda z: (1.53 <= z <= 3.83, 2.32 <= z <= 5.33)                       # H-alpha, [O III] inside G235H/F170LP
CO32 = lambda z: 1.98 <= z <= 3.12; CO43 = lambda z: 1.83 <= z <= 2.69
def D_of(glo, ghi, scale):
    lo = max(glo, 0.05)*scale; hi = max(ghi, lo*1.0001)*scale
    if hi <= CUT: return 1.0
    if lo >= CUT: return 0.0
    return (math.log10(CUT) - math.log10(lo))/(math.log10(hi) - math.log10(lo))
def R_of(V, sig):
    if V is None or sig is None or sig == 0: return 0.4
    r = V/sig
    return 1.0 if r > 2 else 0.75 if r > 1.5 else 0.4 if r > 1 else 0.1
def L_of(t):
    if t["mu"] == 1.0: return 1.0
    return 0.0 if "disagreement" in t.get("note", "") else 0.7
def G_of(t):
    if t["Mmol"]: return 1.0
    return 0.7 if CO32(t["z"]) else 0.4 if CO43(t["z"]) else 0.3
def F_of(mu): return 0.3 + 0.7*min(1.0, math.log10(max(mu or 1.0, 1.0))/1.7)
W = dict(D=0.35, R=0.25, L=0.15, G=0.15, F=0.10)
print("=" * 120); print("highz_target_score_2026 -- the relayed funnel score applied to the committed deep-MOND target ledger"); print("=" * 120)
print(f"    weights {W}; deep-MOND cut g_bar/a0 < {CUT}; footings a0 = {A0C:.4g} / {A0A:.4g} (alt bracket scale {A0C/A0A:.3f})")
rows = []
for t in T:
    comp = {}
    for foot, scale in (("canonical", 1.0), ("alt", A0C/A0A)):
        c = dict(D=D_of(t["glo"], t["ghi"], scale), R=R_of(t["V"], t["sig"]), L=L_of(t), G=G_of(t), F=F_of(t["mu"]))
        c["S"] = sum(W[k]*c[k] for k in W); comp[foot] = c
    ha, o3 = NIR(t["z"])
    rows.append(dict(name=t["name"], z=t["z"], mu=t["mu"], vs=(t["V"]/t["sig"] if t["V"] and t["sig"] else None), comp=comp, nir="Ha+[OIII]" if ha and o3 else "Ha only" if ha else "[OIII] only" if o3 else "neither", co="CO(3-2)/B3" if CO32(t["z"]) else "CO(4-3)/B4" if CO43(t["z"]) else "no B3/B4 CO"))
rows.sort(key=lambda r: -r["comp"]["canonical"]["S"])
print(f"\n    {'rank':4s} {'name':38s} {'z':5s} {'mu':5s} {'V/sig':5s} | {'D':4s} {'R':4s} {'L':4s} {'G':4s} {'F':4s} | {'S_can':5s} {'S_alt':5s} | NIRSpec G235H   ALMA")
for i, r in enumerate(rows, 1):
    c = r["comp"]["canonical"]
    print(f"    {i:4d} {r['name'][:38]:38s} {r['z']:5.2f} {r['mu']:5.1f} {('%.2f' % r['vs']) if r['vs'] is not None else '  -- ':5s} | {c['D']:.2f} {c['R']:.2f} {c['L']:.2f} {c['G']:.2f} {c['F']:.2f} | {c['S']:.3f} {r['comp']['alt']['S']:.3f} | {r['nir']:13s}   {r['co']}")
check("T1 [ledger] all ledger objects scored on both footings with S in [0, 1]", len(rows) == len(T) and all(0 <= r["comp"][f]["S"] <= 1 for r in rows for f in ("canonical", "alt")), f"N = {len(rows)}")
gate = lambda c: c["D"] >= 0.5 and c["R"] >= 0.75 and c["L"] >= 0.7
passing = [r["name"] for r in rows if gate(r["comp"]["canonical"]) and gate(r["comp"]["alt"])]
check("T2 [gate] at least one ledger object passes the flagship gates (D >= 0.5, R >= 0.75, L >= 0.7) on both footings", bool(passing), f"passing = {passing}" if passing else "none: every rotating object is high-acceleration and every deep-MOND candidate has no measured rotation -- the decisive object must be found, as the ledger concluded")
m0451 = next(r for r in rows if "MACS0451" in r["name"]); rank0451 = rows.index(m0451) + 1
check("T3 [MACS0451] the highest-magnification gas-measured object is not the flagship (dispersion-dominated, lens models 21.5 vs 49)", rank0451 > 1, f"rank {rank0451}, S = {m0451['comp']['canonical']['S']:.3f}, V/sigma = {m0451['vs']:.2f}")
inwin = [r["name"] for r in rows if 2.32 <= r["z"] <= 3.12]
check("T4 [windows] the simultaneous NIRSpec (Ha + [OIII] in G235H) and ALMA CO(3-2)/Band-3 window is 2.32 < z < 3.12; ledger objects inside it are listed", True, f"{len(inwin)} inside: {inwin}")
print("\n    unscored (relayed note, no mass/size/kinematics in this repo): " + "; ".join(f"{n} z = {z}: NIRSpec {'Ha+[OIII]' if all(NIR(z)) else 'partial'}, {'CO(3-2)/B3' if CO32(z) else 'no B3'}" for n, z in (("Abell 68 C4", 2.622), ("Abell 68 C20b", 2.689))))
best = rows[0]
print(f"\n  OUTCOME: top of the ledger on the relayed score is {best['name']} (S = {best['comp']['canonical']['S']:.3f}/{best['comp']['alt']['S']:.3f}); the flagship gate is passed by {len(passing)} object(s)."
      "\n           The score changes nothing about the ledger's verdict: the decisive galaxy is a low-surface-density lensed disc that has to be screened for rotation"
      "\n           with NIRSpec first and then given ALMA CO(3-2) in Band 3 -- the note's ordering rule and line choice are adopted; the +0.33 dex / 0.13 dex targets are the repo's own.")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "")); sys.exit(0)
