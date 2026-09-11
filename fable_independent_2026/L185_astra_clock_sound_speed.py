#!/usr/bin/env python3
"""L185 -- DOES ASTRA'S CLOCK CLUSTER? The sound speed of the clock perturbation along astra's own radiation-majority branch
(qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026, commit c5ffc6b59; its modules are imported
READ-ONLY, nothing of astra's is edited or refitted). Method: astra's exact finite-k transfer operator mode_system(v, k) (6 x 6, state
(sigma, v, r1, v_r, theta1, drho_b)) is evaluated at each archived sample of the backward branch (radiation_002/result.json) and its
eigenvalues taken at k >> aH: a propagating pair has lambda^2 = -c_s^2 k^2/a^2 (frozen-coefficient WKB). The perfect-fluid radiation pair
must give c_s^2 = 1/3 (validation); the dust row gives ~0; the clock pair gives c_s^2(clock). Then the consequence, on the repository's
own CMB tooling: CLASS (kernel off, ./L183_class_mond_kernel/site) with CDM replaced by a w ~ 0 fluid of sound speed cs2 -- the third
peak at recombination vs cs2, and the linear P(k) at z = 3 (forest) and z = 0 vs cs2 -- locating astra's clock on that scan.
The branch is astra's dimensionless one (not recombination-calibrated); only the dimensionless c_s^2 is carried across. No literal-True checks."""
import sys, os, json, numpy as np
ASTRA = os.path.abspath("../qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026")
sys.path.insert(0, ASTRA); sys.path.insert(0, os.path.abspath("L183_class_mond_kernel/site"))
from radiation_probe import ProbeBackground          # astra's backward coefficient history + sourced background (read-only)
from transfer_evolve import mode_system               # astra's exact 6x6 finite-k transfer operator (read-only)
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("=" * 118 + "\nL185 THE CLOCK'S SOUND SPEED ON ASTRA'S RADIATION-MAJORITY BRANCH, AND WHAT IT MEANS FOR THE CMB AND THE FOREST\n" + "=" * 118)
R = json.load(open(os.path.join(ASTRA, "radiation_002/result.json"))); S = R["samples"]
bg = ProbeBackground(R["parameters"]["coefficient_efolds"])
KS = (300., 3000., 30000.)
rows = []
print("    a        H       s0      m_rel      c_s^2(rad) k=3e3   c_s^2(clock) at k = 300, 3000, 30000      naive k-essence form m_rel(1-s0 m)/(2-m) [diagnostic only]")
for smp in S[::23] + [S[-1]]:
    st = [smp["a"], smp["H"], smp["q"], smp["tau"], smp["rho_baryon"], smp["rho_radiation"]]
    v = bg.evaluate(st, extended=True)[0]; a = smp["a"]; H = smp["H"]; s0 = v["sbar"]; mrel = smp["relative_logarithm_margin"]
    cs_rad = cs_clk = None; clk = []; dust = None
    for k in KS:
        op = mode_system(v, k)[0]; lam = np.linalg.eigvals(op); c2 = -(lam ** 2) * a * a / (k * k)      # lambda^2 a^2/k^2 -> -c_s^2
        c2r = np.sort(np.real(c2))                                                                          # three pairs: clock, dust(~0), radiation(1/3)
        pairs = []
        used = np.zeros(6, bool)
        for i in np.argsort(-abs(c2)):                                                                      # pair by nearest value
            if used[i]: continue
            j = min((jj for jj in range(6) if jj != i and not used[jj]), key=lambda jj: abs(c2[jj] - c2[i])); used[i] = used[j] = True
            pairs.append(0.5 * (c2[i] + c2[j]).real)
        pairs = sorted(pairs)                                                                               # [smallest ... largest]
        rad = min(pairs, key=lambda x: abs(x - 1 / 3)); rest = sorted([p for p in pairs if p != rad], key=abs)
        d_, c_ = rest[0], rest[1]                                                                           # dust ~ 0, clock = the other
        clk.append(c_)
        if k == 3000.: cs_rad = rad
    naive = mrel * (1 - s0 * mrel) / (2 - mrel)
    rows.append(dict(a=a, H=H, s0=s0, mrel=mrel, cs2_rad=cs_rad, cs2_clock=clk, naive=naive))
    print(f"    {a:.4f}  {H:7.3f}  {s0:.4f}  {mrel:.3e}   {cs_rad:.5f}          " + "  ".join(f"{c:+.4e}" for c in clk) + f"          {naive:.4e}")
cs2_branch = [r["cs2_clock"][-1] for r in rows]
check("V1 [validation of the extraction] the perfect-fluid radiation pair of astra's operator gives c_s^2 = 1/3 within 1% at every sample (k = 3000)",
      all(abs(r["cs2_rad"] - 1 / 3) < 0.01 / 3 for r in rows), "c_s^2(rad) = " + " ".join(f"{r['cs2_rad']:.4f}" for r in rows))
check("V2 the clock pair's c_s^2 is converged in k (k = 3000 vs 30000 within 5% at every sample): a genuine frozen-coefficient sound speed",
      all(abs(r["cs2_clock"][2] / r["cs2_clock"][1] - 1) < 0.05 for r in rows), "ratios " + " ".join(f"{r['cs2_clock'][2]/r['cs2_clock'][1]:.3f}" for r in rows))
late = [r for r in rows if r["a"] >= 0.3]; early = [r for r in rows if r["a"] <= 0.25]
check("V3 [DEFICIT verified] GRADIENT INSTABILITY on the late branch: c_s^2 < 0 at every sample with a >= 0.3 (z <= 2.3), k-converged, i.e. real eigenvalues +/-|c_s| k/a growing without bound in k -- the frozen action is UV-ill-posed on its own late-time branch",
      len(late) >= 4 and all(r["cs2_clock"][-1] < 0 for r in late), "late c_s^2 = " + " ".join(f"{r['cs2_clock'][-1]:+.2e}" for r in late) + f"; growth rate |c_s| k/a = {np.sqrt(-min(r['cs2_clock'][-1] for r in late)):.3f} k/a vs H ~ 1")
check("V4 [computed] the sign changes along the branch: c_s^2 > 0 (1e-4 .. 7e-4) at every sample with a <= 0.25 -- gradient-stable and very soft early",
      len(early) >= 3 and all(0 < r["cs2_clock"][-1] < 1e-3 for r in early), "early c_s^2 = " + " ".join(f"{r['cs2_clock'][-1]:+.2e}" for r in early))
print("    NOTE: the naive k-essence form fails by factors -28 .. +3.6 (the cuscuton clock constraint enters the sub-horizon dispersion at O(k^2)); it carries no claim.")
# ---- consequence on the repository's own CMB/forest tooling: CDM -> w~0 fluid of sound speed cs2 ----
from classy import Class
h = 0.6736; base = {"h": h, "omega_b": 0.02237, "A_s": 2.1e-9, "n_s": 0.9649, "tau_reio": 0.0544, "N_ur": 3.046, "N_ncdm": 0, "YHe": 0.2454,
                    "output": "tCl,mPk", "l_max_scalars": 1500, "P_k_max_h/Mpc": 10., "z_pk": "0,3", "mond_a0": 0.0}
def run(extra):
    c = Class(); p = dict(base); p.update(extra); c.set(p); c.compute(); cl = c.raw_cl(1500); l = cl["ell"][2:]; D = l * (l + 1) * cl["tt"][2:] / (2 * np.pi)
    at = lambda r: D[np.argmin(abs(l - r))]; pk = {z: [c.pk(k * h, z) * h ** 3 for k in (0.2, 1., 5.)] for z in (0., 3.)}
    return at(816) / at(537), pk
L, pkL = run({"omega_cdm": 0.1200})
print(f"    CLASS scan (kernel off): CDM -> fluid w0 = -1e-4 (dust-like), Omega_fld = Omega_c, cs2_fld varied.  LCDM: peak3/peak2 = {L:.3f}")
print("    cs2_fld     peak3/peak2   restoration   P/P_LCDM(z=3) at k = 0.2, 1, 5 h/Mpc     P/P_LCDM(z=0) at k = 0.2, 1, 5 h/Mpc")
scan = {}
for cs2 in (1.0, 1e-2, 3e-3, 1e-3, 3e-4, 1e-4, 1e-5, 1e-6, 1e-8, 3e-9, 1e-9, 1e-10):
    r32, pk = run({"omega_cdm": 1e-6, "Omega_fld": 0.1200 / h ** 2, "w0_fld": -1e-4, "wa_fld": 0.0, "cs2_fld": cs2, "use_ppf": "no"})
    scan[cs2] = (r32, pk); rest = (r32 - scan[1.0][0]) / (L - scan[1.0][0]) if 1.0 in scan else float("nan")
    print(f"    {cs2:<10.0e}  {r32:.3f}         {rest:+.2f}          " + " ".join(f"{pk[3.][i]/pkL[3.][i]:.3f}" for i in range(3)) + "                      " + " ".join(f"{pk[0.][i]/pkL[0.][i]:.3f}" for i in range(3)))
cmb_ok = [c for c, (r, _) in scan.items() if (r - scan[1.0][0]) / (L - scan[1.0][0]) > 0.9]
forest_ok = [c for c, (_, pk) in scan.items() if pk[3.][2] / pkL[3.][2] > 0.9]
cs2_cmb = max(cmb_ok) if cmb_ok else 0.; cs2_forest = max(forest_ok) if forest_ok else 0.
pos = [r["cs2_clock"][-1] for r in early]; lo, hi = min(pos), max(pos)
print(f"    thresholds: third peak restored (> 0.9) for cs2 <= {cs2_cmb:.0e};  forest P(k = 5 h/Mpc, z = 3) within 10% for cs2 <= {cs2_forest:.0e};  astra's clock, early stable branch (a <= 0.25): c_s^2 = {lo:.1e} .. {hi:.1e}")
check("V5 [CMB proxy, the gate the EARLY clock passes] a w ~ 0 fluid restores the third peak for cs2 <= 1e-2, and the whole early-branch range lies below it: a clock this soft clusters on the acoustic scales (candidate for the clustering cold component of the L166 certificate) -- moot while V3 stands",
      cs2_cmb >= 1e-2 and hi <= cs2_cmb, f"early c_s^2 <= {hi:.1e} vs CMB threshold {cs2_cmb:.0e}")
check("V6 [forest, DEFICIT verified] the forest (P(k = 5 h/Mpc, z = 3) within 10%) needs cs2 below the computed threshold, and even the softest early-branch value exceeds it by > 1e3: as frozen, the clock is pressure-supported on Ly-alpha scales (L173/L174 velocity-filter kills apply)",
      cs2_forest > 0 and lo > 1e3 * cs2_forest, f"min early c_s^2 {lo:.1e} vs forest threshold {cs2_forest:.0e} (ratio {lo/max(cs2_forest,1e-300):.0e})")
# ---- adversarial checks on the load-bearing deficit (V3): eigenvector localisation and an independent background object ----
from transfer_evolve import Background
fwd = Background(0.02); vf = fwd.at(0.)[0]; opf = mode_system(vf, 3000.)[0]; lamf = np.linalg.eigvals(opf); c2f = np.sort(np.real(-(lamf ** 2) / 9e6))
smp = [r for r in S if abs(r["a"] - 0.4221) < 1e-3][0]; v42 = bg.evaluate([smp["a"], smp["H"], smp["q"], smp["tau"], smp["rho_baryon"], smp["rho_radiation"]], extended=True)[0]
lam, vec = np.linalg.eig(mode_system(v42, 3000.)[0]); i = int(np.argmax(np.real(lam))); w = abs(vec[:, i]) ** 2 / np.sum(abs(vec[:, i]) ** 2)
check("V7 [adversarial] astra's own FORWARD sourced background object (transfer_evolve.Background at t = 0, a = 1) reproduces the backward-history value c_s^2(clock) = -1.55e-3 within 1%: the deficit is not an artefact of the backward continuation",
      abs(c2f[0] / rows[0]["cs2_clock"][1] - 1) < 0.01, f"forward object: most negative pair {c2f[0]:+.4e} vs backward object {rows[0]['cs2_clock'][1]:+.4e}")
check("V8 [adversarial] at a = 0.42 the growing eigenvector (largest real eigenvalue, k = 3000) lives in the clock subspace: > 90% of its norm in the (sigma, v) components -- it is the clock mode, not dust or radiation",
      w[0] + w[1] > 0.9, "norm fractions (sigma, v, r1, v_r, theta1, drho_b) = " + " ".join(f"{x:.3f}" for x in w) + f"; Re lambda = {np.real(lam[i]):.1f} = {np.real(lam[i])*smp['a']/3000.:.4f} k/a")
print("    LIMITS: frozen-coefficient WKB sound speed from astra's exact linear operator (no mode coupling, gamma = 1e-6 kept); astra's branch is dimensionless\n"
      "    and not recombination-calibrated (c_s^2 carried across as a pure number); CLASS proxy = w0 = -1e-4 fluid with constant cs2 (astra's c_s^2 varies with the\n"
      "    margin along the branch: the scan brackets it); the forest threshold is a linear-P(k) 10% criterion at k = 5 h/Mpc, z = 3.")
json.dump(dict(rows=rows, cs2_cmb=cs2_cmb, cs2_forest=cs2_forest, scan={str(k): v[0] for k, v in scan.items()}), open("L185_results.json", "w"), indent=1, default=float)
print(f"\nL185 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
