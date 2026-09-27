#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FP20b -- FP20's EXACT PROJECTOR APPLIED TO THE THREE LANES COMMITTED BEFORE IT: FP15 (138f73b69) and FP16 (b3f5759a4) score
KiDS with L352's projector through AT3's kids_switched (the switched fit at the common cell, WITH carrier templates -- where
FP20 found L352's projector worst: up to +187% / -123% at 35 kpc on cored or hollowed carriers), and FP19 (0c18c582f) scores
KiDS with FP6's esd_of_M through FP13's kids_class (FP20's P1 bug: -59% at 35 kpc on the SIS).  Every KiDS number of the three
lanes is re-scored with FP20's committed projector (its source exec'd read-only: ESDFix for the P1 path, M2Fix + the direct
model_M2 for the P2 path), by FP20's drop-in method: each lane's own committed code, exec'd in this lane's private namespace,
the projector swapped, no file of theirs edited, file writes refused.

WHAT IS RE-RUN (only what the KiDS numbers need; the lanes' other gates do not read the projector)
  FP16  its KiDS hosts: the four lens bins' re-accretion model runs at z_l = 0.25 (every kick: 575/600/625/650 km/s; G4) and in
        XR19's nominal web (575/650; G11) -- FP16's own job(), run_all() and q_profile(), 28 runs + references -- then G4's and G11's
        kids_switched.  (XR19's other web brackets feed only X-COP in FP16; they are not KiDS numbers.)
  FP15  its one computed KiDS cell (T5, the yield onset on FP13's H_S at zeta = 94.6, q = 0): the four lens hosts' FK1 retention
        at 575/650 km/s (FP10's retained_fk1 with FP15's set_trigger), in place and optimistic.  FP15's other KiDS entries are the
        text "pass (FP10 B4)" (FP10's numbers, FP20 R11's estimate).
  FP19  its whole main() re-run with the projector swapped after it loads FP13's machinery (KB recomputed): H_K1 at z = 0.25 /
        0.4 / 0.7, the L_Lambda window (B1, whose lower edge is set by KiDS at z = 0.4), the c_y and choice scans (B2, B3), the n scan
        (H6), the stationary scans (A3, A4) and the hybrid table (C) -- by FP19's own code and gates.

CHECKS
  V1 [load-bearing; MUTATE must fail] the projector applied here reproduces the singular isothermal sphere at the 15 KiDS radii
     (P1 grid, point values) and L360's capped carrier template (bin 4; L352's grid, annulus averages) to < 0.2%.
  K1 [load-bearing] CONTROLS: with the committed projector this harness reproduces FP16's G4 (4 kicks) and G11 (2 kicks) and
     FP15's in-place and optimistic KiDS exactly (the host runs and retention profiles recomputed, deterministic seeds); FP19's
     re-run reproduces its committed non-KiDS headline numbers (sigma_8, forest, flagships, SPARC) exactly.
  R1 FP16, R2 FP15, R3 FP19 (reported): before -> after with each lane's own gate; R4 the flips (both directions).
  F  [load-bearing] every re-score completed with finite numbers.   W the ledger.
MUTATE=1 restores the committed projector everywhere: V1 FAILS (rc = 1) and every re-score reproduces the committed numbers.

Run from the lane directory:  python3 FP20b_rescore_fp15_fp16_fp19.py > FP20b_rescore_fp15_fp16_fp19.out 2>&1; echo rc=$? >> ...out
(~10 min; at most two threads.)
"""
import os, sys, io, re, gc, json, math, time, builtins, contextlib, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
for _v in ("AT1_THREADS", "AT3_THREADS", "L357_THREADS"):
    os.environ[_v] = "2"
warnings.filterwarnings("ignore")
import numpy as np

np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "FP20b_rescore_fp15_fp16_fp19"
OUT = {"lane": "FP20b", "mutate": MUTATE, "checks": {}, "numbers": {}, "ledger": []}
CH, TABLE, FAILS = [], [], []
T0 = time.time()
FOOTS = ("canonical", "alt")


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)


def el():
    return f"[{time.time() - T0:.0f} s]"


def check(name, measured, ok, load_bearing=True, reading=None):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing, "name": name}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def row(lane, item, foot, before, after, gate=None, sense="le"):
    vb, va = float(before), float(after)
    vd = ""
    if gate is not None:
        pb = (vb <= gate) if sense == "le" else (vb > gate)
        pa = (va <= gate) if sense == "le" else (va > gate)
        vd = f"{'PASS' if pb else 'FAIL'} -> {'PASS' if pa else 'FAIL'}" + ("  ** FLIP **" if pb != pa else "")
    TABLE.append(dict(lane=lane, item=item, foot=foot, before=vb, after=va, gate=gate, sense=sense, verdict=vd))


def show(lane):
    for r in TABLE:
        if r["lane"] == lane:
            g = "" if r["gate"] is None else f" (gate {'<=' if r['sense'] == 'le' else '>'} {r['gate']:g})"
            P(f"    {r['item'][:70]:70s} {r['foot'][:9]:9s} {r['before']:+10.3f} -> {r['after']:+10.3f}{g:16s} {r['verdict']}")


def guard(lane, fn):
    try:
        return fn()
    except Exception as ex:
        FAILS.append((lane, f"{type(ex).__name__}: {ex}"))
        P(f"    !! {lane}: re-score raised {type(ex).__name__}: {str(ex)[:300]}")
        return None


P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the committed projector is restored everywhere -- V1 must FAIL and every re-score must reproduce the committed numbers ***")

# ================================================================================================= FP20's committed code (read-only)
P20PATH = os.path.join(HERE, "FP20_esd_projection_fix.py")
_s20 = open(P20PATH).read()
P20 = {"np": np, "math": math, "os": os, "io": io, "json": json, "builtins": builtins, "contextlib": contextlib, "MUTATE": False,
       "__name__": "fp20_code", "__file__": P20PATH}
exec(compile(_s20[_s20.index("# ================================================================================================= the harness"):
                  _s20.index("# ================================================================================================= the record's projectors (loaded)")],
             P20PATH, "exec"), P20)
exec(compile(_s20[_s20.index("def model_M2_factory(L, direct):"):_s20.index("def r9_p2():")], P20PATH, "exec"), P20)
ESDFix, M2Fix, shell_mats, model_M2_factory = P20["ESDFix"], P20["M2Fix"], P20["shell_mats"], P20["model_M2_factory"]
exec_slices, lane_env, _ro_open, check_flips, checks_by_id = (P20["exec_slices"], P20["lane_env"], P20["_ro_open"], P20["check_flips"],
                                                              P20["checks_by_id"])
P(f"\n  FP20's committed projector and harness exec'd read-only from {os.path.basename(P20PATH)} (ESDFix, M2Fix, model_M2_factory, "
  f"exec_slices)   {el()}")


def swap_p2(A3):
    """point AT3's switched KiDS machinery (L360's fit on L352's grid) at FP20's projector; returns a restore function."""
    N60 = A3["N60"]; L = N60["L52"]
    saved = (L["model_M2"], N60["project_M2"], dict(A3["BASE60"]))
    if not MUTATE:
        P20["FIX2"] = M2Fix(L["rr"], L["Rp"])
        L["model_M2"] = model_M2_factory(L, True); N60["project_M2"] = P20["FIX2"]
    L["_PROF"].clear(); L["_ESD"].clear()
    A3["BASE60"] = {f: A3["fit_model60"](A3["A052"][f], 0.0, "none", True)[0] for f in FOOTS}

    def restore():
        L["model_M2"], N60["project_M2"] = saved[0], saved[1]; L["_PROF"].clear(); L["_ESD"].clear(); A3["BASE60"] = saved[2]
    return restore


# ================================================================================================= V1  the projector applied here
def v1():
    banner("V1  THE PROJECTOR APPLIED HERE against the analytic standard (FP20 V1/V1b, re-checked in this lane)")
    m6 = exec_slices(os.path.join(HERE, "FP6_gate_survey.py"), [(None, 'banner("K  CONTROLS')], name="fp6_head")[0]
    L52 = {"__name__": "l352", "__file__": os.path.join(REPO, "real_research", "g03_audit_2026", "L352_switch_gauss_compensation.py"), "open": _ro_open}
    with lane_env():
        exec(open(L52["__file__"]).read().split("real_mode = ")[0].replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), L52)
    RR, RP, MPCm, PCm, MS = m6["RR"], m6["RP"], m6["MPCm"], m6["PCm"], m6["MS6"]
    RD = np.genfromtxt(os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar", "Fig-3_Lensing-rotation-curves_Massbin-1.txt"),
                       comments="#")[:, 0]
    K = (200e3) ** 2 / 6.6743e-11; RT = RR[-1]
    x = RD * MPCm / RT
    sis = K / (math.pi * RD * MPCm) * ((1 - np.sqrt(1 - x * x)) / x + np.arccos(x) / 2) * PCm ** 2 / MS
    proj1 = m6["esd_of_M"] if MUTATE else (lambda M, Mb, F=ESDFix(RR, RP, PCm, MS): (RP / MPCm, F(M, Mb)))
    e1 = np.interp(RD, RP / MPCm, proj1(K * np.minimum(RR, RT), 0.0)[1]) / sis - 1
    # L360's capped carrier of bin 4 (FP20 V1b), node densities on L352's grid vs a 16000-shell reference
    rr2, Rp2 = L52["rr"], L52["Rp"]
    Om, OL, rc0, MS2 = L52["Om"], L52["OL"], L52["rho_crit0"], L52["MS"]
    rhoc = rc0 * (Om * 1.25 ** 3 + OL); FB = 0.02237 / (0.02237 + 0.1200); M200 = 5.55e12
    c = 10 ** (0.905 - 0.101 * math.log10(M200 / (1e12 / 0.6736))); r200 = (3 * M200 * MS2 / (4 * math.pi * 200 * rhoc)) ** (1 / 3); rs = r200 / c
    rho_s = M200 * MS2 / (4 * math.pi * rs ** 3 * (math.log(1 + c) - c / (1 + c)))
    rv = (Om * 1.25 ** 3 / (Om * 1.25 ** 3 + OL) + 2 / 3 * 700.0 * (Om * 1.25 ** 3 + OL)) * rhoc

    def rho_c(r):
        rho = np.where(r < r200, rho_s / ((r / rs) * (1 + r / rs) ** 2), 0.0)
        return np.minimum((1 - FB) * rho, rv)
    rf = np.geomspace(1e-5, 30.0, 60000) * MPCm; q = 4 * math.pi * rf ** 2 * rho_c(rf)
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (q[1:] + q[:-1]) * np.diff(rf))])
    rF = np.geomspace(1e-4, 30.0, 16000) * MPCm; MF = np.interp(rF, rf, cum)
    CF = shell_mats(rF, Rp2)[1]
    ann = lambda M2: L52["annulus_esd"](lambda R: np.interp(np.log(R), np.log(Rp2), M2), RD)
    ref = ann(CF @ np.diff(MF) + MF[0])
    proj2 = L52["project_M2"] if MUTATE else M2Fix(rr2, Rp2)
    e2 = ann(proj2(rho_c(rr2))) / ref - 1
    P("    SIS (P1 grid, point) error [%]: " + " ".join(f"{100 * v:+.2f}" for v in e1))
    P("    capped carrier, bin 4 (L352 grid, annulus) error [%]: " + " ".join(f"{100 * v:+.2f}" for v in e2))
    check("V1 THE PROJECTOR APPLIED HERE IS FP20's EXACT ONE: the singular isothermal sphere (P1 grid, point values -- FP19's path) and "
          "L360's capped carrier template (L352's grid, node densities, annulus averages -- FP15/FP16's path) to < 0.2% at the 15 KiDS radii",
          f"max |error| SIS {100 * float(np.max(np.abs(e1))):.3f}%, carrier {100 * float(np.max(np.abs(e2))):.3f}%",
          float(np.max(np.abs(e1))) < 2e-3 and float(np.max(np.abs(e2))) < 2e-3)
    P(f"    {el()}")


guard("V1", v1)


# ================================================================================================= R1  FP16
def r1_fp16():
    banner("R1  FP16 (daughter re-accretion): G4 KiDS at every kick and G11's nominal-web KiDS -- the KiDS hosts re-run by FP16's own code")
    P16 = os.path.join(HERE, "FP16_daughter_reaccretion.py")
    J16 = json.load(open(P16.replace(".py", "_results.json")))["numbers"]
    ns = exec_slices(P16, [(None, 'run_all(JOBS, f"all hosts')], name="fp16_head")[0]
    code = '''
KJ = []
for b_ in range(4):
    M_ = F10["M200_KIDS"][b_]
    for v_ in VKR: KJ.append(job("fk1", M_, F10["ZL"], "%.4f" % alpha_eff(M_), 0.0, v_, wins=(F10["ZL"],),
                                 central=(1.3 * 10 ** F10["LOGMS"][b_], 3.0), tag="kids"))
for b_ in range(4):
    M_ = F10["M200_KIDS"][b_]
    for v_ in (575.0, 650.0): KJ.append(job("fk1", M_, F10["ZL"], "%.4f" % alpha_eff(M_), 0.0, v_, wins=(F10["ZL"],),
                                            central=(1.3 * 10 ** F10["LOGMS"][b_], 3.0), tag="web", web="nominal"))
run_all(KJ, "the KiDS hosts")


def kids_profs(v_, web=None):
    """G4 (FP16:1246-1253) and G11's kdw (FP16:1470-1477), verbatim in effect."""
    profs = []
    for b_ in range(4):
        M200 = F10["M200_KIDS"][b_]; c_ = float(F10["c200_55"](M200))
        Mn, r200, rs = F10["nfw21"](M200, c_, F10["RHOC_ZL"]); pro = np.geomspace(0.02 * rs, 0.999 * r200, 40)
        kw = dict(central=(1.3 * 10 ** F10["LOGMS"][b_], 3.0))
        if web: kw["web"] = web
        jj = job("fk1", M200, F10["ZL"], "%.4f" % alpha_eff(M200), 0.0, v_, wins=(F10["ZL"],), **kw)
        profs.append((pro, np.clip(q_profile(jj, F10["ZL"], pro / r200), 0.0, 2.0)))
    return profs
'''
    with lane_env() as buf:
        exec(compile(code, P16 + " [FP20b: FP16's KiDS jobs]", "exec"), ns)
    P("    " + buf.getvalue().strip().split("\n")[-1].strip() + f"   {el()}")
    A3 = ns["F10"]["A3"]; ks = ns["F10"]["kids_switched"]
    PR = {("G4", v): ns["kids_profs"](v) for v in ns["VKR"]}
    PR.update({("G11", v): ns["kids_profs"](v, "nominal") for v in (575.0, 650.0)})
    before = {k: ks(p) for k, p in PR.items()}
    restore = swap_p2(A3)
    try:
        after = {k: ks(p) for k, p in PR.items()}
    finally:
        restore()
    ctl = [(before[("G4", v)][f], J16["G4"][f"{v:.0f}"]["kids"][f]) for v in ns["VKR"] for f in FOOTS] + \
          [(before[("G11", v)][f], J16["G11"]["kids"][f"{v:.0f}"][f]) for v in (575.0, 650.0) for f in FOOTS]
    dctl = max(abs(a - b) for a, b in ctl)
    P(f"    control: FP16's committed G4/G11 KiDS recomputed with the committed projector: max |d chi^2| {dctl:.1e}")
    for (g, v), b in before.items():
        for f in FOOTS:
            lab = f"G4 KiDS v_k {v:.0f} (modelled re-accretion; gate <= +4)" if g == "G4" else f"G11 KiDS v_k {v:.0f}, XR19 nominal web (reported)"
            row("FP16", lab, f, b[f], after[(g, v)][f], 4.0)
    g4b = all(before[("G4", v)][f] <= 4 for v in ns["VKR"] for f in FOOTS); g4a = all(after[("G4", v)][f] <= 4 for v in ns["VKR"] for f in FOOTS)
    OUT["numbers"]["R1_FP16"] = dict(control_max_dev=dctl, G4={f"{v:.0f}": dict(before=before[("G4", v)], after=after[("G4", v)]) for v in ns["VKR"]},
                                     G11={f"{v:.0f}": dict(before=before[("G11", v)], after=after[("G11", v)]) for v in (575.0, 650.0)},
                                     G4_verdict=[g4b, g4a], r200_retention={f"{v:.0f}": [float(p[1][-1]) for p in PR[("G4", v)]] for v in ns["VKR"]})
    show("FP16")
    P(f"    FP16 G4 (KiDS passes at every kick, both footings): {'PASS' if g4b else 'FAIL'} -> {'PASS' if g4a else 'FAIL'}   {el()}")
    return dctl


D16 = guard("FP16", r1_fp16)
gc.collect()


# ================================================================================================= R2  FP15
def r2_fp15():
    banner("R2  FP15 (zero-knob dark sector): its one computed KiDS cell -- T5's yield onset on H_S (zeta 94.6, q = 0), in place and optimistic")
    P15 = os.path.join(HERE, "FP15_zero_knob_dark_sector.py")
    J15 = json.load(open(P15.replace(".py", "_results.json")))["numbers"]
    ZETA_S = float(J15["T4e"]["zeta"])
    ns = exec_slices(P15, [(None, 'banner("C0  CONTROLS')], name="fp15_head")[0]
    F = ns["F"]; A3 = F["A3"]; ks = F["kids_switched"]; K_HI = ns["K_HI"]
    ns["set_trigger"](ZETA_S, 0.0)
    jobs = [(v_, b) for v_ in ns["VKS"] for b in range(4)]

    def prof(j):                                                                    # FP15:1093-1101, verbatim in effect
        v_, b = j
        M200 = F["M200_KIDS"][b]; c_ = float(F["c200_55"](M200))
        Mn, r200, rs = F["nfw21"](M200, c_, F["RHOC_ZL"])
        pro = np.geomspace(0.02 * rs, 0.999 * r200, 40)
        Mb_fn = F["hernquist"](1.3 * 10 ** F["LOGMS"][b], 3.0)
        Pp = F["prof_bary"](M200, c_, F["ZL"], Mb_fn, rhoc=F["RHOC_ZL"])
        r_, S_ = ns["DB"](Pp, v_)
        rv = F["front"](r_, S_, 1.0 / K_HI)
        ratio_p, _ = F["retained_fk1"](Mb_fn, M200, c_, list(pro), rv, v_, F["RHOC_ZL"], N=8000)
        return j, (pro, np.asarray(ratio_p))
    with lane_env():
        PR = dict(prof(j) for j in jobs)                                               # serial: DB's defaults are shared state
    ns["DB"].__defaults__ = ns["DB_DEF"]
    P(f"    the four lens hosts' FK1 retention at 575/650 km/s recomputed with FP15's trigger (zeta {ZETA_S:.4f}, q = 0)   {el()}")
    profs = {v_: [PR[(v_, b)] for b in range(4)] for v_ in ns["VKS"]}
    zero = [(p[0], np.zeros_like(p[1])) for p in profs[ns["VKS"][0]]]
    before = {("inplace", v_): ks(profs[v_]) for v_ in ns["VKS"]}; before["zero"] = ks(zero)
    restore = swap_p2(A3)
    try:
        after = {("inplace", v_): ks(profs[v_]) for v_ in ns["VKS"]}; after["zero"] = ks(zero)
    finally:
        restore()
    com = J15["T5"]["yield_cell"]["kids"]
    ctl = [(before[("inplace", v_)][f], com[f"{v_:.0f}"]["inplace"][f]) for v_ in ns["VKS"] for f in FOOTS]
    dctl = max(abs(a - b) for a, b in ctl)
    opt_zero = max(abs(before["zero"][f] - com[f"{v_:.0f}"]["optimistic"][f]) for v_ in ns["VKS"] for f in FOOTS)
    P(f"    control: FP15's committed in-place KiDS recomputed with the committed projector: max |d chi^2| {dctl:.1e}; its committed "
      f"OPTIMISTIC values equal the zero-carrier fit to {opt_zero:.1e} (every bin's template max(q - F_b, 0) is zero), so the optimistic "
      f"reading re-scores as the zero-carrier fit")
    for v_ in ns["VKS"]:
        for f in FOOTS:
            row("FP15", f"T5 yield-onset cell, KiDS in place, v_k {v_:.0f} (gate <= +4)", f, com[f"{v_:.0f}"]["inplace"][f], after[("inplace", v_)][f], 4.0)
            row("FP15", f"T5 yield-onset cell, KiDS optimistic, v_k {v_:.0f} (gate <= +4)", f, com[f"{v_:.0f}"]["optimistic"][f], after["zero"][f], 4.0)
    OUT["numbers"]["R2_FP15"] = dict(control_max_dev=dctl, optimistic_is_zero_carrier=opt_zero, zeta=ZETA_S,
                                     inplace={f"{v_:.0f}": dict(before=before[("inplace", v_)], after=after[("inplace", v_)]) for v_ in ns["VKS"]},
                                     optimistic=dict(before=before["zero"], after=after["zero"]))
    show("FP15")
    P("    FP15's other KiDS entries (T5's 'FK1 q = 7/4' and 'shared q = 3.75' rows) are the text 'pass (FP10 B4)': FP10's committed "
      f"numbers, estimated in FP20 R11 (no carrier: -6.0/-0.5 -> about -4.1/+0.0; still pass)   {el()}")
    return max(dctl, opt_zero)


D15 = guard("FP15", r2_fp15)
gc.collect()


# ================================================================================================= R3  FP19 (its whole main re-run)
def r3_fp19():
    banner("R3  FP19 (H_K1, the repaired separator): its main() re-run whole with the projector swapped after it loads FP13's machinery")
    P19 = os.path.join(HERE, "FP19_hs_repair.py")
    old = json.load(open(P19.replace(".py", "_results.json")))
    src = open(P19).read()
    mod = src[:src.index("\ndef main():")]
    body = src[src.index("\ndef main():") + len("\ndef main():"):src.index('    fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))')]
    body = "\n".join(l_[4:] if l_.startswith("    ") else l_ for l_ in body.split("\n"))
    cut = body.index("\nNS = load_fp13()\n") + len("\nNS = load_fp13()\n")
    ns = {"__file__": P19, "__name__": "fp19_rerun", "open": _ro_open}

    def hook(n):
        NS = n["NS"]; m6 = NS["M6"]
        if not MUTATE:
            fx = ESDFix(m6["RR"], m6["RP"], m6["PCm"], m6["MS6"])
            m6["esd_of_M"] = lambda M, Mb, fx=fx, m6=m6: (m6["RP"] / m6["MPCm"], fx(M, Mb))
        NS["KB"] = {f: NS["kids_class"](NS["A0"][f]) for f in NS["FOOTS"]}
    with lane_env():
        exec(compile(mod, P19, "exec"), ns)
        exec(compile(body[:cut], P19, "exec"), ns)
        hook(ns)
        exec(compile("\n" * body[:cut].count("\n") + body[cut:], P19, "exec"), ns)
    on, nn = old["numbers"], json.loads(json.dumps(ns["OUT"]["numbers"], default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o)))
    # control: the projector-free headline numbers are reproduced exactly
    dctl = 0.0
    for grp in ("s8", "forest", "flag", "sparc"):
        for k_, v in on["H1"][grp].items():
            w = nn["H1"][grp][k_]; dctl = max(dctl, abs(w - v) if v == 0 else abs(w / v - 1))
    P(f"    control: the re-run reproduces FP19's committed H1 sigma_8, forest, flagships and SPARC to {dctl:.1e} (they do not read the projector)")
    for z, key in ((0.25, "kids"), (0.4, "kids@0.4"), (0.7, "kids@0.7")):
        for f in FOOTS:
            row("FP19", f"H1 the H_K1 HEADLINE: KiDS at z = {z}" + (" (a prediction, reported)" if z == 0.7 else " (gate <= +9)"), f,
                on["H1"][key][f], nn["H1"][key][f], None if z == 0.7 else 9.0)
    lo_b, hi_b = on["B1"]["window"]; lo_a, hi_a = nn["B1"]["window"]
    row("FP19", "B1 the L_Lambda window, lower edge [Mpc] (set by KiDS at z = 0.4)", "both", lo_b, lo_a)
    row("FP19", "B1 the L_Lambda window, upper edge [Mpc] (set by sigma_8)", "both", hi_b, hi_a)
    for LL in ("2.5", "2.6", "2.65", "2.7", "2.8", "3.0"):
        for f in FOOTS:
            row("FP19", f"B1 L_Lambda = {LL} Mpc: KiDS at z = 0.4 (gate <= +9)", f, on["B1"]["scan"][LL]["kids@0.4"][f], nn["B1"]["scan"][LL]["kids@0.4"][f], 9.0)
    for n_ in ("2.5", "3.0"):
        for f in FOOTS:
            row("FP19", f"H6 n = {n_} (L(0.25) fixed): KiDS at z = 0.4 (gate <= +9)", f, on["H6"]["n_scan"][n_]["kids@0.4"][f], nn["H6"]["n_scan"][n_]["kids@0.4"][f], 9.0)
    for mu in ("70.0", "100.0", "150.0"):
        row("FP19", f"A4 stationary law, cost mu = {mu}: KiDS at z = 0.4 (gate <= +9)", "max", on["A4"]["scan"][f"{mu}/0.013"]["kids04"],
            nn["A4"]["scan"][f"{mu}/0.013"]["kids04"], 9.0)
    for f in FOOTS:
        row("FP19", "A3 closed band-pass (z <= z_q0): KiDS at z = 0.25 (fails iff > +9)", f, on["A3"]["closed"]["kids"][f], nn["A3"]["closed"]["kids"][f], 9.0, "gt")
    for cy in ("1/Z^3", "1/Z^2", "kappa^6"):
        for f in FOOTS:
            row("FP19", f"B2 yield coefficient {cy}: KiDS at z = 0.7 (reported)", f, on["B2"]["candidates"][cy]["kids@0.7"][f], nn["B2"]["candidates"][cy]["kids@0.7"][f])
    hyb = {k_: (v["ok"].get("KiDS"), v["ok"].get("KiDS@0.4"), nn["C"][k_]["ok"].get("KiDS"), nn["C"][k_]["ok"].get("KiDS@0.4")) for k_, v in on["C"].items()}
    P("    C the hybrid table, KiDS / KiDS@0.4 flags: " + "; ".join(f"{k_.strip()}: {a}/{b} -> {c}/{d}" for k_, (a, b, c, d) in hyb.items()))
    fl = check_flips(ns["CH"], old["checks"])
    P(f"    FP19's own checks: {sum(1 for c in ns['CH'] if c[1])}/{len(ns['CH'])} pass (committed {sum(1 for v in old['checks'].values() if v['ok'])}/"
      f"{len(old['checks'])}); flips: " + (", ".join(f"{f_['id']} {f_['before']}->{f_['after']}{'' if f_['load_bearing'] else ' (rep.)'}" for f_ in fl) or "none"))
    OUT["numbers"]["R3_FP19"] = dict(control_max_dev=dctl, H1={k: dict(before=on["H1"][k], after=nn["H1"][k]) for k in ("kids", "kids@0.4", "kids@0.7")},
                                     B1_window=dict(before=[lo_b, hi_b], after=[lo_a, hi_a]), hybrids=hyb, flips=fl)
    show("FP19")
    P(f"    {el()}")
    return dctl, fl


R3 = guard("FP19", r3_fp19)

# ================================================================================================= K1  controls, R4 flips, F, W
banner("K1 / R4  CONTROLS AND THE FLIPS")
dmax = [d for d in (D16, D15, (R3[0] if R3 else None)) if d is not None]
check("K1 CONTROLS: with the committed projector this harness reproduces FP16's G4 (4 kicks) and G11 (2 kicks) and FP15's in-place and "
      "optimistic KiDS exactly (their host runs and retention profiles recomputed by their own code, deterministic seeds); FP19's re-run "
      "reproduces its committed sigma_8, forest, flagships and SPARC exactly (numbers the projector cannot touch)",
      f"FP16 {D16 if D16 is None else f'{D16:.1e}'}; FP15 {D15 if D15 is None else f'{D15:.1e}'}; FP19 {R3[0] if R3 else None}",
      len(dmax) == 3 and max(dmax) < 1e-6)
flips = [r for r in TABLE if "FLIP" in r["verdict"]]
P(f"    {len(TABLE)} rows re-scored; {len(flips)} cross their lane's gate:")
for r in flips:
    P(f"      {r['lane']:5s} {r['item'][:84]:84s} {r['foot'][:9]:9s} {r['before']:+9.2f} -> {r['after']:+9.2f}  {r['verdict']}")
fl19 = R3[1] if R3 else []
if MUTATE:
    same = all(abs(r["after"] - r["before"]) < 1e-6 for r in TABLE)
    P(f"    MUTATE control: with the committed projector every re-score reproduces the committed number: {same}")
    OUT["numbers"]["mutate_reproduces_committed"] = same
check("R4 (reported) THE FLIPS, both directions: gate crossings in the before/after table, and FP19's own checks that change verdict",
      f"{len(flips)} gate crossings; FP19 check flips: " + (", ".join(f"{f_['id']} {f_['before']}->{f_['after']}" for f_ in fl19) or "none"),
      True, load_bearing=False)
OUT["numbers"]["table"] = TABLE
nonfinite = [(r["lane"], r["item"]) for r in TABLE if not (math.isfinite(r["after"]) and math.isfinite(r["before"]))]
check("F EVERY RE-SCORE COMPLETED: no re-run raised and every number is finite", f"errors {FAILS or 'none'}; non-finite {nonfinite or 'none'}",
      not FAILS and not nonfinite and len(TABLE) > 0)


def tb(lane, prefix, foot):
    for r in TABLE:
        if r["lane"] == lane and r["item"].startswith(prefix) and r["foot"] == foot:
            return r["before"], r["after"]
    return float("nan"), float("nan")


def span(lane, prefix):
    rs = [r for r in TABLE if r["lane"] == lane and r["item"].startswith(prefix)]
    if not rs:
        return "n/a"
    b = [r["before"] for r in rs]; a = [r["after"] for r in rs]
    return f"{min(b):+.1f}..{max(b):+.1f} -> {min(a):+.1f}..{max(a):+.1f}"


banner("W  THE LEDGER")
LEDGER = [
    ("F20b-a", f"FP16's G4 KiDS pass with the modelled re-accretion, every kick, both footings: {span('FP16', 'G4 KiDS')} (gate <= +4)",
     "DERIVED" if all(r["after"] <= 4 for r in TABLE if r["lane"] == "FP16" and r["item"].startswith("G4")) else "FAILS",
     "corrected by FP20b (R1: FP16's KiDS hosts re-run by its own code; FP20's projector)"),
    ("F20b-b", f"FP16 G11: KiDS in XR19's nominal web (reported) {span('FP16', 'G11 KiDS')}", "CONSTRAINT", "corrected by FP20b (R1)"),
    ("F20b-c", f"FP15's T5 yield-onset cell passes KiDS: in place {span('FP15', 'T5 yield-onset cell, KiDS in place')}, optimistic "
               f"{span('FP15', 'T5 yield-onset cell, KiDS optimistic')} (gate <= +4); its other KiDS entries are FP10 B4's text",
     "DERIVED" if all(r["after"] <= 4 for r in TABLE if r["lane"] == "FP15") else "FAILS", "corrected by FP20b (R2)"),
    ("F20b-d", f"FP19's H_K1 passes KiDS at z = 0.25 ({span('FP19', 'H1 the H_K1 HEADLINE: KiDS at z = 0.25')}) and 0.4 "
               f"({span('FP19', 'H1 the H_K1 HEADLINE: KiDS at z = 0.4')})",
     "DERIVED" if all(r["after"] <= 9 for r in TABLE if r["lane"] == "FP19" and r["item"].startswith("H1") and "0.7" not in r["item"]) else "FAILS",
     "corrected by FP20b (R3: FP19's main re-run whole)"),
    ("F20b-e", f"FP19's headline prediction: KiDS for lenses at z = 0.7 {span('FP19', 'H1 the H_K1 HEADLINE: KiDS at z = 0.7')} (the yield "
               "switches the phantom off beyond ~0.1-0.3 Mpc)", "CONSTRAINT", "corrected by FP20b (R3)"),
    ("F20b-f", f"FP19's L_Lambda window: {OUT['numbers'].get('R3_FP19', {}).get('B1_window', {}).get('before')} -> "
               f"{OUT['numbers'].get('R3_FP19', {}).get('B1_window', {}).get('after')} Mpc (lower edge from KiDS at z = 0.4); the declared "
               "L_Lambda = 2.9 Mpc " + ("stays inside" if (OUT['numbers'].get('R3_FP19', {}).get('B1_window', {}).get('after') or [9, 0])[0] <= 2.9
                                        <= (OUT['numbers'].get('R3_FP19', {}).get('B1_window', {}).get('after') or [9, 0])[1] else "LEAVES it"),
     "CONSTRAINT", "corrected by FP20b (R3)"),
]
for k_, what, st, why in LEDGER:
    P(f"    {k_:7s} {st:11s} {what}  --  {why}")
OUT["ledger"] = [dict(link=k_, what=w, status=s_, basis=b_) for k_, w, s_, b_ in LEDGER]
check("W (reported) the ledger", f"{len(LEDGER)} links", True, load_bearing=False)

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
banner("VERDICT")
P(f"""  FP15, FP16 and FP19 re-scored with FP20's exact projector by their own committed code: {len(flips)} gate crossings in
  {len(TABLE)} rows; FP19's own checks that flip: {', '.join(f_['id'] for f_ in fl19) or 'none'}.  See the table (R1-R3) and the
  ledger; not 'closed'.  Time {time.time() - T0:.0f} s.""")
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), n_fail, time.time() - T0
fn = os.path.join(HERE, f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json")
with builtins.open(fn, "w") as fh:
    json.dump(OUT, fh, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating, np.integer)) else str(o)))
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {os.path.basename(fn)}")
sys.exit(0 if n_fail == 0 else 1)
