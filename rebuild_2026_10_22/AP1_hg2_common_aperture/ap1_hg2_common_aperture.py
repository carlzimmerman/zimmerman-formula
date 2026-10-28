#!/usr/bin/env python3
"""AP1_hg2_common_aperture: HG2's sign at a common physical aperture for both arms (member-light stars + beta-model gas, g_obs = 3 sigma^2 / r_ap).
Frozen criteria 5bb77f83c6 (committed alone). Machinery: GA1's committed script (133f61510d) executed read-only up to its graded runs.

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, not a particle; not theory closed;
nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I ap1_hg2_common_aperture.py      (AP1_MUTATE=1 twin)
"""
import os, sys, json, math, hashlib, resource
import numpy as np

MUT = os.environ.get("AP1_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
GA1 = os.path.join(REB, "GA1_group_gas_audit", "ga1_group_gas_audit.py")
src = open(GA1).read(); src = src[:src.index('RES = dict(criteria="5afacf2b5c"')]
os.environ.pop("GA1_MUTATE", None)
NS = {"__file__": os.path.join(HERE, "ga1_ro.py"), "__name__": "ga1_ro"}
exec(compile(src, GA1, "exec"), NS)
P, hg1, hg2, ref, A0, nu, FEET, SEED, audit = (NS[k] for k in ("P", "hg1", "hg2", "ref", "A0", "nu", "FEET", "SEED", "audit"))
HO = NS["NS"]; MEM = HO["mem"]; G, MSUN, MPC = hg1.G, hg1.MSUN, hg1.MPC
P("\n================ AP1_hg2_common_aperture (criteria 5bb77f83c6)" + ("  [MUTATE: light counted outside r_ap]" if MUT else ""))
checks = {}

def geom(r):
    ms = [m for m in MEM.get(int(r["name"]), []) if np.isfinite(m[4])]
    d = r["d_mpc"]
    lk = np.array([10 ** (-0.4 * (m[4] - 5 * np.log10(d * 1e6) + 5 - 3.28)) for m in ms])
    ra = np.array([m[1] for m in ms]); de = np.array([m[2] for m in ms])
    cra, cde = np.average(ra, weights=lk), np.average(de, weights=lk)
    rp = hg1.sep_rad(ra, de, cra, cde) * d
    return lk, rp

def mstar_ap(lk, rp, rap):
    sel = (rp >= rap) if MUT else (rp < rap)
    return 0.6 * float(lk[sel].sum())

def ap_rows(base_rows, emg, rap):
    out, nd, rh = [], 0, {"BRIGHT": [], "FAINT": []}; k1 = True
    for r in base_rows:
        lk, rp = geom(r)
        k1 &= abs(mstar_ap(lk, rp, 10.0) / (0.6 * lk.sum()) - 1) < 1e-9 if lk.sum() > 0 else True
        rh[r["flag"]].append(float(np.median(rp)))
        ms = mstar_ap(lk, rp, rap)
        if r["flag"] == "BRIGHT":
            e = emg[r["erass"]][0]; mg = e[4] * hg1.beta_mass_fraction(rap, e[5])
        else:
            mg = 0.0
        if ms <= 0: nd += 1; continue
        q = dict(r); q["r_mpc"] = rap; q["mgas"] = mg
        q["gbar"] = G * (ms + mg) * MSUN / (rap * MPC) ** 2; q["gobs"] = 3 * (r["sigma"] * 1e3) ** 2 / (rap * MPC)
        out.append(q)
    return out, nd, {k: float(np.median(v)) for k, v in rh.items()}, k1

def grade(rows, emg, label):
    HO["rows"] = rows; HO["EMG"] = emg
    dm = hg2.deltas(rows, ref); Dm, nb, nf = hg1.D_stat(rows, dm)
    rng = np.random.default_rng(SEED); pw = hg1.power(rows, dm, rng); lo, hi, _ = hg2.bootstrap(rows, ref, rng)
    gbar = np.array([r["gbar"] for r in rows]); lref = ref.logref(gbar)
    o = dict(n_rows=len(rows), n_bright=sum(r["flag"] == "BRIGHT" for r in rows), D_meas=Dm, ci95=[lo, hi], power=pw, nb=nb, nf=nf, footings={})
    for f in FEET:
        gp = HO["group_pred"](f)[0]
        Dp = hg1.D_stat(rows, np.log10(gp) - lref)[0]; Dl = hg1.D_stat(rows, np.log10(gbar * nu(gbar / A0[f])) - lref)[0]
        if nb < 6: cls = "UNDERPOWERED"
        elif lo <= Dp <= hi: cls = "GEOMETRY EXPLAINS THE SIGN"
        elif hi < 0 and Dp > hi: cls = "SIGN SURVIVES A COMMON APERTURE"
        else: cls = "APERTURE MOVES THE SIGN"
        o["footings"][f] = dict(D_pred_base=Dp, D_pred_all_law=Dl, cls=cls)
    P(f"\n=== {label}: rows {o['n_rows']}, BRIGHT {o['n_bright']} (shared-bin BRIGHT {nb} / FAINT {nf})")
    P(f"  measured D {Dm:+.4f}  95% [{lo:+.4f}, {hi:+.4f}]  power {pw:.3f}")
    for f in FEET:
        x = o["footings"][f]; P(f"  [{f}] D_pred base {x['D_pred_base']:+.4f}, all-law {x['D_pred_all_law']:+.4f} -> {x['cls']}")
    return o

ga_rows, ga_emg, _, _ = audit("ac")
RES = dict(criteria="5bb77f83c6", machinery="GA1 133f61510d (read-only)", mutate=MUT, runs={})
r0 = grade([dict(r) for r in ga_rows], ga_emg, "STEP 0 (GA1 PRIMARY, own apertures)")
checks["K0"] = abs(r0["D_meas"] - (-0.36229)) < 5e-5 and abs(r0["footings"]["canonical"]["D_pred_base"] - 0.30590) < 5e-5 and abs(r0["footings"]["alt"]["D_pred_base"] - 0.28210) < 5e-5
P(f"  K0 reproduces GA1 PRIMARY: {'PASS' if checks['K0'] else 'FAIL'}")
RES["runs"]["step0"] = r0
k1all = True
for lab, rap, base in (("PRIMARY r_ap 0.5 Mpc", 0.5, "ga"), ("V r_ap 0.3 Mpc", 0.3, "ga"), ("V r_ap 0.8 Mpc", 0.8, "ga"), ("V HG2 original rows, r_ap 0.5", 0.5, "orig")):
    if base == "ga": br, em = ga_rows, ga_emg
    else: br, em, _, _ = audit("none")
    rows, nd, rh, k1 = ap_rows(br, em, rap); k1all &= k1
    o = grade(rows, em, lab); o.update(dropped_zero_light=nd, median_Rh_Mpc=rh); RES["runs"][lab] = o
    P(f"  median R_h: BRIGHT {rh['BRIGHT']:.3f} Mpc, FAINT {rh['FAINT']:.3f} Mpc; dropped (no light inside r_ap) {nd}")
checks["K1"] = bool(k1all)
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9; checks["K2"] = peak < 1.0
RES["verdict"] = {f: RES["runs"]["PRIMARY r_ap 0.5 Mpc"]["footings"][f]["cls"] for f in FEET}; RES["checks"] = checks
P(f"\n  K1 aperture light at 10 Mpc = all members: {'PASS' if checks['K1'] else 'FAIL'};  K2 peak RSS {peak:.2f} GB")
P(f"=== VERDICT (PRIMARY): canonical {RES['verdict']['canonical']}; alt {RES['verdict']['alt']}")
fn = os.path.join(HERE, f"ap1_hg2_common_aperture_results{TAG}.json")
json.dump(RES, open(fn, "w"), indent=1, default=float)
P(f"checks {sum(checks.values())}/{len(checks)}; results sha256 {hashlib.sha256(open(fn, 'rb').read()).hexdigest()}")
open(os.path.join(HERE, f"ap1_hg2_common_aperture{TAG}.out"), "w").write("\n".join(HO["OUT"]).replace(REPO, "<repo>") + "\n")
sys.exit(0 if all(checks.values()) else 1)
