#!/usr/bin/env python3
"""CFG656 gates (FROZEN_CRITERIA.md, c1236bf88): CFG634's static T3 (X-COP, headline 1000 kpc + inner band 200-420 kpc) and T2
(Tian+26 groups) executed from CFG634's committed source with CFG637's single RD patch, the derived reservoir read from
cfg656_profiles.npz (this lane's catchment supply) and, for T2 primary / M-OLD cross-checks, CFG637's own profiles.
MUTATE: M-OLD (OLD convention reproduces CFG637's eta to 1e-9), M-HALF (half supply raises eta). Verdict per §3.
Run from the repository root:  OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG656_xcop_native_supply/cfg656_gates.py
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import io, math, json, time, contextlib
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
D634 = os.path.join(LANES, "CFG634_condensed_baryon_source"); D637 = os.path.join(LANES, "CFG637_derived_reservoir")
try:
    os.nice(10)
except OSError:
    pass
LOG, CHK, RES = [], {}, {"lane": "CFG656", "script": "cfg656_gates", "criteria": "c1236bf88"}
PROF = dict(np.load(os.path.join(HERE, "cfg656_profiles.npz")))
P637 = dict(np.load(os.path.join(D637, "cfg637_profiles.npz")))
DER = json.load(open(os.path.join(HERE, "cfg656_derive_results.json")))
J637 = json.load(open(os.path.join(D637, "cfg637_gates_results.json")))
FOOTS = ("canonical", "alt")
SRC_TAG = {"cond": "HCB", "all": "B"}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg):
    CHK[name] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


def patch(src, old, new):
    assert src.count(old) == 1, old[:60]
    return src.replace(old, new)


CTX = dict(mode="P", group="637")
P(__doc__.split("Run from")[0].strip())
S = open(os.path.join(D634, "cfg634_static.py")).read()
hdr = S[:S.index("P(__doc__.split")]
t2 = S[S.index("with contextlib.redirect_stdout(io.StringIO()):\n    import cfg543_group_supply"):S.index("J543 = json.load")]
t3 = S[S.index("with contextlib.redirect_stdout(io.StringIO()):\n    import cluster_audit"):S.index("T3 = {}\nCELLS3")]
t2 = patch(t2, '''    elif res == "RI":
        cold = np.maximum(mph, COLD_G * Mb_r)''', '''    elif res == "RI":
        cold = np.maximum(mph, COLD_G * Mb_r)
    elif res == "RD":                                                     # CFG637's RD patch (reservoir source: CFG656 context)
        rr_, MM_ = RD_GROUP(o, src)
        cold = mph + np.interp(rk, rr_, MM_, left=0.0, right=MM_[-1])''')
# T2-CEN: the group supply edge read with the census catchment (only when CTX group == "CEN"; else 0.10 exactly as CFG634)
t2 = patch(t2, '''    supply = COLD_G * M / 0.10                                                   # P2 containment (catchment cold energy unchanged)''',
           '''    supply = COLD_G * M / GROUP_F(o)                                             # CFG656: 0.10 (CFG634) or census f_ret (T2-CEN)''')
t3 = patch(t3, '''    elif res == "RI":
        cold = max(mph, COLD_X * Mb)''', '''    elif res == "RI":
        cold = max(mph, COLD_X * Mb)
    elif res == "RD":                                                     # CFG637's RD patch (reservoir source: CFG656 context)
        rr_, MM_ = RD_XCOP(foot, name, src)
        cold = mph + float(np.interp(r_kpc, rr_, MM_, left=0.0, right=MM_[-1])) * C4.MSUN''')
NS = dict(__file__=os.path.join(D634, "cfg634_static.py"), __name__="cfg634_static_ro", __doc__="")
FCEN = DER.get("group_fret_census", {})


def GROUP_F(o):
    return FCEN[o["id"]] if CTX["group"] == "CEN" else 0.10


def RD_GROUP(o, src):
    foot = NS["_FOOT_NOW"]
    if CTX["group"] == "CEN":
        k = f"G|CEN|{o['id']}|{foot}|{SRC_TAG[src]}"; return PROF[k + "|r"], PROF[k + "|Mres"]
    k = f"G|{o['id']}|{foot}|{SRC_TAG[src]}|A|P"; return P637[k + "|r"], P637[k + "|Mres"]


def RD_XCOP(foot, name, src):
    k = f"X|{CTX['mode']}|{name}|{foot}|{SRC_TAG[src]}"
    return PROF[k + "|r"], PROF[k + "|Mres"]


NS.update(RD_GROUP=RD_GROUP, RD_XCOP=RD_XCOP, GROUP_F=GROUP_F)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(hdr, "cfg634_static_hdr", "exec"), NS)
NS["P"], NS["check"] = (lambda *a: None), check
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(t2, "cfg634_static_T2", "exec"), NS)
    exec(compile(t3, "cfg634_static_T3", "exec"), NS)
C4, CA = NS["C4"], NS["CA"]
NAMES = NS["NAMES"]

# ================================================================================================ T3
P("\n== T3 X-COP (CFG634 code + CFG637 RD patch; reservoir = CFG637 derivation with this lane's catchment supply)")
MODES = ["OLD", "P", "HI", "LO", "FLOOR", "RET", "NAT", "HALF", "P_eps0.5", "P_q0.05", "P_q0.2", "P_uniform"]
T3 = {}
for mode in MODES:
    CTX["mode"] = mode
    for src in ("cond", "all"):
        head = {f: NS["t3_cell"](f, src, "RD") for f in FOOTS}
        inner = {f: NS["t3_cell"](f, src, "RD", band=(200, 420)) for f in FOOTS}
        b02 = {f: NS["t3_cell"](f, src, "RD", bias=0.2) for f in FOOTS}
        nm = f"{SRC_TAG[src]}|{mode}"
        T3[nm] = dict(headline=head, label=NS["t3_label"](list(head.values())), inner_200_420=inner,
                      inner_label=NS["t3_label"](list(inner.values())), bias02=b02)
        P(f"  {nm:16s} eta headline " + " / ".join(f"{head[f]['eta_median']:.3f}+-{head[f]['sigma']:.3f}" for f in FOOTS) + f" -> {T3[nm]['label']:8s}"
          + " | inner 200-420 " + " / ".join(f"{inner[f]['eta_median']:.3f}" for f in FOOTS) + f" ({T3[nm]['inner_label']})"
          + " | b=0.2 " + " / ".join(f"{b02[f]['eta_median']:.3f}" for f in FOOTS))
RES["T3"] = T3
P("  per-cluster headline eta (1000 kpc), canonical / alt (reported):")
PER = {}
for mode in ("OLD", "P", "HI", "LO", "FLOOR", "RET", "NAT"):
    CTX["mode"] = mode
    for src in ("cond", "all"):
        for f in FOOTS:
            for name, pts in NS["ROWS3"][f].items():
                r, gb, gh = sorted(pts)[-1]
                PER[f"{SRC_TAG[src]}|{mode}|{name}|{f}"] = NS["cl_model"](f, name, r, gb, gh, src, "RD")[0]
for name in NAMES:
    P(f"    {name:8s} H-CB " + "  ".join(f"{m} {PER[f'HCB|{m}|{name}|canonical']:.2f}/{PER[f'HCB|{m}|{name}|alt']:.2f}" for m in ("OLD", "P", "LO", "FLOOR"))
      + f"  | B P {PER[f'B|P|{name}|canonical']:.2f}/{PER[f'B|P|{name}|alt']:.2f}")
RES["per_cluster_eta"] = PER

# ---- M-OLD
mo = 0.0
for s in ("HCB", "B"):
    ref = J637["T3"][f"{s}|RD|P|phase"]; me = T3[f"{s}|OLD"]
    for f in FOOTS:
        mo = max(mo, abs(me["headline"][f]["eta_median"] - ref["headline"][f]["eta_median"]), abs(me["headline"][f]["sigma"] - ref["headline"][f]["sigma"]),
                 abs(me["inner_200_420"][f]["eta_median"] - ref["inner_200_420"][f]["eta_median"]))
check("M-OLD OLD convention re-derived here reproduces CFG637 T3 RD|P|phase (headline eta, sigma, inner eta; both sources, both footings; 1e-9)",
      mo <= 1e-9, f"max abs diff {mo:.1e}")
mp = 0.0
for n in NAMES:
    for f in FOOTS:
        for s in ("B", "HCB"):
            a = PROF[f"X|OLD|{n}|{f}|{s}|Mres"]; b = P637[f"X|{n}|{f}|{s}|A|P|Mres"]
            mp = max(mp, float(np.max(np.abs(a - b)) / max(np.max(np.abs(b)), 1.0)))
P(f"  M-OLD (reported) re-derived OLD reservoir profiles vs cfg637_profiles.npz: max rel diff {mp:.1e}")


# ---- M-HALF
def res_inside(mode, n, f, s, r=1000.0):
    return float(np.interp(r, PROF[f"X|{mode}|{n}|{f}|{s}|r"], PROF[f"X|{mode}|{n}|{f}|{s}|Mres"]))


ok_nd, ok_inc, msg = True, True, []
for s in ("HCB", "B"):
    for f in FOOTS:
        eP = T3[f"{s}|P"]["headline"][f]["eta_median"]; eH = T3[f"{s}|HALF"]["headline"][f]["eta_median"]
        nonempty = any(res_inside("P", n, f, s) > 0 for n in NAMES)
        ok_nd &= eH >= eP - 1e-9
        if nonempty:
            ok_inc &= eH > eP + 1e-6
        msg.append(f"{s}/{f}: {eP:.4f} -> {eH:.4f} ({'reservoir present' if nonempty else 'reservoir empty: n/a'})")
check("M-HALF half supply never lowers eta and raises it wherever the primary reservoir is non-empty inside 1000 kpc", ok_nd and ok_inc, "; ".join(msg))

# ================================================================================================ diagnostic eta(R200)
P("\n== diagnostic eta(R200) (reported only, NO verdict weight): M_FORW(R200) / [M_b(<R200) + source phantom + M_res(<R200)]")
CLD = {c["name"]: c for c in [CA.load_cluster(n) for n in NAMES]}
DIAG = {}
for mode in ("OLD", "P", "HI", "LO", "FLOOR", "RET", "NAT"):
    base = mode if mode in ("OLD", "P", "HI", "LO", "FLOOR") else "P"
    for s in ("HCB", "B"):
        for f in FOOTS:
            a0 = C4.A0[f]; v = []
            for n in NAMES:
                c = CLD[n]; R2 = NS["R200"][n]
                MF = float(CA.loginterp(R2, c["rh"], c["M_FORW"]))
                rr = PROF[f"XC|{base}|{n}|r"]; g = float(np.interp(R2, rr, PROF[f"XC|{base}|{n}|gas"])); st = float(np.interp(R2, rr, PROF[f"XC|{base}|{n}|stars"]))
                Ms = (g + st) if s == "B" else st
                gN = C4.G_SI * Ms * C4.MSUN / (R2 * C4.KPC) ** 2
                mph = (float(C4.nu_mono(gN / a0)) - 1.0) * Ms
                v.append(MF / (g + st + mph + res_inside(mode, n, f, s, R2)))
            DIAG[f"{s}|{mode}|{f}"] = dict(eta_median=float(np.median(v)), sigma=float(np.std(v, ddof=1) / math.sqrt(len(v))))
        P(f"  {s:3s} {mode:5s} eta(R200) " + " / ".join(f"{DIAG[f'{s}|{mode}|{f}']['eta_median']:.3f}+-{DIAG[f'{s}|{mode}|{f}']['sigma']:.3f}" for f in FOOTS))
RES["diag_eta_R200"] = DIAG

# ================================================================================================ T2
P("\n== T2 Tian+26 groups (consistency)")
T2 = {}
mr2 = 0.0
for grp in ("637", "CEN"):
    CTX["group"] = grp
    for foot, fk in (("canonical", "can"), ("alt", "alt")):
        a0 = NS["C540"].FOOT[fk]; NS["_FOOT_NOW"] = foot
        for src in ("cond", "all"):
            st = NS["run_groups"](a0, src=src, res="RD"); st.pop("Delta", None)
            nm = f"{'PRIMARY (rule unchanged)' if grp == '637' else 'T2-CEN'}|{SRC_TAG[src]}|{foot}"
            T2[nm] = st
            if grp == "637":
                ref = J637["T2"][foot][f"{SRC_TAG[src]}|RD|P|phase"]
                mr2 = max(mr2, abs(st["mean"] - ref["mean"]), abs(st["Z"] - ref["Z"]))
            P(f"  {nm:36s} mean {st['mean']:+.3f}  Z {st['Z']:+.2f}  -> {st['label']}")
check("T2 primary (group rule unchanged) equals CFG637 RD|P|phase (mean, Z; 1e-9)", mr2 <= 1e-9, f"max abs diff {mr2:.1e}")
RES["T2"] = T2

# ================================================================================================ verdict (§3)
P("\n== verdict (FROZEN §3)")


def klass(s, mode):
    t = T3[f"{s}|{mode}"]
    if t["label"] == "PASS":
        return "CLOSES"
    ref = J637["T3"][f"{s}|RD|P|phase"]["headline"]
    if all(abs(t["headline"][f]["eta_median"] - 1) <= 0.75 * abs(ref[f]["eta_median"] - 1) for f in FOOTS):
        return "SHRINKS"
    return "ROBUST TO THE SUPPLY CONVENTION"


VER = {}
for s in ("HCB", "B"):
    kP = klass(s, "P")
    others = {m: klass(s, m) for m in ("HI", "LO", "FLOOR", "RET", "NAT", "P_eps0.5", "P_q0.05", "P_q0.2", "P_uniform")}
    flips = [m for m, k in others.items() if k != kP]
    lab = kP + f" (T3 {T3[f'{s}|P']['label']}; inner {T3[f'{s}|P']['inner_label']})"
    if flips:
        lab += "; BRACKET-DEPENDENT (" + ", ".join(f"{m}: {others[m]}" for m in flips) + ")"
    if T3[f"{s}|P"]["inner_label"] == "FAIL" and J637["T3"][f"{s}|RD|P|phase"]["inner_label"] == "PASS":
        lab += "; INNER BAND BROKEN"
    if not all(T2[f"PRIMARY (rule unchanged)|{s}|{f}"]["label"] == "CLOSES" for f in FOOTS):
        lab += "; CONSISTENCY FAIL (T2)"
    VER[s] = dict(label=lab, primary=kP, brackets=others)
    P(f"  VERDICT [{s}]: {lab}")
RES["verdict"] = VER
RES["checks"] = CHK; RES["elapsed_s"] = round(time.time() - T0, 1)
nf = sum(1 for c in CHK.values() if not c["ok"])
P(f"\n{len(CHK) - nf}/{len(CHK)} checks pass; elapsed {RES['elapsed_s']} s")
json.dump(C4.jclean(RES), open(os.path.join(HERE, "cfg656_gates_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg656_gates.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nf else 0)
