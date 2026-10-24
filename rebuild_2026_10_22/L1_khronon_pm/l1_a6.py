#!/usr/bin/env python3
"""L1_khronon_pm AMENDMENT A6 reader: the DBI-IC set (BS25's BBN-viable DBI K; sets cap30 = mu_K 14.8 h/Mpc, lambda_D 30, and
P1 = BS24 P1 223 kpc, lambda_D 30), 256^3 and 384^3, mu_K 14.8, z_i 199. FROZEN_CRITERIA A6 item 5: REPORTED, never pooled,
no verdict weight -
  * sigma8_PM per cell and the P(k) ratio against A5's S0 at the same N (the dust limit, same phases);
  * rho_NL = (sigma8[KX] - sigma8[LIN]) / (sigma8[S0] - sigma8[LIN]) per set and footing, with the frozen reading bands,
    each marked "indicative";
  * halo dust/baryon ratios (0.3-1 and 1-3 Mpc), satellites (1-3 Mpc from a cluster-class or top50 halo) vs field (none
    within 3 Mpc), from the engine's own halo classes.
Reads only completed cells (work/prod/A6_*/result.json, status "done"); cells still running are listed as pending.

  OMP_NUM_THREADS=1 nice -n 15 python3 l1_a6.py            -> l1_a6.out, l1_a6_results.json
  L1_MUTATE=1 ...  : the S0 control is replaced by the set's LIN cell, so rho_NL has a zero denominator -> A4 must FAIL.
kappa = 1/2 FITTED; footings never pooled; never 'the data favour the framework'; no dark-matter particle."""
import glob, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROD = os.path.join(HERE, "work", "prod")
MUT = os.environ.get("L1_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUT else ""
OUT, CHK = [], {}
RES = {"lane": "L1_khronon_pm", "part": "A6 DBI-IC set (reported only, no verdict weight)", "mutate": MUT, "sets": {}}
KREF = (0.1, 0.3, 1.0)


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(name, ok, val, thr):
    CHK[name] = dict(ok=bool(ok), value=val, threshold=thr); P(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")


def reading(rho):
    if not math.isfinite(rho):
        return "undefined"
    if rho >= 0.5:
        r = "the nonlinear J_x term restores most of the linear deficit"
    elif rho >= 0.1:
        r = "partial"
    elif rho <= -0.1:
        r = "deepens the deficit"
    else:
        r = "does not restore growth"
    return r + " (indicative; A6 reported only)"


def load(tag):
    fn = os.path.join(PROD, tag, "result.json")
    if not os.path.exists(fn):
        return None
    r = json.load(open(fn))
    return r if r.get("status") == "done" else None


def pk_ratio(F, S):
    kF, PF = F["snap"]["z0"]["k"], F["snap"]["z0"]["P"]
    kS, PS = S["snap"]["z0"]["k"], S["snap"]["z0"]["P"]
    out = {}
    for k0 in KREF:
        i = min(range(len(kF)), key=lambda j: abs(math.log(kF[j] / k0)) if kF[j] > 0 else 1e9)
        out[str(k0)] = dict(k=kF[i], ratio=PF[i] / PS[i] if PS[i] else float("nan"))
    return out


def halos(r):
    h = r["snap"]["z0"].get("halos") or {}
    cl = h.get("classes", {})
    pick = lambda c: {k: cl.get(c, {}).get(k) for k in ("n", "ratio_0p3_1_median", "ratio_1_3_median")}
    return dict(n_halos=h.get("n_halos"), cosmic_tau_over_b=h.get("cosmic_tau_over_b"), satellite=pick("satellite_1_3Mpc"),
                field=pick("field_gt3Mpc"), galaxy=pick("galaxy"))


conv, rhos, pending, controls = [], [], [], []
for N in (256, 384):
    S0 = load(f"A5_S0_N{N}_zi199")
    controls.append((N, S0 is not None))
    for sset in ("cap30", "P1"):
        cells = {m: load(f"A6_{m}_dbi_{sset}_N{N}_zi199") for m in ("LIN", "KX_can", "KX_alt")}
        missing = [m for m, r in cells.items() if r is None]
        if missing or S0 is None:
            pending.append(f"{sset}@{N}: " + ("S0 control missing; " if S0 is None else "") + ", ".join(missing))
            continue
        L = cells["LIN"]
        norm = L if MUT else S0
        row = {"S0_sigma8": S0["snap"]["z0"]["sigma8"]}
        for m, r in cells.items():
            conv.append(r["nonconverged_calls"] == 0)
            z = r["snap"]["z0"]
            row[m] = dict(sigma8=z["sigma8"], sigma8_b=z["sigma8_b"], sigma8_tau=z["sigma8_tau"], sigma8_over_S0=z["sigma8"] / row["S0_sigma8"],
                          lamD=r["cfg"].get("lamD"), nonconverged=r["nonconverged_calls"], peak_rss_gb=r["peak_rss_gb"],
                          pk_ratio_vs_S0=pk_ratio(r, S0), halos=halos(r))
        for f in ("can", "alt"):
            den = norm["snap"]["z0"]["sigma8"] - L["snap"]["z0"]["sigma8"]
            rho = (row[f"KX_{f}"]["sigma8"] - row["LIN"]["sigma8"]) / den if den != 0 else float("nan")
            row[f"rho_NL_{f}"] = rho; row[f"reading_{f}"] = reading(rho); rhos.append((N, sset, f, rho))
        RES["sets"][f"{sset}@{N}"] = row
        P(f"{sset} @ {N}^3 (lambda_D {row['LIN']['lamD']}): sigma8 S0 {row['S0_sigma8']:.4f}, LIN {row['LIN']['sigma8']:.4f} "
          f"({row['LIN']['sigma8_over_S0']:.3f} of S0), KX-can {row['KX_can']['sigma8']:.4f}, KX-alt {row['KX_alt']['sigma8']:.4f}; "
          f"rho_NL {row['rho_NL_can']:+.4f} / {row['rho_NL_alt']:+.4f}: {row['reading_can']}")
        for m in ("LIN", "KX_can", "KX_alt"):
            pk = row[m]["pk_ratio_vs_S0"]; hh = row[m]["halos"]
            P(f"   {m}: P/P_S0 " + ", ".join(f"k {v['k']:.2f} {v['ratio']:.3g}" for v in pk.values())
              + f"; halos {hh['n_halos']} (satellites {hh['satellite']['n']}, field {hh['field']['n']}); dust/baryon 0.3-1 Mpc "
              f"sat {hh['satellite']['ratio_0p3_1_median']} field {hh['field']['ratio_0p3_1_median']} (cosmic {hh['cosmic_tau_over_b']})")

RES["pending"] = pending
P("pending: " + ("; ".join(pending) if pending else "none"))
check("A1", any(ok for _, ok in controls), "; ".join(f"S0-{N} {'present' if ok else 'missing'}" for N, ok in controls), "an A5 S0 control exists")
check("A2", len(conv) > 0 and all(conv), f"{sum(conv)}/{len(conv)} completed A6 cells with every hold call converged", "all")
check("A3", len(RES["sets"]) > 0, f"{len(RES['sets'])} complete (set, N) groups", ">= 1")
check("A4", len(rhos) > 0 and all(math.isfinite(r) for *_, r in rhos), "; ".join(f"{s}@{N}/{f}: {r:+.4f}" for N, s, f, r in rhos), "rho_NL finite")
RES["checks"] = CHK
npass = sum(c["ok"] for c in CHK.values())
P(f"L1_A6 COMPLETE: {npass}/{len(CHK)} checks PASS.  (reported only; no verdict weight; the frozen 512^3 production run decides)")
open(os.path.join(HERE, f"l1_a6{SUF}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"l1_a6{SUF}_results.json"), "w"), indent=1, default=float)
sys.exit(0 if npass == len(CHK) else 1)
