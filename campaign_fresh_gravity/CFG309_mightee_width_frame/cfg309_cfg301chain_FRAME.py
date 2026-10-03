#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG309 consequence (FROZEN_CRITERIA.md section 8, ec54de4ac): CFG301's committed width chain re-run with the catalogue W50 read as REST-frame
(k = 0: W50 not divided by 1 + z) -- a labelled variant; CFG301's files are not edited.  kappa = 1/2 is FITTED.

The committed source campaign_fresh_gravity/CFG301_mightee_hi_catalogue_width_chain/cfg301_width_chain.py (git blob d11f89e0..., asserted) is exec'd with
STAGE=B, MUTATE=0, DRYRUN=0 and __file__ set to CFG301's script (so it reads CFG301's committed stage-A / SELFTEST / CC2 JSONs), with textual
substitutions, each asserted to match exactly once:
  (s1) "REC0 = dict(delta=0.0, k=1,"  ->  "REC0 = dict(delta=0.0, k=0,"          (FRAME run only)
  (s2) the two output paths -> this folder, cfg309_cfg301chain_stageB_{FRAME|IDENTITY}.out / _results.json
Runs: IDENTITY (s2 only, k = 1; control C-ID) and FRAME (s1 + s2).  Then C-CONS (FRAME pooled a0 vs CFG306 P1's 1.3111e-10, <= 0.001 dex) and the summary
on both footings (canonical 9.3603e-11, alt 1.1312e-10; kappa = 1/2 * a0 / a0_footing).
Writes cfg309_cfg301chain_FRAME_summary.out and _summary.json.
"""
import os, sys, json, math, ast, hashlib, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
SRC = os.path.join(CFG, "CFG301_mightee_hi_catalogue_width_chain", "cfg301_width_chain.py")
COMMITTED = os.path.join(CFG, "CFG301_mightee_hi_catalogue_width_chain", "cfg301_stageB_results.json")
CFG306 = os.path.join(CFG, "CFG306_paper40_referee", "cfg306_physics_checks_results.json")
BLOB = "d11f89e0d853a68cf9a2f1434a6a20edab575176"
LOG, CHK = [], []


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def check(name, detail, ok):
    CHK.append((name, bool(ok))); P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         {detail}")


raw = open(SRC, "rb").read()
blob = hashlib.sha1(b"blob %d\0" % len(raw) + raw).hexdigest()
src = raw.decode()
P(__doc__.strip())
check("K0 CFG301's source is the committed blob", f"git blob {blob}", blob == BLOB)
doc = ast.get_docstring(ast.parse(src), clean=False)
S1 = ("REC0 = dict(delta=0.0, k=1,", "REC0 = dict(delta=0.0, k=0,")
S2 = [('os.path.join(HERE, f"cfg301{SFX}.out")', 'os.path.join(_CFG309_OUT, f"cfg309_cfg301chain{SFX}{_CFG309_TAG}.out")'),
      ('os.path.join(HERE, f"cfg301{SFX}_results.json")', 'os.path.join(_CFG309_OUT, f"cfg309_cfg301chain{SFX}{_CFG309_TAG}_results.json")')]


def run(tag, frame):
    s = src
    subs = ([S1] if frame else []) + S2
    for a, b in subs:
        n = s.count(a); assert n == 1, (a, n); s = s.replace(a, b)
    os.environ.update(STAGE="B", MUTATE="0", DRYRUN="0")
    g = {"__name__": "__cfg301_exec__", "__file__": SRC, "__doc__": doc, "_CFG309_OUT": HERE, "_CFG309_TAG": tag}
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            exec(compile(s, SRC + f" [CFG309 {tag}]", "exec"), g)
        except SystemExit as ex:                                             # CFG301 ends with sys.exit(status)
            g["_exit"] = ex.code
    tail = [l for l in buf.getvalue().splitlines() if "checks pass" in l]
    P(f"  run {tag}: substitutions {len(subs)}; CFG301's own last line: {tail[-1].strip() if tail else '?'}")
    return json.load(open(os.path.join(HERE, f"cfg309_cfg301chain_stageB{tag}_results.json")))


JI = run("_IDENTITY", frame=False)
JF = run("_FRAME", frame=True)
JC = json.load(open(COMMITTED))
ri, rc = JI["numbers"]["results"], JC["numbers"]["results"]
dmax = max(abs(ri[k]["log_s"] - rc[k]["log_s"]) for k in ("pooled", "W1", "W2", "W3"))
check("C-ID the k = 1 harness reproduces CFG301's committed pooled and window log s* to <= 1e-12", f"max |diff| {dmax:.2e}", dmax <= 1e-12)
A0C, A0A = 9.3603e-11, 1.1312e-10
rf = JF["numbers"]["results"]["pooled"]
a0f = rf["a0"]
p306 = json.load(open(CFG306))["numbers"]["P1_frame"]["k0"]["a0"]
dcons = math.log10(a0f / p306)
check("C-CONS the k = 0 pooled a0 agrees with CFG306 P1's k = 0 value to <= 0.001 dex", f"{a0f:.5e} vs {p306:.5e} ({dcons:+.2e} dex)", abs(dcons) <= 0.001)


def summ(J, label):
    N = J["numbers"]; r = N["results"]; po = r["pooled"]; a0 = po["a0"]; s = po["s"]; A0 = a0 / s
    q = [A0 * 10 ** v for v in po["q"]]
    cal = N["calibration"]
    out = dict(label=label, a0=a0, s=s, q_a0=q, recipe_half=po["recipe_half"], dex_canonical=math.log10(a0 / A0C), dex_alt=math.log10(a0 / A0A),
               kappa_canonical=0.5 * a0 / A0C, kappa_alt=0.5 * a0 / A0A, windows_a0={w: r[w]["a0"] for w in ("W1", "W2", "W3")},
               drift_W3_W1=cal.get("drift"), cc1=cal.get("cc1"), cc3=cal.get("cc3"), calibrated=cal.get("calibrated"), offset_sparc=cal.get("offset_sparc"),
               btfr_all=N["btfr"]["(i) all survivors"]["median"], btfr_all_dex=[N["btfr"]["(i) all survivors"]["dex_canonical"], N["btfr"]["(i) all survivors"]["dex_alt"]],
               checks=f"{sum(c['ok'] for c in J['checks'])}/{len(J['checks'])}")
    P(f"  {label}: pooled a0 {a0:.4e} m/s^2 (s* {s:.4f}); 68% {q[1]:.3e}-{q[2]:.3e}, 95% {q[0]:.3e}-{q[3]:.3e}; recipe half-width {po['recipe_half']:.3f} dex; "
      f"vs canonical 9.3603e-11 {out['dex_canonical']:+.3f} dex, vs alt 1.1312e-10 {out['dex_alt']:+.3f} dex; kappa {out['kappa_canonical']:.3f} (canonical footing) / "
      f"{out['kappa_alt']:.3f} (alt footing); windows W1/W2/W3 {', '.join(f'{v:.3e}' for v in out['windows_a0'].values())} (W3-W1 {out['drift_W3_W1']:+.3f} dex); "
      f"CC1 {out['cc1']}, CC3 {out['cc3']}, calibrated {out['calibrated']} (W1 vs SPARC {out['offset_sparc']:+.3f} dex); A1 BTFR (i) {out['btfr_all']:.3e}; CFG301 checks {out['checks']}")
    return out


P("\nSummary (kappa = 1/2 is FITTED; both footings):")
SI = summ(JI, "k = 1 (CFG301 committed frame: W50/(1+z))")
SF = summ(JF, "k = 0 (W50 read as rest-frame) -- the _FRAME variant")
npass = sum(ok for _, ok in CHK)
P(f"\n{npass}/{len(CHK)} checks pass")
open(os.path.join(HERE, "cfg309_cfg301chain_FRAME_summary.out"), "w").write("\n".join(LOG).replace(REPO, "<repo>") + "\n")
json.dump(dict(lane="CFG309", frozen="ec54de4ac", checks=[dict(name=n, ok=o) for n, o in CHK], identity=SI, frame=SF, cfg306_k0=p306, cons_dex=dcons, id_max_diff=dmax),
          open(os.path.join(HERE, "cfg309_cfg301chain_FRAME_summary.json"), "w"), indent=1)
