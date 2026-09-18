#!/usr/bin/env python3
"""SW05 -- the L268 quadrature action: (i) its X_loc AS WRITTEN carries the full AQUAL cross term (the script's B1 defined
x^2 + eta^2 by hand); (ii) the one-substitution repair X_loc = h^{mn} d_m(phi - phibar) d_n(phi - phibar); (iii) the repaired
action is direction-blind to O((r/l)^2) at r_M, is scalar-OFF at Saturn, and is therefore NOT reached by SW04's alpha1
theorem: for THIS structure the l-window is OPEN (SW04's 'no window' was a theorem about the smoothed-total-switch structure
of SW02/SW03, not about the quadrature).  Both a0 footings, both kernels, sympy where exact.  MUTATE=1 removes the
subtraction (the action as written): 1c/1d/2c must then FAIL.  A FAIL is a finding; no literal-True checks."""
import os, json, math
import sympy as sp
from scipy.optimize import brentq
MUT = os.environ.get("MUTATE", "0") == "1"
CH, OUT = [], {"mutate": MUT}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("SW05 -- the quadrature action (L268), as written and repaired; the l-window for THIS structure" + ("   [MUTATE: no subtraction]" if MUT else "") + "\n")

# ------------------------------------------------------------------ 1. exact flat-space smoothing of a point mass in a uniform field
print("=" * 100); print("1. Yukawa smoothing phibar = (1 - l^2 lap)^{-1} phi for phi = -GM/r - g_ext z; the two X's, exactly"); print("=" * 100)
r, th, ell, GM, gext, a0 = sp.symbols('r theta ell GM g_ext a0', positive=True)
lap_rad = lambda f: sp.diff(r ** 2 * sp.diff(f, r), r) / r ** 2 + sp.diff(sp.sin(th) * sp.diff(f, th), th) / (r ** 2 * sp.sin(th))   # spherical Laplacian (r > 0)
phi_own = -GM / r
phib_own = -(GM / r) * (1 - sp.exp(-r / ell))                                          # the regular smoothed 1/r
check("1a (1 - l^2 lap) phibar_own = phi_own for r > 0 (the delta functions at the origin cancel: phibar_own -> -GM/l, finite) and a linear phi_ext = -g_ext z is its own smoothing (lap z = 0)",
      sp.simplify(phib_own - ell ** 2 * lap_rad(phib_own) - phi_own) == 0 and sp.limit(phib_own, r, 0) == -GM / ell and sp.simplify(lap_rad(r * sp.cos(th))) == 0)
s = r / ell
g_own = GM / r ** 2
# unit vectors: r_hat, theta_hat; z_hat = cos(th) r_hat - sin(th) theta_hat.  All gradients live in the (r_hat, theta_hat) plane.
def vec(rad, tan): return sp.Matrix([rad, tan])
grad_own = vec(g_own, 0)                                                                # grad(phi_own) = +GM/r^2 r_hat
grad_ext = vec(-gext * sp.cos(th), gext * sp.sin(th))                                   # grad(-g_ext z) = -g_ext z_hat
grad_hp = vec(sp.diff(phi_own - phib_own, r), 0)                                        # grad of the HIGH-pass own part  phi_own e^{-r/l}
grad_lp = vec(sp.diff(phib_own, r), 0) + grad_ext                                       # grad of the LOW-pass part phibar (own smoothed + ext)
X_vec = (grad_own + grad_ext).dot(grad_own + grad_ext) / a0 ** 2                        # local AQUAL: |g_own + g_ext|^2
X_written = X_vec + grad_lp.dot(grad_lp) / a0 ** 2                                       # L268 as written: X_loc = |grad phi|^2 (TOTAL) + X_env
X_rep = (grad_hp.dot(grad_hp) + grad_lp.dot(grad_lp)) / a0 ** 2                          # repaired: X_loc = |grad(phi - phibar)|^2 + X_env
X_use = X_written if MUT else X_rep
x, eta = sp.symbols('x eta', positive=True)
sub = {GM: x * a0 * r ** 2, gext: eta * a0}                                             # x = g_own/a0 at this r, eta = g_ext/a0
f_s = 1 - sp.exp(-s) * (1 + s)
crossof = lambda X: sp.simplify((X - X.subs(th, sp.pi / 2)).subs(sub))                  # the theta-dependent part of X (cos(theta) = 0 at pi/2)
cross_vec = crossof(X_vec)                                                              # AQUAL's cross term: -2 x eta cos(theta) in this sign convention (grad phi, not g)
check("1b L268 AS WRITTEN: X_loc = h^{mn} d_m phi d_n phi is the TOTAL local gradient, so X_loc + X_env carries AQUAL's cross term PLUS the smoothed-own x external one: cross = (1 + f(r/l)) x AQUAL's, >= AQUAL's at every l -- the action as written is NOT direction-blind (its B1 check assigned x^2 + eta^2 by hand)",
      sp.simplify(crossof(X_written) - cross_vec * (1 + f_s)) == 0 and sp.simplify(cross_vec + 2 * x * eta * sp.cos(th)) == 0,
      f"cross_written / cross_AQUAL = {sp.simplify(crossof(X_written) / cross_vec)}")
# first-order size of the written action's anisotropy at the r_M shell relative to AQUAL's, with L268's own deep-MOND F: mu = sqrt(X)
xs, es = 1.0, 2.23
ratio_written = (1 / (2 * math.sqrt(xs ** 2 + 2 * es ** 2))) / (1 / (2 * math.sqrt(xs ** 2 + es ** 2)))   # d mu/d(cross) = mu'(X) = 1/(2 sqrt X), cross terms equal for l >> r_M
check("1b2 the written action's quadrupole is AQUAL's times mu'(x^2 + 2 eta^2)/mu'(x^2 + eta^2) ~ 0.7 at the r_M shell (l >> r_M, mu = sqrt X, first order in the cross term): 6.44 x 0.7 ~ 4.8 x the Cassini ceiling -- still dead",
      0.5 < ratio_written < 0.9 and 6.44 * ratio_written > 1, f"ratio = {ratio_written:.2f}; written-action quadrupole ~ {6.44*ratio_written:.1f} x ceiling (mu_2, canonical)")
cross_rep = crossof(X_use)
check("1c REPAIRED (X_loc = |grad(phi - phibar)|^2): the cross term is AQUAL's times f(r/l), f(s) = 1 - e^{-s}(1 + s) = s^2/2 - s^3/3 + ... EXACTLY (sympy); the subtraction removes the own-external cross term to O((r/l)^2)",
      sp.simplify(cross_rep - cross_vec * f_s) == 0 and sp.simplify(sp.series(f_s, r, 0, 4).removeO() - (r ** 2 / (2 * ell ** 2) - r ** 3 / (3 * ell ** 3))) == 0,
      f"cross / cross_AQUAL = {sp.simplify(cross_rep / cross_vec)}")
lim0 = sp.simplify(sp.limit(X_use.subs(sub), ell, sp.oo)); liminf = sp.simplify(sp.limit(X_use.subs(sub), ell, 0))
check("1d the repaired action interpolates: l >> r gives X -> x^2 + eta^2 (SW01's direction-blind rule, the framework's cap law); l << r gives X -> |g_own + g_ext|^2/a0^2 (AQUAL's vector rule): the EFE is direction-blind INSIDE l and directional OUTSIDE it",
      sp.simplify(lim0 - (x ** 2 + eta ** 2)) == 0 and sp.simplify(liminf - X_vec.subs(sub)) == 0, f"l->inf: {lim0};  l->0: {liminf}")
fnum = lambda sv: 1 - math.exp(-sv) * (1 + sv)

# ------------------------------------------------------------------ 2. the l-window for the quadrature structure
print("\n" + "=" * 100); print("2. the l-window: the Cassini quadrupole (needs l >> r_M) against the Sun's Galactic eta through X_env (needs l << R_0)"); print("=" * 100)
G, MSUN, PC, KPC, AU, KMS = 6.674e-11, 1.989e30, 3.0857e16, 3.0857e19, 1.496e11, 1e3
R0 = 8.2 * KPC; g_gal = (230 * KMS) ** 2 / R0
Q_OVER = {("canonical", "mu_2"): 6.44, ("canonical", "nu_RAR"): 6.23, ("alt", "mu_2"): 7.63, ("alt", "nu_RAR"): 7.63 / 1.12}   # L243 exact-AQUAL / Park 2026 ceiling
FOOT = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
win = {}
for foot, a0n in FOOT.items():
    rM = math.sqrt(G * MSUN / a0n)
    for kn in ("mu_2", "nu_RAR"):
        need = 1.0 / Q_OVER[(foot, kn)]                       # the anisotropy at the r_M shell must drop below 1/(L243 overshoot)
        if MUT:
            l_min = float("inf")                              # the written action has f = 1 at every l: no l passes
        else:
            l_min = rM / brentq(lambda sv: fnum(sv) - need, 1e-6, 50.0)            # f(r_M/l) < need  <=>  l > r_M/s*
            l_min3 = 3 * rM / brentq(lambda sv: fnum(sv) - need, 1e-6, 50.0)       # conservative: the shell out to 3 r_M
        l_max = R0 / brentq(lambda sv: fnum(sv) - 0.9, 1e-6, 50.0)                 # the Sun keeps >= 90% of the Galactic field in X_env (point-source proxy at R_0)
        win[(foot, kn)] = dict(rM_pc=rM / PC, l_min_pc=l_min / PC, l_min3_pc=(l_min3 / PC if not MUT else float("inf")), l_max_pc=l_max / PC, need=need)
        print(f"    {foot:9s} {kn:6s}: r_M = {rM/PC:.4f} pc; quadrupole needs f(r_M/l) < {need:.3f} -> l > {l_min/PC:.3g} pc (shell to 3 r_M: l > {win[(foot,kn)]['l_min3_pc']:.3g} pc); "
              f"Galactic eta needs f(R_0/l) > 0.9 -> l < {l_max/PC:.3g} pc = {l_max/KPC:.2f} kpc")
OUT["window"] = {f"{k[0]}/{k[1]}": v for k, v in win.items()}
check("2a the quadrupole condition: for the REPAIRED action the L243 overshoot (6.2-7.6x) is beaten by f(r_M/l) < 1/overshoot at a finite l_min of order a few r_M on every footing and kernel",
      all(math.isfinite(v["l_min_pc"]) and v["l_min_pc"] < 10 * v["rM_pc"] for v in win.values()), f"l_min = {[round(v['l_min_pc'],3) for v in win.values()]} pc (r_M = 0.035-0.039 pc); MUTATE: no l passes")
check("2b the eta condition: the Sun still reads >= 90% of the Galactic field through X_env for l below ~2 kpc (point-source proxy at R_0 = 8.2 kpc; an extended disc is milder)",
      all(1.0 * KPC < v["l_max_pc"] * PC < 5.0 * KPC for v in win.values()), f"l_max = {win[('canonical','mu_2')]['l_max_pc']/1e3:.2f} kpc")
ratio = min(v["l_max_pc"] / v["l_min3_pc"] for v in win.values()) if not MUT else 0.0
check("2c THE WINDOW IS OPEN for the quadrature structure: l_max/l_min(conservative) > 1 on every footing and kernel -- unlike SW03's smoothed-total-switch, where SW04 found none (PPN l <= 0.001 pc vs quadrupole l >= 0.1 pc)",
      ratio > 1, f"min l_max/l_min3 = {ratio:.3g} (about four orders of magnitude: l in [~0.2 pc, ~2 kpc]); MUTATE: closed")
OUT["window_ratio_min"] = ratio

# ------------------------------------------------------------------ 3. SW04's alpha1 theorem on the repaired action
print("\n" + "=" * 100); print("3. SW04's theorem alpha1~ = -8(nu - 1)/nu at Saturn: the argument is the LOCAL x here, the Galactic eta there"); print("=" * 100)
nu_rar = lambda y: 1.0 / (1.0 - math.exp(-math.sqrt(y))) if y < 1e4 else 1.0 + math.exp(-math.sqrt(y))
mu2 = lambda u: 1.0 - (1.0 + u) ** -2
def nu_mu2(y):
    if y > 1e3: return 1.0 + 4.0 / y ** 2            # 1 - mu_2 ~ 4/x^2 (L243)
    return brentq(lambda g: g * mu2(g / 2.0) - y, y, 50 * y + 50) / y
KERN = {"nu_RAR": nu_rar, "mu_2": nu_mu2}
r_sat = 9.5 * AU; a1 = {}
for foot, a0n in FOOT.items():
    x_sat = G * MSUN / r_sat ** 2 / a0n; eta_g = g_gal / a0n
    for kn, nuf in KERN.items():
        arg_rep = math.sqrt(x_sat ** 2 + eta_g ** 2) if not MUT else math.sqrt(x_sat ** 2 + 2 * eta_g ** 2 + 2 * x_sat * eta_g)   # written: adds the cross term (theta = 0 worst case)
        nu_rep = nuf(arg_rep); nu_sw03 = nuf(eta_g)          # SW03: the smoothed switch reads eta only
        a1_rep = -8 * (nu_rep - 1) / nu_rep; a1_sw03 = -8 * (nu_sw03 - 1) / nu_sw03
        a1[(foot, kn)] = dict(x_sat=x_sat, eta=eta_g, nu_minus1_rep=nu_rep - 1, alpha1_rep=a1_rep, alpha1_sw03=a1_sw03)
        print(f"    {foot:9s} {kn:6s}: x_Saturn = {x_sat:.2e}, eta_gal = {eta_g:.2f}; quadrature: nu - 1 = {nu_rep-1:.1e} -> alpha1~ = {a1_rep:+.1e};   SW03's smoothed switch: nu(eta) - 1 = {nu_sw03-1:.3f} -> alpha1~ = {a1_sw03:+.3f}")
OUT["alpha1"] = {f"{k[0]}/{k[1]}": v for k, v in a1.items()}
check("3a the repaired quadrature action passes SW04's alpha1 gate: |alpha1~| = 8(nu(sqrt(x_Sat^2 + eta^2)) - 1)/nu < 1e-4 on both footings and kernels, because the LOCAL x_Saturn ~ 7e5 sits unsmoothed in the argument and switches the scalar off (mu_2: 4/x^2 ~ 1e-11; nu_RAR: e^{-sqrt x})",
      all(abs(v["alpha1_rep"]) < 1e-4 for v in a1.values()), f"max |alpha1~| = {max(abs(v['alpha1_rep']) for v in a1.values()):.1e} (bound 1e-4); the khronon's own alpha1, alpha2 remain, tunable to 0 on the Blas-Sibiryakov family (L270 P3)")
check("3b the same formula with SW03's argument (the smoothed switch reads eta_gal only) reproduces SW04's kill, |alpha1~| >= 1.4: the entire difference between the two structures is the unsmoothed local magnitude in the argument",
      all(abs(v["alpha1_sw03"]) >= 1.4 for v in a1.values()), f"SW03 values: {[round(v['alpha1_sw03'], 2) for v in a1.values()]}")

# ------------------------------------------------------------------ 4. what the repaired action predicts at each scale
print("\n" + "=" * 100); print("4. direction-blind below l, AQUAL above it: f(R/l) for the systems on the record"); print("=" * 100)
systems = {"wide binary (10 kAU)": 0.05 * PC, "globular cluster": 10 * PC, "classical dSph": 0.5 * KPC, "SPARC disc": 10 * KPC}
ells = {"l = 0.2 pc": 0.2 * PC, "l = 10 pc": 10 * PC, "l = 1 kpc": KPC, "l = 2 kpc": 2 * KPC}
print(f"    {'system':22s}" + "".join(f"{k:>12s}" for k in ells))
tab = {}
for sn, R in systems.items():
    tab[sn] = {ln: fnum(R / L) for ln, L in ells.items()}
    print(f"    {sn:22s}" + "".join(f"{tab[sn][ln]:12.3f}" for ln in ells))
OUT["f_table"] = tab
l_max_min = min(v["l_max_pc"] for v in win.values()) * PC
check("4a at every l in the window (l <= l_max ~ 2 kpc) a SPARC-scale disc (R ~ 10 kpc) has f > 0.9: its external-field effect is AQUAL's DIRECTIONAL one, so the GAME_PLAN's DE05 fingerprint ('direction-NO for galaxies') is NOT this action's prediction; the direction-blind regime is sub-l (wide binaries, the Oort cloud, star clusters)",
      fnum(10 * KPC / l_max_min) > 0.9, f"f(10 kpc / l_max) = {fnum(10 * KPC / l_max_min):.3f}")
l_min_max = max(v["l_min3_pc"] for v in win.values()) * PC if not MUT else float("inf")
check("4b at every l in the window a wide binary (0.05 pc) is direction-blind (f < 1/6.2), so SW01's gamma_v = 1.09-1.15 (below the AQUAL band 1.16-1.23) stays the DR4 prediction of this structure",
      (not MUT) and fnum(0.05 * PC / l_min_max) < 1 / 6.2, f"f(0.05 pc / l_min) = {fnum(0.05 * PC / l_min_max) if not MUT else 1.0:.3f}")

n, n_pass = len(CH), sum(CH)
print(f"\nSW05 COMPLETE: {n_pass}/{n} checks PASS." + ("  [MUTATE: the written action -- 1c/1d/2a/2c/4b are expected to FAIL]" if MUT else ""))
print("""VERDICT.  (1) L268's action AS WRITTEN is not direction-blind: X_loc is the total local gradient and carries the full AQUAL
cross term (its B1 check defined x^2 + eta^2 by hand).  (2) The one-substitution repair X_loc = |grad(phi - phibar)|^2 makes it
direction-blind to f(r/l) = 1 - e^{-r/l}(1 + r/l) ~ (r/l)^2/2 inside l and AQUAL outside l.  (3) SW04's alpha1 theorem does NOT
reach the repaired action: the unsmoothed local x_Saturn ~ 7e5 switches the scalar off (|alpha1~| ~ 1e-11), whereas SW03's
smoothed switch read eta_gal and gave |alpha1~| = 1.4-2.1.  The l-window for THIS structure is OPEN: l in [~0.2 pc, ~2 kpc].
SW04's 'no window' is a theorem about the smoothed-total-switch structure only; the FINDINGS/memory sentence 'the isotropic-EFE
+ preferred-frame-lensing class is dead' was too broad and is corrected to 'the smoothed-total-switch realisation is dead'.
(4) The price of the open window: the repaired action is AQUAL at galaxy scale (directional EFE for discs and most dSphs), so
DE05 cannot be its fingerprint; its fingerprints are sub-l: DR4 gamma_v below the AQUAL band and NO field-aligned Oort/comet
anisotropy inside l.  OPEN GATES, named not computed: the matter-phi coupling (with matter on g only phi has no source; the
disformal coupling through the khronon's u gives lensing = dynamics and, with the scalar off locally, leaves alpha1 to the
khronon); the FRW background (X = 0 there: the TeVeS strong-coupling problem, no Theta-term in L268 -- SW03's is the available
fix); the scalar has no time-kinetic term (X is purely spatial): an instantaneous constraint field in a preferred foliation, the
record's req-9 uniform-ellipticity question; ghost-freedom of khronon + phi on the alpha1 = alpha2 = 0 family (L270 P4); the
cluster residual (unaddressed).  Nothing here derives kappa.""")
json.dump(dict(pass_=n_pass, n=n, **OUT), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "SW05_results_MUTATE.json" if MUT else "SW05_results.json"), "w"), indent=1, default=str)   # the control run must never overwrite the main results
