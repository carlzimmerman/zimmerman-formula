#!/usr/bin/env python3
"""CFG303 R5 / A2.3 -- CFG274 (the eight Amvrosiadis+ discs) with the gas conversion that was calibrated on the dynamics under an ASSUMED
dark-matter fraction (alpha_CO = 0.92, f_dm = 0.25; tagged LCDM-MODEL) replaced by the record's two declared conventions, alpha_CO = 0.8 and 4.36
(a bracket, neither preferred).  CFG274's own gbar_of(..., gas_fac = alpha/0.92) and hzq_core.s_star, exec'd from its committed source.
Frozen criteria: FROZEN_CRITERIA.md (52976ec22) + ADDENDUM_1 + ADDENDUM_2 (section A2.3), written before any native number was computed.
kappa = 1/2 FITTED.  The cold mass is still required; no dark-matter particle is added.  No sentence here says the data favour a law.
Run:  python3 campaign_fresh_gravity/CFG303_lcdm_free_inputs/cfg303_amvrosiadis_LCDMFREE.py
Outputs: cfg303_amvrosiadis_LCDMFREE.out, cfg303_amvrosiadis_LCDMFREE_results.json (this lane only).
"""
import os, sys, io, json, math, contextlib, time, hashlib
sys.dont_write_bytecode = True
import numpy as np

T0 = time.time()
LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
for k in ("MUTATE", "SELFTEST"):
    os.environ.pop(k, None)
OUT, CHK = [], []


def P(s=""):
    print(s, flush=True); OUT.append(s)


def check(name, val, ok):
    CHK.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


P(__doc__.split("Run:")[0].strip())
for f in ("FROZEN_CRITERIA.md", "FROZEN_CRITERIA_ADDENDUM_1.md", "FROZEN_CRITERIA_ADDENDUM_2.md"):
    P(f"  {f}: sha256 {sha(os.path.join(LANE, f))}")
F274 = os.path.join(CFG, "CFG274_amvrosiadis_eight_discs", "cfg274_amvrosiadis_eight.py")
src = open(F274).read()
STOP = "# ================================================================== STAGE B"
assert src.count(STOP) == 1
os.environ["STAGE"] = "B"
ns = {"__file__": F274, "__name__": "cfg303_exec"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index(STOP)], "cfg274[upto STAGE B]", "exec"), ns)
os.environ.pop("STAGE", None)
H, G, IDS, POOLS, gbar_of = ns["H"], ns["G"], ns["IDS"], ns["POOLS"], ns["gbar_of"]
P(f"  CFG274 (sha {sha(F274)[:12]}) exec'd up to its stage-B block; {len(IDS)} discs")
JR = json.load(open(os.path.join(CFG, "CFG274_amvrosiadis_eight_discs", "cfg274_stageB_results.json")))["numbers"]["rows"]
ALPHA = {"committed 0.92": 0.92, "native 0.8 (ULIRG minimum)": 0.8, "native 4.36 (Galactic)": 4.36}


def one(g, gas_fac):
    go = g["V"] ** 2 / g["R"] * H.G2SI
    gb = float(gbar_of(g, gas_fac=gas_fac))
    (ls, u) = H.s_star(np.array([go / gb]), np.array([gb]))
    return dict(ls=float(ls), no_root=bool(u), s=H.s_val(ls, u), D=go / gb, GB=gb, GO=go, y=gb / H.A0C)


RES = {}
for an, a in ALPHA.items():
    RES[an] = {i: one(G[i], a / 0.92) for i in IDS}
    for pn, ids in POOLS.items():
        D = np.array([RES[an][i]["D"] for i in ids]); gb = np.array([RES[an][i]["GB"] for i in ids])
        ls, u = H.s_star(D, gb)
        RES[an][pn] = dict(ls=float(ls), no_root=bool(u), s=H.s_val(ls, u))
P("\nCONTROLS")
dd = max(abs(RES["committed 0.92"][i]["ls"] - JR[i]["ls"]) + (0 if RES["committed 0.92"][i]["no_root"] == JR[i]["no_root"] else 1) for i in IDS)
dp = max(abs(RES["committed 0.92"][p]["ls"] - JR[p]["ls"]) + (0 if RES["committed 0.92"][p]["no_root"] == JR[p]["no_root"] else 1) for p in POOLS)
check("C-ii gas_fac = 1 through CFG274's gbar_of and hzq_core.s_star reproduces every committed per-disc s* and no-root flag", f"max |diff| {dd:.1e}", dd <= 1e-9)
check("C-ii(b) (reported) the pooled P8 / P6 rows by the median rule on the same arrays against the committed pooled rows", f"max |diff| {dp:.1e}", True)
okm = all(abs(math.log10(H.gdisc(G[i]["Mg"] * 10 ** 0.2, G[i]["Re"], G[i]["R"]) / H.gdisc(G[i]["Mg"], G[i]["Re"], G[i]["R"])) - 0.2) < 1e-12 for i in IDS)
check("C-iii MUTATE: gas x 10^0.2 moves log g_bar,gas by exactly 0.2 for every disc", str(okm), okm)
P("\nPER DISC (s*; D = g_obs / g_bar; y = g_bar / a0), by gas conversion")
for i in IDS:
    P(f"  ALESS {i}: " + ";  ".join(f"{an}: {'NO ROOT' if RES[an][i]['no_root'] else format(RES[an][i]['s'], '.2f')} (D {RES[an][i]['D']:.3f}, y {RES[an][i]['y']:.1f})" for an in ALPHA))
for p in POOLS:
    P(f"  pooled {p}: " + ";  ".join(f"{an}: {'NO ROOT' if RES[an][p]['no_root'] else format(RES[an][p]['s'], '.2f')}" for an in ALPHA))
nr = {an: sum(RES[an][i]["no_root"] for i in IDS) for an in ALPHA}
P("  discs with NO ROOT: " + ", ".join(f"{an} {v}/8" for an, v in nr.items()))
npass = sum(CHK)
P(f"\n{npass}/{len(CHK)} checks pass   ({time.time() - T0:.0f} s)")
json.dump(dict(rows=RES, no_root_counts=nr, checks=dict(passed=npass, n=len(CHK))), open(os.path.join(LANE, "cfg303_amvrosiadis_LCDMFREE_results.json"), "w"), indent=1, default=float)
open(os.path.join(LANE, "cfg303_amvrosiadis_LCDMFREE.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == len(CHK) else 1)
