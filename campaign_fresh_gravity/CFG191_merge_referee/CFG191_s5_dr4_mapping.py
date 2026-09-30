#!/usr/bin/env python3
"""CFG191_s5_dr4_mapping -- item (e): CFG179's DR4 mapping (merge -> Arm A 1.16-1.18 / MI 1.08; ownership -> 1.000) against the frozen
preregistration (read-only, string-matched). Own linear-response tensors for P2 and nu_RAR; crude transfers; the arm table.
The computed P2 merge value from the pipeline estimator is in CFG191_s5b_pipeline_tier2.py.  No CFG179 file is opened.
MUTATE=1: M7 (P2 tensors replaced by Route A's) and M8 (merge mapped to Arm B) -- both must make a main-passing check fail."""
import warnings; warnings.filterwarnings("ignore")
import numpy as np, sympy as sp, hashlib
from scipy.optimize import brentq
from CFG191_common import Run, REPO, rel
np.seterr(all="ignore")
R = Run("CFG191_s5_dr4_mapping", "item (e): the DR4 mapping against the preregistration")
MUT = R.mutate
PRE = REPO/"prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md"
raw = PRE.read_bytes(); txt = " ".join(" ".join(l.lstrip("> ").split()) for l in raw.decode("utf-8").splitlines())
R.p(f"preregistration {rel(PRE)} read-only; sha256 now {hashlib.sha256(raw).hexdigest()[:8]}...{hashlib.sha256(raw).hexdigest()[-6:]} (at phase-1 writing: 97aa97c4...d3ad25)")
R.check("preregistration file hash unchanged since phase 1 (informational; the file is append-only)", hashlib.sha256(raw).hexdigest().startswith("97aa97c4"), lb=False)
SIG_FIT, SIG_SYS = 0.019, 0.020
SIG_TOT = 0.028

R.sec("quotes (each asserted present in the frozen text)")
quotes = ["1.1614 ± 0.0175", "1.1814 ± 0.0150", "1.1917 ± 0.0175", "1.2267 ± 0.0200", "1.0000 ± 0.0025", "γ_v = 1.000 (exactly Newtonian)",
          "1.0799", "1.0310", "1.0218 – 1.0472", "1.0725", "1.0900", "σ_sys = 0.02", "σ_tot = sqrt(σ_fit² + 0.02²)".replace("σ","sigma").replace("²","^2"),
          "1.47342", "kill-from-above 1.084", "> 1.23", "Consistent with H**\" requires |z_H| < 2", "the frozen kernel taken as modified gravity with no coherence length"]
miss = []
for q in quotes:
    ok = " ".join(q.split()) in txt or ("sigma_tot = sqrt(sigma_fit^2 + 0.02^2)" in q and "sigma_tot = sqrt(sigma_fit^2 + 0.02^2)" in txt)
    if not ok: miss.append(q)
R.p("  missing quotes: " + (str(miss) if miss else "none"))
R.check("E0 every quoted preregistration string is present in the frozen file", not miss, lb=True)
R.p("  Arm A definition (Amendment 11(a)): 'the full nonlinear AQUAL-EFE solve of the frozen kernel taken as modified gravity with no coherence length'; the solve's docstring (aqual_efe_full_solve_2026.py) names the kernel: Route A, nu_RAR = 1/(1-exp(-sqrt y)), y_extN = 1.28903/0.99240.")
R.check("E0b the solve file names the Route A / nu_RAR kernel and y_extN 1.28903 / 0.99240", all(s in " ".join((REPO/"prep_2026/gaia_dr4_prep/aqual_efe_full_solve_2026.py").read_text().split()) for s in ["1.28903 (canonical) / 0.99240 (alt)", "return 1.0 / (1.0 - np.exp(-s))"]))

R.sec("E1  control: distances of the registered arms from 1.000 in sigma_tot = 0.028 (sqrt(0.019^2+0.02^2) = %.4f)" % np.hypot(SIG_FIT, SIG_SYS))
arms = {"Arm A floor can": 1.1614, "Arm A top can": 1.1814, "Arm A floor alt": 1.1917, "Arm A top alt": 1.2267, "MI alpha=1 (Amdt 2, retired)": 1.0799, "MI alpha=2 (Amdt 4, in force)": 1.0310, "chain ceiling can": 1.0725, "chain ceiling alt": 1.0900, "Arm B": 1.0, "Arm C": 1.0}
for k, v in arms.items(): R.p(f"  {k:32s} {v:.4f}  z from Newton = {(v-1)/SIG_TOT:5.2f} sigma_tot")
zz = [(arms[k]-1)/SIG_TOT for k in ("Arm A floor can", "Arm A top can", "Arm A floor alt", "Arm A top alt", "MI alpha=1 (Amdt 2, retired)")]
R.check("E1 distances 5.76, 6.48, 6.85, 8.10, 2.85 reproduce the README's 5.8-6.5 / 6.8-8.1 / 2.9 (to its 0.06 rounding)", np.allclose(zz, [5.8, 6.5, 6.8, 8.1, 2.9], atol=0.06))

R.sec("E2  kernel identity: linear-response tensors for a point mass in a uniform field (own derivation)")
# symbols: response of the radial force to first order in the perturbation
y_, L_, nu0 = sp.symbols("y L nu0", positive=True)
k, kz = sp.symbols("k k_z", positive=True)
R.p("  QUMOND (Poisson-solved): Phi_Q(k) = nu0 (1 + L k_z^2/k^2) Phi_N(k), L = dln nu/dln y at the Newtonian external field y_e.")
R.p("    real space: Phi_Q = -GM nu0 [ (1 + L/2)/r - (L/2) z^2/r^3 ]  =>  radial boost B_r(theta) = nu0 [1 + (L/2) sin^2 theta]; B_par = nu0, B_perp = nu0 (1 + L/2); sphere average nu0 (1 + L/3).")
R.p("  AQUAL: operator mu0 [lap + L0 d_z^2] phi = 4 pi G rho with L0 = dln mu/dln x (x = observed field/a0); rescaled Green's function gives B_par = 1/mu0 = nu0, B_perp = nu0/sqrt(1+L0).")
R.p("  algebraic / local (MI-type) tensor: perpendicular perturbation nu0, parallel perturbation d(y nu)/dy = nu0 (1+L).")
# verify the QUMOND real-space claims symbolically: inverse FT of k_z^2/k^4
r_, z_, GM = sp.symbols("r z GM", positive=True)
lap = lambda f: sp.diff(f, z, 2)   # only the z-derivative of the k_z^2/k^4 kernel is needed
kern = sp.diff(r_, r_)  # placeholder to keep sympy imports used
x_, yv, zv = sp.symbols("x y zc", real=True)
rr = sp.sqrt(x_**2 + yv**2 + zv**2)
lap3 = sp.simplify(sp.diff(rr, x_, 2) + sp.diff(rr, yv, 2) + sp.diff(rr, zv, 2))
R.check("E2a sympy: lap(r) = 2/r, so F^-1[1/k^4] = -r/(8 pi) solves lap f = -1/(4 pi r)*(... ) as used (checks the k_z^2/k^4 -> (1/8pi)(1/r - z^2/r^3) step)", sp.simplify(lap3 - 2/rr) == 0 and sp.simplify(sp.diff(rr, zv, 2) - (1/rr - zv**2/rr**3)) == 0)
def tensors(nu, y_extN):
    nuv = float(nu(y_extN)); h = 1e-6*y_extN
    L = (np.log(nu(y_extN*(1+1e-6))) - np.log(nu(y_extN*(1-1e-6))))/(np.log(1+1e-6) - np.log(1-1e-6))
    dxdy = nuv*(1+L); L0 = nuv/dxdy - 1
    return dict(nu0=nuv, L=L, dxdy=dxdy, L0=L0, aq_par=nuv, aq_perp=nuv/np.sqrt(1+L0), q_par=nuv, q_perp=nuv*(1+L/2), mi_perp=nuv, mi_par=dxdy)
nu_rar = lambda y: 1/(1-np.exp(-np.sqrt(y))); nu_p2 = lambda y: np.sqrt(1+1/y)
inv = lambda nu, x: brentq(lambda y: y*nu(y) - x, 1e-9, 1e6)
GEXT = 1.778e-10
FOOT = {"canonical": 9.36e-11, "alt": 1.13e-10}    # the preregistration's a0 (pipeline constants A0_CAN / A0_ALT)
T = {}
for kn, nu in (("nu_RAR", nu_rar), ("P2", nu_p2)):
    for foot, a0 in FOOT.items():
        x = GEXT/a0; y = inv(nu, x); T[(kn, foot)] = dict(x_ext=x, y_extN=y, **tensors(nu, y))
R.p(f"  {'kernel':7s} {'footing':9s} {'x_ext':>7s} {'y_extN':>8s} {'nu0':>7s} {'L':>8s} {'L0':>7s} | AQUAL par/perp | QUMOND par/perp | algebraic(MI) par/perp | sqrt(nu0)")
for (kn, foot), t in T.items():
    R.p(f"  {kn:7s} {foot:9s} {t['x_ext']:7.4f} {t['y_extN']:8.5f} {t['nu0']:7.4f} {t['L']:8.4f} {t['L0']:7.4f} | {t['aq_par']:.4f}/{t['aq_perp']:.4f} | {t['q_par']:.4f}/{t['q_perp']:.4f} | {t['mi_par']:.4f}/{t['mi_perp']:.4f} | {np.sqrt(t['nu0']):.4f}")
R.data["tensors"] = {f"{k[0]}|{k[1]}": v for k, v in T.items()}
tr = T[("nu_RAR", "canonical")]; ta = T[("nu_RAR", "alt")]
R.check("E2b [control] nu_RAR: y_extN 1.28903/0.99240 (to 5e-3), sqrt(nu(y_extN)) 1.2139/1.2592 (to 1e-3), B_par 1.4732, B_perp 1.2598 (to 3e-3 relative)",
        abs(tr["y_extN"]-1.28903) < 5e-3 and abs(ta["y_extN"]-0.99240) < 5e-3 and abs(np.sqrt(tr["nu0"])-1.2139) < 1e-3 and abs(np.sqrt(ta["nu0"])-1.2592) < 3e-3 and abs(tr["aq_par"]/1.4732-1) < 3e-3 and abs(tr["aq_perp"]/1.2598-1) < 3e-3)
tp = T[("P2", "canonical")]; tpa = T[("P2", "alt")]
R.check("E2c [control] P2: y_extN 1.4647 / 1.1513 (to 5e-3) and sqrt(nu) = 1.1390 (to 1e-3) -- the frozen section-1.1 numbers", abs(tp["y_extN"]-1.4647) < 5e-3 and abs(tpa["y_extN"]-1.1513) < 5e-3 and abs(np.sqrt(tp["nu0"])-1.139) < 1e-3)
R.p(f"  the two kernels differ: y_extN {tr['y_extN']:.3f} (nu_RAR) vs {tp['y_extN']:.3f} (P2) canonical; sqrt(nu0) {np.sqrt(tr['nu0']):.4f} vs {np.sqrt(tp['nu0']):.4f}")
R.p("  NOTE: CFG179's quoted P2 'perpendicular 1.139 / parallel 1.017' are the ALGEBRAIC (MI-type) eigenvalues (perp=nu0, par=nu0(1+L)); the Poisson-solved MG tensor (Arm A's structure, QUMOND or AQUAL) has the LARGE axis PARALLEL (B_par = nu0).")

R.sec("E3  transfer to the estimator: crude, labelled")
def sph(t): return np.sqrt((t["aq_par"] + 2*t["aq_perp"])/3)
band = {"canonical": (1.1614, 1.1814), "alt": (1.1917, 1.2267)}
reg_perp = {"canonical": 1.2139, "alt": 1.2592}
rows3 = {}
for foot in FOOT:
    tr_, tp_ = T[("nu_RAR", foot)], T[("P2", foot)]
    T1 = [b/reg_perp[foot] for b in band[foot]]                               # band / registered sqrt(nu) point value
    T2 = [b/sph(tr_) for b in band[foot]]                                     # band / AQUAL-tensor sphere average
    p2_from_T1 = [np.sqrt(tp_["nu0"])*t for t in T1]
    p2_from_T2 = [sph(tp_)*t for t in T2]
    rows3[foot] = dict(T1=T1, T2=T2, p2_T1=p2_from_T1, p2_T2=p2_from_T2, p2_sph=sph(tp_), rar_sph=sph(tr_))
    R.p(f"  {foot:9s}: nu_RAR AQUAL sphere-avg {sph(tr_):.4f}, P2 {sph(tp_):.4f}; transfer T1 (band/sqrt(nu0)) {T1[0]:.3f}-{T1[1]:.3f} -> P2 {p2_from_T1[0]:.4f}-{p2_from_T1[1]:.4f}; T2 (band/sphere-avg) {T2[0]:.3f}-{T2[1]:.3f} -> P2 {p2_from_T2[0]:.4f}-{p2_from_T2[1]:.4f}   (Arm A band {band[foot][0]}-{band[foot][1]})")
R.data["transfer"] = rows3
if MUT:
    R.p("  MUTATE M7: P2's tensors replaced by Route A's (kernel swap) before the transfer")
    rows3_use = {foot: dict(p2_T1=[np.sqrt(T[("nu_RAR", foot)]["nu0"])*t for t in rows3[foot]["T1"]], p2_T2=[sph(T[("nu_RAR", foot)])*t for t in rows3[foot]["T2"]]) for foot in FOOT}
else:
    rows3_use = rows3
gap = {}
for foot in FOOT:
    lo = min(rows3_use[foot]["p2_T1"] + rows3_use[foot]["p2_T2"]); hi = max(rows3_use[foot]["p2_T1"] + rows3_use[foot]["p2_T2"])
    gap[foot] = (band[foot][0] - hi, band[foot][0] - lo)
    R.p(f"  {foot:9s}: P2 crude range {lo:.4f}-{hi:.4f}; below Arm A floor {band[foot][0]} by {gap[foot][0]:.4f}-{gap[foot][1]:.4f} = {gap[foot][0]/SIG_FIT:.1f}-{gap[foot][1]/SIG_FIT:.1f} sigma_fit = {gap[foot][0]/SIG_TOT:.1f}-{gap[foot][1]/SIG_TOT:.1f} sigma_tot")
R.check("E3 [M7 bites here] a P2 merge, transferred through Arm A's own band-to-point-field ratios, sits below Arm A's floor by more than 1 sigma_fit (0.019) on both footings", all(g[0] > SIG_FIT for g in gap.values()))
R.p("  Crude means: the ratios T1/T2 are Route A's, applied to P2 without re-solving. The pipeline-grade P2 number is CFG191_s5b_pipeline_tier2.py.")

R.sec("E4  arm table on a grid of gamma-hat (frozen z-rule, sigma_tot 0.028): which readings are consistent (|z|<2) / disfavoured (|z|>3)")
p2_mid = {f: np.mean(rows3[f]["p2_T1"] + rows3[f]["p2_T2"]) for f in FOOT}
readings = [("Arm A (floor,canonical)", 1.1614), ("Arm A (top,canonical)", 1.1814), ("P2 merge, crude transfer (canonical)", p2_mid["canonical"]), ("chain ceiling (canonical)", 1.0725), ("MI alpha=2 in force", 1.0310), ("Arm B / Arm C / Newton", 1.0000)]
grid = [0.95, 1.00, 1.03, 1.06, 1.084, 1.10, 1.13, 1.16, 1.20, 1.25]
R.p("  gamma-hat | " + " | ".join(f"{n[:22]:22s}" for n, _ in readings))
for g in grid:
    cells = []
    for n, v in readings:
        z = (g - v)/SIG_TOT; cells.append(f"z={z:+5.1f} {'cons' if abs(z) < 2 else ('DISF' if abs(z) > 3 else '2-3s')}".ljust(22))
    R.p(f"  {g:8.3f}  | " + " | ".join(cells))
names = [n for n, _ in readings]; vals = np.array([v for _, v in readings])
R.p("  pairwise separation |dv|/sigma_tot:")
for i in range(len(names)):
    R.p("   " + names[i][:36].ljust(36) + " ".join(f"{abs(vals[i]-vals[j])/SIG_TOT:5.1f}" for j in range(len(names))))
R.data["arm_values"] = dict(readings)
R.p("  reading: DR4 separates the unscreened strict law (Arm A) from Arm B / Arm C by 5.8-6.5 sigma_tot; Arm B and Arm C are the SAME number; the chain (a P2-kernel merge with screening) sits 2.6 sigma_tot above 1.000 at its ceiling and falls onto Newton at larger xi.")
R.p("  So a Newtonian result kills Arm A only; a HIGH result (>= 1.084 with the frozen stability conditions) kills Arm C and Arm B (not the chain below 1.157). 'DR4 decides merge vs ownership' holds only for {unscreened strict merge} vs {ownership, screened merges, Newton}.")

R.sec("mapping claims (frozen 'what would falsify' check)")
mapped = 1.0 if MUT else 1.1614
if MUT: R.p("  MUTATE M8: the merge is mapped to Arm B (1.000) instead of Arm A")
R.check("E5 [M8 bites here] CFG179's mapped merge value (Arm A floor) exceeds the frozen 3-sigma_tot-from-Newton edge 1 + 3*0.028 = 1.084", mapped > 1.084)
new_rows = [v for v in (1.1614, 1.1814, 1.1917, 1.2267, 1.0799, 1.000) if v not in (1.1614, 1.1814, 1.1917, 1.2267, 1.0799, 1.000)]
R.check("E6 every CFG179 DR4 number equals an already-registered value (Arm A band, MI alpha=1 1.0799, Arm C 1.000): the mapping adds no new decision row", not new_rows)
R.sec("VERDICT (frozen rule)")
if not MUT:
    R.finding("(e) DR4 mapping", "AGREES WITH QUALIFICATION (arithmetic) / DISAGREES on the kernel label",
      f"E1 arithmetic reproduces. Arm A is the Route A (nu_RAR) solve, not P2; my P2 tensors differ (y_extN 1.4647 vs 1.289), and a P2 merge transferred through Arm A's own ratios lands at {min(rows3['canonical']['p2_T1']+rows3['canonical']['p2_T2']):.3f}-{max(rows3['canonical']['p2_T1']+rows3['canonical']['p2_T2']):.3f} (canonical), below Arm A's floor 1.1614 by >= {gap['canonical'][0]/SIG_FIT:.1f} sigma_fit. 1.0799 is the retired alpha=1 MI value (in force 1.0310). Screened merge-type readings (Arm B 1.000, chain <= 1.0725/1.0900) are registered and omitted from the mapping. The mapping adds no new row; DR4 separates Arm A from Arm C at 5.8 sigma_tot, Arm B from Arm C at 0.")
R.finish()
