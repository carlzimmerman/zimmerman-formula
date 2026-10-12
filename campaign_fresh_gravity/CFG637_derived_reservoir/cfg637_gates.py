#!/usr/bin/env python3
"""CFG637 gates (FROZEN_CRITERIA.md, e67940c56): CFG634's static gates T2 (Tian+26 groups), T3 (X-COP, incl. the inner band)
and T4b/c (Bullet) re-scored with the DERIVED reservoir (RD = Method A, RB = Method B maximum entropy) read from
cfg637_profiles.npz (written by cfg637_derive.py).

CFG634's scripts are executed from their committed source text (slices of cfg634_static.py and cfg634_bullet.py), with ONE
textual patch per reservoir function: a branch res == "RD" that adds the derived reservoir M_res(<r) (gate units) to the settled
phantom. Everything else (data, settled phantom, supply, statistics, thresholds) is CFG634's. MUTATE M-R: with res = R0 / RI / RN
the same executed code must reproduce CFG634's JSON numbers to 1e-9.
Run from the repository root:  OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG637_derived_reservoir/cfg637_gates.py
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import io, math, json, time, contextlib
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
D634 = os.path.join(LANES, "CFG634_condensed_baryon_source")
try:
    os.nice(10)
except OSError:
    pass
LOG, CHK, RES = [], {}, {"lane": "CFG637", "script": "cfg637_gates", "criteria": "e67940c56"}
QUICK = os.environ.get("CFG637_QUICK") == "1"          # debugging only: missing systems read as an empty reservoir
PROF = dict(np.load(os.path.join(HERE, "cfg637_profiles_QUICK.npz" if QUICK else "cfg637_profiles.npz")))
BRK = ("P", "eps0.5", "q0.05", "q0.2", "uniform")


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg):
    CHK[name] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


def patch(src, old, new):
    assert src.count(old) == 1, old[:60]
    return src.replace(old, new)


RD_CTX = dict(method="A", bk="P", readout="phase")


def rd_profile(prefix):
    m = RD_CTX["method"]; bk = RD_CTX["bk"]
    key = f"{prefix}|{m}|{bk}"
    if QUICK and key + "|r" not in PROF:
        return np.array([1.0, 1e5]), np.zeros(2)
    r = PROF[key + "|r"]
    M = PROF[key + ("|Mres_avg" if RD_CTX["readout"] == "avg" else "|Mres")]
    return r, M


P(__doc__.split("Run from")[0].strip())
# ================================================================================================ static (T2, T3) from CFG634 source
S = open(os.path.join(D634, "cfg634_static.py")).read()
hdr = S[:S.index("P(__doc__.split")]
t2 = S[S.index("with contextlib.redirect_stdout(io.StringIO()):\n    import cfg543_group_supply"):S.index("J543 = json.load")]
t3 = S[S.index("with contextlib.redirect_stdout(io.StringIO()):\n    import cluster_audit"):S.index("T3 = {}\nCELLS3")]
t2 = patch(t2, '''    elif res == "RI":
        cold = np.maximum(mph, COLD_G * Mb_r)''', '''    elif res == "RI":
        cold = np.maximum(mph, COLD_G * Mb_r)
    elif res == "RD":                                                     # CFG637: the derived reservoir (only patch)
        rr_, MM_ = RD_GROUP(o, src)
        cold = mph + np.interp(rk, rr_, MM_, left=0.0, right=MM_[-1])''')
t3 = patch(t3, '''    elif res == "RI":
        cold = max(mph, COLD_X * Mb)''', '''    elif res == "RI":
        cold = max(mph, COLD_X * Mb)
    elif res == "RD":                                                     # CFG637: the derived reservoir (only patch)
        rr_, MM_ = RD_XCOP(foot, name, src)
        cold = mph + float(np.interp(r_kpc, rr_, MM_, left=0.0, right=MM_[-1])) * C4.MSUN''')
NS = dict(__file__=os.path.join(D634, "cfg634_static.py"), __name__="cfg634_static_ro", __doc__="")
SRC_TAG = {"cond": "HCB", "all": "B"}


def RD_GROUP(o, src):
    foot = NS["_FOOT_NOW"]
    return rd_profile(f"G|{o['id']}|{foot}|{SRC_TAG[src]}")


def RD_XCOP(foot, name, src):
    return rd_profile(f"X|{name}|{foot}|{SRC_TAG[src]}")


NS.update(RD_GROUP=RD_GROUP, RD_XCOP=RD_XCOP)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(hdr, "cfg634_static_hdr", "exec"), NS)
NS["P"], NS["check"] = (lambda *a: None), check
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(t2, "cfg634_static_T2", "exec"), NS)
    exec(compile(t3, "cfg634_static_T3", "exec"), NS)
J634 = json.load(open(os.path.join(D634, "cfg634_static_results.json")))
FOOTS = ("canonical", "alt")

# ---- T2
P("\n== T2 Tian+26 groups (CFG634 code; RD = derived reservoir)")
CELLS = {"PRIMARY R0 hot0.08 H": dict(), "hot0.04": dict(fh=0.04), "hot0.16": dict(fh=0.16), "hotshape X": dict(hshape="X"),
         "Re k=1.563": dict(k=1.563), "RN c4": dict(res="RN"), "RN c3": dict(res="RN", conc=3.0), "RN c5": dict(res="RN", conc=5.0),
         "RI": dict(res="RI"), "B (all source) R0 [=M1]": dict(src="all"), "B (all source) RN c4": dict(src="all", res="RN"),
         "B (all source) RI": dict(src="all", res="RI"), "M2 no source R0": dict(src="none")}
mr2 = 0.0
for foot, fk in (("canonical", "can"), ("alt", "alt")):
    a0 = NS["C540"].FOOT[fk]; NS["_FOOT_NOW"] = foot
    for nm, kw in CELLS.items():
        st = NS["run_groups"](a0, **kw)
        ref = J634["T2"]["rows"][foot][nm]
        mr2 = max(mr2, abs(st["mean"] - ref["mean"]), abs(st["Z"] - ref["Z"]))
check("M-R T2: R0/RI/RN/hot/M2 cells reproduce CFG634 (mean and Z, 1e-9)", mr2 <= 1e-9, f"max abs diff {mr2:.1e}")
T2 = {}
for foot, fk in (("canonical", "can"), ("alt", "alt")):
    a0 = NS["C540"].FOOT[fk]; NS["_FOOT_NOW"] = foot
    T2[foot] = {}
    for src in ("cond", "all"):
        cells = [("A", b, "phase") for b in BRK] + [("A", "P", "avg"), ("B", "P", "phase")]
        for m, b, ro in cells:
            RD_CTX.update(method=m, bk=b, readout=ro)
            st = NS["run_groups"](a0, src=src, res="RD"); st.pop("Delta", None)
            nm = f"{SRC_TAG[src]}|R{'D' if m == 'A' else 'B'}|{b}|{ro}"
            T2[foot][nm] = st
            P(f"  [{foot}] {nm:22s} mean {st['mean']:+.3f}  Z {st['Z']:+.2f}  -> {st['label']}")
RES["T2"] = T2

# ---- T3
P("\n== T3 X-COP (CFG634 code; RD = derived reservoir)")
mr3 = 0.0
for tag, srcm in (("HCB", "cond"), ("B", "all"), ("M2", "none")):
    for res, conc in (("R0", 4.0), ("RI", 4.0), ("RN", 4.0), ("RN", 3.0), ("RN", 5.0)):
        nm = f"{tag}|{res}" + (f"c{conc:g}" if res == "RN" else "")
        for f in FOOTS:
            a = NS["t3_cell"](f, srcm, res, conc); b = NS["t3_cell"](f, srcm, res, conc, band=(200, 420))
            ra = J634["T3"]["rows"][nm]["headline"][f]; rb = J634["T3"]["rows"][nm]["inner_200_420"][f]
            mr3 = max(mr3, abs(a["eta_median"] - ra["eta_median"]), abs(a["sigma"] - ra["sigma"]), abs(b["eta_median"] - rb["eta_median"]))
check("M-R T3: R0/RI/RN cells reproduce CFG634 (headline eta, sigma, inner band, 1e-9)", mr3 <= 1e-9, f"max abs diff {mr3:.1e}")
T3 = {}
for src in ("cond", "all"):
    cells = [("A", b, "phase") for b in BRK] + [("A", "P", "avg"), ("B", "P", "phase")]
    for m, b, ro in cells:
        RD_CTX.update(method=m, bk=b, readout=ro)
        nm = f"{SRC_TAG[src]}|R{'D' if m == 'A' else 'B'}|{b}|{ro}"
        head = {f: NS["t3_cell"](f, src, "RD") for f in FOOTS}
        inner = {f: NS["t3_cell"](f, src, "RD", band=(200, 420)) for f in FOOTS}
        b02 = {f: NS["t3_cell"](f, src, "RD", bias=0.2) for f in FOOTS}
        T3[nm] = dict(headline=head, label=NS["t3_label"](list(head.values())), inner_200_420=inner,
                      inner_label=NS["t3_label"](list(inner.values())), bias02=b02)
        P(f"  {nm:22s} eta headline " + " / ".join(f"{head[f]['eta_median']:.3f}+-{head[f]['sigma']:.3f}" for f in FOOTS) + f" -> {T3[nm]['label']:8s}"
          + " | inner 200-420 " + " / ".join(f"{inner[f]['eta_median']:.3f}" for f in FOOTS) + f" ({T3[nm]['inner_label']})"
          + " | b=0.2 " + " / ".join(f"{b02[f]['eta_median']:.3f}" for f in FOOTS))
RES["T3"] = T3

# ================================================================================================ Bullet (T4) from CFG634 source
P("\n== T4 Bullet (CFG634 code; RD = derived reservoir)")
SB = open(os.path.join(D634, "cfg634_bullet.py")).read()
bh = SB[:SB.index("P(__doc__.split")]
bb = SB[SB.index("J4 = json.load(open(os.path.join(LANES, \"CFG4_clusters_results.json\")))"):SB.index("# (a) invariance")]
bb = patch(bb, '''    supply = COLD * p.Mb; Mu = max(supply - Mt, 0.0)''', '''    if res == "RD":                                                       # CFG637: the derived reservoir (only patch)
        rr_, MM_ = RD_BULLET(p, src)
        Mr_ = np.interp(r, rr_, MM_, left=0.0, right=MM_[-1])
        rho_r = np.maximum(np.gradient(Mr_, r) / (4 * math.pi * np.maximum(r, 1e-3) ** 2), 0.0)
        return rho_set, rho_r, Mt, float(Mr_[-1])
    supply = COLD * p.Mb; Mu = max(supply - Mt, 0.0)''')
NB = dict(__file__=os.path.join(D634, "cfg634_bullet.py"), __name__="cfg634_bullet_ro", __doc__="")


def RD_BULLET(p, src):
    ft = "can" if abs(p.a0 - NB["L625"].A0["can"]) < 1e-9 * p.a0 else "alt"
    return rd_profile(f"BU|{p.variant}_{p.role}|{ft}|{SRC_TAG[src]}")


NB["RD_BULLET"] = RD_BULLET
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(bh, "cfg634_bullet_hdr", "exec"), NB)
NB["P"], NB["check"] = (lambda *a: None), check
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(bb, "cfg634_bullet_body", "exec"), NB)
L625, TAB, POS, SIGCR, AP, DK_OBS = NB["L625"], NB["TAB"], NB["POS"], NB["SIGCR"], NB["AP"], NB["DK_OBS"]
PRO = {}
for var in ("BASE", "B1", "B2", "B3"):
    for ft in ("can", "alt"):
        PRO[(var, ft, "main")] = L625.Progenitor625(1.5e15, ft, cloud=False, variant=var)
        PRO[(var, ft, "sub")] = L625.Progenitor625(1.5e14, ft, cloud=True, variant=var)


def t4_cell(var, ft, srcm, res):        # CFG634's loop body, verbatim in substance (aperture contrast + core ratio)
    comp = {}
    for role in ("main", "sub"):
        p = PRO[(var, ft, role)]
        rs_, rr_, Mt, Mu = NB["dark_components"](p, srcm, res)
        comp[role] = dict(p=p, rho_d=rs_ + rr_, Mset=Mt, Mres=Mu)
    SD = {role: NB["sigma_of"](comp[role]["p"].r, comp[role]["rho_d"]) for role in comp}
    cen = {"main": POS["Main cluster BCG"], "sub": POS["Subcluster BCG"]}
    kap = {}
    for lab in TAB:
        Md = sum(NB["ap_mass"](SD[role], cen[role], POS[lab]) for role in SD)
        kap[lab] = (TAB[lab]["MX"] + TAB[lab]["Ms"] + Md) / (SIGCR * AP)
    dk = {"main": kap["Main cluster BCG"] - kap["Main cluster plasma"], "sub": kap["Subcluster BCG"] - kap["Subcluster plasma"]}
    zz = {g: (dk[g] - DK_OBS[g][0]) / DK_OBS[g][1] for g in dk}
    core = {}
    for role in ("main", "sub"):
        p = comp[role]["p"]
        bar = p.rho_g + p.rho_cc + p.rho_s
        tot = L625.proj_mass(p.r, bar, 250.0) + L625.proj_mass(p.r, comp[role]["rho_d"], 250.0)
        core[role] = dict(proj250=tot, ratio_P16=tot / L625.P16_M250[role][0], Mset=comp[role]["Mset"], Mres=comp[role]["Mres"])
    lab_b = "PASS" if all(abs(zz[g]) <= 2 and dk[g] > 0 for g in dk) else ("FAIL" if any(abs(zz[g]) >= 3 for g in dk) else "TENSION")
    return dict(dkappa=dk, z=zz, label=lab_b, core=core)


J634B = json.load(open(os.path.join(D634, "cfg634_bullet_results.json")))
mr4 = 0.0
for var in ("BASE", "B1", "B2", "B3"):
    for ft in ("can", "alt"):
        for tag, srcm in (("HCB", "cond"), ("B_alpha0", "all"), ("M2", "none")):
            for res in ("R0", "RI", "RN"):
                c = t4_cell(var, ft, srcm, res); ref = J634B["T4"][f"{var}|{ft}|{tag}|{res}"]
                for g in ("main", "sub"):
                    mr4 = max(mr4, abs(c["dkappa"][g] - ref["dkappa"][g]), abs(c["core"][g]["ratio_P16"] - ref["core"][g]["ratio_P16"]))
check("M-R T4: R0/RI/RN cells (4 variants x 2 footings x 3 sources) reproduce CFG634 (dkappa, M250/P16, 1e-9)", mr4 <= 1e-9, f"max abs diff {mr4:.1e}")
T4 = {}
for var in ("BASE", "B1", "B2", "B3"):
    for ft in ("can", "alt"):
        for src in ("cond", "all"):
            cells = [("A", "P", "phase")]
            if var == "B1":
                cells += [("A", b, "phase") for b in BRK[1:]] + [("A", "P", "avg"), ("B", "P", "phase")]
            for m, b, ro in cells:
                RD_CTX.update(method=m, bk=b, readout=ro)
                c = t4_cell(var, ft, src, "RD")
                nm = f"{var}|{ft}|{SRC_TAG[src]}|R{'D' if m == 'A' else 'B'}|{b}|{ro}"
                T4[nm] = c
                if var == "B1" or b == "P":
                    P(f"  {nm:30s} dkappa main {c['dkappa']['main']:+.3f} (z {c['z']['main']:+.2f}), sub {c['dkappa']['sub']:+.3f} (z {c['z']['sub']:+.2f}) -> {c['label']:7s}"
                      f" | M(<250)/P16 main {c['core']['main']['ratio_P16']:.2f}, sub {c['core']['sub']['ratio_P16']:.2f} | reservoir main {c['core']['main']['Mres']:.2e}, sub {c['core']['sub']['Mres']:.2e}")
RES["T4"] = T4

# ================================================================================================ joint gates
P("\n== joint gates J (T2 PASS, T3 headline PASS, T4b B1 PASS, each on both footings) and J+ (plus T3 inner band PASS)")
JNT = {}
for s in ("HCB", "B"):
    for m in ("RD", "RB"):
        for b in (BRK if m == "RD" else ("P",)):
            for ro in (("phase", "avg") if (m == "RD" and b == "P") else ("phase",)):
                k = f"{s}|{m}|{b}|{ro}"
                t2 = {f: T2[f][k]["label"] for f in FOOTS}
                t3 = T3[k]["label"]; t3i = T3[k]["inner_label"]
                t4 = {ft: T4[f"B1|{ft}|{k}"]["label"] for ft in ("can", "alt")}
                j = all(v == "CLOSES" for v in t2.values()) and t3 == "PASS" and all(v == "PASS" for v in t4.values())
                jp = j and t3i == "PASS"
                JNT[k] = dict(T2=t2, T3=t3, T3_inner=t3i, T4b_B1=t4, J=j, Jplus=jp)
                P(f"  {k:22s} T2 {t2['canonical']}/{t2['alt']} | T3 {t3} (inner {t3i}) | T4b B1 {t4['can']}/{t4['alt']} -> J {'PASS' if j else 'FAIL'}, J+ {'PASS' if jp else 'FAIL'}")
RES["joint"] = JNT
verdict = {}
for s in ("HCB", "B"):
    prim = JNT[f"{s}|RD|P|phase"]
    flips = [k for k, v in JNT.items() if k.startswith(s + "|RD|") and k != f"{s}|RD|P|phase" and v["J"] != prim["J"]]
    mB = JNT[f"{s}|RB|P|phase"]["J"] != prim["J"]
    if prim["J"]:
        lab = "SINGLE DERIVED RULE PASSES" + (" (J+ too)" if prim["Jplus"] else " (J+ FAILS: X-COP inner band)")
    else:
        failing = [g for g, ok in (("T2 groups", all(v == "CLOSES" for v in prim["T2"].values())), ("T3 X-COP", prim["T3"] == "PASS"),
                                   ("T4b Bullet", all(v == "PASS" for v in prim["T4b_B1"].values()))) if not ok]
        lab = "DERIVED RESERVOIR FAILS " + ", ".join(failing)
    if flips:
        lab += f"; DERIVATION-BRACKET-DEPENDENT (flipped by {', '.join(flips)})"
    if mB:
        lab += "; METHOD-DEPENDENT (Method B differs)"
    verdict[s] = lab
    P(f"  VERDICT [{s}]: {lab}")
RES["verdict"] = verdict
RES["checks"] = CHK; RES["elapsed_s"] = round(time.time() - T0, 1)
nf = sum(1 for c in CHK.values() if not c["ok"])
P(f"\n{len(CHK) - nf}/{len(CHK)} checks pass; elapsed {RES['elapsed_s']} s")
sfx = "_QUICK" if QUICK else ""
json.dump(NS["C4"].jclean(RES), open(os.path.join(HERE, f"cfg637_gates_results{sfx}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg637_gates{sfx}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nf else 0)
