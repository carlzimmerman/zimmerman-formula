#!/usr/bin/env python3
"""CFG658 S0 + G-D2 (FROZEN_CRITERIA.md, 12c5ab6b3).
S0  raw SPARC control: CFG695's S2 fit code (sliced read-only) with nu_s and nu_mono.
D2  CONTEXT ONLY (no verdict): CFG556's halo model executed read-only with its kernel swapped (nu_s; nu_mono as a second reference;
    the recorded exponential kernel as the MUTATE reproduction).  The halo model's mass function, bias and NFW comparator are
    LCDM-built, so nothing here is a verdict.  Its two file writes are redirected to this lane (no CFG556 file is touched).
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg658_d2_sparc.py   -> cfg658_d2_sparc.out, cfg658_d2_sparc_results.json
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, io, json, math, time, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
T0 = time.time(); OUT, RES, CHK = [], {"lane": "CFG658", "gate": "S0+D2", "criteria": "12c5ab6b3"}, {}
try:
    os.nice(10)
except OSError:
    pass


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(name, ok, msg):
    CHK[name] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}"); return bool(ok)


def nu_s(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


sys.path.insert(0, LANES)
import CFG4_common as C4                                                       # noqa: E402
P(__doc__.split("Run:")[0].strip())

# ============================================================================ S0 SPARC
P("\n== S0  raw SPARC (CFG695 S2 code, sliced read-only) ==")
P695 = os.path.join(LANES, "CFG695_saturating_vacuum", "cfg695.py"); s695 = open(P695).read()
N5 = dict(C4=C4, np=np, math=math)
exec(compile(s695[s695.index("GAL = C4.load_sparc()"):s695.index("NU_SIMPLE =")], P695, "exec"), N5)
S0 = {}
for f in C4.FOOTS:
    rs, us = N5["fit"](nu_s, C4.A0[f]); rm, um = N5["fit"](C4.nu_mono, C4.A0[f])
    S0[f] = dict(rms_s=rs, U_s=us, rms_mono=rm, U_mono=um)
    P(f"  {f:9s}: nu_s {rs:.4f} dex @ Upsilon {us:.2f};  nu_mono {rm:.4f} @ {um:.2f}")
J695 = json.load(open(os.path.join(LANES, "CFG695_saturating_vacuum", "cfg695_results.json")))["numbers"]["S2"]
check("S0 control: nu_s reproduces CFG695 S2 (rms 1e-4, identical Upsilon) on both footings",
      all(abs(S0[f]["rms_s"] - J695[f]["rms"]) <= 1e-4 and S0[f]["U_s"] == J695[f]["U"] for f in C4.FOOTS),
      "; ".join(f"{f} {S0[f]['rms_s']:.4f}@{S0[f]['U_s']:.2f} vs {J695[f]['rms']:.4f}@{J695[f]['U']:.2f}" for f in C4.FOOTS))
check("M-K SPARC: nu_mono reproduces 0.1003 / 0.0991 (CFG4 H2 via CFG695 controls, 1e-4)",
      all(abs(S0[f]["rms_mono"] - J695[f]["rms_mono"]) <= 1e-4 for f in C4.FOOTS),
      "; ".join(f"{f} {S0[f]['rms_mono']:.4f}" for f in C4.FOOTS))
RES["S0"] = S0

# ============================================================================ D2 CONTEXT
P("\n== D2  CFG556 halo model with the kernel swapped (CONTEXT ONLY: LCDM-built mass function / bias / comparator) ==")
P556 = os.path.join(LANES, "CFG556_halo_model_matter_power", "cfg556_halo_model.py"); s556 = open(P556).read()
k_old = s556[s556.index("def nu_k(y):"):s556.index("# ------------------------------------------------------------------ sigma(M)")]
w1 = 'json.dump(res, open(os.path.join(HERE, f"cfg556_results{SUF}.json"), "w"), indent=1, default=float)'
w2 = 'open(os.path.join(HERE, f"cfg556_halo_model{SUF}.out"), "w").write("\\n".join(OUT) + "\\n")'
assert s556.count(w1) == 1 and s556.count(w2) == 1 and s556.count(k_old) == 1
src = s556.replace(k_old, "nu_k = KERNEL_\n\n").replace(w1, "HOLD_.append(res)").replace(w2, "HOLD_.append(OUT)")
J556 = json.load(open(os.path.join(LANES, "CFG556_halo_model_matter_power", "cfg556_results.json")))


def nu_exp(y):                                                                   # CFG556's recorded kernel, verbatim
    y = np.maximum(y, 1e-300); s = np.sqrt(y)
    return np.where(s > 50, 1.0, 1.0 / -np.expm1(-np.minimum(s, 50)))


D2 = {}
os.environ.pop("CFG556_MUTATE", None)
for kn, kf in (("exp_recorded", nu_exp), ("nu_mono", C4.nu_mono), ("nu_s", nu_s)):
    hold = []
    ns = {"__file__": P556, "__name__": "cfg556_ro", "KERNEL_": kf, "HOLD_": hold}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src, P556, "exec"), ns)
    res = hold[0]
    for foot in ("canonical", "alt"):
        c = res["cases"][f"{foot}|census|cen"]
        D2[f"{kn}|{foot}"] = dict(E=c["E"], kE=c["kE"], D=c["D"], s8_ratio=c["s8_ratio"], R_at=c["R_at"], verdict=res["verdict"][foot]["verdict"],
                                  re_over_rta_at=c.get("re_over_rta_at"), emg_E=res["cases"][f"{foot}|census|emg"]["E"],
                                  r200scope_D=res["cases"][f"{foot}|census|cen|r200scope"]["D"])
        P(f"  {kn:12s} {foot:9s}: E {c['E']:+.3f} (k {c['kE']:.2f});  R(k) " + ", ".join(f"{k}: {float(v):.3f}" for k, v in c["R_at"].items())
          + f";  sigma8 ratio {c['s8_ratio']:.4f};  emergent-edge E {D2[f'{kn}|{foot}']['emg_E']:+.3f};  CFG556 class {res['verdict'][foot]['verdict']}")
    P(f"     ({kn}: done {time.time() - T0:.0f} s)")
dE = max(abs(D2[f"exp_recorded|{f}"]["E"] - J556["cases"][f"{f}|census|cen"]["E"]) for f in ("canonical", "alt"))
check("M-K CFG556: the recorded kernel reproduces E +0.715 / +0.883 (1e-3)", dE < 1e-3, f"max |dE| {dE:.1e}")
for foot in ("canonical", "alt"):
    P(f"  dE (nu_s - recorded) {foot}: {D2[f'nu_s|{foot}']['E'] - D2[f'exp_recorded|{foot}']['E']:+.3f};  (nu_s - nu_mono): "
      f"{D2[f'nu_s|{foot}']['E'] - D2[f'nu_mono|{foot}']['E']:+.3f}")
RES["D2"] = D2
RES["checks"] = CHK; RES["elapsed_s"] = time.time() - T0
json.dump(RES, open(os.path.join(HERE, "cfg658_d2_sparc_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg658_d2_sparc.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(v["ok"] for v in CHK.values()) else 1)
