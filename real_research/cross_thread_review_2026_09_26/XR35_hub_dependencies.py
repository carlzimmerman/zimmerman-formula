#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR35_hub_dependencies.py -- WHICH HUB LANES LEAN ON THE DEFECTIVE KiDS PROJECTORS, BY HOW MUCH, AND DOES ANY VERDICT MOVE?
Cross-thread review lane XR35, part 2 (2026-09-27).  Read-only on every committed file; XR28 (in flight in another lane) is
read, never run.

WHY.  FP20 (7a8c25321) listed the hub lanes that use either defective projection with a token scan of the sources (its H
section).  A token scan cannot tell a call from a docstring, a regex, a substring or a same-named local function.  This lane
traces the lanes the review asked about -- XR10's validator rows, XR18 (frw_yield_crossing; state_separator via FP9/FP13's
kids_class), XR25_lambda_regulator, XR29_mw_outer_curve, and XR28 (list only) -- at the level of the code, says which of their
checks consume a projected number, prices each, and re-runs only where a verdict could flip.  XR35_kids_rescore.py re-scores
the M* chain itself (DE10, XR9, XR14); its results are read here for XR10's rows.

WHERE A VERDICT COULD FLIP.  XR10's check E fails (rc = 1) whenever an enabled approximation rule's committed evidence stops
holding.  Two enabled rules rest on KiDS numbers computed with the defective P2 projector:
  SIGMA0_FOR_SIGMA1 : DE8's sigma_shift_by_branch r200/upper <= 0.4 and nfw/upper <= 0.4 (committed 0.39991 and 0.31318 --
                      the first sits 9e-5 under its bar);
  HARDW_FOR_SMOOTH  : DE9's MOND-sector window at p = 1 contains x_c0 = 2.5 at w = 0.1 and 0.25 (its upper edge is DE9's
                      switch-only KiDS cap / E(0.25)^2; this rule is one of the two that carry XR14.kids, the only row
                      claimed ON M*).
Both are re-scored here with FP20's drop-ins (DE8's upper-branch scan re-run whole; DE9's cap_kids re-run at the two widths),
each after a control that reproduces the committed numbers exactly with the committed projector.

PRE-DECLARED (written before any corrected-projection number of DE8 or DE9 was computed; the writer's expectation in brackets)
  HX1 [reported] SIGMA0_FOR_SIGMA1's evidence holds under the corrected projection: DE8's upper-branch sigma shift <= 0.4 on both
      outer conventions.  [uncertain: the committed r200/upper value sits 9e-5 under the bar]
  HX2 [reported] HARDW_FOR_SMOOTH's evidence holds: DE9's MOND-sector window at p = 1 still contains x_c0 = 2.5 at w = 0.1 and
      0.25.  [expected to hold -- NOT a blind prediction: XR35_kids_rescore's main run, read before this was written, showed
      XR9's C6 flip (the w = 0.25 switch-only cap falls below 4.347) and p1_x2.5's switch-only KiDS at x_c,eff = 3.25 still
      passing (-21.5/-17.5), which brackets the new cap inside the window]

CHECKS
  P0 [load-bearing; MUTATE must fail] the corrected slot is FP20's drop-in: CellFix (DE8's cells) and M2Fix (node densities)
     reproduce the annulus-averaged Delta Sigma of the truncated singular isothermal sphere and of NFW 3e12 c4 (Wright &
     Brainerd) to 0.04% at the 15 KiDS radii (the committed projector is -2.6% / +8.2% there).
  D1 [load-bearing] THE TRACE: an AST-level scan of each lane (names, attributes, imports, defs, and string constants EQUAL to a
     projector's name -- the keys the lanes use to pull functions out of exec'd namespaces; docstrings, messages and regex
     patterns are longer strings and do not match), judged on CALLS (a bare same-named variable is listed, not counted -- the
     first development run counted XR10's local set 'gates'; see the README), each call and each 'kids'-keyed access mapped to
     the check it feeds, finds: XR18_frw_yield_crossing and XR25_lambda_regulator reach FP6's esd_of_M only through FP9's
     kids_class, XR18_state_separator only through FP13's gates(), and in all three the projected number feeds ONLY the K1
     control; XR10_answer_validator and XR29_mw_outer_curve call nothing of the kind (FP20's H flagged them on a regex string
     and on the substring 'fit_cell' of 'refit_cell'), and XR29 reads nothing projected from the FP11 it exec's; the XR28 files
     call only their own model_esd.
  D2 (reported) the effect sizes on those K1 controls, read from FP20's committed re-score (R2: FP9 H2; R3: FP13 H1 at z = 0.25,
     0.4, 0.7) after checking that each lane's committed K1 value is FP20's 'before'; each K1 would fail on a re-run (pinned to a
     defective-projection number); no other check of those lanes consumes KiDS.
  K1 [load-bearing] CONTROL: with the committed projector, DE8's upper-branch scan (2 outer conventions x 36 cells x 2 sigma x 2
     footings) and its two sigma shifts are reproduced exactly (1e-9).
  K2 [load-bearing] CONTROL: with the committed projector, DE9's MOND-sector switch-only KiDS caps at w = 0.1 and 0.25
     (4.478906 / 4.347266) are reproduced exactly.
  X1 (reported; = HX1) SIGMA0_FOR_SIGMA1's evidence under the corrected projection, and DE8's upper-branch verdict counts.
  X2 (reported; = HX2) HARDW_FOR_SMOOTH's evidence under the corrected projection: the new caps and DE9's window at p = 1.
  X3 (reported) XR10's KiDS rows: each row's lane, the projector it scores with, and its before -> after where re-scored (here,
     XR35_kids_rescore, FP20); XR10's own axis verdicts consume no projected number.
  XR28 (reported) the in-flight lane's dependency, listed from its sources (not run).
  F  [load-bearing] every re-score completed with finite numbers.
MUTATE=1 puts the committed projectors in the corrected slot: P0 must FAIL (rc = 1) and X1/X2's 'after' must equal 'before'.
Outputs *_MUTATE.out / *_results_MUTATE.json.

SCOPE.  Dependencies on the three projectors named by FP20 only.  kappa = 1/2 is FITTED (Z = 5.7888).  Not 'closed'.
Run from the repository root (after XR35_kids_rescore.py):
    python3 real_research/cross_thread_review_2026_09_26/XR35_hub_dependencies.py        (MUTATE=1 first)
"""
import os, sys, io, re, ast, json, math, time, builtins, contextlib, warnings, subprocess
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
warnings.filterwarnings("ignore")
import numpy as np

np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR35_hub_dependencies"
T0 = time.time()
FEET = ("canonical", "alt")


class _Tee:
    def __init__(self, fh): self.fh, self.so = fh, sys.__stdout__
    def write(self, s): self.so.write(s); self.fh.write(s)
    def flush(self): self.so.flush(); self.fh.flush()


_OUTFH = builtins.open(os.path.join(HERE, SLUG + ("_MUTATE" if MUTATE else "") + ".out"), "w")
sys.stdout = _Tee(_OUTFH)
CH, OUT = [], {"lane": "XR35 part 2 (hub dependencies on the defective KiDS projectors)", "mutate": MUTATE, "checks": {}, "numbers": {}}


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)


def el():
    return f"[{time.time() - T0:.0f} s]"


def check(name, measured, ok, load_bearing=True, reading=None):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing, "name": name}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def jdefault(o):
    return o.tolist() if hasattr(o, "tolist") else (bool(o) if isinstance(o, np.bool_) else str(o))


def jnorm(o):
    return json.loads(json.dumps(o, default=jdefault))


def rel(p):
    return os.path.relpath(p, REPO)


def _ro_open(file, mode="r", *a, **k):
    if any(c in mode for c in "wax+"):
        raise PermissionError(f"XR35 refuses to write {os.path.basename(str(file))!r} from a re-executed lane")
    return builtins.open(file, mode, *a, **k)


@contextlib.contextmanager
def lane_env():
    old = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            yield buf
    finally:
        if old is None:
            os.environ.pop("MUTATE", None)
        else:
            os.environ["MUTATE"] = old


def git_head(relpath):
    r = subprocess.run(["git", "-C", REPO, "show", f"HEAD:{relpath}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def _slice(src, a, b):
    i = src.index(a); return src[i:src.index(b, i)]


P(__doc__.split("PRE-DECLARED")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the committed projectors are put in the corrected slot -- P0 must FAIL, and X1/X2's 'after' must equal "
      "'before' ***")

# ================================================================================================= FP20's drop-ins (git HEAD)
FP20_REL = "real_research/derivation_chain_2026/FP20_esd_projection_fix.py"
FP20_SRC = git_head(FP20_REL)
FPNS = {"np": np, "math": math, "MUTATE": MUTATE, "__name__": "fp20_dropins"}
exec(compile(_slice(FP20_SRC, "def shell_mats(edges, Rv):", "# ================================================================================================= the record's projectors (loaded)"),
             "FP20_esd_projection_fix.py[drop-ins, git HEAD]", "exec"), FPNS)
exec(compile(_slice(FP20_SRC, "def model_M2_factory(L, direct):", "\n\ndef r9_p2():"), "FP20_esd_projection_fix.py[model_M2_factory, git HEAD]",
             "exec"), FPNS)
CellFix, M2Fix, model_M2_factory = FPNS["CellFix"], FPNS["M2Fix"], FPNS["model_M2_factory"]
DEDIR = os.path.join(REPO, "real_research", "dark_energy_2026")
P8 = os.path.join(DEDIR, "DE8_kids_sigma_axis_both_branches.py")
P9 = os.path.join(DEDIR, "DE9_smooth_gate_window.py")
for _p in (P8, P9):
    assert builtins.open(_p).read() == git_head(rel(_p)), f"{rel(_p)} differs from git HEAD"
SRC8 = builtins.open(P8).read()
M_C1 = "# ============================================================================================ C1 C2 C3 controls"


def load_de8():
    D8 = {"__name__": "de8", "__file__": P8, "open": _ro_open}
    with lane_env():
        exec(compile(SRC8.split(M_C1)[0].replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), P8, "exec"), D8)
    return D8


def patch_de8(D8, lab):
    """the corrected slot in a DE8 namespace: esd_from_mlens's m2_of_rho -> CellFix; the carrier templates (node densities) ->
    M2Fix; L352's model_M2 -> FP20's direct path; every cache cleared; L352's unswitched base recomputed."""
    L = D8["L52"]; Rp, Rd = D8["Rp"], D8["Rd"]
    cells = D8["m2_of_rho"] if MUTATE else CellFix(D8["faces"], Rp)
    nodes = L["project_M2"] if MUTATE else M2Fix(L["rr"], Rp)
    FPNS["FIX2"] = M2Fix(L["rr"], Rp)
    D8["m2_of_rho"] = cells
    for key_, rc in D8.get("RHOC", {}).items():
        D8["TC"][key_] = D8["annulus_esd"](lambda R, M2=nodes(rc): np.interp(np.log(R), np.log(Rp), M2), Rd[key_[2]])
    L["model_M2"] = model_M2_factory(L, True); L["_PROF"].clear(); L["_ESD"].clear(); D8["_ESD"].clear()
    base = {f_: D8["fit_model"](D8["A0"][f_], 0.0, "none", True)[0] for f_ in FEET}
    D8["BASE"] = base
    return base


# ================================================================================================= P0: the corrected slot
banner("P0  THE CORRECTED SLOT IS FP20's DROP-IN (the SIS and an NFW halo, annulus averages at the 15 KiDS radii)")
D8P = load_de8()
LP = D8P["L52"]; rr, Rp, RD = LP["rr"], LP["Rp"], LP["Rd"][0]; G, MS, MPCm = LP["G"], LP["MS"], LP["MPCm"]
RT = rr[-1]; ann = LP["annulus_esd"]
K = (200e3) ** 2 / G
RHOC = LP["rho_crit0"] * (LP["Om"] * 1.25 ** 3 + LP["OL"])
r200 = (3 * 3e12 * MS / (4 * math.pi * 200 * RHOC)) ** (1 / 3); rs = r200 / 4.0
rhos = 3e12 * MS / (4 * math.pi * rs ** 3 * (math.log(5.0) - 4.0 / 5.0))
PR = {"SIS V=200": dict(M=lambda r: K * np.minimum(r, RT), rho=lambda r: np.where(r <= RT, K / (4 * math.pi * r ** 2), 0.0),
                        M2=lambda R: K * (RT - np.sqrt(RT ** 2 - R ** 2) + R * np.arccos(R / RT))),
      "NFW 3e12 c4": dict(M=lambda r: 4 * math.pi * rhos * rs ** 3 * (np.log1p(np.minimum(r, RT) / rs) - (np.minimum(r, RT) / rs) / (1 + np.minimum(r, RT) / rs)),
                          rho=lambda r: np.where(r <= RT, rhos / ((r / rs) * (1 + r / rs) ** 2), 0.0),
                          M2=lambda R: 4 * math.pi * rhos * rs ** 3 * (np.log(R / rs / 2) + np.where(
                              R < rs, np.arccosh(1 / np.minimum(R / rs, 1 - 1e-15)) / np.sqrt(np.maximum(1 - (R / rs) ** 2, 1e-300)),
                              np.arccos(1 / np.maximum(R / rs, 1 + 1e-15)) / np.sqrt(np.maximum((R / rs) ** 2 - 1, 1e-300)))))}
cells_slot = D8P["m2_of_rho"] if MUTATE else CellFix(D8P["faces"], Rp)
nodes_slot = LP["project_M2"] if MUTATE else M2Fix(rr, Rp)
p0 = {}
for nm, pr in PR.items():
    ref = ann(pr["M2"], RD)
    en = ann(lambda R, M2=nodes_slot(pr["rho"](rr)): np.interp(np.log(R), np.log(Rp), M2), RD) / ref - 1
    old = D8P["m2_of_rho"]
    try:
        D8P["m2_of_rho"] = cells_slot
        ec = D8P["esd_from_mlens"](0.0, pr["M"](D8P["rf"]), 0) / ref - 1
    finally:
        D8P["m2_of_rho"] = old
    p0[nm] = (float(np.max(np.abs(en))), float(np.max(np.abs(ec))))
OUT["numbers"]["P0"] = p0
check("P0 THE CORRECTED SLOT IS FP20's DROP-IN: M2Fix (node densities) and CellFix (DE8's cells) reproduce the SIS and NFW 3e12 c4 "
      "annulus Delta Sigma to 0.04% at the 15 KiDS radii", "; ".join(f"{nm}: nodes {100 * a_:.4f}%, cells {100 * b_:.4f}%" for nm, (a_, b_) in p0.items()),
      max(max(v) for v in p0.values()) <= 4e-4)

# ================================================================================================= D1: the trace
banner("D1  THE TRACE: code-level references to the defective projectors in the hub lanes named, and the checks they feed")
P1_TOK = {"esd_of_M", "kids_class", "kids_chi2", "kids_isolated", "kids_score", "gates"}
P2_TOK = {"project_M2", "annulus_esd", "esd_from_mlens", "m2_of_rho", "esd_bin", "fit_model", "fit_cell", "fit_comb", "kids_switched", "model_esd"}
TOK = P1_TOK | P2_TOK
HUBF = ["XR10_answer_validator.py", "XR18_frw_yield_crossing.py", "XR18_state_separator.py", "XR25_lambda_regulator.py", "XR25_common.py",
        "XR29_mw_outer_curve.py", "XR28_common.py", "XR28_controls.py", "XR28_outskirts_L.py", "XR28_hot_phase.py"]


def check_ids(tree, src_lines):
    """(line, check id) for every call check("<ID> ...") / check(f"<ID> ...") / R.check(...) in the file."""
    out = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and ((isinstance(n.func, ast.Name) and n.func.id == "check") or
                                        (isinstance(n.func, ast.Attribute) and n.func.attr == "check")) and n.args:
            a0 = n.args[0]
            while isinstance(a0, ast.BinOp):
                a0 = a0.left
            s = a0.value if isinstance(a0, ast.Constant) and isinstance(a0.value, str) else \
                (a0.values[0].value if isinstance(a0, ast.JoinedStr) and a0.values and isinstance(a0.values[0], ast.Constant) else "")
            if s:
                out.append((n.lineno, s.split()[0]))
    return sorted(out)


def _key(sl):
    """the constant text of a subscript key (a string, or an f-string's constant parts)."""
    if isinstance(sl, ast.Constant) and isinstance(sl.value, str):
        return sl.value
    if isinstance(sl, ast.JoinedStr):
        return "".join(v.value for v in sl.values if isinstance(v, ast.Constant) and isinstance(v.value, str))
    return None


def trace(path):
    """code-level references to the projectors; the checks their CALLS and every 'kids'-keyed access feed; the containers that
    hold a projected number and their later uses (with their keys), for the reader."""
    src = builtins.open(path).read()
    tree = ast.parse(src)
    lines = src.split("\n")
    defs = {n.name: n.lineno for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    refs = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Name) and n.id in TOK:
            refs.append((n.lineno, n.id, "name"))
        elif isinstance(n, ast.Attribute) and n.attr in TOK:
            refs.append((n.lineno, n.attr, "attribute"))
        elif isinstance(n, ast.Constant) and isinstance(n.value, str) and n.value in TOK:
            refs.append((n.lineno, n.value, "string key"))
        elif isinstance(n, ast.ImportFrom):
            refs += [(n.lineno, a.name, "import") for a in n.names if a.name in TOK]
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name in TOK:
            refs.append((n.lineno, n.name, "def"))
    refs = sorted(set(refs))
    chk = check_ids(tree, lines)

    def feeds(L_):
        nxt = [cid for (cl, cid) in chk if cl >= L_]
        return nxt[0] if nxt else "(after the last check: results only)"
    calls = sorted({(n.lineno, n.func.id if isinstance(n.func, ast.Name) else n.func.attr) for n in ast.walk(tree) if isinstance(n, ast.Call)
                    and ((isinstance(n.func, ast.Name) and n.func.id in TOK) or (isinstance(n.func, ast.Attribute) and n.func.attr in TOK))})
    recording = set()                                                  # statements that only record results (targets keyed 'numbers')
    for s in ast.walk(tree):
        if isinstance(s, ast.Assign) and any(_key(m.slice) == "numbers" for t in s.targets for m in ast.walk(t) if isinstance(m, ast.Subscript)):
            recording.update(range(s.lineno, getattr(s, "end_lineno", s.lineno) + 1))
    kidskeys = sorted({(n.lineno, _key(n.slice)) for n in ast.walk(tree) if isinstance(n, ast.Subscript) and _key(n.slice) is not None
                       and "kids" in _key(n.slice).lower() and n.lineno not in recording})
    fed = sorted({feeds(L_) for L_, tok in calls if defs.get(tok) != L_} | {feeds(L_) for L_, _ in kidskeys})
    # the containers a call's result (or a 'kids'-keyed value) is stored in, and their later uses (after the check fed), with keys;
    # generic loop names (v_, k_, f, ...) are rebound all over these scripts and are not followed
    holders = set()
    hot = {L_ for L_, _ in calls} | {L_ for L_, _ in kidskeys}
    for s in ast.walk(tree):
        if isinstance(s, (ast.Assign, ast.AugAssign)):
            lo, hi = s.lineno, getattr(s, "end_lineno", s.lineno)
            if any(lo <= L_ <= hi for L_ in hot):
                for t in (s.targets if isinstance(s, ast.Assign) else [s.target]):
                    root = t
                    while isinstance(root, ast.Subscript):
                        root = root.value
                    if isinstance(root, ast.Name) and root.id not in ("OUT", "v_", "k_", "f", "f_", "v", "k", "m", "i", "x", "t_") and root.id not in TOK:
                        holders.add(root.id)
    last_fed = max((cl for (cl, cid) in chk if cid in fed), default=0)
    later = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name) and n.value.id in holders and n.lineno > last_fed and n.lineno not in recording:
            later.append((n.lineno, n.value.id, _key(n.slice)))
        elif isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id in holders and n.lineno > last_fed and n.lineno not in recording:
            later.append((n.lineno, n.value.id, "." + n.attr))
    later = sorted(set(later))
    execd = sorted({n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str) and n.value.endswith(".py")
                    and " " not in n.value})
    return dict(refs=refs, defs={k_: v_ for k_, v_ in defs.items() if k_ in TOK}, calls=calls, kidskeys=kidskeys, feeds=fed, holders=sorted(holders),
                later_uses=[(L_, h, k_, lines[L_ - 1].strip()[:140]) for L_, h, k_ in later], execd=execd,
                lines={L_: lines[L_ - 1].strip()[:150] for L_ in sorted({r_[0] for r_ in refs})})


TR = {}
for fn in HUBF:
    pth = os.path.join(HERE, fn)
    if not os.path.exists(pth):
        TR[fn] = None; P(f"    {fn}: not found"); continue
    t_ = trace(pth)
    TR[fn] = t_
    committed = git_head(rel(pth)) is not None
    P(f"    -- {fn} ({'committed' if committed else 'UNCOMMITTED, in flight: read only'}); exec'd / named sources: {t_['execd'] or 'none'}")
    if not t_["refs"]:
        P("       no code-level reference to any of the three projectors or the machinery that calls them")
    for (L_, tok, kind) in t_["refs"]:
        P(f"       line {L_:4d}  {tok:14s} ({kind:10s}{', own def' if tok in t_['defs'] else ''})  {t_['lines'][L_]}")
    if t_["refs"] and not t_["calls"]:
        P("       none of these is a CALL of a projector or of machinery that calls one (a same-named variable / key only)")
    if t_["calls"]:
        P(f"       calls {[f'{t}@{L_}' for L_, t in t_['calls']]}; 'kids'-keyed accesses {[f'{k}@{L_}' for L_, k in t_['kidskeys']]}; checks fed: "
          f"{t_['feeds']}")
        for (L_, h, k_, s_) in t_["later_uses"]:
            P(f"       later use of the container '{h}' (after the check fed) at line {L_}, key {k_!r}: {s_}")
# the XR29 exec path: FP11 is exec'd whole -- which of its names does XR29 read?
src29 = builtins.open(os.path.join(HERE, "XR29_mw_outer_curve.py")).read()
t29 = ast.parse(src29)
f11keys = sorted({n.slice.value for n in ast.walk(t29) if isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name) and n.value.id == "F11"
                  and isinstance(n.slice, ast.Constant)})
P(f"    XR29 exec's FP11_local_group_flyby.py whole (FP11 computes KiDS rows internally); XR29 reads from it only: {f11keys}")
OUT["numbers"]["D1"] = dict(trace={k_: v_ for k_, v_ in TR.items()}, XR29_reads_from_FP11=f11keys)
exp = {"XR18_frw_yield_crossing.py": ({"kids_class"}, ["K1"]), "XR18_state_separator.py": ({"gates"}, ["K1"]),
       "XR25_lambda_regulator.py": ({"kids_class"}, ["K1"])}
ok_p1 = all(TR[f_] and {c_[1] for c_ in TR[f_]["calls"]} == toks and [x for x in TR[f_]["feeds"] if not x.startswith("(")] == chk_
            for f_, (toks, chk_) in exp.items())
ok_none = all(TR[f_] is not None and not TR[f_]["calls"] for f_ in ("XR10_answer_validator.py", "XR29_mw_outer_curve.py", "XR25_common.py"))
xr28 = [f_ for f_ in HUBF if f_.startswith("XR28") and TR.get(f_)]
xr28_own = all({c_[1] for c_ in TR[f_]["calls"]} <= {"model_esd"} for f_ in xr28) and any("model_esd" in TR[f_]["defs"] for f_ in xr28)
ok_f11 = not (set(f11keys) & TOK)
check("D1 THE TRACE: XR18_frw and XR25 reach FP6's esd_of_M only through kids_class and XR18_state only through FP13's gates(), "
      "and every call and every 'kids'-keyed access feeds only the K1 control (the containers' later uses are printed with their "
      "keys); XR10, XR29 (and XR25_common) call nothing of the kind, and XR29 reads nothing projected from the FP11 it exec's; "
      "the XR28 files call only their own model_esd",
      "; ".join(f"{f_}: calls {sorted({c_[1] for c_ in TR[f_]['calls']})} -> {TR[f_]['feeds']}" for f_ in exp)
      + f" | no calls in XR10/XR29/XR25_common: {ok_none} (XR10's 'gates' is a local set of a row's gate names); XR29 reads from FP11 "
      f"{f11keys}; XR28 calls: {[sorted({c_[1] for c_ in TR[f_]['calls']}) for f_ in xr28]}",
      ok_p1 and ok_none and xr28_own and ok_f11)

# ================================================================================================= D2: FP20's committed re-score of those K1s
banner("D2  THE P1 CONSUMERS' K1 CONTROLS, PRICED BY FP20's COMMITTED RE-SCORE (FP9 H2, FP13 H1)")
FP20J = json.loads(git_head("real_research/derivation_chain_2026/FP20_esd_projection_fix_results.json"))
T20 = FP20J["numbers"]["R10_table"]


def fp20_row(lane, prefix, foot):
    r_ = [t for t in T20 if t["lane"] == lane and t["item"].startswith(prefix) and t["foot"] == foot]
    return (r_[0]["before"], r_[0]["after"]) if r_ else (float("nan"), float("nan"))


XRJ = {k_: json.loads(git_head(f"real_research/cross_thread_review_2026_09_26/{k_}_results.json")) for k_ in
       ("XR18_frw_yield_crossing", "XR18_state_separator", "XR25_lambda_regulator")}
D2 = []
k18 = XRJ["XR18_frw_yield_crossing"]["numbers"]["K1"]["kids"]
for f_ in FEET:
    b_, a_ = fp20_row("FP9", "H2 the (H_Y) HEADLINE at z = 0.25", f_)
    D2.append(("XR18_frw_yield_crossing", "K1", f"FP9 H2 KiDS (z = 0.25) {f_}", k18[f_], b_, a_))
out18 = git_head("real_research/cross_thread_review_2026_09_26/XR18_state_separator.out") or ""   # its JSON keeps only K1's deviation
ks = {}
for key, pat in (("kids", r"KiDS \{'canonical': ([-+\d.e]+), 'alt': ([-+\d.e]+)\}"), ("kids@0.4", r"KiDS@0\.4 \{'canonical': ([-+\d.e]+), 'alt': ([-+\d.e]+)\}")):
    pass
    m_ = re.search(pat, out18)
    if m_:
        ks[key] = {"canonical": float(m_.group(1)), "alt": float(m_.group(2))}
for z, key in ((0.25, "kids"), (0.4, "kids@0.4"), (0.7, "kids@0.7")):
    for f_ in FEET:
        b_, a_ = fp20_row("FP13", f"H1 the H_S HEADLINE: KiDS d chi^2 at z = {z}", f_)
        D2.append(("XR18_state_separator", "K1", f"FP13 H1 KiDS (z = {z}) {f_}", ks[key][f_] if key in ks else float("nan"), b_, a_))
k25 = XRJ["XR25_lambda_regulator"]["numbers"]
k25v = None
for cand in ("K1", "k1", "K1_rows"):
    if cand in k25:
        k25v = k25[cand]; break
for f_ in FEET:
    b_, a_ = fp20_row("FP13", "H1 the H_S HEADLINE: KiDS d chi^2 at z = 0.25", f_)
    cv = float("nan")
    if isinstance(k25v, dict):
        v_ = k25v.get(f"kids {f_}")
        cv = v_[0] if isinstance(v_, list) else (v_ if isinstance(v_, (int, float)) else float("nan"))
    D2.append(("XR25_lambda_regulator", "K1", f"FP13 H1 KiDS (z = 0.25) {f_}", cv, b_, a_))
for (ln, cid, item, cval, b_, a_) in D2:
    P(f"    {ln:24s} {cid}: {item:30s} committed in the lane {cval:+9.3f} | FP20 before {b_:+9.3f} -> after {a_:+9.3f}  (shift {a_ - b_:+7.3f})")
match = all((not math.isfinite(c)) or abs(c - b_) < 5e-3 for (_, _, _, c, b_, _) in D2)
nmatch = sum(1 for (_, _, _, c, b_, _) in D2 if math.isfinite(c) and abs(c - b_) < 5e-3)
OUT["numbers"]["D2"] = [dict(lane=a, check=b, item=c, committed=d, fp20_before=e, fp20_after=f) for a, b, c, d, e, f in D2]
check("D2 (reported) THE P1 CONSUMERS' K1 CONTROLS: each lane's committed K1 KiDS value is FP20's 'before', FP20's committed re-score "
      "moves it by the shift printed; each K1 would fail on a re-run (pinned to a defective-projection number); no other check of "
      "these lanes consumes KiDS (D1)", f"{nmatch} of {sum(1 for x in D2 if math.isfinite(x[3]))} committed values equal FP20's 'before'; "
      f"largest shift {max(abs(x[5] - x[4]) for x in D2):.2f}", match, load_bearing=False)

# ================================================================================================= X1: DE8's upper branch (SIGMA0_FOR_SIGMA1)
banner("X1  XR10's SIGMA0_FOR_SIGMA1 EVIDENCE: DE8's upper-branch sigma shift, committed vs corrected projection")
M_SCAN = 'banner("THE SCAN: branch x switch cell x carrier x 1/m x w x sigma x footing (amplitude 1, L352\'s criterion)")'
M_V1 = 'banner("V1  THE VERDICT PER BRANCH")'
SCAN = SRC8[SRC8.index(M_SCAN):SRC8.index(M_V1)]
assert 'BRANCHES = ["upper", "lower", "lower_abs"]' in SCAN
SCAN_UP = SCAN.replace('BRANCHES = ["upper", "lower", "lower_abs"]', 'BRANCHES = ["upper"]')
DE8J = json.loads(git_head(rel(P8).replace(".py", "_results.json")))
X1 = {}
for tag in ("committed", "corrected"):
    D8 = load_de8()
    base = patch_de8(D8, tag) if tag == "corrected" else dict(D8["BASE"])
    t1 = time.time()
    with lane_env():
        exec(compile("\n" * SRC8[:SRC8.index(M_SCAN)].count("\n") + SCAN_UP, P8, "exec"), D8)
    sc = D8["OUT"]["numbers"]["scan"]
    shift = {k_: v_ for k_, v_ in D8["OUT"]["numbers"]["sigma_shift_by_branch"].items()}
    passes = lambda row, sg: all(row[f"{sg}/{f_}"] <= 4.0 for f_ in FEET)
    cnt = {o: dict(pass_sigma0=sum(1 for k_, r_ in sc.items() if k_.startswith(o + "/") and passes(r_, 0.0)),
                   pass_sigma1=sum(1 for k_, r_ in sc.items() if k_.startswith(o + "/") and passes(r_, 1.0)),
                   cells=sum(1 for k_ in sc if k_.startswith(o + "/"))) for o in ("r200", "nfw")}
    X1[tag] = dict(base=base, scan=jnorm(sc), shift=shift, counts=cnt, secs=time.time() - t1)
    P(f"    {tag:9s} projection: L352 base {base['canonical']:.3f}/{base['alt']:.3f}; sigma shift r200/upper {shift['r200/upper']:.5f}, "
      f"nfw/upper {shift['nfw/upper']:.5f}; cells passing (sigma = 0 / 1): r200 {cnt['r200']['pass_sigma0']}/{cnt['r200']['pass_sigma1']} of "
      f"{cnt['r200']['cells']}, nfw {cnt['nfw']['pass_sigma0']}/{cnt['nfw']['pass_sigma1']} of {cnt['nfw']['cells']}   [{time.time() - t1:.0f} s]")
cs, cc_ = DE8J["numbers"]["scan"], X1["committed"]["scan"]
dK1 = max(abs(cc_[k_][s_] - cs[k_][s_]) for k_ in cc_ for s_ in cc_[k_])
dsh = max(abs(X1["committed"]["shift"][k_] - DE8J["numbers"]["sigma_shift_by_branch"][k_]) for k_ in ("r200/upper", "nfw/upper"))
check("K1 CONTROL: with the committed projector DE8's upper-branch scan (2 outer conventions x 36 cells x 2 sigma x 2 footings) and "
      "its two sigma shifts are reproduced exactly", f"{sum(len(v_) for v_ in cc_.values())} numbers, max |d| {dK1:.1e}; shifts max |d| {dsh:.1e}",
      dK1 <= 1e-9 and dsh <= 1e-9 and len(cc_) == 72)
sh_a = X1["corrected"]["shift"]
worst_cell = max(((k_, abs(r_[f"1.0/{f_}"] - r_[f"0.0/{f_}"])) for k_, r_ in X1["corrected"]["scan"].items() for f_ in FEET), key=lambda t_: t_[1])
P(f"    the largest corrected-projection sigma shift sits at {worst_cell[0]} ({worst_cell[1]:.5f})")
hx1 = all(sh_a[k_] <= 0.4 for k_ in ("r200/upper", "nfw/upper"))
OUT["numbers"]["X1"] = dict(committed_shift={k_: X1["committed"]["shift"][k_] for k_ in ("r200/upper", "nfw/upper")},
                            corrected_shift={k_: sh_a[k_] for k_ in ("r200/upper", "nfw/upper")}, counts={t_: X1[t_]["counts"] for t_ in X1},
                            worst_cell=worst_cell, corrected_scan=X1["corrected"]["scan"])
check("X1 (reported; = HX1, pre-declared) XR10's SIGMA0_FOR_SIGMA1 evidence under the corrected projection: DE8's upper-branch sigma "
      "shift <= 0.4 on both outer conventions (XR10's json_le evidence)",
      f"r200/upper {X1['committed']['shift']['r200/upper']:.5f} -> {sh_a['r200/upper']:.5f}; nfw/upper {X1['committed']['shift']['nfw/upper']:.5f} "
      f"-> {sh_a['nfw/upper']:.5f}", hx1, load_bearing=False,
      reading=("the evidence would still hold when DE8 is re-run with the corrected projection" if hx1 else
               "when DE8 is re-committed with the corrected projection, XR10's check E fails (rc = 1) on this rule until its evidence "
               "or its bar is revisited"))

# ================================================================================================= X2: DE9's cap (HARDW_FOR_SMOOTH)
banner("X2  XR10's HARDW_FOR_SMOOTH EVIDENCE: DE9's MOND-sector switch-only KiDS cap and its p = 1 window")
SRC9 = builtins.open(P9).read()
M9 = 'banner("C1 C2  CONTROLS: the near-hard smooth gate reproduces DE2\'s hard caps")'
DE9J = json.loads(git_head(rel(P9).replace(".py", "_results.json")))
X2 = {}
for tag in ("committed", "corrected"):
    n9 = {"__name__": "de9", "__file__": P9, "open": _ro_open}
    t1 = time.time()
    with lane_env():
        exec(compile(SRC9[:SRC9.index(M9)].replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), P9, "exec"), n9)
    if tag == "corrected":
        n9["BASE"] = patch_de8(n9["D8"], tag)
    with lane_env():
        caps = {w: n9["cap_kids"](w, 100 * n9["KPC_"], 1.0, "mond") for w in (0.1, 0.25)}
    X2[tag] = dict(caps=caps, base=dict(n9["BASE"]), secs=time.time() - t1)
    P(f"    {tag:9s} projection: MOND-sector switch-only KiDS cap x_c,eff(0.25) at w = 0.1: {caps[0.1]}, w = 0.25: {caps[0.25]}   "
      f"[{time.time() - t1:.0f} s]")
kc9 = DE9J["numbers"]["KiDS_cap"]["mond"]
dK2 = max(abs(X2["committed"]["caps"][w] - kc9[str(w)]) for w in (0.1, 0.25))
check("K2 CONTROL: with the committed projector DE9's MOND-sector switch-only KiDS caps at w = 0.1 and 0.25 are reproduced exactly",
      f"{X2['committed']['caps']} vs DE9 {kc9['0.1']}/{kc9['0.25']} (max |d| {dK2:.1e})", dK2 <= 1e-9)
E2G = lambda z: 0.3138 * (1 + z) ** 3 + 0.6862
FC9 = DE9J["numbers"]["flagship_cap"]["mond"]
WIN = {}
for tag in X2:
    WIN[tag] = {}
    for w in (0.1, 0.25):
        hi = min(X2[tag]["caps"][w] / E2G(0.25), min(FC9[str(w)].values()) / E2G(2.5))
        lo = 1.5 / (1 - w)
        WIN[tag][w] = (round(lo, 3), round(hi, 3)) if hi >= lo else None
won = DE9J["numbers"]["window"]["mond/1.0"]
P(f"    DE9's committed window (mond, p = 1): w = 0.1 {won['0.1']}, w = 0.25 {won['0.25']}; recomputed committed {WIN['committed']}; "
  f"corrected {WIN['corrected']}")
hx2 = all(WIN["corrected"][w] is not None and WIN["corrected"][w][0] <= 2.5 <= WIN["corrected"][w][1] for w in (0.1, 0.25))
OUT["numbers"]["X2"] = dict(caps={t_: {str(w): v_ for w, v_ in X2[t_]["caps"].items()} for t_ in X2}, window={t_: {str(w): v_ for w, v_ in WIN[t_].items()} for t_ in WIN},
                            flagship_cap_used=FC9)
check("X2 (reported; = HX2, pre-declared) XR10's HARDW_FOR_SMOOTH evidence under the corrected projection: DE9's MOND-sector window "
      "at p = 1 still contains x_c0 = 2.5 at w = 0.1 and 0.25",
      f"caps w = 0.1: {kc9['0.1']:.4f} -> {X2['corrected']['caps'][0.1]}; w = 0.25: {kc9['0.25']:.4f} -> {X2['corrected']['caps'][0.25]}; windows "
      f"{WIN['committed']} -> {WIN['corrected']}", hx2, load_bearing=False)
if MUTATE:
    same = (all(abs(X1["corrected"]["shift"][k_] - X1["committed"]["shift"][k_]) < 1e-12 for k_ in ("r200/upper", "nfw/upper"))
            and all(X2["corrected"]["caps"][w] == X2["committed"]["caps"][w] for w in (0.1, 0.25)))
    check("K-MUT (MUTATE control) with the committed projector in the corrected slot X1's and X2's 'after' equal their 'before'",
          f"identical: {same}", same)

# ================================================================================================= X3: XR10's KiDS rows
banner("X3  XR10's KiDS ROWS: the projector each row scores with, and before -> after where re-scored")
X10 = json.loads(git_head("real_research/cross_thread_review_2026_09_26/XR10_answer_rows.json"))
RSC = os.path.join(HERE, f"XR35_kids_rescore_results{'_MUTATE' if MUTATE else ''}.json")
R1J = json.load(builtins.open(RSC)) if os.path.exists(RSC) else None
res1 = (R1J or {}).get("numbers", {}).get("results", {})
rows1 = (R1J or {}).get("numbers", {}).get("R_rows", [])
l390 = [r_ for r_ in rows1 if r_["lane"] == "DE10" and r_["cell"].startswith("C1: L390")]
at3 = FP20J["numbers"].get("R11_AT3", {})
X3 = []
for r_ in X10["rows"]:
    if not any("kids" in g_ for g_ in r_.get("gates", [])):
        continue
    scr = os.path.join(REPO, r_["script"])
    fam = []
    if os.path.exists(scr):
        t_ = trace(scr)
        toks = {x[1] for x in t_["refs"]}
        if toks & P1_TOK: fam.append("P1 (esd_of_M via kids_* / gates)")
        if toks & P2_TOK: fam.append("P2 (project_M2 / esd_from_mlens via L352 / DE8)")
    rid = r_["id"]
    if rid == "DE10.kids" and "DE10" in res1:
        ba = f"worst {res1['DE10']['worst_before']:+.2f} -> {res1['DE10']['worst_after']:+.2f} (still passes; XR35_kids_rescore R1)"
    elif rid == "XR9.kids" and "XR9" in res1:
        ba = f"passing cells {res1['XR9']['passing_before']} -> {res1['XR9']['passing_after']} (XR35_kids_rescore R2)"
    elif rid == "XR14.kids" and "XR14" in res1:
        ba = (f"M* worst {res1['XR14']['worst_before']['MSPH']:+.2f} -> {res1['XR14']['worst_after']['MSPH']:+.2f}, L388 "
              f"{res1['XR14']['worst_before']['L388']:+.2f} -> {res1['XR14']['worst_after']['L388']:+.2f} (still passes; XR35_kids_rescore R3)")
    elif rid == "L390.kids" and l390:
        ba = "; ".join(f"{x['cell'][-9:]}: {x['before']['canonical']:+.2f}/{x['before']['alt']:+.2f} -> {x['after']['canonical']:+.2f}/"
                       f"{x['after']['alt']:+.2f}" for x in l390) + " (its R1 at 600/650 km/s = DE10's C1, re-scored in XR35_kids_rescore; bar +4)"
    elif rid == "DE8.kids":
        ba = (f"upper branch (X1): sigma shift r200 {X1['committed']['shift']['r200/upper']:.4f} -> {sh_a['r200/upper']:.4f}, nfw "
              f"{X1['committed']['shift']['nfw/upper']:.4f} -> {sh_a['nfw/upper']:.4f}; passing cells r200 {X1['committed']['counts']['r200']['pass_sigma1']} -> "
              f"{X1['corrected']['counts']['r200']['pass_sigma1']} of 36, nfw {X1['committed']['counts']['nfw']['pass_sigma1']} -> "
              f"{X1['corrected']['counts']['nfw']['pass_sigma1']} of 36 (sigma = 1); lower branches not re-scored")
    elif rid == "DE9.msc":
        ba = f"MOND-sector caps (X2) w = 0.1 {kc9['0.1']:.4f} -> {X2['corrected']['caps'][0.1]}, w = 0.25 {kc9['0.25']:.4f} -> {X2['corrected']['caps'][0.25]}"
    elif rid == "AT3.gates":
        ba = f"FP20 R11: window cells keep their KiDS pass {at3.get('window', ['?', '?'])[1] if at3 else '?'}; gate moves {at3.get('shift_range')}"
    else:
        ba = "on the defective projector; NOT re-scored (here, in XR35_kids_rescore or in FP20); a comparison row"
    X3.append(dict(id=rid, claim=r_["claim"], projector=fam, before_after=ba))
    P(f"    {rid:16s} [{r_['claim']:10s}] {', '.join(fam) or 'no projector reference'}\n{'':22s}{ba}")
OUT["numbers"]["X3"] = X3
check("X3 (reported) XR10's KiDS rows mapped: every row that scores KiDS uses a defective projector; the rows re-scored here, in "
      "XR35_kids_rescore and in FP20 are listed before -> after; XR10's own verdicts are axis classifications from the code and "
      "consume no projected number", f"{len(X3)} rows; re-scored {sum(1 for x in X3 if 'NOT re-scored' not in x['before_after'])}; "
      f"not re-scored {[x['id'] for x in X3 if 'NOT re-scored' in x['before_after']]}", R1J is not None, load_bearing=False)

# ================================================================================================= XR28 (listed, not run)
banner("XR28 (IN FLIGHT IN ANOTHER LANE: LISTED FROM ITS SOURCES, NOT RUN)")
src28 = builtins.open(os.path.join(HERE, "XR28_common.py")).read()
own_kernel = "def shell_esd_kernel(R, e):" in src28 and "Mcyl = 1.0 - (4 * np.pi / 3) * rho" in src28
P(f"    XR28_common's model_esd projects its stacked profiles with its own uniform-shell kernel (shell_esd_kernel: the exact "
  f"uniform-shell Sigma and cylinder mass, the same closed form as FP20's shell_mats): {own_kernel}; XR28_controls K5 checks it "
  f"against Wright & Brainerd; FP6 is exec'd there only for phantom() (K4).  It does not use esd_of_M, project_M2 or "
  f"esd_from_mlens; FP20's H flagged it on the name model_esd (DE8 has a function of that name) and on esd_of_M in K5's docstring.")
check("XR28 (reported) the in-flight lane uses none of the three defective projectors (its own exact uniform-shell kernel)",
      f"own kernel present: {own_kernel}; code references {[sorted({r_[1] for r_ in TR[f_]['refs']}) for f_ in xr28]}", own_kernel and xr28_own,
      load_bearing=False)

# ================================================================================================= F, verdict
allnum = [v_ for t_ in X1 for r_ in X1[t_]["scan"].values() for v_ in r_.values()] + [v_ for t_ in X2 for v_ in X2[t_]["caps"].values() if v_ is not None]
check("F EVERY RE-SCORE COMPLETED: DE8's upper branch and DE9's caps in both projections, every number finite",
      f"{len(allnum)} numbers; non-finite {sum(1 for x in allnum if not math.isfinite(x))}; DE9 caps found: "
      f"{all(v_ is not None for t_ in X2 for v_ in X2[t_]['caps'].values())}",
      all(math.isfinite(x) for x in allnum) and all(v_ is not None for t_ in X2 for v_ in X2[t_]["caps"].values()))
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
banner("VERDICT")
P(f"""  XR18_frw / XR18_state / XR25: the projected KiDS number feeds only each lane's K1 control (FP9 H2, FP13 H1), which FP20's
  committed re-score moves by up to {max(abs(x[5] - x[4]) for x in D2):.2f}; each K1 would fail on a re-run (pinned to a defective number); no
  physics check of those lanes moves.  XR29: no dependency.  XR28: its own exact kernel (listed, not run).
  XR10: its verdicts consume no projected number, but two enabled rules rest on KiDS evidence computed with the defective P2:
    SIGMA0_FOR_SIGMA1 (DE8 upper sigma shift <= 0.4): r200 {X1['committed']['shift']['r200/upper']:.5f} -> {sh_a['r200/upper']:.5f}, nfw
    {X1['committed']['shift']['nfw/upper']:.5f} -> {sh_a['nfw/upper']:.5f} -- {'holds' if hx1 else 'FAILS: XR10 check E would go rc = 1 once DE8 is re-committed'};
    HARDW_FOR_SMOOTH (DE9 window contains x_c0 = 2.5): caps {kc9['0.1']:.3f}/{kc9['0.25']:.3f} -> {X2['corrected']['caps'][0.1]:.3f}/
    {X2['corrected']['caps'][0.25]:.3f}, windows {WIN['corrected']} -- {'holds' if hx2 else 'FAILS'}.
  kappa = 1/2 is FITTED (Z = 5.7888).  Not closed.""")
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), n_fail, round(time.time() - T0)
fn = os.path.join(HERE, f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json")
with builtins.open(fn, "w") as fh:
    json.dump(jnorm(OUT), fh, indent=1)
rc = 0 if n_fail == 0 else 1
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {os.path.basename(fn)}   {el()}")
P(f"rc={rc}")
sys.stdout.flush(); _OUTFH.close(); sys.stdout = sys.__stdout__
sys.exit(rc)
