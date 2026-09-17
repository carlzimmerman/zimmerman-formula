#!/usr/bin/env python3
"""SW02 -- THE MESOSCOPIC SWITCH: the a0 response switched by the Yukawa-smoothed gravitational field energy density.

The equations (Newtonian limit):
        (1 - l^2 nabla^2) psi = |grad Phi|^2 / (8 pi G),        div[ mu( sqrt(psi/u0) ) grad Phi ] = 4 pi G rho,      u0 = a0^2/(8 pi G).
psi is the field energy density averaged over the length l with the Yukawa kernel e^{-s/l}/(4 pi l^2 s).  For a system smaller than l
the cross term g_own . g_ext averages to zero, so the external field caps the response only through its magnitude (SW01's rule, now
from an equation); for a system much larger than l, psi = u and the theory is ordinary MOND.  L264 requires a magnitude response;
L243 forbids the vector-sum anisotropy; this is the construction that satisfies both, and it introduces ONE length, l.

Computed here, with the kills fixed first:
  A  the solar neighbourhood: psi = u_gal (the Sun's own field is averaged away for l >> r_M(Sun) = 0.03 pc), so mu is a CONSTANT
     mu(eta) across the solar system: exact Newton with G_eff = G/mu(eta), no phantom, no quadrupole.  The leading residual is the
     GRADIENT of |g_gal| across the solar system (l-independent): a dipolar modulation of G_eff, delta = (d ln mu/d ln psi) x 2 x
     (r/R0) -- estimated against Saturn's anomalous-precession bound (order 0.1-1 mas/yr).  Gate: below 1 mas/yr.
  B  the l-window: for l in {3, 10, 30, 100, 300} pc the predicted dispersion boost 1/mu(r_h) for the Sun/wide binaries, Pal 14,
     NGC 2419, Segue 1, Draco, Fornax and an isolated 1e9 M_sun dwarf, each with its own Plummer field and its Galactic g_ext,
     versus standard isotropic-EFE MOND (no smoothing).  Gate: an l exists with boost < 1.3 for BOTH outer-halo globular clusters
     (observed Newtonian: Jordi+09, Ibata+11) AND boost > 2 for BOTH classical dwarfs (observed dark-matter-dominated).
  C  the cost at that l: the ultra-faint dwarf (Segue 1, r_h ~ 30 pc, sigma_obs = 3.7 km/s) -- if its boost is < 1.5 the theory
     needs UFDs out of equilibrium; recorded as the kill it would die by.  Wide binaries: gamma_v = 1.00 (G_eff renormalises the
     laboratory G identically).  Galaxies: psi = u to O((l/h)^2), the RAR unchanged.
Kernel: mu_2(x) = 1 - (1 + x/2)^-2 and nu_RAR; both a0 footings.  No literal-True checks; a FAIL is a finding."""
import os, json, math
import numpy as np
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
G, MSUN, PC, AU, KMS, KPC = 6.674e-11, 1.989e30, 3.0857e16, 1.496e11, 1e3, 3.0857e19
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
R0, VC = 8.2 * KPC, 230 * KMS
mu2 = lambda x: 1.0 - (1.0 + x / 2.0) ** -2
def mu_rar(x):                                    # mu from nu_RAR by inversion of g = nu(g_N/a0) g_N: mu = g_N/g at g = x a0
    from scipy.optimize import brentq
    nu = lambda y: 1.0 / (1.0 - math.exp(-math.sqrt(y)))
    y = brentq(lambda yy: nu(yy) * yy - x, 1e-12, x) if x > 1e-9 else 0.0
    return y / x if x > 0 else 0.0
KERN = {"mu_2": mu2, "mu_RAR": mu_rar}
print("SW02 -- the mesoscopic switch\n")

# ------------------------------------------------------------------ A. the solar neighbourhood
print("=" * 100); print("A. the solar neighbourhood: constant mu(eta), exact Newton with G_eff, and the l-independent gradient residual"); print("=" * 100)
g_gal = VC ** 2 / R0
for foot, a0 in A0.items():
    eta = g_gal / a0
    for kn, mu in KERN.items():
        m0 = mu(eta); dlnmu = (math.log(mu(eta * 1.01)) - math.log(mu(eta * 0.99))) / (math.log(1.01) - math.log(0.99))   # d ln mu / d ln x
        dlnmu_psi = 0.5 * dlnmu                                                                                          # x = sqrt(psi/u0)
        r_sat = 9.5 * AU
        delta = dlnmu_psi * 2 * (2 * r_sat / R0)                                                                          # |g_gal| ~ 1/R: d ln u/d ln R = -2; across 2 r_sat
        # a dipolar G_eff modulation delta produces an anomalous precession of order delta per orbit (order-of-magnitude)
        prec_mas_yr = delta / (29.5) * 206265e3
        print(f"    {foot:9s} {kn:6s}: eta = {eta:.2f}, mu(eta) = {m0:.3f} -> G_eff = {1/m0:.3f} G (uniform: renormalises the laboratory G, unobservable);"
              f" gradient residual delta = {delta:.1e} -> precession ~ {prec_mas_yr:.2f} mas/yr (bound order 0.1-1)")
        OUT.setdefault("A", {})[f"{foot}/{kn}"] = dict(eta=eta, mu=m0, G_eff=1 / m0, delta=delta, prec_mas_yr=prec_mas_yr)
check("A1 the l-independent gradient residual is below Saturn's anomalous-precession bound taken at 1 mas/yr (both footings, both kernels)",
      all(v["prec_mas_yr"] < 1.0 for v in OUT["A"].values()), f"max {max(v['prec_mas_yr'] for v in OUT['A'].values()):.2f} mas/yr; a quadrupole is absent by construction (constant mu)")

# ------------------------------------------------------------------ B. the l-window
print("\n" + "=" * 100); print("B. the l-window: dispersion boost 1/mu at r_h under the smoothed switch versus standard isotropic-EFE MOND"); print("=" * 100)
from scipy.integrate import quad
def yukawa_at(r, ufun, ell, rmin, rmax):
    """psi(r) = int r'^2 dr' u(r') [e^{-|r-r'|/l} - e^{-(r+r')/l}]/(2 l r r')  (angular average of the Yukawa kernel), exact quadrature in ln r'"""
    f = lambda lr: (lambda rp: ufun(rp) * (math.exp(-abs(r - rp) / ell) - math.exp(-(r + rp) / ell)) / (2 * ell * r * rp) * rp ** 3)(math.exp(lr))
    pts = sorted(set(math.log(x) for x in (r, r + ell, max(r - ell, rmin * 1.01), r + 5 * ell, max(r - 5 * ell, rmin * 1.01)) if rmin < x < rmax))
    val, _ = quad(f, math.log(rmin), math.log(rmax), points=pts, limit=800)
    return val
SYS = {  # name: (mass M_sun, Plummer b = r_h/1.3 [pc], Galactocentric R [kpc] or None, observed reading)
    "wide binary 1 M_sun":    (1.0, 0.05 / 1.3, 8.2, "Newtonian (registered band 1.16-1.23 assumes AQUAL EFE)"),
    "Pal 14":                 (1.2e4, 27 / 1.3, 71, "Newtonian, sigma = 0.38 +- 0.12 (Jordi+09)"),
    "NGC 2419":               (9e5, 20 / 1.3, 90, "Newtonian, MOND disfavoured (Ibata+11)"),
    "Segue 1 (UFD)":          (3e3, 30 / 1.3, 28, "sigma = 3.7 km/s: dark-dominated if in equilibrium"),
    "Draco":                  (3e5, 200 / 1.3, 76, "dark-dominated"),
    "Fornax":                 (2e7, 700 / 1.3, 147, "dark-dominated"),
    "isolated dwarf 1e9":     (1e9, 1500 / 1.3, None, "on the RAR"),
}
ELLS = (3.0, 10.0, 30.0, 100.0, 300.0)
a0 = A0["canonical"]; u0 = a0 ** 2 / (8 * math.pi * G)
print(f"    {'system':22s} {'x_h':>7s} {'eta':>6s} {'EFE-MOND':>9s} " + " ".join(f"l={e:>3.0f}pc" for e in ELLS) + "   observed")
table = {}
for name, (M, b_pc, Rk, obs) in SYS.items():
    b = b_pc * PC; rh = 1.3 * b
    gext = VC ** 2 / (Rk * KPC) if Rk else 0.0; eta = gext / a0
    ufun = lambda rp: (G * M * MSUN * rp / (rp ** 2 + b ** 2) ** 1.5) ** 2 / (8 * math.pi * G)
    rmin, rmax = b * 1e-4, b * 1e5
    xh = (G * M * MSUN * rh / (rh ** 2 + b ** 2) ** 1.5) / a0
    efe = 1.0 / mu2(math.sqrt(xh ** 2 + eta ** 2))
    row = dict(x_h=xh, eta=eta, efe_mond=efe, boosts={})
    for ell in ELLS:
        psi = yukawa_at(rh, ufun, ell * PC, rmin, rmax) + gext ** 2 / (8 * math.pi * G)
        xeff = math.sqrt(psi / u0)
        row["boosts"][ell] = 1.0 / mu2(xeff)
    table[name] = row
    print(f"    {name:22s} {xh:7.3f} {eta:6.2f} {efe:9.2f} " + " ".join(f"{row['boosts'][e]:7.2f} " for e in ELLS) + f"   {obs}")
OUT["B"] = {k: dict(x_h=v["x_h"], eta=v["eta"], efe_mond=v["efe_mond"], boosts={str(e): b_ for e, b_ in v["boosts"].items()}) for k, v in table.items()}
good = [e for e in ELLS if table["Pal 14"]["boosts"][e] < 1.3 and table["NGC 2419"]["boosts"][e] < 1.3 and table["Draco"]["boosts"][e] > 2.0 and table["Fornax"]["boosts"][e] > 2.0]
check("B1 an l exists with boost < 1.3 for both outer-halo globular clusters AND boost > 2 for both classical dwarfs", len(good) > 0,
      f"viable l: {good} pc" if good else "none: no single smoothing length makes Pal 14 / NGC 2419 Newtonian while keeping Draco / Fornax dark-dominated")
check("B2 standard isotropic-EFE MOND (no smoothing) predicts a boost > 1.3 for at least one of the two Newtonian globular clusters (the anomaly the switch is asked to remove)",
      table["Pal 14"]["efe_mond"] > 1.3 or table["NGC 2419"]["efe_mond"] > 1.3, f"Pal 14 {table['Pal 14']['efe_mond']:.2f}, NGC 2419 {table['NGC 2419']['efe_mond']:.2f}")
check("B3 the isolated dwarf galaxy keeps its RAR boost at every l (boost within 5% of the unsmoothed value)",
      all(abs(table["isolated dwarf 1e9"]["boosts"][e] / table["isolated dwarf 1e9"]["efe_mond"] - 1) < 0.05 for e in ELLS))
check("B4 wide binaries are Newtonian at every l (boost within 1% of the constant-mu(eta) value, i.e. gamma_v = 1.00 after G renormalisation)",
      all(abs(table["wide binary 1 M_sun"]["boosts"][e] * mu2(table["wide binary 1 M_sun"]["eta"]) - 1) < 0.01 for e in ELLS))

# ------------------------------------------------------------------ C. the cost
print("\n" + "=" * 100); print("C. the cost at the viable l: the ultra-faint dwarf"); print("=" * 100)
if good:
    for e in good:
        bseg = table["Segue 1 (UFD)"]["boosts"][e]
        print(f"    l = {e:.0f} pc: Segue 1 boost = {bseg:.2f} (EFE-MOND {table['Segue 1 (UFD)']['efe_mond']:.2f}); Newtonian sigma ~ sqrt(G M/(3 r_h)) = {math.sqrt(G*3e3*MSUN/(3*30*PC))/KMS:.2f} km/s vs observed 3.7")
    check("C1 at the viable l the ultra-faint dwarf keeps a boost > 1.5 (else UFDs must be out of equilibrium: the kill the theory would die by)",
          any(table["Segue 1 (UFD)"]["boosts"][e] > 1.5 for e in good), "the smoothing that makes globular clusters Newtonian makes Segue 1 Newtonian too. [FAIL is the finding: the kill is named]")
else:
    check("C1 (not evaluated: no viable l)", False, "B1 failed")
n, n_pass = len(CH), sum(CH)
print(f"\nSW02 COMPLETE: {n_pass}/{n} checks PASS.")
json.dump(dict(pass_=n_pass, n=n, parts=OUT), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "SW02_results.json"), "w"), indent=1, default=str)
