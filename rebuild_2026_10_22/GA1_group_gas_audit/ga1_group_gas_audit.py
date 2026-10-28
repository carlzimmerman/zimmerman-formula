#!/usr/bin/env python3
"""GA1_group_gas_audit: data-only audit of HG2's X-ray-bright groups' hot gas, then HG2's sign regraded on the audited rows.
Frozen criteria 5afacf2b5c (committed alone). Machinery: HO1's committed script (91cc5c3bd4) executed read-only up to its grade
block (HG2/HG1 rows, blue-lens reference, D_stat, bootstrap, the base picture's group_pred), as DS1 does.

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, not a particle; not theory closed;
nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I ga1_group_gas_audit.py      (GA1_MUTATE=1 twin)
"""
import os, sys, json, math, hashlib, resource
import numpy as np
from astropy.io import fits

MUT = os.environ.get("GA1_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
HO1 = os.path.join(REB, "HO1_xcop_hotgas_heldout", "ho1_heldout.py")
src = open(HO1).read()
src = src[:src.index("# ------------------------------------------------------------------ 6. grade per footing")]
src = src.replace('"ho1_heldout.out"', '"ga1_ho1_step0_STOPPED.out"').replace('"ho1_heldout_results.json"', '"ga1_ho1_step0_STOPPED.json"')
os.environ.pop("HO1_MUTATE", None)
NS = {"__file__": os.path.join(HERE, "ho1_ro.py"), "__name__": "ho1_ro"}
exec(compile(src, HO1, "exec"), NS)
P, hg1, hg2, ref, A0, nu, FEET, SEED = NS["P"], NS["hg1"], NS["hg2"], NS["ref"], NS["A0"], NS["nu"], NS["FEET"], NS["SEED"]
ROWS0 = [dict(r) for r in NS["rows"]]; EMG0 = {k: list(v) for k, v in NS["EMG"].items()}
G, MSUN, MPC = hg1.G, hg1.MSUN, hg1.MPC
H_NAT = 0.6856427; MU, MP, KEV = 0.6, 1.67262192e-27, 1.602176634e-16
P("\n================ GA1_group_gas_audit (criteria 5afacf2b5c)" + ("  [MUTATE: rule (a) disabled]" if MUT else ""))
checks = {}

# ---------- Lovisari+2015 fits (h70 -> native h)
lov = [l.rstrip("\n").split("\t") for l in open(os.path.join(REPO, "real_research", "data", "lovisari2015_groups.tsv")) if l.strip() and not l.startswith("#")]
hdr = lov[0]; L = [dict(zip(hdr, r)) for r in lov[1:]]
lkT = np.log10([float(r["kT_keV"]) for r in L]); lMg = np.log10([float(r["Mgas500_1e12"]) * 1e12 for r in L]); lR = np.log10([float(r["R500_kpc"]) / 1e3 for r in L])
b, a = np.polyfit(lkT, lMg, 1); d, c = np.polyfit(lkT, lR, 1)
sMg = float(np.std(lMg - (a + b * lkT), ddof=2)); sR = float(np.std(lR - (c + d * lkT), ddof=2))
hc = 0.70 / H_NAT
ratio25 = float(np.median([float(r["Mgas2500_1e12"]) / float(r["Mgas500_1e12"]) for r in L]))
prof = float(hg1.beta_mass_fraction(0.45, 1.0))
P(f"  Lovisari fits (N {len(L)}, h70): log Mgas500 = {a:.4f} + {b:.4f} log kT (rms {sMg:.3f} dex); log R500[Mpc] = {c:.4f} + {d:.4f} log kT (rms {sR:.3f} dex)")
P(f"  profile check: beta-model M(<0.45 R500)/M(<R500) = {prof:.3f} vs Lovisari median Mgas2500/Mgas500 = {ratio25:.3f}")

# ---------- eRASS1 KT by name
F = fits.open(os.path.join(REPO, "real_research", "data", "erass1cl_primary_v3.2.fits"))[1].data
IDX = {str(n).strip(): i for i, n in enumerate(F["NAME"])}

def audit(mode, sig_shift=0.0):
    """mode: 'none' | 'a' (dedupe, eRASS gas) | 'ac' (PRIMARY) | 'abc' (V-b). Returns audited rows, EMG, table."""
    rows = [dict(r) for r in ROWS0]; emg = {k: [tuple(e) for e in v] for k, v in EMG0.items()}; tab = []
    if mode == "none":
        return rows, emg, tab, 0
    by = {}
    for i, r in enumerate(rows):
        if r["flag"] == "BRIGHT": by.setdefault(r["erass"], []).append(i)
    drop = set()
    if not MUT:
        for e, ii in by.items():
            if len(ii) > 1:
                keep = sorted(ii, key=lambda i: (-rows[i]["Nm"], rows[i]["name"]))[0]
                drop |= {i for i in ii if i != keep}
    nmis = 0
    for i, r in enumerate(rows):
        if r["flag"] != "BRIGHT" or i in drop: continue
        j = IDX.get(str(r["erass"]).strip())
        kT = float(F["KT"][j]) if j is not None else float("nan")
        bspec = (r["sigma"] * 1e3) ** 2 / (kT * KEV / (MU * MP)) if np.isfinite(kT) and kT > 0 else float("nan")
        mis = not (1 / 3 <= bspec <= 3)
        row = dict(erass=r["erass"], group=r["name"], sigma=r["sigma"], Nm=r["Nm"], kT=kT, beta_spec=bspec, mismatched=bool(mis),
                   mgas500_erass=float(emg[r["erass"]][0][4]), mstar=r["mstar"], gas_to_star_before=float(emg[r["erass"]][0][4]) / r["mstar"])
        if mode in ("ac", "abc"):
            if not (np.isfinite(kT) and kT > 0):
                drop.add(i); row["dropped"] = "no eRASS1 kT"; tab.append(row); continue
            m5 = 10 ** (a + b * math.log10(kT) + sig_shift * sMg) * hc ** 2.5
            r5 = 10 ** (c + d * math.log10(kT) + sig_shift * sR) * hc
            mg = m5 * hg1.beta_mass_fraction(r["r_mpc"], r5)
            K1 = abs(mg / (m5 * hg1.beta_mass_fraction(r["r_mpc"], r5)) - 1) < 1e-12
            r["mgas"] = mg; r["gbar"] = G * (0.5 * r["mstar"] + mg) * MSUN / (r["r_mpc"] * MPC) ** 2
            e0 = emg[r["erass"]][0]; emg[r["erass"]] = [(e0[0], e0[1], e0[2], e0[3], m5, r5)]
            row.update(mgas500_aud=m5, r500_aud=r5, ratio_erass_over_aud=row["mgas500_erass"] / m5, gas_to_star_after=m5 / r["mstar"], k1=bool(K1))
        if mode == "abc" and mis:
            drop.add(i); row["dropped"] = "MISMATCHED"
        nmis += mis; tab.append(row)
    rows = [r for i, r in enumerate(rows) if i not in drop]
    return rows, emg, tab, nmis

def grade(mode, sig_shift=0.0, label=None):
    rows, emg, tab, nmis = audit(mode, sig_shift)
    NS["rows"] = rows; NS["EMG"] = emg
    dm = hg2.deltas(rows, ref)
    Dm, nb, nf = hg1.D_stat(rows, dm)
    rng = np.random.default_rng(SEED)                                    # A1: HG2's order - power first, then bootstrap, one generator
    pw = hg1.power(rows, dm, rng)
    lo, hi, _ = hg2.bootstrap(rows, ref, rng)
    gbar = np.array([r["gbar"] for r in rows]); lref = ref.logref(gbar)
    out = dict(mode=mode, sig_shift=sig_shift, n_rows=len(rows), n_bright=sum(r["flag"] == "BRIGHT" for r in rows), D_meas=Dm, ci95=[lo, hi],
               power=pw, nb_shared=nb, nf_shared=nf, n_mismatched=nmis, table=tab, footings={})
    for f in FEET:
        gp, _, _, _ = NS["group_pred"](f)
        Dp = hg1.D_stat(rows, np.log10(gp) - lref)[0]
        Dl = hg1.D_stat(rows, np.log10(gbar * nu(gbar / A0[f])) - lref)[0]
        rec = lo <= Dp <= hi
        unaud = {"canonical": abs(0.2293 - (-0.294)), "alt": abs(0.2011 - (-0.294))}[f]
        if nb < 6: cls = "UNDERPOWERED"
        elif rec: cls = "GAS AUDIT RECONCILES THE SIGN"
        elif abs(Dp - Dm) <= 0.7 * unaud: cls = "GAS AUDIT MOVES THE SIGN BUT DOES NOT RECONCILE"
        else: cls = "GAS AUDIT DOES NOT HELP"
        out["footings"][f] = dict(D_pred_base=Dp, D_pred_all_law=Dl, gap=abs(Dp - Dm), gap_unaudited=unaud, cls=cls)
    P(f"\n=== {label or mode}: rows {out['n_rows']}, BRIGHT {out['n_bright']} (shared-bin BRIGHT {nb} / FAINT {nf}), MISMATCHED {nmis}")
    P(f"  measured D {Dm:+.4f}  95% [{lo:+.4f}, {hi:+.4f}]  power {pw:.3f}")
    for f in FEET:
        o = out["footings"][f]
        P(f"  [{f}] D_pred base {o['D_pred_base']:+.4f}, all-law {o['D_pred_all_law']:+.4f}; gap {o['gap']:.3f} (unaudited {o['gap_unaudited']:.3f}) -> {o['cls']}")
    return out

RES = dict(criteria="5afacf2b5c", machinery="HO1 91cc5c3bd4 (read-only)", mutate=MUT,
           lovisari=dict(a=a, b=b, rms_Mg=sMg, c=c, d=d, rms_R=sR, N=len(L), h_conv=hc, profile_beta=prof, profile_lovisari=ratio25), runs={})
r0 = grade("none", label="STEP 0 (no audit)")
k0 = abs(r0["D_meas"] - NS["D0"]) < 1e-9 and abs(r0["ci95"][0] - NS["lo0"]) < 1e-9 and abs(r0["ci95"][1] - NS["hi0"]) < 1e-9 \
     and abs(r0["footings"]["canonical"]["D_pred_base"] - 0.2293) < 5e-5 and abs(r0["footings"]["alt"]["D_pred_base"] - 0.2011) < 5e-5
checks["K0"] = bool(k0); P(f"  K0 Step 0 reproduces HG2 D/CI and HO1(b) D_pred: {'PASS' if k0 else 'FAIL'}")
RES["runs"]["step0"] = r0
for key, args in (("V_a", ("a",)), ("PRIMARY", ("ac",)), ("V_b", ("abc",)), ("V_sig_plus", ("ac", +1.0)), ("V_sig_minus", ("ac", -1.0))):
    RES["runs"][key] = grade(*args, label=key)
pr = RES["runs"]["PRIMARY"]
checks["K1"] = all(t.get("k1", True) for t in pr["table"])
used = [t["erass"] for t in pr["table"] if "dropped" not in t]
checks["K2"] = len(used) == len(set(used))
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
checks["K3"] = peak < 1.0
P("\n  audit table (PRIMARY): eRASS1 source | group sigma | kT | beta_spec | Mgas500 eRASS1 -> audited (ratio) | gas/star before -> after")
for t in pr["table"]:
    P(f"   {t['erass']:26s} s {t['sigma']:4.0f} kT {t['kT']:.2f} b_spec {t['beta_spec']:.2f}{' MISMATCHED' if t['mismatched'] else ''}  "
      + (f"{t['mgas500_erass']:.2e} -> {t['mgas500_aud']:.2e} ({t['ratio_erass_over_aud']:.2f})  g/s {t['gas_to_star_before']:.2f} -> {t['gas_to_star_after']:.2f}"
         if "mgas500_aud" in t else t.get("dropped", "")))
P(f"\n  K1 audited gas = Mgas500,aud x beta fraction: {'PASS' if checks['K1'] else 'FAIL'};  K2 one source per BRIGHT group: {'PASS' if checks['K2'] else 'FAIL'};  K3 peak RSS {peak:.2f} GB: {'PASS' if checks['K3'] else 'FAIL'}")
RES["verdict"] = {f: pr["footings"][f]["cls"] for f in FEET}; RES["checks"] = checks
P(f"\n=== VERDICT (PRIMARY): canonical {RES['verdict']['canonical']}; alt {RES['verdict']['alt']}")
fn = os.path.join(HERE, f"ga1_group_gas_audit_results{TAG}.json")
json.dump(RES, open(fn, "w"), indent=1, default=float)
P(f"checks {sum(checks.values())}/{len(checks)}; results sha256 {hashlib.sha256(open(fn, 'rb').read()).hexdigest()}")
open(os.path.join(HERE, f"ga1_group_gas_audit{TAG}.out"), "w").write("\n".join(NS["OUT"]).replace(REPO, "<repo>") + "\n")
sys.exit(0 if all(checks.values()) else 1)
