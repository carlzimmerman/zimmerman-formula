#!/usr/bin/env python3
"""CFG768: the NGC 1052 trail (DF2, DF4, DF9, LEDA 4014647) with alpha taken from the record's own physics.

Criteria: FROZEN_CRITERIA.md (committed alone, 35f781ce3). Seconds, < 100 MB, no downloads.
Part A: P-wave export window (CFG760/761/767) + one-c_P rule (CFG762) -> alpha_P; f_cap = S + F (CFG657 code, alpha = 0).
Part B: formation-at-rest clocks CFG763 (universal) and CFG764 (orbital) at lenient ages / orbits.
CFG768_MUTATE=1: M1 gap off (c_P,max -> inf), M2 ages 0.3 Gyr; exit 1 iff both teeth bite.
kappa = 1/2 FITTED; both footings, never pooled; the cold energy's mass is required; no particle species; not "theory closed".
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
MUT = os.environ.get("CFG768_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"cfg768{TAG}.out"), "w")
RES = {"lane": "CFG768", "criteria": "35f781ce3", "mutate": MUT, "A": {}, "B": {}, "verdict": {}}


def P_(s=""):
    print(s, flush=True)
    OUT.write(s + "\n")


P_(__doc__.strip())

# ---- CFG657 code, copied by exec of its text above the run section (no edits)
src = open(os.path.join(CFG, "CFG657_trail_capture_rule", "cfg657_capture.py")).read()
src = src[:src.index("\nlines = []")]
os.environ["MUTATE"] = "0"
NS = {"__file__": os.path.join(CFG, "CFG657_trail_capture_rule", "cfg657_capture.py"), "__name__": "cfg657_copy"}
exec(compile(src, "cfg657_copy", "exec"), NS)
GAL, FOOTS, PRIMARY, BRACKET, capture, zf = NS["GAL"], NS["FOOTS"], NS["PRIMARY"], NS["BRACKET"], NS["capture"], NS["zf"]

BOUND = {"DF2": {"canonical": 0.36, "alt": 0.33}, "DF4": {"canonical": 0.29, "alt": 0.26}, "DF9": {"canonical": 0.52, "alt": 0.46}}
c657 = json.load(open(os.path.join(CFG, "CFG657_trail_capture_rule", "cfg657_capture_results.json")))
FMIN = {f: c657["verdict"][f]["f_min_LEDA"] for f in FOOTS}
c762 = json.load(open(os.path.join(CFG, "CFG762_one_cP", "cfg762_results.json")))["numbers"]
SPARC_CMIN = {f: c762[f]["max_cP_min"] for f in FOOTS}
DEBRIS = ("DF2", "DF4", "DF9")

G, MSUN, KPC, GYR_S = 6.6743e-11, 1.98847e30, 3.0856775814913673e19, 3.15576e16
LSTAR = 5.754 * 3.0856775814913673e16
X_E = 0.71
GYR_KPC_KMS = 0.97779       # 1 kpc/(km/s) in Gyr


def window(M_sun, r_kpc, a0):
    M = M_sun * MSUN; r = r_kpc * KPC
    rM = math.sqrt(G * M / a0); ell = LSTAR ** 2 / (2 * rM); s0 = r / ell
    V = 2 * (G * M * a0) ** 0.25
    cmax = math.inf if MUT else V / (X_E * math.sqrt(2 * s0))       # CFG767 deep-limit, CFG761 generous x_e
    cmin = r / (13.8 * GYR_S)
    return dict(s0=s0, V_ms=V, cP_max_ms=cmax, cP_min_ms=cmin, open=bool(cmax >= cmin))


# =========================================================================== Part A
P_("\nPART A  P-wave export window (L* = 5.754 pc, x_e = 0.71, V = 2 V_f, c_P,min = r / 13.8 Gyr)")
A_close = {}
for foot, a0 in FOOTS.items():
    A_close[foot] = True
    RES["A"][foot] = {}
    for n in GAL:
        c = capture(n, foot, dict(PRIMARY))
        M = c["M_b"]
        rows = {lab: window(M, r, a0) for lab, r in (("r_half", c["r_half"]), ("R_c", c["R_c"]))}
        cmax_all = max(w["cP_max_ms"] for w in rows.values())
        shared = cmax_all >= SPARC_CMIN[foot]
        A_close[foot] &= not shared
        RES["A"][foot][n] = dict(windows=rows, cP_max_best=cmax_all, SPARC_cP_min=SPARC_CMIN[foot], overlaps_SPARC=bool(shared))
        for lab, w in rows.items():
            P_(f"  {foot:9s} {n:5s} {lab:6s} s0 {w['s0']:.3e}  c_P,max {w['cP_max_ms']:8.1f} m/s  c_P,min {w['cP_min_ms']:7.1f} m/s  "
               f"own window {'OPEN' if w['open'] else 'closed'}")
    P_(f"  {foot:9s} one c_P: SPARC needs c_P >= {SPARC_CMIN[foot]:.0f} m/s (CFG762); best trail c_P,max "
       f"{max(RES['A'][foot][n]['cP_max_best'] for n in GAL):.1f} m/s -> " + ("CLOSED (alpha_P = 0)" if A_close[foot] else "NOT CLOSED"))

P_("\n  f_cap with alpha_P = 0 (channels S + F; CFG657 code): primary and max over one-at-a-time brackets (alpha excluded)")
A_verdict = {}
for foot in FOOTS:
    fc = {}
    for n in GAL:
        prim = capture(n, foot, dict(PRIMARY, alpha=0.0))["fcap"]
        vals = [prim]
        for key, (lo, hi) in BRACKET.items():
            if key == "alpha":
                continue
            for v in (lo, hi):
                vals.append(capture(n, foot, dict(PRIMARY, alpha=0.0, **{key: v}))["fcap"])
        fc[n] = dict(primary=prim, max=max(vals), min=min(vals))
        tgt = f"<= {BOUND[n][foot]}" if n in DEBRIS else f">= f_min {FMIN[foot]:.4f}"
        P_(f"  {foot:9s} {n:5s} f_cap primary {prim:.2e}  bracket [{min(vals):.2e}, {max(vals):.2e}]   need {tgt}")
    deb_ok = all(fc[n]["max"] <= BOUND[n][foot] for n in DEBRIS)
    leda_ok_any = fc["LEDA"]["max"] >= FMIN[foot]
    if not A_close[foot]:
        v = "NOT DERIVED"
    elif deb_ok and leda_ok_any and fc["LEDA"]["primary"] >= FMIN[foot]:
        v = "REPRODUCES"
    elif deb_ok and not leda_ok_any:
        v = "LEDA UNSUPPLIED"
    else:
        v = "OTHER"
    A_verdict[foot] = v
    RES["A"][foot]["f_cap_alpha0"] = fc
    RES["A"][foot]["verdict"] = v
    P_(f"  {foot:9s} VERDICT A: {v}")

# =========================================================================== Part B
P_("\nPART B  formation at rest: f = 1 - exp(-t/tau); lenient ages / orbits (debris: smallest f; LEDA: largest f)")
CLK = {"canonical": dict(tau=(0.72, 3.47), k=(0.46, 1.20)), "alt": dict(tau=(0.83, 3.47), k=(0.52, 1.20))}
B_verdict = {}
for foot in FOOTS:
    RES["B"][foot] = {}
    for clock in ("universal", "orbital"):
        rows = {}
        for n, g in GAL.items():
            age, eup, elo = g["age"]
            if MUT:
                age, eup, elo = 0.3, 0.0, 0.0
            s, su, sl = g["obs"]
            r = (4.0 / 3.0) * g["Re"]                       # kpc, CFG655 r_1/2 at D = D_ref
            if n in DEBRIS:
                t = max(0.0, min(age - elo, 6.0 if not MUT else age))
                Vc = math.sqrt(3) * max(1.0, s - sl)
                torb = 2 * math.pi * r / Vc * GYR_KPC_KMS
                tau = CLK[foot]["tau"][1] if clock == "universal" else CLK[foot]["k"][1] * torb
            else:
                t = age + eup
                Vc = math.sqrt(3) * (s + su)
                torb = 2 * math.pi * r / Vc * GYR_KPC_KMS
                tau = CLK[foot]["tau"][0] if clock == "universal" else CLK[foot]["k"][0] * torb
            f = 1.0 - math.exp(-t / tau)
            ok = (f <= BOUND[n][foot]) if n in DEBRIS else (f >= FMIN[foot])
            Z = zf(n, foot, f)
            rows[n] = dict(t_Gyr=t, t_orb_Gyr=torb, tau_Gyr=tau, f=f, ok=bool(ok), Z_at_f=Z)
            tgt = f"<= {BOUND[n][foot]}" if n in DEBRIS else f">= {FMIN[foot]:.4f}"
            P_(f"  {foot:9s} {clock:9s} {n:5s} t {t:5.2f} Gyr  t_orb {torb:5.2f}  tau {tau:5.2f}  f {f:.3f} (need {tgt})  "
               f"Z {Z:+.2f}  [{'ok' if ok else 'FAIL'}]")
        deb_fail = [n for n in DEBRIS if not rows[n]["ok"]]
        v = ("EXCLUDED (debris overfilled: " + ", ".join(deb_fail) + ")") if deb_fail else ("CONSISTENT" if rows["LEDA"]["ok"] else "OTHER (LEDA short)")
        RES["B"][foot][clock] = dict(rows=rows, verdict=v)
        B_verdict[(foot, clock)] = v
        P_(f"  {foot:9s} {clock:9s} VERDICT B: {v}")

# =========================================================================== overall / MUTATE
if MUT:
    m1 = not any(A_close.values())
    m2 = all(RES["B"][f]["universal"]["rows"][n]["ok"] for f in FOOTS for n in DEBRIS)
    P_(f"\nMUTATE  M1 gap off -> one-c_P closure fails: {m1};  M2 ages 0.3 Gyr -> universal clock keeps every debris <= bound: {m2}")
    RES["verdict"] = dict(M1_bites=m1, M2_bites=m2)
    json.dump(RES, open(os.path.join(HERE, f"cfg768_results{TAG}.json"), "w"), indent=1)
    sys.exit(1 if (m1 and m2) else 0)

for foot in FOOTS:
    allB_ex = all(B_verdict[(foot, c)].startswith("EXCLUDED") for c in ("universal", "orbital"))
    over = ("FRAMEWORK ASSEMBLY DOES NOT REPRODUCE THE TRAIL" if (A_verdict[foot] == "LEDA UNSUPPLIED" and allB_ex)
            else "AS FOUND: A " + A_verdict[foot] + "; B " + "; ".join(B_verdict[(foot, c)] for c in ("universal", "orbital")))
    RES["verdict"][foot] = over
    P_(f"\nOVERALL {foot}: {over}")
json.dump(RES, open(os.path.join(HERE, f"cfg768_results{TAG}.json"), "w"), indent=1)
