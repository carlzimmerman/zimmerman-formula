#!/usr/bin/env python3
"""AG5 scorer for the November ALMA releases (U4_27928 on 2026-11-06, GS4_24110 on 2026-11-28), exactly as FROZEN_SCORING.md.
  python3 score_alma.py --selftest            S1 seal hashes, S2 exact reproduction of every sealed number, S3 synthetic F-DESI case
  AG5_MUTATE=1 python3 score_alma.py --selftest    S4: a synthetic R-H-like measurement must FIRE the kill (exit 1 = bites)
  python3 score_alma.py measured_<target>.json    real scoring (only after release; see measured_TEMPLATE_*.json)
CFG571's prediction code is executed read-only; no sealed file is written.  kappa = 1/2 fitted; not theory closed."""
import hashlib, json, math, os, sys
import numpy as np
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CFGD = os.path.join(REPO, "campaign_fresh_gravity"); ARG = os.path.join(REPO, "argon_push")
MUT = os.environ.get("AG5_MUTATE") == "1"
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
FAILS = []
def check(name, ok, d=""):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {d}" if d else "")); (None if ok else FAILS.append(name)); return ok

# ------------------------------------------------------------------------------------------------ seals (S1)
C571 = os.path.join(CFGD, "CFG571_prereg_proprietary_alma")
SEALS = {"CFG571": (os.path.join(C571, "cfg571_prereg_results.json"), open(os.path.join(C571, "PREDICTIONS_HASH.txt")).read().split()[0]),
         "CFG775": (os.path.join(CFGD, "CFG775_bh_horizon_dark_energy", "SEALED_BH_BRANCH.json"), "3d2363782783e9ca4190afdb607162b2d14c00e257b8823ffb1bdf5af8d3249e"),
         "CFG778": (os.path.join(CFGD, "CFG778_sealed_event_horizon_branch", "SEALED_EVENT_HORIZON.json"), "b9f3e827f79256c0509c15fdcd60c7fdc258ac45dbfa81be3d9b0ce554dc9aad"),
         "AG4e": (os.path.join(ARG, "AG4e_n1_alma_seal", "SEALED_N1.json"), "9802de0d170ccaea7116af91c8a93dc05f72ca1a50bb52d46504f0ed8261538c"),
         "AG4d": (os.path.join(ARG, "AG4d_n2_alma_seal", "SEALED_N2.json"), "d64727b54b07b31c22386ad49afa6c0529ab1d77898b3d8aaef02d0ecc12a996")}
P("AG5 November ALMA scorer (FROZEN_SCORING.md)" + ("   *** MUTATE (S4) ***" if MUT else ""))
P("kappa = 1/2 fitted; footings never pooled; cold-energy mass required; not theory closed. One disc per date is a demonstration.")
P("\nS1 seal hashes")
SJ = {}
for k, (f, h) in SEALS.items():
    got = hashlib.sha256(open(f, "rb").read()).hexdigest(); check(f"S1 {k} sha256", got == h, got[:16] + "…"); SJ[k] = json.load(open(f))
if FAILS:
    P("a seal does not match its recorded hash: STOP (nothing scored)"); sys.exit(2)

# ------------------------------------------------------------------------------------------------ CFG571 code, read-only
P571 = os.path.join(C571, "cfg571_prereg.py")
head = open(P571).read().split("# ---- controls ----")[0]
ns = {"__file__": P571, "__name__": "cfg571_import"}
argv0 = sys.argv; sys.argv = [argv0[0]]; exec(compile(head, "cfg571_head", "exec"), ns); sys.argv = argv0
G, v2_exp, FOOT, FMT = ns["G"], ns["v2_exp"], ns["FOOT"], ns["fmt"]
KERN = {"nu_mono": ns["NU"], "n1": (lambda y: 0.5 * (1 + np.sqrt(1 + 4 / np.asarray(y, float)))), "n2": (lambda y: np.sqrt(1 + 1 / np.asarray(y, float)))}
ZK = {1.41933: "1.41933", 1.997: "1.997"}
def tab(d):
    def f(z):
        k = min(ZK, key=lambda q: abs(q - z)); assert abs(k - z) < 1e-6
        return float(d[ZK[k]])
    return f
ns["MODELS"] = {"E": tab(SJ["CFG778"]["ratios"]["E"]), "E-CCBH": tab(SJ["CFG778"]["ratios"]["E-CCBH"]), "F-flat": lambda z: 1.0, "F-DESI": ns["r_desi"],
                "BH-k3": None, "R-H": ns["r_H"], "L-fb(RAR-eq)": ns["r_fb"]}
# BH-k3 ratio: CFG775's results-table interpolation, the convention CFG778, AG4d and AG4e computed their seals with (S2 diagnosis)
_bh = json.load(open(os.path.join(CFGD, "CFG775_bh_horizon_dark_energy", "cfg775_results.json")))["numbers"]["B2"]["8.0"]["r_BH"]
ns["MODELS"]["BH-k3"] = lambda z: float(np.interp(z, [float(k) for k in _bh], list(_bh.values())))
FRAMEWORK, KILLERS = ("F-flat", "F-DESI", "BH-k3"), ("R-H", "E", "E-CCBH")
z4 = 1.41933
dc = 2.99792458e5 / 70.0 * quad(lambda x: 1 / math.sqrt(0.3 * (1 + x) ** 3 + 0.7), 0, z4)[0] * 1e3; Re4 = 0.49 / 206264.806 * dc / (1 + z4)
TGT = {"U4_27928": dict(z=z4, R=2 * Re4, Rd=Re4 / 1.678, Mstar=(10.74,), Vc=None),
       "GS4_24110": dict(z=1.997, R=7.39, Rd=7.39 / 1.678, Mstar=(10.89, 10.76), Vc=206.0)}


def req(kernel, tgt, lm, Vc):
    ns["NU"] = KERN[kernel]; t = TGT[tgt]
    return {f"{a}|{b}": c for (a, b), c in ns["predict"](t["R"], Vc, t["z"], 10 ** lm, t["Rd"]).items()}


# ------------------------------------------------------------------------------------------------ S2: exact reproduction
P("\nS2 recomputation reproduces every sealed logVbar2R_G")
SEAL_OF = {"CFG571": "nu_mono", "CFG775": "nu_mono", "CFG778": "nu_mono", "AG4e": "n1", "AG4d": "n2"}
worst, ncmp = 0.0, 0
for sk, kern in SEAL_OF.items():
    for tgt in TGT:
        blk = SJ[sk]["results"][tgt] if sk == "CFG571" else SJ[sk][tgt]
        for key, ent in blk.items():
            lm, Vc = ((float(key), 206.0) if tgt == "GS4_24110" else (10.74, float(key)))
            r = req(kern, tgt, lm, Vc)
            for k2, d in ent.items():
                worst = max(worst, abs(r[k2]["logVbar2R_G"] - d["logVbar2R_G"])); ncmp += 1
check("S2 exact reproduction of all sealed numbers", worst <= 1e-12 and ncmp > 0, f"max |d| {worst:.1e} over {ncmp} entries")
for sk, kern in SEAL_OF.items():
    w = 0.0
    for tgt in TGT:
        blk = SJ[sk]["results"][tgt] if sk == "CFG571" else SJ[sk][tgt]
        for key, ent in blk.items():
            lm, Vc = ((float(key), 206.0) if tgt == "GS4_24110" else (10.74, float(key))); r = req(kern, tgt, lm, Vc)
            w = max([w] + [abs(r[k2]["logVbar2R_G"] - d["logVbar2R_G"]) for k2, d in ent.items()])
    P(f"     {sk}: max |d| {w:.1e} dex")


FLOOR_DEX = [0.15]                                                      # CFG571's systematic floor (S4b sets 0 for the code-path check only)


def vbar_meas(tgt, lm, logMgas, shape):
    t = TGT[tgt]; Rg = t["Rd"] * (1.0 if shape == "Rg=Rd" else 1.5)
    vs = v2_exp(10 ** lm, t["Rd"], t["R"]); vg = v2_exp(10 ** logMgas, Rg, t["R"]) if logMgas is not None else 0.0
    return math.log10((vs + vg) * t["R"] / G), vg / (vs + vg)


def score(meas):
    """meas: {"target", "routes": {name: {"logMgas", "sig", "detected"}}, "primary_route", ["Vc", "eVc" for U4]}"""
    tgt = meas["target"]; t = TGT[tgt]; rows = []
    Vc = meas["Vc"] if tgt == "U4_27928" else t["Vc"]; eV = meas.get("eVc", 0.0) if tgt == "U4_27928" else 0.0
    for kern in KERN:
        for lm in t["Mstar"]:
            R0 = req(kern, tgt, lm, Vc); Rp = req(kern, tgt, lm, Vc + eV) if eV else R0; Rm_ = req(kern, tgt, lm, Vc - eV) if eV else R0
            for rn, rt in meas["routes"].items():
                for shape in ("Rg=Rd", "Rg=1.5Rd"):
                    lv, fg = vbar_meas(tgt, lm, rt["logMgas"], shape)
                    for key, d in R0.items():
                        fn, m = key.split("|")
                        D = lv - d["logVbar2R_G"]; dV = abs((lv - Rp[key]["logVbar2R_G"]) - (lv - Rm_[key]["logVbar2R_G"])) / 2
                        s = math.sqrt((fg * rt["sig"]) ** 2 + dV ** 2 + FLOOR_DEX[0] ** 2)
                        if not rt.get("detected", True):             # upper limit: one-sided
                            rd = "CONSISTENT" if D <= 2 * s else ("TENSION" if D <= 3 * s else ">=3sigma OFF")
                        else:
                            a = abs(D) / s; rd = "CONSISTENT" if a <= 2 else ("TENSION" if a <= 3 else ">=3sigma OFF")
                        floor_against = bool(d["floor"] and rt.get("detected", True) and rt["logMgas"] is not None)
                        rows.append(dict(kernel=kern, Mstar=lm, route=rn, shape=shape, foot=fn, model=m, Delta=D, sigma=s, reading=rd,
                                         floor=bool(d["floor"]), floor_against=floor_against))
    return rows


def kill_test(rows, routes, primary):
    def fires(route):
        out = []
        for lm in sorted({r["Mstar"] for r in rows}):
            sel = [r for r in rows if r["kernel"] == "nu_mono" and r["foot"].startswith("canon") and r["route"] == route and r["shape"] == "Rg=Rd" and r["Mstar"] == lm]
            fw = any(r["reading"] == "CONSISTENT" and not r["floor_against"] for r in sel if r["model"] in FRAMEWORK)
            kl = any(r["reading"] == "CONSISTENT" and not r["floor_against"] for r in sel if r["model"] in KILLERS)
            out.append((not fw) and kl)
        return all(out)
    f0 = fires(primary)
    lim = any(abs(routes[r]["logMgas"] - routes[primary]["logMgas"]) > 2 * math.hypot(routes[r]["sig"], routes[primary]["sig"])
              for r in routes if r != primary and routes[r].get("logMgas") is not None and routes[primary].get("logMgas") is not None)
    if lim:
        return f0 and all(fires(r) for r in routes), True
    return f0, False


def report(meas, rows):
    P(f"\n=== {meas['target']} ===  routes: {', '.join(meas['routes'])} (primary {meas['primary_route']})" + (f"; V_c {meas['Vc']} +- {meas.get('eVc', 0)}" if meas["target"] == "U4_27928" else ""))
    for kern in KERN:
        for lm in TGT[meas["target"]]["Mstar"]:
            sel = [r for r in rows if r["kernel"] == kern and r["Mstar"] == lm and r["route"] == meas["primary_route"] and r["shape"] == "Rg=Rd"]
            P(f"  {kern:7s} M* {lm}: " + "; ".join(f"{r['foot'][:5]} {r['model']} {r['Delta']:+.2f}±{r['sigma']:.2f} {r['reading'].split()[0]}{' FLOOR-against' if r['floor_against'] else ''}" for r in sel))
    k, lim = kill_test(rows, meas["routes"], meas["primary_route"])
    lf = {kern: any(r["reading"] == "CONSISTENT" and not r["floor_against"] for r in rows if r["kernel"] == kern and r["model"] in FRAMEWORK
                    and r["foot"].startswith("canon") and r["route"] == meas["primary_route"] and r["shape"] == "Rg=Rd") for kern in KERN}
    P(f"  THEORY KILL (canonical v1 section 2): {'FIRES' if k else 'does not fire'}{' (TRACER-LIMITED: required on every route)' if lim else ''}")
    P("  law forms with a CONSISTENT framework branch (canonical footing, primary route): " + ", ".join(f"{kk} {'yes' if v else 'no'}" for kk, v in lf.items()))
    return k, lim, lf


# ------------------------------------------------------------------------------------------------ self tests / real run
if "--selftest" in sys.argv:
    if not MUT:
        req_fd = SJ["CFG571"]["results"]["GS4_24110"]["10.89"]["canon 9.36e-11|F-DESI"]["logMgas_Rg=Rd"]
        meas = {"target": "GS4_24110", "primary_route": "synthetic", "routes": {"synthetic": {"logMgas": req_fd, "sig": 0.05, "detected": True}}}
        rows = score(meas); k, lim, lf = report(meas, rows)
        fd = [r for r in rows if r["kernel"] == "nu_mono" and r["Mstar"] == 10.89 and r["foot"].startswith("canon") and r["model"] == "F-DESI" and r["shape"] == "Rg=Rd"][0]
        check("S3 synthetic F-DESI measurement: F-DESI CONSISTENT (Delta ~ 0) and the kill does not fire", fd["reading"] == "CONSISTENT" and abs(fd["Delta"]) < 1e-6 and not k,
              f"Delta {fd['Delta']:+.2e}, kill {k}")
    else:
        hit = None
        for Vc in np.arange(225, 301, 5.0):
            r = req("nu_mono", "U4_27928", 10.74, float(Vc)); rh = r["canon 9.36e-11|R-H"]
            if rh["floor"] or rh["logMgas_Rg=Rd"] is None:
                continue
            meas = {"target": "U4_27928", "Vc": float(Vc), "eVc": 0.0, "primary_route": "synthetic",
                    "routes": {"synthetic": {"logMgas": rh["logMgas_Rg=Rd"], "sig": 0.05, "detected": True}}}
            rows = score(meas); sel = [x for x in rows if x["kernel"] == "nu_mono" and x["foot"].startswith("canon") and x["shape"] == "Rg=Rd" and x["model"] in FRAMEWORK]
            if all(abs(x["Delta"]) > 3 * x["sigma"] for x in sel):
                hit = (Vc, meas, rows); break
        if hit is None:
            P("S4 (as frozen): no V_c in 225-300 km/s separates every framework branch from R-H by > 3 sigma_tot; the tooth cannot be built.")
            P("  This is a POWER fact: with the 0.15 dex floor the canonical kill line cannot fire on U4_27928 (see README).")
            P("S4b (disclosed, code path only): the same U4 synthetic R-H case with the systematic floor set to 0 and sig 0.01")
            global_floor = 0.0
            Vc = 300.0; r = req("nu_mono", "U4_27928", 10.74, Vc); rh = r["canon 9.36e-11|R-H"]
            meas = {"target": "U4_27928", "Vc": Vc, "eVc": 0.0, "primary_route": "synthetic", "routes": {"synthetic": {"logMgas": rh["logMgas_Rg=Rd"], "sig": 0.01, "detected": True}}}
            FLOOR_DEX[0] = 0.0; rows = score(meas); k, lim, lf = report(meas, rows); FLOOR_DEX[0] = 0.15
            P(f"MUTATE (S4b): kill {'FIRES -> the kill code path BITES (exit 1)' if k else 'did NOT fire (recorded)'}")
            open(os.path.join(HERE, "score_alma_selftest_MUTATE.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1 if k else 0)
        P(f"S4: synthetic U4 measurement = R-H requirement at V_c {hit[0]:.0f} km/s")
        k, lim, lf = report(hit[1], hit[2])
        P(f"MUTATE (S4): kill {'FIRES -> control BITES (exit 1, as designed)' if k else 'did NOT fire (recorded)'}")
        open(os.path.join(HERE, "score_alma_selftest_MUTATE.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1 if k else 0)
    open(os.path.join(HERE, "score_alma_selftest.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(1 if FAILS else 0)

if "--power" in sys.argv:                                               # can the canonical kill line fire at all? (sealed numbers only)
    P("\nPOWER U4_27928: measured gas = R-H's requirement; framework |Delta|/sigma_tot (nu_mono, canonical, Rg=Rd)")
    for Vc in (225.0, 250.0, 275.0, 300.0):
        rh = req("nu_mono", "U4_27928", 10.74, Vc)["canon 9.36e-11|R-H"]
        if rh["floor"] or rh["logMgas_Rg=Rd"] is None:
            P(f"  V_c {Vc:.0f}: R-H FLOOR"); continue
        m = {"target": "U4_27928", "Vc": Vc, "eVc": 0.0, "primary_route": "s", "routes": {"s": {"logMgas": rh["logMgas_Rg=Rd"], "sig": 0.05, "detected": True}}}
        rows = score(m); k, _ = kill_test(rows, m["routes"], "s")
        sel = [x for x in rows if x["kernel"] == "nu_mono" and x["foot"].startswith("canon") and x["shape"] == "Rg=Rd" and x["model"] in FRAMEWORK]
        P(f"  V_c {Vc:.0f}: " + "; ".join(f"{x['model']} {abs(x['Delta']) / x['sigma']:.2f}" for x in sel) + f"; kill {k}")
    P("\nPOWER GS4_24110: kill fires? and the best framework |Delta|/sigma_tot per M* (sig 0.1 dex)")
    for lg in np.arange(8.0, 11.01, 0.25):
        line = []
        for det in (True, False):
            m = {"target": "GS4_24110", "primary_route": "s", "routes": {"s": {"logMgas": float(lg), "sig": 0.1, "detected": det}}}
            rows = score(m); k, _ = kill_test(rows, m["routes"], "s")
            bf = [min(abs(r["Delta"]) / r["sigma"] for r in rows if r["kernel"] == "nu_mono" and r["foot"].startswith("canon") and r["shape"] == "Rg=Rd"
                      and r["Mstar"] == lm and r["model"] in FRAMEWORK) for lm in (10.89, 10.76)]
            line.append(f"{'detected' if det else 'upper limit'}: kill {k}" + (f" (best framework {bf[0]:.2f} / {bf[1]:.2f})" if det else ""))
        P(f"  log M_gas {lg:5.2f}: " + "; ".join(line))
    open(os.path.join(HERE, "score_alma_power.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1 if FAILS[1:] else 0)

if len(sys.argv) > 1 and sys.argv[1].endswith(".json"):
    meas = json.load(open(sys.argv[1])); rows = score(meas); k, lim, lf = report(meas, rows)
    base = os.path.splitext(os.path.basename(sys.argv[1]))[0]
    json.dump(dict(measured=meas, rows=rows, kill=k, tracer_limited=lim, law_forms=lf), open(os.path.join(HERE, f"score_{base}.json"), "w"), indent=1)
    open(os.path.join(HERE, f"score_{base}.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(1 if FAILS else 0)
P("usage: --selftest | measured_<target>.json")
