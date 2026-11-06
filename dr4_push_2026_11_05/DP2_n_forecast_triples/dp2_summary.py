#!/usr/bin/env python3
"""DP2 summary: N range, sigma_fit models, D2 edges, Newtonian-sky decisiveness, N_R (FROZEN_CRITERIA.md 1.2-1.3).
Arithmetic on dp2_forecast_results.json and dp2_triples_results.json (K = 30, the frozen run). INFORMATION ONLY (owner D8).
Run: python3 -B dp2_summary.py -> dp2_summary.out / _results.json.  kappa = 1/2 FITTED; not theory closed."""
import sys
sys.dont_write_bytecode = True
import os, json, math

HERE = os.path.dirname(os.path.abspath(__file__))
F = json.load(open(os.path.join(HERE, "dp2_forecast_results.json")))
T = json.load(open(os.path.join(HERE, "dp2_triples_results.json")))
OUT = []
def P(s=""):
    OUT.append(s); print(s, flush=True)

Phi = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
S1, S2 = F["scenarios"]["S1"]["N"], F["scenarios"]["S2"]["N"]
s86, s30 = T["runs"]["8600"]["summary"], T["runs"]["30000"]["summary"]
rem10, rem20 = s86["0.1"]["DR4_removed_Dphys"], s86["0.2"]["DR4_removed_Dphys"]
N = {"low": S1 * (1 - rem20) * (1 - 0.034) * (1 - 0.05),
     "central": S2 * (1 - rem10) * (1 - 0.017),
     "high": float(S2), "DR3 (6,210)": 6210.0, "registered (30,000)": 30000.0}
P("DP2 summary (INFORMATION ONLY, owner D8; mock numbers are MOCKS). kappa = 1/2 FITTED; footings never pooled.")
P(f"precision forecast: S1 errors-only {S1:,}, S2 noise-shrunk {S2:,} (MC seeds {F['S2_seed_N']}); Dphys NSS removal at f_t 0.10 / 0.20: {rem10:.3f} / {rem20:.3f}")
for k, v in N.items():
    P(f"  N {k:20s} {v:8,.0f}")
ANCH = {"canonical": 1.1614, "alt": 1.1917}
GATE = {"canonical": 0.048, "alt": 0.058}


def mock_stats(foot, n):
    """Newton-sky mean and rms from the f_t = 0 mocks at 8,600 and 30,000, power-law in N for rms, linear in log N for the mean."""
    a, b = s86["0.0"][f"DR4_off|{foot}"], s30["0.0"][f"DR4_off|{foot}"]
    al = math.log(b["rms"] / a["rms"]) / math.log(30000 / 8600)
    rms = a["rms"] * (n / 8600) ** al
    sg = a["sg_mean"] * (n / 8600) ** (math.log(b["sg_mean"] / a["sg_mean"]) / math.log(30000 / 8600))
    t = (math.log(n) - math.log(8600)) / (math.log(30000) - math.log(8600))
    mu = a["mean"] + t * (b["mean"] - a["mean"])
    sh = s86["0.1"][f"DR4_on_Dphys|{foot}"]["mean"] - a["mean"]
    sh30 = s30["0.1"][f"DR4_on_Dphys|{foot}"]["mean"] - b["mean"]
    return mu, rms, sg, sh + t * (sh30 - sh)


rows = []
P("\nEdges (owner 11-05 2c rule): law-first excluded iff gamma_hat <= anchor - 3 sigma; screened excluded iff gamma_hat >= 1 + 3 sigma")
P("P_dec = P(gamma_hat <= law-first edge) for a Newton mock sky (f_t 0) / with the f_t 0.10 NSS-on (Dphys) shift added")
P(f"{'N':>20s} {'foot':4s} {'sfit model':10s} {'s_fit':>6s} {'s_sys':>6s} {'sigma':>6s} {'law edge':>8s} {'scr edge':>8s} {'band':>14s} {'P_dec':>6s} {'P_dec+t':>7s}  reading")
for nk, n in N.items():
    for foot in ("canonical", "alt"):
        mu, rms, sg, sh = mock_stats(foot, n)
        models = {"registered": 0.019 * math.sqrt(30000 / n), "DR3-cal": 0.055 * math.sqrt(6210 / n), "mock": max(sg, rms)}
        for mn, sf in models.items():
            for ss in (0.020, 0.0375):
                sig = math.hypot(sf, ss)
                le, se = ANCH[foot] - 3 * sig, 1 + 3 * sig
                band = f"{le:.3f}-{se:.3f}" if le < se else f"overlap {se:.3f}-{le:.3f}"
                pd = Phi((le - mu) / rms); pdt = Phi((le - mu - sh) / rms)
                reading = "DECISIVE" if pd >= 0.95 else "LIKELY" if pd >= 0.5 else "UNDECIDED-likely"
                rows.append(dict(N_label=nk, N=n, footing=foot, sfit_model=mn, sigma_fit=sf, sigma_sys=ss, sigma=sig,
                                 law_first_edge=le, screened_edge=se, newton_mu=mu, newton_rms=rms, P_decisive=pd,
                                 P_decisive_triples010=pdt, shift_triples010=sh, reading=reading, gate_pass=ss < GATE[foot]))
                P(f"{nk:>20s} {foot[:4]:4s} {mn:10s} {sf:6.4f} {ss:6.4f} {sig:6.4f} {le:8.4f} {se:8.4f} {band:>14s} {pd:6.3f} {pdt:7.3f}  {reading}")
P("\nsigma_sys(b) gate (< 0.048 canonical / < 0.058 alt): passes for sigma_sys 0.020 and 0.0375 on both footings.")
P("Newton-sky mock mean / rms used: " + "; ".join(f"{k} {f}: mu {mock_stats(f, n)[0]:.4f} rms {mock_stats(f, n)[1]:.4f}"
                                                   for k, n in N.items() for f in ("canonical",)))
P("\nR statistic (CFG943 A0: N_R = 2,095 of 30,000 = 0.0698; sigma_R formula part = hypot(0.019 sqrt(30000/N_R), 0.020); sigma_boot not modelled)")
Rrows = []
for nk, n in N.items():
    nr = 0.0698 * n
    sR = math.hypot(0.019 * math.sqrt(30000 / nr), 0.020)
    Rrows.append(dict(N_label=nk, N=n, N_R=nr, sigma_R=sR, kill_R=1 + max(0.01, 3 * sR)))
    P(f"  {nk:20s} N {n:8,.0f}: N_R {nr:6.0f}, sigma_R {sR:.4f}, KILL needs R >= {1 + max(0.01, 3 * sR):.3f}")
json.dump(dict(N=N, edges=rows, R=Rrows, information_only=True), open(os.path.join(HERE, "dp2_summary_results.json"), "w"), indent=1)
open(os.path.join(HERE, "dp2_summary.out"), "w").write("\n".join(OUT) + "\n")
