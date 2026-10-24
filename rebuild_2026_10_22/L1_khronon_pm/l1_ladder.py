#!/usr/bin/env python3
"""L1_khronon_pm AMENDMENT A5 ladder reader: per-rung statistics of the resolution ladder (128 / 256 / 384, mu_K 14.8,
z_i 199, NSEED 512), with the frozen definitions of FROZEN_CRITERIA.md section 4 and A4/A5. Convergence only: NO verdict,
never pooled with the 512^3 cells; every reading carries the word "indicative". Reads only completed cells
(work/prod/A5_*/result.json with status "done"); rungs still running are listed as pending.

  OMP_NUM_THREADS=1 nice -n 15 python3 l1_ladder.py            -> l1_ladder.out, l1_ladder_results.json
  L1_MUTATE=1 ...  : the S0 normaliser is replaced by the LIN cell, so rho_NL has a zero denominator -> L4 must FAIL.
kappa = 1/2 FITTED; footings never pooled; never 'the data favour the framework'; no dark-matter particle."""
import glob, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROD = os.path.join(HERE, "work", "prod")
MUT = os.environ.get("L1_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUT else ""
OUT, CHK = [], {}
RES = {"lane": "L1_khronon_pm", "part": "A5 ladder (convergence only, no verdict)", "mutate": MUT, "rungs": {}}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(name, ok, val, thr):
    CHK[name] = dict(ok=bool(ok), value=val, threshold=thr); P(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")


def reading(rho):
    """FROZEN_CRITERIA.md section 4 bands, with the A5 word 'indicative'."""
    if not math.isfinite(rho):
        return "undefined"
    if rho >= 0.5:
        r = "the nonlinear J_x term restores most of the linear deficit"
    elif rho >= 0.1:
        r = "partial"
    elif rho <= -0.1:
        r = "deepens the deficit"
    elif abs(rho) < 0.1:
        r = "does not restore growth"
    else:
        r = "between bands"
    return r + " (indicative, convergence only; the frozen 512^3 production run decides)"


cells = {}
for fn in sorted(glob.glob(os.path.join(PROD, "A5_*", "result.json"))):
    r = json.load(open(fn))
    if r.get("status") == "done":
        cells[os.path.basename(os.path.dirname(fn))] = r
pending = sorted(os.path.basename(d) for d in glob.glob(os.path.join(PROD, "A5_*")) if os.path.basename(d) not in cells)
P(f"completed A5 cells: {sorted(cells)}")
P(f"not completed (pending or running): {pending}")
RES["completed"], RES["pending"] = sorted(cells), pending


def cell(mode, N, ic="", foot=""):
    tag = f"A5_{mode}{('_' + foot) if foot else ''}_N{N}_zi199{('_' + ic) if ic else ''}"
    return tag, cells.get(tag)


def stats(r):
    z = r["snap"]["z0"]
    d = dict(sigma8_pm=z["sigma8"], sigma8_b=z["sigma8_b"], sigma8_tau=z["sigma8_tau"], sigma8_lin_box=r["ic"]["sigma8_lin_box"],
             ratio_pm_lin=z["sigma8"] / r["ic"]["sigma8_lin_box"], nonconverged=r["nonconverged_calls"], peak_rss_gb=r["peak_rss_gb"])
    h = z.get("halos") or {}
    if h:
        rat = [x for x in (h.get("catalog_top200", {}).get("ratio_0p3_1") or []) if isinstance(x, (int, float)) and math.isfinite(x)]
        rat.sort()
        d["halos"] = dict(n_halos=h.get("n_halos"), classes={k: v.get("n") for k, v in h.get("classes", {}).items()},
                          dust_over_baryon_0p3_1_median=(rat[len(rat) // 2] if rat else None), cosmic_tau_over_b=h.get("cosmic_tau_over_b"),
                          cell_Mpc_phys=h.get("cell_Mpc_phys"))
    return d


all_conv, s0_ok, lin_ok, rho_ok = [], [], [], []
for N in (128, 256, 384):
    tS, S = cell("S0", N); tL, L = cell("LIN", N)
    if S is None or L is None:
        P(f"rung {N}^3: S0 or LIN not completed -> pending"); continue
    rung = {"S0": stats(S), "LIN": stats(L)}
    s0n = rung["LIN"] if MUT else rung["S0"]
    all_conv += [S["nonconverged_calls"] == 0, L["nonconverged_calls"] == 0]
    s0_ok.append((N, rung["S0"]["ratio_pm_lin"])); lin_ok.append((N, rung["LIN"]["ratio_pm_lin"]))
    for foot in ("can", "alt"):
        tK, K = cell("KX", N, foot=foot)
        if K is None:
            P(f"rung {N}^3 KX-{foot}: pending"); continue
        rung[f"KX_{foot}"] = stats(K); all_conv.append(K["nonconverged_calls"] == 0)
        den = s0n["sigma8_pm"] - rung["LIN"]["sigma8_pm"]
        rho = (rung[f"KX_{foot}"]["sigma8_pm"] - rung["LIN"]["sigma8_pm"]) / den if den != 0 else float("nan")
        rung[f"rho_NL_{foot}"] = rho; rung[f"reading_{foot}"] = reading(rho); rho_ok.append((N, foot, rho))
    if N == 384:  # A4/A5 LOB-IC pair at 384, control S0-384
        tLL, LL = cell("LIN", N, ic="LOB"); tKL, KL = cell("KX", N, ic="LOB", foot="can")
        if LL is not None and KL is not None:
            rung["LIN_LOB"], rung["KX_can_LOB"] = stats(LL), stats(KL)
            all_conv += [LL["nonconverged_calls"] == 0, KL["nonconverged_calls"] == 0]
            den = s0n["sigma8_pm"] - rung["LIN_LOB"]["sigma8_pm"]
            rho = (rung["KX_can_LOB"]["sigma8_pm"] - rung["LIN_LOB"]["sigma8_pm"]) / den if den != 0 else float("nan")
            rung["rho_NL_LOB_can"] = rho; rung["reading_LOB_can"] = reading(rho); rho_ok.append((N, "LOB_can", rho))
        else:
            P("rung 384^3 LOB-IC pair: pending")
    RES["rungs"][str(N)] = rung
    P(f"rung {N}^3: sigma8_PM S0 {rung['S0']['sigma8_pm']:.4f}, LIN {rung['LIN']['sigma8_pm']:.4f}"
      + "".join(f", KX-{f} {rung['KX_' + f]['sigma8_pm']:.4f} (rho_NL {rung['rho_NL_' + f]:+.4f}: {rung['reading_' + f]})" for f in ("can", "alt") if f"KX_{f}" in rung)
      + (f"; LOB-IC rho_NL {rung['rho_NL_LOB_can']:+.4f}: {rung['reading_LOB_can']}" if "rho_NL_LOB_can" in rung else ""))
    for f in ("can", "alt"):
        h = rung.get(f"KX_{f}", {}).get("halos")
        if h:
            P(f"   KX-{f} halos (reported only): n {h['n_halos']} {h['classes']}; median dust/baryon in 0.3-1 Mpc {h['dust_over_baryon_0p3_1_median']} "
              f"(cosmic {h['cosmic_tau_over_b']:.3f}; cell {h['cell_Mpc_phys']:.3f} Mpc, resolution-limited)")

check("L1", len(all_conv) > 0 and all(all_conv), f"{sum(all_conv)}/{len(all_conv)} completed ladder cells with every hold call converged", "all")
check("L2", len(s0_ok) > 0 and all(0.98 <= v <= 1.15 for _, v in s0_ok), "; ".join(f"{n}: {v:.3f}" for n, v in s0_ok), "S0 sigma8_PM/sigma8_lin_box in [0.98, 1.15]")
check("L3", len(lin_ok) > 0 and all(0.98 <= v <= 1.30 for _, v in lin_ok), "; ".join(f"{n}: {v:.3f}" for n, v in lin_ok), "LIN sigma8_PM/sigma8_lin_box in [0.98, 1.30]")
check("L4", len(rho_ok) > 0 and all(math.isfinite(r) for *_, r in rho_ok), "; ".join(f"{n}/{f}: {r:+.4f}" for n, f, r in rho_ok), "rho_NL finite on every completed footing")
RES["checks"] = CHK
npass = sum(c["ok"] for c in CHK.values())
P(f"L1_LADDER COMPLETE: {npass}/{len(CHK)} checks PASS.  (convergence only; no verdict; the frozen 512^3 production run decides)")
open(os.path.join(HERE, f"l1_ladder{SUF}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"l1_ladder{SUF}_results.json"), "w"), indent=1, default=float)
sys.exit(0 if npass == len(CHK) else 1)
