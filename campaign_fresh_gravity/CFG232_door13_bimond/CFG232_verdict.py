#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG232_verdict -- reads the CFG232_*.json outputs and prints the gate table per sub-variant (no physics).  Each cell cites its script and verdict key."""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    p = os.path.join(HERE, f"CFG232_{name}.json")
    if not os.path.exists(p):
        return None
    with open(p) as f:
        return json.load(f)


def V(script, key, default="NOT RUN"):
    j = load(script)
    if not j:
        return default
    return j.get("numbers", {}).get("verdicts", {}).get(key, {}).get("status", default)


def ck(script, name_frag):
    j = load(script)
    if not j:
        return None
    for c in j["checks"]:
        if name_frag in c["name"]:
            return c
    return None


def short(s, n=70):
    return s if len(s) <= n else s[: n - 3] + "..."


A1, A2, A3, A4, A5, A6, A7, A8 = ("A1_static_reduction", "A2_spectrum", "A3_cold_coupling", "A4_cosmology", "A5_lambda_tie", "A6_solar_system", "A7_scalar_tensor_13c", "A8_energy")

rows = [
    ("G1-law (law target nu(g_N) g_N)", [f"{short(V(A1, 'G1-law'))} [A1]"] * 3 + [f"{short(V(A7, 'G1-law 13c'))} [A7]"]),
    ("G1-law vs CFG44 C(r) target", ["FAIL on the exponential sphere at M_b <= 1e11 (up to 0.50 P2; 0.54 nu_mono) [A1 B.3b]"] * 3 + ["same (law depends on g_N alone) [A1/A7]"]),
    ("G1-C (c-g)", [f"{V(A3, 'G1-C 13a/13b (c-g)')} [A3]"] * 3 + [f"{V(A3, 'G1-C 13c')} [A3]"]),
    ("G1-C (c-ghat)", [f"{V(A3, 'G1-C 13a/13b (c-gh)')} [A3]"] * 3 + ["n/a (cold in Einstein frame / conformal: both FAIL) [A3]"]),
    ("G1-mechanism", [f"{short(V(A1, 'G1-mechanism'), 60)} [A1]"] * 3 + ["M1-inv [A7]"]),
    ("G2", ["UNDEFINED (no B=0 branch; Q<0 needs a continuation); growth estimate FAIL [A4]", "UNDEFINED; growth estimate FAIL [A4]", "UNDEFINED [A4]", "FAIL on the nonlinear estimate (linear theory strongly coupled: UNDEFINED) [A7]"]),
    ("G3 reaction", [f"PASS* (c-g) / FAIL (c-ghat) [A3]"] * 3 + ["PASS* [A3]"]),
    ("G3 energy", [f"{V(A8, 'G3 energy (13a/13b/13c-analogue, field-side)')} (up to 253x orbital energy in |E_int|; E_rel excess 1.2-2.8x, sign of E_int negative) [A8]"] * 3 + ["FAIL by the (2/3)ln(r_e/r_M) indicator (>=1.8) [A8 hand column]"]),
    ("G4 strict", [f"{V(A5, 'G4 13a')} [A5]", f"{V(A5, 'G4 13b-i strict')} [A5]", f"{V(A5, 'G4 13b-ii strict')} [A5]", f"{V(A5, 'G4 13c')} [A5]"]),
    ("G4 a0-Lambda tie", ["not tied [A5]", "written in (rule T), Lambdah = Lambda_g by hand [A5]", "native but inverted (a0 primary, kappa = value of M at 0), derived kappa^2 = -16 pi beta/(sigma_s M0) [A5]", "not tied [A5]"]),
    ("G5a well-posedness", [f"{V(A2, 'G5a (13a/13b, flat and static-MOND: REPRODUCTION)')} (reproduction) + FRW background: {V(A4, 'G5a (13b, FRW background: NEW)')} [A2, A4]"] * 3 + [f"{short(V(A7, 'G5a 13c (static branch)'), 60)} [A7]"]),
    ("G5b Q2 (bare law)", [f"{V(A6, 'G5b Q2 (13a/13b/13c as a bare law)')} (Sun at Saturn 6e3-1.6e4 x bound) [A6]"] * 4),
    ("G5b gamma", [f"{V(A6, 'G5b gamma')} (Psi'/Phi'-1 = -5e-7) [A6]"] * 3 + ["PASS (same slip order, analytic + A6 law-level) [A6]"]),
    ("G5c c_T", ["UNDEFINED for the relative TT modes (kinetic term vanishes at the tuned point); sum graviton c=1 [A2]"] * 3 + ["PASS (analytic: EH + conformal scalar) [not scripted]"]),
    ("G7 frame/background", [f"{V(A4, 'G7 (frozen rule: differs between readings)')} (R-static PASS; R-add FAIL) [A4]"] * 3 + ["PASS (analytic: X is a gradient scalar; not scripted)"]),
]
hdr = ["gate", "13a", "13b-i", "13b-ii", "13c"]
print("GATE TABLE (each cell cites its script; see README.md for the reading of every cell)\n")
for r in rows:
    print(f"- {r[0]}")
    for name, cell in zip(hdr[1:], r[1]):
        print(f"    {name:7s}: {cell}")
out = {r[0]: dict(zip(hdr[1:], r[1])) for r in rows}
with open(os.path.join(HERE, "CFG232_verdict.json"), "w") as f:
    json.dump(out, f, indent=1)
# control ledger
print("\nCONTROL LEDGER (main runs)")
for s in (A1, A2, A3, A4, A5, A6, A7, A8):
    j = load(s)
    if not j:
        print(f"  {s}: NOT RUN"); continue
    bad = [c["name"][:110] for c in j["checks"] if c["kind"] == "control" and not c["ok"]]
    print(f"  {s}: {len(j['checks'])} checks, control failures: {bad if bad else 'none'}")
print("\nMUTATE ledger")
for fn in sorted(os.listdir(HERE)):
    if "_MUTATE_" in fn and fn.endswith(".json"):
        with open(os.path.join(HERE, fn)) as f:
            j = json.load(f)
        print(f"  {j['slug']}: {'BITES' if j.get('control_bites') else 'DOES NOT BITE (declared control failure)'}")
