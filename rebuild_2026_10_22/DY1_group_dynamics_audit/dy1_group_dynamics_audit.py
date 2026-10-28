#!/usr/bin/env python3
"""DY1_group_dynamics_audit: sigma recomputed from KT2017 member velocities (gapper, 3-sigma clip) on GA1's audited rows; HG2's sign regraded.
Frozen criteria 6707283e80 (committed alone). Machinery: GA1's committed script (133f61510d) executed read-only up to its graded runs
(which itself executes HO1 91cc5c3bd4 read-only).

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, not a particle; not theory closed;
nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I dy1_group_dynamics_audit.py      (DY1_MUTATE=1 twin)
"""
import os, sys, json, math, hashlib, resource
import numpy as np

MUT = os.environ.get("DY1_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
GA1 = os.path.join(REB, "GA1_group_gas_audit", "ga1_group_gas_audit.py")
src = open(GA1).read()
src = src[:src.index('RES = dict(criteria="5afacf2b5c"')]
os.environ.pop("GA1_MUTATE", None)
NS = {"__file__": os.path.join(HERE, "ga1_ro.py"), "__name__": "ga1_ro"}
exec(compile(src, GA1, "exec"), NS)
P, hg1, hg2, ref, A0, nu, FEET, SEED, audit = (NS[k] for k in ("P", "hg1", "hg2", "ref", "A0", "nu", "FEET", "SEED", "audit"))
MPC, KEV, MU, MP, IDX, F = NS["MPC"], NS["KEV"], NS["MU"], NS["MP"], NS["IDX"], NS["F"]
P("\n================ DY1_group_dynamics_audit (criteria 6707283e80)" + ("  [MUTATE: sigma_aud x1.5 in the rows]" if MUT else ""))
checks = {}

def gapper(v):
    v = np.sort(np.asarray(v, float)); n = len(v)
    if n < 2: return float("nan")
    i = np.arange(1, n); w = i * (n - i)
    return float(math.sqrt(math.pi) / (n * (n - 1)) * np.sum(w * np.diff(v)))

def clip_sigma(v):
    v = np.asarray(v, float)
    while True:
        s = gapper(v); m = np.median(v)
        keep = np.abs(v - m) <= 3 * s
        if keep.all() or keep.sum() < 2: return s, len(v)
        v = v[keep]

# K1: gapper on a synthetic Gaussian
syn = np.random.default_rng(20261028).normal(0.0, 300.0, 2000)
checks["K1"] = abs(gapper(syn) / 300.0 - 1) < 0.03
P(f"  K1 gapper on N 2000, sigma 300: {gapper(syn):.1f} km/s: {'PASS' if checks['K1'] else 'FAIL'}")

# member velocities by group (KT2017 galaxies: PGC, RA, Dec, HRV, Ksmag, PGC1)
MEM = {}
for l in open(os.path.join(REPO, "real_research", "data", "kt2017_galaxies.tsv")):
    if l.startswith("#") or not l.strip(): continue
    p = l.rstrip("\n").split("\t")
    try: MEM.setdefault(int(p[5]), []).append(float(p[3]))
    except (ValueError, IndexError): continue

def dyn_rows(base_rows, nmin=5, drop_mis=False):
    out, tab = [], []
    for r in base_rows:
        v = [x for x in MEM.get(int(r["name"]), []) if np.isfinite(x) and x > -900]
        s, n = clip_sigma(v) if len(v) >= 2 else (float("nan"), len(v))
        t = dict(group=r["name"], flag=r["flag"], sigma_cat=r["sigma"], sigma_aud=s, n_vel=len(v), n_clip=n,
                 ratio=(s / r["sigma"]) if r["sigma"] > 0 else float("nan"))
        if r["flag"] == "BRIGHT":
            j = IDX.get(str(r["erass"]).strip()); kT = float(F["KT"][j]) if j is not None else float("nan")
            t["beta_spec_aud"] = (s * 1e3) ** 2 / (kT * KEV / (MU * MP)) if np.isfinite(s) and kT > 0 else float("nan")
            t["beta_spec_cat"] = (r["sigma"] * 1e3) ** 2 / (kT * KEV / (MU * MP)) if kT > 0 else float("nan")
        tab.append(t)
        if not (np.isfinite(s) and n >= nmin and s > 0): t["dropped"] = f"n_clip {n} < {nmin}"; continue
        if drop_mis and r["flag"] == "BRIGHT" and not (1 / 3 <= t["beta_spec_cat"] <= 3): t["dropped"] = "MISMATCHED (GA1)"; continue
        q = dict(r); sa = s * (1.5 if MUT else 1.0)
        q["sigma"] = sa; q["gobs"] = 3 * (sa * 1e3) ** 2 / (r["r_mpc"] * MPC); q["_saud"] = s
        out.append(q)
    return out, tab

def grade(rows, emg, label, gap_ref):
    NS["NS"]["rows"] = rows; NS["NS"]["EMG"] = emg
    dm = hg2.deltas(rows, ref); Dm, nb, nf = hg1.D_stat(rows, dm)
    rng = np.random.default_rng(SEED); pw = hg1.power(rows, dm, rng); lo, hi, _ = hg2.bootstrap(rows, ref, rng)
    gbar = np.array([r["gbar"] for r in rows]); lref = ref.logref(gbar)
    o = dict(n_rows=len(rows), n_bright=sum(r["flag"] == "BRIGHT" for r in rows), D_meas=Dm, ci95=[lo, hi], power=pw, nb_shared=nb, nf_shared=nf, footings={})
    for f in FEET:
        gp = NS["NS"]["group_pred"](f)[0]
        Dp = hg1.D_stat(rows, np.log10(gp) - lref)[0]; Dl = hg1.D_stat(rows, np.log10(gbar * nu(gbar / A0[f])) - lref)[0]
        gap = abs(Dp - Dm)
        cls = "UNDERPOWERED" if nb < 6 else ("DYNAMICS AUDIT RECONCILES THE SIGN" if lo <= Dp <= hi else
              ("DYNAMICS AUDIT MOVES THE SIGN BUT DOES NOT RECONCILE" if gap <= 0.7 * gap_ref[f] else "DYNAMICS AUDIT DOES NOT HELP"))
        o["footings"][f] = dict(D_pred_base=Dp, D_pred_all_law=Dl, gap=gap, cls=cls)
    P(f"\n=== {label}: rows {o['n_rows']}, BRIGHT {o['n_bright']} (shared-bin BRIGHT {nb} / FAINT {nf})")
    P(f"  measured D {Dm:+.4f}  95% [{lo:+.4f}, {hi:+.4f}]  power {pw:.3f}")
    for f in FEET:
        x = o["footings"][f]; P(f"  [{f}] D_pred base {x['D_pred_base']:+.4f}, all-law {x['D_pred_all_law']:+.4f}; gap {x['gap']:.3f} -> {x['cls']}")
    return o

GAP = {"canonical": 0.668, "alt": 0.644}
ga_rows, ga_emg, _, _ = audit("ac")
RES = dict(criteria="6707283e80", machinery="GA1 133f61510d (read-only)", mutate=MUT, runs={})
r0 = grade([dict(r) for r in ga_rows], ga_emg, "STEP 0 = V-cat (GA1 PRIMARY, catalogue sigma)", GAP)
k0 = abs(r0["D_meas"] - (-0.36229)) < 5e-5 and abs(r0["footings"]["canonical"]["D_pred_base"] - 0.30590) < 5e-5 and abs(r0["footings"]["alt"]["D_pred_base"] - 0.28210) < 5e-5
checks["K0"] = bool(k0); P(f"  K0 reproduces GA1 PRIMARY (D -0.3623, D_pred +0.3059 / +0.2821): {'PASS' if k0 else 'FAIL'}")
RES["runs"]["V_cat"] = r0
prim_rows, tab = dyn_rows(ga_rows)
RES["runs"]["PRIMARY"] = grade(prim_rows, ga_emg, "PRIMARY (sigma from member velocities, Nm >= 5)", GAP)
RES["runs"]["PRIMARY"]["table"] = tab
r10, _ = dyn_rows(ga_rows, nmin=10); RES["runs"]["V_10"] = grade(r10, ga_emg, "V-10 (Nm >= 10)", GAP)
rk, _ = dyn_rows(ga_rows, drop_mis=True); RES["runs"]["V_kT"] = grade(rk, ga_emg, "V-kT (GA1 MISMATCHED dropped)", GAP)
checks["K2"] = all(abs(q["gobs"] / (3 * (q["_saud"] * 1e3) ** 2 / (q["r_mpc"] * MPC)) - 1) < 1e-12 for q in prim_rows)
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9; checks["K3"] = peak < 1.0
fin = [t for t in tab if np.isfinite(t["ratio"])]
P(f"\n  sigma_aud / sigma_cat: median {np.median([t['ratio'] for t in fin]):.3f}, 16-84% [{np.percentile([t['ratio'] for t in fin], 16):.2f}, {np.percentile([t['ratio'] for t in fin], 84):.2f}] over {len(fin)} groups; dropped {sum('dropped' in t for t in tab)}")
P("  BRIGHT groups: group | n_vel/n_clip | sigma cat -> aud | beta_spec cat -> aud")
for t in tab:
    if t["flag"] == "BRIGHT":
        P(f"   {t['group']:>8s} {t['n_vel']:3d}/{t['n_clip']:3d}  {t['sigma_cat']:5.0f} -> {t['sigma_aud']:6.1f}  b_spec {t['beta_spec_cat']:.2f} -> {t['beta_spec_aud']:.2f}  {t.get('dropped', '')}")
P(f"\n  K2 g_obs = 3 sigma_aud^2 / r: {'PASS' if checks['K2'] else 'FAIL'};  K3 peak RSS {peak:.2f} GB: {'PASS' if checks['K3'] else 'FAIL'}")
RES["verdict"] = {f: RES["runs"]["PRIMARY"]["footings"][f]["cls"] for f in FEET}; RES["checks"] = checks
P(f"\n=== VERDICT (PRIMARY): canonical {RES['verdict']['canonical']}; alt {RES['verdict']['alt']}")
fn = os.path.join(HERE, f"dy1_group_dynamics_audit_results{TAG}.json")
json.dump(RES, open(fn, "w"), indent=1, default=float)
P(f"checks {sum(checks.values())}/{len(checks)}; results sha256 {hashlib.sha256(open(fn, 'rb').read()).hexdigest()}")
open(os.path.join(HERE, f"dy1_group_dynamics_audit{TAG}.out"), "w").write("\n".join(NS["NS"]["OUT"]).replace(REPO, "<repo>") + "\n")
sys.exit(0 if all(checks.values()) else 1)
