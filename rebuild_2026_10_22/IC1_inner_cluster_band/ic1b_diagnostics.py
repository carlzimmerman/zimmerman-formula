#!/usr/bin/env python3
"""IC1_inner_cluster_band -- POST-RUN DIAGNOSTICS of OS1's one cluster miss (INNER M-all). Labelled, NOT graded.

Run before any criteria were frozen; nothing here is a grade. q = OS1's q_f per footing (0.892 / 0.748).
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ic1b_diagnostics.py   -> ic1b_diagnostics.out, _results.json
"""
import os, sys, json, math, time, resource
T0 = time.time()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import ic1b_lib as L

OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
P("IC1_inner_cluster_band DIAGNOSTICS (post-run, labelled, not graded). kappa = 1/2 FITTED; footings never pooled; "
  "cold dark energy, not matter; not theory closed")
RES = {}
for foot in L.FEET:
    q = L.QF[foot]; R = RES[foot] = {}
    P(f"\n=== [{foot}] q_f = {q:.3f} (OS1)")
    # D0 reproduction
    base = {}; vecs = {}
    for hk in L.HK:
        V, VC, ns = L.cluster_vectors(foot, hk, q); c, vB, vC = L.cells_from(foot, hk, V); base[hk] = c; vecs[hk] = (V, vB, vC)
    o1 = L.OS1J["footings"][foot]["clusters"]["cells"]
    d0 = max(abs(base[hk][k]["pred"] - o1[hk][k]["pred"]) for hk in L.HK for k in o1[hk])
    P(f"D0 reproduces OS1 cells: max |dpred| {d0:.1e}")
    R["D0"] = d0
    for hk in L.HK:
        a, b = base[hk]["G-IN-Mall"], base[hk]["G-IN-all"]
        P(f"   {hk}: G-IN-Mall meas {a['meas']:.3f}+-{a['s']:.3f} pred {a['pred']:.3f} Z {a['Z']:+.2f} (pred/meas {a['pred']/a['meas']:.2f}); "
          f"G-IN-all (KT) meas {b['meas']:.3f}+-{b['s']:.3f} pred {b['pred']:.3f} Z {b['Z']:+.2f} (pred/meas {b['pred']/b['meas']:.2f})")
    # D1 terciles
    P("D1 INNER by MGAS500 tercile (M_terc|INNER, s_IN) and by KT tercile (KT_terc|INNER, s_IN):")
    R["D1"] = {}
    for hk in L.HK:
        o = L.M[f"{foot}|{hk}"]; V, vB, vC = vecs[hk]; kt, ktC = vB[L.I], vC[L.I]; rows = {}
        for t in range(3):
            m = L.T3M == t; pm = float(vB[m, 0].sum() / vC[m, 0].sum()); mm = o["M_terc|INNER"][t]
            pk = float(kt[L.TID == t, 0].sum() / ktC[L.TID == t, 0].sum()); mk = o["KT_terc|INNER"][t]
            rows[f"M{t+1}"] = dict(meas=mm["A"], s=mm["s_IN"], pred=pm, Z=(mm["A"] - pm) / mm["s_IN"])
            rows[f"T{t+1}"] = dict(meas=mk["A"], s=mk["s_IN"], pred=pk, Z=(mk["A"] - pk) / mk["s_IN"])
        # each tercile's share of the M-all INNER over-prediction (pred - meas) * d_t / d_all
        dall = vC[:, 0].sum(); n_ = L.MEAS[(foot, hk)]["n"][:, 0]
        share = {f"M{t+1}": float((vB[L.T3M == t, 0].sum() - n_[L.T3M == t].sum()) / (vB[:, 0].sum() - n_.sum())) for t in range(3)}
        R["D1"][hk] = dict(rows=rows, share_of_overprediction=share)
        P(f"   {hk}: " + "; ".join(f"{k} {v['meas']:.2f}+-{v['s']:.2f} pred {v['pred']:.2f} Z {v['Z']:+.2f}" for k, v in rows.items()))
        P(f"   {hk}: share of M-all INNER excess (pred - meas, d-weighted): " + ", ".join(f"{k} {v:+.2f}" for k, v in share.items()))
    # D2 error budget
    P("D2 INNER error budget (s_IN = sqrt(s_STAT^2 + A_x^2 + A_RR^2)):")
    R["D2"] = {}
    for hk in L.HK:
        o = L.M[f"{foot}|{hk}"]; r = {}
        for key, cell in (("M_all|INNER", "G-IN-Mall"), ("KT_all|INNER", "G-IN-all")):
            m = o[key]; pr = base[hk][cell]["pred"]
            r[cell] = dict(A=m["A"], s_STAT=m["s"], A_x=m["A_x"], A_RR=m["A_RR"], s_IN=m["s_IN"], Z_IN=(m["A"] - pr) / m["s_IN"], Z_STAT=(m["A"] - pr) / m["s"])
        zkt_with_mall_err = (o["KT_all|INNER"]["A"] - base[hk]["G-IN-all"]["pred"]) / o["M_all|INNER"]["s_IN"]
        r["Z_KT_at_Mall_error"] = zkt_with_mall_err; R["D2"][hk] = r
        P(f"   {hk}: " + "; ".join(f"{c} A {v['A']:.2f} s_STAT {v['s_STAT']:.2f} A_x {v['A_x']:+.2f} A_RR {v['A_RR']:+.2f} s_IN {v['s_IN']:.2f} "
                                    f"Z_IN {v['Z_IN']:+.2f} Z_STAT {v['Z_STAT']:+.2f}" for c, v in r.items() if isinstance(v, dict))
          + f"; KT-all at M-all's error: Z {zkt_with_mall_err:+.2f}")
    # D3 miscentering scale and a BCG point mass (direction only)
    P("D3 miscentering (offset x0 / x2, model AND C* denominator re-built; meas re-normalised) and BCG point mass 1e12 Msun (direction):")
    R["D3"] = {}
    for hk in L.HK:
        r = {}
        n_ = L.MEAS[(foot, hk)]["n"][:, 0]; s0M = L.M[f"{foot}|{hk}"]["M_all|INNER"]["s_IN"]; s0K = L.M[f"{foot}|{hk}"]["KT_all|INNER"]["s_IN"]
        d0all = L.bsum(L.DC[(foot, hk)])[:, 0]
        for lab, kw in (("off x0", dict(offscale=0.0)), ("off x2", dict(offscale=2.0)), ("BCG 1e12", dict(mbcg=1e12))):
            V, VC, _ = L.cluster_vectors(foot, hk, q, **kw); vB, vC = L.bsum(V)[:, 0], L.bsum(VC)[:, 0]
            out = {}
            for cell, Ix, s0 in (("G-IN-Mall", L.ALLI, s0M), ("G-IN-all", L.I, s0K)):
                pr = vB[Ix].sum() / vC[Ix].sum(); me = n_[Ix].sum() / vC[Ix].sum(); s = s0 * d0all[Ix].sum() / vC[Ix].sum()
                out[cell] = dict(pred=float(pr), meas=float(me), s=float(s), Z=float((me - pr) / s))
            r[lab] = out
            P(f"   {hk} {lab:8s}: " + "; ".join(f"{c} meas {v['meas']:.2f} pred {v['pred']:.2f} Z {v['Z']:+.2f}" for c, v in out.items()))
        R["D3"][hk] = r
    # D4 shape
    P("D4 shape at OS1's q_f: non-singular isothermal (King r0, LN1 T7's premise) vs Burkert, same Sigma = rho0 r0, same mass rule:")
    ci, oki, nsat = L.grade(foot, q, "isothermal")
    s_iso = L.sparc(foot, L.BGS["A_c2b_refit"], q, "isothermal")
    fails_b = [k for k, v in L.OS1J["footings"][foot]["clusters"]["ok"].items() if not v]
    P(f"   SPARC A at q_f: isothermal rms {s_iso['rms']:.4f} @ U {s_iso['U_median']:.2f} (Burkert {L.OS1J['footings'][foot]['sparc_A']['rms']:.4f}); "
      f"cluster saturations {nsat}")
    for k in ci["h0672"]:
        P(f"     {k:10s} Burkert Z {base['h0672'][k]['Z']:+.2f}/{base['h0686'][k]['Z']:+.2f}  isothermal Z {ci['h0672'][k]['Z']:+.2f}/{ci['h0686'][k]['Z']:+.2f}"
          + ("" if oki[k] else "  FAIL"))
    P(f"   fails: Burkert {fails_b}; isothermal {[k for k in oki if not oki[k]]}")
    R["D4"] = dict(sparc_iso=dict(rms=s_iso["rms"], U=s_iso["U_median"]), cells_iso=ci, ok_iso=oki, nsat=nsat)
    # D5 tercile fill of sigma
    P("D5 sigma fill (220 clusters without KT take their MGAS500 tercile's median sigma_KT):")
    R["D5"] = {}
    for hk in L.HK:
        V, vB, vC = vecs[hk]; c = L.MEAS[(foot, hk)]; r = {}
        for lab, Ix in (("KT clusters", np.where(L.OKK)[0]), ("filled clusters", np.where(~L.OKK)[0])):
            ms = L.NX["meas_stats"](c, Ix, "INNER", 31000 + len(Ix)); pr = float(vB[Ix, 0].sum() / vC[Ix, 0].sum())
            r[lab] = dict(n=len(Ix), meas=ms["A"], s_IN=ms["s_IN"], pred=pr, Z=(ms["A"] - pr) / ms["s_IN"])
        # alternative fill (reported only): log sigma_KT vs log Mgas500 OLS on KT clusters
        lm = np.log10(np.asarray(L.NX["MY"]["Mgas500"], float)); ls = np.log10(L.SIG_C)
        A_ = np.c_[np.ones(L.OKK.sum()), lm[L.OKK]]; co = np.linalg.lstsq(A_, ls[L.OKK], rcond=None)[0]
        sig2 = L.SIG_C.copy(); sig2[~L.OKK] = 10 ** (co[0] + co[1] * lm[~L.OKK])
        V2, _, _ = L.cluster_vectors(foot, hk, q, sig=sig2); c2 = L.cells_from(foot, hk, V2)[0]
        r["regression fill"] = dict(slope=float(co[1]), Z_Mall=c2["G-IN-Mall"]["Z"], pred_Mall=c2["G-IN-Mall"]["pred"],
                                    fails=[k for k in c2 if abs(c2[k]["Z"]) > 2])
        R["D5"][hk] = r
        P(f"   {hk}: " + "; ".join(f"{k} (n {v['n']}) meas {v['meas']:.2f}+-{v['s_IN']:.2f} pred {v['pred']:.2f} Z {v['Z']:+.2f}"
                                    for k, v in r.items() if "n" in v)
          + f"; regression fill (slope {co[1]:.3f}): G-IN-Mall pred {c2['G-IN-Mall']['pred']:.2f} Z {c2['G-IN-Mall']['Z']:+.2f}, |Z|>2 at this h: {r['regression fill']['fails']}")
    P(f"   [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
open(os.path.join(L.HERE, "ic1b_diagnostics.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(L.HERE, "ic1b_diagnostics_results.json"), "w"), indent=1, default=float)
