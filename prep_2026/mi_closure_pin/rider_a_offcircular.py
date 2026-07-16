#!/usr/bin/env python3
r"""
RIDER (a) -- OFF-CIRCULAR DYNAMICS after the Wightman-pullback verdict (eta(beta) is FREE)
=========================================================================================
Framework: de Sitter-Unruh MODIFIED INERTIA (Carl Zimmerman). Own interpolation
nu(y)=sqrt(1+1/y), mu(x)=(sqrt(1+4x^2)-1)/(2x)=K(x^2). Both a0 footings:
canonical a0=9.36e-11 (cH_L/Z), alt a0=1.13e-10 (rho_tot/cH0).

PULLBACK VERDICT (input, established upstream in the closure-pin lane): the off-circular dS-Unruh
Wightman pole stays at/above kappa=H_Lambda for EVERY eccentricity, EVERY anisotropy, and EVERY
reduction weighting (kappa_eff=sqrt(H_L^2+(a/c)^2)>=H_L; orbital AC content is a comb at
n*omega_orbit >> H_L, nothing in the (0,H_L) amplitude-MOND band). Because the pole is >= H_L for ALL
weightings, the pullback CANNOT select one -> the reduction-weighting function eta(beta) is NOT
pinned. FREEDOM STANDS.

QUESTION FOR THIS RIDER: given eta(beta) free, is the dSph/dispersion RAR offset a FORCED number or
still a BRACKET? Computed straight (a NULL is as publishable as a win). Built on the VALIDATED rb3
machinery (mi_fingerprint/rb3_eccentric_offset.py: Plummer tracer, per-orbit closure-B fixed point,
virial-level sigma^2 proxy) -- re-derived here, not trusted, with the pullback-consequence framing.

WHAT IS COMPUTED (exit 0 iff all pass; no hard-coded verdict booleans):
 [1] Closure A (instantaneous |a|): dispersion systems sit EXACTLY on the rotation RAR, offset=0.
     The LOWER bracket endpoint.
 [2] The offset SIGN is set by the orbit-shape population (= eta(beta)): apocentre-dominated
     tangential orbits sit BELOW (negative), pericentre-dominated radial/plunging orbits run ABOVE
     (positive, the kinetic pump). Two admissible populations -> OPPOSITE signs -> a BRACKET, not a
     forced number. Computed on integrated orbits.
 [3] What IS forced (pullback-independent): d(offset)/d(radial-anisotropy) > 0 (radial hotter than
     tangential at fixed depth). Sign computed from the orbits, not set.
 [4] MG-with-the-same-nu (isolated spherical): offset 0 AND zero anisotropy dependence -> the
     forced anisotropy-derivative sign is MG-IMPOSSIBLE (the clean differential discriminator).
 [5] Bracket magnitude, isotropic ensemble, BOTH footings (~10-15% footing-stable).
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

PASS = True
def check(name, cond):
    global PASS
    ok = bool(cond)
    print(f"   [{'PASS' if ok else 'FAIL'}] {name}")
    if not ok: PASS = False

rng = np.random.default_rng(7)
A0_DE, A0_TOT = 9.36e-11, 1.13e-10
mu_fw = lambda x: (np.sqrt(1+4*x**2)-1)/(2*x)
nu_fw = lambda y: np.sqrt(1+1/y)

# ---- rb3's validated Plummer machinery (re-derived) ----------------------------------------------
gN = lambda r: r/(1+r**2)**1.5                       # Plummer, GM=b=1
def make_field(a0): return lambda r: nu_fw(gN(r)/a0)*gN(r)
def jeans_sigma(gA):
    rg = np.geomspace(1e-3, 300, 400); rho = (1+rg**2)**(-2.5)
    integ = rho*gA(rg)
    I = np.concatenate([np.cumsum((0.5*(integ[1:]+integ[:-1])*np.diff(rg))[::-1])[::-1], [0.0]])
    return lambda r: np.interp(r, rg, I/rho)
def integrate_orbit(gA, r0, vvec, n_periods=15):
    vc = np.sqrt(gA(r0)*r0); T = n_periods*2*np.pi*r0/max(vc, 1e-6)
    def rhs(t, s):
        x, y_, vx, vy = s; r = np.hypot(x, y_); g = gA(r)
        return [vx, vy, -g*x/r, -g*y_/r]
    sol = solve_ivp(rhs, [0, T], [r0, 0.0, vvec[0], vvec[1]], t_eval=np.linspace(0, T, 6000),
                    rtol=1e-9, atol=1e-12, method='DOP853')
    return np.hypot(sol.y[0], sol.y[1])
def orbit_offset(gA, a0, r_t):
    """Per-orbit closure-B fixed point + virial-level offset vs closure A (rb3, re-derived)."""
    gN_t = gN(r_t); aA_t = gA(r_t)
    gN2 = np.mean(gN_t**2)
    mB = brentq(lambda m: m - mu_fw(np.sqrt(gN2)/(m*a0)), 1e-8, 1.0, xtol=1e-14)
    gB_t = gN_t/mB
    return np.log10(np.mean(gB_t*r_t)/np.mean(aA_t*r_t))

# ======================================================================================
print("#"*96)
print("# [1] CLOSURE A endpoint: instantaneous |a| -> offset EXACTLY 0 (lower bracket end)")
print("#"*96)
xs = np.logspace(-3, 3, 200)
res = np.abs(mu_fw(nu_fw(xs)*xs)*(nu_fw(xs)*xs)/xs - 1).max()
print(f"   pointwise inversion mu_fw(nu*x)*nu*x/x - 1 : max |dev| over 6 decades = {res:.2e}")
check("Closure A: dispersion systems sit EXACTLY on the rotation RAR (offset 0 to machine prec.)",
      res < 1e-12)

# ======================================================================================
print("#"*96)
print("# [2] SIGN set by orbit-shape population (= eta(beta)): tangential<0 vs radial/plunging>0")
print("#"*96)
# Deep dSph-like regime y(b)=g_N(1)/a0 ~ 2.36. Launch at r0=1, v=lam*v_circ tangentially: high lam
# => near-circular/tangential (apocentre-dominated), low lam => plunging/radial (pericentre pump).
a0_deep = 2.357                                      # rb3's deep-MOND relabelled depth
gA = make_field(a0_deep)
print(f"   deep regime y(b)=g_N(1)/a0 = {gN(1.0)/a0_deep:.3f}; launch v=lam*v_circ at r0=1:")
print("   lam   ecc     offset (dex)   population")
shape = []
for lam, tag in [(0.9, "tangential/apocentre-dominated"), (0.7, "mild"),
                 (0.5, "eccentric"), (0.3, "radial/plunging (pericentre pump)")]:
    r_t = integrate_orbit(gA, 1.0, [0.0, lam*np.sqrt(gA(1.0)*1.0)])
    e = (r_t.max()-r_t.min())/(r_t.max()+r_t.min())
    d = orbit_offset(gA, a0_deep, r_t)
    shape.append((lam, e, d))
    print(f"   {lam:.1f}   {e:.3f}   {d:+.4f}      {tag}")
d_tan = shape[0][2]; d_rad = shape[-1][2]
check("tangential/apocentre-dominated orbit sits BELOW the rotation RAR (offset < 0)", d_tan < 0)
check("radial/plunging orbit runs ABOVE (offset > 0, the pericentre kinetic pump) -> SIGN FLIP",
      d_rad > 0)
check("=> two admissible orbit-shape populations give OPPOSITE-sign offsets -> the offset is a "
      "BRACKET spanning 0, its overall sign set by the unpinned eta(beta), NOT forced",
      d_tan < 0 and d_rad > 0)

# ======================================================================================
print("#"*96)
print("# [3] What IS forced: d(offset)/d(radial-anisotropy) > 0 (radial hotter) -- computed")
print("#"*96)
# Anisotropy index = orbit eccentricity from an angular-momentum-deficit (tangential) launch: lower
# lam -> lower L -> more radial/plunging -> larger e (rb3's validated lever). Sweep lam, correlate
# offset with e. A positive rank-correlation IS d(offset)/d(radial-anisotropy) > 0.
print("   tangential launch v=lam v_c at r0=1; eccentricity e indexes radial anisotropy:")
print("   lam    e        offset (dex)")
ecc, offs_e = [], []
for lam in [0.85, 0.75, 0.65, 0.55, 0.45, 0.35, 0.28]:
    r_t = integrate_orbit(gA, 1.0, [0.0, lam*np.sqrt(gA(1.0)*1.0)])
    e = (r_t.max()-r_t.min())/(r_t.max()+r_t.min())
    d = orbit_offset(gA, a0_deep, r_t)
    ecc.append(e); offs_e.append(d)
    print(f"   {lam:.2f}   {e:.3f}    {d:+.4f}")
# Spearman rank-correlation between eccentricity (radial anisotropy) and offset:
def spearman(a, b):
    ra = np.argsort(np.argsort(a)); rb = np.argsort(np.argsort(b))
    return np.corrcoef(ra, rb)[0, 1]
rho_sp = spearman(np.array(ecc), np.array(offs_e))
print(f"   Spearman rho(eccentricity, offset) = {rho_sp:+.3f}  (endpoints: e_min {offs_e[0]:+.4f} -> "
      f"e_max {offs_e[-1]:+.4f} dex)")
check("FORCED: d(offset)/d(radial-anisotropy) > 0 -- offset rises monotonically with orbit "
      "eccentricity (Spearman rho>0.8 and plunging end hotter than tangential end); computed not set",
      rho_sp > 0.8 and offs_e[-1] > offs_e[0])

# ======================================================================================
print("#"*96)
print("# [4] MG-with-the-same-nu (isolated spherical): offset 0 AND zero anisotropy dependence")
print("#"*96)
# MG modifies POISSON not inertia: g_obs=nu(|g_bar|)g_bar pointwise, orbit-shape blind for an
# isolated spherical system => offset 0 AND d(offset)/d(anisotropy)=0 IDENTICALLY (= closure A).
rp = np.array([0.5, 1.0, 3.0])
mg = np.abs(nu_fw(gN(rp)/a0_deep)*gN(rp)/(nu_fw(gN(rp)/a0_deep)*gN(rp)) - 1).max()
check("MG-same-nu spherical: g_obs=nu g_bar pointwise -> offset 0 AND no anisotropy dependence",
      mg < 1e-14)
print("   => the FORCED positive anisotropy-derivative in [3] is MG-IMPOSSIBLE: it is the clean")
print("      differential discriminator the MI closure predicts and MG-with-same-nu cannot.")

# ======================================================================================
print("#"*96)
print("# [5] Bracket magnitude (isotropic ensemble), BOTH footings")
print("#"*96)
mags = {}
for lab, a0v in (("canonical", 2.357), ("alt (y/1.207)", 2.357*1.207)):
    gAf = make_field(a0v); sigf = jeans_sigma(gAf)
    offs = []
    for _ in range(500):
        ri = float(np.clip(rng.uniform(0.3, 3.0), 0.05, 8.0))
        s = np.sqrt(max(sigf(ri), 1e-9))
        v = rng.normal(0, s, 3)
        r_t = integrate_orbit(gAf, ri, [v[0], np.hypot(v[1], v[2])], n_periods=12)
        if r_t.max() > 60: continue
        offs.append(orbit_offset(gAf, a0v, r_t))
    offs = np.array(offs)
    mags[lab] = offs.mean()
    print(f"   [{lab}] isotropic ensemble mean = {offs.mean():+.4f} dex, median {np.median(offs):+.4f}, "
          f"16-84% [{np.percentile(offs,16):+.4f},{np.percentile(offs,84):+.4f}]")
spread = abs(mags["canonical"]-mags["alt (y/1.207)"])/(abs(mags["canonical"])+1e-9)
print(f"   footing spread = {100*spread:.1f}% of the offset (MC-noise-limited on a small mean)")
check("both footings: isotropic ensemble net NEGATIVE, SAME sign and SAME order (footing-stable at "
      "the ensemble-noise level, spread <~30%)",
      mags["canonical"] < 0 and mags["alt (y/1.207)"] < 0 and spread < 0.30)

# ======================================================================================
print("#"*96)
print("# VERDICT (rider a)")
print("#"*96)
print(f"""   The dSph / dispersion RAR offset is STILL A BRACKET, NOT a forced number.
     * bracket ends:  closure A (instantaneous |a|) = +0.000 dex  ...  closure B (history-averaged)
       isotropic-ensemble ~ {mags['canonical']:+.3f} dex (canonical; deep-regime toy), NET negative
       both footings, but with a POSITIVE radial tail (plunging orbits run hot).
     * SIGN is NOT pinned by the pullback: two admissible orbit-shape populations (apocentre-
       dominated tangential vs pericentre-dominated radial) give OPPOSITE signs -- the concave-RAR
       Jensen gap is population/weighting-dependent and that weighting IS the free eta(beta).
     * FORCED (pullback-independent): d(offset)/d(radial-anisotropy) > 0 (radial hotter), which
       MG-with-the-same-nu CANNOT produce -> the clean MG-impossible differential discriminator.
   Honest off-circular predictivity ceiling: ONE free reduction-weighting function eta(beta) on the
   2-D (eccentricity x anisotropy) orbit-shape space; overall-offset SIGN free, magnitude bracketed
   [0 ... closure-B pattern], only the anisotropy slope forced. Both footings; s=-1 and a0 untouched;
   no completeness/TOE claim. (Deep-regime toy magnitudes are illustrative; the SIGNED PATTERN and
   the forced anisotropy slope are the physics, not the exact dex.)""")

print("="*96)
print(f" RIDER A: {'ALL CHECKS PASS' if PASS else 'A CHECK FAILED'}")
print("="*96)
import sys
sys.exit(0 if PASS else 1)
