#!/usr/bin/env python3
"""SG1_sluggs_imf_gas: SLUGGS centrals under the frozen CL2 picture with the measured hot gas (truncated at the measured edge; extrapolated variant).
Frozen criteria e93b338fa2 (committed alone). Machinery: HO2's committed script (a3bb1e781f) executed read-only up to its SLUGGS child,
with one source edit inside that child adding the 'trunc' reading and K1 (no rule change to HO2's readings).

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, not a particle; not theory closed;
nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I sg1_sluggs_imf_gas.py      (SG1_MUTATE=1 twin)
"""
import os, sys, json, hashlib, resource
MUTS = os.environ.get("SG1_MUTATE", "0") == "1"; TAGS = "_MUTATE" if MUTS else ""
HERE_S = os.path.dirname(os.path.abspath(__file__)); REB_S = os.path.dirname(HERE_S); REPO_S = os.path.dirname(REB_S)
HO2 = os.path.join(REB_S, "HO2_sluggs_milkyway_heldout", "ho2_heldout.py")
src = open(HO2).read()
src = src[:src.index('C1 = call("child_sluggs")')]
old = '        bar = sluggs_cl2(f, gas="extrap"); law = sluggs_cl2(f, force="law")'
assert src.count(old) == 1
new = ('        bar = sluggs_cl2(f, gas="extrap"); law = sluggs_cl2(f, force="law")\n'
       '        _gp0 = gas_profile\n'
       '        if SG1_MUT: gas_profile = (lambda n_, m_, x=1.0: None if m_ is None else _gp0(n_, m_, 0.0 if m_ == "trunc" else x))\n'
       '        trn = sluggs_cl2(f, gas="trunc")\n'
       '        gas_profile = _gp0\n'
       '        import numpy as _np\n'
       '        _k1 = all(bool(_np.all(_np.abs(_gp0(n_, "trunc")[_gp0.__globals__["RG"] <= _gp0.__globals__["GAS"][n_][1]["r_meas"]] - _gp0(n_, "extrap")[_gp0.__globals__["RG"] <= _gp0.__globals__["GAS"][n_][1]["r_meas"]]) <= 1e-12 * _np.abs(_gp0(n_, "extrap")[_gp0.__globals__["RG"] <= _gp0.__globals__["GAS"][n_][1]["r_meas"]]).max())) for n_ in CEN)\n'
       '        SG1_K1[f] = _k1 and not SG1_MUT\n')
src = src.replace(old, new)
src = src.replace('out["sluggs"][f] = dict(cls=c, cl2=pk(st), x38_q0=pk(s0), rep_bar=pk(bar), rep_law_all=pk(law),',
                  'out["sluggs"][f] = dict(cls=c, cl2=pk(st), x38_q0=pk(s0), rep_bar=pk(bar), rep_law_all=pk(law), sg1_trunc=pk(trn), sg1_cls_trunc=cls(trn, s0), sg1_cls_extrap=cls(bar, s0), sg1_k1=SG1_K1[f],')
os.environ.pop("HO2_MUTATE", None)
import types
_mod = types.ModuleType("ho2_ro"); sys.modules["ho2_ro"] = _mod                    # the forked pool pickles _child by module name
NS2 = _mod.__dict__; NS2.update({"__file__": os.path.join(HERE_S, "ho2_ro.py"), "SG1_MUT": MUTS, "SG1_K1": {}})
exec(compile(src, HO2, "exec"), NS2)
P = NS2["P"]
C1 = NS2["call"]("child_sluggs")
P(f"\n================ SG1_sluggs_imf_gas (criteria e93b338fa2){'  [MUTATE: trunc gas x0 on the graded path]' if MUTS else ''}")
checks = {}; RES = dict(criteria="e93b338fa2", machinery="HO2 a3bb1e781f (read-only, one child edit)", mutate=MUTS, footings={})
HJ = json.load(open(os.path.join(REB_S, "HO2_sluggs_milkyway_heldout", "ho2_heldout_results.json")))
for f in NS2["FEET"]:
    s = C1["sluggs"][f]
    ref = HJ["footings"][f]["sluggs"] if "footings" in HJ and f in HJ["footings"] and "sluggs" in HJ["footings"][f] else None
    k0 = abs(s["cl2"]["mean"] - 0.152) < 0.0015 and abs(s["rep_bar"]["mean"] - (-0.002)) < 0.0015
    checks[f"K0_{f}"] = bool(k0); checks[f"K1_{f}"] = bool(s["sg1_k1"])
    ms = {k: (v.get("Mstar_over_Mjam") if isinstance(v, dict) else None) for k, v in (s["cl2"]["info"] or {}).items()}
    pr = s["sg1_cls_trunc"]
    v = "MEASURED GAS RESOLVES SLUGGS" if pr == "PASS" else ("ONLY EXTRAPOLATED GAS RESOLVES SLUGGS" if s["sg1_cls_extrap"] == "PASS" else "GAS DOES NOT RESOLVE SLUGGS")
    P(f"\n=== [{f}] CL2 (no gas) mean {s['cl2']['mean']:+.3f}, cleared {s['cl2']['n_cleared']}/4 | extrap {s['rep_bar']['mean']:+.3f} ({s['rep_bar']['n_cleared']}/4, {s['sg1_cls_extrap']}) | "
      f"TRUNC (measured gas only) {s['sg1_trunc']['mean']:+.3f} ({s['sg1_trunc']['n_cleared']}/4, {pr})")
    P(f"  per galaxy trunc: " + "; ".join(f"{k} {v_:+.3f}" if v_ is not None else f"{k} n/c" for k, v_ in s["sg1_trunc"]["per"].items()))
    P(f"  IMF bound: M*/M_JAM (JAM analogue, already the dynamical maximum) = " + ", ".join(f"{k} {v_:.2f}" for k, v_ in ms.items() if v_ is not None))
    P(f"  K0 (HO2 CL2 +0.152 and extrap -0.002 reproduced): {'PASS' if k0 else 'FAIL'};  K1 trunc = extrap inside r_meas: {'PASS' if s['sg1_k1'] else 'FAIL'}")
    P(f"  VERDICT [{f}]: {v}")
    RES["footings"][f] = dict(cl2=s["cl2"], extrap=s["rep_bar"], trunc=s["sg1_trunc"], cls_trunc=pr, cls_extrap=s["sg1_cls_extrap"], Mstar_over_Mjam=ms, verdict=v)
checks["K2"] = C1["rss"] < 1.0
RES["checks"] = checks
fn = os.path.join(HERE_S, f"sg1_sluggs_imf_gas_results{TAGS}.json")
json.dump(RES, open(fn, "w"), indent=1, default=float)
P(f"\nchecks {sum(checks.values())}/{len(checks)}; child RSS {C1['rss']:.2f} GB; results sha256 {hashlib.sha256(open(fn, 'rb').read()).hexdigest()}")
open(os.path.join(HERE_S, f"sg1_sluggs_imf_gas{TAGS}.out"), "w").write("\n".join(NS2["OUT"]).replace(REPO_S, "<repo>") + "\n")
sys.exit(0 if all(checks.values()) else 1)
