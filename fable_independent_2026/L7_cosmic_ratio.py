#!/usr/bin/env python3
"""
L7 -- is the cluster residual simply the COSMIC dark-to-baryon share? The decisive diagnostic.
==============================================================================================
L2 established that what clusters require is not an interpolation function but "extra mass tracing the
baryons"; L5 and L6 closed the two structural ways to supply that without mass (a fixed-strength
finite-range force, and a screened force in potential, density or enclosed mass).  Every mechanism this
programme owns is now closed for the cluster residual.  That makes ONE question decisive, and it has not
been asked in this form: is the required source quantitatively the COSMIC dark-to-baryon ratio?

Because if it is, the economical reading of clusters is not a missing mechanism at all -- it is that
clusters contain cold dark matter at close to the universal abundance, which is the LambdaCDM answer, and
the thing needing explanation becomes the galaxy-scale success of the kernel rather than the cluster
failure.  If it is NOT -- if the required ratio is well away from cosmic, or varies wildly between
clusters -- then LambdaCDM owes an explanation too and the framework has room.

This test is adverse to the framework by construction if it passes, and is reported either way.

Definitions.  From the corrected X-COP audit: M_HSE(<r) = g_HSE r^2/G and M_bar(<r) = g_bar r^2/G.
  NEWTONIAN reading  : M_dark = M_HSE - M_bar,          ratio_N = M_dark/M_bar   (LambdaCDM's dark halo)
  FRAMEWORK reading  : M_resid = M_HSE - M_kernel,      ratio_F = M_resid/M_bar  (what the kernel still misses)
with M_kernel = [g_bar + a0 Delta(g_bar/a0)] r^2/G, nu_RAR saturated (THE_ACTION section 3).
The framework's prediction is ratio_F = 0.  LambdaCDM's prediction is ratio_N = Omega_dm/Omega_b = 5.43
corrected for the observed baryon depletion of clusters (they retain 70-90% of the cosmic share at R500,
so the expected ratio is 5.4-8.0, and it should be NEARLY UNIVERSAL across clusters).

  R0 [control]   the baryon fraction recovered from these rows at the outermost radius lands in the
                 observed cluster range f_bar = 0.08-0.18 (Vikhlinin/X-COP-class measurements). If this
                 fails the mass reconstruction is wrong and nothing below means anything;
  R1 [cosmic]    the NEWTONIAN dark-to-baryon ratio at the outermost audited radius is consistent with the
                 cosmic value 5.43 allowing 0-30% baryon depletion, i.e. inside 5.4-8.0;
  R2 [universal] that ratio is nearly universal across clusters: fractional scatter below 30%;
  R3 [framework] the framework's residual is consistent with its own prediction of ZERO, i.e. within the
                 measurement scatter of ratio_F = 0;
  R4 [trend]     the framework's residual does not grow systematically with radius (a residual that tracks
                 the acceleration is the signature of a kernel that is simply wrong, not of a mass);
  R5 [verdict]   the framework's reading of clusters is at least as economical as the cosmic-share reading.
Both a0 footings.  FAIL marks a requirement the stated reading does not meet.
"""
import numpy as np, math, json, os, sys
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = 6.674e-11; MSUN = 1.989e30; kpc = 3.0857e19; Mpc = 3.0857e22
H0 = 0.674*100e3/Mpc; Om, Ob, Od = 0.315, 0.049, 0.266
COSMIC = Od/Ob                                            # 5.43
print("=" * 118); print("L7 -- is the cluster residual the cosmic dark-to-baryon share?"); print("=" * 118, flush=True)
print(f"    cosmic Omega_dm/Omega_b = {COSMIC:.2f}; clusters retain 70-100% of the cosmic baryon share at R500,")
print(f"    so the LambdaCDM expectation for M_dark/M_bar is {COSMIC:.1f}-{COSMIC/0.7:.1f}, and it should be nearly universal.", flush=True)

def Delta(s):
    s = np.asarray(s, float); d = np.where(s > 0, s/np.expm1(np.sqrt(np.maximum(s, 1e-300))), 0.0)
    return np.where(s > 2.540, 0.6476, d)

CLJ = json.load(open(os.path.join(REPO, "qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026/results.json")))
A0 = CLJ["a0_m_s2"]; R500 = {d["name"]: d["own_R500_kpc"] for d in CLJ["radius_audit"]}
DAT = {}
for rw in CLJ["rows"]:
    foot = rw.get("footing", "canonical"); a0 = A0[foot]
    DAT.setdefault(foot, {}).setdefault(rw["cluster"], []).append(
        (float(rw["r_kpc"]), float(rw["g_baryon_over_a0"])*a0, float(rw["g_hse_over_a0"])*a0))

SUM = {}
for foot in sorted(DAT):
    a0 = A0[foot]; per = []
    for name, pts in DAT[foot].items():
        p = np.array(sorted(pts)); r = p[:, 0]*kpc; gb = p[:, 1]; gh = p[:, 2]
        Mb = gb*r**2/G; Mh = gh*r**2/G; Mk = (gb + a0*Delta(gb/a0))*r**2/G
        i = len(r) - 1                                              # outermost audited radius
        per.append(dict(name=name, r_kpc=r[i]/kpc, frac_R500=r[i]/kpc/R500.get(name, np.nan),
                        ratio_N=(Mh[i] - Mb[i])/Mb[i], ratio_F=(Mh[i] - Mk[i])/Mb[i],
                        fbar=Mb[i]/Mh[i],
                        trend=np.polyfit(np.log10(r/kpc), (Mh - Mk)/Mb, 1)[0]))
    SUM[foot] = per
    rN = np.array([x["ratio_N"] for x in per]); rF = np.array([x["ratio_F"] for x in per])
    fb = np.array([x["fbar"] for x in per]); tr = np.array([x["trend"] for x in per])
    print(f"\n    {foot}: {len(per)} clusters at r = {np.median([x['r_kpc'] for x in per]):.0f} kpc median "
          f"({np.nanmedian([x['frac_R500'] for x in per]):.2f} R500)")
    print(f"      baryon fraction f_bar        : median {np.median(fb):.3f}  [{fb.min():.3f}, {fb.max():.3f}]")
    print(f"      NEWTONIAN  M_dark/M_bar      : median {np.median(rN):.2f}  +/- {np.std(rN, ddof=1):.2f}  "
          f"({100*np.std(rN, ddof=1)/np.median(rN):.0f}% scatter)   [cosmic {COSMIC:.2f}]")
    print(f"      FRAMEWORK  M_resid/M_bar     : median {np.median(rF):.2f}  +/- {np.std(rF, ddof=1):.2f}  "
          f"({100*np.std(rF, ddof=1)/max(np.median(rF), 1e-9):.0f}% scatter)   [framework predicts 0]")
    print(f"      framework residual radial trend d(ratio_F)/dlog r: median {np.median(tr):+.2f} per dex", flush=True)
    for x in sorted(per, key=lambda y: -y["ratio_N"]):
        print(f"        {x['name'][:22]:22s} r = {x['r_kpc']:6.0f} kpc  f_bar {x['fbar']:.3f}   Newtonian {x['ratio_N']:5.2f}   framework {x['ratio_F']:5.2f}")

fb_all = np.array([x["fbar"] for f in SUM for x in SUM[f]])
check("R0 [control] the baryon fraction recovered from these rows lands in the observed cluster range 0.08-0.18",
      0.08 <= np.median(fb_all) <= 0.18, f"median f_bar = {np.median(fb_all):.3f}, range [{fb_all.min():.3f}, {fb_all.max():.3f}]")
rN_all = {f: np.array([x["ratio_N"] for x in SUM[f]]) for f in SUM}
check("R1 [cosmic] the Newtonian dark-to-baryon ratio at the outermost radius is consistent with the cosmic value allowing 0-30% baryon depletion (5.4-8.0)",
      all(COSMIC <= np.median(rN_all[f]) <= COSMIC/0.7 for f in rN_all),
      ", ".join(f"{f} median {np.median(rN_all[f]):.2f}" for f in rN_all) + f"; cosmic {COSMIC:.2f}, depleted-30% {COSMIC/0.7:.2f}")
check("R2 [universal] that ratio is nearly universal across clusters (fractional scatter below 30%)",
      all(np.std(rN_all[f], ddof=1)/np.median(rN_all[f]) < 0.30 for f in rN_all),
      ", ".join(f"{f} {100*np.std(rN_all[f], ddof=1)/np.median(rN_all[f]):.0f}%" for f in rN_all))
rF_all = {f: np.array([x["ratio_F"] for x in SUM[f]]) for f in SUM}
zF = {f: np.median(rF_all[f])/(np.std(rF_all[f], ddof=1)/math.sqrt(len(rF_all[f]))) for f in rF_all}
check("R3 [framework] the framework's residual is consistent with its own prediction of zero",
      all(abs(zF[f]) < 3 for f in zF), ", ".join(f"{f} median {np.median(rF_all[f]):.2f} M_bar, {abs(zF[f]):.0f} sigma from 0" for f in zF))
tr_all = {f: np.array([x["trend"] for x in SUM[f]]) for f in SUM}
check("R4 [trend] the framework's residual does not grow systematically with radius (a residual that tracks acceleration is a wrong kernel, not a mass)",
      all(abs(np.median(tr_all[f])) < 0.5 for f in tr_all), ", ".join(f"{f} {np.median(tr_all[f]):+.2f} per dex" for f in tr_all))
econ = all(abs(zF[f]) < 3 for f in zF)
check("R5 [verdict] the framework's reading of clusters is at least as economical as the cosmic-share reading",
      econ, "the Newtonian reading needs ONE number that is not fitted here -- the cosmic ratio, known independently from the CMB "
            "and BBN -- and reproduces the clusters with the scatter quoted in R2; the framework's reading needs a residual it predicts to be zero")
print("\n  what this does and does not show: it does NOT measure dark matter, and it does not touch the galaxy-scale"
      "\n  evidence, where baryons plus the kernel work and a cosmic-share halo would overshoot (g04k: 2.6 M_b inside 10 kpc"
      "\n  against the 0.25 M_b the RAR tolerates).  It shows only which reading of the CLUSTER rows is the more economical,"
      "\n  and that the number clusters ask for is one that LambdaCDM fixes independently rather than fits.")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "")); sys.exit(0)
